# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 160 nodes · 214 edges · 18 communities (10 shown, 8 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a8d270b1`
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
5. `_json_context()` - 6 edges
6. `AppContext` - 5 edges
7. `handle_errors()` - 5 edges
8. `_report()` - 5 edges
9. `PartialBatchError` - 4 edges
10. `ProviderAuthError` - 4 edges

## Surprising Connections (you probably didn't know these)
- `test_rich_mode_uses_the_renderer_and_prints_no_json()` --calls--> `emit()`  [INFERRED]
  tests/unit/test_render.py → src/thumbforge/cli/_render.py
- `test_only_transient_and_timeout_are_retryable()` --calls--> `ProviderAuthError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py
- `test_only_transient_and_timeout_are_retryable()` --calls--> `ProviderTimeoutError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py
- `test_only_transient_and_timeout_are_retryable()` --calls--> `ProviderTransientError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py
- `boom()` --calls--> `NotFoundError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py

## Import Cycles
- None detected.

## Communities (18 total, 8 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.07
Nodes (35): enum, Exception, IntEnum, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError, ProviderError (+27 more)

### Community 1 - "Community 1"
Cohesion: 0.10
Nodes (17): hashlib, MonkeyPatch, os, pathlib, pytest, new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort… (+9 more)

### Community 2 - "Community 2"
Cohesion: 0.15
Nodes (12): functools, json, parametrize, rich_console, Turn exceptions into process exits. The only module permitted to exit the…, ThumbforgeError, test_error_maps_to_documented_exit_code(), test_keyboard_interrupt_exits_130() (+4 more)

### Community 3 - "Community 3"
Cohesion: 0.15
Nodes (14): callback, Context, envvar, help, is_eager, Option, main(), Path (+6 more)

### Community 4 - "Community 4"
Cohesion: 0.17
Nodes (12): collections_abc, dataclasses, rich_panel, rich_table, kv(), panel(), The only module allowed to write to stdout. Every command produces one of two…, Build a Rich table. Rendering is the caller's job via :func:`emit`. (+4 more)

### Community 5 - "Community 5"
Cohesion: 0.27
Nodes (10): Console, JsonValue, RenderableType, emit(), Print ``data`` as JSON in ``--json`` mode, otherwise print ``render()``.…, _json_context(), AppContext, test_json_mode_output_round_trips() (+2 more)

### Community 6 - "Community 6"
Cohesion: 0.24
Nodes (11): P, R, _app_context(), handle_errors(), wrapper(), _is_json_mode(), AppContext, ThumbforgeError (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.33
Nodes (6): Path, main(), Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys, test_sha256_file_matches_sha256_bytes()

### Community 8 - "Community 8"
Cohesion: 0.33
Nodes (5): ComplianceError, A generated image violates the YouTube thumbnail requirements., Machine mode contract: stdout carries command output, stderr carries the…, test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), boom()

### Community 9 - "Community 9"
Cohesion: 0.33
Nodes (3): thumbforge, thumbforge_cli_app, typer_testing

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 83 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `test_only_transient_and_timeout_are_retryable()` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.269) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `emit()` (e.g. with `test_json_mode_output_round_trips()` and `test_non_finite_floats_are_rejected()`) actually correct?**
  _`emit()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.07152496626180836 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.10476190476190476 - nodes in this community are weakly interconnected._