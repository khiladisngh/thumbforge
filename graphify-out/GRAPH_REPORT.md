# Graph Report - thumbforge-P5.1  (2026-09-25)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1673 nodes · 3337 edges · 124 communities (81 shown, 43 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 285 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dbe690de`
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

## Communities (124 total, 43 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (58): MonkeyPatch, PlaylistItemMeta, One video's place in a playlist., data_dir(), ChannelMeta, fixture, Path, PlaylistMeta (+50 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (58): _envelope(), _plant_image(), _provider(), Any, GenerationRequest, MonkeyPatch, parametrize, Path (+50 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (41): field_validator, ChannelMeta, _Meta, PlaylistMeta, datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Default for `fetched_at`: an aware UTC instant, never a naive local one., Shared configuration and provenance for every fetched snapshot. (+33 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (47): FixtureRequest, pil, shutil, fit_to(), Image, Resize and centre-crop an image to an exact target size (ROADMAP P5.1)., Scale `img` to cover `width`x`height`, then centre-crop to exactly that size,…, provider() (+39 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (45): DeclarativeBase, enum, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations., Origin of channel metadata. (+37 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (47): The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Repositories, _channel(), _playlist(), ChannelMeta, PlaylistMeta, VideoMeta, Upsert semantics the rest of Phase 2 depends on (ROADMAP P2.3, PLAN.md §3). (+39 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (34): json, re, declarations(), main(), Path, Compare a committed graphify graph against a freshly extracted one. Only…, Ids of the nodes graphify parsed out of a file in this repository., Report whether the committed graph still describes the current declarations. (+26 more)

### Community 7 - "Community 7"
Cohesion: 0.08
Nodes (31): alembic, alembic_config, alembic_runtime_migration, alembic_script, Config, Connection, ConnectionPoolEntry, sqlalchemy (+23 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (35): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, asset_store() (+27 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (34): _fixture(), Any, `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from. (+26 more)

### Community 10 - "Community 10"
Cohesion: 0.11
Nodes (34): Engine, integration, get_engine(), init_db(), Session, sessionmaker, Ensure directory exists and upgrade DB to head. Returns: Tuple of…, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the… (+26 more)

### Community 11 - "Community 11"
Cohesion: 0.11
Nodes (34): Channel, Playlist, PlaylistItem, JsonPayload, RenderableType, Repositories, Build the JSON payload and the Rich renderable from the **stored** rows.…, _view() (+26 more)

### Community 12 - "Community 12"
Cohesion: 0.10
Nodes (27): dataclasses, rich_panel, rich_table, main(), Root Typer application: global flags, context construction, sub-app…, ``thumbforge fetch`` — pull YouTube metadata into the database (ROADMAP P2.3)., panel(), The only module allowed to write to stdout. Every command produces one of two… (+19 more)

### Community 13 - "Community 13"
Cohesion: 0.08
Nodes (30): entries(), _Entry, fixture, MonkeyPatch, Registry behaviour: discovery, duplicate keys, and broken plugins (ADR 0010,…, A plugin needs only an entry point: the registry never imports it by name., Providers should not each have to handle `None`., `provider list` output must not reorder between runs. (+22 more)

### Community 14 - "Community 14"
Cohesion: 0.09
Nodes (28): contextlib, RawInfo, RetryCallState, _duration(), _log_retry(), _published_at(), ChannelMeta, datetime (+20 more)

### Community 15 - "Community 15"
Cohesion: 0.12
Nodes (28): command, ImageProvider, _KEY_ARGUMENT, check(), _config(), list_(), collect(), models() (+20 more)

### Community 16 - "Community 16"
Cohesion: 0.09
Nodes (22): os, sqlalchemy_exc, sqlalchemy_orm, new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of ``data``. (+14 more)

### Community 17 - "Community 17"
Cohesion: 0.17
Nodes (27): default_config_path(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., Spike S5 superseded decision D4: the dangerous flag is not opted into by…, The secret filter must not swallow ordinary nested provider settings. (+19 more)

### Community 18 - "Community 18"
Cohesion: 0.16
Nodes (26): BoundLogger, CaptureFixture, LogFormat, configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``., Configure structlog and the stdlib root logger. Safe to call more than once. (+18 more)

### Community 19 - "Community 19"
Cohesion: 0.15
Nodes (26): FakeProvider, Generate a deterministic placeholder image without leaving the machine., parametrize, Path, `FakeProvider` behaviour the generic contract cannot express (PLAN.md §4.2,…, A test asserting style anchoring needs to see the reference in the output., Callers pass a run-scoped directory that may not exist yet., The fake honours dimensions exactly, which the generic contract cannot require.… (+18 more)

### Community 20 - "Community 20"
Cohesion: 0.14
Nodes (24): min, P, R, init_(), path_(), command, Context, help (+16 more)

### Community 21 - "Community 21"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, Yield `exc` and its `cause` links; `ExtractorError` nests the real failure… (+16 more)

### Community 22 - "Community 22"
Cohesion: 0.12
Nodes (17): Collection, NotFoundError, A referenced entity does not exist., PlaylistRepository, Playlist, PlaylistItem, PlaylistMeta, Playlist rows and their ordered items. (+9 more)

### Community 23 - "Community 23"
Cohesion: 0.12
Nodes (19): functools, IntEnum, rich_console, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.… (+11 more)

### Community 24 - "Community 24"
Cohesion: 0.13
Nodes (22): find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,…, redact() (+14 more)

### Community 25 - "Community 25"
Cohesion: 0.11
Nodes (19): GenerationResult, ProviderOutputMissingError, The provider reported success but produced no usable image., _aspect_words(), GenerationRequest, Path, Build the prompt sent to `agy -p`. The aspect ratio is given in words because…, Describe the requested shape in words the image tool responds to. 16:9 is named… (+11 more)

### Community 26 - "Community 26"
Cohesion: 0.12
Nodes (20): `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, FakeSource, `FetchService` decisions: kind dispatch, the freshness rule, and what each…, If the fake drifts from `MetadataSource`, these tests stop meaning anything., Spec behaviour 2: a playlist fetched inside the window is not re-fetched., Just past the window the network call must happen again., `--refresh` must win even one second after a fetch., A video fetch is one cheap request and always reflects the latest title. (+12 more)

### Community 27 - "Community 27"
Cohesion: 0.13
Nodes (21): Argument, metavar, rich_syntax, _as_toml(), _config_path(), path_(), command, Context (+13 more)

### Community 28 - "Community 28"
Cohesion: 0.12
Nodes (18): collections_abc, ProviderFactory, ProviderRegistryError, Provider discovery failed: duplicate key, or a plugin that will not load., The JSON shape that crosses every machine-readable boundary. Defined in `core`…, `AntigravityProvider` — drives the Antigravity CLI headlessly (ADR 0013,…, Image providers: concrete `core.providers.ImageProvider` implementations and…, _discover() (+10 more)

### Community 29 - "Community 29"
Cohesion: 0.13
Nodes (22): JsonPayload, ProviderAuthError, ProviderError, ProviderPermanentError, ProviderTimeoutError, ProviderTransientError, Base class for image-provider failures., The provider rejected our credentials, or none were cached. (+14 more)

### Community 30 - "Community 30"
Cohesion: 0.10
Nodes (21): platformdirs, pydantic_settings, pydantic_settings_sources, BatchSettings, ConfigSchema, default_config_toml(), _format_validation_error(), GeneralSettings (+13 more)

### Community 31 - "Community 31"
Cohesion: 0.12
Nodes (15): ProviderCapabilities, ProviderInfo, AntigravityProvider, _installed_plugins(), HealthReport, Generate an image by driving `agy` in headless mode., Measured in spikes S3, S4 and S7 — see the module docstring., Report the CLI version, and auth as `unknown` rather than guessing. `unknown`… (+7 more)

### Community 32 - "Community 32"
Cohesion: 0.17
Nodes (19): Any, importlib_util, ModuleType, _declaration(), _graph(), _module(), Path, The drift check's node filter (issue #26). This is a CI gate, so a silently… (+11 more)

### Community 33 - "Community 33"
Cohesion: 0.10
Nodes (15): GenerationRequest, GenerationResult, HealthReport, JsonValue, Path, ProviderCapabilities, ProviderInfo, If the stub drifts from `ImageProvider`, every test here stops meaning anything. (+7 more)

### Community 34 - "Community 34"
Cohesion: 0.16
Nodes (12): FetchResult, FetchService, ResolvedUrl, Playlist rows written., Fetch YouTube metadata and persist it., Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order. (+4 more)

### Community 35 - "Community 35"
Cohesion: 0.12
Nodes (13): FetchStore, ChannelMeta, datetime, MetadataSource, PlaylistMeta, VideoMeta, Take the metadata source and persistence layer the CLI selected., The persistence surface a fetch needs, satisfied by `storage.Repositories`. (+5 more)

### Community 36 - "Community 36"
Cohesion: 0.11
Nodes (15): Unit tests for ``thumbforge provider`` (ROADMAP P3.5, phase-3 spec Commands…, `fake` is healthy and offers nothing; that is a 0, not a failure., A typo must cost a message, not a typed-out secret., A stored empty string reads back as "no key" while occupying a credential entry., The variable that authenticates a provider follows pydantic-settings' nesting., No provider needs an API key yet, so the credential row is informational only., The JSON contract carries the full capability object, not the display summary., Exit 3, and the hint lists what is installed, because the cause is usually a… (+7 more)

### Community 37 - "Community 37"
Cohesion: 0.15
Nodes (13): asyncio, Image, GenerationRequest, One image to generate. Providers ignore what their capabilities disclaim., _contrasting(), _digest(), Path, `FakeProvider` — deterministic, offline image generation (PLAN.md §4.2, ROADMAP… (+5 more)

### Community 38 - "Community 38"
Cohesion: 0.13
Nodes (13): decimal, Protocol, GenerationResult, ImageProvider, ProviderCapabilities, Path, The `ImageProvider` Protocol and the values that cross it (ADR 0010, ROADMAP…, A produced image and the provenance needed to reproduce or audit it.… (+5 more)

### Community 39 - "Community 39"
Cohesion: 0.12
Nodes (12): hashlib, pathlib, pytest, Domain layer: models, errors and services. Imports nothing internal except…, testcontainers_core_container, Integration tests using Testcontainers for database verification (ADR 0004)., MonkeyPatch, Path (+4 more)

### Community 40 - "Community 40"
Cohesion: 0.15
Nodes (16): Settings, init_(), Option, Write a commented configuration file with every default., Return the settings, or re-raise the failure that prevented loading them.…, Configuration is missing, malformed, or contains something it must not., SettingsError, _atomic_write() (+8 more)

### Community 41 - "Community 41"
Cohesion: 0.12
Nodes (16): callback, count, help, is_eager, Option, Context, handle_errors, Path (+8 more)

### Community 42 - "Community 42"
Cohesion: 0.13
Nodes (15): FetchResult, MetadataSource, fetch(), Argument, ChannelSource, Context, handle_errors, help (+7 more)

### Community 43 - "Community 43"
Cohesion: 0.16
Nodes (10): ChannelRepository, Channel, ChannelMeta, Persist a playlist, its owning channel, its videos and its item order. Reports…, Persist a channel on its own (a channel URL was fetched)., Channel rows, keyed by YouTube channel id., Return the row for a YouTube channel id, or `None`., Insert or refresh a channel, preserving its ULID. (+2 more)

### Community 44 - "Community 44"
Cohesion: 0.15
Nodes (11): importlib_metadata, logging_handlers, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, bind(), clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Bind context onto every subsequent log record in this task (run id, provider,…, Drop all bound context. (+3 more)

### Community 45 - "Community 45"
Cohesion: 0.21
Nodes (13): keyring, keyring_errors, api_key(), describe(), env_var(), _from_env(), Provider API keys: read from the environment or the system keyring (ROADMAP…, The environment variable this provider's key is read from. Mirrors pydantic-… (+5 more)

### Community 46 - "Community 46"
Cohesion: 0.19
Nodes (14): list_(), Argument, command, Context, handle_errors, help, Option, List stored videos, most recently fetched first. (+6 more)

### Community 47 - "Community 47"
Cohesion: 0.15
Nodes (11): Check, HealthReport, Every check this provider can run, with actionable detail on each failure., One named healthcheck outcome, with enough detail to act on a failure., The result of `provider check`: every check, not just the first failure. `ok`…, True when every check passed., Always healthy, and says why, so `provider check` output is never blank., `ok` is derived, so a report cannot claim health while carrying a failure. (+3 more)

### Community 48 - "Community 48"
Cohesion: 0.20
Nodes (13): _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, Record `tests/fixtures/ytdlp/*.json` from live YouTube, and assert the S11…, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`., A full extract must carry the fields a flat entry cannot (S11). Also the only… (+5 more)

### Community 49 - "Community 49"
Cohesion: 0.19
Nodes (9): Video, VideoMeta, Look a video up by ULID or YouTube id, raising `NotFoundError` if absent. Both…, Insert or refresh a video, preserving its ULID. `channel_row_id` is supplied…, Videos, newest fetch first, optionally restricted to one channel., Persist one video and, when known, its channel. A single-video fetch can afford…, Video rows, keyed by YouTube video id., Return the row for a YouTube video id, or `None`. (+1 more)

### Community 50 - "Community 50"
Cohesion: 0.22
Nodes (8): BaseSettings, PydanticBaseSettingsSource, default_data_dir(), default_state_dir(), Path, Effective configuration for one invocation: defaults, then file, then…, Default source order, with the environment source filtered of secrets.…, Settings

### Community 51 - "Community 51"
Cohesion: 0.22
Nodes (12): pydantic, parametrize, Invariants the provider boundary models enforce (ADR 0010, ROADMAP P3.1/P3.2)., Providers join this onto a path, so it must not be able to leave the workdir.…, The constraint must not reject what `PLAN.md` §6 and the test suites really use., A filename has a length limit even when every character is safe., A request is a value; mutating one after dispatch would desync it from its key., _request() (+4 more)

### Community 52 - "Community 52"
Cohesion: 0.17
Nodes (12): Check, _healthcheck(), stub(), HealthReport, Both exit 4, but the machine-readable code is what tells the user where to look., "No models" and "not signed in" look identical in output and must not be…, A stand-in `AntigravityProvider.healthcheck` returning a fixed report., A failing check must not hide the passing ones: the table is printed, then the… (+4 more)

### Community 53 - "Community 53"
Cohesion: 0.17
Nodes (9): Extractor, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes…, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch., test_permanent_failures_are_not_retried() (+1 more)

### Community 54 - "Community 54"
Cohesion: 0.17
Nodes (12): parametrize, UrlKind, `@` alone names no channel, so it must not resolve successfully., `urlparse` raises `ValueError` on these; the CLI only handles…, Every URL form thumbforge accepts, and the exact identifier it must extract., Bad input must be a usage error (exit 2), not a source failure or a crash., An explicit form fixes the kind; the id's shape must not override it.…, test_classify_url() (+4 more)

### Community 55 - "Community 55"
Cohesion: 0.20
Nodes (12): A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs. (+4 more)

### Community 56 - "Community 56"
Cohesion: 0.18
Nodes (10): BaseModel, model_validator, Self, Cost, What one generation consumed. `credits`/`currency` are optional because a…, AntigravitySettings, OutputSettings, ProviderSettings (+2 more)

### Community 57 - "Community 57"
Cohesion: 0.20
Nodes (9): datetime, _iso(), Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).…, When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, One item's `part_number` before and after a `playlist renumber`. Captured per…, Render an aware datetime as the ISO-8601 UTC string the schema stores., Renumbering, thumbforge_core_services_fetch (+1 more)

### Community 58 - "Community 58"
Cohesion: 0.22
Nodes (9): EnvSettingsSource, _deep_merge(), _drop_secrets(), Any, Environment source that drops secret-looking variables before validation. The…, Recursively remove secret-looking keys, and any section left empty by their…, Build settings where the environment outranks the TOML file. File values cannot…, Merge ``override`` into ``base``, recursing into nested tables. (+1 more)

### Community 59 - "Community 59"
Cohesion: 0.18
Nodes (5): What persisting a playlist actually wrote. Returned instead of the ORM row…, StoredPlaylist, ChannelMeta, PlaylistMeta, VideoMeta

### Community 60 - "Community 60"
Cohesion: 0.20
Nodes (9): FakeStore, DateTime, A single video can afford the channel request, which populates…, One playlist request plus one channel request, regardless of item count., Channel-wide enumeration is a Phase 2 non-goal., The `FetchStore` surface, recording what was written., test_channel_url_does_not_enumerate_videos(), test_playlist_url_fetches_playlist_then_its_owner() (+1 more)

### Community 61 - "Community 61"
Cohesion: 0.20
Nodes (8): ResolvedUrl, classify_url(), Resolve a YouTube URL, handle or bare id to its kind and identifier. A `watch`…, ResolvedUrl, `v=` wins over `list=`: the URL names a video being watched inside a playlist.…, Pasted URLs routinely carry a trailing newline or space., test_surrounding_whitespace_is_tolerated(), test_watch_url_with_list_resolves_to_the_video()

### Community 62 - "Community 62"
Cohesion: 0.22
Nodes (7): PartialBatchError, Exception, A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., TemplateError, ThumbforgeError

### Community 63 - "Community 63"
Cohesion: 0.20
Nodes (10): MonkeyPatch, parametrize, `PLAN.md` §8 lookup order: the environment variable wins., An exported-but-empty variable is how shells leave unset values; it must not…, ADR 0014: a backend that stores nothing must be distinguishable from an empty…, The variable name is useful; its value is not, and must not be echoed., test_a_blank_environment_variable_falls_through_to_the_keyring(), test_check_names_the_keyring_backend_without_printing_the_key() (+2 more)

### Community 64 - "Community 64"
Cohesion: 0.22
Nodes (7): Process, Kill a child and collect it, tolerating one that has already exited. The exit…, _reap(), The kill can land after the child has gone, and that must not mask the timeout.…, The spec's acceptance criterion: after a timeout the child is gone. Uses a real…, test_reap_actually_kills_a_running_child(), test_reap_tolerates_a_child_that_already_exited()

### Community 65 - "Community 65"
Cohesion: 0.25
Nodes (8): DatabaseError, Error hierarchy and the exit codes it maps to. Every failure the user can…, A database operation failed (e.g. migration, lock, disk failure)., Reclaim free space, truncate the WAL, and delete unreferenced asset files.…, vacuum_db(), parametrize, A non-positive window would let vacuum delete an in-flight write's files., test_vacuum_rejects_non_positive_grace()

### Community 66 - "Community 66"
Cohesion: 0.25
Nodes (9): A supplied URL or identifier is not recognisable YouTube input., UrlError, _channel_handle(), classify_id(), _expect_kind(), UrlKind, Classify a bare YouTube identifier by its shape. Order matters: a channel id…, Classify `value` and require it to be the kind its URL form promises. An… (+1 more)

### Community 67 - "Community 67"
Cohesion: 0.32
Nodes (7): CliRunner, _as_int(), _cost(), JsonValue, Read the provider's own config slice; `run` is injected by tests only. `run`…, Turn the envelope's `usage` into a `Cost`. Tokens only: S8 measured no credit,…, Read an int from untyped JSON, rejecting bools and non-numbers.

### Community 68 - "Community 68"
Cohesion: 0.32
Nodes (7): get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline(), run_migrations_online()

### Community 69 - "Community 69"
Cohesion: 0.25
Nodes (8): MonkeyPatch, parametrize, A generated config must contain defaults, not whatever the current shell…, A valid env override must not let an invalid assignment be written to disk., The documented way to supply a provider key must not brick every command. ADR…, test_a_provider_api_key_in_the_environment_does_not_break_loading(), test_environment_cannot_mask_an_invalid_file_value(), test_init_defaults_ignore_the_environment()

### Community 70 - "Community 70"
Cohesion: 0.43
Nodes (6): Console, _json_context(), `emit` is the machine boundary: what it prints must always be parseable JSON., test_json_mode_output_round_trips(), test_non_finite_floats_are_rejected(), test_non_json_payload_raises_instead_of_being_stringified()

### Community 71 - "Community 71"
Cohesion: 0.38
Nodes (3): Session, Build the three repositories over one session, so they share a transaction., Bind to the caller's session; the service owns the transaction.

### Community 72 - "Community 72"
Cohesion: 0.40
Nodes (6): ComplianceError, A generated image violates the YouTube thumbnail requirements., Machine mode contract: stdout carries command output, stderr carries the…, test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), boom(), root()

### Community 73 - "Community 73"
Cohesion: 0.33
Nodes (4): ProviderInfo, Identity and auth state. Must not raise for a merely unauthenticated provider., Identity and auth state, for `provider list`., Always authenticated: there is nothing to authenticate against.

### Community 74 - "Community 74"
Cohesion: 0.33
Nodes (5): Reading is a question, not a demand: a CI runner has no backend at all., Writing is a demand, and the hint has to name the fallback that needs no…, test_an_unusable_keyring_is_fatal_when_storing(), test_an_unusable_keyring_reports_no_key_rather_than_failing(), explode()

### Community 75 - "Community 75"
Cohesion: 0.40
Nodes (3): fixture, _no_real_keyring(), Replace the OS credential store with a dict for the whole module.

### Community 76 - "Community 76"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 77 - "Community 77"
Cohesion: 0.50
Nodes (4): _parse_models(), Slugs from `agy models` output, which is `slug<TAB>display name` per line. The…, `agy models` prefixes a progress line; keying off the tab ignores it by…, test_models_output_is_parsed_by_its_tab_not_its_banner()

### Community 78 - "Community 78"
Cohesion: 0.50
Nodes (3): parametrize, Every error in CASES exits with the code documented in PLAN.md 5.1., test_error_maps_to_documented_exit_code()

### Community 79 - "Community 79"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

### Community 82 - "Community 82"
Cohesion: 0.67
Nodes (3): Path, `providers.antigravity.*` must actually configure the instance `provider list`…, test_provider_settings_reach_the_provider()

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 818 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **43 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FetchStore` connect `Community 35` to `Community 26`, `Community 38`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `StubProvider` connect `Community 33` to `Community 13`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `FakeProvider` connect `Community 19` to `Community 37`, `Community 38`, `Community 73`, `Community 47`, `Community 80`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `emit()` (e.g. with `check()` and `list_()`) actually correct?**
  _`emit()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05273937532002048 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.07731694828469023 - nodes in this community are weakly interconnected._