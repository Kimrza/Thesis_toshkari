# Change record — three supervisor-owned freezes (D-12, D-13, D-14)

Vision §15.2 change record. Six required fields, in order. One record covers three
freezes because they were decided together, from one option set, at one sitting.

| Field | Value |
|---|---|
| Record ID | `CR-2026-08-21-FREEZES` |
| Date | 2026-08-21 |
| Approver | Kimia Rezaei, project owner, acting under the recorded student/supervisor authority equivalence |
| Effective version | Vision v4.3 — **issued 2026-08-21**; the affected rows are amended in place and annotated |
| Governance origin | `governance/reviews/GOV-2026-08-21-RA-01.md` Rec 5 and Rec 13; `team.md` § Walking Skeleton (Q-31) |

## 1. Requested change and reason

Freeze the three values that were blocking the G-05/G-09 freeze set as
`TBD — supervisor freeze gate` holes:

| Decision | Value frozen | Authority row closed |
|---|---|---|
| **D-12** | ≥90% usable hourly coverage per station per month, hard gate, alongside D-2's day rule | Vision §6.1B "numerical minimum … TBD — supervisor freeze gate" |
| **D-13** | H4/SRQ-5 stay confirmatory only with ≥3 independent §9.3 storm events in December | Vision §5.2 "the supervisor-approved minimum" |
| **D-14** | Scientific fixture window = March 2022, all three cells | Q-31, TE §15.1 |

Reason: each was a named hole inside the freeze set. §18.3's preflight gate requires
"zero unresolved P0 fields", and `project.md` § Forbidden bars any agent from filling
such a value by convenience — so they could only be closed by an owner decision, and
until they were, `nfr-requirements` (3.2) could not assemble a complete G-05 manifest.

**Method note, applying to all three.** A literature survey run on 2026-08-21 found no
published consensus figure for any of them: no TEC-completeness acceptance threshold, and
storm-event samples in the field spanning 11 to 170 with no stated minimum. Every one of
these three decisions therefore either **reuses a number the project's own approved
documents already state** (D-12 takes Vision §6.12's 90%; D-13 takes Vision §9.3's
three-event rule) or **selects among data the project already holds** (D-14). No figure
was imported from outside and none was invented.

## 2. Alternatives

**D-12.** (a) 95% hourly — rejected: fails NICO in September (93.2%), November (94.2%)
and June (94.0%), discarding held data including D-11's plumbing month. (b) Per-station
two-tier, 95% ARUC/BSHM and 90% NICO — rejected: precise but reads as fitting the
criterion to the data, for no measured gain. (c) Defer, leaving D-2's day rule alone —
rejected: keeps a `TBD` inside the freeze set and leaves a threshold set after five
months had been seen carrying the gate by itself.

**D-13.** (a) 72 disturbed hours (~10% of December) — rejected: unsourced. (b) 48
disturbed hours (~6.5%) — rejected: unsourced, and a low bar chosen to keep H4
confirmatory invites exactly that reading. (c) Two-part floor, ≥48 disturbed hours **and**
≥1 storm event — covers one extra failure shape, rejected on the same ground for its hour
limb.

**D-14.** (a) 2022-11, the plumbing month — rejected: concentrates all fixture evidence
in one month, the weakness D-11's own limitation warns about; NICO 94.2%. (b) 2022-01,
best coverage and closest seasonal analogue to December — rejected because
`audit_evidence_2022-01/` carries the year-blind predicate's custody irregularity (743
December-2022 records, copy still present under `superseded_2026-08-16/`) and
`GOV-2026-08-20-RA-01` findings `VAL-1` and `VAL-3` are open against those bytes.
(c) 2022-10 — rejected: regime too close to November for a real separation gain, NICO 1.5
points thinner than March.

## 3. Affected requirements, data, code, experiments, schedule, and claims

**Authority documents, amended in place with annotations.**

| Document | Row | Change |
|---|---|---|
| Vision §6.1B | "numerical minimum … TBD" | → frozen at 90% hourly per station per month, hard gate, with D-2's day rule; §6.12's exception path closed at G-P1A |
| Vision §5.2 | H4 predeclaration | → the minimum is D-13's three-independent-storm-event rule; no separate disturbed-hour count |

**Requirements.** `requirements.md` FR-P1-02-4 (rewritten from a named hole to D-12's
frozen gate, with the measured per-station table); FR-P1-05-18 (threshold now D-13);
FR-WS-1 (scientific fixture window now March 2022 under D-14); § Assumptions items 2 and
3 (both moved from open assumption to resolved).

**Data.** No data changes. No file is rewritten, recomputed or moved.

**Code.** None. D-14 determines which month the scientific fixture will *run on*; the
fixture does not yet exist.

**Experiments.** None. No model, prediction or metric exists.

**Schedule.** All three `TBD — supervisor freeze gate` holes inside the G-05/G-09 set are
closed, so §18.3's zero-TBD assertion can now be evaluated for these fields. G-P1A gains
a decidable coverage criterion. **This does not unblock G-05**: the sixteen open blocking
findings of `GOV-2026-08-20-RA-01` stand, including all three Validation Auditor vetoes.

**Claims.** D-12 tightens what the prepared data must show before any claim rests on it.
D-13 governs whether a disturbed-condition claim (H4, SRQ-5) may be confirmatory at all.
D-14 carries a mandatory limitation that must travel with every fixture result: March
2022 is an equinox month, does not reproduce December's winter-solstice regime or activity
distribution, and is not representative of the locked test month.

**What these freezes do NOT do.** They do not close Vision §6.6's hourly aggregation
statistic (still `TBD — supervisor freeze gate`; `GOV-2026-08-20-RA-01` finding
`DATA-05`/`TEC-04`), and they do not supply D-1's missing Student + Supervisor
countersignature on the coordinate-to-cell rule. Both remain open.

## 4. Whether the locked test has been accessed

**No.** No model, prediction or metric exists, so no performance evaluation of December
2022 has occurred; G-05 and G-06 are both blocked.

Recorded deliberately: December was **not** read while producing D-12's coverage table.
Doing so would have added a third and unlogged December access on top of the two the
locked-month access log already carries — the gap `GOV-2026-08-20-RA-01` finding `VAL-2`
is open against. December's own hourly coverage comes from the required pre-G-05
performance-blind audit, with an access-log row written before the read.

D-13's storm-event count likewise has **not** been computed. It requires GFZ Kp/Hp60 at a
recorded release grade, which the project has not yet acquired, and D-11 bars the
provisional-Dst material in `.dst_summary.json` from supplying it.

## 5. Required regeneration or invalidation

**None caused by these freezes.** No value, dataset or artifact is recomputed.

Obligations these freezes create, all forward-looking:

- The pre-G-05 December coverage audit must report December's hourly coverage against
  D-12's 90% gate, performance-blind, with an access-log row written first.
- The December regime audit must establish the independent-storm-event count from GFZ
  Kp/Hp60 at a recorded release grade, and the H4/SRQ-5 demotion — if it fires — must be
  recorded **before** the G-05 freeze.
- The scientific fixture's counts, tolerances, row-count ranges, support and missingness
  limits, timestamp tolerances, required outputs and expected CPU runtime range are
  measured from the March 2022 run and frozen into
  `tests/fixtures/scientific_1month/fixture_manifest.yaml` (TE §15.1, §15.2) — never
  inferred from the selection figures in D-14.

Unchanged pre-existing obligations: the `raw_isprint_cache/` re-acquisition; the
`audit_evidence_2022-FULL/` re-merge or provenance re-pointing; and the broken SHA-256
verification chain on Windows checkouts (`core.autocrlf=true`, no `.gitattributes` —
independently confirmed 2026-08-21), which currently prevents that re-merge from running
at all.

**Citation consequence, resolved 2026-08-21.** Vision v4.3 was issued the same day, and
the citation sweep was deliberately partial: pre-2026-08-21 artifacts keep their `v4.2`
citations because those were correct when written. See
`governance/CHANGE_RECORD_2026-08-21_D-144.md` § 5 for the rule applied.

## 6. Approver, date, and effective version

Approved by **Kimia Rezaei**, project owner, **2026-08-21**, under the recorded
student/supervisor authority equivalence for this workspace. No supervisor signature
artifact exists and none is claimed.

Effective version: **Vision v4.3, issued 2026-08-21.** D-14 needs no version bump — Q-31
is Student-owned under TE §18.2.

Companion record from the same day: `governance/CHANGE_RECORD_2026-08-21_D-144.md`
(D-144 approval, plus D-2 and the WS-01 acceptance-set exception).
---

## Addendum — 2026-08-21, later the same day

The body above is **left unedited**. Its closing paragraph states that these freezes do
not close Vision §6.6's hourly aggregation statistic and do not supply D-1's
countersignature. Both were closed later the same day, by separate decisions:

- **D-16** freezes the Phase 1 hourly aggregation statistic as the **median**, with
  zenith-weighted aggregation declared as a sensitivity and deferred because the audited
  Phase 1 product carries five columns (`ut1_unix`, `gdlat`, `glon`, `tec`, `dtec`) and
  no elevation, zenith angle or satellite identifier. Nothing is substituted for the
  unavailable information.
- The **D-1 addendum** records the owner's approval of the coordinate-to-cell rule under
  the recorded student/supervisor authority equivalence, which is the documented
  delegation the TE §18.2 supervisor role is exercised under. No signature is forged.
  D-1's IGS site-log validation limitation remains separately open.
- **D-17** freezes the Phase 1 target-row contract from the audited product schema, and
  **D-15** relocates every December-bearing artifact under
  `evidence/locked_test_restricted/`.

Also superseded: §3's note that "This does not unblock G-05: the sixteen open blocking
findings of `GOV-2026-08-20-RA-01` stand". Twelve of those recommendations were approved
and applied on 2026-08-21; the remaining open items are listed in
`governance/reviews/GOV-2026-08-21-RA-01.md` and in that report's § Prior review. G-05
remains blocked.

