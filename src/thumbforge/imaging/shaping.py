"""Shape text with HarfBuzz and draw the glyphs through Pillow's BASIC engine (ADR 0019).

Pillow's BASIC engine maps one character to one glyph, which cannot form Devanagari conjuncts or
move vowel signs. HarfBuzz does the shaping, pinned to its OpenType shaper and to an explicit
script and language so the glyphs never depend on the machine's locale. Pillow cannot draw a
glyph by id, so a copy of the font whose character map points at glyph ids lets BASIC draw each
shaped glyph exactly where HarfBuzz placed it: same FreeType, same stroke code, same pixels on
every OS, and no libraqm.
"""

from __future__ import annotations

import io
from dataclasses import dataclass
from functools import cache
from typing import TYPE_CHECKING

import uharfbuzz as hb
from PIL import ImageFont

from thumbforge.imaging.glyphfont import GLYPH_BASE, glyph_addressed_font

if TYPE_CHECKING:
    from pathlib import Path

    from PIL import ImageDraw


@dataclass(frozen=True, slots=True)
class Glyph:
    """One shaped glyph, in font units: its id, how far the pen advances, and its offset."""

    gid: int
    x_advance: int
    x_offset: int
    y_offset: int


@cache
def _hb_face(path: Path) -> hb.Face:
    # Bytes, not a memory map: a mapped font file cannot be deleted on Windows while loaded.
    return hb.Face(hb.Blob(path.read_bytes()))


@cache
def _hb_font(path: Path) -> hb.Font:
    return hb.Font(_hb_face(path))


@cache
def covers(path: Path, ch: str) -> bool:
    """Whether the font at `path` has a glyph for `ch`."""
    return _hb_font(path).get_nominal_glyph(ord(ch)) not in (None, 0)


class ShapedFont:
    """A bundled TrueType font shaped with HarfBuzz and drawn glyph by glyph."""

    def __init__(self, path: Path, *, script: str, language: str) -> None:
        self.path = path
        self._script = script
        self._language = language
        self._units_per_em = _hb_face(path).upem
        self._shaped: dict[str, tuple[Glyph, ...]] = {}
        self._fonts: dict[int, ImageFont.FreeTypeFont] = {}

    def shape(self, text: str) -> tuple[Glyph, ...]:
        """The glyphs of `text` in drawing order, in font units."""
        if (glyphs := self._shaped.get(text)) is None:
            buf = hb.Buffer()
            buf.add_str(text)
            buf.direction = "ltr"
            buf.script = self._script
            buf.language = self._language
            hb.shape(_hb_font(self.path), buf, shapers=["ot"])
            glyphs = tuple(
                Glyph(info.codepoint, pos.x_advance, pos.x_offset, pos.y_offset)
                for info, pos in zip(buf.glyph_infos, buf.glyph_positions, strict=True)
            )
            self._shaped[text] = glyphs
        return glyphs

    def getlength(self, text: str, size: int) -> float:
        """Width of `text` at `size` px."""
        return sum(glyph.x_advance for glyph in self.shape(text)) * size / self._units_per_em

    def getmetrics(self, size: int) -> tuple[int, int]:
        """Ascent and descent at `size` px."""
        return self._font(size).getmetrics()

    def draw(
        self,
        draw: ImageDraw.ImageDraw,
        x: float,
        baseline: float,
        text: str,
        size: int,
        *,
        fill: str,
        stroke_width: int = 0,
        stroke_fill: str | None = None,
    ) -> None:
        """Draw `text` with its pen starting at `x` on `baseline`; stroke as Pillow strokes."""
        font = self._font(size)
        scale = size / self._units_per_em
        for glyph in self.shape(text):
            draw.text(
                (x + glyph.x_offset * scale, baseline - glyph.y_offset * scale),
                chr(GLYPH_BASE + glyph.gid),
                font=font,
                fill=fill,
                stroke_width=stroke_width,
                stroke_fill=stroke_fill,
                anchor="ls",
            )
            x += glyph.x_advance * scale

    def _font(self, size: int) -> ImageFont.FreeTypeFont:
        if (font := self._fonts.get(size)) is None:
            font = ImageFont.truetype(
                io.BytesIO(glyph_addressed_font(self.path)),
                size,
                layout_engine=ImageFont.Layout.BASIC,
            )
            self._fonts[size] = font
        return font
