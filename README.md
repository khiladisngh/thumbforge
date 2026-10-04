# thumbforge

[![ci](https://github.com/khiladisngh/thumbforge/actions/workflows/ci.yml/badge.svg)](https://github.com/khiladisngh/thumbforge/actions/workflows/ci.yml)
[![docs](https://github.com/khiladisngh/thumbforge/actions/workflows/docs.yml/badge.svg)](https://khiladisngh.github.io/thumbforge/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/khiladisngh/thumbforge/blob/main/LICENSE)
![Python 3.14](https://img.shields.io/badge/python-3.14-blue)

Generate consistent, spec-compliant YouTube thumbnails from a hero image and a playlist — from the terminal.

- **Hero first.** Generate several candidates for one video, compare, pick, refine.
- **Batch second.** Use the picked hero as the style reference for every video in a playlist, with deterministic titles and "Part N" badges rendered by Pillow over AI-generated art.
- **Pluggable providers.** Antigravity CLI first; add your own via the `thumbforge.providers` entry-point group. A deterministic `fake` provider keeps tests offline.
- **Local database.** Channels, playlists, videos, templates, runs, iterations and assets in SQLite; images content-addressed on disk; interrupted batches resume without regenerating finished items.

## Install

Thumbforge needs [uv](https://docs.astral.sh/uv/) and Python 3.14 (uv downloads Python if it is missing). Install it from PyPI:

```
uv tool install thumbforge
```

To read YouTube metadata through the Data API instead of yt-dlp (optional; it needs an API key), install the `api` extra: `uv tool install "thumbforge[api]"`.

Or build it from a checkout:

```
git clone https://github.com/khiladisngh/thumbforge
cd thumbforge
uv tool install .
```

Check it:

```
thumbforge --version
```

## Quick start

This reproduces the three examples of [`PLAN.md` §5.3](https://github.com/khiladisngh/thumbforge/blob/main/PLAN.md#53-examples) — fetch a playlist, generate a hero, run a batch — with the offline `fake` provider, so it needs no account and no API key. `fetch` reads public YouTube metadata, so it needs network access. The images the `fake` provider returns are placeholders, not artwork.

Point Thumbforge at a scratch config and data directory first, so nothing touches your real setup. These two lines are the only shell-specific part:

```
# Linux / macOS
export THUMBFORGE_CONFIG="$PWD/scratch/config.toml"
export THUMBFORGE_GENERAL__DATA_DIR="$PWD/scratch/data"
```

```
# Windows PowerShell
$env:THUMBFORGE_CONFIG = "$PWD\scratch\config.toml"
$env:THUMBFORGE_GENERAL__DATA_DIR = "$PWD\scratch\data"
```

Create the database, which also stores the built-in templates:

```
$ thumbforge db init
initialized database at <data-dir>/thumbforge.sqlite3 (0001)
```

**1. Fetch a playlist.** This one is public and large (about 180 videos); `batch --only` below keeps the run short. It prints the playlist and one row per video, with the video's part number and id:

```
$ thumbforge fetch "https://www.youtube.com/playlist?list=PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI"
…
Stored 1 channel, 1 playlist, <n> videos.
```

**2. Generate a hero.** Pass the id of the first video from the table above as `<video-id>`:

```
$ thumbforge thumb generate <video-id> --template bold-title --provider fake --n 4
Run <run-id>
Kind      hero
Status    completed
Template  bold-title@1
Provider  fake@0.1.1:<fingerprint>
Video     <video-id>
Started   <timestamp>
Finished  <timestamp>
┏━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━┓
┃ # ┃ Status    ┃ Size      ┃ Compliant ┃ Key          ┃ Cost ┃ Asset / Error ┃
┡━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━┩
│ 1 │ completed │ 1920x1080 │ ✔         │ <key>        │ —    │ <asset>       │
│ 2 │ completed │ 1920x1080 │ ✔         │ <key>        │ —    │ <asset>       │
│ 3 │ completed │ 1920x1080 │ ✔         │ <key>        │ —    │ <asset>       │
│ 4 │ completed │ 1920x1080 │ ✔         │ <key>        │ —    │ <asset>       │
└───┴───────────┴───────────┴───────────┴──────────────┴──────┴───────────────┘
…
Pick one with: thumbforge thumb pick <run-id> <ordinal>
```

The `…` is a table of file paths (a terminal that can draw images shows a preview instead). Copy the run id from the first line.

**3. Pick one candidate.** The picked image becomes the style reference for the batch:

```
$ thumbforge thumb pick <run-id> 2
Picked #2 of run <run-id> (iteration <iteration-id>)
Export it with: thumbforge thumb export <run-id> --to PATH
```

**4. Run a batch** for the first three videos of the playlist, in the hero's style:

```
$ thumbforge batch PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI --hero <run-id> --template series-parts --only 1-3
Batch run <batch-run-id>
Playlist    <playlist-title>
Template    series-parts@1
Provider    fake@0.1.1:<fingerprint>
Reference   <asset> (final)
Parent run  <run-id>
Status      completed
Items       3 completed, 0 failed, 0 pending of 3
…
```

Run ids, asset hashes and timestamps differ on every run, and the playlist's videos change over time. Progress lines such as `run started` go to stderr and are left out above; `--quiet` hides them. `batch --dry-run` prints the plan and generates nothing. If a batch is interrupted or some items fail, `thumbforge runs resume <batch-run-id>` finishes the rest without regenerating the completed ones.

Where to go next:

- [Getting started](https://khiladisngh.github.io/thumbforge/user-guide/getting-started/): the same flow with templates, exporting and playlist numbering.
- [Generate a hero](https://khiladisngh.github.io/thumbforge/user-guide/how-to/generate-a-hero/) and [Pick and refine](https://khiladisngh.github.io/thumbforge/user-guide/how-to/pick-and-refine/).
- [Providers](https://khiladisngh.github.io/thumbforge/user-guide/concepts/providers/): the real image providers and their keys.
- [Shell completion](https://khiladisngh.github.io/thumbforge/user-guide/how-to/shell-completion/).

## Documentation

Published at **https://khiladisngh.github.io/thumbforge/**, in three sections: a user guide, developer docs (architecture, conventions, testing, specs) and maintainer docs (release process, CI, roadmap, decision records).

- [`PLAN.md`](https://github.com/khiladisngh/thumbforge/blob/main/PLAN.md) — full project plan
- [`CHANGELOG.md`](https://github.com/khiladisngh/thumbforge/blob/main/CHANGELOG.md) — changes by Conventional Commit type
- [`AGENTS.md`](https://github.com/khiladisngh/thumbforge/blob/main/AGENTS.md) — instructions for coding agents (this repo is built spec-first by agents)
- [`OPEN_QUESTIONS.md`](https://github.com/khiladisngh/thumbforge/blob/main/OPEN_QUESTIONS.md) — spikes and decisions

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

[MIT](https://github.com/khiladisngh/thumbforge/blob/main/LICENSE) © 2026 Gishant Singh
