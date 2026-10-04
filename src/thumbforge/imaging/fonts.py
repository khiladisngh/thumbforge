"""Resolve a layout's font name to a loaded TrueType font (ADR 0007, ADR 0008, ADR 0019)."""

from __future__ import annotations

from pathlib import Path
from typing import Final

from PIL import ImageFont
from platformdirs import user_config_dir

from thumbforge.logging import get_logger

log = get_logger(__name__)

BUNDLED_DIR: Final = Path(__file__).parent / "fonts"
FALLBACK_FONT: Final = BUNDLED_DIR / "Inter-Bold.ttf"

#: The one bundled font that draws what the layout's font cannot cover (ADR 0019). It is shaped
#: as Hindi: HarfBuzz needs an explicit script and language, never the machine's locale.
SCRIPT_FALLBACK_FONT: Final = BUNDLED_DIR / "NotoSansDevanagari-Bold.ttf"
SCRIPT_FALLBACK_SCRIPT: Final = "Deva"
SCRIPT_FALLBACK_LANGUAGE: Final = "hi"

#: A font name is a bare file stem. Anything that could steer the join out of the fonts
#: directory (separators, parent references, a Windows drive prefix) skips the lookups.
_NOT_A_STEM: Final = ("/", "\\", ":", "..")


def resolve_font(
    name: str, size_px: int, *, config_dir: Path | None = None
) -> ImageFont.FreeTypeFont:
    """Load `name` at `size_px`: user fonts first, then bundled fonts, then the bundled fallback.

    Lookup order: ``<config_dir>/fonts/<name>.ttf``, bundled ``imaging/fonts/<name>.ttf``,
    then bundled ``Inter-Bold.ttf`` with a ``fonts.fallback`` warning. `config_dir` defaults to
    the user config directory. Fonts load with the BASIC layout engine so rendering does not
    depend on whether libraqm is installed.
    """
    return load_font(font_path(name, config_dir=config_dir), size_px)


def font_path(name: str, *, config_dir: Path | None = None) -> Path:
    """The file `resolve_font` loads for `name`, with the same lookup order and warning."""
    if not any(part in name for part in _NOT_A_STEM):
        base = (
            Path(user_config_dir("thumbforge", appauthor=False))
            if config_dir is None
            else config_dir
        )
        for candidate in (base / "fonts" / f"{name}.ttf", BUNDLED_DIR / f"{name}.ttf"):
            if candidate.is_file():
                return candidate
    log.warning("fonts.fallback", font=name, fallback=FALLBACK_FONT.stem)
    return FALLBACK_FONT


def load_font(path: Path, size_px: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size_px, layout_engine=ImageFont.Layout.BASIC)
