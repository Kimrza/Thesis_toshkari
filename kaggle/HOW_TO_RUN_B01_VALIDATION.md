# How to run the B-01 validation session on Kaggle — step by step

**Status of the local half: DONE.** `case_5_BSHM_20220804T12Z.txt` was collected on
2026-09-22; its server-echoed header reads `2022/ -216/12.0UT  geog Lat/Long/Alt= 32.8/
35.0/ 300.0`, which is day-of-year 216 = 4 August 2022 at **12 UT** at BSHM — the case §4
of the collection sheet specifies. `kaggle/official_reference_outputs/parse_official_outputs.py`
then matched **8 of 8** cases by header (never by filename) and wrote
`kaggle/b01_validation_samples.json`. The eight official IRI-2016 reference values are:

| # | Site | Target time (UT) | Class | Official TEC (TECU) | t/% | hmF2 (km) |
|---|---|---|---|---|---|---|
| 1 | ARUC | 2022-01-07 12:00 | day, quiet | **12.1** | 76 | 227.03 |
| 2 | ARUC | 2022-01-07 00:00 | night, quiet | **4.0** | 76 | 292.54 |
| 3 | ARUC | 2022-03-13 22:00 | night, disturbed | **4.6** | 76 | 327.50 |
| 4 | BSHM | 2022-09-04 10:00 | day, disturbed | **33.1** | 67 | 296.62 |
| 5 | BSHM | 2022-08-04 12:00 | day, quiet | **29.2** | 68 | 283.94 |
| 6 | NICO | 2022-09-04 22:00 | night, disturbed | **8.5** | 75 | 341.94 |
| 7 | NICO | 2022-11-17 02:00 | night, quiet | **4.1** | 75 | 278.26 |
| 8 | NICO | 2022-04-14 16:00 | day, disturbed | **21.7** | 75 | 279.95 |

No December case; the selection was frozen 2026-09-19T20:28:42Z, **before** any retrieval,
and no case was replaced after a discrepancy was seen.

**What is left is a Kaggle session**, because `iricore` cannot be installed on the local
Windows machine and the adapter's own values for these eight cases do not exist yet.

---

## Step 0 — the predeclared tolerance: ALREADY FROZEN, verify and move on

*(Corrected 2026-09-22 before this file was first used: an earlier draft of this step said
the tolerance still had to be written. Measured against the config, it does not.)*

`configs/experiment.yaml: benchmark_b01.validation_report` already carries
`tolerance_tecu: 1.0` (D-50, student-approved) and
`tolerance_declared_at_utc: "2026-09-20T12:27:01Z"`. R-59 limb 2 requires the declaration to
**precede** the comparison, and 2026-09-20 precedes any session you run now, so the ordering
holds. Nothing is owed here — just confirm both lines are present and unchanged before you
start, because `src/external/iri.py: build_validation_report` refuses if either reverts to
`TBD — freeze gate`.

**Do not look at any adapter value for these eight cases outside the report builder.** The
collection sheet §8 says so and TE §18.2 makes it binding: a tolerance is not a tolerance if
it is chosen after seeing the result. The tolerance is frozen; keep it that way.

**Carry this open risk into the session knowingly.**
`governance/proposed/B01_TOLERANCE_PROPOSAL_2026-09-19.md:50` measured a CCMC quadrature
offset that scales to **≈ −1.3 TECU at 50 TECU**. Cases 4 (33.1 TECU) and 5 (29.2 TECU) are
the high-TEC cases, so some may exceed the frozen 1.0 TECU. **If that happens the answer is
not to widen the tolerance** — it is §7 of the collection sheet: the legacy CCMC form, or a
compiled official IRI-2016 reference build run with the pinned index files, each recorded
with its own provenance. That is a Student + Supervisor decision, not an implementation one.

---

## Step 1 — build the upload package

Locally:

```bash
python kaggle/build_b01_package.py
```

This rebuilds `kaggle/dist/tec_b01_package.zip` from the current tree, including
`b01_validation_samples.json`. Check the script's output names the eight filled cases.

---

## Step 2 — create the Kaggle notebook

* **New Notebook** → attach `kaggle/dist/tec_b01_package.zip` as a **private dataset**
  (or upload the repository tree as a private dataset — either works; the package is
  smaller).
* **Accelerator: None / CPU.** TC-01: CPU is a complete execution path, and a GPU result is
  not the governed one.
* **Internet: ON.** Needed to install `iricore` and the pinned dependencies.
* **Do not attach, upload or reference `evidence/locked_test_restricted/`.** The locked
  December root never leaves the governed machine.

---

## Step 3 — the environment

D-49 records the exception under which the B-01 benchmark runs in a **Python 3.10** venv
(`iricore` has no 3.11 wheel path that installs in this environment), while the main
governed pin stays 3.11 (TC-03d). The Kaggle notebook
`kaggle/kaggle_iri2016_benchmark.ipynb` already builds that venv — revision 4 also runs the
whole test suite inside it before any stage runs, so a language-level incompatibility stops
the session with junit counts instead of a stage traceback.

Verify in the notebook's own output, before trusting anything downstream:

* `iricore==1.8.0`, wheel sha256 `f452b22316891d87ee766dba266de6a07e4e6008ab515ffed902ea8b5446a874`;
* index files `apf107.dat` sha256 `cdf4d5df…` and `ig_rz.dat` sha256 `fbbed304…` — the
  **pinned** files D-45 names. If either hash differs, **stop**: the comparison would be
  against different index inputs and the disagreement would be uninterpretable.

---

## Step 4 — run the adapter over the eight cases and emit the R-59 report

Inside the 3.10 venv, from the repository root:

```bash
export CUDA_VISIBLE_DEVICES=""
export PYTHONHASHSEED=0
export TEC_PLATFORM=kaggle
COMMIT=<the commit the uploaded tree was taken from>

# 4a. runtime identity: which wheel, which index files, hashed
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --code-commit "$COMMIT" --verify-runtime

# 4b. the paired comparison against the eight official values, and the R-59 report
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --code-commit "$COMMIT" \
  --build-validation-report \
  --validation-report artifacts/external/b01/iri_implementation_validation_report.json
```

Step 4b is the paired comparison: for each of the eight cases it computes the adapter's
TEC at the same station coordinates, the same UT instant, the same 90–2000 km integration
bounds, and compares against `official_interface_value` at the **declared** tolerance. The
report records per-case adapter value, official value, difference, and pass/fail, plus the
declaration instant that must precede the comparison.

**Read the report, don't skim the exit code.** R-59 limb 1 wants *a passing pre-declared
validation report*; 8/8 PASS at 1.0 TECU is the closure evidence Recommendation 10 names.
Anything less is a result to bring back, not to fix in place.

---

## Step 5 — only if 4b passed: generate the benchmark

```bash
python scripts/04_build_external_products.py --config configs/ --phase 1 \
  --code-commit "$COMMIT" \
  --generate-benchmark \
  --validation-report artifacts/external/b01/iri_implementation_validation_report.json \
  --months 1 2 3
```

`--generate-benchmark` refuses without a passing report (`src/external/iri.py`, R-59 limb 1),
so this step is self-gating. Start with a few months to measure the per-call cost before
committing a session to the whole year.

---

## Step 6 — the in-session gate, in the same session

While you are there, discharge **TC-03g** — the critical set and both fixtures inside the
Kaggle session (`kaggle/HOW_TO_RUN_IN_SESSION_GATE.md`, and now with a production caller):

```bash
python scripts/gate_in_session.py --config configs/ --phase 1 --code-commit "$COMMIT"
```

It refuses immediately unless `TEC_PLATFORM=kaggle`, runs the critical set, then both
fixtures in order, emits `artifacts/walking_skeleton/in_session_gate_result.json` and
judges it against this session's own lock. **Note:** it will currently stop at the fixture
step, because the fixture ladder does not yet complete end to end — see the ladder status in
`governance/CHANGE_RECORD_2026-09-21_gov_cg01_closure_pass.md`'s addendum. Run it anyway if
you want the refusal recorded honestly; run it *for real* once the ladder completes.

---

## Step 7 — what to bring back

Download from the Output pane and commit:

| File | Goes to |
|---|---|
| `iri_implementation_validation_report.json` | `artifacts/external/b01/` |
| `b01_runtime_identity.json` | `artifacts/external/b01/` |
| `b01_iri2016_rows.jsonl` + `b01_provenance.json` (only if step 5 ran) | `artifacts/external/b01/` |
| the notebook's full console log | `artifacts/exec_evidence/run_<UTC>/` |
| `pip freeze`, `python -V` from the 3.10 venv | `artifacts/exec_evidence/run_<UTC>/` |
| the appended experiment-registry rows | merge append-only into `artifacts/registry/experiment_registry.jsonl` |

Then tell me, and I will write the change record and the D-number draft for the validation
outcome — including, if any case failed, the §7 fallback as an owner decision rather than a
tolerance change.

---

## What this session does NOT do

It does not pass **G-04** — that is a supervisor gate, and this produces its evidence. It
does not touch December, does not open the locked test, and does not compute any model
result. No credential appears in any cell, output or registry note (TE §10; NFR-SEC-01):
Kaggle credentials come from Kaggle's own secret store.
