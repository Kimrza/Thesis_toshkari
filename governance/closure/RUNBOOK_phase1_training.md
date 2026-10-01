# Runbook: from closure to Phase 1 LSTM training (as of 2026-10-01)

Status of every gate is in `CLOSURE_ASSESSMENT_2026-10-01.md`. Steps marked **BLOCKED** must
not be run until the step before them is done; the scripts refuse anyway.

## 0. Environments (all on LAPTOP-TV4UGFBC, D-83)

| id | where | use | rebuild |
|---|---|---|---|
| `tec-thesis-311` (a) | native Windows conda | every stage script, training | `environment/bootstrap_env.ps1` (win-64 locks) |
| `b01_iri` (b) | WSL2 Ubuntu | B-01 generation only | `bash environment/bootstrap_b01.sh` |
| `g07-clean-run` (c) | WSL2 Ubuntu | G-07 reproduction only | `bash environment/bootstrap_g07.sh <repo> <clone> <commit>` |

Every governed command runs with `TEC_ENVIRONMENT_ID=<id>`, `TEC_PLATFORM=local` and
`PYTHONHASHSEED=0`, from a clean committed tree.

```powershell
conda activate tec-thesis-311
$env:TEC_ENVIRONMENT_ID = "tec-thesis-311"; $env:TEC_PLATFORM = "local"; $env:PYTHONHASHSEED = "0"
python -m pytest -q tests          # dependency + critical-set check; must be all green
```

## 1. Freeze plumbing_7day (the Student's act) — OPEN

Follow `PROPOSED_D-85_plumbing_7day_freeze.md` steps 1–4. Step 4 is the verification run
that writes the plumbing receipt.

## 2. scientific_1month — BLOCKED on 1

1. One undesignated rehearsal in (a):
   `python scripts/run_walking_skeleton.py --config configs/ --fixture scientific_1month --emit-candidate --identity tests/fixtures/scientific_1month/identity_declaration.yaml`
2. Precommit, then two designated runs in (a) and two in (c) (fresh clone, as for P-6).
3. `python scripts/compose_cross_environment_candidate.py --config configs/ --fixture scientific_1month --identity tests/fixtures/scientific_1month/identity_declaration.yaml --outputs-run <a run> --result <4 measuring_result files>`
4. Check every output element resolved to a declared field (the run refuses otherwise);
   that is the field-to-unit table's verification against actual output.
5. The Student's Q-31 freeze (same shape as D-85), then a verification run.

## 3. Governed Phase 1 dataset — BLOCKED on 2

No governed full-year release exists (`artifacts/releases/` holds only a fixture-class
target). TE 13.2 order, each in (a):

```powershell
python scripts/00_acquire_prepared_vtec.py       --config configs/
python scripts/01_inventory_and_registry.py      --config configs/ --phase 1
python scripts/02_standardize_prepared_target.py --config configs/
python scripts/04_build_external_products.py     --config configs/ --phase 1
python scripts/05_build_features_and_splits.py   --config configs/ --phase 1
```

Obligations before 00: team.md re-acquisition record (provider filename with version
suffix, retrieval date, SHA-256); December records stay under the locked root (D-15);
B-01 for January–November must be generated in (b) with `--months 1-11` (December only
after G-05, W-1/W-3).

## 4. LSTM tuning and training — BLOCKED on 3

```powershell
python scripts/06_train_and_predict.py --config configs/ --phase 1
```

- Trains M-01..M-06 on F1–F4 (January–November only; 24 h embargo; expanding window),
  seeds from `seeds.yaml` (three-seed mean is the confirmatory prediction), checkpoints and
  registry rows written by the script. `models.selected` and `refit.epochs` are produced by
  this run's selection record and frozen under their own D-numbers before the refit and
  before G-05; never edit them by hand.
- Progress: `artifacts/registry/experiment_registry.jsonl` (started/completed/aborted rows)
  and the script's stdout.
- Success: a `completed` registry row per run; checkpoint manifest present; no `aborted` row.
- December: never read; the locked-test guard refuses it before G-05
  (`tests/test_locked_test_guard.py`). IRI/GIM: never features; joined only in 07.

## 5. Evaluation against IRI and baselines — BLOCKED on 4

```powershell
python scripts/07_evaluate_and_report.py --config configs/ --phase 1
```

Primary table co-reports persistence, 24 h seasonal persistence and climatology with the
LSTM-vs-IRI comparison (project.md Mandated). Locked December evaluation only after G-05
and G-06, once, hash before metrics.
