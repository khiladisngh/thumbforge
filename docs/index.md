# Thumbforge

Generate consistent, spec-compliant YouTube thumbnails from a hero image and a playlist — from the terminal.

- **Hero first.** Generate several candidates for one video, compare, pick, refine.
- **Batch second.** Use the picked hero as the style reference for every video in a playlist, with deterministic titles and "Part N" badges rendered by Pillow.
- **Pluggable providers.** Antigravity CLI first; any provider can be added through the `thumbforge.providers` entry-point group.
- **Local database.** Channels, playlists, videos, templates, runs, iterations and assets live in SQLite; images are content-addressed on disk.

## Status

Pre-alpha. The project is being built spec-first, primarily by coding agents. Start with:

- [Architecture](ARCHITECTURE.md) — package layout, dependency rule, data model
- [Roadmap](ROADMAP.md) — phases and PR-sized tasks
- [Conventions](CONVENTIONS.md) and [Testing](TESTING.md)
- [ADRs](adr/0000-template.md) — every stack decision
- [Specs](specs/README.md) — one per phase
- [Branching & releases](BRANCHING.md)

Source: [github.com/khiladisngh/thumbforge](https://github.com/khiladisngh/thumbforge). MIT licensed.
