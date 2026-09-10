# Code Summary — `acquisition`

**Unit** `acquisition` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Plan**: `code-generation-plan.md` — all 9 steps executed, checkboxes marked. No `git commit` (governance stop). No December content, restricted-root path, or live network call anywhere in this pass.

## Files created

| Path | What |
|---|---|
| `src/data/acquisition.py` | Q2=A new module. Redaction serializer `guard_egress`/`guard_egress_value`: signed URLs + auth headers refused **unconditionally** (allowlist never consulted for them); prefix/entropy heuristic blocks and names its match (3 mixed classes at len ≥ 20, or 2 at len ≥ 32 without filename separators); `REDACTION_ALLOWLIST` as documented review surface with no-silencing rule; `CredentialEgressError` + `AcquisitionError` derive from `IntegrityError` (R-01 any-future clause). `RetrievalClient`: injected transport/sleep/rng/clock; approved policy (5 attempts, backoff 1 s ×2 cap 60 s full jitter, 60 s timeout) embedded in run record + manifests via `retrieval_policy()`; **completeness before hash**; partial never promoted; divergence recorded (both filenames, both hashes) + overwrite refused; resumption via offset. Manifest writers: R-35 absent-key = literal `"unknown"` (one raise site), R-36 `provenance_class` full\|derived_only + hash-less provider row refused, R-40 nine §5.1 fields + one release grade per series, R-37 NaN + conservation invariant as manifest field, R-34/R-42 release-side refusals, R-31 record-timestamp membership (`assert_no_locked_month_records`). Notebook saved-output check + `check-notebook-outputs` CLI |
| `scripts/00_acquire_prepared_vtec.py` | Position 00; `--config configs/`; `ensure_process_determinism` first statement (AST-pinned); six-step stage entry; `assert_no_raw_fields` before first write — **governance-guards' completeness checker now checks a real population (skip branch retired)**; started/aborted/completed registry rows; missing months as machine-readable manifest fields; no `locked_test` import (test-pinned) |
| `tests/test_acquisition.py` | 47 tests — every Step 1–4 negative control + R-31 reaffirmation; holds no restricted-root literal (boundary composed from imported `RESTRICTED_ROOT` against tmp_path via documented seam) |
| `governance/CHANGE_RECORD_2026-09-05_R33_write_restricted.md` | The Q1=A change-control acceptance: interface amendment to `locked_test.py` (`write_restricted`, shared `_append_and_flush`, `AccessRecord.purpose` enum extension), citing R-33/BLK-07, ruling 2026-09-05 |

## Files modified in place

| Path | What |
|---|---|
| `src/data/locked_test.py` | Q1=A acceptance built: `write_restricted` sibling of `open_restricted` — **logs durably first (shared `_append_and_flush`), then writes**; refuses uncharacterised platforms (before any row), non-`acquisition_write` purposes, ordinary paths, existing targets (never overwrite); boundary from `_repo_root()` (one home both directions; `open_restricted` refactored onto it, behaviour unchanged); `PURPOSES` extended to 5 (`acquisition_read`, `acquisition_write`) with change-record citation. Exempt list untouched at **7** |
| `src/data/config.py` | `REQUIRED_FIELDS_MAP` gained `("acquisition", 1)` — designed extension point, field identities only (`data.acquisition.experiment|kindat|parameters`, `seeds.development`); the script now **refuses at the §18.3 preflight until D-144's frozen set is transcribed into `data.yaml` by its owner**. No governed config touched |
| `.githooks/pre-commit` | Step 1b: staged-`.ipynb` saved-output refusal reading the **staged blob** (`git show :path`) through the module CLI; fails closed on violations, unparseable notebooks, and absent python; no auto-strip |

## Test and lint results (smoke evidence only — never governed)

- **Full suite: 497 passed, 2 skipped, 0 failed** — Python 3.11.9; **re-run independently by the orchestrating session, same counts.** New module: 47 passed. Guard trio (`test_acquisition_window` + `test_locked_test_guard` + `test_phase_contract`): 101 passed with the new files in place — exempt list still 7, literal scan green, producing-script completeness check now exercising its real branch.
- `ruff check`: all checks passed on the five touched files; three new files `ruff format`-clean. (12+ pre-existing files fail `ruff format --check` tree-wide — pre-existing, untouched.)
- Hook CLI smoke: current workspace notebook exits 0; dirty fixture exits 1 naming cells; unparseable exits 1 fail-closed.

## Key decisions

1. Release-side refusals (`assert_release_free_of_unresolved_mismatch`, `assert_derived_release_provenance`) live in `acquisition.py`; `release.py`'s `identity_fields`/`suffix_mismatch` amendments stay **owed and unbuilt** (R-35/R-34 open items; `provenance_class` fifteenth-field seam routed to G-P1A/3.2). Guard-home split stated in the guard's docstring (nfr-design c58).
2. `AccessRecord.purpose` already existed; the **enum** gained the two acquisition values per R-33/Q2=C — existing rows/tests green.
3. `CREDENTIAL_NAME_MAP` left empty; Madrigal-identity question stays supervisor-owned, no reading adopted.
4. `_build_transport` refuses with a recorded reason — no live provider client (network blocked; re-acquisition is deferred DATA-07 work).
5. Heuristic width stated so provider filenames pass and hex/base64 secrets do not; sha256/UUID/commit-hex via named allowlist.

## Deviations

- graphify CLI unavailable — graph stale for touched files; `graphify update .` owed.
- `evidence/test_run_access_log.jsonl` grew during suite runs — pre-existing designed behaviour of guarded test reads, not a change by this pass. No production access-log path is defined anywhere yet — **flagged for the gate** if a dedicated path is wanted.
- No `python` on system PATH, so the pre-commit hook fails closed on this machine — its designed posture.
- `notebooks/00_acquire_phase1_vtec.ipynb` does not exist and was not created (D-144 approved as-is; the equivalence test attaches when it exists).

## Governance stop — owed before any commit (student acts; cumulative with prior units)

- `CHANGE_RECORD_2026-09-05_R33_write_restricted.md` **exists** (written this pass, before any commit).
- TE §12 naming amendment for `src/data/acquisition.py` — third new-module amendment this Bolt (after `experiment_registry.py`, `phase_contract.py`).
- Commit cites **D-144, D-15, D-5/D-10.2** as touched decisions.
- BLK-07's authorization limb stays **open** (mechanism built; closure is 3.1-owned). R-32 named accessors and R-35 `identity_fields` remain owed. **No acceptance row discharged: TA-16, TA-31, TA-32, TA-08, TA-15 stay `Pending`; the 7 rowless requirements stay `UNTESTED`.**

## Review — 2026-09-05 (code-generation, iteration 1)

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T13:18:38Z
**Iteration:** 1

### Findings

| # | Severity | Where | What | Recommended action |
|---|---|---|---|---|
| 1 | Major | `scripts/00_acquire_prepared_vtec.py` `_registry_row` (lines ~202-230); `src/data/experiment_registry.py` (no `guard_egress` reference anywhere in the file, confirmed by repo-wide grep) | `acquisition.py`'s own docstring (Purpose item 1) and `write_request_manifest`/`write_sha256_manifest`'s docstrings claim "one declared chokepoint every value this unit writes to a manifest, **log** or notebook output passes through." The experiment-registry row this unit's own script writes (`notes`, `reason` on the `aborted` branch — `reason=str(exc)`) is a log this unit writes, and it is composed and handed to `append_registry_event`/`record_abort_honestly` with **no call to `guard_egress`/`guard_egress_value` anywhere on that path** — confirmed by grepping every use of `guard_egress` in the tree: all seven call sites are internal to `acquisition.py`'s own two manifest writers and the `RetrievalClient.retrieve` record; `experiment_registry.py` contains no redaction call at all. Today this is inert (`notes` is built from the static `retrieval_policy()` dict; `reason` is `str(exc)` on a project-authored `IntegrityError` whose message text is hand-written, and `CredentialEgressError`'s own message already omits the raw value by design) — but it is a real, verified second path into a written log that bypasses the declared chokepoint, exactly the "guard fails open on a forgotten call site" shape `project.md`'s own learned corrections (`nfr-design:c58`, `c59`) were written to catch: the moment `_build_transport` is wired to a live provider (the unit's own stated deferred work), a transport exception's `str(exc)` — which may embed the request URL, response headers, or provider error bodies — reaches the registry `reason` field unredacted. | Either (a) route `reason`/`notes` (and any other free-text registry field this stage populates) through `guard_egress_value` before constructing the row, or (b) narrow the docstring's claim to name its actual scope (the two manifest writers and the retrieval record) so the unit's stated invariant matches what the code enforces. Flag as an owed item alongside the unit's already-tracked R-32/R-35 amendments if deferred. |

### Verified and held (adversarial checks that found no defect)

- **December/restricted discipline**: repo-wide, tool-derived AST literal-fold scan (`tests/test_locked_test_guard.py::test_restricted_literal_holders_are_exactly_the_enumerated_exemption` and `::test_exempt_list_membership_is_rederived_exactly`, both re-run and PASSED) confirms `src/data/acquisition.py`, `scripts/00_acquire_prepared_vtec.py` and `tests/test_acquisition.py` hold no restricted-root literal, and the exempt set is still exactly the same 7 modules (none of this unit's new files added). Manual grep of `tests/test_acquisition.py` confirms no `evidence/locked_test_restricted` construction and no real December date literal outside prose/test-data strings dated 2022-11/12 used only as *input* to negative controls.
- **`write_restricted` ordering**: re-ran `tests/test_acquisition.py`'s Step-4 negative controls independently — failed log append aborts with no byte written (`test_failed_log_append_aborts_the_write_with_no_byte_written`), uncharacterised platform refused before any row (`test_uncharacterised_platform_refuses_the_write_before_any_row`), non-`acquisition_write` purpose refused (`test_a_read_purpose_is_refused_on_the_write_path`), existing target never overwritten (`test_an_existing_restricted_target_is_never_overwritten`). Exempt list confirmed still 7 (see above).
- **Completeness-before-hash / divergence**: `test_truncated_stream_never_yields_a_manifest_row_with_a_hash` and `test_divergent_rerun_records_both_and_refuses_to_overwrite` re-run and pass; code inspection confirms the incomplete branch returns before any `hashlib.sha256` call and writes no destination file.
- **Serializer coverage on its own declared surface**: `write_request_manifest`/`write_sha256_manifest`/`RetrievalClient.retrieve` all call `guard_egress` on their full payload before returning/writing (confirmed by reading the call sites), and `test_manifest_writer_refuses_a_credential_and_writes_nothing` confirms nothing is written on refusal. (Coverage gap on the registry-log path is Finding 1.)
- **Script contract**: `ensure_process_determinism` is confirmed the literal first statement of `main()` by an AST-based test (`test_stage_script_opens_main_with_ensure_process_determinism`, re-run, passed — not merely claimed); `assert_no_raw_fields` is called before the first write in `_run()` (`_assert_phase1_field_contract()` is the first line); the six-step stage-entry order in `_stage_entry` matches the docstring; no `locked_test` import (`test_stage_script_takes_config_and_never_imports_the_restricted_guard`, re-run, passed, and independently confirmed by direct read of the import block); `configs/data.yaml` carries no `acquisition:` section, so `assert_no_tbd` genuinely refuses at preflight rather than being fed a filled value.
- **`config.py` edit**: `REQUIRED_FIELDS_MAP[("acquisition", 1)]` adds field *identities* only (`data.acquisition.experiment|kindat|parameters`, `seeds.development`) — no value, no scientific constant, confirmed by reading the full diff region.
- **Hook**: `.githooks/pre-commit` reads the staged blob via `git show ":$nb"` (not the working tree), fails closed when `python` is absent, and performs no auto-strip — confirmed by direct read.
- **Claim honesty / plan-vs-disk**: all 9 plan steps have matching on-disk work; no acceptance row is claimed anywhere in the produced artifacts; `governance/CHANGE_RECORD_2026-09-05_R33_write_restricted.md` faithfully reflects the receipted Q1=A ruling in `code-generation-questions.md` (scope, "what this record does NOT cover," and owed-list entries all match; no wider claim made).
- **Suite/lint integrity, independently re-derived**: full suite re-run under the pinned Python 3.11.9 interpreter: **497 passed, 2 skipped, 0 failed** (both skips pre-existing and unrelated to this unit: `test_phase_boundary.py` and `test_release_contract.py`) — matches the claimed count exactly. `tests/test_acquisition.py` alone: 47 tests collected, all passed — matches the claimed "47 tests." Guard trio (`test_acquisition_window.py` + `test_locked_test_guard.py` + `test_phase_contract.py`): 101 tests collected, all passed — matches the claimed "101 passed." `ruff check` and `ruff format --check` both clean on the three new/modified files — matches the claimed "ruff clean."

### Coverage limits

This pass verified the `acquisition` unit's own artifact set and the two named sibling carve-outs (`governance-guards`' and `foundation`'s cited security-design sections, read only where this unit's design names an integration point). It did not re-audit `foundation`'s or `governance-guards`' own prior-pass code beyond the specific call surfaces this unit's new code touches (`resolve_platform_roots`, `CHARACTERISED_DURABILITY_PLATFORMS`, `IntegrityError`/`ReleaseError`/`LockedTestError` hierarchy, `append_registry_event`/`record_abort_honestly`). No live-network or Kaggle-platform execution was exercised (none is possible in this environment; `_build_transport` deliberately refuses).

### Summary

One Major finding: the redaction chokepoint's own docstring claims coverage of "every value this unit writes to a manifest, **log** or notebook output," but the experiment-registry log row this unit's script constructs bypasses `guard_egress` entirely — a verified, currently-inert gap that becomes live the moment the deferred live-transport work lands. Every other adversarial angle (December/restricted discipline, write-ordering, completeness-before-hash, script contract, config edit, hook, claim honesty, suite/lint counts) was independently re-derived and held. One Major and zero Critical findings.

**Verdict: READY**

### Cross-unit edit record (2026-09-10) — edits made by `fixtures-and-reproducibility`, owner-authorised

Appended after the gate rejection lifted the receipt freeze, so this summary does not
misdescribe the on-disk script. Under `CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY`
(§5, §6.1, §11.5; the owner's "apply the recommended option" ruling), the fixtures unit
made these ADDITIVE edits to this unit's surfaces — nothing on the full-year path changed:

- `src/data/acquisition.py` (commit `64c0551`): one public predicate
  `assert_records_within_window(records, *, start, end, timestamp_key)` on the same private
  date reader as `partition_by_locked_month`, so the record-date window rule has ONE home.
- `scripts/00_acquire_prepared_vtec.py` (commit `cf3185d`): `--fixture-manifest` option (the
  visible Q5 = A exemption carrier), `_stage_entry(..., fixture_manifest=None)` kwarg, and
  ONE `require_receipts_for_snapshot` call after `assert_lock_complete` (TE §9.2's
  two-receipt gate; exempt on a fixture run).
- `scripts/00_acquire_prepared_vtec.py` (commit `0e002cd`, board Rec 2 / ML-01):
  `_declared_data_window` reads `configs/data.yaml`'s `acquisition.window_start`/
  `window_end` (STRUCTURAL field names on this unit's config surface — the VALUES stay this
  unit's owner's to transcribe) and binds the fixture exemption to the scope's cited
  window; undeclared → the fixture exemption refuses naming the fields (TE §18.3).

Tests live in `tests/test_clean_run.py` (`test_rec2_00_...` and the Q5 controls). This
unit's owner may confirm or reverse per the change record.
