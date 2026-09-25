# Graph Report - thumbforge-P4.1  (2026-09-25)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1746 nodes · 3488 edges · 133 communities (93 shown, 40 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 302 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ec3ecf65`
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
- Community 109
- Community 110
- Community 111
- Community 112
- Community 113
- Community 114
- Community 115
- Community 116
- Community 117
- Community 118
- Community 119
- Community 120
- Community 121
- Community 122
- Community 123
- Community 124
- Community 125
- Community 126
- Community 127
- Community 128
- Community 129
- Community 130
- Community 131
- Community 132

## God Nodes (most connected - your core abstractions)
1. `emit()` - 34 edges
2. `load_settings()` - 26 edges
3. `Repositories` - 25 edges
4. `StubSource` - 24 edges
5. `FakeProvider` - 24 edges
6. `get_engine()` - 22 edges
7. `AntigravityProvider` - 21 edges
8. `AssetStore` - 21 edges
9. `get_app_context()` - 21 edges
10. `YtDlpSource` - 20 edges

## Surprising Connections (you probably didn't know these)
- `repeating()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_cli_fetch.py → src/thumbforge/core/models.py
- `stub()` --indirect_call--> `models()`  [INFERRED]
  tests/unit/test_cli_provider.py → src/thumbforge/cli/provider.py
- `test_insert_all_nine_models_and_verify_relations()` --uses--> `Asset`  [INFERRED]
  tests/unit/test_storage_models.py → src/thumbforge/storage/models.py
- `test_on_delete_restrict_on_reference_asset()` --uses--> `Asset`  [INFERRED]
  tests/unit/test_storage_models.py → src/thumbforge/storage/models.py
- `_provider()` --uses--> `AntigravityProvider`  [INFERRED]
  tests/unit/test_antigravity_provider.py → src/thumbforge/providers/antigravity.py

## Import Cycles
- None detected.

## Communities (133 total, 40 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (59): BaseModel, model_validator, parametrize, pydantic, Self, Anchor, BadgeBlock, Box (+51 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (55): MonkeyPatch, data_dir(), ChannelMeta, fixture, Path, VideoMeta, `fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP…, An initialised database, since every command here needs the schema. (+47 more)

### Community 2 - "Community 2"
Cohesion: 0.04
Nodes (51): Check, fixture, _healthcheck(), stub(), _no_real_keyring(), HealthReport, MonkeyPatch, parametrize (+43 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (42): DeclarativeBase, enum, sqlalchemy, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations. (+34 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (45): The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Repositories, _channel(), _playlist(), ChannelMeta, PlaylistMeta, VideoMeta, `UNIQUE(playlist_id, position)` makes an in-place swap a constraint violation. (+37 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (42): _envelope(), _plant_image(), _provider(), Any, GenerationRequest, Path, `AntigravityProvider` error mapping and argv, with the CLI replaced (ROADMAP…, S2: the tool takes no output path, so the adapter finds and copies the result. (+34 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (30): asyncio, collections_abc, decimal, json, pathlib, pil, pytest, ``thumbforge provider`` — inspect providers and store their keys (ROADMAP P3.5). (+22 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (35): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, asset_store() (+27 more)

### Community 8 - "Community 8"
Cohesion: 0.08
Nodes (31): entries(), _Entry, fixture, MonkeyPatch, Registry behaviour: discovery, duplicate keys, and broken plugins (ADR 0010,…, A plugin needs only an entry point: the registry never imports it by name., Providers should not each have to handle `None`., `provider list` output must not reorder between runs. (+23 more)

### Community 9 - "Community 9"
Cohesion: 0.09
Nodes (32): FixtureRequest, shutil, provider(), _provider_params(), Any, fixture, GenerationRequest, ImageProvider (+24 more)

### Community 10 - "Community 10"
Cohesion: 0.11
Nodes (20): dataclasses, rich_console, rich_panel, rich_table, main(), Root Typer application: global flags, context construction, sub-app…, ``thumbforge fetch`` — pull YouTube metadata into the database (ROADMAP P2.3)., panel() (+12 more)

### Community 11 - "Community 11"
Cohesion: 0.09
Nodes (23): os, sqlalchemy_exc, sqlalchemy_orm, new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of ``data``. (+15 more)

### Community 12 - "Community 12"
Cohesion: 0.08
Nodes (23): ProviderCapabilities, ProviderInfo, AntigravityProvider, _installed_plugins(), _parse_models(), HealthReport, Generate an image by driving `agy` in headless mode., Measured in spikes S3, S4 and S7 — see the module docstring. (+15 more)

### Community 13 - "Community 13"
Cohesion: 0.16
Nodes (26): BoundLogger, CaptureFixture, LogFormat, configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``., Configure structlog and the stdlib root logger. Safe to call more than once. (+18 more)

### Community 14 - "Community 14"
Cohesion: 0.17
Nodes (26): default_config_path(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., Spike S5 superseded decision D4: the dangerous flag is not opted into by…, The secret filter must not swallow ordinary nested provider settings. (+18 more)

### Community 15 - "Community 15"
Cohesion: 0.10
Nodes (22): ResolvedUrl, classify_url(), Resolve a YouTube URL, handle or bare id to its kind and identifier. A `watch`…, ResolvedUrl, Classify input without touching the network; `core.urls` does the work., ResolvedUrl, UrlKind, Which YouTube URLs and ids resolve to which kind (ADR 0005, ROADMAP P2.1). (+14 more)

### Community 16 - "Community 16"
Cohesion: 0.11
Nodes (22): ComplianceError, PartialBatchError, ProviderAuthError, ProviderError, ProviderTimeoutError, ProviderTransientError, Exception, Error hierarchy and the exit codes it maps to. Every failure the user can… (+14 more)

### Community 17 - "Community 17"
Cohesion: 0.09
Nodes (24): PlaylistItemMeta, One video's place in a playlist., PlaylistMeta, Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)., `resolve()` returns both halves (ADR 0005); an empty id is never a valid result., A minimal valid video, so each test states only the field it is about., A fetched snapshot is a value; mutating one would desync it from `fetched_at`., `extra="forbid"` turns an unexpected yt-dlp field into a loud failure. yt-dlp's… (+16 more)

### Community 18 - "Community 18"
Cohesion: 0.15
Nodes (24): Playlist, list_(), Argument, command, Context, handle_errors, help, Option (+16 more)

### Community 19 - "Community 19"
Cohesion: 0.13
Nodes (22): find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,…, redact() (+14 more)

### Community 20 - "Community 20"
Cohesion: 0.12
Nodes (20): functools, IntEnum, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.…, _report() (+12 more)

### Community 21 - "Community 21"
Cohesion: 0.11
Nodes (19): GenerationResult, ProviderOutputMissingError, The provider reported success but produced no usable image., GenerationRequest, Path, Build the prompt sent to `agy -p`. The aspect ratio is given in words because…, Run one generation and copy its output into `workdir`., Assemble the command line. Never `--continue`: every image is a fresh run. (+11 more)

### Community 22 - "Community 22"
Cohesion: 0.12
Nodes (20): `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, FakeSource, `FetchService` decisions: kind dispatch, the freshness rule, and what each…, If the fake drifts from `MetadataSource`, these tests stop meaning anything., Spec behaviour 2: a playlist fetched inside the window is not re-fetched., Just past the window the network call must happen again., `--refresh` must win even one second after a fetch., A video fetch is one cheap request and always reflects the latest title. (+12 more)

### Community 23 - "Community 23"
Cohesion: 0.15
Nodes (23): FakeProvider, Generate a deterministic placeholder image without leaving the machine., parametrize, Path, A test asserting style anchoring needs to see the reference in the output., Callers pass a run-scoped directory that may not exist yet., The fake honours dimensions exactly, which the generic contract cannot require.…, Phase 3's retry policy selects on `retryable`, so the flag is the contract. (+15 more)

### Community 24 - "Community 24"
Cohesion: 0.14
Nodes (21): Argument, metavar, rich_syntax, _as_toml(), _config_path(), init_(), path_(), command (+13 more)

### Community 25 - "Community 25"
Cohesion: 0.16
Nodes (22): command, _KEY_ARGUMENT, check(), _config(), list_(), collect(), models(), Context (+14 more)

### Community 26 - "Community 26"
Cohesion: 0.13
Nodes (18): RawInfo, _duration(), ChannelMeta, PlaylistMeta, VideoMeta, Turn an unexpected yt-dlp info-dict *shape* into a `SourceError`. yt-dlp parses…, Read a string field, treating a missing key and an explicit `None` alike. Both…, Read `duration` as whole seconds. Flat and full extracts disagree by up to a… (+10 more)

### Community 27 - "Community 27"
Cohesion: 0.12
Nodes (20): CliRunner, JsonPayload, Cost, What one generation consumed. `credits`/`currency` are optional because a…, _as_int(), _as_str(), _cost(), _looks_like_timeout() (+12 more)

### Community 28 - "Community 28"
Cohesion: 0.12
Nodes (21): DownloadError, NotFoundError, SourceError, Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, _translate(), _download_error(), Exception (+13 more)

### Community 29 - "Community 29"
Cohesion: 0.16
Nodes (20): min, P, R, init_(), path_(), command, Context, help (+12 more)

### Community 30 - "Community 30"
Cohesion: 0.17
Nodes (19): Any, importlib_util, ModuleType, _declaration(), _graph(), _module(), Path, The drift check's node filter (issue #26). This is a CI gate, so a silently… (+11 more)

### Community 31 - "Community 31"
Cohesion: 0.13
Nodes (19): Channel, PlaylistItem, JsonPayload, RenderableType, Repositories, Build the JSON payload and the Rich renderable from the **stored** rows.…, _view(), channel_payload() (+11 more)

### Community 32 - "Community 32"
Cohesion: 0.10
Nodes (15): GenerationRequest, GenerationResult, HealthReport, JsonValue, Path, ProviderCapabilities, ProviderInfo, If the stub drifts from `ImageProvider`, every test here stops meaning anything. (+7 more)

### Community 33 - "Community 33"
Cohesion: 0.13
Nodes (19): `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., A source wired to a fixture, plus the recorder that captured its calls., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get…, `position` comes from enumeration order because `playlist_index` is absent… (+11 more)

### Community 34 - "Community 34"
Cohesion: 0.16
Nodes (12): Collection, PlaylistRepository, Playlist, PlaylistItem, Playlist rows and their ordered items., Return the row for a YouTube playlist id, or `None`., Look a playlist up by ULID or YouTube id, raising `NotFoundError` if absent., Insert or refresh a playlist. `channel_row_id` is required: the column is NOT… (+4 more)

### Community 35 - "Community 35"
Cohesion: 0.13
Nodes (18): Settings, Return the settings, or re-raise the failure that prevented loading them.…, Configuration is missing, malformed, or contains something it must not., SettingsError, _atomic_write(), _format_validation_error(), _parse_scalar(), Replace ``path`` atomically: write a sibling temp file, fsync, then rename. A… (+10 more)

### Community 36 - "Community 36"
Cohesion: 0.16
Nodes (12): FetchResult, FetchService, ResolvedUrl, Playlist rows written., Fetch YouTube metadata and persist it., Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order. (+4 more)

### Community 37 - "Community 37"
Cohesion: 0.15
Nodes (18): Engine, integration, Session, sessionmaker, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., session_factory(), session_scope() (+10 more)

### Community 38 - "Community 38"
Cohesion: 0.12
Nodes (13): FetchStore, ChannelMeta, datetime, MetadataSource, PlaylistMeta, VideoMeta, Take the metadata source and persistence layer the CLI selected., The persistence surface a fetch needs, satisfied by `storage.Repositories`. (+5 more)

### Community 39 - "Community 39"
Cohesion: 0.15
Nodes (15): alembic, alembic_config, alembic_runtime_migration, alembic_script, Config, sqlalchemy_pool, sqlite3, _alembic_config() (+7 more)

### Community 40 - "Community 40"
Cohesion: 0.12
Nodes (17): callback, count, envvar, is_eager, Option, Context, handle_errors, help (+9 more)

### Community 41 - "Community 41"
Cohesion: 0.21
Nodes (16): Path, Unit tests for ``thumbforge db`` CLI commands (ADR 0004, Phase 1 spec)., test_db_init_creates_database_and_is_idempotent(), test_db_init_json_mode(), test_db_json_error_stream_contract(), test_db_path_command(), test_db_path_json_mode(), test_db_status_command() (+8 more)

### Community 42 - "Community 42"
Cohesion: 0.15
Nodes (15): _fixture(), Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Load one recorded yt-dlp info dict. (+7 more)

### Community 43 - "Community 43"
Cohesion: 0.15
Nodes (12): importlib_metadata, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set() (+4 more)

### Community 44 - "Community 44"
Cohesion: 0.19
Nodes (11): ChannelMeta, _Meta, PlaylistMeta, Shared configuration and provenance for every fetched snapshot., A fetched YouTube channel., A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, A fetched YouTube playlist and its ordered items., Number of items fetched, for the `playlist.item_count` column. (+3 more)

### Community 45 - "Community 45"
Cohesion: 0.13
Nodes (15): FetchResult, MetadataSource, fetch(), Argument, ChannelSource, Context, handle_errors, help (+7 more)

### Community 46 - "Community 46"
Cohesion: 0.15
Nodes (14): platformdirs, pydantic_settings, pydantic_settings_sources, ConfigSchema, default_config_toml(), Configuration: TOML file, ``THUMBFORGE_*`` environment variables, and defaults.…, The shape of ``config.toml``, with no environment involvement. Kept separate…, Render the default configuration as commented TOML for ``config init``. (+6 more)

### Community 47 - "Community 47"
Cohesion: 0.18
Nodes (14): DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., get_db_status(), Path, Inspect migration revision and file metadata for ``db_path``., Run Alembic upgrade to ``revision`` on ``db_path``., Reclaim free space, truncate the WAL, and delete unreferenced asset files.…, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the… (+6 more)

### Community 48 - "Community 48"
Cohesion: 0.20
Nodes (13): fit_to(), Image, Resize and centre-crop an image to an exact target size (ROADMAP P5.1)., Scale `img` to cover `width`x`height`, then centre-crop to exactly that size,…, Image, parametrize, `fit_to`: cover the target, centre-crop, never distort (ROADMAP P5.1)., Three equal bands, red / green / blue, left to right or top to bottom. (+5 more)

### Community 49 - "Community 49"
Cohesion: 0.15
Nodes (13): BaseException, contextlib, RetryCallState, _cause_chain(), _log_retry(), _published_at(), datetime, `YtDlpSource` — YouTube metadata via `yt-dlp`, no API key (ADR 0005, ROADMAP… (+5 more)

### Community 50 - "Community 50"
Cohesion: 0.21
Nodes (13): Console, emit(), kv(), JsonValue, RenderableType, Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.…, Build a two-column key/value table, the default shape for ``show``-style…, _json_context() (+5 more)

### Community 51 - "Community 51"
Cohesion: 0.21
Nodes (13): keyring, keyring_errors, api_key(), describe(), env_var(), _from_env(), Provider API keys: read from the environment or the system keyring (ROADMAP…, The environment variable this provider's key is read from. Mirrors pydantic-… (+5 more)

### Community 52 - "Community 52"
Cohesion: 0.19
Nodes (9): Video, VideoMeta, Look a video up by ULID or YouTube id, raising `NotFoundError` if absent. Both…, Insert or refresh a video, preserving its ULID. `channel_row_id` is supplied…, Videos, newest fetch first, optionally restricted to one channel., Persist one video and, when known, its channel. A single-video fetch can afford…, Video rows, keyed by YouTube video id., Return the row for a YouTube video id, or `None`. (+1 more)

### Community 53 - "Community 53"
Cohesion: 0.20
Nodes (13): parametrize, Invariants the provider boundary models enforce (ADR 0010, ROADMAP P3.1/P3.2)., Providers join this onto a path, so it must not be able to leave the workdir.…, The constraint must not reject what `PLAN.md` §6 and the test suites really use., A filename has a length limit even when every character is safe., `extra="forbid"` stops a caller asserting health that the checks contradict., A request is a value; mutating one after dispatch would desync it from its key., _request() (+5 more)

### Community 54 - "Community 54"
Cohesion: 0.22
Nodes (8): BaseSettings, PydanticBaseSettingsSource, default_data_dir(), default_state_dir(), Path, Effective configuration for one invocation: defaults, then file, then…, Default source order, with the environment source filtered of secrets.…, Settings

### Community 55 - "Community 55"
Cohesion: 0.18
Nodes (12): ProviderFactory, ProviderRegistryError, Provider discovery failed: duplicate key, or a plugin that will not load., Image providers: concrete `core.providers.ImageProvider` implementations and…, _discover(), get(), keys(), ImageProvider (+4 more)

### Community 56 - "Community 56"
Cohesion: 0.22
Nodes (12): get_engine(), Format a SQLite connection URL for SQLAlchemy., Create a SQLAlchemy engine configured for thumbforge SQLite usage., sqlite_url(), get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output. (+4 more)

### Community 57 - "Community 57"
Cohesion: 0.29
Nodes (12): init_db(), Ensure directory exists and upgrade DB to head. Returns: Tuple of…, Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_get_db_status_nonexistent_and_initialized(), test_init_db_and_idempotence(), test_session_scope_commits_on_success() (+4 more)

### Community 58 - "Community 58"
Cohesion: 0.17
Nodes (9): Extractor, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes…, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch., test_permanent_failures_are_not_retried() (+1 more)

### Community 59 - "Community 59"
Cohesion: 0.17
Nodes (8): hashlib, Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 60 - "Community 60"
Cohesion: 0.23
Nodes (12): list_(), Argument, command, Context, handle_errors, help, Option, List stored videos, most recently fetched first. (+4 more)

### Community 61 - "Community 61"
Cohesion: 0.21
Nodes (11): A supplied URL or identifier is not recognisable YouTube input., UrlError, What a URL or bare identifier turned out to be (ADR 0005)., ResolvedUrl, _channel_handle(), classify_id(), _expect_kind(), UrlKind (+3 more)

### Community 62 - "Community 62"
Cohesion: 0.20
Nodes (12): _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`., A full extract must carry the fields a flat entry cannot (S11). Also the only…, Re-assert the S11 field set, so a yt-dlp upgrade that changes it fails loudly. (+4 more)

### Community 63 - "Community 63"
Cohesion: 0.21
Nodes (8): ChannelRepository, Channel, ChannelMeta, Persist a channel on its own (a channel URL was fetched)., Channel rows, keyed by YouTube channel id., Return the row for a YouTube channel id, or `None`., Insert or refresh a channel, preserving its ULID., Every channel, newest fetch first.

### Community 64 - "Community 64"
Cohesion: 0.20
Nodes (9): datetime, _iso(), Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).…, When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, One item's `part_number` before and after a `playlist renumber`. Captured per…, Render an aware datetime as the ISO-8601 UTC string the schema stores., Renumbering, thumbforge_core_services_fetch (+1 more)

### Community 65 - "Community 65"
Cohesion: 0.22
Nodes (9): EnvSettingsSource, _deep_merge(), _drop_secrets(), Any, Environment source that drops secret-looking variables before validation. The…, Recursively remove secret-looking keys, and any section left empty by their…, Build settings where the environment outranks the TOML file. File values cannot…, Merge ``override`` into ``base``, recursing into nested tables. (+1 more)

### Community 66 - "Community 66"
Cohesion: 0.22
Nodes (8): datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Default for `fetched_at`: an aware UTC instant, never a naive local one., Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC., _utcnow(), Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1). Pure…, thumbforge_core_enums, urllib_parse

### Community 67 - "Community 67"
Cohesion: 0.22
Nodes (9): GenerationRequest, GenerationResult, Path, One image to generate. Providers ignore what their capabilities disclaim., A produced image and the provenance needed to reproduce or audit it.…, Produce one image, or raise a `ProviderError` subclass. `workdir` is a caller-…, _digest(), Render one deterministic PNG into `workdir`. Raises before doing any work when… (+1 more)

### Community 68 - "Community 68"
Cohesion: 0.18
Nodes (5): What persisting a playlist actually wrote. Returned instead of the ORM row…, StoredPlaylist, ChannelMeta, PlaylistMeta, VideoMeta

### Community 69 - "Community 69"
Cohesion: 0.20
Nodes (9): FakeStore, DateTime, A single video can afford the channel request, which populates…, One playlist request plus one channel request, regardless of item count., Channel-wide enumeration is a Phase 2 non-goal., The `FetchStore` surface, recording what was written., test_channel_url_does_not_enumerate_videos(), test_playlist_url_fetches_playlist_then_its_owner() (+1 more)

### Community 70 - "Community 70"
Cohesion: 0.22
Nodes (8): Image, ProviderPermanentError, The provider failed in a way that retrying cannot fix., _contrasting(), Path, Paint the image. Pure function of `request` and `digest`, so output is stable., Paste one reference thumbnail into a corner, clockwise from top-left. A missing…, Black on light backgrounds, white on dark, so the digest text is always legible.

### Community 71 - "Community 71"
Cohesion: 0.24
Nodes (10): A metadata source failed for a reason worth retrying (network, throttling).…, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs., test_retry_emits_a_log_event(), failing() (+2 more)

### Community 72 - "Community 72"
Cohesion: 0.22
Nodes (8): Check, HealthReport, One named healthcheck outcome, with enough detail to act on a failure., The result of `provider check`: every check, not just the first failure. `ok`…, True when every check passed., Always healthy, and says why, so `provider check` output is never blank., `ok` is derived, so a report cannot claim health while carrying a failure., test_health_report_ok_cannot_disagree_with_its_checks()

### Community 73 - "Community 73"
Cohesion: 0.22
Nodes (9): dir_okay, exists, readable, Context, handle_errors, help, Path, Validate a template layout spec against the schema. (+1 more)

### Community 74 - "Community 74"
Cohesion: 0.22
Nodes (8): logging_handlers, bind(), clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Bind context onto every subsequent log record in this task (run id, provider,…, Drop all bound context., structlog, structlog_stdlib

### Community 75 - "Community 75"
Cohesion: 0.22
Nodes (7): Process, Kill a child and collect it, tolerating one that has already exited. The exit…, _reap(), The kill can land after the child has gone, and that must not mask the timeout.…, The spec's acceptance criterion: after a timeout the child is gone. Uses a real…, test_reap_actually_kills_a_running_child(), test_reap_tolerates_a_child_that_already_exited()

### Community 76 - "Community 76"
Cohesion: 0.22
Nodes (7): MonkeyPatch, The real subprocess path, which the injected runner bypasses everywhere else.…, An unanswered call is no evidence about credentials. Reported as `auth` it…, A non-zero exit from `agy models` is the one signal that the CLI is not signed…, test_a_clean_models_failure_is_an_auth_failure(), test_a_hung_child_is_killed_and_reported_as_a_timeout(), test_a_models_timeout_is_not_reported_as_an_auth_failure()

### Community 77 - "Community 77"
Cohesion: 0.29
Nodes (7): re, declarations(), main(), Path, Compare a committed graphify graph against a freshly extracted one. Only…, Ids of the nodes graphify parsed out of a file in this repository., Report whether the committed graph still describes the current declarations.

### Community 78 - "Community 78"
Cohesion: 0.25
Nodes (3): Path, Unit tests for ``thumbforge template`` CLI commands (ROADMAP P4.1, phase-4…, test_template_validate_nonexistent_file()

### Community 79 - "Community 79"
Cohesion: 0.25
Nodes (8): MonkeyPatch, parametrize, A generated config must contain defaults, not whatever the current shell…, A valid env override must not let an invalid assignment be written to disk., The documented way to supply a provider key must not brick every command. ADR…, test_a_provider_api_key_in_the_environment_does_not_break_loading(), test_environment_cannot_mask_an_invalid_file_value(), test_init_defaults_ignore_the_environment()

### Community 80 - "Community 80"
Cohesion: 0.29
Nodes (5): Protocol, ImageProvider, Generate one image per call. Implementations live in `providers/`., What this provider supports; callers check before sending a request., Every check this provider can run, with actionable detail on each failure.

### Community 81 - "Community 81"
Cohesion: 0.38
Nodes (3): Session, Build the three repositories over one session, so they share a transaction., Bind to the caller's session; the service owns the transaction.

### Community 82 - "Community 82"
Cohesion: 0.33
Nodes (4): ProviderInfo, Identity and auth state. Must not raise for a merely unauthenticated provider., Identity and auth state, for `provider list`., Always authenticated: there is nothing to authenticate against.

### Community 83 - "Community 83"
Cohesion: 0.40
Nodes (3): field_validator, Refuse a key that is only dots, which the character class alone would allow., ValidationInfo

### Community 84 - "Community 84"
Cohesion: 0.30
Nodes (3): JsonValue, Accept a config mapping for registry symmetry; nothing in it is required., Deliberately permissive, so callers exercise their full request-building path.

### Community 85 - "Community 85"
Cohesion: 0.40
Nodes (5): _aspect_words(), Describe the requested shape in words the image tool responds to. 16:9 is named…, parametrize, S3: the ratio words are the only lever on output size, so they must be right., test_aspect_is_described_in_words()

### Community 86 - "Community 86"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 87 - "Community 87"
Cohesion: 0.50
Nodes (4): Connection, ConnectionPoolEntry, Apply PRAGMA statements required by ADR 0004 on every SQLite connection., _set_sqlite_pragmas()

### Community 88 - "Community 88"
Cohesion: 0.67
Nodes (4): NotFoundError, A referenced entity does not exist., test_hint_and_code_reach_stderr(), boom()

### Community 89 - "Community 89"
Cohesion: 0.50
Nodes (3): DbStatus, Whether the database is fully migrated to the latest revision., Migration status and storage health metadata.

### Community 90 - "Community 90"
Cohesion: 0.50
Nodes (3): PlaylistMeta, Persist a playlist, its owning channel, its videos and its item order. Reports…, StoredPlaylist

### Community 91 - "Community 91"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

### Community 92 - "Community 92"
Cohesion: 0.67
Nodes (3): ImageProvider, The capability flags worth seeing in a one-line table cell., _summarise()

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 848 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `fetch()` connect `Community 45` to `Community 36`, `Community 37`, `Community 10`, `Community 18`, `Community 50`, `Community 25`, `Community 31`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `show()` connect `Community 18` to `Community 25`, `Community 50`, `Community 31`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Why does `emit()` connect `Community 50` to `Community 73`, `Community 10`, `Community 45`, `Community 18`, `Community 20`, `Community 24`, `Community 25`, `Community 60`, `Community 29`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `emit()` (e.g. with `check()` and `list_()`) actually correct?**
  _`emit()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05314685314685315 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.05727644652250146 - nodes in this community are weakly interconnected._