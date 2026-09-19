# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 274 nodes · 468 edges · 20 communities (8 shown, 12 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 27 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4dd0d275`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 22 edges
2. `set_values()` - 18 edges
3. `emit()` - 13 edges
4. `ThumbforgeError` - 12 edges
5. `set_()` - 12 edges
6. `root()` - 11 edges
7. `SettingsError` - 10 edges
8. `write_default_config()` - 10 edges
9. `write_config()` - 10 edges
10. `init_()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `boom()` --calls--> `ComplianceError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py
- `boom()` --calls--> `NotFoundError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py

## Import Cycles
- None detected.

## Communities (20 total, 12 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (39): enum, Exception, IntEnum, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError (+31 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (35): BaseModel, BaseSettings, model_validator, platformdirs, pydantic, pydantic_settings, Self, AntigravitySettings (+27 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (37): Any, MonkeyPatch, Configuration is missing, malformed, or contains something it must not., SettingsError, _deep_merge(), _format_validation_error(), load_settings(), Build settings where the environment outranks the TOML file. File values cannot… (+29 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (22): callback, Context, envvar, is_eager, main(), help, Option, Path (+14 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (23): functools, P, parametrize, R, rich_console, _app_context(), handle_errors(), wrapper() (+15 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (23): hashlib, json, os, Path, pathlib, pytest, main(), Compare a committed graphify graph against a freshly extracted one. Only the… (+15 more)

### Community 6 - "Community 6"
Cohesion: 0.13
Nodes (25): AppContext, Argument, command, handle_errors, help, JsonValue, metavar, Option (+17 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (22): collections_abc, Console, dataclasses, RenderableType, rich_panel, rich_table, emit(), kv() (+14 more)

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 124 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SettingsError` connect `Community 2` to `Community 0`, `Community 1`, `Community 6`?**
  _High betweenness centrality (0.173) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 2` to `Community 1`, `Community 6`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `set_values()` connect `Community 2` to `Community 1`, `Community 6`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `emit()` (e.g. with `init_()` and `path_()`) actually correct?**
  _`emit()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.06312292358803986 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.07073170731707316 - nodes in this community are weakly interconnected._