# Resume an interrupted run

Stop a long batch with Ctrl+C, or lose it to a crash or a provider outage, and carry on later without paying for the same images twice. Thumbforge records every finished image as it goes; resuming regenerates only the items that did not finish, and retries failed ones up to a limit. You will also be able to list, inspect, cancel and delete runs. See [Hero](../concepts/hero.md#runs-and-iterations) for run states.

!!! note "Coming in v0.1.0"

    Interrupt and resume handling is roadmap task P7.2 and the `thumbforge runs list|show|resume|cancel|delete` commands are P7.4, defined in the [Phase 7 spec](../../specs/phase-7-batch.md#behaviour) and [ADR 0012](../../adr/0012-idempotency-and-resumable-runs.md).

## Prerequisites you can do today

```
thumbforge config path
thumbforge db status
```

`config path` shows where the database and logs live; `db status` confirms the database is at the current schema revision.
