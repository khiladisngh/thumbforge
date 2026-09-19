# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 578 nodes · 1117 edges · 44 communities (16 shown, 28 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 87 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `64720402`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 22 edges
2. `emit()` - 20 edges
3. `get_engine()` - 19 edges
4. `set_values()` - 17 edges
5. `root()` - 17 edges
6. `configure_logging()` - 17 edges
7. `get_logger()` - 16 edges
8. `init_db()` - 15 edges
9. `test_insert_all_nine_models_and_verify_relations()` - 14 edges
10. `SettingsError` - 13 edges

## Surprising Connections (you probably didn't know these)
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `test_sqlite_database_in_container()` --uses--> `ChannelSource`  [INFERRED]
  tests/integration/test_db_container.py → src/thumbforge/core/enums.py
- `test_sqlite_database_in_container()` --uses--> `Channel`  [INFERRED]
  tests/integration/test_db_container.py → src/thumbforge/storage/models.py

## Import Cycles
- None detected.

## Communities (44 total, 28 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic, pydantic_settings, Self (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (69): alembic, alembic_config, alembic_runtime_migration, alembic_script, Config, Connection, ConnectionPoolEntry, contextlib (+61 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (60): datetime, DeclarativeBase, E, enum, shutil, sqlalchemy, sqlalchemy_exc, sqlalchemy_orm (+52 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (49): hashlib, json, MonkeyPatch, os, Path, pathlib, pytest, main() (+41 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (48): BoundLogger, callback, CaptureFixture, Context, count, envvar, is_eager, LogFormat (+40 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (35): Exception, IntEnum, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError, ProviderError (+27 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (23): parametrize, re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure. (+15 more)

### Community 7 - "Community 7"
Cohesion: 0.13
Nodes (23): Argument, help, metavar, Option, rich_syntax, _as_toml(), _config_path(), init_() (+15 more)

### Community 8 - "Community 8"
Cohesion: 0.13
Nodes (14): dataclasses, functools, rich_console, main(), Root Typer application: global flags, context construction, sub-app…, Turn exceptions into process exits. The only module permitted to exit the…, sys, The exit-code contract: a script parsing our status codes must never be… (+6 more)

### Community 9 - "Community 9"
Cohesion: 0.15
Nodes (18): AssetStore, fixture, io, pil, isolate_user_environment(), MonkeyPatch, Path, Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.… (+10 more)

### Community 10 - "Community 10"
Cohesion: 0.17
Nodes (13): Asset, AssetKind, new_id(), Path, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of a file, read in chunks so large images stay off the…, sha256_file(), AssetStore (+5 more)

### Community 11 - "Community 11"
Cohesion: 0.23
Nodes (15): init_(), path_(), command, Context, handle_errors, ``thumbforge db`` — database lifecycle and migration management (ADR 0004)., Print the SQLite database file path., Reclaim unused disk space and checkpoint the Write-Ahead Log (WAL). (+7 more)

### Community 12 - "Community 12"
Cohesion: 0.14
Nodes (11): collections_abc, rich_panel, rich_table, kv(), panel(), The only module allowed to write to stdout. Every command produces one of two…, Build a Rich table. Rendering is the caller's job via :func:`emit`., Build a titled Rich panel. (+3 more)

### Community 13 - "Community 13"
Cohesion: 0.13
Nodes (13): Settings, AppContext, get_app_context(), Context, Per-invocation state built by the root callback and stored on ``ctx.obj``., Return the settings, or re-raise the failure that prevented loading them.…, Extract and validate the AppContext from a Typer execution context., Machine mode contract: stdout carries command output, stderr carries the… (+5 more)

### Community 14 - "Community 14"
Cohesion: 0.19
Nodes (12): AppContext, P, R, _app_context(), handle_errors(), wrapper(), _is_json_mode(), Find the :class:`AppContext` the root callback stored on the Click context.… (+4 more)

### Community 15 - "Community 15"
Cohesion: 0.27
Nodes (10): Console, RenderableType, emit(), JsonValue, Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.…, _json_context(), AppContext, test_json_mode_output_round_trips() (+2 more)

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 258 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `root()` connect `Community 4` to `Community 8`, `Community 0`, `Community 7`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `SettingsError` connect `Community 0` to `Community 4`, `Community 5`, `Community 7`, `Community 8`, `Community 13`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 0` to `Community 1`, `Community 4`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `load_settings()` (e.g. with `root()` and `SettingsError`) actually correct?**
  _`load_settings()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `emit()` (e.g. with `test_json_mode_output_round_trips()` and `test_non_finite_floats_are_rejected()`) actually correct?**
  _`emit()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `get_engine()` (e.g. with `_set_sqlite_pragmas()` and `asset_store()`) actually correct?**
  _`get_engine()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._