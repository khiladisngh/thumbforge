"""The exit-code contract: a script parsing our status codes must never be surprised."""

from __future__ import annotations

import json

import pytest
import typer
from rich.console import Console
from typer.testing import CliRunner

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import AppContext
from thumbforge.core.errors import (
    ComplianceError,
    ExitCode,
    NotFoundError,
    PartialBatchError,
    ProviderAuthError,
    ProviderTimeoutError,
    ProviderTransientError,
    SettingsError,
    SourceError,
    TemplateError,
    ThumbforgeError,
)

runner = CliRunner()

CASES = [
    (SettingsError, 2),
    (TemplateError, 2),
    (NotFoundError, 3),
    (ProviderAuthError, 4),
    (ProviderTransientError, 4),
    (ProviderTimeoutError, 4),
    (ComplianceError, 5),
    (PartialBatchError, 6),
    (SourceError, 1),
]


@pytest.mark.parametrize(("error_class", "expected"), CASES)
def test_error_maps_to_documented_exit_code(
    error_class: type[ThumbforgeError], expected: int
) -> None:
    app = typer.Typer()

    @app.command()
    @handle_errors
    def boom(ctx: typer.Context) -> None:
        raise error_class("it broke", hint="try harder")

    result = runner.invoke(app, [])
    assert result.exit_code == expected


def test_hint_and_code_reach_stderr() -> None:
    app = typer.Typer()

    @app.command()
    @handle_errors
    def boom(ctx: typer.Context) -> None:
        raise NotFoundError("no such video", hint="run thumbforge fetch first")

    result = runner.invoke(app, [])
    assert result.exit_code == 3
    assert "not_found" in result.output
    assert "run thumbforge fetch first" in result.output


def test_keyboard_interrupt_exits_130() -> None:
    app = typer.Typer()

    @app.command()
    @handle_errors
    def boom(ctx: typer.Context) -> None:
        raise KeyboardInterrupt

    assert runner.invoke(app, []).exit_code == int(ExitCode.INTERRUPTED)


def test_keyboard_interrupt_in_json_mode_emits_one_line_on_stderr() -> None:
    """Ctrl-C during a batch must still leave machine mode with parseable output."""
    app = typer.Typer()

    @app.callback()
    def root(ctx: typer.Context) -> None:
        ctx.obj = AppContext(console=Console(), json_mode=True)

    @app.command()
    @handle_errors
    def boom(ctx: typer.Context) -> None:
        raise KeyboardInterrupt

    result = CliRunner().invoke(app, ["boom"])
    assert result.exit_code == int(ExitCode.INTERRUPTED)
    assert result.stdout == ""
    lines = [line for line in result.stderr.splitlines() if line.strip()]
    assert len(lines) == 1, f"diagnostic was split across lines: {lines!r}"
    assert json.loads(lines[0]) == {"error": "interrupted", "exit_code": 130}


def test_unexpected_exception_is_not_swallowed() -> None:
    app = typer.Typer()

    @app.command()
    @handle_errors
    def boom(ctx: typer.Context) -> None:
        raise ValueError("programmer error")

    result = runner.invoke(app, [])
    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)


def test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout() -> None:
    """Machine mode contract: stdout carries command output, stderr carries the diagnostic."""
    app = typer.Typer()

    @app.callback()
    def root(ctx: typer.Context) -> None:
        ctx.obj = AppContext(console=Console(), json_mode=True)

    @app.command()
    @handle_errors
    def boom(ctx: typer.Context) -> None:
        # Long enough that Rich would have soft-wrapped it across lines.
        raise ComplianceError(
            "image is 4:3 but 16:9 is required; " + "and this message keeps going " * 6,
            hint="crop to 16:9",
        )

    separated = CliRunner()
    result = separated.invoke(app, ["boom"])
    assert result.exit_code == 5
    assert result.stdout == ""

    lines = [line for line in result.stderr.splitlines() if line.strip()]
    assert len(lines) == 1, f"diagnostic was split across lines: {lines!r}"
    payload = json.loads(lines[0])
    assert payload["error"] == "compliance"
    assert payload["exit_code"] == 5
    assert payload["hint"] == "crop to 16:9"
    assert payload["message"].startswith("image is 4:3 but 16:9 is required;")


def test_only_transient_and_timeout_are_retryable() -> None:
    assert ProviderTransientError("x").retryable
    assert ProviderTimeoutError("x").retryable
    assert not ProviderAuthError("x").retryable
