# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 25 nodes · 24 edges · 7 communities (2 shown, 5 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `50379632`
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
2. `_version_callback()` - 2 edges
3. `main()` - 2 edges
4. `thumbforge command-line interface.` - 1 edges
5. `Root Typer application. Phase 0 ships only ``--version``. Sub-apps (fetch,…` - 1 edges
6. `thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and…` - 1 edges
7. `Typer command surface. Commands are thin; behaviour lives in…` - 1 edges
8. `Shared pytest fixtures. Establishes ``tests/`` as the pytest root.` - 1 edges
9. `thumbforge` - 0 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (7 total, 5 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.29
Nodes (7): callback, help, is_eager, Option, thumbforge command-line interface., root(), _version_callback()

### Community 1 - "Community 1"
Cohesion: 0.40
Nodes (4): main(), Root Typer application. Phase 0 ships only ``--version``. Sub-apps (fetch,…, typer, typing

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 18 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `root()` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.290) - this node is a cross-community bridge._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
