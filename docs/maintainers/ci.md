# CI and local checks

Three GitHub Actions workflows live in `.github/workflows/`. Every job installs uv with `astral-sh/setup-uv` and runs tools through `uv run`.

## `ci.yml` — checks on every push

Runs on every push to `main` and on pull requests. With the direct-to-main workflow, the push to `main` is the run that matters. A newer run for the same ref cancels the one in progress. It has two jobs.

**`test (<os>, 3.14)`** runs on `ubuntu-latest` and `windows-latest` with Python 3.14 (`fail-fast: false`, so one leg failing does not cancel the other). Steps, in order:

1. `uv sync --locked`
2. `uv run ruff check .`
3. `uv run ruff format --check .`
4. `uv run pyright`
5. `uv run lint-imports`
6. `uv run pytest --cov --cov-fail-under=80`
7. `uv run zensical build`

Both legs are required status checks on `main` (see [Release process](branching-and-releases.md#branch-protection-main)). Because `zensical.toml` sets `strict = true`, the docs build fails on any warning, including a broken link or anchor.

**`graphify drift (advisory)`** runs on `ubuntu-latest` with `continue-on-error: true` and is not a required check. It installs graphify with `uv tool install graphifyy`, exits early if `graphify-out/graph.json` is not committed, copies the committed graph aside, re-extracts with `graphify extract . --code-only`, and runs `scripts/check_graph_drift.py` on the two graphs. The script compares the set of declaration nodes, not the files byte for byte, and names any symbol added, removed or renamed without regenerating the graph. [Conventions → Knowledge graph](../developers/conventions.md#knowledge-graph) explains what it deliberately ignores and how to rebuild the graph.

## `docs.yml` — publish the site

Runs on **every push to `main`** (there is no path filter, so a code-only merge also redeploys) and on manual dispatch. Deployments are serialised in the `pages` concurrency group and never cancelled.

- `build` (`ubuntu-latest`): `uv sync --locked --only-group dev`, `uv run zensical build`, then `actions/configure-pages` and `actions/upload-pages-artifact` with the `site/` directory.
- `deploy`: `actions/deploy-pages` into the `github-pages` environment, which publishes to <https://khiladisngh.github.io/thumbforge/>.

## `release.yml` — publish a release

Runs when a tag matching `v*.*.*` is pushed.

- `build` (`ubuntu-latest`, full history): fails unless the tag equals `v` plus the version reported by `uv version --short`; runs `uv build`; generates release notes with `git-cliff` (`cliff.toml`, `--latest --strip header`); creates the GitHub release with those notes and the files in `dist/` attached; uploads `dist/` as a workflow artifact.
- `publish`: downloads the artifact and publishes it to PyPI with `pypa/gh-action-pypi-publish` from the `pypi` environment (trusted publishing; the publisher must be configured on PyPI before the first tag).

The steps around it — version bump commit, tagging — are in [Release process](branching-and-releases.md#releases).

## Running the same checks locally

| Check                    | Command                                   | In CI                   |
| ------------------------ | ----------------------------------------- | ----------------------- |
| Install from the lock    | `uv sync --locked`                        | `ci.yml`                |
| Lint                     | `uv run ruff check .`                     | `ci.yml`                |
| Format                   | `uv run ruff format --check .`            | `ci.yml`                |
| Types                    | `uv run pyright`                          | `ci.yml`                |
| Tests with coverage gate | `uv run pytest --cov --cov-fail-under=80` | `ci.yml`                |
| Import contracts         | `uv run lint-imports`                     | `ci.yml`                |
| Docs build               | `uv run zensical build`                   | `ci.yml`, `docs.yml`    |
| Pre-commit hooks         | `pre-commit run --all-files`              | not run by any workflow |

`uv run pytest -q` (unit and contract tests, without the coverage gate) is the quick loop; [Testing](../developers/testing.md) covers the opt-in `integration` and `golden` markers. The pre-commit hooks (ruff, pyright, prettier for Markdown/YAML/JSON, `uv lock --check`, whitespace and Conventional Commit checks) are part of the definition of done in `AGENTS.md` but run only locally.

`scripts/ci-local.sh` (Linux) and `scripts/ci-local.cmd` (Windows) run the `test` job's steps in order on each OS, so run both before pushing to `main`. When the `test` job changes, change both scripts in the same commit.

To reproduce the graphify drift check:

```
mkdir -p .pytest_tmp
cp graphify-out/graph.json .pytest_tmp/committed-graph.json
graphify extract . --code-only
uv run python scripts/check_graph_drift.py .pytest_tmp/committed-graph.json graphify-out/graph.json
```
