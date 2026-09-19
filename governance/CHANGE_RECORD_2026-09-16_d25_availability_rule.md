# Change Record — 2026-09-16 — D-25 availability rule: Route 1 minimum contract

**Change ID:** `CR-2026-09-16-D25-AVAILABILITY-RULE`
**Authority:** the project decision owner's explicit in-session ruling authorising
**Route 1** for D-25 — *"Implement the minimum additive availability-rule contract"* —
restated verbatim on 2026-09-18 as the reconstruction brief for this clone. This is the
owner instruction `project.md` (`code-generation:c32`) names as the sanctioned route for
an edit to a READY-reviewed unit's module (`features-and-splits`, receipt READY at
`construction/features-and-splits/code-generation/code-summary.md`).
**Decision remediated:** **D-25** (`evidence/DECISIONS.md`, frozen 2026-08-22):
`availability_ts(median(D-1)) = 00:00 UTC on D`. D-25 is already frozen; this record
changes no decision. **No new D-number is required or drafted** — the rule identity
introduced here transcribes D-25's own text into an executable contract and decides no
scientific constant, no governed config value, and no §18.2 item.
**Repository state:** written from `HEAD = 18843aa`. **No commit is made by this pass**
(owner instruction; the commit remains the student's act). The commit, when the student
makes it, cites this change ID per `team.md`'s linking rule.
**Provenance of this record:** the original Route 1 implementation and this record were
produced and reviewed on 2026-09-16 in a working tree that was never committed or pushed
and is not this clone (`git reflog` here: clone 2026-09-12, pull 2026-09-13, one
audit-only commit 2026-09-14; nothing later on any ref, stash or dangling object).
The owner ruled on 2026-09-18 that this clone is canonical from now on and that Route 1
is **reconstructed here from the approved specification only** — not from memory of the
lost diff, not by cherry-pick or copy. The filename keeps the original record date; the
content is the reconstruction.

This record is written FIRST, before any code or test edit of this pass.

---

## 1. Why the contract is needed (the gap, stated exactly)

`src/features/availability.py` at `18843aa` represents every feature's availability as
one scalar `safe_lag_hours`, read from `configs/features.yaml: availability_lags`. D-25
is a **calendar-day** rule: the daily F10.7 median for UT day *D* becomes available at
`00:00 UTC on D+1`, so its lag at a forecast origin depends on the origin's hour within
the day (1 h at 01:00, 23 h at 23:00). No scalar `safe_lag_hours` can state that rule
faithfully — any scalar either over-states availability for early-day origins (leakage)
or under-states it for late-day origins (a fabricated lag). The matrix therefore needs
a rule identity, not a number, for that feature.

## 2. The change, exactly (minimum additive contract)

`src/features/availability.py`:

1. **Closed rule set.** `AVAILABILITY_RULE_PREVIOUS_DAY_MEDIAN_MIDNIGHT_UTC =
   "previous_day_median_midnight_utc"` and `AVAILABILITY_RULE_KINDS`, a `frozenset` of
   the recognised kinds (exactly one today). An `availability_rule` value outside the
   set — or `TBD — freeze gate`, or a non-string — is refused at config read.
2. **`AvailabilityRow` gains `availability_rule: str | None`** (additive, defaulted).
   `safe_lag_hours` becomes `float | None`, and is `None` ONLY when a recognised
   `availability_rule` is recorded on the same row.
3. **Mutual exclusion at config read.** A rule-bearing feature must not also declare
   `safe_lag_hours`; must not also declare a trailing `window` (the anchor limb is a
   scalar-lag construct: `expected_anchor = origin − safe_lag_hours`); and a feature with
   neither a valid scalar nor a recognised rule is refused naming both.
4. **`build_availability_matrix`.** The existing observation/publication availability
   instant is computed exactly as before. For the D-25 rule the rule instant is
   `midnight UTC of observation_day + 1 day`, and the recorded availability instant is
   `max(existing_available_at, rule_available_at)`. A resulting negative lag (an origin
   before the rule instant — same-day or future-day anchoring) is refused at build with
   `LeakageError`. The row records `safe_lag_hours=None` and the rule identity.
5. **`assert_lags_safe`.** A rule row passes limb 1 on a non-negative measured lag and a
   recognised rule identity; a row carrying neither a scalar nor a rule fails; scalar
   rows are compared exactly as before.
6. **Block-level fail-closed is untouched**: an absent, `TBD`, non-mapping or empty
   `availability_lags` block still refuses naming D-10.3, and a scalar feature's absent
   or `TBD` `safe_lag_hours` still refuses.

`scripts/05_build_features_and_splits.py`: `PRODUCED_FIELDS` gains
`"availability_rule"`, so R-24's produced-field guard (`assert_no_raw_fields`) sees the
new matrix column before the first write. No other line of the script changes.

**The conservative direction, stated once.** `max(existing, rule)` means the rule sets a
floor on availability, never a ceiling. It can only ever shorten a measured lag, which is
the conservative direction — a shorter lag is closer to the limb-1 floor and to the
negative-lag refusal. A publication timestamp later than the rule instant still governs,
because the max keeps it; the rule never bypasses a later publication.

> **Amended 2026-09-19 (A2, owner-approved; `CR-2026-09-19-GATE-PREP-2` § A2).** Item 6
> above ("must not also declare a trailing window") is NARROWED: a feature carrying the
> D-25 rule `previous_day_median_midnight_utc` MAY compose with a trailing window
> (`AVAILABILITY_RULES_WITH_WINDOW`), and the anchor limb then derives the window end day
> from the rule (`latest_eligible_window_end`: the latest observation day whose constituent
> availability instant is at or before the forecast origin) and verifies every constituent's
> availability. The rule is confined to the F10.7 rows (`AVAILABILITY_RULE_SCOPE`) and is
> never extended to the GFZ series. Items 3–5, 7–10 are unchanged. Reason: the executable
> counterexample in `CR-2026-09-18-GATE-PREP` §2 (the scalar-plus-window shape passed
> limb 1 only under an anchor-day-midnight convention).

## 3. What this change does NOT do

- `configs/features.yaml: availability_lags` remains the literal `"TBD — freeze gate"`.
  No entry is transcribed — not Q1 (`kp_safe`/`ap_safe`), not Q2 (`hp60_safe`/`ap60_safe`),
  not the F10.7 rule. The contract exists; the configuration is still owed at the freeze.
- `feature_dictionary`, `feature_set_id`, `normalization` remain `TBD`.
- No producer artifact is created; no `permitted_producers` driver row is added.
- Stage 07 is not wired. `window.recomputation_tolerance` is not chosen.
- No target, feature-selection, leakage-policy, history-length, horizon, station-weighting,
  comparison-set, regime or Phase 2 text or code is touched. No scientific scope expands.
- No data is acquired; no live provider transport is authorised or constructed
  (`scripts/00_acquire_prepared_vtec.py:_build_transport` still refuses; DATA-07 stands).

## 4. Tests added (no existing control weakened or removed)

`tests/test_feature_availability.py`, new section "D-25 availability rule (Route 1)",
using the module's existing synthetic-fixture conventions (`_lags`, `_drivers`,
`synthetic_snapshot`; SYNTHETIC values only — no frozen lag appears):

1. a valid D-25 rule computes next-day-midnight availability (row carries the rule,
   `safe_lag_hours is None`, measured lag = origin − 00:00 UTC of D+1);
2. the availability instant is independent of the origin hour for one observation day;
3. same-day anchoring (origin on the observation day) is refused;
4. centered / future-looking anchoring (observation day after the origin day) is refused;
5. an unknown rule kind is refused at config read;
6. rule + scalar `safe_lag_hours` is refused;
7. rule + trailing `window` is refused;
8. neither scalar nor recognised rule is refused, naming both;
9. a publication timestamp later than the rule instant still governs the lag;
10. scalar features keep their previous rows exactly (`availability_rule is None`);
11. incomplete / `TBD` configuration stays fail-closed with the rule present
    (`availability_rule: TBD`, an empty block, a `TBD` scalar beside a rule feature);
12. `assert_lags_safe` refuses a rule row with a negative lag and a row with neither
    scalar nor rule.

## 5. Disclosure obligations (`project.md` `code-generation:gf-3`, `c30`)

- **`features-and-splits` code-summary is now stale** under its READY receipt for
  `src/features/availability.py` (its `AvailabilityRow` field list and the module's
  function set) and for `tests/test_feature_availability.py` (its "54 test functions"
  count). Per `gf-3` the staleness is carried here and to the `build-and-test` gate as an
  explicit finding; the receipted record is not rewritten. **`external-products` is not
  touched** (the F10.7 daily-cadence composition stop in `spaceweather.py` stays).
- `scripts/05_build_features_and_splits.py` is a `features-and-splits` module; the same
  disclosure covers its one-tuple edit.
- Design annotation, not an edit: `construction/features-and-splits/functional-design/
  domain-entities.md` § AvailabilityRow lists the six approved fields plus two additive
  ones; a third additive field now exists. Annotated here; the signed design is not edited.

## 6. Propagation sweep (CHANGE_RECORD_PROCEDURE step 2)

Superseded literal: none — this record amends no count, enumeration, ID range or
status. The `AvailabilityRow` field count ("six approved fields plus two ADDITIVE") is a
description in the module docstring and in the design; the docstring is updated in the
same edit, the design is annotated in §5. Sweep for `safe_lag_hours` consumers outside
the unit: `grep -rln "safe_lag_hours\|AvailabilityRow" src scripts tests` → exactly
`scripts/05_build_features_and_splits.py`, `src/features/availability.py`,
`src/features/build.py` (reads `row.feature` only), `tests/test_feature_availability.py`.
No other consumer.

## 7. Verification (appended after execution, 2026-09-18)

**Environment, stated exactly.** CPython **3.14.7** (`C:\Python314\python.exe`) with real
`pytest 9.1.1`; `pyyaml`, `numpy`, `pandas`, `tensorflow` absent; `ruff` not installed.
This is NOT the governed pin (TE §8.1: Python 3.11) and NOT Kaggle (TC-03g), so every
result below is **supplemental smoke evidence**, never a governed run, and none of it
discharges WS-11, TA-08 or any §16/§19 row.

**Measured diff (`git diff --numstat`, HEAD `18843aa`):**

| File | + | − |
|---|---|---|
| `src/features/availability.py` | 143 | 13 |
| `tests/test_feature_availability.py` | 202 | 0 |
| `scripts/05_build_features_and_splits.py` | 1 | 0 |
| `governance/CHANGE_RECORD_2026-09-16_d25_availability_rule.md` | new | — |

The 2026-09-16 record's figure for `availability.py` (+121 / −5) is **not reproduced**
and is **not claimed**: this is a reconstruction from the specification, not a copy of the
lost diff, and its measured statistic is +143 / −13 (the difference is docstring and
message text, not a different contract).

- `python -m pytest tests/test_feature_availability.py`: **66 passed, 2 skipped**
  (both skips: `yaml` absent) — 54 pre-existing + **12 new**, none removed or weakened.
- `python -m pytest tests` (whole `tests/` tree, `PYTHONHASHSEED=0`): **1192 passed,
  39 skipped, 0 failed** in 96.96 s.
- `python -m compileall -q src scripts tests`: exit **0**.
- `git diff --check`: exit 0. `ruff`: not available on this host — not run.
- **Mutation controls, 8/8 killed** (scratchpad script; original bytes restored and
  SHA-256-verified afterwards): M1 rule instant same-day; M2 `min` for `max`; M3 open rule
  set; M4 rule+scalar accepted; M5 rule+window accepted; M6 negative rule lag not refused
  at build; M7 neither-scalar-nor-rule accepted in `assert_lags_safe`; M8 rule overrides
  a later publication. Each killed by a different named test.
- Guards re-verified after the run: `configs/` has zero diff; `availability_lags`,
  `feature_dictionary`, `feature_set_id`, `normalization` all read `"TBD — freeze gate"`;
  zero driver rows under `permitted_producers`; zero `safe_lag_hours` literals in
  `src/`, `scripts/`, `configs/`; `scripts/07_evaluate_and_report.py` untouched;
  no file under `evidence/`, `artifacts/` or `tests/fixtures/` created.

**Side effect disclosed, not reverted.** The whole-suite run appended **148** rows to
`evidence/test_run_access_log.jsonl` (140 from `test_release_hashes`, 8 from
`test_acquisition_window`; class `TA-15 integrity verification; Vision 8.3
performance-blind class`, `performance_inspected: false`). That log is append-only by
design (NFR-AUD-01: never delete an access record) and the student committed the
previous 74 rows in `897e33b`; the rows are left in place for the student's commit
decision.

**Not done, by the owner's bounds:** no data acquired; no live transport authorised or
constructed; no `availability_lags` entry written; no Q1/Q2 transcription; no producer
artifact or `permitted_producers` row; no Stage 07 wiring; no `recomputation_tolerance`;
no commit, no push, no `graphify query`.
