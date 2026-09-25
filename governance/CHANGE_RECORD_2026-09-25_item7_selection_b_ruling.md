# Change Record — Item 7 (§18.3 selection reconciliation) ruling execution

**Date:** 2026-09-25
**Owner instruction:** Student, verbatim (session message, 2026-09-25): "I approve
selection (b) — the ten-module §18.3 selection (685/685, `crit.xml`) — as the
authoritative 'critical set' for §18.3's gate criterion... update
`evidence/DECISIONS.md`... noting that selection (b) is designated authoritative,
with (a) and (c) explicitly superseded/not applicable for this gate."

## Background

`build-and-test`'s `build-test-results.md` § "§18.3 selection reconciliation" (Rec 5,
ruled option 1) identified three coexisting "critical set" selections that must not be
conflated:

- **(a)** the pre-commit hook's five-module commit-time subset (Rec 30 option 1;
  restricted readers deselected — a subset by design, never a candidate for "the"
  §18.3 run).
- **(b)** the ten-module §18.3 selection — the module homes of §18.3's ten named
  critical items (DCB-sign has no Phase 1 module by design): `test_prepared_target_schema`,
  `test_feature_availability`, `test_iri_denial`, `test_split_embargo`,
  `test_train_only_transforms`, `test_common_masks`, `test_checkpoint_restore`,
  `test_bootstrap`, `test_release_hashes`, `test_locked_test_guard`.
- **(c)** the 766-test selection behind `governance/PENDING_FOLLOWUPS.md` §1a's
  "766/766 passed" — spans all 29 test modules, no surviving junit evidence at green
  (the only committed 766-test XML records 2 failures), and was run while the three
  site-log bytes were already absent from tracking.

## Ruling executed

Selection **(b)** is designated the authoritative "critical set" for §18.3's "zero
unresolved P0 fields and no failing critical test" gate criterion, on the following
basis, per the Student's instruction:

- (b) is the only selection whose ten module homes map 1:1 onto §18.3's ten named
  critical items (target contract and DCB sign; availability lags; IRI-free denial;
  split embargo; train-only transforms; comparison-wide masks and matched windows;
  checkpoint restore; vector bootstrap; release hashes; locked-test access guard).
- (a) is explicitly a commit-time subset by design (Rec 30 option 1), never intended
  to stand alone as the full critical set.
- (c) has no surviving green junit evidence and was run against a since-corrected
  evidence-custody defect (the site logs it implicitly excluded or ran without).

**(a) and (c) are superseded / not applicable for the §18.3 gate criterion** — this
does not retract either as a historical record; the 766-test run and the hook subset
stand as their own dated evidence for what they were, per `project.md`'s never-edit-a-
signed-record correction.

## Verification — fresh run, this session

Re-ran selection (b) fresh (not reused from the 2026-09-24 `crit.xml`), governed env
`tec-thesis-311` (Python 3.11.16), `PYTHONHASHSEED=0`:

**685 total, 685 passed, 0 failed, 0 errors, 0 skipped**, 54.870 s wall time.
Persisted: `artifacts/exec_evidence/run_2026-09-25_item7_selection_b/crit.xml`
(sha256 `005fdb00a282e9c57c8007a0a18b71d324c81e3143b3019c9ea5d2b5a85b16a3`).
Matches the prior 2026-09-24 `crit.xml` figure (685/685) — no regression across the
one-day gap.

## Disposition

§18.3's "no failing critical test" precondition is **satisfied** for the now-
authoritative selection (b), verified fresh this session. Recorded as `D-69` in
`evidence/DECISIONS.md`.
