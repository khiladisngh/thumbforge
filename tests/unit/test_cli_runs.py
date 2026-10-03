"""`thumbforge runs list|show|resume|cancel|delete` end to end with the real fake provider.

Every test starts from a migrated database holding the built-in templates, one stored hero video
and a five-video playlist, drives the real Typer app through `CliRunner`, and reads back what the
command prints, which exit status it returns and what it left in the database and on disk
(ROADMAP P7.4, phase-7 spec Behaviour 5-7). The service underneath is covered by
`test_batch_service.py`; what is defended here is the commands' contract: arguments, output, exit
codes, the interrupt, and which rows and files a delete may touch.
"""

from __future__ import annotations

import asyncio
import json
import re
import signal
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

import pytest
from tenacity import wait_none
from typer.testing import CliRunner

from thumbforge.cli._youtube import open_repositories
from thumbforge.cli.app import app
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
#: Wide enough that Rich never wraps a run id or a title inside a table or a diagnostic.
WIDE = {"COLUMNS": "200"}
ANSI = re.compile(r"\x1b\[[0-9;]*m")


class _Recording(FakeProvider):
    """The real fake, remembering every request it was handed."""

    key: ClassVar[str] = "recording"
    requests: ClassVar[list[GenerationRequest]] = []

    async def generate(self, request: GenerationRequest, *, workdir: Path) -> GenerationResult:
        self.requests.append(request)
        return await super().generate(request, workdir=workdir)


class _Twin(_Recording):
    """A second provider that makes exactly what `recording` makes, under another profile."""

    key: ClassVar[str] = "twin"


class _InterruptAfter(_Recording):
    """The real fake, but call number `allowed + 1` raises a real SIGINT and never returns."""

    key: ClassVar[str] = "interrupt-after"
    allowed: ClassVar[int] = 2
    seen: ClassVar[int] = 0

    async def generate(self, request: GenerationRequest, *, workdir: Path) -> GenerationResult:
        type(self).seen += 1
        if type(self).seen == type(self).allowed + 1:
            self.requests.append(request)
            signal.raise_signal(signal.SIGINT)
            await asyncio.sleep(60)
        return await super().generate(request, workdir=workdir)


@pytest.fixture(autouse=True)
def providers(monkeypatch: pytest.MonkeyPatch) -> type[_Recording]:
    monkeypatch.setitem(registry.BUILTIN, "recording", _Recording)
    monkeypatch.setitem(registry.BUILTIN, "twin", _Twin)
    monkeypatch.setitem(registry.BUILTIN, "interrupt-after", _InterruptAfter)
    monkeypatch.setattr(_Recording, "requests", [])
    monkeypatch.setattr(_InterruptAfter, "allowed", 2)
    monkeypatch.setattr(_InterruptAfter, "seen", 0)
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


def _run(data_dir: Path, *args: str, json_mode: bool = False) -> Result:
    command = ["--data-dir", str(data_dir), *(["--json"] if json_mode else [])]
    return runner.invoke(app, [*command, *args], env=WIDE)


def _json(result: Result) -> Any:
    return json.loads(result.stdout)


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


def _flaky_template(data_dir: Path, tmp_path: Path, part: int) -> str:
    """A template whose prompt carries the permanent-failure marker for one part only."""
    prompt = (
        "Part {{ part_number }}: {{ video.title }}"
        f"{{% if part_number == {part} %}} {FAIL_PERMANENT}{{% endif %}}"
    )
    return _template(data_dir, tmp_path, f"series-flaky-{part}", prompt)


def _hero(data_dir: Path, *, pick: bool = True) -> dict[str, Any]:
    """A completed two-iteration hero run, the first iteration picked."""
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
    payload: dict[str, Any] = _json(result)
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
        json_mode=True,
    )


def _batch_ok(data_dir: Path, hero_payload: dict[str, Any], *args: str, **kwargs: str) -> Any:
    result = _batch(data_dir, hero_payload, *args, **kwargs)
    assert result.exit_code == ExitCode.OK, result.output
    return _json(result)


def _show(data_dir: Path, run_id: str) -> Any:
    result = _run(data_dir, "runs", "show", run_id, json_mode=True)
    assert result.exit_code == ExitCode.OK, result.output
    return _json(result)


def _paused_batch(data_dir: Path, hero_payload: dict[str, Any]) -> dict[str, Any]:
    """A batch run interrupted on its third provider call, with some items finished and some not.

    Which items are in flight when the signal lands is up to the scheduler, so a test reads the
    split from the payload instead of expecting one.
    """
    result = _batch(data_dir, hero_payload, "--concurrency", "1", provider="interrupt-after")
    assert result.exit_code == ExitCode.INTERRUPTED, result.output
    payload: dict[str, Any] = _json(result)
    summary = payload["summary"]
    assert summary["total"] == EPISODES
    assert summary["completed"] >= 1
    assert summary["failed"] >= 1
    assert summary["pending"] >= 1
    assert summary["completed"] + summary["failed"] + summary["pending"] == EPISODES
    _Recording.requests.clear()
    return payload


def _titles(payload: dict[str, Any], status: str) -> list[str]:
    """The titles of the items of a batch payload that are in `status`."""
    return [item["title"] for item in payload["items"] if item["status"] == status]


def _rows(data_dir: Path, sql: str) -> list[tuple[Any, ...]]:
    with closing(sqlite3.connect(data_dir / "thumbforge.sqlite3")) as connection:
        return connection.execute(sql).fetchall()


def _count(data_dir: Path, table: str) -> int:
    return _rows(data_dir, f"SELECT COUNT(*) FROM {table}")[0][0]


def _iteration_paths(payload: dict[str, Any]) -> list[Path]:
    """Every stored raw and final file of the run `payload` describes."""
    paths: list[Path] = []
    for item in payload["iterations"]:
        for kind in ("raw_asset", "final_asset"):
            if item[kind] is not None:
                paths.append(Path(item[kind]["path"]))
    return paths


# --- runs list ------------------------------------------------------------------------------


def test_list_shows_every_run_newest_first_with_its_counts(data_dir: Path, tmp_path: Path) -> None:
    hero_payload = _hero(data_dir)
    done = _batch_ok(data_dir, hero_payload)
    flaky = _flaky_template(data_dir, tmp_path, 3)
    partial = _json(_batch(data_dir, hero_payload, template=flaky))
    assert partial["run"]["status"] == "failed"

    result = _run(data_dir, "runs", "list", json_mode=True)

    assert result.exit_code == ExitCode.OK, result.output
    runs = _json(result)["runs"]
    assert [run["id"] for run in runs] == [
        partial["run"]["id"],
        done["run"]["id"],
        hero_payload["run"]["id"],
    ]
    newest, middle, oldest = runs
    assert (newest["kind"], newest["status"]) == ("batch", "failed")
    assert newest["counts"] == {"total": 5, "completed": 4, "failed": 1, "pending": 0}
    assert newest["template"] == "series-flaky-3@1"
    assert (middle["kind"], middle["status"]) == ("batch", "completed")
    assert middle["counts"] == {"total": 5, "completed": 5, "failed": 0, "pending": 0}
    assert middle["provider"] == done["run"]["provider"]
    assert (oldest["kind"], oldest["status"]) == ("hero", "completed")
    assert oldest["counts"]["total"] == 2
    assert oldest["video"] == HERO_VIDEO


def test_list_prints_a_table_of_the_runs(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)
    done = _batch_ok(data_dir, hero_payload)

    result = _run(data_dir, "runs", "list")

    assert result.exit_code == ExitCode.OK, result.output
    assert done["run"]["id"] in result.stdout
    assert hero_payload["run"]["id"] in result.stdout
    assert "batch" in result.stdout
    assert "hero" in result.stdout
    assert "5/5" in result.stdout
    assert "series-parts@1" in result.stdout


def test_list_filters_by_kind_status_and_limit(data_dir: Path, tmp_path: Path) -> None:
    hero_payload = _hero(data_dir)
    done = _batch_ok(data_dir, hero_payload)
    flaky = _flaky_template(data_dir, tmp_path, 2)
    partial = _json(_batch(data_dir, hero_payload, template=flaky))

    def ids(*args: str) -> list[str]:
        result = _run(data_dir, "runs", "list", *args, json_mode=True)
        assert result.exit_code == ExitCode.OK, result.output
        return [run["id"] for run in _json(result)["runs"]]

    assert ids("--kind", "hero") == [hero_payload["run"]["id"]]
    assert ids("--kind", "batch") == [partial["run"]["id"], done["run"]["id"]]
    assert ids("--status", "failed") == [partial["run"]["id"]]
    assert ids("--kind", "batch", "--status", "completed") == [done["run"]["id"]]
    assert ids("--limit", "1") == [partial["run"]["id"]]
    assert ids("--kind", "iterate") == []


def test_list_on_an_empty_database_is_an_empty_list(data_dir: Path) -> None:
    result = _run(data_dir, "runs", "list", json_mode=True)

    assert result.exit_code == ExitCode.OK, result.output
    assert _json(result) == {"runs": []}
    assert _run(data_dir, "runs", "list").exit_code == ExitCode.OK


@pytest.mark.parametrize("option", ["--kind", "--status"])
def test_list_rejects_a_value_that_is_not_a_kind_or_status(data_dir: Path, option: str) -> None:
    result = _run(data_dir, "runs", "list", option, "sepia")

    assert result.exit_code == ExitCode.USAGE
    # Typer styles its usage errors when it thinks it is on CI, and the codes split the option.
    assert option in ANSI.sub("", result.output)


# --- runs show ------------------------------------------------------------------------------


def test_show_of_a_batch_run_reports_its_playlist_and_progress(data_dir: Path) -> None:
    paused = _paused_batch(data_dir, _hero(data_dir))
    run_id = paused["run"]["id"]

    shown = _show(data_dir, run_id)
    plain = _run(data_dir, "runs", "show", run_id)

    counts = paused["summary"]
    assert shown["summary"] == counts
    assert shown["run"]["status"] == "paused"
    assert shown["run"]["playlist"] == PLAYLIST
    assert plain.exit_code == ExitCode.OK, plain.output
    assert "The Series" in plain.stdout
    assert (
        f"{counts['completed']} completed, {counts['failed']} failed, "
        f"{counts['pending']} pending of 5"
    ) in plain.stdout


def test_show_of_a_hero_run_has_a_summary_but_no_playlist(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)

    shown = _show(data_dir, hero_payload["run"]["id"])
    plain = _run(data_dir, "runs", "show", hero_payload["run"]["id"])

    assert shown["summary"] == {"total": 2, "completed": 2, "failed": 0, "pending": 0}
    assert shown["run"]["playlist"] is None
    assert "Playlist" not in plain.stdout


# --- runs resume ----------------------------------------------------------------------------


def test_resume_regenerates_only_the_items_that_are_not_completed(data_dir: Path) -> None:
    paused = _paused_batch(data_dir, _hero(data_dir))
    run_id = paused["run"]["id"]
    done = [item["iteration_id"] for item in paused["items"] if item["status"] == "completed"]
    left = [
        title
        for title in (f"Episode {n}" for n in range(1, 6))
        if title not in _titles(paused, "completed")
    ]
    before = _rows(data_dir, "SELECT id, updated_at FROM iteration ORDER BY id")
    runs_before = _count(data_dir, "run")
    iterations_before = _count(data_dir, "iteration")

    result = _run(data_dir, "runs", "resume", run_id, json_mode=True)

    assert result.exit_code == ExitCode.OK, result.output
    payload = _json(result)
    assert payload["exit_code"] == 0
    assert payload["run"]["id"] == run_id
    assert payload["run"]["status"] == "completed"
    assert payload["summary"] == {"total": 5, "completed": 5, "failed": 0, "pending": 0}
    # Each unfinished item is asked for once; the finished ones cost nothing and stay as written.
    assert 0 < len(left) < EPISODES
    assert len(_Recording.requests) == len(left)
    for number in range(1, EPISODES + 1):
        asked = [r for r in _Recording.requests if f"Episode {number}" in r.prompt]
        assert len(asked) == (1 if f"Episode {number}" in left else 0)
    after = dict(_rows(data_dir, "SELECT id, updated_at FROM iteration"))
    assert all(after[iteration] == stamp for iteration, stamp in before if iteration in done)
    # The same run, finished in place: no new run and no new iteration.
    assert _count(data_dir, "run") == runs_before
    assert _count(data_dir, "iteration") == iterations_before
    assert _show(data_dir, run_id)["run"]["status"] == "completed"


def test_resume_prints_the_summary_table_for_a_person(data_dir: Path) -> None:
    paused = _paused_batch(data_dir, _hero(data_dir))

    result = _run(data_dir, "runs", "resume", paused["run"]["id"])

    assert result.exit_code == ExitCode.OK, result.output
    for number in range(1, EPISODES + 1):
        assert f"Episode {number}" in result.stdout
    assert result.stdout.count("✔") == EPISODES


def test_resume_retries_a_failed_item_once_more_then_leaves_it(
    data_dir: Path, tmp_path: Path
) -> None:
    flaky = _flaky_template(data_dir, tmp_path, 3)
    failed = _json(_batch(data_dir, _hero(data_dir), template=flaky))
    assert failed["exit_code"] == ExitCode.PARTIAL
    run_id = failed["run"]["id"]
    _Recording.requests.clear()

    again = _run(data_dir, "runs", "resume", run_id, json_mode=True)

    # The one failed item is tried again, fails again, and the run still ends partial.
    assert again.exit_code == ExitCode.PARTIAL
    assert [request.prompt.split(":")[0] for request in _Recording.requests] == ["Part 3"]
    assert _json(again)["summary"] == {"total": 5, "completed": 4, "failed": 1, "pending": 0}
    assert _json(again)["exit_code"] == 6
    assert _show(data_dir, run_id)["run"]["status"] == "failed"
    _Recording.requests.clear()

    # Its tries are used up now: resuming again makes no provider call.
    last = _run(data_dir, "runs", "resume", run_id, json_mode=True)
    assert last.exit_code == ExitCode.PARTIAL
    assert _Recording.requests == []


def test_resume_pressed_with_ctrl_c_pauses_the_run_again_and_exits_130(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    paused = _paused_batch(data_dir, _hero(data_dir))
    run_id = paused["run"]["id"]
    # Re-arm the provider so the first call of the resume is interrupted too.
    monkeypatch.setattr(_InterruptAfter, "seen", 0)
    monkeypatch.setattr(_InterruptAfter, "allowed", 0)
    before = signal.getsignal(signal.SIGINT)

    result = _run(data_dir, "runs", "resume", run_id, json_mode=True)

    assert result.exit_code == ExitCode.INTERRUPTED
    assert signal.getsignal(signal.SIGINT) is before
    payload = _json(result)
    assert payload["exit_code"] == 130
    assert payload["run"]["status"] == "paused"
    # Finished work is never undone by a second interrupt.
    assert payload["summary"]["completed"] == paused["summary"]["completed"]
    assert payload["summary"]["pending"] + payload["summary"]["failed"] == (
        EPISODES - paused["summary"]["completed"]
    )
    assert _show(data_dir, run_id)["run"]["status"] == "paused"
    error = json.loads(result.stderr.strip().splitlines()[-1])
    assert error["error"] == "interrupted"


def test_resume_refuses_a_completed_run(data_dir: Path) -> None:
    done = _batch_ok(data_dir, _hero(data_dir))
    _Recording.requests.clear()

    result = _run(data_dir, "runs", "resume", done["run"]["id"])

    assert result.exit_code == ExitCode.USAGE
    assert "completed" in result.stderr
    assert _Recording.requests == []


def test_resume_refuses_a_cancelled_run(data_dir: Path) -> None:
    paused = _paused_batch(data_dir, _hero(data_dir))
    assert _run(data_dir, "runs", "cancel", paused["run"]["id"]).exit_code == ExitCode.OK

    result = _run(data_dir, "runs", "resume", paused["run"]["id"])

    assert result.exit_code == ExitCode.USAGE
    assert "cancelled" in result.stderr
    assert _Recording.requests == []


def test_resume_refuses_a_run_that_is_not_a_batch(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)

    result = _run(data_dir, "runs", "resume", hero_payload["run"]["id"])

    assert result.exit_code == ExitCode.USAGE
    assert "batch" in result.stderr
    assert _Recording.requests == []


def test_resume_of_an_unknown_run_exits_3(data_dir: Path) -> None:
    result = _run(data_dir, "runs", "resume", "01ARZ3NDEKTSV4RRFFQ69G5FAV")

    assert result.exit_code == ExitCode.NOT_FOUND
    assert "not_found" in result.stderr


# --- runs cancel ----------------------------------------------------------------------------


def test_cancel_marks_a_paused_run_and_its_unfinished_iterations_cancelled(
    data_dir: Path,
) -> None:
    paused = _paused_batch(data_dir, _hero(data_dir))
    run_id = paused["run"]["id"]

    result = _run(data_dir, "runs", "cancel", run_id, json_mode=True)

    assert result.exit_code == ExitCode.OK, result.output
    assert _json(result)["run"]["id"] == run_id
    assert _json(result)["run"]["status"] == "cancelled"
    shown = _show(data_dir, run_id)
    assert shown["run"]["status"] == "cancelled"
    statuses = sorted(item["status"] for item in shown["iterations"])
    counts = paused["summary"]
    # Finished and failed work stays as it was; what was still waiting is abandoned.
    assert statuses == sorted(
        ["completed"] * counts["completed"]
        + ["failed"] * counts["failed"]
        + ["cancelled"] * counts["pending"]
    )
    assert _Recording.requests == []


def test_cancelling_a_cancelled_run_changes_nothing(data_dir: Path) -> None:
    paused = _paused_batch(data_dir, _hero(data_dir))
    run_id = paused["run"]["id"]
    assert _run(data_dir, "runs", "cancel", run_id).exit_code == ExitCode.OK
    stored = _show(data_dir, run_id)

    result = _run(data_dir, "runs", "cancel", run_id)

    assert result.exit_code == ExitCode.OK, result.output
    assert _show(data_dir, run_id) == stored


def test_cancel_refuses_a_completed_run_and_leaves_it_completed(data_dir: Path) -> None:
    done = _batch_ok(data_dir, _hero(data_dir))
    run_id = done["run"]["id"]

    result = _run(data_dir, "runs", "cancel", run_id)

    assert result.exit_code == ExitCode.USAGE
    assert "completed" in result.stderr
    assert _show(data_dir, run_id)["run"]["status"] == "completed"


def test_cancel_prints_a_line_for_a_person(data_dir: Path) -> None:
    paused = _paused_batch(data_dir, _hero(data_dir))

    result = _run(data_dir, "runs", "cancel", paused["run"]["id"])

    assert result.exit_code == ExitCode.OK, result.output
    assert paused["run"]["id"] in result.stdout
    assert "cancelled" in result.stdout


def test_cancel_of_an_unknown_run_exits_3(data_dir: Path) -> None:
    result = _run(data_dir, "runs", "cancel", "01ARZ3NDEKTSV4RRFFQ69G5FAV")

    assert result.exit_code == ExitCode.NOT_FOUND
    assert "not_found" in result.stderr


# --- runs delete ----------------------------------------------------------------------------


def test_delete_removes_the_run_and_its_iterations_but_keeps_the_files(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)
    done = _batch_ok(data_dir, hero_payload)
    run_id = done["run"]["id"]
    files = _iteration_paths(_show(data_dir, run_id))
    assert len(files) == 2 * EPISODES
    runs_before = _count(data_dir, "run")
    iterations_before = _count(data_dir, "iteration")
    assets_before = _count(data_dir, "asset")

    result = _run(data_dir, "runs", "delete", run_id, json_mode=True)

    assert result.exit_code == ExitCode.OK, result.output
    assert _json(result) == {"deleted": {"run": run_id, "iterations": EPISODES, "assets": []}}
    assert _count(data_dir, "run") == runs_before - 1
    assert _count(data_dir, "iteration") == iterations_before - EPISODES
    # Without --assets the images stay: rows and files alike.
    assert _count(data_dir, "asset") == assets_before
    assert all(path.is_file() for path in files)
    assert _run(data_dir, "runs", "show", run_id).exit_code == ExitCode.NOT_FOUND
    assert _show(data_dir, hero_payload["run"]["id"])["summary"]["completed"] == 2


def test_delete_prints_a_line_for_a_person(data_dir: Path) -> None:
    done = _batch_ok(data_dir, _hero(data_dir))

    result = _run(data_dir, "runs", "delete", done["run"]["id"])

    assert result.exit_code == ExitCode.OK, result.output
    assert done["run"]["id"] in result.stdout
    assert f"{EPISODES} iterations" in result.stdout


def test_delete_with_assets_unlinks_only_the_files_nothing_else_uses(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)
    first = _batch_ok(data_dir, hero_payload)
    # The twin makes byte-identical images under another provider profile, so a different set
    # of iterations (new keys) shares every one of the first batch's files.
    second = _batch_ok(data_dir, hero_payload, provider="twin")
    first_files = _iteration_paths(_show(data_dir, first["run"]["id"]))
    second_files = _iteration_paths(_show(data_dir, second["run"]["id"]))
    assert first["run"]["id"] != second["run"]["id"]
    assert set(first_files) == set(second_files)
    hero_files = _iteration_paths(_show(data_dir, hero_payload["run"]["id"]))
    assert not set(hero_files) & set(first_files)
    assets_before = _count(data_dir, "asset")

    kept = _run(data_dir, "runs", "delete", first["run"]["id"], "--assets", json_mode=True)

    # The second batch still holds every image, so nothing may go.
    assert kept.exit_code == ExitCode.OK, kept.output
    assert _json(kept)["deleted"]["assets"] == []
    assert _count(data_dir, "asset") == assets_before
    assert all(path.is_file() for path in first_files)

    gone = _run(data_dir, "runs", "delete", second["run"]["id"], "--assets", json_mode=True)

    assert gone.exit_code == ExitCode.OK, gone.output
    removed = _json(gone)["deleted"]["assets"]
    assert sorted(Path(path) for path in removed) == sorted(set(second_files))
    assert not any(path.exists() for path in second_files)
    assert _count(data_dir, "asset") == assets_before - len(set(second_files))
    # The hero's own images, which the batches used as their reference, were never candidates.
    assert all(path.is_file() for path in hero_files)
    assert _show(data_dir, hero_payload["run"]["id"])["summary"]["completed"] == 2


def test_delete_with_assets_keeps_the_reference_image_its_hero_still_owns(
    data_dir: Path,
) -> None:
    hero_payload = _hero(data_dir)
    done = _batch_ok(data_dir, hero_payload)
    reference = Path(done["run"]["reference_asset"]["path"])
    assert reference.is_file()

    result = _run(data_dir, "runs", "delete", done["run"]["id"], "--assets", json_mode=True)

    assert result.exit_code == ExitCode.OK, result.output
    assert str(reference) not in _json(result)["deleted"]["assets"]
    assert reference.is_file()
    hero_after = _show(data_dir, hero_payload["run"]["id"])
    assert all(path.is_file() for path in _iteration_paths(hero_after))


def test_delete_refuses_a_hero_a_batch_uses_and_leaves_everything_intact(
    data_dir: Path,
) -> None:
    hero_payload = _hero(data_dir)
    hero_id = hero_payload["run"]["id"]
    done = _batch_ok(data_dir, hero_payload)
    files = _iteration_paths(_show(data_dir, hero_id))
    tables = {name: _count(data_dir, name) for name in ("run", "iteration", "asset")}

    result = _run(data_dir, "runs", "delete", hero_id, "--assets")

    assert result.exit_code == ExitCode.USAGE
    assert done["run"]["id"] in result.stderr
    assert "delete" in result.stderr
    assert tables == {name: _count(data_dir, name) for name in tables}
    assert all(path.is_file() for path in files)
    assert _show(data_dir, hero_id)["summary"]["completed"] == 2


def test_delete_refuses_the_parent_of_a_refinement(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)
    hero_id = hero_payload["run"]["id"]
    refined = _run(data_dir, "thumb", "iterate", hero_id, "--n", "1", json_mode=True)
    assert refined.exit_code == ExitCode.OK, refined.output
    child_id = _json(refined)["run"]["id"]
    assert _json(refined)["run"]["parent_run_id"] == hero_id

    result = _run(data_dir, "runs", "delete", hero_id, json_mode=True)

    assert result.exit_code == ExitCode.USAGE
    assert child_id in json.loads(result.stderr.strip().splitlines()[-1])["message"]
    assert _show(data_dir, hero_id)["run"]["id"] == hero_id


def test_a_hero_can_be_deleted_once_its_batch_is_gone(data_dir: Path) -> None:
    hero_payload = _hero(data_dir)
    hero_id = hero_payload["run"]["id"]
    files = _iteration_paths(_show(data_dir, hero_id))
    done = _batch_ok(data_dir, hero_payload)
    assert _run(data_dir, "runs", "delete", hero_id).exit_code == ExitCode.USAGE
    assert _run(data_dir, "runs", "delete", done["run"]["id"], "--assets").exit_code == 0

    result = _run(data_dir, "runs", "delete", hero_id, "--assets", json_mode=True)

    assert result.exit_code == ExitCode.OK, result.output
    assert sorted(Path(path) for path in _json(result)["deleted"]["assets"]) == sorted(set(files))
    assert not any(path.exists() for path in files)
    assert _count(data_dir, "run") == 0
    assert _count(data_dir, "iteration") == 0
    assert _count(data_dir, "asset") == 0


def test_delete_of_an_unknown_run_exits_3(data_dir: Path) -> None:
    result = _run(data_dir, "runs", "delete", "01ARZ3NDEKTSV4RRFFQ69G5FAV")

    assert result.exit_code == ExitCode.NOT_FOUND
    assert "not_found" in result.stderr
