# Graph Report - thumbforge-P4.1  (2026-09-25)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1752 nodes · 3492 edges · 132 communities (84 shown, 48 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 300 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c3e9c9c5`
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

## God Nodes (most connected - your core abstractions)
1. `emit()` - 34 edges
2. `load_settings()` - 26 edges
3. `Repositories` - 25 edges
4. `FakeProvider` - 24 edges
5. `StubSource` - 24 edges
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
- `test_valid_layout_spec_loads()` --uses--> `Anchor`  [INFERRED]
  tests/unit/test_layout.py → src/thumbforge/core/layout.py
- `test_valid_layout_spec_loads()` --uses--> `TextCase`  [INFERRED]
  tests/unit/test_layout.py → src/thumbforge/core/layout.py
- `test_sqlite_database_in_container()` --uses--> `ChannelSource`  [INFERRED]
  tests/integration/test_db_container.py → src/thumbforge/core/enums.py

## Import Cycles
- None detected.

## Communities (132 total, 48 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (50): CliRunner, GenerationResult, JsonPayload, ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderRegistryError, ProviderTimeoutError (+42 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (52): Config, Engine, integration, DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., _alembic_config(), get_db_status(), get_engine() (+44 more)

### Community 2 - "Community 2"
Cohesion: 0.10
Nodes (45): DeclarativeBase, enum, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations., Origin of channel metadata. (+37 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (47): The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Repositories, _channel(), _playlist(), ChannelMeta, PlaylistMeta, VideoMeta, Upsert semantics the rest of Phase 2 depends on (ROADMAP P2.3, PLAN.md §3). (+39 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (43): Playlist, list_(), Argument, command, Context, handle_errors, help, Option (+35 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (33): dataclasses, functools, IntEnum, json, rich_console, rich_markup, rich_panel, rich_table (+25 more)

### Community 6 - "Community 6"
Cohesion: 0.07
Nodes (33): LayoutSpec, ComplianceError, PartialBatchError, Exception, A generated image violates the YouTube thumbnail requirements., A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render. (+25 more)

### Community 7 - "Community 7"
Cohesion: 0.07
Nodes (36): Channel, FetchResult, MetadataSource, PlaylistItem, fetch(), Argument, ChannelSource, Context (+28 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (35): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, asset_store() (+27 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (25): asyncio, collections_abc, contextlib, decimal, pathlib, ``thumbforge provider`` — inspect providers and store their keys (ROADMAP P3.5)., Wiring and shared views for the YouTube metadata commands (ROADMAP P2.3).…, The JSON shape that crosses every machine-readable boundary. Defined in `core`… (+17 more)

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (33): _envelope(), _plant_image(), _provider(), Any, Path, S2: the tool takes no output path, so the adapter finds and copies the result., The second "SUCCESS is not success" trap, found by a live run rather than a…, The finding that would have shipped a bug (S6c). `--print-timeout` expiry… (+25 more)

### Community 11 - "Community 11"
Cohesion: 0.07
Nodes (30): Check, fixture, _healthcheck(), stub(), _no_real_keyring(), HealthReport, MonkeyPatch, parametrize (+22 more)

### Community 12 - "Community 12"
Cohesion: 0.09
Nodes (32): command, ImageProvider, _KEY_ARGUMENT, ProviderFactory, check(), _config(), list_(), collect() (+24 more)

### Community 13 - "Community 13"
Cohesion: 0.09
Nodes (32): FixtureRequest, shutil, provider(), _provider_params(), Any, fixture, GenerationRequest, ImageProvider (+24 more)

### Community 14 - "Community 14"
Cohesion: 0.09
Nodes (31): pytest, A supplied URL or identifier is not recognisable YouTube input., UrlError, _channel_handle(), classify_id(), classify_url(), _expect_kind(), UrlKind (+23 more)

### Community 15 - "Community 15"
Cohesion: 0.06
Nodes (29): entries(), _Entry, fixture, MonkeyPatch, A plugin needs only an entry point: the registry never imports it by name., Providers should not each have to handle `None`., `provider list` output must not reorder between runs., Shadowing a provider would make `--provider x` mean different things per… (+21 more)

### Community 16 - "Community 16"
Cohesion: 0.08
Nodes (24): hashlib, os, pil, sqlalchemy_exc, sqlalchemy_orm, Error hierarchy and the exit codes it maps to. Every failure the user can…, new_id(), Path (+16 more)

### Community 17 - "Community 17"
Cohesion: 0.08
Nodes (22): alembic, alembic_config, alembic_runtime_migration, alembic_script, Connection, ConnectionPoolEntry, sqlalchemy, sqlalchemy_pool (+14 more)

### Community 18 - "Community 18"
Cohesion: 0.08
Nodes (28): BaseModel, pydantic, Anchor, BadgeBlock, Box, Canvas, NegativeSpace, PartBlock (+20 more)

### Community 19 - "Community 19"
Cohesion: 0.10
Nodes (24): RawInfo, RetryCallState, _duration(), _log_retry(), _published_at(), ChannelMeta, datetime, PlaylistMeta (+16 more)

### Community 20 - "Community 20"
Cohesion: 0.14
Nodes (27): FakeProvider, Generate a deterministic placeholder image without leaving the machine., parametrize, Path, `FakeProvider` behaviour the generic contract cannot express (PLAN.md §4.2,…, A test asserting style anchoring needs to see the reference in the output., Callers pass a run-scoped directory that may not exist yet., The fake honours dimensions exactly, which the generic contract cannot require.… (+19 more)

### Community 21 - "Community 21"
Cohesion: 0.16
Nodes (26): BoundLogger, CaptureFixture, LogFormat, configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``., Configure structlog and the stdlib root logger. Safe to call more than once. (+18 more)

### Community 22 - "Community 22"
Cohesion: 0.11
Nodes (26): Console, min, init_(), path_(), command, Context, help, Option (+18 more)

### Community 23 - "Community 23"
Cohesion: 0.17
Nodes (26): default_config_path(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., Spike S5 superseded decision D4: the dangerous flag is not opted into by…, The secret filter must not swallow ordinary nested provider settings. (+18 more)

### Community 24 - "Community 24"
Cohesion: 0.12
Nodes (25): Argument, metavar, P, R, rich_syntax, _as_toml(), _config_path(), init_() (+17 more)

### Community 25 - "Community 25"
Cohesion: 0.13
Nodes (18): ChannelMeta, _Meta, PlaylistMeta, datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Default for `fetched_at`: an aware UTC instant, never a naive local one., Shared configuration and provenance for every fetched snapshot., Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC. (+10 more)

### Community 26 - "Community 26"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, Yield `exc` and its `cause` links; `ExtractorError` nests the real failure… (+16 more)

### Community 27 - "Community 27"
Cohesion: 0.12
Nodes (17): Collection, NotFoundError, A referenced entity does not exist., PlaylistRepository, Playlist, PlaylistItem, PlaylistMeta, Playlist rows and their ordered items. (+9 more)

### Community 28 - "Community 28"
Cohesion: 0.10
Nodes (23): PlaylistItemMeta, One video's place in a playlist., Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)., `resolve()` returns both halves (ADR 0005); an empty id is never a valid result., A minimal valid video, so each test states only the field it is about., A fetched snapshot is a value; mutating one would desync it from `fetched_at`., `extra="forbid"` turns an unexpected yt-dlp field into a loud failure. yt-dlp's…, `fetched_at` is persisted as ISO-8601 UTC, so a naive datetime is ambiguous. (+15 more)

### Community 29 - "Community 29"
Cohesion: 0.13
Nodes (22): find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,…, redact() (+14 more)

### Community 30 - "Community 30"
Cohesion: 0.08
Nodes (21): Path, Unit tests for ``thumbforge provider`` (ROADMAP P3.5, phase-3 spec Commands…, `fake` is healthy and offers nothing; that is a 0, not a failure., Spec behaviour 5: works for `fake` even though it ignores keys, so the path is…, A typo must cost a message, not a typed-out secret., A stored empty string reads back as "no key" while occupying a credential entry., The variable that authenticates a provider follows pydantic-settings' nesting., `providers.antigravity.*` must actually configure the instance `provider list`… (+13 more)

### Community 31 - "Community 31"
Cohesion: 0.12
Nodes (19): `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, FakeSource, ResolvedUrl, `FetchService` decisions: kind dispatch, the freshness rule, and what each…, If the fake drifts from `MetadataSource`, these tests stop meaning anything., One playlist request plus one channel request, regardless of item count., Channel-wide enumeration is a Phase 2 non-goal., Spec behaviour 2: a playlist fetched inside the window is not re-fetched. (+11 more)

### Community 32 - "Community 32"
Cohesion: 0.12
Nodes (15): ProviderCapabilities, ProviderInfo, AntigravityProvider, _installed_plugins(), HealthReport, Generate an image by driving `agy` in headless mode., Measured in spikes S3, S4 and S7 — see the module docstring., Report the CLI version, and auth as `unknown` rather than guessing. `unknown`… (+7 more)

### Community 33 - "Community 33"
Cohesion: 0.12
Nodes (20): tenacity, `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., A source wired to a fixture, plus the recorder that captured its calls., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get… (+12 more)

### Community 34 - "Community 34"
Cohesion: 0.17
Nodes (19): Any, importlib_util, ModuleType, _declaration(), _graph(), _module(), Path, The drift check's node filter (issue #26). This is a CI gate, so a silently… (+11 more)

### Community 35 - "Community 35"
Cohesion: 0.12
Nodes (19): platformdirs, pydantic_settings, pydantic_settings_sources, _atomic_write(), ConfigSchema, default_config_toml(), Configuration: TOML file, ``THUMBFORGE_*`` environment variables, and defaults.…, The shape of ``config.toml``, with no environment involvement. Kept separate… (+11 more)

### Community 36 - "Community 36"
Cohesion: 0.10
Nodes (15): GenerationRequest, GenerationResult, HealthReport, JsonValue, Path, ProviderCapabilities, ProviderInfo, If the stub drifts from `ImageProvider`, every test here stops meaning anything. (+7 more)

### Community 37 - "Community 37"
Cohesion: 0.15
Nodes (18): GenerationRequest, parametrize, `AntigravityProvider` error mapping and argv, with the CLI replaced (ROADMAP…, An interrupted run says nothing about whether a retry would succeed., A CLI change must surface as a diagnosable error, not a crash mid-pipeline., Each flag here was verified in the spikes; `--continue` must never appear., Without the injected runner the real subprocess call is attempted., S3: the ratio words are the only lever on output size, so they must be right. (+10 more)

### Community 38 - "Community 38"
Cohesion: 0.12
Nodes (17): callback, count, envvar, is_eager, Option, Context, handle_errors, help (+9 more)

### Community 39 - "Community 39"
Cohesion: 0.29
Nodes (16): parametrize, LayoutSpec, Complete layout specification for a thumbnail template., Unit tests for LayoutSpec and its block models (ROADMAP P4.1, phase-4 spec)., Return a valid layout spec dictionary matching the phase-4 spec TOML., test_box_past_the_canvas_is_rejected(), test_box_within_canvas_exact_bounds_valid(), test_extra_fields_forbidden() (+8 more)

### Community 40 - "Community 40"
Cohesion: 0.21
Nodes (16): Path, Unit tests for ``thumbforge db`` CLI commands (ADR 0004, Phase 1 spec)., test_db_init_creates_database_and_is_idempotent(), test_db_init_json_mode(), test_db_json_error_stream_contract(), test_db_path_command(), test_db_path_json_mode(), test_db_status_command() (+8 more)

### Community 41 - "Community 41"
Cohesion: 0.15
Nodes (15): _fixture(), Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Load one recorded yt-dlp info dict. (+7 more)

### Community 42 - "Community 42"
Cohesion: 0.16
Nodes (13): Image, ProviderPermanentError, The provider failed in a way that retrying cannot fix., GenerationRequest, One image to generate. Providers ignore what their capabilities disclaim., _contrasting(), _digest(), Path (+5 more)

### Community 43 - "Community 43"
Cohesion: 0.13
Nodes (11): Extractor, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, ResolvedUrl, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., Classify input without touching the network; `core.urls` does the work., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes… (+3 more)

### Community 44 - "Community 44"
Cohesion: 0.16
Nodes (11): importlib_metadata, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set() (+3 more)

### Community 45 - "Community 45"
Cohesion: 0.13
Nodes (10): ResolvedUrl, ChannelMeta, PlaylistMeta, VideoMeta, Spec acceptance criteria: same table, `(cached)`, and no source call., A non-YouTube URL is input validation, not a source failure., Canned metadata standing in for `YtDlpSource`., StubSource (+2 more)

### Community 46 - "Community 46"
Cohesion: 0.18
Nodes (9): FetchResult, ResolvedUrl, Playlist rows written., Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order., A channel on its own; enumerating its videos is a Phase 2 non-goal., What was fetched, for rendering and for the `--json` contract. Counts are of… (+1 more)

### Community 47 - "Community 47"
Cohesion: 0.20
Nodes (13): fit_to(), Image, Resize and centre-crop an image to an exact target size (ROADMAP P5.1)., Scale `img` to cover `width`x`height`, then centre-crop to exactly that size,…, Image, parametrize, `fit_to`: cover the target, centre-crop, never distort (ROADMAP P5.1)., Three equal bands, red / green / blue, left to right or top to bottom. (+5 more)

### Community 48 - "Community 48"
Cohesion: 0.16
Nodes (10): ChannelRepository, Channel, ChannelMeta, Persist a playlist, its owning channel, its videos and its item order. Reports…, Persist a channel on its own (a channel URL was fetched)., Channel rows, keyed by YouTube channel id., Return the row for a YouTube channel id, or `None`., Insert or refresh a channel, preserving its ULID. (+2 more)

### Community 49 - "Community 49"
Cohesion: 0.21
Nodes (13): keyring, keyring_errors, api_key(), describe(), env_var(), _from_env(), Provider API keys: read from the environment or the system keyring (ROADMAP…, The environment variable this provider's key is read from. Mirrors pydantic-… (+5 more)

### Community 50 - "Community 50"
Cohesion: 0.16
Nodes (10): FetchStore, ChannelMeta, datetime, PlaylistMeta, VideoMeta, The persistence surface a fetch needs, satisfied by `storage.Repositories`., Persist one video, and its channel when the caller fetched one., Persist a playlist, its owner, its videos and its order. (+2 more)

### Community 51 - "Community 51"
Cohesion: 0.19
Nodes (9): Video, VideoMeta, Look a video up by ULID or YouTube id, raising `NotFoundError` if absent. Both…, Insert or refresh a video, preserving its ULID. `channel_row_id` is supplied…, Videos, newest fetch first, optionally restricted to one channel., Persist one video and, when known, its channel. A single-video fetch can afford…, Video rows, keyed by YouTube video id., Return the row for a YouTube video id, or `None`. (+1 more)

### Community 52 - "Community 52"
Cohesion: 0.22
Nodes (8): BaseSettings, PydanticBaseSettingsSource, default_data_dir(), default_state_dir(), Path, Effective configuration for one invocation: defaults, then file, then…, Default source order, with the environment source filtered of secrets.…, Settings

### Community 53 - "Community 53"
Cohesion: 0.18
Nodes (12): Settings, Return the settings, or re-raise the failure that prevented loading them.…, Configuration is missing, malformed, or contains something it must not., SettingsError, _format_validation_error(), _parse_scalar(), Apply several dotted keys to the TOML file, validating the result once. All…, Parse a CLI value using TOML scalar rules, falling back to a bare string.… (+4 more)

### Community 54 - "Community 54"
Cohesion: 0.15
Nodes (13): Path, The `PLAN.md` §5.3 shape: panel, `#`/`Part` table, then the stored counts., `--refresh` bypasses the freshness rule., Consistent with `video show`., Human output must show `—` rather than a blank or a zero for an unnumbered item., Consistent with `playlist show`., Failing beats silently renumbering everything one step off., test_fetch_playlist_prints_the_panel_table_and_summary() (+5 more)

### Community 55 - "Community 55"
Cohesion: 0.17
Nodes (9): Protocol, GenerationResult, ImageProvider, Path, A produced image and the provenance needed to reproduce or audit it.…, Generate one image per call. Implementations live in `providers/`., What this provider supports; callers check before sending a request., Every check this provider can run, with actionable detail on each failure. (+1 more)

### Community 56 - "Community 56"
Cohesion: 0.20
Nodes (12): A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs. (+4 more)

### Community 57 - "Community 57"
Cohesion: 0.20
Nodes (12): _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`., A full extract must carry the fields a flat entry cannot (S11). Also the only…, Re-assert the S11 field set, so a yt-dlp upgrade that changes it fails loudly. (+4 more)

### Community 58 - "Community 58"
Cohesion: 0.17
Nodes (11): `fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP…, Spec behaviour 3, and it must not surface as an ImportError., Spec behaviour 4: a ULID, a YouTube id or a URL all resolve to the same row., Spec acceptance criteria: exit 3 and `not_found: video 'doesnotexist'`., The spec's acceptance criteria, through the CLI: skipped is `—`, rest are 0,1,…., test_renumber_prints_before_and_after_and_show_reflects_it(), test_source_api_exits_two_with_the_install_hint(), test_video_show_accepts_id_and_url() (+3 more)

### Community 59 - "Community 59"
Cohesion: 0.24
Nodes (11): parametrize, Invariants the provider boundary models enforce (ADR 0010, ROADMAP P3.1/P3.2)., Providers join this onto a path, so it must not be able to leave the workdir.…, The constraint must not reject what `PLAN.md` §6 and the test suites really use., A filename has a length limit even when every character is safe., A request is a value; mutating one after dispatch would desync it from its key., _request(), test_legitimate_idempotency_keys_are_accepted() (+3 more)

### Community 60 - "Community 60"
Cohesion: 0.20
Nodes (9): datetime, _iso(), Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).…, When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, One item's `part_number` before and after a `playlist renumber`. Captured per…, Render an aware datetime as the ISO-8601 UTC string the schema stores., Renumbering, thumbforge_core_services_fetch (+1 more)

### Community 61 - "Community 61"
Cohesion: 0.22
Nodes (9): EnvSettingsSource, _deep_merge(), _drop_secrets(), Any, Environment source that drops secret-looking variables before validation. The…, Recursively remove secret-looking keys, and any section left empty by their…, Build settings where the environment outranks the TOML file. File values cannot…, Merge ``override`` into ``base``, recursing into nested tables. (+1 more)

### Community 62 - "Community 62"
Cohesion: 0.20
Nodes (9): logging_handlers, bind(), clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Bind context onto every subsequent log record in this task (run id, provider,…, Drop all bound context., structlog, structlog_stdlib (+1 more)

### Community 63 - "Community 63"
Cohesion: 0.18
Nodes (11): MonkeyPatch, data_dir(), fixture, An initialised database, since every command here needs the schema., A shrinking playlist must say so rather than quietly dropping rows., `UNIQUE(playlist_id, video_id)` means a repeat stores one row, not two. The…, Replace the real source so no test touches the network., source() (+3 more)

### Community 64 - "Community 64"
Cohesion: 0.18
Nodes (7): Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 65 - "Community 65"
Cohesion: 0.18
Nodes (5): What persisting a playlist actually wrote. Returned instead of the ORM row…, StoredPlaylist, ChannelMeta, PlaylistMeta, VideoMeta

### Community 66 - "Community 66"
Cohesion: 0.20
Nodes (9): FakeStore, DateTime, A single video can afford the channel request, which populates…, `--refresh` must win even one second after a fetch., `fetch` tells the user a re-fetch shrank the playlist., The `FetchStore` surface, recording what was written., test_refresh_overrides_a_fresh_copy(), test_removed_item_count_is_reported() (+1 more)

### Community 67 - "Community 67"
Cohesion: 0.20
Nodes (8): HealthReport, The result of `provider check`: every check, not just the first failure. `ok`…, True when every check passed., Always healthy, and says why, so `provider check` output is never blank., `ok` is derived, so a report cannot claim health while carrying a failure., `extra="forbid"` stops a caller asserting health that the checks contradict., test_health_report_ok_cannot_disagree_with_its_checks(), test_health_report_rejects_a_supplied_ok()

### Community 68 - "Community 68"
Cohesion: 0.20
Nodes (8): FetchService, MetadataSource, Fetch YouTube metadata and persist it., Take the metadata source and persistence layer the CLI selected., Whether a stored playlist is recent enough to skip the network., Just past the window the network call must happen again., test_stale_playlist_is_refetched(), timedelta

### Community 69 - "Community 69"
Cohesion: 0.22
Nodes (5): Path, Unit tests for ``thumbforge template`` CLI commands (ROADMAP P4.1, phase-4…, test_a_missing_file_keeps_the_json_error_contract(), test_markup_in_the_template_name_is_printed_literally(), thumbforge_cli_app

### Community 70 - "Community 70"
Cohesion: 0.22
Nodes (7): Process, Kill a child and collect it, tolerating one that has already exited. The exit…, _reap(), The kill can land after the child has gone, and that must not mask the timeout.…, The spec's acceptance criterion: after a timeout the child is gone. Uses a real…, test_reap_actually_kills_a_running_child(), test_reap_tolerates_a_child_that_already_exited()

### Community 71 - "Community 71"
Cohesion: 0.22
Nodes (7): MonkeyPatch, The real subprocess path, which the injected runner bypasses everywhere else.…, An unanswered call is no evidence about credentials. Reported as `auth` it…, A non-zero exit from `agy models` is the one signal that the CLI is not signed…, test_a_clean_models_failure_is_an_auth_failure(), test_a_hung_child_is_killed_and_reported_as_a_timeout(), test_a_models_timeout_is_not_reported_as_an_auth_failure()

### Community 72 - "Community 72"
Cohesion: 0.29
Nodes (7): re, declarations(), main(), Path, Compare a committed graphify graph against a freshly extracted one. Only…, Ids of the nodes graphify parsed out of a file in this repository., Report whether the committed graph still describes the current declarations.

### Community 73 - "Community 73"
Cohesion: 0.32
Nodes (7): get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline(), run_migrations_online()

### Community 74 - "Community 74"
Cohesion: 0.25
Nodes (8): MonkeyPatch, parametrize, A generated config must contain defaults, not whatever the current shell…, A valid env override must not let an invalid assignment be written to disk., The documented way to supply a provider key must not brick every command. ADR…, test_a_provider_api_key_in_the_environment_does_not_break_loading(), test_environment_cannot_mask_an_invalid_file_value(), test_init_defaults_ignore_the_environment()

### Community 75 - "Community 75"
Cohesion: 0.38
Nodes (3): Session, Build the three repositories over one session, so they share a transaction., Bind to the caller's session; the service owns the transaction.

### Community 76 - "Community 76"
Cohesion: 0.33
Nodes (6): Context, handle_errors, help, Path, Validate a template layout spec against the schema., validate()

### Community 77 - "Community 77"
Cohesion: 0.33
Nodes (4): ProviderInfo, Identity and auth state. Must not raise for a merely unauthenticated provider., Identity and auth state, for `provider list`., Always authenticated: there is nothing to authenticate against.

### Community 78 - "Community 78"
Cohesion: 0.40
Nodes (3): field_validator, Refuse a key that is only dots, which the character class alone would allow., ValidationInfo

### Community 79 - "Community 79"
Cohesion: 0.30
Nodes (3): JsonValue, Accept a config mapping for registry symmetry; nothing in it is required., Deliberately permissive, so callers exercise their full request-building path.

### Community 80 - "Community 80"
Cohesion: 0.50
Nodes (3): model_validator, Self, OutputSettings

### Community 81 - "Community 81"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 82 - "Community 82"
Cohesion: 0.50
Nodes (4): _parse_models(), Slugs from `agy models` output, which is `slug<TAB>display name` per line. The…, `agy models` prefixes a progress line; keying off the tab ignores it by…, test_models_output_is_parsed_by_its_tab_not_its_banner()

### Community 83 - "Community 83"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 848 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **48 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `StubProvider` connect `Community 36` to `Community 9`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `AssetStore` connect `Community 8` to `Community 16`, `Community 2`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `FetchStore` connect `Community 50` to `Community 68`, `Community 55`, `Community 31`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `emit()` (e.g. with `check()` and `list_()`) actually correct?**
  _`emit()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05185185185185185 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.07617051013277429 - nodes in this community are weakly interconnected._