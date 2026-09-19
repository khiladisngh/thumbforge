# Phase 1 — Skeleton

Status: Implemented (P1.1–P1.6)
ROADMAP tasks: P1.1, P1.2, P1.3, P1.4, P1.5, P1.6
ADRs: `docs/adr/0002-typer-rich-cli.md`, `docs/adr/0003-settings-toml-platformdirs.md`, `docs/adr/0004-sqlite-sqlalchemy-alembic.md`, `docs/adr/0011-content-addressed-assets.md`, `docs/adr/0014-secrets-env-keyring.md`, `docs/adr/0015-structlog-logging.md`

## Scope

Phase 1 turns the empty package into a runnable CLI with every cross-cutting service the later phases depend on, but no domain behaviour: settings, logging, database + migrations, asset store, error hierarchy with exit codes, the root Typer app with global flags, and the import-linter contracts that enforce `PLAN.md` §2.2.

- **P1.1 settings** — `src/thumbforge/settings.py`, `cli/config.py` (`config show|path|set|init`).
- **P1.2 logging** — `src/thumbforge/logging.py`.
- **P1.3 database** — `src/thumbforge/core/enums.py` (domain enums), `storage/db.py` (engine, sessions, WAL, migrations), `storage/models.py` (all tables from `PLAN.md` §3), `storage/migrations/`, `cli/db.py` (`db init|upgrade|status|path|vacuum`).
- **P1.4 asset store** — `storage/assets.py` (content-addressed `AssetStore`, Pillow MIME sniffing, verify drift check).
- **P1.5 errors + root app** — `core/errors.py`, `cli/_errors.py`, `cli/app.py`, `cli/_render.py`.
- **P1.6 import-linter** — `[tool.importlinter]` contracts in `pyproject.toml`; CI step `uv run lint-imports`.

Runtime dependencies added: `typer`, `rich`, `pydantic`, `pydantic-settings`, `platformdirs`, `sqlalchemy`, `alembic`, `structlog`, `tenacity`, `keyring`, `python-ulid`, `pillow`.

## Non-goals

- No `fetch`, `thumb`, `batch`, `template`, `provider` commands — they are registered as sub-apps in later phases; in Phase 1 `cli/app.py` registers only `config` and `db`.
- No repositories beyond what `db status` needs (`storage/repositories.py` is created empty with the module docstring; per-aggregate repositories arrive with their phases).
- No secrets are read in Phase 1; the settings validator only _rejects_ secret-looking TOML keys. `provider set-key` is Phase 3.
- Terminal image preview (`_render.py` preview helper) is Phase 5 / spike S10.

## Interfaces

### Settings (`settings.py`)

`Settings(BaseSettings)` with `model_config = SettingsConfigDict(env_prefix="THUMBFORGE_", env_nested_delimiter="__", toml_file=<config path>, extra="forbid")`. Source precedence, highest first: CLI flags (`--config`, `--data-dir`, `--json`, `-v`), environment variables, TOML file, defaults.

TOML schema and defaults:

```toml
[general]
data_dir = "<platformdirs user_data_dir('thumbforge')>"
default_provider = "fake"
default_template = "bold-title"

[output]
width = 1920
height = 1080
format = "jpeg"          # "jpeg" | "png"
quality = 90
max_bytes = 2097152      # 2 MiB; overridable per command with --max-bytes up to 52428800

[batch]
concurrency = 1
max_retries = 2
stale_after_s = 900

[providers.antigravity]
binary = "agy"
model = null             # slug from `agy models`; null = provider default
effort = "low"           # low | medium | high
timeout_s = 600
skip_permissions = true  # decision D4

[logging]
level = "INFO"           # DEBUG | INFO | WARNING | ERROR
format = "console"       # console | json
```

Locations (ADR 0003):

| Purpose                      | Path                                                     | Override                                                                |
| ---------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------- |
| Config file                  | `platformdirs.user_config_dir("thumbforge")/config.toml` | `--config PATH` or `THUMBFORGE_CONFIG`                                  |
| Data (DB, assets, templates) | `platformdirs.user_data_dir("thumbforge")`               | `--data-dir PATH`, `THUMBFORGE_GENERAL__DATA_DIR`, `[general] data_dir` |
| State (logs)                 | `platformdirs.user_state_dir("thumbforge")`              | `THUMBFORGE_STATE_DIR`                                                  |
| DB file                      | `<data_dir>/thumbforge.sqlite3`                          | derived                                                                 |
| Assets                       | `<data_dir>/assets/`                                     | derived                                                                 |
| User templates               | `<config_dir>/templates/`                                | derived                                                                 |

Environment mapping examples: `THUMBFORGE_OUTPUT__WIDTH=1280`, `THUMBFORGE_PROVIDERS__ANTIGRAVITY__MODEL=…`, `THUMBFORGE_LOG_FORMAT=json` (alias for `[logging] format`, kept because `PLAN.md` §7.3 names it).

Secret rejection (ADR 0014): after loading, a `model_validator(mode="after")` walks every TOML-sourced key; any key whose last segment matches `*_key`, `*_token`, `*_secret` raises `SettingsError("secrets are not allowed in config.toml", hint="use THUMBFORGE_PROVIDERS__<KEY>__API_KEY or `thumbforge provider set-key`")`. `SettingsError` is a `ThumbforgeError` subclass with exit code `2`.

Public API:

```python
def load_settings(*, config_path: Path | None, data_dir: Path | None) -> Settings
def default_config_toml() -> str            # rendered defaults with comments; used by `config init`
def set_value(settings_path: Path, dotted_key: str, raw: str) -> None   # `config set`; validates against the schema before writing
```

### `config` commands

| Command                              | Behaviour                                                                                                                                                                                                                   | Exit |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| `thumbforge config init`             | Writes `default_config_toml()` to the config path; refuses to overwrite unless `--force`                                                                                                                                    | 0, 2 |
| `thumbforge config show`             | Prints effective settings as TOML (Rich syntax panel) or JSON with `--json`                                                                                                                                                 | 0    |
| `thumbforge config path`             | Prints config path, data dir, state dir, DB path (one per line; JSON object with `--json`)                                                                                                                                  | 0    |
| `thumbforge config set KEY=VALUE...` | One or more assignments (`output.width=1280 output.height=720`); values parsed as TOML scalars; the whole result is validated through `Settings` before the file is rewritten, so a rejected edit leaves the file untouched | 0, 2 |

`config set` takes assignments rather than a `KEY VALUE` pair because linked keys must change together: `output.width` and `output.height` are bound by the 16:9 invariant, and setting either alone leaves a configuration that cannot validate, making the value unreachable.

Precedence note: file values are merged _underneath_ environment values rather than passed to `Settings(**file_values)`. Constructor arguments are the highest-priority source in pydantic-settings, so the naive form would let `config.toml` silently beat `THUMBFORGE_*`.

### Logging (`logging.py`)

Copied from `PLAN.md` §7.3:

- `logging.py` exposes `configure_logging(level: str, fmt: Literal["console", "json"], log_file: Path) -> None` and `get_logger(name: str) -> structlog.stdlib.BoundLogger`.
- Processor chain: `structlog.contextvars.merge_contextvars`, `add_log_level`, `TimeStamper(fmt="iso", utc=True)`, `StackInfoRenderer`, `format_exc_info`, then the renderer: `structlog.dev.ConsoleRenderer(colors=True)` on stderr for `console` (default); `structlog.processors.JSONRenderer()` when `--json` or `THUMBFORGE_LOG_FORMAT=json`.
- Stdlib bridge: `structlog.stdlib.ProcessorFormatter` on the root `logging` handler so `yt_dlp`, `sqlalchemy` and `alembic` records render through the same pipeline. `logger_factory=structlog.stdlib.LoggerFactory()`, `wrapper_class=structlog.stdlib.BoundLogger`, `cache_logger_on_first_use=True`.
- Log file: always JSON lines at `<state_dir>/logs/thumbforge.log` via `RotatingFileHandler` (5 files × 5 MB).
- Context: `structlog.contextvars.bind_contextvars(run_id=…, iteration_id=…, provider=…)` at run/iteration entry, `clear_contextvars()` on exit.
- Rich progress bars and tables go to **stdout**; logs go to **stderr**. They never interleave.
- Provider subprocess stdout/stderr are captured per iteration to `<state_dir>/logs/runs/<run_id>/<iteration_id>.{out,err}`.

Stream contract in `--json` mode, enforced by `cli/_errors.py`. Verify with a command that
fails, for example a missing config path:

```
$ thumbforge --json --config /nonexistent/config.toml config show > out.json 2> err.jsonl; echo $?
2
$ wc -l < out.json          # stdout carries command output only; nothing on failure
0
$ wc -l < err.jsonl         # exactly one physical line, however long the message
1
$ jq -c . < err.jsonl
{"error":"settings","message":"...","exit_code":2,"hint":"..."}
```

- **stdout** carries command output only: exactly one JSON document per successful invocation, nothing when the command fails.
- **stderr** carries the diagnostic: one line of JSON with `error`, `message`, `exit_code`, plus `hint` when present. `KeyboardInterrupt` yields `{"error": "interrupted", "exit_code": 130}` and exit `130`.

> Implementation note, not an acceptance criterion: diagnostics are written with
> `sys.stderr.write(json.dumps(...) + "\n")` rather than `Console.print_json`, because the
> latter pretty-prints and soft-wraps at terminal width, which would split a long message
> across lines and break the one-line guarantee above.

Level mapping from global flags: the console defaults to `[logging] level` (`INFO`), `-v` → `INFO`, `-vv` → `DEBUG`, `--quiet` → `ERROR` (it outranks `-v`). The file handler is always `DEBUG`, so a bug report carries detail without the user reproducing under `-vv`. `--no-color` sets `ConsoleRenderer(colors=False)`, and `--json` forces the JSON renderer. If the log file cannot be opened, logging degrades to console and emits one `file logging disabled` warning rather than failing the command.

A broken `config.toml` does not block the commands that repair it. The root callback captures a `SettingsError` instead of raising it; `config init` and `config set` rewrite the file without reading the parsed settings, while every other command calls `AppContext.require_settings()`, which re-raises. Otherwise the hint printed on a parse failure — `run thumbforge config init --force` — would name an unreachable command.

### Database (`storage/db.py`, `storage/migrations/`)

- Engine: `create_engine("sqlite+pysqlite:///<data_dir>/thumbforge.sqlite3", future=True)`; on every `connect` event execute `PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;`.
- `session_factory() -> sessionmaker[Session]`; `session_scope()` context manager commits on success, rolls back on exception.
- ORM (`storage/models.py`): SQLAlchemy 2.0 `DeclarativeBase` with `Mapped[...]` annotations; one class per table in `PLAN.md` §3 (`channel`, `playlist`, `video`, `playlist_item`, `template`, `provider_profile`, `run`, `iteration`, `asset`) including all `UNIQUE`, `CHECK` and `ON DELETE RESTRICT` constraints. PKs are `TEXT` ULIDs generated by `core/ids.py:new_id()`; `created_at`/`updated_at` are ISO-8601 UTC text set by ORM events.
- Alembic layout:

```
src/thumbforge/storage/migrations/
  env.py             # reads DB URL from Settings (never from alembic.ini); target_metadata = Base.metadata; render_as_batch=True (SQLite)
  script.py.mako
  versions/
    0001_initial.py  # full schema from PLAN.md §3
alembic.ini          # repo root; script_location = src/thumbforge/storage/migrations
```

- `uv run alembic revision --autogenerate -m "<msg>"` is the only way to create migrations; a CI test (`tests/storage/test_migrations.py`) asserts `alembic check` reports no drift between ORM and head.

### `db` commands

| Command                 | Behaviour                                                                                                | Exit |
| ----------------------- | -------------------------------------------------------------------------------------------------------- | ---- |
| `thumbforge db init`    | Creates parent dirs, runs `alembic upgrade head` on a fresh file; no-op with a notice if already at head | 0, 1 |
| `thumbforge db upgrade` | `alembic upgrade head`                                                                                   | 0, 1 |
| `thumbforge db status`  | Prints current revision, head revision, pending count, file size, `journal_mode`                         | 0, 1 |
| `thumbforge db path`    | Prints the DB file path                                                                                  | 0    |
| `thumbforge db vacuum`  | `VACUUM` + `PRAGMA wal_checkpoint(TRUNCATE)`, then deletes unreferenced `assets/` files and stale `tmp/` entries; reports the reclaimed count | 0, 1 |

Exit `1` here means `SourceError`-class unexpected failure (locked file, disk full) per `PLAN.md` §5.1.

### Asset store (`storage/assets.py`)

```python
class AssetStore:
    def __init__(self, data_dir: Path, session_factory: sessionmaker[Session]) -> None: ...
    def put(self, src: bytes | Path, kind: AssetKind) -> Asset: ...
    def path_for(self, asset: Asset) -> Path: ...
    def verify(self, asset: Asset) -> bool: ...
```

- Layout: `<data_dir>/assets/<sha256[:2]>/<sha256>.<ext>`; `asset.rel_path` is relative to `data_dir` so the data directory is relocatable.
- Write path: write to `<data_dir>/tmp/<ulid>`, `fsync`, compute sha256, then publish with `os.link` (create-only), falling back to an atomic rename where hard links are unsupported. Identical bytes dedupe to the same row.
- Publication is idempotent: the path is content-addressed, so an existing target already holds byte-identical content and a concurrent publication is never a conflict. A published file is never unlinked by `put` — another caller may already reference it — so an orphan left by a crash between publication and insert is reclaimed by `db vacuum` (ADR 0011).
- A concurrent caller that wins the `asset.sha256` unique constraint is adopted: `put` re-queries and returns that row instead of failing.
- `AssetStore.verify(asset)` re-hashes the file and reports drift.
- `put` sniffs `mime`, `width`, `height` with Pillow; `bytes` is the file size; `kind ∈ {raw, final, reference, preview}`; `compliant`/`compliance_report_json` stay `NULL` until Phase 5 fills them.
- `ext` is derived from the sniffed MIME (`jpg`, `png`, `webp`), never from the source filename; any other format raises `AssetError`.

### Errors (`core/errors.py`, `cli/_errors.py`)

Copied from `PLAN.md` §7.1:

```
ThumbforgeError(code: str, exit_code: int, hint: str | None)
├── NotFoundError            exit 3
├── ProviderError            exit 4
│   ├── ProviderAuthError
│   ├── ProviderPermanentError
│   ├── ProviderTransientError
│   ├── ProviderTimeoutError
│   └── ProviderOutputMissingError
├── ComplianceError          exit 5
├── PartialBatchError        exit 6
├── SourceError              exit 1
└── TemplateError            exit 2
```

Plus `SettingsError` (exit 2), `DatabaseError` (exit 1), `AssetError` (exit 1), and `ProviderRegistryError` (exit 1), all defined in Phase 1 so later phases only raise them.

Exit codes (`PLAN.md` §5.1):

| Code  | Meaning                                                         |
| ----- | --------------------------------------------------------------- |
| `0`   | success                                                         |
| `1`   | unexpected error (`SourceError`, uncaught)                      |
| `2`   | usage / validation error (Typer default; `TemplateError`)       |
| `3`   | not found (video, playlist, run, iteration, template, provider) |
| `4`   | provider error (auth, permanent, output missing)                |
| `5`   | compliance failure                                              |
| `6`   | partial batch — some items failed; run is resumable             |
| `130` | interrupted (SIGINT)                                            |

`cli/_errors.py` wraps every command: catches `ThumbforgeError`, prints `code: message` and `hint` to stderr (one line of JSON when `--json`), exits with `exit_code`. Anything else is logged with traceback and exits `1`. Implementation: a single decorator `@handle_errors` applied by `cli/app.py` to every registered command callback, plus a `KeyboardInterrupt` branch that exits `130`. The JSON error shape is flat, as specified in the stream contract above: `{"error": "<code>", "message": "...", "exit_code": N}` plus `"hint"` when the error carries one. It is deliberately not nested under an `error` object — one shape, defined in one place.

### Root app (`cli/app.py`)

- `app = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")`; `main()` is the console-script entry.
- Global options on the root callback: `--config PATH`, `--data-dir PATH`, `--json`, `-v/-vv` (count), `--quiet`, `--no-color`, `--version` (eager, prints `thumbforge <version>`).
- The callback builds `Settings`, calls `configure_logging`, and stores an `AppContext(settings, console, json_mode)` on `ctx.obj`; sub-commands receive it via `typer.Context`.
- `--json` sets `console = Console(file=sys.stdout, no_color=True, highlight=False)` and makes every command emit a single JSON document on stdout instead of Rich output; Rich tables are never printed in JSON mode.
- `cli/_render.py` provides `table(rows, columns)`, `panel(title, body)`, `kv(mapping)` and `emit(ctx, data, render=...)` which picks JSON or Rich according to `ctx.obj.json_mode`. It is the only module allowed to call `console.print`.

### Import-linter contracts (`pyproject.toml`)

Dependency rule (`PLAN.md` §2.2): `cli → core, storage, providers, sources, templates, imaging`; `core → nothing internal except errors/ids`; `providers/sources/storage/templates/imaging → core`; nothing imports `cli`.

```toml
[tool.importlinter]
root_package = "thumbforge"

[[tool.importlinter.contracts]]
name = "nothing imports cli"
type = "forbidden"
source_modules = ["thumbforge.core", "thumbforge.storage", "thumbforge.providers", "thumbforge.sources", "thumbforge.templates", "thumbforge.imaging", "thumbforge.settings", "thumbforge.logging"]
forbidden_modules = ["thumbforge.cli"]

[[tool.importlinter.contracts]]
name = "core is pure"
type = "forbidden"
source_modules = ["thumbforge.core"]
forbidden_modules = ["thumbforge.storage", "thumbforge.providers", "thumbforge.sources", "thumbforge.templates", "thumbforge.imaging", "thumbforge.cli", "thumbforge.settings"]

[[tool.importlinter.contracts]]
name = "adapters depend only on core"
type = "independence"
modules = ["thumbforge.providers", "thumbforge.sources", "thumbforge.storage", "thumbforge.templates", "thumbforge.imaging"]
```

Note: `core.services.*` orchestrate adapters through Protocols defined in `core`/`providers.base`/`sources.base`; the concrete instances are injected by `cli`. If `providers.base` must be importable from `core.services`, the Protocol moves to `core/models.py` — the contract is the rule, the file placement bends.

CI step added to `ci.yml` after `pyright`: `uv run lint-imports`. Pre-commit hook: local `lint-imports` (`language: system`, `pass_filenames: false`).

## Behaviour

1. First run with no config file: `Settings` uses defaults; `config init` writes the TOML above with comments; data/state directories are created lazily by the first command that needs them.
2. Precedence example: `[output] width = 1280` in TOML, `THUMBFORGE_OUTPUT__WIDTH=1600` in env → effective `1600`; `--data-dir` on the CLI beats both.
3. `config set output.width abc` → `SettingsError`, exit `2`, file untouched.
4. TOML containing `[providers.openai] api_key = "sk-…"` → any command exits `2` with the secrets hint before doing anything else.
5. `db init` on a fresh data dir creates `thumbforge.sqlite3` in WAL mode at Alembic head `0001_initial`; running it again prints `already at head` and exits `0`.
6. `db status` on a DB behind head reports `pending: N` and exits `0`; `db upgrade` applies them.
7. `AssetStore.put` with bytes already stored returns the existing row without writing; `put` with a `Path` never moves or deletes the source file.
8. Every command runs under `@handle_errors`; `KeyboardInterrupt` exits `130`; an unknown `ThumbforgeError` subclass still maps through `exit_code`.
9. Logging: with `-vv`, stderr shows console-rendered lines; with `--json`, stderr shows one JSON object per line; `<state_dir>/logs/thumbforge.log` receives JSON lines regardless.
10. `lint-imports` fails the build when any contract is broken.

## Acceptance criteria

- `thumbforge config init` writes `config.toml` at `platformdirs.user_config_dir("thumbforge")` (or `--config` path); `thumbforge config path` prints it; second `config init` without `--force` exits `2`.
- `thumbforge db init` creates the DB with `alembic current` = head; `thumbforge db status` prints `current == head`, `journal_mode = wal`.
- `thumbforge --json config show` prints a single JSON object parseable by `json.loads`, containing keys `general`, `output`, `batch`, `providers`, `logging` with the defaults above.
- `thumbforge nope` exits `2` with Typer's usage error.
- `thumbforge -vv db status` emits console-rendered lines on stderr containing the log event, ISO timestamp, and level.
- `thumbforge --json db status 2>err.jsonl` yields one parseable JSON object per line in `err.jsonl`, each with `run_id` absent and `event` present.
- A TOML with `api_key = "x"` under any table makes `thumbforge config show` exit `2` and print the keyring/env hint.
- `AssetStore.put(b"...", "raw")` twice returns the same `asset.id`; the file exists at `<data_dir>/assets/<sha256[:2]>/<sha256>.<ext>`; `<data_dir>/tmp/` is empty afterwards; `verify` returns `False` after the file is modified on disk.
- `uv run lint-imports` exits `0`; introducing `from thumbforge.cli import app` in `core/ids.py` makes it exit non-zero.
- `uv run alembic check` reports no drift.

## Test plan

- Unit (`tests/settings/`): precedence matrix (default < TOML < env < flag), secret rejection, `config set` validation, path resolution with `tmp_path` and monkeypatched `platformdirs`.
- Unit (`tests/logging/`): `configure_logging` with `fmt="json"` and a `tmp_path` log file; assert the JSON lines and that a stdlib `logging.getLogger("sqlalchemy").warning(...)` record appears through the bridge; assert `bind_contextvars(run_id=...)` shows in subsequent records and disappears after `clear_contextvars()`.
- Unit (`tests/storage/`): engine pragmas (`journal_mode`, `foreign_keys`), migration up/down on an in-memory and file DB, `alembic check`, `ON DELETE RESTRICT` on `run.parent_run_id`, `AssetStore` put/dedupe/verify/tmp-cleanup.
- Unit (`tests/cli/`): `CliRunner` for every `config`/`db` command in Rich and `--json` mode; exit-code mapping for each `ThumbforgeError` subclass via a hidden `_raise` test command registered only under `pytest`.
- Contract / integration / golden: opt-in testcontainers integration test (`tests/integration/test_db_container.py`); golden image overlay in Phase 5.
- No network in any Phase 1 test.

## Open spikes

- None block Phase 1. Spike S10 (terminal preview) touches `cli/_render.py` in Phase 5, not here.
