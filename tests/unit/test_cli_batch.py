"""`thumbforge batch` end to end with the real fake provider and a real SQLite database.

Every test starts from a migrated database holding the built-in templates, one stored hero video
and a five-video playlist, drives the real Typer app through `CliRunner`, and reads back what the
command prints, which exit status it returns and what it left in the database (ROADMAP P7.3,
phase-7 spec Behaviour 1-8). The service underneath is covered by `test_batch_service.py`; what
is defended here is the command's contract: arguments, output, exit codes and the interrupt.
"""

from __future__ import annotations

import asyncio
import io
import json
import signal
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

import pytest
from rich.console import Console
from tenacity import wait_none
from typer.testing import CliRunner

from thumbforge.cli._youtube import open_repositories
from thumbforge.cli.app import app
from thumbforge.core.enums import RunStatus
from thumbforge.core.errors import ExitCode
from thumbforge.core.models import ChannelMeta, PlaylistItemMeta, PlaylistMeta, VideoMeta
from thumbforge.core.services import hero
from thumbforge.providers import registry
from thumbforge.providers.fake import FAIL_PERMANENT, FakeProvider

if TYPE_CHECKING:
    from typer.testing import Result

    from thumbforge.core.providers import GenerationRequest, GenerationResult

runner = CliRunner()
TEMPLATES = Path(__file__).parent.parent / "fixtures" / "templates"
HERO_VIDEO = "heroVideo01"
PLAYLIST = "PLseries0001"
EPISODES = 5
#: Wide enough that Rich never wraps a title or an error inside the summary table.
WIDE = {"COLUMNS": "200"}


class _Recording(FakeProvider):
    """The real fake, remembering every request it was handed."""

    key: ClassVar[str] = "recording"
    requests: ClassVar[list[GenerationRequest]] = []

    async def generate(self, request: GenerationRequest, *, workdir: Path) -> GenerationResult:
        self.requests.append(request)
        return await super().generate(request, workdir=workdir)


class _Interrupting(_Recording):
    """The real fake, but the first call it ever gets raises a real SIGINT and never returns."""

    key: ClassVar[str] = "interrupting"
    armed: ClassVar[bool] = True

    async def generate(self, request: GenerationRequest, *, workdir: Path) -> GenerationResult:
        if type(self).armed:
            type(self).armed = False
            self.requests.append(request)
            signal.raise_signal(signal.SIGINT)
            await asyncio.sleep(60)
        return await super().generate(request, workdir=workdir)


@pytest.fixture(autouse=True)
def providers(monkeypatch: pytest.MonkeyPatch) -> type[_Recording]:
    monkeypatch.setitem(registry.BUILTIN, "recording", _Recording)
    monkeypatch.setitem(registry.BUILTIN, "interrupting", _Interrupting)
    monkeypatch.setattr(_Recording, "requests", [])
    monkeypatch.setattr(_Interrupting, "armed", True)
    # A transient failure is retried in-process; without this each retry sleeps for seconds.
    monkeypatch.setattr(hero, "_RETRY_WAIT", wait_none())
    return _Recording


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    directory = tmp_path / "data"
    assert runner.invoke(app, ["--data-dir", str(directory), "db", "init"]).exit_code == 0
    channel = ChannelMeta(youtube_id="UC" + "o" * 22, title="Owner", url="https://yt/owner")
    episodes = tuple(
        PlaylistItemMeta(
            video=VideoMeta(
                youtube_id=f"video{number:06d}",
                title=f"Episode {number}",
                url=f"https://www.youtube.com/watch?v=video{number:06d}",
                channel_id=channel.youtube_id,
            ),
            position=number,
        )
        for number in range(1, EPISODES + 1)
    )
    with open_repositories(directory / "thumbforge.sqlite3") as repos:
        repos.store_video(
            VideoMeta(
                youtube_id=HERO_VIDEO,
                title="The Hero Episode",
                url=f"https://www.youtube.com/watch?v={HERO_VIDEO}",
                channel_id=channel.youtube_id,
            ),
            channel,
        )
        repos.store_playlist(
            PlaylistMeta(
                youtube_id=PLAYLIST,
                title="The Series",
                url=f"https://www.youtube.com/playlist?list={PLAYLIST}",
                channel_id=channel.youtube_id,
                items=episodes,
            ),
            channel,
        )
    return directory


def _run(
    data_dir: Path, *args: str, json_mode: bool = False, env: dict[str, str] | None = None
) -> Result:
    command = ["--data-dir", str(data_dir), *(["--json"] if json_mode else [])]
    return runner.invoke(app, [*command, *args], env={**WIDE, **(env or {})})


def _template(data_dir: Path, tmp_path: Path, name: str, prompt: str) -> str:
    """Import a template called `name` whose prompt is `prompt`; return its name."""
    directory = tmp_path / name
    directory.mkdir()
    layout = (TEMPLATES / "valid.toml").read_text(encoding="utf-8")
    (directory / f"{name}.toml").write_text(
        layout.replace('name = "bold-title"', f'name = "{name}"'), encoding="utf-8"
    )
    (directory / f"{name}.j2").write_text(prompt, encoding="utf-8")
    result = _run(data_dir, "template", "import", str(directory / f"{name}.toml"))
    assert result.exit_code == ExitCode.OK, result.output
    return name


def _failing_on(data_dir: Path, tmp_path: Path, marker: str, *parts: int) -> str:
    """A template whose prompt carries `marker` for the listed parts only."""
    condition = ", ".join(map(str, parts))
    prompt = (
        "Part {{ part_number }}: {{ video.title }}"
        f"{{% if part_number in ({condition},) %}} {marker}{{% endif %}}"
    )
    return _template(data_dir, tmp_path, "series-flaky", prompt)


def _hero(data_dir: Path, *, pick: bool = True) -> dict[str, Any]:
    """A completed two-iteration hero run, the first iteration picked; no provider call is kept."""
    result = _run(
        data_dir,
        "thumb",
        "generate",
        HERO_VIDEO,
        "--provider",
        "recording",
        "--n",
        "2",
        json_mode=True,
    )
    assert result.exit_code == ExitCode.OK, result.output
    payload: dict[str, Any] = json.loads(result.stdout)
    if pick:
        assert _run(data_dir, "thumb", "pick", payload["run"]["id"], "1").exit_code == ExitCode.OK
    _Recording.requests.clear()
    return payload


def _batch(
    data_dir: Path,
    hero_payload: dict[str, Any],
    *args: str,
    template: str = "series-parts",
    provider: str = "recording",
    json_mode: bool = False,
    env: dict[str, str] | None = None,
) -> Result:
    return _run(
        data_dir,
        "batch",
        PLAYLIST,
        "--hero",
        hero_payload["run"]["id"],
        "--template",
        template,
        "--provider",
        provider,
        *args,
        json_mode=json_mode,
        env=env,
    )


def _batch_json(data_dir: Path, hero_payload: dict[str, Any], *args: str, **kwargs: Any) -> Any:
    result = _batch(data_dir, hero_payload, *args, json_mode=True, **kwargs)
    assert result.exit_code == ExitCode.OK, result.output
    return json.loads(result.stdout)


def _asset(hero_payload: dict[str, Any], kind: str) -> dict[str, Any]:
    """The first hero iteration's `final_asset` or `raw_asset`."""
    return hero_payload["iterations"][0][kind]


def _batch_runs(data_dir: Path) -> int:
    with closing(sqlite3.connect(data_dir / "thumbforge.sqlite3")) as connection:
        row = connection.execute("SELECT COUNT(*) FROM run WHERE kind = 'batch'").fetchone()
    return row[0]


def _iteration_count(data_dir: Path) -> int:
    with closing(sqlite3.connect(data_dir / "thumbforge.sqlite3")) as connection:
        row = connection.execute("SELECT COUNT(*) FROM iteration").fetchone()
    return row[0]


def _stored_status(data_dir: Path, run_id: str) -> str:
    shown = _run(data_dir, "runs", "show", run_id, json_mode=True)
    assert shown.exit_code == ExitCode.OK, shown.output
    return json.loads(shown.stdout)["run"]["status"]


# --- the happy path ------------------------------------------------------------------------


def test_batch_over_a_playlist_exits_0_and_the_summary_lists_every_item(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)

    result = _batch(data_dir, hero_payload)

    assert result.exit_code == ExitCode.OK, result.output
    for number in range(1, EPISODES + 1):
        assert f"Episode {number}" in result.stdout
    assert result.stdout.count("✔") == EPISODES
    assert result.stdout.count("completed") >= EPISODES
    assert len(_Recording.requests) == EPISODES
    assert _batch_runs(data_dir) == 1


def test_json_prints_one_summary_object_with_the_run_and_every_item(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)
    final = _asset(hero_payload, "final_asset")

    payload = _batch_json(data_dir, hero_payload)

    assert payload["exit_code"] == 0
    assert payload["run"]["kind"] == "batch"
    assert payload["run"]["status"] == "completed"
    assert payload["run"]["parent_run_id"] == hero_payload["run"]["id"]
    assert payload["run"]["reference_asset"]["id"] == final["id"]
    assert payload["summary"] == {"total": 5, "completed": 5, "failed": 0, "pending": 0}
    items = payload["items"]
    assert [item["part"] for item in items] == [1, 2, 3, 4, 5]
    assert [item["title"] for item in items] == [f"Episode {n}" for n in range(1, 6)]
    assert {item["status"] for item in items} == {"completed"}
    assert {item["action"] for item in items} == {"create"}
    assert all(item["compliant"] is True for item in items)
    assert all(Path(item["final_asset"]).is_file() for item in items)
    # Every provider call was handed the hero's finished thumbnail, and nothing else.
    assert len(_Recording.requests) == EPISODES
    assert all(r.reference_images == (Path(final["path"]),) for r in _Recording.requests)


def test_log_lines_carry_the_batch_run_id(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)

    result = _batch(data_dir, hero_payload, json_mode=True)

    assert result.exit_code == ExitCode.OK, result.output
    run_id = json.loads(result.stdout)["run"]["id"]
    events = [json.loads(line) for line in result.stderr.splitlines() if line.startswith("{")]
    finished = [event for event in events if event.get("event") == "iteration finished"]
    assert len(finished) == EPISODES
    assert {event["run_id"] for event in finished} == {run_id}


def test_running_the_same_command_again_calls_no_provider_and_creates_nothing(
    data_dir: Path,
) -> None:
    hero_payload = _hero(data_dir)
    _batch_json(data_dir, hero_payload)
    iterations = _iteration_count(data_dir)
    _Recording.requests.clear()

    again = _batch_json(data_dir, hero_payload)

    assert _Recording.requests == []
    assert _iteration_count(data_dir) == iterations
    assert again["exit_code"] == 0
    assert again["summary"]["completed"] == EPISODES
    assert {item["action"] for item in again["items"]} == {"skip"}


# --- --reference ---------------------------------------------------------------------------


def test_reference_final_is_the_default_and_raw_hands_over_the_bare_art(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)
    final = _asset(hero_payload, "final_asset")
    raw = _asset(hero_payload, "raw_asset")
    assert final["id"] != raw["id"]

    by_default = _batch_json(data_dir, hero_payload)
    assert by_default["run"]["reference_asset"]["id"] == final["id"]
    assert {r.reference_images for r in _Recording.requests} == {(Path(final["path"]),)}
    _Recording.requests.clear()

    bare = _batch_json(data_dir, hero_payload, "--reference", "raw")
    assert bare["run"]["reference_asset"]["id"] == raw["id"]
    assert bare["summary"]["completed"] == EPISODES
    # A different reference is a different key: the playlist is generated again, not skipped.
    assert {item["action"] for item in bare["items"]} == {"create"}
    assert {r.reference_images for r in _Recording.requests} == {(Path(raw["path"]),)}


def test_an_unknown_reference_kind_exits_2(data_dir: Path) -> None:
    result = _batch(data_dir, _hero(data_dir), "--reference", "sepia")

    assert result.exit_code == ExitCode.USAGE
    assert "--reference" in result.output
    assert _Recording.requests == []


# --- failures: exit 6 and 4 ----------------------------------------------------------------


def test_one_failing_item_exits_6_and_the_summary_names_the_split(
    data_dir: Path, tmp_path: Path
) -> None:
    template = _failing_on(data_dir, tmp_path, FAIL_PERMANENT, 3)

    result = _batch(data_dir, _hero(data_dir), template=template)

    assert result.exit_code == ExitCode.PARTIAL
    assert result.stdout.count("✔") == EPISODES - 1
    assert "failed" in result.stdout
    # The marker is square-bracketed; Rich would swallow it as markup unless escaped.
    assert "FAIL_PERMANENT" in result.stdout
    assert "4 of 5 items completed, 1 failed" in result.stderr
    assert "run the same command again" in result.stderr


def test_a_partial_batch_reports_the_failed_run_in_json(data_dir: Path, tmp_path: Path) -> None:
    template = _failing_on(data_dir, tmp_path, FAIL_PERMANENT, 3)

    result = _batch(data_dir, _hero(data_dir), template=template, json_mode=True)

    assert result.exit_code == ExitCode.PARTIAL
    payload = json.loads(result.stdout)
    assert payload["exit_code"] == 6
    assert payload["run"]["status"] == "failed"
    assert payload["summary"] == {"total": 5, "completed": 4, "failed": 1, "pending": 0}
    failed = [item for item in payload["items"] if item["status"] == "failed"]
    assert [item["part"] for item in failed] == [3]
    assert "provider_permanent" in failed[0]["error"]
    assert json.loads(result.stderr.strip().splitlines()[-1])["error"] == "partial_batch"


def test_a_transient_failure_is_tried_three_times_then_fails_that_item_only(
    data_dir: Path, tmp_path: Path
) -> None:
    template = _failing_on(data_dir, tmp_path, "[[FAIL_TRANSIENT]]", 3)

    result = _batch(data_dir, _hero(data_dir), template=template)

    assert result.exit_code == ExitCode.PARTIAL
    marked = [r for r in _Recording.requests if "FAIL_TRANSIENT" in r.prompt]
    assert len(marked) == 3
    assert len(_Recording.requests) == (EPISODES - 1) + 3
    assert "4 of 5 items completed, 1 failed" in result.stderr


def test_every_item_failing_exits_4(data_dir: Path, tmp_path: Path) -> None:
    template = _failing_on(data_dir, tmp_path, FAIL_PERMANENT, 1, 2, 3, 4, 5)

    result = _batch(data_dir, _hero(data_dir), template=template)

    assert result.exit_code == ExitCode.PROVIDER
    assert result.stdout.count("✔") == 0
    assert result.stdout.count("failed") >= EPISODES
    assert "all 5 items failed" in result.stderr


# --- --dry-run, --only, --max-images --------------------------------------------------------


def test_dry_run_prints_the_plan_and_calls_no_provider(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)

    result = _batch(data_dir, hero_payload, "--dry-run")

    assert result.exit_code == ExitCode.OK, result.output
    for number in range(1, EPISODES + 1):
        assert f"Episode {number}" in result.stdout
    assert result.stdout.count("create") >= EPISODES
    assert _Recording.requests == []
    assert _batch_runs(data_dir) == 0


def test_dry_run_in_json_gives_each_items_key_and_action_and_tracks_a_finished_batch(
    data_dir: Path,
) -> None:
    hero_payload = _hero(data_dir)

    planned = _batch_json(data_dir, hero_payload, "--dry-run")
    assert planned["dry_run"] is True
    assert planned["summary"] == {"create": 5, "retry": 0, "skip": 0}
    assert [row["action"] for row in planned["plan"]] == ["create"] * 5
    assert len({row["key"] for row in planned["plan"]}) == 5
    assert all(len(row["key"]) == 32 for row in planned["plan"])
    assert _Recording.requests == []

    _batch_json(data_dir, hero_payload)
    replanned = _batch_json(data_dir, hero_payload, "--dry-run")

    assert replanned["summary"] == {"create": 0, "retry": 0, "skip": 5}
    assert {row["reason"] for row in replanned["plan"]} == {"completed"}
    assert [row["key"] for row in replanned["plan"]] == [row["key"] for row in planned["plan"]]


def test_only_limits_the_batch_to_the_listed_parts(data_dir: Path) -> None:
    result = _batch(data_dir, _hero(data_dir), "--only", "2,4-5")

    assert result.exit_code == ExitCode.OK, result.output
    for number in (2, 4, 5):
        assert f"Episode {number}" in result.stdout
    for number in (1, 3):
        assert f"Episode {number}" not in result.stdout
    assert len(_Recording.requests) == 3


def test_max_images_below_the_work_exits_2_before_any_provider_call(data_dir: Path) -> None:
    result = _batch(data_dir, _hero(data_dir), "--max-images", "2")

    assert result.exit_code == ExitCode.USAGE
    assert "--max-images" in result.stderr
    assert _Recording.requests == []
    assert _batch_runs(data_dir) == 0


def test_max_images_that_covers_the_work_lets_it_run(data_dir: Path) -> None:
    result = _batch(data_dir, _hero(data_dir), "--max-images", "5")

    assert result.exit_code == ExitCode.OK, result.output
    assert len(_Recording.requests) == EPISODES


@pytest.mark.parametrize("expression", ["x", "3-", "5-3", "0", "2,,3"])
def test_a_malformed_only_expression_exits_2(data_dir: Path, expression: str) -> None:
    result = _batch(data_dir, _hero(data_dir), "--only", expression)

    assert result.exit_code == ExitCode.USAGE
    assert "--only" in result.stderr
    assert _Recording.requests == []


# --- things that cannot be found or used ----------------------------------------------------


def test_an_unknown_playlist_exits_3(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)

    result = _run(
        data_dir,
        "batch",
        "PLnothere000",
        "--hero",
        hero_payload["run"]["id"],
        "--provider",
        "recording",
    )

    assert result.exit_code == ExitCode.NOT_FOUND
    assert "not_found" in result.stderr
    assert _Recording.requests == []


@pytest.mark.parametrize("flag", ["--hero", "--template", "--provider"])
def test_an_unknown_hero_template_or_provider_exits_3(data_dir: Path, flag: str) -> None:
    options = {
        "--hero": _hero(data_dir)["run"]["id"],
        "--template": "series-parts",
        "--provider": "recording",
    }
    options[flag] = "nope"

    result = _run(data_dir, "batch", PLAYLIST, *[part for pair in options.items() for part in pair])

    assert result.exit_code == ExitCode.NOT_FOUND
    assert _Recording.requests == []
    assert _batch_runs(data_dir) == 0


def test_a_hero_run_with_no_pick_exits_2_with_the_command_that_fixes_it(data_dir: Path) -> None:
    hero_payload = _hero(data_dir, pick=False)

    result = _batch(data_dir, hero_payload)

    assert result.exit_code == ExitCode.USAGE
    assert "thumb pick" in result.stderr
    assert _Recording.requests == []


# --- interrupt ------------------------------------------------------------------------------


def test_a_real_sigint_pauses_the_run_and_exits_130(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)
    before = signal.getsignal(signal.SIGINT)

    result = _batch(data_dir, hero_payload, provider="interrupting", json_mode=True)

    assert result.exit_code == ExitCode.INTERRUPTED
    assert signal.getsignal(signal.SIGINT) is before
    payload = json.loads(result.stdout)
    assert payload["exit_code"] == 130
    assert payload["run"]["status"] == "paused"
    assert payload["summary"] == {"total": 5, "completed": 0, "failed": 1, "pending": 4}
    first, *rest = payload["items"]
    assert (first["status"], first["error"]) == ("failed", "interrupted")
    assert {item["status"] for item in rest} == {"pending"}
    assert _stored_status(data_dir, payload["run"]["id"]) == "paused"
    error = json.loads(result.stderr.strip().splitlines()[-1])
    assert error["error"] == "interrupted"
    assert "paused (0 completed, 1 failed, 4 pending)" in error["message"]


def test_the_interrupt_message_names_the_counts_and_how_to_continue(data_dir: Path) -> None:
    result = _batch(data_dir, _hero(data_dir), provider="interrupting")

    assert result.exit_code == ExitCode.INTERRUPTED
    assert "paused (0 completed, 1 failed, 4 pending)" in result.stderr
    assert "run the same command again" in result.stderr
    assert "pending" in result.stdout


def test_running_the_same_command_after_an_interrupt_finishes_it_in_the_original_run(
    data_dir: Path,
) -> None:
    hero_payload = _hero(data_dir)
    interrupted = json.loads(
        _batch(data_dir, hero_payload, provider="interrupting", json_mode=True).stdout
    )
    iterations = _iteration_count(data_dir)
    _Recording.requests.clear()

    finished = _batch_json(data_dir, hero_payload, provider="interrupting")

    assert finished["exit_code"] == 0
    assert finished["summary"] == {"total": 5, "completed": 5, "failed": 0, "pending": 0}
    assert {item["action"] for item in finished["items"]} == {"retry"}
    # Unfinished items are revived where they were created: no iteration row is added.
    assert _iteration_count(data_dir) == iterations
    assert [item["iteration_id"] for item in finished["items"]] == [
        item["iteration_id"] for item in interrupted["items"]
    ]
    assert len(_Recording.requests) == EPISODES
    # The re-run is its own run and ends `completed`; the interrupted run keeps what it stored.
    assert finished["run"]["id"] != interrupted["run"]["id"]
    assert _stored_status(data_dir, finished["run"]["id"]) == "completed"
    assert _stored_status(data_dir, interrupted["run"]["id"]) == "paused"


# --- progress display -----------------------------------------------------------------------


def test_a_terminal_gets_progress_on_stderr_and_json_mode_does_not(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)
    terminal = {"FORCE_COLOR": "1"}

    shown = _batch(data_dir, hero_payload, env=terminal)

    assert shown.exit_code == ExitCode.OK, shown.output
    for number in range(1, EPISODES + 1):
        assert f"Part {number}  Episode {number}" in shown.stderr

    # A different reference means new work, so there is something to show progress for.
    machine = _batch(data_dir, hero_payload, "--reference", "raw", json_mode=True, env=terminal)

    assert machine.exit_code == ExitCode.OK, machine.output
    assert len(_Recording.requests) == 2 * EPISODES
    assert "Episode" not in machine.stderr


def _progress_output(*, enabled: bool) -> str:
    from thumbforge.cli.batch import BatchProgress

    stream = io.StringIO()
    console = Console(
        file=stream, force_terminal=True, width=100, color_system=None, legacy_windows=False
    )
    labels = {1: "Part 1  Episode 1", 2: "Part 2  Episode 2"}
    with BatchProgress(console, labels, enabled=enabled) as progress:
        progress.run_started("RUN", 2)
        progress.iteration_finished("RUN", 1, RunStatus.COMPLETED, None)
        progress.iteration_finished("RUN", 2, RunStatus.FAILED, "provider_permanent: [[BOOM]]")
    return stream.getvalue()


def test_progress_names_each_part_by_title_as_it_finishes() -> None:
    output = _progress_output(enabled=True)

    assert "Part 1  Episode 1" in output
    assert "Part 2  Episode 2" in output
    assert "✔" in output
    assert "✘" in output
    # The error is shown literally: its square brackets are not markup.
    assert "[[BOOM]]" in output


def test_progress_prints_nothing_when_it_is_off() -> None:
    assert _progress_output(enabled=False) == ""
