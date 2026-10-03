"""Draw the title and the Part badge from a layout spec, deterministically (ADR 0008).

Coordinates are canvas pixels: the image is expected to be fitted to ``layout.canvas`` already.
Determinism rests on the bundled font and the BASIC layout engine (see :mod:`.fonts`): same
image, layout, text and font give the same pixels on every OS.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from PIL import ImageDraw

from thumbforge.core.layout import Anchor, TextCase
from thumbforge.imaging.fonts import resolve_font
from thumbforge.logging import get_logger

if TYPE_CHECKING:
    from PIL import Image, ImageFont

    from thumbforge.core.layout import LayoutSpec, TitleBlock

log = get_logger(__name__)

ELLIPSIS: Final = "…"
_SIZE_STEP_PX: Final = 4

#: Where each anchor sits on each axis: 0 = left/top, 1 = centre, 2 = right/bottom.
_ALIGN: Final[dict[Anchor, tuple[int, int]]] = {
    Anchor.TOP_LEFT: (0, 0),
    Anchor.TOP_CENTER: (1, 0),
    Anchor.TOP_RIGHT: (2, 0),
    Anchor.CENTER_LEFT: (0, 1),
    Anchor.CENTER: (1, 1),
    Anchor.CENTER_RIGHT: (2, 1),
    Anchor.BOTTOM_LEFT: (0, 2),
    Anchor.BOTTOM_CENTER: (1, 2),
    Anchor.BOTTOM_RIGHT: (2, 2),
}


def overlay(
    img: Image.Image,
    layout: LayoutSpec,
    *,
    title: str,
    part_number: int | None,
    part_label: str | None,
) -> Image.Image:
    """Return a new RGB image with the title and, when asked for, the Part badge drawn on.

    The title is drawn when ``layout.title.enabled`` and `title` is not blank; the badge when
    ``layout.part.enabled`` and `part_number` is not None. `img` is left untouched.
    """
    out = img.convert("RGB")  # a copy even when `img` is RGB already
    draw = ImageDraw.Draw(out)
    if layout.title.enabled and title.strip():
        _draw_title(draw, title, layout.title)
    if layout.part.enabled and part_number is not None:
        _draw_part(draw, layout, part_number, part_label)
    return out


def _layout_title(title: str, block: TitleBlock) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    """Pick the font size and line breaks for `title` inside ``block.box``.

    The box is inset by ``stroke_px`` on every side. Sizes go from ``size_px`` down in 4 px
    steps, ending exactly at ``min_size_px``; the first size whose greedy word wrap fits the
    width and the line budget wins. When none does, the title is cut at ``min_size_px`` with an
    ellipsis and a warning is logged. The budget is at least one line, so a box too short for
    one line at ``min_size_px`` still gets one, which then overflows the box vertically.
    """
    words = _cased(title, block.case)
    width = block.box.w - 2 * block.stroke_px
    font = resolve_font(block.font, block.size_px)
    for size in [*range(block.size_px, block.min_size_px, -_SIZE_STEP_PX), block.min_size_px]:
        if size != font.size:
            font = font.font_variant(size=size)
        lines = _wrap(words, font, width)
        if len(lines) <= _line_budget(font, block) and all(
            font.getlength(line) <= width for line in lines
        ):
            return font, lines

    lines = _truncate(words, font, width, _line_budget(font, block))
    # Never the title itself: it is user content.
    log.warning("overlay.title_truncated", size_px=block.min_size_px, max_lines=block.max_lines)
    return font, lines


def _cased(title: str, case: TextCase) -> list[str]:
    words = title.split()
    match case:
        case TextCase.NONE:
            return words
        case TextCase.UPPER:
            return [word.upper() for word in words]
        case TextCase.TITLE:
            return [word[:1].upper() + word[1:] for word in words]


def _line_height(font: ImageFont.FreeTypeFont) -> int:
    ascent, descent = font.getmetrics()
    return ascent + descent


def _line_budget(font: ImageFont.FreeTypeFont, block: TitleBlock) -> int:
    height = block.box.h - 2 * block.stroke_px
    return max(1, min(block.max_lines, height // _line_height(font)))


def _wrap(words: list[str], font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    """Greedy word wrap; a word wider than `width` still gets a line of its own."""
    lines: list[str] = []
    line = ""
    for word in words:
        candidate = f"{line} {word}" if line else word
        if line and font.getlength(candidate) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    lines.append(line)
    return lines


def _truncate(
    words: list[str], font: ImageFont.FreeTypeFont, width: int, max_lines: int
) -> list[str]:
    """Fill `max_lines` lines, cutting over-wide words in place, ellipsising the last line.

    The first ``max_lines - 1`` wrapped lines are kept; one that is over width is a single word
    and gets cut with an ellipsis. The remaining words share the last line, ellipsised when they
    do not fit; when no words remain there is no last line.
    """
    wrapped = _wrap(words, font, width)[: max_lines - 1]
    kept = [
        line if font.getlength(line) <= width else _ellipsize(line.split(), font, width)
        for line in wrapped
    ]
    rest = words[sum(len(line.split()) for line in wrapped) :]
    if not rest:
        return kept
    last = " ".join(rest)
    return [*kept, last if font.getlength(last) <= width else _ellipsize(rest, font, width)]


def _ellipsize(words: list[str], font: ImageFont.FreeTypeFont, width: int) -> str:
    """Drop trailing words, then characters of a lone word, until ``text + "…"`` fits."""
    while len(words) > 1 and font.getlength(" ".join(words) + ELLIPSIS) > width:
        words = words[:-1]
    text = " ".join(words)
    while text and font.getlength(text + ELLIPSIS) > width:
        text = text[:-1]
    return text + ELLIPSIS


def _draw_title(draw: ImageDraw.ImageDraw, title: str, block: TitleBlock) -> None:
    font, lines = _layout_title(title, block)
    line_height = _line_height(font)
    h_align, v_align = _ALIGN[block.anchor]
    box = block.box
    x = box.x + block.stroke_px + (box.w - 2 * block.stroke_px) * h_align // 2
    height = box.h - 2 * block.stroke_px
    top = box.y + block.stroke_px + (height - line_height * len(lines)) * v_align // 2
    for i, line in enumerate(lines):
        draw.text(
            (x, top + i * line_height),
            line,
            font=font,
            fill=block.color,
            stroke_width=block.stroke_px,
            stroke_fill=block.stroke_color,
            anchor="lmr"[h_align] + "a",
        )


def _part_text(fmt: str, number: int, label: str | None) -> str:
    """Fill ``{n}`` and ``{label}`` by plain replacement: layouts are user data, not format strings.

    Without a label, ``{label}`` is dropped and the whitespace around it collapsed.
    """
    text = fmt.replace("{n}", str(number))
    if "{label}" not in text:
        return text
    if label:
        return text.replace("{label}", label)
    return " ".join(text.replace("{label}", "").split())


def _draw_part(
    draw: ImageDraw.ImageDraw, layout: LayoutSpec, number: int, label: str | None
) -> None:
    part = layout.part
    text = _part_text(part.format, number, label)
    if not text:
        return
    font = resolve_font(part.font, part.size_px)
    badge = part.badge
    stroke = 0 if badge else layout.title.stroke_px
    padding = badge.padding_px if badge else 0

    # Size the block on the text's own ink box so the badge hugs the glyphs evenly.
    left, top, right, bottom = (round(v) for v in font.getbbox(text, stroke_width=stroke))
    width = right - left + 2 * padding
    height = bottom - top + 2 * padding
    canvas = layout.canvas
    margin = canvas.safe_margin_px
    h_align, v_align = _ALIGN[part.anchor]
    x0 = margin + (canvas.width - 2 * margin - width) * h_align // 2
    y0 = margin + (canvas.height - 2 * margin - height) * v_align // 2
    origin = (x0 + padding - left, y0 + padding - top)

    if badge is None:
        draw.text(
            origin,
            text,
            font=font,
            fill=layout.title.color,
            stroke_width=stroke,
            stroke_fill=layout.title.stroke_color,
        )
        return
    draw.rounded_rectangle(
        (x0, y0, x0 + width - 1, y0 + height - 1), radius=badge.radius_px, fill=badge.fill
    )
    draw.text(origin, text, font=font, fill=_contrasting(badge.fill))


def _contrasting(fill: str) -> str:
    """Black on light fills, white on dark ones, by Rec. 709 luma of the ``#RRGGBB`` fill."""
    r, g, b = (int(fill[i : i + 2], 16) for i in (1, 3, 5))
    luma = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    return "#000000" if luma >= 0.5 else "#FFFFFF"
