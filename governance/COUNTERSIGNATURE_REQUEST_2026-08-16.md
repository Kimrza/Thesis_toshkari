# Supervisor countersignature request — 2026-08-16

**To:** Dr. Reza Saraf Shirazi
**From:** Kimia Rezaei
**Concerning:** four supervisor-owned items arising from the TEC governance board's
full seven-seat review of AI-DLC stage 2.2 (practices-discovery)

**Status, 2026-08-16 — items 1 and 2 are countersigned by the supervisor**, recorded on
the student's report. Both stage-blocking items are therefore closed. Items 3 and 4
remain open; neither blocks the practices-discovery gate.

Each item below states what was asked, the evidence, the alternative if declined, and the
consequence of leaving it open. Items 1–3 are readings of the governing documents; item 4
is a filing gap.

| # | Item | Status |
|---|---|---|
| 1 | TE §12 amendment for `test_acquisition_window.py` | **Countersigned 2026-08-16** |
| 2 | WS-09–WS-20 acceptance, WS-01–WS-08 deferred to G-P3A | **Countersigned 2026-08-16** |
| 3 | §1.3 script/notebook count inconsistency | Open |
| 4 | D-3/D-144 signature artifact and its two unfrozen sub-values | Open |

---

## Item 1 — Approve a new `tests/test_acquisition_window.py` module in TE §12

### What is asked

Approve adding an eighteenth module to the `tests/` tree enumerated in
`Technical_Environment_and_Research_Implementation` §12:

```
│   ├── test_acquisition_window.py   # run-window conformance; asserts the retrieved
│   │                                # set matches the requested (year, month) window
│   │                                # plus at most one documented straddle day
```

§12's tree is exhaustive, so adding to it amends the governing document.

### Why it is needed

The acquisition notebook selected experiments on month without year:

```python
if exp.startmonth not in RUN_MONTHS and exp.endmonth not in RUN_MONTHS:
    continue
```

The enclosing `getExperiments` window spans the whole audit year and legitimately
returns experiments overlapping 2022 at both ends. Testing month alone admits a
31-December experiment from either year. Realised consequences:

- 743 records dated **2022-12-31 — the locked test month** — were retrieved during the
  January run and filed into `evidence/audit_evidence_2022-01/`, on an unrestricted path
  with no access record;
- 642 records dated 2021-12-31 were filed into `evidence/audit_evidence_2022-12/`;
- `audit_evidence_2022-01/madrigal_coverage_summary.csv` reported
  `december_days_present = 1` and `december_coverage_pct = 3.226` from a January run.

### Why no existing module covers it

| Module | Why it does not catch this |
|---|---|
| `test_release_hashes.py` | Proves bytes are unmutated. Misfiled bytes hash correctly; it passes |
| `test_locked_test_guard.py` (WS-18) | Guards December *execution*, not acquisition |
| `test_station_registry.py` | Covers registry and coverage population, not the retrieval predicate |
| `test_phase_boundary.py` | Module-import graph test |

The merge script's existing calendar-year guard also cannot express the invariant: it
tests year membership, while the defect is run-window membership. The 2022-12-31 rows
*are* year 2022 and pass it untouched — which is exactly why the merged year artifact
stayed correct while the January per-month summary did not.

### Evidence

- Fix: `notebooks/madrigal_phase1_coverage_audit.ipynb` Cell 10, predicate now tests
  `(year, month)` membership. One line; the intended one-day straddle survives in every
  month.
- Test behaviour: **5 failed / 23 passed before the fix, 28 passed after.** It carries a
  negative control asserting the year-blind predicate admits both intruders, so it cannot
  pass vacuously.
- Correction record: `evidence/CORRECTION_2026-08-16_acquisition_window.md`.
- Access log: `evidence/experiment_registry.md`.
- Affected evidence regenerated; originals preserved under `superseded_2026-08-16/`.

### Alternative if you decline

Extend `test_station_registry.py`'s coverage remit to include acquisition-window
assertion over `src/data/prepared.py`. Keeps §12's tree at seventeen modules. Costs
clarity — the check is not station-registry work.

### If left open

The defect is fixed but unguarded by any mandated test, so a regression would not be
caught. The board recorded this as a missing-critical-test finding.

---

## Item 2 — Accept WS-09–WS-20 as Phase 1's acceptance set, WS-01–WS-08 deferred to G-P3A

### What is asked

Confirm that Phase 1's Section 16 acceptance set is **WS-09 through WS-20**, with
WS-01–WS-08 deferred to gate G-P3A, and that §16's "all 20" is read as the whole-project
set across both phases rather than a Phase 1 gate condition.

### The contradiction being resolved

| Clause | Says |
|---|---|
| TE §16 | Acceptance occurs only when **all 20** WS rows are PASS |
| TE §16.1 | WS-01–WS-08 are evidence for **G-P3A**, a Phase 2 gate |
| TE §7.0, NFR-PHASE-01 | Phase 1 must not import or execute the raw-processing path that produces WS-01–WS-08 |

Phase 1 cannot satisfy "all 20" without violating NFR-PHASE-01. The three clauses cannot
all hold as written for Phase 1.

### Independent verification

The board's ML & Statistical Methods seat verified that this reading leaves **no
leakage-, fold-, mask-, or estimand-related check unenforced in Phase 1**. Every such row
falls inside WS-09–WS-20:

| Row | Covers |
|---|---|
| WS-10 | IRI denial fails on deliberate injection |
| WS-11 | Driver lags, trailing F10.7, Dst diagnostic-only |
| WS-12 | F1–F4 folds, 24-hour embargo |
| WS-13 | Matched input windows |
| WS-16 | Comparison-wide masks, no pairwise mask |
| WS-17 | Vector bootstrap, cross-station carry, seed reproducibility |
| WS-18 | Locked-test guard |
| WS-20 | Clean CPU reproduction |

WS-01–WS-08 are target-*construction* checks (RINEX parse, DCB sign, STEC, mapping,
uncertainty budget) for a target Phase 1 does not build.

### One residual to note

No WS row covers **train-only transforms** — §16's checklist has no such row in either
subset. NFR-LEAK-01 is enforced instead through TE §18.3's ten-item gate-test list and
TA-11. The guarantee holds; it does not hold via WS. Recording this prevents the omission
being misread later as a coverage gap.

### Alternative if you decline

State which of §16, §16.1 or §7.0 is to be amended, and Phase 1 acceptance is
re-derived from your ruling.

### If left open

Construction proceeds against an unconfirmed acceptance set. `user-stories` (2.4) is
skipped in this workflow, so the WS and TA rows are the only acceptance vocabulary
Construction will have.

---

## Item 3 — Resolve the §1.3 script and notebook count inconsistency

### What is asked

Confirm that **nine stage scripts and five notebooks** (TE §12, §14, §19) are operative,
and that TE §1.3's "Scripts 18 → 7 / Notebooks 11 → 4" is a stale change-log row.

### Evidence

- TA-01 approves against the §12/§14/§19 structure, which is the practical argument for
  treating it as operative.
- **Vision §14.2 D-130 already records the seven/four counts as "superseded by D-135 and
  D-142."** On the authority order (Vision above TE), this appears to settle the question
  without a fresh ruling.
- **Caution, and the reason this is still being asked:** D-135 and D-142 are supersession
  pointers that carry no counts of their own. This is a Vision-internal citation defect,
  so the D-130 evidence should be confirmed rather than treated as clean.

### Alternative if you decline

Rule that §1.3 is operative and the other sections reconcile down to it. This would
change the file structure Construction generates.

### If left open

The scaffold is built against an unconfirmed file count. Cost of confirming now is one
reading; cost of discovering it later is regenerating the stage scripts.

---

## Item 4 — File or remediate the missing D-144 signature artifact

### What is asked

Either file the signature artifact for D-3/D-144, or authorise recording in the evidence
base that acquisition proceeded on an unartifacted countersignature.

### The gap

`evidence/DECISIONS.md` supervisor-review table, D-3 row:

> Countersigned by the supervisor. Recorded 2026-08-15 as reported by the student; **no
> signature artifact (signed document, email or minute) is filed in this repository.**

Meanwhile:

- Vision §14.2 lists D-144's status as **"Decision required — Approve / Reject / Modify /
  Postpone."**
- Vision line 1357 requires that, if approved, D-144 freezes the Madrigal
  experiment/kindat, VTEC parameter and units, coordinate-to-cell rule, hourly aggregation
  **and the numerical coverage minimum**.
- Vision Appendix C requires that freeze **before** replacement acquisition.
- **Twelve months of Madrigal acquisition have already executed.**
- At least two values the approval was to freeze remain open: the coordinate-to-cell rule
  is still self-labelled "PROVISIONAL / DEFAULT convention adopted here" in the audit
  notebook, and the numerical coverage minimum is still "TBD — supervisor freeze gate"
  at Vision line 441.

### What is needed

1. The signature artifact, or an explicit record that none exists;
2. A ruling on whether the twelve completed acquisition months stand, given the ordering;
3. The two unfrozen sub-values, or a statement that they remain open and what that blocks.

### If left open

Every downstream artifact rests on an acquisition whose authorising decision is
unartifacted and two of whose mandated freezes are unresolved. This was raised by the
board's Chair seat as a missing-approver finding.

---

## Summary

| # | Item | Owner | Blocks |
|---|---|---|---|
| 1 | TE §12 amendment for `test_acquisition_window.py` | Supervisor | Stage 2.2 gate |
| 2 | WS-09–WS-20 acceptance for Phase 1 | Supervisor | Stage 2.2 gate, Construction acceptance |
| 3 | §1.3 count inconsistency | Student + Supervisor (§18.2) | Scaffold generation |
| 4 | D-144 signature artifact | Supervisor | G-P1A evidence integrity |

Related student-owned decisions taken without countersignature, for your visibility:
**D-11** (walking-skeleton fixture window, 2022-11-01..07, Q-31 Student-owned) and the
ML-01 correction restoring the two-event locked-test rule to match Vision §8.3.
