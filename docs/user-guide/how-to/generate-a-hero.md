# Generate a hero

Generate several candidate thumbnails for one video with a chosen template and provider, compare them side by side in the terminal, and keep the run so you can pick one. The result is a `hero` run whose iterations each hold a raw image from the provider and a final, fitted image with the title drawn on it. See [Hero](../concepts/hero.md) for the ideas behind it.

!!! note "Coming in v0.1.0"

    `thumbforge thumb generate` is roadmap task P6.1; it depends on the built-in templates and template versioning (P4.3, P4.4) and on the final image render (P5.3). Its behaviour is defined in the [Phase 6 spec](../../specs/phase-6-hero.md#behaviour).

## Prerequisites you can do today

```
thumbforge config init
thumbforge db init
thumbforge fetch "https://www.youtube.com/watch?v=<video-id>"
thumbforge provider list
thumbforge provider check fake
thumbforge template render my-series --video <video-id> --var mood=bright
```

The last command prints the exact prompt a hero run would send, using a template from your configuration folder; see [Getting started](../getting-started.md#7-preview-a-templates-prompt).
