"""`fit_to`: cover the target, centre-crop, never distort (ROADMAP P5.1)."""

from __future__ import annotations

import pytest
from PIL import Image

from thumbforge.imaging.fit import fit_to

RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)


@pytest.mark.parametrize(
    ("src_size", "target"),
    [
        ((1376, 768), (1920, 1080)),  # Antigravity's native size (spike S3): upscale
        ((4000, 1000), (1920, 1080)),  # much wider: crops the sides
        ((1080, 1920), (1920, 1080)),  # portrait: crops top and bottom
        ((3840, 2160), (1920, 1080)),  # exact 16:9 downscale
        ((579, 326), (1920, 1080)),  # 579 * scale == 1919.9999…: truncation would lose a column
        ((800, 600), (500, 500)),
    ],
)
def test_result_is_exactly_the_target_size_with_no_padding(
    src_size: tuple[int, int], target: tuple[int, int]
) -> None:
    # Pillow's crop pads out-of-bounds areas with black instead of failing, so a scaled
    # image one pixel short still has the right size; only the corners give it away.
    result = fit_to(Image.new("RGB", src_size, GREEN), *target)
    assert (result.size, result.mode) == (target, "RGB")
    w, h = target
    assert {result.getpixel(xy) for xy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]} == {
        GREEN
    }


def test_source_at_target_size_keeps_its_pixels() -> None:
    src = Image.effect_noise((1920, 1080), 64).convert("RGB")
    assert fit_to(src, 1920, 1080).tobytes() == src.tobytes()


@pytest.mark.parametrize("mode", ["RGBA", "L", "P", "CMYK"])
def test_non_rgb_input_comes_out_rgb(mode: str) -> None:
    assert fit_to(Image.new(mode, (800, 600)), 400, 300).mode == "RGB"


def _stripes(size: tuple[int, int], *, vertical: bool) -> Image.Image:
    """Three equal bands, red / green / blue, left to right or top to bottom."""
    img = Image.new("RGB", size)
    w, h = size
    for i, colour in enumerate((RED, GREEN, BLUE)):
        box = (
            (i * w // 3, 0, (i + 1) * w // 3, h)
            if vertical
            else (0, i * h // 3, w, (i + 1) * h // 3)
        )
        img.paste(colour, box)
    return img


@pytest.mark.parametrize(("size", "vertical"), [((300, 100), True), ((100, 300), False)])
def test_crop_keeps_the_centre(size: tuple[int, int], *, vertical: bool) -> None:
    result = fit_to(_stripes(size, vertical=vertical), 100, 100)
    assert result.getpixel((0, 0)) == GREEN
    assert result.getpixel((99, 99)) == GREEN
