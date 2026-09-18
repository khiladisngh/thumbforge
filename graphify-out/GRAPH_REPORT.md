# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 160 nodes · 221 edges · 15 communities (8 shown, 7 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `18584026`
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

## God Nodes (most connected - your core abstractions)
1. `AppContext` - 13 edges
2. `ThumbforgeError` - 12 edges
3. `root()` - 11 edges
4. `ProviderError` - 9 edges
5. `emit()` - 9 edges
6. `_json_context()` - 6 edges
7. `_stderr()` - 6 edges
8. `handle_errors()` - 5 edges
9. `_report()` - 5 edges
10. `PartialBatchError` - 4 edges

## Surprising Connections (you probably didn't know these)
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/test_errors.py → src/thumbforge/cli/_render.py
- `_json_context()` --uses--> `AppContext`  [INFERRED]
  tests/test_render.py → src/thumbforge/cli/_render.py
- `test_rich_mode_uses_the_renderer_and_prints_no_json()` --uses--> `AppContext`  [INFERRED]
  tests/test_render.py → src/thumbforge/cli/_render.py
- `test_only_transient_and_timeout_are_retryable()` --calls--> `ProviderAuthError`  [INFERRED]
  tests/test_errors.py → src/thumbforge/core/errors.py
- `test_only_transient_and_timeout_are_retryable()` --calls--> `ProviderTimeoutError`  [INFERRED]
  tests/test_errors.py → src/thumbforge/core/errors.py

## Import Cycles
- None detected.

## Communities (15 total, 7 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.07
Nodes (34): enum, Exception, IntEnum, ComplianceError, ExitCode, PartialBatchError, ProviderAuthError, ProviderError (+26 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (21): collections_abc, dataclasses, JsonValue, RenderableType, rich_panel, rich_table, emit(), kv() (+13 more)

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (19): Console, functools, json, P, R, _app_context(), handle_errors(), wrapper() (+11 more)

### Community 3 - "Community 3"
Cohesion: 0.13
Nodes (13): MonkeyPatch, Path, pathlib, pytest, main(), Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys (+5 more)

### Community 4 - "Community 4"
Cohesion: 0.14
Nodes (14): callback, Context, envvar, help, is_eager, Option, rich_console, main() (+6 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (12): parametrize, NotFoundError, A referenced entity does not exist., ThumbforgeError, The exit-code contract: a script parsing our status codes must never be…, test_error_maps_to_documented_exit_code(), test_hint_and_code_reach_stderr(), boom() (+4 more)

### Community 6 - "Community 6"
Cohesion: 0.15
Nodes (12): hashlib, os, new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of ``data``., Return the hex SHA-256 of a file, read in chunks so large images stay off the… (+4 more)

### Community 7 - "Community 7"
Cohesion: 0.29
Nodes (3): importlib_metadata, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, typer_testing

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 84 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `test_only_transient_and_timeout_are_retryable()` connect `Community 0` to `Community 5`?**
  _High betweenness centrality (0.217) - this node is a cross-community bridge._
- **Why does `AppContext` connect `Community 2` to `Community 1`, `Community 4`?**
  _High betweenness centrality (0.182) - this node is a cross-community bridge._
- **Why does `test_json_mode_emits_machine_readable_diagnostic()` connect `Community 2` to `Community 0`, `Community 5`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `AppContext` (e.g. with `root()` and `_app_context()`) actually correct?**
  _`AppContext` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.07396870554765292 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.1225296442687747 - nodes in this community are weakly interconnected._