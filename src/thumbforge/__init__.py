"""thumbforge: consistent, spec-compliant YouTube thumbnails from a hero image and a playlist."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("thumbforge")
except PackageNotFoundError:  # pragma: no cover - only when running from an unbuilt checkout
    __version__ = "0.0.0"

__all__ = ["__version__"]
