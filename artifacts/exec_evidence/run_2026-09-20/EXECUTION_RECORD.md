# Execution evidence — first governed-environment run of the test suite

**Date (UTC):** 2026-09-20
**Scope of this session:** environment establishment and execution-dependent remediation only.
No governance decision, documentation cleanup or reviewer workflow was performed.

This record exists because every prior remediation pass was **statically complete and never
executed** — `governance/reviews/GOV-2026-09-20-CG-01.md` § "⚠ Verification status — read
first" states it plainly: *"No claim in this manifest may be read as 'verified passing.'"*
This is the run that changes that for the eligible subset.

---

## 1. Environment

| Item | Value |
|---|---|
| Interpreter | CPython **3.11.16** (`conda` env `tec-thesis-311`) |
| Interpreter path | `C:\Users\LOTUS\anaconda3\envs\tec-thesis-311\python.exe` |
| Governed pin | `pyproject.toml` `requires-python = "==3.11.*"` (TS-01 / TC-03d) — **satisfied** |
| Platform | local (Windows 11, `LAPTOP-TV4UGFBC`), `TEC_PLATFORM` unset |
| Device policy | `CUDA_VISIBLE_DEVICES=""` on every invocation; CPU-only (TC-01) |
| `PYTHONHASHSEED` | `0` on the final run (TE §13.2 amendment, `CR-2026-08-22-TE-AMEND`) |
| Code commit | `de1732fc0b28c411308424de28e7ba9bfdfeb08b` |
| Full freeze | `pip_freeze.txt` (51 packages), `python_version.txt` |
| Input hashes | `input_hashes.txt` (`requirements.txt` + all four `configs/*.yaml`) |
| Working tree at run | `git_status_at_run.txt` |

**The environment was already present and was not rebuilt.** The conda env `tec-thesis-311`
existed with every governed pin already matching `requirements.txt` exactly:

```
numpy 1.26.4   pandas 2.1.4   PyYAML 6.0.1   scikit-learn 1.4.2
tensorflow 2.21.0   pytest 8.2.2   ruff 0.4.8
```

TensorFlow 2.21.0 imports and initialises on CPU (verified directly). No pin was changed, no
version substituted, and **Python 3.14.7 — the interpreter on `PATH` — was not used for any
governed command.** Other Python installations were left untouched.

**Two packages remain absent, both deliberately:**

* `matplotlib` — its version is a live `TBD — freeze gate` in `requirements.txt` (Rec 38,
  dispositions §5 item 15, Student, before G-07). Installing it would require choosing a
  version, which is exactly the convenience-fill Vision §1.2 / TE §1.1 forbid. No executed
  test needed it.
* `pyarrow` — unpinned, escalation 5 of the remediation manifest. Same class; not pinned by
  any agent.

**Correction to the review's environment finding.** `GOV-2026-09-20-CG-01` records
*"PyPI is unreachable — `pypi.org/simple/` times out"*. Measured 2026-09-20 on this clone:
`https://pypi.org/simple/pytest/` returns **HTTP 200 in 1.42 s**. PyPI reachability is no
longer a blocker; the remaining blockers are the frozen-value ones in §4 below.

---

## 2. What was executed, and what was deliberately not

**Command (final run), reproducible verbatim:**

```bash
CUDA_VISIBLE_DEVICES="" PYTHONHASHSEED=0 \
  /c/Users/LOTUS/anaconda3/envs/tec-thesis-311/python.exe -m pytest -q tests/ \
  --ignore=tests/test_release_hashes.py \
  --ignore=tests/test_acquisition_window.py \
  --ignore=tests/test_phase_boundary.py \
  -p no:cacheprovider --junitxml=artifacts/exec_evidence/run_2026-09-20/junit_final.xml
```

**Result: 1,190 tests — 1,186 passed, 0 failed, 0 errors, 4 skipped, 168.8 s.**
Machine-readable: `junit_final.xml`. Console: `pytest_final.log`.

**The three deselected modules were never run**, on the criterion `.githooks/pre-commit`
already derives and states: a module belongs to the gate-only set when it **reads bytes from
under `evidence/locked_test_restricted/`**.

| Deselected module | Why |
|---|---|
| `tests/test_release_hashes.py` | `_sha256()` streams December bytes |
| `tests/test_acquisition_window.py` | `csv.DictReader` over December rows |
| `tests/test_phase_boundary.py` | `_csv_header()` reads December rows |

Each requires an occasion carrying an authorization to record (Vision §8.3). **No such
authorization exists, so they were not run.** No December 2022 target value was read by any
command in this session.

**Custody artifacts, verified before and after every run:**

| Artifact | Before | After | Verdict |
|---|---|---|---|
| `evidence/test_run_access_log.jsonl` | 5,964 rows, sha256 `985f0671…` | 5,964 rows, sha256 `985f0671…` | **byte-identical** |
| `artifacts/registry/experiment_registry.jsonl` | 28 rows, sha256 `5bb40cab…` | 30 rows, sha256 `c7b641a8…` | **+2 rows, append-only** |

The two registry rows are disclosed rather than suppressed: they are the `started` and
`aborted` pair for `walking-skeleton-plumbing_7day-20260920T194651Z-b26647bd`, the measuring-run
attempt in §4 below, carrying `locked_test_accessed: false` and the abort's full reason text.
This is NFR-AUD-01 behaving as designed — a failed run stays visible with its status and
reason. No row was modified, deleted or re-run. Four `artifacts/run_snapshots/` directories
were likewise written by those attempts.

---

## 3. Failures found by execution, and the fixes

The first-ever run produced **6 failures out of 1,188**. Two were real code defects; four were
expectations that had gone stale against the very remediation that landed on 2026-09-20.

### 3.1 Real defect — the Recommendation 1 placeholder survived in a third producer

`tests/test_merge_script_restricted_reads.py::test_guarded_routes_a_restricted_path_and_writes_a_row`

```
ValueError: Invalid isoformat string: 'recorded-at-call-time-by-the-runner'
```

`src/data/locked_test.py`'s `_assert_parseable_retrieved_at` docstring states *"The two
producers were fixed 2026-09-20"*. There were **three**. `scripts/merge_coverage_year.py:124`
still passed the literal placeholder, so the guard refused it and the script could not route a
restricted path at all. Static review could not see this: the guard and the caller are both
individually correct-looking, and only running them together raises.

**Fix:** `retrieved_at_utc=datetime.now(timezone.utc).isoformat()`, with the scope of the field
documented at the call site (it is the caller's claim; `logged_at_utc`, stamped by the guard
before the `fsync`, remains the ordering evidence). `grep` over `src/`, `scripts/`, `tests/`
now returns zero live occurrences of the placeholder outside historical commentary.

### 3.2 Real defect — the R-24 leakage-guard detector was wrong in both directions

`tests/test_phase_contract.py::test_every_phase1_producing_script_calls_the_field_guard_before_its_first_write`

```
AssertionError: Phase 1 producing script(s) violate R-24's before-first-write obligation:
{'07_evaluate_and_report.py': 'first write (line 1040) precedes the first
 assert_no_raw_fields call (line 1213)'}
```

**`scripts/07_evaluate_and_report.py` is not in violation.** The check compared the smallest
write line number against the smallest guard line number, which is a proxy for R-24's actual
obligation — that the guard *runs* before the first write *runs*. Derived from the AST and
printed before assertion:

* line 1040 is inside `_report_set` (744–1077), which is **defined above** but **called below**
  the guard;
* `_run` (1292) calls `assert_no_raw_fields` at :1295, then reaches `_report_set` via
  `_evaluate_partition` (1347);
* the fixture entry `_run_fixture_scale` (1186) guards at :1213 before the same descent at 1240.

Both execution paths satisfy R-24. The more serious half is the **false negative** the same
proxy carries: a writer helper defined *below* the guard but called *before* it would have a
larger line number, clear the check, and write unguarded at run time.

**Fix:** `_first_unguarded_write_lineno` walks the call graph from the module body in statement
order, carrying a `guarded` flag; a write reached while unguarded is the violation. Unresolvable
calls are stepped over, so the check stays conservative in the same direction as before. The
"never calls `assert_no_raw_fields`" branch is unchanged and still fires for a producing script
with no guard call at all, write-bearing or not.

**Two controls added** (the project's negative-control-per-rule practice):
`test_a_write_in_a_helper_called_before_the_guard_is_detected` — the false-negative shape, which
the superseded check cleared — and `test_a_write_in_a_helper_called_after_the_guard_passes`,
`07`'s real shape reduced, which it wrongly flagged. Both pass; the four pre-existing controls
are untouched and still pass.

### 3.3 Stale expectation — fixture manifests now exist by owner-authorised remediation

`tests/test_clean_run.py::test_fixture_trees_exist_without_manifests` asserted the manifests must
**not exist**, as a proxy for BLK-02 ("no manifest may be authored by hand"). Recommendation 37's
approved remediation then authored both as structural skeletons carrying only `TBD — freeze gate`
sentinels. File absence and BLK-02 had come apart.

**Fix:** rebound to BLK-02 itself, renamed
`test_fixture_manifests_are_structural_only_and_carry_no_measured_value`. For each manifest that
exists it now asserts the sentinel is present **and** that `load_fixture_manifest` refuses it by
name at a measured field. This is stronger than absence: a hand-authored measured value would
load clean and is now caught, where previously it would have been caught only if someone noticed
the file. Absence remains permitted.

### 3.4 Stale expectation — the Rec 44 fence selector matched two fences

`REPRODUCTION.md` carries `export PYTHONHASHSEED=0` in **two** `bash` fences: §3's stage sequence
and §4's "Running the tests locally" block. Both are correct — a reproducer must export it before
pytest too, and deleting it from §4 to make a test pass would damage the guide to protect the
checker.

**Fix:** the selector now requires the fence to carry `run_walking_skeleton.py` as well, which
only the sequence fence has. Both conditions are asserted, so a guide that later drops the export
from the sequence fence still fails rather than silently selecting the wrong block.

### 3.5 Stale expectation — the December custody inventory gained the supersession notice

The Rec 1 remediation added `evidence/test_run_access_log.SUPERSEDED_2026-09-20.md` beside the
closed log; the inventory's `outside_automated_inspection` expectation did not list it.

**Fix:** added, with the reason derived rather than assumed — it lands there because it is a
Markdown record, the disposition every other `.md` in that set carries, **not** because of its
content: it matches `vtec|tecu` 0 times and carries no `2022-12-DD` date (printed before
assertion). The closed log it describes is unmodified.

### 3.6 A test assertion that verified nothing — `ruff` B015

`tests/test_train_only_transforms.py:319` read

```python
assert_consumable(_bundle(_score_spec("F1"), transform_id="T-F1")) is None
```

— a bare expression statement with no `assert`. The call still ran, so a refusal would still
have raised; but the `is None` result was discarded and verified nothing. Not vacuous, and not
a passing test that should have failed, but a stated expectation that was not being checked.
`assert` prepended; the module's 31 tests pass and B015 is gone.

### 3.7 Lint

`tests/test_phase_contract.py` and `tests/test_locked_test_guard.py` were clean at `HEAD` and
are clean now. The pre-existing findings in `scripts/merge_coverage_year.py` (legacy, pending
the §5 retirement ruling), `tests/test_clean_run.py` and the rest of `tests/` are unchanged in
number and kind — 28 across the suite, none introduced here. No file was wholesale reformatted,
deliberately: `ruff format` would rewrite these files wholesale and bury the substantive diff.

**Final state after all fixes: 1,190 tests — 1,186 passed, 0 failed, 0 errors, 4 skipped.**

---

## 4. Execution-owed items that remain blocked, and by what exactly

### 4.1 Twenty-five `TBD — freeze gate` sentinels in the governed configs

Derived and printed: `configs/experiment.yaml` **20**, `configs/features.yaml` **4**,
`configs/data.yaml` **1**, `configs/seeds.yaml` **0**. Among them `experiment.folds`,
`features.feature_set_id`, `features.normalization`, `experiment.window_length_hours`.

Every stage entry point refuses while these stand, which is §18.3 behaving correctly. Confirmed
by execution, not inferred:

```
01_inventory_and_registry: preflight refusal: … fixture_manifest.yaml:
row_count_ranges.hourly_target: measured field carries no measuring_run_id …
```

and `tests/test_clean_run.py::test_clean_run_completion_or_skip_with_named_reason` skipping with
*"first unmet precondition: configs/experiment.yaml: folds is `TBD — freeze gate`"*.

No implementer may fill these (Vision §1.2; TE §1.1; §18.3's "must stop and report rather than
choose a default"). **This blocks §5 items 6, 7, 8, 10 and 11 and every remaining
execution-owed finding not discharged in §5 below.**

### 4.2 A deadlock between Recommendation 37's skeletons and R-134 obligation 3 — new, remediation-introduced

Found by execution, not present in the sixty findings. The two paths that could populate the
fixture manifests refuse each other:

```
# comparison run
run_walking_skeleton: preflight refusal: … fixture_manifest.yaml:
row_count_ranges.hourly_target: measured field carries no measuring_run_id …

# measuring run
run_walking_skeleton: aborted: … fixture_manifest.yaml:
a manifest already exists; it is preserved, never overwritten (R-134 obligation 3)
```

`scripts/run_walking_skeleton.py:752` gates `--emit-candidate` on a bare
`manifest_path_for(...).exists()`. That guard exists to stop a **frozen, measured** manifest being
overwritten by a re-measurement. It cannot distinguish one from a pure-sentinel structural
skeleton, so authoring the skeletons closed the only route to the measured values they are
waiting for — dispositions §5 item 8 cannot be performed as written.

**Deliberately not fixed in this session.** Narrowing a governed guard is an owner act, and it
would buy nothing executable while §4.1 stands: the measuring run would refuse at the first
stage script anyway. **Owner ruling needed**, two options: move the skeletons to a
non-colliding name (they are remediation artifacts, not owner freezes, and their own headers say
they are not frozen manifests), or narrow the guard to refuse only a manifest carrying at least
one measured field with a `measuring_run_id`, preserving the replaced file rather than deleting
it. The second is durable; both need the ruling.

**Checked and corrected before reporting:** stage scripts refuse in *both* states — with the
skeletons present at a measured field, with them absent at BLK-02 — so the skeletons did **not**
introduce a new class of block for the stage scripts. The block they introduced is specific to
the measuring path.

### 4.3 Owner-gated config blocks

`configs/experiment.yaml` is missing three blocks the remediated code refuses without:
`models.climatology` (dispositions §4.1, Rec 2), `models.refit` (§4.2, Rec 5), and
`reporting.top1pct_sensitivity` (Rec 21). Each needs a D-number adoption and, for §4.1/§4.2, a
supervisor countersignature. **No M-03 fit, no refit, and no completed `scripts/07` run until
they land.**

### 4.4 Authorization-gated

The three restricted modules, and with them the `test_release_hashes` / `test_acquisition_window`
evidence and `test_locked_test_guard`'s test-mode reconciliation limb (skipped with a named
reason). These need a recorded authorization occasion, not an environment.

---

## 5. Findings whose execution evidence now exists

Closure is claimed only where the acceptance criterion is "the test executes and passes", and
only for the limb this run actually covers.

| Rec | Remaining limb per the manifest | State after this run |
|---|---|---|
| 12 | execution (21 functions / 25 cases, four TA controls) | **Executed: 25 cases in `tests/test_feature_leakage_guards.py`, all passing.** The §12-mandated module is no longer unexecuted. |
| 6 | execution of the end-to-end locked-path control (synthetic December only) | **Executed and passing:** `test_the_locked_path_runs_end_to_end_on_synthetic_december_and_leaves_a_receipt` and `test_script_05_has_a_guarded_dec_branch_that_refuses_without_the_signature`. Synthetic December only; no real locked byte read. |
| 5 | §4.2 D-number; `models.refit` block; execution | **Execution limb done** — the seven refit / locked-partition controls in `tests/test_models_smoke.py` §15 pass, including "no fitted family may be fitted on the locked partition" and "a December bundle offered as the validation set is refused". D-number and config block remain owner-gated. |
| 14, 16, 19, 25, 26, 30, 32, 41, 44, 46, 50, 58 | execution / execution of invocation controls | **Executed within the 1,186 passing tests.** Each module named in the manifest for these ran green; see `junit_final.xml` for the per-test record. |
| 1 | reconciliation run; owner ruling on two historical `run_id`s | **Execution surfaced the unfixed third producer (§3.1) and it is now fixed.** The reconciliation run and the owner ruling remain. |

Not claimed closed: anything whose evidence is a fixture run, a clean run, a Kaggle session, a
provider census, a CCMC value, or a restricted-module execution. All are blocked by §4.

---

## 6. Prohibitions observed

* No December 2022 target value read; no file content read under `evidence/locked_test_restricted/`.
* The three restricted test modules were not run.
* No row of `evidence/test_run_access_log.jsonl` modified — byte-identical before and after.
* No registry row modified, deleted or re-run; two rows appended by a real aborted run, disclosed above.
* No scientific value invented; no `TBD — freeze gate` sentinel filled.
* No governed pin changed; no `PreFlight/` document edited; nothing written to `evidence/DECISIONS.md`.
* No git commit, amend, rebase or config change; `core.hooksPath` left **UNSET** (enabling it is
  dispositions §5 item 4, an owner act).
* The temporary manifest rename used to isolate §4.2's cause was restored in the same command;
  `git status` on `tests/fixtures/` is clean.

---

# Session 2 — blocker resolution and the first partial fixture sequence

Same environment (`tec-thesis-311`, CPython 3.11.16, `CUDA_VISIBLE_DEVICES=""`,
`PYTHONHASHSEED=0`), same governed pins, unchanged. Baseline commit `de1732f`.

## 7. Suite

**1,202 tests — 1,198 passed, 0 failed, 0 errors, 4 skipped.** Up from 1,190/1,186 at the end
of session 1: +12 new controls, 0 regressions. `junit_final_session2.xml`,
`pytest_final_session2.log`.

The three December-reading modules were again **not run**. `evidence/test_run_access_log.jsonl`
is byte-identical across both sessions: 5,964 rows, sha256 `985f0671…`. Zero registry rows
anywhere carry `locked_test_accessed: true`.

## 8. The fixture sequence now runs, and stops somewhere real

Registry evidence from this session (append-only, 18 rows):

| Stage | Outcome |
|---|---|
| `acquisition` (00) | **completed** ×2 |
| `inventory-and-registry` (01) | **completed** (after the identity transcription; 2 earlier aborts before it) |
| `target-standardization` (02) | aborted — `configs/data.yaml qc_operations`: list absent, supervisor freeze owed |

Before this session the sequence could not start at all. It now reaches stage 02 and stops at a
genuine governance precondition rather than at a tooling collision.

## 9. What was fixed

* **The fixture deadlock** (`CR-2026-09-20-FIXTURE-CANDIDATE-PATH`). A measuring run writes to
  its own per-run candidate path; promotion to the reference manifest is a separate, recorded,
  validating act that preserves what it replaces. 9 synthetic controls, including the deadlock
  control and the must-not-move control on comparison mode.
* **A hole found by those tests, not by the board**: `validate_manifest_mapping` refused a
  measured field carrying no `measuring_run_id`, but accepted one carrying a run id **and the
  `TBD — freeze gate` sentinel as its value** — so an unmeasured bound could have reached a
  comparison run's runtime-range assertion. Now refused anywhere in a manifest.
* **Three config blocks** (`CR-2026-09-20-CONFIG-BLOCKS`): `models.climatology` (Rec 2),
  `models.refit` (Rec 5's rule limb), `data.target.identity` (transcription of already-approved
  identifiers, which also unblocks the required pre-G-05 December coverage audit path).
  `reporting.top1pct_sensitivity` written as sentinels with the open choice stated.
* **A false precondition**: the clean-run scanner named `experiment.folds` and attributed
  `assert_no_tbd` to it. Measured false — `folds` is in no `REQUIRED_FIELDS_MAP` entry, and
  stage 01 completed with it still unresolved. The scanner now names `qc_operations`.

## 10. Still owed — human acts only

`qc_operations` (supervisor freeze, blocking now); D-number adoption + countersignature for the
climatology and refit rules; `window_length_hours` (dispositions §4.4); `top1pct_sensitivity`
scope and fraction (supervisor, before G-06); `declared_baseline_per_track` / `selection`;
`december_day_range`; the three `features.yaml` ids. Full table:
`CONFIG_SENTINEL_RECONCILIATION.md`.

## 11. Prohibitions, session 2

Unchanged from §6 and re-verified: no December value read, no restricted module run, no access
log row touched, no registry row modified (18 appended by real runs, every one attributable), no
scientific value invented, no sentinel filled by convenience, no D-number written to
`evidence/DECISIONS.md`, no supervisor signature claimed or backdated, no git commit or config
change, `core.hooksPath` still UNSET.
