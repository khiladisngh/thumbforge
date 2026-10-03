"""`IterateService` — refine an earlier run from one of its iterations (ROADMAP P6.3).

An iterate run is a hero run with two extras: a parent run, and the raw image of one of the
parent's iterations as the provider's reference. Everything else (rendering, the provider
semaphore, retries, finalizing, the status roll-up) is `HeroService`, so this module only
decides *what to refine*: which iteration, from which run, with which template and provider.

The store resolves that from stored rows, because `core` may not name ORM models; the service
turns the answer into a `RunSpec` and hands it to the hero machinery.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from thumbforge.core.enums import RunKind
from thumbforge.core.services.hero import RunSpec

if TYPE_CHECKING:
    from collections.abc import Mapping

    from thumbforge.core.json import JsonValue
    from thumbforge.core.services.hero import AssetInfo, HeroService, ProgressSink, RunResult


@dataclass(frozen=True, slots=True)
class IterateSource:
    """What a refinement starts from, as stored."""

    #: The run the child is attached to: the run named, or the run of the iteration named.
    parent_run_id: str
    #: Row id of the parent's video.
    video_id: str
    #: `NAME@VERSION` of the parent's template, so the child renders the same one.
    template_ref: str
    #: The parent's provider and the settings it was snapshotted with.
    provider_key: str
    provider_params: Mapping[str, JsonValue]
    #: The raw asset of the iteration being refined.
    reference: AssetInfo


class IterateStore(Protocol):
    """Where a refinement starts, satisfied by `storage.runs.RunRepository`."""

    def resolve_source(self, ref: str, *, from_picked: bool) -> IterateSource:
        """The source `ref` (a run or an iteration id) names.

        A run yields its picked iteration, or with `from_picked` the nearest pick up its
        parent chain; an iteration id yields that iteration, which must be completed.
        `NotFoundError` for an unknown id, `UsageError` when there is nothing usable to refine.
        """
        ...


class IterateService:
    """Start an `iterate` run from a picked or given iteration."""

    def __init__(self, store: IterateStore, hero: HeroService) -> None:
        """Take the store that resolves the source and the service that runs the child."""
        self._store = store
        self._hero = hero

    async def iterate(
        self,
        ref: str,
        *,
        n: int,
        concurrency: int,
        prompt_append: str | None,
        vars: Mapping[str, str],
        from_picked: bool,
        progress: ProgressSink,
    ) -> RunResult:
        """Run `n` refinements of `ref` and report how they ended.

        Raises before any row is written when `ref` is unknown, has nothing to refine, or the
        prompt does not render. `vars` are the child's own: nothing is inherited from the
        parent, so a template that needs a variable needs it passed again.
        """
        source = self._store.resolve_source(ref, from_picked=from_picked)
        spec = RunSpec(
            video_id=source.video_id,
            template_ref=source.template_ref,
            provider_key=source.provider_key,
            n=n,
            concurrency=concurrency,
            vars=vars,
            provider_params=source.provider_params,
            kind=RunKind.ITERATE,
            parent_run_id=source.parent_run_id,
            reference=source.reference,
            prompt_append=prompt_append,
        )
        return await self._hero.generate(spec, progress=progress)
