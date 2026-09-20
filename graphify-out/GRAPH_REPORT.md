# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1395 nodes · 2792 edges · 107 communities (67 shown, 40 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 262 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f9aeb109`
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

## God Nodes (most connected - your core abstractions)
1. `emit()` - 29 edges
2. `FakeProvider` - 26 edges
3. `Repositories` - 25 edges
4. `StubSource` - 24 edges
5. `load_settings()` - 24 edges
6. `get_engine()` - 22 edges
7. `AssetStore` - 21 edges
8. `YtDlpSource` - 20 edges
9. `AssetKind` - 20 edges
10. `ThumbforgeError` - 19 edges

## Surprising Connections (you probably didn't know these)
- `repeating()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_cli_fetch.py → src/thumbforge/core/models.py
- `StubProvider` --uses--> `GenerationRequest`  [INFERRED]
  tests/unit/test_provider_registry.py → src/thumbforge/core/providers.py
- `StubProvider` --uses--> `ProviderInfo`  [INFERRED]
  tests/unit/test_provider_registry.py → src/thumbforge/core/providers.py
- `test_generate_returns_a_real_image()` --uses--> `GenerationResult`  [INFERRED]
  tests/contract/test_provider_contract.py → src/thumbforge/core/providers.py
- `test_healthcheck_reports_at_least_one_check()` --uses--> `HealthReport`  [INFERRED]
  tests/contract/test_provider_contract.py → src/thumbforge/core/providers.py

## Import Cycles
- None detected.

## Communities (107 total, 40 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (57): MonkeyPatch, data_dir(), ChannelMeta, fixture, Path, VideoMeta, `fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP…, An initialised database, since every command here needs the schema. (+49 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (37): Collection, Session, ChannelRepository, PlaylistRepository, Channel, ChannelMeta, Playlist, PlaylistItem (+29 more)

### Community 2 - "Community 2"
Cohesion: 0.10
Nodes (45): DeclarativeBase, enum, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations., Origin of channel metadata. (+37 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (47): The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Repositories, _channel(), _playlist(), ChannelMeta, PlaylistMeta, VideoMeta, Upsert semantics the rest of Phase 2 depends on (ROADMAP P2.3, PLAN.md §3). (+39 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (34): alembic_config, alembic_runtime_migration, alembic_script, Config, contextlib, sqlalchemy, sqlalchemy_pool, sqlite3 (+26 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (34): fixture, FixtureRequest, pil, ImageProvider, Path, Generate one image per call. Implementations live in `providers/`., What this provider supports; callers check before sending a request., Every check this provider can run, with actionable detail on each failure. (+26 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (31): main(), Root Typer application: global flags, context construction, sub-app…, Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set() (+23 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (35): Engine, integration, get_engine(), init_db(), Session, sessionmaker, Ensure directory exists and upgrade DB to head. Returns: Tuple of…, Create a SQLAlchemy engine configured for thumbforge SQLite usage. (+27 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (33): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, Store an image file or bytes content-addressed by SHA-256. If identical content… (+25 more)

### Community 9 - "Community 9"
Cohesion: 0.10
Nodes (22): alembic, collections_abc, pytest, The JSON shape that crosses every machine-readable boundary. Defined in `core`…, `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1). Pure…, Provider lookup by key, merging builtins with installed plugins (ADR 0010,…, `YtDlpSource` — YouTube metadata via `yt-dlp`, no API key (ADR 0005, ROADMAP… (+14 more)

### Community 10 - "Community 10"
Cohesion: 0.09
Nodes (30): Any, importlib_util, ModuleType, re, declarations(), main(), Path, Compare a committed graphify graph against a freshly extracted one. Only… (+22 more)

### Community 11 - "Community 11"
Cohesion: 0.08
Nodes (27): entries(), _Entry, fixture, Registry behaviour: discovery, duplicate keys, and broken plugins (ADR 0010,…, A plugin needs only an entry point: the registry never imports it by name., Providers should not each have to handle `None`., `provider list` output must not reorder between runs., Same rule when neither side is a builtin. (+19 more)

### Community 12 - "Community 12"
Cohesion: 0.10
Nodes (23): BaseModel, decimal, Check, Cost, GenerationResult, HealthReport, ProviderCapabilities, The `ImageProvider` Protocol and the values that cross it (ADR 0010, ROADMAP… (+15 more)

### Community 13 - "Community 13"
Cohesion: 0.15
Nodes (28): BoundLogger, CaptureFixture, LogFormat, bind(), configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``. (+20 more)

### Community 14 - "Community 14"
Cohesion: 0.09
Nodes (28): parametrize, ResolvedUrl, A supplied URL or identifier is not recognisable YouTube input., UrlError, _channel_handle(), classify_id(), classify_url(), _expect_kind() (+20 more)

### Community 15 - "Community 15"
Cohesion: 0.11
Nodes (26): Channel, FetchResult, PlaylistItem, JsonPayload, RenderableType, Repositories, ``thumbforge fetch`` — pull YouTube metadata into the database (ROADMAP P2.3)., The ``Stored N channel, N playlist, N videos.`` line from ``PLAN.md`` §5.3. (+18 more)

### Community 16 - "Community 16"
Cohesion: 0.15
Nodes (26): FakeProvider, Generate a deterministic placeholder image without leaving the machine., parametrize, Path, `FakeProvider` behaviour the generic contract cannot express (PLAN.md §4.2,…, A test asserting style anchoring needs to see the reference in the output., Callers pass a run-scoped directory that may not exist yet., The fake honours dimensions exactly, which the generic contract cannot require.… (+18 more)

### Community 17 - "Community 17"
Cohesion: 0.10
Nodes (24): model_validator, platformdirs, pydantic_settings, Self, AntigravitySettings, BatchSettings, ConfigSchema, default_config_toml() (+16 more)

### Community 18 - "Community 18"
Cohesion: 0.18
Nodes (25): default_config_path(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., Spike S5 superseded decision D4: the dangerous flag is not opted into by…, Write a config file and return its path, so tests read as one expression. (+17 more)

### Community 19 - "Community 19"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, Yield `exc` and its `cause` links; `ExtractorError` nests the real failure… (+16 more)

### Community 20 - "Community 20"
Cohesion: 0.13
Nodes (22): find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,…, redact() (+14 more)

### Community 21 - "Community 21"
Cohesion: 0.13
Nodes (22): Argument, metavar, rich_syntax, _as_toml(), _config_path(), init_(), path_(), command (+14 more)

### Community 22 - "Community 22"
Cohesion: 0.13
Nodes (21): get_app_context(), Context, Extract and validate the AppContext from a Typer execution context., list_(), Argument, command, Context, handle_errors (+13 more)

### Community 23 - "Community 23"
Cohesion: 0.11
Nodes (15): asyncio, hashlib, pathlib, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return the hex SHA-256 of ``data``., sha256_bytes(), Domain layer: models, errors and services. Imports nothing internal except…, `FakeProvider` — deterministic, offline image generation (PLAN.md §4.2, ROADMAP… (+7 more)

### Community 24 - "Community 24"
Cohesion: 0.19
Nodes (20): Playlist, list_(), Argument, command, Context, handle_errors, help, Option (+12 more)

### Community 25 - "Community 25"
Cohesion: 0.10
Nodes (17): shutil, sqlalchemy_exc, sqlalchemy_orm, new_id(), Path, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of a file, read in chunks so large images stay off the…, sha256_file() (+9 more)

### Community 26 - "Community 26"
Cohesion: 0.12
Nodes (14): Protocol, FetchStore, ChannelMeta, datetime, MetadataSource, PlaylistMeta, VideoMeta, Take the metadata source and persistence layer the CLI selected. (+6 more)

### Community 27 - "Community 27"
Cohesion: 0.16
Nodes (12): FetchResult, FetchService, ResolvedUrl, Playlist rows written., Fetch YouTube metadata and persist it., Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order. (+4 more)

### Community 28 - "Community 28"
Cohesion: 0.12
Nodes (17): callback, count, envvar, is_eager, Context, handle_errors, help, Option (+9 more)

### Community 29 - "Community 29"
Cohesion: 0.16
Nodes (17): min, P, R, init_(), path_(), command, Context, help (+9 more)

### Community 30 - "Community 30"
Cohesion: 0.16
Nodes (16): _app_context(), wrapper(), _is_json_mode(), Find the :class:`AppContext` the root callback stored on the Click context.…, _report(), AppContext, Per-invocation state built by the root callback and stored on ``ctx.obj``., ComplianceError (+8 more)

### Community 31 - "Community 31"
Cohesion: 0.15
Nodes (15): _fixture(), Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Load one recorded yt-dlp info dict. (+7 more)

### Community 32 - "Community 32"
Cohesion: 0.18
Nodes (15): Console, Print current revision, head revision, pending count, file size, and journal…, status(), emit(), kv(), JsonValue, RenderableType, Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.… (+7 more)

### Community 33 - "Community 33"
Cohesion: 0.20
Nodes (11): functools, json, rich_console, rich_panel, rich_table, ``thumbforge db`` — database lifecycle and migration management (ADR 0004)., Turn exceptions into process exits. The only module permitted to exit the…, The only module allowed to write to stdout. Every command produces one of two… (+3 more)

### Community 34 - "Community 34"
Cohesion: 0.15
Nodes (15): ProviderFactory, NotFoundError, ProviderRegistryError, Provider discovery failed: duplicate key, or a plugin that will not load., A referenced entity does not exist., Image providers: concrete `core.providers.ImageProvider` implementations and…, _discover(), get() (+7 more)

### Community 35 - "Community 35"
Cohesion: 0.14
Nodes (14): pydantic, datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Default for `fetched_at`: an aware UTC instant, never a naive local one., _utcnow(), Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)., `resolve()` returns both halves (ADR 0005); an empty id is never a valid result., `extra="forbid"` turns an unexpected yt-dlp field into a loud failure. yt-dlp's… (+6 more)

### Community 36 - "Community 36"
Cohesion: 0.13
Nodes (12): PartialBatchError, Exception, A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., A metadata source failed., SourceError, TemplateError (+4 more)

### Community 37 - "Community 37"
Cohesion: 0.13
Nodes (11): Extractor, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, ResolvedUrl, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., Classify input without touching the network; `core.urls` does the work., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes… (+3 more)

### Community 38 - "Community 38"
Cohesion: 0.18
Nodes (14): RawInfo, _duration(), _published_at(), datetime, PlaylistMeta, Read a string field, treating a missing key and an explicit `None` alike. Both…, Recover an upload instant from `timestamp`, or `None` if yt-dlp reported none.…, Read `duration` as whole seconds. Flat and full extracts disagree by up to a… (+6 more)

### Community 39 - "Community 39"
Cohesion: 0.20
Nodes (14): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderTimeoutError, ProviderTransientError, Error hierarchy and the exit codes it maps to. Every failure the user can…, Base class for image-provider failures. (+6 more)

### Community 40 - "Community 40"
Cohesion: 0.13
Nodes (13): FakeSource, ResolvedUrl, If the fake drifts from `MetadataSource`, these tests stop meaning anything., A single video can afford the channel request, which populates…, Just past the window the network call must happen again., `--refresh` must win even one second after a fetch., `playlist.channel_id` is NOT NULL, so there is no row to write without it.…, A `MetadataSource` that records calls and returns canned metadata. (+5 more)

### Community 41 - "Community 41"
Cohesion: 0.14
Nodes (13): FakeStore, DateTime, One playlist request plus one channel request, regardless of item count., Channel-wide enumeration is a Phase 2 non-goal., Spec behaviour 2: a playlist fetched inside the window is not re-fetched., A video fetch is one cheap request and always reflects the latest title., `fetch` tells the user a re-fetch shrank the playlist., The `FetchStore` surface, recording what was written. (+5 more)

### Community 42 - "Community 42"
Cohesion: 0.20
Nodes (10): BaseSettings, _atomic_write(), default_state_dir(), Path, Effective configuration for one invocation: defaults, then file, then…, Replace ``path`` atomically: write a sibling temp file, fsync, then rename. A…, Write the commented default configuration, refusing to clobber unless ``force``., Settings (+2 more)

### Community 43 - "Community 43"
Cohesion: 0.18
Nodes (11): Image, GenerationRequest, One image to generate. Providers ignore what their capabilities disclaim., _contrasting(), _digest(), Path, Render one deterministic PNG into `workdir`. Raises before doing any work when…, Paint the image. Pure function of `request` and `digest`, so output is stable. (+3 more)

### Community 44 - "Community 44"
Cohesion: 0.20
Nodes (13): parametrize, Invariants the provider boundary models enforce (ADR 0010, ROADMAP P3.1/P3.2)., Providers join this onto a path, so it must not be able to leave the workdir.…, The constraint must not reject what `PLAN.md` §6 and the test suites really use., A filename has a length limit even when every character is safe., `extra="forbid"` stops a caller asserting health that the checks contradict., A request is a value; mutating one after dispatch would desync it from its key., _request() (+5 more)

### Community 45 - "Community 45"
Cohesion: 0.14
Nodes (14): S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., A source wired to a fixture, plus the recorder that captured its calls., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get…, `position` comes from enumeration order because `playlist_index` is absent…, _source() (+6 more)

### Community 46 - "Community 46"
Cohesion: 0.17
Nodes (10): RetryCallState, _log_retry(), ChannelMeta, VideoMeta, Turn an unexpected yt-dlp info-dict *shape* into a `SourceError`. yt-dlp parses…, Full extract of one video, so `description` and `published_at` are populated., Channel metadata only — never its video list. Enumerating a channel is a non-…, Extract off the event loop, retrying only transient failures (PLAN.md §7.2). (+2 more)

### Community 47 - "Community 47"
Cohesion: 0.18
Nodes (12): Settings, Return the settings, or re-raise the failure that prevented loading them.…, Configuration is missing, malformed, or contains something it must not., SettingsError, _format_validation_error(), _parse_scalar(), Apply several dotted keys to the TOML file, validating the result once. All…, Parse a CLI value using TOML scalar rules, falling back to a bare string.… (+4 more)

### Community 48 - "Community 48"
Cohesion: 0.17
Nodes (10): importlib_metadata, os, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, structlog, isolate_user_environment(), fixture, MonkeyPatch, Path (+2 more)

### Community 49 - "Community 49"
Cohesion: 0.17
Nodes (12): MetadataSource, fetch(), Argument, ChannelSource, Context, handle_errors, help, Option (+4 more)

### Community 50 - "Community 50"
Cohesion: 0.26
Nodes (8): ChannelMeta, A fetched YouTube channel., A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, What a URL or bare identifier turned out to be (ADR 0005)., ResolvedUrl, VideoMeta, MetadataSource, Protocol

### Community 51 - "Community 51"
Cohesion: 0.20
Nodes (12): _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`., A full extract must carry the fields a flat entry cannot (S11). Also the only…, Re-assert the S11 field set, so a yt-dlp upgrade that changes it fails loudly. (+4 more)

### Community 52 - "Community 52"
Cohesion: 0.18
Nodes (5): What persisting a playlist actually wrote. Returned instead of the ORM row…, StoredPlaylist, ChannelMeta, PlaylistMeta, VideoMeta

### Community 53 - "Community 53"
Cohesion: 0.22
Nodes (8): dataclasses, datetime, _iso(), Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).…, When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, Render an aware datetime as the ISO-8601 UTC string the schema stores., thumbforge_core_services_fetch, thumbforge_storage_models

### Community 54 - "Community 54"
Cohesion: 0.24
Nodes (10): A metadata source failed for a reason worth retrying (network, throttling).…, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs., test_retry_emits_a_log_event(), failing() (+2 more)

### Community 55 - "Community 55"
Cohesion: 0.20
Nodes (7): ProviderInfo, Identity and auth state. Must not raise for a merely unauthenticated provider., Identity and auth state, for `provider list`., Always authenticated: there is nothing to authenticate against., Provenance is recorded from this, so it must not disagree with the registry., test_info_reports_the_key_it_is_registered_under(), Identity, with auth reported as unknown.

### Community 56 - "Community 56"
Cohesion: 0.27
Nodes (9): Format a SQLite connection URL for SQLAlchemy., sqlite_url(), get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline() (+1 more)

### Community 57 - "Community 57"
Cohesion: 0.20
Nodes (10): A minimal valid video, so each test states only the field it is about., A fetched snapshot is a value; mutating one would desync it from `fetched_at`., Optional columns default to the values the `video` table expects., `position` is 1-based playlist order; 0 would break part numbering. Not sourced…, `item_count` feeds the `playlist.item_count` column, so it must not drift., test_defaults_match_the_schema(), test_item_count_tracks_items(), test_playlist_position_is_one_based() (+2 more)

### Community 58 - "Community 58"
Cohesion: 0.24
Nodes (6): Connection, ConnectionPoolEntry, Apply PRAGMA statements required by ADR 0004 on every SQLite connection., _set_sqlite_pragmas(), testcontainers_core_container, Integration tests using Testcontainers for database verification (ADR 0004).

### Community 59 - "Community 59"
Cohesion: 0.29
Nodes (5): field_validator, _Meta, Shared configuration and provenance for every fetched snapshot., Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC., Refuse a key that is only dots, which the character class alone would allow.

### Community 60 - "Community 60"
Cohesion: 0.33
Nodes (5): logging_handlers, clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Drop all bound context., structlog_stdlib

### Community 61 - "Community 61"
Cohesion: 0.40
Nodes (4): IntEnum, ExitCode, Process exit statuses. Values are a public contract., test_keyboard_interrupt_exits_130()

### Community 62 - "Community 62"
Cohesion: 0.40
Nodes (3): PlaylistMeta, A fetched YouTube playlist and its ordered items., Number of items fetched, for the `playlist.item_count` column.

### Community 63 - "Community 63"
Cohesion: 0.40
Nodes (5): MonkeyPatch, A generated config must contain defaults, not whatever the current shell…, A valid env override must not let an invalid assignment be written to disk., test_environment_cannot_mask_an_invalid_file_value(), test_init_defaults_ignore_the_environment()

### Community 64 - "Community 64"
Cohesion: 0.50
Nodes (3): PlaylistItemMeta, One video's place in a playlist., PlaylistMeta

### Community 65 - "Community 65"
Cohesion: 0.50
Nodes (3): _deep_merge(), Build settings where the environment outranks the TOML file. File values cannot…, Merge ``override`` into ``base``, recursing into nested tables.

### Community 66 - "Community 66"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 676 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `test_sqlite_database_in_container()` connect `Community 7` to `Community 58`, `Community 2`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Why does `classify_url()` connect `Community 14` to `Community 37`, `Community 40`, `Community 9`, `Community 50`, `Community 24`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `PlaylistRepository` connect `Community 1` to `Community 53`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `FakeProvider` (e.g. with `Check` and `GenerationRequest`) actually correct?**
  _`FakeProvider` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `Repositories` (e.g. with `repos()` and `test_duplicate_video_in_a_playlist_is_listed_once()`) actually correct?**
  _`Repositories` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.0546448087431694 - nodes in this community are weakly interconnected._