# Evidence — Practices Discovery

Reverse-engineering (2.1) is `SKIP` in this scope (`aidlc-state.md` §Stage
Progress), so this stage worked from direct workspace inspection rather than
from `code-structure`/`technology-stack`/`dependencies`/`code-quality-assessment`/
`architecture`/`business-overview` artifacts. Their absence is by design and is
not treated as an error or a gap.

## What each participant inspected or inferred

**Lead (first-pass draft).** Read
`PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` in
full (§1–§11); `PreFlight/vision_document(3)(2)(2).md` §1–§7.1 of 1526 lines
(truncated at a tool-side page cap, remainder not reached);
`scripts/audit_ec1_drivers.py` and `scripts/merge_coverage_year.py` in full;
`evidence/DECISIONS.md` in full; `governance/reviews/GOV-2026-08-15-AH-01.md`
in full; the two `test-pro` sensor manifests; the initiative brief and the
constraint register; `aidlc-state.md`; `org.md`/`team.md`/`project.md`; the
workspace root and `notebooks/` listings. Did not open
`notebooks/madrigal_phase1_coverage_audit.ipynb`, did not check the active
scope file's `skeleton` flag directly, and did not read
`GOV-2026-08-13-IC-01.md`/`IC-02.md`/`GOV-2026-08-15-FE-01.md`/`FE-02.md`.

**Quality reviewer.** Re-read
`Technical_Environment_and_Research_Implementation(1)(2).md` §§7.0, 7.1, 8.1,
12, 13.1–13.4, 16, 16.1, 18.2, 18.3, 19 against the draft's § Testing Posture;
cross-checked `constraint-register.md` TC-06; read
`.claude/scopes/aidlc-research-pipeline-governed.md` frontmatter directly
(the lead had not); read `governance/reviews/GOV-2026-08-15-FE-01.md` finding
`GOV-F-06` (the lead had listed it as unread). Did not independently re-open
the notebook.

**Developer reviewer.** Read both scripts in full a second time with a
line-level diff focus; **opened `notebooks/madrigal_phase1_coverage_audit.ipynb`
in full** (19 cells, 14 code cells, ~455 source lines, kernelspec `python3`,
`language_info.version` 3.11, outputs stripped) — the lead's `evidence.md` had
recorded this notebook as not opened; re-read
`Technical_Environment_and_Research_Implementation(1)(2).md` §§1.3, 7, 7.0,
8.1, 8.3, 10, 10.1, 11, 12, 13.1, 13.2, 14, 18.2, 18.3, 19.

**DevSecOps reviewer.** Ran a targeted repository scan against NFR-SEC-01's
"repository scan/checklist" evidence requirement, reading
`notebooks/madrigal_phase1_coverage_audit.ipynb` cell 2 and all thirteen
`evidence/audit_evidence_2022-{01..12,FULL}/request_manifest.json` and
`sha256_manifest.json` files directly for identity, version-pin, and hash-
coverage fields; re-read
`Technical_Environment_and_Research_Implementation(1)(2).md` §§8.1, 8.3, 10,
10.1, 11, 12, 13.1, 13.3, 13.4, 16.1, 18.2, 18.3, 19; checked the workspace
`.gitignore` for a credential deny-list (found none).

**Human (interview).** Answered `practices-discovery-questions.md` Q1–Q15,
FU-1, FU-2 in full; confirmed the consolidated summary as correct. The
answers are authoritative for every practice choice recorded in
`team-practices.md` and `discovered-rules.md`.

## Key facts established, with direct evidence

1. **Not a git repository at the time of this stage.** `ls -a` on the
   workspace root lists no `.git` directory. This is recorded as a gap
   against the normative core's own requirements, not as neutral context:
   §13.1 requires each run to capture a code commit, §13.4 makes
   `code_commit` a required experiment-registry column, and TA-01's evidence
   column is "Repository tree and code commit" — three independent
   requirements a workspace without git cannot satisfy (devsecops finding J,
   developer finding 12). `team-practices.md` § Way of Working now affirms
   initializing git as this stage's decision (Q1=C) rather than leaving it
   open.
2. **Language mismatch, now with four-fold Python evidence.**
   `aidlc-state.md` records `Languages: TypeScript`. The research code
   actually present — `scripts/audit_ec1_drivers.py`,
   `scripts/merge_coverage_year.py`, and (once opened by the developer
   review) `notebooks/madrigal_phase1_coverage_audit.ipynb`, whose
   `language_info.version` is `3.11` — is Python 3.11, the exact governed pin
   (§8.1, TC-03d). §8.3 makes Python-only a hard normative rule (R, Julia,
   MATLAB "Prohibited"; PyTorch prohibited to avoid a second deep-learning
   stack), not merely an observed fact. Recorded as a discrepancy for the
   human to confirm at requirements-analysis, not silently resolved here,
   since editing `aidlc-state.md` is outside this stage's produced artifacts.
3. **The notebook holds frozen scientific values and production logic that
   have never before been recorded as evidence.** `notebooks/madrigal_phase1_coverage_audit.ipynb`
   cell 4: `STATIONS = {'ARUC': {'lat': 40.286, 'lon': 44.086, ...}, 'BSHM':
   {...32.778987, 35.022987...}, 'NICO': {...35.140989, 33.396450...}}`,
   self-labelled "PROVISIONAL until validated against the official site-log
   PDF for each station"; a `cell_bounds(lat, lon)` function implementing a
   1°×1° lower-left-corner convention, self-labelled "DEFAULT convention
   adopted here ... CONFIRM this matches the real bin edges Madrigal returns
   ... before treating it as frozen." Both are §18.2 forbidden-choice items
   (station coordinates: Student; cell-selection rule: Student + Supervisor,
   D-143/D-144/G-P1) and TC-03e scientific constants that must not live in
   source or a notebook. This is not a breach today (the notebook predates
   the §12/§14 production scaffold) but is a named migration obligation,
   resolved at the interview (Q11=B): freeze the current inline constants as
   a D-number decision first, then migrate the values into `configs/data.yaml`
   and the logic into `src/data/registry.py`.
4. **The notebook contains a hardcoded personal email and identity fields
   persisted into thirteen artifacts — a live NFR-SEC-01 breach.**
   `notebooks/madrigal_phase1_coverage_audit.ipynb` cell 2 assigns
   `USER_FULLNAME`, `USER_EMAIL` (a personal Gmail address, written
   literally), and `USER_AFFILIATION` as in-source constants. `user_fullname`
   and `user_affiliation` are additionally persisted into all 13
   `evidence/audit_evidence_2022-{01..12,FULL}/request_manifest.json` files.
   NFR-SEC-01 (§11): "No secrets in notebooks, source, configs, logs, or
   artifacts; no personally identifiable information is required or stored."
   This sits under a genuine, unresolved tension the interview named and
   resolved rather than papering over: CEDAR's rules-of-the-road require a
   real identity per Madrigal request (the notebook's own cell 2 comment
   states this), while NFR-SEC-01 forbids storing it. Resolved (Q13=A):
   identity continues to be supplied to CEDAR at request time, sourced from
   an environment variable, never persisted; the three fields are scrubbed
   from the thirteen existing manifests and never written again. This
   resolution is recorded as a **verification obligation this project owns**
   (the scrub is a concrete, checkable action against artifacts already in
   the workspace), not a governance dependency.
5. **`madrigalWeb_version` is recorded as `"unknown"` in all twelve monthly
   `request_manifest.json` files** (`evidence/audit_evidence_2022-01/` through
   `-12/`). §10's Madrigal row requires "a pinned `madrigalWeb`
   API/command"; §8.1 requires pinning the client or recording the exact
   web-service interface; §13.3 requires acquisition provenance. The coverage
   audit that produced this evidence ran on an unpinned client — not
   reproducible under NFR-REP-01 as recorded. Resolved (Q14=A, Q8=A): a
   blocking remediation obligation to close before requirements-analysis —
   pin and record the client version going forward; the twelve existing
   months are treated as pre-TC-06 evidence to be re-verified once the test
   suite exists (Q8=A), not silently accepted as-is.
6. **`raw_isprint_cache/` is unhashed everywhere and absent entirely from
   2022-04, 2022-07, and 2022-12.** Each
   `evidence/audit_evidence_2022-*/sha256_manifest.json` hashes exactly four
   files — the three derived coverage CSVs and `request_manifest.json` — never
   the contents of `raw_isprint_cache/`. **Correction, 2026-08-16 (governance
   finding DATA-04):** this fact previously described those contents as "the
   native provider files under `raw_isprint_cache/`". They are not native
   provider files. Every member is named
   `bbox___opt_openmadrigal_madroot_experiments4_<year>_gps_<ddmmmyy>_<file>.hdf5.txt`
   and is the **text output of a bounding-box `isprint` query**, with the provider
   filename embedded in its own name. `find evidence -name "*.hdf5"` returns
   nothing: no provider byte stream exists anywhere in the workspace. The
   consequence is stronger than this fact originally recorded — hashing the cache
   as it stands would still not discharge §13.3, whose `source_files` row requires
   a SHA-256 per **provider file**, so §13.3 cannot be populated for any month, not
   only for the three with no cache at all. Note also the observed provider version
   drift (`g.002` versus `g.003`), which means a later re-acquisition producing
   different bytes would be uninterpretable without the original version suffixes
   recorded — and those were never captured. §10's Madrigal row
   requires retaining native files; §13.3's `source_files` field requires
   provider, permanent citation, filename, retrieval date, and SHA-256 per
   source file. The three missing months include **December**, the
   locked-test month. Consequence: nothing in the workspace today can
   demonstrate that the derived CSVs correspond to the bytes the provider
   served — `scripts/merge_coverage_year.py`'s refuse-to-merge-unverified-
   evidence check verifies only the derived artifacts, not the retrieval
   itself. Resolved: this gap is a blocking remediation obligation (Q14=A),
   but its re-acquisition step is explicitly sequenced **after**
   requirements-analysis (FU-1=B) — narrowing Q14 rather than Q8 — so that no
   acquisition work precedes the requirements stage that will specify what
   the re-acquired data must satisfy. This is the resolved form of the
   ordering tension FU-1 raised: Q8=A (no further acquisition before the
   repository/pins/test-suite exist, TC-06) and Q14=A (all three integrity
   gaps blocking-before-requirements-analysis) would otherwise have required
   building the suite and re-acquiring three months before the stage that
   defines what the suite must verify.
7. **`merge_coverage_year.py:182–208` copies eight provenance fields under an
   unverified identity assumption.** The script takes `request_manifest.json`
   from the first month as a template and copies `madrigal_url`,
   `instrument_code`, `kindat_code`, `parameters_requested`, `stations`,
   `coordinate_to_cell_convention`, `user_fullname`, and `user_affiliation`
   into the merged manifest under the comment "carried unchanged from the
   source runs -- identical across all of them." Nothing in the script
   asserts that identity. Two of the eight fields — `stations` and
   `coordinate_to_cell_convention` — are §18.2 forbidden-choice items, so a
   silent divergence between monthly runs would be exactly the class of
   error the governance regime exists to catch. Disposition (Q14=A): to be closed
   before requirements-analysis, alongside the version-pin gap — the assertion is
   added rather than left as an unchecked comment. **Status correction,
   2026-08-16 (governance finding DATA-10): this is NOT yet done.** The previous
   wording read "Resolved (Q14=A): closed now", which contradicted
   `evidence/CORRECTION_2026-08-16_acquisition_window.md` § Still open item 4.
   `scripts/merge_coverage_year.py` is unchanged and still copies the eight fields
   under the unasserted comment. The obligation stands; the claim of completion
   was wrong.
7a. **The acquisition query was year-blind, and it filed locked-test-month
   records onto an unrestricted path.** Added 2026-08-16; found by the TEC
   governance board (findings IMPL-01, IMPL-02, DATA-01, DATA-02, ML-07, TEC-09,
   VAL-01), and missed by all three support reviews and by this stage's own
   evidence pass, which claimed full manifest coverage. In
   `notebooks/madrigal_phase1_coverage_audit.ipynb` Cell 10 the selection
   predicate read `if exp.startmonth not in RUN_MONTHS and exp.endmonth not in
   RUN_MONTHS: continue` — month without year. The enclosing `getExperiments`
   call spans the whole audit year and legitimately returns experiments
   *overlapping* 2022 at both ends, so a 31-December experiment from either year
   matched. Measured consequences: **743 records dated 2022-12-31 — the locked
   test month — were filed into `evidence/audit_evidence_2022-01/`**, and 642
   records dated 2021-12-31 into `audit_evidence_2022-12/`. The January summary
   consequently reported `unique_days = 32`, `december_days_present = 1` and
   `december_coverage_pct = 3.226` from a January-only run.

   **Bound of the contamination** (DATA-02, recorded so a later reader of the
   January folder alone is not misled): it reaches three columns of one file plus
   the reviewer note in `DECISIONS.md`. `audit_evidence_2022-FULL/` is correct
   (365 days, 100%, all three stations) because the merge script's year guard
   excludes out-of-year rows from statistics, and D-9 promotes FULL rather than
   the per-month folders. D-2's coverage verdict is judged on
   `madrigal_coverage_monthly.csv` day counts, which were correct. Nothing
   downstream was mis-decided.

   **Why no existing check caught it:** per-file SHA-256 verifies outputs, and
   selection happens upstream of hashing; the merge script's guard tests
   calendar-year membership while the defect is run-window membership — the
   2022-12-31 rows *are* year 2022 and passed it untouched. That asymmetry is
   precisely why FULL stayed correct while the January summary did not. The claim
   that this proves the hash chain "cannot detect wrong-math errors" was raised
   and **withdrawn** as unsupported.

   **Custody classification** (VAL-01): manifest timestamps show the authorized
   Vision §8.3 performance-blind December coverage audit ran at
   2026-08-12T10:25:30Z and the January run at 2026-08-12T22:41:57Z. The January
   run therefore exposed no locked-month information not already lawfully in hand,
   and only coverage counting was performed on it. Classified a **within-authorization
   irregularity, not an unauthorized access event**; the seat recorded that a
   first-contact January run would have been judged differently.

   **Resolved 2026-08-16.** Predicate corrected to a `(year, month)` membership
   test; `tests/test_acquisition_window.py` added as the owning check (5 failed /
   23 passed before the fix, 28 passed after, with a negative control proving it
   catches the defect rather than passing vacuously) — a **new** module that
   amends §12's exhaustive tree and awaits supervisor countersignature; the
   misfiled locked-month extract moved to `evidence/locked_test_restricted/` and
   logged in `evidence/experiment_registry.md` with `locked_test_accessed = true`;
   January and December artifacts regenerated with originals preserved under
   `superseded_2026-08-16/`. December's statistics were unchanged, confirming no
   December science moved. Full record:
   `evidence/CORRECTION_2026-08-16_acquisition_window.md`. Still open:
   `audit_evidence_2022-FULL/` has not been re-merged, so its provenance points at
   the superseded per-month hashes; and the `DECISIONS.md` reviewer note still
   asserts a different root cause and calls the anomaly "correct" (DATA-01).
8. **This is a governed scientific pipeline, not a web service** — testing
   and deployment mean reproducibility, leakage control, evidence packaging,
   and freeze/gate discipline. Direct evidence, expanded from the first-pass
   draft: the ten-item §18.3 preflight critical set (not the two tests
   originally named); the §12 seventeen-module `tests/` tree; the §16
   WS-01–WS-20 and §19 TA-01–TA-32 pass/fail acceptance vocabulary (the only
   one Construction has, since `user-stories` (2.4) is `SKIP`); the required
   pre-G-05 December coverage audit (Vision §8.3) distinct from the one-shot
   locked-metrics evaluation (G-06); the `phase_transition_manifest` freeze
   (§7.0B) enforced by a hash-diff test at gate G-P3C; the two-platforms-only
   governance (§9.1).
9. **Decisions, not commits, are this project's current unit of auditable
   change**, and that stays true even once git exists. `evidence/DECISIONS.md`
   D-1 through D-10 each record a decision date, decider, rationale, and
   (where applicable) a countersign status. Resolved at the interview (Q2=C):
   `DECISIONS.md` remains authoritative for scientific/governance decisions;
   commits are authoritative for code; any commit touching a scientific
   constant, config value, or governed artifact must cite its D-number.
10. **No formatter/linter configuration exists yet, and `pyproject.toml` is
    not merely absent — it is a mandated, not-yet-built deliverable.** No
    `.prettierrc`, `pyproject.toml`, `setup.cfg`, `ruff.toml`, `.flake8`,
    `tox.ini`, `requirements.txt`, or `.python-version` was found at the
    workspace root, nor were `src/`, `configs/`, or `tests/` directories
    present. §12's repository tree mandates `pyproject.toml` at the root;
    TA-01 gates the repository skeleton's acceptance on it. Resolved (Q10=A):
    `ruff`, for both lint and format, adopted now.
11. **The two observed scripts are not the same style family** — this
    corrects the first-pass draft's "same style family" characterisation.
    They diverge on four axes: typing (`from __future__ import annotations` +
    PEP 604 hints in `audit_ec1_drivers.py` only), path handling (`pathlib`
    vs. `os.path`), string quoting/formatting (double-quote f-strings vs.
    single-quote `%`-formatting), and the fatal-exit idiom (`raise
    SystemExit`/`sys.exit(main())` vs. bare `sys.exit('message')` with `main()`
    returning `None`). What they genuinely share is the module-level
    docstring convention and `snake_case` naming. The notebook was
    subsequently inspected (developer review) and does not resolve this
    divergence either way — it is a third, distinct file with its own
    conventions and its own copy of the SHA-256 helper, making the hashing
    helper triplicated (`sha256` in `audit_ec1_drivers.py`, `sha256_of_file`
    in `merge_coverage_year.py`, and a third copy inside the notebook), not
    merely duplicated as first recorded.

## What remains uncertain

- **This stage's own evidence pass was not load-bearing on acquisition
  integrity.** Recorded 2026-08-16 after the governance board. The section above
  states that all thirteen `request_manifest.json` and `sha256_manifest.json`
  files were read, yet fact 7a — locked-test-month records on an unrestricted
  path — was found by neither the lead nor the three support reviewers. Two
  further characterisations in this file were wrong as first written: the
  `raw_isprint_cache/` contents (fact 6, corrected) and the "same style family"
  reading (fact 11, already corrected at integration). The integrity conclusions
  here should be treated as reviewed rather than proven, and re-checked against
  the artifacts on any later reliance.
- **Fixture selection is now partly closed.** The seven-day plumbing window was
  frozen by the student as **D-11** (November 2022, 2022-11-01 to 2022-11-07, all
  three cells) under Q-31, which TE §18.2 assigns to the Student; no supervisor
  countersignature is required for it. The **one-month all-station scientific
  window remains open**, and 2022-04 and 2022-07 are ineligible for it until the
  `raw_isprint_cache/` re-acquisition, which FU-1=B sequences after
  requirements-analysis. All Dst evidence informing D-11 is **provisional grade**;
  D-10.1's open item — the Kyoto Dst release grade for calendar 2022 — is still
  unchecked, and definitive-grade verification is required before any Dst value is
  used beyond fixture characterisation.
- **Supervisor-owned items, status 2026-08-16.** All four are set out in
  `governance/COUNTERSIGNATURE_REQUEST_2026-08-16.md`.
  - **Countersigned 2026-08-16, recorded on the student's report:** the TE §12
    amendment adding `tests/test_acquisition_window.py`, and the WS-09–WS-20
    Phase 1 acceptance split with WS-01–WS-08 deferred to G-P3A. This closes
    governance findings IMPL-03 (missing owning test for acquisition-window
    conformance) and the acceptance-set half of ML-08 / CHAIR-04.
  - **Still open:** the §1.3 script/notebook count inconsistency (note that Vision
    §14.2 D-130 already records the seven/four counts as superseded, though its
    pointers carry no counts of their own); and the missing D-3/D-144 signature
    artifact together with its two still-unfrozen sub-values, the
    coordinate-to-cell rule and the numerical coverage minimum.
- **Vision document not read past §7.1 (line 657 of 1526)** in the lead's
  original pass. §7.2 through §17 were not directly re-read during this
  stage's integration either. No claim in `team-practices.md` or
  `discovered-rules.md` rests solely on an unread Vision section; every claim
  traces to the Technical Environment document (read in full across all four
  participants) or to a specifically-read Vision section (§1–§7.1, plus
  §8.3, §13.1's gate table, and §2.2/§2.4/§5.3–§5.4/§6/§9.2, each cited where
  used).
- **`governance/reviews/GOV-2026-08-13-IC-01.md`, `IC-02.md`,
  `GOV-2026-08-15-FE-02.md`** remain unopened; only `AH-01.md` (lead) and
  `FE-01.md`'s finding `GOV-F-06` (quality reviewer) were read directly. No
  practice claim here rests on their unread content beyond what
  `initiative-brief.md` and `constraint-register.md` already quote from them.
- **Sensor scripts (`tools/aidlc-sensor-*.ts`) were not opened**, only their
  manifest files (`sensors/aidlc-*.md`). Their advisory-severity behaviour is
  taken from the manifest's own frontmatter and prose, not from reading the
  implementation.
- **Two open supervisor countersignatures**, named here per `project.md`'s
  rule to enumerate every open supervisor gate the phase handoff surfaces,
  and kept separate from this project's own verification obligations above:
  1. **Phase 1 walking-skeleton acceptance-set reading.** §16 states
     acceptance requires all 20 WS rows `PASS`; §16.1 assigns WS-01–WS-08 to
     the Phase 2 gate G-P3A; §7.0 bars Phase 1 from the raw-processing path
     that produces that evidence. Resolved for this project's own use as
     WS-09–WS-20 (Q6=A), but this reading is **not yet supervisor-signed** —
     owner: supervisor, before it is relied on at a freeze gate.
  2. **Script/notebook count contradiction.** §1.3's v2.0 change row states
     "Scripts 18 → 7 / Notebooks 11 → 4"; §7, §12, §14, and §19 all describe
     nine phase-aware stage scripts and five notebooks, and TA-01 approves
     against the latter. Resolved for this project's own use as §12/§14/§19
     operative, §1.3 recorded as a stale change-log row (Q15=A), but this
     reading is **not yet supervisor-signed** — owner: supervisor, raised for
     countersignature alongside item 1.
  Both are governance dependencies owned outside this project's own
  verification work — the project can act on the resolved reading
  provisionally, but neither is closed until the supervisor countersigns.
- **The AGPLv3 Global-TEC-forecasting repository's distribution obligations**
  (§10.1) — whether direct copying from it is actually permitted — is a
  governance dependency owned by the student, supervisor, and institutional
  policy (§18.2), not a check this project performs on itself. Left open,
  owner: student + supervisor, before any code is copied from that source.
- **The TensorFlow pin** (§8.1) is explicitly unresolved in the governing
  document itself, frozen only after Kaggle/local fixture installation
  passes — left open with the other `TBD — freeze gate` items, not decided
  by this stage.
- **The specific calendar month for the one-month all-station walking-
  skeleton fixture** is not named in this artifact; `team-practices.md`
  § Walking Skeleton records the selection criterion (verified three-station
  coverage, December excluded) rather than a specific month, since
  identifying it requires a mechanical hash-verification check against each
  month's `raw_isprint_cache/` status that this stage did not perform.
  Left open, owner: student, before the D-number entry is written.

## No git commit hash exists for this stage

The workspace is not yet a git repository (`ls -a` shows no `.git` directory;
see fact 1 above), so `practices-discovery-timestamp.md` records the literal
`no-git` in the commit-hash position rather than an invented hash. Once
`team-practices.md` § Way of Working's Q1=C decision is acted on (git
initialized, work on `main`, freeze gates tagged), subsequent stage
timestamps will carry a real commit hash.

## Sources

- `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md`
- `PreFlight/vision_document(3)(2)(2).md` (§1–§7.1 read by the lead; §8.3,
  §13.1's gate table, and other individually-cited sections read by
  reviewers; remainder not reached)
- `scripts/audit_ec1_drivers.py`
- `scripts/merge_coverage_year.py`
- `notebooks/madrigal_phase1_coverage_audit.ipynb` (opened by the developer
  reviewer; cells 2 and 4 read in full by the developer and devsecops
  reviewers respectively)
- `evidence/DECISIONS.md`
- `evidence/audit_evidence_2022-{01..12,FULL}/request_manifest.json` and
  `sha256_manifest.json` (all thirteen, read by the devsecops reviewer)
- `governance/reviews/GOV-2026-08-15-AH-01.md`, `GOV-2026-08-15-FE-01.md`
  (finding `GOV-F-06`)
- `sensors/aidlc-coverage-threshold.md`, `sensors/aidlc-requirement-coverage.md`
- `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/approval-handoff/initiative-brief.md`
- `aidlc/spaces/default/intents/260813-tec-hourly-forecast/ideation/feasibility/constraint-register.md`
- `aidlc/spaces/default/intents/260813-tec-hourly-forecast/aidlc-state.md`
- `.claude/scopes/aidlc-research-pipeline-governed.md`
- `aidlc/spaces/default/memory/org.md`, `team.md`, `project.md`,
  `phases/inception.md`, `phases/construction.md`
- Workspace root and `notebooks/` directory listings (`ls -a`)
- `contributions/aidlc-quality-agent.md`, `contributions/aidlc-developer-agent.md`,
  `contributions/aidlc-devsecops-agent.md`
- `practices-discovery-questions.md` — Q1–Q15, FU-1, FU-2, human-confirmed

## Assumptions & Open Questions

- Assumed that the Technical Environment document, read in full by every
  participant, is a reliable implementation-level restatement of the Vision
  sections not directly re-read (§7.2–§17), since the Technical Environment
  document's own §1.1 states it "translates the approved scientific and
  methodological rules" from the Vision and "must not redefine" them. This
  assumption should be checked if a later stage needs a Vision-only detail
  (e.g. exact model architecture parameters) not also covered in the
  Technical Environment document.
- Assumed `constraint-register.md` and `initiative-brief.md`'s citations of
  Vision §13.1 and other later sections are faithful restatements, since
  both are themselves prior-stage artifacts already subject to their own
  governance review.
- Left open, verification obligation this project owns: whether the human
  wants the Vision document's remaining sections (§7.2–§17) re-read before
  requirements-analysis, which will need the full feature/model/evaluation
  detail regardless.
