"""`resolve_face`: Latin through the primary font, other scripts through the shaped fallback."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from structlog.testing import capture_logs

from thumbforge.imaging.face import resolve_face
from thumbforge.imaging.fonts import SCRIPT_FALLBACK_FONT, resolve_font

if TYPE_CHECKING:
    from pathlib import Path

    from structlog.typing import EventDict

LATIN_TEXTS = ["Ownership explained", "PART 7 | 01 - Hindi Audiobook …", "gyp"]
HINDI = "महाभारत भाग 01 - हिंदी ऑडियोबुक"


def _uncovered(logs: list[EventDict]) -> list[EventDict]:
    return [e for e in logs if e["event"] == "fonts.uncovered"]


@pytest.mark.parametrize("text", LATIN_TEXTS)
def test_latin_text_is_measured_exactly_like_the_plain_font(tmp_path: Path, text: str) -> None:
    face = resolve_face("Inter-Bold", 96, text=text, config_dir=tmp_path)
    font = resolve_font("Inter-Bold", 96, config_dir=tmp_path)

    assert face.size == 96
    assert face.getlength(text) == font.getlength(text)
    assert face.getmetrics() == font.getmetrics()
    smaller = face.font_variant(size=60)
    assert smaller.size == 60
    assert smaller.getlength(text) == font.font_variant(size=60).getlength(text)


def test_devanagari_text_is_measured_with_the_fallback_font(tmp_path: Path) -> None:
    face = resolve_face("Inter-Bold", 96, text=HINDI, config_dir=tmp_path)
    plain = resolve_font("Inter-Bold", 96, config_dir=tmp_path)

    # Inter has no Devanagari glyphs, so the plain font measures a row of missing-glyph boxes.
    assert face.getlength("हिंदी") != plain.getlength("हिंदी")
    # The line must also leave room for the fallback's taller marks and deeper descenders.
    ascent, descent = face.getmetrics()
    assert ascent >= plain.getmetrics()[0]
    assert descent > plain.getmetrics()[1]


def test_conjuncts_are_shaped_not_spelled_out(tmp_path: Path) -> None:
    text = "कष क्ष"
    face = resolve_face("Inter-Bold", 96, text=text, config_dir=tmp_path)

    # क + virama + ष forms a half form or ligature, narrower than the two full consonants.
    assert face.getlength("क्ष") < face.getlength("क") + face.getlength("ष")


def test_a_mixed_line_is_as_long_as_its_runs_laid_end_to_end(tmp_path: Path) -> None:
    text = "Hindi | हिंदी"
    face = resolve_face("Inter-Bold", 96, text=text, config_dir=tmp_path)

    runs = face.getlength("Hindi | ") + face.getlength("हिंदी")
    assert face.getlength(text) == pytest.approx(runs)


def test_characters_no_font_covers_log_one_warning_without_the_text(tmp_path: Path) -> None:
    with capture_logs() as logs:
        resolve_face("Inter-Bold", 96, text="Hi 漢字 हिंदी", config_dir=tmp_path)
    [event] = _uncovered(logs)
    assert event["log_level"] == "warning"
    assert event["count"] == 2
    assert "漢" not in repr(logs)


@pytest.mark.parametrize("text", [*LATIN_TEXTS, HINDI])
def test_text_a_bundled_font_covers_logs_no_warning(tmp_path: Path, text: str) -> None:
    with capture_logs() as logs:
        resolve_face("Inter-Bold", 96, text=text, config_dir=tmp_path)
    assert _uncovered(logs) == []


def test_the_fallback_font_ships_with_its_licence() -> None:
    assert SCRIPT_FALLBACK_FONT.is_file()
    licence = SCRIPT_FALLBACK_FONT.with_name("OFL-NotoSansDevanagari.txt")
    assert "SIL OPEN FONT LICENSE" in licence.read_text(encoding="utf-8").upper()
