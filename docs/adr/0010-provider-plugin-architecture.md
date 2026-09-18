# ADR 0010: Provider plugin architecture

## Status

`Accepted` — 2026-09-19

## Context

Image generation backends differ in capabilities (reference images, seeds, negative prompts, batch size, safe concurrency, output formats) and in lifecycle (local CLI vs. HTTP API vs. deterministic fake). The core services (`hero`, `iterate`, `batch`) must not know which provider is in use, tests must run without any real provider, and third parties should be able to add a provider without patching this repo.

## Decision

The provider contract in `providers/base.py` is exactly:

```python
class ProviderCapabilities(BaseModel, frozen=True):
    supports_reference_image: bool
    supports_seed: bool
    supports_negative_prompt: bool
    supports_aspect_ratio: bool
    max_batch: int            # images per call; 1 for Antigravity
    max_concurrency: int      # provider-side safe parallelism; 1 for Antigravity
    output_formats: frozenset[str]   # {"jpeg"} for Antigravity

class ImageProvider(Protocol):
    key: ClassVar[str]        # "antigravity", "fake"
    capabilities: ProviderCapabilities
    async def info(self) -> ProviderInfo          # name, version string, auth state
    async def healthcheck(self) -> HealthReport   # binary found, auth ok, model list
    async def generate(self, req: GenerationRequest, *, workdir: Path) -> GenerationResult
```

`GenerationRequest` and `GenerationResult` are the frozen Pydantic models in `PLAN.md` §4 (`core/models.py`).

- **Registry** (`providers/registry.py`): builtin map `{"fake": FakeProvider, "antigravity": AntigravityProvider}` merged with `importlib.metadata.entry_points(group="thumbforge.providers")`. The entry-point **name** is the provider key; the value is an `ImageProvider` class. Duplicate key → `ProviderRegistryError` at load time. Unknown key on the CLI → `NotFoundError` → exit `3`. Core code never imports a concrete provider.
- **FakeProvider** (`providers/fake.py`) is a first-class builtin, deterministic and offline, with the failure markers `[[FAIL_TRANSIENT]]` / `[[FAIL_PERMANENT]]` (`PLAN.md` §4.2). It is the default provider in settings.
- **Contract test suite** `tests/contract/test_provider_contract.py` is parametrised over every registered provider; real providers are gated by `-m integration`.
- Services consult `capabilities` to clamp concurrency (`asyncio.Semaphore(min(--concurrency, capabilities.max_concurrency))`) and to reject unsupported requests early (e.g. `--seed` with `supports_seed=False` is a usage error, exit `2`).
- A `provider_profile` row snapshots `provider_key`, `provider_version` and `params_json` for every run; it never stores secrets (ADR 0014).

## Consequences

- Phases 4–7 are developed and tested entirely against `FakeProvider`; Antigravity (ADR 0013) can slip without blocking them.
- Adding a provider = one class + one entry point + passing the contract suite.
- Providers are `async`; the CLI layer bridges with `asyncio.run` once per command.

## Alternatives considered

- **Abstract base class instead of Protocol** — rejected: forces third-party plugins to inherit from this package; Protocol keeps structural typing and pyright checks it.
- **Setuptools-style `pkg_resources` discovery** — rejected: deprecated; `importlib.metadata.entry_points` is stdlib.
- **Config-driven dotted-path loading** (`provider.class = "pkg.mod:Cls"`) — rejected: entry points are discoverable by `provider list` without editing config.
