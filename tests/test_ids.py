"""ULIDs must be unique and time-sortable; hashes must match the content they address."""

from __future__ import annotations

import hashlib
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from thumbforge.core.ids import new_id, sha256_bytes, sha256_file


def test_ids_are_26_char_crockford_base32() -> None:
    value = new_id()
    assert len(value) == 26
    assert set(value) <= set("0123456789ABCDEFGHJKMNPQRSTVWXYZ")


def test_ids_are_unique() -> None:
    assert len({new_id() for _ in range(2000)}) == 2000


def test_ids_sort_by_creation_time() -> None:
    first = new_id()
    time.sleep(0.002)
    second = new_id()
    assert first < second


def test_sha256_file_matches_sha256_bytes(tmp_path: Path) -> None:
    data = b"thumbnail bytes" * 100_000  # larger than the 1 MiB read chunk
    target = tmp_path / "asset.bin"
    target.write_bytes(data)
    assert sha256_file(target) == sha256_bytes(data) == hashlib.sha256(data).hexdigest()
