# Open questions

Two lists: **Spikes** (facts to verify by running something; each has a copy-pasteable command and states what changes depending on the answer) and **Decisions** (preferences only you can settle). Spike results go to `docs/spikes/<topic>.md`; close the item here with a link.

## Spikes

### S1 — Does headless `agy -p` expose an image-generation tool?

- Verify (PowerShell or bash):
    ```
    agy -p "reply with the single word ok" --output-format stream-json | jq -r 'select(.event=="init") | .init.tools[]'
    ```
    Look for a tool named like `generate_image`. Record the exact name.
- Changes: the tool name goes into `antigravity_wrapper.j2`, the `permissions.allow` rule (S5) and ADR 0013. If no image tool is listed, `AntigravityProvider` cannot work headlessly: keep ADR 0013 _Proposed_, block P3.4, and add an `external-file` provider (user supplies an image path) so Phases 5–7 proceed.

### S2 — Output path control

- Verify:
    ```
    mkdir C:\tmp\agyspike
    agy -p "Use your image generation tool once to create a picture of a red circle on white. Save it to exactly C:\tmp\agyspike\test.jpg. Do not run any shell commands." --add-dir C:\tmp\agyspike --output-format json --dangerously-skip-permissions --print-timeout 10m
    dir C:\tmp\agyspike; dir $HOME\.gemini\antigravity-cli\scratch
    ```
- Changes: if the file lands in scratch instead, the adapter must copy from scratch (`ProviderOutputMissingError` hint) or the prompt wording must change.

### S3 — Output format and size

- Verify: repeat S2 with prompts "1920 x 1080 pixels, 16:9 widescreen" and "16:9 widescreen"; then `python -c "from PIL import Image; im=Image.open(r'C:\tmp\agyspike\test.jpg'); print(im.format, im.size)"`.
- Changes: `ProviderCapabilities.output_formats`, `supports_aspect_ratio`, and whether `imaging/fit.py` must upscale from 1376×768 (affects D2).

### S4 — Reference images

- Verify: place `ref.png` in `C:\tmp\agyspike\refs`, add `--add-dir C:\tmp\agyspike\refs`, mention the absolute path in the prompt, run with `--output-format stream-json`, and inspect `select(.event=="step_update") | .step_update.tool_info.parameters` for the reference.
- Changes: `supports_reference_image`; if references are ignored, batch consistency must rely on prompt-only style anchors and ADR 0008 gains weight.

### S5 — Permissions

- Verify: run S2 **without** `--dangerously-skip-permissions`; capture stderr. Then add `{"permissions":{"allow":["<tool name from S1>"]}}` to `~/.gemini/antigravity-cli/settings.json` and re-run.
- Changes: D4 default; `provider check antigravity` behaviour.

### S6 — Exit codes and status matrix

- Verify: (a) throwaway profile without login → expect `authentication required`; (b) `--model does-not-exist --output-format json; echo $LASTEXITCODE`; (c) `--print-timeout 1s`.
- Changes: error-mapping table in PLAN.md §4.3 and the fake-`agy` unit tests in P3.4.

### S7 — Rate limits / quota

- Verify: 5 sequential generations, then 2 in parallel; record any error text; run `agy -p /usage`.
- Changes: `max_concurrency`, backoff parameters, `--max-images` default.

### S8 — Cost / usage fields

- Verify: compare `usage` in the JSON envelope for a text-only run vs an image run; look for any credit field.
- Changes: `Cost` model fields and P8.3 cost report.

### S9 — graphify on Windows with uv

- Verify:
    ```
    uv tool install graphifyy
    graphify install --project --platform agents
    graphify .
    graphify hook install; graphify hook status
    ```
    Time the build; confirm `graphify-out/{graph.html,GRAPH_REPORT.md,graph.json}` and `.agents/skills/`.
- Changes: regeneration mode (post-commit hook vs CI vs manual) recorded in `AGENTS.md`; fallback is manual `uv tool run --from graphifyy graphify update .`.

### S10 — Terminal image preview

- Verify: `uv run --with rich-pixels python -c "from rich_pixels import Pixels; from rich.console import Console; Console().print(Pixels.from_image_path('test.jpg'))"` in Windows Terminal.
- Changes: ADR 0002 preview approach; P5.4 fallback.

### S11 — yt-dlp flat playlist fields

- Verify: `uv run --with yt-dlp python -c "import yt_dlp,json; print(json.dumps(yt_dlp.YoutubeDL({'extract_flat':'in_playlist','quiet':True}).extract_info('<playlist url>', download=False)['entries'][0], indent=1))"`; confirm `playlist_index`, `channel_id`, `title`, `id`, `duration` are present.
- Changes: `VideoMeta` fields and the P2.2 fixture recorder.

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

| ID  | Decision                                                                                                                                                                                                                                                                  |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D1  | Tool name **`thumbforge`** (package, command, repo `khiladisngh/thumbforge`).                                                                                                                                                                                             |
| D2  | Default output size **1920×1080**; `imaging/fit.py` upscales from the provider's native 16:9 when smaller (S3 confirms the native size).                                                                                                                                  |
| D3  | Type checker **pyright**, strict on `src/`.                                                                                                                                                                                                                               |
| D4  | Antigravity runs with **`--dangerously-skip-permissions` by default** (`providers.antigravity.skip_permissions = true`); a `permissions.allow` rule is the documented alternative once S1 names the tool.                                                                 |
| D5  | GitHub **`khiladisngh/thumbforge`**, CODEOWNERS `@khiladisngh`, **MIT** license, PyPI trusted publishing (`release.yml`, environment `pypi`; publisher to be configured on PyPI before the first tag). Docs on GitHub Pages at https://khiladisngh.github.io/thumbforge/. |
| D6  | Overlay default: `bold-title` = title only; `series-parts` = title + "Part N" badge. Bundled font **Inter (OFL)**.                                                                                                                                                        |
| D7  | YouTube Data API source **kept** as the Phase 8 optional extra `thumbforge[api]`.                                                                                                                                                                                         |
