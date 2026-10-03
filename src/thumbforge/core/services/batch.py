"""`BatchService` — one thumbnail per playlist item, idempotent and resumable (ROADMAP P7.1).

A batch run takes a playlist, a picked hero's image as the style reference, a template and a
provider, and produces one iteration per selected item. What this module decides:

- which items are selected (`--only`, and which items count when it is absent),
- what each item's idempotency key is and, from the stored iterations, what to do about it:
  skip a `completed` one, retry a `failed` one while it has attempts left, create the rest,
- the pre-flight budget guard (`--max-images`), applied before anything is written,
- how items are bounded (one semaphore over the provider call) and how outcomes roll up,
- how a run ends early (an interrupt pauses it), continues (`resume`) and is abandoned (`cancel`).

The per-item pipeline is `hero.run_iteration`: a batch item is generated, stored, finalized and
recorded exactly as a hero iteration is. Every collaborator arrives as a Protocol, so this module
imports no adapter package and, like `hero`, logs nothing.

Not here yet: the `runs` commands (P7.4), which call `resume` and `cancel`. The `batch` command
and its progress display (P7.3) live in `cli/batch.py`; `BatchResult.error` is what it raises.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any, Final, Literal, Protocol, cast

from thumbforge.core.enums import RunKind, RunStatus
from thumbforge.core.errors import (
    ExitCode,
    PartialBatchError,
    ProviderError,
    RunInterruptedError,
    TemplateError,
    ThumbforgeError,
    UsageError,
)
from thumbforge.core.ids import new_id, sha256_bytes
from thumbforge.core.json import JsonPayload, JsonValue, canonical_json
from thumbforge.core.services.hero import (
    INTERRUPTED,
    IterationDraft,
    IterationStore,
    RunContext,
    failure_text,
    run_iteration,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Collection, Coroutine, Mapping, Sequence
    from pathlib import Path

    from thumbforge.core.layout import Template
    from thumbforge.core.providers import ImageProvider
    from thumbforge.core.services.hero import (
        AssetInfo,
        Done,
        Finalize,
        HeroTarget,
        ProgressSink,
        ProviderRegistry,
        TemplateRenderer,
    )

#: Provider calls an item may spend over all its tries when the caller does not say.
DEFAULT_MAX_RETRIES: Final = 2
#: Seconds after which an iteration still `running` is taken to belong to a dead process.
DEFAULT_STALE_AFTER_S: Final = 900


class PlanAction(StrEnum):
    """What a batch will do with one item."""

    SKIP = "skip"
    RETRY = "retry"
    CREATE = "create"


@dataclass(frozen=True, slots=True)
class BatchSpec:
    """What the user asked for. `playlist_id` and `hero` are ULIDs or YouTube/run ids."""

    playlist_id: str
    #: A run (its picked iteration is the style reference) or an iteration id.
    hero: str
    template_ref: str
    provider_key: str
    concurrency: int = 2
    #: Part numbers to generate; `None` means every item that has a part number.
    only: frozenset[int] | None = None
    dry_run: bool = False
    #: Which of the hero's images is the reference: the finished thumbnail or the bare art.
    reference: Literal["final", "raw"] = "final"
    max_images: int | None = None
    max_retries: int = DEFAULT_MAX_RETRIES
    provider_params: Mapping[str, JsonValue] = field(default_factory=dict[str, JsonValue])


@dataclass(frozen=True, slots=True)
class BatchItem:
    """One playlist item as the service needs it."""

    target: HeroTarget
    position: int
    part_number: int | None
    part_label: str | None


@dataclass(frozen=True, slots=True)
class BatchPlaylist:
    """A stored playlist: its row id and its items in playlist order."""

    row_id: str
    items: tuple[BatchItem, ...]


@dataclass(frozen=True, slots=True)
class BatchReference:
    """The style reference a batch is given: the hero run it hangs off and the image."""

    parent_run_id: str
    #: The hero iteration the image belongs to; a resume names it, so a later pick cannot move it.
    iteration_id: str
    asset: AssetInfo


@dataclass(frozen=True, slots=True)
class ExistingIteration:
    """A stored iteration found by its idempotency key."""

    id: str
    #: The run the iteration was created in, which keeps it however many later runs retry it.
    run_id: str
    status: RunStatus
    #: Provider calls spent on it over all earlier tries.
    attempts: int
    started_at: datetime | None


@dataclass(frozen=True, slots=True)
class StoredBatch:
    """A batch run as stored: its status and what its `BatchSpec` is rebuilt from."""

    status: RunStatus
    playlist_id: str
    template_ref: str
    provider_key: str
    provider_params: Mapping[str, JsonValue]
    #: The run's own parameters, as `BatchService.run` recorded them.
    params: Mapping[str, JsonValue]


class BatchStore(IterationStore, Protocol):
    """The persistence surface a batch run needs, satisfied by `storage.runs.RunRepository`."""

    def resolve_playlist(self, reference: str) -> BatchPlaylist:
        """The stored playlist named by a ULID or YouTube id; `NotFoundError` if unknown."""
        ...

    def resolve_reference(self, ref: str, *, raw: bool) -> BatchReference:
        """The reference image of the run's picked iteration, or of the iteration named.

        `NotFoundError` for an unknown id, `UsageError` when nothing is picked or the
        iteration is not completed, `AssetError` when the file is missing or altered.
        """
        ...

    def find_iterations(self, keys: Collection[str]) -> Mapping[str, ExistingIteration]:
        """The stored iterations whose idempotency key is in `keys`, by key."""
        ...

    def create_run(
        self,
        run_id: str,
        *,
        kind: RunKind,
        template: Template,
        profile_id: str,
        video_id: str | None,
        playlist_id: str,
        params_json: str,
        iterations: Sequence[IterationDraft],
        parent_run_id: str,
        reference_asset_id: str,
    ) -> list[str]:
        """Insert a `running` run and its `pending` iterations; return the iteration ids."""
        ...

    def run_status(self, run_id: str) -> RunStatus:
        """The status of any run; `NotFoundError` if unknown."""
        ...

    def load_batch(self, run_id: str) -> StoredBatch:
        """A batch run to resume; `NotFoundError` if unknown, `UsageError` if not a batch."""
        ...

    def reopen_run(self, run_id: str) -> None:
        """Put a run back to `running`, clearing its end time and reason."""
        ...

    def cancel_run(self, run_id: str) -> None:
        """Mark the run `cancelled`, and every iteration still `pending` or `running` with it."""
        ...


@dataclass(frozen=True, slots=True)
class PlanRow:
    """One selected item and what the batch will do with it."""

    item: BatchItem
    key: str
    prompt: str
    action: PlanAction
    reason: str
    #: The stored iteration with this key, when there is one.
    existing: ExistingIteration | None


@dataclass(frozen=True, slots=True)
class BatchPlan:
    """Every selected item, in playlist order."""

    rows: tuple[PlanRow, ...]

    @property
    def work(self) -> tuple[PlanRow, ...]:
        """The rows that call the provider: `create` and `retry`."""
        return tuple(row for row in self.rows if row.action is not PlanAction.SKIP)


@dataclass(frozen=True, slots=True)
class BatchResult:
    """How a batch ended. Counts only: the CLI reads the stored rows back to render them.

    A skipped `completed` item counts as completed, and a skipped item that has used up its
    retries counts as failed, so a re-run reports the playlist's state, not just its own work.
    A batch has no compliance exit: a non-compliant final is an ordinary failure (spec P7).
    """

    plan: BatchPlan
    #: `None` for a dry run, which writes no run.
    run_id: str | None
    status: RunStatus | None
    #: The iterations this batch ran, in playlist order.
    iteration_ids: tuple[str, ...]
    completed: int
    failed: int
    #: Items an interrupt left unstarted; `resume` picks them up.
    pending: int = 0
    #: A reference was asked for but the provider cannot take one, so the run went prompt-only.
    reference_ignored: bool = False

    @property
    def exit_code(self) -> ExitCode:
        """`130` when interrupted; `0` clean; `4` when nothing completed; else `6`."""
        if self.status is RunStatus.PAUSED:
            return ExitCode.INTERRUPTED
        if self.failed == 0:
            return ExitCode.OK
        return ExitCode.PROVIDER if self.completed == 0 else ExitCode.PARTIAL

    def error(self) -> ThumbforgeError | None:
        """The error the CLI raises once it has printed the result, or `None` on success.

        Re-running the same command is the way to continue until `runs resume` exists (P7.4):
        it retries failed and unfinished items inside the run that created them.
        """
        total = len(self.plan.rows)
        run_id = self.run_id or ""
        again = (
            "run the same command again to retry what is left; "
            f"`thumbforge runs show {run_id}` lists each iteration"
        )
        match self.exit_code:
            case ExitCode.OK:
                return None
            case ExitCode.INTERRUPTED:
                counts = f"{self.completed} completed, {self.failed} failed, {self.pending} pending"
                return RunInterruptedError(f"run {run_id} paused ({counts})", hint=again)
            case ExitCode.PROVIDER:
                msg = (
                    f"all {total} items failed"
                    if self.failed == total
                    else f"no item completed, {self.failed} of {total} failed"
                )
                return ProviderError(msg, hint=again)
            case _:
                return PartialBatchError(
                    f"{self.completed} of {total} items completed, {self.failed} failed",
                    hint=f"the completed items are kept; {again}",
                    completed=self.completed,
                    failed=self.failed,
                    pending=self.pending,
                )


def idempotency_key(
    template: Template,
    profile_id: str,
    youtube_id: str,
    part_number: int | None,
    prompt: str,
    seed: int | None,
    reference_sha256: str,
) -> str:
    """`PLAN.md` §6's key: one item, prompt, template, provider and reference give one key.

    `part_number` and `seed` are empty strings when absent, as in the hero keys.
    """
    material = (
        template.spec_hash
        + profile_id
        + youtube_id
        + ("" if part_number is None else str(part_number))
        + prompt
        + ("" if seed is None else str(seed))
        + reference_sha256
    )
    return sha256_bytes(material.encode())[:32]


def select_items(items: Sequence[BatchItem], only: Collection[int] | None) -> list[BatchItem]:
    """The items a batch covers.

    Without `only`, every item that has a part number: `playlist renumber --skip` clears it on
    purpose. With `only`, the items whose part number is listed, plus a part-less item whose
    playlist position is listed.
    """
    if only is None:
        return [item for item in items if item.part_number is not None]
    return [
        item
        for item in items
        if (item.part_number if item.part_number is not None else item.position) in only
    ]


def _classify(
    existing: ExistingIteration | None, max_retries: int, stale_after_s: int, now: datetime
) -> tuple[PlanAction, str]:
    """`PLAN.md` §6's resume algorithm for one key.

    A `running` iteration older than `stale_after_s` belongs to a process that died, so it is
    treated as `failed`; a younger one may still be running and is left alone.
    """
    if existing is None:
        return PlanAction.CREATE, "new"
    stale = existing.status is RunStatus.RUNNING and (
        existing.started_at is None or (now - existing.started_at).total_seconds() > stale_after_s
    )
    tries = f"{existing.attempts} of {max_retries} tries used"
    match existing.status:
        case RunStatus.COMPLETED:
            return PlanAction.SKIP, "completed"
        case RunStatus.RUNNING if not stale:
            return PlanAction.SKIP, "running in another run"
        case RunStatus.RUNNING | RunStatus.FAILED:
            label = "stale" if stale else "failed"
            if existing.attempts >= max_retries:
                return PlanAction.SKIP, f"{label}, {tries}"
            return PlanAction.RETRY, f"{label}, {tries}"
        case _:
            return PlanAction.RETRY, f"unfinished ({existing.status.value})"


def _draft(row: PlanRow) -> IterationDraft:
    return IterationDraft(
        ordinal=row.item.position,
        idempotency_key=row.key,
        prompt_text=row.prompt,
        seed=None,
        video_id=row.item.target.row_id,
        part_number=row.item.part_number,
        part_label=row.item.part_label,
        prior_attempts=0 if row.existing is None else row.existing.attempts,
    )


def _run_params(spec: BatchSpec, hero_iteration_id: str) -> JsonPayload:
    """What a run records of its spec; `_spec_from` reads it back.

    The hero is stored as the iteration whose image was used, not as the run or iteration the
    user named, so a later pick on the hero run cannot change what a resume refers to.
    """
    return {
        "hero": hero_iteration_id,
        "concurrency": spec.concurrency,
        "only": None if spec.only is None else sorted(spec.only),
        "reference": spec.reference,
        "max_images": spec.max_images,
        "max_retries": spec.max_retries,
    }


def _spec_from(stored: StoredBatch) -> BatchSpec:
    """The `BatchSpec` a stored run was started with."""
    params = stored.params
    only = cast("list[int] | None", params["only"])
    return BatchSpec(
        playlist_id=stored.playlist_id,
        hero=cast("str", params["hero"]),
        template_ref=stored.template_ref,
        provider_key=stored.provider_key,
        concurrency=cast("int", params["concurrency"]),
        only=None if only is None else frozenset(only),
        reference=cast("Literal['final', 'raw']", params["reference"]),
        max_images=cast("int | None", params["max_images"]),
        max_retries=cast("int", params["max_retries"]),
        provider_params=stored.provider_params,
    )


async def _until_cancelled[T](
    job: Callable[[], Coroutine[Any, Any, T]], cancel: asyncio.Event | None
) -> T | None:
    """Run `job` unless `cancel` is set first; `None` when it was cut short.

    The job is cancelled and awaited, so whatever it does on cancellation is finished before
    this returns. A cancellation of the caller is passed on the same way and then re-raised.
    """
    if cancel is not None and cancel.is_set():
        return None
    work = asyncio.create_task(job())
    watcher = None if cancel is None else asyncio.create_task(cancel.wait())
    try:
        await asyncio.wait(
            {work} if watcher is None else {work, watcher}, return_when=asyncio.FIRST_COMPLETED
        )
    finally:
        if watcher is not None:
            watcher.cancel()
        work.cancel()
        await asyncio.wait({work})
    return None if work.cancelled() else work.result()


@dataclass(frozen=True, slots=True)
class _Prepared:
    """Everything resolved before a batch writes its first row."""

    playlist: BatchPlaylist
    reference: BatchReference
    template: Template
    provider: ImageProvider
    profile_id: str
    plan: BatchPlan


class BatchService:
    """Generate one thumbnail per playlist item, skipping what is already done."""

    def __init__(
        self,
        store: BatchStore,
        registry: ProviderRegistry,
        renderer: TemplateRenderer,
        finalize: Finalize,
        *,
        logs_dir: Path,
        stale_after_s: int = DEFAULT_STALE_AFTER_S,
    ) -> None:
        """Take the collaborators the CLI selected; `logs_dir` holds `<run_id>/` workdirs."""
        self._store = store
        self._registry = registry
        self._renderer = renderer
        self._finalize = finalize
        self._logs_dir = logs_dir
        self._stale_after_s = stale_after_s

    async def plan(self, spec: BatchSpec) -> BatchPlan:
        """What `run` would do, computed without a provider call and without writing a run.

        It is `async` because a key needs the provider's identity, and the first use of a
        provider settings snapshot is stored (a `provider_profile` row is the only write).
        """
        return (await self._prepare(spec)).plan

    async def run(
        self, spec: BatchSpec, *, progress: ProgressSink, cancel: asyncio.Event | None = None
    ) -> BatchResult:
        """Run `spec` to completion and report how it ended; a dry run only plans.

        Raises before any run exists when the playlist, hero, template or provider is
        unknown, a prompt does not render, nothing is selected, or the images to generate
        would exceed `max_images`. Once the run exists, per-item failures are recorded and
        reflected in the result instead of raised.

        Setting `cancel` interrupts the run: iterations in flight end `failed` with
        `error_text = "interrupted"`, those not yet started stay `pending`, finished ones are
        untouched, and the run ends `paused` (exit `130`). Cancelling the task running this
        does the same, then raises `CancelledError` as asyncio requires.
        """
        prepared = await self._prepare(spec)
        plan = prepared.plan
        if spec.dry_run:
            return BatchResult(plan, None, None, (), 0, 0)

        work = plan.work
        if spec.max_images is not None and len(work) > spec.max_images:
            msg = f"{len(work)} images to generate exceeds --max-images {spec.max_images}"
            raise UsageError(
                msg,
                hint="raise --max-images or narrow the batch with --only; --dry-run shows the plan",
            )

        store = self._store
        reference = prepared.reference
        run_id = new_id()
        created = iter(
            store.create_run(
                run_id,
                kind=RunKind.BATCH,
                template=prepared.template,
                profile_id=prepared.profile_id,
                video_id=None,
                playlist_id=prepared.playlist.row_id,
                params_json=canonical_json(_run_params(spec, reference.iteration_id)),
                iterations=[_draft(row) for row in work if row.action is PlanAction.CREATE],
                parent_run_id=reference.parent_run_id,
                reference_asset_id=reference.asset.id,
            )
        )
        # A retried item keeps the iteration (and run) it was created in: its key is unique.
        iteration_ids = [next(created) if row.existing is None else row.existing.id for row in work]
        store.commit()
        return await self._execute(
            prepared, spec, run_id, plan.rows, work, iteration_ids, progress, cancel
        )

    async def resume(
        self,
        run_id: str,
        *,
        progress: ProgressSink,
        cancel: asyncio.Event | None = None,
        concurrency: int | None = None,
    ) -> BatchResult:
        """Continue a batch run: retry what it left unfinished or failed, nothing else.

        The run's `BatchSpec` is rebuilt from what it stored, so the same keys come out and
        the same reference image is used; `concurrency` may override. Resume works on the
        iterations the run itself created, in place, and ends that same run: no new run is
        made, and iterations that belong to other runs are not touched. A `running` iteration
        younger than `stale_after_s` is left alone, an older one is retried.

        `NotFoundError` for an unknown run; `UsageError` for one that is not a batch run or is
        `completed` or `cancelled`. Interrupts behave as in `run`.
        """
        stored = self._store.load_batch(run_id)
        if stored.status in (RunStatus.COMPLETED, RunStatus.CANCELLED):
            msg = f"run {run_id} is {stored.status.value} and cannot be resumed"
            raise UsageError(msg, hint="start a new batch to generate again")
        spec = _spec_from(stored)
        if concurrency is not None:
            spec = replace(spec, concurrency=concurrency)
        prepared = await self._prepare(spec)
        owned = [
            row
            for row in prepared.plan.rows
            if row.existing is not None and row.existing.run_id == run_id
        ]
        work = [row for row in owned if row.action is PlanAction.RETRY]
        iteration_ids = [row.existing.id for row in work if row.existing is not None]
        self._store.reopen_run(run_id)
        self._store.commit()
        return await self._execute(
            prepared, spec, run_id, owned, work, iteration_ids, progress, cancel
        )

    def cancel(self, run_id: str) -> None:
        """Abandon a run: it and its unfinished iterations become `cancelled`.

        `UsageError` for a `completed` run, which has nothing left to cancel; cancelling a
        `cancelled` run changes nothing. Stopping a process that is running it is the
        caller's job (`run`'s `cancel` event).
        """
        status = self._store.run_status(run_id)
        if status is RunStatus.COMPLETED:
            msg = f"run {run_id} is completed and cannot be cancelled"
            raise UsageError(msg, hint="a completed run has nothing left to cancel")
        if status is not RunStatus.CANCELLED:
            self._store.cancel_run(run_id)
            self._store.commit()

    async def _execute(
        self,
        prepared: _Prepared,
        spec: BatchSpec,
        run_id: str,
        scope: Sequence[PlanRow],
        work: Sequence[PlanRow],
        iteration_ids: Sequence[str],
        progress: ProgressSink,
        cancel: asyncio.Event | None,
    ) -> BatchResult:
        """Run `work` inside the existing run `run_id` and close the run.

        `scope` is every plan row whose state the run reports: the whole selection for a new
        run, the run's own iterations for a resume. Counts and status are read back from the
        stored rows, so they hold for an interrupted run as well.
        """
        store = self._store
        provider = prepared.provider
        progress.run_started(run_id, len(work))
        workdir = self._logs_dir / run_id
        workdir.mkdir(parents=True, exist_ok=True)
        capabilities = provider.capabilities
        gate = asyncio.Semaphore(max(1, min(spec.concurrency, capabilities.max_concurrency)))
        usable_reference = capabilities.supports_reference_image
        references = (prepared.reference.asset.path,) if usable_reference else ()

        async def items() -> list[Done]:
            async with asyncio.TaskGroup() as group:
                tasks = [
                    group.create_task(
                        run_iteration(
                            store,
                            self._finalize,
                            RunContext(
                                run_id,
                                row.item.target,
                                prepared.template,
                                spec.provider_params,
                                provider,
                                workdir,
                                gate,
                                progress,
                                references,
                            ),
                            iteration_id,
                            _draft(row),
                        )
                    )
                    for row, iteration_id in zip(work, iteration_ids, strict=True)
                ]
            return [task.result() for task in tasks]

        try:
            done = await _until_cancelled(items, cancel)
        except asyncio.CancelledError:
            # Ctrl-C under `asyncio.run` cancels the main task: pause the run, then let it go.
            store.finish_run(run_id, RunStatus.PAUSED, INTERRUPTED)
            store.commit()
            raise
        except BaseException as error:
            # A bug: the run must not stay `running` forever.
            store.finish_run(run_id, RunStatus.FAILED, failure_text(error))
            store.commit()
            raise

        found = store.find_iterations([row.key for row in scope])
        states = [found[row.key].status for row in scope]
        completed = states.count(RunStatus.COMPLETED)
        failed = states.count(RunStatus.FAILED)
        if done is None:
            status, reason = RunStatus.PAUSED, INTERRUPTED
        elif failed == 0:
            status, reason = RunStatus.COMPLETED, None
        else:
            status, reason = RunStatus.FAILED, f"{failed} of {len(scope)} items failed"
        store.finish_run(run_id, status, reason)
        store.commit()
        return BatchResult(
            plan=prepared.plan,
            run_id=run_id,
            status=status,
            iteration_ids=tuple(iteration_ids),
            completed=completed,
            failed=failed,
            pending=states.count(RunStatus.PENDING),
            reference_ignored=not usable_reference,
        )

    async def _prepare(self, spec: BatchSpec) -> _Prepared:
        """Resolve everything a batch needs and plan it; nothing but the profile is written."""
        store = self._store
        playlist = store.resolve_playlist(spec.playlist_id)
        reference = store.resolve_reference(spec.hero, raw=spec.reference == "raw")
        template = self._renderer.resolve(spec.template_ref)
        provider = self._registry.get(spec.provider_key, spec.provider_params)
        info = await provider.info()

        selected = select_items(playlist.items, spec.only)
        if not selected:
            msg = "no playlist item is selected"
            raise UsageError(
                msg,
                hint="`--only` lists part numbers; `thumbforge playlist show --videos` shows them",
            )
        prompts: list[str] = []
        for item in selected:
            prompt = self._renderer.render(
                template,
                item.target.video,
                item.target.channel,
                {},
                part_number=item.part_number,
                part_label=item.part_label,
            )
            if not prompt.strip():
                msg = f"template {template.ref} rendered an empty prompt for part {item.position}"
                raise TemplateError(msg, hint="check the template's prompt")
            prompts.append(prompt)

        params_json = canonical_json(dict(spec.provider_params))
        profile_name = f"{info.key}@{info.version}:{sha256_bytes(params_json.encode())[:12]}"
        profile_id = store.ensure_profile(profile_name, info.key, info.version, params_json)
        store.commit()

        keys = [
            idempotency_key(
                template,
                profile_id,
                item.target.video.youtube_id,
                item.part_number,
                prompt,
                None,
                reference.asset.sha256,
            )
            for item, prompt in zip(selected, prompts, strict=True)
        ]
        found = store.find_iterations(keys)
        now = datetime.now(UTC)
        rows: list[PlanRow] = []
        for item, prompt, key in zip(selected, prompts, keys, strict=True):
            existing = found.get(key)
            action, reason = _classify(existing, spec.max_retries, self._stale_after_s, now)
            rows.append(PlanRow(item, key, prompt, action, reason, existing))
        return _Prepared(
            playlist, reference, template, provider, profile_id, BatchPlan(tuple(rows))
        )
