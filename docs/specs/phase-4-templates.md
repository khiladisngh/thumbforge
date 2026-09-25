# Phase 4 — Templates

Status: Proposed
ROADMAP tasks: P4.1, P4.2, P4.3, P4.4
ADRs: `docs/adr/0006-jinja2-prompts-toml-layouts.md`, `docs/adr/0008-deterministic-text-overlay.md`, `docs/adr/0018-shared-models-live-in-core.md`

## Scope

A template pairs a Jinja2 **prompt** (what the provider is asked to paint) with a TOML **layout spec** (how Pillow overlays text in Phase 5). Templates are versioned, immutable rows in the `template` table; builtins ship in the package.

- **P4.1** `core/layout.py` — Pydantic `LayoutSpec`; `templates/schema.py` — TOML loading into it. The model lives in `core` because `imaging` (Phase 5) and `core.services` (Phase 6) consume it, and neither may import `templates`.
- **P4.2** `templates/render.py` — Jinja2 environment (`StrictUndefined`, `autoescape=False`), render context.
- **P4.3** `templates/builtin/{bold-title,minimal,series-parts}.{toml,j2}`.
- **P4.4** `templates/loader.py`, `cli/template.py`, versioning in `TemplateRepository`.

## Non-goals

- Rendering pixels — Phase 5 consumes the layout spec; Phase 4 only validates it.
- Calling a provider — `template render` prints prompt text only.
- Template marketplace / remote import.

## Interfaces

### Layout spec (TOML → `LayoutSpec`)

```toml
[template]
name = "bold-title"
description = "Large title bottom-left, optional Part badge top-right"

[canvas]
width = 1920
height = 1080
safe_margin_px = 64

[title]
enabled = true
font = "Inter-Bold"          # resolved by imaging/fonts.py; bundled OFL fallback
max_lines = 3
size_px = 120
min_size_px = 72             # shrink-to-fit floor
color = "#FFFFFF"
stroke_px = 6
stroke_color = "#000000"
anchor = "bottom-left"       # one of 9 anchors
box = { x = 64, y = 640, w = 1400, h = 376 }
case = "upper"               # none | upper | title

[part]
enabled = true               # decision D6
format = "PART {n}"          # also {label} when playlist_item.part_label is set
font = "Inter-Bold"
size_px = 72
anchor = "top-right"
badge = { fill = "#E53935", padding_px = 24, radius_px = 16 }

[negative_space]
hint = "leave the lower-left third uncluttered"   # injected into the prompt via {{ negative_space }}
```

```python
class LayoutSpec(BaseModel, frozen=True, extra="forbid"):
    template: TemplateMeta
    canvas: Canvas
    title: TitleBlock
    part: PartBlock
    negative_space: NegativeSpace


class Template(BaseModel, frozen=True):
    name: str
    version: int
    prompt_template: str
    layout: LayoutSpec
    spec_hash: str  # sha256(prompt_template + canonical_json(layout_spec))
    is_builtin: bool
```

### Prompt rendering

```python
class TemplateRenderer:
    def render(self, template: Template, ctx: RenderContext) -> str
```

`RenderContext(video: VideoMeta, playlist: PlaylistMeta | None, part_number: int | None, part_label: str | None, channel: ChannelMeta | None, vars: dict[str, str], negative_space: str, width: int, height: int)`. Jinja2 `Environment(undefined=StrictUndefined, autoescape=False, trim_blocks=True, lstrip_blocks=True)`; a missing variable is a `TemplateError` (exit `2`) naming the variable and template. `--var key=value` populates `vars`.

Builtin prompts state the size and the negative-space hint and must not ask the model to paint text (ADR 0008).

### Commands (`PLAN.md` §5.2)

| Command                                   | Key flags                             | Output                                                         | Exit    |
| ----------------------------------------- | ------------------------------------- | -------------------------------------------------------------- | ------- |
| `thumbforge template list`                |                                       | table `name, version, builtin`                                 | 0       |
| `thumbforge template show NAME[@VERSION]` |                                       | prompt + layout spec                                           | 0, 3    |
| `thumbforge template new NAME`            | `--from NAME`                         | writes `<config_dir>/templates/NAME.toml` + `.j2` from builtin | 0, 2    |
| `thumbforge template validate PATH`       |                                       | schema + Jinja parse check                                     | 0, 2    |
| `thumbforge template import PATH`         |                                       | stores as new version                                          | 0, 2    |
| `thumbforge template render NAME`         | `--video <id>`, `--part 3`, `--var …` | prints rendered prompt only; no provider call                  | 0, 2, 3 |

## Behaviour

1. On first use, `loader.sync_builtins()` inserts each builtin template at `version = 1` with `is_builtin = 1`; a changed builtin in a new package release inserts `version + 1` (old versions stay for reproducibility).
2. `template import PATH` reads `PATH.toml` + sibling `PATH.j2` (or a directory holding both), validates, computes `spec_hash`; if a row with the same `name` and `spec_hash` exists, prints it and exits `0` without inserting; otherwise inserts `max(version) + 1`.
3. `NAME` without `@VERSION` resolves to the highest version; `NAME@2` resolves exactly; unknown → exit `3`.
4. `template validate` reports every schema error at once (Pydantic error list) and Jinja syntax errors with line numbers; exit `2` on any.
5. `template render bold-title --video dQw4w9WgXcQ --part 3` prints the prompt to stdout; with `--json` prints `{"template": "bold-title@1", "prompt": "..."}`.
6. `template new NAME --from minimal` copies both builtin files to `<config_dir>/templates/`; refuses to overwrite (exit `2`).

## Acceptance criteria

- `thumbforge template list` after a fresh `db init` shows `bold-title 1 yes`, `minimal 1 yes`, `series-parts 1 yes`.
- `thumbforge template render series-parts --video <fixture video> --part 7` prints a prompt containing the video title, `Part 7` wording and the negative-space hint, and no `{{`.
- `thumbforge template render bold-title --video <id> --var mood=` with a template referencing `{{ vars.tone }}` exits `2` with `template_error: undefined variable 'vars.tone' in bold-title@1`.
- Importing the same TOML/J2 pair twice yields one row; changing one character in the `.j2` yields `version 2` with a different `spec_hash`.
- `thumbforge template validate tests/fixtures/templates/bad-anchor.toml` exits `2` listing `title.anchor` as invalid.
- `template show bold-title@1` output equals `template show bold-title` while only version 1 exists.

## Test plan

- Unit: `LayoutSpec` validation matrix (anchors, colours, box within canvas, `min_size_px <= size_px`); renderer with `StrictUndefined`; `spec_hash` stability across key order (canonical JSON); loader versioning on in-memory DB; CLI via `CliRunner` with the Phase 2 fixture video.
- Contract / integration: none.
- Golden: prompt snapshots for the three builtins against the fixture video (`tests/templates/golden/*.txt`, marker `golden`).

## Open spikes

- None. Decision **D6** (title only vs title + Part badge; bundled Inter) sets the builtin `[part] enabled` default and the font names used in the builtin specs.
