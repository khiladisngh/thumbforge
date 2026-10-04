"""A title's typeface: the layout's font plus a fallback for characters it lacks (ADR 0019).

Latin text never touches the fallback: when the primary font covers every character, a `Face`
measures and draws exactly as the plain Pillow font does, so Latin goldens do not move. Only a
title with characters the primary lacks and the fallback covers is split into runs, each shaped
and laid end to end on one baseline.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache, partial
from typing import TYPE_CHECKING, Final

from thumbforge.imaging.fonts import (
    SCRIPT_FALLBACK_FONT,
    SCRIPT_FALLBACK_LANGUAGE,
    SCRIPT_FALLBACK_SCRIPT,
    font_path,
    load_font,
)
from thumbforge.imaging.runs import Run, split_runs
from thumbforge.imaging.shaping import ShapedFont, covers
from thumbforge.logging import get_logger

if TYPE_CHECKING:
    from pathlib import Path

    from PIL import ImageDraw, ImageFont

log = get_logger(__name__)

#: ``_H_ANCHORS[h_align] + "a"`` is the Pillow anchor of a line aligned left, centre or right.
_H_ANCHORS: Final = "lmr"


@cache
def _script_fallback() -> ShapedFont:
    return ShapedFont(
        SCRIPT_FALLBACK_FONT, script=SCRIPT_FALLBACK_SCRIPT, language=SCRIPT_FALLBACK_LANGUAGE
    )


@dataclass(frozen=True, slots=True)
class Face:
    """The layout's font at one size, plus the fallback when the title needs it."""

    primary: ImageFont.FreeTypeFont
    primary_path: Path
    fallback: ShapedFont | None

    @property
    def size(self) -> int:
        return int(self.primary.size)

    def font_variant(self, *, size: int) -> Face:
        return Face(self.primary.font_variant(size=size), self.primary_path, self.fallback)

    def getlength(self, text: str) -> float:
        """Width of `text` on one line."""
        fallback = self.fallback
        if fallback is None:
            return self.primary.getlength(text)
        return sum(self._run_length(run, fallback) for run in self._runs(text, fallback))

    def getmetrics(self) -> tuple[int, int]:
        """Ascent and descent of a line: the larger of each across the fonts in use."""
        ascent, descent = self.primary.getmetrics()
        if self.fallback is None:
            return ascent, descent
        fallback_ascent, fallback_descent = self.fallback.getmetrics(self.size)
        return max(ascent, fallback_ascent), max(descent, fallback_descent)

    def draw_line(
        self,
        draw: ImageDraw.ImageDraw,
        x: float,
        top: float,
        text: str,
        *,
        h_align: int,
        fill: str,
        stroke_width: int,
        stroke_fill: str,
    ) -> None:
        """Draw one line with its top at `top`; `h_align` 0, 1, 2 puts `x` left, middle, right."""
        fallback = self.fallback
        if fallback is None:
            draw.text(
                (x, top),
                text,
                font=self.primary,
                fill=fill,
                stroke_width=stroke_width,
                stroke_fill=stroke_fill,
                anchor=_H_ANCHORS[h_align] + "a",
            )
            return

        runs = self._runs(text, fallback)
        pen_start = x - self.getlength(text) * h_align / 2
        baseline = top + self.getmetrics()[0]
        # Strokes first, fills second: a glyph's stroke must not paint over its neighbour's fill.
        passes = [(stroke_fill, stroke_width), (fill, 0)] if stroke_width else [(fill, 0)]
        for ink, width in passes:
            pen = pen_start
            for run in runs:
                if run.fallback:
                    fallback.draw(
                        draw,
                        pen,
                        baseline,
                        run.text,
                        self.size,
                        fill=ink,
                        stroke_width=width,
                        stroke_fill=ink,
                    )
                else:
                    draw.text(
                        (pen, baseline),
                        run.text,
                        font=self.primary,
                        fill=ink,
                        stroke_width=width,
                        stroke_fill=ink,
                        anchor="ls",
                    )
                pen += self._run_length(run, fallback)

    def _runs(self, text: str, fallback: ShapedFont) -> list[Run]:
        return split_runs(
            text,
            primary=partial(covers, self.primary_path),
            fallback=partial(covers, fallback.path),
        )

    def _run_length(self, run: Run, fallback: ShapedFont) -> float:
        if run.fallback:
            return fallback.getlength(run.text, self.size)
        return self.primary.getlength(run.text)


def resolve_face(name: str, size_px: int, *, text: str, config_dir: Path | None = None) -> Face:
    """Load `name` at `size_px` for drawing `text`, adding the fallback font when `text` needs it.

    The font is found as `resolve_font` finds it. The fallback is attached only when the font
    lacks characters of `text` that the fallback covers. Characters neither covers are drawn as
    the font's missing-glyph box, with one ``fonts.uncovered`` warning that counts them and never
    quotes the text.
    """
    path = font_path(name, config_dir=config_dir)
    missing = [ch for ch in text if not covers(path, ch)]
    reachable = [ch for ch in missing if covers(SCRIPT_FALLBACK_FONT, ch)]
    if len(reachable) < len(missing):
        log.warning("fonts.uncovered", font=name, count=len(missing) - len(reachable))
    fallback = _script_fallback() if reachable else None
    return Face(load_font(path, size_px), path, fallback)
