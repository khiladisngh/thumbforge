# ADR 0018: `LayoutSpec` and `ComplianceReport` live in `core`; imaging does not persist

## Status

`Accepted` — 2026-09-25

Supersedes the layout-spec bullet of [ADR 0006](0006-jinja2-prompts-toml-layouts.md), which placed the Pydantic model in `templates/schema.py`. Every other decision in ADR 0006 — Jinja2 with `StrictUndefined`, TOML layout files, immutable versioned template rows, the builtin set, the commands — stands unchanged.

## Context

The dependency rule (`AGENTS.md`, enforced by import-linter) says `core` imports no other internal package and every adapter package may import `core` only. The Phase 4 and Phase 5 specs as first written broke it twice:

- ADR 0006 put `LayoutSpec` in `templates/schema.py`, but `imaging/overlay.py` (Phase 5) and `HeroService` in `core.services` (Phase 6) both consume it. Neither may import `templates`.
- The Phase 5 spec put `finalize()` in `core/services/compliance.py`, calling `imaging`, `LayoutSpec`, `AssetStore` (storage) and `OutputSettings` (settings). The `core is pure` contract forbids all four.

The same problem was solved before: `MetadataSource` moved to `core/sources.py` (P2.3) and the `ImageProvider` boundary models to `core/providers.py` (P3.1) because `core.services` consumes them.

## Decision

- `LayoutSpec` and its blocks live in `src/thumbforge/core/layout.py`. `templates/schema.py` only loads TOML into it (`load_layout(path) -> LayoutSpec`).
- `ComplianceReport` lives in `src/thumbforge/core/models.py`.
- `imaging/finalize.py::render_final(raw, layout, output, *, title, part_number, part_label) -> tuple[bytes, ComplianceReport]` does pixels only: fit, overlay, encode, then check. It touches neither the database nor the asset store.
- P6.1's `HeroService` receives `render_final` as an injected callable and stores the result: the `final` asset, `compliant`, `compliance_report_json`, and `ComplianceError` handling. Its collaborators arrive as Protocols, as `FetchService`'s do.
- `imaging` and `templates` join the `adapters are independent` import-linter contract.

## Consequences

- import-linter keeps passing with no exceptions carved out.
- Persistence is in one place (the service), so hero and batch runs record compliance the same way.
- `render_final` can be tested with no database: bytes in, bytes and a report out.
- Specs updated: `docs/specs/phase-4-templates.md`, `phase-5-imaging.md`, `phase-6-hero.md`, `phase-7-batch.md`; ROADMAP P4.1, P5.3 (now depends on P5.2) and P6.1.

## Alternatives considered

- **Keep `finalize` in `core` and inject fit, overlay and check through an `Imaging` Protocol** — rejected: one Protocol with four methods and one implementation, only to keep a function that `imaging` can own outright.
- **Relax `core is pure` for `imaging`** — rejected: it reopens the dependency rule for one caller and makes `core` untestable without Pillow.
- **Keep `LayoutSpec` in `templates` and let `imaging` import `templates`** — rejected: adapters would depend on each other, and `core.services` still could not see the type.
