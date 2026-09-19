# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 612 nodes · 1179 edges · 62 communities (29 shown, 33 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 111 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `efe6f701`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Community 21
- Community 22
- Community 23
- Community 24
- Community 25
- Community 26
- Community 27
- Community 28
- Community 29
- Community 30
- Community 31
- Community 32
- Community 33
- Community 34
- Community 35
- Community 36
- Community 37
- Community 38
- Community 39
- Community 40
- Community 41
- Community 42
- Community 43
- Community 44
- Community 45
- Community 46
- Community 47
- Community 48
- Community 49
- Community 50
- Community 51
- Community 52
- Community 53
- Community 54
- Community 55
- Community 56
- Community 57
- Community 58
- Community 59
- Community 60
- Community 61

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 22 edges
2. `emit()` - 19 edges
3. `get_engine()` - 19 edges
4. `AssetStore` - 18 edges
5. `set_values()` - 17 edges
6. `root()` - 17 edges
7. `configure_logging()` - 17 edges
8. `init_db()` - 16 edges
9. `get_logger()` - 16 edges
10. `ThumbforgeError` - 14 edges

## Surprising Connections (you probably didn't know these)
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_sqlite_database_in_container()` --uses--> `ChannelSource`  [INFERRED]
  tests/integration/test_db_container.py → src/thumbforge/core/enums.py
- `test_sqlite_database_in_container()` --uses--> `Channel`  [INFERRED]
  tests/integration/test_db_container.py → src/thumbforge/storage/models.py
- `test_session_scope_commits_on_success()` --uses--> `Channel`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/storage/models.py

## Import Cycles
- None detected.

## Communities (62 total, 33 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic, pydantic_settings, Self (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (52): datetime, DeclarativeBase, E, enum, pytest, sqlalchemy, AssetKind, ChannelSource (+44 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (47): Argument, command, Console, Context, handle_errors, help, metavar, min (+39 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (37): hashlib, json, MonkeyPatch, Path, pathlib, main(), Compare a committed graphify graph against a freshly extracted one. Only the…, structure() (+29 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (40): Exception, IntEnum, AssetError, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError (+32 more)

### Community 5 - "Community 5"
Cohesion: 0.16
Nodes (26): BoundLogger, CaptureFixture, LogFormat, configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``., Configure structlog and the stdlib root logger. Safe to call more than once. (+18 more)

### Community 6 - "Community 6"
Cohesion: 0.14
Nodes (16): contextlib, io, _make_jpeg_bytes(), _make_png_bytes(), Unit tests for content-addressed AssetStore (PLAN.md §3.2, ADR 0011)., Bytes Pillow cannot identify are rejected, and the temp file is cleaned up., A valid image outside the JPEG/PNG/WebP allowlist is rejected with a hint., A failed insert never unlinks the published file, and a retry adopts it. A… (+8 more)

### Community 7 - "Community 7"
Cohesion: 0.16
Nodes (13): Asset, AssetKind, Session, sessionmaker, AssetStore, _fsync_dir(), Path, Return the absolute path on disk for ``asset``. (+5 more)

### Community 8 - "Community 8"
Cohesion: 0.18
Nodes (15): parametrize, re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure. (+7 more)

### Community 9 - "Community 9"
Cohesion: 0.13
Nodes (13): alembic_config, alembic_runtime_migration, alembic_script, Connection, ConnectionPoolEntry, sqlalchemy_pool, sqlite3, DbStatus (+5 more)

### Community 10 - "Community 10"
Cohesion: 0.19
Nodes (14): AppContext, functools, P, R, rich_console, _app_context(), handle_errors(), wrapper() (+6 more)

### Community 11 - "Community 11"
Cohesion: 0.15
Nodes (13): dataclasses, rich_panel, rich_syntax, rich_table, ``thumbforge config`` — inspect and edit the configuration file., get_app_context(), panel(), Context (+5 more)

### Community 12 - "Community 12"
Cohesion: 0.18
Nodes (15): fixture, integration, Session, sessionmaker, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., session_factory(), session_scope() (+7 more)

### Community 13 - "Community 13"
Cohesion: 0.14
Nodes (14): callback, count, envvar, is_eager, handle_errors, Path, thumbforge command-line interface., root() (+6 more)

### Community 14 - "Community 14"
Cohesion: 0.18
Nodes (9): main(), Root Typer application: global flags, context construction, sub-app…, The exit-code contract: a script parsing our status codes must never be…, test_keyboard_interrupt_exits_130(), test_unexpected_exception_is_not_swallowed(), thumbforge_cli, thumbforge_cli_errors, thumbforge_cli_render (+1 more)

### Community 15 - "Community 15"
Cohesion: 0.17
Nodes (13): _backdate(), parametrize, Path, A `Path` source that does not exist fails before anything is written., `db vacuum` deletes expired unreferenced files and stale tmp entries (ADR 0011)., A file from an in-flight `put` is newer than the grace age, so vacuum leaves…, A non-positive window would let vacuum delete an in-flight write's files., Age files past the vacuum grace window without sleeping. (+5 more)

### Community 16 - "Community 16"
Cohesion: 0.21
Nodes (11): alembic, Format a SQLite connection URL for SQLAlchemy., sqlite_url(), get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database. (+3 more)

### Community 17 - "Community 17"
Cohesion: 0.21
Nodes (10): pil, shutil, sqlalchemy_exc, sqlalchemy_orm, Content-addressed local image asset store (PLAN.md §3.2, ADR 0011)., Storage layer for thumbforge (SQLite + SQLAlchemy 2.0 + Alembic)., thumbforge_core_enums, thumbforge_core_ids (+2 more)

### Community 18 - "Community 18"
Cohesion: 0.20
Nodes (6): collections_abc, structlog, Shared fixtures. Establishes ``tests/`` as the pytest root., Unit tests for Alembic migrations and drift detection (ADR 0004, Phase 1 spec)., thumbforge, typing

### Community 19 - "Community 19"
Cohesion: 0.18
Nodes (10): os, new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of ``data``., Return the hex SHA-256 of a file, read in chunks so large images stay off the…, sha256_bytes() (+2 more)

### Community 20 - "Community 20"
Cohesion: 0.25
Nodes (10): ``thumbforge db`` — database lifecycle and migration management (ADR 0004)., Print current revision, head revision, pending count, file size, and journal…, status(), DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., get_db_status(), Inspect migration revision and file metadata for ``db_path``., Run Alembic upgrade to ``revision`` on ``db_path``. (+2 more)

### Community 21 - "Community 21"
Cohesion: 0.31
Nodes (10): init_db(), Ensure directory exists and upgrade DB to head. Returns: Tuple of…, Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_engine_pragmas_on_memory(), test_get_db_status_nonexistent_and_initialized(), test_init_db_and_idempotence() (+2 more)

### Community 22 - "Community 22"
Cohesion: 0.29
Nodes (9): Engine, get_engine(), Path, Reclaim free space, truncate the WAL, and delete unreferenced asset files.…, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the…, Create a SQLAlchemy engine configured for thumbforge SQLite usage., _reclaim_orphans(), vacuum_db() (+1 more)

### Community 23 - "Community 23"
Cohesion: 0.22
Nodes (7): Settings, AppContext, Per-invocation state built by the root callback and stored on ``ctx.obj``., Return the settings, or re-raise the failure that prevented loading them.…, Ctrl-C during a batch must still leave machine mode with parseable output., test_keyboard_interrupt_in_json_mode_emits_one_line_on_stderr(), root()

### Community 24 - "Community 24"
Cohesion: 0.25
Nodes (7): logging_handlers, bind(), clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Bind context onto every subsequent log record in this task (run id, provider,…, Drop all bound context., structlog_stdlib

### Community 25 - "Community 25"
Cohesion: 0.25
Nodes (8): Return a copy of ``value`` with every secret-keyed entry replaced. A copy,…, redact(), Replace secret-looking values anywhere in the event dict (ADR 0017). Logs reach…, redact_secrets(), The batch resume identifier must stay readable in logs, or debugging a run is…, Logging observes data; it must never alter a caller's dict., test_idempotency_key_survives_a_log_record(), test_redaction_does_not_mutate_the_caller_structure()

### Community 26 - "Community 26"
Cohesion: 0.33
Nodes (7): Config, _alembic_config(), Build an Alembic configuration targeting ``db_path``., Path, CI gate: assert alembic check reports no drift between ORM models and…, test_alembic_check_no_drift(), test_migrations_upgrade_and_downgrade()

### Community 27 - "Community 27"
Cohesion: 0.40
Nodes (4): parametrize, Every error in CASES exits with the code documented in PLAN.md 5.1., test_error_maps_to_documented_exit_code(), ThumbforgeError

### Community 28 - "Community 28"
Cohesion: 0.50
Nodes (4): isolate_user_environment(), MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 279 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `root()` connect `Community 13` to `Community 0`, `Community 2`, `Community 5`, `Community 14`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `SettingsError` connect `Community 0` to `Community 2`, `Community 4`, `Community 11`, `Community 13`, `Community 14`, `Community 23`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `AssetStore` connect `Community 7` to `Community 17`, `Community 12`, `Community 6`, `Community 15`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `load_settings()` (e.g. with `root()` and `SettingsError`) actually correct?**
  _`load_settings()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `emit()` (e.g. with `init_()` and `path_()`) actually correct?**
  _`emit()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `get_engine()` (e.g. with `_set_sqlite_pragmas()` and `asset_store()`) actually correct?**
  _`get_engine()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._