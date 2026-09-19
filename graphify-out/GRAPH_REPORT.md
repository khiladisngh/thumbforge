# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 545 nodes · 1059 edges · 43 communities (15 shown, 28 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 80 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `854d660a`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 22 edges
2. `emit()` - 20 edges
3. `get_engine()` - 19 edges
4. `set_values()` - 17 edges
5. `root()` - 17 edges
6. `configure_logging()` - 17 edges
7. `get_logger()` - 16 edges
8. `init_db()` - 15 edges
9. `Base` - 14 edges
10. `test_insert_all_nine_models_and_verify_relations()` - 14 edges

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

## Communities (43 total, 28 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic, pydantic_settings, Self (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (52): datetime, DeclarativeBase, E, enum, sqlalchemy, sqlalchemy_exc, AssetKind, ChannelSource (+44 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (42): AppContext, Console, dataclasses, functools, json, P, R, rich_console (+34 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (48): BoundLogger, callback, CaptureFixture, Context, count, envvar, is_eager, LogFormat (+40 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (34): collections_abc, fixture, hashlib, MonkeyPatch, os, pathlib, pytest, new_id() (+26 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (38): Exception, IntEnum, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError, ProviderError (+30 more)

### Community 6 - "Community 6"
Cohesion: 0.07
Nodes (38): Argument, help, metavar, Option, rich_syntax, Settings, _as_toml(), _config_path() (+30 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (27): Path, Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode() (+19 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (23): parametrize, re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure. (+15 more)

### Community 9 - "Community 9"
Cohesion: 0.17
Nodes (20): Engine, integration, Session, sessionmaker, get_engine(), Reclaim free space and truncate the WAL file., Create a SQLAlchemy engine configured for thumbforge SQLite usage., Create a thread-safe sessionmaker bound to ``engine``. (+12 more)

### Community 10 - "Community 10"
Cohesion: 0.20
Nodes (18): RenderableType, init_(), path_(), command, Context, handle_errors, ``thumbforge db`` — database lifecycle and migration management (ADR 0004)., Print the SQLite database file path. (+10 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (15): alembic_config, alembic_runtime_migration, alembic_script, Connection, ConnectionPoolEntry, contextlib, sqlalchemy_orm, sqlalchemy_pool (+7 more)

### Community 12 - "Community 12"
Cohesion: 0.20
Nodes (16): Config, DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., _alembic_config(), get_db_status(), init_db(), Path, Build an Alembic configuration targeting ``db_path``. (+8 more)

### Community 13 - "Community 13"
Cohesion: 0.28
Nodes (8): alembic, get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline(), run_migrations_online()

### Community 14 - "Community 14"
Cohesion: 0.32
Nodes (7): Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_engine_pragmas_on_memory(), test_init_db_and_idempotence(), test_sqlite_url_formats_path(), thumbforge_core_enums

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 248 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `root()` connect `Community 3` to `Community 0`, `Community 2`, `Community 6`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `SettingsError` connect `Community 0` to `Community 2`, `Community 3`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 0` to `Community 3`, `Community 13`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `load_settings()` (e.g. with `root()` and `SettingsError`) actually correct?**
  _`load_settings()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `emit()` (e.g. with `test_json_mode_output_round_trips()` and `test_non_finite_floats_are_rejected()`) actually correct?**
  _`emit()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.051490514905149054 - nodes in this community are weakly interconnected._