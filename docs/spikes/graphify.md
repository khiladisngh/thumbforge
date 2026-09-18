# Spike results — graphify on Windows (closed 2026-09-19)

## S9 — graphify installation and usage on Windows with uv

- Command: `uv tool install graphifyy`
- Result: installed `graphifyy==0.9.63` and entry-points `graphify`, `graphify-mcp`.
- Build command:
    ```bash
    graphify extract . --code-only
    graphify cluster-only . --no-label
    graphify export html
    ```
- Result: extracted 25 nodes, 24 edges across 7 code files in < 5 seconds. Generated:
    - `graphify-out/graph.json` (full queryable graph)
    - `graphify-out/GRAPH_REPORT.md` (human/agent summary)
    - `graphify-out/graph.html` (interactive browser visualisation)
- Query test: `graphify query "where is the root typer app?"` correctly located `src/thumbforge/cli/app.py`, `main()`, `root()`, `_version_callback()`.
- Maintenance: regeneration is **manual**, not git-hooked (`graphify hook install` rebuilds in the background on every commit, which races the commit and is noise for a repo this size):
    ```bash
    graphify extract . --code-only && graphify cluster-only . --no-label
    ```
- Committed: `graph.json`, `GRAPH_REPORT.md`, `graph.html`, `manifest.json`, `.graphify_analysis.json`. Ignored: `graphify-out/cache/` (machine-local AST cache) and `graphify-out/cost.json`.
- CI: `.github/workflows/ci.yml` runs an advisory (`continue-on-error: true`) drift job. A byte diff of `graph.json` is useless — it embeds `built_at_commit`, which changes on every commit — so `scripts/check_graph_drift.py` compares node and edge **sets** only and prints what was added or removed. Verified locally: exit 0 on a current graph, exit 1 listing the 7 added nodes when run against a stale one.
