"""Provider lookup by key, merging builtins with installed plugins (ADR 0010, P3.1).

Core code never imports a concrete provider — it asks here. That is what lets a third party
ship a provider by declaring an entry point in the `thumbforge.providers` group without this
repository knowing about it.

Discovery lives in `providers/` rather than `core/` because it reads installed distribution
metadata, which is an adapter concern. The Protocol it hands back lives in `core.providers`.

A provider is constructed from its **own config mapping**, not from `Settings`. `storage` and
`sources` likewise take plain values, so no adapter depends on the application's whole
configuration tree; `cli` extracts `settings.providers.<key>` and passes it down. A mapping
rather than a typed model because the registry cannot know which model each third-party
provider wants, and `provider_profile.params_json` already stores provider config this way.
"""

from __future__ import annotations

from importlib.metadata import entry_points
from typing import TYPE_CHECKING, cast

from thumbforge.core.errors import NotFoundError, ProviderRegistryError

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from thumbforge.core.json import JsonValue
    from thumbforge.core.providers import ImageProvider

#: The entry-point group third-party providers declare. The entry-point **name** is the
#: provider key; its value must be a callable returning an `ImageProvider` — in practice the
#: implementing class, whose `__init__` takes the config mapping.
ENTRY_POINT_GROUP = "thumbforge.providers"

type ProviderFactory = Callable[[Mapping[str, JsonValue]], ImageProvider]

#: Providers shipped in this package. Populated by P3.2 (`fake`) and P3.4 (`antigravity`);
#: empty until then, so the registry is exercised through entry points only.
BUILTIN: dict[str, ProviderFactory] = {}


def _discover() -> dict[str, ProviderFactory]:
    """Merge builtins with installed entry points, refusing any duplicate key.

    A duplicate is an error rather than a precedence rule: silently shadowing a provider
    would make `--provider x` mean different things depending on what else is installed,
    and that failure surfaces as wrong images rather than as a message.
    """
    found: dict[str, ProviderFactory] = dict(BUILTIN)
    origin: dict[str, str] = dict.fromkeys(found, "builtin")

    for entry in entry_points(group=ENTRY_POINT_GROUP):
        if entry.name in found:
            msg = (
                f"provider key {entry.name!r} is claimed twice: "
                f"{origin[entry.name]} and {entry.value}"
            )
            raise ProviderRegistryError(msg, hint="uninstall one of the conflicting providers")

        try:
            loaded = entry.load()
        except Exception as exc:
            # A broken plugin must not be skipped silently: that is indistinguishable from
            # "never installed", which is the harder failure to diagnose. It also must not
            # be swallowed, so `provider list` reports the real reason.
            msg = f"provider {entry.name!r} failed to load from {entry.value}"
            raise ProviderRegistryError(msg, hint="reinstall or uninstall that plugin") from exc

        if not callable(loaded):
            msg = f"provider {entry.name!r} is {loaded!r}, which is not callable"
            raise ProviderRegistryError(
                msg, hint="the entry point must name an ImageProvider class"
            )

        # `entry.load()` is untyped by construction — the plugin is not part of this build.
        # The cast is the boundary; `get` instantiates and the caller meets the Protocol.
        found[entry.name] = cast("ProviderFactory", loaded)
        origin[entry.name] = entry.value

    return found


def keys() -> list[str]:
    """Every registered provider key, sorted so command output is stable."""
    return sorted(_discover())


def get(key: str, config: Mapping[str, JsonValue] | None = None) -> ImageProvider:
    """Instantiate the provider registered under `key`.

    An unknown key raises `NotFoundError` (exit 3) and the hint lists what is available,
    because the cause is almost always a typo or a plugin that was never installed.
    """
    found = _discover()
    factory = found.get(key)
    if factory is None:
        available = ", ".join(sorted(found)) or "none installed"
        msg = f"provider {key!r}"
        raise NotFoundError(msg, hint=f"available: {available}")
    return factory(config or {})
