# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1295 nodes · 2571 edges · 109 communities (78 shown, 31 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 217 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `91a40e48`
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
- Community 100
- Community 101
- Community 102
- Community 103
- Community 104
- Community 105
- Community 106
- Community 107
- Community 108

## God Nodes (most connected - your core abstractions)
1. `emit()` - 29 edges
2. `Repositories` - 25 edges
3. `StubSource` - 24 edges
4. `load_settings()` - 24 edges
5. `get_engine()` - 22 edges
6. `AssetStore` - 21 edges
7. `YtDlpSource` - 20 edges
8. `AssetKind` - 20 edges
9. `AppContext` - 19 edges
10. `ThumbforgeError` - 19 edges

## Surprising Connections (you probably didn't know these)
- `repeating()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_cli_fetch.py → src/thumbforge/core/models.py
- `repos()` --uses--> `Repositories`  [INFERRED]
  tests/unit/test_repositories.py → src/thumbforge/storage/repositories.py
- `FakeStore` --uses--> `StoredPlaylist`  [INFERRED]
  tests/unit/test_fetch_service.py → src/thumbforge/core/services/fetch.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_sqlite_database_in_container()` --uses--> `ChannelSource`  [INFERRED]
  tests/integration/test_db_container.py → src/thumbforge/core/enums.py

## Import Cycles
- None detected.

## Communities (109 total, 31 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (57): MonkeyPatch, data_dir(), ChannelMeta, fixture, Path, VideoMeta, `fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP…, An initialised database, since every command here needs the schema. (+49 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (47): The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Repositories, _channel(), _playlist(), ChannelMeta, PlaylistMeta, VideoMeta, Upsert semantics the rest of Phase 2 depends on (ROADMAP P2.3, PLAN.md §3). (+39 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (39): DeclarativeBase, sqlalchemy, sqlalchemy_exc, ChannelSource, Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations., Origin of channel metadata., RunKind (+31 more)

### Community 3 - "Community 3"
Cohesion: 0.10
Nodes (31): Channel, collections_abc, PlaylistItem, rich_console, rich_panel, rich_table, main(), Root Typer application: global flags, context construction, sub-app… (+23 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (32): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, _backdate() (+24 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (28): fixture, entries(), _Entry, Registry behaviour: discovery, duplicate keys, and broken plugins (ADR 0010,…, A plugin needs only an entry point: the registry never imports it by name., Providers should not each have to handle `None`., `provider list` output must not reorder between runs., Same rule when neither side is a builtin. (+20 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (26): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+18 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (26): Any, importlib_util, ModuleType, declarations(), main(), Path, Compare a committed graphify graph against a freshly extracted one. Only…, Ids of the nodes graphify parsed out of a file in this repository. (+18 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (16): pathlib, pytest, `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1). Pure…, testcontainers_core_container, Shared fixtures. Establishes ``tests/`` as the pytest root., Integration tests using Testcontainers for database verification (ADR 0004)., Record `tests/fixtures/ytdlp/*.json` from live YouTube, and assert the S11… (+8 more)

### Community 9 - "Community 9"
Cohesion: 0.18
Nodes (25): default_config_path(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., Spike S5 superseded decision D4: the dangerous flag is not opted into by…, Write a config file and return its path, so tests read as one expression. (+17 more)

### Community 10 - "Community 10"
Cohesion: 0.16
Nodes (24): BoundLogger, CaptureFixture, LogFormat, configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``., Configure structlog and the stdlib root logger. Safe to call more than once. (+16 more)

### Community 11 - "Community 11"
Cohesion: 0.09
Nodes (22): parametrize, ResolvedUrl, classify_url(), Resolve a YouTube URL, handle or bare id to its kind and identifier. A `watch`…, ResolvedUrl, Classify input without touching the network; `core.urls` does the work., ResolvedUrl, UrlKind (+14 more)

### Community 12 - "Community 12"
Cohesion: 0.12
Nodes (23): re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 13 - "Community 13"
Cohesion: 0.11
Nodes (21): FakeSource, FakeStore, DateTime, If the fake drifts from `MetadataSource`, these tests stop meaning anything., One playlist request plus one channel request, regardless of item count., Channel-wide enumeration is a Phase 2 non-goal., Just past the window the network call must happen again., `--refresh` must win even one second after a fetch. (+13 more)

### Community 14 - "Community 14"
Cohesion: 0.12
Nodes (22): platformdirs, pydantic_settings, AntigravitySettings, BatchSettings, ConfigSchema, default_config_toml(), GeneralSettings, LoggingSettings (+14 more)

### Community 15 - "Community 15"
Cohesion: 0.11
Nodes (21): pydantic, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)., A minimal valid video, so each test states only the field it is about., A fetched snapshot is a value; mutating one would desync it from `fetched_at`., `extra="forbid"` turns an unexpected yt-dlp field into a loud failure. yt-dlp's…, `fetched_at` is persisted as ISO-8601 UTC, so a naive datetime is ambiguous., Offsets are preserved as an instant, then stored in UTC. (+13 more)

### Community 16 - "Community 16"
Cohesion: 0.14
Nodes (21): Argument, metavar, rich_syntax, _as_toml(), _config_path(), init_(), path_(), command (+13 more)

### Community 17 - "Community 17"
Cohesion: 0.13
Nodes (21): Engine, integration, Session, sessionmaker, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the…, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., _reclaim_orphans() (+13 more)

### Community 18 - "Community 18"
Cohesion: 0.10
Nodes (22): FetchResult, MetadataSource, fetch(), Argument, ChannelSource, Context, handle_errors, help (+14 more)

### Community 19 - "Community 19"
Cohesion: 0.13
Nodes (18): RawInfo, _duration(), ChannelMeta, PlaylistMeta, VideoMeta, Turn an unexpected yt-dlp info-dict *shape* into a `SourceError`. yt-dlp parses…, Read a string field, treating a missing key and an explicit `None` alike. Both…, Read `duration` as whole seconds. Flat and full extracts disagree by up to a… (+10 more)

### Community 20 - "Community 20"
Cohesion: 0.12
Nodes (21): DownloadError, NotFoundError, SourceError, Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, _translate(), _download_error(), Exception (+13 more)

### Community 21 - "Community 21"
Cohesion: 0.18
Nodes (20): Playlist, list_(), Argument, command, Context, handle_errors, help, Option (+12 more)

### Community 22 - "Community 22"
Cohesion: 0.13
Nodes (19): `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., A source wired to a fixture, plus the recorder that captured its calls., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get…, `position` comes from enumeration order because `playlist_index` is absent… (+11 more)

### Community 23 - "Community 23"
Cohesion: 0.16
Nodes (15): functools, json, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.…, _report() (+7 more)

### Community 24 - "Community 24"
Cohesion: 0.15
Nodes (19): min, P, R, init_(), path_(), command, Context, help (+11 more)

### Community 25 - "Community 25"
Cohesion: 0.19
Nodes (18): ``thumbforge db`` — database lifecycle and migration management (ADR 0004)., DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., get_db_status(), init_db(), Path, Inspect migration revision and file metadata for ``db_path``., Ensure directory exists and upgrade DB to head. Returns: Tuple of… (+10 more)

### Community 26 - "Community 26"
Cohesion: 0.15
Nodes (15): alembic, alembic_config, alembic_runtime_migration, alembic_script, Config, sqlalchemy_pool, sqlite3, _alembic_config() (+7 more)

### Community 27 - "Community 27"
Cohesion: 0.18
Nodes (12): BaseModel, ChannelMeta, _Meta, PlaylistMeta, Shared configuration and provenance for every fetched snapshot., A fetched YouTube channel., A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, A fetched YouTube playlist and its ordered items. (+4 more)

### Community 28 - "Community 28"
Cohesion: 0.15
Nodes (17): list_(), Argument, command, Context, handle_errors, help, Option, List stored videos, most recently fetched first. (+9 more)

### Community 29 - "Community 29"
Cohesion: 0.15
Nodes (14): os, pil, shutil, sqlalchemy_orm, new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits. (+6 more)

### Community 30 - "Community 30"
Cohesion: 0.20
Nodes (14): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderTimeoutError, ProviderTransientError, Error hierarchy and the exit codes it maps to. Every failure the user can…, Base class for image-provider failures. (+6 more)

### Community 31 - "Community 31"
Cohesion: 0.17
Nodes (15): Configuration is missing, malformed, or contains something it must not., SettingsError, _atomic_write(), _format_validation_error(), _parse_scalar(), Replace ``path`` atomically: write a sibling temp file, fsync, then rename. A…, Write the commented default configuration, refusing to clobber unless ``force``., Apply several dotted keys to the TOML file, validating the result once. All… (+7 more)

### Community 32 - "Community 32"
Cohesion: 0.18
Nodes (9): FetchResult, ResolvedUrl, Playlist rows written., Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order., A channel on its own; enumerating its videos is a Phase 2 non-goal., What was fetched, for rendering and for the `--json` contract. Counts are of… (+1 more)

### Community 33 - "Community 33"
Cohesion: 0.14
Nodes (11): FetchStore, ChannelMeta, datetime, MetadataSource, VideoMeta, Take the metadata source and persistence layer the CLI selected., The persistence surface a fetch needs, satisfied by `storage.Repositories`., Persist one video, and its channel when the caller fetched one. (+3 more)

### Community 34 - "Community 34"
Cohesion: 0.16
Nodes (11): _fsync_dir(), Path, Session, sessionmaker, Return the absolute path on disk for ``asset``., Re-hash the file on disk and report whether it matches ``asset.sha256``., Flush a directory entry to disk so a publication survives power loss. Fsyncing…, Bind the store to a data directory and the session factory used for asset rows. (+3 more)

### Community 35 - "Community 35"
Cohesion: 0.18
Nodes (13): _fixture(), Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Load one recorded yt-dlp info dict., Extractor stub that returns a fixture and remembers how it was called. (+5 more)

### Community 36 - "Community 36"
Cohesion: 0.15
Nodes (13): asyncio, BaseException, contextlib, RetryCallState, _cause_chain(), _log_retry(), _published_at(), datetime (+5 more)

### Community 37 - "Community 37"
Cohesion: 0.21
Nodes (13): Console, emit(), kv(), JsonValue, RenderableType, Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.…, Build a two-column key/value table, the default shape for ``show``-style…, _json_context() (+5 more)

### Community 38 - "Community 38"
Cohesion: 0.14
Nodes (11): Extractor, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch. (+3 more)

### Community 39 - "Community 39"
Cohesion: 0.15
Nodes (10): PartialBatchError, Exception, A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., TemplateError, ThumbforgeError, parametrize (+2 more)

### Community 40 - "Community 40"
Cohesion: 0.18
Nodes (13): A supplied URL or identifier is not recognisable YouTube input., UrlError, What a URL or bare identifier turned out to be (ADR 0005)., ResolvedUrl, _channel_handle(), classify_id(), _expect_kind(), UrlKind (+5 more)

### Community 41 - "Community 41"
Cohesion: 0.21
Nodes (9): PlaylistRepository, Playlist, PlaylistMeta, Playlist rows and their ordered items., Return the row for a YouTube playlist id, or `None`., Look a playlist up by ULID or YouTube id, raising `NotFoundError` if absent., Insert or refresh a playlist. `channel_row_id` is required: the column is NOT…, Rewrite a playlist's items to exactly `video_ids`, in order. Rows are deleted… (+1 more)

### Community 42 - "Community 42"
Cohesion: 0.19
Nodes (9): Video, VideoMeta, Look a video up by ULID or YouTube id, raising `NotFoundError` if absent. Both…, Insert or refresh a video, preserving its ULID. `channel_row_id` is supplied…, Videos, newest fetch first, optionally restricted to one channel., Persist one video and, when known, its channel. A single-video fetch can afford…, Video rows, keyed by YouTube video id., Return the row for a YouTube video id, or `None`. (+1 more)

### Community 43 - "Community 43"
Cohesion: 0.18
Nodes (12): ImageProvider, ProviderFactory, ProviderRegistryError, Provider discovery failed: duplicate key, or a plugin that will not load., Image providers: concrete `core.providers.ImageProvider` implementations and…, _discover(), get(), keys() (+4 more)

### Community 44 - "Community 44"
Cohesion: 0.15
Nodes (10): ProviderCapabilities, ProviderInfo, JsonValue, If the stub drifts from `ImageProvider`, every test here stops meaning anything., A minimal `ImageProvider`, standing in for a third-party plugin., Keep the config so a test can prove it was passed through., Deliberately unlike Antigravity, so a test cannot pass by coincidence., Identity, with auth reported as unknown. (+2 more)

### Community 45 - "Community 45"
Cohesion: 0.23
Nodes (7): BaseSettings, Return the settings, or re-raise the failure that prevented loading them.…, default_data_dir(), default_state_dir(), Path, Effective configuration for one invocation: defaults, then file, then…, Settings

### Community 46 - "Community 46"
Cohesion: 0.17
Nodes (12): callback, count, envvar, is_eager, Context, handle_errors, help, Option (+4 more)

### Community 47 - "Community 47"
Cohesion: 0.18
Nodes (10): Collection, NotFoundError, A referenced entity does not exist., PlaylistItem, A playlist's items in playlist order., Reassign `part_number` sequentially from `start` in playlist order. Videos…, One item's `part_number` before and after a `playlist renumber`. Captured per…, Renumbering (+2 more)

### Community 48 - "Community 48"
Cohesion: 0.17
Nodes (8): hashlib, Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 49 - "Community 49"
Cohesion: 0.20
Nodes (12): A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs. (+4 more)

### Community 50 - "Community 50"
Cohesion: 0.20
Nodes (12): _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`., A full extract must carry the fields a flat entry cannot (S11). Also the only…, Re-assert the S11 field set, so a yt-dlp upgrade that changes it fails loudly. (+4 more)

### Community 51 - "Community 51"
Cohesion: 0.23
Nodes (11): get_engine(), Create a SQLAlchemy engine configured for thumbforge SQLite usage., asset_store(), fixture, Provide an initialized AssetStore backed by a temporary SQLite database., Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file() (+3 more)

### Community 52 - "Community 52"
Cohesion: 0.21
Nodes (8): ChannelRepository, Channel, ChannelMeta, Persist a channel on its own (a channel URL was fetched)., Channel rows, keyed by YouTube channel id., Return the row for a YouTube channel id, or `None`., Insert or refresh a channel, preserving its ULID., Every channel, newest fetch first.

### Community 53 - "Community 53"
Cohesion: 0.20
Nodes (10): logging_handlers, bind(), clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Bind context onto every subsequent log record in this task (run id, provider,…, Drop all bound context., structlog, structlog_stdlib (+2 more)

### Community 54 - "Community 54"
Cohesion: 0.24
Nodes (10): Format a SQLite connection URL for SQLAlchemy., sqlite_url(), get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline() (+2 more)

### Community 55 - "Community 55"
Cohesion: 0.22
Nodes (8): dataclasses, datetime, _iso(), Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).…, When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, Render an aware datetime as the ISO-8601 UTC string the schema stores., thumbforge_core_services_fetch, thumbforge_storage_models

### Community 56 - "Community 56"
Cohesion: 0.24
Nodes (9): decimal, Cost, GenerationResult, ProviderInfo, BaseModel, The `ImageProvider` Protocol and the values that cross it (ADR 0010, ROADMAP…, A produced image and the provenance needed to reproduce or audit it.…, Identity and auth state, for `provider list`. (+1 more)

### Community 57 - "Community 57"
Cohesion: 0.22
Nodes (7): Protocol, ImageProvider, ProviderCapabilities, Generate one image per call. Implementations live in `providers/`., What this provider supports; callers check before sending a request., Identity and auth state. Must not raise for a merely unauthenticated provider., What a provider can actually do, so callers degrade instead of guessing.

### Community 58 - "Community 58"
Cohesion: 0.25
Nodes (7): FetchService, Fetch YouTube metadata and persist it., Whether a stored playlist is recent enough to skip the network., A single video can afford the channel request, which populates…, Spec behaviour 2: a playlist fetched inside the window is not re-fetched., test_recent_playlist_is_served_without_a_network_call(), test_video_url_fetches_the_video_and_its_channel()

### Community 59 - "Community 59"
Cohesion: 0.25
Nodes (5): PlaylistMeta, What persisting a playlist actually wrote. Returned instead of the ORM row…, Persist a playlist, its owner, its videos and its order., StoredPlaylist, PlaylistMeta

### Community 60 - "Community 60"
Cohesion: 0.29
Nodes (5): importlib_metadata, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, Provider lookup by key, merging builtins with installed plugins (ADR 0010,…, thumbforge_core_json, thumbforge_core_providers

### Community 61 - "Community 61"
Cohesion: 0.38
Nodes (3): Session, Build the three repositories over one session, so they share a transaction., Bind to the caller's session; the service owns the transaction.

### Community 62 - "Community 62"
Cohesion: 0.33
Nodes (5): field_validator, datetime, Default for `fetched_at`: an aware UTC instant, never a naive local one., Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC., _utcnow()

### Community 63 - "Community 63"
Cohesion: 0.40
Nodes (6): ComplianceError, A generated image violates the YouTube thumbnail requirements., Machine mode contract: stdout carries command output, stderr carries the…, test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), boom(), root()

### Community 64 - "Community 64"
Cohesion: 0.33
Nodes (4): HealthReport, Every check this provider can run, with actionable detail on each failure., The result of `provider check`: every check, not just the first failure. `ok`…, True when every check passed.

### Community 66 - "Community 66"
Cohesion: 0.40
Nodes (4): enum, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., UrlKind

### Community 67 - "Community 67"
Cohesion: 0.40
Nodes (4): GenerationRequest, GenerationResult, Path, Return a result pointing at a path inside `workdir`.

### Community 68 - "Community 68"
Cohesion: 0.40
Nodes (4): IntEnum, ExitCode, Process exit statuses. Values are a public contract., test_keyboard_interrupt_exits_130()

### Community 69 - "Community 69"
Cohesion: 0.40
Nodes (4): GenerationRequest, Path, One image to generate. Providers ignore what their capabilities disclaim., Produce one image, or raise a `ProviderError` subclass. `workdir` is a caller-…

### Community 70 - "Community 70"
Cohesion: 0.40
Nodes (5): level_from_flags(), Resolve the console level from the global flags. ``--quiet`` wins over ``-v``…, parametrize, --quiet outranks -v: an explicit request for silence beats a scripted -v., test_flag_to_level_mapping()

### Community 71 - "Community 71"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 72 - "Community 72"
Cohesion: 0.40
Nodes (5): MonkeyPatch, A generated config must contain defaults, not whatever the current shell…, A valid env override must not let an invalid assignment be written to disk., test_environment_cannot_mask_an_invalid_file_value(), test_init_defaults_ignore_the_environment()

### Community 73 - "Community 73"
Cohesion: 0.50
Nodes (4): Connection, ConnectionPoolEntry, Apply PRAGMA statements required by ADR 0004 on every SQLite connection., _set_sqlite_pragmas()

### Community 74 - "Community 74"
Cohesion: 0.50
Nodes (3): HealthReport, Check, One named healthcheck outcome, with enough detail to act on a failure.

### Community 75 - "Community 75"
Cohesion: 0.50
Nodes (3): PlaylistItemMeta, One video's place in a playlist., PlaylistMeta

### Community 76 - "Community 76"
Cohesion: 0.50
Nodes (3): _deep_merge(), Build settings where the environment outranks the TOML file. File values cannot…, Merge ``override`` into ``base``, recursing into nested tables.

### Community 77 - "Community 77"
Cohesion: 0.50
Nodes (3): DbStatus, Whether the database is fully migrated to the latest revision., Migration status and storage health metadata.

### Community 78 - "Community 78"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 625 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FetchService` connect `Community 58` to `Community 32`, `Community 33`, `Community 8`, `Community 13`, `Community 18`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `YtDlpSource` connect `Community 38` to `Community 35`, `Community 36`, `Community 11`, `Community 49`, `Community 18`, `Community 19`, `Community 22`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `fetch()` connect `Community 18` to `Community 3`, `Community 37`, `Community 17`, `Community 21`, `Community 58`, `Community 28`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `Repositories` (e.g. with `repos()` and `test_duplicate_video_in_a_playlist_is_listed_once()`) actually correct?**
  _`Repositories` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.0546448087431694 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.09308510638297872 - nodes in this community are weakly interconnected._