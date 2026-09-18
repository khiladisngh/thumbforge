# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 153 nodes · 198 edges · 14 communities (7 shown, 7 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e79664fb`
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

## God Nodes (most connected - your core abstractions)
1. `ThumbforgeError` - 12 edges
2. `AppContext` - 11 edges
3. `root()` - 11 edges
4. `ProviderError` - 9 edges
5. `_stderr()` - 6 edges
6. `handle_errors()` - 5 edges
7. `_report()` - 5 edges
8. `emit()` - 5 edges
9. `PartialBatchError` - 4 edges
10. `ProviderAuthError` - 4 edges

## Surprising Connections (you probably didn't know these)
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/test_errors.py → src/thumbforge/cli/_render.py
- `test_json_mode_emits_machine_readable_diagnostic()` --uses--> `AppContext`  [INFERRED]
  tests/test_errors.py → src/thumbforge/cli/_render.py
- `test_only_transient_and_timeout_are_retryable()` --calls--> `ProviderAuthError`  [INFERRED]
  tests/test_errors.py → src/thumbforge/core/errors.py
- `test_only_transient_and_timeout_are_retryable()` --calls--> `ProviderTimeoutError`  [INFERRED]
  tests/test_errors.py → src/thumbforge/core/errors.py
- `test_only_transient_and_timeout_are_retryable()` --calls--> `ProviderTransientError`  [INFERRED]
  tests/test_errors.py → src/thumbforge/core/errors.py

## Import Cycles
- None detected.

## Communities (14 total, 7 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (33): collections_abc, Console, dataclasses, functools, json, JsonValue, P, R (+25 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (31): enum, Exception, IntEnum, ExitCode, PartialBatchError, ProviderAuthError, ProviderError, ProviderOutputMissingError (+23 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (24): hashlib, MonkeyPatch, os, Path, pathlib, main(), Compare a committed graphify graph against a freshly extracted one. Only the…, structure() (+16 more)

### Community 3 - "Community 3"
Cohesion: 0.14
Nodes (14): callback, Context, envvar, help, is_eager, Option, main(), Path (+6 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (12): parametrize, pytest, NotFoundError, A referenced entity does not exist., ThumbforgeError, The exit-code contract: a script parsing our status codes must never be…, test_error_maps_to_documented_exit_code(), test_hint_and_code_reach_stderr() (+4 more)

### Community 5 - "Community 5"
Cohesion: 0.29
Nodes (3): importlib_metadata, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, typer_testing

### Community 6 - "Community 6"
Cohesion: 0.40
Nodes (5): ComplianceError, A generated image violates the YouTube thumbnail requirements., test_json_mode_emits_machine_readable_diagnostic(), boom(), root()

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 84 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `test_only_transient_and_timeout_are_retryable()` connect `Community 1` to `Community 4`?**
  _High betweenness centrality (0.224) - this node is a cross-community bridge._
- **Why does `AppContext` connect `Community 0` to `Community 3`, `Community 6`?**
  _High betweenness centrality (0.174) - this node is a cross-community bridge._
- **Why does `test_json_mode_emits_machine_readable_diagnostic()` connect `Community 6` to `Community 0`, `Community 4`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `AppContext` (e.g. with `root()` and `_app_context()`) actually correct?**
  _`AppContext` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.07899159663865546 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.08067226890756303 - nodes in this community are weakly interconnected._