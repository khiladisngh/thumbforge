# User guide

This guide is for people who install Thumbforge and run it: creators who publish videos in series or playlists and want every thumbnail to share one look, with the right title and part number on each. It assumes you are comfortable typing commands in a terminal. It does not assume you know Python.

## What works today

Thumbforge is pre-alpha. These commands exist and work now:

- **Setup** — `thumbforge config init|show|path|set` writes and inspects the configuration file; `thumbforge db init|upgrade|status|path|vacuum` creates and maintains the local database.
- **Metadata** — `thumbforge fetch <url>` stores a video, playlist or channel's metadata (titles, order, durations) without a YouTube API key. `thumbforge playlist list|show` and `thumbforge video list|show` browse what you fetched.
- **Part numbers** — `thumbforge playlist renumber` assigns the "Part N" numbers, optionally leaving a trailer or an outro unnumbered.
- **Providers** — `thumbforge provider list|check|models|set-key` shows which image providers are installed, checks that they are ready, and stores their API keys in the system keyring.
- **Templates** — `thumbforge template validate` checks a layout file; `thumbforge template render` prints the prompt a template produces for a stored video, without calling any provider.
- **Shell completion** — `thumbforge --install-completion` sets up Tab completion in bash, zsh, fish and PowerShell; see [Shell completion](how-to/shell-completion.md).

## What lands in v0.1.0

!!! note "Coming in v0.1.0"

    Generating thumbnails is not implemented yet. The [roadmap](../ROADMAP.md) plans, in order:

    - built-in templates and template management (`template list|show|new|import`) — [Phase 4 spec](../specs/phase-4-templates.md);
    - the final image: fit to 16:9, text overlay and the YouTube compliance check — [Phase 5 spec](../specs/phase-5-imaging.md);
    - generating, picking, refining and exporting a hero (`thumb generate|pick|show|export|iterate`) — [Phase 6 spec](../specs/phase-6-hero.md);
    - batching a whole playlist, with resume and cancel (`batch`, `runs list|show|resume|cancel|delete`) — [Phase 7 spec](../specs/phase-7-batch.md);
    - an optional YouTube Data API source and a cost report — [Phase 8 spec](../specs/phase-8-polish.md).

    The [specs overview](../specs/README.md) shows which phases are implemented.

## In this guide

- [Getting started](getting-started.md) — install, then a first run with the commands that exist today.
- Concepts — [Hero](concepts/hero.md), [Series and playlists](concepts/series-and-playlists.md), [Templates](concepts/templates.md), [Providers](concepts/providers.md).
- How-to guides — [Generate a hero](how-to/generate-a-hero.md), [Pick and refine](how-to/pick-and-refine.md), [Batch a playlist](how-to/batch-a-playlist.md), [Resume an interrupted run](how-to/resume-an-interrupted-run.md), [Write a custom template](how-to/write-a-custom-template.md), [Shell completion](how-to/shell-completion.md).
- Reference — [CLI reference](reference/cli.md).
