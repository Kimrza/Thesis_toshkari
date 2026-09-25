# Change record — 2026-09-24 — GOV-2026-09-24-BT-01 rulings and remediation

**ID:** `CR-2026-09-24-GOV-BT-01-RULINGS`
**Authority:** the Student's explicit rulings of 2026-09-24 on all sixteen recommendations of
governance report `GOV-2026-09-24-BT-01` (build-and-test stage review; verdict FAIL). The
rulings arrived as one message: R1=opt 1 ("and make sure this issue never happens again"),
R2=opt 1, R3=opt 2, R4=opt 2, R5=opt 1, R6=opt 1, R7=opt 1, R8=opt 1, R9–R16=approve
(each block's stated preferred option).
**Repository state at start:** `41fd109` + the build-and-test stage artifacts and the D-68
test-pin amendment already in the working tree.
**Written FIRST, before execution, per this project's change-record convention.**

## Ruling-by-ruling disposition

| Rec | Ruling | Action taken in this pass |
|---|---|---|
| 1 | Option 1 + never-again | **Retrieval BLOCKED from this network** (see §2) — negation line + prevention control executed; retrieval spec recorded for an IGS-reachable host; commit deferred until the bytes exist |
| 2 | Option 1 | `build-instructions.md` addendum recipe corrected to the executed command; refused matplotlib install recorded separately |
| 3 | Option 2 | `core.hooksPath` set to `.githooks` on this clone under this ruling; fresh dated verification written into the two artifacts; PATH dependency disclosed |
| 4 | Option 2 | Both passages corrected to the sidecar log (`artifacts/exec_evidence/test_access_log.jsonl`) + provenance note that the stale claim migrated from the pre-Rec-1 diary entry of 2026-09-18 |
| 5 | Option 1 | Reconciliation paragraph written into `build-test-results.md` (766/766 unevidenced; committed 766-XML shows 2 failures; selection set-difference); hook qualified as the five-module commit-time subset in `unit-test-instructions.md` and `build-test-results.md` (the security artifact carries the deselection substance without the count — closure-verification finding 1); "which selection is THE §18.3 run" routed to the Student as an open question |
| 6 | Option 1 | `full.xml`, `crit.xml`, `acq.xml`, `conda list --export`, `requirements.txt` SHA-256 persisted under `artifacts/exec_evidence/run_2026-09-24_git-ae-srv/`; Sources repointed; first-pass row marked no-surviving-XML |
| 7 | Option 1 | Dated custody addendum in `security-test-instructions.md`: sixth purpose, callers, day bound, G-05 gate, kill switch, six `test_ph_*` tests |
| 8 | Option 1 | Staleness disclosed in `build-and-test-summary.md`; `src/models/persistence.py:29–46` docstring repaired under this ruling (the owner-authorized cross-unit amendment); `models-and-baselines` code-summary given a dated addendum per `gf-3` |
| 9 | Approve (opt 1) | `read_persistence_history_lookup` Raises clause and the `:544–547` comment corrected to filter semantics |
| 10 | Approve (opt 1) | `run_id` parameter threaded from the stage-06 wiring; refuse-empty; new test + wiring test updated |
| 11 | Approve (opt 1) | Disclosure line for `artifacts/run_snapshots/20260924T192432Z-79c9b825/` added to `build-test-results.md` |
| 12 | Approve (opt 1) | Rec 30 citation corrected to option 1 (deselect restricted readers from the commit set) |
| 13 | Approve (opt 1) | Disposition option 2 reworded to "the two declared JSON artifacts", `hash_count` 5→2 noted (textual accuracy only — R1's ruling selects option 1, so option 2 is not executed) |
| 14 | Approve (opt 1) | Addendum sentence superseding `build-instructions.md` Step 6's ladder-state paragraph |
| 15 | Approve (opt 1) | R-05 reference repointed to `governance/CHANGE_RECORD_2026-09-13_R05_windows_exit_code.md` |
| 16 | Approve (opt 1, folded) | The stale five-member comment above `PURPOSES` corrected in the same authorized touch of `locked_test.py` as R9/R10 |

## §2 — Rec 1: what is executable here and what is not, measured

The three IGS site logs (`aruc00arm_20260317.log`, `bshm00isr_20260422.log`,
`nico00cyp_20251027.log`) must be re-retrieved and verified against the committed
`sha256_manifest.json`. Probed 2026-09-24 from this host: `files.igs.org` (the recorded
source), `igs.org`, `network.igs.org`, `igs.bkg.bund.de`, `epncb.oma.be`, `epncb.eu`, and
`gnss-metadata.eu` **all connect-timeout**; the reachable egress set observed this session is
approximately {github.com, repo.anaconda.com, conda.anaconda.org}. The retrieval is therefore
**not executable from this network**, and no substitute bytes were invented.

**Retrieval specification, complete and host-independent** (everything a future session or the
Student needs): the recorded URLs, expected SHA-256 values, and expected byte counts are all
in `evidence/station_registry_sources_2026-09-19/sitelog_index.json` (17,177 / 18,442 /
28,906 bytes respectively, retrieved 2026-09-19T20:15Z). Acceptance: SHA-256 of the retrieved
bytes equals the recorded hash. On mismatch: record the divergence (provider superseded the
log — DATA-07's version-drift rule by analogy) and route to the Student; never silently
accept different bytes under the recorded name. After verification: commit the three files —
the `.gitignore` negation below already guarantees git will take them.

**Never-again mechanism, executed now (the ruling's second clause):**

1. `.gitignore` gains `!evidence/**/*.log` (and the run-snapshot-safe equivalent for
   `artifacts/` manifest-declared evidence is covered by the test below) so a generic
   build-noise pattern can never again swallow governed evidence bytes.
2. A new negative control in `tests/test_release_hashes.py` (authorized by this ruling):
   every file declared in any tracked `sha256_manifest.json` must NOT be matched by
   `.gitignore` — asserted via `git check-ignore`, so the defect is caught **at authoring
   time on the machine that still holds the bytes**, not two clones later. The control is
   proven to bite by construction: at pre-fix HEAD, the three site-log paths are ignored and
   the test fails; with the negation line, it passes.

## §3 — Rec 3: the activation act and its disclosed consequence

`git config core.hooksPath .githooks` was run on this clone under the Student's option-2
ruling (the hook header's "no agent may run that command" is superseded by this explicit
instruction, recorded here). Disclosed consequence, measured: the hook requires `python` with
`pytest` importable on `PATH`; this machine's default `python` is a Windows Store stub, so a
commit made from a shell without the governed environment on `PATH` will be **blocked by
design** with the hook's own message. That is the affirmed Q7=D behaviour, not a defect; the
commit procedure in `build-instructions.md` records the `PATH` prefix needed.

## §4 — Evidence and verification

Every edit in this pass is re-verified by: the module-scoped pytest runs recorded in
`build-test-results.md` (updated), the persisted junit XMLs under
`artifacts/exec_evidence/run_2026-09-24_git-ae-srv/`, and a closure-verification pass over
all sixteen recommendations whose result is appended to the stage record. Frozen scientific
values touched: **none**. December bytes read: **none**.

## §5 — Closure verification and updated verdict (2026-09-24)

An independent adversarial closure-verification pass re-derived every closure at the
mechanism level (recomputed hashes and junit tuples; an empirical git-level proof that the
new manifest-vs-gitignore control bites when the negation is removed; code-level
confirmation the `run_id` threading refuses when absent and reaches the sole production
call site). Result: **15 of 16 CLOSED, Rec 1 PARTIAL** (retrieval network-blocked; spec
frozen; never-again half done), **no new defect**. Four notes recorded, including the
verifier's own disclosed-and-restored transient overwrite of `.gitignore` during probing
(`git diff` verified to show only the intended Rec-1 block afterwards). Post-remediation
full suite: **1584 / 1581 passed / 3 failed / 6 skipped** (`full_post.xml`) — the three
failures are the site-log custody rows only.

**Updated board verdict: `CONDITIONAL PASS`** (from FAIL), with exactly one condition:
the three IGS site logs are retrieved on an IGS-reachable host, verified against the
SHA-256 values and byte counts in `sitelog_index.json`, and committed **before this
stage's evidence is relied on at any freeze gate**. Owner: Student. The board's verdict
remains a recommendation; the human's acceptance at the stage gate is the approval.
