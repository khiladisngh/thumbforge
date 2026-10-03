"""`preview` draws real side-by-side image tiles, or degrades to a path listing."""

from __future__ import annotations

import io
from typing import TYPE_CHECKING

import pytest
from PIL import Image
from rich.console import Console

from thumbforge.cli._render import AppContext, preview

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

RED = (200, 40, 40)
BLUE = (40, 60, 200)
GREEN = (40, 180, 60)
HALF_BLOCKS = ("▀", "▄")
EXPORT_HINT = "thumbforge thumb export"
# 320x180 at width 60, two columns: tile width (60 - 1) // 2 = 29, height round(29 * 9/16) = 16
# pixels, and rich-pixels packs two pixel rows per text line.
TILE_LINES_AT_WIDTH_60 = 8


@pytest.fixture(autouse=True)
def _capable_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    # Rich reads TERM and NO_COLOR from the live environment; a dumb or colourless shell running
    # the suite must not decide which branch these tests exercise.
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.delenv("NO_COLOR", raising=False)


def _image(directory: Path, name: str, colour: tuple[int, int, int]) -> Path:
    path = directory / name
    Image.new("RGB", (320, 180), colour).save(path)
    return path


def _pixel_console(width: int = 60) -> Console:
    return Console(
        force_terminal=True,
        color_system="truecolor",
        width=width,
        # Rich ignores an explicit width on a dumb terminal unless the height is set too.
        height=24,
        legacy_windows=False,
        highlight=False,
        no_color=False,
    )


def _render(
    console: Console,
    paths: list[Path],
    columns: int = 2,
    *,
    json_mode: bool = False,
    captions: list[str] | None = None,
) -> str:
    ctx = AppContext(console=console, json_mode=json_mode)
    with console.capture() as captured:
        preview(ctx, paths, columns=columns, captions=captions)
    return captured.get()


def _lines_with(output: str, colour: tuple[int, int, int]) -> set[int]:
    sgr = "38;2;{};{};{}".format(*colour)
    return {index for index, line in enumerate(output.split("\n")) if sgr in line}


def test_two_tiles_share_the_same_lines(tmp_path: Path) -> None:
    # The proof that the grid is real: rich.columns.Columns stacked two Pixels tiles instead of
    # placing them side by side, so preview uses Table.grid and this asserts the outcome.
    red = _image(tmp_path, "red.png", RED)
    blue = _image(tmp_path, "blue.png", BLUE)

    output = _render(_pixel_console(), [red, blue])

    red_lines = _lines_with(output, RED)
    blue_lines = _lines_with(output, BLUE)
    assert red_lines
    assert red_lines == blue_lines
    assert len(red_lines) == TILE_LINES_AT_WIDTH_60
    assert "red.png" in output
    assert "blue.png" in output


def test_one_column_stacks_tiles(tmp_path: Path) -> None:
    red = _image(tmp_path, "red.png", RED)
    blue = _image(tmp_path, "blue.png", BLUE)

    output = _render(_pixel_console(), [red, blue], columns=1)

    red_lines = _lines_with(output, RED)
    blue_lines = _lines_with(output, BLUE)
    assert red_lines
    assert blue_lines
    assert red_lines.isdisjoint(blue_lines)
    assert max(red_lines) < min(blue_lines)


def test_odd_count_leaves_the_last_row_half_full(tmp_path: Path) -> None:
    red = _image(tmp_path, "red.png", RED)
    blue = _image(tmp_path, "blue.png", BLUE)
    green = _image(tmp_path, "green.png", GREEN)

    output = _render(_pixel_console(), [red, blue, green])

    red_lines = _lines_with(output, RED)
    green_lines = _lines_with(output, GREEN)
    assert red_lines == _lines_with(output, BLUE)
    assert len(green_lines) == TILE_LINES_AT_WIDTH_60
    assert min(green_lines) > max(red_lines)
    assert "green.png" in output


def test_json_mode_prints_nothing(tmp_path: Path) -> None:
    red = _image(tmp_path, "red.png", RED)

    assert _render(_pixel_console(), [red], json_mode=True) == ""


def _assert_fallback(output: str, paths: list[Path]) -> None:
    for path in paths:
        assert str(path) in output
    assert not any(glyph in output for glyph in HALF_BLOCKS)
    assert EXPORT_HINT in output


# Each case differs from a capable truecolor terminal in exactly one property, built inside the
# test so the environment fixture is already in place.
@pytest.mark.parametrize(
    "make_console",
    [
        pytest.param(
            lambda: Console(force_terminal=False, width=200, no_color=False),
            id="not-a-terminal",
        ),
        pytest.param(
            lambda: Console(
                force_terminal=True,
                color_system=None,
                width=200,
                legacy_windows=False,
                no_color=False,
            ),
            id="no-colour-system",
        ),
        pytest.param(
            lambda: Console(
                force_terminal=True,
                color_system="truecolor",
                width=200,
                legacy_windows=False,
                no_color=True,
            ),
            id="no-color-flag",
        ),
        pytest.param(
            lambda: Console(
                force_terminal=True,
                color_system="truecolor",
                width=200,
                legacy_windows=True,
                no_color=False,
            ),
            id="legacy-windows",
        ),
        pytest.param(
            lambda: Console(
                file=io.TextIOWrapper(io.BytesIO(), encoding="latin-1"),
                force_terminal=True,
                color_system="truecolor",
                width=200,
                legacy_windows=False,
                no_color=False,
            ),
            id="non-utf-encoding",
        ),
    ],
)
def test_incapable_console_lists_paths(tmp_path: Path, make_console: Callable[[], Console]) -> None:
    paths = [_image(tmp_path, "red.png", RED), _image(tmp_path, "blue.png", BLUE)]

    _assert_fallback(_render(make_console(), paths), paths)


def test_dumb_terminal_lists_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TERM", "dumb")
    paths = [_image(tmp_path, "red.png", RED)]

    _assert_fallback(_render(_pixel_console(width=200), paths), paths)


def test_unreadable_path_falls_back_for_the_whole_call(tmp_path: Path) -> None:
    red = _image(tmp_path, "red.png", RED)
    missing = tmp_path / "missing.png"
    not_an_image = tmp_path / "notes.png"
    not_an_image.write_text("not an image", encoding="utf-8")
    paths = [red, missing, not_an_image]

    _assert_fallback(_render(_pixel_console(width=200), paths), paths)


def test_columns_must_be_positive(tmp_path: Path) -> None:
    red = _image(tmp_path, "red.png", RED)

    with pytest.raises(ValueError, match="columns"):
        _render(_pixel_console(), [red], columns=0)


def test_captions_replace_the_file_names_under_the_tiles(tmp_path: Path) -> None:
    red = _image(tmp_path, "red.png", RED)
    blue = _image(tmp_path, "blue.png", BLUE)

    output = _render(_pixel_console(), [red, blue], captions=["#1 ★ ✔", "#2 ✘"])

    assert "#1 ★ ✔" in output
    assert "#2 ✘" in output
    assert "red.png" not in output
    assert "blue.png" not in output


def test_captions_lead_each_row_of_the_fallback_listing(tmp_path: Path) -> None:
    paths = [_image(tmp_path, "red.png", RED), _image(tmp_path, "blue.png", BLUE)]
    console = Console(force_terminal=False, width=200, no_color=False)

    output = _render(console, paths, captions=["#1 ★ ✔", "#2 ✘"])

    _assert_fallback(output, paths)
    assert "#1 ★ ✔" in output
    assert "#2 ✘" in output


def test_captions_must_match_the_paths(tmp_path: Path) -> None:
    red = _image(tmp_path, "red.png", RED)

    with pytest.raises(ValueError, match="captions"):
        _render(_pixel_console(), [red], captions=["one", "two"])
