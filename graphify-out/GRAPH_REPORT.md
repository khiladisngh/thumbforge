# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 537 nodes · 1054 edges · 48 communities (21 shown, 27 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 81 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4e6965b8`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 22 edges
2. `emit()` - 20 edges
3. `get_engine()` - 18 edges
4. `set_values()` - 17 edges
5. `configure_logging()` - 17 edges
6. `root()` - 17 edges
7. `get_logger()` - 16 edges
8. `init_db()` - 15 edges
9. `Base` - 14 edges
10. `test_insert_all_nine_models_and_verify_relations()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_sqlite_database_in_container()` --uses--> `ChannelSource`  [INFERRED]
  tests/integration/test_db_container.py → src/thumbforge/core/enums.py
- `test_session_scope_commits_on_success()` --uses--> `ChannelSource`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/core/enums.py
- `test_session_scope_rolls_back_on_error()` --uses--> `ChannelSource`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/core/enums.py
- `test_sqlite_database_in_container()` --uses--> `Channel`  [INFERRED]
  tests/integration/test_db_container.py → src/thumbforge/storage/models.py

## Import Cycles
- None detected.

## Communities (48 total, 27 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic, pydantic_settings, Self (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (49): datetime, DeclarativeBase, sqlalchemy, sqlalchemy_exc, sqlalchemy_orm, AssetKind, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md… (+41 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (34): collections_abc, Console, fixture, hashlib, MonkeyPatch, os, pathlib, pytest (+26 more)

### Community 3 - "Community 3"
Cohesion: 0.10
Nodes (38): BoundLogger, CaptureFixture, LogFormat, logging_handlers, bind(), clear_context(), configure_logging(), get_logger() (+30 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (36): enum, Exception, IntEnum, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError (+28 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (27): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+19 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (30): Argument, callback, Context, count, envvar, help, is_eager, metavar (+22 more)

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (23): parametrize, re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure. (+15 more)

### Community 8 - "Community 8"
Cohesion: 0.13
Nodes (18): rich_panel, rich_syntax, rich_table, ``thumbforge config`` — inspect and edit the configuration file., get_app_context(), kv(), panel(), Context (+10 more)

### Community 9 - "Community 9"
Cohesion: 0.20
Nodes (18): RenderableType, init_(), path_(), command, Context, handle_errors, ``thumbforge db`` — database lifecycle and migration management (ADR 0004)., Print the SQLite database file path. (+10 more)

### Community 10 - "Community 10"
Cohesion: 0.20
Nodes (17): Engine, integration, Session, sessionmaker, get_engine(), Create a SQLAlchemy engine configured for thumbforge SQLite usage., Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error. (+9 more)

### Community 11 - "Community 11"
Cohesion: 0.15
Nodes (13): alembic, alembic_config, alembic_runtime_migration, alembic_script, contextlib, Database engine, session management, and migration execution (PLAN.md §3, ADR…, Apply PRAGMA statements required by ADR 0004 on every SQLite connection., _set_sqlite_pragmas() (+5 more)

### Community 12 - "Community 12"
Cohesion: 0.23
Nodes (14): Config, DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., _alembic_config(), get_db_status(), init_db(), Path, Build an Alembic configuration targeting ``db_path``. (+6 more)

### Community 13 - "Community 13"
Cohesion: 0.23
Nodes (12): AppContext, functools, P, R, _app_context(), handle_errors(), wrapper(), _is_json_mode() (+4 more)

### Community 14 - "Community 14"
Cohesion: 0.17
Nodes (10): Settings, AppContext, Per-invocation state built by the root callback and stored on ``ctx.obj``., Return the settings, or re-raise the failure that prevented loading them.…, Machine mode contract: stdout carries command output, stderr carries the…, Ctrl-C during a batch must still leave machine mode with parseable output., test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), root() (+2 more)

### Community 15 - "Community 15"
Cohesion: 0.18
Nodes (7): rich_console, The exit-code contract: a script parsing our status codes must never be…, test_error_maps_to_documented_exit_code(), test_keyboard_interrupt_exits_130(), test_unexpected_exception_is_not_swallowed(), thumbforge_cli_errors, ThumbforgeError

### Community 16 - "Community 16"
Cohesion: 0.24
Nodes (10): Format a SQLite connection URL for SQLAlchemy., sqlite_url(), get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline() (+2 more)

### Community 17 - "Community 17"
Cohesion: 0.28
Nodes (8): Reclaim free space and truncate the WAL file., vacuum_db(), Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_engine_pragmas_on_memory(), test_init_db_and_idempotence(), test_vacuum_db_success_and_missing_error()

### Community 18 - "Community 18"
Cohesion: 0.29
Nodes (7): json, Path, main(), Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys, test_sha256_file_matches_sha256_bytes()

### Community 19 - "Community 19"
Cohesion: 0.33
Nodes (5): dataclasses, main(), Root Typer application: global flags, context construction, sub-app…, thumbforge_cli, thumbforge_cli_render

### Community 20 - "Community 20"
Cohesion: 0.50
Nodes (3): DbStatus, Migration status and storage health metadata., Whether the database is fully migrated to the latest revision.

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 241 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `root()` connect `Community 6` to `Community 0`, `Community 3`, `Community 19`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `SettingsError` connect `Community 0` to `Community 4`, `Community 6`, `Community 8`, `Community 14`, `Community 19`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 0` to `Community 16`, `Community 6`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `load_settings()` (e.g. with `root()` and `SettingsError`) actually correct?**
  _`load_settings()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `emit()` (e.g. with `test_json_mode_output_round_trips()` and `test_non_finite_floats_are_rejected()`) actually correct?**
  _`emit()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.051490514905149054 - nodes in this community are weakly interconnected._