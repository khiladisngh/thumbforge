"""Content-addressed local image asset store (PLAN.md §3.2, ADR 0011)."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from PIL import Image, UnidentifiedImageError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from thumbforge.core.errors import AssetError
from thumbforge.core.ids import new_id, sha256_file
from thumbforge.storage.db import session_scope
from thumbforge.storage.models import Asset

if TYPE_CHECKING:
    from sqlalchemy.orm import Session, sessionmaker

    from thumbforge.core.enums import AssetKind

_MIME_TO_EXT: dict[str, str] = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
}


def _fsync_dir(path: Path) -> None:
    """Flush a directory entry to disk so a publication survives power loss.

    Fsyncing the file itself does not make its *directory entry* durable on POSIX, so
    without this a crash could drop a freshly linked asset while its row survives.
    Windows cannot open a directory for fsync, so this is a best-effort no-op there.
    """
    try:
        fd = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(fd)
    except OSError:
        pass  # platform does not support directory fsync
    finally:
        os.close(fd)


class AssetStore:
    """Content-addressed storage for thumbnail iterations, raw art, and style references."""

    def __init__(self, data_dir: Path, session_factory: sessionmaker[Session]) -> None:
        self.data_dir = data_dir
        self.assets_dir = data_dir / "assets"
        self.tmp_dir = data_dir / "tmp"
        self.session_factory = session_factory

    def put(self, src: bytes | Path, kind: AssetKind) -> Asset:
        """Store an image file or bytes content-addressed by SHA-256.

        If identical content already exists, returns the existing Asset row without
        rewriting the file. If src is a Path, the source file is never moved or deleted.
        """
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        tmp_path = self.tmp_dir / new_id()

        try:
            # 1. Write to temporary location and fsync
            if isinstance(src, Path):
                if not src.exists():
                    msg = f"Source file does not exist: {src}"
                    raise AssetError(msg)
                with src.open("rb") as src_f, tmp_path.open("wb") as dst_f:
                    shutil.copyfileobj(src_f, dst_f)
                    dst_f.flush()
                    os.fsync(dst_f.fileno())
            else:
                with tmp_path.open("wb") as f:
                    f.write(src)
                    f.flush()
                    os.fsync(f.fileno())

            # 2. Sniff image metadata with Pillow
            try:
                with Image.open(tmp_path) as img:
                    format_name = img.format or ""
                    mime = Image.MIME.get(format_name, f"image/{format_name.lower()}")
                    width, height = img.size
            except UnidentifiedImageError as exc:
                msg = f"Unsupported or corrupted image format: {exc}"
                raise AssetError(msg) from exc

            ext = _MIME_TO_EXT.get(mime)
            if ext is None:
                msg = (
                    f"Unsupported image format {mime!r}; expected one of "
                    f"{sorted(_MIME_TO_EXT.keys())}"
                )
                raise AssetError(msg, hint="only JPEG, PNG, and WebP images are supported")

            sha256 = sha256_file(tmp_path)
            file_bytes = tmp_path.stat().st_size

            # 3. Deduplication check against DB
            with session_scope(self.session_factory) as session:
                existing = session.scalar(select(Asset).where(Asset.sha256 == sha256))
                if existing is not None:
                    return existing

            # 4. Publish at assets/<sha256[:2]>/<sha256>.<ext>.
            # The path is content-addressed, so any pre-existing target holds byte-identical
            # content: `link` (create-only) and the `replace` fallback are both safe, and a
            # concurrent publication is never a conflict. A published file is NEVER unlinked
            # here — another invocation may already reference it — so orphans left by a crash
            # between publication and insert are reclaimed by `db vacuum` (ADR 0011).
            bucket_dir = self.assets_dir / sha256[:2]
            bucket_dir.mkdir(parents=True, exist_ok=True)
            target_path = bucket_dir / f"{sha256}.{ext}"

            try:
                os.link(tmp_path, target_path)
            except FileExistsError:
                pass  # already published by a concurrent call; identical bytes
            except OSError:
                # Hard links unsupported on this filesystem: atomic rename of the
                # already-fsynced temp file, so the target is never partially written.
                tmp_path.replace(target_path)

            _fsync_dir(bucket_dir)

            rel_path = target_path.relative_to(self.data_dir).as_posix()

            # 5. Persist Asset row
            asset = Asset(
                sha256=sha256,
                rel_path=rel_path,
                mime=mime,
                width=width,
                height=height,
                bytes=file_bytes,
                kind=kind,
                compliant=None,
                compliance_report_json=None,
            )
            try:
                with session_scope(self.session_factory) as session:
                    session.add(asset)
            except IntegrityError:
                # A concurrent call won the `sha256` unique constraint; adopt its row.
                with session_scope(self.session_factory) as session:
                    existing = session.scalar(select(Asset).where(Asset.sha256 == sha256))
                    if existing is not None:
                        return existing
                raise

            return asset
        finally:
            tmp_path.unlink(missing_ok=True)

    def path_for(self, asset: Asset) -> Path:
        """Return the absolute path on disk for ``asset``."""
        return self.data_dir / asset.rel_path

    def verify(self, asset: Asset) -> bool:
        """Re-hash the file on disk and report whether it matches ``asset.sha256``."""
        path = self.path_for(asset)
        if not path.is_file():
            return False
        return sha256_file(path) == asset.sha256
