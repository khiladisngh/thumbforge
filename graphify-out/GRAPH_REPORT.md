# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 804 nodes · 1683 edges · 38 communities (31 shown, 7 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 160 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `53784227`
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

## God Nodes (most connected - your core abstractions)
1. `SettingsError` - 25 edges
2. `load_settings()` - 24 edges
3. `AppContext` - 21 edges
4. `AssetStore` - 21 edges
5. `AssetKind` - 20 edges
6. `get_engine()` - 20 edges
7. `handle_errors()` - 20 edges
8. `emit()` - 20 edges
9. `ThumbforgeError` - 19 edges
10. `YtDlpSource` - 19 edges

## Surprising Connections (you probably didn't know these)
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout()` --uses--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `root()` --calls--> `AppContext`  [EXTRACTED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `_json_context()` --uses--> `AppContext`  [INFERRED]
  tests/unit/test_render.py → src/thumbforge/cli/_render.py
- `test_rich_mode_uses_the_renderer_and_prints_no_json()` --uses--> `AppContext`  [INFERRED]
  tests/unit/test_render.py → src/thumbforge/cli/_render.py

## Import Cycles
- None detected.

## Communities (38 total, 7 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): BaseModel, BaseSettings, model_validator, platformdirs, pydantic_settings, Self, Return the settings, or re-raise the failure that prevented loading them.…, Configuration is missing, malformed, or contains something it must not. (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (73): alembic_config, alembic_runtime_migration, alembic_script, Config, Connection, ConnectionPoolEntry, contextlib, Engine (+65 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (57): BoundLogger, callback, CaptureFixture, count, envvar, is_eager, LogFormat, logging_handlers (+49 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (42): asyncio, ChannelMeta, datetime, PlaylistMeta, RawInfo, RetryCallState, Metadata sources: YouTube metadata providers behind one Protocol (ADR 0005)., _duration() (+34 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (39): DeclarativeBase, enum, sqlalchemy, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations., Origin of channel metadata. (+31 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (35): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, asset_store() (+27 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (28): importlib_metadata, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set() (+20 more)

### Community 7 - "Community 7"
Cohesion: 0.13
Nodes (25): min, P, R, RenderableType, init_(), path_(), command, Context (+17 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (24): pydantic, PlaylistItemMeta, datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the…, Default for `fetched_at`: an aware UTC instant, never a naive local one., One video's place in a playlist., _utcnow(), Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005). (+16 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (23): re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 10 - "Community 10"
Cohesion: 0.10
Nodes (24): BaseException, DownloadError, NotFoundError, SourceError, _cause_chain(), Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, Yield `exc` and its `cause` links; `ExtractorError` nests the real failure… (+16 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (20): rich_console, ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError (+12 more)

### Community 12 - "Community 12"
Cohesion: 0.09
Nodes (20): ComplianceError, NotFoundError, PartialBatchError, Exception, A generated image violates the YouTube thumbnail requirements., A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render. (+12 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (22): tenacity, _fixture(), `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., Only `None` is the documented "could not fetch" sentinel. An empty dict is an…, Classification is pure, so `resolve` must not spend a network call. (+14 more)

### Community 14 - "Community 14"
Cohesion: 0.13
Nodes (15): alembic, collections_abc, Console, pathlib, pytest, testcontainers_core_container, Integration tests using Testcontainers for database verification (ADR 0004)., Record `tests/fixtures/ytdlp/*.json` from live YouTube, and assert the S11… (+7 more)

### Community 15 - "Community 15"
Cohesion: 0.14
Nodes (21): Argument, metavar, rich_syntax, _as_toml(), _config_path(), init_(), path_(), command (+13 more)

### Community 16 - "Community 16"
Cohesion: 0.11
Nodes (17): dataclasses, rich_panel, rich_table, main(), Root Typer application: global flags, context construction, sub-app…, Typer command surface. Commands are thin; behaviour lives in…, get_app_context(), kv() (+9 more)

### Community 17 - "Community 17"
Cohesion: 0.14
Nodes (17): parametrize, Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1). Pure…, UrlKind, Which YouTube URLs and ids resolve to which kind (ADR 0005, ROADMAP P2.1)., `@` alone names no channel, so it must not resolve successfully., `urlparse` raises `ValueError` on these; the CLI only handles…, Every URL form thumbforge accepts, and the exact identifier it must extract., Bad input must be a usage error (exit 2), not a source failure or a crash. (+9 more)

### Community 18 - "Community 18"
Cohesion: 0.18
Nodes (15): functools, IntEnum, _app_context(), wrapper(), _is_json_mode(), Turn exceptions into process exits. The only module permitted to exit the…, Find the :class:`AppContext` the root callback stored on the Click context.…, _report() (+7 more)

### Community 19 - "Community 19"
Cohesion: 0.15
Nodes (12): Protocol, ChannelMeta, PlaylistMeta, A fetched YouTube channel., A fetched YouTube playlist and its ordered items., Number of items fetched, for the `playlist.item_count` column., MetadataSource, The `MetadataSource` Protocol every metadata backend implements (ADR 0005). A… (+4 more)

### Community 20 - "Community 20"
Cohesion: 0.17
Nodes (17): A supplied URL or identifier is not recognisable YouTube input., UrlError, What a URL or bare identifier turned out to be (ADR 0005)., ResolvedUrl, _channel_handle(), classify_id(), classify_url(), _expect_kind() (+9 more)

### Community 21 - "Community 21"
Cohesion: 0.14
Nodes (14): pil, shutil, sqlalchemy_exc, sqlalchemy_orm, new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits. (+6 more)

### Community 22 - "Community 22"
Cohesion: 0.16
Nodes (11): _fsync_dir(), Path, Session, sessionmaker, Return the absolute path on disk for ``asset``., Re-hash the file on disk and report whether it matches ``asset.sha256``., Flush a directory entry to disk so a publication survives power loss. Fsyncing…, Bind the store to a data directory and the session factory used for asset rows. (+3 more)

### Community 23 - "Community 23"
Cohesion: 0.18
Nodes (11): Any, yt-dlp yields `None` for a deleted video; positions must stay contiguous., A video id is the one field nothing can be reconstructed from., A YouTube change can make yt-dlp return the wrong type for a field. Without the…, `datetime.fromtimestamp` rejects these, and not all of them as `ValueError`.…, Extractor stub that returns a fixture and remembers how it was called., _Recorder, test_entry_without_an_id_is_a_source_error() (+3 more)

### Community 24 - "Community 24"
Cohesion: 0.15
Nodes (10): Extractor, ResolvedUrl, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp., Classify input without touching the network; `core.urls` does the work., YtDlpSource, A missing video will still be missing on attempt three; retrying just wastes…, `cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch. (+2 more)

### Community 25 - "Community 25"
Cohesion: 0.15
Nodes (11): field_validator, _Meta, Shared configuration and provenance for every fetched snapshot., Reject naive datetimes: `fetched_at` is persisted as ISO-8601 UTC., A fetched YouTube video. `channel_id` is the channel's *YouTube* id, not a…, VideoMeta, Fetch one video's metadata., `extra="forbid"` turns an unexpected yt-dlp field into a loud failure. yt-dlp's… (+3 more)

### Community 26 - "Community 26"
Cohesion: 0.17
Nodes (8): hashlib, Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 27 - "Community 27"
Cohesion: 0.22
Nodes (11): MonkeyPatch, A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code., Phase 2 acceptance criteria require retries to be observable in the logs., test_retry_emits_a_log_event() (+3 more)

### Community 28 - "Community 28"
Cohesion: 0.33
Nodes (6): json, main(), Path, Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys

### Community 29 - "Community 29"
Cohesion: 0.67
Nodes (3): E, _enum_values(), Extract serialized string values from an Enum class.

### Community 30 - "Community 30"
Cohesion: 0.67
Nodes (3): What a YouTube URL or bare identifier refers to., UrlKind, StrEnum

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 378 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `YtDlpSource` connect `Community 24` to `Community 27`, `Community 3`, `Community 13`, `Community 23`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `root()` connect `Community 2` to `Community 16`, `Community 0`, `Community 18`, `Community 7`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `UrlError` connect `Community 20` to `Community 11`, `Community 12`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `SettingsError` (e.g. with `root()` and `set_()`) actually correct?**
  _`SettingsError` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `AppContext` (e.g. with `root()` and `_config_path()`) actually correct?**
  _`AppContext` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.0526006464883926 - nodes in this community are weakly interconnected._