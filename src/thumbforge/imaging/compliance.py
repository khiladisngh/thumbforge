"""Check encoded thumbnail bytes against YouTube's upload rules (ROADMAP P5.3).

The matrix is the phase 5 spec's Compliance rule: 16:9 within ±1 px, width ≥ 1280, JPEG or
PNG, at most `max_bytes`, sRGB. Only the header is read; pixels are never decoded.
"""

from __future__ import annotations

import io
from typing import Final

from PIL import Image, ImageCms

from thumbforge.core.models import ComplianceReport

#: 2 MiB, YouTube's mobile upload limit.
DEFAULT_MAX_BYTES: Final = 2_097_152
#: Project floor; YouTube's own minimum is 640.
MIN_WIDTH: Final = 1280
FORMATS: Final = frozenset({"JPEG", "PNG"})
COLOR_MODE: Final = "RGB"
#: ±1 px on either side of 16:9: ``|9w - 16h|`` is 9 per pixel of width, 16 per pixel of height.
_ASPECT_SLACK: Final = 16


def check(data: bytes, *, max_bytes: int = DEFAULT_MAX_BYTES) -> ComplianceReport:
    """Report every rule `data` breaks, as codes in the order aspect, width, format, size, color.

    Bytes Pillow cannot identify raise Pillow's own error; they are not a compliance verdict.
    """
    with Image.open(io.BytesIO(data)) as img:
        width, height = img.size
        fmt = img.format or ""
        mode = img.mode
        icc: bytes | None = img.info.get("icc_profile")

    violations: list[str] = []
    if abs(9 * width - 16 * height) > _ASPECT_SLACK:
        violations.append("aspect")
    if width < MIN_WIDTH:
        violations.append("width")
    if fmt not in FORMATS:
        violations.append("format")
    if len(data) > max_bytes:
        violations.append("size")
    if mode != COLOR_MODE or (icc and not _is_srgb(icc)):
        violations.append("color")

    return ComplianceReport(
        ok=not violations,
        width=width,
        height=height,
        bytes=len(data),
        format=fmt,
        color_mode=mode,
        violations=violations,
    )


def _is_srgb(icc: bytes) -> bool:
    """Whether the ICC profile describes itself as sRGB; an unreadable profile is not."""
    try:
        description = ImageCms.getProfileDescription(io.BytesIO(icc))
    except ImageCms.PyCMSError:
        return False
    return "srgb" in description.lower()
