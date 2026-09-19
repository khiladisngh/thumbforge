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

## Knowledge graph

Regenerate after any structural source change and commit `graphify-out/` (see `AGENTS.md`):

```
graphify extract . --code-only && graphify cluster-only . --no-label
```

CI runs an advisory drift check (`graphify drift (advisory)`, `continue-on-error`, not one of
branch protection's required contexts) that re-extracts and compares node/edge **sets** — never a
byte diff, since `graph.json` embeds `built_at_commit`. Reproduce it locally by diffing a copy of
the committed graph against a fresh extract; keep scratch files under the ignored `.pytest_tmp/`:

```
cp graphify-out/graph.json .pytest_tmp/committed-graph.json
graphify extract . --code-only
uv run python scripts/check_graph_drift.py .pytest_tmp/committed-graph.json graphify-out/graph.json
```

Regenerate as the **last** step before `git add`, after formatters have run — otherwise their edits
shift line spans and reintroduce drift.

### Rebuild from scratch when counts diverge

`graphify extract` is incremental and **never prunes symbols deleted from source**, so the
committed graph accumulates staleness that neither the incremental extract nor the CI drift check
can see — the check compares incrementally on top of whatever is already committed, so a phantom
present in both sides cancels out. A clean rebuild is the ground truth:

```
rm -rf graphify-out
graphify extract . --code-only && graphify cluster-only . --no-label
```

Measured at `3ff0f30`, the incremental graph had drifted to 612 nodes/1179 edges against 577/1282
from scratch. The clean build has *fewer* nodes but *more* edges, and is strictly more accurate: it
had dropped a phantom node for the `AssetStoreError` alias deleted two PRs earlier, added the
`test_ids.py`/`test_render.py` module nodes the stale graph was missing, and resolved 11 unresolved
import placeholders (`imports_from thumbforge_cli_errors`) into real cross-module edges
(`imports src_thumbforge_cli_errors_handle_errors`).

Because `AGENTS.md` points every agent at `GRAPH_REPORT.md` first, a stale graph misleads later
work. Rebuild clean after deleting or renaming exported symbols, and whenever node/edge counts
diverge noticeably from the committed graph. Note that a clean rebuild is a large diff and shifts
ids, so give it its own PR rather than burying it in a feature change.

## Documentation

- Decisions → ADR (`docs/adr/`, use `0000-template.md`; supersede, never edit an Accepted decision).
- Behaviour → phase spec (`docs/specs/`).
- Spike results → `docs/spikes/<topic>.md`; close the item in `OPEN_QUESTIONS.md`.
- Terms → `GLOSSARY.md`.
- Docs are published with zensical to GitHub Pages on every merge to `main`.
