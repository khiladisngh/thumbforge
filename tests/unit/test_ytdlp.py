"""`YtDlpSource` against recorded fixtures — no network, no `yt_dlp` call (ROADMAP P2.2).

The fixtures are real yt-dlp output, recorded by `tests/integration/test_ytdlp_record.py`,
so these tests pin the mapping against shapes YouTube actually returns rather than a
hand-written idea of them.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, cast

import pytest
from tenacity import wait_none
from yt_dlp.networking.exceptions import HTTPError, TransportError
from yt_dlp.utils import DownloadError, ExtractorError

from thumbforge.core.enums import ChannelSource, UrlKind
from thumbforge.core.errors import (
    ExitCode,
    NotFoundError,
    SourceError,
    SourceTransientError,
)
from thumbforge.logging import configure_logging
from thumbforge.sources import MetadataSource, ytdlp
from thumbforge.sources.ytdlp import YtDlpSource, _translate

if TYPE_CHECKING:
    from collections.abc import Mapping

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "ytdlp"


def _fixture(name: str) -> dict[str, Any]:
    return json.loads((FIXTURES / f"{name}.json").read_text(encoding="utf-8"))


class _Recorder:
    """Extractor stub that returns a fixture and remembers how it was called."""

    def __init__(self, info: Mapping[str, Any]) -> None:
        self.info = info
        self.calls: list[tuple[str, bool, str | None]] = []

    def __call__(self, url: str, flat: bool, items: str | None = None) -> Mapping[str, Any]:
        self.calls.append((url, flat, items))
        return self.info


def _source(name: str) -> tuple[YtDlpSource, _Recorder]:
    recorder = _Recorder(_fixture(name))
    return YtDlpSource(recorder), recorder


def test_satisfies_the_metadata_source_protocol() -> None:
    """`cli/fetch.py` selects a source by Protocol, so drift here breaks dispatch."""
    assert isinstance(YtDlpSource(), MetadataSource)
    assert YtDlpSource.key == ChannelSource.YTDLP.value


async def test_resolve_needs_no_extraction() -> None:
    """Classification is pure, so `resolve` must not spend a network call."""
    source, recorder = _source("video")
    resolved = await source.resolve("https://youtu.be/dQw4w9WgXcQ")
    assert resolved.kind is UrlKind.VIDEO
    assert recorder.calls == []


async def test_fetch_video_uses_a_full_extract() -> None:
    """A single video must be extracted deeply: that is the only way to get description."""
    source, recorder = _source("video")
    video = await source.fetch_video("jNQXAC9IVRw")

    assert recorder.calls == [("https://www.youtube.com/watch?v=jNQXAC9IVRw", False, None)]
    assert video.youtube_id == "jNQXAC9IVRw"
    assert video.title
    assert video.description
    assert video.duration_s == 19
    assert video.channel_id == "UC4QobU6STFB0P71PMvOGN5A"
    assert video.published_at == datetime(2005, 4, 24, 3, 31, 52, tzinfo=UTC)
    assert video.source_thumbnail_url is not None
    assert video.fetched_at.tzinfo is UTC


async def test_fetch_playlist_numbers_items_by_order() -> None:
    """`position` comes from enumeration order because `playlist_index` is absent (S11)."""
    source, recorder = _source("playlist")
    playlist = await source.fetch_playlist("PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI")

    url = "https://www.youtube.com/playlist?list=PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI"
    assert recorder.calls == [(url, True, None)]
    assert playlist.item_count == 12
    assert [item.position for item in playlist.items] == list(range(1, 13))
    assert playlist.channel_id == "UC-9-kyTW8ZkZNDHQJ6FgpwQ"

    # Order must match the fixture's entry order, not a set or a sort.
    expected = [entry["id"] for entry in _fixture("playlist")["entries"]]
    assert [item.video.youtube_id for item in playlist.items] == expected


async def test_playlist_videos_have_no_description_or_publish_date() -> None:
    """S11: a flat extract cannot supply these, so the defaults must survive.

    Asserting this stops a later "improvement" from quietly fanning out one full extract
    per item to fill them in, which for a 183-video playlist is 183 network round trips.
    """
    source, _ = _source("playlist")
    playlist = await source.fetch_playlist("PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI")

    assert all(item.video.description == "" for item in playlist.items)
    assert all(item.video.published_at is None for item in playlist.items)
    # Everything a flat entry *does* carry must be populated.
    assert all(item.video.title for item in playlist.items)
    assert all(item.video.duration_s is not None for item in playlist.items)
    assert all(item.video.channel_id for item in playlist.items)


async def test_fetch_channel_asks_for_no_items() -> None:
    """Enumerating a channel is a non-goal and expensive, so pin the cheap request."""
    source, recorder = _source("channel")
    channel = await source.fetch_channel("UC-9-kyTW8ZkZNDHQJ6FgpwQ")

    url = "https://www.youtube.com/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ"
    assert recorder.calls == [(url, True, "0")]
    assert channel.youtube_id == "UC-9-kyTW8ZkZNDHQJ6FgpwQ"
    assert channel.title == "Music"


async def test_fetch_channel_accepts_a_handle() -> None:
    """`@handle` is not a `UC…` id, so it must not be pasted into the /channel/ path."""
    source, recorder = _source("channel")
    await source.fetch_channel("@mkbhd")
    assert recorder.calls == [("https://www.youtube.com/@mkbhd", True, "0")]


async def test_unfetchable_playlist_entries_are_dropped_without_leaving_holes() -> None:
    """yt-dlp yields `None` for a deleted video; positions must stay contiguous."""
    info = _fixture("playlist")
    info["entries"] = [info["entries"][0], None, info["entries"][1]]
    source = YtDlpSource(_Recorder(info))

    playlist = await source.fetch_playlist("PL0000000000000000")
    assert [item.position for item in playlist.items] == [1, 2]


async def test_entry_without_an_id_is_a_source_error() -> None:
    """A video id is the one field nothing can be reconstructed from."""
    info = _fixture("playlist")
    info["entries"] = [{"title": "no id here"}]
    source = YtDlpSource(_Recorder(info))

    with pytest.raises(SourceError):
        await source.fetch_playlist("PL0000000000000000")


async def test_transient_failures_are_retried_then_reraised(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Three attempts, then exit 1 — `SourceTransientError` keeps `SourceError`'s code."""
    # Neutralise the backoff clock: the policy is under test, not PLAN.md's 2s/4s waits.
    monkeypatch.setattr(ytdlp, "_RETRY_WAIT", wait_none())
    attempts = 0

    def failing(url: str, flat: bool, items: str | None = None) -> dict[str, Any]:
        nonlocal attempts
        attempts += 1
        msg = "connection reset"
        raise SourceTransientError(msg)

    with pytest.raises(SourceTransientError) as caught:
        await YtDlpSource(failing, attempts=3).fetch_video("dQw4w9WgXcQ")

    assert attempts == 3
    assert caught.value.exit_code is ExitCode.UNEXPECTED


async def test_permanent_failures_are_not_retried() -> None:
    """A missing video will still be missing on attempt three; retrying just wastes time."""
    attempts = 0

    def missing(url: str, flat: bool, items: str | None = None) -> dict[str, Any]:
        nonlocal attempts
        attempts += 1
        msg = "This video is unavailable"
        raise NotFoundError(msg)

    with pytest.raises(NotFoundError):
        await YtDlpSource(missing).fetch_video("aaaaaaaaaaa")
    assert attempts == 1


async def test_retry_emits_a_log_event(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Phase 2 acceptance criteria require retries to be observable in the logs."""
    monkeypatch.setattr(ytdlp, "_RETRY_WAIT", wait_none())
    configure_logging(level="INFO", fmt="json")

    def failing(url: str, flat: bool, items: str | None = None) -> dict[str, Any]:
        msg = "connection reset"
        raise SourceTransientError(msg)

    with pytest.raises(SourceTransientError):
        await YtDlpSource(failing, attempts=2).fetch_video("dQw4w9WgXcQ")

    events = [json.loads(line) for line in capsys.readouterr().err.splitlines() if line]
    retries = [event for event in events if event["event"] == "retry"]
    assert [event["attempt"] for event in retries] == [1]
    assert retries[0]["error"] == "connection reset"


def _download_error(inner: Exception) -> DownloadError:
    """Wrap an exception the way `YoutubeDL.extract_info` does, traceback included."""
    try:
        raise inner
    except Exception:
        return DownloadError(str(inner), cast("Any", sys.exc_info()))


def test_network_failure_maps_to_a_transient_error() -> None:
    """Measured shape: a network failure arrives as a `TransportError` subclass."""
    mapped = _translate(_download_error(TransportError("connection reset")), "https://x")
    assert isinstance(mapped, SourceTransientError)


def test_unavailable_video_maps_to_not_found() -> None:
    """`expected=True` is yt-dlp's own flag for "YouTube said no", so exit 3, not 1."""
    inner = ExtractorError("This video is unavailable", expected=True)
    mapped = _translate(_download_error(inner), "https://x")
    assert isinstance(mapped, NotFoundError)
    assert mapped.exit_code is ExitCode.NOT_FOUND


def test_unexpected_extractor_failure_maps_to_source_error() -> None:
    """A yt-dlp bug is not a missing video: it must not be reported as exit 3."""
    inner = ExtractorError("Unable to extract yt initial data", expected=False)
    mapped = _translate(_download_error(inner), "https://x")
    assert type(mapped) is SourceError
    assert mapped.exit_code is ExitCode.UNEXPECTED


def test_network_error_wrapped_by_the_extractor_is_still_transient() -> None:
    """yt-dlp's top-level handler hides a network failure behind `expected=True`.

    `IE.extract()` raises `ExtractorError("A network error has occurred.", cause=e,
    expected=True)`. Classifying on `expected` before inspecting `cause` would report a
    retryable network failure as a missing video: exit 3, and no retries at all.
    """
    inner = ExtractorError(
        "A network error has occurred.", cause=TransportError("connection reset"), expected=True
    )
    mapped = _translate(_download_error(inner), "https://x")
    assert isinstance(mapped, SourceTransientError)


def test_retryable_http_status_behind_the_extractor_wrapper_is_transient() -> None:
    """A 503 nested in an `ExtractorError` must retry, not fail as "not found"."""
    response = SimpleNamespace(status=503, reason="Service Unavailable")
    inner = ExtractorError("boom", cause=HTTPError(cast("Any", response)), expected=True)
    mapped = _translate(_download_error(inner), "https://x")
    assert isinstance(mapped, SourceTransientError)


def test_cause_chain_survives_a_cycle() -> None:
    """`cause` is a plain attribute yt-dlp sets, so nothing guarantees it terminates."""
    first = ExtractorError("a", expected=True)
    second = ExtractorError("b", expected=True)
    first.cause = second
    second.cause = first

    mapped = _translate(_download_error(first), "https://x")
    assert isinstance(mapped, NotFoundError)


@pytest.mark.parametrize(
    ("label", "entries"),
    [
        ("entries is not iterable", 7),
        ("an entry is not a mapping", ["oops"]),
        ("thumbnails is not iterable", [{"id": "x" * 11, "thumbnails": 5}]),
    ],
)
async def test_unexpected_metadata_shape_is_a_source_error(label: str, entries: Any) -> None:
    """A YouTube change can make yt-dlp return the wrong type for a field.

    Without the boundary guard these raise `TypeError`/`AttributeError`, which escape
    `handle_errors` (it only catches `ThumbforgeError`) and show the user a traceback.
    """
    info = {"id": "PL0000000000000000", "title": "t", "entries": entries}
    source = YtDlpSource(_Recorder(info))

    with pytest.raises(SourceError) as caught:
        await source.fetch_playlist("PL0000000000000000")
    assert caught.value.exit_code is ExitCode.UNEXPECTED
    assert caught.value.hint is not None
