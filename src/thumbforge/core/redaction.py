"""Secret detection shared by configuration loading and logging (ADR 0014, ADR 0017).

One deny-list and one traversal, used two ways: settings *refuses* to load a config file
containing these keys, and the log pipeline *redacts* them from event dictionaries. A key that
is a secret for one is therefore a secret for the other.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Final, cast

#: Key suffixes that mark a value as secret. Matched case-insensitively.
SECRET_SUFFIXES: Final[tuple[str, ...]] = ("_key", "_token", "_secret", "_password")

#: What a redacted value is replaced with. Replacing rather than dropping keeps the fact that a
#: field was present visible, which matters when triaging a log.
REDACTED: Final[str] = "***redacted***"


def is_secret_key(key: str) -> bool:
    """Return whether ``key`` names a secret."""
    return key.lower().endswith(SECRET_SUFFIXES)


def find_secret_keys(data: object, prefix: str = "") -> list[str]:
    """Return the dotted paths of every secret-looking key in a nested structure."""
    found: list[str] = []
    if isinstance(data, Mapping):
        for raw_key, value in cast("Mapping[object, object]", data).items():
            key = str(raw_key)
            path = f"{prefix}.{key}" if prefix else key
            if is_secret_key(key):
                found.append(path)
            found.extend(find_secret_keys(value, path))
    elif isinstance(data, (list, tuple)):
        items = cast("Sequence[object]", data)
        for index, item in enumerate(items):
            found.extend(find_secret_keys(item, f"{prefix}[{index}]"))
    return found


def redact(value: object) -> object:
    """Return a copy of ``value`` with every secret-keyed entry replaced.

    A copy, never an in-place mutation: the caller may have passed a live settings object or a
    dict shared with other code, and logging must not alter what it observes.
    """
    if isinstance(value, Mapping):
        return {
            key: REDACTED if is_secret_key(str(key)) else redact(item)
            for key, item in cast("Mapping[object, object]", value).items()
        }
    # str and bytes are Sequences but hold no keys of their own.
    if isinstance(value, (list, tuple, set)):
        entries = cast("Iterable[object]", value)
        return [redact(item) for item in entries]
    return value
