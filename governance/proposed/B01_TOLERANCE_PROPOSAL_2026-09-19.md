# Proposed predeclared tolerance for the B-01 IRI-2016 validation comparison (R-59 area 7)

**Status: APPROVED 2026-09-20T12:27:01Z, recorded as `D-50` in `evidence/DECISIONS.md`.**
`configs/experiment.yaml: benchmark_b01.validation_report.tolerance_tecu = 1.0` and
`tolerance_declared_at_utc = "2026-09-20T12:27:01Z"` are now frozen. This file is kept as the
derivation D-50 cites; no term below was changed by the approval. Revision 1 (2026-09-19)
derived its terms from documentation; revision 2 (this text) replaces every term with a
**measured** value from independent numerical checks on the pinned wheel and states what those
checks cannot establish. Nothing has been compared under the frozen tolerance yet: no official
value exists, and no adapter value for the eight cases has been computed or looked at.

**Not reused:** D-47's `8.0e-12 sfu` is the F10.7 recomputation tolerance — a floating-point
reproduction bound in sfu with a different purpose. This comparison is in TECU between two
independent executions of IRI-2016.

## 1. Evidence base (all under `evidence/b01_tolerance_basis_2026-09-20/`)

- **Environment.** The exact pinned wheel `iricore-1.8.0-cp310-manylinux_2_35_x86_64` installed
  `--require-hashes` into a CPython 3.10.21 environment on Linux x86-64 (WSL2); index files at
  the D-45 pinned SHA-256s; the Kaggle smoke-test value (2024-01-06 12 UT, ARUC) reproduced
  **bit-identically** (37.373754526924806 TECU) — `environment.json`. Diagnostic only; not a
  governed run and not the Kaggle B-01 environment.
- **Profile set.** 288 profiles: the three stations × 8 non-December days (2022-01-08, 03-14,
  04-15, 06-21, 08-05, 09-05, 09-23, 11-16) × 12 UT hours. **None of the eight R-59 cases is in
  the set**, so no case value was seen. Adapter TEC ranged 2.6–38.1 TECU.
- **Convergence check** (`b01_quadrature_convergence.py` → `…_results.json`): per profile, the
  adapter's own call; a converged reference (composite Simpson on a 0.1 km grid, 90–2000 km and
  100–2000 km); the 90–100 km and 65–90 km bands; and an emulation of IRI's own `iri_tec`
  midpoint scheme (`iritec.for` shipped in the wheel) for its three step options `istep` = 0/1/2,
  including its fixed 100 km start and its topside clamp.
- **Mismatch sensitivity** (`b01_mismatch_sensitivity.py` → `…_results.json`): the same 288
  profiles under each configuration mismatch the validation exists to catch.

## 2. Measured terms (adapter − X, TECU, n = 288)

| Term | Measured | Comment |
|---|---|---|
| Adapter − converged reference, 90–2000 km | **+0.004 … +0.062** (mean +0.025) | ≤ 0.19 % of TEC. Entirely `iricore`'s `_clean_ne_for_tec` step (its "spike" filter shifts every decreasing sample by one grid point; measured +0.004 … +0.061 on its own). The 0.5 km rectangle quadrature itself is converged to < 0.001 TECU |
| 90–100 km band (adapter includes it; `iri_tec` starts at 100 km whatever `tecLower` ≤ 100 is set to) | **0.0015 … 0.078** | daytime maximum; night ≈ 0.002. Revision 1's "≤ 0.02" was wrong by 4× |
| 65–90 km band (would be added only if the form's default `tecLower` = 65 mattered — it does not, see above) | 0.0002 … 0.006 | recorded for completeness |
| `iri_tec` istep = 2 ("best", 1/0.5 km) − reference from 100 km | −0.0011 … +0.0005 | the scheme is converged |
| `iri_tec` istep = 1 ("standard", 2/1/2.5/10/30 km) − reference from 100 km | −0.008 … +0.004 | converged to < 0.01 TECU |
| `iri_tec` istep = 0 ("fast", exponential topside approximation) − reference from 100 km | **+0.066 … +0.941** (mean +0.39) | 2.2 % of TEC on average, 2.6 % maximum; grows with TEC |
| **Adapter − official if the server uses istep 1 or 2** | **+0.006 … +0.140** (mean +0.05) | = band + clean step; adapter always HIGHER, ≤ 0.51 % of TEC |
| **Adapter − official if the server uses istep 0** | **−0.816 … −0.060** (mean −0.34) | adapter always LOWER; at the ≤ 38 TECU of this set; scales to ≈ −1.3 TECU at 50 TECU |
| Display rounding (one decimal expected) | ± 0.05 | to be confirmed from the first output header |
| IRI version in the wheel | 0 | IRI-2016 and IRI-2020 return bit-identical Ne under the standard switches in this wheel (oarr/Te differ); `version=16` is correct and not discriminating |
| Index inputs | 0 if the header's F10.7/Rz12/IG12 equal the pinned files' 2022 values; otherwise a documented discrepancy | checked from the header, never absorbed |

**Which `istep` the CCMC server uses is not known** and could not be established from the page
or its JavaScript. IRI's own driver `IRIT13` uses istep = 2; the "standard, recommended" option
is 1; the "fast" option 0 is documented as "uncertainty < 5 %". This is the one unquantified
assumption in the proposal and it is declared, not hidden.

## 3. Discriminating power (what a per-case bound can and cannot catch)

|adapter − variant| over the 288 profiles, for the mismatches the validation exists to detect:

| Mismatch (form set wrongly) | median | max | share > 1.0 | share > 0.5 |
|---|---|---|---|---|
| hmF2 AMTB (the form's DEFAULT) instead of Shubin-COSMIC | 0.07 | **0.45** | 0 % | 0 % |
| hmF2 from M3000F2 | 0.05 | 0.48 | 0 % | 0 % |
| foF2 CCIR instead of URSI-88 | 1.13 | 4.34 | 55 % | 70 % |
| B0 Bil-2000 instead of ABT-2009 | 0.24 | 2.67 | 13 % | 29 % |
| foF2 storm model off | 0.00 (quiet days) | 3.78 (storm days) | 16 % | 23 % |
| Topside IRI-2001-corr instead of NeQuick | 0.97 | 7.11 | 49 % | 57 % |
| Ceiling 1000 km instead of 2000 km | 0.72 | 1.79 | 31 % | 67 % |

Consequence: **no per-case tolerance in the plausible range (0.25–1.0 TECU) detects an hmF2-model
mismatch** — its effect is at most 0.45 TECU. That mismatch is prevented procedurally (Shubin set
on the form, screenshot retained) and is visible in the official output itself: output type 1
prints **hmF2**, and the adapter's IRI call returns the same quantity (`oarr[1]`). Recording the
official hmF2 beside the TEC value is therefore recommended as a diagnostic (no threshold; not part
of R-59's tolerance) so a wrong hmF2 option is caught by inspection rather than absorbed.
The other mismatch classes shift TEC by 1–7 TECU on at least half of the cases (the disturbed
daytime cases, 4 and 8, are where they are largest), so a 1.0 TECU bound catches them on the
majority of the eight and a 0.5 TECU bound on more; neither catches them on every quiet-night case.

## 4. Recommendation

**|adapter − official| ≤ 1.0 TECU for every one of the eight cases** (absolute, per case; the
report also records the mean and maximum signed difference). Status `passed` only if all eight hold.

Why 1.0 and not tighter:

- Under the two converged server schemes (istep 1 or 2) the expected difference is
  +0.006 … +0.19 TECU including display rounding — 1.0 leaves a ≥ 5× margin and any failure is
  then a real mismatch, not quadrature.
- Under the fast scheme (istep 0) the expected difference is −2.2 % of TEC on average (−2.6 %
  max): within 1.0 TECU for every profile up to 38 TECU, and up to ≈ −1.3 TECU at 50 TECU. A
  0.5 TECU bound would fail most daytime cases under that scheme for a reason that has nothing
  to do with the adapter; 1.0 fails at most the one or two highest daytime cases.
- 1.0 remains well below the 1–7 TECU of the mismatch classes that matter (§3), except the hmF2
  option, which no tolerance catches and which is handled procedurally.

Limitations stated with the recommendation:

1. The server's `istep` is unknown. **Predeclared signature, so it is not reasoned post hoc:**
   with istep 1/2 every difference is expected small and positive (adapter higher); with istep 0
   every difference is expected negative and roughly proportional to TEC (−2 … −3 %). If the
   report fails on one or two high-TEC daytime cases with the adapter LOWER by 1.0–1.3 TECU
   while every other case is negative-signed and in tolerance, that is the istep-0 signature.
   The report is still written `failed` and generation stays blocked (R-59); the predeclared
   follow-up is the official Fortran reference build run with a **known** `istep` and the pinned
   index files (collection sheet §7, alternative 2) — never a widened tolerance and never a
   switched implementation (TE §18.2).
2. The 288-profile set spans the three stations, four seasons, quiet and disturbed days and all
   hours, but it is not the eight cases; the measured bounds are empirical maxima over that set,
   not proofs. The eight cases' TEC is expected within the set's range (2.6–38 TECU) except
   possibly cases 4 and 8 (disturbed daytime), for which the istep-0 term is extrapolated.
3. Index inputs are not covered by the tolerance at all: a server-side revision of the 2022
   F10.7/Rz12/IG12 values is detected from the recorded header lines and reported as a
   discrepancy.
4. `_clean_ne_for_tec` is part of the pinned adapter and stays as is; its +0.004 … +0.06 TECU is a
   known, recorded bias of the implementation, not something to correct for after the fact.

## 5. What the tolerance does not do

It does not absorb a scientific mismatch. If any case fails, the report is written with
`status: failed`, generation stays blocked, and the cause is investigated from the recorded
headers (server index version, option mapping, hmF2 column) — the implementation is never
switched and the tolerance never widened after the fact (R-59; TE §18.2).

## 6. Decision — resolved

**1.0 TECU absolute per case: APPROVED** (D-50, 2026-09-20T12:27:01Z — the approval instant is
the declaration time recorded in `experiment.yaml`).

**hmF2 diagnostic column: APPROVED 2026-09-20 (D-50 addendum) and implemented.** The samples
carry `official_interface_hmf2_km` (parsed from the output's `Peak Heights/km: hmF2=` line) and
the report records `adapter_hmf2_km` and `hmf2_diff_km_diagnostic_no_threshold` per case. It
never enters the tolerance verdict. Nothing about the frozen 1.0 TECU changed.
