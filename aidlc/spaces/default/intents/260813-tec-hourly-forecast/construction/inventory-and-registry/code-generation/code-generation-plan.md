# Code Generation Plan — `inventory-and-registry`

**Unit** `inventory-and-registry` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`
**Inputs**: `functional-design/` (W-1…W-9; R-44…R-53), `nfr-design/security-design.md` (SD-I-00…SD-I-08), `nfr-design/logical-components.md`, `unit-of-work.md` §4, `requirements.md`, `application-design/component-methods.md` (`Station`, `load_registry`, `assert_registry_resolved`). Answers: Q1=A (`SchemaError` identical disposition), Q2=A (single pre-G-P1A freeze event; TBD sentinels stay) — receipted.
**Authority**: G-09 signed (D-31). All four owned files are named in unit-of-work/§12/application design — **no naming amendment owed for this unit**.

## Ground rules binding every step

Same as prior units (3.11 target; in-place edits; no scientific constant in source; no credential values; two-tier errors; docstrings; ruff clean; negative control per hard rule; nothing discharged; smoke ≠ governed; **no git commit**). Plus this unit's own: **the December coverage/regime audit is NOT executed this run** (BLK-07 authorization limb open; no run touches calendar 2022-12); membership by record timestamps only, never path or filename; no §18.2 forbidden-choice value entered (coordinates, cell rule, IGRF all stay `TBD — freeze gate` per Q2=A); `assert_no_december_outside_restricted` is a standing regression check, never the audit's classifier.

## Recorded input — nfr-design review Minor (human ruling 2026-09-05)

One gate-routed, record-only Minor rides this unit's terminal READY review (per its own `## Review` trail: "0 Critical, 0 Major, 1 Minor (carried, gate-routed)"). No code step derives from it; quoted at the stage gate.

## Steps

- [x] **Step 1 — Exceptions in `src/data/config.py` (in place)** [Q1=A + nfr-design Q2=A; SD-I-02, SD-I-03]
  Declare `InventoryError`, `AuditScopeError`, `SchemaError` — `IntegrityError` subclasses, added to `__all__`, R-01 any-future clause (the "deliberately stopped asserting a count" sentence recorded); constructor contract inherited (resource + violated expectation; `AuditScopeError`'s resource is the declared scope, never a file path). Widen `RegistryError`'s docstring to name both registries, discriminated by `resource` (SD-I-03); every station-registry raise names its registry artifact or `station_id`. `StationRegistryError` NOT introduced.

- [x] **Step 2 — `src/data/inventory.py` (new; named in components.md — no amendment)** [FR-P1-02-1/2; SD-I-06; R-44; W-1]
  TE §5.1 nine-field entries; per-entry failure naming entry + missing field; FR-P1-01-6's verbatim acknowledgment notice as a **distinct field** from operational access notes; every written value routes through `acquisition.guard_egress` (hard dependency — exists since the acquisition pass); no credential/token/signed URL in any field.

- [x] **Step 3 — `src/data/registry.py` (new; named in components.md)** [FR-P1-02-1/2/7; SD-I-07; R-45…R-48; W-2/W-2a/W-3/W-4]
  `Station` with per-field provenance; `load_registry` + `assert_registry_resolved` per approved method signatures; refusals: missing §6.2 field, **defaulted rather than pinned `igrf_version`** (absent fails, never falls back — R-45), conflict resolved by averaging (equality against the NAMED source — R-47, with the coincidence-case negative control pinning the residual), migration diff asserting no value changed (R-48). Runtime refusal while coordinates/cell rule/IGRF are `TBD — freeze gate` (Q2=A) — code complete, values awaiting the one freeze event.

- [x] **Step 4 — Audit engine (importable, in `src/data/inventory.py` or a sibling section of it)** [FR-P1-02-3/4/5; SD-I-04, SD-I-05, SD-I-08; R-49…R-53; W-5/W-6]
  Check 1: up-front scope declaration vs governed reference set (twelve 2022 months, December 1–31, three cells, named artifact classes) — `AuditScopeError` **before any read**. Check 2: two-class routing decided by **RECORD DATE** (December-bearing → `acquisition`'s accessor → `open_restricted`, one durable row per artifact before the read, `purpose` coverage_audit/regime_audit, `performance_inspected=False`; ordinary → direct read, no row); **disagreement between record-date class and restricted-root residency = stop-and-report naming the file**; `locked_evaluation` purpose refused. Check 3: reconciliation 3a (access rows vs declared scope, per `run_id`) + 3b (all twelve declared months vs the report's per-month output; December included); mismatch fails. Interrupted audit → **no report** (all-or-nothing evidence); rows stand. Unique `run_id` per attempt (format: `audit-<UTCstamp>-<8charuuid>`, joined to the environment lock), per-`run_id` reconciliation. Every coverage figure carries `data07_caveat` from that month's `provenance_class`; absent field = **§18.3 stop-and-report**, never an uncaveated figure. R-51 G-P1A record: verdicts against BOTH D-12 and D-2, measured figure attributed per D-number, no soft margin, D-2's post-hoc disclosure travels on the record; R-52 four separately named prohibition results asserted present before G-P1A. Governed schema: self-contained report recording expected-schema digest + observed values (stdlib only — no new dependency; if a package proves necessary, STOP and report to 3.2, do not add one).

- [x] **Step 5 — `scripts/01_inventory_and_registry.py` (new)** [W-9; §12/§13.2 conventions]
  Position 01; `--config configs/`; `ensure_process_determinism` first; six-step entry; `assert_no_raw_fields` before first write; orchestrates Steps 2–4; registry rows via foundation's writer; `merge_coverage_year.py`'s merge/coverage logic **migrated in** — `sha256_of_file` usage consolidated onto `src/data/release.py`'s helper, the `retrieved_at_utc='recorded-at-call-time-by-the-runner'` placeholder **replaced** (guard-stamped `logged_at_utc` is the ordering evidence; DISC-I-2 discharged in the migrated copy) — the original script left untouched this run (its §12 retirement is a gate item). **The script can run only its non-December, non-registry paths today; the audit entry point refuses while BLK-07 stands** (explicit refusal naming BLK-07).

- [x] **Step 6 — Import boundary, two limbs (in `tests/`)** [SEC-I-01 limb 2; SD-I-01; NFR-PHASE-01 untouched]
  Limb A: direct-import check over every file in `src/data/*` + `scripts/01_inventory_and_registry.py` against `src/models/*`/`src/evaluation/*` (reuse `_imported_modules`; unparseable = fail). Limb B: transitive closure from the audit entry point over `src/` + `scripts/`; cycle terminates, never fails; **unresolved dynamic/computed import reported, never assumed clean**; closure containing models/evaluation fails. Negative controls: one injected direct import (Limb A), one injected two-hop chain through an unconstrained package (Limb B) — two separately named results. `test_phase_boundary.py`'s `PHASE1_PERMITTED_PACKAGES` behaviour untouched.

- [x] **Step 7 — `tests/test_station_registry.py` (new, §12-mandated) + audit tests** — every refusal in Steps 1–4 negative-controlled (nine-field failure names entry+field; averaged-conflict refused; coincidence residual pinned; short scope refused before read; ordinary path never logged; December-bearing-outside-root stop-and-report; interrupted audit leaves no report; caveat-less derived_only figure fails; unattributed threshold figure fails).

- [x] **Step 8 — Full-suite smoke + lint** — green under 3.11.9 (smoke only); ruff clean on touched files.

- [x] **Step 9 — Governance records + stop before commit (student acts)**
  DRAFT `governance/CHANGE_RECORD_2026-09-05_import_boundary_matrix.md`: the 3 `component-dependency.md` edits (two `src/data` cells `—`→`X`; named carve-out withdrawing the `scripts/*` `yes` grant for script 01 — listed FIRST as the largest deviation) — **the matrix itself is NOT edited**; owner approval at the gate applies it. Gate-routed rulings restated: W-6 two-class wording (amend upstream by change record vs narrowing recorded in gate record); FR-P1-02-8 replacement acceptance row (TA-29 withdrawn); the SchemaError Q1=A ruling recorded in the change-record draft's context. Commit cites D-12, D-2, D-15 as touched. **No governed commit before the records exist.**

## Out of scope

Executing the December audit (BLK-07), any coordinate/cell-rule/IGRF value (Q2=A single freeze event), editing `component-dependency.md` or W-6 upstream, widening `assert_no_december_outside_restricted`'s `.json`-only scan (governance-guards' change — recorded, not made), `merge_coverage_year.py` deletion/retirement, `StationRegistryError`, every acceptance-row discharge (WS-01, TA-04, TA-25 stay `Pending`; FR-P1-02-7/-8 stay rowless).
