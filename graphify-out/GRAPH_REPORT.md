# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1375 nodes · 2762 edges · 104 communities (68 shown, 36 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 258 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ecc25c5f`
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
- `repos()` --uses--> `Repositories`  [INFERRED]
  tests/unit/test_repositories.py → src/thumbforge/storage/repositories.py
- `test_only_transient_and_timeout_are_retryable()` --uses--> `ProviderAuthError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py
- `test_only_transient_and_timeout_are_retryable()` --uses--> `ProviderTimeoutError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py
- `test_only_transient_and_timeout_are_retryable()` --uses--> `ProviderTransientError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py

## Import Cycles
- None detected.

## Communities (104 total, 36 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (58): MonkeyPatch, ResolvedUrl, data_dir(), ChannelMeta, fixture, Path, VideoMeta, `fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP… (+50 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (45): The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Repositories, _channel(), _playlist(), ChannelMeta, PlaylistMeta, VideoMeta, `UNIQUE(playlist_id, position)` makes an in-place swap a constraint violation. (+37 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (38): Channel, FetchResult, MetadataSource, PlaylistItem, fetch(), Argument, ChannelSource, Context (+30 more)

### Community 3 - "Community 3"
Cohesion: 0.12
Nodes (35): DeclarativeBase, ChannelSource, Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations., Origin of channel metadata., RunKind, RunStatus, Storage layer for thumbforge (SQLite + SQLAlchemy 2.0 + Alembic). (+27 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (28): functools, IntEnum, json, rich_console, rich_panel, rich_syntax, rich_table, ``thumbforge config`` — inspect and edit the configuration file. (+20 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (29): asyncio, contextlib, RawInfo, RetryCallState, _duration(), _log_retry(), _published_at(), ChannelMeta (+21 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (26): BaseModel, decimal, Check, Cost, GenerationRequest, GenerationResult, HealthReport, ProviderInfo (+18 more)

### Community 7 - "Community 7"
Cohesion: 0.09
Nodes (31): FixtureRequest, ImageProvider, Generate one image per call. Implementations live in `providers/`., Identity and auth state. Must not raise for a merely unauthenticated provider., Every check this provider can run, with actionable detail on each failure., provider(), fixture, Path (+23 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (32): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, _backdate() (+24 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (29): entries(), _Entry, fixture, Registry behaviour: discovery, duplicate keys, and broken plugins (ADR 0010,…, If the stub drifts from `ImageProvider`, every test here stops meaning anything., A plugin needs only an entry point: the registry never imports it by name., Providers should not each have to handle `None`., `provider list` output must not reorder between runs. (+21 more)

### Community 10 - "Community 10"
Cohesion: 0.08
Nodes (27): ComplianceError, PartialBatchError, ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderTimeoutError, ProviderTransientError, Exception (+19 more)

### Community 11 - "Community 11"
Cohesion: 0.10
Nodes (26): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+18 more)

### Community 12 - "Community 12"
Cohesion: 0.13
Nodes (27): FakeProvider, JsonValue, Generate a deterministic placeholder image without leaving the machine., Accept a config mapping for registry symmetry; nothing in it is required., Path, `FakeProvider` behaviour the generic contract cannot express (PLAN.md §4.2,…, A test asserting style anchoring needs to see the reference in the output., Callers pass a run-scoped directory that may not exist yet. (+19 more)

### Community 13 - "Community 13"
Cohesion: 0.14
Nodes (27): Playlist, list_(), Argument, command, Context, handle_errors, help, Option (+19 more)

### Community 14 - "Community 14"
Cohesion: 0.10
Nodes (23): `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, FakeSource, ResolvedUrl, `FetchService` decisions: kind dispatch, the freshness rule, and what each…, If the fake drifts from `MetadataSource`, these tests stop meaning anything., A single video can afford the channel request, which populates…, One playlist request plus one channel request, regardless of item count., Channel-wide enumeration is a Phase 2 non-goal. (+15 more)

### Community 15 - "Community 15"
Cohesion: 0.10
Nodes (24): model_validator, platformdirs, pydantic_settings, Self, AntigravitySettings, BatchSettings, ConfigSchema, default_config_toml() (+16 more)

### Community 16 - "Community 16"
Cohesion: 0.18
Nodes (25): default_config_path(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., Spike S5 superseded decision D4: the dangerous flag is not opted into by…, Write a config file and return its path, so tests read as one expression. (+17 more)

### Community 17 - "Community 17"
Cohesion: 0.10
Nodes (20): alembic, alembic_config, alembic_runtime_migration, alembic_script, Config, Connection, ConnectionPoolEntry, sqlalchemy (+12 more)

### Community 18 - "Community 18"
Cohesion: 0.16
Nodes (24): BoundLogger, CaptureFixture, LogFormat, configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``., Configure structlog and the stdlib root logger. Safe to call more than once. (+16 more)

### Community 19 - "Community 19"
Cohesion: 0.13
Nodes (17): collections_abc, importlib_metadata, pathlib, pil, pytest, The JSON shape that crosses every machine-readable boundary. Defined in `core`…, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, `FakeProvider` — deterministic, offline image generation (PLAN.md §4.2, ROADMAP… (+9 more)

### Community 20 - "Community 20"
Cohesion: 0.12
Nodes (23): re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 21 - "Community 21"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, Yield `exc` and its `cause` links; `ExtractorError` nests the real failure… (+16 more)

### Community 22 - "Community 22"
Cohesion: 0.11
Nodes (23): Engine, integration, Session, sessionmaker, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the…, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., _reclaim_orphans() (+15 more)

### Community 23 - "Community 23"
Cohesion: 0.10
Nodes (22): pydantic, Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)., `resolve()` returns both halves (ADR 0005); an empty id is never a valid result., A minimal valid video, so each test states only the field it is about., A fetched snapshot is a value; mutating one would desync it from `fetched_at`., `extra="forbid"` turns an unexpected yt-dlp field into a loud failure. yt-dlp's…, `fetched_at` is persisted as ISO-8601 UTC, so a naive datetime is ambiguous., Offsets are preserved as an instant, then stored in UTC. (+14 more)

### Community 24 - "Community 24"
Cohesion: 0.15
Nodes (21): Any, importlib_util, ModuleType, _provider_params(), One param per registered provider, marking the ones that need the real world.…, _declaration(), _graph(), _module() (+13 more)

### Community 25 - "Community 25"
Cohesion: 0.13
Nodes (19): dataclasses, main(), Root Typer application: global flags, context construction, sub-app…, list_(), Argument, command, Context, handle_errors (+11 more)

### Community 26 - "Community 26"
Cohesion: 0.17
Nodes (21): DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., get_db_status(), init_db(), Inspect migration revision and file metadata for ``db_path``., Ensure directory exists and upgrade DB to head. Returns: Tuple of…, Run Alembic upgrade to ``revision`` on ``db_path``., upgrade_db() (+13 more)

### Community 27 - "Community 27"
Cohesion: 0.14
Nodes (20): parametrize, classify_url(), Resolve a YouTube URL, handle or bare id to its kind and identifier. A `watch`…, UrlKind, Which YouTube URLs and ids resolve to which kind (ADR 0005, ROADMAP P2.1)., `@` alone names no channel, so it must not resolve successfully., `urlparse` raises `ValueError` on these; the CLI only handles…, Every URL form thumbforge accepts, and the exact identifier it must extract. (+12 more)

### Community 28 - "Community 28"
Cohesion: 0.13
Nodes (17): E, os, shutil, sqlalchemy_exc, sqlalchemy_orm, new_id(), Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits. (+9 more)

### Community 29 - "Community 29"
Cohesion: 0.12
Nodes (12): What persisting a playlist actually wrote. Returned instead of the ORM row…, StoredPlaylist, FakeStore, ChannelMeta, DateTime, PlaylistMeta, VideoMeta, Spec behaviour 2: a playlist fetched inside the window is not re-fetched. (+4 more)

### Community 30 - "Community 30"
Cohesion: 0.13
Nodes (19): `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., A source wired to a fixture, plus the recorder that captured its calls., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get…, `position` comes from enumeration order because `playlist_index` is absent… (+11 more)

### Community 31 - "Community 31"
Cohesion: 0.14
Nodes (19): Argument, metavar, _as_toml(), _config_path(), init_(), path_(), command, Context (+11 more)

### Community 32 - "Community 32"
Cohesion: 0.16
Nodes (12): Collection, PlaylistRepository, Playlist, PlaylistItem, Playlist rows and their ordered items., Return the row for a YouTube playlist id, or `None`., Look a playlist up by ULID or YouTube id, raising `NotFoundError` if absent., Insert or refresh a playlist. `channel_row_id` is required: the column is NOT… (+4 more)

### Community 33 - "Community 33"
Cohesion: 0.15
Nodes (19): min, P, R, init_(), path_(), command, Context, help (+11 more)

### Community 34 - "Community 34"
Cohesion: 0.12
Nodes (14): Protocol, FetchStore, ChannelMeta, datetime, MetadataSource, PlaylistMeta, VideoMeta, Take the metadata source and persistence layer the CLI selected. (+6 more)

### Community 35 - "Community 35"
Cohesion: 0.16
Nodes (12): FetchResult, FetchService, ResolvedUrl, Playlist rows written., Fetch YouTube metadata and persist it., Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order. (+4 more)

### Community 36 - "Community 36"
Cohesion: 0.14
Nodes (17): Settings, Return the settings, or re-raise the failure that prevented loading them.…, Configuration is missing, malformed, or contains something it must not., SettingsError, _atomic_write(), _format_validation_error(), _parse_scalar(), Replace ``path`` atomically: write a sibling temp file, fsync, then rename. A… (+9 more)

### Community 37 - "Community 37"
Cohesion: 0.14
Nodes (14): Path, Return the hex SHA-256 of a file, read in chunks so large images stay off the…, sha256_file(), _fsync_dir(), Path, Session, sessionmaker, Return the absolute path on disk for ``asset``. (+6 more)

### Community 38 - "Community 38"
Cohesion: 0.19
Nodes (12): ChannelMeta, _Meta, PlaylistMeta, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Shared configuration and provenance for every fetched snapshot., A fetched YouTube channel., A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, A fetched YouTube playlist and its ordered items. (+4 more)

### Community 39 - "Community 39"
Cohesion: 0.15
Nodes (15): _fixture(), Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Load one recorded yt-dlp info dict. (+7 more)

### Community 40 - "Community 40"
Cohesion: 0.14
Nodes (12): Image, ProviderPermanentError, The provider failed in a way that retrying cannot fix., _contrasting(), _digest(), Path, Render one deterministic PNG into `workdir`. Raises before doing any work when…, Paint the image. Pure function of `request` and `digest`, so output is stable. (+4 more)

### Community 41 - "Community 41"
Cohesion: 0.18
Nodes (15): get_engine(), Path, Reclaim free space, truncate the WAL, and delete unreferenced asset files.…, Format a SQLite connection URL for SQLAlchemy., Create a SQLAlchemy engine configured for thumbforge SQLite usage., sqlite_url(), vacuum_db(), get_url() (+7 more)

### Community 42 - "Community 42"
Cohesion: 0.13
Nodes (11): Extractor, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, ResolvedUrl, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., Classify input without touching the network; `core.urls` does the work., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes… (+3 more)

### Community 43 - "Community 43"
Cohesion: 0.19
Nodes (13): A supplied URL or identifier is not recognisable YouTube input., UrlError, What a URL or bare identifier turned out to be (ADR 0005)., ResolvedUrl, _channel_handle(), classify_id(), _expect_kind(), UrlKind (+5 more)

### Community 44 - "Community 44"
Cohesion: 0.21
Nodes (13): Console, emit(), kv(), JsonValue, RenderableType, Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.…, Build a two-column key/value table, the default shape for ``show``-style…, _json_context() (+5 more)

### Community 45 - "Community 45"
Cohesion: 0.19
Nodes (9): Video, VideoMeta, Look a video up by ULID or YouTube id, raising `NotFoundError` if absent. Both…, Insert or refresh a video, preserving its ULID. `channel_row_id` is supplied…, Videos, newest fetch first, optionally restricted to one channel., Persist one video and, when known, its channel. A single-video fetch can afford…, Video rows, keyed by YouTube video id., Return the row for a YouTube video id, or `None`. (+1 more)

### Community 46 - "Community 46"
Cohesion: 0.17
Nodes (12): callback, count, envvar, is_eager, Context, handle_errors, help, Option (+4 more)

### Community 47 - "Community 47"
Cohesion: 0.17
Nodes (8): hashlib, Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 48 - "Community 48"
Cohesion: 0.20
Nodes (11): ProviderFactory, ProviderRegistryError, Provider discovery failed: duplicate key, or a plugin that will not load., Image providers: concrete `core.providers.ImageProvider` implementations and…, _discover(), get(), keys(), JsonValue (+3 more)

### Community 49 - "Community 49"
Cohesion: 0.20
Nodes (12): A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs. (+4 more)

### Community 50 - "Community 50"
Cohesion: 0.20
Nodes (12): _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`., A full extract must carry the fields a flat entry cannot (S11). Also the only…, Re-assert the S11 field set, so a yt-dlp upgrade that changes it fails loudly. (+4 more)

### Community 51 - "Community 51"
Cohesion: 0.21
Nodes (8): ChannelRepository, Channel, ChannelMeta, Persist a channel on its own (a channel URL was fetched)., Channel rows, keyed by YouTube channel id., Return the row for a YouTube channel id, or `None`., Insert or refresh a channel, preserving its ULID., Every channel, newest fetch first.

### Community 52 - "Community 52"
Cohesion: 0.20
Nodes (9): datetime, _iso(), Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).…, When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, One item's `part_number` before and after a `playlist renumber`. Captured per…, Render an aware datetime as the ISO-8601 UTC string the schema stores., Renumbering, thumbforge_core_services_fetch (+1 more)

### Community 53 - "Community 53"
Cohesion: 0.20
Nodes (10): logging_handlers, bind(), clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Bind context onto every subsequent log record in this task (run id, provider,…, Drop all bound context., structlog, structlog_stdlib (+2 more)

### Community 54 - "Community 54"
Cohesion: 0.29
Nodes (6): BaseSettings, default_data_dir(), default_state_dir(), Path, Effective configuration for one invocation: defaults, then file, then…, Settings

### Community 55 - "Community 55"
Cohesion: 0.29
Nodes (7): declarations(), main(), Path, Compare a committed graphify graph against a freshly extracted one. Only…, Ids of the nodes graphify parsed out of a file in this repository., Report whether the committed graph still describes the current declarations., sys

### Community 56 - "Community 56"
Cohesion: 0.25
Nodes (5): ProviderCapabilities, What this provider supports; callers check before sending a request., What a provider can actually do, so callers degrade instead of guessing., Deliberately permissive, so callers exercise their full request-building path., Deliberately unlike Antigravity, so a test cannot pass by coincidence.

### Community 57 - "Community 57"
Cohesion: 0.38
Nodes (3): Session, Build the three repositories over one session, so they share a transaction., Bind to the caller's session; the service owns the transaction.

### Community 58 - "Community 58"
Cohesion: 0.33
Nodes (5): enum, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., UrlKind, StrEnum

### Community 59 - "Community 59"
Cohesion: 0.33
Nodes (5): field_validator, datetime, Default for `fetched_at`: an aware UTC instant, never a naive local one., Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC., _utcnow()

### Community 60 - "Community 60"
Cohesion: 0.40
Nodes (5): level_from_flags(), Resolve the console level from the global flags. ``--quiet`` wins over ``-v``…, parametrize, --quiet outranks -v: an explicit request for silence beats a scripted -v., test_flag_to_level_mapping()

### Community 61 - "Community 61"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 62 - "Community 62"
Cohesion: 0.40
Nodes (5): MonkeyPatch, A generated config must contain defaults, not whatever the current shell…, A valid env override must not let an invalid assignment be written to disk., test_environment_cannot_mask_an_invalid_file_value(), test_init_defaults_ignore_the_environment()

### Community 63 - "Community 63"
Cohesion: 0.67
Nodes (4): NotFoundError, A referenced entity does not exist., test_hint_and_code_reach_stderr(), boom()

### Community 64 - "Community 64"
Cohesion: 0.50
Nodes (3): PlaylistItemMeta, One video's place in a playlist., PlaylistMeta

### Community 65 - "Community 65"
Cohesion: 0.50
Nodes (3): _deep_merge(), Build settings where the environment outranks the TOML file. File values cannot…, Merge ``override`` into ``base``, recursing into nested tables.

### Community 66 - "Community 66"
Cohesion: 0.50
Nodes (3): DbStatus, Whether the database is fully migrated to the latest revision., Migration status and storage health metadata.

### Community 67 - "Community 67"
Cohesion: 0.50
Nodes (3): PlaylistMeta, Persist a playlist, its owning channel, its videos and its item order. Reports…, StoredPlaylist

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 667 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **36 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PlaylistRepository` connect `Community 32` to `Community 57`, `Community 52`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `fetch()` connect `Community 2` to `Community 35`, `Community 44`, `Community 13`, `Community 22`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Why does `Repositories` connect `Community 1` to `Community 67`, `Community 45`, `Community 51`, `Community 52`, `Community 22`, `Community 57`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `FakeProvider` (e.g. with `Check` and `GenerationRequest`) actually correct?**
  _`FakeProvider` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `Repositories` (e.g. with `repos()` and `test_duplicate_video_in_a_playlist_is_listed_once()`) actually correct?**
  _`Repositories` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05222734254992319 - nodes in this community are weakly interconnected._