"""Turn exceptions into process exits. The only module permitted to exit the process.

Commands raise :class:`~thumbforge.core.errors.ThumbforgeError` subclasses and never call
``sys.exit``; the decorator below maps them onto the documented exit codes, prints a diagnostic to
**stderr** (stdout stays reserved for command output), and re-raises as ``typer.Exit``.
"""

from __future__ import annotations

import functools
import json
import sys
from collections.abc import Callable, Mapping

import typer
from rich.console import Console

from thumbforge.cli._render import AppContext
from thumbforge.core.errors import ExitCode, ThumbforgeError


def _app_context(args: tuple[object, ...], kwargs: Mapping[str, object]) -> AppContext | None:
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


def _is_json_mode(app_ctx: AppContext | None) -> bool:
    return app_ctx is not None and app_ctx.json_mode


def _report(app_ctx: AppContext | None, error: ThumbforgeError) -> None:
    if _is_json_mode(app_ctx):
        payload: dict[str, str | int] = {
            "error": error.code,
            "message": error.message,
            "exit_code": int(error.exit_code),
        }
        if error.hint:
            payload["hint"] = error.hint
        # Written directly rather than through Rich: `Console.print_json` pretty-prints and
        # soft-wraps at terminal width, which can split a long message across lines and break
        # whatever is parsing it.
        sys.stderr.write(json.dumps(payload) + "\n")
        sys.stderr.flush()
        return
    console = Console(stderr=True, highlight=False)
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
        try:
            return func(*args, **kwargs)
        except ThumbforgeError as error:
            # Resolved here, not before the call: the root callback populates ctx.obj as part
            # of its body, so a failure inside it would otherwise be reported with no context
            # and ignore --json.
            _report(_app_context(args, kwargs), error)
            raise typer.Exit(int(error.exit_code)) from error
        except KeyboardInterrupt as error:
            if _is_json_mode(_app_context(args, kwargs)):
                sys.stderr.write(json.dumps({"error": "interrupted", "exit_code": 130}) + "\n")
                sys.stderr.flush()
            else:
                Console(stderr=True, highlight=False).print("[yellow]interrupted[/]")
            raise typer.Exit(int(ExitCode.INTERRUPTED)) from error

    return wrapper
