# Open questions

Two lists: **Spikes** (facts to verify by running something; each has a copy-pasteable command and states what changes depending on the answer) and **Decisions** (preferences only you can settle). Spike results go to `docs/spikes/<topic>.md`; close the item here with a link.

## Spikes

### S1 — Does headless `agy -p` expose an image-generation tool? — **closed**, see `docs/spikes/antigravity.md`

- Verify: `agy -p "reply with the single word ok" --output-format stream-json | jq -r 'select(.event=="init") | .init.tools[]'`
- Result: **yes — `generate_image`**, one of 57 tools listed in the `init` event (`agy 1.2.6`). `AntigravityProvider` is viable, so ADR 0013 moves to Accepted and P3.4 is unblocked.

### S2 — Output path control — **closed**, see `docs/spikes/antigravity.md`

- Verify: prompt the tool to save to an exact absolute path under `--add-dir`, then inspect that directory and `~/.gemini/antigravity-cli/scratch`.
- Result: **not controllable.** `generate_image` takes no path parameter; the image lands in `~/.gemini/antigravity-cli/brain/<conversation_id>/<ImageName>_<epoch_ms>.jpg`. The `--add-dir` target and `scratch/` both stayed empty, so the third-party "scratch" report is wrong for 1.2.6. The path is still deterministic because the envelope returns `conversation_id`, so the adapter globs that directory and copies into the asset store.

### S3 — Output format and size — **closed**, see `docs/spikes/antigravity.md`

- Verify: generate with and without aspect-ratio wording, then read `Image.open(...).format`/`.size`.
- Result: **always JPEG.** The words "16:9 widescreen" reliably give **1376×768** (5 of 5); stating exact pixels changes nothing; omitting the ratio gives an unpredictable size (1024×1024 and 1264×848 both seen), so the wrapper must always state the ratio. `1376/768 = 1.792`, slightly wider than true 16:9, so a small crop is always needed. Confirms the native size D2 anticipated: reaching the 1920×1080 default needs a 1.40× upscale in `imaging/fit.py`.

### S4 — Reference images — **closed**, see `docs/spikes/antigravity.md`

- Verify: name a reference image's absolute path in the prompt with `--add-dir`, then inspect `.step_update.tool_info.parameters`.
- Result: **prose only.** The agent `view_file`s the reference and _describes_ it into the `Prompt`; `generate_image` has no image parameter, so the bytes never reach the image model. Palette transfer is nonetheless good (reference `(250,240,20)` → generated dominant `(246,233,14)`), but there is no image-to-image conditioning and two runs will not be pixel-consistent. `supports_reference_image = False`; batch consistency rests on prompt-only style anchors, which strengthens ADR 0008.

### S5 — Permissions — **closed**, see `docs/spikes/antigravity.md`

- Verify: run an image generation **without** `--dangerously-skip-permissions` and with no `permissions.allow` entry.
- Result: **no grant needed.** Exit 0, `SUCCESS`, empty stderr, no soft-deny notice. Supersedes **D4**: `providers.antigravity.skip_permissions` defaults to `false` and no `permissions.allow` rule is required.

### S6 — Exit codes and status matrix — **closed** (except 6a), see `docs/spikes/antigravity.md`

- Verify: (a) unauthenticated profile; (b) `--model does-not-exist`; (c) `--print-timeout 1s`.
- Result: (b) exit `1` with a clean `ERROR` envelope naming the available models. (c) **exit `0` with `status: SUCCESS`, an empty `response`, zero `usage` and a stderr notice** — a timeout reports success, so it must map to `ProviderTimeoutError` (retryable) _before_ the "SUCCESS but file missing" row, or every long generation permanently fails its batch item. (a) **not verified**: overriding `USERPROFILE`/`HOME` did not isolate the cached credentials, and confirming it would mean signing the maintainer out of Antigravity. The `authentication required` behaviour stays documentation-only and `ProviderAuthError` is mapped defensively.

### S7 — Rate limits / quota — **closed**, see `docs/spikes/antigravity.md`

- Verify: five sequential generations, then two in parallel; then `agy -p "/usage"`.
- Result: **no throttling.** Five sequential and two concurrent runs all succeeded; the concurrent pair finished in ~17 s each versus 32–40 s sequentially, so forcing `max_concurrency = 1` costs wall-clock time without protecting a limit. Seven generations moved the five-hour quota `99% → 98%` and left the weekly figure unchanged at `71%`. `/usage` returns a parsable tab-separated report with reset timestamps.

### S8 — Cost / usage fields — **closed**, see `docs/spikes/antigravity.md`

- Verify: compare `usage` for a text-only run against an image run; look for a credit field.
- Result: **tokens only.** Five keys, no credit/price/currency. `total_tokens = input + output`; `cache_read_tokens` is excluded from the total. An image run costs ~3.5× a trivial text run (67,706 vs 19,246 total tokens). `Cost` can record tokens and `duration_seconds` only, so the P8.3 report is limited to tokens plus the `/usage` percentages.

### S9 — graphify on Windows with uv — **closed**, see `docs/spikes/graphify.md`

- Verify: `uv tool install graphifyy && graphify extract . --code-only && graphify cluster-only . --no-label`
- Result: working seamlessly under Windows with uv; generated `graphify-out/` committed to repo.

### S10 — terminal image preview with `rich-pixels` in Windows Terminal

- Verify (run in Windows Terminal, the primary development terminal):
    ```
    uv run --with rich --with rich-pixels --with pillow python -c "from PIL import Image; from rich.console import Console; from rich_pixels import Pixels; c=Console(); Image.new('RGB',(1920,1080),(200,40,40)).save('preview.png'); w=max(c.width//2-2,20); c.print(Pixels.from_image_path('preview.png',resize=(w,w*9//16)))"
    ```
    Replace the synthetic fill with a real thumbnail once one exists. The tile is sized to
    half the terminal width, which is what one cell of the `--columns 2` grid gets. Confirm
    the block-character output is legible — that the title and overall composition are
    recognisable, not that it is pixel-accurate. Note that `rich.columns.Columns` did **not**
    lay two `Pixels` tiles side by side in a smoke test, so P5.4 must verify the real grid
    layout rather than assume it.
- Changes: the `_render.preview()` helper and P5.4. If unusable, `preview` prints the asset paths plus the `thumb export` hint and `thumb show` falls back to a table (ADR 0002).

### S11 — yt-dlp flat playlist fields under `extract_flat` — **closed**, see `docs/spikes/ytdlp.md`

- Verify: `uv run --with yt-dlp python -c "import yt_dlp,json; print(sorted(yt_dlp.YoutubeDL({'extract_flat':'in_playlist','quiet':True}).extract_info('<playlist url>', download=False)['entries'][0]))"`
- Result: `id`, `title`, `duration`, `channel_id`, `channel`, `url`, `thumbnails`, `view_count` are always present (183/183 entries). **`playlist_index` is absent** — this spike assumed it would be there — so `PlaylistItemMeta.position` comes from enumeration order. `description` is likewise **absent** from every entry, while `timestamp`, `availability` and `live_status` are present but always `None` — so a flat extract cannot fill `description` or `published_at`; those need a per-video full extract.

### S12 — Python 3.15 GA timing

- Verify: python.org release page; GA expected October 2026.
- Changes: add `3.15` to the CI matrix after GA; `requires-python` stays `>=3.14`.

### S13 — prettier via pre-commit on Windows — **closed**, see `docs/spikes/tooling.md`

- Verify: `pre-commit try-repo https://github.com/pre-commit/mirrors-prettier prettier --files README.md`; confirm Node bootstraps without a repo `package.json`; pick the pinned `rev`.
- Changes: if the mirror is archived or fails, fall back to `mdformat` (`uv run --with mdformat mdformat`) for Markdown only and drop YAML/JSON formatting.

### S14 — zensical build of the ADR/spec tree — **closed**, see `docs/spikes/tooling.md`

- Verify: `uv add --dev zensical && uv run zensical build`; confirm mermaid fences render (check whether a `pymdownx.superfences` custom fence is required in `zensical.toml`); record the exact version.
- Changes: `zensical.toml` contents in `docs/specs/phase-0-infra.md`.

## Decisions

All decided 2026-09-19 by the maintainer, taking the recommended option in each case.

| ID  | Decision                                                                                                                                                                                                                                                                                                                                                  |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D1  | Tool name **`thumbforge`** (package, command, repo `khiladisngh/thumbforge`).                                                                                                                                                                                                                                                                             |
| D2  | Default output size **1920×1080**; `imaging/fit.py` upscales from the provider's native 16:9 when smaller. S3 measured that native size as **1376×768**, so the upscale is 1.40× and a small crop is needed (1.792 vs 1.778).                                                                                                                             |
| D3  | Type checker **pyright**, strict on `src/`.                                                                                                                                                                                                                                                                                                               |
| D4  | ~~Antigravity runs with `--dangerously-skip-permissions` by default~~ — **superseded by spike S5**, which measured `generate_image` succeeding with neither the flag nor a `permissions.allow` rule. `providers.antigravity.skip_permissions` now defaults to **`false`**. The decision's premise (that the image tool is permission-gated) did not hold. |
| D5  | GitHub **`khiladisngh/thumbforge`**, CODEOWNERS `@khiladisngh`, **MIT** license, PyPI trusted publishing (`release.yml`, environment `pypi`; publisher to be configured on PyPI before the first tag). Docs on GitHub Pages at https://khiladisngh.github.io/thumbforge/.                                                                                 |
| D6  | Overlay default: `bold-title` = title only; `series-parts` = title + "Part N" badge. Bundled font **Inter (OFL)**.                                                                                                                                                                                                                                        |
| D7  | YouTube Data API source **kept** as the Phase 8 optional extra `thumbforge[api]`.                                                                                                                                                                                                                                                                         |
