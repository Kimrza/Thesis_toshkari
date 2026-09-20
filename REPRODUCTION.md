# REPRODUCTION.md — the TE §13.2 ordered clean-run contract

**Purpose.** The single on-disk reproduction guide this project's governing document requires.
`PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §13.2:763 states "The
reproduction guide **must provide** one ordered sequence." Until 2026-09-20 no such file
existed, so a reproducer had to read the Technical Environment or a source constant
(`GOV-2026-09-20-CG-01` Recommendation 44). This is that file.

**Inputs.** `configs/` (the four governed configuration files), `requirements.txt` (the pin
surface), a clean Python 3.11 environment. **Re-run behaviour:** the whole sequence is
re-runnable from a clean checkout and must complete on CPU; nothing here is stateful.

**Status.** ⚠ This guide is the CONTRACT, not a record of a passing run. Neither
walking-skeleton fixture has ever run, no measured value exists, and **no claim on this page
has been executed**. WS-20 and TA-17 stay `Pending` until a governed run produces the
clean-run log.

---

## 0. Before anything

| Requirement | Value | Authority |
|---|---|---|
| Interpreter | **Python 3.11**, exact | TE §8.1; TS-01 / TC-03d |
| Compute | **CPU is a complete execution path**, never an emergency mode. GPU is an optional accelerator and never a dependency of any result | Vision §9.2; TE §9.2; TC-01 |
| Platforms | **Exactly two** — Kaggle (primary compute, Phase 1 acquisition/audit host) and local (development, small tests, fixture runs, review). No third platform is authorised | TC-03c; TE §9.1 |
| Dependencies | `pip install -r requirements.txt`. One required package, `matplotlib`, is **not yet pinned** — its version is a Student act owed before G-07; see the block in `requirements.txt` | TE §8.1, §13.1; Rec 38 |

```bash
python --version          # must report 3.11.x
pip install -r requirements.txt
```

---

## 1. The ordered sequence

Reproduced **verbatim** from TE §13.2:765-789. Do not re-order, re-flag or re-number these
lines: `tests/test_clean_run.py` parses this fence, the TE fence and
`scripts/run_walking_skeleton.py`'s `PHASE1_SEQUENCE` and asserts all three agree on
membership, order and flags. A drift here fails that test rather than silently misleading a
reproducer.

`export PYTHONHASHSEED=0` is **part of the contract**, not a convenience. It is set once
before the first command and holds for the whole sequence (TE §13.2's `PYTHONHASHSEED`
amendment, `CR-2026-08-22-TE-AMEND`, ADR-10). Omitting it is the single most likely way for
an external reproducer to report a determinism failure that is a documentation gap rather
than a code defect.

```bash
export PYTHONHASHSEED=0        # required; set before any command below
python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day
python scripts/run_walking_skeleton.py --config configs/ --fixture scientific_1month

# Phase 1 acquisition, only after D-144 and source settings are frozen:
# run notebooks/00_acquire_phase1_vtec.ipynb in Kaggle with Internet enabled.
# The equivalent reusable automation companion is:
python scripts/00_acquire_prepared_vtec.py        --config configs/
python scripts/01_inventory_and_registry.py       --config configs/ --phase 1
python scripts/02_standardize_prepared_target.py  --config configs/
python scripts/04_build_external_products.py      --config configs/ --phase 1
python scripts/05_build_features_and_splits.py    --config configs/ --phase 1
python scripts/06_train_and_predict.py            --config configs/ --phase 1
python scripts/07_evaluate_and_report.py          --config configs/ --phase 1

# Phase 2, only after G-P2
python scripts/01_inventory_and_registry.py       --config configs/ --phase 2
python scripts/02_build_vtec_target.py            --config configs/
python scripts/03_verify_processing.py            --config configs/
python scripts/04_build_external_products.py      --config configs/ --phase 2
python scripts/05_build_features_and_splits.py    --config configs/ --phase 2
python scripts/06_train_and_predict.py            --config configs/ --phase 2
python scripts/07_evaluate_and_report.py          --config configs/ --phase 2
```

**Both fixtures must pass, in order, before full execution**, and the whole sequence must
complete on CPU (TE §13.2:791; §9.2; TC-03f).

---

## 2. What the ordering rules actually forbid

- **Fixture ordering is hard, not advisory.** The seven-day single-station plumbing fixture
  runs first, then the one-month all-station scientific fixture, then any full-year job
  (TE §9.2; TC-03f). The plumbing fixture is a **smoke test and never scientific evidence** —
  it may not be cited, plotted as a result, or interpreted as skill.
- **The Phase 2 block does not run in Phase 1.** `scripts/02_build_vtec_target.py` and
  `scripts/03_verify_processing.py` are Phase 2 only and are actively refused on a Phase 1
  invocation (`run_walking_skeleton.py`'s `assert_phase1_invocation`, raising
  `PhaseBoundaryError`). RINEX parsing, DCB handling, STEC calculation and mapping are inside
  TE §7.0's Phase 1 hard prohibition.
- **Script ordinals are phase-scoped.** Two distinct scripts carry `02`. That is correct and
  documented at TE §13.2:795, not a numbering defect. `scripts/` holds 8 numbered scripts
  against §13.2's "nine phase-aware stages"; the ninth is the Phase-2-only
  `02_build_vtec_target.py`, correctly absent from the Phase 1 path.

---

## 3. Running on Kaggle

A Kaggle session carries **no git working tree**, so the local pre-commit hook cannot fire
there and a local suite run proves nothing about the environment a governed run actually
executes in. TC-03g (binding: hard) therefore requires, **inside the Kaggle session and
before any governed run executed there**:

1. the critical test set;
2. **both** walking-skeleton fixtures, in order;
3. the gate result emitted via `src.data.fixture_gate.emit_in_session_gate_result`, with the
   platform taken from `ConfigSnapshot` rather than asserted.

The result is captured in that run's evidence record (TA-03, TA-26). Running the in-Kaggle
session is a **Student act** — `CR-2026-09-20-GOV-CG-01-DISPOSITIONS` §5 item 10 — and no
agent performs it.

---

## 4. Running the tests locally

```bash
export PYTHONHASHSEED=0
python -m pytest tests/
```

Two things a reproducer should know before reading a result:

- **The commit-time set is deliberately narrower than the full set.** `.githooks/pre-commit`
  deselects `tests/test_release_hashes.py`, `tests/test_acquisition_window.py` and
  `tests/test_phase_boundary.py` because each reads December restricted content, and a
  boundary crossed as a side effect of `git commit` is not a governed access (Vision §8.3;
  Recommendation 30). Those three run in the gate/freeze suite, where an authorization exists
  to be recorded. Enabling the hook at all (`git config core.hooksPath .githooks`) is a
  Student act, §5 item 4.
- **Restricted reads write an access row.** A full-suite run under the real evidence tree
  appends `AccessRecord` rows to `artifacts/exec_evidence/test_access_log.jsonl` — a
  gitignored **test-mode** sidecar. `evidence/test_run_access_log.jsonl` is reserved for
  real, governed accesses and is **closed to further appends**; its 5,964 historical rows
  stand unedited under `evidence/test_run_access_log.SUPERSEDED_2026-09-20.md`
  (Recommendation 1). Records are superseded, never rewritten and never deleted.

---

## 5. What reproduction does NOT include

- **The locked December 2022 test set is not opened by this sequence.** It is opened exactly
  once, for the one-shot performance evaluation, hash-before-metrics, after **G-05** is
  signed (gate G-06). That is distinct from — and does not forbid — the **required**
  performance-blind pre-G-05 December coverage and regime audit. Every access is recorded in
  the experiment registry with `locked_test_accessed = true`.
- **No measured fixture value exists to compare against.** Both
  `tests/fixtures/*/fixture_manifest.yaml` files are `status: candidate` skeletons whose
  every measured field is the literal `TBD — freeze gate`, with no `measuring_run_id` — which
  is exactly what makes `load_fixture_manifest` refuse them by name. Populating them from a
  real run under the governed **Python 3.11** pin is a Student act, §5 item 8, owed before
  G-07. The Python 3.10 environment is for the isolated B-01 benchmark **only**; the D-49
  register row at `evidence/DECISIONS.md:3056` stands as written.
- **A clean run FAILS when a value exceeds its declared tolerance** and must never silently
  update the expected value (TE §13.7; NFR-REP-01).

---

## 6. Provenance caveat carried by every figure this pipeline reports

`evidence/locked_test_restricted/audit_evidence_2022-FULL/` rests on twelve monthly runs
whose provenance is **unverifiable in principle, not merely unverified**: no provider byte
stream exists anywhere in the workspace, and three of the twelve months (2022-04, 2022-07 and
2022-12, the locked month) hold no `raw_isprint_cache/` at all (DATA-07). Any artifact relying
on FULL's coverage figures states this, and FULL must not be relied on at a freeze gate while
its provenance chain points at superseded per-month hashes.

---

## Sources

- `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §8.1, §9.1, §9.2,
  §13.1, §13.2 (the fence, verbatim, lines 765-789), §13.7, §7.0, §15.1.
- `scripts/run_walking_skeleton.py` — `PHASE1_SEQUENCE`, `PHASE2_ONLY_SCRIPTS`,
  `assert_phase1_invocation`.
- `tests/test_clean_run.py` — the fence parser and the three-way comparison that binds this
  file to the other two.
- `governance/reviews/GOV-2026-09-20-CG-01.md` Recommendations 1, 30, 37, 38, 44.
- `governance/CHANGE_RECORD_2026-09-20_GOV-CG-01_dispositions.md` §5 items 4, 8, 9, 10, 15.
- `aidlc/spaces/default/memory/team.md` § Walking Skeleton, § Testing Posture, § Deployment.
