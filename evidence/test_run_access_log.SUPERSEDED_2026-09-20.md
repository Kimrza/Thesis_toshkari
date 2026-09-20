# `evidence/test_run_access_log.jsonl` — SUPERSEDED and CLOSED 2026-09-20

**Status:** closed to further appends as of this remediation. **Not deleted, not rewritten,
not truncated. Not one row was modified.** Records are superseded, never deleted.

**Authority:** the approved governance remediation of **Recommendation 1**, owner ruling
= option 2 (separate the test-mode access log from the governed evidence access log).

---

## What the 5,964 rows are

Every row in `evidence/test_run_access_log.jsonl` is a **test-suite** access record, written
by the `src/data/locked_test.open_restricted` chokepoint on behalf of two pytest modules.
Not one of them is a real, governed December access.

| Fact | Value | How derived |
|---|---|---|
| Total rows | **5,964** | `wc -l` over the file, 2026-09-20 |
| Distinct `run_id`s | **2** | `grep -o '"run_id": "[^"]*"' \| sort \| uniq -c` |
| `run_id: test_release_hashes` | **5,640** rows | same |
| `run_id: test_acquisition_window` | **324** rows | same |
| First `logged_at_utc` | **2026-08-28T07:26:55.543632+00:00** | first line of the file |
| Last `logged_at_utc` | **2026-09-20T15:16:20.348742+00:00** | last line of the file |
| Rows with a real `retrieved_at_utc` | **0** | `grep -vc` against the placeholder literal |
| Rows with `performance_inspected: true` | **0** | `grep -c` |
| Rows with `performance_inspected: false` | **5,964** | `grep -c` |
| Rows with `locked_test_accessed: true` | **5,964** | `grep -c` |

Every count above was derived from the file and printed before being asserted
(`project.md` `application-design:count-derivation`). No row was opened for its December
content; the derivations above read only the JSON envelope fields named in the table.

## The three defects this closure addresses

1. **Every row carries a PLACEHOLDER `retrieved_at_utc`** — the literal string
   `"recorded-at-call-time-by-the-runner"`, on all 5,964 rows without exception. A
   caller-supplied field that is the same constant on every row cannot evidence anything,
   which left FR-P1-02-3 / VAL-2's log-then-read **ordering** requirement unverifiable from
   the one artifact that records it. (The guard's own `logged_at_utc` stamp, added
   2026-08-28 for exactly this reason, is real and is what the ordering check actually uses;
   `retrieved_at_utc` sat alongside it saying nothing.) Both producers now write
   `dt.datetime.now(dt.timezone.utc).isoformat()`, and
   `src/data/locked_test.AccessRecord.__post_init__` now **refuses** any value that does not
   parse as ISO-8601, so no future producer can reintroduce the placeholder.

2. **Suite noise was indistinguishable from a governed access.** A G-06 reviewer opening
   this file to find a real December access had to find it among 5,964 test rows. From
   2026-09-20 the two test modules write to `artifacts/exec_evidence/test_access_log.jsonl`
   (gitignored), and `evidence/test_run_access_log.jsonl` is reserved for real, governed
   accesses only.

3. **The R-19 reconciliation had never been run against the real pair.**
   `src/data/experiment_registry.reconcile_access_records` joins `AccessRecord` and
   `RegistryEvent` on `run_id` and raises on an orphan in either direction. With 5,964
   access rows under two `run_id`s that appear nowhere in
   `artifacts/registry/experiment_registry.jsonl` (28 rows, none carrying
   `locked_test_accessed`), that reconciliation would have raised on the first row.
   `tests/test_release_hashes.py` and `tests/test_locked_test_guard.py` now carry the
   standing check; see § Reconciliation below.

## Nothing here inspected performance

All 5,964 rows record `purpose: coverage_audit` and `performance_inspected: false`. Vision
§8.3 permits the performance-blind class before G-05, and the required pre-G-05 December
coverage and regime audit is a separate, still-unperformed event. **No row in this file is
the G-06 one-shot locked evaluation, and none may be read as evidence that it occurred.**

## Reconciliation, and what remains owed

These 5,964 rows are **expected orphans** against
`artifacts/registry/experiment_registry.jsonl`: they were produced by pytest runs, which
open no registry run. `reconcile_access_records` accepts them only through its
`known_orphans` mapping, which **reports** rather than suppresses them and never writes.
It must never be satisfied by back-filling a registry row — that is the reconstruction
failure this project has already refused once.

**Owed to the owner, not performed here:** a ruling on whether the two historical `run_id`s
are registered as permanent `known_orphans` with this notice as their reason, or whether the
closed log is excluded from reconciliation entirely on the ground that it is now a
superseded artifact rather than a live one. This notice states the facts; the ruling is the
student's.

## Provenance of this notice

Written 2026-09-20 by the approved Recommendation 1 remediation. The log file itself was
opened read-only and was neither edited, reordered, truncated, deduplicated nor
re-timestamped. No December 2022 value was read.
