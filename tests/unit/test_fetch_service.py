"""`FetchService` decisions: kind dispatch, the freshness rule, and what each fetch writes.

The service is exercised against fakes rather than the database, because what is under test
is which calls it makes — the persistence itself is covered by `test_repositories.py`.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, ClassVar

import pytest

from thumbforge.core.enums import UrlKind
from thumbforge.core.errors import SourceError
from thumbforge.core.models import (
    ChannelMeta,
    PlaylistItemMeta,
    PlaylistMeta,
    ResolvedUrl,
    VideoMeta,
)
from thumbforge.core.services.fetch import DEFAULT_MAX_AGE, FetchService
from thumbforge.core.sources import MetadataSource
from thumbforge.core.urls import classify_url

if TYPE_CHECKING:
    from datetime import datetime as DateTime

OWNER = "UC" + "o" * 22
PLAYLIST = "PL" + "p" * 16
VIDEO = "dQw4w9WgXcQ"


class FakeSource:
    """A `MetadataSource` that records calls and returns canned metadata."""

    key: ClassVar[str] = "ytdlp"

    def __init__(self, *, playlist_owner: str | None = OWNER) -> None:
        self.calls: list[str] = []
        self._playlist_owner = playlist_owner

    async def resolve(self, url: str) -> ResolvedUrl:
        self.calls.append(f"resolve:{url}")
        return classify_url(url)

    async def fetch_video(self, youtube_id: str) -> VideoMeta:
        self.calls.append(f"video:{youtube_id}")
        return VideoMeta(
            youtube_id=youtube_id,
            title="A video",
            url=f"https://youtu.be/{youtube_id}",
            channel_id=OWNER,
        )

    async def fetch_playlist(self, youtube_id: str) -> PlaylistMeta:
        self.calls.append(f"playlist:{youtube_id}")
        return PlaylistMeta(
            youtube_id=youtube_id,
            title="A playlist",
            url="https://yt/playlist",
            channel_id=self._playlist_owner,
            items=(
                PlaylistItemMeta(
                    video=VideoMeta(youtube_id=VIDEO, title="One", url="u"), position=1
                ),
                PlaylistItemMeta(
                    video=VideoMeta(youtube_id="x" * 11, title="Two", url="u"), position=2
                ),
            ),
        )

    async def fetch_channel(self, youtube_id: str) -> ChannelMeta:
        self.calls.append(f"channel:{youtube_id}")
        return ChannelMeta(youtube_id=youtube_id, title="The channel", url="https://yt/c")


class FakeStore:
    """The `FetchStore` surface, recording what was written."""

    def __init__(self, *, fetched_at: DateTime | None = None, removed: int = 0) -> None:
        self.written: list[str] = []
        self._fetched_at = fetched_at
        self._removed = removed

    def store_video(self, meta: VideoMeta, channel: ChannelMeta | None = None) -> object:
        self.written.append(f"video:{meta.youtube_id}:channel={channel is not None}")
        return object()

    def store_playlist(self, meta: PlaylistMeta, channel: ChannelMeta) -> tuple[object, int]:
        self.written.append(f"playlist:{meta.youtube_id}:owner={channel.youtube_id}")
        return object(), self._removed

    def store_channel(self, meta: ChannelMeta) -> object:
        self.written.append(f"channel:{meta.youtube_id}")
        return object()

    def playlist_fetched_at(self, youtube_id: str) -> DateTime | None:
        return self._fetched_at


def test_fake_source_satisfies_the_protocol() -> None:
    """If the fake drifts from `MetadataSource`, these tests stop meaning anything."""
    assert isinstance(FakeSource(), MetadataSource)


async def test_video_url_fetches_the_video_and_its_channel() -> None:
    """A single video can afford the channel request, which populates `video.channel_id`."""
    source, store = FakeSource(), FakeStore()

    result = await FetchService(source, store).fetch(f"https://youtu.be/{VIDEO}")

    assert result.kind is UrlKind.VIDEO
    assert source.calls == [
        f"resolve:https://youtu.be/{VIDEO}",
        f"video:{VIDEO}",
        f"channel:{OWNER}",
    ]
    assert store.written == [f"video:{VIDEO}:channel=True"]
    assert (result.channels_stored, result.playlists_stored, result.videos_stored) == (1, 0, 1)


async def test_playlist_url_fetches_playlist_then_its_owner() -> None:
    """One playlist request plus one channel request, regardless of item count."""
    source, store = FakeSource(), FakeStore()

    result = await FetchService(source, store).fetch(
        f"https://www.youtube.com/playlist?list={PLAYLIST}"
    )

    assert result.kind is UrlKind.PLAYLIST
    assert source.calls[1:] == [f"playlist:{PLAYLIST}", f"channel:{OWNER}"]
    assert store.written == [f"playlist:{PLAYLIST}:owner={OWNER}"]
    assert result.videos_stored == 2


async def test_channel_url_does_not_enumerate_videos() -> None:
    """Channel-wide enumeration is a Phase 2 non-goal."""
    source, store = FakeSource(), FakeStore()

    result = await FetchService(source, store).fetch(f"https://www.youtube.com/channel/{OWNER}")

    assert result.kind is UrlKind.CHANNEL
    assert source.calls == [
        f"resolve:https://www.youtube.com/channel/{OWNER}",
        f"channel:{OWNER}",
    ]
    assert store.written == [f"channel:{OWNER}"]


async def test_recent_playlist_is_served_without_a_network_call() -> None:
    """Spec behaviour 2: a playlist fetched inside the window is not re-fetched."""
    source = FakeSource()
    store = FakeStore(fetched_at=datetime.now(UTC) - timedelta(hours=1))

    result = await FetchService(source, store).fetch(PLAYLIST)

    assert result.cached is True
    assert result.youtube_id == PLAYLIST
    assert source.calls == [f"resolve:{PLAYLIST}"]
    assert store.written == []
    assert (result.channels_stored, result.playlists_stored, result.videos_stored) == (0, 0, 0)


async def test_stale_playlist_is_refetched() -> None:
    """Just past the window the network call must happen again."""
    source = FakeSource()
    store = FakeStore(fetched_at=datetime.now(UTC) - DEFAULT_MAX_AGE - timedelta(minutes=1))

    result = await FetchService(source, store).fetch(PLAYLIST)

    assert result.cached is False
    assert store.written == [f"playlist:{PLAYLIST}:owner={OWNER}"]


async def test_refresh_overrides_a_fresh_copy() -> None:
    """`--refresh` must win even one second after a fetch."""
    source = FakeSource()
    store = FakeStore(fetched_at=datetime.now(UTC))

    result = await FetchService(source, store).fetch(PLAYLIST, refresh=True)

    assert result.cached is False
    assert f"playlist:{PLAYLIST}" in source.calls


async def test_freshness_only_applies_to_playlists() -> None:
    """A video fetch is one cheap request and always reflects the latest title."""
    source = FakeSource()
    store = FakeStore(fetched_at=datetime.now(UTC))

    result = await FetchService(source, store).fetch(VIDEO)

    assert result.cached is False
    assert f"video:{VIDEO}" in source.calls


async def test_playlist_without_an_owner_is_a_source_error() -> None:
    """`playlist.channel_id` is NOT NULL, so there is no row to write without it.

    Failing beats inventing a placeholder channel that later fetches would have to
    reconcile against the real one.
    """
    source, store = FakeSource(playlist_owner=None), FakeStore()

    with pytest.raises(SourceError) as caught:
        await FetchService(source, store).fetch(PLAYLIST)

    assert caught.value.hint is not None
    assert store.written == []


async def test_removed_item_count_is_reported() -> None:
    """`fetch` tells the user a re-fetch shrank the playlist."""
    service = FetchService(FakeSource(), FakeStore(removed=3))

    result = await service.fetch(PLAYLIST)

    assert result.removed_items == 3
