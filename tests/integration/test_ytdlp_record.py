"""Record `tests/fixtures/ytdlp/*.json` from live YouTube, and assert the S11 field set.

Marked `integration`, so the default `pytest` run (`-m 'not integration'`) never hits the
network. Re-record after a yt-dlp upgrade changes the info-dict shape:

    uv run pytest -m integration tests/integration/test_ytdlp_record.py

The recorded JSON is committed. Recording is the *only* place live YouTube is touched; every
other test replays these files, which is what keeps the unit suite deterministic and offline.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from thumbforge.sources.ytdlp import _extract_with_ytdlp

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "ytdlp"

#: "Popular Music Videos" — large, public and stable; the same playlist spike S11 measured.
PLAYLIST_ID = "PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI"
#: "Me at the zoo", the oldest video on YouTube: public, short, and never going away.
VIDEO_ID = "jNQXAC9IVRw"
#: The channel that owns the playlist above.
CHANNEL_ID = "UC-9-kyTW8ZkZNDHQJ6FgpwQ"

#: Keep the playlist fixture reviewable. The spec's acceptance criteria count 12 videos.
FIXTURE_ITEMS = "1:12"

#: Media-delivery keys stripped before writing. thumbforge sets `skip_download` and never
#: reads any of these, yet together they are ~80 KB of the ~87 KB a full extract returns,
#: which would make the fixture unreviewable. Every field the source *does* read is kept
#: verbatim, so the fixture still exercises real yt-dlp values.
DROPPED_KEYS = frozenset(
    {
        "_format_sort_fields",
        "automatic_captions",
        # When the extraction ran. Nothing reads it, and keeping it makes every re-record a
        # dirty diff even when YouTube returned identical metadata.
        "epoch",
        "formats",
        "heatmap",
        "requested_formats",
        "subtitles",
    }
)

pytestmark = pytest.mark.integration


def _write(name: str, info: Any) -> None:
    """Persist an info dict, minus the media-delivery keys listed in `DROPPED_KEYS`."""
    FIXTURES.mkdir(parents=True, exist_ok=True)
    trimmed = {key: value for key, value in info.items() if key not in DROPPED_KEYS}
    # indent=2 matches prettier, which owns every *.json outside graphify-out/. With any
    # other width a re-record and the pre-commit hook fight, and the diff is 900 lines of
    # indentation instead of the field changes a yt-dlp upgrade actually made (#31).
    payload = json.dumps(trimmed, indent=2, sort_keys=True, default=str)
    (FIXTURES / f"{name}.json").write_text(payload + "\n", encoding="utf-8")


def test_record_video(capsys: pytest.CaptureFixture[str]) -> None:
    """A full extract must carry the fields a flat entry cannot (S11).

    Also the only place the real yt-dlp runs, so it is where the stdout contract is
    checkable: Rich tables own stdout (`PLAN.md` §7.3), and yt-dlp is handed a stdlib
    logger precisely so its own `ERROR:`/`WARNING:` writes cannot land there.
    """
    info = _extract_with_ytdlp(f"https://www.youtube.com/watch?v={VIDEO_ID}", False, None)
    assert capsys.readouterr().out == ""
    assert info["id"] == VIDEO_ID
    for key in ("title", "description", "duration", "channel_id", "timestamp", "thumbnail"):
        assert info.get(key) is not None, f"full extract lost {key}"
    _write("video", info)


def test_record_playlist() -> None:
    """Re-assert the S11 field set, so a yt-dlp upgrade that changes it fails loudly."""
    info = _extract_with_ytdlp(
        f"https://www.youtube.com/playlist?list={PLAYLIST_ID}", True, FIXTURE_ITEMS
    )
    assert info["id"] == PLAYLIST_ID
    assert info["channel_id"] == CHANNEL_ID
    entries = info["entries"]
    assert len(entries) == 12

    for entry in entries:
        for key in ("id", "title", "duration", "channel_id", "url", "thumbnails"):
            assert entry.get(key) is not None, f"flat entry lost {key}"
        # The two findings this module is built on. If either flips, yt-dlp changed and
        # fetch_playlist's position and description handling has to be revisited.
        assert "playlist_index" not in entry
        assert "description" not in entry

    _write("playlist", info)


def test_record_channel() -> None:
    """`playlist_items="0"` must return channel fields and no entries."""
    info = _extract_with_ytdlp(f"https://www.youtube.com/channel/{CHANNEL_ID}", True, "0")
    assert info["channel_id"] == CHANNEL_ID
    assert info["title"]
    assert not info.get("entries")
    _write("channel", info)
