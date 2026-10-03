# Glossary

| Term                 | Meaning                                                                                                                                                  |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Hero**             | The single reference thumbnail for one video, chosen from several iterations. Its asset becomes the style reference for a batch.                         |
| **Iteration**        | One generated image attempt inside a run: prompt, seed, provider response, raw asset, final asset.                                                       |
| **Run**              | A unit of work of kind `hero`, `iterate` or `batch`; owns iterations; has a status (`pending`, `running`, `paused`, `completed`, `failed`, `cancelled`). |
| **Batch**            | A run that generates one thumbnail per playlist item using the hero as reference.                                                                        |
| **Raw asset**        | Provider output before overlay/fit.                                                                                                                      |
| **Final asset**      | Raw asset after fit to 16:9, text overlay and compliance check.                                                                                          |
| **Reference asset**  | The asset passed to the provider as a style reference (a hero's final or raw asset).                                                                     |
| **Asset**            | A content-addressed file (`sha256`) with metadata in the DB.                                                                                             |
| **Template**         | A versioned pair: Jinja2 prompt template + TOML layout spec. Immutable per version.                                                                      |
| **Layout spec**      | TOML describing canvas, title box, part badge, font, colours and safe margins for the overlay.                                                           |
| **Provider**         | An implementation of the `ImageProvider` protocol (e.g. `antigravity`, `fake`).                                                                          |
| **Provider profile** | Snapshot of the provider key, version and parameters used by a run. Never contains secrets.                                                              |
| **Capabilities**     | Flags a provider declares: reference image, seed, negative prompt, aspect ratio, batch size, concurrency, output formats.                                |
| **Metadata source**  | An implementation of `MetadataSource` (`ytdlp`, `api`) that fetches channel/playlist/video data.                                                         |
| **Part number**      | The ordinal shown on a playlist thumbnail ("Part 3"); defaults to `position`, editable via `playlist renumber`.                                          |
| **Idempotency key**  | Hash identifying an iteration's inputs; lets a batch resume without regenerating finished items.                                                         |
| **Compliance**       | Check against YouTube thumbnail requirements: 16:9, width ≥ 1280, JPEG/PNG, ≤ 2 MB by default, sRGB.                                                     |
| **Spike**            | A time-boxed verification of an unknown fact, tracked in `OPEN_QUESTIONS.md` (S-items), results in `docs/spikes/`.                                       |
| **Decision**         | A preference only the maintainer can settle (D-items in `OPEN_QUESTIONS.md`).                                                                            |
| **ADR**              | Architecture Decision Record in `docs/adr/`.                                                                                                             |
| **Golden test**      | Snapshot comparison of rendered images.                                                                                                                  |
| **graphify**         | Tool that builds the committed codebase knowledge graph in `graphify-out/`, read by agents before working.                                               |
