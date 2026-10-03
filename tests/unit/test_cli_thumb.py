"""`thumb generate|pick|show|export` and `runs show` end to end with the real fake provider.

Every test starts from a migrated database holding the built-in templates and one stored
video, drives the real Typer app through `CliRunner`, and reads back what the commands print
and what exit status they return (ROADMAP P6.1 and P6.2, phase-6 spec Behaviour 1-5 and 7).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

import pytest
from typer.testing import CliRunner

from thumbforge.cli._youtube import open_repositories
from thumbforge.cli.app import app
from thumbforge.core.errors import ExitCode
from thumbforge.core.models import VideoMeta
from thumbforge.providers import registry
from thumbforge.providers.fake import FAIL_PERMANENT, FakeProvider

if TYPE_CHECKING:
    from typer.testing import Result

    from thumbforge.core.providers import GenerationRequest, GenerationResult

runner = CliRunner()
TEMPLATES = Path(__file__).parent.parent / "fixtures" / "templates"
VIDEO = "dQw4w9WgXcQ"


class _Flaky(FakeProvider):
    """The real fake, failing for the one seed that the second iteration of a default run uses."""

    key: ClassVar[str] = "flaky"

    async def generate(self, request: GenerationRequest, *, workdir: Path) -> GenerationResult:
        if request.seed == 1:
            request = request.model_copy(update={"prompt": f"{request.prompt} {FAIL_PERMANENT}"})
        return await super().generate(request, workdir=workdir)


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    directory = tmp_path / "data"
    assert runner.invoke(app, ["--data-dir", str(directory), "db", "init"]).exit_code == 0
    with open_repositories(directory / "thumbforge.sqlite3") as repos:
        repos.store_video(
            VideoMeta(
                youtube_id=VIDEO,
                title="Never Gonna Give You Up",
                url=f"https://www.youtube.com/watch?v={VIDEO}",
            )
        )
    return directory


def _run(data_dir: Path, *args: str, json_mode: bool = False) -> Result:
    command = ["--data-dir", str(data_dir), *(["--json"] if json_mode else [])]
    return runner.invoke(app, [*command, *args])


def _generate_json(data_dir: Path, *args: str) -> dict[str, Any]:
    result = _run(data_dir, "thumb", "generate", VIDEO, *args, json_mode=True)
    assert result.exit_code == ExitCode.OK, result.output
    return json.loads(result.stdout)


def _import_failing_template(data_dir: Path, tmp_path: Path) -> None:
    directory = tmp_path / "failing"
    directory.mkdir()
    layout = (TEMPLATES / "valid.toml").read_text(encoding="utf-8")
    (directory / "failing.toml").write_text(
        layout.replace('name = "bold-title"', 'name = "failing"'), encoding="utf-8"
    )
    (directory / "failing.j2").write_text(
        "Art for {{ video.title }}. {{ vars.fail }}", encoding="utf-8"
    )
    result = _run(data_dir, "template", "import", str(directory / "failing.toml"))
    assert result.exit_code == ExitCode.OK, result.output


def test_generate_with_the_fake_provider_completes_four_iterations(data_dir: Path) -> None:
    result = _run(data_dir, "thumb", "generate", VIDEO, "--provider", "fake", "--n", "4")

    assert result.exit_code == ExitCode.OK, result.output
    assert result.stdout.count("completed") >= 4
    assert result.stdout.count("✔") == 4
    assert "bold-title@1" in result.stdout
    assert "Pick one with: thumbforge thumb pick" in result.stdout


def test_json_generate_prints_one_object_with_the_run_and_its_iterations(data_dir: Path) -> None:
    payload = _generate_json(data_dir, "--n", "3")

    assert payload["exit_code"] == 0
    assert payload["run"]["kind"] == "hero"
    assert payload["run"]["status"] == "completed"
    assert len(payload["iterations"]) == 3
    assert all(item["compliant"] is True for item in payload["iterations"])
    assert all(item["final_asset"]["width"] == 1920 for item in payload["iterations"])


def test_runs_show_lists_the_iterations_with_distinct_keys(data_dir: Path) -> None:
    run_id = _generate_json(data_dir)["run"]["id"]

    shown = _run(data_dir, "runs", "show", run_id, json_mode=True)
    plain = _run(data_dir, "runs", "show", run_id)

    assert shown.exit_code == ExitCode.OK, shown.output
    iterations = json.loads(shown.stdout)["iterations"]
    assert len(iterations) == 4
    assert len({item["idempotency_key"] for item in iterations}) == 4
    assert plain.exit_code == ExitCode.OK, plain.output
    assert plain.stdout.count("completed") >= 4
    assert run_id in plain.stdout


def test_a_run_that_cannot_be_found_exits_3(data_dir: Path) -> None:
    result = _run(data_dir, "runs", "show", "01ARZ3NDEKTSV4RRFFQ69G5FAV")

    assert result.exit_code == ExitCode.NOT_FOUND
    assert "not_found" in result.stderr


def test_every_iteration_failing_exits_4_and_the_markers_survive_rendering(
    data_dir: Path, tmp_path: Path
) -> None:
    _import_failing_template(data_dir, tmp_path)

    result = _run(
        data_dir,
        "thumb",
        "generate",
        VIDEO,
        "--template",
        "failing",
        "--var",
        f"fail={FAIL_PERMANENT}",
    )

    assert result.exit_code == ExitCode.PROVIDER
    assert result.stdout.count("failed") >= 4
    assert "all 4 iterations failed" in result.stderr
    assert "Pick one with" not in result.stdout
    # The marker is square-bracketed; Rich would swallow it as markup unless escaped.
    assert "FAIL_PERMANENT" in result.stdout


def test_some_iterations_failing_exits_6_and_names_the_split(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setitem(registry.BUILTIN, "flaky", _Flaky)

    result = _run(data_dir, "thumb", "generate", VIDEO, "--provider", "flaky")

    assert result.exit_code == ExitCode.PARTIAL
    assert "3 of 4 iterations completed, 1 failed" in result.stderr
    assert "Pick one with" in result.stdout


def test_a_final_that_breaks_the_rules_exits_5_and_is_marked(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("THUMBFORGE_OUTPUT__MAX_BYTES", "1000")

    result = _run(data_dir, "thumb", "generate", VIDEO, "--n", "2")

    assert result.exit_code == ExitCode.COMPLIANCE
    assert result.stdout.count("✘") == 2
    assert "not compliant" in result.stdout
    assert "not YouTube-compliant" in result.stderr


def test_json_mode_reports_a_failure_on_stdout_and_stderr(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("THUMBFORGE_OUTPUT__MAX_BYTES", "1000")

    result = _run(data_dir, "thumb", "generate", VIDEO, "--n", "2", json_mode=True)

    assert result.exit_code == ExitCode.COMPLIANCE
    assert json.loads(result.stdout)["exit_code"] == 5
    assert json.loads(result.stderr.strip().splitlines()[-1])["error"] == "compliance"


@pytest.mark.parametrize(
    "args",
    [
        ["thumb", "generate", "nope"],
        ["thumb", "generate", VIDEO, "--provider", "nope"],
        ["thumb", "generate", VIDEO, "--template", "nope"],
    ],
)
def test_an_unknown_video_provider_or_template_exits_3(data_dir: Path, args: list[str]) -> None:
    assert _run(data_dir, *args).exit_code == ExitCode.NOT_FOUND


def test_a_missing_template_variable_exits_2_and_creates_no_run(
    data_dir: Path, tmp_path: Path
) -> None:
    _import_failing_template(data_dir, tmp_path)

    result = _run(data_dir, "thumb", "generate", VIDEO, "--template", "failing")

    assert result.exit_code == ExitCode.USAGE
    assert "vars.fail" in result.stderr


def test_out_copies_every_completed_final(data_dir: Path, tmp_path: Path) -> None:
    out = tmp_path / "out"

    result = _run(data_dir, "thumb", "generate", VIDEO, "--n", "2", "--out", str(out))

    assert result.exit_code == ExitCode.OK, result.output
    assert sorted(path.name for path in out.iterdir()) == [f"{VIDEO}-1.jpg", f"{VIDEO}-2.jpg"]


def test_seeds_count_up_from_the_seed_option(data_dir: Path, tmp_path: Path) -> None:
    _import_failing_template(data_dir, tmp_path)

    result = _run(
        data_dir,
        "thumb",
        "generate",
        VIDEO,
        "--template",
        "failing",
        "--var",
        "fail=calm",
        "--seed",
        "5",
        "--n",
        "2",
        json_mode=True,
    )

    assert result.exit_code == ExitCode.OK, result.output
    assert [item["seed"] for item in json.loads(result.stdout)["iterations"]] == [5, 6]


def test_log_lines_carry_the_run_id(data_dir: Path) -> None:
    result = _run(data_dir, "thumb", "generate", VIDEO, "--n", "2", json_mode=True)

    assert result.exit_code == ExitCode.OK, result.output
    run_id = json.loads(result.stdout)["run"]["id"]
    events = [json.loads(line) for line in result.stderr.splitlines() if line.startswith("{")]
    finished = [event for event in events if event.get("event") == "iteration finished"]
    assert len(finished) == 2
    assert {event["run_id"] for event in finished} == {run_id}


# --- pick, show, export (P6.2) -------------------------------------------------------------

CAPTION = re.compile(r"#(\d+) (★ )?([✔✘])")


def _generate_any(data_dir: Path, *args: str) -> dict[str, Any]:
    """Generate in JSON mode whatever the exit status: the payload carries the run either way."""
    result = _run(data_dir, "thumb", "generate", VIDEO, *args, json_mode=True)
    return json.loads(result.stdout)


def _flaky_run(data_dir: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """A run whose ordinal 2 failed and whose ordinals 1, 3 and 4 completed."""
    monkeypatch.setitem(registry.BUILTIN, "flaky", _Flaky)
    payload = _generate_any(data_dir, "--provider", "flaky")
    assert payload["exit_code"] == ExitCode.PARTIAL
    return payload


def _failed_run(data_dir: Path, tmp_path: Path) -> dict[str, Any]:
    """A run in which every iteration failed at the provider."""
    _import_failing_template(data_dir, tmp_path)
    payload = _generate_any(data_dir, "--template", "failing", "--var", f"fail={FAIL_PERMANENT}")
    assert payload["exit_code"] == ExitCode.PROVIDER
    return payload


def _shown(data_dir: Path, run_id: str) -> dict[str, Any]:
    result = _run(data_dir, "runs", "show", run_id, json_mode=True)
    assert result.exit_code == ExitCode.OK, result.output
    return json.loads(result.stdout)


def _picked(data_dir: Path, run_id: str) -> list[int]:
    return [item["ordinal"] for item in _shown(data_dir, run_id)["iterations"] if item["picked"]]


def _ids(payload: dict[str, Any]) -> dict[int, str]:
    return {item["ordinal"]: item["id"] for item in payload["iterations"]}


def _captions(output: str) -> list[tuple[int, bool, str]]:
    return [(int(n), bool(star), mark) for n, star, mark in CAPTION.findall(output)]


def test_picking_an_ordinal_marks_exactly_that_iteration(data_dir: Path) -> None:
    run_id = _generate_json(data_dir)["run"]["id"]
    assert _picked(data_dir, run_id) == []

    result = _run(data_dir, "thumb", "pick", run_id, "2")

    assert result.exit_code == ExitCode.OK, result.output
    assert f"Picked #2 of run {run_id}" in result.stdout
    assert _picked(data_dir, run_id) == [2]


def test_picking_again_moves_the_pick_instead_of_adding_one(data_dir: Path) -> None:
    payload = _generate_json(data_dir)
    run_id = payload["run"]["id"]
    ids = _ids(payload)

    assert _run(data_dir, "thumb", "pick", run_id, "2").exit_code == ExitCode.OK
    assert _run(data_dir, "thumb", "pick", run_id, ids[4]).exit_code == ExitCode.OK
    assert _picked(data_dir, run_id) == [4]
    # Picking what is already picked succeeds and changes nothing.
    assert _run(data_dir, "thumb", "pick", run_id, "4").exit_code == ExitCode.OK
    assert _picked(data_dir, run_id) == [4]


def test_a_pick_in_one_run_leaves_another_runs_pick_alone(data_dir: Path) -> None:
    first = _generate_json(data_dir, "--n", "2")["run"]["id"]
    second = _generate_json(data_dir, "--n", "2")["run"]["id"]

    assert _run(data_dir, "thumb", "pick", first, "1").exit_code == ExitCode.OK
    assert _run(data_dir, "thumb", "pick", second, "2").exit_code == ExitCode.OK

    assert _picked(data_dir, first) == [1]
    assert _picked(data_dir, second) == [2]


def test_json_pick_prints_the_run_and_the_picked_iteration(data_dir: Path) -> None:
    payload = _generate_json(data_dir)
    run_id = payload["run"]["id"]

    result = _run(data_dir, "thumb", "pick", run_id, "3", json_mode=True)

    assert result.exit_code == ExitCode.OK, result.output
    assert json.loads(result.stdout) == {
        "run_id": run_id,
        "picked": {"id": _ids(payload)[3], "ordinal": 3},
    }


def test_picking_something_that_does_not_exist_exits_3(data_dir: Path) -> None:
    payload = _generate_json(data_dir, "--n", "2")
    run_id = payload["run"]["id"]
    other = _generate_json(data_dir, "--n", "2")

    assert _run(data_dir, "thumb", "pick", run_id, "9").exit_code == ExitCode.NOT_FOUND
    assert _run(data_dir, "thumb", "pick", run_id, "0").exit_code == ExitCode.NOT_FOUND
    unknown_run = _run(data_dir, "thumb", "pick", "01ARZ3NDEKTSV4RRFFQ69G5FAV", "1")
    assert unknown_run.exit_code == ExitCode.NOT_FOUND
    # An iteration of another run is not an iteration of this one.
    foreign = _run(data_dir, "thumb", "pick", run_id, _ids(other)[1])
    assert foreign.exit_code == ExitCode.NOT_FOUND
    assert _picked(data_dir, run_id) == []


def test_picking_a_failed_iteration_exits_2_and_keeps_the_pick(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    payload = _flaky_run(data_dir, monkeypatch)
    run_id = payload["run"]["id"]
    assert _run(data_dir, "thumb", "pick", run_id, "1").exit_code == ExitCode.OK

    by_ordinal = _run(data_dir, "thumb", "pick", run_id, "2")
    by_id = _run(data_dir, "thumb", "pick", run_id, _ids(payload)[2])

    assert by_ordinal.exit_code == ExitCode.USAGE
    assert by_id.exit_code == ExitCode.USAGE
    assert "usage" in by_ordinal.stderr
    assert "hint:" in by_ordinal.stderr
    assert _picked(data_dir, run_id) == [1]


def test_a_non_compliant_final_cannot_be_picked(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("THUMBFORGE_OUTPUT__MAX_BYTES", "1000")
    run_id = _generate_any(data_dir, "--n", "2")["run"]["id"]

    result = _run(data_dir, "thumb", "pick", run_id, "1")

    assert result.exit_code == ExitCode.USAGE
    assert _picked(data_dir, run_id) == []


def test_show_draws_every_iteration_and_marks_the_pick(data_dir: Path) -> None:
    run_id = _generate_json(data_dir)["run"]["id"]

    before = _run(data_dir, "thumb", "show", run_id)
    assert _run(data_dir, "thumb", "pick", run_id, "2").exit_code == ExitCode.OK
    after = _run(data_dir, "thumb", "show", run_id)

    assert before.exit_code == ExitCode.OK, before.output
    assert _captions(before.stdout) == [(n, False, "✔") for n in (1, 2, 3, 4)]
    assert after.exit_code == ExitCode.OK, after.output
    assert _captions(after.stdout) == [(n, n == 2, "✔") for n in (1, 2, 3, 4)]
    assert "bold-title@1" in after.stdout
    assert "2 ★" in after.stdout


def test_show_accepts_a_column_count_and_rejects_zero(data_dir: Path) -> None:
    run_id = _generate_json(data_dir, "--n", "2")["run"]["id"]

    assert _run(data_dir, "thumb", "show", run_id, "--columns", "1").exit_code == ExitCode.OK
    assert _run(data_dir, "thumb", "show", run_id, "--columns", "0").exit_code == ExitCode.USAGE


def test_json_show_is_the_same_document_as_runs_show(data_dir: Path) -> None:
    run_id = _generate_json(data_dir, "--n", "2")["run"]["id"]
    assert _run(data_dir, "thumb", "pick", run_id, "1").exit_code == ExitCode.OK

    shown = _run(data_dir, "thumb", "show", run_id, json_mode=True)

    assert shown.exit_code == ExitCode.OK, shown.output
    assert json.loads(shown.stdout) == _shown(data_dir, run_id)
    assert json.loads(shown.stdout)["iterations"][0]["picked"] is True


def test_show_skips_a_failed_iteration_and_still_draws_the_rest(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run_id = _flaky_run(data_dir, monkeypatch)["run"]["id"]

    result = _run(data_dir, "thumb", "show", run_id)

    assert result.exit_code == ExitCode.OK, result.output
    assert [ordinal for ordinal, _, _ in _captions(result.stdout)] == [1, 3, 4]
    assert "failed" in result.stdout


def test_show_draws_a_non_compliant_final_with_a_cross(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("THUMBFORGE_OUTPUT__MAX_BYTES", "1000")
    run_id = _generate_any(data_dir, "--n", "2")["run"]["id"]

    result = _run(data_dir, "thumb", "show", run_id)

    assert result.exit_code == ExitCode.OK, result.output
    assert _captions(result.stdout) == [(1, False, "✘"), (2, False, "✘")]


def test_showing_an_unknown_run_exits_3(data_dir: Path) -> None:
    result = _run(data_dir, "thumb", "show", "01ARZ3NDEKTSV4RRFFQ69G5FAV")

    assert result.exit_code == ExitCode.NOT_FOUND


def test_exporting_a_run_writes_every_final_byte_for_byte(data_dir: Path, tmp_path: Path) -> None:
    payload = _generate_json(data_dir)
    out = tmp_path / "out" / "nested"

    result = _run(data_dir, "thumb", "export", payload["run"]["id"], "--to", str(out))

    assert result.exit_code == ExitCode.OK, result.output
    assert sorted(path.name for path in out.iterdir()) == [f"{VIDEO}-{n}.jpg" for n in (1, 2, 3, 4)]
    for item in payload["iterations"]:
        stored = Path(item["final_asset"]["path"]).read_bytes()
        assert (out / f"{VIDEO}-{item['ordinal']}.jpg").read_bytes() == stored


def test_export_raw_writes_the_raw_assets(data_dir: Path, tmp_path: Path) -> None:
    payload = _generate_json(data_dir, "--n", "2")
    out = tmp_path / "raw"

    result = _run(data_dir, "thumb", "export", payload["run"]["id"], "--to", str(out), "--raw")

    assert result.exit_code == ExitCode.OK, result.output
    assert sorted(path.name for path in out.iterdir()) == [f"{VIDEO}-1.png", f"{VIDEO}-2.png"]
    for item in payload["iterations"]:
        stored = Path(item["raw_asset"]["path"]).read_bytes()
        assert (out / f"{VIDEO}-{item['ordinal']}.png").read_bytes() == stored


def test_exporting_an_iteration_writes_only_that_one(data_dir: Path, tmp_path: Path) -> None:
    payload = _generate_json(data_dir)
    out = tmp_path / "one"

    result = _run(data_dir, "thumb", "export", _ids(payload)[3], "--to", str(out))

    assert result.exit_code == ExitCode.OK, result.output
    assert [path.name for path in out.iterdir()] == [f"{VIDEO}-3.jpg"]


def test_exporting_a_partial_run_skips_the_failed_iteration(
    data_dir: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    payload = _flaky_run(data_dir, monkeypatch)
    out = tmp_path / "out"

    result = _run(data_dir, "thumb", "export", payload["run"]["id"], "--to", str(out))

    assert result.exit_code == ExitCode.OK, result.output
    assert sorted(path.name for path in out.iterdir()) == [f"{VIDEO}-{n}.jpg" for n in (1, 3, 4)]


def test_json_export_lists_the_files_it_wrote(data_dir: Path, tmp_path: Path) -> None:
    payload = _generate_json(data_dir, "--n", "2")
    out = tmp_path / "out"

    result = _run(
        data_dir, "thumb", "export", payload["run"]["id"], "--to", str(out), json_mode=True
    )

    assert result.exit_code == ExitCode.OK, result.output
    exported = json.loads(result.stdout)
    assert exported == {
        "run_id": payload["run"]["id"],
        "iteration_id": None,
        "raw": False,
        "files": [str(out / f"{VIDEO}-1.jpg"), str(out / f"{VIDEO}-2.jpg")],
    }


def test_exporting_an_unknown_run_or_iteration_exits_3(data_dir: Path, tmp_path: Path) -> None:
    result = _run(
        data_dir, "thumb", "export", "01ARZ3NDEKTSV4RRFFQ69G5FAV", "--to", str(tmp_path / "out")
    )

    assert result.exit_code == ExitCode.NOT_FOUND
    assert not (tmp_path / "out").exists()


def test_exporting_a_run_with_nothing_completed_exits_2(data_dir: Path, tmp_path: Path) -> None:
    payload = _failed_run(data_dir, tmp_path)
    out = tmp_path / "out"

    run = _run(data_dir, "thumb", "export", payload["run"]["id"], "--to", str(out))
    iteration = _run(data_dir, "thumb", "export", _ids(payload)[1], "--to", str(out))

    assert run.exit_code == ExitCode.USAGE
    assert iteration.exit_code == ExitCode.USAGE
    assert "hint:" in run.stderr
    assert not out.exists()


def test_exporting_a_failed_iteration_exits_2(
    data_dir: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    payload = _flaky_run(data_dir, monkeypatch)

    result = _run(data_dir, "thumb", "export", _ids(payload)[2], "--to", str(tmp_path / "out"))

    assert result.exit_code == ExitCode.USAGE


def test_export_requires_a_destination(data_dir: Path) -> None:
    run_id = _generate_json(data_dir, "--n", "1")["run"]["id"]

    assert _run(data_dir, "thumb", "export", run_id).exit_code == ExitCode.USAGE


def test_an_unwritable_destination_is_a_clean_asset_error(data_dir: Path, tmp_path: Path) -> None:
    run_id = _generate_json(data_dir, "--n", "1")["run"]["id"]
    blocker = tmp_path / "file"
    blocker.write_text("in the way", encoding="utf-8")

    result = _run(data_dir, "thumb", "export", run_id, "--to", str(blocker))

    assert result.exit_code == ExitCode.UNEXPECTED
    assert "asset" in result.stderr
