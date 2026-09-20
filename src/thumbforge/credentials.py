"""Provider API keys: read from the environment or the system keyring (ROADMAP P3.5).

`PLAN.md` §8 fixes the lookup order and the single writer:

1. ``THUMBFORGE_PROVIDERS__<KEY>__API_KEY`` in the environment.
2. The system keyring, under service ``thumbforge`` and username ``<provider_key>``.

Nothing else in the codebase writes a secret, and no secret reaches the database, a TOML
file, a log line or a test fixture. `core.redaction` keeps settings and logging from printing
one by accident; this module is the only place that can retrieve or store one.

Named ``credentials`` rather than ``secrets`` so it does not shadow the standard-library
module of that name for readers or for tooling.
"""

from __future__ import annotations

import os

import keyring
from keyring.errors import KeyringError

from thumbforge.core.errors import ProviderAuthError
from thumbforge.logging import get_logger

log = get_logger(__name__)

#: Keyring service name. A single service with one username per provider keeps every key
#: together in the OS credential store, so a user can find and revoke them in one place.
SERVICE = "thumbforge"


def env_var(provider_key: str) -> str:
    """The environment variable this provider's key is read from.

    Mirrors pydantic-settings' nested delimiter, so the variable that configures a provider
    and the variable that authenticates it follow the same convention.
    """
    return f"THUMBFORGE_PROVIDERS__{provider_key.upper()}__API_KEY"


def _from_env(provider_key: str) -> str | None:
    """The key this provider's environment variable supplies, if it supplies one.

    Whitespace-only counts as absent, matching `store_api_key`: an exported-but-blank
    variable is how a shell leaves a value unset, and letting it win would mask a perfectly
    good keyring entry. The value itself is returned unstripped — trimming a credential
    silently changes it.
    """
    value = os.environ.get(env_var(provider_key))
    return value if value and value.strip() else None


def api_key(provider_key: str) -> str | None:
    """This provider's API key, or `None` when neither source has one.

    A keyring that is absent or locked is *not* an error here: the environment may well have
    supplied the key, and a missing key is a reportable state rather than a failure.
    """
    from_env = _from_env(provider_key)
    if from_env is not None:
        return from_env

    try:
        return keyring.get_password(SERVICE, provider_key)
    except KeyringError as exc:
        # Logged, not raised: the caller asked whether a key exists, and "the keyring is
        # unavailable" answers that with "not from here" rather than aborting the command.
        log.debug("credentials.keyring_unavailable", provider=provider_key, error=str(exc))
        return None


def describe(provider_key: str) -> str:
    """Where this provider's key would come from, and which keyring backend is active.

    ADR 0014 asks `provider check` to name the backend: on a CI runner `keyring` resolves to
    a backend that stores nothing, which is otherwise indistinguishable from a working store
    that happens to be empty. Never includes the value.

    Lives here rather than in `cli/` because deciding which source wins is credential logic,
    and `cli/` holds no business logic.
    """
    variable = env_var(provider_key)
    if _from_env(provider_key) is not None:
        return f"key from {variable}"
    backend = type(keyring.get_keyring()).__name__
    found = (
        "key in keyring"
        if api_key(provider_key) is not None
        else f"no key stored; set {variable} to supply one"
    )
    return f"{found} (backend: {backend})"


def store_api_key(provider_key: str, value: str) -> None:
    """Write this provider's key to the system keyring. The only writer of a secret.

    A blank value is rejected rather than stored, because a stored empty string reads back as
    falsy and would look like "no key" while still occupying a credential-store entry.
    """
    if not value.strip():
        msg = f"refusing to store an empty key for provider {provider_key!r}"
        raise ProviderAuthError(msg, hint="pass a non-empty value, or delete the entry instead")

    try:
        keyring.set_password(SERVICE, provider_key, value)
    except KeyringError as exc:
        # Here the keyring *is* the destination, so its absence is fatal and the hint has to
        # name the fallback that works without one.
        msg = f"the system keyring rejected the key for provider {provider_key!r}: {exc}"
        raise ProviderAuthError(msg, hint=f"set {env_var(provider_key)} instead") from exc

    log.info("credentials.stored", provider=provider_key, service=SERVICE)
