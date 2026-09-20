# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1183 nodes · 2409 edges · 87 communities (60 shown, 27 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 234 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e19a79ef`
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

## God Nodes (most connected - your core abstractions)
1. `Repositories` - 29 edges
2. `emit()` - 26 edges
3. `StubSource` - 24 edges
4. `load_settings()` - 24 edges
5. `get_engine()` - 22 edges
6. `AssetStore` - 21 edges
7. `YtDlpSource` - 20 edges
8. `AssetKind` - 20 edges
9. `AppContext` - 20 edges
10. `FetchService` - 19 edges

## Surprising Connections (you probably didn't know these)
- `repeating()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_cli_fetch.py → src/thumbforge/core/models.py
- `_playlist()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_repositories.py → src/thumbforge/core/models.py
- `test_duplicate_video_in_a_playlist_is_listed_once()` --calls--> `PlaylistItemMeta`  [INFERRED]
  tests/unit/test_repositories.py → src/thumbforge/core/models.py
- `repos()` --uses--> `Repositories`  [INFERRED]
  tests/unit/test_repositories.py → src/thumbforge/storage/repositories.py
- `test_channel_url_does_not_enumerate_videos()` --uses--> `FetchService`  [INFERRED]
  tests/unit/test_fetch_service.py → src/thumbforge/core/services/fetch.py

## Import Cycles
- None detected.

## Communities (87 total, 27 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (55): data_dir(), ChannelMeta, fixture, Path, VideoMeta, `fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP…, An initialised database, since every command here needs the schema., The `PLAN.md` §5.3 shape: panel, `#`/`Part` table, then the stored counts. (+47 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (44): field_validator, pydantic, ChannelMeta, _Meta, PlaylistItemMeta, PlaylistMeta, datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the… (+36 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (47): The repository bundle services receive (`docs/specs/phase-6-hero.md`)., Repositories, _channel(), _playlist(), ChannelMeta, PlaylistMeta, VideoMeta, Upsert semantics the rest of Phase 2 depends on (ROADMAP P2.3, PLAN.md §3). (+39 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (43): DeclarativeBase, enum, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations., Origin of channel metadata. (+35 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (30): What persisting a playlist actually wrote. Returned instead of the ORM row…, StoredPlaylist, FakeSource, FakeStore, ChannelMeta, DateTime, PlaylistMeta, VideoMeta (+22 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (28): importlib_metadata, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set() (+20 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (31): Config, DatabaseError, A database operation failed (e.g. migration, lock, disk failure)., _alembic_config(), get_db_status(), get_engine(), Path, Build an Alembic configuration targeting ``db_path``. (+23 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (26): functools, IntEnum, rich_console, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.… (+18 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (28): Engine, init_db(), Session, sessionmaker, Ensure directory exists and upgrade DB to head. Returns: Tuple of…, Delete unreferenced ``assets/`` files and stale ``tmp/`` entries older than the…, Create a thread-safe sessionmaker bound to ``engine``., Transactional context manager: commits on clean exit, rolls back on error. (+20 more)

### Community 9 - "Community 9"
Cohesion: 0.16
Nodes (26): BoundLogger, CaptureFixture, LogFormat, configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``., Configure structlog and the stdlib root logger. Safe to call more than once. (+18 more)

### Community 10 - "Community 10"
Cohesion: 0.10
Nodes (21): dataclasses, json, pathlib, rich_panel, rich_table, declarations(), main(), Path (+13 more)

### Community 11 - "Community 11"
Cohesion: 0.14
Nodes (25): list_(), Argument, command, Context, handle_errors, help, Option, ``thumbforge playlist`` — list and inspect stored playlists (ROADMAP P2.3). (+17 more)

### Community 12 - "Community 12"
Cohesion: 0.13
Nodes (23): Any, importlib_util, ModuleType, _deep_merge(), Build settings where the environment outranks the TOML file. File values cannot…, Merge ``override`` into ``base``, recursing into nested tables., _declaration(), _graph() (+15 more)

### Community 13 - "Community 13"
Cohesion: 0.13
Nodes (22): collections_abc, JsonPayload, RenderableType, JsonPayload, ``thumbforge fetch`` — pull YouTube metadata into the database (ROADMAP P2.3)., Build the JSON payload and the Rich renderable from the **stored** rows.…, _view(), ``thumbforge video`` — list and inspect stored videos (ROADMAP P2.3). (+14 more)

### Community 14 - "Community 14"
Cohesion: 0.12
Nodes (23): re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 15 - "Community 15"
Cohesion: 0.19
Nodes (24): default_config_path(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., Spike S5 superseded decision D4: the dangerous flag is not opted into by…, Write a config file and return its path, so tests read as one expression. (+16 more)

### Community 16 - "Community 16"
Cohesion: 0.10
Nodes (22): BaseModel, model_validator, platformdirs, pydantic_settings, Self, AntigravitySettings, BatchSettings, _format_validation_error() (+14 more)

### Community 17 - "Community 17"
Cohesion: 0.14
Nodes (21): Argument, metavar, rich_syntax, _as_toml(), _config_path(), init_(), path_(), command (+13 more)

### Community 18 - "Community 18"
Cohesion: 0.15
Nodes (21): min, P, R, init_(), path_(), command, Context, help (+13 more)

### Community 19 - "Community 19"
Cohesion: 0.13
Nodes (18): RawInfo, _duration(), ChannelMeta, PlaylistMeta, VideoMeta, Turn an unexpected yt-dlp info-dict *shape* into a `SourceError`. yt-dlp parses…, Read a string field, treating a missing key and an explicit `None` alike. Both…, Read `duration` as whole seconds. Flat and full extracts disagree by up to a… (+10 more)

### Community 20 - "Community 20"
Cohesion: 0.12
Nodes (21): DownloadError, NotFoundError, SourceError, Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, _translate(), _download_error(), Exception (+13 more)

### Community 21 - "Community 21"
Cohesion: 0.11
Nodes (15): alembic, alembic_config, alembic_runtime_migration, alembic_script, Connection, ConnectionPoolEntry, sqlalchemy, sqlalchemy_pool (+7 more)

### Community 22 - "Community 22"
Cohesion: 0.15
Nodes (15): BaseSettings, Return the settings, or re-raise the failure that prevented loading them.…, Configuration is missing, malformed, or contains something it must not., SettingsError, _atomic_write(), default_data_dir(), default_state_dir(), Path (+7 more)

### Community 23 - "Community 23"
Cohesion: 0.12
Nodes (14): Protocol, FetchStore, ChannelMeta, datetime, MetadataSource, PlaylistMeta, VideoMeta, Take the metadata source and persistence layer the CLI selected. (+6 more)

### Community 24 - "Community 24"
Cohesion: 0.16
Nodes (12): FetchResult, FetchService, ResolvedUrl, Playlist rows written., Fetch YouTube metadata and persist it., Resolve `url`, fetch the thing it names, and store it., A single video, plus its channel when the video names one. The extra channel…, A playlist, its owning channel, its videos and its item order. (+4 more)

### Community 25 - "Community 25"
Cohesion: 0.14
Nodes (18): `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., A source wired to a fixture, plus the recorder that captured its calls., Classification is pure, so `resolve` must not spend a network call., A single video must be extracted deeply: that is the only way to get…, `position` comes from enumeration order because `playlist_index` is absent… (+10 more)

### Community 26 - "Community 26"
Cohesion: 0.12
Nodes (17): callback, count, envvar, is_eager, Context, handle_errors, help, Option (+9 more)

### Community 27 - "Community 27"
Cohesion: 0.15
Nodes (15): _fixture(), Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Load one recorded yt-dlp info dict. (+7 more)

### Community 28 - "Community 28"
Cohesion: 0.18
Nodes (10): PlaylistRepository, Playlist, PlaylistItem, Playlist rows and their ordered items., Return the row for a YouTube playlist id, or `None`., Look a playlist up by ULID or YouTube id, raising `NotFoundError` if absent., Insert or refresh a playlist. `channel_row_id` is required: the column is NOT…, Rewrite a playlist's items to exactly `video_ids`, in order. Rows are deleted… (+2 more)

### Community 29 - "Community 29"
Cohesion: 0.15
Nodes (13): pil, shutil, sqlalchemy_exc, new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of ``data``. (+5 more)

### Community 30 - "Community 30"
Cohesion: 0.18
Nodes (15): get_app_context(), Context, Extract and validate the AppContext from a Typer execution context., list_(), Argument, command, Context, handle_errors (+7 more)

### Community 31 - "Community 31"
Cohesion: 0.15
Nodes (15): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError, Base class for image-provider failures. (+7 more)

### Community 32 - "Community 32"
Cohesion: 0.15
Nodes (13): asyncio, BaseException, contextlib, RetryCallState, _cause_chain(), _log_retry(), _published_at(), datetime (+5 more)

### Community 33 - "Community 33"
Cohesion: 0.14
Nodes (14): ChannelSource, MetadataSource, fetch(), Argument, ChannelSource, Context, handle_errors, help (+6 more)

### Community 34 - "Community 34"
Cohesion: 0.19
Nodes (12): io, _make_jpeg_bytes(), _make_png_bytes(), MonkeyPatch, Unit tests for content-addressed AssetStore (PLAN.md §3.2, ADR 0011)., A failed insert never unlinks the published file, and a retry adopts it. A…, Generate synthetic PNG image bytes for testing., Generate synthetic JPEG image bytes for testing. (+4 more)

### Community 35 - "Community 35"
Cohesion: 0.23
Nodes (10): pytest, `FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).…, Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1). Pure…, `FetchService` decisions: kind dispatch, the freshness rule, and what each…, Which YouTube URLs and ids resolve to which kind (ADR 0005, ROADMAP P2.1)., thumbforge_core_enums, thumbforge_core_errors, thumbforge_core_models (+2 more)

### Community 36 - "Community 36"
Cohesion: 0.15
Nodes (10): PartialBatchError, Exception, A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., TemplateError, ThumbforgeError, parametrize (+2 more)

### Community 37 - "Community 37"
Cohesion: 0.19
Nodes (9): Video, VideoMeta, Look a video up by ULID or YouTube id, raising `NotFoundError` if absent. Both…, Insert or refresh a video, preserving its ULID. `channel_row_id` is supplied…, Videos, newest fetch first, optionally restricted to one channel., Persist one video and, when known, its channel. A single-video fetch can afford…, Video rows, keyed by YouTube video id., Return the row for a YouTube video id, or `None`. (+1 more)

### Community 38 - "Community 38"
Cohesion: 0.15
Nodes (10): ResolvedUrl, classify_url(), Resolve a YouTube URL, handle or bare id to its kind and identifier. A `watch`…, ResolvedUrl, Classify input without touching the network; `core.urls` does the work., ResolvedUrl, `v=` wins over `list=`: the URL names a video being watched inside a playlist.…, Pasted URLs routinely carry a trailing newline or space. (+2 more)

### Community 39 - "Community 39"
Cohesion: 0.17
Nodes (9): Extractor, Metadata sources: concrete `core.sources.MetadataSource` implementations (ADR…, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes…, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch., test_permanent_failures_are_not_retried() (+1 more)

### Community 40 - "Community 40"
Cohesion: 0.17
Nodes (8): hashlib, Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 41 - "Community 41"
Cohesion: 0.17
Nodes (12): parametrize, UrlKind, `@` alone names no channel, so it must not resolve successfully., `urlparse` raises `ValueError` on these; the CLI only handles…, Every URL form thumbforge accepts, and the exact identifier it must extract., Bad input must be a usage error (exit 2), not a source failure or a crash., An explicit form fixes the kind; the id's shape must not override it.…, test_classify_url() (+4 more)

### Community 42 - "Community 42"
Cohesion: 0.26
Nodes (12): AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, Bytes Pillow cannot identify are rejected, and the temp file is cleaned up., A `Path` source that does not exist fails before anything is written. (+4 more)

### Community 43 - "Community 43"
Cohesion: 0.20
Nodes (12): A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, CaptureFixture, MonkeyPatch, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs. (+4 more)

### Community 44 - "Community 44"
Cohesion: 0.20
Nodes (12): _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, Any, CaptureFixture, `playlist_items="0"` must return channel fields and no entries., Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`., A full extract must carry the fields a flat entry cannot (S11). Also the only…, Re-assert the S11 field set, so a yt-dlp upgrade that changes it fails loudly. (+4 more)

### Community 45 - "Community 45"
Cohesion: 0.21
Nodes (8): ChannelRepository, Channel, ChannelMeta, Persist a channel on its own (a channel URL was fetched)., Channel rows, keyed by YouTube channel id., Return the row for a YouTube channel id, or `None`., Insert or refresh a channel, preserving its ULID., Every channel, newest fetch first.

### Community 46 - "Community 46"
Cohesion: 0.29
Nodes (10): Console, emit(), JsonValue, Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.…, _json_context(), `emit` is the machine boundary: what it prints must always be parseable JSON., test_json_mode_output_round_trips(), test_non_finite_floats_are_rejected() (+2 more)

### Community 47 - "Community 47"
Cohesion: 0.20
Nodes (11): asset_store(), _backdate(), fixture, Path, `db vacuum` deletes expired unreferenced files and stale tmp entries (ADR 0011)., A file from an in-flight `put` is newer than the grace age, so vacuum leaves…, Age files past the vacuum grace window without sleeping., Provide an initialized AssetStore backed by a temporary SQLite database. (+3 more)

### Community 48 - "Community 48"
Cohesion: 0.22
Nodes (8): datetime, sqlalchemy_orm, _iso(), Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).…, When a stored playlist was last fetched, or `None` if it is not stored. Parsed…, Render an aware datetime as the ISO-8601 UTC string the schema stores., thumbforge_core_services_fetch, thumbforge_storage_models

### Community 49 - "Community 49"
Cohesion: 0.20
Nodes (10): ConfigSchema, default_config_toml(), The shape of ``config.toml``, with no environment involvement. Kept separate…, Write the commented default configuration, refusing to clobber unless ``force``., Render the default configuration as commented TOML for ``config init``., _toml_value(), write_default_config(), test_non_16_9_output_is_rejected() (+2 more)

### Community 50 - "Community 50"
Cohesion: 0.25
Nodes (8): Collection, NotFoundError, A referenced entity does not exist., Reassign `part_number` sequentially from `start` in playlist order. Videos…, One item's `part_number` before and after a `playlist renumber`. Captured per…, Renumbering, test_hint_and_code_reach_stderr(), boom()

### Community 51 - "Community 51"
Cohesion: 0.22
Nodes (8): os, structlog, isolate_user_environment(), fixture, MonkeyPatch, Path, Shared fixtures. Establishes ``tests/`` as the pytest root., Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 52 - "Community 52"
Cohesion: 0.25
Nodes (9): A supplied URL or identifier is not recognisable YouTube input., UrlError, _channel_handle(), classify_id(), _expect_kind(), UrlKind, Classify a bare YouTube identifier by its shape. Order matters: a channel id…, Classify `value` and require it to be the kind its URL form promises. An… (+1 more)

### Community 53 - "Community 53"
Cohesion: 0.25
Nodes (7): _fsync_dir(), Path, Session, sessionmaker, Flush a directory entry to disk so a publication survives power loss. Fsyncing…, Bind the store to a data directory and the session factory used for asset rows., Store an image file or bytes content-addressed by SHA-256. If identical content…

### Community 54 - "Community 54"
Cohesion: 0.25
Nodes (7): logging_handlers, bind(), clear_context(), structlog configuration (ADR 0015). One pipeline for everything. Application…, Bind context onto every subsequent log record in this task (run id, provider,…, Drop all bound context., structlog_stdlib

### Community 55 - "Community 55"
Cohesion: 0.29
Nodes (6): integration, testcontainers_core_container, Path, Integration tests using Testcontainers for database verification (ADR 0004)., Verify that a database initialized on host can be mounted and read in a Linux…, test_sqlite_database_in_container()

### Community 56 - "Community 56"
Cohesion: 0.38
Nodes (3): Session, Build the three repositories over one session, so they share a transaction., Bind to the caller's session; the service owns the transaction.

### Community 57 - "Community 57"
Cohesion: 0.40
Nodes (5): MonkeyPatch, A generated config must contain defaults, not whatever the current shell…, A valid env override must not let an invalid assignment be written to disk., test_environment_cannot_mask_an_invalid_file_value(), test_init_defaults_ignore_the_environment()

### Community 59 - "Community 59"
Cohesion: 0.50
Nodes (3): PlaylistMeta, Persist a playlist, its owning channel, its videos and its item order. Reports…, StoredPlaylist

### Community 60 - "Community 60"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 563 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FetchService` connect `Community 24` to `Community 33`, `Community 35`, `Community 4`, `Community 13`, `Community 23`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `FetchStore` connect `Community 23` to `Community 35`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `Repositories` connect `Community 2` to `Community 37`, `Community 8`, `Community 11`, `Community 45`, `Community 13`, `Community 48`, `Community 56`, `Community 59`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `Repositories` (e.g. with `_view()` and `open_repositories()`) actually correct?**
  _`Repositories` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `emit()` (e.g. with `fetch()` and `list_()`) actually correct?**
  _`emit()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.056107539450613676 - nodes in this community are weakly interconnected._