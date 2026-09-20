"""Upsert semantics the rest of Phase 2 depends on (ROADMAP P2.3, PLAN.md §3)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import pytest

from thumbforge.core.errors import NotFoundError
from thumbforge.core.models import ChannelMeta, PlaylistItemMeta, PlaylistMeta, VideoMeta
from thumbforge.storage.db import get_engine, init_db, session_factory, session_scope
from thumbforge.storage.repositories import Repositories

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path


OWNER = "UC" + "o" * 22
OTHER = "UC" + "x" * 22


@pytest.fixture
def repos(tmp_path: Path) -> Iterator[Repositories]:
    """Repositories over a real migrated SQLite file: the constraints are under test."""
    db_file = tmp_path / "repos.sqlite3"
    init_db(db_file)
    engine = get_engine(db_file)
    factory = session_factory(engine)
    with session_scope(factory) as session:
        yield Repositories(session)
    engine.dispose()


def _channel(youtube_id: str = OWNER, title: str = "Owner") -> ChannelMeta:
    """A minimal valid channel, so each test states only the field it is about."""
    return ChannelMeta(youtube_id=youtube_id, title=title, url=f"https://yt/{youtube_id}")


def _video(suffix: str, *, channel_id: str | None = OWNER, **extra: object) -> VideoMeta:
    """A video whose YouTube id is `suffix` padded to the required 11 characters."""
    youtube_id = suffix.ljust(11, "z")
    return VideoMeta(
        youtube_id=youtube_id,
        title=f"Video {suffix}",
        url=f"https://youtu.be/{youtube_id}",
        channel_id=channel_id,
        **extra,  # type: ignore[arg-type]
    )


def _playlist(*videos: VideoMeta, title: str = "Series") -> PlaylistMeta:
    """A playlist over `videos`, numbered 1..n in the order given."""
    return PlaylistMeta(
        youtube_id="PL" + "p" * 16,
        title=title,
        url="https://yt/playlist",
        channel_id=OWNER,
        items=tuple(
            PlaylistItemMeta(video=video, position=index)
            for index, video in enumerate(videos, start=1)
        ),
    )


def test_upsert_keeps_the_row_id(repos: Repositories) -> None:
    """A re-fetch must not mint a new ULID: runs and assets reference it."""
    first = repos.channels.upsert(_channel(title="Before"))
    original_id = first.id

    second = repos.channels.upsert(_channel(title="After"))

    assert second.id == original_id
    assert second.title == "After"
    assert len(repos.channels.list()) == 1


def test_part_number_defaults_to_position(repos: Repositories) -> None:
    """The first video of a series is "Part 1" (`PLAN.md` §5.3)."""
    repos.store_playlist(_playlist(_video("a"), _video("b"), _video("c")), _channel())

    playlist = repos.playlists.resolve("PL" + "p" * 16)
    items = repos.playlists.items(playlist)
    assert [item.position for item in items] == [1, 2, 3]
    assert [item.part_number for item in items] == [1, 2, 3]


def test_renumbered_parts_survive_a_refetch(repos: Repositories) -> None:
    """`playlist renumber` writes `part_number`; a later fetch must not revert it.

    This is the only user edit Phase 2 can lose, and losing it silently would make
    `renumber` pointless for anyone who ever re-fetches.
    """
    meta = _playlist(_video("a"), _video("b"))
    repos.store_playlist(meta, _channel())
    playlist = repos.playlists.resolve(meta.youtube_id)
    items = repos.playlists.items(playlist)
    items[0].part_number = 7
    items[1].part_number = None
    items[0].part_label = "Intro"
    repos.session.flush()

    repos.store_playlist(meta, _channel())

    refetched = repos.playlists.items(repos.playlists.resolve(meta.youtube_id))
    assert [item.part_number for item in refetched] == [7, None]
    assert refetched[0].part_label == "Intro"


def test_reordering_videos_does_not_collide_on_position(repos: Repositories) -> None:
    """`UNIQUE(playlist_id, position)` makes an in-place swap a constraint violation."""
    first, second = _video("a"), _video("b")
    repos.store_playlist(_playlist(first, second), _channel())

    repos.store_playlist(_playlist(second, first), _channel())

    items = repos.playlists.items(repos.playlists.resolve("PL" + "p" * 16))
    assert [item.position for item in items] == [1, 2]
    assert [item.video.youtube_id for item in items] == [
        second.youtube_id,
        first.youtube_id,
    ]


def test_removed_items_are_reported_and_videos_kept(repos: Repositories) -> None:
    """A video dropped from a playlist keeps its row: its thumbnails are still real."""
    repos.store_playlist(_playlist(_video("a"), _video("b")), _channel())

    _, removed = repos.store_playlist(_playlist(_video("a")), _channel())

    assert removed == 1
    items = repos.playlists.items(repos.playlists.resolve("PL" + "p" * 16))
    assert len(items) == 1
    assert repos.videos.get("bzzzzzzzzzz") is not None


def test_duplicate_video_in_a_playlist_is_listed_once(repos: Repositories) -> None:
    """`UNIQUE(playlist_id, video_id)` cannot represent a repeat, so the first place wins."""
    video = _video("a")
    playlist = PlaylistMeta(
        youtube_id="PL" + "p" * 16,
        title="Series",
        url="https://yt/playlist",
        channel_id=OWNER,
        items=(
            PlaylistItemMeta(video=video, position=1),
            PlaylistItemMeta(video=_video("b"), position=2),
            PlaylistItemMeta(video=video, position=3),
        ),
    )

    repos.store_playlist(playlist, _channel())

    stored = repos.playlists.resolve(playlist.youtube_id)
    items = repos.playlists.items(stored)
    assert [item.position for item in items] == [1, 2]
    assert [item.video.youtube_id for item in items] == ["azzzzzzzzzz", "bzzzzzzzzzz"]
    # item_count must match the rows written, not the three entries fetched: `fetch` would
    # otherwise print "3 videos" above a two-row table and `playlist list` would agree.
    assert stored.item_count == 2


def test_foreign_channel_videos_are_not_linked(repos: Repositories) -> None:
    """A playlist mixes channels; linking each would cost one request per video (S11)."""
    repos.store_playlist(
        _playlist(_video("a", channel_id=OWNER), _video("b", channel_id=OTHER)),
        _channel(),
    )

    assert repos.videos.resolve("azzzzzzzzzz").channel is not None
    assert repos.videos.resolve("bzzzzzzzzzz").channel is None


def test_flat_refetch_does_not_erase_richer_video_fields(repos: Repositories) -> None:
    """A playlist entry carries no description or publish date (S11).

    Overwriting with the empty defaults would make a playlist re-fetch destroy what a
    single-video full extract had already stored.
    """
    published = datetime(2020, 5, 1, tzinfo=UTC)
    repos.store_video(
        _video("a", description="The full story", published_at=published, duration_s=120),
        _channel(),
    )

    repos.store_playlist(_playlist(_video("a")), _channel())

    video = repos.videos.resolve("azzzzzzzzzz")
    assert video.description == "The full story"
    assert video.published_at == published.isoformat()
    assert video.duration_s == 120


def test_resolve_accepts_a_ulid_or_a_youtube_id(repos: Repositories) -> None:
    """`video show` takes either, and the two are only distinguishable by trying."""
    stored = repos.store_video(_video("a"))

    assert repos.videos.resolve(stored.id).id == stored.id
    assert repos.videos.resolve("azzzzzzzzzz").id == stored.id


def test_resolve_raises_not_found_with_a_hint(repos: Repositories) -> None:
    """Exit 3 and an actionable hint, not an empty result (spec behaviour 4)."""
    with pytest.raises(NotFoundError) as caught:
        repos.videos.resolve("nope")
    assert caught.value.hint is not None

    with pytest.raises(NotFoundError):
        repos.playlists.resolve("nope")


def test_playlist_fetched_at_round_trips_as_aware_utc(repos: Repositories) -> None:
    """The freshness rule compares against `datetime.now(UTC)`; a naive value would raise."""
    assert repos.playlist_fetched_at("PL" + "p" * 16) is None

    fetched = datetime.now(UTC) - timedelta(hours=1)
    meta = _playlist(_video("a"))
    repos.store_playlist(meta.model_copy(update={"fetched_at": fetched}), _channel())

    stored = repos.playlist_fetched_at(meta.youtube_id)
    assert stored is not None
    assert stored.tzinfo is not None
    assert stored == fetched


def test_listing_can_be_scoped_to_a_channel(repos: Repositories) -> None:
    """`video list --channel` / `playlist list --channel` filter on the YouTube id."""
    repos.store_playlist(_playlist(_video("a")), _channel())
    repos.store_video(_video("b", channel_id=OTHER), _channel(OTHER, "Other"))

    assert [video.youtube_id for video in repos.videos.list(channel=OTHER)] == ["bzzzzzzzzzz"]
    assert len(repos.playlists.list(channel=OWNER)) == 1
    assert repos.playlists.list(channel=OTHER) == []


def test_list_limit_applies(repos: Repositories) -> None:
    """`--limit` must bound the query, not the rendering."""
    for suffix in "abc":
        repos.store_video(_video(suffix))

    assert len(repos.videos.list(limit=2)) == 2
