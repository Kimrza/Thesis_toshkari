# Change record — 2026-09-23 — stage 04 publishes the four driver releases

**Change ID:** `CR-2026-09-23-DRIVER-RELEASE-OPTION-A`
**Authority:** the project decision owner's ruling of 2026-09-23, verbatim: *"extend D-61 to
the Stage 04 driver-release boundary under the D-63 identities. No new D-number."*
**Baseline:** `HEAD = 09180b2`. Every figure below is measured and printed before assertion.
**Register discipline:** **no D-number is written by this pass**, as ruled. The releases
cite this change record as their `change_record_id`; the governing decisions they publish
under are D-39, D-40, D-21/D-22/D-23, D-10.1 and D-63, all of which already exist.
**Gate status:** `GOV-2026-09-20-CG-01` stands at `FAIL`. This record does not change it.

---

## 1. The defect, in the script's own words

`scripts/04_build_external_products.py` has said it since 2026-09-18 (`:807-816`): the two
GFZ series *"are NOT YET CONSUMED by this stage: no driver product is built from them here
and no producer artifact exists (D-41 identities only)"*, recorded on every run as a
machine-readable completeness fact. D-63 (2026-09-21) then named the producing-artifact
identity of each driver-class TE §6.2 row and `configs/features.yaml: permitted_producers`
transcribed them, so `build_features` already knew which artifact each row must come from —
**and nothing published one**. Third instance of the same shape (D-61 at 00→01/02;
`CR-2026-09-23-TARGET-RELEASE-OPTION-A` at 02→05; this at 04→05).

## 2. What was implemented

**One release per D-63 producing artifact**, the directory named for the identity itself so
the mapping from `permitted_producers` to the release root is the identity rather than a
convention a reader must learn:

| Release | Series | Parsed from | Governing decision |
|---|---|---|---|
| `gfz_kp_ap_nowcast_2022` | `kp`, `ap` (3-hourly) | `Kp_now2022.wdc` | D-39 (archived settled nowcast, DOI 10.5880/Kp.0001) |
| `gfz_hp60ap60_v2_2022` | `hp60`, `ap60` (hourly) | `hp60ap60doi_2022_v2.txt` | D-40 (Hpo.0002 **V2.0**; V3.0 is a comparator only and is never parsed as an input) |
| `nrcan_f107_observed_daily_median_2022` | `f107_daily_median` (daily) | `nrcan_f107/fluxtable.txt` | D-21/D-22/D-23 |
| `kyoto_wdc_dst_2022` | `dst_nt` (hourly) | `kyoto_dst/dst_provisional_*.html` | D-10.1 (one release grade, recorded before use) |

Each carries the thirteen caller-supplied TE §13.3 fields, its `producing_artifact` stated
**on the manifest** (so a consumer reads the D-63 identity rather than inferring it from a
directory name), its `release_status` from the governing decision, and its window.

**Nothing is fabricated and nothing is filled.** Values come from provider bytes this run
has already hash-verified. A provider missing marker becomes an **empty cell** and is
counted in `exclusions_qc_summary` — never written as the sentinel, never interpolated,
never carried forward (D-5; D-10.2; the 3-hour carry-forward is a *feature-time* rule at the
availability boundary, not an acquisition-time fill). Rows are bounded to the run's audit
window, so a fixture run publishes the fixture's window and nothing wider.

**The F10.7 median is not re-implemented.** `_f107_rows` calls
`spaceweather.daily_medians_from_readings`, which owns D-21's median, D-22's duplicate
averaging and D-23's high-spread flag. The release records `duplicate_readings_averaged` and
`high_spread_pct` per day so both flags travel with the value.

**TC-12 is visible in the shape.** `row_counts.by_station` records
`time_indexed_no_station_axis` rather than a per-station count: a driver series that *could*
be counted per station is already the artefact TC-12 (`binding: hard`) exists to prevent.
Both provider interval boundaries are preserved on every interval-valued row, because D-43
makes the safe-lag reference instant the interval **end** and a consumer holding only a
start cannot apply the rule.

**`processing`'s target-shaped keys.** TE §13.3 requires all seven non-empty, and four of
them describe a gridded *target*. Each carries an explicit statement of non-applicability
naming TC-12, rather than a value borrowed from the target's release (which would be false)
or an empty string (which `write_release` refuses).

**Re-runs and R-13**, identical to the target release: identical content republishes
nothing; different content refuses naming both hashes rather than overwriting a citation.

## 3. One parser per provider format

`parse_wdc` and `parse_hpo` lived in `scripts/audit_gfz_drivers.py`. The driver release and
the audit must read the provider's bytes **identically**, and two parsers of one format
drift — the failure `nfr-design` c58 records. Both moved to
`src/external/spaceweather.py` (the module that owns driver-product arithmetic) as
`parse_kp_ap_wdc` and `parse_hpo_v2`; the audit script now imports them under its own
historical names, so nothing that reads that script has to learn a new one, and exactly one
implementation exists. `KP_MISSING` moved with them.

## 4. A defect this pass introduced and then closed

The first version published fixture-run driver releases under the governed citation with no
mark of what they were: seven days of fixture data sitting at
`artifacts/releases/gfz_kp_ap_nowcast_2022/`, indistinguishable from a full-year governed
product to anyone reading the manifest without its run log. The driver *audit* artifact has
been quarantined to the walking-skeleton root as `evidence_class: fixture_plumbing` since
`CR-2026-09-13-04-FIXTURE-WINDOW`; the release was not.

Closed by stamping `evidence_class` and `fixture_scope_id` **on the manifest** of every
release, in stage 04 and in stage 02's target release alike. The stamp is on the artifact
rather than in the directory name because `05`, `06` and `07` resolve the target release's
directory by a **fixed** name, so the name cannot carry the distinction.

**Open question recorded, not decided:** whether a fixture-scoped release should live under
a fixture-named directory at all. Stage 00's fixture releases already do
(`plumbing_7day_<stamp>/`); the target release cannot while its consumers resolve it by a
fixed name. Deciding this changes three consumers, so it is the owner's.

## 5. Executed

Governed pin (conda `tec-thesis-311`, CPython 3.11.16, `CUDA_VISIBLE_DEVICES=""`,
`PYTHONHASHSEED=0`), fixture window 2022-11-01..07:

| Release | `dataset_version` | Rows | Absent values |
|---|---|---|---|
| `gfz_kp_ap_nowcast_2022` | `8facdfc61810` | **56** (7 × 8 three-hour intervals) | 0 |
| `gfz_hp60ap60_v2_2022` | `369b27ec4dd4` | **168** (7 × 24) | 0 |
| `nrcan_f107_observed_daily_median_2022` | `f395e4c8639b` | **7** days, from 21 readings | 0 |
| `kyoto_wdc_dst_2022` | `bdbd958aec68` | **168** | 0 |

**An independent cross-check, worth recording because it was not constructed to pass.** The
released Dst over the window has **minimum −92 nT**. D-11 characterised this exact window,
months earlier and by a different path, as *"geomagnetically disturbed on provisional Dst"*
carrying *"the month's minimum provisional Dst of −92 nT"*. The release reproduces a value a
frozen decision already fixed, so the parse, the window bound and the hour indexing are
right — not merely self-consistent. F10.7 daily medians run 117.7–134.6 sfu, Kp peaks at
5.0 with ap 48, all consistent with a disturbed early-November week.

## 6. Where the ladder stops now

Stages **00, 01, 02 and 04 complete**. Stage 05 stops at its own deliberate TE §18.3 stub in
`_load_release_inputs`.

**Every precondition that stub names, and both producers it waited on, now exist.** Its text
— *"reached only after the permitted-producer list, the partitions and the availability lags
are frozen; none is today"* — was already stale before this pass (D-63, D-38,
D-42/D-43/D-46/D-47) and is now stale in a second way: the released target and the released
driver products it says it would read both exist. What remains is **unbuilt
implementation**, not a missing decision, a missing declaration or a missing producer: the
loader that reads those releases into frames, and the feature build, training and evaluation
paths behind it, across `features-and-splits`, `models-and-baselines` and
`evaluation-and-comparison`. The stub's message should be corrected by the unit that builds
the loader; it is recorded here rather than edited, because the module is another unit's.

The fixture manifests' measured fields (dispositions §5 item 8) therefore remain out of
reach — now behind implementation alone.
