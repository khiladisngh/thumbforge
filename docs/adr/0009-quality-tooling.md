# ADR 0009: Quality tooling — ruff, pyright, pytest, pre-commit, prettier

## Status

`Accepted` — 2026-09-19

## Context

The repository is built mostly by coding agents, so automated checks must be strict, fast and identical locally and in CI. Python needs linting, formatting and type checking; the planning-heavy docs tree (Markdown, YAML workflows, JSON fixtures) needs consistent formatting too, but ruff does not format those file types.

## Decision

- **ruff** for Python lint **and** format. `[tool.ruff] line-length = 100`, `target-version = "py314"`, `select = ["E", "F", "I", "UP", "B", "SIM", "TCH", "RUF"]` plus `T201` (no `print`) outside `cli/_render.py`. CI runs `ruff check` and `ruff format --check`.
- **pyright** as the type checker, strict on the package: `[tool.pyright] strict = ["src"]`, `pythonVersion = "3.14"`. Tests are checked in basic mode.
- **pytest** with `asyncio_mode = "auto"` (pytest-asyncio), markers `integration` (network / real `agy`), `golden` (image comparison), `record` (fixture recorder); `pytest-cov` with `--cov-fail-under=80`.
- **pre-commit** hooks, in order: `ruff` (fix), `ruff-format`, `pyright`, `mirrors-prettier`, `uv lock --check`, `end-of-file-fixer`, `conventional-pre-commit` (commit-msg stage).
- **prettier ONLY for Markdown, YAML and JSON**, never Python. It runs through the `mirrors-prettier` pre-commit hook with `types_or: [markdown, yaml, json]`; there is **no Node project in the repo** (no `package.json`), the hook bootstraps its own Node. `.prettierrc` is `{"proseWrap": "preserve", "printWidth": 100}`; `.prettierignore` lists `graphify-out/`, `site/`, `uv.lock`, `CHANGELOG.md`. The exact pinned `rev` and Windows behaviour are settled by spike S13.
- **import-linter** enforces the layering rule from `PLAN.md` §2.2 (Phase 1).
- **Conventional Commits** are enforced on commit messages; `git-cliff` generates the changelog from them.

## Consequences

- One command set for humans and agents: `uv run ruff check . && uv run ruff format .`, `uv run pyright`, `uv run pytest -q`, `pre-commit run --all-files`.
- Strict pyright on `src` forces typed boundaries (Pydantic models, Protocols) from Phase 1; untyped third-party libraries (`yt_dlp`) get local stubs or `# pyright: ignore` with a reason.
- No Node toolchain to maintain; Markdown formatting cost is one hook bootstrap per machine.
- If S13 shows the prettier mirror is broken on Windows, the fallback is `mdformat` via `uv run --with mdformat` for Markdown only, and YAML/JSON formatting is dropped.

## Alternatives considered

- **ty** (astral-sh) — rejected for now: not yet at its stable milestone; revisit once it ships stable.
- **mypy** — rejected: slower on incremental runs and weaker inference for Protocol/`ClassVar` patterns used by the provider registry.
- **black + isort + flake8** — rejected: three tools where ruff is one, with the same rule coverage.
- **A repo-level `package.json` running prettier via npm** — rejected: introduces a second package manager into a uv-only repo.
- **markdownlint** — rejected: lints but does not format; prettier does both.
