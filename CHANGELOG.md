# Changelog

## 0.1.1 (2026-10-04)

### Features

- **imaging:** Render Devanagari titles with shaping and a bundled fallback font (ccd363b)

### Bug fixes

- **ci:** Keep dist/.gitignore out of release assets (ecae27a)

### Documentation

- Install from PyPI (e50d057)
- **user-guide:** Bring the guide in line with the shipped CLI (a540249)
- Bring the home page, specs index and maintainer pages up to date (471f6f3)
- Document playlist fetch, batch selection and log locations (46f7a7c)
- **user-guide:** Add a try-it-on-a-playlist walkthrough (98472dc)
## 0.1.0 (2026-10-04)

### Features

- **infra:** Integrate graphify codebase knowledge graph (P0.6) (c7b261f)
- **core:** Add error hierarchy, exit codes, render layer and root app (P1.5, P1.6) (a8d270b)
- **settings:** Add configuration and the config command group (P1.1) (bdc2141)
- **logging:** Add structlog configuration and wire the verbosity flags (P1.2) (4db73b6)
- **storage:** Implement SQLite database, models, and CLI (P1.3) (e76e096)
- **storage:** Implement content-addressed AssetStore (P1.4) (a986d50)
- **sources:** MetadataSource protocol, metadata models and URL classifier (#24) (087a07b)
- **sources:** YtDlpSource with recorded fixtures (#29) (4178814)
- **fetch:** Repositories, FetchService and the fetch/video/playlist commands (#32) (ec8dd2f)
- **playlist:** Playlist renumber (#34) (50a5d4d)
- **providers:** ImageProvider protocol, capabilities and registry (#40) (ecc25c5)
- **providers:** FakeProvider and the provider contract suite (#42) (5b7b17e)
- **providers:** AntigravityProvider (P3.4) (#45) (bc7fde0)
- **cli:** Provider commands and credential storage (P3.5) (#47) (2b02fc1)
- **imaging:** Fit_to resizes and centre-crops to the output size (P5.1) (#50) (ec3ecf6)
- **templates:** LayoutSpec in core and template validate (P4.1) (#51) (9b9b21d)
- **templates:** Render prompts with Jinja (P4.2) (5b630c2)
- **imaging:** Deterministic text overlay with golden tests (P5.2) (60161ab)
- **cli:** Two-column Rich image preview with fallback (P5.4) (af77b7f)
- **templates:** Ship bold-title, minimal and series-parts built-ins (P4.3) (a04b4d8)
- **imaging:** Compliance check and final render (P5.3) (3027a59)
- **templates:** Template commands, versioning and built-in sync (P4.4) (63035d0)
- **sources:** Optional YouTube Data API source (P8.1) (3b55e4e)
- **hero:** HeroService and thumb generate (P6.1) (7f24b8d)
- **hero:** Thumb pick, show and export (P6.2) (5c77fb6)
- **hero:** Thumb iterate with lineage (P6.3) (09dc3d9)
- **batch:** BatchService with idempotent playlist runs (P7.1) (be04997)
- **batch:** Interrupt, resume and cancel (P7.2) (a6cf2a8)
- **batch:** Batch command with progress and summary (P7.3) (d9a02f1)
- **runs:** Runs list, resume, cancel and delete (P7.4) (5594f62)
- **runs:** Runs cost and a cost column in runs show (P8.4) (b52d132)

### Bug fixes

- **cli:** Move tests under tests/unit and write JSON diagnostics raw (488630f)
- **cli:** Unblock the config repair path, redact secrets, align the docs (aeb8f63)
- **redaction:** Stop treating a bare trailing key as a credential (26ac91f)
- **storage:** Move AssetError to core, enforce strict MIME allowlist, and guard orphan cleanup (997f9a3)
- **storage:** Harden AssetStore publication and add db vacuum orphan reclamation (P1.4) (e5c4026)
- **storage:** Drop AssetStoreError alias and pin new error exit codes (#16) (4a252ce)
- **ci:** Compare declaration nodes in the drift check, not everything (#26) (d34f907)
- **deps:** Keep SQLAlchemy below 2.1 (P8.2) (82d5b58)

### Documentation

- Restore the missing S10 and S11 spike headings (#22) (95006ca)
- **spikes:** Resolve S11 — yt-dlp flat playlist fields (#27) (b537c1a)
- **spikes:** Resolve S1-S8 — Antigravity CLI is viable, with four corrections (#37) (ab90a68)
- **specs:** Move finalize out of core and reconcile specs with the import contracts (#49) (5bb9a36)
- **agents:** Direct-to-main workflow with local gates (829c6b3)
- **site:** Restructure the docs for users, developers and maintainers (859f5a0)
- **site:** New landing page (4bb33ad)
- **user-guide:** Getting started and install (P8.2) (ca3a5f8)
- **user-guide:** Shell completion (P8.3) (80e8f18)
- README quick start, changelog and release readiness (P8.5) (da0a5e2)

### Tests

- **batch:** Strip ANSI codes before reading a usage error (P7.3) (95101ab)

### Maintenance

- Bootstrap thumbforge (Phase 0 infrastructure) (37244f4)
- Bump actions to Node 24 majors (checkout v5, setup-uv v6, artifact v5/v6) (5037963)
- **ci:** Add CodeRabbit AI review configuration (cc66103)
- **ci:** Ignore local scratch artifacts and document the graph-drift recipe (#18) (3ff0f30)
- **graph:** Rebuild knowledge graph from scratch and correct the drift guidance (#20) (618692f)
- **ci:** Run lint-imports in CI and add local CI scripts (902f7df)
- **editor:** Add a VS Code workspace file (76794b6)
