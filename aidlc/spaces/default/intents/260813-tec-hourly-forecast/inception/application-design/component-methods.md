# Component Methods — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.6 (application-design), intent `260813-tec-hourly-forecast`.

## Sources

- Requirements: `../requirements-analysis/requirements.md`.
- Affirmed practices: `../practices-discovery/team-practices.md` — `snake_case`,
  a module docstring stating purpose, inputs and re-run behaviour, and the
  two-tier error posture (integrity violations exit; completeness shortfalls are
  recorded as machine-readable fields).
- Authority: TE v3.3 §12, §13.1–13.7, §6.2; Vision v4.3 §6, §8.
- Stage answer **Q1 = B**, which sets this document's depth.

## Depth, and why

**Full signatures with types for cross-package boundary calls. Names and one-line
purposes for intra-package functions.** Q1 = B.

The reason is empirical rather than stylistic: every defect this project's
governance has actually caught travelled across a package boundary — IRI reaching
features, a raw-processing module reachable from Phase 1, a carried-forward lag
reaching the model, a benchmark whose drivers were never in the availability
matrix. Those are the contracts worth fixing before Construction. Intra-package
shapes are cheap to change at `functional-design` (3.1) and expensive to guess
today.

Conventions used below:

- Type hints are PEP 604 (`X | None`), with `from __future__ import annotations`
  assumed per the team's affirmed typing convention.
- `Path` is `pathlib.Path`. `DataFrame` is `pandas.DataFrame`. `NDArray` is
  `numpy.typing.NDArray`.
- **Raises** lists only integrity failures, which terminate the run with a
  message naming the file and the violated expectation. Completeness shortfalls
  return a machine-readable field instead and never raise.
- Every signature below is a **cross-package boundary**. Intra-package helpers
  appear as names only, in the tables at the end of each section.

---

## `src/data/config.py` — **NEW** (Q2 = B)

The only module that reads `configs/`. Everything downstream receives resolved
values, never a path into `configs/`.

```python
@dataclass(frozen=True)
class ConfigSnapshot:
    data: Mapping[str, object]           # configs/data.yaml, parsed
    features: Mapping[str, object]       # configs/features.yaml
    experiment: Mapping[str, object]     # configs/experiment.yaml
    seeds: Mapping[str, object]          # configs/seeds.yaml
    hashes: Mapping[str, str]            # filename -> sha256, all four
    snapshot_dir: Path                   # where the verbatim copies were written
    resolved_roots: Mapping[str, Path]   # platform roots actually used (Q7)
    platform: str                        # "kaggle" | "local"


def load_configs(config_dir: Path, *, phase: int) -> ConfigSnapshot: ...
```
Loads all four files, copies them verbatim into the run's snapshot directory,
hashes each, resolves platform roots, and returns the frozen snapshot.
**Raises** `ConfigError` when a file is missing, unparseable, or when
`phase` is not `1` or `2`.

```python
def assert_no_tbd(snapshot: ConfigSnapshot, *, required: Sequence[str]) -> None: ...
```
Asserts no field named in `required` is `TBD` in any of the four configs — the
§18.3 zero-`TBD` precondition. **Raises** `PreflightError` naming every offending
field, so a run reports all of them rather than the first.

```python
def assert_declared_sources_exist(snapshot: ConfigSnapshot) -> None: ...
```
The §18.3 clause restored by `DATA-13`: every declared source and hash resolves.
**Raises** `PreflightError` naming each unresolved declaration. A declared hash
that does not resolve is a failure, never a warning.

```python
def resolve_platform_roots(env: Mapping[str, str]) -> tuple[str, Mapping[str, Path]]: ...
```
Q7 = C. Reads roots from the environment, returns the platform label and the
resolved roots. **No credential is returned or logged** — credentials stay in the
environment and reach the provider client directly (§10). **Raises**
`PlatformError` when the platform cannot be identified as exactly one of the two
authorised (TC-03c).

### Determinism helper (Q6 = X), same module

```python
@dataclass(frozen=True)
class DeterminismRecord:
    seeds_applied: Mapping[str, int]        # e.g. {"python": 42, "numpy": 42, "tensorflow": 42}
    pythonhashseed: str                     # the value in force, read from os.environ
    reexec_performed: bool                  # FU-1: True when the script re-exec'd itself
    framework_versions: Mapping[str, str]   # python, numpy, tensorflow, ...
    tf_op_determinism: bool                 # enable_op_determinism() succeeded
    nondeterministic_ops: Sequence[str]     # operations determinism is NOT guaranteed for


def seed_everything(snapshot: ConfigSnapshot, *, stage: str) -> DeterminismRecord: ...
```
Applies the `seeds.yaml` values to Python, NumPy and TensorFlow, enables
TensorFlow op determinism **before any graph construction**, and returns the
record for the environment lock and the experiment registry. **Raises**
`DeterminismError` when TensorFlow has already been initialised — the check Q6
names, because enabling op determinism afterwards is not equivalent. **Does not**
touch the bootstrap seed: that carve-out is `src/evaluation/bootstrap.py`.

```python
def ensure_process_determinism(argv: Sequence[str]) -> None: ...
```
FU-1 = D. When `PYTHONHASHSEED` is unset, re-execs the current interpreter with
it set and the same argv, so the guarantee holds for a directly invoked script.
When already set, returns immediately. **The re-exec is recorded** in
`DeterminismRecord.reexec_performed` and in the run log, so it is never mistaken
for a double run. Called as the **first statement** of every stage script's
`main()`, before any framework import.

| Intra-package helper | Purpose |
|---|---|
| `_parse_yaml` | Strict YAML load, duplicate-key rejection. |
| `_write_snapshot` | Verbatim copy of the four files into the run directory. |
| `_flatten_for_tbd_scan` | Walks nested config structures for the `TBD` scan. |

---

## `src/data/phase_contract.py` — the phase boundary (Q3 = B)

```python
RAW_MODULES: Final[frozenset[str]] = frozenset({
    "src.gnss.rinex", "src.gnss.calibration",
    "src.gnss.target", "src.gnss.verification",
})


def assert_phase_boundary(phase: int, *, loaded_modules: Mapping[str, object]) -> None: ...
```
Q3 = B. Given `phase == 1`, asserts no name in `RAW_MODULES` is present in
`loaded_modules` (normally `sys.modules`) and **refuses to proceed** otherwise.
Called at entry by every phase-aware stage script, so the prohibition holds
inside the Kaggle session where a commit hook cannot fire. **Raises**
`PhaseBoundaryError` naming the offending module.

`RAW_MODULES` names all four `gnss` modules, not the two `src/gnss/rinex.py` and
`calibration.py` that FR-P1-03-2's earlier wording listed — `target.py` and
`verification.py` are raw-processing adapters and were explicitly added to the
prohibition per finding `IMPL-2`.

```python
def assert_no_raw_fields(frame: DataFrame, *, phase: int) -> None: ...
```
The **produced-field limb**, separately checkable per FR-P1-03-2's requirement of
two independent results. Rejects a Phase 1 artifact carrying a DCB, STEC,
mapping, satellite or arc field. **Raises** `PhaseBoundaryError` naming the
field. Neither this nor `assert_phase_boundary` substitutes for the other.

```python
@dataclass(frozen=True)
class TransitionManifest:
    protected_hashes: Mapping[str, str]   # exactly the canonical protected set
                                          # derived from TE §2.2 u §7.0B. Final
                                          # enumeration and cardinality are
                                          # DEFERRED TO STAGE 3.1; this design
                                          # states neither. See BLK-06 in
                                          # unit-of-work.md
    phase1_artifacts: Mapping[str, str]   # artifact id -> sha256, evidence-backed
    phase1_schema: Sequence[str]          # the OBSERVED Phase 1 columns, D-17
    config_hashes: Mapping[str, str]
    approved_decisions: Sequence[str]     # D-numbers this handoff rests on
    invariants: Sequence[str]             # what Phase 2 must preserve
    unresolved_phase2: Sequence[str]      # named, never invented


def build_transition_manifest(
    snapshot: ConfigSnapshot,
    *,
    artifacts: Mapping[str, Path],
) -> TransitionManifest: ...


def diff_protected_hashes(
    frozen: TransitionManifest, current: TransitionManifest
) -> Mapping[str, tuple[str, str]]: ...
```
Q8 = B. The manifest **is** the Phase 1 → Phase 2 interface — an artifact and
data contract, not a call surface. `phase1_schema` records the **observed**
five-column product; the Phase 2 ten-field contract is not represented here and
is not imposed on it. `unresolved_phase2` names open Phase 2 decisions rather
than freezing unsupported values. `diff_protected_hashes` returns the differing
keys with both values; an empty mapping is the G-P3C pass condition, and its
`protected_hashes` key list is asserted equal to **the canonical protected set
derived from the union of TE §2.2 and TE §7.0B**, so a short list cannot pass
silently. **The final enumeration and its cardinality are deferred to stage 3.1
(`functional-design`); this design states neither, and no number is carried into
this artifact.** The assertion is only as strong as the canonical set behind it,
and that set is not yet established: `requirements.md` FR-P1-06-1 carries the
current approved candidate list, but its derivation from §7.0B is incomplete —
`history window`, `station encoding` and `baselines` are named immutable in
§7.0B and appear in none of its items, with no deduplication or subsumption rule
recorded anywhere. Until `functional-design` (3.1) discharges **BLK-06**
(`unit-of-work.md` § Blocker register), an empty `diff_protected_hashes` result
must not be read as proof that no protected item changed. Annotated 2026-08-22
per governance finding `UG-01` (`GOV-2026-08-21-UG-01`), on the authorized
project decision owner's directive; no scientific value and no design decision
changed, and no replacement number was invented.

---

## `src/data/locked_test.py` — **NEW** (Q4 = C, FU-2 = A)

The **path guard**: one chokepoint for every read under the restricted root. The
execution guard is `splits.py`; the two obligations stay separate because the
pre-G-05 coverage audit is a *required read* while the metrics run is *barred*
until after G-05.

```python
RESTRICTED_ROOT: Final[str] = "evidence/locked_test_restricted"


@dataclass(frozen=True)
class AccessRecord:
    run_id: str
    retrieved_at_utc: str
    scope: str                  # e.g. "December 2022, ARUC/BSHM/NICO cells"
    purpose: str                # "coverage_audit" | "regime_audit" | "locked_evaluation"
    performance_inspected: bool
    locked_test_accessed: bool   # always True for any read under RESTRICTED_ROOT
    authorization: str           # the G-05 signature reference, or the audit authority


def open_restricted(
    path: Path,
    *,
    record: AccessRecord,
    registry: Path,
) -> Path: ...
```
Writes `record` to the access log **and flushes it** before returning the path
for reading. Log-then-read ordering is the requirement (`VAL-2`, FR-P1-02-3): an
access recorded after the fact fails the ordering check rather than satisfying
it. **Raises** `LockedTestError` when `path` is not under `RESTRICTED_ROOT`
(callers must not route ordinary reads through the guard), or when the registry
write fails — a failed log write must abort the read, not proceed unlogged.

```python
def assert_no_december_outside_restricted(evidence_root: Path) -> Sequence[Path]: ...
```
FR-P1-02-6's regression guard, retained after D-15 relocated 21 files. Walks
`evidence/` **recursively** and returns any December-bearing artifact found
outside the restricted root. An empty sequence is the pass condition. Recursive
by construction, because `DATA-01` showed a non-recursive glob silently stopped
checking the artifacts that matter most.

---

## `src/data/splits.py` — partitions and the execution guard

```python
@dataclass(frozen=True)
class FoldSpec:
    fold_id: str                 # "F1".."F4"
    train_end: date
    validation_month: int
    embargo_hours: int = 24


def build_folds(snapshot: ConfigSnapshot) -> Sequence[FoldSpec]: ...


def materialise_locked_partition(
    snapshot: ConfigSnapshot,
    *,
    g05_signature: str | None,
) -> DataFrame: ...
```
Q4 = C's execution half. The December partition materialises **only** when
`g05_signature` is present and verifies. **Raises** `LockedTestError` when it is
`None` or fails verification — that is the pre-G-05 execution block WS-18
evidences. A *read* for the required coverage audit does not come through here;
it comes through `locked_test.open_restricted`, which is why the two are
separate functions in separate modules.

```python
def assert_membership_from_timestamps(frame: DataFrame) -> None: ...
```
Fold and partition membership derives from record timestamps, never from a
directory name or filename. **Raises** on any row whose month or year disagrees
with its partition — the defect that filed locked-month records into
`audit_evidence_2022-01/`.

---

## `src/data/release.py` — releases and hashing

```python
def sha256_file(path: Path) -> str: ...
```
The single project-wide SHA-256 helper. The team practice consolidates three
copies here; the notebook copy is removed rather than left as a fourth.

```python
def write_release(
    manifest: Mapping[str, object],
    *,
    files: Mapping[str, Path],
    out_dir: Path,
) -> Path: ...
```
Writes an immutable release carrying **all fourteen** TE §13.3 fields across its
ten manifest rows. `source_files`' own six items are validated against
`inventory.py` rather than restated as a bare hash. **Raises** `ReleaseError`
when a field is absent or when `out_dir` already holds a release — a release is
write-protected or stored under a new version, never overwritten.

```python
def verify_release(manifest_path: Path) -> Sequence[str]: ...
```
Returns the names of files whose hash does not match. Empty means verified.

---

## `src/data/registry.py` — station registry

```python
@dataclass(frozen=True)
class Station:
    station_id: str                    # "ARUC" | "BSHM" | "NICO"
    lat: float
    lon: float
    ellipsoidal_height_m: float
    domes: str
    receiver_intervals: Sequence[tuple[date, date, str]]
    antenna_intervals: Sequence[tuple[date, date, str]]
    firmware_intervals: Sequence[tuple[date, date, str]]
    sampling_interval_s: int
    observable_codes: Sequence[str]
    hardware_changes_2022: Sequence[tuple[date, str]]
    igrf_version: str                  # pinned, never defaulted
    cell: tuple[int, int]              # (floor(lat), floor(lon)), half-open, D-1


def load_registry(snapshot: ConfigSnapshot) -> Mapping[str, Station]: ...


def assert_registry_resolved(registry: Mapping[str, Station]) -> None: ...
```
FR-P1-02-1 and FR-P1-02-7. `assert_registry_resolved` **raises**
`RegistryError` when any §6.2 field is missing, when `igrf_version` is a default
rather than a pin, or when a conflict was resolved by averaging — *"A conflict
must be resolved and recorded, never averaged or ignored."* An unresolved registry
**blocks** `station_lat` and excludes `lst_sin`/`lst_cos`, so
`features.build` calls this before constructing either.

---

## `src/features` — boundary calls

```python
@dataclass(frozen=True)
class AvailabilityRow:
    feature: str
    observation_timestamp: str
    publication_timestamp: str
    release_status: str          # "real-time" | "provisional" | "final"
    safe_lag_hours: float
    actual_lag_hours: float


def build_availability_matrix(
    snapshot: ConfigSnapshot, *, drivers: Mapping[str, DataFrame]
) -> Sequence[AvailabilityRow]: ...


def assert_lags_safe(matrix: Sequence[AvailabilityRow]) -> None: ...
```
**Raises** `LeakageError` when any row has `actual_lag_hours <
safe_lag_hours`, when a driver's `release_status` indicates a backfilled final
value where the contemporaneous grade was required, or when `f107_81_trailing`'s
window does not **end at the safe-lagged day** — the anchor `TEC-13` restored.

```python
def build_features(
    target: DataFrame,
    *,
    drivers: Mapping[str, DataFrame],
    registry: Mapping[str, Station],
    matrix: Sequence[AvailabilityRow],
    fold: FoldSpec,
    snapshot: ConfigSnapshot,
) -> tuple[DataFrame, NDArray]: ...
```
Returns the flattened matrix and the sequence tensor from **one** window
definition (`windows.py`), so FR-P1-04-8's parity is structural rather than
asserted. **Raises** `LeakageError` on: any field outside the §6.2 dictionary; a
carried-forward `vtec_lag_*` value (prohibited — the ≤3 h allowance is external
drivers only); an incomplete `vtec_seq_24` window that was not excluded; a
support field used as an input without a recorded G-04 approval; a target-hour
quality field; a raw-longitude column; a driver carried forward beyond 3 h.

```python
def fit_transforms(train: DataFrame, *, fold: FoldSpec) -> Transform: ...
def apply_transforms(frame: DataFrame, *, transform: Transform) -> DataFrame: ...
```
Two functions, deliberately. Fitting takes only the training partition and the
fold; applying takes a fitted transform. A single `fit_transform(all_data)` is
unrepresentable in this interface, which is how NFR-LEAK-01 is enforced by shape
rather than by review.

---

## `src/models` — boundary calls

```python
@dataclass(frozen=True)
class Prediction:
    model_id: str                # "M-01".."M-06"
    seed: int | None             # None for unseeded models
    frame: DataFrame             # station, interval_start_utc, y_hat
    target_definition_id: str
    phase_id: str
    source_id: str


def fit_predict(
    model_id: str,
    *,
    features: DataFrame,
    tensor: NDArray,
    fold: FoldSpec,
    snapshot: ConfigSnapshot,
) -> Prediction: ...


def three_seed_mean(predictions: Sequence[Prediction]) -> Prediction: ...
```
Q6's confirmatory-prediction rule. `three_seed_mean` **verifies sample alignment
explicitly** before averaging and **raises** `AlignmentError` when the three
frames do not share an identical index — averaging misaligned predictions
silently is the failure this check exists for. It **raises** `SeedError` when
given fewer than three predictions or when their seeds are not exactly the
frozen set: selecting a best seed, or substituting a single-seed prediction, is
unrepresentable here. The individual predictions are preserved by the caller;
this function does not discard them.

```python
def climatology_fit_partition(prediction: Prediction) -> Sequence[str]: ...
```
FR-P1-05-21. Returns the partition identifiers M-03 was actually fitted on, so
the negative case — a climatology fitted across all of 2022 — **fails** a test
rather than passing a module inventory.

---

## `src/evaluation` — boundary calls

```python
def build_comparison_mask(
    predictions: Sequence[Prediction], *, benchmark: Prediction
) -> DataFrame: ...
```
One comparison-wide intersection mask, computed **once** per comparison set.
**Raises** `FairnessError` if called per-pair, detected by the caller passing
fewer than the full comparison set.

```python
def paired_loss_differential(
    model: Prediction, benchmark: Prediction, *, mask: DataFrame
) -> tuple[float, Mapping[str, float]]: ...
```
Mean within-station difference of squared errors, **benchmark minus model**,
equal-station weighting; positive favours the model. Returns the scalar and the
per-station components. The sign convention is stated in every table that
reports it (FR-P1-05-7).

```python
def vector_block_bootstrap(
    model: Prediction,
    benchmark: Prediction,
    *,
    mask: DataFrame,
    block_hours: int = 24,
    replicates: int = 10_000,
    seed: int,
) -> BootstrapResult: ...
```
Q6's carve-out. `seed` is **required and passed in** — read from `seeds.yaml`
(TE §13.5), never defaulted and never inlined, satisfying TC-03e. The function
builds **its own local generator** from it, so changing a model seed cannot
change a bootstrap draw. **Raises** `BootstrapError` when a block does not carry
all three stations at the same timestamps, when a paired prediction is missing
and no declared rule handled it, or when the resulting interval is **narrower**
than a naive within-station bootstrap on the same data — the widening control,
which is what makes the other checks sufficient.

```python
def count_storm_events(
    kp: DataFrame,
    *,
    release_grade: str,
    source: str,
) -> tuple[int, Sequence[tuple[str, str]]]: ...
```
`release_grade` and `source` are **required arguments, not inferred**, so the
§9.3 count cannot be computed from an unrecorded or provisional-Dst-derived
series without that appearing at the call site. **Raises** `RegimeError` when
`source` is not GFZ Kp/Hp60 or when `release_grade` is absent.

*This is as far as design can carry the open advisory finding.* FR-P1-05-18 has
no criterion testing the count's source; making the source an explicit parameter
means a test *can* assert it, but writing that criterion is a `requirements.md`
change and is not in this stage's produces list.

## Assumptions & Open Questions

- **[assumption]** `ConfigError`, `PreflightError`, `PlatformError`, `DeterminismError`, `PhaseBoundaryError`, `LockedTestError`, `ReleaseError`, `RegistryError`, `LeakageError`, `AlignmentError`, `SeedError`, `FairnessError`, `BootstrapError` and `RegimeError` are project-defined exceptions in a shared base. §12 names no exceptions module; they are declared where raised until 3.1 places them.
- **[Q1]** Intra-package helper names are indicative. `functional-design` (3.1) specifies them per unit and may rename freely — only the signatures above are contracts.
- **Open.** `Transform` and `BootstrapResult` are referenced as types and left unspecified: both are intra-package shapes under Q1 = B.
- **None** of the signatures above encodes a scientific constant. Every threshold, seed, grid and window length arrives through `ConfigSnapshot`.
