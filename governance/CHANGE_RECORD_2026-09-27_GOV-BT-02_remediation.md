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
| R4 | Fixture-manifest countersignature misstatement corrected to the register's then-actual state (D-33 countersignature outstanding); **superseded same day** — D-33's governance condition CLOSED 2026-09-27 on the Student's explicit verbal confirmation, under the same authority equivalence that closed D-1 (`evidence/DECISIONS.md` D-33 addendum) | `tests/fixtures/plumbing_7day/fixture_manifest.yaml`, `configs/data.yaml:176`, `evidence/DECISIONS.md` (§ 2 below is the full change text) |
| R5 | **CLOSED on option 1 (recovery), same day — and extended.** The report was never a file — it was delivered in chat 2026-09-24 per the output contract's default. Verbatim text recovered from this clone's session transcript (`9ccb10d0…`, line 432, 2026-09-24T19:42:32Z, 31,019 chars, 16 Recommendation blocks, counts re-derived 1/7/7/1) and written to `governance/reviews/GOV-2026-09-24-BT-01.md` with a provenance header; the body is byte-verbatim, nothing reconstructed. **On the Student's further instruction of 2026-09-27, the companion closure-verification pass was recovered by the same method** (same transcript, lines 726/727, 2026-09-25T08:23–08:33Z, 9,171 chars, 16 closure rows, the "Lift FAIL to CONDITIONAL PASS" recommendation) and written to `governance/reviews/GOV-2026-09-24-BT-01-CLOSURE-VERIFICATION.md` with its dispatch brief appended verbatim as evidence the pass was mandated adversarial. The interim limitation record is marked SUPERSEDED and carries corrections to two claims it made wrongly (the board was `ADAPTIVE`, not full-board; it ran on THIS clone `GIT-AE-SRV-RDT1`, not LOTUS) | `governance/reviews/GOV-2026-09-24-BT-01.md`, `governance/reviews/GOV-2026-09-24-BT-01-CLOSURE-VERIFICATION.md`, `CHANGE_RECORD_2026-09-27_GOV-BT-01_report_loss.md` |
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
was corrected 2026-09-27 to the register's then-actual state — coordinates frozen
(D-1, closed 2026-08-21 under the recorded student/supervisor authority equivalence,
**no signature artifact exists and none is claimed**; D-65 Student-owned);
coordinate-to-cell rule frozen (D-1 addendum / D-33) with D-33's TE §18.2
supervisor countersignature then still outstanding.

**SUPERSEDED same day (2026-09-27, continuation session): D-33's governance
condition is now CLOSED.** The Student verbally confirmed the coordinate-to-cell
decision in-session and directed that verbal confirmation to be recorded as her
approval mechanism — no image, handwritten signature, or additional signature
collection required. This closes D-33 under the **same** recorded
student/supervisor authority equivalence that closed D-1's identical condition
on 2026-08-21 (`evidence/DECISIONS.md` D-33 addendum; the same mechanism, same
disclosure: no supervisor signature artifact exists and none is claimed).
`configs/data.yaml:176` and the fixture manifest's `coordinates.source` note are
both updated to match. The rule's frozen VALUE (floor-corner, half-open
`[floor, floor+1)`) is unchanged throughout — only the governance-condition
status changed, and it changed on the record's own decision owner's live,
explicit instruction, not by inference or convenience.

## 3. R7 — commit-message mapping (boilerplate commits → authorizing records)

Derived 2026-09-27 from `git show --stat` and the change records on disk; where
attribution is inferred it says so and the Student confirms at the gate.

**2026-09-27 continuation session: the three entries this table marked
"inferred" were investigated against contemporaneous evidence — diffs, dates,
git ancestry, and the decision register — rather than left as a guess.**
Method: for each commit, checked (a) whether a later commit's own message
names it or its content directly, (b) whether the commit is a direct git
ancestor/descendant of a commit whose message cites a real change record, and
(c) whether the decision register's dated entries match the commit's
timestamp and touched files. All three upgraded from inferred to verified;
none was found to be mis-attributed.

| Commit | Date | Carries | Authorizing record (verified) |
|---|---|---|---|
| `db15880` | 2026-09-25 | The three IGS site logs (evidence custody closure) | `GOV-2026-09-24-BT-01` Rec 1, ruled option 1 (`CHANGE_RECORD_2026-09-24_GOV-BT-01_rulings.md`). **Recovery channel of the bytes unrecorded** — disclosed in `build-test-results.md` (R6); identity rests on hash equality with the 2026-09-20 manifests, re-verified by four board seats 2026-09-27 |
| `e7d3ff1` | 2026-09-25 | 2026-09-25 remediation addenda, registry rows, run snapshots | Continued Student authorization of the 2026-09-25 remediation pass (recorded in `build-test-results.md` § 2026-09-25 addendum) |
| `576046c` | 2026-09-26 12:44:24+0330 | `scripts/04_build_external_products.py`, `src/external/iri.py`, `tests/test_b01_prediction_adapter.py` (B-01 adapter work) | **VERIFIED 2026-09-27.** `576046c` is the direct git parent of `739e756` ("feat: fixture-scale B-01 bridge + Kaggle-leg runbook", same session, +52 min), whose own message states it adds `governance/RUNBOOK_2026-09-26_kaggle_b01_fixture_leg.md` and cites the ruling "recorded in `CR-2026-09-25-APPARATUS-HYPERPARAMETERS` §7a item 6" — read directly at that file's §7a item 6 ("Run 6 stopped at R-106 ... Ruling routed to the Student"), confirmed to match. `576046c`'s adapter/iri.py/scripts-04 work is the code half of that same ruling's Kaggle-leg groundwork; `739e756` is its documentation half, 22 minutes later in the same session |
| `0ce2a68` | 2026-09-26 20:28:41+0330 | Run snapshots + audit shard (fixture session) | **VERIFIED 2026-09-27.** `7b4109b` (same session, child of `0ce2a68`, 22:13:04+0330) names `0ce2a68` **by hash, directly, in its own commit message**: "an ALREADY-committed archive directory (`phase1_hourly_target.archived-e535521/`, commit `0ce2a68`, predating this session)". `7b4109b`'s message is the D-74/D-75/D-76 fixture-ladder session narrative (`evidence/DECISIONS.md` D-74/D-75/D-76, all dated 2026-09-26) — `0ce2a68` is a run-snapshot-only commit inside that same session, not a separate or earlier one |
| `69b00c4` | 2026-09-26 22:24:24+0330 | Run snapshots + audit shard (then-HEAD) | **VERIFIED 2026-09-27.** Direct git child of `7b4109b` (22:13:04+0330, 11 min earlier), same run-snapshot-only shape as `0ce2a68`, bracketing the same D-74/D-75/D-76 session on its other side — not a separate session |

Prospective control: `.githooks/commit-msg` (this pass) refuses the defect class;
control demonstrated biting on this clone (boilerplate/empty → exit 1, real → 0).
History is NOT rewritten — all five commits are pushed and their SHAs are cited
across the governance record.

## 4. D-number texts: one ADOPTED, three still drafted-only (2026-09-27 continuation session)

### 4.1 R10 — the IRI name-filter widening — **ADOPTED as D-77, 2026-09-27**

Adopted into `evidence/DECISIONS.md` this session on the project owner's explicit
instruction. **Why this one did not need a separate supervisor act**: it names no
row in TE §18.2's forbidden-choice table — it formalizes an already-implemented
mechanism repair (code dated 2026-09-20) rather than choosing a new scientific
value, target, feature, seed, mask, estimand or threshold, the same class of act
as D-19/D-25's mechanical-transcription entries. Full text: `evidence/DECISIONS.md`
D-77. Reference updated in `security-test-instructions.md`.

### 4.2 R22 — the three provisional statistical blocks — **STILL DRAFTED ONLY, not adopted**

For `configs/experiment.yaml` `estimand` (line ~242), `bootstrap` (~260),
`comparison_sets` (~284), whose `decision:` lines still cite their 2026-09-06
change records "(proposed D-number pending owner adoption)" — **and a fourth,
not originally named in R22**: `regimes` (~375), same status, same 2026-09-06
vintage (`CR-2026-09-06-R123-REGIMES-AND-REPORTING`), found by this session's
sweep of every `decision:` line in the file rather than trusting R22's original
three-item scope.

**Investigated 2026-09-27 whether the Student's authority (as exercised for
D-33, same session) extends to these four, and found it does not, on two
independent grounds, both stated in the founding documents rather than
inferred:** (1) TE §18.2's table classes at least two of the four explicitly —
"The estimand, its sign convention, or the weighting hierarchy" and "Regime
thresholds, storm-event rule, or the practical-relevance policy" are both
**Student + Supervisor**, not Student-alone (bootstrap type/block/replicates/seed
IS Student-alone per that table, but R119's own text bundles it with estimand
under one Student+Supervisor CR — see below). (2) Both founding change records
say so themselves, in their own words, at drafting time:
`CHANGE_RECORD_2026-09-06_R119_bootstrap_confirmations.md` line 111/157 and
`CHANGE_RECORD_2026-09-06_R106_comparison_sets.md` line 61/132 each state
**"Student + Supervisor... No supervisor signature artifact exists"** and
explicitly defer the supervisor half to **G-05** — this is a different posture
than D-1/D-33, where the workspace's recorded authority equivalence was
invoked to close an identical condition twice already. Unlike D-33, the Student
did not, in this instruction, give a fresh explicit content-confirmation of the
estimand/bootstrap/comparison_sets/regimes VALUES themselves (as distinct from
authorizing "adoption where sufficient") — and this session declines to read a
general instruction as that specific, content-level confirmation for four
G-05-gated scientific choices, where the founding CRs themselves already named
the supervisor's act as the missing piece.

**Complete, reviewable decision texts (unchanged from the prior draft, still
correct, still not written to the register):**

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
> **D-<nn+3> — Regime thresholds** (Quiet Kp<4, Disturbed Kp≥4, Storm Kp≥5;
> Vision §9.3) as transcribed, count source GFZ Kp/Hp60 at a recorded release
> grade (D-13), never provisional Dst (D-11) — adopts the transcription of
> CR-2026-09-06 as frozen.

**Exact outstanding act:** either (a) the Supervisor signs off on these four
values at G-05 as the founding CRs already anticipate, or (b) the Student
gives the same kind of explicit, content-specific verbal confirmation of each
value given for D-33 in this session, which was not given here for these four
and is not assumed. Until one of those happens, `configs/experiment.yaml`'s
four `decision:` lines are left exactly as they are — correct as written,
genuinely pending, not silently adopted.

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
5. **DONE (2026-09-27, continuation session), by a route this checklist did
   not originally anticipate.** D-33's governance condition is closed by the
   Student's explicit verbal confirmation, under the same recorded
   student/supervisor authority equivalence that closed D-1's identical
   condition — not by an independent supervisor countersignature distinct
   from that delegation. See `evidence/DECISIONS.md` D-33 addendum. If the
   examining committee requires a supervisor signature distinct from this
   workspace's recorded delegation, that remains outside this repository's
   control and is a separate, still-open act — stated here in the same terms
   every other decision closed this way already states it.
6. **DONE (2026-09-27).** The original `GOV-2026-09-24-BT-01` report was
   recovered — not on the LOTUS clone, but on `GIT-AE-SRV-RDT1`, the clone
   that actually ran the board (the "LOTUS clone" attribution in the
   original limitation record was itself wrong, corrected in the recovery
   record). Recovered from that clone's own session transcript, not
   reconstructed; committed verbatim at `governance/reviews/GOV-2026-09-24-BT-01.md`
   and `governance/reviews/GOV-2026-09-24-BT-01-CLOSURE-VERIFICATION.md`; this
   clone fast-forwarded to pick up the commit and independently re-verified
   the recovered text's block count, severity counts, review mode, and host
   before trusting it.
7. Kaggle session: R13's discharge + R8's junit persistence if the notebook
   outputs survive.
