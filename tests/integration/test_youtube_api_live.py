"""One live Data API v3 playlist fetch (phase 8 spec, acceptance criteria).

Marked `integration`, so the default run never hits the network, and skipped unless
`THUMBFORGE_PROVIDERS__API__API_KEY` is set. Costs a handful of quota units:

    THUMBFORGE_PROVIDERS__API__API_KEY=… uv run pytest -m integration \
        tests/integration/test_youtube_api_live.py

The key is read from the environment directly rather than through `credentials`, so a run
can never fall back to a key stored in the developer's keyring by accident.
"""

from __future__ import annotations

import os

import pytest

from thumbforge.core.enums import ChannelSource
from thumbforge.credentials import env_var
from thumbforge.sources.youtube_api import YouTubeDataApiSource

pytestmark = pytest.mark.integration

#: The playlist `tests/fixtures/ytdlp/playlist.json` was recorded from. The fixture keeps
#: only its first 12 items (`FIXTURE_ITEMS` in `test_ytdlp_record.py`); the live playlist
#: has far more (183 when spike S11 measured it) and its contents change over time, so the
#: live check asserts the 12-item floor and the invariants rather than exact ids.
PLAYLIST_ID = "PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI"
FIXTURE_ITEMS = 12


async def test_live_playlist_fetch() -> None:
    api_key = os.environ.get(env_var(ChannelSource.API.value), "").strip()
    if not api_key:
        pytest.skip(f"{env_var(ChannelSource.API.value)} is not set")

    playlist = await YouTubeDataApiSource(api_key).fetch_playlist(PLAYLIST_ID)

    assert playlist.item_count >= FIXTURE_ITEMS
    assert [item.position for item in playlist.items] == list(range(1, playlist.item_count + 1))
    assert playlist.channel_id == "UC-9-kyTW8ZkZNDHQJ6FgpwQ"
    assert all(item.video.title for item in playlist.items)
    assert playlist.source is ChannelSource.API
    assert {item.video.source for item in playlist.items} == {ChannelSource.API}
