"""The `MetadataSource` Protocol every metadata backend implements (ADR 0005).

A Protocol rather than a base class so `YtDlpSource` (P2.2) and the Phase 8 Data API
source stay independent implementations; `cli` selects one and everything else sees only
this shape. Methods are async because both implementations do network I/O — `yt_dlp` is
synchronous and is called through `asyncio.to_thread`.

It lives in `core` rather than in `sources/` because `core.services.fetch` consumes it and
`core` may not import `sources`. `docs/specs/phase-1-skeleton.md` anticipated this: *"If
`providers.base` must be importable from `core.services`, the Protocol moves to `core` —
the contract is the rule, the file placement bends."* The alternative was a second,
structurally identical Protocol inside `core`, which would drift from this one.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Protocol, runtime_checkable

if TYPE_CHECKING:
    from thumbforge.core.models import ChannelMeta, PlaylistMeta, ResolvedUrl, VideoMeta


@runtime_checkable
class MetadataSource(Protocol):
    """Fetch YouTube channel, playlist and video metadata."""

    #: Selector used by `--source`; matches `ChannelSource` and is stored on fetched rows.
    key: ClassVar[str]

    async def resolve(self, url: str) -> ResolvedUrl:
        """Classify a URL or bare identifier into its kind and YouTube id."""
        ...

    async def fetch_video(self, youtube_id: str) -> VideoMeta:
        """Fetch one video's metadata."""
        ...

    async def fetch_playlist(self, youtube_id: str) -> PlaylistMeta:
        """Fetch a playlist and its ordered items."""
        ...

    async def fetch_channel(self, youtube_id: str) -> ChannelMeta:
        """Fetch a channel's metadata."""
        ...
