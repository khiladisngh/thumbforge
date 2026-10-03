# Developers

These pages are for people who change Thumbforge's code: fixing a bug, implementing a roadmap task, or adding a provider. The canonical working instructions — project map, dependency rule, conventions, definition of done — are in [`AGENTS.md`](https://github.com/khiladisngh/thumbforge/blob/main/AGENTS.md) at the repository root; these pages expand on it.

## Set up the repository

Everything runs through [uv](https://docs.astral.sh/uv/); never `pip` or a bare `python -m`.

```
git clone https://github.com/khiladisngh/thumbforge
cd thumbforge
uv sync --locked
uv run thumbforge --help
```

| Purpose               | Command                                       |
| --------------------- | --------------------------------------------- |
| Lint + format Python  | `uv run ruff check . && uv run ruff format .` |
| Type check            | `uv run pyright`                              |
| Unit + contract tests | `uv run pytest -q`                            |
| Import contracts      | `uv run lint-imports`                         |
| Docs preview          | `uv run zensical serve`                       |
| Docs build (CI gate)  | `uv run zensical build`                       |
| All pre-commit hooks  | `pre-commit run --all-files`                  |

[CI and local checks](../maintainers/ci.md) lists exactly what CI runs.

## Read next

- [Architecture](architecture.md) — package layout, dependency rule, data model, key decisions.
- [Conventions](conventions.md) — code style, commits and PRs, the knowledge graph, where docs go.
- [Testing](testing.md) — test layers, markers, fixtures.
- [Specs](../specs/README.md) — one contract per phase; every roadmap task links to one.
- Spikes — recorded experiments that settled unknown facts: [Antigravity CLI](../spikes/antigravity.md), [graphify](../spikes/graphify.md), [Terminal preview](../spikes/terminal-preview.md), [Tooling](../spikes/tooling.md), [yt-dlp](../spikes/ytdlp.md).
- [Glossary](glossary.md) — the project's terms.
- [`PLAN.md`](https://github.com/khiladisngh/thumbforge/blob/main/PLAN.md) — the full project plan: data model, provider interface, command tree, exit codes.
