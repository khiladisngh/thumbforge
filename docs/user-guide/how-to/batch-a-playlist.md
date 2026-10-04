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

## Choose what to generate

Three options shape a batch, and each does one job:

| Option           | What it does                                                                                                                                                                                                                                 |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--only 3,7-9`   | **Selects** parts, by part number (not position). `--only 1-3` is exactly parts 1, 2 and 3. Without it the batch covers every video that has a part number.                                                                                  |
| `--max-images N` | **Caps** the work and selects nothing: on its own it applies to every part. If more than `N` images would be generated, the batch refuses to start (exit `2`) and stores nothing. Items that are already completed do not count towards `N`. |
| `--dry-run`      | **Previews**: prints one row per item with the action it would take (`create`, `retry` or `skip`) and why, and makes no provider call. It ignores `--max-images`, so it plans the whole batch even when the cap would stop the real run.     |

The safe combination is the same `--only` three times: preview it with `--dry-run`, then run it with `--max-images` set to the `to generate` count the preview printed.

```
$ thumbforge batch <playlist-id> --hero <hero-run> --template series-parts --provider fake --only 1-3 --dry-run
…
3 to generate, 0 to retry, 0 to skip. Nothing was generated (--dry-run).
$ thumbforge batch <playlist-id> --hero <hero-run> --template series-parts --provider fake --only 1-3 --max-images 3
Batch run <batch-run>
…
```

Leave `--only` out and `--max-images` guards the whole playlist. For a 35-video playlist that has not been batched yet, `--dry-run --max-images 5` still plans all 35:

```
$ thumbforge batch <playlist-id> --hero <hero-run> --template series-parts --provider fake --dry-run --max-images 5
…
35 to generate, 0 to retry, 0 to skip. Nothing was generated (--dry-run).
```

and the same command without `--dry-run` stops before it makes anything:

```
$ thumbforge batch <playlist-id> --hero <hero-run> --template series-parts --provider fake --max-images 5
usage: 35 images to generate exceeds --max-images 5
hint: raise --max-images or narrow the batch with --only; --dry-run shows the
plan
```

## Running it again

An item's key is made from the template version, the provider, the video, its part number, the prompt and the reference image. An item whose key already has a finished image is skipped. So running the same `batch` command a second time generates nothing, but it still creates a run of its own, with no images in it:

```
$ thumbforge batch <playlist-id> --hero <hero-run> --template series-parts --provider fake --only 1-3
Batch run <batch-run-2>
…
$ thumbforge runs list
┏━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━┓
┃ Run         ┃ Kind    ┃ Status    ┃ Template   ┃ Provider    ┃ Done ┃ Failed ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━┩
│ <batch-run… │ batch   │ completed │ series-pa… │ fake@0.1.0… │ 0/0  │ 0      │
│ <batch-run… │ batch   │ completed │ series-pa… │ fake@0.1.0… │ 3/3  │ 0      │
…
```

The new run's table still lists the three finished items it found, but `runs list` shows `0/0` for it and `runs show` reports `0 completed, 0 failed, 0 pending of 0`: it made nothing. `runs resume` then refuses a run that is already `completed`:

```
$ thumbforge runs resume <batch-run-2>
usage: run <batch-run-2> is completed and cannot be resumed
hint: start a new batch to generate again
```

It exits `2`. The hint does not mean "run it again": an identical batch skips everything, as above. To get new images for the same parts, change something that goes into the key: pick another hero image (or use `--reference raw`), use another `--template` or `--provider`, or import a new version of the template. To finish a batch that was interrupted or had failures, use `runs resume` as described in [Resume an interrupted run](resume-an-interrupted-run.md).

## Export the results

```
thumbforge thumb export <batch-run> --to out/
```

writes one file per image named `<batch-run>-<n>.jpg`, with `n` counting from 1 in the order of the run's table (the `#` column of `runs show`). It is not the part number, so use the batch table to match files to parts. Exporting a hero run names its files after the video instead.

## When it does not all work

- `0`: every item is completed.
- `6`: some items failed and some completed; the completed ones are kept.
- `4`: nothing completed, every item that ran failed.
- `130`: you pressed Ctrl+C; the run is paused and finished items are kept.
- `3`: the playlist, hero, template or provider was not found.
- `2`: a bad option such as `--only 5-3`, `--max-images` below the work to do, or a hero run with no picked iteration.

For `6`, `4` and `130`, run `thumbforge runs resume <run>`: items that completed are skipped, and failed or unfinished ones are retried (a failed item is retried while it has tries left, 2 by default). Running the same `batch` command again retries the same items in a run of its own; see [Running it again](#running-it-again). See [Resume an interrupted run](resume-an-interrupted-run.md).

Add `--json` for one JSON object instead of the tables: the run, a summary and every item. Progress is never drawn in `--json` mode.
