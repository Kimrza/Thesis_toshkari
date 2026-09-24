# Ruling request — 2026-09-21 — the `GOV-2026-09-20-CG-01` items that need a human decision

**Raised by:** the agent, on the project decision owner's instruction of 2026-09-21 to close
out the board's open items. **Repository state:** written from `HEAD = de1732f` plus the
2026-09-21 working tree. **Nothing below is decided here.** Each item states the question, the
evidence it rests on, the options with their consequences, a recommendation, and who owns it.
No governed value is filled, no decision is written to `evidence/DECISIONS.md`, and no gate is
signed by this document.

The three items the owner asked to have *proposed* rather than decided are §1, §2 and §3.
§4 records what could not be done at all and why.

---

## §1 — G-09: the historical identity literal in git history (Recommendation 39 / DATA-16)

**Question.** What is done about the personal email address that exists in the committed
history of `notebooks/madrigal_phase1_coverage_audit.ipynb`, and in thirteen committed
manifests carrying `user_fullname` / `user_affiliation`?

**State, measured 2026-09-21.** The *working-tree* literal was removed on 2026-09-20 (first
remediation pass) and the notebook's guard refuses the sentinel, so **no new commit propagates
it**. `git ls-files` finds no live occurrence. The *history* still carries it: the finding's
own record (`GOV-2026-08-20-RA-01.md:294`, finding `DATA-16`) established that it is present
in all four commits of that notebook's history.

**The bind, stated exactly.** TA-22 requires a secret scan over **tree and history** returning
clean. History cannot be rewritten without rewriting the commits the freeze-gate tags point
at, and `team.md` § Way of Working makes those tags the recoverable record of each gate —
`project.md` § Forbidden and NFR-AUD-01 make the audit trail immutable. So the two obligations
are jointly unsatisfiable on the existing range, and only a human may choose which yields.

**Options.**

1. **Accept and disclose.** Record the historical breach as accepted, with a reviewed, dated
   `.gitleaks.toml` allowlist entry naming the exact commit range and the exact literal, and
   a G-09 gate-record entry stating that TA-22's history limb is discharged *as bounded* — the
   tree is clean, the history carries a known, disclosed, non-credential personal identifier.
   *Consequence:* TA-22 is never "clean" in its literal wording; it is clean-with-a-named-
   exception, and a reader of the gate record sees the exception. No tag moves. This is the
   only option that preserves the audit trail intact.
2. **Rewrite history.** `git filter-repo` over the range, re-tag every freeze gate, force-push.
   *Consequence:* every commit hash changes, so every `code_commit` recorded in the experiment
   registry, in every environment lock, in every change record and in every unit record becomes
   a dangling reference — the exact property §13.1's environment lock exists to provide. This
   trades a disclosed personal identifier for a broken provenance chain across the whole
   project. **Not recommended, and stated so plainly.**
3. **Defer again.** *Consequence:* the item has been open since 2026-08-20; deferring past
   G-09 means the gate is approached with a known unremediated NFR-SEC-01 item and no decision.

**Recommendation: option 1**, which is also what Recommendation 39 recommended ("(1)"), and
what DATA-16 asked for when it split prospective cleanliness from the unrewritable history.
**No history rewrite is performed by anyone until this ruling exists** — that is the standing
instruction until the owner rules otherwise.

**Owner:** Student + Supervisor. **Due:** G-09.

**Decision required — Approve / Reject / Modify / Postpone.**

---

## §2 — Rec 15: may the two persistence baselines read 1 December history for a 2 December origin?

**Question.** M-01 (persistence, `y(t−h)`) and M-02 (24-hour seasonal persistence,
`y(t−24 h)`) read target history strictly *before* the row they forecast. On the locked
partition the frame they are handed begins at **2 December 00:00** (D-28's embargo excludes
December's first 24 hours), so M-01 cannot forecast 2 December 00:00 and M-02 cannot forecast
any hour of 2 December. Those rows carry a missing `y_hat`, drop out of the comparison-wide
intersection mask, and the scored set becomes **29 days** while every artifact discloses 30.

**What is already fixed and needs no ruling.** The *disclosure* half (Recommendation 15's
option 2, the mandatory remediation) landed on 2026-09-20: `require_locked_receipt` limb 3
now asserts the masked-row coverage against the stated window, so a shrunk set refuses instead
of being silently disclosed as 30 days. That guard fires whichever way this ruling goes.

**The question this ruling answers is narrower:** whether the *cause* is fixed too, by
supplying the two families with target history from 1 December.

**Proposed solution, offered for the owner to accept, modify or reject.**

> **Read-only, history-only, no scoring, no metric.** The two persistence families may read
> target values dated **2022-12-01** *solely* as lookup history for a forecast origin inside
> the scored window, subject to all five of the following, every one of which is
> mechanically checkable:
>
> 1. **No 1 December row is ever scored.** The scored set stays D-28's 2–31 December. A row
>    whose `interval_start_utc` falls on 1 December may appear as a *source* value in a
>    lookup and must never appear as a row in any mask, metric, bootstrap block or table.
>    Enforced by the existing comparison-wide mask plus one new assertion that the scored
>    key set is disjoint from the embargo window.
> 2. **Only the two unfitted families.** M-01 and M-02 read it. No fitted model (Ridge, RF,
>    LSTM), no transform, no selection, no threshold and no hyperparameter touches it —
>    which is exactly the line `project.md` § Forbidden already draws ("NEVER let December
>    inform model selection, feature selection, thresholds or hyperparameters"). Reading a
>    single value as a naive lag is not informing a choice; it is applying a frozen rule.
> 3. **Access goes through the one door, logged.** The read happens through
>    `open_restricted` with an `AccessRecord` carrying `purpose = "persistence_history"`,
>    `performance_inspected = false`, `locked_test_accessed = true`, and the G-05
>    authorization of the occasion. It appears in `evidence/test_run_access_log.jsonl` and
>    the registry row exactly as every other December access does (Vision §8.3; §13.4).
> 4. **It is a G-05-gated act, not a pre-G-05 one.** Nothing reads 1 December before G-05 is
>    signed. This ruling does not widen the pre-G-05 coverage audit, which stays
>    performance-blind.
> 5. **Recorded as a D-number before the read.** With its own entry stating the scope above
>    verbatim, so the boundary is in the register rather than in a commit message.
>
> **Why this is defensible:** both lookups are at `t−1 h` and `t−24 h`, i.e. strictly before
> the forecast origin, so no future information enters — the same availability logic that
> governs every driver. **Why it still needs a ruling:** it is a read of the locked month
> outside the one-shot evaluation event, and "how much of December may be touched, and when"
> is a supervisor question by construction, not an implementation detail.
>
> **The alternative, if the owner prefers the tighter boundary:** leave the data as is and
> **amend D-28's disclosure from 30 days to the measured 29**, restating the scored set as
> 2–31 December *less the hours no baseline can forecast*. That is honest, needs no December
> read at all, and costs one day of scored data plus a correction sweep over every artifact
> asserting 30. It is a real option, not a straw man.

**Owner:** Supervisor. **Due:** before G-05.

**Decision required — Approve / Reject / Modify / Postpone.**

> ## ✅ RULED 2026-09-24 (Student), REVISED 2026-09-24 same day — option (b) approved
>
> **Superseded history, kept rather than deleted.** The Student first approved amending
> D-28's disclosure to 29 days (zero additional December contact). That amendment was
> drafted into `evidence/DECISIONS.md` D-28 the same day, then found to conflict with
> D-59 (Student+Supervisor countersigned, live in config, code-enforced at 30 days) and
> to have no working code path to actually produce 29 days without either a new
> December-specific mechanism or incorrectly widening the shared, Mandated 24-hour fold
> embargo. Full analysis: `governance/CHANGE_RECORD_2026-09-24_d28_29day_amendment.md`.
>
> **Final ruling, same day: option (b).** The 29-day amendment is **reverted** — D-28's
> `evidence/DECISIONS.md` entry is back to its original 30-day text, D-59 is untouched,
> `configs/experiment.yaml:376` is untouched. Instead, **this document's own Option A**
> (the bounded, logged 1-December lookup read, drafted above but never implemented) is
> now built: a narrowly-gated mechanism letting only M-01/M-02 read 1 December as
> lookup-only history, post-G-05, under its own new D-number, recovering the true 30-day
> scored set without amending anything else. Implementation, its 5 enforced conditions,
> and the drafted D-number are in `governance/CHANGE_RECORD_2026-09-24_d28_option_a_bounded_read.md`.
>
> **The 55-file "sweep to 29" was never performed and stays unperformed** — correctly,
> since the underlying figure never actually changed from 30. Only this document and
> `governance/REC_13_60_STATUS_2026-09-24.md` were touched, both now updated to reflect
> the final state (option A implemented, D-28/D-59 both stand as originally frozen).

---

## §3 — December-reading tests: the authorization occasion (Recommendation 32 and the deselected trio)

**Question.** Three test modules — `tests/test_release_hashes.py`,
`tests/test_acquisition_window.py`, `tests/test_phase_boundary.py` — read bytes under
`evidence/locked_test_restricted/`. They are deselected from the pre-commit hook and from
every suite run this session made (Recommendation 30's split criterion: *a module belongs to
the gate-only set when it reads bytes from under the restricted root*). They have therefore
**never been executed**, and their acceptance rows (TA-15, the acquisition-window control,
the phase-boundary control) rest on static reading alone.

**What is being asked for.** A recorded authorization occasion on which the three modules run
once, locally, under the governed 3.11 pin, with every access logged. Concretely:

> **Authorization for a locked-root test occasion.** On a named date, the Student runs
> `python -m pytest -q tests/test_release_hashes.py tests/test_acquisition_window.py
> tests/test_phase_boundary.py` with `purpose = "guard_verification"`,
> `performance_inspected = false`. The occasion reads December *target bytes* only through the
> modules' existing `open_restricted` routing, computes **no metric, no prediction and no
> comparison**, and inspects **no model performance**. Its access rows are appended to
> `evidence/test_run_access_log.jsonl` and disclosed in the run's evidence record and to the
> supervisor at the next gate. The junit result becomes the missing evidence for the three
> acceptance rows and completes the `aws_ai_dlc_preflight_report`'s "release hashes" limb,
> which currently renders **absent**.

**Why it needs a ruling rather than just happening.** Vision §8.3's authorization limb is
meant to be a decision, not a constant — that is precisely why Recommendation 30 took these
modules *out* of the commit hook. An agent may not grant the occasion to itself, and this
session did not: the three modules were not run.

**Note on sequencing.** This is independent of §2 and of G-05. It reads December bytes to
verify the *guards*, not to evaluate a model, so it is the same class as the required pre-G-05
coverage audit — performance-blind, recorded, and not the one-shot event.

**Owner:** Student, with the Supervisor informed (or Supervisor, if the owner reads Vision
§8.3 as reserving every December read). **Due:** before G-05, since the preflight report
cannot reach a green verdict without it.

**Decision required — Approve / Reject / Modify / Postpone.**

> ## ✅ RULED 2026-09-24 — approved by the owner, executed
>
> **Run, once, under the governed environment.** `conda activate tec-thesis-311` (Python
> 3.11.16 — the governed pin; confirmed by version check, not assumed) was located and used
> after `README.md`'s 2026-09-24 documentation commit (`b894284`) recorded it. The three
> named modules ran together with the rest of the Phase-1-reachable §18.3 critical set:
> ```
> pytest tests/test_prepared_target_schema.py tests/test_feature_availability.py
>   tests/test_iri_denial.py tests/test_split_embargo.py tests/test_train_only_transforms.py
>   tests/test_common_masks.py tests/test_checkpoint_restore.py tests/test_bootstrap.py
>   tests/test_release_hashes.py tests/test_acquisition_window.py tests/test_phase_boundary.py
>   tests/test_locked_test_guard.py --junitxml=artifacts/exec_evidence/run_2026-09-24/junit_final.xml
> ```
> **Result: 766 tests, 2 failures, 0 errors.** Both failures are the pre-existing,
> already-documented self-referential chokepoint-scanner false positives in
> `test_release_hashes.py` and `test_phase_boundary.py` (each module's own
> `Path(__file__).read_text()` flags itself; see the 2026-09-23 note on this document's own
> §7-equivalent). `test_acquisition_window.py`: clean. **`test_locked_test_guard.py`'s
> orphan-reconciliation test, previously failing, now PASSES** (66/66) — measured, not
> assumed; whatever closed it is not attributed here without further investigation, only the
> observed state recorded.
>
> **Purpose recorded is `coverage_audit`, not `guard_verification`.** Each of the three
> modules hardcodes its `AccessRecord.purpose` literal in its own source
> (`tests/test_release_hashes.py:110`, `tests/test_acquisition_window.py:98`,
> `tests/test_phase_boundary.py:125`). Introducing a new `"guard_verification"` value would
> mean editing the three gate-critical modules themselves — exactly the class of change this
> session's general rules say to flag rather than make unilaterally. The run proceeded under
> the existing, already-accepted `coverage_audit` purpose value instead of inventing a new
> one; `performance_inspected: false` is unchanged and correct either way.
>
> **Where the access rows landed.** Not `evidence/test_run_access_log.jsonl` — that file is
> explicitly reserved for real governed accesses (module comment, all three files) and is
> untouched (`git status` shows no change). The rows went to
> `artifacts/exec_evidence/test_access_log.jsonl`, the dedicated, gitignored sidecar the
> three modules route through (`ACCESS_LOG` constant, all three files) — this **is** Rec 1's
> "Option 2 — separate the logs" disposition already in effect, not a defect. The sidecar grew
> by 72 rows this run (1684 → 1756, measured before/after).
>
> **`aws_ai_dlc_preflight_report` updated**, from the junit evidence:
> `artifacts/preflight/aws_ai_dlc_preflight_report_20260923T214427Z.json`. The "release
> hashes" limb moved from **`absent`** (no run had ever produced evidence) to
> **`failed`** — 233 passed, 1 failed (the known chokepoint false positive) — which is
> honest, execution-backed evidence, not a green result. TE §18.3's own rule holds:
> "absent evidence is absent, never passed." Overall verdict stays `not_green`
> (`limbs_not_passed: ['critical_tests']`); the other three limbs (`zero_tbd`,
> `declared_sources`, `supervisor_signoff`) are unaffected and still `passed`.
>
> **Not swept:** the TA-15 / acquisition-window-control / phase-boundary-control rows as
> they appear inside dozens of per-unit AI-DLC artifacts (`functional-design`,
> `nfr-design`, `code-summary.md` files across at least four units). The authoritative
> evidence pointer is recorded here and in the fresh preflight report; a full textual sweep
> of every per-unit mention is outside this pass's scope and is flagged, not silently
> skipped, per `project.md`'s own sweep-completeness rule.
>
> **Disclosed to the Supervisor at the next gate**, as stated above. Independent of Layer‑2
> §2 and of G-05.

---

## §4 — What could not be done at all, and why (Recommendation 10 / dispositions §5 item 7)

The owner asked for the eighth CCMC reference value to be determined, stage 04 to be executed
and the paired comparison performed. **None of the three is performable from here**, and the
reason is recorded rather than worked around:

1. **The eighth value is a manual browser collection.** Seven of eight official IRI-2016
   reference values were collected by hand from the CCMC Instant Run form and are saved at
   `kaggle/official_reference_outputs/case_[1,2,3,4,6,7,8]_*.txt`. Case 5 was rejected because
   it was retrieved at the wrong hour — the saved file's own header reads `2022/-216/ 0.0UT`
   (1 August + 216 days = 4 August, **00:00 UT**) where the frozen selection specifies **BSHM
   2022-08-04T12:00Z**, a *day* case. The collection sheet
   (`kaggle/b01_official_reference_collection_sheet.md` §1) records that programmatic run
   requests were refused **HTTP 429** on 2026-09-19 and instructs, in its own words: *"collect
   the eight runs by hand in the browser, one at a time … do not script it and do not retry in
   a loop."* Scripting it now would defy that instruction and hammer a public NASA service.
   **What is needed from the Student:** one browser run of the CCMC form with the §2 settings
   exactly as the sheet specifies (IRI-2016; UT; 2022 / 08 / 04 / **12**; geographic
   32.778987 / 35.022987; height 300–300–10; `tecUpper` 2000; `tecLower` 90; output type 1;
   optionals ON; NeQuick topside; URSI-88 foF2), saved as
   `kaggle/official_reference_outputs/case_5_BSHM_20220804T12Z.txt`.
2. **The adapter side cannot run locally.** `iricore` is uninstallable in this Windows
   environment (the exhaustive wheel/toolchain diagnosis is in
   `governance/CHANGE_RECORD_2026-09-19_scientific_decisions_p2.md` §2), so no adapter value
   exists for any of the eight cases and `kaggle/b01_validation_samples.json` cannot be
   assembled. The adapter runs only in the Kaggle 3.10 environment D-49 covers.
3. **`04 --generate-benchmark` refuses by design** until a passing pre-declared validation
   report exists (R-59 limb 1, `src/external/iri.py`). The refusal is correct and is the
   deliverable; there is no compliant shortcut, as Recommendation 10 itself states ("Only (1)
   is valid").

**Therefore the ordering is:** the Student collects case 5 → the Kaggle 3.10 session computes
the eight adapter values and assembles `b01_validation_samples.json` → `04
--build-validation-report` emits the R-59 report → only then can `--generate-benchmark` run
and G-04 be approached. The open risk Recommendation 10 recorded carries forward unchanged:
`B01_TOLERANCE_PROPOSAL_2026-09-19.md:50` measures a CCMC quadrature offset scaling to
≈ −1.3 TECU at 50 TECU, beyond D-50's frozen 1.0 TECU tolerance, so whether the eight cases
*pass* is not predictable from the evidence on disk. **Nothing here pre-judges that.**

---

## §5 — Standing items this document does not reopen

* `budget_value`'s combination rule (dispositions §4.5, Recommendation 20) — the **structural**
  half landed 2026-09-21 (the producer now emits the consumer's shape; the real artifact passes
  `_assert_budget`), and the rule itself stays a `TBD — freeze gate` block at
  `configs/data.yaml: target.uncertainty_budget` with the closed option sets written beside it.
  A Student + Supervisor freeze under its own D-number is what fills it.
* The locked root's presence in git and its exposure to GitHub Actions (escalation 1 of the
  board's remediation manifest) — unchanged and still owed a Student + Supervisor ruling.
* D-63's, D-64's and D-65's supervisor limbs, where the register records them as open.

**STOP.** No document is updated and no finding applied beyond what the owner rules on each
item above.
