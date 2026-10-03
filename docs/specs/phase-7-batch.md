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
    async def resume(self, run_id: str, *, progress: ProgressSink, cancel=None, concurrency=None) -> RunResult
    def cancel(self, run_id: str) -> None                # refuses a completed run
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
3. Per item: render prompt with `part_number`/`part_label` → `GenerationRequest` with `reference_images=(ref_path,)` → provider (Phase 3 retries) → `finalize` (Phase 5 `render_final`, injected as in P6.1) → raw and final asset rows → iteration `completed`. When the report is not `ok`, the final asset is still stored with `compliant = 0` and `compliance_report_json`, and the iteration is marked `failed` with `error_text` from the report's `violations`, so resume retries it and the roll-up counts it as an ordinary failure (exit `6` or `4`; batch has no exit `5`). Every step is logged with `run_id`, `iteration_id`, `provider` bound in contextvars.
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

## Decisions made in P7.1

The service lands before its command (P7.3), so these are where the spec was silent or the code had to choose:

- `BatchService.run(spec, *, progress)` takes no `cancel` event yet and `BatchSpec` has no `resume_run_id` or `vars` (P7.2, P7.3). `hero` is a run or iteration id; `BatchSpec` also carries `provider_params`. `plan(spec)` is `async`, because a key needs the provider's identity; the only row a plan writes is the provider profile.
- `--max-images` is checked in `run` against the `create` + `retry` rows, before the run row exists, and raises `UsageError` (exit `2`). A dry run ignores it: it returns the plan so the user can see what to narrow.
- Every non-dry run writes a batch run, also when every item is skipped (it then has no iterations of its own). A retried item is reused in place: its key is unique, so it stays in the iteration (and run) it was created in, and `BatchResult.iteration_ids` lists the iterations this batch ran.
- Selection: without `--only`, the items that have a `part_number` (`playlist renumber --skip` clears it on purpose). With `--only`, an item is selected when its `part_number` is listed, or when it has none and its playlist position is listed. Selecting nothing is a `UsageError`.
- Retry budget: `provider_response_json.attempts` is cumulative over all tries of an iteration, and a failed iteration is retried while it is `< max_retries`. A transient failure uses its three provider calls in one try, so it is not retried automatically; a permanent one is retried once with the default of 2.
- A `running` iteration with the same key is skipped as "running in another run". Staleness (`batch.stale_after_s`) belongs to P7.2.
- The roll-up reports the playlist, not just the batch's own work: a skipped `completed` item counts as completed and a skipped failed item whose tries are used up counts as failed. Exit `0` when nothing failed, `4` when nothing completed, else `6`; a batch has no exit `5`.
- No seed is sent: the key's `seed` and `part_number` parts are empty strings when absent, as in hero keys. A provider that cannot take a reference image runs prompt-only and the result says so (`reference_ignored`).
- The per-item pipeline is `hero.run_iteration`; `TemplateRenderer.render` takes keyword-only `part_number` and `part_label`.

## Decisions made in P7.2

The commands that call these (`batch`, `runs resume|cancel`) are P7.3 and P7.4, so P7.2 is service behaviour only and adds no CLI.

- `run(spec, *, progress, cancel=None)` takes the `cancel` event, optional so callers that never interrupt need not make one. `resume(run_id, *, progress, cancel=None, concurrency=None)` replaces `BatchSpec.resume_run_id`: the spec is rebuilt from the stored run, so the field would only repeat it. `cancel(run_id)` is synchronous.
- Interrupt is `cancel.set()` or cancelling the task that runs `run`, which is what Ctrl-C does under `asyncio.run`. Both pause the run (`error_text = "interrupted"`). An iteration past the semaphore ends `failed` with `error_text = "interrupted"` and the try is **not** charged against `max_retries` (an interrupt is not a provider failure, and two Ctrl-Cs must not exhaust an item); one still waiting for the semaphore stays `pending`; finished ones are untouched. `BatchResult.exit_code` is `130` for a paused result and `BatchResult.pending` counts what is left, for the `Interrupted: … paused (7 completed, 1 failed, 4 pending)` line. The task-cancel path raises `CancelledError` after pausing, as asyncio requires; mapping it to exit `130` is the CLI's. Tests drive both paths; a real OS signal is not raised, because forwarding one is the CLI's (P7.3).
- **Resume continues the run in place** (P7.1 review Should 1). It plans the run's spec again and retries only the iterations that run itself created: no new run, no new iteration, other runs' iterations untouched. The run is reopened (`running`, end time and reason cleared) and ends `completed` or `failed` from its own iterations, so a retried item no longer leaves a `failed` run behind. A run with every try used up ends `failed` again without a provider call. `completed` and `cancelled` runs, and runs that are not batch runs, are refused (exit `2`); an unknown run is exit `3`. A `running` run is resumable: it is what a crashed process leaves. `max_images` is not applied again: a resume creates nothing new. A plain `batch` re-run retries unfinished and failed items in the run that created them (their key is unique, so there is no other place) and leaves that run's status as it was, whether `failed`, `paused` or `cancelled`, while the re-run itself has no iterations of its own; P7.3 decided what the command does with that (below).
- A run stores the **iteration** its reference image came from (`params_json.hero`), not the run id the user typed, so moving the pick on the hero run cannot change a resume's keys and regenerate finished items.
- Staleness: `BatchService(stale_after_s=…)` (the command passes `batch.stale_after_s`; the default is 900, as `max_retries` defaults to 2). The plan treats a `running` iteration older than that, or one with no start time, as `failed` (reason `stale, …`, retried within `max_retries`); a younger one is skipped as `running in another run`.
- `cancel` refuses a `completed` run (exit `2`), does nothing to a `cancelled` one, and otherwise marks the run and its `pending`/`running` iterations `cancelled`; finished iterations stay. It does not stop a live process: the cancel flag file is P7.4.
- Counts and status are read back from the stored iterations of the run's scope (the whole selection for `run`, the run's own iterations for `resume`), which is what lets a paused run report them. A fresh `running` iteration owned by a live process counts as neither completed nor failed, as in P7.1.

## Decisions made in P7.3

- **The command** is the bare `thumbforge batch <playlist> --hero <run|iteration>`; `--hero` is required, because the reference image is what makes the thumbnails a series. Flags: `--template`, `--provider` (both default from `[general]`), `--concurrency` (default `[batch] concurrency`), `--only 3,7-9`, `--max-images N`, `--dry-run`, `--reference final|raw` (default `final`). Left off the table above on purpose: `--resume`, which `runs resume` replaces (P7.2), and `--max-retries`, which comes from `[batch] max_retries`; a flag would be a second way to set the same knob. `[batch] stale_after_s` goes to the service. `--only` is parsed by the command: part numbers `1` to `10000`, ranges ascending, anything else is exit `2`.
- **A plain `batch` re-run is a supported way to continue**, and the only one until `runs resume` lands (P7.4). It retries failed and unfinished items inside the runs that created them (no iteration row is added), writes a run of its own that ends `completed` or `failed` from the whole selection, and leaves the older run's stored status as it was (`paused` stays `paused`). Closing that older run is what `runs resume <id>` is for. The line after a partial, all-failed or interrupted batch therefore says to run the same command again, and names `runs show <id>`; P7.4 adds `runs resume <id>` to it. Nothing was changed in the service for this.
- **Exit codes** come from `BatchResult.error()`, after the output is printed: `4` `ProviderError` ("all N items failed", or "no item completed, F of N failed" when some are neither), `6` `PartialBatchError` ("C of N items completed, F failed"), `130` the new `RunInterruptedError`, code `interrupted` ("run R paused (7 completed, 1 failed, 4 pending)"). A dry run is `0`. `3` and `2` are the service's usual errors, raised before any run exists.
- **Output.** stdout is a header, then the summary table `Part, Title, Status, Size, Compliant, Asset, Error`, one row per selected item in playlist order, including items skipped because they are already `completed`. It is read back from the stored rows, so an interrupted run shows its `pending` items. `--json` prints one object: `run` (the same object `runs show` prints), `summary` (`total`, `completed`, `failed`, `pending`), `items` (`part`, `position`, `video`, `title`, `action`, `iteration_id`, `status`, `compliant`, `final_asset`, `error`), `reference_ignored`, `exit_code`. `--dry-run` prints the table `Part, Title, Key, Action, Reason` (key shortened to 8 characters) and `--json` gives `dry_run`, `summary` (`skip`, `retry`, `create`), `plan` (the same fields with the full key) and `exit_code`.
- **Progress** is a Rich bar on stderr plus one `✔ Part 3  Title` (or `✘`, with the error) line per finished item. It is drawn only when stderr is a terminal, and never with `--json` or `--dry-run`. While it is drawn the per-iteration log lines drop to DEBUG (the log file still gets them), so they cannot tear the bar. The bar's count is items done of items to generate; the line says `Part 3`, not `Part 3/12` as the `PLAN.md` §5.3 sketch does, because under `--only` a part number over the number of selected items reads wrongly.
- **Ctrl-C** sets the service's cancel event: the command installs a SIGINT handler for the run, in the main thread only, and puts the previous handler back afterwards. It is `signal.signal`, not the loop's `add_signal_handler`, which Windows lacks. The run pauses as P7.2 specifies, the result is printed, and the command exits `130`. A second Ctrl-C only sets the same event again; there is no hard stop. The test raises a real `SIGINT` from inside the fake provider's call with `signal.raise_signal`.
- Shared with `thumb`: `LogProgress` and `finalizer` moved to `cli/_runs.py`, `run_payload` was extracted from `run_view`, and `RunRepository.iterations_by_key` returns the rows the table is drawn from.

## Decisions made in P7.4

- **`runs list`** prints the newest runs first (`Run, Kind, Status, Template, Provider, Done, Failed`; `Done` is `completed/total`) and takes `--kind`, `--status` and `--limit` (default 50). `--json` prints `{"runs": [...]}`; each entry has `id`, `kind`, `status`, `template`, `provider`, `video`, `parent_run_id`, `started_at`, `finished_at` and `counts` (`total`, `completed`, `failed`, `pending`, the shape `batch` prints as `summary`).
- **`runs show`** keeps its output and adds, for every run, `summary` (the same counts) and `run.playlist` (the playlist's YouTube id) to `--json`; a batch run's header also shows `Playlist` and `Items` (`2 completed, 1 failed, 2 pending of 5`).
- **`runs resume R [--concurrency N]`** wraps `BatchService.resume` with the progress display and the Ctrl-C handling `batch` has (`cancel_on_sigint`, `BatchProgress` and `batch_view` moved from private names to shared ones in `cli/batch.py`; the service wiring is `batch_service` in `cli/_runs.py`). It prints what `batch` prints, with the reference mode read back from the run's stored parameters, and exits `0`, `4`, `6` or `130` from `BatchResult.error()`. Unknown run `3`; a completed, cancelled or non-batch run `2`.
- **`runs cancel R`** wraps `BatchService.cancel`: `{"run": ...}` in `--json`, one line for a person; a completed run is refused (`2`), a cancelled one is a no-op, an unknown one is `3`.
- **The cancel flag file is not built.** Item 6 above has `runs cancel` on a `running` run also write `<state_dir>/runs/<R>.cancel`, polled by the live process. That needs the service to poll a file inside its run loop and a second writer of state beside the database; with one user, one terminal per batch and Ctrl-C already pausing a run cleanly, there is no caller for it. `runs cancel` therefore marks the stored rows only (as P7.2 decided) and does not stop a live process.
- **`runs delete R [--assets]`** is `RunRepository.delete_run`, with no service on top: it is two queries and a delete. It refuses (`UsageError`, exit `2`, naming the dependent run ids) while another run has `parent_run_id = R` (a refinement, or a batch whose hero it is) or a `reference_asset_id` among R's raw and final assets. Otherwise it deletes the run and, through the ORM cascade, its iterations. With `--assets` it then deletes the asset rows among R's raw and final images and its reference image that no remaining iteration or run refers to, commits, and only then unlinks their files (a file never goes before the rows that name it). Assets are content-addressed, so an image two runs made is one row and one file and survives the first delete. `--json` prints `{"deleted": {"run", "iterations", "assets": [paths removed]}}`.
- **Not touched by `delete`:** the run's log directory under `<state_dir>/logs/runs/<R>/`, and the shared provider profile, template and video rows. They are small, other runs may share them, and nothing needs them removed yet.
- **Hint after a partial or interrupted batch** still says to run the same command again (the existing tests pin it), which also works; the user guide names `runs resume <run>` as the way that finishes the run itself.

## Test plan

- Unit: `plan()` matrix (completed/skip, running-stale/retry, failed-under-max/retry, failed-at-max/skip-with-reason, new/create); `--only` parsing (`3,7-9`); reference resolution; roll-up + exit codes; key formula golden values for fixed inputs.
- Unit (async): `BatchService.run` with FakeProvider and `delay_ms` — semaphore bound, SIGINT via `cancel.set()`, stale detection with a frozen clock, resume continuation.
- Contract: none new.
- Integration (`-m integration`): one 2-item batch with Antigravity after S1–S4, S7 close.
- Golden: none.

## Open spikes

- **S7** rate limits / quota — may require a fixed delay between Antigravity calls (`[providers.antigravity] cooldown_s`, added only if S7 shows throttling).
- **S8** cost/usage — decides what the summary's cost column shows (Phase 8 cost report reads `iteration.cost_json`).
