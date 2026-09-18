"""Identifier and content-hash helpers.

ULIDs are used for primary keys: they sort by creation time, which makes ``runs list`` ordering
free and keeps SQLite indexes append-friendly, unlike random UUID4.
"""

from __future__ import annotations

import hashlib
import os
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

_CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
_READ_CHUNK = 1024 * 1024


def new_id() -> str:
    """Return a 26-character Crockford base32 ULID: 48-bit timestamp + 80 random bits."""
    value = (int(time.time() * 1000) << 80) | int.from_bytes(os.urandom(10), "big")
    return "".join(_CROCKFORD[(value >> shift) & 0x1F] for shift in range(125, -1, -5))


def sha256_bytes(data: bytes) -> str:
    """Return the hex SHA-256 of ``data``."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    """Return the hex SHA-256 of a file, read in chunks so large images stay off the heap."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(_READ_CHUNK):
            digest.update(chunk)
    return digest.hexdigest()
