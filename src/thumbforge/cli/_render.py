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
from PIL import Image
from rich.console import Console, Group, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich_pixels import Pixels

from thumbforge.core.errors import SettingsError
from thumbforge.core.json import JsonValue

if TYPE_CHECKING:
    from thumbforge.settings import Settings


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


_EXPORT_HINT = "Copy images out with: thumbforge thumb export <run|iteration> --to PATH"


def _can_draw_pixels(console: Console) -> bool:
    """Whether ``console`` can show the coloured block characters a tile is made of."""
    return (
        console.is_terminal
        and console.color_system is not None
        and not console.no_color
        and not console.is_dumb_terminal
        and not console.legacy_windows
        and console.encoding.startswith("utf")
    )


def preview(ctx: AppContext, paths: Sequence[Path], columns: int = 2) -> None:
    """Draw ``paths`` as block-character thumbnails, ``columns`` tiles per row.

    Each tile is as wide as its grid cell, keeps the image's aspect ratio and carries the file
    name as a caption. The grid is a ``Table.grid``: ``rich.columns.Columns`` does not place
    ``Pixels`` tiles side by side.

    Falls back to a numbered path table plus the export hint when the console cannot draw
    colour (not a terminal, no colour, a non-UTF-8 encoding, dumb or legacy Windows console)
    or when any path cannot be decoded; a preview never raises for a bad image. Prints nothing
    in ``--json`` mode.
    """
    if columns < 1:
        msg = f"columns must be at least 1, got {columns}"
        raise ValueError(msg)
    if ctx.json_mode or not paths:
        return
    console = ctx.console
    tile_width = max((console.width - (columns - 1)) // columns, 8)
    tiles: list[RenderableType] = []
    try:
        if _can_draw_pixels(console):
            for path in paths:
                with Image.open(path) as image:
                    width, height = image.size
                    tile_height = max(round(tile_width * height / width), 1)
                    # rich-pixels packs two pixel rows per text line; an even height avoids a
                    # half-empty last line.
                    tile_height += tile_height % 2
                    # Shrink here, not in rich-pixels, whose nearest-neighbour resize breaks up
                    # small text; LANCZOS matches imaging.fit.
                    small = image.convert("RGB").resize(  # pyright: ignore[reportUnknownMemberType]
                        (tile_width, tile_height), Image.Resampling.LANCZOS
                    )
                pixels = Pixels.from_image(small)
                caption = Text(path.name, style="dim", no_wrap=True, overflow="ellipsis")
                tiles.append(Group(pixels, caption))
    except OSError, Image.DecompressionBombError:
        tiles = []
    if not tiles:
        rows = [(str(index), str(path)) for index, path in enumerate(paths, start=1)]
        console.print(table(["#", "path"], rows))
        console.print(Text(_EXPORT_HINT, style="dim"))
        return
    grid = Table.grid(padding=(0, 1))
    for _ in range(columns):
        grid.add_column(width=tile_width, no_wrap=True)
    for start in range(0, len(tiles), columns):
        row = tiles[start : start + columns]
        grid.add_row(*row, *[""] * (columns - len(row)))
    console.print(grid)
