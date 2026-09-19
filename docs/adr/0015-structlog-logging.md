# ADR 0015: structlog for logging

## Status

`Superseded by [ADR 0017](0017-logging-verbosity-and-redaction.md)` — 2026-09-19

The structlog decision itself stands; only the verbosity mapping and the redaction mechanism below were revised. See ADR 0017.

## Context

Batch runs execute many iterations concurrently across a subprocess-driven provider, `yt-dlp`, SQLAlchemy and Alembic. Diagnosing a failed iteration requires every log line to carry `run_id`, `iteration_id` and `provider` without threading those through every function. Humans want coloured, readable stderr; `--json` mode and the log file need machine-parseable lines; Rich output on stdout must never be polluted.

## Decision

Use **structlog** (`uv add structlog`), configured once in `src/thumbforge/logging.py`:

- `logging.py` exposes `configure_logging(level: str, fmt: Literal["console", "json"], log_file: Path) -> None` and `get_logger(name: str) -> structlog.stdlib.BoundLogger`.
- Processor chain: `structlog.contextvars.merge_contextvars`, `add_log_level`, `TimeStamper(fmt="iso", utc=True)`, `StackInfoRenderer`, `format_exc_info`, then the renderer: `structlog.dev.ConsoleRenderer(colors=True)` on stderr for `console` (default); `structlog.processors.JSONRenderer()` when `--json` or `THUMBFORGE_LOG_FORMAT=json`.
- Stdlib bridge: `structlog.stdlib.ProcessorFormatter` on the root `logging` handler so `yt_dlp`, `sqlalchemy` and `alembic` records render through the same pipeline. `logger_factory=structlog.stdlib.LoggerFactory()`, `wrapper_class=structlog.stdlib.BoundLogger`, `cache_logger_on_first_use=True`.
- Log file: always JSON lines at `<state_dir>/logs/thumbforge.log` via `RotatingFileHandler` (5 files × 5 MB).
- Context: `structlog.contextvars.bind_contextvars(run_id=…, iteration_id=…, provider=…)` at run/iteration entry, `clear_contextvars()` on exit.
- Rich progress bars and tables go to **stdout**; logs go to **stderr**. They never interleave.
- Provider subprocess stdout/stderr are captured per iteration to `<state_dir>/logs/runs/<run_id>/<iteration_id>.{out,err}`.
- Verbosity: default `INFO` (`[logging] level`), `-v` → `DEBUG` for `thumbforge.*`, `-vv` → `DEBUG` for everything including third-party loggers; `--quiet` → `WARNING`.
- A final processor drops event-dict keys matching the secret deny-list from ADR 0014.
- Modules obtain a logger with `get_logger(__name__)`; `print()` is banned outside `cli/_render.py`.

## Consequences

- One `jq`-able log file per machine records every run; `runs show` can point at the exact lines by `run_id`.
- Third-party noise is uniformly formatted and filterable, rather than escaping through stdlib's default handler.
- Async tasks inherit context automatically via `contextvars`, so concurrent iterations are distinguishable without explicit parameters.
- Acceptance in `docs/specs/phase-1-skeleton.md`: `thumbforge -vv db status` emits console lines with `level`, `timestamp`, `event`; `thumbforge --json db status 2>err.jsonl` yields one JSON object per line.

## Alternatives considered

- **Bare stdlib `logging`** — rejected: no structured context; `run_id` would have to be interpolated into every message string.
- **loguru** — rejected: no processor pipeline for adding/dropping keys, and poor interoperability with stdlib loggers used by `yt-dlp`, SQLAlchemy and Alembic.
- **Logging to stdout** — rejected: would corrupt `--json` output and Rich progress rendering.
