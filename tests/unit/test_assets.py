"""Unit tests for content-addressed AssetStore (PLAN.md §3.2, ADR 0011)."""

from __future__ import annotations

import io
import os
import time
from contextlib import contextmanager
from typing import TYPE_CHECKING

import pytest
from PIL import Image

from thumbforge.core.enums import AssetKind
from thumbforge.core.errors import AssetError, DatabaseError
from thumbforge.storage.assets import AssetStore
from thumbforge.storage.db import (
    get_engine,
    init_db,
    session_factory,
    session_scope,
    vacuum_db,
)

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

    from sqlalchemy.orm import Session, sessionmaker


def _backdate(*paths: Path, age_seconds: float = 7200) -> None:
    """Age files past the vacuum grace window without sleeping."""
    stamp = time.time() - age_seconds
    for path in paths:
        os.utime(path, (stamp, stamp))


def _make_png_bytes(
    width: int = 1920, height: int = 1080, color: tuple[int, int, int] = (255, 0, 0)
) -> bytes:
    """Generate synthetic PNG image bytes for testing."""
    img = Image.new("RGB", (width, height), color=color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _make_jpeg_bytes(
    width: int = 1280, height: int = 720, color: tuple[int, int, int] = (0, 255, 0)
) -> bytes:
    """Generate synthetic JPEG image bytes for testing."""
    img = Image.new("RGB", (width, height), color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


@pytest.fixture
def asset_store(tmp_path: Path) -> Generator[AssetStore]:
    """Provide an initialized AssetStore backed by a temporary SQLite database."""
    data_dir = tmp_path / "data"
    db_path = data_dir / "thumbforge.sqlite3"
    init_db(db_path)
    engine = get_engine(db_path)
    factory = session_factory(engine)
    try:
        yield AssetStore(data_dir=data_dir, session_factory=factory)
    finally:
        engine.dispose()


def test_put_bytes_and_deduplication(asset_store: AssetStore) -> None:
    raw_png = _make_png_bytes(1920, 1080)

    # 1. First put: stores file and creates row
    asset1 = asset_store.put(raw_png, kind=AssetKind.RAW)
    assert asset1.id is not None
    assert asset1.mime == "image/png"
    assert asset1.width == 1920
    assert asset1.height == 1080
    assert asset1.bytes == len(raw_png)
    assert asset1.rel_path.startswith("assets/")
    assert asset1.rel_path.endswith(".png")

    # Verify physical file
    stored_path = asset_store.path_for(asset1)
    assert stored_path.is_file()
    assert stored_path.read_bytes() == raw_png

    # Verify tmp directory is clean afterwards
    tmp_files = list(asset_store.tmp_dir.iterdir())
    assert len(tmp_files) == 0

    # 2. Second put with identical bytes: returns existing asset row
    asset2 = asset_store.put(raw_png, kind=AssetKind.FINAL)
    assert asset2.id == asset1.id
    assert asset2.sha256 == asset1.sha256
    assert asset2.rel_path == asset1.rel_path
    assert len(list(asset_store.tmp_dir.iterdir())) == 0


def test_put_path_source_never_moved_or_deleted(asset_store: AssetStore, tmp_path: Path) -> None:
    src_file = tmp_path / "original_source.jpg"
    jpeg_data = _make_jpeg_bytes(1280, 720)
    src_file.write_bytes(jpeg_data)

    asset = asset_store.put(src_file, kind=AssetKind.FINAL)

    # Original source file must still exist and be identical
    assert src_file.exists()
    assert src_file.read_bytes() == jpeg_data

    # Target asset exists in store
    target = asset_store.path_for(asset)
    assert target.is_file()
    assert target.read_bytes() == jpeg_data
    assert asset.mime == "image/jpeg"
    assert asset.rel_path.endswith(".jpg")

    # Tmp dir must be clean
    assert len(list(asset_store.tmp_dir.iterdir())) == 0


def test_verify_detects_drift_and_missing_file(asset_store: AssetStore) -> None:
    png_data = _make_png_bytes(640, 480)
    asset = asset_store.put(png_data, kind=AssetKind.PREVIEW)

    # Initial verification passes
    assert asset_store.verify(asset) is True

    # Tamper with file on disk
    target = asset_store.path_for(asset)
    target.write_bytes(b"corrupted image bytes")

    # Drift is detected
    assert asset_store.verify(asset) is False

    # Delete file completely
    target.unlink()
    assert asset_store.verify(asset) is False


def test_put_corrupted_or_non_image_raises(asset_store: AssetStore) -> None:
    with pytest.raises(AssetError, match="Unsupported or corrupted image"):
        asset_store.put(b"not an image file at all", kind=AssetKind.RAW)

    # Tmp dir must be clean even after an error
    assert len(list(asset_store.tmp_dir.iterdir())) == 0


def test_put_missing_source_path_raises(asset_store: AssetStore, tmp_path: Path) -> None:
    non_existent = tmp_path / "does_not_exist.png"
    with pytest.raises(AssetError, match="Source file does not exist"):
        asset_store.put(non_existent, kind=AssetKind.RAW)

    assert len(list(asset_store.tmp_dir.iterdir())) == 0


def test_put_extension_derived_from_sniffed_mime_not_filename(
    asset_store: AssetStore, tmp_path: Path
) -> None:
    # File has .jpg extension but contains PNG bytes
    misleading_path = tmp_path / "sneaky.jpg"
    png_data = _make_png_bytes(800, 600)
    misleading_path.write_bytes(png_data)

    asset = asset_store.put(misleading_path, kind=AssetKind.RAW)
    assert asset.mime == "image/png"
    assert asset.rel_path.endswith(".png")
    assert asset_store.path_for(asset).suffix == ".png"


def test_put_unsupported_mime_raises(asset_store: AssetStore) -> None:
    # Create a valid GIF image (not in JPEG/PNG/WebP allowlist)
    img = Image.new("P", (100, 100))
    buf = io.BytesIO()
    img.save(buf, format="GIF")
    gif_bytes = buf.getvalue()

    with pytest.raises(AssetError, match="Unsupported image format") as exc_info:
        asset_store.put(gif_bytes, kind=AssetKind.RAW)
    assert exc_info.value.hint is not None
    assert "JPEG, PNG, and WebP" in exc_info.value.hint
    assert len(list(asset_store.tmp_dir.iterdir())) == 0


def test_put_leaves_published_file_for_vacuum_on_insert_failure(
    asset_store: AssetStore, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A failed insert never unlinks the published file, and a retry adopts it.

    A published path is content-addressed and may already be referenced by a concurrent
    call, so `put` must not delete it; ADR 0011 assigns orphan reclamation to `db vacuum`.
    """
    png_data = _make_png_bytes(300, 300)
    real_scope = session_scope
    calls = 0

    @contextmanager
    def failing_session_scope(factory: sessionmaker[Session]) -> Generator[Session]:
        nonlocal calls
        calls += 1
        if calls == 1:  # the deduplication query
            with real_scope(factory) as session:
                yield session
        else:  # the row insert
            raise RuntimeError("simulated DB crash after publication")

    monkeypatch.setattr("thumbforge.storage.assets.session_scope", failing_session_scope)
    with pytest.raises(RuntimeError, match="simulated DB crash after publication"):
        asset_store.put(png_data, kind=AssetKind.FINAL)

    orphans = list(asset_store.assets_dir.glob("**/*.png"))
    assert len(orphans) == 1, "published file must survive for db vacuum to reclaim"
    assert orphans[0].read_bytes() == png_data
    assert len(list(asset_store.tmp_dir.iterdir())) == 0

    # Retrying with a working session adopts the orphan rather than failing on it.
    monkeypatch.undo()
    asset = asset_store.put(png_data, kind=AssetKind.FINAL)
    assert asset_store.path_for(asset) == orphans[0]
    assert asset_store.verify(asset) is True


def test_vacuum_reclaims_expired_orphans_and_spares_referenced_files(
    asset_store: AssetStore, tmp_path: Path
) -> None:
    """`db vacuum` deletes expired unreferenced files and stale tmp entries (ADR 0011)."""
    kept = asset_store.put(_make_png_bytes(120, 120), kind=AssetKind.FINAL)
    kept_path = asset_store.path_for(kept)

    # An orphan with no asset row, and a leftover temp file from a crashed write.
    orphan = asset_store.assets_dir / "ab" / f"{'ab' * 32}.png"
    orphan.parent.mkdir(parents=True, exist_ok=True)
    orphan.write_bytes(b"orphaned bytes")
    stale_tmp = asset_store.tmp_dir / "01ABCDEF"
    stale_tmp.write_bytes(b"interrupted write")

    # Backdate past the default window; a zero/negative grace is rejected outright.
    _backdate(orphan, stale_tmp)
    reclaimed = vacuum_db(tmp_path / "data" / "thumbforge.sqlite3")

    assert reclaimed == 2
    assert not orphan.exists()
    assert not stale_tmp.exists()
    assert kept_path.is_file(), "a referenced asset file must never be reclaimed"
    assert asset_store.verify(kept) is True


def test_vacuum_spares_files_inside_the_grace_window(
    asset_store: AssetStore, tmp_path: Path
) -> None:
    """A file from an in-flight `put` is newer than the grace age, so vacuum leaves it.

    `put` publishes before it inserts, so a just-published file is legitimately
    unreferenced; reclaiming it would strand the row the caller is about to commit.
    """
    in_flight = asset_store.assets_dir / "cd" / f"{'cd' * 32}.png"
    in_flight.parent.mkdir(parents=True, exist_ok=True)
    in_flight.write_bytes(b"just published, row not committed yet")
    asset_store.tmp_dir.mkdir(parents=True, exist_ok=True)
    fresh_tmp = asset_store.tmp_dir / "01INFLIGHT"
    fresh_tmp.write_bytes(b"mid-write")

    reclaimed = vacuum_db(tmp_path / "data" / "thumbforge.sqlite3")

    assert reclaimed == 0
    assert in_flight.is_file()
    assert fresh_tmp.is_file()


@pytest.mark.parametrize("grace", [0, -1.0])
def test_vacuum_rejects_non_positive_grace(tmp_path: Path, grace: float) -> None:
    """A non-positive window would let vacuum delete an in-flight write's files."""
    db_path = tmp_path / "data" / "thumbforge.sqlite3"
    init_db(db_path)
    with pytest.raises(DatabaseError, match="grace_seconds must be positive"):
        vacuum_db(db_path, grace_seconds=grace)
