"""Shell completion through the real app (ROADMAP P8.3).

Typer's installed completion scripts all call the program back with `_THUMBFORGE_COMPLETE` set
and read the candidates from stdout, so driving that protocol against the real app proves what
the user sees on <TAB>. The scripts themselves are exercised per shell in the manual smoke
recorded with the user-guide page, not here.
"""

from __future__ import annotations

import re

import pytest
from typer.testing import CliRunner

from thumbforge.cli.app import app

runner = CliRunner()

ANSI = re.compile(r"\x1b\[[0-9;]*m")


def _complete(monkeypatch: pytest.MonkeyPatch, command_line: str) -> list[str]:
    """Candidates the bash completion script would offer for `command_line`."""
    words = command_line.split()
    monkeypatch.setenv("_THUMBFORGE_COMPLETE", "complete_bash")
    monkeypatch.setenv("COMP_WORDS", command_line)
    monkeypatch.setenv("COMP_CWORD", str(len(words) - 1))
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    return result.output.splitlines()


@pytest.mark.parametrize(
    ("command_line", "expected"),
    [
        ("thumbforge ba", ["batch"]),
        ("thumbforge th", ["thumb"]),
        ("thumbforge thumb ge", ["generate"]),
        ("thumbforge --ver", ["--verbose", "--version"]),
    ],
)
def test_tab_completes_commands_and_options(
    monkeypatch: pytest.MonkeyPatch, command_line: str, expected: list[str]
) -> None:
    assert _complete(monkeypatch, command_line) == expected


def test_help_advertises_the_completion_options() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    text = ANSI.sub("", result.output)
    assert "--install-completion" in text
    assert "--show-completion" in text
