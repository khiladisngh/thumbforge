# ADR 0003: pydantic-settings with TOML config and platformdirs locations

## Status

`Accepted` — 2026-09-19

## Context

The CLI needs persistent user configuration (default provider, output size, provider parameters, logging), a data directory for the SQLite database and asset store, and a state directory for logs. Locations must follow OS conventions on Windows and Linux, be overridable per invocation (`--config`, `--data-dir`) and via environment for CI. Secrets must never be in the config file (ADR 0014).

## Decision

- Settings are a `pydantic-settings` `BaseSettings` model in `src/thumbforge/settings.py`, loaded in this precedence (highest first): CLI flags → environment variables → TOML file → defaults.
- Environment: `env_prefix = "THUMBFORGE_"`, `env_nested_delimiter = "__"`. Example: `THUMBFORGE_PROVIDERS__ANTIGRAVITY__MODEL`.
- Locations via `platformdirs` with app name `thumbforge`:
    - config: `user_config_dir("thumbforge")/config.toml`
    - data (DB + assets): `user_data_dir("thumbforge")`
    - state (logs, per-iteration provider output): `user_state_dir("thumbforge")`
- TOML schema (defaults):

    ```toml
    [general]
    data_dir = "<platformdirs user_data_dir>"
    default_provider = "fake"
    default_template = "bold-title"

    [output]
    width = 1920
    height = 1080
    format = "jpeg"
    quality = 90
    max_bytes = 2097152

    [batch]
    concurrency = 1
    max_retries = 2
    stale_after_s = 900

    [providers.antigravity]
    binary = "agy"
    model = null
    effort = "low"
    timeout_s = 600
    skip_permissions = true

    [logging]
    level = "INFO"
    format = "console"
    ```

- `thumbforge config init` writes the defaults; `config show|path|set KEY VALUE` read and modify it; `config set` validates the dotted key against the schema and exits `2` on error.
- A model validator rejects any TOML key matching `*_key`, `*_token`, `*_secret` with `SettingsError` (ADR 0014).

## Consequences

- One typed object is the only source of configuration; services receive it by parameter, never read the environment themselves.
- Relocating `data_dir` is safe because `asset.rel_path` is relative (ADR 0011).
- Output size defaults depend on decision D2; the schema does not change, only the default values.
- Tests set `THUMBFORGE_GENERAL__DATA_DIR` to a `tmp_path`, so no test touches real user directories.

## Alternatives considered

- **YAML config** — rejected: needs an extra parser dependency and has implicit type coercion; TOML is stdlib (`tomllib`) and matches `pyproject.toml`.
- **Config inside the SQLite database** — rejected: unreadable and un-diffable by hand; provider settings should be editable with a text editor.
- **`dynaconf` / `hydra`** — rejected: heavier than needed for a single-file config; pydantic-settings gives the same typed model used for validation everywhere else.
