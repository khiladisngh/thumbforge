# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 607 nodes · 1174 edges · 56 communities (21 shown, 35 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 111 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e5c40263`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 22 edges
2. `get_engine()` - 19 edges
3. `emit()` - 19 edges
4. `AssetStore` - 18 edges
5. `set_values()` - 17 edges
6. `root()` - 17 edges
7. `configure_logging()` - 17 edges
8. `init_db()` - 16 edges
9. `get_logger()` - 16 edges
10. `ThumbforgeError` - 14 edges

## Surprising Connections (you probably didn't know these)
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `asset_store()` --uses--> `AssetStore`  [INFERRED]
  tests/unit/test_assets.py → src/thumbforge/storage/assets.py
- `test_put_corrupted_or_non_image_raises()` --uses--> `AssetStore`  [INFERRED]
  tests/unit/test_assets.py → src/thumbforge/storage/assets.py
- `test_put_leaves_published_file_for_vacuum_on_insert_failure()` --uses--> `AssetStore`  [INFERRED]
  tests/unit/test_assets.py → src/thumbforge/storage/assets.py

## Import Cycles
- None detected.

## Communities (56 total, 35 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic, pydantic_settings, Self (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (65): alembic_config, alembic_runtime_migration, alembic_script, Config, Connection, ConnectionPoolEntry, contextlib, Engine (+57 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (56): datetime, DeclarativeBase, E, enum, sqlalchemy, AssetKind, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md… (+48 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (45): Argument, callback, command, Context, count, envvar, handle_errors, help (+37 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (40): Exception, IntEnum, AssetError, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError (+32 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (38): BoundLogger, CaptureFixture, LogFormat, logging_handlers, bind(), clear_context(), configure_logging(), get_logger() (+30 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (27): Path, Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode() (+19 more)

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (23): parametrize, re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure. (+15 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (17): functools, rich_console, rich_syntax, main(), Root Typer application: global flags, context construction, sub-app…, ``thumbforge config`` — inspect and edit the configuration file., Turn exceptions into process exits. The only module permitted to exit the…, The exit-code contract: a script parsing our status codes must never be… (+9 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (16): hashlib, os, pathlib, pytest, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return the hex SHA-256 of ``data``., sha256_bytes(), structlog (+8 more)

### Community 10 - "Community 10"
Cohesion: 0.16
Nodes (13): Asset, AssetKind, new_id(), Path, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of a file, read in chunks so large images stay off the…, sha256_file(), _fsync_dir() (+5 more)

### Community 11 - "Community 11"
Cohesion: 0.22
Nodes (14): io, AssetStore, Content-addressed storage for thumbnail iterations, raw art, and style…, _make_jpeg_bytes(), _make_png_bytes(), Unit tests for content-addressed AssetStore (PLAN.md §3.2, ADR 0011)., Generate synthetic PNG image bytes for testing., Generate synthetic JPEG image bytes for testing. (+6 more)

### Community 12 - "Community 12"
Cohesion: 0.18
Nodes (13): AppContext, P, R, _app_context(), handle_errors(), wrapper(), _is_json_mode(), Find the :class:`AppContext` the root callback stored on the Click context.… (+5 more)

### Community 13 - "Community 13"
Cohesion: 0.18
Nodes (11): dataclasses, rich_panel, rich_table, kv(), panel(), The only module allowed to write to stdout. Every command produces one of two…, Build a Rich table. Rendering is the caller's job via :func:`emit`., Build a titled Rich panel. (+3 more)

### Community 14 - "Community 14"
Cohesion: 0.21
Nodes (10): pil, shutil, sqlalchemy_exc, sqlalchemy_orm, Content-addressed local image asset store (PLAN.md §3.2, ADR 0011)., Storage layer for thumbforge (SQLite + SQLAlchemy 2.0 + Alembic)., thumbforge_core_enums, thumbforge_core_ids (+2 more)

### Community 15 - "Community 15"
Cohesion: 0.17
Nodes (10): Settings, AppContext, get_app_context(), Context, Per-invocation state built by the root callback and stored on ``ctx.obj``., Return the settings, or re-raise the failure that prevented loading them.…, Extract and validate the AppContext from a Typer execution context., Ctrl-C during a batch must still leave machine mode with parseable output. (+2 more)

### Community 16 - "Community 16"
Cohesion: 0.20
Nodes (11): _backdate(), parametrize, Path, `db vacuum` deletes expired unreferenced files and stale tmp entries (ADR 0011)., A file from an in-flight `put` is newer than the grace age, so vacuum leaves…, A non-positive window would let vacuum delete an in-flight write's files., Age files past the vacuum grace window without sleeping., test_put_missing_source_path_raises() (+3 more)

### Community 17 - "Community 17"
Cohesion: 0.43
Nodes (6): Console, _json_context(), AppContext, test_json_mode_output_round_trips(), test_non_finite_floats_are_rejected(), test_non_json_payload_raises_instead_of_being_stringified()

### Community 18 - "Community 18"
Cohesion: 0.29
Nodes (7): fixture, isolate_user_environment(), MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.…, asset_store(), Provide an initialized AssetStore backed by a temporary SQLite database.

### Community 19 - "Community 19"
Cohesion: 0.40
Nodes (5): json, main(), Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys

### Community 21 - "Community 21"
Cohesion: 0.40
Nodes (4): MonkeyPatch, A failed insert never unlinks the published file, and a retry adopts it. A…, test_put_leaves_published_file_for_vacuum_on_insert_failure(), test_ids_sort_by_creation_time()

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 274 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `root()` connect `Community 3` to `Community 8`, `Community 0`, `Community 5`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `SettingsError` connect `Community 0` to `Community 8`, `Community 3`, `Community 4`, `Community 15`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `AssetStore` connect `Community 11` to `Community 10`, `Community 14`, `Community 16`, `Community 18`, `Community 21`, `Community 23`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `load_settings()` (e.g. with `root()` and `SettingsError`) actually correct?**
  _`load_settings()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `get_engine()` (e.g. with `_set_sqlite_pragmas()` and `asset_store()`) actually correct?**
  _`get_engine()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `emit()` (e.g. with `init_()` and `path_()`) actually correct?**
  _`emit()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._