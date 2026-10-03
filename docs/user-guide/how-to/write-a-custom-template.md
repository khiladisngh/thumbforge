# Write a custom template

Create your own template — a prompt and a layout — starting from a built-in one, adjust where the title and badge sit and what the provider is asked to paint, and import it so runs can use it. Every import of a changed template becomes a new version, so earlier runs stay reproducible. See [Templates](../concepts/templates.md).

!!! note "Coming in v0.1.0"

    The built-in templates are roadmap task P4.3 and `thumbforge template list|show|new|import` with versioning is P4.4, defined in the [Phase 4 spec](../../specs/phase-4-templates.md#behaviour).

## Prerequisites you can do today

You can already write a template by hand and check it. Put `NAME.toml` and `NAME.j2` in the `templates/` folder next to your configuration file ([Getting started](../getting-started.md#7-preview-a-templates-prompt) has a complete example), then:

```
thumbforge template validate <config-dir>/templates/NAME.toml
thumbforge template render NAME --video <video-id> --var key=value
```

`validate` lists every layout error at once; `render` prints the prompt for a stored video and calls no provider.
