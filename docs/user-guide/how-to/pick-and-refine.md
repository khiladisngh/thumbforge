# Pick and refine

Choose the best candidate from a hero run, then refine it: start a new run that uses the picked image as its reference, with extra words appended to the prompt or different template variables, and pick again. Each refinement is its own run linked to the one it came from, so earlier candidates are never lost. When you are happy, export the final image to a folder. See [Hero](../concepts/hero.md#picking-and-refining).

## Pick one

List the iterations of a run, then pick one by its number (or by its iteration id):

```
thumbforge runs show <run>
thumbforge thumb pick <run> 2
```

A run has exactly one pick. Picking another iteration moves it, and picking an iteration that failed is refused, because it has no usable image. Fix the number or id if Thumbforge says it cannot find the iteration.

## Look at the candidates

```
thumbforge thumb show <run>
```

The grid shows each candidate captioned with its number, a `★` on the picked one, and `✔` or `✘` for whether it passes YouTube's thumbnail rules. On a terminal that cannot draw colour you get a list of file paths instead. `--columns 3` changes how many fit on a row; `--json` prints the same data as `runs show`.

## Export

```
thumbforge thumb export <run> --to out/
thumbforge thumb export <run> --to out/ --raw
thumbforge thumb export <iteration-id> --to out/
```

A run exports every completed candidate as `out/<video-id>-<number>.jpg`; an iteration id exports just that one. `--raw` copies the images exactly as the provider returned them (`.png` for the fake provider) instead of the finals. The folder is created if needed and the originals stay in the store.

!!! note "Coming in v0.1.0"

    Refining a pick with `thumbforge thumb iterate` is roadmap task P6.3, defined in the [Phase 6 spec](../../specs/phase-6-hero.md#behaviour). Until then you can preview how a refinement would change the prompt:

    ```
    thumbforge template render my-series --video <video-id> --var mood=moody
    ```
