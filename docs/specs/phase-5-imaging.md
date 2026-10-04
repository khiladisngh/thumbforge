# Phase 5 — Imaging

Status: Implemented (P5.1–P5.4)
ROADMAP tasks: P5.1, P5.2, P5.3, P5.4
ADRs: `docs/adr/0007-pillow-imaging.md`, `docs/adr/0008-deterministic-text-overlay.md`, `docs/adr/0002-typer-rich-cli.md`, `docs/adr/0018-shared-models-live-in-core.md`, `docs/adr/0019-complex-script-titles.md`

## Scope

Turn raw provider art into a final, YouTube-compliant thumbnail: fit/crop to the target 16:9 size, overlay title and "Part N" text deterministically with Pillow, check compliance, and preview in the terminal.

- **P5.1** `imaging/fit.py` — resize/crop to 1280×720 / 1920×1080 (or any 16:9 target).
- **P5.2** `imaging/overlay.py`, `imaging/fonts.py`, bundled font under `imaging/fonts/`; golden tests.
- **P5.3** `imaging/compliance.py`, `imaging/finalize.py`.
- **P5.4** `cli/_render.py` preview helper via `rich-pixels`.
- **Devanagari titles** (after P5.4, ADR 0019) `imaging/face.py`, `imaging/runs.py`, `imaging/shaping.py`, `imaging/glyphfont.py`, bundled `NotoSansDevanagari-Bold.ttf`; goldens for Hindi titles.

## Non-goals

- Asking the provider to render text — ADR 0008 forbids it; the prompt only requests negative space.
- Upscaling models (ESRGAN etc.); `fit` uses Pillow `LANCZOS` only.
- Inline terminal image protocols (kitty/iTerm) — spike S10 marks them deferred.

## Interfaces

`LayoutSpec` is defined in `core/layout.py` (P4.1) and `ComplianceReport` in `core/models.py`, because `core.services` consumes both and `core` may import no other package. `imaging` joins `templates`, `storage`, `sources` and `providers` in the `adapters are independent` contract, so it never imports `templates` or `storage`: nothing here touches the database or the asset store.

```python
# imaging/fit.py
def fit_to(img: Image.Image, width: int, height: int) -> Image.Image
    # scale so the target is fully covered, then centre-crop to exactly width×height; converts to RGB

# imaging/fonts.py
def resolve_font(name: str, size_px: int, *, config_dir: Path | None = None) -> ImageFont.FreeTypeFont
    # lookup order: <config_dir>/fonts/<name>.ttf, bundled imaging/fonts/<name>.ttf, bundled Inter-Bold.ttf fallback (logged at WARNING, event fonts.fallback)
    # config_dir defaults to platformdirs.user_config_dir("thumbforge"); a name that is not a bare file stem skips straight to the fallback
    # fonts load with the BASIC layout engine so output does not depend on libraqm
def font_path(name: str, *, config_dir: Path | None = None) -> Path    # the same lookup, returning the file

# imaging/face.py (ADR 0019)
def resolve_face(name: str, size_px: int, *, text: str, config_dir: Path | None = None) -> Face
    # the layout's font for `text`, plus the bundled Devanagari fallback only when `text` has characters the font lacks that the fallback covers;
    # Face offers size, getlength, getmetrics, font_variant and draw_line, so a Latin-only title measures and draws exactly like the plain Pillow font
    # characters neither font covers are drawn as the layout font's missing-glyph box, with one WARNING (event fonts.uncovered, field count, never the text)

# imaging/overlay.py
def overlay(img: Image.Image, layout: LayoutSpec, *, title: str, part_number: int | None, part_label: str | None) -> Image.Image
    # wraps/shrinks title into layout.title.box respecting max_lines/min_size_px; draws stroke then fill; draws part badge when enabled and part_number is not None

# core/models.py
class ComplianceReport(BaseModel, frozen=True):
    ok: bool
    width: int; height: int; bytes: int; format: str; color_mode: str
    violations: list[str]

# imaging/compliance.py
def check(data: bytes, *, max_bytes: int = 2_097_152) -> ComplianceReport

# imaging/finalize.py
def render_final(raw: Path, layout: LayoutSpec, output: OutputSettings, *, title: str, part_number: int | None, part_label: str | None) -> tuple[bytes, ComplianceReport]
    # fit to layout.canvas → overlay → fit to output size → encode (jpeg quality / png) → re-encode 5 quality lower while bytes > max_bytes (floor 60) → check
```

Persisting the result is not Phase 5's job: P6.1's `HeroService` (in `core`) receives `render_final` as an injected callable (the CLI binds `output`), stores the bytes as the `final` asset, and records the report.

### Compliance rule

| Check  | Rule                                                                   |
| ------ | ---------------------------------------------------------------------- |
| Aspect | exactly 16:9, tolerance ±1 px on either dimension                      |
| Width  | ≥ 1280 px (project floor; YouTube's minimum is 640)                    |
| Format | JPEG or PNG                                                            |
| Size   | ≤ 2,097,152 bytes by default; `--max-bytes` overrides up to 52,428,800 |
| Colour | sRGB (mode `RGB`; embedded ICC other than sRGB is a violation)         |

Default output is 1920×1080 (decision D2; `[output] width/height`), upscaled with `LANCZOS` from the provider's native size when smaller (Antigravity's reported 1376×768 is spike S3).

### Preview

`_render.preview(ctx: AppContext, paths: Sequence[Path], columns: int = 2) -> None` draws each image as a `rich_pixels.Pixels` tile, `columns` tiles per row, laid out with `Table.grid(padding=(0, 1))` (`rich.columns.Columns` stacks `Pixels` tiles instead of placing them side by side, spike S10). Each tile is as wide as its cell, `max((console.width - (columns - 1)) // columns, 8)`, keeps the image's aspect ratio (resampled with `LANCZOS`, like `fit_to`), and carries the file name as a dim caption; a short last row is padded with empty cells. `ctx` comes first, like `emit`: in `--json` mode, or with no paths, it prints nothing. `columns < 1` raises `ValueError`. When the console cannot show colour blocks (not a terminal, no colour system, a non-UTF-8 encoding, `--no-color`/`NO_COLOR`, dumb terminal, legacy Windows console) or any path cannot be opened or decoded, it prints a numbered `#`/`path` table and a dim `thumbforge thumb export` hint instead; it never raises for a bad image. Used by `thumb show`, `thumb generate`, `batch` summary.

## Behaviour

1. `fit_to` never distorts: scale = `max(width/w, height/h)`, then crop; a source already at the target size is returned unchanged (same object not guaranteed, pixels identical).
2. `overlay` is deterministic: same input image, layout, text and bundled font → byte-identical output on every OS. Only bundled fonts are used in tests.
3. Title layout: text is upper-cased per `layout.title.case`, wrapped by words into ≤ `max_lines` at `size_px`; if it does not fit, size decreases by 4 px until `min_size_px`; if it still does not fit, the last line is ellipsised and a `WARNING` is logged. An ellipsis never follows a dangling virama or joiner.
4. Part badge: rendered only when `layout.part.enabled` and `part_number is not None`; `{n}` and `{label}` are filled by plain string replacement, never `str.format`, because layouts are user data. `part_label` replaces `{label}`; when it is missing or empty, `{label}` is removed and the whitespace collapsed (`"{label} {n}"` → `"7"`). With `part.badge` the text sits on a rounded rectangle and is black or white by the fill's luminance; without it the text takes the title's colour and stroke. The badge is placed by `part.anchor` inside the canvas inset by `canvas.safe_margin_px`.
5. `render_final` fits the raw to `layout.canvas` (overlay coordinates are canvas pixels), overlays, then fits to `[output] width/height` (a plain copy when they match, a `LANCZOS` rescale otherwise). A canvas with a different aspect ratio than the output raises `TemplateError` (the final fit would crop the overlay), hint "use a canvas with the same aspect ratio as [output] width/height". A JPEG over `max_bytes` is re-encoded 5 quality lower at a time, never below 60; a starting quality at or below 60 is kept, and PNG is encoded once. It returns the encoded bytes and the report even when the report is not `ok`, so the caller can store the non-compliant asset for inspection before raising `ComplianceError` (exit `5`; P6.1). `violations` holds the codes `aspect`, `width`, `format`, `size`, `color`, in that order; an ICC profile counts as sRGB when its description contains `sRGB`, and an unreadable one is a violation.
6. JPEG encode: `quality=[output] quality`, `subsampling=0`, `optimize=True`; PNG: `optimize=True`. Metadata stripped, including what Pillow would copy from the raw (a PNG's ICC profile). Pillow holds an optimized JPEG in one buffer of `width×height` bytes below quality 95 (2,073,600 at 1920×1080, under the 2 MiB default), so the encode raises `PIL.ImageFile.MAXBLOCK` to at least `2×width×height` for the save and restores it afterwards.
7. Fallback font (ADR 0019): when the title has characters the layout's font lacks and `NotoSansDevanagari-Bold` covers, the title is split into runs by the font that covers each character (joiners and combining marks stay with the character they attach to). Latin runs use the layout's font; Devanagari runs are shaped with HarfBuzz (OpenType shaper, script `Deva`, language `hi`, left to right: never the machine's locale) and each glyph is drawn through Pillow's BASIC engine at its HarfBuzz position, so the pixels stay identical on every OS and no libraqm is involved. Runs sit on one baseline; line height is the larger ascent plus the larger descent of the two fonts; wrapping, shrinking, `max_lines`, `min_size_px`, anchor and case work as for Latin. Strokes are drawn for every glyph first and fills second, so a stroke never covers a neighbouring glyph. The Part badge text still uses its own font alone.

## Acceptance criteria

- `fit_to(Image.new("RGB", (1376, 768)), 1920, 1080).size == (1920, 1080)`; `fit_to(Image.new("RGB", (4000, 1000)), 1920, 1080)` crops the sides and is `(1920, 1080)`.
- Golden: overlaying `tests/fixtures/imaging/flat-grey.png` with the `bold-title` layout and title `Ownership explained` produces pixels equal to `tests/golden/overlay/bold-title-ownership.png`; same for `series-parts` with `part_number=7`.
- A 40-word title with `max_lines = 3` renders at `min_size_px` with an ellipsis and logs `overlay.title_truncated`.
- Golden: `render_final` with the `bold-title` layout and the bilingual title `Mahabharat Bhag 01 - Hindi Audiobook | महाभारत भाग 01 - हिंदी ऑडियोबुक` equals `tests/golden/overlay/bold-title-bhag-01.png`, and with `series-parts` (parts 2 and 3) equals `series-parts-bhag-02-part-2.png` and `series-parts-bhag-03-part-3.png`; the same pixels on Windows and Linux. Latin-only titles still equal the goldens made before the fallback font.
- `check` on a 1920×1080 JPEG of 1.5 MB returns `ok=True`; on 1919×1080 returns `ok=True` (±1 px); on 1918×1080 returns `ok=False` with `aspect` in `violations`; on 1280×720 PNG `ok=True`; on 1024×576 `ok=False` with `width`; on a 3 MB JPEG `ok=False` with `size` unless `max_bytes=52_428_800`; on a CMYK JPEG `ok=False` with `color`.
- `render_final` on a raw image that encodes to more than 2,097,152 bytes at quality 90 lowers quality until it fits and returns a report with `ok=True`.
- `thumbforge thumb show <run>` in Windows Terminal draws a block-character preview (manual check, spike S10); with `--json` it prints only JSON.

## Test plan

- Unit: `fit_to` size matrix; `resolve_font` fallback order with `tmp_path` config dir; `check` matrix above using synthetic images from Pillow; `render_final` quality loop with a noise image.
- Golden (`-m golden`): overlay snapshots for the `bold-title` and `series-parts` layouts, built in the test module, plus real finals of Hindi titles from the built-in layouts; compared on exact decoded pixels; regenerated only via `uv run pytest -m golden --update-golden` and reviewed in the PR diff.
- Contract / integration: none.

## Open spikes

- **S3** Antigravity output size/format — decides whether upscaling from 1376×768 is the normal path for the default 1920×1080 output.
- **S10** terminal image preview with `rich-pixels` — **closed** (except legibility in Windows Terminal; `docs/spikes/terminal-preview.md`): tiles and the `Table.grid` layout verified under a Linux pty; legibility in Windows Terminal remains the manual `thumb show` check above.
