"""`thumbforge thumb generate` and `thumbforge runs show` end to end with the real fake provider.

Every test starts from a migrated database holding the built-in templates and one stored
video, drives the real Typer app through `CliRunner`, and reads back what the commands print
and what exit status they return (ROADMAP P6.1, phase-6 spec Behaviour 1-4).
"""

from __future__ import annotations

import json
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
