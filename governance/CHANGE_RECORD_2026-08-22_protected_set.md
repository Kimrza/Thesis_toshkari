# Change Record — `CR-2026-08-22-PROTECTED-SET`

**Vision §15.2 change-control record.**

| Field | Value |
|---|---|
| **Change record ID** | `CR-2026-08-22-PROTECTED-SET` |
| **Date** | 2026-08-22 |
| **Requested by** | Project decision owner, acting under the recorded student/supervisor authority equivalence |
| **Approved by** | Project decision owner, in advance and explicitly: *"Amend FR-P1-06-1 under §15.2 if its existing enumeration or fixed item count conflicts with the approved canonical set."* A conflict exists (14 versus 17), so the authorization is engaged. No separate supervisor signature artifact exists and none is claimed |
| **Origin** | Governance finding `UG-01` (`GOV-2026-08-21-UG-01`) → **BLK-06**; owner instruction of 2026-08-22, item 5; decision **D-24** |
| **Documents amended** | `aidlc/.../inception/requirements-analysis/requirements.md` — FR-P1-06-1 only |

## What changed

FR-P1-06-1 required `protected_hashes.keys()` to equal a **fourteen-item enumeration**.
D-24 freezes the canonical protected set as the deduplicated union of TE §2.2 (12 items)
and TE §7.0B (16 items) with three previously unmapped §7.0B immutables added explicitly —
**17 items**, the cardinality calculated from the enumeration rather than assumed.

| | Before | After |
|---|---|---|
| Item count | 14 | **17** |
| Basis | "the union of TE §2.2 and §7.0B" with no stated deduplication rule | D-24's enumeration with its explicit deduplication rule |
| Items added | — | `history window`, `station encoding`, `baselines` |
| `baselines` scope | absent entirely | M-01, M-02, M-03, **B-01 IRI-2016 with its 2000 km ceiling**, C-01 CODE GIM |
| Criterion | "asserted equal to the fourteen-item enumeration" | "asserted equal to D-24's seventeen-item enumeration"; cardinality calculated, never assumed |

## Why the three items were added

Cross-checking §7.0B against the previous fourteen, item by item: `feature schema and safe
lags` maps to `feature manifest`; `target cadence/horizon` to `target contract`; `loss` and
`optimizer policy` to `optimizer/loss policy`; `splits`, `embargo` and `comparison-set
masks` to `split/mask manifests`. **Three map onto nothing.**

`history window` and `station encoding` are *plausibly* inside `feature manifest`, but no
artifact says so — and an assumed subsumption is not a hash. **`baselines` has no plausible
home in the previous list at all**, and that omission was the consequential one: a Phase 2
confirmatory run could change an M-01, M-02 or M-03 baseline definition and still produce
the empty `diff_protected_hashes` result that *is* G-P3C's pass condition. Protected-protocol
drift would pass undetected at a full-board gate.

## What did not change

- **No scientific value, threshold, seed, grid, fold, mask, embargo or estimand.**
- The refuse-to-train rule, the `exploratory=true` escape, and the test link (TA-27).
- **No locked-December protection.** This requirement governs the Phase 1 → Phase 2
  transition manifest and touches no December data.
- **No leakage surface.** Every added item is a *protection*, widening what the manifest
  hashes. Nothing is removed from protection and no data path is opened.

## What this does not close

BLK-06's **implementation** limb. `TransitionManifest.protected_hashes` and
`diff_protected_hashes` do not exist, and creating them stays gated by **G-09** and stage
3.5. The "hashable representation" column of D-24 names the intended form; binding each
item to a concrete config field completes at functional design, because none of the four
config files exists yet. **No file path or field name in D-24's table is claimed to exist
today.**

## Verification performed

- TE §2.2's protected sentence enumerated by hand: **12** items.
- TE §7.0B's immutables sentence enumerated by hand: **16** items.
- Deduplication applied under the stated rule; unmapped remainder: **3**.
- Canonical cardinality **calculated**: 14 carried forward + 3 added = **17**.

**No test was executed for this amendment.**

**Correction, 2026-08-22.** An earlier revision of this record stated "no test suite exists in this repository". That was wrong. **Three of the mandated modules exist** — `tests/test_acquisition_window.py`, `tests/test_phase_boundary.py` and `tests/test_release_hashes.py` — and `.pytest_cache` records **226 collected test node IDs** from a run on 2026-08-21 under CPython 3.11 / pytest 8.3.5. What remains true is that **no test was executed for this amendment**, and that the modules this amendment concerns do not exist. The three existing modules were **not** run during this work, deliberately: all three reference `evidence/locked_test_restricted/`, and the `open_restricted` access-log chokepoint that BLK-07 requires does not exist yet, so executing them would perform December reads with no access-log row.
