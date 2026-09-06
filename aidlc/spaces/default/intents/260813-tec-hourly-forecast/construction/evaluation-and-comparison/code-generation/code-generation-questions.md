# Code Generation Questions — `evaluation-and-comparison`

**Unit** `evaluation-and-comparison` (Bolt 9) · **Kind** `library` · **Stage** `code-generation`

This unit owns **BLK-08** (the `ABL-DIFF` inverse edge) and inherits BLK-03, BLK-04 and
BLK-09. BLK-04/BLK-09 were approved 2026-09-05 (`CHANGE_RECORD_2026-09-05_R74_R83_leakage_contracts.md`)
and BLK-03 was approved 2026-09-06 (`CHANGE_RECORD_2026-09-06_BLK03_confirmatory_contract.md`),
so the contracts every metric here inherits now exist. BLK-08's mechanism limb is still open:
R-103's edge `src/evaluation` → `src/features` is "an amendment owed and a gate item, not
approved" (D-27: *"no import-boundary change is authorised"*), and the owner's ruling FU-2 = B
at the `models-and-baselines` pass (reopen D-27 by a new D-number first) has no D-number on
disk yet. Six items are rulings rather than defaults (TE §18.3 stop-and-report), because each
is either a scientific confirmation the design explicitly routed to the gate or a cross-unit
ownership question no design fixed.

**Recorded input (human ruling, 2026-09-05)**: this unit's terminal READY nfr-design reviews
(2026-09-04 and the 2026-09-05 post-gate repair verification) carry **three Minors**, listed
here so the plan states per Minor what the code does: (1) the present-tense "proven once /
proven per entry point" over-claim in SD-C-01 — record-only in prose; the code makes it true
by shipping one negative control per public entry point; (2) the SD-C-02 read-then-write
sequence with no stated atomicity — this unit's half (`require_locked_receipt`) reads only
completed artifacts and refuses on absence, so no race is introduced here; the co-owner's
write half is `governance-guards`' and stays a gate item; (3) the illustrative
negative-control sentence not extended to the sixth guard — record-only; the sixth guard's
control is built regardless.

---

## Question 1
**Comparison-set membership (R-106, `domain-entities.md` § 1).** Three declared sets were
PROPOSED at functional-design "for confirmation at the gate — a scientific choice this stage
may propose but not make": **primary** {`M-01`, `M-02`, `M-03`, `M-06`, `B-01`}, **GIM**
{`M-06`, `C-01`}, **tier-3** {`M-04`, `M-05`, `M-06`} (Recommendation 19, owner-ruled
2026-08-28). `experiment.yaml` carries no `comparison_sets` today, and its own rule is that
only values frozen under an approved D-number are transcribed. `evidence/DECISIONS.md` has no
D-number for the memberships. How do the sets reach configuration?

A) Confirm the three sets as proposed, and GATE their transcription on a D-number you write in `evidence/DECISIONS.md` (proposed text supplied in this unit's change record); until it exists `comparison_sets` is `TBD — freeze gate`, the mask builder refuses naming it, and the tests exercise synthetic declared sets
   > **Impact**: Keeps the "D-number before transcription" discipline the configs state; `07` cannot build a real mask until you write the decision, which is the same posture as every other unfrozen value. Same gate pattern as the `models-and-baselines` Step 7 (it stopped, because the D-number was absent).

B) Confirm the three sets and transcribe them now into `experiment.yaml` citing this receipted ruling, Vision §2.4's tiers and R-106 as authority — no D-number
   > **Impact**: The masks become buildable this pass; but a scientific membership enters a governed config on a plan-question ruling rather than a decision-register entry, which team.md's "a decision is not real until it has a D-number" forbids. Not recommended.

C) Do not confirm; leave the sets open, `comparison_sets` stays TBD with no gate — the membership is ruled later
   > **Impact**: Identical code outcome to A today, but the confirmation the design routed to this gate goes unanswered again.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it answers the confirmation the design asked for and keeps the register the only place a scientific membership becomes real; the code is identical under A and C today, so A costs nothing extra and settles the science.

[Answer]: B

## Question 2
**BLK-08 / R-103 half A — the `ABL-DIFF`-only inverse gate** (`inverse_gate`, C4). The edge
`src/evaluation` → `src/features` is unauthorised (D-27) and your FU-2 = B ruling makes a new
D-number the precondition. What does this pass build?

A) GATED, as at `models-and-baselines` Step 7: `inverse_gate` is built as a fail-closed resolver — `resolve_inverse(transform_id)` raises `InverseTransformError` naming BLK-08, D-27 and the owed edge; `src/evaluation` imports nothing from `src/features`; R-104's boundary is real (`untransformed` and non-target-touching pass; target-touching without inversion lineage refuses). If, when the developer reaches the step, a D-number reopening D-27 exists on disk, the resolver is wired to `features-and-splits`' `load_inverse` (which then also needs building — its half B) and the edge is recorded; otherwise the step stops and reports
   > **Impact**: `ABL-DIFF` stays unexecutable until your decision exists — which is BLK-08 open, stated as a fact; every confirmatory-path metric is unaffected (D-27: the primary target is raw TECU). One gate, one file, no import until authorised.

B) Build the edge now
   > **Impact**: Contradicts D-27's recorded withholding and R-103's own "stage 3.5 may not treat it as approved"; the never-reopen rule requires your decision first. Not recommended.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it is the reading R-103 itself prescribes for 3.5, and it composes with FU-2 = B without pre-empting it.

[Answer]: B

## Question 3
**Module layout vs. the §12 tree and the one-guard-home rule.** `unit-of-work.md` § 9 `Owns`
and TE §12 name **two** modules here: `src/evaluation/masks.py`, `src/evaluation/metrics.py`
(plus `scripts/07_evaluate_and_report.py`, `tests/test_common_masks.py`).
`logical-components.md` proposes **six** (`guards`, `masks`, `estimand`, `inverse_gate`,
`locked_eval`, `honesty`), naming them "proposed to 3.5". `project.md` (nfr-design:c58)
requires every enforcement boundary to have exactly one guard home with one negative control
per entry point. Which layout?

A) Three modules: `masks.py` (C2), `metrics.py` (C3 estimand + C5 locked_eval + C6 honesty + C4 inverse gate as sections), and **`guards.py` as the single guard home** (C1's six refusals + the SD-C-02 containment check). ONE §12 naming amendment owed (`guards.py`), same class as `_frames.py` / `acquisition.py`
   > **Impact**: Honours the one-guard-home rule and the `Owns` list with the smallest naming deviation; `metrics.py` is large but sectioned. Every public entry point of `masks.py` / `metrics.py` calls into `guards.py` and gets its own negative control.

B) Two modules exactly as §12 names them: guards split between `masks.py` (mask-side refusals) and `metrics.py` (metric-side refusals)
   > **Impact**: No naming amendment, but two guard homes for one boundary — the drift class c58 exists to prevent (the R-105-vs-R-92 mismatch was that drift realised).

C) Six modules as `logical-components.md` proposes; four §12 naming amendments owed
   > **Impact**: Cleanest separation, largest deviation from the mandated tree; four amendment items instead of one.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — one guard home is a recorded project rule; one naming amendment is the price, and it is the same price two prior units already paid.

[Answer]: A

## Question 4
**Two homes for "the comparison mask".** `component-methods.md` places
`build_comparison_mask(predictions, *, benchmark) -> DataFrame` in `src/evaluation`. But
`features-and-splits` (READY, 2026-09-06) already built a `ComparisonMask` dataclass,
`build_comparison_mask(member_rows, *, comparison_set_id, identity)`, `_mask_id`,
`assert_mask_is_comparison_wide`, `write_mask`, `load_mask` in `src/features/windows.py` under
its own R-81 / SD-F-06. `src/evaluation` may not import `src/features` (D-27; no edge), so it
cannot reuse that object. How is the duplication handled?

A) `src/evaluation/masks.py` owns the approved-signature `build_comparison_mask(predictions, *, benchmark)`, the registry, `mask_id`, stamps, exclusion counts and the R-107 limb-6 reporting surface, with NO import from `src/features`; the features-side object is left as built and the two-homes fact is recorded in the change record as a gate item (which one is canonical is the owner's ruling; the design contracts point here)
   > **Impact**: This unit's contract is met as approved; a second mask implementation exists in a sibling module until the owner rules. Honestly stated: two `mask_id` derivations could diverge — the gate item names it.

B) Edit `src/features/windows.py` to remove or deprecate its `ComparisonMask` family (sibling module, READY unit)
   > **Impact**: One home, but a cross-unit edit to a reviewed module without that unit's re-check, and R-81 (features-and-splits' own rule) would lose its implementation.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — build what this unit's approved contract names, touch no sibling, and put the canonical-home ruling where it belongs.

[Answer]: A

## Question 5
**SD-C-02's containment fields on `AccessRecord`.** `require_locked_receipt` refuses a `DEC`
metric unless the access record carries `mask_bundle_ids` and `mask_registry_hash` and the
scored mask's id is in the bundle. `AccessRecord` in `src/data/locked_test.py`
(`governance-guards`, READY 2026-09-05) has seven fields and neither of these; populating
them at access time is the co-owner's half, "stated, not declared satisfied". What does this
pass do?

A) No sibling edit: `require_locked_receipt` reads the two fields if present and REFUSES (`LockedTestError`) when absent — fail-closed; the co-owner's half stays a gate item for `governance-guards`
   > **Impact**: G-06 cannot pass this guard until `governance-guards` adds and populates the fields — correct, since G-06 is signature-blocked anyway; ownership respected; the half-contract is stated in both directions in the change record.

B) Additive edit to `AccessRecord` (two optional fields) and to `open_restricted` (populate them from the mask registry) in `src/data/locked_test.py`, flagged for `governance-guards`' record
   > **Impact**: G-06's ordering check becomes runnable end to end this pass, at the cost of editing a reviewed sibling module and its exempt-set / literal-scan tests.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the design itself says the half is the co-owner's; a refusal that names the missing fields is the honest state.

[Answer]: B

## Question 6
**`estimand` in `experiment.yaml` is `TBD — freeze gate`.** R-108 fixes the estimand as an
ordered executable pipeline from already-mandated text (Vision §2.3; TE §1.3; `project.md`
§ Mandated: *benchmark minus model, equal-station weighting, positive favours the model*).
Transcribe the identities (`orientation: benchmark_minus_model`, `weighting: equal_station`,
the sign-convention sentence) now, citing those sources, so `EstimandResult` can assert
them from config? `practical_relevance_threshold` stays TBD regardless (PC-09; no value exists).

A) Transcribe the estimand identities now with citations; threshold stays TBD
   > **Impact**: A copy of mandated text, like the §8.6 settings; R-108's result object asserts its convention against config rather than a source literal. No scientific value is chosen.

B) Leave `estimand` TBD; the code holds the orientation/weighting as identity tokens in source and the config transcription waits
   > **Impact**: Identity tokens in source are arguably identities not values (the `REQUIRED_FIELDS_MAP` precedent), but the config surface stays incomplete and R-108's "assertable field" has no config to assert against.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the text is frozen in two governing documents and mandated in `project.md`; transcribing it is a copy, and it is what makes the convention checkable.

[Answer]: A

---

## Follow-up questions — the Q1 and Q2 answers contradict recorded rules

Both chosen options were marked "not recommended" for a stated reason; you chose them with
that reason in view. They are put back once, side by side with the record, so the ruling is
explicit and the record shows how it is honoured (stage protocol § 3; project.md § Way of
Working: a recorded refusal is reversed only by a new argument or an explicit human decision
that honours the original reasoning).

## Follow-up 1 (Q1 = B — transcribe the comparison sets now, no D-number)
Side by side with the record: `configs/data.yaml` and `experiment.yaml` state *"only values
frozen under an approved D-number are transcribed here, citing that D-number"*; team.md
§ Way of Working: *"a decision is not real until it has a D-number"*; the design itself
routed the three memberships to this gate as *"a scientific choice this stage may propose
but not make"*. Your ruling at this gate is the owner's decision; what is missing is its
register entry.

A) Transcribe now, with the gap stated in the file: `comparison_sets` enters `experiment.yaml` with `decision: "owner ruling 2026-09-06 at the evaluation-and-comparison code-generation gate (Q1 = B); D-number OWED"`, the change record records the ruling and carries the proposed D-number text for you to adopt, and a test asserts the transcription matches R-106's three sets exactly
   > **Impact**: Masks are buildable this pass; the config carries a visible non-D-number citation until you write the decision — an exception to the configs' own rule, recorded rather than hidden. If the D-number is never written, the gap stays visible at every gate.

B) Gate the transcription on your D-number (the Q1 = A posture): `comparison_sets` stays `TBD — freeze gate` until the register entry exists; tests use synthetic sets
   > **Impact**: No exception to the register rule; no real mask until you write the decision.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B keeps the register the only place a scientific membership becomes real. If you choose A, it is executed exactly as written above — as your recorded exception — and the D-number stays owed at every subsequent gate.

[Answer]: B

## Follow-up 2 (Q2 = B — build the `src/evaluation` → `src/features` edge now)
Side by side with the record: **D-27** (2026-08-24) — *"No import-boundary change is
authorised by this decision"*; R-103 — *"the edge is unauthorised until both a change record
and a gate ruling exist, and stage 3.5 may not treat it as approved"*; your own FU-2 = B at the
`models-and-baselines` pass (2026-09-06) — reopen D-27 by a new D-number FIRST — which has no
D-number on disk. This is the second time you have chosen to build it; the edge is useless
without the co-owner's half B (`load_inverse(transform_id) -> Inverse`, `touches_target`, the
round-trip control) in `src/features/transforms.py` — a READY sibling module.

A) Build BOTH halves now under an explicit change record: the record quotes D-27's reasoning (the primary target is raw TECU; the edge was withheld, not refused on the merits), states the new argument (`ABL-DIFF` is a mandated ablation that must inverse-transform before any metric; the edge is scoped to `ABL-DIFF`, the object exposes only `inverse(frame)`, no forward apply crosses it), records your ruling as the gate ruling R-103 required, and carries the proposed D-number text for you to adopt. Then: half B lands additively in `src/features/transforms.py` (`Inverse`, `load_inverse`, `Transform.touches_target`, the round-trip control in `tests/test_train_only_transforms.py`), flagged for `features-and-splits`' record; half A's `inverse_gate` imports it (the one authorised edge, one file); `component-dependency.md`'s amendment stays owed to the owner; `ABL-DIFF` becomes executable through R-104's boundary
   > **Impact**: `ABL-DIFF`'s inverse path exists end to end; cost is a cross-unit edit to a module reviewed READY this morning (its code summary becomes stale — flagged), an import edge the dependency matrix does not yet carry (amendment owed), and a D-number owed to you. Nothing on the confirmatory path changes (D-27's reading stands).

B) Build half A's resolver against a `load_inverse` that does not exist yet: the edge import is written but fails closed with `InverseTransformError` until half B lands in a later pass
   > **Impact**: Records the intent, executes nothing new; `ABL-DIFF` still has no inverse path.

C) Return to the gated posture (Q2 = A): no edge until the D-number exists on disk
   > **Impact**: Matches FU-2 = B as you ruled it at the previous unit; `ABL-DIFF` stays unexecutable until you write the decision.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: If you want the inverse this pass, Option A is the only form that honours the never-reopen rule — an explicit, recorded reversal with D-27's reasoning quoted and the new argument stated — and it is your decision to take. Option C is the safer default and matches your earlier ruling. B buys nothing.

[Answer]: A

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Q1 = B superseded by **Follow-up 1 = B** — the three comparison sets (primary {`M-01`, `M-02`, `M-03`, `M-06`, `B-01`}; GIM {`M-06`, `C-01`}; tier-3 {`M-04`, `M-05`, `M-06`}) are CONFIRMED as proposed, but their transcription into `experiment.yaml` is GATED on a D-number you write in `evidence/DECISIONS.md` (proposed text in the change record). Until then `comparison_sets` stays `TBD — freeze gate`, the mask builder refuses naming it, and the tests run on synthetic declared sets.
- Q2 = B superseded by **Follow-up 2 = A** — **your explicit, recorded reversal of D-27's withholding of the inverse edge**: the change record quotes D-27's reasoning (primary target raw TECU; edge withheld), states the new argument (`ABL-DIFF` is a mandated ablation that must inverse-transform before any metric; the edge is scoped to `ABL-DIFF`; the crossing object exposes only `inverse(frame)`), records this ruling as the gate ruling R-103 required, and carries the proposed D-number text for you to adopt (the D-number stays OWED). Then BOTH halves are built: **half B** additively in `src/features/transforms.py` (`Inverse` exposing only `inverse(frame)`, `load_inverse(transform_id) -> Inverse`, `Transform.touches_target`, and the round-trip control in `tests/test_train_only_transforms.py`) — a cross-unit edit to features-and-splits' READY module, flagged for that unit's record; **half A** in `src/evaluation` (`inverse_gate` section) importing `load_inverse` — the one authorised edge, one file, no forward `apply` crosses it; `ABL-DIFF` becomes executable through R-104's boundary; `component-dependency.md`'s amendment row stays owed to you. `models-and-baselines`' `ABL-DIFF` refusal is updated to route through the inverse once present.
- Q3 = A — three modules: `src/evaluation/masks.py` (C2), `src/evaluation/metrics.py` (C3 estimand, C5 locked_eval, C6 honesty, C4 inverse gate as sections), **`src/evaluation/guards.py` as the single guard home** (six refusals + SD-C-02 containment); one §12 naming amendment owed (`guards.py`).
- Q4 = A — `masks.py` owns the approved `build_comparison_mask(predictions, *, benchmark)`, the once-only registry, deterministic `mask_id`, stamps, per-station surviving and exclusion counts, the scored-window statement and the R-107 limb-6 reporting surface, with no import from `src/features`; the features-side `ComparisonMask` in `windows.py` is left as built and the two-homes fact is a gate item.
- Q5 = B — **additive edit to `src/data/locked_test.py`** (governance-guards' READY module, flagged): `AccessRecord` gains optional `mask_bundle_ids` and `mask_registry_hash`; `open_restricted` populates them from the frozen mask bundle's manifest when one exists (purpose `locked_evaluation`) — write half of SD-C-02; `require_locked_receipt` reads them and refuses when absent or non-verifying. The exempt-set / literal-scan tests must stay green.
- Q6 = A — `experiment.yaml` `estimand` gains the mandated identities (`orientation: benchmark_minus_model`, `weighting: equal_station`, the Vision §2.3 sign-convention sentence) citing Vision §2.3 / TE §1.3 / `project.md` § Mandated; `practical_relevance_threshold` stays `TBD — freeze gate`.
- Build set: `src/evaluation/{guards,masks,metrics}.py`, `scripts/07_evaluate_and_report.py` (six-step entry; reads predictions/benchmark/mask; receipt-before-metric on `DEC` via R-109 limbs 1–3 incl. the 2–31 December / 30-day assertion (D-28); no December read outside `open_restricted`; bootstrap and breakdowns NOT built here — statistical-inference's and regimes-diagnostics-reporting's, called only if present, otherwise refused by name), `tests/test_common_masks.py` (WS-16: stable `mask_id`, per-station counts, pairwise attempt fails, recomputed-different-id fails, limb-6 five values, matched-window assertion incl. on the tier-3 set) plus one negative control per public entry point of `masks.py` / `metrics.py` (Q2 = C at nfr-design), the three Minors addressed as stated above, `beats_model` field and the spatial-representativeness caveat emitted by the producing path, the GIM overlap-audit precondition, completeness refusal per declared set.
- Not built: any real mask or metric over real predictions (no predictions exist); the bootstrap; the report tables; December access. Smoke evidence only under the stdlib stand-in; ruff owed; no commit.

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Plan Approval

The code-generation plan for `evaluation-and-comparison` is at
`construction/evaluation-and-comparison/code-generation/code-generation-plan.md` —
12 steps: change record with your recorded D-27 reversal + two proposed D-number texts
FIRST (1), estimand transcription and comparison_sets shape key (2), half B in
src/features/transforms.py (3), guards.py single guard home (4), masks.py (5),
metrics.py with the one inverse-gate import (6), AccessRecord containment fields (7),
script 07 (8), tests incl. one negative control per entry point (9), models-and-baselines
ABL-DIFF follow-through (10), smoke + lint (11), governance stop (12).

- Approve Plan
- Request Changes

[Answer]: Approve Plan
