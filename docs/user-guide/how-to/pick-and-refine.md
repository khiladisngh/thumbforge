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

## Refine

```
thumbforge thumb iterate <run> --n 4 --prompt-append "warmer colours"
thumbforge thumb iterate <run> --var mood=moody
thumbforge thumb iterate <iteration-id>
thumbforge thumb iterate <run> --from-picked
```

This starts a new run, linked to the one you refined, that uses the raw image of your pick as its reference. It keeps the same template and provider; `--n` sets how many candidates you get (4 by default). With a run id it refines that run's pick, so pick first; with an iteration id it refines exactly that iteration and ignores any pick. If the run you name has no pick of its own, `--from-picked` borrows the nearest one from the runs it was refined from.

`--prompt-append` adds your words after the rendered prompt. `--var key=value` fills the template's variables; they are not carried over from the earlier run, so pass again any the template needs. To preview the prompt first, use `thumbforge template render my-series --video <video-id> --var mood=moody`.

The new run prints like `thumb generate` does, so pick from it and refine again. `thumbforge runs show <run>` lists the lineage: a refinement shows its `Parent run`, and the run it came from shows its `Child runs`.

A provider that cannot take a reference image (the Antigravity provider is one) still refines, from the prompt alone, and warns you that the reference was not used.
