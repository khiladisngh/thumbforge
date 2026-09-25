"""Unit tests for ``thumbforge template`` CLI commands (ROADMAP P4.1, phase-4 spec)."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from thumbforge.cli.app import app
from thumbforge.core.errors import ExitCode

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


def test_template_validate_nonexistent_file(tmp_path: Path) -> None:
    result = runner.invoke(app, ["template", "validate", str(tmp_path / "missing.toml")])
    assert result.exit_code == ExitCode.USAGE
