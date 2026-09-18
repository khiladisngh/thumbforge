# thumbforge

[![ci](https://github.com/khiladisngh/thumbforge/actions/workflows/ci.yml/badge.svg)](https://github.com/khiladisngh/thumbforge/actions/workflows/ci.yml)
[![docs](https://github.com/khiladisngh/thumbforge/actions/workflows/docs.yml/badge.svg)](https://khiladisngh.github.io/thumbforge/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python 3.14](https://img.shields.io/badge/python-3.14-blue)

Generate consistent, spec-compliant YouTube thumbnails from a hero image and a playlist — from the terminal.

- **Hero first.** Generate several candidates for one video, compare, pick, refine.
- **Batch second.** Use the picked hero as the style reference for every video in a playlist, with deterministic titles and "Part N" badges rendered by Pillow over AI-generated art.
- **Pluggable providers.** Antigravity CLI first; add your own via the `thumbforge.providers` entry-point group. A deterministic `fake` provider keeps tests offline.
- **Local database.** Channels, playlists, videos, templates, runs, iterations and assets in SQLite; images content-addressed on disk; interrupted batches resume without regenerating finished items.

> **Status: pre-alpha.** Phase 0 (infrastructure) is complete; no thumbnail generation exists yet. See the [roadmap](docs/ROADMAP.md).

## Install (once released)

```
uv tool install thumbforge
thumbforge --version
```

## Planned workflow

```
thumbforge fetch "https://www.youtube.com/playlist?list=PL…"
thumbforge thumb generate <video-id> --template bold-title --provider antigravity --n 4
thumbforge thumb pick <run-id> 2
thumbforge batch <playlist-id> --hero <run-id> --template series-parts
```

## Documentation

Published at **https://khiladisngh.github.io/thumbforge/** — architecture, roadmap, ADRs, specs.

- [`PLAN.md`](PLAN.md) — full project plan
- [`AGENTS.md`](AGENTS.md) — instructions for coding agents (this repo is built spec-first by agents)
- [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md) — spikes and decisions

## Development

```
uv sync --locked
uv run pytest -q
uv run ruff check . && uv run ruff format .
uv run pyright
uv run zensical serve      # docs at http://localhost:8000
pre-commit install
```

## License

[MIT](LICENSE) © 2026 Gishant Singh
