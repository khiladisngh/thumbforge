"""``thumbforge runs`` — inspect generation runs (ROADMAP P6.1).

Only `show` exists so far; `list`, `resume`, `cancel` and `delete` arrive with P7.4.
"""

from __future__ import annotations

from typing import Annotated

import typer

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import emit, get_app_context
from thumbforge.cli._runs import open_run_store, run_view

app = typer.Typer(
    name="runs",
    help="Inspect generation runs.",
    no_args_is_help=True,
)


@app.command("show")
@handle_errors
def show(
    ctx: typer.Context,
    run: Annotated[str, typer.Argument(help="Run id, as printed by `thumb generate`.")],
) -> None:
    """Print a run's header and its iterations."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    with open_run_store(settings) as store:
        payload, renderable = run_view(store.runs.get(run), settings.general.data_dir)
    emit(app_ctx, payload, render=lambda: renderable)
