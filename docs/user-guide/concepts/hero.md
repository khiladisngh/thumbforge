# Hero

A **hero** is the one thumbnail you choose for one video, and the style every other thumbnail in the series follows. You get to it in three steps: generate a few candidates, pick the best, and optionally refine it. Then you hand it to `batch`.

## Runs and iterations

Every time Thumbforge generates images it records a **run**. A run holds one or more **iterations**: each iteration is one image attempt, with the prompt and settings that produced it.

There are three kinds of run:

| Kind      | Made by                | What it does                                                                     |
| --------- | ---------------------- | -------------------------------------------------------------------------------- |
| `hero`    | `thumb generate`       | Generates several candidate thumbnails (four by default) for one video.          |
| `iterate` | `thumb iterate`        | Refines a hero: generates new candidates using the picked one as a reference.    |
| `batch`   | `batch`, `runs resume` | Generates one thumbnail per video in a playlist, using the picked hero as style. |

A run is `pending`, `running`, `paused`, `completed`, `failed` or `cancelled`. Runs and their images stay in your local database, so you can come back to them later: `thumbforge runs list` shows them, `runs show` prints one, and `runs cost` totals what a provider reported it used.

Only `batch` runs can be resumed. A `hero` or `iterate` run is small, so if it fails you run `thumb generate` or `thumb iterate` again. See [Resume an interrupted run](../how-to/resume-an-interrupted-run.md).

## Picking and refining

From a hero run you **pick** exactly one iteration. Picking again simply moves the mark, and only an iteration that completed can be picked. `thumb show` stars the picked one.

To refine, you run `thumb iterate` on the run (it takes the picked image) or on one iteration's id, optionally adding words to the prompt ("warmer colours", "more contrast"). The refinement is a new `iterate` run linked to the one it came from, using the picked image as its reference, so nothing is overwritten. `runs show` prints the link: the refinement shows its `Parent run` and the reference image, and the run it came from lists its `Child runs`. Pick from the new run to refine again, as many times as you like.

A provider that cannot take a reference image refines from the prompt alone, and tells you so.

## From hero to batch

`thumbforge batch <playlist> --hero <run>` uses the picked iteration of that run as the style reference for every video in the playlist. A hero run with no pick is refused. `--reference final` (the default) hands the provider the finished thumbnail, text included; `--reference raw` hands it the art without the overlay. See [Batch a playlist](../how-to/batch-a-playlist.md).

## Background art and text are separate

The image provider paints only the background. Thumbforge then fits the image to 16:9, draws the title and the "Part N" badge itself from the template's layout, and checks the result against YouTube's thumbnail requirements. Each iteration therefore keeps two images:

- the **raw** image, exactly as the provider returned it;
- the **final** image, fitted, with text, ready to upload.

Because the text is drawn the same way every time, titles are spelled correctly and every part of a series has identical typography — something image models do not reliably do. See [Templates](templates.md) for the layout that controls the text.

The check on each final covers the 16:9 ratio (within one pixel), a width of at least 1280, JPEG or PNG, a file size within `[output] max_bytes` (2 MB by default) and sRGB colour. The result shows as a ✔ or ✘ in the `Compliant` column. A final that fails is kept so you can look at it, but its iteration counts as failed: it cannot be picked or exported, and when every failure in a run is a compliance failure the command exits `5`.

## Going deeper

- [Generate a hero](../how-to/generate-a-hero.md) and [Pick and refine](../how-to/pick-and-refine.md) — the commands, step by step.
- [Glossary](../../developers/glossary.md) — exact definitions of hero, run, iteration, raw and final asset.
- [ADR 0008](../../adr/0008-deterministic-text-overlay.md) — why the text is drawn by Thumbforge, not by the model.
- [ADR 0012](../../adr/0012-idempotency-and-resumable-runs.md) — run states and how runs resume.
