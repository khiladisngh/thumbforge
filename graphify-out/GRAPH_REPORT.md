# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1152 nodes · 2366 edges · 83 communities (61 shown, 22 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 233 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ec8dd2f9`
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
- Community 62
- Community 63
- Community 64
- Community 65
- Community 66
- Community 67
- Community 68
- Community 69
- Community 70
- Community 71
- Community 72
- Community 73
- Community 74
- Community 75
- Community 76
- Community 77
- Community 78
- Community 79
- Community 80
- Community 81
- Community 82

## God Nodes (most connected - your core abstractions)
1. `Repositories` - 30 edges
2. `emit()` - 26 edges
3. `SettingsError` - 24 edges
4. `StubSource` - 24 edges
5. `load_settings()` - 23 edges
6. `get_engine()` - 22 edges
7. `YtDlpSource` - 21 edges
8. `AssetStore` - 21 edges
9. `AssetKind` - 20 edges
10. `AppContext` - 20 edges

## Surprising Connections (you probably didn't know these)
- `repeating()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_cli_fetch.py → src/thumbforge/core/models.py
- `test_unique_constraint_template_name_version()` --uses--> `Template`  [INFERRED]
  tests/unit/test_storage_models.py → src/thumbforge/storage/models.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_channel_url_does_not_enumerate_videos()` --uses--> `FetchService`  [INFERRED]
  tests/unit/test_fetch_service.py → src/thumbforge/core/services/fetch.py
- `test_freshness_only_applies_to_playlists()` --uses--> `FetchService`  [INFERRED]
  tests/unit/test_fetch_service.py → src/thumbforge/core/services/fetch.py

## Import Cycles
- None detected.

## Communities (83 total, 22 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic_settings, Self, Return the settings, or re-raise the failure that prevented loading them.… (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (53): data_dir(), ChannelMeta, MonkeyPatch, Path, VideoMeta, `fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP…, An initialised database, since every command here needs the schema., The `PLAN.md` §5.3 shape: panel, `#`/`Part` table, then the stored counts. (+45 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (34): Collection, Session, ChannelRepository, PlaylistRepository, Channel, ChannelMeta, Playlist, PlaylistItem (+26 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (50): collections_abc, pytest, The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Repositories, Shared fixtures. Establishes ``tests/`` as the pytest root., _channel(), _playlist(), ChannelMeta (+42 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (35): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, asset_store() (+27 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (27): FakeSource, FakeStore, ChannelMeta, DateTime, VideoMeta, If the fake drifts from `MetadataSource`, these tests stop meaning anything., A single video can afford the channel request, which populates…, One playlist request plus one channel request, regardless of item count. (+19 more)

### Community 6 - "Community 6"
Cohesion: 0.14
Nodes (31): DeclarativeBase, Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations., RunKind, RunStatus, Storage layer for thumbforge (SQLite + SQLAlchemy 2.0 + Alembic)., Asset, Base (+23 more)

### Community 7 - "Community 7"
Cohesion: 0.14
Nodes (21): asyncio, contextlib, dataclasses, ``thumbforge fetch`` — pull YouTube metadata into the database (ROADMAP P2.3)., Wiring and shared views for the YouTube metadata commands (ROADMAP P2.3).…, `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, `YtDlpSource` — YouTube metadata via `yt-dlp`, no API key (ADR 0005, ROADMAP…, _iso() (+13 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (24): RawInfo, RetryCallState, _duration(), _log_retry(), _published_at(), ChannelMeta, datetime, PlaylistMeta (+16 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (24): Argument, metavar, rich_syntax, _as_toml(), _config_path(), init_(), path_(), command (+16 more)

### Community 10 - "Community 10"
Cohesion: 0.16
Nodes (24): BoundLogger, CaptureFixture, LogFormat, configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``., Configure structlog and the stdlib root logger. Safe to call more than once. (+16 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (23): re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 12 - "Community 12"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, Yield `exc` and its `cause` links; `ExtractorError` nests the real failure… (+16 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (21): parametrize, classify_url(), Resolve a YouTube URL, handle or bare id to its kind and identifier. A `watch`…, ResolvedUrl, ResolvedUrl, UrlKind, Which YouTube URLs and ids resolve to which kind (ADR 0005, ROADMAP P2.1)., `@` alone names no channel, so it must not resolve successfully. (+13 more)

### Community 14 - "Community 14"
Cohesion: 0.10
Nodes (22): datetime, Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)., `resolve()` returns both halves (ADR 0005); an empty id is never a valid result., A minimal valid video, so each test states only the field it is about., A fetched snapshot is a value; mutating one would desync it from `fetched_at`., `extra="forbid"` turns an unexpected yt-dlp field into a loud failure. yt-dlp's…, `fetched_at` is persisted as ISO-8601 UTC, so a naive datetime is ambiguous., Offsets are preserved as an instant, then stored in UTC. (+14 more)

### Community 15 - "Community 15"
Cohesion: 0.16
Nodes (20): min, P, R, init_(), path_(), command, Context, help (+12 more)

### Community 16 - "Community 16"
Cohesion: 0.14
Nodes (14): The ``Stored N channel, N playlist, N videos.`` line from ``PLAN.md`` §5.3., _summary(), FetchResult, FetchService, ResolvedUrl, Playlist rows written., Fetch YouTube metadata and persist it., Resolve `url`, fetch the thing it names, and store it. (+6 more)

### Community 17 - "Community 17"
Cohesion: 0.12
Nodes (20): tenacity, `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., A source wired to a fixture, plus the recorder that captured its calls., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get… (+12 more)

### Community 18 - "Community 18"
Cohesion: 0.14
Nodes (19): Engine, integration, Session, sessionmaker, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the…, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., _reclaim_orphans() (+11 more)

### Community 19 - "Community 19"
Cohesion: 0.18
Nodes (20): list_(), Argument, command, Context, handle_errors, help, Option, Reassign part numbers sequentially, optionally leaving some videos unnumbered.… (+12 more)

### Community 20 - "Community 20"
Cohesion: 0.14
Nodes (16): enum, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Origin of channel metadata., UrlKind, Channel, A YouTube channel that owns playlists and videos. (+8 more)

### Community 21 - "Community 21"
Cohesion: 0.11
Nodes (15): Extractor, build_source(), ChannelSource, MetadataSource, Select a metadata source. The Data API source is a Phase 8 extra, so asking for…, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, ResolvedUrl, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation). (+7 more)

### Community 22 - "Community 22"
Cohesion: 0.12
Nodes (14): Protocol, FetchStore, ChannelMeta, datetime, MetadataSource, PlaylistMeta, VideoMeta, Take the metadata source and persistence layer the CLI selected. (+6 more)

### Community 23 - "Community 23"
Cohesion: 0.18
Nodes (11): ChannelMeta, PlaylistMeta, A fetched YouTube channel., A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, A fetched YouTube playlist and its ordered items., Number of items fetched, for the `playlist.item_count` column., What a URL or bare identifier turned out to be (ADR 0005)., ResolvedUrl (+3 more)

### Community 24 - "Community 24"
Cohesion: 0.21
Nodes (16): Path, Unit tests for ``thumbforge db`` CLI commands (ADR 0004, Phase 1 spec)., test_db_init_creates_database_and_is_idempotent(), test_db_init_json_mode(), test_db_json_error_stream_contract(), test_db_path_command(), test_db_path_json_mode(), test_db_status_command() (+8 more)

### Community 25 - "Community 25"
Cohesion: 0.15
Nodes (15): _fixture(), Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Load one recorded yt-dlp info dict. (+7 more)

### Community 26 - "Community 26"
Cohesion: 0.15
Nodes (12): importlib_metadata, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set() (+4 more)

### Community 27 - "Community 27"
Cohesion: 0.15
Nodes (16): RenderableType, JsonPayload, Build the JSON payload and the Rich renderable from the **stored** rows.…, _view(), channel_payload(), item_payload(), item_rows(), Channel (+8 more)

### Community 28 - "Community 28"
Cohesion: 0.17
Nodes (15): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError, Error hierarchy and the exit codes it maps to. Every failure the user can… (+7 more)

### Community 29 - "Community 29"
Cohesion: 0.14
Nodes (12): Path, Return the hex SHA-256 of a file, read in chunks so large images stay off the…, sha256_file(), _fsync_dir(), Path, Session, sessionmaker, Return the absolute path on disk for ``asset``. (+4 more)

### Community 30 - "Community 30"
Cohesion: 0.13
Nodes (13): alembic_config, alembic_runtime_migration, alembic_script, Connection, ConnectionPoolEntry, sqlalchemy_pool, sqlite3, DbStatus (+5 more)

### Community 31 - "Community 31"
Cohesion: 0.18
Nodes (15): list_(), Argument, command, Context, handle_errors, help, Option, List stored videos, most recently fetched first. (+7 more)

### Community 32 - "Community 32"
Cohesion: 0.16
Nodes (12): os, pil, shutil, sqlalchemy_exc, sqlalchemy_orm, new_id(), Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits. (+4 more)

### Community 33 - "Community 33"
Cohesion: 0.21
Nodes (10): main(), Root Typer application: global flags, context construction, sub-app…, ``thumbforge playlist`` — list and inspect stored playlists (ROADMAP P2.3)., ``thumbforge video`` — list and inspect stored videos (ROADMAP P2.3)., lookup_key(), Reduce a user-supplied reference to something a repository can look up. `video…, thumbforge, thumbforge_cli (+2 more)

### Community 34 - "Community 34"
Cohesion: 0.20
Nodes (13): _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, Record `tests/fixtures/ytdlp/*.json` from live YouTube, and assert the S11…, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`., A full extract must carry the fields a flat entry cannot (S11). Also the only… (+5 more)

### Community 35 - "Community 35"
Cohesion: 0.18
Nodes (9): alembic, sqlalchemy, get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline() (+1 more)

### Community 36 - "Community 36"
Cohesion: 0.24
Nodes (13): Config, _alembic_config(), get_db_status(), init_db(), Path, Build an Alembic configuration targeting ``db_path``., Inspect migration revision and file metadata for ``db_path``., Ensure directory exists and upgrade DB to head. Returns: Tuple of… (+5 more)

### Community 37 - "Community 37"
Cohesion: 0.17
Nodes (12): callback, count, envvar, is_eager, Context, handle_errors, help, Option (+4 more)

### Community 38 - "Community 38"
Cohesion: 0.17
Nodes (8): hashlib, Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 39 - "Community 39"
Cohesion: 0.18
Nodes (9): rich_console, rich_panel, rich_table, panel(), The only module allowed to write to stdout. Every command produces one of two…, Build a titled Rich panel., The exit-code contract: a script parsing our status codes must never be…, test_only_transient_and_timeout_are_retryable() (+1 more)

### Community 40 - "Community 40"
Cohesion: 0.21
Nodes (11): AppContext, Per-invocation state built by the root callback and stored on ``ctx.obj``., ComplianceError, A generated image violates the YouTube thumbnail requirements., Machine mode contract: stdout carries command output, stderr carries the…, Ctrl-C during a batch must still leave machine mode with parseable output., test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), boom() (+3 more)

### Community 41 - "Community 41"
Cohesion: 0.21
Nodes (11): A supplied URL or identifier is not recognisable YouTube input., UrlError, _channel_handle(), classify_id(), _expect_kind(), UrlKind, Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1). Pure…, Classify a bare YouTube identifier by its shape. Order matters: a channel id… (+3 more)

### Community 42 - "Community 42"
Cohesion: 0.20
Nodes (12): A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs. (+4 more)

### Community 43 - "Community 43"
Cohesion: 0.27
Nodes (11): get_engine(), Format a SQLite connection URL for SQLAlchemy., Create a SQLAlchemy engine configured for thumbforge SQLite usage., sqlite_url(), Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_engine_pragmas_on_memory() (+3 more)

### Community 44 - "Community 44"
Cohesion: 0.29
Nodes (10): Console, emit(), JsonValue, Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.…, _json_context(), `emit` is the machine boundary: what it prints must always be parseable JSON., test_json_mode_output_round_trips(), test_non_finite_floats_are_rejected() (+2 more)

### Community 45 - "Community 45"
Cohesion: 0.22
Nodes (9): field_validator, pydantic, _Meta, datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Default for `fetched_at`: an aware UTC instant, never a naive local one., Shared configuration and provenance for every fetched snapshot., Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC. (+1 more)

### Community 46 - "Community 46"
Cohesion: 0.20
Nodes (10): logging_handlers, bind(), clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Bind context onto every subsequent log record in this task (run id, provider,…, Drop all bound context., structlog, structlog_stdlib (+2 more)

### Community 47 - "Community 47"
Cohesion: 0.22
Nodes (7): PartialBatchError, Exception, A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., TemplateError, ThumbforgeError

### Community 48 - "Community 48"
Cohesion: 0.36
Nodes (7): functools, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.…, _report()

### Community 49 - "Community 49"
Cohesion: 0.25
Nodes (8): fetch(), Argument, ChannelSource, Context, handle_errors, help, Option, Fetch a video, playlist or channel and store its metadata.

### Community 50 - "Community 50"
Cohesion: 0.32
Nodes (8): DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., Reclaim free space, truncate the WAL, and delete unreferenced asset files.…, vacuum_db(), parametrize, A non-positive window would let vacuum delete an in-flight write's files., test_vacuum_rejects_non_positive_grace(), test_vacuum_db_success_and_missing_error()

### Community 51 - "Community 51"
Cohesion: 0.25
Nodes (5): What persisting a playlist actually wrote. Returned instead of the ORM row…, StoredPlaylist, PlaylistMeta, Persist a playlist, its owning channel, its videos and its item order. Reports…, PlaylistMeta

### Community 52 - "Community 52"
Cohesion: 0.33
Nodes (6): json, main(), Path, Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys

### Community 53 - "Community 53"
Cohesion: 0.33
Nodes (6): pathlib, Path, Unit tests for Alembic migrations and drift detection (ADR 0004, Phase 1 spec)., CI gate: assert alembic check reports no drift between ORM models and…, test_alembic_check_no_drift(), test_migrations_upgrade_and_downgrade()

### Community 54 - "Community 54"
Cohesion: 0.40
Nodes (4): IntEnum, ExitCode, Process exit statuses. Values are a public contract., test_keyboard_interrupt_exits_130()

### Community 55 - "Community 55"
Cohesion: 0.40
Nodes (5): level_from_flags(), Resolve the console level from the global flags. ``--quiet`` wins over ``-v``…, parametrize, --quiet outranks -v: an explicit request for silence beats a scripted -v., test_flag_to_level_mapping()

### Community 56 - "Community 56"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 57 - "Community 57"
Cohesion: 0.67
Nodes (4): NotFoundError, A referenced entity does not exist., test_hint_and_code_reach_stderr(), boom()

### Community 58 - "Community 58"
Cohesion: 0.50
Nodes (3): PlaylistItemMeta, One video's place in a playlist., PlaylistMeta

### Community 59 - "Community 59"
Cohesion: 0.50
Nodes (3): parametrize, Every error in CASES exits with the code documented in PLAN.md 5.1., test_error_maps_to_documented_exit_code()

### Community 60 - "Community 60"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 543 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PlaylistRepository` connect `Community 2` to `Community 7`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `root()` connect `Community 37` to `Community 0`, `Community 33`, `Community 40`, `Community 10`, `Community 55`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `Repositories` connect `Community 3` to `Community 2`, `Community 7`, `Community 18`, `Community 51`, `Community 27`, `Community 31`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `Repositories` (e.g. with `_view()` and `open_repositories()`) actually correct?**
  _`Repositories` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `emit()` (e.g. with `fetch()` and `list_()`) actually correct?**
  _`emit()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `SettingsError` (e.g. with `set_()` and `AppContext`) actually correct?**
  _`SettingsError` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._