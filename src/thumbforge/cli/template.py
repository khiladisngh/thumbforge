"""``thumbforge template`` — validate and render thumbnail templates (ROADMAP P4.1, P4.2)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer
from rich.markup import escape
from rich.text import Text

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import emit, get_app_context
from thumbforge.cli._youtube import lookup_key, open_repositories
from thumbforge.core.errors import NotFoundError, TemplateError
from thumbforge.core.layout import LayoutSpec
from thumbforge.core.models import ChannelMeta, PlaylistMeta, VideoMeta
from thumbforge.settings import default_config_path
from thumbforge.storage.models import Video
from thumbforge.templates.render import RenderContext, render_prompt
from thumbforge.templates.schema import load_layout

app = typer.Typer(
    name="template",
    help="Inspect, validate, and manage thumbnail templates.",
    no_args_is_help=True,
)


@app.command("validate")
@handle_errors
def validate(
    ctx: typer.Context,
    path: Annotated[Path, typer.Argument(help="Path to the layout spec TOML file to validate.")],
) -> None:
    """Validate a template layout spec against the schema."""
    app_ctx = get_app_context(ctx)
    layout = load_layout(path)
    emit(
        app_ctx,
        {
            "status": "ok",
            "path": str(path),
            "template": layout.template.name,
        },
        render=lambda: (
            f"[green]ok[/] {escape(str(path))} ([cyan]{escape(layout.template.name)}[/])"
        ),
    )


@app.command("render")
@handle_errors
def render(
    ctx: typer.Context,
    name: Annotated[
        str, typer.Argument(help="Template name: NAME.toml + NAME.j2 in the config dir.")
    ],
    video: Annotated[str, typer.Option("--video", help="Video ULID, YouTube id, or URL.")],
    part: Annotated[
        int | None,
        typer.Option("--part", min=1, help="Part number; defaults to the video's playlist part."),
    ] = None,
    var: Annotated[
        list[str] | None,
        typer.Option("--var", help="key=value for {{ vars.key }}; repeatable."),
    ] = None,
) -> None:
    """Print a template's rendered prompt for a stored video. No provider is called."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    templates_dir = (app_ctx.config_path or default_config_path()).parent / "templates"
    layout, prompt = _read_template(name, templates_dir)
    variables = _parse_vars(var or [])

    with open_repositories(settings.db_path) as repos:
        render_ctx = _render_context(
            repos.videos.resolve(lookup_key(video)), layout, part, variables
        )

    rendered = render_prompt(prompt, render_ctx, name=name)
    # Text, not str: Rich would read `[...]` in a prompt as markup and drop it.
    emit(app_ctx, {"template": name, "prompt": rendered}, render=lambda: Text(rendered))


def _read_template(name: str, templates_dir: Path) -> tuple[LayoutSpec, str]:
    """Load ``NAME.toml`` and ``NAME.j2``. Replaced by the database loader in P4.4."""
    if Path(name).name != name:
        msg = f"template name {name!r} must not contain a path"
        raise TemplateError(msg)
    layout_path = templates_dir / f"{name}.toml"
    prompt_path = templates_dir / f"{name}.j2"
    if not (layout_path.is_file() and prompt_path.is_file()):
        msg = f"template {name!r} not found"
        raise NotFoundError(
            msg, hint=f"expected {layout_path.name} and {prompt_path.name} in {templates_dir}"
        )
    layout = load_layout(layout_path)
    try:
        return layout, prompt_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as err:
        msg = f"Cannot read prompt {prompt_path}: {err}"
        raise TemplateError(msg) from err


def _parse_vars(pairs: list[str]) -> dict[str, str]:
    variables: dict[str, str] = {}
    for pair in pairs:
        key, separator, value = pair.partition("=")
        if not separator or not key:
            msg = f"--var expects key=value, got {pair!r}"
            raise TemplateError(msg)
        variables[key] = value
    return variables


def _render_context(
    row: Video, layout: LayoutSpec, part: int | None, variables: dict[str, str]
) -> RenderContext:
    """Build the render context from a stored video.

    A video in exactly one playlist supplies the playlist, its part number and label; in
    none or several there is nothing unambiguous to supply, so only ``--part`` applies.
    """
    item = row.playlist_items[0] if len(row.playlist_items) == 1 else None
    channel = row.channel
    return RenderContext(
        video=VideoMeta(
            youtube_id=row.youtube_id,
            title=row.title,
            url=row.url,
            channel_id=None if channel is None else channel.youtube_id,
            description=row.description,
            duration_s=row.duration_s,
            published_at=None
            if row.published_at is None
            else datetime.fromisoformat(row.published_at),
            source_thumbnail_url=row.source_thumbnail_url,
            fetched_at=datetime.fromisoformat(row.fetched_at),
        ),
        playlist=None
        if item is None
        else PlaylistMeta(
            youtube_id=item.playlist.youtube_id,
            title=item.playlist.title,
            url=item.playlist.url,
            description=item.playlist.description,
            fetched_at=datetime.fromisoformat(item.playlist.fetched_at),
        ),
        part_number=part if part is not None or item is None else item.part_number,
        part_label=None if item is None else item.part_label,
        channel=None
        if channel is None
        else ChannelMeta(
            youtube_id=channel.youtube_id,
            title=channel.title,
            url=channel.url,
            source=channel.source,
            fetched_at=datetime.fromisoformat(channel.fetched_at),
        ),
        vars=variables,
        negative_space=layout.negative_space.hint,
        width=layout.canvas.width,
        height=layout.canvas.height,
    )
