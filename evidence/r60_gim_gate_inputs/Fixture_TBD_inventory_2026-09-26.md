# `tests/fixtures/plumbing_7day/fixture_manifest.yaml` — TBD field inventory

Prepared 2026-09-26, in response to the instruction to inventory the fixture's
`TBD — freeze gate` fields by owner and governing rule, provide measured
evidence and concrete proposals where possible, and name what needs a
Student decision — without filling anything by convenience. **Nothing in
this document has been written into the fixture manifest.** The manifest
itself states plainly why: "this file is never edited by code; the measuring
run emits its own candidate and the owner's Q-31 act freezes it."

## Exact count

**72** `TBD — freeze gate` occurrences, counted directly and precisely:
`grep -c '"TBD — freeze gate"' fixture_manifest.yaml` → 72. (An earlier,
looser line-count pass gave 73 by also matching a non-value occurrence; 72
is the exact count of actual `"TBD — freeze gate"` field values, and is
what the category breakdown below sums to.) The preflight refusal message's
"71 other field(s)" counts differently again (likely excluding the one field
it names as the first refusal plus one it treats separately) — 72 is used
throughout this inventory as the verified figure.

Breakdown: **1** stale citation (Category 1) + **20** Student-decision
fields (Category 2: 19 `comparison_class` + 1 `exact_fields`) + **51**
execution-blocked measurements (Category 3: 32 non-ledger + 19
`comparison_ledger.*.units`, which depend on Category 2's classification
landing first) = **72**.

## Category 1 — Already decided elsewhere; this is a stale citation, not an open decision

| Field | Status |
|---|---|
| `units.coordinates` | **Already frozen.** Geodetic: D-1 (`evidence/DECISIONS.md`). Geomagnetic: D-65 (2026-09-21, Q-06/Rec 13), fully populated with provenance in `configs/data.yaml` (IGRF-13, Hapgood-1992 MAG frame, NOAA NCEI coefficient hash). This manifest field is simply **not yet transcribed** from an already-decided source — no new decision is owed, only a citation copy-in at the next manifest revision. |

**Proposed fix** (for the measuring run or a manual transcription, not applied here):
```yaml
units:
  coordinates:
    value: "geodetic under D-1; geomagnetic (centered-dipole, IGRF-13, epoch 2022.5, Hapgood-1992 MAG frame) under D-65"
    source: "configs/data.yaml: stations.<ID>.{lat,lon,geomagnetic_lat,geomagnetic_lon}"
```

## Category 2 — A real Student decision, not a measurement (TE §13.7's own classification)

The manifest's own comment is explicit: assigning each output's
`comparison_class` (exact vs. toleranced) "decides whether a clean run
compares it byte-for-byte or within a tolerance... An implementer choosing
it by convenience is precisely what TE §1.1 forbids." This is **20 fields**:
19 outputs' `comparison_class` + `numerical_variation.exact_fields` (which
the file states is "the same frozen decision").

**Proposed classification**, derived from TE §13.7's own stated rule
("exact equality is required for hashes, schemas, partition membership, IDs
and deterministic CPU transformations; floating-point predictions and
metrics use fixture-derived tolerances") — offered for the Student's
approve/reject, not applied:

| Output | Proposed class | Basis |
|---|---|---|
| `input_manifest.yaml` | exact | schema/ID, no floats |
| `processing_config_snapshot.yaml` | exact | schema/hash |
| `hourly_vtec.parquet` | exact | deterministic CPU transform (D-16 median aggregation), not a model fit |
| `feature_table.parquet` | exact | deterministic CPU transform |
| `iri_benchmark.parquet` | exact | C-01's sibling B-01 is GENERATED, not trained (deterministic) |
| `gim_comparator.parquet` | exact | C-01 is GENERATED, not trained (D-72's rule C is pure deterministic interpolation — verified in this session: identical inputs reproduce identical output to 15 significant figures across repeated runs) |
| `split_manifest.json` | exact | partition membership |
| `mask_manifest.json` | exact | partition membership |
| `predictions.parquet` | **toleranced** | model-fit output (LSTM/ridge/RF), TE §13.7's named floating-point-predictions case |
| `metrics.json` | **toleranced** | derived from predictions, TE §13.7's named case |
| `bootstrap_summary.json` | **toleranced** | resampling-derived statistic |
| `checkpoint_manifest.json` | exact | hash/ID |
| `registry_entry.json` | exact | schema/ID |
| `plots/*.{png,...}` | **toleranced** (or exempt) | rendering can vary by platform/library version; needs the Student's own call on whether plots are compared at all |
| `test_report.*` | exact | pass/fail schema |
| `clean_run_log.*` | exact | log schema/hash |
| `numerical_variation.exact_fields` | *(the classification itself)* | same decision, restated |

This is a **proposal**, not a freeze: 7 of the 19 (predictions, metrics,
bootstrap, plots) are floating-point-derived and TE §13.7 already names
"predictions and metrics" as the toleranced case explicitly, so those four
are close to unambiguous under the cited rule; the other 15 follow by the
same rule's "exact" branch but are the Student's call to confirm.

## Category 3 — Genuinely blocked on executing a real fixture run (measurement, not decision)

**51 fields** remain that TE §15.1 states plainly cannot be written before a
real measuring run: "exact counts, tolerances, and runtimes are measured
from the fixtures and frozen; they are not invented here." No fixture has
ever run. I did not attempt to run the full seven-stage pipeline in this
session — that is a materially larger undertaking (stations/windows through
scripts 00–07) than this task's scope, and inventing plausible-looking
numbers here would be exactly the "unmeasured manifest disguised as a
measured one" the file's own header calls "the worst possible outcome."

| Area | Fields | What unblocks them |
|---|---|---|
| `inputs`: site_log, iri, ionex, space_weather | 4 | A real `scripts/01_inventory_and_registry.py` + `scripts/04_build_external_products.py` run against this fixture's window (BSHM, 2022-11-01..07) |
| `processing.full_config_id` | 1 | Per-run identity; exists the moment any stage script runs |
| `expected_schema`: feature, benchmark, comparator, prediction, metric | 5 | feature is gated on G-04 (separate, larger open item); benchmark/comparator/prediction/metric are each a real run of their producing script away |
| `units`: seconds_counts, external_index_units | 2 | Bound at measuring time from already-frozen dictionary rules (TE §6.2) |
| `row_count_ranges`: hourly_target, feature_window, split (min/max) | 6 | A real run over BSHM Nov 1–7 2022 |
| `support_missingness`: target_support, invalid_hour, external_feature, comparator | 4 | Same |
| `timestamp_tolerances`: hourly_boundary, iri, gim, feature_alignment | 4 | Same |
| `independent_reference_checks.sample_iri_gim_values` | 1 | See below — partially answerable now |
| `comparison_ledger.*.units` (one per output, 19 outputs — depends on Category 2's `comparison_class` landing first) | 19 | Same run, once classified |
| `runtime`: cpu_total, storage_total (min/max) | 4 | Timed/measured during the real run |
| `numerical_variation.floating_point_tolerances` | 1 | Measured; depends on the Category 2 classification landing first |
| **Total** | **51** | 4+1+5+2+6+4+4+1+19+4+1 = 51, verified by direct arithmetic against the 72-field grep count (1 + 20 + 51 = 72) |

## What I CAN offer now, concretely, from this session's own real work

`independent_reference_checks.sample_iri_gim_values` asks for real sample
IRI and GIM values at the fixture's own timestamps. This session built and
ran the real GIM half:

- `artifacts/releases/gim_comparator_C-01_2022/gim_comparator.parquet` — real
  rule-C interpolated values, ARUC/BSHM/NICO, 2022-04-10 through 2022-04-16
  (a different window than the fixture's own Nov 1–7, since only the
  already-acquired months were in scope here) — see the release's own
  manifest for row counts and hashes.
- To produce the fixture's own exact sample (BSHM, 2022-11-01..07), the same
  `--build-gim-comparator-release` CLI added this session can be re-run with
  `--start-date 2022-11-01 --end-date 2022-11-07` against the already-
  acquired `codg305*.22i.Z`..`codg311*.22i.Z` files (day-of-year 305–311) —
  not run in this session, but the mechanism is real, tested, and ready.
- The IRI half needs B-01's own execution path (`scripts/04_build_external_products.py --generate-benchmark`), which is separately gated on its own R-59 validation report and out of this session's scope.

## Governing rules cited throughout

- TE §15.1/§15.2/§15.4 — the fixture manifest's twelve content areas and the
  required-outputs enumeration.
- TE §13.7 — the exact-vs-toleranced classification rule (Category 2).
- TE §18.2 — Student/Supervisor forbidden-choice items (coordinates already
  resolved under this; comparison_class classification is a related but
  distinct TE §13.7 act, not itself a §18.2 item).
- Q-31 — the fixture's own freeze mechanism: identity declared (done,
  2026-09-13), a measuring run emits a candidate, the owner's Q-31 act
  freezes it. No code path performs step 3.
- R-134 control 8 (`_validate_measured`) — refuses a manifest with a measured
  field carrying no `measuring_run_id`, by design, until a real run exists.

## What this inventory does NOT do

It does not run the fixture. It does not call the walking-skeleton fixture
passed — `run_walking_skeleton.py --fixture plumbing_7day` still refuses,
correctly, exactly as it did before this session (verified again after
today's GIM work: same refusal, same field, same reason). It does not fill
any TBD field in the actual manifest file. It surfaces one stale citation
(Category 1), one concrete proposal awaiting Student approval (Category 2),
and a precise list of what a real measuring run would need to touch
(Category 3) — with the GIM-specific portion of that list now backed by
real, working infrastructure this session built.
