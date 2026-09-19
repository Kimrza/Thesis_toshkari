# Change Record — 2026-09-18 — GFZ driver-pair acquisition audit (Kp/ap, Hp60/ap60)

**Change ID:** `CR-2026-09-18-GFZ-DRIVER-PAIR-AUDIT`
**Authority:** the project decision owner's **qualified approval of 2026-09-18**, given
in-session after the read-only GFZ archive check, quoted in substance: (1) for Kp/ap,
retrieve the provider-native 2022 pair `Kp_now2022.wdc` / `Kp_def2022.wdc` and perform
the value-by-value comparison R-63 control 5 requires, recording that the archived
nowcast is the settled, final-stage nowcast after its ~1–2-day revision period, not the
first-issued value at each forecast origin, and claiming no exact first-issue
reconstruction; (2) for Hp60/ap60, accept Hpo.0002 V2.0 as the contemporaneous 2022
product grade and compare it with Hpo.0003 V3.0 **only as a documented substitute
control**, labelled "contemporaneous V2.0 versus later algorithm-recomputed V3.0", never
"NRT versus definitive"; (3) record the provider limitation explicitly; (4) proceed with
retrieval, hashing, parsing and comparison while preserving the locked-test access and
experiment-registry controls. This is the owner instruction `project.md`
(`code-generation:c32`) names as the sanctioned route for work touching a READY unit's
surface — here `acquisition`'s retrieval client and manifest writers are USED, not edited.
**Repository state:** HEAD `18843aa`, working tree carrying the uncommitted D-25 Route 1
reconstruction (`CR-2026-09-16-D25-AVAILABILITY-RULE`). **No commit is made by this
pass.** **No D-number is drafted**: no scientific constant, config value or §18.2 item is
decided; the required release grade per series remains the Student + Supervisor item
`acquisition` R-40 routes to G-04.

---

## 1. What was done

`scripts/audit_gfz_drivers.py` (new; stdlib + this repository's own modules) retrieved
exactly four provider files into `evidence/audit_gfz_2026-09-18/`, hashed them, parsed
them, validated 2022 coverage / chronology / cadence / duplicates / missingness, and
compared each pair value by value. Retrieval went through `acquisition`'s
`RetrievalClient` (TS-A-01, bounded retry, rate bound 1 s) with a stdlib `urllib`
transport **injected by the script**; `scripts/00_acquire_prepared_vtec.py:_build_transport`
is unchanged and still refuses. Licence CC BY 4.0 on every file; no credential exists or
was used for provider `gfz`.

| Logical name | Provider product identity (version = DOI) | Server Last-Modified | Bytes | SHA-256 |
|---|---|---|---|---|
| `Kp_now2022.wdc` | `Kp_now2022.wdc` (DOI 10.5880/Kp.0001, folder `Kp_nowcast`) | 2023-01-24 06:57:38 GMT | 23,581 | `7929d16aa1a14d35dff6759c02367746438b09dd084fdc731a4052af5a7475a4` |
| `Kp_def2022.wdc` | `Kp_def2022.wdc` (DOI 10.5880/Kp.0001, folder `Kp_definitive`) | 2023-01-24 06:57:38 GMT | 23,581 | `c1d9030254e5b1e9581065166ab501b7aad9f2e07756551aefa8b18302c2b829` |
| `hp60ap60doi_2022_v2.txt` | `Hp60ap60doi_2022.txt` (DOI 10.5880/Hpo.0002, folder `Hpo60`) | 2023-01-24 06:57:43 GMT | 527,283 | `0ad71bf0eab1412852dd57ade1f7e2fdf5ff18f1cf9d20ebab8babc1fe471ad6` |
| `hp60ap60doi_2022_v3.txt` | `Hp60ap60doi_2022.txt` (DOI 10.5880/Hpo.0003, folder `Hpo60`) | 2025-04-03 09:28:21 GMT | 527,342 | `a689ddef5590bf9cb6cc32cf72817921c93bf7e40d658b9181e2b5a3f665d461` |

Retrieval date 2026-09-18 (UTC). The Hpo files are stored under lower-case logical names
with a version suffix because the provider filename is identical across DOIs; the served
name and the DOI are both recorded in `retrieval_record.json`.

## 2. Measured results (derived by the script and printed; nothing carried)

**Parse validation** — all four files: 2022 epochs complete (Kp: 2,920 = 365×8; Hp60:
8,760 = 365×24), chronology monotonic, 0 cadence breaks, 0 out-of-year rows, 0 missing
symbols.

**Kp/ap — nowcast versus definitive (R-63 control 5, literal form).**
1,046 of 2,920 epochs differ (35.82 %); per month (Jan→Dec): 75, 78, 96, 87, 89, 76, 95,
99, 90, 91, 80, 90; max |ΔKp| = 0.667 (two thirds), max |Δap| = 17. The designed control
`spaceweather.assert_gfz_cross_products` fires when the emitted series equals the
definitive product — consistent with the count.

**Hp60/ap60 — contemporaneous V2.0 versus later algorithm-recomputed V3.0 (documented
SUBSTITUTE control; NOT NRT versus definitive).** 1,790 of 8,760 epochs differ
(20.43 %); per month: 163, 130, 157, 135, 129, 124, 203, 183, 159, 151, 121, 135;
max |ΔHp60| = 0.667, max |Δap60| = 31. The designed control fires on the same basis.

## 3. Provider limitations — recorded verbatim in `retrieval_record.json`,
`gfz-comparison-report.json` and `GFZ-AUDIT.md`

- **Kp/ap:** historical nowcast and definitive variants exist for 2022 (DOI
  10.5880/Kp.0001). The archived nowcast is the **settled, final-stage nowcast** after its
  approximately 1–2-day revision period ("At the time of the calculation of the definitive
  Kp, also the nowcast Kp for the previous month has reached a final stage. It will not
  change any more and is archived here." — `kp_index_data_description_20210311.pdf` §4).
  It is **not** the first-issued value available at each 2022 forecast origin, and **no
  exact first-issue reconstruction is claimed**.
- **Hp60/ap60:** **no provider-native NRT/definitive pair exists.** GFZ publishes Hpo as a
  single near-real-time-algorithm product ("Currently always D = 0, reserved for future
  use"; JSON service: "Status is not available for Hp30 and Hp60"). The comparison
  performed is "contemporaneous V2.0 (DOI 10.5880/Hpo.0002, in force 2022-03-26 →
  2024-06-17) versus later algorithm-recomputed V3.0 (DOI 10.5880/Hpo.0003, 2024-06-17;
  algorithm "changed to give a better occurrence frequency of index values for Hpo ≥ 9")".
  It **tests sensitivity to later algorithmic recomputation and does not demonstrate
  definitive backfill**; the literal R-63 control 5 comparison is impossible for this
  series.

## 4. Controls preserved

- **Locked-test access.** Only DRIVER records were read; no December 2022 TARGET value
  was touched. Driver artifacts are excluded from locked-test custody by
  `governance-guards` R-26; registry rows carry `locked_test_accessed = false`; no
  access-log row is written (none is owed for a driver read). JSON outputs key months as
  INTEGERS and epochs as `{y, m, d, h}` objects, and `_write_json` refuses any `"2022-12`
  literal, so `assert_no_december_outside_restricted` (which matches that literal in
  `*.json`) has nothing to match. Verified: `tests/test_locked_test_guard.py`,
  `tests/test_acquisition.py`, `tests/test_release_hashes.py`,
  `tests/test_external_drivers.py` — **121 passed** with the new evidence in place.
- **Experiment registry.** Every run appended a `started` row and a terminal row through
  `append_registry_event` (`artifacts/registry/experiment_registry.jsonl`, created by this
  pass). **Five runs FAILED before the first completed one** — each on the W-9 credential
  egress guard refusing a legitimate value shape (the DOI-path identity, a run id with a
  `T`, a 23-character mixed-case logical name, the grade label `contemporaneous-V2.0`,
  the `platform.platform()` string) — and each failure is recorded with its reason,
  never deleted (NFR-AUD-01, R-09). The fix in every case was to change the SCRIPT's
  value shape, **never to grow `REDACTION_ALLOWLIST`** (a reviewed surface). Then one
  completed online run and two completed `--offline` re-runs (byte-identical provider
  hashes; identical comparison counts).
- **`environment_lock_hash`** on every row is a **supplemental stdlib lock**
  (`environment_supplemental.json`: interpreter, platform, script hash, `code_commit`,
  dirty flag), NOT `capture_environment_lock`, which needs `pyyaml` — absent on this host.
  Stated in `notes` on every row.

## 5. Findings disclosed, not repaired

1. **`write_sha256_manifest` (W-4) is incompatible with TA-15's governed reader.**
   `tests/test_release_hashes.py::_declared_artifacts` flattens EVERY
   `evidence/**/sha256_manifest.json` as `{filename: sha256}`; W-4's nested shape
   (`provider_files`, `derived_artifacts`, `hash_count`, `provenance_class`,
   `producing_interpreter`) fails that test on its own metadata keys — observed here
   (3 failures on first run). This pass writes BOTH: the W-4 manifest as
   `w4_provider_sha256_manifest.json` and a flat TA-15-shape `sha256_manifest.json`.
   A real `scripts/00` acquisition landing under `evidence/` would hit the same
   incompatibility — an `acquisition` / `fixtures-and-reproducibility` finding for the
   `build-and-test` gate.
2. **R-26's exhaustively enumerated driver-exclusion list (four classes) now has a
   fifth candidate**: raw GFZ index files and their derived audit JSON under
   `evidence/audit_gfz_2026-09-18/`. The enumeration is design text (no coded list
   exists); the owner should rule whether the design's table gains a row.
3. **The W-9 heuristic refuses ordinary provider identities** (any ≥20-char token with
   upper+lower+digits). Worked around by prose-shaped identities; worth an `acquisition`
   note before `scripts/00` records real Madrigal filenames.
4. **Pre-existing December-scan offender**: `evidence/audit_ec1_2026-08-15/ec1-audit-report.json`
   carries `"2022-12-31"` (`last_2022_date`) and is returned by
   `assert_no_december_outside_restricted`; it is R-26 class 3 and untouched by this pass.

## 6. What this pass does NOT do

No producer artifact; no `permitted_producers` row; `configs/` untouched
(`availability_lags` = `"TBD — freeze gate"`); no release grade decided; no
`recomputation_tolerance`; Stage 07 unwired; `_build_transport` unmodified; no commit,
push or `graphify query`. Q4/Q5 (Hp60 provider = GFZ; three producer ids) remain
unrecorded and are still owed before any registration.

## 7. Files

New: `scripts/audit_gfz_drivers.py`; `evidence/audit_gfz_2026-09-18/` (4 provider files,
`retrieval_record.json`, `gfz-comparison-report.json`, `GFZ-AUDIT.md`,
`environment_supplemental.json`, `w4_provider_sha256_manifest.json`,
`sha256_manifest.json`); `artifacts/registry/experiment_registry.jsonl`; this record.
Modified by this pass: none of the D-25 files; `construction/build-and-test/memory.md`
(diary). Propagation sweep (CHANGE_RECORD_PROCEDURE step 2): this record amends no count
or status in any prior artifact; the "GFZ never retrieved" statements in
`scripts/04_build_external_products.py:751-759`, `external-products` R-63 and
`acquisition` R-40 are now historically true and future-stale — **left standing** (a
completed stage's artifacts; script 04's comment is code owned by `external-products`
under its receipt) and listed here as owed at the next gate.
