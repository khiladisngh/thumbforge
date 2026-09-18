# ADR 0011: Content-addressed asset store with DB metadata

## Status

`Accepted` — 2026-09-19

## Context

Every iteration produces up to two images (`raw` provider output, `final` after fit and overlay), plus reference images and previews. Batch runs reuse the hero's asset as a reference across many iterations, resumed runs must not duplicate files, and the idempotency key (ADR 0012) needs a stable identity for "the reference image". Files must survive relocation of the data directory and be verifiable.

## Decision

- Files live under `<data_dir>/assets/<sha256[:2]>/<sha256>.<ext>`. The `asset` table stores `rel_path` relative to `data_dir`, so the data directory is relocatable.
- `asset` columns: `id`, `sha256 UNIQUE`, `rel_path`, `mime`, `width`, `height`, `bytes`, `kind CHECK IN ('raw','final','reference','preview')`, `compliant BOOL NULL`, `compliance_report_json NULL`, plus the standard timestamps.
- Write path: write to `<data_dir>/tmp/<ulid>`, `fsync`, compute sha256, `rename` into place. Identical bytes dedupe to the same row (`put` returns the existing `Asset`).
- `AssetStore` API (`storage/assets.py`):

    ```python
    class AssetStore:
        def put(self, src: bytes | Path, kind: AssetKind) -> Asset
        def path_for(self, asset: Asset) -> Path
        def verify(self, asset: Asset) -> bool     # re-hashes; False on drift
    ```

- Assets are immutable; "editing" produces a new asset. Deletion happens only via `runs delete --assets`, which unlinks files no longer referenced by any `iteration` or `run.reference_asset_id`.
- The hero→batch link stores `run.reference_asset_id`; providers receive `path_for(asset)` as an absolute path in `GenerationRequest.reference_images` (`PLAN.md` §3.1).

## Consequences

- Re-running a step that yields identical bytes costs no disk space and no new row.
- `sha256` of the reference asset is a stable input to the idempotency key.
- `thumb export` is a copy from `path_for`; nothing in the store is ever served in place.
- Orphaned files after a crash between `fsync` and the DB insert are cleaned by `db vacuum`, which also removes stale `tmp/` entries.

## Alternatives considered

- **Store image bytes as BLOBs in SQLite** — rejected: multi-megabyte rows bloat the database, slow `VACUUM`, and prevent opening the files with normal viewers.
- **Path-addressed files (`runs/<run>/<ordinal>.jpg`)** — rejected: duplicates identical output, and a moved or renamed file silently breaks the reference link; hashing gives verifiability.
- **Git LFS or an object store** — rejected: this is a local single-user tool; no remote is involved.
