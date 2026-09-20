"""``thumbforge fetch`` — pull YouTube metadata into the database (ROADMAP P2.3)."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Annotated

import typer
from rich.console import Group

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import emit, get_app_context, panel, table
from thumbforge.cli._youtube import (
    JsonPayload,
    build_source,
    channel_payload,
    item_payload,
    item_rows,
    open_repositories,
    playlist_payload,
    video_payload,
)
from thumbforge.core.enums import ChannelSource, UrlKind
from thumbforge.core.errors import NotFoundError
from thumbforge.core.services.fetch import FetchService

if TYPE_CHECKING:
    from rich.console import RenderableType

    from thumbforge.core.services.fetch import FetchResult
    from thumbforge.storage.repositories import Repositories


def _summary(result: FetchResult) -> str:
    """The ``Stored N channel, N playlist, N videos.`` line from ``PLAN.md`` §5.3."""
    if result.cached:
        return "[yellow](cached)[/] nothing fetched — pass [cyan]--refresh[/] to force one"
    line = (
        f"[green]Stored[/] {result.channels_stored} channel, "
        f"{result.playlists_stored} playlist, {result.videos_stored} videos."
    )
    if result.removed_items:
        line += f" [yellow]{result.removed_items} item(s) left the playlist.[/]"
    return line


def _view(result: FetchResult, repos: Repositories) -> tuple[JsonPayload, RenderableType]:
    """Build the JSON payload and the Rich renderable from the **stored** rows.

    Reading the database rather than the fetched snapshot is what makes the cached path
    render the same table (spec acceptance criteria) and what keeps a `playlist renumber`
    visible in `Part` instead of being overwritten by the position.
    """
    payload: JsonPayload = {
        "kind": result.kind.value,
        "youtube_id": result.youtube_id,
        "cached": result.cached,
        "stored": {
            "channels": result.channels_stored,
            "playlists": result.playlists_stored,
            "videos": result.videos_stored,
        },
    }
    if result.removed_items:
        payload["removed_items"] = result.removed_items

    match result.kind:
        case UrlKind.PLAYLIST:
            playlist = repos.playlists.resolve(result.youtube_id)
            items = repos.playlists.items(playlist)
            payload["playlist"] = playlist_payload(playlist)
            payload["channel"] = channel_payload(playlist.channel)
            payload["videos"] = item_payload(items)
            # The marker goes in the panel *title*: appended to the body it lands past the
            # terminal width for a long playlist name and is silently clipped.
            head = panel(
                "Playlist (cached)" if result.cached else "Playlist",
                f"{playlist.title}   {playlist.youtube_id}   "
                f"{playlist.item_count} videos   {playlist.channel.title}",
            )
            body = table(["#", "Part", "Video ID", "Title"], item_rows(items))
            return payload, Group(head, body)

        case UrlKind.VIDEO:
            video = repos.videos.resolve(result.youtube_id)
            payload["video"] = video_payload(video)
            if video.channel is not None:
                payload["channel"] = channel_payload(video.channel)
            return payload, panel("Video", f"{video.title}   {video.youtube_id}")

        case UrlKind.CHANNEL:
            channel = repos.channels.get(result.youtube_id)
            if channel is None:  # pragma: no cover - the fetch just wrote this row
                msg = f"channel {result.youtube_id!r}"
                raise NotFoundError(msg)
            payload["channel"] = channel_payload(channel)
            return payload, panel("Channel", f"{channel.title}   {channel.youtube_id}")


@handle_errors
def fetch(
    ctx: typer.Context,
    url: Annotated[str, typer.Argument(help="Video, playlist or channel URL, or a bare id.")],
    source: Annotated[
        ChannelSource, typer.Option("--source", help="Metadata source to use.")
    ] = ChannelSource.YTDLP,
    refresh: Annotated[
        bool, typer.Option("--refresh", help="Re-fetch even when the stored copy is recent.")
    ] = False,
) -> None:
    """Fetch a video, playlist or channel and store its metadata."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    metadata_source = build_source(source)

    with open_repositories(settings.db_path) as repos:
        service = FetchService(metadata_source, repos)
        # One `asyncio.run` per invocation: the CLI is the only sync/async boundary.
        result = asyncio.run(service.fetch(url, refresh=refresh))
        payload, renderable = _view(result, repos)

    emit(app_ctx, payload, render=lambda: renderable)
    if not app_ctx.json_mode:
        app_ctx.console.print(_summary(result))
