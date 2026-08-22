# `CR-2026-08-22-INC-CORRECTIONS` — Inception-phase governance corrections

| Field | Value |
|---|---|
| **Change record ID** | `CR-2026-08-22-INC-CORRECTIONS` |
| **Date** | 2026-08-22 |
| **Origin** | Governance report `GOV-2026-08-22-INC-01` (full-board review of the Inception phase, stages 2.2–2.8 plus the Inception→Construction boundary) |
| **Approved by** | **Project decision owner**, explicitly and per-recommendation, under the recorded student/supervisor authority equivalence. Recommendations 1–9 approved at option 1; Recommendations 10 and 11 approved at option 2. No separate supervisor signature artifact exists and none is claimed |
| **Class** | **Documentation integrity and one requirement addition.** No scientific value, frozen constant, gate criterion, fold, mask, seed, estimand, threshold or approval is changed by any item below |
| **Scientific values changed** | **None.** No D-number is created, amended or superseded |
| **Gates affected** | G-09, G-08, G-P2, G-P3C — **readiness only; no gate opened** |
| **Locked test accessed** | Access-log **row 9** added for the reviewing session's directory-listing read. No December record opened |

## Why this record exists

`GOV-2026-08-22-INC-01` found that the Inception artifact set was scientifically
sound — every blocking invariant verified — but that the 2026-08-22 amendment
wave had left **derived views frozen at four different points in one day's
sequence**. One governed figure, the mandated test-module count, stood at 17, 19,
20 and 21 in different artifacts simultaneously. A second, the untested-requirement
count, stood at 36 in its register and 40 in six live sites.

The gate verdict was **`FAIL`** on that basis, together with one missing authority
artifact (see § Recommendation 1 — not discharged). This record applies the ten
recommendations the owner approved for immediate action.

## What changed, by recommendation

### Rec 2 — Technical Environment §12 provenance block

`PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md`, §12.

- The "**Five** entries above were added by amendment" sentence is replaced by a
  statement that the table itself is the enumeration, with no restated total —
  the table carries **seven** rows, and two later same-day records each added one
  after the original figure was written.
- "none of the **six** newly approved **modules** exists" is corrected to "six
  newly approved **entries, five of them modules**", naming the five and
  identifying the sixth entry as `PYTHONHASHSEED` in §13.2 — an
  environment-variable setting, not a module. `tests/test_acquisition_window.py`
  is identified as the seventh row and as historical rather than newly approved.
- Both superseded sentences are preserved verbatim in place.

### Rec 3 — the test-module count, corrected to 21 everywhere reachable

Derived, printed before assertion:
`sed -n '675,703p' <TE> | grep -oE 'test_[a-z_]+\.py' | sort -u | wc -l` → **21**.

The count's history is 17 → 19 (`CR-2026-08-22-TE-AMEND`) → 20
(`CR-2026-08-22-TARGET-SCHEMA-TEST`) → 21 (`CR-2026-08-22-LEAKAGE-TA`). Every
value was correct once.

- `requirements.md` **REQ-ENG-4**: the row's lead already read 21; its body read
  "all nineteen are now enumerated" and "The tree reached nineteen by two
  amendments". Corrected to twenty-one and four amendments, with the three
  amending records named and both superseded phrases preserved. The row now also
  states that **18 of the 21 are unwritten**, only
  `test_acquisition_window.py`, `test_phase_boundary.py` and
  `test_release_hashes.py` existing.
- `unit-of-work.md`, three sites: the ADR-10 bullet, the `RES-02` register row,
  and the `RES-02` narrative status. All corrected to 21, superseded text
  preserved. The narrative's claim that "the 17-versus-19 question is settled in
  the authority documents" is corrected to 17-versus-21.
- **Not changed here:** `team-practices.md` and
  `aidlc/spaces/default/memory/team.md`. `org.md` reserves both for the
  practices-affirmation gate. Routed there under Rec 8.

### Rec 4 — `CR-2026-08-22-TARGET-SCHEMA-TEST` arithmetic

`governance/CHANGE_RECORD_2026-08-22_leakage_ta_and_schema_test.md`. That file
states at its head that both of its amendments are "recorded in one file because
both amend TE §12/§19 in the same act", then computed its totals over only one of
them.

- "The tree now enumerates **20** test modules" → **21**, with a boxed arithmetic
  correction explaining that the omitted module,
  `tests/test_feature_leakage_guards.py`, is added by the record's own other half.
- "All **19** prior modules are flat under `tests/`" → **20**.
- "TE §12 `test_*.py` entries after the amendment: **20**, enumerated" → **21**
  after *both* amendments, with the derivation command printed.
- Superseded figures preserved at each site.

### Rec 5 — the untested count, and the mechanism

Derived: 36 rows carry `UNTESTED` in the requirement tables' test-row column.

Corrected 40 → 36 at four delivery-planning sites: `bolt-plan.md` (two),
`risk-and-sequencing-rationale.md` (one), and
`delivery-planning-questions.md` (one, rendered as "40 when this question was
written, 36 since `CR-2026-08-22-LEAKAGE-TA`" because the sentence is a record of
a question asked at a point in time). The two sites in
`phase-check-inception.md` are corrected under Rec 6.

**Mechanism.** `governance/CHANGE_RECORD_PROCEDURE.md` is created, requiring every
future change record that amends a count, enumeration, ID range, cardinality or
status to name the superseded literal, sweep the governed trees for it, record
the sweep result with each site's disposition, check its own arithmetic against
its own full scope, and re-derive rather than decrement. It also names the files a
sweep may report on but never edit.

### Rec 6 — the phase-boundary certificate, reissued

`verification/phase-check-inception.md`. The superseded version is preserved
verbatim at `phase-check-inception.superseded-2026-08-22.md`.

Every count re-derived at the current artifact state:

| Measure | First issue | Reissue | Derivation |
|---|---|---|---|
| Requirement IDs defined / assigned | 105 / 105 | **105 / 105** | row-lead extraction, both files, set difference empty both ways |
| Units / dependency edges | 12 / 23 | **12 / 23** | `- name:` entries; sum of `depends_on` members |
| Acceptance rows in Table 2 | 40 (13 WS + 27 TA) | **44 (13 WS + 31 TA)** | `WS-nn` / `TA-nn` row leads, sorted unique |
| Rows with an evidence-producing unit | 39 | **43** | 44 minus rows whose unit column reads `(none` |
| Requirements with no acceptance row | 40 | **36** | `NO CURRENT ACCEPTANCE ROW` occurrences |
| Mandated modules testing post-`acquisition` units | 16 of 19 | **18 of 21** | TE §12 tree enumeration |

The acceptance figures moved in opposite directions for one reason: TA-33–TA-36
raised the mapped rows to 44 and simultaneously removed four requirements from
the untested list. The reissue states explicitly that those four now have an
acceptance criterion but **no implemented test, no execution and no pass**.

**No verdict or conclusion changed.** Checks 1, 2, 3, 5 pass; Check 4 passes on
traceability and fails on completeness against a smaller but identical gap; Check
6 passes; Check 7 hands forward the same six blockers.

### Rec 7 — stage 2.7 blocker register annotated in place

`unit-of-work.md`. The board itself split on whether a completed stage's artifact
may be annotated after its gate; the owner settled it for annotate-in-place,
following the 2026-08-22 precedent. **No blocker is closed outright and the count
of open blockers remains six.**

- **BLK-02** station limb discharged by **D-20**; `fixture_manifest.yaml` limb open.
- **BLK-05** naming and documentation limbs discharged
  (`CR-2026-08-22-TARGET-SCHEMA-TEST`); implementation and execution limbs open.
- **BLK-06** enumeration limb discharged by **D-24**; per-item config binding and
  implementation open, so BLK-06 still blocks G-P2 and G-P3C.
- **BLK-03, BLK-04, BLK-07** unchanged and open.
- **`RES-03` narrative bullet reconciled with its own register row.** The bullet
  read "FR-P1-06-1 still requires… a fourteen-item enumeration" while the table
  row for the same item already recorded the derivation complete and the
  amendment applied 14 → 17. The bullet now records D-24, the
  `CR-2026-08-22-PROTECTED-SET` amendment, and the genuinely open limbs.

### Rec 8 — affirmed practices routed to their own gate

The four modules absent from `team-practices.md` § Testing Posture's 17-item list
are named, derived by set difference against TE §12's 21:
`test_acquisition_window.py`, `test_determinism.py`,
`test_prepared_target_schema.py`, `test_feature_leakage_guards.py` — **three of
them leakage, determinism and schema controls.**

`team-practices.md` and `memory/team.md` are **not edited**: `org.md` reserves
them for the practices-affirmation gate, and stage 2.8 was correct to refuse.
What is applied here is the second limb: **`RES-02`'s closure target is corrected
from 19 to 21** in `unit-of-work.md`, so that closing RES-02 as written will no
longer leave two modules unaccounted for.

### Rec 9 — locked-month access log

`evidence/experiment_registry.md` § Locked-month access log gains **row 9**,
recording the reviewing session's `ls` of `evidence/locked_test_restricted/` —
five directory-entry names, nothing opened, nothing computed. Narrower in scope
than row 8, which also read manifest contents.

Marked **retrospective**: logged after the read, the same ordering defect rows 5
and 8 record, and the row does not repair it. The board disclosed the access in
its own report and did **not** write the row itself; it was written on the owner's
approval. The "Rows 3, 4, 5 and 8 are retrospective" paragraph is updated to five.

The owner approved option 1 only, so **no standing pre-declaration rule** for
future reviewer access was adopted. The enforcement gap itself — that
`evidence/locked_test_restricted/` is a declared location rather than an enforced
control, reachable by any recursive traversal from `evidence/` — remains carried
as **`RES-04`**, due before G-05.

### Rec 10 — the claims-boundary requirement gains a row

`requirements.md` gains a new subsection, **§ Vision §11.2 claim-boundary
requirement**, carrying `REQ-CLAIM-01` with a pass/fail criterion. Placed in its
own table rather than in the eleven-row TE §11 adoption table, because
`REQ-CLAIM-01` is a Vision §11.2 ID adopted unchanged and not a TE §11 NFR — that
table's count and provenance are untouched.

**The criterion is referenced, not duplicated.** The prohibited-class enumeration
remains maintained solely in § Out of scope C, where it already existed in full;
copying it would have created exactly the drift this record exists to correct.
`REQ-CLAIM-01` remains **`UNTESTED`** — adding a criterion is not adding a §16 or
§19 acceptance row, and creating one is a Vision §15.2 amendment not made here.

**Effect on counts, derived:** requirement-definition rows 104 → **105**, matching
the 105 distinct IDs every artifact already reported, so no other count moves.
The untested total stays **36** and becomes **fully derivable from the test-row
column** for the first time — previously `REQ-CLAIM-01` had no row and had to be
added by hand. Both the crosswalk row and the § Traceability row are re-pointed.

### Rec 11 — deferred to stage 3.1, nothing changed here

The IRI **import-boundary** check has no owning §12 module (self-recorded at
`component-dependency.md` § Assumptions, origin `IMPL-13`). Stage 2.6 was correct
to record the authority-level silence rather than invent a module.

**Carried obligation for stage 3.1 (`functional-design`), due before G-04:**
assign the import-boundary check explicitly to `tests/test_iri_denial.py` and
extend that module's TE §12 comment to name **both** limbs — the data-flow limb
(`iri_*` fields reaching ML, which the comment states today) and the module-graph
limb (`src/external/iri.py` / `gim.py` imported from `src/features/` or
`src/models/`, which it does not). This clarifies an existing module's scope
rather than adding one. **No Inception artifact is changed under this item.**

## Recommendation 1 — NOT DISCHARGED

**`GOV-2026-08-22-DP-01` is still missing.** The owner approved **option 1** —
recover the report from the session transcript that produced it and persist it
unmodified at `governance/reviews/GOV-2026-08-22-DP-01.md`.

**That option could not be executed.** The report was produced in an earlier
session, and the remediating agent has no access to that transcript. The report
was **not reconstructed**: fabricating a governance record — even from the change
records that applied its findings — would manufacture the very evidence the audit
chain exists to provide, and would be circular as proof that the applied changes
were the ones recommended.

The citation footprint stands unchanged at **16 citations across 11 files**,
including the Technical Environment (precedence level 2) and five change records
(precedence level 3). The five finding IDs cited but unreadable are `DP-CHAIR-01`,
`DP-CHAIR-02`, `DP-CHAIR-04`, `DP-ML-01` and `DP-BENCH-01`.

**Open action for the owner:** supply the transcript so option 1 can complete, or
authorise the approved fallback — **option 2**, a labelled provenance-gap record
that states the report is lost, lists the five finding IDs, and reconstructs each
finding's substance from the change records that applied it, explicitly marked a
reconstruction and never as the original. **Until one of these completes, the
`FAIL` verdict of `GOV-2026-08-22-INC-01` stands.**

## Verification

- Requirement-definition rows: **105**; distinct IDs: **105**; rows carrying
  `UNTESTED`: **36** — each derived and printed, not carried.
- TE §12 `test_*.py` entries: **21**, enumerated.
- Units **12**; dependency edges **23**; acceptance rows **44** (13 WS + 31 TA);
  rows with no evidence-producing unit **1** (TA-24).
- Every count in this record was recomputed from the artifact after the edits,
  per `governance/CHANGE_RECORD_PROCEDURE.md` step 5.
- **Sweep result** (procedure step 3): the literals `40 untested`, `40 of 105`,
  `19 mandated`, `of the 19` and `fourteen-item` were searched across
  `PreFlight/`, the active intent tree, `evidence/` and `governance/`. All live
  assertions corrected; all remaining occurrences are explicitly labelled
  superseded or are historical revision notes. Two sites reported and **not**
  edited: `team-practices.md` and `memory/team.md`, both reserved to the
  practices-affirmation gate and tracked as `RES-02`.

## Files changed

| File | Change |
|---|---|
| `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` | §12 provenance block: two count corrections (Rec 2) |
| `aidlc/.../requirements-analysis/requirements.md` | REQ-ENG-4 body (Rec 3); § Intent analysis — removed a trailing "total is 19 / remainder is 16" fragment that contradicted the corrected clause in the same parenthesis (Rec 3); new `REQ-CLAIM-01` subsection, crosswalk and traceability rows, untested-list note (Rec 10) |
| `aidlc/.../units-generation/unit-of-work.md` | three count sites (Rec 3); RES-02 closure target (Rec 8); blocker annotations and RES-03 reconciliation (Rec 7) |
| `aidlc/.../delivery-planning/bolt-plan.md` | two count sites (Rec 5) |
| `aidlc/.../delivery-planning/risk-and-sequencing-rationale.md` | one count site (Rec 5) |
| `aidlc/.../delivery-planning/delivery-planning-questions.md` | one count site (Rec 5) |
| `aidlc/.../verification/phase-check-inception.md` | reissued with all counts re-derived (Rec 6) |
| `aidlc/.../verification/phase-check-inception.superseded-2026-08-22.md` | **new** — superseded certificate preserved verbatim |
| `evidence/experiment_registry.md` | access-log row 9 and the retrospective paragraph (Rec 9) |
| `governance/CHANGE_RECORD_2026-08-22_leakage_ta_and_schema_test.md` | three arithmetic corrections (Rec 4) |
| `governance/CHANGE_RECORD_PROCEDURE.md` | **new** — propagation-sweep procedure (Rec 5) |
| `governance/CHANGE_RECORD_2026-08-22_INC_corrections.md` | **new** — this record |

**Not changed, deliberately:** `aidlc-state.md` and every lifecycle field
(governance never mutates AI-DLC state); `team-practices.md` and
`memory/team.md` (reserved to the practices-affirmation gate);
`aidlc/.../application-design/*` (no finding required a change);
`evidence/DECISIONS.md` (no D-number created or amended);
`governance/reviews/*` (prior reports preserved unchanged).
