"""Secret detection shared by configuration loading and logging (ADR 0014, ADR 0017).

One deny-list and one traversal, used two ways: settings *refuses* to load a config file
containing these keys, and the log pipeline *redacts* them from event dictionaries. A key that
is a secret for one is therefore a secret for the other.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from typing import Final, cast

#: Final word of a key that marks it secret: ``api_key``, ``apiKey``, ``X-API-KEY``.
SECRET_WORDS: Final[frozenset[str]] = frozenset(
    {"key", "token", "secret", "password", "passwd", "credentials", "credential"}
)

#: Whole keys that are secret but do not end in one of the words above.
SECRET_NAMES: Final[frozenset[str]] = frozenset(
    {"authorization", "auth", "cookie", "setcookie", "proxyauthorization"}
)

#: What a redacted value is replaced with. Replacing rather than dropping keeps the fact that a
#: field was present visible, which matters when triaging a log.
REDACTED: Final[str] = "***redacted***"

_WORD = re.compile(r"[A-Z]+(?![a-z])|[A-Z][a-z]*|[a-z]+|[0-9]+")


def _words(key: str) -> list[str]:
    """Split a key into lowercase words across separators and camelCase boundaries."""
    return [match.group().lower() for match in _WORD.finditer(key)]


def is_secret_key(key: str) -> bool:
    """Return whether ``key`` names a secret.

    Matching is on word boundaries, not raw suffixes, so naming style does not decide whether a
    credential is protected — ``Authorization``, ``apiKey``, ``api_key`` and ``X-API-KEY`` are
    all secret — while ordinary words that merely end in one are not: ``monkey`` is not a key.
    """
    words = _words(key)
    if not words:
        return False
    return "".join(words) in SECRET_NAMES or words[-1] in SECRET_WORDS


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
