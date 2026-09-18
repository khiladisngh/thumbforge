# Testing

## Layers

| Layer       | Location             | Rules                                                                                                                                                                             |
| ----------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Unit        | `tests/unit/`        | No network, no real providers, no real `agy`. Use `FakeProvider` and recorded yt-dlp fixtures (`tests/fixtures/ytdlp/*.json`). Fast (< 1 s each).                                 |
| Contract    | `tests/contract/`    | `test_provider_contract.py` is parametrised over every provider in the registry; a provider that cannot pass it cannot ship. Real providers are skipped unless `-m integration`.  |
| Integration | `tests/integration/` | Marked `integration`; hit live YouTube or the real Antigravity CLI. Excluded by default (`addopts = "-m 'not integration'"`). Run with `uv run pytest -m integration`.            |
| Golden      | `tests/golden/`      | Marked `golden`; text overlay and layout rendering compared against committed PNGs with a small pixel tolerance. Only bundled fonts are used so output is stable across machines. |

## Commands

```
uv run pytest -q                       # unit + contract (default)
uv run pytest -m integration           # live systems, opt-in
uv run pytest -m golden                # image snapshots
uv run pytest --cov --cov-fail-under=80
```

## Fixtures

- yt-dlp responses are recorded once by an `integration`-marked recorder test and committed as JSON. Re-record when yt-dlp changes shape; review the diff.
- FakeProvider is deterministic: same prompt + seed → same bytes. Prompts containing `[[FAIL_TRANSIENT]]` / `[[FAIL_PERMANENT]]` raise the corresponding errors, which is how retry and resume paths are tested.
- Antigravity adapter unit tests use a fake `agy` script on `PATH` that emits chosen JSON envelopes and exit codes, covering every row of the error-mapping table in `PLAN.md` §4.3.

## What a test must do

Defend an observable contract: behaviour, boundaries, invariants, state transitions, error mapping. Do not test wiring, defaults, or source text. Delete tests that only pin implementation.

## CI

`ci.yml` runs ruff, pyright, pytest with coverage (fail under 80 %), and `zensical build` on Ubuntu and Windows for Python 3.14.
