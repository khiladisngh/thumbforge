"""Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from thumbforge.core.enums import ChannelSource, UrlKind
from thumbforge.core.models import (
    ChannelMeta,
    PlaylistItemMeta,
    PlaylistMeta,
    ResolvedUrl,
    VideoMeta,
)


def _video(youtube_id: str = "dQw4w9WgXcQ") -> VideoMeta:
    """A minimal valid video, so each test states only the field it is about."""
    return VideoMeta(youtube_id=youtube_id, title="A video", url=f"https://youtu.be/{youtube_id}")


def test_snapshots_are_frozen() -> None:
    """A fetched snapshot is a value; mutating one would desync it from `fetched_at`."""
    video = _video()
    with pytest.raises(ValidationError):
        video.title = "changed"  # type: ignore[misc]


def test_unknown_upstream_field_is_rejected() -> None:
    """`extra="forbid"` turns an unexpected yt-dlp field into a loud failure.

    yt-dlp's info dict changes shape between releases; silently dropping a renamed field
    would surface later as missing metadata instead of at the boundary.
    """
    with pytest.raises(ValidationError):
        VideoMeta(youtube_id="x" * 11, title="t", url="u", chanel_id="typo")  # type: ignore[call-arg]


def test_naive_fetched_at_is_rejected() -> None:
    """`fetched_at` is persisted as ISO-8601 UTC, so a naive datetime is ambiguous."""
    with pytest.raises(ValidationError, match="timezone-aware"):
        ChannelMeta(
            youtube_id="UC" + "x" * 22,
            title="c",
            url="u",
            fetched_at=datetime(2026, 1, 1, 12, 0, 0),  # deliberately naive
        )


def test_aware_fetched_at_is_normalised_to_utc() -> None:
    """Offsets are preserved as an instant, then stored in UTC."""
    meta = ChannelMeta(
        youtube_id="UC" + "x" * 22,
        title="c",
        url="u",
        fetched_at=datetime(2026, 1, 1, 12, 0, tzinfo=timezone(timedelta(hours=5, minutes=30))),
    )
    assert meta.fetched_at.tzinfo is UTC
    assert meta.fetched_at == datetime(2026, 1, 1, 6, 30, tzinfo=UTC)


def test_defaults_match_the_schema() -> None:
    """Optional columns default to the values the `video` table expects."""
    video = _video()
    assert video.source is ChannelSource.YTDLP
    assert video.description == ""
    assert video.duration_s is None
    assert video.channel_id is None
    assert video.fetched_at.tzinfo is UTC


def test_negative_duration_is_rejected() -> None:
    """`duration_s` is a length; a negative value would corrupt part numbering downstream."""
    with pytest.raises(ValidationError):
        VideoMeta(youtube_id="x" * 11, title="t", url="u", duration_s=-1)


def test_playlist_position_is_one_based() -> None:
    """`position` mirrors yt-dlp's 1-based `playlist_index`; 0 would break part numbering."""
    with pytest.raises(ValidationError):
        PlaylistItemMeta(video=_video(), position=0)


def test_item_count_tracks_items() -> None:
    """`item_count` feeds the `playlist.item_count` column, so it must not drift."""
    playlist = PlaylistMeta(
        youtube_id="PL" + "x" * 16,
        title="p",
        url="u",
        items=(
            PlaylistItemMeta(video=_video("aaaaaaaaaaa"), position=1),
            PlaylistItemMeta(video=_video("bbbbbbbbbbb"), position=2),
        ),
    )
    assert playlist.item_count == 2
    assert PlaylistMeta(youtube_id="PL" + "x" * 16, title="p", url="u").item_count == 0


def test_resolved_url_carries_kind_and_id() -> None:
    """`resolve()` returns both halves (ADR 0005); an empty id is never a valid result."""
    resolved = ResolvedUrl(kind=UrlKind.PLAYLIST, youtube_id="PL" + "x" * 16)
    assert resolved.kind is UrlKind.PLAYLIST
    with pytest.raises(ValidationError):
        ResolvedUrl(kind=UrlKind.VIDEO, youtube_id="")
