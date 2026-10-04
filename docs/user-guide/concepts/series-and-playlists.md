# Series and playlists

Thumbforge treats a YouTube playlist as a **series**: an ordered set of videos that should share one thumbnail style, each marked with its part number.

## Fetching a playlist

`thumbforge fetch <playlist-url>` stores the playlist, its channel and every video in your local database. It reads public metadata (titles, order, durations) with yt-dlp and needs no YouTube account or API key. Videos that leave the playlist on a later fetch are removed from the playlist, but their records and any thumbnails made for them are kept. A playlist fetched in the last 24 hours is shown from the database without going back to YouTube; `--refresh` re-reads it.

If you would rather use the YouTube Data API, install the optional `api` extra (`uv tool install "thumbforge[api]"`), store your key with `thumbforge provider set-key api` (or set `THUMBFORGE_PROVIDERS__API__API_KEY`), and run `thumbforge fetch --source api <url>`. It stores the same records. Without the extra, or without a key, `fetch --source api` exits `1` and says which one is missing.

## Position and part number

Each video in a playlist has two numbers:

- its **position** — where it sits in the playlist on YouTube;
- its **part number** — the number printed on its thumbnail.

When a playlist is first fetched, the part number equals the position, so the first video is Part 1. Often that is not what you want: a playlist may open with a trailer, or end with a behind-the-scenes extra. `thumbforge playlist renumber` reassigns the part numbers in playlist order from a starting number, and `--skip-ids` leaves chosen videos unnumbered. Skipped videos are not counted, so the remaining parts stay consecutive: skip the trailer and the first episode is still Part 1.

Your numbering survives `fetch --refresh`. `thumbforge playlist show <playlist> --videos` shows positions and part numbers side by side.

## The "Part N" badge

The badge is drawn by Thumbforge from the template's layout, not painted by the image model, so the number is always correct and looks the same on every thumbnail. The layout decides whether there is a badge at all, where it sits, and its wording — `"PART {n}"` in the built-in layouts, where `{n}` is the part number. The built-in `series-parts` template draws the badge; `bold-title` and `minimal` do not. A video without a part number gets no badge.

## Batching the series

`thumbforge batch <playlist> --hero <run>` generates one thumbnail for every video in the playlist, each with its own title and badge, in the style of your picked hero. `--only 3,7-9` limits it to some parts (the numbers are part numbers, so renumber first). See [Batch a playlist](../how-to/batch-a-playlist.md).

## Going deeper

- [Glossary](../../developers/glossary.md) — part number, batch, idempotency key.
- [Phase 2 spec](../../specs/phase-2-youtube-fetch.md#behaviour) — exact fetch and renumber rules.
- [Phase 7 spec](../../specs/phase-7-batch.md#behaviour) — exact batch rules.
- [ADR 0008](../../adr/0008-deterministic-text-overlay.md) — why badges are drawn, not generated.
