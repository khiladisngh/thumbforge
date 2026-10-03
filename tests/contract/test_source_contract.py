"""Every `MetadataSource` must honour these, whatever it wraps (ADR 0005, phase 8 spec).

One suite, parametrised over `{ytdlp, api}`: `fetch` treats the two as interchangeable, so a
field one fills and the other leaves empty — or an id one reports as missing while the other
raises something else — is a bug a user would only meet by switching `--source`. Only the
factory differs per source; every assertion is shared. Fields a source legitimately cannot
fill (a yt-dlp flat playlist has no `description` or `published_at`, spike S11) are not
asserted here; the per-source unit tests pin those.

Both factories replay recorded fixtures through the source's own injection seam — the
`extract` callable for yt-dlp, a stubbed `_build_client` for the Data API — so the suite never
touches the network and needs no key. The two fixture sets describe the same 12 videos.
"""

from __future__ import annotations

import json
from datetime import UTC
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

from thumbforge.core.enums import ChannelSource, UrlKind
from thumbforge.core.errors import NotFoundError
from thumbforge.core.sources import MetadataSource
from thumbforge.sources import youtube_api
from thumbforge.sources.youtube_api import YouTubeDataApiSource
from thumbforge.sources.ytdlp import YtDlpSource

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"

VIDEO_ID = "jNQXAC9IVRw"
VIDEO_CHANNEL_ID = "UC4QobU6STFB0P71PMvOGN5A"
PLAYLIST_ID = "PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI"
CHANNEL_ID = "UC-9-kyTW8ZkZNDHQJ6FgpwQ"
UNKNOWN = {"video": "aaaaaaaaaaa", "playlist": "PL0000000000000000", "channel": "UC" + "0" * 22}

#: A recorded call: whatever the source's seam was asked, in order.
type Calls = list[object]
type Factory = Callable[[pytest.MonkeyPatch], tuple[MetadataSource, Calls]]


def _load(directory: str, name: str) -> dict[str, Any]:
    return json.loads((FIXTURES / directory / f"{name}.json").read_text(encoding="utf-8"))


def _ytdlp(_monkeypatch: pytest.MonkeyPatch) -> tuple[MetadataSource, Calls]:
    """yt-dlp through its `extract` seam; unknown URLs fail the way yt-dlp's translation does."""
    by_url = {
        f"https://www.youtube.com/watch?v={VIDEO_ID}": "video",
        f"https://www.youtube.com/playlist?list={PLAYLIST_ID}": "playlist",
        f"https://www.youtube.com/channel/{CHANNEL_ID}": "channel",
    }
    calls: Calls = []

    def extract(url: str, flat: bool, items: str | None = None) -> Mapping[str, Any]:
        calls.append((url, flat, items))
        if url not in by_url:
            msg = f"{url}: This video is unavailable"
            raise NotFoundError(msg)
        return _load("ytdlp", by_url[url])

    return YtDlpSource(extract), calls


class _Request:
    def __init__(self, respond: Callable[[], Mapping[str, Any]]) -> None:
        self._respond = respond

    def execute(self) -> Mapping[str, Any]:
        return self._respond()


class _Collection:
    def __init__(self, name: str, calls: Calls) -> None:
        self._name = name
        self._calls = calls

    def list(self, **params: Any) -> _Request:
        self._calls.append((self._name, params))
        return _Request(lambda: _api_response(self._name, params))


class _FixtureClient:
    """What `build("youtube", "v3")` returns, answering from `tests/fixtures/youtube_api/`."""

    def __init__(self, calls: Calls) -> None:
        self._calls = calls

    def videos(self) -> _Collection:
        return _Collection("videos", self._calls)

    def playlists(self) -> _Collection:
        return _Collection("playlists", self._calls)

    def playlistItems(self) -> _Collection:
        return _Collection("playlistItems", self._calls)

    def channels(self) -> _Collection:
        return _Collection("channels", self._calls)


def _api_response(resource: str, params: Mapping[str, Any]) -> Mapping[str, Any]:
    """Answer one list call the way the Data API does, including its empty results."""
    empty = {"kind": f"youtube#{resource}ListResponse", "etag": "e", "items": []}
    match resource:
        case "videos":
            pool = {
                item["id"]: item
                for name in ("video", "videos_batch")
                for item in _load("youtube_api", name)["items"]
            }
            return {**empty, "items": [pool[i] for i in params["id"].split(",") if i in pool]}
        case "playlists":
            return _load("youtube_api", "playlist") if params["id"] == PLAYLIST_ID else empty
        case "playlistItems":
            page1 = _load("youtube_api", "playlist_items_page1")
            if params.get("pageToken") == page1["nextPageToken"]:
                return _load("youtube_api", "playlist_items_page2")
            return page1
        case _:
            # A miss on channels.list omits `items` entirely rather than sending `[]`.
            found = params.get("id") == CHANNEL_ID
            return _load("youtube_api", "channel") if found else {"kind": "k", "etag": "e"}


def _api(monkeypatch: pytest.MonkeyPatch) -> tuple[MetadataSource, Calls]:
    """The Data API source with `build()` stubbed out by the fixture client."""
    calls: Calls = []
    monkeypatch.setattr(youtube_api, "_build_client", lambda _key: _FixtureClient(calls))
    return YouTubeDataApiSource("contract-key"), calls


SOURCES = [
    pytest.param((_ytdlp, ChannelSource.YTDLP), id="ytdlp"),
    pytest.param((_api, ChannelSource.API), id="api"),
]


@pytest.fixture(params=SOURCES)
def wired(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> tuple[MetadataSource, Calls, ChannelSource]:
    """A fixture-backed source, the calls its seam received, and the key it must report."""
    factory, expected = request.param
    source, calls = factory(monkeypatch)
    return source, calls, expected


def test_satisfies_the_protocol(wired: tuple[MetadataSource, Calls, ChannelSource]) -> None:
    """`cli` selects a source by Protocol, and `key` is what `--source` and the rows carry."""
    source, _, expected = wired
    assert isinstance(source, MetadataSource)
    assert source.key == expected.value


async def test_resolve_needs_no_io(wired: tuple[MetadataSource, Calls, ChannelSource]) -> None:
    """Classification is pure: a cached `fetch` must not spend a request or quota on it."""
    source, calls, _ = wired
    resolved = await source.resolve(f"https://www.youtube.com/playlist?list={PLAYLIST_ID}")
    assert (resolved.kind, resolved.youtube_id) == (UrlKind.PLAYLIST, PLAYLIST_ID)
    assert calls == []


async def test_fetch_video(wired: tuple[MetadataSource, Calls, ChannelSource]) -> None:
    source, _, expected = wired
    video = await source.fetch_video(VIDEO_ID)

    assert video.youtube_id == VIDEO_ID
    assert video.title
    assert video.channel_id == VIDEO_CHANNEL_ID
    assert video.duration_s == 19
    assert video.fetched_at.tzinfo is UTC
    assert video.source is expected


async def test_fetch_playlist(wired: tuple[MetadataSource, Calls, ChannelSource]) -> None:
    """Twelve items, numbered 1..12 in playlist order, owned by the playlist's channel."""
    source, _, expected = wired
    playlist = await source.fetch_playlist(PLAYLIST_ID)

    order = [entry["id"] for entry in _load("ytdlp", "playlist")["entries"]]
    assert playlist.youtube_id == PLAYLIST_ID
    assert playlist.item_count == 12
    assert [item.position for item in playlist.items] == list(range(1, 13))
    assert [item.video.youtube_id for item in playlist.items] == order
    assert playlist.channel_id == CHANNEL_ID
    assert all(item.video.title for item in playlist.items)
    assert all(item.video.duration_s is not None for item in playlist.items)
    assert playlist.source is expected
    assert {item.video.source for item in playlist.items} == {expected}


async def test_fetch_channel(wired: tuple[MetadataSource, Calls, ChannelSource]) -> None:
    source, _, expected = wired
    channel = await source.fetch_channel(CHANNEL_ID)

    assert channel.youtube_id == CHANNEL_ID
    assert channel.title == "Music"
    assert channel.source is expected


@pytest.mark.parametrize("kind", ["video", "playlist", "channel"])
async def test_unknown_id_is_not_found(
    wired: tuple[MetadataSource, Calls, ChannelSource], kind: str
) -> None:
    """Exit 3 for a missing id from either source, never a generic failure or an empty row."""
    source, _, _ = wired
    fetch = {
        "video": source.fetch_video,
        "playlist": source.fetch_playlist,
        "channel": source.fetch_channel,
    }[kind]
    with pytest.raises(NotFoundError):
        await fetch(UNKNOWN[kind])
