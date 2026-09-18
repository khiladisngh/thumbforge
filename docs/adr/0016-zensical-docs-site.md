# ADR 0016: zensical for the documentation site

## Status

`Accepted` — 2026-09-19

## Context

The repository's documentation (ARCHITECTURE, ROADMAP, CONVENTIONS, TESTING, GLOSSARY, ADRs, specs) is written in Markdown under `docs/` and is the primary input for the coding agents that build the project. It should also be browsable as a site with navigation and search, with mermaid diagrams rendered, and its build should be a CI gate so broken links and malformed pages are caught early.

Verified (zensical.org/docs/create-your-site): PyPI package `zensical`, version 0.0.62 observed, pre-1.0, by the Material for MkDocs team; `zensical new .` scaffolds `zensical.toml`, `docs/index.md` and `.github/workflows/docs.yml`; `zensical serve` on localhost:8000; `zensical build`; configuration `[project] site_name = "…"` with `site_url` recommended.

## Decision

- **zensical** builds the docs site. Installed as a dev dependency (`uv add --dev zensical`) so the version is pinned **exactly** in `uv.lock` (pre-1.0: every bump is a deliberate PR).
- `zensical.toml` at the repo root:

    ```toml
    [project]
    site_name = "Thumbforge"
    site_url = "https://<owner>.github.io/thumbforge/"
    docs_dir = "docs"
    ```

    followed by a `nav` list covering ARCHITECTURE, ROADMAP, CONVENTIONS, TESTING, GLOSSARY, `adr/`, `specs/` (decision D5 supplies `<owner>`).

- `uv run zensical build` is a CI gate in the main workflow: warnings are errors, so a missing nav target or broken relative link fails the PR.
- `docs.yml` workflow (scaffolded by `zensical new`, adjusted to use uv) builds the site and publishes to GitHub Pages on push to `main`.
- `uv run zensical serve` is the local preview command in `AGENTS.md`.
- Build output `site/` is gitignored and prettier-ignored.
- Mermaid rendering inside the built site is confirmed by spike S14; if a `pymdownx.superfences` custom fence is required, it is added to `zensical.toml` at that point.

## Consequences

- Docs and code review in the same PR; the site is always in sync with `main`.
- Pre-1.0 risk is contained by the exact pin and by the build being a visible CI check (`PLAN.md` §9).
- ADRs and specs need no front-matter or special syntax; plain Markdown files are pages.
- One more tool in the dev group; no Node or Ruby toolchain.

## Alternatives considered

- **mkdocs-material** — rejected: in maintenance mode; zensical is its successor by the same team with a TOML-first configuration.
- **Sphinx** — rejected: reStructuredText friction for contributors and agents writing Markdown; MyST adds another layer.
- **GitHub's rendered Markdown only (no site)** — rejected: no navigation, no search, no mermaid gate in CI.
- **Docusaurus / VitePress** — rejected: require a Node project in the repo, contrary to ADR 0009.
