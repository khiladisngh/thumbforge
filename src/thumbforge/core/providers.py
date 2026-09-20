"""The `ImageProvider` Protocol and the values that cross it (ADR 0010, ROADMAP P3.1).

Lives in `core` rather than in `providers/` because `core.services` consumes these types —
`HeroService` (P6.1) builds a `GenerationRequest` and reads a `GenerationResult` — and
`core` may not import `providers`. This is the same constraint that moved `MetadataSource`
to `core/sources.py` in P2.3, and `docs/specs/phase-1-skeleton.md` pre-authorised it: *"the
contract is the rule, the file placement bends."* `providers/` keeps the registry and the
concrete adapters.

Capabilities exist so callers can degrade instead of guessing. The Antigravity spikes
(`docs/spikes/antigravity.md`) are the reason each flag is a flag rather than an assumption:
that provider cannot take a reference image, cannot be given a seed, cannot be told an exact
size, and emits only JPEG.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import ClassVar, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field, field_validator

from thumbforge.core.json import JsonPayload

# `Decimal`, `Path` and `JsonPayload` are runtime imports, not TYPE_CHECKING ones: Pydantic
# resolves a model's annotations when the class is built, so hiding them breaks import.

#: Provider auth state. `unknown` is distinct from `missing`: a provider that cannot cheaply
#: prove its credentials must not be reported as unauthenticated, or `provider check` would
#: tell users to fix something that is not broken.
type AuthState = Literal["ok", "missing", "unknown"]


class ProviderCapabilities(BaseModel):
    """What a provider can actually do, so callers degrade instead of guessing."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    supports_reference_image: bool
    supports_seed: bool
    supports_negative_prompt: bool
    #: Whether the requested aspect ratio influences the result. It does **not** promise the
    #: exact width x height: spike S3 measured Antigravity honouring "16:9 widescreen"
    #: while always returning 1376x768, so Phase 5 fits every result regardless.
    supports_aspect_ratio: bool
    #: Images per `generate` call.
    max_batch: int = Field(ge=1)
    #: Provider-side safe parallelism, measured rather than assumed (S7 put Antigravity at 2).
    max_concurrency: int = Field(ge=1)
    output_formats: frozenset[str] = Field(min_length=1)


class ProviderInfo(BaseModel):
    """Identity and auth state, for `provider list`."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    key: str = Field(min_length=1)
    name: str = Field(min_length=1)
    version: str
    auth: AuthState


class Check(BaseModel):
    """One named healthcheck outcome, with enough detail to act on a failure."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(min_length=1)
    ok: bool
    detail: str = ""


class HealthReport(BaseModel):
    """The result of `provider check`: every check, not just the first failure.

    `ok` is derived rather than supplied, so a report cannot claim health while carrying a
    failed check.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    checks: tuple[Check, ...] = ()
    models: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        """True when every check passed."""
        return all(check.ok for check in self.checks)


class Cost(BaseModel):
    """What one generation consumed.

    `credits`/`currency` are optional because a provider may not report money: spike S8
    measured Antigravity's `usage` as tokens only, with no credit, price or currency field,
    so the Phase 8 cost report falls back to tokens for it.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    tokens_in: int = Field(default=0, ge=0)
    tokens_out: int = Field(default=0, ge=0)
    credits: Decimal | None = None
    currency: str | None = None


class GenerationRequest(BaseModel):
    """One image to generate. Providers ignore what their capabilities disclaim."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    prompt: str = Field(min_length=1)
    negative_prompt: str | None = None
    width: int = Field(ge=1)
    height: int = Field(ge=1)
    reference_images: tuple[Path, ...] = ()
    seed: int | None = None
    #: Provider-specific knobs, passed through from the provider profile.
    params: JsonPayload = Field(default_factory=dict)
    #: Identifies this request for deduplication (`PLAN.md` §6); providers may use it to
    #: name their output but must not depend on the caller having stored it.
    #:
    #: Constrained to filename-safe characters because providers join it onto a path.
    #: `PLAN.md` §6 already makes it a `sha256(...)[:32]`, so nothing legitimate is excluded
    #: — but `min_length=1` alone let `"../../escaped"` through, and a provider that then
    #: created the parent directory would write outside the caller's workdir. Validating
    #: here fixes it for every provider rather than each one guarding its own join.
    idempotency_key: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9._-]+$")

    @field_validator("idempotency_key")
    @classmethod
    def _reject_traversal(cls, value: str) -> str:
        """Refuse a key that is only dots, which the character class alone would allow."""
        if set(value) <= {"."}:
            msg = "idempotency_key must contain more than dots"
            raise ValueError(msg)
        return value


class GenerationResult(BaseModel):
    """A produced image and the provenance needed to reproduce or audit it.

    `image_path` is a file the provider owns until the caller copies it into the asset
    store. Antigravity's lands in its own brain directory (S2), so the path can be outside
    any thumbforge directory.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    image_path: Path
    provider_key: str = Field(min_length=1)
    provider_version: str
    model: str | None = None
    #: The seed the provider actually used, which may differ from the one requested, or be
    #: `None` when it has no notion of one.
    seed_used: int | None = None
    duration_ms: int = Field(ge=0)
    cost: Cost | None = None
    #: The provider's own response, stored verbatim for diagnosis.
    raw_response: JsonPayload = Field(default_factory=dict)


@runtime_checkable
class ImageProvider(Protocol):
    """Generate one image per call. Implementations live in `providers/`."""

    #: Registry key, matching the entry-point name (`"fake"`, `"antigravity"`).
    key: ClassVar[str]

    @property
    def capabilities(self) -> ProviderCapabilities:
        """What this provider supports; callers check before sending a request."""
        ...

    async def info(self) -> ProviderInfo:
        """Identity and auth state. Must not raise for a merely unauthenticated provider."""
        ...

    async def healthcheck(self) -> HealthReport:
        """Every check this provider can run, with actionable detail on each failure."""
        ...

    async def generate(self, request: GenerationRequest, *, workdir: Path) -> GenerationResult:
        """Produce one image, or raise a `ProviderError` subclass.

        `workdir` is a caller-owned scratch directory the provider may write to. A provider
        that cannot be told where to write (Antigravity, per S2) reports the path it chose
        in `GenerationResult.image_path` instead.
        """
        ...


__all__ = [
    "AuthState",
    "Check",
    "Cost",
    "GenerationRequest",
    "GenerationResult",
    "HealthReport",
    "ImageProvider",
    "ProviderCapabilities",
    "ProviderInfo",
]
