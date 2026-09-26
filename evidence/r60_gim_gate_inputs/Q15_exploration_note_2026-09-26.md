# Q-15 exploration note — interpolation rule comparison (EXPLORATORY, not a freeze)

Dated 2026-09-26. Informs the Student's Q-15 freeze act in
`governance/Q15_DECISION_OPTIONS_2026-09-26_gim_interpolation.md`; decides
nothing by itself. No model prediction, no model-vs-GIM skill score, and no
December data entered this comparison anywhere — the worked numbers below
all come from the single January–November file
`evidence/gim_code_final_2022/codg1000.22i.Z` (day-of-year 100, 2022-04-10).
The `[Answer]:` field in the decision document was not touched, and no
`configs/` file was edited.

## The three candidate rules, mathematically

CODE final GIM ships VTEC on a fixed lat/lon grid (2.5°×5°, this dataset)
at fixed hourly epochs. Every rule below answers the same question — what
VTEC value does the grid imply at an arbitrary station coordinate and
arbitrary scored epoch — differently.

**A) Nearest grid point, nearest map epoch.** Snap the target coordinate to
its closest grid node and the target time to its closest map epoch; read
that one stored value. No interpolation at all.
- *Boundary behavior*: at the poles (lat=±87.5° is the first/last row) or
  the date line (lon=180°=-180°, the grid is periodic there per the header's
  own LON1/LON2 = -180.0/180.0), nearest-point lookup is trivial — no wrap
  logic needed since you're just picking the single closest stored node.
- *Missing-data behavior*: IONEX uses `9999` as a sentinel for "no value" in
  0.1 TECU units (stated in-file: "TEC/RMS values in 0.1 TECU; 9999, if no
  value available"). A pure nearest-lookup can return that sentinel
  untranslated if the nearest node happens to be a gap — the rule as stated
  needs an explicit sentinel check bolted on, which none of the three
  options' descriptions mention needing separately from the others (the
  9999 check is orthogonal to which interpolation rule is chosen, but rule
  A returns it raw and unmasked far more often than B or C, since it never
  looks at three neighbors that could carry real data instead).

**B) Bilinear spatial + linear temporal.** Standard four-corner bilinear
interpolation in (lat, lon) at each of the two bracketing map epochs,
followed by linear interpolation in time between the two resulting values.
- *Boundary behavior*: works cleanly in the grid interior. At the
  poles (lat outside [-87.5, 87.5] isn't reachable for any real station
  coordinate on Earth, so not a live concern here) and at the date-line
  wrap (lon bracket spanning -180/180), the longitude bracket needs modular
  arithmetic (`lon_hi = lon_lo + dlon`, wrapped mod 360) — a real
  implementation detail, not exercised by this note's worked example since
  none of ARUC/BSHM/NICO sit near ±180° longitude.
- *Missing-data behavior*: any of the four corner values being the `9999`
  sentinel poisons the whole bilinear result unless masked before
  averaging — same caveat as A, but now four cells can carry the sentinel
  instead of one.
- Ignores that CODE's GIM is generated in a solar-geomagnetic (sun-fixed)
  reference frame (stated in the file's own header DESCRIPTION block), so
  linearly blending two maps that are really rotated relative to each other
  in Earth-fixed coordinates introduces a systematic bias, worst at
  local dawn/dusk gradients.

**C) Bilinear on consecutive rotated maps (IONEX spec's own method,
Schaer et al. 1998).** Same bilinear spatial step as B, but each of the two
bracketing maps first has its effective longitude shifted by the Earth's
rotation over the elapsed time to/from the target epoch (15°/hour), before
the corner lookup. Temporal blend is then linear as in B.
- *Boundary behavior*: same date-line wrap consideration as B, now applied
  twice (once per map, at each map's own shifted longitude) — one extra
  wrap-check, not a qualitatively new problem.
- *Missing-data behavior*: identical sentinel-masking need as B; the
  rotated lookup can hit a different (still potentially missing) grid cell
  than the unrotated one would have, but that's a difference in *which*
  cells might be missing, not a new missing-data mechanism.
- This is the method the IONEX format's own documentation and CODE's
  header text imply as the intended consumption pattern, since the product
  explicitly states it is generated sun-fixed.

## Measured rule-vs-rule difference (one worked point)

Full arithmetic in `R60_handcheck_2026-09-26.md`. At station BSHM
(32.778987°N, 35.022987°E), 2022-04-10 00:20 UTC:

| Rule | Value (TECU) |
|---|---|
| A (nearest) | 18.600 |
| B (bilinear, no rotation) | 18.333 |
| C (rotated bilinear) | 18.262 |

B vs C differ by 0.071 TECU (~0.4% of the ~18 TECU value here) — small at
this instant. A vs C differ by 0.338 TECU (~1.9%) — meaningfully larger,
consistent with A being "a deliberately crude bound" per the decision
document's own framing.

**This is a single point, a single station, a single 20-minute offset into
one map interval, on one day out of 334 eligible days.** It is not a claim
about the typical or worst-case B-vs-C gap across ARUC/BSHM/NICO or across
seasons — the decision document's own recommendation already anticipates
that a fuller sweep might show B and C "differ negligibly," and this one
point is consistent with that possibility without establishing it. A
systematic multi-day, multi-station sweep is exactly the kind of
"exploration on the internet-connected system" the runbook anticipates as
future work once a lightweight, non-comparator IONEX reader exists in this
environment — not undertaken here beyond this one worked instant, given
this session's scope (acquisition + one verifiable hand-check + this
qualitative comparison were the requested deliverables, not a full-year
sensitivity study).

## What was deliberately NOT done here

- No model prediction of any kind was computed or referenced.
- No model-vs-GIM skill score was computed.
- No December file was opened, decompressed, or read for its TEC values.
- No `configs/` file was edited; no scientific constant was written to disk
  outside this evidence directory.
- The `[Answer]:` field in
  `governance/Q15_DECISION_OPTIONS_2026-09-26_gim_interpolation.md` was not
  filled — that remains the Student's act.

## Non-binding observation for the Q-15 D-number's rationale (not a recommendation from this note)

The decision document's own recommendation (Option C) is not contradicted
by anything measured here. If a fuller sweep (not run in this session)
confirms B and C differ negligibly across all three stations and the full
January–November window, that measured fact — per the decision document's
own text — belongs in the D-number's rationale as a *disclosed sensitivity*,
with the freeze still naming C as the citable, IONEX-spec-standard method.
