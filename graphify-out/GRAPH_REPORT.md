# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 800 nodes · 1673 edges · 38 communities (32 shown, 6 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 158 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cdf757d2`
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
- `asset_store()` --uses--> `AssetStore`  [INFERRED]
  tests/unit/test_assets.py → src/thumbforge/storage/assets.py
- `test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout()` --uses--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py

## Import Cycles
- None detected.

## Communities (38 total, 6 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (73): BaseModel, BaseSettings, model_validator, platformdirs, pydantic_settings, Self, Return the settings, or re-raise the failure that prevented loading them.…, Configuration is missing, malformed, or contains something it must not. (+65 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (55): io, pil, shutil, sqlalchemy_exc, sqlalchemy_orm, AssetKind, Functional role of a stored image asset., AssetError (+47 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (52): BoundLogger, callback, CaptureFixture, count, envvar, is_eager, LogFormat, logging_handlers (+44 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (48): field_validator, Protocol, pydantic, ChannelMeta, _Meta, PlaylistItemMeta, PlaylistMeta, datetime (+40 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (49): DeclarativeBase, E, enum, sqlalchemy, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run. (+41 more)

### Community 5 - "Community 5"
Cohesion: 0.06
Nodes (45): asyncio, ChannelMeta, contextlib, datetime, PlaylistMeta, RawInfo, RetryCallState, Metadata sources: YouTube metadata providers behind one Protocol (ADR 0005). (+37 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (36): parametrize, ResolvedUrl, A supplied URL or identifier is not recognisable YouTube input., UrlError, What a URL or bare identifier turned out to be (ADR 0005)., ResolvedUrl, _channel_handle(), classify_id() (+28 more)

### Community 7 - "Community 7"
Cohesion: 0.08
Nodes (29): NotFoundError, PartialBatchError, ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError (+21 more)

### Community 8 - "Community 8"
Cohesion: 0.07
Nodes (23): hashlib, importlib_metadata, os, pathlib, pytest, Domain layer: models, errors and services. Imports nothing internal except…, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, structlog (+15 more)

### Community 9 - "Community 9"
Cohesion: 0.10
Nodes (26): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+18 more)

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (23): re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 11 - "Community 11"
Cohesion: 0.13
Nodes (23): Argument, metavar, P, R, rich_syntax, _config_path(), init_(), path_() (+15 more)

### Community 12 - "Community 12"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, Yield `exc` and its `cause` links; `ExtractorError` nests the real failure… (+16 more)

### Community 13 - "Community 13"
Cohesion: 0.17
Nodes (20): init_(), path_(), command, Context, ``thumbforge db`` — database lifecycle and migration management (ADR 0004)., Print the SQLite database file path., Create the database file and upgrade schema to Alembic head., Apply pending Alembic migrations up to head. (+12 more)

### Community 14 - "Community 14"
Cohesion: 0.14
Nodes (19): _fixture(), `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get…, `position` comes from enumeration order because `playlist_index` is absent… (+11 more)

### Community 15 - "Community 15"
Cohesion: 0.16
Nodes (17): Engine, integration, Session, sessionmaker, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the…, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., _reclaim_orphans() (+9 more)

### Community 16 - "Community 16"
Cohesion: 0.18
Nodes (15): functools, IntEnum, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.…, _report() (+7 more)

### Community 17 - "Community 17"
Cohesion: 0.12
Nodes (12): collections_abc, dataclasses, rich_panel, rich_table, get_app_context(), panel(), Context, The only module allowed to write to stdout. Every command produces one of two… (+4 more)

### Community 18 - "Community 18"
Cohesion: 0.13
Nodes (13): alembic_config, alembic_runtime_migration, alembic_script, Connection, ConnectionPoolEntry, sqlalchemy_pool, sqlite3, DbStatus (+5 more)

### Community 19 - "Community 19"
Cohesion: 0.19
Nodes (13): DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., get_engine(), Reclaim free space, truncate the WAL, and delete unreferenced asset files.…, Create a SQLAlchemy engine configured for thumbforge SQLite usage., vacuum_db(), asset_store(), fixture (+5 more)

### Community 20 - "Community 20"
Cohesion: 0.26
Nodes (11): Console, RenderableType, emit(), JsonValue, Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.…, _json_context(), `emit` is the machine boundary: what it prints must always be parseable JSON., test_json_mode_output_round_trips() (+3 more)

### Community 21 - "Community 21"
Cohesion: 0.24
Nodes (10): alembic, Format a SQLite connection URL for SQLAlchemy., sqlite_url(), get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database. (+2 more)

### Community 22 - "Community 22"
Cohesion: 0.22
Nodes (9): Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, Extractor stub that returns a fixture and remembers how it was called., _Recorder, test_entry_without_an_id_is_a_source_error(), test_unexpected_metadata_shape_is_a_source_error() (+1 more)

### Community 23 - "Community 23"
Cohesion: 0.22
Nodes (11): MonkeyPatch, A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs., test_retry_emits_a_log_event() (+3 more)

### Community 24 - "Community 24"
Cohesion: 0.20
Nodes (8): Extractor, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes…, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch., test_permanent_failures_are_not_retried(), test_satisfies_the_metadata_source_protocol()

### Community 25 - "Community 25"
Cohesion: 0.31
Nodes (9): Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_engine_pragmas_on_memory(), test_get_db_status_nonexistent_and_initialized(), test_init_db_and_idempotence(), test_session_scope_rolls_back_on_error(), test_sqlite_url_formats_path() (+1 more)

### Community 26 - "Community 26"
Cohesion: 0.22
Nodes (6): rich_console, The exit-code contract: a script parsing our status codes must never be…, test_keyboard_interrupt_exits_130(), test_only_transient_and_timeout_are_retryable(), test_unexpected_exception_is_not_swallowed(), typer

### Community 27 - "Community 27"
Cohesion: 0.33
Nodes (7): Config, _alembic_config(), Build an Alembic configuration targeting ``db_path``., Path, CI gate: assert alembic check reports no drift between ORM models and…, test_alembic_check_no_drift(), test_migrations_upgrade_and_downgrade()

### Community 28 - "Community 28"
Cohesion: 0.33
Nodes (6): json, main(), Path, Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys

### Community 29 - "Community 29"
Cohesion: 0.40
Nodes (6): ComplianceError, A generated image violates the YouTube thumbnail requirements., Machine mode contract: stdout carries command output, stderr carries the…, test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), boom(), root()

### Community 30 - "Community 30"
Cohesion: 0.40
Nodes (5): min, help, Option, Reclaim unused disk space, checkpoint the WAL, and delete orphaned asset files., vacuum()

### Community 31 - "Community 31"
Cohesion: 0.67
Nodes (3): _as_toml(), JsonValue, Render effective settings as TOML for display. ``tomli_w`` cannot serialise…

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 376 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `YtDlpSource` connect `Community 24` to `Community 5`, `Community 6`, `Community 14`, `Community 22`, `Community 23`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `root()` connect `Community 2` to `Community 16`, `Community 0`, `Community 11`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `UrlError` connect `Community 6` to `Community 7`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `SettingsError` (e.g. with `root()` and `set_()`) actually correct?**
  _`SettingsError` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `AssetStore` (e.g. with `AssetKind` and `AssetError`) actually correct?**
  _`AssetStore` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05359831376091539 - nodes in this community are weakly interconnected._