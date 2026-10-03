"""Runs, iterations and provider profiles, as `HeroService` reads and writes them (ROADMAP P6.1).

`RunRepository` satisfies the `HeroStore` Protocol declared beside the service. It exchanges
the core value types (`HeroTarget`, `AssetInfo`, ...) rather than ORM rows, which `core` may
not name; `get` returns the row because the CLI renders from it, as `fetch` does.

The repository owns no transaction: it flushes, and the service calls `commit`. One rule
matters more than the rest: the `AssetStore` writes through its **own** connection, and
SQLite allows one writer, so the session must hold nothing uncommitted when `put_raw` or
`put_final` run. The service commits before every `await` and every asset write for that
reason; waiting out `busy_timeout` would only end in "database is locked".
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

from thumbforge.core.enums import AssetKind, RunKind, RunStatus
from thumbforge.core.errors import NotFoundError
from thumbforge.core.services.hero import AssetInfo, HeroTarget
from thumbforge.storage.models import Asset, Iteration, ProviderProfile, Run, utcnow_iso
from thumbforge.storage.models import Template as TemplateRow
from thumbforge.storage.repositories import VideoRepository, channel_meta, video_meta

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

    from sqlalchemy.orm import Session

    from thumbforge.core.layout import Template
    from thumbforge.core.models import ComplianceReport
    from thumbforge.core.services.hero import IterationDraft, IterationOutcome
    from thumbforge.storage.assets import AssetStore


class RunRepository:
    """Hero runs over one session and one asset store."""

    def __init__(self, session: Session, assets: AssetStore) -> None:
        """Bind to the caller's session; the service owns the transaction."""
        self._session = session
        self._assets = assets

    def resolve_video(self, reference: str) -> HeroTarget:
        """The stored video named by a ULID or YouTube id, with its channel when known."""
        row = VideoRepository(self._session).resolve(reference)
        channel = None if row.channel is None else channel_meta(row.channel)
        return HeroTarget(row_id=row.id, video=video_meta(row), channel=channel)

    def ensure_profile(
        self, name: str, provider_key: str, provider_version: str, params_json: str
    ) -> str:
        """The id of the profile called `name`; created on first use, never changed after."""
        row = self._session.scalars(
            select(ProviderProfile).where(ProviderProfile.name == name)
        ).one_or_none()
        if row is None:
            row = ProviderProfile(
                name=name,
                provider_key=provider_key,
                provider_version=provider_version,
                params_json=params_json,
            )
            self._session.add(row)
            self._session.flush()
        return row.id

    def create_run(
        self,
        run_id: str,
        *,
        kind: RunKind,
        template: Template,
        profile_id: str,
        video_id: str,
        params_json: str,
        iterations: Sequence[IterationDraft],
    ) -> list[str]:
        """Insert a `running` run and its `pending` iterations; return the iteration ids."""
        template_id = self._session.scalars(
            select(TemplateRow.id).where(
                TemplateRow.name == template.name, TemplateRow.version == template.version
            )
        ).one_or_none()
        if template_id is None:
            msg = f"template {template.ref!r}"
            raise NotFoundError(msg, hint="`thumbforge template list` shows the stored templates")

        self._session.add(
            Run(
                id=run_id,
                kind=kind,
                status=RunStatus.RUNNING,
                template_id=template_id,
                provider_profile_id=profile_id,
                video_id=video_id,
                params_json=params_json,
                started_at=utcnow_iso(),
            )
        )
        rows = [
            Iteration(
                run_id=run_id,
                video_id=video_id,
                ordinal=draft.ordinal,
                idempotency_key=draft.idempotency_key,
                status=RunStatus.PENDING,
                prompt_text=draft.prompt_text,
                seed=draft.seed,
            )
            for draft in iterations
        ]
        self._session.add_all(rows)
        self._session.flush()
        return [row.id for row in rows]

    def mark_iteration_running(self, iteration_id: str) -> None:
        """Move an iteration to `running` and stamp its start."""
        row = self._iteration(iteration_id)
        row.status = RunStatus.RUNNING
        row.started_at = utcnow_iso()
        self._session.flush()

    def finish_iteration(self, iteration_id: str, outcome: IterationOutcome) -> None:
        """Record how an iteration ended."""
        row = self._iteration(iteration_id)
        row.status = outcome.status
        row.raw_asset_id = outcome.raw_asset_id
        row.final_asset_id = outcome.final_asset_id
        row.error_text = outcome.error_text
        row.provider_request_json = outcome.provider_request_json
        row.provider_response_json = outcome.provider_response_json
        row.duration_ms = outcome.duration_ms
        row.cost_json = outcome.cost_json
        row.finished_at = utcnow_iso()
        self._session.flush()

    def finish_run(self, run_id: str, status: RunStatus, error_text: str | None) -> None:
        """Record how a run ended."""
        row = self.get(run_id)
        row.status = status
        row.error_text = error_text
        row.finished_at = utcnow_iso()
        self._session.flush()

    def put_raw(self, path: Path) -> AssetInfo:
        """Store a provider's output as a `raw` asset."""
        return self._info(self._assets.put(path, AssetKind.RAW))

    def put_final(self, data: bytes, report: ComplianceReport) -> AssetInfo:
        """Store rendered bytes as a `final` asset and put the verdict on its row.

        The verdict is written even when the bytes dedupe to an existing asset: identical
        bytes get the identical report, so the write is idempotent.
        """
        stored = self._assets.put(data, AssetKind.FINAL)
        # `put` committed in its own session, so the row is loaded afresh in this one.
        row = self._session.get(Asset, stored.id)
        if row is None:  # pragma: no cover - `put` just committed this row
            msg = f"asset {stored.id!r}"
            raise NotFoundError(msg)
        row.compliant = report.ok
        row.compliance_report_json = report.model_dump_json()
        self._session.flush()
        return self._info(row)

    def commit(self) -> None:
        """Make everything written so far durable."""
        self._session.commit()

    def get(self, run_id: str) -> Run:
        """The run with this id, or `NotFoundError`."""
        row = self._session.get(Run, run_id)
        if row is None:
            msg = f"run {run_id!r}"
            raise NotFoundError(msg, hint="run ids are printed by `thumbforge thumb generate`")
        return row

    def _iteration(self, iteration_id: str) -> Iteration:
        row = self._session.get(Iteration, iteration_id)
        if row is None:  # pragma: no cover - the service only passes ids it just created
            msg = f"iteration {iteration_id!r}"
            raise NotFoundError(msg)
        return row

    def _info(self, asset: Asset) -> AssetInfo:
        return AssetInfo(
            id=asset.id,
            sha256=asset.sha256,
            path=self._assets.path_for(asset),
            mime=asset.mime,
            width=asset.width,
            height=asset.height,
            bytes=asset.bytes,
        )
