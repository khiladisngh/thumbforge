"""`HeroService` — generate N hero thumbnails for one video (ROADMAP P6.1).

`IterateService` (P6.3) reuses it: a refinement is a run of the same shape that also carries a
parent run and a reference image, so those ride in `RunSpec` and the machinery stays here.

The CLI contributes argument parsing and rendering; the decisions live here:

- what a hero run is made of (one run, N iterations, one profile snapshot, one prompt),
- how iterations are bounded (a semaphore over the provider call only) and retried,
- how a result becomes stored assets and a compliance verdict,
- how per-iteration outcomes roll up into a run status and an exit code.

Every collaborator arrives as a Protocol declared here, so this module imports no adapter
package (`core is pure`). ORM rows never cross that line either: the store speaks the small
value types below, and the CLI reads the stored rows back to render them, as `fetch` does.

Nothing here logs: the `core is pure` contract forbids `core -> thumbforge.logging`. A
`ProgressSink` is the seam the CLI uses to bind `run_id` and report each iteration.
"""

from __future__ import annotations

import asyncio
import shutil
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Final, Protocol

from tenacity import AsyncRetrying, retry_if_exception, stop_after_attempt, wait_exponential_jitter

from thumbforge.core.enums import RunKind, RunStatus
from thumbforge.core.errors import (
    AssetError,
    ComplianceError,
    ExitCode,
    PartialBatchError,
    ProviderError,
    TemplateError,
    ThumbforgeError,
)
from thumbforge.core.ids import new_id, sha256_bytes
from thumbforge.core.json import JsonPayload, JsonValue, canonical_json
from thumbforge.core.providers import GenerationRequest, GenerationResult

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from pathlib import Path

    from thumbforge.core.layout import LayoutSpec, Template
    from thumbforge.core.models import ChannelMeta, ComplianceReport, VideoMeta
    from thumbforge.core.providers import ImageProvider

#: Provider calls per iteration: the first attempt plus two retries (`PLAN.md` §7.2).
_ATTEMPTS: Final = 3
#: Backoff between provider retries. A module constant so tests can neutralise the clock, as
#: they do for the metadata source.
_RETRY_WAIT: Final = wait_exponential_jitter(initial=2.0, exp_base=2.0, max=60.0, jitter=2.0)


@dataclass(frozen=True, slots=True)
class RunSpec:
    """What the user asked for. `video_id` is a ULID or a YouTube id."""

    video_id: str
    template_ref: str
    provider_key: str
    n: int = 4
    concurrency: int = 1
    seed: int | None = None
    vars: Mapping[str, str] = field(default_factory=dict[str, str])
    out_dir: Path | None = None
    #: The provider's own settings. Handed to the registry and to every request, and
    #: snapshotted into the `provider_profile` row.
    provider_params: Mapping[str, JsonValue] = field(default_factory=dict[str, JsonValue])
    #: What kind of run this is; `iterate` for a refinement of an earlier run.
    kind: RunKind = RunKind.HERO
    #: The run this one refines, and the asset it takes as reference. Both `None` for a hero.
    parent_run_id: str | None = None
    reference: AssetInfo | None = None
    #: Text added after the rendered prompt, on its own paragraph.
    prompt_append: str | None = None


@dataclass(frozen=True, slots=True)
class HeroTarget:
    """A stored video as the service needs it: the row id plus its metadata."""

    row_id: str
    video: VideoMeta
    channel: ChannelMeta | None


@dataclass(frozen=True, slots=True)
class AssetInfo:
    """A stored asset: where it is and what it is."""

    id: str
    sha256: str
    path: Path
    mime: str
    width: int
    height: int
    bytes: int


@dataclass(frozen=True, slots=True)
class IterationDraft:
    """One iteration as created: nothing has run yet."""

    ordinal: int
    idempotency_key: str
    prompt_text: str
    seed: int | None
    #: A batch iteration belongs to its own video and part; a hero run's is the run's video.
    video_id: str | None = None
    part_number: int | None = None
    part_label: str | None = None
    #: Provider calls spent on earlier tries of this iteration (a batch retry).
    prior_attempts: int = 0


@dataclass(frozen=True, slots=True)
class IterationOutcome:
    """How one iteration ended, as the store records it."""

    status: RunStatus
    raw_asset_id: str | None
    final_asset_id: str | None
    error_text: str | None
    provider_request_json: str
    provider_response_json: str
    duration_ms: int | None
    cost_json: str | None


class IterationStore(Protocol):
    """What running one iteration and closing its run needs, shared by hero and batch runs.

    The repository's session must have nothing uncommitted when `put_raw` or `put_final`
    run: the asset store writes through its own connection, and SQLite allows one writer.
    The services therefore commit before every `await` and every asset write.
    """

    def ensure_profile(
        self, name: str, provider_key: str, provider_version: str, params_json: str
    ) -> str:
        """The id of the provider profile called `name`, created on first use."""
        ...

    def mark_iteration_running(self, iteration_id: str) -> None:
        """Move an iteration to `running` and stamp its start."""
        ...

    def finish_iteration(self, iteration_id: str, outcome: IterationOutcome) -> None:
        """Record how an iteration ended."""
        ...

    def finish_run(self, run_id: str, status: RunStatus, error_text: str | None) -> None:
        """Record how a run ended."""
        ...

    def put_raw(self, path: Path) -> AssetInfo:
        """Store a provider's output as a `raw` asset."""
        ...

    def put_final(self, data: bytes, report: ComplianceReport) -> AssetInfo:
        """Store rendered bytes as a `final` asset, with the compliance verdict on its row."""
        ...

    def commit(self) -> None:
        """Make everything written so far durable."""
        ...


class HeroStore(IterationStore, Protocol):
    """The persistence surface a hero run needs, satisfied by `storage.runs.RunRepository`."""

    def resolve_video(self, reference: str) -> HeroTarget:
        """The stored video named by a ULID or YouTube id; `NotFoundError` if unknown."""
        ...

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
        parent_run_id: str | None = None,
        reference_asset_id: str | None = None,
    ) -> list[str]:
        """Insert a `running` run and its `pending` iterations; return the iteration ids."""
        ...


class TemplateRenderer(Protocol):
    """Template lookup and prompt rendering, satisfied by `templates.loader.PromptRenderer`."""

    def resolve(self, ref: str) -> Template:
        """The template `NAME[@VERSION]` names; `NotFoundError` if unknown."""
        ...

    def render(
        self,
        template: Template,
        video: VideoMeta,
        channel: ChannelMeta | None,
        vars: Mapping[str, str],
        *,
        part_number: int | None = None,
        part_label: str | None = None,
    ) -> str:
        """The provider prompt; `TemplateError` for a syntax error or a missing variable."""
        ...


class ProviderRegistry(Protocol):
    """Provider lookup by key, satisfied by `providers.registry`."""

    def get(self, key: str, config: Mapping[str, JsonValue] | None = None) -> ImageProvider:
        """Instantiate the provider registered under `key`; `NotFoundError` if unknown."""
        ...


class Finalize(Protocol):
    """Raw art to final bytes plus their compliance report: `imaging.finalize.render_final`.

    The CLI binds `output` from `[output]` before injecting it.
    """

    def __call__(
        self,
        raw: Path,
        layout: LayoutSpec,
        *,
        title: str,
        part_number: int | None,
        part_label: str | None,
    ) -> tuple[bytes, ComplianceReport]:
        """Render `raw` with `layout` and check the result."""
        ...


class ProgressSink(Protocol):
    """Where the service reports progress; the CLI logs it and a later phase draws it."""

    def run_started(self, run_id: str, total: int) -> None:
        """The run exists and `total` iterations are about to start."""
        ...

    def iteration_finished(
        self, run_id: str, ordinal: int, status: RunStatus, error: str | None
    ) -> None:
        """One iteration reached `status`; `error` is set when it failed."""
        ...


class NullProgress:
    """A `ProgressSink` that ignores everything."""

    def run_started(self, run_id: str, total: int) -> None:
        """Ignore."""

    def iteration_finished(
        self, run_id: str, ordinal: int, status: RunStatus, error: str | None
    ) -> None:
        """Ignore."""


@dataclass(frozen=True, slots=True)
class RunResult:
    """How a run ended. Counts only: the CLI reads the stored rows back to render them.

    `failed` includes `compliance_failed`: an iteration whose final was stored but is not
    compliant is a failed iteration (spec Behaviour 3).
    """

    run_id: str
    status: RunStatus
    iteration_ids: tuple[str, ...]
    completed: int
    failed: int
    compliance_failed: int
    #: A reference was asked for but the provider cannot take one, so the run went prompt-only.
    reference_ignored: bool = False

    @property
    def exit_code(self) -> ExitCode:
        """`0` clean; `5` when every failure is a compliance failure; else `4` when nothing
        completed, else `6`."""
        if self.failed == 0:
            return ExitCode.OK
        if self.failed == self.compliance_failed:
            return ExitCode.COMPLIANCE
        if self.completed == 0:
            return ExitCode.PROVIDER
        return ExitCode.PARTIAL

    def error(self) -> ThumbforgeError | None:
        """The error the CLI raises once it has printed the result, or `None` on success."""
        total = len(self.iteration_ids)
        inspect = f"`thumbforge runs show {self.run_id}` lists each iteration"
        match self.exit_code:
            case ExitCode.OK:
                return None
            case ExitCode.COMPLIANCE:
                return ComplianceError(
                    f"{self.failed} of {total} finals are not YouTube-compliant",
                    hint=f"{inspect} with its violations; adjust [output] or the template",
                )
            case ExitCode.PROVIDER:
                return ProviderError(f"all {total} iterations failed", hint=inspect)
            case _:
                return PartialBatchError(
                    f"{self.completed} of {total} iterations completed, {self.failed} failed",
                    hint=(
                        "the completed iterations are kept; re-run `thumbforge thumb generate` "
                        f"to try again. {inspect}"
                    ),
                    completed=self.completed,
                    failed=self.failed,
                )


@dataclass(slots=True)
class _Attempts:
    """Provider calls made for one iteration, readable after the call raised."""

    count: int = 0


@dataclass(frozen=True, slots=True)
class RunContext:
    """Everything one iteration needs besides its own draft."""

    run_id: str
    target: HeroTarget
    template: Template
    provider_params: Mapping[str, JsonValue]
    provider: ImageProvider
    workdir: Path
    gate: asyncio.Semaphore
    progress: ProgressSink
    #: Reference images sent with every request; empty when there is none or it cannot be used.
    references: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class Done:
    """What one finished iteration contributes to the run roll-up."""

    ordinal: int
    status: RunStatus
    compliance_failure: bool
    final: AssetInfo | None


def _is_retryable(error: BaseException) -> bool:
    """Only a provider error that says a retry could help is retried."""
    return isinstance(error, ProviderError) and error.retryable


async def _generate(
    provider: ImageProvider, request: GenerationRequest, workdir: Path, attempts: _Attempts
) -> GenerationResult:
    """One provider call, retried on transient failures (`PLAN.md` §7.2)."""

    async def call() -> GenerationResult:
        attempts.count += 1
        return await provider.generate(request, workdir=workdir)

    retrying = AsyncRetrying(
        stop=stop_after_attempt(_ATTEMPTS),
        wait=_RETRY_WAIT,
        retry=retry_if_exception(_is_retryable),
        reraise=True,
    )
    return await retrying(call)


def _idempotency_key(
    template: Template,
    profile_id: str,
    youtube_id: str,
    prompt: str,
    seed: int | None,
    ordinal: int,
    reference_sha256: str,
    run_id: str,
) -> str:
    """`PLAN.md` §6's key for a hero or iterate iteration.

    `part_number` is an empty string for both, so it drops out of the concatenation, as does
    `reference_asset.sha256` for a hero run; the ordinal rides in the seed, or is the seed
    when the provider has none. The run id is appended: neither kind is deduplicated or
    resumable, and without it re-issuing a run would collide on `iteration.idempotency_key
    UNIQUE`.
    """
    seed_part = str(ordinal) if seed is None else str(seed)
    material = (
        template.spec_hash
        + profile_id
        + youtube_id
        + prompt
        + seed_part
        + reference_sha256
        + run_id
    )
    return sha256_bytes(material.encode())[:32]


def copy_assets(out_dir: Path, stem: str, files: Sequence[tuple[int, Path]]) -> list[Path]:
    """Copy each `(ordinal, source)` to `out_dir/<stem>-<ordinal><suffix of source>`.

    Copies, never moves. `out_dir` is created on first use, so a call with nothing to copy
    makes nothing. Returns the files written, in the order given.
    """
    written: list[Path] = []
    try:
        for ordinal, source in files:
            out_dir.mkdir(parents=True, exist_ok=True)
            target = out_dir / f"{stem}-{ordinal}{source.suffix}"
            shutil.copyfile(source, target)
            written.append(target)
    except OSError as error:
        msg = f"cannot write to {out_dir}: {error}"
        raise AssetError(msg, hint="check the destination directory is writable") from error
    return written


def _leaf(error: BaseException) -> BaseException:
    """The first real error inside a (possibly nested) exception group."""
    members: tuple[BaseException, ...] = getattr(error, "exceptions", ())
    return _leaf(members[0]) if members else error


def failure_text(error: BaseException) -> str:
    """A short run-level reason for an error that is not an expected failure."""
    leaf = _leaf(error)
    if isinstance(leaf, asyncio.CancelledError | KeyboardInterrupt):
        return "interrupted"
    return f"unexpected error: {type(leaf).__name__}"


async def run_iteration(
    store: IterationStore,
    finalize: Finalize,
    context: RunContext,
    iteration_id: str,
    draft: IterationDraft,
) -> Done:
    """Generate, store, finalize and record one iteration; never raises a `ThumbforgeError`."""
    layout = context.template.layout
    request = GenerationRequest(
        prompt=draft.prompt_text,
        width=layout.canvas.width,
        height=layout.canvas.height,
        reference_images=context.references,
        seed=draft.seed,
        params=dict(context.provider_params),
        idempotency_key=draft.idempotency_key,
    )
    attempts = _Attempts(draft.prior_attempts)
    result: GenerationResult | None = None
    raw: AssetInfo | None = None
    final: AssetInfo | None = None
    compliance_failure = False
    try:
        # The semaphore bounds the provider, the scarce resource; finalizing and storing
        # run outside it so they overlap with the next generation.
        async with context.gate:
            store.mark_iteration_running(iteration_id)
            store.commit()
            result = await _generate(context.provider, request, context.workdir, attempts)
        raw = store.put_raw(result.image_path)
        if result.image_path.parent == context.workdir:
            result.image_path.unlink(missing_ok=True)
        data, report = await asyncio.to_thread(
            finalize,
            raw.path,
            layout,
            title=context.target.video.title,
            part_number=draft.part_number,
            part_label=draft.part_label,
        )
        final = store.put_final(data, report)
        if report.ok:
            status, error_text = RunStatus.COMPLETED, None
        else:
            # Stored so it can be inspected, but it is not a usable thumbnail.
            compliance_failure = True
            status = RunStatus.FAILED
            error_text = "not compliant: " + ", ".join(report.violations)
    except ThumbforgeError as error:
        status, error_text = RunStatus.FAILED, f"{error.code}: {error.message}"

    response: JsonPayload = {"attempts": attempts.count}
    cost_json = None
    duration_ms = None
    if result is not None:
        response |= {
            "provider_key": result.provider_key,
            "provider_version": result.provider_version,
            "model": result.model,
            "seed_used": result.seed_used,
            "raw_response": result.raw_response,
        }
        duration_ms = result.duration_ms
        cost_json = None if result.cost is None else result.cost.model_dump_json()
    store.finish_iteration(
        iteration_id,
        IterationOutcome(
            status=status,
            raw_asset_id=None if raw is None else raw.id,
            final_asset_id=None if final is None else final.id,
            error_text=error_text,
            provider_request_json=request.model_dump_json(),
            provider_response_json=canonical_json(response),
            duration_ms=duration_ms,
            cost_json=cost_json,
        ),
    )
    store.commit()
    context.progress.iteration_finished(context.run_id, draft.ordinal, status, error_text)
    return Done(draft.ordinal, status, compliance_failure, final)


class HeroService:
    """Generate hero thumbnails: one run, N iterations, one provider, one prompt."""

    def __init__(
        self,
        store: HeroStore,
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

    async def generate(self, spec: RunSpec, *, progress: ProgressSink) -> RunResult:
        """Run `spec` to completion and report how it ended.

        Raises before any row is written when the video, template or provider is unknown or
        the prompt does not render. Once the run exists, per-iteration failures are recorded
        and reflected in the result instead of raised.
        """
        store = self._store
        target = store.resolve_video(spec.video_id)
        template = self._renderer.resolve(spec.template_ref)
        provider = self._registry.get(spec.provider_key, spec.provider_params)
        info = await provider.info()
        prompt = self._renderer.render(template, target.video, target.channel, spec.vars)
        if spec.prompt_append:
            prompt = f"{prompt}\n\n{spec.prompt_append}"
        if not prompt.strip():
            # Caught here, not by the request model after the run exists.
            msg = f"template {template.ref} rendered an empty prompt"
            raise TemplateError(msg, hint="check the template's prompt and any --var it uses")

        params_json = canonical_json(dict(spec.provider_params))
        profile_name = f"{info.key}@{info.version}:{sha256_bytes(params_json.encode())[:12]}"
        profile_id = store.ensure_profile(profile_name, info.key, info.version, params_json)

        capabilities = provider.capabilities
        reference_sha256 = "" if spec.reference is None else spec.reference.sha256
        usable_reference = spec.reference is not None and capabilities.supports_reference_image
        run_id = new_id()
        drafts: list[IterationDraft] = []
        for ordinal in range(1, spec.n + 1):
            seed = ((spec.seed or 0) + ordinal - 1) if capabilities.supports_seed else None
            key = _idempotency_key(
                template,
                profile_id,
                target.video.youtube_id,
                prompt,
                seed,
                ordinal,
                reference_sha256,
                run_id,
            )
            drafts.append(IterationDraft(ordinal, key, prompt, seed))

        run_params: JsonPayload = {
            "n": spec.n,
            "concurrency": spec.concurrency,
            "seed": spec.seed,
            "vars": dict(spec.vars),
        }
        if spec.prompt_append:
            run_params["prompt_append"] = spec.prompt_append
        iteration_ids = store.create_run(
            run_id,
            kind=spec.kind,
            template=template,
            profile_id=profile_id,
            video_id=target.row_id,
            params_json=canonical_json(run_params),
            iterations=drafts,
            parent_run_id=spec.parent_run_id,
            reference_asset_id=None if spec.reference is None else spec.reference.id,
        )
        store.commit()
        progress.run_started(run_id, len(drafts))

        workdir = self._logs_dir / run_id
        workdir.mkdir(parents=True, exist_ok=True)
        gate = asyncio.Semaphore(max(1, min(spec.concurrency, capabilities.max_concurrency)))
        references = (spec.reference.path,) if spec.reference and usable_reference else ()
        context = RunContext(
            run_id,
            target,
            template,
            spec.provider_params,
            provider,
            workdir,
            gate,
            progress,
            references,
        )

        try:
            async with asyncio.TaskGroup() as group:
                tasks = [
                    group.create_task(
                        run_iteration(store, self._finalize, context, iteration_id, draft)
                    )
                    for iteration_id, draft in zip(iteration_ids, drafts, strict=True)
                ]
        except BaseException as error:
            # Cancellation, Ctrl-C or a bug: the run must not stay `running` forever.
            # Resuming or pausing it is Phase 7's job.
            store.finish_run(run_id, RunStatus.FAILED, failure_text(error))
            store.commit()
            raise

        done = [task.result() for task in tasks]
        completed = sum(1 for item in done if item.status is RunStatus.COMPLETED)
        failed = len(done) - completed
        compliance_failed = sum(1 for item in done if item.compliance_failure)
        status = RunStatus.COMPLETED if failed == 0 else RunStatus.FAILED
        store.finish_run(
            run_id,
            status,
            None if failed == 0 else f"{failed} of {len(done)} iterations failed",
        )
        store.commit()

        if spec.out_dir is not None:
            self._export(spec.out_dir, target.video.youtube_id, done)
        return RunResult(
            run_id=run_id,
            status=status,
            iteration_ids=tuple(iteration_ids),
            completed=completed,
            failed=failed,
            compliance_failed=compliance_failed,
            reference_ignored=spec.reference is not None and not usable_reference,
        )

    @staticmethod
    def _export(out_dir: Path, youtube_id: str, done: Sequence[Done]) -> None:
        """Copy each completed iteration's final to `out_dir/<youtube_id>-<ordinal>.<ext>`."""
        copy_assets(
            out_dir,
            youtube_id,
            [
                (item.ordinal, item.final.path)
                for item in done
                if item.status is RunStatus.COMPLETED and item.final is not None
            ],
        )
