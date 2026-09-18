## What

<!-- one paragraph: the single concern this PR addresses -->

## Links

- ROADMAP task: P?.?
- Spec: docs/specs/…
- Issue: #…

## Checklist

- [ ] One concern only; title is a Conventional Commit
- [ ] Spec updated if behaviour changed
- [ ] Tests at the right layer (unit / contract / integration / golden); no network in unit tests
- [ ] `uv run ruff check . && uv run ruff format --check .`
- [ ] `uv run pyright`
- [ ] `uv run pytest --cov --cov-fail-under=80`
- [ ] `uv run zensical build`
- [ ] Docs / ADR / `AGENTS.md` updated if structure or conventions changed
- [ ] `graphify update .` run and `graphify-out/` committed (minus `cost.json`) if source structure changed

## Test evidence

<!-- paste the actual command output that proves the acceptance criteria -->
