# Hero

A **hero** is the one thumbnail you choose for one video, and the style every other thumbnail in the series follows. You get to it in three steps: generate a few candidates, pick the best, and optionally refine it.

## Runs and iterations

Every time Thumbforge generates images it records a **run**. A run holds one or more **iterations**: each iteration is one image attempt, with the prompt and settings that produced it.

There are three kinds of run:

| Kind      | What it does                                                                     |
| --------- | -------------------------------------------------------------------------------- |
| `hero`    | Generates several candidate thumbnails (four by default) for one video.          |
| `iterate` | Refines a hero: generates new candidates using the picked one as a reference.    |
| `batch`   | Generates one thumbnail per video in a playlist, using the picked hero as style. |

A run is `pending`, `running`, `paused`, `completed`, `failed` or `cancelled`. Runs and their images stay in your local database, so you can come back to them later.

## Picking and refining

From a hero run you **pick** exactly one iteration. Picking again simply moves the mark. To refine, you start an `iterate` run from the picked image, optionally adding words to the prompt ("warmer colours", "more contrast"). The refinement is a new run linked to the one it came from, so the lineage stays visible and nothing is overwritten.

## Background art and text are separate

The image provider paints only the background. Thumbforge then fits the image to 16:9, draws the title and the "Part N" badge itself from the template's layout, and checks the result against YouTube's thumbnail requirements. Each iteration therefore keeps two images:

- the **raw** image, exactly as the provider returned it;
- the **final** image, fitted, with text, ready to upload.

Because the text is drawn the same way every time, titles are spelled correctly and every part of a series has identical typography — something image models do not reliably do. See [Templates](templates.md) for the layout that controls the text.

!!! note "Coming in v0.1.0"

    Refining a hero (`thumbforge thumb iterate`) is roadmap task P6.3, defined in the [Phase 6 spec](../../specs/phase-6-hero.md#behaviour); generating, picking, showing and exporting (`thumb generate|pick|show|export`) work today. The overlay and compliance check are defined in the [Phase 5 spec](../../specs/phase-5-imaging.md). See [Generate a hero](../how-to/generate-a-hero.md) and [Pick and refine](../how-to/pick-and-refine.md).

## Going deeper

- [Glossary](../../developers/glossary.md) — exact definitions of hero, run, iteration, raw and final asset.
- [ADR 0008](../../adr/0008-deterministic-text-overlay.md) — why the text is drawn by Thumbforge, not by the model.
- [ADR 0012](../../adr/0012-idempotency-and-resumable-runs.md) — run states and how runs resume.
