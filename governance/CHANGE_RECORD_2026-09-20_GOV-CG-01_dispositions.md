# Change record — owner dispositions on governance report GOV-2026-09-20-CG-01

**Record ID:** `CR-2026-09-20-GOV-CG-01-DISPOSITIONS`
**Filed:** 2026-09-20
**Governance report:** `governance/reviews/GOV-2026-09-20-CG-01.md`
**Reviewed stage:** AI-DLC 3.5 `code-generation`, all twelve Construction units
**Gate verdict being dispositioned:** `FAIL`
**Decision:** proposed D-numbers are drafted in §4 below for the owner to adopt. **Nothing in this record has been written into `evidence/DECISIONS.md`.**

---

## Vision §15.2's six fields

| # | Field | Content |
|---|---|---|
| 1 | **What changed** | The project decision owner ruled on all twelve Critical findings of `GOV-2026-09-20-CG-01` and authorised the board's preferred option on the remaining forty-eight (28 High, 15 Medium, 5 Low). Two rulings **change a scientific definition** and are therefore recorded here as proposed decisions awaiting D-numbers, not as applied facts: the M-03 climatology key, and the refit epoch-count rule. Remediation of the agent-doable findings was executed in the same session and is itemised in §3. |
| 2 | **Why** | Stage 3.5 closed on 2026-09-13 with a standing reviewer `NOT-READY` on `external-products`, and had never received a TEC governance review. The first such review returned `FAIL` on four independent grounds: an unsound approval record, three stages advanced past a standing governance `FAIL`, two defects that would corrupt the one-shot G-06 event, and a December access log that reconciles to zero experiment-registry rows. The owner elected to resolve rather than defer. |
| 3 | **Superseded text, quoted** | `construction/fixtures-and-reproducibility/code-generation/code-summary.md:15-17`: *"**WS-20 and TA-17 are UNREACHABLE — not merely `Pending`**"*, and `:57`: *"**The owner ruled on 2026-09-13: record it, rule on the remedy later. No code has moved.**"* Both are superseded by commit `8d4297d` under `CR-2026-09-13-04-FIXTURE-WINDOW`, applied 2026-09-13, seven days before this record. Also superseded: `src/models/lstm.py:123-128`'s refusal text *"the TensorFlow pin is TBD — freeze gate (TS-M-01)"*, against `requirements.txt` line 5 `tensorflow==2.21.0` frozen under D-36. Also superseded: the D-49 register row at `evidence/DECISIONS.md:3056`, *"scope excludes training, **fixtures**, every other stage"*, against the extension recorded in `CR-2026-09-20-B01-PREREQS` §1.2 — **the owner has ruled that the register row stands and the extension is withdrawn**; see §2 item 9. |
| 4 | **Authority** | The project decision owner, in session, 2026-09-20, under the recorded student/supervisor authority equivalence (`evidence/DECISIONS.md` D-1 addendum). **No independent supervisor signature artifact exists for any ruling in this record and none is claimed.** Four items below are marked as requiring supervisor countersignature before the gate they serve; they are not treated as signed. |
| 5 | **Evidence** | The owner's express rulings, recorded verbatim in §2. The board's findings, each with its printed derivation, in `governance/reviews/GOV-2026-09-20-CG-01.md`. ⚠ **No test was executed in producing either the review or the remediation** — no usable Python interpreter exists on this clone (`python.exe` resolves to a zero-byte Windows Store alias stub). Every claim about code behaviour in both documents is **static**, read from source, and none should be read as "verified passing". |
| 6 | **Consequences** | The stage-3.5 gate verdict remains `FAIL` until the closure evidence in §3 is produced and a fresh reviewer verdict for `external-products` post-dates its own human approval turn. Four items are preconditions of G-05 that only the student or supervisor can discharge (§5). The `nfr-design` consolidated report is declared **permanently lost** and its Recommendations 10–13 **void** rather than pending — see §2 item 4. G-06 remains blocked; the locked December set has **not** been opened. |

---

## 1. Scope of this record

This record disposes of `GOV-2026-09-20-CG-01`. It does **not** accept the TEC gate — the board's verdict is a recommendation and the gate is accepted by the human after reading the report. It does not authorise locked-test access. It does not grant academic approval.

---

## 2. The owner's rulings, as given

| Rec | Ruling |
|---|---|
| 1 | **Option 2** — separate the test-mode access log from the evidence access log. Archive the current file as superseded; never rewrite a row. |
| 2 | **Option 2, with the key specified by the owner.** Quoted: *"Redefine M-03 as the mean VTEC by **station and hour**, calculated exclusively from each partition's training data. Remove month from the key, document the seasonal limitation, and fail early if a required key is missing. Record the definition before G-05 and verify it without accessing the locked test."* |
| 3 | **Option 1** — re-open stage 3.5 for `external-products` alone; one reviewer dispatch; a human turn that post-dates the resulting verdict. |
| 4 | **Option 1** — the 2026-09-20 board discharges the owed 3.1 re-run; the lost `nfr-design` Recommendations 10–13 are declared **void**, not pending. |
| 5 | **Option 2 with option 1's guard.** Quoted: *"Determine the final epoch count from the median best-validation epoch across the predefined pre-December folds and seeds, rounding half upward. Freeze this rule and its resulting value before G-05. Retrain from scratch on January–November, save and hash the models, and make December strictly inference-only. Verify the complete path using synthetic data; December must never influence training or model selection."* |
| 6 | **Option 2** — a guarded `scripts/05 --partition DEC` branch behind the G-05 signature produces the score bundle; `scripts/06`'s locked branch loads persisted REFIT weights and predicts only. |
| 7 | **Option 1** — produce `aws_ai_dlc_preflight_report` now from the existing `assert_no_tbd` machinery; annotate D-31 with the date it was finally produced. |
| 8 | **Option 1** — run the provider-version census before G-05; record it as a D-number; obtain or record the absence of the provider's version statement; wire `assert_unmixed_sources`. |
| 9 | **Option 1** — restore D-49's original exclusion. The Python 3.10 environment is for the isolated B-01 benchmark **only**; both walking-skeleton fixtures run under the governed 3.11 pin. |
| 10 | **Option 1** — complete the eight-case R-59 validation: re-collect case 5 at the correct hour, assemble `b01_validation_samples.json`, run the stage-04 paired comparison, emit the report. |
| 11 | **Option 1** — correct the CRITICAL banner in the artifact **body**, preserving the residual limitation. |
| 12 | **Option 1** — write `tests/test_feature_leakage_guards.py` with four negative controls, one per TA row. |
| 13–60 | The board's preferred option in each block, authorised without individual variation. |

---

## 3. Remediation executed in this session

Executed by agent, read-only of every protected surface, under the prohibitions in §6. **No test was run. No git command was run. No row of any access log or registry was modified or deleted. Nothing was written to `evidence/DECISIONS.md` or to any `PreFlight/` document.**

An itemised file-by-file manifest of what changed, with the closure evidence owed for each finding, is maintained in `governance/reviews/GOV-2026-09-20-CG-01.md` § Remediation manifest.

---

## 4. Proposed D-number text — **for the owner to adopt; not written**

These are drafts. A decision is not real until the student gives it a D-number in `evidence/DECISIONS.md`. Two of the four additionally require supervisor countersignature because they fix a §18.2 forbidden-choice value.

### 4.1 Proposed — M-03 climatology key definition *(requires supervisor countersignature)*

> **Decision.** The M-03 fitted climatology is defined as the mean VTEC keyed on **(station, hour)**, estimated exclusively from the training partition of each fold. The calendar-month term is removed from the key.
>
> **Why.** The prior definition, station × month × hour, is unsatisfiable on a single study year under a strictly expanding-window split: the scored month always falls after the training range, so no key exists for any scored partition. Derived over the six partition blocks of `configs/data.yaml:178-208` — F1 validation month 4 ∉ {1,2,3}; F2 7 ∉ {1..6}; F3 10 ∉ {1..9}; F4 11 ∉ {1..10}; DEC 12 ∉ {1..11} — five of five scored partitions produce no prediction, which empties the comparison-wide intersection mask and prevents the primary results table being produced at all.
>
> **Limitation, mandatory wherever M-03 is reported.** A station × hour climatology carries **no seasonal term**. It is therefore a weaker difficulty control than a station × month × hour climatology would be, and no interpretation of M-03's performance may imply that it adjusts for season. This limitation is stated at every surface where M-03 appears beside the LSTM–IRI comparison.
>
> **Rejected alternatives, and why.** Widening the fit basis across multiple years breaches D-8's frozen claim boundary (calendar year 2022). Fitting on or including the scored month breaches R-98, NFR-LEAK-01 and Vision §8.4's own sentence that M-03 "is never fitted using validation or December data". Neither is admissible.
>
> **Enforcement.** The key lives in `configs/experiment.yaml`, never in source (TC-03e). `fit_climatology` raises at fit time when the training range cannot produce a key the scored partition will demand, naming the missing key. Verified on synthetic data; no locked-test access is required or permitted to verify it.

### 4.2 Proposed — refit epoch-count rule *(requires supervisor countersignature)*

> **Decision.** The final January–November refit epoch count for M-06 is the **median of the best-validation epochs observed across the pre-December folds F1–F4 and the final seeds 1337, 2024 and 7, rounding half upward**. The rule is frozen now; the resulting value is frozen before G-05, once the folds have run.
>
> **Why.** The refit partition is scored nowhere (`validation_month: null`), so it has no validation month of its own. Absent this rule, the implementation fell through to using the DEC score bundle's December labels for early stopping and best-checkpoint restoration — December selecting a hyperparameter of the confirmatory model, in breach of Vision §8.3, whose trigger is December being **seen**, not the lock being opened.
>
> **Consequences.** Phase 1 retrains from newly initialised weights on January–November; the fitted model is persisted and SHA-256 hashed; December is **strictly inference-only** and no `model.fit` is reachable on the locked path. The epoch count is a protected hash at the phase transition (TE §7.0B), so it must be frozen before G-05 and must not change afterwards.
>
> **Verification.** The complete locked path is exercised end to end on **synthetic** December data only.

### 4.3 Proposed — provider product-version census *(student freeze; supervisor acceptance of the limitation)*

> **Decision.** The Phase 1 prepared-VTEC evidence is recorded as drawing on more than one Madrigal product-processing version. The measured per-month and per-day distribution is `<INSERT FROM CENSUS RUN — do not transcribe from this draft>`.
>
> **Observed before the census.** Five of eleven non-December months carry a g.001/g.002 mix — 2022-04 (613 / 18,377), -06 (580 / 17,614), -07 (1,712 / 17,020), -08 (610 / 18,517), -11 (1,896 / 16,287) — and the FULL merge additionally carries 743 g.003 records, **all dated 2022-12-31**, inside the locked test month. The mix appears in no configuration, no manifest, no prior decision and no change record; `grep "g.001"` over every Markdown file in the workspace returned zero matches.
>
> **What must be settled.** Whether g.001, g.002 and g.003 differ in bin construction, quality filtering or fill handling for instrument 8000 kindat 3500. If they do, the December locked test is not drawn from the same product as the training folds, and the paired loss differential would measure product drift alongside model skill.
>
> **Disposition.** Either (a) the provider certifies the versions physically equivalent for this product, and that certification is recorded here; or (b) the mix is declared a limitation bounding every claim, stated wherever a coverage figure or a comparison result is reported. Option (b) is the standing default until (a) is obtained.

### 4.4 Proposed — `window_length_hours` transcription *(student freeze; supervisor countersignature)*

> **Decision.** `experiment.window_length_hours` is transcribed as **24**, together with the `feature_dictionary` lag rows `[1, 2, 3, 24]`, so that `read_window_length`'s cross-check against `sequence_steps` is satisfied by two agreeing frozen values rather than one.
>
> **Why this is a transcription, not a choice.** Vision §8.1 states the 24-hour primary history is not a tuned hyperparameter. The value was nonetheless absent from every governed config — not a `TBD — freeze gate` sentinel but no key at all, so `assert_no_tbd` could not name it and the §18.3 preflight could report zero unresolved fields while the primary history window was undefined. The sentinel has been declared as an interim so the gap is visible; this decision resolves it.

### 4.5 Proposed — `budget_value` combination rule *(§18.2 forbidden-choice; supervisor countersignature required)*

> **Open.** How the Phase 1-applicable target-uncertainty contents combine into a single scalar `budget_value` is not fixed by any governing document. Until it is, `practical_relevance_statement` refuses with a message naming the missing rule and its owner, so Vision §5.3's second conjunct — that a practical-relevance reference must not be smaller than the target uncertainty budget — fails visibly rather than silently never running. **No implementer may supply this value.**

---

## 5. Gated owner acts — nothing below was performed

| # | Act | Who | Due |
|---|---|---|---|
| 1 | Adopt the four proposed D-numbers in §4.1–§4.4 in `evidence/DECISIONS.md` | Student | before G-05 |
| 2 | Obtain supervisor countersignature for §4.1, §4.2, §4.4 and, when it exists, §4.5 | Supervisor | before G-05 |
| 3 | Re-run the reviewer on `external-products` and take the gate turn **after** the verdict exists (Rec 3) | Student | before `build-and-test` closes |
| 4 | Enable the pre-commit hook: `git config core.hooksPath .githooks` — **after** the restricted-case deselection lands, or every commit performs December access | Student | immediately |
| 5 | Commit the working tree, including the 110-line uncommitted correction to `CHANGE_RECORD_2026-09-13_00_01_02_fixture_window.md`, citing D-numbers in the message (Rec 54, Rec 36) | Student | immediately |
| 6 | Run the provider-version census and fill §4.3's placeholder from the run (Rec 8) | Student | before G-05 |
| 7 | Collect the eighth CCMC reference value, re-collecting case 5 at the correct hour, and run the stage-04 paired comparison (Rec 10) | Student | before G-04 |
| 8 | Run both fixtures under the governed **Python 3.11** pin and populate the measured fields of the two `fixture_manifest.yaml` files from the run (Rec 9, Rec 37) | Student | before G-07 |
| 9 | Withdraw the Python 3.10 fixture extension recorded in `CR-2026-09-20-B01-PREREQS` §1.2, restoring D-49's original scope; the D-49 register row at `evidence/DECISIONS.md:3056` is correct as written and stands | Student | before any fixture freeze act |
| 10 | Run the in-Kaggle session discharging W-6 step 8's durability measurement and TC-03g's in-session gate (Rec 28, Rec 57) | Student | before G-05 |
| 11 | Produce `aws_ai_dlc_preflight_report` and annotate D-31 with its production date (Rec 7) | Student + Supervisor | before G-05 |
| 12 | Rule on the historical DATA-16 identity breach in git history — the working-tree literal is removed; history is unrewritable without breaking audit-trail immutability (Rec 39) | Student + Supervisor | G-09 |
| 13 | Rule on whether the two persistence baselines may read 1 December history for a 2 December forecast origin (Rec 15) | Supervisor | before G-05 |
| 14 | Rule on whether the top-1%-error-removed sensitivity is taken comparison-wide or per station; equal-station weighting makes this material (Rec 21) | Supervisor | before G-06 |
| 15 | Fix the `matplotlib` pin version, if no repository evidence determines it (Rec 38) | Student | before G-07 |

---

## 6. Prohibitions observed during remediation

Recorded so a later reader can check what was and was not touched.

- `evidence/DECISIONS.md` — **not written**. Four decisions drafted in §4 instead.
- `PreFlight/vision_document(3)(2)(2).md`, `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **not edited**.
- `evidence/test_run_access_log.jsonl` — **no row modified, rewritten, truncated or deleted**. Superseded by notice; the file stands.
- `artifacts/registry/experiment_registry.jsonl` — **no row modified**. No registry row back-filled; `reconcile_access_records` forbids it and must keep forbidding it.
- `evidence/locked_test_restricted/` — **no file content read**. File names, sizes and paths only. No December 2022 target value was read by any seat or any remediation worker.
- Human-signed records — **not edited to match a later derivation**. Where a signed record conflicts with a derived value, the correction is recorded in the artifacts the board owns and routed as a ruling.
- `git` — **no commit, add, amend, rebase, or config change**.
- Test execution — **none**. No interpreter is available; and executing the suite appends to a custody artifact.
- Scientific values — **none invented**. Where a value is owed, the literal `TBD — freeze gate` sentinel was written and reported.

---

**STOP.** The gate verdict stands at `FAIL` pending the closure evidence in `governance/reviews/GOV-2026-09-20-CG-01.md` and the fifteen gated acts in §5. This record does not accept the TEC gate, does not grant academic approval, and does not authorise locked-test access.
