# Batch a playlist

Generate one thumbnail for every video in a playlist, using your picked hero as the style reference, with each video's own title and "Part N" badge drawn on top. You will be able to preview the plan without generating anything, limit the batch to some parts, cap the number of images, and watch progress per video. See [Series and playlists](../concepts/series-and-playlists.md).

!!! note "Coming in v0.1.0"

    `thumbforge batch` is roadmap tasks P7.1–P7.3, defined in the [Phase 7 spec](../../specs/phase-7-batch.md#behaviour). It needs a picked hero (P6.2).

## Prerequisites you can do today

```
thumbforge fetch "https://www.youtube.com/playlist?list=<playlist-id>"
thumbforge playlist show <playlist-id> --videos
thumbforge playlist renumber <playlist-id> --start 1 --skip-ids <trailer-video-id>
thumbforge template render my-series --video <video-id> --var mood=bright
```

Get the part numbers right before batching: they are what the badges show, and a batch will select parts by number.
