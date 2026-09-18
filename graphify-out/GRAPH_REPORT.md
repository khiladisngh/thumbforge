# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 33 nodes · 32 edges · 7 communities (4 shown, 3 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `49d35f9e`
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

## God Nodes (most connected - your core abstractions)
1. `root()` - 7 edges
2. `structure()` - 3 edges
3. `main()` - 2 edges
4. `_version_callback()` - 2 edges
5. `main()` - 2 edges
6. `Compare a committed graphify graph against a freshly extracted one. Only the…` - 1 edges
7. `thumbforge command-line interface.` - 1 edges
8. `thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…` - 1 edges
9. `Root Typer application. Phase 0 ships only ``--version``. Sub-apps (fetch,…` - 1 edges
10. `Typer command surface. Commands are thin; behaviour lives in…` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (7 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.29
Nodes (7): json, Path, pathlib, main(), Compare a committed graphify graph against a freshly extracted one. Only the…, structure(), sys

### Community 1 - "Community 1"
Cohesion: 0.29
Nodes (7): callback, help, is_eager, Option, thumbforge command-line interface., root(), _version_callback()

### Community 2 - "Community 2"
Cohesion: 0.29
Nodes (3): importlib_metadata, thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…, typer_testing

### Community 3 - "Community 3"
Cohesion: 0.40
Nodes (4): main(), Root Typer application. Phase 0 ships only ``--version``. Sub-apps (fetch,…, typer, typing

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 23 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `root()` connect `Community 1` to `Community 3`?**
  _High betweenness centrality (0.161) - this node is a cross-community bridge._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._