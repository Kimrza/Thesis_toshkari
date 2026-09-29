# CR-2026-09-29-GOV-BT-03-RULINGS: execution of the Student's rulings on GOV-2026-09-29-BT-03

**Status: EXECUTED, apart from the Supervisor acts.** The Student ruled on the four
owner acts on 2026-09-29:

- **Rec 1:** adopt D-82; the agent writes it on the Student's instruction.
- **Rec 6:** tracking policy **B**.
- **Rec 14:** platform ruling **P2**.
- **Rec 3:** commit with the drafted message.

All four were executed in this pass; see §8. Two items still open:

- the Supervisor countersignature on D-82 and on P2 (Rec 47's authorization);
- the post-commit re-run addendum (Rec 3, step 2).

The first owner-act draft of this record said this record writes no D-number. That held
until the Student's instruction; D-82 was then written to `evidence/DECISIONS.md` on that
instruction, matching the D-74-amendment precedent.

**Authority.** The Student's rulings of 2026-09-29 on all 17 recommendations of the
full-board report `governance/reviews/GOV-2026-09-29-BT-03.md` (verdict FAIL).

## 1. Executed (working tree, uncommitted)

| Rec | Ruling | What was done | Evidence |
|---|---|---|---|
| 4 | 1 | Dated correction: the first blocker of the clean run is promoting the `plumbing_7day` candidate, then the Q-31 freeze | `build-test-results.md` § 2026-09-29 corrections; summary; `integration-test-instructions.md` |
| 5 | 1 | Snapshot count corrected from 131 to **133**; the 2 this session created are named | the same section |
| 6 | 1 | 7 untracked release directories and 97 `*.archived-*` paths disclosed; the policy ruling is routed (§4) | the same section |
| 7 | 1 | `test_control_20b_receipt_at_the_same_instant_as_the_call_raises` added. Bite-proof: with `<` relaxed to `<=` the control FAILED; the guard was restored and `git diff -- src/` is empty | `tests/test_common_masks.py` |
| 8 | 1 | The runtime annotated in place: full suite 660.7 s, crit 105.8 s, fixture 365–366 s | summary, Readiness |
| 9 | 1 | The `gf-3` disclosure widened to `208f138`, `9710daf` and this test edit | results § corrections |
| 10 | 1 | Superseded pointers added to the summary header, the module count, the 2026-09-25 verdict, results line 74 and integration instructions | those files |
| 11 | 1 | The orphan `test_zz_bite_common_masks*.pyc` deleted | `tests/__pycache__/` |
| 13 | 1 | The sidecar SHA-256 is recorded with the commit-anchored re-run (§3) | results § corrections |
| 15 | 2 | `test_target_definition_id_is_byte_identical_everywhere_it_is_declared` added, with a case-variant control. Bite-proof: `experiment.yaml` retyped to `GRIDDED_VTEC_1H` made the test FAIL; the file was restored with `git checkout` | `tests/test_prepared_target_schema.py` |
| 16 | 1 | The §12 set enumerated from the Technical Environment: 21 mandated, 18 present, 3 absent (all Phase 2-only); the transition-hash tests are located | results § corrections |
| 17 | 1 | The report persisted | `governance/reviews/GOV-2026-09-29-BT-03.md` |

**Cross-unit edits (per code-generation c32; the rulings above are the explicit ruling):**

- `tests/test_common_masks.py` belongs to `evaluation-and-comparison`.
- `tests/test_prepared_target_schema.py` belongs to `target-standardization`.

Both owners' code-summaries are now out of date for these edits, and are carried under gf-3.

## 2. Rec 2 (ruling: option 2): annotating the two untraceable commits

History is not rewritten, so the freeze tags stay valid. This section is the traceability
record for the two commits.

- **`889acdd`** (2026-09-28 20:24 +0330, message "your commit message"). It adds 50 files
  and 6802 lines, all under `artifacts/walking_skeleton/plumbing_7day/`. They are
  `predictions/FIX-NOV-FOLD-0{1,2}.archived-989f290` and the
  `features/*.archived-989f290` fold bundles, which archive the fixture outputs
  superseded by commit `989f290`'s adoption of D-78…D-81. It is an archive-only
  commit: it changes no config, no source code and no decision. The outputs were
  superseded by `989f290` adopting **D-78…D-81**. No decision governs the archiving act
  itself; it follows the project's "archive, never delete" convention (the
  `*.archived-*` renames in `CR-2026-09-29-Q31-CLOSURE` §5A).
- **`208f138`** (message "Record fixture resolution decisions", no body). It touches
  196 files. The material content:
  - `src/evaluation/masks.py`: `source_id` moves from `_IDENTITY_KEYS` to a new
    `_PROVENANCE_KEYS`;
  - `tests/test_common_masks.py`: +3 tests:
    - `…different_source_id_are_accepted_when_lineage_matches`;
    - `…disagreeing_on_phase_id_or_target_definition_id_still_refuse`;
    - `…missing_or_empty_source_id_still_refuses`;
  - `evidence/DECISIONS.md`: +43 lines, the D-49 addendum 2 (WSL2);
  - five fixture release directories, and a `registry_entry.json` update.

  The mask change has **no governing decision**. Its D-number is proposed in §3 and
  remains open until the Student adopts it.

Residual risk, disclosed: the hook was left unchanged under the ruling, so a placeholder
message can still pass it. This record mitigates what already happened; it does not
prevent the next one.

## 3. Rec 1 (ruling: option 1): proposed D-82 text, for the Student to adopt

> **D-82 — Comparison-set identity vs provenance: `source_id` is provenance (owner
> ruling, 2026-09-29; ratifies commit `208f138`).** Members of a declared comparison
> set must agree on `phase_id` and `target_definition_id`, which together form the
> comparison-context identity. `source_id` is **provenance**. Every member must carry a
> present, non-empty `source_id`, and the mask records every distinct producer, but
> members are not required to share it. **Reason:** the primary comparison is the LSTM
> (`source_id=GNSS_VTEC`) against IRI-2016 (`source_id=IRI2016_B01`), so requiring
> `source_id` equality made the primary comparison impossible to build. Stamping all
> three ids on every artifact (TEC-05, project.md Mandated) is unchanged. Agreement on
> target lineage is what makes a comparison fair under NFR-FAIR-01; agreement on
> producer never did. Enforced by `src/evaluation/masks.py` (`_IDENTITY_KEYS`,
> `_PROVENANCE_KEYS`) and by the three `208f138` tests in `tests/test_common_masks.py`.
> Supervisor countersignature: required under TE §18.2 if the Student classes the
> comparison-set structure as a G-05 input (D-80 precedent), and **open**.
> CR-2026-09-29-GOV-BT-03-RULINGS.

Until D-82 is adopted, Recommendation 1 stays open and the stage's governance verdict
stays FAIL.

## 4. Rec 6: tracking policy for snapshots, archives and releases (open, for the Student)

The untracked items are 133 `artifacts/run_snapshots/*`, 97 `*.archived-*` paths, and
7 release directories under `plumbing_7day/releases/`.

- **A. Commit everything.** Pro: fully durable; TA-15 hashes point at recoverable bytes.
  Con: the repository grows by roughly the size of these directories, and every future
  run adds more.
- **B. Commit releases only; gitignore snapshots and archives, with a committed hash
  manifest for each.** Pro: the immutable TE §13.3 objects are durable; derived and
  scratch outputs become verifiable but not stored. Con: the bytes of snapshots and
  archives are lost with the disk.
- **C. Gitignore everything and keep a committed SHA-256 manifest.** Pro: the
  repository stays small. Con: releases are not recoverable, which breaks the
  durability TE §13.3 expects.

Recommended: **B**. Only releases are TE §13.3 objects; snapshots are re-derivable,
because `load_configs` writes them on each call.

## 5. Rec 14 (ruling: option 2): proposed platform rulings (Student + Supervisor)

The GitHub Actions `verify.yml` runs on Ubuntu and Windows runners. It deselects the
five restricted-reader modules, but its checkout still materialises the tracked
`evidence/locked_test_restricted/` root.

- **P1. Authorise CI as a non-scientific verification surface (write the Rec 47
  record).** CI may run non-restricted tests only. Restricted readers stay deselected,
  and CI output is never gate evidence. Pro: keeps the automatic check on push. Con: the
  locked month still lands on third-party runners at checkout, and access through that
  path goes unrecorded.
- **P2. P1 plus a sparse checkout that excludes `evidence/locked_test_restricted/`.**
  Pro: closes the custody residual while keeping CI. Con: one workflow change, and it
  needs a test proving the root is absent on the runner.
- **P3. Retire the workflow.** Pro: exactly two platforms, matching TC-03c and team.md's
  "No CI service is used". Con: loses automatic push-time verification; the local hook
  becomes the only automatic check.
- **P4. Untrack the restricted root from git**, whichever of P1–P3 is chosen. Pro:
  removes the exposure at its source. Con: it reverses the 2026-09-24 locked-root ruling
  (ACCEPTABLE, conditioned) and needs its own change record; the locked bytes then need
  another custody home.

Recommended: **P2**. It is the smallest change that keeps the automatic check and closes
the custody residual. P3 is equally defensible if strict two-platform conformance
outweighs CI convenience.

## 6. Rec 12: recorded obligation

At the Q-31 freeze of `plumbing_7day`, the frozen manifest's `sample_iri_gim_values`
`note` gains one line. The line says the comparison is grid cell against station
coordinate, and that the steady offset of GIM above IRI partly reflects IRI's frozen
`htop_km: 2000.0` integration height against GIM's plasmasphere content (Vision §6.6).
Owner: Student, at the freeze act.

## 7. Rec 3: the commit, then a re-run (open; the commit is the Student's act)

1. The Student commits the stage edits (the two test files, the stage artifacts, this
   record and the report) with a message citing this record.
2. The crit set and the full suite are re-run at the new commit.
3. The junit files and the sidecar SHA-256 are recorded in an addendum that names the
   commit.

This record is updated with the commit hash when that is done.

## 8. Owner acts executed on the Student's rulings (2026-09-29)

- **Rec 1: D-82 adopted.** The §3 text was appended to `evidence/DECISIONS.md` on
  the Student's instruction. It sits before `## Supervisor review` and keeps the
  register's CRLF line endings. Supervisor countersignature: **OPEN**.
- **Rec 6: policy B applied.**
  - `.gitignore` gains `artifacts/run_snapshots/` and `*.archived-*`, with a
    negation that keeps archived *releases* tracked.
  - The 1142 untracked snapshot and archive files (24,863,590 bytes) are hashed in
    the committed `artifacts/untracked_outputs_manifest_2026-09-29.json`.
  - The seven release directories are committed.
  - The 1684 snapshot files and 163 archive files tracked before this rule stay
    tracked.
- **Rec 14: P2 applied.** The `actions/checkout` step in `.github/workflows/verify.yml`
  now uses a non-cone sparse checkout that excludes `evidence/locked_test_restricted/`.
  A new custody step fails the job if that root is ever materialised.
  - Local simulation (a `git clone --no-checkout` with the same patterns): root
    **absent**, 29 files still tracked, the rest of `evidence/` present.
  - Not yet observed on a GitHub runner; that needs a push.
  - Supervisor countersignature on the platform authorization (Rec 47): **OPEN**.
- **Rec 3: commit.** Made with the drafted message; the hash is recorded in the
  post-commit addendum of `build-test-results.md`.
