# pyright: basic
# fontTools ships no type information, so this one small module is not checked strictly.
"""A copy of a font that Pillow can draw glyph by glyph id (ADR 0019)."""

from __future__ import annotations

import io
from functools import cache
from typing import TYPE_CHECKING, Final

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable, table__c_m_a_p

if TYPE_CHECKING:
    from pathlib import Path

#: Supplementary Private Use Area-A: in the glyph-addressed font, glyph id `n` is `GLYPH_BASE + n`.
GLYPH_BASE: Final = 0xF0000


@cache
def glyph_addressed_font(path: Path) -> bytes:
    """The font at `path` with its character map replaced by `GLYPH_BASE + glyph id` entries.

    Nothing else changes, so FreeType renders the same outlines; Pillow's BASIC engine can then
    draw any glyph HarfBuzz picked by writing ``chr(GLYPH_BASE + gid)``.
    """
    with TTFont(str(path)) as font:
        subtable = CmapSubtable.newSubtable(12)
        subtable.platformID, subtable.platEncID, subtable.language = 3, 10, 0
        subtable.cmap = {GLYPH_BASE + gid: name for gid, name in enumerate(font.getGlyphOrder())}
        cmap = table__c_m_a_p("cmap")
        cmap.tableVersion = 0
        cmap.tables = [subtable]
        font["cmap"] = cmap
        out = io.BytesIO()
        font.save(out)
    return out.getvalue()
