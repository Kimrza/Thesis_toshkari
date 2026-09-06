# Change Record — R-33 interface amendment: `write_restricted` in `src/data/locked_test.py`

**Date:** 2026-09-05
**Ruling:** Project decision owner, 2026-09-05, at the `acquisition` code-generation
plan gate (Q1 = A, receipted in
`aidlc/spaces/default/intents/260813-tec-hourly-forecast/construction/acquisition/code-generation/code-generation-plan.md`).
**Change class:** Interface amendment to an approved stage-2.6 contract
(`component-methods.md`'s `src/data/locked_test.py` block), applied at stage 3.5
under the accepted amendment.

## What was owed, and by whom

`functional-design/business-rules.md` R-33 and its Open item record **three amendments
owed to approved stage-2.6 contracts, stated not applied**, and state plainly that the
restricted writer and the `AccessRecord.purpose` extension *"need change records"* —
BLK-07's routing contract was **proposed rather than approved** until change control
cleared it. `nfr-design/security-design.md` § SD-A-03 (iteration-1 finding 3, Major)
added the disclosure that the amendment was **unapproved, not merely unbuilt**:
`governance-guards` had to accept the interface amendment before any implementation
could exist to be built.

## The ruling this record implements

**Q1 = A (2026-09-05): the R-33/BLK-07 interface amendment is ACCEPTED.** This record
is the change-control artifact that acceptance owed. It covers, exactly:

1. **`write_restricted(path, payload, *, record, registry)`** added to
   `src/data/locked_test.py` as a sibling of `open_restricted` — **log-before-WRITE**
   ordering through the SHARED `_append_and_flush` (one durability implementation for
   both directions), boundary derived from the module's own location (`_repo_root()`),
   refusal of ordinary paths, the same Q1 = A uncharacterised-platform fail-closed
   refusal as the read side, refusal of a non-`acquisition_write` purpose, refusal of
   an existing target (a restricted artifact is never overwritten), and **no byte
   written when the access-log append or its durability confirmation fails**.
2. **The `AccessRecord.purpose` enum extension** (R-33's constraint; Q2 = C at
   functional design): `PURPOSES` gains `acquisition_read` and `acquisition_write`
   alongside the three Vision §8.3 values. Recording a knowingly wrong value
   (`coverage_audit` for an acquisition write) was rejected because a G-05 reviewer
   must be able to read the access log's rows as meaning what they say.
   `authorization` widens by documentation to name a D-number for the acquisition
   purposes; its type (non-empty string) is unchanged, so existing rows and tests
   stay green.
3. **`RESTRICTED_LITERAL_EXEMPT_MODULES` stays at SEVEN members.** The writer lives in
   the module that already names the restricted root, so no new literal holder exists
   and R-28's one-door property is preserved (SD-A-03: a separate write path in
   `acquisition` would have taken the list from seven to eight; "the boundary does not
   weaken slightly; it ends").

**Ownership is unchanged:** the module is `governance-guards`'; `acquisition` is the
caller of `write_restricted`, never the boundary's co-owner. Any future change to the
guard is `governance-guards`' to review.

## What this record does NOT cover

* **BLK-07's authorization limb stays OPEN.** This amendment supplies the MECHANISM
  limb only. Which units may reach the locked month, and when, remains the project
  decision owner's decision; BLK-07's closure is a 3.1-owned contract decision and is
  not effected by this record. **No acquisition run may touch calendar 2022-12 while
  BLK-07 stands**, and no December content, path or fixture was touched in building or
  testing the writer — the negative controls in `tests/test_acquisition.py` run
  against `tmp_path` roots through the module's supported test seam only.
* **The other two owed amendments** — R-32's named accessors (`open_d9_input` and
  siblings) and R-35's `identity_fields` parameter on `src/data/release.py`'s
  `write_release` — are NOT covered here and remain owed; neither was built in this
  pass.
* **No scientific value is decided**, no `TBD — freeze gate` field is filled, no
  acceptance row (TA-08, TA-15, TA-16, TA-31, TA-32) is discharged, and no gate status
  changes. `component-methods.md` itself (the stage-2.6 artifact) is not edited by
  this record; this record IS the change-control trail the next revision of that
  contract cites.

## Evidence

* Implementation: `src/data/locked_test.py` (`write_restricted`, extended `PURPOSES`,
  `_repo_root()` documented test seam).
* Negative controls: `tests/test_acquisition.py` — failed log append aborts the write
  with no byte written; ordinary path refused; uncharacterised platform refused before
  any row; read purpose refused on the write path; existing target never overwritten;
  `PURPOSES` extension compatibility.
* Exempt-list preservation: `tests/test_locked_test_guard.py`'s membership assertion
  re-derives the seven on-disk holders and passed after this change (suite 497 passed
  / 2 skipped under Python 3.11.9 — smoke evidence, not governed evidence).

## Owed list, grown by this pass (recorded, not discharged)

* **TE §12 naming amendment for `src/data/acquisition.py`** — the third new-module
  naming amendment of this Bolt (after `experiment_registry.py` and
  `phase_contract.py`): TE §12's tree does not enumerate the module; Q2 = A placed it
  there. Owed to the TE amendment route, raised at the gate.
* **The governed commit** for this pass cites **D-144** (the approved notebook/product
  identity this script builds toward), **D-15** (the restricted relocation whose
  boundary the writer extends), and **D-5/D-10.2** (gaps as explicit NaN, extended to
  driver series) as touched decisions. **No governed commit before this record
  exists** — this record exists first, and the commit is the student's act, not the
  agent's.
