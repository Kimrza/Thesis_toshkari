# Code Generation Questions — `external-products`

**Unit** `external-products` (Bolt 1) · **Kind** `library` · **Stage** `code-generation`

One genuine gap needs a ruling; everything else is design-fixed or already
routed to the stage gate by nfr-design (the `tests/*` allowlist blanket-row
discrepancy; the foundation-preflight skip-reason dependency; the flipped
provenance default's cross-unit enlargement; `DriverError` deliberately NOT
declared this run — its raise-conditions are self-contradictory upstream
(carried Finding 9) and the design says the declaration waits on that
reconciliation). The IRI benchmark and GIM comparator are NOT generated this
run (R-59 validation not run; Q-15 interpolation rule UNSET; both refusals are
the designed behaviour).

**Recorded input (human ruling, 2026-09-05)**: this unit's terminal READY
nfr-design review rides on an iteration-2 pass after seven reviewer passes and
two owner-directed redos; record-only Minors listed in the plan, per
`governance/RULING_2026-09-05_nfr-design_governance_dispositions.md`.

---

## Question 1
`BenchmarkError` and `ComparatorError` — two of the five missing exceptions
the nfr-design derivation found (Q2 there put only `ImportBoundaryError` +
`FeatureAvailabilityError` to you; those two are settled = declared in
`config.py`). Both are raised by this unit alone, nothing to reconcile, and
the design proposes the identical disposition, routed here for an explicit
yes/no rather than folded into an answer you were not shown. Declare both in
`src/data/config.py` (IntegrityError subclasses, `__all__`, R-01 any-future
clause, not enumeration entries)?

A) Yes — identical disposition for both
   > **Impact**: SD-E-04's benchmark-gate refusals and SD-E-05's comparator refusals become implementable with declared, catchable classes; consistent with the three prior rulings of this shape. R-01's enumeration unchanged.

B) No — defer both; refusals raise generic `IntegrityError`
   > **Impact**: Gate refusals become indistinguishable by type from every other integrity failure; a later ruling adds the classes and a rename sweep.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — same footing as the four exceptions you have already ruled on this Bolt; the only reason it is a question is the no-silent-widening rule. `DriverError` stays undeclared either way (contested upstream; not this run's to fix).

[Answer]: A

---

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Q1 = A — `BenchmarkError` and `ComparatorError` declared in `src/data/config.py` (IntegrityError subclasses, `__all__`, R-01 any-future clause, not enumeration entries). `ImportBoundaryError` + `FeatureAvailabilityError` likewise (design-decided at nfr-design Q2=A). `DriverError` NOT declared (contested upstream, carried Finding 9).
- Build set: `src/external/spaceweather.py` (driver builders — availability lags, trailing-81-day F10.7 proven as a shifted-input property, ≤3h carry-forward with injected-4h control, time-indexed one-value-per-epoch, grades never mixed, release-status fields, no backfill; `carry_forward_composition` TBD → `FeatureAvailabilityError` stop), `src/external/iri.py` (benchmark gate: refuses without passing pre-declared validation report, tolerance timestamp precedes comparison, field-by-field report assertion — generation stays BLOCKED, R-59 validation has not run), `src/external/gim.py` (comparator: refuses while Q-15 interpolation rule UNSET; hand-check timestamp ordering; map-to-map + spatial-mismatch statement emitted by the reporting path; no-tuning grep-class check; overlap-flag disclosure keyed to artifact existing), `scripts/04_build_external_products.py` (position 04; `audit_ec1_drivers.py` logic migrated in with the exit-code gap closed on the two-tier posture; every written value provenance-stamped + through `guard_egress`), `tests/test_iri_denial.py` (§12-mandated — ordered-switch containment check, skipped-never-passed with structured reason, complement-defined candidate set over `.py` + `.ipynb` cells, walk includes `__init__.py`/count subtracts, transitive; WS-10 negative control: injected `iri_*` field caught; injected import caught; absent provenance fails), driver/comparator tests, SD-E-07 byte-identical re-run refusal (acquisition's contract adopted).
- Governance: R-55 boundary-contract change record DRAFTED (one record, three modules); `tests/*` blanket-row discrepancy, foundation-preflight skip-reason dependency, and the provenance-default enlargement stay gate-routed; no IRI benchmark, no GIM comparator, no acceptance row claimed; no commit.

- Looks correct
- Request changes

[Answer]: Looks correct

---

## Plan Approval

The code-generation plan for `external-products` is at
`construction/external-products/code-generation/code-generation-plan.md` — 10
steps: 4 exceptions (1), spaceweather.py (2), iri.py gate (3), gim.py
refusals (4), provenance stamps + SD-E-07 (5), script 04 with
audit_ec1_drivers migrated + exit-code gap closed (6), test_iri_denial.py —
the largest open item closed (7), driver tests (8), smoke + lint (9),
governance records + stop (10).

- Approve Plan
- Request Changes

[Answer]: Approve Plan
