# Roadmap

Each task is one PR. Task lines follow `P<phase>.<n> <title> — deps: […] — AC: <observable criteria>`. A task may start only when its deps are merged. Every task links to the phase spec in `docs/specs/` and, where noted, to a spike in `OPEN_QUESTIONS.md`.

Branch naming: `feat/P3.2-fake-provider`, `infra/P0.5-github`, `spike/S1-agy-image-tool`.

## Phase 0 — Infrastructure (no runtime code)

Spec: `docs/specs/phase-0-infra.md`

- P0.1 Repo bootstrap — deps: none — AC: `uv init --package --python 3.14` layout committed; `pyproject.toml` has `requires-python = ">=3.14"`, name `thumbforge`, `[project.scripts] thumbforge = "thumbforge.cli.app:main"`; `.editorconfig`, `.gitignore`, `LICENSE` (MIT); `uv sync --locked` passes; `uv run thumbforge --version` prints `0.0.0`.
- P0.2 Quality tooling — deps: P0.1 — AC: ruff, pyright, pytest, pytest-asyncio, coverage, import-linter as dev deps; `.pre-commit-config.yaml` with ruff, ruff-format, pyright, mirrors-prettier (markdown/yaml/json), `uv lock --check`, end-of-file-fixer, conventional-pre-commit; `.prettierrc` + `.prettierignore`; `pre-commit run --all-files` green on the empty package. Blocked on spike S13 for the prettier `rev`.
- P0.3 Agent instruction files — deps: P0.1 — AC: `AGENTS.md` per the draft; `CLAUDE.md` and `GEMINI.md` each contain only the pointer line.
- P0.4 Docs skeleton + zensical site — deps: P0.1 — AC: `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, `docs/TESTING.md`, `docs/GLOSSARY.md`, `docs/adr/0000-template.md`, ADRs 0001–0016, `docs/specs/README.md`; `zensical.toml` with nav covering ARCHITECTURE/ROADMAP/CONVENTIONS/TESTING/GLOSSARY/adr/specs; `uv run zensical build` succeeds with zero warnings. Blocked on spike S14 for mermaid rendering.
- P0.5 GitHub setup — deps: P0.2 — AC: `.github/PULL_REQUEST_TEMPLATE.md` (spec link, checklist, test evidence); issue templates `feature.yml`, `bug.yml`, `spike.yml`; `.github/labels.yml` + sync workflow; `CODEOWNERS`; `ci.yml` running `uv sync --locked`, `ruff check`, `ruff format --check`, `pyright`, `pytest --cov --cov-fail-under=80`, `uv run zensical build` on `3.14` × `ubuntu-latest, windows-latest`; `docs.yml` deploying the zensical site to GitHub Pages on push to `main`; `release.yml` (tag `v*` → `uv build` → PyPI trusted publishing, `git-cliff` changelog); `docs/CONVENTIONS.md` documents branch protection (PR required, 1 review, CI green, linear history, no force-push). Needs decision D5.
- P0.6 graphify integration — deps: P0.3, spike S9 — AC: `graphify-out/` committed (minus `cost.json`), `.agents/skills/` present, `AGENTS.md` "Before you start" points at `graphify-out/GRAPH_REPORT.md`; regeneration method (hook / CI / manual) recorded in `AGENTS.md`.
- P0.7 Phase 0 + Phase 1 specs — deps: P0.4 — AC: `docs/specs/phase-0-infra.md` and `docs/specs/phase-1-skeleton.md` complete with acceptance criteria; later phase specs present as outlines.

## Phase 1 — Skeleton (config, DB, logging, errors)

Spec: `docs/specs/phase-1-skeleton.md`

- P1.1 Settings — deps: P0.7 — AC: `settings.py` (pydantic-settings, TOML at `user_config_dir("thumbforge")/config.toml`, env prefix `THUMBFORGE_`, nested delimiter `__`); `thumbforge config init|show|path|set`; `thumbforge --json config show` prints JSON; secret-looking TOML keys rejected with `SettingsError`.
- P1.2 Logging — deps: P1.1 — AC: `logging.py` with `configure_logging` / `get_logger` (structlog, processor chain and stdlib bridge per PLAN.md §7.3); `thumbforge -vv db status` prints console-rendered lines; `thumbforge --json db status 2>err.jsonl` yields one JSON object per line; rotating JSON log file under `user_state_dir`.
- P1.3 DB engine + Alembic — deps: P1.1 — AC: `storage/db.py` (WAL, `foreign_keys=ON`), `storage/models.py` with all tables from PLAN.md §3, initial Alembic migration, `thumbforge db init|upgrade|status|path|vacuum`; `db init` creates the DB at Alembic head.
- P1.4 Asset store — deps: P1.3 — AC: `AssetStore.put/path_for/verify`; identical bytes dedupe; tmp→fsync→rename write path; unit tests with `tmp_path`.
- P1.5 Errors + root CLI — deps: P1.2 — AC: `core/errors.py` hierarchy and `cli/_errors.py` mapping per PLAN.md §5.1/§7.1; root Typer app with global flags; unknown command exits `2`; a raised `NotFoundError` exits `3` with `hint` on stderr.
- P1.6 Import-linter contracts — deps: P1.5 — AC: `[tool.importlinter]` contracts encode PLAN.md §2.2; `uv run lint-imports` green and wired into CI.

## Phase 2 — YouTube fetch

Spec: `docs/specs/phase-2-youtube-fetch.md`

- P2.1 MetadataSource protocol + models — deps: P1.5 — AC: `MetadataSource` Protocol (added as `sources/base.py`, moved to `core/sources.py` in P2.3 so `core.services` can consume it); `core/models.py` `ChannelMeta`, `PlaylistMeta`, `VideoMeta`; URL classifier (`video | playlist | channel`) with unit tests.
- P2.2 YtDlpSource with recorded fixtures — deps: P2.1, spike S11 — AC: `sources/ytdlp.py` using `extract_flat="in_playlist"`; fixture recorder marked `integration` writes `tests/fixtures/ytdlp/*.json`; unit tests replay fixtures with no network.
- P2.3 Repositories + fetch/video/playlist commands — deps: P1.3, P2.2 — AC: upsert semantics for channel/playlist/video/playlist_item; `thumbforge fetch <url>`, `video list|show`, `playlist list|show [--videos]`; `--refresh` re-fetches; `--json` output.
- P2.4 Playlist renumber — deps: P2.3 — AC: `thumbforge playlist renumber <playlist> --start N [--skip-ids …]` rewrites `part_number` sequentially, skipped videos get NULL; `playlist show --videos` reflects it.

## Phase 3 — Provider layer (Fake + Antigravity)

Spec: `docs/specs/phase-3-providers.md`

- P3.1 Provider protocol + registry — deps: P1.5 — AC: `core/providers.py` `ImageProvider` Protocol and boundary models (placed in `core` because `core.services` consumes them); `providers/registry.py` merging `BUILTIN` with the `thumbforge.providers` entry-point group. Observable: `uv run pytest -q tests/unit/test_provider_registry.py` passes; and real discovery is proven out-of-tree by building a throwaway distribution whose `pyproject.toml` declares `[project.entry-points."thumbforge.providers"] smoke = "tfplug:SmokeProvider"`, then `uv pip install <dist> && uv run python -c "from thumbforge.providers import registry; print(registry.keys())"` prints `['smoke']`, `registry.get('smoke', {...})` returns that class with its config, a `BUILTIN` entry of the same key raises `ProviderRegistryError` (exit 4), and `uv pip uninstall tfplug` returns `keys()` to `[]`.
- P3.2 FakeProvider + contract tests — deps: P3.1 — AC: `providers/fake.py` registered in `BUILTIN`; `uv run pytest -q tests/contract/ tests/unit/test_fake_provider.py` passes. Deterministic to the byte for an identical request; honours the requested size exactly (a property of the fake, not of the interface — the contract suite only asserts the ratio is within 5%); `[[FAIL_TRANSIENT]]`/`[[FAIL_PERMANENT]]` raise the retryable and non-retryable errors and leave no file behind; `params.delay_ms` is awaited so four 120 ms calls gathered finish in well under 480 ms. The contract suite is parametrised over `registry.keys()`, so P3.4's provider is held to it automatically under `-m integration`.
- P3.3 Antigravity spikes S1–S8 — deps: none — AC: `docs/spikes/antigravity.md` records commands, raw outputs, and conclusions for each spike; ADR 0013 status updated.
- P3.4 AntigravityProvider — deps: P3.2, P3.3 — AC: `providers/antigravity.py` + `antigravity_wrapper.j2` implementing PLAN.md §4.3 with any corrections from P3.3; unit tests with a fake `agy` script covering every row of the error-mapping table; `integration`-marked live test.
- P3.5 Provider commands — deps: P3.2 — AC: `thumbforge provider list|check|models|set-key`; `set-key` stores in keyring only.

## Phase 4 — Templates

Spec: `docs/specs/phase-4-templates.md`

- P4.1 Layout spec schema — deps: P1.5 — AC: Pydantic model for the TOML layout spec (canvas, title box, part badge, font, colours, safe margins); `template validate PATH` reports schema errors with exit `2`.
- P4.2 Prompt rendering — deps: P4.1 — AC: Jinja2 environment with `StrictUndefined`, `autoescape=False`; context = video/playlist/part/vars; missing variable → `TemplateError`; `template render NAME --video <id> [--part N]` prints the prompt.
- P4.3 Builtin templates — deps: P4.2 — AC: `bold-title`, `minimal`, `series-parts` shipped under `templates/builtin/`; loaded as `is_builtin=1` version 1 on `db init`.
- P4.4 Template commands + versioning — deps: P4.3, P1.3 — AC: `template list|show|new|import`; importing a changed spec creates version+1; `spec_hash` stable for identical content.

## Phase 5 — Imaging

Spec: `docs/specs/phase-5-imaging.md`

- P5.1 Fit/crop — deps: P1.5 — AC: `imaging/fit.py` resizes/crops any input to the configured 16:9 target (default 1920×1080) with centre crop; unit tests on synthetic images.
- P5.2 Text overlay + golden tests — deps: P4.1, P5.1 — AC: `imaging/overlay.py` renders title and "Part N" badge from the layout spec with the bundled OFL font; `golden`-marked snapshot tests compare against `tests/golden/*.png` with a pixel tolerance.
- P5.3 Compliance check — deps: P5.1 — AC: `imaging/compliance.py` enforces 16:9 ±1 px, width ≥ 1280, JPEG/PNG, ≤ 2 MB default (`--max-bytes` up to 50 MB), sRGB; returns a report stored in `asset.compliance_report_json`; failing asset raises `ComplianceError` (exit `5`).
- P5.4 Rich preview — deps: P5.1, spike S10 — AC: `cli/_render.py` grid preview via `rich-pixels`; degrades to a table when the terminal cannot render.

## Phase 6 — Hero thumbnail + iterations

Spec: `docs/specs/phase-6-hero.md`

- P6.1 HeroService + `thumb generate` — deps: P2.3, P3.2, P4.4, P5.3 — AC: creates hero run + N iterations, runs provider under a semaphore, overlays, checks compliance, stores raw and final assets; exit `6` when some iterations fail; works end-to-end with `fake`.
- P6.2 `thumb pick|show|export` — deps: P6.1 — AC: exactly one picked iteration per run; `show` grid; `export --to PATH [--raw]`.
- P6.3 `thumb iterate` — deps: P6.2 — AC: child run with `parent_run_id`, reference = picked (or given) iteration's raw asset, `--prompt-append` and `--var` applied; `runs show` displays lineage.

## Phase 7 — Playlist batch

Spec: `docs/specs/phase-7-batch.md`

- P7.1 BatchService — deps: P6.2 — AC: idempotency key per PLAN.md §6; existing `completed` keys skipped; `asyncio.Semaphore(min(--concurrency, max_concurrency))`; `--only` and `--max-images` honoured; `--dry-run` prints the plan without provider calls.
- P7.2 Resume / cancel / interrupt — deps: P7.1 — AC: SIGINT marks run `paused`, in-flight iterations `failed` with `error_text="interrupted"`, exit `130`; `runs resume` regenerates only non-completed items (test: 20-item playlist interrupted after 7 resumes with exactly 13 provider calls); stale `running` iterations older than `stale_after_s` retried; `runs cancel` refuses completed runs.
- P7.3 `batch` command + progress — deps: P7.2 — AC: Rich progress with per-item title; summary table; exit `6` on partial, `4` when all fail; `--reference final|raw`.
- P7.4 `runs` commands — deps: P7.1 — AC: `runs list|show|resume|cancel|delete [--assets]`; delete refuses runs referenced by a batch (exit `2`).

## Phase 8 — Polish

Spec: `docs/specs/phase-8-polish.md`

- P8.1 YouTube Data API source — deps: P2.3, decision D7 — AC: optional extra `thumbforge[api]`; `fetch --source api` behind the same `MetadataSource`; key via env/keyring; missing extra or key → `SourceError` with install/set-key hint.
- P8.2 Install docs — deps: P6.1 — AC: `docs/GETTING_STARTED.md` covers `uv tool install thumbforge` and first run; `uv tool install .` puts `thumbforge` on PATH.
- P8.3 Shell completion — deps: P8.2 — AC: `thumbforge --install-completion` documented and smoke-tested on PowerShell, bash, zsh.
- P8.4 Cost report — deps: P7.3 — AC: `thumbforge runs cost <run>` aggregates `iteration.cost_json` (tokens, credits, `no_cost_data` count); `runs show` gains a cost column; `--json` supported.
- P8.5 README + first release — deps: P8.3, P8.4 — AC: README quick start reproduces the three PLAN.md examples using `fake`; `git-cliff` changelog; tag `v0.1.0` runs `release.yml` green.
