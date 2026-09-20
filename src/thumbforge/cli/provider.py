"""``thumbforge provider`` — inspect providers and store their keys (ROADMAP P3.5)."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Annotated

import typer

from thumbforge import credentials
from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import emit, get_app_context, kv, table
from thumbforge.core.errors import ProviderAuthError, ProviderPermanentError
from thumbforge.core.json import JsonPayload, JsonValue
from thumbforge.providers import registry

if TYPE_CHECKING:
    from collections.abc import Mapping

    from thumbforge.core.providers import HealthReport, ImageProvider
    from thumbforge.settings import Settings

app = typer.Typer(
    name="provider",
    help="Inspect image providers, check their health, and store their API keys.",
    no_args_is_help=True,
)

#: The `Check.name` a provider uses for "are we authenticated". A failure under this name is
#: reported as `ProviderAuthError` so a `--json` consumer can tell "not signed in" from
#: "installed wrong" — both exit 4, but they call for different actions.
AUTH_CHECK = "auth"

_KEY_ARGUMENT = Annotated[str, typer.Argument(metavar="KEY", help="Provider registry key.")]


def _config(settings: Settings, key: str) -> Mapping[str, JsonValue]:
    """The provider's own settings section, or an empty mapping when it has none.

    Providers take a plain mapping rather than `Settings` so nothing in `providers/` depends
    on the settings model. `fake` has no section at all, which is not an error.
    """
    section = getattr(settings.providers, key, None)
    if section is None:
        return {}
    dumped: JsonPayload = section.model_dump(mode="json")
    return dumped


def _summarise(provider: ImageProvider) -> str:
    """The capability flags worth seeing in a one-line table cell."""
    caps = provider.capabilities
    flags = [
        name
        for name, enabled in (
            ("reference", caps.supports_reference_image),
            ("seed", caps.supports_seed),
            ("negative", caps.supports_negative_prompt),
            ("aspect", caps.supports_aspect_ratio),
        )
        if enabled
    ]
    formats = "/".join(sorted(caps.output_formats))
    return f"{', '.join(flags) or 'none'} · {formats} · x{caps.max_concurrency}"


def _raise_for_report(key: str, report: HealthReport) -> None:
    """Turn a failed health report into the error whose exit code the CLI contract promises.

    The report is already printed by the caller, so the failing checks go into the hint
    rather than the message: the user has the full table and needs the next action.
    """
    if report.ok:
        return
    failed = [check for check in report.checks if not check.ok]
    hint = "; ".join(f"{check.name}: {check.detail}" for check in failed)
    msg = f"provider {key!r} is not healthy"
    if any(check.name == AUTH_CHECK for check in failed):
        raise ProviderAuthError(msg, hint=hint)
    raise ProviderPermanentError(msg, hint=hint)


@app.command("list")
@handle_errors
def list_(ctx: typer.Context) -> None:
    """List every registered provider with its version, auth state and capabilities."""
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()

    async def collect() -> list[JsonPayload]:
        rows: list[JsonPayload] = []
        # Bound to a local because SIM118 mistakes this module-level function for dict.keys().
        registered = registry.keys()
        for key in registered:
            provider = registry.get(key, _config(settings, key))
            info = await provider.info()
            rows.append(
                {
                    **info.model_dump(mode="json"),
                    "capabilities": provider.capabilities.model_dump(mode="json"),
                    "summary": _summarise(provider),
                }
            )
        return rows

    # One `asyncio.run` per invocation: the CLI is the only sync/async boundary.
    rows = asyncio.run(collect())

    emit(
        app_ctx,
        {"providers": rows, "count": len(rows)},
        render=lambda: table(
            ["Key", "Name", "Version", "Auth", "Capabilities"],
            [
                [
                    str(row["key"]),
                    str(row["name"]),
                    str(row["version"]),
                    str(row["auth"]),
                    str(row["summary"]),
                ]
                for row in rows
            ],
        ),
    )


@app.command("check")
@handle_errors
def check(ctx: typer.Context, key: _KEY_ARGUMENT) -> None:
    """Run a provider's health checks and report every one of them.

    Exits 3 for an unknown key, 4 when a check fails, 0 when all pass.
    """
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()

    provider = registry.get(key, _config(settings, key))
    report = asyncio.run(provider.healthcheck())
    # Resolved once: the render thunk would otherwise repeat the keyring read.
    credential_state = credentials.describe(key)
    payload: JsonPayload = {
        "provider": key,
        "ok": report.ok,
        **report.model_dump(mode="json"),
        "credentials": credential_state,
    }

    emit(
        app_ctx,
        payload,
        render=lambda: table(
            ["Check", "Result", "Detail"],
            [
                *(
                    [check_.name, "ok" if check_.ok else "FAILED", check_.detail]
                    for check_ in report.checks
                ),
                # Informational, and deliberately not part of `report.ok`: no provider needs
                # an API key yet, so "no key stored" must not fail the command. ADR 0014
                # asks `provider check` to name the active backend, because a keyring that
                # silently has none is otherwise indistinguishable from an empty one.
                ["credentials", "info", credential_state],
            ],
            title=f"{key} · {'healthy' if report.ok else 'not healthy'}",
        ),
    )

    _raise_for_report(key, report)


@app.command("models")
@handle_errors
def models(ctx: typer.Context, key: _KEY_ARGUMENT) -> None:
    """List the model slugs a provider offers, for use as ``providers.<key>.model``.

    Read from the provider's health report, which is where the protocol already carries them,
    so this needs no second way of asking.
    """
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()

    provider = registry.get(key, _config(settings, key))
    report = asyncio.run(provider.healthcheck())

    # A failed report first: reporting "no models" when the real problem is a missing login
    # would send the user looking in the wrong place.
    _raise_for_report(key, report)

    emit(
        app_ctx,
        {"provider": key, "models": list(report.models), "count": len(report.models)},
        render=lambda: (
            table(["Model"], [[slug] for slug in report.models])
            if report.models
            else f"{key} reports no model selection"
        ),
    )


@app.command("set-key")
@handle_errors
def set_key(ctx: typer.Context, key: _KEY_ARGUMENT) -> None:
    """Store a provider's API key in the system keyring.

    The only writer of a secret in this codebase. The value is prompted for rather than taken
    as an argument, so it never reaches the shell history or a process listing.
    """
    app_ctx = get_app_context(ctx)
    settings = app_ctx.require_settings()

    # Resolved before prompting so a typo costs a message rather than a typed-out secret.
    registry.get(key, _config(settings, key))

    value = typer.prompt(f"API key for {key}", hide_input=True)
    credentials.store_api_key(key, value)

    emit(
        app_ctx,
        {"provider": key, "stored": True, "service": credentials.SERVICE},
        render=lambda: kv(
            {
                "provider": key,
                "keyring service": credentials.SERVICE,
                "overrides": f"{credentials.env_var(key)} still wins if set",
            },
            title="stored in the system keyring",
        ),
    )
