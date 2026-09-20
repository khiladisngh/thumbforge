# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 671 nodes · 1447 edges · 37 communities (35 shown, 2 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 140 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `087a07b5`
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

## God Nodes (most connected - your core abstractions)
1. `SettingsError` - 25 edges
2. `load_settings()` - 24 edges
3. `AssetStore` - 21 edges
4. `AppContext` - 21 edges
5. `AssetKind` - 20 edges
6. `get_engine()` - 20 edges
7. `handle_errors()` - 20 edges
8. `emit()` - 20 edges
9. `ThumbforgeError` - 19 edges
10. `root()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `test_insert_all_nine_models_and_verify_relations()` --uses--> `AssetKind`  [INFERRED]
  tests/unit/test_storage_models.py → src/thumbforge/core/enums.py
- `test_on_delete_restrict_on_reference_asset()` --uses--> `AssetKind`  [INFERRED]
  tests/unit/test_storage_models.py → src/thumbforge/core/enums.py
- `test_sqlite_database_in_container()` --uses--> `ChannelSource`  [INFERRED]
  tests/integration/test_db_container.py → src/thumbforge/core/enums.py
- `test_session_scope_commits_on_success()` --uses--> `ChannelSource`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/core/enums.py
- `test_session_scope_rolls_back_on_error()` --uses--> `ChannelSource`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/core/enums.py

## Import Cycles
- None detected.

## Communities (37 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (58): io, pil, shutil, sqlalchemy_exc, sqlalchemy_orm, AssetKind, Functional role of a stored image asset., AssetError (+50 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (49): DeclarativeBase, E, enum, sqlalchemy, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run. (+41 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (49): BoundLogger, callback, CaptureFixture, count, envvar, is_eager, LogFormat, logging_handlers (+41 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (31): Exception, NotFoundError, PartialBatchError, ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError (+23 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (24): collections_abc, re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure. (+16 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (22): BaseModel, model_validator, platformdirs, pydantic_settings, Self, AntigravitySettings, BatchSettings, ConfigSchema (+14 more)

### Community 6 - "Community 6"
Cohesion: 0.13
Nodes (22): Argument, metavar, rich_syntax, _as_toml(), _config_path(), init_(), path_(), command (+14 more)

### Community 7 - "Community 7"
Cohesion: 0.13
Nodes (23): min, P, R, RenderableType, init_(), path_(), command, Context (+15 more)

### Community 8 - "Community 8"
Cohesion: 0.21
Nodes (22): default_config_path(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, parametrize, Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., Guards the conftest fixture itself: a regression there silently pollutes real… (+14 more)

### Community 9 - "Community 9"
Cohesion: 0.13
Nodes (20): datetime, pydantic, PlaylistItemMeta, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Default for `fetched_at`: an aware UTC instant, never a naive local one., One video's place in a playlist., _utcnow(), Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005). (+12 more)

### Community 10 - "Community 10"
Cohesion: 0.13
Nodes (16): functools, IntEnum, rich_console, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.… (+8 more)

### Community 11 - "Community 11"
Cohesion: 0.15
Nodes (18): Engine, integration, Session, sessionmaker, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the…, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., _reclaim_orphans() (+10 more)

### Community 12 - "Community 12"
Cohesion: 0.14
Nodes (17): parametrize, Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1). Pure…, UrlKind, Which YouTube URLs and ids resolve to which kind (ADR 0005, ROADMAP P2.1)., `@` alone names no channel, so it must not resolve successfully., `urlparse` raises `ValueError` on these; the CLI only handles…, Every URL form thumbforge accepts, and the exact identifier it must extract., Bad input must be a usage error (exit 2), not a source failure or a crash. (+9 more)

### Community 13 - "Community 13"
Cohesion: 0.14
Nodes (16): alembic, alembic_config, alembic_runtime_migration, alembic_script, Config, contextlib, sqlalchemy_pool, sqlite3 (+8 more)

### Community 14 - "Community 14"
Cohesion: 0.17
Nodes (16): Any, Configuration is missing, malformed, or contains something it must not., SettingsError, _deep_merge(), _format_validation_error(), Build settings where the environment outranks the TOML file. File values cannot…, Merge ``override`` into ``base``, recursing into nested tables., Apply several dotted keys to the TOML file, validating the result once. All… (+8 more)

### Community 15 - "Community 15"
Cohesion: 0.21
Nodes (16): ``thumbforge db`` — database lifecycle and migration management (ADR 0004)., DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., get_db_status(), init_db(), Path, Inspect migration revision and file metadata for ``db_path``., Ensure directory exists and upgrade DB to head. Returns: Tuple of… (+8 more)

### Community 16 - "Community 16"
Cohesion: 0.17
Nodes (17): A supplied URL or identifier is not recognisable YouTube input., UrlError, What a URL or bare identifier turned out to be (ADR 0005)., ResolvedUrl, _channel_handle(), classify_id(), classify_url(), _expect_kind() (+9 more)

### Community 17 - "Community 17"
Cohesion: 0.21
Nodes (16): Path, Unit tests for ``thumbforge db`` CLI commands (ADR 0004, Phase 1 spec)., test_db_init_creates_database_and_is_idempotent(), test_db_init_json_mode(), test_db_json_error_stream_contract(), test_db_path_command(), test_db_path_json_mode(), test_db_status_command() (+8 more)

### Community 18 - "Community 18"
Cohesion: 0.17
Nodes (11): BaseSettings, Return the settings, or re-raise the failure that prevented loading them.…, _atomic_write(), default_data_dir(), default_state_dir(), Path, Effective configuration for one invocation: defaults, then file, then…, Replace ``path`` atomically: write a sibling temp file, fsync, then rename. A… (+3 more)

### Community 19 - "Community 19"
Cohesion: 0.17
Nodes (15): Connection, ConnectionPoolEntry, get_engine(), Format a SQLite connection URL for SQLAlchemy., Apply PRAGMA statements required by ADR 0004 on every SQLite connection., Create a SQLAlchemy engine configured for thumbforge SQLite usage., _set_sqlite_pragmas(), sqlite_url() (+7 more)

### Community 20 - "Community 20"
Cohesion: 0.16
Nodes (10): Protocol, PlaylistMeta, A fetched YouTube playlist and its ordered items., Number of items fetched, for the `playlist.item_count` column., MetadataSource, The `MetadataSource` Protocol every metadata backend implements (ADR 0005). A…, Fetch YouTube channel, playlist and video metadata., Classify a URL or bare identifier into its kind and YouTube id. (+2 more)

### Community 21 - "Community 21"
Cohesion: 0.15
Nodes (13): rich_panel, rich_table, get_app_context(), kv(), panel(), Context, The only module allowed to write to stdout. Every command produces one of two…, Extract and validate the AppContext from a Typer execution context. (+5 more)

### Community 22 - "Community 22"
Cohesion: 0.15
Nodes (11): field_validator, ChannelMeta, _Meta, Shared configuration and provenance for every fetched snapshot., Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC., A fetched YouTube channel., Fetch a channel's metadata., `fetched_at` is persisted as ISO-8601 UTC, so a naive datetime is ambiguous. (+3 more)

### Community 23 - "Community 23"
Cohesion: 0.18
Nodes (8): os, pathlib, pytest, structlog, testcontainers_core_container, Shared fixtures. Establishes ``tests/`` as the pytest root., Integration tests using Testcontainers for database verification (ADR 0004)., typing

### Community 24 - "Community 24"
Cohesion: 0.19
Nodes (10): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+2 more)

### Community 25 - "Community 25"
Cohesion: 0.17
Nodes (8): hashlib, Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 26 - "Community 26"
Cohesion: 0.21
Nodes (11): AppContext, Per-invocation state built by the root callback and stored on ``ctx.obj``., ComplianceError, A generated image violates the YouTube thumbnail requirements., Machine mode contract: stdout carries command output, stderr carries the…, Ctrl-C during a batch must still leave machine mode with parseable output., test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), boom() (+3 more)

### Community 27 - "Community 27"
Cohesion: 0.22
Nodes (6): dataclasses, importlib_metadata, main(), Root Typer application: global flags, context construction, sub-app…, Typer command surface. Commands are thin; behaviour lives in…, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…

### Community 28 - "Community 28"
Cohesion: 0.33
Nodes (8): Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_engine_pragmas_on_memory(), test_get_db_status_nonexistent_and_initialized(), test_init_db_and_idempotence(), test_sqlite_url_formats_path(), test_upgrade_db_on_fresh_file()

### Community 29 - "Community 29"
Cohesion: 0.25
Nodes (7): A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, VideoMeta, Fetch one video's metadata., `extra="forbid"` turns an unexpected yt-dlp field into a loud failure. yt-dlp's…, `duration_s` is a length; a negative value would corrupt part numbering…, test_negative_duration_is_rejected(), test_unknown_upstream_field_is_rejected()

### Community 30 - "Community 30"
Cohesion: 0.43
Nodes (6): Console, _json_context(), `emit` is the machine boundary: what it prints must always be parseable JSON., test_json_mode_output_round_trips(), test_non_finite_floats_are_rejected(), test_non_json_payload_raises_instead_of_being_stringified()

### Community 31 - "Community 31"
Cohesion: 0.33
Nodes (6): json, main(), Path, Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys

### Community 32 - "Community 32"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 33 - "Community 33"
Cohesion: 0.50
Nodes (3): DbStatus, Whether the database is fully migrated to the latest revision., Migration status and storage health metadata.

### Community 34 - "Community 34"
Cohesion: 0.67
Nodes (3): MonkeyPatch, A generated config must contain defaults, not whatever the current shell…, test_init_defaults_ignore_the_environment()

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 304 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UrlError` connect `Community 16` to `Community 3`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Why does `SettingsError` connect `Community 14` to `Community 2`, `Community 3`, `Community 5`, `Community 6`, `Community 8`, `Community 18`, `Community 21`, `Community 26`, `Community 27`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `root()` connect `Community 2` to `Community 7`, `Community 8`, `Community 14`, `Community 18`, `Community 26`, `Community 27`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `SettingsError` (e.g. with `root()` and `set_()`) actually correct?**
  _`SettingsError` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `AssetStore` (e.g. with `AssetKind` and `AssetError`) actually correct?**
  _`AssetStore` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `AppContext` (e.g. with `root()` and `_config_path()`) actually correct?**
  _`AppContext` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._