# Try it on a playlist

Take a real public playlist from the first command to exported thumbnails, in twelve steps and about ten minutes. It uses the offline `fake` provider, so it costs nothing and needs no key; the images are placeholders, but every other step behaves as it will with a real provider. The sample output comes from a real run; run ids, timestamps and paths on your machine will differ.

The worked example is a public 35-part playlist, `PLzR-P7aCk914xnDyG-7_U0Bq0SunTERrI`, whose first video is `P_VKXcoLvO0`. To use your own, put its playlist id in place of the one below and a video id from `playlist show --videos` in place of the first video. Run ids and iteration ids are different every time, so those stay as `<run>` placeholders: copy them from the output of the step before.

To keep this out of your real database, set the scratch configuration and data directory first, as in [Getting started](../getting-started.md#where-thumbforge-keeps-its-files). The logs still go to the per-user state directory; see [Files and logs](../reference/cli.md#files-and-logs).

## 1. Install

```
$ uv tool install thumbforge
$ thumbforge --version
thumbforge 0.1.0
```

## 2. Set up and check

```
$ thumbforge db init
initialized database at <data-dir>/thumbforge.sqlite3 (0001)
$ thumbforge template list
┏━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┓
┃ Name         ┃ Version ┃ Builtin ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━┩
│ bold-title   │ 1       │ yes     │
│ minimal      │ 1       │ yes     │
│ series-parts │ 1       │ yes     │
└──────────────┴─────────┴─────────┘
$ thumbforge provider check fake
fake · healthy
…
```

`bold-title` draws a large title, and `series-parts` adds a "PART N" badge, which is what a series needs.

## 3. Fetch the playlist

```
$ thumbforge fetch "https://www.youtube.com/playlist?list=PLzR-P7aCk914xnDyG-7_U0Bq0SunTERrI"
╭───────────────── Playlist ─────────────────╮
│ <playlist title>   PLzR-P7aCk914xnDyG-7_U0Bq0SunTERrI   35 videos   <channel> │
╰────────────────────────────────────────────╯
┏━━━━┳━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ #  ┃ Part ┃ Video ID    ┃ Title   ┃
┡━━━━╇━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━┩
│ 1  │ 1    │ P_VKXcoLvO0 │ <title> │
│ 2  │ 2    │ UQTvV9-Nayo │ <title> │
…
Stored 1 channel, 1 playlist, 35 videos.
```

Use the playlist link, and put it in quotes. A watch link with `&list=…` on the end stores that one video and no playlist, and without quotes the `&` cuts the command short; see [Series and playlists](../concepts/series-and-playlists.md#fetching-a-playlist).

## 4. Look at the playlist

```
$ thumbforge playlist show PLzR-P7aCk914xnDyG-7_U0Bq0SunTERrI --videos
<playlist title>
Title       <playlist title>
YouTube id  PLzR-P7aCk914xnDyG-7_U0Bq0SunTERrI
Videos      35
Channel     <channel>
URL         https://www.youtube.com/playlist?list=PLzR-P7aCk914xnDyG-7_U0Bq0SunTERrI
Fetched     <timestamp>
┏━━━━┳━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ #  ┃ Part ┃ Video ID    ┃ Title   ┃
┡━━━━╇━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━┩
│ 1  │ 1    │ P_VKXcoLvO0 │ <title> │
…
```

The `Part` column is the number the badge will show. Here it equals the position, so no renumbering is needed; if your playlist opens with a trailer, see [Series and playlists](../concepts/series-and-playlists.md#position-and-part-number).

## 5. Look at one video

```
$ thumbforge video show P_VKXcoLvO0
<title>
Title       <title>
YouTube id  P_VKXcoLvO0
Length      9:06
Channel     <channel>
Published   —
URL         https://www.youtube.com/watch?v=P_VKXcoLvO0
Thumbnail   https://i.ytimg.com/vi/P_VKXcoLvO0/hqdefault.jpg?sqp=…
Fetched     <timestamp>
Playlists   1
```

The `Thumbnail` line is the address of the video's current thumbnail on YouTube. Thumbforge 0.1.0 has no command that downloads or shows it: open the address in a browser, or save it with `curl`. See [Getting started](../getting-started.md#work-with-a-playlist).

## 6. Generate candidates for the first video

```
$ thumbforge thumb generate P_VKXcoLvO0 --template bold-title --provider fake --n 4
Run <run>
Kind      hero
Status    completed
Template  bold-title@1
Provider  fake@0.1.0:<fingerprint>
Video     P_VKXcoLvO0
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
```

Copy the id on the first line: it is the `<run>` for the next two steps. This is the hero run, the one whose pick sets the look of the series.

## 7. Pick one and look at it

```
$ thumbforge thumb pick <run> 2
Picked #2 of run <run> (iteration <iteration-id>)
Export it with: thumbforge thumb export <run> --to PATH
$ thumbforge thumb show <run>
…
│ 2 ★ │ completed │ 1920x1080 │ ✔         │ <key>        │ —    │ <asset>      │
…
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ #      ┃ path                                                                ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ #1 ✔   │ <data-dir>/assets/<xx>/<asset-file>                                 │
│ #2 ★ ✔ │ <data-dir>/assets/<xx>/<asset-file>                                 │
…
```

`thumb show` marks the pick with a `★`. The path table above is what you get when the terminal cannot draw pictures, for example when the output is piped; on a colour terminal that handles UTF-8 you see a grid of small block-character pictures instead. Either way, open the files from the table in an image viewer to see the real candidates.

## 8. Refine it and pick again

```
$ thumbforge thumb iterate <run> --n 2 --prompt-append "warmer colours, golden hour light"
Run <refined-run>
Kind        iterate
Status      completed
Template    bold-title@1
Provider    fake@0.1.0:<fingerprint>
Video       P_VKXcoLvO0
Parent run  <run>
Reference   <asset>
…
$ thumbforge thumb pick <refined-run> 1
Picked #1 of run <refined-run> (iteration <iteration-id>)
Export it with: thumbforge thumb export <refined-run> --to PATH
```

`iterate` starts a new run from your pick, with your words added to the prompt. With a real provider those words steer the image; the `fake` provider only makes placeholders. The hero for the batch is `<refined-run>`.

## 9. Preview the batch

```
$ thumbforge batch PLzR-P7aCk914xnDyG-7_U0Bq0SunTERrI --hero <refined-run> --template series-parts --provider fake --only 1-3 --dry-run
┏━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ Part ┃ Title     ┃ Key      ┃ Action ┃ Reason ┃
┡━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ 1    │ <title>   │ <key>    │ create │ new    │
│ 2    │ <title>   │ <key>    │ create │ new    │
│ 3    │ <title>   │ <key>    │ create │ new    │
└──────┴───────────┴──────────┴────────┴────────┘
3 to generate, 0 to retry, 0 to skip. Nothing was generated (--dry-run).
```

`--only 1-3` selects parts 1, 2 and 3 by part number. `--dry-run` calls no provider. For a real provider, add `--max-images 3` to the real run: it refuses to start if more than three images would be made, but it never selects anything itself, and `--dry-run` ignores it. See [Batch a playlist](batch-a-playlist.md#choose-what-to-generate).

## 10. Run the batch

Run the same command without `--dry-run`:

```
$ thumbforge batch PLzR-P7aCk914xnDyG-7_U0Bq0SunTERrI --hero <refined-run> --template series-parts --provider fake --only 1-3
Batch run <batch-run>
Playlist    <playlist title>
Template    series-parts@1
Provider    fake@0.1.0:<fingerprint>
Reference   <asset> (final)
Parent run  <refined-run>
Status      completed
Items       3 completed, 0 failed, 0 pending of 3
…
```

The table that follows has one row per part. Run the command a second time and nothing is generated, because every item is already done; it still makes a new, empty run. See [Running it again](batch-a-playlist.md#running-it-again).

## 11. Inspect the runs

```
$ thumbforge runs list
┏━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━┓
┃ Run         ┃ Kind    ┃ Status    ┃ Template   ┃ Provider    ┃ Done ┃ Failed ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━┩
│ <batch-run… │ batch   │ completed │ series-pa… │ fake@0.1.0… │ 3/3  │ 0      │
│ <refined-r… │ iterate │ completed │ bold-titl… │ fake@0.1.0… │ 2/2  │ 0      │
│ <run>       │ hero    │ completed │ bold-titl… │ fake@0.1.0… │ 4/4  │ 0      │
└─────────────┴─────────┴───────────┴────────────┴─────────────┴──────┴────────┘
$ thumbforge runs show <batch-run>
…
Items       3 completed, 0 failed, 0 pending of 3
…
$ thumbforge runs cost <batch-run>
Run <batch-run> has no cost data: its provider reported none for its 3 iterations.
```

`runs list` shows the newest run first. `runs cost` has nothing to total for `fake`; a real provider that reports usage gets a total here.

## 12. Export

```
$ thumbforge thumb export <batch-run> --to out
Wrote out/<batch-run>-1.jpg
Wrote out/<batch-run>-2.jpg
Wrote out/<batch-run>-3.jpg
```

The files are numbered 1 to 3 in the order of the batch table, which here is part 1 to part 3. They are 1920x1080 JPEGs, ready to upload as each video's thumbnail. Exporting a hero run names its files after the video instead (`P_VKXcoLvO0-1.jpg`).

To do the whole playlist, run step 10 again without `--only`: the three finished parts are skipped, and the other 32 are generated. Set `--max-images 32` on it so a typing mistake cannot start a larger batch than you meant.

## With the real provider

Everything above works with a real provider by naming it. For Antigravity:

```
thumbforge provider check antigravity
thumbforge thumb generate P_VKXcoLvO0 --template bold-title --provider antigravity --n 4
thumbforge batch PLzR-P7aCk914xnDyG-7_U0Bq0SunTERrI --hero <refined-run> --template series-parts --provider antigravity --only 1-3 --max-images 3
```

`provider check antigravity` must pass first; see [Providers](../concepts/providers.md). Expect about a minute per image, so check a small batch before you run the rest. Antigravity cannot take a reference image, so `thumb iterate` and `batch` cannot copy the look of the hero from the picture: they run from the prompt alone, and warn you that the reference was not used. Put the look you want into the template and the `--prompt-append` words, and check a three-part batch before you run the rest.

## If something is not as described

[Common surprises](../getting-started.md#common-surprises) lists the behaviours that catch people out: a watch link that stores one video, `--max-images` selecting nothing, a repeated batch that makes nothing, logs that ignore your scratch directory, and `thumb show` printing paths.
