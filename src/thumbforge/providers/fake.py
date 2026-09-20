"""`FakeProvider` — deterministic, offline image generation (PLAN.md §4.2, ROADMAP P3.2).

Exists so the unit, contract, retry, resume and concurrency suites can exercise the whole
pipeline with no network, no credentials and no cost. Three properties make it useful as a
test double rather than a stub:

- **Deterministic.** The same request produces byte-identical output, so a caller can assert
  on the image instead of merely asserting one exists.
- **Distinguishable.** Different prompts, seeds or sizes produce visibly different images, so
  a test that accidentally reuses a request fails rather than passing on a coincidence.
- **Failable on demand.** `[[FAIL_TRANSIENT]]` and `[[FAIL_PERMANENT]]` in the prompt raise
  the two error classes Phase 3's retry policy and Phase 7's resume logic branch on. Without
  a way to fail deliberately, neither path could be tested offline.
"""

from __future__ import annotations

import asyncio
import hashlib
import time
from typing import TYPE_CHECKING, ClassVar, Final

from PIL import Image, ImageDraw

from thumbforge.core.errors import ProviderPermanentError, ProviderTransientError
from thumbforge.core.providers import (
    Check,
    GenerationResult,
    HealthReport,
    ProviderCapabilities,
    ProviderInfo,
)

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from thumbforge.core.json import JsonValue
    from thumbforge.core.providers import GenerationRequest

#: Markers a test puts in the prompt to choose a failure mode.
FAIL_TRANSIENT: Final = "[[FAIL_TRANSIENT]]"
FAIL_PERMANENT: Final = "[[FAIL_PERMANENT]]"

#: Edge length of the reference-image thumbnails pasted into the corners.
_REFERENCE_THUMB_PX: Final = 96

_CAPABILITIES: Final = ProviderCapabilities(
    supports_reference_image=True,
    supports_seed=True,
    supports_negative_prompt=True,
    supports_aspect_ratio=True,
    max_batch=8,
    max_concurrency=8,
    output_formats=frozenset({"png"}),
)


def _digest(request: GenerationRequest) -> str:
    """Hash every input that the rendered image depends on.

    Size is included because the provider honours it: without it, two requests that differ
    only in dimensions would share a digest and a caller could not tell them apart from the
    `raw_response` alone. `negative_prompt` is included because `supports_negative_prompt`
    is advertised as `True`, and a flag that changes nothing is worse than a missing one.
    """
    parts = (
        request.prompt,
        request.negative_prompt or "",
        str(request.seed),
        f"{request.width}x{request.height}",
    )
    return hashlib.sha256("\x00".join(parts).encode()).hexdigest()


class FakeProvider:
    """Generate a deterministic placeholder image without leaving the machine."""

    key: ClassVar[str] = "fake"

    def __init__(self, config: Mapping[str, JsonValue] | None = None) -> None:
        """Accept a config mapping for registry symmetry; nothing in it is required."""
        self._config = dict(config or {})

    @property
    def capabilities(self) -> ProviderCapabilities:
        """Deliberately permissive, so callers exercise their full request-building path."""
        return _CAPABILITIES

    async def info(self) -> ProviderInfo:
        """Always authenticated: there is nothing to authenticate against."""
        from thumbforge import __version__

        return ProviderInfo(key=self.key, name="Fake", version=__version__, auth="ok")

    async def healthcheck(self) -> HealthReport:
        """Always healthy, and says why, so `provider check` output is never blank."""
        return HealthReport(
            checks=(Check(name="offline", ok=True, detail="no binary or credentials needed"),),
        )

    async def generate(self, request: GenerationRequest, *, workdir: Path) -> GenerationResult:
        """Render one deterministic PNG into `workdir`.

        Raises before doing any work when the prompt carries a failure marker, so a test
        asserting on the error cannot accidentally also produce a file.
        """
        if FAIL_PERMANENT in request.prompt:
            msg = f"fake provider asked to fail permanently via {FAIL_PERMANENT}"
            raise ProviderPermanentError(msg, hint="remove the marker from the prompt")
        if FAIL_TRANSIENT in request.prompt:
            msg = f"fake provider asked to fail transiently via {FAIL_TRANSIENT}"
            raise ProviderTransientError(msg, hint="remove the marker from the prompt")

        started = time.perf_counter()
        delay_ms = request.params.get("delay_ms", 0)
        if isinstance(delay_ms, (int, float)) and not isinstance(delay_ms, bool) and delay_ms > 0:
            # Awaited rather than slept so a semaphore-bounded caller really overlaps, which
            # is what makes Phase 7's concurrency assertions meaningful.
            await asyncio.sleep(delay_ms / 1000)

        digest = _digest(request)
        image_path = workdir / f"{request.idempotency_key}.png"
        await asyncio.to_thread(self._render, request, digest, image_path)

        return GenerationResult(
            image_path=image_path,
            provider_key=self.key,
            provider_version=(await self.info()).version,
            model=None,
            seed_used=request.seed,
            duration_ms=int((time.perf_counter() - started) * 1000),
            cost=None,
            raw_response={"digest": digest, "config": dict(self._config)},
        )

    def _render(self, request: GenerationRequest, digest: str, destination: Path) -> None:
        """Paint the image. Pure function of `request` and `digest`, so output is stable."""
        background = (
            int(digest[0:2], 16),
            int(digest[2:4], 16),
            int(digest[4:6], 16),
        )
        image = Image.new("RGB", (request.width, request.height), background)
        draw = ImageDraw.Draw(image)

        # The digest prefix is drawn so a human comparing two failures can see at a glance
        # whether the provider was given the same request twice.
        draw.text((16, 16), digest[:16], fill=_contrasting(background))

        for index, reference in enumerate(request.reference_images):
            self._paste_reference(image, reference, index)

        destination.parent.mkdir(parents=True, exist_ok=True)
        # `optimize=False` and no metadata: Pillow must not embed anything that varies
        # between runs, or byte-identical output would not hold.
        image.save(destination, format="PNG", optimize=False)

    def _paste_reference(self, image: Image.Image, reference: Path, index: int) -> None:
        """Paste one reference thumbnail into a corner, clockwise from top-left.

        A missing or unreadable reference is a permanent error rather than a silent skip: a
        caller that passed a path it cannot read has a bug, and hiding it would make the
        generated image look correct while ignoring the style anchor.
        """
        size = (_REFERENCE_THUMB_PX, _REFERENCE_THUMB_PX)
        try:
            with Image.open(reference) as opened:
                # Pillow's own stub declares `resize`'s size parameter with an `Unknown`
                # member, so pyright strict rejects the call itself. Suppressed narrowly
                # rather than restructured around a third-party stub defect.
                thumb = opened.convert("RGB").resize(size)  # pyright: ignore[reportUnknownMemberType]
        except OSError as exc:
            msg = f"reference image cannot be read: {reference}"
            raise ProviderPermanentError(msg, hint="check the path exists and is an image") from exc

        right = max(image.width - _REFERENCE_THUMB_PX, 0)
        bottom = max(image.height - _REFERENCE_THUMB_PX, 0)
        corners = ((0, 0), (right, 0), (right, bottom), (0, bottom))
        image.paste(thumb, corners[index % len(corners)])


def _contrasting(background: tuple[int, int, int]) -> tuple[int, int, int]:
    """Black on light backgrounds, white on dark, so the digest text is always legible."""
    red, green, blue = background
    luminance = 0.299 * red + 0.587 * green + 0.114 * blue
    return (0, 0, 0) if luminance > 140 else (255, 255, 255)
