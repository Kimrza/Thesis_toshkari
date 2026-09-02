# NFR Requirements — Questions — `evaluation-and-comparison`

**Unit** `evaluation-and-comparison` (Bolt 9) · **Kind** `library` · **Stage** `nfr-requirements`

Two artifacts only — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit.

**Not re-asked, because `functional-design` already decided them.** BLK-08's joint
transform-resolution contract **narrowed to `ABL-DIFF`**, stated once in two halves (R-103,
W-3); **inverse-before-metric enforced at the boundary every caller crosses** (R-104);
`07`'s **stamp refusal** at this unit's boundary (R-105, W-4); comparison-set membership as
**declared configuration, checked exactly** (R-106); **mask identity, once-only registration
and the G-05 freeze** (R-107, W-1); the estimand as an **ordered executable contract** whose
result **carries its own interpretation** (R-108, W-2); the G-06 evaluation — **hash-receipt
before metrics, one chokepoint, exactly 2–31 December** (R-109, W-5); the honesty mechanics —
**completeness upstream, the disclosure trigger as a field, the caveat emitted by the path**
(R-110, W-6); `tests/test_common_masks.py`'s masks-plus-matched-window assertion and the
WS-13 proposal (R-111, W-8); IRI and GIM joining at evaluation time onto the frozen mask,
**this unit narrowing nothing** (R-112).

**Carried, not decided here.** **FR-P1-05-7's row is `Pending` — APPROVED under D-32
(2026-08-28), never run, NOT passed.** An approved-but-unrun row and an absent row are both
`Pending`, and **neither is evidence**.

---

## Question 1

**FR-P1-05-17 is `UNTESTED` and has no acceptance row at all.** What it governs is an
**ordering**: the comparison-wide mask must be **frozen before** the locked test is accessed.
W-1 step 4 produces the frozen bundle; W-5 carries the freeze-precedes-access ordering.

The design records that ordering as a property of the **G-05 record** — something a reader
checks after the fact. A mask frozen *after* December was opened would produce a comparison
whose mask could have been shaped by what December contained, and nothing in the pipeline
would stop it.

What should `security-requirements.md` require?

A. **Machine-enforced ordering**: the locked-test access path **refuses** unless a registered, frozen mask bundle exists whose registration timestamp **precedes** the access, and the refusal is a hard failure rather than a warning
   > **Impact**: Turns an after-the-fact record property into a precondition checked at the moment it matters, closing a window in which the project's fairness guarantee could be shaped by the test set. It couples this unit's mask registry to `governance-guards`' access path — a cross-unit contract this stage can state only one half of — and **that path does not exist** while BLK-07 is open.

B. Keep it as a **record property** and require the ordering to be an explicit, named G-05 review item
   > **Impact**: No new cross-unit coupling, and G-05 is a human gate that can genuinely check a timestamp pair. It leaves the guarantee resting on a reviewer noticing an ordering among many G-05 items, and the artifact that would reveal a violation is produced by the same run that committed it.

C. Require both — the refusal, **and** the named G-05 review item
   > **Impact**: Strongest, and matches the two-limb pattern used elsewhere in this project for rules that matter. It duplicates one obligation in two places, which this project has recorded as how two statements of one fact drift apart.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — a mask frozen after December was seen is a fairness failure that no downstream check can detect, because the mask is what every comparison is measured through. The cross-unit cost must be stated honestly as a half-contract, and so must the fact that it is **unrunnable while BLK-07 is open** — the same posture `models-and-baselines` takes for its December-window block. Option B's weakness is specific: the run that violates the ordering is the run that writes the record proving it.

[Answer]: A

---

## Question 2

R-108 makes the estimand an ordered executable contract and says its result **carries its own
interpretation**. The estimand is the **mean within-station difference of squared errors,
benchmark minus model, with equal-station weighting** — and **a positive value favours the
model**.

That sign convention is the entire thesis conclusion. Reversing it turns *"the LSTM beats
IRI"* into *"IRI beats the LSTM"*, and the number itself looks identical either way. The
project already treats a sign as this dangerous elsewhere: TA-07/WS-04 require a **reversed-sign
negative control** on DCB.

What should the artifacts require of the estimand's sign?

A. The sign convention **travels as data**: every emitted estimand value carries a field naming its orientation (`benchmark_minus_model`) and its weighting (`equal_station`), and a consumer that reports the value without them **fails**
   > **Impact**: Makes the most consequential number in the thesis self-describing, so a value cannot be read under the wrong convention downstream. It obliges reporting units to carry and check fields they did not ask for — a cross-unit half-contract — and adds fields to every emitted result.

B. A **reversed-sign negative control** on the estimand, on the DCB precedent: a deliberately inverted computation must fail the test
   > **Impact**: Proves the implementation computes the convention it claims, using a pattern this project already runs and trusts. It verifies the *producer* and says nothing about a *consumer* reading a correct value under the wrong assumption, which is the failure mode a written convention in a document invites.

C. Both — the carried fields **and** the reversed-sign control
   > **Impact**: Covers producer and consumer, which are genuinely different failures. It is two mechanisms for one property, and the duplication risk this project has recorded applies.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C — and unusually, the duplication objection does not apply here, because the two mechanisms check **different things**: the control proves the producer computes `benchmark − model`, the carried field prevents a consumer reporting it as `model − benchmark`. Neither substitutes for the other, which is the same reasoning `governance-guards` R-23 uses to keep both phase-boundary limbs. The cost is real: extra fields on every result, plus one more test.

[Answer]: C

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. Nothing below decides a
scientific value, and nothing claims a gate or acceptance row is discharged.

**Scope.** Two artifacts — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit. Those categories are still
assessed in the security artifact's scope note.

**Q1 = A — the mask-freeze-precedes-access ordering becomes machine-enforced.** The
locked-test access path **refuses** unless a registered, frozen mask bundle exists whose
registration timestamp **precedes** the access. A **hard failure**, not a warning. The reason
is specific: a mask frozen after December was seen is a fairness failure **no downstream check
can detect**, because the mask is what every comparison is measured through — and the run that
would violate the ordering is the run that writes the record proving it. **Two costs stated:**
it is a **cross-unit half-contract** with `governance-guards`' access path, of which this stage
states only this unit's half; and it is **unrunnable today** because **BLK-07 is open** and
that path does not exist.

**Q2 = C — the estimand's sign gets both mechanisms, because they check different things.**
(1) A **reversed-sign negative control** on the DCB precedent (TA-07/WS-04): a deliberately
inverted computation **must fail**, proving the producer computes **benchmark − model**.
(2) Every emitted estimand value **carries its orientation and weighting as fields**
(`benchmark_minus_model`, `equal_station`), and a consumer reporting the value without them
**fails** — preventing a correct value being read under the wrong convention downstream.
**Neither substitutes for the other**, which is why the duplication objection this project
otherwise applies does not attach here: the control verifies the producer, the fields protect
the consumer. **A positive value favours the model**, and reversing that sign inverts the
thesis conclusion while the number looks identical.

**Carried, not re-decided.** R-103's BLK-08 joint contract **narrowed to `ABL-DIFF`**, stated
once in two halves; R-104's **inverse-before-metric at the boundary every caller crosses**;
R-105's stamp refusal; R-106's comparison-set membership as declared configuration checked
exactly; R-107's mask identity, **once-only registration** and G-05 freeze; R-108's ordered
executable estimand; R-109's G-06 evaluation — **hash-receipt before metrics, one chokepoint,
exactly 2–31 December**; R-110's honesty mechanics — completeness upstream, the disclosure
trigger **as a field**, the caveat **emitted by the path**; R-111's masks-plus-matched-window
assertion; R-112's evaluation-time IRI and GIM join, **this unit narrowing nothing**.

**Status claims made.** None. **FR-P1-05-7's row is `Pending` — APPROVED under D-32
(2026-08-28), never run, NOT passed**; **FR-P1-05-17 has no row at all and is `UNTESTED`**. An
approved-but-unrun row and an absent row are both `Pending`, and **neither is evidence**.
WS-16 and TA-11 are undischarged. **BLK-07 is open.** G-09 is signed (D-31) with preconditions
UNMET; stage 3.1 remains FAIL; `configs/` does not exist; no Python interpreter exists here, so
every test is written-but-unexecuted or unwritten and **no metric has ever been computed**.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
