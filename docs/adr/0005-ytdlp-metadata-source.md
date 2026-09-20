# ADR 0005: yt-dlp as the default metadata source

## Status

`Accepted` — 2026-09-19

## Context

`thumbforge fetch <url>` must resolve a video, playlist or channel URL into titles, descriptions, durations, publish dates, playlist ordering and source thumbnail URLs, without asking the user for a Google Cloud project or API key. Tests must run offline and deterministically.

## Decision

- `core/sources.py` defines a `MetadataSource` Protocol (this decision said `sources/base.py`; the Protocol moved in P2.3 because `core.services.fetch` consumes it and `core` may not import `sources`. Only the file placement changed, so this is a factual correction rather than a superseding decision):

    ```python
    class MetadataSource(Protocol):
        key: ClassVar[str]                  # "ytdlp", "api"
        async def resolve(self, url: str) -> ResolvedUrl        # kind: video|playlist|channel + youtube_id
        async def fetch_video(self, youtube_id: str) -> VideoMeta
        async def fetch_playlist(self, youtube_id: str) -> PlaylistMeta   # includes ordered items
        async def fetch_channel(self, youtube_id: str) -> ChannelMeta
    ```

- `sources/ytdlp.py` (`YtDlpSource`) is the default (`--source ytdlp`). It imports `yt_dlp` as a library (not a subprocess) with `quiet=True, skip_download=True, extract_flat="in_playlist"` for playlists and a full extraction for single videos. The `yt_dlp` logger is routed through structlog (ADR 0015).
- Playlist entries map to `playlist_item` rows: `position` from `playlist_index`, `part_number = position + 1` by default; the exact field set present under `extract_flat` is confirmed by spike S11 and captured in a fixture.
- `yt-dlp` is pinned in `uv.lock`; a bump is a deliberate PR that re-records fixtures.
- Fixtures: `tests/fixtures/ytdlp/*.json` are produced by a `pytest -m record` recorder that runs live once and stores the raw info-dict; unit tests replay them with `yt_dlp.YoutubeDL.extract_info` monkeypatched. Live tests are `-m integration` and opt-in.
- Network errors retry via `tenacity` with the same backoff as providers (`PLAN.md` §7.2); everything else raises `SourceError` (exit `1`).
- The YouTube Data API v3 source (`sources/youtube_api.py`, extra `api`) is Phase 8 and depends on decision D7.

## Consequences

- No credentials for the common path; `fetch` works for public content immediately.
- YouTube page changes can break `yt-dlp`; the pin plus recorded fixtures keep the test suite green and make breakage visible only in the opt-in live tests.
- The Data API source, when added, must satisfy the same Protocol and the same fixture-replay test pattern.

## Alternatives considered

- **YouTube Data API v3 only** — rejected: requires an API key and a Cloud project before the first command works, and quota (10 000 units/day) is easily exhausted while iterating.
- **`pytube`** — rejected: slower maintenance cadence than yt-dlp and frequent breakage on playlist extraction.
- **Scraping `youtube.com` HTML directly** — rejected: duplicates what yt-dlp already maintains.
