# B-01 — official IRI-2016 reference values: manual collection sheet (R-59 area 6)

Programmatic access to the official interface was refused on 2026-09-19 (HTTP 429 on every
run request after two schema probes, then connection resets — `evidence/iri2016_official_reference_2026-09-19/official_runs.json`).
The eight cases below were **selected before any retrieval** (`sample_selection.json`,
selected 2026-09-19T20:28:42Z) from the extremes of the audited definitive Kp record. Collect
them exactly as specified; do not replace a case because it looks awkward.

## Where

`https://kauai.ccmc.gsfc.nasa.gov/instantrun/iri` — CCMC Instant Run. Choose **IRI-2016** in
the version selector.

## Settings — identical for every case (these match the pinned `iricore` 1.8.0 IRI-2016 "standard" switch set)

| Form field | Value | Why |
|---|---|---|
| Time type | **UT** | the project's target times are UTC |
| Date/time | the case's UTC time (below) | |
| Coordinate type | **geographic** | D-1 station coordinates |
| Latitude / Longitude | the case's values (below), degrees, E positive | |
| Profile type | **Height**; start **300**, stop **300**, step **10** | one output row; TEC does not depend on the profile row |
| Upper height for TEC integration | **2000** km | Vision §6.11 ceiling; matches `htop_km` |
| Lower height for TEC integration | **90** km | matches the adapter's `hbot_km`; the form default 65 must be changed |
| Output type | **1** (hmF2, hmF1, hmE, hmD, NmF2 …, **TEC**, TOP) | the TEC column is the reference value |
| **Use Optionals: ON** | | the form default hmF2 model is NOT the IRI-2016 standard |
| Ne Topside | NeQuick | jf(29)=jf(30)=false |
| foF2 model | URSI-88 | jf(5)=false |
| foF2 storm | **checked** | jf(26)=true |
| Ne topside storm | unchecked | jf(37)=true |
| hmF2 model | **Shubin-COSMIC-model** (change from AMTB) | jf(39)=jf(40)=false, IRI-2016 standard |
| hmF2 with foF2 storm | unchecked | jf(36)=true |
| Bottomside thickness B0 | ABT-2009 | jf(4)=false, jf(31)=true |
| F1 model | Scotto-1997-no-L | jf(19)=jf(20)=true |
| E-peak auroral storm | unchecked | jf(35)=false |
| D | IRI-1990 | jf(24)=true |
| Te | TBT-2012_PF107 | jf(23)=false, jf(42)=true |
| Ti | Bil-1981 | only IRI-2016 option |
| Ion composition | RBV10/TBT15 | jf(6)=false |
| Auroral boundary model | unchecked | jf(33)=false |
| F107D, F107_81AVG, Rz12, IG12 | **leave blank** | file inputs, as D-45 item 1 (no overrides) |

## The eight cases

| # | site | lat | lon | UTC | class | activity (GFZ definitive Kp) |
|---|---|---|---|---|---|---|
| 1 | ARUC | 40.286 | 44.086 | 2022-01-07 12:00 | day | quiet (Kp 0 all day) |
| 2 | ARUC | 40.286 | 44.086 | 2022-01-07 00:00 | night | quiet |
| 3 | ARUC | 40.286 | 44.086 | 2022-03-13 22:00 | night | disturbed (Kp 6+) |
| 4 | BSHM | 32.778987 | 35.022987 | 2022-09-04 10:00 | day | disturbed (Kp 6+) |
| 5 | BSHM | 32.778987 | 35.022987 | 2022-08-04 12:00 | day | quiet (max Kp 2) |
| 6 | NICO | 35.140989 | 33.396450 | 2022-09-04 22:00 | night | disturbed (Kp 5) |
| 7 | NICO | 35.140989 | 33.396450 | 2022-11-17 02:00 | night | quiet (max Kp 0.67) |
| 8 | NICO | 35.140989 | 33.396450 | 2022-04-14 16:00 | day | disturbed (Kp 6) |

## What to copy for each case — into `kaggle/b01_validation_samples.json`

Copy `kaggle/b01_validation_samples.TEMPLATE.json` to `kaggle/b01_validation_samples.json`
(it already lists the eight cases) and fill, per case:

- `official_interface_value`: the **TEC** column value exactly as displayed (do not round, do
  not convert; units are TECU = 10^16 m^-2). Note the number of decimals shown.
- `official_interface_source`: `CCMC Instant Run IRI-2016, <retrieval date UTC>, <the output
  text URL the page offers ("txt")>`.
- `official_interface_top`: the **TOP** column value (topside share), if displayed.
- `official_interface_header`: the header lines of the text output verbatim — in particular
  any line stating the F10.7 / Rz12 / IG12 used and the model/data version; this is how a
  server-side index-file difference is identified rather than assumed.
- Save the full text output of every run beside the JSON as
  `kaggle/official_reference_outputs/case_<n>.txt` (retained in the package as provenance).

## Do not

- Do not compute or look at the adapter's values for these cases before the tolerance is
  approved and its declaration time is recorded in `configs/experiment.yaml`
  (`benchmark_b01.validation_report.tolerance_tecu` / `tolerance_declared_at_utc`); the report
  builder refuses to run while they are TBD.
- Do not change a case, the lower/upper heights, or any option to obtain agreement.
