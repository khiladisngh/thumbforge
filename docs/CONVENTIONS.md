# Conventions

`AGENTS.md` is canonical; this page expands on it for humans.

## Code

- Python 3.14, `src/` layout, `uv` for everything (`uv sync --locked`, `uv run …`, `uv tool install`).
- Full type hints; `pyright` strict on `src/`. Prefer `Protocol` over ABCs for interfaces.
- Pydantic v2 models at boundaries (CLI input, provider I/O, settings); `dataclass(frozen=True, slots=True)` for internal value objects.
- `StrEnum` for enumerations, `match` for dispatch, `pathlib.Path` for every path.
- Async only in providers, sources and batch fan-out; the CLI calls `asyncio.run` once.
- Logging via `thumbforge.logging.get_logger(__name__)`; never `print()` outside `cli/_render.py`.
- Errors: raise a `ThumbforgeError` subclass; `cli/_errors.py` owns exit codes (`PLAN.md` §5.1).
- Secrets: env var or keyring only.
- Every schema change ships with an Alembic migration.

## Formatting and linting

- `ruff` lints and formats Python (`line-length = 100`).
- `prettier` formats Markdown, YAML and JSON only, via the pre-commit hook. No Node project in the repo.
- `pre-commit run --all-files` must be green before pushing.

## Commits and PRs

- Conventional Commits: `feat(scope): …`, `fix(scope): …`, `docs: …`, `chore(ci): …`, `refactor: …`, `test: …`. Scope = package (`providers`, `batch`, `cli`, …) or area (`ci`, `adr`).
- One concern per PR; link the ROADMAP task or issue; fill in the PR template's test-evidence section with real output.
- Update docs, specs and `AGENTS.md` in the same PR when behaviour or structure changes.
- Green CI required. Squash-merge; the squash title must itself be a Conventional Commit (it feeds the changelog).
- **CodeRabbit** reviews every non-draft PR automatically, provided the CodeRabbit GitHub App is installed on and authorised for the repository (free for public repositories); `.coderabbit.yaml` alone does nothing without it. Reviews are advisory — they do not gate merges — but resolve or explicitly reject each comment before merging. The rules mirror this page: layering, typing, structlog-only logging, `ThumbforgeError` exit codes, migrations for schema changes, and no network in unit tests. Useful commands in a PR comment: `@coderabbitai review` (re-review), `@coderabbitai resolve` (close its comments), `@coderabbitai configuration` (dump the effective config). When a review comment is wrong for this project, reply explaining why — CodeRabbit stores the learning for later PRs.

## Documentation

- Decisions → ADR (`docs/adr/`, use `0000-template.md`; supersede, never edit an Accepted decision).
- Behaviour → phase spec (`docs/specs/`).
- Spike results → `docs/spikes/<topic>.md`; close the item in `OPEN_QUESTIONS.md`.
- Terms → `GLOSSARY.md`.
- Docs are published with zensical to GitHub Pages on every merge to `main`.
