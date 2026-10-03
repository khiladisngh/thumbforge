"""Wiring and the shared run view for `thumb generate` and `runs show` (ROADMAP P6.1).

`core.services.hero` declares Protocols; the concrete store is chosen here, which is the
injection point `PLAN.md` §2.2 describes. The view reads the **stored** rows, never what the
service returned: `generate` and `runs show` then print the same thing, and a run looks the
same a minute or a month after it finished.
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from rich.console import Group
from rich.markup import escape

from thumbforge.cli._render import kv, table
from thumbforge.core.enums import RunStatus
from thumbforge.core.errors import TemplateError
from thumbforge.core.json import JsonPayload, JsonValue
from thumbforge.storage.assets import AssetStore
from thumbforge.storage.db import get_engine, session_factory, session_scope
from thumbforge.storage.repositories import Repositories
from thumbforge.storage.runs import RunRepository

if TYPE_CHECKING:
    from collections.abc import Generator, Mapping
    from pathlib import Path

    from rich.console import RenderableType

    from thumbforge.settings import Settings
    from thumbforge.storage.models import Asset, Iteration, Run

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


def final_paths(run: Run, data_dir: Path) -> list[Path]:
    """The stored final image of every completed iteration, in ordinal order."""
    return [
        data_dir / iteration.final_asset.rel_path
        for iteration in _ordered(run)
        if iteration.status is RunStatus.COMPLETED and iteration.final_asset is not None
    ]


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
    if run.parent_run_id is not None:
        header["Parent run"] = run.parent_run_id
    header["Started"] = run.started_at or EMPTY
    header["Finished"] = run.finished_at or EMPTY
    if run.error_text:
        header["Error"] = escape(run.error_text)

    payload: JsonPayload = {
        "run": {
            "id": run.id,
            "kind": run.kind.value,
            "status": run.status.value,
            "template": f"{run.template.name}@{run.template.version}",
            "provider": run.provider_profile.name,
            "video": None if run.video is None else run.video.youtube_id,
            "parent_run_id": run.parent_run_id,
            "started_at": run.started_at,
            "finished_at": run.finished_at,
            "error": run.error_text,
        },
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


def _ordered(run: Run) -> list[Iteration]:
    return sorted(run.iterations, key=lambda item: item.ordinal)


_STATUS_STYLE = {RunStatus.COMPLETED: "green", RunStatus.FAILED: "red"}


def _iteration_row(item: Iteration) -> list[str]:
    final = item.final_asset
    style = _STATUS_STYLE.get(item.status)
    status = item.status.value if style is None else f"[{style}]{item.status.value}[/]"
    size = EMPTY if final is None else f"{final.width}x{final.height}"
    if final is None or final.compliant is None:
        compliant = EMPTY
    else:
        compliant = "✔" if final.compliant else "✘"
    if item.error_text:
        detail = escape(item.error_text)
    else:
        detail = EMPTY if final is None else final.sha256[:12]
    return [str(item.ordinal), status, size, compliant, item.idempotency_key[:12], detail]


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
