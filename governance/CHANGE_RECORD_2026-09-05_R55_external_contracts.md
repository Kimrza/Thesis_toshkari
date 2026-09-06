# CHANGE RECORD — `src/external` boundary contracts owed to `component-methods.md` (R-55)

**Status: DRAFT — NOT APPLIED. Applied only on the project decision owner's approval.**
**Date raised:** 2026-09-05 · **Raised by:** stage 3.5 (`code-generation`), unit `external-products` (Bolt 1)
**Owning rule:** `construction/external-products/functional-design/business-rules.md` R-55 (Q1 = D):
the contracts for `spaceweather.py`, `iri.py` and `gim.py` are designed in the unit's
artifacts and recorded as **one amendment owed** to
`inception/application-design/component-methods.md`, *"needing a change record before
stage 3.5 treats any of them as approved."* This record is that change record. **No
application-design artifact is edited by this record's existence**; the blocks below are
the proposed text, applied in place only on approval.

R-55 further **proposes — and does not take —** that this amendment be judged together
with the four other owed boundary-contract amendments (`acquisition` 3,
`inventory-and-registry` 1 — **five across three units**, boundary contracts only) as one
consolidated set. That consolidation remains the owner's call; this unit's amendment is
recorded either way.

## Why owed

`components.md` § `src/external` names the three modules and the importable-only rule;
`component-methods.md` carries boundary-call blocks for `src/features`, `src/models` and
`src/evaluation` and **nothing for `src/external`** — and its § Depth policy makes
boundary calls the contract surface. `iri.py` and `gim.py` are importable from
`scripts/04_build_external_products.py` and `src/evaluation/`, and `spaceweather.py`
feeds `src/features`, so all three are cross-package boundaries.

## Proposed boundary-contract blocks (as implemented at 3.5, 2026-09-05)

### `src/external/spaceweather.py` — deliberately OUTSIDE the IRI/GIM restriction

```python
def trailing_mean(daily_values: Mapping[date, float], *, end_day: date,
                  window_days: int) -> float
    # RAISES IntegrityError: a window day missing or NaN (TC-20: never impute the
    # F10.7 outage window). Trailing by construction; future-independence is R-57's
    # tested property. window_days is caller-supplied from its frozen source.

def resolve_f107_at_origin(daily_medians: Mapping[date, float], *, origin: datetime,
                           availability_ts: Callable[[date], datetime],
                           features: Mapping[str, Any]) -> tuple[date, float]
    # RAISES FeatureAvailabilityError: previous-day median unavailable while
    # features.carry_forward_composition is TBD/absent — names origin, last available
    # median's day, staleness in BOTH units (R-57a; D-21/G-04). RAISES IntegrityError
    # on any filled composition value: its application awaits the Student's freeze.

def align_interval_series(observations: Sequence[Mapping[str, Any]])
        -> dict[datetime, float]
def assert_alignment(series_id: str, aligned: Mapping[datetime, float],
                     observations: Sequence[Mapping[str, Any]]) -> None
    # RAISES AlignmentError (the shared-base class that owns this unit's two alignment
    # conditions): value outside its own interval; Dst shifted to a neighbouring hour.

def apply_carry_forward(hourly: Mapping[datetime, float | None], *, bound_h: int)
        -> dict[str, Any]  # values / carried_forward_epochs / excluded_epochs
def assert_carry_forward_conservation(values, observations,
                                      carried_forward_epochs) -> None
    # RAISES IntegrityError: any value at an epoch with no observation and no recorded
    # carry-forward; a recorded count that does not reconcile (R-58 limb 3).

def assert_time_indexed_shape(rows) -> None            # RAISES IntegrityError (TC-12)
def assert_identical_across_cells(joined_rows, *, epoch_key, value_key,
                                  cell_key) -> None    # RAISES IntegrityError (TC-12)
def assert_single_grade(series_id, grades) -> None     # RAISES IntegrityError (D-10.1)
def assert_grade_eligible(series_id, grade, *, use) -> None
    # RAISES IntegrityError: provisional barred from modelling_input/frozen_tolerance/
    # g05_regime_count (D-11, D-13); Dst diagnostic-only for modelling_input (TC-11).
def assert_series_provenance(series_id, entry) -> None
    # RAISES IntegrityError: any of the four provenance fields absent; declared status
    # inconsistent with product identity; declared-status-only series without the
    # documented-absence + unverified-status statement, or reported as closed (R-63).
def assert_gfz_cross_products(series_id, *, near_real_time, definitive,
                              emitted) -> None         # RAISES IntegrityError (R-63 c5)
def provenance_stamp(*, source: str, produced_by: str) -> dict[str, str]
    # SD-E-03 producing half; stamp_class="evidentiary", NEVER cryptographic.
def write_driver_manifest(path: Path, *, series_entries, missing_months,
                          produced_by: str) -> Path
    # Two-tier: missing_months machine-readable and non-fatal; provenance omission or
    # inconsistency terminal. Every value through guard_egress; every entry stamped.
def refuse_divergent_rerun(product_path: Path, *, recorded_identity: str,
                           recorded_sha256: str, current_identity: str) -> None
    # SD-E-07 (SEC-A-02 adopted unchanged): on divergence records BOTH identities
    # (incl. version/issue designation) and BOTH hashes; RAISES IntegrityError;
    # never overwrites.
```

### `src/external/iri.py` — importable ONLY by script 04 and `src/evaluation/`

```python
REPORT_CONTENT_AREAS: tuple[str, ...]  # FR-P1-04-15's seven areas, field-by-field
def assert_validation_report(report: Mapping[str, Any], *, report_name: str) -> None
def assert_benchmark_drivers_in_matrix(availability_matrix, *, benchmark_drivers,
                                       report_name) -> None
def evaluate_generation_gates(*, validation_report, report_name,
                              availability_matrix, benchmark_drivers) -> None
def generate_benchmark(*, validation_report, report_name, availability_matrix,
                       benchmark_drivers, injection_mode: bool = False) -> None
    # RAISES BenchmarkError on every attempt today: no passing pre-declared report
    # (R-59 limb 1); missing content area / non-2000 km ceiling / sample set outside
    # 5-10 or not spanning sites, day-night, quiet-disturbed, or unvalidated against
    # the official interface (limb 3); tolerance timestamp not PRECEDING the
    # comparison (limb 2); benchmark drivers absent from the frozen availability
    # matrix or rows missing the CR-2026-08-22-EV-12 evidence shape (limb 4 — D-25
    # carried AS STANDING; its §15.2 amendment NOT treated as granted). The
    # implementation is never silently switched on failure. `iricore` is imported
    # ONLY inside the gated path. Injection mode never generates.
```

### `src/external/gim.py` — importable ONLY by script 04 and `src/evaluation/`

```python
MAP_TO_MAP_STATEMENT: str; SPATIAL_REPRESENTATIVENESS_STATEMENT: str
Q15_CONFIG_KEY = "gim_interpolation_rule"  # a key NAME; the value is Q-15's, UNSET
def interpolation_rule_from(experiment: Mapping[str, Any]) -> str | None
def evaluate_generation_gates(*, interpolation_rule, hand_check, overlap_audit,
                              generation_attempt_utc) -> None
def generate_comparator(*, interpolation_rule, hand_check, overlap_audit,
                        injection_mode: bool = False, now=None) -> None
    # RAISES ComparatorError on every attempt today: Q-15 UNSET (obligation 1 — a
    # mitigation that EXPIRES); hand-check absent, without worked arithmetic, or not
    # PRECEDING generation (obligation 2, EV-11 — retrospective not accepted); overlap
    # audit absent or not PRECEDING generation (R-60's Constraint, Rec 41). Injection
    # mode never generates.
def render_comparison_report(*, comparison, overlap_audit) -> dict[str, Any]
    # The reporting chokepoint: EMITS the map-to-map limitation, the spatial-
    # representativeness mismatch and the gim_network_overlap_flag value ITSELF;
    # RAISES ComparatorError on any comparison with no registered audit result —
    # the trigger is the COMPARISON'S EXISTENCE (Vision §6.10).
```

## Also carried on this record (context, not amendments)

- The four exceptions (`ImportBoundaryError`, `FeatureAvailabilityError`,
  `BenchmarkError`, `ComparatorError`) were declared in `src/data/config.py` per the
  receipted Q1 = A ruling, riding R-01's any-future clause. **`DriverError` was NOT
  declared** (contested upstream — carried Finding 9; recorded in `config.py`'s and
  `spaceweather.py`'s module docstrings).
- A governed commit of this unit's code cites **D-25** (the F10.7 availability
  convention limb 4 leans on, amendment ungranted) and **D-21** (the carry-forward
  composition raise) as touched context.

## Decision requested

Approve, reject, or modify the `component-methods.md` amendment above (and state
whether it is consolidated with the other four owed amendments). Until approved, the
implemented contracts stand as stage-3.5 code whose design authority is this unit's
approved `functional-design`/`nfr-design` artifacts, with the `component-methods.md`
block **owed, not present**.
