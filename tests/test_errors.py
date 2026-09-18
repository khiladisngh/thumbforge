"""The exit-code contract: a script parsing our status codes must never be surprised."""

from __future__ import annotations

import json

import pytest
import typer
from typer.testing import CliRunner

from thumbforge.cli._errors import handle_errors
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


def test_unexpected_exception_is_not_swallowed() -> None:
    app = typer.Typer()

    @app.command()
    @handle_errors
    def boom(ctx: typer.Context) -> None:
        raise ValueError("programmer error")

    result = runner.invoke(app, [])
    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)


def test_json_mode_emits_machine_readable_diagnostic() -> None:
    from thumbforge.cli._render import AppContext

    app = typer.Typer()

    @app.callback()
    def root(ctx: typer.Context) -> None:
        from rich.console import Console

        ctx.obj = AppContext(console=Console(), json_mode=True)

    @app.command()
    @handle_errors
    def boom(ctx: typer.Context) -> None:
        raise ComplianceError("image is 4:3", hint="crop to 16:9")

    result = runner.invoke(app, ["boom"])
    assert result.exit_code == 5
    payload = json.loads(result.output)
    assert payload == {
        "error": "compliance",
        "message": "image is 4:3",
        "exit_code": 5,
        "hint": "crop to 16:9",
    }


def test_only_transient_and_timeout_are_retryable() -> None:
    assert ProviderTransientError("x").retryable
    assert ProviderTimeoutError("x").retryable
    assert not ProviderAuthError("x").retryable
