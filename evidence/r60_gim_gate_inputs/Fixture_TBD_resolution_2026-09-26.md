# `plumbing_7day` fixture — full 72-item resolution table (2026-09-26)

Companion to `Fixture_TBD_inventory_2026-09-26.md` (the original inventory).
This document reports what actually happened to each of the 72 original
`TBD — freeze gate` items after this session's work. Four statuses used:
**resolved** (a real value/classification is now in the manifest, with
evidence), **awaiting your decision** (a genuine scope/scientific choice,
proposed but not applied), **awaiting external artifact** (blocked on bytes
this session could not produce), **awaiting measured run** (blocked on
executing the pipeline, not yet done).

## Summary

| Status | Count |
|---|---|
| Resolved with evidence | 18 |
| Awaiting your decision | 4 |
| Awaiting external artifact | 0 (none identified — see note below) |
| Awaiting measured run | 50 |
| **Total** | **72** |

**18 resolved**: 1 stale citation (`units.coordinates`, D-1/D-65) + 15
`comparison_class` entries + `numerical_variation.exact_fields` (partial, 12
of eventually up to 16) + `gim_comparator.parquet`'s `units` (measured from
the real release this session built) = 18.

**4 awaiting your decision**: the `plots/*` group's `comparison_class` +
`units` (4 outputs, one combined decision question — see below) — these are
the only items in Category 2 this session did not apply, because TE §13.7's
own wording does not answer how a rendered image is compared.

**50 awaiting measured run**: every remaining Category-3 field. This session
attempted the real measuring run twice (`run_walking_skeleton.py
--emit-candidate`) and got further than any prior attempt — through stage
00 (acquire) and 01 (inventory/registry) for real, finding and fixing two
real bugs along the way (see below) — but stopped at stage 02 on a genuine,
correctly-firing write-once conflict: a pre-existing candidate `phase1_hourly_target`
release (committed under `e535521`, an earlier attempt) has DIFFERENT
content than what a fresh run against the same declared inputs now produces,
and R-13 refuses to overwrite a citation other artifacts may depend on.
**Choosing how to version this is an owner act** — see the decision question.

## Real bugs found and fixed while attempting the measuring run

1. **`src.data.prepared.load_released_provider_rows` didn't exclude driver
   releases.** Once stage 04 had published the four D-63 driver releases
   into the same shared release root (D-61 option A), stage 02 tried to read
   `hp60_ap60_1h.csv` as five-column provider VTEC and refused on the column
   mismatch — correctly refusing a wrong file, but the file should never
   have reached that check. Fixed: `_non_provider_release_dirs()` now
   excludes all four driver identities, sourced from
   `spaceweather.DRIVER_PRODUCERS` (one import, no duplicated list).
2. **`02_standardize_prepared_target.py` wrote the target CSV to its
   published path before checking whether a conflicting release already
   existed there.** A refused write still silently overwrote the committed
   `hourly_target_phase1.csv` on disk — found because it actually happened,
   twice, during this session's attempts; both times restored from git
   immediately. Fixed: write to a temp path, decide against the manifest
   hash, only `.replace()` into the published path on a new-or-identical
   result; the published file is now provably untouched on a version
   conflict (static proof in `tests/test_fixture_run_fixes.py`).

Both fixes are tested (`tests/test_fixture_run_fixes.py`, 3 tests) and were
necessary just to reach the current (honest, correct) stopping point —
without them, the run was failing on a *wrong* file, or silently corrupting
a committed artifact, neither of which was the real, reportable blocker.

## Why "awaiting external artifact" is empty

The instruction asked me to identify any missing B-01 Kaggle artifact or
other external bytes if the run needed them. It never got that far — stage
02's version conflict stopped it first, using only already-acquired,
already-committed inputs (the Nov 2022 evidence, the driver evidence, the
GIM bundle). Whether B-01/Kaggle artifacts are needed for stages 04 onward
is genuinely unknown from this session — not resolved, not verified absent,
just not reached.

## Full 72-item table

| # | Field | Status | Evidence / reference |
|---|---|---|---|
| 1 | `units.coordinates` | resolved | D-1, D-65, `configs/data.yaml: stations.BSHM.*`; edited in the manifest, verified by grep count drop 72→71 |
| 2 | `input_manifest.yaml.comparison_class` | resolved | D-74; TE §13.7 mechanical application (exact: schema+hash) |
| 3 | `processing_config_snapshot.yaml.comparison_class` | resolved | D-74 (exact) |
| 4 | `hourly_vtec.parquet.comparison_class` | resolved | D-74 (exact: deterministic transform, D-16 median) |
| 5 | `feature_table.parquet.comparison_class` | resolved | D-74 (exact) |
| 6 | `iri_benchmark.parquet.comparison_class` | resolved | D-74 (exact: B-01 GENERATED NOT TRAINED) |
| 7 | `gim_comparator.parquet.comparison_class` | resolved | D-74 (exact: C-01 GENERATED NOT TRAINED, verified deterministic this session) |
| 8 | `split_manifest.json.comparison_class` | resolved | D-74 (exact: partition membership) |
| 9 | `mask_manifest.json.comparison_class` | resolved | D-74 (exact: partition membership) |
| 10 | `predictions.parquet.comparison_class` | resolved | D-74 (toleranced: TE §13.7's own named case) |
| 11 | `metrics.json.comparison_class` | resolved | D-74 (toleranced) |
| 12 | `bootstrap_summary.json.comparison_class` | resolved | D-74 (toleranced) |
| 13 | `checkpoint_manifest.json.comparison_class` | resolved | D-74 (exact: hash/ID) |
| 14 | `registry_entry.json.comparison_class` | resolved | D-74 (exact: TE §13.4 schema/ID) |
| 15 | `plots/target_support.*.comparison_class` | **awaiting your decision** | see decision question below |
| 16 | `plots/predictions.*.comparison_class` | **awaiting your decision** | same |
| 17 | `plots/residuals.*.comparison_class` | **awaiting your decision** | same |
| 18 | `plots/quality_diagnostics.*.comparison_class` | **awaiting your decision** | same |
| 19 | `test_report.*.comparison_class` | resolved | D-74 (exact: pass/fail schema) |
| 20 | `clean_run_log.*.comparison_class` | resolved | D-74 (exact: log schema/hash) |
| 21 | `numerical_variation.exact_fields` | resolved (partial) | D-74; 12 of up to 16 named, plots pending |
| 22 | `inputs.site_log.value` | awaiting measured run | needs `scripts/01_inventory_and_registry.py` execution against BSHM |
| 23 | `inputs.iri.value` | awaiting measured run | needs `scripts/04_build_external_products.py --generate-benchmark` execution |
| 24 | `inputs.ionex.value` | awaiting measured run (partially answerable) | this session's real `gim_comparator_C-01_2022` release covers Apr 10-16, not the fixture's own Nov 1-7 window; re-run `--build-gim-comparator-release --start-date 2022-11-01 --end-date 2022-11-07` to get the fixture's exact window |
| 25 | `inputs.space_weather.value` | awaiting measured run | needs the fixture-scoped driver-release run over Nov 1-7 |
| 26 | `processing.full_config_id` | awaiting measured run | per-run identity; exists the moment stage 00 completes cleanly |
| 27 | `expected_schema.feature.value` | awaiting measured run | additionally gated on G-04 (separate, larger open item, not addressed this session) |
| 28 | `expected_schema.benchmark.value` | awaiting measured run | needs B-01 execution |
| 29 | `expected_schema.comparator.value` | awaiting measured run (partially answerable) | real schema known from `gim_comparator_C-01_2022/gim_comparator.parquet` (12 columns, listed in item 34's units entry) — same window caveat as item 24 |
| 30 | `expected_schema.prediction.value` | awaiting measured run | needs `scripts/06_train_and_predict.py` execution |
| 31 | `expected_schema.metric.value` | awaiting measured run | needs `scripts/07_evaluate_and_report.py` execution |
| 32 | `units.seconds_counts.value` | awaiting measured run | bound at measuring time from TE §6.2's dictionary |
| 33 | `units.external_index_units.value` | awaiting measured run | same |
| 34 | `comparison_ledger.gim_comparator.parquet.units` | **resolved** | real schema measured from `artifacts/releases/gim_comparator_C-01_2022/gim_comparator.parquet` this session (`value_tecu`: TECU; others identifiers/dimensionless) |
| 35-52 | `comparison_ledger.*.units` (remaining 18 of 19 outputs) | awaiting measured run | each needs its producing script executed for real; blocked at stage 02 this session |
| 53 | `row_count_ranges.hourly_target.{min,max}` | awaiting measured run | blocked at stage 02 |
| 54 | `row_count_ranges.feature_window.{min,max}` | awaiting measured run | needs stage 05 |
| 55 | `row_count_ranges.split.{min,max}` | awaiting measured run | needs stage 05 |
| 56 | `support_missingness.target_support.limit` | awaiting measured run | needs stage 02 |
| 57 | `support_missingness.invalid_hour.limit` | awaiting measured run | needs stage 02 |
| 58 | `support_missingness.external_feature.limit` | awaiting measured run | needs stage 04/05 |
| 59 | `support_missingness.comparator.limit` | awaiting measured run | needs stage 04 |
| 60 | `timestamp_tolerances.hourly_boundary.tolerance` | awaiting measured run | needs stage 02 |
| 61 | `timestamp_tolerances.iri.tolerance` | awaiting measured run | needs B-01 |
| 62 | `timestamp_tolerances.gim.tolerance` | awaiting measured run (partially answerable) | this session's `--build-gim-comparator-release` produces the raw values a tolerance would be measured from; the tolerance itself (cross-run variation) needs 2+ repeated runs to measure, not done this session |
| 63 | `timestamp_tolerances.feature_alignment.tolerance` | awaiting measured run | needs stage 05 |
| 64 | `independent_reference_checks.sample_iri_gim_values.value` | awaiting measured run (partially answerable) | GIM half real and available (item 24); IRI half needs B-01 |
| 65 | `runtime.cpu_total.{min,max}_seconds` | awaiting measured run | needs a full clean run, timed |
| 66 | `runtime.storage_total.{min,max}_bytes` | awaiting measured run | same |
| 67 | `numerical_variation.floating_point_tolerances.value` | awaiting measured run | depends on item 15-18's decision landing first, then a real run |
| 68-72 | (the 4 `plots/*.units` fields, already counted in 15-18's row range but tracked here for the exact 72 total): see 15-18 | **awaiting your decision** | same decision question |

(Rows 35-52 and 68-72 are compressed ranges to keep this table readable; the
exact field names are enumerated in `Fixture_TBD_inventory_2026-09-26.md`'s
Category 3 breakdown and in the manifest's own `comparison_ledger` block.)

## Decision question — routed to you, not decided here

**The `plots/*` comparison method (4 outputs: `target_support`,
`predictions`, `residuals`, `quality_diagnostics`).** TE §13.7 states exact
equality for "hashes, schemas, partition membership, IDs, and deterministic
CPU transformations" and tolerances for "floating-point predictions and
metrics" — it says nothing about rendered images.

> **Option A — exact hash.** Byte-for-byte comparison of the rendered file.
> **Impact**: Simplest to implement and verify. Brittle across matplotlib/
> library version changes or font rendering differences on different
> machines — a clean-run environment change unrelated to any real
> reproducibility issue could fail the fixture.

> **Option B — toleranced, perceptual/structural comparison.** Compare
> pixel data within a similarity tolerance (e.g. structural similarity
> index) rather than exact bytes.
> **Impact**: Robust to benign rendering differences. Needs a new dependency
> and a measured similarity threshold (another Category-3 item), and "how
> similar is similar enough" is itself a judgment call with no existing
> project precedent to derive it from.

> **Option C — exempt plots from automated comparison entirely.** Generate
> them, hash-list them in `artifact_manifest.json` (so their presence and a
> stable identity are still checked), but exclude them from the clean-run
> pass/fail ledger.
> **Impact**: Avoids inventing a fragile or under-specified image-comparison
> rule. Weakens the clean-run guarantee for these four specific outputs —
> a silently-broken plot would not fail the fixture. Matches how this
> project already treats other genuinely-unverifiable-by-hash artifacts
> (e.g. `test_report.*`'s own pass/fail schema check, which doesn't
> byte-compare either).

> D. Other (please specify)
>    **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. This project's own TE §13.7 rule doesn't
> reach plots at all, and inventing a perceptual-similarity threshold (B)
> would be exactly the "an implementer choosing it by convenience" TE §1.1
> already forbids for the fields the rule DOES name — extending that same
> discipline to a field the rule doesn't name, rather than guessing, seems
> more consistent with how this project has handled every other genuinely
> open item. Option A's brittleness risk (failing a clean run over a font
> version, not a real regression) seems like the wrong trade for four
> smoke-test plots in a walking-skeleton fixture whose own binding
> limitation already states it produces "not scientific evidence."

[Answer]:

## The target-release versioning conflict — also routed to you

Not one of the original 72 fields, but the actual blocker this session hit
executing the measuring run:

> **Option A — supersede the old candidate.** Delete/archive the 2026-08-2x
> `phase1_hourly_target` release under `e535521` and let a fresh run publish
> under the same citation.
> **Impact**: Unblocks the measuring run immediately. Loses the ability to
> diff exactly what changed between the two runs unless the old one is
> archived first (e.g. renamed aside, not deleted) — recommend archiving,
> not deleting, if chosen.

> **Option B — version the citation.** Change `TARGET_RELEASE_DIR`'s naming
> convention to be version-suffixed (e.g. `phase1_hourly_target_v2`), so
> both live side by side.
> **Impact**: Preserves history cleanly. Is itself a real, non-trivial code
> change (every consumer that reads `phase1_hourly_target` by fixed name
> needs to learn the new resolution rule) — larger than this session's
> remaining scope, and arguably its own decision about how stage
> 05/06/07 should resolve "the current" version.

> C. Other (please specify)
>    **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A (archive, don't delete, the old candidate).
> It's the smallest correct move that unblocks the actual measuring run you
> asked for, and the old candidate's content stays recoverable from git
> history (`e535521`) regardless of what happens to the working copy.

[Answer]:
