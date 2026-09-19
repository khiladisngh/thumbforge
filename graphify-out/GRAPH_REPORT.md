# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 340 nodes · 615 edges · 28 communities (13 shown, 15 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 28 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4db73b61`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 21 edges
2. `set_values()` - 18 edges
3. `root()` - 18 edges
4. `configure_logging()` - 17 edges
5. `get_logger()` - 17 edges
6. `Settings` - 14 edges
7. `emit()` - 14 edges
8. `ThumbforgeError` - 12 edges
9. `AppContext` - 12 edges
10. `set_()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `test_json_mode_output_round_trips()` --calls--> `emit()`  [INFERRED]
  tests/unit/test_render.py → src/thumbforge/cli/_render.py
- `test_non_finite_floats_are_rejected()` --calls--> `emit()`  [INFERRED]
  tests/unit/test_render.py → src/thumbforge/cli/_render.py

## Import Cycles
- None detected.

## Communities (28 total, 15 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (48): Any, BaseSettings, MonkeyPatch, Return the settings, or re-raise the failure that prevented loading them.…, Configuration is missing, malformed, or contains something it must not., SettingsError, _atomic_write(), _deep_merge() (+40 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (39): enum, Exception, IntEnum, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError (+31 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (36): BaseModel, collections_abc, logging_handlers, model_validator, platformdirs, pydantic, pydantic_settings, Self (+28 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (31): AppContext, dataclasses, functools, P, R, rich_console, rich_panel, rich_table (+23 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (37): Argument, command, metavar, RenderableType, rich_syntax, _as_toml(), _config_path(), _context() (+29 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (31): BoundLogger, CaptureFixture, LogFormat, bind(), clear_context(), configure_logging(), get_logger(), Path (+23 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (17): callback, Context, count, envvar, is_eager, parametrize, handle_errors, help (+9 more)

### Community 7 - "Community 7"
Cohesion: 0.19
Nodes (10): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` rewrites the file, so it must not require parsing the old one…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+2 more)

### Community 8 - "Community 8"
Cohesion: 0.18
Nodes (10): new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of ``data``., Return the hex SHA-256 of a file, read in chunks so large images stay off the…, sha256_bytes(), sha256_file() (+2 more)

### Community 9 - "Community 9"
Cohesion: 0.20
Nodes (9): os, pytest, TempPathFactory, isolate_user_environment(), fixture, Path, Shared fixtures. Establishes ``tests/`` as the pytest root., Point platformdirs at a temp directory and drop stray ``THUMBFORGE_*``… (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.25
Nodes (5): hashlib, Path, test_ids_sort_by_creation_time(), test_sha256_file_matches_sha256_bytes(), thumbforge_core

### Community 11 - "Community 11"
Cohesion: 0.43
Nodes (6): Console, _json_context(), AppContext, test_json_mode_output_round_trips(), test_non_finite_floats_are_rejected(), test_non_json_payload_raises_instead_of_being_stringified()

### Community 12 - "Community 12"
Cohesion: 0.33
Nodes (6): json, pathlib, main(), Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 157 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SettingsError` connect `Community 0` to `Community 1`, `Community 4`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 0` to `Community 2`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Why does `root()` connect `Community 6` to `Community 0`, `Community 3`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `root()` (e.g. with `AppContext` and `Settings`) actually correct?**
  _`root()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.07946127946127945 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.06312292358803986 - nodes in this community are weakly interconnected._