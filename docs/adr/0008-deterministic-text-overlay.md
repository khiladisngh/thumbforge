# ADR 0008: Deterministic text overlay over AI-generated background

## Status

`Accepted` — 2026-09-19

## Context

Playlist thumbnails must look like a set: identical title typography, identical "Part N" badge placement, consistent colours, across twelve or more images. Image models render text unreliably (misspellings, varying fonts, drifting positions), and the first provider (Antigravity CLI) offers no seed control and returns JPEG only (both pending spikes S3 and S6 in `OPEN_QUESTIONS.md`). The hero-then-batch workflow already gives the provider a reference image for style; text is the remaining source of inconsistency.

## Decision

**Yes: the AI paints the background; Pillow renders the text.**

- The provider prompt (rendered from the template's `.j2`, ADR 0006) asks for artwork with negative space in the region declared by the layout spec, and explicitly asks for **no text** in the image.
- `imaging/overlay.py` composites the title and, when `part` is set, a "Part N" badge onto the fitted image using the TOML layout spec (ADR 0006) and bundled fonts (ADR 0007). Output is stored as the iteration's `final_asset_id`; untouched provider output is `raw_asset_id`.
- The overlay is deterministic: same layout spec + same text + same fonts + same input image ⇒ byte-identical output. This is protected by golden tests.
- Batch runs default to `--reference final` (picked hero including its text) but support `--reference raw` so the provider never sees text it might imitate (`PLAN.md` §3.1 step 3).
- Because provider output may be JPEG (no alpha), the overlay composites onto an RGB canvas; the badge and text box carry their own alpha.
- Defaults for what is drawn (title only vs. title + badge) and the bundled font are decision D6.

## Consequences

- Batch consistency no longer depends on the model's typography; "Part N" is always correct.
- Titles can be edited (via `playlist renumber`, template variables) and re-rendered without regenerating art.
- Some artistic integration of text into the scene is lost; users wanting that can pass `--var no_overlay=true` in a template that renders text through the provider, at their own consistency risk.
- Two assets per iteration (`raw`, `final`) roughly doubles storage; deduplication by hash (ADR 0011) mitigates repeats.

## Alternatives considered

- **Let the provider render text** — rejected: observed misspellings and inconsistent placement; impossible to guarantee "Part 7" is legible and identical to "Part 6".
- **Inpainting a text region with a second provider call** — rejected: doubles cost and latency, and still leaves font choice to the model.
- **SVG compositing via a browser** — rejected: heavy runtime dependency for what `ImageDraw.text` already does.
