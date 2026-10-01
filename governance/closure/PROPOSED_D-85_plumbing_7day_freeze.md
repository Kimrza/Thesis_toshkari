# Proposed D-85: `plumbing_7day` Q-31 freeze (drafted 2026-10-01, NOT adopted)

This is draft text for the Student to adopt, amend or reject. Nothing here is in
`evidence/DECISIONS.md`. The freeze itself is the Student's Q-31 act (TE §18.2; R-134
obligation 2). The agent's attempt to perform the freeze edit on 2026-10-01 was refused by
the session's permission control, and it was not pursued by any other route.

## What is ready

- Reference manifest `tests/fixtures/plumbing_7day/fixture_manifest.yaml`, installed by
  `run_walking_skeleton.py --promote-candidate` (row in `fixture_manifest.promotions.jsonl`;
  the previous skeleton is preserved as `fixture_manifest.superseded_20261001T143501Z.yaml`).
  It is byte-identical to the composed candidate
  `fixture_manifest.candidate_walking-skeleton-plumbing_7day-20261001T142715Z-12195f9f+xenv.yaml`,
  SHA-256 `74292c93a4ce2ba984ab8b2ca859fd69f8a703bac19bae738ac6432dfde72ef6`, `status: candidate`,
  0 `TBD`, loads through `load_fixture_manifest`.
- Composed from exactly the four P-6 designated runs (precommitment P-6,
  `governance/closure/PROGRESS_2026-10-01.md`), code commit `14e09f2`:
  - (a) `tec-thesis-311`: `walking-skeleton-plumbing_7day-20261001T141835Z-e79b04b2`,
    `walking-skeleton-plumbing_7day-20261001T142715Z-12195f9f`;
  - (c) `g07-clean-run` (lock-built env, fresh clone):
    `walking-skeleton-plumbing_7day-20261001T141915Z-32dfaa64`,
    `walking-skeleton-plumbing_7day-20261001T142500Z-3a3f9119`.
- Determinism precondition (D-83 A8 item 9): passed on both legs.
- Item 11 per-field tolerance (D-83 A8 items 10, 17):

  | Output | Field | Unit | max abs (c)-(a) | floor | tolerance |
  |---|---|---|---|---|---|
  | predictions.parquet | y_hat (648) | TECU | 1.9073e-06 | 5.6447e-06 | 5.6447e-06 |
  | metrics.json | paired_loss_differential (24) | TECU^2 | 6.5978e-06 | 3.4519e-05 | 3.4519e-05 |
  | metrics.json | row_count (4) | count | 0 | 5.1260e-06 | 5.1260e-06 |
  | metrics.json | exclusion_count (4) | count | 0 | 1.6689e-05 | 1.6689e-05 |

  The same four values were measured independently by P-3 (different commit, before the
  B-01 re-run and config renormalisation), so they are stable.
- Runtime range (cpu_total) 331.80 to 502.88 s; storage_total 6,146,225 to 6,327,309 bytes.
- Inputs: B-01 re-generated in `b01_iri` 2026-10-01 (`bfe5fd3`; November bit-identical to
  the superseded receipt); configs LF-renormalised (`871be23b`, `1b1ebdfd`, `8427794f`,
  `c951f949`).

## Proposed D-text

> **D-85 — `plumbing_7day` fixture manifest: Q-31 freeze.** The Student freezes
> `tests/fixtures/plumbing_7day/fixture_manifest.yaml` (composed from P-6 runs e79b04b2,
> 12195f9f in `tec-thesis-311` and 32dfaa64, 3a3f9119 in `g07-clean-run`, code commit
> 14e09f2) as the reference for every later `plumbing_7day` run. The acceptance tolerances
> are the D-83 item 11 per-field tolerances it records (table above), derived by the
> adopted rule max(statistic, 2^-23 x max|x|) and not chosen. Smoke evidence only, never
> scientific evidence (TC-03f). Supervisor approval: reported by the Student on 2026-10-01
> as covering the (a)/(c) measuring runs and tolerance freeze; verbal, no written artifact.
> fixture_manifest_sha256: <the SHA-256 printed by step 2 below>

## Freeze steps (the Student's act)

From the repository root, in `tec-thesis-311`:

1. Set `"status": "frozen"` and add `"freeze_citation": {"decision": "D-85"}` inside
   `"identity"` in `tests/fixtures/plumbing_7day/fixture_manifest.yaml` (no other edit).
2. Record its hash beside it:
   `python -c "import hashlib;h=hashlib.sha256(open('tests/fixtures/plumbing_7day/fixture_manifest.yaml','rb').read()).hexdigest();open('tests/fixtures/plumbing_7day/fixture_manifest.sha256','w',newline='\n').write(h+'  fixture_manifest.yaml\n');print(h)"`
3. Append the D-text above to `evidence/DECISIONS.md` as `## D-85 — ...`, with the printed
   hash on its `fixture_manifest_sha256:` line.
4. Verification run (produces the plumbing receipt that `scientific_1month` requires):
   `TEC_ENVIRONMENT_ID=tec-thesis-311 TEC_PLATFORM=local python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day`
