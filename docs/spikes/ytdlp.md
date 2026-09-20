# Spike results — yt-dlp

## S11 — flat playlist fields under `extract_flat` (closed 2026-09-20)

`yt-dlp` version: resolved by `uv run --with yt-dlp` on 2026-09-20. Playlist used:
`https://www.youtube.com/playlist?list=PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI` ("Popular Music
Videos", 183 items) — a large, stable, public playlist.

### Command

```bash
uv run --with yt-dlp python -c "
import yt_dlp
url = 'https://www.youtube.com/playlist?list=PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI'
with yt_dlp.YoutubeDL({'extract_flat':'in_playlist','quiet':True,'skip_download':True}) as ydl:
    info = ydl.extract_info(url, download=False)
print(sorted(info['entries'][0]))
"
```

### Result — playlist level

```
TOP-LEVEL KEYS: ['_type', 'availability', 'channel', 'channel_follower_count', 'channel_id',
 'channel_url', 'description', 'epoch', 'extractor', 'extractor_key', 'id', 'modified_date',
 'original_url', 'playlist_count', 'release_year', 'tags', 'thumbnails', 'title', 'uploader',
 'uploader_id', 'uploader_url', 'view_count', 'webpage_url', 'webpage_url_basename',
 'webpage_url_domain']

playlist title      : Popular Music Videos
playlist id         : PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI
playlist_count      : 183
channel/uploader    : Music / Music
channel_id          : UC-9-kyTW8ZkZNDHQJ6FgpwQ
n entries           : 183
```

`playlist_count` matches `len(entries)`, and the playlist carries its own `title`,
`description`, `channel_id` and `thumbnails` — enough to fill `PlaylistMeta` and the owning
`ChannelMeta` from a single call.

### Result — entry level

```
ENTRY[0] KEYS: ['__x_forwarded_for_ip', '_type', 'availability', 'channel', 'channel_id',
 'channel_url', 'creators', 'duration', 'id', 'ie_key', 'live_status', 'thumbnails',
 'timestamp', 'title', 'uploader', 'uploader_url', 'url', 'view_count']
```

```
playlist_index present in any entry: False
timestamp values (first 5)         : [None, None, None, None, None]
description present in any entry   : False
duration None count                : 0 / 183
channel_id None count              : 0 / 183
keys missing from some entries     : ['uploader_id']
```

| Field            | Under `extract_flat` | Note                                            |
| ---------------- | -------------------- | ----------------------------------------------- |
| `id`             | ✅ always            | 11-char video id                                |
| `title`          | ✅ always            |                                                 |
| `duration`       | ✅ always (183/183)  | seconds; differs by ±1s from a full extract     |
| `channel_id`     | ✅ always (183/183)  | the **video's** channel, not the playlist owner |
| `channel`        | ✅ always            |                                                 |
| `url`            | ✅ always            | canonical `watch?v=` form                       |
| `thumbnails`     | ✅ always            | list, max 336×188 — no `maxresdefault`          |
| `view_count`     | ✅ always            |                                                 |
| `playlist_index` | ❌ **absent**        | the key does not exist on any entry             |
| `description`    | ❌ always `None`     | key present, never populated                    |
| `timestamp`      | ❌ always `None`     | so no `published_at`                            |
| `availability`   | ❌ always `None`     |                                                 |
| `uploader_id`    | ⚠️ missing on some   | do not rely on it                               |

### Result — full extract of one video, for comparison

```
$ uv run --with yt-dlp python -c "...YoutubeDL({'quiet':True,'skip_download':True})..."
{
 "id": "fOT0BUpITw8",
 "title": "BELLAKEO (Video Oficial) - Peso Pluma, Anitta",
 "duration": 234,
 "channel_id": "UCzrM_068Odho89mTRrrxqbA",
 "upload_date": "20231208",
 "timestamp": 1701993610,
 "description": "BELLAKEO (Video Oficial) - Peso Pluma, Anitta\nDouble P Records\n\n...",
 "view_count": 761508498,
 "live_status": "not_live",
 "availability": "public",
 "thumbnail": "https://i.ytimg.com/vi/fOT0BUpITw8/maxresdefault.jpg"
}
```

A full extract also emits a warning worth knowing about, though it does not affect metadata:

```
WARNING: [youtube] No supported JavaScript runtime could be found. Only deno is enabled by
default ... YouTube extraction without a JS runtime has been deprecated, and some formats may
be missing.
```

Formats are irrelevant here — thumbforge never downloads media — but the warning must be
suppressed or allow-listed so it does not pollute `fetch` output.

### Conclusions

1. **`playlist_index` does not exist under `extract_flat`.** The spike as written in
   `OPEN_QUESTIONS.md` assumed it would. `PlaylistItemMeta.position` must therefore be
   derived from enumeration order — `enumerate(info["entries"], start=1)` — and the P2.1
   docstring claiming it "mirrors yt-dlp's 1-based `playlist_index`" is corrected in this PR.
   Enumeration order is the playlist order, so the derived value is the intended one; it is
   the _provenance_ that was wrong, not the semantics.
2. **A flat playlist extract cannot fill `description` or `published_at`.** `VideoMeta` keeps
   its `""` / `None` defaults for playlist-sourced rows; a full per-video extract is required
   to populate them. P2.2 must not fan out 183 full extracts during `fetch` — the flat pass
   stays the default and `--refresh` on a single video does the deep one. `PLAN.md` §5.2's
   `video show` is therefore allowed to display an empty description for a video that was
   only ever seen through a playlist.
3. **`duration` disagrees by ±1s between flat and full extracts** (235 flat vs 234 full for
   the same video). A refresh that switches extraction mode will flip the stored value; that
   is upstream rounding, not a bug, and the upsert must not treat it as a meaningful change.
4. **`channel_id` on an entry is the video's own channel**, not the playlist owner's. The
   playlist's `channel_id` is on the top-level dict. Both are needed: `playlist.channel_id`
   for ownership, `video.channel_id` for the per-video row.
5. **`thumbnails` in a flat extract top out at 336×188.** A 1280×720 source thumbnail needs
   either the full extract's `thumbnail` (`maxresdefault.jpg`) or the conventional
   `i.ytimg.com/vi/<id>/maxresdefault.jpg` URL. Relevant to P5.1, which fits a source
   thumbnail to 1280×720.

### Fixture recorder consequence (P2.2)

The recorder must store the whole `info` dict for a playlist, including the top-level keys —
not just `entries` — because `PlaylistMeta` and the owning `ChannelMeta` are built from them.
Fixtures must cover both shapes: one flat playlist extract and one full single-video extract.
