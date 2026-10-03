"""``thumbforge batch`` — one thumbnail per playlist item, from a picked hero (ROADMAP P7.3).

The command wraps `BatchService`: it parses the arguments into a `BatchSpec`, runs the service
once under `asyncio.run`, then prints what the run **stored** and raises the error its outcome
calls for. Two things live here because only the terminal knows about them: the progress display
(stderr, and only on a terminal and without `--json`) and Ctrl-C, which sets the service's cancel
event so the run pauses cleanly and the command exits `130`.
"""

from __future__ import annotations

import asyncio
import logging
import signal
import threading
from collections.abc import Generator
from contextlib import contextmanager
from typing import TYPE_CHECKING, Annotated, Literal, Self

import typer
from rich.console import Console, Group
from rich.markup import escape
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
)

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import emit, get_app_context, kv, table
from thumbforge.cli._runs import (
    EMPTY,
    LogProgress,
    compliance_cell,
    finalizer,
    open_run_store,
    provider_config,
    run_payload,
    size_cell,
    status_cell,
)
from thumbforge.cli._youtube import lookup_key
from thumbforge.core.enums import RunStatus
from thumbforge.core.errors import UsageError
from thumbforge.core.services.batch import BatchPlan, BatchService, BatchSpec, PlanAction
from thumbforge.core.services.hero import NullProgress
from thumbforge.logging import get_logger
from thumbforge.providers import registry
from thumbforge.templates.loader import PromptRenderer

if TYPE_CHECKING:
    from collections.abc import Mapping
    from types import TracebackType

    from rich.console import RenderableType

    from thumbforge.cli._runs import RunStore
    from thumbforge.core.json import JsonPayload
    from thumbforge.core.services.batch import BatchResult
    from thumbforge.settings import Settings

log = get_logger(__name__)

#: The largest part number `--only` accepts, so that `1-999999999` cannot build a huge set.
_MAX_PART = 10_000


def _parse_only(text: str | None) -> frozenset[int] | None:
    """Part numbers from `3,7-9`, or `None` when the option is absent."""
    if text is None:
        return None
    parts: set[int] = set()
    for chunk in text.split(","):
        first_text, dash, last_text = chunk.strip().partition("-")
        try:
            first = int(first_text)
            last = int(last_text) if dash else first
        except ValueError:
            first = last = 0
        if not 1 <= first <= last <= _MAX_PART:
            msg = f"--only expects part numbers like 3,7-9 (1 to {_MAX_PART}), got {text!r}"
            raise UsageError(
                msg, hint="`thumbforge playlist show <playlist> --videos` lists the part numbers"
            )
        parts.update(range(first, last + 1))
    return frozenset(parts)


class BatchProgress(LogProgress):
    """Per-item progress on stderr: a bar, and a `✔ Part 3  Title` line per finished item.

    `labels` maps an iteration's ordinal (its playlist position) to the text shown for it.
    With `enabled` false it draws nothing and logs like any other run; while it draws, the
    per-item log lines drop to DEBUG so they do not tear the bar (the log file keeps them).
    """

    def __init__(self, console: Console, labels: Mapping[int, str], *, enabled: bool) -> None:
        """Draw on `console`; `labels` names the items."""
        super().__init__(logging.DEBUG if enabled else logging.INFO)
        self._labels = labels
        self._enabled = enabled
        self._bar = Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=True,
            disable=not enabled,
        )
        self._task: TaskID | None = None

    def __enter__(self) -> Self:
        self._bar.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._bar.stop()

    def run_started(self, run_id: str, total: int) -> None:
        super().run_started(run_id, total)
        self._task = self._bar.add_task("starting", total=total)

    def iteration_finished(
        self, run_id: str, ordinal: int, status: RunStatus, error: str | None
    ) -> None:
        super().iteration_finished(run_id, ordinal, status, error)
        if not self._enabled or self._task is None:
            return
        label = escape(self._labels.get(ordinal, f"Item {ordinal}"))
        mark = "[green]✔[/]" if status is RunStatus.COMPLETED else "[red]✘[/]"
        detail = "" if error is None else f"  [dim]{escape(error)}[/]"
        self._bar.console.print(f"{mark} {label}{detail}")
        self._bar.update(self._task, advance=1, description=label)


def _labels(plan: BatchPlan) -> dict[int, str]:
    """`Part 3  Title` for each item the batch will run, keyed by its ordinal."""
    return {
        row.item.position: (
            f"Part {row.item.part_number or row.item.position}  {row.item.target.video.title}"
        )
        for row in plan.work
    }


@contextmanager
def _cancel_on_sigint(cancel: asyncio.Event, loop: asyncio.AbstractEventLoop) -> Generator[None]:
    """Set `cancel` on Ctrl-C for the duration of the block, then put the old handler back.

    A plain `signal.signal` handler rather than `loop.add_signal_handler`, which Windows does
    not have. It only runs in the main thread, where Python delivers signals; elsewhere there
    is nothing to hook and the block runs as it is.
    """
    if threading.current_thread() is not threading.main_thread():
        yield
        return
    previous = signal.getsignal(signal.SIGINT)

    def interrupt(_signal: int, _frame: object) -> None:
        loop.call_soon_threadsafe(cancel.set)

    signal.signal(signal.SIGINT, interrupt)
    try:
        yield
    finally:
        signal.signal(signal.SIGINT, signal.SIG_DFL if previous is None else previous)


async def _drive(
    service: BatchService, spec: BatchSpec, console: Console, *, show_progress: bool
) -> BatchResult:
    """Run `spec`, with Ctrl-C wired to the service's cancel event."""
    cancel = asyncio.Event()
    with _cancel_on_sigint(cancel, asyncio.get_running_loop()):
        if spec.dry_run:
            return await service.run(spec, progress=NullProgress(), cancel=cancel)
        labels = _labels(await service.plan(spec)) if show_progress else {}
        with BatchProgress(console, labels, enabled=show_progress) as progress:
            return await service.run(spec, progress=progress, cancel=cancel)


def _plan_view(result: BatchResult) -> tuple[JsonPayload, RenderableType]:
    """The dry run: what each item would do, and nothing stored."""
    rows = result.plan.rows
    counts = {action: sum(1 for row in rows if row.action is action) for action in PlanAction}
    payload: JsonPayload = {
        "dry_run": True,
        "summary": {action.value: count for action, count in counts.items()},
        "plan": [
            {
                "part": row.item.part_number,
                "position": row.item.position,
                "video": row.item.target.video.youtube_id,
                "title": row.item.target.video.title,
                "key": row.key,
                "action": row.action.value,
                "reason": row.reason,
            }
            for row in rows
        ],
    }
    renderable = Group(
        table(
            ["Part", "Title", "Key", "Action", "Reason"],
            [
                [
                    EMPTY if row.item.part_number is None else str(row.item.part_number),
                    escape(row.item.target.video.title),
                    row.key[:8],
                    row.action.value,
                    escape(row.reason),
                ]
                for row in rows
            ],
        ),
        f"{counts[PlanAction.CREATE]} to generate, {counts[PlanAction.RETRY]} to retry, "
        f"{counts[PlanAction.SKIP]} to skip. Nothing was generated (--dry-run).",
    )
    return payload, renderable


def _run_view(
    store: RunStore, settings: Settings, result: BatchResult, reference: str
) -> tuple[JsonPayload, RenderableType]:
    """The run and one row per selected item, read back from what was stored."""
    if result.run_id is None:  # pragma: no cover - only a dry run has no run
        msg = "a batch that ran has a run id"
        raise ValueError(msg)
    data_dir = settings.general.data_dir
    run = store.runs.get(result.run_id)
    stored = store.runs.iterations_by_key([row.key for row in result.plan.rows])
    items: list[JsonPayload] = []
    cells: list[list[str]] = []
    for row in result.plan.rows:
        found = stored.get(row.key)
        final = None if found is None else found.final_asset
        status = RunStatus.PENDING if found is None else found.status
        error = None if found is None else found.error_text
        title = row.item.target.video.title
        part = row.item.part_number
        items.append(
            {
                "part": part,
                "position": row.item.position,
                "video": row.item.target.video.youtube_id,
                "title": title,
                "action": row.action.value,
                "iteration_id": None if found is None else found.id,
                "status": status.value,
                "compliant": None if final is None else final.compliant,
                "final_asset": None if final is None else str(data_dir / final.rel_path),
                "error": error,
            }
        )
        cells.append(
            [
                EMPTY if part is None else str(part),
                escape(title),
                status_cell(status),
                size_cell(final),
                compliance_cell(final),
                EMPTY if final is None else final.sha256[:12],
                EMPTY if not error else escape(error),
            ]
        )
    total = len(result.plan.rows)
    summary: JsonPayload = {
        "total": total,
        "completed": result.completed,
        "failed": result.failed,
        "pending": result.pending,
    }
    header: dict[str, object] = {
        "Playlist": EMPTY if run.playlist is None else escape(run.playlist.title),
        "Template": escape(f"{run.template.name}@{run.template.version}"),
        "Provider": escape(run.provider_profile.name),
        "Reference": (
            EMPTY
            if run.reference_asset is None
            else f"{run.reference_asset.sha256[:12]} ({reference})"
        ),
        "Parent run": run.parent_run_id or EMPTY,
        "Status": run.status.value,
        "Items": (
            f"{result.completed} completed, {result.failed} failed, "
            f"{result.pending} pending of {total}"
        ),
    }
    payload: JsonPayload = {
        "run": run_payload(run, data_dir),
        "summary": summary,
        "items": items,
        "reference_ignored": result.reference_ignored,
    }
    renderable = Group(
        kv(header, title=f"Batch run {run.id}"),
        table(["Part", "Title", "Status", "Size", "Compliant", "Asset", "Error"], cells),
    )
    return payload, renderable


@handle_errors
def batch(
    ctx: typer.Context,
    playlist: Annotated[
        str, typer.Argument(help="Playlist ULID, YouTube id, or URL (fetch it first).")
    ],
    hero: Annotated[
        str,
        typer.Option(
            "--hero",
            help="Hero run (its picked iteration is the reference) or an iteration id.",
        ),
    ],
    template: Annotated[
        str | None,
        typer.Option("--template", help="NAME or NAME@VERSION; default from [general]."),
    ] = None,
    provider: Annotated[
        str | None, typer.Option("--provider", help="Provider key; default from [general].")
    ] = None,
    concurrency: Annotated[
        int | None,
        typer.Option("--concurrency", min=1, help="Parallel provider calls; default from [batch]."),
    ] = None,
    only: Annotated[
        str | None,
        typer.Option("--only", help="Part numbers to generate, e.g. 3,7-9; default all parts."),
    ] = None,
    max_images: Annotated[
        int | None,
        typer.Option(
            "--max-images", min=1, help="Refuse to start if more images than this are needed."
        ),
    ] = None,
    dry_run: Annotated[
        bool, typer.Option("--dry-run", help="Print the plan and generate nothing.")
    ] = False,
    reference: Annotated[
        Literal["final", "raw"],
        typer.Option(
            "--reference",
            help="Which hero image is the style reference: the finished thumbnail "
            "(final) or the art without overlay text (raw).",
        ),
    ] = "final",
) -> None:
    """Generate one thumbnail for every item of a playlist, in the hero's style."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()
    provider_key = provider or settings.general.default_provider
    spec = BatchSpec(
        playlist_id=lookup_key(playlist),
        hero=hero,
        template_ref=template or settings.general.default_template,
        provider_key=provider_key,
        concurrency=concurrency or settings.batch.concurrency,
        only=_parse_only(only),
        dry_run=dry_run,
        reference=reference,
        max_images=max_images,
        max_retries=settings.batch.max_retries,
        provider_params=provider_config(settings, provider_key),
    )
    # Progress goes to stderr and only to a person: not to a pipe, not alongside `--json`.
    console = Console(stderr=True, no_color=app_ctx.console.no_color, highlight=False)
    show_progress = console.is_terminal and not app_ctx.json_mode

    with open_run_store(settings) as store:
        service = BatchService(
            store.runs,
            registry,
            PromptRenderer(store.repos.templates),
            finalizer(settings.output),
            logs_dir=settings.state_dir / "logs" / "runs",
            stale_after_s=settings.batch.stale_after_s,
        )
        # One `asyncio.run` per invocation: the CLI is the only sync/async boundary.
        result = asyncio.run(_drive(service, spec, console, show_progress=show_progress))
        payload, renderable = (
            _plan_view(result) if dry_run else _run_view(store, settings, result, reference)
        )

    if result.reference_ignored:
        log.warning("provider takes no reference image; generating from the prompt alone")
    emit(
        app_ctx,
        {**payload, "exit_code": int(result.exit_code)},
        render=lambda: renderable,
    )
    # After the output, so the table is on screen when the diagnostic and exit code arrive.
    if (error := result.error()) is not None:
        raise error
