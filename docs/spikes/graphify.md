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
- Maintenance: incremental updates run via `graphify update .` (or extract + cluster-only). Committed to git (with `cost.json` ignored).
- CI: `.github/workflows/ci.yml` includes an advisory `graphify drift` check.
