# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1282 nodes · 2573 edges · 100 communities (74 shown, 26 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 223 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ab90a683`
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
- Community 87
- Community 88
- Community 89
- Community 90
- Community 91
- Community 92
- Community 93
- Community 94
- Community 95
- Community 96
- Community 97
- Community 98
- Community 99

## God Nodes (most connected - your core abstractions)
1. `emit()` - 29 edges
2. `Repositories` - 25 edges
3. `StubSource` - 24 edges
4. `load_settings()` - 24 edges
5. `get_engine()` - 22 edges
6. `AssetStore` - 21 edges
7. `AssetKind` - 20 edges
8. `YtDlpSource` - 20 edges
9. `ThumbforgeError` - 19 edges
10. `AppContext` - 19 edges

## Surprising Connections (you probably didn't know these)
- `repeating()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_cli_fetch.py → src/thumbforge/core/models.py
- `test_sqlite_database_in_container()` --uses--> `ChannelSource`  [INFERRED]
  tests/integration/test_db_container.py → src/thumbforge/core/enums.py
- `test_session_scope_commits_on_success()` --uses--> `ChannelSource`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/core/enums.py
- `test_session_scope_rolls_back_on_error()` --uses--> `ChannelSource`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/core/enums.py
- `test_vacuum_db_success_and_missing_error()` --uses--> `ChannelSource`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/core/enums.py

## Import Cycles
- None detected.

## Communities (100 total, 26 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (54): MonkeyPatch, data_dir(), ChannelMeta, fixture, Path, VideoMeta, `fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP…, An initialised database, since every command here needs the schema. (+46 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (44): DeclarativeBase, enum, sqlalchemy, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations. (+36 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (47): The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Repositories, _channel(), _playlist(), ChannelMeta, PlaylistMeta, VideoMeta, Upsert semantics the rest of Phase 2 depends on (ROADMAP P2.3, PLAN.md §3). (+39 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (35): functools, IntEnum, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.…, _report() (+27 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (35): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, asset_store() (+27 more)

### Community 5 - "Community 5"
Cohesion: 0.16
Nodes (26): BoundLogger, CaptureFixture, LogFormat, configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``., Configure structlog and the stdlib root logger. Safe to call more than once. (+18 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (22): os, pathlib, pil, shutil, sqlalchemy_exc, sqlalchemy_orm, new_id(), Path (+14 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (24): Argument, importlib_metadata, metavar, rich_syntax, _as_toml(), _config_path(), init_(), path_() (+16 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (21): BaseSettings, Return the settings, or re-raise the failure that prevented loading them.…, Configuration is missing, malformed, or contains something it must not., SettingsError, _atomic_write(), default_state_dir(), _format_validation_error(), _parse_scalar() (+13 more)

### Community 9 - "Community 9"
Cohesion: 0.10
Nodes (24): model_validator, platformdirs, pydantic_settings, Self, AntigravitySettings, BatchSettings, ConfigSchema, default_config_toml() (+16 more)

### Community 10 - "Community 10"
Cohesion: 0.18
Nodes (25): default_config_path(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., Spike S5 superseded decision D4: the dangerous flag is not opted into by…, Write a config file and return its path, so tests read as one expression. (+17 more)

### Community 11 - "Community 11"
Cohesion: 0.11
Nodes (22): _Entry, Registry behaviour: discovery, duplicate keys, and broken plugins (ADR 0010,…, A plugin needs only an entry point: the registry never imports it by name., Providers should not each have to handle `None`., `provider list` output must not reorder between runs., Same rule when neither side is a builtin., A skipped plugin looks identical to one that was never installed. That is the…, An entry point naming a module or constant cannot be instantiated. (+14 more)

### Community 12 - "Community 12"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, Yield `exc` and its `cause` links; `ExtractorError` nests the real failure… (+16 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (17): Collection, NotFoundError, A referenced entity does not exist., PlaylistRepository, Playlist, PlaylistItem, PlaylistMeta, Playlist rows and their ordered items. (+9 more)

### Community 14 - "Community 14"
Cohesion: 0.11
Nodes (22): pydantic, datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Default for `fetched_at`: an aware UTC instant, never a naive local one., _utcnow(), Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)., `resolve()` returns both halves (ADR 0005); an empty id is never a valid result., A minimal valid video, so each test states only the field it is about. (+14 more)

### Community 15 - "Community 15"
Cohesion: 0.11
Nodes (21): FakeSource, FakeStore, DateTime, If the fake drifts from `MetadataSource`, these tests stop meaning anything., A single video can afford the channel request, which populates…, One playlist request plus one channel request, regardless of item count., Channel-wide enumeration is a Phase 2 non-goal., Spec behaviour 2: a playlist fetched inside the window is not re-fetched. (+13 more)

### Community 16 - "Community 16"
Cohesion: 0.13
Nodes (17): decimal, Check, Cost, HealthReport, ProviderCapabilities, BaseModel, The `ImageProvider` Protocol and the values that cross it (ADR 0010, ROADMAP…, What a provider can actually do, so callers degrade instead of guessing. (+9 more)

### Community 17 - "Community 17"
Cohesion: 0.11
Nodes (19): ResolvedUrl, A supplied URL or identifier is not recognisable YouTube input., UrlError, _channel_handle(), classify_id(), classify_url(), _expect_kind(), UrlKind (+11 more)

### Community 18 - "Community 18"
Cohesion: 0.14
Nodes (19): Channel, MetadataSource, PlaylistItem, ``thumbforge fetch`` — pull YouTube metadata into the database (ROADMAP P2.3)., build_source(), channel_payload(), item_payload(), item_rows() (+11 more)

### Community 19 - "Community 19"
Cohesion: 0.16
Nodes (20): min, P, R, init_(), path_(), command, Context, help (+12 more)

### Community 20 - "Community 20"
Cohesion: 0.17
Nodes (19): Any, importlib_util, ModuleType, _declaration(), _graph(), _module(), Path, The drift check's node filter (issue #26). This is a CI gate, so a silently… (+11 more)

### Community 21 - "Community 21"
Cohesion: 0.17
Nodes (20): Playlist, list_(), Argument, command, Context, handle_errors, help, Option (+12 more)

### Community 22 - "Community 22"
Cohesion: 0.13
Nodes (19): `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., A source wired to a fixture, plus the recorder that captured its calls., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get…, `position` comes from enumeration order because `playlist_index` is absent… (+11 more)

### Community 23 - "Community 23"
Cohesion: 0.12
Nodes (17): logging_handlers, Return a copy of ``value`` with every secret-keyed entry replaced. A copy,…, redact(), bind(), clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Bind context onto every subsequent log record in this task (run id, provider,…, Drop all bound context. (+9 more)

### Community 24 - "Community 24"
Cohesion: 0.14
Nodes (17): parametrize, Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1). Pure…, UrlKind, Which YouTube URLs and ids resolve to which kind (ADR 0005, ROADMAP P2.1)., `@` alone names no channel, so it must not resolve successfully., `urlparse` raises `ValueError` on these; the CLI only handles…, Every URL form thumbforge accepts, and the exact identifier it must extract., Bad input must be a usage error (exit 2), not a source failure or a crash. (+9 more)

### Community 25 - "Community 25"
Cohesion: 0.17
Nodes (17): asyncio, contextlib, RawInfo, _duration(), _published_at(), datetime, `YtDlpSource` — YouTube metadata via `yt-dlp`, no API key (ADR 0005, ROADMAP…, Read a string field, treating a missing key and an explicit `None` alike. Both… (+9 more)

### Community 26 - "Community 26"
Cohesion: 0.15
Nodes (18): Engine, integration, Session, sessionmaker, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., session_factory(), session_scope() (+10 more)

### Community 27 - "Community 27"
Cohesion: 0.12
Nodes (18): FetchResult, fetch(), Argument, ChannelSource, Context, handle_errors, help, JsonPayload (+10 more)

### Community 28 - "Community 28"
Cohesion: 0.15
Nodes (15): alembic, alembic_config, alembic_runtime_migration, alembic_script, Config, sqlalchemy_pool, sqlite3, _alembic_config() (+7 more)

### Community 29 - "Community 29"
Cohesion: 0.20
Nodes (13): rich_console, rich_panel, rich_table, ``thumbforge playlist`` — list and inspect stored playlists (ROADMAP P2.3)., kv(), The only module allowed to write to stdout. Every command produces one of two…, Build a Rich table. Rendering is the caller's job via :func:`emit`., Build a two-column key/value table, the default shape for ``show``-style… (+5 more)

### Community 30 - "Community 30"
Cohesion: 0.21
Nodes (16): Path, Unit tests for ``thumbforge db`` CLI commands (ADR 0004, Phase 1 spec)., test_db_init_creates_database_and_is_idempotent(), test_db_init_json_mode(), test_db_json_error_stream_contract(), test_db_path_command(), test_db_path_json_mode(), test_db_status_command() (+8 more)

### Community 31 - "Community 31"
Cohesion: 0.14
Nodes (12): RetryCallState, _log_retry(), ChannelMeta, PlaylistMeta, VideoMeta, Turn an unexpected yt-dlp info-dict *shape* into a `SourceError`. yt-dlp parses…, Full extract of one video, so `description` and `published_at` are populated., Flat extract of a playlist and its items, in playlist order. One network round… (+4 more)

### Community 32 - "Community 32"
Cohesion: 0.17
Nodes (16): list_(), Argument, command, Context, handle_errors, help, Option, List stored videos, most recently fetched first. (+8 more)

### Community 33 - "Community 33"
Cohesion: 0.17
Nodes (15): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError, Error hierarchy and the exit codes it maps to. Every failure the user can… (+7 more)

### Community 34 - "Community 34"
Cohesion: 0.19
Nodes (14): find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., _words(), parametrize (+6 more)

### Community 35 - "Community 35"
Cohesion: 0.18
Nodes (14): json, _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, Record `tests/fixtures/ytdlp/*.json` from live YouTube, and assert the S11…, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`. (+6 more)

### Community 36 - "Community 36"
Cohesion: 0.15
Nodes (11): Protocol, FetchStore, ChannelMeta, datetime, PlaylistMeta, VideoMeta, The persistence surface a fetch needs, satisfied by `storage.Repositories`., Persist one video, and its channel when the caller fetched one. (+3 more)

### Community 37 - "Community 37"
Cohesion: 0.18
Nodes (14): DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., get_db_status(), Path, Inspect migration revision and file metadata for ``db_path``., Run Alembic upgrade to ``revision`` on ``db_path``., Reclaim free space, truncate the WAL, and delete unreferenced asset files.…, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the… (+6 more)

### Community 38 - "Community 38"
Cohesion: 0.18
Nodes (9): FetchResult, ResolvedUrl, Playlist rows written., Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order., A channel on its own; enumerating its videos is a Phase 2 non-goal., What was fetched, for rendering and for the `--json` contract. Counts are of… (+1 more)

### Community 39 - "Community 39"
Cohesion: 0.16
Nodes (10): ChannelRepository, Channel, ChannelMeta, Persist a playlist, its owning channel, its videos and its item order. Reports…, Persist a channel on its own (a channel URL was fetched)., Channel rows, keyed by YouTube channel id., Return the row for a YouTube channel id, or `None`., Insert or refresh a channel, preserving its ULID. (+2 more)

### Community 40 - "Community 40"
Cohesion: 0.18
Nodes (13): _fixture(), Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Load one recorded yt-dlp info dict., Extractor stub that returns a fixture and remembers how it was called. (+5 more)

### Community 41 - "Community 41"
Cohesion: 0.14
Nodes (11): Extractor, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch. (+3 more)

### Community 42 - "Community 42"
Cohesion: 0.21
Nodes (9): PlaylistMeta, A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, A fetched YouTube playlist and its ordered items., Number of items fetched, for the `playlist.item_count` column., What a URL or bare identifier turned out to be (ADR 0005)., ResolvedUrl, VideoMeta, MetadataSource (+1 more)

### Community 43 - "Community 43"
Cohesion: 0.19
Nodes (9): Video, VideoMeta, Look a video up by ULID or YouTube id, raising `NotFoundError` if absent. Both…, Insert or refresh a video, preserving its ULID. `channel_row_id` is supplied…, Videos, newest fetch first, optionally restricted to one channel., Persist one video and, when known, its channel. A single-video fetch can afford…, Video rows, keyed by YouTube video id., Return the row for a YouTube video id, or `None`. (+1 more)

### Community 44 - "Community 44"
Cohesion: 0.22
Nodes (12): get_engine(), Format a SQLite connection URL for SQLAlchemy., Create a SQLAlchemy engine configured for thumbforge SQLite usage., sqlite_url(), get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output. (+4 more)

### Community 45 - "Community 45"
Cohesion: 0.29
Nodes (12): init_db(), Ensure directory exists and upgrade DB to head. Returns: Tuple of…, Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_get_db_status_nonexistent_and_initialized(), test_init_db_and_idempotence(), test_session_scope_commits_on_success() (+4 more)

### Community 46 - "Community 46"
Cohesion: 0.19
Nodes (10): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+2 more)

### Community 47 - "Community 47"
Cohesion: 0.18
Nodes (10): collections_abc, datetime, _iso(), Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).…, When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, One item's `part_number` before and after a `playlist renumber`. Captured per…, Render an aware datetime as the ISO-8601 UTC string the schema stores., Renumbering (+2 more)

### Community 48 - "Community 48"
Cohesion: 0.26
Nodes (11): Console, emit(), JsonValue, RenderableType, Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.…, _json_context(), `emit` is the machine boundary: what it prints must always be parseable JSON., test_json_mode_output_round_trips() (+3 more)

### Community 49 - "Community 49"
Cohesion: 0.17
Nodes (8): hashlib, Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 50 - "Community 50"
Cohesion: 0.23
Nodes (10): ProviderFactory, Image providers: concrete `core.providers.ImageProvider` implementations and…, _discover(), get(), keys(), JsonValue, Provider lookup by key, merging builtins with installed plugins (ADR 0010,…, Merge builtins with installed entry points, refusing any duplicate key. A… (+2 more)

### Community 51 - "Community 51"
Cohesion: 0.20
Nodes (12): A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs. (+4 more)

### Community 52 - "Community 52"
Cohesion: 0.21
Nodes (7): `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, `FetchService` decisions: kind dispatch, the freshness rule, and what each…, `playlist.channel_id` is NOT NULL, so there is no row to write without it.…, test_playlist_without_an_owner_is_a_source_error(), thumbforge_core_models, thumbforge_core_sources, typing

### Community 53 - "Community 53"
Cohesion: 0.18
Nodes (11): callback, count, envvar, is_eager, Context, handle_errors, help, Option (+3 more)

### Community 54 - "Community 54"
Cohesion: 0.18
Nodes (5): What persisting a playlist actually wrote. Returned instead of the ORM row…, StoredPlaylist, ChannelMeta, PlaylistMeta, VideoMeta

### Community 55 - "Community 55"
Cohesion: 0.20
Nodes (8): BaseModel, field_validator, _Meta, PlaylistItemMeta, Shared configuration and provenance for every fetched snapshot., Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC., One video's place in a playlist., PlaylistMeta

### Community 56 - "Community 56"
Cohesion: 0.22
Nodes (8): GenerationRequest, GenerationResult, Path, One image to generate. Providers ignore what their capabilities disclaim., A produced image and the provenance needed to reproduce or audit it.…, Produce one image, or raise a `ProviderError` subclass. `workdir` is a caller-…, Path, Return a result pointing at a path inside `workdir`.

### Community 57 - "Community 57"
Cohesion: 0.20
Nodes (8): FetchService, MetadataSource, Fetch YouTube metadata and persist it., Take the metadata source and persistence layer the CLI selected., Whether a stored playlist is recent enough to skip the network., Just past the window the network call must happen again., test_stale_playlist_is_refetched(), timedelta

### Community 58 - "Community 58"
Cohesion: 0.25
Nodes (7): dataclasses, main(), Root Typer application: global flags, context construction, sub-app…, _version_callback(), thumbforge, thumbforge_cli, thumbforge_cli_render

### Community 59 - "Community 59"
Cohesion: 0.25
Nodes (8): re, declarations(), main(), Path, Compare a committed graphify graph against a freshly extracted one. Only…, Ids of the nodes graphify parsed out of a file in this repository., Report whether the committed graph still describes the current declarations., sys

### Community 60 - "Community 60"
Cohesion: 0.25
Nodes (6): ImageProvider, Generate one image per call. Implementations live in `providers/`., What this provider supports; callers check before sending a request., Every check this provider can run, with actionable detail on each failure., If the stub drifts from `ImageProvider`, every test here stops meaning anything., test_stub_satisfies_the_provider_protocol()

### Community 61 - "Community 61"
Cohesion: 0.29
Nodes (6): fixture, entries(), MonkeyPatch, Shadowing a provider would make `--provider x` mean different things per…, Replace the installed entry-point group with a list the test controls., test_duplicate_key_is_refused()

### Community 62 - "Community 62"
Cohesion: 0.38
Nodes (3): Session, Build the three repositories over one session, so they share a transaction., Bind to the caller's session; the service owns the transaction.

### Community 63 - "Community 63"
Cohesion: 0.29
Nodes (6): ChannelMeta, A fetched YouTube channel., `fetched_at` is persisted as ISO-8601 UTC, so a naive datetime is ambiguous., Offsets are preserved as an instant, then stored in UTC., test_aware_fetched_at_is_normalised_to_utc(), test_naive_fetched_at_is_rejected()

### Community 64 - "Community 64"
Cohesion: 0.33
Nodes (4): ProviderInfo, Identity and auth state. Must not raise for a merely unauthenticated provider., Identity and auth state, for `provider list`., Identity, with auth reported as unknown.

### Community 65 - "Community 65"
Cohesion: 0.40
Nodes (5): level_from_flags(), Resolve the console level from the global flags. ``--quiet`` wins over ``-v``…, parametrize, --quiet outranks -v: an explicit request for silence beats a scripted -v., test_flag_to_level_mapping()

### Community 66 - "Community 66"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 67 - "Community 67"
Cohesion: 0.40
Nodes (5): MonkeyPatch, A generated config must contain defaults, not whatever the current shell…, A valid env override must not let an invalid assignment be written to disk., test_environment_cannot_mask_an_invalid_file_value(), test_init_defaults_ignore_the_environment()

### Community 68 - "Community 68"
Cohesion: 0.50
Nodes (4): Connection, ConnectionPoolEntry, Apply PRAGMA statements required by ADR 0004 on every SQLite connection., _set_sqlite_pragmas()

### Community 69 - "Community 69"
Cohesion: 0.50
Nodes (3): pytest, testcontainers_core_container, Integration tests using Testcontainers for database verification (ADR 0004).

### Community 70 - "Community 70"
Cohesion: 0.50
Nodes (3): _deep_merge(), Build settings where the environment outranks the TOML file. File values cannot…, Merge ``override`` into ``base``, recursing into nested tables.

### Community 71 - "Community 71"
Cohesion: 0.50
Nodes (3): Session, sessionmaker, Bind the store to a data directory and the session factory used for asset rows.

### Community 72 - "Community 72"
Cohesion: 0.50
Nodes (3): DbStatus, Whether the database is fully migrated to the latest revision., Migration status and storage health metadata.

### Community 73 - "Community 73"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 614 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Repositories` connect `Community 2` to `Community 39`, `Community 43`, `Community 47`, `Community 26`, `Community 62`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `test_classify_url()` connect `Community 24` to `Community 17`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `show()` connect `Community 21` to `Community 48`, `Community 18`, `Community 32`, `Community 29`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `Repositories` (e.g. with `repos()` and `test_duplicate_video_in_a_playlist_is_listed_once()`) actually correct?**
  _`Repositories` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05868118572292801 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.10549645390070922 - nodes in this community are weakly interconnected._