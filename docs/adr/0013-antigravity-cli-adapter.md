# ADR 0013: Antigravity CLI adapter contract

## Status

`Accepted` — 2026-09-20 (proposed 2026-09-19; revised after spikes S1–S8, see `docs/spikes/antigravity.md`)

## Context

The first real `ImageProvider` drives Google's Antigravity CLI (`agy` on PATH; written against 1.2.3, spiked against 1.2.6) in headless mode. Verified from the official headless docs and `agy --help`:

- `agy -p "<prompt>" --output-format json` prints one JSON envelope to stdout; diagnostics go to stderr.
- Envelope fields: `conversation_id`, `status`, `response`, `error?`, `duration_seconds`, `num_turns`, `usage{input_tokens, output_tokens, thinking_tokens, cache_read_tokens, total_tokens}`.
- `status` ∈ `SUCCESS | ERROR | CANCELED | INTERRUPTED | INVALID | WAITING | RUNNING`. Exit `0` on success; non-zero (observed `1`) on failure. Unknown `--model` → exit `1` with an `ERROR` envelope.
- Flags: `--add-dir <abs>` (repeatable), `--print-timeout <dur>` (default `5m`), `--model <slug>` (`agy models`), `--effort low|medium|high`, `--dangerously-skip-permissions`.
- Headless mode uses cached credentials; an unauthenticated run exits with `authentication required`.
- Permission-gated tools are soft-denied in headless mode (exit 0, notice on stderr) unless allowed via `permissions.allow` in `~/.gemini/antigravity-cli/settings.json` or `--dangerously-skip-permissions`.

Spikes S1–S8 have since been run against **`agy 1.2.6`** (`docs/spikes/antigravity.md`). They confirmed viability and **falsified four of this ADR's original design points**:

- `generate_image` exists headlessly, with exactly two parameters: `ImageName` and `Prompt`. There is no path, size, aspect-ratio, seed or reference parameter, and `tool_info.output` is `null`.
- Output lands in `~/.gemini/antigravity-cli/brain/<conversation_id>/<ImageName>_<epoch_ms>.jpg` — **not** in `--add-dir` and **not** in `scratch/`. The path is deterministic because the envelope returns `conversation_id`.
- `"16:9 widescreen"` in the prompt reliably yields **1376×768** JPEG (5 of 5); omitting the ratio gives an unpredictable size. Exact dimensions are never controllable.
- A reference image is read with `view_file` and _described into the prompt_; its bytes never reach the image model.
- `generate_image` requires **no** permission grant (S5), so `--dangerously-skip-permissions` is unnecessary.
- **`--print-timeout` expiry returns exit `0` with `status: SUCCESS`, an empty `response` and zero `usage`** (S6c). A timeout looks like a success that produced no file.
- Two concurrent invocations succeed and are _faster_ per run than sequential ones (S7); seven generations moved the five-hour quota by 1%.
- `usage` carries tokens only — no credit, price or currency field (S8).

Still unverified: the unauthenticated path (S6a). Isolating the profile via `USERPROFILE`/`HOME` does not work, and confirming it would require signing the maintainer out, so the `authentication required` behaviour remains documentation-only.

## Decision

`providers/antigravity.py` is a subprocess adapter designed around the verified facts only:

1. Build the prompt from `providers/antigravity_wrapper.j2`, which (a) instructs the agent to call `generate_image` exactly once, (b) states the aspect ratio in **words** ("16:9 widescreen") — measured as the only lever on output size, (c) lists reference image absolute paths so the agent can `view_file` and describe them, (d) forbids running shell commands or other tools. It does **not** state an output path: `generate_image` has no path parameter, so the instruction is unachievable and the agent spends a turn apologising for it.
2. Run `[binary, "-p", prompt, "--output-format", "json", "--add-dir", str(workdir), *("--add-dir", d for d in reference_dirs), "--print-timeout", f"{timeout_s}s", *(["--dangerously-skip-permissions"] if skip_permissions else []), *(["--model", model] if model else []), *(["--effort", effort] if effort else [])]` via `asyncio.create_subprocess_exec(..., cwd=workdir, stdout=PIPE, stderr=PIPE)`.
3. Locate the output by globbing `~/.gemini/antigravity-cli/brain/<conversation_id>/` for an image, using the `conversation_id` from the envelope, then copy it into the asset store. Success ⇔ exit code `0` **and** `status == "SUCCESS"` **and** exactly one such image is found **and** Pillow opens it.
4. Error mapping:

    Order matters: the timeout row **must** be evaluated before the missing-output row,
    because a `--print-timeout` expiry presents as `SUCCESS` with no file (S6c). Reversing
    them turns every long generation into a permanent failure and abandons the batch item.

    | Observation                                                       | Exception                                                            | Retryable |
    | ----------------------------------------------------------------- | -------------------------------------------------------------------- | --------- |
    | `SUCCESS`, empty `response`, `total_tokens == 0`, no output image | `ProviderTimeoutError` (agy's own print timeout)                     | **yes**   |
    | `SUCCESS` but no output image found in `brain/<conversation_id>/` | `ProviderOutputMissingError` (message names the **brain** directory) | no        |
    | `status ∈ {CANCELED, INTERRUPTED}`                                | `ProviderTransientError`                                             | yes       |
    | `ERROR` and `error` contains `authentication required`            | `ProviderAuthError` (mapping is defensive; S6a unverified)           | no        |
    | `ERROR` otherwise / `INVALID` / `WAITING` / `RUNNING`             | `ProviderPermanentError`                                             | no        |
    | subprocess exceeds `timeout_s + 30`                               | `ProviderTimeoutError` (process killed)                              | yes       |
    | binary not found                                                  | `ProviderPermanentError` with hint "install Antigravity CLI"         | no        |

5. `usage` tokens and `duration_seconds` are written to `iteration.cost_json`; the whole envelope to `provider_response_json`; stdout/stderr to per-iteration log files.
6. Never uses `--continue`/`--conversation`; every image is a fresh conversation.
7. Settings `[providers.antigravity] binary="agy" model=null effort="low" timeout_s=600 skip_permissions=false`. S5 superseded decision D4: `generate_image` needs neither the flag nor a `permissions.allow` rule, so the default no longer opts into `--dangerously-skip-permissions`. The flag stays configurable for users whose `settings.json` is more restrictive.
8. Capabilities, as measured: `reference=False` (S4 — the agent describes a reference rather than conditioning on it), `seed=False`, `negative=True` (prompt-only), `aspect=True` but **influence only** — the ratio words steer the result and the exact size is never guaranteed (S3), `max_batch=1`, `max_concurrency=2` (S7 measured two concurrent runs as safe and faster), `formats={"jpeg"}` (S3 — JPEG in 7 of 7).
9. `provider check antigravity` reports the contents of `~/.gemini/config/plugins/`. Every headless run inherits the developer's globally installed plugins — the S4 run opened a `superpowers` skill file unprompted — so generation is not a pure function of thumbforge's inputs, and a surprising result must be diagnosable.

## Consequences

- P3.3 ran S1–S8 (`docs/spikes/antigravity.md`); this ADR is now `Accepted` and **P3.4 is unblocked**. The "external image file" fallback provider is not needed.
- Every iteration is a fresh process, so cost is one CLI invocation per image. Concurrency is 2 rather than 1, on measured evidence.
- `imaging/fit.py` must upscale 1376×768 → 1920×1080 (1.40×) and crop the 1.792 ratio to 1.778, per decision D2. Dropping the default to 1280×720 would avoid the upscale; D2 chose 1920×1080 knowingly.
- Batch style consistency cannot rely on image-to-image conditioning (S4), so ADR 0008's "AI paints the background; Pillow renders the text" carries more weight than when it was written.
- Cost reporting (P8.3) is limited to tokens, `duration_seconds` and the `/usage` percentages: the CLI exposes no monetary figure (S8).

## Alternatives considered

- **Calling a Google image API directly (HTTP)** — rejected for v1: requires API keys and billing setup, whereas `agy` reuses the user's existing login; may become a second provider.
- **Driving `agy` interactively via a PTY** — rejected: fragile parsing, no JSON envelope, not portable to Windows CI.
- **`--output-format stream-json` as the primary mode** — rejected: the single JSON envelope is sufficient for success/failure, and S3 measured `tool_info.output` as `null`, so the stream does not even carry the produced path. Stream mode is used only by spikes for inspection.
