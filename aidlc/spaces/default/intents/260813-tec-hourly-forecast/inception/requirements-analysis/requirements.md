# Requirements — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.3 (requirements-analysis), intent `260813-tec-hourly-forecast`.
Depth: Comprehensive. Scope: `research-pipeline-governed`.

**Revision record.** Revised 2026-08-21 under the student's approved
dispositions against governance report `GOV-2026-08-21-RA-01` (verdict `FAIL`,
adaptive board escalated to full board). Applied: Rec 2 (full open-gate
enumeration), Rec 3 (closed ML input space, target-derived lag contract),
Rec 4 (five-ablation registry), Rec 6 (registry column contract), Rec 7
(applicable TA rows, TA-09 reading), Rec 8 (B-01/C-01 inventory), Rec 9 (NFR
count), Rec 11 (plots split from breakdowns), Rec 12 (WS-01 exception, interim),
Rec 13 (December regime audit and demotion ordering), Rec 14 (18 test modules),
Rec 15 (ID drift), Rec 16 (evaluation-code freeze). Rec 10 applied as fallback B (board-finding citations re-sourced to the persisted
rule text — see § Sources **[board]**). Rec 1 (D-144), Rec 5 (D-2) and Rec 12
(WS-01) **approved by the project owner** under the recorded student/supervisor
authority equivalence; recorded in
`governance/CHANGE_RECORD_2026-08-21_D-144.md`.

**Second revision, same day — GOV-2026-08-20-RA-01.** A prior full-board review of
this artifact (20 blocking finding IDs) was discovered untracked in a git
worktree, having never reached the main tree. Its findings were independently
reverified and its twelve open recommendations approved. Applied: Rec 17
(`.gitattributes` marking `evidence/**`, `artifacts/**`, `tests/fixtures/**`
`-text`, working tree denormalized, `tests/test_release_hashes.py` added — all
13 manifests / 52 artifacts and all 13 EC-1 hashes now verify on this checkout);
Rec 18 (FR-P1-02-6, restricted-path custody); Rec 19 (access-log ordering in
FR-P1-02-3 and FR-P1-05-12, plus two retrospective rows in the registry);
Rec 20 (`test_acquisition_window.py` custody collector widened to walk
`evidence/` recursively — **expected to fail until the December copies are
relocated**); Rec 21 option C, first half (FR-P1-03-1's false freeze corrected;
open question 2 corrected on D-1); Rec 22 (FR-P1-03-5 target field set, § Known
defects row 10 with **no reading adopted**); Rec 23 (FR-P1-04-14 §8.7 selection
and refit, Final-refit partition); Rec 24 (FR-P1-04-15 benchmark validation,
FR-P1-05-19 plasmaspheric disclosure); Rec 25 (FR-P1-06-1 fourteen protected
hashes); Rec 26 (FR-P1-03-2 both prohibition limbs); Rec 27 (`REQ-CLAIM-01`
adopted, prohibited classes enumerated, two items moved from Future to
Out-of-claim); Rec 28 (REQ-ENG-10/11, §12 tree enumeration completed, FR-WS-6
citation corrected).

Three supervisor-owned values frozen the same day: **D-12** (≥90% usable hourly
coverage per station per month, hard gate, with D-2's day rule), **D-13** (H4 and
SRQ-5 confirmatory only with ≥3 independent §9.3 storm events), **D-14**
(scientific fixture window = March 2022, all three cells). Change record:
`governance/CHANGE_RECORD_2026-08-21_freezes.md`.

**Third revision, same day — remediation completed.** The relocation and the
decisions the second revision left pending were carried out under owner approval.

- **D-15** relocated every December-bearing artifact under
  `evidence/locked_test_restricted/` — 21 files, all verified byte-identical, old
  paths gone. FR-P1-02-6 now **passes** and is retained as a regression guard.
  `scripts/merge_coverage_year.py` and `tests/test_acquisition_window.py` resolve
  both roots and refuse to run when a month appears in both.
- **D-16** froze the hourly aggregation statistic as the **median**, after the
  false "already frozen" claim in FR-P1-03-1 was corrected first — Rec 21's two
  stages, in order. Zenith-weighted aggregation is declared as a sensitivity and
  **deferred as not computable**: the audited product carries `ut1_unix`,
  `gdlat`, `glon`, `tec`, `dtec` and nothing else. Nothing is substituted.
- **D-17** froze the Phase 1 target-row contract from that audited schema, which
  **dissolves** § Known defects row 10 rather than adjudicating it:
  `valid_satellite_count` is not computable in Phase 1, so no reading of the
  Vision §6.6 / TE §7.0 conflict had to be adopted. Two further facts recorded
  there: TE §6.1's provisional `valid_observation_count >= 20` is unsatisfiable on
  a ≤12-sample cell-hour, and D-4's four driver columns were never actually
  requested.
- The **D-1 addendum** states the cell rule as already frozen —
  `cell = (floor(lat), floor(lon))`, half-open \([floor, floor+1)\) — and closes
  its TE §18.2 countersignature under the recorded delegation, forging nothing.
- `tests/test_phase_boundary.py` created with both §7.0 limbs;
  `tests/test_release_hashes.py` added; `.gitattributes` committed and the working
  tree denormalized, so 60/60 manifest artifacts and 13/13 EC-1 hashes verify.
- Vision **v4.3** and TE **v3.3** issued; the citation sweep is deliberately
  partial, since pre-2026-08-21 artifacts cited v4.2/v3.2 correctly when written.
- `GOV-2026-08-20-RA-01` filed verbatim under `governance/reviews/`.

**Fourth revision, 2026-08-21 — `GOV-2026-08-20-RA-01` non-blocking audit.** A
resume-time verification pass found this revision record wrong about its own
document, and audited all 43 of that board's non-blocking findings (30 MAJOR, 13
MINOR/NOTE) one by one against the requirement rows rather than against this
record. Result: **7 fully closed, 9 partially closed, 27 open**. Two of those verdicts are corrections to the audit's own first pass: `TEC-15` (Vision §6.2's affirmative characterisation) and `BENCH-05` (the compute envelope and the four `binding: hard` TC-03 rows) were both initially read as open on a keyword search and are in fact **already present** — the first in § Out of scope C, wrapped across a line break, the second inside REQ-ENG-11 rather than in § Constraints. Both are recorded as closed, and the near-miss is why every other verdict was checked by reading the row rather than by grepping for a phrase. The previous
blanket claim that the "MAJOR and MINOR sets are unworked" was wrong in both
directions and is withdrawn. Owner-approved disposition, recorded in
`governance/CHANGE_RECORD_2026-08-21_RA_audit.md`: fix all 38 open-or-partial
findings here, in four groups ordered by consequence — false assurance (8), an open leakage or integrity path (7), an invisible or unfrozen scientific choice (5), and accuracy and completeness (16, after the two reclassifications above). Two items are deferred and recorded rather
than dropped: `VAL-11`'s file custody for `.dst_summary.json` (a workspace
action, not a requirement; Student, before G-05) and `DATA-14`'s thesis-appendix
and notice-location mechanics (G-P2, restated at stage 3.2).

Three defects neither board raised were found in the same pass and are corrected
here. (a) The four support thresholds are **frozen as D-19**, not `TBD`; the
`TEC-05` and `ML-01` residues are **closed**; and a real pytest run **has**
occurred — **224 passed, 2 skipped** on CPython 3.11.9, the governed pin,
re-executed at resume and matching commit `13d5796`. The paragraph this replaces
asserted the opposite of all four. (b) **D-18** — the year re-merge that
discharges the `PROVENANCE_NOTICE` obligation `DATA-08` raised and moves FULL's
`source_runs` digests onto current per-month hashes — was absent from this
record entirely. (c) FR-P1-03-5 claimed the D-19 values are "recorded in
`data.yaml` … so the zero-TBD preflight now passes"; **no `configs/data.yaml`
exists** — there is no `configs/`, `src/` or `pyproject.toml`, the REQ-ENG
scaffold being unbuilt — so that row now names `evidence/DECISIONS.md` as where
D-19 lives and the scaffold as when it reaches config.

**Fifth revision, 2026-08-21 — `GOV-2026-08-21-RA-02`.** The fourth revision was put to a full board, which returned `FAIL` on three blocking findings and is filed at `governance/reviews/GOV-2026-08-21-RA-02.md`. All eight actionable findings are remediated here; the ninth, `BENCH-12`, is a `NOTE` recorded below rather than a change. **Two of the three blockers were defects in the fourth revision's own remediation**, which is worth stating plainly rather than absorbing quietly:

- **`ML-14`** — `ML-05` was recorded as *closed* in this document's disposition table and in `CR-2026-08-21-RA-AUDIT`, and was not. The criteria said the grid and seed content was "compared against configuration" while naming none of it; the artifact contained **zero occurrences** of `ridge 6`, `RF 18`, `LSTM 16`, `seed 42`, `{1337, 2024, 7}`, `dropout 0.2`, `patience 10` or `1e-4`. A finding marked closed is not re-reviewed, so a false closure outlives an open one. The frozen values are now named in FR-P1-05-2 and FR-P1-05-5 — restating what D-121 and D-122 approved, changing nothing.
- **`IMPL-15`** — the new REQ-ENG-12 applied TE §14's analysis-notebook rules to all five notebooks, contradicting D-144's express approval of `00_acquire_phase1_vtec.ipynb` as a *"narrowly approved self-contained acquisition/audit interface"* with a **different** six-item declaration set. Split into REQ-ENG-12 (the four analysis/review notebooks) and REQ-ENG-13 (the acquisition notebook), with `IMPL-16`'s misquote — "behavioural" for the authority's "behavioral" — and its over-broad equivalence scope corrected in the same pass.

Also applied: `DATA-21` (FR-P1-04-11's count restated as §13.3's ten rows and fourteen fields, after an earlier revision carried "thirteen" from a finding's text without counting the table, and `source_files` restored to a cross-reference rather than a reduction to "SHA-256 hashes"); `DATA-23` (FR-P1-02-1 split, FR-P1-02-7 created, so no row holds two verdicts); `DATA-24` (FR-P1-01-7's `features.yaml` dependency stated); `CHAIR-04` (§ Known defects rows reordered 1–13, having run 1,2,3,4,5,6,10,8,9,7,11,12,13 while three requirements cite them by number).

**`CHAIR-03` — a disclosure about that board, not a change to this document.** `GOV-2026-08-21-RA-02`'s Chair was **conflicted**: the agent that authored the fourth revision reviewed it, in the same session, with no independent seat between authorship and validation. `review-board.md` bars exactly that — *"Anyone who … materially changed the artifact … must not chair its final validation decision"* — and provides the remedy used here: the human is the decision owner and the AI board is advisory. So `GOV-2026-08-21-RA-02`'s `PASS` rows are weaker evidence than the same rows in `GOV-2026-08-20-RA-01`, which reviewed an artifact it had not written, and the two must not be read as interchangeable. A future revision of this artifact should be reviewed by a board that did not author it.

**`BENCH-12`, recorded as a `NOTE`.** Vision line 472 requires that if the coverage audit shows GPS-only support inadequate against §6.6's thresholds, **GPS+Galileo must be evaluated before full-year processing and the change recorded**, evidenced by `constellation_observable_cadence_report`. Neither appears in this document. That is correct rather than missing: Vision line 289 scopes GPS-only L1/L2 at 30 s to **Phase 2**, which §7.0 bars Phase 1 from, and § Out of scope B places Phase 2 outside this document. Recorded so a Phase 2 reader does not treat the escalation path as already required.

**Still open.** Vision §6.6 and TE §6.1 remain in textual conflict for Phase 1 —
D-17 lets work proceed without resolving it, and correcting the source sentences
runs through Vision §15.2. D-1's IGS site-log validation limitation is unchanged.
`.dst_summary.json` is still tracked, unmanifested and unhashed at the repository
root, deferred as above. Both governance verdicts — `GOV-2026-08-20-RA-01` and
`GOV-2026-08-21-RA-01` — stand at `FAIL` until a board is rerun against this
revision, and nothing in this revision opens a TEC gate.

## Sources

- [desc] Initial description, carried verbatim in
  `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/intent-capture/intent-statement.md`
  § Sources.
- [scope] Workflow-selected scope: `research-pipeline-governed`. This scope
  ships no `scope-document` artifact — `scope-definition` (1.4) produced its
  boundary inside the intent statement's `## Initial Scope Signal` section
  instead, which is where the product boundary, deliverable set and frozen
  modelling target are read from below. The `consumes` entry for
  `scope-document` is therefore satisfied by that section, not by a separate
  file; this is recorded rather than left as a silent gap.
- [intent] `ideation/intent-capture/intent-statement.md` — problem statement,
  driver contract, benchmark role, success layers, primary estimand, metric
  set, mandatory difficulty controls, model set, forecast horizon, reporting
  contract, sealing condition, scoped verification obligations, governance
  dependencies.
- [practices] `inception/practices-discovery/team-practices.md` and its
  companion `evidence.md` — affirmed way of working, testing posture,
  deployment posture, code style, and the observed-workspace evidence facts
  those practices rest on.
- [rules] `inception/practices-discovery/discovered-rules.md` and
  `aidlc/spaces/default/memory/project.md` — the 58 affirmed hard rules.
- [Vision] `PreFlight/vision_document(3)(2)(2).md` — **v4.3** (issued 2026-08-21).
  This artifact was authored against **v4.2** and revised against v4.3; the v4.3
  amendments it relies on are D-144's approval (§14.2, §17), the §6.1B coverage
  minimum (D-12) and the §5.2 H4 threshold (D-13). No other Vision clause changed,
  so v4.2-era citations elsewhere remain accurate for the clauses they name.
- [TE] `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` —
  **v3.3** (issued 2026-08-21), authored against **v3.2**. The v3.3 amendments are
  the §1.5 and TA-25 D-144 annotations; §6.1's row contract is **unchanged** and
  remains in conflict with Vision §6.6/§6.1A for Phase 1 — see § Known defects
  row 10 and D-17.
- [D-n] `evidence/DECISIONS.md`.
- **[board]** Governance board findings. The seven-seat board that reviewed
  practices-discovery (2026-08-16) produced findings `DATA-03`, `DATA-04`,
  `DATA-07`, `TEC-02`, `TEC-04`, `TEC-05`, `TEC-09`, `TEC-10`, `TEC-11`,
  `ML-02`…`ML-07`, `BENCH-01`, `BENCH-05`, `IMPL-07`, `VAL-05`, `CHAIR-02`,
  `GOV-22` and `GOV-25`, but **its report was never written to disk and its
  original text does not exist in this repository** — the same failure recorded
  at the head of `governance/reviews/GOV-2026-08-13-IC-01.md`. Per
  `GOV-2026-08-21-RA-01` Rec 10 (fallback B, approved 2026-08-21), every
  citation below therefore resolves to the **persisted rule text** that carries
  the finding's substance — `aidlc/spaces/default/memory/project.md`,
  `aidlc/spaces/default/memory/team.md`, or
  `inception/practices-discovery/team-practices.md` — with the finding ID kept
  only as a provenance label, marked *unpersisted*. No requirement rests on an
  unreadable authority. Reconstructing the report from memory and presenting it
  as the original is expressly not done.
- [Q1]–[Q10] Confirmed answers in `requirements-analysis-questions.md`.

## How to read this document

`requirements.md` is a **decomposition layer**, not a restatement and not an
index. [Q1] Each requirement carries:

1. a **stable ID** that later stages cite unchanged;
2. a **pass/fail criterion** — a condition an artifact, a test, or a named
   report either meets or does not;
3. an **inline source tag** naming the authority it derives from [Q7];
4. a **test link** to the §16 walking-skeleton row (`WS-nn`) or §19 technical
   approval row (`TA-nn`) that tests it.

`user-stories` (2.4) is SKIP in this scope, so WS-09–WS-20 and TA-01–TA-32 are
the **only** acceptance vocabulary Construction inherits. [practices] A
requirement with no WS or TA row is marked **`UNTESTED`** and listed in
§ Requirements with no testing row. No test row is invented to fill a gap. [Q1]

Functional decomposition follows the Technical Environment §7.0 Phase 1 stage
table P1-00 through P1-06, so requirements map onto the pipeline's own stages
rather than onto the `src/` package layout or an abstract dimension list. [Q2]
[TE §7.0]

**Phase-boundary discipline.** The intent statement's `## Success Metrics`
phase-boundary note binds this stage: the metric set, difficulty controls,
model set, horizon, reporting contract and sealing condition are **inherited,
not re-derived**. This stage's job is to give each a stable ID and a checkable
criterion. [intent] Nothing below re-opens a value the authority documents fix.

## Constraints inherited, not restated

Binding constraints live where they were affirmed. This document cites them and
does not copy them, so a later correction has exactly one place to land. [Q8]

| Constraint body | Where it lives | What it governs here |
|---|---|---|
| 58 affirmed hard rules (`ALWAYS`/`NEVER`) | `aidlc/spaces/default/memory/project.md` §§ Forbidden, Mandated; mirrored in `inception/practices-discovery/discovered-rules.md` | Every requirement below; a requirement never weakens one |
| Affirmed team practices — way of working, testing posture, deployment, code style | `inception/practices-discovery/team-practices.md` | REQ-ENG-*, and the acceptance model in § Success and acceptance |
| Observed-workspace evidence facts (13 facts, incl. the `raw_isprint_cache/` provenance finding) | `inception/practices-discovery/evidence.md` | FR-P1-01-*, REQ-DEF-* |
| Constraint register TC/OC/PC rows | `ideation/feasibility/constraint-register.md` | Cited inline as `[TC-nn]` etc. |
| Acquisition-window correction (year-blind predicate) | `evidence/CORRECTION_2026-08-16_acquisition_window.md` | FR-P1-01-4, FR-P1-04-2 |
| Governance board reports GOV-2026-08-13-IC-01/-02, GOV-2026-08-15-FE-01/-02, GOV-2026-08-15-AH-01, **GOV-2026-08-20-RA-01**, GOV-2026-08-21-RA-01 | `governance/reviews/` | § Known defects in the authority documents |
| Practices-discovery board findings (`DATA-*`, `TEC-*`, `ML-*`, `BENCH-*`, `IMPL-07`, `VAL-05`, `CHAIR-02`, `GOV-22`, `GOV-25`) | **Report not persisted.** Substance carried in `aidlc/spaces/default/memory/project.md`, `team.md` and `team-practices.md`; see § Sources **[board]** | Cited inline with the persisted rule text, finding ID kept as a provenance label |
| D-1 … D-19 scientific and governance decisions | `evidence/DECISIONS.md` | Cited inline as `[D-n]`. Added 2026-08-21: **D-12** §6.1B coverage minimum, **D-13** H4/SRQ-5 demotion threshold, **D-14** scientific fixture window, **D-15** locked-month custody relocation, **D-16** hourly aggregation statistic, **D-17** Phase 1 target-row contract, plus the **D-1 addendum** closing its countersignature under the recorded delegation |
| Supervisor gate table (G-05, G-06, G-07, G-P1A, G-P2, G-P3A/C) | Vision §13.1 | § Open supervisor gates |

## Intent analysis

**What the student is trying to achieve.** Two joined goals, in stated
priority order. [intent]

1. **Primary — a defensible hourly VTEC forecast** for the three frozen cells
   (ARUC 40/44, BSHM 32/35, NICO 35/33), calendar 2022, +1 h confirmatory
   horizon, evaluated once on locked December 2022. The claim that must
   survive examination is the paired loss differential (IRI-2016 squared loss
   minus LSTM squared loss, positive favours the model) with a 95% confidence
   interval, co-reported with three mandatory difficulty controls.
   [Vision §2.3] [TE §1.3]
2. **Supporting — a governed, reproducible pipeline** that demonstrably
   prevented leakage, recorded its own provenance, and reproduces on CPU from
   a clean environment.

**The goal behind the goal.** A forecast number is worth only the provenance
and leakage discipline behind it. [intent] Every requirement below exists to
make one of two statements checkable: *this predictor was genuinely available
at its forecast origin*, and *this artifact came from these exact bytes under
this exact configuration*.

**What is being requested now.** The immediate work is not model research. It
is: build the repository scaffold, pins and test suite (TC-06); re-acquire and
provenance the Phase 1 source; align the drivers onto the hourly grid without
interpolation; lag every predictor against its availability timestamp; then
build features, splits, masks, models and the evaluation. [desc] [TE §7.0]

**Type and complexity.** New build on a partially populated workspace: two scripts, one notebook, twelve months of derived audit evidence, and — corrected 2026-08-21 — **three test modules that do exist**, `tests/test_acquisition_window.py`, `tests/test_phase_boundary.py` and `tests/test_release_hashes.py`, against which FR-P1-01-5, FR-P1-02-6, FR-P1-03-2, FR-P1-04-11, FR-WS-3 and REQ-NFR-A2 all discharge. Still absent: `src/`, `configs/`, `pyproject.toml`, and the remaining **eighteen** of REQ-ENG-4's **twenty-one** test modules (corrected 2026-08-22 per `GOV-2026-08-22-UG-02` Rec 3, then re-derived 2026-08-22 after `CR-2026-08-22-TARGET-SCHEMA-TEST` and `CR-2026-08-22-LEAKAGE-TA` each added a module: the sentence formerly read "fifteen of eighteen" and then "sixteen of nineteen", both superseded; the total is now 21 and with three modules existing the remainder is 18. Counted from the TE §12 tree as amended by `CR-2026-08-22-TE-AMEND` — the total is 19, and with three modules existing the remainder is 16). The previous flat "no `tests/`" contradicted six of this document's own requirements [origin `IMPL-9`+`DATA-18`+`VAL-10`]. System-wide scope, complex domain, heavy external governance. Depth: Comprehensive.

---

## Functional requirements

Decomposed by the Technical Environment §7.0 Phase 1 stage table. [Q2] [TE §7.0]

### REQ-ENG — Repository scaffold, pins and tests (precondition to P1-01)

TC-06 places the scaffold, pinned environment and test suite **before any
further acquisition work, inside this initiative**. [TC-06] These are therefore
requirements of this initiative, not of a later one.

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| REQ-ENG-1 | The repository skeleton exists: `pyproject.toml` at root, four configs under `configs/` (`data.yaml`, `features.yaml`, `experiment.yaml`, `seeds.yaml`), six `src/` packages (`data`, `gnss`, `external`, `features`, `models`, `evaluation`), nine phase-aware stage scripts, five notebooks, `tests/`, `artifacts/`, **`requirements.txt`, `README.md` and `scripts/run_walking_skeleton.py`** — the last three are in the §12 tree and were omitted from this enumeration until 2026-08-21 | Repository tree matches the §12 layout item for item; the tree and its commit are recorded | [TE §12] [TE §13.2, which makes `run_walking_skeleton.py` the first clean-run command] | TA-01 |
| REQ-ENG-2 | All four configuration files exist and every unresolved field is visibly marked `TBD — freeze gate` | Config inventory plus schema validation returns no unmarked hole | [TE §12] [Vision §1.2] | TA-02 |
| REQ-ENG-3 | Python 3.11 with exact pins installs on **both** Kaggle and local. **The two-platform rule is stated so it can fail:** every governed run records its `platform` field (TE §13.1), and a run whose recorded platform is neither Kaggle nor local **fails**; the absence of a third-platform record is not itself taken as evidence none was used. **TE §9.1's inter-platform transfer rule applies to every artifact crossing between them:** a SHA-256 manifest accompanies the transfer and the transfer itself is recorded | Lock file, install log and environment hash from both platforms; the registry's `platform` values are a subset of {Kaggle, local}; each cross-platform transfer has a manifest and a recorded transfer event | [TE §8.1, §9.1 transfer rule] [TE §13.1 `platform`] [TC-03c, TC-03d] [origin `BENCH-09`] | TA-03, TA-26 |
| REQ-ENG-4 | The **21** mandated test modules exist under `tests/` — **all nineteen are now enumerated in §12's tree directly**, the count re-derived from that amended tree on 2026-08-22 by listing its `test_*.py` entries and counting them (`CR-2026-08-22-TE-AMEND`), not carried from prose. The tree reached nineteen by two amendments of different authority: `test_acquisition_window.py` was **countersigned 2026-08-16** (`governance/COUNTERSIGNATURE_REQUEST_2026-08-16.md` item 1) but was not written into §12 until 2026-08-22, and `test_determinism.py` was added under **ADR-10**, approved 2026-08-22 by the project owner under the recorded student/supervisor authority equivalence. Neither module's presence in the tree implies it exists: `test_determinism.py` is unwritten and remains subject to G-09 and its own stage — plus the two fixture directories `tests/fixtures/plumbing_7day/` and `tests/fixtures/scientific_1month/` | Each named module is present and collectible, `test_acquisition_window.py` included, since FR-P1-01-5 and FR-WS-3 discharge onto it. **Fixture assertion data lives in `fixture_manifest.yaml` carrying all thirteen of TE §15.2's content areas** — identity, input hashes, expected schema, row-count ranges, support and missingness limits, timestamp tolerances, required outputs, expected CPU runtime range measured before freeze, and permitted floating-point tolerances — never hardcoded in test bodies. Without the tolerance areas, FR-WS-5's *"within declared tolerances"* is evaluated against tolerances no requirement requires to exist. **TE §15.4's `artifact_manifest.json` hash-listing is required as well**, and **TE §13.7's rule that a mismatch "must not silently update the expected value"** governs every fixture expectation. **D-11's pre-freeze obligation stands: ARUC's one-bin shortfall on five of seven days is explained before the plumbing fixture is frozen**, not after [origin `DATA-11`+`IMPL-5`] | [TE §12, §15.2] [practices] [countersigned 2026-08-16] | TA-09 — bounded, see § Known defects row 8 |
| REQ-ENG-5 | Every hard rule in `discovered-rules.md` has a **negative-path** test proving the violation is caught — not only a happy-path test | For each such rule, a test exists that fails when the violation is injected | [practices] [Vision §7.1] | WS-10, TA-07, TA-08, TA-12, TA-27 |
| REQ-ENG-6 | Git is initialized before any further acquisition work, on `main`, with a credential/secret deny-list in `.gitignore` (`.env`, `*.key`, `kaggle.json`, `.netrc`, `credentials*`) present **before the first commit** | `git log` exists; **a secret scan over the working tree returns clean, and the pre-existing history breach is recorded separately rather than folded into that check** — the two are different obligations and the combined form was already unsatisfiable. `notebooks/madrigal_phase1_coverage_audit.ipynb` cell 2 carries `USER_EMAIL = 'kiimiiarezaee2025@gmail.com'` in every commit, and thirteen committed manifests carry `user_fullname` and `user_affiliation`; history is not rewritable without breaking the audit-trail immutability `team.md` affirms. So: prospective cleanliness is **tested**; the historical breach is **recorded** with its chosen remediation, and the underlying conflict is recorded in § Known defects with no reading adopted. The `.gitignore` deny-list this requirement names is already present [origin `DATA-16`] | [practices] [TE §10] [NFR-SEC-01] | TA-22 |
| REQ-ENG-7 | Each freeze gate (G-05, G-06, each phase transition) is tagged, and any commit changing a scientific constant or a governed config cites its D-number | Tag list covers the signed gates; commit-message audit shows a D-number on every governed change | [practices] | `UNTESTED` |
| REQ-ENG-8 | The two existing scripts and the coverage notebook migrate onto the §12 structure: `--config configs/` (and `--phase 1\|2` where applicable), a numbered `NN_verb_noun.py` position, the triplicated SHA-256 helper consolidated into `src/data/release.py`, the notebook's inline station coordinates and coordinate-to-cell rule moved into `configs/data.yaml` and `src/data/registry.py` **only after** those current values are frozen under a D-number, **and the acquisition identity block (`USER_EMAIL`, `user_fullname`, `user_affiliation`) migrated out of notebook source into platform-secret or environment configuration** — omitted from this list until 2026-08-21 [origin `DATA-16`] | Migration complete; `grep` shows no scientific constant remaining in source or notebook; the freeze D-number exists and precedes the move | [practices] [TE §12, §14] [TC-03e] [Q11] | TA-16 |
| REQ-ENG-10 | **Per-run environment lock.** Every run captures TE §13.1's eight items: the `requirements.txt` hash and a per-run `pip freeze`; Python, OS, CPU and key library versions; the code commit; configuration snapshot hashes for all four configs; input dataset and manifest versions; the platform; and any known nondeterministic operations | A registry row exists carrying all eight fields, populated — not `unavailable`; a run that captures none of them fails the check rather than completing silently. This is the requirement the thirteen existing runs are recorded as violating (`evidence/experiment_registry.md` § Acquisition runs: the §13.1 list "was not captured at the time and cannot be reconstructed"), so it binds from the next run forward | [TE §13.1] [NFR-REP-01] [NFR-AUD-01] | `UNTESTED` — no WS/TA row covers the §13.1 capture list; candidate new TA row via Vision §15.2 |
| REQ-ENG-11 | **Environment and CPU preflight report.** `environment_and_cpu_preflight_report` is produced, carrying TE §9.2's four elements — install-from-pins on **both** platforms, a completed walking-skeleton run, and measured CPU runtime, peak RAM and storage — and the run stays inside TE §9.3's **10.0 GB** hard planning envelope. TC-03, TC-03a (10 GB), TC-03b (GPU not required) and TC-03g are all `binding: hard` and are cited here rather than left out of § Constraints | The report exists and is the artifact G-07 accepts; each of the four elements is present with a measured value, not an assertion; recorded storage use is at or below 10.0 GB | [TE §9.2, §9.3] [TC-03, TC-03a, TC-03b, TC-03g] | TA-17, TA-26 |
| REQ-ENG-9 | `audit_ec1_drivers.py`'s exit-code gap is closed: a completeness shortfall is recorded as a machine-readable field in the output manifest, an integrity violation terminates the run naming the file and the violated expectation | Injecting a missing month yields a non-silent, machine-readable record; injecting a hash mismatch yields a non-zero exit with a naming message | [practices] `scripts/audit_ec1_drivers.py:184` | `UNTESTED` |
| REQ-ENG-12 | **TE §14's obligations for the four analysis/review notebooks**, stated rather than presumed by citing TA-16. Each of `01_data_and_target_audit`, `02_processor_verification`, `03_features_and_splits_review` and `04_results_and_figures` **imports functions from `src/`, reads versioned artifacts, and begins with the dataset version, code commit, configuration IDs and artifact IDs it expects**; **none of the four holds the only copy** of parsing, calibration, feature, split, training, evaluation or bootstrap logic. **"Run all" either succeeds from declared inputs or stops with a clear missing-artifact or Internet-access message** rather than proceeding on partial state — TE §14 states that sentence after both notebook classes, so it binds these four as well as the acquisition notebook. **The acquisition notebook is deliberately excluded from the import-from-`src/` and no-only-copy rules** and is governed by REQ-ENG-13 instead | Each of the four carries the four declarations; a `grep` finds no logic class present only in one of the four; a deliberately missing declared input makes "Run all" stop with the stated message rather than continue | [TE §14, lines 774 and 784, scoped as written] [TE §7 separation, quoted] [origin `IMPL-8`; scope corrected per `IMPL-15`] | TA-16 — re-pointed here, TA-16's content being stated by this requirement rather than assumed by REQ-ENG-8's citation of it |
| REQ-ENG-13 | **`00_acquire_phase1_vtec.ipynb` is a self-contained acquisition/audit interface, approved as such under D-144** — TE §14 calls it *"a narrowly approved self-contained acquisition/audit interface after D-144"*, so REQ-ENG-12's import-from-`src/` and no-only-copy rules **do not** reach it. It owes a **different** declaration set, six items and not four: **its own version, year and stations, source URLs, retrieval timestamp, destination paths, and resulting hashes**. Its **four prohibitions** hold: it *"may not calculate TEC/VTEC from observations, map `los` data, create model features, or train a model"*. Its reusable companion is **`scripts/00_acquire_prepared_vtec.py`** and **behavioral equivalence between that pair is tested** — the test is scoped to that named pair, not to acquisition logic at large. "Run all" either succeeds from declared inputs or **stops with a clear missing-artifact or Internet-access message** rather than proceeding on partial state | The six declarations are present; each of the four prohibitions has a check that **fails** when the prohibited operation is introduced; the notebook-versus-script equivalence test passes for the named pair; a deliberately missing declared input makes "Run all" stop with the stated message rather than continue | [TE §14, quoted] [D-144] [origin `IMPL-15`, `IMPL-16`] | TA-16 |

### FR-P1-00 — Close the rejected-source audit

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-00-1 | The ICTP source-failure evidence is immutable and machine-readable: `source_status=REJECTED_COVERAGE`, coverage recorded as ARUC 27/365, BSHM 35/365, NICO 0/365, decision stored as D-143 | The evidence set exists, hashes verify, and the status field is machine-readable | [TE §7.0 P1-00] [D-143] | TA-31 |
| FR-P1-00-2 | No ICTP artifact enters target construction or training | An import/data-lineage check shows no ICTP artifact reachable from the target or feature path | [TE §7.0 P1-00] [Vision R-23] | TA-25 |

### FR-P1-01 — Acquire the Phase 1 prepared VTEC product

This stage carries the deferred `raw_isprint_cache/` re-acquisition. FU-1=B
sequenced it **after** this requirements pass; per [Q4] it is specified now so
the deferred work has a specification when it runs, together with the
acceptance evidence that closes DATA-03 and DATA-04.

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-01-1 | Acquisition retrieves the approved Madrigal MAPGPS `gps` binned-VTEC product under D-144 (**approved 2026-08-21**, see § Known defects row 5; two of D-144's four attached freezes remain open and are named there), with the exact experiment and kindat/parameters frozen, and applies **no** scientific transformation at retrieval | The frozen experiment/kindat/parameter set is recorded; a diff of retrieved against stored values shows no transformation | [TE §7.0 P1-01] [D-144] | TA-32 |
| FR-P1-01-2 | Every retrieved file records provider, permanent citation, **full provider filename including its version suffix** (e.g. `g.002` vs `g.003`), retrieval date and SHA-256; a mismatch against a previously recorded suffix is surfaced, never silently accepted | `request_manifest.json` carries all five fields per provider file; an injected suffix mismatch raises. **`source_files` carries all six of TE §13.3's items, not five** — the earlier five-item list fixed a truncated count as the bar (`DATA-09`) | [TE §13.3] [practices § Walking Skeleton, § Deployment; origin DATA-07, unpersisted] | TA-15 |
| FR-P1-01-3 | The `madrigalWeb` client version is pinned and recorded — never `"unknown"` — and the exact web-service interface is recorded alongside it. **This is the acceptance evidence that closes DATA-03** (finding text unpersisted; the obligation it states — a recorded, pinned `madrigalWeb` version, never `"unknown"` — is verifiable against `evidence/*/request_manifest.json` independently of the report). | **Two checks, because a single string test was satisfiable by omission.** (1) Every `request_manifest.json` carries a **non-empty** `madrigalWeb_version`, and an **absent** key fails exactly as `"unknown"` fails — the live case being `evidence/locked_test_restricted/audit_evidence_2022-FULL/request_manifest.json`, which has no such key because `merge_coverage_year.py` copies eight identity fields and drops that one. (2) A derived release **verifies** that its identity fields agree across every source manifest rather than asserting they do; the eight fields do in fact agree across the twelve months, but nothing checked it. The pin also appears in the lock file | [TE §8.1, §10, §13.3] [evidence fact 5] [NFR-REP-01] | TA-03, TA-15 |
| FR-P1-01-4 | Native provider byte streams are retained, and `sha256_manifest.json` hashes **one entry per provider file**, not only the four derived artifacts. **This is the acceptance evidence that closes DATA-04** (finding text unpersisted; the obligation it states — provider byte streams retained and hashed per file, not only the four derived artifacts — is verifiable against the manifests independently of the report). | `find` locates provider files for every acquired month; each month's manifest hash count equals its provider-file count plus its derived-artifact count; the twelve pre-TC-06 months are re-verified under the new test suite rather than re-acquired from scratch. **An artifact produced outside the governed envelope is flagged, not silently re-verified:** `evidence/experiment_registry.md` records the 2026-08-16 corrected extracts as produced under **Python 3.14, local**, outside the 3.11 pin, so re-verification records the producing interpreter and marks any out-of-envelope artifact as such rather than treating a passing hash as evidence the envelope held [origin `DATA-20`] | [TE §10, §13.3] [evidence fact 6] | TA-04, TA-15 |
| FR-P1-01-11 | **A derived multi-month release either re-merges from the current months or carries a D-number re-pointing its provenance.** `PROVENANCE_NOTICE.md` stated this as prose — *"Do not rely on this artifact at a freeze gate while this notice stands… Either re-merge from the corrected months, or record an explicit decision re-pointing FULL's provenance"* — with no ID, criterion or test link, so nothing checked it | The release's `source_runs` digests **equal** the current per-month manifest hashes, **or** a D-number recording the re-pointing exists and is cited at G-P1A. A release whose digests predate a regeneration of any source month fails rather than being relied on. **Satisfied today by D-18**, whose re-merge is the first branch | [`PROVENANCE_NOTICE.md`, quoted] [D-18] [origin `DATA-08`] | `UNTESTED` — no WS/TA row covers derived-release provenance currency; candidate new TA row via Vision §15.2 |
| FR-P1-01-5 | Acquisition membership is derived from **record timestamps**, never from an acquisition directory name or filename; every per-month statistic excludes out-of-month and out-of-year records | `tests/test_acquisition_window.py` passes, including the case that produced the original defect (December records filed under `audit_evidence_2022-01/`) | [project.md § Forbidden] [`evidence/CORRECTION_2026-08-16_acquisition_window.md`] | `UNTESTED` — no WS/TA row covers the acquisition-window predicate; see § Requirements with no testing row |
| FR-P1-01-6 | Driver acquisition follows the frozen contract: Kp/ap3 and Hp60/ap60 from GFZ, hourly Dst from Kyoto WDC at a **single recorded release grade** for all of 2022, observed (not 1-AU-adjusted) F10.7 from Canada's Solar Radio Monitoring Program. SSN is absent | Each series carries **all nine of TE §5.1's inventory fields**, not three — provider, role, filename or product identifier, coverage, retrieval date, checksum, version or release status, licence and access notes, **and the configuration that consumes it**; a `grep` confirms SSN is absent from the codebase. **Two citation obligations are discharged before G-P1A rather than left uncollected:** the **Kyoto non-commercial-use notice recorded verbatim** (D-6, EC1-R-1) and the **CEDAR rules-of-the-road and acknowledgment** attached to `madrigalWeb`. A series carrying fewer than the nine fields, or a notice recorded by reference rather than verbatim, fails | [intent driver contract] [TE §5.1, enumerated] [D-6, EC1-R-1] [D-10.1, D-10.3] [Vision §6] [origin `DATA-14`+`IMPL-12`+`BENCH-10`] | TA-08 |
| FR-P1-01-7 | **The suspected outage beginning on 2022-03-18 was audited against the available 2022 source data. No missing calendar day was observed: at least one observation is present on 365 of 365 calendar days. This finding does not assert uninterrupted within-day coverage or uninterrupted provider availability.** Qualifiers and any reconstructed values are reported to the extent the source permits — the held archive carries no qualifier, flag or provenance column, so measured-versus-reconstructed is **not determinable from it** and is asserted neither way. **No imputation, substitution or reconstruction occurs until the measured gap is recorded and governed.** | The audit report exists with exact dates. **The three selection choices are frozen (2026-08-22) and are transcribed into `features.yaml` when Bolt 1 creates it, each citing its D-number:** (a) **the daily value is the daily median** of that UT day's observed readings — **D-21**; (b) **duplicate UT records take the mean** of the duplicated measurements, with duplicate logging and a quality-control flag, **provider-defined correction semantics taking precedence when documented** — **D-22**; (c) **the high-spread handling for the four days whose within-day spread exceeds 20% of the median — 2022-01-18, 2022-03-31, 2022-08-28, and 2022-08-29 — whose observed outliers occur at 18 UT, 20 UT, 20 UT, and 17 UT, respectively. Because outliers occur across multiple UT slots, fixed-hour selection without quality controls can retain contaminated observations.** Affected days are flagged and retained with the approved daily median as the representative value — **D-23**. **Availability constraint, binding: the approved daily F10.7 value must not become available to a forecast before all observations required to compute that value were actually available** (D-21). No same-day look-ahead is introduced. A run whose `features.yaml` leaves any of the three unset fails the zero-TBD preflight rather than resolving it by convention | [intent obligation 2] [TC-20] [EC1-AUDIT] [EC1-R-2, EC1-R-3, due G-04 before G-05] [D-21] [D-22] [D-23] [origin `DATA-15`; amended per `GOV-2026-08-22-DP-01`] | `UNTESTED` — the three selection choices are now frozen under D-21, D-22 and D-23 but carry no WS/TA row; the availability constraint's enforcement is verified through the FR-P1-04-2 availability matrix (WS-11, TA-08) rather than by a row of its own |

<!--
  FR-P1-01-7 amended 2026-08-22 under Vision §15.2, change record
  `CR-2026-08-22-F107-CORRECTIONS`, on the project decision owner's explicit
  approval, using the owner-supplied wording. Origin: governance report
  `GOV-2026-08-22-DP-01`.

  TWO CORRECTIONS INCORPORATED:

  (1) The claim "three of those four contaminated readings falling at 20 UT, the
      conventional pick" was wrong. Derived from the held provider file
      `evidence/audit_ec1_2026-08-15/nrcan_f107/fluxtable.txt` on 2026-08-22, the
      four high-spread days carry their observed outlier at 18 UT (2022-01-18),
      20 UT (2022-03-31), 20 UT (2022-08-28) and 17 UT (2022-08-29) — TWO at
      20 UT, not three. Replaced with the measured distribution and the owner's
      bounded consequence ("fixed-hour selection without quality controls can
      retain contaminated observations"). The stronger claims considered during
      review — that no single slot is clean, or that no fixed-hour convention is
      safe — are NOT made here: neither has been independently demonstrated.

  (2) The "documented month-long outage" framing asserted a hazard the data does
      not show. Replaced with the measured result at its stated granularity: at
      least one observation present on 365 of 365 CALENDAR DAYS. This explicitly
      does not assert uninterrupted within-day coverage or uninterrupted provider
      availability, and is not described as "zero outage".

  ALSO UPDATED (status, not correction): clauses (a)(b)(c) moved from open
  freeze-gate holes to frozen decisions D-21, D-22 and D-23, and D-21's
  availability constraint was carried into the criterion.

  WHAT DID NOT CHANGE: the no-imputation rule; the zero-TBD preflight
  consequence; the requirement ID; the test column's `UNTESTED` status; the
  source citations. No scientific value was invented. No locked-December data
  was accessed — the F10.7 archive sits outside evidence/locked_test_restricted/
  and is a predictor series, not target values or performance quantities.
-->
<!-- markdownlint-disable-line -->
| FR-P1-01-8 | No driver is backfilled from future final or definitive archived index values; the **release status** of every driver is recorded, not only its lag | Each driver's manifest carries a release-status field; a reanalysed-value check passes | [TE §10] [project.md § Forbidden, "NEVER backfill a driver from future final or definitive archived index values"; origin TEC-04, unpersisted] | `UNTESTED` |
| FR-P1-01-9 | Data gaps are stored as explicit `NaN` at acquisition time; no interpolation, smoothing or fill occurs at acquisition | An injected gap survives acquisition as `NaN` | [D-5, D-10.2] | `UNTESTED` |
| FR-P1-01-10 | Credentials and secrets are supplied through platform secret stores or environment configuration excluded from version control, and appear in no notebook, source file, configuration snapshot, log or registry note | Secret scan over tree, history and artifacts returns clean | [TE §10] [NFR-SEC-01] | TA-22 |

### FR-P1-02 — Inventory, registry and the G-P1A coverage gate

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-02-1 | **Station coordinates and the coordinate-to-cell rule** are validated against the **official IGS site logs** before being treated as final, and live in `configs/data.yaml` / `src/data/registry.py`, never in a notebook literal. The registry's remaining Vision §6.2 content — ellipsoidal height, DOMES identifier, receiver/antenna/firmware intervals, sampling interval, observable codes, 2022 hardware changes and the pinned IGRF version — is **FR-P1-02-7**, so this row's requirement text and its criterion cover the same ground. *"A conflict must be resolved and recorded, never averaged or ignored."* **An unresolved registry blocks `station_lat` and excludes `lst_sin`/`lst_cos` until longitude is verified** (TE §6.2), so this requirement gates feature construction rather than merely documenting it. **Split into two rows** so each carries one pass/fail verdict: the coordinates, cell rule, header cross-check and the never-average rule are tested here; the remaining §6.2 content is FR-P1-02-7 [per `DATA-23`] | Coordinates and the coordinate-to-cell rule match the official site logs; the header cross-check shows no unresolved conflict, and a conflict resolved by **averaging** fails; a run attempting to build `station_lat` or `lst_*` against an unresolved registry fails rather than proceeding | [Vision §6.2, enumerated and quoted] [TE §6.2 registry-blocking rule] [TE §7.0 P1-02] [§18.2 forbidden-choice items] [D-1, whose coordinates came from IGS network pages rather than the official site logs, validation outstanding] [origin `TEC-07`] | WS-01 — retained in Phase 1 as a named exception, see § Known defects row 9; TA-04 |
| FR-P1-02-7 | **The registry's §6.2 content beyond coordinates**: ellipsoidal height; DOMES or full identifier; receiver, antenna and firmware intervals covering all of 2022; sampling interval; available observable codes; any 2022 hardware change; and **one pinned IGRF version**, pinned rather than defaulted. All of it validated against the official IGS site logs before being treated as final | Every one of the seven is present and matches the site logs; a defaulted or absent IGRF version fails | [Vision §6.2] [origin `TEC-07`; split from FR-P1-02-1 per `DATA-23`] | `UNTESTED` — WS-01 reaches the registry's existence and the header cross-check only. Candidate new TA row via Vision §15.2 |
| FR-P1-02-2 | Schema validation covers parameter names, units, fill values, UTC cadence and duplicates for the prepared product | The prepared-data schema report exists and passes | [TE §7.0 P1-02] | TA-04 |
| FR-P1-02-3 | File, cell, day, month and common-timestamp coverage is audited **including December**, without inspecting any model performance. **An access-log row with `locked_test_accessed = true` is written BEFORE any operation that reads a December 2022 record** — the scope is *access*, unqualified, so it covers derived-artifact merges, re-derivations, corrections, coverage recounts and schema validations, not only a model execution | The coverage report covers all twelve months; no performance figure appears in it or in its execution log; every December read has a preceding access-log row, and a read with no prior row fails rather than proceeding | [TE §7.0 P1-02] [Vision §8.3, "access" unqualified] [origin VAL-2, GOV-2026-08-20-RA-01] | WS-18, TA-25 |
| FR-P1-02-4 | **G-P1A acceptance is decided against Vision §6.1B's numerical coverage minimum, frozen 2026-08-21 as D-12:** at least **90% usable hourly coverage per station per month**, as a hard gate, **together with** D-2's day rule (≥95% of calendar days per month, 100% of December days). Both must pass; neither substitutes for the other. §6.12's exception-plus-claim-limitation path does not apply at G-P1A | The G-P1A decision record cites D-12's 90% hourly figure and D-2's day rule, reports the measured per-station hourly and day coverage for every month, and never an unattributed number. Measured in-month hourly coverage as at 2026-08-21 (straddle days excluded): ARUC 99.2–100.0%, BSHM 99.3–100.0%, NICO 93.2–98.9% across the nine cached non-December months — every station-month clears 90% | [Vision §6.1B as amended] [D-12] [D-2] [Q3] | TA-25 |
| FR-P1-02-5 | The G-P1A prepared-data acceptance gate is reached with its evidence complete before any dependent work proceeds | The gate's evidence set exists and is registered | [Vision §6.1B] | TA-25 |
| FR-P1-02-8 | **Four prohibitions at the G-P1A gate**, split from FR-P1-02-5 so each row carries one verdict: silent imputation; source mixing; retrospective split redesign after model performance is viewed; and labelling a map value as station-observed VTEC | Each of the four has an injection test that **fails** the pipeline; four separate results, not one | [Vision §6.1B] [Vision §6.6] | `UNTESTED` — **`TA-29` was cited for this content and is withdrawn**: § Success and acceptance lists TA-29 under "Not applicable in Phase 1 — Phase 2 by definition", so citing it made the row *appear* covered and kept it out of this document's untested list, which is what stage 3.2 reads to size the G-05 freeze manifest. Four governance boards did not catch it. Candidate new TA row via Vision §15.2 [origin advisory pass, fifth revision] |

| FR-P1-02-6 | **Locked-test artifacts reside only under a restricted path until G-05 is complete.** TE §12 states two obligations in one sentence — restricted paths **and** the `locked_test_accessed` registry flag — and only the flag half was previously decomposed. Any file containing a December 2022 target value is a locked-test artifact, the merged year artifact and every `superseded_*` snapshot included | **No file under `evidence/` at any depth, outside `evidence/locked_test_restricted/`, contains a record whose observation date falls in December 2022.** Enforced by `tests/test_acquisition_window.py::test_locked_month_values_exist_only_under_the_restricted_path`. **Satisfied 2026-08-21 by the relocation recorded in D-15.** It was written while failing, against four unrestricted holders — 21,258 December rows each in `audit_evidence_2022-12/`, `audit_evidence_2022-FULL/` and `audit_evidence_2022-12/superseded_2026-08-16/`, plus 743 in `audit_evidence_2022-01/superseded_2026-08-16/`, roughly 58 MB. All are now under `evidence/locked_test_restricted/`; the criterion is retained as a regression guard, so any future run, merge or correction that re-creates a December-bearing artifact outside the restricted root turns it red again. **The restricted path is a governance boundary, not an access control** — no filesystem permission, encryption or ACL is involved, and none is claimed; what it buys is one declared location, a machine-checkable invariant, and an unambiguous access-log trigger | [TE §12] [origin VAL-1, GOV-2026-08-20-RA-01, Validation Auditor veto] | `UNTESTED` in §16/§19 — no WS/TA row covers at-rest location; enforced by the project test named above |

### FR-P1-03 — Standardize the prepared hourly target

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-03-1 | Provider values are preserved; only documented QC, UTC normalization, cell selection and the hourly aggregation are applied. **The hourly aggregation statistic is frozen as D-16 (2026-08-21): the median of the valid provider VTEC samples inside the UTC hour for the station's frozen cell.** Zenith-weighted aggregation is a separately declared sensitivity, authorised only before training and only if the data supports it — and it is **deferred as not computable**, because the Phase 1 product carries five columns (`ut1_unix`, `gdlat`, `glon`, `tec`, `dtec`) with no elevation, zenith angle or satellite identifier. **Nothing is substituted** for unavailable satellite-level or zenith information. TE §18.2 lists the statistic as a Student + Supervisor forbidden choice; exercised under the recorded authority delegation | A value-level diff against the provider bytes shows only the documented transformations, **and** the aggregation statistic cited by the run resolves to **D-16** rather than to a default. An earlier revision of this row asserted "the frozen hourly aggregation" when no decision had frozen it; that false statement was corrected first, and the freeze recorded second, as two explicit stages — GOV-2026-08-21-RA-01 Rec 21, option C | [TE §7.0 P1-03] [Vision §6.6] [TE §18.2] [origin DATA-05 and TEC-04, GOV-2026-08-20-RA-01] | TA-04 |
| FR-P1-03-2 | Phase 1 never estimates DCB or STEC, never maps `los` observations, and never silently interpolates a missing cell. **Import limb:** `src/gnss/rinex.py`, `src/gnss/calibration.py` **and every raw-processing adapter** are inaccessible from the Phase 1 target-build command — the §12 tree's `src/gnss/target.py` and `src/gnss/verification.py` are raw-processing adapters and are named here explicitly, having previously fallen outside every stated prohibition. **Produced-field limb, separately checkable:** Phase 1 must not produce DCB, STEC, mapping, **satellite** or **arc** fields | Two independent pass/fail results, not one: (a) `tests/test_phase_boundary.py` fails when an import of any named raw module is introduced, demonstrated for each; (b) the same suite rejects a Phase 1 artifact carrying a DCB, STEC, mapping, satellite or arc field. Neither result substitutes for the other | [TE §7.0 hard prohibition, quoted in full] [NFR-PHASE-01] [origin IMPL-2, GOV-2026-08-20-RA-01] | TA-27 |
| FR-P1-03-3 | Every dataset, prediction, mask and comparison is stamped with `phase_id`, `source_id` and `target_definition_id` | Schema test asserts all three on every such artifact | [TE §13] [NFR-TDEF-01] | TA-15 |
| FR-P1-03-4 | The Phase 1 target is labelled **location-sampled gridded VTEC**, never receiver-specific station-observed VTEC, everywhere it is described | A claims-checklist review over every artifact and figure caption finds no mislabelling | [Vision §6.6] [NFR-TDEF-01] | TA-15 |
| FR-P1-03-5 | **The Phase 1 target row carries exactly the contract frozen as D-17**, defined from the product that exists rather than from TE §6.1's Phase 2-shaped list: `interval_start_utc`; `station_id`; `cell_gdlat`/`cell_glon`; `cell_lat_bounds`/`cell_lon_bounds` (half-open, D-1); `vtec_tecu` (median, D-16); `valid_observation_count`; `within_hour_spread_tecu`; `largest_internal_gap_s`; `provider_dtec_summary`; `aggregation_config_id`; `target_valid`; `phase_id`/`source_id`/`target_definition_id`. **Excluded and never substituted:** `valid_satellite_count`, any per-satellite or per-IPP quantity, zenith angle or weight, elevation, DCB, STEC, mapping output, arc or slip statistics — none is derivable from a five-column gridded product (`ut1_unix`, `gdlat`, `glon`, `tec`, `dtec`, audited 2026-08-21 across all twelve request manifests), and TE §7.0 requires the phase-boundary test to reject a satellite field. `processor_qc_flags` carries **aggregation** flags only; the package, DCB, arc, elevation, slip and mapping classes are Phase 2 and are recorded not-applicable rather than emitted empty | A schema test asserts exactly D-17's field set — a row carrying an excluded field fails, and a row missing a required field fails. All four support values are **frozen as D-19 (2026-08-21)** from measured January–November distributions, December excluded by construction: `valid_observation_count` minimum **3** (keeps 95.24% of 23,709 deduplicated cell-hours), `within_hour_spread_tecu` statistic **range (max − min)** with a **10.0 TECU** threshold (p99 = 9.616), `largest_internal_gap_s` maximum **1800 s** (keeps 93.39%; median gap 300 s confirms the 5-minute cadence), `provider_dtec_summary` statistic **median of `dtec`** with a **1.5 TECU** flag (p99 = 1.314). They are recorded in `evidence/DECISIONS.md` under D-19 with their measured basis, and move into `configs/data.yaml` carrying that provenance when the REQ-ENG scaffold is built. **No `configs/` directory exists yet**, so the zero-TBD preflight (REQ-ENG-2, FR-WS-7) is not yet runnable on this component; the freeze is what will let it pass once the scaffold exists, and until then this row claims a decision made, never a check passed. **TE §6.1's provisional `valid_observation_count >= 20` is superseded for Phase 1 because it retains zero cell-hours** — the deduplicated maximum is 12, the product's native cadence being 5-minutely. `valid_satellite_count`'s provisional minimum of 4 remains **not applicable** in Phase 1 rather than open. `target_support_threshold_report` is the evidence artifact | [D-17] [D-16] [D-1] [TE §6.1] [Vision §6.6] [TE §18.2 Q-12] [EV-06] [origin TEC-03 and DATA-04, GOV-2026-08-20-RA-01] | `UNTESTED` in §16/§19 — the only field-contract row, WS-05, is deferred to G-P3A by FR-WS-4; enforced by the D-17 schema test and `tests/test_phase_boundary.py` |

### FR-P1-04 — External products, features, splits, masks

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-04-1 | No `iri_*` field, IRI-derived residual, or IRI-computed value reaches ML training or inference; IRI and GIM join **only at evaluation time** on the frozen comparison-wide mask; and the import boundary holds **as an allowlist, not a denylist** — TE §12 states it as "imported only by `scripts/04_build_external_products.py` and `src/evaluation/`", so an import from `src/data/`, `src/gnss/`, a training script or a notebook violates it exactly as an import from `src/features/` or `src/models/` does | `tests/test_iri_denial.py` **fails** on deliberate `iri_*` injection; the import-boundary check passes and **rejects an importer outside the two permitted ones**, the denylist-only form having left every other module free to import. No §12 module owns this check today — an authority-level silence recorded here rather than left to be read as covered (`IMPL-13`) | [Vision §7.1] [NFR-IRI-01] [TE §12 allowlist, quoted] [origin `IMPL-3`, `IMPL-13`] | WS-10, TA-07 |
| FR-P1-04-2 | Every predictor is lagged to its actual availability timestamp: Kp/ap3 ≥ 3 h, Hp60/ap60 ≥ 1 h, F10.7 at the previous-day observed value with a **trailing 81-day mean ending at the safe-lagged day** — never centered, and the anchor is part of the rule, not decoration; Dst is diagnostic/hindcast-only; SSN is absent | The availability matrix asserts actual lag ≥ declared safe lag for every primary feature; a centered-mean injection fails; **and the trailing window's end date is asserted to be the safe-lagged day**, since a trailing 81-day mean ending at day *t* passes both the not-centered check and the lag assertion while including same-day F10.7 | [Vision §6] [TE §6.2 `f107_81_trailing`, quoted] [D-10.3] [TC-10, TC-11] [origin `TEC-13`] | WS-11, TA-08 |
| FR-P1-04-3 | Missing external driver values carry forward at most 3 hours; beyond that the row is excluded | An injected 4-hour gap excludes the row | [TE §6.2] [TC-09] | WS-11 |
| FR-P1-04-4 | Driver series are time-indexed only — one value per epoch, identical across all three cells; a join never implies a per-cell measurement | Schema test asserts a single value per epoch across cells | [TC-12] | `UNTESTED` |
| FR-P1-04-5 | Folds are exact fixed calendar boundaries (F1: Jan–Mar/Apr; F2: Jan–Jun/Jul; F3: Jan–Sep/Oct; F4: Jan–Oct/Nov; December locked), each with a 24-hour embargo; no random or shuffled cross-validation; the first 24 h are excluded and counted. **The partition list also carries `Final refit: 1 Jan – 30 Nov`, and November enters the final refit only after all features, hyperparameters, masks, seeds, thresholds and analysis rules are frozen** — previously omitted, which left Vision §8.1's rule that each target timestamp belongs to exactly one partition with no list to check November against | No window crosses a boundary; the split manifest records the excluded count and enumerates all five partitions; a refit executed before the freeze fails rather than proceeding | [TE §7.1] [Vision §8.2, §8.1] [origin ML-02, GOV-2026-08-20-RA-01] | WS-12, TA-11 |
| FR-P1-04-6 | Any scaling or standardization is fitted on training partitions only, per fold, never on the full dataset | A full-dataset fit injected into the pipeline is caught | [Vision §6.4] [NFR-LEAK-01] | TA-11 |
| FR-P1-04-7 | A **single comparison-wide intersection mask** is computed once per comparison set and used for every model-versus-baseline comparison; masks carry stable IDs and reported row counts; no pairwise or model-specific mask is produced | Mask manifest shows one mask per comparison set with a stable ID; a pairwise mask attempt fails | [Vision glossary] [NFR-FAIR-01] [TC-16] | WS-16, TA-11 |
| FR-P1-04-8 | The flattened matrix and the sequence tensor for a given feature-set ID contain the same underlying window values | Matched-window assertion passes | [TE §16 WS-13] | WS-13, TA-11 |
| FR-P1-04-9 | The IRI benchmark and GIM comparator sample alignment passes; the IRI ceiling and drivers are recorded; the **`gim_network_overlap_flag` audit is present and its result disclosed**, and no independence claim precedes the audit. The IRI benchmark (**B-01**) and the GIM comparator (**C-01**) are represented in the model/config inventory and are labelled **generated, not trained** | Tolerance report, config snapshot and overlap audit all exist; the flag value appears wherever GIM is compared; the model/config inventory shows B-01 and C-01 present and marked generated-not-trained, never fitted | [TE §5.2] [Vision §6.10] [TC-08] [TE §19 TA-12] | WS-09, TA-12 |
| FR-P1-04-18 | **The GIM comparator's interpolation and independence obligations, split out of FR-P1-04-9, which carried only the overlap-flag limb.** Four requirements in one row because Vision §6.10 states them as one contract: (a) interpolation is **bilinear in space, linear in time, with a longitude-rotation correction** — a §18.2 **Student-owned forbidden choice** (Q-15), so no implementer may pick it; (b) *"One sample interpolation must be hand-checked against the code"*, and EV-11 places that hand-calculation **before** comparator generation; (c) because Madrigal binned VTEC is the adopted Phase 1 target, §6.10's conditional is **live**: the Phase 1 GIM comparison *"is explicitly a map-product-to-map-product comparison … cannot validate receiver-level station VTEC or serve as an independent target check"*, and that sentence is stated wherever the comparison is reported; (d) the comparator is never tuned and then claimed independent | `gim_interpolation_and_independence_report` exists and carries the interpolation rule, the hand-checked sample with its worked arithmetic, and the map-to-map statement; the hand-check's timestamp **precedes** comparator generation; a comparator generated before the hand-check fails rather than being accepted retrospectively | [Vision §6.10, quoted] [TE §5.2] [TE §18.2 Q-15] [EV-11] [TC-08] [origin `TEC-08`+`BENCH-03`] | `UNTESTED` — no WS/TA row covers the interpolation rule, the hand-check or the map-to-map statement; WS-09 and TA-12 reach sample alignment and the model/config inventory only. Candidate new TA row via Vision §15.2 |
| FR-P1-04-10 | Raw longitude never enters as a predictor; longitude enters only through `lst_sin` and `lst_cos` | Feature manifest contains no raw-longitude column | [TE §7.2] | `UNTESTED` |
| FR-P1-04-11 | Every dataset release records **TE §13.3's manifest in full — ten rows naming fourteen fields, against the seven this requirement previously listed**: `dataset_version`; `created_at_utc`; `source_manifest_id`; **`source_files`, whose own six items are specified by FR-P1-01-2 and are not restated in reduced form here**; the whole **`processing`** group — phase and target-definition ID, provider experiment/kindat, parameters, the station-coordinate-to-cell rule, selected cell bounds and hourly aggregation; `schema_version`; `units`; `row_counts`; `exclusions_qc_summary`; `fold_ids`; `mask_ids`; `feature_set_ids`; `output_files`; `change_record_id`. The count is stated as §13.3 states it: an earlier revision of this row said "thirteen field groups", a number carried from `DATA-09`'s finding text rather than counted against the table [count corrected per `DATA-21`]. The release is write-protected or stored under a new version rather than overwritten | `tests/test_release_hashes.py` mutation-protection test passes, **and a release missing any of the fourteen fields fails** rather than passing on the seven; `source_files` is checked against FR-P1-01-2's six items rather than against a hash alone. The previous seven-item list fixed a truncated count as the bar, so a release omitting its own processing provenance was conformant | [TE §13.3, enumerated] [origin `DATA-09`] | TA-15 |
| FR-P1-04-12 | **The permitted ML input space is closed.** The feature set is exactly the TE §6.2 dictionary — no field outside that table, and no derived tensor built from one, enters training or inference. Window length is one frozen value per feature-set ID, shared across all model families, and **the primary history window is 24 hours — a frozen constant, not a tuned hyperparameter** (Vision §8.1: "History length is not a tuned hyperparameter") | A field absent from the §6.2 dictionary fails feature construction rather than passing silently; the feature manifest enumerates only §6.2 fields; `experiment.yaml`'s window length **equals 24 and appears in no grid**, so a run that tunes it fails rather than proceeding; `ABL-HIST48` is the only sanctioned 48-hour path and runs after the primary configuration is frozen. **Concrete case named:** D-4 decided to acquire `kp, dst, f10.7, ap3` alongside the target, which would have placed driver columns of unrecorded release grade inside the Phase 1 target files — `dst` among them, where Dst is diagnostic-only. D-17 records that those four were **never actually requested** (the executed manifests take five columns), so the risk is closed by fact rather than by rule; the closed-set assertion is what keeps it closed if a re-acquisition changes the parameter list | [TE §6.2 "This table is the complete permitted ML input space"] [TE §6.4] | **TA-33** — negative-path acceptance row approved 2026-08-22 under Vision §15.2 (`CR-2026-08-22-LEAKAGE-TA`). Status `Pending`: the row exists, no test module is implemented, none has been executed, and none has passed |
| FR-P1-04-13 | **Target-derived lag contract.** `vtec_lag_1h/2h/3h/24h` are strictly causal at exact lags `[1,2,3,24]`; `vtec_seq_24` is a 24-step causal sequence excluded when incomplete; **carry-forward is prohibited for target-derived lags and the window is excluded instead** — the opposite of FR-P1-04-3's ≤ 3 h allowance, which is scoped to external drivers only and must never be read as reaching `vtec_lag_*`; the pooled model carries `station_onehot_ARUC/BSHM/NICO` plus verified `station_lat`, and an unresolved station registry blocks their use | An injected carried-forward `vtec_lag_*` value fails; an incomplete window is excluded and counted; the feature manifest carries the exact lag set, the 24-step sequence, the station one-hot columns and verified latitude | [TE §6.2 dictionary rows `vtec_lag_*`, `vtec_seq_24`, `station_onehot_*`, `station_lat`] [TE §2.1 model-granularity row, Q-05] [NFR-LEAK-01] | **TA-34** — negative-path acceptance row approved 2026-08-22 under Vision §15.2 (`CR-2026-08-22-LEAKAGE-TA`). Status `Pending`: row exists; not implemented, not executed, not passing |

| FR-P1-04-14 | **Vision §8.7's selection and refit protocol.** Configurations are selected on the **mean per-fold skill score across F1–F4**. Raw mean RMSE is **not** used; row-count weighting is **not** used. The declared baseline per track is named in configuration **before tuning begins**. Where mean skill differs by less than **1%**, the **simpler** configuration is selected. The selected configuration is then refit on January–November **without changing any hyperparameter** | Two mechanical comparisons: the selection record's criterion equals the criterion configured before tuning, and the refit hyperparameters equal the selected ones. A selection made on raw mean RMSE or row-count weighting fails; a refit that alters any hyperparameter fails; a run with no pre-tuning declared baseline fails | [Vision §8.7] [Vision §8.2 Final-refit partition] [TE §18.2, which makes the tuning criterion and refit rule human-owned] [origin ML-02] | `UNTESTED` — no WS/TA row covers the selection criterion; candidate new TA row via Vision §15.2 |
| FR-P1-04-15 | **The IRI-2016 benchmark is validated before generation, and generation is blocked if validation fails.** Per Vision §6.11, the `iri_implementation_validation_report` records: the pinned package/build with its exact version or commit; all model switches and the topside option; **the altitude ceiling stated explicitly as 2000 km**; units and output extraction; the coordinate, time, solar and geomagnetic driver inputs **with confirmation that no driver is future-centered or unavailable at target time**; and five to ten samples spanning sites, day and night, quiet and disturbed, validated against the **official IRI interface** within a tolerance **predeclared before the comparison runs**. The 26,000-call workload is timed, and the `iri2016` Fortran build re-establishes from pins on a cold session (TC-04) | The report exists with its sample tolerance table; **the benchmark's own drivers appear as rows in the same frozen availability matrix used for ML features**, each carrying observation timestamp, publication timestamp, release status and safe lag; a validation failure **blocks** benchmark generation rather than warning (TE §10); the measured 26,000-call runtime is recorded | [Vision §6.11] [TE §10] [TE §6.3] [TC-04] [EV-10] [origin TEC-01, TEC-02 and BENCH-02] | `UNTESTED` — no WS/TA row covers benchmark validation; `test_feature_availability.py` asserts over the ML feature table and B-01 is not a feature |
| FR-P1-04-16 | **The support-field rules are stated as requirements, not left inside an NFR criterion.** Three rules, all from TE §6.2: support fields are **diagnostic by default**; a support field may only be read over **hours ≤ t**, never the target hour or later; and **model use of any support field requires explicit G-04 approval** recorded before the feature set is frozen. A fourth is already carried by NFR-LEAK-01 and is restated here for completeness: **target-hour quality fields are permanently forbidden** as features | A support field used as a model input without a recorded G-04 approval **fails** feature construction; a support field read at or beyond hour *t* fails; the feature manifest marks every support field diagnostic unless an approval ID is present | [TE §6.2 support-field rules] [NFR-LEAK-01] [origin `ML-09`] | **TA-35** — negative-path acceptance row approved 2026-08-22 under Vision §15.2 (`CR-2026-08-22-LEAKAGE-TA`). Status `Pending`: row exists; not implemented, not executed, not passing |
| FR-P1-04-17 | **D-10.2's driver alignment contract.** Kp/ap3 is repeated **only within its own defined 3-hour interval**; Dst is aligned to **its own hourly averaging interval** and is *"not shifted to a neighbouring hour for convenience"*; F10.7 is daily; and **no driver is interpolated**, at any stage. This is distinct from FR-P1-04-3's ≤ 3 h carry-forward, which governs a *missing* value, where this governs how a *present* value maps onto the hourly grid | An alignment test carrying **both negative controls**: a Kp value repeated outside its 3-hour interval fails, and a Dst value shifted to a neighbouring hour fails. A `grep`-level check finds no interpolation call on any driver series | [`evidence/DECISIONS.md` D-10.2, quoted] [D-5] [origin `DATA-10`] | **TA-36** — negative-path acceptance row approved 2026-08-22 under Vision §15.2 (`CR-2026-08-22-LEAKAGE-TA`). Status `Pending`: row exists; not implemented, not executed, not passing |

### FR-P1-05 — Models, prediction, evaluation

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-05-1 | The model set is persistence (M-01), 24-hour seasonal persistence (M-02), fitted station×month×hour climatology trained on training folds only (M-03), ridge (M-04), Random Forest (M-05) and the compact LSTM (M-06); **residual and GRU modules are absent from the codebase**; TensorFlow/Keras is the only NN stack | All required model IDs are present in modules and configs; grep evidence shows residual and GRU absent, and PyTorch absent. M-03's fitting partition is a separate assertion and is carried by FR-P1-05-21, this inventory criterion not reaching a model fit | [intent model set] [TE §8.3] | WS-14, TA-12, TA-26 |
| FR-P1-05-2 | M-06 trains and restores its lowest-validation-RMSE checkpoint; the **three-seed element-wise mean** from `seeds.yaml` is the confirmatory prediction; no seed is selected on validation or after seeing December | Checkpoint-restore and seed tests pass; the seeds are fixed in config, not chosen at runtime; **and the seed values themselves are asserted against the frozen set**: development seed **42**, final seeds **{1337, 2024, 7}**, bootstrap seed **20221201** (Vision §8.6, D-122; TE §13.5). "Fixed in config" is satisfied by any three numbers, so the values are named rather than referenced. **D-122's own status is carried, not hidden:** Vision §14.2 marks it *"Approved — supervisor sign-off pending"*, so the seed set is frozen for implementation and still owes a signature at G-05 | [NFR-DET-01] [TC-21] [Vision §8.6] [TE §13.5] [origin `ML-05`] | WS-15, TA-13 |
| FR-P1-05-3 | No Random Forest importance score adds, removes or ranks a feature into the production feature set; RF importance is saved only as a non-authoritative diagnostic figure | The feature manifest's provenance shows no importance-derived selection | [Vision §6.4] [TE §6.4] | `UNTESTED` |
| FR-P1-05-4 | Tuning uses **January–November only**; model selection, feature selection, thresholds and hyperparameters are never informed by December. The trigger is December being **seen**, not the locked test being opened | The tuning record shows no December-derived input, including after the required pre-G-05 coverage audit | [Vision §8.3] [project.md § Forbidden, "NEVER let December inform model selection, feature selection, thresholds or hyperparameters"; origin ML-02, unpersisted] | `UNTESTED` — WS-18 tests the locked-test-open channel only, which a performance-blind coverage audit passes by construction, so it cannot test the trigger this requirement names: December being *seen*. WS-18 stays on FR-P1-05-12, where it does test the thing named. Candidate new TA row via Vision §15.2 [origin `ML-03`, GOV-2026-08-20-RA-01 MAJOR 1] |
| FR-P1-05-5 | Hyperparameter grids are exact and committed to configuration **before G-05**, and no grid range changes after December is seen; no second 2022 test period is selected after results are observed | `experiment.yaml` grids are frozen at the G-05 commit; a post-G-05 grid diff is empty; **and the grid *content* is asserted against the frozen values, named here so the check is falsifiable without a second lookup**: **ridge 6, RF 18, LSTM 16** combinations (Vision §8.6, D-121), with Vision §8.6's fixed LSTM training settings — **dropout 0.2, Adam, MSE loss, maximum 100 epochs, early-stopping patience 10 monitored on validation RMSE, minimum improvement 1e-4 TECU, best-checkpoint restoration rather than last epoch**. Naming them changes no value: D-121 and D-122 already approved them and this document only restates them. Provenance and immutability alone let a 40-combination LSTM grid be committed before G-05, diff empty afterwards, and pass with none of the specified members in it | [Vision §8.7, §8.10] [Vision §8.6 grid and fixed-setting content] [TE §7.1] [TE §13.5] [origin `ML-05`+`BENCH-11`+`IMPL-14`] | `UNTESTED` |
| FR-P1-05-6 | Ablations are **predeclared** as named runs registered in `experiment.yaml` with a run ID, executed on the frozen January–November folds with identical folds, masks and tuning budget. TE §7.2's registry is **five** named ablations, and each must hold a pre-freeze registry row: **`ABL-NODOY`**, **`ABL-DIFF`**, **`ABL-NOSW`**, **`ABL-HIST48`**, **`ABL-ZENITH`**. `ABL-DIFF` inverse-transforms to absolute TECU before any metric; `ABL-HIST48` runs only after the primary configuration is frozen. **No ablation is promoted to primary once the locked test is opened**, and no secondary result replaces the primary conclusion. **Phase call on `ABL-ZENITH`:** it varies the hourly aggregation of the target (zenith-weighted versus IPP median, Vision §6.6), a choice that does not exist on the Phase 1 location-sampled gridded target, so it is **deferred to Phase 2** and registered there — recorded here rather than left as an omission | All five IDs have a pre-freeze registry row, or in `ABL-ZENITH`'s case a recorded phase deferral; a missing required ablation fails the check rather than passing unnoticed; no ablation is registered after results are seen; **and the reported primary configuration's hash equals the one frozen at G-05** — an ablation promoted to primary after December is thereby detected rather than presented as the headline | [TE §7.2, including "no ablation configuration may be promoted to primary once the locked test is opened"] [Vision §2.4, which bars any secondary result replacing the primary conclusion] [TE §6.2 "subject to the required no-DOY ablation"] [origin `ML-06`] | `UNTESTED` |
| FR-P1-05-7 | The confirmatory estimand is the **paired loss differential — mean within-station difference of squared errors, benchmark minus model — with equal-station weighting**, positive favouring the model, reported at 95% | The evaluation module computes exactly this quantity; percentage reduction is computed only as a labelled derived summary; **and every table reporting the differential states the sign convention** — Vision §2.3 makes *"positive values favour the LSTM"* a binding convention that must appear in each table, because a signed differential printed without it inverts the conclusion for any reader who assumes the opposite orientation | [Vision §2.3, including the reporting convention] [TE §1.3] [origin `ML-11`] | `UNTESTED` |
| FR-P1-05-8 | Uncertainty uses the **vector time-block bootstrap**: 24-hour blocks carrying all three stations together, 10,000 replicates, seed 20221201, 95% CI, with the cross-station paired-error correlation reported. A within-station or naive bootstrap is not substituted | **Eight mechanical checks, not two.** TE §13.6 names seven and the widening control is the eighth: (1) predictions are **paired** per station-hour before differencing; (2) the resampling unit is a **vector block carrying all three stations at the same timestamps**, never one station resampled independently; (3) **block length** is 24 hours; (4) **replicate count** is 10,000; (5) station **weighting** is equal, matching the estimand; (6) the run **reproduces exactly** from seed 20221201 on synthetic correlated data; (7) a block holding a **missing paired prediction** is handled by the declared rule rather than silently dropped; (8) the interval is **wider** than the same data run through a naive within-station bootstrap — a narrower interval fails. A 48-hour block-length sensitivity is produced as well. Check 8 is why the other seven are not enough: without it a within-station resampler seeded 20221201 satisfies every stated criterion while producing systematically narrower intervals, which is exactly TC-19's named failure | [TE §13.6, all seven required tests] [TC-19] [origin `ML-04`+`IMPL-6`] | WS-17, TA-14 |
| FR-P1-05-9 | The three mandatory difficulty controls (M-01, M-02, M-03) are co-reported **in the primary results table**, never in an appendix | The primary results table contains all three controls plus the IRI comparison | [Vision §2.4 binding honesty rule] [PC-03] | TA-20 |
| FR-P1-05-20 | **Any baseline that beats the LSTM on the locked test appears in the primary results table *and* in the abstract-level conclusion.** A favourable LSTM-versus-IRI result never licenses silence about an unfavourable LSTM-versus-persistence or LSTM-versus-climatology result | A review of the abstract-level conclusion against the primary results table finds every baseline that beat the model disclosed in both places; a disclosure present in the table and absent from the conclusion fails | [Vision §2.4 binding honesty rule] [PC-04] [origin `BENCH-06`] | `UNTESTED` — TA-20 covers only the presence of the three controls in the table (PC-03) and reaches no abstract-level text; split out of FR-P1-05-9, which carried both limbs behind one TA-20 link on the project's highest-rated reporting risk (R-16, High/High). Candidate new TA row via Vision §15.2 |
| FR-P1-05-10 | The target uncertainty budget is produced and reported **adjacent to** the primary result; a top-1%-absolute-error-removed sensitivity is reported | **Contents, not existence.** `target_uncertainty_budget.json` exists, appears beside the primary result, and carries Vision §6.9's **Phase 1-applicable** contents together with the **asymmetry statement**: a slowly varying per-station-day bias partially cancels in the paired difference but *"does not cancel in the derived percentage summary, because it inflates the reference denominator"*. A budget file that exists and states nothing fails. Four of §6.9's six content items are Phase 2 quantities barred from Phase 1 and are recorded as not-applicable rather than emitted empty — see § Known defects row 11 | [Vision §6.9, contents and asymmetry] [NFR-DQ-01] [intent reporting] [origin `TEC-09`] | TA-19 |
| FR-P1-05-11 | The required prediction, residual, target-support and quality **plots** exist, each carrying its source-data IDs | Plot manifest lists every required plot with its source-data IDs | [TE §16 WS-19] | WS-19 |
| FR-P1-05-16 | Required reporting **breakdowns** are produced: per-cell metrics at +1 h, equal-station macro-average as the headline, pooled row-weighted as supplementary, quiet/disturbed/storm regime split, **observation-quality strata computed from D-17's measured-available fields only — bins over `valid_observation_count`, `within_hour_spread_tecu` and `provider_dtec_summary`; no stratum is defined on satellite count, elevation or zenith angle**, none of which exists on the five-column Phase 1 product — daily error and four local-solar-time diagnostic bins; December regime results are **descriptive only** unless at least three independent storm events occur (the same measured quantity D-13 uses) | Each named breakdown exists in the results artifact, each computed from a field the target declares; the storm-claim guard is enforced. **Two breakdowns previously absent are required as well:** Vision §9.5's **F1–F4 validation-fold table**, and **per-seed three-seed stability** reported per seed together with the mean and the spread (TE §13.5), not the mean alone. **Vision §9.4's four named diagnostic quantities are named rather than collapsed** into "observation-quality strata" | [intent reporting] [Vision §9.5 fold table] [Vision §9.4, four named quantities] [Vision §5.5] [TE §13.5 per-seed reporting] [origin `ML-12`, `TEC-14`; the previous `[Vision §11]` citation pointed at Traceability rather than at the reporting authorities] | `UNTESTED` — WS-19 tests plot existence only and reaches no breakdown and not the storm guard; split out of FR-P1-05-11 per GOV-2026-08-21-RA-01 Rec 11 |
| FR-P1-05-12 | The **locked-test guard** blocks December performance execution before G-05 is signed, records every access, and sets `locked_test_accessed = true` in the experiment registry; predictions are generated and written **once**, and hashed **before** any metric is computed | `tests/test_locked_test_guard.py` blocks a pre-G-05 December run; the access log row is written **before** the read, not after it, for every December access including non-execution reads; and the prediction hash precedes the metrics. An access recorded after the fact fails the ordering check rather than satisfying it. **Write-once has its own detection criterion**, since a bundled obligation with no check is what `VAL-8` found: the prediction file's hash is recorded at first write and re-verified before any later read, so a second write is *detected* rather than assumed absent. `tests/test_release_hashes.py` is scoped to dataset releases and does not reach predictions, so this check is separate and is named as such. An overwritten prediction is a Validation-Auditor veto condition. **The guard also records `prior_period_exposure=true`** — TE §7.0B states it as a positive obligation (*"shall record"*) and a `grep` for the field name previously returned zero occurrences in this document | [Vision §5.3, §8.3 — "access" unqualified] [OC-03] [origin VAL-2] | WS-18, TA-18 |
| FR-P1-05-13 | The experiment registry is operational, append-safe and atomic; failed and aborted runs remain visible with status and reason; no entry is deleted, overwritten or silently re-run. **Its schema is TE §13.4's twenty columns**: `run_id`, `started_at_utc`, `completed_at_utc`, `status`, `code_commit`, `environment_lock_hash`, `platform`, `dataset_version`, `fold_id`, `mask_id`, `feature_set_id`, `model_id`, `hyperparameters_json`, `seed`, `validation_metric_name`, `validation_metric_value`, `artifact_manifest_path`, `prediction_hash`, `locked_test_accessed`, `notes` | Registry tests pass, including a failed-run sample that remains visible; a schema assertion confirms all twenty columns exist and that `code_commit` and `environment_lock_hash` are populated on every row | [NFR-AUD-01] [TE §13.4] | TA-10 |
| FR-P1-05-14 | Any test-driven change made to the pipeline **after** locked-test access is labelled exploratory | Every post-access change carries the exploratory label in the registry | [Vision §8.3] | `UNTESTED` |
| FR-P1-05-15 | No practical-relevance threshold is introduced, changed or reinterpreted after December is opened. **Vision §5.4's first constraint is binding as well and was absent:** where the practical-relevance reference is **smaller than the target uncertainty budget**, practical relevance is **descriptive only** and may not be claimed as a result | The threshold record's timestamp precedes G-06; **and the reference is compared against the budget of FR-P1-05-10, with the descriptive-only label applied when it is the smaller of the two** — a practical-relevance claim made under that condition fails | [Vision §5.4, both constraints] [PC-09] [origin `TEC-09`] | `UNTESTED` |
| FR-P1-05-17 | **Evaluation code is authored, reviewed and frozen as part of the G-05 set before December 2022 is opened.** No evaluation code exists at intent time; it is authored inside this initiative | The evaluation modules exist, carry a recorded review, and their hashes sit inside the G-05 frozen config bundle; the freeze timestamp precedes any December access recorded under FR-P1-05-12 | [intent § Scoped Verification Obligations row 5] [Vision §13.1 G-05] | `UNTESTED` — no WS/TA row covers evaluation-code completeness, review or freeze |
| FR-P1-05-19 | **The plasmaspheric-offset disclosure accompanies every interpretation of the primary comparison.** Vision §6.11: GNSS-derived TEC extends farther into the plasmasphere than a 2000 km ceiling, so reported IRI–GNSS discrepancies *"contain a physical, structured, time-varying component that is not forecast error"* and this *"must be disclosed wherever the primary comparison is interpreted"*. Vision §5.1 SRQ-9 asks this question directly | A claims-checklist row asserts the disclosure text is present at each interpretation point — the primary results-table caption, the abstract-level conclusion, and the limitations section. Absent it, a structured physical offset reads as model skill in the headline number | [Vision §6.11] [Vision §5.1 SRQ-9] [origin TEC-01, TEC-02, BENCH-02] | `UNTESTED` — no WS/TA row covers the disclosure; candidate new TA row via Vision §15.2 |
| FR-P1-05-18 | **The December regime-count audit is required G-05 evidence, and the H4 demotion is legitimate only if recorded before the freeze.** The audit is performance-blind (as FR-P1-02-3) and produces the `December regime-count audit report` that Vision §13.1 names as a G-05 input. If it shows fewer disturbed hours than the supervisor-approved minimum, H4 and secondary research question 5 are predeclared **validation-fold-only** and reported as such. **That threshold is frozen as D-13 (2026-08-21): H4 and SRQ-5 stay confirmatory only if December contains at least three independent storm events under Vision §9.3's unchanged definitions — a contiguous interval of Kp>=5, with independence at >=24 h of Kp<4. No separate disturbed-hour count exists, by design: the threshold reuses the storm-event rule §9.3 already freezes, so H4's fate and the general storm-claim rule turn on one measured quantity. The count must come from GFZ Kp/Hp60 at a recorded release grade; D-11 bars any provisional-Dst-derived figure**. **Two further pieces of Vision §9.3 are carried here rather than referenced, both previously absent, because FR-P1-05-16's regime split and FR-P1-05-11's storm guard key on them:** the three **regime thresholds** — quiet `Kp<4`, disturbed `Kp>=4`, storm `Kp>=5` — which the regime split needs and which appeared nowhere; and each event's **analysis window of −12 h to +24 h** around it. The event and independence definitions are D-13's, quoted above, and are not restated in a second notation. All of §9.3 is *"frozen before any model result is inspected"* [origin `ML-10`+`VAL-5`+`VAL-6`+`TEC-10`] | Four obligations, four clauses — this criterion previously covered only the first two. (1) The audit report exists, is registered before the G-05 signature, and carries no model-performance figure. (2) Any H4/SRQ-5 demotion record carries a timestamp preceding the G-05 freeze; a demotion recorded after the freeze is invalid rather than corrected. (3) **The three regime thresholds are asserted as configured values** — an hour classified quiet at `Kp>=4`, or disturbed at `Kp>=5`, fails; the classification is read from configuration rather than recomputed per report. (4) **Each storm event's analysis window is asserted at −12 h to +24 h** — a window of any other span fails, and the event and independence definitions are checked against D-13's. Clauses 3 and 4 were added to the requirement text in the fourth revision without a matching criterion, so both obligations were unfalsifiable until now [origin advisory pass, fifth revision] | [Vision §13.1 G-05 evidence] [Vision §5.2 predeclaration for H4] [Vision §8.3] [R-13] | `UNTESTED` — no WS/TA row covers the regime-count audit or the demotion ordering |
| FR-P1-05-21 | **M-03's fitting partition.** The station×month×hour climatology is fitted on **training partitions only** and is never fitted using validation or December data | A negative case in which the climatology is fitted across all of 2022 **fails**; the fitted-partition record for M-03 names training folds only | [Vision §8.4, quoted] [origin `BENCH-07`] | `UNTESTED` — FR-P1-05-1's criterion is a module and `grep` inventory and does not reach a model fit; FR-P1-04-6 covers scaler fitting, not a model fit; WS-14, TA-12 and TA-26 test predictions running, an ID inventory and the pins row. Whether TA-11's "train-only transforms" is intended to reach a model fit is **unverified**, so it is not claimed here — confirming that reading, or adding a row, runs through Vision §15.2. A climatology fitted on all of 2022 would otherwise stop functioning as a difficulty control while passing every stated check |
| FR-P1-05-22 | **The +24 h horizon is implemented and testable, excluded only from the default run list.** TE §2.1: `experiment.yaml` *"shall expose `horizons: [1]` with `24` implemented and testable but not included in the default run list"*, and *"Building the +24 h label must require no code change, only a config change."* The artifact previously carried only the exclusion, in § Out of scope C, which leaves Construction free to build a +1 h-only path | A test builds the +24 h label **from configuration alone**, with no code change; `experiment.yaml` exposes `horizons: [1]` with 24 available and absent from the default run list. A +24 h path that requires a code edit fails | [TE §2.1, quoted] [origin `IMPL-7`] | `UNTESTED` — no WS/TA row covers the config-only horizon obligation; candidate new TA row via Vision §15.2 |

### FR-P1-06 — Phase transition freeze

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-06-1 | `phase_transition_manifest` hashes and freezes the **canonical protected set frozen as D-24 — the deduplicated union of TE §2.2 and §7.0B, seventeen items**, amended 2026-08-22 under Vision §15.2 (`CR-2026-08-22-PROTECTED-SET`): model source; TensorFlow/Keras environment; architecture serialization; feature manifest; **history window**; **station encoding**; target contract; split/mask manifests; grids; selected hyperparameters; **optimizer/loss policy**; seeds; **metrics**; **statistical configuration**; **bootstrap**; **reporting hierarchy**; **baselines**. **The three items in the last group — `history window`, `station encoding` and `baselines` — appear in TE §7.0B and mapped onto no item of the previous fourteen-item list.** `baselines` protects M-01 persistence, M-02 24-hour seasonal persistence, M-03 climatology, **B-01 the IRI-2016 benchmark with its frozen generation configuration including the 2000 km ceiling**, and C-01 the CODE final GIM comparator with its frozen product identity and interpolation rule. Phase 2 refuses to train if any protected hash differs. **A deliberate difference requires a change record and an `exploratory=true` label** (TE §2.2) — the only sanctioned escape, and therefore the only one | `tests/test_phase_boundary.py` **and** a transition-manifest hash-diff test both pass, **and the hash-diff test's protected-key list is asserted equal to D-24's seventeen-item enumeration** so a short list cannot pass silently; G-P3C confirms protected hashes unchanged; any deliberate difference resolves to a change record carrying `exploratory=true`. **The cardinality is calculated from D-24's enumeration, never assumed** | [D-24] [TE §2.2, 12 items] [TE §7.0B, 16 items] [NFR-PHASE-01] [origin IMPL-1, GOV-2026-08-20-RA-01; amended per GOV-2026-08-22-DP-01 and the owner instruction of 2026-08-22] | TA-27 |

<!--
  FR-P1-06-1 amended 2026-08-22 under Vision §15.2, change record
  `CR-2026-08-22-PROTECTED-SET`, on the project decision owner's explicit
  authorization ("Amend FR-P1-06-1 under §15.2 if its existing enumeration or
  fixed item count conflicts with the approved canonical set"). A conflict
  existed: the approved canonical set carries 17 items, this requirement carried 14.

  PRIOR TEXT, preserved for the audit trail — the item list read:
    "the union of TE §2.2 and §7.0B — fourteen items, not the nine previously
     enumerated: model source; TensorFlow/Keras environment; architecture
     serialization; feature manifest; target contract; split/mask manifests;
     grids; selected hyperparameters; optimizer/loss policy; seeds; metrics;
     statistical configuration; bootstrap; reporting hierarchy"
  and the criterion read "asserted equal to the fourteen-item enumeration".

  WHAT CHANGED: three items added (history window, station encoding, baselines),
  the count moved 14 -> 17, `baselines` was enumerated to its five protected
  methods, and the criterion now points at D-24 rather than a literal count.

  WHAT DID NOT CHANGE: no scientific value, threshold, seed, grid, fold, mask or
  estimand; the refuse-to-train rule; the exploratory-label escape; the test link
  (TA-27). This closes BLK-06's enumeration limb only — TransitionManifest.
  protected_hashes and diff_protected_hashes remain unwritten and gated by G-09.
-->
<!-- markdownlint-disable-line -->
| FR-P1-06-2 | Phase 1 fitted weights are never carried into Phase 2, and no Phase 1 result motivates a Phase 2 model or evaluation change, unless a separately approved, exploratory-labelled transfer-learning experiment exists | Phase 2 initializes from new weights; the change log shows no Phase 1-motivated change | [TE §7.0B] | TA-27 |
| FR-P1-06-3 | Every reused or materially adapted third-party source is recorded in the §10.1 register with the **full field set** — `reuse_id`, repository URL, immutable commit/tag, upstream file and line/function, retrieval date, licence and SPDX ID, copied-versus-adapted status, destination file, scientific purpose, modifications, tests, original citation, notice location, reviewer, approval date — **before** the code is used and before G-P2 | `tests/test_reuse_registry.py` passes; no adapter exists without a complete register row. **The adapter pattern is required, not presumed:** reused code lives behind a project-owned adapter and is **never pasted into a notebook** (TE §10.1, §14). This requirement governs acts occurring at **P1-01 and P1-04**, not only at the transition freeze under which it is filed, and FR-P1-01-6 and FR-P1-04-18 cross-reference it for that reason. The thesis-appendix inclusion and the notice-location mechanics are **deferred to G-P2** and recorded there rather than restated here [origin `DATA-14`+`IMPL-12`+`BENCH-10`] | [TE §10.1] [NFR-LIC-01] | TA-28 |
| FR-P1-06-4 | Third-party source whose licence is absent, ambiguous or incompatible is **not** copied or materially adapted; the published method is reimplemented from the paper with a citation instead. This is the standing default while the AGPLv3 distribution question remains open | The register contains no row with an unresolved licence status | [TE §10.1] [project.md § Forbidden, "NEVER copy or materially adapt third-party source whose licence is absent, ambiguous, or incompatible"; origin BENCH-05 and IMPL-07, unpersisted] | TA-28 |

### FR-WS — Walking-skeleton fixtures and clean run

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-WS-1 | Both fixtures run, in order, **before any full-year job**: the seven-day single-station plumbing fixture (frozen by D-11 as 2022-11-01 to 2022-11-07, all three cells) and the one-month all-station scientific fixture (**March 2022, all three cells, frozen 2026-08-21 as D-14** under Q-31) | Fixture run log shows plumbing before scientific before any full-year job | [TE §9.2] [TC-03f] [D-11] | WS-20, TA-09 |
| FR-WS-2 | The seven-day fixture is **never** treated as scientific evidence | No result artifact cites the plumbing fixture as evidence | [TC-03f] | `UNTESTED` |
| FR-WS-3 | No record whose **observation date** falls in December 2022 enters either fixture — asserted on record dates, never on the folder a file was filed under | `tests/test_acquisition_window.py` passes | [practices] [project.md § Forbidden, "NEVER derive fold or partition membership from an acquisition directory name or a filename"; origin ML-07, unpersisted] | `UNTESTED` |
| FR-WS-4 | Phase 1's acceptance set is **WS-09 through WS-20, plus WS-01 as a named exception**; WS-02–WS-08 are explicitly deferred to G-P3A because §7.0's Phase 1 hard prohibition bars Phase 1 from producing the raw-processing evidence those rows require. WS-01 (station registry) requires no raw-processing evidence and is Phase 1-producible, so the prohibition does not reach it — see § Known defects row 9. (WS-09–WS-20 countersigned 2026-08-16; the WS-01 exception approved 2026-08-21 by the project owner under the recorded authority equivalence.) | All twelve of WS-09–WS-20 PASS with evidence links, and WS-01 passes; no Phase 1 artifact claims a WS-02–WS-08 result | [TE §16, §16.1] [practices Q6=A] [GOV-2026-08-21-RA-01 Rec 12] | WS-01, WS-09…WS-20 |
| FR-WS-5 | A clean **CPU** environment reproduces both fixtures within declared tolerances, following the §13.2 ordered clean-run command sequence; GPU is an optional accelerator only and no result depends on it | `tests/test_clean_run.py` passes on a fresh CPU environment; the clean-run log and artifact comparison report exist | [TE §13.2] [NFR-REP-01] [TC-01] | WS-20, TA-17 |
| FR-WS-6 | The critical test set **and both fixtures** run **inside the Kaggle session** before any governed run executed there; the result is captured in that run's evidence record | The Kaggle run's evidence record contains an in-session test and fixture result, not a local one | [TE §9.1, §9.2] [TC-03g, which fixes the two-platform rule this obligation rests on; the in-session requirement itself is TE §9.1 and §9.2, and the earlier citation of TC-03g for the obligation is corrected here] [origin BENCH-01, unpersisted] | TA-03, TA-26 |
| FR-WS-7 | The §18.3 preflight gate passes before an affected component is implemented: **zero unresolved P0 fields and no failing critical test**, an automated assertion confirms no required field in the four configs is `TBD`, and supervisor sign-off covers the scientific hierarchy, IRI role, horizons, estimand, seeds and locked-test protocol. **A third assertion, restored verbatim from §18.3 and previously dropped: that every declared source and hash exists.** That is the clause which would have caught `DATA-01` (a verification chain that did not reproduce on this checkout) and `DATA-08` (a merged-year artifact whose `source_runs` digests pointed at superseded per-month hashes); both were found by a governance board instead. **The ten critical tests are enumerated rather than left as "the critical set":** target contract and DCB sign; availability lags; IRI-free denial; split embargo; train-only transforms; comparison-wide masks and matched windows; checkpoint restore; vector bootstrap; release hashes; locked-test access guard | `aws_ai_dlc_preflight_report` shows all four preconditions met — zero `TBD` fields, every declared source and hash resolving, all ten named tests passing, and the sign-off present. A declared hash that does not resolve fails the gate rather than being reported as a warning. An agent **stops and reports** rather than choosing a default when a P0 decision is unresolved | [TE §18.3, quoted] [origin `DATA-13`+`IMPL-10`] | TA-23 |

---

## Non-functional requirements

The Technical Environment §11 NFRs are **adopted by reference with their
existing IDs**. They are not renumbered and not restated; each gains a
pass/fail criterion and a test mapping here. [Q5]

**Correction to the question text.** `requirements-analysis-questions.md` Q5
enumerated nine §11 NFRs. §11 carries **eleven**: the nine named there plus
**NFR-DQ-01** (data quality and target uncertainty) and **NFR-TDEF-01**
(target-definition integrity). `NFR-REP-01` is **not** a twelfth — the Q5 stem
already lists it among its nine; it is named here only because the practices
artifacts under-cite it. All eleven are adopted, and the adoption table below
carries exactly eleven rows. [TE §11] [corrected per GOV-2026-08-21-RA-01 Rec 9]

| ID | Adopted meaning (not restated — see §11) | Pass/fail criterion here | Test |
|---|---|---|---|
| NFR-IRI-01 | IRI boundary integrity | `test_iri_denial.py` fails on deliberate injection; import-boundary check passes | WS-10, TA-07 |
| NFR-LEAK-01 | Forecast safety | Availability matrix asserts actual lag ≥ declared safe lag for every primary feature; no centered mean, **no future-aware interpolation**, no all-data scaling, no target-hour QC field as a feature — four sub-rules, §11's full set, the interpolation clause having been dropped previously (`ML-09`) | WS-11, TA-08, TA-11 |
| NFR-FAIR-01 | Fair comparisons | One comparison-wide mask per comparison set, stable ID, reported row counts, same window length and lag set | WS-16, TA-11 |
| NFR-REP-01 | Clean CPU reproducibility | The §13.2 ordered sequence completes on CPU from a clean environment, **and §13.7's exact-equality classes hold exactly**: hashes, schemas, partition membership, IDs and deterministic CPU transformations compare for equality, not tolerance, and a mismatch **must not silently update the expected value**. This is not theoretical here — the D-18 re-merge initially hashed differently from an artifact holding the identical record set, because output order followed directory traversal, and a sort on the dedup key was needed before two consecutive runs agreed byte for byte (`DATA-17`) | WS-20, TA-17 |
| NFR-DET-01 | Controlled randomness | Seeds fixed in `seeds.yaml`; three-seed element-wise mean is the confirmatory prediction; nondeterministic ops recorded | WS-17, TA-13 |
| NFR-DQ-01 | Data quality and target uncertainty | Units, times, signs and fill values documented; unexplained negative VTEC rejected; missingness and support reported by cell and month; target uncertainty budget produced | TA-19 |
| NFR-AUD-01 | Auditability and versioning | Stable IDs connect inputs to claims; registry is append-safe; failed runs stay visible | TA-10, TA-21 |
| NFR-SEC-01 | Secret protection and privacy | Secret scan over tree, history, configs, logs and artifacts returns clean; no PII stored | TA-22 |
| NFR-PHASE-01 | Phase-boundary integrity | `test_phase_boundary.py` plus the transition-manifest hash-diff test both pass | TA-27 |
| NFR-TDEF-01 | Target-definition integrity | Every target/prediction carries phase/source/definition IDs; no gridded value labelled a station observation; the grid-cell-versus-IPP mismatch disclosed | TA-15 |
| NFR-LIC-01 | Reuse and licensing integrity | Every adapted fragment has a complete §10.1 register row before use | TA-28 |

### NFRs the §11 set does not cover [Q5=C]

Three gaps were found. Each is proposed here with a **new** ID in a distinct
namespace so it cannot be confused with a §11 ID, and each is flagged as
requiring supervisor acceptance before it is treated as binding.

| ID | Requirement | Rationale — why §11 does not cover it | Pass/fail criterion | Test |
|---|---|---|---|---|
| REQ-NFR-A1 | **Driver release-grade integrity.** Every driver series records its release status (real-time / provisional / final), grades are never mixed within a series, and no value is backfilled from a future final archive | §11 has no driver-provenance NFR. NFR-LEAK-01 governs *timing*; a series can satisfy its declared lag while being built from reanalysed values — invisible to every existing check | Each driver manifest carries a single recorded grade for calendar 2022; a mixed-grade injection fails | `UNTESTED` |
| REQ-NFR-A2 | **Acquisition-window integrity.** Fold and partition membership derives from record timestamps only, never from a directory name or filename | §11 has no acquisition-provenance NFR. This gap already produced a realized defect: the year-blind predicate filed locked-test-month records under `audit_evidence_2022-01/` | `tests/test_acquisition_window.py` passes | `UNTESTED` |
| REQ-NFR-A3 | **Platform-parity of the gate.** The critical test set and both fixtures execute inside the platform where the governed run executes, not only locally | NFR-REP-01 governs *a* clean environment; it does not require the gate to run where the governed run runs. A Kaggle session carries no git working tree, so a commit hook cannot fire there | The Kaggle evidence record contains an in-session result | TA-03 |

---

## Constraints

**Technical.** Python 3.11 exactly; TensorFlow/Keras as the only NN stack;
PyTorch prohibited; R, Julia and MATLAB prohibited for the pipeline
[TE §8.1, §8.3]. Exactly two execution platforms — Kaggle and local; Google
Colab and Google Drive removed as governed platforms [TC-03c]. CPU is a
complete execution path, not an emergency mode [TC-01]. Exactly four governed
config files; no scientific constant in source or a notebook [TC-03e]. Notebooks
do not own production logic [TE §7, §14]. `ruff` for lint and format, configured
in `pyproject.toml` [practices].

**Data.** Three cells only, calendar 2022 only, December 2022 locked. NICO holds
53.8% of its native 5-minute slots against 96.4% of its hourly bins, so any
question requiring 5-minute resolution at NICO is out of reach on this dataset
and must not be claimed [D-7]. `evidence/locked_test_restricted/audit_evidence_2022-FULL/` (relocated 2026-08-21 under D-15; reading it is a logged December access) rests on
twelve monthly runs whose provenance is **unverifiable in principle** — no
provider byte stream exists in the workspace, and three months (2022-04,
2022-07 and **2022-12, the locked-test month**) have no `raw_isprint_cache/` at
all. Every artifact produced before the re-acquisition carries that caveat. The **superseded-hash** limb of it is discharged: **D-18 (2026-08-21) re-merged FULL from the corrected months**, moving `merged_at_utc` from 2026-08-13T06:27:03Z to 2026-08-21T09:25:59Z and its `source_runs` digests onto current per-month hashes, with the prior artifact preserved at `superseded_2026-08-21_audit_evidence_2022-FULL/` rather than overwritten. All twelve per-month manifests verified first. The **provenance** limb is untouched by that re-merge and still stands: no provider byte stream exists, so FULL's provenance remains unverifiable in principle until the re-acquisition, and this is now a requirement rather than a paragraph — see FR-P1-01-11 [practices § Walking Skeleton, § Deployment; origin DATA-07, unpersisted; `DATA-08`].

**Compute.** TC-03, TC-03a (10 GB), TC-03b (GPU not required) and TC-03g are all `binding: hard` and are carried as a requirement rather than restated here: REQ-ENG-11 requires the `environment_and_cpu_preflight_report` with TE §9.2's four per-run elements — install-from-pins on both platforms, a completed walking-skeleton run, and measured CPU runtime, peak RAM and storage — inside TE §9.3's **10.0 GB** hard planning envelope. Recorded here because a reader of this section would otherwise conclude the envelope is unstated [`BENCH-05`, found already closed by the 2026-08-21 audit].

**Organizational.** Single-author thesis codebase; the supervisor signs at named
freeze gates rather than reviewing merges [practices]. No CI service is used;
`ci-pipeline` (3.7) is SKIP in this scope. `user-stories` (2.4) is SKIP, so
WS/TA rows are the only acceptance vocabulary. No implementer or coding agent
may fill a `TBD — freeze gate` value by convenience [Vision §1.2] [TE §1.1].

---

## Success and acceptance

Vision's success framework is **adopted by reference**; only the measurable
engineering acceptance criteria are stated here. [Q9] The three success layers
(project completion, statistical evidence, practical relevance) and the
comparison hierarchy with its three mandatory difficulty controls live in
Vision §5 and §2.4 and in the intent statement's `## Success Metrics`.

**Engineering acceptance is independent of scientific outcome.** [Q9=C] The
pipeline passes engineering acceptance when its requirements above are met with
their evidence — regardless of whether the LSTM beats IRI-2016 or the
difficulty controls. **A correctly executed negative result passes engineering
acceptance.** A result that favours the model but was produced by a pipeline
failing a leakage, mask, seed or locked-test requirement does **not**.

Recording this separation is not a softening of the bar. It removes the one
incentive that most reliably corrupts a governed pipeline: the temptation to
treat an unfavourable result as an engineering defect to be debugged away.

**Engineering acceptance criterion.** WS-09 through WS-20 all `PASS` with
evidence links [FR-WS-4], the §18.3 preflight gate green [FR-WS-7], and the
Phase 1-applicable TA rows `Pass`. Visual inspection alone is insufficient at
every row [TE §16, §19].

**Which TA rows are applicable, enumerated.** Left undefined, "applicable" is
not checkable; enumerated 2026-08-21 per GOV-2026-08-21-RA-01 Rec 7.

- **Phase 1-applicable (30 rows):** TA-01, TA-02, TA-03, TA-04, TA-07, TA-08,
  TA-09 (bounded — see § Known defects row 8), TA-10, TA-11, TA-12, TA-13,
  TA-14, TA-15, TA-16, TA-17, TA-18, TA-19, TA-20, TA-21, TA-22, TA-23, TA-24,
  TA-25, TA-26, TA-28, TA-32, **TA-33, TA-34, TA-35, TA-36**.
  The last four were added 2026-08-22 under Vision §15.2
  (`CR-2026-08-22-LEAKAGE-TA`) as negative-path controls for FR-P1-04-12,
  FR-P1-04-13, FR-P1-04-16 and FR-P1-04-17; the count moved 26 → 30 and was
  recomputed from this enumeration. All four carry status `Pending` — approved as
  criteria, not implemented, not executed, not passing.
- **Not applicable in Phase 1:** TA-05 (`gnss-tec` adapter and calibration
  layer) and TA-06 (DCB sign worked example and reversed-sign control) — both
  require the raw-processing evidence §7.0's Phase 1 hard prohibition bars;
  TA-29 (Phase 2 target acceptance) and TA-30 (cross-phase 2×2 analysis) —
  Phase 2 by definition.
- **Evaluated at the phase boundary, not inside Phase 1:** TA-27's second limb
  ("Phase 2 cannot change protected forecasting hashes"), which G-P2 and G-P3C
  accept; its first limb (Phase 1 cannot import raw GNSS modules) is Phase
  1-applicable and is carried by FR-P1-03-2.
- **Already dispositioned:** TA-31 — recorded in TE §19 as "Pass for audit
  mechanics; source viability failed". It is not re-earned here and is not
  evidence that any source passed.

### Open supervisor gates

Enumerated in full, not only those on the visible critical path. [project.md
§ Way of Working]

Every row of Vision §13.1's gate-ownership table is carried below, with the
status and due condition that table records — not only the gates on this
initiative's critical path. This closes `AH-F-01` (GOV-2026-08-15-AH-01), which
assigned this enumeration to Requirements Analysis (2.3), and `AH-F-03`, whose
remediation was to make the decision log visibly identified as G-01 evidence.
Corrected 2026-08-21 per GOV-2026-08-21-RA-01 Rec 2; the prior seven-row table
omitted G-01, G-02, G-03, G-04, G-08 and G-09 behind a full-enumeration claim.

| Gate | What it accepts | Status per Vision §13.1 | Due condition | Owner |
|---|---|---|---|---|
| G-01 | Scientific framing — question, IRI-role statement, comparison hierarchy, claims, horizon scope | Pending sign-off | Before implementation freeze | Supervisor |
| G-02 | Station/data viability — site logs, headers, coverage, observables, cadence | Open | Before package freeze | Supervisor consulted |
| G-03 | GNSS target — package trial, DCB sign, sensitivities | Open | Before full-year processing | Supervisor |
| G-04 | Feature safety — availability matrix and dictionary, IRI-free contract proven | Open | **Before model tuning** | Supervisor for ambiguous inputs |
| G-05 | Experiment freeze — folds, masks, grids, seeds, estimand, bootstrap, regimes, storm rule, December regime audit | Open | Before December access | Supervisor |
| G-06 | Locked evaluation — write-once, hash-before-metrics December run | Blocked on G-05 | After G-05 | Student executes; supervisor authorises |
| G-07 | Reproducibility — CPU clean run, `environment_and_cpu_preflight_report`, clean-run log, matched artifacts | Blocked | Before thesis submission | Supervisor / reviewer |
| G-08 | Claims — conclusions matched to evidence, claims checklist, limitations, target uncertainty budget | Blocked | Before thesis submission | Supervisor |
| G-09 | Agent preflight — all P0 freezes complete, automated zero-TBD check, `aws_ai_dlc_preflight_report` | Open | **Before any affected component is coded** | Supervisor |
| G-P1 / G-P1A | Prepared-data MVP and source viability, incl. the §6.1B coverage minimum | Blocked — ICTP failed; Madrigal replacement audit pending. **The §6.1B coverage minimum is no longer the blocker: it is frozen by D-12** (≥90% usable hourly coverage per station per month, hard gate, together with D-2's day rule), Vision §6.1B amended in place 2026-08-21, change record `CR-2026-08-21-FREEZES`. The former "§6.1B value unfrozen" clause is corrected 2026-08-22 per governance finding `UG-02`; the gate itself stays `Blocked` on the replacement audit, which is a separate question from whether its threshold is frozen | Before the phase transition | Supervisor |
| G-P2 | Phase transition — protocol hashes frozen, reuse/licence register complete | Blocked | Before Phase 2 raw processing | Supervisor |
| G-P3 / G-P3A | Raw-target acceptance; WS-01–WS-08 raw-processing acceptance deferred from Phase 1 | Blocked / deferred to Phase 2 | Before Phase 2 model training | Supervisor |
| G-P3C | Phase 2 model validity — protected hashes unchanged, model reinitialized and retrained | Not yet reached | Before the Phase 2 confirmatory result | Supervisor |
| G-P1B | MVP validity — target release immutable, leakage and IRI-denial tests pass, baselines share the mask, tuning uses validation only, December opened once | Not yet reached | Before the MVP decision | Supervisor |
| G-P1C | MVP decision — Phase 1 result and uncertainty fully reported, negative and inconclusive outcomes included, mandatory controls present | Not yet reached | Before Phase 2 begins | Supervisor |
| G-P3B | Cross-processor validity — Phase 2 target on matched timestamps against Phase 1 and two approved references, thresholds frozen in advance | Not yet reached | Before Phase 2 model training | Supervisor |
| G-P3D | Reproducibility and claims — both phases reproduce on CPU, conclusions separate target-processing from forecasting effects | Not yet reached | Before thesis submission | Supervisor |

The last four rows are **TE §16.1** sub-gates, not Vision §13.1 rows, and are cited as such: seventeen gates govern this project in total. They were absent until 2026-08-21 (GOV-2026-08-20-RA-01 finding `TEC-05`, whose remediation asked for the §16.1 set alongside the §13.1 twelve).

**G-01 evidence, named.** Vision §13.1 lists G-01's evidence as "Sections 2, 4, 5
and decision log". The decision log that satisfies the last of those is
`ideation/approval-handoff/decision-log.md`; it is identified here so a produced
artifact that partly satisfies an open gate is visibly linked to it. Two of
G-09's inputs are stated in this document: FR-WS-7 (the §18.3 preflight) and
REQ-ENG-2 (the zero-`TBD` config assertion). G-04 accepts the FR-P1-04 group,
including the closed input space (FR-P1-04-12) and the target-derived lag
contract (FR-P1-04-13).

---

## Out of scope

Three lists, kept separate because the three exclusions have three different
reasons and conflating them would hide why. [Q6]

**A. Future (Vision §3.5)** — excluded because they are later work, not because
they are prohibited: operations, real-time ingestion, monitoring, service
deployment. Models here are versioned artifacts with a registry, not deployed
services [TE §7.0A stage 6, §8.2].

*Correction, 2026-08-21.* Two items previously placed in this list belong in list C,
because Vision §4.2 and §4.3 **prohibit** them rather than defer them: **a real-time
production service** (§4.2) and the non-proof clause of §4.3 — the work *"does not prove
operational readiness, commercial value, positioning benefit, or user demand"*. Listing a
prohibition as later work states the opposite disposition from the Vision, and a later
reader could reasonably treat an excluded claim as merely deferred. Both are moved below
[GOV-2026-08-21-RA-01 Rec 27; origin BENCH-01].

**B. Phase 2 (§7.0 hard prohibition)** — excluded because Phase 1 code is
**barred** from them: full-year GNSS-derived VTEC construction, RINEX parsing,
DCB handling, STEC calculation, mapping, satellite and arc fields. Phase 1 code
paths must not import or execute `src/gnss/rinex.py` or
`src/gnss/calibration.py` [NFR-PHASE-01].

**C. Out-of-claim (D-8, Vision §4.2, §4.3)** — excluded because no claim may extend
there. Adopted as **`REQ-CLAIM-01`**, the stable ID Vision §11.2 already assigns to
bounded claims, with its named check `TST-CLAIMS-01`; a new project-local ID is
deliberately **not** minted, because Vision §17's freeze checklist keys on the Vision IDs
and a parallel numbering would force a hand-built crosswalk.

**`REQ-CLAIM-01` criterion.** The claims-and-limitations checklist records, for each
prohibited class below, that no artifact, figure caption or abstract-level statement
asserts it. Test row: `UNTESTED` — see § Requirements with no testing row.

Prohibited classes, enumerated (Vision §4.2, §4.3):

- positioning-domain claims, and any improved-positioning claim;
- all-Iran, whole-sector or arbitrary-location claims;
- multi-year or solar-cycle generalisation;
- commercial, user-market, UI or deployment claims;
- **a real-time production service** (moved from list A);
- **operational readiness, commercial value, positioning benefit or user demand** — §4.3
  states the work does not prove any of them (moved from list A).

**Affirmative characterisation, required.** Vision §6.2: the thesis describes *"a bounded
three-station study in the mid-latitude Eastern Mediterranean–South Caucasus sector, not
a statistically representative regional sample"*. Vision §2.5 makes the sector name
**descriptive only** and denies independent spatial sampling — the three sites are
correlated, not independent spatial samples.

And, as before: generalisation beyond ARUC 40/44, BSHM 32/35 and NICO 35/33; beyond
calendar 2022; beyond December 2022 as the test month; beyond the +1 h confirmatory
horizon. The +24 h horizon is an optional extension outside the critical path,
and no thesis claim depends on it [intent]. No horizon between +1 h and +24 h
is authorised.

**D. What a reader might expect but will not get** [Q6=C] — stated so its
absence is not read as an oversight:

- **5-minute resolution at NICO.** Out of reach on this dataset; must not be
  claimed [D-7].
- **Receiver-specific station-observed VTEC.** The Phase 1 target is
  location-sampled gridded VTEC. Every IRI or GIM comparison carries a
  documented spatial-representativeness mismatch — a grid cell against a
  station-coordinate evaluation in Phase 1, an IPP cloud against a zenith
  estimate in Phase 2 — and part of any measured difference is a geometry and
  sampling artefact rather than skill [Vision §6.6] [TE §5].
- **Numerical equivalence between the Phase 1 and Phase 2 targets.** Cross-phase
  results test protocol transfer across a target-domain shift; agreement is not
  proof the two estimate the same physical quantity [Vision §2.2].
- **A second statistically independent blind test in Phase 2.** Phase 2 is a
  fixed-protocol replication on a new target lineage, because it reuses the
  December timestamps after Phase 1 has already reported them. This must be
  stated in the abstract-level interpretation [Vision §2.2, §7.0B; project.md § Mandated, "ALWAYS state in the abstract-level interpretation that Phase 2 is a fixed-protocol replication"; origin VAL-05, unpersisted].
- **Thesis chapter prose.** This initiative supplies figures, tables, metrics
  and methods text; the chapter is authored outside it [intent].

---

## Known defects in the authority documents

Every known defect this document relies on is recorded with the reading adopted
and its status, so a later reader is not misled by the source. [Q10]

| # | Defect | Reading adopted here | Status |
|---|---|---|---|
| 1 | **§16 vs §16.1 contradiction.** §16 states acceptance requires all 20 WS rows `PASS`; §16.1 assigns WS-01–WS-08 to the Phase 2 gate G-P3A, and §7.0's Phase 1 hard prohibition bars Phase 1 from producing the evidence those rows need. A Phase 1 fixture run cannot satisfy "all 20" without violating NFR-PHASE-01 | Phase 1's acceptance set is **WS-09 through WS-20**; WS-01–WS-08 deferred to G-P3A. See FR-WS-4 | **Resolved.** Supervisor-countersigned 2026-08-16, recorded on the student's report. Residual, recorded so it is not later misread as a coverage gap: no WS row covers train-only transforms in either subset; NFR-LEAK-01 is enforced through §18.3's gate-test list and TA-11 instead |
| 2 | **§1.3 stale counts.** The script and notebook counts in §1.3 do not match the §12 tree and §19 TA-01 | TA-01's enumeration (four configs, six packages, nine phase-aware stage scripts, five notebooks, tests, artifacts) is authoritative for REQ-ENG-1 | **Open.** Correction runs through Vision §15.2 change control, not through this workflow |
| 3 | **OC-03 over-broad wording.** Its "unexamined" phrasing, read flatly, forbids the pre-G-05 December coverage and regime audit that Vision §8.3 makes **required** | Two distinct events: the coverage/regime audit is required and performance-blind; the metrics evaluation is the one-shot, hash-gated G-06 event. Vision §8.3 supersedes OC-03's wording for coverage and regime counts. See FR-P1-02-3 and FR-P1-05-12 | **Open in the source; resolved in practice.** The reading is affirmed in `team-practices.md` § Testing Posture |
| 4 | **Vision §14.2 D-130 supersession pointers carry no counts.** The pointers name what supersedes what but not the affected row counts, so a reader cannot verify the supersession is complete | No requirement here depends on a D-130 count. Where a count is needed, the underlying artifact is counted directly | **Open.** Non-blocking for this stage |
| 5 | **D-144's status disagreed across the authority stack.** Vision v4.2 §14.2 carried it as "Decision required — Approve / Reject / Modify / Postpone" and "not yet adopted"; Vision §17's freeze line was unchecked; TE §1.5 read `Pending — D-144`; TA-25 read `Blocked`; `evidence/DECISIONS.md` D-3 recorded a 2026-08-15 countersignature with **no filed signature artifact** [origin GOV-22, unpersisted] | **D-144 is approved.** Granted 2026-08-21 by the project owner under the recorded student/supervisor authority equivalence, not by a filed supervisor signature — see `governance/CHANGE_RECORD_2026-08-21_D-144.md`, which carries the §15.2 six-field record, and the annotated status rows in Vision §14.2/§17 and TE §1.5/TA-25. The earlier reading ("countersigned … not blocked on it") asserted the same conclusion from a lower-precedence record and is superseded by this express approval | **Resolved 2026-08-21; residual updated 2026-08-22.** The four freezes Vision §17 attaches to D-144 are **all now closed**: Madrigal experiment/kindat and VTEC parameter/units by **D-4**; the coordinate-to-cell rule by **D-1**, its formerly blank countersignature row closed by the **D-1 addendum** under the recorded authority equivalence; the hourly aggregation statistic by **D-16**, with the resulting target-row contract frozen by **D-17**; and the numerical coverage minimum by **D-12**. The prior wording — "the hourly aggregation statistic (still `TBD — supervisor freeze gate`, Vision §6.6) and the numerical coverage minimum (still `TBD`, Vision §6.1B). Two of the four remain open" — was already superseded by `CR-2026-08-21-FREEZES` § Addendum when it was written; corrected per governance finding `UG-02` (`GOV-2026-08-21-UG-01`). **Still open, and not closed by this correction:** Vision §6.6's "exactly these fields" sentence remains in textual conflict with TE §6.1 (see row 10); D-1's IGS site-log validation limitation is separately open; and **TA-25 stays `Blocked` on the Madrigal replacement audit**, which no freeze discharges |
| 6 | **Q5 of this stage's own question set under-enumerated §11 as nine NFRs.** §11 carries **eleven** — `NFR-REP-01` is already inside Q5's nine, so the two genuinely missing IDs are `NFR-DQ-01` and `NFR-TDEF-01` | All eleven adopted; see § Non-functional requirements | **Resolved here.** An earlier revision of this row said "twelve", double-counting `NFR-REP-01`; corrected 2026-08-21 per GOV-2026-08-21-RA-01 Rec 9 |
| 7 | **`scripts/merge_coverage_year.py`'s hash check verifies derived artifacts, not retrieval.** Every `sha256_manifest.json` hashes exactly four derived files and never the contents of `raw_isprint_cache/` — and that cache holds isprint text extractions, not provider `.hdf5` bytes | Fixture eligibility is judged on **derived-artifact** verification, not retrieval verification. Retrieval-level verification is unavailable until the re-acquisition [FR-P1-01-4] | **Open.** Closes when FR-P1-01-4 is satisfied |
| 8 | **TA-09 independently repeats §16's "all 20" wording.** TE §19 TA-09 reads "Both walking-skeleton fixtures pass all 20 Section 16 checks with evidence links". Defect 1 resolved that wording for §16 and §16.1 only; TA-09 is a separate §19 row, and it is cited as the test link for REQ-ENG-4 and FR-WS-1, both Phase 1 requirements | **TA-09 is read as bounded by the approved Phase 1 acceptance set in FR-WS-4** — for a Phase 1 fixture run it means **WS-01 plus WS-09 through WS-20**, a set of **13** rows, pass with evidence links. **Corrected 2026-08-22 (`CR-2026-08-22-TE-AMEND`):** this row previously said "WS-09 through WS-20", omitting WS-01 and thereby stating a 12-row set. FR-WS-4 adds WS-01 as a named exception — WS-01 (station registry) needs no raw-processing evidence and is Phase 1-producible, so §7.0's prohibition does not reach it — approved 2026-08-21 by the project owner under the recorded authority equivalence, after the 2026-08-16 countersignature of WS-09–WS-20. Counts re-derived from §16 on 2026-08-22 by enumerating its WS rows: **20** total, **13** in Phase 1's set, **7** (WS-02–WS-08) deferred to G-P3A; 13 + 7 = 20. Reading TA-09 literally as "all 20" would require Phase 1 to produce WS-02–WS-08 evidence, which §7.0's hard prohibition bars — the identical contradiction defect 1 records | **Source clarified 2026-08-22; no new policy.** TE §19 TA-09's text now carries a clarification bounding it to FR-WS-4's approved set (`CR-2026-08-22-TE-AMEND`). That clarification restates an approved decision and creates no acceptance policy of its own. The reading remains consequential to FR-WS-4 rather than a separate decision. Originally recorded 2026-08-21 per GOV-2026-08-21-RA-01 Rec 7; WS-01 omission corrected per GOV-2026-08-22-REM-01 Rec 6 |
| 9 | **WS-01 is Phase 1-producible, yet falls inside the WS-01–WS-08 block deferred to G-P3A.** WS-01 (station registry populated from official site logs, pinned IGRF coordinates, header cross-check) is produced by `01_inventory_and_registry.py` and `test_station_registry.py`; neither is a raw-processing module, and `team-practices.md` lists `test_station_registry.py` as Phase 1-reachable. FR-P1-02-1 is a Phase 1 requirement (stage P1-02) and cites WS-01 as its test row, which FR-WS-4 simultaneously places outside Phase 1's acceptance set | **WS-01 is retained in Phase 1's acceptance set as a named exception to the WS-01–WS-08 deferral**, because §7.0's Phase 1 hard prohibition — the stated basis for that deferral — does not reach a station registry. WS-02 through WS-08 remain deferred to G-P3A unchanged. Without this exception the Phase 1 station registry, the authority for `station_lat`, the coordinate-to-cell rule and every per-cell statistic, would have no acceptance row at all | **Resolved 2026-08-21.** The amendment narrowing the 2026-08-16 deferral to WS-02–WS-08 was approved by the project owner under the recorded student/supervisor authority equivalence. Recorded per GOV-2026-08-21-RA-01 Rec 12 |
| 10 | **Vision §6.6 mandates a field TE §7.0 requires the phase-boundary test to reject.** TE §6.1 defines `vtec_tecu` as the median of valid VTEC at observed IPPs and `valid_satellite_count` as distinct valid satellites; Vision §6.1A/§6.6 fix the Phase 1 target as location-sampled gridded VTEC from a 1°×1° Madrigal bin — a product carrying no per-satellite or per-IPP quantity — while Vision §6.6 states "Each row must retain exactly these fields"; and TE §7.0 separately requires `test_phase_boundary.py` to **fail** if Phase 1 produces a satellite field | **Resolved by measurement, not by inference — D-17.** The conflict is real and is stated in full: Vision §6.6 says *"Each row must retain exactly these fields"* over TE §6.1's ten-field list, which includes `valid_satellite_count` (distinct valid satellites) and defines `vtec_tecu` as the median *"at observed IPPs"*; TE §7.0 separately requires `test_phase_boundary.py` to **fail** if Phase 1 produces a satellite field; and Vision §6.1A/§6.6 fix the Phase 1 target as gridded VTEC from a 1°×1° Madrigal bin. Rather than choose which document yields, the Phase 1 product schema was **audited**: `parameters_requested = ["ut1_unix", "gdlat", "glon", "tec", "dtec"]` in all twelve request manifests, matching the retrieved isprint extracts — five columns, no satellite identifier, no elevation, no IPP record, native cadence 5-minutely so at most 12 samples per cell-hour — **verified on 23,709 cell-hours deduplicated on `(station, ut1_unix, gdlat, glon)`; an earlier undeduplicated pass reported counts to 24 by double-counting the documented straddle day, and that error is recorded in D-19 rather than left as a stale figure**. `valid_satellite_count` is therefore **not computable** in Phase 1: the contradiction is not adjudicated, it is dissolved on the facts. D-17 records the contract this permits and marks the field not-applicable in Phase 1, Phase 2-only, with nothing substituted. A second consequence is recorded: TE §6.1's provisional `valid_observation_count >= 20` is **unsatisfiable** on a ≤12-sample hour and was evidently written for the Phase 2 IPP population | **Documented and resolved for Phase 1; the source texts remain in conflict.** D-17 lets Phase 1 proceed without adopting a reading, because it enumerates only measured-available fields. What is **not** resolved: Vision §6.6's "exactly these fields" sentence and TE §6.1's Phase 2-shaped provisional minima still read as binding on Phase 1 as written, and correcting them runs through Vision §15.2 change control. Recorded 2026-08-21 per GOV-2026-08-21-RA-01 Rec 22; origin TEC-03 + DATA-04 |
| 11 | **Vision §6.9's uncertainty-budget content list is Phase 2-shaped.** Four of its six required contents are per-satellite, per-IPP or geometry quantities that the five-column Phase 1 product (`ut1_unix`, `gdlat`, `glon`, `tec`, `dtec`) cannot yield, and §6.9 states the list without a phase qualifier | The **two applicable** contents plus the **asymmetry statement** are required by FR-P1-05-10; the four Phase 2 quantities are recorded **not-applicable in Phase 1** rather than emitted empty, on the same measured basis D-17 used to dissolve defect row 10 | **Documented; the source list is unqualified as written.** Adding the phase qualifier to §6.9 runs through Vision §15.2. Recorded 2026-08-21 per `GOV-2026-08-20-RA-01` `TEC-09` |
| 12 | **FR-WS-1 asserted both "single-station" and "all three cells" for the same `plumbing_7day` fixture.** TE §15.1 mandates one station and TC-03f describes the plumbing fixture as single-station; D-11 froze the window across all three cells. Both statements sat in one sentence with the conflict recorded nowhere | **Reading adopted 2026-08-22 — the D-11 clarification.** The original entry adopted no reading, on the ground that the conflict lay between a frozen decision (D-11, student-owned under Q-31) and an authority sentence (TE §15.1), and that resolving it either way would change what the fixture *is*: narrowing D-11 to one station would re-open a closed freeze, and reading §15.1 as permissive would rewrite an authority clause by inference. That reasoning is preserved above as the record of the conflict. **The resolution took neither route.** The **D-11 clarification of 2026-08-22** (`evidence/DECISIONS.md`, student-owned under Q-31, approved by the project owner under the recorded student/supervisor authority equivalence, on `GOV-2026-08-22-REM-01` Rec 3 option C) resolves a tension **inside D-11's own text** rather than between two documents: D-11's `Stations:` line is the **eligibility evidence** for the frozen window, and TE §15.1's **one-station execution scope is retained**. No authority document is amended — §15.1's "One station" stands, and D-11's frozen window (2022-11-01 to 2022-11-07 inclusive) is unchanged | **Reading limb closed 2026-08-22; station-selection limb open and still blocking.** `fixture_manifest.yaml` still cannot state its identity, because **the single station is not selected and not frozen** — that selection is the project owner's under Q-31 (TE §18.2 assigns fixture station, dates and tolerances to the Student). **No station may be selected by convenience and no manifest may be invented, inferred or substituted.** D-11's pre-freeze obligation stands: **ARUC's one-bin shortfall on five of the seven days must be explained before the manifest is frozen** if ARUC is selected. Tracked as **BLK-02** in `unit-of-work.md` § Blocker register. Originally recorded 2026-08-21 per `GOV-2026-08-20-RA-01` `DATA-11`+`IMPL-5`; **amended in place 2026-08-22 per `GOV-2026-08-22-UG-02` Recommendation 7, option 2, on the project owner's approval — the board had recommended option 1 (track the reconciliation as a residual and leave this row unedited, so a stage 2.7 remediation would not edit an approved stage 2.3 artifact); the owner ruled for direct amendment, and that ruling governs** |
| 13 | **NFR-SEC-01 forbids stored PII; the Madrigal rules of the road require a real identity on every request.** Both are binding, and the acquisition already performed under the second: `USER_EMAIL` is in the coverage notebook in every commit and thirteen committed manifests carry `user_fullname` and `user_affiliation`. Git history is not rewritable without breaking the audit-trail immutability `team.md` affirms | **No reading is adopted** on which obligation yields. What is decided is narrower and does not require choosing: REQ-ENG-6 tests **prospective** cleanliness over the working tree, the **historical** breach is recorded with its remediation, and REQ-ENG-8 migrates the identity block out of notebook source. Whether the retained manifest identity fields constitute an NFR-SEC-01 breach or a mandated provider record is the supervisor's call | **Open.** Owner: Student + Supervisor, G-09. Recorded 2026-08-21 per `GOV-2026-08-20-RA-01` `DATA-16` |

---

## Assumptions & Open Questions

**Assumptions carried, with rationale.**

1. **[assumption] Supervisor approval reported at Q3 does not itself supply the
   §6.1B numerical coverage minimum.** The student states supervisor approval is
   held and asked that it not be re-raised. No numeric value accompanied that
   statement, and `project.md` § Forbidden bars any agent from filling a
   `TBD — freeze gate` value by convenience. FR-P1-02-4 is therefore written
   with the threshold as an explicit named hole and operates on D-2's interim
   rule (≥95% of calendar days per month, 100% of December) until the frozen
   number is recorded under its own D-number. **Recording that D-number is the
   student's action, not this stage's.** [Q3]
2. **[resolved 2026-08-21, was an assumption] All three previously unfrozen
   supervisor values are now frozen.** Vision §6.1B's numerical coverage
   minimum is **D-12** (≥90% usable hourly coverage per station per month, hard
   gate, alongside D-2's day rule); the H4/SRQ-5 demotion threshold is **D-13**
   (three independent §9.3 storm events, no separate disturbed-hour count); the
   Q-31 one-month scientific fixture window is **D-14** (March 2022, all three
   cells). All three were approved by the project owner under the recorded
   student/supervisor authority equivalence; change record
   `governance/CHANGE_RECORD_2026-08-21_freezes.md`. **Standing restriction,
   unchanged:** D-11 bars provisional Dst from becoming a G-05 regime count, so
   D-13's storm-event count must be established from GFZ Kp/Hp60 at a recorded
   release grade, never from the provisional-Dst material in `.dst_summary.json`.

3. **[resolved 2026-08-21] The one-month all-station scientific fixture window
   is March 2022**, all three cells (**D-14**), selected for maximum regime
   separation from D-11's frozen November plumbing window and for the best
   measured coverage of any eligible month outside January — which was excluded
   because `audit_evidence_2022-01/` carries the year-blind-predicate custody
   irregularity that `GOV-2026-08-20-RA-01` findings `VAL-1` and `VAL-3` are
   open against. Measured in-month hourly coverage: ARUC 99.5%, BSHM 99.9%,
   NICO 97.8%; 32-day run staged with cache present. **Per TE §15.1 the
   fixture's counts, tolerances and runtimes are measured and frozen at
   fixture-manifest time, never inferred** — the figures here are selection
   evidence only.
4. **[assumption] The twelve already-acquired months are re-verified under the
   new test suite rather than re-acquired from scratch** (Q8=A of
   practices-discovery). Existing bytes stay; the checks that validate them are
   rebuilt. This assumption is what makes FR-P1-01-4's "re-verified" clause
   meaningful rather than a second full acquisition.

**Open questions carried forward.**

1. **§1.3's script/notebook count** — affects how the pipeline decomposes into
   units at `units-generation` (2.7). Defect #2 above.
2. **The coordinate-to-cell rule — corrected 2026-08-21.** The earlier text here
   described this as "currently a self-labelled 'PROVISIONAL' inline function in
   the coverage notebook", which is wrong: **D-1 already froze it** —
   `cell = (floor(lat), floor(lon))`, tested half-open on both axes, with the
   three assigned cells recorded and verified against executed 2022 output. What
   is open is the **countersignature**: TE §18.2 makes the cell rule a Student
   **and** Supervisor forbidden choice, and D-1's row in
   `evidence/DECISIONS.md` § Supervisor review is still blank, while twelve
   acquired months and D-11's fixture already rest on it. D-1's own recorded
   limitation is separate and also open: the station coordinates came from IGS
   network pages rather than the official site-log PDFs, which rank higher in the
   §6.2 evidence hierarchy, so site-log validation remains outstanding
   (FR-P1-02-1). REQ-ENG-8 sequences the notebook migration after the freeze,
   which D-1 supplies; the countersignature is not this stage's to make.
   [origin DATA-05 / TEC-04, GOV-2026-08-20-RA-01]
3. **The AGPLv3 distribution question** on the Global-TEC-forecasting
   repository — a governance dependency this project does not resolve on its
   own. FR-P1-06-4 states the standing default (reimplement from the paper)
   while it remains open.
4. **D-9 and D-10 signature rows remain blank**, so the acquisition route and
   the driver-source corrections are sole-signed [origin GOV-22, unpersisted; substance in `evidence/DECISIONS.md` D-3 row and `governance/COUNTERSIGNATURE_REQUEST_2026-08-16.md` item 4].

## Requirements with no testing row

Listed rather than invented. [Q1] Each carries a real pass/fail criterion above;
what is missing is a §16 or §19 row that tests it. These are the concrete input
`nfr-requirements` (3.2) needs when it assembles the G-05 freeze manifest, and
several are candidates for a new TA row through Vision §15.2 change control.

REQ-ENG-7, REQ-ENG-9, REQ-ENG-10, **FR-P1-01-11**, FR-P1-01-5, FR-P1-01-7,
FR-P1-01-8, FR-P1-01-9, FR-P1-02-6, FR-P1-03-5, FR-P1-04-4, FR-P1-04-10,
FR-P1-04-14, FR-P1-04-15, **FR-P1-04-18**, FR-P1-05-3, **FR-P1-05-4**,
FR-P1-05-5, FR-P1-05-6, FR-P1-05-7, FR-P1-05-14, FR-P1-05-15, FR-P1-05-16,
FR-P1-05-17, FR-P1-05-18, FR-P1-05-19, **FR-P1-05-20**, **FR-P1-05-21**,
**FR-P1-05-22**, FR-WS-2, FR-WS-3, REQ-CLAIM-01, REQ-NFR-A1, REQ-NFR-A2,
**FR-P1-02-7** and **FR-P1-02-8** — **36 fully untested requirements**. No row is partially untested any more: FR-P1-02-1 held both a test row and an `UNTESTED` qualifier in one pass/fail cell until the fifth revision split its §6.2 content out as FR-P1-02-7, so every requirement now carries exactly one verdict [per `DATA-23`].

**Four removed 2026-08-22 — 40 → 36.** `FR-P1-04-12`, `FR-P1-04-13`,
`FR-P1-04-16` and `FR-P1-04-17` left this list when the project decision owner
approved four distinct negative-path acceptance rows for them — **TA-33, TA-34,
TA-35 and TA-36** — under Vision §15.2, change record
`CR-2026-08-22-LEAKAGE-TA`. The four are leakage-sensitive controls rather than
ordinary coverage gaps, which is why they were promoted out of this list rather
than left in it (origin: governance finding `DP-ML-01`,
`GOV-2026-08-22-DP-01`). **The count above was recomputed from the test-row
column, not decremented by hand.**

**Four distinctions this change does NOT collapse.** Each of the four
requirements now has an **acceptance criterion**. None has an **implemented
test** — no module exists. None has been **executed**. None has **passed**. All
four §19 rows carry status `Pending`, and module placement for their tests is an
open assignment at functional design.

**Count, corrected.** The previous text said "the list is now 23 entries" while
listing 30, and said "five entries were added (bold)" while bolding twelve. Both
numbers were wrong, and a wrong count in this particular list is worse than no
count: it is the input `nfr-requirements` (3.2) uses to size the G-05 freeze
manifest. The counts above are computed from the test-row column of the
requirement tables, not maintained by hand.

**Nine entries were added on 2026-08-21** in the fourth revision (bold), each
one either a requirement that previously had no ID or a requirement whose test
link did not test it — which is again why the list grew rather than shrank:
FR-P1-01-11 (derived-release provenance currency, `DATA-08`); FR-P1-04-16
(support-field rules, `ML-09`); FR-P1-04-17 (driver alignment, `DATA-10`);
FR-P1-04-18 (GIM interpolation and independence, `TEC-08`+`BENCH-03`);
**FR-P1-05-4**, which was *removed* from the tested set — its WS-18 link cannot
test the trigger it names (`ML-03`); FR-P1-05-20 (the abstract-level disclosure
limb split out of FR-P1-05-9, `BENCH-06`); FR-P1-05-21 (M-03's fitting
partition, `BENCH-07`); FR-P1-05-22 (the config-only +24 h horizon, `IMPL-7`);
and FR-P1-02-1, which the fifth revision then split rather than leaving as a mixed verdict (`TEC-07`, then `DATA-23`). **Two more were added in the fifth revision:** FR-P1-02-7, the station registry's §6.2 content beyond coordinates, and **FR-P1-02-8**, the four G-P1A prohibitions — the latter because it had been citing `TA-29`, a row this document itself lists as not applicable in Phase 1, so it counted as covered while nothing tested it. That one was found by the advisory reviewer after four governance boards had passed over it, which is the clearest evidence in this file that a citation is not a test.

Three are worth naming as the most consequential gaps. **FR-P1-05-7** — the
confirmatory estimand itself has no TA row; TA-14 tests the bootstrap that
carries it, not the estimand's definition. **FR-P1-01-5 / REQ-NFR-A2** — the
acquisition-window predicate, which has already produced one realized defect and
is guarded today only by a project-authored test. **FR-P1-05-20** — the
abstract-level honesty disclosure, on the project's highest-rated reporting risk
(R-16, High/High), which until this revision was shown as covered by TA-20 and
was not.

**Two items are deferred rather than fixed here**, recorded so neither is later
read as an oversight:

| Deferred | Why | Owner / gate |
|---|---|---|
| Manifest or remove `.dst_summary.json` — 5,653 B at the repository root, tracked in git, unmanifested, unhashed, referenced by no script, manifest, decision or `.gitignore` entry, and holding December storm-day characterisation derived from **provisional** Dst | A workspace custody action, not a requirement. No custody breach — Dst is a public predictor series — but it is the path of least resistance for filling the regime-count requirement with an input D-11 prohibits. That substantive risk is already closed in FR-P1-05-18, which requires the count to come from GFZ Kp/Hp60 at a recorded release grade | Student / before G-05 [`VAL-11`] |
| The thesis-appendix inclusion and notice-location mechanics for reused third-party source | Governed at G-P2 and restated by stage 3.2's licence NFR; the acquisition-time obligations are fixed here in FR-P1-01-6 and FR-P1-06-3 | Student / G-P2 [`DATA-14`] |

## Traceability

Inline source tags appear on every requirement above; this table is the audit
view of the same mapping. [Q7]

| Requirement group | Primary authority | Ideation origin | Test rows |
|---|---|---|---|
| REQ-ENG-1…13 | TE §12, §14; D-144; §8.1, §9.2, §9.3, §10, §13.1, §18.3; TC-03, TC-03a, TC-03b, TC-03d, TC-03g, TC-06 | intent § Initial Scope Signal (deliverable: runnable pipeline); practices § Way of Working, § Code Style | TA-01, TA-02, TA-03, TA-09, TA-16, TA-17, TA-22, TA-26; REQ-ENG-10 `UNTESTED` |
| FR-P1-00-1…2 | TE §7.0 P1-00; D-143; Vision R-23 | intent § Phase 1 source status | TA-25, TA-31 |
| FR-P1-01-1…11 | TE §7.0 P1-01, §10, §13.3; D-144, D-5, D-10.1/.2/.3 | intent § Driver contract, § Driver preconditions, obligations 1–2 | TA-03, TA-04, TA-08, TA-15, TA-22, TA-32 |
| FR-P1-02-1…8 | Vision §6.2, §6.6; TE §7.0 P1-02, §12 (restricted paths); Vision §6.1B as amended, §8.3; D-2, D-12 | intent § Frozen modelling target | WS-01, WS-18, TA-04, TA-25; FR-P1-02-6 enforced by `tests/test_acquisition_window.py` |
| FR-P1-03-1…5 | TE §6.1, §7.0 P1-03, §7.0 prohibition, §13, §18.2; Vision §6.6; NFR-PHASE-01, NFR-TDEF-01 | intent § Target representativeness — binding | TA-04, TA-15, TA-27; FR-P1-03-5 `UNTESTED` (WS-05 deferred to G-P3A) |
| FR-P1-04-1…18 | Vision §6, §6.4, §6.11, §7.1, §8.1, §8.2, §8.7; TE §5.2, §6.2, §6.3, §6.4, §7.1, §10, §13.3, §18.2; TC-04, TC-08–TC-16 | intent § Benchmark role, § Driver contract | WS-09…WS-13, WS-16, TA-07, TA-08, TA-11, TA-12, TA-15; FR-P1-04-12, -13, -14, -15 `UNTESTED` |
| FR-P1-05-1…22 | Vision §2.3, §9.3, §9.4, §9.5, §2.4, §5.2, §5.3, §8.3, §8.6, §8.7, §13.1; TE §1.3, §7.2, §13.4, §13.6 | intent § Primary estimand, § Metrics, § Mandatory difficulty controls, § Model set, § Reporting, § Test-set sealing condition, § Scoped Verification Obligations row 5 | WS-14, WS-15, WS-17, WS-18, WS-19, TA-10, TA-12, TA-13, TA-14, TA-18, TA-19, TA-20; FR-P1-05-16, -17, -18 `UNTESTED` |
| FR-P1-06-1…4 | TE §2.2, §7.0B, §10.1; NFR-LIC-01 | intent § Governance Dependencies (G-P2) | TA-27, TA-28 |
| FR-WS-1…7 | TE §9.1, §9.2, §13.2, §16, §16.1, §18.3; D-11; TC-01, TC-03f, TC-03g | practices § Walking Skeleton, § Testing Posture | WS-09…WS-20, TA-03, TA-09, TA-17, TA-23, TA-26 |
| NFR-IRI-01 … NFR-LIC-01 | TE §11 (adopted by reference, IDs unchanged) | intent § Success Metrics phase-boundary note | as tabulated in § Non-functional requirements |
| REQ-CLAIM-01 | Vision §11.2 (ID adopted unchanged), §4.2, §4.3, §2.5, §6.2 | intent § Claim boundary; D-8 | `TST-CLAIMS-01` named by Vision §11.2; `UNTESTED` in §16/§19 |
| REQ-NFR-A1…A3 | Gaps found against TE §11; TE §10 driver table, §9.1 | practices § Testing Posture; board findings TEC-04, ML-07 and BENCH-01 (all unpersisted; substance carried in `project.md` and `team.md`) | mostly `UNTESTED` |

**Vision §11.2 crosswalk.** §11.2 supplies seven `REQ-*` IDs and states that *"The implementation shall expand this matrix rather than invent a separate traceability system"*. Vision §17's freeze checklist keys on those IDs, so a parallel numbering would force a hand-built crosswalk at the freeze gate. The crosswalk is therefore stated here rather than left to be reconstructed, and no Vision ID is uncovered [origin `ML-13`].

| Vision §11.2 ID | Covered here by | Note |
|---|---|---|
| `REQ-LEAK-01` | FR-P1-04-2, FR-P1-04-3, FR-P1-04-6, FR-P1-04-13, FR-P1-04-16, FR-P1-04-17; NFR-LEAK-01 | Availability lags, carry-forward bounds, train-only transforms, target-lag prohibition, support-field rules, driver alignment |
| `REQ-SPLIT-01` | FR-P1-04-5 | Fixed calendar folds with 24-hour embargo; never shuffled |
| `REQ-FAIR-01` | FR-P1-04-7, FR-P1-04-8 | One comparison-wide intersection mask; matched windows |
| `REQ-UNC-01` | FR-P1-05-8, FR-P1-05-10 | Vector time-block bootstrap; target uncertainty budget |
| `REQ-PRIMARY-01` | FR-P1-05-7, FR-P1-05-20 | The confirmatory estimand and the disclosure that protects it |
| `REQ-CONTROL-01` | FR-P1-05-1, FR-P1-05-9, FR-P1-05-21 | The three difficulty controls, their co-reporting, and M-03's fitting partition |
| `REQ-IRIFREE-01` | FR-P1-04-1; NFR-IRI-01 | IRI data-flow denial and the §12 import allowlist |
| `REQ-CLAIM-01` | § Out of scope C | Vision ID adopted unchanged rather than re-minted |

**Traceability rule honoured.** No requirement above is new. Each derives from
Vision v4.3 (authored against v4.2), Technical Environment v3.3 (authored against v3.2), a D-number decision, the constraint
register, the intent statement, or the affirmed practices — and says which.
[phases/inception.md § Traceability] The three REQ-NFR-A items are the single
exception class, and each is explicitly marked as a **proposed** addition
requiring supervisor acceptance, with its origin (the board finding that
exposed the gap) named.

## Review

NOT-READY

*(Advisory review by aidlc-product-lead-agent. Findings below go verbatim to the human approval gate. Three passes are recorded: iteration 1 below, a second advisory pass appended as "### Findings — advisory pass, 2026-08-21 (fifth revision)" against the fifth revision, and a third appended as "### Findings — advisory pass, 2026-08-21 (sixth revision)" against the sixth.)*

### Findings

1. **Major — the "Correction to the question text" NFR count is internally inconsistent and inflates §11's actual count.** (§ Non-functional requirements, lines 246–250.) The text states: *"`requirements-analysis-questions.md` Q5 enumerated nine §11 NFRs. §11 carries **twelve**: the nine named there plus **NFR-DQ-01**..., **NFR-TDEF-01**..., and **NFR-REP-01**, which the question listed but the practices artifacts under-cite. All twelve are adopted."* But the Q5 question stem it is "correcting" already lists `NFR-REP-01` among its nine IDs ("NFR-IRI-01, NFR-LEAK-01, NFR-FAIR-01, **NFR-REP-01**, NFR-DET-01, NFR-PHASE-01, NFR-SEC-01, NFR-LIC-01 and NFR-AUD-01" — `requirements-analysis-questions.md` line 76), so counting it a second time as one of the "plus" three double-counts it: 9 + 2 genuinely-new IDs (`NFR-DQ-01`, `NFR-TDEF-01`) = 11, not 12. This matches the source: `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §11 (lines 533–543) defines exactly eleven NFR IDs (`NFR-IRI-01`, `NFR-LEAK-01`, `NFR-FAIR-01`, `NFR-REP-01`, `NFR-DET-01`, `NFR-DQ-01`, `NFR-AUD-01`, `NFR-SEC-01`, `NFR-PHASE-01`, `NFR-TDEF-01`, `NFR-LIC-01`), and the artifact's own adoption table two paragraphs later (lines 252–264) lists exactly eleven rows — the table and its own preceding prose disagree by one. This is precisely the kind of authority-document-defect bookkeeping error Q10 was answered "A" to catch and record; here the artifact introduces a new one of its own, uncaught. Fix: change "twelve" to "eleven" and "the nine named there plus NFR-DQ-01, NFR-TDEF-01 and NFR-REP-01" to "the nine named there plus NFR-DQ-01 and NFR-TDEF-01," or otherwise reconcile the prose with the eleven-row table.

2. **Major — TA-09's own wording still requires "all 20" WS rows, and the artifact cites TA-09 as a test link for Phase-1-scope requirements without flagging the resulting contradiction with FR-WS-4.** `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` line 1014 defines TA-09 verbatim as: *"Both walking-skeleton fixtures pass **all 20** Section 16 checks with evidence links."* The artifact's § Known defects table (item 1, lines 404) records and resolves the **§16 vs §16.1** contradiction (§16 says "all 20 PASS"; §16.1 defers WS-01–WS-08 to G-P3A) by adopting FR-WS-4: "Phase 1's acceptance set is WS-09 through WS-20." But TA-09 is a separate, §19 row that independently repeats "all 20," and it is not named in the Known-defects table at all. The artifact nonetheless cites TA-09 as the test link for REQ-ENG-4 (line 128) and FR-WS-1 (line 230) — both Phase-1-scope requirements — and § Success and acceptance (line 331) states engineering acceptance requires "the applicable TA rows `Pass`," which would include TA-09 as written. A reader cannot tell whether TA-09 is (a) also superseded by the WS-09–20 reading, (b) genuinely unsatisfiable in Phase 1 the way §16 was, or (c) satisfied some other way — the artifact is silent. Fix: add TA-09 to § Known defects (or extend defect #1) with an explicit reading, e.g. "TA-09 is read as bounded by the same WS-09–WS-20 acceptance set as §16.1," and note its status (open/resolved) the way defect #1 does.

3. **Minor — Scoped Verification Obligation #5 from the intent statement (evaluation code must be authored, reviewed, and frozen as part of the G-05 set) has no corresponding requirement ID.** `ideation/intent-capture/intent-statement.md` § Scoped Verification Obligations, row 5: *"No evaluation code exists yet. It is authored inside this initiative and must be complete, reviewed and frozen as part of the G-05 set before December 2022 is opened."* This is a binding, checkable obligation ("complete, reviewed and frozen ... before December is opened") but no `FR-P1-05-*` or other requirement in this document states it as a pass/fail criterion with its own ID — the closest, FR-P1-05-12 (locked-test guard) and FR-P1-05-5 (grid freeze before G-05), cover adjacent but different content (access blocking and hyperparameter grids, not evaluation-code completeness/review/freeze). Under Q1's own rule ("Requirements with no testing row are flagged rather than invented"), the expected treatment for a sourced-but-uncovered obligation is a requirement ID in § Requirements with no testing row, not silent omission. Fix: add a requirement (e.g. `FR-P1-05-16`) stating the evaluation-code completeness/review/freeze obligation, sourced to the intent statement's obligation 5, and list it under § Requirements with no testing row if no WS/TA row covers it.

4. **Minor — TA-12's `B-01`/`C-01` model-ID and "generated, not trained" evidence scope is not decomposed into its own requirement.** `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` line 1017 defines TA-12 as covering *"All required model IDs M-01–M-06 plus **B-01 and C-01**"* (B-01 = IRI-2016 benchmark, C-01 = GIM comparator, both "generated, not trained" per line 424–425). FR-P1-05-1 (line 201), which is the requirement citing TA-12 as its test link, states only the M-01–M-06 model set and says nothing about B-01/C-01 or the generated-not-trained distinction TA-12 also checks. FR-P1-04-9 covers IRI/GIM evaluation-time usage but not this specific TA-12 grep-evidence scope. This leaves part of what TA-12 tests unaccounted for by any single requirement's stated criterion.

### Disposition of the advisory findings (2026-08-21)

All four were independently re-verified against the authority documents by the
TEC governance board (`GOV-2026-08-21-RA-01`) rather than accepted on
assertion, and all four are now remediated. The advisory text above is left
unedited as the original record.

| Advisory finding | Board finding | Disposition |
|---|---|---|
| 1 — NFR count says twelve, table has eleven | Rec 9 (High) | **Closed.** Prose and § Known defects row 6 both read eleven; `NFR-REP-01` identified as already inside Q5's nine |
| 2 — TA-09 repeats "all 20" and is cited for Phase 1 requirements | Rec 7 (High) | **Closed.** TA-09 added as § Known defects row 8 with its bounded reading; the Phase 1-applicable TA set enumerated in § Success and acceptance |
| 3 — evaluation-code freeze obligation has no requirement ID | Rec 16 (Medium) | **Closed.** Added as FR-P1-05-17 and listed under § Requirements with no testing row |
| 4 — TA-12's B-01/C-01 and generated-not-trained scope undecomposed | Rec 8 (Medium) | **Closed.** Carried into FR-P1-04-9 with TA-12 added as a test link, rather than into FR-P1-05-1, so the comparators stay out of the trained-model requirement |

### Disposition of `GOV-2026-08-20-RA-01`'s non-blocking findings (fourth revision, 2026-08-21)

That board's twelve blocking recommendations were applied in the second revision. Its 30 MAJOR and 13 MINOR/NOTE findings were then carried in this document as "unworked", which a resume-time audit found to be wrong in both directions. The per-finding result and the remediation are below. Every row was checked against the requirement text, not against the previous revision record.

| Finding | Status before | Where it landed |
|---|---|---|
| `ML-03` | Open | FR-P1-05-4's link changed to `UNTESTED`; WS-18 retained on FR-P1-05-12 |
| `ML-04`+`IMPL-6` | Open | FR-P1-05-8's criterion: eight checks, TE §13.6's seven plus the widening control |
| `ML-05`+`BENCH-11`+`IMPL-14` | Open | FR-P1-05-5 and FR-P1-05-2 now assert grid and seed **content**, not only provenance |
| `ML-06` | Open | FR-P1-05-6: the non-promotion rule and the primary-configuration hash comparison |
| `ML-07`+`TEC-12` | **Closed** | Five ablations already enumerated, `ABL-ZENITH` deferred to Phase 2 on a recorded phase call |
| `ML-08` | **Closed** | Already FR-P1-04-13 |
| `ML-09` | Open | New FR-P1-04-16; NFR-LEAK-01 regains "no future-aware interpolation" |
| `ML-10`+`VAL-5`+`VAL-6`+`TEC-10` | Partial | FR-P1-05-18 gains §9.3's three regime thresholds and the −12 h/+24 h event window |
| `ML-11` | Open | FR-P1-05-7: the sign convention is required in every table |
| `ML-12` | Partial | FR-P1-05-16 gains the F1–F4 fold table and per-seed stability |
| `ML-13` | Open | § Traceability gains the Vision §11.2 crosswalk, all seven IDs mapped |
| `DATA-07` | Open | FR-P1-01-3: an absent key fails as `"unknown"` does, plus identity-field agreement |
| `DATA-08` | Open | New FR-P1-01-11; the § Constraints caveat updated to what D-18 discharged |
| `DATA-09` | Open | FR-P1-04-11 restated against §13.3's thirteen groups; FR-P1-01-2's six `source_files` items |
| `DATA-10` | Open | New FR-P1-04-17, with both negative controls |
| `DATA-11`+`IMPL-5` | Partial | REQ-ENG-4 extended to §15.2's thirteen areas, §15.4's hash-listing, §13.7's no-silent-update and D-11's ARUC obligation; § Known defects row 12 records the station-count conflict with **no reading adopted** |
| `DATA-13`+`IMPL-10` | Open | FR-WS-7 regains §18.3's source-and-hash clause and enumerates the ten critical tests |
| `DATA-14`+`IMPL-12`+`BENCH-10` | Partial | FR-P1-01-6 gains §5.1's nine fields and the two citation obligations; FR-P1-06-3 gains the adapter and no-paste rules; appendix mechanics deferred to G-P2 |
| `DATA-15` | Open | FR-P1-01-7 gains the three F10.7 selection choices as `features.yaml` freezes due before G-05 |
| `DATA-16` | Open | REQ-ENG-6 separates prospective from historical; REQ-ENG-8 gains the identity block; § Known defects row 13, **no reading adopted** |
| `DATA-17` | Open | NFR-REP-01 gains §13.7's exact-equality classes and the no-silent-update rule |
| `DATA-19` | **Closed** | `run_walking_skeleton.py` already in REQ-ENG-1 |
| `DATA-20` | Open | FR-P1-01-4 flags out-of-envelope artifacts rather than silently re-verifying them |
| `TEC-06` | **Closed** | Vision §6.12's 90% rule already carried via D-12 |
| `TEC-07` | Open | FR-P1-02-1 restated against §6.2's full content, including the pinned IGRF version and the never-average rule |
| `TEC-08`+`BENCH-03` | Open | New FR-P1-04-18, carrying all four limbs |
| `TEC-09` | Open | FR-P1-05-10 gains contents and the asymmetry statement; FR-P1-05-15 gains §5.4's first constraint; § Known defects row 11 |
| `TEC-13` | Open | FR-P1-04-2 regains the trailing window's safe-lagged-day anchor |
| `TEC-14` | Open | FR-P1-05-16 re-cited to §9.5, §9.4 and §5.5; §9.4's four diagnostic quantities named |
| `TEC-15` | **Closed** | Already in § Out of scope C — an audit false negative, corrected |
| `BENCH-05` | **Closed** | Already in REQ-ENG-11 — an audit false negative, corrected; § Constraints now points at it |
| `BENCH-06` | Open | FR-P1-05-9 split; the PC-04 limb is FR-P1-05-20, `UNTESTED` and listed |
| `BENCH-07` | Partial | New FR-P1-05-21 with a negative case; TA-11's reach left **unclaimed** rather than assumed |
| `BENCH-09` | Partial | REQ-ENG-3 made falsifiable; §9.1's transfer rule added |
| `VAL-4`+`BENCH-08`+`IMPL-11` | Partial | `prior_period_exposure` added to FR-P1-05-12 |
| `VAL-8` | Partial | FR-P1-05-12 gains a write-once **detection** criterion |
| `VAL-9` | **Closed** | Already FR-P1-05-18 |
| `VAL-11` | Partial | The provisional-Dst bar was already in place; the file's custody is **deferred**, recorded under § Requirements with no testing row |
| `IMPL-3` | Open | FR-P1-04-1 restated as §12's **allowlist** |
| `IMPL-7` | Open | New FR-P1-05-22, config-only +24 h label |
| `IMPL-8` | Open | New REQ-ENG-12 carrying TA-16's content; TA-16 re-pointed to it |
| `IMPL-9`+`DATA-18`+`VAL-10` | Partial | § Intent analysis inventory corrected — three test modules exist |
| `IMPL-13` | Open | Recorded inside FR-P1-04-1 as an authority-level silence, no owning §12 module existing |

### Disposition of `GOV-2026-08-21-RA-02` (fifth revision, 2026-08-21)

| Finding | Severity | Disposition |
|---|---|---|
| `CHAIR-03` — the Chair authored the revision it reviewed | `BLOCKER` | **Disclosed, not closed.** Recorded in the revision record above; the human is the decision owner under `review-board.md`'s stated remedy. The finding is structural and cannot be closed by editing this document |
| `ML-14` — `ML-05` recorded closed and not closed | `BLOCKER` | **Closed.** Vision §8.6's grid counts, fixed LSTM settings and D-122's seed values are named in FR-P1-05-2 and FR-P1-05-5; D-122's pending supervisor sign-off is carried rather than hidden |
| `IMPL-15` — REQ-ENG-12 contradicts D-144 | `BLOCKER` | **Closed.** Split into REQ-ENG-12 (four analysis/review notebooks) and REQ-ENG-13 (the acquisition notebook, six declarations, four prohibitions, self-contained under D-144) |
| `DATA-21` — "thirteen field groups" and a reduced `source_files` | `MAJOR` | **Closed.** Restated as §13.3's ten rows and fourteen fields; `source_files` cross-references FR-P1-01-2 instead of collapsing to a hash |
| `DATA-23` — a mixed verdict in a pass/fail cell | `MAJOR` | **Closed.** FR-P1-02-1 split; FR-P1-02-7 created; the untested count recomputed to 39 |
| `IMPL-16` — misquote and over-broad equivalence scope | `MAJOR` | **Closed.** "behavioral" restored and the test scoped to the named notebook/script pair in REQ-ENG-13 |
| `CHAIR-04` — § Known defects rows out of numeric order | `MINOR` | **Closed.** Reordered 1–13 |
| `DATA-24` — `features.yaml` dependency unstated | `MINOR` | **Closed.** Sequenced behind REQ-ENG-1 in FR-P1-01-7 |
| `BENCH-12` — constellation report unrequired | `NOTE` | **Recorded, no change.** Phase 2-scoped; see the revision record above |

**What this remediation is not.** Every row above corrects a *specification*. A corrected specification is not evidence that the specified behaviour exists: 38 of these requirements have no §16 or §19 row, `src/` and `configs/` do not exist, and 15 of REQ-ENG-4's 18 test modules are unwritten. Both governance verdicts stand at `FAIL` until a board is rerun against this revision.

No findings on: Q3's handling of the unfrozen §6.1B coverage minimum (FR-P1-02-4 correctly writes the threshold as a named hole per the Forbidden-rule bar on filling TBD values, matching the Consolidated Summary's Q3 reading); the Q2 decomposition-by-P1-00..P1-06 structure (matches `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §7.0's stage table verbatim); the §16/§16.1 contradiction itself (correctly identified and resolved per the supervisor-countersigned FR-WS-4); the Q4/DATA-03/DATA-04 closure requirements (FR-P1-01-3 and FR-P1-01-4 explicitly name the DATA-03/DATA-04 items they close); or the out-of-scope, traceability-table, or "constraints inherited" sections, which are internally consistent and correctly sourced.

### Findings — advisory pass, 2026-08-21 (fifth revision)

*(Single, non-repeating advisory pass per `review_class: advisory`. Findings go verbatim to the human approval gate; this pass does not re-derive ground already covered by `GOV-2026-08-20-RA-01`, `GOV-2026-08-21-RA-01` or `GOV-2026-08-21-RA-02`, and confines itself to what a product lens sees that those technical boards' scopes did not: consumability by stages 2.6/2.7/3.2, requirement-quality-as-requirements, and completeness against the intent statement.)*

1. **Major — FR-P1-02-5 cites `TA-29` as a test link, but § Success and acceptance names `TA-29` explicitly as "Not applicable in Phase 1" ("Phase 2 target acceptance" / "Phase 2 by definition").** (FR-P1-02-5, § FR-P1-02 table; § Success and acceptance, "Which TA rows are applicable" list.) `FR-P1-02-5` sits inside "FR-P1-02 — Inventory, registry and the G-P1A coverage gate," a Phase 1 requirement group, and its Test column reads `TA-25, TA-29`. Two sections later, the same document states the Phase 1-applicable TA set as 26 named rows and separately lists "Not applicable in Phase 1: TA-05 … and TA-06 …" plus, in the very next clause, "TA-29 (Phase 2 target acceptance) and TA-30 (cross-phase 2×2 analysis) — Phase 2 by definition." No other requirement in the document cites TA-29 or TA-30 as a test link (checked by search), so this is an isolated, self-contained contradiction rather than a broader pattern. The practical effect is exactly the "false assurance" failure class the fourth revision's own remediation plan prioritized first (8 findings, ordered by consequence): `FR-P1-02-5` reads, on its face, as carrying test coverage, so it does **not** appear in § Requirements with no testing row — the very mechanism this document built to surface untested requirements to `nfr-requirements` (3.2) when it assembles the G-05/G-P1A freeze manifest. A reader assembling that manifest, or `application-design`/`units-generation` scoping test-writing work against this table, cannot get evidence for TA-29 inside Phase 1 (it is Phase 2 by definition) and has no signal from the document that they shouldn't try. Fix: either replace `TA-29` in FR-P1-02-5's test link with the correct Phase 1 row (if one of the 26 already covers the four prohibited actions named), or drop it and move FR-P1-02-5 into § Requirements with no testing row alongside its sibling FR-P1-02-4/-06, recording explicitly that no Phase 1-applicable TA row currently reaches this prohibition set.

2. **Minor — FR-P1-05-18 packs four separable obligations behind one ID and one merged pass/fail criterion, which a builder will necessarily implement (and a QA reviewer will necessarily check) as three or four independent items.** (FR-P1-05-18, § FR-P1-05 table.) The row's requirement text carries: (a) the December regime-count audit is required G-05 evidence and must be performance-blind; (b) the H4/SRQ-5 demotion is legitimate only if recorded before the G-05 freeze, with D-13's storm-event threshold; (c) the three regime thresholds (quiet/disturbed/storm, by Kp value); and (d) each storm event's −12h/+24h analysis window. Unlike the document's other intentionally-merged multi-part rows (e.g. FR-P1-04-18's four lettered sub-items, FR-P1-05-8's eight numbered checks), which each state their sub-parts as an enumerated, individually-checkable list inside one criterion cell, FR-P1-05-18's criterion sentence blends (a) and (b) into prose ("The audit report exists, is registered before the G-05 signature, and carries no model-performance figure; any H4/SRQ-5 demotion record carries a timestamp preceding the G-05 freeze…") while (c) and (d) — the regime thresholds and the analysis window — appear only in the requirement-text cell with no corresponding clause in the criterion cell at all, so there is no stated pass/fail test for whether the thresholds or window were actually applied correctly, only for the audit's existence and timing. This is not disputing the content (the four facts are all correctly sourced and needed), only that the row's own stated contract — "a pass/fail criterion, a condition an artifact, a test, or a named report either meets or does not" (§ How to read this document) — is not met for two of its four stated obligations. Fix: either add explicit pass/fail clauses for the regime thresholds and the analysis window to the criterion cell, or split them into their own row(s) the way FR-P1-02-1/FR-P1-02-7 and FR-P1-05-9/FR-P1-05-20/FR-P1-05-16 were split elsewhere in this same revision for the identical reason (one verdict per row).

No findings on: the mapping of the intent statement's five Scoped Verification Obligations onto this document (obligation 1 → FR-P1-01-6, obligation 2 → FR-P1-01-7, obligation 3 → FR-P1-05-7 and § Intent analysis, obligation 4 → correctly left as a Governance Dependency rather than an FR, per `project.md`'s split rule, obligation 5 → FR-P1-05-17 — all five checked and present, closing the one gap the intent statement's own history recorded as previously missed); the REQ-ENG scaffold's usability as a unit boundary for `units-generation` (2.7) (the six `src/` packages, nine stage scripts, and `NN_verb_noun.py`/`--config configs/`/`--phase` naming convention are stated with enough specificity to draw unit boundaries from directly); or the internal arithmetic of the Phase 1-applicable/not-applicable/boundary/dispositioned TA-row partition in § Success and acceptance (26 + 4 + 1 + 1 = 32, TA-01 through TA-32 fully accounted for with no gap and no overlap, verified by direct count).

### Findings — advisory pass, 2026-08-21 (sixth revision)

*(Single, non-repeating advisory pass per `review_class: advisory`, verifying the sixth revision's two named fixes — FR-P1-02-5's `TA-29` split into FR-P1-02-8, and FR-P1-05-18's criterion expansion — against the fifth-revision findings above, and hunting for the same "requirement text left broader than its narrowed criterion after a split" defect class this document has reintroduced twice before.)*

1. **Fifth-revision finding 1 (FR-P1-02-5 citing `TA-29`) is correctly closed, with no residue.** FR-P1-02-5's requirement text now reads only "The G-P1A prepared-data acceptance gate is reached with its evidence complete before any dependent work proceeds," Test column `TA-25` — the four prohibitions (silent imputation, source mixing, retrospective split redesign, station-observed mislabelling) that previously hung off this row under the withdrawn `TA-29` citation are now exclusively in the new FR-P1-02-8, Test column `` `UNTESTED` `` with the withdrawal documented inline. Checked for the specific split-defect pattern this document has shown twice before (a requirement's text left broader than its narrowed criterion): FR-P1-02-5's text names nothing FR-P1-02-8 now owns, and FR-P1-02-8's text names nothing left untested-by-omission back at FR-P1-02-5 — the four prohibitions appear in exactly one row's text and exactly one row's criterion. `TA-29` was searched across the whole document (`grep`) and appears only twice: § Success and acceptance's own "Not applicable in Phase 1" list (line 509) and FR-P1-02-8's withdrawal note — it is not cited as a live test link anywhere. `TA-25` is correctly retained on FR-P1-02-5 and is consistent with its use elsewhere (FR-P1-00-2, FR-P1-02-3, FR-P1-02-4). The untested-requirements list (§ Requirements with no testing row) was independently recomputed by reading all 40 listed IDs' own Test-column cells against the full requirement tables: every one of the 40 carries `` `UNTESTED` `` (not a test-row citation) in its own row, no listed ID is double-counted, and no row outside the list carries `` `UNTESTED` `` — the claimed "40 fully untested, 0 partial" is arithmetically correct as stated. **No finding — verified, not just re-asserted.**

2. **Major — FR-P1-05-18's fix added clauses for two of its four stated obligations, but the criterion still never tests the one obligation that actually determines whether H4/SRQ-5 confirmatory status is legitimate: that the storm-event count driving the demotion decision is sourced from GFZ Kp/Hp60 at a recorded release grade and not from provisional Dst.** (FR-P1-05-18, § FR-P1-05 table.) The requirement text carries, distinctly: (a) the audit is required G-05 evidence and performance-blind; (b) any H4/SRQ-5 demotion is legitimate only if recorded before the G-05 freeze; (c) D-13's threshold itself — "confirmatory only if December contains at least three independent §9.3 storm events," with "the count must come from GFZ Kp/Hp60 at a recorded release grade; D-11 bars any provisional-Dst-derived figure"; (d) the three regime thresholds (quiet `Kp<4`, disturbed `Kp>=4`, storm `Kp>=5`); (e) each event's −12h/+24h analysis window. The disposition table for the board finding this fix answers (`ML-10`+`VAL-5`+`VAL-6`+`TEC-10`, line 871) states the fix's own scope exactly: "FR-P1-05-18 gains §9.3's three regime thresholds and the −12h/+24h event window" — (d) and (e) only. Reading the new four-clause criterion confirms that scope precisely: clause (1) tests audit existence/timing/no-performance-figure — (a); clause (2) tests only that "any H4/SRQ-5 demotion record carries a timestamp preceding the G-05 freeze" — the *ordering* half of (b), not whether the demotion was correctly triggered; clause (3) tests that the regime thresholds are "asserted as configured values" — (d); clause (4) tests the −12h/+24h window — (e). No clause tests (c): that the count feeding the ≥3-storm-event comparison is drawn from GFZ Kp/Hp60 at a recorded release grade rather than from `.dst_summary.json`'s provisional-Dst-derived material — the exact substitution risk the requirement's own text names and the exact one this document's deferred-items table (§ Requirements with no testing row, `VAL-11` row) says is "already closed in FR-P1-05-18" by declaring the requirement's *existence* sufficient. It is not: a demotion (or non-demotion) decision built on a provisional-Dst-sourced count would satisfy clauses 1–4 exactly as written — an existing, correctly-timed, correctly-configured-threshold report — while resting on the one data-source substitution D-11 was frozen to bar. This is the same defect class the fifth-revision fix for this row was meant to close (a stated obligation with no corresponding criterion clause), reintroduced on the one clause that carries the highest consequence rather than closed across the board. Fix: add a fifth clause asserting the storm-event count's source field names GFZ Kp/Hp60 at a recorded release grade, and that a count sourced from `.dst_summary.json` or unattributed provisional Dst fails the check — the same treatment already given to clauses 3 and 4.

3. **Minor — the traceability table's per-group "Test rows" cells inconsistently name the untested sub-IDs, and the FR-P1-02 row is now the most complete case, which makes the inconsistency easier to notice, not new.** (§ Traceability, lines 797–800.) FR-P1-03-1…5's row names "FR-P1-03-5 `UNTESTED`"; FR-P1-04-1…18's row names four of its nine untested members ("-12, -13, -14, -15"); FR-P1-05-1…22's row names three of its twelve untested members ("-16, -17, -18"); FR-P1-02-1…8's row names none of its three untested members (FR-P1-02-6, FR-P1-02-7, FR-P1-02-8) even though the group grew an eighth row and a second untested member this revision. This predates the sixth revision and is not a regression from either fix, so it does not weigh on the verdict for the two fixes under review, but a reader relying on the traceability table alone (rather than cross-checking § Requirements with no testing row, as this pass did) would read the FR-P1-02 group as more fully tested than it is. Fix: either make every group row name its full untested subset, or drop the partial parenthetical convention everywhere and rely solely on § Requirements with no testing row as the single source of truth it already claims to be.
