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

**Still open.** Vision §6.6 and TE §6.1 remain in textual conflict for Phase 1 —
D-17 lets work proceed without resolving it, and correcting the source sentences
runs through Vision §15.2. Four support thresholds stay `TBD — freeze gate` by
design. `GOV-2026-08-20-RA-01`'s MAJOR and MINOR sets are unworked, as are its
`TEC-05` residue (TE §16.1's four sub-gates) and its `ML-01` residue (the
24-hour window asserted untuned in `experiment.yaml`). D-1's IGS site-log
validation limitation is unchanged. The governance verdict stands at `FAIL`
until the board is rerun against this revision, and **no pytest run has occurred**
— no Python interpreter is available in this environment.

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
| Governance board reports GOV-2026-08-13-IC-01/-02, GOV-2026-08-15-FE-01/-02, GOV-2026-08-15-AH-01, GOV-2026-08-21-RA-01 | `governance/reviews/` | § Known defects in the authority documents |
| Practices-discovery board findings (`DATA-*`, `TEC-*`, `ML-*`, `BENCH-*`, `IMPL-07`, `VAL-05`, `CHAIR-02`, `GOV-22`, `GOV-25`) | **Report not persisted.** Substance carried in `aidlc/spaces/default/memory/project.md`, `team.md` and `team-practices.md`; see § Sources **[board]** | Cited inline with the persisted rule text, finding ID kept as a provenance label |
| D-1 … D-17 scientific and governance decisions | `evidence/DECISIONS.md` | Cited inline as `[D-n]`. Added 2026-08-21: **D-12** §6.1B coverage minimum, **D-13** H4/SRQ-5 demotion threshold, **D-14** scientific fixture window, **D-15** locked-month custody relocation, **D-16** hourly aggregation statistic, **D-17** Phase 1 target-row contract, plus the **D-1 addendum** closing its countersignature under the recorded delegation |
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

**Type and complexity.** New build on a partially populated workspace
(two scripts, one notebook, twelve months of derived audit evidence, no
`tests/`, no `src/`, no `configs/`, no `pyproject.toml`). System-wide scope,
complex domain, heavy external governance. Depth: Comprehensive.

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
| REQ-ENG-3 | Python 3.11 with exact pins installs on **both** Kaggle and local; no third platform is used | Lock file, install log and environment hash from both platforms | [TE §8.1, §9.1] [TC-03c, TC-03d] | TA-03, TA-26 |
| REQ-ENG-4 | The **18** mandated test modules exist under `tests/` — the 17 enumerated in §12 plus `test_acquisition_window.py`, added to §12's tree by the amendment **countersigned 2026-08-16** (`governance/COUNTERSIGNATURE_REQUEST_2026-08-16.md` item 1) — plus the two fixture directories `tests/fixtures/plumbing_7day/` and `tests/fixtures/scientific_1month/` | Each named module is present and collectible, `test_acquisition_window.py` included, since FR-P1-01-5 and FR-WS-3 discharge onto it; fixture assertion data lives in `fixture_manifest.yaml`, never hardcoded in test bodies | [TE §12, §15.2] [practices] [countersigned 2026-08-16] | TA-09 — bounded, see § Known defects row 8 |
| REQ-ENG-5 | Every hard rule in `discovered-rules.md` has a **negative-path** test proving the violation is caught — not only a happy-path test | For each such rule, a test exists that fails when the violation is injected | [practices] [Vision §7.1] | WS-10, TA-07, TA-08, TA-12, TA-27 |
| REQ-ENG-6 | Git is initialized before any further acquisition work, on `main`, with a credential/secret deny-list in `.gitignore` (`.env`, `*.key`, `kaggle.json`, `.netrc`, `credentials*`) present **before the first commit** | `git log` exists; a secret scan over the tree and history returns clean | [practices] [TE §10] [NFR-SEC-01] | TA-22 |
| REQ-ENG-7 | Each freeze gate (G-05, G-06, each phase transition) is tagged, and any commit changing a scientific constant or a governed config cites its D-number | Tag list covers the signed gates; commit-message audit shows a D-number on every governed change | [practices] | `UNTESTED` |
| REQ-ENG-8 | The two existing scripts and the coverage notebook migrate onto the §12 structure: `--config configs/` (and `--phase 1|2` where applicable), a numbered `NN_verb_noun.py` position, the triplicated SHA-256 helper consolidated into `src/data/release.py`, the notebook's inline station coordinates and coordinate-to-cell rule moved into `configs/data.yaml` and `src/data/registry.py` **only after** those current values are frozen under a D-number | Migration complete; `grep` shows no scientific constant remaining in source or notebook; the freeze D-number exists and precedes the move | [practices] [TE §12, §14] [TC-03e] [Q11] | TA-16 |
| REQ-ENG-10 | **Per-run environment lock.** Every run captures TE §13.1's eight items: the `requirements.txt` hash and a per-run `pip freeze`; Python, OS, CPU and key library versions; the code commit; configuration snapshot hashes for all four configs; input dataset and manifest versions; the platform; and any known nondeterministic operations | A registry row exists carrying all eight fields, populated — not `unavailable`; a run that captures none of them fails the check rather than completing silently. This is the requirement the thirteen existing runs are recorded as violating (`evidence/experiment_registry.md` § Acquisition runs: the §13.1 list "was not captured at the time and cannot be reconstructed"), so it binds from the next run forward | [TE §13.1] [NFR-REP-01] [NFR-AUD-01] | `UNTESTED` — no WS/TA row covers the §13.1 capture list; candidate new TA row via Vision §15.2 |
| REQ-ENG-11 | **Environment and CPU preflight report.** `environment_and_cpu_preflight_report` is produced, carrying TE §9.2's four elements — install-from-pins on **both** platforms, a completed walking-skeleton run, and measured CPU runtime, peak RAM and storage — and the run stays inside TE §9.3's **10.0 GB** hard planning envelope. TC-03, TC-03a (10 GB), TC-03b (GPU not required) and TC-03g are all `binding: hard` and are cited here rather than left out of § Constraints | The report exists and is the artifact G-07 accepts; each of the four elements is present with a measured value, not an assertion; recorded storage use is at or below 10.0 GB | [TE §9.2, §9.3] [TC-03, TC-03a, TC-03b, TC-03g] | TA-17, TA-26 |
| REQ-ENG-9 | `audit_ec1_drivers.py`'s exit-code gap is closed: a completeness shortfall is recorded as a machine-readable field in the output manifest, an integrity violation terminates the run naming the file and the violated expectation | Injecting a missing month yields a non-silent, machine-readable record; injecting a hash mismatch yields a non-zero exit with a naming message | [practices] `scripts/audit_ec1_drivers.py:184` | `UNTESTED` |

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
| FR-P1-01-2 | Every retrieved file records provider, permanent citation, **full provider filename including its version suffix** (e.g. `g.002` vs `g.003`), retrieval date and SHA-256; a mismatch against a previously recorded suffix is surfaced, never silently accepted | `request_manifest.json` carries all five fields per provider file; an injected suffix mismatch raises | [TE §13.3] [practices § Walking Skeleton, § Deployment; origin DATA-07, unpersisted] | TA-15 |
| FR-P1-01-3 | The `madrigalWeb` client version is pinned and recorded — never `"unknown"` — and the exact web-service interface is recorded alongside it. **This is the acceptance evidence that closes DATA-03** (finding text unpersisted; the obligation it states — a recorded, pinned `madrigalWeb` version, never `"unknown"` — is verifiable against `evidence/*/request_manifest.json` independently of the report). | No `request_manifest.json` written after this requirement takes effect contains `madrigalWeb_version: "unknown"`; the pin appears in the lock file | [TE §8.1, §10, §13.3] [evidence fact 5] [NFR-REP-01] | TA-03, TA-15 |
| FR-P1-01-4 | Native provider byte streams are retained, and `sha256_manifest.json` hashes **one entry per provider file**, not only the four derived artifacts. **This is the acceptance evidence that closes DATA-04** (finding text unpersisted; the obligation it states — provider byte streams retained and hashed per file, not only the four derived artifacts — is verifiable against the manifests independently of the report). | `find` locates provider files for every acquired month; each month's manifest hash count equals its provider-file count plus its derived-artifact count; the twelve pre-TC-06 months are re-verified under the new test suite rather than re-acquired from scratch | [TE §10, §13.3] [evidence fact 6] | TA-04, TA-15 |
| FR-P1-01-5 | Acquisition membership is derived from **record timestamps**, never from an acquisition directory name or filename; every per-month statistic excludes out-of-month and out-of-year records | `tests/test_acquisition_window.py` passes, including the case that produced the original defect (December records filed under `audit_evidence_2022-01/`) | [project.md § Forbidden] [`evidence/CORRECTION_2026-08-16_acquisition_window.md`] | `UNTESTED` — no WS/TA row covers the acquisition-window predicate; see § Requirements with no testing row |
| FR-P1-01-6 | Driver acquisition follows the frozen contract: Kp/ap3 and Hp60/ap60 from GFZ, hourly Dst from Kyoto WDC at a **single recorded release grade** for all of 2022, observed (not 1-AU-adjusted) F10.7 from Canada's Solar Radio Monitoring Program. SSN is absent | Each series carries its source, release grade and retrieval record; a grep confirms SSN is absent from the codebase | [intent driver contract] [D-10.1, D-10.3] [Vision §6] | TA-08 |
| FR-P1-01-7 | The Canadian F10.7 archive is audited from 2022-03-18 onward for the documented month-long outage; exact missing dates, qualifiers and any reconstructed values are reported. **No imputation, substitution or reconstruction occurs until the measured gap is recorded and governed.** | The audit report exists with exact dates; no filled value exists in the series before the governing decision | [intent obligation 2] [TC-20] | `UNTESTED` |
| FR-P1-01-8 | No driver is backfilled from future final or definitive archived index values; the **release status** of every driver is recorded, not only its lag | Each driver's manifest carries a release-status field; a reanalysed-value check passes | [TE §10] [project.md § Forbidden, "NEVER backfill a driver from future final or definitive archived index values"; origin TEC-04, unpersisted] | `UNTESTED` |
| FR-P1-01-9 | Data gaps are stored as explicit `NaN` at acquisition time; no interpolation, smoothing or fill occurs at acquisition | An injected gap survives acquisition as `NaN` | [D-5, D-10.2] | `UNTESTED` |
| FR-P1-01-10 | Credentials and secrets are supplied through platform secret stores or environment configuration excluded from version control, and appear in no notebook, source file, configuration snapshot, log or registry note | Secret scan over tree, history and artifacts returns clean | [TE §10] [NFR-SEC-01] | TA-22 |

### FR-P1-02 — Inventory, registry and the G-P1A coverage gate

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-02-1 | Station coordinates and the coordinate-to-cell rule are validated against the **official IGS site logs** before being treated as final, and live in `configs/data.yaml` / `src/data/registry.py` rather than in a notebook literal | Registry values match the site logs; header cross-check shows no unresolved conflict | [TE §7.0 P1-02] [§18.2 forbidden-choice items] | WS-01 — retained in Phase 1 as a named exception, see § Known defects row 9; TA-04 |
| FR-P1-02-2 | Schema validation covers parameter names, units, fill values, UTC cadence and duplicates for the prepared product | The prepared-data schema report exists and passes | [TE §7.0 P1-02] | TA-04 |
| FR-P1-02-3 | File, cell, day, month and common-timestamp coverage is audited **including December**, without inspecting any model performance. **An access-log row with `locked_test_accessed = true` is written BEFORE any operation that reads a December 2022 record** — the scope is *access*, unqualified, so it covers derived-artifact merges, re-derivations, corrections, coverage recounts and schema validations, not only a model execution | The coverage report covers all twelve months; no performance figure appears in it or in its execution log; every December read has a preceding access-log row, and a read with no prior row fails rather than proceeding | [TE §7.0 P1-02] [Vision §8.3, "access" unqualified] [origin VAL-2, GOV-2026-08-20-RA-01] | WS-18, TA-25 |
| FR-P1-02-4 | **G-P1A acceptance is decided against Vision §6.1B's numerical coverage minimum, frozen 2026-08-21 as D-12:** at least **90% usable hourly coverage per station per month**, as a hard gate, **together with** D-2's day rule (≥95% of calendar days per month, 100% of December days). Both must pass; neither substitutes for the other. §6.12's exception-plus-claim-limitation path does not apply at G-P1A | The G-P1A decision record cites D-12's 90% hourly figure and D-2's day rule, reports the measured per-station hourly and day coverage for every month, and never an unattributed number. Measured in-month hourly coverage as at 2026-08-21 (straddle days excluded): ARUC 99.2–100.0%, BSHM 99.3–100.0%, NICO 93.2–98.9% across the nine cached non-December months — every station-month clears 90% | [Vision §6.1B as amended] [D-12] [D-2] [Q3] | TA-25 |
| FR-P1-02-5 | Silent imputation, source mixing, retrospective split redesign after model performance is viewed, and labelling a map value as station-observed VTEC are each prohibited at this gate | Each prohibited action has an injection test that fails the pipeline | [Vision §6.1B] | TA-25, TA-29 |

| FR-P1-02-6 | **Locked-test artifacts reside only under a restricted path until G-05 is complete.** TE §12 states two obligations in one sentence — restricted paths **and** the `locked_test_accessed` registry flag — and only the flag half was previously decomposed. Any file containing a December 2022 target value is a locked-test artifact, the merged year artifact and every `superseded_*` snapshot included | **No file under `evidence/` at any depth, outside `evidence/locked_test_restricted/`, contains a record whose observation date falls in December 2022.** Enforced by `tests/test_acquisition_window.py::test_locked_month_values_exist_only_under_the_restricted_path`. **Satisfied 2026-08-21 by the relocation recorded in D-15.** It was written while failing, against four unrestricted holders — 21,258 December rows each in `audit_evidence_2022-12/`, `audit_evidence_2022-FULL/` and `audit_evidence_2022-12/superseded_2026-08-16/`, plus 743 in `audit_evidence_2022-01/superseded_2026-08-16/`, roughly 58 MB. All are now under `evidence/locked_test_restricted/`; the criterion is retained as a regression guard, so any future run, merge or correction that re-creates a December-bearing artifact outside the restricted root turns it red again. **The restricted path is a governance boundary, not an access control** — no filesystem permission, encryption or ACL is involved, and none is claimed; what it buys is one declared location, a machine-checkable invariant, and an unambiguous access-log trigger | [TE §12] [origin VAL-1, GOV-2026-08-20-RA-01, Validation Auditor veto] | `UNTESTED` in §16/§19 — no WS/TA row covers at-rest location; enforced by the project test named above |

### FR-P1-03 — Standardize the prepared hourly target

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-03-1 | Provider values are preserved; only documented QC, UTC normalization, cell selection and the hourly aggregation are applied. **The hourly aggregation statistic is frozen as D-16 (2026-08-21): the median of the valid provider VTEC samples inside the UTC hour for the station's frozen cell.** Zenith-weighted aggregation is a separately declared sensitivity, authorised only before training and only if the data supports it — and it is **deferred as not computable**, because the Phase 1 product carries five columns (`ut1_unix`, `gdlat`, `glon`, `tec`, `dtec`) with no elevation, zenith angle or satellite identifier. **Nothing is substituted** for unavailable satellite-level or zenith information. TE §18.2 lists the statistic as a Student + Supervisor forbidden choice; exercised under the recorded authority delegation | A value-level diff against the provider bytes shows only the documented transformations, **and** the aggregation statistic cited by the run resolves to **D-16** rather than to a default. An earlier revision of this row asserted "the frozen hourly aggregation" when no decision had frozen it; that false statement was corrected first, and the freeze recorded second, as two explicit stages — GOV-2026-08-21-RA-01 Rec 21, option C | [TE §7.0 P1-03] [Vision §6.6] [TE §18.2] [origin DATA-05 and TEC-04, GOV-2026-08-20-RA-01] | TA-04 |
| FR-P1-03-2 | Phase 1 never estimates DCB or STEC, never maps `los` observations, and never silently interpolates a missing cell. **Import limb:** `src/gnss/rinex.py`, `src/gnss/calibration.py` **and every raw-processing adapter** are inaccessible from the Phase 1 target-build command — the §12 tree's `src/gnss/target.py` and `src/gnss/verification.py` are raw-processing adapters and are named here explicitly, having previously fallen outside every stated prohibition. **Produced-field limb, separately checkable:** Phase 1 must not produce DCB, STEC, mapping, **satellite** or **arc** fields | Two independent pass/fail results, not one: (a) `tests/test_phase_boundary.py` fails when an import of any named raw module is introduced, demonstrated for each; (b) the same suite rejects a Phase 1 artifact carrying a DCB, STEC, mapping, satellite or arc field. Neither result substitutes for the other | [TE §7.0 hard prohibition, quoted in full] [NFR-PHASE-01] [origin IMPL-2, GOV-2026-08-20-RA-01] | TA-27 |
| FR-P1-03-3 | Every dataset, prediction, mask and comparison is stamped with `phase_id`, `source_id` and `target_definition_id` | Schema test asserts all three on every such artifact | [TE §13] [NFR-TDEF-01] | TA-15 |
| FR-P1-03-4 | The Phase 1 target is labelled **location-sampled gridded VTEC**, never receiver-specific station-observed VTEC, everywhere it is described | A claims-checklist review over every artifact and figure caption finds no mislabelling | [Vision §6.6] [NFR-TDEF-01] | TA-15 |
| FR-P1-03-5 | **The Phase 1 target row carries exactly the contract frozen as D-17**, defined from the product that exists rather than from TE §6.1's Phase 2-shaped list: `interval_start_utc`; `station_id`; `cell_gdlat`/`cell_glon`; `cell_lat_bounds`/`cell_lon_bounds` (half-open, D-1); `vtec_tecu` (median, D-16); `valid_observation_count`; `within_hour_spread_tecu`; `largest_internal_gap_s`; `provider_dtec_summary`; `aggregation_config_id`; `target_valid`; `phase_id`/`source_id`/`target_definition_id`. **Excluded and never substituted:** `valid_satellite_count`, any per-satellite or per-IPP quantity, zenith angle or weight, elevation, DCB, STEC, mapping output, arc or slip statistics — none is derivable from a five-column gridded product (`ut1_unix`, `gdlat`, `glon`, `tec`, `dtec`, audited 2026-08-21 across all twelve request manifests), and TE §7.0 requires the phase-boundary test to reject a satellite field. `processor_qc_flags` carries **aggregation** flags only; the package, DCB, arc, elevation, slip and mapping classes are Phase 2 and are recorded not-applicable rather than emitted empty | A schema test asserts exactly D-17's field set — a row carrying an excluded field fails, and a row missing a required field fails. All four support values are **frozen as D-19 (2026-08-21)** from measured January–November distributions, December excluded by construction: `valid_observation_count` minimum **3** (keeps 95.24% of 23,709 deduplicated cell-hours), `within_hour_spread_tecu` statistic **range (max − min)** with a **10.0 TECU** threshold (p99 = 9.616), `largest_internal_gap_s` maximum **1800 s** (keeps 93.39%; median gap 300 s confirms the 5-minute cadence), `provider_dtec_summary` statistic **median of `dtec`** with a **1.5 TECU** flag (p99 = 1.314). They are recorded in `data.yaml` with their D-19 provenance rather than as `TBD`, so the zero-TBD preflight (REQ-ENG-2, FR-WS-7) now passes on this component. **TE §6.1's provisional `valid_observation_count >= 20` is superseded for Phase 1 because it retains zero cell-hours** — the deduplicated maximum is 12, the product's native cadence being 5-minutely. `valid_satellite_count`'s provisional minimum of 4 remains **not applicable** in Phase 1 rather than open. `target_support_threshold_report` is the evidence artifact | [D-17] [D-16] [D-1] [TE §6.1] [Vision §6.6] [TE §18.2 Q-12] [EV-06] [origin TEC-03 and DATA-04, GOV-2026-08-20-RA-01] | `UNTESTED` in §16/§19 — the only field-contract row, WS-05, is deferred to G-P3A by FR-WS-4; enforced by the D-17 schema test and `tests/test_phase_boundary.py` |

### FR-P1-04 — External products, features, splits, masks

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-04-1 | No `iri_*` field, IRI-derived residual, or IRI-computed value reaches ML training or inference; IRI and GIM join **only at evaluation time** on the frozen comparison-wide mask; no module under `src/features/` or `src/models/` imports `src/external/iri.py` or `src/external/gim.py`, directly or transitively | `tests/test_iri_denial.py` **fails** on deliberate `iri_*` injection, and the import-boundary check passes | [Vision §7.1] [NFR-IRI-01] [TE §12] | WS-10, TA-07 |
| FR-P1-04-2 | Every predictor is lagged to its actual availability timestamp: Kp/ap3 ≥ 3 h, Hp60/ap60 ≥ 1 h, F10.7 at the previous-day observed value with a **trailing** (never centered) 81-day mean; Dst is diagnostic/hindcast-only; SSN is absent | The availability matrix asserts actual lag ≥ declared safe lag for every primary feature; a centered-mean injection fails | [Vision §6] [TE §6.2] [D-10.3] [TC-10, TC-11] | WS-11, TA-08 |
| FR-P1-04-3 | Missing external driver values carry forward at most 3 hours; beyond that the row is excluded | An injected 4-hour gap excludes the row | [TE §6.2] [TC-09] | WS-11 |
| FR-P1-04-4 | Driver series are time-indexed only — one value per epoch, identical across all three cells; a join never implies a per-cell measurement | Schema test asserts a single value per epoch across cells | [TC-12] | `UNTESTED` |
| FR-P1-04-5 | Folds are exact fixed calendar boundaries (F1: Jan–Mar/Apr; F2: Jan–Jun/Jul; F3: Jan–Sep/Oct; F4: Jan–Oct/Nov; December locked), each with a 24-hour embargo; no random or shuffled cross-validation; the first 24 h are excluded and counted. **The partition list also carries `Final refit: 1 Jan – 30 Nov`, and November enters the final refit only after all features, hyperparameters, masks, seeds, thresholds and analysis rules are frozen** — previously omitted, which left Vision §8.1's rule that each target timestamp belongs to exactly one partition with no list to check November against | No window crosses a boundary; the split manifest records the excluded count and enumerates all five partitions; a refit executed before the freeze fails rather than proceeding | [TE §7.1] [Vision §8.2, §8.1] [origin ML-02, GOV-2026-08-20-RA-01] | WS-12, TA-11 |
| FR-P1-04-6 | Any scaling or standardization is fitted on training partitions only, per fold, never on the full dataset | A full-dataset fit injected into the pipeline is caught | [Vision §6.4] [NFR-LEAK-01] | TA-11 |
| FR-P1-04-7 | A **single comparison-wide intersection mask** is computed once per comparison set and used for every model-versus-baseline comparison; masks carry stable IDs and reported row counts; no pairwise or model-specific mask is produced | Mask manifest shows one mask per comparison set with a stable ID; a pairwise mask attempt fails | [Vision glossary] [NFR-FAIR-01] [TC-16] | WS-16, TA-11 |
| FR-P1-04-8 | The flattened matrix and the sequence tensor for a given feature-set ID contain the same underlying window values | Matched-window assertion passes | [TE §16 WS-13] | WS-13, TA-11 |
| FR-P1-04-9 | The IRI benchmark and GIM comparator sample alignment passes; the IRI ceiling and drivers are recorded; the **`gim_network_overlap_flag` audit is present and its result disclosed**, and no independence claim precedes the audit. The IRI benchmark (**B-01**) and the GIM comparator (**C-01**) are represented in the model/config inventory and are labelled **generated, not trained** | Tolerance report, config snapshot and overlap audit all exist; the flag value appears wherever GIM is compared; the model/config inventory shows B-01 and C-01 present and marked generated-not-trained, never fitted | [TE §5.2] [Vision §6.10] [TC-08] [TE §19 TA-12] | WS-09, TA-12 |
| FR-P1-04-10 | Raw longitude never enters as a predictor; longitude enters only through `lst_sin` and `lst_cos` | Feature manifest contains no raw-longitude column | [TE §7.2] | `UNTESTED` |
| FR-P1-04-11 | Every dataset release records version, source manifest, SHA-256 hashes, schema, row counts, exclusions and fold/mask identifiers, and is write-protected or stored under a new version rather than overwritten | `tests/test_release_hashes.py` mutation-protection test passes | [TE §13.3] | TA-15 |
| FR-P1-04-12 | **The permitted ML input space is closed.** The feature set is exactly the TE §6.2 dictionary — no field outside that table, and no derived tensor built from one, enters training or inference. Window length is one frozen value per feature-set ID, shared across all model families, and **the primary history window is 24 hours — a frozen constant, not a tuned hyperparameter** (Vision §8.1: "History length is not a tuned hyperparameter") | A field absent from the §6.2 dictionary fails feature construction rather than passing silently; the feature manifest enumerates only §6.2 fields; `experiment.yaml`'s window length **equals 24 and appears in no grid**, so a run that tunes it fails rather than proceeding; `ABL-HIST48` is the only sanctioned 48-hour path and runs after the primary configuration is frozen. **Concrete case named:** D-4 decided to acquire `kp, dst, f10.7, ap3` alongside the target, which would have placed driver columns of unrecorded release grade inside the Phase 1 target files — `dst` among them, where Dst is diagnostic-only. D-17 records that those four were **never actually requested** (the executed manifests take five columns), so the risk is closed by fact rather than by rule; the closed-set assertion is what keeps it closed if a re-acquisition changes the parameter list | [TE §6.2 "This table is the complete permitted ML input space"] [TE §6.4] | `UNTESTED` — dictionary closure has no WS/TA row; candidate new TA row via Vision §15.2 |
| FR-P1-04-13 | **Target-derived lag contract.** `vtec_lag_1h/2h/3h/24h` are strictly causal at exact lags `[1,2,3,24]`; `vtec_seq_24` is a 24-step causal sequence excluded when incomplete; **carry-forward is prohibited for target-derived lags and the window is excluded instead** — the opposite of FR-P1-04-3's ≤ 3 h allowance, which is scoped to external drivers only and must never be read as reaching `vtec_lag_*`; the pooled model carries `station_onehot_ARUC/BSHM/NICO` plus verified `station_lat`, and an unresolved station registry blocks their use | An injected carried-forward `vtec_lag_*` value fails; an incomplete window is excluded and counted; the feature manifest carries the exact lag set, the 24-step sequence, the station one-hot columns and verified latitude | [TE §6.2 dictionary rows `vtec_lag_*`, `vtec_seq_24`, `station_onehot_*`, `station_lat`] [TE §2.1 model-granularity row, Q-05] [NFR-LEAK-01] | `UNTESTED` — no WS/TA row covers the target-lag carry-forward prohibition; candidate new TA row via Vision §15.2 |

| FR-P1-04-14 | **Vision §8.7's selection and refit protocol.** Configurations are selected on the **mean per-fold skill score across F1–F4**. Raw mean RMSE is **not** used; row-count weighting is **not** used. The declared baseline per track is named in configuration **before tuning begins**. Where mean skill differs by less than **1%**, the **simpler** configuration is selected. The selected configuration is then refit on January–November **without changing any hyperparameter** | Two mechanical comparisons: the selection record's criterion equals the criterion configured before tuning, and the refit hyperparameters equal the selected ones. A selection made on raw mean RMSE or row-count weighting fails; a refit that alters any hyperparameter fails; a run with no pre-tuning declared baseline fails | [Vision §8.7] [Vision §8.2 Final-refit partition] [TE §18.2, which makes the tuning criterion and refit rule human-owned] [origin ML-02] | `UNTESTED` — no WS/TA row covers the selection criterion; candidate new TA row via Vision §15.2 |
| FR-P1-04-15 | **The IRI-2016 benchmark is validated before generation, and generation is blocked if validation fails.** Per Vision §6.11, the `iri_implementation_validation_report` records: the pinned package/build with its exact version or commit; all model switches and the topside option; **the altitude ceiling stated explicitly as 2000 km**; units and output extraction; the coordinate, time, solar and geomagnetic driver inputs **with confirmation that no driver is future-centered or unavailable at target time**; and five to ten samples spanning sites, day and night, quiet and disturbed, validated against the **official IRI interface** within a tolerance **predeclared before the comparison runs**. The 26,000-call workload is timed, and the `iri2016` Fortran build re-establishes from pins on a cold session (TC-04) | The report exists with its sample tolerance table; **the benchmark's own drivers appear as rows in the same frozen availability matrix used for ML features**, each carrying observation timestamp, publication timestamp, release status and safe lag; a validation failure **blocks** benchmark generation rather than warning (TE §10); the measured 26,000-call runtime is recorded | [Vision §6.11] [TE §10] [TE §6.3] [TC-04] [EV-10] [origin TEC-01, TEC-02 and BENCH-02] | `UNTESTED` — no WS/TA row covers benchmark validation; `test_feature_availability.py` asserts over the ML feature table and B-01 is not a feature |

### FR-P1-05 — Models, prediction, evaluation

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-05-1 | The model set is persistence (M-01), 24-hour seasonal persistence (M-02), fitted station×month×hour climatology trained on training folds only (M-03), ridge (M-04), Random Forest (M-05) and the compact LSTM (M-06); **residual and GRU modules are absent from the codebase**; TensorFlow/Keras is the only NN stack | All required model IDs are present in modules and configs; grep evidence shows residual and GRU absent, and PyTorch absent | [intent model set] [TE §8.3] | WS-14, TA-12, TA-26 |
| FR-P1-05-2 | M-06 trains and restores its lowest-validation-RMSE checkpoint; the **three-seed element-wise mean** from `seeds.yaml` is the confirmatory prediction; no seed is selected on validation or after seeing December | Checkpoint-restore and seed tests pass; the seeds are fixed in config, not chosen at runtime | [NFR-DET-01] [TC-21] [Vision §8.6] | WS-15, TA-13 |
| FR-P1-05-3 | No Random Forest importance score adds, removes or ranks a feature into the production feature set; RF importance is saved only as a non-authoritative diagnostic figure | The feature manifest's provenance shows no importance-derived selection | [Vision §6.4] [TE §6.4] | `UNTESTED` |
| FR-P1-05-4 | Tuning uses **January–November only**; model selection, feature selection, thresholds and hyperparameters are never informed by December. The trigger is December being **seen**, not the locked test being opened | The tuning record shows no December-derived input, including after the required pre-G-05 coverage audit | [Vision §8.3] [project.md § Forbidden, "NEVER let December inform model selection, feature selection, thresholds or hyperparameters"; origin ML-02, unpersisted] | WS-18 |
| FR-P1-05-5 | Hyperparameter grids are exact and committed to configuration **before G-05**, and no grid range changes after December is seen; no second 2022 test period is selected after results are observed | `experiment.yaml` grids are frozen at the G-05 commit; a post-G-05 grid diff is empty | [Vision §8.7, §8.10] [TE §7.1] | `UNTESTED` |
| FR-P1-05-6 | Ablations are **predeclared** as named runs registered in `experiment.yaml` with a run ID, executed on the frozen January–November folds with identical folds, masks and tuning budget. TE §7.2's registry is **five** named ablations, and each must hold a pre-freeze registry row: **`ABL-NODOY`**, **`ABL-DIFF`**, **`ABL-NOSW`**, **`ABL-HIST48`**, **`ABL-ZENITH`**. `ABL-DIFF` inverse-transforms to absolute TECU before any metric; `ABL-HIST48` runs only after the primary configuration is frozen. **Phase call on `ABL-ZENITH`:** it varies the hourly aggregation of the target (zenith-weighted versus IPP median, Vision §6.6), a choice that does not exist on the Phase 1 location-sampled gridded target, so it is **deferred to Phase 2** and registered there — recorded here rather than left as an omission | All five IDs have a pre-freeze registry row, or in `ABL-ZENITH`'s case a recorded phase deferral; a missing required ablation fails the check rather than passing unnoticed; no ablation is registered after results are seen | [TE §7.2] [TE §6.2 "subject to the required no-DOY ablation"] | `UNTESTED` |
| FR-P1-05-7 | The confirmatory estimand is the **paired loss differential — mean within-station difference of squared errors, benchmark minus model — with equal-station weighting**, positive favouring the model, reported at 95% | The evaluation module computes exactly this quantity; percentage reduction is computed only as a labelled derived summary | [Vision §2.3] [TE §1.3] | `UNTESTED` |
| FR-P1-05-8 | Uncertainty uses the **vector time-block bootstrap**: 24-hour blocks carrying all three stations together, 10,000 replicates, seed 20221201, 95% CI, with the cross-station paired-error correlation reported. A within-station or naive bootstrap is not substituted | The bootstrap reproduces exactly from seed 20221201 on synthetic correlated data; a 48-hour sensitivity is produced | [TE §13.6] [TC-19] | WS-17, TA-14 |
| FR-P1-05-9 | The three mandatory difficulty controls (M-01, M-02, M-03) are co-reported **in the primary results table**, never in an appendix; any baseline that beats the LSTM appears in that table **and** in the abstract-level conclusion | The primary results table contains all three controls plus the IRI comparison; a review of the abstract confirms disclosure | [Vision §2.4 binding honesty rule] [PC-03, PC-04] | TA-20 |
| FR-P1-05-10 | The target uncertainty budget is produced and reported **adjacent to** the primary result; a top-1%-absolute-error-removed sensitivity is reported | `target_uncertainty_budget.json` exists and appears beside the primary result | [NFR-DQ-01] [intent reporting] | TA-19 |
| FR-P1-05-11 | The required prediction, residual, target-support and quality **plots** exist, each carrying its source-data IDs | Plot manifest lists every required plot with its source-data IDs | [TE §16 WS-19] | WS-19 |
| FR-P1-05-16 | Required reporting **breakdowns** are produced: per-cell metrics at +1 h, equal-station macro-average as the headline, pooled row-weighted as supplementary, quiet/disturbed/storm regime split, **observation-quality strata computed from D-17's measured-available fields only — bins over `valid_observation_count`, `within_hour_spread_tecu` and `provider_dtec_summary`; no stratum is defined on satellite count, elevation or zenith angle**, none of which exists on the five-column Phase 1 product — daily error and four local-solar-time diagnostic bins; December regime results are **descriptive only** unless at least three independent storm events occur (the same measured quantity D-13 uses) | Each named breakdown exists in the results artifact, each computed from a field the target declares; the storm-claim guard is enforced | [intent reporting] [Vision §11] | `UNTESTED` — WS-19 tests plot existence only and reaches no breakdown and not the storm guard; split out of FR-P1-05-11 per GOV-2026-08-21-RA-01 Rec 11 |
| FR-P1-05-12 | The **locked-test guard** blocks December performance execution before G-05 is signed, records every access, and sets `locked_test_accessed = true` in the experiment registry; predictions are generated and written **once**, and hashed **before** any metric is computed | `tests/test_locked_test_guard.py` blocks a pre-G-05 December run; the access log row is written **before** the read, not after it, for every December access including non-execution reads; and the prediction hash precedes the metrics. An access recorded after the fact fails the ordering check rather than satisfying it | [Vision §5.3, §8.3 — "access" unqualified] [OC-03] [origin VAL-2] | WS-18, TA-18 |
| FR-P1-05-13 | The experiment registry is operational, append-safe and atomic; failed and aborted runs remain visible with status and reason; no entry is deleted, overwritten or silently re-run. **Its schema is TE §13.4's twenty columns**: `run_id`, `started_at_utc`, `completed_at_utc`, `status`, `code_commit`, `environment_lock_hash`, `platform`, `dataset_version`, `fold_id`, `mask_id`, `feature_set_id`, `model_id`, `hyperparameters_json`, `seed`, `validation_metric_name`, `validation_metric_value`, `artifact_manifest_path`, `prediction_hash`, `locked_test_accessed`, `notes` | Registry tests pass, including a failed-run sample that remains visible; a schema assertion confirms all twenty columns exist and that `code_commit` and `environment_lock_hash` are populated on every row | [NFR-AUD-01] [TE §13.4] | TA-10 |
| FR-P1-05-14 | Any test-driven change made to the pipeline **after** locked-test access is labelled exploratory | Every post-access change carries the exploratory label in the registry | [Vision §8.3] | `UNTESTED` |
| FR-P1-05-15 | No practical-relevance threshold is introduced, changed or reinterpreted after December is opened | The threshold record's timestamp precedes G-06 | [Vision §5.4] [PC-09] | `UNTESTED` |
| FR-P1-05-17 | **Evaluation code is authored, reviewed and frozen as part of the G-05 set before December 2022 is opened.** No evaluation code exists at intent time; it is authored inside this initiative | The evaluation modules exist, carry a recorded review, and their hashes sit inside the G-05 frozen config bundle; the freeze timestamp precedes any December access recorded under FR-P1-05-12 | [intent § Scoped Verification Obligations row 5] [Vision §13.1 G-05] | `UNTESTED` — no WS/TA row covers evaluation-code completeness, review or freeze |
| FR-P1-05-19 | **The plasmaspheric-offset disclosure accompanies every interpretation of the primary comparison.** Vision §6.11: GNSS-derived TEC extends farther into the plasmasphere than a 2000 km ceiling, so reported IRI–GNSS discrepancies *"contain a physical, structured, time-varying component that is not forecast error"* and this *"must be disclosed wherever the primary comparison is interpreted"*. Vision §5.1 SRQ-9 asks this question directly | A claims-checklist row asserts the disclosure text is present at each interpretation point — the primary results-table caption, the abstract-level conclusion, and the limitations section. Absent it, a structured physical offset reads as model skill in the headline number | [Vision §6.11] [Vision §5.1 SRQ-9] [origin TEC-01, TEC-02, BENCH-02] | `UNTESTED` — no WS/TA row covers the disclosure; candidate new TA row via Vision §15.2 |
| FR-P1-05-18 | **The December regime-count audit is required G-05 evidence, and the H4 demotion is legitimate only if recorded before the freeze.** The audit is performance-blind (as FR-P1-02-3) and produces the `December regime-count audit report` that Vision §13.1 names as a G-05 input. If it shows fewer disturbed hours than the supervisor-approved minimum, H4 and secondary research question 5 are predeclared **validation-fold-only** and reported as such. **That threshold is frozen as D-13 (2026-08-21): H4 and SRQ-5 stay confirmatory only if December contains at least three independent storm events under Vision §9.3's unchanged definitions — a contiguous interval of Kp>=5, with independence at >=24 h of Kp<4. No separate disturbed-hour count exists, by design: the threshold reuses the storm-event rule §9.3 already freezes, so H4's fate and the general storm-claim rule turn on one measured quantity. The count must come from GFZ Kp/Hp60 at a recorded release grade; D-11 bars any provisional-Dst-derived figure** | The audit report exists, is registered before the G-05 signature, and carries no model-performance figure; any H4/SRQ-5 demotion record carries a timestamp preceding the G-05 freeze; a demotion recorded after the freeze is invalid rather than corrected | [Vision §13.1 G-05 evidence] [Vision §5.2 predeclaration for H4] [Vision §8.3] [R-13] | `UNTESTED` — no WS/TA row covers the regime-count audit or the demotion ordering |

### FR-P1-06 — Phase transition freeze

| ID | Requirement | Pass/fail criterion | Source | Test |
|---|---|---|---|---|
| FR-P1-06-1 | `phase_transition_manifest` hashes and freezes the **union of TE §2.2 and §7.0B — fourteen items**, not the nine previously enumerated: model source; TensorFlow/Keras environment; architecture serialization; feature manifest; target contract; split/mask manifests; grids; selected hyperparameters; **optimizer/loss policy**; seeds; **metrics**; **statistical configuration**; **bootstrap**; **reporting hierarchy**. Phase 2 refuses to train if any protected hash differs. **A deliberate difference requires a change record and an `exploratory=true` label** (TE §2.2) — the only sanctioned escape, and therefore the only one | `tests/test_phase_boundary.py` **and** a transition-manifest hash-diff test both pass, **and the hash-diff test's protected-key list is asserted equal to the fourteen-item enumeration** so a short list cannot pass silently; G-P3C confirms protected hashes unchanged; any deliberate difference resolves to a change record carrying `exploratory=true` | [TE §2.2] [TE §7.0B] [NFR-PHASE-01] [origin IMPL-1, GOV-2026-08-20-RA-01] | TA-27 |
| FR-P1-06-2 | Phase 1 fitted weights are never carried into Phase 2, and no Phase 1 result motivates a Phase 2 model or evaluation change, unless a separately approved, exploratory-labelled transfer-learning experiment exists | Phase 2 initializes from new weights; the change log shows no Phase 1-motivated change | [TE §7.0B] | TA-27 |
| FR-P1-06-3 | Every reused or materially adapted third-party source is recorded in the §10.1 register with the **full field set** — `reuse_id`, repository URL, immutable commit/tag, upstream file and line/function, retrieval date, licence and SPDX ID, copied-versus-adapted status, destination file, scientific purpose, modifications, tests, original citation, notice location, reviewer, approval date — **before** the code is used and before G-P2 | `tests/test_reuse_registry.py` passes; no adapter exists without a complete register row | [TE §10.1] [NFR-LIC-01] | TA-28 |
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
| FR-WS-7 | The §18.3 preflight gate passes before an affected component is implemented: **zero unresolved P0 fields and no failing critical test**, an automated assertion confirms no required field in the four configs is `TBD`, and supervisor sign-off covers the scientific hierarchy, IRI role, horizons, estimand, seeds and locked-test protocol | `aws_ai_dlc_preflight_report` shows all three preconditions met. An agent **stops and reports** rather than choosing a default when a P0 decision is unresolved | [TE §18.3] | TA-23 |

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
| NFR-LEAK-01 | Forecast safety | Availability matrix asserts actual lag ≥ declared safe lag for every primary feature; no centered mean, no all-data scaling, no target-hour QC field as a feature | WS-11, TA-08, TA-11 |
| NFR-FAIR-01 | Fair comparisons | One comparison-wide mask per comparison set, stable ID, reported row counts, same window length and lag set | WS-16, TA-11 |
| NFR-REP-01 | Clean CPU reproducibility | The §13.2 ordered sequence completes on CPU from a clean environment | WS-20, TA-17 |
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
all. Every artifact produced before the re-acquisition carries that caveat, and
FULL must not be relied on at a freeze gate while its provenance chain points
at superseded per-month hashes [practices § Walking Skeleton, § Deployment; origin DATA-07, unpersisted].

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

- **Phase 1-applicable (26 rows):** TA-01, TA-02, TA-03, TA-04, TA-07, TA-08,
  TA-09 (bounded — see § Known defects row 8), TA-10, TA-11, TA-12, TA-13,
  TA-14, TA-15, TA-16, TA-17, TA-18, TA-19, TA-20, TA-21, TA-22, TA-23, TA-24,
  TA-25, TA-26, TA-28, TA-32.
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
| G-P1 / G-P1A | Prepared-data MVP and source viability, incl. the §6.1B coverage minimum | Blocked — ICTP failed; replacement pending; §6.1B value unfrozen | Before the phase transition | Supervisor |
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
| 5 | **D-144's status disagreed across the authority stack.** Vision v4.2 §14.2 carried it as "Decision required — Approve / Reject / Modify / Postpone" and "not yet adopted"; Vision §17's freeze line was unchecked; TE §1.5 read `Pending — D-144`; TA-25 read `Blocked`; `evidence/DECISIONS.md` D-3 recorded a 2026-08-15 countersignature with **no filed signature artifact** [origin GOV-22, unpersisted] | **D-144 is approved.** Granted 2026-08-21 by the project owner under the recorded student/supervisor authority equivalence, not by a filed supervisor signature — see `governance/CHANGE_RECORD_2026-08-21_D-144.md`, which carries the §15.2 six-field record, and the annotated status rows in Vision §14.2/§17 and TE §1.5/TA-25. The earlier reading ("countersigned … not blocked on it") asserted the same conclusion from a lower-precedence record and is superseded by this express approval | **Resolved 2026-08-21.** Residual, tracked separately and **not** closed by this approval: the four freezes Vision line 1357 attaches to D-144 — Madrigal experiment/kindat and VTEC parameter/units (frozen by D-4), the coordinate-to-cell rule (frozen by D-1, countersignature row still blank), the hourly aggregation statistic (still `TBD — supervisor freeze gate`, Vision §6.6) and the numerical coverage minimum (still `TBD`, Vision §6.1B). Two of the four remain open, so TA-25 stays `Blocked` on the replacement audit |
| 6 | **Q5 of this stage's own question set under-enumerated §11 as nine NFRs.** §11 carries **eleven** — `NFR-REP-01` is already inside Q5's nine, so the two genuinely missing IDs are `NFR-DQ-01` and `NFR-TDEF-01` | All eleven adopted; see § Non-functional requirements | **Resolved here.** An earlier revision of this row said "twelve", double-counting `NFR-REP-01`; corrected 2026-08-21 per GOV-2026-08-21-RA-01 Rec 9 |
| 10 | **Vision §6.6 mandates a field TE §7.0 requires the phase-boundary test to reject.** TE §6.1 defines `vtec_tecu` as the median of valid VTEC at observed IPPs and `valid_satellite_count` as distinct valid satellites; Vision §6.1A/§6.6 fix the Phase 1 target as location-sampled gridded VTEC from a 1°×1° Madrigal bin — a product carrying no per-satellite or per-IPP quantity — while Vision §6.6 states "Each row must retain exactly these fields"; and TE §7.0 separately requires `test_phase_boundary.py` to **fail** if Phase 1 produces a satellite field | **Resolved by measurement, not by inference — D-17.** The conflict is real and is stated in full: Vision §6.6 says *"Each row must retain exactly these fields"* over TE §6.1's ten-field list, which includes `valid_satellite_count` (distinct valid satellites) and defines `vtec_tecu` as the median *"at observed IPPs"*; TE §7.0 separately requires `test_phase_boundary.py` to **fail** if Phase 1 produces a satellite field; and Vision §6.1A/§6.6 fix the Phase 1 target as gridded VTEC from a 1°×1° Madrigal bin. Rather than choose which document yields, the Phase 1 product schema was **audited**: `parameters_requested = ["ut1_unix", "gdlat", "glon", "tec", "dtec"]` in all twelve request manifests, matching the retrieved isprint extracts — five columns, no satellite identifier, no elevation, no IPP record, native cadence 5-minutely so at most 12 samples per cell-hour — **verified on 23,709 cell-hours deduplicated on `(station, ut1_unix, gdlat, glon)`; an earlier undeduplicated pass reported counts to 24 by double-counting the documented straddle day, and that error is recorded in D-19 rather than left as a stale figure**. `valid_satellite_count` is therefore **not computable** in Phase 1: the contradiction is not adjudicated, it is dissolved on the facts. D-17 records the contract this permits and marks the field not-applicable in Phase 1, Phase 2-only, with nothing substituted. A second consequence is recorded: TE §6.1's provisional `valid_observation_count >= 20` is **unsatisfiable** on a ≤12-sample hour and was evidently written for the Phase 2 IPP population | **Documented and resolved for Phase 1; the source texts remain in conflict.** D-17 lets Phase 1 proceed without adopting a reading, because it enumerates only measured-available fields. What is **not** resolved: Vision §6.6's "exactly these fields" sentence and TE §6.1's Phase 2-shaped provisional minima still read as binding on Phase 1 as written, and correcting them runs through Vision §15.2 change control. Recorded 2026-08-21 per GOV-2026-08-21-RA-01 Rec 22; origin TEC-03 + DATA-04 |
| 8 | **TA-09 independently repeats §16's "all 20" wording.** TE §19 TA-09 reads "Both walking-skeleton fixtures pass all 20 Section 16 checks with evidence links". Defect 1 resolved that wording for §16 and §16.1 only; TA-09 is a separate §19 row, and it is cited as the test link for REQ-ENG-4 and FR-WS-1, both Phase 1 requirements | **TA-09 is read as bounded by the same acceptance set as §16.1** — for a Phase 1 fixture run it means WS-09 through WS-20 pass with evidence links, on the same countersigned reasoning as FR-WS-4. Reading it literally would require Phase 1 to produce WS-01–WS-08 evidence, which §7.0's hard prohibition bars — the identical contradiction defect 1 records | **Open in the source; resolved in practice.** This reading is consequential to the 2026-08-16 countersignature of the WS-09–WS-20 acceptance set rather than a new decision, but it is not itself countersigned. Correcting TA-09's text runs through Vision §15.2 change control. Recorded 2026-08-21 per GOV-2026-08-21-RA-01 Rec 7 |
| 9 | **WS-01 is Phase 1-producible, yet falls inside the WS-01–WS-08 block deferred to G-P3A.** WS-01 (station registry populated from official site logs, pinned IGRF coordinates, header cross-check) is produced by `01_inventory_and_registry.py` and `test_station_registry.py`; neither is a raw-processing module, and `team-practices.md` lists `test_station_registry.py` as Phase 1-reachable. FR-P1-02-1 is a Phase 1 requirement (stage P1-02) and cites WS-01 as its test row, which FR-WS-4 simultaneously places outside Phase 1's acceptance set | **WS-01 is retained in Phase 1's acceptance set as a named exception to the WS-01–WS-08 deferral**, because §7.0's Phase 1 hard prohibition — the stated basis for that deferral — does not reach a station registry. WS-02 through WS-08 remain deferred to G-P3A unchanged. Without this exception the Phase 1 station registry, the authority for `station_lat`, the coordinate-to-cell rule and every per-cell statistic, would have no acceptance row at all | **Resolved 2026-08-21.** The amendment narrowing the 2026-08-16 deferral to WS-02–WS-08 was approved by the project owner under the recorded student/supervisor authority equivalence. Recorded per GOV-2026-08-21-RA-01 Rec 12 |
| 7 | **`scripts/merge_coverage_year.py`'s hash check verifies derived artifacts, not retrieval.** Every `sha256_manifest.json` hashes exactly four derived files and never the contents of `raw_isprint_cache/` — and that cache holds isprint text extractions, not provider `.hdf5` bytes | Fixture eligibility is judged on **derived-artifact** verification, not retrieval verification. Retrieval-level verification is unavailable until the re-acquisition [FR-P1-01-4] | **Open.** Closes when FR-P1-01-4 is satisfied |

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

REQ-ENG-7, REQ-ENG-9, **REQ-ENG-10**, FR-P1-01-5, FR-P1-01-7, FR-P1-01-8,
FR-P1-01-9, **FR-P1-02-6**, **FR-P1-03-5**, FR-P1-04-4, FR-P1-04-10,
**FR-P1-04-12**, **FR-P1-04-13**, **FR-P1-04-14**, **FR-P1-04-15**, FR-P1-05-3,
FR-P1-05-5, FR-P1-05-6, FR-P1-05-7, FR-P1-05-14, FR-P1-05-15, **FR-P1-05-16**,
**FR-P1-05-17**, **FR-P1-05-18**, **FR-P1-05-19**, FR-WS-2, FR-WS-3,
**REQ-CLAIM-01**, REQ-NFR-A1, REQ-NFR-A2.

Five entries were added on 2026-08-21 (bold) per GOV-2026-08-21-RA-01: the two
new FR-P1-04 requirements closing the §6.2 input space and the target-derived
lag contract (Rec 3); the reporting-breakdown requirement split out of
FR-P1-05-11, whose WS-19 link tests plot existence only (Rec 11); the
evaluation-code freeze obligation (Rec 16); and the December regime-count audit
with its pre-freeze demotion ordering (Rec 13). The list is now 23 entries, and
each addition is a requirement that previously either had no ID or carried a
test link that did not test it — which is why the list grew rather than shrank.

Two of these are worth naming as the most consequential gaps: **FR-P1-05-7**
(the confirmatory estimand itself has no TA row — TA-14 tests the bootstrap
that carries it, not the estimand's definition) and **FR-P1-01-5 /
REQ-NFR-A2** (the acquisition-window predicate, which has already produced one
realized defect and is guarded today only by a project-authored test).

## Traceability

Inline source tags appear on every requirement above; this table is the audit
view of the same mapping. [Q7]

| Requirement group | Primary authority | Ideation origin | Test rows |
|---|---|---|---|
| REQ-ENG-1…11 | TE §12, §8.1, §9.2, §9.3, §10, §13.1, §18.3; TC-03, TC-03a, TC-03b, TC-03d, TC-03g, TC-06 | intent § Initial Scope Signal (deliverable: runnable pipeline); practices § Way of Working, § Code Style | TA-01, TA-02, TA-03, TA-09, TA-16, TA-17, TA-22, TA-26; REQ-ENG-10 `UNTESTED` |
| FR-P1-00-1…2 | TE §7.0 P1-00; D-143; Vision R-23 | intent § Phase 1 source status | TA-25, TA-31 |
| FR-P1-01-1…10 | TE §7.0 P1-01, §10, §13.3; D-144, D-5, D-10.1/.2/.3 | intent § Driver contract, § Driver preconditions, obligations 1–2 | TA-03, TA-04, TA-08, TA-15, TA-22, TA-32 |
| FR-P1-02-1…6 | TE §7.0 P1-02, §12 (restricted paths); Vision §6.1B as amended, §8.3; D-2, D-12 | intent § Frozen modelling target | WS-01, WS-18, TA-04, TA-25; FR-P1-02-6 enforced by `tests/test_acquisition_window.py` |
| FR-P1-03-1…5 | TE §6.1, §7.0 P1-03, §7.0 prohibition, §13, §18.2; Vision §6.6; NFR-PHASE-01, NFR-TDEF-01 | intent § Target representativeness — binding | TA-04, TA-15, TA-27; FR-P1-03-5 `UNTESTED` (WS-05 deferred to G-P3A) |
| FR-P1-04-1…15 | Vision §6, §6.4, §6.11, §7.1, §8.1, §8.2, §8.7; TE §5.2, §6.2, §6.3, §6.4, §7.1, §10, §13.3, §18.2; TC-04, TC-08–TC-16 | intent § Benchmark role, § Driver contract | WS-09…WS-13, WS-16, TA-07, TA-08, TA-11, TA-12, TA-15; FR-P1-04-12, -13, -14, -15 `UNTESTED` |
| FR-P1-05-1…19 | Vision §2.3, §2.4, §5.2, §5.3, §8.3, §8.6, §8.7, §13.1; TE §1.3, §7.2, §13.4, §13.6 | intent § Primary estimand, § Metrics, § Mandatory difficulty controls, § Model set, § Reporting, § Test-set sealing condition, § Scoped Verification Obligations row 5 | WS-14, WS-15, WS-17, WS-18, WS-19, TA-10, TA-12, TA-13, TA-14, TA-18, TA-19, TA-20; FR-P1-05-16, -17, -18 `UNTESTED` |
| FR-P1-06-1…4 | TE §2.2, §7.0B, §10.1; NFR-LIC-01 | intent § Governance Dependencies (G-P2) | TA-27, TA-28 |
| FR-WS-1…7 | TE §9.1, §9.2, §13.2, §16, §16.1, §18.3; D-11; TC-01, TC-03f, TC-03g | practices § Walking Skeleton, § Testing Posture | WS-09…WS-20, TA-03, TA-09, TA-17, TA-23, TA-26 |
| NFR-IRI-01 … NFR-LIC-01 | TE §11 (adopted by reference, IDs unchanged) | intent § Success Metrics phase-boundary note | as tabulated in § Non-functional requirements |
| REQ-CLAIM-01 | Vision §11.2 (ID adopted unchanged), §4.2, §4.3, §2.5, §6.2 | intent § Claim boundary; D-8 | `TST-CLAIMS-01` named by Vision §11.2; `UNTESTED` in §16/§19 |
| REQ-NFR-A1…A3 | Gaps found against TE §11; TE §10 driver table, §9.1 | practices § Testing Posture; board findings TEC-04, ML-07 and BENCH-01 (all unpersisted; substance carried in `project.md` and `team.md`) | mostly `UNTESTED` |

**Traceability rule honoured.** No requirement above is new. Each derives from
Vision v4.3 (authored against v4.2), Technical Environment v3.3 (authored against v3.2), a D-number decision, the constraint
register, the intent statement, or the affirmed practices — and says which.
[phases/inception.md § Traceability] The three REQ-NFR-A items are the single
exception class, and each is explicitly marked as a **proposed** addition
requiring supervisor acceptance, with its origin (the board finding that
exposed the gap) named.

## Review

READY

*(Advisory review by aidlc-product-lead-agent, iteration 1, single non-repeating pass. Findings below go verbatim to the human approval gate.)*

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

No findings on: Q3's handling of the unfrozen §6.1B coverage minimum (FR-P1-02-4 correctly writes the threshold as a named hole per the Forbidden-rule bar on filling TBD values, matching the Consolidated Summary's Q3 reading); the Q2 decomposition-by-P1-00..P1-06 structure (matches `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §7.0's stage table verbatim); the §16/§16.1 contradiction itself (correctly identified and resolved per the supervisor-countersigned FR-WS-4); the Q4/DATA-03/DATA-04 closure requirements (FR-P1-01-3 and FR-P1-01-4 explicitly name the DATA-03/DATA-04 items they close); or the out-of-scope, traceability-table, or "constraints inherited" sections, which are internally consistent and correctly sourced.
