# ADR 0017: Logging verbosity mapping and secret redaction

## Status

`Accepted` — 2026-09-19

Supersedes the verbosity and redaction bullets of [ADR 0015](0015-structlog-logging.md). Every other decision in ADR 0015 — structlog, the stdlib bridge, stderr-only logs, the always-DEBUG JSON file handler — stands unchanged.

## Context

ADR 0015 and `docs/specs/phase-1-skeleton.md` specified two different verbosity mappings, and the implementation matched neither:

| Source         | default           | `-v`                       | `-vv`              | `--quiet` |
| -------------- | ----------------- | -------------------------- | ------------------ | --------- |
| ADR 0015       | `INFO`            | `DEBUG` for `thumbforge.*` | `DEBUG` everywhere | `WARNING` |
| Spec §135      | `WARNING`         | `INFO`                     | `DEBUG`            | `ERROR`   |
| Implementation | `[logging] level` | `INFO`                     | `DEBUG`            | `ERROR`   |

ADR 0015 also specified a processor that _drops_ secret-looking keys. It was never implemented, so a provider key passed to a log call would reach the console, the rotating log file, and any bug report pasted from it.

Two further facts emerged while implementing:

- Scoping `-v` to `thumbforge.*` only means a second, invisible axis of filtering. Third-party records already flow through the same processor chain via `ProcessorFormatter`; filtering them differently surprises anyone reading the output.
- Dropping a secret key entirely hides that a field was present at all, which makes a redacted log harder to reason about than one that says a value was withheld.

## Decision

**Verbosity.** The console level defaults to `[logging] level` (itself defaulting to `INFO`); `-v` → `INFO`, `-vv` → `DEBUG`, `--quiet` → `ERROR`. `--quiet` outranks `-v`: an explicit request for silence should beat a `-v` baked into someone's script. The mapping applies to all loggers, not only `thumbforge.*`. The file handler is unaffected and always records `DEBUG`.

**Redaction.** A final processor, `redact_secrets`, _replaces_ — rather than drops — values whose key matches the deny-list, substituting `***redacted***`. It walks nested mappings and sequences, because a secret is as likely to arrive inside `settings={"api_key": ...}` as at the top level. It applies to bound contextvars as well as call-site fields.

The deny-list lives in `thumbforge.core.redaction` and is shared with the settings loader from [ADR 0014](0014-secrets-env-keyring.md), so a key that is a secret for configuration is a secret for logging.

**Degradation.** If the log file cannot be opened, logging falls back to console only and emits one `file logging disabled` warning. Logging is support infrastructure; a read-only state directory must not stop a command the user asked for.

## Consequences

- One documented mapping, matching the code and the spec; `docs/specs/phase-1-skeleton.md` §135 updated in the same change.
- Redacted records show which fields were withheld, at the cost of a recursive walk over event values on **every** log call. Handler levels are applied after the processor chain runs, so a suppressed record still pays the walk; the cost is bounded by event size and accepted deliberately, because a chain that skips redaction under some conditions is a chain that leaks.
- Sharing the deny-list means widening it later protects configuration and logs together.

## Alternatives considered

- **Keep ADR 0015's mapping** — rejected: `--quiet` → `WARNING` still prints warnings, which is not what "quiet" means to anyone scripting the tool, and per-namespace `-v` filtering is invisible to the user.
- **Keep the spec's mapping (default `WARNING`)** — rejected: it ignores `[logging] level`, making that setting inert unless flags are absent, which is the opposite of how the rest of the configuration behaves.
- **Drop secret keys rather than replace them** — rejected: an absent field is indistinguishable from one that was never set, which is worse when triaging.
- **Redact only top-level keys** — rejected: nested structures are exactly where a settings dump or provider payload carries a key.
