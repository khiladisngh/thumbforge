"""Turn exceptions into process exits. The only module permitted to exit the process.

Commands raise :class:`~thumbforge.core.errors.ThumbforgeError` subclasses and never call
``sys.exit``; the decorator below maps them onto the documented exit codes, prints a diagnostic to
**stderr** (stdout stays reserved for command output), and re-raises as ``typer.Exit``.
"""

from __future__ import annotations

import functools
import json
from collections.abc import Callable
from typing import Any

import typer
from rich.console import Console

from thumbforge.cli._render import AppContext
from thumbforge.core.errors import ExitCode, ThumbforgeError


def _app_context(args: tuple[Any, ...], kwargs: dict[str, Any]) -> AppContext | None:
    """Find the :class:`AppContext` the root callback stored on the Click context.

    Typer injects the context by keyword and vendors its own Click, so neither
    ``isinstance(x, click.Context)`` nor ``isinstance(x, typer.Context)`` matches the object
    actually passed. Duck-typing on the payload is the stable check.
    """
    for candidate in (*args, *kwargs.values()):
        obj = getattr(candidate, "obj", None)
        if isinstance(obj, AppContext):
            return obj
    return None


def _stderr(app_ctx: AppContext | None) -> tuple[Console, bool]:
    """Return the stderr console and whether the invocation wants JSON diagnostics."""
    json_mode = bool(app_ctx is not None and app_ctx.json_mode)
    return Console(stderr=True, no_color=json_mode, highlight=False), json_mode


def _report(app_ctx: AppContext | None, error: ThumbforgeError) -> None:
    console, json_mode = _stderr(app_ctx)
    if json_mode:
        payload: dict[str, Any] = {
            "error": error.code,
            "message": error.message,
            "exit_code": int(error.exit_code),
        }
        if error.hint:
            payload["hint"] = error.hint
        console.print_json(json.dumps(payload))
        return
    console.print(f"[bold red]{error.code}[/]: {error.message}")
    if error.hint:
        console.print(f"[dim]hint:[/] {error.hint}")


def handle_errors[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """Map ``ThumbforgeError`` and ``KeyboardInterrupt`` onto exit codes.

    Unexpected exceptions are deliberately **not** swallowed: they propagate so the traceback
    reaches the log and the user, and Typer exits ``1``.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        app_ctx = _app_context(args, kwargs)
        try:
            return func(*args, **kwargs)
        except ThumbforgeError as error:
            _report(app_ctx, error)
            raise typer.Exit(int(error.exit_code)) from error
        except KeyboardInterrupt as error:
            console, _ = _stderr(app_ctx)
            console.print("[yellow]interrupted[/]")
            raise typer.Exit(int(ExitCode.INTERRUPTED)) from error

    return wrapper
