# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 321 nodes · 570 edges · 27 communities (10 shown, 17 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 28 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e706217f`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 23 edges
2. `set_values()` - 18 edges
3. `root()` - 17 edges
4. `configure_logging()` - 15 edges
5. `get_logger()` - 15 edges
6. `emit()` - 13 edges
7. `ThumbforgeError` - 12 edges
8. `set_()` - 12 edges
9. `SettingsError` - 10 edges
10. `write_default_config()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_rich_mode_uses_the_renderer_and_prints_no_json()` --calls--> `kv()`  [INFERRED]
  tests/unit/test_render.py → src/thumbforge/cli/_render.py
- `boom()` --calls--> `ComplianceError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py

## Import Cycles
- None detected.

## Communities (27 total, 17 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (47): Any, BaseSettings, MonkeyPatch, Configuration is missing, malformed, or contains something it must not., SettingsError, _atomic_write(), _deep_merge(), default_config_path() (+39 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (33): callback, Context, count, envvar, is_eager, parametrize, rich_console, main() (+25 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (36): enum, Exception, IntEnum, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError (+28 more)

### Community 3 - "Community 3"
Cohesion: 0.10
Nodes (33): Argument, command, Console, handle_errors, help, JsonValue, metavar, Option (+25 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (32): BoundLogger, CaptureFixture, fixture, LogFormat, logging_handlers, bind(), clear_context(), configure_logging() (+24 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (26): BaseModel, model_validator, platformdirs, pydantic, pydantic_settings, Self, AntigravitySettings, BatchSettings (+18 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (22): hashlib, os, Path, pathlib, pytest, main(), Compare a committed graphify graph against a freshly extracted one. Only the…, structure() (+14 more)

### Community 7 - "Community 7"
Cohesion: 0.19
Nodes (14): AppContext, functools, P, R, _app_context(), handle_errors(), wrapper(), _is_json_mode() (+6 more)

### Community 8 - "Community 8"
Cohesion: 0.16
Nodes (9): json, Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), thumbforge, thumbforge_cli_app (+1 more)

### Community 9 - "Community 9"
Cohesion: 0.18
Nodes (11): collections_abc, dataclasses, rich_panel, rich_table, kv(), panel(), The only module allowed to write to stdout. Every command produces one of two…, Build a Rich table. Rendering is the caller's job via :func:`emit`. (+3 more)

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 144 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SettingsError` connect `Community 0` to `Community 2`, `Community 3`?**
  _High betweenness centrality (0.153) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 0` to `Community 1`, `Community 3`, `Community 5`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Why does `root()` connect `Community 1` to `Community 0`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_settings()` (e.g. with `root()` and `SettingsError`) actually correct?**
  _`load_settings()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `root()` (e.g. with `AppContext` and `load_settings()`) actually correct?**
  _`root()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08345428156748912 - nodes in this community are weakly interconnected._