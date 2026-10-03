# Providers

A **provider** is the part of Thumbforge that turns a prompt into an image. Providers are plugins: Thumbforge ships with some built in, and anyone can publish another as a separate Python package. The rest of Thumbforge — templates, text overlay, runs, resume — works the same whichever provider you choose.

## The `fake` provider

`fake` is always installed. It needs no network, no account and no key, and it is **deterministic**: the same request always produces exactly the same image, coloured by a hash of the prompt. It is useless for real thumbnails and ideal for trying Thumbforge, testing a template, or rehearsing a batch without spending anything.

## Seeing what is installed

```
thumbforge provider list
thumbforge provider check KEY
thumbforge provider models KEY
```

`provider list` shows every installed provider with its version, authentication state and capabilities. `provider check` runs one provider's health checks (is its program installed, is it signed in) and reports each one. `provider models` lists the models a provider offers, for the `providers.<key>.model` setting.

## Capabilities

Providers differ. Each one declares what it supports: a reference image, a fixed seed, a negative prompt, an aspect ratio, how many images it makes per call, how many calls may run at once, and its output formats. Thumbforge reads these declarations, for example to limit how many images are generated in parallel. `provider list` prints them.

## API keys

A provider that needs a key gets it from the environment variable `THUMBFORGE_PROVIDERS__<KEY>__API_KEY` (provider key in upper case) or, failing that, from your system keyring. `thumbforge provider set-key KEY` prompts for a key and stores it in the keyring. Keys are never written to the configuration file, the database or the logs.

## Adding a provider

A provider plugin registers itself under the `thumbforge.providers` entry-point group of its Python package; installing that package next to Thumbforge makes it appear in `provider list`. [ADR 0010](../../adr/0010-provider-plugin-architecture.md) and the [Phase 3 spec](../../specs/phase-3-providers.md#interfaces) describe the interface a plugin implements.

!!! note "Coming in v0.1.0"

    Choosing a provider for a run (`--provider KEY` on `thumbforge thumb generate` and `thumbforge batch`) arrives with roadmap tasks P6.1 and P7.3; see the [Phase 6 spec](../../specs/phase-6-hero.md#behaviour).

## Going deeper

- [ADR 0010](../../adr/0010-provider-plugin-architecture.md) — the provider plugin design.
- [ADR 0014](../../adr/0014-secrets-env-keyring.md) — how keys are stored.
- [Phase 3 spec](../../specs/phase-3-providers.md#interfaces) — the provider interface and the commands.
