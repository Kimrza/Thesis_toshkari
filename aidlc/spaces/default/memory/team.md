# Team-Level Rules

> This team's affirmed practices and corrections. Loaded after `org.md` as
> strict-additive guidance; contradictions with broader policy are rejected.
> Populated by the practices-discovery affirmation gate. Edit at the gate,
> not directly.

## Way of Working

Version control is required, not optional. `Technical_Environment_and_Research_Implementation(1)(2).md`
§13.1 requires every run to capture a **code commit** as part of its environment
lock; §13.4 makes `code_commit` a required column of every experiment-registry
row; §19 TA-01's evidence column is "Repository tree and **code commit**"; §10's
credential rule ("environment configuration excluded from **version control**")
itself presupposes version control exists. The earlier draft's framing — that no
governing document mandates version control — is corrected: it does (all three
reviewers independently flagged this), and the interview question was never
*whether* to use git, only *how* (Q1).

Affirmed practice (Q1=C, Q2=C):

- Initialize git now, before any further acquisition work. Work directly on
  `main`. No feature branches, no pull requests — this is a single-author thesis
  codebase (student: Kimia Rezaei) with a supervisor (Dr. Reza Saraf Shirazi) who
  signs at named freeze gates, not one who reviews merges. This narrows, but does
  not relocate, `org.md`'s trunk-based-development default: the trunk exists, the
  branch/PR ceremony around it does not, per `project.md` § Way of Working
  ("honour a human's disposition by narrowing what a rule requires, never by
  relocating a rule the governing normative core fixes").
- Tag each freeze gate — G-05, G-06, and each phase transition — so the frozen
  state at that gate is separately recoverable by tag, in addition to the commit
  history.
- Both `evidence/DECISIONS.md` and commits stand as records, with a hard linking
  rule: `evidence/DECISIONS.md` (D-1 through D-10 today) remains authoritative
  for scientific and governance decisions — a decision is not real until it has
  a D-number. Any commit that changes a scientific constant, a config value
  (`data.yaml`, `features.yaml`, `experiment.yaml`, `seeds.yaml`), or another
  governed artifact must cite its D-number in the commit message. This keeps the
  project's existing, already-working decision-recording practice as the
  scientific record of truth while giving code changes their own commit
  history.
- Before the first commit, the `.gitignore` needs a credential/secret deny-list
  it does not currently have (no `.env`, `*.key`, `kaggle.json`, `.netrc`,
  `credentials*` entries were found — devsecops review, item J) so that §10's
  "excluded from version control" mechanism actually exists before anything is
  committed. This is a precondition of initializing git safely, not a separate
  practice.

## Walking Skeleton

No AI-DLC skeleton ceremony: the active scope file,
`.claude/scopes/aidlc-research-pipeline-governed.md`, declares `skeleton: off`
in its frontmatter, with the stated rationale that the data contract is frozen
and the pipeline stages attach to an existing, known input surface, so there is
nothing to bootstrap end-to-end first. The first unit runs like any other Bolt;
the ladder prompt does not fire. This is a separate fact from the one below, and
the two must not be blurred (Q3=A; quality review N.1).

Independently and still hard-binding: `Technical Environment` §9.2 — "Run both
walking-skeleton fixtures before any full-year job" — is a pipeline-enforced
sequencing rule, not AI-DLC ceremony, and it survives `skeleton: off` untouched:

- a **seven-day single-station plumbing fixture** — smoke test only, never
  scientific evidence (TC-03f);
- a **one-month all-station scientific fixture**.

The fixture-selection criterion is fixed here (Q4=A, FU-2=A), and the concrete
seven-day window has since been frozen by the student as **D-11** in
`evidence/DECISIONS.md`. Q-31 in the Technical Environment document assigns
fixture station, dates and acceptance tolerances to the **Student**, so this is a
student-owned freeze; no supervisor countersignature is required for it.

The criterion, corrected 2026-08-16 after governance finding CHAIR-02 showed the
original wording was unsatisfiable by any month:

- **Eligibility is judged on derived-artifact verification, not retrieval
  verification.** The earlier wording required a month whose *retrieval* evidence
  passes the hash-check pattern in `scripts/merge_coverage_year.py`. No month can
  satisfy that: every `sha256_manifest.json` hashes exactly four derived files
  and never the contents of `raw_isprint_cache/`, and that check verifies the
  derived artifacts rather than the retrieval itself (see `evidence.md` fact 6,
  which also records that the cache holds isprint text extractions rather than
  provider `.hdf5` bytes). A month is therefore eligible when its four declared
  artifacts verify against its `sha256_manifest.json` and its per-day coverage is
  present in all three cells. Retrieval-level verification is unavailable until
  the `raw_isprint_cache/` re-acquisition, which FU-1=B sequences **after**
  requirements-analysis.
- **Interim caveat, binding until that re-acquisition completes** (governance
  finding DATA-07). `evidence/audit_evidence_2022-FULL/` — relocated 2026-08-21 to `evidence/locked_test_restricted/audit_evidence_2022-FULL/` under D-15; the path as written was correct when this practice was affirmed — the artifact D-9
  promotes as the Phase 1 acquisition input — rests on twelve monthly runs whose
  provenance is **unverifiable in principle, not merely unverified**: no provider
  byte stream exists anywhere in the workspace, and three of the twelve months
  (2022-04, 2022-07 and **2022-12, the locked-test month**) have no
  `raw_isprint_cache/` at all. Every artifact produced before the re-acquisition
  carries that caveat and must state it wherever FULL's coverage figures are
  relied on. FULL must not be relied on at a freeze gate while its provenance
  chain points at superseded per-month hashes.
- **Re-acquisition must record provider file version suffixes** (DATA-07).
  Re-acquisition produces new bytes; it cannot retroactively prove the original
  ones. Provider version drift is already observed in this dataset (`g.002`
  versus `g.003`), so a disagreement between original and re-acquired bytes would
  be uninterpretable unless the original suffixes were recorded — and for the
  three missing months they were not. Every re-acquired file therefore records its
  full provider filename including version suffix, retrieval date, and SHA-256,
  and any mismatch against a previously recorded suffix is surfaced rather than
  silently accepted. This is an obligation on the deferred work, not an
  observation about the past omission.
- **Record-date exclusion, not directory-name exclusion.** No record whose
  observation date falls in December 2022 may enter either fixture, asserted on
  record dates rather than on the folder a file was filed under. The earlier
  "December is excluded regardless" excluded by month label only, which the
  year-blind acquisition predicate had already defeated —
  `audit_evidence_2022-01/` was carrying locked-month records at the time this
  criterion was written (governance finding TEC-09; see
  `evidence/CORRECTION_2026-08-16_acquisition_window.md`). Enforced by
  `tests/test_acquisition_window.py`.
- **Months with no `raw_isprint_cache/` are ineligible for the scientific
  fixture**: 2022-04 and 2022-07. 2022-12 is excluded as the locked month.
- **The seven-day plumbing window** needs only one station (TC-03f) and is drawn
  from the same eligible set.
- **Completeness figures are measured, not tested against a threshold.** No
  fixture completeness requirement exists to clear: §15.1 states that exact
  counts, tolerances and runtimes are measured from the fixtures and frozen,
  never invented, and the numerical coverage minimum at Vision §6.1B is a
  separate **supervisor** freeze gate governing G-P1A prepared-data acceptance,
  not fixture selection. The selected window's measured completeness becomes the
  baseline frozen into the fixture manifest. Day presence is checked against D-2's
  ≥95%-of-calendar-days rule by analogy, that being the only existing numeric
  coverage rule.
- **Frozen by D-11 (2026-08-16):** November 2022, window 2022-11-01 to 2022-11-07
  inclusive, all three cells; late autumn and pre-solstice; geomagnetically
  disturbed on provisional Dst. Measured completeness ARUC 163/168, BSHM 168/168,
  NICO 155/168, with 7/7 day presence in every cell. D-11 carries the mandatory
  limitation that this window does not reproduce December's winter-solstice
  regime or activity distribution and is not representative of the locked month,
  and the restriction that provisional Dst may characterise selection only and
  must never become a modelling input, a frozen tolerance, or a G-05 regime
  count. The one-month all-station scientific window remains open under Q-31.
- Both fixtures must pass, in order, before any full-year job — this remains a
  hard, pipeline-enforced sequencing rule, carried in `discovered-rules.md`
  § Mandated.
- Fixture assertion data belongs in `tests/fixtures/<fixture_id>/fixture_manifest.yaml`
  (identity, input hashes, expected schema, row-count ranges, support/missingness
  limits, timestamp tolerances, required outputs, expected CPU runtime range
  measured before freeze, and permitted floating-point tolerances — §15.2), not
  hardcoded inside test bodies. This is the project's actual test-data
  convention and should be followed once the fixture files exist.

## Testing Posture

This project is a governed scientific research pipeline with a locked December
2022 test set and supervisor-held gates. Testing here is categorically
different from "tests run in CI before merge" — that org default has no
mechanism to attach to (no CI stage in this scope, no git merge event until Q1
above), and the affirmed practice below replaces it rather than forcing it.

**The project's actual quality gate is §18.3, not an inherited coverage
percentage.** `Technical_Environment_and_Research_Implementation(1)(2).md`
§18.3 ("Preflight gate") states the decision criterion verbatim: *"zero
unresolved P0 fields and no failing critical test."* Its named critical set —
ten items, not the two the earlier draft named — is: target contract and DCB
sign; availability lags; IRI-free denial; split embargo; train-only transforms;
comparison-wide masks and matched windows; checkpoint restore; vector
bootstrap; release hashes; locked-test access guard. Preconditions: every P0
decision-register entry for the affected component is resolved; an automated
assertion confirms no required field in `data.yaml`, `features.yaml`,
`experiment.yaml`, or `seeds.yaml` is `TBD`; supervisor sign-off covers the
scientific hierarchy, IRI role, horizons, estimand, seeds, and locked-test
protocol. Evidence artifact: `aws_ai_dlc_preflight_report`. Binding on agents,
quoted: *"Claude Code or any equivalent agent must not implement an affected
component while its P0 decision is unresolved, and must stop and report rather
than choose a default."* This governs `code-generation` (3.5) and
`build-and-test` (3.6) directly and is affirmed as binding practice.

**The test suite is a near-term deliverable, ordered ahead of acquisition.**
`constraint-register.md` TC-06 (binding: hard): "Repository structure, pinned
environment and test suite are built before any acquisition work, inside this
initiative." TC-06 is affirmed as binding from now on (Q8=A): the repository,
pins, and test suite are built before any further acquisition; the twelve
months already acquired are treated as pre-TC-06 evidence and are re-verified
under the new suite once it exists, rather than re-acquired from scratch
(existing bytes stay; the checks that validate them are rebuilt and re-run).

**The mandated test set is 17 modules, not 2**, per §12's `tests/` tree:
`test_station_registry.py`, `test_rinex_schema.py` (Phase 2 only),
`test_dcb_sign.py` (Phase 2 only; includes the reversed-sign negative control),
`test_hourly_target.py` (Phase 2 only), `test_iri_denial.py`,
`test_phase_boundary.py`, `test_reuse_registry.py`,
`test_feature_availability.py` (asserts actual lag ≥ declared safe lag),
`test_split_embargo.py`, `test_train_only_transforms.py`,
`test_common_masks.py`, `test_models_smoke.py`, `test_checkpoint_restore.py`,
`test_bootstrap.py`, `test_locked_test_guard.py`, `test_release_hashes.py`,
`test_clean_run.py`, plus the two fixture directories
`tests/fixtures/plumbing_7day/` and `tests/fixtures/scientific_1month/`.
`test_rinex_schema.py`, `test_dcb_sign.py`, and `test_hourly_target.py` attach
to raw-processing stages Phase 1 is barred from running (§7.0); all others are
Phase 1-reachable. No `tests/` directory exists yet in the workspace.

**Acceptance vocabulary — the only one Construction gets, since `user-stories`
(2.4) is `SKIP` in this scope.** §16's Walking-Skeleton Acceptance Checklist
(WS-01 through WS-20) and §19's Technical Approval Checklist (TA-01 through
TA-32) are pass/fail, each linked to machine-readable or reviewable evidence —
"visual inspection alone is insufficient." §16 states acceptance requires all
20 WS rows `PASS`, but §16.1 assigns WS-01–WS-08 to the Phase 2 gate G-P3A, and
§7.0's Phase 1 hard prohibition bars Phase 1 from producing the raw-processing
evidence those rows require. A Phase 1 fixture run cannot satisfy "all 20"
without violating NFR-PHASE-01 — an unresolved contradiction that
`phases/inception.md` forbids carrying forward silently. Resolved at the
interview (Q6=A): **Phase 1's acceptance set is WS-09 through WS-20**, with
WS-01–WS-08 explicitly deferred to G-P3A. **Countersigned by the supervisor,
2026-08-16, recorded on the student's report.** The board's ML & Statistical
Methods seat independently verified that this reading leaves no leakage-, fold-,
mask-, or estimand-related check unenforced in Phase 1. One residual, recorded so
it is not later misread as a coverage gap: no WS row covers train-only
transforms in either subset; NFR-LEAK-01 is enforced through §18.3's gate-test
list and TA-11 instead.
Test-bearing WS rows worth naming directly: WS-10 (IRI-denial fails on
deliberate injection), WS-11 (availability lags, trailing F10.7, Dst
diagnostic-only, SSN absent), WS-12 (splits/embargo), WS-13 (matrix/tensor
window parity), WS-16 (comparison-wide masks), WS-17 (bootstrap reproduces
exactly from seed 20221201), WS-18 (locked-test guard blocks December
execution before G-05 and records access), WS-20 (clean CPU environment
reproduces both fixtures within declared tolerances). Test-bearing TA rows:
TA-07 through TA-09, TA-11 through TA-14, TA-17, TA-18, TA-22, TA-23, TA-26,
TA-27 (TA-23 is §18.3's preflight gate expressed as an approval row).

**The project's real testing methodology is a negative control paired with
every hard rule**, not positive-path testing alone: WS-10 injects an `iri_*`
field and requires the denial test to catch it; WS-04/TA-07's reversed-sign
negative control on DCB; TA-08/TA-12's grep evidence that SSN, residuals, and
GRU modules are absent from the codebase; TA-27's phase-boundary-plus-
transition-manifest-hash test. Affirmed as a mandated construction practice:
every hard rule in `discovered-rules.md` gets a test that proves the violation
is caught, not only a test that the happy path works. The operational form of
the IRI rule for Construction: the injection test suite must pass by proving
the denial mechanism rejects a deliberately injected `iri_*` field (exactly
what WS-10 and TA-07 measure) — the earlier "must fail if any `iri_*` field...
reaches ML training or inference" phrasing is the source document's wording and
is preserved as a quotation, but is not itself an implementable test spec.

**No enforced numeric coverage floor** (Q5=A). `org.md`'s per-scope coverage
table has no row matching the active scope, `research-pipeline-governed`, so
its 80% default never attached here by its own terms — this replaces the
earlier draft's weaker "does not map cleanly" framing. Separately,
`sensors/aidlc-coverage-threshold.md` does carry embedded defaults of **line 80
/ branch 70**, applied automatically whenever `build-and-test`'s emitted
`test-pro-coverage-summary.json` omits an explicit `targets` object — so
declining to set a floor is not neutral; it is a choice to accept those
embedded defaults as advisory reporting only, with no enforced floor. That
input (`test-pro-coverage-summary.json.targets`, left unset) is recorded here
per `project.md` § Way of Working ("specify the inputs a gating condition
depends on in the same stage that records the condition"). The named required
tests, plus the §16/§19 pass/fail rows above, remain the real bar; the sensor
is reporting only and never blocks.

**Locked-test discipline is an executable guard, not only a signature.** The
locked December test set is opened once for the one-shot performance
evaluation, hash-before-metrics, after G-05 is signed (Vision §5.3, gate table
row G-06; `constraint-register.md` OC-03) — but this is distinct from a
separate, **required** pre-G-05 December *coverage* audit: Vision §8.3, first
bullet, "December target values may be audited for coverage and regime counts
without inspecting model performance. This audit is required before G-05." The
earlier draft's "opened exactly once" was corrected at review (quality finding
G) because, read flatly, it forbids that mandatory pre-G-05 audit; the affirmed
practice keeps both facts distinct: the coverage audit is required and
performance-blind; the metrics evaluation is the one-shot, hash-gated event.
The guard is executable, not procedural: `tests/test_locked_test_guard.py`
(§12), evidenced by WS-18 and TA-18 ("guard test and access-log sample"), and
every access is recorded in the experiment registry via a
`locked_test_accessed = true` flag (Vision §8.3; §13.4). Any test-driven change
made to the pipeline after locked-test access is labeled exploratory (Vision
§8.3).

**Reproducibility is executable, not asserted.** §13.2's ordered clean-run
contract is the reproducibility test's actual definition: a literal command
sequence beginning `python scripts/run_walking_skeleton.py --config configs/
--fixture plumbing_7day` and `--fixture scientific_1month`, then the nine
phase-aware stage scripts, all completing on CPU. Its pass/fail form is
`test_clean_run.py` (§12), WS-20, and TA-17. Determinism is likewise tested,
not asserted: `seeds.yaml`'s fixed seeds, the three-seed element-wise mean as
the confirmatory prediction (NFR-DET-01, TC-21), `test_bootstrap.py`, WS-17,
TA-13, TA-26. The open supervisor gate that actually accepts this evidence is
**G-07 Reproducibility** (Vision §13.1 gate table, status `Blocked`, owner
Supervisor/reviewer, evidence `environment_and_cpu_preflight_report` plus the
clean-run log and matched artifacts, due before thesis submission) — named
here alongside G-05/G-06 per `project.md`'s rule to enumerate every open
supervisor gate, not only the ones on the visible critical path.

**Who runs the gate tests, and when** (Q7=D, resolving quality finding M): with
`3.7 (ci-pipeline)` `SKIP` in this scope and no git merge event to hang a check
on, `org.md`'s "tests run in CI before merge" is replaced, not inherited
unmeetably. The affirmed practice: a git pre-commit/pre-push hook runs the
critical test set on every commit once git exists (Way of Working, Q1); the
full suite runs locally before every acquisition or training run and before
every governed run (freeze gate, phase transition), with the result captured
in that run's evidence record and, where applicable, the
`aws_ai_dlc_preflight_report`. No CI service is used.

**One governance finding in this stage's lane, now carried forward**:
`governance/reviews/GOV-2026-08-15-FE-01.md` finding `GOV-F-06` — the
one-executing-leakage-test acquisition-start threshold could be misread as
narrowing the critical-test obligation. Stated here in substance per its
remediation: the one-leakage-test acquisition-start threshold does not narrow
the critical negative-path test set required at G-05 and G-07.

## Deployment

There is no staging/production split and "deploy on merge" does not apply
(Q9=C). The framework default is replaced outright with a project-specific
practice:

- **Exactly two execution platforms**: Kaggle (primary compute and the Phase 1
  acquisition/audit host) and local (development, small tests, fixture runs,
  review). No third platform is authorised (TC-03c); Google Colab and Google
  Drive are explicitly removed as governed platforms (Technical Environment
  §9.1, Vision §8.3).
- **"Deployment" means dataset and model releases.** Every immutable dataset
  release records a version, source manifest, SHA-256 hashes, schema, row
  counts, exclusions, and fold/mask identifiers, and the release is
  write-protected or stored under a new version rather than overwritten,
  gated by a mutation-protection test (`tests/test_release_hashes.py`, TA-15) —
  **Technical Environment §13.3**, correcting the earlier draft's citation
  (§6.13, cited previously, does not exist in the document; this correction was
  raised independently by the devsecops review). Models are versioned
  artifacts with a registry, not deployed services (§7.0A stage 6, §8.2).
- **Supervisor-signed freeze gates are this project's release gates.** The
  closest analogue to a production gate is the phase-transition freeze: after
  Phase 1, `phase_transition_manifest` hashes and freezes the model source,
  environment, architecture, feature manifest, target contract, splits/masks,
  grids, hyperparameters, and seeds; Phase 2 refuses to train if any protected
  hash differs (§2.2, §7.0B). **This phase-transition hash freeze is the
  project's explicit rollback-safety mechanism** — a signed, hashed freeze
  rather than a deploy/rollback command — and is enforced by a test, not only
  by a manifest: NFR-PHASE-01's evidence includes `test_phase_boundary.py`
  *and* a transition-manifest hash-diff test, required by gate G-P3C ("protected
  hashes unchanged"). Phase 2 also does not carry Phase 1 fitted weights
  forward (retrains from newly initialized weights) unless a separately
  approved, exploratory-labelled transfer-learning experiment exists, and no
  Phase 1 result may motivate a Phase 2 model or evaluation change (§7.0B) —
  both carried into `discovered-rules.md`.
- **The locked-test "release" (G-06)** is a one-time, hash-before-metrics
  event, supervisor-gated, not a CI/CD pipeline step (`constraint-register.md`
  OC-03), distinct from the required pre-G-05 coverage audit described in
  § Testing Posture above.
- **Credentials and secrets** must be supplied through platform secret stores
  or environment configuration excluded from version control; none may appear
  in a notebook, configuration snapshot, log, registry note, or committed
  script (Technical Environment §10). This is affirmed as-is, with the
  correction that it is not yet satisfied in the workspace today — see
  `evidence.md` for the current NFR-SEC-01 breaches this rule is meant to
  prevent, and § Way of Working above for the `.gitignore` precondition.
- **Registry integrity is part of "deployment" here**: registry writes must be
  atomic or append-safe; failed and aborted runs remain visible with status and
  reason; silent reruns are prohibited (NFR-AUD-01, §13.4, gated by TA-10).

## Code Style

No existing convention to affirm — this is a choice being made, not an
observation being ratified. Direct comparison of the two Python files present,
`scripts/audit_ec1_drivers.py` and `scripts/merge_coverage_year.py`, shows they
diverge on four axes:

| Axis | `audit_ec1_drivers.py` | `merge_coverage_year.py` |
|---|---|---|
| Typing | `from __future__ import annotations`, PEP 604 hints (`dict[dt.date, list[dict]]`) | none |
| Paths | `pathlib.Path` throughout | `os.path.join` throughout |
| Strings | double quotes, f-strings | single quotes, `%`-formatting |
| Fatal exit | `raise SystemExit(...)` / `sys.exit(main())` | `sys.exit('message')`, bare `main()` call |

What the two files genuinely share: a module-level docstring stating purpose,
inputs, and re-run behaviour, and `snake_case` naming throughout — both
affirmed as mandated conventions (Q12=C) rather than inferred from a
non-existent shared style.

Affirmed choices (Q10=A, Q11=B):

- **`ruff`, for both linting and formatting**, configured in the mandated
  `pyproject.toml`, adopted now — before the nine stage scripts are written —
  rather than deferred. `pyproject.toml` is not merely absent; §12's repository
  tree mandates it at the repository root, and TA-01 gates the repository
  skeleton's acceptance on it existing, alongside four configs, six `src/`
  packages, nine phase-aware stage scripts, five notebooks, `tests/`, and
  `artifacts/`. TC-06 places this scaffold before any acquisition work, inside
  this initiative.
- **Migration obligation on the two existing scripts and the one notebook**:
  when the scaffold is built, all three move onto the §12 structure — the
  scripts are rewritten to take `--config configs/` (and `--phase 1|2` where
  applicable) and gain their numbered `NN_verb_noun.py` position in
  `scripts/`; the notebook's frozen scientific values move out of code and
  into config. This is recorded as a migration obligation now, not left open.
  Specifically: `notebooks/madrigal_phase1_coverage_audit.ipynb` cell 4 holds
  the ARUC/BSHM/NICO station coordinates as an inline literal and a
  coordinate-to-cell rule as an inline function, both self-labelled
  "PROVISIONAL"/"DEFAULT convention adopted here" in the notebook's own
  comments. Both are §18.2 forbidden-choice items (station coordinates:
  Student; cell-selection rule: Student + Supervisor) and TC-03e scientific
  constants that must not live in source or a notebook. Per the interview
  (Q11=B), **the current inline constants are frozen as a D-number decision
  first**, so the migration itself cannot silently change a scientific value —
  only after that freeze do the values move into `configs/data.yaml` and the
  cell-bounds logic into `src/data/registry.py`, validated against the
  official IGS site logs before being treated as final.
- The triplicated SHA-256 hashing helper (`sha256` in `audit_ec1_drivers.py`,
  `sha256_of_file` in `merge_coverage_year.py`, and a third copy inside the
  notebook) consolidates into `src/data/release.py` at scaffold time — one of
  the six mandated `src/` packages (`data`, `gnss`, `external`, `features`,
  `models`, `evaluation`; there is no seventh `utils` package to place it in
  instead), and the notebook's copy is removed rather than left as the sole
  copy of that logic, per §14's rule that a notebook must not hold the only
  copy of parsing, calibration, feature, split, training, evaluation, or
  bootstrap logic.
- Naming and CLI convention, fixed by §12/§13.2, not left for `code-generation`
  to reinvent: stage scripts are `NN_verb_noun.py` with a two-digit ordinal
  prefix; every stage script takes `--config configs/`, phase-aware stages
  additionally take `--phase 1|2`; the walking-skeleton orchestrator takes
  `--fixture plumbing_7day` / `--fixture scientific_1month`; test files are
  `test_<subject>.py`; notebooks are `NN_topic.ipynb`.
- The observed two-tier error-handling posture is affirmed as a mandated
  practice: integrity violations (hash mismatch, missing manifest, violated
  invariant) terminate the run with a message naming the file and the
  violated expectation (Q12=B); completeness shortfalls (a missing month, a
  partial retrieval) are non-fatal but must be recorded as machine-readable
  fields in the output manifest — never console text only — with the artifact
  explicitly marked derived and/or partial. `audit_ec1_drivers.py:184`
  returning `0` regardless of missing months is noted as a gap against this
  practice, to be fixed when the script migrates.
- Reusable logic belongs in `src/`; the nine phase-aware stage scripts
  orchestrate it; **notebooks do not own production logic** (§7, quoted
  exactly, since §14's notebook rule depends on this separation being read as
  written, not softened).
- Exactly four governed config files, under `configs/` — `data.yaml`,
  `features.yaml`, `experiment.yaml`, `seeds.yaml` — with no scientific
  constant hidden in source or a notebook (§12; TC-03e; Q12=D). Every stage
  script receives them as `--config configs/`; each run snapshots and hashes
  all four (§13.1); before an affected component is implemented, an automated
  preflight asserts no required field in any of the four is `TBD` (§18.3).
- `src/external/iri.py` and `src/external/gim.py` are never imported, directly
  or transitively, by any module under `src/features/` or `src/models/` — the
  only permitted importers are `scripts/04_build_external_products.py` and
  `src/evaluation/` (§12 import-boundary rule; TA-07; Q12=A). This is a
  module-graph constraint distinct from the data-flow IRI rule already in
  `discovered-rules.md`, and is carried there as its own entry.
- Copied or materially adapted third-party code lives behind a
  project-owned adapter with a `src/data/reuse_registry.py` record — never
  pasted into a notebook (§10.1; NFR-LIC-01; `tests/test_reuse_registry.py`;
  Q12=E), before the code is used and before gate G-P2. The AGPLv3
  Global-TEC-forecasting repository is the one approved direct-copy source
  today; whether its repository-distribution obligations permit that copying
  is a governance dependency this project does not resolve on its own — see
  `evidence.md`.

**Python, not TypeScript, is the project's implementation language.**
`aidlc-state.md` records `Languages: TypeScript`, which traces to the AI-DLC
framework's own tooling (`.claude/tools/*.ts`, `.claude/hooks/*.ts`,
`sensors/aidlc-sensor-*.ts`) — infrastructure for running the workflow, not a
project deliverable. The actual research code — `scripts/audit_ec1_drivers.py`,
`scripts/merge_coverage_year.py`, and `notebooks/madrigal_phase1_coverage_audit.ipynb`
(kernelspec `python3`, `language_info.version` 3.11) — is Python 3.11, the
exact governed pin (§8.1, TC-03d). This is not merely an observation: §8.3
makes Python-only a hard normative rule — R, Julia, and MATLAB are explicitly
"Prohibited" for the pipeline, and PyTorch is prohibited to avoid a second
deep-learning stack. `aidlc-state.md`'s `Languages` field should read
`Python 3.11`, with the TypeScript tooling recorded as workflow infrastructure,
not a project language — this correction is recorded here rather than silently
applied, since editing `aidlc-state.md` is outside this stage's produced
artifacts.

## Forbidden

<!-- Team-specific forbidden patterns -->

## Mandated

<!-- Team-specific mandates -->

## Corrections

<!-- Self-learning loop appends here. -->
- ALWAYS read the §12 `tests/` mandated set as **21** modules, not 17. § Testing Posture above states "The mandated test set is 17 modules, not 2" and enumerates 17; the figure is superseded. Derived 2026-08-28 by enumerating §12's tree and printed before assertion, then set-differenced against the affirmed 17 as **+4 / −0**. The four beyond the enumerated 17 are named in `construction/regimes-diagnostics-reporting/functional-design/business-rules.md` R-132's printed derivation. This stale figure is the root cause of governance finding `GOV-2026-08-28-FD-01` Recommendation 27, and it also propagated into `RES-02` of `inception/delivery-planning/external-dependency-map.md`, which tracked it as 19 — itself wrong, corrected in place 2026-08-28 on owner approval. Corrected under the §13 learnings ritual, the only sanctioned write path into a memory file, on the project decision owner's authorisation at the `functional-design` gate (Recommendation 33). The superseded 17 is left standing in § Testing Posture rather than overwritten, because this path appends and never replaces; § Testing Posture's own rewrite is owed to the next practices-affirmation gate. (learned 2026-08-28) <!-- cid:functional-design:fd-team-01-test-module-count -->
- ALWAYS record this project's implementation language as **Python 3.11**, never TypeScript. § Code Style above already states this correction and notes it was recorded rather than applied; it is restated here because the stale value did not stay inert. It propagated out of `aidlc-state.md` into the dispatch brief of the `GOV-2026-08-28-FD-01` governance board itself (Recommendation 33), which is the concrete harm that makes this a correction rather than a tidy-up. `aidlc-state.md`'s `Languages` field was corrected by hand on 2026-08-22 under `GOV-2026-08-21-UG-01` and now reads `Python 3.11`. TypeScript remains the language of the AI-DLC framework's own tooling (`.claude/tools/*.ts`, `.claude/hooks/*.ts`) — workflow infrastructure, never a project deliverable. TE §8.3 makes Python-only a hard normative rule: R, Julia and MATLAB are prohibited for the pipeline, and PyTorch is prohibited to avoid a second deep-learning stack. (learned 2026-08-28) <!-- cid:functional-design:fd-team-02-languages-python -->
- ALWAYS state Phase 1's walking-skeleton acceptance set as **WS-01 plus WS-09 through WS-20**, not WS-09 through WS-20 alone. § Testing Posture above defines it as "WS-09 through WS-20" with WS-01–WS-08 deferred to G-P3A; that is right for WS-02 through WS-08 and wrong for **WS-01**, which `unit-of-work-story-map.md` carries as an in-Phase-1 row under FR-WS-4 and which `fixtures-and-reproducibility` records as TA-09's bounded scope ("WS-01 and WS-09…WS-20"). The supervisor countersignature of 2026-08-16 covered the WS-09–WS-20 reading, so this correction narrows a deferral rather than widening a claim: one fewer row is deferred to G-P3A. Recorded as `RES-02`'s third tracked item. (learned 2026-08-28) <!-- cid:functional-design:fd-team-03-ws01-exception -->
- ALWAYS read TC-06's "test suite" as the full §12 mandated set, not as the subset a given initiative happens to need. § Testing Posture above affirms TC-06 as binding — repository structure, pinned environment and test suite built before any acquisition work — and the narrower reading was flagged as owed to this gate by `RES-02`. The narrow reading would let an initiative declare TC-06 satisfied while most of the mandated modules remain unwritten, which is the failure `GOV-2026-08-15-FE-01` finding `GOV-F-06` already warned of in its own terms: a one-executing-leakage-test acquisition-start threshold does not narrow the critical negative-path test set required at G-05 and G-07. The same logic governs TC-06. (learned 2026-08-28) <!-- cid:functional-design:fd-team-04-tc06-test-suite -->
