"""Hindi titles through the real overlay and `render_final`: shaped, deterministic, boxed in."""

from __future__ import annotations

import io
import tomllib
import unicodedata
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest
from PIL import Image, ImageChops

import thumbforge.templates
from thumbforge.core.layout import LayoutSpec
from thumbforge.imaging.finalize import render_final
from thumbforge.imaging.overlay import _layout_title, overlay  # pyright: ignore[reportPrivateUsage]
from thumbforge.settings import OutputSettings

if TYPE_CHECKING:
    from collections.abc import Callable

TESTS = Path(__file__).parent.parent
FLAT_GREY = TESTS / "fixtures" / "imaging" / "flat-grey.png"
GOLDEN = TESTS / "golden" / "overlay"
BUILTIN = Path(thumbforge.templates.__file__).parent / "builtin"

BHAG_01 = "Mahabharat Bhag 01 - Hindi Audiobook | महाभारत भाग 01 - हिंदी ऑडियोबुक"
BHAG_02 = "Mahabharat Bhag 02 - Hindi Audiobook | महाभारत भाग 02 - हिंदी ऑडियोबुक"
BHAG_03 = "Mahabharat Bhag 03 - Hindi Audiobook | महाभारत भाग 03 - हिंदी ऑडियोबुक"
WHITE = b"\xff\xff\xff"


def _builtin(name: str, *, title: dict[str, Any] | None = None) -> LayoutSpec:
    data = tomllib.loads((BUILTIN / f"{name}.toml").read_text(encoding="utf-8"))
    data["title"] = {**data["title"], **(title or {})}
    return LayoutSpec.model_validate(data)


def _grey() -> Image.Image:
    with Image.open(FLAT_GREY) as img:
        return img.convert("RGB")


def _overlay(layout: LayoutSpec, title: str) -> Image.Image:
    return overlay(_grey(), layout, title=title, part_number=None, part_label=None)


def _final(layout: LayoutSpec, title: str, part_number: int | None) -> Image.Image:
    """The real final: raw file in, PNG bytes out, decoded again."""
    data, report = render_final(
        FLAT_GREY,
        layout,
        OutputSettings(format="png"),
        title=title,
        part_number=part_number,
        part_label=None,
    )
    assert report.ok
    with Image.open(io.BytesIO(data)) as img:
        return img.convert("RGB")


# --- golden: the real finals ----------------------------------------------------------------


@pytest.mark.golden
def test_bold_title_hindi_golden(assert_golden: Callable[[Image.Image, Path], None]) -> None:
    assert_golden(_final(_builtin("bold-title"), BHAG_01, None), GOLDEN / "bold-title-bhag-01.png")


@pytest.mark.golden
@pytest.mark.parametrize(("title", "part"), [(BHAG_02, 2), (BHAG_03, 3)])
def test_series_parts_hindi_golden(
    assert_golden: Callable[[Image.Image, Path], None], title: str, part: int
) -> None:
    img = _final(_builtin("series-parts"), title, part)
    assert_golden(img, GOLDEN / f"series-parts-bhag-{part:02d}-part-{part}.png")


@pytest.mark.golden
def test_latin_titles_still_match_the_goldens_made_before_the_fallback_font(
    assert_golden: Callable[[Image.Image, Path], None],
) -> None:
    assert_golden(
        _final(_builtin("bold-title"), "Ownership explained", None),
        GOLDEN / "bold-title-ownership.png",
    )
    assert_golden(
        _final(_builtin("series-parts"), "Ownership explained", 7),
        GOLDEN / "series-parts-ownership-part-7.png",
    )


# --- behaviour ------------------------------------------------------------------------------


def test_devanagari_is_not_drawn_as_missing_glyph_boxes() -> None:
    layout = _builtin("bold-title", title={"case": "none"})
    # Two different words of the same length: boxes would make them indistinguishable.
    assert _overlay(layout, "कखग").tobytes() != _overlay(layout, "खगघ").tobytes()


def test_a_hindi_title_stays_inside_its_box() -> None:
    layout = _builtin("bold-title")
    box = layout.title.box
    base = _grey()
    bbox = _ink(_overlay(layout, BHAG_01), base)
    left, top, right, bottom = bbox
    assert box.x <= left
    assert right <= box.x + box.w
    assert box.y <= top
    assert bottom <= box.y + box.h


def test_a_hindi_title_shrinks_to_fit_its_line_budget() -> None:
    layout = _builtin("bold-title")
    face, lines = _layout_title(BHAG_01, layout.title)
    width = layout.title.box.w - 2 * layout.title.stroke_px

    assert len(lines) <= layout.title.max_lines
    assert all(face.getlength(line) <= width for line in lines)
    assert (layout.title.size_px - face.size) % 4 == 0


def test_stroke_never_paints_over_a_neighbouring_glyph() -> None:
    # Same origin with and without the stroke: top-left anchor, box shifted by the stroke width.
    stroke = 8
    word = "महाभारत"
    bold = _builtin("bold-title", title={"case": "none", "anchor": "top-left", "max_lines": 1})
    box = bold.title.box
    shifted = {"x": box.x + stroke, "y": box.y + stroke, "w": box.w - 2 * stroke, "h": box.h}
    plain = _builtin(
        "bold-title",
        title={
            "case": "none",
            "anchor": "top-left",
            "max_lines": 1,
            "stroke_px": 0,
            "box": shifted,
        },
    )
    region = (box.x, box.y, box.x + box.w, box.y + box.h)
    stroked = _white(_overlay(bold, word).crop(region))
    unstroked = _white(_overlay(plain, word).crop(region))

    assert unstroked, "precondition: the word has opaque fill pixels"
    # The fill pass runs after every stroke pass, so no opaque fill pixel may be lost.
    assert unstroked <= stroked


@pytest.mark.parametrize("width", range(300, 700, 37))
def test_a_cut_title_never_ends_in_a_dangling_virama(width: int) -> None:
    layout = _builtin(
        "bold-title",
        title={"case": "none", "box": {"x": 96, "y": 560, "w": width, "h": 440}},
    )
    _, lines = _layout_title("क्षत्रिय" * 12, layout.title)
    last = lines[-1]
    assert last.endswith("…")
    before = last.removesuffix("…")[-1]
    assert unicodedata.combining(before) != 9
    assert before not in "‌‍"


# --- helpers --------------------------------------------------------------------------------


def _ink(img: Image.Image, base: Image.Image) -> tuple[int, int, int, int]:
    bbox = ImageChops.difference(img, base).getbbox()
    assert bbox is not None, "nothing was drawn"
    return bbox


def _white(img: Image.Image) -> set[int]:
    """Byte offsets of the pixels that are exactly the fill colour."""
    data = img.tobytes()
    return {i for i in range(0, len(data), 3) if data[i : i + 3] == WHITE}
