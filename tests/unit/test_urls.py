"""Which YouTube URLs and ids resolve to which kind (ADR 0005, ROADMAP P2.1)."""

from __future__ import annotations

import pytest

from thumbforge.core.enums import UrlKind
from thumbforge.core.errors import ExitCode, UrlError
from thumbforge.core.urls import classify_url

VIDEO_ID = "dQw4w9WgXcQ"
PLAYLIST_ID = "PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI"
CHANNEL_ID = "UCuAXFkgsw1L7xaCfnd5JJOw"


@pytest.mark.parametrize(
    ("url", "kind", "youtube_id"),
    [
        # Video forms
        (f"https://www.youtube.com/watch?v={VIDEO_ID}", UrlKind.VIDEO, VIDEO_ID),
        (f"https://youtu.be/{VIDEO_ID}", UrlKind.VIDEO, VIDEO_ID),
        (f"https://www.youtube.com/shorts/{VIDEO_ID}", UrlKind.VIDEO, VIDEO_ID),
        (f"https://www.youtube.com/embed/{VIDEO_ID}", UrlKind.VIDEO, VIDEO_ID),
        (f"https://www.youtube.com/live/{VIDEO_ID}", UrlKind.VIDEO, VIDEO_ID),
        (f"https://m.youtube.com/watch?v={VIDEO_ID}", UrlKind.VIDEO, VIDEO_ID),
        (f"youtube.com/watch?v={VIDEO_ID}", UrlKind.VIDEO, VIDEO_ID),
        (VIDEO_ID, UrlKind.VIDEO, VIDEO_ID),
        # Playlist forms
        (f"https://www.youtube.com/playlist?list={PLAYLIST_ID}", UrlKind.PLAYLIST, PLAYLIST_ID),
        (f"https://www.youtube.com/watch?list={PLAYLIST_ID}", UrlKind.PLAYLIST, PLAYLIST_ID),
        (PLAYLIST_ID, UrlKind.PLAYLIST, PLAYLIST_ID),
        # Channel forms
        (f"https://www.youtube.com/channel/{CHANNEL_ID}", UrlKind.CHANNEL, CHANNEL_ID),
        ("https://www.youtube.com/@channelhandle", UrlKind.CHANNEL, "@channelhandle"),
        ("https://www.youtube.com/c/SomeName", UrlKind.CHANNEL, "SomeName"),
        ("https://www.youtube.com/user/SomeName", UrlKind.CHANNEL, "SomeName"),
        ("@channelhandle", UrlKind.CHANNEL, "@channelhandle"),
        (CHANNEL_ID, UrlKind.CHANNEL, CHANNEL_ID),
    ],
)
def test_classify_url(url: str, kind: UrlKind, youtube_id: str) -> None:
    """Every URL form thumbforge accepts, and the exact identifier it must extract."""
    resolved = classify_url(url)
    assert resolved.kind is kind
    assert resolved.youtube_id == youtube_id


def test_watch_url_with_list_resolves_to_the_video() -> None:
    """`v=` wins over `list=`: the URL names a video being watched inside a playlist.

    Fetching the whole playlist here would silently pull in dozens of videos the user
    did not ask for; `/playlist?list=…` is the way to mean the playlist.
    """
    resolved = classify_url(f"https://www.youtube.com/watch?v={VIDEO_ID}&list={PLAYLIST_ID}")
    assert resolved.kind is UrlKind.VIDEO
    assert resolved.youtube_id == VIDEO_ID


def test_surrounding_whitespace_is_tolerated() -> None:
    """Pasted URLs routinely carry a trailing newline or space."""
    assert classify_url(f"  https://youtu.be/{VIDEO_ID}  ").youtube_id == VIDEO_ID


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
        "https://vimeo.com/123456",
        "https://example.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/",
        "https://www.youtube.com/playlist",
        "https://youtu.be/",
        "not-an-id",
        "https://www.youtube.com/watch?v=tooshort",
    ],
)
def test_unrecognised_input_is_a_usage_error(value: str) -> None:
    """Bad input must be a usage error (exit 2), not a source failure or a crash."""
    with pytest.raises(UrlError) as caught:
        classify_url(value)
    assert caught.value.exit_code is ExitCode.USAGE
    assert caught.value.hint is not None


@pytest.mark.parametrize(
    "value",
    [
        f"https://youtu.be/{PLAYLIST_ID}",
        f"https://youtu.be/{CHANNEL_ID}",
        f"https://www.youtube.com/watch?v={PLAYLIST_ID}",
        f"https://www.youtube.com/shorts/{PLAYLIST_ID}",
        f"https://www.youtube.com/channel/{VIDEO_ID}",
        f"https://www.youtube.com/playlist?list={VIDEO_ID}",
        f"https://www.youtube.com/watch?list={VIDEO_ID}",
    ],
)
def test_identifier_must_match_the_kind_its_url_form_promises(value: str) -> None:
    """An explicit form fixes the kind; the id's shape must not override it.

    `youtu.be` only serves videos and `/channel/` only channels, so a playlist-shaped id in
    a short link is malformed input. Classifying by shape here would resolve it to
    `PLAYLIST` and send `fetch` to `fetch_playlist` for a host that has no playlists.
    """
    with pytest.raises(UrlError) as caught:
        classify_url(value)
    assert caught.value.exit_code is ExitCode.USAGE


@pytest.mark.parametrize("value", ["@", "https://www.youtube.com/@"])
def test_empty_channel_handle_is_rejected(value: str) -> None:
    """`@` alone names no channel, so it must not resolve successfully."""
    with pytest.raises(UrlError):
        classify_url(value)


@pytest.mark.parametrize("value", ["https://[::1", "https://[not-an-ipv6]"])
def test_malformed_authority_is_a_usage_error(value: str) -> None:
    """`urlparse` raises `ValueError` on these; the CLI only handles `ThumbforgeError`.

    Letting the `ValueError` escape would turn bad input into an unexpected-error exit
    instead of the documented usage exit. Asserting the `__cause__` keeps this test honest:
    without it, a case that merely fails the host check would pass for the wrong reason.
    """
    with pytest.raises(UrlError) as caught:
        classify_url(value)
    assert caught.value.exit_code is ExitCode.USAGE
    assert isinstance(caught.value.__cause__, ValueError)
