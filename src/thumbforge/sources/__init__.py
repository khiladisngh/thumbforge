"""Metadata sources: YouTube metadata providers behind one Protocol (ADR 0005)."""

from thumbforge.sources.base import MetadataSource
from thumbforge.sources.ytdlp import YtDlpSource

__all__ = ["MetadataSource", "YtDlpSource"]
