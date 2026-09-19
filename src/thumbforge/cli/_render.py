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
from typing import TYPE_CHECKING

import typer
from rich.console import Console, RenderableType
from rich.panel import Panel
from rich.table import Table

from thumbforge.core.errors import SettingsError

if TYPE_CHECKING:
    from thumbforge.settings import Settings

type JsonValue = str | int | float | bool | Sequence[JsonValue] | Mapping[str, JsonValue] | None
"""What a command may emit in ``--json`` mode.

`Sequence`/`Mapping` rather than `list`/`dict` because the concrete types are invariant: an
ordinary `dict[str, str]` payload would not satisfy `dict[str, JsonValue]`, forcing a cast at
every call site. The looser protocols technically admit `bytes` and `range`, which `json.dumps`
rejects; `emit` lets that rejection happen loudly at runtime rather than coercing, and
`tests/unit/test_render.py` pins that behaviour.
"""


@dataclass(frozen=True, slots=True)
class AppContext:
    """Per-invocation state built by the root callback and stored on ``ctx.obj``."""

    console: Console
    json_mode: bool
    config_path: Path | None = None
    data_dir: Path | None = None
    settings: Settings | None = None
    settings_error: SettingsError | None = None

    def require_settings(self) -> Settings:
        """Return the settings, or re-raise the failure that prevented loading them.

        Commands that read configuration call this; commands that repair the file
        (``config init``, ``config set``) deliberately do not, so they keep working when
        ``config.toml`` is broken — otherwise the documented fix would be unreachable.
        """
        if self.settings_error is not None:
            raise self.settings_error
        if self.settings is None:  # pragma: no cover - the root callback always sets one
            msg = "settings were not loaded"
            raise SettingsError(msg)
        return self.settings


def get_app_context(ctx: typer.Context) -> AppContext:
    """Extract and validate the AppContext from a Typer execution context."""
    obj = ctx.obj
    if not isinstance(obj, AppContext):  # pragma: no cover - the root callback always sets it
        msg = "CLI context was not initialised"
        raise SettingsError(msg)
    return obj


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
    rendered = Table(title=title, box=None, show_header=False, pad_edge=False)
    rendered.add_column(style="bold cyan", no_wrap=True)
    rendered.add_column(overflow="fold")
    for key, value in mapping.items():
        rendered.add_row(key, "" if value is None else str(value))
    return rendered


def emit(
    ctx: AppContext,
    data: JsonValue,
    *,
    render: Callable[[], RenderableType] | None = None,
    soft_wrap: bool = True,
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
    ctx.console.print(render() if render is not None else data, soft_wrap=soft_wrap)
