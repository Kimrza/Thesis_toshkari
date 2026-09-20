# Proposed predeclared tolerance for the B-01 IRI-2016 validation comparison (R-59 area 7)

**Status:** PROPOSAL, awaiting the project decision owner's approval. Nothing has been
compared: no official reference value has been retrieved (access refused 2026-09-19), no
adapter value has been computed for the eight cases, and `configs/experiment.yaml:
benchmark_b01.validation_report.tolerance_tecu` / `tolerance_declared_at_utc` stay
`TBD — freeze gate` until the owner approves. On approval the value and the **actual**
approval instant are written there; the declaration is never backdated, and the report
builder refuses a declaration that does not precede the comparison (R-59 limb 2).

**Not reused:** D-47's `8.0e-12 sfu` is the F10.7 recomputation tolerance — a floating-point
reproduction bound in sfu with a different purpose. This comparison is in TECU between two
independent executions of IRI-2016.

## Proposed value

**|adapter − official| ≤ 1.0 TECU for every one of the eight cases** (absolute, per case; the
report also records the mean and maximum difference). Status `passed` only if all eight hold.

## Derivation (each term bounded from documented facts, none from the data)

| Term | Bound | Source |
|---|---|---|
| Reference display precision | ≤ 0.05 TECU | CCMC output prints TEC to one decimal (to be confirmed from the first header; if two decimals, the term shrinks) |
| Integration scheme | ≤ ~1 % of TEC ≈ ≤ 0.5 TECU at the ≤ 50 TECU expected for these mid-latitude 2022 cases | IRI's `iri_tec` (`iritec.for`, shipped in the wheel) integrates segment-wise with 1–30 km steps (istep = 1 standard; istep = 0 documented "uncertainty < 5 %"); the adapter sums Ne × 0.5 km over 90–2000 km (`iricore.tec._integrate_ne`). Two different quadratures of the same profile. |
| Lower bound | ≤ 0.02 TECU | form `tecLower` set to 90 km to match `hbot_km`; `iri_tec` starts its first segment at 100 km, so at most 90–100 km of D-region density (≈ 10^10 m^-3 daytime) separates the two |
| Upper bound, version, switches | 0 by construction | `tecUpper` 2000 = `htop_km`; IRI-2016 selected on both; every optional set to the IRI-2016 standard switch set the adapter uses (`hmF2` Shubin-COSMIC, NeQuick, URSI, storm on, ABT-2009, …) — see the collection sheet |
| Index inputs | 0 if the server's index files carry the same 2022 values; otherwise a documented discrepancy, not tolerance | pinned 1.8.0 files = 2024-06 files on every 2022 row/month (`index_comparison_report.json`); the output header's F10.7/Rz12/IG12 lines are recorded per case to detect a server-side revision |

Sum of the bounded terms ≈ 0.6 TECU; 1.0 TECU leaves margin for the quadrature term at
the higher end of the expected range. It stays **well below** the effect of a configuration
mismatch this validation exists to catch: a different hmF2 model, topside option, IRI
version, altitude ceiling or index input shifts TEC by several TECU at these levels.

## What the tolerance does not do

- It does not absorb a scientific mismatch. If any case fails, the report is written with
  `status: failed`, generation stays blocked, and the cause is investigated from the recorded
  headers (server index version, option mapping) — the implementation is never switched or
  the tolerance widened after the fact (R-59; TE §18.2).
- If the official interface proves not meaningfully comparable (e.g. its index files carry
  revised 2022 values it cannot be told to ignore), the R-59-permitted alternative is a
  comparison against the official IRI-2016 **Fortran reference build** run with the pinned
  index files (same source, `iri2016` distribution), which the same report schema accepts
  as `official_interface_value` with the source recorded.

## Decision requested

Approve **1.0 TECU** (or state another value) — the approval message's own timestamp is the
declaration time recorded in `experiment.yaml`.
