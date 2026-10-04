"""`split_runs`: which font draws each stretch of a title (ADR 0019)."""

from __future__ import annotations

import pytest

from thumbforge.imaging.runs import Run, split_runs

ZWJ = "‍"
ACUTE = "́"  # a combining mark both stand-in fonts cover

BHAG_01 = "Bhag 01 - Hindi | महाभारत भाग 01 - हिंदी ऑडियोबुक"


def _primary(ch: str) -> bool:
    """Stands in for a Latin font: everything below U+0900 plus the joiner."""
    return ord(ch) < 0x0900 or ch == ZWJ


def _fallback(ch: str) -> bool:
    """Stands in for a Devanagari font: its block, the joiner and the acute accent."""
    return 0x0900 <= ord(ch) <= 0x097F or ch in (ZWJ, ACUTE)


def _runs(text: str) -> list[Run]:
    return split_runs(text, primary=_primary, fallback=_fallback)


def test_empty_text_has_no_runs() -> None:
    assert _runs("") == []


def test_text_the_primary_font_covers_is_one_run() -> None:
    assert _runs("Ownership explained | 01 - …") == [Run("Ownership explained | 01 - …", False)]


def test_text_only_the_fallback_covers_is_one_fallback_run() -> None:
    assert _runs("महाभारत") == [Run("महाभारत", True)]


def test_a_bilingual_title_alternates_runs_and_keeps_every_character() -> None:
    assert _runs(BHAG_01) == [
        Run("Bhag 01 - Hindi | ", False),
        Run("महाभारत", True),
        Run(" ", False),
        Run("भाग", True),
        Run(" 01 - ", False),
        Run("हिंदी", True),
        Run(" ", False),
        Run("ऑडियोबुक", True),
    ]
    assert "".join(run.text for run in _runs(BHAG_01)) == BHAG_01


def test_a_joiner_stays_inside_the_word_it_joins() -> None:
    # Both fonts cover the joiner; drawing it with the primary would cut the conjunct in two.
    assert _runs(f"क्{ZWJ}ष") == [Run(f"क्{ZWJ}ष", True)]
    assert _runs(f"a{ZWJ}b") == [Run(f"a{ZWJ}b", False)]


def test_a_combining_mark_follows_the_character_it_attaches_to() -> None:
    # The primary covers the acute too, but on a Devanagari base it belongs to the fallback run.
    assert _runs(f"क{ACUTE}") == [Run(f"क{ACUTE}", True)]
    assert _runs(f"e{ACUTE}") == [Run(f"e{ACUTE}", False)]


@pytest.mark.parametrize("text", ["a漢b", "漢"])
def test_a_character_no_font_covers_stays_with_the_primary(text: str) -> None:
    # It is drawn as the primary's missing-glyph box, not handed to a font that cannot draw it.
    assert _runs(text) == [Run(text, False)]
