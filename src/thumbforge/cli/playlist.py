"""``thumbforge playlist`` — list and inspect stored playlists (ROADMAP P2.3)."""

from __future__ import annotations

from typing import Annotated, Any

import typer
from rich.console import Group

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import emit, get_app_context, kv, table
from thumbforge.cli._youtube import (
    channel_payload,
    item_payload,
    item_rows,
    open_repositories,
    playlist_payload,
)

app = typer.Typer(
    name="playlist",
    help="Inspect playlists already fetched into the database.",
    no_args_is_help=True,
)


@app.command("list")
@handle_errors
def list_(
    ctx: typer.Context,
    channel: Annotated[
        str | None,
        typer.Option("--channel", help="Restrict to one channel's YouTube id."),
    ] = None,
) -> None:
    """List stored playlists, most recently fetched first."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()

    with open_repositories(settings.db_path) as repos:
        playlists = repos.playlists.list(channel=channel)
        payload = [playlist_payload(playlist) for playlist in playlists]
        rows = [
            [
                playlist.youtube_id,
                str(playlist.item_count),
                playlist.channel.title,
                playlist.title,
            ]
            for playlist in playlists
        ]

    emit(
        app_ctx,
        {"playlists": payload, "count": len(payload)},
        render=lambda: table(["Playlist ID", "Videos", "Channel", "Title"], rows),
    )


@app.command("show")
@handle_errors
def show(
    ctx: typer.Context,
    reference: Annotated[str, typer.Argument(help="Playlist ULID, YouTube id, or URL.")],
    videos: Annotated[
        bool,
        typer.Option("--videos", help="Also list the playlist's items in order."),
    ] = False,
) -> None:
    """Show one playlist, optionally with its ordered items."""
    from thumbforge.core.urls import classify_url

    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()

    with open_repositories(settings.db_path) as repos:
        lookup = reference
        if "/" in reference or "." in reference:
            lookup = classify_url(reference).youtube_id
        playlist = repos.playlists.resolve(lookup)

        payload: dict[str, Any] = playlist_payload(playlist)
        payload["channel"] = channel_payload(playlist.channel)
        fields: dict[str, object] = {
            "Title": playlist.title,
            "YouTube id": playlist.youtube_id,
            "Videos": playlist.item_count,
            "Channel": playlist.channel.title,
            "URL": playlist.url,
            "Fetched": playlist.fetched_at,
        }
        summary = kv(fields, title=playlist.title)

        if not videos:
            emit(app_ctx, payload, render=lambda: summary)
            return

        items = repos.playlists.items(playlist)
        payload["videos"] = item_payload(items)
        rows = item_rows(items)

    emit(
        app_ctx,
        payload,
        render=lambda: Group(summary, table(["#", "Part", "Video ID", "Title"], rows)),
    )
