# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 595 nodes · 1148 edges · 49 communities (17 shown, 32 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 102 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3abd0e5e`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 22 edges
2. `get_engine()` - 19 edges
3. `emit()` - 19 edges
4. `AssetStore` - 17 edges
5. `set_values()` - 17 edges
6. `root()` - 17 edges
7. `configure_logging()` - 17 edges
8. `get_logger()` - 16 edges
9. `init_db()` - 15 edges
10. `session_scope()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `asset_store()` --uses--> `AssetStore`  [INFERRED]
  tests/unit/test_assets.py → src/thumbforge/storage/assets.py
- `test_put_corrupted_or_non_image_raises()` --uses--> `AssetStore`  [INFERRED]
  tests/unit/test_assets.py → src/thumbforge/storage/assets.py

## Import Cycles
- None detected.

## Communities (49 total, 32 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic, pydantic_settings, Self (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (73): alembic, alembic_config, alembic_runtime_migration, alembic_script, Config, Connection, ConnectionPoolEntry, contextlib (+65 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (46): Asset, AssetKind, io, MonkeyPatch, pil, shutil, sqlalchemy_exc, sqlalchemy_orm (+38 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (49): datetime, DeclarativeBase, E, enum, sqlalchemy, AssetKind, ChannelSource, Domain enumerations for thumbforge lifecycle and data classification (PLAN.md… (+41 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (40): Exception, IntEnum, AssetError, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError (+32 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (38): BoundLogger, CaptureFixture, LogFormat, logging_handlers, bind(), clear_context(), configure_logging(), get_logger() (+30 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (32): json, Path, main(), Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys, Path, Root application behaviour: version, exit codes, and diagnostics from the… (+24 more)

### Community 7 - "Community 7"
Cohesion: 0.08
Nodes (22): collections_abc, hashlib, os, pathlib, pytest, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return the hex SHA-256 of ``data``., sha256_bytes() (+14 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (23): parametrize, re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure. (+15 more)

### Community 9 - "Community 9"
Cohesion: 0.13
Nodes (23): Argument, help, metavar, Option, rich_syntax, _as_toml(), _config_path(), init_() (+15 more)

### Community 10 - "Community 10"
Cohesion: 0.16
Nodes (12): rich_console, main(), Root Typer application: global flags, context construction, sub-app…, _version_callback(), ``thumbforge db`` — database lifecycle and migration management (ADR 0004)., The exit-code contract: a script parsing our status codes must never be…, test_keyboard_interrupt_exits_130(), test_unexpected_exception_is_not_swallowed() (+4 more)

### Community 11 - "Community 11"
Cohesion: 0.16
Nodes (15): AppContext, functools, P, R, _app_context(), handle_errors(), wrapper(), _is_json_mode() (+7 more)

### Community 12 - "Community 12"
Cohesion: 0.21
Nodes (17): command, Context, handle_errors, RenderableType, init_(), path_(), Print the SQLite database file path., Reclaim unused disk space, checkpoint the WAL, and delete orphaned asset files. (+9 more)

### Community 13 - "Community 13"
Cohesion: 0.14
Nodes (14): dataclasses, rich_panel, rich_table, get_app_context(), kv(), panel(), Context, The only module allowed to write to stdout. Every command produces one of two… (+6 more)

### Community 14 - "Community 14"
Cohesion: 0.22
Nodes (7): Settings, AppContext, Per-invocation state built by the root callback and stored on ``ctx.obj``., Return the settings, or re-raise the failure that prevented loading them.…, Ctrl-C during a batch must still leave machine mode with parseable output., test_keyboard_interrupt_in_json_mode_emits_one_line_on_stderr(), root()

### Community 15 - "Community 15"
Cohesion: 0.25
Nodes (8): callback, count, envvar, is_eager, handle_errors, Path, thumbforge command-line interface., root()

### Community 16 - "Community 16"
Cohesion: 0.43
Nodes (6): Console, _json_context(), AppContext, test_json_mode_output_round_trips(), test_non_finite_floats_are_rejected(), test_non_json_payload_raises_instead_of_being_stringified()

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 268 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `root()` connect `Community 15` to `Community 0`, `Community 5`, `Community 9`, `Community 10`, `Community 12`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `SettingsError` connect `Community 0` to `Community 4`, `Community 9`, `Community 10`, `Community 13`, `Community 14`, `Community 15`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `AssetStore` connect `Community 2` to `Community 1`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `load_settings()` (e.g. with `root()` and `SettingsError`) actually correct?**
  _`load_settings()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `emit()` (e.g. with `init_()` and `path_()`) actually correct?**
  _`emit()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.051490514905149054 - nodes in this community are weakly interconnected._