# Generate a hero

Generate several candidate thumbnails for one video with a chosen template and provider, compare them side by side in the terminal, and keep the run so you can pick one. The result is a `hero` run whose iterations each hold a raw image from the provider and a final, fitted image with the title drawn on it. See [Hero](../concepts/hero.md) for the ideas behind it.

## Before you start

```
thumbforge config init
thumbforge db init
thumbforge fetch "https://www.youtube.com/watch?v=<video-id>"
thumbforge provider check fake
```

The video has to be fetched first: `thumb generate` takes the video's YouTube id, its URL or its stored id (a ULID), and exits `3` when it is not in the database. `db init` also stores the built-in templates (`bold-title`, `minimal`, `series-parts`). A template of your own has to be imported before a run can use it; see [Write a custom template](write-a-custom-template.md).

## Generate

```
thumbforge thumb generate <video-id> --n 3
```

```
Run <run>
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
└───┴───────────┴───────────┴───────────┴──────────────┴──────┴───────────────┘
Copy images out with: thumbforge thumb export <run|iteration> --to PATH
Pick one with: thumbforge thumb pick <run> <ordinal>
```

It prints the run, then one row per candidate: its number, status, final size, whether the final passes YouTube's thumbnail rules, a short idempotency key, the cost the provider reported (`—` when it reported none, as the `fake` provider does) and the stored image or the error. On a colour terminal that handles UTF-8 you also get a preview of every candidate, drawn in block characters; elsewhere (output piped, `--no-color`) you get a table of file paths. The run id on the first line is what `thumb pick`, `thumb show`, `thumb export` and `thumb iterate` take next.

## Options

- `--template NAME` or `NAME@VERSION` picks the template; without it, `[general] default_template` applies (`bold-title`). A bare name means its latest version.
- `--provider KEY` picks the provider; without it, `[general] default_provider` applies (`fake`). See [Providers](../concepts/providers.md).
- `--n 4` is how many candidates to make (4 by default).
- `--seed 7` is the first seed; candidate _k_ uses `seed + k - 1`, for a provider that accepts a seed. Without it the seeds count up from 0.
- `--var key=value` fills a variable the template's prompt uses (`{{ vars.key }}`); repeat it for more. A variable the prompt needs and you did not give is an error and no run is made (exit `2`).
- `--concurrency N` is how many provider calls run at once; without it, `[batch] concurrency` applies (1). A provider can lower it.
- `--out DIR` also copies every completed final into `DIR` as `<video-id>-<number>.jpg`.

`thumbforge --json thumb generate ...` prints one JSON document instead of the tables (global options go before the command name).

## When it does not all work

- `0`: every candidate completed.
- `6`: some candidates failed and some completed; the completed ones are kept.
- `4`: nothing completed.
- `5`: every failure was a compliance failure: the images were made but a final breaks one of YouTube's rules. `thumb show` still draws them with a ✘ so you can see why.
- `3`: the video, template or provider was not found.
- `2`: a bad option, or a template variable with no value.

A hero run is not resumed. Fix the cause and run `thumb generate` again; each run keeps its own candidates.

## Next

Compare and choose with [Pick and refine](pick-and-refine.md). To preview the prompt a template produces without calling a provider, use `thumbforge template render <template> --video <video-id>`.
