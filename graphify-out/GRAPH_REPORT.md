# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 522 nodes · 1027 edges · 31 communities (11 shown, 20 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 87 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3933ac33`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 22 edges
2. `emit()` - 19 edges
3. `set_values()` - 18 edges
4. `root()` - 17 edges
5. `configure_logging()` - 17 edges
6. `get_engine()` - 16 edges
7. `get_logger()` - 16 edges
8. `SettingsError` - 14 edges
9. `Base` - 14 edges
10. `test_insert_all_nine_models_and_verify_relations()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_session_scope_commits_on_success()` --uses--> `Channel`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/storage/models.py
- `test_session_scope_rolls_back_on_error()` --uses--> `Channel`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/storage/models.py

## Import Cycles
- None detected.

## Communities (31 total, 20 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): Any, BaseModel, BaseSettings, model_validator, platformdirs, pydantic, pydantic_settings, Self (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (60): Argument, command, Console, dataclasses, handle_errors, JsonValue, metavar, RenderableType (+52 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (54): alembic_config, alembic_runtime_migration, alembic_script, Config, contextlib, Engine, Session, sessionmaker (+46 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (50): datetime, DeclarativeBase, listens_for, Mapper, sqlalchemy_exc, Storage layer for thumbforge (SQLite + SQLAlchemy 2.0 + Alembic)., Asset, AssetKind (+42 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (45): BoundLogger, callback, CaptureFixture, Context, count, envvar, help, is_eager (+37 more)

### Community 5 - "Community 5"
Cohesion: 0.06
Nodes (35): AppContext, functools, json, P, Path, R, rich_console, main() (+27 more)

### Community 6 - "Community 6"
Cohesion: 0.06
Nodes (33): alembic, collections_abc, fixture, hashlib, logging_handlers, MonkeyPatch, os, pathlib (+25 more)

### Community 7 - "Community 7"
Cohesion: 0.06
Nodes (39): enum, Exception, IntEnum, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError (+31 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (25): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+17 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (23): parametrize, re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw…, Return the dotted paths of every secret-looking key in a nested structure. (+15 more)

### Community 10 - "Community 10"
Cohesion: 0.24
Nodes (9): logging_config, get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database., run_migrations_offline(), run_migrations_online() (+1 more)

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 230 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SettingsError` connect `Community 0` to `Community 1`, `Community 4`, `Community 5`, `Community 7`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `root()` connect `Community 4` to `Community 0`, `Community 5`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 0` to `Community 10`, `Community 4`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `load_settings()` (e.g. with `root()` and `SettingsError`) actually correct?**
  _`load_settings()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `emit()` (e.g. with `init_()` and `path_()`) actually correct?**
  _`emit()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.051490514905149054 - nodes in this community are weakly interconnected._