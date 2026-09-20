# Phase 2 — YouTube fetch

Status: Proposed
ROADMAP tasks: P2.1, P2.2, P2.3, P2.4
ADRs: `docs/adr/0005-ytdlp-metadata-source.md`, `docs/adr/0004-sqlite-sqlalchemy-alembic.md`

## Scope

Fetch channel, playlist and video metadata from YouTube via `yt-dlp` (no API key), persist it, and expose it through `fetch`, `video` and `playlist` commands. Establishes the `MetadataSource` protocol that Phase 8's Data API source also implements.

- **P2.1** `sources/base.py` (`MetadataSource` Protocol), `core/enums.py` (`UrlKind`), `core/models.py` (`ChannelMeta`, `PlaylistMeta`, `VideoMeta`, `PlaylistItemMeta`, `ResolvedUrl`), `core/urls.py` (URL classifier).
- **P2.2** `sources/ytdlp.py` (`YtDlpSource`) + recorded fixtures under `tests/fixtures/ytdlp/*.json`.
- **P2.3** `storage/repositories.py` (`ChannelRepository`, `PlaylistRepository`, `VideoRepository`), `cli/fetch.py`, `cli/video.py`, `cli/playlist.py`.
- **P2.4** `playlist renumber`.

## Non-goals

- YouTube Data API source — Phase 8 (`phase-8-polish.md`, decision D7).
- Downloading video or thumbnail bytes; `source_thumbnail_url` is stored as a string only.
- Channel-wide enumeration beyond what a channel URL's uploads playlist yields.

## Interfaces

```python
class MetadataSource(Protocol):
    key: ClassVar[str]                                       # "ytdlp", "api"
    async def resolve(self, url: str) -> ResolvedUrl         # kind: UrlKind + youtube_id
    async def fetch_video(self, youtube_id: str) -> VideoMeta
    async def fetch_playlist(self, youtube_id: str) -> PlaylistMeta   # includes ordered items
    async def fetch_channel(self, youtube_id: str) -> ChannelMeta
```

`resolve` returns `ResolvedUrl(kind, youtube_id)` rather than a bare `UrlKind`: an earlier
draft of this spec returned only the kind, but every caller immediately needs the id too, and
ADR 0005 — which is Accepted and therefore authoritative — already specified the richer shape.
The `fetch_*` methods correspondingly take a `youtube_id`, not a URL.

`VideoMeta`, `PlaylistMeta`, `ChannelMeta` are Pydantic v2 frozen models mirroring the `video`, `playlist`, `channel` columns in `PLAN.md` §3 (`youtube_id`, `title`, `description`, `duration_s`, `published_at`, `url`, `source_thumbnail_url`, …) plus `source: ChannelSource` and `fetched_at: datetime`. `PlaylistItemMeta(video: VideoMeta, position: int)`; `PlaylistMeta.item_count` is derived from `items`. All use `extra="forbid"`, so a renamed yt-dlp field fails at the boundary instead of silently arriving empty, and `fetched_at` must be timezone-aware (it is persisted as ISO-8601 UTC).

URL classification is a pure function in `core/urls.py` (`classify_url`, `classify_id`), not a
method body, so both this source and the Phase 8 Data API source resolve input identically and
the rules are testable without network. Recognised: `watch?v=`, `youtu.be/<id>`, `/shorts/`,
`/embed/`, `/live/`, `/v/`, `/playlist?list=`, `/channel/<UC…>`, `/@handle`, `/c/<name>`,
`/user/<name>`, and bare ids discriminated by shape (11-char video, `UC…` channel, `PL|UU|LL|FL|OL|RD…` playlist).
A `watch` URL carrying **both** `v=` and `list=` resolves to the **video**: it names one video
being watched in a playlist's context, and fetching the whole playlist would pull in videos the
user did not ask for.

Where a URL form fixes the kind, the extracted identifier is validated **against that form**
rather than classified by shape: `youtu.be/<id>`, `v=<id>`, `/shorts|embed|live|v/<id>` must
carry a video id, `/playlist?list=` and a bare `list=` a playlist id, `/channel/<id>` a channel
id. Otherwise `youtu.be/PL…` would resolve to `PLAYLIST` and send `fetch` to `fetch_playlist`
for a host that serves no playlists. `/c/<name>`, `/user/<name>` and `@handle` return `CHANNEL`
directly because their values are names, not shape-classifiable ids, and `@` alone is rejected.

Unrecognised input raises `UrlError` (code `url`, exit `2`) — a validation failure, not a
`SourceError`. This includes a malformed authority, which `urllib.parse.urlparse` reports as
`ValueError`: it is caught and re-raised as `UrlError` so it cannot escape `handle_errors`,
which only handles `ThumbforgeError`.

`YtDlpSource` wraps `yt_dlp.YoutubeDL` with `quiet=True, skip_download=True, extract_flat="in_playlist"` for playlists and a full extract for single videos; called through `asyncio.to_thread`. Network errors (`yt_dlp.utils.DownloadError` with a network cause) are retried per `PLAN.md` §7.2; anything else becomes `SourceError` (exit `1`). An id that YouTube reports as unavailable becomes `NotFoundError` (exit `3`).

Commands (from `PLAN.md` §5.2):

| Command                                   | Key flags                          | Output                                                                                                    | Exit    |
| ----------------------------------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------- | ------- |
| `thumbforge fetch <url>`                  | `--source ytdlp\|api`, `--refresh` | Detects video / playlist / channel URL; upserts channel, playlist, videos, playlist_items; prints a table | 0, 1, 2 |
| `thumbforge video list`                   | `--channel`, `--limit`             | table                                                                                                     | 0       |
| `thumbforge video show <id\|url>`         |                                    | panel with metadata + runs                                                                                | 0, 3    |
| `thumbforge playlist list`                | `--channel`                        | table                                                                                                     | 0       |
| `thumbforge playlist show <id\|url>`      | `--videos`                         | panel; with `--videos` a table `position, part, title, youtube_id`                                        | 0, 3    |
| `thumbforge playlist renumber <playlist>` | `--start N`, `--skip-ids ID,ID`    | rewrites `part_number` sequentially from `--start`, skipping listed videos (their `part_number` → NULL)   | 0, 3    |

## Behaviour

1. `fetch <url>` resolves the URL kind, calls the matching `fetch_*`, and upserts by `youtube_id` (insert or update `title`, `description`, `fetched_at`, …; never changes `id`). Playlist fetch upserts the owning channel, the playlist, every video, and `playlist_item` rows with `position` = 1-based index from yt-dlp; `part_number` is set to `position + 1` only when the row is new (existing overrides survive re-fetch). Items no longer in the playlist are deleted from `playlist_item` (videos stay).
2. Without `--refresh`, a playlist fetched less than 24 h ago is reported from the DB without a network call; `--refresh` forces the fetch.
3. `--source api` in Phase 2 exits `2` with hint "install the `api` extra (Phase 8)".
4. `video show` / `playlist show` accept a ULID, a YouTube id or a URL; unknown → `NotFoundError`, exit `3`.
5. `playlist renumber P --start 3 --skip-ids a,b` assigns `part_number` 3,4,5… to items in `position` order, skipping `a` and `b` (set to `NULL`); prints the before/after table.
6. All commands honour `--json`: `fetch` emits `{"kind": "playlist", "channel": {...}, "playlist": {...}, "videos": [...]}`.

## Acceptance criteria

- `thumbforge fetch "https://www.youtube.com/playlist?list=PLxxxx"` against the recorded fixture prints the playlist panel and item table from `PLAN.md` §5.3 and the line `Stored 1 channel, 1 playlist, 12 videos.`; exit `0`.
- Re-running the same `fetch` without `--refresh` prints the same table with `(cached)` in the panel and makes no yt-dlp call (asserted via a spy).
- `thumbforge playlist show PLxxxx --videos` shows `part` = `position + 1` for every row; after `thumbforge playlist renumber PLxxxx --start 0 --skip-ids dQw4w9WgXcQ`, `part` for the skipped video is `—` and the rest are `0,1,2…`.
- `thumbforge video show doesnotexist` exits `3` and prints `not_found: video 'doesnotexist'` on stderr.
- `thumbforge fetch <playlist>` where yt-dlp raises a network error retries 3 times with backoff (observable via structlog `retry` events) and then exits `1`.
- `thumbforge --json fetch <video url>` prints one JSON object with `kind == "video"`.

## Test plan

- Unit: `YtDlpSource` against `tests/fixtures/ytdlp/{video,playlist,channel}.json` loaded by a `FakeYoutubeDL` fixture; repositories on an in-memory SQLite with the Phase 1 migrations; CLI via `CliRunner`.
- Fixture recorder: `uv run pytest -m integration tests/integration/test_ytdlp_record.py` rewrites the fixtures from live YouTube; the recorded JSON is committed and the recorder runs only under the `integration` marker. It also asserts the S11 field set, so a yt-dlp upgrade that changes the info-dict shape fails loudly instead of silently producing empty metadata. Media-delivery keys (`formats`, `subtitles`, `heatmap`, …) are stripped before writing — thumbforge sets `skip_download` and never reads them, and they are ~80 KB of the ~87 KB a full extract returns.
- Integration (`-m integration`): one live `fetch` of a public playlist, asserting the field set from spike S11.
- No golden/contract tests.

## Open spikes

- **S11** yt-dlp flat playlist fields — **resolved**, see `docs/spikes/ytdlp.md`. `id`, `title`, `duration`, `channel_id`, `channel`, `url`, `thumbnails` and `view_count` are always present per entry under `extract_flat="in_playlist"`. `playlist_index` is **absent**, so `PlaylistItemMeta.position` is derived from enumeration order. `description` is **absent** from every entry, and `timestamp`, `availability` and `live_status` are present but always `None`, so playlist-sourced `VideoMeta` rows keep their empty `description` and `published_at=None`; a per-video full extract fills them, and `fetch` must not fan out one per item.
