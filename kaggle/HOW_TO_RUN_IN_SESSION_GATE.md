# How to run the TC-03g in-session gate on Kaggle

**Updated 2026-09-27 (GOV-2026-09-27-BT-02 continuation session, second pass).**
Every command below has now been verified locally against commit `b63a7e0` plus
this session's fixes — **not inside Kaggle itself, which remains untested by this
session.** Read "What is verified vs. what is not" before booking anything.

## What is verified vs. what is not

**Verified locally, this session, with reproducible commands and logs (never a
governed run, never a December byte):**

1. `scripts/gate_in_session.py`'s fixture invocation was missing
   `--emit-candidate --identity <path>` and would have failed inside Kaggle on
   both fixtures. **Fixed** (commit pending as of this writing) and covered by a
   new bite-proofed test, `tests/test_in_session_gate.py::test_the_wrapper_s_fixture_invocation_is_a_measuring_run_with_the_right_identity`.
2. A real R-13 release conflict existed in the local artifact tree (a previous
   session's D-33 governance-comment edit to `configs/data.yaml` shifted that
   file's hash, which is stamped into the target release's
   `aggregation_config_id`). **Diagnosed and resolved** by archiving the
   affected releases/feature-bundles/predictions under the project's existing
   `.archived-<commit>` convention and re-running — see
   `evidence/DECISIONS.md` "D-76 addendum" for the full diagnosis. Every
   scientific value was confirmed byte-identical before archiving; nothing was
   guessed.
3. With both of the above fixed, `python scripts/run_walking_skeleton.py
   --config configs/ --fixture plumbing_7day --emit-candidate --identity
   tests/fixtures/plumbing_7day/identity_declaration.yaml --code-commit
   b63a7e0` now runs stages 00 through 06 **successfully** and stops at stage
   07 on exactly one refusal:
   ```
   07_evaluate_and_report: aborted: comparison set primary on partition
   FIX-NOV-FOLD-01: prediction(s) missing for declared member(s) ['B-01'];
   the mask is built over the declared set exactly, never over whatever
   arrived (R-106)
   ```
   This is the **same structural refusal** `CHANGE_RECORD_2026-09-25_apparatus_hyperparameters.md`
   §7a item 6 already documented on 2026-09-26: the comparison set `primary`
   declares member `B-01` (the IRI-2016 benchmark), and no B-01 payload exists
   locally — it requires `iricore`, a Linux-only wheel, which only Kaggle can
   provide (D-49). **This is the one concrete remaining local blocker**, named
   precisely, not fabricated around.
4. Full log: `artifacts/exec_evidence/run_2026-09-27_kaggle_readiness/plumbing_7day_emit_candidate_b63a7e0.log`.
   Focused test suite green: `tests/test_in_session_gate.py` (11/11),
   `tests/test_fixture_run_fixes.py`, `tests/test_prepared_target_schema.py`,
   `tests/test_recorded_presence.py`, `tests/test_release_hashes.py`,
   `tests/test_locked_test_guard.py`, `tests/test_clean_run.py` — all pass, no
   new failures, no guard weakened.

**NOT verified — can only be confirmed inside an actual Kaggle session:**

- That `iricore==1.8.0` actually installs and runs on Kaggle's current base
  image (glibc compatibility for the `manylinux_2_35` wheel).
- That `scripts/gate_in_session.py` end-to-end, including the critical test
  set and the `emit_in_session_gate_result` write, behaves the same way under
  Kaggle's actual filesystem/platform stamp as it does against synthetic
  inputs locally (`test_in_session_gate.py` tests the wrapper's logic with
  synthetic locks/manifests, not a real Kaggle run).
- Real network/session behaviour (Kaggle account phone verification,
  dataset upload size/time, session timeout limits).
- Whether stage 07 clears once a real B-01 payload exists — the local
  dry-run above proves everything **up to** that point works; it does not
  prove what happens after, since no B-01 payload exists here to test with.

**Do not treat this file's local verification as proof Kaggle will succeed.**
It proves the commands are syntactically and logically correct against this
repository as it stands, and identifies the one real remaining gap.

## What TC-03g actually requires, quoted from its own rule

`project.md` § Mandated: *"ALWAYS run the critical test set and both walking-skeleton
fixtures **inside the Kaggle session** before any governed run executed there, capturing
the result in that run's evidence record. A Kaggle session carries no git working tree, so
a commit hook cannot fire there and a local suite run proves nothing about the environment
the governed run actually executes in."* (TE §9.1, §9.2; `constraint-register.md` TC-03g;
TA-03, TA-26.)

## The two Kaggle sessions you need, in order

There are **two separate Kaggle sessions**. Do the first one first; only book
the second after the first's output has been brought back and the fixture
ladder clears locally.

- **Session A — the B-01 leg.** Produces the IRI-2016 benchmark payload. This
  is the one concrete blocker named above. Do this first.
- **Session B — the TC-03g in-session gate.** Runs the critical test set and
  both fixtures inside Kaggle, for the durability/environment-attestation
  requirement. Only book this after Session A's output is bridged back locally
  and the fixture ladder passes stage 07 locally (confirms the payload is
  correctly formed before spending a second Kaggle session).

---

## Session A — the B-01 Kaggle leg (numbered, beginner-friendly)

**Full technical runbook:** `governance/RUNBOOK_2026-09-26_kaggle_b01_fixture_leg.md`
(verified current 2026-09-27 except its own "known remaining blocker" note on
Q-15/`gim_comparator.parquet`, which is now stale and safe to ignore — Q-15 was
frozen as D-72 on 2026-09-26 and a governed release already exists).

### 1. What to upload

Create a **private Kaggle dataset** (Kaggle → Create → New Dataset), not a
notebook file attachment, containing the whole repository working tree:
`configs/`, `src/`, `scripts/`, `tests/` (including `tests/fixtures/`),
`requirements.txt`, `pyproject.toml`, and the `evidence/` months the fixture
manifest cites. **Do NOT upload `evidence/locked_test_restricted/`** — the
locked December root must never leave this machine (Vision §8.3; D-15).

### 2. Notebook/session settings

| Setting | Value | Why |
|---|---|---|
| Accelerator | **None / CPU** | TC-01: CPU is a complete execution path |
| Internet | **ON** | needed to install `iricore` and its index files |
| Environment | build a **Python 3.10** virtual environment inside the session | D-49's exception is 3.10 for this benchmark only — do not use the kernel's default interpreter without checking its version first |
| Dataset | attach the private dataset from step 1 | no other attachment needed |

### 3. Cells/commands, in order

```bash
# cell 1 — confirm the interpreter, then install iricore==1.8.0 and its pinned index files
python --version   # must print 3.10.x
pip install iricore==1.8.0
# apf107.dat / ig_rz.dat SHA-256s must match D-49/D-45's recorded values — verify before use

# cell 2 — pin check BEFORE (D-45 annotation item 2)
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --code-commit <HASH> --verify-runtime
```
Expected output: a runtime-identity report confirming CPython 3.10.12,
`iricore==1.8.0`, and both index-file hashes. **If any hash disagrees, stop —
do not proceed with a drifted pin.**

```bash
# cell 3 — R-59 validation report (needs YOUR OWN samples file — see below)
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --code-commit <HASH> --build-validation-report <your_samples.json>
```
`<your_samples.json>` is a file **you** (the Student) prepare, covering R-59's
seven required areas — this is not something an agent may fabricate. Expected
output: a JSON report ending in `"status": "passed"`. **If it says `"failed"`,
stop — do not switch implementations to force a pass; that is a governance
violation (project.md § Forbidden).**

```bash
# cell 4 — generation (November only, the fixture month — never run over December)
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --code-commit <HASH> --generate-benchmark \
  --validation-report artifacts/external/b01/iri_implementation_validation_report.json \
  --months 11

# cell 5 — pin check AFTER (a drifted pin invalidates the whole session, D-49)
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --code-commit <HASH> --verify-runtime
```

### 4. What successful output looks like

`artifacts/external/b01/` in the Kaggle session's working directory contains:
`b01_runtime_identity.json`, `iri_implementation_validation_report.json`
(status `passed`), `b01_iri2016_rows.jsonl`, `b01_provenance.json`,
`sha256_manifest.json`. No error text in the cell outputs; the last cell's pin
check matches cell 2's.

### 5. Download and send back to me (or bring to your own local bridge step)

From Kaggle's Output pane, download the whole `artifacts/external/b01/`
folder. **What you should return**: all five files listed in step 4, plus the
full cell outputs/console log of cells 1–5 (as text, not a screenshot — hashes
need to be copy-checkable).

### 6. The local bridge step (run on YOUR governed machine, not Kaggle)

After verifying the returned files against their own `sha256_manifest.json`:
```bash
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --emit-prediction-payload artifacts/walking_skeleton/plumbing_7day/predictions \
  --benchmark-rows <returned b01_iri2016_rows.jsonl> \
  --benchmark-provenance <returned b01_provenance.json>
```
This re-verifies R-59 at consumption and writes one stamped `B-01.json` per
apparatus fold.

### 7. Confirm locally before booking Session B

```bash
export TEC_PLATFORM=local
export PYTHONHASHSEED=0
python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day \
  --emit-candidate --identity tests/fixtures/plumbing_7day/identity_declaration.yaml \
  --code-commit <your current commit>
```
Expected: this now passes stage 07 (the exact refusal quoted at the top of
this file should no longer occur). If it still refuses at 07 with the same
`B-01` message, the bridge step (6) did not complete correctly — check the
returned files' hashes again before re-attempting.

### Troubleshooting (Session A)

| Symptom | Likely cause | Fix |
|---|---|---|
| `pip install iricore==1.8.0` fails / no matching wheel | Kaggle's glibc doesn't match the `manylinux_2_35` wheel | This is a real, reportable blocker — do not substitute a different `iricore` version (violates D-49's exact pin) |
| pin-check hash disagrees | Kaggle's environment installed a different `apf107.dat`/`ig_rz.dat` | Re-download the exact pinned files; never proceed on a hash mismatch |
| R-59 report says `"failed"` | Your samples don't match the implementation to the declared tolerance | Investigate the implementation or the samples — never force a pass |
| `--generate-benchmark` refuses citing December | You passed the wrong `--months` value | Use `--months 11` only, never touch December from this leg |

---

## Session B — the TC-03g in-session gate (after Session A + step 7 above succeed)

### 1. What to upload

Same private Kaggle dataset as Session A, refreshed to the commit where stage
07 now passes locally (confirmed in Session A step 7).

### 2. Notebook/session settings

| Setting | Value | Why |
|---|---|---|
| Accelerator | **None / CPU** | TC-01 |
| Internet | **ON** | to install `requirements.txt` |
| Environment | **Python 3.11** (the governed pin, TC-03d) — this is a DIFFERENT environment from Session A's 3.10 | do not run this gate under the B-01 leg's 3.10 env |
| Dataset | the refreshed dataset | no other attachment |

`requirements.txt` pins the governed set exactly (`numpy==1.26.4`,
`pandas==2.1.4`, `pyyaml==6.0.1`, `scikit-learn==1.4.2`, `tensorflow==2.21.0`,
`matplotlib==3.9.0`, `pyarrow==16.1.0`, `pytest==8.2.2`, `ruff==0.4.8`). If the
Kaggle image is not 3.11, build one and run everything inside it — record the
actual interpreter version either way.

### 3. The command

```bash
export TEC_PLATFORM=kaggle
export CUDA_VISIBLE_DEVICES=""          # TC-01: no GPU visible
export PYTHONHASHSEED=0                 # TE §13.2 determinism
COMMIT=<the exact commit sha the uploaded tree was taken from>

python scripts/gate_in_session.py --config configs/ --phase 1 --code-commit "$COMMIT"
```

### 4. What successful output looks like

The last printed line reads:
```
gate_in_session: accepted on kaggle; N critical module(s), fixtures
{'plumbing_7day': 'passed', 'scientific_1month': 'passed'}; measured total
<seconds> s -> artifacts/walking_skeleton/in_session_gate_result.json
```
Exit code 0. If it prints `gate_in_session: aborted: <reason>` instead, the
reason is stated explicitly — read it before re-running (see troubleshooting
below).

**Note on `scientific_1month`:** as of this writing its own
`fixture_manifest.yaml` is also `status: candidate` (Q-31's scientific-fixture
manifest freeze is a separate, still-owed Student act, distinct from
everything fixed this session). If this session still shows that fixture
failing for that reason, it is a **separate, pre-existing blocker**, not
something Session A or this gate's own fix touches — do not attempt to freeze
that manifest yourself; it is a Student-owned act (TE §18.2, Q-31).

### 5. Where the evidence lands, and how to bring it back

| File | Written to (inside the Kaggle session) | What it evidences |
|---|---|---|
| Critical-set junit | `artifacts/exec_evidence/in-session-gate-<UTC>/junit_in_session.xml` | the critical set ran **in session** (TA-03, TA-26) |
| Both fixture roots | `artifacts/walking_skeleton/plumbing_7day/` and `.../scientific_1month/` | both fixtures ran in session (TE §9.2) |
| The gate result itself | `artifacts/walking_skeleton/in_session_gate_result.json` | **the TC-03g artifact** — platform, environment lock/hash, frozen manifest hashes, per-test and per-fixture results, measured runtime |
| Registry rows | appended to `artifacts/registry/experiment_registry.jsonl` | NFR-AUD-01: every run visible with status and reason, success or failure |
| Environment record | `pip freeze` and `python -V` output, saved as text | the session's actual environment, beside the declared pins |

From Kaggle's Output pane, download `artifacts/exec_evidence/in-session-gate-<UTC>/`,
the two fixture root directories under `artifacts/walking_skeleton/`,
`in_session_gate_result.json`, and the appended registry rows.

### 6. Then, separately, the G-09 preflight report (not part of `gate_in_session.py`)

```bash
python scripts/gate_preflight_report.py --config configs/ --phase 1 \
  --junit artifacts/exec_evidence/in-session-gate-<UTC>/junit_in_session.xml \
  --signoff governance/G09_SUPERVISOR_SIGNOFF_RECORD.yaml \
  --code-commit "$COMMIT" \
  --output /kaggle/working/aws_ai_dlc_preflight_report_kaggle.json
```
Download `aws_ai_dlc_preflight_report_kaggle.json` too.

### 7. What to send back to me (or commit yourself)

All of: the gate's final printed line (success or the exact abort reason),
`in_session_gate_result.json`, the junit XML, the appended registry rows,
`pip freeze` + `python -V` output, and `aws_ai_dlc_preflight_report_kaggle.json`.
Commit them under the paths in the table above with a message citing this
runbook and TC-03g; never delete a row from the registry even if the run
aborted.

### Troubleshooting (Session B)

| Symptom | Likely cause | Fix |
|---|---|---|
| `refusing: resolved platform is 'local'` | `TEC_PLATFORM=kaggle` not set, or set after `load_configs` already ran | Set the env var before invoking the script, in the same shell |
| Aborts at the critical set with named failing module(s) | A real test failure inside the Kaggle environment (different from local — e.g. a pin drift) | Read the failing module list the abort message prints; do not weaken or skip the test to force a pass |
| Aborts on `plumbing_7day` | Session A's B-01 payload was not correctly bridged, or the uploaded dataset is stale | Re-check Session A step 7 passed locally before re-uploading |
| Aborts on `scientific_1month` citing `TBD` fields | Q-31's manifest freeze is not yet done — a separate, pre-existing, Student-owned gap | Report to the Student; do not attempt to fill the sentinel yourself |
| `gate result refused: ...` at the end (critical set and fixtures both passed) | `require_in_session_gate`'s own self-check caught a platform/hash/manifest disagreement (R-141) | Read the exact IntegrityError message — it names which of the three checks failed |
| Second run in the same workspace refuses | The gate result is write-once by design | Move or version the prior `in_session_gate_result.json` before re-running; never overwrite |

### What the session does NOT do

It does not open the locked December set, does not pass G-05 or G-06, and does
not by itself sign G-09 — the preflight report is evidence for that gate, and
the gate is the supervisor's (Vision §13.1). No credential may appear in the
notebook, in any output, or in any registry note (TE §10; NFR-SEC-01): Kaggle
credentials come from Kaggle's own secrets, never from a cell.
