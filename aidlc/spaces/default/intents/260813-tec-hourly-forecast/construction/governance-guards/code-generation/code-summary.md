# Code Summary — `governance-guards`

**Unit** `governance-guards` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Plan**: `code-generation-plan.md` — all 11 steps executed, checkboxes marked. No `git commit` (governance stop).

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

`evidence/test_run_access_log.jsonl` carries **74 uncommitted appended rows** from the
full-suite run. These are written by `tests/test_acquisition_window.py:70` and
`tests/test_release_hashes.py:75` (sibling-owned, pre-existing by design — the guard
logs every real restricted read), **not** by Section 10, whose registries are all under
`tmp_path`. Checked: **zero of the new rows contain `2022-12`**.

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
