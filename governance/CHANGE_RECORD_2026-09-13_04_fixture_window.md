# Change Record — 2026-09-13 — Scope-derived windowing of the 04 driver audit on fixture runs (Option a)

**Change ID:** `CR-2026-09-13-04-FIXTURE-WINDOW`
**Authority:** the project decision owner's ruling of **2026-09-13**, in-session, verbatim
heading "OWNER RULING — APPROVE OPTION (A)", adopting scope-derived windowing of the
`04_build_external_products.py` audit on fixture runs, with the bounding conditions
restated in §2 below. This resolves the remedy the owner deferred earlier the same day
("record it, rule later") on the fixture-ladder deadlock finding recorded in
`CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md` § "Dated correction,
2026-09-13" and in `external-products`' code-generation plan § "Gate finding".
**Repository state:** written from `HEAD = 19b6e12`. **No commit is made by this pass**
(the commit is the student's act and needs separate authorization).
**Register discipline:** no agent writes `evidence/DECISIONS.md`. **Governance inspection
for a D-number, performed:** this repair changes no frozen scientific value — D-8's
claim boundary (calendar 2022) governs the GOVERNED full-year audit, which is unchanged;
D-11/D-14's fixture windows are read, never written; the fixture-scoped audit artifact is
plumbing evidence under TC-03f, a class TE §9.2/TC-03f already define. **No D-number is
required.** The commit, when authorized, cites this change ID.

This record is written FIRST, before any code or test edit of this pass.

---

## 1. The defect being repaired (root cause, from the read-only investigation)

`scripts/04_build_external_products.py` is a full-calendar-year audit
(`_AUDIT_YEAR = 2022`, `:120`; `_audit_dst` loops months 1–12; `_audit_f107` filters on
the year) embedded in a fixture ladder whose board-Rec-2 contract requires every stage to
touch only the fixture scope's cited window. On a fixture run the ladder passes
`--fixture-manifest` unconditionally (`run_walking_skeleton.py:529`), which arms `04`'s
declared-window binding (`04:306`); `_declared_data_window()` then declares
2022-01-01..2022-12-31, which can never lie inside a 7-day or 1-month scope
(`fixture_gate.py:209-251`; `fixture_manifest.py` scopes). The refusal is unconditional,
the plumbing receipt can never be written, and WS-20/TA-17 are unreachable. The rules are
individually correct and jointly unsatisfiable for `04` as built.

## 2. The intended contract (the owner's ruling, restated as the invariant)

**INVARIANT enforced by this repair:**

> **On a fixture run (`--fixture-manifest` present), `04`'s declared audit window IS the
> fixture scope's cited window, and every audit read, count, and requirement is bounded
> to evidence intersecting that window. The declaration is made true by narrowing the
> READS — never by narrowing the report while reading wider. On a non-fixture run,
> behaviour is unchanged: full-calendar-year audit, non-exempt two-receipt gate.**

Bounding conditions honoured verbatim: `fixture_gate.py` NOT modified;
`run_walking_skeleton.py` / `PHASE1_SEQUENCE` NOT modified; the `--fixture-manifest`
binding NOT removed; no skip/no-op mode; no false declaration; D-11/D-14 values
untouched; the `acquisition.window_start/window_end` transcription and the fixture
manifests are separate prerequisite acts, NOT performed here.

## 3. The repair, exactly (all inside `scripts/04_build_external_products.py`)

1. **Window derivation.** `_stage_entry` loads the scope once
   (`load_fixture_scope(fixture_manifest)`, imported from `src.data.fixture_manifest` —
   the same one-loader every consumer uses; `fixture_gate` is untouched and re-validates
   internally as before) and, on the fixture path, passes `declared_window =
   scope.window` to the unchanged gate. The non-fixture path still passes
   `declared_window = None`. The entry dict carries `audit_window` (scope window on
   fixture runs; 2022-01-01..2022-12-31 otherwise) and `fixture_scope_id`.
2. **Windowed reads.** `_audit_dst(kyoto_dir, window=...)` iterates only the months
   intersecting the window; per-month `expected_days` and `missing_days` cover only the
   in-window day range; out-of-window monthly files are neither opened, hashed, counted,
   nor required. `_audit_f107(flux_path, window=...)` filters rows to the window and
   computes missing days over the window (`fluxtable.txt` remains the in-window carrier
   file: it is read if present, and its per-day accounting is window-bounded).
3. **Windowed integrity tier.** `_verify_recorded_hashes(evidence_root, window=...,
   fixture_scoped=...)`: on fixture runs, recorded dst entries for out-of-window months
   are not read and not required; a recorded dst entry whose month cannot be parsed from
   its filename REFUSES (fail-closed — it cannot be proven out-of-window); the recorded
   fluxtable entry keeps today's semantics (recorded-but-missing refuses; it carries
   in-window days). Non-fixture runs: byte-identical behaviour.
4. **Segregated, labelled output.** `--out` default becomes `None`; when absent it
   resolves to the current path `artifacts/external/ec1_driver_audit_manifest.json` on
   non-fixture runs (behaviour-identical) and to
   `artifacts/walking_skeleton/<fixture_id>/external/ec1_driver_audit_manifest.json`
   (under `WALKING_SKELETON_ROOT`, the Rec-4 root convention) on fixture runs — so a
   plumbing artifact can never land on, or divergently collide with, the governed
   full-year manifest path. The run summary and each series entry carry
   `evidence_class: "fixture_plumbing"` plus the scope id and window on fixture runs,
   with the TC-03f statement that this is never scientific governed-run evidence; the
   three new field names are added to `PRODUCED_FIELDS` (screened through R-24 as ever).
   TE §15.4's required-output enumeration names no driver-manifest output, so no fixture
   receipt expectation changes.
5. **Docstrings/labels** updated where they asserted the full year unconditionally; the
   `_AUDIT_YEAR` constant and D-8 note stay, now explicitly the NON-fixture window
   identity. GFZ/absent-series completeness strings derive their range label from the
   window (full-year label renders byte-identically as `2022-01..2022-12`).

## 4. Full-year (non-fixture) compatibility argument

With `--fixture-manifest` absent: `declared_window` stays `None` (gate call unchanged);
`audit_window` = (2022-01-01, 2022-12-31), so `_audit_dst` iterates exactly months 1–12
with full-month `expected_days`, `_audit_f107`'s window filter is extensionally identical
to the old `date.year == 2022` filter, `_verify_recorded_hashes` checks the identical
list, the output path resolves to the identical default, and no labelling fields are
emitted. The only observable differences on a governed run are none; the diff on that
path is signature plumbing plus prose.

## 5. Tests that prove the repair (in `tests/test_external_drivers.py`)

1. **Load-bearing negative control** — `_audit_dst` under a 2022-11-01..07 window with a
   POISONED out-of-window artifact (`dst_provisional_202201.html` created as a
   *directory*, so any open/hash attempt raises): the audit must succeed, report only
   the in-window month, and neither read nor count nor require January. Run against the
   PRE-repair code this control fails (the old signature reads all 12 months and trips
   the poison / counts out-of-window months missing).
2. **Declaration-truth control** — on the fixture path, the declared window handed to
   the gate is derived from `scope.window` (behavioural, via a stub scope; plus an AST
   pin that `_stage_entry`'s fixture branch consumes the scope window and that no
   full-year literal reaches the gate on that path).
3. **Full-year invariance control** — without a window override: `_audit_dst` still
   iterates 12 months (absent months named exactly as today), `_audit_f107` still
   accounts the whole year, the default output path is unchanged, and the fixture-only
   labelling fields are absent.
4. **Narrowest ladder/integration control** — `_verify_recorded_hashes` fixture-scoped:
   a recorded out-of-window dst entry that is MISSING on disk does not refuse, while the
   same recording refuses on the non-fixture path (both directions asserted); and the
   unparseable-filename fail-closed refusal.

Executed under the stdlib stand-in on real CPython 3.11.16 — **smoke evidence only,
never governed** (TC-03g; no real pytest exists on this clone). No full suite, no
fixture ladder, no Kaggle.

## 6. Disclosures

- `scripts/04_build_external_products.py` and `tests/test_external_drivers.py` are
  `external-products`' modules, READY-reviewed at the closed `code-generation` gate
  (that unit's stage verdict is terminal NOT-READY on precisely this deadlock). Its
  `code-summary.md` becomes stale for this edit; per `project.md` (`gf-3`) the staleness
  is carried to the next gate via this record and the `build-and-test` stage diary — the
  receipted record is not edited.
- Adjacent standing fact, NOT solved here: TE §15.4 requires `iri_benchmark.parquet` and
  `gim_comparator.parquet` among fixture outputs while `04`'s R-59/Q-15 refusals stand —
  the fixture ladder will record those as missing outputs until their own gates resolve.
  Separate prerequisites also unchanged: the two `fixture_manifest.yaml` freezes
  (student, Q-31) and the `acquisition.window_start/window_end` transcription (owner).

## 7. Results — appended 2026-09-13 after the probes ran

All runs on real CPython 3.11.16 (the governed pin) under the stdlib stand-in — **smoke
evidence only, never governed** (TC-03g; no real pytest exists on this clone). No full
suite, no fixture ladder, no Kaggle.

**The five new controls, repaired code:**

```
PASS  test_fixture_scoped_dst_audit_reads_only_in_window_evidence
PASS  test_fixture_scoped_f107_accounting_is_window_bounded
PASS  test_fixture_scoped_integrity_tier_neither_reads_nor_requires_out_of_window
PASS  test_full_year_audit_behaviour_is_unchanged_without_a_fixture_scope
PASS  test_fixture_declaration_derives_from_the_scope_never_the_full_year
5/5 passed
```

**Mutation proof that the load-bearing control bites** — the same scenario against the
PRE-repair `04` extracted from `HEAD = 19b6e12` into the session scratchpad (repository
untouched):

```
pre-repair _audit_dst takes a window parameter: False
pre-repair walked months: ['2022-11']
pre-repair out-of-window missing entries: 11
CONTROL BITES
```

The unrepaired audit counts eleven out-of-window months missing under a 7-day scope
(the control's `missing == []` fails), so the control detects exactly the defect class
this record repairs.

**No regression in the owning module:** the full `tests/test_external_drivers.py` run
under the stand-in is **56/56 passed** (51 pre-existing + 5 new; 0 failed, 0 errors,
0 skipped). Both edited files `py_compile` clean; max line length 99 (the configured
bound).

**One disclosed behavioural tightening on malformed input (full-year path):**
`day_rows_parsed` now counts only day numbers valid for the month's in-window slice; a
malformed monthly file carrying a row for a day outside the month (e.g. "day 30" in
February) was previously counted as parsed and no longer is. For well-formed Kyoto files
— every file this audit has ever read — the figure is identical. Missing-day accounting
was already bounded pre-repair and is unchanged on the full-year path.

**Deliberately NOT run, per the ruling's scope:** the fixture ladder (its completion
additionally needs the two student fixture-manifest freezes and, for stages 00–02, the
owner's `acquisition.window_*` transcription — the separate prerequisites §6 names);
Kaggle; anything producing governed evidence. The repaired `04` window path is therefore
proven at function level and remains ladder-unobserved on this clone.

**No commit was made by this pass.** The student's eventual commit cites
`CR-2026-09-13-04-FIXTURE-WINDOW`.
