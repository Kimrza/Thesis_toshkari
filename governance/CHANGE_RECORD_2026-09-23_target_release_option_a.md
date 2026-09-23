# Change record — 2026-09-23 — stage 02 publishes the `phase1_hourly_target` release

**Change ID:** `CR-2026-09-23-TARGET-RELEASE-OPTION-A`
**Authority:** the project decision owner's ruling of 2026-09-23, in session, approving
**option A** for the 02→05 boundary — the stage publishes the release the downstream stages
consume. This applies D-61's ruling (2026-09-21, the same option at the 00→01/02 boundary)
to the next boundary; the owner was asked whether D-61 extends or a new D-number is wanted,
and answered option A.
**Baseline:** `HEAD = a6b3130`. Every figure below is measured and printed before assertion.
**Register discipline:** no D-number is written by this pass. Whether this act sits under
D-61's existing scope or wants its own entry is recorded below as the one open register
question; no agent writes `evidence/DECISIONS.md`.
**Gate status:** `GOV-2026-09-20-CG-01` stands at `FAIL`. This record does not change it.

---

## 1. The defect

`scripts/05_build_features_and_splits.py`, `06_train_and_predict.py` and
`07_evaluate_and_report.py` each resolve
`release_root/phase1_hourly_target/release_manifest.json` **literally** and refuse when it
is absent. `scripts/02_standardize_prepared_target.py` wrote its standardized target to
`artifacts/prepared_target/` and published **no release**, so all three refused at their
first check and the fixture ladder stopped at stage 05.

This is D-61's shape exactly, one boundary downstream: a complete, tested release writer
with no production caller at the boundary that needs it.

## 2. What was implemented

`_publish_target_release` in stage 02, plus two helpers, all in this unit's own files:

* `_consumed_release_manifests` re-enumerates the releases under the root and **re-verifies**
  each through `verify_release` before citing it. The rows were verified when they were
  read; the manifest is being cited now, so it is checked now.
* `_target_release_manifest` builds the thirteen caller-supplied TE §13.3 fields entirely
  from run facts: `source_files` from the **consumed** release manifests (one entry per
  released file, carrying that release's `dataset_version`, `content_hash` and creation
  instant); `processing` from the consumed release's own seven Phase 1 keys with the
  identity re-resolved from config; `row_counts` across all four axes; and
  `exclusions_qc_summary` derived from the coverage report's measured `invalid_reasons`.
  `dataset_version` is absent by construction — `write_release` derives it (D-29) and
  refuses a caller-supplied value.
* `fold_ids` / `mask_ids` / `feature_set_ids` carry an explicit
  `NOT_YET_ASSIGNED_stage_02_precedes_splits_masks_features` token, the same device and the
  same reason as stage 00's: TE §13.3 requires all fourteen fields non-empty, and a
  deliberately unusable token states the stage's position rather than fabricating an id.

**Re-runs and R-13.** The consumers fix the directory name, so a re-run cannot write a new
version beside the old one. R-13 refuses an overwrite and this code never asks it to: when a
release already exists, the would-be manifest's `content_hash` is computed and compared with
the published one. **Identical content republishes nothing** and says so (the content hash
excludes `created_at_utc`, so an identical run is identical by construction). **Different
content refuses**, naming both hashes — a changed target under an unchanged citation is
what TE §13.3's "new version rather than overwritten" forbids, and choosing that version is
an owner act.

## 3. Two defects found by EXECUTION, not by review

Both were invisible to reading and appeared on the second and third runs.

1. **The producer consumed its own output.** `load_released_provider_rows` enumerates every
   manifest under the release root, so the second run of stage 02 read the target release it
   had just published, found the D-17 target columns where the five provider columns belong,
   and refused. The loader was right about the wrong file. Fixed in
   `src/data/prepared.py`: the provider-input enumeration excludes `TARGET_RELEASE_DIR`,
   with the reason recorded at the exclusion — a producer never consumes its own release.
2. **`exclusions_qc_summary` contradicted `row_counts` inside one manifest.** The first
   version read `result.coverage_report["payload"]["invalid_reasons"]`, but `payload` is the
   wrapper `write_json_artifact` adds on the way to disk; the in-memory report has the key at
   the top level. The result was `count: 0` beside `post_documented_qc_invalid: 10`. Fixed to
   read the raw shape with the wrapped one as a fallback. A second pass then showed the
   reasons were keyed by **measured value** (seven classes for ten rows, four of them
   singletons) rather than by the rule violated; now grouped by field-and-bound, giving
   `largest_internal_gap_s above D-19 maximum 1800.0` ×5 and
   `within_hour_spread_tecu above D-19 range bound 10.0` ×5 — **5 + 5 = 10**, agreeing with
   `by_qc_stage` as one manifest's internal arithmetic must.

## 4. Executed

Governed pin (conda `tec-thesis-311`, CPython 3.11.16, `CUDA_VISIBLE_DEVICES=""`,
`PYTHONHASHSEED=0`). Stage 02 publishes `artifacts/releases/phase1_hourly_target/`,
`dataset_version 323f7a53db51`, **168 rows** (BSHM's 168/168 D-11 bins), 158 valid, three
cited source files from the stage-00 release. A second run reported the identical-content
path and rewrote nothing.

**The ladder then advanced one more step and stopped somewhere new.** Stages 00, 01, 02 and
04 complete; stage 05's missing-release refusal is gone; it now stops at `05`'s deliberate
TE §18.3 stub inside `_load_release_inputs`.

## 5. What blocks the ladder now — and one stale refusal worth recording

The stub's own message reads: *"reading the released target and driver products into frames
is reached only after the permitted-producer list, the partitions and the availability lags
are frozen; none is today"*. **All three named preconditions are now met** — the
permitted-producer list was closed by D-63 (2026-09-21), the partitions by D-38
(2026-09-10), the availability lags by D-42/D-43/D-46/D-47 (transcribed 2026-09-19). The
refusal text is stale and should be corrected by `features-and-splits` when it builds the
loader; it is recorded here rather than edited, because the module is another unit's.

**The real remaining blocker is a third missing producer: no driver release exists.**
`scripts/04_build_external_products.py` says so in its own words at `:807-816` — the two GFZ
series were retrieved on 2026-09-18 *"but are NOT YET CONSUMED by this stage: no driver
product is built from them here and no producer artifact exists (D-41 identities only)"*,
recorded as a machine-readable completeness fact on every run. D-63 named the producing
artifact identities; nothing publishes an artifact under them yet.

So the fixture manifests' measured fields (dispositions §5 item 8) remain out of reach,
blocked now on the driver-product producer in `external-products` plus the feature-build
loader in `features-and-splits` — both implementation, both other units, and the first of
them is the same missing-producer pattern this record and D-61 have each closed once.

## 6. The one open register question

Does D-61's ruling cover this act, or does the target release want its own D-number? The
manifest cites `CR-2026-09-23-TARGET-RELEASE-OPTION-A` as its `change_record_id` either way.
No scientific value changed: D-16's statistic, D-17's contract, D-19's thresholds and D-53's
QC list all govern the rows unchanged, and the release only publishes what stage 02 already
produced.
