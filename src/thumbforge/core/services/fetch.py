"""`FetchService` — resolve a YouTube URL, fetch it, persist it (ROADMAP P2.3).

The CLI contributes argument parsing and rendering only; the decisions live here:

- which `fetch_*` a URL kind maps to,
- whether a recent fetch can be served from the database instead of the network,
- which rows a fetch of each kind is responsible for.

Both collaborators arrive as Protocols so this module imports no adapter package. The
`MetadataSource` lives in `core.sources` for this reason. `FetchStore` is deliberately
narrow — the methods a fetch needs — rather than a mirror of `storage.Repositories`; a later
service declares whatever it needs.

Nothing here logs: the `core is pure` import contract forbids `core -> thumbforge.logging`,
and everything worth reporting (including whether the result was served from cache) is
already rendered by `cli/fetch.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Protocol

from thumbforge.core.enums import UrlKind
from thumbforge.core.errors import SourceError

if TYPE_CHECKING:
    from thumbforge.core.models import ChannelMeta, PlaylistMeta, ResolvedUrl, VideoMeta
    from thumbforge.core.sources import MetadataSource

#: How long a stored playlist is considered current (spec behaviour 2). A playlist gains
#: videos over days, not minutes, so re-fetching on every command would spend a network
#: round trip to learn nothing. `--refresh` always overrides it.
DEFAULT_MAX_AGE = timedelta(hours=24)


class FetchStore(Protocol):
    """The persistence surface a fetch needs, satisfied by `storage.Repositories`."""

    def store_video(self, meta: VideoMeta, channel: ChannelMeta | None = None) -> object:
        """Persist one video, and its channel when the caller fetched one."""
        ...

    def store_playlist(self, meta: PlaylistMeta, channel: ChannelMeta) -> tuple[object, int]:
        """Persist a playlist, its owner, its videos and its order; return items removed."""
        ...

    def store_channel(self, meta: ChannelMeta) -> object:
        """Persist a channel on its own."""
        ...

    def playlist_fetched_at(self, youtube_id: str) -> datetime | None:
        """When a stored playlist was last fetched, or `None` if it is not stored."""
        ...


@dataclass(frozen=True, slots=True)
class FetchResult:
    """What was fetched, for rendering and for the `--json` contract.

    Counts are of rows *written*, which is why `videos` is 1 for a video fetch and
    `len(items)` for a playlist: the caller reports "Stored 1 channel, 1 playlist, 12
    videos" (`PLAN.md` §5.3) and must not have to recount.

    `youtube_id` is always set, including on the cached path where no metadata was fetched,
    because the caller renders its table from the stored rows either way.
    """

    kind: UrlKind
    youtube_id: str
    channel: ChannelMeta | None = None
    playlist: PlaylistMeta | None = None
    video: VideoMeta | None = None
    cached: bool = False
    removed_items: int = 0

    @property
    def channels_stored(self) -> int:
        """Channel rows written."""
        return 0 if self.cached or self.channel is None else 1

    @property
    def playlists_stored(self) -> int:
        """Playlist rows written."""
        return 0 if self.cached or self.playlist is None else 1

    @property
    def videos_stored(self) -> int:
        """Video rows written."""
        if self.cached:
            return 0
        if self.playlist is not None:
            return self.playlist.item_count
        return 0 if self.video is None else 1


class FetchService:
    """Fetch YouTube metadata and persist it."""

    def __init__(
        self,
        source: MetadataSource,
        store: FetchStore,
        *,
        max_age: timedelta = DEFAULT_MAX_AGE,
    ) -> None:
        """Take the metadata source and persistence layer the CLI selected."""
        self._source = source
        self._store = store
        self._max_age = max_age

    async def fetch(self, url: str, *, refresh: bool = False) -> FetchResult:
        """Resolve `url`, fetch the thing it names, and store it."""
        resolved = await self._source.resolve(url)
        match resolved.kind:
            case UrlKind.VIDEO:
                return await self._fetch_video(resolved)
            case UrlKind.PLAYLIST:
                return await self._fetch_playlist(resolved, refresh=refresh)
            case UrlKind.CHANNEL:
                return await self._fetch_channel(resolved)

    async def _fetch_video(self, resolved: ResolvedUrl) -> FetchResult:
        """A single video, plus its channel when the video names one.

        The extra channel request is affordable for one video and it populates
        `video.channel_id`, which `video list --channel` needs.
        """
        video = await self._source.fetch_video(resolved.youtube_id)
        channel = None
        if video.channel_id:
            channel = await self._source.fetch_channel(video.channel_id)
        self._store.store_video(video, channel)
        return FetchResult(
            kind=UrlKind.VIDEO,
            youtube_id=video.youtube_id,
            video=video,
            channel=channel,
        )

    async def _fetch_playlist(self, resolved: ResolvedUrl, *, refresh: bool) -> FetchResult:
        """A playlist, its owning channel, its videos and its item order."""
        if not refresh and self._is_fresh(resolved.youtube_id):
            return FetchResult(kind=UrlKind.PLAYLIST, youtube_id=resolved.youtube_id, cached=True)

        playlist = await self._source.fetch_playlist(resolved.youtube_id)
        if not playlist.channel_id:
            # `playlist.channel_id` is NOT NULL, so there is no row to write without it.
            # Failing here beats inventing a placeholder channel that later fetches would
            # have to reconcile.
            msg = f"playlist {resolved.youtube_id} reports no owning channel"
            raise SourceError(msg, hint="re-run with --refresh, or check the playlist is public")

        channel = await self._source.fetch_channel(playlist.channel_id)
        _, removed = self._store.store_playlist(playlist, channel)
        return FetchResult(
            kind=UrlKind.PLAYLIST,
            youtube_id=playlist.youtube_id,
            playlist=playlist,
            channel=channel,
            removed_items=removed,
        )

    async def _fetch_channel(self, resolved: ResolvedUrl) -> FetchResult:
        """A channel on its own; enumerating its videos is a Phase 2 non-goal."""
        channel = await self._source.fetch_channel(resolved.youtube_id)
        self._store.store_channel(channel)
        return FetchResult(kind=UrlKind.CHANNEL, youtube_id=channel.youtube_id, channel=channel)

    def _is_fresh(self, youtube_id: str) -> bool:
        """Whether a stored playlist is recent enough to skip the network."""
        fetched_at = self._store.playlist_fetched_at(youtube_id)
        if fetched_at is None:
            return False
        return datetime.now(UTC) - fetched_at < self._max_age
