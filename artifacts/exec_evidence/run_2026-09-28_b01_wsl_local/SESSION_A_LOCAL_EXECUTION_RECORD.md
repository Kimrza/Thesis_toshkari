# Session A (B-01 Kaggle leg) executed locally on WSL2 — execution record

**Date:** 2026-09-28. **Platform:** WSL2 (Ubuntu) on `LAPTOP-TV4UGFBC`, ruled in as
satisfying D-49's B-01 environment exception under the same laptop/local platform
(`D-49 addendum 2`, `evidence/DECISIONS.md`, approved by the project owner verbatim
2026-09-28). Not Kaggle's cloud infrastructure. `TEC_PLATFORM=local` throughout.

## 1. Environment setup

```
$HOME/miniconda3/bin/conda create -y -n b01_iri -c conda-forge --override-channels python=3.10.12
source $HOME/miniconda3/bin/activate b01_iri
pip install iricore==1.8.0 numpy==1.26.4 fortranformat==2.0.3 pymap3d==3.2.0 pyyaml==6.0.1
$HOME/miniconda3/bin/conda install -y -n b01_iri -c conda-forge --override-channels libgfortran5
```
Note: Anaconda's `defaults` channel returned HTTP 403 for this network at the time of
this session (Cloudflare-fronted, `repo.anaconda.com`); `conda-forge` was used instead
and worked without issue. `libgfortran5` (GNU Fortran runtime) was a missing system
dependency for the compiled `libiri2016.so` inside the `iricore` wheel — not documented
anywhere in the project prior to this run; installed from conda-forge, no root needed.

## 2. Pin check BEFORE — PASSED

```
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --code-commit 989f290 --verify-runtime
```
Result: `apf107.dat` `cdf4d5df...`, `ig_rz.dat` `fbbed304...` — both match D-49 item 3
exactly. `iri_version_requested: 16`. Full report:
`artifacts/external/b01/b01_runtime_identity.json`.

## 3. R-59 validation report — PASSED

```
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --code-commit 989f290 --build-validation-report kaggle/b01_validation_samples.json
```
Used the existing, prior-session-sourced 8-sample file (CCMC IRI-2016 official web
interface reference values, retrieved 2026-09-20, saved reference texts under
`kaggle/official_reference_outputs/`) — not newly fabricated. Status: `passed`.
Full report: `artifacts/external/b01/iri_implementation_validation_report.json`.

## 4. Generation (November only) — COMPLETED, 0 errors

```
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --code-commit 989f290 --generate-benchmark \
  --validation-report artifacts/external/b01/iri_implementation_validation_report.json \
  --months 11
```
2160 rows generated (0 error rows), 527.6 s. Output:
`artifacts/external/b01/b01_iri2016_rows_partial.jsonl` (named `_partial`: a
`--months`-restricted, not full-year, product — by the script's own design).

## 5. Pin check AFTER — PASSED, no drift

Same command as step 2, re-run after generation. Hashes identical to step 2.

## 6. Local bridge — COMPLETED

```
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --emit-prediction-payload artifacts/walking_skeleton/plumbing_7day/predictions \
  --benchmark-rows artifacts/external/b01/b01_iri2016_rows_partial.jsonl \
  --benchmark-provenance artifacts/external/b01/b01_provenance.json
```
Wrote `B-01.json` into both `predictions/FIX-NOV-FOLD-01/` and `.../FIX-NOV-FOLD-02/`.

## 7. Fixture ladder re-run (governed 3.11 env, not WSL) — stages 00-06 clean

`python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day
--emit-candidate --identity tests/fixtures/plumbing_7day/identity_declaration.yaml
--code-commit 989f290` — required three archive-and-retry cycles for leftover
non-identical-config-hash artifacts from earlier sessions (same class of issue as the
R-13 recurrence already recorded in the D-76 addendum; each cycle's leftover bundles
were confirmed untracked/uncommitted scratch before removal, never a committed
artifact). Final clean pass: stages 00-06 completed, stopped at stage 07 needing B-01
— exactly the expected refusal.

## 8. Stage 07, invoked standalone (mirroring the orchestrator's own argv exactly, to
avoid a fourth full-ladder re-run) — NEW STRUCTURAL BLOCKER FOUND

```
python scripts/07_evaluate_and_report.py --config configs/ --phase 1 \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --code-commit 989f290 \
  --predictions-run artifacts/walking_skeleton/plumbing_7day/predictions \
  --evaluation-out artifacts/walking_skeleton/plumbing_7day/evaluation \
  --target-release-manifest artifacts/walking_skeleton/plumbing_7day/releases/phase1_hourly_target/release_manifest.json \
  --budget-artifact artifacts/prepared_target/uncertainty_budget.json
```

Result:
```
07_evaluate_and_report: aborted: comparison set primary: members disagree on source_id
['GNSS_VTEC', 'IRI2016_B01']; a comparison across target lineages is not a comparison
(Vision §2.2/§6.6 stamp rule; TE §13)
```

**Diagnosis.** `src/evaluation/masks.py: build_comparison_mask` requires every member of
a declared comparison set to agree on `phase_id`, `source_id`, and `target_definition_id`
(the W-1 stamp rule). M-01/M-02/M-03/M-06's predictions carry `source_id: "GNSS_VTEC"`
(confirmed by direct inspection of the written prediction JSON files).
`configs/experiment.yaml: benchmark_b01.stamps` sets `source_id: "IRI2016_B01"` — a
DIFFERENT value — while `target_definition_id: "GRIDDed_VTEC_1H"` in the same block was
already deliberately aligned to match the models' (its own comment says "B-01 is scored
on that target"). `source_id` was not similarly aligned. `src/external/iri.py` reads
`source_id` straight from this config value (`contract.stamps["source_id"]`) with no
independent logic — this is a configuration value, not a code defect.

**This is the first time this exact interaction has ever been exercised end-to-end** —
the B-01 Kaggle leg had never previously been run to completion on any clone before this
session, so this stamp mismatch was structurally unreachable until now. Not previously
discussed anywhere in the governance record (checked: no mention of `IRI2016_B01` or this
`source_id` question in `governance/` or `evidence/`).

**Not fixed by this session.** `source_id` is one of the three stamped-identity fields
Vision §2.2/§6.6 and TE §13 govern — exactly the class of value this project's own
practice treats as requiring explicit Student authorization before an agent changes it,
and it is the FIRST time this specific value has ever been exercised, so the correct
resolution (does `source_id` mean "target data source" — in which case B-01 should also
read `GNSS_VTEC`, since it predicts the same real target via an independent method — or
does the project intend something more specific by a per-method tag, in which case the
mask rule or the `primary` set's membership needs a different fix) is a decision, not an
obvious correction.

**No evaluation output was written.** The refusal fires before any file write
(`artifacts/walking_skeleton/plumbing_7day/evaluation/` does not exist) — no partial,
misleading, or fabricated result exists anywhere.
