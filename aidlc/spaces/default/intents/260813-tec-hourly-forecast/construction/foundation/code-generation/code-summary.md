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
