# Change record — 2026-09-24 — D-28 option (b) mechanism BUILT (unfrozen via post-receipt amendment); wiring STOPPED

**Status.** The bounded 1-December lookup mechanism (`RULING_REQUEST_2026-09-21_GOV-CG-01_OPEN_ITEMS.md`
§2 Option A) is now **built, tested, and inert** in `src/data/locked_test.py`
(`governance-guards` unit), via the same post-receipt amendment pattern used for the
chokepoint scanner fix earlier today. **Wiring it into the live M-01/M-02 prediction path is
NOT done** — stopped deliberately, see the STOP section below.

---

## What was built

`src/data/locked_test.py`:
- `PURPOSES` gains `"persistence_history"`.
- `PERSISTENCE_HISTORY_CALLERS = frozenset({"M-01", "M-02"})`.
- `PERSISTENCE_HISTORY_DAY = "2022-12-01"`.
- `read_persistence_history_lookup(snapshot, *, model_id, g05_signature, loader, registry, now=None)`
  — the mechanism itself.

`configs/experiment.yaml`:
- New `persistence_history_lookup: {authorized: false, decision: "TBD — freeze gate"}` block
  — the mechanism's own kill switch, shipped OFF.

`tests/test_locked_test_guard.py`: 6 new tests, one per condition plus a real-config check.

## The 5 conditions — each independently enforced and tested

| # | Condition | Enforcement | Test |
|---|---|---|---|
| i | No 1-Dec row is ever scored | Structural (by construction, in `persistence.py`'s own indexing, unaffected by this change) **plus** this function's own second check: silently drops any row outside `PERSISTENCE_HISTORY_DAY` | `test_ph_condition_i_never_returns_a_row_outside_1_december` |
| ii | Only M-01/M-02 | `model_id not in PERSISTENCE_HISTORY_CALLERS` raises before any read | `test_ph_condition_ii_only_m01_m02_may_call_it` |
| iii | Routed through `open_restricted`, logged | Every call appends a real `AccessRecord` (`purpose="persistence_history"`) through the one-door chokepoint | `test_ph_condition_iii_logs_a_complete_access_record` |
| iv | Post-G-05 only | Reuses `verify_g05_signature` (`src.data.splits`) — the SAME function `materialise_locked_partition` uses for the scored DEC frame itself | `test_ph_condition_iv_blocked_pre_g05_succeeds_post_g05` |
| v | Frozen under its own D-number before use | `configs/experiment.yaml: persistence_history_lookup.authorized` must be `True` AND `.decision` must start with `"D-"` — both fail-closed | `test_ph_condition_v_inert_until_its_own_d_number_is_authorized` |

Plus `test_ph_the_real_config_ships_inert_today` — confirms against the real, committed
`configs/experiment.yaml` (not a synthetic stand-in) that the mechanism is unauthorized as
shipped.

## Verification performed 2026-09-24

- `ruff check` on both modified files: clean.
- New tests: 6/6 passed in isolation.
- Full `test_locked_test_guard.py`: 72/72 passed (66 existing + 6 new).
- Full §18.3 critical test set, re-run after this change: **772/772 passed** (766 + 6 new,
  count reconciles exactly — no regression anywhere else).
- All under the governed `tec-thesis-311` (Python 3.11.16) environment.

## STOP (2026-09-24) then RESOLVED (2026-09-24, same day) — wiring now built

Originally stopped here: wiring means editing `scripts/06_train_and_predict.py` (owned by
`fixtures-and-reproducibility`/`models-and-baselines`), a second/third unit beyond
`governance-guards`, which no prior post-receipt amendment in this repository's history had
crossed into.

**The Student explicitly authorized connecting the mechanism** the same day, after D-68 was
ruled. The wiring is now built — a thin, isolated helper
(`_persistence_history_augmented_target`) plus three new optional keyword parameters on
`_locked_predictions`, none of which changes behaviour for any caller that omits them.
Full account, including its own dedicated test proving the wiring in isolation from the
mechanism's already-tested 5 conditions: `governance/CHANGE_RECORD_2026-09-24_d28_option_a_wiring.md`.

## RULED — D-68, written into `evidence/DECISIONS.md` 2026-09-24

Countersignature: Student — Approved by instruction, 2026-09-24, no separate supervisor
signature claimed. `configs/experiment.yaml: persistence_history_lookup` now reads
`authorized: true`, `decision: "D-68"`. The mechanism is live and, as of the same-day
wiring authorization, connected to the real DEC-partition prediction path — see
`governance/CHANGE_RECORD_2026-09-24_d28_option_a_wiring.md`.

**Decision required — Approve / Reject / Modify / Postpone** on the mechanism as built, and a
separate decision on whether/when to authorize the cross-unit wiring follow-up.
