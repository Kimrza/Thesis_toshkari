# Code Summary — `governance-guards`

**Unit** `governance-guards` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Plan**: `code-generation-plan.md` — Steps 1–10 executed, plus the **repair Step 11 added and executed 2026-09-13** under the owner's Option 4 ruling at the rejected stage gate. Checkboxes marked.

**Repository state, re-derived 2026-09-13 at HEAD `1670ac8` — CORRECTED after the iteration-1 Critical.** An earlier version of this header claimed "this unit's code is committed and HEAD is `1670ac8`". **That was false for the two files Repair Step 11 produced**, and is corrected in the body rather than left standing for its own reader. Derived: `git status --porcelain` shows `tests/test_phase_boundary.py` and `tests/test_phase_contract.py` as ` M` — **unstaged working-tree modifications**; `git diff --cached --stat` is empty, so nothing is even staged; `git diff HEAD --numstat` returns `125 5` and `12 3` respectively. The unit's Steps 1–10 code IS committed, but **the D-17 repair — the corrected sixteen-field contract and the new drift guard — exists only in the working tree.** Until it is committed, a `git reset --hard`, a `git clean`, or a fresh checkout silently regenerates the exact 17-vs-16 defect this repair closes, with no commit trail showing the fix ever existed. **No commit, amend or push was made by this stage** — the commit is the student's act (`project.md` `code-generation:c30`) — so committing this repair is routed to the gate as an owed act in its own right, not merely as another instance of the message-citation question.

## Repair Step 11 — D-17 field-contract reconciliation, 2026-09-13

Written into the body rather than a review addendum per `project.md`
(`code-generation:fr-2`). Both files below are this unit's own; **no cross-unit edit was
made**, and `src/data/prepared.py` (`target-standardization`'s, and already correct) was
left untouched — `git diff` on it is empty.

**The contradiction, and why it was stale twice.** `tests/test_phase_boundary.py:95`'s
`D17_TARGET_FIELDS` carried **17** names against D-17's frozen **16**, the extra being
`processor_qc_flags` — which is not a target-row column at all but a key inside the
data-quality block (R-71/NFR-DQ-01, W-3), built at `src/data/prepared.py:1304`. That much
had been flagged as a Minor by `target-standardization` on four consecutive passes. What no
pass had caught: the constant is consumed as a **set equality in both directions**, so
`extra` would equally have flagged **`lineage_caveat`** — which the producer emits by
contract (`_TARGET_CSV_HEADER = (*D17_FIELDS, LINEAGE_CAVEAT_FIELD)`, `prepared.py:1324`)
and its own row guard explicitly permits (`prepared.py:791`). Repairing only the first limb
would have swapped which assertion fires on the first real artifact, not fixed the test.

**Authority.** No D-number was required and none was drafted. `git blame` puts every line of
`D17_TARGET_FIELDS` in commit **`b844a4d`** (2026-08-21) — **the same commit that first
wrote D-17's sixteen-row table into `evidence/DECISIONS.md`** — and
`git show b844a4d:evidence/DECISIONS.md` shows that table already carrying 16 rows,
byte-identical to today's. The seventeen is therefore a same-commit transcription slip
against TE §6.1's data dictionary, which D-17 explicitly supersedes for Phase 1; it was
never a competing decision.

**Derivations, printed before assertion.** D-17 table **Field column only**: 16 (a first
naive grep returned 20 by sweeping whole rows and picking up `ut1_unix`/`gdlat`/`glon`/`dtec`
out of the *Source* cell — the wrong intermediate is recorded because the corrected method
is what the 16 rests on). `prepared.D17_FIELDS`: 16, unchanged. `D17_TARGET_FIELDS`:
**17 → 16**. `D17_ALLOWED_FIELDS`: **17 → 16**. `processor_qc_flags` in D-17's Field column:
**0**. Set differences after: `boundary vs prepared`, `contract vs prepared`, and
`prepared vs D-17 table` all `[]`.

**Changes.** `tests/test_phase_boundary.py` (**+125/−5**, re-derived 2026-09-13 by `git diff HEAD --numstat` after the iteration-1 Minor; an earlier version of this line carried +130/−4, which was never derived): `processor_qc_flags` removed;
header comment rewritten off "Column names a Phase 1 target artifact **may carry**" — a
permission list — onto the exact sixteen-field bound matching `prepared.py:788`, stating
that `processor_qc_flags` is a W-3 data-quality-block key; `extra` now subtracts
`DECLARED_CAVEAT_FIELD`, mirroring `prepared.py:791`; **`missing` untouched, still the full
sixteen**; new drift guard `test_d17_target_fields_match_the_producer_contract`.
`tests/test_phase_contract.py` (**+12/−3**, same derivation; an earlier version carried
+15/−2): "the seventeen allowed columns" corrected, constant aligned to 16, and the comment
now says what it is actually for (a happy-path sample for `assert_no_raw_fields` at
`:147`/`:177`, no runtime contract effect).

**Import-boundary finding.** The drift guard does **not** import `src.data.prepared`.
`test_phase_boundary.py` carries no `sys.path` insert and no `from src...` import, and the
repo has **no `conftest.py`** — `test_phase_contract.py:44-46` does its own inline insert
for exactly that reason. A module-level import would add machinery the file does not carry,
transitively pull `src.data.{acquisition,config,release}` in at collection time, and turn
the module's designed "SKIP when `src/` is absent" into a collection error. So the guard
follows the path the module already uses to reach source — **AST parsing**, via its existing
`ast.parse` mechanism — and fails closed like `_imported_modules`.

**What the new controls prove is caught**, beyond set equality: a stale 17th field
returning; a field silently dropped; the producer gaining a field; the producer constant
renamed, removed, unparseable, or computed rather than literal (each fails, never a quiet
pass); `lineage_caveat` literal drift between the two now-separate spellings. Nine further
controls pin the conformance limb — 16+caveat accepted, bare 16 accepted, an extra Phase 2
column *beside* the caveat still refused, `processor_qc_flags` on a row now refused, and a
dropped contract field still failing, which demonstrates the `missing` limb was not
weakened. **No guard was weakened to make anything pass.**

**Execution — smoke only, never governed.** Real `pytest` is unavailable (PyPI egress
blocked). Both files `py_compile` clean and **89 passed / 1 skipped / 0 failed** across every
test in both modules, including all parametrized cases, under a stdlib pytest stand-in on a
scratchpad CPython **3.11.16** left by a prior session. The single skip is the module's own
designed skip (no hourly-target artifact exists); its body was driven separately by
redirecting `EVIDENCE_DIR`. A hand-rolled stand-in is not pytest and the environment is not
governed. `ruff` is not installed; no introduced line exceeds the configured 99 (the three
over-99 lines are pre-existing and identical at HEAD, and `E501` is ignored project-wide).
No acceptance row is claimed discharged.

## Files created

| Path | What |
|---|---|
| `src/data/phase_contract.py` | `assert_phase_boundary(phase, *, loaded_modules)` (approved component-methods signature; `RAW_MODULES` = 4 dotted names); `assert_no_raw_fields` (D-17's 8 exclusion classes, token-based matching + compounds so renamed columns trip and innocent lookalikes pass); `diff_protected_hashes` + `assert_protected_hashes_unchanged` (G-P3C refusal as pure function); `ManifestError`, `PhaseBoundaryError` via `IntegrityError` from `src/data/config.py` |
| `src/data/reuse_registry.py` | §10.1 register: `ReuseRecord` (15 fields), `register_reuse` (append + fsync), `load_register` (fail-closed), `assert_reuse_registered_before_use` (`REUSE-PROVENANCE:` marker scan); reimplementation-default posture + AGPLv3 dependency stated in docstring, not resolved |
| `tests/test_phase_contract.py` | 36 tests: per-RAW-module import controls, 8 produced-field controls + 4 renamed-column controls, R-23 independence, R-24 completeness (checker factored to `_producing_script_violations(scripts_dir)`; 4 synthetic-fixture controls prove detection fires — no guard call, call-after-write, compliant, unparseable — before the real population exists), 5 hash-diff controls, documentation + hierarchy tests |
| `tests/test_reuse_registry.py` | 27 tests: 15 blank-field refusals, use-before-registration, unparseable-line failure, append safety, duplicate reuse_id, real-tree completeness |

## Files modified in place

| Path | What |
|---|---|
| `src/data/locked_test.py` | ⚠️ **INCOMPLETE as written — a second, later edit to this file is disclosed in § "Cross-unit edit disclosed (2026-09-11)" below; read the two together.** **Q1=A refusal — found ABSENT, implemented**: fires FIRST, before any row append, when `resolve_platform_roots` labels a non-`local` platform not in `CHARACTERISED_DURABILITY_PLATFORMS` (imported from foundation's `config.py`, so stamp posture and refusal posture can never disagree; set empty ⇒ kaggle refused until W-6 step 8 measures). Also: `EvidenceScanError` + shared `fail_unparseable` helper (R-27's one home); residency scan's silent `continue` on unreadable files replaced with failure; `RESTRICTED_LITERAL_EXEMPT_MODULES` source constant (7 members). Built chokepoint properties untouched |
| `tests/test_locked_test_guard.py` | 16 → 36 tests. Literal scan now AST-based with constant folding. Scope stated exactly (iteration-1 Major 1 fix): **DISC-2's named evasion (Q2=B `+`-concatenation) closed; folder extended to constant-only call forms** (`os.path.join`/`joinpath`, `%`-format, `str.format`, `str.join` over constant elements, pathlib `/` over constants — one negative control per caught form); **runtime assembly remains statically unclosable and is disclosed** in the scan's docstring, pinned by a documentation test that also proves a runtime-fed assembly is genuinely not caught. Substring check retained as superset; notebook code cells included; unparseable ⇒ failure through shared helper. Exempt-set exact re-derivation (seven members, both directions). Q1=A controls. 3 SD-G-02 reconciliation tests |
| `tests/test_phase_boundary.py` | Additive only: subordinate-status docstring paragraph (Q7 rider); documentation test guards it. All 53 tests green, none weakened |
| `tests/test_determinism.py` | **Join-required edit to foundation's file, flagged for the gate**: its R-15 needle was assembled from concatenated constants ("assembled so this test file itself passes") — exactly the evasion the new folding scan exists to catch, and it was caught on first run. Needle now derived at run time from `locked_test.RESTRICTED_ROOT`; R-15's control intact; the ruled-at-seven exempt list NOT widened |

## Test and lint results (smoke evidence only — never governed)

- **Full suite after iteration-2 fixes: 449 passed, 3 skipped, 0 failed** — Python 3.11.9 (bootstrapped env). Iteration 1's counts were 437/3, independently re-verified by the reviewer; the +12 are the iteration-2 controls (8 in test_locked_test_guard, 4 in test_phase_contract). Skips unchanged: no hourly-target artifact; producing-script population empty (explicit-record skip, never silent vacuity) — ⚠️ **this middle clause is SUPERSEDED as of 2026-09-11; the population is no longer empty and the test no longer skips. See § "Cross-unit edit disclosed (2026-09-11)" → "Correction 2" below for the printed derivation**; dataset_version derivation covered by D-29 tests.
- Per-module: test_locked_test_guard 36, test_phase_contract 36, test_reuse_registry 27, test_phase_boundary 53, test_determinism 35.
- `ruff check`: all checks passed on the 8 created/modified files; the 4 new files plus `tests/test_locked_test_guard.py` also `ruff format`-clean (remaining pre-existing files not wholesale reformatted — repo was not format-clean before this unit; owed to a later cleanup if wanted).

## Key decisions

1. Q1=A implemented against foundation's `CHARACTERISED_DURABILITY_PLATFORMS` so guard refusal and registry stamp share one measured-platform source of truth.
2. AST scan keeps the substring check as a superset (comment-held literals stay listed); notebooks JSON-decoded with magics dropped as a declared transformation. Scope of the closure stated exactly, never as a blanket "DISC-2 closed": the named `+`-concatenation evasion is closed, constant-only call forms are folded (join-like folds yield both the separator-joined and separator-less concatenation, conservative in the catching direction), and **runtime assembly remains statically unclosable — a named, disclosed residual**, bounded by review plus the run-time chokepoint, which refuses any out-of-root path regardless of how its string was assembled (the same layering R-28 records for the run-time-path-assembly gap).
3. Completeness test skips with the empty population stated verbatim (established explicit-skip convention); a producing script appearing without `assert_no_raw_fields` before its first write fails. The checker is factored (`_producing_script_violations(scripts_dir)`) and its detection is PROVEN by synthetic tmp_path fixture scripts — omitted call, call-after-write, compliant, unparseable — so the promise no longer rests on unexercised code (iteration-1 Major 2 fix); an unparseable producing script is itself flagged, never cleared.
4. `diff_protected_hashes` takes `protected_entries` as caller parameter — R-19 places the authoritative 17-item list in `configs/experiment.yaml`, R-20 records the test-source question OPEN (BLK-06 untouched); missing/unknown keys are `ManifestError`s BEFORE any diff, so a short set can never produce a reassuring empty diff.
5. `ManifestError`/`EvidenceScanError`/`ReuseError` declared in their sole-raising modules under R-01's any-future clause — foundation's `config.py` not edited.
6. `_read_guarded` defining files (review-Minor closure): `tests/test_release_hashes.py:97` and `tests/test_acquisition_window.py:88`.
7. `build_transition_manifest`/`TransitionManifest` deliberately NOT built — mode-channel amendment stays an OPEN owner item; Step 3 shipped only the pure diff.

## Deviations

- Foundation's `tests/test_determinism.py` edited (join-required; above; gate item).
- `assert_no_raw_fields` signature is `(artifact_fields, *, phase)` duck-typing `.columns` — satisfies both the plan's and component-methods' forms without a pandas dependency.
- Residency scan stays `*.json`-scoped; the narrowing is now disclosed in its docstring rather than widened (R-27 full-width walk not ordered by this plan).
- graphify CLI unavailable; graph stale for `src/data/*`, `tests/*`; `graphify update .` owed.

## Governance stop — owed before any commit (student acts; cumulative with foundation's)

- TE §12 naming check for `src/data/phase_contract.py` (amendment if not named; config.py precedent). Same check for `src/data/reuse_registry.py` (§12 does carry `tests/test_reuse_registry.py`).
- Commit citing D-15, D-18, D-31 (+ foundation's D-29/D-122 items); pre-commit hook runs the critical set (Q7=D).
- Nothing discharged: **WS-18, TA-18, TA-25, TA-27, TA-28 all stay `Pending`**; DISC-1's six-vs-seven prose count stays a gate item (code asserts the true seven); FR-P1-02-6 remains rowless; BLK-06 per-item binding and BLK-07 remain open.

## Iteration 2 — both Majors fixed (2026-09-05, same session)

The reviewer's iteration-1 section below is left standing untouched; its NOT-READY verdict predates these fixes and does not cover them.

- **Major 1 (literal-scan residual)** — fixed in two parts. (a) `_fold_constant_str` replaced by `_fold_candidates`: folds string literals, `+`-concatenation, constant f-string parts, `%`-formatting and `str.format` with constant operands, `str.join` over constant-element lists/tuples, `os.path.join`-shaped calls and `.joinpath` over constant args, and pathlib-style `/` over constants; join-like folds yield both the separator-joined and separator-less concatenation (conservative in the catching direction); cartesian products capped at 64. All three reviewer-proved evasions (`os.path.join("locked_test", "_restricted")`, `"%s_restricted" % "locked_test"`, `"".join(["locked_test", "_restricted"])`) are now caught, each pinned by its own negative control (7 parametrized forms). (b) The disclosure, verbatim where the scan lives and here: **"DISC-2's named evasion (Q2=B `+`-concatenation) closed; folder extended to constant-only call forms; runtime assembly remains statically unclosable and is disclosed."** A documentation test pins the disclosure phrase in the module docstring AND proves a runtime-fed assembly is genuinely not caught, so the residual can never be silently re-implied closed. `tests/test_determinism.py`'s docstring wording softened to match.
- **Major 2 (unproven completeness detection)** — the R-24 checker is factored to `_producing_script_violations(scripts_dir)` and exercised by four synthetic tmp_path fixture scripts (no additions to the real `scripts/`): guard call omitted → detected; guard call after first write → detected ("precedes"); compliant → clears; unparseable → flagged (fail-closed, replacing the prior `pytest.fail`-inside-loop shape). The real test still targets `scripts/` with the explicit-skip convention.
- Re-verified: full suite **449 passed, 3 skipped, 0 failed** (Python 3.11.9, smoke only); `ruff check` clean on all 8 touched files; new-file set plus `test_locked_test_guard.py` `ruff format`-clean. Plan checkboxes unchanged — no step description materially changed. Still no `git commit`; WS-18, TA-18, TA-25, TA-27, TA-28 all still `Pending`.

## Review — 2026-09-05 (code-generation, iteration 1)

**Reviewer:** aidlc-architecture-reviewer-agent

### Findings

| # | Severity | Where | What | Recommended action |
|---|---|---|---|---|
| 1 | Major | `tests/test_locked_test_guard.py:319-360` (`_fold_constant_str`), same evasion class reachable via `tests/test_determinism.py:594-615` (R-15 control) | The "one-door" literal scan (R-27/R-28) folds only `ast.Constant`, `BinOp(Add)` concatenation, and `JoinedStr` parts. Verified by direct execution against `_source_holds_literal`: `os.path.join("locked_test", "_restricted")`, `"%s_restricted" % "locked_test"`, and `"".join(["locked_test", "_restricted"])` all construct the restricted-root literal and are **not caught** — the joined text never appears contiguously in source, and none of `Call`/`Mod`/`.join()` is folded. This is a materially different residual from DISC-2's specific named evasion (`nfr-requirements` Q2=B's commitment was scoped to "a path assembled from joined literals" via `+` concatenation, which the implementation genuinely does close — see Verified below). But code-summary and both docstrings state "DISC-2 closed" and describe the property as "does not weaken slightly; it ends" without disclosing that call-based literal assembly is a live, equally-easy bypass of the same boundary — unlike every other known narrowing in this unit (the `*.json`-only residency-scan width, the AGPLv3 register-dependency, the DISC-1 six-vs-seven prose count), each of which is explicitly flagged as open. `test_determinism.py`'s R-15 control derives its needle from the same literal and inherits the identical gap. | Add `ast.Call` folding for at least `os.path.join`/`posixpath.join`/`pathlib.PurePath.joinpath` and string `%`/`.format()`/`.join()` construction, or — if deferred — add an explicit disclosed-narrowing note (parallel to the `*.json`-only residency-scan disclosure) naming call-based literal assembly as an open residual, so "DISC-2 closed" is not read as "no assembly technique escapes the scan." |
| 2 | Major | `tests/test_phase_contract.py:232-276` (`test_every_phase1_producing_script_calls_the_field_guard_before_its_first_write`) | R-24's completeness test is exercised only against real on-disk scripts, and today's population is zero (all eight producing scripts are unwritten), so the test only ever executes its `pytest.skip` branch. The detection logic it depends on (`_first_write_lineno`, `_first_guard_call_lineno`) has **no test coverage at all** — no synthetic fixture script exists that omits the `assert_no_raw_fields` call, or calls it after a write, to prove the ordering check actually fires. This is exactly the gap `team.md` § Testing Posture's mandated practice targets ("every hard rule... gets a test that proves the violation is caught, not only a test that the happy path works"), and R-24's completeness claim currently rests entirely on unexercised code. | Add a `tmp_path`-based synthetic-script fixture test that (a) omits the guard call and asserts the completeness test's own detection helper flags it, and (b) calls the guard after a write and asserts that ordering violation is flagged too — proving the mechanism works before the real population arrives, not only that it skips cleanly today. |

### Verified and held (adversarial angles pressed, not defeated)

- **DISC-2's own named evasion** (`+`-concatenation, `EVIDENCE_DIR / ("locked_test" + "_restricted")`) is genuinely caught by constant folding — reproduced with a synthetic snippet; matches `nfr-requirements` Q2=B's specific commitment.
- Unparseable file (Python and notebook) is a hard failure through the shared `fail_unparseable` helper — reproduced with a deliberately broken `.py` and a malformed `.ipynb`; both raise `EvidenceScanError` rather than skipping.
- Notebook code cells are genuinely scanned (magics/shell lines dropped as a declared transformation); reproduced with a synthetic notebook containing the concatenated evasion in a code cell.
- Q1=A refuses **before** any row append (verified in `open_restricted`'s control flow and by `test_uncharacterised_platform_is_refused_before_any_row`, which asserts the registry file does not exist after refusal); `local` is exempted per the design's scheduling note; `CHARACTERISED_DURABILITY_PLATFORMS` is a single empty constant in foundation's `config.py`, imported (never duplicated) by `locked_test.py`, so the two postures cannot diverge.
- R-23 independence (import limb vs. produced-field limb) is tested in both directions in one dedicated test; neither limb's pass conditions the other's.
- `diff_protected_hashes`/`assert_protected_hashes_unchanged`: missing or unknown manifest keys raise `ManifestError` **before** any diff is computed (code-level and test-level verified); an empty or duplicated `protected_entries` list is refused, so a short list cannot manufacture a reassuring empty diff.
- Reuse register: all fifteen §10.1 fields are enforced non-blank at construction (`ReuseRecord.__post_init__`) and again at load (`load_register`); `copied_or_adapted` is a closed vocabulary. Use-before-registration is caught via the `REUSE-PROVENANCE:` marker scan — this scheme is **self-reporting by construction** (an unmarked copy is indistinguishable from original work), but that limitation is explicitly disclosed in the module's own docstring rather than silently assumed, so it is not counted as an undisclosed gap.
- `tests/test_determinism.py`'s edited R-15 needle is derived at run time from `locked_test.RESTRICTED_ROOT` rather than held or reassembled locally; this is not the circularity R-28 rejects (`locked_test.py` is not the module under test in that file, and no path is resolved from the derived name) — the edit is join-required and correctly disclosed as a gate item rather than applied silently.
- Exempt-set test (`test_exempt_list_membership_is_rederived_exactly`) enumerates the seven members literally rather than importing the constant under test, and checks both directions (unlisted holder fails; listed-but-no-longer-holding member fails).
- No boundary trespass: none of the four new/modified `src/data/` or `tests/` files import anything from `src/features/`, `src/models/`, or `src/external/`; foundation's `config.py`/`experiment_registry.py`/`release.py` do not import any governance-guards module (dependency edge runs one way, governance-guards → foundation, no cycle).
- Claim honesty: WS-18/TA-18/TA-25/TA-27/TA-28 are consistently stated `Pending` everywhere checked (plan, summary); no acceptance-row discharge or governed-evidence claim is made for the smoke run.
- Suite integrity: independently re-run, `437 passed, 3 skipped, 0 failed` — exact match. Per-module counts independently re-derived by collection and exactly match the claimed 28/32/27/53/35. `ruff check` independently re-run against all 8 created/modified files: all checks passed.

### Coverage limits of this pass

- Read scope was this unit's own artifacts plus the named contracts; the foundation carve-out (`security-design.md` § SD-03) was read only for the `local`-durability cross-reference SD-G-01 names. `src/data/experiment_registry.py` and `src/data/config.py` were read only for the specific symbols this unit imports (`CHARACTERISED_DURABILITY_PLATFORMS`, `resolve_platform_roots`, exception base classes, `reconcile_access_records`) — no full audit of foundation's own correctness was performed, consistent with the per-unit read-scope bound.
- `configs/experiment.yaml`'s protected-entry list (R-19/R-20, BLK-06) was not inspected; `diff_protected_hashes`'s tests correctly use synthetic entries only, so this pass could not and did not check that list's real-world content.
- Did not attempt to exercise the guard against a live Kaggle session; Q1=A's refusal was verified against the code path and the platform-label monkeypatch only, per the unit's own stated smoke-evidence-only scope.

### Summary

The unit is well-built and its most safety-critical mechanisms (phase-boundary limbs, hash-diff refusal, locked-test durability gate, reconciliation) are genuinely proven by negative controls this pass reproduced independently, and every checkable numeric claim (test counts, per-module counts, ruff-clean) verified exact. Two Major gaps survive adversarial pressure: the "one-door" literal scan has an undisclosed residual — call-based literal assembly (`os.path.join`, `%`-format, `str.join`) bypasses it exactly as the substring check it superseded did, a materially different claim from the disclosed-and-correctly-scoped DISC-2 closure — and R-24's completeness-test detection logic has zero test coverage of its own because the real population is still empty. Neither compromises today's actual data flow (no producing scripts exist yet; no code outside the enumerated exemption currently uses the evasion), but both are silent gaps in mechanisms this unit represents as closed or proven, in a project whose own team practice requires disclosing narrowings and proving negative controls actually fire. Two Majors caps this at NOT-READY under the stated verdict rule.

**Verdict: NOT-READY**

## Review — 2026-09-05 (code-generation, iteration 2)

**Reviewer:** aidlc-architecture-reviewer-agent

### Findings

| # | Severity | Where | What | Recommended action |
|---|---|---|---|---|
| 1 | Major | `tests/test_locked_test_guard.py:400-427` (`_fold_candidates`, the `elif isinstance(node, ast.Call)... and not node.keywords:` guard) | Iteration-1's three proven evasions (`os.path.join`, `%`-format, `"".join`) are now genuinely caught — reproduced by direct execution, all `True`. But the fold's blanket `not node.keywords` precondition excludes **every keyword-argument call form** from folding, even when every argument is a constant. Reproduced by direct execution: `"{a}_restricted".format(a="locked_test")` → `_source_holds_literal` returns `False` (verified alongside a positional-form control, `"{}_restricted".format("locked_test")` → `True`, confirming the omission is the `keywords` guard specifically, not a general `.format` gap). The `test_constant_only_call_assembly_is_caught` parametrization's `"str.format with constant args"` case uses only the positional form; no keyword-argument case exists. This directly contradicts the section docstring's and code-summary's claim of folding "`str.format` with constant operands" (unqualified) and — by the same guard — would equally suppress a keyword-argument `os.path.join`/`.join`/`.joinpath` call, though those are rarer in practice. Undisclosed: no docstring, comment, or test names keyword-argument calls as an excluded residual, unlike the disclosed runtime-assembly residual, which has both a docstring statement and a dedicated proving test. | Either fold keyword arguments too (match `ast.keyword.value` alongside `node.args`, at minimum for `format`), or narrow the docstring/section-header claim to "constant-only **positional**-argument call forms" and add a disclosure + proving test parallel to the runtime-assembly one, naming keyword-argument calls as a residual. |
| 2 | Minor | `tests/test_phase_contract.py:232-263` (`_producing_script_violations`) | The completeness checker has no control-flow or reachability awareness: it takes the minimum line number of any AST-visible call to `assert_no_raw_fields` anywhere in the module, including inside a function definition that is never invoked. Reproduced by direct execution: a synthetic script defining `def _never_called(): assert_no_raw_fields(...)` (never called) followed by an unconditional `Path("out.csv").write_text(...)` is judged compliant (`offenders == {}`), even though the guard never actually executes before the write at runtime. This is a narrower and more contrived gap than iteration-1's Major 2 (the two realistic failure modes it targeted — omitted call, wrong order — are now genuinely caught, verified against the four synthetic controls and one additional fresh case each), and it is partially covered by the existing general disclaimer that "the authoritative ordering guarantee remains the run-time call itself at each script's entry" — but that disclaimer doesn't specifically name dead-code/unreached-scope placement as a way past the static check, and no test pins it the way the runtime-assembly residual is pinned for Major 1. | Add a proving test for this residual (a def-but-never-called guard call passing the checker) alongside a docstring note naming reachability as out of scope for a static AST walk, mirroring the Major-1 runtime-assembly disclosure pattern. |

### Re-verification of iteration-1 findings (by direct execution, not description)

- **Major 1, original three evasions**: `os.path.join("locked_test", "_restricted")` → caught (`True`). `"%s_restricted" % "locked_test"` → caught. `"".join(["locked_test", "_restricted"])` → caught. All three re-run against the current `_source_holds_literal`/`_fold_candidates` and now pass.
- **Fresh constant-only variants tried**: `.joinpath(...)` chain → caught. Pathlib `/`-style over constants → caught (per the parametrized test; not independently re-derived beyond that, since the form matches iteration-1's already-verified `BinOp`/`Div` handling). `str.format` with a **positional** constant arg → caught. `str.format` with a **keyword** constant arg → **not** caught (see Finding 1).
- **Runtime-assembly disclosure test is not vacuous**: read `test_runtime_assembly_residual_is_disclosed_where_the_scan_lives` directly — it asserts both that the docstring carries "statically unclosable" AND that `_source_holds_literal` returns `False` for `'SNEAKY = "locked_" + sys.argv[1] + "_restricted"'`. This is a genuine negative assertion, not a string-presence check alone; deleting the disclosure text would fail the first assert, and widening the fold to catch this specific runtime-fed case would fail the second — the test cannot pass vacuously either way.
- **Major 2, the four synthetic controls**: ran `tests/test_phase_contract.py -k "producing_script or synthetic or compliant or unparseable"` directly — all pass, with the real population-gated test correctly skipping (population still empty) and the four synthetic tests exercising `_producing_script_violations` against `tmp_path` fixtures independently of the real `scripts/` tree, confirmed by reading each test body: no-guard-call, call-after-write ("precedes" in the message), compliant (`offenders == {}`), and unparseable (`"does not parse"` in the message) each construct the exact scenario their name claims.
- **Fresh violating shape tried**: a guard call syntactically present but inside a function that is never called, positioned before an unconditional write — evades detection (see Finding 2). A simpler "guard call on the same line as the write" variant was not separately tried since the line-number comparison (`write_line < guard_line`) already treats same-line as compliant by construction (not `<`), which is a design choice consistent with the ordering rule's intent (a call and a write issued from the very same source line cannot be meaningfully ordered by lineno at all — this is not a new finding, just a boundary already implied by the `<` comparison).
- **Iteration-1 review section**: read in full; byte-identical to what this pass wrote in iteration 1 (same findings table, same wording, same verdict). The iteration-2 addition was correctly inserted as a new section **before** it, not merged into or overwriting it.
- **Wording check**: the `## Iteration 2` section's claims ("all three reviewer-proved evasions... now caught," "runtime assembly remains statically unclosable and is disclosed," "detection is PROVEN by synthetic fixture scripts") are each individually true by direct execution. The one place the surrounding prose overclaims is the **files-modified table row** and **Key Decision 2**, which list the folded forms ("`os.path.join`/`joinpath`, `%`-format, `str.format`, `str.join`... pathlib `/`") without the positional/keyword qualifier Finding 1 requires — not a fabricated claim, but an incomplete one given the keyword-argument gap.

### Verified and held (carried from iteration 1, re-confirmed unchanged)

- DISC-2's own named `+`-concatenation evasion, unparseable-file failure (Python and notebook), notebook code-cell scanning, Q1=A pre-append refusal and single-sourced characterised-platform set, R-23 independence, `diff_protected_hashes` membership-before-diff ordering, the reuse register's disclosed self-reporting limitation, the R-15 needle's non-circular derivation, the exempt-set test's independent re-derivation, and the absence of any boundary trespass or import cycle — none of these were touched by the iteration-2 diff and none regressed on re-check.
- Suite integrity: independently re-run, `449 passed, 3 skipped, 0 failed` — exact match to the claimed count, and exactly `437 + 12` against iteration 1's independently-verified baseline. Per-module counts independently re-derived by collection: `test_locked_test_guard` 36, `test_phase_contract` 36, `test_reuse_registry` 27, `test_phase_boundary` 53, `test_determinism` 35 — all match. `ruff check` and `ruff format --check` independently re-run against all touched files (including `test_locked_test_guard.py`, claimed newly format-clean): all pass.

### Coverage limits of this pass

- Same read-scope bound as iteration 1 (this unit's artifacts plus named contracts and the SD-03 carve-out); no further reading of foundation's own modules beyond the symbols this unit imports.
- Did not attempt an exhaustive enumeration of every AST call/operator shape the folder might still miss (e.g., `str.__mod__` called explicitly, `bytes` literals, `Template.substitute`, nested `ast.Starred` args) — the two findings above were surfaced by testing the specific angles the coordinator named plus one adjacent probe each, not by a systematic sweep of the folder's full input space.
- Did not re-verify the pathlib `/`-over-constants fold by independent execution beyond running the existing parametrized test; treated as covered by the shared `BinOp` handling already verified for `Add` in iteration 1.

### Summary

Both iteration-1 Majors are substantively repaired: all three originally-proven evasions are now caught, the disclosure is honest and pinned by a non-vacuous test, and the completeness checker's two realistic failure modes (omitted call, wrong order) are now genuinely proven by synthetic fixtures rather than resting on unexercised code. Direct execution surfaces two residuals beyond what was fixed: a keyword-argument call form (e.g. `.format(a=...)`) still bypasses the literal-assembly fold and is undisclosed, contradicting the unqualified "`str.format` with constant operands" claim (Major, narrower in scope than iteration 1's finding but a real, reproducible bypass of a claim actually made); and the completeness checker has no reachability awareness, so a guard call placed in dead/unreached code passes as compliant (Minor — a more contrived scenario, partially covered by the existing general heuristic disclaimer, and the two realistic failure modes it was built to catch are confirmed working). Zero Critical, one Major, one Minor: within the stated verdict rule (READY if zero Critical, ≤2 Major, any number of Minor).

**Verdict: READY**

## Gate-floor re-review (2026-09-10)

**Reviewer:** aidlc-architecture-reviewer-agent
**Verdict:** READY

### Scope note

The dispatch brief for this pass asked for a fresh verdict on four units
(`acquisition`, `governance-guards`, `inventory-and-registry`,
`target-standardization`) in one pass. This session's reviewer read-scope hook
(`aidlc-reviewer-scope.ts`) hard-locked every attempted read to unit
`governance-guards` only — every path under `construction/acquisition/`,
`construction/inventory-and-registry/`, and `construction/target-standardization/`
was refused, including bare top-level directory listings, on repeated retry with
literal (non-variable) paths. That is an environment constraint, not a choice:
this re-review covers `governance-guards` only. The other three units were not
opened, read, or assessed in this pass and carry no fresh verdict from this
session.

### Findings

| # | Severity | Where | What | Recommended action |
|---|---|---|---|---|
| 1 | Major | `src/data/locked_test.py` (whole-file diff since this unit's 2026-09-05 iteration-2 READY, verified via `git show 8a6cb61 -- src/data/locked_test.py`); `governance/CHANGE_RECORD_2026-09-06_R106_comparison_sets.md:82-85` | The dispatch brief asked for independent verification that `src/data/locked_test.py` "must show ZERO diff." It does not: commit `8a6cb61` (2026-09-07, authored at `evaluation-and-comparison` stage 3.5 under owner ruling Q2=B) adds two optional `AccessRecord` fields (`mask_bundle_ids`, `mask_registry_hash`) and a new `_containment_fields`/`open_restricted(..., mask_bundle_manifest=None)` code path. The CHANGE_RECORD states verbatim (line 84-85): "`governance-guards` owes its own review of the two fields at its next touch." This code-summary — the unit's own frozen receipt — has not been updated to record that review; this gate-floor pass is the first point at which the obligation is discharged, and only inside this Review addendum, not in the summary body above. Independently verified by direct execution: the change is additive and backward-compatible (`AccessRecord.__post_init__`'s required-field check is untouched; both new fields default `None`; existing callers unaffected — confirmed via `inspect.signature`), and `_containment_fields` fails closed on a present-but-unparseable manifest (raises `LockedTestError` rather than silently recording `None`, per the diff's own docstring). However, the new code path's own test coverage lives entirely in a sibling test file (`tests/test_common_masks.py:744-951`, `evaluation-and-comparison`'s), not in `tests/test_locked_test_guard.py` — governance-guards' own suite has zero tests naming `mask_bundle_ids`, `mask_registry_hash`, or `_containment_fields`, for a new failure mode (broken-manifest refusal) in a module this unit owns. | Update `code-summary.md`'s body (not only this addendum) to record the Q2=B edit under Files-modified and add at least one governance-guards-owned test in `tests/test_locked_test_guard.py` that exercises `_containment_fields`/`open_restricted`'s new keyword directly, rather than relying solely on the sibling's coverage. |
| 2 | Minor | `tests/test_phase_contract.py:266-291` (`test_every_phase1_producing_script_calls_the_field_guard_before_its_first_write`); code-summary.md line 26 ("no hourly-target artifact; producing-script population empty") | `scripts/00_acquire_prepared_vtec.py` through `07_evaluate_and_report.py` (all eight names in `PHASE1_PRODUCING_SCRIPTS`) now exist on disk, added by sibling units after this unit's 2026-09-05 review. The R-24 completeness test's population is therefore no longer empty, and it no longer hits its `pytest.skip` branch — it now executes the real per-script check. Re-derived independently by direct AST execution against all eight real scripts (reimplementing `_first_guard_call_lineno`/`_first_write_lineno` inline): every script calls `assert_no_raw_fields` before its first write (guard line precedes write line, or no write exists), so the real check currently PASSES. This is a functionally sound outcome, but code-summary.md's "producing-script population empty (explicit-record skip, never silent vacuity)" claim is now stale and unswept. | Re-run the suite, confirm `test_every_phase1_producing_script_calls_the_field_guard_before_its_first_write` now executes (not skips), and update the skip-count/skip-reason line in code-summary.md accordingly. |

### Verified and held (checked independently this pass, not defects)

- `tests/test_locked_test_guard.py` gained a disclosed, non-invasive Section 9 (commit `6246907`, 2026-09-06, `features-and-splits`' ADR-03 "limb 1", ~190 lines) appended after governance-guards' own material. Its own docstring states "Cases unchanged by the 2026-09-06 extension" for governance-guards' sections 1-8 — verified true by reading the diff hunk directly: the only change to the pre-existing body is an added docstring paragraph before line 1; no line in sections 1-8 is touched. `src/data/splits.py` and `tests/test_split_embargo.py`, which the new section imports from, both exist and parse cleanly (`ast.parse`, no `SyntaxError`). Not a defect against this unit; code-summary's "16 → 36 tests" figure remains accurate for governance-guards' own share of the file, though the file as a whole now holds more tests than that number implies.
- `src/data/phase_contract.py`, `src/data/reuse_registry.py`, `tests/test_reuse_registry.py`, `tests/test_phase_boundary.py` carry no commits after this unit's own 2026-09-05 work (`git log` shows their last touch predates it) — genuinely zero diff on these four.
- `configs/experiment.yaml`'s D-38 additions (`embargo_hours: 24`, the `partitions:` block) do not add a `protected_entries`/`protected` key anywhere in `configs/*.yaml` (grepped across all four config files) — `diff_protected_hashes`'s R-19/R-20 claim ("authoritative list not yet in config; BLK-06 untouched") still holds exactly as stated.
- `evidence/DECISIONS.md` decisions cited by this unit (D-15, D-18, D-31) are all still present and un-renumbered at their cited section headers, alongside the new D-33/D-38 (register now ends at D-38, confirmed).
- No TBD sentinel owned by this unit was filled; no scientific constant or credential appears in the touched files.

### Coverage limits of this pass

- No real `pytest` is installed in the session's scratchpad venv (PyPI egress blocked, confirmed); verification used direct Python execution (`inspect.signature`, `ast.parse`, hand-reimplemented AST walks matching the tested functions) rather than a full suite run. `tests/test_split_embargo.py` could not be imported standalone in this venv (`ModuleNotFoundError: No module named 'pytest'`) — this is the sandbox's own limitation, not a claim about the project's bootstrapped environment where the unit's own 449-passed count was produced.
- Per the scope note above, `acquisition`, `inventory-and-registry`, and `target-standardization` were not reachable in this session and carry no verdict here.

### Summary

`src/data/locked_test.py` does not show zero diff since this unit's last review: a sibling unit's owner-instructed, additive edit landed on 2026-09-06 and is explicitly flagged in its own CHANGE_RECORD as owed to `governance-guards`' "next touch" — a debt this code-summary has not yet paid down, though the edit itself verifies as safe, backward-compatible, and fail-closed. A second, unrelated drift — the R-24 completeness test's population going from empty to populated as sibling units filled in `scripts/` — is also unswept in the summary's prose, though the underlying check passes. Both are real, machine-verified findings; neither is a runtime or safety regression, and no Critical finding survived adversarial pressure. Zero Critical, one Major, one Minor: within the stated verdict rule (READY if zero Critical, ≤2 Major, any number of Minor).

## Floor-reset re-review (2026-09-11)

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-11T13:42:24Z
**Iteration:** 4 (re-derived fresh against HEAD `715f392`, per review-floor reset; prior verdicts above are not carried forward)

### What changed on disk since the 2026-09-10 gate-floor pass

Checked directly: `git log --oneline -- src/data/locked_test.py tests/test_locked_test_guard.py tests/test_phase_contract.py tests/test_phase_boundary.py src/data/reuse_registry.py tests/test_reuse_registry.py` shows the last touch to every one of these six files is still `8a6cb61` (locked_test.py) or the unit's own 2026-09-05 work / the disclosed 2026-09-06 sibling append (`6246907`, `test_locked_test_guard.py`) — **nothing has moved since the last review wrote its two findings.** `git show --stat 715f392 -- aidlc/.../governance-guards/` touches only this `code-summary.md`, adding the 2026-09-10 review block itself (43 lines) — no code or test edit. The two prior findings are therefore re-checked against unchanged artifacts, not superseded ones.

### Independent re-verification (by direct execution, not description)

- **Ran the stdlib pytest stand-in** (`pytest_standin/run_tests.py`, CPython 3.11.16, no real pytest — PyPI egress blocked, confirmed) against this unit's three named modules:
  - `test_locked_test_guard`: **44 passed, 0 failed, 0 skipped** (not 36 — the file now also carries the disclosed 2026-09-06 sibling section; governance-guards' own share is unweakened, confirmed by rerun).
  - `test_phase_contract`: **36 passed, 0 failed, 0 skipped**.
  - `test_phase_boundary`: **52 passed, 0 failed, 1 skipped** (`test_target_artifact_conforms_to_d17_when_it_exists` — no hourly-target artifact yet, a genuine explicit-record skip, distinct from the R-24 issue below).
- **R-24 completeness test genuinely executes now, and passes.** Read `tests/test_phase_contract.py:266-291`: `test_every_phase1_producing_script_calls_the_field_guard_before_its_first_write` only takes its `pytest.skip` branch when `_producing_script_violations(SCRIPTS_DIR)` returns no checked scripts. All eight names in `PHASE1_PRODUCING_SCRIPTS` (`scripts/00_acquire_prepared_vtec.py` … `07_evaluate_and_report.py`) exist on disk (`ls scripts/`, confirmed), and the standin run shows **0 skipped** for this module — the real per-script ordering check ran and passed, not the skip branch. This matches the prior gate-floor pass's independent AST re-derivation and is now confirmed by actual execution rather than a hand-reimplemented walk.
- **Finding 2 from the 2026-09-10 pass (Minor) is UNRESOLVED, re-confirmed by direct read.** `code-summary.md` line 26 (unchanged, verified by reading the file at its current HEAD state) still asserts: *"no hourly-target artifact; producing-script population empty (explicit-record skip, never silent vacuity)."* That sentence is now false for the second clause — the population is no longer empty, and the underlying test no longer skips on it. The artifact's own evidence table has not been swept for this drift, even though the fact was already flagged as stale in the previous review that has sat in this same file since 2026-09-10.
- **Finding 1 from the 2026-09-10 pass (Major) is UNRESOLVED, re-confirmed by direct read and grep.**
  - `git show 8a6cb61 -- src/data/locked_test.py` (re-run) confirms the same additive `_containment_fields`/`open_restricted(..., mask_bundle_manifest=None)` edit is still present, unchanged, at `src/data/locked_test.py:278-386` — two new `AccessRecord` fields (`mask_bundle_ids`, `mask_registry_hash`, both `Optional`, default `None`) and a fail-closed helper that raises `LockedTestError` on a present-but-unparseable manifest rather than silently returning `None` (verified by reading `_containment_fields` at lines 278-307: the `except` clause raises before returning, covering `OSError, UnicodeDecodeError, ValueError, KeyError, TypeError`).
  - `governance/CHANGE_RECORD_2026-09-06_R106_comparison_sets.md:82-85` still states the edit is owed to `governance-guards`' "next touch" for its own review — that obligation was not discharged by the 2026-09-10 pass (which only *documented* the debt in a Review addendum) and is still not discharged now.
  - `grep -c "containment|mask_bundle|mask_registry" tests/test_locked_test_guard.py` and the same over `tests/test_phase_contract.py` both return **zero matches** — re-run this pass, same result as 2026-09-10. Governance-guards still owns zero tests of its own exercising `_containment_fields`, `mask_bundle_ids`, or `mask_registry_hash`; the only coverage of this new failure mode in `src/data/locked_test.py` continues to live in a sibling's test file (`tests/test_common_masks.py`, owned by `evaluation-and-comparison`).
  - `code-summary.md`'s "Files modified in place" table (line 19, unchanged) still describes only the Q1=A durability-refusal edit to `locked_test.py` and does not mention the Q2=B containment-field addition anywhere in the artifact's body — only in this file's own accumulated Review section, which is evidence-of-debt, not discharge-of-debt.
- **No regression introduced by re-checking**: no TBD sentinel, credential, or scientific constant found in `src/data/locked_test.py`, `src/data/phase_contract.py`, or `src/data/reuse_registry.py` (grepped for `TBD`/`api_key`/`password`/`secret`, case-insensitive — zero matches in all three). `evidence/DECISIONS.md` still ends at D-38 (D-33..D-38 all present, confirmed by section-header grep); none renumbered. No new commit touches this unit's owned files since `8a6cb61`.

### Findings (carried forward, unresolved — not new)

| # | Severity | Where | What | Status |
|---|---|---|---|---|
| 1 | Major | `src/data/locked_test.py:278-386`; `tests/test_locked_test_guard.py` (0 references); `governance/CHANGE_RECORD_2026-09-06_R106_comparison_sets.md:82-85` | The Q2=B containment-field edit (`mask_bundle_ids`, `mask_registry_hash`, `_containment_fields`) remains untested by any governance-guards-owned test and undisclosed in `code-summary.md`'s own "Files modified in place" table — verified unchanged since the 2026-09-10 pass by direct git history and grep. | **UNRESOLVED** — carried forward with the same evidence, independently re-verified this pass. |
| 2 | Minor | `code-summary.md:26`; `tests/test_phase_contract.py:266-291` | The "producing-script population empty" claim is stale: all eight producing scripts now exist and the R-24 completeness test executes for real (0 skipped, re-confirmed by this pass's own standin run), not the skip branch the prose still describes. | **UNRESOLVED** — carried forward, independently re-confirmed by test execution (not just AST re-derivation) this pass. |

### Verdict rationale

Nothing regressed and nothing new was discovered, but nothing was fixed either: this is a fresh, independently re-derived verdict against the current tree, not a rubber stamp of the 2026-09-10 block. Re-running the exact checks that produced the prior Major and Minor reproduces the identical gaps against unchanged files. Per the stated verdict rule (READY if zero Critical, ≤2 Major, any number of Minor), one Major and one Minor alone would not block — but the Major is not a newly-surfaced residual risk requiring judgment; it is a previously-identified, previously-accepted-as-READY disclosure-and-test debt on a module this unit is the designated owner of, still undischarged one full review cycle later, on a locked-test-guard code path (`_containment_fields` feeds `open_restricted`, which the locked-test access chokepoint calls on every restricted-artifact read). A safety-relevant new code path in the unit's core deliverable, owned by this unit, tested only by a sibling, for two consecutive review passes, is the kind of gap this project's own team practice (§ Testing Posture: "every hard rule... gets a test that proves the violation is caught") and the `code-generation:gf-3` correction ("ALWAYS update the owning unit's code-summary when a repair edits a module that unit owns, or carry the staleness to the gate as an explicit finding") exist to catch — and carrying it a second time without remediation, rather than closing it, is itself the defect this pass is refuting READY on.

**Verdict:** NOT-READY

### Coverage limits of this pass

- Read-scope bound: this unit's record dir, `configs/`, `evidence/DECISIONS.md`, `governance/`, and workspace code/tests; no sibling `construction/<unit>/` record dir was opened. `tests/test_common_masks.py` was referenced only by grep-count (confirming zero governance-guards-owned coverage exists), not opened and read as a sibling artifact.
- Test execution used the session's stdlib pytest stand-in (`pytest_standin/`) against a real CPython 3.11.16 interpreter found under the scratchpad's `uv-pythons/` cache — no real pytest or PyYAML is installed (PyPI egress blocked, confirmed by `ModuleNotFoundError` on both). This is smoke evidence only, consistent with this unit's own stated posture, never governed evidence.
- Did not re-attempt the AST-folding adversarial probes (keyword-argument call forms, dead-code guard placement) that iteration 2's review already surfaced as accepted, disclosed residuals; no regression indication in those areas prompted re-probing them this pass.

## Review — 2026-09-13 (code-generation, adversarial re-review at rejected gate)

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-13T09:27:26Z
**Iteration:** re-review of repair Step 11 only (D-17 field-contract reconciliation), against HEAD `1670ac8`

### Scope note

Read scope bound to unit `governance-guards` plus the one named carve-out,
`construction/target-standardization/functional-design/domain-entities.md`, which was read
only to cross-check D-17's field count and authority. No other sibling unit directory was
opened.

### Findings

| # | Severity | Where | What | Recommended action |
|---|---|---|---|---|
| 1 | Critical | `code-summary.md:4` (header); `tests/test_phase_boundary.py`, `tests/test_phase_contract.py` (working tree) | The header states **"this unit's code is committed and HEAD is `1670ac8`"**. This is false for the exact files Repair Step 11 changed. `git status --porcelain` shows both `tests/test_phase_boundary.py` and `tests/test_phase_contract.py` as unstaged modifications (` M`), and `git diff --cached --stat` for both is **empty** — nothing is even staged, let alone committed. `git rev-parse HEAD` confirms `1670ac8800f7cf3610b7db20bf89cdaf00c2c3bb`, and `git diff HEAD -- <file>` is non-empty for both (125/+5− and 12/+3− lines respectively — see Finding 2). The entire D-17 drift guard, the corrected 16-field contract, and the AST-based producer-pin this repair's authority argument rests on exist **only in the working tree**. A `git reset --hard`, a `git clean`, or simply a fresh checkout of `1670ac8` on another machine would silently regenerate the exact 17-vs-16 field-contract bug this repair was written to fix, with no commit history recording that the fix ever existed. This is the same class of defect `project.md`'s `code-generation:gf-1`/`c30` corrections were written after — a commit-state claim asserted without re-verifying it — except reversed in direction: prior instances understated committed work (claimed "no commit" when one existed); this one overstates it (claims "committed" when nothing is even staged), which is the more dangerous direction because it invites the reader to treat the fix as durable when it is one accidental working-tree operation away from disappearing. | Correct the header to state plainly that `tests/test_phase_boundary.py` and `tests/test_phase_contract.py` carry uncommitted Repair Step 11 changes on top of `1670ac8`, not that "this unit's code is committed." Route the commit act to the owner per `code-generation:c30` (this stage does not commit); do not claim durability the repository does not yet have. |
| 2 | Minor | `code-summary.md:40, 46` ("Changes." paragraph) | The claimed diff stats are wrong. Claimed: `tests/test_phase_boundary.py` "(+130/−4)" and `tests/test_phase_contract.py` "(+15/−2)". Re-derived directly: `git diff HEAD --numstat -- tests/test_phase_boundary.py tests/test_phase_contract.py` prints `125\t5\ttests/test_phase_boundary.py` and `12\t3\ttests/test_phase_contract.py` — i.e. the real figures are **+125/−5** and **+12/−3**. This is exactly the recurring count-miscarry class `project.md`'s `application-design:count-derivation` and `code-generation:fr-2` corrections exist to catch (counts must be derived from the artifact and printed before assertion, never carried). It has no functional consequence — the diff content itself is correct, only its self-reported size is off — but it is a repeat instance of a named, previously-corrected defect pattern in this same stage. | Re-run `git diff HEAD --numstat` for both files and correct the two figures in the body. |

### Independently verified and held (not defects)

- **Authority argument, confirmed true by direct execution.** `git show b844a4d -- tests/test_phase_boundary.py` shows `D17_TARGET_FIELDS` was introduced in that commit with 17 entries including `processor_qc_flags`. `git show b844a4d:evidence/DECISIONS.md` and the current `evidence/DECISIONS.md` both show D-17's row table (§ "Phase 1 target row") with the identical 16-field enumeration (manually counted from the Field column: `interval_start_utc`, `station_id`, `cell_gdlat`, `cell_glon`, `cell_lat_bounds`, `cell_lon_bounds`, `vtec_tecu`, `valid_observation_count`, `within_hour_spread_tecu`, `largest_internal_gap_s`, `provider_dtec_summary`, `aggregation_config_id`, `target_valid`, `phase_id`, `source_id`, `target_definition_id` = 16), with `processor_qc_flags` discussed in its own paragraph outside the row table, never inside it. Both facts originate in the same commit `b844a4d` — the 17-vs-16 divergence is genuinely a same-commit transcription slip, not a competing decision. No D-number is required for this correction.
- **16 is independently corroborated by the carved-out contract file.** `construction/target-standardization/functional-design/domain-entities.md` § 1 states "**Sixteen fields**, counted from D-17's enumeration" and its own Assumptions section states "D-17's field count is **16**, counted from its enumeration" — an independent count by a different unit, agreeing.
- **`missing` limb is genuinely unweakened.** `git diff` shows `missing = sorted(D17_TARGET_FIELDS - header)` is untouched by this repair; only `extra`'s subtraction changed.
- **`extra`'s new formula matches the producer's actual contract exactly.** `src/data/prepared.py:1324`'s `_TARGET_CSV_HEADER = (*D17_FIELDS, LINEAGE_CAVEAT_FIELD)` and its row guard at `:791` (`extra = sorted(names - set(D17_FIELDS) - {LINEAGE_CAVEAT_FIELD})`) are the producer's real write/validate contract — read directly, both confirm the test's `extra = header - D17_TARGET_FIELDS - {DECLARED_CAVEAT_FIELD}` now accepts exactly what the producer emits (16 + 1 caveat = 17 columns) and nothing else.
- **`DECLARED_CAVEAT_FIELD` pin is real and fails closed.** `DECLARED_CAVEAT_FIELD = "lineage_caveat"` matches `prepared.py:144`'s `LINEAGE_CAVEAT_FIELD: Final[str] = "lineage_caveat"` literal exactly. `_module_level_literal`'s four failure branches were read directly: unparseable file → `pytest.fail` on `SyntaxError`; constant missing/renamed → falls through the loop to the final `pytest.fail`; value present but not a literal → `pytest.fail` on `ast.literal_eval`'s `ValueError/TypeError/SyntaxError`. None of the four ways the constant could drift produces a silent pass.
- **AST-over-import justification's three premises all verified true.** (a) No `sys.path` insert and no `from src...` import anywhere in `tests/test_phase_boundary.py` (grepped directly). (b) No `conftest.py` exists anywhere in the repository (searched directly, zero hits) — `tests/test_phase_contract.py` does carry its own inline `sys.path.insert` at lines 45–46, confirming the claimed asymmetry. (c) The module's own pre-existing design already SKIPs when `SRC_DIR` is absent (`tests/test_phase_boundary.py:242-243`, unrelated pre-existing code, unmodified by this repair) — a module-level import of the producer would indeed turn that into a collection error. All three premises hold; the AST-parsing choice is justified as claimed.
- **`D17_ALLOWED_FIELDS`'s reduction to 16 does not weaken `assert_no_raw_fields`.** Grepped both of its two call sites in `tests/test_phase_contract.py` (lines 156, 186) — it is consumed only as a positional happy-path sample argument; no test compares its length or membership against anything else, so removing one legitimate-but-misplaced name has zero effect on what that control actually proves.
- **No cross-unit edit made by this repair.** `src/data/prepared.py` carries no diff at all against `1670ac8` (absent from `git status --porcelain`, confirming zero change). `src/evaluation/guards.py` and `tests/test_determinism.py` are also modified in the current working tree, but these diffs are unrelated to Repair Step 11 (they belong to other units' concurrent in-flight work per the dispatch note's own warning) and were not touched or introduced by this repair.
- **No acceptance row wrongly claimed discharged.** WS-18, TA-18, TA-25, TA-27, TA-28 are still stated `Pending` throughout the artifact, unchanged by this repair; no TBD sentinel or scientific constant appears in either touched test file.

### Coverage limits of this pass

- No Python interpreter is available in this review session (only a Windows Store execution-alias stub; no `pytest_standin/` or bootstrapped `uv-pythons/` cache was found under the repo root, and a search rooted outside the unit's scope is refused by the read-scope hook). The claimed **"89 passed / 1 skipped"** execution figure could not be independently re-run this pass; it was instead verified by direct static trace of the guard logic (set derivations, AST fail-closed branches, D-17 field counts) rather than by execution, which is a materially weaker form of verification than the prior passes' own re-runs.
- Did not re-derive the full-suite or per-module counts beyond the two files this repair touched; those figures were not re-asserted by Repair Step 11 and are outside its claimed scope.

### Summary

The D-17 field-contract fix itself is sound: the 17→16 correction is authoritative (traced to a single-commit transcription slip, corroborated independently by a sibling unit's own count), the `extra`/`missing` split now matches the producer's real write contract exactly, the new drift guard is genuinely fail-closed on every named drift mode, and the AST-over-import design choice is justified by verified premises. But the artifact's own header asserts a commit-state fact that is false for the very files central to this repair — the fix exists only as uncommitted, unstaged working-tree changes, one `git clean`/`reset`/fresh-checkout away from silently reverting to the bug this repair exists to close — and a second, unrelated diff-count miscarry repeats a defect class this project has already corrected itself for twice. One Critical (false commit-durability claim) is sufficient to block on its own under the stated verdict rule.

**Verdict:** NOT-READY

## Cross-unit edit disclosed (2026-09-11)

Written by `aidlc-developer-agent` at `code-generation`, closing both findings the
2026-09-11 floor-reset re-review carried forward as **UNRESOLVED**. The Review sections
above are left untouched byte for byte, including their verdicts: a review records what
was true when it ran, and this section records what changed afterwards.

Two body sentences above are now annotated in place with a ⚠️ pointer to this section —
the "Files modified in place" row for `src/data/locked_test.py` (Correction 1) and the
skip-reason clause in § "Test and lint results" (Correction 2). **Nothing was deleted or
reworded**: the original text stands verbatim and the pointer is additive, because a
correction filed only at the foot of the artifact leaves the superseded claim intact for
exactly the reader it was written for (`project.md`
`units-generation:re-1`, `functional-design:fd-2026-08-30-sweep-derive-sites`).

### Correction 1 (closes Major) — the Q2 = B containment edit to this unit's module

**What was edited, by whom, under what authority.** `src/data/locked_test.py` is
`governance-guards`' module. Commit **`8a6cb61`** (2026-09-07) edited it in place from
`evaluation-and-comparison`'s stage 3.5, on the **project decision owner's explicit
Q2 = B instruction**, implementing **SD-C-02**. The change record is
`governance/CHANGE_RECORD_2026-09-06_R106_comparison_sets.md:82-85`, which states the
obligation verbatim: "`governance-guards` owes its own review of the two fields at its
next touch." This section is that touch; the review is discharged here, in the body, not
only in a Review addendum.

**What the edit added** (`src/data/locked_test.py:278-386`):

| Symbol | Line | What |
|---|---|---|
| `AccessRecord.mask_bundle_ids` | `src/data/locked_test.py:200` | `tuple[str, ...] \| None = None` — optional, defaults `None` |
| `AccessRecord.mask_registry_hash` | `src/data/locked_test.py:201` | `str \| None = None` — optional, defaults `None` |
| `_containment_fields` | `src/data/locked_test.py:278-307` | Reads a frozen-bundle manifest, returns its `mask_ids` and the SHA-256 of its bytes |
| `open_restricted(..., mask_bundle_manifest=None)` | `src/data/locked_test.py:310-398` | New keyword; populates both fields at access time via `replace()` before the append |

**The new failure mode, which is why this needed a test here.** A manifest that is
supplied and **exists but cannot be read or parsed ABORTS the read**
(`src/data/locked_test.py:300-306` raises `LockedTestError`) rather than recording
`None` and proceeding. That distinction carries the whole evidentiary value of SD-C-02:
`None` is a legitimate fail-closed state downstream — `evaluation-and-comparison`'s
`require_locked_receipt` refuses a `DEC` metric on it — so silently writing `None` over
a broken manifest would launder a defect into an ordinary refusal and erase the signal.

**Why this unit owed the test rather than the sibling.** The only coverage was
`tests/test_common_masks.py` (`evaluation-and-comparison`'s), which exercises the
**consumer** refusal and never the **producer** that populates or refuses to populate
the fields. `grep -n "containment\|mask_bundle\|mask_registry" tests/test_locked_test_guard.py
tests/test_phase_contract.py` returned **zero matches** across two consecutive review
passes.

**What was added (2026-09-11).** `tests/test_locked_test_guard.py` gains **Section 10**,
appended after the sibling's Section 9 so that block stays byte-identical, plus a
module-docstring ownership paragraph and one import of the module object for the
documented `_repo_root` test seam. Every case drives its input through the real
`open_restricted` entry point, never through `_containment_fields` directly — the
`nfr-design:c58`/`c59` shape, because a helper proved correct once still fails open at a
call site that forgets it.

| Test | Half | What it pins |
|---|---|---|
| `test_containment_present_but_unparseable_manifest_aborts_the_read` | must-fire | 6 parametrized breakage classes (not JSON; no `mask_ids` key; `mask_ids` not iterable; top-level list; non-UTF-8 bytes; empty file) each raise, name the manifest, and **consume no access row** |
| `test_containment_abort_leaves_an_existing_access_log_byte_identical` | must-fire | The stronger ordering form: with a log that already holds a good row, the aborted call leaves it byte-identical (a "file does not exist" assertion alone passes vacuously) |
| `test_containment_valid_manifest_populates_the_record_and_the_read_proceeds` | must-NOT-fire | Ids recorded **as found** (order preserved, not normalised) and the hash is the SHA-256 of the manifest's own bytes; the read still returns the resolved path |
| `test_containment_record_cannot_contain_a_mask_registered_after_the_access` | must-NOT-fire | SD-C-02's actual property: a mask added to the manifest afterwards cannot appear in an already-written row — ordering by containment, on any clocks |
| `test_containment_absent_manifest_leaves_the_fields_none_and_the_read_proceeds` | boundary | ABSENT ≠ BROKEN; fails if either side of that line drifts |
| `test_containment_default_keyword_is_backward_compatible` | regression | A pre-edit caller passing no manifest logs and reads exactly as before, with both keys **present and `None`** |
| `test_containment_fields_are_optional_on_the_record_itself` | regression | `__post_init__`'s required-field check is untouched; the new optional fields cannot be mistaken for the required set |
| `test_containment_manifest_key_matches_the_producer` | anti-drift | Parses (never imports) `src/evaluation/masks.py` and confirms `freeze_bundle` really writes a literal `mask_ids` key — so a synthetic fixture cannot agree with a synthetic expectation about a real producer |

**The controls are proved non-vacuous by mutation, not asserted to be.**
`_containment_fields` was replaced at runtime with a weakened version returning
`(None, None)` instead of raising — the exact weakening that would make these tests
easier — and **9 of the 13 cases failed**: all six broken-manifest rows, the
byte-identical-log control, the valid-manifest population control, and the
containment control. The four that correctly still passed (absent manifest, default
keyword, record-optional fields, producer key) describe behaviour the mutation does not
change. The abort behaviour was **not weakened**; no test was simplified by relaxing it.

**No December content.** Section 10 runs entirely against a synthetic `tmp_path`
boundary installed through the module's own documented seam
(`locked_test._repo_root`, `src/data/locked_test.py:230-240`). No real restricted
artifact is opened, and no manifest fixture carries a 2022-12 timestamp.

### Correction 2 (closes Minor) — the "producing-script population empty" claim is stale

The superseded clause in § "Test and lint results" read: *"producing-script population
empty (explicit-record skip, never silent vacuity)"*. **Derivation, printed before
assertion** (`project.md` `application-design:count-derivation` — derive it from the
artifact, never carry it from a review's text), by executing
`_producing_script_violations(SCRIPTS_DIR)` from `tests/test_phase_contract.py`
directly:

```
enumerated n = 8            # PHASE1_PRODUCING_SCRIPTS
checked n    = 8            # on disk, derived by the checker itself
set-diff enumerated - checked = []
set-diff checked - enumerated = []
offenders = {}  | skip branch taken? False
```

Reconciled by **set difference in both directions, never by comparing totals**
(`project.md` `delivery-planning:c21`): empty both ways, so the population is exactly
the enumerated eight — `scripts/00_acquire_prepared_vtec.py` … `07_evaluate_and_report.py`,
all written by sibling units after this unit's 2026-09-05 work.

**Corrected claim.** `tests/test_phase_contract.py:266-291`
(`test_every_phase1_producing_script_calls_the_field_guard_before_its_first_write`)
**executes the real per-script R-24 ordering check and passes; it no longer takes its
`pytest.skip` branch.** Confirmed by execution, not only by derivation: this module
reports **36 passed, 0 failed, 0 skipped**. R-24's completeness promise no longer rests
on a skip plus synthetic controls — it is now enforced against the real population.

### Test results (smoke evidence only — never governed)

**Runner named honestly: there is NO real `pytest` and NO `ruff` in this session.** PyPI
egress is blocked (verified: `ModuleNotFoundError` for `pytest`, `yaml`, `numpy`). Every
figure below comes from the session's **stdlib pytest stand-in**
(`pytest_standin/run_tests.py`) on **CPython 3.11.16**. **No `ruff check` and no
`ruff format` were run, and none is claimed** — the 99-column limit and clean
`ast.parse` were verified by a direct script instead (0 lines over 99, 0 trailing
whitespace, file parses).

| Module | Before (HEAD `715f392`) | After | Δ |
|---|---|---|---|
| `tests/test_locked_test_guard.py` | 44 passed, 0 failed, 0 skipped | **57 passed, 0 failed, 0 skipped** | +13 |
| `tests/test_phase_contract.py` | 36 passed, 0 failed, 0 skipped | **36 passed, 0 failed, 0 skipped** | 0 |
| `tests/test_phase_boundary.py` | 52 passed, 0 failed, 1 skipped | **52 passed, 0 failed, 1 skipped** | 0 |
| `tests/test_common_masks.py` | 60 passed, 0 failed, 1 skipped | **60 passed, 0 failed, 1 skipped** | 0 |

Full suite, all 26 test modules: **1157 passed, 0 failed, 39 skipped, 0 errors.** Of the
39 skips, **37 are this sandbox's missing third-party packages** (31 `yaml`, 5 `numpy`,
1 `test_clean_run` whose named first unmet precondition is pyyaml) and **2 are genuine
explicit-record project skips** (no hourly-target artifact yet; `dataset_version`
derived by `write_release`, covered by the D-29 tests). This is smoke evidence on a
dependency-incomplete clone, never governed evidence, and it does not reproduce the
bootstrapped environment in which this unit's earlier 449-passed figure was produced.

### Repository state, re-verified at summary-writing time

Per `project.md` `code-generation:c30`. The dispatch brief named HEAD `715f392`; **HEAD
moved during this session to `b0b7c1d` (2026-09-11 17:47 +0400)** — an owner commit,
outside this stage. Verified by `git show --name-only`: it touches **no** file under
`src/`, `tests/` or `scripts/` (only workspace record files, including this
`code-summary.md`, plus `evidence/test_run_access_log.jsonl`), so the code work above is
unaffected by it. **No commit, amend or push was made by this stage** — the governance
stop above still stands, and the disposition (fold into the next commit, or a follow-up)
is the owner's.

`evidence/test_run_access_log.jsonl` — this paragraph previously asserted **74 uncommitted
appended rows**. That figure was wrong when written (the reviewer derived **111** on
2026-09-11) and is wrong again now for a different reason, so it is corrected in the body
rather than carried, per `project.md` (`application-design:count-derivation` and
`code-generation:fr-2`).

**Re-derived 2026-09-13 at HEAD `1670ac8`: the file carries 4459 lines and ZERO uncommitted
rows** — `git diff HEAD -- evidence/test_run_access_log.jsonl` is empty. The appended rows
were committed by the owner in **`88f5c7e`**. The correct current statement is therefore
not a count of pending rows at all: there are none. The rows are written by
`tests/test_acquisition_window.py:70` and `tests/test_release_hashes.py:75` (sibling-owned,
pre-existing by design — the guard logs every real restricted read), **not** by Section 10,
whose registries are all under `tmp_path`.

**The safety-relevant half of the original claim held at every derivation and still holds:
zero rows contain `2022-12`.** That is the part that mattered; the numeral was the part
that kept going stale. Note the lesson the three successive values make concrete — an
uncommitted-row count is a claim about working-tree state, which changes under the artifact
without anyone editing it, so it must be re-derived at read time or not asserted at all.

### Residual, stated rather than implied closed

`test_containment_manifest_key_matches_the_producer` **parses** `src/evaluation/masks.py`
and does not **execute** `freeze_bundle`. It therefore pins the manifest's *key name*
across the unit boundary but not its runtime payload; a producer that emitted a
`mask_ids` key of the wrong type would still be caught at read time by the abort path
(`TypeError` is in `_containment_fields`' caught set — pinned by the `mask_ids is not
iterable` row), but not by this static check. Executing the sibling's producer would take
a runtime dependency on `evaluation-and-comparison`'s module from `governance-guards`'
own test, which is not this unit's call to make. Disclosed, not narrowed silently.

Nothing in this section discharges an acceptance row: **WS-18, TA-18, TA-25, TA-27,
TA-28 all remain `Pending`**; BLK-06 and BLK-07 remain open; no TBD sentinel was filled;
no locked December data was accessed.

## Floor-reset re-review — iteration 2 (2026-09-11, terminal)

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-11T14:02:34Z
**Iteration:** 2 of 2 (ADVERSARIAL, terminal — this verdict stands)

### Independent re-verification performed (by direct execution, not description)

**Fix 1 (was Major — sibling's Q2=B edit untested/undisclosed).**

- `git diff 8a6cb61 HEAD -- src/data/locked_test.py` and `git diff 8a6cb61 -- src/data/locked_test.py` (working tree) both empty: `src/data/locked_test.py` is byte-identical to its post-`8a6cb61` state, through HEAD (`b0b7c1d`) and in the current working tree. The abort logic was **not weakened** to ease testing.
- Read `src/data/locked_test.py:278-398` directly: `_containment_fields` raises `LockedTestError` on `(OSError, UnicodeDecodeError, ValueError, KeyError, TypeError)` **before** `open_restricted` calls `_append_and_flush` (line 383 precedes line 390) — confirms "consumes no access row" is a structural property, not merely asserted.
- Read `tests/test_locked_test_guard.py:1114-1451` (Section 10) in full: 13 test cases exactly as claimed — the 6-way parametrized broken-manifest control (`test_containment_present_but_unparseable_manifest_aborts_the_read`), the byte-identical-log ordering control, the must-not-fire population control, the containment/no-future-mask control, the absent-≠-broken boundary test, the backward-compatible-default regression, the `__post_init__`-untouched regression, and the producer-key-name cross-check (parses, never imports, `src/evaluation/masks.py`). All drive input through the real `open_restricted` entry point per the file's own text — confirmed by reading each case body, not just its docstring.
- Read `src/evaluation/masks.py:659-696` (`freeze_bundle`): writes a literal `"mask_ids"` key into the manifest dict — matches what the cross-boundary test asserts via AST parse.
- **Ran the tests myself** with the session's stdlib pytest stand-in (`pytest_standin/run_tests.py`, CPython 3.11.16 at the scratchpad's `uv-pythons/cpython-3.11.16-windows-x86_64-none/python.exe` — no real pytest/PyYAML, PyPI egress confirmed blocked): `test_locked_test_guard` → **57 passed, 0 failed, 0 skipped**; `test_phase_contract` → **36/0/0**; `test_phase_boundary` → **52/0/1** (named skip: no hourly-target artifact); `test_common_masks` → **60/0/1** (named skip: `yaml` unimportable). All four exactly match the code-summary's claimed figures.
- **Ran the mutation myself**, independently of the artifact's narration: temporarily replaced `_containment_fields`'s body with `return None, None`, re-ran `test_locked_test_guard`, then restored the file via `git checkout --` (confirmed clean afterward, `git diff --stat` empty). Result: **48 passed, 9 failed** — the exact 9 named (all 6 broken-manifest parametrizations, the byte-identical-log control, the valid-manifest-population control, the containment-property control); the other 4 (absent-manifest, default-keyword, post-init, producer-key) correctly still passed. This reproduces the claimed "9 of 13" precisely — not merely accepted on the artifact's word.
- `git diff HEAD -- tests/test_locked_test_guard.py`: confirms Section 9 (lines 1-1091, all pre-existing test functions) carries **zero code changes** — the only edit above the Section 10 append is a rewording of the module-docstring's ownership-limb paragraph (to mention Section 10) and one new import line; no test body in Section 9 was touched.
- Disclosure section verified at `code-summary.md:224-391` (`## Cross-unit edit disclosed (2026-09-11)`), exactly where claimed. `git diff HEAD` on this file shows the two ⚠️-pointer edits are **strictly additive superstrings** of the original sentences (original text preserved verbatim, pointer appended in-line) — nothing deleted or reworded. The prior `## Review` blocks (lines 61-222, including the 2026-09-05 iteration-1/2 blocks and the 2026-09-11 floor-reset block) are untouched by this diff.

**Fix 2 (was Minor — stale R-24 claim).**

- Read `tests/test_phase_contract.py:255-289` directly: `test_every_phase1_producing_script_calls_the_field_guard_before_its_first_write` takes its `pytest.skip` branch only when `_producing_script_violations(SCRIPTS_DIR)` returns an empty `checked`; my own run of this module shows **0 skipped**, confirming the real per-script check executed, not the skip branch.
- The printed derivation in Correction 2 (`enumerated n = 8`, `checked n = 8`, empty set-diff both directions, `skip branch taken? False`) is consistent with direct execution.
- Confirmed appended, not rewritten in place: `git diff HEAD` shows the original stale sentence in `code-summary.md:26` ("producing-script population empty...") preserved verbatim with only an inline ⚠️ pointer added; the correction's own text lives entirely in the new `## Cross-unit edit disclosed` section below it.

### New finding (Minor, emerges from this iteration's added disclosure text)

| # | Severity | Location | Finding | Evidence |
|---|---|---|---|---|
| 1 | Minor | `code-summary.md` § "Repository state, re-verified at summary-writing time" (~line 372) | The claim "`evidence/test_run_access_log.jsonl` carries **74 uncommitted appended rows**" is wrong; the actual count is **111** (`git diff HEAD -- evidence/test_run_access_log.jsonl` shows 111 added lines; `wc -l` on the file is 4311 against `git show HEAD:...` at 4200, i.e. 4311−4200=111). The safety-relevant part of the claim — zero rows contain `2022-12` — is independently confirmed true (`grep -c "2022-12"` on the diff's added lines returns 0), and all 111 added rows carry `run_id` of either `test_acquisition_window` (6) or `test_release_hashes` (105), consistent with the claim these are sibling-owned pre-existing loggers rather than anything from Section 10 (whose fixtures are all under `tmp_path`, confirmed by reading Section 10's fixture code). The miscount does not touch either of the two closed findings and does not indicate any governed-evidence or leakage problem, but it is exactly the kind of uncounted-then-asserted numeral `project.md`'s `application-design:count-derivation` correction exists to catch, and it should be corrected at the next touch of this artifact rather than carried forward silently. |

### Also verified

- No TBD-sentinel fill: the one `TBD` hit in `tests/test_locked_test_guard.py:1044` is a negative-control literal value inside a test parametrization (`test_limb1_unsigned_or_tbd_gate_record_never_verifies`), not a filled sentinel. No credential/secret pattern (`api_key`/`password`/`secret`, case-insensitive) in any of the three touched/added `src/` modules.
- No locked-December access: 0 occurrences of `2022-12` in the newly appended access-log rows; Section 10's fixtures are entirely synthetic under `tmp_path`, confirmed by direct read.
- No guard weakened: `src/data/locked_test.py` byte-identical to its `8a6cb61` post-edit state, confirmed by `git diff` both against history and the working tree.
- Full-suite claim (1157/0/39/0) was not re-run in full (would exceed this pass's scope/time); the four named modules were re-run in full and match exactly, and the described skip composition (37 missing-package + 2 genuine explicit-record skips) is internally consistent with the per-module skip reasons observed directly in the four modules actually re-run.
- Read-scope respected: only this unit's record dir, `configs/`, `evidence/`, `governance/`, and workspace code/tests were read; `src/evaluation/masks.py` was opened only as the disclosed cross-boundary integration point, and only to check the one function (`freeze_bundle`) the disclosure names.

### Verdict rationale

Both carried-forward findings are independently confirmed closed by direct execution, not accepted on the report's word: the Major's missing test coverage now exists, runs through the real entry point, is proven non-vacuous by an independently-reproduced mutation kill, and is honestly disclosed as an additive appendix without touching the frozen prior Review history; the Minor's stale claim is corrected with a re-executed, matching derivation. The one new finding (Minor, a miscounted row count) does not touch either closed item, carries no safety implication (the count that matters — zero December rows — is independently confirmed correct), and is well within the stated verdict rule (READY if zero Critical, ≤2 Major, any Minor): 0 Critical, 0 Major, 1 Minor.

**Verdict:** READY

## Review — 2026-09-13 (code-generation, TERMINAL adversarial re-review, iteration 2)

**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-13T09:34:37Z
**Iteration:** 2 of 2 (TERMINAL — this verdict stands; no further pass follows)

### Scope note

Read scope bound to unit `governance-guards` plus the one named carve-out,
`construction/target-standardization/functional-design/domain-entities.md`. No other
sibling unit directory was opened. Baseline for every "unchanged"/"zero diff" claim in
this pass is commit `1670ac8` (`project.md` `code-generation:gf-1`).

### Independent re-derivation of both iteration-1 findings (by direct execution, not description)

**Finding 1 (was Critical — false commit-durability claim).** Re-ran the exact commands
myself against the live tree: `git rev-parse HEAD` → `1670ac8800f7cf3610b7db20bf89cdaf00c2c3bb`.
`git status --porcelain` shows `tests/test_phase_boundary.py` and `tests/test_phase_contract.py`
as ` M`. `git diff --cached --stat -- tests/test_phase_boundary.py tests/test_phase_contract.py`
is empty (nothing staged). `git diff HEAD --numstat` for the two files returns `125\t5` and
`12\t3`. The corrected header (line 6) now states this exactly — it distinguishes the
committed Steps 1–10 code from the uncommitted repair, names the `reset --hard`/`clean`/
fresh-checkout risk, and routes the commit act to the owner per `code-generation:c30` — and,
checked independently, does **not** overshoot into implying the unit's Steps 1–10 code is
uncommitted: `git diff HEAD --numstat` for `src/data/phase_contract.py`, `src/data/reuse_registry.py`,
`tests/test_reuse_registry.py`, `src/data/locked_test.py`, and `tests/test_locked_test_guard.py`
is empty for all five, confirming those files are genuinely committed as the header claims.
**RESOLVED**, independently re-verified, correctly calibrated in both directions.

**Finding 2 (was Minor — wrong diff stats).** Re-ran `git diff HEAD --numstat` myself: the
artifact's corrected figures (line 42: "+125/−5"; line 48: "+12/−3") match exactly what I
derived. Swept the whole file for the superseded numerals in every form: `+130/` and `+15/`
appear only twice each — once in the corrected sentence's own "an earlier version... carried"
clause (lines 42, 48) and once inside the frozen iteration-1 finding-table quote (line 317,
correctly preserved as a historical record of what was wrong) — no other site asserts the
stale figures as current fact. **RESOLVED**, sweep is clean.

### Independent substance re-attack on Repair Step 11 (not inherited from the prior pass)

- **D-17 Field-column count, re-counted directly from `evidence/DECISIONS.md:788-803`**: the
  row table's individual field names (some rows carry 2–3 names) total exactly **16** —
  `interval_start_utc`, `station_id`, `cell_gdlat`, `cell_glon`, `cell_lat_bounds`,
  `cell_lon_bounds`, `vtec_tecu`, `valid_observation_count`, `within_hour_spread_tecu`,
  `largest_internal_gap_s`, `provider_dtec_summary`, `aggregation_config_id`, `target_valid`,
  `phase_id`, `source_id`, `target_definition_id`. `processor_qc_flags` is discussed at
  lines 815–817, outside and after the row table — confirms the artifact's "outside the row
  table" claim.
- **`D17_TARGET_FIELDS` (`tests/test_phase_boundary.py:106-123`) and `D17_ALLOWED_FIELDS`
  (`tests/test_phase_contract.py:73-90`)**: both hand-counted directly, each exactly **16**
  entries, identical sets to each other and to the D-17 table and to the producer's
  `D17_FIELDS` (`src/data/prepared.py:195-212`, also independently counted at 16).
  `processor_qc_flags` is absent from both.
- **Producer header** (`src/data/prepared.py:1324`): `_TARGET_CSV_HEADER: Final[tuple[str, ...]]
  = (*D17_FIELDS, LINEAGE_CAVEAT_FIELD)`, confirmed verbatim by direct read; row guard at
  `:791` — `extra = sorted(names - set(D17_FIELDS) - {LINEAGE_CAVEAT_FIELD})` — confirmed
  verbatim.
- **`extra`/`missing` in the repaired test** (`tests/test_phase_boundary.py:349-377`), read in
  full: `extra = sorted(header - D17_TARGET_FIELDS - {DECLARED_CAVEAT_FIELD})` accepts exactly
  the producer's real 16+caveat header and refuses anything else; `missing = sorted(D17_TARGET_FIELDS
  - header)` still demands the full sixteen, untouched by this repair — confirmed by reading
  the function body directly, not by trusting the artifact's characterization.
- **AST drift guard `_module_level_literal`** (`tests/test_phase_boundary.py:157-189`), read
  in full: fails closed on all four claimed drift modes — unparseable file (`SyntaxError` →
  `pytest.fail`), constant missing/renamed (loop falls through to a final `pytest.fail`),
  value present but not a literal (`ast.literal_eval`'s `ValueError/TypeError/SyntaxError` →
  `pytest.fail`), and the calling test `test_d17_target_fields_match_the_producer_contract`
  (`:298-346`) additionally checks type, no-duplicates, set-equality both directions, exact
  count == 16, and the caveat literal's cross-copy agreement plus its exclusion from the
  target-field set — none of these six checks was weakened.
- **Authority argument**: `git show --stat b844a4d` independently confirms that single commit
  touched both `evidence/DECISIONS.md` (1370-line rewrite) and `tests/test_phase_boundary.py`
  ("created with both TE 7.0 limbs") — corroborating the same-commit-transcription-slip claim
  rather than a competing decision. Cross-checked against the one permitted carve-out,
  `construction/target-standardization/functional-design/domain-entities.md:106,461`, which
  independently states "Sixteen fields, counted from D-17's enumeration" — agrees.
- **`src/data/prepared.py` shows ZERO diff against `1670ac8`**: `git diff HEAD --numstat --
  src/data/prepared.py` returns nothing. No cross-unit edit was made by this repair.

### Attribution check

`git status --porcelain` at the top of this pass also shows `src/evaluation/guards.py` and
`tests/test_determinism.py` modified in the same working tree, plus several sibling
`code-summary.md` files. The artifact (line 328) correctly attributes these as "other units'
concurrent in-flight work," not touched or introduced by Repair Step 11, and does not credit
this unit for them. Confirmed: no diff attributable to this repair falls outside
`tests/test_phase_boundary.py`, `tests/test_phase_contract.py`, `code-generation-plan.md`, and
`code-summary.md` itself.

### Execution-honesty check

No Python interpreter is available in this review session (confirmed directly: `python3`
resolves to a Windows Store execution-alias stub, matching the artifact's own stated
constraint). The claimed "89 passed / 1 skipped" figure could not be independently re-run
this pass either, consistent with the prior iteration-1 pass's identical limitation — recorded
here as a coverage limit, not a finding. Checked the whole file for any sentence implying real
`pytest` ran: every occurrence of the 89/1 figure and the surrounding "smoke only, never
governed" framing (lines 71–79) is consistently qualified with the stdlib-standin/PyPI-blocked
caveat; no bare, unqualified claim of a real pytest run was found.

### Acceptance-row and forbidden-content check

`WS-18`, `TA-18`, `TA-25`, `TA-27`, `TA-28` are stated `Pending` consistently everywhere in the
artifact (lines 126, 329, 522) — no row is claimed discharged by this repair. Grepped both
touched test files directly for `TBD`, `api_key`, `password`, `secret`, `2022-12`
(case-insensitive): zero matches in either file. No scientific constant introduced; no
restricted-root or December content touched.

### Verdict rationale

Both iteration-1 findings are independently re-derived as resolved, not accepted on the
artifact's word: the commit-durability claim is now accurate and correctly calibrated (neither
overstating nor understating what is committed), and the diff-stat correction matches a
freshly re-run `git diff HEAD --numstat` exactly, with the sweep confirming no other site
carries the stale figures. Independent re-derivation of the D-17 field-contract substance —
counts, producer header, `extra`/`missing` logic, and the AST drift guard's four fail-closed
branches — matches the artifact's claims at every checked site, corroborated by both the
same-commit authority trace and the permitted cross-unit carve-out. No new defect surfaced.
Zero Critical, zero Major, zero Minor.

**Verdict:** READY

## Post-receipt amendment — 2026-09-19 (D-48 structural December detection and class 5; `CR-2026-09-19-SCI-DECISIONS`, item 6 of the 2026-09-19 owner authorization)

*Appended under `project.md` `code-generation:gf-3`. Nothing above is rewritten; the
READY receipt stands as history. Authority: `evidence/DECISIONS.md` D-48 (no supervisor
approval required — R-26's class list amended by the owner under the D-30 precedent; no
target value involved).*

| Module | What changed (measured, `git diff --numstat` vs `18843aa`) |
|---|---|
| `src/data/locked_test.py` | +447 / −31. `DECEMBER_DRIVER_EXCLUSION_CLASSES` widened from four to five (paths now tuples, allowing class 5's three patterns). New: structural December detection per format (`_json_december` — string literals, `{y, m}` records at any depth, month-number-keyed per-month mappings; `_detect_december` dispatches by suffix/filename to JSON, WDC-line, Hpo-line, isprint-endpoint, CSV-`ut1_unix`-epoch or literal detection), content validators per class (`_class_content_ok`, `_gfz_report_ok` — a schema-validated check admitting `y`/`coverage` tokens ONLY in their structurally valid positions), provenance check for class 5 (`_gfz_provenance` — a sibling `retrieval_record.json` SHA-256 or `run_id` match), `DecemberCustodyEntry`/`december_custody_inventory` (every file outside the restricted root inventoried with its detection method and disposition — `flagged`/`excluded`/`no_december_content`/`outside_automated_inspection`), `_read_text` (UTF-8 with a Latin-1 fallback for non-JSON text formats only — JSON stays strict). `december_driver_exclusion_class` now needs BOTH the path AND the validated content (and, for class 5, provenance); `assert_no_december_outside_restricted` is reimplemented as a filter over `december_custody_inventory`, same public contract (empty sequence = pass), same recursive/unparseable-is-failure behaviour. |
| `tests/test_locked_test_guard.py` | +273 / −10. `test_r26_driver_exclusions_are_exactly_four_and_content_gated` renamed/extended to `..._exactly_five_and_content_gated` (five-class enumeration, full real-tree inventory assertion — 9 excluded files with their exact class, 5 files outside automated inspection, 0 flagged); new `test_december_detection_is_structural_not_lexical` (eight synthetic shapes: integer `{y,m}` records, month-number keys, compact literals, nested year/month strings, WDC/Hpo line layouts, isprint endpoint epochs, `ut1_unix` CSV epochs, Markdown outside-scope reporting — all flagged where no class covers them, proving the widened scan is no longer defeated by dodging a quoted literal); new `test_class_5_excludes_only_validated_driver_captures_with_provenance` (six negative controls: target key inside the report, `y`/`coverage` outside their valid structural position, an extra column in a raw line, bytes not matching the recorded SHA-256, no retrieval record at all, a prediction file dropped into the directory — every one flagged, proving the directory name alone never qualifies content). 60 test functions total. |

Runs (governed pin, conda `tec-thesis-311`, CPython 3.11.16): `tests/test_locked_test_guard.py`
(60 tests) green; the real evidence tree scan (`december_custody_inventory`, 369 files,
~0.9 s) reproduced 0 flagged, 9 excluded, 5 outside automated inspection. `ruff
check`/`ruff format` clean.

**What this amendment does NOT do.** It does not relocate or reserialise any evidence
file; it does not widen custody beyond the five classes' exact content-and-provenance
conditions; it does not certify holdout independence "unaffected" (exposure is recorded,
never asserted away); it does not pass G-04.

---

## Custody/environment remediation — 2026-09-20, `GOV-2026-09-20-CG-01` (worker D)

Appended under the owner-authorised remediation recorded in
`governance/CHANGE_RECORD_2026-09-20_GOV-CG-01_dispositions.md`, disclosing changes to
modules **this unit owns or co-owns** so a reader is not left describing a pre-edit state
(`project.md` `code-generation:gf-3`).

⚠ **NOTHING BELOW WAS EXECUTED.** No usable Python interpreter exists on this clone
(`python.exe` is a zero-byte Windows Store alias stub; PyPI is unreachable). Every statement
about behaviour is **static**, read from source. Nothing here is "verified passing".

### Rec 1 — the December access log is separated; the governed log is closed, not rewritten

Owner ruling: **option 2** — separate the test-mode access log from the evidence access log;
archive the current file as superseded; **never rewrite a row**. Both halves were honoured.

| Change | Where |
|---|---|
| `AccessRecord.__post_init__` now refuses a `retrieved_at_utc` that does not parse as ISO-8601, via `_assert_parseable_retrieved_at`. The check runs **last**, so an existing caller violating emptiness/purpose/`locked_test_accessed` still fails for its own reason. | `src/data/locked_test.py` (+46) |
| Both suite producers write real call-time timestamps and append to `artifacts/exec_evidence/test_access_log.jsonl`, a **gitignored test-mode sidecar**, instead of the governed log. | `tests/test_release_hashes.py`, `tests/test_acquisition_window.py` |
| The one-file ignore entry, scoped so `artifacts/exec_evidence/`'s committed run evidence stays tracked. | `.gitignore` (+11) |
| R-19 reconciliation run against the **real** registry/log pair, with the two historical test `run_id`s declared as `known_orphans`, plus a negative control that plants an unregistered access into a `tmp_path` **copy** and asserts the raise. | `tests/test_locked_test_guard.py` (+244/−12) |

`evidence/test_run_access_log.jsonl` is **unmodified** — no row rewritten, truncated or
deleted — and `evidence/test_run_access_log.SUPERSEDED_2026-09-20.md` is its notice.
`artifacts/registry/experiment_registry.jsonl` is likewise unmodified; no registry row was
back-filled, and `reconcile_access_records` must keep forbidding it.

**Open, and encoded rather than decided:** whether the two suite `run_id`s are permanently
registered as known orphans, or whether the closed log leaves reconciliation scope entirely.
The test encodes the first reading; the ruling is owed.

### Rec 32 — the restricted-read chokepoint, and its drift controls

`R-28`'s `RESTRICTED_LITERAL_EXEMPT_MODULES` covers **holding** the restricted-root literal
and has never covered obtaining the **content** — its own comment says so. Two modules were
outside that exemption:

- `tests/test_release_hashes.py::_sha256` opened December bytes directly. Now routed through
  `_read_guarded`, guarded at the single point the bytes are opened rather than per call site.
- `tests/test_phase_boundary.py::_csv_header` opened every collected December artifact
  directly; the module had **zero** `open_restricted` references. Now routed, with a lazy
  import that **fails closed** — a restricted read is refused outright if the chokepoint is
  unimportable, rather than performed unguarded.

Each module gained an **AST drift control** that walks its own source for content reads and
refuses any receiver that is not guarded or enumerated, each with a negative control pushing
three mutants through the real entry point and must-not-fire limbs. A scanner that never
fires proves nothing.

### Rec 58 — the G-P3C hash-diff limb's location, cross-referenced both ways

`team.md` § Deployment names `tests/test_phase_boundary.py` as the hash-diff test's home; it
is not there. `diff_protected_hashes` / `assert_protected_hashes_unchanged` are exercised in
`tests/test_phase_contract.py`. Both required tests exist and **only the location differs**.
Cross-references were added in **both** directions — `test_phase_boundary.py`'s docstring
points to `test_phase_contract.py` (+13 to the latter) — so a G-P3C reviewer arriving from
either side finds the limb instead of recording a false gap.

### Rec 50 — the phase-boundary detector now has negative controls

Two reviewers independently **refuted** the vacuity hypothesis: the scan reads the live import
graph and skips with a stated reason rather than passing when `src/` is absent. The real gap
was that nothing proved it would **catch** an injected violation (`grep -c 'pytest.raises'` =
0). The two scan bodies are now callables taking a root — the shape `run_containment_scan`
already uses — and synthetic `tmp_path` trees exercise **the same code the real assertions
run**: a direct `import src.gnss.rinex` in a synthetic `src/features/` module and a transitive
chain, each with a must-not-fire limb on the clean tree first. No real module is edited by any
control.

### Recs 30 / 35 — commit-time December access removed; the hook is still OFF

`.githooks/pre-commit` (+68/−5) previously ran a single critical set unconditionally, three of
whose modules read December restricted content. The set is now split by a stated criterion —
**reads bytes under `evidence/locked_test_restricted/`** — with the per-module derivation
printed in the hook itself. Deselected to the gate/freeze suite: `test_release_hashes.py`,
`test_acquisition_window.py`, and **`test_phase_boundary.py`**, the last being a reader only
*since* Rec 32's remediation the same day — the finding named two modules because two was the
truth when it was written, and the hook applies the criterion rather than the enumeration.
Retained at commit time: `test_locked_test_guard.py` and
`test_merge_script_restricted_reads.py`, which resolve a path through `open_restricted` to a
`tmp_path` registry and read **no** bytes; deselecting them would delete the guard's own
controls.

**`git config core.hooksPath .githooks` was NOT run** and no state-changing git command was
issued. Enabling the hook is a **Student act** (dispositions §5 item 4), explicitly sequenced
*after* this deselection — which has now landed, so the bar is clear.

### Rec 25 follow-up — `_release_manifest` brought onto the new sub-schema (2026-09-20, same worker, second pass)

The data-provenance worker's Rec 25 remediation added four sub-schema guards to
`src/data/release.py` (`SOURCE_FILE_FIELDS`, `PROCESSING_PHASE1_FIELDS`, `ROW_COUNT_AXES`,
`EXCLUSION_ENTRY_FIELDS`; composed in `assert_manifest_content_contract`, wired into
`write_release`), and reported — correctly, per `code-generation:c32`, without editing a file
outside its scope — that `tests/test_release_hashes.py::_release_manifest` would now be
refused. Verified statically and repaired here, in the module's owning record:

- **`source_files`**: was one entry with no `location_date` and a `retrieved_at_utc` key
  TE §13.3 does not name. Now carries all six `SOURCE_FILE_FIELDS` (`provider`, `citation`,
  `location_date`, `filename`, `retrieval_date`, `sha256`), with a full provider filename
  including its version suffix (`syn220301g.003.hdf5`) — the field Rec 8's version mixing is
  recordable in — under a **synthetic** stem.
- **`processing`**: was four keys, one of them `cell_rule` (not the mandated
  `station_coordinate_to_cell_rule`). Now all seven `PROCESSING_PHASE1_FIELDS`, every value
  SYNTHETIC. The old `"floor(lat), floor(lon), half-open"` read like the governed rule —
  a §18.2 forbidden-choice item — and was deliberately not carried forward, matching
  `tests/test_release_contract.py::_manifest_for`'s convention.
- **`row_counts`**: was station-keyed (`{"ARUC": 8760, …}`), one axis of four. Now all four
  `ROW_COUNT_AXES` (`by_station`, `by_month`, `by_split`, `by_qc_stage`), each a non-empty
  label→integer mapping with synthetic station labels.
- **`exclusions_qc_summary`** already satisfied the reason→count mapping form; unchanged.

Blast radius, derived: all seven `write_release` call sites in the module consume the one
helper (one with a `body=` override, schema-neutral); **no test assertion referenced the old
field values**; the AST drift control is unaffected (the release section's three content
reads all have receiver root `target`, already in `TMP_PATH_ROOTS`). Nothing else in the
module changed — the ACCESS_LOG sidecar wiring and the chokepoint controls stand as
disclosed above.

⚠ Static only, as before: **no test was executed** — no interpreter exists on this clone —
so "would now pass the new guards" is a source-level claim, not a run result.

## Post-receipt amendment — 2026-09-24 (chokepoint scanner self-reference fix, unfreezing `PENDING_FOLLOWUPS.md` item 1)

*Appended under `project.md` `code-generation:gf-3`, following the same pattern as this
unit's own 2026-09-19 and 2026-09-20 amendments above. Nothing above is rewritten; the
READY receipt stands as history. Authority: Student ruling.*

**What changed, measured (`git diff --numstat` vs the receipted state).** One file this
unit owns: `tests/test_phase_boundary.py`. `+9 / -0`: added
`"test_no_restricted_read_in_this_module_bypasses_the_chokepoint"` to
`SOURCE_TREE_ONLY_READERS`, exempting that one test function's body (which holds only its
own `Path(__file__).read_text(...)` self-scan call) with a stated reason, per this
scanner's own documented remediation path.

**Why.** Same root cause and same finding as the sibling fix in `tests/test_release_hashes.py`
(`foundation`'s own post-receipt amendment, same date, this session): the chokepoint
scanner flagged its own positive-limb test reading its own module's source (`__file__`,
under `tests/`, never under `evidence/locked_test_restricted/`) — a false positive, not a
restricted-root read. `test_phase_boundary.py`'s scanner keys its exemption by enclosing
function name (`SOURCE_TREE_ONLY_READERS`), not by receiver name
(`test_release_hashes.py`'s `UNRESTRICTED_READ_RECEIVERS`), so the fix takes the shape that
module's own mechanism specifies rather than mirroring the sibling's literally. First
identified in `GOV-2026-09-20-CG-01` §7, tracked in `governance/PENDING_FOLLOWUPS.md` item
1 pending this unfreeze — which also unblocked the D-28 option (b) bounded-read design
(`governance/CHANGE_RECORD_2026-09-24_d28_option_a_bounded_read.md`), still separately
gated and not built in this pass.

**Verified, not merely reasoned — first EXECUTED verification on this unit's own chokepoint
tests in this thread.** `test_the_exempt_readers_are_named_and_still_exist` (this module's
own pinning test) confirms the new exemption name resolves to a real, callable function in
the module. Full module run: 294/294 passed (`tests/test_phase_boundary.py` +
`tests/test_release_hashes.py` together). Full §18.3 critical test set re-run after this
change: **766/766 passed**, 0 failures — resolves both prior static-only caveats on this
unit's earlier amendments ("no test was executed... a source-level claim, not a run
result") for THIS specific fix, under the governed environment
(`tec-thesis-311`, CPython 3.11.16) now available on this clone. Earlier amendments'
own static-only caveats stand unchanged for the work they cover.

**Also resolved by measurement, not by this change**: `test_locked_test_guard.py`'s
previously-reported orphan-reconciliation failure (§7's third named issue) no longer
reproduces — confirmed passing in the same 766-test run. Not attributed to this amendment;
recorded as the observed current state.

**What this amendment does NOT do.** It does not touch `scan_unguarded_reads`'s logic in
either file, does not widen any other exemption, and does not touch the `ACCESS_LOG`
sidecar wiring, the chokepoint controls, or any other module this unit owns — scope is
exactly the one exemption-set entry named above.

## Post-receipt amendment — 2026-09-24, second amendment same day (D-28 option (b) bounded 1-December read, mechanism only)

*Appended under `project.md` `code-generation:gf-3`, same pattern as the amendment
immediately above. Nothing above is rewritten; the READY receipt stands as history.
Authority: Student ruling, `RULING_REQUEST_2026-09-21_GOV-CG-01_OPEN_ITEMS.md` §2 Option A.*

**What changed, measured (`git diff --numstat` vs the receipted state).** Two files this
unit owns: `src/data/locked_test.py` (`+167 / -2`) and `tests/test_locked_test_guard.py`
(`+224 / -0`); plus `configs/experiment.yaml` (`+11 / -0`), a shared governed config file,
not owned by any single unit.

**What was added to `src/data/locked_test.py`**: `PURPOSES` gains `"persistence_history"`;
new `PERSISTENCE_HISTORY_CALLERS = frozenset({"M-01", "M-02"})` and
`PERSISTENCE_HISTORY_DAY = "2022-12-01"` constants; new function
`read_persistence_history_lookup(snapshot, *, model_id, g05_signature, loader, registry, now=None)`
— a bounded, logged, post-G-05, kill-switched lookup of 2022-12-01 target history for the
two unfitted persistence baselines only. Imports `verify_g05_signature` from
`src.data.splits` and `records_of` from `src.features._frames` (both verified acyclic by
grep before adding — neither imports this module). Full design and all 5 enforced
conditions: `governance/CHANGE_RECORD_2026-09-24_d28_option_a_mechanism_built.md`.

**What was added to `configs/experiment.yaml`**: a `persistence_history_lookup:
{authorized: false, decision: "TBD — freeze gate"}` block — the mechanism's own kill
switch, shipped OFF. Nothing else in that file was touched.

**Why.** D-28's original disclosed 30-day scored set (D-28/D-59) silently shrinks to 29 days
because the two mandatory persistence-baseline difficulty controls (M-01, M-02) cannot
forecast into 2 December without reading 1 December history. `GOV-2026-09-20-CG-01`
Recommendation 15 raised this; the owner's first ruling (amend D-28 to 29 days) was reverted
same-day after conflicting with D-59 (see `CHANGE_RECORD_2026-09-24_d28_29day_amendment.md`);
the final ruling, option (b), is this mechanism — recovering the true 30-day set via a
narrowly-scoped lookup rather than amending any frozen decision.

**Verified, not merely reasoned.** 6 new tests, one per enforced condition plus a real-config
check, all passing (`tests/test_locked_test_guard.py::test_ph_*`). Full module:
**72/72 passed** (66 existing + 6 new). Full §18.3 critical test set re-run after this
change: **772/772 passed**, 0 failures (766 from the earlier same-day amendment + 6 new —
count reconciles exactly, no regression). `ruff check` on both modified files: clean. All
under the governed `tec-thesis-311` (Python 3.11.16) environment.

**What this amendment does NOT do.** It does not wire the mechanism into the live
prediction path — `scripts/06_train_and_predict.py` and `src/models/persistence.py`
(owned by `models-and-baselines`/`fixtures-and-reproducibility`, not this unit) are
untouched, confirmed by `git diff --stat` showing zero changes to either. This is a
deliberate stop, not an oversight: wiring is a cross-cutting, multi-unit change to the live
DEC-partition prediction data flow, a materially larger class of change than this or any
prior post-receipt amendment in this unit's history, and is flagged as a separate,
not-yet-authorized follow-up in the same change record. The mechanism itself is inert
today regardless — `authorized: false` in `configs/experiment.yaml` means every call
refuses, proven by `test_ph_the_real_config_ships_inert_today`.
