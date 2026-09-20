# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1510 nodes · 3073 edges · 106 communities (71 shown, 35 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 279 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e2b13eba`
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

## God Nodes (most connected - your core abstractions)
1. `emit()` - 29 edges
2. `Repositories` - 25 edges
3. `StubSource` - 24 edges
4. `FakeProvider` - 24 edges
5. `load_settings()` - 24 edges
6. `get_engine()` - 22 edges
7. `AssetStore` - 21 edges
8. `YtDlpSource` - 20 edges
9. `AssetKind` - 20 edges
10. `Runner` - 19 edges

## Surprising Connections (you probably didn't know these)
- `repeating()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_cli_fetch.py → src/thumbforge/core/models.py
- `test_check_constraint_channel_source()` --uses--> `Channel`  [INFERRED]
  tests/unit/test_storage_models.py → src/thumbforge/storage/models.py
- `_request()` --uses--> `GenerationRequest`  [INFERRED]
  tests/contract/test_provider_contract.py → src/thumbforge/core/providers.py
- `_request()` --uses--> `GenerationRequest`  [INFERRED]
  tests/unit/test_core_providers.py → src/thumbforge/core/providers.py
- `_request()` --uses--> `GenerationRequest`  [INFERRED]
  tests/unit/test_fake_provider.py → src/thumbforge/core/providers.py

## Import Cycles
- None detected.

## Communities (106 total, 35 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (57): MonkeyPatch, data_dir(), ChannelMeta, fixture, Path, VideoMeta, `fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP…, An initialised database, since every command here needs the schema. (+49 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (52): parametrize, _envelope(), _plant_image(), _provider(), GenerationRequest, Path, `AntigravityProvider` error mapping and argv, with the CLI replaced (ROADMAP…, S2: the tool takes no output path, so the adapter finds and copies the result. (+44 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (47): BoundLogger, callback, CaptureFixture, count, envvar, is_eager, LogFormat, Context (+39 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (47): The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Repositories, _channel(), _playlist(), ChannelMeta, PlaylistMeta, VideoMeta, Upsert semantics the rest of Phase 2 depends on (ROADMAP P2.3, PLAN.md §3). (+39 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (40): DeclarativeBase, enum, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations., RunKind, RunStatus (+32 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (38): Channel, FetchResult, MetadataSource, PlaylistItem, fetch(), Argument, ChannelSource, Context (+30 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (31): dataclasses, functools, IntEnum, json, rich_console, rich_panel, rich_table, main() (+23 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (38): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, asset_store() (+30 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (37): Config, integration, ChannelSource, Origin of channel metadata., DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., _alembic_config(), get_db_status() (+29 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (35): FixtureRequest, shutil, ImageProvider, Generate one image per call. Implementations live in `providers/`., Identity and auth state. Must not raise for a merely unauthenticated provider., Every check this provider can run, with actionable detail on each failure., provider(), _provider_params() (+27 more)

### Community 10 - "Community 10"
Cohesion: 0.09
Nodes (30): BaseException, RawInfo, RetryCallState, _cause_chain(), _duration(), _log_retry(), _published_at(), ChannelMeta (+22 more)

### Community 11 - "Community 11"
Cohesion: 0.08
Nodes (21): collections_abc, hashlib, logging_handlers, pathlib, pytest, Domain layer: models, errors and services. Imports nothing internal except…, The JSON shape that crosses every machine-readable boundary. Defined in `core`…, structlog configuration (ADR 0015). One pipeline for everything. Application… (+13 more)

### Community 12 - "Community 12"
Cohesion: 0.08
Nodes (27): entries(), _Entry, fixture, Registry behaviour: discovery, duplicate keys, and broken plugins (ADR 0010,…, A plugin needs only an entry point: the registry never imports it by name., Providers should not each have to handle `None`., `provider list` output must not reorder between runs., Same rule when neither side is a builtin. (+19 more)

### Community 13 - "Community 13"
Cohesion: 0.08
Nodes (27): alembic, alembic_config, alembic_runtime_migration, alembic_script, Connection, ConnectionPoolEntry, contextlib, sqlalchemy (+19 more)

### Community 14 - "Community 14"
Cohesion: 0.09
Nodes (25): ResolvedUrl, classify_url(), Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1). Pure…, Resolve a YouTube URL, handle or bare id to its kind and identifier. A `watch`…, ResolvedUrl, Classify input without touching the network; `core.urls` does the work., ResolvedUrl, UrlKind (+17 more)

### Community 15 - "Community 15"
Cohesion: 0.10
Nodes (26): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+18 more)

### Community 16 - "Community 16"
Cohesion: 0.09
Nodes (21): asyncio, Image, pil, GenerationRequest, GenerationResult, Path, One image to generate. Providers ignore what their capabilities disclaim., A produced image and the provenance needed to reproduce or audit it.… (+13 more)

### Community 17 - "Community 17"
Cohesion: 0.09
Nodes (22): os, sqlalchemy_exc, sqlalchemy_orm, new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of ``data``. (+14 more)

### Community 18 - "Community 18"
Cohesion: 0.15
Nodes (26): FakeProvider, Generate a deterministic placeholder image without leaving the machine., parametrize, Path, `FakeProvider` behaviour the generic contract cannot express (PLAN.md §4.2,…, A test asserting style anchoring needs to see the reference in the output., Callers pass a run-scoped directory that may not exist yet., The fake honours dimensions exactly, which the generic contract cannot require.… (+18 more)

### Community 19 - "Community 19"
Cohesion: 0.10
Nodes (24): model_validator, platformdirs, pydantic_settings, Self, AntigravitySettings, BatchSettings, ConfigSchema, default_config_toml() (+16 more)

### Community 20 - "Community 20"
Cohesion: 0.19
Nodes (24): default_config_path(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., Spike S5 superseded decision D4: the dangerous flag is not opted into by…, Write a config file and return its path, so tests read as one expression. (+16 more)

### Community 21 - "Community 21"
Cohesion: 0.14
Nodes (22): Any, importlib_util, ModuleType, _deep_merge(), Build settings where the environment outranks the TOML file. File values cannot…, Merge ``override`` into ``base``, recursing into nested tables., _declaration(), _graph() (+14 more)

### Community 22 - "Community 22"
Cohesion: 0.16
Nodes (23): Playlist, list_(), Argument, command, Context, handle_errors, help, Option (+15 more)

### Community 23 - "Community 23"
Cohesion: 0.13
Nodes (22): find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,…, redact() (+14 more)

### Community 24 - "Community 24"
Cohesion: 0.12
Nodes (21): `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, FakeSource, `FetchService` decisions: kind dispatch, the freshness rule, and what each…, If the fake drifts from `MetadataSource`, these tests stop meaning anything., A single video can afford the channel request, which populates…, One playlist request plus one channel request, regardless of item count., Channel-wide enumeration is a Phase 2 non-goal., `--refresh` must win even one second after a fetch. (+13 more)

### Community 25 - "Community 25"
Cohesion: 0.14
Nodes (21): Argument, metavar, rich_syntax, _as_toml(), _config_path(), init_(), path_(), command (+13 more)

### Community 26 - "Community 26"
Cohesion: 0.13
Nodes (16): BaseModel, Check, HealthReport, ProviderInfo, Identity and auth state, for `provider list`., One named healthcheck outcome, with enough detail to act on a failure., The result of `provider check`: every check, not just the first failure. `ok`…, True when every check passed. (+8 more)

### Community 27 - "Community 27"
Cohesion: 0.12
Nodes (21): DownloadError, NotFoundError, SourceError, Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, _translate(), _download_error(), Exception (+13 more)

### Community 28 - "Community 28"
Cohesion: 0.13
Nodes (18): decimal, pydantic, Cost, The `ImageProvider` Protocol and the values that cross it (ADR 0010, ROADMAP…, What one generation consumed. `credits`/`currency` are optional because a…, parametrize, Invariants the provider boundary models enforce (ADR 0010, ROADMAP P3.1/P3.2)., Providers join this onto a path, so it must not be able to leave the workdir.… (+10 more)

### Community 29 - "Community 29"
Cohesion: 0.13
Nodes (19): `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., A source wired to a fixture, plus the recorder that captured its calls., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get…, `position` comes from enumeration order because `playlist_index` is absent… (+11 more)

### Community 30 - "Community 30"
Cohesion: 0.14
Nodes (18): Engine, Session, sessionmaker, Reclaim free space, truncate the WAL, and delete unreferenced asset files.…, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the…, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., _reclaim_orphans() (+10 more)

### Community 31 - "Community 31"
Cohesion: 0.15
Nodes (19): min, P, R, init_(), path_(), command, Context, help (+11 more)

### Community 32 - "Community 32"
Cohesion: 0.12
Nodes (14): Protocol, FetchStore, ChannelMeta, datetime, MetadataSource, PlaylistMeta, VideoMeta, Take the metadata source and persistence layer the CLI selected. (+6 more)

### Community 33 - "Community 33"
Cohesion: 0.15
Nodes (18): list_(), Argument, command, Context, handle_errors, help, Option, ``thumbforge video`` — list and inspect stored videos (ROADMAP P2.3). (+10 more)

### Community 34 - "Community 34"
Cohesion: 0.16
Nodes (12): FetchResult, FetchService, ResolvedUrl, Playlist rows written., Fetch YouTube metadata and persist it., Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order. (+4 more)

### Community 35 - "Community 35"
Cohesion: 0.12
Nodes (14): HealthReport, Process, ProviderCapabilities, ProviderInfo, AntigravityProvider, _installed_plugins(), Generate an image by driving `agy` in headless mode., Measured in spikes S3, S4 and S7 — see the module docstring. (+6 more)

### Community 36 - "Community 36"
Cohesion: 0.14
Nodes (17): Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)., `resolve()` returns both halves (ADR 0005); an empty id is never a valid result., A minimal valid video, so each test states only the field it is about., A fetched snapshot is a value; mutating one would desync it from `fetched_at`., `fetched_at` is persisted as ISO-8601 UTC, so a naive datetime is ambiguous., Offsets are preserved as an instant, then stored in UTC., Optional columns default to the values the `video` table expects., `position` is 1-based playlist order; 0 would break part numbering. Not sourced… (+9 more)

### Community 37 - "Community 37"
Cohesion: 0.15
Nodes (14): GenerationResult, _aspect_words(), GenerationRequest, Path, Build the prompt sent to `agy -p`. The aspect ratio is given in words because…, Describe the requested shape in words the image tool responds to. 16:9 is named…, Run one generation and copy its output into `workdir`., Assemble the command line. Never `--continue`: every image is a fresh run. (+6 more)

### Community 38 - "Community 38"
Cohesion: 0.18
Nodes (16): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError, Error hierarchy and the exit codes it maps to. Every failure the user can… (+8 more)

### Community 39 - "Community 39"
Cohesion: 0.15
Nodes (15): _fixture(), Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Load one recorded yt-dlp info dict. (+7 more)

### Community 40 - "Community 40"
Cohesion: 0.16
Nodes (13): importlib_metadata, ProviderFactory, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, Image providers: concrete `core.providers.ImageProvider` implementations and…, _discover(), get(), keys(), JsonValue (+5 more)

### Community 41 - "Community 41"
Cohesion: 0.21
Nodes (13): Console, emit(), kv(), JsonValue, RenderableType, Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.…, Build a two-column key/value table, the default shape for ``show``-style…, _json_context() (+5 more)

### Community 42 - "Community 42"
Cohesion: 0.22
Nodes (13): JsonPayload, _as_str(), _looks_like_timeout(), _parse_envelope(), _raise_for_envelope(), `AntigravityProvider` — drives the Antigravity CLI headlessly (ADR 0013,…, Read the single JSON envelope, or explain why there isn't one., Whether a `SUCCESS` envelope is really agy's print timeout. S6c measured the… (+5 more)

### Community 43 - "Community 43"
Cohesion: 0.15
Nodes (10): PartialBatchError, Exception, A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., TemplateError, ThumbforgeError, parametrize (+2 more)

### Community 44 - "Community 44"
Cohesion: 0.21
Nodes (9): ChannelMeta, PlaylistMeta, A fetched YouTube channel., A fetched YouTube playlist and its ordered items., Number of items fetched, for the `playlist.item_count` column., What a URL or bare identifier turned out to be (ADR 0005)., ResolvedUrl, MetadataSource (+1 more)

### Community 45 - "Community 45"
Cohesion: 0.21
Nodes (9): PlaylistRepository, Playlist, PlaylistMeta, Playlist rows and their ordered items., Return the row for a YouTube playlist id, or `None`., Look a playlist up by ULID or YouTube id, raising `NotFoundError` if absent., Insert or refresh a playlist. `channel_row_id` is required: the column is NOT…, Rewrite a playlist's items to exactly `video_ids`, in order. Rows are deleted… (+1 more)

### Community 46 - "Community 46"
Cohesion: 0.19
Nodes (9): Video, VideoMeta, Look a video up by ULID or YouTube id, raising `NotFoundError` if absent. Both…, Insert or refresh a video, preserving its ULID. `channel_row_id` is supplied…, Videos, newest fetch first, optionally restricted to one channel., Persist one video and, when known, its channel. A single-video fetch can afford…, Video rows, keyed by YouTube video id., Return the row for a YouTube video id, or `None`. (+1 more)

### Community 47 - "Community 47"
Cohesion: 0.18
Nodes (12): Settings, Return the settings, or re-raise the failure that prevented loading them.…, Configuration is missing, malformed, or contains something it must not., SettingsError, _format_validation_error(), _parse_scalar(), Apply several dotted keys to the TOML file, validating the result once. All…, Parse a CLI value using TOML scalar rules, falling back to a bare string.… (+4 more)

### Community 48 - "Community 48"
Cohesion: 0.18
Nodes (10): Collection, NotFoundError, A referenced entity does not exist., PlaylistItem, A playlist's items in playlist order., Reassign `part_number` sequentially from `start` in playlist order. Videos…, One item's `part_number` before and after a `playlist renumber`. Captured per…, Renumbering (+2 more)

### Community 49 - "Community 49"
Cohesion: 0.17
Nodes (9): Extractor, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes…, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch., test_permanent_failures_are_not_retried() (+1 more)

### Community 50 - "Community 50"
Cohesion: 0.20
Nodes (9): field_validator, _Meta, datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Default for `fetched_at`: an aware UTC instant, never a naive local one., Shared configuration and provenance for every fetched snapshot., Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC., _utcnow() (+1 more)

### Community 51 - "Community 51"
Cohesion: 0.20
Nodes (12): A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs. (+4 more)

### Community 52 - "Community 52"
Cohesion: 0.20
Nodes (12): _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`., A full extract must carry the fields a flat entry cannot (S11). Also the only…, Re-assert the S11 field set, so a yt-dlp upgrade that changes it fails loudly. (+4 more)

### Community 53 - "Community 53"
Cohesion: 0.21
Nodes (8): ChannelRepository, Channel, ChannelMeta, Persist a channel on its own (a channel URL was fetched)., Channel rows, keyed by YouTube channel id., Return the row for a YouTube channel id, or `None`., Insert or refresh a channel, preserving its ULID., Every channel, newest fetch first.

### Community 54 - "Community 54"
Cohesion: 0.18
Nodes (5): What persisting a playlist actually wrote. Returned instead of the ORM row…, StoredPlaylist, ChannelMeta, PlaylistMeta, VideoMeta

### Community 55 - "Community 55"
Cohesion: 0.20
Nodes (9): FakeStore, DateTime, Spec behaviour 2: a playlist fetched inside the window is not re-fetched., Just past the window the network call must happen again., `fetch` tells the user a re-fetch shrank the playlist., The `FetchStore` surface, recording what was written., test_recent_playlist_is_served_without_a_network_call(), test_removed_item_count_is_reported() (+1 more)

### Community 56 - "Community 56"
Cohesion: 0.29
Nodes (6): BaseSettings, default_data_dir(), default_state_dir(), Path, Effective configuration for one invocation: defaults, then file, then…, Settings

### Community 57 - "Community 57"
Cohesion: 0.24
Nodes (8): CliRunner, JsonValue, _as_int(), _cost(), Read the provider's own config slice; `run` is injected by tests only. `run`…, Turn the envelope's `usage` into a `Cost`. Tokens only: S8 measured no credit,…, Read an int from untyped JSON, rejecting bools and non-numbers., Accept a config mapping for registry symmetry; nothing in it is required.

### Community 58 - "Community 58"
Cohesion: 0.20
Nodes (7): ProviderCapabilities, What this provider supports; callers check before sending a request., What a provider can actually do, so callers degrade instead of guessing., Deliberately permissive, so callers exercise their full request-building path., Callers branch on these, so a nonsensical combination is a bug in the provider., test_capabilities_are_declared_and_self_consistent(), Deliberately unlike Antigravity, so a test cannot pass by coincidence.

### Community 59 - "Community 59"
Cohesion: 0.25
Nodes (7): datetime, _iso(), Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).…, When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, Render an aware datetime as the ISO-8601 UTC string the schema stores., thumbforge_core_services_fetch, thumbforge_storage_models

### Community 60 - "Community 60"
Cohesion: 0.25
Nodes (9): A supplied URL or identifier is not recognisable YouTube input., UrlError, _channel_handle(), classify_id(), _expect_kind(), UrlKind, Classify a bare YouTube identifier by its shape. Order matters: a channel id…, Classify `value` and require it to be the kind its URL form promises. An… (+1 more)

### Community 61 - "Community 61"
Cohesion: 0.29
Nodes (7): re, declarations(), main(), Path, Compare a committed graphify graph against a freshly extracted one. Only…, Ids of the nodes graphify parsed out of a file in this repository., Report whether the committed graph still describes the current declarations.

### Community 62 - "Community 62"
Cohesion: 0.38
Nodes (3): Session, Build the three repositories over one session, so they share a transaction., Bind to the caller's session; the service owns the transaction.

### Community 63 - "Community 63"
Cohesion: 0.29
Nodes (6): A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, VideoMeta, `extra="forbid"` turns an unexpected yt-dlp field into a loud failure. yt-dlp's…, `duration_s` is a length; a negative value would corrupt part numbering…, test_negative_duration_is_rejected(), test_unknown_upstream_field_is_rejected()

### Community 64 - "Community 64"
Cohesion: 0.40
Nodes (6): ComplianceError, A generated image violates the YouTube thumbnail requirements., Machine mode contract: stdout carries command output, stderr carries the…, test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), boom(), root()

### Community 65 - "Community 65"
Cohesion: 0.33
Nodes (6): _atomic_write(), Replace ``path`` atomically: write a sibling temp file, fsync, then rename. A…, Write the commented default configuration, refusing to clobber unless ``force``., write_default_config(), test_write_default_config_refuses_to_clobber(), test_write_is_atomic_and_leaves_no_temp_files()

### Community 66 - "Community 66"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 67 - "Community 67"
Cohesion: 0.40
Nodes (5): MonkeyPatch, A generated config must contain defaults, not whatever the current shell…, A valid env override must not let an invalid assignment be written to disk., test_environment_cannot_mask_an_invalid_file_value(), test_init_defaults_ignore_the_environment()

### Community 68 - "Community 68"
Cohesion: 0.50
Nodes (3): PlaylistItemMeta, One video's place in a playlist., PlaylistMeta

### Community 69 - "Community 69"
Cohesion: 0.50
Nodes (3): Find the image `generate_image` wrote, in the conversation's brain directory.…, The agent's prose report of an upstream quota or rate-limit failure, if that is…, _relayed_exhaustion()

### Community 70 - "Community 70"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 731 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `YtDlpSource` connect `Community 49` to `Community 5`, `Community 39`, `Community 10`, `Community 14`, `Community 51`, `Community 29`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `GenerationRequest` connect `Community 16` to `Community 9`, `Community 18`, `Community 50`, `Community 26`, `Community 28`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `HealthReport` connect `Community 26` to `Community 16`, `Community 9`, `Community 18`, `Community 28`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `Repositories` (e.g. with `repos()` and `test_duplicate_video_in_a_playlist_is_listed_once()`) actually correct?**
  _`Repositories` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.0546448087431694 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.08709273182957393 - nodes in this community are weakly interconnected._