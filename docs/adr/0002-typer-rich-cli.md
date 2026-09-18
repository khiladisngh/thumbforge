# ADR 0002: Typer and Rich for the CLI

## Status

`Accepted` — 2026-09-19

## Context

The product surface is a command tree (`fetch`, `video`, `playlist`, `thumb`, `batch`, `runs`, `template`, `provider`, `config`, `db`) with global options (`--config PATH`, `--data-dir PATH`, `--json`, `-v/-vv`, `--quiet`, `--no-color`, `--version`). Humans need tables, panels, progress bars and an image preview grid; scripts need stable JSON on stdout. Business logic must not live in the CLI layer (ADR dependency rule in `PLAN.md` §2.2).

## Decision

- **Typer** builds the command tree. `cli/app.py` is the root app; each sub-command group is its own module (`cli/fetch.py`, `cli/thumb.py`, …) registered via `app.add_typer`. Typer's default exit code `2` for usage errors is adopted as the project's "usage / validation" code.
- **Rich** renders all human output through `cli/_render.py` only: tables, panels, `Progress` bars, and the preview grid. `--json` disables Rich and prints one JSON document to stdout; `--no-color` and `NO_COLOR` disable ANSI.
- Rich output goes to **stdout**; logs go to **stderr** (ADR 0015). They never interleave.
- Image preview in the terminal uses `rich-pixels` (block characters). Native inline-image protocols (kitty, iTerm2) are deferred; spike S10 tests `rich-pixels` in Windows Terminal before Phase 5 commits to it.
- `cli/_errors.py` is the single `ThumbforgeError → exit code` handler wrapping every command (`PLAN.md` §7.1).
- `cli/` modules contain no business logic; they parse arguments, call a service, and render.

## Consequences

- Every command's `--json` shape becomes part of the public contract and is tested in Phase 1+.
- `print()` is banned outside `cli/_render.py`; enforced by review and a ruff rule (`T201`) in Phase 0.
- Shell completion comes for free from Typer (Phase 8 task).
- The preview grid quality depends on S10; if `rich-pixels` is unusable on Windows Terminal, `thumb show` falls back to a table plus `thumb export`.

## Alternatives considered

- **argparse** — rejected: no automatic help formatting for nested sub-apps, manual type coercion.
- **Click directly** — rejected: Typer is Click underneath and removes decorator boilerplate while keeping Click's testing utilities.
- **textual TUI** — rejected: the tool is batch-oriented and scriptable; a full-screen UI would fight `--json`.
- **kitty/iTerm inline images as default preview** — deferred (S10): not supported by Windows Terminal, the primary development terminal.
