# Code Generation Questions — `target-standardization`

**Unit** `target-standardization` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`

Two rulings the nfr-design routed to a human are needed before code exists;
everything else is design-fixed (the caveat COLUMN with round-trip test; the
sixteen-field D-17 contract; value-level closed-set diff with its tolerance
left to the fixture manifest; asserted-never-substituted excluded set; no
`02a`/`02b` invention; the D-17 authority question and the run-manifest
dependency stay gate items). The standardized target is NOT produced this run
— the QC list is `TBD — freeze gate`, and the refusal is the designed
behaviour. The schema-test module name is settled: `CR-2026-08-22-TARGET-SCHEMA-TEST`
already amended the §12 tree with `tests/test_prepared_target_schema.py`.

**Recorded input (human ruling, 2026-09-05)**: this unit's terminal READY
nfr-design review Minors are record-only (the re-dated interpreter-reachability
note; banner corrections); listed in the plan, per
`governance/RULING_2026-09-05_nfr-design_governance_dispositions.md`.

---

## Question 1
`StandardizationError` — this unit's only `RAISES` declaration, absent from
`config.py`'s `__all__` (set difference is exactly that one name), and the
nfr-design question set never asked about it (DISC-T-1, routed here for an
explicit yes/no). Declare it in `src/data/config.py` like the six you have
already ruled on (IntegrityError subclass, `__all__`, any-future clause)?

A) Yes — identical disposition
   > **Impact**: SD-T-01's QC-gate refusal and the fifth-transformation failure get a declared, catchable class; consistent with the six prior rulings of this shape.

B) No — defer; refusals raise generic `IntegrityError`
   > **Impact**: Standardization failures indistinguishable by type; later ruling adds the class + rename sweep.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — raised by this unit alone, nothing to reconcile; the question exists only because of the no-silent-widening rule.

[Answer]: A

## Question 2
While `qc_operations` is `TBD — freeze gate`, what does standardization do?
Your nfr-design Q2=A chose fail-closed ("refuse to RUN"), but that answer was
given on an option set that omitted a third option, so the corrected design
routes the choice back to you (SD-T-01 correction box).

A) Refuse to RUN — no standardized target artifact is produced at all until the QC list is frozen under a D-number; the raise names `configs/data.yaml` `qc_operations` and the frozen-under-a-D-number expectation
   > **Impact**: Nothing uncertain ever exists on disk — the strongest containment, matching the unit's own "rather produce nothing" posture. Cost: every downstream consumer of the target waits on the supervisor freeze; fixture exercise of the full pipeline path also waits (schema/caveat tests still run on fixtures — the rule's scope binds only target-producing runs).

B) Refuse to RELEASE — the run may produce the artifact, but it is never hashed, registered, or promoted, and is marked non-governed
   > **Impact**: Fixture exercise and downstream development keep moving. Risk is the one the design names: a non-governed file is still a file, and this project's own evidence (FULL) records how a caveated artifact becomes a relied-on one.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the artifact-on-disk argument is this project's own realized failure mode (FULL), and the schema/caveat contracts stay testable against fixtures either way, so B's practical gain is small next to its risk.

[Answer]: A

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Q1 = A — `StandardizationError` declared in `src/data/config.py` (IntegrityError subclass, `__all__`, R-01 any-future clause, not an enumeration entry).
- Q2 = A — **refuse to RUN**: while `qc_operations` is `TBD — freeze gate`, no standardized target artifact is produced; the raise names the field and the frozen-under-a-D-number expectation (never mere non-emptiness). Scope bound: only target-producing runs — the D-17 schema contract, the caveat column, and their fixture tests run regardless.
- Build set: `src/data/prepared.py` (four-transformation closed set, fifth fails; D-17 sixteen-field contract; `phase_id`/`source_id`/`target_definition_id` on every row; lineage-caveat COLUMN with the two disclosures + this unit's own round-trip preservation test; excluded set asserted never substituted; D-19 thresholds read from config with their basis, never inlined; data-quality block with unexplained-kept-unexplained; uncertainty budget states bounds), `scripts/02_standardize_prepared_target.py` (position 02, `--phase 1`, six-step entry, never a DCB/STEC/mapping/satellite/arc field, never the receiver-specific label), `scripts/03_verify_processing.py` Phase 1 scope (value-level closed-set diff; float tolerance from the fixture manifest — unset → stop naming TE §15.2), `tests/test_prepared_target_schema.py` (name per `CR-2026-08-22-TARGET-SCHEMA-TEST`).
- Gate items restated, not decided: the D-17 authority question (R-20's shape), the run-manifest executed-scripts dependency on foundation, the consumer half of the caveat contract, no `02a`/`02b` invention.
- No standardized target produced; nothing discharged; no commit.

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Plan Approval

The code-generation plan for `target-standardization` is at
`construction/target-standardization/code-generation/code-generation-plan.md`
— 7 steps: StandardizationError (1), prepared.py — closed set, D-17 contract,
IDs, caveat column, asserted excluded set, refuse-to-RUN gate (2), script 02
(3), script 03 value-level diff (4), test_prepared_target_schema.py + negative
controls (5), smoke + lint (6), governance stop (7).

- Approve Plan
- Request Changes

[Answer]: Approve Plan
