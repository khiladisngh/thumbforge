# Getting started

This page installs Thumbforge and walks through a first run: set up, fetch a video, generate thumbnail candidates with the offline `fake` provider, then pick one and export it. The sample output comes from real runs; ids, timestamps and paths on your machine will differ.

## Requirements

- [uv](https://docs.astral.sh/uv/), the Python package and tool manager. Thumbforge needs Python 3.14; uv downloads it for you if it is not installed.
- Network access for `thumbforge fetch`, which reads public YouTube metadata. No YouTube API key is needed.

## Install

Once Thumbforge is published to PyPI, installing it is one command:

```
uv tool install thumbforge
```

!!! note "Not on PyPI yet"

    Thumbforge is not published to PyPI yet, so `uv tool install thumbforge` does not work today; the first release (roadmap task P8.5) publishes it. Until then install from GitHub:

    ```
    uv tool install git+https://github.com/khiladisngh/thumbforge
    ```

    or from a checkout of the repository:

    ```
    git clone https://github.com/khiladisngh/thumbforge
    cd thumbforge
    uv tool install .
    ```

`uv tool install` puts the `thumbforge` command on your `PATH` in its own isolated environment. Check that it resolves:

```
$ thumbforge --version
thumbforge 0.1.0
```


If your shell says `thumbforge` is not found, the directory printed by `uv tool dir --bin` is not on your `PATH`. Run `uv tool update-shell` and open a new terminal. To remove Thumbforge again, run `uv tool uninstall thumbforge`.

## Where Thumbforge keeps its files

```
thumbforge config path
```

prints every path Thumbforge reads and writes: the configuration file, the data directory (database and images), the state directory and the log file. They follow your operating system's conventions for per-user configuration and data.

To try Thumbforge without touching your real setup, point it at a scratch location. Every command accepts two global options, written **before** the command name:

```
thumbforge --config ./scratch/config.toml --data-dir ./scratch/data config path
```

Or set the same two things for a whole terminal session with environment variables:

=== "Linux / macOS"

    ```
    export THUMBFORGE_CONFIG="$PWD/scratch/config.toml"
    export THUMBFORGE_GENERAL__DATA_DIR="$PWD/scratch/data"
    ```

=== "Windows (PowerShell)"

    ```
    $env:THUMBFORGE_CONFIG = "$PWD\scratch\config.toml"
    $env:THUMBFORGE_GENERAL__DATA_DIR = "$PWD\scratch\data"
    ```

=== "Windows (cmd)"

    ```
    set THUMBFORGE_CONFIG=%CD%\scratch\config.toml
    set THUMBFORGE_GENERAL__DATA_DIR=%CD%\scratch\data
    ```

Logs still go to the state directory shown by `config path`. Progress lines such as `run started` also print to your terminal (stderr); they are left out of the samples below, and `--quiet` hides them.

## First run

### 1. Write a configuration file

```
$ thumbforge config init
wrote <config-file>
```

`config init` writes a commented `config.toml` listing every setting with its default and prints its path. `thumbforge config show` prints the effective configuration (defaults, then the file, then `THUMBFORGE_*` environment variables); `thumbforge config set` changes a key and validates the result before writing. The defaults already select the `fake` provider and the `bold-title` template, which is all this page needs.

### 2. Create the database

```
$ thumbforge db init
initialized database at <data-dir>/thumbforge.sqlite3 (0001)
```

`db init` creates the SQLite database in your data directory, stores the built-in templates in it, and prints its path. `thumbforge db status` reports the schema revision, file size and journal mode.

### 3. Check the provider

```
$ thumbforge provider list
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Key         ┃ Name            ┃ Version ┃ Auth    ┃ Capabilities                                 ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ antigravity │ Antigravity CLI │ unknown │ missing │ negative, aspect · jpeg · x2                 │
│ fake        │ Fake            │ 0.1.0   │ ok      │ reference, seed, negative, aspect · png · x8 │
└─────────────┴─────────────────┴─────────┴─────────┴──────────────────────────────────────────────┘
$ thumbforge provider check fake
fake · healthy
```

`provider list` prints one row per installed provider with its version, authentication state and capabilities. The `fake` provider is always there: it works offline and needs no key, so the rest of this page uses it. `provider check KEY` runs that provider's health checks and prints a table of results below the summary line. See [Providers](concepts/providers.md) for the real ones.

### 4. Fetch a video

```
$ thumbforge fetch "https://www.youtube.com/watch?v=jNQXAC9IVRw"
╭─────────── Video ───────────╮
│ Me at the zoo   jNQXAC9IVRw │
╰─────────────────────────────╯
Stored 1 channel, 0 playlist, 1 videos.
```

`fetch` accepts a video, playlist or channel URL, or a bare id, and stores the metadata in the database. `jNQXAC9IVRw` is a short public video used as an example; any public video works. yt-dlp may print a warning about a missing JavaScript runtime; the fetch still succeeds.

### 5. Generate candidates

```
$ thumbforge thumb generate jNQXAC9IVRw --n 3
Run <run>
Kind      hero
Status    completed
Template  bold-title@1
Provider  fake@0.1.0:<fingerprint>
Video     jNQXAC9IVRw
Started   <timestamp>
Finished  <timestamp>
┏━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ # ┃ Status    ┃ Size      ┃ Compliant ┃ Key          ┃ Asset / Error ┃
┡━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ 1 │ completed │ 1920x1080 │ ✔         │ <key>        │ <asset>       │
│ 2 │ completed │ 1920x1080 │ ✔         │ <key>        │ <asset>       │
│ 3 │ completed │ 1920x1080 │ ✔         │ <key>        │ <asset>       │
└───┴───────────┴───────────┴───────────┴──────────────┴───────────────┘
Copy images out with: thumbforge thumb export <run|iteration> --to PATH
Pick one with: thumbforge thumb pick <run> <ordinal>
```

This makes three candidates (the default is four) from the `bold-title` template and prints one row per candidate. `Compliant` is whether the final image passes YouTube's thumbnail rules. On a terminal that can draw images you also get a preview of each candidate; elsewhere you get a table of file paths. The `fake` provider returns the same image for the same prompt and seed, so the candidates are placeholders, not artwork. Copy the run id (the `<run>` in the commands below) from the first line.

### 6. Pick one and export it

```
$ thumbforge thumb pick <run> 2
Picked #2 of run <run> (iteration <iteration-id>)
Export it with: thumbforge thumb export <run> --to PATH
$ thumbforge thumb show <run>
$ thumbforge thumb export <run> --to out
Wrote out/jNQXAC9IVRw-1.jpg
Wrote out/jNQXAC9IVRw-2.jpg
Wrote out/jNQXAC9IVRw-3.jpg
```

`thumb pick` marks candidate 2 as the one to keep; picking another one moves the mark. `thumb show` prints the run again with a grid of the finals, and the picked one carries a `★`. `thumb export` copies every completed candidate into the folder `out` (created if needed) as `<video-id>-<number>.jpg`; on Windows the paths print with backslashes. [Pick and refine](how-to/pick-and-refine.md) covers `--raw`, exporting one iteration and refining the pick with `thumb iterate`.

### 7. Preview a template's prompt

A template is two files: a TOML layout and a Jinja prompt. `bold-title`, `minimal` and `series-parts` are built in (`thumbforge template list`). To write your own, create `my-series.toml` in the `templates` folder next to your configuration file (the folder `thumbforge template new` writes to), with this content:

```toml title="templates/my-series.toml"
[template]
name = "my-series"
description = "Large title bottom-left, Part badge top-right"

[canvas]
width = 1920
height = 1080
safe_margin_px = 64

[title]
enabled = true
font = "Inter-Bold"
max_lines = 3
size_px = 120
min_size_px = 72
color = "#FFFFFF"
stroke_px = 6
stroke_color = "#000000"
anchor = "bottom-left"
box = { x = 64, y = 640, w = 1400, h = 376 }
case = "upper"

[part]
enabled = true
format = "PART {n}"
font = "Inter-Bold"
size_px = 72
anchor = "top-right"
badge = { fill = "#E53935", padding_px = 24, radius_px = 16 }

[negative_space]
hint = "leave the lower-left third uncluttered"
```

and `my-series.j2` beside it:

```jinja title="templates/my-series.j2"
Background art for "{{ video.title }}", {{ width }}x{{ height }}.
{% if part_number %}
Series instalment {{ part_number }}.
{% endif %}
Composition: {{ negative_space }}.
Mood: {{ vars.mood }}.
```

Then check the layout, store it in the database, and print the prompt it produces for the video you fetched:

```
$ thumbforge template validate <config-dir>/templates/my-series.toml
ok <config-dir>/templates/my-series.toml (my-series)
$ thumbforge template import <config-dir>/templates/my-series
imported my-series@1 (<spec-hash>)
$ thumbforge template render my-series --video jNQXAC9IVRw --var mood=bright
Background art for "Me at the zoo", 1920x1080.
Composition: leave the lower-left third uncluttered.
Mood: bright.
```

`<config-dir>` is the folder holding the `config` file from `thumbforge config path`. `validate` reports every schema error at once. `import` stores the template as a new immutable version. `render` fills in the video's title, its part number (this video is in no playlist, so there is none) and the layout's negative-space hint, and calls no provider. Leaving out a variable the prompt uses is an error, not a blank:

```
$ thumbforge template render my-series --video jNQXAC9IVRw
template: undefined variable 'vars.mood' in my-series@1
```

That command exits with code `2`. To use the template for a run, pass `--template my-series` to `thumb generate`. See [Templates](concepts/templates.md).

## Work with a playlist

The same flow works for a whole series. Fetch a playlist, browse what was stored, and give the videos their part numbers:

```
thumbforge fetch "https://www.youtube.com/playlist?list=<playlist-id>"
thumbforge playlist list
thumbforge playlist show <playlist-id> --videos
thumbforge video list
thumbforge video show <video-id>
```

`fetch` stores the channel, the playlist and every video, and prints the playlist with each video's position, part number, id and title. A playlist fetched in the last 24 hours is shown from the database without going back to YouTube; add `--refresh` to re-read it. `playlist show` and `video show` accept a YouTube id or a URL; `--videos` adds the ordered list of videos with their part numbers.

Each video starts with a part number equal to its position in the playlist. When the playlist opens with a trailer, leave it unnumbered so the first real episode is Part 1:

```
thumbforge playlist renumber <playlist-id> --start 1 --skip-ids <trailer-video-id>
```

The table it prints shows each video's old and new part number; a `—` marks a video left without one. Skipped videos are not counted, so the remaining parts stay consecutive, and part numbers you set survive a later `--refresh`. See [Series and playlists](concepts/series-and-playlists.md).

## Exit codes

Every command exits `0` on success. The full table (usage errors, not found, provider errors, compliance failures, partial batches, interruption) is in [`PLAN.md` §5.1](https://github.com/khiladisngh/thumbforge/blob/main/PLAN.md#51-exit-codes).

## Next steps

- Read the concepts: [Hero](concepts/hero.md), [Series and playlists](concepts/series-and-playlists.md), [Templates](concepts/templates.md), [Providers](concepts/providers.md).
- [Generate a hero](how-to/generate-a-hero.md) and [Pick and refine](how-to/pick-and-refine.md) go deeper on the commands used above.
- [Shell completion](how-to/shell-completion.md) adds Tab completion for commands and options in bash, zsh, fish and PowerShell.
- `thumbforge --help` and `thumbforge <command> --help` list every option.
