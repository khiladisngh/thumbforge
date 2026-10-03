"""`overlay`: deterministic title and Part badge drawn from a `LayoutSpec`."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest
from PIL import Image, ImageChops
from structlog.testing import capture_logs

from thumbforge.core.layout import Anchor, LayoutSpec
from thumbforge.imaging.fonts import resolve_font
from thumbforge.imaging.overlay import _layout_title, overlay  # pyright: ignore[reportPrivateUsage]

if TYPE_CHECKING:
    from collections.abc import Callable

    from structlog.typing import EventDict

TESTS = Path(__file__).parent.parent
FLAT_GREY = TESTS / "fixtures" / "imaging" / "flat-grey.png"
GOLDEN = TESTS / "golden" / "overlay"

TITLE = "Ownership explained"
FORTY_WORDS = " ".join(f"word{i:02d}" for i in range(40))

BOLD_TITLE: dict[str, Any] = {
    "template": {"name": "bold-title"},
    "canvas": {"width": 1920, "height": 1080, "safe_margin_px": 64},
    "title": {
        "font": "Inter-Bold",
        "max_lines": 2,
        "size_px": 160,
        "min_size_px": 96,
        "color": "#FFFFFF",
        "stroke_px": 8,
        "stroke_color": "#000000",
        "anchor": "bottom-left",
        "box": {"x": 96, "y": 560, "w": 1728, "h": 440},
        "case": "upper",
    },
    "part": {"enabled": False, "font": "Inter-Bold", "size_px": 72},
    "negative_space": {"hint": "lower half"},
}

SERIES_PARTS: dict[str, Any] = {
    "template": {"name": "series-parts"},
    "canvas": {"width": 1920, "height": 1080, "safe_margin_px": 64},
    "title": {
        "font": "Inter-Bold",
        "max_lines": 2,
        "size_px": 128,
        "min_size_px": 72,
        "color": "#FFFFFF",
        "stroke_px": 6,
        "stroke_color": "#101010",
        "anchor": "bottom-center",
        "box": {"x": 160, "y": 680, "w": 1600, "h": 336},
        "case": "title",
    },
    "part": {
        "format": "PART {n}",
        "font": "Inter-Bold",
        "size_px": 72,
        "anchor": "top-right",
        "badge": {"fill": "#FFD400", "padding_px": 24, "radius_px": 16},
    },
    "negative_space": {"hint": "bottom third"},
}


def _layout(
    base: dict[str, Any],
    *,
    title: dict[str, Any] | None = None,
    part: dict[str, Any] | None = None,
) -> LayoutSpec:
    """`base` with its `title` / `part` tables shallow-merged with the overrides."""
    data = {
        **base,
        "title": {**base["title"], **(title or {})},
        "part": {**base["part"], **(part or {})},
    }
    return LayoutSpec.model_validate(data)


def _grey() -> Image.Image:
    with Image.open(FLAT_GREY) as img:
        return img.convert("RGB")


def _render(
    layout: LayoutSpec,
    *,
    title: str = TITLE,
    part_number: int | None = None,
    part_label: str | None = None,
) -> Image.Image:
    return overlay(_grey(), layout, title=title, part_number=part_number, part_label=part_label)


def _ink(img: Image.Image, base: Image.Image) -> tuple[int, int, int, int]:
    """Bounding box of every pixel that differs from `base`."""
    bbox = ImageChops.difference(img, base).getbbox()
    assert bbox is not None, "nothing was drawn"
    return bbox


def _warnings(logs: list[EventDict]) -> list[EventDict]:
    return [e for e in logs if e["log_level"] == "warning"]


# --- golden -------------------------------------------------------------------------------


@pytest.mark.golden
def test_bold_title_golden(assert_golden: Callable[[Image.Image, Path], None]) -> None:
    assert_golden(_render(_layout(BOLD_TITLE)), GOLDEN / "bold-title-ownership.png")


@pytest.mark.golden
def test_series_parts_golden(assert_golden: Callable[[Image.Image, Path], None]) -> None:
    img = _render(_layout(SERIES_PARTS), part_number=7)
    assert_golden(img, GOLDEN / "series-parts-ownership-part-7.png")


# --- title layout ---------------------------------------------------------------------------


def test_too_long_title_renders_at_min_size_with_an_ellipsis_and_one_warning() -> None:
    # 160 -> 90 is not a multiple of 4: the last size tried must still be exactly 90.
    layout = _layout(BOLD_TITLE, title={"max_lines": 3, "min_size_px": 90})
    font, lines = _layout_title(FORTY_WORDS, layout.title)

    assert font.size == 90
    assert len(lines) == 3
    assert lines[-1].endswith("…")
    width = layout.title.box.w - 2 * layout.title.stroke_px
    assert all(font.getlength(line) <= width for line in lines)

    with capture_logs() as logs:
        _render(layout, title=FORTY_WORDS)
    [event] = _warnings(logs)
    assert event["event"] == "overlay.title_truncated"
    assert (event["size_px"], event["max_lines"]) == (90, 3)
    assert "word" not in repr(logs).lower()


def test_single_word_wider_than_the_box_is_cut_by_characters() -> None:
    word = "SUPERCALIFRAGILISTICEXPIALIDOCIOUS"
    layout = _layout(BOLD_TITLE, title={"box": {"x": 96, "y": 560, "w": 400, "h": 440}})
    font, [line] = _layout_title(word.lower(), layout.title)
    width = 400 - 2 * layout.title.stroke_px
    kept = line.removesuffix("…")
    assert font.size == layout.title.min_size_px
    assert line.endswith("…") and kept and word.startswith(kept)
    # As many characters as fit: one more would overflow.
    assert font.getlength(line) <= width < font.getlength(word[: len(kept) + 1] + "…")


def test_over_wide_word_is_cut_in_place_and_later_words_keep_their_line() -> None:
    word = "X" * 40
    layout = _layout(BOLD_TITLE, title={"max_lines": 3, "case": "none"})
    font, lines = _layout_title(f"A {word} b c d", layout.title)
    assert font.size == layout.title.min_size_px
    first, second, third = lines
    assert first == "A"
    assert second.endswith("…") and word.startswith(second.removesuffix("…"))
    assert third == "b c d"


def test_cut_last_word_leaves_no_bare_ellipsis_line() -> None:
    layout = _layout(BOLD_TITLE, title={"max_lines": 3, "case": "none"})
    _, lines = _layout_title("A " + "X" * 40, layout.title)
    assert lines[0] == "A"
    assert "…" not in lines


def test_box_shorter_than_a_line_still_takes_one_line_without_truncating() -> None:
    box = {"x": 96, "y": 900, "w": 1728, "h": 50}  # far less than one line at min_size_px
    layout = _layout(BOLD_TITLE, title={"box": box, "case": "none"})
    with capture_logs() as logs:
        _, lines = _layout_title("Hi", layout.title)
    assert lines == ["Hi"]
    assert _warnings(logs) == []


@pytest.mark.parametrize("anchor", ["top-left", "bottom-left"])
def test_stroked_descenders_stay_inside_the_box(anchor: str) -> None:
    # Descenders plus an 8 px stroke: the ink must not cross box.y or box.y + box.h (1000).
    layout = _layout(
        BOLD_TITLE,
        title={"anchor": anchor, "case": "none", "max_lines": 1, "stroke_px": 8},
    )
    box = layout.title.box
    _, top, _, bottom = _ink(_render(layout, title="Typography gyp"), _grey())
    assert box.y <= top
    assert bottom <= box.y + box.h


def test_title_shrinks_in_4px_steps_to_the_first_size_that_fits() -> None:
    layout = _layout(BOLD_TITLE, title={"max_lines": 1})
    block = layout.title
    font, lines = _layout_title(TITLE, block)

    assert block.min_size_px < font.size < block.size_px
    assert (block.size_px - font.size) % 4 == 0
    assert lines == [TITLE.upper()]
    # One step larger would not have fitted on one line.
    bigger = resolve_font(block.font, int(font.size) + 4)
    assert bigger.getlength(lines[0]) > block.box.w - 2 * block.stroke_px


def test_title_that_fits_logs_no_warning() -> None:
    with capture_logs() as logs:
        _render(_layout(BOLD_TITLE))
    assert _warnings(logs) == []


@pytest.mark.parametrize(
    ("case", "expected"),
    [("none", ["the rUST book"]), ("upper", ["THE RUST BOOK"]), ("title", ["The RUST Book"])],
)
def test_title_case(case: str, expected: list[str]) -> None:
    layout = _layout(BOLD_TITLE, title={"case": case, "max_lines": 1})
    _, lines = _layout_title("the  rUST book", layout.title)
    assert lines == expected


@pytest.mark.parametrize("override", [{"title": "   "}, {"layout": {"enabled": False}}])
def test_no_title_is_drawn_when_blank_or_disabled(override: dict[str, Any]) -> None:
    layout = _layout(BOLD_TITLE, title=override.get("layout"))
    img = _render(layout, title=override.get("title", TITLE))
    assert img.tobytes() == _grey().tobytes()


def test_title_stays_in_its_box_and_follows_the_anchor() -> None:
    base = _grey()
    centres: dict[Anchor, tuple[float, float]] = {}
    for anchor in Anchor:
        layout = _layout(
            BOLD_TITLE,
            title={"anchor": anchor.value, "max_lines": 1, "size_px": 96, "min_size_px": 96},
        )
        box = layout.title.box
        left, top, right, bottom = _ink(_render(layout, title="Ownership"), base)
        assert box.x <= left and right <= box.x + box.w
        assert box.y <= top and bottom <= box.y + box.h
        centres[anchor] = ((left + right) / 2, (top + bottom) / 2)

    x = {a: c[0] for a, c in centres.items()}
    y = {a: c[1] for a, c in centres.items()}
    assert x[Anchor.TOP_LEFT] < x[Anchor.TOP_CENTER] < x[Anchor.TOP_RIGHT]
    assert x[Anchor.BOTTOM_LEFT] < x[Anchor.CENTER] < x[Anchor.CENTER_RIGHT]
    assert y[Anchor.TOP_LEFT] < y[Anchor.CENTER_LEFT] < y[Anchor.BOTTOM_LEFT]
    assert y[Anchor.TOP_RIGHT] < y[Anchor.CENTER] < y[Anchor.BOTTOM_CENTER]


# --- part badge ---------------------------------------------------------------------------


def test_badge_is_absent_without_a_part_number_or_when_disabled() -> None:
    title_only = _render(_layout(SERIES_PARTS, part={"enabled": False}), part_number=7)
    assert _render(_layout(SERIES_PARTS), part_number=None).tobytes() == title_only.tobytes()
    # A format that resolves to nothing draws no empty badge.
    empty = _render(_layout(SERIES_PARTS, part={"format": "{label}"}), part_number=7)
    assert empty.tobytes() == title_only.tobytes()
    assert _render(_layout(SERIES_PARTS), part_number=7).tobytes() != title_only.tobytes()


@pytest.mark.parametrize(
    ("fmt", "label", "literal"),
    [
        ("{label} {n}", "EP", "EP 7"),
        ("{label} {n}", None, "7"),
        ("{label} {n}", "", "7"),
        ("PART {n} {unknown}", None, "PART 7 {unknown}"),  # user data, not a format string
    ],
)
def test_badge_text_substitution(fmt: str, label: str | None, literal: str) -> None:
    actual = _render(_layout(SERIES_PARTS, part={"format": fmt}), part_number=7, part_label=label)
    expected = _render(_layout(SERIES_PARTS, part={"format": literal}), part_number=7)
    assert actual.tobytes() == expected.tobytes()


@pytest.mark.parametrize("anchor", ["top-right", "bottom-left"])
def test_badge_sits_in_the_safe_area_corner(anchor: str) -> None:
    layout = _layout(SERIES_PARTS, title={"enabled": False}, part={"anchor": anchor})
    left, top, right, bottom = _ink(_render(layout, part_number=7), _grey())
    margin, width, height = 64, 1920, 1080
    match anchor:
        case "top-right":
            assert (top, right) == (margin, width - margin)
        case _:
            assert (left, bottom) == (margin, height - margin)


@pytest.mark.parametrize(("fill", "text"), [("#FFD400", (0, 0, 0)), ("#1A237E", (255, 255, 255))])
def test_badge_text_contrasts_with_its_fill(fill: str, text: tuple[int, int, int]) -> None:
    badge = {"fill": fill, "padding_px": 24, "radius_px": 16}
    layout = _layout(SERIES_PARTS, title={"enabled": False}, part={"badge": badge})
    img = _render(layout, part_number=7)
    region = img.crop(_ink(img, _grey()))
    colours = {c for _, c in region.getcolors(maxcolors=1 << 16) or []}
    assert text in colours


def test_badge_without_a_fill_uses_the_title_colour_and_stroke() -> None:
    layout = _layout(SERIES_PARTS, title={"enabled": False}, part={"badge": None})
    img = _render(layout, part_number=7)
    colours = {c for _, c in img.crop(_ink(img, _grey())).getcolors(maxcolors=1 << 16) or []}
    assert {(255, 255, 255), (16, 16, 16)} <= colours
    assert (255, 212, 0) not in colours


# --- image contract -------------------------------------------------------------------------


def test_input_is_not_mutated_and_output_is_a_new_rgb_image() -> None:
    src = _grey()
    before = src.tobytes()
    out = overlay(src, _layout(SERIES_PARTS), title=TITLE, part_number=7, part_label=None)
    assert src.tobytes() == before
    assert out is not src
    assert (out.mode, out.size) == ("RGB", src.size)


def test_same_inputs_give_identical_pixels() -> None:
    layout = _layout(SERIES_PARTS)
    first = _render(layout, part_number=7)
    second = _render(layout, part_number=7)
    assert first.tobytes() == second.tobytes()
