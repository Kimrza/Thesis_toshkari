# GFZ driver-pair audit — retrieval, hashes, parse validation and cross-comparison

Generated 2026-09-18T21:17:30.194366+00:00 by `scripts/audit_gfz_drivers.py`; machine-readable twins: `retrieval_record.json`, `gfz-comparison-report.json`, `sha256_manifest.json`.

## Retrieved files (TE 13.3 source_files items)

| Logical name | Provider product identity (incl. DOI version path) | Retrieval date | Server Last-Modified | Bytes | SHA-256 |
|---|---|---|---|---|---|
| `Kp_now2022.wdc` | `Kp_now2022.wdc (DOI 10.5880/Kp.0001, folder Kp_nowcast)` | 2026-09-18 | Tue, 24 Jan 2023 06:57:38 GMT | 23581 | `7929d16aa1a14d35dff6759c02367746438b09dd084fdc731a4052af5a7475a4` |
| `Kp_def2022.wdc` | `Kp_def2022.wdc (DOI 10.5880/Kp.0001, folder Kp_definitive)` | 2026-09-18 | Tue, 24 Jan 2023 06:57:38 GMT | 23581 | `c1d9030254e5b1e9581065166ab501b7aad9f2e07756551aefa8b18302c2b829` |
| `hp60ap60doi_2022_v2.txt` | `Hp60ap60doi_2022.txt (DOI 10.5880/Hpo.0002, folder Hpo60)` | 2026-09-18 | Tue, 24 Jan 2023 06:57:43 GMT | 527283 | `0ad71bf0eab1412852dd57ade1f7e2fdf5ff18f1cf9d20ebab8babc1fe471ad6` |
| `hp60ap60doi_2022_v3.txt` | `Hp60ap60doi_2022.txt (DOI 10.5880/Hpo.0003, folder Hpo60)` | 2026-09-18 | Thu, 03 Apr 2025 09:28:21 GMT | 527342 | `a689ddef5590bf9cb6cc32cf72817921c93bf7e40d658b9181e2b5a3f665d461` |

## Parse validation

| File | 2022 epochs | expected | chronology | cadence breaks | missing epochs |
|---|---|---|---|---|---|
| `Kp_now2022.wdc` | 2920 | 2920 | monotonic | 0 | 0 |
| `Kp_def2022.wdc` | 2920 | 2920 | monotonic | 0 | 0 |
| `hp60ap60doi_2022_v2.txt` | 8760 | 8760 | monotonic | 0 | 0 |
| `hp60ap60doi_2022_v3.txt` | 8760 | 8760 | monotonic | 0 | 0 |

## Value-by-value comparisons

### `kp_ap3` — nowcast (settled, final-stage) versus definitive — R-63 control 5, literal

- epochs compared: 2920; only in first: 0; only in second: 0
- mismatching epochs: **1046** (35.8219% of compared)
- mismatches per month (1..12): [75, 78, 96, 87, 89, 76, 95, 99, 90, 91, 80, 90]
- designed control `assert_gfz_cross_products` fired: True (consistent with count: True)

### `hp60_ap60` — contemporaneous V2.0 versus later algorithm-recomputed V3.0 — documented SUBSTITUTE control, not NRT versus definitive

- epochs compared: 8760; only in first: 0; only in second: 0
- mismatching epochs: **1790** (20.4338% of compared)
- mismatches per month (1..12): [163, 130, 157, 135, 129, 124, 203, 183, 159, 151, 121, 135]
- designed control `assert_gfz_cross_products` fired: True (consistent with count: True)

## Provider limitations (recorded verbatim in the JSON twins)

- **kp_ap3**: Historical nowcast and definitive variants exist for 2022 under DOI 10.5880/Kp.0001 (Kp_nowcast/Kp_now2022.wdc, Kp_definitive/Kp_def2022.wdc). The archived nowcast is the SETTLED, final-stage nowcast after its approximately 1-2-day revision period, not the first-issued value available at each 2022 forecast origin; exact first-issue reconstruction is not claimed.
- **hp60_ap60**: No provider-native NRT/definitive pair exists: GFZ publishes Hpo as a single near-real-time-algorithm product with no definitive grade and no archived nowcast. The comparison performed is 'contemporaneous V2.0 (DOI 10.5880/Hpo.0002, in force 2022-03-26 to 2024-06-17) versus later algorithm-recomputed V3.0 (DOI 10.5880/Hpo.0003, 2024-06-17)'. It tests sensitivity to later algorithmic recomputation and does NOT demonstrate definitive backfill; the literal R-63 control 5 comparison is impossible for this series.

## What this audit does NOT do

- creates no producer artifact and no `permitted_producers` entry; `availability_lags` stays `TBD — freeze gate`;
- decides no release grade for any feature contract (Student + Supervisor, G-04);
- reads no December 2022 target value (`locked_test_accessed = false`; driver records are R-26-excluded from custody);
- claims no first-issue reconstruction for the Kp nowcast and no definitive-backfill detection for Hp60/ap60.
