# Phase 0 — Infrastructure

Status: Implemented (P0.1–P0.7)
ROADMAP tasks: P0.1, P0.2, P0.3, P0.4, P0.5, P0.6, P0.7
ADRs: `docs/adr/0001-python-and-uv.md`, `docs/adr/0009-quality-tooling.md`, `docs/adr/0016-zensical-docs-site.md`

## Scope

Phase 0 produces a repository that a coding agent can work in safely before a single line of feature code exists: package skeleton, quality gates, agent instructions, docs site, GitHub automation, and the graphify knowledge graph. The only runtime code allowed is the `__version__` shim needed for `thumbforge --version`.

Deliverables, grouped by task:

- **P0.1 bootstrap** — `pyproject.toml`, `uv.lock`, `src/thumbforge/__init__.py`, `src/thumbforge/__main__.py`, `.editorconfig`, `.gitignore`, `LICENSE` (MIT, decision D5), `README.md`.
- **P0.2 quality tooling** — `.pre-commit-config.yaml`, `.prettierrc`, `.prettierignore`, `[tool.*]` tables, `tests/conftest.py`, `tests/test_version.py`.
- **P0.3 agent instructions** — `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
- **P0.4 docs** — `docs/index.md`, `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, `docs/TESTING.md`, `docs/GLOSSARY.md`, `docs/ROADMAP.md`, `docs/adr/0000-template.md`, ADRs 0001–0016, `zensical.toml`.
- **P0.5 GitHub** — `.github/PULL_REQUEST_TEMPLATE.md`, `.github/ISSUE_TEMPLATE/{feature,bug,spike}.yml`, `.github/CODEOWNERS`, `.github/labels.yml`, `.github/workflows/{ci,docs,release}.yml`, `docs/BRANCHING.md`.
- **P0.6 graphify** — `graphify-out/` committed, `.agents/skills/` committed, hooks per spike S9.
- **P0.7 specs** — `docs/specs/README.md`, `phase-0-infra.md`, `phase-1-skeleton.md` (this tree).

## Non-goals

- No settings, logging, DB, CLI sub-commands — Phase 1 (`phase-1-skeleton.md`).
- No provider or yt-dlp code; no network access anywhere in Phase 0.
- No PyPI publish on tag until decision D5 confirms publishing; `release.yml` ships with the publish job present but the workflow is only triggered by tags, which nobody pushes before D5.
- Python 3.15 in the CI matrix — spike S12.

## Interfaces

### File inventory

| Path                                                         | Purpose                                                                                                                                           | Task      |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| `pyproject.toml`                                             | Project metadata, dependencies, `[project.scripts] thumbforge = "thumbforge.cli.app:main"`, all `[tool.*]` tables below                           | P0.1/P0.2 |
| `uv.lock`                                                    | Locked resolution; CI runs `uv sync --locked`                                                                                                     | P0.1      |
| `src/thumbforge/__init__.py`                                 | `__version__ = importlib.metadata.version("thumbforge")`                                                                                          | P0.1      |
| `src/thumbforge/__main__.py`                                 | `from thumbforge.cli.app import main; main()` — in Phase 0 `cli/app.py` contains only the root Typer app with `--version`                         | P0.1      |
| `.editorconfig`                                              | `indent_style = space`, `indent_size = 4` (py) / `2` (yaml, toml, json, md), `end_of_line = lf`, `insert_final_newline = true`, `charset = utf-8` | P0.1      |
| `.gitignore`                                                 | Python/uv defaults plus `site/`, `graphify-out/cost.json`, `.coverage`, `htmlcov/`, `*.log`, `.venv/`                                             | P0.1      |
| `LICENSE`                                                    | MIT, copyright holder from D5                                                                                                                     | P0.1      |
| `README.md`                                                  | One-screen pitch, install (`uv tool install thumbforge`), links to docs site                                                                      | P0.1      |
| `.pre-commit-config.yaml`                                    | Hook list below                                                                                                                                   | P0.2      |
| `.prettierrc`                                                | Prettier options below                                                                                                                            | P0.2      |
| `.prettierignore`                                            | Prettier exclusions below                                                                                                                         | P0.2      |
| `tests/conftest.py`                                          | Empty fixtures module; establishes `tests/` as the pytest root                                                                                    | P0.2      |
| `tests/test_version.py`                                      | Asserts `thumbforge --version` via `typer.testing.CliRunner` prints `thumbforge 0.0.0`                                                            | P0.2      |
| `AGENTS.md`                                                  | Canonical instructions for coding agents                                                                                                          | P0.3      |
| `CLAUDE.md`, `GEMINI.md`                                     | Single line: `Read AGENTS.md; it is the canonical instruction file.`                                                                              | P0.3      |
| `docs/index.md`                                              | Docs site landing page; links to every top-level doc                                                                                              | P0.4      |
| `docs/ARCHITECTURE.md`                                       | `PLAN.md` §2 (layout, dependency rule, data-flow diagram) extracted                                                                               | P0.4      |
| `docs/CONVENTIONS.md`                                        | Code conventions (mirrors `AGENTS.md` Conventions, longer form)                                                                                   | P0.4      |
| `docs/TESTING.md`                                            | Test layers, markers, fixture recording procedure                                                                                                 | P0.4      |
| `docs/GLOSSARY.md`                                           | hero, iteration, run, asset, template, provider profile, idempotency key, part number                                                             | P0.4      |
| `docs/ROADMAP.md`                                            | Phase/task list                                                                                                                                   | P0.4      |
| `docs/adr/0000-template.md`, `0001`–`0016`                   | Decision records                                                                                                                                  | P0.4      |
| `docs/specs/`                                                | This directory                                                                                                                                    | P0.7      |
| `zensical.toml`                                              | Docs site config below                                                                                                                            | P0.4      |
| `.github/PULL_REQUEST_TEMPLATE.md`                           | PR checklist below                                                                                                                                | P0.5      |
| `.github/ISSUE_TEMPLATE/feature.yml`, `bug.yml`, `spike.yml` | Issue forms                                                                                                                                       | P0.5      |
| `.github/CODEOWNERS`                                         | `* @<owner>` (D5)                                                                                                                                 | P0.5      |
| `.github/labels.yml`                                         | Label list below; applied by a manual `gh label` script documented in `docs/BRANCHING.md`                                                         | P0.5      |
| `.github/workflows/ci.yml`                                   | Lint/type/test/docs on PR and push                                                                                                                | P0.5      |
| `.github/workflows/docs.yml`                                 | Build + deploy docs to GitHub Pages                                                                                                               | P0.5      |
| `.github/workflows/release.yml`                              | Tag → build → PyPI (proposal)                                                                                                                     | P0.5      |
| `docs/BRANCHING.md`                                          | Branch protection, labels script, release procedure                                                                                               | P0.5      |
| `graphify-out/graph.html`, `GRAPH_REPORT.md`, `graph.json`   | Knowledge graph (committed); `cost.json` ignored                                                                                                  | P0.6      |
| `.agents/skills/`                                            | Written by `graphify install --project --platform agents`                                                                                         | P0.6      |

### `pyproject.toml`

```toml
[project]
name = "thumbforge"
version = "0.0.0"
description = "Generate consistent, spec-compliant YouTube thumbnails from a hero image and a playlist."
readme = "README.md"
requires-python = ">=3.14"
license = "MIT"
dependencies = []          # Phase 1 adds typer, rich, pydantic-settings, platformdirs, sqlalchemy, alembic, structlog, tenacity, keyring

[project.scripts]
thumbforge = "thumbforge.cli.app:main"

[project.entry-points."thumbforge.providers"]
# populated in Phase 3: fake = "thumbforge.providers.fake:FakeProvider"

[dependency-groups]
dev = [
  "ruff",
  "pyright",
  "pytest",
  "pytest-asyncio",
  "pytest-cov",
  "pre-commit",
  "import-linter",
  "zensical",
]

[build-system]
requires = ["uv_build"]
build-backend = "uv_build"

[tool.ruff]
line-length = 100
target-version = "py314"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "TCH", "RUF"]

[tool.pyright]
strict = ["src"]
pythonVersion = "3.14"
venvPath = "."
venv = ".venv"

[tool.pytest.ini_options]
asyncio_mode = "auto"
markers = ["integration", "golden"]
testpaths = ["tests"]
addopts = "-m 'not integration'"

[tool.coverage.run]
source = ["thumbforge"]
branch = true

[tool.coverage.report]
fail_under = 80
show_missing = true

[tool.importlinter]
root_package = "thumbforge"
# contracts are added in Phase 1 (phase-1-skeleton.md)
```

Notes: `ruff` handles both lint and format for Python; `pyright` is the type checker (decision D3, ADR 0009). Version pinning for `zensical` and `graphifyy` is exact in `uv.lock` / `uv tool install` because both are pre-1.0 (`PLAN.md` §9).

### `.prettierrc`

```json
{ "proseWrap": "preserve", "printWidth": 100 }
```

### `.prettierignore`

```
graphify-out/
site/
uv.lock
CHANGELOG.md
```

### `.pre-commit-config.yaml` hook list

| Order | Repo                                 | Hook                      | Notes                                                                                          |
| ----- | ------------------------------------ | ------------------------- | ---------------------------------------------------------------------------------------------- |
| 1     | `astral-sh/ruff-pre-commit`          | `ruff`                    | `args: [--fix]`                                                                                |
| 2     | `astral-sh/ruff-pre-commit`          | `ruff-format`             |                                                                                                |
| 3     | `RobertCraigie/pyright-python`       | `pyright`                 | uses project `.venv`                                                                           |
| 4     | `pre-commit/mirrors-prettier`        | `prettier`                | `types_or: [markdown, yaml, json]`; `rev` pinned per spike S13                                 |
| 5     | local                                | `uv-lock-check`           | `entry: uv lock --check`, `language: system`, `pass_filenames: false`, `files: pyproject.toml` |
| 6     | `pre-commit/pre-commit-hooks`        | `end-of-file-fixer`       |                                                                                                |
| 7     | `pre-commit/pre-commit-hooks`        | `trailing-whitespace`     | `args: [--markdown-linebreak-ext=md]`                                                          |
| 8     | `compilerla/conventional-pre-commit` | `conventional-pre-commit` | `stages: [commit-msg]`                                                                         |

No repo-level `package.json`; prettier is bootstrapped by pre-commit's Node environment. If spike S13 finds the mirror unusable on Windows, hook 4 is replaced by `uv run --with mdformat mdformat` on Markdown only, and YAML/JSON formatting is dropped.

### `zensical.toml`

```toml
[project]
site_name = "Thumbforge"
site_url = "https://<owner>.github.io/thumbforge/"   # D5
docs_dir = "docs"
site_dir = "site"

nav = [
  { "Home" = "index.md" },
  { "Architecture" = "ARCHITECTURE.md" },
  { "Roadmap" = "ROADMAP.md" },
  { "Conventions" = "CONVENTIONS.md" },
  { "Testing" = "TESTING.md" },
  { "Glossary" = "GLOSSARY.md" },
  { "Branching & releases" = "BRANCHING.md" },
  { "ADRs" = "adr/" },
  { "Specs" = "specs/" },
]
```

Mermaid rendering of ADR/spec diagrams is spike S14; if a `pymdownx.superfences` custom fence is required it is added under `[project.markdown_extensions]` in the same PR that closes S14.

### `.github/workflows/ci.yml` outline

```yaml
name: ci
on:
    pull_request:
    push:
        branches: [main]
concurrency:
    group: ci-${{ github.ref }}
    cancel-in-progress: true
jobs:
    test:
        strategy:
            fail-fast: false
            matrix:
                os: [ubuntu-latest, windows-latest]
                python: ["3.14"]
        runs-on: ${{ matrix.os }}
        steps:
            - uses: actions/checkout@v4
            - uses: astral-sh/setup-uv@v5
              with: { python-version: "${{ matrix.python }}", enable-cache: true }
            - run: uv sync --locked
            - run: uv run ruff check .
            - run: uv run ruff format --check .
            - run: uv run pyright
            - run: uv run pytest --cov --cov-fail-under=80
            - run: uv run zensical build
    graph-drift:
        runs-on: ubuntu-latest
        continue-on-error: true # warning-only until spike S9 decides
        steps:
            - uses: actions/checkout@v4
            - uses: astral-sh/setup-uv@v5
            - run: uv tool install graphifyy
            - run: graphify update . && git diff --exit-code graphify-out/graph.json
```

`pytest` runs with `addopts = "-m 'not integration'"`, so no network or provider tests run in CI by default. Python 3.15 is added to `matrix.python` when spike S12 closes.

### `.github/workflows/docs.yml` outline

```yaml
name: docs
on:
    push:
        branches: [main]
permissions: { contents: read, pages: write, id-token: write }
jobs:
    build:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4
            - uses: astral-sh/setup-uv@v5
            - run: uv sync --locked --only-group dev
            - run: uv run zensical build
            - uses: actions/upload-pages-artifact@v3
              with: { path: site }
    deploy:
        needs: build
        runs-on: ubuntu-latest
        environment: github-pages
        steps:
            - id: deployment
              uses: actions/deploy-pages@v4
```

### `.github/workflows/release.yml` proposal

```yaml
name: release
on:
    push:
        tags: ["v*.*.*"]
permissions: { contents: write, id-token: write }
jobs:
    build:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4
              with: { fetch-depth: 0 }
            - uses: astral-sh/setup-uv@v5
            - run: uv build
            - uses: orhun/git-cliff-action@v4
              with: { args: --latest --strip header }
              id: cliff
            - uses: softprops/action-gh-release@v2
              with: { body: "${{ steps.cliff.outputs.content }}", files: dist/* }
            - uses: actions/upload-artifact@v4
              with: { name: dist, path: dist }
    publish:
        needs: build
        runs-on: ubuntu-latest
        environment: pypi
        steps:
            - uses: actions/download-artifact@v4
              with: { name: dist, path: dist }
            - uses: pypa/gh-action-pypi-publish@release/v1 # trusted publishing; no token
```

Version source is `[project] version` in `pyproject.toml`; the tag must equal `v${version}` (checked by a step before `uv build`). `git-cliff` reads Conventional Commits (enforced by the `conventional-pre-commit` hook) to generate `CHANGELOG.md`; `CHANGELOG.md` is prettier-ignored because git-cliff owns its formatting.

### `.github/labels.yml`

| Label                  | Colour    | Use                                                    |
| ---------------------- | --------- | ------------------------------------------------------ |
| `type:feature`         | `#0e8a16` | New behaviour                                          |
| `type:bug`             | `#d73a4a` | Defect                                                 |
| `type:spike`           | `#fbca04` | Time-boxed investigation (`OPEN_QUESTIONS.md` S-items) |
| `type:docs`            | `#0075ca` | Docs / ADR / spec only                                 |
| `type:infra`           | `#5319e7` | CI, tooling, repo config                               |
| `phase:0` … `phase:8`  | `#c5def5` | ROADMAP phase                                          |
| `provider:antigravity` | `#bfd4f2` | Antigravity adapter                                    |
| `provider:fake`        | `#bfd4f2` | FakeProvider                                           |
| `needs:decision`       | `#e99695` | Blocked on a D-item in `OPEN_QUESTIONS.md`             |

### `.github/CODEOWNERS`

```
* @<owner>
```

`<owner>` is resolved by decision D5.

### Issue templates

- `feature.yml`: fields _ROADMAP task id_, _Spec link_, _Acceptance criteria_, _ADRs affected_; label `type:feature`.
- `bug.yml`: fields _Command run_, _Expected_, _Actual_, _`thumbforge --version`_, _OS_, _log excerpt from `<state_dir>/logs/thumbforge.log`_; label `type:bug`.
- `spike.yml`: fields _Spike id (S1–S14)_, _Question_, _Verification command_, _What the answer changes_, _Time box_; label `type:spike`.

### `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
## What

<one paragraph>

## Links

- ROADMAP task: P?.?
- Spec: docs/specs/…#…
- Issue: #…

## Checklist

- [ ] One concern only
- [ ] Spec updated if behaviour differs from it
- [ ] Tests at the right layer (unit / contract / integration / golden)
- [ ] `pre-commit run --all-files` green locally
- [ ] Docs and AGENTS.md updated if structure changed
- [ ] `graphify update .` run and graphify-out/ committed (minus cost.json)
```

### Branch protection (`main`)

- Pull request required; direct pushes disabled.
- 1 approving review (CODEOWNERS satisfy this when D5 sets a real owner).
- Required status checks: `ci / test (ubuntu-latest, 3.14)`, `ci / test (windows-latest, 3.14)`. `graph-drift` is not required.
- Linear history required (squash or rebase merges only).
- Force-push and deletion of `main` disabled.
- Conversation resolution required before merge.

### PR discipline

- One concern per PR; a PR that touches two ROADMAP tasks is split.
- Every PR links its spec and issue in the template; a PR with no spec link is returned without review.
- CI must be green on both OS legs before review starts.
- Docs, ADRs and `AGENTS.md` are updated in the same PR as the change they describe.
- Commit messages follow Conventional Commits (`feat(providers): …`, `fix(cli): …`, `docs: …`, `chore(infra): …`), enforced by the commit-msg hook.

### graphify integration (P0.6)

Steps, executed in this order and recorded in `docs/BRANCHING.md`:

1. `uv tool install graphifyy` (pin exact version once spike S9 records it).
2. `graphify install --project --platform agents` → writes `.agents/skills/` and appends a section to `AGENTS.md`.
3. `graphify .` → `graphify-out/{graph.html,GRAPH_REPORT.md,graph.json,cost.json}` (PowerShell: `graphify .`, not `/graphify .`).
4. Commit `graphify-out/` except `cost.json` (already in `.gitignore`).
5. Ongoing: `graphify update .` before each PR; CI `graph-drift` job runs `graphify update . && git diff --exit-code graphify-out/graph.json` as warning-only.
6. Spike S9 decides whether `graphify hook install` (post-commit + post-checkout background rebuild) is enabled, whether the drift check moves to pre-commit, or whether it stays manual. Until S9 closes, step 5 is the rule.

## Behaviour

1. `uv sync --locked` installs the runtime (empty) and dev groups from `uv.lock`; a stale lock fails.
2. `uv run thumbforge --version` prints `thumbforge 0.0.0` and exits `0`; `uv run thumbforge` with no arguments prints Typer help and exits `0`; `uv run thumbforge nope` exits `2`.
3. `pre-commit run --all-files` runs the eight hooks above and is green on the empty package.
4. `uv run zensical build` renders every page in the `nav` list plus the ADR and spec directories into `site/` with zero warnings.
5. On push to `main`, `docs.yml` deploys `site/` to GitHub Pages.
6. On PR, `ci.yml` runs the `test` matrix (2 jobs) and `graph-drift` (advisory).

## Acceptance criteria

Per file/task:

- **P0.1** — `uv sync --locked` exits `0`; `uv run thumbforge --version` prints `thumbforge 0.0.0`; `git ls-files` shows `LICENSE`, `.editorconfig`, `.gitignore`, `README.md`, `uv.lock`, `pyproject.toml`; `python -c "import thumbforge; print(thumbforge.__version__)"` prints `0.0.0`.
- **P0.2** — `pre-commit run --all-files` exits `0`; `uv run ruff check .`, `uv run ruff format --check .`, `uv run pyright` each exit `0`; `uv run pytest --cov --cov-fail-under=80` exits `0` with `tests/test_version.py` passing; `.prettierrc` contains exactly the JSON above; `.prettierignore` contains exactly the four entries above.
- **P0.3** — `AGENTS.md` exists with the sections listed in `PLAN.md`'s plan (Project map, Commands, Before you start, Conventions, Definition of done, How to pick up a task, Never do); `CLAUDE.md` and `GEMINI.md` are the single pointer line.
- **P0.4** — `uv run zensical build` exits `0` with no `WARNING` lines; `site/adr/0016-zensical-docs-site/index.html` and `site/specs/phase-0-infra/index.html` exist; every ADR 0001–0016 is present with `Status:` set.
- **P0.5** — `ci.yml` runs green on both matrix legs on the bootstrap PR; `docs.yml` deploys on the first merge to `main` and the Pages URL serves `index.html`; `release.yml` passes `actionlint` but is not exercised; `gh label list` shows every label from `labels.yml` after running the script in `docs/BRANCHING.md`; branch protection matches the list above (verified via `gh api repos/<owner>/thumbforge/branches/main/protection`).
- **P0.6** — `graphify-out/graph.json` and `GRAPH_REPORT.md` are committed; `graphify query "where is the provider registry"` returns an answer referencing `docs/ARCHITECTURE.md`; `git check-ignore graphify-out/cost.json` exits `0`.
- **P0.7** — `docs/specs/README.md`, `phase-0-infra.md`, `phase-1-skeleton.md` exist and are in the docs nav.

## Test plan

- Unit: `tests/test_version.py` only (CliRunner, no network).
- Contract / integration / golden: none in Phase 0; markers are registered so later phases do not change `pyproject.toml`.
- Tooling: `pre-commit run --all-files`, `actionlint .github/workflows/*.yml` run once locally on the bootstrap PR.

## Open spikes

- **S9** graphify on Windows/uv — decides hooks vs CI vs manual for P0.6; if graphify fails on Windows, P0.6 becomes a documented manual `uv tool run --from graphifyy graphify update .` step and the `graph-drift` CI job is removed.
- **S12** Python 3.15 GA — adds `"3.15"` to the CI matrix.
- **S13** prettier via pre-commit on Windows — pins the `mirrors-prettier` `rev`, or swaps hook 4 for `mdformat`.
- **S14** zensical build of the ADR/spec tree with mermaid — may add a superfence config to `zensical.toml`; records the exact zensical version to pin.
