"""Domain enumerations for thumbforge lifecycle and data classification (PLAN.md §3)."""

from __future__ import annotations

from enum import StrEnum


class ChannelSource(StrEnum):
    """Origin of channel metadata."""

    YTDLP = "ytdlp"
    API = "api"


class UrlKind(StrEnum):
    """What a YouTube URL or bare identifier refers to."""

    VIDEO = "video"
    PLAYLIST = "playlist"
    CHANNEL = "channel"


class RunKind(StrEnum):
    """Lifecycle classification of a thumbnail generation run."""

    HERO = "hero"
    ITERATE = "iterate"
    BATCH = "batch"


class RunStatus(StrEnum):
    """Execution status for runs and iterations."""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AssetKind(StrEnum):
    """Functional role of a stored image asset."""

    RAW = "raw"
    FINAL = "final"
    REFERENCE = "reference"
    PREVIEW = "preview"
