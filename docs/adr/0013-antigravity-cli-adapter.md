# ADR 0013: Antigravity CLI adapter contract

## Status

`Proposed (until spikes S1–S8 in OPEN_QUESTIONS.md close)` — 2026-09-19

## Context

The first real `ImageProvider` drives Google's Antigravity CLI (`agy 1.2.3` on PATH) in headless mode. Verified from the official headless docs and `agy --help`:

- `agy -p "<prompt>" --output-format json` prints one JSON envelope to stdout; diagnostics go to stderr.
- Envelope fields: `conversation_id`, `status`, `response`, `error?`, `duration_seconds`, `num_turns`, `usage{input_tokens, output_tokens, thinking_tokens, cache_read_tokens, total_tokens}`.
- `status` ∈ `SUCCESS | ERROR | CANCELED | INTERRUPTED | INVALID | WAITING | RUNNING`. Exit `0` on success; non-zero (observed `1`) on failure. Unknown `--model` → exit `1` with an `ERROR` envelope.
- Flags: `--add-dir <abs>` (repeatable), `--print-timeout <dur>` (default `5m`), `--model <slug>` (`agy models`), `--effort low|medium|high`, `--dangerously-skip-permissions`.
- Headless mode uses cached credentials; an unauthenticated run exits with `authentication required`.
- Permission-gated tools are soft-denied in headless mode (exit 0, notice on stderr) unless allowed via `permissions.allow` in `~/.gemini/antigravity-cli/settings.json` or `--dangerously-skip-permissions`.

**Not verified** (third-party reports only): whether an image tool is exposed headlessly (S1), prompt-driven output path and the scratch directory (S2), JPEG-only output and size behaviour (S3), reference-image passing (S4), permission rule name (S5), exit/status matrix (S6), rate limits (S7), cost fields (S8).

## Decision

`providers/antigravity.py` is a subprocess adapter designed around the verified facts only:

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
7. Settings `[providers.antigravity] binary="agy" model=null effort="low" timeout_s=600 skip_permissions=true` (decision D4). The documented alternative is a `permissions.allow` rule for the image tool discovered in spike S1.
8. Capabilities: reference=True (pending S4), seed=False, negative=True (prompt-only), aspect=True (pending S3), max_batch=1, max_concurrency=1, formats={"jpeg"}.

## Consequences

- Roadmap task P3.3 executes S1–S8 and records results in `docs/spikes/antigravity.md` before P3.4 writes the adapter; this ADR flips to `Accepted` or is superseded by the outcome.
- If S1 finds no image tool headlessly, P3.4 is blocked; `FakeProvider` plus an "external image file" provider keep Phases 5–7 moving.
- Concurrency is forced to 1 and every iteration is a fresh process, so cost is one CLI invocation per image.

## Alternatives considered

- **Calling a Google image API directly (HTTP)** — rejected for v1: requires API keys and billing setup, whereas `agy` reuses the user's existing login; may become a second provider.
- **Driving `agy` interactively via a PTY** — rejected: fragile parsing, no JSON envelope, not portable to Windows CI.
- **`--output-format stream-json` as the primary mode** — rejected: the single JSON envelope is sufficient for success/failure; stream mode is used only by spikes S1 and S4 for inspection.
