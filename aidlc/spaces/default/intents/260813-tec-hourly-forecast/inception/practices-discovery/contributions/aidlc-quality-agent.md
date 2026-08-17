**Collaborator:** aidlc-quality-agent

## Contribution

Scope of this review: the `## Testing Posture` section of `team-practices.md`, the
test-related rules in `discovered-rules.md`, and the test-related evidence in
`evidence.md`. Every claim below cites the file and section it rests on.

### A. What the draft established correctly

- The categorical judgement is right: this is a governed scientific pipeline, not a
  service, and `org.md`'s "tests run in CI before merge" has no mechanism here. That
  framing should survive integration unchanged.
- Refusing to invent an 80% figure is correct, and correct for a stronger reason than
  the draft gives — see (F) below.
- `pytest` as the required tool is correctly sourced
  (`PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §8.1, the
  approved-stack table row: "`pytest` | Required | Unit, integration, leakage, schema,
  denial, and fixture checks").

### B. Largest omission — §18.3 is this project's quality gate, and the draft never names it

`Technical_Environment_and_Research_Implementation(1)(2).md` §18.3 ("Preflight gate")
defines the mechanism that stands in for the CI gate `org.md` assumes. It is missing
from `team-practices.md` § Testing Posture entirely. It must be added, because it is
the only place the governing documents state a testable pass/fail criterion for "may
implementation proceed":

- **Decision criterion (quoted):** "zero unresolved P0 fields and no failing critical
  test." Evidence artifact: `aws_ai_dlc_preflight_report`.
- **The named critical set (quoted, §18.3 final paragraph):** "target contract and DCB
  sign; availability lags; **IRI-free denial**; split embargo; train-only transforms;
  comparison-wide masks and matched windows; checkpoint restore; vector bootstrap;
  release hashes; locked-test access guard." Ten items, not the two the draft names.
- **Preconditions:** all P0 decision-register entries for the affected component
  resolved; automated assertion that no required field in `data.yaml`,
  `features.yaml`, `experiment.yaml`, `seeds.yaml` is `TBD`; supervisor sign-off on
  the scientific hierarchy, IRI role, horizons, estimand, seeds, and locked-test
  protocol.
- **Binding on agents:** "Claude Code or any equivalent agent must not implement an
  affected component while its P0 decision is unresolved, and must stop and report
  rather than choose a default." This is a testing-posture rule with direct
  consequences for `code-generation` (3.5) and `build-and-test` (3.6) and belongs in
  the affirmed practice.

Suggested integration: a "Gate tests, not CI gates" bullet in § Testing Posture
enumerating all ten, plus the decision criterion verbatim, cited to §18.3.

### C. The test suite is a near-term deliverable, ordered ahead of acquisition (TC-06)

`aidlc/.../ideation/feasibility/constraint-register.md` TC-06 (`binding: hard`):
"Repository structure, pinned environment and test suite are built **before** any
acquisition work, inside this initiative." The draft's § Testing Posture does not
mention TC-06 at all, so it reads as if testing is a downstream concern. It is not:
TC-06 makes the suite a Construction deliverable of *this* initiative and fixes its
position in the order. This also supplies the missing rationale for why practices must
be affirmed now rather than at `build-and-test`.

TC-15 (correctly quoted by the draft) supplies the "why"; TC-06 supplies the "when".
Both belong in the section.

### D. Named tests: the draft names 2 of 17

`Technical_Environment_and_Research_Implementation(1)(2).md` §12 (repository tree,
`tests/` block) enumerates the required modules. The draft names
`tests/test_iri_denial.py`, `test_phase_boundary.py`, and "leakage tests" generically.
The full mandated set is:

`test_station_registry.py`, `test_rinex_schema.py`, `test_dcb_sign.py` (explicitly
"includes the reversed-sign negative control"), `test_hourly_target.py`,
`test_iri_denial.py`, `test_phase_boundary.py`, `test_reuse_registry.py`,
`test_feature_availability.py` ("asserts actual lag >= declared safe lag"),
`test_split_embargo.py`, `test_train_only_transforms.py`, `test_common_masks.py`,
`test_models_smoke.py`, `test_checkpoint_restore.py`, `test_bootstrap.py`,
`test_locked_test_guard.py`, `test_release_hashes.py`, `test_clean_run.py`, plus
`tests/fixtures/plumbing_7day/` and `tests/fixtures/scientific_1month/`.

Several are Phase 2 only (`test_rinex_schema.py`, `test_dcb_sign.py`,
`test_hourly_target.py` attach to `02_build_vtec_target.py` /
`03_verify_processing.py`, both barred from Phase 1 by §7.0). The affirmed practice
should list the set and mark the Phase 1 subset, rather than list two and imply the
rest do not exist. Workspace state for the record: no `tests/` directory exists yet
(`ls` of the workspace root; `evidence.md` does not record this, and it should).

### E. Testability — the draft's bullets have no pass/fail criteria, and the source documents do

`aidlc/spaces/default/memory/phases/inception.md` § Requirements Quality requires a
clear pass/fail criterion per requirement. The draft's § Testing Posture is prose with
no criteria attached. Two tables in the governing document supply them and are cited
nowhere in any of the four artifacts:

- **§16 Walking-Skeleton Acceptance Checklist, WS-01 through WS-20** — "Every check is
  pass/fail and must link to machine-readable or reviewable evidence. Visual
  inspection alone is insufficient... Acceptance occurs only when all 20 rows are
  `PASS`, each evidence target exists, hashes match, and no unresolved failure is
  waived informally." Directly test-bearing rows: WS-10 (IRI-denial fails on
  deliberate injection), WS-11 (availability lags, trailing F10.7, Dst diagnostic-only,
  SSN absent), WS-12 (splits/embargo, no window crossing a boundary, first 24 h
  excluded and counted), WS-13 (flattened matrix and sequence tensor share the same
  window values), WS-16 (comparison-wide masks with stable IDs, no pairwise mask),
  WS-17 (bootstrap reproduces exactly from seed 20221201), WS-18 (locked-test guard
  blocks December execution before G-05 and records access), WS-20 (clean CPU
  environment reproduces both fixtures within declared tolerances).
- **§19 Technical Approval Checklist, TA-01 through TA-32** — the implementation
  readiness criteria, each with a named evidence artifact and a `Pending` /
  `Blocked` status. Test-bearing rows the affirmed posture should point at: TA-07,
  TA-08, TA-09, TA-11, TA-12, TA-13, TA-14, TA-17, TA-18, TA-22, TA-23, TA-26, TA-27.
  Note TA-23 is the §18.3 preflight expressed as an approval row.

These two tables are the project's acceptance criteria. Since `user-stories` (2.4) is
`SKIP` in this scope (`aidlc-state.md` § Scope Configuration), WS-xx and TA-xx are the
*only* acceptance-criteria vocabulary Construction will have. That makes naming them a
practice, not a nicety.

### F. The "no coverage floor" position is right but the evidence is stated wrongly

Two corrections to the draft's coverage bullet:

1. **`org.md`'s 80% does not attach by its own terms.** The `org.md` § Testing Posture
   default is a per-scope table listing `mvp`, `enterprise`, `feature`, `infra`,
   `bugfix`, `security-patch`, `poc`, `refactor`, `workshop`. The active scope is
   `research-pipeline-governed` (`aidlc-state.md` § Project Information;
   `.claude/scopes/aidlc-research-pipeline-governed.md`). No row matches, so there is
   no inherited 80% floor to decline — say that, rather than "does not map cleanly",
   which reads as a judgement call against an applicable default.
2. **A numeric floor already exists in tooling, so declining to set one is not
   neutral.** `sensors/aidlc-coverage-threshold.md` states: "Targets travel inside the
   JSON (`targets`), falling back to **embedded defaults (line 80 / branch 70)**, so no
   per-stage config or dispatcher flag is needed". If `build-and-test` emits
   `test-pro-coverage-summary.json` without a `targets` object, the sensor reports
   against 80/70 by default and will emit `SENSOR_FAILED` findings against a suite
   that was never intended to hit them. The draft's "no coverage threshold is stated
   anywhere" is therefore inaccurate as a statement about this workspace. The
   interview must either set explicit `targets` for the sensor or accept 80/70 as the
   advisory reporting baseline — a choice, either way, and one whose input
   (`test-pro-coverage-summary.json.targets`) must be recorded now per `project.md`
   § Way of Working ("ALWAYS specify the inputs a gating condition depends on in the
   same stage that records the condition").

`evidence.md` correctly notes both sensors are advisory; it should add that
`coverage-threshold` carries embedded defaults, since that is the operative fact.

### G. Locked-test discipline — one correctness error and three missing mechanisms

The draft says "The locked December test set is opened exactly once, after G-05 is
signed... a supervisor signature controls, not a merge event." Correct as far as it
goes, but:

- **Correctness error.** Vision §8.3 first bullet: "December target values **may** be
  audited for coverage and regime counts without inspecting model performance. This
  audit is **required** before G-05." A flat "opened exactly once" reads as forbidding
  that mandatory pre-G-05 coverage audit. The affirmed practice must distinguish the
  required target-side coverage audit from the one-shot performance evaluation.
- **Missing: it is an executable guard, not only a signature.**
  `test_locked_test_guard.py` (§12 tree), WS-18 ("Locked-test guard blocks December
  performance execution before G-05 and records access"), TA-18 ("Guard test and
  access-log sample"), and §18.3's "locked-test access guard" in the critical set all
  make this a testable control. The draft presents it as governance only.
- **Missing: the registry flag.** Vision §8.3: "Locked-test access is recorded in the
  experiment registry with `locked_test_accessed = true`", and the registry must record
  failed and aborted runs as well (§13.4, NFR-AUD-01).
- **Missing: the exploratory-label rule.** Vision §8.3: "Any test-driven change is
  labeled exploratory." This is a testing-posture rule — it governs what happens to the
  suite and its results after a test-informed change, and it is the enforcement partner
  of `discovered-rules.md`'s existing PC-09 threshold rule.

### H. Reproducibility — cited at the NFR level only; the executable contract is missing

The draft cites NFR-REP-01 and TC-03g. Missing, and needed for a testable practice:

- **§13.2 Ordered clean-run contract** — a literal ordered command sequence beginning
  `python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day`
  and `--fixture scientific_1month`, then the nine phase-aware stage scripts. "Both
  fixtures must pass before full execution. The whole sequence must complete **on
  CPU**." This is the reproducibility test's actual definition; NFR-REP-01 only names
  its evidence file.
- **`test_clean_run.py`** (§12 tree) and **WS-20** / **TA-17** — the pass/fail form.
- **G-07 Reproducibility** (Vision §13.1 gate table, status `Blocked`, owner
  Supervisor/reviewer, evidence `environment_and_cpu_preflight_report` + clean-run log
  + matched artifacts, due before thesis submission). The draft names G-05 and G-06 but
  not G-07, which is the supervisor gate that actually accepts the reproducibility
  evidence it describes. `project.md` § Way of Working requires enumerating every open
  supervisor gate from the authority's gate table, not only those on the visible path.
- **Determinism is likewise testable, not asserted**: NFR-DET-01 / TC-21, three-seed
  element-wise mean as the confirmatory prediction, `test_bootstrap.py` and WS-17
  ("reproduces exactly from seed 20221201"), TA-13 and TA-26. `discovered-rules.md`
  carries the seeds rule but § Testing Posture does not record that it is verified by
  test.

### I. Unresolved contradiction the interview must resolve, not carry forward

`phases/inception.md` § Requirements Quality: "Never carry forward unresolved
contradictions between requirements; surface and resolve them explicitly."

§16 states acceptance "occurs only when all 20 rows are `PASS`". But §16.1 assigns
WS-01–WS-08 to **G-P3A Raw pipeline validity**, a Phase 2 gate, and §7.0's Phase 1 hard
prohibition bars Phase 1 from importing or executing the raw-processing path that
produces WS-02/WS-04/WS-05/WS-06/WS-07/WS-08 evidence (`02_build_vtec_target.py`,
`03_verify_processing.py`, `src/gnss/rinex.py`, `src/gnss/calibration.py`). A Phase 1
fixture run therefore **cannot** produce all 20 `PASS` rows without violating
NFR-PHASE-01. The team practice must state the Phase 1 acceptance subset explicitly
(WS-01, WS-09 through WS-20 appear to be the Phase 1-reachable rows) rather than
inherit "all 20". This needs a human decision at the interview; it is not mine to fix.

### J. The fixture rule the draft states as executable is not yet executable

`team-practices.md` § Walking Skeleton and `discovered-rules.md` both mandate "run both
required walking-skeleton fixtures... before any full-year job" as a hard rule. Its
inputs are unresolved:

- §15.1: Fixture 1's exact interval is **"TBD — freeze gate"** (provisionally NICO,
  March 2022, "subject to the coverage audit"); Fixture 2's month is **"TBD — freeze
  gate"** and "cannot be frozen unless prepared-data coverage exists for all three
  stations."
- §18.2 forbidden-choice table: "Fixture station, dates, or acceptance tolerances |
  Student | Q-31" — an agent may never pick them.
- §15.2: `tests/fixtures/<fixture_id>/fixture_manifest.yaml` must define identity,
  input hashes, expected schema, **row-count ranges**, support/missingness limits,
  timestamp tolerances, required outputs, expected **CPU** runtime range "measured
  before freeze", and permitted floating-point tolerances.

Per `project.md` § Way of Working, the gating condition and its inputs belong in the
same stage. Recommend the affirmed practice state the rule *and* its three unmet
inputs (Q-31 freeze, prepared-data coverage evidence for all three stations, measured
CPU runtime) rather than the rule alone. Also worth naming as the project's testing
pattern: **assertion data lives in the fixture manifest, not in test bodies** — that is
what §15.2 actually prescribes, and it is a real, transferable convention.

### K. Open governance finding in this stage's lane, uncarried

`governance/reviews/GOV-2026-08-15-FE-01.md` § `GOV-F-06` ("Test start threshold could
be read as narrowing the critical-test obligation", `MINOR`, ML & Statistical Methods):
evidence "GC-01 input 4 permits one executing leakage test as sufficient to begin
acquisition"; remediation "state that the start threshold does not narrow the critical
negative-path test set required at G-05 / G-07". `evidence.md` records reading only
`GOV-2026-08-15-AH-01.md` and lists `FE-01.md` among files "not opened in this pass".
This stage's § Testing Posture is where that remediation sentence belongs. Recommend
adding it verbatim in substance: *the one-leakage-test acquisition start threshold does
not narrow the critical negative-path test set required at G-05 and G-07.*

### L. The project's real testing methodology: paired negative controls

Across the source documents, every hard rule is paired with a deliberate-violation test
that must detect it: WS-10 (inject an `iri_*` field, denial test must catch it), WS-04
("the reversed-sign negative control clearly fails"), TA-07 (denial test plus an
import-boundary check), TA-08 and TA-12 (grep evidence that `SSN`, residual and GRU
modules are absent from the codebase), TA-27 (phase boundary plus transition-manifest
hash test). This negative-control-per-rule pattern is the actual house style and is
worth affirming as a mandated practice, since Construction will otherwise write
positive-path tests only.

One wording precision for the affirmed text: the draft writes that `test_iri_denial.py`
"must fail if any `iri_*` field... reaches ML training or inference". That is the
source document's phrasing (§6.2, §11 NFR-IRI-01) and should be preserved as a
quotation, but the affirmed practice needs the operational form too, or Construction
will build a permanently red test: *the injection test suite must pass by proving the
denial mechanism rejects a deliberately injected `iri_*` field* (this is exactly what
WS-10 and TA-07 measure).

### M. CI quality gates — record the absence explicitly, with its consequence

`aidlc-state.md` § Scope Configuration lists `3.7 (ci-pipeline)` among **Stages to
Skip**, and `.claude/scopes/aidlc-research-pipeline-governed.md` gives the reason:
"`infrastructure-design` and `ci-pipeline` skip — the pipeline runs on existing
local/lab compute with no new infrastructure surface." Combined with the workspace not
being a git repository, there is no CI, no merge event, and no automated trigger for
the ten §18.3 gate tests. The affirmed practice must therefore say **who runs the gate
tests and when**, or `org.md`'s "tests run in CI before merge" is carried forward as an
unmeetable inherited rule. The only stage that will produce test results in this scope
is `build-and-test` (3.6, `EXECUTE`), and the only defined trigger is §18.3's "before
the agent implements an affected component". Recommend affirming: gate tests run
locally on CPU before each affected component and again at each fixture run, with the
`aws_ai_dlc_preflight_report` as the recorded evidence.

### N. Two factual corrections to the drafts

1. **The scope file's skeleton flag was checkable and is answered.**
   `team-practices.md` § Walking Skeleton and `evidence.md` § What remains uncertain
   both leave open whether the active scope declares `skeleton: on` or `off`. It
   declares **`skeleton: off`** — `.claude/scopes/aidlc-research-pipeline-governed.md`
   frontmatter line 6, with a prose rationale under its `## Walking skeleton` heading
   ("The data contract is frozen and the pipeline stages attach to an existing, known
   input surface, so there is nothing to bootstrap end-to-end first. The first unit runs
   like any other; the ladder prompt does not fire."). The lead's underlying point
   still stands and should be stated plainly: AI-DLC's skeleton *ceremony* is off, which
   has no bearing on TC-03f's two fixtures, which remain `binding: hard`. Those are two
   different things and the draft currently blurs them.
2. **Miscitation in `discovered-rules.md` § Sources.** It cites
   "`Technical_Environment_and_Research_Implementation(1)(2).md` — ... §7.1
   (`test_iri_denial.py`)". §7.1 is "Split configuration" (the F1–F4 fold table) and
   contains no reference to that test. The correct sources are §6.2 (the binding rule
   under the ML feature dictionary: "`tests/test_iri_denial.py` must fail if one
   does"), §11 NFR-IRI-01, and §18.3. The same § Sources line correctly attributes
   `test_phase_boundary.py` to §7.0.

### O. Gaps the interview must resolve (my recommended question set)

1. Which coverage targets, if any, does `build-and-test` emit in
   `test-pro-coverage-summary.json.targets` — explicit values, or accept the sensor's
   embedded 80/70 advisory baseline?
2. Which WS-xx rows constitute the Phase 1 fixture acceptance subset, given that
   WS-02–WS-08 require the Phase-2-only raw path (see I)?
3. Who runs the ten §18.3 gate tests, on what trigger, and where is the result
   recorded, given no CI and no git (see M)?
4. Is the negative-control-per-hard-rule pattern affirmed as a mandated practice for
   every rule in `discovered-rules.md`, or only for the rules that already name a test
   (see L)?
5. Does the team affirm "assertion data lives in `fixture_manifest.yaml`, never
   hardcoded in test bodies" as the project's test-data convention (see J)?
6. Should `evidence/DECISIONS.md` gain a decision entry when a gate test's expected
   behaviour is first frozen, so test expectations are auditable in the same register
   as scientific decisions (this project's actual unit of auditable change, per the
   draft's own § Way of Working)?

## Positions

- AGREE: Treating this project's testing posture as categorically unlike a service's
  CI-gated regression suite — the draft's core framing is correct and should survive
  integration.
- AGREE: Declining to invent an 80% line-coverage floor — no governing document states
  one, and no `org.md` scope row matches `research-pipeline-governed`.
- AGREE: `discovered-rules.md` sourcing each rule to the normative core rather than to
  `constraint-register.md`, consistent with the `project.md` rule against relocating a
  requirement out of the layer the authority document fixes.
- OBJECT: § Testing Posture omits §18.3's preflight gate and its named ten-test critical
  set — the project's actual quality gate and the only stated pass/fail criterion for
  proceeding with implementation (see B).
- OBJECT: § Testing Posture omits TC-06 — the test suite is ordered **before** any
  acquisition work inside this initiative, which makes it a near-term Construction
  deliverable rather than a downstream concern (see C).
- OBJECT: Two of seventeen mandated test modules are named; §12's `tests/` tree and its
  Phase 1 / Phase 2 split are absent from all four artifacts (see D).
- OBJECT: No pass/fail criteria are attached to any Testing Posture bullet, though §16
  (WS-01–WS-20) and §19 (TA-01–TA-32) supply them — a direct miss against
  `phases/inception.md` § Requirements Quality, and material because `user-stories` is
  `SKIP` so WS/TA are the only acceptance vocabulary Construction will have (see E).
- OBJECT: "No coverage threshold is stated anywhere" is inaccurate for this workspace —
  `sensors/aidlc-coverage-threshold.md` carries embedded defaults of line 80 / branch 70
  that apply whenever the emitted JSON omits `targets`, so declining to choose is
  itself a choice with an unrecorded input (see F).
- OBJECT: "The locked December test set is opened exactly once" as written contradicts
  Vision §8.3's **required** pre-G-05 December coverage audit, and omits the executable
  guard (`test_locked_test_guard.py`, WS-18, TA-18), the `locked_test_accessed = true`
  registry flag, and the "any test-driven change is labeled exploratory" rule (see G).
- OBJECT: Reproducibility is cited only at NFR level; §13.2's ordered clean-run
  contract, `test_clean_run.py` / WS-20 / TA-17, and the open supervisor gate **G-07**
  are all missing, the last against the `project.md` gate-enumeration rule (see H).
- OBJECT: §16's "all 20 rows `PASS`" conflicts with §16.1's assignment of WS-01–WS-08 to
  the Phase 2 gate G-P3A and with §7.0's Phase 1 prohibition; an unresolved
  contradiction may not be carried past this stage (see I).
- OBJECT: The "run both fixtures first" rule is recorded without its unmet inputs —
  both fixture windows are `TBD — freeze gate`, student-owned under Q-31, and Fixture 2
  cannot be frozen before three-station coverage exists (see J).
- OBJECT: Open governance finding `GOV-F-06` falls in this stage's lane and its
  remediation sentence is not carried into the draft; `FE-01.md` was listed as unread
  in `evidence.md` (see K).
- OBJECT: The absence of CI is described but its consequence is not — with no CI stage
  (`3.7` is `SKIP`), no git and no merge event, the practice must name who runs the gate
  tests and when, or `org.md`'s CI rule is carried forward unmeetable (see M).
- OBJECT: `team-practices.md` and `evidence.md` leave the scope's skeleton flag open
  when it is directly readable — `.claude/scopes/aidlc-research-pipeline-governed.md`
  declares `skeleton: off` — and the draft blurs that AI-DLC flag with TC-03f's
  independently hard-binding fixtures (see N.1).
- OBJECT: `discovered-rules.md` § Sources miscites §7.1 as the source of
  `test_iri_denial.py`; §7.1 is the split-configuration table (see N.2).
