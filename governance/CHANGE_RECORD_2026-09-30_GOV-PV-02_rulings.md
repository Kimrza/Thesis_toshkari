# CR-2026-09-30-GOV-PV-02-RULINGS: the Student's rulings on GOV-2026-09-29-PV-02

**Status: PARTLY EXECUTED (2026-09-30).**
- The documentation changes in §2 are applied.
- D-83 is at revision 3.
- The D-84 further amendment and the D-24 annotation are **drafted, not written** (§3).
- **No code was changed.** **Nothing was committed.**

**Authority.**
- **What was reviewed.** The consolidated governance report `GOV-2026-09-29-PV-02` was delivered
  in chat on 2026-09-29. It covered two scopes:
  - a **full-board** review of D-83 revision 2;
  - an **adaptive** review of the delta after the `GOV-2026-09-29-PV-01` closure verification.
- **Verdicts.**
  - Stage 4.6 approval: **CONDITIONAL PASS**.
  - D-83 revision 2 as an adoption candidate: **FAIL**.
- **Findings.** 31 in total: Critical 0, High 17, Medium 9, Low 5.
- **Seat positions.** All seven seats returned CONDITIONAL PASS. The Validation Auditor
  **lifted** the PV-01 Rec 2 veto for the revision-2 item 3 text, and **reserved** it for the
  D-number that would characterise `local`.
- **Persistence.** At first the report was not written to `governance/reviews/`. It was later
  persisted on the Student's instruction as `governance/reviews/GOV-2026-09-29-PV-02.md` (see §4
  P-6). *(Corrected 2026-09-30, `GOV-2026-09-30-PV-03` Rec 25.)*
- **Process disclosure from the review.**
  - Three seats wrote temporary files outside the project and deleted them.
  - The TEC seat's cleanup (`rm -f /tmp/tmp.*`) may also have deleted one Git-Bash `/tmp` file
    that was not its own.
  - No project file was touched.

## 1. Rulings (option numbers verbatim, 2026-09-30)

| Rec | Subject (short) | Ruling |
|---|---|---|
| 1 | G-07 evidence path hard-wired to Kaggle | **1**: code ruling to re-key control 30 to the governed environment |
| 2 | Local custody bar not code-enforced | **2**: stays procedural; G-05 preflight assertion detects after the fact |
| 3 | Durability keyed by a coarse label | **1**: characterising D-number removes the exemption and keys by environment identity; non-member refusal test |
| 4 | Durability protocol undefined | **1**: protocol written into D-83 now |
| 5 | No cross-run one-shot guard; (c) reaches restricted root | **3**: DEC-repeat refusal plus required sparse checkout for (c) plus re-hash in (a) |
| 6 | No environment identity per run | **1**: `environment_id` extension, per-run lock items, pin conformance, negative controls |
| 7 | Environment (a) not the locked environment | **2**: keep `tec-thesis-311`; record its full freeze as the governed identity |
| 8 | Environment (c) undefined | **1**: linux-64 lock, fresh clone, CPU guard, same-hardware limitation, Supervisor acknowledgement |
| 9 | Tolerance could be frozen after (c) is seen | **1**: declared freeze order |
| 10 | Confirmatory set / Kaggle fallback | **2**: fallback only for whole-set re-execution |
| 11 | §R2 grep blind spot | **2**: re-derive with platform-role vocabulary, print, add results |
| 12 | Rec 16 carried as "retirement" | **1**: RSS/CPU capture and local `scientific_1month` are **adoption** preconditions |
| 13 | Feasibility trigger; TC-03 envelope | **1**: dormancy exit tied to code rulings; Class C clean run for retirement; local envelope replaces TC-03 |
| 14 | In-environment critical set for (b)/(c) | **1**: critical set inside every environment before a governed run |
| 15 | `--code-commit` override | **1**: Rec 6 guard is a precondition of G-06, G-07 and full-year B-01 |
| 16 | Rec 14 single access log not a precondition | **1**: added to D-83 preconditions |
| 17 | D-84 "full" list incomplete | **1**: further amendment, governed-tree sweep, per-site disposition, D-24 annotated |
| 18 | B-01 smoke-value criterion | **1**: bit-identity |
| 19 | "addendum 1" ambiguous | **1**: cite by date and line |
| 20 | §15.2 change-record fields | **1**: §15.2 block added |
| 21 | "Exactly once" scope; Phase 2 | **1**: once per `phase_id` / `target_definition_id`; disclosure unchanged |
| 22 | B-01 identity checks not in code | **1**: extend `verify_runtime` (code ruling) |
| 23 | MAX_PATH | **1**: preflight records `LongPathsEnabled` or a root-length rule |
| 24 | Stale status pointers | **1**: dated corrections at all sites |
| 25 | Corrective-run preconditions | **1**: clean-root definition, ≥ 2 designated runs, pins exact, narrowed promotion wording |
| 26 | Custody record | **1**: citations fixed, 3 paths added to O-5, in-place rewrite disclosed |
| 27 | November B-01 wheel identity | **2**: label "declared, not measured" |
| 28 | Re-acquisition cross-reference | **Approve** |
| 29 | `locked_test.py` docstring | **Approve**: fix with the next code change to that module |
| 30 | `masks.py` stale comment | **Approve**: fix at the next code change citing D-84 |
| 31 | `experiment.yaml` hash drift | **Approve**: confirmed and disclosed (§2) |

## 2. Executed in this pass (working tree, uncommitted)

| Rec | What changed | Where |
|---|---|---|
| 1–16, 18–23, 28 | D-83 **revision 3** written. Revision 2 is retained verbatim, marked superseded. It adds:<br>• §R1-3 facts;<br>• §R2-3, the re-derived surface list with both derivations printed;<br>• §R3-3 consequences;<br>• §R3a-3, the Vision §15.2 fields;<br>• §R4-3, the D-text;<br>• §R5-3, 19 open items. | `governance/CHANGE_RECORD_2026-09-29_platform_local_only.md` |
| 7 | Pre-restore identity baseline of `tec-thesis-311`: full pip freeze, explicit conda list, interpreter, SHA-256 per file; the drift is derived by script. The drift is 3 of 32 wheel-lock entries; **6** of 61 pip packages sit in neither lock, and 2 drift against the conda lock (`fonttools`, `pytz`); 20 conda packages are installed against 119 in the lock, with 0 build strings matching; Full conda-layer drift: 10 version, 7 build-only, 3 absent from the lock; see the snapshot README table (PV-04 Rec 23). the Python build differs. *(Corrected 2026-09-30, PV-03 Rec 1: this first read "22 of 61 in neither lock".)* | `evidence/environment_identity_2026-09-30_tec-thesis-311/` |
| 7, 24 | A-10 corrected: the D-71 rebuild is on another host, not this one; full drift stated; stale FU-1R pointer removed. The l.17–18 "no defect" claim is qualified. A-6 records that Rec 12 confirmed its reading. | `nfr-validation-matrix.md` |
| 7, 24, 26, 27, 31 | Updates to `load-test-results.md`:<br>• full drift (l.30);<br>• wheel identity declared, not measured, plus the line-ending finding (l.31);<br>• `.gitignore` citation corrected to l.119–120, with the three O-5 paths named;<br>• the in-place rewrite of the canonical C-01 `release_manifest.json` disclosed as a bounded TE §13.3 breach;<br>• the "Kaggle limb" row's FU-1R pointer replaced;<br>• RSS capture marked as an adoption precondition;<br>• step-9 line citation added. | `load-test-results.md` |
| 24, 25 | Heading corrected to FU-1R = A. M-1 preconditions added: citation fix, clean-root definition, ≥ 2 designated runs, exact pins. Q-31 promotion wording narrowed. | `load-test-plan.md` |
| 24 | Diary entries closing FU-1R, the corrective-run choice and the D-83 redraft, plus a remediation deviation entry (append-only) | `memory.md` |
| 26 | Manifest note citation corrected (l.118–119 → l.119–120). JSON re-validated. The manifest's hash is not cited anywhere else. | `artifacts/untracked_outputs_manifest_2026-09-29_pv.json` |
| 26 | O-5 row names the three archived release files and the rewritten canonical manifest | `governance/CHANGE_RECORD_2026-09-29_GOV-PV-01_rulings.md` §4 |
| 17 | §3 annotated to point here | `governance/CHANGE_RECORD_2026-09-29_GOV-PV-01_rulings.md` §3 |

**Rec 31 finding, in full.**
- **What was checked.**
  - The B-01 runtime identity records the `experiment.yaml` hash as `10028bf0b62a…`.
  - That value matches no committed blob.
  - It **does** equal the SHA-256 of the `989f290` blob rendered with CRLF line endings. The LF rendering of that blob is `8427794fcafd…`, which is today's file.
  - Today's working tree is mixed. `data.yaml` and `features.yaml` are CRLF; `experiment.yaml` and `seeds.yaml` are LF (`git ls-files --eol`). `.gitattributes` sets `eol=lf`.
  - `ENVIRONMENT_IDENTITY_ITEMS` (`src/data/fixture_gate.py:141`) includes `config_hashes`.
- **Conclusion.**
  - The content is identical, so run `d139bf12` consumed B-01 rows generated under the same `experiment.yaml` content. That concern is **cleared**.
  - Separately, line-ending churn alone changes the environment identity that D-49 item 4 matches on. That is **disclosed**, and routed as D-83 §R5-3 item 13.

## 3. Rec 17: D-84 further amendment (DRAFT for the Student to adopt; not written to the register)

**Why this is drafted, not written.** `evidence/DECISIONS.md` is the Student's register, and
`project.md` code-generation:c31 says to offer proposed text rather than write into it. The
Student may adopt this text by instructing that it be appended to D-84, or may amend it.

### 3a. Sweep (derived 2026-09-30, printed before this was written)

**Command.** A Python walk over the working tree, excluding:
- `evidence/locked_test_restricted/`, `graphify-out/`, `.git/`, `.claude/worktrees/`, run snapshots, `__pycache__`, and audit shards;
- every file type except `.md`, `.yaml`, `.yml`, `.py`, `.json` and `.txt`.

**Pattern.** `station\s*[×x*]\s*month\s*[×x*]\s*hour|station,\s*month,?\s*(and\s*)?hour` (case-insensitive).

**Result.** **46 lines in 31 files.** This excludes this record's own later self-references.

**Pattern-bounded (added 2026-09-30, PV-03 Rec 22).** The pattern does not match hyphenated or
list-literal forms. A broader re-run (`station.{0,6}month.{0,6}hour`, `station[- ]by[- ]month`,
`month[- ]by[- ]hour`) found **3 more lines**, all of them non-references:
- `src/models/climatology.py` l.35 and l.133 (the limitation text);
- `tests/test_models_smoke.py` l.614 (a negative-control key).

The total is therefore **49**.

**Relabelled (PV-03 Rec 26).** Two sites moved from "historical" to "not a reference":
- CG-01 dispositions l.69 (the D-55 limitation sentence);
- MB `code-summary.md` l.20 (records the supersession).

The counts now sum as 7 + 1 + 21 + 5 + 14 + 1 = 49.

| Disposition | Count | Sites |
|---|---|---|
| **Already listed** in the 2026-09-29 amendment | 7 | Vision l.55 (historical), l.171, l.294, l.775; TE l.458; `constraint-register.md` l.103 (PC-03); `project.md` l.111 |
| **New, forward-looking, in the register** | 1 | `evidence/DECISIONS.md` l.1208: **D-24 item 17**, the canonical protected set (M-03 description) |
| **New, forward-looking, in AI-DLC stage artifacts** (completed stages; annotation needs owner approval per item under `CHANGE_RECORD_PROCEDURE.md`) | 21 | `inception/requirements-analysis/requirements.md` l.394 (FR-P1-05-1), l.414 (FR-P1-05-21); `inception/application-design/components.md` l.159; `inception/delivery-planning/bolt-plan.md` l.1034, l.1197; `inception/practices-discovery/discovered-rules.md` l.57; `inception/units-generation/unit-of-work.md` l.365, l.807; `ideation/intent-capture/intent-statement.md` l.29, l.131; `construction/evaluation-and-comparison/functional-design/business-rules.md` l.695; `construction/evaluation-and-comparison/nfr-requirements/security-requirements.md` l.168; `construction/governance-guards/functional-design/business-logic-model.md` l.451; `construction/models-and-baselines/code-generation/code-generation-plan.md` l.25; `construction/models-and-baselines/functional-design/business-rules.md` l.503 (R-98); `construction/models-and-baselines/functional-design/domain-entities.md` l.65; `construction/models-and-baselines/nfr-design/security-design.md` l.264; `construction/models-and-baselines/nfr-requirements/security-requirements.md` l.130; `construction/models-and-baselines/nfr-requirements/tech-stack-decisions.md` l.80; `construction/regimes-diagnostics-reporting/functional-design/business-logic-model.md` l.373; `construction/regimes-diagnostics-reporting/nfr-requirements/security-requirements.md` l.60 |
| **Historical record**, left as is | 5 | `ideation/approval-handoff/decision-log.md` l.26 (IC-8, as decided at the time); `governance/CHANGE_RECORD_2026-09-20_GOV-CG-01_dispositions.md` l.67 (the D-55 origin); `governance/reviews/GOV-2026-09-20-CG-01.md` l.141; `construction/evaluation-and-comparison/code-generation/code-summary.md` l.962; `construction/regimes-diagnostics-reporting/nfr-requirements/security-requirements.md` l.244 (a review-finding row) |
| **Not a reference to the live key** (the superseding record itself, explanations, or a different subject) | 14 | `evidence/DECISIONS.md` l.4304, 4316, 4326, 4328, 4359 (D-84 itself); `governance/CHANGE_RECORD_2026-09-29_GOV-PV-01_rulings.md` l.56; Vision l.568 (the coverage audit "by station, month, and hour", not M-03); `src/models/climatology.py` l.43 (explains the substitution); `tests/test_models_smoke.py` l.508 (describes the superseded key); **added under PV-03 Recs 22 and 26:** `CHANGE_RECORD_2026-09-20_GOV-CG-01_dispositions.md` l.69; `construction/models-and-baselines/code-generation/code-summary.md` l.20; `src/models/climatology.py` l.35, l.133; `tests/test_models_smoke.py` l.614. **Count: 14** |
| **Stale code comment** | 1 | `src/evaluation/masks.py` l.152, which says the key is "awaiting its D-number and a supervisor countersignature". D-55 was countersigned on 2026-09-21. Fixed at the next code change citing D-84 (Rec 30). |

### 3b. Proposed text, to append to D-84

> **Further amendment (2026-09-30, `GOV-2026-09-29-PV-02` Recommendation 17; <adopted by the
> Student on date>).**
>
> **The claim is narrowed.** The 2026-09-29 amendment called its list "the full, grep-derived
> set". That list covered the authority documents and the memory layers only. It is narrowed to
> that scope.
>
> **The governed tree has now been swept.** The sweep is recorded with a disposition for every
> hit in `governance/CHANGE_RECORD_2026-09-30_GOV-PV-02_rulings.md` §3a: 49 lines in total. Those are
> 46 lines from the pattern `station\s*[×x*]\s*month\s*[×x*]\s*hour|station,\s*month,?\s*(and\s*)?hour`
> and 3 more from a broader hyphen and list-form pattern. The sweep is bounded by those
> patterns and does not claim to be exhaustive.
> It found 22 further forward-looking passages:
> - D-24 item 17 in this register;
> - 21 passages in AI-DLC stage artifacts, including the requirement FR-P1-05-1 and its
>   acceptance row FR-P1-05-21.
>
> Item 1's "wherever it appears" already governs each of them.
>
> **D-24 item 17** is annotated in place (text below), because the protected-set definition is
> gate-bearing at G-P3C.
>
> **Each stage-artifact passage** receives an in-place annotation only with owner approval for
> that item (`CHANGE_RECORD_PROCEDURE.md`), tracked as O-6 part 2. Until then, this entry
> governs.
>
> **Supervisor acknowledgement** remains OPEN.

### 3c. Proposed in-place annotation for D-24 item 17 (`evidence/DECISIONS.md` l.1208)

> *[Annotated <date> under D-84 (further amendment of 2026-09-30), owner-approved: the M-03
> key is **station and hour**, fitted on each partition's own training data only, per D-55. It
> carries D-55's mandatory no-seasonal-term limitation wherever M-03 is reported (D-84 item 2).
> "station×month×hour" above is superseded wording. The protected-set member is M-03 as
> implemented (`src/models/climatology.py`; `configs/experiment.yaml`). The item-17 hash
> **scope** (source plus config) is unchanged; no phase-transition hash exists yet.]*
>
> *(Text revised 2026-09-30, `GOV-2026-09-30-PV-03` Rec 23.)*

## 4. Open (not performable by the agent in this pass)

| # | Item | Owner |
|---|---|---|
| P-1 | Adopt, amend or reject the D-84 further amendment (§3b) and the D-24 annotation (§3c) | Student |
| P-2 | O-6 part 2: approve, item by item, in-place annotations of the 21 stage-artifact passages in §3a | Student |
| P-3 | Every open item in D-83 revision 3 §R5-3 (19 items), including the adoption preconditions, all code rulings, the retry-after-abort rule for DEC, and the full-board re-review of revision 3 | Student; Supervisor |
| P-4 | Rec 29 and Rec 30 comment fixes, done with the next code change to `locked_test.py` or with the next change citing D-84 | Student |
| P-5 | Commit the stage outputs, this record, D-83 revision 3 and `evidence/environment_identity_2026-09-30_tec-thesis-311/`, together with the existing O-5 set | Student |
| P-6 | ~~Whether `GOV-2026-09-29-PV-02` should be persisted to `governance/reviews/`~~ **CLOSED 2026-09-30**: persisted at the Student's instruction as `governance/reviews/GOV-2026-09-29-PV-02.md` (as delivered, with a provenance header) | Student |
