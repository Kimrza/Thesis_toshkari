# Code Generation Questions — `features-and-splits`

**Unit** `features-and-splits` (Bolt 7) · **Kind** `library` · **Stage** `code-generation`

This unit is barred outright: **"No implementation is authorised while BLK-04
stands"** (nfr-design banner), and BLK-04, BLK-08 and BLK-09 are open exit
conditions whose contracts (R-74, R-84, R-83) were authored at
functional-design but never separately approved — every artifact repeats
"approving this design is not its approval." The four questions below are the
change-control rulings that decide what this run may build. TE §18.3's
stop-and-report rule is why they are questions rather than defaults.

**Recorded input (human ruling, 2026-09-05)**: this unit's terminal READY
nfr-design review carries a READY (1 Major, 1 Minor) verdict whose findings are
record-only at this stage; listed in the plan, per
`governance/RULING_2026-09-05_nfr-design_governance_dispositions.md`.

---

## Question 1
**BLK-04** — approve R-74 (the ADR-11 train-only fitting contract: identity
check, the single enumerated `REFIT`→`DEC`/`role="score"` exception,
`fit_transforms`' four raises) as the governed cross-unit contract, recorded as
a change record citing `GOV-2026-08-22-REM-01`'s exit ruling? This is the
approval the blocker has been waiting on; without it no implementation of this
unit is authorised.

A) Approve R-74 now — change record written to `governance/` before any commit; implementation proceeds under it
   > **Impact**: Unblocks this unit and the four downstream units' eventual builds; the contract every reported number inherits becomes governed. NFR-LEAK-01's *evidence* is still owed to the Supervisor at G-04/G-05 — approval here governs the mechanism, not the evidence.

B) Defer — the unit stays barred; skip its code generation this Bolt
   > **Impact**: features-and-splits and everything downstream (models, evaluation, inference, reporting) stay unbuildable; the Bolt ends at six of twelve units.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — R-74 survived five review cycles and an adversarial nfr-design pass; it is the mechanism ADR-11 already fixed, and deferral blocks half the pipeline. Honestly stated: your approval here is the change-control acceptance the register requires, and the change record must exist before any commit.

[Answer]: A
## Question 2
**BLK-09** — approve R-83's amendment: `Partition` gains `train_start: date`,
both bounds sourced from `configs/data.yaml` and read from the `Partition`
(never inferred from a January-1 convention or a hard-coded year), with the
strict-subset negative control?

A) Approve R-83 now — recorded in the same change record; `src/data/splits.py` buildable
   > **Impact**: The identity check's range comparison gets the value it compares against; TC-03e holds (no scientific constant in source). The calendar VALUES themselves still enter `data.yaml` only under the split-boundary freeze (they are already TE §7.1-fixed text).

B) Defer — splits.py cannot be built; the unit's partition half stays open
   > **Impact**: transforms/availability/windows could build but nothing can express a partition; most of the unit's tests have no subject.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — R-83 exists precisely because the alternative (an inferred boundary) is "where an embargo silently disappears"; there is no second reasonable reading.

[Answer]: A
## Question 3
The **permitted-producer accessor** (SD-F-01): the list itself is unauthored
and stays that way (fail-closed raise is the deliverable), but HOW
`build_features` reads it is change-control-gated — the approved
`ConfigSnapshot` is frozen and carries no such field. Which accessor?

A) A separate loader beside `ConfigSnapshot` (`load_permitted_producers(configs_dir)` reading `configs/features.yaml`'s `permitted_producers` block) — no amendment to the frozen approved shape
   > **Impact**: Smallest change-control footprint; the frozen `ConfigSnapshot` is untouched; the TC-03e config-versus-code question resolves toward governed config (the block, when authored, is frozen under a D-number like every governed value). The raise binds this accessor.

B) Amend `ConfigSnapshot` to gain a `permitted_producers` field — change record against the approved application-design shape (the `write_restricted` footing)
   > **Impact**: One canonical snapshot object, but a change record against a frozen approved interface for a field only this unit reads.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — same governed-config direction the project takes everywhere else, and it avoids amending a frozen interface for a single consumer. Either way the list stays unauthored and `build_features` refuses while it is.

[Answer]: A
## Question 4
**BLK-08** (co-owned with `evaluation-and-comparison`) — half B is narrowed to
`ABL-DIFF` by D-27, which also states "no import-boundary change is authorised
by this decision". Confirm the defer: this run builds `Transform` with its
fitted state and `transform_id` addressing, but NO inverse-loading path and NO
`src/evaluation` → `src/features` edge?

A) Confirm defer — inverse mechanism + edge stay open, resolved at evaluation-and-comparison's build or a later change record
   > **Impact**: Consistent with D-27's explicit withholding; `ABL-DIFF` (an ablation) is not on Bolt 7's path. The R-84-vs-R-103 naming divergence (`load_inverse`/`Inverse` vs `load_transform`/`Transform`) also stays open for that unit's pass.

B) Approve the edge now
   > **Impact**: Directly contradicts D-27's recorded withholding — would need an explicit reversal argument per the never-reopen-a-refusal rule. Not recommended.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — D-27 already ruled; reopening a recorded refusal needs a new argument, and none exists.

[Answer]: A

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Q1 = A — **R-74 approved** as the governed BLK-04 cross-unit contract (ADR-11 identity check; single enumerated `REFIT`→`DEC`/`role="score"` exception; `fit_transforms`' four raises). Change record written to `governance/` before any commit; implementation of this unit is now authorised. NFR-LEAK-01's evidence stays owed to the Supervisor at G-04/G-05.
- Q2 = A — **R-83 approved**: `Partition` carries both `train_start` and `train_end`, sourced from `configs/data.yaml`, strict-subset negative control; recorded in the same change record. Calendar values enter `data.yaml` only at their freeze.
- Q3 = A — permitted-producer accessor is a **separate loader** (`load_permitted_producers(configs_dir)` reading `configs/features.yaml`); the frozen `ConfigSnapshot` untouched; the list itself stays unauthored and `build_features` **refuses** while it is (fail-closed, naming which §6.2 rows lack entries).
- Q4 = A — **BLK-08 defer confirmed**: `Transform` built with fitted state + `transform_id` addressing; no inverse path; no `src/evaluation` → `src/features` edge (D-27 stands).
- Build set: `src/features/{availability,build,transforms,windows}.py`, `src/data/splits.py`, `scripts/05_build_features_and_splits.py`, tests (`test_feature_availability.py`, `test_split_embargo.py`, `test_train_only_transforms.py` incl. the M10 synthetic fixture per Q12=C, limb-1 cases added to `test_locked_test_guard.py` per Q3=C with the two-unit ownership block); `spec.json` per-column provenance (Q2=A upstream); six partitions / five manifest rows; 24 h embargo excluded-and-counted; three availability limbs incl. the anchor recomputation; raw-longitude raise; window length 24 asserted grid-free; WS-13 two-ordered-assertion parity (value half unrunnable until the fixture tolerance freezes); `materialise_locked_partition` signature guard (no December execution).
- **No feature matrix is produced** (permitted-producer list unset — the refusal is the deliverable); no commit.

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Plan Approval

The code-generation plan for `features-and-splits` is at
`construction/features-and-splits/code-generation/code-generation-plan.md` —
10 steps: the R-74/R-83 change record FIRST (1), splits.py with both bounds +
locked-partition guard (2), availability.py with the anchor limb (3), build.py
+ separate loader with the fail-closed producer raise (4), transforms.py under
the approved contract (5), windows.py + spec.json provenance + WS-13 parity
(6), script 05 (7), four test modules incl. the M10 fixture and limb-1 cases
(8), smoke + lint (9), governance stop (10).

- Approve Plan
- Request Changes

[Answer]: