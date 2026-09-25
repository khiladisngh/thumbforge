# Phase 7 — Batch

Status: Proposed
ROADMAP tasks: P7.1, P7.2, P7.3, P7.4
ADRs: `docs/adr/0012-idempotency-and-resumable-runs.md`, `docs/adr/0015-structlog-logging.md`, `docs/adr/0011-content-addressed-assets.md`

## Scope

Generate one consistent thumbnail per playlist item using a picked hero as the style reference, with idempotent, resumable, interruptible runs and the `runs` management commands.

- **P7.1** `core/services/batch.py` (`BatchService`) — idempotency keys, semaphore, per-item pipeline.
- **P7.2** resume / cancel / SIGINT handling.
- **P7.3** `cli/batch.py` — Rich progress, summary table, exit `6`.
- **P7.4** `cli/runs.py` — `runs list|show|resume|cancel|delete`.

## Non-goals

- Cross-machine or multi-process runs; the DB is single-user and the `running`-staleness rule is the only recovery from a crashed process.
- Scheduling / daemon mode.
- Re-fetching playlist metadata inside `batch` (run `fetch --refresh` first; `batch` uses stored items).

## Interfaces

```python
class BatchService:
    async def run(self, spec: BatchSpec, *, progress: ProgressSink, cancel: asyncio.Event) -> RunResult
        # BatchSpec(playlist_id, hero: Run | Iteration, template_ref, provider_key, concurrency, only: set[int] | None,
        #           dry_run, resume_run_id, reference: Literal["final","raw"], max_images, max_retries)
    def plan(self, spec: BatchSpec) -> BatchPlan         # per item: key, action ∈ {skip, retry, create}, reason
```

Hero → batch link (`PLAN.md` §3.1): `batch <playlist> --hero <run|iteration>` creates `run(kind='batch', playlist_id=P, parent_run_id=<hero run id>, reference_asset_id=<picked iteration>.final_asset_id)`. Passing `--reference raw` uses `raw_asset_id` instead. Each batch `iteration` receives the reference asset's absolute path in `GenerationRequest.reference_images`.

Idempotency key (`PLAN.md` §6, verbatim): `sha256(template.spec_hash + provider_profile.id + video.youtube_id + str(part_number) + rendered_prompt + str(seed) + reference_asset.sha256)[:32]`, stored on `iteration.idempotency_key UNIQUE`.

Batch / resume algorithm (`PLAN.md` §6, verbatim): for every selected `playlist_item`, compute the key. If an iteration with that key exists and is `completed` → skip (counted as done). If `running` and `started_at` is older than `batch.stale_after_s` (default 900 s) → treat as `failed`. If `failed` → retry while `provider_response_json.attempts < --max-retries` (default 2). Otherwise create a `pending` iteration.

Concurrency: `asyncio.Semaphore(min(--concurrency, capabilities.max_concurrency))`; Antigravity is therefore serialised.

Interrupt: SIGINT → cancel in-flight tasks, mark those iterations `failed` with `error_text = "interrupted"`, mark run `paused`, exit `130`. Finished iterations are never touched.

Partial completion: run ends with ≥1 failed and ≥1 completed → run `failed`, exit `6`, message shows the resume command. All failed → run `failed`, exit `4`.

Budget guard: `--max-images N` aborts before creating more than N new iterations (pre-flight count, exit `2`).

State machine: `pending → running → {completed, failed, cancelled, paused}`; `paused/failed → running` via `runs resume`; `pending → cancelled` via `runs cancel`.

Commands (`PLAN.md` §5.2):

| Command                        | Key flags                                                                                                                                                                                        | Output                                                                                                           | Exit            |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | --------------- |
| `thumbforge batch <playlist>`  | `--hero <run\|iteration>`, `--template NAME`, `--provider KEY`, `--concurrency 2`, `--only 3,7-9`, `--dry-run`, `--resume RUN_ID`, `--reference final\|raw`, `--max-images N`, `--max-retries 2` | batch run; Rich progress; summary table                                                                          | 0, 3, 4, 6, 130 |
| `thumbforge runs list`         | `--kind`, `--status`, `--limit`                                                                                                                                                                  | table                                                                                                            | 0               |
| `thumbforge runs show <run>`   |                                                                                                                                                                                                  | panel + iterations table                                                                                         | 0, 3            |
| `thumbforge runs resume <run>` | `--concurrency`                                                                                                                                                                                  | continues a `paused`/`failed` run                                                                                | 0, 3, 4, 6      |
| `thumbforge runs cancel <run>` |                                                                                                                                                                                                  | marks `cancelled` (only if not `completed`)                                                                      | 0, 3            |
| `thumbforge runs delete <run>` | `--assets`                                                                                                                                                                                       | deletes run + iterations; `--assets` also unlinks unreferenced assets; refuses if referenced by a batch (exit 2) | 0, 2, 3         |

## Behaviour

1. `batch P --hero H` validates: playlist exists (3), hero run/iteration exists (3), hero has a picked iteration or `H` is an iteration id (2 otherwise), reference asset file verifies (`AssetStore.verify`, else 1). `--only 3,7-9` selects by `part_number`; items with `part_number NULL` are skipped unless listed explicitly by position.
2. `plan()` is computed before any provider call; `--dry-run` prints it as a table (`part, title, key[:8], action, reason`) and exits `0`. `--max-images` compares against the count of `create` + `retry` rows.
3. Per item: render prompt with `part_number`/`part_label` → `GenerationRequest` with `reference_images=(ref_path,)` → provider (Phase 3 retries) → `finalize` (Phase 5 `render_final`, injected as in P6.1) → asset rows → iteration `completed`. Every step is logged with `run_id`, `iteration_id`, `provider` bound in contextvars.
4. Progress (stdout) shows `Part n/N  <title>` per `PLAN.md` §5.3; logs (stderr) never interleave with it. In `--json` mode, progress is suppressed and a single summary object is printed at the end.
5. `runs resume R` reloads `BatchSpec` from `run.params_json`, applies the resume algorithm, and continues; `--concurrency` may override. `runs resume` on a `completed` or `cancelled` run exits `2`.
6. `runs cancel R` on `pending`/`running`/`paused`/`failed` sets `cancelled`; on `running` it also sets a cancel flag file `<state_dir>/runs/<R>.cancel` polled by the live process, which then behaves as SIGINT but records `cancelled` instead of `paused`.
7. `runs delete R` refuses while any run has `parent_run_id = R` or references one of its assets (`ON DELETE RESTRICT` surfaces as exit `2` with the dependent run ids); `--assets` unlinks asset files no other row references.
8. Summary table at the end: `part, title, status, size, compliant, asset, error`; then `Resume with: thumbforge runs resume <id>` when exit is `6` or `130`.

## Acceptance criteria

- `thumbforge batch PLxxxx --hero <hero run> --template series-parts --provider fake` on the 12-item fixture produces 12 `completed` iterations, run `completed`, exit `0`; every iteration's `provider_request_json.reference_images[0]` is the hero's final asset path.
- Re-running the identical command creates no new iterations (all 12 `skip`), makes zero provider calls, and exits `0`.
- With `--var fail=[[FAIL_TRANSIENT]]` interpolated on parts 3 and 7 only (template `{% if part_number in (3,7) %}`), the run ends `failed`, exit `6`, summary shows 10 completed / 2 failed, and stderr shows 3 retry attempts per failed item.
- `runs resume <that run>` after removing the failing var completes the 2 remaining items and exits `0`; the 10 earlier iterations are untouched (`updated_at` unchanged).
- Sending SIGINT during a FakeProvider `delay_ms=2000` run with `--concurrency 1` leaves the run `paused`, the in-flight iteration `failed` with `error_text = "interrupted"`, prints the message from `PLAN.md` §5.3, exit `130`.
- An iteration left `running` with `started_at` 1000 s ago is retried by `runs resume` when `stale_after_s = 900`.
- `--max-images 5` on a 12-item playlist exits `2` before any provider call; `--dry-run` prints 12 `create` rows and exits `0`.
- `--concurrency 4 --provider antigravity` runs strictly one provider process at a time (asserted with a stub `agy` that records overlapping start/end timestamps).
- `runs delete <hero run>` while the batch run exists exits `2` naming the batch run id.
- `--reference raw` stores `reference_asset_id = <picked>.raw_asset_id`.

## Test plan

- Unit: `plan()` matrix (completed/skip, running-stale/retry, failed-under-max/retry, failed-at-max/skip-with-reason, new/create); `--only` parsing (`3,7-9`); reference resolution; roll-up + exit codes; key formula golden values for fixed inputs.
- Unit (async): `BatchService.run` with FakeProvider and `delay_ms` — semaphore bound, SIGINT via `cancel.set()`, stale detection with a frozen clock, resume continuation.
- Contract: none new.
- Integration (`-m integration`): one 2-item batch with Antigravity after S1–S4, S7 close.
- Golden: none.

## Open spikes

- **S7** rate limits / quota — may require a fixed delay between Antigravity calls (`[providers.antigravity] cooldown_s`, added only if S7 shows throttling).
- **S8** cost/usage — decides what the summary's cost column shows (Phase 8 cost report reads `iteration.cost_json`).
