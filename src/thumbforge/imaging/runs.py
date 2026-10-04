"""Split a title into runs by the font that draws each character (ADR 0019).

Pure logic: the caller says which characters each font covers, this module decides where one
font hands over to the other.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from collections.abc import Callable

_JOINERS: Final = "‌‍"
_MARKS: Final = ("Mn", "Mc", "Me")


@dataclass(frozen=True, slots=True)
class Run:
    """A stretch of text drawn by one font: the fallback when `fallback`, else the primary."""

    text: str
    fallback: bool


def split_runs(
    text: str, *, primary: Callable[[str], bool], fallback: Callable[[str], bool]
) -> list[Run]:
    """Cut `text` into maximal runs, each drawn by the font that covers its characters.

    The primary font draws what it covers; the fallback draws the rest it covers. A character
    neither covers stays with the primary, which draws its missing-glyph box. Joiners and
    combining marks follow the character they attach to when that character's font covers them,
    so a conjunct is never split between two fonts.
    """
    runs: list[Run] = []
    previous: bool | None = None
    for ch in text:
        use_fallback = _picks_fallback(ch, previous, primary, fallback)
        if runs and use_fallback == previous:
            runs[-1] = Run(runs[-1].text + ch, use_fallback)
        else:
            runs.append(Run(ch, use_fallback))
        previous = use_fallback
    return runs


def _picks_fallback(
    ch: str,
    previous: bool | None,
    primary: Callable[[str], bool],
    fallback: Callable[[str], bool],
) -> bool:
    if previous is not None and _attaches(ch) and (fallback if previous else primary)(ch):
        return previous
    return not primary(ch) and fallback(ch)


def _attaches(ch: str) -> bool:
    return ch in _JOINERS or unicodedata.category(ch) in _MARKS
