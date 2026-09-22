# Change record — 2026-09-21 — `GOV-2026-09-20-CG-01` closure pass

**Change ID:** `CR-2026-09-21-GOV-CG01-CLOSURE`
**Authority:** the project decision owner's instruction of 2026-09-21, itemised, in session.
**Baseline:** `HEAD = de1732f` throughout; every diff figure below is `git diff --numstat` or
`grep -c` against that commit, run and printed before assertion.
**Register discipline:** three decisions (D-63, D-64, D-65) were written to
`evidence/DECISIONS.md` on the owner's explicit instruction to complete the configs and pin
the coordinates; each states its own countersignature status honestly and none is claimed as
supervisor-signed beyond what the owner reported. Per the owner's standing rule of
2026-09-21, *the student's report of the supervisor's countersignature is the evidence*; no
separately signed artifact is claimed to exist anywhere.
**Gate status:** the `GOV-2026-09-20-CG-01` verdict is **`FAIL`** and this record does not
change it. Closure remains the owner's and the board's.

---

## 1. `configs/features.yaml: permitted_producers` — the seven driver rows (D-63)

`src/external/spaceweather.py` **+22 / −0**: `DRIVER_PRODUCERS`, the producing-artifact
identity per driver-class TE §6.2 row, each a transcription of the product a prior decision
already selected (D-39, D-40, D-21/D-22/D-23/D-25, D-10.1). `configs/features.yaml` now
carries **18 of 18** rows. `tests/test_feature_availability.py` **+49 / −35**: the
exact-rows test expects the union and asserts config = constant = literal in three
independent statements; the "still fails closed on every deferred driver row" control is
replaced by one pinning a single producer per row, refusing the definitive-grade and V3.0
identities by name, and asserting `dst` stays `DIAGNOSTIC_ONLY_SERIES`.

**Executed:** stage 05's refusal moved from `permitted_producers: incomplete: no
permitted-producer entry for dictionary row(s) ['ap60_safe', 'ap_safe', 'dst',
'f107_81_trailing', 'f107_safe', 'hp60_safe', 'kp_safe']` to a different, earlier stop that
belongs to another unit. *(Corrected in this body 2026-09-22 rather than only in the
addendum: the first draft of this paragraph named `_load_release_inputs` as the new stop.
Measured on the fixture run recorded in the addendum, the actual new stop is the missing
apparatus-partition declaration in `tests/fixtures/plumbing_7day/identity_declaration.yaml`
(R-137), which precedes the loader. The claim that the permitted-producer list is no longer
the blocker is unchanged and correct; the name of what replaced it was wrong.)*

## 2. The provider-version census, RUN (D-64; Recommendations 8 and 22)

`src/data/inventory.py: provider_suffix_census` run read-only over the eleven non-December
months. Measured: 208,387 records; `g.001` 5,411 in **nine whole provider files** —
2022-04-21, 06-16, 07-13, 07-14, 07-18, 08-15, 11-13, 11-28, 11-29; `g.002` 202,976; **zero
days carry more than one token**; zero unrecognised tokens. Figures agree exactly with the
board's own per-month counts. Two facts the census adds: the mix is a whole-day reissue
pattern, not a mid-day switch; and D-11's plumbing window (2022-11-01..07) contains no
`g.001` day, so the plumbing fixture's input is single-version by measurement. December was
**not read** (restricted root); the board's 743 `g.003` records dated 2022-12-31 stand as
recorded. Filed at `evidence/provider_version_census_2026-09-21/` and
`artifacts/exec_evidence/run_2026-09-21/provider_version_census_raw.json`.

`configs/data.yaml: declared_sources` went from the literal `[]` to **eleven** hash-declared
entries, each carrying the nine TE §5.1 fields' inputs plus `release_status_versions` from
the census. Stage 01 re-measures on every run and refuses a mix the declaration does not
cover (`assert_sources_unmixed_or_recorded` — R-52 prohibition 2's first production call
site). **Executed:** `01_inventory_and_registry.py --config configs/ --phase 1
--fixture-manifest tests/fixtures/plumbing_7day/identity_declaration.yaml` completed,
`entries_written: 11`, and `artifacts/inventory/source_inventory.json` now carries eleven
entries that pass `assert_source_entry` — where it previously wrote a literal empty list, the
reason `assert_source_entry` and `assert_verbatim_notice` had never fired (Recommendation 26).
Two completeness shortfalls stay machine-readable and non-fatal: the one uninventoried month
(December, DATA-07 re-acquisition) and the untranscribed Madrigal acknowledgment notice
(FR-P1-01-6, the owner's transcription).

The `<INSERT FROM CENSUS RUN>` placeholder in
`CR-2026-09-20-GOV-CG-01-DISPOSITIONS` §4.3 is filled from the run, as that draft required.

## 3. Geomagnetic coordinates in the Station contract (D-65; Recommendation 13, option 1)

`src/data/registry.py`: `geomagnetic_lat` / `geomagnetic_lon` added to `SECTION_6_2_FIELDS`,
to the `Station` dataclass, to `load_registry` (absent or sentinel loads as `None`, never
defaulted; a non-numeric value is refused at load) and to `assert_registry_resolved`, where
an unresolved pair is refused **by name in both phases** — the Vision §6.2 freeze-gate column
that previously had no representation at all and let the gate return clean. Values frozen at
epoch 2022.5 from the NOAA NCEI IGRF-13 coefficient file (sha256 `460b8d8b…`, filed at
`evidence/igrf13_coefficients_2026-09-21/` with the full derivation and a Boulder control):
ARUC 35.642 / 123.046, BSHM 29.544 / 112.963, NICO 32.110 / 111.913. Four negative controls
in `tests/test_station_registry.py` prove an absent, a `TBD`, a non-numeric and a
provenance-less value are each refused by name.

## 4. `aws_ai_dlc_preflight_report` now exists (Recommendation 7; dispositions §5 item 11)

New: `src/data/preflight_report.py` and `scripts/gate_preflight_report.py`, implementing
`foundation`'s W-3 / R-02 design without amending it. Four limbs: **zero `TBD`** over every
`REQUIRED_FIELDS_MAP` entry of the phase, **declared sources** resolving, the **ten TE §18.3
critical tests** read from a junit XML an actual pytest run wrote, and the **supervisor
sign-off** read from a record the student authors. R-02's bar is implemented literally — a
limb with no collected evidence renders `absent`, never `passed`, and the verdict is `green`
only when all four are `passed`. `tests/test_preflight_report.py` carries R-02's five
withheld-limb controls plus the live case: `tests/test_release_hashes.py` is deselected from
every ordinary run (Recommendation 30), so the "release hashes" test renders **absent**, and
the report says so rather than counting it passed. The two Phase-2-only modules
(`test_dcb_sign.py`, `test_hourly_target.py`) render **deferred**, not failed (NFR-PHASE-01).

`governance/G09_SUPERVISOR_SIGNOFF_RECORD.yaml` transcribes precondition 3's six items, each
pointing at the register row that records it and stating the basis — the student's report of
the supervisor's countersignature, or the recorded authority equivalence D-31 itself relied
on. No signature is forged and no separately signed document is claimed.

**What this does not do:** it does not sign G-09. D-31 signed that gate on 2026-08-28 with
its preconditions recorded as unmet; this artifact is the evidence D-31 said did not exist,
and it now exists and reports its own state truthfully.

## 5. Recommendation 20, producer half

`src/data/prepared.py`: `build_uncertainty_budget` reshaped to the consumer's contract —
`artifact_id`, `units`, `phase1_contents` (per content: the statement **and** its measured
TECU scalars), `phase2_quantities` (mapping, every value the literal `recorded
not-applicable`), `budget_value`, `budget_value_rule` — emitted **beside** the R-72 fields
`assert_budget_complete` checks, so one artifact satisfies both sides and no adapter exists.
`budget_value` is computed only under a frozen rule read from `configs/data.yaml:
target.uncertainty_budget` (`resolve_budget_rule`; closed sets `statistic ∈ {median, p95,
max}`, `combination ∈ {sum, quadrature, max}`, a cited D-number required). The block is
written as three `TBD — freeze gate` sentinels: **the rule itself is the §18.2
forbidden-choice item and no implementer fills it.** While it is unset the budget carries
`budget_value: null` naming the owed decision and its owner, and
`practical_relevance_statement` refuses — Vision §5.3's second conjunct fails visibly rather
than silently never running. Closure evidence the finding asked for:
`tests/test_prepared_target_schema.py::test_real_budget_passes_the_consumer_contract` passes
the **real** producer output through the consumer's `_assert_budget`; four parametrised
controls recompute `budget_value` from the same rows by an independent path; three controls
refuse an out-of-set statistic, combination and decision by name.

## 6. Pins (Recommendation 38 and escalation 5)

`requirements.txt`: `matplotlib==3.9.0` and `pyarrow==16.1.0`. No repository evidence
determined either version — the 2026-09-20 derivation printed zero matches anywhere — so the
owner's instruction of 2026-09-21 fixed both under **one stated criterion applied
identically**: the newest release on or before the pin set's own freeze date, taken as the
release date of its newest non-TensorFlow pin (`ruff 0.4.8`, 2024-06-05). Release dates read
from PyPI on 2026-09-21 and recorded in the file: matplotlib 3.8.4 = 2024-04-04, **3.9.0 =
2024-05-15**, 3.9.1 = 2024-07-04 (after); pyarrow 16.0.0 = 2024-04-20, **16.1.0 =
2024-05-14**, 17.0.0 = 2024-07-16 (after). Both installed into the governed environment
(`tec-thesis-311`, CPython 3.11.16) beside numpy 1.26.4 / pandas 2.1.4 and exercised before
the pins were written. `plots.py:249`'s refusal message, which named `requirements.txt` as
the pin surface, is now accurate.

## 7. The pre-commit hook is enabled (Recommendation 35; §5 item 4)

`git config core.hooksPath .githooks`, run on the owner's instruction, **after** its stated
precondition: Recommendation 30's restricted-case deselection landed 2026-09-20, so enabling
the hook does not make a commit perform a December read. `gitleaks` **8.18.4** — the version
the hook pins and refuses any other — was installed to `~/bin`. The hook's header records the
activation date, the two environment facts, and that the first commit it gated is the commit
carrying that header.

## 8. `external-products` re-reviewed (Recommendation 3)

The unit's terminal verdict was `NOT-READY` (2026-09-13, iteration 2) on one ground: a
five-link chain proving `04` could never complete inside the fixture ladder. That Critical was
remedied the same day under `CR-2026-09-13-04-FIXTURE-WINDOW` (owner ruling "APPROVE OPTION
(A)"), committed in `8d4297d` — and the unit's record never said so. A dated amendment now
states it, re-traced link by link against the current code, with every count and diff figure
re-derived. A fresh reviewer dispatch (`aidlc-architecture-reviewer-agent`, dispatch record
written and deleted per the 12a protocol, one unit in scope) re-verified the chain
independently, re-derived every figure, ran the unit's two test modules in the governed
environment, and returned **READY** on 2026-09-21. Its one surviving Major — the unit's
`code-generation-plan.md` still carrying the stale "record it, rule later … no code moves on
it" account — is closed by a dated pointer appended to that plan.

**The gate turn is the human's and must post-date this verdict.** Nothing here takes it.

## 9. `team.md` correction through the §13 ritual (escalation 6)

`team.md` § Way of Working asserts the `.gitignore` credential deny-list is absent and a
precondition of the first commit. Measured false: the deny-list exists at `HEAD`, lines
63–81, carrying every entry the practice reported missing. Corrected under `##
Corrections` by `bun .claude/tools/aidlc-learnings.ts persist` — the only sanctioned write
path into a memory file — which emitted its `RULE_LEARNED` audit event (`rule_learned: 1`).
The superseded text is left standing, because that path appends and never replaces.

---

## Execution evidence

Governed environment throughout: conda `tec-thesis-311`, CPython **3.11.16**,
`CUDA_VISIBLE_DEVICES=""`, `PYTHONHASHSEED=0`, code commit `de1732f`. The full eligible suite
was run after every change; the three December-reading modules
(`test_release_hashes.py`, `test_acquisition_window.py`, `test_phase_boundary.py`) were
**not run** on any occasion, on Recommendation 30's criterion. Junit and console logs at
`artifacts/exec_evidence/run_2026-09-21/`.

One class of failure was **found by execution, not by review**: the eleven new
`declared_sources` entries made `assert_declared_sources_exist` refuse inside
`tests/test_external_drivers.py`'s temporary smoke workspaces (twelve controls failed at
their "governed refusal" assertion, all naming absent declared sources rather than the
refusal each control exists to observe). `_mirror_declared_sources` now hard-links the real
bytes into the smoke workspace; nothing is fabricated, and a genuinely absent path stays
absent and is named exactly as in production. A second, smaller one: the new
`preflight_report.py` module's docstring contained the restricted-root path as a literal,
which `tests/test_locked_test_guard.py`'s R-28 one-door control caught immediately —
rephrased, not exempted.

## Prohibitions observed

No December 2022 target value was read; no file content under
`evidence/locked_test_restricted/` was read (names and counts only); the three restricted
test modules were not run. `evidence/test_run_access_log.jsonl` is unmodified. No registry
row was modified, deleted or re-run — rows appended are real runs with their own status and
reason. No scientific value was invented: every `TBD — freeze gate` sentinel that was filled
was filled from a decision that already existed, and the ones that remain
(`target.uncertainty_budget`, `models.selected`, `models.refit.epochs`, the ablation
registration stamps, `practical_relevance_threshold`) were left standing. No human-signed
record was edited to match a later derivation. No `PreFlight/` document was edited. No
history was rewritten and no tag was moved.

---

## Addendum — 2026-09-22, measured after the closure commit `cda8869`

A measuring fixture run (`run_walking_skeleton.py --config configs/ --fixture plumbing_7day
--emit-candidate --identity tests/fixtures/plumbing_7day/identity_declaration.yaml`) was
executed under the governed pin to establish where the ladder now stops. Registry rows, all
appended and attributable:

| Stage | Outcome |
|---|---|
| `acquisition` (00) | **completed** |
| `inventory-and-registry` (01) | **completed** |
| `target-standardization` (02) | **completed** |
| `external-products` (04) | **completed** |
| `features-and-splits` (05) | aborted — `tests/fixtures/plumbing_7day/identity_declaration.yaml`: *"no apparatus partition declaration; stages 05-07 run a fixture at fixture scale over the manifest's declared apparatus partitions, never over a frozen id (R-137)"* |

**Two facts this establishes.** First, **stage 04 completed inside the fixture ladder** —
the execution evidence the 2026-09-21 reviewer recorded as owed for the 2026-09-13 Critical.
The step that could never complete now does; the remedy is confirmed by running it, not only
by reading it. Second, the ladder's current stop is an **owner-authored declaration field**,
not code: the fixture identity declaration carries no apparatus-partition block, which R-137
requires before stages 05–07 can run at fixture scale. That is a Q-31 fixture-declaration act
(Student), and no agent supplies it — the log is at
`artifacts/exec_evidence/run_2026-09-21/measuring_run_after_d63.log`.

Consequently the two `fixture_manifest.yaml` files still carry only `TBD — freeze gate`
sentinels and **no measured field is populated**: dispositions §5 item 8 (populate the
measured fields from a fixture run) remains open, now blocked on the apparatus-partition
declaration rather than on the deadlock `CR-2026-09-20-FIXTURE-CANDIDATE-PATH` removed or on
the permitted-producer list D-63 closed.

---

## Addendum 2 — 2026-09-22/23, the owner's three follow-up items

### A. Apparatus partitions for `plumbing_7day` (owner: Option A)

Written into `tests/fixtures/plumbing_7day/identity_declaration.yaml`, mirroring
`scientific_1month`'s own precedent (two expanding folds) and adding the one refit the
project's fixtures otherwise never exercise:

| id | kind | train | validation_month | scored, after the 24 h embargo |
|---|---|---|---|---|
| `FIX-NOV-FOLD-01` | fold | 2022-11-01..03 | 2022-11-04 | 11-05..07 (72 h) |
| `FIX-NOV-FOLD-02` | fold | 2022-11-01..05 | 2022-11-06 | 11-07 (24 h) |
| `FIX-NOV-REFIT` | refit | 2022-11-01..07 | null | scored nowhere (FR-P1-04-14) |

Every id is outside the six frozen ids (R-137 control 15); no partition is `locked`; both
training ranges lie inside D-11's cited window; at most one refit. **No D-number:** the
scientific fixture's apparatus block carries none either, and these are apparatus constants
(R-122), not scientific values — the window and station they sit inside are D-11's and
D-20's and are unchanged.

**Disclosed, not hidden:** fold-01's scored range overlaps fold-02's, because
`validation_month_range` runs to end-of-month while the fixture is seven days. Fixture 2 has
the identical overlap. The plumbing fixture is TC-03f smoke and never scientific evidence, so
this changes nothing it is used for.

**Executed.** The measuring run accepted the block and advanced: stage 05 no longer refuses
at the apparatus declaration. It now stops one step further on, at
`artifacts/releases/phase1_hourly_target/release_manifest.json` — **no released Phase 1
hourly target exists**. Stage 02 writes its target to `artifacts/prepared_target/` and does
not publish it as a release, so the 02→05 boundary has the same missing-producer shape D-61
closed at the 00→01/02 boundary. **Option B (drop the refit) and Option C (single fold) were
therefore never needed and were not tried** — the refit is not what stopped the run.

**Open, and it is an owner decision, not an oversight:** whether D-61's ruling ("the stage
publishes the release the downstream stages consume", option A) extends to stage 02
publishing `phase1_hourly_target`, or whether that wants its own D-number. Until it is
ruled, the ladder cannot reach the measured fixture fields, so dispositions §5 item 8 stays
open — now blocked on this, not on the apparatus declaration.

### B. B-01 case 5 collected; the samples file is complete

`kaggle/official_reference_outputs/case_5_BSHM_20220804T12Z.txt` was collected by the
Student on 2026-09-22 at the corrected hour. Verified by the **server-echoed header**, never
by the filename: `2022/ -216/12.0UT  geog Lat/Long/Alt= 32.8/  35.0/ 300.0` — day-of-year
216 = 4 August, 12 UT, BSHM. `parse_official_outputs.py` matched **8/8** cases by header and
wrote `kaggle/b01_validation_samples.json`: ARUC 12.1 / 4.0 / 4.6, BSHM 33.1 / 29.2, NICO
8.5 / 4.1 / 21.7 TECU, each with its `t/%` and hmF2 diagnostic. The rejected wrong-hour file
is retained as evidence of the attempt.

R-59 limb 1 is **still open**: no adapter value exists for any case (`iricore` is
uninstallable locally), so no paired comparison has run and no validation report exists.
`kaggle/HOW_TO_RUN_B01_VALIDATION.md` is the step-by-step for the session that closes it.
One correction recorded there rather than repeated: the predeclared tolerance is **already
frozen** — `tolerance_tecu: 1.0`, `tolerance_declared_at_utc: "2026-09-20T12:27:01Z"` (D-50)
— so nothing is owed before the session, and the declaration already precedes any comparison
(R-59 limb 2).

### C. TC-03g's production caller now exists (Recommendation 28)

`scripts/gate_in_session.py`, following the `gate_*.py` convention `gate_secret_scan.py` and
`gate_preflight_report.py` already set. It refuses a non-Kaggle platform **before running
anything** (rather than after both fixtures, which is when `require_in_session_gate` would
have refused it), runs the critical set with the three restricted readers deselected by the
pre-commit hook's own criterion, runs both fixtures in TE §9.2 order with the second only
after the first passes, emits the gate result, and then passes it straight back through
`require_in_session_gate` against this session's own lock and the frozen manifests in force.
It offers no flag to skip a fixture, and a test asserts that it never grows one.

`tests/test_in_session_gate.py` — ten controls: the must-not-fire acceptance case, then
control 30 (a `local` stamp), control 31 (another session's `code_commit`; other
`config_hashes`), control 32 (a result predating a manifest re-freeze), a non-gate payload,
the deselection list by name, the no-skip-flag check, the platform refusal proven by
asserting **no subprocess is launched**, and the one-parser check (the junit summary reuses
`preflight_report.read_junit_module_outcomes` rather than growing a second parser to drift
from it — `nfr-design` c58).

The consuming side needed nothing: `build_environment_and_cpu_preflight_report` already
refuses when no gate result is supplied (Recommendation 28's first limb, closed 2026-09-20).

**Found by the suite, not by review:** the new script's own docstring carried the
restricted-root path as a literal, and `tests/test_locked_test_guard.py`'s R-28 one-door
control failed on it immediately. Rephrased to name D-15 and `src/data/locked_test.py`
instead — the second time in three days that control has caught a new module, which is the
guard working as designed.
