# ADR 0006: Jinja2 prompt templates and TOML layout specs

## Status

`Superseded by [ADR 0018](0018-shared-models-live-in-core.md)` — 2026-09-25

Only the placement of the layout-spec model (`templates/schema.py`) was revised; it now lives in `core/layout.py`. Every other decision below stands. See ADR 0018.

## Context

A template must express two things: the text prompt sent to an image provider (varies per video: title, part number, channel, user variables) and the layout of the deterministic overlay (font, position, colours, badge). Templates must be versioned so a resumed batch renders the same prompt, and `thumbforge template render` must show the exact prompt without calling a provider.

## Decision

- A template is a pair of files with the same stem: `NAME.j2` (prompt) and `NAME.toml` (layout spec). Builtin templates live in `src/thumbforge/templates/builtin/`; user templates in `<config_dir>/templates/`.
- **Jinja2** renders prompts with `Environment(undefined=StrictUndefined, autoescape=False, trim_blocks=True, lstrip_blocks=True)`. Context variables: `video` (`VideoMeta`), `playlist` (`PlaylistMeta | None`), `part` (`int | None`), `channel`, and `vars` from `--var key=value`. A missing variable raises `TemplateError` (exit `2`).
- **TOML** layout specs are validated by a Pydantic model in `templates/schema.py` (title box, font, size range, alignment, colours, badge style, negative-space hint passed to the prompt).
- Templates are stored immutably in the `template` table with `UNIQUE(name, version)`; `spec_hash = sha256(prompt_template + canonical_json(layout_spec))` feeds the idempotency key (ADR 0012). Editing a template creates `version + 1`; `NAME@VERSION` selects a version explicitly, bare `NAME` means latest.
- Builtin set: `bold-title`, `minimal`, `series-parts`.
- Commands: `template list|show|new|validate|import|render` (`PLAN.md` §5.2).

## Consequences

- Prompt text is fully reproducible from `(template version, video, part, vars)`, which makes the idempotency key meaningful.
- `StrictUndefined` turns typos into immediate, testable errors instead of silently empty prompts.
- Layout and prompt are decoupled, so the same layout can be reused with provider-specific prompts.
- Autoescape off means templates must not be rendered into HTML; prompts are plain text only.

## Alternatives considered

- **Python f-strings / `str.format`** — rejected: no conditionals or loops (needed for optional "Part N" and reference hints), no strict-undefined behaviour.
- **YAML for layout specs** — rejected: ADR 0003 already standardises on TOML; `tomllib` is stdlib.
- **Storing templates only as files (no DB rows)** — rejected: a resumed run must find the exact prompt template even after the user edited the file; immutable versions in the DB give that guarantee.
- **Mako** — rejected: smaller ecosystem and no equivalent of `StrictUndefined`.
