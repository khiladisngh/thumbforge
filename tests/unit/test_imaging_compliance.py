"""`check`: the YouTube compliance matrix on encoded bytes (ROADMAP P5.3)."""

from __future__ import annotations

import io
import random
from typing import Any, Literal

import pytest
from PIL import Image, ImageCms
from pydantic import ValidationError

from thumbforge.imaging.compliance import check

MIB = 1_048_576
GREY = (128, 128, 128)


def _noise(width: int, height: int, *, seed: int = 0) -> Image.Image:
    """Seeded RGB noise: deterministic, and expensive to compress."""
    return Image.frombytes(
        "RGB", (width, height), random.Random(seed).randbytes(width * height * 3)
    )


def _encode(img: Image.Image, fmt: str, **params: Any) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt, **params)
    return buf.getvalue()


def _flat(size: tuple[int, int], fmt: str = "JPEG", mode: str = "RGB", **params: Any) -> bytes:
    return _encode(Image.new(mode, size), fmt, **params)


def _icc(name: Literal["LAB", "XYZ", "sRGB"]) -> bytes:
    return ImageCms.ImageCmsProfile(ImageCms.createProfile(name)).tobytes()


def test_a_1_5_mb_1920x1080_jpeg_is_ok_and_reported_in_full() -> None:
    data = _encode(
        _noise(960, 540).resize((1920, 1080), Image.Resampling.BICUBIC), "JPEG", quality=90
    )
    assert MIB < len(data) < 2 * MIB, "precondition: a ~1.5 MB JPEG"

    report = check(data)

    assert report.ok
    assert (report.width, report.height) == (1920, 1080)
    assert report.bytes == len(data)
    assert (report.format, report.color_mode) == ("JPEG", "RGB")
    assert report.violations == []


@pytest.mark.parametrize(("size", "ok"), [((1919, 1080), True), ((1918, 1080), False)])
def test_aspect_tolerates_one_pixel_and_no_more(size: tuple[int, int], ok: bool) -> None:
    report = check(_flat(size))
    assert report.ok is ok
    assert report.violations == ([] if ok else ["aspect"])


def test_aspect_tolerates_one_pixel_of_height() -> None:
    assert check(_flat((1920, 1081))).ok
    assert check(_flat((1920, 1082))).violations == ["aspect"]


def test_a_1280x720_png_is_ok() -> None:
    report = check(_flat((1280, 720), "PNG"))
    assert report.ok
    assert report.format == "PNG"


def test_a_16_9_image_narrower_than_1280_violates_only_width() -> None:
    report = check(_flat((1024, 576), "PNG"))
    assert not report.ok
    assert report.violations == ["width"]


def test_a_jpeg_over_2_mib_violates_size_unless_max_bytes_allows_it() -> None:
    data = _encode(_noise(1920, 1080), "JPEG", quality=95, subsampling=0)
    assert len(data) > 3_000_000, "precondition: a 3 MB JPEG"

    assert check(data).violations == ["size"]
    assert check(data, max_bytes=52_428_800).ok


def test_size_limit_is_inclusive() -> None:
    data = _flat((1920, 1080))
    assert check(data, max_bytes=len(data)).ok
    assert check(data, max_bytes=len(data) - 1).violations == ["size"]


@pytest.mark.parametrize(
    ("fmt", "mode"),
    [("JPEG", "CMYK"), ("JPEG", "L"), ("PNG", "RGBA")],
)
def test_a_mode_other_than_rgb_violates_color(fmt: str, mode: str) -> None:
    report = check(_flat((1920, 1080), fmt, mode))
    assert report.color_mode == mode
    assert report.violations == ["color"]


def test_an_embedded_srgb_profile_is_ok() -> None:
    assert check(_flat((1920, 1080), icc_profile=_icc("sRGB"))).ok


@pytest.mark.parametrize(
    "profile",
    [_icc("LAB"), _icc("XYZ"), b"not an ICC profile"],
    ids=["lab", "xyz", "unreadable"],
)
def test_an_embedded_profile_other_than_srgb_violates_color(profile: bytes) -> None:
    for fmt in ("JPEG", "PNG"):
        assert check(_flat((1920, 1080), fmt, icc_profile=profile)).violations == ["color"]


@pytest.mark.parametrize("fmt", ["WEBP", "BMP"])
def test_a_format_other_than_jpeg_or_png_violates_format(fmt: str) -> None:
    # Uncompressed BMP is ~6 MB: lift the size limit so only the format is judged.
    report = check(_flat((1920, 1080), fmt), max_bytes=52_428_800)
    assert report.format == fmt
    assert report.violations == ["format"]


def test_violations_are_listed_in_matrix_order() -> None:
    # 1000x1000 RGBA WebP: wrong aspect, too narrow, wrong format, too big for 10 bytes, not RGB.
    report = check(_flat((1000, 1000), "WEBP", "RGBA"), max_bytes=10)
    assert report.violations == ["aspect", "width", "format", "size", "color"]


def test_report_is_frozen() -> None:
    report = check(_flat((1920, 1080)))
    with pytest.raises(ValidationError):
        report.ok = False  # pyright: ignore[reportAttributeAccessIssue]
