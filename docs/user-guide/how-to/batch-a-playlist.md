# Batch a playlist

Generate one thumbnail for every video in a playlist, using your picked hero as the style reference, with each video's own title and "Part N" badge drawn on top. You can preview the plan without generating anything, limit the batch to some parts, cap the number of images, and watch progress per video. See [Series and playlists](../concepts/series-and-playlists.md).

## Before you start

```
thumbforge fetch "https://www.youtube.com/playlist?list=<playlist-id>"
thumbforge playlist show <playlist-id> --videos
thumbforge playlist renumber <playlist-id> --start 1 --skip-ids <trailer-video-id>
thumbforge template render my-series --video <video-id> --var mood=bright
```

Get the part numbers right before batching: they are what the badges show, and `--only` selects parts by number. The batch uses the playlist as it is stored; run `fetch` again to pick up new videos.

You also need a hero: a completed `thumb generate` run with one iteration picked (`thumb pick`), or the id of any completed iteration.

## Run it

```
thumbforge batch <playlist-id> --hero <hero-run> --template series-parts --provider fake
```

`--hero` takes a run id (its picked iteration is the reference) or an iteration id. `--template` and `--provider` default to the `[general]` settings, `--concurrency` to `[batch] concurrency`.

On a terminal a progress bar on stderr shows each item as it finishes, with its part and title. When it is done, stdout has a table with one row per item: part, title, status, size, compliance, asset and, for a failure, the error. Items that were already `completed` from an earlier batch are listed too, and are not generated again.

Choose which hero image is the reference with `--reference final` (the default: the finished thumbnail, text and all) or `--reference raw` (the provider's art without the overlay). A different reference makes a different batch, so the playlist is generated again.

## Look before you spend

```
thumbforge batch <playlist-id> --hero <hero-run> --dry-run
```

prints the plan, one row per item with the action it would take (`create`, `retry` or `skip`) and why, and makes no provider call. `--only 3,7-9` limits the batch to those part numbers, `--max-images 5` refuses to start (exit `2`) if more than five images would be generated.

## When it does not all work

- `0`: every item is completed.
- `6`: some items failed and some completed; the completed ones are kept.
- `4`: nothing completed, every item that ran failed.
- `130`: you pressed Ctrl+C; the run is paused and finished items are kept.
- `3`: the playlist, hero, template or provider was not found.
- `2`: a bad option such as `--only 5-3`, `--max-images` below the work to do, or a hero run with no picked iteration.

For `6`, `4` and `130`, run the same command again: items that completed are skipped, and failed or unfinished ones are retried (a failed item is retried while it has tries left, 2 by default). See [Resume an interrupted run](resume-an-interrupted-run.md).

Add `--json` for one JSON object instead of the tables: the run, a summary and every item. Progress is never drawn in `--json` mode.
