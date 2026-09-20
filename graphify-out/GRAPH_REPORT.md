# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1656 nodes · 3311 edges · 121 communities (80 shown, 41 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 284 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d503504a`
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

## God Nodes (most connected - your core abstractions)
1. `emit()` - 33 edges
2. `load_settings()` - 27 edges
3. `Repositories` - 25 edges
4. `StubSource` - 24 edges
5. `FakeProvider` - 24 edges
6. `get_engine()` - 22 edges
7. `AntigravityProvider` - 21 edges
8. `AssetStore` - 21 edges
9. `YtDlpSource` - 20 edges
10. `AssetKind` - 20 edges

## Surprising Connections (you probably didn't know these)
- `stub()` --indirect_call--> `models()`  [INFERRED]
  tests/unit/test_cli_provider.py → src/thumbforge/cli/provider.py
- `repeating()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_cli_fetch.py → src/thumbforge/core/models.py
- `test_item_count_tracks_items()` --uses--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_core_models.py → src/thumbforge/core/models.py
- `test_playlist_position_is_one_based()` --uses--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_core_models.py → src/thumbforge/core/models.py
- `_playlist()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_repositories.py → src/thumbforge/core/models.py

## Import Cycles
- None detected.

## Communities (121 total, 41 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): ProviderCapabilities, ProviderInfo, AntigravityProvider, _parse_models(), HealthReport, Generate an image by driving `agy` in headless mode., Measured in spikes S3, S4 and S7 — see the module docstring., Report the CLI version, and auth as `unknown` rather than guessing. `unknown`… (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (58): MonkeyPatch, PlaylistItemMeta, One video's place in a playlist., data_dir(), ChannelMeta, fixture, Path, PlaylistMeta (+50 more)

### Community 2 - "Community 2"
Cohesion: 0.10
Nodes (45): DeclarativeBase, enum, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations., Origin of channel metadata. (+37 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (47): The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Repositories, _channel(), _playlist(), ChannelMeta, PlaylistMeta, VideoMeta, Upsert semantics the rest of Phase 2 depends on (ROADMAP P2.3, PLAN.md §3). (+39 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (32): dataclasses, functools, IntEnum, rich_console, rich_panel, rich_table, Settings, main() (+24 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (33): json, declarations(), main(), Path, Compare a committed graphify graph against a freshly extracted one. Only…, Ids of the nodes graphify parsed out of a file in this repository., Report whether the committed graph still describes the current declarations., Path (+25 more)

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (35): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, asset_store() (+27 more)

### Community 7 - "Community 7"
Cohesion: 0.08
Nodes (34): _fixture(), Any, `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from. (+26 more)

### Community 8 - "Community 8"
Cohesion: 0.09
Nodes (34): Argument, Console, metavar, rich_syntax, _as_toml(), _config_path(), init_(), path_() (+26 more)

### Community 9 - "Community 9"
Cohesion: 0.13
Nodes (32): Config, DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., _alembic_config(), get_db_status(), get_engine(), init_db(), Path (+24 more)

### Community 10 - "Community 10"
Cohesion: 0.09
Nodes (28): contextlib, RawInfo, RetryCallState, _duration(), _log_retry(), _published_at(), ChannelMeta, datetime (+20 more)

### Community 11 - "Community 11"
Cohesion: 0.09
Nodes (32): FixtureRequest, shutil, provider(), _provider_params(), Any, fixture, GenerationRequest, ImageProvider (+24 more)

### Community 12 - "Community 12"
Cohesion: 0.06
Nodes (29): entries(), _Entry, fixture, MonkeyPatch, A plugin needs only an entry point: the registry never imports it by name., Providers should not each have to handle `None`., `provider list` output must not reorder between runs., Shadowing a provider would make `--provider x` mean different things per… (+21 more)

### Community 13 - "Community 13"
Cohesion: 0.11
Nodes (29): asyncio, pil, `FakeProvider` — deterministic, offline image generation (PLAN.md §4.2, ROADMAP…, parametrize, Path, `FakeProvider` behaviour the generic contract cannot express (PLAN.md §4.2,…, A test asserting style anchoring needs to see the reference in the output., Callers pass a run-scoped directory that may not exist yet. (+21 more)

### Community 14 - "Community 14"
Cohesion: 0.12
Nodes (29): Channel, Playlist, PlaylistItem, list_(), Argument, command, Context, handle_errors (+21 more)

### Community 15 - "Community 15"
Cohesion: 0.09
Nodes (26): pydantic, datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Default for `fetched_at`: an aware UTC instant, never a naive local one., _utcnow(), Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)., `resolve()` returns both halves (ADR 0005); an empty id is never a valid result., A minimal valid video, so each test states only the field it is about. (+18 more)

### Community 16 - "Community 16"
Cohesion: 0.09
Nodes (21): alembic, alembic_config, alembic_runtime_migration, alembic_script, Connection, ConnectionPoolEntry, sqlalchemy, sqlalchemy_orm (+13 more)

### Community 17 - "Community 17"
Cohesion: 0.16
Nodes (26): BoundLogger, CaptureFixture, LogFormat, configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``., Configure structlog and the stdlib root logger. Safe to call more than once. (+18 more)

### Community 18 - "Community 18"
Cohesion: 0.10
Nodes (21): os, pathlib, sqlalchemy_exc, new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of ``data``. (+13 more)

### Community 19 - "Community 19"
Cohesion: 0.10
Nodes (23): parametrize, ResolvedUrl, classify_url(), Resolve a YouTube URL, handle or bare id to its kind and identifier. A `watch`…, ResolvedUrl, Classify input without touching the network; `core.urls` does the work., ResolvedUrl, UrlKind (+15 more)

### Community 20 - "Community 20"
Cohesion: 0.17
Nodes (26): default_config_path(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., Spike S5 superseded decision D4: the dangerous flag is not opted into by…, The secret filter must not swallow ordinary nested provider settings. (+18 more)

### Community 21 - "Community 21"
Cohesion: 0.13
Nodes (25): command, Context, handle_errors, ImageProvider, _KEY_ARGUMENT, check(), _config(), list_() (+17 more)

### Community 22 - "Community 22"
Cohesion: 0.12
Nodes (23): re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 23 - "Community 23"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, Yield `exc` and its `cause` links; `ExtractorError` nests the real failure… (+16 more)

### Community 24 - "Community 24"
Cohesion: 0.12
Nodes (17): Collection, NotFoundError, A referenced entity does not exist., PlaylistRepository, Playlist, PlaylistItem, PlaylistMeta, Playlist rows and their ordered items. (+9 more)

### Community 25 - "Community 25"
Cohesion: 0.12
Nodes (21): `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, FakeSource, `FetchService` decisions: kind dispatch, the freshness rule, and what each…, If the fake drifts from `MetadataSource`, these tests stop meaning anything., A single video can afford the channel request, which populates…, Channel-wide enumeration is a Phase 2 non-goal., Spec behaviour 2: a playlist fetched inside the window is not re-fetched., Just past the window the network call must happen again. (+13 more)

### Community 26 - "Community 26"
Cohesion: 0.16
Nodes (17): collections_abc, MetadataSource, ``thumbforge fetch`` — pull YouTube metadata into the database (ROADMAP P2.3)., ``thumbforge provider`` — inspect providers and store their keys (ROADMAP P3.5)., build_source(), ChannelSource, Wiring and shared views for the YouTube metadata commands (ROADMAP P2.3).…, Select a metadata source. The Data API source is a Phase 8 extra, so asking for… (+9 more)

### Community 27 - "Community 27"
Cohesion: 0.13
Nodes (21): list_(), Argument, command, Context, handle_errors, help, Option, ``thumbforge video`` — list and inspect stored videos (ROADMAP P2.3). (+13 more)

### Community 28 - "Community 28"
Cohesion: 0.13
Nodes (20): Engine, integration, Session, sessionmaker, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the…, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., _reclaim_orphans() (+12 more)

### Community 29 - "Community 29"
Cohesion: 0.13
Nodes (16): Image, JsonValue, GenerationRequest, One image to generate. Providers ignore what their capabilities disclaim., _contrasting(), _digest(), FakeProvider, Path (+8 more)

### Community 30 - "Community 30"
Cohesion: 0.17
Nodes (19): Any, importlib_util, ModuleType, _declaration(), _graph(), _module(), Path, The drift check's node filter (issue #26). This is a CI gate, so a silently… (+11 more)

### Community 31 - "Community 31"
Cohesion: 0.11
Nodes (19): platformdirs, pydantic_settings, pydantic_settings_sources, BatchSettings, ConfigSchema, default_config_toml(), _format_validation_error(), GeneralSettings (+11 more)

### Community 32 - "Community 32"
Cohesion: 0.10
Nodes (15): GenerationRequest, GenerationResult, HealthReport, JsonValue, Path, ProviderCapabilities, ProviderInfo, If the stub drifts from `ImageProvider`, every test here stops meaning anything. (+7 more)

### Community 33 - "Community 33"
Cohesion: 0.15
Nodes (19): min, P, R, init_(), path_(), command, Context, help (+11 more)

### Community 34 - "Community 34"
Cohesion: 0.15
Nodes (17): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError, Error hierarchy and the exit codes it maps to. Every failure the user can…, Base class for image-provider failures. (+9 more)

### Community 35 - "Community 35"
Cohesion: 0.16
Nodes (13): ChannelMeta, _Meta, PlaylistMeta, Shared configuration and provenance for every fetched snapshot., A fetched YouTube channel., A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, A fetched YouTube playlist and its ordered items., Number of items fetched, for the `playlist.item_count` column. (+5 more)

### Community 36 - "Community 36"
Cohesion: 0.12
Nodes (18): FetchResult, fetch(), Argument, ChannelSource, Context, handle_errors, help, JsonPayload (+10 more)

### Community 37 - "Community 37"
Cohesion: 0.14
Nodes (10): What persisting a playlist actually wrote. Returned instead of the ORM row…, StoredPlaylist, FakeStore, ChannelMeta, DateTime, PlaylistMeta, VideoMeta, A video fetch is one cheap request and always reflects the latest title. (+2 more)

### Community 38 - "Community 38"
Cohesion: 0.11
Nodes (15): Unit tests for ``thumbforge provider`` (ROADMAP P3.5, phase-3 spec Commands…, `fake` is healthy and offers nothing; that is a 0, not a failure., A typo must cost a message, not a typed-out secret., A stored empty string reads back as "no key" while occupying a credential entry., The variable that authenticates a provider follows pydantic-settings' nesting., No provider needs an API key yet, so the credential row is informational only., The JSON contract carries the full capability object, not the display summary., Exit 3, and the hint lists what is installed, because the cause is usually a… (+7 more)

### Community 39 - "Community 39"
Cohesion: 0.15
Nodes (14): GenerationResult, _aspect_words(), GenerationRequest, Path, Build the prompt sent to `agy -p`. The aspect ratio is given in words because…, Describe the requested shape in words the image tool responds to. 16:9 is named…, Run one generation and copy its output into `workdir`., Assemble the command line. Never `--continue`: every image is a fresh run. (+6 more)

### Community 40 - "Community 40"
Cohesion: 0.12
Nodes (16): callback, count, help, is_eager, Option, Context, handle_errors, Path (+8 more)

### Community 41 - "Community 41"
Cohesion: 0.17
Nodes (14): CliRunner, _as_int(), _as_str(), _cost(), _installed_plugins(), JsonValue, `AntigravityProvider` — drives the Antigravity CLI headlessly (ADR 0013,…, Read the provider's own config slice; `run` is injected by tests only. `run`… (+6 more)

### Community 42 - "Community 42"
Cohesion: 0.15
Nodes (12): decimal, Protocol, GenerationResult, ImageProvider, ProviderInfo, Path, The `ImageProvider` Protocol and the values that cross it (ADR 0010, ROADMAP…, A produced image and the provenance needed to reproduce or audit it.… (+4 more)

### Community 43 - "Community 43"
Cohesion: 0.18
Nodes (9): FetchResult, ResolvedUrl, Playlist rows written., Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order., A channel on its own; enumerating its videos is a Phase 2 non-goal., What was fetched, for rendering and for the `--json` contract. Counts are of… (+1 more)

### Community 44 - "Community 44"
Cohesion: 0.16
Nodes (10): ChannelRepository, Channel, ChannelMeta, Persist a playlist, its owning channel, its videos and its item order. Reports…, Persist a channel on its own (a channel URL was fetched)., Channel rows, keyed by YouTube channel id., Return the row for a YouTube channel id, or `None`., Insert or refresh a channel, preserving its ULID. (+2 more)

### Community 45 - "Community 45"
Cohesion: 0.15
Nodes (11): importlib_metadata, logging_handlers, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, bind(), clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Bind context onto every subsequent log record in this task (run id, provider,…, Drop all bound context. (+3 more)

### Community 46 - "Community 46"
Cohesion: 0.21
Nodes (13): keyring, keyring_errors, api_key(), describe(), env_var(), _from_env(), Provider API keys: read from the environment or the system keyring (ROADMAP…, The environment variable this provider's key is read from. Mirrors pydantic-… (+5 more)

### Community 47 - "Community 47"
Cohesion: 0.15
Nodes (10): PartialBatchError, Exception, A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., TemplateError, ThumbforgeError, parametrize (+2 more)

### Community 48 - "Community 48"
Cohesion: 0.19
Nodes (14): Configuration is missing, malformed, or contains something it must not., SettingsError, _atomic_write(), _parse_scalar(), Replace ``path`` atomically: write a sibling temp file, fsync, then rename. A…, Write the commented default configuration, refusing to clobber unless ``force``., Apply several dotted keys to the TOML file, validating the result once. All…, Parse a CLI value using TOML scalar rules, falling back to a bare string.… (+6 more)

### Community 49 - "Community 49"
Cohesion: 0.16
Nodes (10): FetchStore, ChannelMeta, datetime, PlaylistMeta, VideoMeta, The persistence surface a fetch needs, satisfied by `storage.Repositories`., Persist one video, and its channel when the caller fetched one., Persist a playlist, its owner, its videos and its order. (+2 more)

### Community 50 - "Community 50"
Cohesion: 0.20
Nodes (13): _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, Record `tests/fixtures/ytdlp/*.json` from live YouTube, and assert the S11…, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`., A full extract must carry the fields a flat entry cannot (S11). Also the only… (+5 more)

### Community 51 - "Community 51"
Cohesion: 0.19
Nodes (9): Video, VideoMeta, Look a video up by ULID or YouTube id, raising `NotFoundError` if absent. Both…, Insert or refresh a video, preserving its ULID. `channel_row_id` is supplied…, Videos, newest fetch first, optionally restricted to one channel., Persist one video and, when known, its channel. A single-video fetch can afford…, Video rows, keyed by YouTube video id., Return the row for a YouTube video id, or `None`. (+1 more)

### Community 52 - "Community 52"
Cohesion: 0.20
Nodes (13): parametrize, Invariants the provider boundary models enforce (ADR 0010, ROADMAP P3.1/P3.2)., Providers join this onto a path, so it must not be able to leave the workdir.…, The constraint must not reject what `PLAN.md` §6 and the test suites really use., A filename has a length limit even when every character is safe., `extra="forbid"` stops a caller asserting health that the checks contradict., A request is a value; mutating one after dispatch would desync it from its key., _request() (+5 more)

### Community 53 - "Community 53"
Cohesion: 0.22
Nodes (8): BaseSettings, PydanticBaseSettingsSource, default_data_dir(), default_state_dir(), Path, Effective configuration for one invocation: defaults, then file, then…, Default source order, with the environment source filtered of secrets.…, Settings

### Community 54 - "Community 54"
Cohesion: 0.17
Nodes (12): Check, _healthcheck(), stub(), HealthReport, Both exit 4, but the machine-readable code is what tells the user where to look., "No models" and "not signed in" look identical in output and must not be…, A stand-in `AntigravityProvider.healthcheck` returning a fixed report., A failing check must not hide the passing ones: the table is printed, then the… (+4 more)

### Community 55 - "Community 55"
Cohesion: 0.17
Nodes (9): Extractor, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes…, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch., test_permanent_failures_are_not_retried() (+1 more)

### Community 56 - "Community 56"
Cohesion: 0.17
Nodes (8): hashlib, Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 57 - "Community 57"
Cohesion: 0.21
Nodes (11): A supplied URL or identifier is not recognisable YouTube input., UrlError, _channel_handle(), classify_id(), _expect_kind(), UrlKind, Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1). Pure…, Classify a bare YouTube identifier by its shape. Order matters: a channel id… (+3 more)

### Community 58 - "Community 58"
Cohesion: 0.20
Nodes (12): A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs. (+4 more)

### Community 59 - "Community 59"
Cohesion: 0.18
Nodes (9): Check, HealthReport, Every check this provider can run, with actionable detail on each failure., One named healthcheck outcome, with enough detail to act on a failure., The result of `provider check`: every check, not just the first failure. `ok`…, True when every check passed., Always healthy, and says why, so `provider check` output is never blank., `ok` is derived, so a report cannot claim health while carrying a failure. (+1 more)

### Community 60 - "Community 60"
Cohesion: 0.17
Nodes (10): FetchService, MetadataSource, Fetch YouTube metadata and persist it., Take the metadata source and persistence layer the CLI selected., Whether a stored playlist is recent enough to skip the network., One playlist request plus one channel request, regardless of item count., `fetch` tells the user a re-fetch shrank the playlist., test_playlist_url_fetches_playlist_then_its_owner() (+2 more)

### Community 61 - "Community 61"
Cohesion: 0.18
Nodes (10): BaseModel, model_validator, Self, Cost, What one generation consumed. `credits`/`currency` are optional because a…, AntigravitySettings, OutputSettings, ProviderSettings (+2 more)

### Community 62 - "Community 62"
Cohesion: 0.20
Nodes (9): datetime, _iso(), Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).…, When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, One item's `part_number` before and after a `playlist renumber`. Captured per…, Render an aware datetime as the ISO-8601 UTC string the schema stores., Renumbering, thumbforge_core_services_fetch (+1 more)

### Community 63 - "Community 63"
Cohesion: 0.22
Nodes (9): EnvSettingsSource, _deep_merge(), _drop_secrets(), Any, Environment source that drops secret-looking variables before validation. The…, Recursively remove secret-looking keys, and any section left empty by their…, Build settings where the environment outranks the TOML file. File values cannot…, Merge ``override`` into ``base``, recursing into nested tables. (+1 more)

### Community 64 - "Community 64"
Cohesion: 0.20
Nodes (10): ProviderFactory, Image providers: concrete `core.providers.ImageProvider` implementations and…, _discover(), get(), keys(), ImageProvider, JsonValue, Instantiate the provider registered under `key`. An unknown key raises… (+2 more)

### Community 65 - "Community 65"
Cohesion: 0.20
Nodes (10): MonkeyPatch, parametrize, `PLAN.md` §8 lookup order: the environment variable wins., An exported-but-empty variable is how shells leave unset values; it must not…, ADR 0014: a backend that stores nothing must be distinguishable from an empty…, The variable name is useful; its value is not, and must not be echoed., test_a_blank_environment_variable_falls_through_to_the_keyring(), test_check_names_the_keyring_backend_without_printing_the_key() (+2 more)

### Community 66 - "Community 66"
Cohesion: 0.28
Nodes (9): JsonPayload, ProviderPermanentError, The provider failed in a way that retrying cannot fix., _looks_like_timeout(), _parse_envelope(), _raise_for_envelope(), Read the single JSON envelope, or explain why there isn't one., Whether a `SUCCESS` envelope is really agy's print timeout. S6c measured the… (+1 more)

### Community 67 - "Community 67"
Cohesion: 0.22
Nodes (7): Process, Kill a child and collect it, tolerating one that has already exited. The exit…, _reap(), The kill can land after the child has gone, and that must not mask the timeout.…, The spec's acceptance criterion: after a timeout the child is gone. Uses a real…, test_reap_actually_kills_a_running_child(), test_reap_tolerates_a_child_that_already_exited()

### Community 68 - "Community 68"
Cohesion: 0.32
Nodes (7): get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline(), run_migrations_online()

### Community 69 - "Community 69"
Cohesion: 0.25
Nodes (8): MonkeyPatch, parametrize, A generated config must contain defaults, not whatever the current shell…, A valid env override must not let an invalid assignment be written to disk., The documented way to supply a provider key must not brick every command. ADR…, test_a_provider_api_key_in_the_environment_does_not_break_loading(), test_environment_cannot_mask_an_invalid_file_value(), test_init_defaults_ignore_the_environment()

### Community 70 - "Community 70"
Cohesion: 0.38
Nodes (3): Session, Build the three repositories over one session, so they share a transaction., Bind to the caller's session; the service owns the transaction.

### Community 71 - "Community 71"
Cohesion: 0.40
Nodes (6): ComplianceError, A generated image violates the YouTube thumbnail requirements., Machine mode contract: stdout carries command output, stderr carries the…, test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), boom(), root()

### Community 72 - "Community 72"
Cohesion: 0.33
Nodes (4): ProviderCapabilities, What this provider supports; callers check before sending a request., What a provider can actually do, so callers degrade instead of guessing., Deliberately permissive, so callers exercise their full request-building path.

### Community 73 - "Community 73"
Cohesion: 0.33
Nodes (5): Reading is a question, not a demand: a CI runner has no backend at all., Writing is a demand, and the hint has to name the fallback that needs no…, test_an_unusable_keyring_is_fatal_when_storing(), test_an_unusable_keyring_reports_no_key_rather_than_failing(), explode()

### Community 74 - "Community 74"
Cohesion: 0.40
Nodes (3): field_validator, Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC., Refuse a key that is only dots, which the character class alone would allow.

### Community 75 - "Community 75"
Cohesion: 0.40
Nodes (3): fixture, _no_real_keyring(), Replace the OS credential store with a dict for the whole module.

### Community 76 - "Community 76"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 77 - "Community 77"
Cohesion: 0.50
Nodes (3): pytest, testcontainers_core_container, Integration tests using Testcontainers for database verification (ADR 0004).

### Community 78 - "Community 78"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

### Community 79 - "Community 79"
Cohesion: 0.67
Nodes (3): Path, `providers.antigravity.*` must actually configure the instance `provider list`…, test_provider_settings_reach_the_provider()

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 808 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **41 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ThumbforgeError` connect `Community 47` to `Community 33`, `Community 34`, `Community 4`, `Community 6`, `Community 71`, `Community 9`, `Community 48`, `Community 24`, `Community 57`, `Community 58`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `handle_errors()` connect `Community 33` to `Community 8`, `Community 4`, `Community 47`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `SettingsError` connect `Community 48` to `Community 34`, `Community 4`, `Community 8`, `Community 47`, `Community 20`, `Community 21`, `Community 26`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `emit()` (e.g. with `check()` and `list_()`) actually correct?**
  _`emit()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `Repositories` (e.g. with `repos()` and `test_duplicate_video_in_a_playlist_is_listed_once()`) actually correct?**
  _`Repositories` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.052100840336134456 - nodes in this community are weakly interconnected._