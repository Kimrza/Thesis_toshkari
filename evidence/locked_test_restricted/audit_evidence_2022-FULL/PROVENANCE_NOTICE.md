# Provenance notice — merged calendar-year evidence set

**Status: the re-merge obligation recorded in the previous notice is DISCHARGED.**
Decision **D-18**, 2026-08-21.

## What this artifact is

The union of the twelve per-month Madrigal coverage runs for calendar 2022, derived by
`scripts/merge_coverage_year.py`. It is **derived, never retrieved**: no request reaches a
provider during a merge.

## Why it was regenerated

The previous merge carried `merged_at_utc = 2026-08-13T06:27:03Z`, which predates the
2026-08-16 acquisition-window correction that regenerated the January and December folders.
Its `source_runs` digests therefore pointed at **superseded** per-month hashes, and the
prior notice recorded the consequence: *"Do not rely on this artifact at a freeze gate
while this notice stands. Either re-merge from the corrected months, or record an explicit
decision re-pointing FULL's provenance."*

The re-merge was chosen over re-pointing, and it ran on 2026-08-21 at
`merged_at_utc = 2026-08-21T09:25:59Z` against the corrected months, with all twelve
per-month hash manifests verifying first — the script prints `All per-month hash manifests
verify.` and exits on any mismatch.

## What changed, precisely

**No scientific content.** The record set is identical to the 2026-08-13 merge: 223,586
unique rows, byte-identical when sorted, and the per-station coverage summary is
byte-identical (`madrigal_coverage_summary.csv` and `madrigal_coverage_monthly.csv` both
unchanged at `b40304b5…` and `6b53d385…`). Coverage remains ARUC, BSHM and NICO at 365/365
days, 100%, December 31/31.

What changed is **provenance metadata**: `merged_at_utc`, and the `source_runs` digests,
which now reference the current per-month manifests rather than superseded ones.

**A determinism defect was found and fixed in the process.** The regenerated raw-records
file initially hashed differently from the 2026-08-13 artifact despite holding the identical
record set, because output order followed month-directory traversal and dedup insertion
order. To anyone checking hashes, that is indistinguishable from a content change.
`merge_coverage_year.py` now sorts rows on the dedup key `(station, ut1_unix, gdlat, glon)`
before writing, and two consecutive runs were confirmed to produce a byte-identical file.
TE §13.7 requires exact equality for deterministic CPU transformations; a merge is one.

## Custody

This artifact holds **21,258 December 2022 records** and lives under
`evidence/locked_test_restricted/` per decision **D-15**. TE §12 requires locked-test
artifacts to sit under a restricted path until G-05 is complete.

**Reading it is a logged December access.** Write the access-log row in
`evidence/experiment_registry.md` § Locked-month access log **before** the read. The
re-merge itself is recorded there as row 7, written in advance.

**The restricted path is a governance boundary, not an access control.** No filesystem
permission, encryption or ACL is involved. It provides one declared location, a
machine-checkable invariant
(`tests/test_acquisition_window.py::test_locked_month_values_exist_only_under_the_restricted_path`),
and an unambiguous access-log trigger — nothing more, and it is not represented as more.

## The prior artifact is preserved, not overwritten

The 2026-08-13 merge is retained verbatim at
`evidence/locked_test_restricted/superseded_2026-08-21_audit_evidence_2022-FULL/`, with its
original notice and its own verifying `sha256_manifest.json`. It is superseded evidence, not
deleted evidence.

## What remains open

- **Underlying provenance of the twelve monthly runs is unchanged by this re-merge.** They
  rest on retrievals whose provider byte streams were never retained, and three months
  (2022-04, 2022-07 and 2022-12, the locked month) have no `raw_isprint_cache/` at all.
  FR-P1-01-2 and FR-P1-01-4 carry the re-acquisition obligation, including recording
  provider filename version suffixes. **That caveat still travels with any figure derived
  from this artifact.**
- `madrigalWeb_version` is recorded as `"unknown"` in all twelve source manifests
  (FR-P1-01-3).
- The twelve monthly runs captured none of TE §13.1's per-run environment fields; the
  registry records that gap as unreconstructable.

This notice supersedes the previous one, which is preserved with the superseded artifact.
