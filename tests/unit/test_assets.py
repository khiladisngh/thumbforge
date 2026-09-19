"""Unit tests for content-addressed AssetStore (PLAN.md §3.2, ADR 0011)."""

from __future__ import annotations

import io
from typing import TYPE_CHECKING

import pytest
from PIL import Image

from thumbforge.core.enums import AssetKind
from thumbforge.storage.assets import AssetStore, AssetStoreError
from thumbforge.storage.db import get_engine, init_db, session_factory

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path


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
    with pytest.raises(AssetStoreError, match="Unsupported or corrupted image"):
        asset_store.put(b"not an image file at all", kind=AssetKind.RAW)

    # Tmp dir must be clean even after an error
    assert len(list(asset_store.tmp_dir.iterdir())) == 0


def test_put_missing_source_path_raises(asset_store: AssetStore, tmp_path: Path) -> None:
    non_existent = tmp_path / "does_not_exist.png"
    with pytest.raises(AssetStoreError, match="Source file does not exist"):
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

    with pytest.raises(AssetStoreError, match="Unsupported image format") as exc_info:
        asset_store.put(gif_bytes, kind=AssetKind.RAW)
    assert exc_info.value.hint is not None
    assert "JPEG, PNG, and WebP" in exc_info.value.hint
    assert len(list(asset_store.tmp_dir.iterdir())) == 0


def test_put_cleans_up_orphaned_file_on_insert_failure(
    asset_store: AssetStore, monkeypatch: pytest.MonkeyPatch
) -> None:
    png_data = _make_png_bytes(300, 300)

    # Cause an unexpected failure during DB insertion
    from contextlib import contextmanager

    original_scope = asset_store.session_factory

    call_count = 0

    @contextmanager
    def failing_session_scope(_factory):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # First call is deduplication check: allow it
            from thumbforge.storage.db import session_scope as real_scope

            with real_scope(original_scope) as s:
                yield s
        else:
            # Second call is row insert: simulate database write failure
            raise RuntimeError("simulated DB crash after replace")

    monkeypatch.setattr("thumbforge.storage.assets.session_scope", failing_session_scope)

    with pytest.raises(RuntimeError, match="simulated DB crash after replace"):
        asset_store.put(png_data, kind=AssetKind.FINAL)

    # No orphaned file should remain in assets_dir
    assert len(list(asset_store.assets_dir.glob("**/*.png"))) == 0
    assert len(list(asset_store.tmp_dir.iterdir())) == 0
