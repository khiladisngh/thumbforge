# Getting started

This page installs Thumbforge and walks through a first run using only the commands that exist today. Generating images is not part of it yet; see [What lands in v0.1.0](index.md#what-lands-in-v010).

## Requirements

- [uv](https://docs.astral.sh/uv/), the Python package and tool manager. Thumbforge needs Python 3.14; uv downloads it for you if it is not installed.
- Network access for `thumbforge fetch`, which reads public YouTube metadata. No YouTube API key is needed.

## Install

Thumbforge installs straight from its GitHub repository:

```
uv tool install git+https://github.com/khiladisngh/thumbforge
thumbforge --version
```

`uv tool install` puts the `thumbforge` command on your `PATH` in its own isolated environment. `thumbforge --version` prints the installed version, for example `thumbforge 0.0.0`.

## Where Thumbforge keeps its files

```
thumbforge config path
```

prints every path Thumbforge reads and writes: the configuration file, the data directory (database and images), the state directory and the log file. They follow your operating system's conventions for per-user configuration and data.

Every command accepts two global options, written **before** the command name, that point it somewhere else. They are useful for trying Thumbforge without touching your real setup:

```
thumbforge --config ./scratch/config.toml --data-dir ./scratch/data config path
```

Logs still go to the state directory shown by `config path`.

## First run

### 1. Write a configuration file

```
thumbforge config init
```

writes a commented `config.toml` listing every setting with its default, and prints its path. `thumbforge config show` prints the effective configuration (defaults, then the file, then `THUMBFORGE_*` environment variables); `thumbforge config set` changes a key and validates the result before writing.

### 2. Create the database

```
$ thumbforge db init
initialized database at <data-dir>/thumbforge.sqlite3 (0001)
```

`db init` creates the SQLite database in your data directory (`<data-dir>` above) and prints its path. `thumbforge db status` reports the schema revision, file size and journal mode.

### 3. List the image providers

```
thumbforge provider list
thumbforge provider check fake
```

`provider list` prints one row per installed provider with its version, authentication state and capabilities. The `fake` provider is always there: it works offline and needs no key, which makes it the safe choice for experiments. `provider check KEY` runs that provider's health checks. See [Providers](concepts/providers.md).

### 4. Fetch a playlist

```
$ thumbforge fetch "https://www.youtube.com/playlist?list=<playlist-id>"
╭───────────────────────── Playlist ────────────────────────╮
│ <playlist title>   <playlist-id>   <n> videos   <channel> │
╰───────────────────────────────────────────────────────────╯
┏━━━━━┳━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
┃ #   ┃ Part ┃ Video ID   ┃ Title   ┃
┡━━━━━╇━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
│ 1   │ 1    │ <video-id> │ Video 1 │
│ 2   │ 2    │ <video-id> │ Video 2 │
│ 3   │ 3    │ <video-id> │ Video 3 │
│ …   │ …    │ …          │ …       │
└─────┴──────┴────────────┴─────────┘
Stored 1 channel, 1 playlist, <n> videos.
```

The output above is abbreviated: rows are cut, and titles and ids are replaced with placeholders.

`fetch` accepts a video, playlist or channel URL, or a bare id. It stores the channel, the playlist and every video in the database and prints the playlist with each video's position, part number, id and title. A playlist fetched in the last 24 hours is shown from the database without going back to YouTube; add `--refresh` to re-read it. Part numbers you set with `playlist renumber` survive a refresh.

### 5. Browse what you fetched

```
thumbforge playlist list
thumbforge playlist show <playlist-id> --videos
thumbforge video list
thumbforge video show <video-id>
```

`playlist show` and `video show` accept a YouTube id or a URL; `--videos` adds the ordered list of videos with their part numbers.

### 6. Number the parts

Each video starts with a part number equal to its position in the playlist. When the playlist opens with a trailer, leave it unnumbered so the first real episode is Part 1:

```
$ thumbforge playlist renumber <playlist-id> --start 1 --skip-ids <trailer-video-id>
┏━━━━━┳━━━━━┳━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
┃ #   ┃ Was ┃ Now ┃ Video ID   ┃ Title   ┃
┡━━━━━╇━━━━━╇━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
│ 1   │ 1   │ —   │ <video-id> │ Trailer │
│ 2   │ 2   │ 1   │ <video-id> │ Video 1 │
│ 3   │ 3   │ 2   │ <video-id> │ Video 2 │
│ …   │ …   │ …   │ …          │ …       │
└─────┴─────┴─────┴────────────┴─────────┘
```

Abbreviated as above. The `—` marks a video left without a part number.

Skipped videos are not counted, so the remaining parts stay consecutive. `playlist show <playlist-id> --videos` shows the result. See [Series and playlists](concepts/series-and-playlists.md).

### 7. Preview a template's prompt

A template is two files: a TOML layout and a Jinja prompt. Until template management lands in v0.1.0, Thumbforge reads templates from a `templates/` folder next to your configuration file (whose path is the `config` line of `thumbforge config path`). Create `templates/my-series.toml` there:

```toml
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

and `templates/my-series.j2` beside it:

```jinja
Background art for "{{ video.title }}", {{ width }}x{{ height }}.
{% if part_number %}
Series instalment {{ part_number }}.
{% endif %}
Composition: {{ negative_space }}.
Mood: {{ vars.mood }}.
```

Then check the layout and print the prompt for one of the videos you fetched:

```
thumbforge template validate <config-dir>/templates/my-series.toml
thumbforge template render my-series --video <video-id> --var mood=bright
```

`validate` reports every schema error at once. `render` fills in the video's title, its part number and the layout's negative-space hint, and calls no provider. Leaving out a variable the prompt uses is an error, not a blank:

```
$ thumbforge template render my-series --video <video-id>
template: undefined variable 'vars.mood' in my-series
```

That command exits with code `2`. See [Templates](concepts/templates.md).

## Exit codes

Every command exits `0` on success. The full table (usage errors, not found, provider errors, compliance failures, partial batches, interruption) is in [`PLAN.md` §5.1](https://github.com/khiladisngh/thumbforge/blob/main/PLAN.md#51-exit-codes).

## Next steps

- Read the concepts: [Hero](concepts/hero.md), [Series and playlists](concepts/series-and-playlists.md), [Templates](concepts/templates.md), [Providers](concepts/providers.md).
- `thumbforge --help` and `thumbforge <command> --help` list every option.
