# Change record — D-144 approval

Vision §15.2 change record. Six required fields, in order.

| Field | Value |
|---|---|
| Record ID | `CR-2026-08-21-D144` |
| Date | 2026-08-21 |
| Approver | Kimia Rezaei, project owner, acting under the recorded student/supervisor authority equivalence |
| Effective version | Vision v4.3 / Technical Environment v3.3 — **issued 2026-08-21**; the affected rows are amended in place and annotated |
| Governance origin | `governance/reviews/GOV-2026-08-21-RA-01.md` Rec 1 (BLOCKER `RA-F-01`), option A |

## 1. Requested change and reason

Approve decision **D-144** — adopt MIT Haystack CEDAR Madrigal MAPGPS `gps`
binned VTEC as the single-source Phase 1 prepared-data replacement — and bring
the four authority rows that recorded it as undecided into agreement with that
approval.

Reason: the status disagreed across the authority stack, and the disagreement was
blocking. Vision v4.2 §14.2 carried D-144 as "Decision required — Approve /
Reject / Modify / Postpone" and "not yet adopted"; Vision §17's freeze line was
unchecked; TE §1.5 read "Pending — D-144, not yet approved"; TE §19 TA-25 read
"Blocked — D-144 and replacement audit pending". Meanwhile
`evidence/DECISIONS.md` D-3 recorded a 2026-08-15 countersignature whose own note
states that **no signature artifact is filed in this repository**, and
`requirements.md` had begun reasoning from that lower-precedence record as though
the Vision-level decision were closed. Twelve months of Madrigal acquisition had
already executed, against Vision Appendix C's requirement that the freeze precede
replacement acquisition.

The governance board rated the resulting state a BLOCKER: an authority conflict
resolved by inference, on an approval with no filed evidence. This record closes
it by express approval rather than by inference.

**What is being approved, and by whom.** The approval is given by the project
owner on 2026-08-21 under the standing student/supervisor authority equivalence
recorded for this workspace. It is **not** a supervisor signature: no signed
document, email or minute exists, and none is claimed anywhere in this record or
in the amended rows.

## 2. Alternatives

1. **File a supervisor signature artifact and update on that basis.** Rejected as
   unavailable — no such artifact exists. Fabricating one was never an option.
2. **Correct the artifact instead of approving the decision** (board Rec 1 option
   B): restate D-144 as open per Vision v4.2 and make FR-P1-01-* conditional on
   its approval. Rejected: it preserves the block rather than resolving it, and
   the owner holds the authority to decide.
3. **Record that acquisition proceeded on an unartifacted countersignature**
   (board Rec 1 option C). Rejected as the primary route: it converts a decision
   the owner can simply make into a permanent recorded irregularity. Its factual
   content is nonetheless preserved — this record states plainly that no
   signature artifact exists.
4. **Reject or modify D-144** — re-open the source search or change scope.
   Rejected: the ICTP failure is measured and closed (D-143), Madrigal is the
   audited replacement, and twelve months are acquired.

## 3. Affected requirements, data, code, experiments, schedule, and claims

**Requirements.** `requirements.md` § Known defects row 5 (rewritten from "open"
to "resolved 2026-08-21"); FR-P1-01-1 ("supervisor-approved" → "approved under
D-144", with the open sub-freezes named). The remaining FR-P1-01 requirements are
unchanged: their content never depended on the status, only their standing did.

**Authority documents, amended in place with annotations.**

| Document | Row | Before | After |
|---|---|---|---|
| Vision §14.2 | D-144 | "Decision required — Approve / Reject / Modify / Postpone" | "Approved 2026-08-21", §6.1B audit noted as still open |
| Vision §17 | D-144 freeze line | `[ ]`, undischarged | `[ ]` retained, annotated partially discharged — 3 of 5 attached freezes done |
| TE §1.5 | Phase 1 replacement provider/product | "Pending — D-144 … not yet approved" | "Approved 2026-08-21 — D-144 … adopted", two sub-values still `TBD` |
| TE §19 | TA-25 | "Blocked — D-144 and replacement audit pending" | "Blocked — replacement audit pending" |

**Data.** No data changes. The twelve acquired months are unaffected in content.
Their ordering irregularity — acquisition before the freeze, Vision Appendix C —
is **not** cured by this approval and remains recorded here and in
`COUNTERSIGNATURE_REQUEST_2026-08-16.md` item 4.

**Code.** None.

**Experiments.** None. No model, prediction or metric exists.

**Schedule.** G-P1A is no longer blocked on D-144's status. It remains blocked on
the §6.1B experiment/schema/cell/coverage audit, and TA-25 stays `Blocked` for
that reason.

**Claims.** No claim changes. The gridded-target labelling rule (location-sampled
gridded VTEC, never receiver-derived station VTEC) is untouched.

**What this approval does NOT do.** Vision line 1357 attaches five freezes to
D-144's approval. Their state after this record:

| Attached freeze | State |
|---|---|
| Madrigal experiment / kindat | Frozen — D-4 |
| VTEC parameter and units | Frozen — D-4 |
| Coordinate-to-cell rule | Frozen — D-1, but its Student + Supervisor countersignature row is **still blank** (TE §18.2 forbidden choice) |
| Hourly aggregation statistic | **Open** — `TBD — supervisor freeze gate`, Vision §6.6 |
| Numerical coverage minimum | **Open** — `TBD — supervisor freeze gate`, Vision §6.1B; D-2 (approved 2026-08-21) governs as the interim rule |

Two of the five remain open, which is why Vision §17's line stays unticked.

## 4. Whether the locked test has been accessed

**Not for metrics.** No model, prediction or metric exists, so no performance
evaluation of December 2022 has occurred and G-06 has not opened.

**Recorded separately, and not cured by this record:** December 2022 target
values were read during acquisition and merging, and `GOV-2026-08-20-RA-01`
findings `VAL-2` and `VAL-3` record that only two of four December read events
appear in the locked-month access log, and that December values sit on four
unrestricted paths. This change record does not authorise, excuse or close any
of that.

## 5. Required regeneration or invalidation

**No regeneration required by this change.** It is a status reconciliation; no
value, dataset or artifact is recomputed.

**Pre-existing regeneration obligations, unaffected and still open:**

- `evidence/audit_evidence_2022-FULL/` must be re-merged from the corrected
  months or have its provenance explicitly re-pointed under a D-number
  (`PROVENANCE_NOTICE.md`).
- The `raw_isprint_cache/` re-acquisition with provider version suffixes
  recorded (FR-P1-01-2, FR-P1-01-4).
- The SHA-256 verification chain does not currently reproduce on a Windows
  checkout (`core.autocrlf=true`, no `.gitattributes`), so the FULL merge cannot
  be regenerated on this clone until that is fixed
  (`GOV-2026-08-20-RA-01` finding `DATA-01`, independently confirmed
  2026-08-21).

**Citation consequence, resolved 2026-08-21.** Vision v4.3 and TE v3.3 were issued
the same day: both headers, TE's subordination and purpose lines, and both revision
tables now carry the new versions. The citation sweep was **deliberately partial**.
Artifacts authored before 2026-08-21 — the ideation set, the practices-discovery set,
the phase-check and the earlier governance reports — keep their `v4.2` / `v3.2`
citations, because those citations were correct when written and rewriting them would
misrepresent when each statement was made. Only the live artifact
(`requirements.md`) cites the current versions, and it states the version it was
authored against alongside them.

## 6. Approver, date, and effective version

Approved by **Kimia Rezaei**, project owner, **2026-08-21**, under the recorded
student/supervisor authority equivalence for this workspace. No supervisor
signature artifact exists and none is claimed.

Effective version: **Vision v4.3 / Technical Environment v3.3, not yet issued.**
The affected rows are amended in place and annotated with this record's path.

Governance origin: `governance/reviews/GOV-2026-08-21-RA-01.md` Rec 1.
Companion approvals granted the same day: D-2 (board Rec 5) and the WS-01
acceptance-set exception (board Rec 12), both recorded in their own artifacts.
---

## Addendum — 2026-08-21, later the same day

This record's §3 table and §5 list were accurate when written and are **left unedited**.
Three of the items they describe as open were closed later the same day, by separate
recorded decisions. The addendum states that rather than rewriting the body, so a reader
can see the sequence.

| Item, as recorded above | State at end of 2026-08-21 |
|---|---|
| Coordinate-to-cell rule — "countersignature row is **still blank**" | **Closed.** `evidence/DECISIONS.md` D-1 addendum: approved by the project owner under the recorded student/supervisor authority equivalence, which is the documented delegation the TE §18.2 supervisor role is exercised under. No supervisor signature artifact exists and none is claimed. D-1's separate IGS site-log validation limitation remains open |
| Hourly aggregation statistic — "**Open** — `TBD — supervisor freeze gate`" | **Closed as D-16.** Median frozen; zenith-weighted declared as a sensitivity and deferred as **not computable** from the audited five-column product |
| Numerical coverage minimum — "**Open** … D-2 governs as the interim rule" | **Closed as D-12.** ≥90% usable hourly coverage per station per month as a hard gate, alongside D-2's day rule |
| §5: "The SHA-256 verification chain does not currently reproduce on a Windows checkout" | **Fixed.** `.gitattributes` marks `evidence/**`, `artifacts/**` and `tests/fixtures/**` as `-text`; the working tree was denormalized; 60 of 60 declared artifacts across 15 manifests and 13 of 13 EC-1 recorded hashes verify. The FULL re-merge obligation itself remains open |
| §5: "`evidence/audit_evidence_2022-FULL/` must be re-merged…" | **Still open**, and the artifact has moved: it is now `evidence/locked_test_restricted/audit_evidence_2022-FULL/` under **D-15**. Reading it is a logged December access |

Vision §17's D-144 freeze line consequently stands at **4 of 5** attached freezes
discharged; the numerical coverage minimum and the aggregation statistic are now frozen,
and only D-1's site-log validation limitation and the §6.1B replacement audit remain
attached to G-P1A. The line stays unticked until the audit completes.

