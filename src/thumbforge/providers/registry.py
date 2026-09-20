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

# Runtime import, not TYPE_CHECKING: `get` isinstance-checks the constructed provider
# against this runtime-checkable Protocol.
from thumbforge.core.providers import ImageProvider
from thumbforge.providers.antigravity import AntigravityProvider
from thumbforge.providers.fake import FakeProvider

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from thumbforge.core.json import JsonValue

#: The entry-point group third-party providers declare. The entry-point **name** is the
#: provider key; its value must be a callable returning an `ImageProvider` — in practice the
#: implementing class, whose `__init__` takes the config mapping.
ENTRY_POINT_GROUP = "thumbforge.providers"

#: Returns `object`, not `ImageProvider`, deliberately: a plugin factory is untyped code
#: this build never saw, so promising the Protocol here would be a static lie that `get`
#: then cannot meaningfully check. `get` narrows it with `isinstance` instead.
type ProviderFactory = Callable[[Mapping[str, JsonValue]], object]

#: Providers shipped in this package.
#:
#: A builtin belongs here and **not** in the `thumbforge.providers` entry points: this map is
#: *merged with* that group, so declaring one in both makes it collide with itself under the
#: duplicate-key rule. The group is purely the third-party extension point.
BUILTIN: dict[str, ProviderFactory] = {
    "antigravity": AntigravityProvider,
    "fake": FakeProvider,
}


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

    provider = factory(config or {})

    # `callable()` at discovery only proved the entry point could be called; it says nothing
    # about what came back. Both checks below guard a plugin this build never saw.
    if not isinstance(provider, ImageProvider):
        msg = (
            f"provider {key!r} constructed {type(provider).__name__}, which is not an ImageProvider"
        )
        raise ProviderRegistryError(msg, hint="implement core.providers.ImageProvider")
    if provider.key != key:
        # Provenance is recorded from `provider.key` onto every run and iteration, so a
        # mismatch would attribute images to a provider that did not make them.
        msg = f"provider registered as {key!r} reports key {provider.key!r}"
        raise ProviderRegistryError(msg, hint="make the class key match its entry-point name")
    return provider
