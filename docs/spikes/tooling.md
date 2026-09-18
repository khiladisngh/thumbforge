# Spike results — tooling

## S13 — prettier via pre-commit on Windows (closed 2026-09-19)

- Command: `uv run pre-commit run --all-files` with `pre-commit/mirrors-prettier` at `rev: v4.0.0-alpha.8`, `types_or: [markdown, yaml, json]`.
- Result: pre-commit bootstrapped its own Node environment on Windows 11 without a repo `package.json`; the hook reformatted 21 Markdown files on first run and passed on the second. It writes a cache to `node_modules/.cache/prettier/` inside the repo, so `node_modules/` is git- and prettier-ignored.
- Decision: keep prettier; no `mdformat` fallback needed.

## S14 — zensical build of the ADR/spec tree (closed 2026-09-19)

- Command: `uv run zensical build` with zensical `0.0.62` (pinned in `uv.lock`).
- Result: `Build started / No issues found / Build finished in 1.4s`. Mermaid fences require the explicit `pymdownx.superfences` custom fence in `zensical.toml`:

    ```toml
    [project.markdown_extensions."pymdownx.superfences"]
    custom_fences = [
      { name = "mermaid", class = "mermaid", format = "pymdownx.superfences.fence_code_format" },
    ]
    ```

- Navigation is generated from the `docs/` folder structure (no `nav` key); `docs/specs/README.md` becomes the specs index.
