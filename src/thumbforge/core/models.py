"""Boundary models for YouTube metadata (PLAN.md §3, ADR 0005).

These mirror the `channel`, `playlist` and `video` columns but are *not* ORM rows: a
`MetadataSource` produces them from an upstream API, and `storage/repositories.py` upserts
them. Keeping the two apart is what lets the Data API source (Phase 8) satisfy the same
Protocol without touching the schema. Frozen, because a fetched snapshot is a value.
"""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from thumbforge.core.enums import ChannelSource, UrlKind


def _utcnow() -> datetime:
    return datetime.now(UTC)


class _Meta(BaseModel):
    """Shared configuration and provenance for every fetched snapshot."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    youtube_id: str = Field(min_length=1)
    title: str
    url: str = Field(min_length=1)
    source: ChannelSource = ChannelSource.YTDLP
    fetched_at: datetime = Field(default_factory=_utcnow)

    @field_validator("fetched_at")
    @classmethod
    def _require_timezone(cls, value: datetime) -> datetime:
        """Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC."""
        if value.tzinfo is None:
            msg = "fetched_at must be timezone-aware"
            raise ValueError(msg)
        return value.astimezone(UTC)


class ChannelMeta(_Meta):
    """A fetched YouTube channel."""


class VideoMeta(_Meta):
    """A fetched YouTube video.

    `channel_id` is the channel's *YouTube* id, not a thumbforge ULID; the repository
    resolves it to a row. It is optional because `extract_flat` playlist entries may omit
    it (spike S11).
    """

    channel_id: str | None = None
    description: str = ""
    duration_s: int | None = Field(default=None, ge=0)
    published_at: datetime | None = None
    source_thumbnail_url: str | None = None


class PlaylistItemMeta(BaseModel):
    """One video's place in a playlist."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    video: VideoMeta
    position: int = Field(ge=1, description="1-based index from yt-dlp's playlist_index")


class PlaylistMeta(_Meta):
    """A fetched YouTube playlist and its ordered items."""

    channel_id: str | None = None
    description: str = ""
    items: tuple[PlaylistItemMeta, ...] = ()

    @property
    def item_count(self) -> int:
        """Number of items fetched, for the `playlist.item_count` column."""
        return len(self.items)


class ResolvedUrl(BaseModel):
    """What a URL or bare identifier turned out to be (ADR 0005)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: UrlKind
    youtube_id: str = Field(min_length=1)
