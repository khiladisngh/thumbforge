"""``thumbforge thumb`` — generate hero thumbnails for one video (ROADMAP P6.1).

`pick`, `show`, `export` (P6.2) and `iterate` (P6.3) join this app in their own tasks.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING, Annotated

import structlog
import typer

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import emit, get_app_context, preview
from thumbforge.cli._runs import (
    final_paths,
    open_run_store,
    parse_vars,
    provider_config,
    run_view,
)
from thumbforge.cli._youtube import lookup_key
from thumbforge.core.services.hero import HeroService, RunSpec
from thumbforge.imaging.finalize import render_final
from thumbforge.logging import get_logger
from thumbforge.providers import registry
from thumbforge.templates.loader import PromptRenderer

if TYPE_CHECKING:
    from thumbforge.core.enums import RunStatus
    from thumbforge.core.layout import LayoutSpec
    from thumbforge.core.models import ComplianceReport
    from thumbforge.core.services.hero import Finalize
    from thumbforge.settings import OutputSettings

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
        service = HeroService(
            store.runs,
            registry,
            PromptRenderer(store.repos.templates),
            _finalizer(settings.output),
            logs_dir=settings.state_dir / "logs" / "runs",
        )
        # One `asyncio.run` per invocation: the CLI is the only sync/async boundary.
        result = asyncio.run(service.generate(spec, progress=_LogProgress()))
        run = store.runs.get(result.run_id)
        payload, renderable = run_view(run, settings.general.data_dir)
        images = final_paths(run, settings.general.data_dir)

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
