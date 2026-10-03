"""Resolve a layout's font name to a loaded TrueType font (ADR 0007, ADR 0008)."""

from __future__ import annotations

from pathlib import Path
from typing import Final

from PIL import ImageFont
from platformdirs import user_config_dir

from thumbforge.logging import get_logger

log = get_logger(__name__)

BUNDLED_DIR: Final = Path(__file__).parent / "fonts"
FALLBACK_FONT: Final = BUNDLED_DIR / "Inter-Bold.ttf"

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
    if not any(part in name for part in _NOT_A_STEM):
        base = (
            Path(user_config_dir("thumbforge", appauthor=False))
            if config_dir is None
            else config_dir
        )
        for candidate in (base / "fonts" / f"{name}.ttf", BUNDLED_DIR / f"{name}.ttf"):
            if candidate.is_file():
                return _load(candidate, size_px)
    log.warning("fonts.fallback", font=name, fallback=FALLBACK_FONT.stem)
    return _load(FALLBACK_FONT, size_px)


def _load(path: Path, size_px: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size_px, layout_engine=ImageFont.Layout.BASIC)
