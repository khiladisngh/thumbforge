# Spike results — Antigravity CLI (`agy`)

Run 2026-09-20 against **`agy 1.2.6`** on Windows 11 (ADR 0013 was written against 1.2.3).
Every command below was executed against the live CLI. Eight images were generated in
total, which cost 1% of the five-hour quota.

Two conventions apply to the captured output:

- **`[…]` marks text this report omitted**, always because it was long and repetitive (a
  full model list, a full generated prompt). Nothing omitted changes a conclusion, and no
  `…` below was emitted by `agy` itself.
- **`<USER>` replaces the local Windows profile name** in paths, so the report is portable
  and does not publish machine-specific paths. Directory _structure_ is unchanged.

**Headline: `generate_image` exists headlessly, so `AntigravityProvider` is viable — but
three of ADR 0013's design points are wrong and one of them would have made every timeout a
permanent failure.** See [Consequences](#consequences-for-adr-0013).

## S1 — Does headless `agy -p` expose an image-generation tool? — **yes, `generate_image`**

```bash
agy -p "reply with the single word ok" --output-format stream-json
```

The `init` event lists **57 tools**, including:

```
generate_image
```

Others relevant to the adapter's "do not use other tools" instruction: `run_command`,
`write_to_file`, `view_file`, `search_web`, `open_browser_url`, `invoke_subagent`,
`ask_permission`, `list_permissions`.

`init` keys are `cwd`, `permission_mode`, `tools` — no version or model field.

Result envelope for the text-only run:

```json
{
    "status": "SUCCESS",
    "response": "ok\n",
    "usage": {
        "input_tokens": 18914,
        "output_tokens": 332,
        "thinking_tokens": 267,
        "cache_read_tokens": 16268,
        "total_tokens": 19246
    }
}
```

## S2 — Output path control — **not controllable; output lands in the brain directory**

```bash
agy -p "Use your image generation tool once to create a picture of a red circle on white. \
Save it to exactly <spikedir>/test.jpg. Do not run any shell commands." \
  --add-dir <spikedir> --output-format json --dangerously-skip-permissions --print-timeout 10m
```

Exit `0`, `status: SUCCESS`, and the agent said so itself:

```
The `generate_image` tool was invoked to generate the image.

The tool does not accept a custom output path parameter and automatically saved the
generated image to the agent's brain directory:
`C:\Users\<USER>\.gemini\antigravity-cli\brain\7e1fba60-8239-4676-8d44-019aabf43362\red_circle_1789896899337.jpg`

As instructed, no shell commands were executed, so the image could not be copied […]
```

The requested `--add-dir` target stayed **empty**, and `scratch/` was **empty** too — the
third-party report that images land in `~/.gemini/antigravity-cli/scratch/` is wrong for
1.2.6.

The path is nonetheless **deterministic**, because the envelope returns the
`conversation_id` that names the directory:

```
envelope conversation_id: 7e1fba60-8239-4676-8d44-019aabf43362
path derived from conversation_id exists: True
```

Layout of `brain/<conversation_id>/`:

```
.system_generated/   .tempmediaStorage/   .user_uploaded/   scratch/
red_circle_1789896899337.jpg
```

So the file is `brain/<conversation_id>/<ImageName>_<epoch_ms>.jpg`. The adapter must glob
that directory rather than name its own path.

## S3 — Output format and size — **JPEG only; size is influenced by wording, never specified**

`generate_image`'s parameters, captured from `stream-json`
(`.step_update.tool_info.parameters`):

```json
{
    "ImageName": "blue_triangle",
    "Prompt": "A clean, solid blue equilateral triangle centered on a pure solid white background, minimal, crisp lines, 1920x1080 widescreen presentation."
}
```

**Two parameters only.** There is no path, size, aspect-ratio, seed, format or reference
parameter. `tool_info.output` is `null`, so the produced path is not in the structured
stream either.

Sizes measured across all seven generations:

| Prompt wording                          | Result        | Ratio |
| --------------------------------------- | ------------- | ----- |
| `"1920 x 1080 pixels, 16:9 widescreen"` | `1376 × 768`  | 1.792 |
| `"16:9 widescreen"`                     | `1376 × 768`  | 1.792 |
| `"16:9 widescreen"` (×3 more)           | `1376 × 768`  | 1.792 |
| no ratio mentioned                      | `1024 × 1024` | 1.000 |
| no ratio mentioned (style-match prompt) | `1264 × 848`  | 1.491 |

```
distinct sizes: [(1024, 1024), (1264, 848), (1376, 768)]
distinct formats: ['JPEG']
images generated: 7
```

Conclusions:

- **Format is always JPEG.** `output_formats = {"jpeg"}` is confirmed.
- **The words "16:9 widescreen" reliably produce 1376 × 768** — 5 for 5. Adding the exact
  pixel dimensions changed nothing, so the wrapper prompt only needs the ratio words.
- **Omitting the ratio gives an unpredictable size** (1024 × 1024 and 1264 × 848 both
  observed), so the wrapper must always state it.
- `1376 / 768 = 1.792`, not `1.778`, so the result is slightly wider than true 16:9 and
  needs a small crop regardless of target.
- **1376 × 768 is smaller than the configured 1920 × 1080 default** (`OutputSettings`), so
  reaching the default requires a **1.40× upscale**. Decision **D2** already chose
  1920 × 1080 "upscaling from the provider's native 16:9 when smaller" _pending this
  measurement_, so this confirms D2 rather than reopening it.

## S4 — Reference images — **prose only; the bytes never reach the image model**

A reference was written to `refs/ref.png` (yellow background, purple ellipse, black border)
and named by absolute path in the prompt, with `--add-dir refs`.

Tool calls, in order:

```
view_file          {"AbsolutePath": ".../refs/ref.png"}
generate_image     {"ImageName": "purple_yellow_cat",
                    "Prompt": "A minimalist 2D flat graphic vector illustration of a cat,
                     matching the exact visual style, flat solid aesthetic, and strict
                     3-color palette of the reference image. The cat is rendered in the
                     exact same vivid purpl[…]"}
```

The agent **reads** the image and then **describes** it into the prompt. Since
`generate_image` takes no image parameter (S3), the reference bytes cannot reach the image
model at all.

The translation is nonetheless effective for palette. The reference background was
`(250, 240, 20)`; the generated image's dominant colour:

```
purple_yellow_cat_1789897119499.jpg JPEG (1264, 848)
  dominant colours: [((246, 233, 14), 520), ((246, 232, 13), 289), ((247, 233, 14), 281)]
```

So `supports_reference_image` is **False** in the sense that matters — there is no
image-to-image conditioning, and two runs from the same reference will not be pixel-
consistent. Batch consistency must come from prompt-only style anchors, which is exactly
the case **ADR 0008** ("AI paints the background; Pillow renders the text") was made for;
this measurement strengthens it.

## S5 — Permissions — **`generate_image` needs no grant**

The S2 prompt was re-run **without** `--dangerously-skip-permissions` and with no
`permissions.allow` entry in `settings.json` (which contained only `statusLine` and
`trustedWorkspaces`):

```
exit=0
stderr: (empty)
status: SUCCESS | error: None
response: 'I have generated the image of an orange star on a white background in 16:9 widescreen format.'
```

No soft-deny notice, no permission prompt. **`skip_permissions` should default to `false`**
(decision **D4**), and no `permissions.allow` rule is needed.

`trustedWorkspaces` was a plausible confound: `settings.json` listed
`trustedWorkspaces: ["C:\\Users\\<USER>"]`, and the brain directory that receives the image
sits _inside_ that path. So the entry was removed (backed up first) and the run repeated
with no permission flag at all:

```
trustedWorkspaces removed; now: {"statusLine": {[…]}}

$ agy -p "Use your image generation tool once to create a picture of a teal diamond on \
white, 16:9 widescreen. Do not run any shell commands." --output-format json --print-timeout 5m
exit=0
stderr: []
status: SUCCESS | error: None
response: 'The teal diamond on a white background (16:9 widescreen) has been generated for you above.'
```

`settings.json` was then restored and verified. The result therefore holds **without** a
trust entry and **without** the flag: `generate_image` is not permission-gated, so decision
D4 is genuinely superseded rather than superseded-if-trusted.

## S6 — Exit codes and status matrix — **one dangerous case**

### (b) Unknown model → exit 1, clean `ERROR` envelope

```
$ agy -p "say ok" --model does-not-exist --output-format json ; echo $?
{"conversation_id":"","status":"ERROR","response":"",
 "error":"invalid model selection (--model \"does-not-exist\" --effort \"\"): model
  does-not-exist is not recognized as a known model or custom model in settings\n
  Available models:\n  Gemini 3.8 Flash (High)\n  […all 14 listed below]"}
exit=1
```

Available models (useful for `provider_profile`):

```
Gemini 3.8 Flash (High|Medium|Low)   Gemini 3.7 Flash (High|Medium|Low)
Gemini 3.6 Flash (High|Medium|Low)   Gemini 3.1 Pro (High|Low)
Claude Sonnet 4.6 (Thinking)         Claude Opus 4.6 (Thinking)
GPT-OSS 120B (Medium)
```

### (c) `--print-timeout 1s` → **exit 0 and `SUCCESS`, with no image**

```
$ agy -p "Use your image generation tool once to create a picture of a purple hexagon, \
  16:9 widescreen." --output-format json --print-timeout 1s ; echo $?
{"conversation_id":"48518c63-[…]","status":"SUCCESS","response":"","duration_seconds":0,
 "num_turns":1,"usage":{"input_tokens":0,"output_tokens":0,"thinking_tokens":0,
 "cache_read_tokens":0,"total_tokens":0}}
exit=0
stderr: [agy] print timeout after 1s with turn in progress; returning partial output
```

**This is the finding that matters most.** A timeout is reported as success. An adapter that
trusts `exit == 0 and status == "SUCCESS"` sees a successful run that produced no file, and
ADR 0013's table maps "SUCCESS but output file missing" to the **non-retryable**
`ProviderOutputMissingError`. A batch would therefore abandon every item that merely ran
long. The distinguishing signals are `response == ""`, `duration_seconds == 0`, all-zero
`usage`, and the stderr notice.

### (a) Unauthenticated — **not verified**

Overriding `USERPROFILE` and `HOME` to an empty directory did **not** isolate the profile;
the run still succeeded with cached credentials, so they live elsewhere (`%APPDATA%` or
`%LOCALAPPDATA%`). Verifying this properly means signing the developer out of Antigravity,
which was not done. ADR 0013's claim that an unauthenticated run reports
`authentication required` remains **documentation-only**, and the `ProviderAuthError`
mapping is therefore written defensively rather than from observation.

## S7 — Rate limits / quota — **generous; 2 concurrent is fine**

Five image generations ran sequentially during S2–S5 with no throttling, error text or
slowdown.

Two more ran **concurrently**:

```
s7p1: status SUCCESS | duration 17.41s
s7p2: status SUCCESS | duration 16.42s
```

Both succeeded, and each was _faster_ than the sequential runs (32–40 s), so serialisation
was costing wall-clock time rather than protecting a limit.

`agy -p "/usage"` returns a parsable tab-separated report:

```
Gemini Models	Weekly Limit Remaining	71%	2026-09-23T06:44:47Z
Gemini Models	Five Hour Limit Remaining	99%	2026-09-20T10:10:48Z
Claude and GPT models	Weekly Limit Remaining	100%	2026-09-27T09:41:36Z
Claude and GPT models	Five Hour Limit Remaining	100%	2026-09-20T14:41:36Z
```

After all seven generations the five-hour figure moved `99% → 98%`, and the weekly figure
did not move from `71%`. So a 12-video playlist is nowhere near a limit, and
`max_concurrency` can safely be raised above 1.

### Correction, measured during P3.4: the limit does exist, and it hides inside `SUCCESS`

"Generous" is not "absent". A later contract run on the same account exhausted the **image
model's** quota — a separate budget from the `/usage` figures above, which track the chat
models. The shape is the important part, because it is indistinguishable from success at the
envelope level:

```
status  : SUCCESS
turns   : 1
duration: 7.47
usage   : {'input_tokens': 20068, 'output_tokens': 511, 'thinking_tokens': 345,
           'cache_read_tokens': 16280, 'total_tokens': 20579}
response: The image generation request was sent with the specified prompt and 16:9 aspect
          ratio, but the service returned a quota exhaustion error:
          > **429 Too Many Requests**: `RESOURCE_EXHAUSTED` - You have exhausted your
          capacity on the image model (`gemini-3.1-flash-image`). Quota resets in
          approximately 2 hours and 20 minutes.
```

Exit code `0`, `status: SUCCESS`, a full turn of real token usage, and **no image**. The 429
appears nowhere machine-readable — not in `error`, not in stderr, not in the status — only as
prose the agent wrote. The brain directory is created and contains only the usual empty
`.system_generated/`, `.user_uploaded/` and `scratch/` subdirectories.

So S6c is not the only "SUCCESS means failure" case, and the adapter cannot treat "SUCCESS
with no image" as permanent. `AntigravityProvider` scans the response for `RESOURCE_EXHAUSTED`
/ `429` / quota / rate-limit markers **when and only when no image was produced**, and raises
a retryable `ProviderTransientError`. Two hours of unavailability is a wait, not a defect, and
the permanent classification would abandon the batch item while blaming the user's setup.

## S8 — Cost / usage fields — **tokens only, no credit or currency**

| Run             | input | output | thinking | cache_read | total |
| --------------- | ----: | -----: | -------: | ---------: | ----: |
| text-only (S1)  | 18914 |    332 |      267 |      16268 | 19246 |
| image (S2)      | 62753 |   4953 |     4459 |      85548 | 67706 |
| timed out (S6c) |     0 |      0 |        0 |          0 |     0 |

`usage` has exactly five keys and **no credit, price or currency field**. `total_tokens`
equals `input + output`; `cache_read_tokens` is reported separately and excluded from the
total. An image run costs roughly 3.5× the tokens of a trivial text run.

So `Cost` can record tokens and `duration_seconds` only. A monetary figure is not available
from the CLI, which constrains the **P8.3** cost report to tokens plus the `/usage`
percentages.

## Also observed: `agy` injects the developer's global plugins

The S4 run opened, unprompted:

```
view_file  {"AbsolutePath": "C:\\Users\\<USER>\\.gemini\\config\\plugins\\superpowers\\skills\\using-superpowers\\SKILL.md"}
```

`~/.gemini/config/plugins/` contains `gemini-api`, `ponytail` and `superpowers`. Every
headless run therefore inherits whatever instructions the developer has installed globally,
which is a **reproducibility hazard for a provider**: the same prompt can behave differently
on another machine, and generation output is not a pure function of thumbforge's inputs.
`provider check antigravity` should report the installed plugin set so a surprising result
is diagnosable.

## Consequences for ADR 0013

Viability is confirmed, and the ADR can move off `Proposed`. Four design points must change
first; the first is a correctness bug, the rest are improvements.

1. **Timeouts must be retryable.** Add: `SUCCESS` with an empty `response`, zero `usage` and
   no output file → `ProviderTimeoutError` (**retryable**), checked _before_ the
   `ProviderOutputMissingError` row. As written, every long generation would permanently
   fail its batch item.
2. **Drop the output path from the wrapper prompt.** `generate_image` has no path parameter,
   so instructing it is noise that the agent then apologises for. The adapter passes
   `ImageName` intent via the prompt and locates the result at
   `brain/<conversation_id>/*.jpg`, copying it into the asset store. The
   `ProviderOutputMissingError` hint must name the **brain** directory, not `scratch/`.
3. **`skip_permissions` defaults to `false`** (D4). The dangerous flag is not required.
4. **`max_concurrency` may exceed 1** — 2 measured as safe and faster. Capabilities become
   `reference=False`, `seed=False`, `aspect=True` (influence only, exact size never
   guaranteed), `formats={"jpeg"}`, `max_batch=1`.

**Decision D2 is confirmed, not reopened.** It already specified 1920 × 1080 with
`imaging/fit.py` "upscaling from the provider's native 16:9 when smaller", pending exactly
this measurement. The native size is 1376 × 768, so Phase 5 upscales 1.40× and crops 1.792
to 1.778. Dropping the default to 1280 × 720 would avoid the upscale and remains available
to the maintainer, but it is not an open question and does not block P3.4.
