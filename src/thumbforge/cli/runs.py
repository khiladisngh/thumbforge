"""``thumbforge runs`` — list, inspect, cost, continue, cancel and delete runs (P7.4, P8.4).

`show` (P6.1), `list` and `cost` (P8.4) read stored rows; `resume` and `cancel` wrap
`BatchService`, with the same progress display and Ctrl-C handling as `batch`; `delete` is the
repository's, which also decides what a delete may not touch.
"""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Annotated

import typer
from rich.console import Console

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import emit, get_app_context
from thumbforge.cli._runs import (
    batch_service,
    cost_view,
    open_run_store,
    run_payload,
    run_view,
    runs_view,
)
from thumbforge.cli.batch import BatchProgress, batch_view, cancel_on_sigint
from thumbforge.core.enums import RunKind, RunStatus

if TYPE_CHECKING:
    from collections.abc import Mapping

    from thumbforge.core.json import JsonPayload
    from thumbforge.core.services.batch import BatchResult, BatchService

app = typer.Typer(
    name="runs",
    help="List, inspect, cost, continue, cancel and delete generation runs.",
    no_args_is_help=True,
)

_RUN_ARGUMENT = typer.Argument(help="Run id, as printed by `thumb generate` and `batch`.")


@app.command("list")
@handle_errors
def list_runs(
    ctx: typer.Context,
    kind: Annotated[RunKind | None, typer.Option("--kind", help="Only runs of this kind.")] = None,
    status: Annotated[
        RunStatus | None, typer.Option("--status", help="Only runs in this status.")
    ] = None,
    limit: Annotated[int, typer.Option("--limit", min=1, help="Show at most this many.")] = 50,
) -> None:
    """List runs, newest first."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    with open_run_store(settings) as store:
        payload, renderable = runs_view(store.runs.list_runs(kind=kind, status=status, limit=limit))
    emit(app_ctx, payload, render=lambda: renderable)


@app.command("show")
@handle_errors
def show(
    ctx: typer.Context,
    run: Annotated[str, _RUN_ARGUMENT],
) -> None:
    """Print a run's header and its iterations."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    with open_run_store(settings) as store:
        payload, renderable = run_view(store.runs.get(run), settings.general.data_dir)
    emit(app_ctx, payload, render=lambda: renderable)


@app.command("cost")
@handle_errors
def cost(
    ctx: typer.Context,
    run: Annotated[str, _RUN_ARGUMENT],
) -> None:
    """Total the tokens and credits a run's iterations used, as its provider reported them."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    with open_run_store(settings) as store:
        payload, renderable = cost_view(store.runs.cost_report(run))
    emit(app_ctx, payload, render=lambda: renderable)


async def _resume(
    service: BatchService,
    run_id: str,
    concurrency: int | None,
    console: Console,
    labels: Mapping[int, str],
    *,
    show_progress: bool,
) -> BatchResult:
    """Resume `run_id`, with Ctrl-C wired to the service's cancel event."""
    cancel = asyncio.Event()
    with (
        cancel_on_sigint(cancel, asyncio.get_running_loop()),
        BatchProgress(console, labels, enabled=show_progress) as progress,
    ):
        return await service.resume(
            run_id, progress=progress, cancel=cancel, concurrency=concurrency
        )


@app.command("resume")
@handle_errors
def resume(
    ctx: typer.Context,
    run: Annotated[str, _RUN_ARGUMENT],
    concurrency: Annotated[
        int | None,
        typer.Option("--concurrency", min=1, help="Parallel provider calls; default as stored."),
    ] = None,
) -> None:
    """Continue a paused or failed batch run: retry what it left unfinished, nothing else."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    # Progress goes to stderr and only to a person: not to a pipe, not alongside `--json`.
    console = Console(stderr=True, no_color=app_ctx.console.no_color, highlight=False)
    show_progress = console.is_terminal and not app_ctx.json_mode

    with open_run_store(settings) as store:
        stored = store.runs.get(run)
        reference = str(json.loads(stored.params_json).get("reference", "final"))
        labels = (
            {}
            if stored.playlist is None
            else {
                item.position: f"Part {item.part_number or item.position}  {item.video.title}"
                for item in stored.playlist.items
            }
        )
        # One `asyncio.run` per invocation: the CLI is the only sync/async boundary.
        result = asyncio.run(
            _resume(
                batch_service(store, settings),
                run,
                concurrency,
                console,
                labels,
                show_progress=show_progress,
            )
        )
        payload, renderable = batch_view(store, settings, result, reference)

    emit(app_ctx, {**payload, "exit_code": int(result.exit_code)}, render=lambda: renderable)
    # After the output, so the table is on screen when the diagnostic and exit code arrive.
    if (error := result.error()) is not None:
        raise error


@app.command("cancel")
@handle_errors
def cancel(
    ctx: typer.Context,
    run: Annotated[str, _RUN_ARGUMENT],
) -> None:
    """Abandon a run: it and the iterations it has not finished become cancelled."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    with open_run_store(settings) as store:
        batch_service(store, settings).cancel(run)
        payload: JsonPayload = {"run": run_payload(store.runs.get(run), settings.general.data_dir)}
    emit(app_ctx, payload, render=lambda: f"Run {run} cancelled.")


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    run: Annotated[str, _RUN_ARGUMENT],
    assets: Annotated[
        bool,
        typer.Option(
            "--assets",
            help="Also delete the image files that no other run, iteration or reference uses.",
        ),
    ] = False,
) -> None:
    """Delete a run and its iterations; refused while another run builds on it."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    with open_run_store(settings) as store:
        deleted = store.runs.delete_run(run, assets=assets)
    files = [str(path) for path in deleted.assets]
    payload: JsonPayload = {
        "deleted": {"run": run, "iterations": deleted.iterations, "assets": list(files)}
    }
    noun = "iteration" if deleted.iterations == 1 else "iterations"
    line = f"Deleted run {run} and its {deleted.iterations} {noun}."
    if assets:
        line += f" Removed {len(files)} image file{'' if len(files) == 1 else 's'}."
    emit(app_ctx, payload, render=lambda: line)
