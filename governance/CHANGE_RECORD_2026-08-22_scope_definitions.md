# Change Record — `CR-2026-08-22-SCOPE-DEFS`

**Vision §15.2 change-control record.**

| Field | Value |
|---|---|
| **Change record ID** | `CR-2026-08-22-SCOPE-DEFS` |
| **Date** | 2026-08-22 |
| **Requested by** | Project decision owner (student), acting under the recorded student/supervisor authority equivalence |
| **Approved by** | Project decision owner. No separate supervisor signature artifact exists and none is claimed |
| **Origin** | Governance report `GOV-2026-08-22-DP-01`, findings `DP-BENCH-01` and `DP-CHAIR-04`; owner instruction of 2026-08-22, items 5 and 7 |
| **Documents amended** | `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §9.2 |

## What changed

Technical Environment §9.2 carried the bullet *"Run both walking-skeleton fixtures before
any full-year job"* with **no definition of "full-year job"**. The same document uses
"full-year generation" (§7) and "full-year processing" (§10 source table) and defines
neither. The document was searched for a definition before this amendment was drafted;
none exists.

The absence was consequential rather than cosmetic. `scripts/run_walking_skeleton.py`
enforces the ordering contract, and that script is written in the last unit of the build
order — so between the first and the eleventh unit the rule had no enforcement point and no
agreed scope. Whether acquiring a full calendar year of provider data fell inside the term
was genuinely open, and an implementer could have read it either way.

**Added to §9.2:** a three-class table distinguishing (A) raw acquisition and custody,
(B) fixture-scale development and testing, and (C) full-year scientific processing and
evaluation — with **only class C** classified as a full-year job requiring prior fixture
evidence.

## What did not change

- **No scientific value, threshold, tolerance, seed, grid, fold, mask or estimand.**
- **No locked-December protection is relaxed.** The amendment states explicitly that every
  December restriction applies to class A unchanged: no analytical inspection of December
  target values, no December performance quantity computed or examined, and every access
  under `evidence/locked_test_restricted/` routed through the single chokepoint that writes
  its access-log row before the read. Integrity verification of December bytes is custody
  work, not analysis.
- **No re-acquisition is authorized.** The amendment records that existing data is not
  re-downloaded without an independently justified and recorded need.
- **The ordering contract itself is unchanged.** Both fixtures still run, in order, before
  any class C activity.

## Why class A is not a full-year job

Two reasons, both structural rather than convenient. Retrieval performs no scientific
processing — it moves and verifies bytes. And the fixtures are themselves built from
retrieved data, so classifying acquisition as a full-year job would make the ordering
contract circular: no fixture could be built until the fixtures had passed.

## Downstream effects

| Artifact | Effect |
|---|---|
| `FR-WS-1` | Unchanged. Its criterion (*"Fixture run log shows plumbing before scientific before any full-year job"*) now resolves against a defined term |
| `WS-20`, `TA-09`, `TA-17` | Unchanged in content; the sequence they test is now unambiguous |
| `bolt-plan.md` § "What every Bolt owes" item 6 | Its three-category table was provisional on this decision and is now settled by it |
| `scripts/run_walking_skeleton.py` | Its guard implements class C, not class A. Specification only — the script does not exist |

## Verification performed

- Searched the Technical Environment for a pre-existing definition of "full-year job",
  "full-year processing" and "full-year generation": **none found**; three undefined
  variants in use at §9.2, §7 and the §10 source table.
- Confirmed the amendment text introduces no numeric value, no threshold and no scientific
  constant.

**No test was executed for this amendment.**

**Correction, 2026-08-22.** An earlier revision of this record stated "no test suite exists in this repository". That was wrong. **Three of the mandated modules exist** — `tests/test_acquisition_window.py`, `tests/test_phase_boundary.py` and `tests/test_release_hashes.py` — and `.pytest_cache` records **226 collected test node IDs** from a run on 2026-08-21 under CPython 3.11 / pytest 8.3.5. What remains true is that **no test was executed for this amendment**, and that the modules this amendment concerns do not exist. The three existing modules were **not** run during this work, deliberately: all three reference `evidence/locked_test_restricted/`, and the `open_restricted` access-log chokepoint that BLK-07 requires does not exist yet, so executing them would perform December reads with no access-log row.
