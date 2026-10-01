# Autonomous execution progress (started 2026-10-01) — durable, append-only

Mandate: the Student's instruction of 2026-10-01, "Autonomous Thesis Project Closure, Scientific
Validation, LSTM Training, and IRI Comparison" (Stages 1-6). The Student gave explicit approval
for the D-85 `plumbing_7day` freeze (promotion, `status: frozen`, `identity.freeze_citation`,
sibling SHA-256, D-85 in `evidence/DECISIONS.md`, post-freeze verification run, evidence). That
approval covers nothing else. Entries are appended in order; nothing above is edited.

## Starting state (verified 2026-10-01)

- Branch `main`, HEAD `5e57651`, 43 commits ahead of `origin/main`. Uncommitted: AI-DLC audit
  shard only; untracked `SRAMPUFThesis/`, `thesis/` (not touched by this work).
- `evidence/DECISIONS.md`: last D-number D-84; D-85 unused.
- Reference manifest `tests/fixtures/plumbing_7day/fixture_manifest.yaml` SHA-256
  `74292c93a4ce2ba984ab8b2ca859fd69f8a703bac19bae738ac6432dfde72ef6`, `status: candidate`,
  byte-identical to the composed P-6 candidate `...20261001T142715Z-12195f9f+xenv.yaml`;
  promotion row present in `fixture_manifest.promotions.jsonl` (authorization D-85).
- No change under `src/`, `scripts/`, `configs/`, `environment/`, `pyproject.toml` between the
  P-6 code commit `14e09f2` and HEAD (`git diff --stat 14e09f2 HEAD -- ...` empty).

## Stage 1 — D-85 plumbing_7day freeze

### Independent verification before the freeze

Recomputed from the four P-6 measuring results (not read from the candidate):
`artifacts/walking_skeleton/plumbing_7day/measuring_result_...{e79b04b2,12195f9f}.json` (a) and
`artifacts/walking_skeleton/plumbing_7day_g07_p6/measuring_result_...{32dfaa64,3a3f9119}.json` (c).

| Output | Field | n | det (a) | det (c) | max abs (c)-(a) | floor 2^-23 max abs (a) | tolerance |
|---|---|---|---|---|---|---|---|
| predictions.parquet | y_hat | 648 (15 NaN, same positions in all four runs) | 0.0 | 0.0 | 1.9073486328125e-06 | 5.644682211970213e-06 | 5.644682211970213e-06 |
| metrics.json | paired_loss_differential | 24 | 0.0 | 0.0 | 6.5977969825326e-06 | 3.4518555001273005e-05 | 3.4518555001273005e-05 |
| metrics.json | row_count | 4 | 0.0 | 0.0 | 0.0 | 5.125999450683594e-06 | 5.125999450683594e-06 |
| metrics.json | exclusion_count | 4 | 0.0 | 0.0 | 0.0 | 1.6689300537109375e-05 | 1.6689300537109375e-05 |

All four equal the candidate's `fp_tolerance` values. Runtime cpu_total range 331.796-502.875 s
and storage_total 6,146,225-6,327,309 bytes equal the min/max of the four runs. Serialisation
round-trip of the installed manifest (json, indent 2, sorted keys, CRLF) is byte-identical, so the
freeze edit changes only the two intended fields.

### Defect found before the verification run (fixed in `51f81f7`)

The first freeze attempt (manifest `74292c93...` frozen to `42f5e5bd...`, D-85 drafted) was
reverted uncommitted when inspection of `compare_required_outputs` and `run_walking_skeleton._run`
showed the comparison would be vacuous: the candidate's `artifact_manifest_ref` was
`..\..\..\artifacts\walking_skeleton\plumbing_7day\artifact_manifest.json`, the directory the
comparison run rewrites (step 7) before it compares (step 8, which re-reads the listing). Every
output would have been compared against itself (R-139; PV-10 Rec 20 had been marked implemented
on this path). The ref was also a Windows relpath that Linux (c) cannot resolve. A second
defect: every `exact` output was compared by whole-file SHA-256, while `schema` outputs carry
their run id and durations, measured as differing A9 vs A10 (clean_run_log, registry_entry,
test_report, processing_config_snapshot). Fix: reference snapshot dir written once at
composition and cited by POSIX relpath; comparison refuses a reference inside the produced tree
and re-verifies reference hashes; `schema`/`hash` kinds compared per TE 13.7 when bytes differ
(probe: schema and SHA-256 leaves equal across A9/A10 and (a)/(c) for all such files); other
kinds stay byte-exact. Tests `tests/test_fixture_reference_isolation.py` (12). Non-restricted
suite: exit 0, 1567+ passed, 4 skipped, 0 failed.

Open for G-07, not Stage 1: on P-6, (c) differs from (a) in bytes for `split_manifest.json`
(CRLF only), `mask_manifest.json` (mask_id values differ) and `checkpoint_manifest.json`
(`restored_validation_rmse` differs ~1e-8), all `exact` byte kinds. A (c) comparison run
against the frozen manifest would refuse on these.

### Freeze performed (Student's D-85 authorization)

- Re-composed `...12195f9f+xenv2.yaml` (SHA-256 `44b15c9d...`) from the same four results;
  differs from `+xenv` only in `artifact_manifest_ref` (verified by full-tree diff).
  Reference dir `tests/fixtures/plumbing_7day/reference_walking-skeleton-plumbing_7day-20261001T142715Z-12195f9f-xenv2/`
  (listing byte-identical to A10's, `279e38ba...`).
- Promoted with `--promote-candidate` at `20261001T161830Z` (authorization D-85); previous
  installation preserved as `fixture_manifest.superseded_20261001T161830Z.yaml`.
- Frozen manifest SHA-256 `92aa38c0edb05edd62d4a35901375c42d164496b6c9c452c587fbaa88cc48933`;
  sibling `fixture_manifest.sha256` agrees; D-85 recorded in `evidence/DECISIONS.md`.
- F7: `assert_freeze_record_agrees` PASS (source `evidence/DECISIONS.md#D-85`);
  `assert_identity_agrees_with_decisions` PASS (D-11 window, D-20 station, 2 clauses verbatim).
- Fixture root cleaned for the verification run: A10's live outputs moved aside with suffix
  `.archived-d85v1` (directories to `archived_releases/{ev,ex,fe,mr,pr}.d85v1`, mapped in
  `ARCHIVE_NAME_MAP.tsv`; GIM release to `releases/gim_comparator_C-01_2022.archived-d85v1`).

### Verification run V-1: aborted (comparator defect, fixed in `147654f`)

- Command (a) `tec-thesis-311`, `PYTHONHASHSEED=0 TEC_PLATFORM=local`:
  `python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day --code-commit 6fa8f1a...`
- Run `walking-skeleton-plumbing_7day-20261001T162304Z-964ce8a8`, code `6fa8f1a`; registry row
  `aborted`, reason `integrity_refusal (IntegrityError)`; log
  `governance/closure/d85_verification/run1.log`.
- The comparison was real this time and refused on `input_manifest.yaml` at
  `/fixture_stamp/frozen_manifest_hash` (null in the measuring-run reference, the frozen hash in
  a comparison run: different by construction; also embedded in byte-exact
  `split_manifest.json`). Full diff of V-1's outputs against the reference: content identical;
  only the stamp, `processing_config_snapshot.snapshot_dir` and `metrics.json` timestamps
  differed.
- Fix `147654f`: stamp set aside, required equal to the reference stamp except
  `frozen_manifest_hash`, which must equal the frozen manifest's SHA-256; structured exact
  outputs then compared by kind (schema / hash / exact value equality). Tests 19 in
  `tests/test_fixture_reference_isolation.py`, `tests/test_clean_run.py` green.
- V-1 outputs moved aside with suffix `.archived-aborted-d85v1` (directories
  `archived_releases/*.d85a1`).

### Verification run V-2: aborted on storage_total (measurement defect, fixed in `91da686`)

- Run `walking-skeleton-plumbing_7day-20261001T164940Z-50846483`, code `5a9839b`, started
  2026-10-01T16:49:21Z; log `governance/closure/d85_verification/run2.log`; registry row
  `aborted`, `integrity_refusal`.
- All 19 required outputs MATCHED the frozen expectation: the 13 exact outputs (8 byte-equal,
  5 schema/hash/value-equal with the stamp bound to `92aa38c0...`), the 2 toleranced outputs
  under the D-83 item 11 per-field tolerances, and the 4 plots by presence. Runtime was in range
  (wall time about 451 s; stage sum 428 s).
- Refused: `storage_total` 6,533,878 bytes against [6,146,225, 6,327,309]. Breakdown of the
  live root: 43 accumulated `releases/plumbing_7day_<utc>` directories held 3,714,039 bytes,
  and 7 live measuring-result files held 431,574 bytes. The measurement summed run history, so
  the D-85 storage range is itself defective.
- Fix `91da686`: the run snapshots the live root before its first write and counts only the
  files it created or rewrote. Tests are in `tests/test_resources_and_storage.py`.
- Consequence: plumbing_7day must be re-measured (precommitment P-7) and re-frozen. A re-freeze
  is a new freeze act on a manifest D-85 already froze. Its form (a new or sub-numbered
  D-number) is routed to the Student; the agent writes no new D-number unasked.
- Environment note: the active power scheme on LAPTOP-TV4UGFBC is the vendor "Silent" scheme
  (AC power, 99 %). V-1's stage 06 took 556 s against 225-253 s in P-6. The agent may not
  change system settings.
