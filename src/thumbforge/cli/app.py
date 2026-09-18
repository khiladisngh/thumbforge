"""Root Typer application.

Phase 0 ships only ``--version``. Sub-apps (fetch, thumb, batch, ...) are registered here in
later phases; see docs/ROADMAP.md.
"""

from typing import Annotated

import typer

from thumbforge import __version__

app = typer.Typer(
    name="thumbforge",
    help="Generate consistent, spec-compliant YouTube thumbnails from a hero image and a playlist.",
    no_args_is_help=True,
    add_completion=True,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"thumbforge {__version__}")
        raise typer.Exit()


@app.callback()
def root(
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


def main() -> None:
    app()
