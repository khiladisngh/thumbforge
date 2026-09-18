# Phase 3 — Providers

Status: Proposed (P3.4 blocked on spikes S1–S8)
ROADMAP tasks: P3.1, P3.2, P3.3, P3.4, P3.5
ADRs: `docs/adr/0010-provider-plugin-architecture.md`, `docs/adr/0013-antigravity-cli-adapter.md`, `docs/adr/0014-secrets-env-keyring.md`

## Scope

Define the `ImageProvider` protocol, capabilities, registry with entry-point discovery, the deterministic `FakeProvider`, the `AntigravityProvider` subprocess adapter, and the `provider` commands.

- **P3.1** `providers/base.py`, `providers/registry.py`, `[project.entry-points."thumbforge.providers"]`.
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
    max_concurrency: int      # provider-side safe parallelism; 1 for Antigravity
    output_formats: frozenset[str]   # {"jpeg"} for Antigravity

class ImageProvider(Protocol):
    key: ClassVar[str]        # "antigravity", "fake"
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

`ProviderInfo(key, name, version, auth: Literal["ok", "missing", "unknown"])`; `HealthReport(ok: bool, checks: list[Check(name, ok, detail)], models: list[str])`.

### Registry (`PLAN.md` §4.1)

- Builtin map `{"fake": FakeProvider, "antigravity": AntigravityProvider}` is merged with `importlib.metadata.entry_points(group="thumbforge.providers")`. The entry-point **name** is the provider key; the value is an `ImageProvider` class.
- Duplicate key (builtin vs plugin, or two plugins) → `ProviderRegistryError` at load time.
- Unknown key on the CLI → `NotFoundError` → exit `3`.
- Core code never imports a concrete provider; it asks the registry.

`registry.get(key: str, settings: Settings) -> ImageProvider`; `registry.keys() -> list[str]`.

### FakeProvider (`PLAN.md` §4.2)

- Renders a 1376×768 PNG. Background colour = first 3 bytes of `sha256(prompt + str(seed))`; draws the sha prefix as text; when reference images are given, pastes 96-px thumbnails of them into the corners.
- Sleeps `params.get("delay_ms", 0)` ms (lets progress-bar and concurrency tests be observable).
- Raises `ProviderTransientError` when the prompt contains `[[FAIL_TRANSIENT]]` and `ProviderPermanentError` on `[[FAIL_PERMANENT]]` — used by contract, retry and resume tests.
- Capabilities: reference=True, seed=True, negative=True, aspect=True, max_batch=8, max_concurrency=8, formats={"png"}.

### AntigravityProvider (`PLAN.md` §4.3)

Designed around verified behaviour only (headless docs + `agy --help`, agy 1.2.3). Everything about the image tool itself is a spike (S1–S8).

1. Build the prompt from `providers/antigravity_wrapper.j2`, which (a) instructs the agent to call its native image tool exactly once, (b) states the exact absolute output path `<workdir>/<idempotency_key>.jpg`, (c) states the target size as digits and words ("1920 x 1080 pixels, 16:9 widescreen"), (d) lists reference image absolute paths, (e) forbids running shell commands or other tools.
2. Run `[binary, "-p", prompt, "--output-format", "json", "--add-dir", str(workdir), *("--add-dir", d for d in reference_dirs), "--print-timeout", f"{timeout_s}s", *(["--dangerously-skip-permissions"] if skip_permissions else []), *(["--model", model] if model else []), *(["--effort", effort] if effort else [])]` via `asyncio.create_subprocess_exec(..., cwd=workdir, stdout=PIPE, stderr=PIPE)`.
3. Success ⇔ exit code `0` **and** `status == "SUCCESS"` **and** the output file exists **and** Pillow opens it.
4. Error mapping:

    | Observation                                            | Exception                                                                            | Retryable |
    | ------------------------------------------------------ | ------------------------------------------------------------------------------------ | --------- |
    | `SUCCESS` but output file missing                      | `ProviderOutputMissingError` (message mentions `~/.gemini/antigravity-cli/scratch/`) | no        |
    | `status ∈ {CANCELED, INTERRUPTED}`                     | `ProviderTransientError`                                                             | yes       |
    | `ERROR` and `error` contains `authentication required` | `ProviderAuthError`                                                                  | no        |
    | `ERROR` otherwise / `INVALID` / `WAITING` / `RUNNING`  | `ProviderPermanentError`                                                             | no        |
    | subprocess exceeds `timeout_s + 30`                    | `ProviderTimeoutError` (process killed)                                              | yes       |
    | binary not found                                       | `ProviderPermanentError` with hint "install Antigravity CLI"                         | no        |

5. `usage` tokens and `duration_seconds` are written to `iteration.cost_json`; the whole envelope to `provider_response_json`; stdout/stderr to per-iteration log files.
6. Never uses `--continue`/`--conversation`; every image is a fresh conversation.
7. `providers.antigravity.skip_permissions` defaults to `true` (decision D4). The documented alternative is a `permissions.allow` rule for the image tool discovered in spike S1.
8. Capabilities: reference=True (pending S4), seed=False, negative=True (prompt-only), aspect=True (prompt-only, pending S3), max_batch=1, max_concurrency=1, formats={"jpeg"}.

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

## Open spikes

S1–S8 block P3.4 (adapter code is not merged until each is recorded in `docs/spikes/antigravity.md`):

- **S1** headless `agy -p` exposes an image tool — if absent, ADR 0013 stays _Proposed_, P3.4 is blocked, and an "external-image-file" provider (user supplies an image path) is added so Phases 5–7 proceed.
- **S2** output path control via `--add-dir` + prompt — if the file lands only in `~/.gemini/antigravity-cli/scratch/`, the adapter must copy from scratch (and step 1(b) of the wrapper changes).
- **S3** output format and size behaviour — decides whether Phase 5 always upscales from 1376×768 and whether `formats` stays `{"jpeg"}`.
- **S4** reference images accepted by absolute path — decides `supports_reference_image`.
- **S5** permission soft-deny and `permissions.allow` rule — decides the D4 default and what `provider check` must verify.
- **S6** exit code / status matrix — confirms the error-mapping table.
- **S7** rate limits / quota — may lower `timeout_s` defaults or add a cooldown between calls.
- **S8** cost/usage fields — decides what `Cost` carries for Antigravity.
