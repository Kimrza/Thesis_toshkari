# Q-15 decision options — GIM interpolation rule (Student-owned freeze)

Drafted 2026-09-26 for the Student's Q-15 freeze act. Q-15 is the `TBD — freeze gate`
interpolation rule `gim.generate_comparator` refuses on (R-60 obligation 1). The choice is
the Student's; adoption happens as a D-number in `evidence/DECISIONS.md`, never by an
implementer filling it (TE §18.2). Exploration on the internet-connected system may inform
the choice under the recorded guardrails: January–November 2022 only, no model-vs-GIM
performance in the loop, chosen rule enters `configs/` only through the freeze act.

Context: CODE final GIM ships as IONEX maps on a 2.5° (lat) × 5° (lon) grid at fixed
epochs; the comparator needs VTEC at each station coordinate at each scored hour. The
interpolation rule is the ONE way grid values become station values — a methodological
constant of the comparison, frozen before any comparator is generated.

## Question 1
Which interpolation rule maps CODE GIM grid values to a station coordinate at a scored
epoch?

A) Nearest grid point, nearest map epoch
   > **Impact**: Trivial to implement and hand-check; introduces up to ~1.25°/2.5° of
   > spatial and up to half a map interval of temporal mismatch, which enters the
   > comparison as structured comparator error at all three stations. Defensible only as
   > a deliberately crude bound; weakens the evaluation-time comparison it exists for.

B) Bilinear spatial interpolation + linear temporal interpolation between the two
   bracketing maps
   > **Impact**: Standard, simple, fully hand-checkable (two bilinear terms + one linear
   > blend). Ignores the ionosphere's sun-fixed rotation between map epochs, which biases
   > temporal blending most at local dawn/dusk gradients — a known, documented, modest
   > error term at mid-latitudes.

C) Bilinear spatial interpolation on CONSECUTIVE ROTATED MAPS (each bracketing map
   rotated about the Earth's axis to the target epoch before the temporal blend) — the
   IONEX specification's recommended method (Schaer et al., IONEX 1.0, 1998)
   > **Impact**: The literature-standard consumption of IONEX GIMs and what CODE's own
   > products anticipate; accounts for the sun-fixed pattern between epochs. Slightly
   > more code than B and the hand-check needs one extra step (the longitude shift),
   > but the R-60 hand-check gate exists precisely to verify that step once, on paper.

D) Other (please specify)
   > **Impact**: Depends on your specific choice. Any rule outside the IONEX-documented
   > family will need its own citation and a fuller hand-check to survive review.

> **💡 Recommendation**: Option C — it is the IONEX specification's own recommended
> method and the standard in the TEC literature, so the comparator inherits a citable,
> reviewer-defensible convention rather than a project-local choice; its one extra
> hand-check step is exactly what the R-60 hand-check gate is designed to absorb. If
> exploration on the internet system shows C and B differ negligibly at ARUC/BSHM/NICO
> for January–November 2022, that measured fact belongs in the D-number's rationale —
> but the freeze should still name C, with B as the disclosed sensitivity, not the
> reverse.

[Answer]:
