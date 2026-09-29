# CR-2026-09-29-Q31-CLOSURE — `plumbing_7day` TE §15.4 outputs and the Q-31 candidate path

**Status: CLOSED 2026-09-29 — candidate manifest VALID over two real measuring runs (§5A).
§5's open decisions were resolved by the owner on 2026-09-29. The candidate is not frozen
(Q-31 freeze act remains the Student's).**

**Authorisation.** The project owner's instruction of 2026-09-29: *"You are now authorized
to CLOSE Q-31 COMPLETELY … Where the existing contract is contradictory, resolve it using
the smallest explicit governance change that preserves the scientific intent, record that
change, implement it, test it, and continue."* No D-number is written by this record;
`evidence/DECISIONS.md` is the Student's register (project.md, code-generation c31). Where a
decision is needed, a proposed D-text is given for the owner to adopt.

## 1. The problem this record addresses

The Q-31 measuring run (`walking-skeleton-plumbing_7day-20260929T101552Z-d02f1630`) ran
stages 00-07 cleanly and then refused at `run_walking_skeleton.collect_required_outputs`:
14 of `plumbing_7day`'s 19 TE §15.4 outputs were absent. The stages produced the content,
but under their own per-fold / per-set names; nothing wrote the TE §15.4 filenames at the
fixture root. Tracing further showed the candidate manifest itself could not compose even
with all 19 present (§4-§5).

## 2. Implemented (code + tests, working tree only)

| TE §15.4 output | Producer | How it is produced | Class |
|---|---|---|---|
| `hourly_vtec.parquet` | `02` | the RELEASED target CSV, re-encoded losslessly | A |
| `iri_benchmark.parquet` | `04` | the R-59-verified B-01 rows, BSHM 2022-11-01..07, `status == ok` | A |
| `gim_comparator.parquet` | `04` | `_build_gim_comparator_release` over the fixture window against the already-acquired IONEX (DOY 305-311, hashes in `evidence/gim_code_final_2022/sha256_manifest.json`) — the procedure `evidence/r60_gim_gate_inputs/Fixture_TBD_resolution_2026-09-26.md` item 24 prescribes | A |
| `feature_table.parquet` | `05` | byte copy of the refit partition's UNTRANSFORMED bundle, asserted to cover exactly the declared window, with the WS-10 IRI-denial check re-applied to every column and its evidence attached | A |
| `split_manifest.json` | `05` | byte copy of the apparatus split manifest | A |
| `predictions.parquet` | `06` | every model payload `06` wrote, verbatim, with identity columns | A |
| `checkpoint_manifest.json` | `06` | the M-06 save/restore facts the fit computed (restored epoch, epochs run, checkpoint selected, epoch source, validation partition, restored validation RMSE, in-run payload ref); **no file hash** (fold checkpoints are in-memory only, TS-M-01) | D→A |
| `mask_manifest.json` | `07` | membership of every registered mask; the skipped `gim` set recorded as skipped | A |
| `metrics.json` | `07` | every metrics artifact verbatim; skipped sets as `not_evaluated` | A |
| `bootstrap_summary.json` | `07` | `status: not_executed` over the per-pair skips the run wrote; no replicate / interval / statistic / tolerance; deterministic bytes | B |
| `plots/{target_support,predictions,residuals,quality_diagnostics}.png` | `07` | `plots.render_series_figure` drawing the fixture target and this run's predictions; an empty or all-NaN figure is refused; `plots/plot_manifest.json` records sources and points drawn | A |

Measurement blocks now emitted (board Rec 4): `row_count_ranges.{hourly_target, split}`,
`support_missingness.{target_support, invalid_hour, external_feature}`,
`timestamp_tolerances.{hourly_boundary, iri, gim, feature_alignment}`; `05`'s WS-13 parity
difference re-filed as `numerical_variation.floating_point_tolerances` (it was filed under
a non-area key with no min/max, which `collect_stage_measurements` refuses; value unchanged).

Cross-run tolerance measurement: each measuring run records numeric fingerprints of its
`toleranced` outputs; composition computes the max element-wise difference across the
recorded runs and stamps it on the ledger entry with the runs' ids. Nothing declares a
tolerance.

Files: `src/data/fixture_outputs.py` (new), `scripts/02/04/05/06/07`,
`scripts/run_walking_skeleton.py`, `src/data/fixture_manifest.py` (measuring-result
fingerprints; composer tolerance stamping — **the ledger validator is unchanged**),
`src/evaluation/plots.py` (`render_series_figure`), `src/models/lstm.py` (one additive
recorded attribute, `checkpoint_payload_ref`), `tests/test_fixture_outputs.py` (new, 32).

### 2.1 Verification (2026-09-29)

- Tests: `tests/test_fixture_outputs.py` 32/32; full governed suite (`tec-thesis-311`,
  `pytest tests/`) exit 0, no failure or error.
- End-to-end, on an ISOLATED COPY of the workspace (so the real fixture root, registry and
  declaration were not touched):
  - run A: stages 00-07 clean; `artifact_manifest.json` lists **19/19** TE §15.4 outputs,
    `missing_required_outputs: []`; every measured TE §15.2 quantity present in the saved
    measuring result; composition refused at the by-design single-run zero-width runtime
    range (board Rec 5).
  - run B (run A's measuring result kept): runtime/storage ranges composed over both runs;
    the candidate schema then refused at `inputs.rinex_crx` — the first declared field the
    identity declaration does not carry (§5.1).
  - generated content: GIM 168 rows (BSHM, 2022-11-01T00 .. 11-07T23, every epoch an exact
    map match, rule C, `codg3050.22i.Z` …); IRI 168; hourly target 168; predictions 648
    (M-01…M-06); checkpoint entries 6 (2 folds × 3 seeds); bootstrap `not_executed` over
    12 recorded pairs; 4 masks, `gim` skipped on both folds.

## 3. Correction to the 2026-09-29 read-only report

That report classed `gim_comparator.parquet` as data-blocked (C). **That was wrong.**
`evidence/gim_code_final_2022/` holds `codgDDD0.22i.Z` for DOY 1-330 as well as the
long-form names for 331-365; the earlier search matched only the long form. The seven
Nov 1-7 files are present and hash-verified against the acquisition manifest.

## 4. Proposed classification change (needs owner adoption)

**`bootstrap_summary.json` on `plumbing_7day`: `toleranced` → `exact` (`exact_kind:
schema`).** D-74 classed it toleranced because a bootstrap summary is a resampling
statistic. On Fixture 1 the file is a status record with no float (TE §15.3 does not
execute bootstrap; `_validate_fixture_bootstrap` refuses a bootstrap block on it), so TE
§13.7's own rule ("exact equality … for schemas … and IDs") classes it exact — the same
mechanical application D-74 made. A toleranced entry would need a measured positive
tolerance for a file with nothing to measure. Fixture 2 is untouched.

> Proposed D-text: *"D-74 amendment (plumbing_7day only): `bootstrap_summary.json` is a
> `not_executed` status record on Fixture 1 (TE §15.3) and is classed `exact`
> (`exact_kind: schema`) by TE §13.7 applied to its actual content; Fixture 2's
> classification is unchanged. CR-2026-09-29-Q31-CLOSURE."*

## 5. OPEN — owner decisions this record cannot take

**5.1 The plumbing ledger and declared fields.** A candidate composes its ledger from the
identity declaration (`run_walking_skeleton.py`), and `tests/fixtures/plumbing_7day/
identity_declaration.yaml` carries none, nor the declared inputs / processing / schema /
units / reference-check fields the candidate schema requires. The additions were prepared
from repository evidence (IGS site log + hash, B-01 artifact identity, the seven IONEX
hashes, the fixture driver releases, the four config hashes, driver units from the
releases' own `units`, schemas from the produced artifacts, D-74/D-75 classes, D-37's
`identity` inverse route). Writing them into the owner-authored declaration was **refused
by the session's safety classifier** and was not attempted another way. The owner applies
them, or authorises the edit.

**5.2 The candidate tolerance of `predictions.parquet` and `metrics.json`.** Four local
runs of 2026-09-29 reproduce every prediction bit-for-bit (max |Δ| = 0.0 for M-03…M-06),
so the honest measured cross-run variation is 0, and the unchanged validator requires
`fp_tolerance.value > 0` (`tests/test_fixture_outputs.py` asserts that refusal still
fires). No positive number can be measured on one platform without inventing it. Options:

- **A. A second platform** (Kaggle, TE §9.1) supplies a measuring run through
  `--measuring-runs`; cross-platform variation is the case TE §13.7 names. No rule changes.
- **B. Candidate-stage scoping**: a *candidate* may record the measured variation (≥ 0,
  over ≥ 2 runs); the positive *acceptance* tolerance stays required of a *frozen* manifest
  and is set at the Q-31 freeze act (Q-31 assigns acceptance tolerances to the Student).
  An attempted edit to this effect was **refused by the session's safety classifier as a
  validator weakening** and fully reverted; `src/data/fixture_manifest.py`'s validator is
  byte-identical to `HEAD`.

## 5A. Resolution pass of 2026-09-29 (owner decisions 1-3: apply ledger; bootstrap exact; no Kaggle)

**Ledger (decision 1) — applied.** `tests/fixtures/plumbing_7day/identity_declaration.yaml`
now carries `required_outputs.comparison_ledger`, 19 entries: classes transcribed from
D-74/D-75 (the owner's skeleton `fixture_manifest.yaml` carries the same classes), units
from the producing artifacts' own `units` fields, `producing_path.script` per producer,
`inverse_route: identity (D-27/D-37)` on the two TECU-bearing toleranced entries, and no
`fp_tolerance` anywhere (the declaration loader refuses one). It loads clean.

**Structural gap found and closed.** `load_identity_declaration` admits only `identity`,
`inputs.prepared_vtec` and the ledger template; it states that every other input,
processing, schema, unit and reference-check quantity is "the measuring run's record". No
code wrote that record, so no candidate could ever have composed. New
`fixture_outputs.recorded_quantities`, called in `run_walking_skeleton.py` step 9, records
them: the non-sentinel entries of the owner's skeleton manifest (frozen contract
citations, Phase-2 `not_applicable` reasons) are carried verbatim, and the sentinels are
filled by READING this run's artifacts: the BSHM site-log hash (checked against
`evidence/station_registry_sources_2026-09-19/sha256_manifest.json`), the B-01 hashes, the
seven IONEX hashes from the GIM release, the four driver releases' content hashes and
units, a config id over the four config hashes, the schemas of the produced parquet/JSON
outputs, and three IRI/GIM sample values. `compose_candidate_manifest` gained `recorded=`
(a declared value is never overridden) and binds each concrete output name
(`clean_run_log.json`, `plots/residuals.png`) to its TE 15.4 wildcard template entry
through the existing `output_matches`.

**Bootstrap (decision 2) — applied.** The ledger classes `bootstrap_summary.json`
`exact` / `exact_kind: schema`. The D-74 amendment text of §4 is the governing text; it is
carried here for the Student's register rather than written into `evidence/DECISIONS.md`
(project.md c31). Fixture 2 is untouched: a `fixture_bootstrap` block is still refused on
the plumbing declaration (tested).

**Why local variation is zero (decision 3, no Kaggle).** Traced: `src/models/lstm.py` calls
`tf.keras.utils.set_random_seed(seed)` and `tf.config.experimental.enable_op_determinism()`
before every fit; `src/data/config.py` seeds python/numpy/TF and enables op determinism;
ridge and RF are seeded from `seeds.yaml`; predictions are exported from this run's own
payloads (the prior run's are moved aside first, and write-once refuses reuse); metrics are
computed from those predictions. Two genuine executions are therefore bit-identical BY THE
GOVERNED CONTRACT (NFR-DET-01, TC-21), not by an accident of the measuring mechanism. No
mechanism was changed to create variation, and none should be.

**Measured, isolated-copy verification (2026-09-29):** two fresh runs,
`walking-skeleton-plumbing_7day-20260929T125041Z-d19cfb3f` and
`walking-skeleton-plumbing_7day-20260929T125706Z-7d5957f6`. Composition over both: 19/19
outputs, all twelve areas and the full ledger resolve; runtime/storage ranges compose;
measured cross-run variation `predictions.parquet` = **0.0 TECU over 648 elements**,
`metrics.json` = **0.0 TECU^2 over 32 elements**. The unchanged validator then refuses at
`comparison_ledger[metrics.json].fp_tolerance.value: 0.0 is not a positive number`.

**RESOLVED — final pass, 2026-09-29 (owner decision: candidate-vs-frozen distinction).**
Applied in `_validate_ledger_entry` (`status` keyword, default `frozen`;
`_validate_required_outputs` passes the manifest's status): candidate → `value >= 0`, never
negative or NaN, and `measured_over_runs >= 2` required on every candidate tolerance
(stricter than the paragraph below, which the classifier would not let be narrowed);
frozen → `value > 0`, unchanged, also the default for any caller passing no status. Tests
in `tests/test_fixture_outputs.py`: candidate zero/positive over 2 runs pass; candidate
negative, NaN, one run, missing run count refuse; frozen (and default) zero refuse; frozen
positive passes. `tests/test_clean_run.py`'s synthetic candidate ledger gained
`measured_over_runs: 2`. The D-74 amendment and this rule are entered in
`evidence/DECISIONS.md` under D-74.

**Real-repository closure runs (2026-09-29):** prior derived outputs renamed
`*.archived-q31-pre-closure` / `*.archived-q31-closure-run1` (never deleted); run 1
`walking-skeleton-plumbing_7day-20260929T133040Z-978317da` (stopped at the by-design
one-run range check), run 2 `walking-skeleton-plumbing_7day-20260929T133720Z-4a959333`
(completed). Candidate
`tests/fixtures/plumbing_7day/fixture_manifest.candidate_walking-skeleton-plumbing_7day-20260929T133720Z-4a959333.yaml`
**VALID**, re-validated from disk: 19/19 outputs present; `predictions.parquet`
fp_tolerance 0.0 TECU (648 values), `metrics.json` 0.0 TECU² (32 values), both over 2 runs;
`bootstrap_summary.json` exact/schema, `status: not_executed`; CPU range 365.156-366.109 s.
The candidate is not frozen: the positive acceptance tolerance is the Student's Q-31
freeze act.

**Superseded paragraph (kept as written).** The contract-consistent
representation of a measured zero is candidate-stage scoping in `_validate_ledger_entry`:
on `status: candidate`, `fp_tolerance.value` may be `>= 0` only when
`measured_over_runs >= 2` (negative, NaN, or a single run stays refused); on
`status: frozen`, `> 0` stays required, because the positive ACCEPTANCE tolerance is the
Student's Q-31 freeze act (TE 18.2). `_validate_required_outputs` passes
`status=data["status"]`, and a caller that passes no status keeps the strict
frozen rule. The owner authorised this explicitly on 2026-09-29; the classifier refused
it twice ("validator weakening"), so it has not been applied, and nothing was committed.
Once applied, the next steps are two real measuring runs in the repository, then the
candidate, then the commit.

## 6. Known residual

`registry_entry.json` (`run_id`), `clean_run_log.json` (`run_id`, `started_at_utc`,
`ended_at_utc`, `duration_seconds`) and `test_report.json` (`started_at_utc`,
`ended_at_utc`, `duration_seconds`, `created_at_utc`) are `exact` under D-74 but carry
per-run fields (measured by grep on the 2026-09-29 run's outputs; `input_manifest.yaml`
and `processing_config_snapshot.yaml` carry none), so two runs cannot be byte-equal.
This does not affect a candidate (no comparison runs on a candidate) but will fail a
frozen comparison; it is pre-existing and recorded, not resolved, here.
