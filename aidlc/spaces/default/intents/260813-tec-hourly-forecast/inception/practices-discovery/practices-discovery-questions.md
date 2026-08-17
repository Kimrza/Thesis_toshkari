# Practices Discovery — Questions

Stage 2.2 (practices-discovery), intent `260813-tec-hourly-forecast`.
Depth: Comprehensive. These questions settle the five sections that get promoted
into `aidlc/spaces/default/memory/team.md`, plus the hard constraints promoted
into `project.md`.

Answer each by filling the `[Answer]:` tag with the option letter.

---

## Q1 — Version control

The lead draft treated "should this project use git at all?" as open. The
reviewers closed it: `Technical_Environment_and_Research_Implementation(1)(2).md`
§13.1 and §13.4 require a code commit recorded per run, and TA-01's evidence
column is "Repository tree and code commit". So version control is required.
What remains open is how you work inside it, as a single author with a
supervisor who signs at named gates rather than reviewing pull requests.

- A. Initialize git now, before any more acquisition work, and work on `main` directly with one commit per completed stage script or decision. No branches, no PRs — the supervisor signs gates, not merges.
- B. Initialize git now, and use short-lived feature branches squash-merged to `main`, matching the framework's default way of working.
- C. Initialize git now, work on `main` directly, and additionally tag each freeze gate (G-05, G-06, phase transition) so the frozen state is recoverable by tag.
- D. Defer initializing git until Construction begins, accepting that runs before then cannot record the commit hash §13.1 requires.
- X. Other (please specify)

[Answer]:C

---

## Q2 — Where decisions get recorded once git exists

Today `evidence/DECISIONS.md` (D-1 through D-10, each signed) is this project's
unit of auditable change. Once commits exist, there are two records of "what
changed and why".

- A. `evidence/DECISIONS.md` stays authoritative for scientific and governance decisions; commits record code changes only. A decision is not real until it has a D-number.
- B. Commits become authoritative; `DECISIONS.md` becomes a summary index pointing at commit hashes.
- C. Both, with a hard rule: every commit that changes a scientific constant, config value, or governed artifact must cite its D-number in the commit message.
- X. Other (please specify)

[Answer]:C

---

## Q3 — Build a thin end-to-end slice first?

A walking skeleton is a minimal version that runs the whole way through, built
first to prove the pieces connect before the real features go in. Your AI-DLC
scope file (`.claude/scopes/aidlc-research-pipeline-governed.md`) declares
`skeleton: off`, so the framework will not add a skeleton ceremony. Separately
and independently, `Technical Environment` §9.2 already binds you: "Run both
walking-skeleton fixtures before any full-year job" — a seven-day single-station
plumbing fixture (smoke test only, never scientific evidence, TC-03f) and a
one-month all-station scientific fixture.

- A. Confirm both: no AI-DLC skeleton ceremony, and §9.2's two fixtures remain a hard sequencing rule enforced by the pipeline itself before any full-year run.
- B. Confirm §9.2's fixtures, and additionally turn the AI-DLC skeleton ceremony on so the first build is gated as a skeleton Bolt.
- C. Treat the seven-day plumbing fixture as optional once the one-month scientific fixture passes.
- X. Other (please specify)

[Answer]:A

---

## Q4 — When the fixture windows get fixed

Both fixture windows are recorded as `TBD — freeze gate`, student-owned under
Q-31. The one-month all-station fixture cannot be frozen before three-station
coverage exists. The framework's own rule (project.md) is that a gating
condition must have its inputs specified in the same stage that records the
condition — so leaving both as TBD makes the condition uncheckable.

- A. Fix both windows now, in this stage, and record them as a D-number decision in `evidence/DECISIONS.md`.
- B. Fix the seven-day plumbing window now (it needs only one station); record the one-month window as blocked on the three-station coverage audit, with that audit named as its explicit input.
- C. Leave both TBD and revisit at requirements-analysis, accepting the condition is uncheckable until then.
- X. Other (please specify)

[Answer]:A

---

## Q5 — Numeric test coverage

The draft said no coverage threshold is stated anywhere. That was wrong:
`sensors/aidlc-coverage-threshold.md` carries embedded defaults of **line 80 /
branch 70**, applied whenever the emitted JSON omits explicit `targets`. It
reports, it never blocks. Separately, `org.md`'s per-scope coverage table has no
row for the `research-pipeline-governed` scope, so the framework's 80% figure
never attached to this project by default.

- A. Accept the sensor defaults (line 80 / branch 70) as advisory reporting, and add no enforced floor. The named mandatory tests remain the real bar.
- B. Set explicit `targets` lower than the defaults for Phase 1 (the pipeline is mostly I/O and audit code), and raise them for Phase 2 modelling code.
- C. Set an enforced coverage floor that fails the preflight gate, and name the number.
- D. Disable the coverage sensor for this project; coverage percentage is the wrong measure for a governed research pipeline.
- X. Other (please specify)

[Answer]:A

---

## Q6 — The §16 contradiction (which checks Phase 1 must pass)

`Technical Environment` §16 says every one of WS-01 through WS-20 must PASS. But
§16.1 assigns WS-01–WS-08 to the Phase 2 gate G-P3A, and §7.0 bars Phase 1 from
importing the raw-processing path that would produce that evidence. Phase 1
therefore cannot satisfy "all 20" without violating NFR-PHASE-01. Framework
rules forbid carrying an unresolved contradiction forward.

- A. Record that Phase 1's acceptance set is WS-09 through WS-20 only, with WS-01–WS-08 explicitly deferred to G-P3A, and take that reading to the supervisor for countersignature.
- B. Record it as a defect in the governing document and raise it with the supervisor before answering it here; do not encode either reading as a practice yet.
- C. Read §16 as aspirational and §16.1 as operative, and encode WS-09–WS-20 without escalating.
- X. Other (please specify)

[Answer]:A

---

## Q7 — Who runs the gate tests, and when

`3.7 ci-pipeline` is SKIP in this scope, there is no CI service, and (until Q1)
no merge event to hang a check on. The framework's "tests run in CI before
merge" rule has nothing to attach to, so it would carry forward unmeetable.

- A. The full test suite runs locally before every acquisition or training run, and its result is captured in that run's evidence record. No CI service.
- B. Tests run locally before each freeze gate (G-05, G-06, phase transition) only; ad-hoc during development.
- C. A git pre-commit or pre-push hook runs the critical test set on every commit, once git exists.
- D. Both A and C: gate tests on every commit, full suite before every governed run.
- X. Other (please specify)

[Answer]:D

---

## Q8 — Test suite before acquisition (TC-06)

`constraint-register.md` TC-06 is a hard constraint: the repository, the pinned
environment, and the **test suite** are built before any acquisition work,
inside this initiative. Acquisition work has already happened (twelve monthly
manifests exist under `evidence/`). No `tests/` directory exists yet.

- A. Affirm TC-06 as binding from now on: build the repo, pins, and test suite before any further acquisition, and treat the existing twelve months as a pre-TC-06 artifact to be re-verified once the suite exists.
- B. Affirm TC-06 and additionally re-run the existing acquisition under the new suite before any of it is used downstream.
- C. Treat TC-06 as satisfied in spirit by the existing audit scripts and evidence records; build the formal suite alongside Construction.
- X. Other (please specify)

[Answer]:A

---

## Q9 — Deployment section

There is no staging/production split here. "Deployment" means immutable dataset
releases, a model registry, and hash-frozen phase transitions across exactly two
platforms (Kaggle and local). The framework's "deploy on merge to staging,
manual gate to production" default has no natural mapping.

- A. Replace the framework's deployment default entirely with a project-specific practice: two platforms, immutable hashed dataset releases, versioned model registry, supervisor-signed freeze gates. Nothing about staging or production.
- B. Keep the framework default as a placeholder for a possible future service, and add the project-specific practice alongside it.
- C. Replace it as in A, and additionally record the phase-transition hash freeze as the project's explicit rollback-safety mechanism.
- X. Other (please specify)

[Answer]:C

---

## Q10 — Linter and formatter

`Technical Environment` §12 mandates a `pyproject.toml`, so the file is not
optional — only the tool choice inside it is open. No linter or formatter config
exists in the workspace today, and the two existing scripts diverge on four
axes (typing style, `pathlib` vs `os.path`, quoting, `raise SystemExit` vs
`sys.exit`). There is no existing convention to affirm.

- A. `ruff` for both linting and formatting, configured in `pyproject.toml`, adopted now before the stage scripts are written.
- B. `ruff` for linting plus `black` for formatting.
- C. `ruff` only, and defer the formatter decision until `src/` exists.
- D. No linter or formatter; rely on review and the mandated tests.
- X. Other (please specify)

[Answer]:A
---

## Q11 — The two existing scripts and the notebook

Neither `scripts/audit_ec1_drivers.py` nor `scripts/merge_coverage_year.py`
appears in §12's exhaustive file tree, and neither takes `--config configs/`.
The notebook holds the ARUC/BSHM/NICO coordinates as inline literals and a
self-labelled "DEFAULT convention adopted here" cell-bounds rule — both §18.2
forbidden-choice items and TC-03e scientific constants that belong in the four
governed config files.

- A. Migrate all three onto the §12 structure when the scaffold is built: constants move into `configs/`, logic moves into `src/`, and the scripts are rewritten to take `--config`. Record it as a migration obligation now.
- B. Same as A, and additionally freeze the current inline constants as a D-number decision first, so the migration cannot silently change a scientific value.
- C. Leave the existing three as historical pre-scaffold artifacts; the §12 structure applies only to new code.
- X. Other (please specify)

[Answer]:B

---

## Q12 — Code patterns to make mandatory

Candidate rules the reviewers surfaced, drawn from the governing documents and
observed code. Select all you want promoted as hard `ALWAYS`/`NEVER` rules
(select all that apply):

- A. NEVER let `src/features/` or `src/models/` import `src/external/iri.py` or `src/external/gim.py` (the import boundary behind NFR-IRI-01).
- B. ALWAYS surface an integrity failure with an explicit exit and a human-readable message; never continue silently past a failed hash check.
- C. ALWAYS give every script and module a docstring stating purpose, inputs, and re-run behaviour.
- D. NEVER hide a scientific constant in source or a notebook; every one lives in `data.yaml`, `features.yaml`, `experiment.yaml`, or `seeds.yaml`.
- E. ALWAYS record reused third-party source in the §10.1 reuse register with its licence, before the code is used (NFR-LIC-01, gates G-P2).
- X. Other (please specify)

[Answer]:X, Do all A, B, C, D, E.

---

## Q13 — Identity in request manifests (unresolved conflict)

A personal email is hardcoded at Cell 2 of
`notebooks/madrigal_phase1_coverage_audit.ipynb`, and `user_fullname` /
`user_affiliation` are persisted into all 13
`evidence/audit_evidence_2022-*/request_manifest.json` files. CEDAR's
rules-of-the-road require a real identity per request; NFR-SEC-01 forbids
storing personal data. Both cannot hold as written.

- A. Keep supplying real identity to CEDAR at request time from an environment variable, and stop persisting it: scrub the three fields from existing manifests and never write them again.
- B. Keep the fields in the manifests as provenance evidence (they prove who made the request), and record an explicit NFR-SEC-01 carve-out for CEDAR identity fields, countersigned by the supervisor.
- C. Replace the persisted values with a stable pseudonymous requester ID, mapped to the real identity in a single file excluded from version control.
- X. Other (please specify)

[Answer]:A

---

## Q14 — Integrity gaps already visible in the evidence

Three measured gaps: `madrigalWeb_version` is `"unknown"` in all twelve monthly
manifests (against §10's pinning requirement); `raw_isprint_cache/` is unhashed
in every month and absent entirely from 2022-04, 2022-07 and 2022-12 — the
locked-test month; and `merge_coverage_year.py:182-208` copies eight provenance
fields (including `stations` and `coordinate_to_cell_convention`) from the first
month's manifest under a comment asserting they are identical, with nothing
checking that.

- A. Treat all three as blocking remediation obligations to close before requirements-analysis, and record them as such.
- B. Close the version pin and the copied-field assertion now; treat the missing `raw_isprint_cache/` months as a separate re-acquisition decision needing its own D-number.
- C. Record all three as known gaps in `evidence.md` and schedule remediation into Construction.
- X. Other (please specify)

[Answer]:A

---

## Q15 — The document's own script/notebook counts

`Technical Environment` §1.3 says "Scripts 18 → 7 / Notebooks 11 → 4", while
§7, §12, §14 and §19 all describe nine stage scripts and five notebooks. TA-01
approves against the latter. §1.1 and §18.2 reserve resolving this to you and
your supervisor.

- A. Treat §12/§14/§19 (nine scripts, five notebooks) as operative, record §1.3 as a stale change-log row, and raise it for supervisor countersignature.
- B. Raise it with the supervisor before encoding either reading; leave the practice silent on counts until then.
- C. Treat §1.3 as operative and reconcile the other sections down to it.
- X. Other (please specify)

[Answer]:A

---

# Follow-up questions

Raised by cross-checking the answers above. Two answer pairs interact in a way
the individual questions did not surface.

---

## FU-1 — Ordering: test suite, re-acquisition, and requirements-analysis

Q8 = A: no further acquisition until the repository, pinned environment and test
suite exist (TC-06). Q14 = A: all three integrity gaps are blocking obligations
closed before requirements-analysis — and one of them (`raw_isprint_cache/`
absent for 2022-04, 2022-07, 2022-12) can only be closed by re-acquiring those
months. Chained, that requires building the test suite and re-acquiring three
months **before** requirements-analysis runs, i.e. building the suite before the
stage that specifies what it must verify.

- A. Accept the ordering: build the repository, pins and a minimal test suite now (covering the integrity and phase-boundary checks only), re-acquire the three months, then run requirements-analysis. The suite grows again afterwards against the specified requirements.
- B. Narrow Q14: keep the version pin and the copied-field assertion as blocking-before-requirements-analysis, and move the `raw_isprint_cache/` re-acquisition to after requirements-analysis, so no acquisition precedes the requirements that govern it.
- C. Narrow Q8 instead: allow the three-month re-acquisition as an explicit TC-06 exception (it re-fetches already-audited months rather than acquiring new data), and keep the full suite scheduled after requirements-analysis.
- D. Keep both answers as given and run requirements-analysis first anyway, treating "before requirements-analysis" in Q14 as "before Construction".
- X. Other (please specify)

[Answer]:B

---

## FU-2 — Fixing the one-month fixture window now

Q4 = A: fix both fixture windows in this stage and record them as a D-number.
But the one-month all-station window's stated precondition is that three-station
coverage exists, and Q14 = A confirms three months have no cached raw data at
all — including 2022-12, the locked-test month, which is excluded from fixture
use regardless.

- A. Fix both windows now from a month where all three stations already have verified coverage, and record the selection criterion in the D-number entry so the choice is reproducible.
- B. Fix the seven-day plumbing window now; record the one-month window as pending, with the three-station coverage audit named as its explicit input and a deadline of the next stage.
- C. Fix both now provisionally, and re-confirm the one-month window after the re-acquisition in FU-1 completes.
- X. Other (please specify)

[Answer]:A

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
