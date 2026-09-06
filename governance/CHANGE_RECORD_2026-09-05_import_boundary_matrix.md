# Change Record — DRAFT: the December-audit import boundary's three matrix edits

**Record** `CHANGE_RECORD_2026-09-05_import_boundary_matrix` · **Status: DRAFT — NOT
APPLIED.** `component-dependency.md` is **not edited** by this record's drafting; the
project decision owner's approval at the `code-generation` gate is what applies it.
**Drafted by** stage 3.5 (`inventory-and-registry`, Bolt 1), executing § SD-I-01 of
`construction/inventory-and-registry/nfr-design/security-design.md`, which records the
change as **owed, not written** — this draft is the owed record.

## What the record changes, and why

SEC-I-01 limb 2 requires the December-audit code path to import no module under
`src/models/` or `src/evaluation/`, directly or transitively. The approved
`inception/application-design/component-dependency.md` currently contradicts that rule in
one place and is silent on it in two, so the boundary now enforced by
`tests/test_import_boundary.py` (Limb A: package-wide direct-import check over
`src/data/*` plus `scripts/01_inventory_and_registry.py`; Limb B: transitive closure from
the audit entry point) needs the matrix brought into agreement. Three edits, the largest
deviation listed **first**:

| # | Edit to `component-dependency.md` | Deviation class |
|---|---|---|
| 1 | **`scripts/*` (all others) row: a named carve-out withdrawing the affirmative `models: yes`, `evaluation: yes` grant for `01_inventory_and_registry.py`** | **Withdraws a permission the matrix explicitly gives.** Larger than edits 2 and 3: promoting an absence records an obligation the matrix did not have, while this contradicts an affirmative grant — the edit a reviewer of this record should look at hardest, named first for that reason (adversarial finding 3, 2026-09-01) |
| 2 | `src/data` → `models`: **`—` → `X`** | Promotes an **absent** edge to a **forbidden** one. The matrix's own words: a forbidden edge needs a test and an absent one does not — the test now exists (`tests/test_import_boundary.py`) |
| 3 | `src/data` → `evaluation`: **`—` → `X`** | Same class as edit 2 |

**What the boundary does NOT constrain:** the audit's right to run. Vision §8.3 makes the
performance-blind coverage and regime audit a precondition of G-05; this boundary
constrains what the audit may import, never whether it may run.

**Assumption carried from DISC-I-1:** no approved component row owns the audit's two
output artifacts, and Limb A binds `scripts/01_inventory_and_registry.py` on the
assumption that this is where the audit lives (it is, as built at 3.5). If a later stage
relocates the audit, Limb A's constrained set and edit 1's carve-out move with it.

## Gate-routed rulings restated (context, not edits of this record)

1. **W-6's two-class wording (SD-I-04, routed to the gate 2026-09-01/02).** The approved
   `business-logic-model.md` W-6 reads *"for each artifact: `acquisition`'s named
   accessor"* with no restricted/ordinary distinction — unbuildable as read, since eleven
   of the twelve declared months are ordinary paths `open_restricted` refuses by
   contract. The ruling owed: **either** W-6's wording is amended by change record to
   carry the two-class RECORD-DATE routing (as built: residency the expected consequence
   of the class, never its definition; any disagreement a stop-and-report naming the
   file), **or** this stage's narrowing stands recorded in the gate record alone — in
   which case a builder reading only the approved W-6 still gets the unbuildable
   instruction, a live cost the human chooses knowingly (terminal finding 11).
2. **FR-P1-02-8's replacement acceptance row.** `TA-29` is withdrawn (it is a row
   `requirements.md` lists under "Not applicable in Phase 1 — Phase 2 by definition").
   The mechanism built at 3.5 — four separately named prohibition results asserted
   present before G-P1A (`assert_prohibition_results`) — is a mechanism, **not** an
   acceptance row; the replacement §19 row is stage 3.2's and change control's, and
   nothing in this Bolt claims FR-P1-02-8 covered.
3. **The `SchemaError` extension of Q1 (receipted 2026-09-05, Q1 = A).** Q2 of
   `nfr-design` was answered on a two-item scope; the set difference derived at
   nfr-design was three (`InventoryError`, `AuditScopeError`, `SchemaError`). The owner's
   receipted Q1 = A ruling at the 3.5 plan gate disposes `SchemaError` **identically** to
   the other two: declared in `src/data/config.py`, deriving from `IntegrityError`,
   added to `__all__`, riding R-01's any-future clause, not an enumeration entry. Applied
   at 3.5 as ruled; recorded here as the ruling's context.

## Decisions touched

The eventual governed commit for this Bolt cites **D-12** (the ≥90% hourly threshold the
G-P1A record judges against), **D-2** (the ≥95% day / 31-31 December threshold and its
post-hoc disclosure, now carried verbatim on the record by
`src/data/inventory.py::D2_DISCLOSURE`), and **D-15** (the restricted-root custody the
two-class routing's residency consequence rests on).

## Standing constraints restated

**No governed commit is made before this record exists** (it now does; the commit is the
student's act, not the agent's). **BLK-07's authorization limb is open** — the audit
entry point refuses naming BLK-07 and no run touches calendar 2022-12. **No scientific
value was entered**: coordinates, cell rule and IGRF stay `TBD — freeze gate` (Q2 = A),
and the D-12/D-2 thresholds are read from `configs/data.yaml`'s (not yet transcribed)
`gp1a` block with a TE 18.3 stop-and-report when absent — never inlined.
