"""`resolve_font`: user fonts, then bundled fonts, then the bundled fallback (logged)."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from PIL import ImageFont
from structlog.testing import capture_logs

import thumbforge.imaging
from thumbforge.imaging.fonts import resolve_font

if TYPE_CHECKING:
    from structlog.typing import EventDict

BUNDLED = Path(thumbforge.imaging.__file__).parent / "fonts" / "Inter-Bold.ttf"


def _user_font(config_dir: Path, name: str) -> Path:
    """Install a copy of the bundled font as `<config_dir>/fonts/<name>.ttf`."""
    target = config_dir / "fonts" / f"{name}.ttf"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(BUNDLED, target)
    return target


def _fallbacks(logs: list[EventDict]) -> list[EventDict]:
    return [e for e in logs if e["event"] == "fonts.fallback"]


def test_user_font_wins_over_the_bundled_font_of_the_same_name(tmp_path: Path) -> None:
    user = _user_font(tmp_path, "Inter-Bold")
    with capture_logs() as logs:
        font = resolve_font("Inter-Bold", 48, config_dir=tmp_path)
    assert Path(str(font.path)) == user
    assert _fallbacks(logs) == []


def test_user_font_is_found_by_name(tmp_path: Path) -> None:
    user = _user_font(tmp_path, "Custom")
    assert Path(str(resolve_font("Custom", 48, config_dir=tmp_path).path)) == user


def test_bundled_font_is_found_by_name_without_a_warning(tmp_path: Path) -> None:
    with capture_logs() as logs:
        font = resolve_font("Inter-Bold", 64, config_dir=tmp_path)
    assert Path(str(font.path)) == BUNDLED
    assert font.size == 64
    # BASIC layout keeps rendering independent of whether libraqm is installed.
    assert font.layout_engine == ImageFont.Layout.BASIC
    assert _fallbacks(logs) == []


def test_unknown_name_falls_back_to_the_bundled_font_with_a_warning(tmp_path: Path) -> None:
    with capture_logs() as logs:
        font = resolve_font("NoSuchFont", 40, config_dir=tmp_path)
    assert Path(str(font.path)) == BUNDLED
    assert font.size == 40
    [event] = _fallbacks(logs)
    assert event["log_level"] == "warning"


@pytest.mark.parametrize("name", ["../escaped", "sub/escaped", "sub\\escaped", "C:escaped"])
def test_name_that_is_not_a_bare_stem_uses_the_fallback(tmp_path: Path, name: str) -> None:
    # A decoy font sits where a naive `fonts / f"{name}.ttf"` join would land (when that stays
    # inside tmp_path), so only the name check keeps it out.
    config_dir = tmp_path / "config"
    decoy = config_dir / "fonts" / f"{name}.ttf"
    if decoy.resolve().is_relative_to(tmp_path.resolve()):
        decoy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(BUNDLED, decoy)
    with capture_logs() as logs:
        font = resolve_font(name, 40, config_dir=config_dir)
    assert Path(str(font.path)) == BUNDLED
    assert len(_fallbacks(logs)) == 1


def test_default_config_dir_is_the_user_config_dir(isolate_user_environment: Path) -> None:
    user = _user_font(isolate_user_environment / "config", "Custom")
    assert Path(str(resolve_font("Custom", 32).path)) == user
