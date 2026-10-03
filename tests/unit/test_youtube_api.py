"""`YouTubeDataApiSource` against Data API v3 fixtures with `build()` stubbed (ROADMAP P8.1).

No network and no real key: `_build_client` is replaced by `FakeYouTube`, which serves
`tests/fixtures/youtube_api/*.json` and records every `list` call, so pagination, batching
and the "no retry on quota" rule are asserted on the requests actually made. Errors are the
real `googleapiclient.errors.HttpError`, built the way the client builds them, because the
mapping reads its status and JSON body.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import httplib2
import pytest
from googleapiclient.errors import HttpError
from sqlalchemy import select
from tenacity import wait_none
from typer.testing import CliRunner

from thumbforge import credentials
from thumbforge.cli.app import app
from thumbforge.core.enums import ChannelSource
from thumbforge.core.errors import (
    ExitCode,
    NotFoundError,
    SourceError,
    SourceTransientError,
)
from thumbforge.logging import configure_logging
from thumbforge.sources import youtube_api, ytdlp
from thumbforge.sources.youtube_api import YouTubeDataApiSource, _duration, require_extra
from thumbforge.storage.db import get_engine, session_scope
from thumbforge.storage.models import Channel

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"

KEY = "AIzaSy-unit-test-key-0000000000000000"
VIDEO_ID = "jNQXAC9IVRw"
PLAYLIST_ID = "PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI"
PLAYLIST_URL = f"https://www.youtube.com/playlist?list={PLAYLIST_ID}"
CHANNEL_ID = "UC-9-kyTW8ZkZNDHQJ6FgpwQ"
VIDEO_PARTS = "snippet,contentDetails"

type Params = dict[str, Any]
type Responder = Callable[[Params], Mapping[str, Any]]


def _fixture(name: str) -> dict[str, Any]:
    return json.loads((FIXTURES / "youtube_api" / f"{name}.json").read_text(encoding="utf-8"))


def _http_error(status: int, body: bytes | dict[str, Any]) -> HttpError:
    """An `HttpError` as the client raises it — including the `key=` in the request URI."""
    content = body if isinstance(body, bytes) else json.dumps(body).encode()
    uri = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet&key={KEY}&alt=json"
    return HttpError(httplib2.Response({"status": str(status)}), content, uri=uri)


def _error_body(status: int, reason: str) -> dict[str, Any]:
    message = f"{reason} happened"
    return {
        "error": {
            "code": status,
            "message": message,
            "errors": [{"message": message, "domain": "youtube", "reason": reason}],
        }
    }


def _videos_from_fixtures(params: Params) -> Mapping[str, Any]:
    pool = {
        item["id"]: item for name in ("video", "videos_batch") for item in _fixture(name)["items"]
    }
    items = [pool[i] for i in params["id"].split(",") if i in pool]
    return {"kind": "youtube#videoListResponse", "etag": "e", "items": items}


def _playlist_items_from_fixtures(params: Params) -> Mapping[str, Any]:
    page1 = _fixture("playlist_items_page1")
    if params.get("pageToken") == page1["nextPageToken"]:
        return _fixture("playlist_items_page2")
    return page1


def _playlists_from_fixtures(params: Params) -> Mapping[str, Any]:
    if params["id"] == PLAYLIST_ID:
        return _fixture("playlist")
    return {"kind": "youtube#playlistListResponse", "etag": "e", "items": []}


def _channels_from_fixtures(params: Params) -> Mapping[str, Any]:
    if params.get("id") == CHANNEL_ID or params.get("forHandle") == "@music":
        return _fixture("channel")
    return {"kind": "youtube#channelListResponse", "etag": "e"}


class _Request:
    def __init__(self, owner: FakeYouTube, resource: str, params: Params) -> None:
        self._owner, self._resource, self._params = owner, resource, params

    def execute(self) -> Mapping[str, Any]:
        self._owner.calls.append((self._resource, self._params))
        return self._owner.responders[self._resource](self._params)


class _Collection:
    def __init__(self, owner: FakeYouTube, resource: str) -> None:
        self._owner, self._resource = owner, resource

    def list(self, **params: Any) -> _Request:
        return _Request(self._owner, self._resource, params)


class FakeYouTube:
    """Stands in for the `build("youtube", "v3")` resource; responders are swappable."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, Params]] = []
        self.keys: list[str] = []
        self.responders: dict[str, Responder] = {
            "videos": _videos_from_fixtures,
            "playlists": _playlists_from_fixtures,
            "playlistItems": _playlist_items_from_fixtures,
            "channels": _channels_from_fixtures,
        }

    def videos(self) -> _Collection:
        return _Collection(self, "videos")

    def playlists(self) -> _Collection:
        return _Collection(self, "playlists")

    def playlistItems(self) -> _Collection:
        return _Collection(self, "playlistItems")

    def channels(self) -> _Collection:
        return _Collection(self, "channels")

    def build(self, api_key: str) -> FakeYouTube:
        """The `_build_client` replacement; remembers the key it was handed."""
        self.keys.append(api_key)
        return self


@pytest.fixture
def fake(monkeypatch: pytest.MonkeyPatch) -> FakeYouTube:
    """Replace `build()` and neutralise the backoff clock; the policy is under test."""
    client = FakeYouTube()
    monkeypatch.setattr(youtube_api, "_build_client", client.build)
    monkeypatch.setattr(youtube_api, "_RETRY_WAIT", wait_none())
    return client


# --- mapping ---------------------------------------------------------------------------


async def test_fetch_video_maps_every_field(fake: FakeYouTube) -> None:
    video = await YouTubeDataApiSource(KEY).fetch_video(VIDEO_ID)

    assert fake.calls == [("videos", {"part": VIDEO_PARTS, "id": VIDEO_ID})]
    assert fake.keys == [KEY]
    assert video.youtube_id == VIDEO_ID
    assert video.title == "Me at the zoo"
    assert video.url == f"https://www.youtube.com/watch?v={VIDEO_ID}"
    assert video.channel_id == "UC4QobU6STFB0P71PMvOGN5A"
    assert video.description
    assert video.duration_s == 19
    assert video.published_at == datetime(2005, 4, 24, 3, 31, 52, tzinfo=UTC)
    assert video.source_thumbnail_url == f"https://i.ytimg.com/vi/{VIDEO_ID}/maxresdefault.jpg"
    assert video.source is ChannelSource.API


async def test_the_client_is_built_once_per_source(fake: FakeYouTube) -> None:
    """Building parses the bundled discovery document; once per command is enough."""
    source = YouTubeDataApiSource(KEY)
    await source.fetch_video(VIDEO_ID)
    await source.fetch_channel(CHANNEL_ID)
    assert fake.keys == [KEY]


@pytest.mark.parametrize(
    ("value", "seconds"),
    [
        ("PT19S", 19),
        ("PT1H2M3S", 3723),
        ("PT10M", 600),
        ("PT2H", 7200),
        ("P1DT1S", 86401),
        ("P1W", 604800),
        ("PT3.9S", 3),
        ("P0D", None),
        ("PT0S", None),
        ("", None),
        ("P", None),
        ("PT", None),
        ("19", None),
        ("P1Y", None),
        ("pt19s", None),
    ],
)
def test_iso_8601_durations(value: str, seconds: int | None) -> None:
    """Whole seconds, truncated like yt-dlp; live (`P0D`) and anything unparseable are None."""
    assert _duration(value) == seconds


@pytest.mark.parametrize(
    ("present", "expected"),
    [
        (("default", "medium", "high", "standard", "maxres"), "maxresdefault"),
        (("default", "medium", "high", "standard"), "sddefault"),
        (("default", "medium", "high"), "hqdefault"),
        (("default", "medium"), "mqdefault"),
        (("default",), "default"),
        ((), None),
    ],
)
async def test_thumbnail_prefers_the_largest_present(
    fake: FakeYouTube, present: tuple[str, ...], expected: str | None
) -> None:
    response = _fixture("video")
    snippet = response["items"][0]["snippet"]
    snippet["thumbnails"] = {k: v for k, v in snippet["thumbnails"].items() if k in present}
    fake.responders["videos"] = lambda _params: response

    video = await YouTubeDataApiSource(KEY).fetch_video(VIDEO_ID)

    if expected is None:
        assert video.source_thumbnail_url is None
    else:
        assert video.source_thumbnail_url == f"https://i.ytimg.com/vi/{VIDEO_ID}/{expected}.jpg"


async def test_live_video_has_no_duration(fake: FakeYouTube) -> None:
    response = _fixture("video")
    response["items"][0]["contentDetails"]["duration"] = "P0D"
    fake.responders["videos"] = lambda _params: response

    assert (await YouTubeDataApiSource(KEY).fetch_video(VIDEO_ID)).duration_s is None


async def test_fetch_channel_by_id(fake: FakeYouTube) -> None:
    channel = await YouTubeDataApiSource(KEY).fetch_channel(CHANNEL_ID)

    assert fake.calls == [("channels", {"part": "snippet", "id": CHANNEL_ID})]
    assert channel.youtube_id == CHANNEL_ID
    assert channel.title == "Music"
    assert channel.url == f"https://www.youtube.com/channel/{CHANNEL_ID}"
    assert channel.source is ChannelSource.API


async def test_fetch_channel_by_handle_uses_for_handle(fake: FakeYouTube) -> None:
    """A handle is not an id; the stored row still carries the canonical `UC…` id."""
    channel = await YouTubeDataApiSource(KEY).fetch_channel("@music")

    assert fake.calls == [("channels", {"part": "snippet", "forHandle": "@music"})]
    assert channel.youtube_id == CHANNEL_ID


# --- playlists -------------------------------------------------------------------------


async def test_playlist_follows_page_tokens_then_batches_videos(fake: FakeYouTube) -> None:
    playlist = await YouTubeDataApiSource(KEY).fetch_playlist(PLAYLIST_ID)

    token = _fixture("playlist_items_page1")["nextPageToken"]
    items_params = {"part": VIDEO_PARTS, "playlistId": PLAYLIST_ID, "maxResults": 50}
    ids = [item["id"] for item in _fixture("videos_batch")["items"]]
    assert fake.calls == [
        ("playlists", {"part": "snippet", "id": PLAYLIST_ID}),
        ("playlistItems", items_params),
        ("playlistItems", {**items_params, "pageToken": token}),
        ("videos", {"part": VIDEO_PARTS, "id": ",".join(ids)}),
    ]
    assert [item.video.youtube_id for item in playlist.items] == ids
    assert [item.position for item in playlist.items] == list(range(1, 13))
    assert playlist.title == "Popular Music Videos"
    assert playlist.url == PLAYLIST_URL
    assert playlist.channel_id == CHANNEL_ID
    # The batch call fills what a yt-dlp flat playlist cannot.
    assert all(item.video.published_at is not None for item in playlist.items)
    assert playlist.items[0].video.duration_s == 235


async def test_large_playlist_asks_for_videos_in_batches_of_fifty(fake: FakeYouTube) -> None:
    """One `videos.list` per 50 ids (1 quota unit each), never one call per video."""
    ids = [f"vid{index:08d}" for index in range(120)]
    pages = [ids[start : start + 50] for start in range(0, 120, 50)]

    def playlist_items(params: Params) -> Mapping[str, Any]:
        page = int(params.get("pageToken", "0"))
        response: dict[str, Any] = {
            "items": [{"contentDetails": {"videoId": video_id}} for video_id in pages[page]]
        }
        if page + 1 < len(pages):
            response["nextPageToken"] = str(page + 1)
        return response

    def videos(params: Params) -> Mapping[str, Any]:
        return {
            "items": [
                {"id": video_id, "snippet": {"title": video_id}}
                for video_id in params["id"].split(",")
            ]
        }

    fake.responders["playlistItems"] = playlist_items
    fake.responders["videos"] = videos

    playlist = await YouTubeDataApiSource(KEY).fetch_playlist(PLAYLIST_ID)

    batches = [params["id"].split(",") for name, params in fake.calls if name == "videos"]
    assert [len(batch) for batch in batches] == [50, 50, 20]
    assert [video_id for batch in batches for video_id in batch] == ids
    assert sum(1 for name, _ in fake.calls if name == "playlistItems") == 3
    assert playlist.item_count == 120


async def test_deleted_and_private_items_are_dropped_without_holes(fake: FakeYouTube) -> None:
    """`videos.list` omits what it cannot show; the rest are renumbered 1..N in order."""
    ids = [item["id"] for item in _fixture("videos_batch")["items"]]
    hidden = {ids[0], ids[5]}

    def videos(params: Params) -> Mapping[str, Any]:
        response = dict(_videos_from_fixtures(params))
        response["items"] = [item for item in response["items"] if item["id"] not in hidden]
        return response

    fake.responders["videos"] = videos

    playlist = await YouTubeDataApiSource(KEY).fetch_playlist(PLAYLIST_ID)

    assert [item.video.youtube_id for item in playlist.items] == [
        video_id for video_id in ids if video_id not in hidden
    ]
    assert [item.position for item in playlist.items] == list(range(1, 11))


async def test_unknown_playlist_is_not_found_without_listing_items(fake: FakeYouTube) -> None:
    with pytest.raises(NotFoundError):
        await YouTubeDataApiSource(KEY).fetch_playlist("PL0000000000000000")
    assert [name for name, _ in fake.calls] == ["playlists"]


# --- errors ----------------------------------------------------------------------------


def _raising(error: Exception) -> Callable[[Params], Mapping[str, Any]]:
    def respond(_params: Params) -> Mapping[str, Any]:
        raise error

    return respond


async def test_quota_exhaustion_is_a_source_error_and_not_retried(fake: FakeYouTube) -> None:
    fake.responders["videos"] = _raising(_http_error(403, _fixture("error_quota")))

    with pytest.raises(SourceError) as caught:
        await YouTubeDataApiSource(KEY).fetch_video(VIDEO_ID)

    assert type(caught.value) is SourceError
    assert caught.value.exit_code is ExitCode.UNEXPECTED
    assert "--source ytdlp" in (caught.value.hint or "")
    assert len(fake.calls) == 1


@pytest.mark.parametrize("reason", ["dailyLimitExceeded", "rateLimitExceeded"])
async def test_other_quota_reasons_are_not_retried(fake: FakeYouTube, reason: str) -> None:
    fake.responders["videos"] = _raising(_http_error(403, _error_body(403, reason)))

    with pytest.raises(SourceError) as caught:
        await YouTubeDataApiSource(KEY).fetch_video(VIDEO_ID)

    assert type(caught.value) is SourceError
    assert len(fake.calls) == 1


#: What the client actually receives for an invalid key, measured against the live API.
INVALID_KEY_BODY = {
    "error": {
        "code": 400,
        "message": "API key not valid. Please pass a valid API key.",
        "errors": [
            {
                "message": "API key not valid. Please pass a valid API key.",
                "domain": "global",
                "reason": "badRequest",
            }
        ],
        "status": "INVALID_ARGUMENT",
    }
}


@pytest.mark.parametrize(
    ("status", "body"),
    [
        (400, INVALID_KEY_BODY),
        (400, _error_body(400, "keyInvalid")),
        (403, _error_body(403, "forbidden")),
        (403, _error_body(403, "accessNotConfigured")),
    ],
    ids=["live-invalid-key", "keyInvalid", "forbidden", "accessNotConfigured"],
)
async def test_rejected_key_points_at_set_key(
    fake: FakeYouTube, status: int, body: dict[str, Any]
) -> None:
    fake.responders["videos"] = _raising(_http_error(status, body))

    with pytest.raises(SourceError) as caught:
        await YouTubeDataApiSource(KEY).fetch_video(VIDEO_ID)

    assert type(caught.value) is SourceError
    assert "thumbforge provider set-key api" in (caught.value.hint or "")
    assert len(fake.calls) == 1


async def test_http_404_is_not_found(fake: FakeYouTube) -> None:
    error = _http_error(404, _error_body(404, "playlistNotFound"))
    fake.responders["playlistItems"] = _raising(error)

    with pytest.raises(NotFoundError):
        await YouTubeDataApiSource(KEY).fetch_playlist(PLAYLIST_ID)


@pytest.mark.parametrize(
    "error",
    [
        _http_error(503, _error_body(503, "backendError")),
        _http_error(429, b"not json at all"),
        OSError("connection reset"),
        httplib2.ServerNotFoundError("Unable to find the server at youtube.googleapis.com"),
    ],
    ids=["503", "429-malformed-body", "oserror", "httplib2"],
)
async def test_transient_failures_are_retried_then_reraised(
    fake: FakeYouTube, error: Exception
) -> None:
    fake.responders["videos"] = _raising(error)

    with pytest.raises(SourceTransientError) as caught:
        await YouTubeDataApiSource(KEY, attempts=3).fetch_video(VIDEO_ID)

    assert len(fake.calls) == 3
    assert caught.value.exit_code is ExitCode.UNEXPECTED


async def test_a_transient_failure_that_clears_succeeds(fake: FakeYouTube) -> None:
    failures = [_http_error(500, _error_body(500, "backendError"))]

    def flaky(params: Params) -> Mapping[str, Any]:
        if failures:
            raise failures.pop()
        return _videos_from_fixtures(params)

    fake.responders["videos"] = flaky

    video = await YouTubeDataApiSource(KEY).fetch_video(VIDEO_ID)
    assert video.youtube_id == VIDEO_ID
    assert len(fake.calls) == 2


async def test_unrecognised_http_error_is_a_source_error(fake: FakeYouTube) -> None:
    fake.responders["videos"] = _raising(_http_error(400, b"{malformed"))

    with pytest.raises(SourceError) as caught:
        await YouTubeDataApiSource(KEY).fetch_video(VIDEO_ID)

    assert type(caught.value) is SourceError
    assert "400" in str(caught.value)
    assert len(fake.calls) == 1


@pytest.mark.parametrize(
    "response",
    [
        ["not", "a", "mapping"],
        {"items": "not a list"},
        {"items": ["not a mapping"]},
        {"items": [{"id": VIDEO_ID, "snippet": ["not", "a", "mapping"]}]},
        {"items": [{"id": VIDEO_ID, "snippet": {"publishedAt": "yesterday"}}]},
        {"items": [{"snippet": {"title": "no id"}}]},
    ],
    ids=["response", "items", "item", "snippet", "published-at", "no-id"],
)
async def test_unexpected_response_shape_is_a_source_error(
    fake: FakeYouTube, response: Any
) -> None:
    fake.responders["videos"] = lambda _params: response

    with pytest.raises(SourceError) as caught:
        await YouTubeDataApiSource(KEY).fetch_video(VIDEO_ID)

    assert type(caught.value) is SourceError


async def test_playlist_item_without_a_video_id_is_a_source_error(fake: FakeYouTube) -> None:
    fake.responders["playlistItems"] = lambda _params: {"items": [{"snippet": {}}]}

    with pytest.raises(SourceError):
        await YouTubeDataApiSource(KEY).fetch_playlist(PLAYLIST_ID)


async def test_the_key_never_reaches_a_message_or_a_log(
    fake: FakeYouTube, capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture
) -> None:
    """The client puts `key=` in every request URI, and `HttpError` repeats that URI."""
    configure_logging(level="DEBUG", fmt="json")
    errors = [
        _http_error(403, _fixture("error_quota")),
        _http_error(503, _error_body(503, "backendError")),
    ]

    def failing(_params: Params) -> Mapping[str, Any]:
        raise errors.pop()

    fake.responders["videos"] = failing

    with pytest.raises(SourceError) as caught:
        await YouTubeDataApiSource(KEY).fetch_video(VIDEO_ID)

    captured = capsys.readouterr()
    retries = [json.loads(line) for line in captured.err.splitlines() if '"retry"' in line]
    assert len(retries) == 1, "the 503 was retried and the retry was logged"
    chain: list[BaseException] = []
    link: BaseException | None = caught.value
    while link is not None:
        chain.append(link)
        link = link.__cause__ or link.__context__
    for text in (
        *(str(exc) for exc in chain),
        *(repr(exc) for exc in chain),
        caught.value.hint or "",
        captured.out,
        captured.err,
        caplog.text,
    ):
        assert KEY not in text


def test_missing_extra_is_a_source_error_with_the_install_hint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(sys.modules, "googleapiclient", None)

    with pytest.raises(SourceError) as caught:
        require_extra()

    assert 'uv tool install "thumbforge[api]"' in (caught.value.hint or "")


async def test_missing_extra_surfaces_from_a_fetch_too(monkeypatch: pytest.MonkeyPatch) -> None:
    """The real `_build_client` owns the import, so a direct caller gets the same hint."""
    monkeypatch.setitem(sys.modules, "googleapiclient", None)

    with pytest.raises(SourceError) as caught:
        await YouTubeDataApiSource(KEY).fetch_video(VIDEO_ID)

    assert type(caught.value) is SourceError
    assert "thumbforge[api]" in (caught.value.hint or "")


def test_require_extra_passes_when_installed() -> None:
    require_extra()


def test_build_client_returns_a_youtube_resource_without_network() -> None:
    """The bundled discovery document is used; nothing is fetched to build the client."""
    client = youtube_api._build_client(KEY)
    assert callable(client.playlistItems)


# --- CLI -------------------------------------------------------------------------------

runner = CliRunner()


@pytest.fixture
def keyring_store(monkeypatch: pytest.MonkeyPatch) -> dict[tuple[str, str], str]:
    """An empty in-memory keyring, so no test reads or writes the developer's store."""
    store: dict[tuple[str, str], str] = {}

    def get_password(service: str, username: str) -> str | None:
        return store.get((service, username))

    monkeypatch.setattr(credentials.keyring, "get_password", get_password)
    return store


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    directory = tmp_path / "data"
    result = runner.invoke(app, ["--data-dir", str(directory), "db", "init"])
    assert result.exit_code == 0, result.stdout
    return directory


def _output(result: Any) -> str:
    return result.stdout + str(result.stderr)


def test_cli_without_a_key_exits_one_with_the_set_key_hint(
    data_dir: Path, keyring_store: dict[tuple[str, str], str]
) -> None:
    result = runner.invoke(
        app, ["--data-dir", str(data_dir), "fetch", PLAYLIST_URL, "--source", "api"]
    )

    assert result.exit_code == 1
    assert "thumbforge provider set-key api" in _output(result)
    assert credentials.env_var("api") in _output(result)


def test_cli_reads_the_key_from_the_keyring(
    data_dir: Path, fake: FakeYouTube, keyring_store: dict[tuple[str, str], str]
) -> None:
    keyring_store[credentials.SERVICE, "api"] = KEY

    result = runner.invoke(
        app, ["--data-dir", str(data_dir), "fetch", PLAYLIST_URL, "--source", "api"]
    )

    assert result.exit_code == 0, _output(result)
    assert fake.keys == [KEY]


def _channel_source(data_dir: Path) -> ChannelSource:
    engine = get_engine(data_dir / "thumbforge.sqlite3")
    try:
        with session_scope(engine) as session:
            return session.scalars(select(Channel.source)).one()
    finally:
        engine.dispose()


def test_cli_playlist_fetch_through_the_api_then_back_to_ytdlp(
    data_dir: Path,
    fake: FakeYouTube,
    keyring_store: dict[tuple[str, str], str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Spec behaviour 1: same rows from either source; a re-fetch updates `source`."""
    monkeypatch.setenv(credentials.env_var("api"), KEY)

    via_api = runner.invoke(
        app,
        ["--json", "--data-dir", str(data_dir), "fetch", PLAYLIST_URL, "--source", "api"],
    )

    assert via_api.exit_code == 0, _output(via_api)
    payload = json.loads(via_api.stdout)
    assert payload["stored"] == {"channels": 1, "playlists": 1, "videos": 12}
    assert len(payload["videos"]) == 12
    assert fake.keys == [KEY]
    assert _channel_source(data_dir) is ChannelSource.API
    assert KEY not in _output(via_api)

    ytdlp_fixtures = FIXTURES / "ytdlp"

    def extract(url: str, flat: bool, items: str | None = None) -> dict[str, Any]:
        name = "playlist" if "list=" in url else "channel"
        return json.loads((ytdlp_fixtures / f"{name}.json").read_text(encoding="utf-8"))

    monkeypatch.setattr(ytdlp, "_extract_with_ytdlp", extract)
    via_ytdlp = runner.invoke(
        app,
        [
            "--json",
            "--data-dir",
            str(data_dir),
            "fetch",
            PLAYLIST_URL,
            "--source",
            "ytdlp",
            "--refresh",
        ],
    )

    assert via_ytdlp.exit_code == 0, _output(via_ytdlp)
    again = json.loads(via_ytdlp.stdout)
    assert [v["youtube_id"] for v in again["videos"]] == [
        v["youtube_id"] for v in payload["videos"]
    ]
    assert _channel_source(data_dir) is ChannelSource.YTDLP
