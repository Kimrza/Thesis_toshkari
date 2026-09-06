# Code Generation Questions — `acquisition`

**Unit** `acquisition` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`

Two genuine gaps stand open at implementation time; everything else is
design-fixed (retrieval-integrity ordering SD-A-01; redaction rules SD-A-02;
provenance contract SD-A-04; R-31 timestamp membership; the retry/backoff/
timeout operational values are owed at 3.5, are explicitly not scientific
constants, and are proposed concretely in the plan for approval there).

**Recorded input (human ruling, 2026-09-05)**: this unit's terminal READY
nfr-design review carries two record-only Minors (a missing prior-review
receipt in the artifact, and one prospective-versus-remedial framing note);
neither changes a design decision — listed in the plan as record-only, per
`governance/RULING_2026-09-05_nfr-design_governance_dispositions.md`.

---

## Question 1
`write_restricted` (SD-A-03, Q2=A): the design places the restricted-root
writer as a sibling of `open_restricted` inside `governance-guards`'
`src/data/locked_test.py` (one module, one door, exempt list stays at seven) —
but the interface amendment is **UNAPPROVED, not merely unbuilt**:
`component-methods.md`'s approved block carries no `write_restricted` and no
shared `_append_and_flush`, and R-33 says the writer and the
`AccessRecord.purpose` extension "need change records". BLK-07's routing
contract is a proposal until change control accepts it. Build it this run?

A) Approve the interface amendment now — this answer is the owner's change-control acceptance; a change record citing R-33/BLK-07 is written to `governance/` before any commit, and `write_restricted` + shared `_append_and_flush` + `AccessRecord.purpose` are built in `src/data/locked_test.py` this run (log-durably-then-write ordering, negative controls)
   > **Impact**: BLK-07's mechanism limb becomes real; acquisition's restricted writes route through the one door; the exempt list stays at seven. Adds one governance artifact (the change record) to the pre-commit owed list. `governance-guards` owns the module — this ruling doubles as that acceptance since both units sit in this Bolt under one owner.

B) Defer — build acquisition without any restricted-write path; BLK-07 stays open
   > **Impact**: No December-touching write is possible anyway (BLK-07 bars it), so nothing built this run is blocked — but the writer contract stays unbuilt, BLK-07 unresolved, and a later run must reopen `locked_test.py`. The FULL re-verification path stays read-only.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the design's argument (one module names the restricted literal; a write that logs after is a mutation with no record) is complete and reviewed; deferring only splits the same change across two Bolts. Risk stated: this is a change-control acceptance by ruling — the change record must actually be written before commit, and December stays untouchable regardless (BLK-07's no-2022-12 bar is lifted by a governed contract plus logged access, not by this code existing).

[Answer]: A

## Question 2
Acquisition's operational code needs a module home. The unit Owns
`scripts/00_acquire_prepared_vtec.py`, the self-contained D-144 notebook, the
two manifest writers, and `tests/test_acquisition_window.py` — but no `src/`
module is named anywhere for the redaction serializer (`CredentialEgressError`,
SD-A-02), the bounded-retry retrieval client (TS-A-01), or the manifest
writers. Where does this logic live?

A) New module `src/data/acquisition.py` — serializer, retrieval client, manifest writers as importable library code; `scripts/00_acquire_prepared_vtec.py` orchestrates it; TE §12 naming amendment recorded (config.py / experiment_registry.py precedent)
   > **Impact**: Follows the project's own rule that reusable logic belongs in `src/` and scripts orchestrate; the serializer becomes one testable chokepoint other units can import. Adds a third §12 naming amendment to the owed list.

B) Everything inside `scripts/00_acquire_prepared_vtec.py` as script-local helpers — no new module, no amendment
   > **Impact**: §12 already names the script, so no naming amendment — but the redaction chokepoint becomes script-local (untestable without importing a script as a module), and "notebooks do not own production logic" pressure lands on the script instead. Violates the reusable-logic-belongs-in-src/ practice for a security-critical boundary.

C) Serializer into foundation's `src/data/config.py` (beside credential resolution), client + writers in the script
   > **Impact**: No new module, but it moves acquisition's egress boundary into the module every unit imports and makes `foundation` co-own a control SEC-A-03 assigns to this unit — the exact "depending on a sibling to catch its own leak" shape SD-A-02 rejects.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — a security chokepoint needs an importable, directly-testable home, and the naming-amendment path is already established twice this Bolt. Risk stated plainly: the §12 amendment record is owed before the commit that creates the module.

[Answer]: A

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Q1 = A — the R-33/BLK-07 interface amendment is ACCEPTED by this ruling: `write_restricted` + shared `_append_and_flush` + `AccessRecord.purpose` are built in `governance-guards`' `src/data/locked_test.py` this run, log-durably-then-write, with negative controls; a change record citing R-33/BLK-07 is written to `governance/` before any commit. BLK-07's no-2022-12 bar stands regardless.
- Q2 = A — new module `src/data/acquisition.py` hosts the redaction serializer (`CredentialEgressError`; signed URL + auth header refused unconditionally, entropy/prefix heuristic blocks-and-names, reviewed allowlist), the bounded-retry retrieval client (completeness check BEFORE hash; partial never promoted; divergence recorded, overwrite refused), and the manifest writers (full provider filename incl. version suffix, retrieval date, SHA-256, driver release-grade field, NaN-at-acquisition). `scripts/00_acquire_prepared_vtec.py` orchestrates. TE §12 naming amendment owed (third this Bolt).
- Plan proposes the operational retry values (bounded retries, exponential backoff, per-request timeout — recorded in the run record) for approval at Plan Approval; they are not scientific constants.
- Pre-commit hook extended: notebook saved-output cells refused (SD-A-02 limb 2).
- Recorded input: two record-only review Minors listed in plan; no acceptance row claimed; no commit.

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Plan Approval

The code-generation plan for `acquisition` is at
`construction/acquisition/code-generation/code-generation-plan.md` — 9 steps:
redaction serializer, retrieval client, manifest writers in new
`src/data/acquisition.py` (1–3), `write_restricted` in `locked_test.py` under
the accepted R-33 amendment (4), `scripts/00_acquire_prepared_vtec.py` (5),
notebook saved-output pre-commit refusal (6), tests (7), smoke + lint (8),
governance records + stop (9). Proposed operational values: 5 retries,
exponential backoff 1 s base ×2 cap 60 s with jitter, 60 s timeout — recorded
per run.

- Approve Plan
- Request Changes

[Answer]: Approve Plan
