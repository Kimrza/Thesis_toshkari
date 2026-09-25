# Build and Test Summary

**Stage:** build-and-test (3.6) · **Lead:** aidlc-quality-agent ·
**Support:** aidlc-devsecops-agent
**Date:** 2026-09-24 · **Repository commit:** `41fd109`
**Test strategy:** Comprehensive

## Overall build status

| Aspect | Status |
|---|---|
| Governed interpreter (CPython 3.11 exact) | ✅ Rebuilt this session (3.11.16, conda-forge) |
| Pin surface | ⚠ Partial: 7 of 9 pinned packages exact; `matplotlib==3.9.0` and `tensorflow==2.21.0` unobtainable from reachable channels (PyPI blocked) — disclosed, not substituted |
| Full test suite (post-remediation, `full_post.xml`) | ⚠ **1581 / 1584 passed, 3 failed, 6 skipped** (junit-derived; the 3 are the site-log custody rows) |
| §18.3 critical set (ten-module selection) | ⚠ 677 / 683 passed — the same 3 failures, all in `test_release_hashes.py` |
| Remaining failures | All three are ONE finding: IGS site logs declared in a committed manifest but never committed (swallowed by the generic `*.log` ignore) — ruled option 1 (re-retrieve + verify + commit); retrieval blocked from this network, never-again mechanism already in place |
| Fixture ladder | Stages 00, 01, 02, 04, 05 complete on `plumbing_7day`; 06/07 not yet run; `scientific_1month` window still an open Q-31 freeze |
| Lint (`ruff check .`) | 63 pre-existing findings tree-wide (advisory; no enforced floor) |

## Test type inventory (what this stage generated)

| Artifact | Contents |
|---|---|
| `build-instructions.md` | Environment reconstruction as the build; 2026-09-24 addendum with the measured conda-forge recipe and the two unobtainable pins |
| `unit-test-instructions.md` | pytest under the governed env; 29 on-disk modules vs the 21-module §12 mandated set; per-module function counts; negative-control-per-rule methodology; no enforced coverage floor (Q5=A) |
| `integration-test-instructions.md` | The fixture ladder as the real integration tier; cross-unit boundary module map; measured ladder state; known blockers |
| `performance-test-instructions.md` | Measured-then-frozen runtime envelopes (TE §15.1/§15.2); CPU completeness (TC-01); determinism checks; explicit non-goals |
| `security-test-instructions.md` | Secret scanning (gitleaks, deny-list, hook); locked-test custody; prohibited-flow negative controls; release integrity; §10.1 reuse governance |
| `build-test-results.md` | Executed results: both suite runs with junit-derived counts, the D-68 pin repair, the site-log custody finding with three proposed dispositions |

## Coverage expectations per unit

No numeric floor is enforced (team.md, Q5=A; `targets` deliberately unset —
the sensor's line 80 / branch 70 defaults are advisory reporting only). The
real bar per unit is its named tests passing plus the §16/§19 pass/fail rows:
Phase 1's acceptance set is **WS-01 plus WS-09–WS-20** (team.md
§ Corrections) and the test-bearing TA rows TA-07–TA-09, TA-11–TA-14, TA-17,
TA-18, TA-22, TA-23, TA-26, TA-27. Per-module function counts are tabulated
in `unit-test-instructions.md`.

## Readiness assessment

- **Build-ready:** yes, with the disclosed partial pin surface. A fresh
  session can rebuild the environment from the recorded recipe without PyPI.
- **Test-ready:** yes — the suite runs end-to-end in 145 s on CPU; every red
  row is root-caused and owner-routed.
- **Deployment-ready** ("deployment" = dataset/model releases here): **no** —
  blocked on the site-log custody disposition, the open student freeze acts
  (scientific fixture window, fixture tolerances), stages 06/07 of the
  ladder, the TC-03g Kaggle-session run, and the open supervisor gates
  (G-05, G-06, G-07). None of these is this stage's to close.

## Known limitations and outstanding items

*(Renumbered 2026-09-24 after the `GOV-2026-09-24-BT-01` rulings —
`governance/CHANGE_RECORD_2026-09-24_GOV-BT-01_rulings.md` is the execution
record.)*

1. **Site-log custody finding (Rec 1, ruled option 1)** — the never-again
   half is DONE (`.gitignore` negation + the manifest-vs-gitignore control);
   the retrieval half is **blocked from this network** (every GNSS
   data-centre host times out) — the three `test_release_hashes.py` rows stay
   red until a `files.igs.org`-reachable host runs the recorded retrieval
   spec and the verified bytes are committed.
2. **TF and matplotlib absent locally** — M-06 and plots paths unexercised;
   Kaggle (or a PyPI-reachable host) owes the TE §8.1 both-platform check.
3. **WS-20 / TA-17 remain `Pending`** — no full clean-run reproduction yet.
4. **Cross-unit staleness now DISCLOSED in place per `gf-3`** —
   `acquisition` (D-68 pin fix), `governance-guards`, `models-and-baselines`
   and `foundation` (the Rec 8/9/10/16 and Rec 1 amendments) each carry a
   dated addendum in their `code-summary.md`; prior sessions' carried
   staleness stands as recorded in `build-instructions.md`.
5. **`aidlc-state.md` `Project Root`** stale for this clone (second
   recurrence; diary Open questions).
6. **Rec 47 (GitHub Actions on a third platform)** unresolved pending a
   GitHub check; interacts with the tracked `evidence/locked_test_restricted/`
   root (owner ruling open).
7. **The operative §18.3 critical-set selection** (Rec 5) — routed to the
   Student; see `build-test-results.md` § "§18.3 selection reconciliation".
8. **Pre-commit hook now ACTIVE on this clone** (Rec 3, ruled option 2;
   `core.hooksPath=.githooks` set and verified 2026-09-24 this session) —
   commits need the governed environment on `PATH`; procedure in
   `build-instructions.md`.

## 2026-09-25 remediation addendum

*(Full derivation in `build-test-results.md` § "2026-09-25 remediation
addendum"; this section is the summary-level pointer, not a restatement.)*

- **Item 1 (site-log custody) — CLOSED.** All three site logs recovered,
  hash-verified, committed, `.gitignore` negation live,
  `test_release_hashes.py` 235/235. This was the only condition this stage's
  prior CONDITIONAL PASS named by number; it no longer holds the verdict
  down on its own.
- **Item 2 (TF/matplotlib absent) — CLOSED locally.** Both now installed at
  exact governed versions in `tec-thesis-311`; pin surface 9/9. The Kaggle
  both-platform check is still owed and is not this addendum's to close.
- **Item 3 (WS-20/TA-17 clean-run) — still Pending**, confirmed by a fresh
  `test_clean_run.py` skip naming the same unmet precondition
  (scientific-fixture manifest still `TBD — freeze gate`).
- **Item 6 (Rec 47 GitHub check) — investigated, not closed.** The workflow
  IS live on GitHub (49 runs); its latest run, at a commit two behind this
  session's HEAD, failed on the exact site-log defect fixed above. No run
  exists yet against the fix. Closing this needs a push, which this
  session is not authorized to do.
- **Item 8 (pre-commit hook) — reconfirmed active**, unchanged.
- Fresh full-suite counts: **1584 total, 1580 passed, 0 failed, 0 errors, 4
  skipped** (`full.xml`, 424.5 s). Fresh §18.3 ten-module selection (b):
  **685/685 passed, 0 failed, 0 skipped** (`crit.xml`, 55.8 s).
- **Overall verdict: still CONDITIONAL PASS**, not upgraded to PASS — the
  remaining open conditions (items 3, 4, 5, 6, 7 above) are unresolved by
  this addendum and several are external to this stage (Student freeze
  acts, a push, the Kaggle run). Reliance on this stage's evidence at a
  freeze gate remains prohibited until those close.

## Sources

- Per-unit `code-generation-plan.md` and `code-summary.md` under
  `<record>/construction/<unit>/code-generation/` — this stage's consumed
  inputs across all twelve units.
- `build-test-results.md` (this stage) for every measured number above.
- TE §8.1, §9.1–9.2, §13.1–13.2, §15, §18.3; team.md § Testing Posture,
  § Walking Skeleton, § Deployment, § Corrections; project.md § Mandated,
  § Forbidden.
- `governance/PENDING_FOLLOWUPS.md`, `governance/REC_13_60_STATUS_2026-09-24.md`,
  `governance/RULING_REQUEST_2026-09-23_CONSTRUCTION_STOPS.md`.
