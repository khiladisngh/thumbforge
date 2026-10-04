# Providers

A **provider** is the part of Thumbforge that turns a prompt into an image. Providers are plugins: Thumbforge ships with two built in, `fake` and `antigravity`, and anyone can publish another as a separate Python package. The rest of Thumbforge — templates, text overlay, runs, resume — works the same whichever provider you choose.

## The `fake` provider

`fake` is always installed. It needs no network, no account and no key, and it is **deterministic**: the same request always produces exactly the same image, coloured by a hash of the prompt. It is useless for real thumbnails and ideal for trying Thumbforge, testing a template, or rehearsing a batch without spending anything.

## The `antigravity` provider

`antigravity` drives the Antigravity command-line program (`agy`), so that program has to be installed and signed in; `thumbforge provider check antigravity` reports whether it is. It takes a negative prompt and an aspect ratio, runs up to two generations at once (one image each) and returns JPEG; it takes no seed, and a reference image only as words in the prompt. Its settings sit in the `[providers.antigravity]` section of the configuration file: `binary` (default `agy`), `model`, `effort` (`low`, `medium` or `high`; `low` by default), `timeout_s` (600) and `skip_permissions` (off). `thumbforge provider models antigravity` lists the models it offers.

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

A provider that needs a key gets it from the environment variable `THUMBFORGE_PROVIDERS__<KEY>__API_KEY` (provider key in upper case) or, failing that, from your system keyring. `thumbforge provider set-key KEY` prompts for a key and stores it in the keyring. Keys are never written to the configuration file, the database or the logs. The same command also stores the key for the optional YouTube Data API metadata source, under the name `api`; see [Series and playlists](series-and-playlists.md#fetching-a-playlist).

## Adding a provider

A provider plugin registers itself under the `thumbforge.providers` entry-point group of its Python package; installing that package next to Thumbforge makes it appear in `provider list`. [ADR 0010](../../adr/0010-provider-plugin-architecture.md) and the [Phase 3 spec](../../specs/phase-3-providers.md#interfaces) describe the interface a plugin implements.

## Choosing a provider for a run

`--provider KEY` on `thumbforge thumb generate` and `thumbforge batch` selects the provider for that run; without it, `[general] default_provider` applies (`fake` unless you change it). `thumb iterate` keeps the provider of the run it refines. Every run records the provider, its version and its settings, and never a key.

## Going deeper

- [ADR 0010](../../adr/0010-provider-plugin-architecture.md) — the provider plugin design.
- [ADR 0014](../../adr/0014-secrets-env-keyring.md) — how keys are stored.
- [Phase 3 spec](../../specs/phase-3-providers.md#interfaces) — the provider interface and the commands.
