# AGENTS.md — canonical instructions for coding agents

This file is the single source of truth for how agents work in this repository. `CLAUDE.md` and `GEMINI.md` only point here. Keep this file current: when structure, commands or conventions change, update it in the same PR.

## Project map

```
src/thumbforge/
  cli/          Typer apps only; no business logic; Rich rendering in cli/_render.py; error→exit mapping in cli/_errors.py
  core/         domain models (Pydantic v2), error hierarchy, id/hash helpers, services (hero, iterate, batch, compliance)
  providers/    ImageProvider protocol, capabilities, registry (entry points "thumbforge.providers"), fake.py, antigravity.py
  sources/      MetadataSource protocol; ytdlp.py (default); youtube_api.py (optional extra)
  storage/      SQLAlchemy 2.0 models, repositories, Alembic migrations, content-addressed AssetStore
  templates/    layout spec schema (TOML), Jinja2 prompt rendering, builtin templates
  imaging/      Pillow fit/crop, text overlay, YouTube compliance check, bundled font
  settings.py   pydantic-settings (TOML + env THUMBFORGE_*), platformdirs paths
  logging.py    structlog configuration
tests/          unit/ contract/ integration/ golden/ fixtures/
docs/           ARCHITECTURE.md ROADMAP.md CONVENTIONS.md TESTING.md GLOSSARY.md adr/ specs/ spikes/
graphify-out/   generated codebase knowledge graph (committed; cache/ and cost.json ignored)
```

Dependency rule: `cli → core, storage, providers, sources, templates, imaging`; `core` imports no other internal **package**; every other package may import `core` only; nothing imports `cli`. Within `core`, modules may import each other — `core.models` needs `core.enums`, services need `core.models` — but `core.enums`, `core.errors` and `core.ids` are leaves and import nothing from `core`. Enforced by import-linter.

## Commands (always via uv)

| Purpose                                                  | Command                                                                |
| -------------------------------------------------------- | ---------------------------------------------------------------------- |
| Install / sync                                           | `uv sync --locked`                                                     |
| Run the CLI                                              | `uv run thumbforge …`                                                  |
| Lint + format Python                                     | `uv run ruff check . && uv run ruff format .`                          |
| Type check                                               | `uv run pyright`                                                       |
| Unit + contract tests                                    | `uv run pytest -q`                                                     |
| Opt-in live tests                                        | `uv run pytest -m integration`                                         |
| Golden image tests                                       | `uv run pytest -m golden`                                              |
| Import contracts                                         | `uv run lint-imports`                                                  |
| New migration                                            | `uv run alembic revision --autogenerate -m "<message>"`                |
| Docs preview                                             | `uv run zensical serve`                                                |
| Docs build (CI gate)                                     | `uv run zensical build`                                                |
| All hooks (incl. prettier for `*.md`, `*.yml`, `*.json`) | `pre-commit run --all-files`                                           |
| Refresh knowledge graph                                  | `graphify extract . --code-only && graphify cluster-only . --no-label` |

Never use `pip`, `poetry`, `npm` inside the repo, or `python -m` without `uv run`.

## Before you start

1. Read `graphify-out/GRAPH_REPORT.md` for the current map of the codebase.
2. Ask the graph before grepping: `graphify query "<question>"`, `graphify explain "<symbol>"`, `graphify path A B`.
3. Read `docs/ARCHITECTURE.md` and the spec linked from your task (`docs/specs/phase-N-*.md`).
4. Check `OPEN_QUESTIONS.md` — if your task depends on an open spike or decision, stop and say so.

## How to pick up a task

1. Find the task id in `docs/ROADMAP.md` (e.g. `P3.2`). Confirm every dependency is merged.
2. Open or claim the GitHub issue for it; the issue must link the spec.
3. Branch: `feat/P3.2-fake-provider`, `infra/P0.5-github`, `fix/<issue>-<slug>`, `spike/S1-agy-image-tool`.
4. Implement only that task. If the spec is wrong or incomplete, update the spec in the same PR and say why in the PR description.
5. Open a PR using the template; fill in the test evidence section with real command output.

## Conventions

- Python 3.14, src layout, full type hints, `pyright` strict on `src/`.
- Pydantic v2 models at boundaries (CLI input, provider I/O, settings); `dataclass(frozen=True, slots=True)` for internal value objects.
- `StrEnum` for enumerations; `match` for dispatch on enums/status; `pathlib.Path` everywhere, never string paths.
- Async only where it earns its keep: provider calls, metadata fetch, batch fan-out (bounded by `asyncio.Semaphore`). Services expose async APIs; the CLI calls `asyncio.run` once.
- Logging: `from thumbforge.logging import get_logger; log = get_logger(__name__)`. Never `print()` outside `cli/_render.py`. Logs go to stderr; Rich output goes to stdout.
- Errors: raise a `ThumbforgeError` subclass with `code`, `exit_code`, `hint`. Never `sys.exit` outside `cli/_errors.py`.
- Secrets: env var or keyring only. Never in the DB, TOML, logs, or fixtures.
- Schema changes always ship with an Alembic migration.
- Commit messages: Conventional Commits (`feat(providers): add FakeProvider`, `fix(batch): …`, `docs(adr): …`, `chore(ci): …`).
- One concern per PR; small and reviewable.

## Definition of done

- Spec or issue linked in the PR.
- Tests added at the right layer: unit (no network, FakeProvider / recorded fixtures), contract (every provider), `integration` marker for live systems, `golden` for image output.
- `uv run ruff check .`, `uv run ruff format --check .`, `uv run pyright`, `uv run pytest -q`, `uv run lint-imports`, `uv run zensical build` all green locally and in CI.
- Docs updated in the same PR when behaviour or structure changed: `docs/ARCHITECTURE.md`, the phase spec, `AGENTS.md`, ADR if a decision changed.
- Knowledge graph refreshed when source structure changed: `graphify extract . --code-only && graphify cluster-only . --no-label`, then commit `graphify-out/`. Installed once with `uv tool install graphifyy`. CI runs an advisory drift check (`scripts/check_graph_drift.py`); regeneration is manual, not hooked.
- CodeRabbit review comments on the PR resolved or explicitly answered (advisory, not a merge gate). Rules live in `.coderabbit.yaml`; `@coderabbitai review` re-runs it. If a comment is wrong for this project, reply with the reason instead of silently dismissing it.

## Updating docs

- Architecture decisions → new ADR in `docs/adr/` using `0000-template.md`; never edit an Accepted ADR's decision — supersede it.
- Behaviour → the phase spec under `docs/specs/`.
- Terms → `docs/GLOSSARY.md`.
- Spike results → `docs/spikes/<topic>.md` and close the item in `OPEN_QUESTIONS.md`.

## Never do

- Use `pip`, `poetry`, or add a Node project to the repo.
- Put business logic in `cli/`.
- Store secrets in the DB, TOML config, logs, or test fixtures.
- Use `print()` for logging.
- Skip an Alembic migration for a schema change.
- Hit the network or a real provider from unit tests.
- Commit `graphify-out/cache/`, `graphify-out/cost.json`, or the built `site/` directory.
- Mark a spike as resolved without recorded command output.
- Widen a PR beyond its ROADMAP task.
