"""The only module allowed to write to stdout.

Every command produces one of two shapes: Rich output for humans, or a single JSON document for
machines (``--json``). ``emit`` picks between them so commands never branch on the mode
themselves.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


@dataclass(frozen=True, slots=True)
class AppContext:
    """Per-invocation state built by the root callback and stored on ``ctx.obj``."""

    console: Console
    json_mode: bool
    config_path: Any = None
    settings: Any = None


def table(
    columns: Sequence[str],
    rows: Sequence[Sequence[str]],
    *,
    title: str | None = None,
) -> Table:
    """Build a Rich table. Rendering is the caller's job via :func:`emit`."""
    rendered = Table(title=title, header_style="bold", show_lines=False)
    for column in columns:
        rendered.add_column(column)
    for row in rows:
        rendered.add_row(*row)
    return rendered


def panel(title: str, body: str) -> Panel:
    """Build a titled Rich panel."""
    return Panel(body, title=title, expand=False)


def kv(mapping: Mapping[str, Any], *, title: str | None = None) -> Table:
    """Build a two-column key/value table, the default shape for ``show``-style commands."""
    rendered = Table(title=title, box=None, show_header=False)
    rendered.add_column(style="bold cyan")
    rendered.add_column()
    for key, value in mapping.items():
        rendered.add_row(key, "" if value is None else str(value))
    return rendered


def emit(ctx: AppContext, data: Any, *, render: Callable[[], Any] | None = None) -> None:
    """Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.

    ``data`` must be JSON-serialisable; it is the machine contract. ``render`` is a thunk so the
    Rich object is never built in JSON mode.
    """
    if ctx.json_mode:
        ctx.console.print_json(json.dumps(data, default=str))
        return
    ctx.console.print(render() if render is not None else data)
