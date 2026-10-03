"""Turn raw provider art into the final thumbnail bytes plus their compliance report (P5.3).

fit to the layout canvas → overlay → fit to the output size → encode → lower JPEG quality
while over budget → check. A non-compliant result is still returned: the caller stores it for
inspection before raising (phase 5 spec, Behaviour 5). A canvas whose aspect ratio differs from
the output's is a `TemplateError`: the final fit would crop the overlay.
"""

from __future__ import annotations

import io
import threading
from contextlib import contextmanager
from typing import TYPE_CHECKING, Final, Literal

from PIL import Image, ImageFile

from thumbforge.core.errors import TemplateError
from thumbforge.imaging.compliance import check
from thumbforge.imaging.fit import fit_to
from thumbforge.imaging.overlay import overlay
from thumbforge.logging import get_logger

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

    from thumbforge.core.layout import LayoutSpec
    from thumbforge.core.models import ComplianceReport
    from thumbforge.settings import OutputSettings

log = get_logger(__name__)

QUALITY_FLOOR: Final = 60
QUALITY_STEP: Final = 5

#: Serialises changes to Pillow's process-wide `ImageFile.MAXBLOCK` (see `_encoder_buffer`).
_MAXBLOCK_LOCK: Final = threading.Lock()


def render_final(
    raw: Path,
    layout: LayoutSpec,
    output: OutputSettings,
    *,
    title: str,
    part_number: int | None,
    part_label: str | None,
) -> tuple[bytes, ComplianceReport]:
    """Render `raw` with `layout` into ``output.width`` x ``output.height`` bytes and check them.

    The overlay is drawn at canvas size, since its coordinates are canvas pixels, then rescaled
    with LANCZOS to the output size when the two differ. A JPEG over ``output.max_bytes`` is
    re-encoded `QUALITY_STEP` lower at a time, down to `QUALITY_FLOOR`; a starting quality at or
    below the floor is kept. PNG is encoded once.

    Raises `TemplateError` when ``layout.canvas`` is not the output's aspect ratio.
    """
    canvas_w, canvas_h = layout.canvas.width, layout.canvas.height
    if canvas_w * output.height != canvas_h * output.width:
        msg = (
            f"layout canvas {canvas_w}x{canvas_h} does not have the aspect ratio of the "
            f"output {output.width}x{output.height}"
        )
        raise TemplateError(
            msg, hint="use a canvas with the same aspect ratio as [output] width/height"
        )

    with Image.open(raw) as img:
        canvas = fit_to(img, canvas_w, canvas_h)
    drawn = overlay(canvas, layout, title=title, part_number=part_number, part_label=part_label)
    final = fit_to(drawn, output.width, output.height)
    # Strip metadata: Pillow's writers copy some of it (PNG: ICC profile) from `info` unasked.
    final.info.clear()

    quality = output.quality
    data = _encode(final, output.format, quality)
    while output.format == "jpeg" and len(data) > output.max_bytes and quality > QUALITY_FLOOR:
        quality = max(quality - QUALITY_STEP, QUALITY_FLOOR)
        log.debug("final.quality_lowered", quality=quality, max_bytes=output.max_bytes)
        data = _encode(final, output.format, quality)
    return data, check(data, max_bytes=output.max_bytes)


def _encode(img: Image.Image, fmt: Literal["jpeg", "png"], quality: int) -> bytes:
    """Encode per Behaviour 6: JPEG 4:4:4 with optimized Huffman tables, PNG optimized."""
    buf = io.BytesIO()
    match fmt:
        case "jpeg":
            with _encoder_buffer(2 * img.width * img.height):
                img.save(buf, format="JPEG", quality=quality, subsampling=0, optimize=True)
        case "png":
            img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


@contextmanager
def _encoder_buffer(min_bytes: int) -> Generator[None]:
    """Hold `ImageFile.MAXBLOCK` at no less than `min_bytes`, then restore it.

    An optimized JPEG must fit Pillow's encoder buffer in one piece, and Pillow sizes that
    buffer at width*height bytes below quality 95: 2,073,600 at 1920x1080, under the 2 MiB
    default budget. Larger output fails ("Suspension not allowed here"). `MAXBLOCK` is the
    buffer's floor; the lock keeps concurrent encodes from restoring it under each other.
    """
    with _MAXBLOCK_LOCK:
        previous = ImageFile.MAXBLOCK
        ImageFile.MAXBLOCK = max(previous, min_bytes)
        try:
            yield
        finally:
            ImageFile.MAXBLOCK = previous
