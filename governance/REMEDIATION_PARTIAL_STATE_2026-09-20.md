# Partial remediation state — GOV-2026-09-20-CG-01, interrupted

> **SUPERSEDED 2026-09-20, later the same day.** The four interrupted workers
> were resumed as verify-then-finish agents on disjoint file allowlists and all
> four returned manifests; the itemised closure state now lives in
> `governance/reviews/GOV-2026-09-20-CG-01.md` § Remediation manifest. The
> agent-doable remediation is statically complete; every edit remains
> **unexecuted and unverified** (no interpreter on this clone), the tree is
> still uncommitted at `ff5c683`, and the gate verdict remains `FAIL`. One
> measured correction to this record: the line 50 hedge ("the controls that
> prove these changes correct may be absent or half-written") is false for
> Recommendations 2, 5 and 6 — the controls were complete on disk; three of the
> four dead workers had finished the item their last transcript line named.
> The original text below stands unedited as the record of the interruption.

**Filed:** 2026-09-20
**Status:** ⚠ **INCOMPLETE. The working tree is mid-remediation and unattested. Do not commit it as a finished state.**
**Governance report:** `governance/reviews/GOV-2026-09-20-CG-01.md`
**Owner dispositions:** `governance/CHANGE_RECORD_2026-09-20_GOV-CG-01_dispositions.md`

---

## What happened

Owner-authorised remediation of the sixty findings was executed by five parallel agents, partitioned over disjoint file sets. **One completed and reported. Four were terminated mid-edit by an API session limit** and returned no manifest. Their last observed actions were:

| Worker | Scope | Last observed action | Manifest |
|---|---|---|---|
| Features / leakage guards | `src/features/`, `src/external/spaceweather.py`, new leakage test module | completed normally | **YES — full** |
| Confirmatory path | `src/models/`, `src/data/splits.py`, `scripts/05`, `scripts/06` | "Now the **B** and **C** negative controls and the end-to-end locked-path test" | **NO** |
| Evaluation / reporting | `src/evaluation/`, `scripts/07` | "Now updating the three unit records" | **NO** |
| Data provenance | `src/data/`, `scripts/00`–`04`, legacy scripts | "Now the census, mix-refusal, disclosure and UTC controls appended to `test_december_audit.py`" | **NO** |
| Custody / environment / records | custody tests, fixtures, hooks, pins, notebooks | "Now item J — the stale fixture README clauses" | **NO** |

## Measured state of the tree

Derived by `git status --short` and `git diff --numstat` on 2026-09-20, printed before assertion. **46 files modified, 6 untracked**, approximately **7,000 insertions**.

Largest changes: `scripts/07_evaluate_and_report.py` +653/−4; `src/models/train.py` +592/−11; `tests/test_models_smoke.py` +486/−11; `src/models/climatology.py` +414/−43; `src/evaluation/diagnostics.py` +385/−30; `tests/test_common_masks.py` +389/−4; `tests/test_phase_boundary.py` +348/−20; `src/data/inventory.py` +342/−9; `src/data/release.py` +338/−2; `tests/test_december_audit.py` +340/−2; `src/models/lstm.py` +325/−72; `scripts/06_train_and_predict.py` +331/−41; `scripts/01_inventory_and_registry.py` +316/−11.

New files: `tests/test_feature_leakage_guards.py`, `tests/fixtures/plumbing_7day/fixture_manifest.yaml`, `tests/fixtures/scientific_1month/fixture_manifest.yaml`, `evidence/test_run_access_log.SUPERSEDED_2026-09-20.md`, plus the two governance documents and this file.

## What is CONFIRMED complete

Only the features/leakage worker's output is attested by its own manifest, and only the governance documents were written directly.

- **Recommendation 12** — `tests/test_feature_leakage_guards.py` created: 21 test functions / 25 collected cases, four TA controls (TA-33, TA-34, TA-35, TA-36) each pushed through `build_features`.
- **Recommendation 14** — duplicate-epoch refusal in `_hourly_series`; `assert_identical_across_cells` wired at the post-join boundary; `assert_carry_forward_conservation` wired into `transforms.carry_forward`; boundary split declared in `spaceweather.py`'s docstring.
- **Recommendation 41** — reciprocal D-10.1 boundary split declared in `spaceweather.py` and `availability.py`.
- **Recommendation 17 (first half)** — `window_length_hours: "TBD — freeze gate"` declared in `configs/experiment.yaml`. The `REQUIRED_FIELDS_MAP` half is **deferred to transcription time** by owner ruling, resolving the collision with receipted ruling Q1 = A (`src/data/config.py:613-624`), which states the field is "NOT listed here BY DESIGN" because a blanket preflight entry would bar `scripts/05`'s honest `aborted` registry row.
- **Recommendation 31** — added to `GOV-2026-08-28-FD-01-REMEDIATION-STATUS.md` with its re-derived status; Resume-sequence step 5 marked discharged under Recommendation 4's ruling.
- **Recommendation 39 — the committed identity, done directly 2026-09-20.** `notebooks/madrigal_phase1_coverage_audit.ipynb` cell 2: `USER_FULLNAME` and `USER_EMAIL` replaced with the `REPLACE_ME` sentinel, which the notebook's own pre-existing guard (`if 'REPLACE_ME' in …: raise RuntimeError`) already refuses on — so a run cannot proceed with a placeholder identity and the values must be set locally, never committed back. `USER_AFFILIATION` left in place: it is institutional rather than personal and appears in the header of the Vision document itself. The **historical** breach in git history is untouched and remains an open owner ruling at G-09 (`CR-2026-09-20-GOV-CG-01-DISPOSITIONS` §5 item 12); it is not rewritable without breaking the audit-trail immutability this project affirms. This was taken out of the worker queue and done directly because it was the one item with a live external exposure and no dependency on anything else.
- The three governance documents.

### One new defect found during remediation, beyond the sixty

**Leakage-class, caught by the features worker while writing TA-33's control.** `src/features/build.py::_assert_field_name_clean` refused only a name beginning `iri_` or carrying a bare `iri` token. This project's own canonical IRI field name, `iri2016_t_plus_1_tecu` (TE §6.2 row identity; `configs/experiment.yaml:318` `benchmark_b01.output_field`), tokenises to `{iri2016, t, plus, 1, tecu}` and matched **neither limb**. Declared on the `target_support` row — the one branch of `_assert_name_matches_row` that imposes no name/row agreement — it reached the feature dictionary intact and, with a valid pre-freeze approval, would have entered the model input set. WS-10's existing injection control uses `iri_vtec` and could not have found it. The filter is now widened to any name token beginning `iri`; it cannot over-match, because the closed §6.2 table bounds legitimate field names and none begins `iri`. **This warrants its own D-number and a note against NFR-IRI-01 / TA-07.**

## What is PARTIAL or UNKNOWN

Edits exist on disk for these, from workers that never reported. **Every one must be read and verified before it is relied on.**

- Recommendations 2, 5, 6 (M-03 key, refit epoch rule, guarded `05 --partition DEC`) — `climatology.py`, `lstm.py`, `train.py`, `scripts/05`, `scripts/06` all heavily modified; the worker died while writing the negative controls and the end-to-end locked-path test, so **the controls that prove these changes correct may be absent or half-written**.
- Recommendations 15, 16, 18, 19, 20, 21, 48 — `src/evaluation/*` and `scripts/07` heavily modified; the worker died before updating any of the three owning unit records.
- Recommendations 8, 22, 23, 24, 25, 26, 43, 46, 49, 51 — `src/data/*`, `scripts/00`, `scripts/01`, `merge_coverage_year.py`, `audit_ec1_drivers.py` modified; the worker died mid-append to `tests/test_december_audit.py`.
- Recommendations 1, 32, 37, 45, 50 — `.gitignore`, `locked_test.py`, `test_release_hashes.py`, `test_acquisition_window.py`, `test_phase_boundary.py`, the two fixture manifests and the superseded-log notice landed; the worker died during the fixture-README sweep.

## What is CONFIRMED NOT STARTED

Derived by absence from `git status`:

- **Recommendation 42** — `models-and-baselines/code-summary.md` unmodified; the stale TensorFlow claims stand.
- Three evaluation-side unit records (`evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`) unmodified.
- **Recommendation 45 (half)** — `tests/fixtures/scientific_1month/README.md` unmodified; only the plumbing README was swept.
- **Recommendation 38** — `requirements.txt` unmodified; `matplotlib` still unpinned.
- **Recommendations 30, 35** — `.githooks/pre-commit` unmodified; restricted cases not deselected, hook still uninstalled.
- **Recommendation 44** — no `REPRODUCTION.md`; `README.md` unmodified.
- **Recommendation 47** — `.github/workflows/verify.yml` unmodified.
- **Recommendations 28 (notebook half), 58** — `kaggle/` notebooks and `src/data/fixture_evidence.py` unmodified.
- **Recommendations 3, 4, 7, 9, 10, 11, 13, 27, 33, 34, 36, 40, 52, 53, 54, 55, 56, 57, 59, 60** — owner acts, records, or not reached.

## Verification status — read this before relying on anything above

- **No test, stage script or notebook cell was executed at any point**, by any seat or any worker. No usable Python interpreter exists on this clone; `python.exe` resolves to a zero-byte Windows Store alias stub. **Every change on disk is unexecuted and unverified.**
- **No git command that changes state was run.** No commit, add, amend, rebase, or `core.hooksPath` change. `HEAD` remains `ff5c683`.
- **No row of `evidence/test_run_access_log.jsonl` or `artifacts/registry/experiment_registry.jsonl` was modified, rewritten, truncated or deleted.**
- **No December 2022 target value was read**, by any seat or worker.
- **Nothing was written to `evidence/DECISIONS.md`.** Five decisions are drafted in the dispositions record §4 for the owner to adopt; a sixth is now owed for the `iri2016_*` filter widening.
- **No `PreFlight/` authority document was edited.**
- **No scientific value was invented.** Where a value is owed, the literal `TBD — freeze gate` sentinel was written.

## Recommended next steps

1. **Do not commit the tree as a finished remediation.** It is mid-edit in at least four places.
2. Resume the four interrupted workers after the session limit resets, each re-scoped to verify what its predecessor left and finish the remainder. The completed-vs-partial split above is the resume brief.
3. Before any commit, run `ruff check` and the full suite **in the governed environment** — the first execution any of this code will have had.
4. Recommendation 39 (the committed personal email) is the one item here with a live external exposure and no dependency on anything else. It is a two-minute fix and should not wait for a resumed worker.
5. Then produce the remediation manifest owed to `governance/reviews/GOV-2026-09-20-CG-01.md` § Remediation manifest, which is currently unwritten.

**The gate verdict is unchanged: `FAIL`.** Nothing in this partial state advances it.
