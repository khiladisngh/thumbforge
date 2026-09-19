"""Root application behaviour: version, exit codes, and diagnostics from the callback itself."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from typer.testing import CliRunner

from thumbforge import __version__
from thumbforge.cli.app import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_version_flag() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == f"thumbforge {__version__}"


def test_unknown_command_is_a_usage_error() -> None:
    assert runner.invoke(app, ["nope"]).exit_code == 2


def test_broken_config_reports_json_when_json_mode_is_set(tmp_path: Path) -> None:
    """The failure happens inside the root callback, before ctx.obj is assigned.

    The diagnostic must still honour --json: the context has to be resolved when the error is
    reported, not when the command is entered.
    """
    config = tmp_path / "config.toml"
    config.write_text("[output\nbroken\n", encoding="utf-8")

    result = runner.invoke(app, ["--json", "--config", str(config), "config", "path"])

    assert result.exit_code == 2
    assert result.stdout == ""
    lines = [line for line in result.stderr.splitlines() if line.strip()]
    assert len(lines) == 1, f"diagnostic was not a single JSON line: {lines!r}"
    payload = json.loads(lines[0])
    assert payload["error"] == "settings"
    assert payload["exit_code"] == 2
    assert "not valid TOML" in payload["message"]


def test_broken_config_reports_rich_without_json_mode(tmp_path: Path) -> None:
    config = tmp_path / "config.toml"
    config.write_text("[output\nbroken\n", encoding="utf-8")

    result = runner.invoke(app, ["--config", str(config), "config", "path"])

    assert result.exit_code == 2
    assert "settings" in result.stderr
    assert "hint" in result.stderr


def test_repair_commands_work_against_a_broken_config(tmp_path: Path) -> None:
    """The hint tells users to run `config init --force`; that must actually be possible."""
    config = tmp_path / "config.toml"
    config.write_text("[output\nbroken\n", encoding="utf-8")

    # The command the error message recommends.
    forced = runner.invoke(app, ["--config", str(config), "config", "init", "--force"])
    assert forced.exit_code == 0, forced.stderr
    assert "quality = 90" in config.read_text(encoding="utf-8")

    # And the file is usable again afterwards.
    assert runner.invoke(app, ["--config", str(config), "config", "path"]).exit_code == 0


def test_config_set_also_works_against_a_broken_config(tmp_path: Path) -> None:
    """`config set` still needs a parseable file, but must fail cleanly rather than crash."""
    config = tmp_path / "config.toml"
    config.write_text("[output\nbroken\n", encoding="utf-8")

    result = runner.invoke(app, ["--config", str(config), "config", "set", "output.quality=85"])

    assert result.exit_code == 2  # the file is still unparseable, reported cleanly
    # Rich wraps at terminal width, so collapse whitespace before matching.
    assert "not valid TOML" in " ".join(result.stderr.split())
