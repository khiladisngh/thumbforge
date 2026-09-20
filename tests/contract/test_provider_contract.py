"""Every provider must honour these, whatever it wraps (ADR 0010, ROADMAP P3.2).

Parametrised over `registry.keys()` rather than a hand-written list, so a provider added by
P3.4 — or by a third party in a test environment — is held to the same contract without
anyone remembering to add it here. That is the point of the suite: `AntigravityProvider`
cannot quietly disagree with `FakeProvider` about what `generate` returns.

Providers that need a real binary, credentials or network are marked `integration` so the
default run (`-m 'not integration'`) excludes them. Their contract is identical; only the
cost of checking it differs.
"""

from __future__ import annotations

import shutil
from typing import TYPE_CHECKING, Any

import pytest
from PIL import Image

from thumbforge.core.errors import ProviderError
from thumbforge.core.providers import (
    GenerationRequest,
    GenerationResult,
    HealthReport,
    ProviderCapabilities,
    ProviderInfo,
)
from thumbforge.providers import registry

if TYPE_CHECKING:
    from pathlib import Path

    from thumbforge.core.providers import ImageProvider

#: Providers that cannot run in the default suite, mapped to the executable they need.
#: Keyed rather than detected, because "needs a real binary" is a property of the provider.
#: The binary is named so `-m integration` *skips* on a machine without it instead of
#: failing — CI excludes these by marker, but a developer opting in should not see a
#: confusing error just because the CLI is not installed.
NEEDS_REAL_WORLD: dict[str, str] = {"antigravity": "agy"}


def _provider_params() -> list[Any]:
    """One param per registered provider, marking the ones that need the real world.

    `list[Any]` because pytest does not export a public type for `pytest.param`'s result.
    """
    registered = registry.keys()  # a function, not a mapping — hence no `.keys()` idiom
    return [
        pytest.param(
            key, id=key, marks=[pytest.mark.integration] if key in NEEDS_REAL_WORLD else []
        )
        for key in registered
    ]


@pytest.fixture(params=_provider_params())
def provider(request: pytest.FixtureRequest) -> ImageProvider:
    """A registered provider, constructed the way the CLI constructs one."""
    key = str(request.param)
    binary = NEEDS_REAL_WORLD.get(key)
    if binary is not None and shutil.which(binary) is None:
        pytest.skip(f"{key} needs {binary!r} on PATH")
    return registry.get(key)


def _request(**overrides: object) -> GenerationRequest:
    """A request every provider should be able to satisfy."""
    fields: dict[str, object] = {
        "prompt": "a plain grey square, minimal",
        "width": 1376,
        "height": 768,
        "idempotency_key": "contract",
    }
    fields.update(overrides)
    return GenerationRequest.model_validate(fields)


def test_registry_is_not_empty() -> None:
    """A green contract suite over zero providers would be meaningless."""
    assert registry.keys()


def test_capabilities_are_declared_and_self_consistent(provider: ImageProvider) -> None:
    """Callers branch on these, so a nonsensical combination is a bug in the provider."""
    capabilities = provider.capabilities

    assert isinstance(capabilities, ProviderCapabilities)
    assert capabilities.max_batch >= 1
    assert capabilities.max_concurrency >= 1
    assert capabilities.output_formats, "a provider that emits no format cannot be used"
    assert all(fmt == fmt.lower() for fmt in capabilities.output_formats), (
        "formats are compared against Pillow's lowercased names"
    )


async def test_info_reports_the_key_it_is_registered_under(provider: ImageProvider) -> None:
    """Provenance is recorded from this, so it must not disagree with the registry."""
    info = await provider.info()

    assert isinstance(info, ProviderInfo)
    assert info.key == provider.key
    assert info.name
    assert info.auth in {"ok", "missing", "unknown"}


async def test_healthcheck_reports_at_least_one_check(provider: ImageProvider) -> None:
    """`provider check` must never print an empty report: that reads as "no opinion"."""
    report = await provider.healthcheck()

    assert isinstance(report, HealthReport)
    assert report.checks
    assert report.ok == all(check.ok for check in report.checks)


async def test_generate_returns_a_real_image(provider: ImageProvider, tmp_path: Path) -> None:
    """The whole point of the interface: a file that exists and that Pillow can open."""
    result = await provider.generate(_request(), workdir=tmp_path)

    assert isinstance(result, GenerationResult)
    assert result.image_path.exists(), "image_path must name a file that was actually written"
    assert result.provider_key == provider.key
    assert result.duration_ms >= 0

    with Image.open(result.image_path) as image:
        assert image.format is not None
        assert image.format.lower() in provider.capabilities.output_formats
        assert image.width > 0
        assert image.height > 0


#: How far a provider's output ratio may sit from the requested one. Antigravity returns
#: 1376x768 (1.792) for a 16:9 request (1.778) — 0.8% off — so the bound must admit that
#: while still rejecting a provider that ignores the request entirely: spike S3 measured
#: 1024x1024 (1.0, 44% off) when the ratio was omitted from the prompt.
ASPECT_TOLERANCE = 0.05


async def test_requested_aspect_ratio_influences_the_output(
    provider: ImageProvider, tmp_path: Path
) -> None:
    """`supports_aspect_ratio` promises *influence*, not exact dimensions.

    Deliberately not an exact size assertion. `core.providers` defines the flag as "the
    requested aspect ratio influences the result … it does not promise the exact width and
    height", and Antigravity cannot honour exact dimensions at all (S3) while still
    correctly advertising the flag — so an exact assertion would fail a conforming provider.
    Phase 5 fits every result regardless of this flag; what the flag buys is that the source
    is not wildly the wrong shape.
    """
    if not provider.capabilities.supports_aspect_ratio:
        pytest.skip("provider does not claim aspect-ratio support")

    request = _request(width=1280, height=720)
    result = await provider.generate(request, workdir=tmp_path)

    wanted = request.width / request.height
    with Image.open(result.image_path) as image:
        actual = image.width / image.height

    assert abs(actual - wanted) / wanted <= ASPECT_TOLERANCE, (
        f"claims aspect support but returned {image.width}x{image.height} "
        f"({actual:.3f}) for a {wanted:.3f} request"
    )


async def test_seed_is_reported_when_supported(provider: ImageProvider, tmp_path: Path) -> None:
    """`seed_used` is what makes a run reproducible, so it must come back when honoured."""
    if not provider.capabilities.supports_seed:
        pytest.skip("provider does not claim seed support")

    result = await provider.generate(_request(seed=1234), workdir=tmp_path)

    assert result.seed_used == 1234


async def test_failures_are_provider_errors(provider: ImageProvider, tmp_path: Path) -> None:
    """Callers catch `ProviderError`; anything else escapes the CLI as a traceback.

    An unreadable reference image is the one failure that can be provoked in any provider
    claiming reference support, without provider-specific markers.
    """
    if not provider.capabilities.supports_reference_image:
        pytest.skip("provider does not claim reference-image support")

    missing = tmp_path / "does-not-exist.png"
    request = _request(reference_images=(missing,))

    with pytest.raises(ProviderError):
        await provider.generate(request, workdir=tmp_path)


async def test_generate_is_deterministic_when_seeded(
    provider: ImageProvider, tmp_path: Path
) -> None:
    """A seeded provider must repeat itself, or callers cannot assert on its output.

    Compared as bytes rather than dimensions: equal sizes would pass for two entirely
    different images, which is exactly the coincidence this is meant to exclude.
    """
    if not provider.capabilities.supports_seed:
        pytest.skip("provider does not claim seed support")

    first = await provider.generate(_request(seed=99, idempotency_key="det-a"), workdir=tmp_path)
    second = await provider.generate(_request(seed=99, idempotency_key="det-b"), workdir=tmp_path)

    assert first.image_path.read_bytes() == second.image_path.read_bytes()
