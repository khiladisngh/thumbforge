"""Runs, iterations and provider profiles, as `HeroService` reads and writes them (ROADMAP P6.1).

`RunRepository` satisfies the `HeroStore` Protocol declared beside the service, and
`IterateStore` (P6.3) for the refinements that start from a stored run. It exchanges
the core value types (`HeroTarget`, `AssetInfo`, ...) rather than ORM rows, which `core` may
not name; `get` returns the row because the CLI renders from it, as `fetch` does.

The repository owns no transaction: it flushes, and the service calls `commit`. One rule
matters more than the rest: the `AssetStore` writes through its **own** connection, and
SQLite allows one writer, so the session must hold nothing uncommitted when `put_raw` or
`put_final` run. The service commits before every `await` and every asset write for that
reason; waiting out `busy_timeout` would only end in "database is locked".
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, cast

from sqlalchemy import or_, select, update

from thumbforge.core.enums import AssetKind, RunKind, RunStatus
from thumbforge.core.errors import AssetError, NotFoundError, UsageError
from thumbforge.core.providers import Cost
from thumbforge.core.services.batch import (
    BatchItem,
    BatchPlaylist,
    BatchReference,
    ExistingIteration,
    StoredBatch,
)
from thumbforge.core.services.hero import AssetInfo, HeroTarget, copy_assets
from thumbforge.core.services.iterate import IterateSource
from thumbforge.storage.models import Asset, Iteration, ProviderProfile, Run, utcnow_iso
from thumbforge.storage.models import Template as TemplateRow
from thumbforge.storage.repositories import (
    PlaylistRepository,
    VideoRepository,
    channel_meta,
    video_meta,
)

if TYPE_CHECKING:
    from collections.abc import Collection, Sequence
    from pathlib import Path

    from sqlalchemy.orm import Session

    from thumbforge.core.json import JsonValue
    from thumbforge.core.layout import Template
    from thumbforge.core.models import ComplianceReport
    from thumbforge.core.services.hero import IterationDraft, IterationOutcome
    from thumbforge.storage.assets import AssetStore


@dataclass(frozen=True, slots=True)
class RunDeletion:
    """What `RunRepository.delete_run` removed."""

    iterations: int
    #: The image files unlinked; empty unless the caller asked for assets to go.
    assets: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class CostReport:
    """What a run's own iterations consumed, as far as their provider said (ROADMAP P8.4).

    An iteration whose provider reported nothing (`cost_json` is null: a failed or unfinished
    one, or a provider with no usage figures) adds nothing to the sums and is counted in
    `no_cost_data`, so a total is never padded with zeros that nobody reported.
    """

    run_id: str
    iterations: int
    #: Iterations with a reported cost; the rest are `no_cost_data`.
    with_cost_data: int
    tokens_in: int
    tokens_out: int
    #: `None` when no iteration reported any: a provider may report tokens only.
    credits: Decimal | None
    #: The currency of `credits`; `None` when there are none or the iterations disagree.
    currency: str | None
    #: Provider time over the run's iterations, from the iteration column, not from `cost_json`.
    duration_ms: int

    @property
    def no_cost_data(self) -> int:
        """Iterations the provider reported no cost for."""
        return self.iterations - self.with_cost_data


def _attempts(response_json: str) -> int:
    """Provider calls recorded in an iteration's response; none for one that never ran."""
    attempts = cast("dict[str, JsonValue]", json.loads(response_json)).get("attempts", 0)
    return attempts if isinstance(attempts, int) else 0


class RunRepository:
    """Hero, iterate and batch runs over one session and one asset store."""

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
        video_id: str | None,
        params_json: str,
        iterations: Sequence[IterationDraft],
        parent_run_id: str | None = None,
        reference_asset_id: str | None = None,
        playlist_id: str | None = None,
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
                playlist_id=playlist_id,
                parent_run_id=parent_run_id,
                reference_asset_id=reference_asset_id,
                params_json=params_json,
                started_at=utcnow_iso(),
            )
        )
        rows = [
            Iteration(
                run_id=run_id,
                video_id=draft.video_id or video_id,
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

    def run_status(self, run_id: str) -> RunStatus:
        """The status of the run with this id."""
        return self.get(run_id).status

    def load_batch(self, run_id: str) -> StoredBatch:
        """What a batch run needs to be resumed: its status and the pieces of its spec."""
        run = self.get(run_id)
        if run.kind is not RunKind.BATCH or run.playlist_id is None:
            msg = f"run {run.id} is a {run.kind.value} run; only batch runs can be resumed"
            raise UsageError(msg, hint="`thumb generate` and `thumb iterate` make new runs instead")
        profile = run.provider_profile
        return StoredBatch(
            status=run.status,
            playlist_id=run.playlist_id,
            template_ref=f"{run.template.name}@{run.template.version}",
            provider_key=profile.provider_key,
            provider_params=cast("dict[str, JsonValue]", json.loads(profile.params_json)),
            params=cast("dict[str, JsonValue]", json.loads(run.params_json)),
        )

    def reopen_run(self, run_id: str) -> None:
        """Put a run back to `running`, clearing its end time and reason."""
        row = self.get(run_id)
        row.status = RunStatus.RUNNING
        row.error_text = None
        row.finished_at = None
        self._session.flush()

    def cancel_run(self, run_id: str) -> None:
        """Mark the run `cancelled`, and every iteration still `pending` or `running` with it."""
        self._session.execute(
            update(Iteration)
            .where(
                Iteration.run_id == run_id,
                Iteration.status.in_((RunStatus.PENDING, RunStatus.RUNNING)),
            )
            .values(status=RunStatus.CANCELLED)
            .execution_options(synchronize_session="fetch")
        )
        self.finish_run(run_id, RunStatus.CANCELLED, None)

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

    def list_runs(
        self, *, kind: RunKind | None = None, status: RunStatus | None = None, limit: int
    ) -> list[Run]:
        """The newest `limit` runs, newest first, optionally of one kind and one status."""
        query = select(Run).order_by(Run.created_at.desc(), Run.id.desc()).limit(limit)
        if kind is not None:
            query = query.where(Run.kind == kind)
        if status is not None:
            query = query.where(Run.status == status)
        return list(self._session.scalars(query))

    def cost_report(self, run_id: str) -> CostReport:
        """What the run's own iterations consumed; `NotFoundError` for an unknown run.

        Child runs (the batches built on a hero, the refinements of a pick) are runs of their
        own and are not folded in: read each one's report.
        """
        run = self.get(run_id)
        costs = [
            Cost.model_validate_json(item.cost_json)
            for item in run.iterations
            if item.cost_json is not None
        ]
        credits = [cost.credits for cost in costs if cost.credits is not None]
        currencies = {cost.currency for cost in costs if cost.currency is not None}
        return CostReport(
            run_id=run.id,
            iterations=len(run.iterations),
            with_cost_data=len(costs),
            tokens_in=sum(cost.tokens_in for cost in costs),
            tokens_out=sum(cost.tokens_out for cost in costs),
            credits=sum(credits, Decimal(0)) if credits else None,
            currency=currencies.pop() if len(currencies) == 1 else None,
            duration_ms=sum(item.duration_ms or 0 for item in run.iterations),
        )

    def delete_run(self, run_id: str, *, assets: bool) -> RunDeletion:
        """Delete a run and its iterations; with `assets`, the images nothing else uses too.

        `UsageError` while another run names this one as its parent (a refinement, or a batch
        whose hero it is) or uses one of its images as its reference: that run still needs it.
        Assets are content-addressed, so two runs that made the same image share one row and
        one file; a row and file go only when no remaining iteration or run refers to it.

        Unlike the rest of the repository this commits, because a file may only be unlinked
        once the rows that named it are gone for good.
        """
        run = self.get(run_id)
        iterations = list(run.iterations)
        owned = {
            asset_id
            for item in iterations
            for asset_id in (item.raw_asset_id, item.final_asset_id)
            if asset_id is not None
        }
        dependents = sorted(
            self._session.scalars(
                select(Run.id).where(
                    Run.id != run.id,
                    or_(Run.parent_run_id == run.id, Run.reference_asset_id.in_(owned)),
                )
            )
        )
        if dependents:
            msg = f"run {run.id} is still used by run {', '.join(dependents)}"
            raise UsageError(
                msg, hint="delete those runs first with `thumbforge runs delete <run>`"
            )
        candidates = owned if run.reference_asset_id is None else {*owned, run.reference_asset_id}
        self._session.delete(run)
        self._session.flush()
        files = self._drop_unreferenced(candidates) if assets else []
        self._session.commit()
        for path in files:
            path.unlink(missing_ok=True)
        return RunDeletion(iterations=len(iterations), assets=tuple(files))

    def pick(self, run_id: str, target: int | str) -> Iteration:
        """Make `target` the run's one picked iteration; its siblings are un-picked.

        `target` is an ordinal or the id of one of this run's iterations. Picking again moves
        the pick, and picking the picked iteration changes nothing. Only a completed iteration
        can be picked: a failed one has no usable final.
        """
        run = self.get(run_id)
        listing = f"`thumbforge runs show {run.id}` lists the run's iterations"
        match target:
            case int():
                chosen = next((row for row in run.iterations if row.ordinal == target), None)
            case str():
                chosen = next((row for row in run.iterations if row.id == target), None)
        if chosen is None:
            msg = f"iteration {target!r} of run {run.id!r}"
            raise NotFoundError(msg, hint=listing)
        if chosen.status is not RunStatus.COMPLETED:
            msg = f"iteration {chosen.ordinal} of run {run.id} is {chosen.status.value}"
            raise UsageError(msg, hint=f"pick a completed iteration; {listing}")
        # One statement: the run is never seen with no pick or with two.
        self._session.execute(
            update(Iteration)
            .where(Iteration.run_id == run.id)
            .values(picked=Iteration.id == chosen.id)
            .execution_options(synchronize_session="fetch")
        )
        self._session.refresh(chosen)
        return chosen

    def resolve_source(self, ref: str, *, from_picked: bool) -> IterateSource:
        """What `thumb iterate REF` refines: a run's pick, or the iteration `REF` names.

        An iteration id names its iteration outright, picked or not; it must be completed,
        like a pick, because only a completed iteration has a usable raw asset. A run id
        yields the run's picked iteration, or with `from_picked` the nearest pick walking up
        its parent chain. The child attaches to the run named (the iteration's own run for an
        iteration id), whichever run the reference came from.
        """
        found = self.resolve_target(ref)
        if isinstance(found, Iteration):
            run, chosen = found.run, found
        else:
            run, chosen = found, self._picked(found, walk=from_picked)
        listing = f"`thumbforge runs show {run.id}` lists the run's iterations"
        if chosen is None:
            where = "or any run it came from " if from_picked else ""
            msg = f"run {run.id} has no picked iteration {where}to refine"
            raise UsageError(
                msg,
                hint=(
                    f"pick one with `thumbforge thumb pick {run.id} <ordinal>`, "
                    "or name an iteration id"
                ),
            )
        if chosen.status is not RunStatus.COMPLETED or chosen.raw_asset is None:
            msg = f"iteration {chosen.ordinal} of run {chosen.run_id} is {chosen.status.value}"
            raise UsageError(msg, hint=f"refine a completed iteration; {listing}")
        if run.video_id is None:  # pragma: no cover - hero runs always carry their video
            msg = f"run {run.id} has no video to refine"
            raise UsageError(msg, hint=listing)
        profile = run.provider_profile
        return IterateSource(
            parent_run_id=run.id,
            video_id=run.video_id,
            template_ref=f"{run.template.name}@{run.template.version}",
            provider_key=profile.provider_key,
            provider_params=cast("dict[str, JsonValue]", json.loads(profile.params_json)),
            reference=self._info(chosen.raw_asset),
        )

    def resolve_playlist(self, reference: str) -> BatchPlaylist:
        """The stored playlist named by a ULID or YouTube id, with its items in order."""
        playlists = PlaylistRepository(self._session)
        playlist = playlists.resolve(reference)
        items = tuple(
            BatchItem(
                target=HeroTarget(
                    row_id=item.video_id,
                    video=video_meta(item.video),
                    channel=None
                    if item.video.channel is None
                    else channel_meta(item.video.channel),
                ),
                position=item.position,
                part_number=item.part_number,
                part_label=item.part_label,
            )
            for item in playlists.items(playlist)
        )
        return BatchPlaylist(row_id=playlist.id, items=items)

    def resolve_reference(self, ref: str, *, raw: bool) -> BatchReference:
        """The image a batch takes as its style reference, from a hero run or iteration.

        A run yields its picked iteration; an iteration id names its iteration outright. It
        must be completed. `raw` chooses the art without overlay text over the finished
        thumbnail. The batch hangs off the run the iteration belongs to, and the file must
        still match its hash: a reference that has gone missing is an asset error, not a
        silent prompt-only run.
        """
        found = self.resolve_target(ref)
        if isinstance(found, Iteration):
            run, chosen = found.run, found
        else:
            run, chosen = found, self._picked(found, walk=False)
        listing = f"`thumbforge runs show {run.id}` lists the run's iterations"
        if chosen is None:
            msg = f"run {run.id} has no picked iteration to use as the reference"
            raise UsageError(
                msg,
                hint=(
                    f"pick one with `thumbforge thumb pick {run.id} <ordinal>`, "
                    "or name an iteration id"
                ),
            )
        asset = chosen.raw_asset if raw else chosen.final_asset
        if chosen.status is not RunStatus.COMPLETED or asset is None:
            msg = f"iteration {chosen.ordinal} of run {chosen.run_id} is {chosen.status.value}"
            raise UsageError(msg, hint=f"use a completed iteration; {listing}")
        if not self._assets.verify(asset):
            msg = f"the reference image {asset.id} is missing or does not match its hash"
            raise AssetError(msg, hint="generate the hero again and pick it")
        return BatchReference(parent_run_id=run.id, iteration_id=chosen.id, asset=self._info(asset))

    def iterations_by_key(self, keys: Collection[str]) -> dict[str, Iteration]:
        """The stored iterations whose idempotency key is in `keys`, by key, as rows to render."""
        rows = self._session.scalars(
            select(Iteration).where(Iteration.idempotency_key.in_(keys))
        ).all()
        return {row.idempotency_key: row for row in rows}

    def find_iterations(self, keys: Collection[str]) -> dict[str, ExistingIteration]:
        """The iterations whose idempotency key is in `keys`, by key, with their try counts."""
        return {
            key: ExistingIteration(
                id=row.id,
                run_id=row.run_id,
                status=row.status,
                attempts=_attempts(row.provider_response_json),
                started_at=None
                if row.started_at is None
                else datetime.fromisoformat(row.started_at),
            )
            for key, row in self.iterations_by_key(keys).items()
        }

    def resolve_target(self, ref: str) -> Run | Iteration:
        """The run or the iteration `ref` is the id of; `NotFoundError` if it is neither."""
        found = self._session.get(Run, ref) or self._session.get(Iteration, ref)
        if found is None:
            msg = f"run or iteration {ref!r}"
            raise NotFoundError(
                msg,
                hint="ids are printed by `thumbforge thumb generate` and `thumbforge runs show`",
            )
        return found

    def export(self, target: Run | Iteration, to: Path, *, raw: bool) -> list[Path]:
        """Copy the final (or, with `raw`, the raw) assets of `target` into the directory `to`.

        A run exports every completed iteration, an iteration only itself. Files are named
        `<youtube id>-<ordinal><extension>`, as `thumb generate --out` names them.
        """
        run = target if isinstance(target, Run) else target.run
        candidates = sorted(run.iterations, key=lambda row: row.ordinal)
        if isinstance(target, Iteration):
            candidates = [target]
        files: list[tuple[int, Path]] = []
        for item in candidates:
            asset = item.raw_asset if raw else item.final_asset
            if item.status is RunStatus.COMPLETED and asset is not None:
                files.append((item.ordinal, self._assets.path_for(asset)))
        if not files:
            subject = (
                f"iteration {target.ordinal} of run {run.id}"
                if isinstance(target, Iteration)
                else f"run {run.id}"
            )
            msg = f"{subject} has no completed iteration to export"
            raise UsageError(msg, hint=f"`thumbforge runs show {run.id}` lists each outcome")
        stem = run.id if run.video is None else run.video.youtube_id
        return copy_assets(to, stem, files)

    @staticmethod
    def _picked(run: Run, *, walk: bool) -> Iteration | None:
        """The run's picked iteration; with `walk`, the nearest one up the parent chain."""
        current: Run | None = run
        while current is not None:
            picked = next((row for row in current.iterations if row.picked), None)
            if picked is not None or not walk:
                return picked
            current = current.parent_run
        return None

    def _drop_unreferenced(self, candidates: set[str]) -> list[Path]:
        """Delete the asset rows among `candidates` that nothing refers to; their file paths."""
        used = {
            *self._session.scalars(
                select(Iteration.raw_asset_id).where(Iteration.raw_asset_id.in_(candidates))
            ),
            *self._session.scalars(
                select(Iteration.final_asset_id).where(Iteration.final_asset_id.in_(candidates))
            ),
            *self._session.scalars(
                select(Run.reference_asset_id).where(Run.reference_asset_id.in_(candidates))
            ),
        }
        rows = self._session.scalars(select(Asset).where(Asset.id.in_(candidates - used))).all()
        paths = sorted(self._assets.path_for(row) for row in rows)
        for row in rows:
            self._session.delete(row)
        self._session.flush()
        return paths

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
