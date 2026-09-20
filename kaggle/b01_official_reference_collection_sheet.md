# B-01 — official IRI-2016 reference values: manual collection sheet (R-59 area 6)

Revision 3, 2026-09-20: §9 records the collection outcome (7 of 8 cases accepted; case 5
to be re-run at the correct hour) and the 12-hour time-picker pitfall. Revision 2 (earlier
the same day, `governance/CHANGE_RECORD_2026-09-20_b01_prerequisites.md` §3) and revision 1
(2026-09-19) are superseded; the eight cases, the URL and the option mapping are
unchanged. New in this revision: the selection re-verification, the station-altitude section,
the integration-limit facts measured on the pinned wheel, the exact per-case field values, the
save list and filenames, and the access status.

## 0. Status of the eight cases (verified 2026-09-20)

- **Selected before any retrieval** — `evidence/iri2016_official_reference_2026-09-19/sample_selection.json`,
  `selected_at_utc` 2026-09-19T20:28:42Z. The record is preserved unchanged.
- **None is in December 2022.** Re-derived by `evidence/b01_tolerance_basis_2026-09-20/verify_selection.py`
  from the audited definitive Kp record (`evidence/audit_gfz_2026-09-18/Kp_def2022.wdc`) with
  **December rows skipped before parsing** (334 January–November rows parsed, 0 December rows).
  Every activity claim in the selection record re-derives from those rows alone: 2022-01-07 is
  the only January–November day with Kp 0.0 in all eight slots; 2022-03-13 21–24 UT 6.33;
  2022-09-04 09–12 UT 6.33 and 21–24 UT 5.0; 2022-08-04 day-max 2.0; 2022-11-17 day-max 0.67;
  2022-04-14 15–18 UT 6.0. An extremum taken over a set that excludes December cannot depend on
  December's values, so **December did not influence the selection**. One precision: the
  record says "extremes"; the two disturbed cases at 6.33 are not the single most disturbed
  January–November slots (2022-04-10 03–06 UT and 2022-08-17 18–21 UT reach 6.67). That is a
  wording nuance, not a defect, and no case is replaced. Output:
  `evidence/b01_tolerance_basis_2026-09-20/selection_verification.json`.
- Kp is a driver series (custody class 5, D-48); no target value and no December target was
  read for this check.

## 1. Where

**URL:** `https://kauai.ccmc.gsfc.nasa.gov/instantrun/iri` — CCMC Instant Run, IRI. Select
**IRI-2016** in the version selector at the top of the form.

Access status: a single bounded `GET` of that page on 2026-09-20T08:40:40Z returned HTTP 200
(7,633 bytes, the page names IRI-2016). Programmatic **run** requests were refused with HTTP 429
on 2026-09-19 after two schema probes (`official_runs.json`), and nothing was retried; collect
the eight runs **by hand in the browser**, one at a time, and if the site answers "rate limit
exceeded", wait several minutes — do not script it and do not retry in a loop.

## 2. Settings — identical for every case

These reproduce the option set the pinned adapter uses (`iricore.vtec` with its default
`default_edens` flag preset = IRI-2016's "standard" `jf` column for the electron density; the
Te/Ti/ion-composition switches it turns off have no effect on Ne or TEC).

| Form field | Set to | Why |
|---|---|---|
| Model version | **IRI-2016** | D-45 |
| Time type | **UT** (universal time) | the project's target times are UTC |
| Year / month / day / hour | the case's UTC values (§4); minutes 0 | |
| Coordinate type | **geographic** | D-1 coordinates are geographic |
| Latitude / longitude | the case's values (§4), decimal degrees, east positive | station coordinates, never a cell centre (D-45; Vision §6.6) |
| Profile type | **Height**; start **300**, stop **300**, step **10** | one output row; the TEC column does not depend on the profile row |
| Upper height for TEC integration (`tecUpper`) | **2000** km | Vision §6.11 ceiling = adapter `htop_km` |
| Lower height for TEC integration (`tecLower`) | **90** km (change from the default 65) | adapter `hbot_km`; see §3 for what this field actually does |
| Output type | **1** (hmF2, hmF1, hmE, hmD, NmF2 …, **TEC**, TOP) | the TEC column is the reference value |
| Use optionals | **ON** | the form's default hmF2 model is NOT the IRI-2016 standard |
| Ne topside | NeQuick | jf(29)=jf(30)=false |
| foF2 model | URSI-88 | jf(5)=false |
| foF2 storm model | **checked** | jf(26)=true |
| Ne topside storm | unchecked | jf(37)=true |
| hmF2 model | **Shubin-COSMIC-model** (change from AMTB) | jf(39)=jf(40)=false — IRI-2016 standard |
| hmF2 with foF2 storm | unchecked | jf(36)=true |
| Bottomside thickness B0 | ABT-2009 | jf(4)=false, jf(31)=true |
| F1 model | Scotto-1997-no-L | jf(19)=jf(20)=true |
| E-peak auroral storm | unchecked | jf(35)=false |
| D-region | IRI-1990 | jf(24)=true |
| Te | TBT-2012_PF107 | no effect on TEC |
| Ti | Bil-1981 | no effect on TEC |
| Ion composition | RBV10/TBT15 | no effect on TEC |
| Auroral boundary model | unchecked | jf(33)=false |
| F107D, F107_81AVG, Rz12, IG12 | **leave blank** ("file input") | D-45 item 1: no overrides; the server's index files are then used and their values appear in the header |

## 3. Station altitude versus the electron-density integration limits — do not confuse them

- **Station altitude is not an IRI input.** IRI-2016 is evaluated at a geographic latitude and
  longitude; the ellipsoidal heights in the registry (ARUC 1222.0 m, BSHM 225.1 m, NICO 190.1 m,
  `configs/data.yaml`) play no role in the model and are not entered anywhere on the form. The
  adapter does not use them either. Vertical TEC is the column integral above the point, not
  above the antenna.
- **The integration limits are model heights** in kilometres: `tecLower` = 90 km and
  `tecUpper` = 2000 km bound the electron-density integral. The adapter integrates Ne from
  90 km to 2000 km in 0.5 km steps (`hbot_km` / `htop_km` / `hstep_km` in `experiment.yaml`).
- **What `tecLower` = 90 actually does on the IRI side, measured on the pinned wheel's own
  Fortran** (`iritec.for`, subroutine `iri_tec`): the routine's first integration node is fixed at
  **100 km** (`hr(1) = 100.`) and a start height below 100 km is simply not used — so any
  `tecLower` ≤ 100 gives the same official TEC, integrated from 100 km. The adapter, by contrast,
  does include 90–100 km. On 288 non-December profiles at the three stations that band is
  **0.0015–0.078 TECU** (daytime maximum; night ≈ 0.002). Setting 90 on the form is still the
  right documentation of intent; expect it to change nothing on the server. Do not lower it to
  the default 65 either — that changes nothing on the server and would misdescribe the adapter.
- The form's height profile (300–300 km) is unrelated to both: it only selects which altitude
  rows are printed.

## 4. The eight cases — every value to enter

Coordinates are the D-1 values transcribed in `configs/data.yaml: stations` (site-log
validated 2026-09-19). Enter latitude/longitude exactly as printed.

| # | Site | Latitude (°N) | Longitude (°E) | Year | Month | Day | Hour UT | Class | Activity (definitive Kp) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ARUC | 40.286 | 44.086 | 2022 | 1 | 7 | 12 | day | quiet — Kp 0.0 all day |
| 2 | ARUC | 40.286 | 44.086 | 2022 | 1 | 7 | 0 | night | quiet — Kp 0.0 all day |
| 3 | ARUC | 40.286 | 44.086 | 2022 | 3 | 13 | 22 | night | disturbed — 21–24 UT Kp 6.33 |
| 4 | BSHM | 32.778987 | 35.022987 | 2022 | 9 | 4 | 10 | day | disturbed — 09–12 UT Kp 6.33 |
| 5 | BSHM | 32.778987 | 35.022987 | 2022 | 8 | 4 | 12 | day | quiet — day-max Kp 2.0 |
| 6 | NICO | 35.140989 | 33.396450 | 2022 | 9 | 4 | 22 | night | disturbed — 21–24 UT Kp 5.0 |
| 7 | NICO | 35.140989 | 33.396450 | 2022 | 11 | 17 | 2 | night | quiet — day-max Kp 0.67 |
| 8 | NICO | 35.140989 | 33.396450 | 2022 | 4 | 14 | 16 | day | disturbed — 15–18 UT Kp 6.0 |

Minutes and seconds: 0. Every other field: §2, unchanged between cases.

## 5. What to save for each case

From the run's text output (the page offers it as a "txt" link — open it and save the whole
file; also keep a screenshot of the filled form the first time):

| Field in `b01_validation_samples.json` | What to copy |
|---|---|
| `official_interface_value` | the **TEC** column value exactly as displayed — no rounding, no conversion (TECU = 10^16 m^-2). Also note how many decimals the page shows (expected one) |
| `official_interface_top` | the **TOP** column (topside share, %) if displayed |
| `official_interface_source` | `CCMC Instant Run IRI-2016, <retrieval instant UTC, e.g. 2026-09-21T10:15Z>, <the txt output URL>` |
| `official_interface_header` | the header lines of the text output **verbatim** — every line that states the F10.7 / F10.7_81 / Rz12 / IG12 used, the model/data version, and the integration limits echoed back; this is how a server-side index-file difference is identified instead of assumed |
| (file) | the full text output saved as `kaggle/official_reference_outputs/case_<n>_<SITE>_<YYYYMMDD>T<HH>Z.txt`, e.g. `case_1_ARUC_20220107T12Z.txt` — retained in the package as provenance |
| (file, once) | a screenshot of the completed form with optionals expanded: `kaggle/official_reference_outputs/form_settings.png` |

Start from `kaggle/b01_validation_samples.TEMPLATE.json` (the eight cases are prefilled), copy it
to `kaggle/b01_validation_samples.json`, fill the fields above per case, then rebuild the package
(`python kaggle/build_b01_package.py`).

## 6. Comparability with the installed path — what is matched, what is not

| Aspect | Adapter (pinned `iricore` 1.8.0, Kaggle) | Official form | Status |
|---|---|---|---|
| Model | IRI-2016 (`version=16`) | IRI-2016 | matched. Measured note: in the pinned wheel, IRI-2016 and IRI-2020 return bit-identical Ne under the standard switches (Te/oarr differ), so the explicit `version=16` is correct but not discriminating there |
| Ne option switches | `default_edens` = IRI-2016 standard column | §2 mapping | matched |
| Index inputs | `apf107.dat` / `ig_rz.dat` pinned by SHA-256 (D-45) | server files, version not displayed | matched only if the header's F10.7/Rz12/IG12 equal the pinned files' 2022 values — checked from the header, never absorbed by the tolerance |
| Coordinates | station lat/lon | same | matched |
| Time | UTC hour, minutes 0 | UT | matched |
| Upper limit | 2000 km | 2000 km | matched |
| Lower limit | 90 km, included | 90 km entered; server integrates from 100 km (§3) | **explicit residual**: ≤ 0.078 TECU, adapter higher |
| Quadrature | rectangle sum, 0.5 km, plus `iricore`'s `_clean_ne_for_tec` step | `iri_tec` midpoint segments (step scheme `istep` unknown: 0/1/2) | **explicit residual**: quantified in the tolerance proposal |
| Display | float64 | one decimal (to be confirmed from the first output) | ≤ 0.05 TECU rounding |

## 7. If manual access also fails

Do not fabricate, estimate or substitute a value. Two source-backed alternatives are prepared
for review (neither is executed without approval):

1. **The legacy CCMC IRI-2016 form** (`https://ccmc.gsfc.nasa.gov/modelweb/models/iri2016_vitmo.php`,
   same institution, same model, saved copy from 2026-09-19 in the previous session's record) —
   an official interface in R-59's sense, different front end.
2. **The official IRI-2016 Fortran reference build** (the `iri2016` distribution from the IRI
   project's site), compiled and run with the **pinned** `apf107.dat` / `ig_rz.dat` and the same
   standard switches — R-59 permits a reference-build comparison; the same report schema takes
   it as `official_interface_value` with the source recorded. This removes the server-index
   unknown but is a self-built reference, so its provenance (source archive hash, compiler,
   commit) must be recorded before use.

## 8. Do not

- Do not compute or look at the adapter's values for these eight cases before the tolerance is
  approved and its declaration instant is written to `configs/experiment.yaml`
  (`benchmark_b01.validation_report.tolerance_tecu` / `tolerance_declared_at_utc`); the report
  builder refuses while they are TBD. (The convergence checks used other, non-December
  dates.)
- Do not change a case, the limits, or any option to obtain agreement; do not replace a case
  because its output looks awkward.

## 9. Collection outcome, 2026-09-20 (revision 3 of this sheet)

Eight text outputs and one screenshot were saved to `kaggle/official_reference_outputs/`
between 13:41 and 13:59 UTC. Checked against the server-echoed header of each file (the
header is authoritative; filenames are not):

| Case | Saved file (after correction) | Header agrees with §4? | Disposition |
|---|---|---|---|
| 1 | `case_1_ARUC_20220107T12Z.txt` | yes (`2022/-7/12.0UT`, 40.3/44.1) | accepted — the file was saved under case 2's name and has been renamed |
| 2 | `case_2_ARUC_20220107T00Z.txt` | yes (`2022/-7/ 0.0UT`) | accepted — was saved under case 1's name; renamed |
| 3 | `case_3_ARUC_20220313T22Z.txt` | yes | accepted |
| 4 | `case_4_BSHM_20220904T10Z.txt` | yes | accepted |
| 5 | `rejected_case_5_BSHM_20220804T00Z_wrong_hour.txt` | **no** — header says `0.0UT`, case 5 is **12 UT** | **rejected; re-run required** (the file is kept as evidence of the attempt, never used) |
| 6 | `case_6_NICO_20220904T22Z.txt` | yes | accepted |
| 7 | `case_7_NICO_20221117T02Z.txt` | yes | accepted (hour token zero-padded) |
| 8 | `case_8_NICO_20220414T16Z.txt` | yes | accepted |

Cause of the three hour errors: the current CCMC form takes the time through a **12-hour
picker** (`hh:mm AM/PM`). `0 UT` must be entered as **12:00 AM**, `12 UT` as **12:00 PM**;
1–11 UT are AM, 13–23 UT are PM. Case 1 and case 2 were entered the other way round and
case 5 as 12:00 AM. The header line `yyyy/mmdd(or -ddd)/hh.h)` on the output is the check:
its last field is the UT hour the server actually used.

What the headers additionally establish, for every accepted case: version selector IRI-2016
(screenshot), NeQuick topside, URSI-88 foF2, foF2 storm on, **Shubin-2015 hmF2**, ABT-2009 B0,
Scotto-97-no-L F1, foE auroral storm off, IRI-1990 D-region, TBT-2012 Te, RBV10+TBT15 ions —
i.e. every §2 option as required, echoed by the server itself. Rz12, IG12, daily and 81-day
F10.7 are printed per case and are recorded verbatim in the samples file. The TEC column is
printed to **one decimal**; `t/%` (share of TEC above the F2 peak) and `hmF2` are recorded
beside it (hmF2 is the D-50 diagnostic, no threshold).

Two deviations, both immaterial by the measured bands in
`governance/proposed/B01_TOLERANCE_PROPOSAL_2026-09-19.md` §2 and recorded rather than
corrected: (i) the current form exposes no `tecLower` field; the header echoes `from 50 to
2000.0 km` (the 50–100 km contribution the server-side `iri_tec` scheme ignores below 100 km
anyway; 65–90 km measured ≤ 0.006 TECU, 50–65 km is D-region and smaller still); (ii) the
saved screenshot `form_settings_default_page_not_the_filled_form.png` shows the form's
default page (2012, 10°/110°), not a filled case with the optionals expanded — it proves the
IRI-2016 selector only; the per-option evidence is the header block of each output, which is
stronger, so no retake is required.

**Assembly.** `kaggle/official_reference_outputs/parse_official_outputs.py` reads every
`case_*.txt`, matches each to its §4 case by the echoed header (never by filename), and writes
`kaggle/b01_validation_samples.DRAFT.json`; it writes `kaggle/b01_validation_samples.json`
only when all eight match. Today: **7/8 filled; case 5 missing.** Re-run case 5 (BSHM,
32.778987 / 35.022987, 2022-08-04, **12:00 PM**), save the txt as
`case_5_BSHM_20220804T12Z.txt`, run the script, then `python kaggle/build_b01_package.py`.
