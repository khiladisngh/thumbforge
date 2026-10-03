# Phase 4 — Templates

Status: Implemented (P4.1–P4.4)
ROADMAP tasks: P4.1, P4.2, P4.3, P4.4
ADRs: `docs/adr/0006-jinja2-prompts-toml-layouts.md`, `docs/adr/0008-deterministic-text-overlay.md`, `docs/adr/0018-shared-models-live-in-core.md`

## Scope

A template pairs a Jinja2 **prompt** (what the provider is asked to paint) with a TOML **layout spec** (how Pillow overlays text in Phase 5). Templates are versioned, immutable rows in the `template` table; builtins ship in the package.

- **P4.1** `core/layout.py` — Pydantic `LayoutSpec`; `templates/schema.py` — TOML loading into it. The model lives in `core` because `imaging` (Phase 5) and `core.services` (Phase 6) consume it, and neither may import `templates`.
- **P4.2** `templates/render.py` — Jinja2 environment (`StrictUndefined`, `autoescape=False`), render context.
- **P4.3** `templates/builtin/{bold-title,minimal,series-parts}.{toml,j2}` (package data, in the wheel) and `templates/builtins.py` — `BUILTIN_NAMES` and `builtin_files(name) -> (toml_path, j2_path)`; an unknown name is `NotFoundError`. No loading into the database (P4.4).
- **P4.4** `templates/loader.py` — `TemplateRef`/`parse_ref`, `resolve`, `store_template`, `import_template`, `sync_builtins`, `write_copy`, and the `TemplateStore` Protocol it needs from persistence (`templates` may not import `storage`); `TemplateRepository` in `storage/repositories.py` satisfies it structurally and `cli` wires the two. The `Template` value object and `spec_hash` live in `core/layout.py`, `canonical_json` in `core/json.py` (ADR 0018). `cli/template.py` gains `list`, `show`, `new`, `import`; `render` resolves through the database; `db init` loads the built-ins. No migration: the `template` table already has every column and `UNIQUE(name, version)`.

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

The TOML above illustrates the schema; it is not a shipped file. The shipped values live in `src/thumbforge/templates/builtin/*.toml`:

- `bold-title` — 160 px (floor 96) upper-case title bottom-left in a 1728×440 box, 8 px black stroke, Part badge disabled; the prompt asks for a punchy, high-contrast hero shot with the lower half kept clear.
- `minimal` — 96 px (floor 64) title, case unchanged, bottom-left in a 1200×216 box at `x = 96, y = 800`, 4 px stroke, Part badge disabled; the prompt asks for one restrained subject with calm space in the lower-left corner.
- `series-parts` — 128 px (floor 72) title-case title bottom-centre, `PART {n}` badge top-right on `#FFD400`; the prompt names `Part {{ part_number }}` of the playlist and fixes one look across the series, with the bottom third and top-right corner kept clear.

```python
class LayoutSpec(BaseModel, frozen=True, extra="forbid"):
    template: TemplateMeta
    canvas: Canvas
    title: TitleBlock
    part: PartBlock
    negative_space: NegativeSpace


class Template(BaseModel, frozen=True, extra="forbid"):  # core/layout.py
    name: str
    version: int  # >= 1
    prompt_template: str
    layout: LayoutSpec
    spec_hash: str  # sha256(prompt_template + canonical_json(layout_spec))
    is_builtin: bool
```

`canonical_json` is `json.dumps(sort_keys=True, separators=(",", ":"), ensure_ascii=False)` over `LayoutSpec.model_dump(mode="json")`, so the hash is independent of TOML key and table order, and a default spelled out hashes the same as one left out. The same string is stored in `template.layout_spec_json`. Prompt files are read in text mode, which turns CRLF into LF, so a `.j2` checked out on Windows hashes the same as on Linux.

A template reference is `NAME` or `NAME@VERSION`, `VERSION` a positive integer without leading zeros. `NAME` is non-empty and contains no `/`, `\` or `@`; the same rule applies to the `[template] name` of an imported template and to the `NAME` of `template new`.

### Prompt rendering

```python
def render_prompt(prompt_template: str, ctx: RenderContext, *, name: str) -> str
```

`RenderContext` is a frozen dataclass: `RenderContext(video: VideoMeta, playlist: PlaylistMeta | None, part_number: int | None, part_label: str | None, channel: ChannelMeta | None, vars: dict[str, str], negative_space: str, width: int, height: int)`. Jinja2 `Environment(undefined=StrictUndefined, autoescape=False, trim_blocks=True, lstrip_blocks=True)`; a missing variable is a `TemplateError` (exit `2`) naming the variable and template. `--var key=value` populates `vars`; a value may be empty, a pair without `=` exits `2`. The error names the dotted path and the resolved `NAME@VERSION`, e.g. `undefined variable 'vars.tone' in bold-title@1`; a Jinja syntax error is also a `TemplateError` and names the template and line. `check_syntax(prompt_template, *, name)` runs the same compile step without rendering, for `validate` and `import`.

Builtin prompts state the size and the negative-space hint and must not ask the model to paint text (ADR 0008).

### Commands (`PLAN.md` §5.2)

| Command                                     | Key flags                                   | Output                                                                                        | Exit    |
| ------------------------------------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------- | ------- |
| `thumbforge template list`                  |                                             | table `name, version, builtin`, one row per stored version; `--json` `{"templates", "count"}` | 0       |
| `thumbforge template show NAME[@VERSION]`   |                                             | prompt + layout spec (TOML); `--json` adds the layout as JSON                                 | 0, 2, 3 |
| `thumbforge template new NAME`              | `--from NAME[@VERSION]` (default `minimal`) | writes `<config_dir>/templates/NAME.toml` + `NAME.j2` copied from the stored template         | 0, 2, 3 |
| `thumbforge template validate PATH`         |                                             | schema check, plus Jinja parse check of a sibling `.j2` when present                          | 0, 2    |
| `thumbforge template import PATH`           |                                             | stores as new version, or prints the stored row with the same content                         | 0, 2    |
| `thumbforge template render NAME[@VERSION]` | `--video <id>`, `--part 3`, `--var …`       | prints rendered prompt only; no provider call                                                 | 0, 2, 3 |

## Behaviour

1. `db init` calls `loader.sync_builtins()` after migrating, also when the schema is already at head. Each builtin missing from the database is inserted at `version = 1` with `is_builtin = 1`; a changed builtin in a new package release (different `spec_hash`) inserts `max(version) + 1` and old versions stay for reproducibility. Unchanged builtins insert nothing, so re-running `db init` is a no-op; its output is unchanged. No other command syncs.
2. `template import PATH` takes `X.toml` (with a sibling `X.j2`), the stem `X`, or a directory holding exactly one `.toml` and one `.j2` of the same stem. It validates the layout and the Jinja syntax of the prompt, reporting every error of both at once (exit `2`), takes the name from `[template] name`, and computes `spec_hash`; if a row with the same `name` and `spec_hash` exists, prints it and exits `0` without inserting; otherwise inserts `max(version) + 1` with `is_builtin = 0`.
3. `NAME` without `@VERSION` resolves to the highest version; `NAME@2` resolves exactly; an unknown name or version exits `3`, the hint listing the stored versions. A malformed reference (`name@x`, `name@0`, empty name, a path) exits `2`.
4. `template validate` reports every schema error at once (Pydantic error list) and, when `PATH` has a sibling `.j2`, its Jinja syntax errors with line numbers; exit `2` on any.
5. `template render bold-title --video dQw4w9WgXcQ --part 3` resolves the template through the database (rule 3) and prints the prompt to stdout; with `--json` prints `{"template": "bold-title@1", "prompt": "..."}`, naming the resolved version. A video in exactly one playlist supplies `playlist`, `part_number` and `part_label`; `--part` overrides the number.
6. `template new NAME --from EXISTING` resolves `EXISTING` (default `minimal`) through the database (rule 3) and writes `<config_dir>/templates/NAME.toml` + `NAME.j2`, with `[template] name` rewritten to `NAME`. The TOML is regenerated from the stored layout, so every default is spelled out and comments are not kept. It refuses to overwrite either file (exit `2`, nothing written); an invalid `NAME` exits `2`. The copy passes `template validate` and `template import`.

## Acceptance criteria

- `thumbforge template list` after a fresh `db init` shows `bold-title 1 yes`, `minimal 1 yes`, `series-parts 1 yes`.
- `thumbforge template render series-parts --video <fixture video> --part 7` prints a prompt containing the video title, `Part 7` wording and the negative-space hint, and no `{{`.
- `thumbforge template render bold-title --video <id> --var mood=` with a template referencing `{{ vars.tone }}` exits `2` with `template: undefined variable 'vars.tone' in bold-title@1`.
- Importing the same TOML/J2 pair twice yields one row; changing one character in the `.j2` yields `version 2` with a different `spec_hash`.
- `thumbforge template validate tests/fixtures/templates/bad-anchor.toml` exits `2` listing `title.anchor` as invalid.
- `template show bold-title@1` output equals `template show bold-title` while only version 1 exists.

## Test plan

- Unit: `LayoutSpec` validation matrix (anchors, colours, box within canvas, `min_size_px <= size_px`); renderer with `StrictUndefined`; `spec_hash` stability across key order (canonical JSON) and CRLF/LF prompts; `dump_layout` → `load_layout` round trip; loader versioning and `sync_builtins` on a migrated SQLite file; CLI via `CliRunner` with the Phase 2 fixture video.
- Contract / integration: none.
- Golden: prompt snapshots for the three builtins against the fixture video (`tests/templates/golden/*.txt`, marker `golden`).

## Open spikes

- None. Decision **D6** (title only vs title + Part badge; bundled Inter) sets the builtin `[part] enabled` default and the font names used in the builtin specs.
