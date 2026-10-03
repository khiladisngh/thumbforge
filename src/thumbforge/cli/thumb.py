"""``thumbforge thumb`` — generate hero thumbnails for one video, then pick and export one.

`generate` is ROADMAP P6.1, `pick`, `show` and `export` are P6.2, `iterate` is P6.3.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING, Annotated

import structlog
import typer
from rich.markup import escape

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import emit, get_app_context, preview
from thumbforge.cli._runs import (
    final_paths,
    final_tiles,
    open_run_store,
    parse_vars,
    provider_config,
    run_view,
)
from thumbforge.cli._youtube import lookup_key
from thumbforge.core.services.hero import HeroService, RunSpec
from thumbforge.core.services.iterate import IterateService
from thumbforge.imaging.finalize import render_final
from thumbforge.logging import get_logger
from thumbforge.providers import registry
from thumbforge.storage.models import Iteration
from thumbforge.templates.loader import PromptRenderer

if TYPE_CHECKING:
    from rich.console import RenderableType

    from thumbforge.cli._render import AppContext
    from thumbforge.cli._runs import RunStore
    from thumbforge.core.enums import RunStatus
    from thumbforge.core.json import JsonPayload
    from thumbforge.core.layout import LayoutSpec
    from thumbforge.core.models import ComplianceReport
    from thumbforge.core.services.hero import Finalize, RunResult
    from thumbforge.settings import OutputSettings, Settings

log = get_logger(__name__)

app = typer.Typer(
    name="thumb",
    help="Generate and manage thumbnails for one video.",
    no_args_is_help=True,
)


class _LogProgress:
    """Binds `run_id` for the run's log lines and reports each finished iteration."""

    def run_started(self, run_id: str, total: int) -> None:
        # Bound inside the service's task, so it reaches every iteration task it spawns.
        structlog.contextvars.bind_contextvars(run_id=run_id)
        log.info("run started", iterations=total)

    def iteration_finished(
        self, run_id: str, ordinal: int, status: RunStatus, error: str | None
    ) -> None:
        log.info("iteration finished", ordinal=ordinal, status=status.value, error=error)


def _finalizer(output: OutputSettings) -> Finalize:
    """`render_final` with the `[output]` settings bound, as the service expects it."""

    def finalize(
        raw: Path,
        layout: LayoutSpec,
        *,
        title: str,
        part_number: int | None,
        part_label: str | None,
    ) -> tuple[bytes, ComplianceReport]:
        return render_final(
            raw, layout, output, title=title, part_number=part_number, part_label=part_label
        )

    return finalize


def _hero_service(store: RunStore, settings: Settings) -> HeroService:
    """The hero machinery, wired to this command's store, as `generate` and `iterate` share it."""
    return HeroService(
        store.runs,
        registry,
        PromptRenderer(store.repos.templates),
        _finalizer(settings.output),
        logs_dir=settings.state_dir / "logs" / "runs",
    )


def _run_report(
    store: RunStore, settings: Settings, result: RunResult
) -> tuple[JsonPayload, RenderableType, list[Path]]:
    """The stored view of the run just finished: payload, table and the finals to preview."""
    run = store.runs.get(result.run_id)
    payload, renderable = run_view(run, settings.general.data_dir)
    return payload, renderable, final_paths(run, settings.general.data_dir)


def _print_run(
    app_ctx: AppContext,
    result: RunResult,
    view: tuple[JsonPayload, RenderableType, list[Path]],
) -> None:
    """Print a finished run, then raise the error its outcome calls for."""
    payload, renderable, images = view
    if result.reference_ignored:
        log.warning("provider takes no reference image; refining from the prompt alone")
    emit(
        app_ctx,
        {**payload, "exit_code": int(result.exit_code)},
        render=lambda: renderable,
    )
    if not app_ctx.json_mode:
        preview(app_ctx, images, columns=2)
        if result.completed:
            app_ctx.console.print(
                f"Pick one with: thumbforge thumb pick {result.run_id} <ordinal>",
                soft_wrap=True,
            )
    # After the output, so the table is on screen when the diagnostic and exit code arrive.
    if (error := result.error()) is not None:
        raise error


@app.command("generate")
@handle_errors
def generate(
    ctx: typer.Context,
    video: Annotated[str, typer.Argument(help="Video ULID, YouTube id, or URL (fetch it first).")],
    template: Annotated[
        str | None,
        typer.Option("--template", help="NAME or NAME@VERSION; default from [general]."),
    ] = None,
    provider: Annotated[
        str | None, typer.Option("--provider", help="Provider key; default from [general].")
    ] = None,
    n: Annotated[int, typer.Option("--n", min=1, help="Iterations to generate.")] = 4,
    concurrency: Annotated[
        int | None,
        typer.Option("--concurrency", min=1, help="Parallel provider calls; default from [batch]."),
    ] = None,
    seed: Annotated[
        int | None, typer.Option("--seed", help="First seed; iteration k uses seed + k - 1.")
    ] = None,
    var: Annotated[
        list[str] | None,
        typer.Option("--var", help="key=value for {{ vars.key }}; repeatable."),
    ] = None,
    out: Annotated[
        Path | None,
        typer.Option("--out", help="Also copy every completed final to DIR/<video>-<n>.<ext>."),
    ] = None,
) -> None:
    """Generate N hero thumbnails for a stored video and print the iterations."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    provider_key = provider or settings.general.default_provider
    spec = RunSpec(
        video_id=lookup_key(video),
        template_ref=template or settings.general.default_template,
        provider_key=provider_key,
        n=n,
        concurrency=concurrency or settings.batch.concurrency,
        seed=seed,
        vars=parse_vars(var or []),
        out_dir=out,
        provider_params=provider_config(settings, provider_key),
    )

    with open_run_store(settings) as store:
        service = _hero_service(store, settings)
        # One `asyncio.run` per invocation: the CLI is the only sync/async boundary.
        result = asyncio.run(service.generate(spec, progress=_LogProgress()))
        view = _run_report(store, settings, result)

    _print_run(app_ctx, result, view)


@app.command("iterate")
@handle_errors
def iterate(
    ctx: typer.Context,
    target: Annotated[
        str,
        typer.Argument(
            help="Run id (refines its picked iteration) or iteration id (refines that one)."
        ),
    ],
    n: Annotated[int, typer.Option("--n", min=1, help="Iterations to generate.")] = 4,
    prompt_append: Annotated[
        str | None,
        typer.Option("--prompt-append", help="Text added after the rendered prompt."),
    ] = None,
    var: Annotated[
        list[str] | None,
        typer.Option("--var", help="key=value for {{ vars.key }}; repeatable, not inherited."),
    ] = None,
    from_picked: Annotated[
        bool,
        typer.Option(
            "--from-picked", help="With a run id and no pick of its own, use its ancestors' pick."
        ),
    ] = False,
) -> None:
    """Refine a picked (or given) iteration: a child run with it as the reference image."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    with open_run_store(settings) as store:
        service = IterateService(store.runs, _hero_service(store, settings))
        result = asyncio.run(
            service.iterate(
                target,
                n=n,
                concurrency=settings.batch.concurrency,
                prompt_append=prompt_append,
                vars=parse_vars(var or []),
                from_picked=from_picked,
                progress=_LogProgress(),
            )
        )
        view = _run_report(store, settings, result)

    _print_run(app_ctx, result, view)


@app.command("pick")
@handle_errors
def pick(
    ctx: typer.Context,
    run: Annotated[str, typer.Argument(help="Run id, as printed by `thumb generate`.")],
    target: Annotated[str, typer.Argument(help="Iteration ordinal, or iteration id.")],
) -> None:
    """Pick the iteration to keep; an earlier pick in the run moves to it."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    with open_run_store(settings) as store:
        chosen = store.runs.pick(run, int(target) if target.isdecimal() else target)
        payload: JsonPayload = {
            "run_id": chosen.run_id,
            "picked": {"id": chosen.id, "ordinal": chosen.ordinal},
        }
        summary = f"Picked #{chosen.ordinal} of run {chosen.run_id} (iteration {chosen.id})"
    emit(app_ctx, payload, render=lambda: summary)
    if not app_ctx.json_mode:
        app_ctx.console.print(
            f"Export it with: thumbforge thumb export {run} --to PATH", soft_wrap=True
        )


@app.command("show")
@handle_errors
def show(
    ctx: typer.Context,
    run: Annotated[str, typer.Argument(help="Run id, as printed by `thumb generate`.")],
    columns: Annotated[int, typer.Option("--columns", min=1, help="Tiles per grid row.")] = 2,
) -> None:
    """Show a run's iterations and a grid of their finals; the picked one is starred."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    with open_run_store(settings) as store:
        stored = store.runs.get(run)
        payload, renderable = run_view(stored, settings.general.data_dir)
        tiles = final_tiles(stored, settings.general.data_dir)
    emit(app_ctx, payload, render=lambda: renderable)
    preview(
        app_ctx,
        [path for path, _ in tiles],
        columns=columns,
        captions=[caption for _, caption in tiles],
    )


@app.command("export")
@handle_errors
def export(
    ctx: typer.Context,
    target: Annotated[
        str, typer.Argument(help="Run id (every completed iteration) or iteration id.")
    ],
    to: Annotated[
        Path, typer.Option("--to", help="Directory to copy into; created if it is missing.")
    ],
    raw: Annotated[
        bool, typer.Option("--raw", help="Copy the provider's raw images instead of the finals.")
    ] = False,
) -> None:
    """Copy the final (or raw) images of a run or one iteration into a directory."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    with open_run_store(settings) as store:
        found = store.runs.resolve_target(target)
        files = store.runs.export(found, to, raw=raw)
        iteration_id = found.id if isinstance(found, Iteration) else None
        run_id = found.run_id if isinstance(found, Iteration) else found.id
    emit(
        app_ctx,
        {
            "run_id": run_id,
            "iteration_id": iteration_id,
            "raw": raw,
            "files": [str(path) for path in files],
        },
        render=lambda: "\n".join(f"Wrote {escape(str(path))}" for path in files),
    )
