# Functional Design Questions — `features-and-splits`

**Unit** `features-and-splits` — the closed ML input space and the partitions that make
forecasting honest.
**Kind** `library` · **Complexity** L · **Deployment** standalone · **Depends on**
`target-standardization`, `external-products`, `governance-guards`.

Unit **7 of 12**, and the one that carries the most acceptance rows in the plan. It owns
`src/features/availability.py`, `build.py`, `transforms.py`, `windows.py`;
`src/data/splits.py`; `scripts/05_build_features_and_splits.py`; and **six** test modules —
`test_feature_availability.py`, `test_iri_denial.py`, `test_split_embargo.py`,
`test_train_only_transforms.py`, `test_locked_test_guard.py`, and
**`test_feature_leakage_guards.py`**.

> **⚠ Corrected 2026-08-23, from "five".** The first five reproduce `unit-of-work.md` § 7's
> `Owns` list, which predates `CR-2026-08-22-LEAKAGE-TA`. **`test_feature_leakage_guards.py`**
> is TA-36's primary negative-path test, assigned here by the story map's § Cross-unit
> responsibilities and confirmed at `external-products` **R-54a**, which also records that
> `external-products` will **not** build it. Left at five, TA-36's primary test would have been
> built by nobody. **Derived: 5 + 1 = 6.** § 7's `Owns` list is a **fourth** stale item going
> to the gate, alongside §§ 5, 6 and 7's counts.

**BLK-04 is an EXIT condition on this stage**, and its contract is authored here. The
register is explicit: this unit and four downstream units **may enter** functional design;
**none may complete or exit without its approved contract**, and **no implementation may
proceed** while the blocker stands.

**11 requirements. The untested count is 1, not 4 — and the two upstream artifacts
disagree.** Derived by reading the rows:

| Source | Untested here | Acceptance rows as primary |
|---|---|---|
| `unit-of-work-story-map.md` Table 1 + § Per-unit coverage summary | **1** — FR-P1-04-10 | **12** — WS-10, WS-11, WS-12, WS-13, WS-18, TA-07, TA-08, TA-11, TA-18, **TA-33, TA-34, TA-35** |
| `unit-of-work.md` § 7 | **4** — the above plus FR-P1-04-12, -13, -16 | **9** — the twelve minus TA-33/34/35 |

**The story map is the current one.** **TA-33, TA-34 and TA-35** were approved
**2026-08-22** under Vision §15.2 (`CR-2026-08-22-LEAKAGE-TA`) as the negative-path rows
for FR-P1-04-12, -13 and -16 — the same change record that produced TA-36 — and
`requirements.md` records the recomputation: *"Four removed 2026-08-22 — 40 → 36… The count
above was recomputed from the test-row column, not decremented by hand."* § 7 was not swept
with it.

**This is the third §-N section of `unit-of-work.md` found stale in this stage**, after
§ 5's module count and § 6's untested list. Question 2 decides what this stage does about
it, and whether three instances is a pattern worth naming as one.

**All three new rows are `Pending`.** `requirements.md` states it per row: *"Status
`Pending`: the row exists, no test module is implemented, none has been executed, and none
has passed."* **A row is not a result.**

**G-09 is not signed.** `src/`, `configs/` and all **six** test modules are absent; `tests/`
holds three modules, none of them this unit's.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 7 — the `Owns` list, the boundary, the 11 requirements, the implementation notes; **BLK-04** with its exit-condition ruling.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2, § Per-unit coverage summary, § Cross-unit responsibilities, § Open verification gaps. **Derived by reading the rows:** 11 requirements, **1** with no acceptance row; **12** rows as primary; **supports** TA-36.
- `../../../inception/requirements-analysis/requirements.md` — FR-P1-04-1, -2, -5, -6, -8, -10, -12, -13, -16; NFR-IRI-01; NFR-LEAK-01; and the 40 → 36 recomputation record.
- `../../../inception/application-design/component-methods.md` — `src/features`' boundary calls (`AvailabilityRow`, `build_availability_matrix`, `assert_lags_safe`, `build_features`, `fit_transforms`/`apply_transforms`) and `src/data/splits.py` (`FoldSpec`, `build_folds`, `materialise_locked_partition`, `assert_membership_from_timestamps`).
- `../../../inception/application-design/services.md` § The nine stage scripts, § Stage entry contract.
- `../target-standardization/functional-design/business-rules.md` — the D-17 target rows this unit consumes.
- `../external-products/functional-design/business-rules.md` — **R-56**'s transitive import scan and **R-58**'s driver alignment.
- `../governance-guards/functional-design/business-rules.md` — **R-19** (the exactly-one-member exclusion shape), **R-23** and **R-24** (the two phase-boundary limbs). **Corrected 2026-08-23:** R-19 and R-24 are cited in this artifact’s body and were absent here; **R-25** (access-log ordering) and **R-28** (restricted root) were listed and drawn on nowhere, and are removed.
- `evidence/DECISIONS.md` — **D-10.3** (lags), **D-11** (fixture window), **D-13** (regime counts).
- Workspace inspection, 2026-08-23: `tests/` holds three modules, none this unit's; `src/` and `configs/` absent.
- Absent by scope design: `stories` (2.4 `SKIP`), `mockups` (1.6 and 2.5 `SKIP`). `kind: library`.

---

## Question 1

**BLK-04's contract is this stage's to author, and the register names exactly what it must
fix.** Quoted:

> *"A governed cross-unit contract enforcing train-only fitting per fold, defining input and
> output types, alignment requirements, ownership of the fitted state, allowed partitions
> (the named fold's training partition only) and failure conditions (`LeakageError` when
> `train`'s index is not a subset of that partition), so validation and locked-test leakage
> are prevented by the contract rather than by review."*

**The gap it closes, stated in the register's own implementation note:**
`fit_transforms(train, *, fold=...)` types `train` as an **unconstrained DataFrame**, so the
two-function split *"prevents the single-call convenience shape but not the underlying
full-dataset fit."* `component-methods.md` claims the interface makes a full-dataset fit
*"unrepresentable"* — it does not: `fit_transforms(all_data, fold=F1)` type-checks.

**Four downstream units inherit whatever this contract permits** —
`models-and-baselines`, `evaluation-and-comparison`, `statistical-inference`,
`regimes-diagnostics-reporting` — because *"every reported number inherits the fit."*

How is train-only fitting enforced?

A) Keep the two-function split and narrow the claim — state that shape alone does not prevent a full-dataset fit
   > **Impact**: Honest, and it is one of the two options the register itself offers. But it leaves NFR-LEAK-01 enforced by review for the one operation whose violation is invisible downstream: a transform fitted on all data produces better validation numbers and no error anywhere.

B) A **runtime assertion**: `train`'s index must be a subset of the named fold's training partition, `LeakageError` otherwise
   > **Impact**: The register's other option, and it closes the gap the type signature cannot. The check is cheap — an index containment test — and it fires at the exact call the leakage would come through. Requires the fold's training partition to be derivable inside `fit_transforms`, which `FoldSpec` plus `build_folds` supplies.

C) B, plus the **fitted state owned by the fold** — a `Transform` carrying its `fold_id`, and `apply_transforms` refusing a transform whose fold does not match the frame's partition
   > **Impact**: Closes the second half of the same leak. B stops a transform being *fitted* on the wrong rows; nothing yet stops one correctly fitted on F1 being *applied* to F3's validation month, which is the same leakage arriving by a different route. The register names *"ownership of the fitted state"* as a required element, and this is what that means operationally.
   
D) C, plus the contract stated once and **consumed by name** by the four downstream units, rather than restated in each
   > **Impact**: The register calls it a *"governed cross-unit contract"*, and four units inherit it. One statement consumed by name cannot drift; four restatements can, and this stage has already corrected four counts that drifted between restatements. Costs naming the contract as an artifact the downstream units cite rather than copy.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A is honest and leaves the project's central leakage rule enforced by reading. B is the register's own fix and closes the fitting half. C closes the applying half — the leak that survives B, and the one *"ownership of the fitted state"* is in the required-elements list to prevent. D makes it a cross-unit contract in fact rather than in name: four units inherit this, and a restated contract in four places is exactly the drift this stage has spent five correction cycles on.

[Answer]: D

> **⚠ Mechanism refined 2026-08-23 — the answer is unchanged, its option text was
> under-specified.** Option C says `apply_transforms` **"refus[es] a transform whose fold does
> not match the frame's partition"**. An adversarial review found that this is a **claim, not
> a check**: `apply_transforms(frame: DataFrame, *, transform: Transform)` carries **no fold
> or partition parameter** and `frame` carries **no partition tag**, so nothing in the
> signature can determine "the frame's partition" — the same defect Question 1's own preamble
> exposes in the approved `fit_transforms` interface, reproduced inside its remedy.
>
> **The first replacement was also wrong** and is recorded here too, because a correction that
> silently replaces a correction hides how the answer got where it is. It read: *"derives each
> row's partition from its record timestamps … a row belonging to any other fold, to the final
> refit, or to December raises `LeakageError`."* A second adversarial pass showed **(a)** the
> training ranges **nest** — Jan–Mar ⊂ Jan–Jun ⊂ Jan–Sep ⊂ Jan–Oct ⊂ Jan–Nov — so a February
> row lies in **five** of the six partition-list entries and *"this row's partition"* is not
> single-valued; and **(b)** excluding December and the refit **blocks G-06**, whose whole
> point is applying the Jan–Nov-fitted transform to December.
>
> **The mechanism now.** The `Transform` carries its **`FoldSpec`** — `component-methods.md`
> leaves `Transform` unspecified as an intra-package shape, so this is **this stage's to
> specify and costs no amendment** — and `apply_transforms` tests every row's timestamp
> against **the transform's own scope**: fold *k*'s training range, embargo and validation
> month; or, for the refit, Jan–Nov **and December**, reached only through the locked-partition
> guard. Rows outside raise `LeakageError`; so does an empty frame. **Still no signature
> change**, so no sixth boundary-contract amendment is owed.
>
> **One thing is left open rather than invented.** `fit_transforms` is typed
> `(train, *, fold: FoldSpec)` and Q9's answer records that **the final refit is not a
> `FoldSpec`** — so the refit's transform has no fitting path until that shape is settled.
> Element 4 is complete for F1–F4 and **conditional on that resolution** for the refit and
> G-06. **The two are one decision** and go to the gate together.
>
> Recorded here rather than by rewriting option C, because option C is what was chosen and
> must stay legible as chosen.

---

## Question 2

**`unit-of-work.md` § 7 is stale, and it is the third such section found in this stage.**

| Claim | § 7 | Story map — **governing** |
|---|---|---|
| Untested requirements | **4** — FR-P1-04-10, -12, -13, -16 | **1** — FR-P1-04-10 |
| Acceptance rows as primary | **9** | **12** — the nine plus TA-33, TA-34, TA-35 |

**Why the story map.** TA-33/34/35 were approved **2026-08-22** under Vision §15.2
(`CR-2026-08-22-LEAKAGE-TA`) for exactly FR-P1-04-12, -13 and -16, and `requirements.md`
records the recomputation as *"recomputed from the test-row column, not decremented by
hand."* § 7's bold list and row count predate it.

**The two earlier instances:** § 5 says the §12 tree holds **19** test modules where its own
BLK-05 table says **21**; § 6 says `external-products` has **5** untested and **1** row where
the story map says **4** and **2**. **All three froze at a 2026-08-22 amendment.**

What does this stage do?

A) Use the story map's figures and note the discrepancy, as the two earlier units did
   > **Impact**: Consistent with how § 5 and § 6 were handled, and it keeps each unit's treatment comparable. But it files a third instance as a third coincidence, which is how a systemic gap gets recorded as unrelated slips — a mistake this stage already made once, over-claiming a different pattern.

B) A, plus naming the three instances together as one finding about `unit-of-work.md`
   > **Impact**: Three sections of one file, all stale from the same day's amendments, is a fact about the file rather than about three units. Naming it lets the owner sweep once instead of three times. Risk: this stage previously named a "pattern" across three units that turned out to be partly a misreading, so the claim must be checkable — and here it is, because all three are the same file and the same amendment date.

C) B, plus checking the remaining five `unit-of-work.md` unit sections for the same staleness
   > **Impact**: Turns the finding from three observed instances into a bounded statement about the whole file — either the other five are clean, or the sweep is larger than three. Either answer is more useful to the owner than three anecdotes. Costs reading five sections against the story map.
   
D) C, with the result reported at the gate for a single annotate-in-place decision covering whatever the sweep finds
   > **Impact**: `CHANGE_RECORD_PROCEDURE.md` reserves approved-stage artifacts, and the owner has granted annotate-in-place before (`GOV-2026-08-22-INC-01` Rec 7). One decision over a complete list beats three decisions over partial ones. Costs the sweep and a gate item, and the owner may still decline.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A repeats the treatment without learning from the repetition. B names the pattern, and unlike the earlier over-claim this one is checkable — same file, same amendment date, three sections. C makes it a bounded fact rather than a count of what happened to be noticed, which matters because *"noticed"* has been the weak link in every correction cycle here. D gives the owner one decision over a complete list.

[Answer]: D

---

## Question 3

**§ 7 records five forbidden edges with no §16/§19 row**, quoted: *"dictionary closure, the
`vtec_lag_*` carry-forward prohibition, driver-interval repetition, support-field rules, and
the target-lag contract. Each is designed as a raise at a named call site so a test **can**
assert it; writing those criteria is a `requirements.md` change and is carried forward to
3.2."*

**That count predates 2026-08-22.** Since then:

| Edge | Now covered by |
|---|---|
| Dictionary closure | **TA-33** (FR-P1-04-12) — `Pending` |
| `vtec_lag_*` carry-forward prohibition | **TA-34** (FR-P1-04-13) — `Pending` |
| Support-field rules | **TA-35** (FR-P1-04-16) — `Pending` |
| Driver-interval repetition | **TA-36** (FR-P1-04-17) — `Pending`. **⚠ Corrected 2026-08-23:** this read *"`external-products`' row, not this unit's"*, from the story map's § Per-unit coverage summary alone. § Cross-unit responsibilities is the reconciling statement and gives **this unit** TA-36's **enforcement raise** at `features.build_features` **and its primary negative-path test** (`tests/test_feature_leakage_guards.py`) — already settled at `external-products` **R-54a**, whose own control says an artifact claiming the wrong side fails review. See `business-rules.md` **R-76a** |
| The target-lag contract | Part of FR-P1-04-13 → **TA-34** |

How does this unit state the remaining gap?

A) Repeat § 7's five
   > **Impact**: Cites the owning artifact directly. But four of the five now have approved rows, so the statement would be wrong in the direction that matters — claiming less coverage than exists, which invites someone to build a row that already exists.

B) State that four of the five now have rows, and only the target-lag contract remains
   > **Impact**: Closer, but wrong the other way: the target-lag contract is *part of* FR-P1-04-13, which TA-34 covers. Recounting without re-deriving would leave a phantom gap.

C) Derive the remaining gap from the requirement rows rather than from § 7's list
   > **Impact**: The only method that survives the amendment. Derived: **FR-P1-04-10 alone** — raw longitude — carries `UNTESTED`. The five-edge list has been fully superseded, and saying so is more useful than either count. Costs the derivation and a sentence explaining why § 7's five no longer holds.
   
D) C, plus stating that all four new rows are **`Pending`** — approved, never run
   > **Impact**: The distinction between *no row* and *a row that has never run* is the one this stage has been bitten by twice: FR-P1-02-8 behind a withdrawn `TA-29`, and TA-36 cited without its status. Four `Pending` rows on this unit's most leakage-sensitive requirements is exactly where that confusion would cost most. Costs a status label per citation.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A and B both restate a count instead of deriving one, which is the failure `project.md` § Way of Working names outright. C derives it: one requirement remains unrowed, not five. D adds the limb that matters most here — four newly approved rows, none implemented, none executed, none passing, on the requirements that carry this unit's leakage controls. A row that has never run is not coverage.

[Answer]: D

---

## Question 4

**FR-P1-04-2 has a third limb that the first two do not catch**, and the requirement says so
explicitly:

> *"The availability matrix asserts actual lag ≥ declared safe lag for every primary feature;
> a centered-mean injection fails; **and the trailing window's end date is asserted to be the
> safe-lagged day**, since a trailing 81-day mean ending at day *t* passes both the
> not-centered check and the lag assertion while including same-day F10.7."*

`component-methods.md` already puts this in `assert_lags_safe`'s raise contract: it raises
*"when `f107_81_trailing`'s window does not **end at the safe-lagged day** — the anchor
`TEC-13` restored."*

**`external-products` R-57 designed a future-independence property for the same series** —
perturbing any day after the safe-lagged day must leave the mean unchanged.

How does this unit assert the anchor?

A) `assert_lags_safe` raises when the window's end date is not the safe-lagged day
   > **Impact**: Exactly the approved raise contract, and it catches the stated hole. But it checks a recorded end date, so a series whose recorded anchor is right and whose values were computed from a different window passes.

B) A, plus recomputing the mean from the anchor and comparing
   > **Impact**: Closes the gap between the declared anchor and the values actually produced. A recorded field is a claim; a recomputation is a check. Costs recomputing an 81-day mean per feature row.

C) B, or accepting `external-products` R-57's future-independence property as the upstream evidence and asserting only the anchor here
   > **Impact**: Avoids two units computing the same guarantee. R-57's property is strictly stronger — it holds at every index rather than at the anchor — so if it passes upstream, recomputation here is redundant. But it makes this unit's assertion depend on a sibling's test having run, and `external-products`' rows are `Pending`.
   
D) A and B here, **independently of R-57**, with the overlap stated as deliberate
   > **Impact**: NFR-LEAK-01 is this unit's requirement and WS-11/TA-08 are this unit's rows; depending on a sibling's `Pending` test for its own acceptance evidence is the shape that let FR-P1-02-8 look covered. Two checks on one boundary is the pattern this stage has already adopted twice — `target-standardization` R-67 and `governance-guards` R-23 on the excluded field set. Costs the recomputation.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A implements the approved raise and leaves declared-versus-computed unchecked. B closes it. C is efficient and makes this unit's own acceptance row depend on a sibling row that has never run — the precise dependency that turns *"covered"* into a citation. D keeps the check where the requirement and the rows are, and states the overlap with R-57 as intended rather than leaving it to look like duplication.

[Answer]: D

> **⚠ Justification corrected 2026-08-23 — the answer is unchanged, one premise was wrong.**
> Option C's impact line and the recommendation both say `external-products`' **rows** are
> `Pending` / that C would depend on *"a sibling row that has never run"*. **There is no
> separate R-57 row.** `external-products`' own R-57 acceptance line states that R-57
> *"contributes to WS-11 and TA-08 (both owned by `features-and-splits`)"*, and the story map
> confirms it: WS-11 and TA-08 are **this unit's** rows, with `external-products` the
> **supporting** unit on them.
>
> D still stands, on a reason corrected twice. The second attempt — *"delegating the evidence
> … makes acceptance here depend on code outside this unit"* — **proves too much**: Q6 does
> exactly that delegation for the module-graph limb and this same answer set endorses it. The
> reason that survives both is **by property**: R-57's future-independence is a **series-level**
> property of the driver product, while the anchor recomputation is a **value-level** property
> of the mean built here, checkable only where it is built — and it catches a
> **recorded-but-wrong anchor** that R-57's *"any day after"* framing does not spell out. Two
> checks over one fact, not a hedge against a sibling.

---

## Question 5

**WS-13's evidence departs from TE §16, and the story map records the departure without
resolving it.** Quoted from Table 2:

> *"matched-window parity assertion over one `windows.py` definition — **departs from TE
> §16's stated evidence for this row, which names `test_common_masks.py`** (owned by
> `evaluation-and-comparison`, not by this row's evidence-producing unit). The substitution
> is defensible, parity being a `windows.py` property, but **no reading is adopted here** and
> the departure is recorded rather than resolved."*

WS-13 is **this unit's row**. `windows.py` is **this unit's module**. `test_common_masks.py`
is **`evaluation-and-comparison`'s**.

What does this stage do?

A) Follow TE §16 — the evidence is `test_common_masks.py`
   > **Impact**: Faithful to the governing document. But it makes this unit's acceptance row depend on a module it does not own, and masks are a different property from window parity — a mask test passing says nothing about whether the flattened matrix and the sequence tensor carry the same values.

B) Follow the story map — a parity assertion over `windows.py`
   > **Impact**: Tests the property WS-13 actually states, in the module that owns it, which is why `component-methods.md` says one window definition makes parity *"structural rather than asserted"*. But it adopts a reading the story map deliberately declined to adopt.

C) B, with the departure from TE §16 stated and carried to the gate as an unresolved reading
   > **Impact**: Builds the check that tests the stated property while leaving the governing-document question where the story map left it — open, and the owner's. `CHANGE_RECORD_PROCEDURE.md` reserves that call. Costs a gate item rather than a decision.
   
D) C, plus TA-11 noted as consuming `test_common_masks.py` regardless, so both evidences exist
   > **Impact**: TA-11's evidence column already names `test_common_masks.py` alongside `test_split_embargo.py`, `test_train_only_transforms.py` and the parity assertion — so the mask test is required for this unit's TA-11 whichever way WS-13 resolves. Stating that removes the appearance of a choice between the two. Costs one sentence, and it makes the departure narrower than it looks.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A ties this unit's row to a sibling's module for a property that module does not test. B builds the right check and quietly adopts a reading the story map refused to adopt. C keeps the reading open where it belongs. D adds the fact that makes the whole question smaller: `test_common_masks.py` is already required here through TA-11, so the departure is about which row cites it, not about whether it runs.

[Answer]: D

---

## Question 6

**FR-P1-04-1's import boundary is an allowlist, not a denylist**, and the requirement is
emphatic:

> *"TE §12 states it as 'imported only by `scripts/04_build_external_products.py` and
> `src/evaluation/`', so an import from `src/data/`, `src/gnss/`, a training script or a
> notebook violates it **exactly as** an import from `src/features/` or `src/models/`
> does."*

Its criterion requires the check to **reject an importer outside the two permitted ones**,
*"the denylist-o…"* — a check that only forbids `src/features` and `src/models` passes a
notebook import.

**`external-products` R-56 already designed this**: a transitive static reachability scan,
declared authoritative for the module-graph property, with the dynamic-import residual named
and accepted.

This unit owns `test_iri_denial.py` and TA-07's import-boundary evidence.

How do the two units divide it?

A) This unit builds its own import-boundary check
   > **Impact**: Keeps this unit's acceptance evidence in this unit. But two independent implementations of one graph property will drift, and R-56 already states the transitive requirement and the dynamic-import limit.

B) This unit consumes `external-products` R-56's check and asserts its result
   > **Impact**: One implementation, one place to fix a gap. But TA-07 is this unit's row and R-56's status is `external-products`' to report — the same dependency shape Question 4 rejects for the F10.7 anchor.

C) B, with the **data-flow limb built here** and the module-graph limb consumed
   > **Impact**: The two limbs are genuinely different properties: `test_iri_denial.py` asks *did an `iri_*` value reach the feature path* — a data-flow question this unit owns — while the import boundary asks *can a module reach `iri.py`* — a source-tree question R-56 owns. Splitting them by property rather than by unit puts each where it can actually be checked. `governance-guards` R-23/R-24 already draw the same line.
   
D) C, plus this unit asserting **the allowlist's completeness** — that the permitted-importer set is exactly the two TE §12 names
   > **Impact**: The requirement's own emphasis is that the check must reject importers *outside* the two, which a denylist cannot do. Asserting the permitted set has exactly two members is the same one-member-exclusion shape `governance-guards` R-19 uses, and it is what makes "allowlist" true rather than aspirational. Costs one assertion, and it must be updated deliberately if TE §12 ever widens.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A duplicates a graph check across two units. B hands this unit's row to a sibling's evidence. C divides by property — data flow here, module graph there — which is the division `governance-guards` already uses and the only one where each check sits where it can be run. D adds the limb the requirement is emphatic about: a denylist passes a notebook import, and only an exactly-two-members assertion makes the allowlist claim checkable.

[Answer]: D

---

## Question 7

**Two adjacent rules on one pipeline have opposite behaviour, and FR-P1-04-13 says the
confusion is the point:**

| Rule | Applies to | Behaviour |
|---|---|---|
| FR-P1-04-3 | **External drivers only** | Carry forward **≤ 3 h**, then exclude the row |
| FR-P1-04-13 | **`vtec_lag_*` target-derived lags** | **Carry-forward prohibited**; the window is **excluded instead** |

The requirement's own words: the ≤3 h allowance *"is scoped to external drivers only and
**must never be read as reaching `vtec_lag_*`**."*

Also FR-P1-04-13: `vtec_lag_1h/2h/3h/24h` are **strictly causal at exact lags `[1,2,3,24]`**;
`vtec_seq_24` is a 24-step causal sequence **excluded when incomplete**; and the pooled model
carries `station_onehot_ARUC/BSHM/NICO` plus **verified** `station_lat`, with an unresolved
registry **blocking their use**.

How is the asymmetry enforced?

A) Two separate checks, one per rule
   > **Impact**: Each rule gets its own enforcement, which is correct as far as it goes. But nothing then prevents a future implementer applying the driver rule to a target lag — the exact misreading the requirement warns against — because the two checks never meet.

B) A, plus the carry-forward function taking the field class as a required argument, with `vtec_lag_*` rejected at that boundary
   > **Impact**: Makes the misreading unrepresentable rather than merely prohibited: a carry-forward call on a target-derived lag cannot type-check its way through. This is the shape `component-methods.md` reached for with `fit_transforms`/`apply_transforms` — and Question 1 shows shape alone is not enough, so this needs the runtime check too.

C) B, plus an assertion that the two field classes **partition** the feature set — every field is exactly one of driver-derived or target-derived
   > **Impact**: Closes the gap B leaves: B stops a target lag entering the driver path, but a field belonging to neither class, or to both, escapes both rules. A partition assertion makes that a failure. Costs classifying every §6.2 dictionary field, which FR-P1-04-12's closure requires anyway.
   
D) C, plus the **excluded-window count recorded** rather than only the exclusion enforced
   > **Impact**: FR-P1-04-13 requires an incomplete `vtec_seq_24` window to be *"excluded **and counted**"*, and FR-P1-04-5 requires the same of the embargo's first 24 h. A silent exclusion and a counted one are indistinguishable at the artifact unless the count exists — and the count is what a reviewer uses to tell a working exclusion from one that never fired. Costs a manifest field.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A enforces both rules and leaves the misreading available. B makes the misreading unrepresentable at the boundary where it would occur. C catches the field that belongs to neither class, which B does not — and the classification is already owed to FR-P1-04-12's dictionary closure. D adds the counted-exclusion limb both requirements state in the same words, and it is the difference between an exclusion that ran and one nobody can tell fired.

[Answer]: D

---

## Question 8

**FR-P1-04-16's support-field rules include an ordering claim about a human approval.** Three
rules from TE §6.2, plus a fourth restated from NFR-LEAK-01:

1. Support fields are **diagnostic by default**.
2. A support field may only be read over **hours ≤ t** — never the target hour or later.
3. **Model use of any support field requires explicit G-04 approval, recorded *before* the
   feature set is frozen.**
4. **Target-hour quality fields are permanently forbidden** as features.

Rule 3 is an ordering claim about an act performed by a person, of the same class as
`inventory-and-registry`'s retrospective split redesign and `external-products`' GIM
hand-check.

How is rule 3 enforced?

A) `build_features` raises when a support field is used without a recorded G-04 approval ID
   > **Impact**: What `component-methods.md`'s raise contract already states, and it catches the unapproved use. But *"recorded before the feature set is frozen"* is an ordering claim, and a presence check passes an approval recorded afterwards.

B) A, with the approval's timestamp asserted to **precede the feature-set freeze**
   > **Impact**: Implements the clause that gives rule 3 its force, using the same frozen-value-plus-timestamp evidence class this stage has now used three times — `inventory-and-registry` R-52, `external-products` R-59 and R-60. Retrospective approval becomes a failure rather than a judgement call.

C) B, plus rules 1, 2 and 4 as separate assertions with separate failures
   > **Impact**: Four rules, four results. TA-35's criterion names two of them explicitly — a support field used without approval **fails**, one read at or beyond hour *t* **fails** — and FR-P1-02-8's history in this stage is what happens when several obligations sit behind one citation. Costs four checks instead of one.
   
D) C, plus **diagnostic-by-default** implemented as the default rather than as a rule to remember — a support field is excluded from the feature set unless an approval ID is present
   > **Impact**: Turns rule 1 from a statement into the system's behaviour: the failure mode it guards against is a support field drifting into the feature set by inclusion rather than by decision, and a default-exclude makes that impossible instead of detectable. Costs nothing beyond stating the default, and it makes rule 3's approval the only entry path.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A implements the raise and misses the ordering. B fixes the ordering with the evidence class this stage has already settled on three times. C separates four obligations that would otherwise sit behind one check — the FR-P1-02-8 failure. D makes rule 1 structural: *diagnostic by default* is a default, and implementing it as one means a support field cannot enter the feature set without passing through rule 3's approval.

[Answer]: D

---

## Question 9

**FR-P1-04-5's partition list carries a fifth entry that was previously omitted**, and the
requirement explains why the omission mattered:

> *"The partition list also carries **`Final refit: 1 Jan – 30 Nov`**, and November enters the
> final refit **only after all features, hyperparameters, masks, seeds, thresholds and
> analysis rules are frozen** — previously omitted, which left Vision §8.1's rule that **each
> target timestamp belongs to exactly one partition** with no list to check November
> against."*

The folds: **F1** Jan–Mar/Apr; **F2** Jan–Jun/Jul; **F3** Jan–Sep/Oct; **F4** Jan–Oct/Nov;
**December locked**. Each carries a **24-hour embargo**; the first 24 h are **excluded and
counted**; **no random or shuffled cross-validation**.

How is the final refit handled?

A) Build F1–F4 and the locked partition; treat the final refit as a later concern
   > **Impact**: Covers what `build_folds` returns today and what WS-12 tests. But it reproduces the omission the requirement just corrected — November would again have no partition list to be checked against, and Vision §8.1's exactly-one-partition rule would again have nothing to range over.

B) A, plus the final refit as a declared partition in the same list
   > **Impact**: Gives §8.1's rule a complete list to check, which is the stated reason the entry was added. Costs representing a partition that is not a fold — `FoldSpec` has `validation_month`, and the final refit has none.

C) B, plus the **freeze precondition asserted**: November enters only after features, hyperparameters, masks, seeds, thresholds and analysis rules are all frozen
   > **Impact**: The entry's substance is the precondition, not the date range. Six named things must be frozen first, and a refit that runs before any of them is the leakage this partition exists to bound. Same timestamp-ordering evidence class as Question 8. Costs enumerating the six freeze artifacts and checking each.
   
D) C, plus **exactly-one-partition** asserted over the complete list, F1–F4 plus the final refit plus December
   > **Impact**: Vision §8.1's rule stated as a check rather than as prose — every target timestamp belongs to exactly one partition, verified over the whole list. It catches both an overlap and a gap, and it is the assertion the corrected list was added to make possible. Costs one pass over the timestamps.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A repeats an omission the requirement was amended to fix. B restores the list. C asserts the precondition that is the entry's actual content — six frozen artifacts before November enters. D is the check the whole correction was for: §8.1's exactly-one-partition rule had no list to range over, and now it does. Note that the final refit is not a `FoldSpec` — it has no validation month — so representing it needs a decision this stage should state rather than assume.

[Answer]: D

---

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence — `foundation` R-01…R-17, `governance-guards` R-18…R-29, `acquisition` R-30…R-43, `inventory-and-registry` R-44…R-53, `external-products` R-54…R-63, `target-standardization` R-64…R-73 — so this unit opens at **R-74**. If per-unit numbering was intended, say so at the gate and the artifacts restart.
- **[assumption]** The **story map governs** where it and `unit-of-work.md` § 7 disagree, because the 2026-08-22 §15.2 approval of TA-33/34/35 is what moved it. Neither artifact is edited by this stage.
- **[assumption]** `src/features/*` and `src/data/splits.py` shapes beyond the named boundary calls are **intra-package** and this stage's to specify (`component-methods.md` § Depth) — **still true, and still owes nothing for them**. But Q1's answer, as finally mechanised, **amends two boundary calls**: `apply_transforms` gains a required `purpose`, and `build_features` gains `transform`. Running total **7 across 4 units**. **Corrected 2026-08-23** from *"no amendment is owed; the total stays five across three units"*.
- **[assumption]** `tests/test_locked_test_guard.py` is **this unit's**, per § 7 — it exercises both limbs and this unit already depends on `governance-guards`, so assigning it there would close a cycle. `governance-guards` supports WS-18 and TA-18.
- **Open — BLK-04 is an EXIT condition on this stage**, and on the four downstream units that inherit the fit. **No affected unit may complete or exit 3.1 without its approved contract**, and **no implementation may proceed** while it stands. NFR-LEAK-01's evidence is still owed to the **Supervisor at G-04 and G-05**.
- **Open — TA-33, TA-34, TA-35 and TA-36 are all `Pending`** — approved, not implemented, not executed, not passing. **A row is not a result.**
- **Open — `unit-of-work.md` § 7 is stale**, the third such section after § 5 and § 6. Question 2 decides whether to sweep the remaining five.
- **Open — WS-13's evidence departs from TE §16** and the story map explicitly adopts no reading. Question 5 decides what this stage does without adopting one either.
- **Open — FR-P1-04-10 is this unit's one requirement with no acceptance row**: raw longitude never enters as a predictor; longitude enters only through `lst_sin` and `lst_cos`.
- **Open — the final refit is not a `FoldSpec`.** It has no validation month, so representing it in the same partition list needs a shape decision this stage states rather than assumes.
- **Open — an unresolved station registry blocks `station_lat` and excludes `lst_sin`/`lst_cos`**, per `inventory-and-registry` R-45/R-46. This unit consumes that block; it does not decide what provenance is sufficient.
- **G-09 is not signed.** No answer here authorises creating any module, and **no implementation may proceed while BLK-04 stands.**
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

---

## FU-4, FU-5, FU-6 — the three iteration-5 findings that need a decision

Five adversarial iterations have run on this unit. Iteration 5 leaves **2 Criticals and 3
Majors** standing, and states the consequence plainly: *"BLK-04's contract remains one whose
closing half a developer would have to invent."* Findings **4, 5, 6 and 7** are mechanical —
a signature block that did not follow its own amendment, two raise-table rows still stating
superseded readings, one sentence duplicated as both contract and refutation, and three
Assumptions entries naming one parameter where the amendment adds two. Those are applied
during regeneration and are **not** put to you here.

The three below cannot be applied without a decision, because each picks between builds with
different prerequisites — and **FU-5 has a scientific consequence** on the locked December
test.

**None of the three decides a scientific constant.** FU-5 decides which rows a call may read,
which is a mechanism question; its scientific consequence is that one option **silently drops
1 December from the G-06 locked-test prediction**, and that is why it is being asked rather
than chosen.

### FU-4 — How is the train-only-transform pairing made observable? *(iteration-5 finding 1, Critical)*

The pairing control is the **sole stated closure of the 10-cell hole**, which is the surviving
half of **BLK-04**'s leak, inherited by four downstream units. It reads that a scored frame
*"was **obtained from a call** with `transform = T_k` and `purpose=evaluate`."* Traced against
`services.md` § The nine stage scripts, that call and that scoring never share a process:
`05_build_features_and_splits.py` **writes** the feature matrix, sequence tensor, folds and
masks; `06_train_and_predict.py` and `07_evaluate_and_report.py` **read** them from artifacts.
So `apply_transforms` is called only in `05`, no scoring site calls it, **nothing stamps the
emitted artifacts with the fold or the purpose**, and the predicate has nothing to test.

A) **Provenance stamp, consumer-side assertion, manifest-based test**
   > **Impact**: `domain-entities.md` § 5 gains `fold_id`, `purpose` and the fitted transform's identity as recorded fields on the emitted feature artifacts; `06`/`07` refuse a frame whose stamp is not `(fold k, evaluate)` when scoring fold *k*'s validation month; `tests/test_train_only_transforms.py` is declared **manifest-based** and asserts that refusal with R-74's two controls. The residual restates as *"an unstamped or hand-assembled frame"*. Closes the observability gap at the point the design can actually see it. **Costs an amendment**: the stamp crosses into `06`/`07`, so § Amendments owed re-derives from 7-across-4 to **8 across 5**.

B) **Static analysis of the nine stage scripts**
   > **Impact**: `test_train_only_transforms.py` parses the nine scripts and asserts no scoring path consumes a frame produced under a non-`evaluate` purpose. No stamp, no amendment, no runtime cost. But it can only see the enumerated scripts — the residual stays *"a caller outside the nine"*, which iteration 5 showed is the **wrong description of the gap**, since the real one is the ordinary `05`→`06` handoff **inside** them. Static analysis of a file-mediated handoff cannot follow the artifact.

C) **Monkeypatch-and-replay runtime check**
   > **Impact**: the test replaces `apply_transforms`, replays the pipeline and records every `(fold, purpose)` actually used. No production change and no amendment. But it verifies a **replay**, not the artifacts a real run emits, and it needs the whole pipeline runnable inside the test — a heavier prerequisite than the fixture suite currently carries, and one nothing in §12's `tests/` tree anticipates.

D) **Stamp and consumer refusal as in A, and declare it a boundary change**
   > **Impact**: everything in A, plus the amendment is **declared explicitly** and § Amendments owed is re-derived in all three artifacts rather than left to a later sweep to notice. Slightly more work now; removes the risk that a downstream unit meets a stamped artifact its own contract never mentioned. This is the reviewer's own recommendation, taken with its stated conditional.

X) **Other (please specify)**
   > **Impact**: Depends on your specific choice. Any option must name a mechanism that can observe the pairing **across a file handoff**, since that is what defeated the current wording.

> **💡 Recommendation**: **Option D** — A and D are the only two that can observe the actual gap, and D differs only in declaring the amendment instead of deferring it. `project.md` § Way of Working requires the inputs a gating condition depends on to be specified in the same stage that records the condition; BLK-04 is an **exit condition on this stage and on four downstream units**, so leaving its closure to a mechanism named later is exactly the failure that rule names. The honest cost: the amendment total moves to 8 across 5, and `06`/`07` belong to units whose design has not run yet, so this stage is writing a requirement into their inbox.

[Answer]: D

### FU-5 — What rows may an `evaluate` call read, given the 24-step causal window? *(iteration-5 finding 2, Critical)*

`component-methods.md:380-393` approves `build_features(target, *, drivers, registry, matrix,
fold, snapshot)` — **no period, month or row-range parameter**, and `fold` is the same value in
both calls. Yet the resolution requires a `train` call over the training partition and an
`evaluate` call over the validation month — **disjoint months** the call cannot express. And
this unit's own contract makes the collision concrete: `vtec_seq_24` is a 24-step causal
sequence and `vtec_lag_24h` an exact 24-hour lag, so the first window of any validation month
needs the **preceding day's rows** — which are lawful inputs at the forecast origin.

A) **`build_features` derives its row set from `fold` + `purpose`; history read but not emitted**
   > **Impact**: the accepted set for `evaluate` is *"fold k's validation month **plus the causal history the frozen 24-hour window requires**, which may not be emitted as rows."* Element 4 tests the **assembled pre-window frame**, stated explicitly. No `LeakageError` on lawful history, no lost rows, and **December keeps 1 December**. Requires the artifacts to state the derivation rule against the approved signature, plus a control that emitted rows never exceed the validation month.

B) **Caller slices the inputs; first 24 hours of each validation month excluded and counted**
   > **Impact**: mechanically simpler and needs no derivation rule. But the first ~24 hours of **every** validation month produce incomplete `vtec_seq_24` windows that W-2 requires excluded — **including 1 December**, so the **G-06 locked-test prediction loses its first day**. The loss would be counted and stated at G-06 rather than silent, but it is still a permanent reduction of the locked test, and § 6's table gives December no embargo row to absorb it.

C) **Caller slices, including a leading history buffer, and element 4 tests the emitted rows only**
   > **Impact**: keeps the approved signature untouched and keeps 1 December. But it moves the row-selection decision **outside** this unit into callers this stage does not own, and element 4 then never sees the pre-window frame — the exact ambiguity iteration 5 named as *"the design never says which frame element 4 tests"*, left open rather than closed.

D) **Option A, plus the December consequence stated where G-06 is described**
   > **Impact**: A's mechanism, and the artifacts additionally record — at the point G-06 is described — that the locked-test prediction covers the **full** December and why no first-day loss occurs. Costs a few lines; makes the scientific consequence checkable at the gate instead of inferable from a mechanism three sections away.

X) **Other (please specify)**
   > **Impact**: Depends on your specific choice. Any option must say **which frame element 4 tests**, since the two readings differ precisely on this case.

> **💡 Recommendation**: **Option D** — the history rows are lawful at the forecast origin, so excluding them buys nothing scientific and costs the first day of every validation month, December included. Option B's loss lands on the **locked test**, the one artifact the project treats as irreplaceable, and `project.md` bars changing the frozen claim boundary. D is A with the consequence written where a gate reader will meet it. The honest cost: A and D both require `build_features` to derive rows from `fold` + `purpose`, which is a **behavioural** specification of an approved signature — legitimate under `component-methods.md` § Depth as an intra-package shape, but it should be declared, not slipped in.

[Answer]: D

### FU-6 — How is the third, uncounted call handled? *(iteration-5 finding 3, Major)*

The resolution's own sequence is **three** calls per fold, not two:
`build_features(transform=None, purpose=None)` produces the features `fit_transforms` is
fitted on; then a `train` call; then an `evaluate` call. The artifacts describe only *"two
calls over disjoint months"*. The fitting call covers the **same** months as the `train` call,
so it is neither of the two — and it emits **both** representations **untransformed**, with
nothing forbidding their consumption. Compounded by `05` writing to artifacts: three
`(matrix, tensor)` pairs per partition reach disk and nothing distinguishes them.

A) **State three calls; fitting-call outputs are a fitting input only, never emitted, persisted or consumed, with a negative control**
   > **Impact**: the call sequence, the artifact inventory and the count agree. The negative control — an untransformed tensor reaching M-06 **fails** — matches this project's mandated negative-control practice. Requires restating the sequence in W-4, R-81 and § 5.

B) **Keep the two-call description; add the prohibition only**
   > **Impact**: less editing, and the hazard is closed. But the count stays wrong in three artifacts, and the next reviewer re-raises the same discrepancy — this is the fifth consecutive iteration in which a remedy was stated as an outcome rather than a mechanism.

C) **Fold the fitting call into `fit_transforms` so no third `build_features` call exists**
   > **Impact**: cleanest conceptually — one call produces the fitting frame internally and nothing untransformed ever reaches disk. But `fit_transforms`' approved signature does not take the inputs `build_features` assembles, so this **amends a boundary call** and raises the amendment total again.

X) **Other (please specify)**
   > **Impact**: Depends on your specific choice. Any option must make the artifact inventory match the call count, since `05` persists what each call emits.

> **💡 Recommendation**: **Option A** — it closes the hazard *and* fixes the count, without touching an approved signature. C is tempting but pays an amendment for a problem A solves in prose plus one control; B leaves a known-wrong count in three artifacts, which this unit's own rule against restated contracts drifting already warns about.

[Answer]: A

---

### Question FU-7 — the December scored-set conflict
Which reading governs the G-06 locked test's scored set?

A) Accept ADR-11's 30-day consequence — FU-5 = D's December clause is recorded as superseded
   > **Impact**: The locked test scores 2–31 December (30 days); the first 24 h are excluded and counted, consistent with every validation month and FR-P1-04-5. FU-5 = D's clause is kept as a dated superseded record, not deleted. No upstream artifact changes; the disclosure ADR-11 already mandates stands. Your ruling is recorded as the project owner's acceptance under the recorded student/supervisor authority equivalence.

B) Reinstate 1 December — direct a 2.6 backward jump to restore a lead-in mechanism
   > **Impact**: Reopens the approved application-design contract a second time, against ADR-11's own recorded rejection of that mechanism; touches a supervisor-owned value (Vision §8.2/§8.7, G-05) and re-derives this unit's rebuild. Costly, and it contradicts FR-P1-04-5 as worded.

C) Defer to the G-05 gate — leave both records standing, decide with the supervisor
   > **Impact**: The conflict stays an Open item through Construction; stage 3.5 cannot implement the scored-set boundary of `06`/`07` while it stands, which likely blocks models-and-baselines' scored-range code at code-generation.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — ADR-11 is the later, contract-level decision, taken with this exact trade-off in view and already carrying its mandatory disclosure; FR-P1-04-5's wording supports it, and 30 scored December days remain a valid locked test under D-8's claim boundary. Option B reopens a supervisor-owned value to recover one day.

[Answer]: A — Accept ADR-11’s 30-day consequence; FU-5 = D’s December clause is recorded as superseded. Ruled by the project owner 2026-08-26, recorded as their acceptance under the recorded student/supervisor authority equivalence.

## Consolidated Summary Confirmation (superseded by the 2026-08-28 post-execution pass below)

Questions 1–9 are answered above as the recommended option in each case — **D throughout** —
on the owner's instruction to apply the recommendations. Consolidated:

| Q | Answer | What it settles |
|---|--------|-----------------|
| 1 | D | **BLK-04's contract.** A runtime assertion that `train`'s index is a subset of the named fold's training partition (`LeakageError` otherwise); the **fitted state owned by the fold**, with `apply_transforms` refusing a mismatched `fold_id`; and the contract **stated once and consumed by name** by the four downstream units rather than restated in each |
| 2 | D | The **story map governs** (1 untested, 12 rows); the three stale `unit-of-work.md` sections named as **one finding about that file**; **the remaining five unit sections swept** against the story map; and the whole result reported at the gate for a **single** annotate-in-place decision |
| 3 | D | The remaining gap **derived, not carried**: **FR-P1-04-10 alone**, not § 7's five. TA-33/34/35/36 now cover four of the five edges — and **all four are `Pending`**, cited with that status |
| 4 | D | FR-P1-04-2's third limb built **here**: the trailing window's end date asserted to be the safe-lagged day, **plus** the mean recomputed from that anchor — independently of `external-products` R-57, with the overlap stated as deliberate rather than left looking like duplication |
| 5 | D | WS-13 built as a **parity assertion over `windows.py`**, with the departure from TE §16 carried to the gate as an **unresolved reading** — and the note that `test_common_masks.py` is required here through **TA-11** regardless, which makes the departure narrower than it looks |
| 6 | D | The two limbs split **by property**: the **data-flow** denial (`test_iri_denial.py`) built here; the **module-graph** boundary consumed from `external-products` R-56 — plus an assertion that the permitted-importer set has **exactly the two TE §12 members**, which is what makes "allowlist, not denylist" checkable |
| 7 | D | The carry-forward asymmetry made unrepresentable: the field class is a **required argument** and `vtec_lag_*` is rejected at that boundary; the two classes asserted to **partition** the feature set; and every **excluded window counted**, not merely excluded |
| 8 | D | Four support-field rules, four separate failures; the **G-04 approval timestamped before the feature-set freeze**; and **diagnostic-by-default implemented as the default** — a support field is excluded unless an approval ID is present, so rule 3's approval is the only entry path |
| 9 | D | **`Final refit: 1 Jan – 30 Nov`** carried as a declared partition; its **six freeze preconditions asserted**; and Vision §8.1's **exactly-one-partition** rule asserted over the complete list — the check the corrected list was added to make possible |

**One answer is the stage's exit condition.** Q1 authors BLK-04's contract. **This unit and
the four downstream units may not complete or exit stage 3.1 without it**, and **no
implementation may proceed while the blocker stands.** NFR-LEAK-01's evidence remains owed
to the **Supervisor at G-04 and G-05** — unchanged by anything answered here.

**One answer commits to work beyond this unit.** Q2's sweep of the remaining five
`unit-of-work.md` sections is done to give the owner one decision over a complete list
rather than three over partial ones. If the sweep finds the other five clean, that is
reported as a bounded fact; if it finds more, the list grows.

**One answer states a shape decision rather than assuming one.** Q9's final refit is **not a
`FoldSpec`** — it has no validation month — so how it is represented in the same partition
list is stated at the gate, not assumed.

**Two answers deliberately overlap a sibling's check, and say so.** Q4 recomputes the F10.7
anchor here despite `external-products` R-57's stronger property, and Q6 keeps the data-flow
denial here while consuming the module-graph scan. Both because **the two checks test
different properties of one fact** — R-57's is series-level, the anchor recomputation
value-level; the module-graph scan is a reachability property, the data-flow denial a
value-flow property.

> **⚠ Corrected 2026-08-23.** This paragraph previously read *"this unit's own acceptance rows
> may not rest on a sibling's `Pending` test"*. **Two things were wrong with it.** There is no
> separate R-57 row — WS-11/TA-08 are this unit's own, with `external-products` supporting.
> And the replacement reason offered at Q4 (*"would depend on a module in another unit"*)
> **proves too much**: Q6 **does** delegate the module-graph limb to `external-products` R-56
> while keeping WS-10/TA-07 here, so applied consistently it would forbid the very split Q6
> adopts. The by-property reason above holds for both, and **neither answer changes**.

**Two amendments are owed, and they are Q1's real price.** The `src/features/*` and
`src/data/splits.py` shapes beyond the named boundary calls are **intra-package**, and
`component-methods.md` § Depth names this stage as where they are specified — **those owe
nothing**, `Transform`'s internals included. But mechanising Q1's answer so that it actually
works required amending **two cross-package boundary calls**: `apply_transforms` gains a
required `purpose` (`train` | `evaluate`), and `build_features` gains **both**
`transform: Transform | None = None` **and** `purpose: ApplyPurpose | None = None` — they
travel together, and supplying one without the other raises. Running total **7 across 4
units** (two functions, not two per function), derived in `business-logic-model.md`
§ Amendments owed.

> **⚠ Corrected 2026-08-23.** This paragraph read *"nothing here owes an amendment … the
> running total stays five owed amendments across three units."* That held for the first two
> attempts at element 4, **both of which avoided a signature change and neither of which
> worked** — the first stated a comparison the signature could not perform, the second derived
> a partition label that does not exist and blocked G-06. The amendment is what a working
> mechanism cost. **The owner approved it on 2026-08-23** after being shown that no row-level
> check can separate a legitimate training use from a leaking evaluation use of the same row.

Carried to the gate, unchanged by these answers: **BLK-04 open and an exit condition**;
TA-33/34/35/36 all `Pending`; `unit-of-work.md` § 7 stale, plus whatever the § sweep finds;
WS-13's departure from TE §16 unresolved; FR-P1-04-10 with no acceptance row; the final
refit's representation; an unresolved station registry blocking `station_lat` and
`lst_sin`/`lst_cos`; rule numbering assumed to continue at R-74; G-09 unsigned.

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

*(Answered `Looks correct`, 2026-08-23; that receipt belongs to the previous attempt, and it
predates FU-4, FU-5 and FU-6. The live answer tag for this section is the blank one at its
end.)*

### Re-confirmation, 2026-08-24 — new stage attempt, and the three iteration-5 decisions

**Why this is being re-asked.** Two reasons, and the second is the substantive one.

1. Inception closed and Construction opened at **2026-08-24T11:46:26Z**, starting a fresh
   `functional-design` attempt and resetting the receipt floor for every unit. Both
   `foundation` passes of that day (`governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md`)
   were checked against this unit and touch nothing it reads: it consumes
   `component-methods.md` § Depth plus the `fit_transforms`/`build_features`/`apply_transforms`
   blocks, `services.md` § The nine stage scripts, and `unit-of-work.md` § 7 — none of them
   the amended `DeterminismRecord`, § Run record and registry, or § 1. Amendment A was
   declined, so **no count moved**.
2. **This unit's § Review verdict is `NOT-READY`** — five adversarial iterations, the last on
   2026-08-23, leaving **2 Criticals and 3 Majors**. Unlike every sibling, this unit is not
   being carried forward as-is. **FU-4, FU-5 and FU-6 above are new questions**, answered
   **D, D, A**, and they change what the artifacts must say.

### What the three answers settle

| | Decision | What the artifacts must now state |
|---|---|---|
| **FU-4 = D** | Provenance stamp **and** the amendment declared | `domain-entities.md` § 5 gains `fold_id`, `purpose` and the fitted transform's identity as recorded fields on the emitted feature artifacts; `06`/`07` **refuse** a frame whose stamp is not `(fold k, evaluate)` when scoring fold *k*'s validation month; `tests/test_train_only_transforms.py` is declared **manifest-based**; the residual restates as *"an unstamped or hand-assembled frame"*, **not** *"a caller outside the nine scripts"*. **§ Amendments owed re-derives from 7 across 4 to 8 across 5** — declared here, not left to a later sweep |
| **FU-5 = D** | Rows derived from `fold` + `purpose`; causal history read but never emitted; December consequence stated at G-06 | `evaluate`'s accepted set is *"fold k's validation month **plus the causal history the frozen 24-hour window requires**, which may not be emitted as rows"*; **element 4 tests the assembled pre-window frame**, stated explicitly; a control asserts emitted rows never exceed the validation month; and the point where **G-06** is described records that the locked-test prediction covers the **full** December with no first-day loss |
| **FU-6 = A** | Three calls per fold, fitting output never emitted | W-4, R-81 and § 5 restate the sequence as **three** calls — `transform=None, purpose=None` to produce the fitting frame, then `train`, then `evaluate`; the fitting call's outputs are a **fitting input only**, never emitted, persisted or consumed; negative control: an untransformed tensor reaching **M-06 fails** |

### What is applied without asking

Findings **4, 5, 6 and 7** are mechanical corrections with no decision in them:

- **W-2's signature block** (`business-logic-model.md:97-101`) becomes
  `INPUT target, drivers, registry, matrix, fold, snapshot, transform, purpose` with the
  pairing requirement noted, and `RAISES LeakageError, AlignmentError`.
- **`domain-entities.md` § 10** — `LeakageError` restated as *"a frame leaving the set the
  declared `purpose` permits for that transform's fold, or an empty or timestamp-less frame"*
  (the pure-containment formulation is an upper bound that admits the leaking direction);
  `PartitionError` restated over **evaluation role** — a 2022 month with two roles or none —
  since the literal *"more than one partition"* reading fires on an ordinary 15 February row.
- **The duplicated sentence** at `business-logic-model.md:327-330` and
  `business-rules.md:165-168` gets the rewrite already applied at `domain-entities.md:237-239`.
- **The three Assumptions entries** read *"`build_features` gains `transform` **and**
  `purpose`, which travel together"*.

Iteration-5 findings **9, 10 and 11** were not re-raised as blocking and were left standing
on 2026-08-24. **Fixed 2026-08-26** on the owner's "fix all" ruling under the fourteenth-redo
floor: the `evaluate` rows carry the read/emit split where the embargo term bites (9), this
unit's `business-rules.md` Sources list received the R-24-in/R-25-R-28-out correction its two
siblings already had (10), and R-76a's id is kept with the reason stated — renumbering would
break `models-and-baselines`' live citations under a frozen READY receipt (11a).

### What still stands, unchanged by any of this

**BLK-04 remains an exit condition** on this stage and on the four downstream units that
inherit the fit — FU-4 and FU-6 supply the mechanism its contract was missing, but **BLK-04
is not closed by this stage** and no implementation may proceed while it stands. NFR-LEAK-01's
evidence is still owed to the **Supervisor at G-04 and G-05**. TA-33/34/35/36 all `Pending` —
**a row is not a result**. `unit-of-work.md` § 7 stale, reported not edited. WS-13's departure
from TE §16 unresolved, with no reading adopted. FR-P1-04-10 with no acceptance row. The final
refit's representation. An unresolved station registry blocking `station_lat` and excluding
`lst_sin`/`lst_cos`, consumed not decided here. Rule numbering assumed to continue at **R-74**.
**G-09 unsigned.** No answer above decides a scientific constant, and none adopts a reading on
a supervisor-owned value.

**One consequence worth naming plainly.** FU-4 = D writes a requirement into the inbox of
`06`/`07` — units whose own design has not run yet. That is deliberate and declared, not a
side effect: BLK-04 is an exit condition on those units too, and `project.md` § Way of Working
requires the inputs a gating condition depends on to be specified in the stage that records
the condition.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded for `features-and-splits` and the three artifacts are **regenerated** — FU-4/5/6 mechanised, findings 4–7 applied, § Amendments owed re-derived to 8 across 5 — then put through a fresh adversarial reviewer pass. BLK-04 stays open.

- Request changes
   > **Impact**: No receipt, nothing regenerated. Use this to revisit FU-4, FU-5 or FU-6, or to challenge the reading of any finding above — including the four being applied without a decision.

> **💡 Recommendation**: **Looks correct** — the three answers supply mechanisms where five iterations found outcomes stated as mechanisms, FU-5 = D keeps 1 December in the locked test, and the four mechanical findings are corrections to what the artifacts already meant rather than changes to what they decide.

*(Answered `Looks correct` earlier on 2026-08-24; that receipt was reset by the authorised redo jump below. The live answer tag for this section is the blank one at its end.)*


### Re-confirmation, 2026-08-24 (post-redo) — receipt floor reset by an authorised redo jump

**Why this is being re-asked, and it is not about this unit.** The project decision owner
authorised a **redo jump on `functional-design`** at **2026-08-24T14:57:07Z**, so that three
standing reviewer findings on **`models-and-baselines`** (unit 8) could be fixed and
re-reviewed — its adversarial budget had been exhausted at NOT-READY, and the write-freeze on a
terminal review receipt made a redo the only route to a fix. **A redo resets the receipt floor for
every unit of the stage**, which is the stated cost that was accepted when the redo was chosen.

**Nothing in `features-and-splits` changed.** No question, option, answer, amendment, rule, entity or
workflow of this unit was touched after its earlier confirmation today. The only artifacts edited
after the redo are `models-and-baselines`'s; its three fixes are confined to its own
files and reach no contract this unit consumes.

**The redo bought what it was for.** `models-and-baselines` returned **READY** on the
second pass of the restored budget, after three further Major findings were fixed. Two residuals
ride that READY verdict and are carried to the stage gate rather than applied.

**Everything this unit carried to the gate still stands, unchanged**, as recorded above.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: The receipt is recorded for `features-and-splits` under the post-redo floor and its three artifacts are re-saved. No answer, rule, entity, count or scientific value changes.

- Request changes
   > **Impact**: No receipt is recorded and nothing is re-saved. Tell me what to change and I re-present first.

> **💡 Recommendation**: **Looks correct** — this unit is untouched; the reset is a mechanical consequence of a redo taken for a different unit, and that redo achieved what it was authorised for.

*(Receipt reset by the fourteenth authorised redo, 2026-08-26T08:18:34Z. The live answer tag is the blank one below.)*

### Re-confirmation, 2026-08-26 — under the fourteenth-redo floor

**This unit changed, and every change is the iteration-5 remediation you ruled on.** The 2026-08-24
remediation (FU-4 = D, FU-5 = D, FU-6 = A, confirmed above) had applied the two Criticals, the three
Majors and minors 6–7 — the provenance stamp with consumer refusal and the manifest-based test,
the read/emit split that keeps 1 December in the G-06 locked test, the three-call sequence, W-2's
signature block, § 10's two rows, and the amendment total re-derived to **8 across 5 units** — but
was never re-reviewed: the last recorded verdict is iteration 5's NOT-READY, which predates all of it.

**Fixed today (2026-08-26), completing your "fix all, stamp route" ruling** — the three findings
the 2026-08-24 pass left standing, plus one alignment sweep:

- **Finding 9**: the `evaluate` rows of both accepted-set tables now carry the read/emit split where
  the embargo term bites — an embargo row **emitted** under `evaluate` raises `LeakageError`; the same
  24 hours stay **readable** as the causal history the first `vtec_seq_24` window needs (W-4b).
- **Finding 10**: `business-rules.md`'s Sources list received the R-24-in / R-25-R-28-out correction
  its two sibling files got on 2026-08-23.
- **Finding 11a**: R-76a's id and filing position are **kept, with the reason stated**: renumbering to
  R-83 would break `models-and-baselines`' live "R-76a's third limb" citations under a frozen READY
  receipt. (11b's tree-revision half already carried its gate referral.)
- **Alignment sweep**: three more sites stating `evaluate`'s set flat as "exactly its validation
  month" (both element-4 tables and § 6's amendment box) now carry the same read/emit split, so no
  live sentence contradicts W-4b.

**Unchanged**: every answer Q1–Q9 and FU-4/5/6, all counts (rules R-74…R-82 plus R-76a, 10
workflows, 6 test modules, 39/5 accepted cells), BLK-04's status as an open exit condition, and
G-09 unsigned. The adversarial review under this floor runs next and verifies the whole remediation.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: Receipt recorded, artifacts re-saved natively, adversarial review dispatched to verify the full iteration-5 remediation.

- Request changes
   > **Impact**: Nothing recorded; tell me what to change.

> **💡 Recommendation**: **Looks correct** — the substantive mechanisms were confirmed by you at FU-4/5/6; today's additions are the three minors you ruled into scope and a consistency sweep, and the reviewer pass is what establishes READY, not this receipt.

*(Superseded the same day: the review this receipt anticipated returned NOT-READY on the ADR-11 Critical, and the artifacts were rebuilt on the owner’s ruling. The live tags are in the section below.)*

### Re-confirmation, 2026-08-26 — after the ADR-11 rebuild (owner-authorised)

The fourteenth-receipt review found every mechanism of both remediation waves targeting an
interface `component-methods.md` retired on 2026-08-23: **ADR-11** removed `apply_transforms`,
replaced `FoldSpec`/`build_folds` with `Partition`/`build_partitions`, returned a single
persisted **`FeatureBundle`** (matrix + tensor + `spec` + `transform_id`), and made the leak
check an **identity comparison** with one enumerated exception (`REFIT` → `DEC` under
`role="score"`, the G-06 apply). On your ruling the three design artifacts were **rebuilt on
that contract**, rule and section identities preserved (R-74…R-82 + R-76a; `models-and-baselines`'
citations of R-80 and R-76a's third limb remain valid), every superseded box kept as dated history.

**How your standing decisions mapped:**

- **FU-4 = D (stamp)** — dissolves into ADR-11: `FeatureBundle.transform_id`/`spec.partition_id`
  ARE the stamp, natively persisted across 05→06→07; consumer refusal restates as `06`/`07`
  raising on `transform_id is None` or identity mismatch; the test stays manifest/bundle-based;
  the residual restates as a **bundle-less frame**.
- **FU-6 = A (three calls)** — call count unchanged under ADR-11; "never persisted" superseded by
  `services.md` M9 (the raw bundle has a named `__untransformed/` address, deliberately visible);
  the load-bearing "never consumed" limb strengthened into a contract raise.
- **§ Amendments owed** — re-derives to **5 across 3 units** (was 8 across 5): all three of this
  unit's owed amendments were made unilaterally by ADR-11 at application-design.
  `models-and-baselines`' frozen READY artifacts still state "8 across 5" — **raised at the
  gate, not edited there**.
- **Iteration-5 finding 6** — the domain-entities § 4 regression the review found is fixed on the
  ADR-11 order.

**One conflict is put to you rather than resolved** (Question below): **FU-5 = D's December
clause**. FU-5 = D (2026-08-24, decided on the retired interface) ruled *"1 December stays in
the G-06 locked test with no first-day loss."* ADR-11 (2026-08-23) considered exactly that
mechanism (`lead_in_hours`) and removed it, honouring FR-P1-04-5 (*"no window crosses a
boundary; the first 24 h are excluded and counted"*), with the stated mandatory-disclosure
consequence: **1 December is not scored; the locked test covers 30 days, not 31** — and ADR-11
notes that enlarging the locked-test scored set is **supervisor-owned** (Vision §8.2, §8.7,
gate G-05). The rebuilt artifacts follow the approved contract and carry the conflict as a
dated box at W-4b, in R-74/R-81's mapping notes, in § 5, and as an Open item in all three
Assumptions lists. FU-5 = D's read/emit substance otherwise survives (spec-bound scored
ranges, containment controls, the causal history readable and never emitted).


### Re-confirmation — receipt, after the ADR-11 rebuild and FU-7

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: Receipt recorded, artifacts re-saved natively, iteration-2 adversarial review dispatched to verify the rebuild.

- Request changes
   > **Impact**: Nothing recorded; tell me what to change.

> **💡 Recommendation**: **Looks correct** — the rebuild preserves every decision that survives ADR-11, states each mapping in a dated box, and puts the one genuine conflict to you above instead of resolving it silently.

[Answer]: Looks correct

---

## Consolidated Summary Confirmation

**What changed in this unit since the last receipt.** Nine-site sweep of the stale claim that `foundation` R-01 "still reads all fourteen on disk" (it reads **fifteen**); `PartitionError` declaration-site **ruled** to `src/data/config.py`, resolving the dependency-matrix impossibility this unit raised; **G-09 signed (D-31)**.

**Governance recorded this pass.** **D-29** (`dataset_version` = first 12 hex of
`content_hash`, verify-on-write), **D-30** (`.dst_summary.json` relocation, performed and
hash-verified), **D-31** (**G-09 signed**, with its §18.3 preconditions recorded as
**unmet**), **D-32** (**all eight Vision §15.2 acceptance rows approved**, board option 1,
none deferred). Change records: `CHANGE_RECORD_2026-08-28_G09_signed.md`,
`CHANGE_RECORD_2026-08-28_dst_summary_relocation.md`.

**Execution evidence, and its exact limits.** Python **3.11.16** — the governed pin (TE §8.1, TC-03d) — obtained via `uv` and used to run the suites: **277 passed, 0 failed, 0 errors, 2 skipped** (both skips justified and recorded). Evidence packaged at `artifacts/exec_evidence/` with a SHA-256 manifest. **The runner was not pytest**: PyPI is unreachable in this environment, so a harness providing the pytest API surface was used; it has no plugins, no conftest and no assertion rewriting, and it **errors** rather than passes on an unsupported fixture. Two defects were found *by execution*: the access log could not evidence its own ordering (fixed — the guard now stamps `logged_at_utc` itself; 37 rows, 37 distinct monotonic instants), and the one-door assertion **failed against a file this session had just written**, which is the behaviour R-28 specifies.

⚠ **What is still NOT discharged, and this receipt does not claim otherwise:** TA-15, WS-18 and TA-18 have passing tests against **current** code, but their acceptance rows are discharged only at their own gates; `aws_ai_dlc_preflight_report` does not exist; `configs/` and the §18.3 zero-TBD preflight are unbuilt; and **D-31 records G-09's own preconditions as unmet**. Stage 3.1 remains **FAIL** and no board has passed it.

Does this all look correct before I generate the artifact?

- Looks correct
   > **Impact**: Receipt recorded, this unit's artifacts re-saved, and a fresh adversarial review dispatched against the post-execution state.

- Request changes
   > **Impact**: Nothing recorded for this unit; name what to change and it is corrected before any receipt is taken.

- Other (please specify)
   > **Impact**: Depends on what you specify.

> **💡 Recommendation**: **Looks correct** — every claim above is either a recorded decision, a hash-verified act, or a test result from a run whose runner limitations are stated; nothing here asserts a gate is discharged.

[Answer]:
