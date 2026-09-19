# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 520 nodes · 1033 edges · 34 communities (16 shown, 18 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 86 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `26ac91ff`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 22 edges
2. `set_values()` - 18 edges
3. `emit()` - 18 edges
4. `get_engine()` - 17 edges
5. `configure_logging()` - 17 edges
6. `root()` - 17 edges
7. `get_logger()` - 16 edges
8. `SettingsError` - 15 edges
9. `Base` - 14 edges
10. `get_db_status()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_session_scope_commits_on_success()` --uses--> `Channel`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/storage/models.py
- `test_session_scope_rolls_back_on_error()` --uses--> `Channel`  [INFERRED]
  tests/unit/test_storage_db.py → src/thumbforge/storage/models.py
- `test_check_constraint_channel_source()` --uses--> `Channel`  [INFERRED]
  tests/unit/test_storage_models.py → src/thumbforge/storage/models.py

## Import Cycles
- None detected.

## Communities (34 total, 18 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (63): alembic_config, alembic_runtime_migration, alembic_script, command, Config, contextlib, Engine, Session (+55 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (50): BoundLogger, callback, CaptureFixture, Context, count, envvar, help, is_eager (+42 more)

### Community 2 - "Community 2"
Cohesion: 0.10
Nodes (45): datetime, DeclarativeBase, sqlalchemy_exc, sqlalchemy_orm, Storage layer for thumbforge (SQLite + SQLAlchemy 2.0 + Alembic)., Asset, AssetKind, Base (+37 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (38): AppContext, dataclasses, functools, P, R, rich_console, rich_panel, rich_table (+30 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (39): enum, Exception, IntEnum, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError (+31 more)

### Community 5 - "Community 5"
Cohesion: 0.06
Nodes (37): fixture, hashlib, listens_for, Mapper, MonkeyPatch, os, Path, pathlib (+29 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (35): Argument, Console, JsonValue, metavar, RenderableType, rich_syntax, _as_toml(), _config_path() (+27 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (25): json, Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode() (+17 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (24): collections_abc, parametrize, re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries., Return whether ``key`` names a secret. Matching is on word boundaries, not raw… (+16 more)

### Community 9 - "Community 9"
Cohesion: 0.20
Nodes (23): default_config_path(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, parametrize, Path, Configuration precedence, validation and the secrets prohibition., width and height must change in one call; neither halfway state is 16:9., Guards the conftest fixture itself: a regression there silently pollutes real… (+15 more)

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (21): BaseModel, model_validator, platformdirs, pydantic, pydantic_settings, Self, AntigravitySettings, BatchSettings (+13 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (16): alembic, logging_config, sqlalchemy, get_url(), Alembic environment configuration for thumbforge (ADR 0004)., Resolve database URL from config options or active thumbforge settings., Run migrations in 'offline' mode with SQL script output., Run migrations in 'online' mode against a live database. (+8 more)

### Community 12 - "Community 12"
Cohesion: 0.17
Nodes (16): Any, Configuration is missing, malformed, or contains something it must not., SettingsError, _atomic_write(), _format_validation_error(), _parse_scalar(), Replace ``path`` atomically: write a sibling temp file, fsync, then rename. A…, Write the commented default configuration, refusing to clobber unless ``force``. (+8 more)

### Community 13 - "Community 13"
Cohesion: 0.23
Nodes (7): BaseSettings, Return the settings, or re-raise the failure that prevented loading them.…, default_data_dir(), default_state_dir(), Path, Effective configuration for one invocation: defaults, then file, then…, Settings

### Community 14 - "Community 14"
Cohesion: 0.40
Nodes (5): MonkeyPatch, A generated config must contain defaults, not whatever the current shell…, A valid env override must not let an invalid assignment be written to disk., test_environment_cannot_mask_an_invalid_file_value(), test_init_defaults_ignore_the_environment()

### Community 15 - "Community 15"
Cohesion: 0.50
Nodes (3): _deep_merge(), Build settings where the environment outranks the TOML file. File values cannot…, Merge ``override`` into ``base``, recursing into nested tables.

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 229 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SettingsError` connect `Community 12` to `Community 0`, `Community 1`, `Community 3`, `Community 4`, `Community 6`, `Community 9`, `Community 13`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `root()` connect `Community 1` to `Community 9`, `Community 3`, `Community 12`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 9` to `Community 1`, `Community 10`, `Community 11`, `Community 12`, `Community 13`, `Community 15`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `load_settings()` (e.g. with `root()` and `SettingsError`) actually correct?**
  _`load_settings()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `emit()` (e.g. with `init_()` and `path_()`) actually correct?**
  _`emit()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.06377204884667571 - nodes in this community are weakly interconnected._