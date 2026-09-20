"""``thumbforge playlist`` — list and inspect stored playlists (ROADMAP P2.3)."""

from __future__ import annotations

from typing import Annotated

import typer
from rich.console import Group

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import emit, get_app_context, kv, table
from thumbforge.cli._youtube import (
    EMPTY,
    channel_payload,
    item_payload,
    item_rows,
    lookup_key,
    open_repositories,
    playlist_payload,
)
from thumbforge.core.json import JsonPayload

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
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()

    with open_repositories(settings.db_path) as repos:
        lookup = lookup_key(reference)
        playlist = repos.playlists.resolve(lookup)

        payload: JsonPayload = playlist_payload(playlist)
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


@app.command("renumber")
@handle_errors
def renumber(
    ctx: typer.Context,
    reference: Annotated[str, typer.Argument(help="Playlist ULID, YouTube id, or URL.")],
    start: Annotated[
        int,
        typer.Option("--start", help="First part number to assign, in playlist order."),
    ] = 1,
    skip_ids: Annotated[
        str | None,
        typer.Option(
            "--skip-ids",
            help="Comma-separated YouTube video ids to leave unnumbered.",
        ),
    ] = None,
) -> None:
    """Reassign part numbers sequentially, optionally leaving some videos unnumbered.

    Skipped videos are not counted, so the remaining parts stay consecutive — the point of
    skipping a trailer or an outro rather than removing it from the playlist.
    """
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    skipped = [item.strip() for item in (skip_ids or "").split(",") if item.strip()]

    with open_repositories(settings.db_path) as repos:
        playlist = repos.playlists.resolve(lookup_key(reference))
        changes = repos.playlists.renumber(playlist, start=start, skip_ids=skipped)

        payload: JsonPayload = {
            "playlist": playlist_payload(playlist),
            "start": start,
            "skipped": skipped,
            "items": [
                {
                    "position": change.position,
                    "youtube_id": change.youtube_id,
                    "title": change.title,
                    "before": change.before,
                    "after": change.after,
                }
                for change in changes
            ],
        }
        rows = [
            [
                str(change.position),
                EMPTY if change.before is None else str(change.before),
                EMPTY if change.after is None else str(change.after),
                change.youtube_id,
                change.title,
            ]
            for change in changes
        ]

    emit(
        app_ctx,
        payload,
        render=lambda: table(["#", "Was", "Now", "Video ID", "Title"], rows),
    )
