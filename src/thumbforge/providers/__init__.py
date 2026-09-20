"""Image providers: concrete `core.providers.ImageProvider` implementations and the registry.

Nothing here is imported by name from outside: callers ask `registry.get(key, config)`, which
is what lets a third-party provider work without this package knowing it exists (ADR 0010).
"""

from thumbforge.providers.registry import ENTRY_POINT_GROUP, get, keys

__all__ = ["ENTRY_POINT_GROUP", "get", "keys"]
