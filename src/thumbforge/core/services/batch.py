"""`BatchService` — one thumbnail per playlist item, idempotent and resumable (ROADMAP P7.1).

A batch run takes a playlist, a picked hero's image as the style reference, a template and a
provider, and produces one iteration per selected item. What this module decides:

- which items are selected (`--only`, and which items count when it is absent),
- what each item's idempotency key is and, from the stored iterations, what to do about it:
  skip a `completed` one, retry a `failed` one while it has attempts left, create the rest,
- the pre-flight budget guard (`--max-images`), applied before anything is written,
- how items are bounded (one semaphore over the provider call) and how outcomes roll up.

The per-item pipeline is `hero.run_iteration`: a batch item is generated, stored, finalized and
recorded exactly as a hero iteration is. Every collaborator arrives as a Protocol, so this module
imports no adapter package and, like `hero`, logs nothing.

Not here yet: interruption, pause and resume (P7.2), the `batch` command and its progress
display (P7.3), and `runs list|delete` (P7.4).
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING, Final, Literal, Protocol

from thumbforge.core.enums import RunKind, RunStatus
from thumbforge.core.errors import ExitCode, TemplateError, UsageError
from thumbforge.core.ids import new_id, sha256_bytes
from thumbforge.core.json import JsonPayload, JsonValue, canonical_json
from thumbforge.core.services.hero import (
    IterationDraft,
    IterationStore,
    RunContext,
    failure_text,
    run_iteration,
)

if TYPE_CHECKING:
    from collections.abc import Collection, Mapping, Sequence
    from pathlib import Path

    from thumbforge.core.layout import Template
    from thumbforge.core.providers import ImageProvider
    from thumbforge.core.services.hero import (
        AssetInfo,
        Finalize,
        HeroTarget,
        ProgressSink,
        ProviderRegistry,
        TemplateRenderer,
    )

#: Provider calls an item may spend over all its tries when the caller does not say.
DEFAULT_MAX_RETRIES: Final = 2


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
    asset: AssetInfo


@dataclass(frozen=True, slots=True)
class ExistingIteration:
    """A stored iteration found by its idempotency key."""

    id: str
    status: RunStatus
    #: Provider calls spent on it over all earlier tries.
    attempts: int


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
    #: A reference was asked for but the provider cannot take one, so the run went prompt-only.
    reference_ignored: bool = False

    @property
    def exit_code(self) -> ExitCode:
        """`0` clean; `4` when nothing completed; else `6` (some failed, some completed)."""
        if self.failed == 0:
            return ExitCode.OK
        return ExitCode.PROVIDER if self.completed == 0 else ExitCode.PARTIAL


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


def _classify(existing: ExistingIteration | None, max_retries: int) -> tuple[PlanAction, str]:
    """`PLAN.md` §6's resume algorithm for one key."""
    if existing is None:
        return PlanAction.CREATE, "new"
    match existing.status:
        case RunStatus.COMPLETED:
            return PlanAction.SKIP, "completed"
        case RunStatus.RUNNING:
            return PlanAction.SKIP, "running in another run"
        case RunStatus.FAILED if existing.attempts >= max_retries:
            return PlanAction.SKIP, f"failed, {existing.attempts} of {max_retries} tries used"
        case RunStatus.FAILED:
            return PlanAction.RETRY, f"failed, {existing.attempts} of {max_retries} tries used"
        case _:
            return PlanAction.RETRY, f"unfinished ({existing.status.value})"


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
    ) -> None:
        """Take the collaborators the CLI selected; `logs_dir` holds `<run_id>/` workdirs."""
        self._store = store
        self._registry = registry
        self._renderer = renderer
        self._finalize = finalize
        self._logs_dir = logs_dir

    async def plan(self, spec: BatchSpec) -> BatchPlan:
        """What `run` would do, computed without a provider call and without writing a run.

        It is `async` because a key needs the provider's identity, and the first use of a
        provider settings snapshot is stored (a `provider_profile` row is the only write).
        """
        return (await self._prepare(spec)).plan

    async def run(self, spec: BatchSpec, *, progress: ProgressSink) -> BatchResult:
        """Run `spec` to completion and report how it ended; a dry run only plans.

        Raises before any run exists when the playlist, hero, template or provider is
        unknown, a prompt does not render, nothing is selected, or the images to generate
        would exceed `max_images`. Once the run exists, per-item failures are recorded and
        reflected in the result instead of raised.
        """
        prepared = await self._prepare(spec)
        plan, provider = prepared.plan, prepared.provider
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
        run_params: JsonPayload = {
            "hero": spec.hero,
            "concurrency": spec.concurrency,
            "only": None if spec.only is None else sorted(spec.only),
            "reference": spec.reference,
            "max_images": spec.max_images,
            "max_retries": spec.max_retries,
        }
        drafts = [
            IterationDraft(
                ordinal=row.item.position,
                idempotency_key=row.key,
                prompt_text=row.prompt,
                seed=None,
                video_id=row.item.target.row_id,
                part_number=row.item.part_number,
                part_label=row.item.part_label,
                prior_attempts=0 if row.existing is None else row.existing.attempts,
            )
            for row in work
        ]
        run_id = new_id()
        created = iter(
            store.create_run(
                run_id,
                kind=RunKind.BATCH,
                template=prepared.template,
                profile_id=prepared.profile_id,
                video_id=None,
                playlist_id=prepared.playlist.row_id,
                params_json=canonical_json(run_params),
                iterations=[
                    draft
                    for draft, row in zip(drafts, work, strict=True)
                    if row.action is PlanAction.CREATE
                ],
                parent_run_id=reference.parent_run_id,
                reference_asset_id=reference.asset.id,
            )
        )
        # A retried item keeps the iteration (and run) it was created in: its key is unique.
        iteration_ids = [next(created) if row.existing is None else row.existing.id for row in work]
        store.commit()
        progress.run_started(run_id, len(work))

        workdir = self._logs_dir / run_id
        workdir.mkdir(parents=True, exist_ok=True)
        capabilities = provider.capabilities
        gate = asyncio.Semaphore(max(1, min(spec.concurrency, capabilities.max_concurrency)))
        usable_reference = capabilities.supports_reference_image
        references = (reference.asset.path,) if usable_reference else ()

        try:
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
                            draft,
                        )
                    )
                    for row, iteration_id, draft in zip(work, iteration_ids, drafts, strict=True)
                ]
        except BaseException as error:
            # Cancellation, Ctrl-C or a bug: the run must not stay `running` forever.
            # Pausing and resuming it is P7.2's job.
            store.finish_run(run_id, RunStatus.FAILED, failure_text(error))
            store.commit()
            raise

        done = [task.result() for task in tasks]
        skipped = [row for row in plan.rows if row.action is PlanAction.SKIP]
        completed = sum(1 for item in done if item.status is RunStatus.COMPLETED) + sum(
            1 for row in skipped if row.existing and row.existing.status is RunStatus.COMPLETED
        )
        failed = sum(1 for item in done if item.status is not RunStatus.COMPLETED) + sum(
            1 for row in skipped if row.existing and row.existing.status is RunStatus.FAILED
        )
        status = RunStatus.COMPLETED if failed == 0 else RunStatus.FAILED
        store.finish_run(
            run_id,
            status,
            None if failed == 0 else f"{failed} of {len(plan.rows)} items failed",
        )
        store.commit()
        return BatchResult(
            plan=plan,
            run_id=run_id,
            status=status,
            iteration_ids=tuple(iteration_ids),
            completed=completed,
            failed=failed,
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
        rows: list[PlanRow] = []
        for item, prompt, key in zip(selected, prompts, keys, strict=True):
            existing = found.get(key)
            action, reason = _classify(existing, spec.max_retries)
            rows.append(PlanRow(item, key, prompt, action, reason, existing))
        return _Prepared(
            playlist, reference, template, provider, profile_id, BatchPlan(tuple(rows))
        )
