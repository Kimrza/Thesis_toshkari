# Runbook — Kaggle leg for fixture-scale B-01 (plumbing_7day)

**Date:** 2026-09-26. **Ruling:** Kaggle-leg option, Student, 2026-09-26 (recorded in
`CR-2026-09-25-APPARATUS-HYPERPARAMETERS` §7a item 6). **Operator: the Student** — the
D-49 environment exception is personal to a Kaggle session; no agent runs these.

## What this produces

`artifacts/external/b01/` on the Kaggle session: `b01_runtime_identity.json` (pins
before + after), `iri_implementation_validation_report.json` (R-59, status `passed`),
`b01_iri2016_rows.jsonl` + `b01_provenance.json`, `sha256_manifest.json`. Brought back
verbatim, these feed the LOCAL bridge step (§4) that writes `B-01.json` per apparatus
fold into the fixture predictions run — the missing member the R-106 refusal named.

## 0. Preconditions (all existing decisions, none new)

- Kaggle session per **D-49**: CPython 3.10.12, `iricore==1.8.0` wheel
  `f452b22316891d87ee766dba266de6a07e4e6008ab515ffed902ea8b5446a874`; index pins
  `apf107.dat` `cdf4d5df…`, `ig_rz.dat` `fbbed304…` (D-45 annotation). Never run
  `iricore.update()`.
- Repo at the commit carrying the fixture-scale bridge (this runbook's commit or later);
  `--code-commit <that hash>` on EVERY invocation (Kaggle has no git tree; REQ-ENG-10).
- TC-03g: run the critical test set inside the session first
  (`python -m pytest -q` over the D-69 ten-module selection). The
  both-fixtures-inside-Kaggle limb is inapplicable-by-circularity here and is the very
  thing this leg exists to unblock — state that in the session log rather than skipping
  silently.
- Every 04 invocation below carries `--fixture-manifest
  tests/fixtures/plumbing_7day/identity_declaration.yaml`: it scopes the run to the
  D-11 window and takes the Q5 fixture exemption on the receipts gate (a fixture-scoped
  generation is not a full-year job; CR-2026-09-13-04-FIXTURE-WINDOW).

## 1. Pin check BEFORE (D-45 annotation item 2)

```
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --code-commit <HASH> --verify-runtime
```

## 2. R-59 validation report (needs YOUR samples file)

```
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --code-commit <HASH> --build-validation-report <your_samples.json>
```

The samples file is the Student's (R-59's seven areas; the tolerance is already
predeclared in `configs/experiment.yaml: benchmark_b01.validation_report`). A `failed`
report is written as-is and generation stays blocked — never switch implementations to
make it pass.

## 3. Generation (November only — the fixture month)

```
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --code-commit <HASH> --generate-benchmark \
  --validation-report artifacts/external/b01/iri_implementation_validation_report.json \
  --months 11
```

Then repeat §1 (pins AFTER — a drifted pin invalidates the session, D-45).

## 4. Back on this machine (agent-runnable, after artifacts verified against their
`sha256_manifest.json`)

```
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --emit-prediction-payload artifacts/walking_skeleton/plumbing_7day/predictions \
  --benchmark-rows <returned b01_iri2016_rows.jsonl> \
  --benchmark-provenance <returned b01_provenance.json>
```

The bridge re-verifies R-59 at consumption (hashes + passing report) and, at fixture
scale, writes one stamped `B-01.json` per APPARATUS fold via one adapter call per fold
(the adapter's single-bucket break assumes governed-disjoint windows; apparatus day
windows overlap — pinned by
`test_overlapping_apparatus_folds_bucket_correctly_only_via_per_fold_calls`).

## Known remaining blocker after this leg

`gim_comparator.parquet` (TE 15.4 plumbing-required) — generation refuses on Q-15
(interpolation rule, `TBD — freeze gate`, Student-owned) and R-60's overlap-audit
obligation. Separate investigation in progress; this runbook does not cover it.
