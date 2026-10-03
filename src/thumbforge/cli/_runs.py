"""Wiring and the shared run view for `thumb generate` and `runs show` (ROADMAP P6.1).

`batch` (P7.3) shares the progress sink, the final-render binding and the run object; the
`runs` commands (P7.4) share the batch service wiring and the list view.

`core.services.hero` declares Protocols; the concrete store is chosen here, which is the
injection point `PLAN.md` §2.2 describes. The view reads the **stored** rows, never what the
service returned: `generate` and `runs show` then print the same thing, and a run looks the
same a minute or a month after it finished.
"""

from __future__ import annotations

import json
import logging
from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

import structlog
from rich.console import Group
from rich.markup import escape

from thumbforge.cli._render import kv, table
from thumbforge.core.enums import RunKind, RunStatus
from thumbforge.core.errors import TemplateError
from thumbforge.core.json import JsonPayload, JsonValue
from thumbforge.core.services.batch import BatchService
from thumbforge.imaging.finalize import render_final
from thumbforge.logging import get_logger
from thumbforge.providers import registry
from thumbforge.storage.assets import AssetStore
from thumbforge.storage.db import get_engine, session_factory, session_scope
from thumbforge.storage.repositories import Repositories
from thumbforge.storage.runs import RunRepository
from thumbforge.templates.loader import PromptRenderer

if TYPE_CHECKING:
    from collections.abc import Generator, Mapping, Sequence
    from pathlib import Path

    from rich.console import RenderableType

    from thumbforge.core.layout import LayoutSpec
    from thumbforge.core.models import ComplianceReport
    from thumbforge.core.services.hero import Finalize
    from thumbforge.settings import OutputSettings, Settings
    from thumbforge.storage.models import Asset, Iteration, Run

log = get_logger(__name__)

#: Shown where an iteration has nothing to report, matching the other tables.
EMPTY = "—"


@dataclass(frozen=True, slots=True)
class RunStore:
    """The two repositories a run command needs, over one session."""

    repos: Repositories
    runs: RunRepository


@contextmanager
def open_run_store(settings: Settings) -> Generator[RunStore]:
    """Open a session and an asset store for one command, committing on success.

    The engine is disposed afterwards: an open SQLite handle keeps a file lock on Windows,
    which breaks `tmp_path` cleanup. The asset store takes its own sessions from the same
    engine, so it must never be called with writes pending here (see `storage.runs`).
    """
    engine = get_engine(settings.db_path)
    try:
        assets = AssetStore(settings.general.data_dir, session_factory(engine))
        with session_scope(engine) as session:
            yield RunStore(Repositories(session), RunRepository(session, assets))
    finally:
        engine.dispose()


def batch_service(store: RunStore, settings: Settings) -> BatchService:
    """The batch service over `store`, as `batch` and `runs resume|cancel` use it."""
    return BatchService(
        store.runs,
        registry,
        PromptRenderer(store.repos.templates),
        finalizer(settings.output),
        logs_dir=settings.state_dir / "logs" / "runs",
        stale_after_s=settings.batch.stale_after_s,
    )


def parse_vars(pairs: list[str]) -> dict[str, str]:
    """Parse repeated `--var key=value` options."""
    variables: dict[str, str] = {}
    for pair in pairs:
        key, separator, value = pair.partition("=")
        if not separator or not key:
            msg = f"--var expects key=value, got {pair!r}"
            raise TemplateError(msg)
        variables[key] = value
    return variables


def provider_config(settings: Settings, key: str) -> Mapping[str, JsonValue]:
    """The provider's own settings section, or an empty mapping when it has none.

    Providers take a plain mapping rather than `Settings` so nothing in `providers/` depends
    on the settings model. `fake` has no section at all, which is not an error.
    """
    section = getattr(settings.providers, key, None)
    if section is None:
        return {}
    dumped: JsonPayload = section.model_dump(mode="json")
    return dumped


def finalizer(output: OutputSettings) -> Finalize:
    """`render_final` with the `[output]` settings bound, as the services expect it."""

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


class LogProgress:
    """Binds `run_id` for the run's log lines and reports each finished iteration."""

    def __init__(self, level: int = logging.INFO) -> None:
        """Log at `level`; a display that owns the terminal asks for `DEBUG`."""
        self._level = level

    def run_started(self, run_id: str, total: int) -> None:
        # Bound inside the service's task, so it reaches every iteration task it spawns.
        structlog.contextvars.bind_contextvars(run_id=run_id)
        log.log(self._level, "run started", iterations=total)

    def iteration_finished(
        self, run_id: str, ordinal: int, status: RunStatus, error: str | None
    ) -> None:
        log.log(
            self._level, "iteration finished", ordinal=ordinal, status=status.value, error=error
        )


def final_paths(run: Run, data_dir: Path) -> list[Path]:
    """The stored final image of every completed iteration, in ordinal order."""
    return [
        data_dir / iteration.final_asset.rel_path
        for iteration in _ordered(run)
        if iteration.status is RunStatus.COMPLETED and iteration.final_asset is not None
    ]


def final_tiles(run: Run, data_dir: Path) -> list[tuple[Path, str]]:
    """The stored final of every iteration that has one, with its grid caption, by ordinal.

    A non-compliant final is included: it is stored so it can be inspected, and its `✘` says
    why it cannot be picked. Captions read `#2 ★ ✔`: ordinal, picked marker, compliance.
    """
    tiles: list[tuple[Path, str]] = []
    for item in _ordered(run):
        final = item.final_asset
        if final is None:
            continue
        picked = " ★" if item.picked else ""
        verdict = "✔" if final.compliant else "✘"
        tiles.append((data_dir / final.rel_path, f"#{item.ordinal}{picked} {verdict}"))
    return tiles


def run_view(run: Run, data_dir: Path) -> tuple[JsonPayload, RenderableType]:
    """The JSON payload and the Rich renderable for one stored run."""
    iterations = _ordered(run)
    header: dict[str, object] = {
        "Kind": run.kind.value,
        "Status": run.status.value,
        "Template": escape(f"{run.template.name}@{run.template.version}"),
        "Provider": escape(run.provider_profile.name),
        "Video": EMPTY if run.video is None else escape(run.video.youtube_id),
    }
    counts = iteration_counts(run)
    if run.kind is RunKind.BATCH:
        header["Playlist"] = EMPTY if run.playlist is None else escape(run.playlist.title)
        header["Items"] = (
            f"{counts['completed']} completed, {counts['failed']} failed, "
            f"{counts['pending']} pending of {counts['total']}"
        )
    children = sorted(child.id for child in run.child_runs)
    if run.parent_run_id is not None:
        header["Parent run"] = run.parent_run_id
    if run.reference_asset is not None:
        header["Reference"] = run.reference_asset.sha256[:12]
    if children:
        header["Child runs"] = ", ".join(children)
    header["Started"] = run.started_at or EMPTY
    header["Finished"] = run.finished_at or EMPTY
    if run.error_text:
        header["Error"] = escape(run.error_text)

    payload: JsonPayload = {
        "run": run_payload(run, data_dir),
        "summary": counts,
        "iterations": [_iteration_payload(item, data_dir) for item in iterations],
    }
    renderable = Group(
        kv(header, title=f"Run {run.id}"),
        table(
            ["#", "Status", "Size", "Compliant", "Key", "Asset / Error"],
            [_iteration_row(item) for item in iterations],
        ),
    )
    return payload, renderable


def runs_view(runs: Sequence[Run]) -> tuple[JsonPayload, RenderableType]:
    """The JSON payload and the Rich table for `runs list`, one row per run in the order given."""
    entries: list[JsonValue] = []
    rows: list[list[str]] = []
    for run in runs:
        counts = iteration_counts(run)
        entries.append(
            {
                "id": run.id,
                "kind": run.kind.value,
                "status": run.status.value,
                "template": f"{run.template.name}@{run.template.version}",
                "provider": run.provider_profile.name,
                "video": None if run.video is None else run.video.youtube_id,
                "parent_run_id": run.parent_run_id,
                "started_at": run.started_at,
                "finished_at": run.finished_at,
                "counts": counts,
            }
        )
        rows.append(
            [
                run.id,
                run.kind.value,
                status_cell(run.status),
                escape(f"{run.template.name}@{run.template.version}"),
                escape(run.provider_profile.name),
                f"{counts['completed']}/{counts['total']}",
                str(counts["failed"]),
            ]
        )
    payload: JsonPayload = {"runs": entries}
    return payload, table(["Run", "Kind", "Status", "Template", "Provider", "Done", "Failed"], rows)


def iteration_counts(run: Run) -> JsonPayload:
    """How many iterations a run has, and how many are completed, failed and still pending.

    The same shape `batch` prints as its `summary`; a `cancelled` or `running` iteration counts
    only toward the total.
    """
    states = [item.status for item in run.iterations]
    return {
        "total": len(states),
        "completed": states.count(RunStatus.COMPLETED),
        "failed": states.count(RunStatus.FAILED),
        "pending": states.count(RunStatus.PENDING),
    }


def run_payload(run: Run, data_dir: Path) -> JsonPayload:
    """The JSON object for a run's own fields, shared by `runs show` and `batch`."""
    return {
        "id": run.id,
        "kind": run.kind.value,
        "status": run.status.value,
        "template": f"{run.template.name}@{run.template.version}",
        "provider": run.provider_profile.name,
        "video": None if run.video is None else run.video.youtube_id,
        "playlist": None if run.playlist is None else run.playlist.youtube_id,
        "parent_run_id": run.parent_run_id,
        "child_run_ids": sorted(child.id for child in run.child_runs),
        "reference_asset": _asset_payload(run.reference_asset, data_dir),
        "started_at": run.started_at,
        "finished_at": run.finished_at,
        "error": run.error_text,
    }


def _ordered(run: Run) -> list[Iteration]:
    return sorted(run.iterations, key=lambda item: item.ordinal)


_STATUS_STYLE = {RunStatus.COMPLETED: "green", RunStatus.FAILED: "red"}


def status_cell(status: RunStatus) -> str:
    """A status for a table cell: green when completed, red when failed."""
    style = _STATUS_STYLE.get(status)
    return status.value if style is None else f"[{style}]{status.value}[/]"


def size_cell(final: Asset | None) -> str:
    """`WxH` of a stored final, or the placeholder when there is none."""
    return EMPTY if final is None else f"{final.width}x{final.height}"


def compliance_cell(final: Asset | None) -> str:
    """`✔` or `✘` for a stored final's verdict, or the placeholder when it has none."""
    if final is None or final.compliant is None:
        return EMPTY
    return "✔" if final.compliant else "✘"


def _iteration_row(item: Iteration) -> list[str]:
    final = item.final_asset
    if item.error_text:
        detail = escape(item.error_text)
    else:
        detail = EMPTY if final is None else final.sha256[:12]
    ordinal = f"{item.ordinal} ★" if item.picked else str(item.ordinal)
    return [
        ordinal,
        status_cell(item.status),
        size_cell(final),
        compliance_cell(final),
        item.idempotency_key[:12],
        detail,
    ]


def _iteration_payload(item: Iteration, data_dir: Path) -> JsonPayload:
    final = item.final_asset
    report: JsonValue = None
    if final is not None and final.compliance_report_json:
        report = cast("JsonValue", json.loads(final.compliance_report_json))
    return {
        "id": item.id,
        "ordinal": item.ordinal,
        "status": item.status.value,
        "idempotency_key": item.idempotency_key,
        "seed": item.seed,
        "picked": item.picked,
        "raw_asset": _asset_payload(item.raw_asset, data_dir),
        "final_asset": _asset_payload(final, data_dir),
        "compliant": None if final is None else final.compliant,
        "compliance_report": report,
        "error": item.error_text,
    }


def _asset_payload(asset: Asset | None, data_dir: Path) -> JsonPayload | None:
    if asset is None:
        return None
    return {
        "id": asset.id,
        "sha256": asset.sha256,
        "path": str(data_dir / asset.rel_path),
        "mime": asset.mime,
        "width": asset.width,
        "height": asset.height,
        "bytes": asset.bytes,
    }
