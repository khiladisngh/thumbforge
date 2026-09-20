"""`FakeProvider` behaviour the generic contract cannot express (PLAN.md §4.2, P3.2).

The contract suite checks what *every* provider owes its callers. These cover what makes
this one usable as a test double: the deliberate failure markers Phase 3's retry policy and
Phase 7's resume logic branch on, and the delay that makes concurrency observable.
"""

from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING

import pytest
from PIL import Image

from thumbforge.core.errors import ProviderPermanentError, ProviderTransientError
from thumbforge.core.providers import GenerationRequest
from thumbforge.providers.fake import FAIL_PERMANENT, FAIL_TRANSIENT, FakeProvider

if TYPE_CHECKING:
    from pathlib import Path


def _request(**overrides: object) -> GenerationRequest:
    fields: dict[str, object] = {
        "prompt": "a red bicycle",
        "width": 320,
        "height": 180,
        "idempotency_key": "k",
    }
    fields.update(overrides)
    return GenerationRequest.model_validate(fields)


async def test_transient_marker_raises_a_retryable_error(tmp_path: Path) -> None:
    """Phase 3's retry policy selects on `retryable`, so the flag is the contract."""
    with pytest.raises(ProviderTransientError) as caught:
        await FakeProvider().generate(_request(prompt=f"x {FAIL_TRANSIENT}"), workdir=tmp_path)

    assert caught.value.retryable is True


async def test_permanent_marker_raises_a_non_retryable_error(tmp_path: Path) -> None:
    """Retrying a permanent failure burns quota for a guaranteed second failure."""
    with pytest.raises(ProviderPermanentError) as caught:
        await FakeProvider().generate(_request(prompt=f"x {FAIL_PERMANENT}"), workdir=tmp_path)

    assert caught.value.retryable is False


@pytest.mark.parametrize("marker", [FAIL_TRANSIENT, FAIL_PERMANENT])
async def test_a_failed_generation_leaves_no_file(tmp_path: Path, marker: str) -> None:
    """A half-written image would make a resumed batch think the item had succeeded."""
    with pytest.raises((ProviderTransientError, ProviderPermanentError)):
        await FakeProvider().generate(_request(prompt=f"x {marker}"), workdir=tmp_path)

    assert list(tmp_path.iterdir()) == []


async def test_permanent_wins_when_both_markers_are_present(tmp_path: Path) -> None:
    """Order must be defined, and the non-retryable answer is the safe one.

    A prompt carrying both is a test setup mistake; retrying it would be the worse guess.
    """
    prompt = f"x {FAIL_TRANSIENT} {FAIL_PERMANENT}"

    with pytest.raises(ProviderPermanentError):
        await FakeProvider().generate(_request(prompt=prompt), workdir=tmp_path)


async def test_delay_is_awaited_so_calls_overlap(tmp_path: Path) -> None:
    """`delay_ms` exists to make concurrency observable, which needs a real await.

    A blocking sleep would serialise the gather and Phase 7's semaphore assertions would
    pass whatever the semaphore did.
    """
    provider = FakeProvider()
    requests = [
        _request(idempotency_key=f"k{index}", params={"delay_ms": 120}) for index in range(4)
    ]

    started = time.perf_counter()
    await asyncio.gather(*(provider.generate(req, workdir=tmp_path) for req in requests))
    elapsed = time.perf_counter() - started

    # Four 120 ms delays serialised would be ~480 ms; overlapped they are ~120 ms.
    assert elapsed < 0.4


async def test_unusable_delay_values_are_ignored(tmp_path: Path) -> None:
    """`params` is untyped JSON, so a string or a bool must not crash or sleep."""
    for delay in ("soon", True, -5, None):
        result = await FakeProvider().generate(
            _request(idempotency_key=f"k-{delay}", params={"delay_ms": delay}), workdir=tmp_path
        )
        assert result.image_path.exists()


async def test_reference_images_are_pasted_into_corners(tmp_path: Path) -> None:
    """A test asserting style anchoring needs to see the reference in the output."""
    reference = tmp_path / "ref.png"
    Image.new("RGB", (40, 30), (10, 200, 120)).save(reference)

    result = await FakeProvider().generate(
        _request(reference_images=(reference, reference)), workdir=tmp_path
    )

    with Image.open(result.image_path) as image:
        rgb = image.convert("RGB")
        assert rgb.getpixel((10, 10)) == (10, 200, 120)
        assert rgb.getpixel((rgb.width - 10, 10)) == (10, 200, 120)


async def test_workdir_is_created_if_absent(tmp_path: Path) -> None:
    """Callers pass a run-scoped directory that may not exist yet."""
    nested = tmp_path / "runs" / "01J9" / "iterations"

    result = await FakeProvider().generate(_request(), workdir=nested)

    assert result.image_path.parent == nested
    assert result.image_path.exists()


async def test_requested_size_is_honoured_exactly(tmp_path: Path) -> None:
    """The fake honours dimensions exactly, which the generic contract cannot require.

    Antigravity cannot (spike S3 measured a fixed 1376x768), so the contract suite only
    asserts the ratio is influenced. Asserting it here is what makes the fake a useful
    stand-in for Phase 5 and 6 tests that need a known-size source image.
    """
    for width, height in ((1376, 768), (1920, 1080), (640, 640)):
        result = await FakeProvider().generate(
            _request(width=width, height=height, idempotency_key=f"k{width}x{height}"),
            workdir=tmp_path,
        )
        with Image.open(result.image_path) as image:
            assert (image.width, image.height) == (width, height)


def test_fake_is_discoverable_through_the_real_registry() -> None:
    """The unpatched registry must resolve `fake` without raising.

    This is the test that would have caught declaring `fake` in both `BUILTIN` and the
    `thumbforge.providers` entry points: the two are merged, so it collided with itself and
    `keys()` raised `ProviderRegistryError` for every caller.
    """
    from thumbforge.providers import registry

    registered = registry.keys()  # a function, not a mapping — hence the local
    assert "fake" in registered
    assert isinstance(registry.get("fake"), FakeProvider)
