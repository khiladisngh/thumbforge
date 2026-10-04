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

| Command                                       | What it does                                                                                               |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `fetch URL [--source ytdlp\|api] [--refresh]` | Fetch a video, playlist or channel and store its metadata.                                                 |
| `video list\|show`                            | List stored videos, or show one.                                                                           |
| `playlist list\|show\|renumber`               | List stored playlists, show one with `--videos`, or reassign part numbers (`--start`, `--skip-ids`).       |
| `template list\|show\|new\|import`            | List stored template versions, print one, copy one to files for editing, or store files as a version.      |
| `template validate\|render`                   | Check a layout file, or print a template's prompt for a stored video; no provider is called.               |
| `provider list\|check\|models\|set-key`       | List providers, check one's health, list a provider's models, or store an API key in the keyring.          |
| `thumb generate VIDEO`                        | Generate hero candidates (`--n`, `--template`, `--provider`, `--seed`, `--var`, `--concurrency`, `--out`). |
| `thumb show\|pick\|export`                    | Show a run's candidates, pick one, or copy finals (`--raw` for the originals) into a directory.            |
| `thumb iterate TARGET`                        | Refine a pick or an iteration into a child run (`--n`, `--prompt-append`, `--var`, `--from-picked`).       |
| `batch PLAYLIST --hero RUN`                   | One thumbnail per playlist item (`--only`, `--max-images`, `--dry-run`, `--reference final\|raw`).         |
| `runs list\|show\|cost`                       | List runs, print one with its iterations, or total its reported cost.                                      |
| `runs resume\|cancel\|delete`                 | Finish an interrupted or failed batch, abandon a run, or delete one (`--assets` also deletes images).      |
| `config init\|show\|path\|set`                | Write, print and edit the configuration file, and print the paths Thumbforge uses.                         |
| `db init\|upgrade\|status\|path\|vacuum`      | Create the database, apply migrations, report its state, print its path, or reclaim space.                 |

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
