# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 311 nodes · 549 edges · 25 communities (10 shown, 15 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 28 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bdc21419`
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

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 23 edges
2. `set_values()` - 18 edges
3. `root()` - 17 edges
4. `emit()` - 13 edges
5. `configure_logging()` - 13 edges
6. `get_logger()` - 13 edges
7. `ThumbforgeError` - 12 edges
8. `set_()` - 12 edges
9. `SettingsError` - 10 edges
10. `init_()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `boom()` --calls--> `ComplianceError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py
- `boom()` --calls--> `NotFoundError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py

## Import Cycles
- None detected.

## Communities (25 total, 15 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (39): enum, Exception, IntEnum, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError (+31 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (39): AppContext, Argument, command, Console, handle_errors, help, JsonValue, metavar (+31 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (37): MonkeyPatch, Configuration is missing, malformed, or contains something it must not., SettingsError, _atomic_write(), _format_validation_error(), load_settings(), Build the effective settings. ``config_path`` and ``data_dir`` are the CLI…, Replace ``path`` atomically: write a sibling temp file, fsync, then rename. A… (+29 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (26): functools, P, R, _app_context(), handle_errors(), wrapper(), _is_json_mode(), AppContext (+18 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (31): BoundLogger, CaptureFixture, fixture, LogFormat, logging_handlers, bind(), clear_context(), configure_logging() (+23 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (25): BaseModel, model_validator, platformdirs, pydantic, pydantic_settings, Self, AntigravitySettings, BatchSettings (+17 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (24): callback, collections_abc, Context, count, dataclasses, envvar, is_eager, rich_console (+16 more)

### Community 7 - "Community 7"
Cohesion: 0.08
Nodes (22): hashlib, json, os, Path, pathlib, pytest, main(), Compare a committed graphify graph against a freshly extracted one. Only the… (+14 more)

### Community 8 - "Community 8"
Cohesion: 0.18
Nodes (10): Any, BaseSettings, _deep_merge(), default_data_dir(), default_state_dir(), Path, Effective configuration for one invocation: defaults, then file, then…, Build settings where the environment outranks the TOML file. File values cannot… (+2 more)

### Community 9 - "Community 9"
Cohesion: 0.33
Nodes (5): parametrize, test_error_maps_to_documented_exit_code(), --quiet outranks -v: an explicit request for silence beats a scripted -v., test_flag_to_level_mapping(), ThumbforgeError

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 141 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SettingsError` connect `Community 2` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.157) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 2` to `Community 8`, `Community 1`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Why does `root()` connect `Community 6` to `Community 1`, `Community 2`, `Community 4`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_settings()` (e.g. with `root()` and `SettingsError`) actually correct?**
  _`load_settings()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `root()` (e.g. with `AppContext` and `load_settings()`) actually correct?**
  _`root()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `emit()` (e.g. with `init_()` and `path_()`) actually correct?**
  _`emit()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._