# Templates

A **template** decides both what the image provider is asked to paint and how Thumbforge lays text over the result. It is a pair of files with the same name:

- a **prompt** (`NAME.j2`) — the request sent to the image provider, written as a [Jinja](https://jinja.palletsprojects.com/) template so it can include the video's title, its part number and your own variables;
- a **layout** (`NAME.toml`) — the canvas size, where the title goes and how big it is, the "Part N" badge, colours and safe margins.

## The prompt

The prompt describes the artwork, not the text: the layout's negative-space hint tells the model which area to keep clear for the title, and Thumbforge draws the text there afterwards. A prompt can use:

| Variable                    | Value                                                     |
| --------------------------- | --------------------------------------------------------- |
| `video`                     | the video's stored metadata, e.g. `{{ video.title }}`     |
| `playlist`, `channel`       | the playlist and channel the video belongs to, if known   |
| `part_number`, `part_label` | the video's part number and label in its playlist, if any |
| `vars`                      | your own values, passed as `--var key=value`              |
| `negative_space`            | the layout's hint for the area to keep clear              |
| `width`, `height`           | the canvas size from the layout                           |

A variable the prompt uses but nobody supplied is an error, not an empty string, so a typo cannot silently produce a vague prompt.

## The layout

The layout is TOML with five sections: `[template]` (name and description), `[canvas]` (size and safe margin), `[title]` (font, size range, colour, outline, position, box, letter case), `[part]` (the badge's format, font, position and colours) and `[negative_space]` (the hint passed to the prompt). [Getting started](../getting-started.md#7-preview-a-templates-prompt) has a complete example.

`thumbforge template validate PATH` checks a layout and lists every problem at once. `thumbforge template render NAME --video <id>` prints the finished prompt for one of your videos without calling a provider, which is the quickest way to see what a template asks for.

!!! note "Coming in v0.1.0"

    Built-in templates (`bold-title`, `minimal`, `series-parts`) and template management (`thumbforge template list|show|new|import`) are planned in roadmap tasks P4.3 and P4.4 and defined in the [Phase 4 spec](../../specs/phase-4-templates.md#behaviour). Templates will then be stored as numbered versions: importing a changed template creates a new version and never alters the old one, so earlier runs stay reproducible. Until then, templates are read from the `templates/` folder next to your configuration file. See [Write a custom template](../how-to/write-a-custom-template.md).

## Going deeper

- [ADR 0006](../../adr/0006-jinja2-prompts-toml-layouts.md) — why Jinja prompts and TOML layouts.
- [ADR 0008](../../adr/0008-deterministic-text-overlay.md) — why the text is drawn by Thumbforge.
- [Phase 4 spec](../../specs/phase-4-templates.md#interfaces) — the full layout schema.
