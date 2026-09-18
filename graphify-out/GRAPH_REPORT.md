# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 146 nodes · 212 edges · 13 communities (9 shown, 4 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 18 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cc66103d`
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

## God Nodes (most connected - your core abstractions)
1. `ThumbforgeError` - 16 edges
2. `AppContext` - 11 edges
3. `root()` - 11 edges
4. `ProviderError` - 9 edges
5. `handle_errors()` - 7 edges
6. `ExitCode` - 6 edges
7. `_stderr()` - 6 edges
8. `ComplianceError` - 5 edges
9. `PartialBatchError` - 5 edges
10. `NotFoundError` - 5 edges

## Surprising Connections (you probably didn't know these)
- `test_partial_batch_carries_counts_for_the_resume_message()` --uses--> `PartialBatchError`  [INFERRED]
  tests/test_errors.py → src/thumbforge/core/errors.py
- `test_json_mode_emits_machine_readable_diagnostic()` --uses--> `AppContext`  [INFERRED]
  tests/test_errors.py → src/thumbforge/cli/_render.py
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/test_errors.py → src/thumbforge/cli/_render.py
- `test_keyboard_interrupt_exits_130()` --uses--> `ExitCode`  [INFERRED]
  tests/test_errors.py → src/thumbforge/core/errors.py
- `test_error_maps_to_documented_exit_code()` --uses--> `ThumbforgeError`  [INFERRED]
  tests/test_errors.py → src/thumbforge/core/errors.py

## Import Cycles
- None detected.

## Communities (13 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.13
Nodes (20): Console, functools, IntEnum, P, R, _app_context(), handle_errors(), wrapper() (+12 more)

### Community 1 - "Community 1"
Cohesion: 0.14
Nodes (18): hashlib, os, new_id(), Path, Identifier and content-hash helpers. ULIDs are used for primary keys: they sort…, Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits., Return the hex SHA-256 of ``data``., Return the hex SHA-256 of a file, read in chunks so large images stay off the… (+10 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (15): Exception, ComplianceError, PartialBatchError, A generated image violates the YouTube thumbnail requirements., A batch finished with some items failed; the run is resumable., Base class for every expected failure. Subclasses set ``code`` and…, Configuration is missing, malformed, or contains something it must not., A template's layout spec or prompt failed to load, validate or render. (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.13
Nodes (15): callback, Context, envvar, help, is_eager, Option, rich_console, main() (+7 more)

### Community 4 - "Community 4"
Cohesion: 0.16
Nodes (16): enum, ProviderAuthError, ProviderError, ProviderOutputMissingError, ProviderPermanentError, ProviderRegistryError, ProviderTimeoutError, ProviderTransientError (+8 more)

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (12): parametrize, pytest, NotFoundError, A referenced entity does not exist., The exit-code contract: a script parsing our status codes must never be…, test_error_maps_to_documented_exit_code(), test_hint_and_code_reach_stderr(), boom() (+4 more)

### Community 6 - "Community 6"
Cohesion: 0.15
Nodes (14): collections_abc, dataclasses, rich_panel, rich_table, emit(), kv(), panel(), Any (+6 more)

### Community 7 - "Community 7"
Cohesion: 0.29
Nodes (7): json, Path, pathlib, main(), Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys

### Community 8 - "Community 8"
Cohesion: 0.29
Nodes (3): importlib_metadata, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, typer_testing

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 75 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ThumbforgeError` connect `Community 2` to `Community 0`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Why does `AppContext` connect `Community 0` to `Community 2`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Why does `root()` connect `Community 3` to `Community 0`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `ThumbforgeError` (e.g. with `handle_errors()` and `_report()`) actually correct?**
  _`ThumbforgeError` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `AppContext` (e.g. with `root()` and `_app_context()`) actually correct?**
  _`AppContext` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `handle_errors()` (e.g. with `wrapper()` and `ExitCode`) actually correct?**
  _`handle_errors()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._