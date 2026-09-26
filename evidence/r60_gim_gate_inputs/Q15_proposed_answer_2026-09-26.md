# Q-15 proposed `[Answer]:` and D-number text — FOR REVIEW, NOT ADOPTED

Prepared 2026-09-26. This is a proposal for the Student to adopt or reject.
Nothing here has been written into
`governance/Q15_DECISION_OPTIONS_2026-09-26_gim_interpolation.md`'s
`[Answer]:` field, and nothing has been written into `configs/`.

## Comparison table

| | A — nearest | B — bilinear + linear | C — bilinear on rotated maps |
|---|---|---|---|
| **Rule, plain language** | Snap to closest grid node and closest map epoch; read one stored value | Four-corner bilinear in (lat,lon) at each bracketing map, then linear blend in time | Same bilinear step, but each map's longitude is first shifted by Earth's rotation (15°/h) toward the target epoch before the lookup |
| **Scientific rationale** | None beyond "closest is a reasonable guess" | Standard numerical interpolation; ignores that CODE's GIM is generated in a sun-fixed frame | IONEX spec's own recommended consumption (Schaer et al. 1998); accounts for the sun-fixed generation frame CODE's own header documents |
| **Benefits** | Trivial to implement and hand-check | Simple, fully hand-checkable, industry-common | Literature-standard, citable, matches what CODE's product anticipates |
| **Drawbacks** | Up to ~1.25° spatial / half-map-interval temporal mismatch enters as structured comparator error | Systematic bias at local dawn/dusk gradients from ignoring frame rotation | Slightly more code; hand-check needs one extra step (longitude shift) |
| **Implementation cost** | Lowest — one nearest-index lookup | Low — two bilinear lookups + one linear blend | Low-Medium — two bilinear lookups on shifted coordinates + one linear blend |
| **Verification cost** | Trivial hand-check | One worked example, as delivered (`R60_handcheck_2026-09-26.md`) | Same hand-check plus the rotation arithmetic — the R-60 gate is explicitly designed to absorb this one extra step |
| **Boundary/missing-data behavior** | Trivial spatial lookup; `9999` sentinel returned raw far more often (only one cell consulted) | Needs longitude-wrap handling at ±180°; any of 4 corners being `9999` poisons the result unless masked | Same wrap/masking needs as B, applied at each map's shifted longitude — one extra wrap-check, not a new problem class |
| **Likely effect on hourly series** | Coarsest — visible step artifacts as target crosses grid cells/epochs | Smoother than A; small systematic dawn/dusk bias vs. C | Smoothest, spec-correct; removes the dawn/dusk bias B carries |

## Measured Jan–Nov evidence (exact figures, one worked point — not a full sweep)

From `Q15_exploration_note_2026-09-26.md` / `R60_handcheck_2026-09-26.md`, station BSHM,
2022-04-10 00:20 UTC, file `codg1000.22i.Z`:

- A = 18.600 TECU
- B = 18.333 TECU
- C = 18.262 TECU
- **B vs C: 0.071 TECU (~0.4%)** — small at this instant
- **A vs C: 0.338 TECU (~1.9%)** — meaningfully larger

This is one point on one day at one station — not a claim about typical or
worst-case magnitude across ARUC/BSHM/NICO or the full January–November
window. No model prediction and no December data entered this measurement.

## Recommendation

**Option C** (bilinear interpolation on rotated maps), for the reasons the
decision document itself already states: it is the IONEX specification's own
recommended method and the literature standard, so the comparator inherits a
citable, reviewer-defensible convention rather than a project-local choice.
The one worked point measured here is *consistent with* B and C differing
negligibly at this instant, which — per the decision document's own framing —
belongs in the D-number's rationale as a disclosed sensitivity, not as a
reason to freeze B instead.

**When B would be preferable instead:** if implementation/verification time
is severely constrained (e.g., late in the timeline with no time to re-verify
the rotation arithmetic), or if a fuller multi-day/multi-station sweep (not
run in this session) later shows B and C differ negligibly across the whole
January–November window and all three stations — then B's simplicity becomes
a legitimate trade against C's fidelity, and the freeze could cite that
sweep. That sweep does not exist yet; this recommendation is not contingent
on it, only aware that it could change the calculus.

**When A would be preferable:** essentially never for the confirmatory
comparator itself — the "deliberately crude bound" framing means A is
defensible only as a diagnostic sanity check run alongside the real rule, not
as the frozen Q-15 choice.

## Proposed `[Answer]:` text (for the Student's own edit, not applied here)

```
[Answer]: C

Rationale: IONEX specification's own recommended method (Schaer et al. 1998);
literature-standard consumption of CODE final GIM, matching the sun-fixed
generation frame CODE's own file header documents. One worked hand-check
point (BSHM, 2022-04-10 00:20 UTC) shows B and C differing by ~0.4% (0.071
TECU) at that instant -- consistent with, but not proof of, a small
B-vs-C gap generally; this is disclosed as a sensitivity, not a reason to
prefer B. See evidence/r60_gim_gate_inputs/Q15_exploration_note_2026-09-26.md
and R60_handcheck_2026-09-26.md for the full worked evidence.
```

## Proposed D-number draft text (for `evidence/DECISIONS.md`, Student's act)

```
D-<next>: GIM interpolation rule (Q-15) frozen as bilinear spatial
interpolation on consecutive rotated maps (IONEX 1.0 spec, Schaer et al.
1998) -- Option C of governance/Q15_DECISION_OPTIONS_2026-09-26_gim_
interpolation.md. Basis: literature/spec standard, citable convention;
one worked hand-check point (BSHM, 2022-04-10 00:20 UTC, file
codg1000.22i.Z) measured B-vs-C difference of 0.071 TECU (~0.4%), disclosed
as a sensitivity finding, not the deciding factor. Exploration bounded to
January-November 2022 per the December-sealed rule; no model-vs-GIM score
entered the choice. Evidence: evidence/r60_gim_gate_inputs/
Q15_exploration_note_2026-09-26.md, R60_handcheck_2026-09-26.md.
```

Both blocks above are drafts only. Adopting either means the Student copies
the text (edited as they see fit) into the real files themselves — per this
project's own rule that a D-number is not real until the Student's own act
creates it, and per TE 18.2 that no implementer fills a Student-owned forbidden
choice by convenience.
