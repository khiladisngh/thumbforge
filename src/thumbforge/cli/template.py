"""``thumbforge template`` — inspect and validate thumbnail templates (ROADMAP P4.1)."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.markup import escape

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import emit, get_app_context
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
