# Pick and refine

Choose the best candidate from a hero run, then refine it: start a new run that uses the picked image as its reference, with extra words appended to the prompt or different template variables, and pick again. Each refinement is its own run linked to the one it came from, so earlier candidates are never lost. When you are happy, export the final image to a folder. See [Hero](../concepts/hero.md#picking-and-refining).

!!! note "Coming in v0.1.0"

    `thumbforge thumb pick|show|export` is roadmap task P6.2 and `thumbforge thumb iterate` is P6.3, both defined in the [Phase 6 spec](../../specs/phase-6-hero.md#behaviour).

## Prerequisites you can do today

```
thumbforge db status
thumbforge video show <video-id>
thumbforge template render my-series --video <video-id> --var mood=moody
```

Rendering the prompt with different `--var` values shows how a refinement would change the request before any image is generated.
