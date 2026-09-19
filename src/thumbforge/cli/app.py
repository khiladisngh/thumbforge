"""Root Typer application: global flags, context construction, sub-app registration.

Commands live in sibling modules and stay thin — parse input, call a service, render. Sub-apps
(`config`, `db`, `fetch`, `thumb`, `batch`, ...) are registered here as their phases land, and
`--data-dir` / `-v` / `--quiet` are added by the settings and logging tasks that give them
meaning; see docs/ROADMAP.md.
"""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from thumbforge import __version__
from thumbforge.cli import config as config_cli
from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import AppContext
from thumbforge.core.errors import SettingsError
from thumbforge.logging import configure_logging, get_logger, level_from_flags
from thumbforge.settings import Settings, load_settings

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
@handle_errors
def root(
    ctx: typer.Context,
    config: Annotated[
        Path | None,
        typer.Option("--config", envvar="THUMBFORGE_CONFIG", help="Path to config.toml."),
    ] = None,
    data_dir: Annotated[
        Path | None,
        typer.Option("--data-dir", help="Override the data directory (database and assets)."),
    ] = None,
    json_mode: Annotated[
        bool,
        typer.Option("--json", help="Emit a single JSON document instead of Rich output."),
    ] = False,
    verbose: Annotated[
        int,
        typer.Option("-v", "--verbose", count=True, help="-v for INFO, -vv for DEBUG."),
    ] = 0,
    quiet: Annotated[bool, typer.Option("--quiet", help="Only log errors.")] = False,
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
    # Set the context before anything that can fail: handle_errors reads it to decide between
    # JSON and Rich diagnostics, and a broken config.toml must still report as JSON under
    # --json.
    ctx.obj = AppContext(
        console=console,
        json_mode=json_mode,
        config_path=config,
        data_dir=data_dir,
    )

    # A broken config.toml must not block the commands that repair it. `config init --force`
    # and `config set` rewrite the file and never read the parsed settings, so the failure is
    # captured and re-raised only when a command actually asks for settings.
    settings: Settings | None = None
    settings_error: SettingsError | None = None
    try:
        settings = load_settings(config_path=config, data_dir=data_dir)
    except SettingsError as error:
        settings_error = error

    defaults = settings if settings is not None else Settings()
    configure_logging(
        level=level_from_flags(
            verbose=verbose,
            quiet=quiet,
            configured=defaults.logging.level,
        ),
        # --json implies JSON logs: a machine reading stdout should not have to parse
        # human-formatted diagnostics on stderr.
        fmt="json" if json_mode else defaults.logging.format,
        log_file=defaults.log_file,
        color=not (no_color or json_mode),
    )
    ctx.obj = replace(ctx.obj, settings=settings, settings_error=settings_error)

    get_logger(__name__).debug(
        "cli configured",
        config=str(config) if config else None,
        data_dir=str(defaults.general.data_dir),
        command=ctx.invoked_subcommand,
        version=__version__,
        config_error=str(settings_error) if settings_error else None,
    )


app.add_typer(config_cli.app)


def main() -> None:
    app()
