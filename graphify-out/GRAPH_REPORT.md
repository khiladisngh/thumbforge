# Graph Report - yt-thumbnail-generator  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 778 nodes · 1672 edges · 39 communities (35 shown, 4 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 170 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b537c1ac`
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

## God Nodes (most connected - your core abstractions)
1. `SettingsError` - 25 edges
2. `load_settings()` - 24 edges
3. `YtDlpSource` - 23 edges
4. `AppContext` - 21 edges
5. `AssetStore` - 21 edges
6. `AssetKind` - 20 edges
7. `get_engine()` - 20 edges
8. `handle_errors()` - 20 edges
9. `emit()` - 20 edges
10. `ThumbforgeError` - 19 edges

## Surprising Connections (you probably didn't know these)
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_entry_without_an_id_is_a_source_error()` --uses--> `SourceError`  [INFERRED]
  tests/unit/test_ytdlp.py → src/thumbforge/core/errors.py
- `test_unexpected_extractor_failure_maps_to_source_error()` --uses--> `SourceError`  [INFERRED]
  tests/unit/test_ytdlp.py → src/thumbforge/core/errors.py
- `test_network_failure_maps_to_a_transient_error()` --uses--> `SourceTransientError`  [INFERRED]
  tests/unit/test_ytdlp.py → src/thumbforge/core/errors.py
- `_source()` --uses--> `YtDlpSource`  [INFERRED]
  tests/unit/test_ytdlp.py → src/thumbforge/sources/ytdlp.py

## Import Cycles
- None detected.

## Communities (39 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic_settings, Self, Return the settings, or re-raise the failure that prevented loading them.… (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (76): Config, Engine, integration, min, P, R, RenderableType, init_() (+68 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (51): DeclarativeBase, E, enum, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md…, What a YouTube URL or bare identifier refers to., Lifecycle classification of a thumbnail generation run., Execution status for runs and iterations. (+43 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (47): io, AssetKind, Functional role of a stored image asset., AssetError, An asset could not be written, verified, or identified., Path, Return the hex SHA-256 of a file, read in chunks so large images stay off the…, sha256_file() (+39 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (50): BoundLogger, callback, CaptureFixture, count, envvar, is_eager, LogFormat, logging_handlers (+42 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (24): field_validator, Protocol, pydantic, ChannelMeta, _Meta, PlaylistMeta, datetime, Boundary models for YouTube metadata (PLAN.md §3, ADR 0005). These mirror the… (+16 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (27): tenacity, _fixture(), Any, `YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP…, S11: a flat extract cannot supply these, so the defaults must survive.…, Enumerating a channel is a non-goal and expensive, so pin the cheap request., `@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path., yt-dlp yields `None` for a deleted video; positions must stay contiguous. (+19 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (26): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+18 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (22): asyncio, RawInfo, RetryCallState, _duration(), _log_retry(), _published_at(), datetime, `YtDlpSource` — YouTube metadata via `yt-dlp`, no API key (ADR 0005, ROADMAP… (+14 more)

### Community 9 - "Community 9"
Cohesion: 0.10
Nodes (24): datetime, PlaylistItemMeta, One video's place in a playlist., Invariants the metadata boundary models enforce (PLAN.md §3, ADR 0005)., `resolve()` returns both halves (ADR 0005); an empty id is never a valid result., A minimal valid video, so each test states only the field it is about., A fetched snapshot is a value; mutating one would desync it from `fetched_at`., `extra="forbid"` turns an unexpected yt-dlp field into a loud failure. yt-dlp's… (+16 more)

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (23): re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure., Return a copy of ``value`` with every secret-keyed entry replaced. A copy,… (+15 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (19): json, main(), Path, Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), _extract_with_ytdlp(), Run a real `yt_dlp` extraction and translate its failures. `yt_dlp` is imported…, sys (+11 more)

### Community 12 - "Community 12"
Cohesion: 0.14
Nodes (20): parametrize, classify_url(), Resolve a YouTube URL, handle or bare id to its kind and identifier. A `watch`…, UrlKind, Which YouTube URLs and ids resolve to which kind (ADR 0005, ROADMAP P2.1)., `@` alone names no channel, so it must not resolve successfully., `urlparse` raises `ValueError` on these; the CLI only handles…, Every URL form thumbforge accepts, and the exact identifier it must extract. (+12 more)

### Community 13 - "Community 13"
Cohesion: 0.15
Nodes (19): Argument, metavar, rich_syntax, _config_path(), init_(), path_(), command, Context (+11 more)

### Community 14 - "Community 14"
Cohesion: 0.14
Nodes (13): functools, rich_console, rich_panel, rich_table, Turn exceptions into process exits. The only module permitted to exit the…, panel(), The only module allowed to write to stdout. Every command produces one of two…, Build a titled Rich panel. (+5 more)

### Community 15 - "Community 15"
Cohesion: 0.17
Nodes (16): Extractor, MonkeyPatch, A metadata source failed., A metadata source failed for a reason worth retrying (network, throttling).…, SourceError, SourceTransientError, Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)., Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp. (+8 more)

### Community 16 - "Community 16"
Cohesion: 0.15
Nodes (16): _app_context(), wrapper(), _is_json_mode(), Find the :class:`AppContext` the root callback stored on the Click context.…, _report(), AppContext, get_app_context(), Context (+8 more)

### Community 17 - "Community 17"
Cohesion: 0.16
Nodes (15): A supplied URL or identifier is not recognisable YouTube input., UrlError, What a URL or bare identifier turned out to be (ADR 0005)., ResolvedUrl, _channel_handle(), classify_id(), _expect_kind(), UrlKind (+7 more)

### Community 18 - "Community 18"
Cohesion: 0.15
Nodes (16): DownloadError, IntEnum, ExitCode, Process exit statuses. Values are a public contract., Exception, Map a `yt_dlp` exception onto the thumbforge error hierarchy. Measured against…, _translate(), _download_error() (+8 more)

### Community 19 - "Community 19"
Cohesion: 0.17
Nodes (15): ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError, Error hierarchy and the exit codes it maps to. Every failure the user can… (+7 more)

### Community 20 - "Community 20"
Cohesion: 0.17
Nodes (10): ComplianceError, PartialBatchError, Exception, A generated image violates the YouTube thumbnail requirements., A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, A template's layout spec or prompt failed to load, validate or render., TemplateError (+2 more)

### Community 21 - "Community 21"
Cohesion: 0.20
Nodes (10): alembic_config, alembic_runtime_migration, alembic_script, contextlib, pathlib, sqlalchemy, sqlalchemy_pool, sqlite3 (+2 more)

### Community 22 - "Community 22"
Cohesion: 0.20
Nodes (7): collections_abc, os, pytest, testcontainers_core_container, Shared fixtures. Establishes ``tests/`` as the pytest root., Integration tests using Testcontainers for database verification (ADR 0004)., typing

### Community 23 - "Community 23"
Cohesion: 0.18
Nodes (7): Domain layer: models, errors and services. Imports nothing internal except…, MonkeyPatch, Path, ULIDs must be unique and time-sortable; hashes must match the content they…, `runs list` orders by id, so a later id must sort after an earlier one., test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes()

### Community 24 - "Community 24"
Cohesion: 0.22
Nodes (6): dataclasses, importlib_metadata, main(), Root Typer application: global flags, context construction, sub-app…, Typer command surface. Commands are thin; behaviour lives in…, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…

### Community 25 - "Community 25"
Cohesion: 0.28
Nodes (8): alembic, get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline(), run_migrations_online()

### Community 26 - "Community 26"
Cohesion: 0.25
Nodes (7): hashlib, new_id(), Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of ``data``., sha256_bytes(), time

### Community 27 - "Community 27"
Cohesion: 0.43
Nodes (6): Console, _json_context(), `emit` is the machine boundary: what it prints must always be parseable JSON., test_json_mode_output_round_trips(), test_non_finite_floats_are_rejected(), test_non_json_payload_raises_instead_of_being_stringified()

### Community 28 - "Community 28"
Cohesion: 0.38
Nodes (7): NotFoundError, A referenced entity does not exist., test_hint_and_code_reach_stderr(), boom(), A missing video will still be missing on attempt three; retrying just wastes…, test_permanent_failures_are_not_retried(), missing()

### Community 29 - "Community 29"
Cohesion: 0.33
Nodes (5): pil, shutil, sqlalchemy_exc, sqlalchemy_orm, Content-addressed local image asset store (PLAN.md §3.2, ADR 0011).

### Community 30 - "Community 30"
Cohesion: 0.40
Nodes (5): kv(), Build a Rich table. Rendering is the caller's job via :func:`emit`., Build a two-column key/value table, the default shape for ``show``-style…, table(), test_rich_mode_uses_the_renderer_and_prints_no_json()

### Community 31 - "Community 31"
Cohesion: 0.40
Nodes (5): isolate_user_environment(), fixture, MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…

### Community 32 - "Community 32"
Cohesion: 0.50
Nodes (4): Connection, ConnectionPoolEntry, Apply PRAGMA statements required by ADR 0004 on every SQLite connection., _set_sqlite_pragmas()

### Community 33 - "Community 33"
Cohesion: 0.50
Nodes (3): parametrize, Every error in CASES exits with the code documented in PLAN.md 5.1., test_error_maps_to_documented_exit_code()

### Community 34 - "Community 34"
Cohesion: 0.67
Nodes (3): _as_toml(), JsonValue, Render effective settings as TOML for display. ``tomli_w`` cannot serialise…

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 358 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `YtDlpSource` connect `Community 15` to `Community 35`, `Community 5`, `Community 6`, `Community 8`, `Community 9`, `Community 17`, `Community 28`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `ThumbforgeError` connect `Community 20` to `Community 0`, `Community 1`, `Community 33`, `Community 3`, `Community 14`, `Community 15`, `Community 16`, `Community 17`, `Community 19`, `Community 28`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `SettingsError` connect `Community 0` to `Community 4`, `Community 13`, `Community 14`, `Community 16`, `Community 19`, `Community 20`, `Community 24`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `SettingsError` (e.g. with `root()` and `set_()`) actually correct?**
  _`SettingsError` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `YtDlpSource` (e.g. with `SourceError` and `SourceTransientError`) actually correct?**
  _`YtDlpSource` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.053482221569203646 - nodes in this community are weakly interconnected._