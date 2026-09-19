"""Secret detection shared by configuration loading and logging (ADR 0014).

One deny-list, used in two places: settings refuses to load a config file containing these keys,
and the log pipeline redacts them from event dictionaries. Keeping the tuple here means a key
that is a secret for one is a secret for the other.
"""

from __future__ import annotations

#: Key suffixes that mark a value as secret. Matched case-insensitively.
SECRET_SUFFIXES = ("_key", "_token", "_secret", "_password")

#: What a redacted value is replaced with.
REDACTED = "***redacted***"


def is_secret_key(key: str) -> bool:
    """Return whether ``key`` names a secret."""
    return key.lower().endswith(SECRET_SUFFIXES)
