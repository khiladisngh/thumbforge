# YouTube Data API v3 fixtures

These files are **not live recordings**. No API key was available when the Data API source
was written, so they were built by hand to the documented v3 response shapes
(`videos.list`, `channels.list`, `playlists.list`, `playlistItems.list`, and the JSON error
body) from the recorded yt-dlp fixtures in `../ytdlp/`. Both fixture sets therefore describe
the same 12 playlist videos: same ids, titles, order, per-video channel ids and durations
(as ISO-8601), the same playlist owner `UC-9-kyTW8ZkZNDHQJ6FgpwQ`, and the same
`jNQXAC9IVRw` video.

| File                        | Response                                                     |
| --------------------------- | ------------------------------------------------------------ |
| `video.json`                | `videos.list?id=jNQXAC9IVRw&part=snippet,contentDetails`     |
| `channel.json`              | `channels.list?id=UC-9-kyTW8ZkZNDHQJ6FgpwQ&part=snippet`     |
| `playlist.json`             | `playlists.list?id=PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI`       |
| `playlist_items_page1.json` | `playlistItems.list`, first page, carries `nextPageToken`    |
| `playlist_items_page2.json` | `playlistItems.list?pageToken=…`, last page                  |
| `videos_batch.json`         | `videos.list` for the playlist's 12 ids in one batch         |
| `error_quota.json`          | the 403 `quotaExceeded` error body                           |

Values the yt-dlp fixtures do not carry are synthetic: every `etag`, playlist item `id` and
`nextPageToken`, the channel and playlist `publishedAt`, the playlist videos' `publishedAt`,
and the thumbnail sets (the conventional `i.ytimg.com` names). The playlist is split into two
pages of six so the fixtures exercise `pageToken`; the real API would return all 12 items on
one page at `maxResults=50`.

Re-record them from the live API once a key exists. The live check is
`tests/integration/test_youtube_api_live.py`
(`THUMBFORGE_PROVIDERS__API__API_KEY=… uv run pytest -m integration`); a recorder belongs
next to it, as `tests/integration/test_ytdlp_record.py` does for yt-dlp.
