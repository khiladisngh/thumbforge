"""Resize and centre-crop an image to an exact target size (ROADMAP P5.1)."""

from __future__ import annotations

from PIL import Image


def fit_to(img: Image.Image, width: int, height: int) -> Image.Image:
    """Scale `img` to cover `width`x`height`, then centre-crop to exactly that size, as RGB.

    Never distorts: one scale factor, `max(width/w, height/h)`, with LANCZOS. A source
    already at the target size keeps its pixels.
    """
    rgb = img if img.mode == "RGB" else img.convert("RGB")
    if rgb.size == (width, height):
        return rgb.copy()

    scale = max(width / rgb.width, height / rgb.height)
    # `round`, not `int`: 579x326 scales to 1919.9999… wide, which truncates to 1919.
    size = (round(rgb.width * scale), round(rgb.height * scale))
    scaled = rgb.resize(size, Image.Resampling.LANCZOS)  # pyright: ignore[reportUnknownMemberType]

    left = (scaled.width - width) // 2
    top = (scaled.height - height) // 2
    return scaled.crop((left, top, left + width, top + height))
