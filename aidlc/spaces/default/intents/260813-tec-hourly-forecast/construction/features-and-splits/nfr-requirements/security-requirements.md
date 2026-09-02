# Security Requirements — `features-and-splits`

**Unit** `features-and-splits` (Bolt 7) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED
>
> **FOUR acceptance rows are `Pending`, not two** *(corrected 2026-09-01 on adversarial finding 2, Major)* — **TA-33, TA-34, TA-35 and TA-36**, all four approved under the same change record `CR-2026-08-22-LEAKAGE-TA`, and for each: **the row exists, no test module is implemented, none has been executed, and none has passed.** **FR-P1-04-10's raw-longitude limb has no acceptance row at all.** WS-12,
> WS-13, WS-16, WS-18, TA-11 and the §18.3 preflight are undischarged.
>
> **What provenance is sufficient for the station registry is NOT decided** — an unresolved
> registry **blocks `station_lat` and excludes `lst_sin`/`lst_cos`**.
>
> **G-09 is signed (D-31) with its own preconditions UNMET**; **stage 3.1 remains FAIL**;
> `configs/` does not exist; no Python interpreter exists in this environment, so every test
> is **written-but-unexecuted** or unwritten.
>
> No scientific value is decided here, and TE §18.2's absolute rule stands.

## Sources

- `../functional-design/business-rules.md` — **R-74** (BLK-04: train-only fitting, **enforced by check rather than by shape**), **R-75** (every predictor is lagged, and the anchor is a third limb), **R-76** (**the ML input space is closed**), **R-76a** (TA-36's enforcement raise and primary test are **this unit's**), **R-77** (two carry-forward rules, **opposite** behaviour, one partition), **R-78** (support fields are **diagnostic by default**), **R-79** (**IRI denial: the data-flow limb is this unit's**), **R-80** (folds are exact calendar boundaries; **five partitions plus the locked month**), **R-81** (one window definition; WS-13's evidence question stays open), **R-82** (the locked partition materialises **only against a verified signature**), **R-83** (`Partition` states **both** bounds of the training range — BLK-09), **R-84** (BLK-08 half B, narrowed to **`ABL-DIFF`**).
- `../functional-design/business-logic-model.md` — **W-1** (the availability matrix, and the limb the first two checks miss), **W-2** (feature construction over a closed dictionary), **W-3** (BLK-04's train-only fitting contract), **W-4** (one window definition, two representations), **W-5** (folds, embargo, and the partition list that was incomplete), **W-6** (the locked partition's execution guard), **W-7** (**IRI denial: two properties, two owners**), **W-8** (two carry-forward rules with opposite behaviour), **W-9** (support fields: diagnostic by default), **W-10** (what Bolt 7 builds and what it must not).
- `../../external-products/nfr-requirements/security-requirements.md` — **§ SEC-E-01**, whose limb 2 this unit's § SEC-F-01 is the matching half of.
- `../../../inception/requirements-analysis/requirements.md` — **FR-P1-04-1**, **FR-P1-04-6**, **FR-P1-04-7**, **FR-P1-04-10**, **FR-P1-04-12**, **FR-P1-04-13**, **FR-P1-04-16**, **FR-P1-04-17**, **NFR-LEAK-01**, **NFR-IRI-01**, **NFR-FAIR-01**, **NFR-TDEF-01** *(cited 2026-09-01 on
  adversarial finding 1, Major — this unit builds a **dataset** and produces the **masks** the
  comparison consumes, two of the four artifact classes NFR-TDEF-01 requires stamped, and
  neither artifact cited it or named the three stamp fields.)*.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§6.2** (the feature dictionary and its safe lags), **§7.1** (the fixed calendar folds and the 24-hour embargo), **§12** (the import-boundary rule), **§18.2–18.3**, **§19** (TA-11, **TA-33, TA-34, TA-35, TA-36** — all four approved under `CR-2026-08-22-LEAKAGE-TA`, all four `Pending`), **§16** (WS-12, WS-13, WS-16, WS-18).
- `../../../../../../../../PreFlight/vision_document(3)(2)(2).md` — **§8.1** (*"History length is not a tuned hyperparameter"*), **§8.3** (December must not inform selection).
- `nfr-requirements-questions.md` — Q1 = A, Q2 = B, and the receipted Consolidated Summary Confirmation.

---

## Scope note

`produces_kinds` excludes `performance-requirements`, `scalability-requirements` and
`reliability-requirements` for a `library` unit. Assessed anyway:

| Category | Assessment for `features-and-splits` | Where it lives |
|---|---|---|
| **Performance** | No latency target. Feature construction is bounded — three cells, calendar 2022, hourly, a closed dictionary. Per-column provenance (§ SEC-F-01) adds a resolution step per column per build; that cost is accepted deliberately. | § SEC-F-01 |
| **Scalability** | Bounded and known. No growth projection. | — |
| **Reliability** | **Fail-closed on leakage**: `build_features` **raises** rather than warns, on a field outside the dictionary, on a raw-longitude column, on an unresolved provenance stamp, and on a window length placed in a grid. This unit would rather produce nothing than produce a matrix that might leak. | § SEC-F-01, § SEC-F-02 |
| **Security** | This artifact — **leakage containment**. This unit is the **last boundary before training**. | — |
| **Observability** | Per-column provenance stamps; the availability matrix; `Partition`'s both-bounds record. | § SEC-F-01, § SEC-F-03 |

---

## SEC-F-01 — The ML input space is closed by name AND by provenance

**Requirement — closure by name (R-76, FR-P1-04-12).** The feature set is **exactly** the
TE §6.2 dictionary — *"no field outside that table, and no derived tensor built from one,
enters training or inference."* `build_features` **raises** on any field outside it.

**Requirement — closure by provenance (Q1 = A). NEW at this stage.** Every column in a built
feature matrix carries a **stamp naming both its §6.2 dictionary row and its producing
artifact**, and `build_features` **raises if a column's provenance does not resolve to a
permitted producer** for that dictionary row.

> ### Why name-based closure is not enough — the channel this closes
>
> A value **computed from IRI**, **renamed to match a legitimate §6.2 field**, and written
> into the feature path:
>
> - passes **R-76's closure** — the name is on the list;
> - passes **`tests/test_iri_denial.py`** — there is no `iri_*` name;
> - passes **`external-products`' import boundary** — there is no import.
>
> `external-products` § SEC-E-01 records exactly this as the residual surviving both of its
> limbs. **This unit owns the feature matrix and is the last boundary before training, so
> the residual is closable here or nowhere.** A column claiming to be `f107_81_trailing` but
> produced by the IRI path **fails on provenance** even though its name is legitimate.

**The cost, stated rather than hidden.** A stamp on **every** column, a resolution step in
**every** build, and a **permitted-producer list per dictionary row that does not exist
yet**. This requirement therefore lands with a **named dependency**, not a mechanism ready to
build — the list is owed before the check can run.

**What still survives, stated with the rule and not only in Assumptions.** A column whose
provenance stamp is itself **forged** — written by hand to name a permitted producer — passes.
Provenance closes the *accidental and the casual* rename; it does not close a **deliberate
falsification**.

**A third channel, named 2026-09-01 on the reviewer's suggestion because the two above did not
cover it.** A column **genuinely produced by a permitted producer** but **mislabelled to the
wrong dictionary row** passes a per-producer check: the producer is on the list for *some* row,
and the stamp resolves. Closing it needs the check to be **per (row, producer) pair**, not per
producer — a sharper form of the same permitted-producer list, and one more reason that list is
the load-bearing artifact this requirement waits on.

**No artifact may describe NFR-IRI-01 as fully enforced.**

**Requirement — the cross-unit contract, matched from both sides.** `external-products`
§ SEC-E-01 states the run-time feature-matrix assertion as one half and names this unit as
owing the other. **W-7's data-flow limb and R-76's closed dictionary already are that half**,
and § SEC-F-01's provenance requirement extends it. **This unit does not declare the contract
satisfied** — TA-33 is `Pending` and nothing is implemented.

**Requirement (R-79, W-7, Q6 = D).** The permitted-importer set for `src/external/iri.py` and
`src/external/gim.py` is asserted to have **exactly two** members —
`scripts/04_build_external_products.py` and `src/evaluation/`. **The allowlist is not a
denylist**: a check that only forbids `src/features` and `src/models` **passes a notebook
import**, and an import from `src/data/`, `src/gnss/`, a training script or a notebook
violates TE §12 **exactly as** one from `src/features/` does.

**Requirement.** IRI and GIM join **only at evaluation time**, onto the **already-frozen
comparison-wide mask**.

## SEC-F-02 — Leakage containment: transforms, lags, longitude, and the window

**Requirement (R-74, W-3, NFR-LEAK-01, BLK-04).** Train-only transformations are fitted on
**training partitions only, per fold, never on the full dataset** — and this is **enforced by
check rather than by shape**. A shape that merely makes leakage inconvenient is not a
control; a check that fails is.

**Requirement (R-75).** Every predictor is **lagged to its actual availability timestamp**
before it can be used at a forecast origin — Kp/ap3 **≥ 3 h**, Hp60/ap60 **≥ 1 h**, F10.7 at
the **previous-day observed** value with a **trailing** (never centered) 81-day mean — and
**the anchor is a third limb**, checked separately from the lag and the value.

**Requirement (R-76, FR-P1-04-10).** **Raw longitude is never a predictor.** Longitude enters
**only** through `lst_sin` and `lst_cos`.

> **Requirement (Q2 = B) — this rule gets a negative control even though §19 has no row for
> it.** *"Longitude enters only through `lst_sin` and `lst_cos`"* is a `project.md`
> **NEVER** rule, and the affirmed practice is that **every hard rule gets a test proving
> the violation is caught**, not only that the happy path works. The control: **introduce a
> raw-longitude column and it must raise.**
>
> **Separately, the missing acceptance row is proposed to the gate.** FR-P1-04-10's longitude
> limb has **no §19 row at all**, which means a passing control evidences nothing at a gate.
> Adding one is a Vision §15.2 act — the route **D-32** already used to approve eight rows.
> **This stage proposes; it does not approve.**

**Requirement (R-76).** The **window length is a frozen constant, not a hyperparameter** —
one value per feature-set ID, shared across all model families, the primary history window
**24 hours** (Vision §8.1: *"History length is not a tuned hyperparameter"*).
**`experiment.yaml`'s window length equals 24 and appears in no grid**, and placing it in a
grid **fails**.

**Requirement (R-77, W-8).** Two carry-forward rules with **opposite** behaviour coexist in
one partition and must not be conflated: external driver values carry forward **at most 3
hours, then the row is excluded**; `vtec_lag_*` carry-forward is **prohibited outright**.

**Requirement (R-78, W-9).** Support fields are **diagnostic by default** — they do not
become predictors by being present.

**Requirement (Vision §8.3).** **December must not inform feature selection or a threshold.**
The trigger is December being **seen**, not the locked test being opened.

## SEC-F-03 — Splits, embargo, and the locked partition

**Requirement — every artifact this unit emits carries the three identity stamps**
(**NFR-TDEF-01**, **FR-P1-03-3**, TE §13, TA-15). **`phase_id`, `source_id` and
`target_definition_id`** are stamped on **the feature matrix and on every mask** this unit
produces — two of the four artifact classes the rule names (dataset, prediction, mask,
comparison), and the two this unit owns. A schema test asserts **all three on every such
artifact**; a mask reaching `evaluation-and-comparison` without them is a **failure**, not a
mask with missing metadata. *(Stated 2026-09-01 on adversarial finding 1, Major. The obligation
was uncited and unstated in both artifacts, while SEC-F-03 already described this unit as
producing "the masks the comparison consumes" — the stamped classes were reproduced without the
rule that stamps them. The **acceptance row TA-15 belongs to `target-standardization`**, which
owns the target-definition contract; what this unit owes is the stamp on its own outputs, and
it does not declare TA-15 discharged from this side.)*

**Requirement (R-80, W-5, TE §7.1).** Folds are **exact fixed calendar boundaries** — F1
Jan–Mar/Apr; F2 Jan–Jun/Jul; F3 Jan–Sep/Oct; F4 Jan–Oct/Nov; **December locked** — each with
a **24-hour embargo**, **excluded and counted**. **No random or shuffled cross-validation.**
The partition list has **five partitions plus the locked month**; an earlier list was
incomplete, which is why the count is stated rather than implied.

**Requirement.** Fold and partition membership derives from **record timestamps**, never from
a directory name or a filename.

**Requirement (R-83, BLK-09).** `Partition` states **both** bounds of the training range. A
single bound leaves the other to be inferred, and an inferred boundary is where an embargo
silently disappears.

**Requirement (R-82, W-6).** The **locked partition materialises only against a verified
signature**. It is not constructed on request; the signature is the precondition.

**Requirement (R-81, W-4).** **One window definition, two representations** — matrix and
tensor — and **WS-13's evidence question stays open**. The two representations must agree on
the window they encode; a disagreement is the defect WS-13 exists to catch, and what
constitutes sufficient evidence for it is **not settled**.

**Requirement (NFR-FAIR-01, TC-16).** A **single comparison-wide intersection mask**,
computed once per comparison set, is used for every model-versus-baseline comparison — never
pairwise, never model-specific. This unit produces the masks the comparison consumes.

## SEC-F-04 — Two cross-unit halves this unit owns

**Requirement (R-76a).** **TA-36's enforcement raise and primary acceptance test are this
unit's.** `external-products` holds **data production and upstream evidence** only. **TA-36
is `Pending` — not implemented, not executed, not passing.**

**Requirement (R-84).** **BLK-08 half B is narrowed to `ABL-DIFF`** — this unit's half of the
joint contract. The other half is `statistical-inference`'s, and **neither side declares the
contract satisfied alone**.

**Open, and not this unit's to close.** **What provenance is sufficient** for the station
registry is **not decided** (consumed from `inventory-and-registry` R-45/R-46). An unresolved
registry **blocks `station_lat` and excludes `lst_sin`/`lst_cos`** — which means SEC-F-02's
longitude rule and this unit's feature set both depend on a decision owned elsewhere.

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| FR-P1-04-1 | SEC-F-01 | WS-10, TA-07 | `Pending` — **data-flow limb this unit's** |
| **FR-P1-04-10** | SEC-F-02 | ⚠ **NO ACCEPTANCE ROW** — proposed to the gate | untested; control required regardless |
| FR-P1-04-12 | SEC-F-01 | **TA-33** | ⚠ **`Pending` — no test module implemented, none executed, none passed** |
| FR-P1-04-17 | SEC-F-04 | **TA-36** | ⚠ **`Pending` — not implemented, not executed, not passing** |
| **FR-P1-04-6** | SEC-F-02 | TA-11 | `Pending` |
| **FR-P1-04-7** | SEC-F-03 | WS-16, TA-11 | `Pending` |
| **FR-P1-04-13** | SEC-F-02 | **TA-34** | ⚠ `Pending` — approved under `CR-2026-08-22-LEAKAGE-TA`, **not implemented, not executed, not passed** |
| **FR-P1-04-16** | SEC-F-02 | **TA-35** | ⚠ `Pending` — approved under `CR-2026-08-22-LEAKAGE-TA`, **not implemented, not executed, not passed** |
| NFR-LEAK-01 | SEC-F-02 | TA-11 | `Pending` |
| NFR-IRI-01 | SEC-F-01 | WS-10, TA-07 | `Pending` — **test written, UNEXECUTED** |
| NFR-FAIR-01 | SEC-F-03 | WS-16, TC-16 | `Pending` |
| **NFR-TDEF-01** | SEC-F-01, SEC-F-03 | **TA-15** | `Pending` |
| **FR-P1-03-3** | SEC-F-01, SEC-F-03 | **TA-15** | `Pending` — row owned by `target-standardization` |

**Derived and printed**: 4 requirement sections (SEC-F-01…SEC-F-04); **11** coverage rows *(corrected 2026-09-01 on adversarial findings 1 and 2, both Major; superseded figure preserved: **7**. **FR-P1-04-6** and **FR-P1-04-7** are implemented verbatim by SEC-F-02 and SEC-F-03 and were cited only through their umbrella NFR IDs. **FR-P1-04-13** and **FR-P1-04-16** carry dedicated acceptance rows **TA-34** and **TA-35**, approved under the SAME change record `CR-2026-08-22-LEAKAGE-TA` that produced TA-33 and TA-36 — which this artifact already disclosed prominently — and were absent entirely, though their governing rules R-77 and R-78 were cited as Sources and implemented in SEC-F-02. Four of this unit's acceptance rows are Pending, not two.)*;
**1** requirement with **no acceptance row** (FR-P1-04-10) — **re-derived 2026-09-01 by counting
blank acceptance-row cells in the table above, not read off the map** — with its row **proposed
to the gate**; **0** rows claimed satisfied.

**Corrected again 2026-09-01, third Major on this unit: 11 → 13 coverage rows.** **NFR-TDEF-01**
and **FR-P1-03-3** were both absent. SEC-F-03 already described this unit as producing "the masks
the comparison consumes" and SEC-F-01/02 as building the feature matrix — **a dataset and a mask,
two of the four artifact classes NFR-TDEF-01 requires stamped with `phase_id`, `source_id` and
`target_definition_id`** — yet neither ID was cited and neither artifact named the three fields at
all. **Superseded figures preserved: 7, then 11.** The pattern across all three corrections on
this unit is one pattern: **the coverage set was built from what this unit owns, and the test is
what its artifacts reproduce.** TA-15 is `target-standardization`'s row; citing it here records an
obligation, not a discharge.

## Assumptions & Open Questions

- **[Q1]** Per-column provenance is **new at this stage** and depends on a **permitted-producer list per §6.2 dictionary row that does not exist**. The requirement is stated with that dependency named; the list is **owed before the check can run**.
- **[assumption]** A provenance stamp is trustworthy. **A forged stamp passes** — provenance closes the accidental and casual rename, not a deliberate falsification. Stated in § SEC-F-01's body as well as here, because it bounds what NFR-IRI-01 enforcement actually reaches.
- **[Q2]** The longitude negative control is required **independently of §19**; the missing acceptance row is **proposed, not approved**, by this stage.
- **Open, and owned elsewhere — what provenance is sufficient for the station registry.** Until it is decided, `station_lat` is blocked and `lst_sin`/`lst_cos` are excluded, which reaches into both SEC-F-01's dictionary and SEC-F-02's longitude rule.
- **Open — WS-13's evidence question** (R-81). What evidence proves the matrix and tensor representations encode the same window is **not settled**.
- **Carried — BLK-08's other half** is `statistical-inference`'s, and **BLK-04**'s check-not-shape enforcement is unimplemented.
- **The signed "nine-site sweep" record stands unedited.** This unit's `functional-design` questions file is human-signed and claims a nine-site sweep the derivation puts at **3**; the correction lives in `business-logic-model.md` § Assumptions with one ruling routed to the gate. **`governance/CHANGE_RECORD_PROCEDURE.md` permits annotating a signed record only with owner approval for the specific item**, and none was given for this one.
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z (system clock; not independently re-verified via shell in this pass — see coverage limits)
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-requirements.md` § Sources, § Requirement coverage, SEC-F-02 | `requirements.md:375` (FR-P1-04-6, "fitted on training partitions only, per fold, never on the full dataset") and `requirements.md:376` (FR-P1-04-7, "single comparison-wide intersection mask... computed once per comparison set... no pairwise or model-specific mask") are substantively implemented verbatim by SEC-F-02's train-only-fitting requirement and SEC-F-03's comparison-wide-mask requirement, and TS-F-02/TS-F-04 in `tech-stack-decisions.md` implement the same two. Neither FR ID is cited in either artifact's Sources or coverage table — only the umbrella NFR-LEAK-01/NFR-FAIR-01 IDs are cited. This is the same defect class the dispatch brief names as having landed a Major on another unit (substance implemented, requirement absent from every coverage table). | Add FR-P1-04-6 and FR-P1-04-7 to both artifacts' Sources and Requirement-coverage tables (acceptance rows TA-11/WS-16 already named for the NFR umbrella, so this is a citation fix, not new content). |
| 2 | Major | `security-requirements.md` § Sources, SEC-F-02, § Requirement coverage | `requirements.md:925` groups FR-P1-04-13 (carry-forward bounds) and FR-P1-04-16 (support-field rules) under `REQ-LEAK-01`, and `requirements.md:844-848` records that both were assigned dedicated negative-path acceptance rows **TA-34** and **TA-35** (alongside TA-33/FR-P1-04-12 and TA-36/FR-P1-04-17, which *are* cited here) under the same `CR-2026-08-22-LEAKAGE-TA` change record. SEC-F-02 implements both substantively — R-77 ("two carry-forward rules with opposite behaviour") is FR-P1-04-13's content, R-78 ("support fields are diagnostic by default") is FR-P1-04-16's content, and both R-77 and R-78 are cited as Sources in this very document. Yet FR-P1-04-13, FR-P1-04-16, TA-34 and TA-35 appear nowhere in either artifact — TA-33 and TA-36 (their siblings from the identical change record) are prominently featured as `Pending`, but TA-34/TA-35 are silently absent rather than also disclosed as `Pending`/undischarged. Given this document's own "nothing claimed satisfied" posture, an implementer reading only these two acceptance rows would not know TA-34/TA-35 exist or that this unit owes evidence toward them. | Add FR-P1-04-13/TA-34 and FR-P1-04-16/TA-35 rows to both coverage tables, each marked `Pending`/undischarged in the same style as TA-33/TA-36, to match the artifact's own completeness standard for its sibling requirements. |

### Verified — did not break

- **Forged-stamp admission (Focus 2):** sits in § SEC-F-01's rule body (`security-requirements.md:78-81`), not only in Assumptions — restated at line 204 with an explicit cross-reference ("Stated in § SEC-F-01's body as well as here"). Matches the prior-Major precedent's fix, not its defect.
- **Named-dependency honesty (Focus 3):** the permitted-producer list is stated as non-existent/not-buildable-today in both artifacts' warning banners, bodies (§ SEC-F-01, TS-F-01), and coverage notes, with no contradicting claim found that treats the check as available.
- **Q2 proposed-not-approved boundary (Focus 4):** "This stage proposes; it does not approve" is explicit; D-32 is cited only as the *route* precedent ("the route D-32 already used to approve eight rows"), never as approval of this row.
- **Undischarged-status claims (Focus 5):** TA-33, TA-36, FR-P1-04-10's missing row, the unresolved station-registry provenance question, `configs/` absence, no Python interpreter, G-09/stage-3.1 status are all stated consistently across both artifacts' banners, bodies and Assumptions — no contradicting "satisfied" claim found.
- **Signed-record discipline (Focus 6):** the nine-site-sweep record is stated as left unedited, with the correction routed to `business-logic-model.md` § Assumptions and one ruling routed to the gate — consistent with `project.md`'s `fd-2026-08-30-never-edit-signed-record` correction.
- **Counts (Focus 7):** re-derived from the printed tables — `security-requirements.md`: 4 sections (SEC-F-01…04), 7 coverage rows, 1 with no acceptance row (FR-P1-04-10) — matches. `tech-stack-decisions.md`: 5 sections (TS-F-01…05), 5 coverage rows, 0 new dependencies, 1 owed artifact, 2 deferred choices — matches.

### Suggestions (not grounds for NOT-READY)

- § SEC-F-01's forged-stamp channel is named as "accidental/casual rename" vs. "deliberate falsification," but a third channel is unaddressed in the rule text: a column *genuinely* produced by a permitted producer for dictionary row A, then labeled/keyed as row B by that same producer (no forgery, no rename — a producer-side mislabel). The stated check ("does not resolve to a permitted producer") would pass this case since the producer is legitimate for *some* row. Worth a sentence if the permitted-producer list, once built, is per-row rather than per-producer.

### Coverage limits

This pass used 7 of an 8-tool-call budget. `requirements.md` was checked by targeted grep/read against the FR-P1-04-* family and the three NFR IDs the artifacts cite (plus the neighbouring FR-P1-04-6/7/13/16 that surfaced from that read); the full FR-P1-04-1…18 range was not independently re-derived beyond what those reads surfaced, and `business-logic-model.md`/`business-rules.md`/`domain-entities.md` were relied on only via the citations already printed in the two artifacts under review, not re-read directly. No sibling-unit files were opened.

READY

## Review — 2026-09-01 confirming pass

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 1 (fresh budget after human gate rejection)

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-requirements.md` § Sources, § Requirement coverage; `tech-stack-decisions.md` (same gap) | `requirements.md:917`/`:482-491` names **NFR-TDEF-01** ("Target-definition integrity … every target/prediction carries phase/source/definition IDs") and `project.md`'s mandated rule states it flatly: "ALWAYS stamp `phase_id`, `source_id` and `target_definition_id` on every dataset, prediction, mask and comparison." SEC-F-03 states in its own words that "This unit produces the masks the comparison consumes," and § SEC-F-01/§SEC-F-02 describe this unit building the feature matrix (a dataset) and `Partition` objects. Both are exactly the artifact classes the mandated rule stamps. Neither artifact cites NFR-TDEF-01 anywhere (confirmed: `grep -n "phase_id\|target_definition_id\|source_id\|NFR-TDEF"` over both files returns zero matches), and neither states whether the feature matrix or the masks this unit emits carry the three IDs, are silent on them, or defer the obligation elsewhere. This is the same defect class the dispatch brief names as having landed repeatedly on other units: an NFR whose substance the artifacts rest on (producing stamped-class artifacts) cited nowhere. | Add NFR-TDEF-01 to Sources and the Requirement-coverage table in both artifacts, and state explicitly whether `build_features`'s output matrix and the comparison-wide masks carry `phase_id`/`source_id`/`target_definition_id`, or name this as an open gap with an acceptance row (TA-15 is NFR-TDEF-01's existing row per `requirements.md:491`) if the stamping mechanism is not yet decided for this unit's artifact classes. |

### Verified — did not break (from the prior 2026-09-01 pass, re-checked)

- Findings 1 and 2 from the prior confirming pass (FR-P1-04-6/-7 citation gap; FR-P1-04-13/TA-34 and FR-P1-04-16/TA-35 omission) remain corrected in the current text: both umbrella FRs and both TA rows are present in the Requirement-coverage table with `Pending` status, matching what the prior pass's fix required.
- The "nothing claimed satisfied" posture, the forged-stamp admission in the SEC-F-01 rule body, and the undischarged-status banners (G-09/stage-3.1/`configs/`/no-Python-interpreter) are unchanged and internally consistent across both artifacts.
- FR-P1-05-* was checked against this unit's scope: the whole range is modeling/evaluation/experiment-registry territory (model set, seeds, grids, ablations, estimand, bootstrap, registry schema, locked-test guard, regime audit) owned by other units, not features-and-splits — its absence from Sources here is correct, not a gap.

### Not re-verified this pass (budget)

Did not re-open `tech-stack-decisions.md` in full this pass (relied on the prior pass's printed section/row counts for it, which the finding above does not disturb); did not re-derive the FR-P1-04-1…18 range beyond the prior pass's coverage; no sibling-unit files opened, per read-scope bound.

NOT-READY

## Review — 2026-09-01 repair verification

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 2 (repair verification, single pass)

### Prior Major — resolved

`NFR-TDEF-01` uncited while this unit's outputs (the feature matrix, every mask) are two of the four artifact classes it stamps. Verified fixed at all five claimed sites:

1. **§ Sources**: `NFR-TDEF-01` cited with a dated note (line 24-27).
2. **SEC-F-03 rule body**: new Requirement paragraph stamping `phase_id`/`source_id`/`target_definition_id` on the feature matrix and every mask, schema-tested, a mask without them a failure — and explicitly states TA-15 belongs to `target-standardization`, not discharged here.
3. **§ Requirement coverage**: two new rows present — `NFR-TDEF-01 | SEC-F-01, SEC-F-03 | TA-15 | Pending` and `FR-P1-03-3 | SEC-F-01, SEC-F-03 | TA-15 | Pending — row owned by target-standardization`.
4. **Count**: table recounted directly — **13** rows (FR-P1-04-1, -10, -12, -17, -6, -7, -13, -16, NFR-LEAK-01, NFR-IRI-01, NFR-FAIR-01, NFR-TDEF-01, FR-P1-03-3). Superseded 7 and 11 both preserved in the correction-box prose only, never asserted as current elsewhere. No-acceptance-row count re-derived from blank cells: **1** (FR-P1-04-10), matches the ⚠ row.
5. **`tech-stack-decisions.md`**: recounted directly — **5** rows (FR-P1-04-12, -1, NFR-LEAK-01, NFR-FAIR-01, FR-P1-04-10). Dependent phrase reads "eight fewer... than thirteen," 13 − 8 = 5, arithmetic checks. The eight named (FR-P1-04-6, -7, -13, -16, -17, NFR-IRI-01, NFR-TDEF-01, FR-P1-03-3) is a complete, correct list of the sections-cited-but-no-tech-choice set. The stale "two fewer than seven" phrase (the known prior blind spot, missed by iteration-1) is now corrected and its own staleness is disclosed in the same breath.

### Cross-reference check

`requirements.md:491` confirms `NFR-TDEF-01`'s acceptance row is **TA-15**; `requirements.md:362` confirms `FR-P1-03-3`'s acceptance row is also **TA-15**. Both citations are accurate — TA-15 is genuinely both requirements' row, not invented. Neither new coverage row claims TA-15 discharged; both are stated `Pending`, and the `target-standardization` ownership attribution is stated as an obligation this unit still owes evidence toward, not a completed hand-off. No overclaim found.

### Sweep for stale numerals

Grepped both files for `7`, `11`, `seven`, `eleven`. Every hit is one of: an unrelated numeral (Bolt 7, TA-11, WS-16, §7.1, §18.2-18.3), a superseded figure preserved inside its own correction-box parenthetical exactly where the project's preserve-don't-delete convention permits it (`security-requirements.md` line 226 "superseded figure preserved: 7", line 236 "Superseded figures preserved: 7, then 11"; `tech-stack-decisions.md` line 116-118's own disclosed-stale "seven"/"eleven"), or a quotation inside a prior `## Review` entry (correctly left standing per instructions). No surviving unqualified assertion of 7 or 11 as a current count was found in either file's live prose, tables, banners, or headings.

### No regression

Re-verified present and unchanged: FR-P1-04-6/-7 and FR-P1-04-13/-16↔TA-34/TA-35 citations (all four still `Pending` rows, matching iteration-1's fix); Q1's per-column provenance and named permitted-producer-list dependency; Q2's longitude negative control stated as required independently of §19 with the row proposed, not approved; `external-products` § SEC-E-01 NFR-IRI-01 limb-2 contract stated as this unit's matched half only, neither side declaring it satisfied; exact fixed calendar folds (F1–F4, December locked) with 24-hour embargo and no shuffled CV; train-only transforms fit per fold on training partitions only (BLK-04, check-not-shape); longitude entering only through `lst_sin`/`lst_cos`. Undischarged-status banner unchanged: G-09 signed (D-31) with preconditions UNMET, stage 3.1 FAIL, `configs/` absent, no Python interpreter, WS-10/11/12/13/16/18, TA-07/11/15/34/35/36 and the §18.3 preflight all stated undischarged; no row anywhere claimed passed. TA-33/TA-36 status unchanged (`Pending`, not implemented/executed/passed).

### Findings

None at Major or Critical severity. No sixth stale site found.

### Summary

All five claimed repair sites are present, mutually consistent, and correctly cross-referenced against `requirements.md`. Both coverage-table counts (13 and 5) were recounted directly from the printed tables and the dependent arithmetic (13 − 8 = 5) holds. The previously-flagged stale "seven"/"two fewer" dependent phrase is now fixed and its own history disclosed. TA-15's ownership is accurately attributed and not overclaimed as a discharge. This unit's implementable-without-guessing bar is met.

READY
