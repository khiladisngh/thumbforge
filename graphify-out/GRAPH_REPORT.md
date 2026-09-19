# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 577 nodes · 1282 edges · 27 communities (25 shown, 2 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 122 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3ff0f309`
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

## God Nodes (most connected - your core abstractions)
1. `SettingsError` - 25 edges
2. `load_settings()` - 24 edges
3. `AssetStore` - 21 edges
4. `AppContext` - 21 edges
5. `AssetKind` - 20 edges
6. `get_engine()` - 20 edges
7. `handle_errors()` - 20 edges
8. `emit()` - 20 edges
9. `root()` - 19 edges
10. `ThumbforgeError` - 18 edges

## Surprising Connections (you probably didn't know these)
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_insert_all_nine_models_and_verify_relations()` --uses--> `AssetKind`  [INFERRED]
  tests/unit/test_storage_models.py → src/thumbforge/core/enums.py
- `test_on_delete_restrict_on_reference_asset()` --uses--> `AssetKind`  [INFERRED]
  tests/unit/test_storage_models.py → src/thumbforge/core/enums.py
- `test_keyboard_interrupt_in_json_mode_emits_one_line_on_stderr()` --uses--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `root()` --calls--> `AppContext`  [EXTRACTED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py

## Import Cycles
- None detected.

## Communities (27 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (76): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic, pydantic_settings, Self (+68 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (59): contextlib, io, pil, shutil, sqlalchemy_exc, sqlalchemy_orm, AssetKind, Functional role of a stored image asset. (+51 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (48): datetime, DeclarativeBase, E, enum, sqlalchemy, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, Lifecycle classification of a thumbnail generation run. (+40 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (49): BoundLogger, callback, CaptureFixture, count, envvar, is_eager, LogFormat, logging_handlers (+41 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (38): Argument, Console, metavar, P, R, RenderableType, _as_toml(), _config_path() (+30 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (26): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+18 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (19): collections_abc, dataclasses, functools, pathlib, rich_console, rich_panel, rich_syntax, rich_table (+11 more)

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (23): re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 8 - "Community 8"
Cohesion: 0.15
Nodes (15): alembic, alembic_config, alembic_runtime_migration, alembic_script, Config, sqlalchemy_pool, sqlite3, _alembic_config() (+7 more)

### Community 9 - "Community 9"
Cohesion: 0.18
Nodes (16): min, init_(), path_(), command, Context, help, Option, ``thumbforge db`` — database lifecycle and migration management (ADR 0004). (+8 more)

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (11): hashlib, pytest, Domain layer: models, errors and services. Imports nothing internal except…, testcontainers_core_container, Integration tests using Testcontainers for database verification (ADR 0004)., MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they… (+3 more)

### Community 11 - "Community 11"
Cohesion: 0.17
Nodes (16): _app_context(), wrapper(), _is_json_mode(), Find the :class:`AppContext` the root callback stored on the Click context.…, _report(), AppContext, get_app_context(), Context (+8 more)

### Community 12 - "Community 12"
Cohesion: 0.17
Nodes (15): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError, Error hierarchy and the exit codes it maps to. Every failure the user can… (+7 more)

### Community 13 - "Community 13"
Cohesion: 0.17
Nodes (15): DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., get_db_status(), Path, Inspect migration revision and file metadata for ``db_path``., Run Alembic upgrade to ``revision`` on ``db_path``., Reclaim free space, truncate the WAL, and delete unreferenced asset files.…, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the… (+7 more)

### Community 14 - "Community 14"
Cohesion: 0.27
Nodes (14): get_engine(), init_db(), Ensure directory exists and upgrade DB to head. Returns: Tuple of…, Create a SQLAlchemy engine configured for thumbforge SQLite usage., Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_engine_pragmas_on_memory() (+6 more)

### Community 15 - "Community 15"
Cohesion: 0.20
Nodes (14): Engine, integration, Session, sessionmaker, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., session_factory(), session_scope() (+6 more)

### Community 16 - "Community 16"
Cohesion: 0.17
Nodes (10): NotFoundError, A referenced entity does not exist., parametrize, The exit-code contract: a script parsing our status codes must never be…, Every error in CASES exits with the code documented in PLAN.md 5.1., test_error_maps_to_documented_exit_code(), test_hint_and_code_reach_stderr(), boom() (+2 more)

### Community 17 - "Community 17"
Cohesion: 0.18
Nodes (9): Exception, PartialBatchError, A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., A metadata source failed., SourceError, TemplateError (+1 more)

### Community 18 - "Community 18"
Cohesion: 0.27
Nodes (9): Format a SQLite connection URL for SQLAlchemy., sqlite_url(), get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline() (+1 more)

### Community 19 - "Community 19"
Cohesion: 0.22
Nodes (7): IntEnum, ExitCode, Process exit statuses. Values are a public contract., Ctrl-C during a batch must still leave machine mode with parseable output., test_keyboard_interrupt_exits_130(), test_keyboard_interrupt_in_json_mode_emits_one_line_on_stderr(), root()

### Community 20 - "Community 20"
Cohesion: 0.29
Nodes (5): importlib_metadata, os, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, structlog, Shared fixtures. Establishes ``tests/`` as the pytest root.

### Community 21 - "Community 21"
Cohesion: 0.40
Nodes (5): json, main(), Path, Compare a committed graphify graph against a freshly extracted one. Only the…, structure()

### Community 22 - "Community 22"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 23 - "Community 23"
Cohesion: 0.50
Nodes (4): Connection, ConnectionPoolEntry, Apply PRAGMA statements required by ADR 0004 on every SQLite connection., _set_sqlite_pragmas()

### Community 24 - "Community 24"
Cohesion: 0.50
Nodes (3): DbStatus, Whether the database is fully migrated to the latest revision., Migration status and storage health metadata.

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 259 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SettingsError` connect `Community 0` to `Community 3`, `Community 4`, `Community 6`, `Community 11`, `Community 12`, `Community 17`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `root()` connect `Community 3` to `Community 0`, `Community 11`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 0` to `Community 18`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `SettingsError` (e.g. with `root()` and `set_()`) actually correct?**
  _`SettingsError` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `AssetStore` (e.g. with `AssetKind` and `AssetError`) actually correct?**
  _`AssetStore` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `AppContext` (e.g. with `root()` and `_config_path()`) actually correct?**
  _`AppContext` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._