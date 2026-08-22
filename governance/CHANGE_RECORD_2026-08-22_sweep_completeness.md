# `CR-2026-08-22-SWEEP-COMPLETENESS` — ten defects that survived the Rec 5 sweep, one committed while recording them, and the blind spot behind all of them

> **The count grew twice while this record was being written, and that is the
> record's most useful evidence.** Six defects were found in the stage 2.8
> artifacts before its approval gate. **Four more** surfaced at the Gate 0
> discharge, in already-approved artifacts (§ Further defects) — the last of those
> only because the sweep was re-run *after* the others were fixed. And **one
> was committed by this record itself** and by the provenance-gap record it
> accompanies — the same carry-a-figure-from-prose habit, reproduced inside the
> document written to correct it, and recorded in § Verification rather than
> folded silently into the count.
>
> The habit survived being named, being written into a project practice, and
> being made the subject of a change record — all within one session. **Six of
> the ten carry no numeral at all** — tallied from the `Carried a numeral?`
> column of the two tables below with awk, not counted by eye, after an earlier
> draft of this very sentence got the tally wrong — which is the mechanism this
> record exists to name.

| Field | Value |
|---|---|
| **Change record ID** | `CR-2026-08-22-SWEEP-COMPLETENESS` |
| **Date** | 2026-08-22 |
| **Origin** | Resume of AI-DLC stage 2.8 (`delivery-planning`). Defects found while re-deriving the counts that `CR-2026-08-22-INC-CORRECTIONS` Rec 5 had corrected |
| **Requested by / approved by** | **Project decision owner**, explicitly, at the stage 2.8 approval gate, under the recorded student/supervisor authority equivalence. No separate supervisor signature artifact exists and none is claimed |
| **Class** | **Documentation integrity.** Six corrections in one unapproved stage's own artifacts, four annotate-in-place corrections in approved artifacts on the owner's explicit approval, and one falsified verification claim recorded against a completed record |
| **Scientific values changed** | **None.** No D-number created, amended or superseded. No threshold, constant, fold, mask, seed, grid, estimand, acceptance row, gate criterion or approval is touched |
| **Gates affected** | **None.** No gate opened, closed or re-scoped |
| **Locked test accessed** | **No.** Nothing under `evidence/locked_test_restricted/` was opened, listed or searched. No access-log row owed or written |

## Why this record exists

`CR-2026-08-22-INC-CORRECTIONS` § Verification states, of its Rec 5 propagation
sweep:

> All live assertions corrected; all remaining occurrences are explicitly
> labelled superseded or are historical revision notes.

**That claim is falsified.** **Ten** live-assertion defects survived the sweep —
six in the stage 2.8 artifacts, found on resume while re-deriving the figures
rather than reading them, and four more in already-approved artifacts, found at
the Gate 0 discharge by checking each "still open" item against the change records
rather than trusting its status line — the last of those only by re-running the
sweep after correcting the others.

This is not a criticism of that record's diligence. **Six of the ten carry no
numeral at all**, and its sweep was a search for superseded *numbers*. The defect
is in the sweep's shape, and the shape is now written into procedure — which is
the part worth recording.

## The first six defects — found before the stage 2.8 approval gate

All six are in `aidlc/spaces/default/intents/260813-tec-hourly-forecast/inception/delivery-planning/`.
Every correction preserves its superseded literal in place, per
`governance/CHANGE_RECORD_PROCEDURE.md` step 1.

| # | Site | Defect | Carried a numeral? |
|---|---|---|---|
| 1 | `bolt-plan.md` § What this plan does not decide | "The **40** requirements with no acceptance row" → **36** | Yes |
| 2 | `risk-and-sequencing-rationale.md` § Sources; § R-02 closing line; § R-05 Risk cell; § R-05 "Why it ranks fifth" cell | Four sites at **40** → **36** | Yes |
| 3 | `bolt-plan.md` § Bolt 3; `risk-and-sequencing-rationale.md` § sequencing argument | `external-products` "**five** of its seven requirements with no acceptance row" → **four**; and its R-05 *Affected* cell "(5 of 7)" → **(4 of 7)** | Yes |
| 4 | `bolt-plan.md` § Bolt 3 confidence hypothesis | "the largest untested **share** of any unit" — **a stale superlative, and an internal contradiction** of § Bolt 10's "joint largest" claim in the same file | **No** |
| 5 | `bolt-plan.md` § Bolt 7 status paragraph; `risk-and-sequencing-rationale.md` § R-02 status paragraph | "none of the four has a §16 or §19 acceptance row … creating one is a Vision §15.2 amendment this stage cannot grant" — **a stale claim, and a direct contradiction** of § R-05 in the same file, which records the four leaving the untested list *because* TA-33…TA-36 were created | **No** |
| 6 | `external-dependency-map.md` § Still open, items 5 and 6 | Both listed as **"Awaiting the owner's explicit selection or final wording"**; both had been decided and applied on 2026-08-22 (`CR-2026-08-22-LEAKAGE-TA` and `CR-2026-08-22-INC-CORRECTIONS` Rec 7) | **No** |

`team-allocation.md` was swept and **found clean**; that null result is recorded in
the file itself, per `CHANGE_RECORD_PROCEDURE.md` step 3 ("a sweep that finds
nothing records that it ran and found nothing").

### Further defects, found at the Gate 0 discharge — after this stage's approval

Found while assembling the Gate 0 decision pack, by checking each "still open"
item against the change records rather than reading its status line. **All four
are in artifacts of stages already approved**, so all four were annotated in
place on the owner's **explicit approval at the Gate 0 discharge**, under the
precedent set at `GOV-2026-08-22-INC-01` Rec 7. Superseded text preserved at each.

| # | Site | Defect | Carried a numeral? |
|---|---|---|---|
| 7 | `external-dependency-map.md` § Still open, item 3 | "Creation is approved; **the name is not**. Three candidates await owner selection" — BLK-05's module name had been chosen as `tests/test_prepared_target_schema.py` under `CR-2026-08-22-TARGET-SCHEMA-TEST` | **No** |
| 8 | `external-dependency-map.md` § Still open, item 4 | "**Not applied.**" — FR-P1-01-7's amendment had been applied under `CR-2026-08-22-F107-CORRECTIONS`; the current row carries the 365-of-365 finding verbatim | **No** |
| 9 | `unit-of-work.md` § BLK-05 limb status | "The tree now enumerates **20** test modules" → **21**. A **fourth** site in that file, missed by this record's parent Rec 3, which corrected three | Yes |
| 10 | `external-dependency-map.md` § resolved-decisions table, BLK-05 row | **The same stale claim as defect 7, in a second table of the same file** — "The name is not chosen — three candidates await owner selection". Found only by re-running the sweep *after* correcting defect 7 | **No** |

**Defect 10 exists because I corrected defect 7 and stopped.** The two are the
same sentence in two tables of one file. Finding the first is not finding the
class, and the only thing that surfaced the second was re-running the search
after the first fix rather than treating the fix as the end of it. Recorded
because "sweep, correct, re-sweep" is the step this record's own subject was
missing.

**Defect 9's provenance is worth tracing, because it shows the mechanism rather
than a lapse.** "20" entered `unit-of-work.md` from
`CR-2026-08-22-TARGET-SCHEMA-TEST`, which computed its total over one of its own
two amendments — the arithmetic defect `GOV-2026-08-22-INC-01` Rec 4 corrected *in
that record*. Correcting the source did not reach the copy the source had already
seeded. Derived before assertion, not decremented:

```
sed -n '675,703p' <TE> | grep -oE 'test_[a-z_]+\.py' | sort -u | wc -l   -> 21
```

**Defects 7, 8 and 10 make the numeral tally decisive.** Tallied from the `Carried a
numeral?` column above rather than counted by eye: **six of the ten carry no
numeral** (defects 4, 5, 6, 7, 8, 10), and four do (1, 2, 3, 9). **A sweep for
superseded numbers finds four of ten — it misses six.**

The self-committed defect in § Verification is a **tenth item of a different
kind**, and is deliberately not folded into this tally: it was not a stale literal
at all but an incomplete *derivation* — a footprint computed over a supplied list
of five IDs instead of a pattern match returning ten. No sweep of any shape finds
that one. Only re-deriving from the artifact does.

**A consequence beyond documentation hygiene.** Items 3 and 4 were the only two
entries under `external-dependency-map.md`'s heading *"Awaiting the owner's
explicit selection or final wording"*. With both stale, that heading advertised
two owner decisions that did not exist — and **Gate 0's entire purpose is to
present the owner's outstanding decisions before Bolt 1.** Read literally, the
artifact would have sent the owner into a decision session over a module name
already chosen and an amendment already applied. Gate 0 was discharged with no
live decision outstanding; without this check it would have been discharged with
two false ones.

### Defects 4 and 5 are the ones that matter

Both are **contradictions internal to a single artifact**, which
`aidlc/spaces/default/memory/phases/inception.md` § Requirements Quality forbids
carrying forward. Defect 5 had one artifact simultaneously asserting that the four
leakage requirements have no acceptance row and that they left the untested list
because their acceptance rows were created. Both halves were true when written and
one became false the same day.

Defect 4 was **wrong when first written**, independently of any amendment: at
5 of 7, `external-products` was already at 71% against `models-and-baselines` at
78%. The word "share" was carrying both *count* and *proportion*, and that
conflation is what let two sites each claim the largest without either looking
wrong. Count and proportion are now named separately at both sites.

## The blind spot, stated as a mechanism

`governance/CHANGE_RECORD_PROCEDURE.md` step 2 reads:

> **Swept the workspace for that literal.**

A search for the superseded *literal* finds defects 1, 2 and 3. It cannot find
defects 4, 5 or 6, because none of them contains the old number — or any number.
What went stale in those three was not a figure but a **superlative** and a
**status claim** that the figure had supported.

This is the same class of defect the procedure was created to stop, arriving
through a channel the procedure does not cover. Rec 5 established the mechanism
and the mechanism has a hole in it.

**Remedy already applied.** A project practice was persisted at the stage 2.8
learnings gate, through `aidlc-learnings.ts persist` — the sanctioned write path,
with its audit event and admission conflict-check — under
`aidlc/spaces/default/memory/project.md` § Way of Working:

> ALWAYS sweep for the superlatives and status claims an amended figure
> supported, not only for the superseded numeral. […]

Two further practices were persisted in the same act, both earned in this work:
set-differencing ID lists rather than comparing totals, and not reopening a
recorded refusal merely because the material it refused is now within reach.

**`CHANGE_RECORD_PROCEDURE.md` is not amended here** — see § Open action.

## Files a sweep may not edit — honoured

`CR-2026-08-22-INC-CORRECTIONS` is **reported on and not edited.** It is a
completed change record, and that procedure's own § "Files a sweep may not edit"
reserves such records absent owner approval for annotate-in-place, which was not
sought for this item. Its falsified § Verification sentence stands in place; this
record is the correction of record.

Likewise unedited: `team-practices.md` and `aidlc/spaces/default/memory/team.md`,
both reserved to the practices-affirmation gate and tracked as **`RES-02`**, whose
17-versus-21 test-module staleness remains open at that gate.

## Verification

**Every count below was derived and printed before assertion**, per
`aidlc/spaces/default/memory/project.md` § Way of Working and
`CHANGE_RECORD_PROCEDURE.md` step 5.

**Untested requirements — 36**, derived twice from two independent artifacts:

```
grep -c "NO CURRENT ACCEPTANCE ROW" .../units-generation/unit-of-work-story-map.md   -> 36
grep "UNTESTED" .../requirements-analysis/requirements.md \
  | grep -vE "^\| *\*{0,2}(REQ|FR|NFR)-[A-Z0-9-]+…" \
  | grep -oE "(REQ|FR|NFR)-[A-Z0-9-]+" | sort -u | wc -l                             -> 36
```

The two ID lists were then **set-differenced in both directions and found
identical** — the same 36 requirements, not merely the same total.

**Per-unit untested counts**, from story-map Table 1, summing to 36:
`models-and-baselines` 7/9 · `acquisition` 7/15 · `regimes-diagnostics-reporting`
7/11 · `external-products` 4/7 · `inventory-and-registry` 2/7 · `foundation` 2/18
· `fixtures-and-reproducibility` 2/8 · `evaluation-and-comparison` 2/4 ·
`target-standardization` 1/6 · `governance-guards` 1/11 · `features-and-splits`
1/12.

> **A wrong derivation, recorded because the way it was caught is the lesson.**
> The first pass over `requirements.md` returned **40**. The excess was an
> artifact of the extraction, not of either document: four crosswalk rows lead
> with an ID *range* (`FR-P1-03-1…5`, `FR-P1-04-1…18`, `FR-P1-05-1…22`,
> `REQ-ENG-1…13`) and mention `UNTESTED` for one member of the range, so the
> extracted lead was the range's first ID. **Comparing the two totals showed a
> difference and gave no indication which side was wrong; set-differencing the ID
> lists named the four culprits immediately.** Anyone re-deriving this figure must
> exclude range-lead rows.

**Citation footprint of `GOV-2026-08-22-DP-01` — 38 lines across 16 files**,
per-file counts tabulated in `governance/reviews/GOV-2026-08-22-DP-01.md` § 3.

> **Superseded figure, and a seventh defect — mine, found after this record's
> first issue.** This record first stated **31 lines**, taken from a footprint
> derived over a **preset list of five finding IDs** copied from
> `CR-2026-08-22-INC-CORRECTIONS`' prose. Deriving the ID set by pattern instead
> returns **ten** distinct findings cited by the governed artifacts:
>
> ```
> grep -rhoE "DP-[A-Z]+-[0-9]+" --include="*.md" \
>   PreFlight aidlc/spaces/default/intents evidence governance | sort | uniq -c
> ```
>
> The four never searched for are **`DP-TEC-01`** (the sequencing deviation rested
> on an unstated upstream independence assumption), **`DP-TEC-02`** (the F10.7
> selection freezes were placed at Gate 0 *and* behind Bolt 1), **`DP-ML-02`** (two
> reporting obligations sat in prose but not in the list that gates the Bolt) and
> **`DP-DATA-01`** (the in-Kaggle rule was a Bolt list that silently exempted the
> two heaviest runs). A fifth, **`DP-CHAIR-03`**, was searched for by neither this
> record nor the provenance-gap record's first issue, which then asserted it was
> cited nowhere — a conclusion drawn from a grep that never included it.
>
> All five are now reconstructed in `governance/reviews/GOV-2026-08-22-DP-01.md`,
> and the error is recorded there in § 2 rather than overwritten.
>
> **Superseded literals for a future sweep:** **`31 lines`**, **`five finding
> IDs`**, **`the five IDs`**.
>
> **This is the same defect class as items 4, 5 and 6 above, committed while
> documenting them.** The figure was carried from adjacent prose rather than
> derived from the artifact — and the practice forbidding exactly that had been
> persisted to `project.md` hours earlier, in the same session. Recorded here
> because a record whose subject is sweep completeness cannot quietly fix its own
> incomplete sweep.

## Sweep (`CHANGE_RECORD_PROCEDURE.md` step 3)

**Superseded literals named for future sweeps**, per step 1:
`40 untested` · `40 of the 105` · `each of the 40` · `the balance of the 40` ·
`the 40 requirements with no acceptance row` · `five of its seven` ·
`external-products (5 of 7)` · `Five of this unit's seven` ·
`the largest untested share of any unit` · `the joint largest untested share` ·
`none of the four has a §16 or §19 row` · `16 citations` · `11 files` ·
`31 lines` · `five finding IDs` · `the five IDs`.

**A note on this list, which is the point of the record.** Sixteen literals, of
which **ten contain a digit and six do not** — derived, not counted by eye:

```
sed -n '/Superseded literals named/,/^$/p' <this file> | grep -o '`[^`]*`' | wc -l          -> 16
sed -n '/Superseded literals named/,/^$/p' <this file> | grep -o '`[^`]*`' | grep -c "[0-9]" -> 10
```

The six with no digit are `five of its seven`, `Five of this unit's seven`, `the
largest untested share of any unit`, `the joint largest untested share`, `five
finding IDs` and `the five IDs` — two superlatives and four cardinalities spelled
as words. Add `none of the four has a §16 or §19 row`, whose only digits are
*section* numbers rather than the amended figure, and a sweep keyed to digits is
searching for the wrong thing in seven of sixteen cases.

**This is the whole finding in one list.** A number that went stale is easy to
search for. A number spelled as a word, a superlative that depended on it, and a
status claim it supported are all invisible to that search — and here they are the
majority.

**Sites found and their disposition:**

| Site | Disposition |
|---|---|
| Defects 1–6, across three delivery-planning artifacts | **Corrected** before the stage 2.8 gate, superseded literal preserved at each |
| Defects 7–10, in artifacts of already-approved stages | **Annotated in place** on the owner's explicit approval at the Gate 0 discharge, superseded text preserved at each |
| `team-allocation.md` | **Clean** — swept, nothing found, null result recorded in the file |
| `delivery-planning-questions.md` § Sources and Q9 option E | **Deliberately not corrected.** A Q&A file records the question the human actually answered; the current figure is carried in the commentary beside the answer and in the plan artifacts |
| `phase-check-inception.md` line 117 | **Not a defect** — already explicitly labelled "Superseded figures, preserved for the audit trail" |
| `CR-2026-08-22-INC-CORRECTIONS` § Verification and its `16 / 11` figure | **Reported, not edited** — completed change record, reserved by procedure |
| `team-practices.md`, `aidlc/spaces/default/memory/team.md` | **Reported, not edited** — reserved to the practices-affirmation gate; tracked as `RES-02` |
| `application-design/decisions.md`, `*/memory.md` | **Not references** — historical review findings and stage diaries, correctly frozen at their dates |
| This record's own `31 lines` figure, and `governance/reviews/GOV-2026-08-22-DP-01.md`'s five-ID finding set | **Corrected** — see the boxed note in § Verification. Found after this record's first issue, by deriving the ID set by pattern rather than from a supplied list |

## Open action for the project decision owner

**Whether to amend `governance/CHANGE_RECORD_PROCEDURE.md` step 2** so the
procedure itself requires sweeping for dependent superlatives and status claims,
not only the superseded literal. Not done here: the project-rules layer already
carries the obligation through the persisted practice above, and amending the
procedure is a change to how every future record is judged — the owner's call,
not a side effect of this correction pass.

The gap between the two is real while it stands. A future change record can
satisfy the procedure's letter, pass its own § Verification, and still leave a
stale superlative behind — which is exactly what happened here.

---

**Status:** Complete. **Approved by:** Project decision owner, 2026-08-22, at the
AI-DLC stage 2.8 approval gate.
