# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 586 nodes · 1132 edges · 45 communities (16 shown, 29 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 98 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `db149bb3`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 22 edges
2. `emit()` - 20 edges
3. `get_engine()` - 19 edges
4. `set_values()` - 17 edges
5. `root()` - 17 edges
6. `configure_logging()` - 17 edges
7. `AssetStore` - 16 edges
8. `get_logger()` - 16 edges
9. `init_db()` - 15 edges
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

## Communities (45 total, 29 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic, pydantic_settings, Self (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (60): datetime, DeclarativeBase, E, enum, pil, shutil, sqlalchemy, sqlalchemy_exc (+52 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (48): Argument, Console, help, metavar, Option, RenderableType, rich_syntax, Settings (+40 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (48): BoundLogger, callback, CaptureFixture, Context, count, envvar, is_eager, LogFormat (+40 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (36): AppContext, dataclasses, functools, json, P, R, rich_console, rich_panel (+28 more)

### Community 5 - "Community 5"
Cohesion: 0.06
Nodes (40): Exception, IntEnum, AssetError, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError (+32 more)

### Community 6 - "Community 6"
Cohesion: 0.07
Nodes (37): Asset, AssetKind, fixture, io, MonkeyPatch, new_id(), Path, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits. (+29 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (27): Path, Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode() (+19 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (18): collections_abc, hashlib, os, pathlib, pytest, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return the hex SHA-256 of ``data``., sha256_bytes() (+10 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (23): parametrize, re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure. (+15 more)

### Community 10 - "Community 10"
Cohesion: 0.15
Nodes (24): init_(), path_(), command, Context, handle_errors, ``thumbforge db`` — database lifecycle and migration management (ADR 0004)., Print the SQLite database file path., Reclaim unused disk space and checkpoint the Write-Ahead Log (WAL). (+16 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (14): alembic_config, alembic_runtime_migration, alembic_script, Connection, ConnectionPoolEntry, contextlib, sqlalchemy_pool, sqlite3 (+6 more)

### Community 12 - "Community 12"
Cohesion: 0.27
Nodes (14): get_engine(), init_db(), Ensure directory exists and upgrade DB to head. Returns: Tuple of…, Create a SQLAlchemy engine configured for thumbforge SQLite usage., Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_engine_pragmas_on_memory() (+6 more)

### Community 13 - "Community 13"
Cohesion: 0.22
Nodes (13): Engine, integration, Session, sessionmaker, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., session_factory(), session_scope() (+5 more)

### Community 14 - "Community 14"
Cohesion: 0.24
Nodes (10): alembic, Format a SQLite connection URL for SQLAlchemy., sqlite_url(), get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database. (+2 more)

### Community 15 - "Community 15"
Cohesion: 0.33
Nodes (7): Config, _alembic_config(), Build an Alembic configuration targeting ``db_path``., Path, CI gate: assert alembic check reports no drift between ORM models and…, test_alembic_check_no_drift(), test_migrations_upgrade_and_downgrade()

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 261 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `root()` connect `Community 3` to `Community 0`, `Community 2`, `Community 4`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `SettingsError` connect `Community 0` to `Community 2`, `Community 3`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 0` to `Community 3`, `Community 14`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `load_settings()` (e.g. with `root()` and `SettingsError`) actually correct?**
  _`load_settings()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `emit()` (e.g. with `test_json_mode_output_round_trips()` and `test_non_finite_floats_are_rejected()`) actually correct?**
  _`emit()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `get_engine()` (e.g. with `_set_sqlite_pragmas()` and `asset_store()`) actually correct?**
  _`get_engine()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._