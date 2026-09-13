# Change Record — 2026-09-13 — R-05 Windows exit-code propagation repair

**Change ID:** `CR-2026-09-13-R05-WINDOWS-EXIT-CODE`
**Authority:** the project decision owner's explicit instruction of **2026-09-13**, given
verbatim in-session after the evidence-only R-05 Decision Brief: *"Act as the
implementation engineer … Your task is to resolve ONLY the currently actionable R-05
Windows exit-code defect"*, with the repair contract spelled out (POSIX `os.execv`
preserved; Windows spawn-and-wait propagating the child's return code; docstring
corrected; minimum tests; no commit). This is the owner instruction `project.md`
(`code-generation:c32`) names as the sanctioned route for an edit to a READY-reviewed
unit's module.
**Repository state:** written from `HEAD = 1670ac8`. **No commit is made by this pass**
(owner instruction; the commit remains the student's act).
**Register discipline:** no agent writes `evidence/DECISIONS.md`. **No D-number is
required or drafted**: this repair decides no scientific constant, no governed config
value, and no §18.2 item — it changes process exit-code handling only. The commit, when
the student makes it, cites this change ID per `team.md`'s linking rule.

This record is written FIRST, before any code or test edit of this pass.

---

## 1. The defect (evidence summary; full brief in the session record and
`construction/build-and-test/memory.md`)

`src/data/config.py:994-1018` `ensure_process_determinism` — R-05's mechanism, the first
statement of `main()` in all nine stage scripts and `scripts/run_walking_skeleton.py` —
re-execs via `os.execv` when `PYTHONHASHSEED` is unset. Its docstring asserted: *"On
Windows, `os.execv` spawns a replacement process and the parent exits — callers observe
one logical run either way."* The second half is **false on Windows**: the parent
terminates with exit code 0 without awaiting the detached child, so the child's exit
code is discarded. Observed 2026-09-13 on CPython 3.11.16 (the governed pin), three
measurements, two methods: `run_walking_skeleton.py` printing `preflight refusal: …`
exited **0** (shell `$?` and `subprocess.run().returncode`); an isolated probe whose
child intends `sys.exit(1)` observed **0**.

**Blast radius, derived not assumed:** the outermost process ONLY. Every child
invocation is already defended — `child_environment`
(`scripts/run_walking_skeleton.py:544-549`) refuses to launch a child without
`PYTHONHASHSEED` (R-138 control 20), and the subprocess-driving tests set
`PYTHONHASHSEED=0` explicitly (e.g. `tests/test_external_drivers.py:727`), so children
never re-exec and their exit codes are real. The exposed case is exactly TE §13.2's
literal command sequence invoked from a shell on `local` (Windows), one of the two
authorised platforms (TC-03c).

**Contracts defeated while unrepaired:** TE §13.2 (a failing step is undetectable by
exit code); TE §9.2 (the fixture orchestrator reports 0 whether it completed or
refused); `project.md` § Mandated "ALWAYS surface an integrity failure … with an
explicit exit"; `team.md`'s two-tier posture ("terminate the run"); the build-and-test
stage file's "the build's own exit code is the load-bearing signal".

**POSIX is believed correct by `execv` image-replacement semantics and was NOT tested**
— no POSIX host is reachable from this clone. That inference is recorded as untested.

## 2. The repair, exactly

`src/data/config.py`, `ensure_process_determinism`, platform split at the re-exec:

- **POSIX — unchanged**: `os.execv(sys.executable, [sys.executable, *argv])`. Genuine
  image replacement; the single process's exit code propagates natively.
- **Windows (`os.name == "nt"`) — new**: after the same two environment writes
  (`PYTHONHASHSEED`, the re-exec sentinel — so the child inherits exactly what the
  `execv` path would have passed), **spawn the replacement interpreter, WAIT for it,
  and exit the parent with precisely the child's return code**:
  `raise SystemExit(subprocess.run([sys.executable, *argv], check=False).returncode)`.
  No detach, no swallowing, no normalisation: 0 stays 0, 1 stays 1, 7 stays 7.
- **Docstring corrected** to state the split and keep the sentinel accounting truthful:
  the child (either platform) still sees `PYTHONHASHSEED` + sentinel, still pops the
  sentinel once, and `DeterminismRecord.reexec_performed` still records exactly one
  logical run. The module-level comment at the sentinel constant (`:443`) is aligned
  where it named `os.execv` as the only carrier.

**What does not change:** no scientific value, no governed config, no seed, no data
path, no import edge, no guard condition. `subprocess` and `sys` were already imported
(`config.py:101-102`). On POSIX the diff is dead code plus prose. Computed outputs of a
logical run are byte-identical on both platforms.

## 3. Design-consistency note (annotation here, never an edit to the signed design)

`foundation`'s functional-design and the inline comment said "The R-05 re-exec IS the
mechanism". After this repair the mechanism is: **exec-replacement on POSIX,
spawn-and-wait on Windows — in both cases one logical run whose exit code is the
child's.** The signed functional-design artifact is not edited (`project.md`,
never-edit-a-signed-record); this paragraph is the standing reconciliation, and the next
practices/design gate may ratify a wording amendment if wanted.

## 4. Tests added (minimum set; no existing control weakened)

In `tests/test_determinism.py`, beside the existing re-exec controls:

1. `test_reexec_child_failure_exit_code_propagates_to_caller` — **the load-bearing
   negative control**: a stage-shaped script with `PYTHONHASHSEED` unset re-execs and
   its child exits 7; the caller must observe 7, never 0. This is the test that fails on
   the pre-repair code and catches any regression to detached spawning.
2. `test_reexec_child_success_exit_code_is_zero` — the happy path: child exits 0,
   caller observes 0.
3. `test_r05_platform_split_is_exact_in_source` — AST control (repo's established
   style): the POSIX branch still calls `os.execv`; the `nt` branch calls
   `subprocess.run` and raises `SystemExit` with its return code; no third path.

The two existing controls are untouched and remain valid:
`test_reexec_establishes_pythonhashseed_and_records_exactly_one_run` (its Windows
handshake-file poll now succeeds immediately, since the outer `subprocess.run` waits —
the poll is satisfied, not bypassed; its `lines == 1` assertion is the recursion guard)
and `test_no_reexec_when_pythonhashseed_already_set`.

## 5. Disclosure obligations (`project.md` `code-generation:c30`/`gf-3`)

`src/data/config.py` and `tests/test_determinism.py` are **`foundation`'s modules**,
READY-reviewed at the now-approved `code-generation` gate. Foundation's `code-summary.md`
is therefore stale for this edit (its Files table and its 43-test-function count). **It
is deliberately NOT edited here**: the owner instructed "do not silently reopen or
invalidate governance receipts yourself", and `gf-3` sanctions the alternative — the
staleness is carried as an explicit finding to the next gate (build-and-test's), via
this record and the build-and-test stage diary. Counts after this pass, derived:
`tests/test_determinism.py` 43 → **46** `def test_` functions.

## 6. Verification performed (appended after execution, same day)

Recorded in § 7 below once the narrowly-scoped probes run. Scope permitted by the owner:
R-05 probes and the re-exec tests only — no full suite, no fixture ladder, no Kaggle, no
governed evidence claimed.

## 7. Results — appended 2026-09-13 after the probes ran

All runs on real CPython 3.11.16 (the governed pin) under the stdlib stand-in — **smoke
evidence only, never governed** (TC-03g still requires the Kaggle session; no real
pytest exists on this clone).

**Repaired code — the five R-05-relevant tests, and ONLY those (owner's scope):**

```
PASS  test_reexec_child_failure_exit_code_propagates_to_caller
PASS  test_reexec_child_success_exit_code_is_zero
PASS  test_r05_platform_split_is_exact_in_source
PASS  test_reexec_establishes_pythonhashseed_and_records_exactly_one_run
PASS  test_no_reexec_when_pythonhashseed_already_set
5/5 passed
```

**Mutation proof that the load-bearing control bites** — the same failure probe run
against the PRE-repair `config.py` (extracted from `HEAD = 1670ac8` into the session
scratchpad; the repository itself untouched):

```
pre-repair: child re-exec'd=True, child exited 7, CALLER OBSERVED exit=0
CONTROL BITES
```

So on the unrepaired code the new negative control fails (observes 0 where 7 is
required), and on the repaired code it passes — the control detects exactly the defect
class it exists for.

**Diff verification:** `git diff --check` scoped to the two repaired files is clean
(exit 0; the repository-wide run reports only pre-existing trailing-whitespace in the
tool-written audit shard, none in files this pass touched). Numstat:
`src/data/config.py` **+31/−8** (docstring, sentinel comment, the `nt` branch — no
functional change on POSIX); `tests/test_determinism.py` **+101/−0 over this pass**
(43 → **46** `def test_` functions; the file's cumulative working-tree diff of +537/−3
includes the earlier, separately-ruled R-01 census). `evidence/test_run_access_log.jsonl`
remains exactly **+74/−0** — untouched by this pass. No script, no governed config, no
dataset, no locked-test content, no other unit's module changed.

**Deliberately NOT run, per the owner's scope:** the full suite; the fixture ladder
(so the repair's effect on `run_walking_skeleton.py`'s shell-visible exit code, while
implied by the probes, is NOT claimed as observed); Kaggle; anything producing governed
evidence. POSIX behaviour remains **untested inference** — no POSIX host is reachable.

**No commit was made by this pass.** The student's eventual commit cites
`CR-2026-09-13-R05-WINDOWS-EXIT-CODE`.
