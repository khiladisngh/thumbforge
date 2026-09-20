"""Classify YouTube URLs and bare identifiers (ADR 0005, ROADMAP P2.1).

Pure pattern matching, no network: every `MetadataSource` resolves input the same way, so
the rules live here rather than in `sources/ytdlp.py` and get reused verbatim by the Data
API source in Phase 8.
"""

from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse

from thumbforge.core.enums import UrlKind
from thumbforge.core.errors import UrlError
from thumbforge.core.models import ResolvedUrl

#: Hosts that serve YouTube content. `youtu.be` is the short-link form.
_YOUTUBE_HOSTS = frozenset(
    {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "music.youtube.com",
        "youtube-nocookie.com",
        "www.youtube-nocookie.com",
    }
)
_SHORT_HOSTS = frozenset({"youtu.be", "www.youtu.be"})

#: A video id is exactly 11 URL-safe base64 characters.
_VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
#: A channel id is `UC` plus 22 more characters.
_CHANNEL_ID = re.compile(r"^UC[A-Za-z0-9_-]{22}$")
#: Playlist ids carry a type prefix; `UU`/`LL`/`FL` are the auto-generated ones.
_PLAYLIST_ID = re.compile(r"^(?:PL|UU|LL|FL|OL|RD)[A-Za-z0-9_-]{10,}$")

#: Path segments that introduce a video id: /shorts/<id>, /embed/<id>, /live/<id>, /v/<id>.
_VIDEO_PATH_PREFIXES = frozenset({"shorts", "embed", "live", "v"})
#: Path segments that introduce a channel: /c/<name>, /user/<name>.
_CHANNEL_PATH_PREFIXES = frozenset({"c", "user"})


def classify_id(value: str) -> ResolvedUrl:
    """Classify a bare YouTube identifier by its shape.

    Order matters: a channel id (`UC…`) and an auto-generated playlist id (`UU…`) share a
    two-letter prefix style, and both are longer than the 11-character video id, so the
    most specific pattern is tried first.
    """
    candidate = value.strip()
    if _CHANNEL_ID.fullmatch(candidate):
        return ResolvedUrl(kind=UrlKind.CHANNEL, youtube_id=candidate)
    if _PLAYLIST_ID.fullmatch(candidate):
        return ResolvedUrl(kind=UrlKind.PLAYLIST, youtube_id=candidate)
    if _VIDEO_ID.fullmatch(candidate):
        return ResolvedUrl(kind=UrlKind.VIDEO, youtube_id=candidate)
    msg = f"not a recognisable YouTube id: {value!r}"
    raise UrlError(msg, hint="pass a video, playlist or channel id, or a full YouTube URL")


def _expect_kind(value: str, kind: UrlKind, form: str) -> ResolvedUrl:
    """Classify `value` and require it to be the kind its URL form promises.

    An explicit URL form carries the authoritative kind: `youtu.be/<id>` only ever serves a
    video, `/channel/<id>` only ever a channel. Trusting the identifier's *shape* instead
    would let `youtu.be/PLxxxxxxxxxx` resolve to a playlist and send `fetch` to
    `fetch_playlist` for a host that has no playlists.
    """
    resolved = classify_id(value)
    if resolved.kind is not kind:
        msg = f"{form} carries a {resolved.kind.value} id, not a {kind.value} id: {value!r}"
        raise UrlError(msg, hint=f"expected a {kind.value} id in this URL form")
    return resolved


def _channel_handle(handle: str, original: str) -> ResolvedUrl:
    """Accept an `@handle` only when it actually names something after the `@`."""
    if len(handle) < 2:
        msg = f"channel handle is empty: {original!r}"
        raise UrlError(msg, hint="expected @<handle>, for example @youtube")
    return ResolvedUrl(kind=UrlKind.CHANNEL, youtube_id=handle)


def classify_url(value: str) -> ResolvedUrl:
    """Resolve a YouTube URL, handle or bare id to its kind and identifier.

    A `watch` URL that also carries `list=` resolves to the **video**: the URL names one
    video being watched in a playlist's context, and `fetch` should not silently pull in
    the whole playlist. Use the `/playlist?list=…` form to mean the playlist.
    """
    candidate = value.strip()
    if not candidate:
        msg = "empty URL"
        raise UrlError(msg, hint="pass a YouTube video, playlist or channel URL")

    # A bare handle is unambiguous even without a host, but `@` alone names nothing.
    if candidate.startswith("@") and "/" not in candidate:
        return _channel_handle(candidate, value)

    if "://" not in candidate and "/" not in candidate and "." not in candidate:
        return classify_id(candidate)

    try:
        parsed = urlparse(candidate if "://" in candidate else f"https://{candidate}")
        host = (parsed.hostname or "").lower()
    except ValueError as exc:
        # urlparse raises on a malformed authority — an unmatched or non-address IPv6
        # bracket. That is bad input, so it must surface as the documented usage error
        # rather than escape `handle_errors`, which only catches ThumbforgeError.
        msg = f"malformed URL: {value!r}"
        raise UrlError(msg, hint="pass a YouTube video, playlist or channel URL") from exc

    if host not in _YOUTUBE_HOSTS and host not in _SHORT_HOSTS:
        msg = f"not a YouTube URL: {value!r}"
        raise UrlError(msg, hint="only youtube.com and youtu.be URLs are supported")

    segments = [segment for segment in parsed.path.split("/") if segment]
    query = parse_qs(parsed.query)

    if host in _SHORT_HOSTS:
        # youtu.be/<video id>; a bare youtu.be/ carries nothing to fetch.
        if segments:
            return _expect_kind(segments[0], UrlKind.VIDEO, "short URL")
        msg = f"short URL names no video: {value!r}"
        raise UrlError(msg, hint="expected youtu.be/<video id>")

    if video_ids := query.get("v"):
        return _expect_kind(video_ids[0], UrlKind.VIDEO, "v= parameter")

    if segments:
        head = segments[0].lower()
        if head == "playlist":
            if list_ids := query.get("list"):
                return _expect_kind(list_ids[0], UrlKind.PLAYLIST, "list= parameter")
            msg = f"playlist URL names no list: {value!r}"
            raise UrlError(msg, hint="expected /playlist?list=<playlist id>")
        if head in _VIDEO_PATH_PREFIXES and len(segments) > 1:
            return _expect_kind(segments[1], UrlKind.VIDEO, f"/{head}/ URL")
        if head == "channel" and len(segments) > 1:
            return _expect_kind(segments[1], UrlKind.CHANNEL, "/channel/ URL")
        if head in _CHANNEL_PATH_PREFIXES and len(segments) > 1:
            # /c/<name> and /user/<name> carry a channel name, not a shape-classifiable id.
            return ResolvedUrl(kind=UrlKind.CHANNEL, youtube_id=segments[1])
        if head.startswith("@"):
            return _channel_handle(head, value)

    # A `list=` with no `v=` and no /playlist path (e.g. /watch?list=…) is still a playlist.
    if list_ids := query.get("list"):
        return _expect_kind(list_ids[0], UrlKind.PLAYLIST, "list= parameter")

    msg = f"cannot tell what this YouTube URL refers to: {value!r}"
    raise UrlError(msg, hint="expected a video, playlist or channel URL")
