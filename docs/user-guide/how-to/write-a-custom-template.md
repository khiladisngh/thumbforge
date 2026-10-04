# Write a custom template

Create your own template — a prompt and a layout — starting from a built-in one, adjust where the title and badge sit and what the provider is asked to paint, and import it so runs can use it. Every import of a changed template becomes a new version, so earlier runs stay reproducible. See [Templates](../concepts/templates.md).

## Start from a built-in

```
thumbforge template list
thumbforge template new my-series --from series-parts
```

`template list` shows every stored version and whether it is built in. `template new` copies the stored template (`minimal` unless you pass `--from NAME` or `--from NAME@VERSION`) to `my-series.toml` and `my-series.j2` in the `templates` folder next to your configuration file (`thumbforge config path` shows where that is) and prints both paths. `template show NAME` prints a stored template's prompt and layout if you want to read one first.

You can also write both files by hand; [Getting started](../getting-started.md#7-preview-a-templates-prompt) has a complete example.

## Edit and check

Edit the two files: the layout (`.toml`) holds the canvas, the title box and the badge; the prompt (`.j2`) holds what the provider is asked to paint. Then check the layout:

```
thumbforge template validate <config-dir>/templates/my-series.toml
```

`validate` lists every layout error at once, and checks the sibling `.j2` for Jinja syntax.

## Fonts

`font` in `[title]` and `[part]` is the name of a TrueType file without its extension. To use your own, copy `MyFont.ttf` into the `fonts` folder of your per-user configuration directory (the folder that holds the default `config.toml`; create `fonts` if it is missing) and set `font = "MyFont"`. A font of that name there wins over a bundled one, and a name Thumbforge cannot find falls back to Inter Bold with a `fonts.fallback` warning.

Two fonts are bundled, both under the SIL Open Font License 1.1: `Inter-Bold` for Latin and `NotoSansDevanagari-Bold` for Devanagari. Latin and Devanagari titles are supported out of the box: whatever your layout's font cannot draw, Hindi for instance, is drawn with Noto Sans Devanagari Bold and shaped correctly, so a bilingual title such as `Bhag 01 | भाग 01` renders in one line. Keep `font = "Inter-Bold"` (or your own Latin font) for the title; `NotoSansDevanagari-Bold` is the fallback and is not meant to be picked directly. Other scripts still fall back with a `fonts.uncovered` warning and may show empty boxes. See [Templates](../concepts/templates.md#fonts).

## Import, preview and use

```
thumbforge template import <config-dir>/templates/my-series
thumbforge template render my-series --video <video-id> --var key=value
thumbforge thumb generate <video-id> --template my-series --var key=value
```

`template import` takes the layout file, its stem, or a folder holding one pair, and stores the pair as `my-series@1`. `render` prints the prompt for a stored video and calls no provider; `--part N` overrides the part number it uses. Both `render` and `thumb generate` read the template from the database, so a custom template is not used until it has been imported: `--template my-series` before that exits `3`.

## Versions

Importing the same content again changes nothing (it reports `already stored`). Importing changed content stores `my-series@2` and leaves `@1` as it was, so `--template my-series@1` still reproduces an earlier run exactly, while `--template my-series` always means the latest version. After editing the files, import again before you render or generate.
