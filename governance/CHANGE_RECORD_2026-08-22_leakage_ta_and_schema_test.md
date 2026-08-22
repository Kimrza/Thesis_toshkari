# Change Record — `CR-2026-08-22-LEAKAGE-TA` and `CR-2026-08-22-TARGET-SCHEMA-TEST`

Two Vision §15.2 amendments approved together by the project decision owner on
2026-08-22 and recorded in one file because both amend TE §12/§19 in the same act.

| Field | Value |
|---|---|
| **Date** | 2026-08-22 |
| **Requested by / approved by** | Project decision owner, under the recorded student/supervisor authority equivalence. No separate supervisor signature artifact exists and none is claimed |
| **Origin** | Governance report `GOV-2026-08-22-DP-01`, findings `DP-ML-01` (leakage rows) and the BLK-05 module-name decision |
| **Documents amended** | `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §12 and §19; `aidlc/.../requirements-analysis/requirements.md`; `aidlc/.../units-generation/unit-of-work-story-map.md`; `aidlc/.../units-generation/unit-of-work.md` |

---

## `CR-2026-08-22-LEAKAGE-TA` — four negative-path acceptance rows

**What changed.** TE §19 gains **TA-33, TA-34, TA-35 and TA-36**, one per
leakage-sensitive requirement that previously had no acceptance row.

| New row | Requirement | Prohibited behaviour | Deliberately invalid input | Expected protective behaviour | Owning unit / Bolt |
|---|---|---|---|---|---|
| **TA-33** | FR-P1-04-12 | A field outside the §6.2 dictionary entering training or inference; a tuned history window | A non-dictionary field injected into feature construction; an `experiment.yaml` placing window length in a grid | Construction **raises**; the tuned-window run **fails** | `features-and-splits` / Bolt 7 |
| **TA-34** | FR-P1-04-13 | A carried-forward `vtec_lag_*` value; an incomplete `vtec_seq_24` window admitted | A carry-forward-produced lag value; a 24-step sequence with a missing step | The carried-forward value **fails**; the incomplete window is **excluded and counted** | `features-and-splits` / Bolt 7 |
| **TA-35** | FR-P1-04-16 | A support field used as a model input without recorded G-04 approval; a support field read at or beyond hour *t* | A support field admitted with no approval ID; one read at the target hour | Feature construction **fails** in both cases | `features-and-splits` / Bolt 7 |
| **TA-36** | FR-P1-04-17 | Kp repeated outside its own 3-hour interval; Dst shifted to a neighbouring hour; any driver interpolation | Both misalignments injected as explicit negative controls | Each **fails**; no interpolation call exists on any driver series | `external-products` / Bolt 5 (requirement owner); enforcement raise at `features.build_features` in `features-and-splits` / Bolt 7 |

**Required acceptance evidence**, per row: executed negative-path test output
showing each rejection, plus the supporting manifest artifact named in the §19
Evidence column (feature manifest, excluded-window count, approval-ID marking, or
driver interval semantics and the no-interpolation check result).

**Why these four and not the other 36 untested requirements.** They are leakage
controls, not coverage gaps. Each prohibits a distinct route by which information
the model should not have can reach it, and each failure is invisible in
validation.

**Status of all four: `Pending`.** Four distinctions are preserved and must not be
collapsed:

1. Each requirement now has an **acceptance criterion** — done.
2. No test is **implemented** — no module exists for any of the four.
3. No test has been **executed**.
4. No test has **passed**.

Module placement for these four tests is an open assignment at functional design.

**Counts recalculated from the updated artifacts, not assumed:**

| Measure | Before | After | Verified how |
|---|---|---|---|
| Requirements with no acceptance row | 40 | **36** | Counted `NO CURRENT ACCEPTANCE ROW` in story-map Table 1, and `UNTESTED` in the requirements tables — both give 36 |
| Phase 1-applicable TA rows mapped | 27 | **31** | Counted `TA-nn` row leads in story-map Table 2 |
| Total acceptance rows mapped | 40 | **44** | 13 WS + 31 TA |
| Acceptance rows with a primary owner | 39 | **43** | 44 mapped, TA-24 unowned |
| `features-and-splits` untested | 4 | **1** | FR-P1-04-10 only |
| `external-products` untested | 5 | **4** | REQ-ENG-9, FR-P1-04-4, FR-P1-04-15, FR-P1-04-18 |

The predicted values were 40 → 36, 27 → 31 and 40 → 44. **All three match the
recomputed values.** No difference to explain.

**Unchanged:** 105 requirements, 12 units, 23 dependency edges, 13 WS rows.

---

## `CR-2026-08-22-TARGET-SCHEMA-TEST` — the D-17 target-schema module

**What changed.** TE §12's `tests/` tree gains
**`tests/test_prepared_target_schema.py`**, with a row in the §12
amendment-provenance table. The tree now enumerates **21** test modules.

> **Arithmetic correction, 2026-08-22** (`GOV-2026-08-22-INC-01` Rec 4,
> approved by the project owner; applied under `CR-2026-08-22-INC-CORRECTIONS`).
> **Superseded text, preserved for the audit trail:** *"The tree now enumerates
> **20** test modules."* That figure counted only this record's own amendment on a
> 19-module base and omitted `tests/test_feature_leakage_guards.py`, which the
> **other half of this same record** (`CR-2026-08-22-LEAKAGE-TA`, see above) adds
> to the same tree. This file states at its head that both amendments are
> "recorded in one file because both amend TE §12/§19 in the same act", so the
> combined result is **21**, not 20. No scientific value, gate, checklist row or
> approval changes under this correction; only the arithmetic.

**Approved acceptance behaviour**, fixed by the owner:

- A valid row containing **exactly** the 16 fields approved by D-17 **passes**.
- A row containing an **excluded or additional** field **fails**.
- A row **missing any required** field **fails**.

**Naming basis.** Selected from three candidates presented against the existing
convention. All 20 prior modules are flat under `tests/`, `test_<subject>.py`,
snake_case, subject naming the thing under test. `test_prepared_target_schema.py`
mirrors its owning module `src/data/prepared.py` the way `test_station_registry.py`
mirrors `registry.py`. It cannot reuse `test_hourly_target.py`, which is Phase 2
only.

**BLK-05 is not resolved by this.** Four limbs, two complete:

| Limb | Status |
|---|---|
| Naming | **Resolved** 2026-08-22 |
| Documentation (§12 tree + downstream artifacts) | **Resolved** 2026-08-22 |
| Test implementation | **Pending** — the module does not exist |
| Execution evidence | **Pending** — never run; no result claimed |

**FR-P1-03-5 remains untested.** Naming a module is not adding an acceptance row;
FR-P1-03-5 stays in the 36-row untested list.

---

## What neither amendment changed

- No scientific value, threshold, tolerance, seed, grid, fold, mask, embargo or
  estimand.
- No frozen decision, no dependency relation, no unit boundary, no
  one-unit-per-Bolt assignment.
- No locked-December protection. Neither amendment touches December data, and no
  December record was read in producing them.
- No prohibition was widened or narrowed — TA-33…TA-36 test prohibitions that
  already existed.

## Verification performed

- TE §19 maximum row before the amendment: **TA-32**; new rows take TA-33…TA-36
  with no collision.
- TE §12 `test_*.py` entries after **both** amendments in this record: **21**,
  enumerated (`sed -n '675,703p' <TE> | grep -oE 'test_[a-z_]+\.py' | sort -u | wc -l`).
  **Superseded text, preserved for the audit trail:** *"TE §12 `test_*.py` entries
  after the amendment: **20**, enumerated."* — computed over one of this record's
  two amendments. Corrected 2026-08-22, `GOV-2026-08-22-INC-01` Rec 4.
- Requirement/acceptance counts recomputed from the artifacts as tabulated above.
- 105 requirements defined and 105 assigned; 12 units; 23 edges — all re-derived
  and unchanged.

**No test was executed for this amendment.**

**Correction, 2026-08-22.** An earlier revision of this record stated "no test suite exists in this repository". That was wrong. **Three of the mandated modules exist** — `tests/test_acquisition_window.py`, `tests/test_phase_boundary.py` and `tests/test_release_hashes.py` — and `.pytest_cache` records **226 collected test node IDs** from a run on 2026-08-21 under CPython 3.11 / pytest 8.3.5. What remains true is that **no test was executed for this amendment**, and that the modules this amendment concerns do not exist. The three existing modules were **not** run during this work, deliberately: all three reference `evidence/locked_test_restricted/`, and the `open_restricted` access-log chokepoint that BLK-07 requires does not exist yet, so executing them would perform December reads with no access-log row.
