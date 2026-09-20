# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1108 nodes · 2298 edges · 69 communities (51 shown, 18 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 236 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `06aa40bc`
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

## God Nodes (most connected - your core abstractions)
1. `Repositories` - 25 edges
2. `emit()` - 25 edges
3. `SettingsError` - 24 edges
4. `load_settings()` - 23 edges
5. `FakeSource` - 22 edges
6. `get_engine()` - 22 edges
7. `AssetStore` - 21 edges
8. `StubSource` - 20 edges
9. `AppContext` - 20 edges
10. `AssetKind` - 20 edges

## Surprising Connections (you probably didn't know these)
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `repos()` --uses--> `Repositories`  [INFERRED]
  tests/unit/test_repositories.py → src/thumbforge/storage/repositories.py
- `test_duplicate_video_in_a_playlist_is_listed_once()` --uses--> `Repositories`  [INFERRED]
  tests/unit/test_repositories.py → src/thumbforge/storage/repositories.py
- `test_flat_refetch_does_not_erase_richer_video_fields()` --uses--> `Repositories`  [INFERRED]
  tests/unit/test_repositories.py → src/thumbforge/storage/repositories.py
- `test_foreign_channel_videos_are_not_linked()` --uses--> `Repositories`  [INFERRED]
  tests/unit/test_repositories.py → src/thumbforge/storage/repositories.py

## Import Cycles
- None detected.

## Communities (69 total, 18 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (73): BaseModel, BaseSettings, model_validator, platformdirs, pydantic_settings, Self, Return the settings, or re-raise the failure that prevented loading them.…, Configuration is missing, malformed, or contains something it must not. (+65 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (58): BoundLogger, callback, CaptureFixture, count, envvar, is_eager, LogFormat, logging_handlers (+50 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (44): data_dir(), ChannelMeta, MonkeyPatch, Path, PlaylistMeta, VideoMeta, `fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP…, An initialised database, since every command here needs the schema. (+36 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (42): DeclarativeBase, enum, sqlalchemy, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations. (+34 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (36): parametrize, A supplied URL or identifier is not recognisable YouTube input., UrlError, What a URL or bare identifier turned out to be (ADR 0005)., ResolvedUrl, _channel_handle(), classify_id(), classify_url() (+28 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (34): importlib_metadata, json, main(), Path, Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, sys (+26 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (38): datetime, _channel(), _playlist(), ChannelMeta, PlaylistMeta, VideoMeta, Upsert semantics the rest of Phase 2 depends on (ROADMAP P2.3, PLAN.md §3)., `UNIQUE(playlist_id, position)` makes an in-place swap a constraint violation. (+30 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (35): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, asset_store() (+27 more)

### Community 8 - "Community 8"
Cohesion: 0.08
Nodes (29): field_validator, pydantic, PlaylistItemMeta, datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Default for `fetched_at`: an aware UTC instant, never a naive local one., Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC., One video's place in a playlist. (+21 more)

### Community 9 - "Community 9"
Cohesion: 0.10
Nodes (27): FakeSource, FakeStore, DateTime, `FetchService` decisions: kind dispatch, the freshness rule, and what each…, If the fake drifts from `MetadataSource`, these tests stop meaning anything., A single video can afford the channel request, which populates…, One playlist request plus one channel request, regardless of item count., Channel-wide enumeration is a Phase 2 non-goal. (+19 more)

### Community 10 - "Community 10"
Cohesion: 0.11
Nodes (25): RawInfo, RetryCallState, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, _duration(), _log_retry(), _published_at(), datetime, `YtDlpSource` — YouTube metadata via `yt-dlp`, no API key (ADR 0005, ROADMAP… (+17 more)

### Community 11 - "Community 11"
Cohesion: 0.08
Nodes (24): hashlib, pytest, Domain layer: models, errors and services. Imports nothing internal except…, _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, testcontainers_core_container, Integration tests using Testcontainers for database verification (ADR 0004)., Any (+16 more)

### Community 12 - "Community 12"
Cohesion: 0.13
Nodes (17): asyncio, collections_abc, ``thumbforge fetch`` — pull YouTube metadata into the database (ROADMAP P2.3)., Wiring and shared views for the YouTube metadata commands (ROADMAP P2.3).…, `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, _iso(), datetime, Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).… (+9 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (23): re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 14 - "Community 14"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, Exception, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against… (+16 more)

### Community 15 - "Community 15"
Cohesion: 0.13
Nodes (22): Argument, metavar, rich_syntax, _as_toml(), _config_path(), init_(), path_(), command (+14 more)

### Community 16 - "Community 16"
Cohesion: 0.16
Nodes (20): min, P, R, init_(), path_(), command, Context, help (+12 more)

### Community 17 - "Community 17"
Cohesion: 0.12
Nodes (14): Protocol, FetchStore, ChannelMeta, datetime, MetadataSource, PlaylistMeta, VideoMeta, Take the metadata source and persistence layer the CLI selected. (+6 more)

### Community 18 - "Community 18"
Cohesion: 0.16
Nodes (11): ChannelMeta, _Meta, PlaylistMeta, Shared configuration and provenance for every fetched snapshot., A fetched YouTube channel., A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, A fetched YouTube playlist and its ordered items., Number of items fetched, for the `playlist.item_count` column. (+3 more)

### Community 19 - "Community 19"
Cohesion: 0.14
Nodes (16): alembic, alembic_config, alembic_runtime_migration, alembic_script, Config, contextlib, sqlalchemy_pool, sqlite3 (+8 more)

### Community 20 - "Community 20"
Cohesion: 0.18
Nodes (13): dataclasses, rich_console, rich_panel, rich_table, main(), Root Typer application: global flags, context construction, sub-app…, ``thumbforge playlist`` — list and inspect stored playlists (ROADMAP P2.3)., The only module allowed to write to stdout. Every command produces one of two… (+5 more)

### Community 21 - "Community 21"
Cohesion: 0.15
Nodes (18): list_(), Argument, command, Context, handle_errors, help, Option, List stored videos, most recently fetched first. (+10 more)

### Community 22 - "Community 22"
Cohesion: 0.14
Nodes (14): Path, Return the hex SHA-256 of a file, read in chunks so large images stay off the…, sha256_file(), _fsync_dir(), Path, Session, sessionmaker, Return the absolute path on disk for ``asset``. (+6 more)

### Community 23 - "Community 23"
Cohesion: 0.16
Nodes (17): Engine, integration, Session, sessionmaker, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., session_factory(), session_scope() (+9 more)

### Community 24 - "Community 24"
Cohesion: 0.14
Nodes (17): JsonPayload, Build the JSON payload and the Rich renderable from the **stored** rows.…, _view(), panel(), Build a titled Rich panel., channel_payload(), item_payload(), item_rows() (+9 more)

### Community 25 - "Community 25"
Cohesion: 0.17
Nodes (17): list_(), Argument, command, Context, handle_errors, help, Option, List stored playlists, most recently fetched first. (+9 more)

### Community 26 - "Community 26"
Cohesion: 0.17
Nodes (15): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError, Error hierarchy and the exit codes it maps to. Every failure the user can… (+7 more)

### Community 27 - "Community 27"
Cohesion: 0.18
Nodes (10): PlaylistRepository, Playlist, PlaylistItem, Playlist rows and their ordered items., Return the row for a YouTube playlist id, or `None`., Look a playlist up by ULID or YouTube id, raising `NotFoundError` if absent., Insert or refresh a playlist. `channel_row_id` is required: the column is NOT…, Rewrite a playlist's items to exactly `video_ids`, in order. Rows are deleted… (+2 more)

### Community 28 - "Community 28"
Cohesion: 0.18
Nodes (13): Any, _fixture(), yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Load one recorded yt-dlp info dict., Extractor stub that returns a fixture and remembers how it was called. (+5 more)

### Community 29 - "Community 29"
Cohesion: 0.18
Nodes (14): DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., get_db_status(), Path, Inspect migration revision and file metadata for ``db_path``., Run Alembic upgrade to ``revision`` on ``db_path``., Reclaim free space, truncate the WAL, and delete unreferenced asset files.…, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the… (+6 more)

### Community 30 - "Community 30"
Cohesion: 0.19
Nodes (10): A metadata source failed., SourceError, FetchService, ResolvedUrl, Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order., A channel on its own; enumerating its videos is a Phase 2 non-goal. (+2 more)

### Community 31 - "Community 31"
Cohesion: 0.13
Nodes (15): S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., A source wired to a fixture, plus the recorder that captured its calls., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get…, `position` comes from enumeration order because `playlist_index` is absent…, _source() (+7 more)

### Community 32 - "Community 32"
Cohesion: 0.16
Nodes (12): os, pil, shutil, sqlalchemy_exc, sqlalchemy_orm, new_id(), Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits. (+4 more)

### Community 33 - "Community 33"
Cohesion: 0.14
Nodes (14): fetch(), Argument, ChannelSource, Context, handle_errors, help, Option, Fetch a video, playlist or channel and store its metadata. (+6 more)

### Community 34 - "Community 34"
Cohesion: 0.19
Nodes (9): Video, VideoMeta, Videos, newest fetch first, optionally restricted to one channel., Persist one video and, when known, its channel. A single-video fetch can afford…, Video rows, keyed by YouTube video id., Return the row for a YouTube video id, or `None`., Look a video up by ULID or YouTube id, raising `NotFoundError` if absent. Both…, Insert or refresh a video, preserving its ULID. `channel_row_id` is supplied… (+1 more)

### Community 35 - "Community 35"
Cohesion: 0.22
Nodes (12): get_engine(), Format a SQLite connection URL for SQLAlchemy., Create a SQLAlchemy engine configured for thumbforge SQLite usage., sqlite_url(), get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output. (+4 more)

### Community 36 - "Community 36"
Cohesion: 0.29
Nodes (12): init_db(), Ensure directory exists and upgrade DB to head. Returns: Tuple of…, Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_get_db_status_nonexistent_and_initialized(), test_init_db_and_idempotence(), test_session_scope_commits_on_success() (+4 more)

### Community 37 - "Community 37"
Cohesion: 0.26
Nodes (11): Console, RenderableType, emit(), JsonValue, Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.…, _json_context(), `emit` is the machine boundary: what it prints must always be parseable JSON., test_json_mode_output_round_trips() (+3 more)

### Community 38 - "Community 38"
Cohesion: 0.21
Nodes (11): AppContext, Per-invocation state built by the root callback and stored on ``ctx.obj``., ComplianceError, A generated image violates the YouTube thumbnail requirements., Machine mode contract: stdout carries command output, stderr carries the…, Ctrl-C during a batch must still leave machine mode with parseable output., test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), boom() (+3 more)

### Community 39 - "Community 39"
Cohesion: 0.21
Nodes (8): ChannelRepository, Channel, ChannelMeta, Persist a channel on its own (a channel URL was fetched)., Channel rows, keyed by YouTube channel id., Return the row for a YouTube channel id, or `None`., Insert or refresh a channel, preserving its ULID., Every channel, newest fetch first.

### Community 40 - "Community 40"
Cohesion: 0.17
Nodes (11): tenacity, `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch., test_out_of_range_timestamp_is_a_source_error(), test_satisfies_the_metadata_source_protocol(), thumbforge_sources, thumbforge_sources_ytdlp (+3 more)

### Community 41 - "Community 41"
Cohesion: 0.24
Nodes (10): functools, IntEnum, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.…, _report() (+2 more)

### Community 42 - "Community 42"
Cohesion: 0.18
Nodes (7): parametrize, The exit-code contract: a script parsing our status codes must never be…, Every error in CASES exits with the code documented in PLAN.md 5.1., test_error_maps_to_documented_exit_code(), test_keyboard_interrupt_exits_130(), test_only_transient_and_timeout_are_retryable(), test_unexpected_exception_is_not_swallowed()

### Community 43 - "Community 43"
Cohesion: 0.22
Nodes (7): PartialBatchError, Exception, A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., TemplateError, ThumbforgeError

### Community 44 - "Community 44"
Cohesion: 0.28
Nodes (9): A metadata source failed for a reason worth retrying (network, throttling).…, SourceTransientError, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs., test_retry_emits_a_log_event(), failing(), test_transient_failures_are_retried_then_reraised() (+1 more)

### Community 45 - "Community 45"
Cohesion: 0.38
Nodes (3): Session, Build the three repositories over one session, so they share a transaction., Bind to the caller's session; the service owns the transaction.

### Community 46 - "Community 46"
Cohesion: 0.33
Nodes (7): NotFoundError, A referenced entity does not exist., test_hint_and_code_reach_stderr(), boom(), A missing video will still be missing on attempt three; retrying just wastes…, test_permanent_failures_are_not_retried(), missing()

### Community 47 - "Community 47"
Cohesion: 0.29
Nodes (4): FetchResult, What was fetched, for rendering and for the `--json` contract. Counts are of…, Channel rows written., Playlist rows written.

### Community 48 - "Community 48"
Cohesion: 0.50
Nodes (4): Connection, ConnectionPoolEntry, Apply PRAGMA statements required by ADR 0004 on every SQLite connection., _set_sqlite_pragmas()

### Community 49 - "Community 49"
Cohesion: 0.50
Nodes (3): DbStatus, Whether the database is fully migrated to the latest revision., Migration status and storage health metadata.

### Community 50 - "Community 50"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 519 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `root()` connect `Community 1` to `Community 0`, `Community 20`, `Community 38`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `SettingsError` connect `Community 0` to `Community 33`, `Community 38`, `Community 43`, `Community 15`, `Community 20`, `Community 25`, `Community 26`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `emit()` connect `Community 37` to `Community 33`, `Community 38`, `Community 15`, `Community 16`, `Community 20`, `Community 21`, `Community 25`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `Repositories` (e.g. with `_view()` and `open_repositories()`) actually correct?**
  _`Repositories` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `emit()` (e.g. with `fetch()` and `list_()`) actually correct?**
  _`emit()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `SettingsError` (e.g. with `set_()` and `AppContext`) actually correct?**
  _`SettingsError` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._