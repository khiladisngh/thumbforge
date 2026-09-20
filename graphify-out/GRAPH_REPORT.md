# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1071 nodes · 2317 edges · 69 communities (55 shown, 14 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 260 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `41788140`
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
1. `ChannelMeta` - 33 edges
2. `VideoMeta` - 30 edges
3. `PlaylistMeta` - 28 edges
4. `Repositories` - 28 edges
5. `YtDlpSource` - 26 edges
6. `StubSource` - 25 edges
7. `emit()` - 25 edges
8. `SettingsError` - 24 edges
9. `ResolvedUrl` - 24 edges
10. `load_settings()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_sqlite_database_in_container()` --uses--> `ChannelSource`  [INFERRED]
  tests/integration/test_db_container.py → src/thumbforge/core/enums.py
- `test_session_scope_commits_on_success()` --uses--> `ChannelSource`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/core/enums.py
- `test_session_scope_rolls_back_on_error()` --uses--> `ChannelSource`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/core/enums.py
- `test_vacuum_db_success_and_missing_error()` --uses--> `ChannelSource`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/core/enums.py

## Import Cycles
- None detected.

## Communities (69 total, 14 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic_settings, Self, Return the settings, or re-raise the failure that prevented loading them.… (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (55): DeclarativeBase, E, enum, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations. (+47 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (30): A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, VideoMeta, `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, FakeSource, FakeStore, DateTime, `FetchService` decisions: kind dispatch, the freshness rule, and what each…, If the fake drifts from `MetadataSource`, these tests stop meaning anything. (+22 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (37): MonkeyPatch, Path, `fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP…, The `PLAN.md` §5.3 shape: panel, `#`/`Part` table, then the stored counts., Spec acceptance criteria: same table, `(cached)`, and no source call., `--refresh` bypasses the freshness rule., Spec behaviour 6: a single JSON object, keyed by what was fetched., The item array is the machine form of the table, so order and `part_number`… (+29 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (35): parametrize, A supplied URL or identifier is not recognisable YouTube input., UrlError, What a URL or bare identifier turned out to be (ADR 0005)., ResolvedUrl, _channel_handle(), classify_id(), classify_url() (+27 more)

### Community 5 - "Community 5"
Cohesion: 0.14
Nodes (31): The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Repositories, _channel(), _playlist(), Upsert semantics the rest of Phase 2 depends on (ROADMAP P2.3, PLAN.md §3)., `UNIQUE(playlist_id, position)` makes an in-place swap a constraint violation., A video dropped from a playlist keeps its row: its thumbnails are still real., `UNIQUE(playlist_id, video_id)` cannot represent a repeat, so the first place… (+23 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (27): field_validator, pydantic, _Meta, datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Default for `fetched_at`: an aware UTC instant, never a naive local one., Shared configuration and provenance for every fetched snapshot., Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC. (+19 more)

### Community 7 - "Community 7"
Cohesion: 0.15
Nodes (28): BoundLogger, CaptureFixture, LogFormat, bind(), configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``. (+20 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (24): Argument, importlib_metadata, metavar, rich_syntax, _as_toml(), _config_path(), init_(), path_() (+16 more)

### Community 9 - "Community 9"
Cohesion: 0.11
Nodes (24): collections_abc, re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure. (+16 more)

### Community 10 - "Community 10"
Cohesion: 0.11
Nodes (17): Extractor, PlaylistItemMeta, PlaylistMeta, One video's place in a playlist., A fetched YouTube playlist and its ordered items., Number of items fetched, for the `playlist.item_count` column., Turn an unexpected yt-dlp info-dict *shape* into a `SourceError`. yt-dlp parses…, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation). (+9 more)

### Community 11 - "Community 11"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, Yield `exc` and its `cause` links; `ExtractorError` nests the real failure… (+16 more)

### Community 12 - "Community 12"
Cohesion: 0.16
Nodes (20): min, P, R, init_(), path_(), command, Context, help (+12 more)

### Community 13 - "Community 13"
Cohesion: 0.13
Nodes (19): datetime, tenacity, `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get… (+11 more)

### Community 14 - "Community 14"
Cohesion: 0.13
Nodes (14): alembic, alembic_config, alembic_runtime_migration, alembic_script, contextlib, sqlalchemy, sqlalchemy_pool, sqlite3 (+6 more)

### Community 15 - "Community 15"
Cohesion: 0.15
Nodes (18): Engine, integration, Session, sessionmaker, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the…, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., _reclaim_orphans() (+10 more)

### Community 16 - "Community 16"
Cohesion: 0.13
Nodes (18): io, pil, sqlalchemy_orm, asset_store(), _backdate(), _make_jpeg_bytes(), fixture, Path (+10 more)

### Community 17 - "Community 17"
Cohesion: 0.12
Nodes (16): logging_handlers, pathlib, pytest, clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Drop all bound context., structlog, structlog_stdlib (+8 more)

### Community 18 - "Community 18"
Cohesion: 0.16
Nodes (17): RawInfo, RetryCallState, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, _duration(), _log_retry(), _published_at(), datetime, `YtDlpSource` — YouTube metadata via `yt-dlp`, no API key (ADR 0005, ROADMAP… (+9 more)

### Community 19 - "Community 19"
Cohesion: 0.15
Nodes (11): FetchResult, FetchService, Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order., A channel on its own; enumerating its videos is a Phase 2 non-goal., Whether a stored playlist is recent enough to skip the network., What was fetched, for rendering and for the `--json` contract. Counts are of… (+3 more)

### Community 20 - "Community 20"
Cohesion: 0.13
Nodes (18): RenderableType, Any, Build the JSON payload and the Rich renderable from the **stored** rows.…, _view(), panel(), Build a titled Rich panel., item_payload(), item_rows() (+10 more)

### Community 21 - "Community 21"
Cohesion: 0.12
Nodes (17): callback, count, envvar, is_eager, Context, handle_errors, help, Option (+9 more)

### Community 22 - "Community 22"
Cohesion: 0.17
Nodes (17): list_(), Argument, command, Context, handle_errors, help, Option, List stored playlists, most recently fetched first. (+9 more)

### Community 23 - "Community 23"
Cohesion: 0.21
Nodes (16): Path, Unit tests for ``thumbforge db`` CLI commands (ADR 0004, Phase 1 spec)., test_db_init_creates_database_and_is_idempotent(), test_db_init_json_mode(), test_db_json_error_stream_contract(), test_db_path_command(), test_db_path_json_mode(), test_db_status_command() (+8 more)

### Community 24 - "Community 24"
Cohesion: 0.15
Nodes (15): data_dir(), _fixture(), Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an… (+7 more)

### Community 25 - "Community 25"
Cohesion: 0.19
Nodes (14): Console, rich_console, rich_panel, rich_table, emit(), JsonValue, The only module allowed to write to stdout. Every command produces one of two…, Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.… (+6 more)

### Community 26 - "Community 26"
Cohesion: 0.19
Nodes (12): dataclasses, main(), Root Typer application: global flags, context construction, sub-app…, ``thumbforge playlist`` — list and inspect stored playlists (ROADMAP P2.3)., ``thumbforge video`` — list and inspect stored videos (ROADMAP P2.3)., channel_payload(), Channel, Channel fields common to every command that mentions one. (+4 more)

### Community 27 - "Community 27"
Cohesion: 0.17
Nodes (15): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError, Error hierarchy and the exit codes it maps to. Every failure the user can… (+7 more)

### Community 28 - "Community 28"
Cohesion: 0.14
Nodes (12): Path, Return the hex SHA-256 of a file, read in chunks so large images stay off the…, sha256_file(), _fsync_dir(), Path, Session, sessionmaker, Return the absolute path on disk for ``asset``. (+4 more)

### Community 29 - "Community 29"
Cohesion: 0.25
Nodes (15): get_engine(), init_db(), Ensure directory exists and upgrade DB to head. Returns: Tuple of…, Create a SQLAlchemy engine configured for thumbforge SQLite usage., Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_engine_pragmas_on_memory() (+7 more)

### Community 30 - "Community 30"
Cohesion: 0.18
Nodes (10): PlaylistRepository, Playlist, PlaylistItem, Playlist rows and their ordered items., Return the row for a YouTube playlist id, or `None`., Look a playlist up by ULID or YouTube id, raising `NotFoundError` if absent., Insert or refresh a playlist. `channel_row_id` is required: the column is NOT…, Rewrite a playlist's items to exactly `video_ids`, in order. Rows are deleted… (+2 more)

### Community 31 - "Community 31"
Cohesion: 0.18
Nodes (15): list_(), Argument, command, Context, handle_errors, help, Option, List stored videos, most recently fetched first. (+7 more)

### Community 32 - "Community 32"
Cohesion: 0.22
Nodes (14): AssetKind, Functional role of a stored image asset., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, _make_png_bytes(), MonkeyPatch, A failed insert never unlinks the published file, and a retry adopts it. A…, `db vacuum` deletes expired unreferenced files and stale tmp entries (ADR 0011). (+6 more)

### Community 33 - "Community 33"
Cohesion: 0.16
Nodes (7): Session, ChannelRepository, Channel, Persist a channel on its own (a channel URL was fetched)., Channel rows, keyed by YouTube channel id., Return the row for a YouTube channel id, or `None`., Every channel, newest fetch first.

### Community 34 - "Community 34"
Cohesion: 0.16
Nodes (11): NotFoundError, PartialBatchError, Exception, A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., A referenced entity does not exist., TemplateError (+3 more)

### Community 35 - "Community 35"
Cohesion: 0.18
Nodes (8): ChannelMeta, A fetched YouTube channel., FetchStore, datetime, Protocol, The persistence surface a fetch needs, satisfied by `storage.Repositories`., Persist one video and, when known, its channel. A single-video fetch can afford…, Persist a playlist, its owning channel, its videos and its item order. Returns…

### Community 36 - "Community 36"
Cohesion: 0.20
Nodes (13): _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, Record `tests/fixtures/ytdlp/*.json` from live YouTube, and assert the S11…, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`., A full extract must carry the fields a flat entry cannot (S11). Also the only… (+5 more)

### Community 37 - "Community 37"
Cohesion: 0.24
Nodes (10): asyncio, ``thumbforge fetch`` — pull YouTube metadata into the database (ROADMAP P2.3)., build_source(), ChannelSource, Wiring and shared views for the YouTube metadata commands (ROADMAP P2.3).…, Select a metadata source. The Data API source is a Phase 8 extra, so asking for…, Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).…, thumbforge_core_errors (+2 more)

### Community 38 - "Community 38"
Cohesion: 0.19
Nodes (10): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+2 more)

### Community 39 - "Community 39"
Cohesion: 0.17
Nodes (8): hashlib, Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 40 - "Community 40"
Cohesion: 0.21
Nodes (11): AppContext, Per-invocation state built by the root callback and stored on ``ctx.obj``., ComplianceError, A generated image violates the YouTube thumbnail requirements., Machine mode contract: stdout carries command output, stderr carries the…, Ctrl-C during a batch must still leave machine mode with parseable output., test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), boom() (+3 more)

### Community 41 - "Community 41"
Cohesion: 0.20
Nodes (12): A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs. (+4 more)

### Community 42 - "Community 42"
Cohesion: 0.24
Nodes (10): functools, IntEnum, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.…, _report() (+2 more)

### Community 43 - "Community 43"
Cohesion: 0.22
Nodes (9): os, shutil, sqlalchemy_exc, new_id(), Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of ``data``., sha256_bytes() (+1 more)

### Community 44 - "Community 44"
Cohesion: 0.18
Nodes (6): Take the metadata source and persistence layer the CLI selected., MetadataSource, Protocol, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch., test_satisfies_the_metadata_source_protocol(), timedelta

### Community 45 - "Community 45"
Cohesion: 0.24
Nodes (7): Video, Videos, newest fetch first, optionally restricted to one channel., Video rows, keyed by YouTube video id., Return the row for a YouTube video id, or `None`., Look a video up by ULID or YouTube id, raising `NotFoundError` if absent. Both…, Insert or refresh a video, preserving its ULID. `channel_row_id` is supplied…, VideoRepository

### Community 46 - "Community 46"
Cohesion: 0.18
Nodes (7): parametrize, The exit-code contract: a script parsing our status codes must never be…, Every error in CASES exits with the code documented in PLAN.md 5.1., test_error_maps_to_documented_exit_code(), test_keyboard_interrupt_exits_130(), test_only_transient_and_timeout_are_retryable(), test_unexpected_exception_is_not_swallowed()

### Community 47 - "Community 47"
Cohesion: 0.29
Nodes (10): Config, _alembic_config(), get_db_status(), Path, Build an Alembic configuration targeting ``db_path``., Inspect migration revision and file metadata for ``db_path``., Run Alembic upgrade to ``revision`` on ``db_path``., Format a SQLite connection URL for SQLAlchemy. (+2 more)

### Community 48 - "Community 48"
Cohesion: 0.20
Nodes (10): fetch(), Argument, ChannelSource, Context, handle_errors, help, Option, Fetch a video, playlist or channel and store its metadata. (+2 more)

### Community 49 - "Community 49"
Cohesion: 0.33
Nodes (6): json, main(), Path, Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys

### Community 50 - "Community 50"
Cohesion: 0.33
Nodes (7): DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., Reclaim free space, truncate the WAL, and delete unreferenced asset files.…, vacuum_db(), parametrize, A non-positive window would let vacuum delete an in-flight write's files., test_vacuum_rejects_non_positive_grace()

### Community 51 - "Community 51"
Cohesion: 0.29
Nodes (5): _iso(), datetime, When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, Render an aware datetime as the ISO-8601 UTC string the schema stores., Insert or refresh a channel, preserving its ULID.

### Community 52 - "Community 52"
Cohesion: 0.33
Nodes (6): AssetError, An asset could not be written, verified, or identified., Bytes Pillow cannot identify are rejected, and the temp file is cleaned up., A valid image outside the JPEG/PNG/WebP allowlist is rejected with a hint., test_put_corrupted_or_non_image_raises(), test_put_unsupported_mime_raises()

### Community 53 - "Community 53"
Cohesion: 0.50
Nodes (4): Connection, ConnectionPoolEntry, Apply PRAGMA statements required by ADR 0004 on every SQLite connection., _set_sqlite_pragmas()

### Community 54 - "Community 54"
Cohesion: 0.50
Nodes (3): DbStatus, Whether the database is fully migrated to the latest revision., Migration status and storage health metadata.

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 491 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PlaylistRepository` connect `Community 30` to `Community 33`, `Community 10`, `Community 37`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `SettingsError` connect `Community 0` to `Community 34`, `Community 37`, `Community 8`, `Community 40`, `Community 22`, `Community 25`, `Community 27`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `YtDlpSource` connect `Community 10` to `Community 2`, `Community 35`, `Community 4`, `Community 37`, `Community 41`, `Community 44`, `Community 13`, `Community 18`, `Community 55`, `Community 24`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `ChannelMeta` (e.g. with `FetchResult` and `FetchStore`) actually correct?**
  _`ChannelMeta` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `VideoMeta` (e.g. with `FetchResult` and `FetchStore`) actually correct?**
  _`VideoMeta` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `PlaylistMeta` (e.g. with `FetchResult` and `FetchStore`) actually correct?**
  _`PlaylistMeta` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `Repositories` (e.g. with `_view()` and `open_repositories()`) actually correct?**
  _`Repositories` has 19 INFERRED edges - model-reasoned connections that need verification._