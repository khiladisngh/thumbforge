---
template: home.html
---

# Thumbforge

Generate consistent, spec-compliant YouTube thumbnails from a hero image and a playlist — from the terminal.

- **Hero first.** Generate several candidates for one video, compare them, pick one and refine it.
- **Batch second.** Use the picked hero as the style reference for every video in a playlist. Titles and "Part N" badges are drawn by Thumbforge itself, so they are exact and identical in style on every thumbnail.
- **Pluggable providers.** Image generation is a plugin; a deterministic `fake` provider works offline.
- **Local and resumable.** Videos, playlists, templates and runs live in a local SQLite database; images are stored by content hash, and an interrupted batch resumes without redoing finished items.

Thumbforge 0.1.0 is on PyPI: `uv tool install thumbforge`. It fetches playlists, numbers the parts, generates and refines a hero, and batches the whole playlist in its style; an interrupted batch resumes where it stopped.

## Where to start

- [**User guide**](user-guide/index.md) — install Thumbforge, run it for the first time, and learn the concepts: heroes, series, templates and providers.
- [**Developers**](developers/index.md) — set up the repository and read the architecture, conventions, testing rules, phase specs and spike results.
- [**Maintainers**](maintainers/index.md) — release process, CI, the roadmap, open questions and decision records.

Source: [github.com/khiladisngh/thumbforge](https://github.com/khiladisngh/thumbforge). MIT licensed.
