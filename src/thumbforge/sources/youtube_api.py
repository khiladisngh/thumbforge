"""`YouTubeDataApiSource` — YouTube metadata via the Data API v3 (decision D7, ROADMAP P8.1).

The optional alternative to `YtDlpSource`, behind the `api` extra
(`uv tool install "thumbforge[api]"`). It produces the same `core.models` values with the same
field mapping; only `source` differs. The key arrives through the constructor: `cli` resolves
it from the environment or the keyring, and no adapter reads credentials.

All knowledge of `googleapiclient` lives in `_build_client` (the only import of the client)
and `_translate` (its exceptions). Both imports are lazy, so this module imports without the
extra and `thumbforge db status` pays nothing; the unit tests replace `_build_client` with a
stub that serves recorded JSON.

Quota shapes the request plan. Every `list` call costs one unit whatever it returns, so a
playlist is fetched as `playlists.list`, then `playlistItems.list` page by page (50 per page),
then `videos.list` in batches of 50 ids for duration, description, upload date and thumbnail —
roughly `2 * ceil(n / 50) + 1` units for `n` items, never one call per video.
"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import re
import threading
from contextlib import contextmanager
from datetime import UTC, datetime
from typing import TYPE_CHECKING, ClassVar, Final, Protocol, cast

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
    from collections.abc import Callable, Generator, Mapping, Sequence

    # Stub-only module (google-api-python-client-stubs, dev group): it types the client's
    # generated resources and has no runtime counterpart, hence TYPE_CHECKING and the ignore.
    from googleapiclient._apis.youtube.v3 import (  # pyright: ignore[reportMissingModuleSource]
        YouTubeResource,
    )
    from tenacity import RetryCallState

    from thumbforge.core.models import ResolvedUrl

log = get_logger(__name__)

#: A decoded Data API response or a part of one. `object` values, because every read is
#: checked on the way out (`_shape_errors`): the client hands back whatever JSON arrived.
type RawResponse = Mapping[str, object]


class _Executable(Protocol):
    """A prepared Data API request; `execute()` performs it and decodes the JSON body."""

    def execute(self) -> RawResponse: ...


#: Builds one request against the client, e.g. `lambda yt: yt.videos().list(...)`.
type RequestBuilder = Callable[[YouTubeResource], _Executable]

_WATCH_URL: Final = "https://www.youtube.com/watch?v={}"
_PLAYLIST_URL: Final = "https://www.youtube.com/playlist?list={}"
_CHANNEL_URL: Final = "https://www.youtube.com/channel/{}"

#: The Data API's ceiling for `maxResults` and for ids in one `videos.list`.
_PAGE_SIZE: Final = 50
_VIDEO_PARTS: Final = "snippet,contentDetails"
#: Largest first. Presence varies per video: `maxres` and `standard` are often missing.
_THUMBNAIL_SIZES: Final = ("maxres", "standard", "high", "medium", "default")

_INSTALL_HINT: Final = 'uv tool install "thumbforge[api]"'
_SET_KEY_HINT: Final = "check the key with `thumbforge provider set-key api`"

#: `errors[0].reason` values meaning "out of quota". Retrying only burns more of it, so none
#: is retried, even `rateLimitExceeded` — which the API sends with 403 as often as with 429.
_QUOTA_REASONS: Final = frozenset({"quotaExceeded", "dailyLimitExceeded", "rateLimitExceeded"})
#: `errors[0].reason` values meaning the key is wrong, unusable, or not enabled for the API.
_KEY_REASONS: Final = frozenset({"keyInvalid", "forbidden", "accessNotConfigured"})
#: An invalid key, measured against the live API, arrives as reason `badRequest` with this in
#: the message (the `API_KEY_INVALID` detail curl sees is absent from the client's response).
_KEY_MESSAGE: Final = "API key"
#: HTTP statuses worth another attempt: 429 is throttling, 5xx is YouTube being down.
_RETRY_STATUSES: Final = frozenset({429, 500, 502, 503, 504})

# Same policy as `ytdlp.py` (PLAN.md §7.2): exponential backoff base 2s, factor 2, max 60s,
# jitter, 3 attempts. Duplicated rather than shared so neither adapter depends on the other.
_RETRY_ATTEMPTS: Final = 3
_RETRY_WAIT: Final = wait_exponential_jitter(initial=2.0, exp_base=2.0, max=60.0, jitter=2.0)

#: ISO-8601 durations as YouTube writes them (`PT1H2M3S`, `P1DT1S`). Years and months are
#: not fixed lengths and never occur for a video, so they deliberately fail to match.
_DURATION = re.compile(
    r"P(?:(?P<weeks>\d+)W)?(?:(?P<days>\d+)D)?"
    r"(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+(?:\.\d+)?)S)?)?"
)
_DURATION_UNITS: Final = {"weeks": 604800, "days": 86400, "hours": 3600, "minutes": 60}


def _missing_extra() -> SourceError:
    msg = "the YouTube Data API source needs the optional 'api' extra"
    return SourceError(msg, hint=_INSTALL_HINT)


def require_extra() -> None:
    """Raise the install hint unless the `api` extra is installed.

    `cli` calls this before resolving a key, so a user without the extra is told to install
    it rather than to store a key the source cannot use. `find_spec` locates the client
    without importing its HTTP stack.
    """
    if importlib.util.find_spec("googleapiclient") is None:
        raise _missing_extra()


def _build_client(api_key: str) -> YouTubeResource:
    """Build the Data API client; the one place `googleapiclient` is imported for use.

    `build` reads the discovery document bundled with the package, so this makes no request
    and there is nothing for the discovery cache to keep.
    """
    try:
        # `build`'s overloads mention `oauth2client.Credentials`, a package that is neither a
        # dependency nor stubbed, so pyright sees it as partially unknown. Only the youtube/v3
        # overload is used and it is fully typed.
        from googleapiclient.discovery import (
            build,  # pyright: ignore[reportUnknownVariableType]
        )
    except ImportError as exc:
        raise _missing_extra() from exc
    return build("youtube", "v3", developerKey=api_key, cache_discovery=False)


def _scrub(text: str, api_key: str) -> str:
    """Remove the key from upstream text: the client puts `key=` in every request URI."""
    return text.replace(api_key, "<redacted>") if api_key else text


def _error_details(content: bytes) -> tuple[str, str]:
    """`errors[0].reason` and `message` from a Data API error body; empty when malformed."""
    try:
        body: object = json.loads(content)
    except TypeError, ValueError:
        return "", ""
    error = _loose_mapping(_loose_mapping(body).get("error"))
    errors = _loose_list(error.get("errors"))
    reason = _loose_mapping(errors[0]).get("reason") if errors else None
    message = error.get("message")
    return (
        reason if isinstance(reason, str) else "",
        message if isinstance(message, str) else "",
    )


def _loose_mapping(value: object) -> RawResponse:
    """`value` if it is an object, else empty: error bodies are read tolerantly."""
    return cast("RawResponse", value) if isinstance(value, dict) else {}


def _loose_list(value: object) -> list[object]:
    """`value` if it is a list, else empty."""
    return cast("list[object]", value) if isinstance(value, list) else []


def _translate(exc: Exception, what: str, api_key: str) -> ThumbforgeError | None:
    """Map a client failure onto the thumbforge hierarchy; `None` for an unexpected bug.

    Only messages built here, from the parsed body and the status, reach the user. The
    exception's own text is never used for `HttpError`: its repr embeds the request URI,
    which carries the key.
    """
    import httplib2
    from googleapiclient.errors import HttpError

    if isinstance(exc, HttpError):
        status = exc.status_code
        reason, message = _error_details(exc.content)
        detail = _scrub(" ".join(p for p in (f"HTTP {status}", reason, message) if p), api_key)
        if reason in _QUOTA_REASONS:
            msg = f"YouTube Data API quota exhausted fetching {what}: {detail}"
            hint = "the daily quota resets at midnight Pacific time; meanwhile use --source ytdlp"
            return SourceError(msg, hint=hint)
        if reason in _KEY_REASONS or _KEY_MESSAGE in message:
            msg = f"YouTube Data API rejected the key fetching {what}: {detail}"
            return SourceError(msg, hint=_SET_KEY_HINT)
        if status == 404:
            return NotFoundError(what, hint="check the id is public and still exists")
        if status in _RETRY_STATUSES:
            return SourceTransientError(f"YouTube Data API {detail} fetching {what}")
        return SourceError(f"YouTube Data API {detail} fetching {what}")
    if isinstance(exc, (OSError, httplib2.HttpLib2Error)):
        text = _scrub(str(exc) or type(exc).__name__, api_key)
        return SourceTransientError(f"network error fetching {what}: {text}")
    return None


@contextmanager
def _shape_errors(what: str) -> Generator[None]:
    """Turn an unexpected response *shape* into a `SourceError`, as `ytdlp._shape_errors` does.

    A guard at the boundary rather than a schema: the fields that matter are validated by the
    `core.models` they flow into, and a wrong type surfaces here as a diagnosable error
    instead of a traceback.
    """
    try:
        yield
    except ThumbforgeError:
        raise
    except (AttributeError, LookupError, OverflowError, TypeError, ValueError) as exc:
        msg = f"unexpected YouTube Data API response for {what}: {exc}"
        raise SourceError(msg, hint="the Data API response changed shape") from exc


def _object(value: object, name: str) -> RawResponse:
    """`value` as a JSON object, or a `TypeError` that `_shape_errors` reports."""
    if not isinstance(value, dict):
        msg = f"{name} is {type(value).__name__}, not an object"
        raise TypeError(msg)
    return cast("RawResponse", value)


def _section(container: RawResponse, key: str) -> RawResponse:
    """A nested object; absent counts as empty, any other type is a shape error."""
    value = container.get(key)
    return {} if value is None else _object(value, repr(key))


def _items(response: object) -> list[RawResponse]:
    """A list response's `items`. The API omits the key entirely when nothing matched."""
    items = _object(response, "response").get("items")
    if items is None:
        return []
    if not isinstance(items, list):
        msg = f"'items' is {type(items).__name__}, not a list"
        raise TypeError(msg)
    return [_object(item, "item") for item in cast("list[object]", items)]


def _text(info: RawResponse, key: str) -> str:
    """Read a string field; missing and `null` both read as empty."""
    value = info.get(key)
    return value if isinstance(value, str) else ""


def _duration(value: str) -> int | None:
    """Whole seconds from an ISO-8601 duration, truncated like `ytdlp._duration`.

    `P0D` is what the API reports for a live or upcoming broadcast, so a zero total means
    "no duration", as it does from yt-dlp. Anything unparseable is `None` too: a duration is
    nice to have, not worth failing a playlist over.
    """
    match = _DURATION.fullmatch(value)
    if match is None:
        return None
    parts = match.groupdict()
    total = float(parts["seconds"] or 0) + sum(
        int(parts[unit] or 0) * factor for unit, factor in _DURATION_UNITS.items()
    )
    return int(total) or None


def _published_at(snippet: RawResponse) -> datetime | None:
    """`snippet.publishedAt` as an aware UTC instant, or `None` when absent."""
    value = _text(snippet, "publishedAt")
    if not value:
        return None
    moment = datetime.fromisoformat(value)
    return moment.replace(tzinfo=UTC) if moment.tzinfo is None else moment.astimezone(UTC)


def _thumbnail_url(snippet: RawResponse) -> str | None:
    """The largest thumbnail the API listed, by name rather than by reported size."""
    thumbnails = _section(snippet, "thumbnails")
    for size in _THUMBNAIL_SIZES:
        url = _text(_section(thumbnails, size), "url")
        if url:
            return url
    return None


def _video_meta(item: RawResponse) -> VideoMeta:
    """Build a `VideoMeta` from one `videos.list` item (parts `snippet,contentDetails`)."""
    youtube_id = _text(item, "id")
    if not youtube_id:
        msg = "YouTube Data API video has no id"
        raise SourceError(msg, hint="the Data API response changed shape")
    snippet = _section(item, "snippet")
    return VideoMeta(
        youtube_id=youtube_id,
        title=_text(snippet, "title"),
        url=_WATCH_URL.format(youtube_id),
        channel_id=_text(snippet, "channelId") or None,
        description=_text(snippet, "description"),
        duration_s=_duration(_text(_section(item, "contentDetails"), "duration")),
        published_at=_published_at(snippet),
        source_thumbnail_url=_thumbnail_url(snippet),
        source=ChannelSource.API,
    )


def _item_video_id(item: RawResponse) -> str:
    """The video a `playlistItems.list` item points at."""
    video_id = _text(_section(item, "contentDetails"), "videoId") or _text(
        _section(_section(item, "snippet"), "resourceId"), "videoId"
    )
    if not video_id:
        msg = "YouTube Data API playlist item has no video id"
        raise SourceError(msg, hint="the Data API response changed shape")
    return video_id


class YouTubeDataApiSource:
    """Fetch YouTube metadata with the Data API v3 (a `MetadataSource` implementation)."""

    key: ClassVar[str] = ChannelSource.API.value

    def __init__(self, api_key: str, *, attempts: int = _RETRY_ATTEMPTS) -> None:
        """Hold the key; the client is built on the first request, not here."""
        self._api_key = api_key
        self._attempts = attempts
        self._client: YouTubeResource | None = None
        self._lock = threading.Lock()

    async def resolve(self, url: str) -> ResolvedUrl:
        """Classify input without a request; `core.urls` does the work."""
        return classify_url(url)

    async def fetch_video(self, youtube_id: str) -> VideoMeta:
        """One `videos.list` call."""
        what = f"video {youtube_id!r}"
        response = await self._list(
            lambda yt: yt.videos().list(part=_VIDEO_PARTS, id=youtube_id), what
        )
        with _shape_errors(what):
            items = _items(response)
            if not items:
                raise NotFoundError(what, hint="check the id is public and still exists")
            return _video_meta(items[0])

    async def fetch_playlist(self, youtube_id: str) -> PlaylistMeta:
        """The playlist, every page of its items, then its videos in batches of 50.

        Items whose video `videos.list` does not return — deleted or private — are dropped
        *before* numbering, so positions stay contiguous `1..N` in playlist order, as with
        yt-dlp. `channel_id` is the playlist owner's; each video keeps its own uploader's.
        """
        what = f"playlist {youtube_id!r}"
        response = await self._list(
            lambda yt: yt.playlists().list(part="snippet", id=youtube_id), what
        )
        with _shape_errors(what):
            found = _items(response)
            if not found:
                raise NotFoundError(what, hint="check the playlist is public and still exists")
            playlist = found[0]
            snippet = _section(playlist, "snippet")

        video_ids = await self._playlist_video_ids(youtube_id, what)
        videos = await self._videos(video_ids, what)
        with _shape_errors(what):
            kept = [videos[video_id] for video_id in video_ids if video_id in videos]
            return PlaylistMeta(
                youtube_id=_text(playlist, "id") or youtube_id,
                title=_text(snippet, "title"),
                url=_PLAYLIST_URL.format(_text(playlist, "id") or youtube_id),
                channel_id=_text(snippet, "channelId") or None,
                description=_text(snippet, "description"),
                items=tuple(
                    PlaylistItemMeta(video=video, position=position)
                    for position, video in enumerate(kept, start=1)
                ),
                source=ChannelSource.API,
            )

    async def fetch_channel(self, youtube_id: str) -> ChannelMeta:
        """One `channels.list` call; the channel's videos are never listed.

        A `UC…` id is looked up by `id`, anything else as a handle, mirroring how
        `YtDlpSource` builds its channel URL.
        """
        what = f"channel {youtube_id!r}"
        if youtube_id.startswith("UC"):
            response = await self._list(
                lambda yt: yt.channels().list(part="snippet", id=youtube_id), what
            )
        else:
            response = await self._list(
                lambda yt: yt.channels().list(part="snippet", forHandle=youtube_id), what
            )
        with _shape_errors(what):
            items = _items(response)
            if not items:
                raise NotFoundError(what, hint="check the channel id or handle")
            channel_id = _text(items[0], "id") or youtube_id
            return ChannelMeta(
                youtube_id=channel_id,
                title=_text(_section(items[0], "snippet"), "title"),
                url=_CHANNEL_URL.format(channel_id),
                source=ChannelSource.API,
            )

    async def _playlist_video_ids(self, playlist_id: str, what: str) -> list[str]:
        """Every item's video id, following `nextPageToken` until the API stops sending one."""
        video_ids: list[str] = []
        token: str | None = None
        seen: set[str] = set()
        while True:
            response = await self._list(_playlist_items_request(playlist_id, token), what)
            with _shape_errors(what):
                video_ids.extend(_item_video_id(item) for item in _items(response))
                token = _text(_object(response, "response"), "nextPageToken") or None
            if token is None:
                return video_ids
            if token in seen:
                msg = f"YouTube Data API repeated a page token while listing {what}"
                raise SourceError(msg)
            seen.add(token)

    async def _videos(self, video_ids: Sequence[str], what: str) -> dict[str, VideoMeta]:
        """Full video metadata by id, `_PAGE_SIZE` ids per `videos.list` call."""
        unique = list(dict.fromkeys(video_ids))
        videos: dict[str, VideoMeta] = {}
        for start in range(0, len(unique), _PAGE_SIZE):
            ids = ",".join(unique[start : start + _PAGE_SIZE])
            response = await self._list(
                lambda yt, ids=ids: yt.videos().list(part=_VIDEO_PARTS, id=ids), what
            )
            with _shape_errors(what):
                for item in _items(response):
                    video = _video_meta(item)
                    videos[video.youtube_id] = video
        return videos

    async def _list(self, request: RequestBuilder, what: str) -> object:
        """Run one request off the event loop, retrying only transient failures."""
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(self._attempts),
            wait=_RETRY_WAIT,
            retry=retry_if_exception_type(SourceTransientError),
            reraise=True,
            before_sleep=_log_retry,
        ):
            with attempt:
                return await asyncio.to_thread(self._execute, request, what)
        msg = f"retries exhausted for {what}"  # pragma: no cover - reraise=True gets there first
        raise SourceError(msg)

    def _execute(self, request: RequestBuilder, what: str) -> object:
        """Build the client if needed, perform the request, translate its failure."""
        with self._lock:
            if self._client is None:
                self._client = _build_client(self._api_key)
            client = self._client
        try:
            return request(client).execute()
        except Exception as exc:
            translated = _translate(exc, what, self._api_key)
            if translated is None:
                raise
        # Raised outside the handler: the original's text and repr carry the request URI, and
        # with it the key, so it must not survive even as `__context__` of what users see.
        raise translated


def _playlist_items_request(playlist_id: str, token: str | None) -> RequestBuilder:
    """One `playlistItems.list` page; `pageToken` is sent only after the first page."""
    if token is None:
        return lambda yt: yt.playlistItems().list(
            part=_VIDEO_PARTS, playlistId=playlist_id, maxResults=_PAGE_SIZE
        )
    return lambda yt: yt.playlistItems().list(
        part=_VIDEO_PARTS, playlistId=playlist_id, maxResults=_PAGE_SIZE, pageToken=token
    )


def _log_retry(state: RetryCallState) -> None:
    """Emit the same `retry` event as `ytdlp._log_retry`."""
    log.warning(
        "retry",
        attempt=state.attempt_number,
        sleep=round(state.next_action.sleep if state.next_action else 0.0, 2),
        error=str(state.outcome.exception()) if state.outcome else None,
    )
