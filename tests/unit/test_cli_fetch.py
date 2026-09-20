"""`fetch`, `video` and `playlist` through `CliRunner`, with no network (ROADMAP P2.3).

`build_source` is patched so the commands run against canned metadata. Everything else —
the database, the session handling, the rendering — is the real code path, which is what
makes the `--json` contract and the exit codes meaningful here.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, ClassVar

import pytest
from typer.testing import CliRunner

from thumbforge.cli import fetch as fetch_cli
from thumbforge.cli.app import app
from thumbforge.core.models import (
    ChannelMeta,
    PlaylistItemMeta,
    PlaylistMeta,
    ResolvedUrl,
    VideoMeta,
)
from thumbforge.core.urls import classify_url

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()

OWNER = "UC" + "o" * 22
PLAYLIST = "PL" + "p" * 16
VIDEO = "dQw4w9WgXcQ"
PLAYLIST_URL = f"https://www.youtube.com/playlist?list={PLAYLIST}"


class StubSource:
    """Canned metadata standing in for `YtDlpSource`."""

    key: ClassVar[str] = "ytdlp"
    titles: ClassVar[tuple[str, ...]] = ("First part", "Second part")

    def __init__(self) -> None:
        self.fetches = 0

    async def resolve(self, url: str) -> ResolvedUrl:
        return classify_url(url)

    async def fetch_video(self, youtube_id: str) -> VideoMeta:
        self.fetches += 1
        return VideoMeta(
            youtube_id=youtube_id,
            title="Me at the zoo",
            url=f"https://youtu.be/{youtube_id}",
            channel_id=OWNER,
            description="The first video",
            duration_s=19,
        )

    async def fetch_playlist(self, youtube_id: str) -> PlaylistMeta:
        self.fetches += 1
        return PlaylistMeta(
            youtube_id=youtube_id,
            title="Rust for Pythonistas",
            url=PLAYLIST_URL,
            channel_id=OWNER,
            items=tuple(
                PlaylistItemMeta(
                    video=VideoMeta(
                        youtube_id=f"vid{index:08d}",
                        title=title,
                        url="https://youtu.be/x",
                        channel_id=OWNER,
                        duration_s=60 * index,
                    ),
                    position=index,
                )
                for index, title in enumerate(self.titles, start=1)
            ),
        )

    async def fetch_channel(self, youtube_id: str) -> ChannelMeta:
        self.fetches += 1
        return ChannelMeta(youtube_id=youtube_id, title="channel-name", url="https://yt/c")


@pytest.fixture
def source(monkeypatch: pytest.MonkeyPatch) -> StubSource:
    """Replace the real source so no test touches the network."""
    stub = StubSource()
    # Patch the name *as imported by the command module*: `cli.fetch` does
    # `from ._youtube import build_source`, so patching `_youtube.build_source` would leave
    # the already-bound reference alone and the real YtDlpSource would hit the network.
    monkeypatch.setattr(fetch_cli, "build_source", lambda _source: stub)
    return stub


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    """An initialised database, since every command here needs the schema."""
    directory = tmp_path / "data"
    result = runner.invoke(app, ["--data-dir", str(directory), "db", "init"])
    assert result.exit_code == 0, result.stdout
    return directory


def test_fetch_playlist_prints_the_panel_table_and_summary(
    data_dir: Path, source: StubSource
) -> None:
    """The `PLAN.md` §5.3 shape: panel, `#`/`Part` table, then the stored counts."""
    result = runner.invoke(app, ["--data-dir", str(data_dir), "fetch", PLAYLIST_URL])

    assert result.exit_code == 0, result.stdout
    assert "Rust for Pythonistas" in result.stdout
    assert "channel-name" in result.stdout
    assert "First part" in result.stdout
    assert "Stored 1 channel, 1 playlist, 2 videos." in result.stdout


def test_refetch_within_the_window_is_cached_and_makes_no_calls(
    data_dir: Path, source: StubSource
) -> None:
    """Spec acceptance criteria: same table, `(cached)`, and no source call."""
    first = runner.invoke(app, ["--data-dir", str(data_dir), "fetch", PLAYLIST_URL])
    assert first.exit_code == 0, first.stdout
    calls_after_first = source.fetches

    second = runner.invoke(app, ["--data-dir", str(data_dir), "fetch", PLAYLIST_URL])

    assert second.exit_code == 0, second.stdout
    assert "(cached)" in second.stdout
    assert "First part" in second.stdout
    assert source.fetches == calls_after_first


def test_refresh_forces_a_fetch(data_dir: Path, source: StubSource) -> None:
    """`--refresh` bypasses the freshness rule."""
    runner.invoke(app, ["--data-dir", str(data_dir), "fetch", PLAYLIST_URL])
    calls_after_first = source.fetches

    result = runner.invoke(app, ["--data-dir", str(data_dir), "fetch", PLAYLIST_URL, "--refresh"])

    assert result.exit_code == 0, result.stdout
    assert "(cached)" not in result.stdout
    assert source.fetches > calls_after_first


def test_fetch_json_emits_one_object_with_the_kind(data_dir: Path, source: StubSource) -> None:
    """Spec behaviour 6: a single JSON object, keyed by what was fetched."""
    result = runner.invoke(
        app, ["--json", "--data-dir", str(data_dir), "fetch", f"https://youtu.be/{VIDEO}"]
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["kind"] == "video"
    assert payload["video"]["youtube_id"] == VIDEO
    assert payload["channel"]["title"] == "channel-name"
    assert payload["stored"] == {"channels": 1, "playlists": 0, "videos": 1}


def test_fetch_playlist_json_lists_items_in_order(data_dir: Path, source: StubSource) -> None:
    """The item array is the machine form of the table, so order and `part_number` matter."""
    result = runner.invoke(app, ["--json", "--data-dir", str(data_dir), "fetch", PLAYLIST_URL])

    payload = json.loads(result.stdout)
    assert [item["position"] for item in payload["videos"]] == [1, 2]
    assert [item["part_number"] for item in payload["videos"]] == [1, 2]
    assert payload["videos"][0]["title"] == "First part"


def test_fetch_channel_url_stores_only_the_channel(data_dir: Path, source: StubSource) -> None:
    """Channel enumeration is a non-goal, so no videos may appear."""
    result = runner.invoke(
        app,
        [
            "--json",
            "--data-dir",
            str(data_dir),
            "fetch",
            f"https://www.youtube.com/channel/{OWNER}",
        ],
    )

    payload = json.loads(result.stdout)
    assert payload["kind"] == "channel"
    assert payload["stored"] == {"channels": 1, "playlists": 0, "videos": 0}


def test_source_api_exits_two_with_the_install_hint(data_dir: Path) -> None:
    """Spec behaviour 3, and it must not surface as an ImportError."""
    result = runner.invoke(
        app, ["--data-dir", str(data_dir), "fetch", PLAYLIST_URL, "--source", "api"]
    )

    assert result.exit_code == 2
    assert "api` extra" in result.stdout + str(result.stderr)


def test_unrecognised_url_exits_two(data_dir: Path, source: StubSource) -> None:
    """A non-YouTube URL is input validation, not a source failure."""
    result = runner.invoke(app, ["--data-dir", str(data_dir), "fetch", "https://vimeo.com/1"])

    assert result.exit_code == 2


def test_video_show_accepts_id_and_url(data_dir: Path, source: StubSource) -> None:
    """Spec behaviour 4: a ULID, a YouTube id or a URL all resolve to the same row."""
    runner.invoke(app, ["--data-dir", str(data_dir), "fetch", f"https://youtu.be/{VIDEO}"])

    by_id = runner.invoke(app, ["--json", "--data-dir", str(data_dir), "video", "show", VIDEO])
    assert by_id.exit_code == 0, by_id.stdout
    payload = json.loads(by_id.stdout)

    by_url = runner.invoke(
        app,
        ["--json", "--data-dir", str(data_dir), "video", "show", f"https://youtu.be/{VIDEO}"],
    )
    assert json.loads(by_url.stdout)["id"] == payload["id"]

    by_ulid = runner.invoke(
        app, ["--json", "--data-dir", str(data_dir), "video", "show", payload["id"]]
    )
    assert json.loads(by_ulid.stdout)["id"] == payload["id"]


def test_video_show_unknown_exits_three(data_dir: Path) -> None:
    """Spec acceptance criteria: exit 3 and `not_found: video 'doesnotexist'`."""
    result = runner.invoke(app, ["--data-dir", str(data_dir), "video", "show", "doesnotexist"])

    assert result.exit_code == 3
    assert "not_found: video 'doesnotexist'" in result.stdout + str(result.stderr)


def test_video_list_filters_by_channel_and_limit(data_dir: Path, source: StubSource) -> None:
    """`--channel` and `--limit` must bound the query."""
    runner.invoke(app, ["--data-dir", str(data_dir), "fetch", PLAYLIST_URL])

    listed = runner.invoke(
        app, ["--json", "--data-dir", str(data_dir), "video", "list", "--channel", OWNER]
    )
    assert json.loads(listed.stdout)["count"] == 2

    limited = runner.invoke(
        app, ["--json", "--data-dir", str(data_dir), "video", "list", "--limit", "1"]
    )
    assert json.loads(limited.stdout)["count"] == 1

    absent = runner.invoke(
        app, ["--json", "--data-dir", str(data_dir), "video", "list", "--channel", "UCnope"]
    )
    assert json.loads(absent.stdout)["count"] == 0


def test_playlist_show_videos_lists_parts(data_dir: Path, source: StubSource) -> None:
    """`--videos` adds the ordered table; without it only the summary is shown."""
    runner.invoke(app, ["--data-dir", str(data_dir), "fetch", PLAYLIST_URL])

    summary = runner.invoke(
        app, ["--json", "--data-dir", str(data_dir), "playlist", "show", PLAYLIST]
    )
    assert "videos" not in json.loads(summary.stdout)

    detailed = runner.invoke(
        app, ["--json", "--data-dir", str(data_dir), "playlist", "show", PLAYLIST, "--videos"]
    )
    payload = json.loads(detailed.stdout)
    assert [item["part_number"] for item in payload["videos"]] == [1, 2]


def test_playlist_show_unknown_exits_three(data_dir: Path) -> None:
    """Consistent with `video show`."""
    result = runner.invoke(app, ["--data-dir", str(data_dir), "playlist", "show", "PLnope"])

    assert result.exit_code == 3


def test_playlist_list_reports_counts(data_dir: Path, source: StubSource) -> None:
    """`playlist list` shows the stored item count, not a recount of rows."""
    runner.invoke(app, ["--data-dir", str(data_dir), "fetch", PLAYLIST_URL])

    result = runner.invoke(app, ["--json", "--data-dir", str(data_dir), "playlist", "list"])

    payload = json.loads(result.stdout)
    assert payload["count"] == 1
    assert payload["playlists"][0]["item_count"] == 2


def test_removed_items_are_reported_on_refetch(
    data_dir: Path, source: StubSource, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A shrinking playlist must say so rather than quietly dropping rows."""
    runner.invoke(app, ["--data-dir", str(data_dir), "fetch", PLAYLIST_URL])
    monkeypatch.setattr(StubSource, "titles", ("First part",))

    result = runner.invoke(app, ["--data-dir", str(data_dir), "fetch", PLAYLIST_URL, "--refresh"])

    assert result.exit_code == 0, result.stdout
    assert "1 item(s) left the playlist." in result.stdout


def test_stored_video_count_matches_the_table_when_a_video_repeats(
    data_dir: Path, source: StubSource, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`UNIQUE(playlist_id, video_id)` means a repeat stores one row, not two.

    The summary line and the table are read by the same person in the same breath, so
    "Stored ... 3 videos" above a two-row table is a bug even though no data is lost.
    """

    async def repeating(self: StubSource, youtube_id: str) -> PlaylistMeta:
        video = VideoMeta(youtube_id="vid00000001", title="First part", url="u", channel_id=OWNER)
        other = VideoMeta(youtube_id="vid00000002", title="Second part", url="u", channel_id=OWNER)
        return PlaylistMeta(
            youtube_id=youtube_id,
            title="Rust for Pythonistas",
            url=PLAYLIST_URL,
            channel_id=OWNER,
            items=(
                PlaylistItemMeta(video=video, position=1),
                PlaylistItemMeta(video=other, position=2),
                PlaylistItemMeta(video=video, position=3),
            ),
        )

    monkeypatch.setattr(StubSource, "fetch_playlist", repeating)

    result = runner.invoke(app, ["--json", "--data-dir", str(data_dir), "fetch", PLAYLIST_URL])

    payload = json.loads(result.stdout)
    assert len(payload["videos"]) == 2
    assert payload["playlist"]["item_count"] == 2
    assert payload["stored"]["videos"] == 2
