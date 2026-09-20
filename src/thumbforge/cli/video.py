"""``thumbforge video`` — list and inspect stored videos (ROADMAP P2.3)."""

from __future__ import annotations

from typing import Annotated, Any

import typer

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import emit, get_app_context, kv, table
from thumbforge.cli._youtube import (
    EMPTY,
    channel_payload,
    duration,
    open_repositories,
    video_payload,
)

app = typer.Typer(
    name="video",
    help="Inspect videos already fetched into the database.",
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
    limit: Annotated[
        int | None,
        typer.Option("--limit", min=1, help="Maximum number of videos to show."),
    ] = None,
) -> None:
    """List stored videos, most recently fetched first."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()

    with open_repositories(settings.db_path) as repos:
        videos = repos.videos.list(channel=channel, limit=limit)
        payload = [video_payload(video) for video in videos]
        rows = [
            [
                video.youtube_id,
                duration(video.duration_s),
                EMPTY if video.channel is None else video.channel.title,
                video.title,
            ]
            for video in videos
        ]

    emit(
        app_ctx,
        {"videos": payload, "count": len(payload)},
        render=lambda: table(["Video ID", "Length", "Channel", "Title"], rows),
    )


@app.command("show")
@handle_errors
def show(
    ctx: typer.Context,
    reference: Annotated[str, typer.Argument(help="Video ULID, YouTube id, or URL.")],
) -> None:
    """Show one video's metadata.

    Accepts a ULID, a YouTube id or a URL; a URL is classified first so that pasting the
    same thing that was fetched works (spec behaviour 4).
    """
    from thumbforge.core.urls import classify_url

    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()

    with open_repositories(settings.db_path) as repos:
        lookup = reference
        if "/" in reference or "." in reference:
            lookup = classify_url(reference).youtube_id
        video = repos.videos.resolve(lookup)

        payload: dict[str, Any] = video_payload(video)
        if video.channel is not None:
            payload["channel"] = channel_payload(video.channel)
        payload["playlists"] = [
            {
                "youtube_id": item.playlist.youtube_id,
                "title": item.playlist.title,
                "position": item.position,
                "part_number": item.part_number,
            }
            for item in video.playlist_items
        ]
        fields: dict[str, object] = {
            "Title": video.title,
            "YouTube id": video.youtube_id,
            "Length": duration(video.duration_s),
            "Channel": EMPTY if video.channel is None else video.channel.title,
            "Published": video.published_at or EMPTY,
            "URL": video.url,
            "Thumbnail": video.source_thumbnail_url or EMPTY,
            "Fetched": video.fetched_at,
            "Playlists": len(payload["playlists"]),
        }

    emit(app_ctx, payload, render=lambda: kv(fields, title=video.title))
