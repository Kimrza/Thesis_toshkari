# Build and Test — Questions

**Stage:** build-and-test (3.6) · **Lead:** aidlc-quality-agent · **Support:** aidlc-devsecops-agent
**Test Strategy:** Comprehensive (`aidlc-state.md`)
**Date:** 2026-09-13

## Environment facts, derived before asking (not assumed)

| Fact | Derivation |
|---|---|
| **Real CPython 3.11.16 is now available** — the exact governed pin (TE §8.1, TC-03d) | `uv python install 3.11` → "Installed Python 3.11.16"; `python -V` on the created venv returns `Python 3.11.16`. The astral index is reachable. **This is new**: every prior session had only Windows Store alias stubs. |
| **PyPI is NOT reachable** | `uv pip install -r requirements.txt` → `Failed to fetch https://pypi.org/simple/pytest/ … operation timed out`, after 3 retries in 47.6 s. |
| **`pytest` is the single blocking dependency** | AST scan of all 26 `tests/test_*.py`: 25 import only `pytest` at module level; `test_regimes_and_reporting.py` imports `pytest` and `yaml`. `numpy`, `pandas`, `sklearn`, `tensorflow` are **lazily imported inside functions by design**, so they do not block collection. |
| **No pytest exists anywhere reachable** | Searched every temp scratchpad, the uv python root and `~/.local`: no `pytest`, `_pytest`, `pluggy`, `iniconfig` or wheel. Prior sessions wrote per-module stdlib stand-ins instead. |
| **26 test modules on disk**; `tests/fixtures/` holds `plumbing_7day/` and `scientific_1month/` | `ls tests/*.py` = 26; `ls tests/fixtures/` |

## Question 1
Given a real governed-pin interpreter but no `pytest`, what execution evidence should this stage attempt?

A) Build a stdlib `pytest` stand-in and run the full suite on real CPython 3.11.16
   > **Impact**: Produces the first execution evidence in this project's history on the *exact governed interpreter* rather than a stub or a 3.14 bootstrap. Still **smoke evidence, never governed** — a hand-rolled stand-in is not pytest, and TC-03g requires the critical set to run *inside the Kaggle session* before any run counts. The stand-in must implement `tmp_path`, `monkeypatch`, `raises`, `parametrize`, `importorskip` and `skip` faithfully or it will silently under-report; that risk is real and must be stated wherever a number from it is quoted.

B) Document only — generate the instruction files, attempt no execution
   > **Impact**: Cheapest and carries zero risk of a misleading figure. But it leaves `build-test-results.md` with no results at all, and forfeits the one genuinely new capability this clone has gained. The stage would close having never run the thing it exists to run.

C) Attempt to vendor `pytest` from an alternative reachable source before deciding
   > **Impact**: If a mirror is reachable, the suite runs under *real* pytest on the governed pin — by far the strongest evidence available off-Kaggle. If not, the time is spent and we fall back to (A) or (B) anyway. Vendoring an unpinned pytest would itself violate the `requirements.txt` pin (`pytest==8.2.2`) unless that exact version is obtained.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — with the stand-in's limitations stated wherever its numbers appear. The project has been quoting stand-in figures since 2026-09-06 (`1160 passed` at the last count) with no interpreter at all behind them; running the same class of harness on the *governed 3.11.16 pin* strictly improves the evidence while changing none of its governance status. Option C is worth the first five minutes inside Option A, not a separate decision — if `pytest==8.2.2` turns out to be fetchable, take it.

[Answer]: C

## Question 2
TE §18.3's preflight gate requires "zero unresolved P0 fields and no failing critical test", and asserts no required field in the four governed configs is `TBD`. Those sentinels are still present by design. How should this stage treat the preflight refusal?

A) The refusal IS the deliverable — document it as correct gate behaviour and record the refusing fields
   > **Impact**: Matches the precedent this project already set at `target-standardization`, where Q2=A made refuse-to-RUN the deliverable, and honours TE §18.3's binding instruction that an agent "must stop and report rather than choose a default". Produces an `aws_ai_dlc_preflight_report`-shaped artifact showing exactly which P0 fields remain open. Nothing is discharged.

B) Treat the refusal as a build failure to diagnose and fix under Step 10's two-attempt rule
   > **Impact**: Would drive the stage toward filling `TBD — freeze gate` values to make the gate pass — which `project.md` forbids absolutely ("NEVER let a coding agent fill a value marked TBD — freeze gate by convenience") and which requires student-and-supervisor approval. **This option is listed for completeness and should not be chosen.**

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A. Option B is not merely worse, it is barred: the refusal is the mechanism §18.3 exists to provide, and Step 10's "diagnose and fix" instruction cannot reach a value only the student and supervisor may freeze.

[Answer]: A

## Question 3
`external-products` and `fixtures-and-reproducibility` closed NOT-READY on the confirmed `04` deadlock: the walking-skeleton ladder cannot complete, so WS-20 and TA-17 are unreachable. How should this stage handle the fixture ladder?

A) Attempt the ladder anyway and capture the actual refusal as evidence
   > **Impact**: Turns the finding from a traced argument into an observed exit code and message — materially stronger for the owner's eventual remedy decision, and cheap. Risk: none to governance, since a refusal produces no data artifact. Requires the interpreter, so it depends on Question 1 not being answered B.

B) Document the ladder as blocked, attempt nothing
   > **Impact**: Avoids spending time on a run known to fail. But it leaves the Critical resting on static tracing alone, when an actual observed refusal is available for the cost of one command.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — observe the refusal and record its exact text. Three separate agents have now traced this chain statically; an executed refusal is the one form of evidence nobody has produced, and it either confirms the finding outright or reveals the trace was wrong, which matters equally.

[Answer]: A

## Question 4
TC-03g (`binding: hard`) requires the critical test set and both fixtures to run **inside the Kaggle session** before any governed run executed there, because a Kaggle session carries no git working tree. Should this stage produce Kaggle-session run instructions?

A) Yes — a dedicated in-Kaggle execution section covering the critical set and both fixtures
   > **Impact**: Closes the gap between what can be run here and what TC-03g actually requires for a governed run, and gives the student a runnable procedure rather than a rule to re-derive. Costs one more instruction file. The instructions cannot be executed or verified from this clone, and must say so.

B) No — treat Kaggle execution as out of scope for this stage
   > **Impact**: Keeps the stage's outputs to what can be checked here. But TA-03 and TA-26 both depend on in-Kaggle evidence, and leaving the procedure unwritten means the requirement is carried as prose in `project.md` with nothing operational behind it.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A. `project.md` § Way of Working requires the inputs a gating condition depends on to be specified in the same stage that records the condition; TA-03/TA-26 are gating conditions this stage is the natural home for.

[Answer]: A

## Consolidated Summary Confirmation

**Answers recorded:** Q1 = C (vendor first, then fall back — the vendoring was attempted, refused on integrity grounds, and fell back to a stdlib stand-in on the real pin per your follow-up ruling); Q2 = A (the preflight refusal is the deliverable); Q3 = A (attempt the ladder and capture the refusal); Q4 = A (produce Kaggle-session instructions).

### What was executed, and what it showed

| | |
|---|---|
| Interpreter | **Real CPython 3.11.16** — the governed pin (TE §8.1, TC-03d), installed via `uv` from the reachable astral index |
| Harness | Stdlib stand-in written this session. **NOT pytest.** Unimplemented and declared: assertion rewriting, conftest, plugins, non-function fixture scopes, xfail, `-k`/`-m` |
| Suite result | **1169 passed · 39 skipped · 0 failed · 0 errors**, 26 modules, exit 0 |
| Fidelity evidence | Reproduces 20+ of the project's own per-module counts derived by other harnesses in other sessions (`test_release_hashes` 149, `test_locked_test_guard` 57, `test_regimes_and_reporting` 88, `test_bootstrap` 31/6, `test_clean_run` 61/3, `test_acquisition_window` 7 fn → 29 cases, …) |
| Repairs confirmed | The R-01 census runs and prints its derivation (12 units / 48 artifacts / 34 subclasses / 15 + 19); the D-17 drift guard passes. First execution-backed confirmation that `code-generation`'s repairs work |

### Three findings this stage produced

1. **CRITICAL — on Windows, every stage script and the orchestrator exit 0 regardless of outcome.** `run_walking_skeleton.py` prints `preflight refusal: …` and exits **0**; same for both fixtures and for `scripts/00` and `scripts/04`. Verified by shell `$?` and by `subprocess.run().returncode`. Cause: `ensure_process_determinism` (`src/data/config.py:994-1018`) calls `os.execv`, whose docstring claims the parent exits and "callers observe one logical run either way" — false on Windows, where `execv` spawns a detached child and terminates the parent with 0. Isolated probe confirms: child intends `sys.exit(1)`, observed exit is 0. **Defeats TE §13.2's clean-run contract and TE §9.2's both-fixtures gate**, which cannot distinguish a pass from a refusal. Correct on Kaggle (POSIX), broken on `local` — the two authorised platforms diverge, and the local one reports success.

2. **The `04` fixture-ladder Critical could NOT be observed here.** An earlier environmental refusal (`pyyaml is required to parse governed configs`) fires before the window check. Q3 asked for the observed refusal; this clone cannot produce it. Recorded as a limit, **not** as confirmation.

3. **Integrity refusal on the `pytest==8.2.2` artifact.** Vendoring was halted: a single planted marker (`# intentional space to create a fake difference for the verification`) in `_pytest/compat.py:27`, an undeclared module-scope `import py` despite `_pytest/_py/path.py` being present, and three sibling packages from the same fetch entirely clean. Content verified byte-identical to what this environment's GitHub API serves and content-addressed to its own blob SHA — authentic to what is served, provenance undetermined. Not placed on the import path; no repository file touched.

### What I will generate on your confirmation

Seven `produces[]` artifacts under `construction/build-and-test/`: `build-instructions.md`, `unit-test-instructions.md`, `integration-test-instructions.md`, `performance-test-instructions.md`, `security-test-instructions.md`, `build-and-test-summary.md`, `build-test-results.md` — with the Kaggle-session procedure (Q4 = A) carried in the build instructions, the §18.3 preflight refusal recorded as correct gate behaviour (Q2 = A), and every count above labelled smoke evidence, never governed. **Nothing is claimed discharged**: WS-20 and TA-17 remain unreachable, TA-03 and TA-26 remain unproducible off Kaggle.

Does this all look correct before I generate the artifact?

[Answer]:
