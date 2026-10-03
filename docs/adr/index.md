# Decision records

An architecture decision record (ADR) captures one decision that shapes the project: the context that forced it, the decision itself with concrete values, its consequences, and the alternatives that were rejected and why. ADRs are numbered and never reuse a number. Each record's status line says whether it is `Proposed`, `Accepted` or `Superseded by` a later one; the records are listed in the navigation.

## Adding a decision

1. Copy [`0000-template.md`](0000-template.md) to `docs/adr/NNNN-<kebab-slug>.md`, using the next free number.
2. Fill in every section; reference unverified facts by their spike id in [Open questions](../maintainers/open-questions.md) instead of asserting them.
3. Set the status line and date as the template shows.
4. Add the file to the "Decision records" section of `nav` in `zensical.toml`; the strict docs build fails on any broken link in it.

## Changing a decision

Never edit an Accepted ADR's decision. Write a new ADR that supersedes it, and change only the old record's status line to `Superseded by ADR NNNN`.
