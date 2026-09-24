# Pending Follow-Ups (not yet due, do not action until triggered)

## 1a. Layer-1 §7 — chokepoint scanner self-exemption — CLOSED 2026-09-24
Resolved via the project's own established "post-receipt amendment" pattern
(`project.md` `code-generation:gf-3`) rather than an `aidlc-jump` redo — no
workflow-wide reset was needed or performed. `tests/test_release_hashes.py`
(`foundation`) and `tests/test_phase_boundary.py` (`governance-guards`) both
fixed; both units' READY receipts stand as history with the fix appended and
disclosed below them. Full §18.3 critical test set: **766/766 passed** under
the governed `tec-thesis-311` environment — the first fully green run in this
thread. `test_locked_test_guard.py`'s previously-reported orphan issue also no
longer reproduces (unattributed, just observed). No further action needed.

## 1b. D-28 option (b) bounded 1-December read — CLOSED 2026-09-24, ruled as D-68 and wired
Built, tested (6 tests, all 5 conditions independently verified) and disclosed in
`governance-guards`' code-summary via the same post-receipt amendment pattern.
Ruled as **D-68** the same day (Student instruction, no separate supervisor
signature claimed) — `configs/experiment.yaml: persistence_history_lookup` now
`authorized: true`, `decision: "D-68"`. **Also connected to the live prediction
path** the same day (explicit Student authorization): `scripts/06_train_and_predict.py`
(`models-and-baselines`) now calls the mechanism for M-01/M-02 during the DEC
iteration, with its own dedicated wiring test. Full history:
`governance/CHANGE_RECORD_2026-09-24_d28_option_a_mechanism_built.md` (mechanism)
and `governance/CHANGE_RECORD_2026-09-24_d28_option_a_wiring.md` (wiring). No
further action needed.

## 2. GitHub Actions push/execution status (Rec 47)
Trigger: the next time network/GitHub access is available in a session, or the
Student explicitly asks about CI/workflow status.
Action needed: check whether `.github/workflows/verify.yml` has actually been
pushed to github.com/Kimrza/Thesis_toshkari and is executing there (local git
history alone cannot confirm this — requires an actual check of the remote/Actions
tab). This was flagged as OPEN-NEEDS-INVESTIGATION and not previously on anyone's
radar in this governance thread as of 2026-09-24.

## 3. D-28/D-59 conflict — RESOLVED 2026-09-24 (kept here as closed history)
The D-28 29-day amendment was reverted the same day it was drafted (conflicted with
D-59, no working code path). Final disposition: **option (b)** — D-28 stays at its
original 30 days, D-59 is untouched, and the true fix is D-68's bounded 1-December
lookup read for M-01/M-02 only — now built, ruled and wired (see item 1b above).
Full history: `governance/CHANGE_RECORD_2026-09-24_d28_29day_amendment.md` (the
reverted amendment). No further action needed on D-28/D-59 themselves — both
stand as originally frozen. This entry stays here only so a future reader doesn't
have to reconstruct the history from chat.

## 4. `budget_value` combination rule — CLOSED 2026-09-24, ruled as D-67
A Consensus literature search (GUM/metrology combination-rule theory + GNSS/TEC
differential-code-bias shared-systematic-error evidence) grounded a proposal for
both open fields, which the Student approved and ruled as **D-67**
(`evidence/DECISIONS.md`, no separate supervisor signature claimed):
`statistic: p95`, `combination: sum`. `configs/data.yaml:
target.uncertainty_budget.decision = "D-67"` — `resolve_budget_rule` now returns
a usable rule for the first time. Full history:
`governance/CHANGE_RECORD_2026-09-24_budget_value_merged.md` (superseding the two
earlier single-field drafts). No further action needed.
