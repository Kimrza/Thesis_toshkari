# Team Allocation — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.8 (`delivery-planning`), intent `260813-tec-hourly-forecast`.

## Sources

- `bolt-plan.md` — the twelve Bolts this document assigns.
- `../units-generation/unit-of-work.md` — unit ownership, deployment class, the blocker register.
- `../units-generation/unit-of-work-dependency.md` — the 23 edges and the one independent pair, which is why no batch assignment is needed.
- `../units-generation/unit-of-work-story-map.md` — the acceptance rows each unit owns as primary and supports on, which is where the supporting-role column below comes from.
- `../application-design/components.md` — the six `src/` packages whose module ownership the assignments follow.
- `../requirements-analysis/requirements.md` — § Constraints (single-author codebase, supervisor signs at freeze gates), § Open supervisor gates.
- `../practices-discovery/team-practices.md` — § Way of Working, which records the single-author reality this allocation reflects.
- **Absent by scope design:** `stories` (`../user-stories/stories.md`) and `mockups` (`../refined-mockups/`) — stages 2.4, 1.6 and 2.5 are `SKIP`. Neither would have changed an allocation here, since no Bolt has a user-facing surface or a story-derived owner.

## Terms used here

A **Bolt** is one build pass over a piece of the work, ending in something that
runs. A **mob** is a small cross-functional group working together on the same
thing at the same time; on this project no mob exists, for the reason given
immediately below. A **Program Board** is the artifact a multi-team delivery uses
to show which team owns which increment and where the cross-team dependencies
fall — it is the multi-team form of this document, and it does not apply here.

## There is one human and one AI implementer

Stage 1.5 (`team-formation`) is **`SKIP`** in the `research-pipeline-governed`
scope, so no team composition exists to reference. That is not a gap to be
filled: `requirements.md` § Constraints records the reality directly — this is a
single-author thesis codebase, and the supervisor signs at named freeze gates
rather than reviewing merges.

So the allocation is short, and stating it fully is more useful than dressing it
up:

- **Every Bolt is implemented by `aidlc-developer-agent`.** That is the framework
  default when team formation is skipped, and it matches the project: there are
  no teams to balance, no mob to compose, no cognitive-load split to make.
- **The student (Kimia Rezaei) is the project decision owner**, and holds every
  decision the agent is barred from making — every `TBD — freeze gate` value,
  every scientific constant, every station or module-name selection.
- **The supervisor (Dr. Reza Saraf Shirazi) signs the freeze gates.** Seventeen
  gates govern this project; the ones this plan runs into are enumerated in
  `external-dependency-map.md`.
- **No Program Board applies.** With one implementer and one team, there is no
  cross-team dependency surface for one to describe.

Because there is one implementer and Bolts run strictly serially, **the
allocation adds no scheduling information beyond the Bolt order itself**. What it
*does* add is the second column below: which unit is on the hook when a Bolt's
acceptance evidence needs something another unit owns.

## Bolt-to-implementer assignment

| Bolt | Unit | Implementer | Decision owner for its blocked scope |
|---|---|---|---|
| 1 | `foundation` | `aidlc-developer-agent` | — (no open blocker) |
| 2 | `governance-guards` | `aidlc-developer-agent` | Project owner — BLK-06's canonical enumeration |
| 3 | `acquisition` | `aidlc-developer-agent` | Functional design authors BLK-07's routing contract; project owner approves |
| 4 | `inventory-and-registry` | `aidlc-developer-agent` | — (no open blocker) |
| 5 | `external-products` | `aidlc-developer-agent` | — (no open blocker) |
| 6 | `target-standardization` | `aidlc-developer-agent` | Supervisor — BLK-05's §12 tree amendment |
| 7 | `features-and-splits` | `aidlc-developer-agent` | Functional design authors BLK-04's transform contract; supervisor accepts the leakage evidence at G-04 and G-05 |
| 8 | `models-and-baselines` | `aidlc-developer-agent` | Functional design authors BLK-03's confirmatory-prediction contract |
| 9 | `evaluation-and-comparison` | `aidlc-developer-agent` | Inherited only — BLK-03 ↓, BLK-04 ↓ |
| 10 | `statistical-inference` | `aidlc-developer-agent` | Inherited only — BLK-03 ↓, BLK-04 ↓ |
| 11 | `regimes-diagnostics-reporting` | `aidlc-developer-agent` | Inherited only — BLK-03 ↓, BLK-04 ↓ |
| 12 | `fixtures-and-reproducibility` | `aidlc-developer-agent` | Project owner under Q-31 — BLK-02's fixture station |

**↓** marks a blocker inherited through a consumed contract rather than owned.

## Cross-unit evidence obligations

A Bolt can close only when its own acceptance rows have evidence — but seven of
the acceptance rows in this plan need an artifact from a unit other than the one
that owns the row. Those are the places where a Bolt's completion depends on work
already done in an earlier Bolt, and they are recorded here so that dependency is
visible rather than discovered late.

| Acceptance row | Owned by (Bolt) | Also needs (Bolt) | What crosses |
|---|---|---|---|
| WS-10, TA-07 (IRI denial) | `features-and-splits` (7) | `governance-guards` (2), `external-products` (5) | The independent import-boundary check has no owning §12 module; the products being denied entry are built in Bolt 5 |
| WS-11, TA-08 (availability lags) | `features-and-splits` (7) | `external-products` (5) | The driver manifests the lag assertions are checked against |
| WS-18, TA-18 (locked-test guard) | `features-and-splits` (7) | `governance-guards` (2), `inventory-and-registry` (4), `evaluation-and-comparison` (9) | The guard is deliberately split: the access-log limb in Bolt 2, the execution limb in Bolt 7. The test exercises both and is owned by Bolt 7 — assigning it to Bolt 2 would close a dependency cycle |
| TA-11 (splits, embargo, transforms, masks) | `features-and-splits` (7) | `evaluation-and-comparison` (9) | `test_common_masks.py` is owned by Bolt 9 |
| TA-13, TA-26 (determinism, checkpoints) | `models-and-baselines` (8) | `foundation` (1), `fixtures-and-reproducibility` (12) | The seed utility and `test_determinism.py` are Bolt 1's; the both-platform serialization restore is Bolt 12's evidence |
| TA-15 (release provenance) | `foundation` (1) | `target-standardization` (6), `acquisition` (3) | Bolt 1 owns the release API; the artifacts it hashes come from Bolts 3 and 6 |
| TA-27 (phase boundary + protected hashes) | `governance-guards` (2) | `fixtures-and-reproducibility` (12) | The transition-manifest hash-diff test has no §12 module and needs frozen artifacts from every earlier unit |
| TA-19 (target uncertainty budget) | `target-standardization` (6) | `regimes-diagnostics-reporting` (11) | Production is Bolt 6's; reporting it adjacent to the primary result is Bolt 11's |

**One consequence worth stating.** TA-27's evidence and TA-13's both-platform
restore are not fully available until Bolt 12. Bolts 2 and 8 therefore close on
their own scope with those rows' evidence completed later — which is exactly why
`unit-of-work.md` records them on the supporting-unit column rather than as
dependency edges: the reverse edge would close a cycle.

## One acceptance row has no implementer, by design

**TA-24** requires the Technical Environment document to be checked against the
current Vision version and marked superseded if the Vision changed. That is
author and supervisor document control, not pipeline work, and no unit can
produce its evidence. It is recorded here as unassigned rather than attached to a
Bolt that does not own it.

## Assumptions & Open Questions

- **[assumption]** "Implementer" here means the agent that writes the code under
  the workflow's approval gates, not an autonomous builder. Every Bolt still
  passes through the stage gates, and §18.3 binds the agent to stop and report
  rather than choose a default while a P0 decision is unresolved.
- **[assumption]** The cross-unit evidence table above is derived from the
  Supporting column of the upstream acceptance mapping. It is a reading of which
  crossings actually gate a Bolt's closure, not a new assignment — no acceptance
  row changes owner here.
- **None** of the above adopts a reading on a supervisor-owned value.

## Reviewed on resume, 2026-08-22 — no correction needed

The propagation sweep that corrected six defects across the other three plan
artifacts was run over this file too, and found nothing to change. Recorded
because `governance/CHANGE_RECORD_PROCEDURE.md` step 3 is explicit that **"a sweep
that finds nothing records that it ran and found nothing. An unrecorded sweep
counts as no sweep."**

What was checked here:

- **Every count.** This file carries no untested-requirement count, no per-unit
  untested figure and no acceptance-row total, so the 40 → 36 correction and the
  `external-products` 5 → 4 correction have no site in it.
- **The TA-24 statement** above — that no unit can produce its evidence and it is
  recorded unassigned. Still accurate: TA-24 remains the one mapped acceptance row
  with no owning unit, unchanged by `CR-2026-08-22-LEAKAGE-TA`, which raised the
  owned rows from 39 to 43 out of 44 without touching TA-24.
- **Every Bolt-to-mob assignment.** All twelve Bolts remain assigned to
  `aidlc-developer-agent`; stage 1.5 (`team-formation`) is `SKIP` in this scope, so
  there is no team roster to have drifted against.
- **The two assumptions** above. Both still hold as written.

No superseded literal is preserved here, because nothing was superseded.
