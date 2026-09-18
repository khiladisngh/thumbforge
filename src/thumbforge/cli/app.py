"""Root Typer application: global flags, context construction, sub-app registration.

Commands live in sibling modules and stay thin — parse input, call a service, render. Sub-apps
(`config`, `db`, `fetch`, `thumb`, `batch`, ...) are registered here as their phases land, and
`--data-dir` / `-v` / `--quiet` are added by the settings and logging tasks that give them
meaning; see docs/ROADMAP.md.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from thumbforge import __version__
from thumbforge.cli._render import AppContext

app = typer.Typer(
    name="thumbforge",
    help="Generate consistent, spec-compliant YouTube thumbnails from a hero image and a playlist.",
    no_args_is_help=True,
    rich_markup_mode="rich",
    add_completion=True,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"thumbforge {__version__}")
        raise typer.Exit()


@app.callback()
def root(
    ctx: typer.Context,
    config: Annotated[
        Path | None,
        typer.Option("--config", envvar="THUMBFORGE_CONFIG", help="Path to config.toml."),
    ] = None,
    json_mode: Annotated[
        bool,
        typer.Option("--json", help="Emit a single JSON document instead of Rich output."),
    ] = False,
    no_color: Annotated[bool, typer.Option("--no-color", help="Disable colour output.")] = False,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Print the version and exit.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """thumbforge command-line interface."""
    console = Console(
        file=sys.stdout,
        no_color=no_color or json_mode,
        highlight=not json_mode,
    )
    ctx.obj = AppContext(console=console, json_mode=json_mode, config_path=config)


def main() -> None:
    app()
