"""`YtDlpSource` — YouTube metadata via `yt-dlp`, no API key (ADR 0005, ROADMAP P2.2).

All knowledge of `yt_dlp` lives in `_extract_with_ytdlp` and `_translate`: the source itself
only turns raw info dicts into `core.models` values. That split is what lets the unit tests
replay recorded fixtures without a network call or a `yt_dlp` import, and it keeps the
exception mapping in one place.

Field availability is not guesswork — it was measured against a live 183-item playlist in
spike S11 (`docs/spikes/ytdlp.md`). The two findings that shape this module:

- `playlist_index` does **not** exist on flat entries, so `position` comes from enumeration
  order.
- `description` is **absent** and `timestamp` is present-but-`None` on flat entries, so a
  playlist fetch cannot fill `description` or `published_at`. It must not fan out one full
  extract per item to get them; `fetch_video` does the deep extract for a single video.
"""

from __future__ import annotations

import asyncio
import logging
from contextlib import contextmanager
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, ClassVar, Final, cast

from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

from thumbforge.core.enums import ChannelSource
from thumbforge.core.errors import (
    NotFoundError,
    SourceError,
    SourceTransientError,
    ThumbforgeError,
)
from thumbforge.core.models import ChannelMeta, PlaylistItemMeta, PlaylistMeta, VideoMeta
from thumbforge.core.urls import classify_url
from thumbforge.logging import get_logger

if TYPE_CHECKING:
    from collections.abc import Callable, Generator, Iterator, Mapping

    from tenacity import RetryCallState

    from thumbforge.core.models import ResolvedUrl

log = get_logger(__name__)

#: A raw yt-dlp info dict. Values are `Any` because each one is validated on the way out.
type RawInfo = Mapping[str, Any]
#: `(url, flat, items) -> info`, where `items` is a yt-dlp `playlist_items` selector or
#: `None` for "all". Injected so tests replay fixtures instead of hitting the network.
type Extractor = Callable[[str, bool, str | None], RawInfo]

_WATCH_URL: Final = "https://www.youtube.com/watch?v={}"
_PLAYLIST_URL: Final = "https://www.youtube.com/playlist?list={}"
_CHANNEL_URL: Final = "https://www.youtube.com/channel/{}"
_HANDLE_URL: Final = "https://www.youtube.com/{}"

#: HTTP statuses worth another attempt: 429 is YouTube throttling, 5xx is YouTube being down.
_RETRY_STATUSES: Final = frozenset({429, 500, 502, 503, 504})

# PLAN.md §7.2: exponential backoff base 2s, factor 2, max 60s, jitter, 3 attempts.
_RETRY_ATTEMPTS: Final = 3
_RETRY_WAIT: Final = wait_exponential_jitter(initial=2.0, exp_base=2.0, max=60.0, jitter=2.0)


def _extract_with_ytdlp(url: str, flat: bool, items: str | None = None) -> RawInfo:
    """Run a real `yt_dlp` extraction and translate its failures.

    `yt_dlp` is imported lazily: it is a heavy import that drags in its own networking
    stack, and `thumbforge db status` must not pay for it.
    """
    import yt_dlp

    options: dict[str, Any] = {
        "quiet": True,
        "skip_download": True,
        "no_warnings": True,
        # `quiet` does not silence errors: yt-dlp still writes "ERROR: ..." straight to
        # stderr, which would interleave with Rich output on stdout. Handing it a stdlib
        # logger routes those records through the structlog pipeline instead (PLAN.md §7.3),
        # where they are rendered like any other log line and stay off stdout.
        "logger": logging.getLogger("yt_dlp"),
    }
    if flat:
        # "in_playlist" yields one flat entry per item instead of a full extract each.
        options["extract_flat"] = "in_playlist"
    if items is not None:
        options["playlist_items"] = items

    try:
        with yt_dlp.YoutubeDL(cast("Any", options)) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as exc:
        raise _translate(exc, url) from exc
    if not info:
        msg = f"yt-dlp returned no metadata for {url}"
        raise SourceError(msg, hint="the id may be unavailable; try the URL in a browser")
    return info


def _translate(exc: Exception, url: str) -> SourceError | NotFoundError:
    """Map a `yt_dlp` exception onto the thumbforge error hierarchy.

    Measured against yt-dlp 2026.08.19 rather than assumed: `extract_info` wraps everything
    in `DownloadError` and stashes the original in `exc_info[1]`. An unavailable or private
    video arrives as `ExtractorError` with `expected=True`; a network failure arrives as a
    `TransportError` subclass.
    """
    from yt_dlp.networking.exceptions import HTTPError, TransportError
    from yt_dlp.utils import DownloadError, ExtractorError

    inner: BaseException = exc
    if isinstance(exc, DownloadError) and exc.exc_info:
        inner = exc.exc_info[1]

    message = str(inner) or str(exc)

    # A network failure may arrive already wrapped: yt-dlp's top-level extractor handler
    # raises `ExtractorError("A network error has occurred.", cause=e, expected=True)`.
    # Trusting `expected` before looking at the cause would report a retryable network
    # failure as a missing video — exit 3 with no retries.
    for link in _cause_chain(inner):
        if isinstance(link, TransportError):
            return SourceTransientError(f"network error fetching {url}: {message}")
        if isinstance(link, HTTPError) and link.status in _RETRY_STATUSES:
            return SourceTransientError(f"HTTP {link.status} fetching {url}: {message}")

    if isinstance(inner, ExtractorError) and inner.expected:
        # yt-dlp's own flag for "YouTube told us this, it is not a bug": unavailable,
        # private, removed, geo-restricted. All mean "you cannot have this id".
        return NotFoundError(message, hint="check the id is public and still exists")
    return SourceError(f"yt-dlp failed for {url}: {message}")


def _cause_chain(exc: BaseException, limit: int = 5) -> Iterator[BaseException]:
    """Yield `exc` and its `cause` links; `ExtractorError` nests the real failure there.

    Bounded because `cause` is an ordinary attribute yt-dlp sets, not the `__cause__`
    Python manages, so nothing guarantees the chain is acyclic.
    """
    seen: list[int] = []
    current: BaseException | None = exc
    while current is not None and len(seen) < limit and id(current) not in seen:
        seen.append(id(current))
        yield current
        nxt = getattr(current, "cause", None)
        current = nxt if isinstance(nxt, BaseException) else None


@contextmanager
def _shape_errors(url: str) -> Generator[None]:
    """Turn an unexpected yt-dlp info-dict *shape* into a `SourceError`.

    yt-dlp parses whatever YouTube currently serves, so a schema change upstream can hand
    back a value of the wrong type. Without this, a `TypeError`/`AttributeError` from the
    mapping escapes `handle_errors` — which only catches `ThumbforgeError` — and the user
    sees a traceback instead of a diagnosable error.

    This deliberately guards the boundary rather than modelling it: a Pydantic schema
    mirroring yt-dlp's ~40-key info dict would have to be maintained against every upstream
    release, and would reject shapes that are merely unfamiliar rather than actually
    unusable. The fields that matter are already validated by the `core.models` they flow
    into.
    """
    try:
        yield
    except ThumbforgeError:
        raise
    except (AttributeError, LookupError, TypeError, ValueError) as exc:
        msg = f"unexpected metadata shape from {url}: {exc}"
        raise SourceError(msg, hint="yt-dlp may need upgrading for a YouTube change") from exc


def _text(info: RawInfo, key: str) -> str:
    """Read a string field, treating a missing key and an explicit `None` alike.

    Both cases occur: spike S11 measured `description` as an absent key and `timestamp` as
    a present-but-`None` one, so callers must not distinguish them.
    """
    value = info.get(key)
    return value if isinstance(value, str) else ""


def _published_at(info: RawInfo) -> datetime | None:
    """Recover an upload instant from `timestamp`, or `None` if yt-dlp reported none.

    Flat playlist entries always carry `timestamp: None` (S11), so every playlist-sourced
    video gets `None` here; only a full extract has the value.
    """
    timestamp = info.get("timestamp")
    if isinstance(timestamp, (int, float)) and not isinstance(timestamp, bool):
        return datetime.fromtimestamp(timestamp, tz=UTC)
    return None


def _duration(info: RawInfo) -> int | None:
    """Read `duration` as whole seconds.

    Flat and full extracts disagree by up to a second for the same video (S11), so this
    truncates rather than rounds, keeping one extraction mode's answer stable.
    """
    duration = info.get("duration")
    if isinstance(duration, (int, float)) and not isinstance(duration, bool) and duration >= 0:
        return int(duration)
    return None


def _thumbnail_url(info: RawInfo) -> str | None:
    """Pick the largest thumbnail yt-dlp reported.

    A full extract supplies `thumbnail` (maxresdefault). A flat entry supplies only
    `thumbnails`, which S11 measured as topping out at 336x188, so a playlist-sourced row
    stores a small URL. The conventional `maxresdefault.jpg` URL is deliberately *not*
    synthesised: it 404s for videos that never had one, and storing a URL that may not
    resolve is worse than storing the small one that does.
    """
    direct = info.get("thumbnail")
    if isinstance(direct, str) and direct:
        return direct
    best: str | None = None
    best_area = -1
    for entry in info.get("thumbnails") or ():
        url = entry.get("url")
        if not isinstance(url, str) or not url:
            continue
        area = int(entry.get("width") or 0) * int(entry.get("height") or 0)
        if area >= best_area:
            best, best_area = url, area
    return best


def _video_meta(info: RawInfo) -> VideoMeta:
    """Build a `VideoMeta` from either a full extract or a flat playlist entry."""
    youtube_id = _text(info, "id")
    if not youtube_id:
        msg = "yt-dlp entry has no video id"
        raise SourceError(msg, hint="the playlist may contain a deleted video")
    url = _text(info, "webpage_url") or _text(info, "url") or _WATCH_URL.format(youtube_id)
    return VideoMeta(
        youtube_id=youtube_id,
        title=_text(info, "title"),
        url=url,
        channel_id=_text(info, "channel_id") or None,
        description=_text(info, "description"),
        duration_s=_duration(info),
        published_at=_published_at(info),
        source_thumbnail_url=_thumbnail_url(info),
    )


class YtDlpSource:
    """Fetch YouTube metadata with `yt-dlp` (a `MetadataSource` implementation)."""

    key: ClassVar[str] = ChannelSource.YTDLP.value

    def __init__(
        self, extract: Extractor | None = None, *, attempts: int = _RETRY_ATTEMPTS
    ) -> None:
        """Wire the extractor: tests pass a fixture-backed one, production gets yt-dlp."""
        self._extract: Extractor = extract if extract is not None else _extract_with_ytdlp
        self._attempts = attempts

    async def resolve(self, url: str) -> ResolvedUrl:
        """Classify input without touching the network; `core.urls` does the work."""
        return classify_url(url)

    async def fetch_video(self, youtube_id: str) -> VideoMeta:
        """Full extract of one video, so `description` and `published_at` are populated."""
        url = _WATCH_URL.format(youtube_id)
        info = await self._info(url, flat=False)
        with _shape_errors(url):
            return _video_meta(info)

    async def fetch_playlist(self, youtube_id: str) -> PlaylistMeta:
        """Flat extract of a playlist and its items, in playlist order.

        One network round trip for the whole playlist. `position` is a 1-based enumeration
        index because `playlist_index` is absent under `extract_flat` (S11). Unfetchable
        entries — yt-dlp yields `None` for a deleted video — are dropped *before*
        numbering, so positions stay contiguous instead of developing holes.
        """
        url = _PLAYLIST_URL.format(youtube_id)
        info = await self._info(url, flat=True)
        with _shape_errors(url):
            entries = [entry for entry in info.get("entries") or () if entry]
            items = tuple(
                PlaylistItemMeta(video=_video_meta(entry), position=position)
                for position, entry in enumerate(entries, start=1)
            )
            return PlaylistMeta(
                youtube_id=_text(info, "id") or youtube_id,
                title=_text(info, "title"),
                url=_text(info, "webpage_url") or url,
                channel_id=_text(info, "channel_id") or None,
                description=_text(info, "description"),
                items=items,
            )

    async def fetch_channel(self, youtube_id: str) -> ChannelMeta:
        """Channel metadata only — never its video list.

        Enumerating a channel is a non-goal of this phase and is also expensive, so the
        request pins `playlist_items` to none: YouTube then returns the channel's own
        fields and zero entries (measured at ~1.3s against a 183-video channel).

        yt-dlp does report a channel `description`, but the `channel` table has no column
        for it (`PLAN.md` §3), so it is dropped rather than carried in a model field with
        nowhere to persist.
        """
        url = (
            _CHANNEL_URL.format(youtube_id)
            if youtube_id.startswith("UC")
            else _HANDLE_URL.format(youtube_id)
        )
        info = await self._info(url, flat=True, items="0")
        with _shape_errors(url):
            return ChannelMeta(
                youtube_id=_text(info, "channel_id") or _text(info, "id") or youtube_id,
                title=_text(info, "title") or _text(info, "channel"),
                url=_text(info, "channel_url") or _text(info, "webpage_url") or url,
            )

    async def _info(self, url: str, *, flat: bool, items: str | None = None) -> RawInfo:
        """Extract off the event loop, retrying only transient failures (PLAN.md §7.2)."""
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(self._attempts),
            wait=_RETRY_WAIT,
            retry=retry_if_exception_type(SourceTransientError),
            reraise=True,
            before_sleep=_log_retry,
        ):
            with attempt:
                return await asyncio.to_thread(self._extract, url, flat, items)
        msg = f"retries exhausted for {url}"  # pragma: no cover - reraise=True gets there first
        raise SourceError(msg)


def _log_retry(state: RetryCallState) -> None:
    """Emit the `retry` event the Phase 2 acceptance criteria assert on."""
    log.warning(
        "retry",
        attempt=state.attempt_number,
        sleep=round(state.next_action.sleep if state.next_action else 0.0, 2),
        error=str(state.outcome.exception()) if state.outcome else None,
    )
