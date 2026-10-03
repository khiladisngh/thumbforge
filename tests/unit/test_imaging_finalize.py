"""`render_final`: fit, overlay, encode within `max_bytes`, report (ROADMAP P5.3)."""

from __future__ import annotations

import io
import random
from typing import TYPE_CHECKING, Any, Literal

import pytest
from PIL import Image, ImageChops, ImageCms, ImageFile

from thumbforge.core.errors import TemplateError
from thumbforge.core.layout import LayoutSpec
from thumbforge.imaging import finalize
from thumbforge.imaging.finalize import _encode, render_final  # pyright: ignore[reportPrivateUsage]
from thumbforge.imaging.fit import fit_to
from thumbforge.settings import OutputSettings

if TYPE_CHECKING:
    from pathlib import Path

    from thumbforge.core.models import ComplianceReport
DEFAULT_MAX_BYTES = 2_097_152
TITLE = "Ownership explained"

LAYOUT: dict[str, Any] = {
    "template": {"name": "finalize-test"},
    "canvas": {"width": 1920, "height": 1080, "safe_margin_px": 64},
    "title": {
        "font": "Inter-Bold",
        "max_lines": 2,
        "size_px": 128,
        "min_size_px": 96,
        "color": "#FFFFFF",
        "stroke_px": 6,
        "stroke_color": "#000000",
        "anchor": "bottom-left",
        "box": {"x": 96, "y": 560, "w": 1728, "h": 440},
        "case": "upper",
    },
    "part": {"enabled": False, "font": "Inter-Bold", "size_px": 72},
    "negative_space": {"hint": "lower half"},
}


@pytest.fixture(scope="module")
def layout() -> LayoutSpec:
    return LayoutSpec.model_validate(LAYOUT)


@pytest.fixture
def flat_raw(tmp_path: Path) -> Path:
    path = tmp_path / "flat.png"
    Image.new("RGB", (1376, 768), (40, 90, 160)).save(path)
    return path


@pytest.fixture
def noise_raw(tmp_path: Path) -> Path:
    """Seeded 960x540 noise; upscaled to 1920x1080 it is smooth but still costly to compress."""
    path = tmp_path / "noise.png"
    data = random.Random(0).randbytes(960 * 540 * 3)
    Image.frombytes("RGB", (960, 540), data).save(path, compress_level=1)
    return path


@pytest.fixture
def qualities(monkeypatch: pytest.MonkeyPatch) -> list[int]:
    """Every quality `render_final` encodes at, in order; the real encoder still runs."""
    tried: list[int] = []
    real = finalize._encode  # pyright: ignore[reportPrivateUsage]

    def recording(img: Image.Image, fmt: Literal["jpeg", "png"], quality: int) -> bytes:
        tried.append(quality)
        return real(img, fmt, quality)

    monkeypatch.setattr(finalize, "_encode", recording)
    return tried


def _render(
    raw: Path, layout: LayoutSpec, output: OutputSettings, *, title: str = TITLE
) -> tuple[bytes, ComplianceReport]:
    return render_final(raw, layout, output, title=title, part_number=None, part_label=None)


def _decode(data: bytes) -> Image.Image:
    with Image.open(io.BytesIO(data)) as img:
        img.load()
        return img


def test_a_flat_raw_renders_a_compliant_1920x1080_jpeg_with_the_title(
    flat_raw: Path, layout: LayoutSpec
) -> None:
    data, report = _render(flat_raw, layout, OutputSettings())
    img = _decode(data)

    assert (img.format, img.size, img.mode) == ("JPEG", (1920, 1080), "RGB")
    assert report.ok
    assert report.bytes == len(data)
    untitled, _ = _render(flat_raw, layout, OutputSettings(), title="")
    assert ImageChops.difference(img, _decode(untitled)).getbbox() is not None


def test_an_oversize_raw_has_its_quality_lowered_until_it_fits(
    noise_raw: Path, layout: LayoutSpec
) -> None:
    with Image.open(noise_raw) as raw:
        at_q90 = _encode(fit_to(raw, 1920, 1080), "jpeg", 90)
    assert len(at_q90) > DEFAULT_MAX_BYTES, "precondition: the raw is over 2 MiB at quality 90"

    data, report = _render(noise_raw, layout, OutputSettings(quality=90))

    assert report.ok
    assert len(data) <= DEFAULT_MAX_BYTES
    assert len(data) < len(at_q90)


def test_a_raw_that_cannot_fit_is_returned_with_a_failing_report(
    noise_raw: Path, layout: LayoutSpec
) -> None:
    data, report = _render(noise_raw, layout, OutputSettings(max_bytes=10_000))

    assert report.ok is False
    assert "size" in report.violations
    assert report.bytes == len(data)
    assert _decode(data).size == (1920, 1080)


@pytest.mark.parametrize(
    ("quality", "expected"),
    [
        (90, [90, 85, 80, 75, 70, 65, 60]),  # steps of 5, stopping at the floor
        (63, [63, 60]),  # the last step is clamped to the floor
        (40, [40]),  # already below the floor: never raised to it
    ],
)
def test_quality_steps_down_by_5_to_a_floor_of_60(
    noise_raw: Path, layout: LayoutSpec, qualities: list[int], quality: int, expected: list[int]
) -> None:
    _, report = _render(noise_raw, layout, OutputSettings(quality=quality, max_bytes=10_000))

    assert qualities == expected
    assert report.violations == ["size"]


def test_an_optimized_jpeg_over_width_times_height_bytes_keeps_its_quality(
    tmp_path: Path, layout: LayoutSpec, qualities: list[int], monkeypatch: pytest.MonkeyPatch
) -> None:
    # Pillow sizes an optimized JPEG's buffer at width*height bytes, below the 2 MiB budget at
    # 1920x1080. Noise blended 74% over grey lands in between at quality 90.
    seeded = random.Random(0).randbytes(960 * 540 * 3)
    noise = Image.frombytes("RGB", (960, 540), seeded)
    raw = tmp_path / "window.png"
    Image.blend(Image.new("RGB", (960, 540), (128, 128, 128)), noise, 0.74).save(raw)
    # The expected bytes need the bigger buffer too, but render_final must not inherit it.
    with monkeypatch.context() as patch, Image.open(raw) as img:
        patch.setattr(ImageFile, "MAXBLOCK", 2 * 1920 * 1080)
        buf = io.BytesIO()
        fit_to(img, 1920, 1080).save(buf, format="JPEG", quality=90, subsampling=0, optimize=True)
    expected = buf.getvalue()
    assert 1920 * 1080 < len(expected) <= DEFAULT_MAX_BYTES, "precondition: inside the window"

    data, report = _render(raw, layout, OutputSettings(quality=90), title="")

    assert qualities == [90]
    assert data == expected
    assert report.ok


def test_png_output_is_a_compliant_png(flat_raw: Path, layout: LayoutSpec) -> None:
    data, report = _render(flat_raw, layout, OutputSettings(format="png"))

    assert report.ok
    assert report.format == "PNG"
    assert _decode(data).size == (1920, 1080)


def test_output_size_differing_from_the_canvas_is_honoured(
    flat_raw: Path, layout: LayoutSpec
) -> None:
    data, report = _render(flat_raw, layout, OutputSettings(width=1280, height=720))

    assert _decode(data).size == (1280, 720)
    assert report.ok
    assert (report.width, report.height) == (1280, 720)


def test_a_canvas_with_another_aspect_ratio_than_the_output_is_a_template_error(
    flat_raw: Path,
) -> None:
    # 4:3: the final fit to 16:9 would crop the top and bottom, title included.
    four_by_three = LayoutSpec.model_validate(
        {
            **LAYOUT,
            "canvas": {"width": 1440, "height": 1080},
            "title": {**LAYOUT["title"], "box": {"x": 96, "y": 560, "w": 1248, "h": 440}},
        }
    )

    with pytest.raises(TemplateError, match=r"1440x1080.*1920x1080") as err:
        _render(flat_raw, four_by_three, OutputSettings())
    assert err.value.hint == "use a canvas with the same aspect ratio as [output] width/height"


@pytest.mark.parametrize("fmt", ["jpeg", "png"])
def test_raw_metadata_is_stripped(
    tmp_path: Path, layout: LayoutSpec, fmt: Literal["jpeg", "png"]
) -> None:
    # A non-sRGB profile on the raw must not travel into the final and fail the colour check.
    lab = ImageCms.ImageCmsProfile(ImageCms.createProfile("LAB")).tobytes()
    raw = tmp_path / "tagged.png"
    Image.new("RGB", (1920, 1080), (40, 90, 160)).save(raw, icc_profile=lab)

    data, report = _render(raw, layout, OutputSettings(format=fmt))

    assert report.ok
    assert "icc_profile" not in _decode(data).info
