"""ULIDs must be unique and time-sortable; hashes must match the content they address."""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

from thumbforge.core import ids

if TYPE_CHECKING:
    from pathlib import Path

    import pytest


def test_ids_are_26_char_crockford_base32() -> None:
    value = ids.new_id()
    assert len(value) == 26
    assert set(value) <= set("0123456789ABCDEFGHJKMNPQRSTVWXYZ")


def test_ids_are_unique() -> None:
    assert len({ids.new_id() for _ in range(2000)}) == 2000


def test_ids_sort_by_creation_time(monkeypatch: pytest.MonkeyPatch) -> None:
    """`runs list` orders by id, so a later id must sort after an earlier one."""
    monkeypatch.setattr(ids.time, "time", lambda: 1_000_000.0)
    earlier = ids.new_id()
    monkeypatch.setattr(ids.time, "time", lambda: 1_000_001.0)
    later = ids.new_id()
    assert earlier < later


def test_sha256_file_matches_sha256_bytes(tmp_path: Path) -> None:
    data = b"thumbnail bytes" * 100_000  # larger than the 1 MiB read chunk
    target = tmp_path / "asset.bin"
    target.write_bytes(data)
    assert ids.sha256_file(target) == ids.sha256_bytes(data) == hashlib.sha256(data).hexdigest()
