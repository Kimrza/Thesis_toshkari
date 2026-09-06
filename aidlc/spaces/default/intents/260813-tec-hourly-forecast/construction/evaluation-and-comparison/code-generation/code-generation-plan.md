# Code Generation Plan — `evaluation-and-comparison`

**Unit** `evaluation-and-comparison` (Bolt 9) · **Kind** `library` · **Stage** `code-generation`
**Inputs**: `functional-design/` (R-103…R-112; `domain-entities.md` § 1–8; `business-logic-model.md` W-1…W-8), `nfr-design/security-design.md` (SD-C-01…SD-C-04, six guards, containment), `nfr-design/logical-components.md` (C-1…C-4), `unit-of-work.md` § 9 (Owns: `src/evaluation/masks.py`, `src/evaluation/metrics.py`, `scripts/07_evaluate_and_report.py`, `tests/test_common_masks.py`), `requirements.md` (FR-P1-04-7, FR-P1-05-7 `Pending` under D-32, FR-P1-05-17 `UNTESTED`, NFR-FAIR-01; context: FR-P1-05-6, -9, -12, -20). Consumed code: `src/models/train.py` (`Prediction`, `fit_predict`, `three_seed_mean`), `src/data/locked_test.py` (`AccessRecord`, `open_restricted`), `src/data/config.py` (`ConfigSnapshot`, exception hierarchy — fifteen, `PartitionError` included), `src/data/splits.py` (`materialise_locked_partition` G-05 guard), `src/external/{iri,gim}.py` (evaluation-time-only comparators).
**Answers (receipted)**: Q1 = A (memberships confirmed, change record + proposed D-number FIRST), Q2 = B (sibling `AccessRecord` gains the two containment fields, flagged for `governance-guards`), Q3 = A (`guards.py`, six refusals), Q4 = A (write-once manifest + atomic rename), Q5 = A (bootstrap attempt, smoke or recorded failure).
**Authority**: BLK-03 contract approved 2026-09-06 (`CHANGE_RECORD_2026-09-06_BLK03_confirmatory_contract.md`); BLK-04/BLK-09 approved 2026-09-05; D-27 UNREOPENED (verified: `evidence/DECISIONS.md` ends at D-32) — the R-103 import edge stays unauthorised and `ABL-DIFF` keeps refusing; D-28 fixes the DEC scored window at 2–31 December, 30 days; D-31 (G-09) authorises module creation; G-05/G-06 stay `Blocked`.

## Ground rules binding every step

Same as prior units (Python 3.11 target; in-place edits, never duplicates; no scientific
constant in source — memberships, the DEC window statement and every threshold reach code
ONLY from `configs/` or the governing artifact; two-tier errors; module docstrings stating
purpose/inputs/re-run behaviour; ruff clean or recorded substitute; a negative control per
hard rule; nothing discharged; smoke ≠ governed; **no git commit**). Plus this unit's own:
**no `src/evaluation` → `src/features` import, direct or transitive** (D-27; the R-103 edge
is unauthorised; `ABL-DIFF` refuses naming D-27 exactly as `train.py` built it);
`src/external/iri.py` / `src/external/gim.py` imported **at evaluation time only**, joined
onto the already-registered frozen mask (NFR-IRI-01, R-112); never a pairwise or
model-specific mask (NFR-FAIR-01); every refusal is an `IntegrityError` subclass naming file
and expectation; `FairnessError` and `InverseTransformError` are declared HERE
(`src/evaluation`), `PartitionError`/`LeakageError`/`LockedTestError` imported; the
discriminating rule (PartitionError = declared-identity disagreement, LeakageError =
information flow, FairnessError = member-vs-mask) is one copy in `guards.py`; no DEC read
outside `open_restricted`; `locked_test_accessed = true` on every access; no
practical-relevance threshold stated anywhere (PC-09).

## Recorded input — nfr-design review Minors riding READY (2026-09-05 ruling)

(a) SD-C-02 read-then-write race → resolved by Q4 = A in Step 3; (b) "proven once"
present-tense over-claim → moot, the controls actually exist and run under this pass;
(c) sixth guard missing from the illustrative example list → the test module carries all six
per-entry controls regardless. Also carried: `statistical-inference` R-113 precondition 2's
`PartitionError` correction is ITS owner's, not made here; `regimes-diagnostics-reporting`
prints the five reporting values, not this unit.

## Steps

- [x] **Step 1 — Change record FIRST: `governance/CHANGE_RECORD_2026-09-06_R106_comparison_sets.md`** [Q1 = A; Q2 = B; R-106]
  Records the owner's confirmation of the three comparison-set memberships (primary
  {M-01, M-02, M-03, M-06, B-01}; GIM {M-06, C-01}; tier-3 {M-04, M-05, M-06}), grounded in
  Vision §2.4 tiers 1–3, §8.4's model table, §8.9's matched-window clause, with a **proposed
  D-number text** for `evidence/DECISIONS.md` (owner adopts or edits; no agent writes the
  register); the Q2 = B sibling edit (two additive `AccessRecord` fields, flagged for
  `governance-guards`' record and re-check); and the honest limits (no supervisor signature
  artifact exists or is claimed; G-05/G-06 stay `Blocked`; FR-P1-05-7 stays `Pending`,
  FR-P1-05-17 `UNTESTED`).

- [x] **Step 2 — Config transcription: `configs/experiment.yaml` gains `comparison_sets`** [Q1 = A; R-106; TC-03e]
  The three sets as named entries with enumerated ordered `member_ids`, `model_id`,
  `benchmark_ids`, each citing the Step 1 record and Vision §2.4/§8.4/§8.9; member counts
  5 / 2 / 3 re-readable by test; nothing else in the file touched; no value §2.4/§8.4/§8.9
  does not fix is written.

- [x] **Step 3 — `src/evaluation/guards.py` (new)** [Q3 = A; Q4 = A; SD-C-01, SD-C-02; R-104…R-109]
  The six refusals as the single failure domain: `require_stamps` (`LeakageError` on `None`
  stamps / `transform_id` disagreement), `require_partition_agreement` (`PartitionError`),
  `require_registered_mask` (`FairnessError`: registered, frozen, exact declared membership,
  never pairwise, never merged sets), `require_target_space` (`InverseTransformError`;
  `untransformed` literal reads native; `ABL-DIFF` refuses naming D-27 — no inverse exists),
  `require_locked_receipt` (`LockedTestError`; three ordered limbs: prediction-hash receipt
  re-verified, SD-C-02 containment — both `AccessRecord` fields present, manifest re-hashes,
  scored `mask_id` ∈ `mask_bundle_ids` — and the D-28 window "2–31 December 2022, 30 days,
  first 24 h excluded and counted", a 1 December row raises), `require_mask_member_alignment`
  (`FairnessError` on member-vs-mask `partition_id` disagreement). `FairnessError` and
  `InverseTransformError` declared here deriving from `IntegrityError`; every raise names
  file/resource and violated expectation.

- [x] **Step 4 — `src/evaluation/masks.py` (new)** [R-106, R-107; W-1; FR-P1-04-7; Q4 = A]
  `build_comparison_mask`: stamps checked first (W-1 step 1), one intersection per declared
  set, deterministic `mask_id` from declared set + masked row content (recomputation
  reproduces or raises), per-station surviving AND exclusion counts, the five exposed
  reporting values (`mask_id`, `feature_set_id`, surviving counts, exclusion counts,
  scored-window statement), full stamp set (`phase_id`, `source_id`, `target_definition_id`,
  `partition_id`, member-`transform_id` set). `MaskRegistry`: once-only registration
  (second registration raises), the frozen-bundle manifest written ONCE via
  `.tmp` → fsync → atomic rename with a refusing second write (Q4 = A; the race analysis in
  the docstring); registry read path for the containment check.

- [x] **Step 5 — `src/evaluation/metrics.py` (new)** [R-104, R-105, R-108, R-110, R-112; W-2, W-6; FR-P1-05-7]
  `paired_loss_differential`: guards first, then the ordered pipeline — squared errors per
  (`station`, hour) on masked rows only → per-station mean of paired differences
  **benchmark minus model** → unweighted mean over the three stations. `EstimandResult` with
  orientation `benchmark_minus_model`, weighting `equal_station`, the machine-readable sign
  sentence, and the four stamps copied from the registered mask at construction (a missing or
  mask-disagreeing stamp fails). `MetricsArtifact`: completeness refusal per declared set
  (any missing member refuses emission), `beats_model` per benchmark from the estimand sign,
  the TEC-06 spatial-representativeness sentence emitted by the producing path on every
  IRI/GIM comparison, the fail-closed GIM overlap disclosure (no registered overlap-audit
  result → `FairnessError`; ordering by containment — comparator records the audit result's
  ID + content hash found at generation), the Phase-2 not-independent-blind-test statement as
  an artifact field. IRI/GIM joined at evaluation time onto the registered mask only (R-112).

- [x] **Step 6 — Q2 = B sibling edit: `src/data/locked_test.py` in place** [SD-C-02; flagged for `governance-guards`]
  `AccessRecord` gains `mask_bundle_ids: tuple[str, ...] | None = None` and
  `mask_registry_hash: str | None = None` (additive, optional — existing rows and callers
  unbroken); `open_restricted` populates both when a frozen-bundle manifest exists at access
  time (reads the manifest, hashes it, lists its `mask_id`s); docstring updated; the edit
  flagged in this unit's summary AND recorded for `governance-guards`' record/re-check.
  Existing behaviour without a manifest: fields stay `None` — and this unit's
  `require_locked_receipt` refuses a `DEC` metric on `None`, which is the fail-closed half.

- [x] **Step 7 — `scripts/07_evaluate_and_report.py` (new)** [W-5; services.md; §12/§13.2; R-109]
  Position 07; six-step stage entry (`ensure_process_determinism` first,
  `assert_no_raw_fields` before first write); `--config configs/` and `--phase 1|2`; reads
  predictions by manifest, builds/loads registered masks, computes estimands per declared
  set, emits the metrics artifact; the `DEC` path enters only through `open_restricted`
  (purpose `"locked_evaluation"`, G-05 signature reference in `authorization`) and
  `materialise_locked_partition`'s guard — **no `DEC` execution today**, the path exists and
  stops at the signature guard; honest `aborted` registry row on every `IntegrityError`;
  bootstrap intervals and breakdown tables NOT computed here (statistical-inference's and
  regimes-diagnostics-reporting's, running inside this script later per the boundary note).

- [x] **Step 8 — `tests/test_common_masks.py` (new)** [R-111; the (1),(3)–(32) controls owned here; WS-16]
  Masks: deterministic `mask_id` (recompute-mismatch fails), once-only registration, pairwise
  mask refused, membership exact (missing/extra/duplicate/merged-sets each raise), the five
  reporting values presence control (31), per-station counts recorded. Guards per entry
  point (Q3 = A): stamp-less prediction into mask build; mismatched-partition pair into the
  estimand; agreeing-but-mask-mismatched set (sixth guard); un-inverted `ABL-DIFF` at any
  metric refuses naming D-27; receipt-less `DEC` call refuses; containment controls —
  fields absent, manifest hash mismatch, scored `mask_id` ∉ `mask_bundle_ids`, 1 December
  row (18)–(23); second-write-of-manifest refusal (Q4 = A). Estimand: inverted orientation
  fails on a known-sign fixture (15), pooled weighting fails on asymmetric counts (16),
  unregistered mask raises (17), four-stamp presence/agreement control (30). Honesty:
  incomplete emission refused per set (24), missing TEC-06 sentence fails (25), GIM without
  registered audit result fails (26), missing `beats_model` fails (27), audit-after-comparator
  containment control (32). Matched windows: mismatched window/lag fails, instantiated on the
  tier-3 set (28). IRI/GIM join onto unregistered mask raises (29). Fresh-subclass catch:
  `InverseTransformError` lands the `aborted` row via R-10's stage-entry catch. Member counts
  5 / 2 / 3 re-read from `experiment.yaml`, never literal. Must-NOT-fire controls: the
  all-`DEC`-stamps-vs-DEC-mask pass, the `untransformed` B-01/C-01 pass, the
  coverage-audit-purpose pass. No test touches December 2022 content, the restricted root,
  or a real signature.

- [x] **Step 9 — Smoke + lint** [Q5 = A]
  Bootstrap attempt: winget user-scope Python 3.11 or uv into the session scratchpad —
  nothing installed into the repo. On success: full suite smoke run, result recorded
  (smoke evidence only, never governed). On failure: the exact failure recorded verbatim in
  the summary; `py_compile`-equivalent syntax posture at minimum. Ruff on touched files if
  available, else the stdlib substitute with ruff recorded as owed.

- [x] **Step 10 — Governance stop before commit (student acts)** *(record verified on disk; NO commit made by this pass; gate items listed in the code-generation summary)*
  Step 1's change record exists FIRST. Gate items: the proposed D-number for the membership
  confirmation (adopt or edit); the Q2 = B sibling edit routed to `governance-guards`' record;
  the R-103 import edge still unauthorised (D-27 stands; `ABL-DIFF` refuses); FR-P1-05-17
  still rowless; FR-P1-05-7 `Pending` (approved D-32, never run); the R-85…R-89 numbering gap
  (observed, unexplained); `statistical-inference`'s R-113 correction owed at its unit; the
  `project.md` GIM-disclosure wording correction owed at the §13 ritual; commit citing
  **D-27, D-28, D-31, D-32** as touched context plus the new D-number if adopted. **No
  governed commit before the records exist.** Nothing discharged: WS-16, TA-11, TA-18 stay
  `Pending`.

## Out of scope

The vector time-block bootstrap (`statistical-inference`); breakdown tables, figures, primary
results table (`regimes-diagnostics-reporting`); any `Transform.inverse` (D-27 unreopened);
executing `DEC` or any real December read; freezing G-05; any acceptance-row discharge;
`test_release_hashes.py` (exists, foundation's).
