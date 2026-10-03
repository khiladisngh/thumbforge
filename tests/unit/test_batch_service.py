"""`BatchService` against the real FakeProvider, real SQLite and the real final render (P7.1).

What is under test is the run a playlist produces and what a second run does with it, so nothing
in the pipeline is faked except where a test needs a provider to count calls, overlap or fail on
demand: those use a thin wrapper around the real `FakeProvider` that still raises the real errors.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

import pytest
from sqlalchemy import func, select
from tenacity import wait_none

from thumbforge.core.enums import RunKind, RunStatus
from thumbforge.core.errors import AssetError, ExitCode, NotFoundError, TemplateError, UsageError
from thumbforge.core.models import (
    ChannelMeta,
    ComplianceReport,
    PlaylistItemMeta,
    PlaylistMeta,
    VideoMeta,
)
from thumbforge.core.services import hero
from thumbforge.core.services.batch import (
    BatchService,
    BatchSpec,
    PlanAction,
    idempotency_key,
)
from thumbforge.core.services.hero import HeroService, NullProgress, RunSpec
from thumbforge.imaging.finalize import render_final
from thumbforge.providers import registry as real_registry
from thumbforge.providers.fake import FAIL_PERMANENT, FakeProvider
from thumbforge.settings import OutputSettings
from thumbforge.storage.assets import AssetStore
from thumbforge.storage.db import get_engine, init_db, session_factory
from thumbforge.storage.models import Iteration, Run
from thumbforge.storage.repositories import Repositories
from thumbforge.storage.runs import RunRepository
from thumbforge.templates.loader import PromptRenderer, import_template, sync_builtins

if TYPE_CHECKING:
    from collections.abc import Collection, Iterator, Mapping

    from sqlalchemy.orm import Session

    from thumbforge.core.json import JsonValue
    from thumbforge.core.layout import LayoutSpec
    from thumbforge.core.providers import (
        GenerationRequest,
        GenerationResult,
        HealthReport,
        ProviderCapabilities,
        ProviderInfo,
    )
    from thumbforge.core.services.hero import Finalize, ProviderRegistry

HERO_VIDEO = "heroVideo01"
PLAYLIST = "PLseries0001"
TEMPLATES = Path(__file__).parent.parent / "fixtures" / "templates"
#: Every part's prompt carries its number; the fail template adds a marker for the parts named.
PROMPT = "Part {{ part_number }}: {{ video.title }}"


def _fail_prompt(*parts: int) -> str:
    return (
        PROMPT
        + "{% if part_number in ("
        + ", ".join(map(str, parts))
        + ",) %} "
        + FAIL_PERMANENT
        + "{% endif %}"
    )


@dataclass
class Env:
    """A migrated database with the built-in templates and one stored hero video."""

    session: Session
    repos: Repositories
    runs: RunRepository
    assets: AssetStore
    logs_dir: Path
    tmp_path: Path


@pytest.fixture
def env(tmp_path: Path) -> Iterator[Env]:
    data_dir = tmp_path / "data"
    db_file = data_dir / "thumbforge.sqlite3"
    init_db(db_file)
    engine = get_engine(db_file)
    factory = session_factory(engine)
    session = factory()
    repos = Repositories(session)
    sync_builtins(repos.templates)
    channel = _channel()
    repos.store_video(
        VideoMeta(
            youtube_id=HERO_VIDEO,
            title="The Hero Episode",
            url=f"https://www.youtube.com/watch?v={HERO_VIDEO}",
            channel_id=channel.youtube_id,
        ),
        channel,
    )
    session.commit()
    assets = AssetStore(data_dir, factory)
    yield Env(session, repos, RunRepository(session, assets), assets, tmp_path / "logs", tmp_path)
    session.close()
    engine.dispose()


def _channel() -> ChannelMeta:
    return ChannelMeta(youtube_id="UC" + "o" * 22, title="Owner", url="https://yt/owner")


def _store_playlist(env: Env, count: int) -> list[str]:
    """Store a playlist of `count` videos whose part numbers are their positions."""
    channel = _channel()
    items = tuple(
        PlaylistItemMeta(
            video=VideoMeta(
                youtube_id=f"video{number:06d}",
                title=f"Episode {number}",
                url=f"https://www.youtube.com/watch?v=video{number:06d}",
                channel_id=channel.youtube_id,
            ),
            position=number,
        )
        for number in range(1, count + 1)
    )
    env.repos.store_playlist(
        PlaylistMeta(
            youtube_id=PLAYLIST,
            title="The Series",
            url=f"https://www.youtube.com/playlist?list={PLAYLIST}",
            channel_id=channel.youtube_id,
            items=items,
        ),
        channel,
    )
    env.session.commit()
    return [item.video.youtube_id for item in items]


def _finalizer(output: OutputSettings) -> Finalize:
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


class _Parts:
    """The real final render, remembering which part it was asked to draw."""

    def __init__(self) -> None:
        self.seen: list[tuple[str, int | None]] = []
        self._inner = _finalizer(OutputSettings())

    def __call__(
        self,
        raw: Path,
        layout: LayoutSpec,
        *,
        title: str,
        part_number: int | None,
        part_label: str | None,
    ) -> tuple[bytes, ComplianceReport]:
        self.seen.append((title, part_number))
        return self._inner(raw, layout, title=title, part_number=part_number, part_label=part_label)


class _Completions:
    """A progress sink that records every outcome and signals once `target` have completed."""

    def __init__(self, target: int) -> None:
        self.target = target
        self.reached = asyncio.Event()
        self.finished: list[tuple[int, RunStatus, str | None]] = []

    def run_started(self, run_id: str, total: int) -> None:
        pass

    def iteration_finished(
        self, run_id: str, ordinal: int, status: RunStatus, error: str | None
    ) -> None:
        self.finished.append((ordinal, status, error))
        if sum(1 for _, seen, _ in self.finished if seen is RunStatus.COMPLETED) >= self.target:
            self.reached.set()


class _OneProvider:
    """A registry that always hands back the provider it was given."""

    def __init__(self, provider: _Probe) -> None:
        self._provider = provider

    def get(self, key: str, config: Mapping[str, JsonValue] | None = None) -> _Probe:
        return self._provider


class _Probe:
    """The real `FakeProvider` plus a record of how it was called, and optional misbehaviour."""

    key: ClassVar[str] = "fake"

    def __init__(
        self,
        *,
        max_concurrency: int | None = None,
        supports_reference_image: bool = True,
        fail_once: Collection[str] = (),
        explode: bool = False,
        block_on_call: int | None = None,
    ) -> None:
        self._inner = FakeProvider()
        #: The call that never returns until the batch is interrupted; `blocked` says it began.
        self.block_on_call = block_on_call
        self.blocked = asyncio.Event()
        self._max_concurrency = max_concurrency
        self._supports_reference_image = supports_reference_image
        self._fail_once = set(fail_once)
        self._explode = explode
        self.in_flight = 0
        self.peak = 0
        self.calls = 0
        self.prompts: Counter[str] = Counter()

    @property
    def capabilities(self) -> ProviderCapabilities:
        update: dict[str, object] = {"supports_reference_image": self._supports_reference_image}
        if self._max_concurrency is not None:
            update["max_concurrency"] = self._max_concurrency
        return self._inner.capabilities.model_copy(update=update)

    async def info(self) -> ProviderInfo:
        return await self._inner.info()

    async def healthcheck(self) -> HealthReport:
        return await self._inner.healthcheck()

    async def generate(self, request: GenerationRequest, *, workdir: Path) -> GenerationResult:
        self.calls += 1
        self.prompts[request.prompt] += 1
        self.in_flight += 1
        self.peak = max(self.peak, self.in_flight)
        try:
            if self.calls == self.block_on_call:
                self.blocked.set()
                await asyncio.Event().wait()
            if self._explode:
                msg = "provider blew up"
                raise RuntimeError(msg)
            for title in tuple(self._fail_once):
                if title in request.prompt:
                    self._fail_once.discard(title)
                    request = request.model_copy(
                        update={"prompt": f"{request.prompt} {FAIL_PERMANENT}"}
                    )
            return await self._inner.generate(request, workdir=workdir)
        finally:
            self.in_flight -= 1


def _template(env: Env, name: str, prompt: str) -> str:
    """Import a template called `name` whose prompt is `prompt`; return its name."""
    directory = env.tmp_path / "templates"
    directory.mkdir(exist_ok=True)
    layout = (TEMPLATES / "valid.toml").read_text(encoding="utf-8")
    toml = directory / f"{name}.toml"
    toml.write_text(layout.replace('name = "bold-title"', f'name = "{name}"'), encoding="utf-8")
    (directory / f"{name}.j2").write_text(prompt, encoding="utf-8")
    import_template(env.repos.templates, toml)
    return name


async def _hero(env: Env, n: int = 1) -> str:
    """A real hero run for the hero video with its first iteration picked; return the run id."""
    service = HeroService(
        env.runs,
        real_registry,
        PromptRenderer(env.repos.templates),
        _finalizer(OutputSettings()),
        logs_dir=env.logs_dir,
    )
    result = await service.generate(
        RunSpec(video_id=HERO_VIDEO, template_ref="bold-title", provider_key="fake", n=n),
        progress=NullProgress(),
    )
    env.runs.pick(result.run_id, 1)
    env.session.commit()
    return result.run_id


def _service(
    env: Env,
    *,
    registry: ProviderRegistry = real_registry,
    finalize: Finalize | None = None,
    **options: Any,
) -> BatchService:
    return BatchService(
        env.runs,
        registry,
        PromptRenderer(env.repos.templates),
        finalize or _finalizer(OutputSettings()),
        logs_dir=env.logs_dir,
        **options,
    )


def _spec(hero_id: str, **overrides: Any) -> BatchSpec:
    base: dict[str, object] = {
        "playlist_id": PLAYLIST,
        "hero": hero_id,
        "template_ref": "series",
        "provider_key": "fake",
    }
    return BatchSpec(**{**base, **overrides})  # type: ignore[arg-type]


def _iterations(env: Env, run_id: str) -> list[Iteration]:
    return sorted(env.runs.get(run_id).iterations, key=lambda item: item.ordinal)


def _count(env: Env, model: type[Run] | type[Iteration]) -> int:
    return env.session.scalar(select(func.count()).select_from(model)) or 0


# --- one run, one item per video ---------------------------------------------------------


async def test_a_playlist_of_five_makes_one_batch_run_with_one_iteration_per_video(
    env: Env,
) -> None:
    youtube_ids = _store_playlist(env, 5)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    parts = _Parts()

    result = await _service(env, finalize=parts).run(_spec(hero_id), progress=NullProgress())

    assert result.exit_code is ExitCode.OK
    assert (result.status, result.completed, result.failed) == (RunStatus.COMPLETED, 5, 0)
    assert result.run_id is not None
    run = env.runs.get(result.run_id)
    assert run.kind is RunKind.BATCH
    assert run.status is RunStatus.COMPLETED
    assert run.playlist is not None
    assert run.playlist.youtube_id == PLAYLIST
    assert run.video_id is None
    assert run.parent_run_id == hero_id
    hero_iteration = env.runs.get(hero_id).iterations[0]
    assert hero_iteration.final_asset is not None
    assert run.reference_asset_id == hero_iteration.final_asset.id

    iterations = _iterations(env, result.run_id)
    assert [item.ordinal for item in iterations] == [1, 2, 3, 4, 5]
    assert [item.video.youtube_id for item in iterations if item.video] == youtube_ids
    assert len({item.idempotency_key for item in iterations}) == 5
    hero_final = env.assets.path_for(hero_iteration.final_asset)
    for item in iterations:
        assert item.status is RunStatus.COMPLETED
        assert item.raw_asset is not None
        assert item.final_asset is not None
        assert item.final_asset.compliant is True
        assert f"Part {item.ordinal}: Episode {item.ordinal}" == item.prompt_text
        sent = json.loads(item.provider_request_json)["reference_images"]
        assert [Path(path) for path in sent] == [hero_final]
    assert sorted(parts.seen) == [(f"Episode {n}", n) for n in range(1, 6)]
    assert result.reference_ignored is False


async def test_the_raw_reference_is_used_when_asked_for(env: Env) -> None:
    _store_playlist(env, 2)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)

    result = await _service(env).run(_spec(hero_id, reference="raw"), progress=NullProgress())

    assert result.run_id is not None
    hero_iteration = env.runs.get(hero_id).iterations[0]
    assert hero_iteration.raw_asset is not None
    assert env.runs.get(result.run_id).reference_asset_id == hero_iteration.raw_asset.id
    sent = json.loads(_iterations(env, result.run_id)[0].provider_request_json)["reference_images"]
    assert [Path(path) for path in sent] == [env.assets.path_for(hero_iteration.raw_asset)]


async def test_a_provider_that_cannot_take_a_reference_goes_prompt_only_and_says_so(
    env: Env,
) -> None:
    _store_playlist(env, 2)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe(supports_reference_image=False)

    result = await _service(env, registry=_OneProvider(probe)).run(
        _spec(hero_id), progress=NullProgress()
    )

    assert result.reference_ignored is True
    assert result.run_id is not None
    for item in _iterations(env, result.run_id):
        assert json.loads(item.provider_request_json)["reference_images"] == []


# --- idempotency -------------------------------------------------------------------------


async def test_running_the_same_batch_again_skips_everything_and_calls_no_provider(
    env: Env,
) -> None:
    _store_playlist(env, 5)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe()
    service = _service(env, registry=_OneProvider(probe))

    first = await service.run(_spec(hero_id), progress=NullProgress())
    assert probe.calls == 5
    second = await service.run(_spec(hero_id), progress=NullProgress())

    assert probe.calls == 5
    assert second.exit_code is ExitCode.OK
    assert (second.completed, second.failed) == (5, 0)
    assert second.iteration_ids == ()
    assert [row.action for row in second.plan.rows] == [PlanAction.SKIP] * 5
    assert {row.reason for row in second.plan.rows} == {"completed"}
    assert second.run_id is not None
    assert second.run_id != first.run_id
    assert env.runs.get(second.run_id).status is RunStatus.COMPLETED
    assert _count(env, Iteration) == 6  # 5 batch + 1 hero; nothing new


async def test_a_new_playlist_item_is_the_only_thing_a_rerun_generates(env: Env) -> None:
    _store_playlist(env, 3)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe()
    service = _service(env, registry=_OneProvider(probe))
    await service.run(_spec(hero_id), progress=NullProgress())

    _store_playlist(env, 4)
    result = await service.run(_spec(hero_id), progress=NullProgress())

    assert probe.calls == 4
    assert [row.action for row in result.plan.rows] == [PlanAction.SKIP] * 3 + [PlanAction.CREATE]
    assert (result.completed, result.failed) == (4, 0)


async def test_a_failed_item_is_retried_in_place_and_completes_without_a_new_iteration(
    env: Env,
) -> None:
    _store_playlist(env, 3)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe(fail_once={"Episode 2"})
    service = _service(env, registry=_OneProvider(probe))

    first = await service.run(_spec(hero_id), progress=NullProgress())
    assert (first.completed, first.failed) == (2, 1)
    assert first.run_id is not None
    failed = _iterations(env, first.run_id)[1]
    assert failed.status is RunStatus.FAILED
    assert json.loads(failed.provider_response_json)["attempts"] == 1

    second = await service.run(_spec(hero_id), progress=NullProgress())

    assert [row.action for row in second.plan.rows] == [
        PlanAction.SKIP,
        PlanAction.RETRY,
        PlanAction.SKIP,
    ]
    assert probe.calls == 4  # three first time, one retry
    assert second.exit_code is ExitCode.OK
    assert second.iteration_ids == (failed.id,)
    env.session.refresh(failed)
    assert failed.status is RunStatus.COMPLETED
    assert failed.final_asset is not None
    assert failed.error_text is None
    assert json.loads(failed.provider_response_json)["attempts"] == 2
    assert _count(env, Iteration) == 4


async def test_a_failed_item_is_retried_only_while_it_has_tries_left(env: Env) -> None:
    _store_playlist(env, 3)
    _template(env, "series-fail", _fail_prompt(2))
    hero_id = await _hero(env)
    probe = _Probe()
    service = _service(env, registry=_OneProvider(probe))
    spec = _spec(hero_id, template_ref="series-fail", max_retries=2)

    await service.run(spec, progress=NullProgress())  # 3 calls; part 2 has used 1 try
    second = await service.run(spec, progress=NullProgress())  # retry: 1 call, 2 tries used
    third = await service.run(spec, progress=NullProgress())  # nothing left: no call

    assert probe.calls == 4
    assert [row.action for row in second.plan.rows] == [
        PlanAction.SKIP,
        PlanAction.RETRY,
        PlanAction.SKIP,
    ]
    assert [row.action for row in third.plan.rows] == [PlanAction.SKIP] * 3
    assert "2 of 2 tries used" in third.plan.rows[1].reason
    assert (third.completed, third.failed) == (2, 1)  # the exhausted item still counts failed
    assert third.exit_code is ExitCode.PARTIAL
    assert third.iteration_ids == ()


async def test_a_changed_reference_is_a_different_key_and_generates_again(env: Env) -> None:
    _store_playlist(env, 2)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe()
    service = _service(env, registry=_OneProvider(probe))

    await service.run(_spec(hero_id), progress=NullProgress())
    result = await service.run(_spec(hero_id, reference="raw"), progress=NullProgress())

    assert probe.calls == 4
    assert [row.action for row in result.plan.rows] == [PlanAction.CREATE] * 2


async def test_the_key_is_plan_section_6_s_sha256_over_its_parts(env: Env) -> None:
    _template(env, "series", PROMPT)
    template = PromptRenderer(env.repos.templates).resolve("series")

    key = idempotency_key(template, "PROFILE", "yt0", 3, "the prompt", None, "refsha")

    material = template.spec_hash + "PROFILE" + "yt0" + "3" + "the prompt" + "" + "refsha"
    assert key == hashlib.sha256(material.encode()).hexdigest()[:32]
    assert len(key) == 32
    assert key != idempotency_key(template, "PROFILE", "yt0", 4, "the prompt", None, "refsha")
    assert key != idempotency_key(template, "PROFILE", "yt0", 3, "the prompt", None, "other")
    assert key != idempotency_key(template, "PROFILE", "yt0", 3, "the prompt", 7, "refsha")
    assert key != idempotency_key(template, "PROFILE", "yt0", None, "the prompt", None, "refsha")


# --- --only and --max-images -------------------------------------------------------------


async def test_only_selects_the_named_parts(env: Env) -> None:
    _store_playlist(env, 5)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe()

    result = await _service(env, registry=_OneProvider(probe)).run(
        _spec(hero_id, only=frozenset({2, 4})), progress=NullProgress()
    )

    assert probe.calls == 2
    assert result.run_id is not None
    assert [item.ordinal for item in _iterations(env, result.run_id)] == [2, 4]
    assert [row.item.part_number for row in result.plan.rows] == [2, 4]


async def test_a_part_cleared_by_renumber_is_left_out_unless_listed_by_position(env: Env) -> None:
    ids = _store_playlist(env, 5)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    playlist = env.repos.playlists.resolve(PLAYLIST)
    env.repos.playlists.renumber(playlist, skip_ids=[ids[4]])  # the trailer: no part number
    env.session.commit()
    service = _service(env)

    default = await service.plan(_spec(hero_id))
    explicit = await service.plan(_spec(hero_id, only=frozenset({5})))

    assert [row.item.position for row in default.rows] == [1, 2, 3, 4]
    assert [row.item.position for row in explicit.rows] == [5]
    assert explicit.rows[0].item.part_number is None


async def test_only_that_matches_nothing_is_a_usage_error_and_writes_nothing(env: Env) -> None:
    _store_playlist(env, 3)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)

    with pytest.raises(UsageError):
        await _service(env).run(_spec(hero_id, only=frozenset({9})), progress=NullProgress())

    assert _count(env, Run) == 1  # the hero


async def test_max_images_below_the_work_aborts_before_any_provider_call_or_row(env: Env) -> None:
    _store_playlist(env, 12)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe()

    with pytest.raises(UsageError, match="12 images"):
        await _service(env, registry=_OneProvider(probe)).run(
            _spec(hero_id, max_images=5), progress=NullProgress()
        )

    assert probe.calls == 0
    assert _count(env, Run) == 1
    assert _count(env, Iteration) == 1


async def test_max_images_equal_to_the_work_runs_and_skips_do_not_count_against_it(
    env: Env,
) -> None:
    _store_playlist(env, 4)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    service = _service(env)

    first = await service.run(_spec(hero_id, max_images=4), progress=NullProgress())
    again = await service.run(_spec(hero_id, max_images=0), progress=NullProgress())

    assert (first.completed, again.completed) == (4, 4)
    assert again.iteration_ids == ()


# --- --dry-run ---------------------------------------------------------------------------


async def test_dry_run_returns_the_plan_and_makes_no_provider_call_or_run(env: Env) -> None:
    _store_playlist(env, 5)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe()

    result = await _service(env, registry=_OneProvider(probe)).run(
        _spec(hero_id, dry_run=True, max_images=1), progress=NullProgress()
    )

    assert probe.calls == 0
    assert result.run_id is None
    assert result.status is None
    assert result.exit_code is ExitCode.OK
    assert [row.action for row in result.plan.rows] == [PlanAction.CREATE] * 5
    assert [row.item.part_number for row in result.plan.rows] == [1, 2, 3, 4, 5]
    assert [row.prompt for row in result.plan.rows][2] == "Part 3: Episode 3"
    assert len({row.key for row in result.plan.rows}) == 5
    assert _count(env, Run) == 1
    assert _count(env, Iteration) == 1


async def test_dry_run_after_a_batch_plans_the_skips_and_matches_the_real_keys(env: Env) -> None:
    _store_playlist(env, 3)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    service = _service(env)
    done = await service.run(_spec(hero_id), progress=NullProgress())
    assert done.run_id is not None

    plan = await service.plan(_spec(hero_id))

    assert [row.action for row in plan.rows] == [PlanAction.SKIP] * 3
    assert [row.key for row in plan.rows] == [
        item.idempotency_key for item in _iterations(env, done.run_id)
    ]


# --- the semaphore -----------------------------------------------------------------------


@pytest.mark.parametrize(("concurrency", "expected_peak"), [(1, 1), (3, 3)])
async def test_provider_calls_never_exceed_the_requested_concurrency(
    env: Env, concurrency: int, expected_peak: int
) -> None:
    _store_playlist(env, 6)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe()

    await _service(env, registry=_OneProvider(probe)).run(
        _spec(hero_id, concurrency=concurrency, provider_params={"delay_ms": 100}),
        progress=NullProgress(),
    )

    assert probe.peak == expected_peak


async def test_the_providers_own_limit_caps_the_requested_concurrency(env: Env) -> None:
    _store_playlist(env, 6)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe(max_concurrency=2)

    await _service(env, registry=_OneProvider(probe)).run(
        _spec(hero_id, concurrency=5, provider_params={"delay_ms": 100}), progress=NullProgress()
    )

    assert probe.peak == 2


# --- failures ----------------------------------------------------------------------------


async def test_failed_items_do_not_abort_the_others_and_the_run_is_failed_with_exit_6(
    env: Env,
) -> None:
    _store_playlist(env, 5)
    _template(env, "series-fail", _fail_prompt(2, 4))
    hero_id = await _hero(env)

    result = await _service(env).run(
        _spec(hero_id, template_ref="series-fail"), progress=NullProgress()
    )

    assert result.exit_code is ExitCode.PARTIAL
    assert (result.status, result.completed, result.failed) == (RunStatus.FAILED, 3, 2)
    assert result.run_id is not None
    run = env.runs.get(result.run_id)
    assert run.status is RunStatus.FAILED
    assert run.error_text == "2 of 5 items failed"
    assert [item.status for item in _iterations(env, result.run_id)] == [
        RunStatus.COMPLETED,
        RunStatus.FAILED,
        RunStatus.COMPLETED,
        RunStatus.FAILED,
        RunStatus.COMPLETED,
    ]
    failed = _iterations(env, result.run_id)[1]
    assert (failed.error_text or "").startswith("provider_permanent:")
    assert failed.final_asset_id is None


async def test_a_transient_failure_is_retried_three_times_then_only_that_item_fails(
    env: Env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(hero, "_RETRY_WAIT", wait_none())
    _store_playlist(env, 3)
    _template(
        env, "series-flaky", PROMPT + "{% if part_number == 2 %} [[FAIL_TRANSIENT]]{% endif %}"
    )
    hero_id = await _hero(env)

    result = await _service(env).run(
        _spec(hero_id, template_ref="series-flaky"), progress=NullProgress()
    )

    assert (result.completed, result.failed) == (2, 1)
    assert result.run_id is not None
    flaky = _iterations(env, result.run_id)[1]
    assert flaky.status is RunStatus.FAILED
    assert json.loads(flaky.provider_response_json)["attempts"] == 3
    assert (flaky.error_text or "").startswith("provider_transient:")


async def test_when_every_item_fails_the_exit_code_is_4(env: Env) -> None:
    _store_playlist(env, 3)
    _template(env, "series-fail", _fail_prompt(1, 2, 3))
    hero_id = await _hero(env)

    result = await _service(env).run(
        _spec(hero_id, template_ref="series-fail"), progress=NullProgress()
    )

    assert (result.completed, result.failed) == (0, 3)
    assert result.exit_code is ExitCode.PROVIDER


async def test_a_non_compliant_final_is_an_ordinary_failure_not_exit_5(env: Env) -> None:
    _store_playlist(env, 2)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)

    result = await _service(env, finalize=_finalizer(OutputSettings(max_bytes=1_000))).run(
        _spec(hero_id), progress=NullProgress()
    )

    assert (result.completed, result.failed) == (0, 2)
    assert result.exit_code is ExitCode.PROVIDER
    assert result.run_id is not None
    for item in _iterations(env, result.run_id):
        assert item.final_asset is not None
        assert item.final_asset.compliant is False
        report = ComplianceReport.model_validate_json(item.final_asset.compliance_report_json or "")
        assert not report.ok
        assert (item.error_text or "").startswith("not compliant:")


# --- nothing is created for a request that cannot run ------------------------------------


async def test_an_unrunnable_request_raises_before_any_batch_row_exists(env: Env) -> None:
    _store_playlist(env, 2)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    unpicked = (
        await HeroService(
            env.runs,
            real_registry,
            PromptRenderer(env.repos.templates),
            _finalizer(OutputSettings()),
            logs_dir=env.logs_dir,
        ).generate(
            RunSpec(video_id=HERO_VIDEO, template_ref="bold-title", provider_key="fake", n=1),
            progress=NullProgress(),
        )
    ).run_id
    cases: list[tuple[dict[str, Any], type[Exception]]] = [
        ({"playlist_id": "nope"}, NotFoundError),
        ({"hero": "nope"}, NotFoundError),
        ({"hero": unpicked}, UsageError),
        ({"template_ref": "nope"}, NotFoundError),
        ({"provider_key": "nope"}, NotFoundError),
    ]

    for overrides, error in cases:
        with pytest.raises(error):
            await _service(env).run(_spec(hero_id, **overrides), progress=NullProgress())

    assert _count(env, Run) == 2  # the two hero runs
    assert _count(env, Iteration) == 2


async def test_a_reference_file_that_has_gone_missing_is_an_asset_error(env: Env) -> None:
    _store_playlist(env, 2)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    picked = env.runs.get(hero_id).iterations[0]
    assert picked.final_asset is not None
    env.assets.path_for(picked.final_asset).unlink()

    with pytest.raises(AssetError):
        await _service(env).run(_spec(hero_id), progress=NullProgress())

    assert _count(env, Run) == 1


async def test_an_unexpected_error_leaves_the_run_failed_not_running(env: Env) -> None:
    _store_playlist(env, 2)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)

    with pytest.raises(ExceptionGroup):
        await _service(env, registry=_OneProvider(_Probe(explode=True))).run(
            _spec(hero_id), progress=NullProgress()
        )

    run = env.session.scalars(select(Run).where(Run.kind == RunKind.BATCH)).one()
    assert run.status is RunStatus.FAILED
    assert "RuntimeError" in (run.error_text or "")
    assert run.finished_at


async def test_a_prompt_that_renders_empty_is_a_template_error_before_any_row(env: Env) -> None:
    _store_playlist(env, 2)
    _template(env, "series-blank", "{% if part_number == 99 %}x{% endif %}")
    hero_id = await _hero(env)

    with pytest.raises(TemplateError):
        await _service(env).run(
            _spec(hero_id, template_ref="series-blank"), progress=NullProgress()
        )

    assert _count(env, Run) == 1


async def test_an_iteration_running_elsewhere_is_left_alone_and_an_unfinished_one_is_retried(
    env: Env,
) -> None:
    _store_playlist(env, 3)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe()
    service = _service(env, registry=_OneProvider(probe))
    first = await service.run(_spec(hero_id), progress=NullProgress())
    assert first.run_id is not None
    rows = _iterations(env, first.run_id)
    rows[0].status = RunStatus.RUNNING
    rows[1].status = RunStatus.PENDING
    env.session.commit()

    result = await service.run(_spec(hero_id), progress=NullProgress())

    assert [row.action for row in result.plan.rows] == [
        PlanAction.SKIP,
        PlanAction.RETRY,
        PlanAction.SKIP,
    ]
    assert result.plan.rows[0].reason == "running in another run"
    assert result.plan.rows[1].reason == "unfinished (pending)"
    assert probe.calls == 4
    assert (result.completed, result.failed) == (2, 0)  # the running one is neither
    assert result.iteration_ids == (rows[1].id,)


# --- interrupt, resume and cancel (P7.2) -------------------------------------------------


def _batch_run(env: Env) -> Run:
    return env.session.scalars(select(Run).where(Run.kind == RunKind.BATCH)).one()


def _attempts(item: Iteration) -> int:
    return json.loads(item.provider_response_json)["attempts"]


@pytest.mark.parametrize("how", ["event", "task"])
async def test_a_batch_interrupted_after_seven_of_twenty_resumes_with_exactly_thirteen_calls(
    env: Env, how: str
) -> None:
    """The interrupt is `cancel.set()` or the task's own cancellation, which is what Ctrl-C does
    under `asyncio.run`; a real OS signal is the CLI's to forward, so it is not raised here."""
    _store_playlist(env, 20)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe(block_on_call=8)  # the eighth call is in flight when the interrupt comes
    service = _service(env, registry=_OneProvider(probe))
    sink = _Completions(7)
    cancel = asyncio.Event()
    batch = asyncio.create_task(
        service.run(_spec(hero_id, concurrency=1), progress=sink, cancel=cancel)
    )
    async with asyncio.timeout(30):
        await sink.reached.wait()
        await probe.blocked.wait()

    if how == "event":
        cancel.set()
        paused = await batch
        assert paused.status is RunStatus.PAUSED
        assert paused.exit_code is ExitCode.INTERRUPTED
        assert (paused.completed, paused.failed, paused.pending) == (7, 1, 12)
    else:
        batch.cancel()
        with pytest.raises(asyncio.CancelledError):
            await batch

    run = _batch_run(env)
    assert run.status is RunStatus.PAUSED
    rows = _iterations(env, run.id)
    assert [item.status for item in rows[:7]] == [RunStatus.COMPLETED] * 7
    assert rows[7].status is RunStatus.FAILED
    assert rows[7].error_text == "interrupted"
    assert _attempts(rows[7]) == 0  # an interrupted try is not charged against max_retries
    assert {item.status for item in rows[8:]} == {RunStatus.PENDING}
    assert (8, RunStatus.FAILED, "interrupted") in sink.finished
    untouched = {item.id: (item.finished_at, item.updated_at) for item in rows[:7]}

    probe.block_on_call = None
    calls_before = probe.calls
    resumed = await service.resume(run.id, progress=NullProgress())

    assert probe.calls - calls_before == 13
    assert probe.calls == 21
    assert resumed.run_id == run.id
    assert (resumed.status, resumed.completed, resumed.failed) == (RunStatus.COMPLETED, 20, 0)
    assert resumed.exit_code is ExitCode.OK
    assert resumed.iteration_ids == tuple(item.id for item in rows[7:])
    assert env.runs.get(run.id).status is RunStatus.COMPLETED
    assert env.runs.get(run.id).error_text is None
    assert [item.status for item in _iterations(env, run.id)] == [RunStatus.COMPLETED] * 20
    assert _attempts(rows[7]) == 1
    assert {item.id: (item.finished_at, item.updated_at) for item in rows[:7]} == untouched
    assert _count(env, Run) == 2  # the hero and the one batch: resume made no new run
    assert _count(env, Iteration) == 21


async def test_a_running_iteration_older_than_stale_after_is_retried_and_a_fresh_one_is_not(
    env: Env,
) -> None:
    _store_playlist(env, 3)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe()
    service = _service(env, registry=_OneProvider(probe), stale_after_s=900)
    first = await service.run(_spec(hero_id), progress=NullProgress())
    assert first.run_id is not None
    rows = _iterations(env, first.run_id)
    now = datetime.now(UTC)
    for item, age_s in ((rows[0], 1000), (rows[1], 10)):
        item.status = RunStatus.RUNNING
        item.started_at = (now - timedelta(seconds=age_s)).isoformat()
        item.finished_at = None
    env.runs.get(first.run_id).status = RunStatus.RUNNING  # the crashed process never closed it
    env.session.commit()

    plan = await service.plan(_spec(hero_id))

    assert [row.action for row in plan.rows] == [PlanAction.RETRY, PlanAction.SKIP, PlanAction.SKIP]
    assert plan.rows[0].reason.startswith("stale")
    assert plan.rows[1].reason == "running in another run"

    resumed = await service.resume(first.run_id, progress=NullProgress())

    assert probe.calls == 4
    assert resumed.iteration_ids == (rows[0].id,)
    assert rows[0].status is RunStatus.COMPLETED
    assert rows[1].status is RunStatus.RUNNING  # a live process may still own it


async def test_resume_retries_a_failed_item_in_its_own_run_and_leaves_the_rest_untouched(
    env: Env,
) -> None:
    _store_playlist(env, 3)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe(fail_once={"Episode 2"})
    service = _service(env, registry=_OneProvider(probe))
    first = await service.run(_spec(hero_id), progress=NullProgress())
    assert first.run_id is not None
    assert env.runs.get(first.run_id).status is RunStatus.FAILED
    rows = _iterations(env, first.run_id)
    untouched = {rows[0].id: rows[0].updated_at, rows[2].id: rows[2].updated_at}

    resumed = await service.resume(first.run_id, progress=NullProgress())

    assert resumed.run_id == first.run_id
    assert (resumed.status, resumed.completed, resumed.failed) == (RunStatus.COMPLETED, 3, 0)
    assert resumed.exit_code is ExitCode.OK
    assert resumed.iteration_ids == (rows[1].id,)
    run = env.runs.get(first.run_id)
    assert run.status is RunStatus.COMPLETED
    assert run.error_text is None
    assert [item.status for item in _iterations(env, first.run_id)] == [RunStatus.COMPLETED] * 3
    assert probe.calls == 4
    assert _count(env, Run) == 2
    assert _count(env, Iteration) == 4
    assert {rows[0].id: rows[0].updated_at, rows[2].id: rows[2].updated_at} == untouched


async def test_resume_with_every_try_used_calls_no_provider_and_the_run_stays_failed(
    env: Env,
) -> None:
    _store_playlist(env, 3)
    _template(env, "series-fail", _fail_prompt(2))
    hero_id = await _hero(env)
    probe = _Probe()
    service = _service(env, registry=_OneProvider(probe))
    first = await service.run(
        _spec(hero_id, template_ref="series-fail", max_retries=2), progress=NullProgress()
    )
    assert first.run_id is not None

    await service.resume(first.run_id, progress=NullProgress())  # the second and last try
    last = await service.resume(first.run_id, progress=NullProgress())

    assert probe.calls == 4
    assert last.iteration_ids == ()
    assert (last.status, last.completed, last.failed) == (RunStatus.FAILED, 2, 1)
    assert last.exit_code is ExitCode.PARTIAL
    assert env.runs.get(first.run_id).status is RunStatus.FAILED


async def test_resume_may_override_the_concurrency_and_keeps_the_stored_provider_settings(
    env: Env,
) -> None:
    _store_playlist(env, 6)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe()
    service = _service(env, registry=_OneProvider(probe))
    cancel = asyncio.Event()
    cancel.set()
    paused = await service.run(
        _spec(hero_id, concurrency=1, provider_params={"delay_ms": 100}),
        progress=NullProgress(),
        cancel=cancel,
    )
    assert paused.run_id is not None

    await service.resume(paused.run_id, concurrency=3, progress=NullProgress())

    assert probe.peak == 3  # three at once, and `delay_ms` came back from the stored profile


async def test_resume_keeps_the_reference_the_run_started_with_when_the_hero_pick_moves(
    env: Env,
) -> None:
    _store_playlist(env, 3)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env, n=2)
    service = _service(env)
    cancel = asyncio.Event()
    cancel.set()
    paused = await service.run(_spec(hero_id), progress=NullProgress(), cancel=cancel)
    assert paused.run_id is not None
    hero_rows = _iterations(env, hero_id)
    assert hero_rows[0].final_asset is not None
    assert hero_rows[1].final_asset is not None
    assert hero_rows[0].final_asset.sha256 != hero_rows[1].final_asset.sha256
    env.runs.pick(hero_id, 2)
    env.session.commit()

    resumed = await service.resume(paused.run_id, progress=NullProgress())

    assert (resumed.completed, resumed.failed) == (3, 0)
    assert _count(env, Iteration) == 5  # two hero, three batch: no second set of keys
    run = env.runs.get(paused.run_id)
    assert run.reference_asset_id == hero_rows[0].final_asset.id
    expected = [env.assets.path_for(hero_rows[0].final_asset)]
    for item in _iterations(env, paused.run_id):
        sent = json.loads(item.provider_request_json)["reference_images"]
        assert [Path(path) for path in sent] == expected


async def test_an_interrupt_before_anything_starts_pauses_the_run_with_no_provider_call(
    env: Env,
) -> None:
    _store_playlist(env, 3)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    probe = _Probe()
    cancel = asyncio.Event()
    cancel.set()

    paused = await _service(env, registry=_OneProvider(probe)).run(
        _spec(hero_id), progress=NullProgress(), cancel=cancel
    )

    assert probe.calls == 0
    assert (paused.status, paused.completed, paused.failed, paused.pending) == (
        RunStatus.PAUSED,
        0,
        0,
        3,
    )
    assert paused.exit_code is ExitCode.INTERRUPTED
    assert {item.status for item in _iterations(env, paused.run_id or "")} == {RunStatus.PENDING}


async def test_cancel_refuses_a_completed_run(env: Env) -> None:
    _store_playlist(env, 2)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    service = _service(env)
    first = await service.run(_spec(hero_id), progress=NullProgress())
    assert first.run_id is not None

    with pytest.raises(UsageError, match="completed") as refused:
        service.cancel(first.run_id)

    assert refused.value.exit_code is ExitCode.USAGE
    assert env.runs.get(first.run_id).status is RunStatus.COMPLETED


async def test_cancel_marks_a_paused_run_and_its_unfinished_iterations_cancelled(env: Env) -> None:
    _store_playlist(env, 3)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    service = _service(env)
    cancel = asyncio.Event()
    cancel.set()
    paused = await service.run(_spec(hero_id), progress=NullProgress(), cancel=cancel)
    assert paused.run_id is not None

    service.cancel(paused.run_id)
    service.cancel(paused.run_id)  # nothing left to do, nothing to refuse

    run = env.runs.get(paused.run_id)
    assert run.status is RunStatus.CANCELLED
    assert run.finished_at
    assert {item.status for item in _iterations(env, paused.run_id)} == {RunStatus.CANCELLED}
    with pytest.raises(UsageError) as refused:
        await service.resume(paused.run_id, progress=NullProgress())
    assert refused.value.exit_code is ExitCode.USAGE


async def test_cancel_marks_a_running_run_cancelled_and_leaves_finished_iterations_alone(
    env: Env,
) -> None:
    _store_playlist(env, 3)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    service = _service(env)
    first = await service.run(_spec(hero_id), progress=NullProgress())
    assert first.run_id is not None
    rows = _iterations(env, first.run_id)
    rows[2].status = RunStatus.RUNNING
    rows[2].finished_at = None
    env.runs.get(first.run_id).status = RunStatus.RUNNING
    env.session.commit()

    service.cancel(first.run_id)

    assert env.runs.get(first.run_id).status is RunStatus.CANCELLED
    assert [item.status for item in _iterations(env, first.run_id)] == [
        RunStatus.COMPLETED,
        RunStatus.COMPLETED,
        RunStatus.CANCELLED,
    ]


async def test_resume_and_cancel_of_an_unknown_run_are_not_found_exit_3(env: Env) -> None:
    service = _service(env)

    with pytest.raises(NotFoundError) as resume_error:
        await service.resume("nope", progress=NullProgress())
    with pytest.raises(NotFoundError) as cancel_error:
        service.cancel("nope")

    assert resume_error.value.exit_code is ExitCode.NOT_FOUND
    assert cancel_error.value.exit_code is ExitCode.NOT_FOUND


async def test_resume_refuses_a_completed_run_and_a_run_that_is_not_a_batch_with_exit_2(
    env: Env,
) -> None:
    _store_playlist(env, 2)
    _template(env, "series", PROMPT)
    hero_id = await _hero(env)
    service = _service(env)
    first = await service.run(_spec(hero_id), progress=NullProgress())
    assert first.run_id is not None

    for run_id in (first.run_id, hero_id):
        with pytest.raises(UsageError) as refused:
            await service.resume(run_id, progress=NullProgress())
        assert refused.value.exit_code is ExitCode.USAGE
