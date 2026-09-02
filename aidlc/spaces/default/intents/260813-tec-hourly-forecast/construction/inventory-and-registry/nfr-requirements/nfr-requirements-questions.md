# NFR Requirements — Questions — `inventory-and-registry`

**Unit** `inventory-and-registry` (Bolt 4) · **Kind** `library` · **Stage** `nfr-requirements`

Two artifacts only — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit.

**Not re-asked, because `functional-design` already decided them.** The December audit's
scope-declaration mechanism (W-6, Q4 = C — declare up front, check against a governed
reference set, fail **before** any read on a short declaration, reconcile rows written
against the declaration); membership from **record timestamps**, never a directory or
filename; the nine §5.1 source fields (R-44); §6.2 in full with the **IGRF version pinned
and never defaulted** (R-45); presence is not provenance (R-46); a resolved value equals the
single value of its **named** source and carries a rationale (R-47); the migration moves
values **without changing them** (R-48); G-P1A decided against two thresholds with every
number attributed (R-51); the four prohibitions with four separately named results (R-52);
ICTP kept out **by reachability** (R-53).

**Carried, not decided here.** **BLK-07 is open**, so `acquisition`'s named accessor — which
W-6 depends on for every read — does not exist. `FR-P1-02-7` and `FR-P1-02-8` carry **no
acceptance row**; `TA-29` was cited for the latter and is **withdrawn**.

---

## Question 1

W-6 records the December audit's blindness as **`performance_inspected=false`** on each
access row. That is a **flag the caller sets**. Nothing structurally prevents the audit
module from importing an evaluation or model module and looking at a metric while writing
`false` — the field would still say `false`.

The project already has a precedent for the structural form of this control: the IRI
import boundary (TE §12 / TA-07), where `src/external/iri.py` and `src/external/gim.py`
may not be imported, directly or transitively, by any module under `src/features/` or
`src/models/`, with only two permitted importers.

What should `security-requirements.md` require?

A. **Both** — keep the declared flag **and** add a module-graph constraint: the December-audit code path may not import, directly or transitively, any module under `src/models/` or `src/evaluation/`, asserted by a test the way TA-07 asserts the IRI boundary
   > **Impact**: Makes blindness checkable rather than attested, using a technique this project already runs and already has a test shape for. It adds an import-boundary test and a new constraint on where audit code may live; if the audit legitimately needs something from `src/evaluation/`, that dependency has to move or be duplicated.

B. Keep the declared flag alone, and state that blindness rests on the auditor's declaration
   > **Impact**: No new mechanism, and the flag is already designed and reconciled against the declared scope. It leaves the single most consequential guarantee in the pre-G-05 window — that December was seen without performance being seen — resting on a self-report, which is the form of evidence §16 calls insufficient ("visual inspection alone is insufficient").

C. Require a human attestation at G-05 in addition to the flag
   > **Impact**: Puts a person behind the claim, which matches how the project gates its freezes. It converts a machine-checkable property into a signature, and the supervisor signing G-05 would be attesting to something they cannot verify from the artifacts.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the flag and the boundary answer different questions, and the project has already decided that this class of guarantee gets a structural control plus a negative-path test (TA-07, WS-10). December informing model selection is the leakage the whole locked-test design exists to prevent, and a boolean the auditor sets is the weakest possible evidence for it. The cost is one import-boundary test and a placement constraint on audit code.

[Answer]: A

---

## Question 2

W-6 reads every artifact in a declared scope — twelve months, December as the full calendar
month 1–31, three cells, named artifact classes — writing a durable access row before each
read. Nothing states what happens if the audit **stops partway**: some access rows written,
some counts produced, the reconciliation never reached.

This matters because the audit is a **precondition of G-05**, and because every access it
made is permanently recorded whether or not it finished.

What should the artifacts require of an interrupted December audit?

A. All-or-nothing as **evidence**, append-only as **record**: the access rows already written stand permanently and are never deleted, but a partial audit produces **no coverage or regime report** and cannot be offered at G-05 — the audit re-runs from the start, logging its accesses again
   > **Impact**: Keeps the two obligations separate and both intact — NFR-AUD-01's "no entry is deleted" and the requirement that G-05's input be a complete audit. It means a re-run adds a second full set of access rows, so the access log will show December opened more times than the audit ran, and that has to be legible rather than alarming.

B. Resumable: the audit records which artifacts it has already counted and continues from there, producing one report across both passes
   > **Impact**: Avoids duplicate accesses and finishes faster after an interruption. The report then spans two sessions with two environment locks, and the "opened once" discipline becomes harder to read from the log rather than easier.

C. Treat a partial audit as a partial result, reported with its own coverage caveat
   > **Impact**: Nothing is wasted and the caveat is honest. It puts an incomplete audit in front of G-05 with a caveat attached, and this project's own evidence records what happens to caveated partial artifacts — they get relied on and the caveat travels less far than the number.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it is the only option that keeps both rules whole. The cost is real and should be stated in the artifact rather than discovered later: the access log will legitimately show more December opens than there were audits, so the reconciliation R-50 already performs must be able to say which rows belong to which attempt. Option B's cross-session report is exactly the kind of artifact whose provenance later becomes unarguable; option C is how a caveated figure becomes a relied-on figure.

[Answer]: A

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. Nothing below decides a
scientific value, and nothing claims a gate or acceptance row is discharged.

**Scope.** Two artifacts — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit. The excluded categories are
still assessed in the security artifact's scope note.

**Q1 = A — blindness is structural as well as declared.** The December audit keeps
`performance_inspected=false` on every access row **and** gains a module-graph constraint:
the December-audit code path may **not import, directly or transitively, any module under
`src/models/` or `src/evaluation/`**, asserted by a test the way TA-07 asserts the IRI
import boundary. The reason is stated plainly: a boolean the auditor sets is the weakest
possible evidence for the one guarantee the whole locked-test design exists to protect, and
§16 already holds that visual inspection alone is insufficient. **Accepted cost:** one
import-boundary test, plus a placement constraint on audit code — if the audit legitimately
needs something from `src/evaluation/`, that dependency must move or be duplicated.

**Q2 = A — a partial audit is all-or-nothing as evidence, append-only as record.** Access
rows already written **stand permanently and are never deleted** (NFR-AUD-01), but a partial
audit produces **no coverage or regime report** and **cannot be offered at G-05**; the audit
re-runs from the start and logs its accesses again. **The consequence is stated rather than
discovered later:** the access log will legitimately show December opened more times than
the audit ran, so R-50's reconciliation must be able to say which rows belong to which
attempt.

**Carried, not re-decided.** W-6's scope-declaration mechanism (Q4 = C — declare up front,
check against a governed reference set derived from the release inventory rather than from
the declaration, fail **before** any read on a short declaration, reconcile rows written
against the declaration, `AuditScopeError` on either mismatch); December declared as the
**full calendar month, 1–31**; membership from **record timestamps**, never a directory or
filename; FR-P1-02-3's scope is **`access`, unqualified** — derived-artifact merges,
re-derivations, corrections, coverage recounts and schema validations, not only a model
execution; R-44's nine §5.1 fields; R-45's §6.2 in full with the **IGRF version pinned and
never defaulted**; R-46 presence is not provenance; R-47 a resolved value equals the single
value of its **named** source; R-48 the migration changes no value; R-51's two G-P1A
thresholds with every number attributed; R-52's four separately named prohibition results;
R-53's ICTP exclusion **by reachability**.

**Status claims made.** None. **BLK-07 is open**, so `acquisition`'s named accessor — which
W-6 depends on for every read — does not exist, and the audit cannot run today.
**`FR-P1-02-7` and `FR-P1-02-8` carry no acceptance row**; `TA-29` was cited for the latter
and is **withdrawn**. WS-01, TA-04 and TA-25 are `Pending`. No Python interpreter exists
here, so every test is written-but-unexecuted or unwritten. G-09 is signed (D-31) with its
preconditions UNMET; stage 3.1 remains FAIL.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
