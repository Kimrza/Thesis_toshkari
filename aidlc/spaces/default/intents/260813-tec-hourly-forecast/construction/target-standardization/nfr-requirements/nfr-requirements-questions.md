# NFR Requirements — Questions — `target-standardization`

**Unit** `target-standardization` (Bolt 6) · **Kind** `library` · **Stage** `nfr-requirements`

Two artifacts only — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit.

**Not re-asked, because `functional-design` already decided them.** The closed set of
**exactly four** transformations, with a fifth a **failure** (R-64, W-2, Q7 = D); the
aggregation statistic resolving to **D-16**, never to a default (R-65); the target row
carrying exactly **D-17's sixteen fields** (R-66, W-3); the excluded set asserted and never
substituted (R-67); the support thresholds being **D-19's**, carrying their basis (R-68);
**three definition IDs on every artifact** (R-70); data quality's four contents with
"unexplained" doing the work (R-71); the uncertainty budget stating its bounds rather than
truncating (R-72); **one `02` script per run, selected by `--phase`**, asserted by the
clean-run contract (R-73, W-6, Q4 = C).

**Carried, not decided here.** The `02` ordinal collision is a **recorded §12 defect, not a
resolved one**, and `code-generation` **must not invent a `02a`/`02b` convention**. Whether
`02_build_vtec_target.py` is unreachable under `--phase 1` is a **phase-boundary** question
belonging to `governance-guards` R-23 — **noted for that unit rather than guarded twice**.

---

## Question 1

W-2 records that three of the four permitted transformations are fully specified — UTC
normalization, cell selection under D-1's half-open floor rule, and D-16's median hourly
aggregation. The fourth, **"documented QC"**, is *"named by FR-P1-03-1 and defined nowhere
in scope"*, and W-2 states plainly that this **defeats the closed-set claim as first
stated**: a diff can only fail on a fifth transformation if it can attribute every observed
change to one of four **known** operations.

W-2's fix is to enumerate the QC operations as a **named list in `configs/data.yaml`**, so
that an operation outside the list fails as a fifth transformation would.

The question this stage must answer is what that enumeration **is**, governance-wise. A QC
operation changes target values.

A. The QC list is a **scientific constant** and must be frozen under a **D-number** before any implementation reads it; until then it is `TBD — freeze gate` in `configs/data.yaml`
   > **Impact**: Treats a value-changing choice the way TE §18.2 treats every other one, and keeps the sentinel visible to the §18.3 zero-TBD preflight. It blocks the closed-set mechanism — and so FR-P1-03-1's whole criterion — until a decision the supervisor and student must make, which may be later than the code is wanted.

B. The QC list is a **configuration structure** this stage may enumerate now, with each entry's *parameters* left as freeze-gate values
   > **Impact**: Unblocks the mechanism immediately: the closed set exists and fails on an unlisted operation even while a threshold inside one entry is still `TBD`. The distinction between "which operations" and "with what parameters" is one this stage would be drawing itself, and picking which operations are permitted is already a scientific act.

C. Leave the QC list to stage 3.5 with a note that it must be enumerated before use
   > **Impact**: Defers to where the code is written. `project.md` records deferring a gating condition's inputs as leaving the condition unmeetable, and W-2 has already established that the closed-set claim fails without this list — so 3.5 would inherit a mechanism that cannot work and no authority to fix it.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — which QC operations may touch the target is a choice that changes target values, and TE §18.2 is unambiguous that no implementer or coding agent fills such a value by convenience. Option B's split is attractive but the line it draws is the very thing in dispute: an operation admitted to the list is admitted to changing values, parameters or not. The honest cost of A is that FR-P1-03-1's closed-set criterion is **blocked on a freeze-gate decision**, and that should be visible now rather than discovered at 3.5.

[Answer]: A

---

## Question 2

R-69 requires the **label and the lineage caveat** to travel with the product, and W-5
carries **two mismatch disclosures** — that the Phase 1 target is **location-sampled gridded
VTEC** and never receiver-specific station-observed VTEC, and that part of any IRI or GIM
difference is a **geometry and sampling artefact rather than skill**.

Nothing states whether these travel as **documentation** or as **data**.

A. Machine-carried: the caveat is a **field on the artifact** — alongside `target_definition_id` — that every consumer reads, and a consumer that reports a comparison without it **fails**
   > **Impact**: Makes the disclosure impossible to lose in transit between units, and gives the "state the mismatch wherever a comparison is reported" rule an enforcement point rather than an instruction. It obliges every downstream consumer to handle a field it did not ask for, which is a cross-unit imposition this stage can only state one half of.

B. Documentary: the caveat lives in the product's manifest and the reporting units are required to reproduce it
   > **Impact**: No cross-unit code obligation, and the manifest is already where provenance lives. It relies on each reporting unit remembering, which is exactly how a caveat travels less far than the number it qualifies — a failure this project has already recorded happening.

C. Both — a machine-carried field, and the requirement on reporting units stated independently so neither depends on the other
   > **Impact**: Strongest, and matches the two-limb pattern used for the phase boundary and now for NFR-IRI-01. It is also the most work, and duplicating an obligation in two places is how two statements of one fact drift apart — a risk W-6 names explicitly in this unit's own artifacts.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the mismatch disclosure is mandatory under Vision §6.6 and the project has already recorded that VAL-05's Phase 2 disclosure was **absent from every stage artifact** when it was checked, which is the evidence that documentary-only travel does not survive contact with a pipeline. Option C's duplication risk is real and W-6 names it in this unit's own words: two rules about one fact is how they drift apart. The cross-unit cost of A must be stated as a half-contract, exactly as `external-products` states its NFR-IRI-01 limb.

[Answer]: A

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. Nothing below decides a
scientific value, and nothing claims a gate or acceptance row is discharged.

**Scope.** Two artifacts — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit. Those categories are still
assessed in the security artifact's scope note.

**Q1 = A — the QC operation list is a scientific constant and stays `TBD — freeze gate`.**
Which QC operations may touch the target is a choice that **changes target values**, so it
is frozen under a **D-number** before any implementation reads it, and the sentinel stays
visible to the §18.3 zero-TBD preflight. **The consequence is stated, not softened:**
FR-P1-03-1's closed-set criterion — *"only the documented transformations"* — is **blocked
on that freeze**, because W-2 has already established that a diff can only fail on a fifth
transformation if it can attribute every observed change to one of four **known**
operations, and *"documented QC"* is defined nowhere in scope. Three of the four are fully
specified (UTC normalization; D-1's half-open floor cell selection; D-16's median hourly
aggregation); the fourth is not.

**Q2 = A — the label and lineage caveat travel as data.** The caveat is a **field on the
artifact**, alongside `target_definition_id`, and **a consumer that reports a comparison
without it fails**. This gives Vision §6.6's "state the mismatch wherever a comparison is
reported" rule an enforcement point rather than an instruction; the evidence that documentary
travel does not survive a pipeline is VAL-05's Phase 2 disclosure, found **absent from every
stage artifact** when it was checked. **The cost is stated as a half-contract:** downstream
consumers must handle a field they did not ask for, and **this stage states only this unit's
half**.

**The two disclosures the caveat carries.** That the Phase 1 target is **location-sampled
gridded VTEC** and is **never** receiver-specific station-observed VTEC; and that part of any
IRI or GIM difference is a **geometry and sampling artefact rather than skill**. **No claim
of numerical equivalence** between the Phase 1 and Phase 2 targets is permitted.

**Carried, not re-decided.** R-64's closed set of **exactly four** transformations with a
fifth a failure; R-65's aggregation statistic resolving to **D-16**, never a default; R-66's
**sixteen D-17 fields**; R-67's asserted, never-substituted excluded set; R-68's **D-19**
support thresholds with their basis; R-70's **three definition IDs on every artifact**;
R-71's four data-quality contents; R-72's uncertainty budget stating its bounds rather than
truncating; R-73's **one `02` script per run selected by `--phase`**, asserted by the
clean-run contract.

**Status claims made.** None. The **`02` ordinal collision is a recorded §12 defect, not a
resolved one**, and `code-generation` **must not invent a `02a`/`02b` convention**. Whether
`02_build_vtec_target.py` is unreachable under `--phase 1` belongs to `governance-guards`
R-23 and is **noted for that unit rather than guarded twice**. G-09 is signed (D-31) with its
preconditions UNMET; stage 3.1 remains FAIL; no Python interpreter exists here, so every test
is written-but-unexecuted or unwritten.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
