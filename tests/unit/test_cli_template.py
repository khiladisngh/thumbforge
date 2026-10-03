"""Unit tests for ``thumbforge template`` CLI commands (ROADMAP P4.1, P4.4, phase-4 spec)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from typer.testing import CliRunner

from thumbforge.cli.app import app
from thumbforge.core.errors import ExitCode

if TYPE_CHECKING:
    from typer.testing import Result

runner = CliRunner()
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "templates"


def test_template_validate_valid_fixture() -> None:
    result = runner.invoke(app, ["template", "validate", str(FIXTURES_DIR / "valid.toml")])
    assert result.exit_code == ExitCode.OK
    assert "ok" in result.stdout.lower()
    assert "bold-title" in result.stdout


def test_template_validate_bad_anchor_fixture() -> None:
    result = runner.invoke(app, ["template", "validate", str(FIXTURES_DIR / "bad-anchor.toml")])
    assert result.exit_code == ExitCode.USAGE
    assert "title.anchor" in result.stderr


def test_template_validate_json_mode_valid() -> None:
    valid_path = str(FIXTURES_DIR / "valid.toml")
    result = runner.invoke(app, ["--json", "template", "validate", valid_path])
    assert result.exit_code == ExitCode.OK
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["template"] == "bold-title"


def test_template_validate_json_mode_bad_anchor() -> None:
    bad_anchor_path = str(FIXTURES_DIR / "bad-anchor.toml")
    result = runner.invoke(app, ["--json", "template", "validate", bad_anchor_path])
    assert result.exit_code == ExitCode.USAGE
    lines = [line for line in result.stderr.splitlines() if line.strip()]
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload["error"] == "template"
    assert payload["exit_code"] == 2
    assert "title.anchor" in payload["message"]


def test_a_missing_file_keeps_the_json_error_contract(tmp_path: Path) -> None:
    result = runner.invoke(app, ["--json", "template", "validate", str(tmp_path / "missing.toml")])
    assert result.exit_code == ExitCode.USAGE
    payload = json.loads(result.stderr)
    assert (payload["error"], payload["exit_code"]) == ("template", 2)


def test_markup_in_the_template_name_is_printed_literally(tmp_path: Path) -> None:
    layout = tmp_path / "markup.toml"
    valid = (FIXTURES_DIR / "valid.toml").read_text(encoding="utf-8")
    layout.write_text(valid.replace('name = "bold-title"', 'name = "foo[/]"'), encoding="utf-8")
    result = runner.invoke(app, ["template", "validate", str(layout)])
    assert result.exit_code == ExitCode.OK, result.output
    assert "foo[/]" in result.stdout


# --- P4.4: database-backed commands -------------------------------------------------------


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    """A freshly initialised database: `db init` has loaded the three built-ins."""
    directory = tmp_path / "data"
    assert _run(directory, "db", "init").exit_code == ExitCode.OK
    return directory


def _run(data_dir: Path, *args: str, json_mode: bool = False) -> Result:
    command = ["--data-dir", str(data_dir), *(["--json"] if json_mode else [])]
    return runner.invoke(app, [*command, *args])


def _pair(directory: Path, name: str = "demo", prompt: str = "Art for {{ video.title }}.") -> Path:
    """Write `name.toml` (the valid fixture renamed) and `name.j2`; return the `.toml`."""
    directory.mkdir(parents=True, exist_ok=True)
    layout = (FIXTURES_DIR / "valid.toml").read_text(encoding="utf-8")
    toml_path = directory / f"{name}.toml"
    toml_path.write_text(
        layout.replace('name = "bold-title"', f'name = "{name}"'), encoding="utf-8"
    )
    (directory / f"{name}.j2").write_text(prompt, encoding="utf-8")
    return toml_path


def _rows(data_dir: Path) -> list[tuple[str, int, bool]]:
    result = _run(data_dir, "template", "list", json_mode=True)
    assert result.exit_code == ExitCode.OK, result.output
    return [(t["name"], t["version"], t["builtin"]) for t in json.loads(result.stdout)["templates"]]


def test_list_after_db_init_shows_the_three_builtins_at_version_1(data_dir: Path) -> None:
    result = _run(data_dir, "template", "list")
    assert result.exit_code == ExitCode.OK, result.output
    rows = [
        [cell.strip() for cell in line.strip("│ ").split("│")]
        for line in result.stdout.splitlines()
        if "│" in line and "Name" not in line
    ]
    assert rows == [
        ["bold-title", "1", "yes"],
        ["minimal", "1", "yes"],
        ["series-parts", "1", "yes"],
    ]


def test_list_json_has_one_entry_per_stored_version(data_dir: Path, tmp_path: Path) -> None:
    path = _pair(tmp_path / "src", "minimal", prompt="my own minimal")
    assert _run(data_dir, "template", "import", str(path)).exit_code == ExitCode.OK
    payload = json.loads(_run(data_dir, "template", "list", json_mode=True).stdout)
    assert payload["count"] == 4
    assert [(t["name"], t["version"], t["builtin"]) for t in payload["templates"]] == [
        ("bold-title", 1, True),
        ("minimal", 1, True),
        ("minimal", 2, False),
        ("series-parts", 1, True),
    ]


def test_rerunning_db_init_stores_nothing_new(data_dir: Path) -> None:
    before = _rows(data_dir)
    assert _run(data_dir, "db", "init").exit_code == ExitCode.OK
    assert _rows(data_dir) == before


def test_show_with_and_without_the_version_is_identical(data_dir: Path) -> None:
    bare = _run(data_dir, "template", "show", "bold-title")
    exact = _run(data_dir, "template", "show", "bold-title@1")
    assert bare.exit_code == exact.exit_code == ExitCode.OK, bare.output
    assert bare.stdout == exact.stdout
    assert "bold-title@1" in bare.stdout
    assert "{{ negative_space }}" in bare.stdout
    assert 'anchor = "bottom-left"' in bare.stdout


def test_show_json_carries_the_prompt_and_the_layout(data_dir: Path) -> None:
    result = _run(data_dir, "template", "show", "series-parts", json_mode=True)
    assert result.exit_code == ExitCode.OK, result.output
    payload = json.loads(result.stdout)
    assert payload["template"] == "series-parts@1"
    assert (payload["name"], payload["version"], payload["builtin"]) == ("series-parts", 1, True)
    assert "Part {{ part_number }}" in payload["prompt"]
    assert payload["layout"]["part"]["badge"]["fill"] == "#FFD400"
    assert len(payload["spec_hash"]) == 64


@pytest.mark.parametrize("ref", ["nope", "bold-title@2"])
def test_show_an_unknown_template_or_version_exits_3(data_dir: Path, ref: str) -> None:
    result = _run(data_dir, "template", "show", ref)
    assert result.exit_code == ExitCode.NOT_FOUND
    assert "hint" in result.stderr


def test_show_an_unknown_version_lists_the_stored_ones(data_dir: Path) -> None:
    result = _run(data_dir, "template", "show", "bold-title@2", json_mode=True)
    payload = json.loads(result.stderr)
    assert payload["exit_code"] == ExitCode.NOT_FOUND
    assert "bold-title@1" in payload["hint"]


@pytest.mark.parametrize("ref", ["name@x", "name@0", "@1", ""])
def test_show_a_malformed_reference_exits_2(data_dir: Path, ref: str) -> None:
    assert _run(data_dir, "template", "show", ref).exit_code == ExitCode.USAGE


def test_importing_the_same_pair_twice_keeps_one_row(data_dir: Path, tmp_path: Path) -> None:
    path = _pair(tmp_path / "src")
    first = _run(data_dir, "template", "import", str(path), json_mode=True)
    second = _run(data_dir, "template", "import", str(path), json_mode=True)
    assert first.exit_code == second.exit_code == ExitCode.OK, second.output
    one, two = json.loads(first.stdout), json.loads(second.stdout)
    assert (one["status"], one["template"]) == ("imported", "demo@1")
    assert (two["status"], two["template"]) == ("unchanged", "demo@1")
    assert two["spec_hash"] == one["spec_hash"]
    assert [r for r in _rows(data_dir) if r[0] == "demo"] == [("demo", 1, False)]
    human = _run(data_dir, "template", "import", str(path))
    assert human.exit_code == ExitCode.OK
    assert "demo@1" in human.stdout


def test_a_one_character_prompt_change_imports_version_2(data_dir: Path, tmp_path: Path) -> None:
    path = _pair(tmp_path / "src", prompt="Art for {{ video.title }}.")
    first = json.loads(_run(data_dir, "template", "import", str(path), json_mode=True).stdout)
    path.with_suffix(".j2").write_text("Art for {{ video.title }}!", encoding="utf-8")
    result = _run(data_dir, "template", "import", str(path.parent), json_mode=True)
    assert result.exit_code == ExitCode.OK, result.output
    second = json.loads(result.stdout)
    assert (second["status"], second["template"]) == ("imported", "demo@2")
    assert second["spec_hash"] != first["spec_hash"]


def test_import_reports_every_layout_error_at_once(data_dir: Path, tmp_path: Path) -> None:
    path = tmp_path / "bad.toml"
    text = (FIXTURES_DIR / "bad-anchor.toml").read_text(encoding="utf-8")
    path.write_text(text.replace("size_px = 120", "size_px = -1"), encoding="utf-8")
    path.with_suffix(".j2").write_text("{{ video.title }}", encoding="utf-8")
    result = _run(data_dir, "template", "import", str(path))
    assert result.exit_code == ExitCode.USAGE
    assert "title.anchor" in result.stderr
    assert "title.size_px" in result.stderr


def test_import_rejects_a_jinja_syntax_error_with_its_line(data_dir: Path, tmp_path: Path) -> None:
    path = _pair(tmp_path / "src", prompt="fine\n{% if video.title %}")
    result = _run(data_dir, "template", "import", str(path))
    assert result.exit_code == ExitCode.USAGE
    assert "line 2" in result.stderr
    assert [r for r in _rows(data_dir) if r[0] == "demo"] == []


def test_import_of_a_missing_path_exits_2(data_dir: Path, tmp_path: Path) -> None:
    result = _run(data_dir, "template", "import", str(tmp_path / "nothing"))
    assert result.exit_code == ExitCode.USAGE


def _config_templates(isolate_user_environment: Path) -> Path:
    return isolate_user_environment / "config" / "templates"


def test_new_copies_minimal_by_default_and_the_copy_validates_and_imports(
    data_dir: Path, isolate_user_environment: Path
) -> None:
    result = _run(data_dir, "template", "new", "mine")
    assert result.exit_code == ExitCode.OK, result.output
    directory = _config_templates(isolate_user_environment)
    toml_path, j2_path = directory / "mine.toml", directory / "mine.j2"
    assert 'name = "mine"' in toml_path.read_text(encoding="utf-8")
    shown = json.loads(_run(data_dir, "template", "show", "minimal", json_mode=True).stdout)
    assert j2_path.read_text(encoding="utf-8") == shown["prompt"]

    validated = _run(data_dir, "template", "validate", str(toml_path), json_mode=True)
    assert validated.exit_code == ExitCode.OK, validated.output
    assert json.loads(validated.stdout)["template"] == "mine"
    imported = _run(data_dir, "template", "import", str(toml_path), json_mode=True)
    assert imported.exit_code == ExitCode.OK, imported.output
    assert json.loads(imported.stdout)["template"] == "mine@1"


def test_new_from_a_stored_version(
    data_dir: Path, isolate_user_environment: Path, tmp_path: Path
) -> None:
    path = _pair(tmp_path / "src", prompt="first")
    _run(data_dir, "template", "import", str(path))
    path.with_suffix(".j2").write_text("second", encoding="utf-8")
    _run(data_dir, "template", "import", str(path))
    result = _run(data_dir, "template", "new", "copy", "--from", "demo@1", json_mode=True)
    assert result.exit_code == ExitCode.OK, result.output
    assert json.loads(result.stdout)["from"] == "demo@1"
    j2_path = _config_templates(isolate_user_environment) / "copy.j2"
    assert j2_path.read_text(encoding="utf-8") == "first"


def test_new_refuses_to_overwrite(data_dir: Path, isolate_user_environment: Path) -> None:
    assert _run(data_dir, "template", "new", "mine").exit_code == ExitCode.OK
    result = _run(data_dir, "template", "new", "mine", "--from", "bold-title")
    assert result.exit_code == ExitCode.USAGE
    toml_text = (_config_templates(isolate_user_environment) / "mine.toml").read_text("utf-8")
    assert "size_px = 96" in toml_text


def test_new_from_an_unknown_template_exits_3(data_dir: Path) -> None:
    assert _run(data_dir, "template", "new", "mine", "--from", "nope").exit_code == 3


@pytest.mark.parametrize("name", ["a/b", "a@1", "../up"])
def test_new_rejects_a_name_that_is_a_path_or_a_reference(
    data_dir: Path, isolate_user_environment: Path, name: str
) -> None:
    assert _run(data_dir, "template", "new", name).exit_code == ExitCode.USAGE
    assert not _config_templates(isolate_user_environment).exists()


def test_validate_checks_the_sibling_prompt_for_jinja_syntax(tmp_path: Path) -> None:
    path = _pair(tmp_path, prompt="ok\nstill ok\n{{ video.title ")
    result = runner.invoke(app, ["template", "validate", str(path)])
    assert result.exit_code == ExitCode.USAGE
    assert "line 3" in result.stderr
