# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1637 nodes · 3282 edges · 116 communities (78 shown, 38 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 279 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bc7fde0c`
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

## God Nodes (most connected - your core abstractions)
1. `emit()` - 33 edges
2. `load_settings()` - 27 edges
3. `Repositories` - 25 edges
4. `FakeProvider` - 24 edges
5. `StubSource` - 24 edges
6. `get_engine()` - 22 edges
7. `AssetStore` - 21 edges
8. `YtDlpSource` - 20 edges
9. `AssetKind` - 20 edges
10. `get_app_context()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `repeating()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_cli_fetch.py → src/thumbforge/core/models.py
- `stub()` --indirect_call--> `models()`  [INFERRED]
  tests/unit/test_cli_provider.py → src/thumbforge/cli/provider.py
- `_request()` --uses--> `GenerationRequest`  [INFERRED]
  tests/unit/test_core_providers.py → src/thumbforge/core/providers.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `_json_context()` --uses--> `AppContext`  [INFERRED]
  tests/unit/test_render.py → src/thumbforge/cli/_render.py

## Import Cycles
- None detected.

## Communities (116 total, 38 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (51): Image, JsonValue, Protocol, GenerationRequest, GenerationResult, ImageProvider, Path, One image to generate. Providers ignore what their capabilities disclaim. (+43 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (56): MonkeyPatch, data_dir(), ChannelMeta, fixture, Path, VideoMeta, `fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP…, An initialised database, since every command here needs the schema. (+48 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (54): _envelope(), _plant_image(), _provider(), Any, GenerationRequest, MonkeyPatch, parametrize, Path (+46 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (48): command, importlib_metadata, _KEY_ARGUMENT, keyring, keyring_errors, ProviderFactory, check(), _config() (+40 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (49): Engine, integration, DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., get_db_status(), get_engine(), init_db(), Path (+41 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (48): Argument, metavar, min, P, R, rich_syntax, _as_toml(), _config_path() (+40 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (45): DeclarativeBase, enum, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations., Origin of channel metadata. (+37 more)

### Community 7 - "Community 7"
Cohesion: 0.07
Nodes (48): PlaylistItemMeta, One video's place in a playlist., The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Repositories, PlaylistMeta, _channel(), _playlist(), ChannelMeta (+40 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (35): asyncio, collections_abc, dataclasses, pathlib, rich_console, rich_panel, rich_table, main() (+27 more)

### Community 9 - "Community 9"
Cohesion: 0.11
Nodes (35): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, asset_store() (+27 more)

### Community 10 - "Community 10"
Cohesion: 0.09
Nodes (34): FixtureRequest, pil, shutil, provider(), _provider_params(), Any, fixture, GenerationRequest (+26 more)

### Community 11 - "Community 11"
Cohesion: 0.10
Nodes (34): Playlist, list_(), Argument, command, Context, handle_errors, help, Option (+26 more)

### Community 12 - "Community 12"
Cohesion: 0.06
Nodes (29): entries(), _Entry, fixture, MonkeyPatch, A plugin needs only an entry point: the registry never imports it by name., Providers should not each have to handle `None`., `provider list` output must not reorder between runs., Shadowing a provider would make `--provider x` mean different things per… (+21 more)

### Community 13 - "Community 13"
Cohesion: 0.10
Nodes (26): RawInfo, RetryCallState, _duration(), _log_retry(), _published_at(), ChannelMeta, datetime, PlaylistMeta (+18 more)

### Community 14 - "Community 14"
Cohesion: 0.08
Nodes (24): alembic, alembic_config, alembic_runtime_migration, alembic_script, Config, Connection, ConnectionPoolEntry, contextlib (+16 more)

### Community 15 - "Community 15"
Cohesion: 0.10
Nodes (26): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+18 more)

### Community 16 - "Community 16"
Cohesion: 0.09
Nodes (27): BaseModel, model_validator, platformdirs, pydantic_settings, pydantic_settings_sources, Self, AntigravitySettings, BatchSettings (+19 more)

### Community 17 - "Community 17"
Cohesion: 0.11
Nodes (26): Any, importlib_util, ModuleType, declarations(), main(), Path, Compare a committed graphify graph against a freshly extracted one. Only…, Ids of the nodes graphify parsed out of a file in this repository. (+18 more)

### Community 18 - "Community 18"
Cohesion: 0.09
Nodes (22): os, sqlalchemy_exc, sqlalchemy_orm, new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of ``data``. (+14 more)

### Community 19 - "Community 19"
Cohesion: 0.16
Nodes (26): BoundLogger, CaptureFixture, LogFormat, configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``., Configure structlog and the stdlib root logger. Safe to call more than once. (+18 more)

### Community 20 - "Community 20"
Cohesion: 0.10
Nodes (23): parametrize, ResolvedUrl, classify_url(), Resolve a YouTube URL, handle or bare id to its kind and identifier. A `watch`…, ResolvedUrl, Classify input without touching the network; `core.urls` does the work., ResolvedUrl, UrlKind (+15 more)

### Community 21 - "Community 21"
Cohesion: 0.11
Nodes (23): functools, IntEnum, Settings, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.… (+15 more)

### Community 22 - "Community 22"
Cohesion: 0.12
Nodes (23): re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 23 - "Community 23"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, Yield `exc` and its `cause` links; `ExtractorError` nests the real failure… (+16 more)

### Community 24 - "Community 24"
Cohesion: 0.19
Nodes (23): Apply several dotted keys to the TOML file, validating the result once. All…, set_values(), Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., A valid env override must not let an invalid assignment be written to disk., Write a config file and return its path, so tests read as one expression., test_data_dir_flag_overrides_everything() (+15 more)

### Community 25 - "Community 25"
Cohesion: 0.10
Nodes (22): pydantic, Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)., `resolve()` returns both halves (ADR 0005); an empty id is never a valid result., A minimal valid video, so each test states only the field it is about., A fetched snapshot is a value; mutating one would desync it from `fetched_at`., `extra="forbid"` turns an unexpected yt-dlp field into a loud failure. yt-dlp's…, `fetched_at` is persisted as ISO-8601 UTC, so a naive datetime is ambiguous., Offsets are preserved as an instant, then stored in UTC. (+14 more)

### Community 26 - "Community 26"
Cohesion: 0.12
Nodes (20): `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, FakeSource, `FetchService` decisions: kind dispatch, the freshness rule, and what each…, If the fake drifts from `MetadataSource`, these tests stop meaning anything., Spec behaviour 2: a playlist fetched inside the window is not re-fetched., Just past the window the network call must happen again., `--refresh` must win even one second after a fetch., A video fetch is one cheap request and always reflects the latest title. (+12 more)

### Community 27 - "Community 27"
Cohesion: 0.11
Nodes (15): Console, json, pytest, testcontainers_core_container, Shared fixtures. Establishes ``tests/`` as the pytest root., Integration tests using Testcontainers for database verification (ADR 0004)., Record `tests/fixtures/ytdlp/*.json` from live YouTube, and assert the S11…, The exit-code contract: a script parsing our status codes must never be… (+7 more)

### Community 28 - "Community 28"
Cohesion: 0.12
Nodes (15): AntigravityProvider, _installed_plugins(), _parse_models(), HealthReport, ProviderCapabilities, ProviderInfo, Generate an image by driving `agy` in headless mode., Measured in spikes S3, S4 and S7 — see the module docstring. (+7 more)

### Community 29 - "Community 29"
Cohesion: 0.10
Nodes (15): GenerationRequest, GenerationResult, HealthReport, JsonValue, Path, ProviderCapabilities, ProviderInfo, If the stub drifts from `ImageProvider`, every test here stops meaning anything. (+7 more)

### Community 30 - "Community 30"
Cohesion: 0.13
Nodes (19): `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., A source wired to a fixture, plus the recorder that captured its calls., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get…, `position` comes from enumeration order because `playlist_index` is absent… (+11 more)

### Community 31 - "Community 31"
Cohesion: 0.12
Nodes (19): Channel, PlaylistItem, JsonPayload, RenderableType, Repositories, Build the JSON payload and the Rich renderable from the **stored** rows.…, _view(), panel() (+11 more)

### Community 32 - "Community 32"
Cohesion: 0.16
Nodes (13): ChannelMeta, _Meta, PlaylistMeta, Shared configuration and provenance for every fetched snapshot., A fetched YouTube channel., A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, A fetched YouTube playlist and its ordered items., Number of items fetched, for the `playlist.item_count` column. (+5 more)

### Community 33 - "Community 33"
Cohesion: 0.16
Nodes (12): FetchResult, FetchService, ResolvedUrl, Playlist rows written., Fetch YouTube metadata and persist it., Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order. (+4 more)

### Community 34 - "Community 34"
Cohesion: 0.12
Nodes (13): FetchStore, ChannelMeta, datetime, MetadataSource, PlaylistMeta, VideoMeta, Take the metadata source and persistence layer the CLI selected., The persistence surface a fetch needs, satisfied by `storage.Repositories`. (+5 more)

### Community 35 - "Community 35"
Cohesion: 0.11
Nodes (15): Unit tests for ``thumbforge provider`` (ROADMAP P3.5, phase-3 spec Commands…, `fake` is healthy and offers nothing; that is a 0, not a failure., Spec behaviour 5: works for `fake` even though it ignores keys, so the path is…, A stored empty string reads back as "no key" while occupying a credential entry., The variable that authenticates a provider follows pydantic-settings' nesting., No provider needs an API key yet, so the credential row is informational only., The JSON contract carries the full capability object, not the display summary., Exit 3, and the hint lists what is installed, because the cause is usually a… (+7 more)

### Community 36 - "Community 36"
Cohesion: 0.16
Nodes (12): BaseSettings, PydanticBaseSettingsSource, _atomic_write(), default_data_dir(), default_state_dir(), Path, Effective configuration for one invocation: defaults, then file, then…, Default source order, with the environment source filtered of secrets.… (+4 more)

### Community 37 - "Community 37"
Cohesion: 0.13
Nodes (14): decimal, Check, HealthReport, ProviderCapabilities, ProviderInfo, The `ImageProvider` Protocol and the values that cross it (ADR 0010, ROADMAP…, What a provider can actually do, so callers degrade instead of guessing., Identity and auth state, for `provider list`. (+6 more)

### Community 38 - "Community 38"
Cohesion: 0.18
Nodes (16): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError, Error hierarchy and the exit codes it maps to. Every failure the user can… (+8 more)

### Community 39 - "Community 39"
Cohesion: 0.15
Nodes (15): _fixture(), Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Load one recorded yt-dlp info dict. (+7 more)

### Community 40 - "Community 40"
Cohesion: 0.12
Nodes (16): callback, count, help, is_eager, Option, Context, handle_errors, Path (+8 more)

### Community 41 - "Community 41"
Cohesion: 0.13
Nodes (15): FetchResult, MetadataSource, fetch(), Argument, ChannelSource, Context, handle_errors, help (+7 more)

### Community 42 - "Community 42"
Cohesion: 0.17
Nodes (13): _aspect_words(), GenerationRequest, GenerationResult, Path, Build the prompt sent to `agy -p`. The aspect ratio is given in words because…, Describe the requested shape in words the image tool responds to. 16:9 is named…, Run one generation and copy its output into `workdir`., Assemble the command line. Never `--continue`: every image is a fresh run. (+5 more)

### Community 43 - "Community 43"
Cohesion: 0.15
Nodes (10): PartialBatchError, Exception, A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., TemplateError, ThumbforgeError, parametrize (+2 more)

### Community 44 - "Community 44"
Cohesion: 0.19
Nodes (9): Video, VideoMeta, Look a video up by ULID or YouTube id, raising `NotFoundError` if absent. Both…, Insert or refresh a video, preserving its ULID. `channel_row_id` is supplied…, Videos, newest fetch first, optionally restricted to one channel., Persist one video and, when known, its channel. A single-video fetch can afford…, Video rows, keyed by YouTube video id., Return the row for a YouTube video id, or `None`. (+1 more)

### Community 45 - "Community 45"
Cohesion: 0.20
Nodes (13): parametrize, Invariants the provider boundary models enforce (ADR 0010, ROADMAP P3.1/P3.2)., Providers join this onto a path, so it must not be able to leave the workdir.…, The constraint must not reject what `PLAN.md` §6 and the test suites really use., A filename has a length limit even when every character is safe., `extra="forbid"` stops a caller asserting health that the checks contradict., A request is a value; mutating one after dispatch would desync it from its key., _request() (+5 more)

### Community 46 - "Community 46"
Cohesion: 0.24
Nodes (12): JsonPayload, _as_str(), _looks_like_timeout(), _parse_envelope(), _raise_for_envelope(), `AntigravityProvider` — drives the Antigravity CLI headlessly (ADR 0013,…, Read the single JSON envelope, or explain why there isn't one., Whether a `SUCCESS` envelope is really agy's print timeout. S6c measured the… (+4 more)

### Community 47 - "Community 47"
Cohesion: 0.19
Nodes (13): Configuration is missing, malformed, or contains something it must not., SettingsError, default_config_path(), _format_validation_error(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, _read_toml(), _reject_secrets() (+5 more)

### Community 48 - "Community 48"
Cohesion: 0.23
Nodes (8): PlaylistRepository, Playlist, Playlist rows and their ordered items., Return the row for a YouTube playlist id, or `None`., Look a playlist up by ULID or YouTube id, raising `NotFoundError` if absent., Insert or refresh a playlist. `channel_row_id` is required: the column is NOT…, Rewrite a playlist's items to exactly `video_ids`, in order. Rows are deleted…, Playlists, newest fetch first, optionally restricted to one channel.

### Community 49 - "Community 49"
Cohesion: 0.17
Nodes (12): Check, _healthcheck(), stub(), HealthReport, Both exit 4, but the machine-readable code is what tells the user where to look., "No models" and "not signed in" look identical in output and must not be…, A stand-in `AntigravityProvider.healthcheck` returning a fixed report., A failing check must not hide the passing ones: the table is printed, then the… (+4 more)

### Community 50 - "Community 50"
Cohesion: 0.17
Nodes (9): Extractor, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes…, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch., test_permanent_failures_are_not_retried() (+1 more)

### Community 51 - "Community 51"
Cohesion: 0.17
Nodes (8): hashlib, Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 52 - "Community 52"
Cohesion: 0.20
Nodes (12): A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs. (+4 more)

### Community 53 - "Community 53"
Cohesion: 0.20
Nodes (12): _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`., A full extract must carry the fields a flat entry cannot (S11). Also the only…, Re-assert the S11 field set, so a yt-dlp upgrade that changes it fails loudly. (+4 more)

### Community 54 - "Community 54"
Cohesion: 0.21
Nodes (8): ChannelRepository, Channel, ChannelMeta, Persist a channel on its own (a channel URL was fetched)., Channel rows, keyed by YouTube channel id., Return the row for a YouTube channel id, or `None`., Insert or refresh a channel, preserving its ULID., Every channel, newest fetch first.

### Community 55 - "Community 55"
Cohesion: 0.22
Nodes (9): EnvSettingsSource, _deep_merge(), _drop_secrets(), Any, Environment source that drops secret-looking variables before validation. The…, Recursively remove secret-looking keys, and any section left empty by their…, Build settings where the environment outranks the TOML file. File values cannot…, Merge ``override`` into ``base``, recursing into nested tables. (+1 more)

### Community 56 - "Community 56"
Cohesion: 0.18
Nodes (5): What persisting a playlist actually wrote. Returned instead of the ORM row…, StoredPlaylist, ChannelMeta, PlaylistMeta, VideoMeta

### Community 57 - "Community 57"
Cohesion: 0.20
Nodes (9): FakeStore, DateTime, A single video can afford the channel request, which populates…, One playlist request plus one channel request, regardless of item count., Channel-wide enumeration is a Phase 2 non-goal., The `FetchStore` surface, recording what was written., test_channel_url_does_not_enumerate_videos(), test_playlist_url_fetches_playlist_then_its_owner() (+1 more)

### Community 58 - "Community 58"
Cohesion: 0.24
Nodes (9): CliRunner, Cost, What one generation consumed. `credits`/`currency` are optional because a…, _as_int(), _cost(), JsonValue, Read the provider's own config slice; `run` is injected by tests only. `run`…, Turn the envelope's `usage` into a `Cost`. Tokens only: S8 measured no credit,… (+1 more)

### Community 59 - "Community 59"
Cohesion: 0.22
Nodes (8): logging_handlers, bind(), clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Bind context onto every subsequent log record in this task (run id, provider,…, Drop all bound context., structlog, structlog_stdlib

### Community 60 - "Community 60"
Cohesion: 0.25
Nodes (9): A supplied URL or identifier is not recognisable YouTube input., UrlError, _channel_handle(), classify_id(), _expect_kind(), UrlKind, Classify a bare YouTube identifier by its shape. Order matters: a channel id…, Classify `value` and require it to be the kind its URL form promises. An… (+1 more)

### Community 61 - "Community 61"
Cohesion: 0.28
Nodes (7): datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Default for `fetched_at`: an aware UTC instant, never a naive local one., _utcnow(), Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1). Pure…, thumbforge_core_enums, urllib_parse

### Community 62 - "Community 62"
Cohesion: 0.22
Nodes (9): MonkeyPatch, `PLAN.md` §8 lookup order: the environment variable wins., An exported-but-empty variable is how shells leave unset values; it must not…, ADR 0014: a backend that stores nothing must be distinguishable from an empty…, The variable name is useful; its value is not, and must not be echoed., test_a_blank_environment_variable_falls_through_to_the_keyring(), test_check_names_the_keyring_backend_without_printing_the_key(), test_check_reports_the_environment_as_the_key_source() (+1 more)

### Community 63 - "Community 63"
Cohesion: 0.25
Nodes (6): Collection, PlaylistItem, A playlist's items in playlist order., Reassign `part_number` sequentially from `start` in playlist order. Videos…, One item's `part_number` before and after a `playlist renumber`. Captured per…, Renumbering

### Community 64 - "Community 64"
Cohesion: 0.32
Nodes (7): get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline(), run_migrations_online()

### Community 65 - "Community 65"
Cohesion: 0.25
Nodes (8): MonkeyPatch, parametrize, A generated config must contain defaults, not whatever the current shell…, The documented way to supply a provider key must not brick every command. ADR…, The secret filter must not swallow ordinary nested provider settings., test_a_non_secret_provider_setting_from_the_environment_still_applies(), test_a_provider_api_key_in_the_environment_does_not_break_loading(), test_init_defaults_ignore_the_environment()

### Community 66 - "Community 66"
Cohesion: 0.38
Nodes (3): Session, Build the three repositories over one session, so they share a transaction., Bind to the caller's session; the service owns the transaction.

### Community 67 - "Community 67"
Cohesion: 0.33
Nodes (5): Reading is a question, not a demand: a CI runner has no backend at all., Writing is a demand, and the hint has to name the fallback that needs no…, test_an_unusable_keyring_is_fatal_when_storing(), test_an_unusable_keyring_reports_no_key_rather_than_failing(), explode()

### Community 68 - "Community 68"
Cohesion: 0.40
Nodes (4): datetime, _iso(), When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, Render an aware datetime as the ISO-8601 UTC string the schema stores.

### Community 69 - "Community 69"
Cohesion: 0.40
Nodes (3): field_validator, Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC., Refuse a key that is only dots, which the character class alone would allow.

### Community 70 - "Community 70"
Cohesion: 0.40
Nodes (4): Process, Run the CLI, or the injected stand-in, and return its output., Kill a child and collect it, tolerating one that has already exited. The exit…, _reap()

### Community 71 - "Community 71"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 72 - "Community 72"
Cohesion: 0.40
Nodes (3): _no_real_keyring(), fixture, Replace the OS credential store with a dict for the whole module.

### Community 73 - "Community 73"
Cohesion: 0.67
Nodes (4): NotFoundError, A referenced entity does not exist., test_hint_and_code_reach_stderr(), boom()

### Community 74 - "Community 74"
Cohesion: 0.50
Nodes (3): Find the image `generate_image` wrote, in the conversation's brain directory.…, The agent's prose report of an upstream quota or rate-limit failure, if that is…, _relayed_exhaustion()

### Community 75 - "Community 75"
Cohesion: 0.50
Nodes (3): PlaylistMeta, Persist a playlist, its owning channel, its videos and its item order. Reports…, StoredPlaylist

### Community 76 - "Community 76"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

### Community 77 - "Community 77"
Cohesion: 0.67
Nodes (3): Path, `providers.antigravity.*` must actually configure the instance `provider list`…, test_provider_settings_reach_the_provider()

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 798 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `root()` connect `Community 40` to `Community 3`, `Community 36`, `Community 8`, `Community 47`, `Community 19`, `Community 21`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `AntigravityProvider` connect `Community 28` to `Community 2`, `Community 3`, `Community 70`, `Community 42`, `Community 74`, `Community 46`, `Community 58`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `Repositories` connect `Community 7` to `Community 66`, `Community 68`, `Community 4`, `Community 8`, `Community 75`, `Community 44`, `Community 54`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `emit()` (e.g. with `check()` and `list_()`) actually correct?**
  _`emit()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `Repositories` (e.g. with `repos()` and `test_duplicate_video_in_a_playlist_is_listed_once()`) actually correct?**
  _`Repositories` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05076679005817028 - nodes in this community are weakly interconnected._