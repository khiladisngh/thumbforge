# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1491 nodes · 3052 edges · 104 communities (67 shown, 37 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 280 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5b7b17e8`
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

## God Nodes (most connected - your core abstractions)
1. `emit()` - 29 edges
2. `Repositories` - 25 edges
3. `StubSource` - 24 edges
4. `FakeProvider` - 24 edges
5. `load_settings()` - 24 edges
6. `get_engine()` - 22 edges
7. `AssetStore` - 21 edges
8. `AntigravityProvider` - 20 edges
9. `GenerationRequest` - 20 edges
10. `YtDlpSource` - 20 edges

## Surprising Connections (you probably didn't know these)
- `repeating()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_cli_fetch.py → src/thumbforge/core/models.py
- `test_item_count_tracks_items()` --uses--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_core_models.py → src/thumbforge/core/models.py
- `test_playlist_position_is_one_based()` --uses--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_core_models.py → src/thumbforge/core/models.py
- `_playlist()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_repositories.py → src/thumbforge/core/models.py
- `test_duplicate_video_in_a_playlist_is_listed_once()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_repositories.py → src/thumbforge/core/models.py

## Import Cycles
- None detected.

## Communities (104 total, 37 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (60): MonkeyPatch, PlaylistItemMeta, One video's place in a playlist., data_dir(), ChannelMeta, fixture, Path, PlaylistMeta (+52 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (49): FixtureRequest, ProviderFactory, shutil, ProviderRegistryError, Provider discovery failed: duplicate key, or a plugin that will not load., ImageProvider, Generate one image per call. Implementations live in `providers/`., What this provider supports; callers check before sending a request. (+41 more)

### Community 2 - "Community 2"
Cohesion: 0.10
Nodes (45): DeclarativeBase, enum, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations., Origin of channel metadata. (+37 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (47): The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Repositories, _channel(), _playlist(), ChannelMeta, PlaylistMeta, VideoMeta, Upsert semantics the rest of Phase 2 depends on (ROADMAP P2.3, PLAN.md §3). (+39 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (44): _envelope(), _plant_image(), _provider(), Any, parametrize, Path, `AntigravityProvider` error mapping and argv, with the CLI replaced (ROADMAP…, The finding that would have shipped a bug (S6c). `--print-timeout` expiry… (+36 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (33): Any, hashlib, importlib_util, ModuleType, pytest, Domain layer: models, errors and services. Imports nothing internal except…, _deep_merge(), Build settings where the environment outranks the TOML file. File values cannot… (+25 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (29): Channel, collections_abc, dataclasses, rich_panel, rich_table, main(), Root Typer application: global flags, context construction, sub-app…, ``thumbforge fetch`` — pull YouTube metadata into the database (ROADMAP P2.3). (+21 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (35): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, asset_store() (+27 more)

### Community 8 - "Community 8"
Cohesion: 0.13
Nodes (32): Config, DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., _alembic_config(), get_db_status(), get_engine(), init_db(), Path (+24 more)

### Community 9 - "Community 9"
Cohesion: 0.09
Nodes (28): contextlib, RawInfo, RetryCallState, _duration(), _log_retry(), _published_at(), ChannelMeta, datetime (+20 more)

### Community 10 - "Community 10"
Cohesion: 0.10
Nodes (26): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+18 more)

### Community 11 - "Community 11"
Cohesion: 0.07
Nodes (26): entries(), _Entry, fixture, A plugin needs only an entry point: the registry never imports it by name., Providers should not each have to handle `None`., `provider list` output must not reorder between runs., Same rule when neither side is a builtin., A skipped plugin looks identical to one that was never installed. That is the… (+18 more)

### Community 12 - "Community 12"
Cohesion: 0.09
Nodes (22): os, sqlalchemy_exc, sqlalchemy_orm, Error hierarchy and the exit codes it maps to. Every failure the user can…, new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits. (+14 more)

### Community 13 - "Community 13"
Cohesion: 0.13
Nodes (28): pil, FakeProvider, Generate a deterministic placeholder image without leaving the machine., parametrize, Path, `FakeProvider` behaviour the generic contract cannot express (PLAN.md §4.2,…, A test asserting style anchoring needs to see the reference in the output., Callers pass a run-scoped directory that may not exist yet. (+20 more)

### Community 14 - "Community 14"
Cohesion: 0.12
Nodes (27): min, P, R, init_(), path_(), command, Context, help (+19 more)

### Community 15 - "Community 15"
Cohesion: 0.16
Nodes (26): BoundLogger, CaptureFixture, LogFormat, configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``., Configure structlog and the stdlib root logger. Safe to call more than once. (+18 more)

### Community 16 - "Community 16"
Cohesion: 0.11
Nodes (25): CliRunner, JsonPayload, Cost, What one generation consumed. `credits`/`currency` are optional because a…, _as_int(), _as_str(), _aspect_words(), _cost() (+17 more)

### Community 17 - "Community 17"
Cohesion: 0.10
Nodes (23): parametrize, ResolvedUrl, classify_url(), Resolve a YouTube URL, handle or bare id to its kind and identifier. A `watch`…, ResolvedUrl, Classify input without touching the network; `core.urls` does the work., ResolvedUrl, UrlKind (+15 more)

### Community 18 - "Community 18"
Cohesion: 0.09
Nodes (20): alembic, alembic_config, alembic_runtime_migration, alembic_script, Connection, ConnectionPoolEntry, sqlalchemy, sqlalchemy_pool (+12 more)

### Community 19 - "Community 19"
Cohesion: 0.11
Nodes (19): BaseModel, decimal, Check, HealthReport, ProviderInfo, The `ImageProvider` Protocol and the values that cross it (ADR 0010, ROADMAP…, Identity and auth state, for `provider list`., One named healthcheck outcome, with enough detail to act on a failure. (+11 more)

### Community 20 - "Community 20"
Cohesion: 0.10
Nodes (24): model_validator, platformdirs, pydantic_settings, Self, AntigravitySettings, BatchSettings, ConfigSchema, default_config_toml() (+16 more)

### Community 21 - "Community 21"
Cohesion: 0.12
Nodes (23): re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 22 - "Community 22"
Cohesion: 0.19
Nodes (24): default_config_path(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., Spike S5 superseded decision D4: the dangerous flag is not opted into by…, Write a config file and return its path, so tests read as one expression. (+16 more)

### Community 23 - "Community 23"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, Yield `exc` and its `cause` links; `ExtractorError` nests the real failure… (+16 more)

### Community 24 - "Community 24"
Cohesion: 0.12
Nodes (17): Collection, NotFoundError, A referenced entity does not exist., PlaylistRepository, Playlist, PlaylistItem, PlaylistMeta, Playlist rows and their ordered items. (+9 more)

### Community 25 - "Community 25"
Cohesion: 0.12
Nodes (19): functools, IntEnum, rich_console, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.… (+11 more)

### Community 26 - "Community 26"
Cohesion: 0.14
Nodes (17): ChannelMeta, _Meta, PlaylistMeta, datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Default for `fetched_at`: an aware UTC instant, never a naive local one., Shared configuration and provenance for every fetched snapshot., A fetched YouTube channel. (+9 more)

### Community 27 - "Community 27"
Cohesion: 0.12
Nodes (21): `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, FakeSource, `FetchService` decisions: kind dispatch, the freshness rule, and what each…, If the fake drifts from `MetadataSource`, these tests stop meaning anything., A single video can afford the channel request, which populates…, One playlist request plus one channel request, regardless of item count., Channel-wide enumeration is a Phase 2 non-goal., `--refresh` must win even one second after a fetch. (+13 more)

### Community 28 - "Community 28"
Cohesion: 0.14
Nodes (21): Argument, metavar, rich_syntax, _as_toml(), _config_path(), init_(), path_(), command (+13 more)

### Community 29 - "Community 29"
Cohesion: 0.11
Nodes (21): Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)., `resolve()` returns both halves (ADR 0005); an empty id is never a valid result., A minimal valid video, so each test states only the field it is about., A fetched snapshot is a value; mutating one would desync it from `fetched_at`., `extra="forbid"` turns an unexpected yt-dlp field into a loud failure. yt-dlp's…, `fetched_at` is persisted as ISO-8601 UTC, so a naive datetime is ambiguous., Offsets are preserved as an instant, then stored in UTC., Optional columns default to the values the `video` table expects. (+13 more)

### Community 30 - "Community 30"
Cohesion: 0.13
Nodes (20): Engine, integration, Session, sessionmaker, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the…, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., _reclaim_orphans() (+12 more)

### Community 31 - "Community 31"
Cohesion: 0.15
Nodes (15): ProviderOutputMissingError, The provider reported success but produced no usable image., AntigravityProvider, Path, Generate an image by driving `agy` in headless mode., Report the CLI version, and auth as `unknown` rather than guessing. `unknown`…, Run one generation and copy its output into `workdir`., Assemble the command line. Never `--continue`: every image is a fresh run. (+7 more)

### Community 32 - "Community 32"
Cohesion: 0.13
Nodes (15): asyncio, GenerationRequest, GenerationResult, Path, One image to generate. Providers ignore what their capabilities disclaim., A produced image and the provenance needed to reproduce or audit it.…, Produce one image, or raise a `ProviderError` subclass. `workdir` is a caller-…, _digest() (+7 more)

### Community 33 - "Community 33"
Cohesion: 0.18
Nodes (20): Playlist, list_(), Argument, command, Context, handle_errors, help, Option (+12 more)

### Community 34 - "Community 34"
Cohesion: 0.11
Nodes (16): ComplianceError, PartialBatchError, Exception, A generated image violates the YouTube thumbnail requirements., A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., TemplateError (+8 more)

### Community 35 - "Community 35"
Cohesion: 0.13
Nodes (19): `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., A source wired to a fixture, plus the recorder that captured its calls., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get…, `position` comes from enumeration order because `playlist_index` is absent… (+11 more)

### Community 36 - "Community 36"
Cohesion: 0.14
Nodes (16): Console, json, pathlib, declarations(), main(), Path, Compare a committed graphify graph against a freshly extracted one. Only…, Ids of the nodes graphify parsed out of a file in this repository. (+8 more)

### Community 37 - "Community 37"
Cohesion: 0.12
Nodes (14): Protocol, FetchStore, ChannelMeta, datetime, MetadataSource, PlaylistMeta, VideoMeta, Take the metadata source and persistence layer the CLI selected. (+6 more)

### Community 38 - "Community 38"
Cohesion: 0.16
Nodes (12): FetchResult, FetchService, ResolvedUrl, Playlist rows written., Fetch YouTube metadata and persist it., Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order. (+4 more)

### Community 39 - "Community 39"
Cohesion: 0.12
Nodes (17): callback, count, envvar, is_eager, Context, handle_errors, help, Option (+9 more)

### Community 40 - "Community 40"
Cohesion: 0.15
Nodes (15): _fixture(), Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Load one recorded yt-dlp info dict. (+7 more)

### Community 41 - "Community 41"
Cohesion: 0.14
Nodes (16): PlaylistItem, JsonPayload, RenderableType, Repositories, Build the JSON payload and the Rich renderable from the **stored** rows.…, _view(), panel(), Build a titled Rich panel. (+8 more)

### Community 42 - "Community 42"
Cohesion: 0.13
Nodes (15): FetchResult, MetadataSource, fetch(), Argument, ChannelSource, Context, handle_errors, help (+7 more)

### Community 43 - "Community 43"
Cohesion: 0.18
Nodes (14): pydantic, parametrize, Invariants the provider boundary models enforce (ADR 0010, ROADMAP P3.1/P3.2)., Providers join this onto a path, so it must not be able to leave the workdir.…, The constraint must not reject what `PLAN.md` §6 and the test suites really use., A filename has a length limit even when every character is safe., `extra="forbid"` stops a caller asserting health that the checks contradict., A request is a value; mutating one after dispatch would desync it from its key. (+6 more)

### Community 44 - "Community 44"
Cohesion: 0.16
Nodes (10): ChannelRepository, Channel, ChannelMeta, Persist a playlist, its owning channel, its videos and its item order. Reports…, Persist a channel on its own (a channel URL was fetched)., Channel rows, keyed by YouTube channel id., Return the row for a YouTube channel id, or `None`., Insert or refresh a channel, preserving its ULID. (+2 more)

### Community 45 - "Community 45"
Cohesion: 0.15
Nodes (11): importlib_metadata, logging_handlers, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, bind(), clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Bind context onto every subsequent log record in this task (run id, provider,…, Drop all bound context. (+3 more)

### Community 46 - "Community 46"
Cohesion: 0.19
Nodes (14): list_(), Argument, command, Context, handle_errors, help, Option, List stored videos, most recently fetched first. (+6 more)

### Community 47 - "Community 47"
Cohesion: 0.19
Nodes (9): Video, VideoMeta, Look a video up by ULID or YouTube id, raising `NotFoundError` if absent. Both…, Insert or refresh a video, preserving its ULID. `channel_row_id` is supplied…, Videos, newest fetch first, optionally restricted to one channel., Persist one video and, when known, its channel. A single-video fetch can afford…, Video rows, keyed by YouTube video id., Return the row for a YouTube video id, or `None`. (+1 more)

### Community 48 - "Community 48"
Cohesion: 0.18
Nodes (12): Settings, Return the settings, or re-raise the failure that prevented loading them.…, Configuration is missing, malformed, or contains something it must not., SettingsError, _format_validation_error(), _parse_scalar(), Apply several dotted keys to the TOML file, validating the result once. All…, Parse a CLI value using TOML scalar rules, falling back to a bare string.… (+4 more)

### Community 49 - "Community 49"
Cohesion: 0.17
Nodes (9): Extractor, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes…, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch., test_permanent_failures_are_not_retried() (+1 more)

### Community 50 - "Community 50"
Cohesion: 0.21
Nodes (11): A supplied URL or identifier is not recognisable YouTube input., UrlError, _channel_handle(), classify_id(), _expect_kind(), UrlKind, Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1). Pure…, Classify a bare YouTube identifier by its shape. Order matters: a channel id… (+3 more)

### Community 51 - "Community 51"
Cohesion: 0.20
Nodes (12): A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs. (+4 more)

### Community 52 - "Community 52"
Cohesion: 0.20
Nodes (12): _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`., A full extract must carry the fields a flat entry cannot (S11). Also the only…, Re-assert the S11 field set, so a yt-dlp upgrade that changes it fails loudly. (+4 more)

### Community 53 - "Community 53"
Cohesion: 0.20
Nodes (9): datetime, _iso(), Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).…, When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, One item's `part_number` before and after a `playlist renumber`. Captured per…, Render an aware datetime as the ISO-8601 UTC string the schema stores., Renumbering, thumbforge_core_services_fetch (+1 more)

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
Cohesion: 0.22
Nodes (8): Image, ProviderPermanentError, The provider failed in a way that retrying cannot fix., _contrasting(), Path, Paint the image. Pure function of `request` and `digest`, so output is stable., Paste one reference thumbnail into a corner, clockwise from top-left. A missing…, Black on light backgrounds, white on dark, so the digest text is always legible.

### Community 58 - "Community 58"
Cohesion: 0.28
Nodes (9): ProviderAuthError, ProviderError, ProviderTimeoutError, ProviderTransientError, Base class for image-provider failures., The provider rejected our credentials, or none were cached., The provider failed in a way that may succeed on retry., The provider did not respond within its timeout. (+1 more)

### Community 59 - "Community 59"
Cohesion: 0.25
Nodes (5): ProviderCapabilities, What a provider can actually do, so callers degrade instead of guessing., Measured in spikes S3, S4 and S7 — see the module docstring., Deliberately permissive, so callers exercise their full request-building path., Deliberately unlike Antigravity, so a test cannot pass by coincidence.

### Community 60 - "Community 60"
Cohesion: 0.32
Nodes (7): get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline(), run_migrations_online()

### Community 61 - "Community 61"
Cohesion: 0.38
Nodes (3): Session, Build the three repositories over one session, so they share a transaction., Bind to the caller's session; the service owns the transaction.

### Community 62 - "Community 62"
Cohesion: 0.33
Nodes (6): _atomic_write(), Replace ``path`` atomically: write a sibling temp file, fsync, then rename. A…, Write the commented default configuration, refusing to clobber unless ``force``., write_default_config(), test_write_default_config_refuses_to_clobber(), test_write_is_atomic_and_leaves_no_temp_files()

### Community 63 - "Community 63"
Cohesion: 0.40
Nodes (3): field_validator, Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC., Refuse a key that is only dots, which the character class alone would allow.

### Community 64 - "Community 64"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 65 - "Community 65"
Cohesion: 0.40
Nodes (5): MonkeyPatch, A generated config must contain defaults, not whatever the current shell…, A valid env override must not let an invalid assignment be written to disk., test_environment_cannot_mask_an_invalid_file_value(), test_init_defaults_ignore_the_environment()

### Community 66 - "Community 66"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 720 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `YtDlpSource` connect `Community 49` to `Community 35`, `Community 40`, `Community 9`, `Community 42`, `Community 17`, `Community 51`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `fetch()` connect `Community 42` to `Community 33`, `Community 6`, `Community 38`, `Community 41`, `Community 46`, `Community 14`, `Community 30`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `emit()` connect `Community 14` to `Community 33`, `Community 36`, `Community 6`, `Community 42`, `Community 46`, `Community 25`, `Community 28`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `Repositories` (e.g. with `repos()` and `test_duplicate_video_in_a_playlist_is_listed_once()`) actually correct?**
  _`Repositories` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05048076923076923 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.050314465408805034 - nodes in this community are weakly interconnected._