# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 583 nodes · 1131 edges · 46 communities (17 shown, 29 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 98 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a986d506`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 22 edges
2. `emit()` - 20 edges
3. `get_engine()` - 19 edges
4. `AssetStore` - 17 edges
5. `set_values()` - 17 edges
6. `root()` - 17 edges
7. `configure_logging()` - 17 edges
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

## Communities (46 total, 29 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic, pydantic_settings, Self (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (59): datetime, DeclarativeBase, E, enum, shutil, sqlalchemy, sqlalchemy_exc, sqlalchemy_orm (+51 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (42): AppContext, Console, dataclasses, functools, json, P, R, rich_console (+34 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (48): BoundLogger, callback, CaptureFixture, Context, count, envvar, is_eager, LogFormat (+40 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (38): Exception, IntEnum, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError, ProviderError (+30 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (38): Argument, help, metavar, Option, rich_syntax, Settings, _as_toml(), _config_path() (+30 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (27): Asset, AssetKind, io, pil, AssetError, An asset could not be written, verified, or identified., Path, Return the hex SHA-256 of a file, read in chunks so large images stay off the… (+19 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (27): Path, Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode() (+19 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (25): collections_abc, parametrize, re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw… (+17 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (23): hashlib, MonkeyPatch, os, pathlib, pytest, new_id(), Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits. (+15 more)

### Community 10 - "Community 10"
Cohesion: 0.14
Nodes (25): Engine, fixture, integration, Session, sessionmaker, get_engine(), Create a SQLAlchemy engine configured for thumbforge SQLite usage., Create a thread-safe sessionmaker bound to ``engine``. (+17 more)

### Community 11 - "Community 11"
Cohesion: 0.20
Nodes (18): RenderableType, init_(), path_(), command, Context, handle_errors, ``thumbforge db`` — database lifecycle and migration management (ADR 0004)., Print the SQLite database file path. (+10 more)

### Community 12 - "Community 12"
Cohesion: 0.20
Nodes (16): Config, DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., _alembic_config(), get_db_status(), init_db(), Path, Build an Alembic configuration targeting ``db_path``. (+8 more)

### Community 13 - "Community 13"
Cohesion: 0.15
Nodes (13): alembic, alembic_config, alembic_runtime_migration, alembic_script, contextlib, sqlalchemy_pool, sqlite3, Database engine, session management, and migration execution (PLAN.md §3, ADR… (+5 more)

### Community 14 - "Community 14"
Cohesion: 0.24
Nodes (10): Format a SQLite connection URL for SQLAlchemy., sqlite_url(), get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline() (+2 more)

### Community 15 - "Community 15"
Cohesion: 0.50
Nodes (4): Connection, ConnectionPoolEntry, Apply PRAGMA statements required by ADR 0004 on every SQLite connection., _set_sqlite_pragmas()

### Community 16 - "Community 16"
Cohesion: 0.50
Nodes (3): DbStatus, Whether the database is fully migrated to the latest revision., Migration status and storage health metadata.

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 258 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `root()` connect `Community 3` to `Community 0`, `Community 2`, `Community 5`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `SettingsError` connect `Community 0` to `Community 2`, `Community 3`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 0` to `Community 3`, `Community 14`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `load_settings()` (e.g. with `root()` and `SettingsError`) actually correct?**
  _`load_settings()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `emit()` (e.g. with `test_json_mode_output_round_trips()` and `test_non_finite_floats_are_rejected()`) actually correct?**
  _`emit()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `get_engine()` (e.g. with `_set_sqlite_pragmas()` and `asset_store()`) actually correct?**
  _`get_engine()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._