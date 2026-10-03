"""`HeroService` against the real FakeProvider, a real SQLite file and the real final render (P6.1).

What is under test is the run it records and the verdict it reaches, so nothing in the
pipeline is faked except where a test needs a provider to misbehave: those use a thin wrapper
around the real `FakeProvider` that still raises the real errors.
"""

from __future__ import annotations

import json
import threading
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

import pytest
from sqlalchemy import func, select
from tenacity import wait_none

from thumbforge.core.enums import AssetKind, RunKind, RunStatus
from thumbforge.core.errors import (
    ComplianceError,
    ExitCode,
    NotFoundError,
    PartialBatchError,
    ProviderError,
    TemplateError,
)
from thumbforge.core.models import ChannelMeta, ComplianceReport, VideoMeta
from thumbforge.core.services import hero
from thumbforge.core.services.hero import HeroService, NullProgress, RunSpec
from thumbforge.imaging.finalize import render_final
from thumbforge.providers import registry as real_registry
from thumbforge.providers.fake import FAIL_PERMANENT, FAIL_TRANSIENT, FakeProvider
from thumbforge.settings import OutputSettings
from thumbforge.storage.assets import AssetStore
from thumbforge.storage.db import get_engine, init_db, session_factory
from thumbforge.storage.models import Asset, Iteration, ProviderProfile, Run
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

VIDEO = "dQw4w9WgXcQ"
TEMPLATES = Path(__file__).parent.parent / "fixtures" / "templates"


@dataclass
class Env:
    """A migrated database with the built-in templates and one stored video."""

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
    channel = ChannelMeta(youtube_id="UC" + "o" * 22, title="Owner", url="https://yt/owner")
    repos.store_video(
        VideoMeta(
            youtube_id=VIDEO,
            title="Never Gonna Give You Up",
            url=f"https://www.youtube.com/watch?v={VIDEO}",
            channel_id=channel.youtube_id,
        ),
        channel,
    )
    session.commit()
    assets = AssetStore(data_dir, factory)
    yield Env(session, repos, RunRepository(session, assets), assets, tmp_path / "logs", tmp_path)
    session.close()
    engine.dispose()


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


def _flip_finalizer() -> Finalize:
    """Real finals that alternate between an impossible byte budget and the default one."""
    strict, lax = _finalizer(OutputSettings(max_bytes=1_000)), _finalizer(OutputSettings())
    lock = threading.Lock()
    calls = 0

    def finalize(
        raw: Path,
        layout: LayoutSpec,
        *,
        title: str,
        part_number: int | None,
        part_label: str | None,
    ) -> tuple[bytes, ComplianceReport]:
        nonlocal calls
        with lock:
            calls += 1
            chosen = strict if calls % 2 == 1 else lax
        return chosen(raw, layout, title=title, part_number=part_number, part_label=part_label)

    return finalize


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
        supports_seed: bool = True,
        fail_seeds: Collection[int] = (),
        explode: bool = False,
    ) -> None:
        self._inner = FakeProvider()
        self._max_concurrency = max_concurrency
        self._supports_seed = supports_seed
        self._fail_seeds = frozenset(fail_seeds)
        self._explode = explode
        self.in_flight = 0
        self.peak = 0
        self.calls: Counter[int | None] = Counter()

    @property
    def capabilities(self) -> ProviderCapabilities:
        update: dict[str, object] = {"supports_seed": self._supports_seed}
        if self._max_concurrency is not None:
            update["max_concurrency"] = self._max_concurrency
        return self._inner.capabilities.model_copy(update=update)

    async def info(self) -> ProviderInfo:
        return await self._inner.info()

    async def healthcheck(self) -> HealthReport:
        return await self._inner.healthcheck()

    async def generate(self, request: GenerationRequest, *, workdir: Path) -> GenerationResult:
        self.calls[request.seed] += 1
        self.in_flight += 1
        self.peak = max(self.peak, self.in_flight)
        try:
            if self._explode:
                msg = "provider blew up"
                raise RuntimeError(msg)
            if request.seed in self._fail_seeds:
                request = request.model_copy(
                    update={"prompt": f"{request.prompt} {FAIL_PERMANENT}"}
                )
            return await self._inner.generate(request, workdir=workdir)
        finally:
            self.in_flight -= 1


class _Events:
    """A progress sink that remembers what it was told."""

    def __init__(self) -> None:
        self.started: list[tuple[str, int]] = []
        self.finished: list[tuple[int, RunStatus]] = []

    def run_started(self, run_id: str, total: int) -> None:
        self.started.append((run_id, total))

    def iteration_finished(
        self, run_id: str, ordinal: int, status: RunStatus, error: str | None
    ) -> None:
        self.finished.append((ordinal, status))


def _service(
    env: Env,
    *,
    registry: ProviderRegistry = real_registry,
    finalize: Finalize | None = None,
) -> HeroService:
    return HeroService(
        env.runs,
        registry,
        PromptRenderer(env.repos.templates),
        finalize or _finalizer(OutputSettings()),
        logs_dir=env.logs_dir,
    )


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


def _failing(env: Env) -> str:
    return _template(env, "failing", "Art for {{ video.title }}. {{ vars.fail }}")


def _spec(template: str = "bold-title", **overrides: Any) -> RunSpec:
    base: dict[str, object] = {
        "video_id": VIDEO,
        "template_ref": template,
        "provider_key": "fake",
        "n": 4,
    }
    return RunSpec(**{**base, **overrides})  # type: ignore[arg-type]


def _iterations(env: Env, run_id: str) -> list[Iteration]:
    return sorted(env.runs.get(run_id).iterations, key=lambda item: item.ordinal)


def _rows(env: Env, model: type[Asset] | type[Run] | type[ProviderProfile]) -> int:
    return env.session.scalar(select(func.count()).select_from(model)) or 0


# --- the happy path ----------------------------------------------------------------------


async def test_four_iterations_complete_with_raw_and_final_assets(env: Env) -> None:
    result = await _service(env).generate(_spec(), progress=NullProgress())

    assert result.exit_code is ExitCode.OK
    assert result.error() is None
    assert (result.status, result.completed, result.failed) == (RunStatus.COMPLETED, 4, 0)

    run = env.runs.get(result.run_id)
    assert (run.kind, run.status) == (RunKind.HERO, RunStatus.COMPLETED)
    assert run.started_at and run.finished_at
    assert run.provider_profile.name.startswith("fake@")
    assert (run.template.name, run.template.version) == ("bold-title", 1)

    iterations = _iterations(env, result.run_id)
    assert [item.ordinal for item in iterations] == [1, 2, 3, 4]
    assert len({item.idempotency_key for item in iterations}) == 4
    for item in iterations:
        assert item.status is RunStatus.COMPLETED
        assert item.raw_asset is not None
        assert item.final_asset is not None
        assert item.raw_asset.kind is AssetKind.RAW
        assert item.final_asset.kind is AssetKind.FINAL
        assert env.assets.verify(item.raw_asset)
        assert env.assets.verify(item.final_asset)
        assert item.final_asset.compliant is True
        report = ComplianceReport.model_validate_json(item.final_asset.compliance_report_json or "")
        assert report.ok
        assert (report.width, report.height) == (1920, 1080)
        response = json.loads(item.provider_response_json)
        assert response["attempts"] == 1
        assert response["provider_key"] == "fake"
        assert json.loads(item.provider_request_json)["idempotency_key"] == item.idempotency_key
        assert item.started_at and item.finished_at and item.duration_ms is not None


async def test_the_prompt_is_rendered_once_for_every_iteration(env: Env) -> None:
    result = await _service(env).generate(_spec(), progress=NullProgress())

    prompts = {item.prompt_text for item in _iterations(env, result.run_id)}
    assert len(prompts) == 1
    assert "Never Gonna Give You Up" in prompts.pop()


async def test_the_provider_scratch_image_does_not_pile_up_in_the_run_logs_dir(env: Env) -> None:
    result = await _service(env).generate(_spec(), progress=NullProgress())

    workdir = env.logs_dir / result.run_id
    assert workdir.is_dir()
    assert list(workdir.glob("*.png")) == []


async def test_progress_reports_the_run_and_every_iteration(env: Env) -> None:
    events = _Events()

    result = await _service(env).generate(_spec(n=3), progress=events)

    assert events.started == [(result.run_id, 3)]
    assert sorted(events.finished) == [
        (1, RunStatus.COMPLETED),
        (2, RunStatus.COMPLETED),
        (3, RunStatus.COMPLETED),
    ]


# --- idempotency keys and assets ---------------------------------------------------------


async def test_reissuing_the_same_spec_makes_new_keys_instead_of_colliding(env: Env) -> None:
    service = _service(env)

    first = await service.generate(_spec(seed=3), progress=NullProgress())
    second = await service.generate(_spec(seed=3), progress=NullProgress())

    keys = {
        item.idempotency_key for run in (first, second) for item in _iterations(env, run.run_id)
    }
    assert len(keys) == 8
    assert _rows(env, Run) == 2
    assert _rows(env, ProviderProfile) == 1  # same provider and params: one snapshot


async def test_identical_bytes_are_stored_once(env: Env) -> None:
    service = _service(env)

    first = await service.generate(_spec(n=3, seed=7), progress=NullProgress())
    second = await service.generate(_spec(n=3, seed=7), progress=NullProgress())

    def ids(run_id: str) -> tuple[list[str | None], list[str | None]]:
        rows = _iterations(env, run_id)
        return [i.raw_asset_id for i in rows], [i.final_asset_id for i in rows]

    assert ids(first.run_id) == ids(second.run_id)
    assert _rows(env, Asset) == 6  # 3 raw + 3 final, not 12


async def test_a_provider_without_seeds_still_gets_distinct_keys(env: Env) -> None:
    probe = _Probe(supports_seed=False)

    result = await _service(env, registry=_OneProvider(probe)).generate(
        _spec(seed=99), progress=NullProgress()
    )

    iterations = _iterations(env, result.run_id)
    assert {item.seed for item in iterations} == {None}
    assert len({item.idempotency_key for item in iterations}) == 4
    # No seed means four identical requests, so the fake draws four identical images.
    assert len({item.raw_asset_id for item in iterations}) == 1


async def test_seeds_count_up_from_the_requested_one(env: Env) -> None:
    result = await _service(env).generate(_spec(seed=40), progress=NullProgress())

    assert [item.seed for item in _iterations(env, result.run_id)] == [40, 41, 42, 43]


# --- the roll-up -------------------------------------------------------------------------


async def test_every_iteration_failing_exits_4_and_stores_nothing(env: Env) -> None:
    template = _failing(env)

    result = await _service(env).generate(
        _spec(template, vars={"fail": FAIL_PERMANENT}), progress=NullProgress()
    )

    assert result.exit_code is ExitCode.PROVIDER
    assert (result.status, result.completed, result.failed) == (RunStatus.FAILED, 0, 4)
    assert isinstance(result.error(), ProviderError)
    assert _rows(env, Asset) == 0
    run = env.runs.get(result.run_id)
    assert run.status is RunStatus.FAILED
    assert run.error_text
    for item in _iterations(env, result.run_id):
        assert item.status is RunStatus.FAILED
        assert (item.error_text or "").startswith("provider_permanent:")
        assert item.raw_asset_id is None
        assert item.final_asset_id is None


async def test_some_iterations_failing_exits_6_and_keeps_the_rest(env: Env) -> None:
    probe = _Probe(fail_seeds={11})

    result = await _service(env, registry=_OneProvider(probe)).generate(
        _spec(seed=10), progress=NullProgress()
    )

    assert result.exit_code is ExitCode.PARTIAL
    assert (result.completed, result.failed) == (3, 1)
    error = result.error()
    assert isinstance(error, PartialBatchError)
    assert (error.completed, error.failed) == (3, 1)
    assert env.runs.get(result.run_id).status is RunStatus.FAILED
    assert [item.status for item in _iterations(env, result.run_id)] == [
        RunStatus.COMPLETED,
        RunStatus.FAILED,
        RunStatus.COMPLETED,
        RunStatus.COMPLETED,
    ]
    assert probe.calls[11] == 1  # a permanent error is attempted once


async def test_a_non_compliant_final_is_stored_and_the_iteration_fails(env: Env) -> None:
    finalize = _finalizer(OutputSettings(max_bytes=1_000))

    result = await _service(env, finalize=finalize).generate(_spec(), progress=NullProgress())

    assert result.exit_code is ExitCode.COMPLIANCE
    assert (result.completed, result.failed, result.compliance_failed) == (0, 4, 4)
    assert isinstance(result.error(), ComplianceError)
    for item in _iterations(env, result.run_id):
        assert item.status is RunStatus.FAILED
        assert item.raw_asset is not None
        assert item.final_asset is not None  # kept, so it can be inspected
        assert item.final_asset.compliant is False
        report = ComplianceReport.model_validate_json(item.final_asset.compliance_report_json or "")
        assert not report.ok
        assert "size" in report.violations
        assert (item.error_text or "").startswith("not compliant:")
        assert "size" in (item.error_text or "")


async def test_when_every_failure_is_a_compliance_failure_exit_5_beats_6(env: Env) -> None:
    result = await _service(env, finalize=_flip_finalizer()).generate(
        _spec(), progress=NullProgress()
    )

    assert (result.completed, result.failed, result.compliance_failed) == (2, 2, 2)
    assert result.exit_code is ExitCode.COMPLIANCE


async def test_a_provider_failure_among_compliance_failures_is_not_exit_5(env: Env) -> None:
    probe = _Probe(fail_seeds={0})

    result = await _service(env, registry=_OneProvider(probe), finalize=_flip_finalizer()).generate(
        _spec(), progress=NullProgress()
    )

    assert (result.completed, result.failed, result.compliance_failed) == (1, 3, 2)
    assert result.exit_code is ExitCode.PARTIAL


# --- retries -----------------------------------------------------------------------------


async def test_transient_errors_are_retried_three_times_then_the_iteration_fails(
    env: Env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(hero, "_RETRY_WAIT", wait_none())
    template = _failing(env)

    result = await _service(env).generate(
        _spec(template, n=2, vars={"fail": FAIL_TRANSIENT}), progress=NullProgress()
    )

    assert result.exit_code is ExitCode.PROVIDER
    for item in _iterations(env, result.run_id):
        assert json.loads(item.provider_response_json)["attempts"] == 3
        assert (item.error_text or "").startswith("provider_transient:")


# --- the semaphore -----------------------------------------------------------------------


@pytest.mark.parametrize(("concurrency", "expected_peak"), [(1, 1), (2, 2), (6, 6)])
async def test_provider_calls_never_exceed_the_requested_concurrency(
    env: Env, concurrency: int, expected_peak: int
) -> None:
    probe = _Probe()

    await _service(env, registry=_OneProvider(probe)).generate(
        _spec(n=6, concurrency=concurrency, provider_params={"delay_ms": 100}),
        progress=NullProgress(),
    )

    assert probe.peak == expected_peak


async def test_the_providers_own_limit_caps_the_requested_concurrency(env: Env) -> None:
    probe = _Probe(max_concurrency=2)

    await _service(env, registry=_OneProvider(probe)).generate(
        _spec(n=6, concurrency=5, provider_params={"delay_ms": 100}), progress=NullProgress()
    )

    assert probe.peak == 2


async def test_concurrency_4_overlaps_the_provider_waits(env: Env) -> None:
    started = time.perf_counter()

    await _service(env).generate(
        _spec(concurrency=4, provider_params={"delay_ms": 500}), progress=NullProgress()
    )

    assert time.perf_counter() - started < 1.5


async def test_concurrency_1_runs_the_provider_waits_back_to_back(env: Env) -> None:
    started = time.perf_counter()

    await _service(env).generate(
        _spec(concurrency=1, provider_params={"delay_ms": 500}), progress=NullProgress()
    )

    assert time.perf_counter() - started > 2.0


# --- --out -------------------------------------------------------------------------------


async def test_out_dir_receives_a_copy_of_every_completed_final(env: Env) -> None:
    out = env.tmp_path / "out"

    result = await _service(env).generate(_spec(out_dir=out), progress=NullProgress())

    assert sorted(path.name for path in out.iterdir()) == [f"{VIDEO}-{n}.jpg" for n in (1, 2, 3, 4)]
    for item in _iterations(env, result.run_id):
        assert item.final_asset is not None
        stored = env.assets.path_for(item.final_asset)
        assert stored.is_file()  # copied, never moved
        assert (out / f"{VIDEO}-{item.ordinal}.jpg").read_bytes() == stored.read_bytes()


async def test_out_dir_gets_nothing_for_non_compliant_finals(env: Env) -> None:
    out = env.tmp_path / "out"

    result = await _service(env, finalize=_finalizer(OutputSettings(max_bytes=1_000))).generate(
        _spec(out_dir=out), progress=NullProgress()
    )

    assert result.completed == 0
    assert not out.exists() or list(out.iterdir()) == []
    assert _rows(env, Asset) > 0  # still inspectable in the store


# --- nothing is created for a request that cannot run ------------------------------------


@pytest.mark.parametrize(
    ("overrides", "error"),
    [
        ({"video_id": "nope"}, NotFoundError),
        ({"provider_key": "nope"}, NotFoundError),
        ({"template_ref": "nope"}, NotFoundError),
        ({"template_ref": "failing"}, TemplateError),  # `vars.fail` is not supplied
        ({"template_ref": "blank", "vars": {"fail": ""}}, TemplateError),  # empty prompt
    ],
)
async def test_an_unrunnable_request_raises_before_any_row_exists(
    env: Env, overrides: dict[str, Any], error: type[Exception]
) -> None:
    _failing(env)
    _template(env, "blank", "{{ vars.fail }}")

    with pytest.raises(error):
        await _service(env).generate(_spec(**overrides), progress=NullProgress())

    assert _rows(env, Run) == 0
    assert _rows(env, Asset) == 0


# --- bugs --------------------------------------------------------------------------------


async def test_an_unexpected_error_leaves_the_run_failed_not_running(env: Env) -> None:
    probe = _Probe(explode=True)

    with pytest.raises(ExceptionGroup):
        await _service(env, registry=_OneProvider(probe)).generate(_spec(), progress=NullProgress())

    run = env.session.scalars(select(Run)).one()
    assert run.status is RunStatus.FAILED
    assert "RuntimeError" in (run.error_text or "")
    assert run.finished_at
