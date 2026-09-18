# ADR 0012: Idempotency keys and resumable runs

## Status

`Accepted` — 2026-09-19

## Context

A batch over a 12-video playlist with a provider that takes 30–60 s per image (Antigravity, pending spike S7) runs for many minutes and will be interrupted: Ctrl-C, a timeout, a transient provider error, a laptop lid. Re-running must not regenerate images that already succeeded, must retry the ones that failed a bounded number of times, and must never double-count.

## Decision

- **Idempotency key** (per iteration): `sha256(template.spec_hash + provider_profile.id + video.youtube_id + str(part_number) + rendered_prompt + str(seed) + reference_asset.sha256)[:32]`, stored on `iteration.idempotency_key UNIQUE`. For hero runs `part_number` is `""` and the ordinal is folded into `seed` (or `str(ordinal)` when the provider has no seed) so N iterations get N keys. Helpers live in `core/ids.py`.
- **Run states**: `pending → running → {completed, failed, cancelled, paused}`; `paused` and `failed` return to `running` via `runs resume`. `pending → cancelled` is allowed.
- **Batch / resume algorithm**: for every selected `playlist_item`, compute the key. If an iteration with that key exists and is `completed` → skip (counted as done). If `running` and `started_at` is older than `batch.stale_after_s` (default 900 s) → treat as `failed`. If `failed` → retry while `provider_response_json.attempts < --max-retries` (default 2). Otherwise create a `pending` iteration.
- **Concurrency**: `asyncio.Semaphore(min(--concurrency, capabilities.max_concurrency))`; Antigravity is therefore serialised.
- **Interrupt**: SIGINT → cancel in-flight tasks, mark those iterations `failed` with `error_text = "interrupted"`, mark run `paused`, exit `130`. Finished iterations are never touched.
- **Partial completion**: run ends with ≥1 failed and ≥1 completed → run `failed`, exit `6` (`PartialBatchError`), message shows the resume command. All failed → run `failed`, exit `4`.
- **Budget guard**: `--max-images N` aborts before creating more than N new iterations (pre-flight count, exit `2`).
- Retries within one attempt (transient/timeout only) use `tenacity` per `PLAN.md` §7.2; the attempt counter that `--max-retries` reads is the cross-invocation one in `provider_response_json.attempts`.

## Consequences

- `runs resume <run>` is the only recovery command a user needs; `--resume RUN_ID` on `batch` is an alias.
- Changing the template version, provider profile, prompt, seed or reference asset changes the key, so a "resume" after such a change correctly regenerates.
- The `UNIQUE` constraint makes accidental double insertion a database error rather than a duplicate image.
- Tests use `FakeProvider` with `[[FAIL_TRANSIENT]]` / `[[FAIL_PERMANENT]]` markers and `delay_ms` to simulate every transition.

## Alternatives considered

- **Sequence-number bookkeeping (`last_completed_position`)** — rejected: breaks with `--only 3,7-9`, parallelism and retries of earlier items.
- **Hashing only `(playlist_id, video_id)`** — rejected: a template or reference change would wrongly skip regeneration.
- **A job queue (Celery, RQ, Huey)** — rejected: needs a broker or a worker process; SQLite rows plus a semaphore give the same guarantees for one process.
