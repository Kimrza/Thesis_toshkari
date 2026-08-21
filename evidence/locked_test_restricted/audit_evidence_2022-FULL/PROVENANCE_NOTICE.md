# Provenance notice — read before relying on this artifact

**Recorded 2026-08-16. Governance finding DATA-11.**

## This artifact's own hashes are valid; its upstream pointers are stale

> **Relocated 2026-08-21 under decision D-15.** This artifact now lives at
> `evidence/locked_test_restricted/audit_evidence_2022-FULL/`, because the merged year
> contains 21,258 December 2022 records and TE §12 requires locked-test artifacts to sit
> under a restricted path until G-05 is complete. Paths written below in their original
> form refer to the pre-relocation layout; the current mapping is:
>
> | Referenced as | Now at |
> |---|---|
> | `audit_evidence_2022-FULL/` | `evidence/locked_test_restricted/audit_evidence_2022-FULL/` |
> | `audit_evidence_2022-12/` | `evidence/locked_test_restricted/audit_evidence_2022-12/` |
> | `audit_evidence_2022-01/superseded_2026-08-16/` | `evidence/locked_test_restricted/superseded_2026-08-16_from_2022-01/` |
> | `audit_evidence_2022-12/superseded_2026-08-16/` | `evidence/locked_test_restricted/audit_evidence_2022-12/superseded_2026-08-16/` |
>
> Contents are unchanged: all 21 relocated files verified byte-identical against a
> pre-move SHA-256 inventory. **Opening this artifact is a logged December access** —
> write the access-log row in `evidence/experiment_registry.md` before reading it.
> Nothing else in this notice is altered, and the obligation it records is still open.

`audit_evidence_2022-FULL/` was **not re-merged** after the 2026-08-16 acquisition-window
correction. Its four declared artifacts still verify against its own
`sha256_manifest.json`, and its statistics remain correct — 365 days, 100% coverage, all
three cells, December 31/31.

What is stale is its provenance. `request_manifest.json` records `source_runs["1"]` with
`rows_fetched_total: 21551` and the pre-correction January `sha256_manifest` digest. Both
`audit_evidence_2022-01/` and `audit_evidence_2022-12/` were regenerated on 2026-08-16, so
a reviewer who follows FULL's provenance to those folders gets a **hash mismatch**.

That mismatch is expected and explained. Without this notice it would be indistinguishable
from tampering, which is why it is recorded in-band rather than only in prose elsewhere.

## What changed upstream

- `audit_evidence_2022-01/` — 743 records dated 2022-12-31 (the locked test month) removed;
  `unique_days` 32 → 31, `december_days_present` 1 → 0, `december_coverage_pct` 3.226 → 0.0.
- `audit_evidence_2022-12/` — 642 records dated 2021-12-31 removed; **statistics unchanged**,
  because the merge script's calendar-year guard had already excluded them from every
  aggregate.

Pre-correction originals are preserved under `superseded_2026-08-16/` in both folders and
verify against their own superseded manifests.

FULL's own statistics were never affected by the defect, for the same reason: the year
guard excluded the out-of-year rows from its aggregates while retaining them in merged raw
records. The correction removed rows the guard was already discounting.

## Constraint on use

**Do not rely on this artifact at a freeze gate while this notice stands.** D-9 promotes
FULL as the Phase 1 acquisition input, so this sits directly on the G-05 evidence path.
Either re-merge from the corrected months, or record an explicit decision re-pointing
FULL's provenance — that choice belongs to the student, which is why the re-merge was not
performed silently as part of the correction.

Two further limitations apply to FULL independently of this notice:

- Its twelve source runs record `madrigalWeb_version` as `"unknown"` (finding DATA-03).
- No provider byte stream exists for any month, and three months — 2022-04, 2022-07 and
  2022-12 — have no `raw_isprint_cache/` at all, so TE §13.3 `source_files` cannot be
  populated (finding DATA-04). Re-acquisition is sequenced after requirements-analysis
  (FU-1=B) and must record provider file version suffixes (finding DATA-07).

Full record: `evidence/CORRECTION_2026-08-16_acquisition_window.md`.
