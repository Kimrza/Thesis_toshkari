# Change record — 2026-09-24 — D-28 amended to 29 days (option B); sweep halted on a new conflict

**Authority:** Student ruling, Layer-2 §2 of `RULING_REQUEST_2026-09-21_GOV-CG-01_OPEN_ITEMS.md`
— option B approved ("amend D-28's disclosure from 30 days to the measured 29"), option A (the
bounded 1-December read) explicitly rejected.
**Repository state:** working tree as left by the prior session, nothing committed by this pass.
**Status: RULED but NOT YET IMPLEMENTABLE** — this record exists to state exactly why, rather
than silently completing a sweep that would make the repository state worse.

---

## What was done

1. `evidence/DECISIONS.md` D-28 amended in place (history preserved, amendment appended and
   dated) to state the scored window is now 3–31 December, 29 days, with the rationale the
   Student gave (zero additional December contact; baselines not expected to be sensitive to
   one day).
2. `governance/RULING_REQUEST_2026-09-21_GOV-CG-01_OPEN_ITEMS.md` §2 — RULED block added.
3. `governance/REC_13_60_STATUS_2026-09-24.md` Rec 15 row — updated to reflect the ruling and
   the blocker.

## What was found, that stops this from being a documentation-only change

### Conflict 1 — the code computes 30 days, not 29, and cannot cleanly compute 29

```
$ grep -n "def scored_window_statement" -A 15 src/evaluation/guards.py
def scored_window_statement(
    month_start: dt.datetime, month_end: dt.datetime, *, embargo_hours: int
) -> str:
    ...
    scored_start = month_start + dt.timedelta(hours=embargo_hours)
    ...
```

`embargo_hours` is read from `configs/experiment.yaml` by a single shared function
(`src/data/splits.py:_read_embargo_hours`) and used for **every** partition — F1–F4's fold
embargoes and DEC's locked-month embargo alike (`src/data/splits.py:119`: *"`DEC` carries its
locked month. `embargo_hours` has..."*). This is the Mandated 24-hour embargo rule
(`org.md`/`project.md`: "each with a 24-hour embargo"), not a December-specific parameter.

- With `embargo_hours = 24` (frozen, Mandated): `scored_window_statement` computes exactly
  "2–31 December 2022, 30 days" — the value this amendment is trying to change.
- Setting `embargo_hours = 48` would produce 29 days for December, **but would also double
  every fold's embargo (F1–F4)**, silently widening a Mandated project-wide rule that has
  nothing to do with this finding. Not proposed, not done.
- No December-specific second embargo/exclusion mechanism currently exists in
  `src/evaluation/guards.py` or `src/data/splits.py`. Building one is a real design change,
  not authorized by this ruling.

**Consequence:** as the code stands today, any real mask build against the December partition
will disclose and enforce "30 days," not "29" — regardless of what `evidence/DECISIONS.md` now
says.

### Conflict 2 — D-59 directly contradicts this amendment and is itself frozen and live

```
$ grep -n "^| D-59" evidence/DECISIONS.md
| D-59 December day range = 2022-12-02 .. 2022-12-31 | **Student states supervisor
countersigned, 2026-09-21** ... | Matches D-28's locked scored set exactly (30 days) ...
Verified: `read_december_day_range` resolves to 30 inclusive days ... |

$ grep -n "december_day_range" configs/experiment.yaml
376:  december_day_range: "2022-12-02..2022-12-31"   # D-59 (proposed); matches D-28's scored set

$ grep -n "def read_december_day_range" -A 5 src/evaluation/regimes.py
def read_december_day_range(config: RegimeConfig) -> tuple[dt.date, dt.date]:
    """The EXPLICITLY CONFIGURED December day range, asserted at the call site (Rec 15).
    The value is a Student + Supervisor gate item; ...
```

D-59 is a **separately supervisor-countersigned** decision (2026-09-21), not merely a
restatement of D-28 — it is its own frozen, live, code-enforced config value. This amendment
was made under Student authority alone (per the Layer-2 §2 framing: "Owner: Supervisor. Due:
before G-05" was the *original* routing, but the Student ruled it directly this session).
Changing D-28's prose does not, and under this project's own rules (`project.md`: "NEVER
change a scientific value after seeing any result"; D-59's own supervisor-countersignature
requirement) **should not**, silently carry over into D-59 or `configs/experiment.yaml`.

**Consequence:** two frozen decisions now disagree on the same fact (D-28 says 29, D-59 says
30), and the code sides with D-59 (30), because D-59, not D-28's prose, is what's actually
configured and read.

## Why the 55-file sweep was not performed against project design/governance artifacts

The task asked for a sweep updating every file asserting "30 days" to "29," or leaving it with
a stated reason. Given Conflicts 1 and 2 above, updating the ~45 substantive occurrences (AI-DLC
functional-design docs across six units, historical change records, prior board reports) to say
"29" would not correct an inconsistency — it would **create** one, since the actual enforced,
supervisor-signed, code-read value is still 30. A reader of a "corrected" functional-design doc
saying 29 would be **more** wrong than one saying 30, because 30 is what the pipeline will
actually produce today. Making that edit now was refused on that basis, consistent with this
thread's standing rule to stop and report a second discrepancy rather than paper over it.

## Full file classification, all 55 originally-matched files

**Category A — false positives, unrelated to the December scored set (7 files), left
unchanged:** the seven `.claude/knowledge/*-agent/*.md` files (`nfr-design-guide.md`,
`cost-optimization-patterns.md`, `infrastructure-guide.md`, `nfr-requirements-guide.md`,
`observability-patterns.md`, `slo-sli-patterns.md`, `nfr-reliability-guide.md`) all match on
generic SLO/log-retention "30 days" boilerplate (e.g. *"99.9% SLO = 43.2 minutes of downtime
per 30 days"*) — framework reference material, never about December. Verified by reading the
matched lines directly (shown above in this session's transcript).

**Category B — auto-generated, not hand-authored (3 files), left unchanged:**
`graphify-out/{2026-09-06,2026-09-07,}/GRAPH_REPORT.md` are knowledge-graph outputs generated
from the rest of the repository; editing them by hand would be overwritten by the next
`graphify update` and is not this project's convention.

**Category C — `evidence/DECISIONS.md` and this thread's own live tracking documents (3
files), updated:** `evidence/DECISIONS.md` (D-28 amended, D-59 conflict flagged inline),
`governance/RULING_REQUEST_2026-09-21_GOV-CG-01_OPEN_ITEMS.md` (§2 RULED block added),
`governance/REC_13_60_STATUS_2026-09-24.md` (Rec 15 row updated).

**Category D — historical, dated governance records and board reports (9 files), left
unchanged, per this project's standing rule against editing a delivered record's substance**
(`project.md`: "NEVER edit a human-signed record... route ONE explicit ruling to the human"):
`governance/CHANGE_RECORD_2026-08-28_locked_scored_set.md`,
`governance/CHANGE_RECORD_2026-09-06_R123_regimes_and_reporting.md`,
`governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md`,
`governance/CHANGE_RECORD_2026-09-21_climatology_refit_and_reconciliation.md`,
`governance/FREEZE_DECISION_REQUEST_2026-09-10.md`,
`governance/reviews/GOV-2026-08-28-FD-01.md`,
`governance/reviews/GOV-2026-09-20-CG-01.md`. These are dated records of what was true and
decided *at the time they were written* (all pre-date this amendment); "30 days" was the
correct, frozen figure when each was written, and rewriting their substance would falsify the
historical record the way rewriting git history was already rejected for the same reason. (Note:
this differs from the earlier §B-1 email redaction, which replaced a single PII literal without
touching any finding's substance — changing "30" to "29" changes a finding's substance and is
not the same class of edit.)

**Category E — live project design/governance artifacts describing the current system
contract (~33 files), left unchanged, blocked on Conflicts 1/2 above:** the AI-DLC per-unit
`functional-design/*.md` files across `evaluation-and-comparison`, `features-and-splits`,
`fixtures-and-reproducibility`, `inventory-and-registry`, `regimes-diagnostics-reporting`,
`statistical-inference` (business-logic-model.md, business-rules.md, domain-entities.md,
functional-design-questions.md — 4 files × 6 units, minus a couple of units missing one file
type = ~22 files), the `inception/application-design/*.md` set (5 files),
`construction/build-and-test/memory.md`, and
`construction/evaluation-and-comparison/code-generation/{code-generation-plan,code-summary}.md`
(2 files, which also cite a specific test, `test_scored_window_statement_reproduces_d28_verbatim`
in `tests/test_common_masks.py`, that currently asserts the 30-day string verbatim — also not
edited, for the same reason, and because it sits in a §18.3-critical test module under the same
class of AI-DLC stage-receipt caution flagged for the chokepoint scanners in the prior session).
**All of these correctly and currently describe the system as it actually behaves (30 days).**
They become stale only once Conflicts 1 and 2 are resolved, at which point they are the correct
sweep target — not before.

## What is needed from the owner

One of the following, before this amendment can be completed:

1. **Amend D-59 too** (needs Supervisor countersignature, since D-59 already carries one) and
   add a December-specific embargo/exclusion mechanism to the code (a real, reviewable change
   to `src/evaluation/guards.py`/`src/data/splits.py`, distinct from the shared 24-hour fold
   embargo) — then the Category E sweep becomes correct to perform.
2. **Revert this amendment and reconsider option A** (the bounded, logged 1-December read) —
   D-59 and the code already agree with the pre-amendment 30-day state, so nothing else would
   need to change.
3. **Hold this amendment as a recorded-but-pending scientific intention**, explicitly not
   applied to config or code, until a dedicated session resolves D-59 — the current state
   (D-28 says 29 with a flagged conflict, D-59 and the code still say 30, nothing else swept)
   is internally honest about being unresolved, which is why it was left this way rather than
   picking a side unilaterally.

**Decision required — which of the three above, or another disposition.**
