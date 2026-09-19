# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 167 nodes · 221 edges · 18 communities (9 shown, 9 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2a129ad9`
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

## God Nodes (most connected - your core abstractions)
1. `ThumbforgeError` - 12 edges
2. `root()` - 11 edges
3. `ProviderError` - 9 edges
4. `emit()` - 9 edges
5. `AppContext` - 7 edges
6. `_json_context()` - 6 edges
7. `handle_errors()` - 5 edges
8. `_report()` - 5 edges
9. `PartialBatchError` - 4 edges
10. `ProviderAuthError` - 4 edges

## Surprising Connections (you probably didn't know these)
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `test_only_transient_and_timeout_are_retryable()` --calls--> `ProviderAuthError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py
- `test_only_transient_and_timeout_are_retryable()` --calls--> `ProviderTimeoutError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py
- `test_only_transient_and_timeout_are_retryable()` --calls--> `ProviderTransientError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py

## Import Cycles
- None detected.

## Communities (18 total, 9 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (31): enum, Exception, IntEnum, ExitCode, PartialBatchError, ProviderAuthError, ProviderError, ProviderOutputMissingError (+23 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (23): hashlib, MonkeyPatch, os, Path, pathlib, pytest, main(), Compare a committed graphify graph against a freshly extracted one. Only the… (+15 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (20): collections_abc, functools, P, R, _app_context(), handle_errors(), wrapper(), _is_json_mode() (+12 more)

### Community 3 - "Community 3"
Cohesion: 0.12
Nodes (22): Console, dataclasses, json, JsonValue, RenderableType, rich_panel, rich_table, emit() (+14 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (19): callback, Context, envvar, help, is_eager, Option, rich_console, main() (+11 more)

### Community 5 - "Community 5"
Cohesion: 0.33
Nodes (6): ComplianceError, A generated image violates the YouTube thumbnail requirements., Machine mode contract: stdout carries command output, stderr carries the…, test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), boom(), root()

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (3): thumbforge, thumbforge_cli_app, typer_testing

### Community 7 - "Community 7"
Cohesion: 0.50
Nodes (3): parametrize, test_error_maps_to_documented_exit_code(), ThumbforgeError

### Community 8 - "Community 8"
Cohesion: 0.50
Nodes (4): NotFoundError, A referenced entity does not exist., test_hint_and_code_reach_stderr(), boom()

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 87 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `test_only_transient_and_timeout_are_retryable()` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.250) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `emit()` (e.g. with `test_json_mode_output_round_trips()` and `test_non_finite_floats_are_rejected()`) actually correct?**
  _`emit()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `AppContext` (e.g. with `root()` and `root()`) actually correct?**
  _`AppContext` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08067226890756303 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.082010582010582 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.10869565217391304 - nodes in this community are weakly interconnected._