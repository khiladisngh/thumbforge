# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 652 nodes · 1431 edges · 26 communities (24 shown, 2 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 145 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `95006ca0`
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

## God Nodes (most connected - your core abstractions)
1. `SettingsError` - 25 edges
2. `load_settings()` - 24 edges
3. `AssetStore` - 21 edges
4. `AppContext` - 21 edges
5. `AssetKind` - 20 edges
6. `handle_errors()` - 20 edges
7. `get_engine()` - 20 edges
8. `emit()` - 20 edges
9. `ThumbforgeError` - 19 edges
10. `root()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_insert_all_nine_models_and_verify_relations()` --uses--> `AssetKind`  [INFERRED]
  tests/unit/test_storage_models.py → src/thumbforge/core/enums.py
- `test_on_delete_restrict_on_reference_asset()` --uses--> `AssetKind`  [INFERRED]
  tests/unit/test_storage_models.py → src/thumbforge/core/enums.py
- `test_error_maps_to_documented_exit_code()` --uses--> `ThumbforgeError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py
- `test_only_transient_and_timeout_are_retryable()` --uses--> `ProviderAuthError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py

## Import Cycles
- None detected.

## Communities (26 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic_settings, Self, Return the settings, or re-raise the failure that prevented loading them.… (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (58): io, pil, shutil, sqlalchemy_exc, sqlalchemy_orm, AssetKind, Functional role of a stored image asset., AssetError (+50 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (45): importlib_metadata, os, pathlib, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, structlog, testcontainers_core_container, isolate_user_environment(), fixture (+37 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (44): datetime, field_validator, Protocol, pydantic, ChannelMeta, _Meta, PlaylistItemMeta, PlaylistMeta (+36 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (49): DeclarativeBase, E, enum, sqlalchemy, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run. (+41 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (49): BoundLogger, callback, CaptureFixture, count, envvar, is_eager, LogFormat, logging_handlers (+41 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (29): hashlib, parametrize, pytest, re, A supplied URL or identifier is not recognisable YouTube input., UrlError, Domain layer: models, errors and services. Imports nothing internal except…, What a URL or bare identifier turned out to be (ADR 0005). (+21 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (30): Argument, Console, metavar, RenderableType, _as_toml(), _config_path(), init_(), path_() (+22 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (23): collections_abc, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 9 - "Community 9"
Cohesion: 0.11
Nodes (19): dataclasses, rich_console, rich_panel, rich_syntax, rich_table, main(), Root Typer application: global flags, context construction, sub-app…, ``thumbforge config`` — inspect and edit the configuration file. (+11 more)

### Community 10 - "Community 10"
Cohesion: 0.14
Nodes (22): min, P, R, init_(), path_(), command, Context, help (+14 more)

### Community 11 - "Community 11"
Cohesion: 0.16
Nodes (17): Engine, integration, Session, sessionmaker, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the…, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., _reclaim_orphans() (+9 more)

### Community 12 - "Community 12"
Cohesion: 0.12
Nodes (14): alembic_config, alembic_runtime_migration, alembic_script, Connection, ConnectionPoolEntry, contextlib, sqlalchemy_pool, sqlite3 (+6 more)

### Community 13 - "Community 13"
Cohesion: 0.14
Nodes (13): Exception, NotFoundError, PartialBatchError, A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., A referenced entity does not exist., A metadata source failed. (+5 more)

### Community 14 - "Community 14"
Cohesion: 0.17
Nodes (15): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError, Error hierarchy and the exit codes it maps to. Every failure the user can… (+7 more)

### Community 15 - "Community 15"
Cohesion: 0.22
Nodes (12): functools, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.…, _report(), AppContext (+4 more)

### Community 16 - "Community 16"
Cohesion: 0.27
Nodes (12): Config, _alembic_config(), get_db_status(), init_db(), Path, Build an Alembic configuration targeting ``db_path``., Inspect migration revision and file metadata for ``db_path``., Ensure directory exists and upgrade DB to head. Returns: Tuple of… (+4 more)

### Community 17 - "Community 17"
Cohesion: 0.26
Nodes (11): get_engine(), Format a SQLite connection URL for SQLAlchemy., Create a SQLAlchemy engine configured for thumbforge SQLite usage., sqlite_url(), Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_engine_pragmas_on_memory() (+3 more)

### Community 18 - "Community 18"
Cohesion: 0.28
Nodes (8): alembic, get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline(), run_migrations_online()

### Community 19 - "Community 19"
Cohesion: 0.22
Nodes (6): parametrize, The exit-code contract: a script parsing our status codes must never be…, Every error in CASES exits with the code documented in PLAN.md 5.1., test_error_maps_to_documented_exit_code(), test_only_transient_and_timeout_are_retryable(), test_unexpected_exception_is_not_swallowed()

### Community 20 - "Community 20"
Cohesion: 0.32
Nodes (8): DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., Reclaim free space, truncate the WAL, and delete unreferenced asset files.…, vacuum_db(), parametrize, A non-positive window would let vacuum delete an in-flight write's files., test_vacuum_rejects_non_positive_grace(), test_vacuum_db_success_and_missing_error()

### Community 21 - "Community 21"
Cohesion: 0.33
Nodes (6): json, main(), Path, Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys

### Community 22 - "Community 22"
Cohesion: 0.40
Nodes (6): ComplianceError, A generated image violates the YouTube thumbnail requirements., Machine mode contract: stdout carries command output, stderr carries the…, test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), boom(), root()

### Community 23 - "Community 23"
Cohesion: 0.40
Nodes (4): IntEnum, ExitCode, Process exit statuses. Values are a public contract., test_keyboard_interrupt_exits_130()

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 292 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SettingsError` connect `Community 0` to `Community 5`, `Community 7`, `Community 9`, `Community 13`, `Community 14`, `Community 15`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `root()` connect `Community 5` to `Community 0`, `Community 9`, `Community 10`, `Community 15`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `handle_errors()` connect `Community 10` to `Community 5`, `Community 7`, `Community 9`, `Community 13`, `Community 15`, `Community 23`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `SettingsError` (e.g. with `root()` and `set_()`) actually correct?**
  _`SettingsError` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `AssetStore` (e.g. with `AssetKind` and `AssetError`) actually correct?**
  _`AssetStore` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `AppContext` (e.g. with `root()` and `_config_path()`) actually correct?**
  _`AppContext` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._