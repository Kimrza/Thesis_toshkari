# Code Generation Questions — `governance-guards`

**Unit** `governance-guards` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`

**No open questions.** Construction questions are exceptional, and this unit's
design leaves no §18.3 stop-and-report point open at implementation time: the
module homes are design-fixed (`src/data/phase_contract.py` per
`business-logic-model.md` and application-design `component-methods.md`;
`src/data/reuse_registry.py` per SD-G-06/TE §12), the literal-scan upgrade is
already ruled (nfr-requirements Q2 = B, AST with constant folding — DISC-2
records it as "owed at 3.5"), and the chokepoint's fail-closed posture is ruled
(nfr-design Q1 = A). DISC-1's six-vs-seven exempt-list count is owed at the
GATE, not here, per the design's own routing.

**Recorded input (human ruling, 2026-09-05)**: this unit's terminal READY
nfr-design review Minors are recorded input for this run — see
`governance/RULING_2026-09-05_nfr-design_governance_dispositions.md`. For
`governance-guards` the standing Minors are the two scope-limited verification
notes (the seven-member exempt list spot-checked rather than re-derived
line-by-line; `_read_guarded`'s defining file outside that review's read
scope) — both are verification-scope records, addressed by this run's tests
re-deriving the exempt set programmatically and by naming `_read_guarded`'s
homes in the code summary.

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

Implementation commitments this run builds from the design (no new decisions):

- `src/data/phase_contract.py` (new): `assert_phase_boundary(phase, loaded_modules)` run-time import limb (RAW_MODULES = rinex, calibration, target, verification); `assert_no_raw_fields` produced-field limb (R-23: neither limb substitutes for the other) with a completeness test that gates on the eight producing scripts existing (none exists today); `diff_protected_hashes` (TE §7.0B / TA-27's hash-diff half); `PhaseBoundaryError` deriving from `IntegrityError` imported from `src/data/config.py`.
- DISC-2 closure: upgrade the restricted-root literal scan in `tests/test_locked_test_guard.py` from textual substring to AST with constant folding, so the concatenated-literal evasion (`"locked_test" + "_restricted"`) is caught; negative control included.
- `src/data/reuse_registry.py` + `tests/test_reuse_registry.py` (new): §10.1 register with the full field set, registered-before-use enforced, reimplementation-as-default posture; AGPLv3 governance dependency stated, never resolved here.
- `src/data/locked_test.py`: verify (and implement if absent) the Q1 = A fail-closed refusal on a platform whose durability semantics are uncharacterised; no behavioural change to the built chokepoint properties (refuse ordinary paths, boundary from module location, failed log write aborts read, fsync, guard-stamped `logged_at_utc`).
- SD-G-02 join: `RegistryEvent`'s producer now exists (`src/data/experiment_registry.py`, built in foundation's pass) — wire/verify both-way orphan reconciliation against `AccessRecord`; the five pre-guard December orphans + the Rec-31 unresolved access stay orphans, never backfilled.
- Tests: negative control per hard rule; exempt-set membership re-derived exactly (seven members, catching DISC-1's stale-count risk in code rather than prose); documentation test that the static scan's subordinate-status docstring stays present.
- No acceptance row claimed discharged (WS-18, TA-18, TA-25, TA-27, TA-28 all stay `Pending`); suite runs are smoke evidence under the bootstrapped 3.11.9, never governed evidence; no git commit (governance stop items accumulate with foundation's).

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Plan Approval

The code-generation plan for `governance-guards` is at
`construction/governance-guards/code-generation/code-generation-plan.md` — 11
steps: phase_contract.py three guards (1–3), DISC-2 AST scan closure (4),
exact exempt-set test (5), locked_test.py Q1=A posture (6), orphan-join wiring
(7), reuse_registry.py + tests (8), documentation tests (9), smoke run + lint
(10), governance stop (11).

- Approve Plan
- Request Changes

[Answer]: Approve Plan
