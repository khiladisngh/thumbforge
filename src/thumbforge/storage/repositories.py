"""Upsert and lookup for fetched YouTube metadata (ROADMAP P2.3, ADR 0004).

Repositories take `core.models` snapshots and reconcile them with ORM rows. Three rules
hold everywhere:

- **Identity is `youtube_id`.** An upsert never changes a row's ULID `id`, because runs,
  iterations and assets reference it. Re-fetching a video must not orphan its history.
- **Timestamps are ISO-8601 UTC strings**, matching the `String` columns in
  `storage/models.py`. Conversion happens here so services deal only in `datetime`.
- **User edits survive a re-fetch.** `playlist_item.part_number` is the only such field
  today: `playlist renumber` (P2.4) writes it and a later `fetch --refresh` must not
  silently revert it.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import select

from thumbforge.core.errors import NotFoundError
from thumbforge.core.services.fetch import StoredPlaylist
from thumbforge.storage.models import Channel, Playlist, PlaylistItem, Video

if TYPE_CHECKING:
    from collections.abc import Collection, Sequence

    from sqlalchemy.orm import Session

    from thumbforge.core.models import ChannelMeta, PlaylistMeta, VideoMeta


@dataclass(frozen=True, slots=True)
class Renumbering:
    """One item's `part_number` before and after a `playlist renumber`.

    Captured per item because the before value is gone once the row is mutated, and the
    command prints a before/after table (spec behaviour 5).
    """

    position: int
    youtube_id: str
    title: str
    before: int | None
    after: int | None


def _iso(moment: datetime) -> str:
    """Render an aware datetime as the ISO-8601 UTC string the schema stores."""
    return moment.isoformat()


class ChannelRepository:
    """Channel rows, keyed by YouTube channel id."""

    def __init__(self, session: Session) -> None:
        """Bind to the caller's session; the service owns the transaction."""
        self._session = session

    def get(self, youtube_id: str) -> Channel | None:
        """Return the row for a YouTube channel id, or `None`."""
        return self._session.scalars(
            select(Channel).where(Channel.youtube_id == youtube_id)
        ).one_or_none()

    def upsert(self, meta: ChannelMeta) -> Channel:
        """Insert or refresh a channel, preserving its ULID."""
        row = self.get(meta.youtube_id)
        if row is None:
            row = Channel(youtube_id=meta.youtube_id)
            self._session.add(row)
        row.title = meta.title
        row.url = meta.url
        row.source = meta.source
        row.fetched_at = _iso(meta.fetched_at)
        self._session.flush()
        return row

    def list(self) -> Sequence[Channel]:
        """Every channel, newest fetch first."""
        return self._session.scalars(select(Channel).order_by(Channel.fetched_at.desc())).all()


class VideoRepository:
    """Video rows, keyed by YouTube video id."""

    def __init__(self, session: Session) -> None:
        """Bind to the caller's session; the service owns the transaction."""
        self._session = session

    def get(self, youtube_id: str) -> Video | None:
        """Return the row for a YouTube video id, or `None`."""
        return self._session.scalars(
            select(Video).where(Video.youtube_id == youtube_id)
        ).one_or_none()

    def resolve(self, reference: str) -> Video:
        """Look a video up by ULID or YouTube id, raising `NotFoundError` if absent.

        Both are accepted because `video show` takes either, and a ULID is distinguishable
        from an 11-character YouTube id only by trying.
        """
        row = self._session.get(Video, reference) or self.get(reference)
        if row is None:
            msg = f"video {reference!r}"
            raise NotFoundError(msg, hint="run `thumbforge fetch <url>` first")
        return row

    def upsert(self, meta: VideoMeta, *, channel_row_id: str | None = None) -> Video:
        """Insert or refresh a video, preserving its ULID.

        `channel_row_id` is supplied only when the owning channel is already stored. A
        playlist can mix videos from many channels — the sampled 183-item playlist in spike
        S11 had a different `channel_id` on every entry — and fetching a channel per video
        would turn one request into hundreds. `video.channel_id` is nullable for exactly
        this reason, and stays `None` until that channel is fetched in its own right.
        """
        row = self.get(meta.youtube_id)
        if row is None:
            row = Video(youtube_id=meta.youtube_id)
            self._session.add(row)
        row.title = meta.title
        row.url = meta.url
        row.fetched_at = _iso(meta.fetched_at)
        if channel_row_id is not None:
            row.channel_id = channel_row_id
        # A flat playlist entry carries neither of these (S11), so an empty value means
        # "this extraction mode cannot tell", not "the video has no description". Keeping
        # the stored value avoids a playlist re-fetch wiping a full extract's richer data.
        if meta.description:
            row.description = meta.description
        if meta.published_at is not None:
            row.published_at = _iso(meta.published_at)
        if meta.duration_s is not None:
            row.duration_s = meta.duration_s
        if meta.source_thumbnail_url is not None:
            row.source_thumbnail_url = meta.source_thumbnail_url
        self._session.flush()
        return row

    def list(self, *, channel: str | None = None, limit: int | None = None) -> Sequence[Video]:
        """Videos, newest fetch first, optionally restricted to one channel."""
        statement = select(Video).order_by(Video.fetched_at.desc())
        if channel is not None:
            statement = statement.join(Channel).where(Channel.youtube_id == channel)
        if limit is not None:
            statement = statement.limit(limit)
        return self._session.scalars(statement).all()


class PlaylistRepository:
    """Playlist rows and their ordered items."""

    def __init__(self, session: Session) -> None:
        """Bind to the caller's session; the service owns the transaction."""
        self._session = session

    def get(self, youtube_id: str) -> Playlist | None:
        """Return the row for a YouTube playlist id, or `None`."""
        return self._session.scalars(
            select(Playlist).where(Playlist.youtube_id == youtube_id)
        ).one_or_none()

    def resolve(self, reference: str) -> Playlist:
        """Look a playlist up by ULID or YouTube id, raising `NotFoundError` if absent."""
        row = self._session.get(Playlist, reference) or self.get(reference)
        if row is None:
            msg = f"playlist {reference!r}"
            raise NotFoundError(msg, hint="run `thumbforge fetch <url>` first")
        return row

    def upsert(self, meta: PlaylistMeta, *, channel_row_id: str) -> Playlist:
        """Insert or refresh a playlist. `channel_row_id` is required: the column is NOT NULL.

        `item_count` is deliberately **not** written here. `replace_items` owns it, because
        it is the only place that knows how many rows were actually stored — which can be
        fewer than `meta.item_count`. Callers must follow an upsert with `replace_items`.
        """
        row = self.get(meta.youtube_id)
        if row is None:
            row = Playlist(youtube_id=meta.youtube_id)
            self._session.add(row)
        row.channel_id = channel_row_id
        row.title = meta.title
        row.description = meta.description
        row.url = meta.url
        row.fetched_at = _iso(meta.fetched_at)
        self._session.flush()
        return row

    def replace_items(self, playlist: Playlist, video_ids: Sequence[str]) -> int:
        """Rewrite a playlist's items to exactly `video_ids`, in order.

        Rows are deleted and re-inserted rather than updated in place. `playlist_item` has
        `UNIQUE(playlist_id, position)`, so shifting two videos past each other collides
        mid-update unless the writes are staged; nothing holds a foreign key to
        `playlist_item`, which makes replacement the simpler correct option.

        `part_number` is carried across by video id, so a `playlist renumber` survives a
        re-fetch. New rows default it to `position`, i.e. the first video is "Part 1"
        (`PLAN.md` §5.3).

        `playlist.item_count` is set from the rows written, not from the fetched entry
        count. A playlist that lists the same video twice yields fewer rows than entries
        (`UNIQUE(playlist_id, video_id)`), and taking the count from the snapshot would
        print "3 videos" above a two-row table.

        Returns the number of items removed, which `fetch` reports.
        """
        existing = {item.video_id: item for item in playlist.items}
        kept_parts = {
            video_id: (item.part_number, item.part_label) for video_id, item in existing.items()
        }
        removed = len(set(existing) - set(video_ids))

        for item in list(playlist.items):
            self._session.delete(item)
        # Without this the inserts below race the deletes and trip the unique constraints.
        self._session.flush()

        for position, video_id in enumerate(video_ids, start=1):
            part_number, part_label = kept_parts.get(video_id, (position, None))
            playlist.items.append(
                PlaylistItem(
                    video_id=video_id,
                    position=position,
                    part_number=part_number,
                    part_label=part_label,
                )
            )
        playlist.item_count = len(video_ids)
        self._session.flush()
        return removed

    def items(self, playlist: Playlist) -> Sequence[PlaylistItem]:
        """A playlist's items in playlist order."""
        return self._session.scalars(
            select(PlaylistItem)
            .where(PlaylistItem.playlist_id == playlist.id)
            .order_by(PlaylistItem.position)
        ).all()

    def renumber(
        self,
        playlist: Playlist,
        *,
        start: int = 1,
        skip_ids: Collection[str] = (),
    ) -> list[Renumbering]:
        """Reassign `part_number` sequentially from `start` in playlist order.

        Videos whose YouTube id is in `skip_ids` get `part_number = NULL` and are not
        counted, so the remaining parts stay consecutive — that is the point of skipping a
        trailer or an outro rather than deleting it from the playlist.

        An id in `skip_ids` that is not in this playlist raises `NotFoundError`. Ignoring it
        would be worse than failing: a mistyped id silently renumbers everything one step
        off, and the user would have no reason to look.

        Returns one record per item so the caller can print the before/after table.
        """
        items = self.items(playlist)
        skipped = set(skip_ids)
        present = {item.video.youtube_id for item in items}
        if unknown := sorted(skipped - present):
            msg = f"not in playlist {playlist.youtube_id}: {', '.join(unknown)}"
            raise NotFoundError(msg, hint="pass YouTube video ids from `playlist show --videos`")

        changes: list[Renumbering] = []
        next_part = start
        for item in items:
            before = item.part_number
            if item.video.youtube_id in skipped:
                item.part_number = None
            else:
                item.part_number = next_part
                next_part += 1
            changes.append(
                Renumbering(
                    position=item.position,
                    youtube_id=item.video.youtube_id,
                    title=item.video.title,
                    before=before,
                    after=item.part_number,
                )
            )
        self._session.flush()
        return changes

    def list(self, *, channel: str | None = None) -> Sequence[Playlist]:
        """Playlists, newest fetch first, optionally restricted to one channel."""
        statement = select(Playlist).order_by(Playlist.fetched_at.desc())
        if channel is not None:
            statement = statement.join(Channel).where(Channel.youtube_id == channel)
        return self._session.scalars(statement).all()


class Repositories:
    """The repository bundle services receive (`docs/specs/phase-6-hero.md`)."""

    def __init__(self, session: Session) -> None:
        """Build the three repositories over one session, so they share a transaction."""
        self.session = session
        self.channels = ChannelRepository(session)
        self.playlists = PlaylistRepository(session)
        self.videos = VideoRepository(session)

    def store_video(self, meta: VideoMeta, channel: ChannelMeta | None = None) -> Video:
        """Persist one video and, when known, its channel.

        A single-video fetch can afford the extra channel request, so `video.channel_id`
        gets populated on that path — unlike playlist items, where it would cost one
        request per video.
        """
        channel_row_id = None if channel is None else self.channels.upsert(channel).id
        return self.videos.upsert(meta, channel_row_id=channel_row_id)

    def store_playlist(self, meta: PlaylistMeta, channel: ChannelMeta) -> StoredPlaylist:
        """Persist a playlist, its owning channel, its videos and its item order.

        Reports what was *written* rather than returning the row: `item_count` can be lower
        than `meta.item_count` when the playlist repeats a video, and `fetch` must print the
        number its own table shows. Videos dropped from a playlist keep their own rows —
        their generated thumbnails are still real artefacts.
        """
        channel_row = self.channels.upsert(channel)
        playlist = self.playlists.upsert(meta, channel_row_id=channel_row.id)

        video_ids: list[str] = []
        for item in meta.items:
            owner = item.video.channel_id
            row_id = channel_row.id if owner == channel_row.youtube_id else None
            video_row = self.videos.upsert(item.video, channel_row_id=row_id)
            # UNIQUE(playlist_id, video_id): a playlist may legitimately list the same
            # video twice, but the schema cannot represent that, so the first place wins.
            if video_row.id not in video_ids:
                video_ids.append(video_row.id)

        removed = self.playlists.replace_items(playlist, video_ids)
        return StoredPlaylist(item_count=playlist.item_count, removed_items=removed)

    def store_channel(self, meta: ChannelMeta) -> Channel:
        """Persist a channel on its own (a channel URL was fetched)."""
        return self.channels.upsert(meta)

    def playlist_fetched_at(self, youtube_id: str) -> datetime | None:
        """When a stored playlist was last fetched, or `None` if it is not stored.

        Parsed back from the ISO-8601 column so the freshness rule in `FetchService` deals
        in `datetime`. A value written before timezones were enforced would be naive, so it
        is assumed UTC rather than allowed to poison an aware comparison.
        """
        row = self.playlists.get(youtube_id)
        if row is None:
            return None
        moment = datetime.fromisoformat(row.fetched_at)
        return moment if moment.tzinfo is not None else moment.replace(tzinfo=UTC)
