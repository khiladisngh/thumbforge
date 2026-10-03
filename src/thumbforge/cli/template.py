"""``thumbforge template`` — list, show, copy, import, validate and render templates.

ROADMAP P4.1, P4.2, P4.4. Templates live in the database as immutable versions; the loader
in ``templates/loader.py`` owns references and versioning, this module only does I/O.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Annotated

import typer
from rich.console import Group
from rich.markup import escape
from rich.text import Text

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import AppContext, emit, get_app_context, kv, table
from thumbforge.cli._runs import parse_vars
from thumbforge.cli._youtube import lookup_key, open_repositories
from thumbforge.core.models import PlaylistMeta
from thumbforge.settings import default_config_path
from thumbforge.storage.repositories import channel_meta, video_meta
from thumbforge.templates.loader import (
    check_name,
    import_template,
    parse_ref,
    resolve,
    validate_files,
    write_copy,
)
from thumbforge.templates.render import RenderContext, render_prompt
from thumbforge.templates.schema import dump_layout

if TYPE_CHECKING:
    from thumbforge.core.json import JsonPayload
    from thumbforge.core.layout import LayoutSpec, Template
    from thumbforge.storage.models import Video

app = typer.Typer(
    name="template",
    help="Inspect, validate, and manage thumbnail templates.",
    no_args_is_help=True,
)

_REF_HELP = "NAME (latest version) or NAME@VERSION."


@app.command("list")
@handle_errors
def list_(ctx: typer.Context) -> None:
    """List every stored template version."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    with open_repositories(settings.db_path) as repos:
        templates = repos.templates.list()

    payload: list[JsonPayload] = [_summary(t) for t in templates]
    rows = [[escape(t.name), str(t.version), "yes" if t.is_builtin else "no"] for t in templates]
    emit(
        app_ctx,
        {"templates": payload, "count": len(payload)},
        render=lambda: table(["Name", "Version", "Builtin"], rows),
    )


@app.command("show")
@handle_errors
def show(
    ctx: typer.Context,
    ref: Annotated[str, typer.Argument(help=_REF_HELP)],
) -> None:
    """Print a stored template's prompt and layout spec."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    parsed = parse_ref(ref)
    with open_repositories(settings.db_path) as repos:
        template = resolve(repos.templates, parsed)

    payload = _summary(template)
    payload["prompt"] = template.prompt_template
    payload["layout"] = template.layout.model_dump(mode="json")
    emit(
        app_ctx,
        payload,
        # Text, not str: prompts and TOML contain `[...]`, which Rich would read as markup.
        render=lambda: Group(
            kv(
                {
                    "Builtin": "yes" if template.is_builtin else "no",
                    "Description": escape(template.layout.template.description),
                    "Spec hash": template.spec_hash,
                },
                title=escape(template.ref),
            ),
            Text("\nPrompt", style="bold"),
            Text(template.prompt_template),
            Text("\nLayout", style="bold"),
            Text(dump_layout(template.layout)),
        ),
    )


@app.command("new")
@handle_errors
def new(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument(help="Name of the new template and its files.")],
    from_: Annotated[
        str, typer.Option("--from", help=f"Stored template to copy: {_REF_HELP}")
    ] = "minimal",
) -> None:
    """Copy a stored template to <config_dir>/templates/NAME.toml + NAME.j2 for editing."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    check_name(name)
    source_ref = parse_ref(from_)
    with open_repositories(settings.db_path) as repos:
        source = resolve(repos.templates, source_ref)

    toml_path, j2_path = write_copy(source, name, _templates_dir(app_ctx))
    emit(
        app_ctx,
        {
            "status": "ok",
            "template": name,
            "from": source.ref,
            "layout_path": str(toml_path),
            "prompt_path": str(j2_path),
        },
        render=lambda: (
            f"[green]created[/] [cyan]{escape(name)}[/] from {escape(source.ref)}: "
            f"{escape(str(toml_path))}, {escape(str(j2_path))}"
        ),
    )


@app.command("import")
@handle_errors
def import_(
    ctx: typer.Context,
    path: Annotated[
        Path,
        typer.Argument(
            help="X.toml with a sibling X.j2, the stem X, or a directory with one pair."
        ),
    ],
) -> None:
    """Store a template as a new version; identical content returns the stored row."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    with open_repositories(settings.db_path) as repos:
        template, created = import_template(repos.templates, path)

    payload = _summary(template)
    payload["status"] = "imported" if created else "unchanged"
    emit(
        app_ctx,
        payload,
        render=lambda: (
            f"[green]imported[/] [cyan]{escape(template.ref)}[/] ({template.spec_hash[:12]})"
            if created
            else f"[yellow]already stored as[/] [cyan]{escape(template.ref)}[/] "
            f"({template.spec_hash[:12]})"
        ),
    )


@app.command("validate")
@handle_errors
def validate(
    ctx: typer.Context,
    path: Annotated[
        Path,
        typer.Argument(help="Layout spec TOML; a sibling .j2 prompt is checked for Jinja syntax."),
    ],
) -> None:
    """Validate a template layout spec against the schema, and its sibling prompt if any."""
    app_ctx = get_app_context(ctx)
    layout, prompt_path = validate_files(path)
    emit(
        app_ctx,
        {
            "status": "ok",
            "path": str(path),
            "template": layout.template.name,
            "prompt_path": None if prompt_path is None else str(prompt_path),
        },
        render=lambda: (
            f"[green]ok[/] {escape(str(path))} ([cyan]{escape(layout.template.name)}[/])"
        ),
    )


@app.command("render")
@handle_errors
def render(
    ctx: typer.Context,
    ref: Annotated[str, typer.Argument(help=f"Stored template: {_REF_HELP}")],
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
    parsed = parse_ref(ref)
    variables = parse_vars(var or [])

    with open_repositories(settings.db_path) as repos:
        template = resolve(repos.templates, parsed)
        render_ctx = _render_context(
            repos.videos.resolve(lookup_key(video)), template.layout, part, variables
        )

    rendered = render_prompt(template.prompt_template, render_ctx, name=template.ref)
    # Text, not str: Rich would read `[...]` in a prompt as markup and drop it.
    emit(app_ctx, {"template": template.ref, "prompt": rendered}, render=lambda: Text(rendered))


def _summary(template: Template) -> JsonPayload:
    return {
        "template": template.ref,
        "name": template.name,
        "version": template.version,
        "builtin": template.is_builtin,
        "spec_hash": template.spec_hash,
    }


def _templates_dir(app_ctx: AppContext) -> Path:
    """``<config_dir>/templates``, next to the ``config.toml`` in use."""
    return (app_ctx.config_path or default_config_path()).parent / "templates"


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
        video=video_meta(row),
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
        channel=None if channel is None else channel_meta(channel),
        vars=variables,
        negative_space=layout.negative_space.hint,
        width=layout.canvas.width,
        height=layout.canvas.height,
    )
