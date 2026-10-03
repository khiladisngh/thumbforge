# Phase 6 — Hero and iterations

Status: Proposed
ROADMAP tasks: P6.1, P6.2, P6.3
ADRs: `docs/adr/0012-idempotency-and-resumable-runs.md`, `docs/adr/0011-content-addressed-assets.md`, `docs/adr/0010-provider-plugin-architecture.md`, `docs/adr/0018-shared-models-live-in-core.md`

## Scope

Generate a hero thumbnail for one video as N iterations, show them, pick one, export, and refine through child `iterate` runs that use the picked image as reference.

- **P6.1** `core/services/hero.py` (`HeroService`), `cli/thumb.py` `generate`.
- **P6.2** `thumb pick|show|export`.
- **P6.3** `core/services/iterate.py` (`IterateService`), `thumb iterate`.

## Non-goals

- Playlist batches and resume — Phase 7. Hero runs are small (default N=4) and are not resumable; a failed hero run is re-issued.
- Provider-side variations/seeds beyond what `capabilities.supports_seed` allows.

## Interfaces

Collaborators arrive as Protocols declared beside the service, as `FetchService` does (`core` imports no other package); the names in the signatures are the adapters the CLI passes in. `core` cannot name ORM rows, so persistence is one `HeroStore` Protocol, satisfied by `storage.runs.RunRepository`, which also writes the raw and final assets; the service returns counts and the CLI reads the stored rows back to render them (as `fetch` does), so `thumb generate` and `runs show` print the same view. `registry` is `providers.registry`; `renderer` is `templates.loader.PromptRenderer`; `finalize` is `imaging.finalize.render_final` with `output` bound from `[output]`.

```python
class HeroService:
    def __init__(self, store: HeroStore, registry: ProviderRegistry, renderer: TemplateRenderer, finalize: Finalize, *, logs_dir: Path) -> None: ...
    async def generate(self, spec: RunSpec, *, progress: ProgressSink) -> RunResult
        # RunSpec(video_id, template_ref, provider_key, n, concurrency, seed, vars, out_dir, provider_params)
        # RunResult(run_id, status, iteration_ids, completed, failed, compliance_failed)
        #   .exit_code -> ExitCode, .error() -> the ThumbforgeError the CLI raises after printing

class IterateService:
    async def iterate(self, parent: Run | Iteration, *, n: int, prompt_append: str | None, vars: dict[str, str], from_picked: bool, progress: ProgressSink) -> RunResult

# storage.runs.RunRepository, over ORM rows, so `core` does not name them
def pick(run_id: str, target: int | str) -> Iteration          # ordinal or iteration id
def resolve_target(ref: str) -> Run | Iteration                # a run id or an iteration id
def export(target: Run | Iteration, to: Path, *, raw: bool) -> list[Path]
```

Idempotency key (`PLAN.md` §6, verbatim): `sha256(template.spec_hash + provider_profile.id + video.youtube_id + str(part_number) + rendered_prompt + str(seed) + reference_asset.sha256)[:32]`, stored on `iteration.idempotency_key UNIQUE`. For hero runs `part_number` is `""` and the ordinal is folded into `seed` (or `str(ordinal)` when the provider has no seed) so N iterations get N keys. Iteration `k` of `--seed S` uses seed `S + k - 1` (`S` defaults to 0) when the provider supports seeds. A hero run is neither deduplicated nor resumable, so its key also folds in the run id as a final term: without it, re-issuing a failed run (the intended recovery) would collide on `iteration.idempotency_key UNIQUE`.

Commands (`PLAN.md` §5.2):

| Command                                               | Key flags                                                                                                                          | Output                                                                                                                   | Exit          |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------- |
| `thumbforge thumb generate <video>`                   | `--template NAME[@VERSION]`, `--provider KEY`, `--n 4`, `--concurrency 1`, `--seed N`, `--var key=value` (repeatable), `--out DIR` | creates hero `run` + N iterations; preview grid; prints run id                                                           | 0, 3, 4, 5, 6 |
| `thumbforge thumb iterate <run\|iteration>`           | `--n 4`, `--prompt-append TEXT`, `--var …`, `--from-picked`                                                                        | child run (`kind='iterate'`, `parent_run_id`), same template/provider; reference = picked or given iteration's raw asset | 0, 3, 4, 6    |
| `thumbforge thumb pick <run> <ordinal\|iteration-id>` |                                                                                                                                    | marks picked; un-picks siblings                                                                                          | 0, 2, 3       |
| `thumbforge thumb show <run>`                         | `--columns 2`                                                                                                                      | preview grid with ordinals, picked marker, compliance status                                                             | 0, 3          |
| `thumbforge thumb export <run\|iteration>`            | `--to DIR`, `--raw`                                                                                                                | copies the final (or raw) asset of every completed iteration of a run, or of one iteration, into DIR                     | 0, 2, 3       |

`thumbforge runs show <run>` (minimal, P6.1; P7.4 adds `list|resume|cancel|delete`) prints the run header and the iteration table of a stored run, or the same as `--json` with each iteration's full idempotency key, assets and compliance report; exit `3` for an unknown run.

## Behaviour

1. `thumb generate V` resolves the video (Phase 2 repos; exit `3` if unknown), template (`[general] default_template` unless `--template`), provider (`[general] default_provider` unless `--provider`); creates or reuses a `provider_profile` snapshot (`name = "<key>@<version>:<params sha>"`); renders the prompt once; creates `run(kind='hero', status='running', video_id=V)` and N `pending` iterations with distinct keys; binds `run_id` in structlog contextvars.
2. Iterations run under `asyncio.Semaphore(min(--concurrency, capabilities.max_concurrency))`, which guards the provider call only (finalizing and storing overlap with the next generation), with the Phase 3 retry policy; each success is stored as the `raw` asset, passed through `finalize` (Phase 5 `render_final`), and the returned bytes are stored as the `final` asset with `compliant` and `compliance_report_json` set from the report — stored even when non-compliant, so the user can inspect it → `raw_asset_id`, `final_asset_id`, `compliant`. Provider stdout/stderr land in `<state_dir>/logs/runs/<run_id>/<idempotency_key>.{out,err}` (the provider names them by the request key, not the iteration id).
3. Run status at the end: all completed → `completed`, exit `0`; some failed → `failed`, exit `6` and the message from `PLAN.md` §5.3; all failed → `failed`, exit `4`. A compliance failure on an otherwise successful iteration marks that iteration `failed` with `error_text` from the report. When every failure is a compliance failure, exit `5` replaces both `6` and `4`.
4. `--out DIR` additionally copies the final asset of every completed iteration to `DIR/<youtube_id>-<ordinal>.<ext>`; a non-compliant final stays inspectable in the store but is not copied.
5. `thumb pick R 2` sets `picked = 1` on ordinal 2 and `0` on siblings in one statement, so a run never has two picks; the argument is an ordinal or the id of one of that run's iterations. Picking again moves the pick; picking the picked iteration changes nothing. An unknown run, ordinal or iteration id exits `3`. An iteration that is not `completed` exits `2` with a hint to pick a completed one: a `failed` iteration (compliance failures included) has no usable final. `--json` prints `{run_id, picked: {id, ordinal}}`.
6. `thumb iterate R --n 4 --prompt-append "warmer colours"` creates `run(kind='iterate', parent_run_id=R, video_id=R.video_id, reference_asset_id=<picked or given iteration>.raw_asset_id)`, re-renders the prompt with the append and `vars`, and passes the reference path in `GenerationRequest.reference_images`. Without a picked iteration and without an explicit iteration id, exit `2` with hint `thumb pick`. `--from-picked` walks to the newest picked iteration in the parent chain.
7. `thumb export` copies (never moves) assets; `--raw` selects `raw_asset_id`. `--to` is always a directory, created when missing, and the files are named `<youtube_id>-<ordinal>.<ext>` like `generate --out`. A run id exports every `completed` iteration; an iteration id exports that one. Export does not need a pick. A target with no `completed` iteration exits `2` with a hint (`runs show`); an unknown id exits `3`; a destination that cannot be written exits `1` (`AssetError`). `--json` prints `{run_id, iteration_id, raw, files}`.
8. `thumb show R` prints the run header and iteration table that `generate` prints (the picked iteration is starred in the table), then a grid with one tile per iteration that has a final, in ordinal order, captioned `#<ordinal>`, ` ★` when picked, then `✔` or `✘` for compliance; a non-compliant final is drawn so it can be inspected. A console that cannot draw colour gets the numbered path table instead, led by the same captions. `--json` prints the document `runs show` prints, each iteration carrying `picked`.

## Acceptance criteria

- `thumbforge thumb generate dQw4w9WgXcQ --provider fake --n 4` prints the run header, a 4-row iteration table with `completed` and `✔`, the preview grid, and `Pick one with: thumbforge thumb pick <run> <ordinal>`; exit `0`; `runs show <run>` lists 4 iterations with distinct `idempotency_key`.
- Same command with `--var fail=[[FAIL_PERMANENT]]` on a template that interpolates `{{ vars.fail }}` into the prompt yields 4 `failed` rows and exit `4`.
- With a FakeProvider `delay_ms=500` and `--concurrency 4`, wall time for `--n 4` is below 1.5 s; with `--concurrency 1` above 2 s.
- `thumbforge thumb pick <run> 2` then `thumb show <run>` marks ordinal 2 with `★`; `thumb pick <run> 9` exits `3`.
- `thumbforge thumb iterate <run> --n 2` creates a run with `kind = iterate`, `parent_run_id = <run>`, `reference_asset_id = <picked>.raw_asset_id`; FakeProvider output shows the reference thumbnail in a corner (pixel check at `(0,0)` region).
- `thumbforge thumb export <run> --to out/` writes `out/dQw4w9WgXcQ-1.jpg` … `-4.jpg`, byte for byte the stored finals; `--raw` writes `.png` for FakeProvider.
- `thumbforge --json thumb generate …` prints one JSON object with `run.id`, `iterations[]`, `exit_code`.

## Test plan

- Unit: `HeroService` with FakeProvider on in-memory DB and `tmp_path` data dir — key uniqueness, status roll-up matrix (all ok / partial / all failed / compliance-only failure), semaphore concurrency timing, `--out` copies; `IterateService` reference resolution (picked, explicit id, `--from-picked` chain, none → exit `2`); `pick`/`export` via `CliRunner`.
- Contract: none new; relies on the Phase 3 contract suite.
- Integration (`-m integration`): one `thumb generate --provider antigravity --n 1` after S1–S4 close.
- Golden: none (Phase 5 covers overlay pixels).

## Open spikes

- **S4** reference images — if Antigravity ignores reference paths, `thumb iterate` with `--provider antigravity` warns that the reference was not used (`capabilities.supports_reference_image = False`) and proceeds prompt-only.
- **S10** preview rendering for `thumb show` (shared with Phase 5).
