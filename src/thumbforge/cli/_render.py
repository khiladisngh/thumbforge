"""The only module allowed to write to stdout.

Every command produces one of two shapes: Rich output for humans, or a single JSON document for
machines (``--json``). ``emit`` picks between them so commands never branch on the mode
themselves.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console, RenderableType
from rich.panel import Panel
from rich.table import Table

type JsonValue = str | int | float | bool | list[JsonValue] | dict[str, JsonValue] | None
"""What a command may emit in ``--json`` mode.

Deliberately `list`/`dict` rather than `Sequence`/`Mapping`: the wider protocols admit `bytes`
and `range`, which `json.dumps` rejects at runtime, so the annotation would promise more than
the serialiser accepts.
"""


@dataclass(frozen=True, slots=True)
class AppContext:
    """Per-invocation state built by the root callback and stored on ``ctx.obj``."""

    console: Console
    json_mode: bool
    config_path: Path | None = None


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


def kv(mapping: Mapping[str, object], *, title: str | None = None) -> Table:
    """Build a two-column key/value table, the default shape for ``show``-style commands."""
    rendered = Table(title=title, box=None, show_header=False)
    rendered.add_column(style="bold cyan")
    rendered.add_column()
    for key, value in mapping.items():
        rendered.add_row(key, "" if value is None else str(value))
    return rendered


def emit(
    ctx: AppContext,
    data: JsonValue,
    *,
    render: Callable[[], RenderableType] | None = None,
) -> None:
    """Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.

    ``data`` is the machine contract and must already be JSON-serialisable: no ``default=``
    coercion, so a stray ``Path`` raises here instead of silently becoming a string in output
    someone parses. ``allow_nan=False`` likewise rejects ``NaN``/``Infinity``, which are
    JavaScript literals rather than valid JSON.

    ``render`` is a thunk so the Rich object is never built in JSON mode.
    """
    if ctx.json_mode:
        ctx.console.print_json(json.dumps(data, allow_nan=False))
        return
    ctx.console.print(render() if render is not None else data)
