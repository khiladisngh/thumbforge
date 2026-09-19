# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 586 nodes · 1132 edges · 52 communities (21 shown, 31 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 98 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `17c47f4d`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 22 edges
2. `emit()` - 20 edges
3. `get_engine()` - 19 edges
4. `set_values()` - 17 edges
5. `configure_logging()` - 17 edges
6. `root()` - 17 edges
7. `AssetStore` - 16 edges
8. `get_logger()` - 16 edges
9. `init_db()` - 15 edges
10. `ThumbforgeError` - 14 edges

## Surprising Connections (you probably didn't know these)
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_sqlite_database_in_container()` --uses--> `ChannelSource`  [INFERRED]
  tests/integration/test_db_container.py → src/thumbforge/core/enums.py
- `test_sqlite_database_in_container()` --uses--> `Channel`  [INFERRED]
  tests/integration/test_db_container.py → src/thumbforge/storage/models.py
- `test_session_scope_commits_on_success()` --uses--> `Channel`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/storage/models.py
- `test_session_scope_rolls_back_on_error()` --uses--> `Channel`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/storage/models.py

## Import Cycles
- None detected.

## Communities (52 total, 31 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic, pydantic_settings, Self (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (49): datetime, DeclarativeBase, E, enum, sqlalchemy, AssetKind, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md… (+41 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (38): Console, hashlib, os, pathlib, pytest, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return the hex SHA-256 of ``data``., sha256_bytes() (+30 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (37): Exception, IntEnum, AssetError, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError (+29 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (38): BoundLogger, CaptureFixture, LogFormat, logging_handlers, bind(), clear_context(), configure_logging(), get_logger() (+30 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (30): io, MonkeyPatch, pil, shutil, sqlalchemy_exc, sqlalchemy_orm, AssetStore, src_thumbforge_storage_assets_assetstoreerror (+22 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (30): Argument, callback, Context, count, envvar, help, is_eager, metavar (+22 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (26): Asset, AssetKind, Path, new_id(), Path, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of a file, read in chunks so large images stay off the…, sha256_file() (+18 more)

### Community 8 - "Community 8"
Cohesion: 0.14
Nodes (25): Engine, fixture, integration, Session, sessionmaker, get_engine(), init_db(), Ensure directory exists and upgrade DB to head. Returns: Tuple of… (+17 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (23): parametrize, re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure. (+15 more)

### Community 10 - "Community 10"
Cohesion: 0.20
Nodes (18): RenderableType, init_(), path_(), command, Context, handle_errors, ``thumbforge db`` — database lifecycle and migration management (ADR 0004)., Print the SQLite database file path. (+10 more)

### Community 11 - "Community 11"
Cohesion: 0.13
Nodes (17): rich_panel, rich_syntax, rich_table, ``thumbforge config`` — inspect and edit the configuration file., get_app_context(), kv(), panel(), Context (+9 more)

### Community 12 - "Community 12"
Cohesion: 0.12
Nodes (14): alembic_config, alembic_runtime_migration, alembic_script, Connection, ConnectionPoolEntry, contextlib, sqlalchemy_pool, sqlite3 (+6 more)

### Community 13 - "Community 13"
Cohesion: 0.19
Nodes (15): Config, DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., _alembic_config(), get_db_status(), Path, Build an Alembic configuration targeting ``db_path``., Inspect migration revision and file metadata for ``db_path``. (+7 more)

### Community 14 - "Community 14"
Cohesion: 0.21
Nodes (13): AppContext, functools, P, R, _app_context(), handle_errors(), wrapper(), _is_json_mode() (+5 more)

### Community 15 - "Community 15"
Cohesion: 0.21
Nodes (11): alembic, Format a SQLite connection URL for SQLAlchemy., sqlite_url(), get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database. (+3 more)

### Community 16 - "Community 16"
Cohesion: 0.17
Nodes (10): Settings, AppContext, Per-invocation state built by the root callback and stored on ``ctx.obj``., Return the settings, or re-raise the failure that prevented loading them.…, Machine mode contract: stdout carries command output, stderr carries the…, Ctrl-C during a batch must still leave machine mode with parseable output., test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), root() (+2 more)

### Community 17 - "Community 17"
Cohesion: 0.18
Nodes (7): The exit-code contract: a script parsing our status codes must never be…, test_error_maps_to_documented_exit_code(), test_keyboard_interrupt_exits_130(), test_unexpected_exception_is_not_swallowed(), thumbforge_cli_errors, ThumbforgeError, typer

### Community 18 - "Community 18"
Cohesion: 0.33
Nodes (5): dataclasses, rich_console, main(), Root Typer application: global flags, context construction, sub-app…, thumbforge_cli

### Community 19 - "Community 19"
Cohesion: 0.38
Nodes (6): Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_engine_pragmas_on_memory(), test_get_db_status_nonexistent_and_initialized(), test_init_db_and_idempotence()

### Community 20 - "Community 20"
Cohesion: 0.40
Nodes (5): json, main(), Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 262 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `root()` connect `Community 6` to `Community 0`, `Community 18`, `Community 4`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `SettingsError` connect `Community 0` to `Community 3`, `Community 6`, `Community 11`, `Community 16`, `Community 18`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 0` to `Community 6`, `Community 15`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `load_settings()` (e.g. with `root()` and `SettingsError`) actually correct?**
  _`load_settings()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `emit()` (e.g. with `test_json_mode_output_round_trips()` and `test_non_finite_floats_are_rejected()`) actually correct?**
  _`emit()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `get_engine()` (e.g. with `_set_sqlite_pragmas()` and `asset_store()`) actually correct?**
  _`get_engine()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._