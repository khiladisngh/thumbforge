# ADR 0014: Secrets via environment variables and keyring

## Status

`Accepted` — 2026-09-19

## Context

Future providers (an HTTP image API) and the optional YouTube Data API source (decision D7) need API keys. The config TOML (ADR 0003) is meant to be shared and committed to dotfiles; the SQLite database (ADR 0004) is copied around with `data_dir`; `provider_profile.params_json` is snapshotted verbatim into every run. None of these may ever contain a secret. The Antigravity CLI needs no key at all — it uses its own cached login.

## Decision

- Lookup order for a provider secret: environment variable `THUMBFORGE_PROVIDERS__<KEY>__API_KEY` (uppercase provider key), then `keyring` (`uv add keyring`) with service `thumbforge` and username `<provider_key>`.
- `thumbforge provider set-key KEY` prompts (no echo) and writes to keyring; nothing else writes secrets. There is no `--api-key` flag.
- The settings loader rejects any TOML key matching `*_key`, `*_token`, `*_secret` with `SettingsError` and a hint pointing at env/keyring.
- The DB schema has no secret columns; `provider_profile.params_json` is validated against a deny-list of the same patterns before insert.
- Secrets are never logged: structlog processors drop keys matching the deny-list (ADR 0015), and provider subprocess environments receive only the variables the adapter whitelists.
- `provider list` shows auth state as `ok | missing | n/a`, never the value.

## Consequences

- CI supplies secrets purely through environment variables; no keyring backend is required on runners.
- On Windows, `keyring` uses Windows Credential Manager; on Linux, Secret Service or a file backend — `provider check KEY` reports which backend is active.
- A `config.toml` can be committed publicly without review for leaked keys.
- Contributors adding a provider must put its secret name in the adapter's `secret_names` tuple so the deny-list and `set-key` know about it.

## Alternatives considered

- **Secrets in `config.toml`** — rejected: the file is user-editable, often synced to dotfiles repos, and printed by `config show`.
- **A `.env` file loaded automatically** — rejected: silently picks up files from the working directory; explicit environment variables are predictable.
- **Encrypting secrets inside SQLite** — rejected: the key would need to live somewhere, which is exactly what keyring already solves.
