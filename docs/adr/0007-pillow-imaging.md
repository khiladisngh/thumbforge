# ADR 0007: Pillow for imaging

## Status

`Accepted` — 2026-09-19

## Context

After a provider returns art, `thumbforge` must fit it to the target 16:9 size, composite the title and "Part N" badge (ADR 0008), check YouTube compliance and write a JPEG/PNG under the size limit. Verified YouTube requirements (support.google.com/youtube/answer/72431): recommended 3840×2160, minimum width 640, 16:9, JPG/PNG, 2 MB limit on mobile and 50 MB on desktop.

## Decision

- **Pillow** is the sole imaging library, used in `src/thumbforge/imaging/`:
    - `fit.py`: resize and centre-crop any input to the configured `[output] width × height` (default 1920×1080, decision D2) using `Image.Resampling.LANCZOS`; upscaling from the provider's native size (Antigravity: 1376×768 pending spike S3) is permitted.
    - `overlay.py`: text rendering with `ImageDraw.text` and `ImageFont.truetype`, stroke and shadow, auto-shrink to fit the title box.
    - `fonts.py`: resolves fonts from the layout spec, falling back to a bundled OFL font (Inter, decision D6) in `imaging/fonts/`; golden tests use only bundled fonts.
    - `compliance.py`: the project check is stricter than YouTube's floor — aspect exactly 16:9 (±1 px), width ≥ 1280, format ∈ {JPEG, PNG}, file size ≤ `[output] max_bytes` (default 2 097 152; `--max-bytes` may raise it up to 50 MB), sRGB (ICC profile stripped or sRGB). Failure raises `ComplianceError` (exit `5`) and is stored in `asset.compliance_report_json`.
- Output encoding: `format="jpeg", quality=90` by default; if the result exceeds `max_bytes`, quality is stepped down by 5 to a floor of 70 before failing.
- Provider output is always opened through Pillow as the definition of "valid image" (`PLAN.md` §4.3 step 3).
- Golden tests (`-m golden`) compare overlay output against checked-in PNGs with a small per-pixel tolerance.

## Consequences

- One dependency covers decode, resize, text and encode; wheels exist for 3.14 on Windows and Linux.
- Text quality depends on Pillow's FreeType build, which is bundled in official wheels.
- Compliance numbers live in one module and are cited by `docs/specs/phase-5-imaging.md`.

## Alternatives considered

- **OpenCV** — rejected: large binary wheel, poor text rendering, no advantage for still-image compositing.
- **Wand / ImageMagick** — rejected: external binary dependency on Windows.
- **Asking the provider to render text** — rejected in ADR 0008.
- **`pyvips`** — rejected: needs libvips installed separately on Windows; Pillow is self-contained.
