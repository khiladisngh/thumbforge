# Resume an interrupted run

Stop a long batch with Ctrl+C, or lose it to a crash or a provider outage, and carry on later without paying for the same images twice. Thumbforge records every finished image as it goes; picking up again regenerates only the items that did not finish, and retries failed ones up to a limit. You can also list, inspect, cancel and delete runs. See [Hero](../concepts/hero.md#runs-and-iterations) for run states.

## Stop a batch

Press Ctrl+C while `thumbforge batch` runs. The item being generated is marked failed with the error `interrupted` (that try does not count against its retries), items that had not started stay `pending`, finished items are untouched, and the run is `paused`. The command prints the counts, for example `paused (7 completed, 1 failed, 4 pending)`, and exits `130`.

## Continue it

```
thumbforge runs resume <run-id>
```

Completed items are skipped without a provider call; failed and unfinished ones are retried in place, inside the same run, and a `running` item that has not moved for 15 minutes (`[batch] stale_after_s`) is taken to belong to a crashed process and retried too. The run is reopened and ends `completed` (or `failed` again) from its own items. The same options as `batch` apply: progress on a terminal, `--json`, and the exit codes `0`, `4`, `6` and `130`. `--concurrency N` overrides the number of parallel provider calls the run was started with.

`runs resume` refuses a run that is `completed` or `cancelled`, or that is not a batch run (exit `2`), and exits `3` for an unknown run id.

Running the same `batch` command again also works: it retries the same items, but as a run of its own, and the interrupted run keeps the `paused` status it was left in.

## Give up on a run

```
thumbforge runs cancel <run-id>
```

marks the run `cancelled`, and every iteration of it that was still `pending` or `running` with it. Finished and failed iterations are left as they are, and a cancelled run cannot be resumed. A `completed` run has nothing to cancel and is refused (exit `2`); cancelling a run that is already cancelled changes nothing. This does not stop a `batch` that is still running in another terminal: press Ctrl+C there.

## Inspect and clean up runs

```
thumbforge runs list [--kind batch] [--status failed] [--limit 20]
thumbforge runs show <run-id>
thumbforge runs cost <run-id>
thumbforge runs delete <run-id> [--assets]
thumbforge config path
thumbforge db status
```

`runs list` prints the newest runs first: id, kind, status, template, provider, how many iterations are done and how many failed. `runs show` lists a run's iterations, with the tokens each one used when its provider reported them; for a batch run it also shows the playlist and the item counts. `runs cost` totals the tokens in and out, the credits and the provider time of the run's own iterations (not those of a batch built on it), and says how many iterations the provider reported no cost for. A run whose provider reported none, like the built-in `fake` one, prints `has no cost data` rather than zeros. `--json` works on both commands. `config path` shows where the database and logs live; `db status` confirms the database is at the current schema revision.

`runs delete` removes a run and its iterations. The image files stay unless you pass `--assets`, which also deletes the files that no other run, iteration or reference image still uses (identical images made by two runs are one shared file, so it goes only with the last of them). A run that other runs build on is refused with exit `2` and the ids of those runs: a hero that a batch took as its reference, or the parent of a refinement made with `thumb iterate`. Delete the batch or the refinement first.
