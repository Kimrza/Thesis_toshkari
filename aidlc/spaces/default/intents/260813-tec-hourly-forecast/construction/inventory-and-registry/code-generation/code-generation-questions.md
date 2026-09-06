# Code Generation Questions — `inventory-and-registry`

**Unit** `inventory-and-registry` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`

Two genuine gaps need a human ruling before code exists; everything else is
design-fixed (two-limb import boundary with its 3-edit change record owed;
two-class record-date audit routing with stop-and-report; per-`run_id`
reconciliation; `RegistryError` resource discrimination; R-44…R-53 refusals;
IGRF version stays `TBD — freeze gate`). The audit itself is NOT executed this
run — BLK-07's authorization limb is open and no run may touch calendar
2022-12.

**Recorded input (human ruling, 2026-09-05)**: this unit's terminal READY
nfr-design review carries one gate-routed Minor (0 Critical, 0 Major, 1 Minor
— carried, gate-routed per the artifact's own `## Review` trail); listed in
the plan as record-only, per
`governance/RULING_2026-09-05_nfr-design_governance_dispositions.md`.

---

## Question 1
`SchemaError` — the third missing exception Q2 (nfr-design) never showed you.
W-5 declares `RAISES SchemaError`; set-differencing W-1…W-6's RAISES lines
against `config.py`'s `__all__` yields {InventoryError, AuditScopeError,
SchemaError}, and your Q2=A ruling covered only the first two. The design
proposes treating it identically and routes the decision here rather than
widening your answer silently. Declare `SchemaError` in `src/data/config.py`
(derives from `IntegrityError`, added to `__all__`, riding R-01's any-future
clause, not claimed as an enumeration entry)?

A) Yes — identical disposition to InventoryError/AuditScopeError
   > **Impact**: W-5's schema validation becomes implementable this run with one declared, catchable exception; consistent with the PartitionError declaration-site precedent. R-01's enumeration is unchanged (any-future clause).

B) No — defer schema validation; W-5's validator raises generic `IntegrityError` for now
   > **Impact**: Schema failures become indistinguishable by type from every other integrity failure; a later ruling adds the class and a rename sweep. Nothing else blocks.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — one unit raises it, nothing needs reconciling, and the design already argued the disposition on its face; the only reason it is a question is that applying your Q2 answer to an item you were not shown would be the exact widening this project corrected once already.

[Answer]: A

## Question 2
Station coordinates and the coordinate-to-cell rule are §18.2 forbidden
choices (coordinates: Student; cell rule: Student + Supervisor) self-labelled
PROVISIONAL in the notebook. Team practice: frozen as a D-number FIRST, only
then moved into `configs/data.yaml` + `src/data/registry.py`, validated
against official IGS site logs before treated as final. Separately, the IGRF
version is also `TBD — freeze gate` — and R-45 means the registry cannot
BUILD until that is frozen regardless. Freeze the coordinates/cell rule now,
or defer?

A) Defer — build all registry code now; every frozen-pending value stays `TBD — freeze gate` in `data.yaml`; the registry build refuses at runtime (R-45/R-46 pattern) until one freeze event (coordinates + cell rule + IGRF, pre-G-P1A) lands the values under D-numbers
   > **Impact**: No §18.2 value is decided by an agent or piecemeal; the registry stays runtime-refused (which IGRF's open freeze forces anyway). One later freeze event unblocks it whole. The code and its negative controls are complete either way.

B) Freeze coordinates + cell rule now under the recorded student/supervisor authority equivalence (D-1 addendum), values transcribed from notebook cell 4, IGS-site-log validation recorded as owed before "final"; IGRF still open
   > **Impact**: Values enter `data.yaml` under a D-number today, but the registry still cannot build until IGRF freezes — so this buys no runnable capability now, and it commits scientific values whose higher-ranked source (IGS site-log PDFs) has not been checked (D-1's open limitation).

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — freezing now yields no runnable registry (IGRF blocks it regardless) while committing values ahead of their best evidence; one deliberate freeze event later is strictly cleaner. Risk stated: G-P1A's schedule then depends on that freeze event happening before the December coverage audit runs.

[Answer]: A

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Q1 = A — `SchemaError` declared in `src/data/config.py` beside `InventoryError` and `AuditScopeError` (all three: `IntegrityError` subclasses, in `__all__`, riding R-01's any-future clause, not enumeration entries; the any-future sentence recorded in `config.py` per the design).
- Q2 = A — coordinates + cell rule + IGRF defer to ONE freeze event pre-G-P1A; `data.yaml` keeps `TBD — freeze gate` sentinels; all registry code built now with R-45/R-46 runtime refusals until the freeze.
- Build set: `src/data/inventory.py` (nine-field entries, per-entry failure, verbatim-notice field distinct from access notes, all values through acquisition's `guard_egress`), `src/data/registry.py` (`Station` per-field provenance, named-source equality R-47, migration diff R-48, refusals), `scripts/01_inventory_and_registry.py` (audit: scope declaration → `AuditScopeError` before first read; two-class RECORD-DATE routing with stop-and-report on residency disagreement; reconciliations 3a per-`run_id` + 3b all twelve months; `data07_caveat` from `provenance_class` else §18.3 stop; unique `run_id` joined to the environment lock; `merge_coverage_year.py` logic migrated in with the `retrieved_at_utc` placeholder replaced), `tests/test_station_registry.py` + audit tests. Two-limb import boundary (Limb A direct-import check over `src/data/*` + the script; Limb B transitive closure from the audit entry point; unparseable = fail; unresolved dynamic import reported).
- Governance: change record DRAFTED for the 3 `component-dependency.md` edits (two `—`→`X` promotions + the `scripts/*` carve-out) — the matrix itself is NOT edited; W-6 two-class wording ruling stays routed to the stage gate; RegistryError discriminated by `resource`, `config.py` docstring widened; `StationRegistryError` NOT introduced.
- The December audit is NOT executed (BLK-07 authorization limb open); no acceptance row claimed; no commit.

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Plan Approval

The code-generation plan for `inventory-and-registry` is at
`construction/inventory-and-registry/code-generation/code-generation-plan.md`
— 9 steps: three exceptions + RegistryError docstring in config.py (1),
inventory.py (2), registry.py with TBD runtime refusals (3), audit engine
(record-date two-class routing, per-run_id reconciliation, data07_caveat stop,
G-P1A record shape) (4), script 01 with merge_coverage_year logic migrated in
and the placeholder replaced (5), two-limb import boundary with injected
negative controls (6), test_station_registry.py + audit tests (7), smoke +
lint (8), governance records + stop — matrix change record DRAFTED, matrix
untouched, no commit (9).

- Approve Plan
- Request Changes

[Answer]: Approve Plan
