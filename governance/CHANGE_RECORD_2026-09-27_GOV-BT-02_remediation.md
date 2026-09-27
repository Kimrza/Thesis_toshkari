# Change record — 2026-09-27 remediation of GOV-2026-09-27-BT-02 (all 29 recommendations approved)

**Authorization:** the Student approved ALL 29 recommendations of the 2026-09-27
full-board governance review `GOV-2026-09-27-BT-02` (build-and-test, stage 3.6,
FULL BOARD mode, gate verdict FAIL) verbatim: "I approve all your recommendations
for remediation." This record is the execution record of that remediation pass —
what was changed, what was drafted for owner adoption, what remains an
owner/supervisor/external act, and what could not be executed on this clone.

**Executing session:** governance remediation session of 2026-09-27, clone
`C:\Users\s_sch\Desktop\test\Thesis_toshkari-main\Thesis_toshkari-main`, HEAD at
execution start `69b00c4` (2026-09-26). This clone carries **no Python
interpreter and no conda** (`Get-Command conda|python` → not found) — every
consequence of that is stated under § Blocked below. No locked-December content
was read; no push was made; no memory-layer file was edited (the team.md
correction is DRAFTED for the §13 ritual, its only sanctioned write path).

---

## 1. Executed this pass (by recommendation)

| Rec | Action executed | Where |
|---|---|---|
| R1 | Re-baseline addenda at HEAD `69b00c4` (34 modules, 10 pins, ladder through stage 06, D-72–D-76, GIM release) written into the artifact bodies; fresh junit at HEAD **BLOCKED** (§ Blocked) | `build-test-results.md`, `build-and-test-summary.md`, `integration-test-instructions.md`, `unit-test-instructions.md` |
| R2 | Rec 47 relabelled "CLOSED (CI-verification limb only)"; restricted-reader modules deselected from CI; consolidated platform ruling DRAFTED for Student+Supervisor; team.md §13 ritual text drafted | `build-test-results.md`, `.github/workflows/verify.yml`, `CHANGE_RECORD_2026-09-27_platform_bound_RULING_REQUEST.md` |
| R3 | `resolve_platform_roots` now refuses `GITHUB_ACTIONS`/`CI`-marked environments (fail-closed); negative control added; `verify.yml` declares `TEC_PLATFORM: local` explicitly; subprocess test helpers strip the CI markers where marker-free default resolution is the tested behaviour | `src/data/config.py`, `tests/test_determinism.py`, `verify.yml`, `tests/test_gim_generation.py`, `tests/test_gim_provenance.py`, `tests/test_external_drivers.py` (×2) |
| R4 | Fixture-manifest countersignature misstatement corrected to the register's actual state (D-33 countersignature OUTSTANDING) | `tests/fixtures/plumbing_7day/fixture_manifest.yaml` (§ 2 below is the change text) |
| R5 | Original report confirmed absent from the entire tree (Glob, 2026-09-27); limitation record written per the c12 pattern (option 2; option 1 remains open if the LOTUS clone holds the file) | `CHANGE_RECORD_2026-09-27_GOV-BT-01_report_loss.md` |
| R6 | Diary reconciliation entry appended (condition CLOSED, the 2026-09-27 retrieval attempt was an optional provenance re-retrieval); custody-channel limitation sentence added to the results addendum; `test_release_hashes.py` re-run **BLOCKED** (§ Blocked) | `memory.md`, `build-test-results.md` |
| R7 | Commit-hash → authorizing-record mapping (§ 3 below); `.githooks/commit-msg` hook added refusing empty/boilerplate messages — **negative control demonstrated on this clone**: boilerplate → exit 1, empty → exit 1, real message → exit 0 (mechanism note: message checks belong to `commit-msg`, not `pre-commit`, which runs before the message exists) | § 3; `.githooks/commit-msg` |
| R8 | Item 9's two never-persisted Kaggle junit citations marked prose-only in the artifact body (option 2; option 1 — persisting the XMLs — remains open if the Kaggle notebook outputs survive) | `build-test-results.md` |
| R9 | Items 6/7 corrected to RULED with CR citations (locked-root exposure ruled 2026-09-24; §18.3 selection (b) ruled 2026-09-25, D-69); the surviving residual (CI-runner access-record persistence) named and routed | `build-and-test-summary.md`, `security-test-instructions.md` |
| R10 | D-number text DRAFTED for owner adoption (§ 4.1) | this record |
| R11 | `iri_column_violations` name limb widened to production's token rule; `iri2016_*` negative control added | `tests/test_iri_denial.py` |
| R12 | Ruling RECORDED (§ 5.1): Student approved option 1 (per-hour exclusion attribution with member-caused refusal above a declared bound); implementation deferred to its own review pass, supervisor concurrence owed, due before G-06 — the pinned known-gap test stands and will fail the day the mechanism lands, forcing the rewrite | § 5.1 |
| R13 | External (Kaggle session + two preconditions); status restated, nothing executable here | § 5.2 |
| R14 | Passed-count corrections in place: `full_post.xml` 1581→**1575**, `rem1.xml` 445→**441**, both re-derived from the XMLs' own attributes this session (1584/3F/6s; 448/3F/4s) | `build-test-results.md`, `build-and-test-summary.md` |
| R15 | Three representations corrected: the Q-31 open act is the scientific-fixture **manifest freeze**; the window is frozen as D-14 (March 2022) | `build-and-test-summary.md`, `integration-test-instructions.md` (×2) |
| R16 | TA-07 attribution corrected to `test_iri_denial.py::iri_gim_containment`; the two guard homes and their boundary split stated per `nfr-design:c58` | `security-test-instructions.md` |
| R17 | Step 4 condition 3 amended to run-and-record (advisory; no enforced lint floor, Q5=A), dated and visible | `build-instructions.md` |
| R18 | Retrieval-host classification folded into the consolidated platform ruling draft (option 1) | `CHANGE_RECORD_2026-09-27_platform_bound_RULING_REQUEST.md` § 3 |
| R19 | Registry roll-up correction appended (row 10 is the sixth retrospective row); guard-test comment corrected in the same pass | `evidence/experiment_registry.md`, `tests/test_locked_test_guard.py` |
| R20 | "Never open December content" reworded to the registry's access taxonomy (byte reads logged before each read; no value parsed) | `unit-test-instructions.md` |
| R21 | Obligation restated with its due point (producer-side interval-end control before the first governed driver release / G-04); nothing executable until the producer exists | § 5.3 |
| R22 | Three D-number texts DRAFTED for owner adoption (§ 4.2) | this record |
| R23 | December-2022 epoch refusal added to `generate_comparator` (fail-closed `g05_signature_verified=False` default, `verify_g05_signature` the authorizing check); negative control added through the sanctioned `scripts/04` subprocess path | `src/external/gim.py`, `tests/test_gim_generation.py` |
| R24 | G-05 package obligation recorded (§ 5.4): the sign-off text must name D-68 as part of the locked-test protocol the supervisor signs | § 5.4 |
| R25 | Persist-before-rerun rule written into the build procedure | `build-instructions.md` § 2026-09-27 amendments |
| R26 | `02_build_vtec_target.py` absence-by-design disclosure sentence added (TA-01 expects eight of nine scripts pre-G-P2) | `build-instructions.md` |
| R27 | Standing migration plan restated at the gate (three SHA-256 helper copies; consolidate on next touch, before G-07 packaging) — no mid-gate code churn | § 5.5 |
| R28 | Third stale recurrence of `aidlc-state.md` Project Root recorded; the drop/relativize decision remains the routed owner question; NO hand-edit made (no sanctioned write path) | § 5.6 |
| R29 | Record-only (AI-DLC coverage sweep on the board record; framework filename nit is upstream's) | — |

Cross-unit disclosure per `project.md` gf-3: this pass edits modules owned by
**foundation** (`src/data/config.py`, `tests/test_determinism.py`),
**external-products** (`src/external/gim.py`, `tests/test_iri_denial.py`,
`tests/test_gim_generation.py`, `tests/test_gim_provenance.py`,
`tests/test_external_drivers.py`) and **governance-guards**
(`tests/test_locked_test_guard.py`, comment-only) under their frozen receipts;
each unit's `code-summary.md` carries a dated addendum naming this pass. The
Student's blanket approval of R3/R11/R19/R23 is the explicit ruling
`code-generation:c32` requires for those cross-unit edits.

## 2. R4 — fixture-manifest correction (change text)

`tests/fixtures/plumbing_7day/fixture_manifest.yaml`, units area, `coordinates.source`:
the 2026-09-26 note claiming both halves "were already frozen and countersigned"
is corrected to the register's actual state — coordinates frozen (D-1, closed
2026-08-21 under the recorded student/supervisor authority equivalence, **no
signature artifact exists and none is claimed**; D-65 Student-owned);
coordinate-to-cell rule frozen (D-1 addendum / D-33) with **D-33's TE §18.2
supervisor countersignature still OUTSTANDING** (`evidence/DECISIONS.md` D-33;
`configs/data.yaml:176` agrees). Option 2 — obtaining the actual countersignature
— remains the open D-33 condition, owed before the Q-31 manifest freeze and in
any case before G-05.

## 3. R7 — commit-message mapping (boilerplate commits → authorizing records)

Derived 2026-09-27 from `git show --stat` and the change records on disk; where
attribution is inferred it says so and the Student confirms at the gate.

| Commit | Date | Carries | Authorizing record (derived) |
|---|---|---|---|
| `db15880` | 2026-09-25 | The three IGS site logs (evidence custody closure) | `GOV-2026-09-24-BT-01` Rec 1, ruled option 1 (`CHANGE_RECORD_2026-09-24_GOV-BT-01_rulings.md`). **Recovery channel of the bytes unrecorded** — disclosed in `build-test-results.md` (R6); identity rests on hash equality with the 2026-09-20 manifests, re-verified by four board seats 2026-09-27 |
| `e7d3ff1` | 2026-09-25 | 2026-09-25 remediation addenda, registry rows, run snapshots | Continued Student authorization of the 2026-09-25 remediation pass (recorded in `build-test-results.md` § 2026-09-25 addendum) |
| `576046c` | 2026-09-26 | `scripts/04_build_external_products.py`, `src/external/iri.py`, `tests/test_b01_prediction_adapter.py` (B-01 adapter work) | 2026-09-26 owner session (D-72/D-73-era external-products work) — **inferred; Student to confirm the covering D-number/CR at the gate** |
| `0ce2a68` | 2026-09-26 | Run snapshots + audit shard (fixture session) | 2026-09-26 fixture-ladder session under D-74/D-75/D-76 (per `7b4109b`'s own message) — **inferred; Student to confirm** |
| `69b00c4` | 2026-09-26 | Run snapshots + audit shard (HEAD) | Same session as above — **inferred; Student to confirm** |

Prospective control: `.githooks/commit-msg` (this pass) refuses the defect class;
control demonstrated biting on this clone (boilerplate/empty → exit 1, real → 0).
History is NOT rewritten — all five commits are pushed and their SHAs are cited
across the governance record.

## 4. Drafted D-number texts (owner adopts into `evidence/DECISIONS.md`; drafting is not deciding — `code-generation:c31`)

### 4.1 R10 — the IRI name-filter widening (proposed text)

> **D-<nn> — NFR-IRI-01 denial-mechanism widening after the `iri2016_t_plus_1_tecu` near-miss (TA-07/WS-10 record)**
> Date: <owner date>. Owner: Student.
> Defect: `_assert_field_name_clean` (`src/features/build.py`) refused only
> `iri_`-prefixed or bare-`iri`-token names; the project's own canonical IRI
> field name `iri2016_t_plus_1_tecu` (TE §6.2 row identity) satisfied neither
> and could reach the feature dictionary via the unconstrained `target_support`
> row. WS-10's then-existing injection control (`iri_vtec`) was structurally
> blind to it.
> Decision: the name limb refuses ANY token beginning `iri`
> (`src/features/build.py:346–362`, repaired 2026-09-20). Controls: (a)
> `tests/test_feature_leakage_guards.py` id
> `ta33-canonical-iri2016-name-on-the-unconstrained-support-row`; (b)
> `tests/test_iri_denial.py::test_canonical_iri2016_name_fails_whatever_its_provenance_says`
> (test-layer restatement widened 2026-09-27, GOV-2026-09-27-BT-02 R11).
> Cited against NFR-IRI-01, TA-07, WS-10. This record discharges the stage
> diary's 2026-09-20 obligation ("owes a D-number… appears in no register").

### 4.2 R22 — the three provisional statistical blocks (proposed texts)

For each of `configs/experiment.yaml` `estimand` (line ~243), `bootstrap`
(~261), `comparison_sets` (~285), whose `decision:` lines cite their 2026-09-06
change records "(proposed D-number pending owner adoption)":

> **D-<nn> — Estimand transcription**: paired loss differential, benchmark
> minus model, equal-station weighting, positive favours the model (Vision
> §2.3; TE §1.3) — adopts the transcription of CR-2026-09-06 as frozen.
> **D-<nn+1> — Bootstrap transcription**: vector time-block bootstrap, 24-hour
> blocks carrying all three stations, 10,000 replicates, seed 20221201, 95%
> CI, 48-hour sensitivity, cross-station paired-error correlation reported
> (TE §13.6; TC-19) — adopts the transcription of CR-2026-09-06 as frozen.
> **D-<nn+2> — Comparison-set memberships** as transcribed, single
> comparison-wide intersection mask per set, mandatory difficulty controls
> declared (Vision §2.4; NFR-FAIR-01) — adopts the transcription of
> CR-2026-09-06 as frozen.

On adoption, the three `decision:` lines in `configs/experiment.yaml` update to
cite the D-numbers (a config-comment edit citing this record).

## 5. Recorded dispositions (no code this pass)

1. **R12 (member-shortfall mask gap):** Student approved option 1 — per-hour
   exclusion ATTRIBUTION (target- vs member-caused) on the mask, member-caused
   exclusions in the locked context refusing above a declared bound. The bound
   is a to-be-declared value (never filled by convenience); implementation is a
   READY-unit mask-schema change requiring its own review pass and supervisor
   concurrence. Due before G-06. The pinned test
   (`test_rec15_residual_member_absence_absorbed_by_exclusion_counts_is_not_caught`)
   stands deliberately and fails the day the mechanism lands.
2. **R13 (Kaggle durability / TC-03g):** already owner-ruled ("Student — before
   G-05"); blocked on in-session-gate wiring and the Q-31 manifest freeze;
   discharge runbook `kaggle/HOW_TO_RUN_IN_SESSION_GATE.md` stands ready.
   Closure: Kaggle-session junit for the full selection (b), green, plus the
   measured durability record populating `CHARACTERISED_DURABILITY_PLATFORMS`.
3. **R21 (interval-end producer control):** owed at the producer build, before
   the first governed driver release feeding G-04 (routed P-1 of
   `CR-2026-09-19-SCI-REVIEW`).
4. **R24 (D-68 in the G-05 package):** the G-05 sign-off text must name D-68 by
   number as part of the locked-test protocol the supervisor signs — recorded
   here as a G-05 preparation-checklist item so it cannot be forgotten.
5. **R27 (hash-helper consolidation):** complete the recorded team.md migration
   when `scripts/audit_ec1_drivers.py` / `scripts/merge_coverage_year.py` are
   next touched; before G-07 reproducibility packaging.
6. **R28 (Project Root):** third stale recurrence; the owner decides whether to
   drop, relativize, or declare the field per-clone-informational; no sanctioned
   direct-write path exists and no hand-edit was made this pass.

## 6. Blocked on this clone (owed verification, first run on a governed host)

- **No Python interpreter/conda exists here**, so: (a) R1's fresh full-suite +
  critical-set junit at HEAD is NOT produced — the operative suite figures
  remain evidence for `db15880`-era commits only; (b) R6's closing
  `test_release_hashes.py` re-run is not executed; (c) every code edit of this
  pass (R3, R11, R19-comment, R23, the env-pop additions) is **statically
  authored and untested on this clone**. First verification: a governed-host
  run of the full suite at the remediation commit, persisted under
  `artifacts/exec_evidence/run_2026-09-27_bt02/`; CI will additionally exercise
  the new controls in `test_determinism.py`, `test_iri_denial.py`,
  `test_gim_generation.py` once pushed (those modules are NOT among the CI
  deselections).
- **No push** (outside this session's authorization): the narrowed `verify.yml`
  takes effect on the Student's next push.
- **Committing on this clone is blocked by design**: the active pre-commit hook
  fails closed without the governed environment on PATH. The remediation is
  left as working-tree changes for the Student to commit from a governed host,
  with a message citing this record (the new commit-msg hook will refuse
  boilerplate).

## 7. Verification checklist (closure evidence per the board's blocks)

1. **DONE (2026-09-27, governed clone).** Suite run at commit `70bb651`
   (the remediation patch, applied on the authoring clone), `tec-thesis-311`
   / CPython 3.11.16 / `PYTHONHASHSEED=0`: full suite 2384 total / 2380
   passed / 0 failed / 0 errors / 4 skipped (`full.xml`); §18.3 selection (b)
   1417/1417 (`crit.xml`); `test_release_hashes.py` 965/965
   (`release_hashes.xml`); all three new negative controls green individually
   AND proven to bite (guard reverted → fails; restored → passes):
   `test_ci_runner_markers_are_refused_not_defaulted`,
   `test_canonical_iri2016_name_fails_whatever_its_provenance_says` (one
   test-data fix applied to isolate this control from an accidental
   provenance-substring match — see `build-test-results.md` § 2026-09-27
   re-baseline addendum for the full bite-proof log),
   `test_generation_december_2022_epoch_refuses_pre_g05`. All junit persisted
   under `artifacts/exec_evidence/run_2026-09-27_bt02/`. Zero failures, zero
   errors, no test weakened/skipped/xfailed to reach this; the four pre-existing
   skips are read and stated individually in the results addendum.
2. **DONE (2026-09-27, this governed clone).** Committed locally (not pushed)
   with a real message citing this record, under `core.hooksPath=.githooks`
   with the governed environment on PATH; `.githooks/commit-msg` verified
   active and refusing boilerplate/empty messages before this commit was
   made (Step 5 of this session). See `git log` for the commit hash — this
   record is not edited again to insert it, per this project's rule against
   editing a change record to chase a derived value after the fact.
3. Student + Supervisor sign
   `CHANGE_RECORD_2026-09-27_platform_bound_RULING_REQUEST.md` (R2/R18/R3
   durable fix) — before G-05 (custody limb) / G-07 (authorization record).
4. Student adopts the § 4 D-number drafts (R10, R22) — before G-05.
5. Supervisor: D-33 countersignature (R4 option 2) — before the Q-31 manifest
   freeze / G-05.
6. LOTUS clone checked for the original `GOV-2026-09-24-BT-01` report file
   (R5 option 1); if found, committed verbatim under `governance/reviews/`.
7. Kaggle session: R13's discharge + R8's junit persistence if the notebook
   outputs survive.
