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

## Fonts

`font` in `[title]` and `[part]` names a TrueType file without its extension. Thumbforge looks for `NAME.ttf` in the `fonts` folder of your per-user configuration directory first, then among the bundled fonts, and uses Inter Bold with a `fonts.fallback` warning when it finds neither.

| Bundled font              | Draws                                    | Licence           |
| ------------------------- | ---------------------------------------- | ----------------- |
| `Inter-Bold`              | Latin letters, digits and punctuation    | SIL Open Font 1.1 |
| `NotoSansDevanagari-Bold` | Devanagari (Hindi, Marathi, Nepali, ...) | SIL Open Font 1.1 |

Latin and Devanagari titles are supported out of the box, alone or mixed in one title (`Bhag 01 | भाग 01`). The title is drawn with the layout's font; the characters that font cannot draw and Noto Sans Devanagari Bold can are drawn with it, shaped so conjuncts, half forms and vowel signs come out right. `NotoSansDevanagari-Bold` is that fallback and is used automatically: do not set it as the layout font, because a font that is picked directly draws character by character, without shaping.

Other scripts (Arabic, Chinese, Japanese, Korean, emoji) are not supported yet. Thumbforge logs one `fonts.uncovered` warning with the number of characters involved, never the title, and the title shows empty "missing glyph" boxes for them. The fallback applies to the title only; the Part badge text is drawn with its own font alone.

## Built-in templates, and your own

Three templates are built in and stored by `thumbforge db init`:

| Template       | Look                                                                                 |
| -------------- | ------------------------------------------------------------------------------------ |
| `bold-title`   | Large upper-case title bottom-left over a punchy, high-contrast image; no badge.     |
| `minimal`      | Small, quiet title bottom-left over a restrained image with a lot of empty space.    |
| `series-parts` | Title bottom-centre with a "PART N" badge top-right: one look across a whole series. |

Templates live in the database as numbered versions: importing a changed template creates a new version and never alters the old one, so earlier runs stay reproducible. `thumbforge template list` shows every version, `template show NAME` prints one, `template new NAME` copies one to editable files next to your configuration file, and `template import PATH` stores the files as a new version. A run takes `--template NAME` (the latest version) or `--template NAME@VERSION`. The default is `[general] default_template`. See [Write a custom template](../how-to/write-a-custom-template.md).

## Going deeper

- [ADR 0006](../../adr/0006-jinja2-prompts-toml-layouts.md) — why Jinja prompts and TOML layouts.
- [ADR 0008](../../adr/0008-deterministic-text-overlay.md) — why the text is drawn by Thumbforge.
- [ADR 0019](../../adr/0019-complex-script-titles.md) — how Hindi titles are shaped and why that stays deterministic.
- [Phase 4 spec](../../specs/phase-4-templates.md#interfaces) — the full layout schema.
