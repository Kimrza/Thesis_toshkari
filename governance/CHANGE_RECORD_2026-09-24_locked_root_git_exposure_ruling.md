# Change record — 2026-09-24 — locked-test-root git exposure, ruled acceptable

**Authority:** Student ruling — "ACCEPTABLE, conditioned on no impact to model training or
performance." **Repository state:** working tree as left by the prior sessions, nothing
committed by this pass.

## What was checked

Whether `evidence/locked_test_restricted/` being tracked in git (confirmed:
`git ls-files | grep locked_test_restricted` returns real files) creates any pathway by which
its bytes could reach feature engineering, training, or evaluation other than through the
audited `open_restricted` chokepoint.

```
$ grep -rln "locked_test_restricted" --include="*.py" src/ scripts/
src/data/locked_test.py
scripts/merge_coverage_year.py

$ grep -rn "evidence/\|EVIDENCE_DIR\|evidence_root" --include="*.py" src/features/ src/models/
src/models/lstm.py:10:...evidence/DECISIONS.md...   <- a documentation citation, not a path read

$ grep -rn "glob\|rglob\|walk\|listdir\|iterdir" --include="*.py" src/ scripts/ | grep -i evidence
src/data/fixture_evidence.py   <- unrelated (Kaggle-session gate check, no evidence/ walk)
src/data/locked_test.py:918    <- december_custody_inventory, walks evidence/ but EXPLICITLY
                                   resolves and treats `locked_test_restricted` as the excluded
                                   boundary it scans FOR, not a source it reads FROM
```

**Findings:**

1. **`src/features/` and `src/models/` never reference `evidence/` at all.** No glob, walk, or
   path construction in the feature-building or modelling code touches this directory tree,
   directly or transitively — confirmed by grep across both packages, zero path-reading hits.
2. **Exactly two files reference the restricted root by name**: `src/data/locked_test.py` (the
   `open_restricted` chokepoint itself, plus the D-15 custody scanner, which walks `evidence/`
   specifically to detect and exclude December content from elsewhere — its own stated purpose)
   and `scripts/merge_coverage_year.py` (an acquisition-side, pre-Phase-2 script, gated by the
   same phase boundary that bars Phase 1 from raw-processing paths).
3. **`open_restricted` (`src/data/locked_test.py:436`) is the single chokepoint** — it refuses
   any path not under `RESTRICTED_ROOT`, and every read of restricted content this project's
   test suite and pipeline perform routes through it, logging an `AccessRecord` each time
   (already exercised and verified in this session's earlier Layer-2 §3 guard-verification run:
   766 tests, access rows appended, no metric/prediction computed).
4. **No accidental-inclusion pathway found**: no build step, feature dictionary entry, or
   config glob was found that could pull `evidence/locked_test_restricted/` content into a
   feature matrix, a model input, or a metric without going through `open_restricted` first.

## Ruling

**Git exposure of `evidence/locked_test_restricted/` is accepted**, conditioned exactly as the
Student stated: on it never being read outside the audited `open_restricted` path. That
condition is met today, by the pathway analysis above — no code path in `src/features/` or
`src/models/` can reach it, and the two files that do reference it are the guard itself and an
acquisition-side script outside the Phase 1 feature/model boundary.

**The existing guard tests are the enforcement mechanism**, not a new one: `test_phase_boundary.py`
(NFR-PHASE-01, refuses raw-processing imports into Phase 1), `test_locked_test_guard.py` (the
access-record and reconciliation controls), and `test_iri_denial.py`'s sibling pattern for a
different forbidden-import boundary all already exist and were verified passing (modulo the
two known, unrelated chokepoint-scanner self-reference false positives) in the prior session's
Layer-2 §3 run.

**This ruling does not address, and is entirely separate from, the *provenance* question**
(whether the git-tracked bytes themselves are safe to have committed at all, e.g. licensing or
data-redistribution concerns) — only the *training/evaluation-impact* question the Student
asked. No such pathway exists; the condition holds.

**No code change made.** This is a documented acceptance of an existing, already-governed
state, not a remediation.
