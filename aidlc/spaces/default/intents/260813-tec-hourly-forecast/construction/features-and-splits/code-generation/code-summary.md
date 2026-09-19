# Code Summary — `features-and-splits`

**Unit** `features-and-splits` (Bolt 7) · **Kind** `library` · **Stage** `code-generation`
**Plan**: `code-generation-plan.md` — all 10 steps executed, checkboxes marked. This stage made no `git commit` (governance stop, Step 10) — but see § Repository state below: a commit by the repository owner, made while this pass ran, does exist and does not meet the commit-message rule.
**Rulings built under** (receipted in `code-generation-questions.md`): Q1 = A (R-74 approved as the BLK-04 contract), Q2 = A (R-83 approved as the BLK-09 amendment), Q3 = A (separate permitted-producer loader; `ConfigSnapshot` untouched), Q4 = A (BLK-08 deferred per D-27). The change record recording all four was written FIRST, before any module.

## Files created

| Path | What |
|---|---|
| `governance/CHANGE_RECORD_2026-09-05_R74_R83_leakage_contracts.md` | Record `CR-2026-09-05-R74-R83-LEAKAGE-CONTRACTS`: owner approval of R-74 (ADR-11 train-only fitting contract — identity check, the single enumerated `REFIT`→`DEC`/`role="score"` exception, `fit_transforms`' four raises, untransformed bundles never consumable) and R-83 (`Partition.train_start` + `train_end` both from `configs/data.yaml`, strict-subset control) as the governed BLK-04 / BLK-09 contracts; Q3 = A accessor decision; BLK-08 deferred per D-27. Blocker-register annotations routed to the gate, not applied (register lives in an approved Inception artifact). Propagation-sweep table lists every site found and marks each "not edited — frozen receipt / gate item". Owed list includes the commit citing D-27, D-28, D-10.3 |
| `src/data/splits.py` | F-3: `PartitionKind`, `Partition` (both bounds per R-83, `validation_month`, `embargo_hours` with NO default), `PARTITION_IDS` / `FITTING_PARTITION_IDS`, `build_partitions(snapshot)` — reads `data.partitions` + `experiment.embargo_hours`, refuses absent/`TBD — freeze gate` naming the field, returns exactly six (`F1`…`F4`, `REFIT`, `DEC`), kind/id agreement, fold contiguity, `DEC.train_end == REFIT.train_end` (structural December-fit bar), exactly one evaluation ROLE per study month (overlap and gap both fail), one study origin; `embargo_exclusions` / `apply_embargo` (excluded AND counted); `build_split_manifest` / `assert_split_manifest` (exactly five rows; six fails, four fails, missing fold count fails); `locked_partition_record` kept separate from the manifest; `assert_membership_from_timestamps` (validates from record timestamps, derives nothing); `verify_g05_signature`; `materialise_locked_partition(snapshot, *, g05_signature, loader=None, …)` — `LockedTestError` on `None`, on failed verification, and when no loader is supplied (execution limb only; the read limb stays `open_restricted`'s). No calendar year, month number or embargo length appears in source |
| `src/features/availability.py` | F-1: `AvailabilityRow` (the six approved fields plus `anchor_policy`, `latency_statement`), `read_availability_lags` (TBD refuses), `build_availability_matrix`, three limbs — `assert_lags_safe` (limb 1: actual lag ≥ declared safe lag, backfill refusal, anchor-record presence), `assert_trailing_not_centered` (limb 2), `assert_anchor_recomputed` (limb 3: anchor equals the safe-lagged day AND the trailing mean is recomputed from that anchor via `spaceweather.trailing_mean` and compared within the configured tolerance) — plus `assert_release_status_not_backfilled`, `assert_dst_diagnostic_only` |
| `src/features/build.py` | F-2: `FrameSpec` (end-exclusive `scored_end`), `FeatureBundle` (+ defaulted `provenance`, `identity`, `excluded_counts`, `standardized_columns`, `sequence_columns`, `tensor_features`), `SECTION_6_2_ROWS` (row identities), `load_feature_dictionary`, **`load_permitted_producers(source)`** (Q3 = A: reads `configs/features.yaml`'s `permitted_producers` block from the configs dir or a `ConfigSnapshot`; unset/incomplete → `LeakageError` naming WHICH §6.2 rows lack entries; no feature matrix produced), `assert_producers_cover`, `validate_spec`, `assert_transform_identity` (one enumerated exception), `_support_admitted` (R-78: default-exclude, approval id, timestamp precedes freeze, lag ≥ 1, target-hour quality permanently forbidden), `build_features` (refusal order spec → identity → dictionary → producers → registry → window; closed dictionary — outside-dictionary name raises, `iri_*` raises, raw longitude raises; `AlignmentError` via `spaceweather.assert_alignment`; provenance key set == column set both directions), `bundle_directory_name`, `write_bundle` / `load_bundle` (`<partition_id>__<role>__<transform_id>/` with `matrix.parquet`, `tensor.npy`, `spec.json`; load reads all three or raises; refuses without `pyarrow`, naming the unpinned dependency) |
| `src/features/transforms.py` | F-4: `Transform` (id + `partition_id` + fitted state; no `apply`/inverse public surface — Q4 = A), `FieldClass` (six members), `fit_transforms(bundle, *, partition)` — `PartitionError` on id disagreement, `LeakageError` on non-train role, already-transformed bundle, and scored range not exactly `[train_start, train_end + 1 d)` in either direction; `apply_fitted_transform` (intra-package, called only by `build_features`), `assert_consumable` (`transform_id is None` never consumable), `carry_forward` (field class a REQUIRED argument; only `driver` reaches the bounded carry-forward; `vtec_lag_*` rejected), `assert_field_classes_partition` |
| `src/features/windows.py` | `read_window_length` (TBD refuses; must equal the dictionary's `sequence_steps`; grid placement fails — no `24` literal in source), `assert_window_length_grid_free`, `build_windows` (one definition emitting both representations, exclusions counted), `assert_window_parity` (two ordered assertions: shape/ordering precondition, then value-level reconstruction; `tolerance=None` stops naming the TE §15.2 fixture-manifest field), `ComparisonMask` / `build_comparison_mask` / `assert_mask_is_comparison_wide` / `write_mask` / `load_mask` (computed once per comparison set, three ID stamps) |
| `src/features/_frames.py` | Private intra-package frame/tensor helpers: pandas/numpy when importable, `RecordFrame`/nested-list fallback otherwise. Not enumerated in TE §12's tree (naming amendment owed, same class as `acquisition.py`) |
| `scripts/05_build_features_and_splits.py` | Position 05; six-step entry (`ensure_process_determinism` first, `assert_no_raw_fields` before first write — passes the R-24 checker in `test_phase_contract`); producer refusal checked FIRST — `load_permitted_producers` over the closed `SECTION_6_2_ROWS` identity table, before the feature dictionary is read (which is itself `TBD — freeze gate` today), then `load_feature_dictionary`, then a producer re-check over the dictionary-derived rows, then partitions, then availability (order corrected at review iteration 2); honest `aborted` registry row via foundation's `record_abort_honestly`; `--partition` choices exclude `DEC`; no December path |
| `tests/test_split_embargo.py` | §12-mandated. 34 test functions (36 cases): exact boundaries, embargo excluded-and-counted, manifest row counts 4/5/6, strict-subset control, DEC structural bar, exactly-one-role overlap/gap, membership-from-timestamps, no `sklearn` splitter and no calendar constant in `splits.py` source. Authors the **M10 synthetic fixture** (`synthetic_partition_block`, `synthetic_snapshot`, `synthetic_partitions`, synthetic year 2001 with R-80's month layout) reused by the other two modules |
| `tests/test_train_only_transforms.py` | §12-mandated. 28 test functions: full-dataset fit raises, train-role bundle at evaluation fails, cross-partition transform fails, untransformed consumer fails, strict-subset and over-wide and one-row-off ranges fail, DEC fit fails; the 30-condition M10 enumeration derived in-test (36 ordered pairs − 6 identities = 30; 1 exempt `REFIT`→`DEC`; 29 raise + 1 passes = 30), `PartitionError`-vs-`LeakageError` discrimination, carry-forward boundary, entry-point refusals through `build_features` |
| `tests/test_feature_availability.py` | §12-mandated. 54 test functions: three limbs each with negative controls (incl. same-day F10.7 through the trailing mean caught by the anchor recomputation), backfill, documented absence, Dst diagnostic-only, SSN identifier scan over `src/`, closed dictionary (`iri_*`, raw longitude, removed row, outside row), producer refusal naming rows (incl. against the real `configs/`), R-78's four rules, grid-free window, one-definition parity, `build_features` happy path over synthetic records, unpermitted producer, absent provenance, `AlignmentError`, registry block, comparison mask |

## Files modified in place

| Path | What |
|---|---|
| `tests/test_locked_test_guard.py` | Additive only (+190 lines): two-unit ownership block in the docstring (read limb — `governance-guards`; execution limb — `features-and-splits`); new section 9 with 8 limb-1 tests (signature `None` refused before any read; invalid signature refused; unsigned/TBD gate record never verifies; no read path owned by `splits.py`; a verifying synthetic signature materialises with embargo excluded and counted; wrong-month row refused by timestamp; the real `data.yaml` carries no G-05 record; `splits.py` holds no restricted-root literal). Existing cases untouched; the exact exempt-set derivation still passes at seven |
| `src/data/config.py` | `REQUIRED_FIELDS_MAP[("features-and-splits", 1)] = ("seeds.development",)` — deliberately minimal, same shape and comment discipline as the three sibling entries; the unit's own fields are enforced at their own entry points so the script's honest `aborted` row stays reachable. Identities only, never values |
| `configs/features.yaml` | `permitted_producers: "TBD — freeze gate"` — the block SHAPE Q3 = A reads, with comment. The LIST stays unauthored (assigned to nobody — gate item). Writing the sentinel is not choosing a value (W-9) |
| `evidence/test_run_access_log.jsonl` | +37 rows appended by running the EXISTING suite (routed restricted reads the existing tests log by design). Not reverted — access records are never deleted — and flagged for the gate |
| `code-generation-plan.md` | Ten checkboxes ticked; no other line changed |

## Test and lint results (smoke evidence only — never governed)

- **Interpreter**: Python 3.11.16 (uv-managed, bootstrapped in the session scratchpad, outside the repo). PyPI is unreachable from this machine (uv and curl both time out), so **none of the pins in `requirements.txt` could be installed**: no pandas, numpy, pyyaml, pytest or ruff.
- **Test execution** therefore ran through a stdlib pytest stand-in (scratchpad `shim/pytest.py`, outside the repo) supplying `raises` / `skip` / `importorskip` / `mark.parametrize` / `fixture` / `tmp_path` / `monkeypatch`. The new modules take their stdlib fallback representations (`RecordFrame`, nested lists) only when pandas/numpy are not importable; governed environments get the governed types.
- **Owned modules under the shim**: `test_split_embargo` 35 passed / 1 skipped (yaml absent); `test_train_only_transforms` 28 passed; `test_feature_availability` 53 passed / 1 skipped (yaml absent); `test_locked_test_guard` 44 passed (8 new + 36 existing).
- **Whole suite under the shim**: 813 passed / 37 failed / 4 skipped across 20 modules. Every one of the 37 failures is environmental — 34 need `yaml` (`test_determinism` 22, `test_external_drivers` 12 incl. subprocess runs of script 04), 3 need `pytest.approx`, 1 needs `capsys` (both shim limitations). None involves the new or edited code. The prior 449 passed / 3 skipped baseline was counted by real pytest and is **not comparable**.
- **Independent check (orchestrator)**: `grep -c '^def test_'` over the four test files gives 34 / 28 / 54 / 34 test functions (the shim's 44 for `test_locked_test_guard` counts parametrised and class-held cases); no `2022` or `2001` literal in `src/data/splits.py`; no `src.external.iri` / `src.external.gim` / `sklearn` / `src.evaluation` import anywhere under `src/features/` or in `splits.py` (the only hits are docstring sentences stating the rule).
- **ruff was NOT run** (not installable). A stdlib substitute checked line length ≤ 99, trailing whitespace and unused imports over all touched files (0 problems). `ruff format` was NOT applied. `ruff check` and `ruff format --check` are owed the first time the pins are installable.
- The two yaml-skipped tests (`test_real_repository_configs_refuse_today`, `test_permitted_producers_reads_the_real_features_yaml_and_refuses_today`) execute the real-`configs/` refusal paths once `pyyaml` is present.

## Key decisions

1. **Refusal order in `build_features`** is spec → identity → dictionary → producers → registry → window. Producers are the first refusal reachable in production (SD-F-01): the script checks them against the §6.2 row identities before it reads the feature dictionary or builds partitions, so the honest `aborted` row names that reason even while the dictionary is also unfrozen (review iteration 1 found the dictionary refusal firing first; fixed).
2. **`Partition.embargo_hours` has no default**: the approved `= 24` is a scientific constant in source (`project.md` § Forbidden); the value enters from `experiment.embargo_hours` only.
3. **"Window length equals 24"** is asserted as agreement between two frozen config values (`experiment.window_length_hours` and the dictionary's `vtec_seq_24.sequence_steps`) plus grid absence; no `24` literal in source.
4. **`FrameSpec.scored_end` is end-exclusive**, so range equality against `[train_start, train_end]` needs no cadence constant.
5. **Calendar values live nowhere in source or tests**: the M10 fixture uses a synthetic year (2001) with R-80's month layout, and a test asserts neither `2022` nor `2001` appears in `splits.py`.
6. **`FieldClass` has six members** (driver, target, station, time, support, diagnostic); R-77's two-class rule is realised as "exactly one class per field" over the whole enum, because TE §6.2 carries station/time/support/diagnostic rows that are neither driver nor target.
7. **`load_permitted_producers(source)`** accepts the configs directory (the ruled signature) or a `ConfigSnapshot` (the same parsed, hashed file); `build_features` passes the snapshot. `ConfigSnapshot`'s eight approved fields are untouched.
8. **`write_bundle` refuses when `pyarrow` is not importable**, naming the unpinned dependency: TE §8.1 requires Parquet, `requirements.txt` carries no pin, and no pin was added by convenience.
9. **`tests/test_feature_leakage_guards.py` (R-76a / TA-36 primary test) was NOT built** — the approved plan's Step 8 does not list it. R-76a's enforcement raise (`AlignmentError`) IS implemented in `build_features` with a control in `test_feature_availability.py`; the module itself remains owed.
10. Exceptions are raised from foundation's hierarchy in `src/data/config.py` (`LeakageError`, `PartitionError`, `LockedTestError`, `FeatureAvailabilityError`, `AlignmentError`, `PreflightError`); none redefined.

## Deviations

- **Approved-signature deviations, recorded as amendment candidates against `component-methods.md`**: `Partition.embargo_hours` without default; `assert_membership_from_timestamps(frame, *, partition, role, timestamp_column)`; `materialise_locked_partition(..., loader=None, partitions=None, timestamp_column=...)`; `build_features(..., parity_tolerance=None, timestamp_column=..., station_column=...)`; additive defaulted fields on `FeatureBundle` and `AvailabilityRow`. All additive or keyword-only; no approved positional signature changed.
- `src/features/_frames.py` is a fifth (private) module TE §12's tree does not enumerate — naming amendment owed.
- Calendar encodings use hours-per-day, degrees-per-hour and days-in-year as arithmetic facts inside `_time_features` / `_station_features`; flagged so a reviewer can rule they are not TC-03e constants.
- `SECTION_6_2_ROWS` holds TE §6.2 row identities in source (incl. the name `vtec_seq_24`), on the `REQUIRED_FIELDS_MAP` identities-not-values precedent.
- `configs/features.yaml` gained the `permitted_producers` sentinel block (shape only) — permitted by Q3 = A's reading of that block from `features.yaml`; no list authored.
- Test execution through a stdlib stand-in rather than pytest, and no ruff run — environmental, stated above; nothing here is governed evidence.
- The developer's brief named the four rule files by path (they also reach the agent through the project CLAUDE.md imports) instead of pasting the rule text verbatim — recorded in the stage diary.

## Governance stop — owed before any commit (student acts; cumulative with prior units)

- **Step 10 items, restated**: blocker-register annotations in `unit-of-work.md` for BLK-04 (contract approved; evidence limb still open at G-04/G-05), BLK-09 (approved), BLK-08 (deferred, narrowed to `ABL-DIFF` per D-27) — annotate-in-place needs the owner there; the permitted-producer LIST needs an owner and a TC-03e classification; the evaluation-ROLE exactly-one reading of Vision §8.1 (adopted so the check can run, not settled); FR-P1-04-10's proposed-not-approved acceptance row; the R-84/R-103 `load_inverse`/`load_transform` naming divergence (evaluation-and-comparison's pass); WS-13's TE §16 criterion reading (parity built, no reading adopted); the governed commit citing **D-27, D-28, D-10.3** — the change record exists first; neither the developer nor the orchestrator committed (see § Repository state for the owner's commit that exists instead).
- **New items from this pass**: the `pyarrow` pin (reviewed change to `requirements.txt` before any bundle can be persisted); `tests/test_feature_leakage_guards.py` unbuilt (TA-36 primary test; a §12 tree question); the `_frames.py` naming amendment; the approved-signature deviations above; the 37 appended access-log rows; R-80's calendar values still owed to `configs/data.yaml` at their freeze; the fixture-manifest tolerance for WS-13's value limb; `ruff check` / `ruff format --check` and a real `pytest -rs` under the pinned environment.
- **Nothing discharged**: WS-10, WS-11, WS-12, WS-13, WS-18, TA-07, TA-08, TA-11, TA-18, TA-33, TA-34, TA-35 all stay `Pending`; FR-P1-04-10 stays rowless. No feature matrix or mask artifact was produced (the permitted-producer refusal is the deliverable). No December content, restricted-root path or real signature was touched by any new test; the restricted-literal exempt set is unchanged at seven.

## Repository state — an owner commit exists (correction after review iteration 1, Major 1)

Derived from `git log` / `git reflog` / `git show --stat` on 2026-09-06, not from prose:

- HEAD is **`6246907d6d87c16f08952773184fb2f194e0eac4`**, author `Kimrza <kiimiiarezaee2025@gmail.com>`, committed 2026-09-06 14:58:39 +04:00 — about one hour after `06207c4` (same author, 13:58:47 +04:00) and while the developer's generation pass was running. The reflog shows both as ordinary `commit:` entries on this clone; no framework tool, hook or agent in this stage ran `git commit` (the developer's return and the orchestrator's own actions are both on record as making none; `.githooks/pre-commit` and the framework tools that mention git do not commit).
- Its message is the **unedited git commit template** ("Please enter the commit message for your changes. …") and cites **no D-number**. It touches `configs/features.yaml` (a governed config) plus every file this pass created or edited, `evidence/test_run_access_log.jsonl`, the change record, this summary, and the whole `graphify-out/` cache — **286 files, +573635 / −83202**.
- `team.md` § Way of Working requires any commit that changes a governed config value to cite its D-number; the change record (`governance/CHANGE_RECORD_2026-09-05_R74_R83_leakage_contracts.md`) names **D-27, D-28, D-10.3** as the citations the governed commit owes and states the commit is the student's act. The existing commit satisfies neither.
- **Disposition is the owner's ruling, not this stage's**: either amend/redo `6246907` with a message citing D-27, D-28, D-10.3 (and consider excluding the `graphify-out/` cache), or record that the placeholder-message commit stands and why. Routed to the human at the first available turn; nothing here reverts, amends or re-commits.

## Iteration 2 — both iteration-1 Majors addressed (2026-09-06, same session)

The reviewer's iteration-1 section below is left standing; its NOT-READY verdict predates these changes.

- **Major 1 (repository state contradicted the "no commit" claim)** — the claim was corrected, not the repository: § Repository state above records commit `6246907` from `git log` / `reflog` / `show --stat` (owner's commit, template message, no D-number, 286 files) and routes its disposition to the owner. No revert, amend or re-commit was made by this stage.
- **Major 2 (refusal order in script 05)** — `_run()` now calls `load_permitted_producers(args.config, dictionary_rows=sorted(SECTION_6_2_ROWS))` first, then `load_feature_dictionary`, then the dictionary-derived producer re-check; docstring and `# 1.` comment state the true order; `SECTION_6_2_ROWS` added to the import list. Diff: one file, 14 insertions / 3 deletions. `py_compile` OK. Under the same shim (smoke only): `test_phase_contract` 36 passed (R-24 checker still satisfied — `assert_no_raw_fields` remains the first statement of `_run()`), `test_split_embargo` 35 + 1 skipped, `test_train_only_transforms` 28, `test_feature_availability` 53 + 1 skipped, `test_locked_test_guard` 44. `git log -1` still `6246907`; no commit made.
- Riding suggestion (the `raising` counter's bookkeeping in `test_identity_check_enumeration_has_exactly_thirty_raising_conditions`) NOT applied — gate input, quoted at the gate.

## Review — 2026-09-06 (code-generation, iteration 1)

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-06T11:04:36Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | Repository HEAD (`6246907d6d87c16f08952773184fb2f194e0eac4`); this file line 4 ("No `git commit`... Step 10") and line 68/70 ("no commit was made") | This artifact's own governance-stop claim is false as of the state under review. `git log -1` shows HEAD is **not** `06207c4` as the review brief instructs checking for — a further commit `6246907` exists, made one hour after `06207c4`, whose diffstat is exactly this stage's deliverable (`src/data/splits.py`, all five `src/features/*.py` files, `scripts/05_build_features_and_splits.py`, all four touched/new test files, `configs/features.yaml`, `evidence/test_run_access_log.jsonl`, the change record, and this summary itself — 286 files, +573635/-83202). The commit message is the **unedited git template placeholder** (`"Please enter the commit message for your changes. Lines starting with '#' will be ignored..."`), citing **no D-number** at all. `team.md` § Way of Working requires: *"Any commit that changes a scientific constant, a config value (`data.yaml`, `features.yaml`, `experiment.yaml`, `seeds.yaml`), or another governed artifact must cite its D-number in the commit message"* — this commit touches `configs/features.yaml` and cites none. The change record itself (`governance/CHANGE_RECORD_2026-09-05_R74_R83_leakage_contracts.md:193-195`) states *"No governed commit before this record exists... the commit is the student's act, not the agent's"* and names the three D-numbers a compliant commit must cite — the commit that actually exists satisfies neither condition. Whether the agent or another process made this commit, the artifact under review asserts a governance stop that the repository's own history does not bear out, and no D-number-citing commit exists in its place. | Do not advance the gate on the current claim. Either (a) the commit is illegitimate and must be reverted/amended by the student with a message citing D-27, D-28, D-10.3 before any further stage proceeds, or (b) if the commit was intentional, `code-summary.md`'s "No git commit" claim and Step 10's "no commit was made" line must be corrected to state what happened and why the D-number citation is missing — either way this is a human decision, not one this review resolves. |
| 2 | Major | `scripts/05_build_features_and_splits.py:313-316`; `code-summary.md` line 18 ("producer refusal checked FIRST, then partitions, then availability") and line 45 ("Producers are the first refusal reachable in production (SD-F-01)") | Read against the real `configs/features.yaml` (all four legacy fields plus the new `permitted_producers` sentinel are `"TBD — freeze gate"`), the claimed refusal order does not hold. `_run()` calls `load_feature_dictionary(snapshot)` (`src/features/build.py`) *before* `load_permitted_producers(...)`; `load_feature_dictionary` raises `PreflightError` the instant `features.feature_dictionary` is the TBD sentinel (`build.py:274-281`) — which it is, today, in the real repository. So the actual first refusal a run hits against this checkout is the **feature-dictionary** TBD refusal, not the **permitted-producer-list** refusal the summary and the script's own docstring ("REFUSES, honestly, at the permitted-producer list... checked FIRST... the reason a reviewer must see on the aborted row") both name as what happens today. The two fields happen to be TBD together right now, so the run still aborts honestly either way, but the *stated* reason for the abort — the one the design says a reviewer "must see" — is not the one that will actually appear on the `aborted` registry row. | Either reorder the two calls in `_run()` so producers really are checked first (matching the stated design intent), or correct the docstring/summary to state the true order (dictionary, then producers) and stop claiming the producer refusal is "the first reachable in production" while the dictionary is also unresolved. |

### Verified — did not break

- `Partition`/`build_partitions`/`FrameSpec`/`Transform`/`FeatureBundle`/`build_features`/`fit_transforms` signatures checked directly against `component-methods.md`'s approved ADR-11 forms (lines 324-336, 513-579): every deviation (`Partition.embargo_hours` losing its `=24` default, `Partition.train_start` added, the additive keyword-only params on `assert_membership_from_timestamps`/`materialise_locked_partition`/`build_features`) is additive/keyword-only and is listed in the summary's own Deviations section — none found undisclosed. `ConfigSnapshot` (`src/data/config.py:470-485`) still carries exactly its 8 approved fields, untouched by this stage's diff (`git diff HEAD~2 -- src/data/config.py` shows only the one `REQUIRED_FIELDS_MAP` entry).
- R-74's four `fit_transforms` raises (`src/features/transforms.py:142-174`) traced against `business-rules.md:146` line by line: role≠train, transform_id≠None, and scored-range≠training-range all raise `LeakageError`; the declared-identity disagreement raises `PartitionError` — matches the rule's exception-class assignment exactly.
- `assert_transform_identity`'s single enumerated exception (`build.py:517-544`) is exactly `REFIT`→`DEC` under `role="score"`; `test_train_only_transforms.py::test_identity_check_enumeration_has_exactly_thirty_raising_conditions` derives 36 pairs / 30 mismatched / 1 exempt programmatically (not carried as a literal) and every non-exempt pair (both roles) is separately asserted to raise via `pytest.raises`, with the one exempt pair separately asserted to pass.
- No `2022`, `2001`, or bare freeze-gated-value literal (embargo hours, window length) in `src/data/splits.py`, `src/features/*.py` or `scripts/05_build_features_and_splits.py` — confirmed by direct grep; the `24`s and `360.0/24.0` present are hours-per-day/degrees-per-hour calendar arithmetic inside `_time_features`/`_station_features` (`build.py:697-738`), correctly flagged by the summary itself as a "rule a reviewer must make," not hidden as settled.
- `load_permitted_producers` (`build.py:389-458`) reads `configs/features.yaml`'s `permitted_producers` block through a path fully separate from `ConfigSnapshot`, refuses on the real sentinel with a `LeakageError` naming missing rows, and produces no feature matrix while unset — confirmed against the actual `configs/features.yaml` diff (`permitted_producers: "TBD — freeze gate"`, shape-only, no list authored).
- `assert_anchor_recomputed` (`availability.py:435-490`) recomputes the trailing mean from the recorded anchor via `trailing_mean` and compares within tolerance, distinct from `assert_trailing_not_centered`'s window-kind check; both are separate limbs as claimed. No centered-window path exists in the module.
- Embargo excluded-and-counted (`splits.py:459-476`, `520-530`); `build_split_manifest`/`assert_split_manifest` (`splits.py:536-611`) enumerate exactly the five fitting-capable ids and fail on six or four rows or a missing count; `DEC.train_end == REFIT.train_end` structural bar (`splits.py:351-357`) is asserted with no calendar constant.
- `materialise_locked_partition` (`splits.py:701-759`) refuses on `g05_signature is None` and on a failed verification, in that order, before any partition build or loader call; refuses again with no `loader` supplied — all three checked before any read. `tests/test_locked_test_guard.py`'s new section 9 runs entirely over a synthetic year/synthetic signature (confirmed: `SYNTH_YEAR`, no `2022` literal in the new block) and the pre-existing `RESTRICTED_LITERAL_EXEMPT_MODULES` (7 members, unchanged) and its other ~36 pre-existing test cases are untouched (diff is `+190` additive lines only, confirmed via `git diff --stat`).
- Import boundary: `grep` over `src/features/*.py` and `src/data/splits.py` for `iri`/`gim`/`sklearn`/`evaluation`/`models` imports found none; `Transform` exposes no `apply`/`inverse` public surface (Q4 = A).
- `assert_window_parity` (`windows.py:342-416`) runs the shape/ordering assertion unconditionally, then raises `IntegrityError` naming `TOLERANCE_MANIFEST_FIELD` (the TE §15.2 fixture-manifest field) exactly when `tolerance is None`, never silently passing the value limb.
- `scripts/05_build_features_and_splits.py`: `ensure_process_determinism` is the literal first statement of `main()`; `_assert_phase1_field_contract` (which calls `assert_no_raw_fields`) runs as the first line of `_run()`, before any write; the `aborted` registry row is written via foundation's `record_abort_honestly` on any `IntegrityError`; `--partition` choices are `FITTING_PARTITION_IDS` (excludes `DEC`); no call to `materialise_locked_partition` exists in the script.
- Counts independently re-derived, not taken from prose: `grep -c '^def test_'` gives 34 / 28 / 54 / 34 across the four test files (matches the summary's own "Independent check" line); running the four modules under the session's stdlib pytest shim (same shim path the developer used) reproduced **exactly** 35 passed/1 skipped, 28 passed, 53 passed/1 skipped, 44 passed — matching the summary's claimed shim results precisely. All eleven touched/created Python files pass `py_compile` under the session's uv-managed Python 3.11.16.
- `configs/features.yaml`'s diff is exactly the claimed 11-line `permitted_producers` sentinel block (shape only, no list); `src/data/config.py`'s diff is exactly the claimed single `REQUIRED_FIELDS_MAP` entry, comment-documented identically to its three siblings.
- `pyarrow` was not added to `requirements.txt`; `write_bundle` (`build.py:1091-1131`) refuses when `pyarrow` is not importable, naming it explicitly — no unpinned dependency was silently assumed.

### Coverage limits

- Could not execute `ruff check`/`ruff format --check` or the yaml-dependent tests (pyyaml unavailable in this environment either); relied on the same stdlib shim and manual grep/`py_compile` the developer used — smoke evidence only, as the summary itself states.
- Did not independently re-derive the R-77/R-78/R-83 rule text beyond the excerpts read from `business-rules.md`; spot-checked R-74, R-76a and R-83's headline text only, per the read-scope bound.
- Did not attempt to execute `scripts/05_build_features_and_splits.py` end-to-end (blocked by the same missing `pyyaml`/`pandas`); the refusal-order finding (#2) is a static trace of the call sequence and the real `configs/features.yaml` content, not an observed runtime abort.
- Did not read any sibling unit's `construction/<other-unit>/` content; cross-unit citations (R-92, R-103, R-104, D-27/D-28) were taken as stated in the passed `business-rules.md` excerpts and not independently verified against those units' own artifacts.
- Did not verify the `evidence/test_run_access_log.jsonl` +37-row claim by diffing the file (large, append-only JSONL); took the summary's count at face value for that item only.

## Review — 2026-09-06 (code-generation, iteration 2)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-06T11:12:23Z
**Iteration:** 2

### Findings

(none)

### Verified — did not break

- **Major 1 disposition (repository state).** Independently re-derived every fact in `§ Repository state` from `git`, not from the section's prose: `git show -s --format="%H|%an|%ae|%ai" HEAD` gives `6246907d6d87c16f08952773184fb2f194e0eac4|Kimrza|kiimiiarezaee2025@gmail.com|2026-09-06 14:58:39 +0400`; `HEAD~1` is `06207c4` at `13:58:47 +0400` (same author) — the stated "about one hour after" holds. `git show --shortstat HEAD` gives `286 files changed, 573635 insertions(+), 83202 deletions(-)`, matching exactly. `git reflog -5` shows both `6246907` and `06207c4` as ordinary `commit:` entries (not `commit (amend):`, not a merge, not a rebase artifact) with the unedited git template as the subject line, and no third entry between them — consistent with the section's claim that no hook or intermediate tool fired a commit of its own between them. `.githooks/pre-commit` exists but its own source contains no `git commit` invocation. `governance/CHANGE_RECORD_2026-09-05_R74_R83_leakage_contracts.md:193-195` does name **D-27, D-28, D-10.3** as the citations a governed commit owes, confirmed by direct read — the section's citation is accurate. The correction does not overclaim: it states the commit's *disposition* as routed to the owner ("either amend/redo... or record that the placeholder-message commit stands") rather than asserting the matter closed, and it does not touch, revert or amend `6246907` itself (`git status --porcelain` shows no staged changes to any file this stage's diff covers except `code-summary.md` and the script). This is the correct handling of a fact this stage cannot unilaterally resolve — Major 1 is adequately addressed as a correction-and-routing, not a code fix (none was available), and iteration 1's finding is otherwise fully accounted for.
- **Major 2 fix (refusal order).** `git diff HEAD -- scripts/05_build_features_and_splits.py` confirms the exact claimed change: one file, 14 insertions / 3 deletions. `_run()` now calls `load_permitted_producers(args.config, dictionary_rows=sorted(SECTION_6_2_ROWS))` as its first statement (before `load_feature_dictionary`), with `SECTION_6_2_ROWS` added to the `src.features.build` import list. Traced `load_permitted_producers`'s Path-branch (`build.py:407-458`) against this call shape: it reads only `configs/features.yaml`'s `permitted_producers` block, never touches `feature_dictionary`, and raises `LeakageError` on the real sentinel — so the permitted-producer refusal now genuinely fires before anything that could raise `PreflightError` on the dictionary, resolving iteration-1 finding #2 exactly as claimed. The second call (`load_permitted_producers(args.config, dictionary_rows=rows)`, after the dictionary loads) is unchanged from iteration 1 and still re-checks against the dictionary-derived rows, so a dictionary/row disagreement still surfaces as before. `SECTION_6_2_ROWS` (`build.py:136-155`) is a `Mapping[str, FieldClass]` of row-name identities to class identities; `sorted(SECTION_6_2_ROWS)` iterates its string keys only — no scientific value (a lag, a window length, a threshold) rides along, confirmed by reading the mapping's literal contents.
- **Re-verified, unchanged**: `py_compile` on `scripts/05_build_features_and_splits.py` succeeds. Re-run under the same stdlib shim: `test_split_embargo` 35 passed/1 skipped, `test_train_only_transforms` 28 passed, `test_feature_availability` 53 passed/1 skipped, `test_locked_test_guard` 44 passed — identical to iteration 1's counts, confirming the reorder touched nothing these suites exercise. `tests/test_phase_contract.py` (the R-24 producing-script completeness checker, distinct from `test_phase_boundary.py`) was additionally run this iteration and gives 36 passed/0 failed/0 skipped — `assert_no_raw_fields` (via `_assert_phase1_field_contract`) remains the literal first statement of `_run()`, ahead of both `load_permitted_producers` calls, so R-24's before-first-write obligation is untouched by the reorder.
- **No new overclaim found** in the iteration-2 passages (`§ Repository state`, `§ Iteration 2`, the reworded docstring/`# 1.` comment, and the reworded Step 10 line): every figure checked (HEAD hash, timestamps, 286/573635/83202, the three D-numbers, 14/3 diff, the four re-run counts) matches what the tools independently produced. The riding suggestion from iteration 1 (the `raising` counter) was confirmed NOT applied — `test_train_only_transforms.py` is byte-for-byte the same 28-function module as iteration 1 (same pass count, no diff against it in `git status`), consistent with the summary's statement that it stays gate input.

### Coverage limits

- Same as iteration 1: no `ruff`/`pyyaml`/`pandas` in this environment; the reorder's actual runtime abort message (which exception text a live run against the real, unpinned config would print first) was traced statically through `load_permitted_producers`'s source rather than observed end-to-end.
- Did not re-open sibling-unit content; did not re-verify the `evidence/test_run_access_log.jsonl` row count this iteration (unchanged since iteration 1, not touched by this pass's two diffs).
- Did not independently re-run the framework's own hook/tool inventory to confirm the negative claim "no framework tool, hook or agent in this stage ran git commit" beyond reading `.githooks/pre-commit`'s source and the reflog shape; this is corroborating evidence for the section's claim, not proof of it, and the section itself routes the underlying disposition to the owner rather than resting on that claim.

### Cross-unit edit record (2026-09-10) — edits made by `fixtures-and-reproducibility`, owner-authorised

Appended after the gate rejection lifted the receipt freeze. Under
`CR-2026-09-07-R133-FIXTURES-AND-REPRODUCIBILITY` (§5, §11.5; the owner's "apply the
recommended option" ruling), the fixtures unit made these ADDITIVE edits to
`scripts/05_build_features_and_splits.py` — nothing on the full-year path changed (current
size, derived: 610 lines, `wc -l`):

- Commit `cf3185d` (Q4/Q5 = A): `--fixture-manifest` option (a frozen `--partition`
  alongside it is a parser error — R-137's two-way quarantine), `_stage_entry` kwarg + ONE
  `require_receipts_for_snapshot` call after `assert_lock_complete`, and ONE early-return
  in `_run` reaching the additive `_run_fixture_scale`: the SAME three-call sequence over
  the scope's APPARATUS partitions (built by `build_apparatus_partitions`, never a frozen
  id), sibling fixture stamps on every bundle, and `apparatus_split_manifest.json` instead
  of the five-row confirmatory manifest. The permitted-producer refusal, dictionary,
  availability lags and release-root reads are UNCHANGED governed reads.
- Commit `0e002cd` (board Rec 4 / ML-03): the fixture path emits a machine-readable
  `fixture_measurements.json` under the bundle root (scored feature-window rows via
  `records_of(score.matrix)`) for the orchestrator's candidate-measurement folding; the
  orchestrator now passes `--bundles-out artifacts/walking_skeleton/<fixture_id>/features`.
- The M10 contract fixture (this unit's `test_train_only_transforms.py` +
  `test_split_embargo.py`) is invoked by `run_walking_skeleton.py` after the plumbing
  fixture (owner Q12 = C — clean-run evidence, never a third receipt), and R-137's
  must-not-fire November-containment control is credited to this unit's module by the
  fixtures suite's ledger (`MNF_HOSTED_ELSEWHERE`) rather than copied.

Tests live in `tests/test_clean_run.py`. This unit's owner may confirm or reverse per the
change record.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-10T11:33:57Z
**Iteration:** Owner-rulings implementation review (2026-09-10)

### Findings

None survive verification at any severity for this unit.

### Verification performed

- **`permitted_producers` (owner ruling 4: strict leakage-safe policy).**
  `configs/features.yaml` diff read in full: 11 of 18 rows filled
  (`vtec_lag`, `vtec_seq_24`, `target_support` → `phase1_hourly_target`;
  `utc_hour_sin/cos`, `doy_sin/cos` → `record_timestamp`; `lst_sin/cos`,
  `station_onehot`, `station_lat` → `station_registry`), 7 driver-class rows
  (`kp_safe`, `ap_safe`, `hp60_safe`, `ap60_safe`, `f107_safe`, `f107_81_trailing`,
  `dst`) deliberately unfilled. Cross-checked each producer id against
  `src/features/build.py` (this unit's own module, zero diff in this pass):
  `STATION_REGISTRY_PRODUCER = "station_registry"` (line 163) and
  `TIMESTAMP_PRODUCER = "record_timestamp"` (line 165) match exactly; `phase1_hourly_target`
  matches the release directory name `scripts/05_build_features_and_splits.py` and its
  siblings already read (`release_root / "phase1_hourly_target" / "release_manifest.json"`
  in `scripts/05_build_features_and_splits.py`) — a pre-existing artifact id, not invented.
  Confirmed `load_permitted_producers` (lines 389–458) and the per-column check at
  build time (lines 995–1015) genuinely gate the real code path: a computed `producer`
  value must be `in producers[row_id]` or the build refuses — this is live enforcement,
  not decorative config.
- **Three new tests in `tests/test_feature_availability.py`** (read in full):
  `test_permitted_producers_real_features_yaml_carries_exactly_the_contract_fixed_rows`
  performs a bidirectional set-difference against a hardcoded (not config-imported)
  11-row literal, so config and code cannot silently drift apart while the test still
  passes; `test_permitted_producers_still_fails_closed_on_every_deferred_driver_row`
  proves each of the 7 deferred rows still refuses by name;
  `test_permitted_producers_admit_no_removed_or_iri_or_longitude_row` proves `ssn`,
  `iri_vtec`, `glon`, `longitude` are all refused, and cross-checks
  `build.REMOVED_ROWS == frozenset({"ssn"})` (verified at `src/features/build.py:157`)
  disjoint from the 11 filled rows. Full-module run:
  `test_feature_availability: 54 passed, 0 failed, 2 skipped, 0 errors` (the 2 skips are
  `pytest.importorskip("yaml")` on this pyyaml-less clone, not silent passes) —
  reproduces the claim exactly.
- **Test totals**: full-suite run (26 modules, stdlib stand-in) reproduces exactly
  `1134 passed, 0 failed, 39 skipped, 0 errors`.
- **`evidence/DECISIONS.md`** ends at D-32, zero diff; draft D-C is unadopted, matching
  the "no D-number minted" constraint.

### Summary

The 11 filled `permitted_producers` rows are genuine transcriptions of this unit's own
pre-existing code constants and a release directory name used elsewhere in the pipeline,
verified against live enforcement code that actually gates the build path — not a set of
strings chosen to make a test pass. The 7 deferred driver rows are honestly reported as
deferred (fail-closed, not admitted), and the new tests exercise real refusal paths rather
than asserting shape only. No defect found in this unit's exposure to the pass.

## Floor-reset re-review (2026-09-11)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-11T14:37:13Z
**Iteration:** Floor-reset re-review, class ADVERSARIAL (repo-wide D-38/D-35 landing)

### Scope and baseline

HEAD `b0b7c1d`. `git diff --stat 715f392 HEAD -- src/data/splits.py src/features/ configs/data.yaml
configs/experiment.yaml configs/features.yaml scripts/05_build_features_and_splits.py
tests/test_split_embargo.py tests/test_train_only_transforms.py tests/test_feature_availability.py
aidlc/.../construction/features-and-splits/` prints **empty** — every file this unit owns is
byte-identical to the state the 2026-09-10 review already accepted. HEAD `b0b7c1d`'s own diff
(`git show --stat HEAD`) touches only `aidlc-state.md`, the audit shard, `foundation`'s and
`governance-guards`' code-summaries, and `evidence/test_run_access_log.jsonl` — none of this
unit's files, so its unedited-git-template message and missing D-number are not this unit's
defect (stated per `project.md:code-generation:gf-1` — baselined explicitly, not asserted as an
unqualified invariant). The only uncommitted (dirty) file touching this unit's territory,
`tests/test_locked_test_guard.py`, is a `governance-guards`-owned addition (its own "Section 10 —
the SD-C-02 containment fields (added 2026-09-11, governance-guards)", diffed and read in full):
it only extends the docstring's ownership paragraph and appends section 10 after this unit's
existing section 9; section 9 itself carries zero diff. Ran the whole file after the addition —
57 passed / 0 failed / 0 errors — confirming the addition did not disturb this unit's limb.

### Verification performed (executed, not read)

All commands run against the REAL repository files under
`C:\Users\s_sch\Desktop\test\Thesis_toshkari-main\Thesis_toshkari-main`, using the session's
CPython 3.11.16 stand-in (`scratchpad/uv-pythons/.../python.exe`; pyyaml/pandas/numpy remain
uninstallable, PyPI egress blocked, matching the summary's own stated environment) plus the
pre-existing stdlib pytest stand-in and a tiny hand-written config-block extractor (printed
before use, same technique the unit's own `Iteration 2`/D-38 commits used) feeding the
project's own unmodified validators — never a rewritten copy of the logic under test.

1. **Split contract against the real, now-filled `configs/data.yaml: partitions` and
   `configs/experiment.yaml: embargo_hours = 24` (D-38).** `build_partitions(snapshot)` built
   from the real file accepts exactly 6 partitions matching the on-disk F1–F4/REFIT/DEC values.
   Eight targeted negative controls, each mutating one field of the real block and re-running
   the unmodified validator: R-80 `DEC.train_end != REFIT.train_end` refused; a validation month
   not immediately after `train_end` refused (fold contiguity); `kind` disagreeing with `id`
   refused; a 5th-partition (missing id) and a 7th-partition (extra id) block both refused; a
   non-null `REFIT.validation_month` refused; a `train_start` diverging from the study origin
   refused (expanding-window bar). `embargo_hours` TBD, `0`, `-1`, and `True` (bool-as-int) all
   refused. `build_split_manifest` gives exactly 5 rows (`DEC` absent); a hand-assembled 6-row
   manifest (with `DEC`) and a 4-row manifest were both fed to `assert_split_manifest` directly
   and both refused; a manifest missing one fold's `excluded_embargo_rows` count refused.
2. **24-hour embargo, executed against the real `embargo_hours=24`.** 30 synthetic hourly rows
   from the validation-month start: `apply_embargo` excludes exactly 24 and keeps 6. Boundary
   check: the row at `start+23h` is excluded, the row at `start+24h` is kept — the boundary is
   `[start, start+24h)`, half-open, matching TE §7.1's "24 hours" column exactly.
3. **NFR-LEAK-01 (train-only transforms).** Read `src/features/transforms.py` in full:
   `fit_transforms` raises `LeakageError` unless `spec.role == "train"` AND
   `(scored_start, scored_end) == (train_start, train_end+1d)` exactly (over-wide and
   strict-subset both refused) AND the bundle is untransformed; there is no code path that
   fits over an unscoped/full-dataset matrix — the only entry point that computes means/scales
   is gated by these three checks in sequence, before any arithmetic runs.
4. **December/locked unreachability.** `materialise_locked_partition` refused with
   `g05_signature=None` and again with a non-verifying signature string — executed, not just
   read. `verify_g05_signature(real_snapshot, "anything") == False`: the real `configs/data.yaml`
   carries no `gates.G-05` block at all today, so nothing verifies. `FITTING_PARTITION_IDS`
   excludes `DEC` (checked directly). `assert_membership_from_timestamps` accepted an in-range
   February row under F1's train role and refused a December-timestamped row under the same
   role/partition — membership is derived from the timestamp, never a directory name.
5. **`permitted_producers` fail-closed (D-35), executed against the real `configs/features.yaml`.**
   Extracted the real 11-row block and called `load_permitted_producers` (the `ConfigSnapshot`
   path, not the yaml-dependent `Path` branch) requesting all 18 `SECTION_6_2_ROWS`: raised
   `LeakageError` naming exactly the 7 deliberately-deferred driver rows
   (`kp_safe, ap_safe, hp60_safe, ap60_safe, f107_safe, f107_81_trailing, dst`) and no others.
   Requesting only the 11 filled rows succeeded and returned the exact producer mapping written
   in the file. Requesting `kp_safe` alone also refused. No feature-matrix path was exercised
   that could route around this refusal — `load_permitted_producers` is the first call in
   `scripts/05_build_features_and_splits.py`'s `_run()` (confirmed by direct read, both
   `_assert_phase1_field_contract`/`ensure_process_determinism` precede it and
   `load_feature_dictionary` follows it, matching iteration 2's fix).
6. **R-114 one-copy rule.** `grep -rln 'def paired_difference_series\|def equal_station_mean' src/`
   returns exactly one file, `src/evaluation/metrics.py`; neither name appears anywhere under
   `src/data/`, `src/features/`, or this unit's test files.
7. **D-27-withheld inverse.** `grep -rn inverse src/features/` returns three hits, all prose
   ("No inverse path", "No `inverse` and no `apply` method exist here") — no `def inverse`, no
   `inverse_transform`, no callable inverse surface anywhere in `build.py` or `transforms.py`.
8. **Count derivation, printed before assertion.** `grep -c '^def test_'` on the four
   §12-mandated modules gives `test_split_embargo.py` 34, `test_train_only_transforms.py` 28,
   `test_feature_availability.py` **56** (not the "54" the Files-created table states — traced
   the discrepancy to source rather than asserting it as a defect: `git show 6246907:tests/
   test_feature_availability.py | grep -c` gives 54 at the pre-D-35 baseline the table describes;
   `git diff 6246907 17e0767` shows the D-35 pass removed
   `test_permitted_producers_reads_the_real_features_yaml_and_refuses_today` — obsolete once the
   config stopped refusing — and added the three new contract tests named in the "Owner-rulings"
   section, net +2 → 56. The "54 passed, 0 failed, 2 skipped" claim in that later section is
   exactly 56 total and matches; no false count found), `test_locked_test_guard.py` 42 (this
   unit's section-9 subset; +15 new section-10 cases from `governance-guards` account for the
   file's 57-passed total, confirmed by the diff in Scope above). Ran all four (plus
   `test_common_masks.py` as the fifth §12 module this unit's R-114 boundary touches) under the
   stdlib stand-in: `test_split_embargo` 35 passed/1 skipped, `test_train_only_transforms` 28
   passed, `test_feature_availability` 54 passed/2 skipped, `test_common_masks` 60 passed/1
   skipped, `test_locked_test_guard` 57 passed — **0 failures across all five**, all skips
   `pytest.importorskip("yaml")` (environmental, not silent passes). No `2022`/`2001` literal
   found in `src/data/splits.py`; no `iri`/`gim`/`sklearn`/`evaluation` import under
   `src/features/*.py` or `src/data/splits.py`.
9. **No TBD sentinel filled by convenience; no credential; no weakened guard.** Read
   `configs/data.yaml`/`experiment.yaml`/`features.yaml` in full: `stations`,
   `feature_dictionary`, `availability_lags`, `normalization`, `feature_set_id`,
   `practical_relevance_threshold`, `folds`, `models.selected`/`declared_baseline_per_track`
   all still carry the sentinel; D-33's `cell_rule` explicitly states its supervisor
   countersignature is NOT YET GIVEN; the 7 driver-producer rows stay unfilled. Grepped the
   touched files for credential/secret/token/API-key patterns — none found. `Partition.
   embargo_hours` still carries no default (`= 24` was the rejected shape); no `24` literal
   reappears anywhere the tests check for it outside the calendar-arithmetic exception the
   prior review already ruled acceptable.
10. **Repository-owner decision cross-check.** `evidence/DECISIONS.md` D-38's prose
    ("six accepted, every structural rule exercised, and a control with an unresolved embargo
    still refused") matches this pass's independent re-derivation exactly, and the commit
    messages for `9d3e853`/`f0d9e49` cite the D-numbers `team.md` requires for a governed-config
    commit — both commits predate and are unaffected by HEAD's un-cited template message, which
    (per Scope above) touches none of this unit's governed files.

### Findings

None survive verification at any severity for this unit's exposure to this pass.

### Coverage limits

- `pyyaml`/`pandas`/`numpy` remain uninstallable in this environment (PyPI egress blocked,
  re-verified this pass); the yaml-dependent branch of `load_permitted_producers` (the `Path`
  signature, as opposed to the `ConfigSnapshot` signature exercised above) and a full
  `load_configs` run were not executed end-to-end — same limitation the unit's own summary and
  D-38's commit both state and route as owed to a governed environment.
- Did not read any sibling unit's `construction/<other-unit>/` content; the `governance-guards`
  section-10 addition to the shared `test_locked_test_guard.py` was read only because it is the
  single file this unit's own record names as jointly owned, and only to confirm it left this
  unit's section 9 untouched (the carve-out for a named integration point).
- Did not re-verify `evidence/test_run_access_log.jsonl`'s append-only growth row-by-row (large,
  JSONL, append-only by construction); confirmed only that it is not this unit's owned artifact
  and that no restricted-root/December content appears in the tests that write to it.

### Summary

Every structural split rule, the 24-hour embargo, the December/locked unreachability guard, the
train-only-transform boundary, the permitted-producer fail-closed policy, and the R-114/D-27
one-copy and no-inverse invariants were exercised against the REAL, now-frozen `configs/data.yaml`
(D-38 partitions), `configs/experiment.yaml` (D-38 embargo_hours), and `configs/features.yaml`
(D-35 permitted_producers) — not read as prose — including eighteen distinct negative controls,
and every one behaved exactly as this unit's code-summary and the governing D-numbers claim. The
one apparent count discrepancy (54 vs. 56 test functions) traced to a legitimate test replacement
at the D-35 pass, not a stale or wrong assertion. This unit's own files carry zero diff since the
last accepted review; the one dirty file in its territory is a sibling's own out-of-scope
addition that leaves this unit's limb intact.

## Re-review at REJECTED gate (2026-09-13)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-13T11:00:13Z
**Iteration:** Adversarial re-review of a REJECTED gate (revision 2) — full independent re-derivation, not a delta check

### Scope and baseline

HEAD `1670ac8`. `git diff --stat b0b7c1d HEAD -- src/data/splits.py src/features/ configs/data.yaml
configs/experiment.yaml configs/features.yaml scripts/05_build_features_and_splits.py
tests/test_split_embargo.py tests/test_train_only_transforms.py tests/test_feature_availability.py
aidlc/.../construction/features-and-splits/` shows only this file's own 2026-09-11 Floor-reset
block (149 insertions) — every module and test file this unit owns is byte-identical to the state
the 2026-09-11 review accepted. The two commits since then (`a44fbce`, `1670ac8`) each touch only
the audit shard (`git show --stat`, both), confirmed by direct read — neither touches any file
this unit owns. This confirms the dispatch premise: nothing in this unit changed; this is a fresh
derivation of a clean prior verdict, not a delta review.

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `code-summary.md` line 21 (Files-created table, `tests/test_feature_availability.py` row: "§12-mandated. 54 test functions"); line 37 ("`test_feature_availability` 53 passed / 1 skipped") | Re-derived independently: `grep -c '^def test_' tests/test_feature_availability.py` gives **56**, not 54, against the current, unedited file (zero diff since `6246907`, confirmed above). This is not a new fact — this artifact's own 2026-09-11 Floor-reset section (item 8) already derived 56 and named the Files-created table's "54" explicitly by number as the figure it disagrees with, and the 2026-09-10 Owner-rulings review's own reproduced run ("54 passed, 0 failed, 2 skipped" = 56 total) is consistent with 56, not 54. Two subsequent review passes (2026-09-10, 2026-09-11) identified or reproduced the correct total and neither edited the Files-created table cell or the stale shim-results line to say so — the correction stayed in review prose, never landing in the artifact body. This is exactly the defect class `project.md`'s `code-generation:fr-2` rule was written to close ("write the correction into the artifact BODY rather than only into a review addendum"), and it survived through two more passes that each explicitly held the correct number in hand. | Edit line 21 to read 56 (with a short note: 54 executed + 2 environment-skipped under the stdlib shim, per the 2026-09-11 derivation) and correct or annotate line 37's stale "53 passed / 1 skipped" (an iteration-1-era figure superseded by the 2026-09-10 review's reproduced "54 passed / 2 skipped" = 56 total). Do this in the artifact body, not a further review addendum. |
| 2 | Major | `code-summary.md` line 69 ("New items from this pass": "R-80's calendar values still owed to `configs/data.yaml` at their freeze") | This owed item is stale. `evidence/DECISIONS.md` D-38 (decided 2026-09-10, jointly authorized by student and supervisor) explicitly transcribes R-80's frozen split configuration into `configs/data.yaml: partitions` (F1–F4/REFIT/DEC, verified by direct read of D-38's table) and `configs/experiment.yaml: embargo_hours = 24` — read directly from `configs/data.yaml` and confirmed the six partitions and their `train_start`/`train_end`/`validation_month` values match D-38's table exactly. The unit's own 2026-09-11 Floor-reset review (§1) ran its negative controls against "the real, now-filled `configs/data.yaml: partitions`" — i.e. it read the very file that discharges this "owed" line — yet did not correct or strike line 69's claim that these values are still owed. This is a second instance of the same class as finding 1: a fact re-derived correctly in a later review pass, never swept into the artifact body it corrects. | Strike or annotate line 69's R-80/`configs/data.yaml` owed item as discharged by D-38 (2026-09-10), citing the transcribed table. Leave the earlier prose standing per the project's append-only correction convention; add the correction rather than delete the record of what was once owed. |
| 3 | Minor | `code-summary.md` § Repository state (lines 72–79) | States "HEAD is `6246907…`" — accurate as of the 2026-09-06 dated derivation it explicitly carries, but current HEAD is now `1670ac8`, three commits later. Not misleading on its own terms (the section is explicitly timestamped and the 2026-09-11 Floor-reset section already re-baselined once), but nothing in the artifact states the two newest commits (`a44fbce`, `1670ac8`) were checked against this unit's territory. Independently confirmed here (Scope and baseline, above) that neither touches this unit's files, so the underlying disposition is unaffected — recorded so the next reviewer does not have to re-derive it. | No artifact edit required; the fact is now on record in this review block. A future pass updating § Repository state's own body should note the re-baseline explicitly rather than leaving the reader to infer it from review addenda. |

### Independent re-verification (executed/read, not carried from prior prose)

- **Test/line counts, re-derived**: `grep -c '^def test_'` gives `test_split_embargo.py` 34, `test_train_only_transforms.py` 28, `test_feature_availability.py` **56** (not 54 — finding 1), `test_locked_test_guard.py` 42 (this unit's section-9 subset). `wc -l`: `src/data/splits.py` 759, `src/features/availability.py` 503, `src/features/build.py` 1197, `src/features/transforms.py` 342, `src/features/windows.py` 559, `src/features/_frames.py` 164, `scripts/05_build_features_and_splits.py` 610 — none of these line counts is asserted anywhere in the artifact body, so none is stale.
- **Repository state**: `git log -1` → `1670ac8`, author `Kimrza`, committed 2026-09-13; message is the unedited git commit template, same defect class as `6246907`/`06207c4`. `git show --stat 1670ac8` and `git show --stat a44fbce` each touch only `aidlc/.../audit/git-ae-srv-rdt1-8d4da85135a5.md` — confirmed neither is this unit's commit or touches this unit's territory. This unit's own files (`git diff --stat b0b7c1d HEAD -- <unit paths>`) are unchanged except this file's own review additions.
- **Attribution**: `tests/test_determinism.py`, `tests/test_phase_boundary.py`, `tests/test_phase_contract.py`, `src/evaluation/guards.py` are dirty in the working tree from other units' repair work (per `git status`); none is created, modified, or claimed by this unit's Files tables — no misattribution found. Checked the dispatch's premise that `src/features/transforms.py` was "edited additively by `evaluation-and-comparison`": `git log --oneline -- src/features/transforms.py` shows exactly one commit (`6246907`, this unit's own), and `git diff --stat 6246907 HEAD -- src/features/transforms.py` / `git diff --stat b0b7c1d HEAD -- src/features/transforms.py` are both empty — the file is unmodified since this unit committed it. That premise is not borne out by the repository; the artifact makes no contrary claim, so this is a note for the record, not a defect.
- **Leakage/import-boundary re-checks, executed directly against HEAD `1670ac8`** (not read from prior review text): `grep -rn "^import\|^from" src/features/*.py src/data/splits.py` for `iri|gim|sklearn|evaluation` returns nothing; `grep -n "2022\|2001" src/data/splits.py` returns nothing; `requirements.txt` still carries no `pyarrow` pin (matches the artifact's "pin owed" claim); `tests/test_feature_leakage_guards.py` still does not exist (matches "unbuilt" claim, key decision 9).
- **Standing owed items re-checked**: TA-36 (R-76a's primary test) confirmed still `Pending` in `requirements.md:388` ("row exists; not implemented, not executed, not passing") — the artifact's "TA-33, TA-34, TA-35... stay Pending" claim (and TA-36 implicitly via key decision 9) is not contradicted.
- **D-37 (2026-09-10, one day before the Floor-reset review) reaffirms D-27 permanently** and closes BLK-08's mechanism limb in D-27's identity form, without creating any generic inverse route or import-boundary change. Checked this artifact's own D-27/BLK-08 language (lines 5, 68) against D-37: "BLK-08 deferred... narrowed to `ABL-DIFF` per D-27" is not contradicted by D-37 — D-37 explicitly does not create an inverse route or touch the import boundary, and this unit's code (no `inverse`/`apply` surface, confirmed above and in the 2026-09-11 pass) is unaffected. Not flagged as a finding: D-37 reaffirms rather than supersedes, and no artifact claim about code behavior is falsified by it.

### Coverage limits

- Same environment limits as every prior pass: no `pyyaml`/`pandas`/`numpy`/`ruff` in this environment (not independently re-verified this pass beyond confirming no new pin was added); no end-to-end script execution.
- Did not read any sibling unit's `construction/<other-unit>/` content; the transforms.py cross-unit-edit check above was resolved entirely from `git log`/`git diff` on the file itself, which is the sanctioned spot-check path for a named integration point.
- Did not re-verify `evidence/test_run_access_log.jsonl`'s row count or re-run the test suites under the stdlib shim this pass; relied on `grep -c '^def test_'` (source-derived, not run-derived) for the corrected counts in findings 1 and the re-verification section.

### Why READY, despite two Major findings

Zero Critical, two Major, one Minor — within the stated verdict threshold (READY at ≤2 Major,
any Critical or >2 Major forces NOT-READY). Both Majors are the same defect class: a count and a
governance-stop "owed" item that a *later review pass already in this artifact* demonstrably
re-derived correctly, and neither correction was swept into the artifact body — it stayed in
review prose (`code-generation:fr-2` exists precisely to prevent this and was not honoured on
either item). Neither finding implicates the code, the tests, or the re-verified leakage
guarantees themselves: every structural split rule, the 24-hour embargo, the December/locked
unreachability guard, the train-only-transform boundary, the permitted-producer fail-closed
policy, the import-boundary and no-scientific-literal checks all re-verified clean against the
real repository at HEAD `1670ac8`, and nothing in this unit's owned files has changed since the
last accepted review. A developer could implement or extend from this artifact without
architectural guidance; they would, however, be handed two stale figures they'd have to
cross-check against the review history themselves. **Both findings should still be corrected in
the artifact body before the gate is presented to the human** — they are gate input, not a
blocker to this verdict.

---

## Post-receipt amendment — 2026-09-18 (D-25 Route 1 reconstruction; gate item G-5)

*Appended under `project.md` `code-generation:gf-3` ("update the owning unit's
code-summary when a repair edits a module that unit owns"). Nothing above is rewritten;
the READY receipt and the review sections stand as history. Authority:
`governance/CHANGE_RECORD_2026-09-16_d25_availability_rule.md` (owner ruling, Route 1),
reconstructed in this clone on 2026-09-18.*

| Module | What changed (measured, `git diff --numstat` vs `18843aa`) |
|---|---|
| `src/features/availability.py` | +143 / −13. `AvailabilityRow` gains a THIRD additive field `availability_rule: str | None`; `safe_lag_hours` is `float | None`, `None` exactly when a recognised rule is recorded. Closed rule set `AVAILABILITY_RULE_KINDS = {"previous_day_median_midnight_utc"}` (D-25). `read_availability_lags`: a rule entry must be in the closed set, must not also declare `safe_lag_hours`, must not also declare a `window`; a feature with neither fails naming both; block-level fail-closed unchanged. `build_availability_matrix`: rule instant = midnight UTC of observation day + 1, combined by `max` with the observation/publication instant; a negative lag under a rule is refused at build (`LeakageError`). `assert_lags_safe`: rule rows pass on non-negative lag + recognised rule; a row with neither scalar nor rule fails. |
| `tests/test_feature_availability.py` | +202 / 0 — **54 → 66 test functions** (12 new: next-day-midnight availability, origin-hour independence, same-day and future anchoring refused, unknown rule kind, rule+scalar, rule+window, neither, later publication governs, scalar rows unchanged, fail-closed with a rule present, `assert_lags_safe` negative/neither). None removed or weakened. 8/8 mutation controls killed (scratchpad, restore SHA-verified). |
| `scripts/05_build_features_and_splits.py` | +1 / 0 — `PRODUCED_FIELDS` gains `"availability_rule"` (R-24 produced-field guard). |

Runs (supplemental, NOT governed: real `pytest 9.1.1` on CPython 3.14.7; the 3.11
governed environment was prepared later the same day, see `CR-2026-09-18-GATE-PREP`):
module 66 passed / 2 skipped (yaml absent); whole tree 1192 passed / 39 skipped / 0
failed; `compileall` 0.

**Known limit of the scalar-plus-window shape under D-25 (recorded here, not
resolved):** `f107_81_trailing` cannot carry the rule (Route 1 item 6), so its limb-1
lag is measured from whatever `observation_timestamp` the driver rows record; the
fixture convention (anchor-day 00:00, scalar 24 h) passes, while the honest constituent
instant (median(D−1) completes ~23 UT on D−1, available 00:00 D under D-25) fails limb 1
at 23 of 24 origin hours. Counterexample and proposed repair: `CR-2026-09-18-GATE-PREP`
§2. No semantic change made.

## Post-receipt amendment — 2026-09-19 (D-43/D-44/D-46/D-47 scientific decisions; config transcription; `CR-2026-09-19-SCI-DECISIONS`, item 6 of the 2026-09-19 owner authorization)

*Appended under `project.md` `code-generation:gf-3`. Nothing above is rewritten. Authority:
`evidence/DECISIONS.md` D-43, D-44, D-46, D-47 (D-42/D-43/D-46 are TE §18.2 Student +
Supervisor items: supervisor approval REPORTED by the student 2026-09-19, countersignature
artifact PENDING — `governance/COUNTERSIGNATURE_REQUEST_2026-09-19.md`).*

| Module | What changed (measured, `git diff --numstat` vs `18843aa`) |
|---|---|
| `src/features/availability.py` | +337 / −40 (cumulative this session). This pass adds `recomputation_tolerance_bound` (D-47's a-priori float64 error bound, `(N+1)·ε·B`) and `assert_recomputation_domain` (the certified-input-domain check: a constituent above the applicability bound fails the certification clearly and is never clipped); `assert_anchor_recomputed` gains an optional `input_bound` parameter that invokes the domain check before recomputing. Docstrings corrected to state a rule in `AVAILABILITY_RULES_WITH_WINDOW` MAY carry a window (A2), and the per-constituent loop in the anchor limb carries a comment naming the monotonicity invariant that makes it redundant under the supported contract (the surviving A2 mutant's disposition). |
| `src/features/build.py` | +72 / −13. `_assert_driver_alignment` gains a second explicit form for a LAGGED `*_safe` series (`attrs["selection"]`): checked by `external-products`' `assert_lagged_selection` instead of the raw own-interval check; a selection lag disagreeing with the availability matrix's declared `safe_lag_hours` for that feature is refused (`AlignmentError`, "applied once") — no double lag, no shortfall. The raw own-interval path is unchanged. |
| `src/external/spaceweather.py` | +342 / −33. New: `select_lagged_series` (the ONE place a lag is applied to an interval-valued index — D-43/D-44), `assert_lagged_selection` (the alignment contract for a lagged series), `availability_rows_from_selection` (matrix rows derived from a selection), `daily_medians_from_readings` (D-21/D-22/D-23's project-derived daily F10.7 value). `resolve_f107_at_origin` now returns `F107Selection` (a dataclass: `source_day`, `value`, `carried_forward`, `excluded`, `staleness_hours`) instead of a bare tuple, and implements D-46's reading B (`CARRY_FORWARD_COMPOSITION_CLOCK_HOURS`): ordinary reuse vs a missing-update clock measured from the designated value's EXPECTED availability instant, inclusive boundary. **Breaking return-type change**, callers updated in the same pass (`tests/test_external_drivers.py`). |
| `configs/features.yaml` | +80 / −1. `availability_lags` transcribed from `TBD — freeze gate` to the six §6.2 driver rows (D-25 rule on the two F10.7 rows; scalar `safe_lag_hours` on the four GFZ rows; D-47's tolerance/domain on `f107_81_trailing`'s window); `carry_forward_bound_hours: 3` and `carry_forward_composition: "clock_hours"` added (D-46). `feature_set_id`, `feature_dictionary`, `normalization`, `permitted_producers` untouched — no feature-dictionary freeze, no producer entries. |
| `tests/test_feature_availability.py` | +775 / −3 (cumulative). This pass: `test_d25_constituent_availability_is_monotone_so_the_anchor_bounds_the_window`, `test_trailing_window_membership_is_exactly_the_declared_days_ending_at_the_anchor`, `test_real_fluxtable_carries_every_day_of_the_window_ending_before_2022`, `test_interval_end_observation_timestamps_make_the_lag_a_post_completion_margin`, `test_d47_tolerance_derivation_against_an_exact_reference_and_the_certified_domain`, `test_lagged_safe_series_passes_through_build_features_with_no_second_lag`, `test_prepared_six_entry_availability_lags_load_without_error` (the real `configs/features.yaml` read through `read_availability_lags` unmodified — 81 test functions total). |
| `tests/test_external_drivers.py` | +313 / −24 (cumulative). D-46 composition tests (`test_f107_ordinary_reuse_...`, `test_f107_missing_update_allows_three_clock_hours_inclusive_then_excludes`, `test_f107_clock_starts_at_the_expected_instant_not_the_carried_value`, `test_f107_frozen_composition_needs_the_configured_bound_and_refuses_other_vocab`), D-21/D-22/D-23 daily-median test, D-43/D-44 selection tests (boundary cases at and before availability, open/stale/double-lag/shortfall/untraceable/dropped-value refusals, composition with carry-forward) — 65 test functions total. |

Runs (governed pin, conda `tec-thesis-311`, CPython 3.11.16): module-scoped focused runs
green throughout implementation; combined `test_feature_availability.py` +
`test_external_drivers.py` + `test_iri_denial.py` + `test_locked_test_guard.py`: see
`governance/CHANGE_RECORD_2026-09-19_scientific_decisions_p2.md` for the exact count.
`ruff check`: 5 pre-existing findings in `test_feature_availability.py`, unchanged from
before this pass (68 at HEAD before this session's work); none introduced by this pass's
own diff hunks were left unaddressed (checked individually).

**What this amendment does NOT do.** It does not certify any `*_safe` feature leakage-free,
does not pass G-04, and the `lag_reference_instant`/`selection_rule`/
`recomputation_input_bound_sfu` fields transcribed into `configs/features.yaml` are carried
by the reader but not yet asserted by it — a reviewed reader change is owed before they are
enforced.

## Post-receipt amendment — 2026-09-19 (D-43/D-44/D-47 configuration validation and real-consumer enforcement; `CR-2026-09-19-SCI-DECISIONS-P3`)

*Appended under `project.md` `code-generation:gf-3`. Nothing above is rewritten; the
"carried but not yet asserted" limit recorded above is CLOSED by this amendment.
Authority: owner instruction 2026-09-19 item 2 ("Complete configuration validation and
enforcement... Verify that downstream consumers actually apply these settings").*

| Module | What changed (measured, `git diff --numstat` vs `18843aa`) |
|---|---|
| `src/features/availability.py` | +435 / −41 (cumulative this session). `read_availability_lags`: `lag_reference_instant`/`selection_rule` now REQUIRED on every scalar-lag row (closed sets `LAG_REFERENCE_INSTANT_KINDS`/`SELECTION_RULE_KINDS`, the latter imported from `spaceweather.SELECTION_RULE_LATEST_COMPLETED_PLUS_LAG` — one source of truth) and FORBIDDEN on a rule row; `_validate_window_fields` requires `recomputation_input_bound_sfu` as a positive number. `AvailabilityRow` gains `lag_reference_instant`/`selection_rule` (populated by `build_availability_matrix` from the validated entry). **The real gap closed**: `build_availability_matrix` now reads `window["recomputation_input_bound_sfu"]` and passes it to `assert_anchor_recomputed`'s `input_bound=` on every real call — previously this parameter was only ever exercised by a test calling the function directly. |
| `src/features/build.py` | +100 / −13 (cumulative). `_assert_driver_alignment` gains `declared_selection_rule`/`declared_lag_reference_instant` parameters, cross-checking a driver's ACTUAL `attrs["selection"]` against the availability matrix row's config-derived fields (not only the hardcoded module constant); `build_features` now looks the matrix row up per feature and threads both new fields through. |
| `src/external/spaceweather.py` | +367 / −33 (cumulative). `assert_lagged_selection` gains `expected_reference_instant`: since the selector only ever implements `LAG_REFERENCE_INSTANT_INTERVAL_END` (hardcoded, D-43), any other declared value is refused as a config-vs-implementation drift guard rather than silently miscomputed. |
| `tests/test_feature_availability.py` | +957 / −3 (cumulative). 4 new test functions this pass (81 → 85): reader-level required/closed-set/bounds checks for both new fields plus the window bound (positive + 4×negative + rule-row-forbidden controls each); an integration test proving `build_availability_matrix` actually applies the configured bound (same constituents pass at 400 sfu, fail at a lowered 5 sfu bound); an end-to-end `build_features` integration test proving a `selection_rule`/`lag_reference_instant` mismatch between config and driver is refused. 26 pre-existing tests updated for the newly-required fields (fixture `_lags()` and one inline dict) — none weakened, none skipped. |

Runs (governed pin, conda `tec-thesis-311`, CPython 3.11.16): module 85 passed / 0
failed; combined with `test_external_drivers.py`/`test_iri_denial.py`/
`test_locked_test_guard.py`: all green. **Full governed suite: 1278 passed / 4 skipped /
0 failed** (was 1274/4 the prior pass; +4 net, matching the 4 new tests). `ruff
check`/`ruff format`: clean; `tests/test_feature_availability.py` at 4 pre-existing
findings, unchanged from the pre-pass baseline.

**What this amendment does NOT do.** It does not change any scientific decision or
configuration value (every field the prior pass transcribed already satisfied the
stricter reader — checked directly, no contradiction found); does not certify any
`*_safe` feature leakage-free; does not pass G-04.
