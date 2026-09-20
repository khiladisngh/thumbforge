"""Wiring and shared views for the YouTube metadata commands (ROADMAP P2.3).

`core.services` declares Protocols; the concrete `YtDlpSource` and `Repositories` are
chosen here, which is the injection point `PLAN.md` §2.2 describes.

The row and payload builders are shared because `fetch` and `playlist show --videos`
present the same playlist in the same shape, and two copies would drift. They read from
the **database**, never from the fetched snapshot: `part_number` can have been rewritten by
`playlist renumber`, and the cached path has no snapshot at all.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING

from thumbforge.cli._render import JsonValue
from thumbforge.core.enums import ChannelSource
from thumbforge.core.errors import SettingsError
from thumbforge.storage.db import get_engine, session_scope
from thumbforge.storage.repositories import Repositories

if TYPE_CHECKING:
    from collections.abc import Generator, Sequence
    from pathlib import Path

    from thumbforge.core.sources import MetadataSource
    from thumbforge.storage.models import Channel, Playlist, PlaylistItem, Video

#: Shown where a nullable column has no value, per `PLAN.md` §5.3.
EMPTY = "—"

#: A mutable JSON object under construction. `JsonValue` for the values rather than `Any`
#: keeps `emit`'s serialisability guarantee: a stray `Path` or `datetime` is a type error
#: here instead of a runtime failure in output someone parses.
type JsonPayload = dict[str, JsonValue]


def build_source(source: ChannelSource) -> MetadataSource:
    """Select a metadata source.

    The Data API source is a Phase 8 extra, so asking for it now is a usage error carrying
    the install hint rather than an import failure (spec behaviour 3).
    """
    if source is ChannelSource.API:
        msg = "the YouTube Data API source is not available yet"
        raise SettingsError(msg, hint="install the `api` extra (Phase 8)")

    from thumbforge.sources.ytdlp import YtDlpSource

    return YtDlpSource()


@contextmanager
def open_repositories(db_path: Path) -> Generator[Repositories]:
    """Open a session for one command, committing on success.

    `session_scope` owns the commit/rollback. The engine is disposed afterwards because an
    open SQLite handle keeps a file lock on Windows, which breaks `tmp_path` cleanup.
    """
    engine = get_engine(db_path)
    try:
        with session_scope(engine) as session:
            yield Repositories(session)
    finally:
        engine.dispose()


def lookup_key(reference: str) -> str:
    """Reduce a user-supplied reference to something a repository can look up.

    `video show`, `playlist show` and `playlist renumber` all accept a ULID, a YouTube id
    or a URL (spec behaviour 4), so pasting the same string that was fetched works. Only
    something URL-shaped is classified; a bare ULID or YouTube id is passed through and the
    repository decides which it is.
    """
    if "/" in reference or "." in reference:
        from thumbforge.core.urls import classify_url

        return classify_url(reference).youtube_id
    return reference


def item_rows(items: Sequence[PlaylistItem]) -> list[list[str]]:
    """`#`, `Part`, `Video ID`, `Title` rows for a playlist's items (`PLAN.md` §5.3)."""
    return [
        [
            str(item.position),
            EMPTY if item.part_number is None else str(item.part_number),
            item.video.youtube_id,
            item.video.title,
        ]
        for item in items
    ]


def item_payload(items: Sequence[PlaylistItem]) -> list[JsonPayload]:
    """The machine-readable form of the same rows."""
    return [
        {
            "position": item.position,
            "part_number": item.part_number,
            "part_label": item.part_label,
            "youtube_id": item.video.youtube_id,
            "title": item.video.title,
            "duration_s": item.video.duration_s,
        }
        for item in items
    ]


def playlist_payload(playlist: Playlist) -> JsonPayload:
    """Playlist fields common to `fetch`, `playlist list` and `playlist show`."""
    return {
        "id": playlist.id,
        "youtube_id": playlist.youtube_id,
        "title": playlist.title,
        "url": playlist.url,
        "item_count": playlist.item_count,
        "fetched_at": playlist.fetched_at,
    }


def video_payload(video: Video) -> JsonPayload:
    """Video fields common to `fetch`, `video list` and `video show`."""
    return {
        "id": video.id,
        "youtube_id": video.youtube_id,
        "title": video.title,
        "url": video.url,
        "duration_s": video.duration_s,
        "published_at": video.published_at,
        "source_thumbnail_url": video.source_thumbnail_url,
        "fetched_at": video.fetched_at,
    }


def channel_payload(channel: Channel) -> JsonPayload:
    """Channel fields common to every command that mentions one."""
    return {
        "id": channel.id,
        "youtube_id": channel.youtube_id,
        "title": channel.title,
        "url": channel.url,
        "fetched_at": channel.fetched_at,
    }


def duration(seconds: int | None) -> str:
    """Render a duration as `H:MM:SS`/`M:SS`, or `—` when yt-dlp reported none."""
    if seconds is None:
        return EMPTY
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"
