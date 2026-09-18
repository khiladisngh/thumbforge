# Phase 8 — Polish

Status: Proposed
ROADMAP tasks: P8.1, P8.2, P8.3, P8.4, P8.5
ADRs: `docs/adr/0005-ytdlp-metadata-source.md`, `docs/adr/0002-typer-rich-cli.md`, `docs/adr/0014-secrets-env-keyring.md`, `docs/adr/0001-python-and-uv.md`

## Scope

Round out the tool for daily use: optional YouTube Data API metadata source, installation and shell completion docs, cost reporting, and the README.

- **P8.1** `sources/youtube_api.py` (`YouTubeDataApiSource`) behind the `api` extra (decision D7).
- **P8.2** `uv tool install thumbforge` documentation and first-run walkthrough (`docs/GETTING_STARTED.md`).
- **P8.3** shell completion (`thumbforge --install-completion`, Typer builtin) documented and smoke-tested on PowerShell, bash, zsh.
- **P8.4** `runs cost <run>` report and a `cost` column in `runs show`.
- **P8.5** `README.md` final content, CHANGELOG via `git-cliff`, first tag `v0.1.0` (release workflow from `phase-0-infra.md`).

## Non-goals

- New providers; the plugin group exists for that.
- GUI/web UI.
- Metrics upload or telemetry of any kind.

## Interfaces

### YouTube Data API source

```toml
# pyproject.toml
[project.optional-dependencies]
api = ["google-api-python-client", "google-auth"]
```

```python
class YouTubeDataApiSource:  # implements MetadataSource from phase-2-youtube-fetch.md
    key: ClassVar[str] = "api"

    def __init__(self, api_key: str) -> None: ...
```

- Selected with `fetch --source api`; the key is resolved by the Phase 3 secrets order (`THUMBFORGE_PROVIDERS__API__API_KEY`, then keyring service `thumbforge` username `api`, written by `thumbforge provider set-key api` — the same keyring path is reused for sources).
- Missing extra → `SourceError` with hint `uv tool install "thumbforge[api]"`, exit `1`; missing key → `SourceError` with hint `thumbforge provider set-key api`, exit `1`.
- Field mapping to `VideoMeta`/`PlaylistMeta`/`ChannelMeta` is identical to `YtDlpSource`; `source = "api"` on stored rows. Pagination via `pageToken` until exhausted; quota errors (`403 quotaExceeded`) map to `SourceError` and are not retried.

### Cost report

```python
def cost_report(run: Run) -> CostReport
    # CostReport(run_id, iterations: int, tokens_in: int, tokens_out: int, credits: Decimal | None, currency: str | None, duration_ms: int)
```

`thumbforge runs cost <run>` prints the report (JSON with `--json`). Values aggregate `iteration.cost_json`; iterations with `cost_json NULL` count as zero and are reported in a `no_cost_data` count. Whether Antigravity populates credits is spike S8.

### Completion

`thumbforge --install-completion` and `--show-completion` are Typer's builtin options; docs cover PowerShell profile placement on Windows.

## Behaviour

1. `fetch --source api` produces rows indistinguishable from `--source ytdlp` except `source`; re-fetching with a different source updates `source` and `fetched_at`.
2. `runs cost` on a FakeProvider run reports zero tokens and `no_cost_data = <n>`; on an Antigravity run reports the summed `usage` fields from the envelopes.
3. `README.md` covers: install, `fetch` → `thumb generate` → `thumb pick` → `batch` in five commands, provider setup (Antigravity login, `skip_permissions` note from decision D4), config path, docs link.
4. `git-cliff` generates `CHANGELOG.md` from Conventional Commits at tag time; the `v0.1.0` tag triggers `release.yml`. PyPI publishing happens only if decision D5 says yes; otherwise the `publish` job is removed before tagging.

## Acceptance criteria

- `uv sync --locked --extra api` then `thumbforge fetch <playlist> --source api` with a valid key (integration marker) stores the same 12 videos as the ytdlp fixture with `source = api`.
- Without the extra, `thumbforge fetch <url> --source api` exits `1` and prints the install hint; with the extra but no key, exits `1` with the `set-key` hint.
- `thumbforge runs cost <fake run>` prints `tokens_in 0`, `no_cost_data 4` for a 4-iteration hero run.
- `thumbforge --install-completion powershell` appends to the PowerShell profile and `thumbforge th<TAB>` completes to `thumb` in a fresh shell (manual check, recorded in the PR).
- `uv tool install .` from a checkout puts `thumbforge` on PATH and `thumbforge --version` prints `thumbforge 0.1.0`.
- Tagging `v0.1.0` runs `release.yml` to a green `build` job with `dist/thumbforge-0.1.0-py3-none-any.whl` attached to the GitHub release.

## Test plan

- Unit: `YouTubeDataApiSource` against recorded API JSON in `tests/fixtures/youtube_api/*.json` with a stubbed `build()`; quota error mapping; pagination; extra-missing and key-missing hints via `CliRunner`; `cost_report` aggregation.
- Integration (`-m integration`): one live Data API playlist fetch when `THUMBFORGE_PROVIDERS__API__API_KEY` is set.
- Contract: `MetadataSource` contract test parametrised over `{ytdlp, api}` (added here; `tests/contract/test_source_contract.py`).
- Golden: none.

## Open spikes

- **S8** cost/usage fields from Antigravity — decides whether `credits`/`currency` are ever non-null.
- **S12** Python 3.15 GA — add to CI matrix and `requires-python` note in README before `v0.1.0` if GA has happened.
- Decision **D7** — if the Data API source is dropped, P8.1 and the `api` extra are removed from this spec and `fetch --source api` keeps the Phase 2 behaviour (exit `2`).
