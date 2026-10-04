# User guide

This guide is for people who install Thumbforge and run it: creators who publish videos in series or playlists and want every thumbnail to share one look, with the right title and part number on each. It assumes you are comfortable typing commands in a terminal. It does not assume you know Python.

## What you can do

- **Set up** — `thumbforge config init|show|path|set` writes and inspects the configuration file; `thumbforge db init|upgrade|status|path|vacuum` creates and maintains the local database.
- **Fetch metadata** — `thumbforge fetch <url>` stores a video, playlist or channel's metadata (titles, order, durations) without a YouTube API key; `--source api` uses the YouTube Data API instead (optional extra). `thumbforge playlist list|show` and `thumbforge video list|show` browse what you fetched.
- **Number the parts** — `thumbforge playlist renumber` assigns the "Part N" numbers, optionally leaving a trailer or an outro unnumbered.
- **Choose a provider** — `thumbforge provider list|check|models|set-key` shows which image providers are installed, checks that they are ready, and stores their API keys in the system keyring.
- **Manage templates** — `thumbforge template list|show|new|import|validate|render` lists the built-in templates, copies one for editing, stores your own as numbered versions, checks a layout, and prints the prompt a template produces for a stored video without calling any provider.
- **Generate a hero** — `thumbforge thumb generate` makes candidates for one video; `thumb show`, `thumb pick` and `thumb export` compare, choose and copy them out; `thumb iterate` refines the pick.
- **Batch a playlist** — `thumbforge batch` makes one thumbnail per video in the style of the picked hero, with progress, a summary table and `--dry-run`.
- **Manage runs** — `thumbforge runs list|show|cost|resume|cancel|delete` inspects every run, totals what it cost, finishes an interrupted batch, and cleans up.
- **Complete commands** — `thumbforge --install-completion` sets up Tab completion in bash, zsh, fish and PowerShell; see [Shell completion](how-to/shell-completion.md).

## In this guide

- [Getting started](getting-started.md) — install, then a first run from fetching a video to batching a playlist.
- Concepts — [Hero](concepts/hero.md), [Series and playlists](concepts/series-and-playlists.md), [Templates](concepts/templates.md), [Providers](concepts/providers.md).
- How-to guides — [Generate a hero](how-to/generate-a-hero.md), [Pick and refine](how-to/pick-and-refine.md), [Batch a playlist](how-to/batch-a-playlist.md), [Resume an interrupted run](how-to/resume-an-interrupted-run.md), [Write a custom template](how-to/write-a-custom-template.md), [Shell completion](how-to/shell-completion.md).
- Reference — [CLI reference](reference/cli.md), with every command and the exit codes.
