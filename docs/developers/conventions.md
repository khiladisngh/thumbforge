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

## Commits and pushing

- Conventional Commits: `feat(scope): …`, `fix(scope): …`, `docs: …`, `chore(ci): …`, `refactor: …`, `test: …`. Scope = package (`providers`, `batch`, `cli`, …) or area (`ci`, `adr`).
- One roadmap task = one commit; name the ROADMAP task in the subject or body.
- Update docs, specs and `AGENTS.md` in the same commit when behaviour or structure changes.
- Solo workflow, no pull requests: run both local CI legs (`scripts/ci-local.sh`, `scripts/ci-local.cmd`) and read your own diff before pushing, then `git fetch origin && git rebase origin/main && git push origin HEAD:main`. History stays linear: rebase, never merge, never force-push.
- Check the remote run after the push (`gh run list --branch main --limit 3`); a red run is fixed forward immediately.

## Knowledge graph

Regenerate after any structural source change and commit `graphify-out/` (see `AGENTS.md`):

```
graphify extract . --code-only && graphify cluster-only . --no-label
```

CI runs an advisory drift check (`graphify drift (advisory)`, `continue-on-error`, not one of
the required status checks) that re-extracts and compares the **declaration node set** —
never a byte diff, since `graph.json` embeds `built_at_commit`. It answers one question: was a
symbol added, removed or renamed without re-running the extract. A failure names the symbols.

It deliberately ignores everything else in the graph, because everything else varies between
machines without the source changing. Measured over five consecutive false alarms (issue #26): CI
resolves imports less completely than a local run and invents placeholder nodes
(`thumbforge_core_errors` where a local extract has `src_thumbforge_core_errors`); external symbol
nodes depend on what is installed; `*_rationale_<line>` ids embed a line number, so moving a comment
renames the node. Edges are dropped entirely — they have no environment-independent form, since CI
can be _missing_ an edge between two fully resolved nodes when it resolved that import to a module
placeholder instead. The cost is that a changed call edge between unchanged symbols goes unnoticed,
which is acceptable given the check already cannot see the staleness class described below.

Reproduce it locally by diffing a copy of the committed graph against a fresh extract; keep scratch
files under the ignored `.pytest_tmp/`:

```
mkdir -p .pytest_tmp
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
from scratch. The clean build has _fewer_ nodes but _more_ edges, and is strictly more accurate: it
had dropped a phantom node for the `AssetStoreError` alias deleted two commits earlier, added the
`test_ids.py`/`test_render.py` module nodes the stale graph was missing, and resolved 11 unresolved
import placeholders (`imports_from thumbforge_cli_errors`) into real cross-module edges
(`imports src_thumbforge_cli_errors_handle_errors`).

Because `AGENTS.md` points every agent at `GRAPH_REPORT.md` first, a stale graph misleads later
work. Rebuild clean after deleting or renaming exported symbols, and whenever node/edge counts
diverge noticeably from the committed graph. Note that a clean rebuild is a large diff and shifts
ids, so give it its own commit rather than burying it in a feature change.

## Documentation

- Decisions → ADR (`docs/adr/`, use `0000-template.md`; supersede, never edit an Accepted decision).
- Behaviour → phase spec (`docs/specs/`).
- Spike results → `docs/spikes/<topic>.md`; close the item in `OPEN_QUESTIONS.md`.
- Terms → [Glossary](glossary.md) (`docs/developers/glossary.md`).
- Docs are published with zensical to GitHub Pages on every push to `main`.
