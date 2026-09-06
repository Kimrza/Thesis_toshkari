# Code Generation Questions — `evaluation-and-comparison`

**Unit** `evaluation-and-comparison` (Bolt 9) · **Kind** `library` · **Stage** `code-generation`

State on disk, verified 2026-09-06 before these questions: `src/evaluation/` exists with an
empty `__init__.py` only. `open_restricted` and `AccessRecord` exist in
`src/data/locked_test.py` — but `AccessRecord` carries **none** of SD-C-02's two containment
fields (`mask_bundle_ids`, `mask_registry_hash`). `configs/experiment.yaml` carries **no
comparison-set declaration**. `evidence/DECISIONS.md` still ends at D-32: **D-27 remains
unreopened**, so `ABL-DIFF` keeps refusing and no `src/evaluation` → `src/features` import
may exist (the R-103 edge is unauthorised; stage 3.5 may not treat it as approved).
BLK-03's contract was approved this morning
(`governance/CHANGE_RECORD_2026-09-06_BLK03_confirmatory_contract.md`), so the confirmatory
`Prediction` this unit consumes is governed. TE §18.3's stop-and-report rule is why the
items below are questions rather than defaults.

**Recorded input (nfr-design Minors riding READY, per the 2026-09-05 ruling)**: (a) the
SD-C-02 read-then-write race between mask registration and locked-test access has no stated
atomicity guarantee — Q4 resolves it; (b) the "proven once / proven per entry point"
present-tense over-claim — moot here, the controls are actually written and run by this pass;
(c) the illustrative negative-control list omitting the sixth guard's example — doc style,
the test module itself carries all six.

---

## Question 1
**The three comparison-set memberships are a frozen scientific choice with no D-number.**
R-106 declares them configuration (`experiment.yaml`), proposed — primary
{`M-01`, `M-02`, `M-03`, `M-06`, `B-01`}, GIM {`M-06`, `C-01`}, tier-3 {`M-04`, `M-05`, `M-06`}
— and routes the confirmation to you as a §18.2/TC-03e student+supervisor choice. No
`comparison_sets` block exists in `experiment.yaml` today, and TE §18.3 bars any implementer
from filling it by convenience. The mask builder reads the declared set from config and
refuses on any mismatch, so without a declaration nothing can ever build a mask. How is the
membership handled?

A) Confirm the three memberships now — the change record written FIRST carries a proposed
   D-number text for `evidence/DECISIONS.md` (you adopt or edit it, exactly the FU-2 = B /
   BLK-03 pattern); after your explicit confirmation the three sets are transcribed into
   `experiment.yaml` citing that ruling and Vision §2.4/§8.4/§8.9, and the code asserts
   membership content from config, never from source
   > **Impact**: Every mask/metric path becomes buildable and testable against real declared sets. The transcription is a copy of your ruling under its citation — the D-121/`seeds.yaml` precedent. Honestly stated: this is you making the R-106 confirmation the design routed to the gate; no supervisor signature artifact exists and none is claimed.

B) Leave the memberships undeclared — `comparison_sets` stays absent, the mask builder
   refuses fail-closed naming the missing declaration, and the confirmation lands later
   under a separate ruling
   > **Impact**: No scientific choice is made this pass, but every mask-dependent test can only assert refusals; the three downstream units inherit an unbuildable comparison surface, and a second ruling is owed before anything scores.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the memberships are already grounded rule-by-rule in Vision §2.4 tier 1–3, §8.4's model table and §8.9's matched-window clause, the GIM/tier-3 separation exists precisely to protect the primary scored set, and the owner-equivalence precedent (D-122, D-28) covers the act. A is the only path that makes WS-16's evidence producible this Bolt; the copy's exactness is testable.

[Answer]: A

## Question 2
**SD-C-02's containment half-contract: `AccessRecord` lacks the two fields.** The design
proves mask-freeze-before-access by containment — the access record carries
`mask_bundle_ids` and `mask_registry_hash` — but those fields live in `governance-guards`'
`src/data/locked_test.py`, a sibling unit's module, recorded as owed to that unit "at its
next touch". This unit's `require_locked_receipt` enforces the check. What lands now?

A) Fail-closed, no sibling edit — `require_locked_receipt` refuses any `DEC` metric unless
   the access record carries both fields with a verifying manifest hash; since the fields do
   not exist yet, the refusal names the owed half-contract and `governance-guards`' record is
   flagged; the DEC path is unreachable anyway (G-05 `Blocked`)
   > **Impact**: Unit boundaries honoured; the containment check is real and tested against synthetic records carrying/omitting the fields; the sibling lands its half at its next touch with its own review. Nothing scoreable is delayed — no DEC metric can run before G-05 regardless.

B) Add the two fields to `AccessRecord` now as additive optional fields — an in-place edit of
   the sibling module, flagged for `governance-guards`' record and re-check, with
   `open_restricted` populating them when a mask-registry manifest exists
   > **Impact**: The half-contract closes in one pass, but a module whose unit was reviewed READY is edited outside its own stage without a recorded ruling — the same cross-unit-edit class FU-2 = B put behind an owner act. Needs your explicit instruction here to be legitimate.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the design itself assigns the population half to `governance-guards`, the refusal is this unit's deliverable, and the check is fully testable with synthetic records. B is procedurally yours to order, but buys nothing executable today (G-05 is `Blocked`, so no real DEC access can exercise the fields).

[Answer]: B

## Question 3
**Guard module shape.** SD-C-01 fixes one guard module with six refusals
(`require_stamps`, `require_partition_agreement`, `require_registered_mask`,
`require_target_space`, `require_locked_receipt`, `require_mask_member_alignment`), one
per-entry-point negative control, proposed name `src/evaluation/guards.py`, final naming owed
to 3.5. Confirm?

A) Confirm — `guards.py` as the single failure domain; public entry points enumerated as
   `build_comparison_mask` (W-1), `paired_loss_differential` (W-2), the `07` DEC path (W-5),
   and the metrics-artifact emission (W-6); each entry point calls the guard module before
   touching a row, and each gets its per-entry violating-input control
   > **Impact**: One copy of every refusal, nothing to drift — the design answer to the R-105-vs-R-92 drift the board caught. Matches the guard-home practice affirmed across the last three nfr-design units (project.md nfr-design:c58).

B) Fold the guards into `masks.py` / `metrics.py` inline
   > **Impact**: Two homes for refusal logic; the drift class SD-C-01 exists to prevent returns. Not recommended.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it is the design as reviewed READY, and c58's affirmed shape: one guard home, invocation proven per entry point.

[Answer]: A

## Question 4
**The SD-C-02 race Minor lands here.** Mask registration (this unit's write) and locked-test
access (the sibling's read) have no stated atomicity guarantee between the registry read and
the access-record write. The frozen bundle's manifest is already write-once per freeze. How
is the race closed?

A) Write-once semantics, no new machinery — the bundle manifest is written once per freeze
   via the project's `.tmp` → fsync → atomic-rename idiom and any second write refuses; the
   access path hashes the manifest it finds, so a mid-registration read sees either the old
   complete manifest or the new complete manifest, never a partial one; the residual
   "registration lands between read and record-write" case is benign by containment (the
   record simply evidences the earlier freeze) and is stated in the module docstring and the
   summary
   > **Impact**: Same idiom as the W-12 receipt path and R-13's overwrite refusal; no lock machinery to maintain; the race analysis is recorded where 3.6 and G-05 will read it.

B) Add an explicit lock file serializing registration against access
   > **Impact**: A second mutual-exclusion mechanism to test and to carry across two platforms (Kaggle has no shared lock semantics with local); more surface than the write-once manifest already provides.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — atomic rename plus write-once already gives the containment proof its integrity; a lock adds cross-platform failure modes the two-platform rule (TC-03c) would then own.

[Answer]: A

## Question 5
**No Python interpreter exists on this clone** (Store stubs only; no uv, no micromamba;
`winget` is present). The suite must still be smoke-run per the affirmed practice — smoke
evidence, never governed. What does this pass do?

A) Attempt a user-scope Python 3.11 bootstrap (winget, or uv fetched into the session
   scratchpad — nothing installed into the repo), run the full suite as smoke; on bootstrap
   failure (offline/no package source), fall back to B with the failure recorded verbatim
   > **Impact**: Best case: real smoke evidence for this unit and a re-run of the whole suite on this clone. Worst case: identical to B plus a recorded attempt. Nothing repo-resident either way.

B) Write everything; no execution on this clone — `py_compile`/syntax posture only if even a
   bare interpreter cannot be bootstrapped; the suite run is recorded as owed, and the
   summary states the honest limit exactly as models-and-baselines did
   > **Impact**: Code and tests land with zero execution evidence from this clone; the owed run must happen before any governed run per the affirmed practice (full suite before every governed run, in-session on Kaggle).

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — a bootstrap attempt costs minutes, keeps the repo untouched, and either produces real smoke evidence or documents exactly why none exists.

[Answer]: A

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Q1 = A — **The three comparison-set memberships are confirmed by you**: change record written FIRST with a proposed D-number text for `evidence/DECISIONS.md` (you adopt or edit); primary {`M-01`, `M-02`, `M-03`, `M-06`, `B-01`}, GIM {`M-06`, `C-01`}, tier-3 {`M-04`, `M-05`, `M-06`} transcribed into `configs/experiment.yaml` as `comparison_sets`, citing that ruling and Vision §2.4/§8.4/§8.9; code asserts membership content from config, never from source; a test re-reads the member counts 5 / 2 / 3 from config.
- Q2 = B — **The sibling module is edited on your instruction**: `AccessRecord` in `src/data/locked_test.py` gains `mask_bundle_ids` and `mask_registry_hash` as additive optional fields, `open_restricted` populates them when a frozen-bundle manifest exists, the edit is in place (no duplicate file) and flagged for `governance-guards`' record and re-check; this unit's `require_locked_receipt` refuses any `DEC` metric without both fields verifying (containment, not clocks).
- Q3 = A — **`src/evaluation/guards.py`** with the six SD-C-01 refusals as the single failure domain; entry points `build_comparison_mask`, `paired_loss_differential`, the `07` `DEC` path, and artifact emission each call the guards and each carries a per-entry violating-input negative control.
- Q4 = A — **Write-once + atomic rename** closes the registration/access race: the frozen-bundle manifest writes once via `.tmp` → fsync → rename, a second write refuses, readers see only complete manifests; residual interleaving benign by containment, stated in the docstring and the summary.
- Q5 = A — **Interpreter bootstrap attempted** (winget / uv, user scope or scratchpad, nothing in the repo); full suite run as smoke on success; on failure, fall back to written-but-unexecuted with the failure recorded verbatim. Smoke evidence only, never governed.
- Fixed context riding every step: D-27 unreopened — `ABL-DIFF` keeps refusing, **no `src/evaluation` → `src/features` import exists** (the R-103 edge stays unauthorised); IRI/GIM join at evaluation time only, onto the already-registered frozen mask; the `DEC` metric path exists and is unreachable behind the G-05 signature guard; estimand ordered pipeline benchmark-minus-model, equal-station, sign sentence machine-readable; `EstimandResult` carries the four stamps copied from the registered mask; `MetricsArtifact` refuses incomplete emission, carries `beats_model` per benchmark, emits the TEC-06 sentence and the fail-closed GIM overlap disclosure; no scientific constant in source; negative controls (1), (3)–(32) per the R-103…R-112 derivation; build set: `src/evaluation/{guards,masks,metrics}.py`, `scripts/07_evaluate_and_report.py`, `tests/test_common_masks.py`, plus the Q1 config transcription, the Q2 sibling fields, and the change record; no commit.

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Plan Approval

The code-generation plan for `evaluation-and-comparison` is at
`construction/evaluation-and-comparison/code-generation/code-generation-plan.md` —
10 steps: membership change record + proposed D-number FIRST (1), comparison_sets
transcription into experiment.yaml (2), guards.py with the six refusals incl. containment
and the D-28 window (3), masks.py with deterministic IDs, once-only registration and the
write-once manifest (4), metrics.py with the ordered estimand, four stamps, completeness
refusal and fail-closed disclosures (5), the Q2=B sibling AccessRecord edit flagged for
governance-guards (6), script 07 with the guarded unreachable DEC path (7),
test_common_masks.py with controls (1),(3)–(32) and the per-entry guard set (8),
bootstrap-attempt smoke + lint (9), governance stop (10).

- Approve Plan
- Request Changes

[Answer]: Approve Plan
