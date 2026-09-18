# ADR 0001: Python 3.14 and uv

## Status

`Accepted` — 2026-09-19

## Context

`thumbforge` is a single-user local CLI that shells out to `agy`, runs `yt-dlp`, drives Pillow and SQLite, and is built primarily by coding agents. The toolchain must be reproducible on Windows and Linux, fast to bootstrap in CI, and unambiguous for agents that read `AGENTS.md`.

Verified on the development machine: `uv 0.12.16` and `python 3.14.7` are installed (`uv python list --only-installed`). Python 3.15.0 is at rc2 with release scheduled for October 2026; the latest stable interpreter is 3.14.7.

## Decision

- Language: Python, `requires-python = ">=3.14"`. CI matrix `["3.14"]` on `ubuntu-latest` and `windows-latest`; 3.15 is added once GA (spike S12).
- Package and environment manager: **uv**. Bootstrap with `uv init --package --python 3.14`; `uv.lock` is committed; CI and developers use `uv sync --locked`. Every command in docs is written as `uv run …`.
- src layout: `src/thumbforge/`, console script `thumbforge = "thumbforge.cli.app:main"`, `__version__` resolved via `importlib.metadata`.
- Third-party CLIs that are not project dependencies (graphify, zensical when used as a tool) are installed with `uv tool install`.
- Language features assumed throughout: `match`, `StrEnum`, PEP 695 generics, `pathlib`, `asyncio` task groups.

## Consequences

- One lockfile, one command set; `uv sync --locked` failing is a CI error, which catches unlocked dependency drift.
- `pip`, `poetry`, `pipx` and `requirements.txt` are not used anywhere in the repo (`AGENTS.md` "Never do").
- Libraries that lag 3.14 support block adoption; ADR 0004 and ADR 0009 pick libraries with current 3.14 wheels.
- Release automation (`uv build` + trusted publishing) follows naturally; see `docs/specs/phase-0-infra.md`.

## Alternatives considered

- **Python 3.12/3.13 floor** — rejected: no dependency needs it, and starting on the current stable interpreter avoids a floor bump within months.
- **Python 3.15 rc** — rejected: pre-release interpreters have no guaranteed wheels for Pillow/SQLAlchemy; tracked by spike S12.
- **poetry** — rejected: slower resolver, separate Python installation story, no `uv tool` equivalent for graphify/zensical.
- **pip + venv + pip-tools** — rejected: three tools where uv is one, and no lockfile check in a single command.
