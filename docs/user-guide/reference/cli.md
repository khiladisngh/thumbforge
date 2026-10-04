# CLI reference

The built-in help is authoritative for every option, and it cannot drift from the code:

```
thumbforge --help
thumbforge <command> --help
thumbforge <command> <subcommand> --help
```

This page is the map: which command does what, and what the exit codes mean.

## Global options

These go **before** the command name.

| Option                                      | Meaning                                                 |
| ------------------------------------------- | ------------------------------------------------------- |
| `--config PATH`                             | Use this `config.toml` (also `THUMBFORGE_CONFIG`).      |
| `--data-dir PATH`                           | Use this data directory for the database and images.    |
| `--json`                                    | Print one JSON document instead of the tables.          |
| `-v`, `-vv`                                 | Log at INFO, or at DEBUG, to stderr.                    |
| `--quiet`                                   | Log only errors.                                        |
| `--no-color`                                | Turn colour off.                                        |
| `--version`                                 | Print the version and exit.                             |
| `--install-completion`, `--show-completion` | Set up, or print, Tab completion for the current shell. |

## Commands

| Command                                       | What it does                                                                                                                                                |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fetch URL [--source ytdlp\|api] [--refresh]` | Fetch a video, playlist or channel and store its metadata. Use the `/playlist?list=` link for a playlist.                                                   |
| `video list\|show`                            | List stored videos, or show one with the address of its current thumbnail; nothing downloads that image.                                                    |
| `playlist list\|show\|renumber`               | List stored playlists, show one with `--videos`, or reassign part numbers (`--start`, `--skip-ids`).                                                        |
| `template list\|show\|new\|import`            | List stored template versions, print one, copy one to files for editing, or store files as a version.                                                       |
| `template validate\|render`                   | Check a layout file, or print a template's prompt for a stored video; no provider is called.                                                                |
| `provider list\|check\|models\|set-key`       | List providers, check one's health, list a provider's models, or store an API key in the keyring.                                                           |
| `thumb generate VIDEO`                        | Generate hero candidates (`--n`, `--template`, `--provider`, `--seed`, `--var`, `--concurrency`, `--out`).                                                  |
| `thumb show\|pick\|export`                    | Show a run's candidates (a picture grid on a colour terminal, file paths elsewhere), pick one, or copy finals (`--raw` for the originals) into a directory. |
| `thumb iterate TARGET`                        | Refine a pick or an iteration into a child run (`--n`, `--prompt-append`, `--var`, `--from-picked`).                                                        |
| `batch PLAYLIST --hero RUN`                   | One thumbnail per playlist item. `--only` selects parts, `--max-images` caps the count, `--dry-run` previews and ignores the cap, `--reference final\|raw`. |
| `runs list\|show\|cost`                       | List runs, print one with its iterations, or total its reported cost.                                                                                       |
| `runs resume\|cancel\|delete`                 | Finish an interrupted or failed batch, abandon a run, or delete one (`--assets` also deletes images).                                                       |
| `config init\|show\|path\|set`                | Write, print and edit the configuration file, and print the paths Thumbforge uses.                                                                          |
| `db init\|upgrade\|status\|path\|vacuum`      | Create the database, apply migrations, report its state, print its path, or reclaim space.                                                                  |

## Files and logs

`thumbforge config path` prints every location Thumbforge uses:

```
$ thumbforge config path
config     <config-dir>/config.toml
data_dir   <data-dir>
state_dir  <state-dir>
db         <data-dir>/thumbforge.sqlite3
assets     <data-dir>/assets
log        <state-dir>/logs/thumbforge.log
```

`--config` (or `THUMBFORGE_CONFIG`) moves `config`, and `--data-dir` (or `THUMBFORGE_GENERAL__DATA_DIR`) moves `data_dir`, `db` and `assets`. They do not move `state_dir`. The state directory holds the log file, one JSON object per line and rotated, and `logs/runs/<run-id>/`, the scratch folder where a provider writes what it produces while a run generates (for the Antigravity provider that includes its raw output and error streams). So a run that uses a scratch config and data directory still writes its logs to your normal per-user state directory.

The state directory is not a `config.toml` setting and has no `THUMBFORGE_*` variable. It comes from the operating system's per-user location, and you move it with the variable the system uses:

| System  | State directory                                                | Move it with                                           |
| ------- | -------------------------------------------------------------- | ------------------------------------------------------ |
| Linux   | `$XDG_STATE_HOME/thumbforge`, else `~/.local/state/thumbforge` | `export XDG_STATE_HOME=$PWD/scratch/state`             |
| Windows | `%LOCALAPPDATA%\thumbforge`                                    | `set WIN_PD_OVERRIDE_LOCAL_APPDATA=%CD%\scratch\state` |

Set it in the same terminal as the other two and `config path` shows the new `state_dir` and `log` lines. On Windows the same variable also moves the default configuration and data directories, which sit under `%LOCALAPPDATA%\thumbforge` too, unless you set those explicitly.

## Exit codes

Every command uses the same codes.

| Code  | Meaning                                                                                             |
| ----- | --------------------------------------------------------------------------------------------------- |
| `0`   | Success.                                                                                            |
| `1`   | An unexpected failure, including a metadata source, database or file error.                         |
| `2`   | Bad usage: a bad option or value, a bad URL, a template error, or a setting that is not valid.      |
| `3`   | Not found: a video, playlist, run, template or provider that does not exist.                        |
| `4`   | The provider failed: no image was made, or a health check failed.                                   |
| `5`   | Compliance: every failure in the run is a final image that breaks one of YouTube's thumbnail rules. |
| `6`   | Partial: some items completed and some failed.                                                      |
| `130` | Interrupted with Ctrl+C; a batch is paused and `runs resume` continues it.                          |
