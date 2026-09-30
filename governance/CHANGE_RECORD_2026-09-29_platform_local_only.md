# CR-2026-09-29-PLATFORM-LOCAL-ONLY: local as the sole execution platform (proposed; not enacted)

## Revision 7 (2026-09-30): the current draft

**Status: DRAFT, NOT ENACTED.** No D-number has been written. Adoption needs:
- the Student's adoption act;
- the Supervisor's countersignature (the authority equivalence is not invoked);
- a **full-board review scoped to the revision-7 policy delta** (§A7 and §R4-7), under route (b);
- completion of the §W7 code-generation work package **before the dates in its rows**, not before
  adoption. The Validation Auditor's code-level reservation (veto limb 3, and §R5-5 item 11) is
  carried into that work package explicitly and is not lifted by adoption.

**Form.** Revision 7 is a **delta revision** on revision 6, which is retained verbatim below.
- §A7 amends revision 6 (and, through it, revision 5).
- §R4-7 **replaces the D-text in full**.
- §W7 is the governed code-generation work package that carries the mechanism fixes.
- §R5-7 **restates** the open-items rows that revision 6 superseded, and adds new rows.

Where §A7 and revision 6 disagree, §A7 governs. Every reference below to an open item is
qualified by its table (for example "§R5-5 item 11", "§R5-7 row 35"); an unqualified "item N"
in §R4-7 means that D-text item.

**Basis.**
- The Student's ruling of 2026-09-30 on `GOV-2026-09-30-PV-08` (persisted as
  `governance/reviews/GOV-2026-09-30-PV-08.md`), verbatim: "Recommendation 1-22 = Approve".
- The Student's process choice, verbatim: "b" — policy fixes into the D-text; mechanism fixes into
  a governed code-generation work package.
- The Student's instruction on the three blocked values, verbatim: "do the Rec 10 floor, the Rec 11
  margin and the TC-03 values". §A7 items 8, 16 and 11 carry the resulting **proposed** values and
  rules, each with its derivation. They were drafted by Claude on that instruction and bind only
  through the Student's adoption act and the Supervisor's countersignature of this D-text (project
  rule: no implementer fills a governed value by convenience).
- The ruling record is `governance/CHANGE_RECORD_2026-09-30_GOV-PV-08_rulings.md`.

### A7. Amendments (PV-08 Rec numbers in brackets; P = policy, carried in §R4-7; W = work package, §W7)

1. **December one-shot record store (Rec 1; P + W).** The one-shot key is a **dedicated
   December-generation marker** written at receipt admission **in (a)**; the write-once receipt is
   the second limb; (b)'s own check stays as defence in depth only. Matches are scoped to records
   logged after the cutoff. The 05/06/07 `locked_evaluation` builders must stamp `script_id` and
   `phase_id`. Negative control: a 05 row does not block the first 06 run. Mechanism: §W7 W-1.
2. **Output naming and assembly (Rec 2; W).** Each B-01 half writes outputs named by month-set and
   `phase_id`; the November receipt is never touched. A declared assembly step, with its own
   manifest, joins the halves and asserts equal index SHA-256 and config hashes. Negative control:
   the December run cannot touch the January–November files. Mechanism: §W7 W-2.
3. **January–November run gated (Rec 3; P + W).** §R5-6 row 30 is a precondition of the
   January–November run, not only of December. The CLI form is `--months 1,2,3,4,5,6,7,8,9,10,11`
   (a comma list; `1..11` does not parse, and an omitted `--months` means 1–12). Script 04 gains a
   `--g05-signature` argument (verifier: `splits.py` l.692). `run_gated_generation` is the single
   guard home, with a negative control through the bridge entry. Mechanism: §W7 W-3.
4. **Admission key defined (Rec 4; P + W).** "Admission by lock hash" means: the SHA-256 of the
   **committed per-environment identity file**, plus a passing pin-conformance check. It is not a
   per-run hash (both existing hashes include `code_commit` and `config_hashes`). Negative controls:
   a run on a new commit in admitted (a) passes; a CI run fails. Mechanism: §W7 W-4.
5. **Qualified references; items restated (Rec 5; P).** §R5-5 items 7, 20 and 25 are restated in
   full as §R5-7 rows 7R, 20R and 25R. Every cross-reference in §R4-7 and §R5-7 is qualified.
6. **Durability scope (Rec 6; P + W).** (b) receipts are written to an **NTFS path** (via `/mnt/c`),
   so the NTFS measurement covers them; the 330-trial NTFS scope stands. Before any power-loss trial:
   a verified backup of the repository and `evidence/`, plus a SHA-256 snapshot of both. **One
   injection method:** forced power-off by holding the power button, with AC power disconnected. Mechanism: the durability harness, §W7 W-6.
7. **January–November B-01 before §R5-5 item 4 (Rec 7; P).** New §R5-7 row 35: the
   January–November B-01 run (prerequisites §R5-5 items 13, 14, 16 and §R5-6 row 34) before
   §R5-5 item 4, because `scientific_1month` is March. No cycle results.
8. **Tolerance mapping, binding and the floor (Rec 8 and PV-07 Rec 10; P).**
   - Per file f: **tolerance_f = max(statistic_f, floor_f)**, in f's own units (TECU or TECU²;
     never mixed).
   - Quantities: every output D-74 tolerances **for the fixture being reproduced** (for
     `scientific_1month` this includes `bootstrap_summary.json`).
   - **Floor (proposed value, Student instruction 2026-09-30):**
     floor_f = 2⁻²³ × max|x| over f's toleranced elements in the (a) measuring runs.
     Derivation: 2⁻²³ = 1.1920929 × 10⁻⁷ is float32 machine epsilon, the compute precision of the
     models (`src/models/lstm.py` uses float32). A difference below one epsilon at the file's
     largest magnitude is a representation-level difference, not a reproducibility failure.
     The floor is a rule, not a hand-picked number; it was fixed **before any (c) run exists**, so
     no (c) value informed it. Prior exposure: the (a) plumbing statistic of 0.0 was already seen.
   - The statistic, quantities, floor and cause-fixed standard are carried into D-text item 11.
9. **"Cause fixed", tightened (Rec 9; P).** The diagnostic artifact is SHA-256-hashed and recorded
   **before** any re-run. A code-commit fix supersedes the (a) runs and the tolerance, and triggers
   a D-number when it touches confirmatory code. An environment-only fix is confined to (c).
10. **Kaggle dormancy backed by code (Rec 10; P + W).** A governed run with `TEC_PLATFORM=kaggle`
    is refused (negative control in §R5-5 item 10). The D-text conditions are the **union** of
    §A6 item 6 and D-text item 2. **Retirement ends the fallback.** Mechanism: §W7 W-5.
11. **TC-03 limit (Rec 11 and PV-07 Rec 24; P). Due before any governed acquisition in (a).**
    Proposed rule and values (Student instruction 2026-09-30):
    - **Runtime limb:** any single unattended governed run, in any environment, completes within
      **12 hours wall-clock**. This is TC-03's own inherited value, kept rather than invented.
    - **RAM limb:** peak RSS of any governed run ≤ the **MemTotal of the WSL2 VM, as recorded in
      (c) at the run's G-07 reproduction**, in all three environments. Reason: (c) must reproduce
      (a), so a run that fits (a) but not (c) cannot pass G-07. No `.wslconfig` exists
      (checked 2026-09-30), so the WSL2 default of 50 % of physical RAM applies: nominally
      ≈ 7.8 GiB of the 15.67 GiB installed. The recorded MemTotal, not this nominal figure, governs.
    - **Storage limb:** TC-03a's ≈ 10 GB envelope is unchanged. Observation, not a limit: C: had
      13.06 GiB free on 2026-09-30.
    - A breach of either limb is a failed run, recorded with status and reason (NFR-AUD-01).
    - Peak RSS is not captured today (PV-01 Rec 16); the capture is §W7 W-7.
12. **D-text omissions (Rec 12; P).** Added to §R4-7: "no identifiable cause → G-07 fails and a
    D-number is triggered"; the durability limitation clause; the missing-field and `script_id`
    rules for B-01; and the R-20 exposure clock keyed on `logged_at_utc` only.
13. **Citations corrected (Rec 13; P).** `REQUIRED_FIELDS_MAP` is `config.py` l.572;
    `fixture_manifest.py` refusal messages are l.1681 and l.1684–1689, and l.985; `load_configs`
    is `config.py` l.804. The "LF blob hashes `871be23b` / `1b1ebdfd`" in §A6 item 9 are SHA-256
    content hashes; the git blob IDs are `d181b967` / `6fd73b12`. Relabelled accordingly.
14. **`environment_id`, two representations (Rec 14; P + W).** It is carried both on `RunRecord`
    and as a registry field; both are required and a control asserts they are equal. §R5-5 item 29
    covers `environment_lock_hash` as well as `environment_identity`. Mechanism: §W7 W-4.
15. **Item 9 plan (Rec 15; P).** Supersedes the §A6 item 9 steps with one explicit list:
    1. commit or stash nothing else; `git status` shows only the intended files;
    2. move `configs/data.yaml` and `configs/features.yaml` to a directory **outside the repository**;
    3. `git checkout HEAD -- configs/data.yaml configs/features.yaml`;
    4. verify SHA-256 against `871be23b…` / `1b1ebdfd…`, and `git check-attr eol` = `lf`;
    5. create the hashed `b01_iri` requirements file; reinstall with `--require-hashes`;
    6. measure the (b) identity;
    7. write `interpreter_exception` into `configs/experiment.yaml` under its D-number (§R5-6 row 34),
       then re-run the `eol` check on that file;
    8. re-record **all four** config hashes (the `experiment.yaml` hash from before step 7 is stale);
    9. commit steps 1–8, record the commit, verify `git status` is empty;
    10. run the B-01 fixture from that commit, without `--code-commit`.
    The superseded revision-5 lines of that plan are struck.
16. **Storage margin (Rec 16 and PV-07 Rec 11; P + W).** Form: frozen range **[min − m, max + m]**,
    m in bytes. Proposed rule (Student instruction 2026-09-30):
    **m = max(max − min, ⌈0.10 × max⌉)** over the fixture's measuring runs.
    - Precondition: `storage_total` must exclude archived copies (§W7 W-8). Today it does not: it
      grows by ≈ 2.3 MB per run (14,778,806 → 17,076,359 → 19,375,740 B over `978317da`, `4a959333`,
      `d139bf12`; `load-test-results.md` l.40), so **no frozen range may be computed from the
      existing runs.**
    - Illustration only: applied to the two candidate runs, m = max(2,297,553, 1,707,636) =
      2,297,553 B, range [12,481,253, 19,373,912] — which `d139bf12` exceeds by 1,828 B. That is
      the archive growth, not the margin, and it is why W-8 is a precondition.
    - **Prior exposure disclosed:** the plumbing storage values were seen before this rule was set
      (ML-05). The 10 % term is a Student-owned choice made after that exposure.
17. **Item 8 after item 10 (Rec 17; P).** §R5-5 item 8 (identity capture) is ordered after §R5-5
    item 10 (the `--all` capture).
18. **Governed-log writers (Rec 18; P + W).** The enumeration adds `gate_in_session.py:247`,
    `run_walking_skeleton.py:504` and `merge_coverage_year.py:113`. The closed-log guard also asserts
    that only harness `run_id`s appear. The Kaggle-merge sentence of §R5-5 item 27 is superseded.
    Mechanism: §W7 W-9.
19. **December re-acquisition timing (Rec 19; P).** It runs after §R5-6 row 32 and after the
    §R5-5 item 11 D-number. Driver files whose span includes any December 2022 epoch count as
    December data for this rule.
20. **Rec 13 row; pip capture site (Rec 20; P).** New §R5-7 row 36 for the entry-point refusal
    (§A6 item 13). The `--all` capture site is the `RunRecord.pip_freeze` producer (cited in W-4).
21. **"One run in (c)" (Rec 21; P).** Added to §A6 item 15's superseded list: (c) has **2**
    measuring runs plus the accepted run.
22. **Bounds labelled (Rec 22; P).** 2.95 % and 25.9 % are **one-sided** 95 % zero-failure bounds
    (two-sided Clopper-Pearson: 3.62 % / 30.8 %). §R5-5 item 7 and adoption are not circular: item 7
    is the protocol, adoption does not wait for its trials, and the trials gate §R5-5 item 11 only.

### R4-7. Proposed D-text (replaces §R4-6 in full; for the Student to adopt, amend or reject)

> ## D-83 — Execution platform: local (native Windows plus WSL2 on the Student's laptop) as the sole platform for new governed runs; Kaggle dormant (Student proposal; Supervisor countersignature required)
>
> **Decision date:** <date of adoption>. **Decided by:** the Student on 2026-09-29 (FU-1R = A).
> Revised under the Student's rulings on `GOV-2026-09-29-PV-02`, `GOV-2026-09-30-PV-03`,
> `GOV-2026-09-30-PV-04`, `GOV-2026-09-30-PV-07` and `GOV-2026-09-30-PV-08`.
>
> **Authority amended:** every forward-looking surface in CR-2026-09-29-PLATFORM-LOCAL-ONLY §R2 and
> §R2-5, plus TE §13.1's "eight items" definition. **Ratifies:** D-49 addendum 2.
>
> **Adoption preconditions:** §R5-5 items 2, 3, 4 and 7, as re-dated and restated in §R5-6 and
> §R5-7. The code mechanisms are delivered by the §W7 work package on the dates in its rows; the
> Validation Auditor's reservation on §R5-5 item 11 stands until W-1 and rows 30–31 pass.
>
> **Supervisor countersignature: REQUIRED, OPEN.**
>
> 1. **Platform.** New governed runs execute on `LAPTOP-TV4UGFBC` in three named environments,
>    each recorded per run as `environment_id`, on both the run record and the registry row, which
>    must agree:
>    - **(a)** native-Windows `tec-thesis-311`: every stage script, the confirmatory set, December
>      re-acquisition, and the evaluation-time IRI/GIM join;
>    - **(b)** WSL2 `b01_iri`: only under D-49 and its addenda, only for B-01 generation and
>      `verify_runtime`; its receipts are written to an NTFS path;
>    - **(c)** WSL2 G-07 clean-run: only for G-07 reproduction.
>
>    TE §9.1's "exactly two execution environments" is read as "one platform with three named
>    environments". Its transfer rule stands.
> 2. **Kaggle is dormant, including in code.** A governed run on `kaggle` is refused. A fallback,
>    never covering DEC, may be invoked only under its own D-number and a code ruling adding a
>    non-custody Kaggle identity, and only: on a precommitted closed list of infrastructure failures
>    (host loss, resource exhaustion, durability failure; never dissatisfaction with results); at
>    most once per `phase_id`, before any DEC receipt or `locked_evaluation` record exists; with both
>    draws' validation results reported; with a Kaggle/(a) tolerance leg and an (a) artifact-load /
>    version-conformance check frozen before any Kaggle artifact is accepted; and superseding every
>    local confirmatory artifact for that phase. Kaggle is retired on the evidence of the first
>    instrumented local Class C clean run, and **retirement ends the fallback**. Artifacts already
>    produced on Kaggle keep their provenance.
> 3. **Locked test.**
>    - Until `local` is characterised, no pre-G-05 audit and no G-06 runs on local.
>    - Every restricted-purpose access row logged before the cutoff fails G-05 preflight. The cutoff
>      is the adoption timestamp of the characterising D-number. The check, and the R-20 exposure
>      clock, key on the guard-stamped `logged_at_utc` only; a row without it, or with an
>      unparseable one, fails. No pre-G-05 audit can pass before the cutoff exists.
>    - After the cutoff, admission is by the SHA-256 of the committed per-environment identity file
>      plus passing pin conformance; never by a declared `environment_id`, never by a per-run hash.
>    - G-06 runs CPU-only in (a), once per `phase_id` (from `data.yaml` `target.identity`). A
>      repeated `06` DEC run is refused; a post-cutoff record missing `phase_id` or `script_id`
>      counts as a match. The 05/06/07 builders stamp both fields.
>    - G-07 re-hashes in (a) and never regenerates. (c) never runs DEC and uses a sparse,
>      blob-filtered clone (a procedural control).
>    - `tf_gpu`, and any environment off its governed identity, are barred.
>    - The Phase 2 non-independence disclosure is unchanged.
> 4. **B-01.** D-49 addendum 2 is ratified.
>    - **Before G-05:** B-01 generates January–November only (`--months 1,2,…,11`), after the
>      December code ruling is in force, from a clean recorded commit with renormalised configs,
>      the entry-point identity checks, a bit-identical smoke value, and the November receipt
>      superseded.
>    - **December rows:** generated only after G-05 is signed and verified by `--g05-signature`;
>      once per `phase_id`, in (b); write-once, into outputs named by month-set and `phase_id`;
>      the one-shot key is a December-generation marker admitted in (a); the receipt is re-verified
>      in (a); the halves are joined only by a declared, manifested assembly step.
>    - A missing `phase_id` or `script_id` on a post-cutoff record counts as a match.
> 5. **Preflight and G-07** (TE §9.2, l.858).
>    - In (a) the report shows: conformance to the recorded identity (verification, not rebuild); a
>      completed skeleton run; the §18.3 critical set run in-environment; measured CPU runtime,
>      peak RSS and storage; the long-path state. (c) shows a clean-run reproduction.
>    - The (a)/(c) tolerance is frozen in the precommitted order by item 11's rule.
>    - A failing accepted (c) run fails G-07. A re-run needs the cause-fixed standard of item 11.
>      **No identifiable cause means no re-run: G-07 fails and a D-number is triggered.**
>    - The in-session gate is keyed to `environment_id`.
> 6. **Transfers.** Every transfer between WSL2 and Windows carries a SHA-256 manifest of every file
>    moved, and the transfer is recorded (TE §9.1).
> 7. **CI** is a non-scientific verification surface, bounded as recorded in
>    `governance/CHANGE_RECORD_2026-09-27_platform_bound_RULING_REQUEST.md`. It is never an
>    execution platform and never admitted.
> 8. **Unchanged:** CPU is a complete path and GPU an optional accelerator; while no governed GPU
>    environment exists, the GPU limbs of Vision l.1102 and l.1394 are not applicable. Every
>    locked-test rule, frozen value and re-acquisition obligation is unchanged. December
>    re-acquisition is written from (a) only, after the durability measurement and the
>    characterising D-number; a driver file whose span includes a December 2022 epoch counts as
>    December data.
> 9. **If rejected or amended**, the Kaggle limb of TE §9.2 and TC-03g reverts to an open G-07
>    item. D-49 addendum 2 stands on its own terms.
> 10. **TC-03 replaced** by the measured local envelope and this limit rule, **due before any
>     governed acquisition in (a)**: runtime ≤ 12 h wall-clock per unattended governed run; peak RSS
>     ≤ the (c) WSL2 VM MemTotal recorded at G-07, in every environment; storage per TC-03a. A
>     breach is a failed run, recorded with status and reason. Installed environments are
>     accounted outside TE §9.3. **Binding status: `hard`**, scoped as TC-03's note says; any other
>     choice needs Supervisor countersignature.
> 11. **Precommitted values** (Student decisions, 2026-09-30):
>     - Candidate storage may be zero-width for a candidate composed over ≥ 2 runs (re-rules the
>       earlier board's Rec 5 / ML-04 for storage only).
>     - **Frozen storage range:** [min − m, max + m], m = max(max − min, ⌈0.10 × max⌉) bytes over
>       the measuring runs, computed only from a `storage_total` that excludes archived copies.
>       Disclosure: the plumbing storage values were seen before this rule was set.
>     - **K = 2.** **(c) measuring runs = 2.**
>     - **(c) tolerance:** per file, tolerance = max(statistic, floor), where the statistic is the
>       maximum element-wise |(c) − (a)| over all (a)×(c) run pairs, the floor is 2⁻²³ × max|x|
>       over that file's (a) elements, and the files are every output D-74 tolerances for the
>       fixture reproduced. Runtime and storage are excluded. Units are never mixed across files.
>     - **Cause fixed:** a named diagnostic, SHA-256-recorded before the re-run; a new commit or a
>       recorded environment correction with before/after evidence; a code fix supersedes the (a)
>       runs and the tolerance, and triggers a D-number if it touches confirmatory code; an
>       environment-only fix stays in (c).
>     - **Re-run cap:** PV-03 Rec 6's rule, no numeric cap (re-rules the cap limb of PV-04 Rec 11).
>     - **Durability:** on NTFS, process-kill N = 100 and power-loss N = 10 per fault × write type;
>       one-sided 95 % zero-failure bounds 2.95 % and 25.9 %; one injection method (forced power-off);
>       a verified, hashed backup before any power-loss trial. **Limitation:** admission rests on
>       detection plus the kill-fault evidence; the power-loss result characterises the risk and
>       does not guarantee against it.

### W7. Code-generation work package (mechanism fixes; governed, reviewed with its code)

Delivered through a governed code-generation pass (design + tests + code reviewed together, §18.3
critical set green, pre-commit hook passing). Each item carries its negative controls from §A7.

| # | Mechanism | Due |
|---|---|---|
| W-1 | December-generation marker in (a); write-once receipt limb; post-cutoff scoping; `script_id`/`phase_id` on the 05/06/07 builders (§A7 item 1). Carries VAL veto limb 3 | before any December B-01 generation, and before §R5-5 item 11 |
| W-2 | Per-month-set, per-`phase_id` B-01 output naming; the assembly step and its manifest (§A7 item 2) | before §R5-7 row 35 |
| W-3 | `--g05-signature`; month-12 refusal in `run_gated_generation`; bridge-entry negative control (§A7 item 3; §R5-6 row 30) | before §R5-7 row 35 |
| W-4 | Admission key from the committed identity file; `environment_id` on `RunRecord` and registry with an equality control; `environment_lock_hash` from `fields(RunRecord)`; `--all` pip capture at the `RunRecord.pip_freeze` producer (§A7 items 4, 14, 20) | with §R5-5 items 10 and 29, before §R5-5 item 4 |
| W-5 | Refusal of a governed run on `kaggle` (§A7 item 10) | with §R5-5 item 10 |
| W-6 | Durability harness: NTFS receipt path for (b), backup-and-hash prerequisite, single injection method (§A7 item 6) | before §R5-6 row 32 |
| W-7 | Peak-RSS and CPU-model capture on every governed run (§A7 item 11) | before any governed acquisition in (a) |
| W-8 | `storage_total` excludes archived copies (§A7 item 16) | before the first designated run |
| W-9 | Governed-log enumeration with the three added writers; closed-log guard with harness-only `run_id` assertion (§A7 item 18) | before the pre-G-05 audit |
| W-10 | `_access_timestamp` on `logged_at_utc` only (§R5-6 row 31); entry-point B-01 refusals (§R5-7 row 36) | row-31 part: before the pre-G-05 audit; row-36 part: before §R5-7 row 35 |

### R5-7. Open items: restated rows and additions (§R5-5 and §R5-6 otherwise stand)

| # | Item | Owner | Due |
|---|---|---|---|
| 2 | **Re-dated:** full-board review of the **revision-7 policy delta** (route b) | per `/review-tec-governance` | before adoption |
| 7R | **Restated** (§R5-5 item 7): the durability protocol — `<N>` per §R4-7 item 11; NTFS; one injection method; backup prerequisite; trials recorded per fault × write type | Student | protocol before §R5-6 row 32 |
| 20R | **Restated** (§R5-5 item 20, as extended by §A6 item 3): convert `test_rec5_...`; `len(measuring_run_ids) ≥ 2`; frozen zero-width storage refused without a Student value; frozen-width schema field named; negative controls per §A6 items 3 and 11 | Student | before §R5-5 item 4 |
| 25R | **Restated** (§R5-5 item 25): `<N>` is set (§R4-7 item 11); bounds labelled one-sided | Student | closed on adoption |
| 28 | **Decided (proposed):** floor rule per §A7 item 8 | Student (adoption) | before the (c) measuring runs |
| 33 | **Decided (proposed):** storage-margin rule (§A7 item 16) and TC-03 limit rule (§A7 item 11). **TC-03 re-dated: before any governed acquisition in (a)** | Student (adoption) | per §A7 |
| 35 | **New:** January–November B-01 run (prerequisites §R5-5 items 13, 14, 16; §R5-6 rows 30, 34; W-2, W-3) | Student | before §R5-5 item 4 |
| 36 | **New:** entry-point B-01 refusal (§A6 item 13), in W-10 | Student | before §R5-7 row 35 |
| 37 | **New:** the §W7 work package, as a governed code-generation pass | Student | per W rows |

---

## Revision 6 (superseded 2026-09-30 by Revision 7; retained verbatim as the base text that §A7 amends)

**Status: DRAFT, NOT ENACTED. NOT READY for adoption.** No D-number has been written. Adoption
needs three things:
- the Student's adoption act;
- the Supervisor's countersignature (the authority equivalence is not invoked, because D-129 is
  amended);
- a **full-board review of revision 6**, which has not yet run.

**Form.** Revision 6 is a **delta revision**:
- Revision 5, retained verbatim below, stays the base text.
- §A6 amends it item by item.
- §R4-6 **replaces the D-text in full**.
- §R5-6 adds rows to the §R5-5 open-items table and re-dates some of its rows.

Where §A6 and revision 5 disagree, §A6 governs.

**Basis.**
- The Student's ruling of 2026-09-30 on `GOV-2026-09-30-PV-07` (persisted as
  `governance/reviews/GOV-2026-09-30-PV-07.md`), verbatim: "all of your recommendations are
  approved with the option you recomend". This takes route (a): stage 4.6 is closed and D-83
  continues on its own track.
- The Student's later choices, the same day:
  - **Rec 6:** dormant.
  - **Rec 13:** entry-point refusal.
  - **Recs 10 and 11:** values deferred (BLOCKED).
- The ruling record is `governance/CHANGE_RECORD_2026-09-30_GOV-PV-07_rulings.md`.

**Validation Auditor position** (after PV-07). The veto stays reserved on the characterising
D-number (§R5-5 item 11).
- Lifted: a DEC read on Kaggle.
- Kept, to be closed by §A6 items 1, 4 and 5:
  - the G-05 exemption loophole;
  - `_access_timestamp`;
  - the uncoded December B-01 one-shot.

### A6. Amendments to revision 5 (PV-07 Rec numbers in brackets)

1. **December B-01 (Rec 1).** Replaces the §R6-5 #26 proposal and amends §R3-5 items 12 and 15.
   - **"Full-year B-01 run" is split in two:**
     - a **pre-G-05 run over January–November only** (`--months 1..11`, labelled partial);
     - a **post-G-05 December-only run**.

     Every "before any full-year B-01 run" in revision 5 now means the January–November run.
   - **Code ruling** (new §R5-6 row 30), in `iri.run_gated_generation` or at the script-04 entry.
     It holds even though `build_target_grid` defaults to months 1–12 (`iri.py` l.672):
     - refuse month 12 unless `verify_g05_signature` passes;
     - make the output write-once (script 04 overwrites today);
     - write a prediction-hash receipt in (b) at generation, and re-verify it in (a) after
       transfer;
     - refuse a second generation per `phase_id` with `script_id="04_build_external_products"`,
       treating a missing field as a match;
     - negative controls: month 12 without a signature, a second December generation, a record
       with a missing field, a receipt mismatch after transfer.
   - Owner: Student and Supervisor (locked-test protocol).
2. **Precommitted values bind through the D-text (Rec 2).** The Student decisions of 2026-09-30 in
   §R6-5 are carried by **D-text item 11** (§R4-6).
3. **Re-rulings labelled (Rec 3).**
   - **The cap limb of PV-04 Rec 11 is re-ruled.** The re-run cap is PV-03 Rec 6's rule, with no
     numeric cap. §R3-5 item 5 and §R5-5 item 28 are read accordingly.
   - **The earlier board's Rec 5 / ML-04 zero-width guard is re-ruled for `storage_total` only.**
     That guard is cited in the `fixture_manifest.py` refusal messages at l.1682–1683 and
     l.1858–1859. `cpu_total` stays non-zero.
   - Code (§R5-5 item 20, extended):
     - convert `tests/test_clean_run.py` `test_rec5_...` rather than deleting it;
     - key the "≥ 2 runs" check on `len(measuring_run_ids)`;
     - add a frozen-manifest refusal of a zero-width storage range that carries no Student value;
     - name the frozen-width schema field (the template's `min_bytes` does not match `min`);
     - negative controls: a single run, a duplicated run id, a zero-width `cpu_total`, a frozen
       zero-width range with no value.
4. **G-05 exemption deleted (Rec 4; closes veto limb 1).**
   - In §R3-5 item 1(a), the clause "unless its `run_id` resolves to a registry row whose
     `environment_id` or lock hash identifies an admitted, characterised environment" is
     **struck**.
   - **Every pre-cutoff restricted-purpose access row fails.**
   - After the cutoff, admission (item 1(c)) is **by lock hash only**, never by the declared
     `environment_id`.
   - New negative control: a pre-cutoff row that resolves to a later-admitted environment fails.
5. **`_access_timestamp` (Rec 5; closes veto limb 2).** Code ruling (new §R5-6 row 31):
   - `experiment_registry._access_timestamp` (l.290–302) keys on the guard-stamped `logged_at_utc`
     only;
   - negative control: a forged `retrieved_at_utc` does not delay the R-20 exposure clock.
6. **Kaggle fallback dormant (Rec 6; the Student chose "Dormant").** Amends §R3-5 item 6 and
   D-text item 2.
   - The fallback is **dormant in code**. There is no Kaggle `environment_id`. Invoking it needs
     its own D-number, plus a code ruling that adds a non-DEC, non-custody Kaggle identity with a
     negative control refusing DEC.
   - Revision 5's "never supply part of that set" wording is superseded.
   - Binding conditions on any future invocation:
     - a **closed list of infrastructure-failure triggers**: host loss, resource exhaustion,
       durability failure. Dissatisfaction with validation results is excluded;
     - **at most one invocation per `phase_id`**;
     - **both draws' validation results reported**;
     - a **Kaggle/(a) tolerance leg plus an artifact-load / version-conformance check in (a)**,
       frozen before the Kaggle artifacts are accepted.
7. **`environment_id` storage (Rec 7).** Amends §R3-5 item 9 and §R5-5 item 10.
   - `environment_lock_hash` (`config.py` l.1310–1328) is derived from `dataclasses.fields(RunRecord)`.
     Today it hand-lists 8 names.
   - A registry extension field `environment_id` is added.
   - `load_configs` / `resolve_platform_roots` (`config.py` l.746–784) carry `environment_id` into
     `ConfigSnapshot`.
   - Control 31 (`fixture_gate.py` l.840–848) is widened to compare `environment_id` and identity.
   - Negative controls:
     - two locks that differ only in `environment_id` hash differently;
     - a registry row without the field fails the G-05 preflight.
8. **Pin conformance, one rule per layer (Rec 8).** Amends §R3-5 items 3 and 9.
   - **Pip:** `name==version` over `pip freeze --all`, with the `pip @ file:///...` line as a
     listed exception.
   - **Conda:** exact match of the explicit URL line (name, version, build) **plus** md5.
   - The duplicated bullets in revision 5 item 9 are struck.
   - **Ordering:** `environment_id`, the `--all` capture and the item 29 non-comparability D-number
     land **together, before §R5-5 item 4**, so item 4's evidence is comparable when it is
     created. This answers the item 24 ordering question: **earlier**.
   - The D-number act lives only in item 29. It is struck from item 24.
9. **PV-03 Rec 12 execution plan, corrected (Rec 9).** Amends the §R6-5 plan.
   - **Step 5 (renormalise).** `git checkout -- <file>` does nothing on stat-clean files, so force
     the rewrite:
     1. move `data.yaml` and `features.yaml` aside;
     2. run `git checkout HEAD -- configs/data.yaml configs/features.yaml`;
     3. verify against the LF blob hashes `871be23b` and `1b1ebdfd`.
   - **New step 2a.** Create the hashed `b01_iri` requirements file and reinstall with
     `--require-hashes` **before** measuring the (b) identity. Steps 2 and 3 are swapped.
   - **New step 2b.** Freezing the measured identity into `configs/experiment.yaml`
     `interpreter_exception` is a governed config change. It carries its own D-number (§R5-6 row
     34). Re-record the four config hashes afterwards.
   - **New step 6a.** Commit steps 1–5, record the commit, and verify that `git status` is empty.
     Step 7 then runs from that clean, recorded commit, without `--code-commit`.
10. **(c) tolerance and "cause fixed" (Rec 10).** Amends §R3-5 item 5 and §R5-5 item 28.
    - **Statistic:** the maximum element-wise |(c) − (a)| over all (a)×(c) run pairs.
    - **Quantities:** the D-74 toleranced outputs only (`predictions.parquet`, `metrics.json`).
      Runtime and storage are excluded.
    - **(c) measuring runs = 2** (a Student decision).
    - **Zero→positive floor: BLOCKED.** The Student sets it in the precommit file before the first
      (c) measuring run. No value is supplied here.
    - **"Cause fixed" evidence standard:**
      - the cause is identified by a named diagnostic artifact;
      - the fix is a new commit or a recorded environment correction, with before/after evidence;
      - "no identifiable cause" means no re-run: G-07 fails, and a D-number is triggered.
11. **Frozen storage width (Rec 11).**
    - Rule: the frozen storage range is the measured value ± a margin precommitted in the M-1
      precommitment file.
    - **The margin is BLOCKED.** The Student sets it before the first designated run.
    - Extra negative controls:
      - a zero-width `cpu_total` is still refused;
      - a duplicated `measuring_run_id` is refused;
      - a second run reusing the first run's outputs is refused, so independent clean-root
        execution is required.
12. **`phase_id` source (Rec 12).** It is taken from `configs/data.yaml` `target.identity.phase_id`,
    as carried on the bundle (`train.py:516`). Revision 5 cited `experiment.yaml` l.501, which is
    the B-01 stamp. Negative control: assert that the bundle's `phase_id` equals
    `benchmark_b01.stamps.phase_id`.
13. **B-01 identity refusals at the entry point (Rec 13; the Student's variant).**
    - The TBD refusal is placed in `verify_runtime` and at the `--generate-benchmark` entry.
    - `REQUIRED_FIELDS_MAP` is left unchanged (`config.py` l.604–609).
    - `read_benchmark_contract` / `BenchmarkContract` are extended with the `interpreter_exception`
      fields.
    - A refusal test joins the §18.3 critical set.
    - Negative control: a script-04 GIM-join run in (a) is **not** refused.
    - PV-04 Rec 20's `REQUIRED_FIELDS_MAP` limb is amended accordingly.
14. **Script-04 mode table (Rec 14).** Amends §R3-5 item 15.
    - B-01 generation is `_generate_benchmark` (script 04 l.1720) → `iri.run_gated_generation`
      (iri.py l.958).
    - `verify_runtime` is called at l.1671 **and** l.1704.
    - `_attempt_benchmark` / `iri.generate_benchmark` (l.1625/1633) gets its own row: "any
      environment; always refuses (negative control)".
15. **Stale text superseded (Rec 15).** These revision-5 passages are superseded by §A6 and by the
    Student decisions:
    - item 6's "whole set / never part";
    - the "conditional" K text. K = 2 stands; the first designated run waits for the item 20 code
      change;
    - the "BLOCKED" rows for the cap and `<N>`;
    - "not resolved here". Contradictions 1 and 2 are resolved, and contradiction 3 is addressed by
      §A6 item 1;
    - item 1(b)'s "no value is supplied here". `<N>` is now set;
    - §R5-5 items 7, 20 and 25.

    "Item 6's SHA-256 manifest" means **§R4-5 / §R4-6 item 6 (Transfers)**.
16. **`<N>`, precisely (Rec 16).**
    - N is counted per **fault type × write type × filesystem**: 100 process-kill and 10
      power-loss trials each for the access-row, registry-row and receipt writes. That is 330
      trials per filesystem.
    - The power-loss injection method is named in the protocol before measurement: forced
      power-off, or battery removal where the hardware allows it.
    - Exact zero-failure 95% bounds: **2.95%** (N = 100) and **25.9%** (N = 10).
    - The characterising D-number (item 11) must state two things:
      - admission rests on detection plus the kill-fault evidence;
      - the power-loss result characterises the risk rather than guaranteeing against it.
17. **Durability measurement row (Rec 17).** New §R5-6 row 32, placed before item 11.
18. **D-text completeness (Rec 18).** See §R4-6.
    - Item 3 now states the missing-field fail-closed rule, the `logged_at_utc`-only key, and that
      no audit can pass before the cutoff.
    - The provenance adds PV-04 and PV-07.
    - "Rec 47" is named by its record, `CHANGE_RECORD_2026-09-27_platform_bound_RULING_REQUEST.md`.
19. **Governed access logs (Rec 19).** Restates §R5-5 item 27. Current state:
    - the test suite already writes to the gitignored `artifacts/exec_evidence/test_access_log.jsonl`,
      and has done since 2026-09-20;
    - `evidence/test_run_access_log.jsonl` (5,964 rows) is the **closed governed** log, still read
      by script 00 (l.329–330);
    - stage scripts 01–07 target `evidence/merge_run_access_log.jsonl`, which does not exist.

    Item 27 therefore becomes:
    - enumerate the governed logs;
    - exclude the closed log by path;
    - add a closure guard that refuses any append to it, with a negative control.
20. **`script_id` scope (Rec 20).** `script_id` is required only on records with
    `purpose="locked_evaluation"`. Other `AccessRecord` builders (`inventory.py`,
    `locked_test.py:674`, `merge_coverage_year.py`) are unaffected.
21. **December re-acquisition (Rec 21).** It is written from environment (a) only (§R3-5 items 1(c)
    and 14).
22. **TC-03 limit (Rec 24).** Before G-07, the measured local envelope (§R3-5 item 7) must name a
    **limit-derivation rule**, so that `hard` binds something. An example is a peak-RSS ceiling
    under the WSL2 cap. The rule and its values are the Student's.
23. **Qualifier (Rec 25).** The "2.3 GB" in §R3-5 item 7 carries "(reviewer measurement, authority
    level 6)".

### R4-6. Proposed D-text (replaces §R4-5 in full; for the Student to adopt, amend or reject)

> ## D-83 — Execution platform: local (native Windows plus WSL2 on the Student's laptop) as the sole platform for new governed runs; Kaggle dormant (Student proposal; Supervisor countersignature required)
>
> **Decision date:** <date of adoption>. **Decided by:** the Student on 2026-09-29 (FU-1R = A).
> Revised under the Student's rulings on `GOV-2026-09-29-PV-02`, `GOV-2026-09-30-PV-03`,
> `GOV-2026-09-30-PV-04` and `GOV-2026-09-30-PV-07`.
>
> **Authority amended:** every forward-looking surface in CR-2026-09-29-PLATFORM-LOCAL-ONLY §R2 and
> §R2-5, plus TE §13.1's "eight items" definition. **Ratifies:** D-49 addendum 2.
>
> **Adoption preconditions:** §R5-5 items 2, 3, 4 and 7, with the §R5-6 re-dates.
>
> **Supervisor countersignature: REQUIRED, OPEN.** The authority equivalence is not invoked.
>
> 1. **Platform.** New governed runs execute on `LAPTOP-TV4UGFBC` in three named environments,
>    each recorded per run as `environment_id`:
>    - **(a)** native-Windows `tec-thesis-311`. Its governed identity is its hashed post-restore
>      freeze. It is the environment for every stage script, the confirmatory set, December
>      re-acquisition, and the evaluation-time IRI/GIM join.
>    - **(b)** WSL2 `b01_iri`. It is used only under D-49 and its addenda, and only for B-01
>      generation and `verify_runtime`.
>    - **(c)** WSL2 G-07 clean-run. It is used only for G-07 reproduction.
>
>    TE §9.1's "exactly two execution environments" is read as "one platform with three named
>    environments". Its transfer rule stands.
> 2. **Kaggle is dormant, including in code.** No governed run executes on Kaggle. A fallback, never
>    covering DEC, may be invoked only under its own D-number and a code ruling that adds a
>    non-custody Kaggle identity. Every invocation is bound as follows:
>    - it is triggered only by a precommitted closed list of infrastructure failures;
>    - it happens at most once per `phase_id`, before any DEC receipt or `locked_evaluation` record
>      exists;
>    - both draws' validation results are reported;
>    - a Kaggle/(a) tolerance leg is frozen before any Kaggle artifact is accepted;
>    - every local confirmatory artifact for that phase is superseded.
>
>    Kaggle is retired on the evidence of the first instrumented local Class C clean run.
>    Artifacts already produced on Kaggle keep their provenance.
> 3. **Locked test.**
>    - Until `local` is characterised, no pre-G-05 audit and no G-06 runs on local.
>    - **Every restricted-purpose access row logged before the cutoff fails G-05 preflight.**
>      - The cutoff is the adoption timestamp of the characterising D-number.
>      - The check is keyed on the guard-stamped `logged_at_utc` only.
>      - A row without it, or with an unparseable timestamp, fails.
>      - **No pre-G-05 audit can pass before the cutoff exists.**
>    - After the cutoff, admission is by lock hash only.
>    - G-06 runs CPU-only in (a), with pins conforming to the hashed recorded identity, **once per
>      `phase_id`**. `phase_id` is taken from `data.yaml` `target.identity`.
>    - Code refuses a repeated `06` DEC run. A record missing `phase_id` or `script_id` counts as a
>      match and is refused.
>    - G-07 re-hashes in (a) and never regenerates.
>    - (c) never runs DEC and uses a sparse, blob-filtered clone. This is a procedural control.
>    - `tf_gpu`, and any environment off its governed identity, are barred.
>    - The Phase 2 non-independence disclosure is unchanged.
> 4. **B-01.**
>    - D-49 addendum 2 is ratified.
>    - **Before G-05:** B-01 generates January–November only.
>    - **December rows:**
>      - generated **only after G-05 is signed**;
>      - once per `phase_id`, in (b);
>      - write-once, with a receipt written at generation and re-verified in (a);
>      - code refuses month 12 without a verifying G-05 signature.
>    - **The January–November run additionally requires:**
>      - the D-49 addendum-2 extension to the B-01 fixture runs;
>      - the entry-point identity checks;
>      - a bit-identical smoke value;
>      - renormalised configs, with the November receipt superseded, then a B-01 fixture re-run
>        from a clean, recorded commit.
> 5. **Preflight and G-07** (TE §9.2, l.858).
>    - In (a), the report shows:
>      - installation conforms to the recorded identity (verification, not rebuild);
>      - a completed skeleton run;
>      - the §18.3 critical set run in-environment;
>      - measured CPU runtime, peak RAM and storage;
>      - the long-path state.
>    - (c) shows a clean-run reproduction.
>    - The (a)/(c) tolerance is frozen in the precommitted order, using the precommitted statistic
>      and quantities.
>    - A failing accepted (c) run fails G-07. Re-runs are permitted only under the "cause fixed"
>      evidence standard.
>    - The in-session gate is keyed to `environment_id`.
> 6. **Transfers.** Every transfer between WSL2 and Windows carries a SHA-256 manifest of every file
>    moved, and the transfer is recorded (TE §9.1).
> 7. **CI** is a non-scientific verification surface. It is bounded as recorded in
>    `governance/CHANGE_RECORD_2026-09-27_platform_bound_RULING_REQUEST.md` (the "Rec 47" bound in
>    `verify.yml`). It is not an execution platform and never an admitted custody environment.
> 8. **Unchanged:**
>    - CPU is a complete path, and GPU is an optional accelerator. While no governed GPU environment
>      exists, the GPU limbs of Vision l.1102 and l.1394 are **not applicable**.
>    - Every locked-test rule and every frozen value is unchanged.
>    - The re-acquisition obligations are unchanged.
> 9. **If rejected or amended**, the Kaggle limb of TE §9.2 and TC-03g reverts to an open G-07
>    item. D-49 addendum 2 stands on its own terms.
> 10. **TC-03 replaced.** TC-03 is replaced by the measured local envelope, with a named
>     limit-derivation rule. Installed environments are accounted outside TE §9.3.
>     **Binding status: `hard`, scoped as TC-03's note says.** Any other choice is a downgrade and
>     requires Supervisor countersignature.
> 11. **Precommitted values** (Student decisions, 2026-09-30):
>     - **Candidate storage:** `storage_total` may be zero-width for a *candidate* composed over at
>       least 2 runs. This re-rules the earlier board's Rec 5 / ML-04 for storage only. A frozen
>       range needs the Student's value.
>     - **K = 2.**
>     - **(c) measuring runs = 2.**
>     - **Re-run cap:** for the accepted (c) run, PV-03 Rec 6's rule with no numeric cap. This
>       re-rules the cap limb of PV-04 Rec 11.
>     - **Durability trials:** process-kill N = 100 and power-loss N = 10, per fault × write type ×
>       filesystem. Exact bounds: 2.95% and 25.9%.
>     - **Still to be set by the Student before first use:** the (c) tolerance floor, the frozen
>       storage margin, and the TC-03 limit values.

### R5-6. Open items: additions and re-dates (§R5-5 otherwise stands)

| # | Item | Owner | Due |
|---|---|---|---|
| 2 | **Re-dated:** full-board review of **revision 6**, scoped to G-06 and G-07 | per `/review-tec-governance` | before adoption |
| 10 | **Re-dated:** `environment_id`, the `--all` capture and pin conformance **land together** with item 29 | Student | **before item 4** |
| 20 | **Extended** per §A6 item 3 | Student | before item 4 |
| 24 | **Amended:** the D-number act is removed (it now lives in item 29 only). The refusal-scope ruling remains | Student | before item 10 |
| 27 | **Restated** per §A6 item 19 | Student | before the pre-G-05 audit |
| 28 | **Partly decided:** statistic, quantities, (c) = 2 and the cause-fixed standard are recorded. **Floor BLOCKED** | Student | floor: before the (c) measuring run |
| 29 | **Re-dated:** lands with item 10 | Student | before item 4 |
| 30 | **New:** December B-01 code ruling (§A6 item 1) | Student + Supervisor | before any December B-01 generation, and before item 11 |
| 31 | **New:** `_access_timestamp` keyed on `logged_at_utc` only (§A6 item 5) | Student | before the pre-G-05 audit, and before item 11 |
| 32 | **New:** run the durability measurement (NTFS; 330 trials; injection method recorded) under the item 7 protocol | Student | before item 11 |
| 33 | **New:** set the storage margin (§A6 item 11), and the TC-03 limit rule and its values (§A6 item 22) | Student | margin: before the first designated run; TC-03: before G-07 |
| 34 | **New:** the identity-freeze D-number for `interpreter_exception` (§A6 item 9, step 2b) | Student | before item 13 |

---

## Revision 5 (superseded 2026-09-30 by Revision 6; retained verbatim as the base text that §A6 amends)

**Status: DRAFT, NOT ENACTED. It is NOT READY for adoption.** §R5-5 lists the items that
must be closed first. It is **not ready** because the Student's ruling on PV-02 Rec 12 makes a
measurement and a code ruling **preconditions of adoption**, and neither exists yet.

*Corrected 2026-09-30 under PV-03 Rec 20:*
- Revision 3 said that PV-02 Rec 16 was also an adoption precondition. It is not: it is a custody
  precondition, due before the pre-G-05 audit.
- **Citation convention:** "PV-01 Rec N", "PV-02 Rec N" and "PV-03 Rec N" name the board. An
  unprefixed "Rec" appears only in the rulings tables below.

- No D-number has been written. `evidence/DECISIONS.md` is the Student's register. The D-text in
  §R4-5 is offered for the Student to adopt, amend or reject.
- The Supervisor must countersign. The authority equivalence is **not** invoked, because this
  amends Vision D-129 (PV-01 Rec 19).
- Revision 5 needs a **full-board re-review** before adoption. `GOV-2026-09-30-PV-04` reviewed
  revision 4; nothing has reviewed revision 5 yet.

**Basis.** Revision 2, below, retained verbatim and marked superseded. On top of it come the
Student's rulings of 2026-09-30 on `GOV-2026-09-29-PV-02`, recorded in
`governance/CHANGE_RECORD_2026-09-30_GOV-PV-02_rulings.md`:

| Rec | Option | Rec | Option | Rec | Option |
|---|---|---|---|---|---|
| 1 | 1 | 9 | 1 | 16 | 1 |
| 2 | 2 | 10 | 2 | 18 | 1 |
| 3 | 1 | 11 | 2 | 19 | 1 |
| 4 | 1 | 12 | 1 | 20 | 1 |
| 5 | 3 | 13 | 1 | 21 | 1 |
| 6 | 1 | 14 | 1 | 22 | 1 |
| 7 | 2 | 15 | 1 | 23 | 1 |
| 8 | 1 | | | | |

It also incorporates:
- PV-02 Rec 27 = 2;
- PV-02 Recs 28–31 approved.

**Revision 4** applies the Student's rulings of 2026-09-30 on `GOV-2026-09-30-PV-03`:

| Rec | Option | Rec | Option | Rec | Option |
|---|---|---|---|---|---|
| 1 | 1 | 7 | 1 | 12 | 3 |
| 2 | 1 | 8 | 1 | 13 | 1 |
| 3 | 1 | 9 | 1 | 14 | 1 |
| 4 | 1 | 10 | **2** | 15–31 | Approve |
| 5 | 1 | 11 | 1 | | |
| 6 | 1 | | | | |

Revision 3 is retained verbatim below, marked superseded.

**Revision 5** applies the Student's rulings of 2026-09-30 on `GOV-2026-09-30-PV-04`
(persisted at `governance/reviews/GOV-2026-09-30-PV-03.md` for PV-03; PV-04 was chat-only at the time; it has since been persisted as `governance/reviews/GOV-2026-09-30-PV-04.md`. Corrected under PV-05 Rec 8):

| Rec | Option | Rec | Option | Rec | Option |
|---|---|---|---|---|---|
| 1 | 1 | 6 | 1 | 11 | 1 |
| 2 | 1 | 7 | **2** | 12 | 1 |
| 3 | 1 | 8 | 1 | 13 | 1 |
| 4 | 1 | 9 | 1 | 14 | **2** |
| 5 | **2** | 10 | 1 | 15–32 | Approve |

**PV-04 Rec 7 = 2 re-rules PV-02 Rec 10 and PV-03 Rec 4.** The "whole confirmatory set,
including DEC" fallback is replaced by a fallback that excludes DEC. The Student chose this
knowing it creates a mixed-platform confirmatory set (§R3-5 item 6).

Revision 4 is retained verbatim below, marked superseded.

**Verification of the board prefixes (PV-04 Rec 1).** After revision 5 was written, every
"PV-0x Rec N" in it was checked against the three rulings tables, and the result was printed.
See the PV-04 rulings record §2.

**Validation Auditor position** (PV-02, updated by PV-03 and PV-04):
- The PV-01 Rec 2 veto against item 3 is **lifted** for the revision-2 text.
- It is **reserved** for the future D-number that would characterise `local` (§R3-5 item 1).
- PV-03 modified the reservation. It now also covers any adoption that keeps revision 3's
  DEC-refusal text or G-05 assertion text. Revision 4 replaces both (§R3-5 items 1(a) and 2,
  under PV-03 Recs 2 and 3).
- PV-02 Rec 2 = 2 narrows the reservation's condition 3 to its test limb. The Validation Auditor
  accepts that only in the fail-closed form written in §R3-5 item 1(a).
- **PV-04 modified the reservation again.** The limb covering the revision-3 texts is discharged.
  The reservation now also covers any adoption that:
  - keys the G-05 assertion on `retrieved_at_utc` (PV-04 Rec 4);
  - lets a DEC read happen on an uncharacterised Kaggle (PV-04 Rec 7);
  - admits a record that lacks a field (PV-04 Rec 15).

  Revision 5 addresses all three: §R3-5 items 1(a), 6 and 2.

### R1-5. Facts (revision 2 §R1 stands; these are added or corrected)

| Fact | Source |
|---|---|
| **Environment (a) is not the locked environment.** Pip layer: 3 of 32 `wheels-win64.lock` entries drift. They are `ml_dtypes` 0.5.4 vs 0.5.3, `setuptools` 83.0.0 vs 84.0.0 and `wheel` 0.47.0 vs 0.48.0. **6** of 61 pip packages appear in neither lock (`distlib`, `filelock`, `platformdirs`, `python-discovery`, `uv`, `virtualenv`). A further 16 are pinned in `conda-win64.lock`, including `scipy` 1.17.1, which matches; two of those drift (`fonttools` 4.65.0 vs 4.66.0, `pytz` 2026.3.post1 vs 2026.4). Conda layer: 20 packages installed against 119 in the lock, and **0 of the 20 build strings match**. Full conda-layer drift: 10 version, 7 build-only, 3 absent from the lock; see the snapshot README table (PV-04 Rec 23). *(Corrected under PV-03 Rec 1; revision 3 said "22 of 61 in neither lock" because the conda lock was never checked.)* Python build: `hb00fc5c_0` from Anaconda `pkgs/main`, where the lock pins conda-forge `hb12b558_2`. This **corrects revision 2 §R1 row 4**, which reported a single-pin drift. | `evidence/environment_identity_2026-09-30_tec-thesis-311/README.md` (derived by script, printed) |
| **The G-07 preflight evidence path refuses every platform but Kaggle.** `require_in_session_gate` refuses `platform != "kaggle"` (control 30). `gate_in_session.py` refuses to run anywhere but Kaggle. `build_environment_and_cpu_preflight_report` requires the in-session gate result. | `src/data/fixture_gate.py:830`; `scripts/gate_in_session.py:230`; `src/data/fixture_evidence.py` l.686–711 |
| **The local exemption is hard-coded.** `platform_label != "local" and …`. The platform enum is exactly `kaggle \| local`. CI declares `TEC_PLATFORM: local`. | `src/data/locked_test.py:497`, `:760`; `src/data/config.py:764`; `.github/workflows/verify.yml:103` |
| **Nothing records the environment per row.** No registry column or extension holds it. `capture_environment_lock` folds `pip freeze` into a hash only. | `src/data/experiment_registry.py:102–123`; `src/data/config.py:1257–1311` |
| **Write-once is enforced per path, not per run.** DEC predictions go under a per-`run_id` directory. | `scripts/06_train_and_predict.py:722`, `:1698`, `:1811`; `src/models/train.py:1575` |
| **The B-01 config hashes differ from today's only in line endings, not in content.** The recorded `experiment.yaml` hash `10028bf0…` equals the CRLF rendering of the `989f290` blob. `data.yaml` and `features.yaml` are still CRLF in the working tree. `experiment.yaml` and `seeds.yaml` are LF, although `.gitattributes` sets `eol=lf`. `ENVIRONMENT_IDENTITY_ITEMS` includes `config_hashes`, so a line-ending change alone changes the environment identity that D-49 item 4 matches on (PV-02 Rec 31). | `b01_runtime_identity.json`; `git show 989f290:configs/experiment.yaml`, rendered with CRLF, then `sha256sum`; `git ls-files --eol configs/*.yaml`; `src/data/fixture_gate.py:141` |
| **The November B-01 rows** were generated with the wheel identity **declared, not measured**: the install did not use `--require-hashes`, and libgfortran was not recorded (PV-02 Rec 27 = 2). | session record §1–4; `b01_provenance.json` |
| **Host, as measured by a reviewer** (authority level 6, not yet a governed measurement): 15.7 GB RAM; i9-12900H with 20 logical CPUs; 29.0 GB free on C:; no `.wslconfig`; `LongPathsEnabled` = 0. `tec-thesis-311` occupies 2.3 GB. *(Revision 3 compared that figure with "TE §9.3's 1.0 GB dependency allowance". That line is "Lock files and wheel cache" (TE l.544), and no TE §9.3 line covers installed environments; see §R3-5 item 7 (PV-03 Rec 10).)* | `GOV-2026-09-29-PV-02` Benchmark and Data seat passes. The CPU model and core count come from the **PV-02 Benchmark seat's read-only host query**, which was reported in session but omitted from the persisted report `governance/reviews/GOV-2026-09-29-PV-02.md`. It is a reviewer measurement (authority level 6), not a governed one (PV-03 Rec 18). |
| **The recorded identity of (a) supports verification, not a rebuild.** `pip freeze --all` carries no artifact hashes and contains a non-resolvable `pip @ file:///home/task_…` line. `conda list --explicit --md5` points at Anaconda `pkgs/main` URLs (PV-03 Rec 8). | `evidence/environment_identity_2026-09-30_tec-thesis-311/pip_freeze_all.txt`, `conda_list_explicit_md5.txt` |
| **The November B-01 identity recorded mixed line endings.** Recorded: `data.yaml`, `features.yaml` and `experiment.yaml` CRLF; `seeds.yaml` LF. The working tree today: `data` and `features` CRLF; `experiment` and `seeds` LF. So today 1 of 4 `config_hashes` differs from the receipt, and renormalising to LF would make 3 of 4 differ (PV-03 Rec 12). | `b01_runtime_identity.json`; LF and CRLF renderings of `989f290`; `git ls-files --eol` |
| **No locked-test access.** `locked_test_accessed` is `true` on 0 of 1,657 registry rows. | `artifacts/registry/experiment_registry.jsonl`, counted 2026-09-30 |

### R2-5. Authority surfaces: re-derived with a platform-role vocabulary (PV-02 Rec 11 = 2)

Revision 2's search key (`kaggle|both platforms`) could not see restatements that do not use
the word. Revision 3 adds a second key and prints what it finds.

**Derivation 1**, 2026-09-30:
- Pattern: `grep -niE "two (execution|platform|environment)s?|exactly two|platform variation|\bRAM\b|\bGPU|session|local (role|environment)|same python"`.
- Files: the Vision, the TE, the constraint register, `configs/*.yaml`, `requirements.txt`, `environment/*`.
- Hits per file: Vision 5, TE 14, register 6, `data.yaml` 1, `experiment.yaml` 4, `features.yaml` 0, `seeds.yaml` 0, `requirements.txt` 2, `environment/*` 0.

**Derivation 2:**
- Pattern: `grep -niE "kaggle|both (governed )?platforms"`.
- Files: `requirements.txt`, `pyproject.toml`, `environment/*`, `configs/*.yaml`.
- These files are outside revision 2's search scope.

**Every hit, classified.** "Already §R2" means revision 2 already lists the line.

| Hit | Classification |
|---|---|
| Vision l.325, 329, 1500 | already §R2 |
| **Vision l.1102** DEP-10 "deterministic CPU/GPU fixture test" | **new, forward-looking**: the GPU limb has no governed environment while `tf_gpu` is barred (§R4-5 item 8) |
| **Vision l.1394** "pass the CPU/GPU fixture tests" | **new, forward-looking**: same reason |
| TE l.22, 279 | not platform text |
| TE l.78, 502, 752 | consistent with D-83; unaffected |
| TE l.151, 530, 1012, 1016 | already §R2 |
| **TE l.495** §9.1 local row: role "Development, small tests, fixture runs, review, artifact inspection"; rule "Same Python 3.11 and exact pins" | **new, forward-looking**: local now carries training, G-06 and Class A acquisition, and environment (b) is CPython 3.10 under D-49 |
| **TE l.498** "There are exactly two execution environments" | **new, forward-looking**: D-83 names one platform with three environments. The same line's transfer rule is kept (§R4-5 item 6). |
| TE l.529 "Record CPU/GPU type, runtime, peak memory … for every run" | unaffected; already binding, and carried by §R3-5 item 5 |
| **TE l.604** NFR-PORT-01 removed because "only two platforms remain" | **new, rationale to review**: cross-environment consistency between (a) and (c) becomes load-bearing for G-07 (§R3-5 item 9) |
| **TE l.858** "fixture-derived tolerances that distinguish expected platform variation" | **new, forward-looking**: governs the (a)/(c) tolerance and its freeze order (§R4-5 item 5) |
| Register TC-01 and TC-04 | consistent; unaffected |
| **Register TC-03** "12-hour session on 30 GB RAM" | **new, forward-looking**: this is the Kaggle session envelope, replaced by a measured local envelope (§R3-5 item 7) |
| Register TC-03b, 03c, 03g | already §R2 |
| `data.yaml:169` ("in-session" verbal confirmation) | not platform text |
| `experiment.yaml` l.427, 433 | already §R2, historical |
| `experiment.yaml` l.436, 438 (comments on B-01 session re-verification) | historical provenance |
| `experiment.yaml` l.466–488 | already §R2 |
| **`experiment.yaml:520`** "deterministic on both governed platforms" | **new, forward-looking** |
| `requirements.txt` l.16, 30 (no GPU package; D-36 CPU wheel) | consistent; unaffected |
| **`requirements.txt` l.8** "reproducible on both governed platforms (Kaggle and local)" and **l.34** "(Kaggle AND local) check are OWED" | **new, forward-looking** |
| **`environment/install_wheels.ps1:20`** "BOTH-platform check still requires the Kaggle run" | **new, forward-looking** |
| **`environment/OFFLINE_REBUILD.md:210`** "satisfies the local half only; the Kaggle …" | **new, forward-looking** |
| **`environment/bootstrap_env.ps1:159`** "owed to Kaggle" | **new, forward-looking** |
| `environment/install_wheels.ps1:137` (native-Windows TF availability message) | not platform-role text |
| `pyproject.toml:51`, `:60` (lint configuration naming the Kaggle 3.10 venv and the `kaggle/` package builder) | historical provenance and tooling; unaffected |

**Code and test surfaces** (PV-02 Rec 1 = 1; revision 2 did not search code):
- `src/data/fixture_gate.py` l.137 (the `KAGGLE` constant), l.830–836 (control 30);
- `scripts/gate_in_session.py` l.17–20, 227–237;
- `src/data/fixture_evidence.py` l.686–711;
- `tests/test_in_session_gate.py` l.108–111;
- `tests/test_clean_run.py` l.1382–1438 (control 30);
- the message at `src/models/lstm.py:165`.

The remaining `kaggle` string occurrences in code, **derived 2026-09-30 (PV-04 Rec 28)** with
`grep -rniI --include=*.py kaggle <dir> | wc -l`: `src` **33**, `scripts` **26**, `tests` **40**.
PV-02 carried 34 / 26 / 49, and those figures were never re-derived. They are **not classified here**. Classifying every one of them is part
of the control-30 code ruling (§R5-5 item 9); it is not asserted done.

### R3-5. Consequences (revision 2 §R3 stands except where replaced here)

1. **Locked-test custody** (replaces revision 2 §R3 item 1; PV-02 Recs 2 = 2, 3 = 1, 4 = 1, 16 = 1).
   - **(a) Interim bar: procedural, with detection (PV-02 Rec 2 = 2).** Until `local` is characterised,
     no pre-G-05 audit and no G-06 may run on local. **The guard is not changed now.**
     `locked_test.py` still lets `local` through.
     - Instead, the G-05 evidence bundle carries a **fail-closed preflight assertion** (PV-03 Rec 3).
       - **Where it lives:** a function in `src/data/locked_test.py`, called by the G-05 evidence
         bundle builder.
       - **What it scans:** every **governed** access log, until the PV-01 Rec 14 single governed log
         exists. The test harness writes to **its own log root**, which the scan never includes
         (PV-04 Rec 5 = 2). That is a code change to the tests, and it removes the 5,964-row and
         5,942-row harness logs, plus the worktree copies, from the scan.
       - **What fails preflight:** any `coverage_audit`, `regime_audit` or `locked_evaluation` access
         record whose guard-stamped **`logged_at_utc`** is earlier than the **cutoff** fails G-05
         preflight, **unless** its `run_id` resolves to a registry row whose **`environment_id` or lock
         hash** (after §R5-5 item 10) identifies an admitted, characterised environment. The
         self-declared platform label is not used (PV-04 Rec 6). `retrieved_at_utc` is
         caller-supplied (`locked_test.py` l.396–410) and is **not** used (PV-04 Rec 4). A row
         without `logged_at_utc`, or with an unparseable timestamp, **fails** (PV-04 Recs 4 and 5).
         Kaggle registry rows are merged into the local registry before the scan, and the
         merge is recorded (PV-04 Rec 6). A
         `run_id` that resolves to no row, such as an orphan left by a read that aborted, **fails**.
       - **The cutoff:** an explicit UTC timestamp frozen as a field of the characterising D-number
         and mirrored in configuration.
       - **Negative controls:**
         - an orphan access row fails;
         - a local row before the cutoff fails;
         - a row after the cutoff passes;
         - a row whose `retrieved_at_utc` is forged after the cutoff but whose `logged_at_utc` is
           before it fails;
         - an unparseable timestamp fails.
       - **Stated plainly (PV-04 Rec 32):** until the characterising D-number exists, the cutoff
         does not exist, so **no pre-G-05 audit can pass preflight**.
       - **Open for the Student:** how a legitimately aborted run is handled (§R5-5 item 22).
     - **Accepted risk, stated plainly:** this detects **logged** breaches after the fact; it does not
       prevent them. It depends on the access log surviving, and that log's durability on `local` is
       exactly what item 1(b) has not yet measured. It is complete only once the PV-01 Rec 14 single
       governed log lands.
     - A local custody read made by operator error would still count as December being "seen"
       (`project.md` Forbidden, Vision §8.3). Its rows would carry the SD-03 stamp and not be gate
       evidence.
     - This departs from the board's preferred option. The PV-02 Validation Auditor made the
       reservation "a guard or test". The G-05 assertion is the test limb of that condition; it
       is not the guard limb.
   - **(b) Durability measurement protocol (PV-02 Rec 4 = 1).** The Student sets the numeric value
     marked `<N>` before the measurement starts, and the Supervisor countersigns the protocol. No
     value is supplied here.
     - **Fault model:** process kill (hard terminate) and host power-loss or crash, each injected
       while one of three writes is in flight:
       - an append of an access row;
       - an append of a registry row;
       - **a prediction-receipt write**: `.tmp`, then fsync, then `os.replace`, with no directory
         fsync (`src/models/train.py` l.1597–1600). This was added under PV-03 Rec 14, because
         both the DEC-repeat refusal and the G-07 re-hash rely on the receipt surviving.
     - **What is measured:** for each trial, whether every row the writer reported as committed
       (appended and fsync'd) is present and parses after restart; whether any row is torn or
       partial; whether any uncommitted row appears.
     - **Filesystems:**
       - native NTFS on the governed root;
       - the WSL2 `/mnt/c` drvfs mount and WSL2 ext4, but **only if** an environment that
         writes access or registry rows will ever run there.
       - Under (c) below, WSL2 is barred from restricted reads and writes, so for custody
         purposes only NTFS is measured.
     - **Trials:** `<N>` per fault type per filesystem. When setting `<N>`, the Student states the
       loss-rate bound it implies, because zero failures in `<N>` trials bounds the rate only
       loosely (PV-03 Rec 31).
     - **Pass:** zero committed rows lost and zero torn rows across all trials. Any loss fails
       the measurement.
     - **Record:** a measurement record with host, filesystem, writer commit, trial log and
       result, cited by the characterising D-number.
   - **(c) The characterising D-number (PV-02 Rec 3 = 1)** must:
     - remove the hard-coded `!= "local"` exemption (`locked_test.py:497`, `:760`), so that
       admission is by set membership only;
     - key membership by **environment identity** (item 7), not by the platform label, so that
       CI (`TEC_PLATFORM: local`) and unmeasured WSL2 filesystems are **not** admitted;
     - come with a test that refuses a non-member environment.
   - **(d) Additional preconditions** for any local pre-G-05 audit or G-06:
     - the PV-01 Rec 14 single governed access log is coded and tested (PV-02 Rec 16 = 1);
     - the code-commit guard is in place (item 10).
2. **One-shot binding** (extends revision 2 §R3 item 2; PV-02 Recs 5 = 3, 21 = 1).
   - **"Exactly once" means once per `phase_id` / `target_definition_id`, under that phase's own
     G-05 / G-P3 signature.** The Phase 2 December prediction on the new target lineage is
     designed (Vision l.279, R-27) and is not barred by this rule. The Vision's mandatory
     disclosure that Phase 2 is **not a second statistically independent blind test** is
     unchanged.
   - **Code ruling (PV-02 Rec 5, limb 1; revised under PV-03 Recs 2 and 15).**
     - **Schema.** `phase_id` and `script_id` are added to `AccessRecord` (`locked_test.py` l.295–303)
       and to `PredictionHashReceipt` (`train.py` l.1547–1554). Today neither record carries
       `phase_id`, and 0 of 1,657 registry rows do. This is a guard-schema change, and it needs
       the governance-guards recheck.
     - **Refusal rule.** `06_train_and_predict.py --partition DEC` refuses when a prior
       **`06`-scope** `locked_evaluation` access record, or a DEC receipt, exists for the same
       `phase_id`. *Scope is defined by `script_id == "06_train_and_predict"`, not by the
       free-text `AccessRecord.scope`. The allowed `script_id` values are the stage-script file stems
       (PV-04 Rec 19).* Revision 3's wording would have fired on the same G-06's own
       `05_build_features_and_splits.py` read (`05:728`), which comes first.
     - **Key.** The refusal is keyed on **`phase_id` alone, everywhere**. That is deliberately
       stricter than "per `phase_id` / `target_definition_id`": `target_definition_id` is
       descriptive and does not widen the refusal.
     - **`phase_id` value (PV-04 Rec 19):** the config's `phase_id` (`P1A` in
       `configs/experiment.yaml` l.501), not the integer `--phase`. The Student confirms this at
       adoption.
     - **Missing fields fail closed (PV-04 Rec 15):** a DEC receipt or `locked_evaluation` record
       that lacks `phase_id` or `script_id` counts as a **match**, and is refused.
     - **Negative controls:**
       - a `05` read followed by a `06` passes;
       - a second `06` in the same phase is refused;
       - a different phase is admitted;
       - a record missing a field is refused.
     - **Open for the Student:** the rule for retrying after an abort that happened before any
       prediction was written (§R5-5 item 12). It must rest on **evidence** that no prediction was
       written and no metric computed, not on an operator's statement (PV-03 Rec 31).
   - **Environment (c) (PV-02 Rec 5, limb 2; PV-03 Rec 13).** The G-07 clean run in (c) runs `06`
     over F1–F4 and REFIT only, **never DEC**.
     - It uses a **required** sparse checkout under which `evidence/locked_test_restricted/` **is not
       checked out**.
     - 29 restricted files are git-tracked, so the sparse checkout must apply before the first
       checkout (`clone --no-checkout`).
     - `/mnt/c` stays mounted, and the guard still admits `local`. So "not checked out" is a
       procedure, not a code barrier.
     - The (c) run record captures the `git sparse-checkout list` output and evidence that the
       restricted root is absent.
     - **Object store (PV-04 Rec 16):** a `--no-checkout` clone still fetches all 29 restricted blobs
       into the (c) object store, where `git show` can read them. (c) is therefore cloned with
       `--filter=blob:none` and a sparse cone that excludes the restricted root, and the run record
       confirms that those blobs are absent.
   - **Re-hash location (PV-02 Rec 5, limb 3).** G-07's verification of G-06 re-hashes the frozen
     predictions **in environment (a)** through `assert_receipt_matches`
     (`src/models/train.py:1625`), logged through the guard. It never regenerates them.
3. **Environment (a) identity (PV-02 Rec 7 = 2).**
   - Environment (a) stays `tec-thesis-311`. It is **not** rebuilt from the committed locks.
   - Its governed identity is the complete `pip freeze --all` and `conda list --explicit --md5`,
     recorded **after** `ml_dtypes==0.5.3` is restored (§R5-5 item 8), and cited by hash.
   - The 2026-09-30 pre-restore baseline is
     `evidence/environment_identity_2026-09-30_tec-thesis-311/`.
   - **Accepted consequence (restated under PV-03 Rec 8):** environment (a) can be **verified**
     against its recorded identity. It cannot be **rebuilt**, either from the committed locks or
     from that record:
     - the pip layer is unhashed;
     - the record contains a non-resolvable `pip @ file:///…` line;
     - a rebuild depends on Anaconda `pkgs/main` still serving those builds.

     G-07 evidence must say so.
   - **"Exact pins" defined:** exact conformance to the **hashed recorded identity**. That means a
     named, committed identity file per environment, and exact `name==version` equality over the
     pip lines and the explicit conda lines. There is a negative control per layer (§R3-5 item 9).
   - **Stated asymmetry:** (c) is built from a `linux-64` lock (item 4), and (a) is not
     lock-built. That package-set difference feeds into the (a)/(c) tolerance (item 5).
4. **Environment (c) definition (PV-02 Rec 8 = 1).** Before any G-07 run in (c):
   - a committed `linux-64` hashed lock (conda plus wheels, `--require-hashes`) and a bootstrap
     script exist;
   - (c) runs from a **fresh clone at the recorded commit**, never the live `/mnt/c` working tree;
   - every (c) invocation sets `CUDA_VISIBLE_DEVICES=""` and records GPU visibility;
   - **Limitation, stated for the Supervisor:** (c) is *cross-OS on the same hardware*. It
     restores the operating-system limb of the G-07 two-environment property. It does **not**
     restore the cross-host limb that Kaggle supplied: (a) and (c) share the CPU, disk and host.
     The Supervisor acknowledges this explicitly before G-07.
5. **Tolerance freeze order (PV-02 Rec 9 = 1).** This is the TE l.858 platform-variation tolerance,
   and the order is fixed:
   1. the measuring runs in (a);
   2. then **one** run in (c), pre-designated as a measuring run;
   3. then the Student's Q-31 tolerance freeze;
   4. then the (c) run that G-07 accepts.

   No tolerance is chosen after the accepted (c) run is seen.

   **(Added under PV-03 Rec 6.)**
   - **A failing accepted (c) run fails G-07.**
   - A re-run needs a cause that is recorded and fixed **before** re-execution. Every attempt is
     reported.
   - The tolerance is never re-frozen after a (c) failure without a new D-number.
   - **Precommitted before the (c) measuring run (PV-04 Rec 11):**
     - the tolerance-derivation rule and its target quantities (runtime and storage ranges,
       prediction values, or both);
     - the number of (c) measuring runs, **≥ 2**, a value the Student sets;
     - a cap on re-runs of the accepted run, and the evidence standard for "cause fixed".

     One (c) sample cannot separate platform variation from run-to-run noise.
   - **Composition (a proposal for the Student to confirm at adoption):** the (c) measuring run is
     **not** folded into the (a) runtime or storage ranges. The platform-variation tolerance is
     derived from its difference against the (a) runs.
   - Because (a) and (c) share hardware (item 4), the tolerance measures **OS and package-set
     variation only**, and G-07 evidence states so.
6. **Kaggle fallback (PV-02 Rec 10 = 2; bounded under PV-03 Rec 4; re-ruled under PV-04 Rec 7 = 2).**
   **Revision 5: the fallback excludes DEC.** DEC always runs in environment (a) under §R3-5 item 2.
   Kaggle may re-execute only F1–F4 tuning, the D-56 derivation, REFIT and all three seeds.
   - **Accepted consequence (the Student's re-ruling):** a **mixed-platform confirmatory set**, with
     tuning and REFIT on Kaggle and DEC in (a). G-07 carries a second environment identity. The
     REFIT artifacts are transferred to (a) under item 6's SHA-256 manifest.
   - Kaggle never reads December, so it needs no durability characterisation. This answers
     PV-04 Rec 7 and the Validation Auditor's condition on DEC.
   - **The revision-4 text below is kept for its bounds; its DEC wording is superseded.** Kaggle may be used again
   only to **re-execute the whole confirmatory set**: F1–F4 tuning, the D-56 derivation, REFIT,
   all three seeds and DEC. It may never supply part of that set. It is also bounded:
   - **When:** it is available **only while no DEC receipt and no `locked_evaluation` record exist
     for the `phase_id`**. Once G-06 has run, it is closed.
   - **How:** invoking it needs a D-number, with its reason recorded **before any Kaggle result
     exists**.
   - **Effect:** on invocation, every local confirmatory artifact for that `phase_id` is superseded
     and is never reported as confirmatory.
   - **Accepted risks, stated:**
     - a second environment identity at G-07;
     - no test rejects a three-seed mean built from mixed lock hashes;
     - the choice to invoke it can follow tuning results already seen in (a).
   - **No guard reaches a Kaggle session.** Kaggle is outside the custody membership set, so the
     bounds above are procedural.
7. **Resource feasibility and envelope (PV-02 Recs 12 = 1, 13 = 1).**
   - **Preconditions of adoption (PV-02 Rec 12 = 1).** This corrects revision 2, which made the
     measurement a precondition of *retiring* Kaggle; the Student's PV-01 Rec 16 ruling said
     *adoption*. Adoption needs both of:
     - peak-RSS and CPU-model capture, coded under a Student code ruling with a negative control;
     - a local `scientific_1month` run measuring runtime, peak RAM and storage.
   - **Dormancy exit and retirement (PV-02 Rec 13 = 1).**
     - The dormancy exit is tied to the PV-01 Rec 4 (storage), PV-01 Rec 5 (CPU seconds) and PV-01
       Rec 16 (RSS and CPU model; corrected under PV-04 Rec 1) code rulings landing with negative controls.
     - **Retiring Kaggle** needs the first **instrumented local Class C clean run** (EV-14) as its
       evidence. A one-month run does not bound the full year.
   - **Local envelope replacing TC-03 (PV-02 Rec 13 = 1).** It records measured values for:
     - host RAM;
     - the WSL2 memory cap (`.wslconfig`, or the default stated);
     - free disk on the governed volume, which also holds the WSL2 virtual disks;
     - the footprint of all three environments.
       - **Accounting (PV-03 Rec 10 = 2):** installed environments are accounted **outside** the
         TE §9.3 envelope. They appear as a separate, measured line in the local envelope record.
       - **Rationale:** TE §9.3's lines cover project data, artifacts, and "Lock files and wheel
         cache" (l.544). No §9.3 line addresses installed interpreter environments, and on Kaggle
         the image was never counted.
       - **Stated plainly:** this can read as weakening TC-03a ("outranks any platform
         allowance"). The Supervisor sees it explicitly at countersignature.

     The reviewer-measured figures in §R1-5 are indications, not these measurements.
   - **Binding status (PV-04 Rec 14 = 2):** the default is **`hard`, scoped as TC-03's note says**
     ("not binding for training or evaluation").
     - The register's binding column for TC-03 reads `hard` (constraint register l.31).
     - Any other choice at adoption is a downgrade.
   - **Figure for the Supervisor (PV-04 Rec 30):** environment (a) alone occupies **2.3 GB**. TE
     §9.3's nearest line, "Dependency/cache allowance 1.0 GB" (l.544), would already be exceeded if
     it were read broadly.
8. **In-environment critical set (PV-02 Rec 14 = 1).** Before any governed run in environment X, for
   X ∈ {(a), (b), (c)}, the §18.3 critical set runs **inside X** and the result is captured in that
   run's evidence. This is TC-03g's in-environment limb carried from the Kaggle session to each
   local environment. For (b), `b01_iri` gains the `requirements.txt` pins that apply to it and
   `pytest`. D-49's 2026-09-20 addendum item 1 already requires this for fixture runs.
   - **Per-environment subset (PV-03 Rec 11):** the Student rules which critical tests apply in
     each environment, with an explicit "not applicable, reason" for every omitted test.
     - (b) is CPython 3.10, while the suite targets 3.11 and TensorFlow.
     - (c) excludes the restricted root, so whether `test_locked_test_guard.py` can run there
       needs a ruling.

     The claim "the critical set passed in X" is checkable only against that list (§R5-5 item 23).
     **That list is due before §R5-5 item 4** (the governed `scientific_1month` run in (a); PV-04 Rec 13).
9. **Environment identity per run (PV-02 Rec 6 = 1)** (replaces revision 2 §R3 item 7's statement).
   Code ruling:
   - add `environment_id` as a **`RunRecord` field** (PV-03 Rec 7 = 1).
     - It is drawn from the closed set `{a_native_win, b_wsl2_b01_iri, c_wsl2_g07}` and declared
       explicitly (for example `TEC_ENVIRONMENT`).
     - Because `LOCK_ITEMS` derives from `RunRecord` (`fixture_gate.py` l.139–141), the lock then
       has **nine items: the eight TE §13.1 items plus `environment_id`**.
     - **Consequence, accepted:** every existing `environment_identity` changes, the November B-01
       receipt included. Historical identities are declared **non-comparable** under a D-number.
       This is consistent with superseding the November receipt anyway (item 12, PV-03 Rec 12 = 3).
   - refuse when it is absent or unknown. **Open for the Student:** whether that refusal is scoped
     to governed runs only (so that CI and the test suite are not refused), and whether
     `environment_id` sits beside `TEC_PLATFORM` (`kaggle|local`) or derives from it
     (§R5-5 item 24);
   - **Consequence, stated in full (PV-04 Rec 9):**
     - `lock_items()` raises when a lock item is missing (`fixture_gate.py` l.162–166). So every
       stored 8-item lock is **refused** in `verify_receipt`, in `require_in_session_gate` and in
       the `lock_from_items` hash recompute. That refusal is the designed behaviour.
     - **Superseded, to be re-run:**
       - every existing fixture-pass receipt, including the Q-31 `plumbing_7day` evidence
         (`9710daf`);
       - the November B-01 receipt.
     - A record without the field is **refused by name**: "pre-`environment_id`, non-comparable
       per D-x".
     - `ENVIRONMENT_IDENTITY_ITEMS` gains `environment_id` automatically.
     - **Code sites that must also be edited:**
       - `lock_from_items` (`fixture_gate.py` l.182–191);
       - `capture_environment_lock` (`config.py`);
       - `tests/test_clean_run.py` `_gate_payload` (l.1385–1396);
       - `tests/test_in_session_gate.py` l.51;
       - the "eight" and "seven" docstrings (`fixture_gate.py` l.156, l.195; `config.py` l.545).
     - TE §13.1's "eight items" definition is added to the §R2 surfaces this decision amends.
   - persist the nine lock items per run, next to the registry row;
   - assert pin conformance at startup for governed runs (PV-03 Rec 8; specified under PV-04 Rec 10):
     - **Capture:** `pip freeze --all` at run time, matching the identity file. Today the runtime
       uses `pip freeze` without `--all` (`config.py` l.1241), so `pip`, `setuptools` and
       `wheel` are missed. For conda: `conda list --explicit --md5`.
     - **Pip layer:** compare `name==version`. The `pip @ file:///…` line is a listed exception,
       and the pip version is recorded separately.
     - **Conda layer:** compare name, version, build and md5.
     - **Layers per environment:** (b) has no conda layer, so that layer is "not applicable" in (b).
     - **Negative controls:** one per layer, including a build-string swap.
     - **Due before §R5-5 item 4 (PV-04 Rec 18).** The pin limb moves ahead of the other item 10
       limbs, because the M-1 designated runs require it.
     - compare against a **named committed identity file per environment**, holding the freeze
       text and its SHA-256;
     - require exact `name==version` equality over the pip lines and the explicit conda lines;
     - add one negative control per layer;
   - add a negative control for each of the above.

   The TC-03g in-session gate is then re-keyed to `environment_id` (item 11).
10. **Code-commit integrity (PV-02 Rec 15 = 1).** The PV-01 Rec 6 guard is a **precondition of G-06, G-07
    and any full-year B-01 run**:
    - `--code-commit` is refused when a git tree exists;
    - a `working_tree_dirty` field is recorded;
    - negative controls are in place.
11. **G-07 evidence path (PV-02 Rec 1 = 1).** Code ruling: re-key control 30 and `gate_in_session.py`
    from the `kaggle` label to "the governed environment the run executes in".
    - It accepts (a) and (c) only.
    - Negative controls: a gate result from `b01_iri`, from CI, or from an environment whose lock
      differs from the caller's must each be refused.

    - The existing tests that assert the local refusal are **converted, not deleted**, into
      refusal tests keyed to `environment_id` (PV-03 Rec 17). *Exact sites (PV-04 Rec 21):*
      - control 30 is `tests/test_clean_run.py` l.1409–1414;
      - controls 31 and 32 in the same file also build `kaggle` locks, and are re-keyed;
      - `tests/test_in_session_gate.py` l.108–111;
      - the pre-refusal at `scripts/gate_in_session.py` l.227–237 is converted as well.

    Until this lands, G-07's named evidence artifact cannot be produced under D-83.
12. **B-01** (extends revision 2 §R3 item 4; PV-02 Recs 18 = 1, 19 = 1, 22 = 1, 27 = 2, 31).
    - **Mirror, cited exactly.** The fixture-run extension to be mirrored is the inline "Addendum
      2026-09-20 — item 4 resolved by resolution (a)" inside D-49 (`evidence/DECISIONS.md`
      l.2786). It is **not** the code-compatibility addendum at l.3483, which D-49 addendum 2
      calls "addendum 1".
    - **Smoke value (PV-02 Rec 18 = 1):** bit-identity with `37.373754526924806` TECU. Any mismatch
      stops the run and goes to the Student, with both values recorded.
      - **The exact call** (PV-03 Rec 27; quoted verbatim under PV-04 Rec 26): `iricore.vtec(...)` at the
        **D-1 ARUC coordinate**, i.e. `iricore.vtec(2024-01-06T12:00Z, 40.286, 44.086, hbot=90,
        htop=2000, hstep=0.5, version=16)` (DECISIONS l.2584). The coordinates are the ARUC station,
        latitude then longitude, not cell 40/44.
      - **Source:** `evidence/DECISIONS.md` l.2584 and
        `evidence/iri2016_kaggle_verification_2026-09-19/verification_report.json`.
      - **Prior reproduction:** WSL2 already reproduced the value bit-identically on 2026-09-20,
        recorded in `evidence/b01_tolerance_basis_2026-09-20/environment.json` as
        `wsl_value_tecu` = `kaggle_value_tecu`.
    - **Identity in code (PV-02 Rec 22 = 1):** `iri.verify_runtime` is extended to check the measured
      wheel hash, glibc, libgfortran and the Python version against `interpreter_exception`, with
      a negative control. This is a code ruling.
      - The expected values do not exist yet: `interpreter_exception` has no glibc, libgfortran or
        measured wheel-hash fields, and still names the Kaggle image.
      - They are added as **`TBD — freeze gate`** fields and frozen from the measured (b) identity
        (PV-03 Rec 16).
      - **Reader and refusal (PV-04 Rec 20):** `verify_runtime` refuses any `TBD` value, and the
        fields are added to `REQUIRED_FIELDS_MAP` for the B-01 stage, so that the §18.3 TBD
        preflight catches them. A negative control is included.
      - They are **not** filled by convenience.
      - `configs/experiment.yaml` is **not** edited by this record, because that is a governed
        config change (§R5-5 item 16).
    - **November fixture rows (PV-02 Rec 27 = 2):** labelled "wheel identity declared, not measured".
      The label now also sits machine-adjacent in a sidecar note,
      `artifacts/external/b01.WHEEL_IDENTITY_NOTE.md` (PV-03 Rec 24). The B-01 artifacts themselves
      are governed bytes and are not edited.
    - **Config line endings (PV-02 Rec 31; decided under PV-03 Rec 12 = 3).** The Student chose to:
      - renormalise the working-tree configs to the committed `eol=lf`;
      - **supersede the November B-01 receipt**;
      - **re-run the B-01 fixture**, which needs about 535 s of workload plus a new receipt.

      Under renormalisation, 3 of the 4 recorded `config_hashes` (`data`, `features`,
      `experiment`) would no longer match (§R1-5). The superseded receipt stays on record. It is
      never matched and never deleted. The renormalisation and the re-run are the Student's acts
      (§R5-5 item 13).
      - **Ordering (PV-04 Rec 13):** the re-run is a governed (b) run. It therefore comes **after**
        §R5-5 items 10, 14, 16 and 23, and uses a `--require-hashes` install. That way its receipt
        is comparable, and its wheel identity is measured rather than declared.
13. **Long paths (PV-02 Rec 23 = 1).** Environment (a)'s preflight records `LongPathsEnabled=1`, or
    states a maximum root length under which every manifest path stays within 260 characters.
    Four paths in the 2026-09-29 untracked-outputs manifest reach 260–264 characters. Changing the
    host setting is the Student's act. **Due before the adoption-precondition `scientific_1month`
    run (§R5-5 item 4), not only before G-07**, because that run is governed and would hit these
    paths (PV-03 Rec 19).
14. **Re-acquisition (PV-02 Rec 28).** Local re-acquisition under revision 2 §R3 item 9 is bound, as
    before and independent of platform, by:
    - DATA-07's provider-suffix, retrieval-date and SHA-256 recording;
    - the no-backfill-from-final-values rule;
    - the rule against mixing Dst grades (`project.md` Forbidden; D-10.1);
    - **December custody and the record-date exclusion.** No record dated December 2022 enters
      any fixture. 2022-12 has no `raw_isprint_cache/`. Every December custody restriction applies
      unchanged (revision 2 §R3 item 9; `team.md`; PV-03 Rec 28).
    - **Where re-acquired December bytes land (PV-04 Rec 27):** re-acquired 2022-12 bytes are written
      only under the D-15 restricted root. Their only pre-G-05 use is the performance-blind
      coverage and regime audit.
15. **Evaluation join (PV-03 Rec 29).** The evaluation-time IRI and GIM join, and GIM comparator
    retrieval, run in **environment (a)**, through `src/evaluation/` and
    `scripts/04_build_external_products.py`. The import boundary and the IRI denial are unchanged.
    **Split by mode (PV-04 Rec 8):**

    | Script 04 mode | Environment |
    |---|---|
    | B-01 generation (`iri.generate_benchmark`, l.1625/1633) and `verify_runtime` (l.1671) | (b) only, under D-49 |
    | Transfer of B-01 rows | (b) → (a), with item 6's SHA-256 manifest |
    | IRI and GIM join, and GIM comparator retrieval | (a) |

    **December B-01 rows:**
    - generated once per `phase_id`;
    - hashed before any metric;
    - generated with the restricted root absent in (b), from timestamps and coordinates only.

    **Open for the Student** (§R5-5 item 26): whether December B-01 generation happens before or
    after G-05.

### R3a-5. Vision §15.2 change-record fields (PV-02 Rec 20 = 1)

| §15.2 field | Entry |
|---|---|
| 1. Requested change and reason | Local as the sole platform for new governed runs; Kaggle dormant. Reason: the Student's instruction and FU-1R = A (§Basis) |
| 2. Alternatives | FU-1R option B: local for everything except B-01, with Kaggle kept for the B-01 leg. FU-1R option C: no platform change, with TE §9.1 roles kept on paper and the Kaggle limb of TE §9.2 left open for G-07. The Student rejected both |
| 3. Affected requirements, data, code, experiments, schedule, claims | Requirements and authority: §R2 plus §R2-5. Code: §R3-5 items 1, 2, 9–12. Experiments: environments and the tolerance freeze order (§R3-5 items 4–6). Schedule: adoption waits on §R3-5 item 7. Claims: none; no claim boundary changes |
| 4. Whether the locked test has been accessed | **No.** 0 of 1,657 registry rows have `locked_test_accessed=true` (2026-09-30) |
| 5. Required regeneration or invalidation | Historical Kaggle evidence keeps its provenance (revision 2 §R3 item 10). **The November B-01 fixture receipt is superseded, and the B-01 fixture is re-run** after config renormalisation (PV-03 Rec 12 = 3). The superseded rows and receipt stay on record, labelled "wheel identity declared, not measured". Historical `environment_identity` values become non-comparable (PV-03 Rec 7 = 1) |
| 6. Approver, date, effective version | Student (adoption) and Supervisor (countersignature), both OPEN. Effective against Vision v4.3 and TE v3.4 |

### R4-5. Proposed D-text (for the Student to adopt, amend or reject)

> ## D-83 — Execution platform: local (native Windows plus WSL2 on the Student's laptop) as the sole platform for new governed runs; Kaggle dormant (Student proposal; Supervisor countersignature required)
>
> **Decision date:** <date of adoption>. **Decided by:** the Student, 2026-09-29 (FU-1R = A), and
> revised under the Student's rulings on `GOV-2026-09-29-PV-02` and `GOV-2026-09-30-PV-03`
> (2026-09-30). **Authority amended:**
> every forward-looking surface in CR-2026-09-29-PLATFORM-LOCAL-ONLY §R2 **and §R2-5**. **Ratifies:**
> D-49 addendum 2. **Adoption preconditions:** §R5-5 items 2, 3, 4 and 7 (PV-04 Rec 17). **Supervisor countersignature:
> REQUIRED, OPEN.** The authority equivalence is not invoked.
>
> 1. **Platform.** New governed runs execute on `LAPTOP-TV4UGFBC` in three named environments.
>    Each is recorded per run as `environment_id` (§R3-5 item 9):
>    - **(a)** native-Windows `tec-thesis-311`. Its governed identity is its recorded full freeze
>      after the pin restore (§R3-5 item 3). It is the environment for every stage script, for
>      the whole confirmatory set, and for the evaluation-time IRI and GIM join (§R3-5 item 15).
>    - **(b)** WSL2 `b01_iri`, only under D-49 and its addenda.
>    - **(c)** WSL2 G-07 clean-run, only for G-07 reproduction, under §R3-5 item 4.
>
>    TE §9.1's "exactly two execution environments" (l.498) is read as "one platform with three
>    named environments". Its transfer rule stands.
> 2. **Kaggle is dormant.** No new governed run executes on Kaggle. It may be used again only to
>    re-execute F1–F4 tuning, the D-56 derivation, REFIT and all three seeds, **never DEC**, which
>    always runs in (a). The resulting mixed-platform confirmatory set is an accepted consequence
>    (§R3-5 item 6; PV-04 Rec 7 = 2). That is allowed only while no DEC
>    receipt and no `locked_evaluation` record exist for the `phase_id`, and only under a D-number
>    whose reason is recorded before any Kaggle result exists. Invoking it supersedes every local
>    confirmatory artifact for that phase (§R3-5 item 6). Kaggle is retired by a further note
>    under this D-number, on the evidence of the first instrumented local Class C clean run.
>    Artifacts already produced on Kaggle keep their provenance.
> 3. **Locked test.**
>    - Until `local` is characterised under §R3-5 item 1(b)–(d), no pre-G-05 audit and no G-06
>      runs on local. The fail-closed G-05 preflight assertion of §R3-5 item 1(a) detects
>      **logged** breaches after the fact. It is complete only once the single governed access log
>      exists.
>    - G-06 then runs CPU-only in (a), with exact pins (conformance to the hashed recorded
>      identity), **once per `phase_id`**.
>    - A repeated `06`-scope `--partition DEC` is refused by code, keyed on `phase_id` (§R3-5
>      item 2).
>    - G-07 re-hashes in (a) and never regenerates. Environment (c) never runs DEC. There the
>      restricted root **is not checked out, and its blobs are not fetched**: a sparse, blob-filtered
>      clone. This is a procedural control, not a code barrier (§R3-5 item 2).
>    - `tf_gpu`, and any environment off its governed identity, are barred from governed runs.
>    - The Phase 2 non-independence disclosure is unchanged.
> 4. **B-01.**
>    - D-49 addendum 2 is ratified.
>    - A full-year B-01 run additionally requires the extension of addendum 2 to the B-01 fixture
>      runs, mirroring the inline D-49 addendum of 2026-09-20 (DECISIONS l.2786).
>    - It also requires the identity checks, coded in `verify_runtime`.
>    - The smoke value must be reproduced bit-identically.
>    - The configs are renormalised to `eol=lf`, the November receipt is superseded, and the B-01
>      fixture is re-run (§R3-5 item 12).
> 5. **Preflight and G-07** (TE §9.2, l.858).
>    - The `environment_and_cpu_preflight_report` shows, in (a): the installed state conforms to
>      the recorded identity (verification, not rebuild); a completed skeleton run; the §18.3 critical set run inside (a);
>      measured CPU runtime, peak RAM and storage; and the long-path state.
>    - It shows a clean-run reproduction in (c) under §R3-5 item 4.
>    - The (a)/(c) tolerance is frozen in the order of §R3-5 item 5. A failing accepted (c) run
>      fails G-07.
>    - The in-session gate is keyed to `environment_id`.
> 6. **Transfers.** Every transfer between WSL2 and Windows carries a SHA-256 manifest of every file
>    moved, and the transfer is recorded (TE §9.1).
> 7. **CI** is a non-scientific verification surface governed by the Rec 47 / P2 record, not an
>    execution platform, and it is never an admitted custody environment.
> 8. **Unchanged:**
>    - CPU is a complete path, GPU is an optional accelerator only, and there is no GPU-only
>      dependency. While no governed GPU environment exists, the GPU limbs of Vision l.1102 and
>      l.1394 are **not applicable**, not failed.
>    - Every locked-test rule and every frozen value is unchanged.
>    - The re-acquisition obligations of §R3-5 item 14 are unchanged.
> 9. **If this decision is rejected or amended,** the Kaggle limb of TE §9.2 and TC-03g reverts to
>    an open G-07 item. D-49 addendum 2 stands on its own terms.
> 10. **TC-03 replaced.** TC-03 (a "12-hour session on 30 GB RAM") is replaced by the measured local
>    envelope of §R3-5 item 7. Installed environments are accounted outside TE §9.3. **Binding
>    status: `hard`, scoped as TC-03's note says** (PV-04 Rec 14 = 2). Any other choice at
>    adoption is a downgrade that requires Supervisor countersignature.

### R5-5. Open items (replaces revision 2 §R5)

| # | Item | Owner | Due |
|---|---|---|---|
| 1 | Adopt, amend or reject §R4-5 | Student | after items 2, 3, 4 and 7 (PV-03 Rec 9; revision 3 said "2–7", which was circular because it included items 5 and 6) |
| 2 | Full-board re-review of revision 5, scoped to G-06 and G-07 | per `/review-tec-governance` | before adoption |
| 3 | Code ruling: peak-RSS and CPU-model capture, with a negative control (PV-01 Rec 16; PV-02 Rec 12) | Student | **adoption precondition** |
| 4 | Local `scientific_1month` run measuring runtime, peak RAM and storage. It needs the PV-01 Rec 4 and PV-01 Rec 5 code rulings (items 20 and 21), a clean root, both fixtures in order, item 3, item 8 (pins restored first) and the long-path limb of item 17. | Student | **adoption precondition** |
| 5 | Countersign | Supervisor | after adoption |
| 6 | Supervisor acknowledgement that (c) is cross-OS on the same hardware (§R3-5 item 4) | Supervisor | before G-07 |
| 7 | Durability protocol: the Student sets `<N>`; the Supervisor countersigns (§R3-5 item 1(b)) | Student; Supervisor | before adoption |
| 8 | Restore `ml_dtypes==0.5.3` in (a), then record and hash the governed identity as a named committed identity file (§R3-5 items 3, 9). Optionally, also record per-wheel SHA-256 from `RECORD` and a hashed requirements file, to make (a) rebuildable (PV-03 Rec 8, the Student's option) | Student | **before item 4**, and before any governed run in (a) |
| 9 | Code ruling: re-key control 30 / `gate_in_session.py` to `environment_id`, with negative controls, and classify every `kaggle` string in code (§R3-5 item 11) | Student | before any G-07 evidence run |
| 10 | Code ruling: `environment_id`, per-run lock items, pin conformance, with negative controls (§R3-5 item 9) | Student | **pin limb: before item 4** (PV-04 Rec 18); the rest: before G-06 and G-07 |
| 11 | Characterising D-number, with the exemption removed, identity-keyed membership and a non-member refusal test, after the measurement (§R3-5 item 1(c)). **Validation Auditor veto reserved.** | Student | before any local pre-G-05 audit or G-06 |
| 12 | Code ruling: add `phase_id` and `script_id` to `AccessRecord` and to the receipt; refuse a repeated `06`-scope `--partition DEC` per `phase_id`; the three negative controls in §R3-5 item 2; the governance-guards recheck. **The Student rules the retry-after-abort-before-write rule, evidence-based.** | Student | before G-06 |
| 13 | **Decided (PV-03 Rec 12 = 3):** renormalise the configs to `eol=lf`; declare the November B-01 receipt superseded; re-run the B-01 fixture and produce a new receipt | Student | **after items 10, 14, 16 and 23**, with a `--require-hashes` install (PV-04 Rec 13); before any full-year B-01 run |
| 14 | Code rulings: the PV-01 Rec 6 `--code-commit` guard (item 10); the PV-01 Rec 14 single governed access log; the G-05 preflight custody assertion (item 1(a)); the `verify_runtime` identity checks (item 12). Each with negative controls. | Student | before G-06 / G-07 / full-year B-01, and before the pre-G-05 audit |
| 15 | `linux-64` hashed lock and bootstrap for (c); sparse-checkout / fresh-clone procedure | Student | before G-07 |
| 16 | Extend D-49 addendum 2 to the B-01 fixture runs; mirror it in `interpreter_exception`; the (b) critical-set install (§R3-5 item 8) | Student | before any full-year B-01 run |
| 17 | Local envelope measurements replacing TC-03, with installed environments accounted outside §9.3 (§R3-5 item 7); `LongPathsEnabled` or a root-length rule (§R3-5 item 13) | Student | long-path limb: **before item 4**; envelope: before G-07 |
| 18 | In-place annotation of every forward-looking surface in §R2 and §R2-5 after adoption, under `CHANGE_RECORD_PROCEDURE.md`; §13 corrections to `team.md` and `project.md` | Student | after adoption |
| 19 | Next code change touching `locked_test.py`: fix the docstring at l.51 ("qualifies" should read "disqualifies"; PV-02 Rec 29) | Student | with item 11 |
| 20 | Code ruling **PV-01 Rec 4**: the storage measure excludes archives, with a negative control (PV-03 Rec 20) | Student | before item 4 |
| 21 | Code ruling **PV-01 Rec 5**: CPU seconds, not wall-clock time, with a negative control (PV-03 Rec 20) | Student | before item 4 |
| 22 | Rule how a legitimately aborted run is handled by the fail-closed G-05 assertion; freeze the cutoff UTC field in the characterising D-number (§R3-5 item 1(a)) | Student | before the pre-G-05 audit |
| 23 | Rule the per-environment critical subset for (a), (b) and (c), with "not applicable, reason" rows (§R3-5 item 8; PV-03 Rec 11) | Student | **before item 4** (PV-04 Rec 13), and before any governed run in (b) or (c) |
| 24 | Rule the scope of the `environment_id` refusal (governed runs only?) and its relation to `TEC_PLATFORM`; issue the D-number declaring historical identities non-comparable (§R3-5 item 9) | Student | before item 10. **Open ordering question (PV-05 Rec 7):** whether item 24 must also precede item 10's **pin limb**, and so come before item 4. To be settled at the revision-5 re-review, by the Student. |
| 25 | Record the durability loss-rate bound implied by `<N>` (§R3-5 item 1(b)) | Student | with item 7 |
| 26 | Rule whether December B-01 rows are generated before or after G-05 (§R3-5 item 15; PV-04 Rec 8) | Student | before any December B-01 generation |
| 27 | Code ruling: move the test harness to its own access-log root, with a negative control (§R3-5 item 1(a); PV-04 Rec 5 = 2) | Student | before the pre-G-05 audit |
| 28 | Precommit the (c) tolerance-derivation rule, the (c) measuring-run count (≥ 2) and the re-run cap and evidence standard (§R3-5 item 5; PV-04 Rec 11) | Student | before the (c) measuring run |
| 29 | Issue the D-number declaring pre-`environment_id` identities non-comparable, and list the re-runs it requires, `plumbing_7day` Q-31 included (§R3-5 item 9; PV-04 Rec 9) | Student | with item 10 |

---

### R6-5. Proposed rulings on the open items — **PROPOSED, NOT ADOPTED** (recorded 2026-09-30)

This section was recorded at the Student's request at the 4.6 gate (revision cycle 4, "Record
proposed rulings"). It comes from a read-only analysis. **None of it is adopted.** Each item needs
the approval shown before it binds, and nothing here changes §R3-5, §R4-5 or §R5-5.

| §R5-5 item | Proposed ruling | Basis | Student | Supervisor |
|---|---|---|---|---|
| 26 (December B-01 timing) | **After G-05** | see text below | adopt | yes (locked-test protocol) |
| K (M-1) | **2, conditional on item 20** | D-74 amendment `measured_over_runs >= 2`; Q-31 closure precedent (2 runs) | adopt | no |
| (c) measuring runs (item 28) | **2** | D-74 companion rule; PV-04 Rec 11 floor | adopt | via D-83 countersignature |
| Re-run cap (item 28) | **BLOCKED — insufficient evidence** | no value exists in the governing documents | set a value, or rule | via D-83 countersignature |
| 22 (aborted runs; cutoff) | no special case; cutoff = the adoption UTC timestamp of the characterising D-number | TE l.829 / NFR-AUD-01 | adopt | yes (custody) |
| 24 (refusal scope; `TEC_PLATFORM`) | governed runs only; `environment_id` sits **beside** `TEC_PLATFORM` | TE §13.1 enum kept for historical rows; CI runs §18.3 as `local` | adopt | no |
| 25 (`<N>` bound) | **BLOCKED — insufficient evidence** | `<N>` is unset | set `<N>` | yes (protocol) |
| 27 (harness log root) | per-test `tmp_path`, or a gitignored test-log root; the tracked 5,964-row log is kept as history and excluded by path | PV-04 Rec 5 = 2 | adopt (code ruling) | no |
| 29 (non-comparability D-number) | refuse pre-`environment_id` locks by name; re-runs owed: `plumbing_7day` Q-31 (`9710daf`) and the November B-01; the November supersession goes in the same D-number | §R3-5 item 9; `fixture_gate.py` l.162–166 | adopt (creates the D-number) | no (Q-31 is Student-owned) |

**Student decisions of 2026-09-30** (4.6 gate, revision cycle 5, given as structured answers).
These resolve three of the BLOCKED values and the storage contradiction. They become binding
through D-83 adoption. The Supervisor countersignature marked above is still required.

| Item | Student decision | Consequence |
|---|---|---|
| Storage contradiction (§R5-5 item 20) | **Zero width allowed.** Code ruling: `storage_total` may be zero-width for a **candidate** composed over ≥ 2 runs, mirroring D-74's `fp_tolerance` companion rule. A **frozen** manifest still requires the Student's Q-31 value. | Resolves contradiction 1 below. It needs a change to `compose_measurement_ranges` (`fixture_manifest.py` l.1684–1688, l.1856), with a negative control: zero-width refusal for a single run, zero-width acceptance at ≥ 2 runs. |
| K (M-1) | **K = 2** | The K = 2 proposal is no longer conditional, because the storage ruling above removes the blocker. It is recorded in the M-1 precommitment file before the first designated run. |
| Re-run cap (§R5-5 item 28) | **PV-03 Rec 6's rule is the cap.** There is no numeric cap: every re-run of the accepted (c) run needs a recorded, fixed cause; every attempt is reported; and there is no re-freeze without a D-number. | Resolves contradiction 2 below. |
| `<N>` (§R3-5 item 1(b); §R5-5 item 25) | **Process-kill: N = 100** per filesystem. **Power-loss: N = 10** per filesystem. | Implied 95% loss-rate bound with zero failures (rule of three, about 3/N): about **3%** for process-kill and about **30%** for power-loss. The weak power-loss bound is stated as a limitation of the characterisation. |

Still open after these decisions:
- #26 (December B-01 timing), #22, #24, #27 and #29: the proposals stand, awaiting adoption.
- Contradiction 3 (one-shot gap for B-01).
- The item 24 / pin-limb ordering question.

**Proposed wording, ready to paste if adopted:**

> **#26 — December B-01 generation timing.** December 2022 B-01 rows are generated only after
> G-05 is signed, exactly once per `phase_id`, in environment (b), from timestamps and station
> coordinates only, with the restricted root absent. They are transferred to (a) under item 6's
> SHA-256 manifest, and hashed with a prediction-hash receipt before any metric is computed. No
> December B-01 value exists before G-05. A code refusal of a second December B-01 generation
> per `phase_id`, with a negative control, is added to §R5-5 item 12.
>
> *Basis:*
> - `project.md` Mandated ("generate and write the locked-test predictions exactly once, after
>   G-05 is signed, and hash them before computing any metric");
> - Vision §8.3;
> - `iri.py` l.1051–1055 (DEC is refused outside the one door);
> - `splits.py` l.719–757 (the DEC partition needs the G-05 signature).
>
> Generating the rows before G-05 would put IRI December values next to the required pre-G-05
> December target audit, which would let benchmark performance be inspected before G-05.

> **K.** K = 2 (the D-74 `measured_over_runs >= 2` floor, and the Q-31 closure precedent). This is
> **conditional on the §R5-5 item 20 storage-measure ruling** defining how a deterministic
> `storage_total` composes. K is recorded now, but no designated run starts until item 20 lands.

> **(c) measuring runs.** Two (c) measuring runs are pre-designated before the Q-31 tolerance
> freeze. The platform-variation tolerance is derived from both, under the D-74 companion rule.

> **Re-run cap: BLOCKED.** The governing documents support no cap value. The Student either:
> - sets a value; or
> - rules that PV-03 Rec 6's rule is the cap (a recorded, fixed cause before each re-run; every
>   attempt reported; no re-freeze without a D-number).

**Contradictions found. Recorded here; not resolved here.**
1. **Storage zero-width vs determinism.** `compose_measurement_ranges` refuses a zero-width
   `storage_total` (`fixture_manifest.py` l.1684–1688, l.1856). On a clean root with deterministic
   outputs, every run can measure identical storage, so **no K** yields a composable candidate.
   This must be resolved inside §R5-5 item 20, for example by treating storage like D-74's
   fp-tolerance rule, where 0 is allowed for a candidate over ≥ 2 runs.
2. **Re-run cap.** PV-03 Rec 6 rejected "R retries, declared in advance" (it chose option 1), but
   PV-04 Rec 11 requires a cap. The two rulings pull in different directions.
3. **One-shot gap for B-01.** §R3-5 item 15 says the December B-01 rows are generated "once per
   `phase_id`", but the only code refusal (§R3-5 item 2) is keyed to `06_train_and_predict`.
   Nothing refuses a second December B-01 generation by code.

**Proposed PV-03 Rec 12 execution plan (not executed).** The sequence "renormalise → supersede →
re-run" is **incomplete**. Steps 2–4 below are the prerequisites it was missing.
1. **Prerequisites already listed in §R5-5 item 13:**
   - item 10 (the `environment_id` and pin-conformance code);
   - the item 14 limbs for the code-commit guard and `verify_runtime`;
   - item 16 (`b01_iri` pins and pytest; the `interpreter_exception` mirror);
   - item 23 (the (b) critical subset).
2. **Missing prerequisite: measure and freeze the (b) identity values.** Measure glibc,
   libgfortran and the wheel hash in (b), using an installed-files / `RECORD` check. The Student
   then freezes them into `interpreter_exception`. Without this, `verify_runtime` refuses `TBD`
   (PV-04 Rec 20).
3. **Missing prerequisite: a hashed requirements file for `b01_iri`**, then a reinstall with
   `--require-hashes`. No such file exists today.
4. **Missing prerequisite: issue the item 29 D-number** (non-comparability plus the November
   supersession) **before** the re-run, so that the new receipt is created under the nine-item
   identity.
5. **Renormalise.**
   - Verify that `git diff --ignore-cr-at-eol HEAD -- configs/` is empty.
   - Record the "before" hashes: data `9c1fe28d`, features `2e77f12f`, experiment `8427794f`,
     seeds `c951f949`.
   - Run `git checkout -- configs/data.yaml configs/features.yaml`. `.gitattributes eol=lf`
     makes those files LF.
   - Verify all four against the LF blob hashes: `871be23b`, `1b1ebdfd`, `8427794f`, `c951f949`.
   - The index is unchanged, so no commit is needed. Record the act in a change record.
6. **Supersede.** The item 29 D-number is the act. The old receipt, the rows and the sidecar are
   left untouched.
7. **In (b):**
   - run the item 23 critical subset and capture it;
   - re-run the November B-01 generation with `environment_id=b_wsl2_b01_iri`, with no
     `--code-commit`, from a clean tree at a recorded commit;
   - check that the smoke value is bit-identical (`37.373754526924806`).
8. **Transfer** every B-01 file to (a) with a SHA-256 manifest, and record the transfer. The new
   receipt is written; the old one stays.

---

## Revision 4 (superseded 2026-09-30 by Revision 5, retained verbatim)

**Status: DRAFT, NOT ENACTED. It is NOT READY for adoption.** §R5-4 lists the items that
must be closed first. It is **not ready** because the Student's ruling on PV-02 Rec 12 makes a
measurement and a code ruling **preconditions of adoption**, and neither exists yet.

*Corrected 2026-09-30 under PV-03 Rec 20:*
- Revision 3 said that PV-02 Rec 16 was also an adoption precondition. It is not: it is a custody
  precondition, due before the pre-G-05 audit.
- **Citation convention:** "PV-01 Rec N", "PV-02 Rec N" and "PV-03 Rec N" name the board. An
  unprefixed "Rec" appears only in the rulings tables below.

- No D-number has been written. `evidence/DECISIONS.md` is the Student's register. The D-text in
  §R4-4 is offered for the Student to adopt, amend or reject.
- The Supervisor must countersign. The authority equivalence is **not** invoked, because this
  amends Vision D-129 (PV-01 Rec 19).
- Revision 4 needs a **full-board re-review** before adoption. `GOV-2026-09-30-PV-03` reviewed
  revision 3; nothing has reviewed revision 4 yet.

**Basis.** Revision 2, below, retained verbatim and marked superseded. On top of it come the
Student's rulings of 2026-09-30 on `GOV-2026-09-29-PV-02`, recorded in
`governance/CHANGE_RECORD_2026-09-30_GOV-PV-02_rulings.md`:

| Rec | Option | Rec | Option | Rec | Option |
|---|---|---|---|---|---|
| 1 | 1 | 9 | 1 | 16 | 1 |
| 2 | 2 | 10 | 2 | 18 | 1 |
| 3 | 1 | 11 | 2 | 19 | 1 |
| 4 | 1 | 12 | 1 | 20 | 1 |
| 5 | 3 | 13 | 1 | 21 | 1 |
| 6 | 1 | 14 | 1 | 22 | 1 |
| 7 | 2 | 15 | 1 | 23 | 1 |
| 8 | 1 | | | | |

It also incorporates:
- PV-02 Rec 27 = 2;
- PV-02 Recs 28–31 approved.

**Revision 4** applies the Student's rulings of 2026-09-30 on `GOV-2026-09-30-PV-03`:

| Rec | Option | Rec | Option | Rec | Option |
|---|---|---|---|---|---|
| 1 | 1 | 7 | 1 | 12 | 3 |
| 2 | 1 | 8 | 1 | 13 | 1 |
| 3 | 1 | 9 | 1 | 14 | 1 |
| 4 | 1 | 10 | **2** | 15–31 | Approve |
| 5 | 1 | 11 | 1 | | |
| 6 | 1 | | | | |

Revision 3 is retained verbatim below, marked superseded.

**Validation Auditor position** (PV-02, updated by PV-03):
- The PV-01 Rec 2 veto against item 3 is **lifted** for the revision-2 text.
- It is **reserved** for the future D-number that would characterise `local` (§R3-4 item 1).
- PV-03 modified the reservation. It now also covers any adoption that keeps revision 3's
  DEC-refusal text or G-05 assertion text. Revision 4 replaces both (§R3-4 items 1(a) and 2,
  under PV-03 Recs 2 and 3).
- PV-02 Rec 2 = 2 narrows the reservation's condition 3 to its test limb. The Validation Auditor
  accepts that only in the fail-closed form written in §R3-4 item 1(a).

### R1-4. Facts (revision 2 §R1 stands; these are added or corrected)

| Fact | Source |
|---|---|
| **Environment (a) is not the locked environment.** Pip layer: 3 of 32 `wheels-win64.lock` entries drift. They are `ml_dtypes` 0.5.4 vs 0.5.3, `setuptools` 83.0.0 vs 84.0.0 and `wheel` 0.47.0 vs 0.48.0. **6** of 61 pip packages appear in neither lock (`distlib`, `filelock`, `platformdirs`, `python-discovery`, `uv`, `virtualenv`). A further 16 are pinned in `conda-win64.lock`, including `scipy` 1.17.1, which matches; two of those drift (`fonttools` 4.65.0 vs 4.66.0, `pytz` 2026.3.post1 vs 2026.4). Conda layer: 20 packages installed against 119 in the lock, and **0 of the 20 build strings match**. *(Corrected under PV-03 Rec 1; revision 3 said "22 of 61 in neither lock" because the conda lock was never checked.)* Python build: `hb00fc5c_0` from Anaconda `pkgs/main`, where the lock pins conda-forge `hb12b558_2`. This **corrects revision 2 §R1 row 4**, which reported a single-pin drift. | `evidence/environment_identity_2026-09-30_tec-thesis-311/README.md` (derived by script, printed) |
| **The G-07 preflight evidence path refuses every platform but Kaggle.** `require_in_session_gate` refuses `platform != "kaggle"` (control 30). `gate_in_session.py` refuses to run anywhere but Kaggle. `build_environment_and_cpu_preflight_report` requires the in-session gate result. | `src/data/fixture_gate.py:830`; `scripts/gate_in_session.py:230`; `src/data/fixture_evidence.py` l.686–711 |
| **The local exemption is hard-coded.** `platform_label != "local" and …`. The platform enum is exactly `kaggle \| local`. CI declares `TEC_PLATFORM: local`. | `src/data/locked_test.py:497`, `:760`; `src/data/config.py:764`; `.github/workflows/verify.yml:103` |
| **Nothing records the environment per row.** No registry column or extension holds it. `capture_environment_lock` folds `pip freeze` into a hash only. | `src/data/experiment_registry.py:102–123`; `src/data/config.py:1257–1311` |
| **Write-once is enforced per path, not per run.** DEC predictions go under a per-`run_id` directory. | `scripts/06_train_and_predict.py:722`, `:1698`, `:1811`; `src/models/train.py:1575` |
| **The B-01 config hashes differ from today's only in line endings, not in content.** The recorded `experiment.yaml` hash `10028bf0…` equals the CRLF rendering of the `989f290` blob. `data.yaml` and `features.yaml` are still CRLF in the working tree. `experiment.yaml` and `seeds.yaml` are LF, although `.gitattributes` sets `eol=lf`. `ENVIRONMENT_IDENTITY_ITEMS` includes `config_hashes`, so a line-ending change alone changes the environment identity that D-49 item 4 matches on (PV-02 Rec 31). | `b01_runtime_identity.json`; `git show 989f290:configs/experiment.yaml`, rendered with CRLF, then `sha256sum`; `git ls-files --eol configs/*.yaml`; `src/data/fixture_gate.py:141` |
| **The November B-01 rows** were generated with the wheel identity **declared, not measured**: the install did not use `--require-hashes`, and libgfortran was not recorded (PV-02 Rec 27 = 2). | session record §1–4; `b01_provenance.json` |
| **Host, as measured by a reviewer** (authority level 6, not yet a governed measurement): 15.7 GB RAM; i9-12900H with 20 logical CPUs; 29.0 GB free on C:; no `.wslconfig`; `LongPathsEnabled` = 0. `tec-thesis-311` occupies 2.3 GB. *(Revision 3 compared that figure with "TE §9.3's 1.0 GB dependency allowance". That line is "Lock files and wheel cache" (TE l.544), and no TE §9.3 line covers installed environments; see §R3-4 item 7 (PV-03 Rec 10).)* | `GOV-2026-09-29-PV-02` Benchmark and Data seat passes. The CPU model and core count come from the **PV-02 Benchmark seat's read-only host query**, which was reported in session but omitted from the persisted report `governance/reviews/GOV-2026-09-29-PV-02.md`. It is a reviewer measurement (authority level 6), not a governed one (PV-03 Rec 18). |
| **The recorded identity of (a) supports verification, not a rebuild.** `pip freeze --all` carries no artifact hashes and contains a non-resolvable `pip @ file:///home/task_…` line. `conda list --explicit --md5` points at Anaconda `pkgs/main` URLs (PV-03 Rec 8). | `evidence/environment_identity_2026-09-30_tec-thesis-311/pip_freeze_all.txt`, `conda_list_explicit_md5.txt` |
| **The November B-01 identity recorded mixed line endings.** Recorded: `data.yaml`, `features.yaml` and `experiment.yaml` CRLF; `seeds.yaml` LF. The working tree today: `data` and `features` CRLF; `experiment` and `seeds` LF. So today 1 of 4 `config_hashes` differs from the receipt, and renormalising to LF would make 3 of 4 differ (PV-03 Rec 12). | `b01_runtime_identity.json`; LF and CRLF renderings of `989f290`; `git ls-files --eol` |
| **No locked-test access.** `locked_test_accessed` is `true` on 0 of 1,657 registry rows. | `artifacts/registry/experiment_registry.jsonl`, counted 2026-09-30 |

### R2-4. Authority surfaces: re-derived with a platform-role vocabulary (PV-02 Rec 11 = 2)

Revision 2's search key (`kaggle|both platforms`) could not see restatements that do not use
the word. Revision 3 adds a second key and prints what it finds.

**Derivation 1**, 2026-09-30:
- Pattern: `grep -niE "two (execution|platform|environment)s?|exactly two|platform variation|\bRAM\b|\bGPU|session|local (role|environment)|same python"`.
- Files: the Vision, the TE, the constraint register, `configs/*.yaml`, `requirements.txt`, `environment/*`.
- Hits per file: Vision 5, TE 14, register 6, `data.yaml` 1, `experiment.yaml` 4, `features.yaml` 0, `seeds.yaml` 0, `requirements.txt` 2, `environment/*` 0.

**Derivation 2:**
- Pattern: `grep -niE "kaggle|both (governed )?platforms"`.
- Files: `requirements.txt`, `pyproject.toml`, `environment/*`, `configs/*.yaml`.
- These files are outside revision 2's search scope.

**Every hit, classified.** "Already §R2" means revision 2 already lists the line.

| Hit | Classification |
|---|---|
| Vision l.325, 329, 1500 | already §R2 |
| **Vision l.1102** DEP-10 "deterministic CPU/GPU fixture test" | **new, forward-looking**: the GPU limb has no governed environment while `tf_gpu` is barred (§R4-4 item 8) |
| **Vision l.1394** "pass the CPU/GPU fixture tests" | **new, forward-looking**: same reason |
| TE l.22, 279 | not platform text |
| TE l.78, 502, 752 | consistent with D-83; unaffected |
| TE l.151, 530, 1012, 1016 | already §R2 |
| **TE l.495** §9.1 local row: role "Development, small tests, fixture runs, review, artifact inspection"; rule "Same Python 3.11 and exact pins" | **new, forward-looking**: local now carries training, G-06 and Class A acquisition, and environment (b) is CPython 3.10 under D-49 |
| **TE l.498** "There are exactly two execution environments" | **new, forward-looking**: D-83 names one platform with three environments. The same line's transfer rule is kept (§R4-4 item 6). |
| TE l.529 "Record CPU/GPU type, runtime, peak memory … for every run" | unaffected; already binding, and carried by §R3-4 item 5 |
| **TE l.604** NFR-PORT-01 removed because "only two platforms remain" | **new, rationale to review**: cross-environment consistency between (a) and (c) becomes load-bearing for G-07 (§R3-4 item 9) |
| **TE l.858** "fixture-derived tolerances that distinguish expected platform variation" | **new, forward-looking**: governs the (a)/(c) tolerance and its freeze order (§R4-4 item 5) |
| Register TC-01 and TC-04 | consistent; unaffected |
| **Register TC-03** "12-hour session on 30 GB RAM" | **new, forward-looking**: this is the Kaggle session envelope, replaced by a measured local envelope (§R3-4 item 7) |
| Register TC-03b, 03c, 03g | already §R2 |
| `data.yaml:169` ("in-session" verbal confirmation) | not platform text |
| `experiment.yaml` l.427, 433 | already §R2, historical |
| `experiment.yaml` l.436, 438 (comments on B-01 session re-verification) | historical provenance |
| `experiment.yaml` l.466–488 | already §R2 |
| **`experiment.yaml:520`** "deterministic on both governed platforms" | **new, forward-looking** |
| `requirements.txt` l.16, 30 (no GPU package; D-36 CPU wheel) | consistent; unaffected |
| **`requirements.txt` l.8** "reproducible on both governed platforms (Kaggle and local)" and **l.34** "(Kaggle AND local) check are OWED" | **new, forward-looking** |
| **`environment/install_wheels.ps1:20`** "BOTH-platform check still requires the Kaggle run" | **new, forward-looking** |
| **`environment/OFFLINE_REBUILD.md:210`** "satisfies the local half only; the Kaggle …" | **new, forward-looking** |
| **`environment/bootstrap_env.ps1:159`** "owed to Kaggle" | **new, forward-looking** |
| `environment/install_wheels.ps1:137` (native-Windows TF availability message) | not platform-role text |
| `pyproject.toml:51`, `:60` (lint configuration naming the Kaggle 3.10 venv and the `kaggle/` package builder) | historical provenance and tooling; unaffected |

**Code and test surfaces** (PV-02 Rec 1 = 1; revision 2 did not search code):
- `src/data/fixture_gate.py` l.137 (the `KAGGLE` constant), l.830–836 (control 30);
- `scripts/gate_in_session.py` l.17–20, 227–237;
- `src/data/fixture_evidence.py` l.686–711;
- `tests/test_in_session_gate.py` l.108–111;
- `tests/test_clean_run.py` l.1382–1438 (control 30);
- the message at `src/models/lstm.py:165`.

The remaining `kaggle` string occurrences in code were counted by the PV-02 seats: `src` 34 lines,
`scripts` 26, `tests` 49. They are **not classified here**. Classifying every one of them is part
of the control-30 code ruling (§R5-4 item 9); it is not asserted done.

### R3-4. Consequences (revision 2 §R3 stands except where replaced here)

1. **Locked-test custody** (replaces revision 2 §R3 item 1; PV-02 Recs 2 = 2, 3 = 1, 4 = 1, 16 = 1).
   - **(a) Interim bar: procedural, with detection (PV-02 Rec 2 = 2).** Until `local` is characterised,
     no pre-G-05 audit and no G-06 may run on local. **The guard is not changed now.**
     `locked_test.py` still lets `local` through.
     - Instead, the G-05 evidence bundle carries a **fail-closed preflight assertion** (PV-03 Rec 3).
       - **Where it lives:** a function in `src/data/locked_test.py`, called by the G-05 evidence
         bundle builder.
       - **What it scans:** **every** access log, until the PV-01 Rec 14 single governed log exists.
       - **What fails preflight:** any `coverage_audit`, `regime_audit` or `locked_evaluation` access
         record whose own `retrieved_at_utc` is earlier than the **cutoff** fails G-05 preflight,
         **unless** its `run_id` resolves to a registry row whose platform is not `local`. A
         `run_id` that resolves to no row, such as an orphan left by a read that aborted, **fails**.
       - **The cutoff:** an explicit UTC timestamp frozen as a field of the characterising D-number
         and mirrored in configuration.
       - **Negative controls:** an orphan access row fails; a local row before the cutoff fails; a
         row after the cutoff passes.
       - **Open for the Student:** how a legitimately aborted run is handled (§R5-4 item 22).
     - **Accepted risk, stated plainly:** this detects **logged** breaches after the fact; it does not
       prevent them. It depends on the access log surviving, and that log's durability on `local` is
       exactly what item 1(b) has not yet measured. It is complete only once the PV-01 Rec 14 single
       governed log lands.
     - A local custody read made by operator error would still count as December being "seen"
       (`project.md` Forbidden, Vision §8.3). Its rows would carry the SD-03 stamp and not be gate
       evidence.
     - This departs from the board's preferred option. The PV-02 Validation Auditor made the
       reservation "a guard or test". The G-05 assertion is the test limb of that condition; it
       is not the guard limb.
   - **(b) Durability measurement protocol (PV-02 Rec 4 = 1).** The Student sets the numeric value
     marked `<N>` before the measurement starts, and the Supervisor countersigns the protocol. No
     value is supplied here.
     - **Fault model:** process kill (hard terminate) and host power-loss or crash, each injected
       while one of three writes is in flight:
       - an append of an access row;
       - an append of a registry row;
       - **a prediction-receipt write**: `.tmp`, then fsync, then `os.replace`, with no directory
         fsync (`src/models/train.py` l.1597–1600). This was added under PV-03 Rec 14, because
         both the DEC-repeat refusal and the G-07 re-hash rely on the receipt surviving.
     - **What is measured:** for each trial, whether every row the writer reported as committed
       (appended and fsync'd) is present and parses after restart; whether any row is torn or
       partial; whether any uncommitted row appears.
     - **Filesystems:**
       - native NTFS on the governed root;
       - the WSL2 `/mnt/c` drvfs mount and WSL2 ext4, but **only if** an environment that
         writes access or registry rows will ever run there.
       - Under (c) below, WSL2 is barred from restricted reads and writes, so for custody
         purposes only NTFS is measured.
     - **Trials:** `<N>` per fault type per filesystem. When setting `<N>`, the Student states the
       loss-rate bound it implies, because zero failures in `<N>` trials bounds the rate only
       loosely (PV-03 Rec 31).
     - **Pass:** zero committed rows lost and zero torn rows across all trials. Any loss fails
       the measurement.
     - **Record:** a measurement record with host, filesystem, writer commit, trial log and
       result, cited by the characterising D-number.
   - **(c) The characterising D-number (PV-02 Rec 3 = 1)** must:
     - remove the hard-coded `!= "local"` exemption (`locked_test.py:497`, `:760`), so that
       admission is by set membership only;
     - key membership by **environment identity** (item 7), not by the platform label, so that
       CI (`TEC_PLATFORM: local`) and unmeasured WSL2 filesystems are **not** admitted;
     - come with a test that refuses a non-member environment.
   - **(d) Additional preconditions** for any local pre-G-05 audit or G-06:
     - the PV-01 Rec 14 single governed access log is coded and tested (PV-02 Rec 16 = 1);
     - the code-commit guard is in place (item 10).
2. **One-shot binding** (extends revision 2 §R3 item 2; PV-02 Recs 5 = 3, 21 = 1).
   - **"Exactly once" means once per `phase_id` / `target_definition_id`, under that phase's own
     G-05 / G-P3 signature.** The Phase 2 December prediction on the new target lineage is
     designed (Vision l.279, R-27) and is not barred by this rule. The Vision's mandatory
     disclosure that Phase 2 is **not a second statistically independent blind test** is
     unchanged.
   - **Code ruling (PV-02 Rec 5, limb 1; revised under PV-03 Recs 2 and 15).**
     - **Schema.** `phase_id` and `script_id` are added to `AccessRecord` (`locked_test.py` l.295–303)
       and to `PredictionHashReceipt` (`train.py` l.1547–1554). Today neither record carries
       `phase_id`, and 0 of 1,657 registry rows do. This is a guard-schema change, and it needs
       the governance-guards recheck.
     - **Refusal rule.** `06_train_and_predict.py --partition DEC` refuses when a prior
       **`06`-scope** `locked_evaluation` access record, or a DEC receipt, exists for the same
       `phase_id`. Revision 3's wording would have fired on the same G-06's own
       `05_build_features_and_splits.py` read (`05:728`), which comes first.
     - **Key.** The refusal is keyed on **`phase_id` alone, everywhere**. That is deliberately
       stricter than "per `phase_id` / `target_definition_id`": `target_definition_id` is
       descriptive and does not widen the refusal.
     - **Negative controls:**
       - a `05` read followed by a `06` passes;
       - a second `06` in the same phase is refused;
       - a different phase is admitted.
     - **Open for the Student:** the rule for retrying after an abort that happened before any
       prediction was written (§R5-4 item 12). It must rest on **evidence** that no prediction was
       written and no metric computed, not on an operator's statement (PV-03 Rec 31).
   - **Environment (c) (PV-02 Rec 5, limb 2; PV-03 Rec 13).** The G-07 clean run in (c) runs `06`
     over F1–F4 and REFIT only, **never DEC**.
     - It uses a **required** sparse checkout under which `evidence/locked_test_restricted/` **is not
       checked out**.
     - 29 restricted files are git-tracked, so the sparse checkout must apply before the first
       checkout (`clone --no-checkout`).
     - `/mnt/c` stays mounted, and the guard still admits `local`. So "not checked out" is a
       procedure, not a code barrier.
     - The (c) run record captures the `git sparse-checkout list` output and evidence that the
       restricted root is absent.
   - **Re-hash location (PV-02 Rec 5, limb 3).** G-07's verification of G-06 re-hashes the frozen
     predictions **in environment (a)** through `assert_receipt_matches`
     (`src/models/train.py:1625`), logged through the guard. It never regenerates them.
3. **Environment (a) identity (PV-02 Rec 7 = 2).**
   - Environment (a) stays `tec-thesis-311`. It is **not** rebuilt from the committed locks.
   - Its governed identity is the complete `pip freeze --all` and `conda list --explicit --md5`,
     recorded **after** `ml_dtypes==0.5.3` is restored (§R5-4 item 8), and cited by hash.
   - The 2026-09-30 pre-restore baseline is
     `evidence/environment_identity_2026-09-30_tec-thesis-311/`.
   - **Accepted consequence (restated under PV-03 Rec 8):** environment (a) can be **verified**
     against its recorded identity. It cannot be **rebuilt**, either from the committed locks or
     from that record:
     - the pip layer is unhashed;
     - the record contains a non-resolvable `pip @ file:///…` line;
     - a rebuild depends on Anaconda `pkgs/main` still serving those builds.

     G-07 evidence must say so.
   - **"Exact pins" defined:** exact conformance to the **hashed recorded identity**. That means a
     named, committed identity file per environment, and exact `name==version` equality over the
     pip lines and the explicit conda lines. There is a negative control per layer (§R3-4 item 9).
   - **Stated asymmetry:** (c) is built from a `linux-64` lock (item 4), and (a) is not
     lock-built. That package-set difference feeds into the (a)/(c) tolerance (item 5).
4. **Environment (c) definition (PV-02 Rec 8 = 1).** Before any G-07 run in (c):
   - a committed `linux-64` hashed lock (conda plus wheels, `--require-hashes`) and a bootstrap
     script exist;
   - (c) runs from a **fresh clone at the recorded commit**, never the live `/mnt/c` working tree;
   - every (c) invocation sets `CUDA_VISIBLE_DEVICES=""` and records GPU visibility;
   - **Limitation, stated for the Supervisor:** (c) is *cross-OS on the same hardware*. It
     restores the operating-system limb of the G-07 two-environment property. It does **not**
     restore the cross-host limb that Kaggle supplied: (a) and (c) share the CPU, disk and host.
     The Supervisor acknowledges this explicitly before G-07.
5. **Tolerance freeze order (PV-02 Rec 9 = 1).** This is the TE l.858 platform-variation tolerance,
   and the order is fixed:
   1. the measuring runs in (a);
   2. then **one** run in (c), pre-designated as a measuring run;
   3. then the Student's Q-31 tolerance freeze;
   4. then the (c) run that G-07 accepts.

   No tolerance is chosen after the accepted (c) run is seen.

   **(Added under PV-03 Rec 6.)**
   - **A failing accepted (c) run fails G-07.**
   - A re-run needs a cause that is recorded and fixed **before** re-execution. Every attempt is
     reported.
   - The tolerance is never re-frozen after a (c) failure without a new D-number.
   - **Composition (a proposal for the Student to confirm at adoption):** the (c) measuring run is
     **not** folded into the (a) runtime or storage ranges. The platform-variation tolerance is
     derived from its difference against the (a) runs.
   - Because (a) and (c) share hardware (item 4), the tolerance measures **OS and package-set
     variation only**, and G-07 evidence states so.
6. **Kaggle fallback (PV-02 Rec 10 = 2; bounded under PV-03 Rec 4).** Kaggle may be used again
   only to **re-execute the whole confirmatory set**: F1–F4 tuning, the D-56 derivation, REFIT,
   all three seeds and DEC. It may never supply part of that set. It is also bounded:
   - **When:** it is available **only while no DEC receipt and no `locked_evaluation` record exist
     for the `phase_id`**. Once G-06 has run, it is closed.
   - **How:** invoking it needs a D-number, with its reason recorded **before any Kaggle result
     exists**.
   - **Effect:** on invocation, every local confirmatory artifact for that `phase_id` is superseded
     and is never reported as confirmatory.
   - **Accepted risks, stated:**
     - a second environment identity at G-07;
     - no test rejects a three-seed mean built from mixed lock hashes;
     - the choice to invoke it can follow tuning results already seen in (a).
   - **No guard reaches a Kaggle session.** Kaggle is outside the custody membership set, so the
     bounds above are procedural.
7. **Resource feasibility and envelope (PV-02 Recs 12 = 1, 13 = 1).**
   - **Preconditions of adoption (PV-02 Rec 12 = 1).** This corrects revision 2, which made the
     measurement a precondition of *retiring* Kaggle; the Student's PV-01 Rec 16 ruling said
     *adoption*. Adoption needs both of:
     - peak-RSS and CPU-model capture, coded under a Student code ruling with a negative control;
     - a local `scientific_1month` run measuring runtime, peak RAM and storage.
   - **Dormancy exit and retirement (PV-02 Rec 13 = 1).**
     - The dormancy exit is tied to the PV-01 Rec 4 (storage), PV-01 Rec 5 (CPU seconds) and PV-01
       PV-02 Rec 16 (RSS and CPU model) code rulings landing with negative controls.
     - **Retiring Kaggle** needs the first **instrumented local Class C clean run** (EV-14) as its
       evidence. A one-month run does not bound the full year.
   - **Local envelope replacing TC-03 (PV-02 Rec 13 = 1).** It records measured values for:
     - host RAM;
     - the WSL2 memory cap (`.wslconfig`, or the default stated);
     - free disk on the governed volume, which also holds the WSL2 virtual disks;
     - the footprint of all three environments.
       - **Accounting (PV-03 Rec 10 = 2):** installed environments are accounted **outside** the
         TE §9.3 envelope. They appear as a separate, measured line in the local envelope record.
       - **Rationale:** TE §9.3's lines cover project data, artifacts, and "Lock files and wheel
         cache" (l.544). No §9.3 line addresses installed interpreter environments, and on Kaggle
         the image was never counted.
       - **Stated plainly:** this can read as weakening TC-03a ("outranks any platform
         allowance"). The Supervisor sees it explicitly at countersignature.

     The reviewer-measured figures in §R1-4 are indications, not these measurements.
   - **The envelope's binding status is stated by the Student at adoption** (D-text item 10). TC-03's own
     note says it is "not binding for training or evaluation" (PV-03 Rec 21).
8. **In-environment critical set (PV-02 Rec 14 = 1).** Before any governed run in environment X, for
   X ∈ {(a), (b), (c)}, the §18.3 critical set runs **inside X** and the result is captured in that
   run's evidence. This is TC-03g's in-environment limb carried from the Kaggle session to each
   local environment. For (b), `b01_iri` gains the `requirements.txt` pins that apply to it and
   `pytest`. D-49's 2026-09-20 addendum item 1 already requires this for fixture runs.
   - **Per-environment subset (PV-03 Rec 11):** the Student rules which critical tests apply in
     each environment, with an explicit "not applicable, reason" for every omitted test.
     - (b) is CPython 3.10, while the suite targets 3.11 and TensorFlow.
     - (c) excludes the restricted root, so whether `test_locked_test_guard.py` can run there
       needs a ruling.

     The claim "the critical set passed in X" is checkable only against that list (§R5-4 item 23).
9. **Environment identity per run (PV-02 Rec 6 = 1)** (replaces revision 2 §R3 item 7's statement).
   Code ruling:
   - add `environment_id` as a **`RunRecord` field** (PV-03 Rec 7 = 1).
     - It is drawn from the closed set `{a_native_win, b_wsl2_b01_iri, c_wsl2_g07}` and declared
       explicitly (for example `TEC_ENVIRONMENT`).
     - Because `LOCK_ITEMS` derives from `RunRecord` (`fixture_gate.py` l.139–141), the lock then
       has **nine items: the eight TE §13.1 items plus `environment_id`**.
     - **Consequence, accepted:** every existing `environment_identity` changes, the November B-01
       receipt included. Historical identities are declared **non-comparable** under a D-number.
       This is consistent with superseding the November receipt anyway (item 12, PV-03 Rec 12 = 3).
   - refuse when it is absent or unknown. **Open for the Student:** whether that refusal is scoped
     to governed runs only (so that CI and the test suite are not refused), and whether
     `environment_id` sits beside `TEC_PLATFORM` (`kaggle|local`) or derives from it
     (§R5-4 item 24);
   - persist the nine lock items per run, next to the registry row;
   - assert pin conformance at startup for governed runs (PV-03 Rec 8):
     - compare against a **named committed identity file per environment**, holding the freeze
       text and its SHA-256;
     - require exact `name==version` equality over the pip lines and the explicit conda lines;
     - add one negative control per layer;
   - add a negative control for each of the above.

   The TC-03g in-session gate is then re-keyed to `environment_id` (item 11).
10. **Code-commit integrity (PV-02 Rec 15 = 1).** The PV-01 Rec 6 guard is a **precondition of G-06, G-07
    and any full-year B-01 run**:
    - `--code-commit` is refused when a git tree exists;
    - a `working_tree_dirty` field is recorded;
    - negative controls are in place.
11. **G-07 evidence path (PV-02 Rec 1 = 1).** Code ruling: re-key control 30 and `gate_in_session.py`
    from the `kaggle` label to "the governed environment the run executes in".
    - It accepts (a) and (c) only.
    - Negative controls: a gate result from `b01_iri`, from CI, or from an environment whose lock
      differs from the caller's must each be refused.

    - The existing tests that assert the local refusal are **converted, not deleted**, into
      refusal tests keyed to `environment_id` (PV-03 Rec 17): `tests/test_clean_run.py`
      l.1382–1438 and `tests/test_in_session_gate.py` l.108–111.

    Until this lands, G-07's named evidence artifact cannot be produced under D-83.
12. **B-01** (extends revision 2 §R3 item 4; PV-02 Recs 18 = 1, 19 = 1, 22 = 1, 27 = 2, 31).
    - **Mirror, cited exactly.** The fixture-run extension to be mirrored is the inline "Addendum
      2026-09-20 — item 4 resolved by resolution (a)" inside D-49 (`evidence/DECISIONS.md`
      l.2786). It is **not** the code-compatibility addendum at l.3483, which D-49 addendum 2
      calls "addendum 1".
    - **Smoke value (PV-02 Rec 18 = 1):** bit-identity with `37.373754526924806` TECU. Any mismatch
      stops the run and goes to the Student, with both values recorded.
      - **The exact call** (PV-03 Rec 27): `vtec(2024-01-06T12:00Z, 40.286, 44.086, hbot=90,
        htop=2000, hstep=0.5, version=16)`.
      - **Source:** `evidence/DECISIONS.md` l.2584 and
        `evidence/iri2016_kaggle_verification_2026-09-19/verification_report.json`.
      - **Prior reproduction:** WSL2 already reproduced the value bit-identically on 2026-09-20,
        recorded in `evidence/b01_tolerance_basis_2026-09-20/environment.json` as
        `wsl_value_tecu` = `kaggle_value_tecu`.
    - **Identity in code (PV-02 Rec 22 = 1):** `iri.verify_runtime` is extended to check the measured
      wheel hash, glibc, libgfortran and the Python version against `interpreter_exception`, with
      a negative control. This is a code ruling.
      - The expected values do not exist yet: `interpreter_exception` has no glibc, libgfortran or
        measured wheel-hash fields, and still names the Kaggle image.
      - They are added as **`TBD — freeze gate`** fields and frozen from the measured (b) identity
        (PV-03 Rec 16).
      - They are **not** filled by convenience.
      - `configs/experiment.yaml` is **not** edited by this record, because that is a governed
        config change (§R5-4 item 16).
    - **November fixture rows (PV-02 Rec 27 = 2):** labelled "wheel identity declared, not measured".
      The label now also sits machine-adjacent in a sidecar note,
      `artifacts/external/b01.WHEEL_IDENTITY_NOTE.md` (PV-03 Rec 24). The B-01 artifacts themselves
      are governed bytes and are not edited.
    - **Config line endings (PV-02 Rec 31; decided under PV-03 Rec 12 = 3).** The Student chose to:
      - renormalise the working-tree configs to the committed `eol=lf`;
      - **supersede the November B-01 receipt**;
      - **re-run the B-01 fixture**, which needs about 535 s of workload plus a new receipt.

      Under renormalisation, 3 of the 4 recorded `config_hashes` (`data`, `features`,
      `experiment`) would no longer match (§R1-4). The superseded receipt stays on record. It is
      never matched and never deleted. The renormalisation and the re-run are the Student's acts
      (§R5-4 item 13).
13. **Long paths (PV-02 Rec 23 = 1).** Environment (a)'s preflight records `LongPathsEnabled=1`, or
    states a maximum root length under which every manifest path stays within 260 characters.
    Four paths in the 2026-09-29 untracked-outputs manifest reach 260–264 characters. Changing the
    host setting is the Student's act. **Due before the adoption-precondition `scientific_1month`
    run (§R5-4 item 4), not only before G-07**, because that run is governed and would hit these
    paths (PV-03 Rec 19).
14. **Re-acquisition (PV-02 Rec 28).** Local re-acquisition under revision 2 §R3 item 9 is bound, as
    before and independent of platform, by:
    - DATA-07's provider-suffix, retrieval-date and SHA-256 recording;
    - the no-backfill-from-final-values rule;
    - the rule against mixing Dst grades (`project.md` Forbidden; D-10.1);
    - **December custody and the record-date exclusion.** No record dated December 2022 enters
      any fixture. 2022-12 has no `raw_isprint_cache/`. Every December custody restriction applies
      unchanged (revision 2 §R3 item 9; `team.md`; PV-03 Rec 28).
15. **Evaluation join (PV-03 Rec 29).** The evaluation-time IRI and GIM join, and GIM comparator
    retrieval, run in **environment (a)**, through `src/evaluation/` and
    `scripts/04_build_external_products.py`. The import boundary and the IRI denial are unchanged.

### R3a-4. Vision §15.2 change-record fields (PV-02 Rec 20 = 1)

| §15.2 field | Entry |
|---|---|
| 1. Requested change and reason | Local as the sole platform for new governed runs; Kaggle dormant. Reason: the Student's instruction and FU-1R = A (§Basis) |
| 2. Alternatives | FU-1R option B: local for everything except B-01, with Kaggle kept for the B-01 leg. FU-1R option C: no platform change, with TE §9.1 roles kept on paper and the Kaggle limb of TE §9.2 left open for G-07. The Student rejected both |
| 3. Affected requirements, data, code, experiments, schedule, claims | Requirements and authority: §R2 plus §R2-4. Code: §R3-4 items 1, 2, 9–12. Experiments: environments and the tolerance freeze order (§R3-4 items 4–6). Schedule: adoption waits on §R3-4 item 7. Claims: none; no claim boundary changes |
| 4. Whether the locked test has been accessed | **No.** 0 of 1,657 registry rows have `locked_test_accessed=true` (2026-09-30) |
| 5. Required regeneration or invalidation | Historical Kaggle evidence keeps its provenance (revision 2 §R3 item 10). **The November B-01 fixture receipt is superseded, and the B-01 fixture is re-run** after config renormalisation (PV-03 Rec 12 = 3). The superseded rows and receipt stay on record, labelled "wheel identity declared, not measured". Historical `environment_identity` values become non-comparable (PV-03 Rec 7 = 1) |
| 6. Approver, date, effective version | Student (adoption) and Supervisor (countersignature), both OPEN. Effective against Vision v4.3 and TE v3.4 |

### R4-4. Proposed D-text (for the Student to adopt, amend or reject)

> ## D-83 — Execution platform: local (native Windows plus WSL2 on the Student's laptop) as the sole platform for new governed runs; Kaggle dormant (Student proposal; Supervisor countersignature required)
>
> **Decision date:** <date of adoption>. **Decided by:** the Student, 2026-09-29 (FU-1R = A), and
> revised under the Student's rulings on `GOV-2026-09-29-PV-02` and `GOV-2026-09-30-PV-03`
> (2026-09-30). **Authority amended:**
> every forward-looking surface in CR-2026-09-29-PLATFORM-LOCAL-ONLY §R2 **and §R2-4**. **Ratifies:**
> D-49 addendum 2. **Adoption preconditions:** §R3-4 item 7. **Supervisor countersignature:
> REQUIRED, OPEN.** The authority equivalence is not invoked.
>
> 1. **Platform.** New governed runs execute on `LAPTOP-TV4UGFBC` in three named environments.
>    Each is recorded per run as `environment_id` (§R3-4 item 9):
>    - **(a)** native-Windows `tec-thesis-311`. Its governed identity is its recorded full freeze
>      after the pin restore (§R3-4 item 3). It is the environment for every stage script, for
>      the whole confirmatory set, and for the evaluation-time IRI and GIM join (§R3-4 item 15).
>    - **(b)** WSL2 `b01_iri`, only under D-49 and its addenda.
>    - **(c)** WSL2 G-07 clean-run, only for G-07 reproduction, under §R3-4 item 4.
>
>    TE §9.1's "exactly two execution environments" (l.498) is read as "one platform with three
>    named environments". Its transfer rule stands.
> 2. **Kaggle is dormant.** No new governed run executes on Kaggle. It may be used again only to
>    re-execute the whole confirmatory set, never part of it. That is allowed only while no DEC
>    receipt and no `locked_evaluation` record exist for the `phase_id`, and only under a D-number
>    whose reason is recorded before any Kaggle result exists. Invoking it supersedes every local
>    confirmatory artifact for that phase (§R3-4 item 6). Kaggle is retired by a further note
>    under this D-number, on the evidence of the first instrumented local Class C clean run.
>    Artifacts already produced on Kaggle keep their provenance.
> 3. **Locked test.**
>    - Until `local` is characterised under §R3-4 item 1(b)–(d), no pre-G-05 audit and no G-06
>      runs on local. The fail-closed G-05 preflight assertion of §R3-4 item 1(a) detects
>      **logged** breaches after the fact. It is complete only once the single governed access log
>      exists.
>    - G-06 then runs CPU-only in (a), with exact pins (conformance to the hashed recorded
>      identity), **once per `phase_id`**.
>    - A repeated `06`-scope `--partition DEC` is refused by code, keyed on `phase_id` (§R3-4
>      item 2).
>    - G-07 re-hashes in (a) and never regenerates. Environment (c) never runs DEC; the restricted
>      root **is not checked out** there.
>    - `tf_gpu`, and any environment off its governed identity, are barred from governed runs.
>    - The Phase 2 non-independence disclosure is unchanged.
> 4. **B-01.**
>    - D-49 addendum 2 is ratified.
>    - A full-year B-01 run additionally requires the extension of addendum 2 to the B-01 fixture
>      runs, mirroring the inline D-49 addendum of 2026-09-20 (DECISIONS l.2786).
>    - It also requires the identity checks, coded in `verify_runtime`.
>    - The smoke value must be reproduced bit-identically.
>    - The configs are renormalised to `eol=lf`, the November receipt is superseded, and the B-01
>      fixture is re-run (§R3-4 item 12).
> 5. **Preflight and G-07** (TE §9.2, l.858).
>    - The `environment_and_cpu_preflight_report` shows, in (a): the installed state conforms to
>      the recorded identity (verification, not rebuild); a completed skeleton run; the §18.3 critical set run inside (a);
>      measured CPU runtime, peak RAM and storage; and the long-path state.
>    - It shows a clean-run reproduction in (c) under §R3-4 item 4.
>    - The (a)/(c) tolerance is frozen in the order of §R3-4 item 5. A failing accepted (c) run
>      fails G-07.
>    - The in-session gate is keyed to `environment_id`.
> 6. **Transfers.** Every transfer between WSL2 and Windows carries a SHA-256 manifest of every file
>    moved, and the transfer is recorded (TE §9.1).
> 7. **CI** is a non-scientific verification surface governed by the Rec 47 / P2 record, not an
>    execution platform, and it is never an admitted custody environment.
> 8. **Unchanged:**
>    - CPU is a complete path, GPU is an optional accelerator only, and there is no GPU-only
>      dependency. While no governed GPU environment exists, the GPU limbs of Vision l.1102 and
>      l.1394 are **not applicable**, not failed.
>    - Every locked-test rule and every frozen value is unchanged.
>    - The re-acquisition obligations of §R3-4 item 14 are unchanged.
> 9. **If this decision is rejected or amended,** the Kaggle limb of TE §9.2 and TC-03g reverts to
>    an open G-07 item. D-49 addendum 2 stands on its own terms.
> 10. **TC-03 replaced.** TC-03 (a "12-hour session on 30 GB RAM") is replaced by the measured local
>    envelope of §R3-4 item 7. Installed environments are accounted outside TE §9.3. **Binding
>    status: <the Student states at adoption: binding or advisory>** (PV-03 Rec 21).

### R5-4. Open items (replaces revision 2 §R5)

| # | Item | Owner | Due |
|---|---|---|---|
| 1 | Adopt, amend or reject §R4-4 | Student | after items 2, 3, 4 and 7 (PV-03 Rec 9; revision 3 said "2–7", which was circular because it included items 5 and 6) |
| 2 | Full-board re-review of revision 4, scoped to G-06 and G-07 | per `/review-tec-governance` | before adoption |
| 3 | Code ruling: peak-RSS and CPU-model capture, with a negative control (PV-01 Rec 16; PV-02 Rec 12) | Student | **adoption precondition** |
| 4 | Local `scientific_1month` run measuring runtime, peak RAM and storage. It needs the PV-01 Rec 4 and PV-01 Rec 5 code rulings (items 20 and 21), a clean root, both fixtures in order, item 3, item 8 (pins restored first) and the long-path limb of item 17. | Student | **adoption precondition** |
| 5 | Countersign | Supervisor | after adoption |
| 6 | Supervisor acknowledgement that (c) is cross-OS on the same hardware (§R3-4 item 4) | Supervisor | before G-07 |
| 7 | Durability protocol: the Student sets `<N>`; the Supervisor countersigns (§R3-4 item 1(b)) | Student; Supervisor | before adoption |
| 8 | Restore `ml_dtypes==0.5.3` in (a), then record and hash the governed identity as a named committed identity file (§R3-4 items 3, 9). Optionally, also record per-wheel SHA-256 from `RECORD` and a hashed requirements file, to make (a) rebuildable (PV-03 Rec 8, the Student's option) | Student | **before item 4**, and before any governed run in (a) |
| 9 | Code ruling: re-key control 30 / `gate_in_session.py` to `environment_id`, with negative controls, and classify every `kaggle` string in code (§R3-4 item 11) | Student | before any G-07 evidence run |
| 10 | Code ruling: `environment_id`, per-run lock items, pin conformance, with negative controls (§R3-4 item 9) | Student | before G-06 and G-07 |
| 11 | Characterising D-number, with the exemption removed, identity-keyed membership and a non-member refusal test, after the measurement (§R3-4 item 1(c)). **Validation Auditor veto reserved.** | Student | before any local pre-G-05 audit or G-06 |
| 12 | Code ruling: add `phase_id` and `script_id` to `AccessRecord` and to the receipt; refuse a repeated `06`-scope `--partition DEC` per `phase_id`; the three negative controls in §R3-4 item 2; the governance-guards recheck. **The Student rules the retry-after-abort-before-write rule, evidence-based.** | Student | before G-06 |
| 13 | **Decided (PV-03 Rec 12 = 3):** renormalise the configs to `eol=lf`; declare the November B-01 receipt superseded; re-run the B-01 fixture and produce a new receipt | Student | before any full-year B-01 run |
| 14 | Code rulings: the PV-01 Rec 6 `--code-commit` guard (item 10); the PV-01 Rec 14 single governed access log; the G-05 preflight custody assertion (item 1(a)); the `verify_runtime` identity checks (item 12). Each with negative controls. | Student | before G-06 / G-07 / full-year B-01, and before the pre-G-05 audit |
| 15 | `linux-64` hashed lock and bootstrap for (c); sparse-checkout / fresh-clone procedure | Student | before G-07 |
| 16 | Extend D-49 addendum 2 to the B-01 fixture runs; mirror it in `interpreter_exception`; the (b) critical-set install (§R3-4 item 8) | Student | before any full-year B-01 run |
| 17 | Local envelope measurements replacing TC-03, with installed environments accounted outside §9.3 (§R3-4 item 7); `LongPathsEnabled` or a root-length rule (§R3-4 item 13) | Student | long-path limb: **before item 4**; envelope: before G-07 |
| 18 | In-place annotation of every forward-looking surface in §R2 and §R2-4 after adoption, under `CHANGE_RECORD_PROCEDURE.md`; §13 corrections to `team.md` and `project.md` | Student | after adoption |
| 19 | Next code change touching `locked_test.py`: fix the docstring at l.51 ("qualifies" should read "disqualifies"; PV-02 Rec 29) | Student | with item 11 |
| 20 | Code ruling **PV-01 Rec 4**: the storage measure excludes archives, with a negative control (PV-03 Rec 20) | Student | before item 4 |
| 21 | Code ruling **PV-01 Rec 5**: CPU seconds, not wall-clock time, with a negative control (PV-03 Rec 20) | Student | before item 4 |
| 22 | Rule how a legitimately aborted run is handled by the fail-closed G-05 assertion; freeze the cutoff UTC field in the characterising D-number (§R3-4 item 1(a)) | Student | before the pre-G-05 audit |
| 23 | Rule the per-environment critical subset for (a), (b) and (c), with "not applicable, reason" rows (§R3-4 item 8; PV-03 Rec 11) | Student | before any governed run in (b) or (c) |
| 24 | Rule the scope of the `environment_id` refusal (governed runs only?) and its relation to `TEC_PLATFORM`; issue the D-number declaring historical identities non-comparable (§R3-4 item 9) | Student | before item 10 |
| 25 | Record the durability loss-rate bound implied by `<N>` (§R3-4 item 1(b)) | Student | with item 7 |

---

## Revision 3 (superseded 2026-09-30 by Revision 4, retained verbatim)

**Status: DRAFT, NOT ENACTED. It is NOT READY for adoption.** §R5-3 lists the items that
must be closed first. It is **not ready** because two of the Student's rulings
(`GOV-2026-09-29-PV-02` Recs 12 and 16) make measurements and code rulings **preconditions
of adoption**, and neither exists yet.

- No D-number has been written. `evidence/DECISIONS.md` is the Student's register. The D-text in
  §R4-3 is offered for the Student to adopt, amend or reject.
- The Supervisor must countersign. The authority equivalence is **not** invoked, because this
  amends Vision D-129 (PV-01 Rec 19).
- Revision 3 needs a **full-board re-review** before adoption. `GOV-2026-09-29-PV-02` reviewed
  revision 2 only.

**Basis.** Revision 2, below, retained verbatim and marked superseded. On top of it come the
Student's rulings of 2026-09-30 on `GOV-2026-09-29-PV-02`, recorded in
`governance/CHANGE_RECORD_2026-09-30_GOV-PV-02_rulings.md`:

| Rec | Option | Rec | Option | Rec | Option |
|---|---|---|---|---|---|
| 1 | 1 | 9 | 1 | 16 | 1 |
| 2 | 2 | 10 | 2 | 18 | 1 |
| 3 | 1 | 11 | 2 | 19 | 1 |
| 4 | 1 | 12 | 1 | 20 | 1 |
| 5 | 3 | 13 | 1 | 21 | 1 |
| 6 | 1 | 14 | 1 | 22 | 1 |
| 7 | 2 | 15 | 1 | 23 | 1 |
| 8 | 1 | | | | |

It also incorporates:
- Rec 27 = 2;
- Recs 28–31 approved.

**Validation Auditor position** (carried from PV-02):
- The PV-01 Rec 2 veto against item 3 is **lifted** for the revision-2 text.
- It is **reserved** for the future D-number that would characterise `local` (§R3-3 item 1).
- Revision 3 keeps every condition that the reservation names. Rec 2 = 2 changes one of them;
  see §R3-3 item 1.

### R1-3. Facts (revision 2 §R1 stands; these are added or corrected)

| Fact | Source |
|---|---|
| **Environment (a) is not the locked environment.** Pip layer: 3 of 32 `wheels-win64.lock` entries drift. They are `ml_dtypes` 0.5.4 vs 0.5.3, `setuptools` 83.0.0 vs 84.0.0 and `wheel` 0.47.0 vs 0.48.0. A further 22 of 61 pip packages appear in neither lock, including `scipy` 1.17.1. Conda layer: 20 packages installed against 119 in the lock. Python build: `hb00fc5c_0` from Anaconda `pkgs/main`, where the lock pins conda-forge `hb12b558_2`. This **corrects revision 2 §R1 row 4**, which reported a single-pin drift. | `evidence/environment_identity_2026-09-30_tec-thesis-311/README.md` (derived by script, printed) |
| **The G-07 preflight evidence path refuses every platform but Kaggle.** `require_in_session_gate` refuses `platform != "kaggle"` (control 30). `gate_in_session.py` refuses to run anywhere but Kaggle. `build_environment_and_cpu_preflight_report` requires the in-session gate result. | `src/data/fixture_gate.py:830`; `scripts/gate_in_session.py:230`; `src/data/fixture_evidence.py` l.686–711 |
| **The local exemption is hard-coded.** `platform_label != "local" and …`. The platform enum is exactly `kaggle \| local`. CI declares `TEC_PLATFORM: local`. | `src/data/locked_test.py:497`, `:760`; `src/data/config.py:764`; `.github/workflows/verify.yml:103` |
| **Nothing records the environment per row.** No registry column or extension holds it. `capture_environment_lock` folds `pip freeze` into a hash only. | `src/data/experiment_registry.py:102–123`; `src/data/config.py:1257–1311` |
| **Write-once is enforced per path, not per run.** DEC predictions go under a per-`run_id` directory. | `scripts/06_train_and_predict.py:722`, `:1698`, `:1811`; `src/models/train.py:1575` |
| **The B-01 config hashes differ from today's only in line endings, not in content.** The recorded `experiment.yaml` hash `10028bf0…` equals the CRLF rendering of the `989f290` blob. `data.yaml` and `features.yaml` are still CRLF in the working tree. `experiment.yaml` and `seeds.yaml` are LF, although `.gitattributes` sets `eol=lf`. `ENVIRONMENT_IDENTITY_ITEMS` includes `config_hashes`, so a line-ending change alone changes the environment identity that D-49 item 4 matches on (PV-02 Rec 31). | `b01_runtime_identity.json`; `git show 989f290:configs/experiment.yaml`, rendered with CRLF, then `sha256sum`; `git ls-files --eol configs/*.yaml`; `src/data/fixture_gate.py:141` |
| **The November B-01 rows** were generated with the wheel identity **declared, not measured**: the install did not use `--require-hashes`, and libgfortran was not recorded (PV-02 Rec 27 = 2). | session record §1–4; `b01_provenance.json` |
| **Host, as measured by a reviewer** (authority level 6, not yet a governed measurement): 15.7 GB RAM; i9-12900H with 20 logical CPUs; 29.0 GB free on C:; no `.wslconfig`; `LongPathsEnabled` = 0. `tec-thesis-311` occupies 2.3 GB, against TE §9.3's 1.0 GB dependency allowance. | `GOV-2026-09-29-PV-02` BENCH and DATA seats |
| **No locked-test access.** `locked_test_accessed` is `true` on 0 of 1,657 registry rows. | `artifacts/registry/experiment_registry.jsonl`, counted 2026-09-30 |

### R2-3. Authority surfaces: re-derived with a platform-role vocabulary (Rec 11 = 2)

Revision 2's search key (`kaggle|both platforms`) could not see restatements that do not use
the word. Revision 3 adds a second key and prints what it finds.

**Derivation 1**, 2026-09-30:
- Pattern: `grep -niE "two (execution|platform|environment)s?|exactly two|platform variation|\bRAM\b|\bGPU|session|local (role|environment)|same python"`.
- Files: the Vision, the TE, the constraint register, `configs/*.yaml`, `requirements.txt`, `environment/*`.
- Hits per file: Vision 5, TE 14, register 6, `data.yaml` 1, `experiment.yaml` 4, `features.yaml` 0, `seeds.yaml` 0, `requirements.txt` 2, `environment/*` 0.

**Derivation 2:**
- Pattern: `grep -niE "kaggle|both (governed )?platforms"`.
- Files: `requirements.txt`, `pyproject.toml`, `environment/*`, `configs/*.yaml`.
- These files are outside revision 2's search scope.

**Every hit, classified.** "Already §R2" means revision 2 already lists the line.

| Hit | Classification |
|---|---|
| Vision l.325, 329, 1500 | already §R2 |
| **Vision l.1102** DEP-10 "deterministic CPU/GPU fixture test" | **new, forward-looking**: the GPU limb has no governed environment while `tf_gpu` is barred (§R4-3 item 8) |
| **Vision l.1394** "pass the CPU/GPU fixture tests" | **new, forward-looking**: same reason |
| TE l.22, 279 | not platform text |
| TE l.78, 502, 752 | consistent with D-83; unaffected |
| TE l.151, 530, 1012, 1016 | already §R2 |
| **TE l.495** §9.1 local row: role "Development, small tests, fixture runs, review, artifact inspection"; rule "Same Python 3.11 and exact pins" | **new, forward-looking**: local now carries training, G-06 and Class A acquisition, and environment (b) is CPython 3.10 under D-49 |
| **TE l.498** "There are exactly two execution environments" | **new, forward-looking**: D-83 names one platform with three environments. The same line's transfer rule is kept (§R4-3 item 6). |
| TE l.529 "Record CPU/GPU type, runtime, peak memory … for every run" | unaffected; already binding, and carried by §R3-3 item 5 |
| **TE l.604** NFR-PORT-01 removed because "only two platforms remain" | **new, rationale to review**: cross-environment consistency between (a) and (c) becomes load-bearing for G-07 (§R3-3 item 9) |
| **TE l.858** "fixture-derived tolerances that distinguish expected platform variation" | **new, forward-looking**: governs the (a)/(c) tolerance and its freeze order (§R4-3 item 5) |
| Register TC-01 and TC-04 | consistent; unaffected |
| **Register TC-03** "12-hour session on 30 GB RAM" | **new, forward-looking**: this is the Kaggle session envelope, replaced by a measured local envelope (§R3-3 item 7) |
| Register TC-03b, 03c, 03g | already §R2 |
| `data.yaml:169` ("in-session" verbal confirmation) | not platform text |
| `experiment.yaml` l.427, 433 | already §R2, historical |
| `experiment.yaml` l.436, 438 (comments on B-01 session re-verification) | historical provenance |
| `experiment.yaml` l.466–488 | already §R2 |
| **`experiment.yaml:520`** "deterministic on both governed platforms" | **new, forward-looking** |
| `requirements.txt` l.16, 30 (no GPU package; D-36 CPU wheel) | consistent; unaffected |
| **`requirements.txt` l.8** "reproducible on both governed platforms (Kaggle and local)" and **l.34** "(Kaggle AND local) check are OWED" | **new, forward-looking** |
| **`environment/install_wheels.ps1:20`** "BOTH-platform check still requires the Kaggle run" | **new, forward-looking** |
| **`environment/OFFLINE_REBUILD.md:210`** "satisfies the local half only; the Kaggle …" | **new, forward-looking** |
| **`environment/bootstrap_env.ps1:159`** "owed to Kaggle" | **new, forward-looking** |
| `environment/install_wheels.ps1:137` (native-Windows TF availability message) | not platform-role text |
| `pyproject.toml:51`, `:60` (lint configuration naming the Kaggle 3.10 venv and the `kaggle/` package builder) | historical provenance and tooling; unaffected |

**Code and test surfaces** (Rec 1 = 1; revision 2 did not search code):
- `src/data/fixture_gate.py` l.137 (the `KAGGLE` constant), l.830–836 (control 30);
- `scripts/gate_in_session.py` l.17–20, 227–237;
- `src/data/fixture_evidence.py` l.686–711;
- `tests/test_in_session_gate.py` l.108–111;
- `tests/test_clean_run.py` l.1382–1438 (control 30);
- the message at `src/models/lstm.py:165`.

The remaining `kaggle` string occurrences in code were counted by the PV-02 seats: `src` 34 lines,
`scripts` 26, `tests` 49. They are **not classified here**. Classifying every one of them is part
of the control-30 code ruling (§R5-3 item 9); it is not asserted done.

### R3-3. Consequences (revision 2 §R3 stands except where replaced here)

1. **Locked-test custody** (replaces revision 2 §R3 item 1; Recs 2 = 2, 3 = 1, 4 = 1, 16 = 1).
   - **(a) Interim bar: procedural, with detection (Rec 2 = 2).** Until `local` is characterised,
     no pre-G-05 audit and no G-06 may run on local. **The guard is not changed now.**
     `locked_test.py` still lets `local` through.
     - Instead, the G-05 evidence bundle carries a **preflight assertion**. For every
       `coverage_audit`, `regime_audit` or `locked_evaluation` access record, it checks that the
       record's `run_id` does not resolve to a registry row whose `platform` is `local` and that
       predates the characterising D-number. Any hit fails G-05 preflight.
     - **Accepted risk, stated plainly:** this detects after the fact; it does not prevent.
     - A local custody read made by operator error would still count as December being "seen"
       (`project.md` Forbidden, Vision §8.3). Its rows would carry the SD-03 stamp and not be gate
       evidence.
     - This departs from the board's preferred option. The PV-02 Validation Auditor made the
       reservation "a guard or test". The G-05 assertion is the test limb of that condition; it
       is not the guard limb.
   - **(b) Durability measurement protocol (Rec 4 = 1).** The Student sets the numeric value
     marked `<N>` before the measurement starts, and the Supervisor countersigns the protocol. No
     value is supplied here.
     - **Fault model:** process kill (hard terminate) and host power-loss or crash, each injected
       while an append of an access row and of a registry row is in flight.
     - **What is measured:** for each trial, whether every row the writer reported as committed
       (appended and fsync'd) is present and parses after restart; whether any row is torn or
       partial; whether any uncommitted row appears.
     - **Filesystems:**
       - native NTFS on the governed root;
       - the WSL2 `/mnt/c` drvfs mount and WSL2 ext4, but **only if** an environment that
         writes access or registry rows will ever run there.
       - Under (c) below, WSL2 is barred from restricted reads and writes, so for custody
         purposes only NTFS is measured.
     - **Trials:** `<N>` per fault type per filesystem.
     - **Pass:** zero committed rows lost and zero torn rows across all trials. Any loss fails
       the measurement.
     - **Record:** a measurement record with host, filesystem, writer commit, trial log and
       result, cited by the characterising D-number.
   - **(c) The characterising D-number (Rec 3 = 1)** must:
     - remove the hard-coded `!= "local"` exemption (`locked_test.py:497`, `:760`), so that
       admission is by set membership only;
     - key membership by **environment identity** (item 7), not by the platform label, so that
       CI (`TEC_PLATFORM: local`) and unmeasured WSL2 filesystems are **not** admitted;
     - come with a test that refuses a non-member environment.
   - **(d) Additional preconditions** for any local pre-G-05 audit or G-06:
     - the Rec 14 single governed access log is coded and tested (Rec 16 = 1);
     - the code-commit guard is in place (item 10).
2. **One-shot binding** (extends revision 2 §R3 item 2; Recs 5 = 3, 21 = 1).
   - **"Exactly once" means once per `phase_id` / `target_definition_id`, under that phase's own
     G-05 / G-P3 signature.** The Phase 2 December prediction on the new target lineage is
     designed (Vision l.279, R-27) and is not barred by this rule. The Vision's mandatory
     disclosure that Phase 2 is **not a second statistically independent blind test** is
     unchanged.
   - **Code ruling (Rec 5, limb 1).** `06_train_and_predict.py --partition DEC` refuses when any
     prior `locked_evaluation` access record, or any DEC receipt, exists for the same `phase_id`.
     It needs a negative control.
     - **Open for the Student:** the rule for retrying after an abort that happened before any
       prediction was written (§R5-3 item 12).
   - **Environment (c) (Rec 5, limb 2).** The G-07 clean run in (c) runs `06` over F1–F4 and REFIT
     only, **never DEC**. It uses a **required** sparse checkout that excludes
     `evidence/locked_test_restricted/`, so December cannot be reached from (c).
   - **Re-hash location (Rec 5, limb 3).** G-07's verification of G-06 re-hashes the frozen
     predictions **in environment (a)** through `assert_receipt_matches`
     (`src/models/train.py:1625`), logged through the guard. It never regenerates them.
3. **Environment (a) identity (Rec 7 = 2).**
   - Environment (a) stays `tec-thesis-311`. It is **not** rebuilt from the committed locks.
   - Its governed identity is the complete `pip freeze --all` and `conda list --explicit --md5`,
     recorded **after** `ml_dtypes==0.5.3` is restored (§R5-3 item 8), and cited by hash.
   - The 2026-09-30 pre-restore baseline is
     `evidence/environment_identity_2026-09-30_tec-thesis-311/`.
   - **Accepted consequence:** environment (a) is reproducible from its recorded identity, not
     from the committed locks. G-07 evidence must say so.
4. **Environment (c) definition (Rec 8 = 1).** Before any G-07 run in (c):
   - a committed `linux-64` hashed lock (conda plus wheels, `--require-hashes`) and a bootstrap
     script exist;
   - (c) runs from a **fresh clone at the recorded commit**, never the live `/mnt/c` working tree;
   - every (c) invocation sets `CUDA_VISIBLE_DEVICES=""` and records GPU visibility;
   - **Limitation, stated for the Supervisor:** (c) is *cross-OS on the same hardware*. It
     restores the operating-system limb of the G-07 two-environment property. It does **not**
     restore the cross-host limb that Kaggle supplied: (a) and (c) share the CPU, disk and host.
     The Supervisor acknowledges this explicitly before G-07.
5. **Tolerance freeze order (Rec 9 = 1).** This is the TE l.858 platform-variation tolerance,
   and the order is fixed:
   1. the measuring runs in (a);
   2. then **one** run in (c), pre-designated as a measuring run;
   3. then the Student's Q-31 tolerance freeze;
   4. then the (c) run that G-07 accepts.

   No tolerance is chosen after the accepted (c) run is seen.
6. **Kaggle fallback (Rec 10 = 2).** Kaggle may be used again only to **re-execute the whole
   confirmatory set**: F1–F4 tuning, the D-56 derivation, REFIT, all three seeds and DEC. It may
   never supply part of that set.
7. **Resource feasibility and envelope (Recs 12 = 1, 13 = 1).**
   - **Preconditions of adoption (Rec 12 = 1).** This corrects revision 2, which made the
     measurement a precondition of *retiring* Kaggle; the Student's PV-01 Rec 16 ruling said
     *adoption*. Adoption needs both of:
     - peak-RSS and CPU-model capture, coded under a Student code ruling with a negative control;
     - a local `scientific_1month` run measuring runtime, peak RAM and storage.
   - **Dormancy exit and retirement (Rec 13 = 1).**
     - The dormancy exit is tied to the Rec 4 (storage), Rec 5 (CPU seconds) and Rec 16 (RSS and
       CPU model) code rulings landing with negative controls.
     - **Retiring Kaggle** needs the first **instrumented local Class C clean run** (EV-14) as its
       evidence. A one-month run does not bound the full year.
   - **Local envelope replacing TC-03 (Rec 13 = 1).** It records measured values for:
     - host RAM;
     - the WSL2 memory cap (`.wslconfig`, or the default stated);
     - free disk on the governed volume, which also holds the WSL2 virtual disks;
     - the footprint of all three environments, accounted under TE §9.3.

     The reviewer-measured figures in §R1-3 are indications, not these measurements.
8. **In-environment critical set (Rec 14 = 1).** Before any governed run in environment X, for
   X ∈ {(a), (b), (c)}, the §18.3 critical set runs **inside X** and the result is captured in that
   run's evidence. This is TC-03g's in-environment limb carried from the Kaggle session to each
   local environment. For (b), `b01_iri` gains the `requirements.txt` pins that apply to it and
   `pytest`. D-49's 2026-09-20 addendum item 1 already requires this for fixture runs.
9. **Environment identity per run (Rec 6 = 1)** (replaces revision 2 §R3 item 7's statement).
   Code ruling:
   - add an R-18 named extension `environment_id`, drawn from the closed set `{a_native_win,
     b_wsl2_b01_iri, c_wsl2_g07}` and declared explicitly (for example `TEC_ENVIRONMENT`);
   - refuse when it is absent or unknown, and include it in the lock hash;
   - persist the eight TE §13.1 lock items per run, next to the registry row;
   - assert pin conformance at startup for governed runs: installed packages against environment
     (a)'s recorded identity, or against that environment's lock;
   - add a negative control for each of the above.

   The TC-03g in-session gate is then re-keyed to `environment_id` (item 11).
10. **Code-commit integrity (Rec 15 = 1).** The Rec 6 guard is a **precondition of G-06, G-07
    and any full-year B-01 run**:
    - `--code-commit` is refused when a git tree exists;
    - a `working_tree_dirty` field is recorded;
    - negative controls are in place.
11. **G-07 evidence path (Rec 1 = 1).** Code ruling: re-key control 30 and `gate_in_session.py`
    from the `kaggle` label to "the governed environment the run executes in".
    - It accepts (a) and (c) only.
    - Negative controls: a gate result from `b01_iri`, from CI, or from an environment whose lock
      differs from the caller's must each be refused.

    Until this lands, G-07's named evidence artifact cannot be produced under D-83.
12. **B-01** (extends revision 2 §R3 item 4; Recs 18 = 1, 19 = 1, 22 = 1, 27 = 2, 31).
    - **Mirror, cited exactly.** The fixture-run extension to be mirrored is the inline "Addendum
      2026-09-20 — item 4 resolved by resolution (a)" inside D-49 (`evidence/DECISIONS.md`
      l.2786). It is **not** the code-compatibility addendum at l.3483, which D-49 addendum 2
      calls "addendum 1".
    - **Smoke value (Rec 18 = 1):** bit-identity with `37.373754526924806` TECU. Any mismatch
      stops the run and goes to the Student, with both values recorded.
    - **Identity in code (Rec 22 = 1):** `iri.verify_runtime` is extended to check the measured
      wheel hash, glibc, libgfortran and the Python version against `interpreter_exception`, with
      a negative control. This is a code ruling.
    - **November fixture rows (Rec 27 = 2):** labelled "wheel identity declared, not measured".
    - **Config line endings (Rec 31):** because the identity match includes byte-level
      `config_hashes`, the working tree's configs must be renormalised to the committed `eol=lf`
      before any B-01 receipt that a later run must match. Alternatively, a code ruling hashes
      line-ending-normalised content. The Student chooses; see §R5-3 item 13.
13. **Long paths (Rec 23 = 1).** Environment (a)'s preflight records `LongPathsEnabled=1`, or
    states a maximum root length under which every manifest path stays within 260 characters.
    Four paths in the 2026-09-29 untracked-outputs manifest reach 260–264 characters. Changing the
    host setting is the Student's act.
14. **Re-acquisition (Rec 28).** Local re-acquisition under revision 2 §R3 item 9 is bound, as
    before and independent of platform, by:
    - DATA-07's provider-suffix, retrieval-date and SHA-256 recording;
    - the no-backfill-from-final-values rule;
    - the rule against mixing Dst grades (`project.md` Forbidden; D-10.1).

### R3a-3. Vision §15.2 change-record fields (Rec 20 = 1)

| §15.2 field | Entry |
|---|---|
| 1. Requested change and reason | Local as the sole platform for new governed runs; Kaggle dormant. Reason: the Student's instruction and FU-1R = A (§Basis) |
| 2. Alternatives | FU-1R option B: local for everything except B-01, with Kaggle kept for the B-01 leg. FU-1R option C: no platform change, with TE §9.1 roles kept on paper and the Kaggle limb of TE §9.2 left open for G-07. The Student rejected both |
| 3. Affected requirements, data, code, experiments, schedule, claims | Requirements and authority: §R2 plus §R2-3. Code: §R3-3 items 1, 2, 9–12. Experiments: environments and the tolerance freeze order (§R3-3 items 4–6). Schedule: adoption waits on §R3-3 item 7. Claims: none; no claim boundary changes |
| 4. Whether the locked test has been accessed | **No.** 0 of 1,657 registry rows have `locked_test_accessed=true` (2026-09-30) |
| 5. Required regeneration or invalidation | None. Historical Kaggle evidence keeps its provenance (revision 2 §R3 item 10). The November B-01 fixture rows are relabelled, not regenerated |
| 6. Approver, date, effective version | Student (adoption) and Supervisor (countersignature), both OPEN. Effective against Vision v4.3 and TE v3.4 |

### R4-3. Proposed D-text (for the Student to adopt, amend or reject)

> ## D-83 — Execution platform: local (native Windows plus WSL2 on the Student's laptop) as the sole platform for new governed runs; Kaggle dormant (Student proposal; Supervisor countersignature required)
>
> **Decision date:** <date of adoption>. **Decided by:** the Student, 2026-09-29 (FU-1R = A), and
> revised under the Student's rulings on `GOV-2026-09-29-PV-02` (2026-09-30). **Authority amended:**
> every forward-looking surface in CR-2026-09-29-PLATFORM-LOCAL-ONLY §R2 **and §R2-3**. **Ratifies:**
> D-49 addendum 2. **Adoption preconditions:** §R3-3 item 7. **Supervisor countersignature:
> REQUIRED, OPEN.** The authority equivalence is not invoked.
>
> 1. **Platform.** New governed runs execute on `LAPTOP-TV4UGFBC` in three named environments.
>    Each is recorded per run as `environment_id` (§R3-3 item 9):
>    - **(a)** native-Windows `tec-thesis-311`. Its governed identity is its recorded full freeze
>      after the pin restore (§R3-3 item 3). It is the environment for every stage script and for
>      the whole confirmatory set.
>    - **(b)** WSL2 `b01_iri`, only under D-49 and its addenda.
>    - **(c)** WSL2 G-07 clean-run, only for G-07 reproduction, under §R3-3 item 4.
>
>    TE §9.1's "exactly two execution environments" (l.498) is read as "one platform with three
>    named environments". Its transfer rule stands.
> 2. **Kaggle is dormant.** No new governed run executes on Kaggle. It may be used again only to
>    re-execute the whole confirmatory set, never part of it. Kaggle is retired by a further note
>    under this D-number, on the evidence of the first instrumented local Class C clean run.
>    Artifacts already produced on Kaggle keep their provenance.
> 3. **Locked test.**
>    - Until `local` is characterised under §R3-3 item 1(b)–(d), no pre-G-05 audit and no G-06
>      runs on local. The G-05 preflight assertion of §R3-3 item 1(a) detects any breach.
>    - G-06 then runs CPU-only in (a), with exact pins, **once per `phase_id` /
>      `target_definition_id`**.
>    - A repeated `--partition DEC` is refused by code (§R3-3 item 2).
>    - G-07 re-hashes in (a) and never regenerates. Environment (c) never runs DEC and cannot
>      reach the restricted root.
>    - `tf_gpu`, and any environment off its governed identity, are barred from governed runs.
>    - The Phase 2 non-independence disclosure is unchanged.
> 4. **B-01.**
>    - D-49 addendum 2 is ratified.
>    - A full-year B-01 run additionally requires the extension of addendum 2 to the B-01 fixture
>      runs, mirroring the inline D-49 addendum of 2026-09-20 (DECISIONS l.2786).
>    - It also requires the identity checks, coded in `verify_runtime`.
>    - The smoke value must be reproduced bit-identically.
>    - Config line endings must be consistent (§R3-3 item 12).
> 5. **Preflight and G-07** (TE §9.2, l.858).
>    - The `environment_and_cpu_preflight_report` shows, in (a): install-from-pins against the
>      recorded identity; a completed skeleton run; the §18.3 critical set run inside (a);
>      measured CPU runtime, peak RAM and storage; and the long-path state.
>    - It shows a clean-run reproduction in (c) under §R3-3 item 4.
>    - The (a)/(c) tolerance is frozen in the order of §R3-3 item 5.
>    - The in-session gate is keyed to `environment_id`.
> 6. **Transfers.** Every transfer between WSL2 and Windows carries a SHA-256 manifest of every file
>    moved, and the transfer is recorded (TE §9.1).
> 7. **CI** is a non-scientific verification surface governed by the Rec 47 / P2 record, not an
>    execution platform, and it is never an admitted custody environment.
> 8. **Unchanged:**
>    - CPU is a complete path, GPU is an optional accelerator only, and there is no GPU-only
>      dependency. While no governed GPU environment exists, the GPU limbs of Vision l.1102 and
>      l.1394 are **not applicable**, not failed.
>    - Every locked-test rule and every frozen value is unchanged.
>    - The re-acquisition obligations of §R3-3 item 14 are unchanged.
> 9. **If this decision is rejected or amended,** the Kaggle limb of TE §9.2 and TC-03g reverts to
>    an open G-07 item. D-49 addendum 2 stands on its own terms.

### R5-3. Open items (replaces revision 2 §R5)

| # | Item | Owner | Due |
|---|---|---|---|
| 1 | Adopt, amend or reject §R4-3 | Student | after items 2–7 |
| 2 | Full-board re-review of revision 3, scoped to G-06 and G-07 | per `/review-tec-governance` | before adoption |
| 3 | Code ruling: peak-RSS and CPU-model capture, with a negative control (PV-01 Rec 16; PV-02 Rec 12) | Student | **adoption precondition** |
| 4 | Local `scientific_1month` run measuring runtime, peak RAM and storage. It needs the Rec 4 and Rec 5 code rulings, a clean root, both fixtures in order, and item 3. | Student | **adoption precondition** |
| 5 | Countersign | Supervisor | after adoption |
| 6 | Supervisor acknowledgement that (c) is cross-OS on the same hardware (§R3-3 item 4) | Supervisor | before G-07 |
| 7 | Durability protocol: the Student sets `<N>`; the Supervisor countersigns (§R3-3 item 1(b)) | Student; Supervisor | before adoption |
| 8 | Restore `ml_dtypes==0.5.3` in (a), then record and hash the governed identity (§R3-3 item 3) | Student | before any governed run in (a) |
| 9 | Code ruling: re-key control 30 / `gate_in_session.py` to `environment_id`, with negative controls, and classify every `kaggle` string in code (§R3-3 item 11) | Student | before any G-07 evidence run |
| 10 | Code ruling: `environment_id`, per-run lock items, pin conformance, with negative controls (§R3-3 item 9) | Student | before G-06 and G-07 |
| 11 | Characterising D-number, with the exemption removed, identity-keyed membership and a non-member refusal test, after the measurement (§R3-3 item 1(c)). **Validation Auditor veto reserved.** | Student | before any local pre-G-05 audit or G-06 |
| 12 | Code ruling: refuse a repeated `--partition DEC` per `phase_id`, with a negative control. **The Student rules the retry-after-abort-before-write rule.** | Student | before G-06 |
| 13 | Choose: renormalise config line endings to `eol=lf`, or a code ruling hashing normalised content (§R3-3 item 12) | Student | before any B-01 receipt a later run must match |
| 14 | Code rulings: the Rec 6 `--code-commit` guard (item 10); the Rec 14 single governed access log; the G-05 preflight custody assertion (item 1(a)); the `verify_runtime` identity checks (item 12). Each with negative controls. | Student | before G-06 / G-07 / full-year B-01, and before the pre-G-05 audit |
| 15 | `linux-64` hashed lock and bootstrap for (c); sparse-checkout / fresh-clone procedure | Student | before G-07 |
| 16 | Extend D-49 addendum 2 to the B-01 fixture runs; mirror it in `interpreter_exception`; the (b) critical-set install (§R3-3 item 8) | Student | before any full-year B-01 run |
| 17 | Local envelope measurements replacing TC-03 (§R3-3 item 7); `LongPathsEnabled` or a root-length rule (§R3-3 item 13) | Student | before G-07 |
| 18 | In-place annotation of every forward-looking surface in §R2 and §R2-3 after adoption, under `CHANGE_RECORD_PROCEDURE.md`; §13 corrections to `team.md` and `project.md` | Student | after adoption |
| 19 | Next code change touching `locked_test.py`: fix the docstring at l.51 ("qualifies" should read "disqualifies"; PV-02 Rec 29) | Student | with item 11 |

---

## Revision 2 (superseded 2026-09-30 by Revision 3, retained verbatim)

**Status: DRAFT, NOT ENACTED.**

- No D-number has been written. `evidence/DECISIONS.md` is the Student's register; the D-text in
  §R4 is offered for the Student to adopt, amend or reject.
- It needs the Supervisor's countersignature and a **full-board** governance review scoped to
  **G-06 and G-07** (Rec 20).
- **The student/supervisor authority equivalence recorded elsewhere in the register is NOT
  invoked:** this amends Vision D-129, so the countersignature is required (Rec 19).

**Basis.**
- The Student's answer to FU-1R (A), given 2026-09-29 on corrected facts, in
  `aidlc/…/operation/performance-validation/performance-validation-questions.md`.
- The Student's rulings on `GOV-2026-09-29-PV-01` Recs 1, 2, 3, 16, 19 and 20, recorded in
  `governance/CHANGE_RECORD_2026-09-29_GOV-PV-01_rulings.md`.
- Revision 1 is retained below, marked superseded.

### R1. Facts (verified 2026-09-29)

| Fact | Source |
|---|---|
| D-49 addendum 2 (2026-09-28) rules WSL2 (Ubuntu) on `LAPTOP-TV4UGFBC` IN as satisfying D-49's B-01 exception, recorded as `local`. It does **not** extend to model training or the fixture ladder. The ruling is the owner's alone, with no Supervisor signature. | `evidence/DECISIONS.md` l.3510 ff. |
| B-01 ran on WSL2 on 2026-09-28: pin check before and after PASSED, R-59 `passed`, 2,160 November rows, 0 errors, `workload_seconds` 535.353. | `artifacts/exec_evidence/run_2026-09-28_b01_wsl_local/SESSION_A_LOCAL_EXECUTION_RECORD.md`; `artifacts/external/b01/b01_provenance.json` |
| The actual WSL2 host reports glibc 2.43. The install was not done with `--require-hashes`. The wheel hash in the validation report is declared, not measured. The libgfortran version is unrecorded. | `b01_runtime_identity.json`; session record §1; `src/external/iri.py` l.523, 573–628, 928 |
| `tec-thesis-311` on native Windows is CPython 3.11.16 with TF 2.21.0 and **`ml_dtypes` 0.5.4, against a pin of 0.5.3**. | `pip freeze`; `requirements.txt:41` |
| TF 2.21 on native Windows sees no GPU. A separate `tf_gpu` environment (TF 2.18.0 plus CUDA) exists and does **not** carry the D-36 pin. | TF import; D-49 addendum 2 |
| `locked_test.py` refuses the durability-unverified platform except `local` (l.481–505, 759–768). The stated reason is that local rows are never gate evidence (SD-03). `CHARACTERISED_DURABILITY_PLATFORMS` is empty (`config.py:479-482`). | code |

### R2. Authority surfaces this decision amends

These were derived with `grep -niE "kaggle|both platforms"` over the Vision, the TE, the
constraint register, `configs/` and the runbooks, and the list was printed before being written
(`GOV-2026-09-29-PV-01` Rec 3).

**Forward-looking, and amended by §R4:**

| Surface | Location |
|---|---|
| Vision | l.66 (platform change row); l.325 (Kaggle GPU hours); l.329 §4.4 ("Kaggle (primary compute) and local"); l.1098 DEP-06; l.1214 D-129; l.1402 G-07 checklist; l.1500 CPU-budget row |
| TE | l.75 (platform row); l.151 (~30 Kaggle GPU hours, parallel to Vision l.325); l.437 (TF pin "frozen only after Kaggle/local fixture installation passes"); l.496 §9.1 Kaggle role; l.530 §9.2 preflight "on both Kaggle and local"; l.759 container-gate premise "both platforms"; l.771 and l.864–868 (acquisition notebook "in Kaggle with Internet enabled", i.e. Class A); l.1012 EV-14; l.1016 EV-18; l.1099 TA-03; l.1122 TA-26 |
| Constraint register | TC-02; TC-03b; TC-03c; TC-03d; TC-03g |
| `configs/experiment.yaml` | l.466–488 `interpreter_exception`, which names the Kaggle image only. Addendum 2 was never mirrored here. |
| Runbook | `governance/RUNBOOK_2026-09-26_kaggle_b01_fixture_leg.md`, to be marked superseded for new runs |
| Memory layers (§13 ritual only) | `team.md` § Deployment; `project.md` Mandated (TC-03g Kaggle-session rule) |

**Historical, and unaffected** (executed or closed records): Vision l.42, 82, 409, 1072 (R-28),
1104 (DEP-12), 1264 (D-142); TE l.55, 112, 344, 1020 (EV-22), 1127 (TA-31); the TE §13.1
platform enum value `kaggle` (l.756), which remains valid for historical rows; TE l.482 (a
rationale only); `configs/experiment.yaml` l.427 and l.433 (comments recording where the D-45
pins were verified and measured, which is provenance).

*Completed 2026-09-29 after the `GOV-2026-09-29-PV-01` closure verification. The first issue of
§R2 omitted TE l.151, TE l.437 and the two config comment lines, although it claimed to be
grep-derived.*

### R3. Consequences named

1. **Locked-test custody (Rec 2; Validation Auditor veto).** Moving G-06 and the pre-G-05 audit
   onto local puts them on the platform the guard exempts, and the exemption rests on "local is
   never gate evidence". **Neither may run on local** until both of the following exist:
   - a durability measurement on the local platform (W-6 step 8, on native NTFS and, if used,
     WSL2);
   - a D-number adding `local` to `CHARACTERISED_DURABILITY_PLATFORMS`, with a test showing G-06
     rows on local no longer carry the refusing SD-03 stamp.
2. **One-shot binding (Rec 2).**
   - G-06 executes **CPU-only, in native-Windows `tec-thesis-311` with every pin exact**.
   - G-07 verifies G-06 by **re-hashing the frozen predictions, never by regenerating them**.
   - Revision 1's "the CPU path must still reproduce every result" is withdrawn wherever it could
     imply a second December generation.
   - The `tf_gpu` environment is barred from every governed run.
3. **G-07 two-environment property (Rec 3).** TE §9.2 and the Vision G-07 checklist require
   reproduction in two environments. Dropping Kaggle would silently remove that. A **second
   clean-run environment on the same laptop is named: WSL2 Linux carrying the governed CPython
   3.11 and the full pins.** It is used for the G-07 clean run only, and restores the cross-OS
   limb.
4. **Full-year B-01 (Rec 3).**
   - Receipts must match the consuming environment identity (D-49 item 4), but addendum 2
     excludes the fixture ladder. A full-year B-01 therefore needs **an addendum extending D-49
     addendum 2 to the B-01 fixture runs**, mirroring addendum 1 for Kaggle. D-49 option (b), an
     `iricore` build for CPython 3.11, remains the fallback.
   - Identity checks are owed before any non-fixture B-01 run: a measured wheel hash (`pip
     download` plus `--require-hashes`, or an installed-files check against `RECORD`), the
     libgfortran and glibc versions, and reproduction of the Kaggle smoke value
     `37.373754526924806` TECU in the governed `b01_iri` environment.
   - `configs/experiment.yaml interpreter_exception` gains the WSL2 identity under that addendum.
5. **Resource feasibility (Rec 16).** No local full-year runtime, RAM or storage measurement
   exists; A-6 and A-11 are open. **Kaggle becomes dormant, not retired**, until a local
   `scientific_1month` run measures runtime, peak RAM and storage. Peak-RSS and CPU-model capture
   is a code ruling owned by the Student.
6. **Transfers (Rec 3).** TE §9.1's transfer rule ("moves with a SHA-256 manifest and the
   transfer is recorded") applies to **every WSL2-to-Windows transfer**. The B-01 transfer
   manifest must list all five B-01 files, where today it lists one.
7. **Environment identity (Rec 3).** Every registry row records which local environment wrote it:
   native Windows, WSL2 `b01_iri`, or WSL2 G-07 clean-run. WSL2 runs use the same working tree
   (`/mnt/c/...`) or a sparse checkout that excludes `evidence/locked_test_restricted/`. This is
   to be resolved together with clauses 2–3 of
   `governance/CHANGE_RECORD_2026-09-27_platform_bound_RULING_REQUEST.md`.
8. **CI (Rec 3).** GitHub Actions (`.github/workflows/verify.yml`, labelled `TEC_PLATFORM=local`)
   is a **non-scientific verification surface, not an execution platform**. Its authorisation
   stays with the Rec 47 / P2 record and that record's pending countersignature. Its `local`
   label is to be corrected there.
9. **Class A acquisition.**
   - Future re-acquisition (for example DATA-07's) runs on the local platform, with Internet, under
     TE §9.2 Class A.
   - The acquisition notebook's "in Kaggle" wording (TE l.771, 864–868) is amended accordingly.
   - Every December custody restriction applies unchanged.
10. **Historical evidence** produced on Kaggle keeps its provenance, and nothing is re-acquired.

### R4. Proposed D-text (for the Student to adopt, amend or reject)

> ## D-83 — Execution platform: local (native Windows plus WSL2 on the Student's laptop) as the sole platform for new governed runs; Kaggle dormant (Student proposal; Supervisor countersignature required)
>
> **Decision date:** <date of adoption>. **Decided by:** the Student, 2026-09-29. FU-1R = A, on
> corrected facts, after the original instruction "i dont want to run anything on kaggle anymore … i
> like to do all the code runnings on my local system". **Authority amended:** every forward-looking
> surface listed in CR-2026-09-29-PLATFORM-LOCAL-ONLY §R2. **Ratifies:** D-49 addendum 2.
> **Supervisor countersignature: REQUIRED, OPEN.** The authority equivalence is not invoked.
>
> 1. **Platform.** New governed runs execute on the local platform, which is the Student's laptop
>    `LAPTOP-TV4UGFBC` and consists of three named environments:
>    - (a) native-Windows `tec-thesis-311`, the default for every stage script;
>    - (b) WSL2 `b01_iri`, only under D-49 and its addenda;
>    - (c) WSL2 G-07 clean-run, CPython 3.11 with the full pins, only for G-07 reproduction.
>
>    Every registry row records its environment.
> 2. **Kaggle is dormant.** No new governed run executes on Kaggle. It stays available as a
>    fallback until a local `scientific_1month` run has measured runtime, peak RAM and storage.
>    Retirement then needs a further note under this D-number. Artifacts already produced on
>    Kaggle keep their provenance.
> 3. **Locked test.**
>    - The pre-G-05 December audit and G-06 do **not** run on local until: local durability is
>      measured (W-6 step 8), `local` enters `CHARACTERISED_DURABILITY_PLATFORMS` under a D-number,
>      and a test shows local G-06 rows are accepted as gate evidence.
>    - G-06 then runs CPU-only in environment (a), with exact pins, exactly once.
>    - G-07 verifies G-06 by re-hashing and never regenerates.
>    - `tf_gpu` and any environment off the D-36 pin are barred from governed runs.
> 4. **B-01.**
>    - D-49 addendum 2 is ratified.
>    - A full-year B-01 run additionally requires an addendum extending it to the B-01 fixture runs,
>      plus the identity checks in §R3 item 4.
>    - `experiment.yaml interpreter_exception` is updated under that addendum.
> 5. **Preflight (TE §9.2).** The `environment_and_cpu_preflight_report` shows install-from-pins, a
>    completed skeleton run and measured CPU runtime, peak RAM and storage in environment (a), and a
>    clean-run reproduction in environment (c).
> 6. **Transfers.** Every transfer between WSL2 and Windows carries a SHA-256 manifest of every file
>    moved, and the transfer is recorded (TE §9.1).
> 7. **CI** is a non-scientific verification surface governed by the Rec 47 / P2 record, not an
>    execution platform.
> 8. **Unchanged:** CPU is a complete path; GPU is an optional accelerator only; there is no GPU-only
>    dependency; every locked-test rule; every frozen value.
> 9. **If this decision is rejected or amended,** the Kaggle limb of TE §9.2 and TC-03g reverts to
>    an open G-07 item. D-49 addendum 2 stands on its own terms.

### R5. Open items

| # | Item | Owner |
|---|---|---|
| 1 | Adopt, amend or reject §R4 | Student |
| 2 | Countersign | Supervisor |
| 3 | Full-board governance review of this record, scoped to G-06 and G-07 | per `/review-tec-governance` |
| 4 | Local durability measurement and the `CHARACTERISED_DURABILITY_PLATFORMS` D-number, before any local G-06 or pre-G-05 audit | Student |
| 5 | Addendum extending D-49 addendum 2 to the B-01 fixture runs; identity checks; config mirror | Student |
| 6 | Local `scientific_1month` measurement (a precondition of retiring Kaggle) | Student |
| 7 | In-place annotation of the §R2 surfaces under `CHANGE_RECORD_PROCEDURE.md` after adoption; §13 corrections to `team.md` and `project.md` | Student |
| 8 | Restore `ml_dtypes==0.5.3` before any governed run in environment (a). Source: the Student's Rec 2 ruling ("G-06 … CPU-only … with every pin exact") and TE §8.1 exact pins. This is **not** a reversal of Rec 9 (option 2, disclose only), which ruled on the past runs. | Student |

---

## Revision 1 (superseded 2026-09-29, retained verbatim)

> **SUSPENDED, 2026-09-29, under `GOV-2026-09-29-PV-01` (verdict FAIL).** Do not adopt or
> countersign this draft. The body below is kept verbatim as the record of what was drafted. It
> is **factually wrong in §1, §2, §3.1–3.2, §4 item 3 and §5 B-1**:
>
> - `evidence/DECISIONS.md` **D-49 addendum 2 (2026-09-28)** already rules WSL2 on this laptop IN
>   as the `local` platform for B-01.
> - B-01 has already run there (R-59 `passed`; 2,160 rows).
> - "B-01 loses its only proven route" and "needs a D-49 amendment" are false.
> - The glibc of the actual host is 2.43, not 2.35.
> - `ml_dtypes` is off-pin (0.5.4 vs 0.5.3), so "matching `requirements.txt`" in §2 is false.
>
> The Validation Auditor seat **vetoes item 1** as drafted: G-06 and the pre-G-05 audit may not
> move to local until the custody consequence (Rec 2) is closed.
>
> **Redraft, owed after the Student's answer to FU-1R**
> (`…/performance-validation-questions.md`), per the Student's rulings in
> `governance/CHANGE_RECORD_2026-09-29_GOV-PV-01_rulings.md`:
>
> - **Rec 1:** cite addendum 2. Redraft item 3 as ratification of addendum 2, and name its open
>   limbs.
> - **Rec 2:** name the custody consequence.
>   - `locked_test.py` exempts `local` from the durability refusal on the ground that local rows
>     are never gate evidence (SD-03).
>   - Require a local durability measurement (W-6 step 8 on local, NTFS and WSL2) and a D-number
>     adding `local` to `CHARACTERISED_DURABILITY_PLATFORMS` before any G-06 or pre-G-05 audit on
>     local.
>   - Bind G-06 to CPU-only native `tec-thesis-311`.
>   - G-07 verifies G-06 by re-hashing, never by regenerating.
>   - Remove the "CPU path must reproduce every result" wording that collides with the one-shot
>     rule.
>   - Bar the unpinned `tf_gpu` environment (TF 2.18) from governed runs.
> - **Rec 3:** derive, print and name every Kaggle-bearing authority surface:
>   - Vision §4.4, DEP-06 and the checklist rows;
>   - TE §13.1/§13.2/§19 TA-03/TA-26 and EV-14/EV-18;
>   - `experiment.yaml interpreter_exception`;
>   - the B-01 runbook;
>   - Class A acquisition.
>
>   Also add:
>   - a second clean-run environment (WSL2 with the 3.11 pins) to keep G-07's two-environment
>     property;
>   - an extension of addendum 2 to the B-01 fixture runs (receipt identity);
>   - a B-01 identity list: measured wheel hash, libgfortran/glibc versions, and the Kaggle
>     smoke-value reproduction;
>   - a CI non-platform clause (Rec 47 / P2);
>   - a §9.1 transfer-manifest clause for WSL2 to Windows;
>   - an environment-identity field;
>   - a cross-reference to `CHANGE_RECORD_2026-09-27_platform_bound_RULING_REQUEST.md`.
> - **Rec 16:** make a local `scientific_1month` measurement of runtime, peak RAM and storage a
>   precondition. Kaggle stays dormant, not retired, until then.
> - **Rec 19:** add a fallback if D-83 is rejected: the Kaggle limb reverts to an open G-07 item.
>   State that the student/supervisor authority equivalence is **not** invoked.
> - **Rec 20:** add G-06 to open item 4.

**Status: DRAFT, NOT ENACTED.** This record proposes a D-number and does not write one.
`evidence/DECISIONS.md` is the Student's register (`project.md` Corrections,
code-generation c31). Until the Student adopts the D-text in §4 **and** the Supervisor
countersigns it, the governing documents stand exactly as written: Kaggle remains the
"primary compute" platform (TE §9.1), and nothing in this record changes a frozen value,
fills a `TBD — freeze gate`, or authorises any run.

**Origin.** AI-DLC stage `performance-validation` (4.6), intent
`260813-tec-hourly-forecast`. At Question 4 of
`aidlc/…/operation/performance-validation/performance-validation-questions.md`, the Student
answered, verbatim: *"i dont want to run anything on kaggle anymore i have both gpu and cpu
on my own laptob and i like to do all the code runnings on my local system"*. At Follow-up
FU-1 the Student chose option A: draft this record, with local as the sole platform, B-01
included. The confirmation receipt was recorded on 2026-09-29.

**Why a record and not a stage answer.** Under `project.md` § Way of Working, a human's
disposition may narrow what a rule requires; it may not relocate a rule the governing
documents fix. The platform roles are fixed in TE §9.1–§9.2 and in Vision D-129, so the change
has to land as a decision, not as an artifact edit.

## 1. What the governing documents say today (quoted, not paraphrased)

| Source | Text |
|---|---|
| TE §9.1 | Local: "Development, small tests, fixture runs, review, artifact inspection" — "Same Python 3.11 and exact pins". Kaggle: "Primary compute and Phase 1 acquisition/audit host". "There are exactly two execution environments. If an artifact must move between them, it moves with a SHA-256 manifest and the transfer is recorded." |
| TE §9.2 | "The `environment_and_cpu_preflight_report` must demonstrate a successful install from pins on both Kaggle and local, a completed skeleton run, and measured CPU runtime, RAM, and storage. No GPU-only dependency may exist." |
| Vision decision table | D-129 (Q-29): "Python 3.11 with exact pins and per-run freeze; Kaggle plus local only; CPU sufficient; Colab, Drive, and the container gate closed" — **Approved** |
| Vision checklist | "CPU clean-run contract tested on Kaggle and local."; CPU budget row: "Benchmark runtime, RAM, storage on Kaggle and local" |
| `constraint-register.md` | TC-03c (`hard`): "Two execution platforms only: Kaggle as primary compute, local for development and cross-check". TC-03g (`hard`): preflight report "demonstrating install-from-pins on both platforms" |
| `evidence/DECISIONS.md` D-49 | the B-01 exception covers "the isolated Kaggle B-01 IRI execution environment" only (CPython 3.10.12, `iricore==1.8.0`) |

## 2. Facts checked on the Student's laptop, 2026-09-29

| Fact | Derivation |
|---|---|
| Local governed environment `tec-thesis-311`: CPython 3.11.16, `tensorflow` 2.21.0, `matplotlib` 3.9.0, matching `requirements.txt` | `conda run -n tec-thesis-311 python -c "import tensorflow, matplotlib, sys …"` |
| `iricore` is **not installed** locally. D-49's route is a Linux `manylinux_2_35` wheel on CPython 3.10.12; no native-Windows route has been found | `importlib.util.find_spec('iricore')` returns `None`; D-49 |
| GPU: NVIDIA GeForce RTX 3060 Laptop GPU, driver 572.83, is present but **invisible to TensorFlow**: "TensorFlow GPU support is not available on native Windows for TensorFlow >= 2.11". `list_physical_devices('GPU')` returns `[]` | `nvidia-smi`; TF import |

## 3. Consequences, each named so none is discovered later

1. **B-01 (IRI-2016 benchmark) loses its only proven route.** A local route is required
   before any B-01 run. The candidate is WSL2 Ubuntu 22.04 (glibc 2.35) with a CPython 3.10.12
   virtualenv and the D-49-pinned wheel. That is itself an amendment of D-49, which names
   Kaggle, and it must be demonstrated (install from hashes, R-59 validation report `passed`,
   index-file hashes matching the D-45 annotation) before it is relied on. **Blocker B-1.**
2. **Is WSL2 a third platform?** TC-03c permits exactly two. WSL2 on the same laptop is
   proposed here as part of the *local* platform, with its environment identity recorded per
   run. Whether that reading is acceptable is part of what the Supervisor countersigns.
3. **TE §9.2 / TC-03g "on both platforms"** becomes "on the local platform", and on WSL2 as
   well if B-01 runs there. This changes G-07's preflight evidence, which is exactly why the
   Supervisor must countersign.
4. **GPU stays an accelerator only** (TC-01; TE §9.2). With WSL2, TensorFlow could see the
   RTX 3060. Any GPU-executed run records CPU/GPU type (TE §9.2) and its nondeterministic
   operations (NFR-DET-01), and the CPU path must still reproduce every result. This record
   changes none of that.
5. **Historical Kaggle evidence is unaffected.** Phase 1 acquisition and audit artifacts
   produced on Kaggle keep their provenance; no re-acquisition is implied (TE §9.2 Class A:
   "Existing data is not re-downloaded without an independently justified and recorded need").
6. **Memory-layer lines that would go stale on adoption**, to be corrected only through the
   AI-DLC §13 learnings ritual, never edited directly:
   - `team.md` § Deployment: "Exactly two execution platforms: Kaggle (primary compute …)";
   - `project.md` Mandated: "ALWAYS run the critical test set and both walking-skeleton
     fixtures **inside the Kaggle session** before any governed run executed there". This
     stays literally true, but becomes vacuous; its intent (test in the environment the
     governed run executes in) carries over to local.

## 4. Proposed D-text (for the Student to adopt, or amend, or reject)

> ## D-83 — Execution platform: local as the sole platform for all remaining runs (Student proposal; Supervisor countersignature required)
>
> **Decision date:** <date of adoption>. **Decided by:** the Student, 2026-09-29 ("i dont want
> to run anything on kaggle anymore … i like to do all the code runnings on my local system").
> **Authority amended:** TE §9.1 (platform roles), TE §9.2 (preflight report "on both Kaggle and
> local"), Vision D-129 (Q-29), `constraint-register.md` TC-03c and TC-03g, D-49 (B-01
> environment). **Supervisor countersignature: REQUIRED, OPEN.**
>
> 1. From adoption onward, every governed run — fixture, full-year (TE §9.2 Class C), tuning,
>    evaluation, and the G-06 locked evaluation — executes on the local platform: the Student's
>    laptop, governed environment `tec-thesis-311` (CPython 3.11, exact pins).
> 2. Kaggle is retained only as the historical provenance host of artifacts already produced
>    there; no new governed run executes on Kaggle.
> 3. The local platform may include one WSL2 Linux environment on the same laptop, used only
>    where a pinned dependency has no native-Windows route (today: B-01's `iricore`). Its
>    environment identity is recorded per run. B-01 may run there only after a D-49 amendment
>    records the route and its demonstration (install from hashes; R-59 `passed`; D-45 index
>    hashes).
> 4. The `environment_and_cpu_preflight_report` demonstrates install-from-pins and a completed
>    skeleton run on the local platform (and on the WSL2 environment where used), with measured
>    CPU runtime, RAM and storage.
> 5. Unchanged: CPU is a complete path; GPU is an optional accelerator only; no GPU-only
>    dependency; the locked-test rules; every frozen value.

## 5. Open items

| # | Item | Owner |
|---|---|---|
| 1 | Adopt, amend or reject §4 | Student |
| 2 | Countersign the adopted D-number (it amends D-129 and TE §9.1/§9.2) | Supervisor |
| B-1 | Demonstrate a local B-01 route and record the D-49 amendment | Student (the demonstration can be agent-assisted; the ruling is the Student's) |
| 3 | §13-ritual corrections to `team.md` § Deployment and the `project.md` Kaggle rule, after adoption | Student, at an AI-DLC learnings gate |
| 4 | Governance review of this record: full board, because it changes the reproducibility-gate evidence (G-07) | per `/review-tec-governance` |
