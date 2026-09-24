# Pending Follow-Ups (not yet due, do not action until triggered)

## 1. Layer-1 §7 — chokepoint scanner self-exemption
Trigger: the next time an `/aidlc` command is run in this repo (any AI-DLC stage
command, not just this specific one).
Action needed: remind the Student that `test_phase_boundary.py` and
`test_release_hashes.py`'s self-reference false-positive fix requires an AI-DLC
stage redo for the `governance-guards` and `foundation` units (both currently
READY-frozen), not a simple edit. See CHANGE_RECORD_2026-09-24 thread for full
context. Ask the Student whether to route this now as part of whatever /aidlc
command was just run, or continue deferring.

## 2. GitHub Actions push/execution status (Rec 47)
Trigger: the next time network/GitHub access is available in a session, or the
Student explicitly asks about CI/workflow status.
Action needed: check whether `.github/workflows/verify.yml` has actually been
pushed to github.com/Kimrza/Thesis_toshkari and is executing there (local git
history alone cannot confirm this — requires an actual check of the remote/Actions
tab). This was flagged as OPEN-NEEDS-INVESTIGATION and not previously on anyone's
radar in this governance thread as of 2026-09-24.

## 3. D-28/D-59 scored-window conflict (added 2026-09-24)
Trigger: before G-05, or the next time anyone touches December-partition code
(`src/evaluation/guards.py`, `src/data/splits.py`, `src/evaluation/regimes.py`) or
`configs/experiment.yaml`'s `embargo_hours`/`regimes.december_day_range` fields.
Action needed: the Student ruled D-28 amended to 29 days (option B, zero additional
December contact), but this directly contradicts D-59 (Student+Supervisor
countersigned, 30 days, live in `configs/experiment.yaml:376`, enforced by
`src/evaluation/regimes.py:read_december_day_range`), and the code's
`scored_window_statement` still computes 30 days from the shared, Mandated
24-hour `embargo_hours` value used by every partition. Full analysis:
`governance/CHANGE_RECORD_2026-09-24_d28_29day_amendment.md`. The 45+ live
project design/governance artifacts still correctly describe the system as 30
days and were deliberately NOT swept to 29 — sweeping them now would be wrong
until this conflict is resolved. Needs one of: amend D-59 too (Supervisor), revert
to option A, or hold as pending. Do not silently sweep the remaining files to "29"
without first resolving this.

## 4. `budget_value` combination rule (added 2026-09-24)
Trigger: before this value is needed for any Vision §5.3 practical-relevance
computation, or the next time the Supervisor is available to rule on a §18.2
forbidden-choice item.
Action needed: no specific combination rule (statistic: median/p95/max;
combination: sum/quadrature/max) has ever been proposed anywhere in this
repository — confirmed by a full-repo search 2026-09-24 (every occurrence of
`budget_value` describes it as open, unfixed, and routed to the Supervisor as a
forbidden-choice item; none proposes actual values). Item 2 of the 2026-09-24
session task stopped here rather than inventing a rule. The exact rule text is
needed from the Student/Supervisor before `configs/data.yaml`'s
`target.uncertainty_budget` block can be frozen.
