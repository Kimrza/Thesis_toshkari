# CR-2026-08-28-LOCKED-SCORED-SET — EXECUTED (record only)

**Status:** **EXECUTED 2026-08-28** for the record it creates. No authority document,
no approved upstream artifact and no memory layer was edited by this record; every
such site is listed below with its disposition and its owner.

**Authorized by** the project decision owner, 2026-08-28, at the `functional-design`
(3.1) governance gate, on governance report `GOV-2026-08-28-FD-01` Recommendation 6 —
ruling: *ratify now*, with the authority conflict disclosed.

**Decision created:** **D-28** — the G-06 locked-test scored set is 2–31 December 2022
(30 days), the first 24 hours excluded and counted. Written to
`evidence/DECISIONS.md` as a full entry plus a countersignature-status register row.

---

## Vision §15.2's six fields

| Field | Value |
|---|---|
| **1. What changed** | The G-06 locked-test scored set is fixed at **2–31 December 2022, 30 days**, with the first 24 h of the locked month excluded and counted. This ratifies stage-3.1 answer **FU-7 = A** (2026-08-26) and records it as a decision; it does not alter the operative value the eight consuming units already encode. |
| **2. Why** | ADR-11 (2026-08-23) removed `lead_in_hours`, the mechanism that let a window cross the November/December boundary. `requirements.md` FR-P1-04-5 states that no window crosses a boundary and that the first 24 h are excluded and counted. Without a lead-in, 1 December's window cannot be built from within December. FU-5 = D (2026-08-24) had ruled the opposite — *"the locked-test prediction covers the full December, 1–31, with no first-day loss"* — but was decided against the interface ADR-11 had retired the day before. |
| **3. What it supersedes, verbatim** | **FU-5 = D's clause:** *"the point where **G-06** is described records that the locked-test prediction covers the **full** December with no first-day loss."* Superseded, retained as dated history in `features-and-splits`. |
| **4. Whether the locked test has been accessed** | **Yes — before this change, and the history is disclosed rather than repaired.** `evidence/experiment_registry.md` § Locked-month access log carries nine rows, of which **rows 3, 4, 5, 8 and 9 are marked retrospective** ("the rows did not exist before the reads, and no row can be made to have preceded them"); row 6 (2026-08-21) is the first logged in advance. § Evidence gap records the 2026-08-21 test-suite run as a governance finding, concluding *"highly likely on the code path and unproven in execution"*, and states at line 110: **"Whether the 2026-08-21 run constituted an unauthorized December access is not resolved here."** No access read December **performance**; no model, prediction or metric exists. This record does not close that question — see governance report Recommendation 31. |
| **5. Authority relied on** | `requirements.md` FR-P1-04-5; `component-methods.md` ADR-11; the recorded student/supervisor authority equivalence (`evidence/DECISIONS.md` D-1 addendum; `CR-2026-08-22-TE-AMEND`; `GOV-2026-08-22-REM-01` Rec 4). **Vision §15.1 places "test dates" under "Supervisor: Approval required", and no supervisor signature artifact exists or is claimed.** |
| **6. Residual obligations** | A **revised split manifest** is owed at G-05 (Vision §8.2). The authority conflict below is carried to G-05 unresolved. `REQ-CLAIM-01`'s boundary text still reads "December 2022 only" and is owed either an owner-approved annotate-in-place or a Vision §15.2 amendment. |

---

## The authority conflict this record discloses rather than resolves

Both level-1 and level-2 authorities carry, byte-exact and identically:

```
| Locked test | — | — | December 2022 only |
```

`PreFlight/vision_document(3)(2)(2).md:751` and
`PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md:400`. Both assign
F1–F4 an explicit `24 hours` embargo and assign the Locked-test row **`—`**. The
boundary protection those tables name is the **frozen manifest**, on the Final refit
row — not a 24-hour exclusion.

`requirements.md` FR-P1-04-5 is a **level-4** artifact. It states the 24-hour embargo and
the excluded-and-counted rule, cites as its source the very tables carrying `—`, and its
own acceptance criterion requires the split manifest to enumerate **"all five
partitions"** — which excludes December from the five. **A level-4 paraphrase is
therefore the sole textual basis for the 30-day reading.** The Review Chair seat graded
this a BLOCKER on the authority route; the Validation Auditor seat, whose exclusive
domain it is, held the recorded equivalence sufficient and the record the only defect.
Both readings are in D-28 and in `GOV-2026-08-28-FD-01` § Reviewer disagreements.

**Neither authority document was edited.** Amending Vision §8.2 or TE §7.1 is a Vision
§15.2 act reserved to the supervisor, and this record does not perform it.

---

## Propagation sweep — per `CHANGE_RECORD_PROCEDURE.md` steps 1–5

**Step 1 — superseded literals named.** `"no first-day loss"`, `"full December"`,
`"December 2022 only"` (as an unqualified scored-set statement), and `"31 days"` /
`"1–31"` where used of the scored set.

**Step 2 — swept.** 236 Markdown files under `PreFlight/`,
`aidlc/spaces/default/intents/260813-tec-hourly-forecast/`,
`aidlc/spaces/default/memory/`, `evidence/` and `governance/` including this record.
Command shape: a Bun walk over those roots matching each literal and printing per-file
counts, run 2026-08-28.

**Step 3 — every site found, with disposition.**

| Literal | Site | Count | Disposition |
|---|---|---|---|
| `December 2022 only` | `PreFlight/vision_document(3)(2)(2).md` | 1 | **Not edited — authority document.** Conflict disclosed in D-28; carried to G-05. Owner: Supervisor (Vision §15.2). |
| | `PreFlight/Technical_Environment...(1)(2).md` | 1 | **Not edited — authority document.** Same disposition. |
| | `<record>/inception/requirements-analysis/requirements.md` (`REQ-CLAIM-01`) | 1 | **Not edited — completed-stage artifact.** Owed: owner-approved annotate-in-place, or a §15.2 amendment to read "30 of the 31 days of December 2022 (2–31, first 24 h excluded)". This is the **maintained source** of the boundary text and will otherwise keep re-seeding the 31-day reading. Governance report Recommendation 16 option (3). |
| | `<record>/inception/units-generation/unit-of-work.md` | 1 | **Not edited — completed-stage artifact.** Recorded as owed with the same route. |
| | `<record>/inception/delivery-planning/bolt-plan.md` | 1 | **Not edited — completed-stage artifact.** Recorded as owed. |
| | `aidlc/spaces/default/memory/project.md` (§ Mandated) | 1 | **Not edited — memory layer.** `org.md` reserves it for the practices-affirmation gate and `CHANGE_RECORD_PROCEDURE.md` § "Files a sweep may not edit" forbids it. Recorded as a **residual obligation on the practices gate**, on `RES-02`'s precedent. |
| | `<record>/construction/regimes-diagnostics-reporting/.../business-logic-model.md` | 1 | **In-stage; corrected under the 3.1 remediation** (Recommendation 16 — the scored-window statement reaches the claim surfaces). |
| | `evidence/DECISIONS.md` | 3 | **Correct as-is.** Two are D-8's and D-13's own frozen text quoted as authority; the third is D-28's own disclosure of the conflict. |
| | `governance/reviews/GOV-2026-08-28-FD-01.md` | 3 | **Correct as-is** — the board's own quotation of the conflict. |
| `no first-day loss` | `<record>/construction/features-and-splits/.../business-logic-model.md` | 5 | **Correct as-is.** All five are quoted-as-superseded inside dated boxes (`:679`, `:693`, `:1708`) or FU-mapping records. Verified by reading each line. |
| | `.../features-and-splits/.../domain-entities.md` | 1 | **Correct as-is** — `:370` quotes it as superseded and states the 30-day outcome. |
| | `.../features-and-splits/.../functional-design-questions.md` | 3 | **Correct as-is** — the receipted interview record of FU-5 and FU-7. |
| | `<record>/construction/functional-design/memory.md` | 1 | **Correct as-is** — the stage diary's record of the conflict. |
| | `evidence/DECISIONS.md` | 1 | **Correct as-is** — D-28's field 3, quoting the superseded clause as this procedure's step 1 requires. |
| `full December` | `.../features-and-splits/.../business-logic-model.md` | 2 | **Correct as-is** — both inside dated superseded boxes. |
| | `.../features-and-splits/.../domain-entities.md` | 1 | **Correct as-is** — quoted as superseded. |
| `2–31 December` | 20 files across `evaluation-and-comparison`, `features-and-splits`, `fixtures-and-reproducibility`, `regimes-diagnostics-reporting`, `statistical-inference` and this record's siblings | 30 | **Correct as-is — this is the new value, already propagated.** D-28 ratifies rather than changes it. |
| `31 days` | `.../evaluation-and-comparison/.../functional-design-questions.md` | 1 | **Correct as-is** — states the 30-of-31 relationship. |
| | `.../features-and-splits/.../business-logic-model.md` | 1 | **Correct as-is** — inside a dated superseded box. |
| | `<record>/inception/application-design/component-methods.md` | 1 | **Correct as-is** — ADR-11's own stated consequence, which is the basis of D-28. |
| | `<record>/inception/application-design/application-design-questions.md` | 1 | **Correct as-is** — Q14's receipted record. |
| | `evidence/DECISIONS.md` | 1 | **Correct as-is** — D-28's arithmetic ground. |
| | `governance/reviews/GOV-2026-08-28-FD-01.md` | 7 | **Correct as-is** — the board's analysis. |

**One Open item is closed by D-28 and must be updated in-stage:**
`.../features-and-splits/.../business-logic-model.md:1152` reads *"**Open** — FU-5 = D's
December consequence conflicts with ADR-11's `lead_in_hours` removal (two owner
decisions)"*. D-28 resolves that conflict. Corrected under the 3.1 remediation.

**Step 4 — arithmetic checked over this record's whole scope.** This record carries one
amendment (the creation of D-28) and states three figures, each computed over that whole
scope: **30** scored days (2–31 December inclusive = 31 − 1); **720** scored hours
(30 × 24); block counts **30** at 24 h and **15** at 48 h (720 ÷ 24, 720 ÷ 48, both
exact). The superseded reading gives 744 hours, and 744 ÷ 48 = 15.5 — **not exact**,
which is the independent arithmetic ground recorded in D-28.

**Step 5 — re-derived, not decremented.** Every figure above is computed from the
calendar boundary rather than adjusted from the size of the change. The 3.2% coverage
reduction is 72 ÷ 2,232 station-hours, where 2,232 = 31 × 24 × 3 and 72 = 1 × 24 × 3.

---

## What this record does not do

- It does not resolve the Vision §8.2 / FR-P1-04-5 conflict. That is carried to G-05.
- It does not amend any authority document, any completed-stage artifact, or any memory
  layer. Six such sites are recorded above as owed, each with its owner and route.
- It does not close the December access-history question (field 4 above; governance
  report Recommendation 31).
- It does not produce the revised split manifest Vision §8.2 requires. No manifest
  exists yet; the obligation attaches at G-05.
- It claims no supervisor signature.
