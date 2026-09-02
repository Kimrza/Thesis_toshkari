# NFR Requirements — Questions — `features-and-splits`

**Unit** `features-and-splits` (Bolt 7) · **Kind** `library` · **Stage** `nfr-requirements`

Two artifacts only — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit.

**Not re-asked, because `functional-design` already decided them.** BLK-04's train-only
fitting **enforced by check rather than by shape** (R-74, W-3); every predictor lagged with
the anchor as a third limb (R-75); TA-36's enforcement raise and primary test being **this
unit's** (R-76a); the **closed ML input space** — exactly the TE §6.2 dictionary, raising on
any field outside it, with window length a **frozen constant not a hyperparameter** and raw
longitude never a predictor (R-76); two carry-forward rules with **opposite** behaviour in
one partition (R-77, W-8); support fields **diagnostic by default** (R-78); the **data-flow
limb of IRI denial being this unit's**, with the permitted-importer set asserted to have
**exactly two** members (R-79, W-7, Q6 = D); folds as exact calendar boundaries with **five
partitions plus the locked month** (R-80, W-5); one window definition in two representations
(R-81, W-4); the locked partition materialising **only against a verified signature** (R-82,
W-6); `Partition` stating **both** bounds of the training range (R-83, BLK-09); BLK-08's
half B narrowed to **`ABL-DIFF`** (R-84).

**Already this unit's, and not re-opened.** `external-products` § SEC-E-01 states a
run-time content assertion at the feature-matrix boundary as **one half of a cross-unit
contract**, with this unit owing the other. **W-7 and R-76 already are that half** — this
stage records the contract as **matched from both sides**, and asks only about the residual
neither side closes (Question 1).

---

## Question 1

R-76 closes the ML input space **by field name**: the feature set is exactly the TE §6.2
dictionary, and `build_features` **raises** on any field outside it. R-79's data-flow limb
and `tests/test_iri_denial.py` catch an injected **`iri_*`** field.

Both are **name-based**. A value computed from IRI, **renamed to match a legitimate §6.2
dictionary field**, and written into the feature path passes R-76's closure (the name is on
the list), passes the IRI denial test (no `iri_*` name), and passes `external-products`'
import boundary (no import). `external-products` § SEC-E-01 already records this as the
residual that survives both its limbs.

What should `security-requirements.md` require of this unit, which owns the feature matrix?

A. **Per-column provenance**: every column in a built feature matrix carries a stamp naming both its §6.2 dictionary row **and its producing artifact**, and `build_features` raises if a column's provenance does not resolve to a permitted producer
   > **Impact**: Closes the renamed-value channel — a column claiming to be `f107_81_trailing` but produced by the IRI path fails on provenance even though its name is legitimate. It adds a stamp to every column and a resolution step to every build, and it needs a list of permitted producers per dictionary row that does not exist yet.

B. Keep name-based closure and **state the residual** where the rule is read, as `external-products` now does
   > **Impact**: No new mechanism, no new list to maintain, and the residual is disclosed rather than hidden. The project's most load-bearing scientific rule then has a known, documented bypass that requires only renaming a column — and this unit is the last place it could be caught.

C. Require the denial test to compare **values** against the IRI benchmark table and fail on a match
   > **Impact**: Catches a renamed IRI value by what it is rather than what it is called, with no provenance machinery. It cannot run before the IRI benchmark exists — and IRI generation is **blocked** on a validation that has not happened — so the check would be specified against an artifact that does not exist, and a legitimate feature could coincide with a benchmark value.

X. Other (please structure)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — this unit owns the feature matrix and is the **last** boundary before training, so the residual is closable here or nowhere. The honest cost is that the permitted-producer list is new work and does not exist, so the requirement lands with a named dependency rather than a mechanism ready to build. Option C is unbuildable in the current order: it needs the IRI benchmark, which is blocked. Option B is defensible and cheapest, and it accepts a documented rename as a bypass of NFR-IRI-01.

[Answer]: A

---

## Question 2

R-76 records that **FR-P1-04-10's raw-longitude limb has no acceptance row at all**, and
**TA-33 is `Pending` — the row exists, no test module is implemented, none has been executed,
and none has passed**. R-76 nonetheless specifies a negative control for the longitude limb:
introduce a raw-longitude column and it must raise.

The project's affirmed practice is that **every hard rule gets a test proving the violation
is caught**, not only that the happy path works.

What should this unit's artifacts require for a rule whose §19 row is absent?

A. The negative control is **required regardless of whether a §19 row exists**, and its absence from §19 is recorded as an **acceptance-coverage gap owned outside this unit**
   > **Impact**: Keeps the test obligation where the rule is, which is what `team.md`'s negative-control practice actually says, and makes the missing row visible as a governance gap rather than an excuse. It creates a test with no §19 row to report into, so passing it evidences nothing at a gate until the row exists.

B. Require the negative control **and** propose the missing acceptance row to the gate
   > **Impact**: Closes both halves — the mechanism and the evidence path. Proposing a §19 row is a Vision §15.2 act with an approval history in this project (D-32 approved eight such rows), so it is a known route, but it puts a decision in front of the owner that this stage cannot take itself.

C. Follow §19: no row, no required test
   > **Impact**: Internally consistent with the acceptance framework and adds nothing unbudgeted. It would leave *"longitude enters only through `lst_sin` and `lst_cos`"* — a `project.md` **NEVER** rule — with no test at all, which is the coverage posture `GOV-F-06` warned against.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B — the negative control is required by the affirmed practice independently of §19, and the missing row is a real gap that D-32's precedent shows can be closed by the owner. Option C reads the acceptance framework as permission not to test a rule the project lists under `## Forbidden`. The cost of B is one more decision routed to the gate, which is the right place for it.

[Answer]: B

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. Nothing below decides a
scientific value, and nothing claims a gate or acceptance row is discharged.

**Scope.** Two artifacts — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit. Those categories are still
assessed in the security artifact's scope note.

**Q1 = A — feature columns carry per-column provenance.** Every column in a built feature
matrix carries a stamp naming both its **TE §6.2 dictionary row** and its **producing
artifact**, and `build_features` **raises** if a column's provenance does not resolve to a
permitted producer. **This closes the renamed-value channel**: a column named
`f107_81_trailing` but produced by the IRI path fails on provenance even though its name is
on the list — the residual that survives R-76's name-based closure, `tests/test_iri_denial.py`'s
`iri_*` check, and `external-products`' import boundary alike. **This unit owns the feature
matrix and is the last boundary before training, so the residual is closable here or
nowhere.**

**The cost is stated, not hidden.** A stamp on every column, a resolution step in every
build, and a **permitted-producer list per dictionary row that does not exist yet** — so the
requirement lands with a named dependency rather than a mechanism ready to build.

**Q2 = B — the longitude negative control is required, and the missing row is proposed.**
*"Longitude enters only through `lst_sin` and `lst_cos`"* is a `project.md` **NEVER** rule, so
its negative control is required by the affirmed every-hard-rule-gets-a-test practice
**independently of §19**. Separately, **FR-P1-04-10's longitude limb has no acceptance row at
all**, and that missing row is **proposed to the gate** as a Vision §15.2 act — the route
D-32 already used to approve eight such rows. **This stage proposes; it does not approve.**

**The cross-unit IRI contract is matched from both sides.** `external-products` § SEC-E-01
states the run-time feature-matrix assertion as one half; **W-7's data-flow limb and R-76's
closed input space are this unit's half**, and they already exist in `functional-design`.
This stage records the contract as **matched**, and Q1 addresses only the residual **neither**
side closes.

**Carried, not re-decided.** R-74's BLK-04 train-only fitting enforced by **check rather than
shape**; R-75's lagging with the anchor as a third limb; R-76a's TA-36 enforcement raise and
primary test as **this unit's**; R-76's closed dictionary, **24-hour window as a frozen
constant appearing in no grid**, and raw-longitude prohibition; R-77's two opposite
carry-forward rules; R-78's diagnostic-by-default support fields; R-79/W-7's **exactly two**
permitted importers; R-80's exact calendar folds with **five partitions plus the locked
month** and the 24-hour embargo; R-81's single window definition; R-82's verified-signature
gate on the locked partition; R-83's both-bounds `Partition` (BLK-09); R-84's `ABL-DIFF`
narrowing (BLK-08 half B).

**Status claims made.** None. **TA-33 is `Pending` — the row exists, no test module is
implemented, none executed, none passed.** **FR-P1-04-10's longitude limb has no row.**
TA-36 is `Pending`. WS-18's guard is undischarged. **What provenance is sufficient for the
station registry is not decided** — an unresolved registry blocks `station_lat` and excludes
`lst_sin`/`lst_cos`. G-09 is signed (D-31) with preconditions UNMET; stage 3.1 remains FAIL;
`configs/` does not exist; no Python interpreter exists here, so every test is
written-but-unexecuted or unwritten.

**The signed "nine-site sweep" item stands unedited.** This unit's `functional-design`
questions file is a human-signed record whose "nine-site sweep" claim was derived as **3**;
the correction lives in `business-logic-model.md` § Assumptions with one ruling routed to the
gate, and **the signed text is not edited**.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
