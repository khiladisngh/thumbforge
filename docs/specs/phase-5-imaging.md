# Phase 5 — Imaging

Status: Proposed
ROADMAP tasks: P5.1, P5.2, P5.3, P5.4
ADRs: `docs/adr/0007-pillow-imaging.md`, `docs/adr/0008-deterministic-text-overlay.md`, `docs/adr/0002-typer-rich-cli.md`

## Scope

Turn raw provider art into a final, YouTube-compliant thumbnail: fit/crop to the target 16:9 size, overlay title and "Part N" text deterministically with Pillow, check compliance, and preview in the terminal.

- **P5.1** `imaging/fit.py` — resize/crop to 1280×720 / 1920×1080 (or any 16:9 target).
- **P5.2** `imaging/overlay.py`, `imaging/fonts.py`, bundled font under `imaging/fonts/`; golden tests.
- **P5.3** `imaging/compliance.py`, `imaging/finalize.py`.
- **P5.4** `cli/_render.py` preview helper via `rich-pixels`.

## Non-goals

- Asking the provider to render text — ADR 0008 forbids it; the prompt only requests negative space.
- Upscaling models (ESRGAN etc.); `fit` uses Pillow `LANCZOS` only.
- Inline terminal image protocols (kitty/iTerm) — spike S10 marks them deferred.

## Interfaces

`LayoutSpec` is defined in `core/layout.py` (P4.1) and `ComplianceReport` in `core/models.py`, because `core.services` consumes both and `core` may import no other package. `imaging` joins `templates`, `storage`, `sources` and `providers` in the `adapters are independent` contract, so it never imports `templates` or `storage`: nothing here touches the database or the asset store.

```python
# imaging/fit.py
def fit_to(img: Image.Image, width: int, height: int, *, anchor: Anchor = "center") -> Image.Image
    # scale so the target is fully covered, then centre-crop (or anchor-crop) to exactly width×height; converts to RGB

# imaging/fonts.py
def resolve_font(name: str, size_px: int) -> ImageFont.FreeTypeFont
    # lookup order: <config_dir>/fonts/<name>.ttf, bundled imaging/fonts/<name>.ttf, bundled Inter-Bold.ttf fallback (logged at WARNING)

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
    # fit → overlay → encode (jpeg quality / png) → re-encode at lower quality while bytes > max_bytes (floor quality 60) → check
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

`_render.preview(paths: list[Path], columns: int = 2) -> None` renders each image with `rich_pixels.Pixels.from_image_path` scaled to the terminal width; in `--json` mode it is a no-op. Used by `thumb show`, `thumb generate`, `batch` summary.

## Behaviour

1. `fit_to` never distorts: scale = `max(width/w, height/h)`, then crop; a source already at the target size is returned unchanged (same object not guaranteed, pixels identical).
2. `overlay` is deterministic: same input image, layout, text and bundled font → byte-identical output on every OS. Only bundled fonts are used in tests.
3. Title layout: text is upper-cased per `layout.title.case`, wrapped by words into ≤ `max_lines` at `size_px`; if it does not fit, size decreases by 4 px until `min_size_px`; if it still does not fit, the last line is ellipsised and a `WARNING` is logged.
4. Part badge: rendered only when `layout.part.enabled` and `part_number is not None`; `part_label` replaces `{label}`; missing label with `{label}` in format falls back to `{n}` formatting.
5. `render_final` returns the encoded bytes and the report even when the report is not `ok`, so the caller can store the non-compliant asset for inspection before raising `ComplianceError` (exit `5`; P6.1).
6. JPEG encode: `quality=[output] quality`, `subsampling=0`, `optimize=True`; PNG: `optimize=True`. Metadata stripped.

## Acceptance criteria

- `fit_to(Image.new("RGB", (1376, 768)), 1920, 1080).size == (1920, 1080)`; `fit_to(Image.new("RGB", (4000, 1000)), 1920, 1080)` crops the sides and is `(1920, 1080)`.
- Golden: overlaying `tests/fixtures/imaging/flat-grey.png` with the `bold-title` layout and title `Ownership explained` produces bytes equal to `tests/golden/overlay/bold-title-ownership.png`; same for `series-parts` with `part_number=7`.
- A 40-word title with `max_lines = 3` renders at `min_size_px` with an ellipsis and logs `overlay.title_truncated`.
- `check` on a 1920×1080 JPEG of 1.5 MB returns `ok=True`; on 1919×1080 returns `ok=True` (±1 px); on 1918×1080 returns `ok=False` with `aspect` in `violations`; on 1280×720 PNG `ok=True`; on 1024×576 `ok=False` with `width`; on a 3 MB JPEG `ok=False` with `size` unless `max_bytes=52_428_800`; on a CMYK JPEG `ok=False` with `color`.
- `render_final` on a raw image that encodes to more than 2,097,152 bytes at quality 90 lowers quality until it fits and returns a report with `ok=True`.
- `thumbforge thumb show <run>` in Windows Terminal draws a block-character preview (manual check, spike S10); with `--json` it prints only JSON.

## Test plan

- Unit: `fit_to` size matrix; `resolve_font` fallback order with `tmp_path` config dir; `check` matrix above using synthetic images from Pillow; `render_final` quality loop with a noise image.
- Golden (`-m golden`): overlay snapshots for the three builtin layouts; regenerated only via `uv run pytest -m golden --update-golden` and reviewed in the PR diff.
- Contract / integration: none.

## Open spikes

- **S3** Antigravity output size/format — decides whether upscaling from 1376×768 is the normal path for the default 1920×1080 output.
- **S10** terminal image preview with `rich-pixels` in Windows Terminal — if unusable, `preview` prints the asset paths and the `thumb export` hint instead.
