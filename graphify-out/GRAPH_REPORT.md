# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 260 nodes · 442 edges · 19 communities (7 shown, 12 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 24 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `488630fd`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 22 edges
2. `set_values()` - 16 edges
3. `emit()` - 14 edges
4. `ThumbforgeError` - 12 edges
5. `set_()` - 12 edges
6. `Settings` - 11 edges
7. `init_()` - 11 edges
8. `root()` - 11 edges
9. `AppContext` - 10 edges
10. `SettingsError` - 10 edges

## Surprising Connections (you probably didn't know these)
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `test_non_16_9_output_is_rejected()` --uses--> `Settings`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `test_json_mode_output_round_trips()` --calls--> `emit()`  [INFERRED]
  tests/unit/test_render.py → src/thumbforge/cli/_render.py
- `test_non_finite_floats_are_rejected()` --calls--> `emit()`  [INFERRED]
  tests/unit/test_render.py → src/thumbforge/cli/_render.py

## Import Cycles
- None detected.

## Communities (19 total, 12 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (42): Argument, collections_abc, command, dataclasses, handle_errors, metavar, RenderableType, rich_panel (+34 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (39): enum, Exception, IntEnum, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError (+31 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (30): Console, hashlib, json, MonkeyPatch, os, Path, pathlib, pytest (+22 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (28): BaseModel, BaseSettings, model_validator, platformdirs, pydantic, pydantic_settings, Self, AntigravitySettings (+20 more)

### Community 4 - "Community 4"
Cohesion: 0.15
Nodes (30): Any, Configuration is missing, malformed, or contains something it must not., SettingsError, _deep_merge(), _format_validation_error(), load_settings(), Build settings where the environment outranks the TOML file. File values cannot…, Merge ``override`` into ``base``, recursing into nested tables. (+22 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (26): functools, P, parametrize, R, _app_context(), handle_errors(), wrapper(), _is_json_mode() (+18 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (17): callback, Context, envvar, is_eager, rich_console, main(), help, Option (+9 more)

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 119 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SettingsError` connect `Community 4` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.180) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 4` to `Community 0`, `Community 3`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Why does `ThumbforgeError` connect `Community 1` to `Community 4`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `emit()` (e.g. with `test_json_mode_output_round_trips()` and `test_non_finite_floats_are_rejected()`) actually correct?**
  _`emit()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.07716701902748414 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.06312292358803986 - nodes in this community are weakly interconnected._