# Walkthrough

A 2½-minute screen recording of Thumbforge on a real playlist: install it, fetch the playlist, generate and refine a hero, batch the series with the part badges, run the batch again to see nothing regenerated, check the cost, and export the files.

<video controls preload="metadata" poster="../../assets/walkthrough/poster.jpg" width="100%">
  <source src="../assets/walkthrough/thumbforge-walkthrough.mp4" type="video/mp4">
  Your browser cannot play this video. <a href="../assets/walkthrough/thumbforge-walkthrough.mp4">Download the MP4</a> (11 MB).
</video>

[Download the MP4](../assets/walkthrough/thumbforge-walkthrough.mp4) (11 MB, 1920×1080, no sound).

## Chapters

Times are approximate.

| Time | What you see                                          |
| ---- | ----------------------------------------------------- |
| 0:00 | Title                                                 |
| 0:04 | Install from PyPI and check the version               |
| 0:10 | Check the provider                                    |
| 0:17 | Set up the database, fetch a playlist, list templates |
| 0:34 | Look at a video's existing thumbnail                  |
| 0:46 | Generate a hero (sped up)                             |
| 0:58 | The hero candidates and a grid                        |
| 1:08 | Pick and show                                         |
| 1:16 | Before and after                                      |
| 1:20 | Refine with `thumb iterate` (sped up)                 |
| 1:31 | The refined candidates                                |
| 1:36 | Preview a three-part batch with a dry run             |
| 1:42 | Run the batch (sped up)                               |
| 1:54 | Run it again: nothing is regenerated                  |
| 2:02 | The three parts with their PART badges                |
| 2:13 | List runs and see the cost                            |
| 2:23 | Export the files                                      |
| 2:27 | End card                                              |

## What to know

- Every command is a real run, and its output is the real capture.
- The playlist is a public Hindi audiobook playlist, shown with its owner's permission.
- The images come from the Antigravity provider (`agy` 1.2.16) on a Windows machine: 8 provider calls and 9 raw image files in total.
- Long waits are sped up, and the video labels the factor on screen.
- Antigravity cannot take a reference image. The `thumb iterate` and `batch` steps ran from the prompt alone (the tool warns about it), so the batch art differs in style from the hero.
- The hero template `bold-title` shortens a long bilingual title with an ellipsis, while `series-parts` fits it.
- The existing YouTube thumbnail is shown at the 336×188 size YouTube served.
- The grid and the before/after slide are composed from the real exported images.
- The thumbnails are AI-generated demonstrations.

## Follow along

- [Getting started](getting-started.md): install, then a first run.
- [Try it on a playlist](how-to/try-it-on-a-playlist.md): the same steps with the offline `fake` provider, no account needed.
- [Batch a playlist](how-to/batch-a-playlist.md#running-it-again): what running a batch again does.
- [Resume an interrupted run](how-to/resume-an-interrupted-run.md): finishing a batch without regenerating what is done.
