# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1177 nodes · 2410 edges · 87 communities (62 shown, 25 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 236 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `50a5d4dd`
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
- Community 83
- Community 84
- Community 85
- Community 86

## God Nodes (most connected - your core abstractions)
1. `Repositories` - 29 edges
2. `emit()` - 26 edges
3. `StubSource` - 24 edges
4. `SettingsError` - 24 edges
5. `load_settings()` - 23 edges
6. `get_engine()` - 22 edges
7. `AssetStore` - 21 edges
8. `AppContext` - 20 edges
9. `YtDlpSource` - 20 edges
10. `AssetKind` - 20 edges

## Surprising Connections (you probably didn't know these)
- `repeating()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_cli_fetch.py → src/thumbforge/core/models.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_aware_fetched_at_is_normalised_to_utc()` --uses--> `ChannelMeta`  [INFERRED]
  tests/unit/test_core_models.py → src/thumbforge/core/models.py
- `test_naive_fetched_at_is_rejected()` --uses--> `ChannelMeta`  [INFERRED]
  tests/unit/test_core_models.py → src/thumbforge/core/models.py
- `test_item_count_tracks_items()` --uses--> `PlaylistMeta`  [INFERRED]
  tests/unit/test_core_models.py → src/thumbforge/core/models.py

## Import Cycles
- None detected.

## Communities (87 total, 25 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (55): MonkeyPatch, data_dir(), ChannelMeta, fixture, Path, VideoMeta, `fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP…, An initialised database, since every command here needs the schema. (+47 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (42): importlib_metadata, json, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, Record `tests/fixtures/ytdlp/*.json` from live YouTube, and assert the S11… (+34 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (45): _channel(), _playlist(), ChannelMeta, PlaylistMeta, VideoMeta, Upsert semantics the rest of Phase 2 depends on (ROADMAP P2.3, PLAN.md §3)., `UNIQUE(playlist_id, position)` makes an in-place swap a constraint violation., A video dropped from a playlist keeps its row: its thumbnails are still real. (+37 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (35): functools, IntEnum, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.…, _report() (+27 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (38): DeclarativeBase, ChannelSource, Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations., Origin of channel metadata., RunKind, RunStatus, Storage layer for thumbforge (SQLite + SQLAlchemy 2.0 + Alembic). (+30 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (35): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, asset_store() (+27 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (30): Any, importlib_util, ModuleType, re, declarations(), main(), Path, Compare a committed graphify graph against a freshly extracted one. Only… (+22 more)

### Community 7 - "Community 7"
Cohesion: 0.15
Nodes (21): dataclasses, sqlalchemy_orm, main(), Root Typer application: global flags, context construction, sub-app…, ``thumbforge fetch`` — pull YouTube metadata into the database (ROADMAP P2.3)., ``thumbforge playlist`` — list and inspect stored playlists (ROADMAP P2.3)., ``thumbforge video`` — list and inspect stored videos (ROADMAP P2.3)., lookup_key() (+13 more)

### Community 8 - "Community 8"
Cohesion: 0.16
Nodes (26): BoundLogger, CaptureFixture, LogFormat, configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``., Configure structlog and the stdlib root logger. Safe to call more than once. (+18 more)

### Community 9 - "Community 9"
Cohesion: 0.09
Nodes (25): pydantic, PlaylistItemMeta, One video's place in a playlist., PlaylistMeta, Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)., `resolve()` returns both halves (ADR 0005); an empty id is never a valid result., A minimal valid video, so each test states only the field it is about., A fetched snapshot is a value; mutating one would desync it from `fetched_at`. (+17 more)

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (23): collections_abc, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 11 - "Community 11"
Cohesion: 0.10
Nodes (20): pil, shutil, sqlalchemy, sqlalchemy_exc, new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits. (+12 more)

### Community 12 - "Community 12"
Cohesion: 0.11
Nodes (22): `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, FakeSource, `FetchService` decisions: kind dispatch, the freshness rule, and what each…, If the fake drifts from `MetadataSource`, these tests stop meaning anything., A single video can afford the channel request, which populates…, One playlist request plus one channel request, regardless of item count., Channel-wide enumeration is a Phase 2 non-goal., Just past the window the network call must happen again. (+14 more)

### Community 13 - "Community 13"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, Yield `exc` and its `cause` links; `ExtractorError` nests the real failure… (+16 more)

### Community 14 - "Community 14"
Cohesion: 0.13
Nodes (22): Argument, metavar, rich_syntax, _as_toml(), _config_path(), init_(), path_(), command (+14 more)

### Community 15 - "Community 15"
Cohesion: 0.21
Nodes (22): default_config_path(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, parametrize, Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., Guards the conftest fixture itself: a regression there silently pollutes real… (+14 more)

### Community 16 - "Community 16"
Cohesion: 0.13
Nodes (20): BaseModel, model_validator, platformdirs, pydantic_settings, Self, AntigravitySettings, BatchSettings, ConfigSchema (+12 more)

### Community 17 - "Community 17"
Cohesion: 0.11
Nodes (19): ResolvedUrl, A supplied URL or identifier is not recognisable YouTube input., UrlError, _channel_handle(), classify_id(), classify_url(), _expect_kind(), UrlKind (+11 more)

### Community 18 - "Community 18"
Cohesion: 0.16
Nodes (22): list_(), Argument, command, Context, handle_errors, help, Option, Reassign part numbers sequentially, optionally leaving some videos unnumbered.… (+14 more)

### Community 19 - "Community 19"
Cohesion: 0.17
Nodes (19): P, R, init_(), path_(), command, Context, help, Option (+11 more)

### Community 20 - "Community 20"
Cohesion: 0.13
Nodes (17): parametrize, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1). Pure…, UrlKind, Which YouTube URLs and ids resolve to which kind (ADR 0005, ROADMAP P2.1)., `@` alone names no channel, so it must not resolve successfully., `urlparse` raises `ValueError` on these; the CLI only handles…, Every URL form thumbforge accepts, and the exact identifier it must extract. (+9 more)

### Community 21 - "Community 21"
Cohesion: 0.13
Nodes (19): `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., A source wired to a fixture, plus the recorder that captured its calls., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get…, `position` comes from enumeration order because `playlist_index` is absent… (+11 more)

### Community 22 - "Community 22"
Cohesion: 0.12
Nodes (14): Protocol, FetchStore, ChannelMeta, datetime, MetadataSource, PlaylistMeta, VideoMeta, Take the metadata source and persistence layer the CLI selected. (+6 more)

### Community 23 - "Community 23"
Cohesion: 0.16
Nodes (13): ChannelMeta, _Meta, PlaylistMeta, Shared configuration and provenance for every fetched snapshot., A fetched YouTube channel., A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, A fetched YouTube playlist and its ordered items., Number of items fetched, for the `playlist.item_count` column. (+5 more)

### Community 24 - "Community 24"
Cohesion: 0.17
Nodes (17): asyncio, contextlib, RawInfo, _duration(), _published_at(), datetime, `YtDlpSource` — YouTube metadata via `yt-dlp`, no API key (ADR 0005, ROADMAP…, Read a string field, treating a missing key and an explicit `None` alike. Both… (+9 more)

### Community 25 - "Community 25"
Cohesion: 0.15
Nodes (18): Engine, integration, Session, sessionmaker, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., session_factory(), session_scope() (+10 more)

### Community 26 - "Community 26"
Cohesion: 0.13
Nodes (18): JsonPayload, RenderableType, JsonPayload, Build the JSON payload and the Rich renderable from the **stored** rows.…, _view(), panel(), Build a titled Rich panel., channel_payload() (+10 more)

### Community 27 - "Community 27"
Cohesion: 0.14
Nodes (10): What persisting a playlist actually wrote. Returned instead of the ORM row…, StoredPlaylist, FakeStore, ChannelMeta, DateTime, PlaylistMeta, VideoMeta, `fetch` tells the user a re-fetch shrank the playlist. (+2 more)

### Community 28 - "Community 28"
Cohesion: 0.12
Nodes (17): callback, count, envvar, is_eager, Context, handle_errors, help, Option (+9 more)

### Community 29 - "Community 29"
Cohesion: 0.14
Nodes (14): logging_handlers, os, pathlib, pytest, bind(), clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Bind context onto every subsequent log record in this task (run id, provider,… (+6 more)

### Community 30 - "Community 30"
Cohesion: 0.17
Nodes (11): BaseSettings, Return the settings, or re-raise the failure that prevented loading them.…, _atomic_write(), default_data_dir(), default_state_dir(), Path, Effective configuration for one invocation: defaults, then file, then…, Replace ``path`` atomically: write a sibling temp file, fsync, then rename. A… (+3 more)

### Community 31 - "Community 31"
Cohesion: 0.19
Nodes (14): Console, rich_console, rich_panel, rich_table, emit(), JsonValue, The only module allowed to write to stdout. Every command produces one of two…, Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.… (+6 more)

### Community 32 - "Community 32"
Cohesion: 0.17
Nodes (16): min, list_(), Argument, command, Context, handle_errors, help, Option (+8 more)

### Community 33 - "Community 33"
Cohesion: 0.14
Nodes (12): RetryCallState, _log_retry(), ChannelMeta, PlaylistMeta, VideoMeta, Turn an unexpected yt-dlp info-dict *shape* into a `SourceError`. yt-dlp parses…, Full extract of one video, so `description` and `published_at` are populated., Flat extract of a playlist and its items, in playlist order. One network round… (+4 more)

### Community 34 - "Community 34"
Cohesion: 0.17
Nodes (15): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError, Error hierarchy and the exit codes it maps to. Every failure the user can… (+7 more)

### Community 35 - "Community 35"
Cohesion: 0.25
Nodes (15): get_engine(), init_db(), Ensure directory exists and upgrade DB to head. Returns: Tuple of…, Create a SQLAlchemy engine configured for thumbforge SQLite usage., Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_engine_pragmas_on_memory() (+7 more)

### Community 36 - "Community 36"
Cohesion: 0.15
Nodes (11): alembic, Config, _alembic_config(), Build an Alembic configuration targeting ``db_path``., Format a SQLite connection URL for SQLAlchemy., sqlite_url(), Path, Unit tests for Alembic migrations and drift detection (ADR 0004, Phase 1 spec). (+3 more)

### Community 37 - "Community 37"
Cohesion: 0.13
Nodes (13): alembic_config, alembic_runtime_migration, alembic_script, Connection, ConnectionPoolEntry, sqlalchemy_pool, sqlite3, DbStatus (+5 more)

### Community 38 - "Community 38"
Cohesion: 0.18
Nodes (14): DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., get_db_status(), Path, Inspect migration revision and file metadata for ``db_path``., Run Alembic upgrade to ``revision`` on ``db_path``., Reclaim free space, truncate the WAL, and delete unreferenced asset files.…, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the… (+6 more)

### Community 39 - "Community 39"
Cohesion: 0.18
Nodes (13): _fixture(), Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Load one recorded yt-dlp info dict., Extractor stub that returns a fixture and remembers how it was called. (+5 more)

### Community 40 - "Community 40"
Cohesion: 0.14
Nodes (14): ChannelSource, MetadataSource, fetch(), Argument, ChannelSource, Context, handle_errors, help (+6 more)

### Community 41 - "Community 41"
Cohesion: 0.14
Nodes (11): Extractor, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch. (+3 more)

### Community 42 - "Community 42"
Cohesion: 0.20
Nodes (14): Configuration is missing, malformed, or contains something it must not., SettingsError, _format_validation_error(), _parse_scalar(), Apply several dotted keys to the TOML file, validating the result once. All…, Parse a CLI value using TOML scalar rules, falling back to a bare string.…, _read_toml(), _reject_secrets() (+6 more)

### Community 43 - "Community 43"
Cohesion: 0.19
Nodes (9): Video, VideoMeta, Look a video up by ULID or YouTube id, raising `NotFoundError` if absent. Both…, Insert or refresh a video, preserving its ULID. `channel_row_id` is supplied…, Videos, newest fetch first, optionally restricted to one channel., Persist one video and, when known, its channel. A single-video fetch can afford…, Video rows, keyed by YouTube video id., Return the row for a YouTube video id, or `None`. (+1 more)

### Community 44 - "Community 44"
Cohesion: 0.23
Nodes (8): FetchService, ResolvedUrl, Fetch YouTube metadata and persist it., Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order., A channel on its own; enumerating its videos is a Phase 2 non-goal., Whether a stored playlist is recent enough to skip the network.

### Community 45 - "Community 45"
Cohesion: 0.23
Nodes (8): PlaylistRepository, Playlist, Playlist rows and their ordered items., Return the row for a YouTube playlist id, or `None`., Look a playlist up by ULID or YouTube id, raising `NotFoundError` if absent., Insert or refresh a playlist. `channel_row_id` is required: the column is NOT…, Rewrite a playlist's items to exactly `video_ids`, in order. Rows are deleted…, Playlists, newest fetch first, optionally restricted to one channel.

### Community 46 - "Community 46"
Cohesion: 0.17
Nodes (8): hashlib, Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 47 - "Community 47"
Cohesion: 0.20
Nodes (12): A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs. (+4 more)

### Community 48 - "Community 48"
Cohesion: 0.21
Nodes (8): ChannelRepository, Channel, ChannelMeta, Persist a channel on its own (a channel URL was fetched)., Channel rows, keyed by YouTube channel id., Return the row for a YouTube channel id, or `None`., Insert or refresh a channel, preserving its ULID., Every channel, newest fetch first.

### Community 49 - "Community 49"
Cohesion: 0.25
Nodes (6): Collection, PlaylistItem, A playlist's items in playlist order., Reassign `part_number` sequentially from `start` in playlist order. Videos…, One item's `part_number` before and after a `playlist renumber`. Captured per…, Renumbering

### Community 50 - "Community 50"
Cohesion: 0.32
Nodes (7): get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline(), run_migrations_online()

### Community 51 - "Community 51"
Cohesion: 0.38
Nodes (3): Session, Build the three repositories over one session, so they share a transaction., Bind to the caller's session; the service owns the transaction.

### Community 52 - "Community 52"
Cohesion: 0.33
Nodes (5): enum, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., UrlKind, StrEnum

### Community 53 - "Community 53"
Cohesion: 0.33
Nodes (5): field_validator, datetime, Default for `fetched_at`: an aware UTC instant, never a naive local one., Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC., _utcnow()

### Community 54 - "Community 54"
Cohesion: 0.33
Nodes (4): FetchResult, Playlist rows written., What was fetched, for rendering and for the `--json` contract. Counts are of…, Channel rows written.

### Community 55 - "Community 55"
Cohesion: 0.40
Nodes (4): datetime, _iso(), When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, Render an aware datetime as the ISO-8601 UTC string the schema stores.

### Community 56 - "Community 56"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 57 - "Community 57"
Cohesion: 0.67
Nodes (4): NotFoundError, A referenced entity does not exist., test_hint_and_code_reach_stderr(), boom()

### Community 58 - "Community 58"
Cohesion: 0.50
Nodes (3): Session, sessionmaker, Bind the store to a data directory and the session factory used for asset rows.

### Community 59 - "Community 59"
Cohesion: 0.50
Nodes (3): PlaylistMeta, Persist a playlist, its owning channel, its videos and its item order. Reports…, StoredPlaylist

### Community 60 - "Community 60"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

### Community 61 - "Community 61"
Cohesion: 0.67
Nodes (3): MonkeyPatch, A generated config must contain defaults, not whatever the current shell…, test_init_defaults_ignore_the_environment()

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 557 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Repositories` connect `Community 7` to `Community 32`, `Community 2`, `Community 43`, `Community 48`, `Community 51`, `Community 55`, `Community 25`, `Community 26`, `Community 59`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `repos()` connect `Community 25` to `Community 40`, `Community 2`, `Community 35`, `Community 7`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `PlaylistRepository` connect `Community 45` to `Community 49`, `Community 51`, `Community 7`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `Repositories` (e.g. with `_view()` and `open_repositories()`) actually correct?**
  _`Repositories` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `emit()` (e.g. with `fetch()` and `list_()`) actually correct?**
  _`emit()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05727644652250146 - nodes in this community are weakly interconnected._