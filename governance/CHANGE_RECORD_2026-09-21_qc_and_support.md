# Change record — `CR-2026-09-21-QC-AND-SUPPORT`

**Date:** 2026-09-21 · **Authorized by:** the project decision owner, explicitly, on that date
("approved, proceed"; "Transcribe existing approvals now") · **Status:** written to config,
verified against the readers; two proposed D-numbers owed to `evidence/DECISIONS.md`

---

## §1 — `configs/data.yaml: qc_operations` (the documented-QC closure act)

`assert_qc_operations_frozen` requires a **D-number citation and a non-empty enumerated
list** — explicitly *"never mere non-emptiness, since a list filled by convenience satisfies
'non-empty' and is exactly what TE §18.2 forbids"*. Until now the field was absent, and no
standardized target artifact could be produced by any path.

### The exact YAML written

```yaml
qc_operations:
  decision: "D-53"                 # PROPOSED number, pending adoption
  frozen_at_utc: "2026-09-21"
  operations:
    - "reject_unexplained_negative_vtec"
    - "flag_valid_observation_count_below_minimum"
    - "flag_within_hour_spread_above_range_bound"
    - "flag_largest_internal_gap_above_maximum"
    - "flag_provider_dtec_summary_above_level"
  preserves_provider_values: true
  gap_policy: "explicit_nan_never_filled"        # D-5; D-10.2
```

### What each operation does, and which requirement governs it

| # | Operation | What it does | Governing requirement | New? |
|---|---|---|---|---|
| 1 | `reject_unexplained_negative_vtec` | A negative VTEC is **rejected** unless a recorded explanation accompanies it; an explained negative is accepted with its explanation carried in the data-quality block. The run raises rather than dropping it quietly. | **R-71 content 2; NFR-DQ-01** — "a negative VTEC is not a small value but an impossible one" | **No** — already implemented and tested |
| 2 | `flag_valid_observation_count_below_minimum` | Marks `target_valid: false` and records the reason when a cell-hour has fewer than **3** contributing samples. | **D-19** (minimum 3; retention 95.24%) | **No** |
| 3 | `flag_within_hour_spread_above_range_bound` | Marks `target_valid: false` when the range (max − min) exceeds **10.0 TECU**. | **D-19** (statistic = range; p99 = 9.616) | **No** |
| 4 | `flag_largest_internal_gap_above_maximum` | Marks `target_valid: false` when the largest internal gap exceeds **1800 s**. | **D-19** (maximum 1800 s; retention 93.39%) | **No** |
| 5 | `flag_provider_dtec_summary_above_level` | Records a **quality flag only** — does *not* invalidate the row — when median provider `dtec` exceeds **1.5 TECU**. | **D-19** (flag level; p99 = 1.314) | **No** |

**Previously approved vs. genuinely new.** All five operations were already approved and are
already implemented in `src/data/prepared.py: standardize_hourly_target`. **The only new act is
the closure of the list** — naming these five as the complete documented-QC set, so that an
operation outside it fails like a fifth transformation would (R-64, via
`assert_qc_operation_permitted`). **No threshold was invented and no provider value is
modified**: three of the five only flag or record, and none alters `vtec_tecu`.

Two facts are recorded in the block so their absence is not read as an omission:
`preserves_provider_values: true` (P1-03: *"preserve provider values; apply only documented
QC … never silently interpolate missing cells"*), and `gap_policy: explicit_nan_never_filled`
(D-5, D-10.2) — there is no gap-filling operation to enumerate because gaps are never filled.

## §2 — `configs/data.yaml: target.support_thresholds` (transcription of D-19)

Discovered by execution after §1 landed: `resolve_support_thresholds` refused next, and its
values are **already frozen by D-19** (approved 2026-08-21). All four rows were transcribed
verbatim with their measured basis, because a threshold without its basis *"is
indistinguishable from a chosen one and FAILS"* (R-68).

| Field | Statistic | Value | Role | Basis (D-19) |
|---|---|---|---|---|
| `valid_observation_count` | minimum | **3** | validity | min 1, p05 3, median 9, max 12; retention 95.24% |
| `within_hour_spread_tecu` | range | **10.0** | validity | median 2.357, p95 6.873, p99 9.616, max 51.206 TECU |
| `largest_internal_gap_s` | maximum | **1800** | validity | median 300 s, p95 2100, p99 3600; retention 93.39% |
| `provider_dtec_summary` | median | **1.5** | **flag** | median 0.920, p95 1.305, p99 1.314, max 5.553 TECU |

Every row carries `basis_window: "January-November 2022"`. **December was excluded by
construction** in D-19's own measurement — deriving a governed constant from the locked month
would let it influence the freeze set — and `resolve_support_thresholds` refuses a basis that
so much as mentions December.

## §3 — Verification

```
qc frozen OK, decision: D-53 | ops: 5
  valid_observation_count: minimum=3.0 role=validity
  within_hour_spread_tecu: range=10.0 role=validity
  largest_internal_gap_s: maximum=1800.0 role=validity
  provider_dtec_summary: median=1.5 role=flag
fifth-op control refuses: qc operation 'silently_interpolate_gaps': absent from the frozen …
```

The fifth-operation control confirms the closure is real: an operation outside the list is
refused exactly as a fifth transformation would be.

## §4 — Owed

`D-53` is a **proposed** number. The list and its five operations are the owner's approval of
2026-09-21; the register entry in `evidence/DECISIONS.md` has not been written by this session,
because the register is the student's. No supervisor signature is claimed for §1 or §2; D-19's
own approval already covers every value in §2.
