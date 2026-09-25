# Specs

A spec is the contract for one phase (or one PR-sized task inside it). It says what will exist, how it behaves, and how we will know it works. Specs live next to the code they describe and are published on the docs site (ADR 0016, `docs/adr/0016-zensical-docs-site.md`).

## Rule

Every task in `docs/ROADMAP.md` links to a spec section. A spec must exist and be merged before the PR that implements it is opened; a PR without a spec link is returned. Specs are updated in the same PR when implementation deviates — the spec is never allowed to drift from the code it describes.

## Index

| File                       | Phase                 | Status      |
| -------------------------- | --------------------- | ----------- |
| `phase-0-infra.md`         | 0 — Infra             | Implemented |
| `phase-1-skeleton.md`      | 1 — Skeleton          | Implemented |
| `phase-2-youtube-fetch.md` | 2 — YouTube fetch     | Implemented |
| `phase-3-providers.md`     | 3 — Providers         | Implemented |
| `phase-4-templates.md`     | 4 — Templates         | Proposed    |
| `phase-5-imaging.md`       | 5 — Imaging           | Proposed    |
| `phase-6-hero.md`          | 6 — Hero + iterations | Proposed    |
| `phase-7-batch.md`         | 7 — Batch             | Proposed    |
| `phase-8-polish.md`        | 8 — Polish            | Proposed    |

## Template

Copy the block below into a new `docs/specs/<name>.md`. Keep every heading, even when the answer is "none".

```markdown
# <Phase or task title>

Status: Proposed | Accepted | Implemented
ROADMAP tasks: P<phase>.<n>, …
ADRs: docs/adr/00NN-<slug>.md, …

## Scope

What this phase delivers, in one paragraph plus a bullet per module/command touched.

## Non-goals

What is explicitly deferred and to which phase or spike.

## Interfaces

Signatures, schemas, CLI invocations, file layouts. Copied verbatim from `PLAN.md`
where PLAN.md defines them — never paraphrased.

## Behaviour

Numbered rules: inputs → effects → outputs. Error cases and exit codes.

## Acceptance criteria

Bullet list. Each bullet is an observable check: a command to run and the exact
outcome (exit code, file created, table printed, JSON field present).

## Test plan

Which layer tests what: unit (FakeProvider, recorded fixtures), contract
(`tests/contract/`), `integration` marker (opt-in, network/provider), `golden`
marker (image snapshots).

## Open spikes

Spike IDs from `OPEN_QUESTIONS.md` this phase depends on, and what changes
if the spike answer is negative.
```

## Conventions

- Headings `##`/`###` only below the title.
- Commands are shown as `thumbforge …` (never a Python path) and are copy-pasteable.
- Exit codes always refer to the table in `PLAN.md` §5.1.
- Anything not yet confirmed by a primary source is a spike reference (`S1`–`S14`), never a statement of fact.
