# Change-record procedure

Established 2026-08-22 under `CR-2026-08-22-INC-CORRECTIONS`, on the project
owner's approval of `GOV-2026-08-22-INC-01` **Recommendation 5, Option 1**.

This file exists because no change-record template or procedure existed when the
recommendation was approved: `governance/` held ten change records and two
countersignature requests, none of them a template. The procedure below is
therefore stated once here rather than repeated in each record.

## Why this exists

Between 08:00 and 15:00 on 2026-08-22, six change records amended overlapping
parts of the same documents. Every record was individually correct. The defect
was that **nothing swept the artifacts that read the amended figures**, so
derived views froze at four different points in one day's sequence:

| Figure | Value by artifact after the wave |
|---|---|
| Mandated test modules (TE §12 tree) | 17 (`team-practices.md`) · 19 (`unit-of-work.md`) · 20 (`CR-2026-08-22-TARGET-SCHEMA-TEST`) · 21 (TE §12, REQ-ENG-4 lead) |
| Untested requirements | 36 (`requirements.md`) · 40 (six other live sites) |

`GOV-2026-08-22-UG-02` Rec 3 had already found and fixed this exact defect class
earlier the same day, at 25 sites. It recurred within hours in the next stage.
Fixing the individual numbers does not address the mechanism; this step does.

## The propagation sweep — required in every change record

A change record that amends a **count, an enumeration, an ID range, a cardinality
or a status** is not complete until its author has:

1. **Named the superseded literal.** State the old value verbatim, not only the
   new one. A record that says "the count is now 21" without saying it was 19
   gives a later sweep nothing to search for.
2. **Swept the workspace for that literal.** Search every governed tree — the
   authority documents under `PreFlight/`, the active intent's artifacts under
   `aidlc/spaces/<space>/intents/<intent>/`, the memory layers under
   `aidlc/spaces/<space>/memory/`, `evidence/`, and `governance/` itself,
   including the record being written.
3. **Recorded the sweep result in the record**, as a list of every site found
   with its disposition — corrected, deferred with owner and gate, or judged
   not-a-reference. A sweep that finds nothing records that it ran and found
   nothing. **An unrecorded sweep counts as no sweep.**
4. **Checked the record's own arithmetic against its own scope.** Where one
   record carries two or more amendments in a single act, every total it states
   must be computed over **all** of them. This is the specific defect
   `CR-2026-08-22-TARGET-SCHEMA-TEST` carried: it computed 20 over one of its two
   amendments while the combined result was 21.
5. **Re-derived rather than decremented.** Compute the new figure from the
   artifact and print the command, per `project.md` § Way of Working. Never
   adjust a total by hand from the size of the change.

## Files a sweep may not edit

A sweep **reports** on these; it never edits them:

- `aidlc/spaces/<space>/memory/team.md` and the other memory layers —
  `org.md` reserves them for the practices-affirmation gate. A stale figure
  found there is recorded as a residual obligation with that gate as its owner
  (the standing example is `RES-02`).
- A completed stage's artifacts, unless the project owner has approved
  annotate-in-place for that item. The precedent and its reasoning are recorded
  at `GOV-2026-08-22-INC-01` Rec 7, where the board itself split on the question
  and the owner settled it.

## Relationship to Vision §15.2

This procedure is **documentation hygiene, not change control.** It adds no
authority and removes none. Whether an amendment is permitted at all remains a
Vision §15.2 question, decided by the project owner or supervisor; this file
governs only the completeness of the record once an amendment is approved.
