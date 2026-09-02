# NFR Requirements — Questions — `regimes-diagnostics-reporting`

**Unit** `regimes-diagnostics-reporting` (Bolt 11) · **Kind** `library` · **Stage** `nfr-requirements`

Two artifacts only — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit.

**Requirement set derived up front from `requirements.md`, not reconstructed afterwards.** The
`functional-design` coverage table carries **11 requirements, 7 without a §16/§19 row** —
**REQ-ENG-12**, **FR-P1-05-9**, **FR-P1-05-10**, **FR-P1-05-11** with rows; **FR-P1-05-14**,
**FR-P1-05-15**, **FR-P1-05-16**, **FR-P1-05-18**, **FR-P1-05-19**, **FR-P1-05-20** and
**REQ-CLAIM-01** without. Of those seven, **five now hold D-32-approved rows that are `Pending`
— never run, NOT passed** — and **two are genuinely rowless**: FR-P1-05-14 and FR-P1-05-15.
This unit's design additionally names **FR-P1-03-4**, **NFR-DQ-01**, **NFR-TDEF-01**,
**REQ-ENG-4**, **REQ-ENG-8** and **REQ-ENG-13**; all are cited. *(Run before writing. The same
check, run only by the reviewer, found a Major or Critical on four consecutive units.)*

**Not re-asked, because `functional-design` already decided them.** One regime classifier with
configured thresholds and **one counting path** (R-123, W-1); **December-blind by signature,
post-receipt by construction**, with two guards (R-124, W-2); the primary results table that
**refuses, co-reports, prints and checks its units** (R-125, W-3); the claims-and-limitations
checklist as **presence checks at named locations** (R-126, W-4); the breakdown family with
**stamped producing functions** and the D-17 bound (R-127, W-5); **practical relevance frozen
and demoted honestly**, post-access runs **labelled** (R-128, W-6); `plots.py`
**presentation-only by signature** (R-129, W-7); the **diagnostics quarantine** (R-130, W-8);
the notebooks' single declaration helper, stop semantics and **no only-copy** (R-131, W-9);
`tests/test_regimes_and_reporting.py` as **one home for every named control** (R-132, W-10).

---

## Question 1

**Two sibling units have named this unit as owing the consumer half of a contract, and neither
half has been stated here.**

1. **`evaluation-and-comparison` § SEC-C-02** requires every emitted estimand value to carry
   its **orientation** (`benchmark_minus_model`) and **weighting** (`equal_station`), and names
   **this unit** as the consumer that must **fail** if it reports the value without them —
   because this unit owns the **primary results table**.
2. **`target-standardization` § SEC-T-02** requires the **label and lineage caveat** to travel
   as a field on the artifact, and requires **a consumer that reports a comparison without it
   to fail** — again this unit, for the same reason.

Both siblings explicitly state they declare **only their own half** and that the consumer half
**has not been stated**.

What should `security-requirements.md` do?

A. **State both consumer halves explicitly**: the primary results table **refuses to render** an estimand value lacking its orientation and weighting fields, and **refuses to render** any IRI or GIM comparison lacking the lineage caveat — each a hard failure, each naming the sibling requirement it completes
   > **Impact**: Closes two contracts that are currently stated from one side only, at the unit that is the actual consumer. It adds two refusals to a rendering path that does not exist yet, and makes the results table fail on inputs that upstream units are not yet producing — so the refusals will fire on everything until both producers land.

B. State them as **obligations acknowledged**, without making the table refuse
   > **Impact**: Records that this unit accepts the contracts without building a mechanism whose inputs do not exist. An acknowledged obligation with no enforcement point is the documentary form this project has repeatedly found does not survive — and both siblings built a refusal on their side.

C. Leave both to stage 3.5, since neither producer exists
   > **Impact**: Avoids specifying against absent inputs. It leaves two half-contracts permanently half-stated across a stage boundary, and neither sibling would have any counterparty.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — a half-contract stated on one side only is not a contract, and this unit is the named counterparty in both. The cost is real and should be written down: **the refusals will fail on every input until the producing halves land**, which is correct fail-closed behaviour but will look like breakage. Option B's weakness is precise — both siblings built refusals, so an acknowledgement here would leave the pair asymmetric, with the producer enforcing and the consumer merely intending.

[Answer]: A

---

## Question 2

R-130 quarantines the diagnostics lane: **Dst is diagnostic and hindcast-only, never a
confirmatory feature**, and the **Random Forest importance figure is non-authoritative** — it
may be saved, but may never rank or select a feature. R-130 gives them **grade discipline,
labelled artifacts and a lane boundary**.

What R-130 governs is **production**. Nothing governs **citation**: a labelled diagnostic
figure, correctly quarantined at the moment it is written, can still be **cited in the thesis
text as if it were evidence** — and the label travels with the artifact, not with the sentence
that references it.

This unit owns the **claims-and-limitations checklist** (R-126, W-4), which already performs
**presence checks at named locations**.

What should `security-requirements.md` require?

A. Extend the checklist to a **citation check**: any thesis-level location citing a quarantined diagnostic must carry its **non-authoritative label** alongside the citation, checked at the same named locations the checklist already inspects
   > **Impact**: Uses a mechanism this unit already owns rather than inventing one, and closes the gap between a labelled artifact and an unlabelled claim about it. Checking prose for a citation-plus-label pairing is weaker than checking a data field, and a citation phrased indirectly would evade it.

B. Keep production-side quarantine only, and record the citation gap as a stated residual
   > **Impact**: Honest about what the mechanism reaches, and adds nothing that could give false assurance. It leaves the one path by which a rejected diagnostic becomes a reported finding — and this project's honesty rules exist precisely because that path matters.

C. Forbid quarantined diagnostics from appearing in thesis-level text at all
   > **Impact**: Eliminates the channel completely and is trivially checkable. It also forbids legitimate uses — Vision requires the RF-importance figure to be *saved* as a diagnostic, and a diagnostic that may never be discussed is of no use to anyone.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the checklist already inspects named locations, so this extends a mechanism rather than adding one, and the failure it addresses is the one the honesty rules are built around: a rejected input reappearing as a reported result. **Its weakness must be stated plainly** — a prose check is weaker than a field check and an indirect citation evades it, so this narrows the gap rather than closing it. Option C would forbid the use Vision explicitly requires.

[Answer]: A

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. Nothing below decides a
scientific value, and nothing claims a gate or acceptance row is discharged.

**Scope.** Two artifacts — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit.

**Requirement set, derived against `requirements.md` across BOTH families.** The FR set is the
`functional-design` map's **11 requirements, 7 without a §16/§19 row** — with rows: **REQ-ENG-12**
(TA-16), **FR-P1-05-9** (TA-20), **FR-P1-05-10** (TA-19, supporting), **FR-P1-05-11** (WS-19);
without: **FR-P1-05-14**, **FR-P1-05-15**, **FR-P1-05-16**, **FR-P1-05-18**, **FR-P1-05-19**,
**FR-P1-05-20**, **REQ-CLAIM-01**. Of those seven, **five hold D-32-approved rows that are
`Pending` — never run, NOT passed**; **two are genuinely rowless** — **FR-P1-05-14** and
**FR-P1-05-15**. The **NFR family was checked separately against `requirements.md`'s eleven
IDs**, because on `statistical-inference` a design-file grep came back clean on the FR families
and still missed **NFR-REP-01**: this unit states obligations against **NFR-DQ-01** and
**NFR-TDEF-01**, and its design also names **FR-P1-03-4**, **REQ-ENG-4**, **REQ-ENG-8** and
**REQ-ENG-13**. All are cited.

**Q1 = A — both consumer halves are stated, as refusals.** The primary results table
**refuses to render** an estimand value lacking its **orientation** (`benchmark_minus_model`)
and **weighting** (`equal_station`) fields — completing `evaluation-and-comparison`
§ SEC-C-02 — and **refuses to render** any IRI or GIM comparison lacking the **lineage
caveat** — completing `target-standardization` § SEC-T-02. Both siblings built a refusal on
their side and named **this unit** as the counterparty, because this unit owns the primary
results table. **A half-contract stated on one side only is not a contract.**

**The cost is written down rather than discovered:** both refusals **will fail on every input
until the producing halves land**. That is correct fail-closed behaviour and it will look like
breakage.

**Q2 = A — the claims checklist extends to citations.** Any thesis-level location citing a
**quarantined diagnostic** — Dst hindcast work, the **non-authoritative RF-importance figure**
— must carry its **non-authoritative label alongside the citation**, checked at the same named
locations R-126's checklist already inspects. R-130 quarantines **production**; nothing governed
**citation**, and the label travels with the artifact rather than with the sentence.

**Its weakness is stated plainly:** a **prose check is weaker than a field check**, and an
**indirectly phrased citation evades it**. This **narrows the gap; it does not close it**, and
no artifact may describe the diagnostics quarantine as fully enforced.

**Carried, not re-decided.** R-123's single regime classifier with configured thresholds and
**one counting path**; R-124's **December-blind by signature, post-receipt by construction**
with its two guards; R-125's results table that **refuses, co-reports, prints and checks its
units**; R-126's presence checks at named locations; R-127's **stamped producing functions** and
the D-17 bound; R-128's **practical relevance frozen and demoted honestly** with post-access
runs **labelled exploratory**; R-129's **presentation-only `plots.py`**; R-130's **diagnostics
quarantine**; R-131's notebooks with **no only-copy**; R-132's single home for every named
control.

**Status claims made.** None. **Five acceptance rows are `Pending` — approved under D-32
(2026-08-28), never run, NOT passed** — and **FR-P1-05-14 and FR-P1-05-15 have no row at all**,
covered by R-128's controls meanwhile. **TA-16, TA-19, TA-20 and WS-19 are undischarged.**
G-09 is signed (D-31) with preconditions UNMET; stage 3.1 remains FAIL; `configs/` does not
exist; no Python interpreter exists here, so **no results table has ever been produced**.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
