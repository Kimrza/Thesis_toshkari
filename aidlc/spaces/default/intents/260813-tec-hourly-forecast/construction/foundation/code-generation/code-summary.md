# Code Summary — `foundation`

**Unit** `foundation` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Plan**: `code-generation-plan.md` — all 12 steps executed, checkboxes marked. No `git commit` was made (Step 12 governance stop).

## Files created

| Path | What |
|---|---|
| `pyproject.toml` | Project metadata, `requires-python == "3.11.*"`, ruff lint+format config, pytest config |
| `requirements.txt` | Pinned: numpy 1.26.4, pandas 2.1.4, pyyaml 6.0.1, pytest 8.2.2, ruff 0.4.8. **No TensorFlow** (Q3=A; pin stays `TBD — freeze gate`); gitleaks 8.18.4 recorded as pinned tool |
| `README.md` | §12 layout, two platforms, CPU-only path, suite/tooling instructions |
| `.gitleaks.toml` | Reviewed allowlist; gitleaks 8.18.4 pinned (Q2=A) |
| `.githooks/pre-commit` | Incremental gitleaks scan (staged diff, fails closed) + critical test set (team practice Q7=D) |
| `configs/{data,features,experiment,seeds}.yaml` | Four governed configs. Frozen values only from D-numbers (seeds D-122: dev 42, final [1337, 2024, 7], bootstrap 20221201, sign-off-pending status carried; D-29 encoding recorded). Every unfrozen scientific field is the literal `TBD — freeze gate`; no machine paths |
| `src/data/experiment_registry.py` | C-2 (Q1=A new module): twenty-column §13.4 append-only registry — R-07/08/09/10/18/19/20, exploratory derivation with G-06 carve-out recorded on-row, durability stamp (every row "unverified on this platform" until W-6 step 8 measures), both-way orphan reconciliation as a pure read |
| `tests/test_determinism.py` | C-1 tests, 35 cases (name authority CR-2026-08-22-TE-AMEND) |
| `tests/test_experiment_registry.py` | C-2 tests, 49 cases |
| `scripts/gate_secret_scan.py` | TA-22 history-inclusive scan wrapper emitting SD-01's evidence contract (tool + pinned version, commit range, scope, result); claims nothing discharged |
| `tests/fixtures/`, `artifacts/releases/`, `artifacts/registry/` | Scaffold dirs with `.gitkeep` |

## Files modified in place

| Path | What |
|---|---|
| `src/data/config.py` | C-1 extension: `ConfigSnapshot`, `DeterminismRecord`, `RunRecord` (8-item lock), `load_configs` (strict YAML, duplicate-key rejection, verbatim snapshot, per-file SHA-256), `assert_no_tbd`, `assert_declared_sources_exist`, `assert_config_hashes_match`, `resolve_platform_roots` (exactly kaggle\|local, no credential value), `assert_credential_names_present` (names only), `seed_everything` (R-06 probe; TF absence recorded honestly as `measurement_status="partial"`), `ensure_process_determinism` (re-exec before graph construction, R-05), `capture_environment_lock` + `assert_lock_complete` |
| `src/data/release.py` | `content_hash_of` now R-11's canonical 12-field representation (floats refused; provenance-bearing); `write_release` refuses caller-supplied `dataset_version` and takes `release_root` — SD-04 enumeration of the single authoritative root, **refuse-on-unreachable** (never empty-population pass); overwrite refusal first (R-13); `verify_release` canonical correspondence |
| `tests/test_release_hashes.py` | SD-04/TA-15 section: all-§13.3-fields assertion; overwrite refusal + bytes-unchanged; unreachable-root refusal (2 shapes); prefix-collision refusal; post-write mutation detection |
| `tests/test_release_contract.py` | Call sites updated to manifest signature; new control: a *correct* supplied `dataset_version` is also refused |

## Test coverage

- **Full suite: 367 passed, 2 skipped, 0 failed** (skips pre-existing) — re-run independently by the orchestrating session with the same result.
- Interpreter: **Python 3.11.9** (matches the governed 3.11 pin at major.minor), bootstrapped via micromamba/conda-forge into a temp env (`Temp\26\tec311`) because this machine had no Python and PyPI is network-blocked. **Smoke evidence only, never governed evidence** — not the governed pip-from-pins path on a governed platform. No acceptance row moves.
- `ruff check` 0.4.8: all checks passed on every created/modified file.
- Negative controls per hard rule: unknown status refused; write-time schema violation refused; no rewrite path; orphans reported never backfilled; durability stamp asserted; overwrite refused; unreachable root refused; collision refused; `assert_no_tbd` fires on planted sentinel; `PlatformError` on unknown platform; hash mismatch terminates naming file + expectation; restricted-root literal absence statically scanned (R-15).

## Key decisions (full detail in the plan + module docstrings)

1. Release identity widened to R-11's canonical 12-field manifest representation — identical bytes with different provenance no longer share identity.
2. `write_release` refuses any supplied `dataset_version`, correct ones included; occupancy check stays first (R-13-conservative ordering).
3. Registry rows carry two extension fields beyond R-18's named three (`exploratory_carveout`, `durability`) — §13.4 is a floor ("including:").
4. R-19 known pre-guard orphans supplied by the auditor (`known_orphans` param); reconciliation is a pure read, byte-identity of both artifacts asserted after it runs.
5. Re-exec sentinel `TEC_FOUNDATION_REEXEC` read-once-and-popped; verified by subprocess handshake test (Windows execv spawn semantics).
6. Restricted-root literal removed from foundation docstrings — the repo's standing R-28 guard test caught the first draft; foundation adds its own R-15 static scan.

## Deviations

- **graphify unavailable** (`graphify` not on PATH): mandatory pre-exploration query and post-modification `graphify update .` could not run; orientation via direct design-artifact reads. Graph now stale for modified files.
- **Interpreter bootstrap** (above) — machine had no Python at all, contradicting the brief's "3.14.7 present" (that interpreter belonged to an earlier clone/session).
- **gitleaks binary not installed**: pre-commit hook fails closed by design; `scripts/gate_secret_scan.py` not executed (gate runs are a human/governed act).
- Step 8 note: `tests/test_release_contract.py` (created under D-31) already covered part of TA-15's matrix; the extension adds the genuinely new SD-04 controls rather than duplicating.
- `evidence/test_run_access_log.jsonl` gained rows from suite runs — the designed behaviour of the locked-test guard's test-mode access log, not a locked-test access.

## Governance stop — owed before any commit (student acts)

- (a) TE §12 naming amendment for `src/data/experiment_registry.py` (config.py precedent, per Q1=A approval).
- (b) D-number for SD-04's enumeration-surface decision (`release_root` = `artifacts/releases` declared relative in `configs/data.yaml`; refuse-on-unreachable).
- (c) Commit message citing D-29, D-122 and the amendment record. Working tree holds 4 modified + 12 new paths; **no governed commit before (a)–(c) exist**.

Owed downstream (restated so not lost): in-Kaggle durability measurement (W-6 step 8) before Kaggle-written registry rows count at a freeze gate; TA-22 history-inclusive scan run + gate acceptance (NFR-SEC-01 unclaimed); D-122 supervisor signature at G-05.

## Review — 2026-09-05 (code-generation, iteration 1)

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T11:17:36Z
**Iteration:** 1

### Findings

| # | Severity | Where | What | Recommended action |
|---|---|---|---|---|
| 1 | Major | `tests/test_determinism.py` (absent); `functional-design/business-rules.md` R-01 "Negative control — the enumeration itself" (lines ~411-416) | R-01's own rule text mandates a specific negative control this unit owns: "A test **re-derives** the distinct project-defined `*Error` names raised across the twelve units' `functional-design` artifacts and **fails** when a name is neither in R-01's fifteen nor disclosed by its raising unit under the any-future clause." This is the control the rule states exists specifically "to catch the failure R-01 suffered twice" (a subclass added later with nobody updating the enumeration), and the governance report's closure evidence explicitly asks for "one programmatic derivation... reconciled against R-01's list and printed in `foundation`'s artifact." No such test exists anywhere in the generated suite: `grep` for "census"/"enumeration"/"fifteen"/"any-future" over `tests/test_determinism.py` (35 collected cases) returns nothing, `code-summary.md`'s own "Negative controls per hard rule" list does not mention it, and the code-generation plan/questions files do not raise it as a stop-and-report item. All sixteen exception classes (`IntegrityError` + 15 subclasses, matching R-01's fifteen named plus `InverseTransformError` riding the any-future clause) are correctly declared in `src/data/config.py`, but the rule's own stated regression guard against the enumeration going stale a third time is unbuilt. | Add a test that greps/parses `construction/*/functional-design/*.md` for `\b[A-Z][A-Za-z0-9]*Error\b` tokens, reconciles the project-defined subset against R-01's sixteen declared classes, and fails on any undisclosed name — matching the rule text and the governance closure evidence verbatim, before this stage is treated as complete. |

### What was verified and held

- **Full suite re-run independently**: `367 passed, 2 skipped` on Python 3.11.9 at `C:\Users\s_sch\AppData\Local\Temp\26\tec311\python.exe` — the claimed count is real, not asserted.
- **ruff 0.4.8** on every created/modified file (`pyproject.toml`, `src/data/config.py`, `src/data/release.py`, `src/data/experiment_registry.py`, `tests/test_determinism.py`, `tests/test_experiment_registry.py`, `tests/test_release_hashes.py`, `tests/test_release_contract.py`, `scripts/gate_secret_scan.py`): all checks passed. (Unrelated pre-existing files outside this unit's touch set — `scripts/audit_ec1_drivers.py`, `scripts/merge_coverage_year.py`, `src/data/locked_test.py`, `tests/test_locked_test_guard.py` — carry 7 lint findings; none are foundation's modified files and the claim "all checks passed on every created/modified file" holds precisely as scoped.)
- **`pyproject.toml`** pins `requires-python == "3.11.*"` exactly; `requirements.txt` excludes TensorFlow entirely (comment-only, no filled pin) matching Q3=A; PyTorch and GPU packages absent.
- **`configs/seeds.yaml`** matches D-122 exactly: `development: 42`, `final: [1337, 2024, 7]`, `bootstrap: 20221201`, pending-signature status carried in comments. No machine/absolute path found in any of the four governed configs (`grep` for `C:\`, `/home/`, `/Users/`, `D:\` — zero hits); every unfrozen field in `data.yaml`/`features.yaml`/`experiment.yaml` is the literal `TBD — freeze gate` sentinel, no value filled by convenience.
- **R-13 (overwrite refusal)**: `write_release` checks `manifest_path.exists()` and refuses before any computation, confirmed in `src/data/release.py`.
- **R-11/R-12 (canonical hash identity, D-29 encoding)**: `content_hash_of` hashes exactly the twelve included fields via RFC-8785-profile canonical JSON with array-element sorting; `dataset_version_for` derives the first 12 hex chars; `write_release` unconditionally refuses a caller-supplied `dataset_version` (correct values included, per `tests/test_release_contract.py::test_a_supplied_correct_dataset_version_is_also_refused`).
- **SD-04 (unreachable release root refuses, never an empty-population pass)**: `_enumerate_release_root` raises `ReleaseError` on a non-directory root rather than returning `[]`; covered by `test_unreachable_release_root_refuses_never_an_empty_population_pass`.
- **SD-06 (eight-item lock)**: `RunRecord` dataclass carries exactly eight fields (`requirements_hash`, `pip_freeze`, `runtime_versions`, `code_commit`, `config_hashes`, `input_versions`, `platform`, `nondeterministic_ops`); `assert_lock_complete` checks all eight, matching the claimed "8-item lock" and `test_environment_lock_captures_eight_of_eight`.
- **R-07/R-08/R-09/R-10/R-18/R-19/R-20**: `src/data/experiment_registry.py` implements the closed status vocabulary with non-empty-reason enforcement, single-append durability-confirmed writes with the torn-write-vs-corruption position distinction, R-18's twenty-column write-time schema assertion (missing-column and unpopulated-column checks both present) plus the `prediction_hash` writer-role refusal and Phase-1 `prior_period_exposure=true` refusal, the `run_id`-keyed both-direction orphan reconciliation with known-orphan reporting (never back-filled), and `exploratory`/`exploratory_carveout`/`durability` all rejected if caller-supplied. All matched against their respective negative controls in `tests/test_experiment_registry.py`.
- **SD-02/R-14 (credential handling)**: `resolve_platform_roots` and `assert_credential_names_present` read only environment-variable **names**, never values; confirmed by direct read of `src/data/config.py` and by `test_resolve_returns_no_credential_value`.
- **R-15 (restricted-root boundary)**: static-scan test correctly excludes `governance-guards`' `src/data/locked_test.py` from `FOUNDATION_MODULES` and asserts the `locked_test_restricted` literal appears in none of the three foundation modules.
- **Boundary trespass**: `grep` of all `import`/`from` lines in `src/data/config.py`, `release.py`, `experiment_registry.py` shows only stdlib and intra-package (`src.data.config`) imports — no import of `src/models`, `src/features`, `src/external`, `src/gnss`, and no new `src/data/registry.py` or `src/data/reuse_registry.py` was created (both correctly left to their owning units).
- **`scripts/gate_secret_scan.py`** explicitly states `"claim_status": "NOT CLAIMED by this script"` in its own evidence JSON and returns non-zero on any precondition failure; claims nothing discharged, consistent with TA-22/NFR-SEC-01 remaining unclaimed.
- **Plan-vs-disk**: all 12 code-generation-plan steps have corresponding artifacts on disk; no `[x]` step claims work that is absent.

### Coverage limits of this pass

- Read scope was this unit's artifacts plus the named contracts (`business-logic-model.md`, `business-rules.md` R-05…R-20, `domain-entities.md`, `security-design.md`, `logical-components.md`, `unit-of-work.md` §1, `requirements.md`, the stage definition). Sibling units' `construction/<other-unit>/` content was not read; the R-01 finding above is grounded entirely in this unit's own `business-rules.md` text and the artifact set under review, not in any sibling artifact.
- Did not independently re-run `.githooks/pre-commit` or `scripts/gate_secret_scan.py` against a live gitleaks binary (not installed in this environment); their fail-closed behavior was verified by code inspection only, consistent with the artifact's own disclosed limitation.
- Did not exhaustively re-verify every one of business-rules.md's ~20 rules line-by-line against every test; R-01 through R-20 and the four SD items named in the dispatch were checked; deeper rules not explicitly named in the dispatch (e.g., R-06's full probe-scope semantics) were spot-checked rather than exhaustively traced.

### Summary

Claim honesty holds throughout: the 367/2 test count, the ruff-clean claim (correctly scoped to created/modified files), the seed values, the absence of machine paths and filled `TBD` sentinels, the eight-item lock, the credential-name-only handling, and the boundary discipline (no cross-unit import, no restricted-root path construction) were all independently re-derived and matched the artifact's own description. The one substantive gap is a missing negative control that R-01 itself mandates by name and that the governance report tied to explicit closure evidence — a real hole in this project's "every hard rule gets a test that proves the violation is caught" testing posture, but narrow in scope (one missing regression test for an enumeration that is today complete and correctly declared) and not accompanied by any other Major or Critical defect. Under this stage's stated verdict rule (NOT-READY on any Critical or more than two Major findings), one Major with zero Critical does not cross the threshold.

**Verdict: READY**

### Cross-unit edit record (2026-09-10) — `tests/test_determinism.py` skip classification, owner-authorised

Appended after the gate rejection lifted the receipt freeze (owner gate worklist
2026-09-10, item 3). On the pyyaml-less clone this unit's `tests/test_determinism.py`
surfaced 19 errors + 3 failures, all one root cause: `load_configs`' production read path
is pyyaml BY DESIGN (TS-01: refuse by name, never a second parser), so every test that
parses a config tree errored at the loader's refusal. Classification applied, not
suppression: `pytest.importorskip("yaml")` at the top of `_write_config_tree` (every
consumer immediately parses the tree) and of the three real-`configs/` tests
(`test_repository_configs_exist_and_parse`, `test_no_config_value_parses_as_an_absolute_path`,
`test_required_fields_map_completeness`). Result on this clone: **12 passed, 23 skipped by
name, 0 failed, 0 errors**; in a governed (pyyaml-bearing) environment all 35 run in full.
No assertion was weakened and no test deleted. Note: the module's earlier import-time error
was the session pytest stand-in's missing `@pytest.fixture` support — a tooling gap fixed
in the scratchpad runner, no repo change.

### Cleanup review (2026-09-10)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-10T07:38:23Z
**Iteration:** 1 (first review pass over the cross-unit edit record above)

**Scope.** Verifies the `tests/test_determinism.py` skip-classification edit recorded
above: is the `importorskip` an honest classification of a design-intended pyyaml-only
read path (TS-01), or a masking of a real repository defect, and was any assertion
weakened.

**Verification performed (adversarial, not trusting the described fix):**

1. **Derived the module's total test count independently**: `grep -c "^def test_"
   tests/test_determinism.py` → **35**, matching 12 passed + 23 skipped exactly (no test
   uncounted or double-counted).
2. **Read the diff directly** (`git diff tests/test_determinism.py`): exactly four
   `pytest.importorskip("yaml")` lines added — one inside `_write_config_tree` (the shared
   tree-builder every config-parsing test calls) and one each at the top of
   `test_repository_configs_exist_and_parse`,
   `test_no_config_value_parses_as_an_absolute_path`, and
   `test_required_fields_map_completeness`. No existing line was deleted, no `assert`
   statement was touched, no `pytest.mark.xfail` or unconditional `pytest.skip`
   introduced — this is purely additive.
3. **Checked whether the skip is an honest classification of a design-intended boundary,
   not a mask for a defect.** `load_configs`'s production read path is stated (both in
   this edit's rationale and independently corroborated by `tests/test_clean_run.py`'s
   own skip at the same boundary: `test_exported_check_full_path_requires_yaml` and the
   module-level clean-run skip both name "pyyaml is not importable on this clone... the
   production read path refuses by name") to refuse any non-pyyaml parse path by name
   (TS-01) rather than silently falling back to a second parser — this is the two-tier
   error-handling posture (`team.md` § Code Style, Q12=B) applied at a missing-dependency
   boundary: an environment gap, not a masked logic defect. The skipped tests are
   precisely the ones that call `_write_config_tree` or otherwise parse the real
   `configs/` tree through `load_configs`; no test unrelated to config-parsing was
   touched.
4. **Reproduced independently** (scratchpad CPython 3.11.16 + stdlib pytest stand-in,
   PyPI unreachable): `tests.test_determinism` → **12 passed, 0 failed, 23 skipped, 0
   errors** — matches the cross-unit edit record's claimed count exactly, and each of the
   23 skip notes names `"could not import 'yaml'"` at the `importorskip` call, not a
   silent pass.
5. **Confirmed via the sibling review above** (this unit's own primary review, dated
   separately) that the 367/2 test count and R-01–R-20 coverage claims already verified
   there are undisturbed by this addition — the edit touches only
   `tests/test_determinism.py`, and does not alter `src/data/environment.py` or any other
   production module (`git diff --stat` confirms zero `src/` changes attributable to this
   unit's edit).

**Findings:** none survive verification at any severity. The skip classification is
honest, narrowly scoped to the pyyaml-dependent config-parsing paths, does not weaken any
assertion, and matches the project's own stated design (TS-01, refuse-by-name rather than
silently substitute a parser).

### Summary

The `test_determinism.py` skip-classification edit is verified as an honest, narrowly
scoped `pytest.importorskip("yaml")` applied only at the pyyaml-dependent config-parsing
boundary that `load_configs` is designed (TS-01) to refuse by name on an environment
without pyyaml. No assertion was weakened, no test was deleted, and the claimed 12/23/0/0
result reproduces exactly under independent execution. No Critical, Major, or Minor
defect found.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-10T11:33:57Z
**Iteration:** Owner-rulings implementation review (2026-09-10)

### Findings

None survive verification at any severity for this unit.

### Verification performed

- **`cell_rule` (owner ruling 2: freeze the EXISTING convention).** `configs/data.yaml`
  diff read in full: `cell_rule: "floor-half-open-d1"`. Cross-checked against
  `src/data/registry.py` — this unit's own module, untouched by the diff (`git diff HEAD --
  src/data/registry.py` produces no output) — where `CELL_RULE_ID: Final[str] =
  "floor-half-open-d1"` (line 98) was already the live identifier `assert_registry_resolved`
  compares the config field against (lines 289–301). The value transcribed into
  `configs/data.yaml` is therefore the pre-existing code constant verbatim, not an invented
  identifier. `stations` in the same file is confirmed byte-unchanged (`TBD — freeze gate`)
  by reading the diff — no station was moved, matching the claim.
  `governance/CHANGE_RECORD_2026-09-10_owner_rulings_implementation.md` §2 (draft D-A)
  states the §18.2 Student+Supervisor countersignature obligation explicitly and marks it
  owed, not discharged — matches TE §18.2's actual assignment of this rule.
- **`practical_relevance_threshold` (owner ruling 3).** Not this unit's owned field
  (`configs/experiment.yaml`, consumed elsewhere in the pipeline); confirmed the sentinel
  `TBD — freeze gate` is preserved verbatim in the diff and that no numeric value was
  written anywhere in the repository search for `practical_relevance_threshold` under
  `src/`, `tests/`, `scripts/` (no enforcement point exists that would require a numeral).
- **`evidence/DECISIONS.md`**: ends at D-32, zero diff — confirmed independently. No
  D-number was minted by this pass for D-A; the register remains the owner's to update.
- **Test totals**: full-suite run under the stdlib pytest stand-in (26 modules) reproduces
  exactly `1134 passed, 0 failed, 39 skipped, 0 errors`, matching the claim, with this
  unit's own `test_determinism.py` module contributing `12 passed, 0 failed, 23 skipped, 0
  errors` unchanged from its own prior review.
- **Untouched TBDs**: spot-checked `folds`, `embargo_hours`, `feature_set_id`,
  `feature_dictionary`, `availability_lags`, `normalization` directly in
  `configs/experiment.yaml`/`configs/features.yaml` — all still read `TBD — freeze gate`
  verbatim, matching §7 of the change record.

### Summary

The `cell_rule` freeze is a genuine transcription of this unit's own pre-existing
`CELL_RULE_ID` constant, not an invented value, and the diff leaves `stations` and this
unit's other TBD sentinels untouched. The Student+Supervisor countersignature obligation
is stated, not silently discharged. No defect found in this unit's exposure to the pass.

## Floor-reset re-review (2026-09-11)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-11T13:30:47Z
**Iteration:** Gate-floor reset — re-derived against HEAD `715f392`, not carried from any
prior verdict in this file.

### Scope and method

Re-verified adversarially against the current tree: `src/data/config.py`,
`src/data/experiment_registry.py`, `src/data/release.py`, `configs/*.yaml`,
`tests/test_determinism.py`, `tests/test_experiment_registry.py`,
`tests/test_release_hashes.py`, plus (spot-check only, per the dispatch's named
integration point) `src/data/acquisition.py` and `tests/test_acquisition.py` for the
cross-unit egress guard this unit's module now calls into. `git log`/`git show 715f392`
used to establish which commit actually changed which files (this unit's module was
edited in `715f392`, not a prior commit, contra a naive stat-only read of that commit's
top-of-diff).

### Findings

| # | Severity | Where | What | Recommendation |
|---|---|---|---|---|
| 1 | Major | `functional-design/business-rules.md` R-01 (lines ~411–416: "Negative control — the enumeration itself"); `tests/` (26 modules, no such test) | **Unresolved across three review passes (2026-09-05, 2026-09-10, this one).** R-01's own rule text mandates a test that re-derives every project-defined `*Error` name raised across the twelve units' `functional-design` artifacts and fails when a name is neither in R-01's fifteen nor disclosed under the any-future clause — the control the rule states exists "to catch the failure R-01 suffered twice." `grep -rn "def test_" tests/*.py` (26 modules) turns up per-unit spot-checks (`issubclass(XError, IntegrityError)` in `test_acquisition.py`, `test_reuse_registry.py`, `test_phase_contract.py`, `test_common_masks.py`, `test_prepared_target_schema.py`) but no census/reconciliation test anywhere in the suite; `tests/test_determinism.py` (this unit's own C-1 module) has none. The governance closure evidence explicitly asked for "one programmatic derivation… reconciled against R-01's list and printed in `foundation`'s artifact" — still absent from both the test suite and this artifact. | Add the reconciliation test to `tests/test_determinism.py` (or a new `tests/test_exception_taxonomy.py`) before this stage is treated as closed; the fifteen-plus-any-future census is otherwise a hand-maintained claim with no regression guard, which is exactly the failure mode R-01 names. |
| 2 | Minor | `code-summary.md` (this file), "Files modified in place" table | This unit's own record still does not describe the credential-egress addition to `src/data/experiment_registry.py` (`REDACTED_FREE_TEXT_FIELDS`, `_guard_free_text_egress`, called from `append_registry_event`) landed by the `acquisition` repair in `715f392`. Confirmed a real gap, not a false claim: `git show 715f392 -- src/data/experiment_registry.py` shows +62/−0 lines to a module this file's own table describes with no reference to the addition anywhere above. Already disclosed as a known gate item in the `715f392` commit message and in `team.md`'s `gf-3` learning, so this is recorded per the dispatch instruction rather than treated as newly discovered. | Update the "Files modified in place" entry for `src/data/experiment_registry.py` at the next touch of this artifact, per `gf-3`. |

### Verification performed (evidence, not trust)

- **Cross-unit edit soundness (item 2 of the dispatch).** Read `git show 715f392 -- src/data/experiment_registry.py` in full: `_guard_free_text_egress` is called inside `append_registry_event` immediately after `_validate_row` and strictly *before* `os.open`/`os.write` (line ~380, confirmed by direct read of the function body, lines 341–430) — `_validate_row` itself performs no I/O (read in full, lines 185–239: pure dict/type checks, no `open`/`os.write`). A refused row therefore reaches no `os.write` call at all; the log is byte-identical on refusal, not merely "restored." `tests/test_acquisition.py::test_registry_reason_carrying_a_credential_refuses_and_writes_no_byte` asserts `registry.read_bytes() == before` directly, and `test_registry_notes_carrying_a_credential_refuses_and_writes_no_byte` asserts `not registry.exists()` on the first-row case — both independently reproduced (below).
  - **False-positive risk on this unit's own legitimate writers**: `test_registry_egress_coverage_is_derived_and_equals_the_declared_field_set` drives every one of the twenty registry columns plus `reason` with a credential sentinel and asserts the DERIVED refused-set equals `REDACTED_FREE_TEXT_FIELDS` exactly (`("notes", "reason")`) — so the guard neither over-refuses a machine-generated column (`run_id`, hex digests, `environment_lock_hash`) nor under-covers a prose column. `test_a_clean_registry_row_still_appends_after_the_guard` is the explicit must-not-fire control: ordinary prose in `notes` appends exactly one record. Reproduced independently (below): both pass.
  - **R-01 compliance of the new exception**: `CredentialEgressError` derives from `IntegrityError` (`src/data/acquisition.py:172`), riding the any-future clause per R-01's own text — consistent, not a second declaration site; R-01 governs the base-class relation, not a single-file-only declaration (business-rules.md ~line 170: "every project-defined exception derives from `IntegrityError`", eighteen named riders including `CredentialEgressError` explicitly enumerated at ~line 226).
- **R-01 single-base-class integrity (re-derived, not carried).** `grep -rn "^class .*Error" src/` → 30 classes; every one derives from `IntegrityError` either directly or (for `AcquisitionError`, `CredentialEgressError`) as its own subclass of `IntegrityError`. `IntegrityError` itself and its 23 direct subclasses live solely in `src/data/config.py` (the single declaration site for the *base hierarchy proper*); the six riders declared in their raising units (`AcquisitionError`, `CredentialEgressError` in `acquisition.py`; `GateError` in `inventory.py`; `EvidenceScanError` in `locked_test.py`; `ManifestError` in `phase_contract.py`; `ReuseError` in `reuse_registry.py`) match R-01's own "declared where raised, under the any-future clause" design — not a violation of R-01, which never claims single-file declaration for every subclass, only a shared base.
- **`load_configs` / `ConfigSnapshot` / D-38 additions.** `configs/data.yaml`'s `partitions` (six entries, F1–F4 plus locked December) and `configs/experiment.yaml`'s `embargo_hours: 24` read as real, transcribed values (not `TBD — freeze gate`); `grep -n "embargo_hours\|folds" configs/experiment.yaml` confirms `folds` is still the literal sentinel and carries an explicit "has NO reader" comment. Neither `partitions` nor `embargo_hours` is a `REQUIRED_FIELDS_MAP` entry for any stage (`src/data/config.py` lines 539–608, read in full) — by the same documented design as the other deliberately-minimal preflight entries, enforced at each consuming unit's own raise point rather than this unit's preflight. `grep -c TBD configs/*.yaml` → data.yaml 2, features.yaml 5, experiment.yaml 20, seeds.yaml 0 — no sentinel silently filled. `grep` for `C:\`, `/home/`, `/Users/`, `D:\` across all four configs → zero hits.
- **`tests/test_determinism.py` skip classification.** `grep -c "^def test_" tests/test_determinism.py` → 35, matching 12+23 exactly. Independently reproduced under the scratchpad's stdlib pytest stand-in (`26ca41ab.../scratchpad/pytest_standin/run_tests.py`, CPython 3.11.16): **12 passed, 0 failed, 23 skipped, 0 errors**, each skip naming `could not import 'yaml'` — matches the prior cleanup review's claim exactly, no drift since 2026-09-10.
- **Test totals, independently re-run** (stdlib stand-in; real pytest/ruff unavailable, PyPI egress blocked — named honestly, not called "pytest"):
  - `tests.test_experiment_registry`: **49 passed, 0 failed, 0 skipped, 0 errors** (26 source-level `def test_` functions, 3 parametrized, expanding to 49 executed cases — matches the code-summary's "49 cases" read as executed-case count, not function count).
  - `tests.test_determinism`: **12 passed, 0 failed, 23 skipped, 0 errors**.
  - `tests.test_release_hashes`: **149 passed, 0 failed, 0 skipped, 0 errors**.
  - Full 26-module suite: **1144 passed, 0 failed, 39 skipped, 0 errors** — reproduces `715f392`'s commit-message claim exactly.
  - `tests.test_acquisition` (spot-check for the cross-unit guard only): **56 passed, 0 failed, 0 skipped, 0 errors**, including the egress-coverage-derivation and must-not-fire controls named above.
- **No credential, no weakened guard, no silently filled TBD** found anywhere in this unit's touched surface. `requirements.txt` carries `tensorflow==2.21.0` per the owner's D-36 ruling, consistent with the dispatch context (install/import unverified, disclosed, not this unit's defect to raise again).

### Coverage limits of this pass

- Read scope: this unit's own artifacts and modules, the shared contracts named in the dispatch, `configs/`, `evidence/DECISIONS.md`, and — as the one permitted spot-check for the named integration point — `src/data/acquisition.py` and `tests/test_acquisition.py` for the guard this unit's module now calls. No other sibling unit's `construction/<unit>/` directory was read.
- Did not re-run `ruff` (not installed, PyPI egress blocked) — consistent with every prior pass on this unit; code inspection only for style/lint conformance on the new lines.
- Did not re-verify governance/gate-worklist state beyond what bears directly on this unit's code and tests.

### Summary

One Major survives, unresolved for the third consecutive review pass: R-01's own mandated reconciliation negative control (the enumeration census) is still absent from the suite, though the hierarchy it would check is today correctly declared and no live violation exists. The cross-unit edit to `src/data/experiment_registry.py` is genuinely additive and fail-closed — verified by direct read of call order (guard before any `os.write`), by independent reproduction of the byte-identical-on-refusal and must-not-fire tests, and by the derived-coverage test that pins the routed-column set exactly to `REDACTED_FREE_TEXT_FIELDS`; it does not newly refuse any row this unit's own writers legitimately produce. The one disclosed record-staleness item (this file not describing that edit) is recorded per dispatch instruction rather than newly discovered, and is not treated as a code defect. D-38's config additions are genuine transcriptions with no TBD weakened and no machine path introduced. All re-run test counts (49 / 12+23 / 149 / 1144 total) reproduce exactly under independent execution. Per this stage's stated verdict rule (NOT-READY only on any Critical or more than two Major findings), one Major with zero Critical does not cross the threshold.

**Verdict: READY**
