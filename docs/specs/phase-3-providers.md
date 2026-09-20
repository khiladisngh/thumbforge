# Phase 3 — Providers

Status: Proposed (P3.4 blocked on spikes S1–S8)
ROADMAP tasks: P3.1, P3.2, P3.3, P3.4, P3.5
ADRs: `docs/adr/0010-provider-plugin-architecture.md`, `docs/adr/0013-antigravity-cli-adapter.md`, `docs/adr/0014-secrets-env-keyring.md`

## Scope

Define the `ImageProvider` protocol, capabilities, registry with entry-point discovery, the deterministic `FakeProvider`, the `AntigravityProvider` subprocess adapter, and the `provider` commands.

- **P3.1** `core/providers.py` (Protocol and boundary models), `core/json.py` (`JsonValue`), `providers/registry.py`, `[project.entry-points."thumbforge.providers"]`.
- **P3.2** `providers/fake.py` + `tests/contract/test_provider_contract.py`.
- **P3.3** spikes S1–S8 executed; findings in `docs/spikes/antigravity.md`.
- **P3.4** `providers/antigravity.py`, `providers/antigravity_wrapper.j2`, marker-gated integration test.
- **P3.5** `cli/provider.py` (`provider list|check|models|set-key`).

## Non-goals

- Overlay, fit, compliance — Phase 5. Providers return raw art only.
- Hero/batch orchestration — Phases 6–7. Phase 3 exposes `generate` for one request at a time.
- Any provider beyond `fake` and `antigravity`; third parties use the entry-point group.

## Interfaces

From `PLAN.md` §4:

```python
class ProviderCapabilities(BaseModel, frozen=True):
    supports_reference_image: bool
    supports_seed: bool
    supports_negative_prompt: bool
    supports_aspect_ratio: bool
    max_batch: int            # images per call; 1 for Antigravity
    max_concurrency: int      # provider-side safe parallelism; 2 for Antigravity (spike S7)
    output_formats: frozenset[str]   # {"jpeg"} for Antigravity

class ImageProvider(Protocol):
    key: ClassVar[str]        # "antigravity", "fake"; matches the entry-point name
    capabilities: ProviderCapabilities
    async def info(self) -> ProviderInfo          # name, version string, auth state
    async def healthcheck(self) -> HealthReport   # binary found, auth ok, model list
    async def generate(self, req: GenerationRequest, *, workdir: Path) -> GenerationResult
```

```python
class GenerationRequest(BaseModel, frozen=True):
    prompt: str
    negative_prompt: str | None
    width: int
    height: int
    reference_images: tuple[Path, ...]
    seed: int | None
    params: dict[str, JsonValue]
    idempotency_key: str


class GenerationResult(BaseModel, frozen=True):
    image_path: Path
    provider_key: str
    provider_version: str
    model: str | None
    seed_used: int | None
    duration_ms: int
    cost: Cost | None  # Cost(tokens_in, tokens_out, credits: Decimal | None, currency: str | None)
    raw_response: dict[str, JsonValue]
```

`ProviderInfo(key, name, version, auth: Literal["ok", "missing", "unknown"])`; `HealthReport(checks, models)` with **`ok` derived** as `all(check.ok …)` rather than supplied, so a report cannot claim health while carrying a failed check. `auth="unknown"` is deliberately distinct from `"missing"`: a provider that cannot cheaply prove its credentials must not be reported as unauthenticated, or `provider check` would tell users to fix something that is not broken.

**Placement.** The Protocol and these models live in **`core/providers.py`**, not `providers/base.py` as an earlier draft of this spec said. `core.services` consumes them — `HeroService` (P6.1) builds a `GenerationRequest` and reads a `GenerationResult` — and `core` may not import `providers`. This is the same constraint that moved `MetadataSource` to `core/sources.py` in P2.3, and `phase-1-skeleton.md` pre-authorised it: _"the contract is the rule, the file placement bends."_ `JsonValue` moved to `core/json.py` for the same reason: `cli` emits it, `core.providers` carries it in `params`/`raw_response`, and `storage` persists it, so it cannot live in `cli`.

`supports_aspect_ratio` means the requested ratio _influences_ the result; it does **not** promise the exact width and height. Spike S3 measured Antigravity honouring "16:9 widescreen" while always returning 1376x768, so Phase 5 fits every result regardless of this flag.

### Registry (`PLAN.md` §4.1)

- Builtin map `{"fake": FakeProvider, "antigravity": AntigravityProvider}` is merged with `importlib.metadata.entry_points(group="thumbforge.providers")`. The entry-point **name** is the provider key; the value is an `ImageProvider` class whose `__init__` takes its config mapping. `BUILTIN` starts empty and is populated by P3.2 and P3.4.
- Duplicate key (builtin vs plugin, or two plugins) → `ProviderRegistryError` at discovery. An error rather than a precedence rule: silently shadowing a provider would make `--provider x` mean different things depending on what else is installed, and that failure surfaces as wrong images rather than as a message.
- A plugin that raises on import → `ProviderRegistryError` naming the entry-point value, with the original error as `__cause__`. Skipping it is indistinguishable from "never installed", which is the harder failure to diagnose.
- An entry point whose value is not callable → `ProviderRegistryError`.
- Unknown key on the CLI → `NotFoundError` → exit `3`, hinting the available keys.
- Core code never imports a concrete provider; it asks the registry.

`registry.get(key: str, config: Mapping[str, JsonValue] | None = None) -> ImageProvider`; `registry.keys() -> list[str]`.

A provider is constructed from **its own config mapping**, not from `Settings` as an earlier draft said. `storage` and `sources` likewise take plain values, so no adapter depends on the application's whole configuration tree — `cli` extracts `settings.providers.<key>` and passes it down. A mapping rather than a typed model because the registry cannot know which model a third-party provider wants, and `provider_profile.params_json` already stores provider config this way.

A provider shipped in this package is registered in `providers.registry.BUILTIN` and **not**
in the `thumbforge.providers` entry points. The map is _merged with_ that group, so declaring
one in both places makes it collide with itself under the duplicate-key rule — the guard
caught exactly that during P3.2. The entry-point group is purely the third-party mechanism.

### FakeProvider (`PLAN.md` §4.2)

- Renders a PNG **at the requested `width`x`height`**. It advertises `supports_aspect_ratio=True`, and a provider that claims that flag and then ignores the request would make Phase 5 skip a fit step the image still needed — so honouring it is what makes the flag testable rather than decorative. An earlier draft said a fixed 1376x768; request that size explicitly to exercise Phase 5's upscale path offline.
- Background colour = first 3 bytes of `sha256(prompt + negative_prompt + seed + size)`; draws the digest prefix as text; when reference images are given, pastes 96-px thumbnails of them into the corners. `negative_prompt` and the size are in the digest because both are advertised as supported, and a flag that changes nothing is worse than a missing one.
- Deterministic to the **byte** for an identical request, so a caller can assert on the image rather than merely on its existence. Nothing varies between runs is embedded in the PNG.
- Sleeps `params.get("delay_ms", 0)` ms (lets progress-bar and concurrency tests be observable).
- Raises `ProviderTransientError` when the prompt contains `[[FAIL_TRANSIENT]]` and `ProviderPermanentError` on `[[FAIL_PERMANENT]]` — used by contract, retry and resume tests.
- Capabilities: reference=True, seed=True, negative=True, aspect=True, max_batch=8, max_concurrency=8, formats={"png"}.

### AntigravityProvider (`PLAN.md` §4.3)

Designed around **measured** behaviour: spikes S1–S8 ran against `agy 1.2.6` and are recorded in `docs/spikes/antigravity.md`. They confirmed the image tool exists (`generate_image`) and falsified four of the original design points, so ADR 0013 is now `Accepted` and the design below reflects the measurements, not the docs. Only the unauthenticated path (S6a) is still unverified.

1. Build the prompt from `providers/antigravity_wrapper.j2`, which (a) instructs the agent to call `generate_image` exactly once, (b) states the aspect ratio in words ("16:9 widescreen") — S3 measured this as the only lever on output size, (c) lists reference image absolute paths for the agent to `view_file`, (d) forbids running shell commands or other tools. It states **no output path**: `generate_image` accepts only `ImageName` and `Prompt`.
2. Run `[binary, "-p", prompt, "--output-format", "json", "--add-dir", str(workdir), *("--add-dir", d for d in reference_dirs), "--print-timeout", f"{timeout_s}s", *(["--dangerously-skip-permissions"] if skip_permissions else []), *(["--model", model] if model else []), *(["--effort", effort] if effort else [])]` via `asyncio.create_subprocess_exec(..., cwd=workdir, stdout=PIPE, stderr=PIPE)`.
3. Locate the image by globbing `~/.gemini/antigravity-cli/brain/<conversation_id>/` using the envelope's `conversation_id`, then copy it into the asset store. Success ⇔ exit `0` **and** `status == "SUCCESS"` **and** exactly one image found **and** Pillow opens it.
4. Error mapping. The timeout row **must** precede the missing-output row — agy's print timeout presents as `SUCCESS` with no file (S6c), so the reverse order makes every long generation a permanent failure:

    | Observation                                                       | Exception                                                            | Retryable |
    | ----------------------------------------------------------------- | -------------------------------------------------------------------- | --------- |
    | `SUCCESS`, empty `response`, `total_tokens == 0`, no output image | `ProviderTimeoutError` (agy's print timeout)                         | **yes**   |
    | `SUCCESS` but no image in `brain/<conversation_id>/`              | `ProviderOutputMissingError` (message names the **brain** directory) | no        |
    | `status ∈ {CANCELED, INTERRUPTED}`                                | `ProviderTransientError`                                             | yes       |
    | `ERROR` and `error` contains `authentication required`            | `ProviderAuthError`                                                  | no        |
    | `ERROR` otherwise / `INVALID` / `WAITING` / `RUNNING`             | `ProviderPermanentError`                                             | no        |
    | subprocess exceeds `timeout_s + 30`                               | `ProviderTimeoutError` (process killed)                              | yes       |
    | binary not found                                                  | `ProviderPermanentError` with hint "install Antigravity CLI"         | no        |

5. `usage` tokens and `duration_seconds` are written to `iteration.cost_json`; the whole envelope to `provider_response_json`; stdout/stderr to per-iteration log files.
6. Never uses `--continue`/`--conversation`; every image is a fresh conversation.
7. `providers.antigravity.skip_permissions` defaults to **`false`** — S5 superseded decision D4 by measuring `generate_image` succeeding with neither the flag nor a `permissions.allow` rule.
8. Capabilities, as measured: reference=**False** (S4: the agent describes a reference rather than conditioning on it), seed=False, negative=True (prompt-only), aspect=True but influence-only (S3), max_batch=1, max_concurrency=**2** (S7), formats={"jpeg"}.
9. `healthcheck()` additionally reports `~/.gemini/config/plugins/`: every headless run inherits the developer's globally installed plugins (S4 observed a `superpowers` skill file being opened unprompted), so output is not a pure function of thumbforge's inputs.

Settings consumed: `[providers.antigravity] binary, model, effort, timeout_s, skip_permissions` (see `phase-1-skeleton.md`). `healthcheck()` runs `shutil.which(binary)`, `agy --version`, `agy models`, and `agy -p "reply ok" --output-format json` and reports auth from the envelope.

### Retries (`PLAN.md` §7.2)

Only `ProviderTransientError` and `ProviderTimeoutError` are retried, via `tenacity`: exponential backoff base 2 s, factor 2, max 60 s, full jitter, `max_attempts = 3` per provider call. Attempt count is recorded in `iteration.provider_response_json.attempts`. The retry wrapper lives in `core/services/` (callers of `generate`), not inside providers, so contract tests see raw behaviour.

### Commands

| Command                           | Key flags | Output                                        | Exit    |
| --------------------------------- | --------- | --------------------------------------------- | ------- |
| `thumbforge provider list`        |           | table `key, version, capabilities, auth`      | 0       |
| `thumbforge provider check KEY`   |           | runs `healthcheck()`                          | 0, 3, 4 |
| `thumbforge provider models KEY`  |           | lists model slugs (Antigravity: `agy models`) | 0, 3, 4 |
| `thumbforge provider set-key KEY` |           | prompts for secret; stores in keyring         | 0, 3    |

Secrets (`PLAN.md` §8): lookup order environment variable `THUMBFORGE_PROVIDERS__<KEY>__API_KEY`, then `keyring` (service `thumbforge`, username `<provider_key>`). `provider set-key` is the only writer. Antigravity needs no key.

## Behaviour

1. `generate` writes exactly one image into `workdir` and returns its path; the caller (Phase 6/7 services) moves it into the `AssetStore`. Providers never touch the DB.
2. A provider raising anything other than a `ProviderError` subclass is a bug; the contract test fails on it.
3. `provider check antigravity` exits `4` with `ProviderAuthError` when the envelope reports `authentication required`; exits `4` with the "install Antigravity CLI" hint when the binary is missing.
4. `provider list` shows plugins discovered via entry points alongside builtins; a duplicate key aborts with `ProviderRegistryError` (exit `1`) naming both distributions.
5. `provider set-key fake` stores a value in keyring even though FakeProvider ignores it (used to test the path without a real provider).

## Acceptance criteria

- `thumbforge provider list` prints rows for `fake` and `antigravity` with `auth` = `ok` for fake and `ok|missing` for antigravity depending on `agy` login state.
- `thumbforge provider check fake` exits `0`; `thumbforge provider check nope` exits `3`.
- `FakeProvider.generate` with the same `prompt` and `seed` twice yields byte-identical PNGs; different seeds yield different background colours.
- Prompt containing `[[FAIL_TRANSIENT]]` raises `ProviderTransientError`; `[[FAIL_PERMANENT]]` raises `ProviderPermanentError`.
- A test distribution registering `fake = tests.plugins:Dup` under `thumbforge.providers` makes `registry.keys()` raise `ProviderRegistryError`.
- With a stubbed `agy` script that prints `{"status":"SUCCESS", ...}` but writes no file, `AntigravityProvider.generate` raises `ProviderOutputMissingError` whose message contains `~/.gemini/antigravity-cli/scratch/`.
- With a stubbed `agy` that sleeps past `timeout_s + 30`, `generate` raises `ProviderTimeoutError` and the child process is gone (`psutil`-free check: `proc.returncode is not None`).
- `uv run pytest -m integration tests/providers/test_antigravity_live.py` produces a JPEG in `workdir` named `<idempotency_key>.jpg` (only after S1–S4 pass).

## Test plan

- Unit: registry merging with monkeypatched `entry_points`; FakeProvider determinism and failure markers; AntigravityProvider argv construction (exact list from step 2), envelope parsing for every `status`, error mapping table row by row using a stub `agy` executable written to `tmp_path`.
- Contract: `tests/contract/test_provider_contract.py` parametrised over `registry.keys()`; per provider asserts `capabilities` is a `ProviderCapabilities`, `info()` and `healthcheck()` return the documented models, `generate` returns a `GenerationResult` whose `image_path` exists and opens with Pillow at width/height consistent with `capabilities.supports_aspect_ratio`, and that failures are `ProviderError` subclasses. Antigravity participates only under `-m integration`.
- Integration (`-m integration`): live Antigravity generation; skipped unless `agy` is on PATH and authenticated.
- Golden: none.

## Resolved spikes

S1–S8 ran on 2026-09-20 against `agy 1.2.6` and are recorded with raw output in
`docs/spikes/antigravity.md`. **P3.4 is unblocked.** Outcomes that changed this spec:

- **S1** — the tool is **`generate_image`** (1 of 57 headless tools). ADR 0013 is `Accepted`; the "external-image-file" fallback provider is not needed.
- **S2** — output path is **not controllable**. The image lands in `~/.gemini/antigravity-cli/brain/<conversation_id>/`, not `--add-dir` and not `scratch/`. The adapter globs that directory using the envelope's `conversation_id`.
- **S3** — **always JPEG**; `"16:9 widescreen"` reliably yields **1376×768** (5 of 5), and exact dimensions are never specifiable. Phase 5 therefore always upscales 1.40× to the 1920×1080 default and crops 1.792 → 1.778.
- **S4** — references are **prose only**: the agent `view_file`s the image and describes it, so `supports_reference_image = False`. Palette transfer measured good, but there is no image-to-image conditioning.
- **S5** — `generate_image` needs **no permission grant**, superseding decision D4: `skip_permissions` defaults to `false`.
- **S6** — a bad `--model` exits `1` with a clean `ERROR` envelope, but **`--print-timeout` expiry returns exit `0` and `SUCCESS` with an empty response**, which is why the timeout row precedes the missing-output row above. The unauthenticated path (S6a) remains unverified.
- **S7** — no throttling; two concurrent runs are safe and faster, so `max_concurrency = 2`. Seven generations cost 1% of the five-hour quota.
- **S8** — `usage` is **tokens only**, with no monetary field, so `Cost` carries tokens and `duration_seconds`.
