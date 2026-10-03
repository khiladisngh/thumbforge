# Resume an interrupted run

Stop a long batch with Ctrl+C, or lose it to a crash or a provider outage, and carry on later without paying for the same images twice. Thumbforge records every finished image as it goes; picking up again regenerates only the items that did not finish, and retries failed ones up to a limit. You will also be able to list, inspect, cancel and delete runs. See [Hero](../concepts/hero.md#runs-and-iterations) for run states.

!!! note "Coming in v0.1.0"

    The `thumbforge runs list|resume|cancel|delete` commands are roadmap task P7.4, defined in the [Phase 7 spec](../../specs/phase-7-batch.md#behaviour) and [ADR 0012](../../adr/0012-idempotency-and-resumable-runs.md). Until then, run the same `batch` command again, as below.

## Stop a batch

Press Ctrl+C while `thumbforge batch` runs. The item being generated is marked failed with the error `interrupted` (that try does not count against its retries), items that had not started stay `pending`, finished items are untouched, and the run is `paused`. The command prints the counts, for example `paused (7 completed, 1 failed, 4 pending)`, and exits `130`.

## Continue it

Run the same `batch` command again. Completed items are skipped without a provider call; failed and unfinished ones are retried inside the run that created them, and a `running` item that has not moved for 15 minutes (`[batch] stale_after_s`) is taken to belong to a crashed process and retried too. The repeat is a run of its own and ends `completed` when everything is done; the interrupted run keeps the `paused` status it was left in.

## Inspect a run

```
thumbforge runs show <run-id>
thumbforge config path
thumbforge db status
```

`runs show` lists a run's iterations. `config path` shows where the database and logs live; `db status` confirms the database is at the current schema revision.
