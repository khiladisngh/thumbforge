# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1123 nodes · 2303 edges · 71 communities (51 shown, 20 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 232 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6c0504c8`
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

## God Nodes (most connected - your core abstractions)
1. `Repositories` - 26 edges
2. `emit()` - 25 edges
3. `SettingsError` - 24 edges
4. `load_settings()` - 23 edges
5. `get_engine()` - 22 edges
6. `AssetStore` - 21 edges
7. `StubSource` - 21 edges
8. `AssetKind` - 20 edges
9. `AppContext` - 20 edges
10. `ThumbforgeError` - 19 edges

## Surprising Connections (you probably didn't know these)
- `repeating()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_cli_fetch.py → src/thumbforge/core/models.py
- `missing()` --calls--> `NotFoundError`  [INFERRED]
  tests/unit/test_ytdlp.py → src/thumbforge/core/errors.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `failing()` --calls--> `SourceTransientError`  [INFERRED]
  tests/unit/test_ytdlp.py → src/thumbforge/core/errors.py
- `_playlist()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_repositories.py → src/thumbforge/core/models.py

## Import Cycles
- None detected.

## Communities (71 total, 20 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (73): BaseModel, BaseSettings, model_validator, platformdirs, pydantic_settings, Self, Return the settings, or re-raise the failure that prevented loading them.…, Configuration is missing, malformed, or contains something it must not. (+65 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (60): BoundLogger, callback, CaptureFixture, count, envvar, is_eager, LogFormat, logging_handlers (+52 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (56): DeclarativeBase, E, enum, sqlalchemy, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run. (+48 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (54): Argument, Console, functools, IntEnum, metavar, rich_syntax, _as_toml(), _config_path() (+46 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (40): FetchResult, FetchService, ResolvedUrl, Playlist rows written., Fetch YouTube metadata and persist it., Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order. (+32 more)

### Community 5 - "Community 5"
Cohesion: 0.06
Nodes (48): MonkeyPatch, data_dir(), ChannelMeta, fixture, Path, PlaylistMeta, VideoMeta, `fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP… (+40 more)

### Community 6 - "Community 6"
Cohesion: 0.06
Nodes (30): Channel, Playlist, PlaylistItem, Session, ChannelRepository, PlaylistRepository, ChannelMeta, VideoMeta (+22 more)

### Community 7 - "Community 7"
Cohesion: 0.07
Nodes (34): importlib_metadata, json, main(), Path, Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, sys (+26 more)

### Community 8 - "Community 8"
Cohesion: 0.08
Nodes (31): parametrize, A supplied URL or identifier is not recognisable YouTube input., UrlError, _channel_handle(), classify_id(), classify_url(), _expect_kind(), UrlKind (+23 more)

### Community 9 - "Community 9"
Cohesion: 0.13
Nodes (29): _channel(), _playlist(), ChannelMeta, PlaylistMeta, VideoMeta, Upsert semantics the rest of Phase 2 depends on (ROADMAP P2.3, PLAN.md §3)., `UNIQUE(playlist_id, position)` makes an in-place swap a constraint violation., A video dropped from a playlist keeps its row: its thumbnails are still real. (+21 more)

### Community 10 - "Community 10"
Cohesion: 0.10
Nodes (23): pydantic, PlaylistItemMeta, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, One video's place in a playlist., Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)., A minimal valid video, so each test states only the field it is about., A fetched snapshot is a value; mutating one would desync it from `fetched_at`., `extra="forbid"` turns an unexpected yt-dlp field into a loud failure. yt-dlp's… (+15 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (23): re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 12 - "Community 12"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, Exception, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against… (+16 more)

### Community 13 - "Community 13"
Cohesion: 0.14
Nodes (22): min, P, R, init_(), path_(), command, Context, help (+14 more)

### Community 14 - "Community 14"
Cohesion: 0.13
Nodes (20): Engine, integration, Session, sessionmaker, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the…, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error., _reclaim_orphans() (+12 more)

### Community 15 - "Community 15"
Cohesion: 0.13
Nodes (18): io, pil, sqlalchemy_orm, asset_store(), _backdate(), _make_jpeg_bytes(), fixture, Path (+10 more)

### Community 16 - "Community 16"
Cohesion: 0.12
Nodes (14): MetadataSource, Protocol, FetchStore, ChannelMeta, datetime, PlaylistMeta, VideoMeta, Take the metadata source and persistence layer the CLI selected. (+6 more)

### Community 17 - "Community 17"
Cohesion: 0.15
Nodes (18): list_(), Argument, command, Context, handle_errors, help, Option, List stored videos, most recently fetched first. (+10 more)

### Community 18 - "Community 18"
Cohesion: 0.15
Nodes (15): Any, _fixture(), yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Load one recorded yt-dlp info dict., Extractor stub that returns a fixture and remembers how it was called. (+7 more)

### Community 19 - "Community 19"
Cohesion: 0.17
Nodes (17): Config, DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., _alembic_config(), get_db_status(), Path, Build an Alembic configuration targeting ``db_path``., Inspect migration revision and file metadata for ``db_path``. (+9 more)

### Community 20 - "Community 20"
Cohesion: 0.26
Nodes (12): ``thumbforge fetch`` — pull YouTube metadata into the database (ROADMAP P2.3)., Wiring and shared views for the YouTube metadata commands (ROADMAP P2.3).…, `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).…, `FetchService` decisions: kind dispatch, the freshness rule, and what each…, thumbforge_cli_render, thumbforge_core_enums, thumbforge_core_errors (+4 more)

### Community 21 - "Community 21"
Cohesion: 0.12
Nodes (14): alembic_config, alembic_runtime_migration, alembic_script, Connection, ConnectionPoolEntry, contextlib, sqlalchemy_pool, sqlite3 (+6 more)

### Community 22 - "Community 22"
Cohesion: 0.15
Nodes (16): RenderableType, JsonPayload, Build the JSON payload and the Rich renderable from the **stored** rows.…, _view(), channel_payload(), item_payload(), item_rows(), playlist_payload() (+8 more)

### Community 23 - "Community 23"
Cohesion: 0.17
Nodes (15): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError, Error hierarchy and the exit codes it maps to. Every failure the user can… (+7 more)

### Community 24 - "Community 24"
Cohesion: 0.13
Nodes (12): PartialBatchError, Exception, A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., A metadata source failed., SourceError, TemplateError (+4 more)

### Community 25 - "Community 25"
Cohesion: 0.14
Nodes (12): Path, Return the hex SHA-256 of a file, read in chunks so large images stay off the…, sha256_file(), _fsync_dir(), Path, Session, sessionmaker, Return the absolute path on disk for ``asset``. (+4 more)

### Community 26 - "Community 26"
Cohesion: 0.19
Nodes (11): ChannelMeta, _Meta, PlaylistMeta, Shared configuration and provenance for every fetched snapshot., A fetched YouTube channel., A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, A fetched YouTube playlist and its ordered items., Number of items fetched, for the `playlist.item_count` column. (+3 more)

### Community 27 - "Community 27"
Cohesion: 0.22
Nodes (14): asyncio, RawInfo, _duration(), _published_at(), datetime, `YtDlpSource` — YouTube metadata via `yt-dlp`, no API key (ADR 0005, ROADMAP…, Read a string field, treating a missing key and an explicit `None` alike. Both…, Recover an upload instant from `timestamp`, or `None` if yt-dlp reported none.… (+6 more)

### Community 28 - "Community 28"
Cohesion: 0.19
Nodes (15): list_(), Argument, command, Context, handle_errors, help, Option, List stored playlists, most recently fetched first. (+7 more)

### Community 29 - "Community 29"
Cohesion: 0.22
Nodes (14): AssetKind, Functional role of a stored image asset., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, _make_png_bytes(), MonkeyPatch, A failed insert never unlinks the published file, and a retry adopts it. A…, `db vacuum` deletes expired unreferenced files and stale tmp entries (ADR 0011). (+6 more)

### Community 30 - "Community 30"
Cohesion: 0.14
Nodes (14): What persisting a playlist actually wrote. Returned instead of the ORM row…, StoredPlaylist, PlaylistMeta, The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Persist a playlist, its owning channel, its videos and its item order. Reports…, Repositories, `video show` takes either, and the two are only distinguishable by trying., Exit 3 and an actionable hint, not an empty result (spec behaviour 4). (+6 more)

### Community 31 - "Community 31"
Cohesion: 0.27
Nodes (14): get_engine(), init_db(), Ensure directory exists and upgrade DB to head. Returns: Tuple of…, Create a SQLAlchemy engine configured for thumbforge SQLite usage., Path, Unit tests for database engine, pragmas, sessions, and status helpers (ADR…, test_engine_pragmas_on_file(), test_engine_pragmas_on_memory() (+6 more)

### Community 32 - "Community 32"
Cohesion: 0.15
Nodes (10): Extractor, What a URL or bare identifier turned out to be (ADR 0005)., ResolvedUrl, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., Classify input without touching the network; `core.urls` does the work., YtDlpSource (+2 more)

### Community 33 - "Community 33"
Cohesion: 0.16
Nodes (9): pathlib, pytest, Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1). Pure…, testcontainers_core_container, Shared fixtures. Establishes ``tests/`` as the pytest root., Integration tests using Testcontainers for database verification (ADR 0004)., Record `tests/fixtures/ytdlp/*.json` from live YouTube, and assert the S11…, Which YouTube URLs and ids resolve to which kind (ADR 0005, ROADMAP P2.1). (+1 more)

### Community 34 - "Community 34"
Cohesion: 0.14
Nodes (14): fetch(), Argument, ChannelSource, Context, handle_errors, help, Option, Fetch a video, playlist or channel and store its metadata. (+6 more)

### Community 35 - "Community 35"
Cohesion: 0.18
Nodes (9): RetryCallState, _log_retry(), Turn an unexpected yt-dlp info-dict *shape* into a `SourceError`. yt-dlp parses…, Full extract of one video, so `description` and `published_at` are populated., Flat extract of a playlist and its items, in playlist order. One network round…, Channel metadata only — never its video list. Enumerating a channel is a non-…, Extract off the event loop, retrying only transient failures (PLAN.md §7.2)., Emit the `retry` event the Phase 2 acceptance criteria assert on. (+1 more)

### Community 36 - "Community 36"
Cohesion: 0.23
Nodes (9): rich_console, main(), Root Typer application: global flags, context construction, sub-app…, ``thumbforge playlist`` — list and inspect stored playlists (ROADMAP P2.3)., ``thumbforge video`` — list and inspect stored videos (ROADMAP P2.3)., thumbforge, thumbforge_cli, thumbforge_cli_errors (+1 more)

### Community 37 - "Community 37"
Cohesion: 0.15
Nodes (13): S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., A source wired to a fixture, plus the recorder that captured its calls., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get…, _source(), test_fetch_channel_accepts_a_handle() (+5 more)

### Community 38 - "Community 38"
Cohesion: 0.17
Nodes (8): hashlib, Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 39 - "Community 39"
Cohesion: 0.20
Nodes (12): _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`., A full extract must carry the fields a flat entry cannot (S11). Also the only…, Re-assert the S11 field set, so a yt-dlp upgrade that changes it fails loudly. (+4 more)

### Community 40 - "Community 40"
Cohesion: 0.18
Nodes (10): datetime, tenacity, `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch., test_satisfies_the_metadata_source_protocol(), thumbforge_sources, thumbforge_sources_ytdlp, types (+2 more)

### Community 41 - "Community 41"
Cohesion: 0.22
Nodes (9): os, shutil, sqlalchemy_exc, new_id(), Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of ``data``., sha256_bytes() (+1 more)

### Community 42 - "Community 42"
Cohesion: 0.25
Nodes (7): NotFoundError, A referenced entity does not exist., The exit-code contract: a script parsing our status codes must never be…, test_hint_and_code_reach_stderr(), boom(), test_only_transient_and_timeout_are_retryable(), test_unexpected_exception_is_not_swallowed()

### Community 43 - "Community 43"
Cohesion: 0.29
Nodes (3): alembic, collections_abc, Unit tests for Alembic migrations and drift detection (ADR 0004, Phase 1 spec).

### Community 44 - "Community 44"
Cohesion: 0.29
Nodes (6): dataclasses, rich_panel, rich_table, panel(), The only module allowed to write to stdout. Every command produces one of two…, Build a titled Rich panel.

### Community 45 - "Community 45"
Cohesion: 0.33
Nodes (5): field_validator, datetime, Default for `fetched_at`: an aware UTC instant, never a naive local one., Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC., _utcnow()

### Community 46 - "Community 46"
Cohesion: 0.33
Nodes (6): AssetError, An asset could not be written, verified, or identified., Bytes Pillow cannot identify are rejected, and the temp file is cleaned up., A valid image outside the JPEG/PNG/WebP allowlist is rejected with a hint., test_put_corrupted_or_non_image_raises(), test_put_unsupported_mime_raises()

### Community 47 - "Community 47"
Cohesion: 0.40
Nodes (5): Reclaim free space, truncate the WAL, and delete unreferenced asset files.…, vacuum_db(), parametrize, A non-positive window would let vacuum delete an in-flight write's files., test_vacuum_rejects_non_positive_grace()

### Community 48 - "Community 48"
Cohesion: 0.40
Nodes (4): _iso(), datetime, When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, Render an aware datetime as the ISO-8601 UTC string the schema stores.

### Community 49 - "Community 49"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 50 - "Community 50"
Cohesion: 0.67
Nodes (3): A missing video will still be missing on attempt three; retrying just wastes…, test_permanent_failures_are_not_retried(), missing()

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 527 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Repositories` connect `Community 30` to `Community 6`, `Community 9`, `Community 14`, `Community 48`, `Community 17`, `Community 20`, `Community 22`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `FetchService` connect `Community 4` to `Community 16`, `Community 34`, `Community 20`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `root()` connect `Community 1` to `Community 0`, `Community 3`, `Community 36`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `Repositories` (e.g. with `_view()` and `open_repositories()`) actually correct?**
  _`Repositories` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `emit()` (e.g. with `fetch()` and `list_()`) actually correct?**
  _`emit()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `SettingsError` (e.g. with `set_()` and `AppContext`) actually correct?**
  _`SettingsError` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._