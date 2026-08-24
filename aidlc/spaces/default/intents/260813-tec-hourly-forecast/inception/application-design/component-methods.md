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

> ## ⚠ AMENDED 2026-08-23 — `FoldSpec` COULD NOT REPRESENT THE FINAL REFIT
>
> **Superseded, preserved:**
> ```python
> @dataclass(frozen=True)
> class FoldSpec:
>     fold_id: str                 # "F1".."F4"
>     train_end: date
>     validation_month: int
>     embargo_hours: int = 24
>
> def build_folds(snapshot: ConfigSnapshot) -> Sequence[FoldSpec]: ...
> ```
>
> `validation_month: int` is **required**, and the final refit (1 Jan – 30 Nov,
> FR-P1-04-14) has none — so the refit was representable nowhere, and both functions
> taking a `FoldSpec` were closed to it. **December inherited the same gap, and G-06
> depends on the refit.** Found on a backward jump from stage 3.1 after five review
> cycles; see § The `src/features` leakage boundary and **ADR-11**.

```python
class PartitionKind(StrEnum):
    fold = "fold"
    refit = "refit"
    locked = "locked"


@dataclass(frozen=True)
class Partition:
    partition_id: str                 # "F1".."F4", "REFIT", "DEC"
    kind: PartitionKind
    train_end: date
    validation_month: date | None     # None for REFIT alone; DEC carries 2022-12-01
    embargo_hours: int = 24


def build_partitions(snapshot: ConfigSnapshot) -> Sequence[Partition]: ...


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

> ## ⚠ SIX PARTITIONS, FIVE MANIFEST ROWS — AMENDED 2026-08-23 (M5)
>
> **Superseded, preserved:** `validation_month: date | None  # None for refit and locked`.
>
> **Two distinct defects, one line apart.**
>
> **1. The locked partition could not say which month it evaluates.** `DEC` carried
> `validation_month = None`, so the one partition whose whole purpose is a named
> evaluation month was the one that could not name it. `None` now means **the final
> refit alone** — which genuinely has no validation month (FR-P1-04-14: selected
> configuration refit on January–November, scored nowhere) — and `DEC` carries
> **2022-12-01**. This is also what makes the *"exactly one evaluation role per
> month"* assertion walk **one** list and terminate: Apr → F1, Jul → F2, Oct → F3,
> Nov → F4, Dec → DEC, `None` → REFIT.
>
> **2. Six `Partition` objects against a criterion that says five.** FR-P1-04-5's
> acceptance criterion reads, verbatim: *"No window crosses a boundary; the split
> manifest records the excluded count and **enumerates all five partitions**; a refit
> executed before the freeze fails rather than proceeding."* The five are the four
> folds **and the final refit** — the requirement text names them as *"F1: Jan–Mar/Apr;
> F2: Jan–Jun/Jul; F3: Jan–Sep/Oct; F4: Jan–Oct/Nov; December locked"* plus *"The
> partition list also carries `Final refit: 1 Jan – 30 Nov`"*. December is **locked**,
> not a manifest row.
>
> **The rule, stated so the two counts cannot be confused again:**
>
> | Artifact | Contents | Count |
> |---|---|---|
> | `build_partitions(snapshot)` return value | `F1`–`F4`, `REFIT`, `DEC` | **6** — every partition any code path needs to name |
> | The **split manifest** FR-P1-04-5 gates on | `F1`–`F4`, `REFIT`, each with its training range, validation month and excluded count | **5** |
> | The locked partition record | `DEC`, its evaluated month (2022-12-01), and its access-gate state | recorded **separately**, because it is access-gated and the manifest is not |
>
> A split manifest carrying six rows **fails** FR-P1-04-5, and so does one carrying
> four. `DEC` appearing in `build_partitions`'s list is not a manifest row and must
> never be written as one: the manifest is reviewed at a gate where December's
> evaluation is not yet permitted to exist.
>
> Raised by the re-entry advisory review as finding 5; resolved under the owner's
> 2026-08-23 ruling.

```python
def assert_membership_from_timestamps(frame: DataFrame) -> None: ...
```
Partition membership derives from record timestamps, never from a
directory name or filename. **Raises** on any row whose month or year disagrees
with its partition — the defect that filed locked-month records into
`audit_evidence_2022-01/`.

> **What this does NOT do, stated 2026-08-23 because stage 3.1 twice read it as more
> than it is.** It returns `None`. It **validates** a row against the partition the row
> is already filed under; it **derives nothing** and yields no per-row label. No
> derivation is possible: the training ranges **nest**, so a 15 February row belongs to
> five of the six partitions at once. Any leakage check that needs to know "which
> partition" must compare **declared identities** (`FrameSpec.partition_id` against
> `Transform.partition_id`), which is what the redesigned `src/features` boundary does.
>
> **Vision §8.1's *"each target timestamp belongs to exactly one partition"* therefore
> cannot run over the training ranges either.** It holds over each month's **evaluation
> role** — Apr (F1), Jul (F2), Oct (F3), Nov (F4), December (locked), training-only for
> the rest — which is disjoint by construction. **This is a reading of a frozen Vision
> rule and is carried to the gate**, not settled here; if §8.1 is meant literally over
> the training ranges it is unsatisfiable as written.

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

## The `src/features` leakage boundary — redesigned 2026-08-23

> **⚠ THE SUPERSEDED INTERFACE, PRESERVED, AND WHY IT COULD NOT WORK**
>
> ```python
> def build_features(target, *, drivers, registry, matrix,
>                    fold: FoldSpec, snapshot) -> tuple[DataFrame, NDArray]: ...
> def fit_transforms(train: DataFrame, *, fold: FoldSpec) -> Transform: ...
> def apply_transforms(frame: DataFrame, *, transform: Transform) -> DataFrame: ...
> ```
>
> It claimed: *"A single `fit_transform(all_data)` is unrepresentable in this
> interface, which is how NFR-LEAK-01 is enforced by shape rather than by review."*
> **It is not.** `train` is an unconstrained `DataFrame`, so `fit_transforms(all_data,
> fold=F1)` type-checks — and stage 3.1 then spent **five adversarial review cycles**
> failing to close the gap from below. Three defects, each verified directly:
>
> 1. **`build_features` had no row selector** — no way to ask for a partition's
>    training rows as distinct from its validation month.
> 2. **`apply_transforms` had no way to reject a wrong-partition frame.** Every
>    row-level rule tried was defeated by the fact that the training ranges **nest**:
>    Jan–Mar ⊂ Jan–Jun ⊂ Jan–Sep ⊂ Jan–Oct ⊂ Jan–Nov. F4's transform applied to April
>    passed every containment test, and F4's fit saw April.
> 3. **Nothing stamped the emitted artifacts**, so provenance could not be checked
>    across the `05` → `06` disk handoff where the actual scoring happens.
>
> The full history is in `application-design-questions.md` § RE-ENTRY and in the five
> preserved reports at `construction/features-and-splits/functional-design/business-logic-model.md`
> § Review.

```python
@dataclass(frozen=True)
class FrameSpec:
    partition_id: str                     # matches Partition.partition_id
    role: Literal["train", "score"]
    scored_start: datetime
    scored_end: datetime


@dataclass(frozen=True)
class Transform:
    transform_id: str
    partition_id: str
    # fitted state is intra-package


@dataclass(frozen=True)
class FeatureBundle:
    matrix: DataFrame
    tensor: NDArray
    spec: FrameSpec
    transform_id: str | None              # None ⇒ untransformed


def build_features(
    target: DataFrame,
    *,
    drivers: Mapping[str, DataFrame],
    registry: Mapping[str, Station],
    matrix: Sequence[AvailabilityRow],
    spec: FrameSpec,
    partitions: Sequence[Partition],
    snapshot: ConfigSnapshot,
    transform: Transform | None = None,
) -> FeatureBundle: ...


def fit_transforms(
    bundle: FeatureBundle,
    *,
    partition: Partition,
) -> Transform: ...
```

> **⚠ `partition` added 2026-08-23 after the re-entry review — the first draft
> reproduced ADR-01's exact error.** It read `fit_transforms(bundle: FeatureBundle)`
> and claimed to raise *"when the bundle's scored range is not its partition's training
> range"*. **That check could not execute**: the argument closure is `matrix, tensor,
> spec, transform_id` / `partition_id, role, scored_start, scored_end, lead_in_hours` —
> **no `Partition`, no `ConfigSnapshot`**, so nothing in scope knows what `F1`'s
> training range *is*. `partition_id` is a **caller-asserted string**, and
> `build_features(spec=FrameSpec("F1", "train", 2022-01-01, 2022-11-30))` would have
> produced a bundle that passes the identity check while carrying all of Jan–Nov.
> The unconstrained argument had **moved**, from `train: DataFrame` to a string, not
> closed. Caught by the advisory reviewer; the same defect class this redesign exists
> to fix, made once more inside the fix.

**`apply_transforms` is removed.** A function that applies a fitted transform to an
arbitrary frame **is** the hole — five cycles of trying to constrain its argument
established that the constraint cannot be expressed over rows. Transforms are now
applied **only** inside `build_features`, which is also the only place both
representations are produced, so a transformed matrix beside an untransformed tensor
is no longer constructible.

**The leak check is an identity, not a containment.** `build_features` **raises
`LeakageError`** when `transform.partition_id != spec.partition_id`. The nesting that
defeated every date-range rule is irrelevant to an id comparison: F4's transform on a
frame whose spec says `F1` fails regardless of which months overlap.

> ## ⚠ ONE ENUMERATED EXCEPTION — `REFIT` → `DEC`, OWNER DECISION 2026-08-23
>
> **The problem.** A pure identity rule raises on `transform.partition_id == "REFIT"`
> against `spec.partition_id == "DEC"` — **which is exactly the G-06 apply.** The
> locked test is scored with the transform fitted on January–November; the only
> alternative a pure identity permits is a `DEC`-stamped transform, i.e. **fitting on
> December**, which is the thing the lock exists to prevent. The first draft of ADR-11
> never said which transform scores December, and Q9–Q12 never asked. Caught by the
> re-entry advisory review.
>
> **The rule, stated as a closed set rather than a softening.** `build_features`
> accepts a transform whose `partition_id` differs from the spec's **only** for the
> pairs in this table, which has exactly one row:
>
> | Transform `partition_id` | Spec `partition_id` | Spec `role` | Why |
> |---|---|---|---|
> | `REFIT` | `DEC` | `score` | The G-06 one-shot evaluation. Fitted Jan–Nov; December is never fitted on. |
>
> **Every other mismatched pair raises.** The permitted pair additionally requires
> `spec.role == "score"` — a `REFIT` transform against a `DEC` **train** frame raises,
> because training on December is the locked-test violation itself.
>
> **What this costs, stated plainly.** The invariant is no longer *"ids must match"*
> but *"ids must match, or be the one enumerated pair"* — strictly weaker, and a
> weaker invariant needs its own evidence. **Negative control:** for every ordered pair
> of partition ids that is **not** this row, a mismatched apply → `LeakageError`,
> asserted by enumeration over the six ids rather than by sampling, so a second
> exception cannot be added without a test failing. **And:** `REFIT` → `DEC` with
> `role="train"` → `LeakageError`.
>
> **December still reaches `apply` only through the guard.** The carve-out permits the
> *pairing*; it grants no access. `splits.materialise_locked_partition` still refuses
> without a verifying `g05_signature` (ADR-03), and `locked_test.open_restricted` still
> logs before every read.

**`fit_transforms` takes a bundle and the `Partition` itself.** It **raises
`LeakageError`** when `bundle.spec.role != "train"`; when `bundle.transform_id is not
None` (already transformed); when `bundle.spec.partition_id != partition.partition_id`;
and — **the check that needs `partition` in scope** — when
`[bundle.spec.scored_start, bundle.spec.scored_end]` is not exactly
`partition`'s training range. The returned `Transform` carries
`partition.partition_id`.

**`build_features` validates the same way, for the same reason.** It takes
`partitions: Sequence[Partition]` and **raises** when `spec.partition_id` names none of
them, or when the spec's scored range is not **contained in** the range its `role`
permits for that partition — the training range for `train`, the
**`validation_month`** for `score`. Without this, `FrameSpec`'s fields are caller
assertions and nothing verifies them, which is precisely how the superseded interface
failed.

> **⚠ Containment, not equality — corrected 2026-08-23.** The first draft required the
> scored range to **equal** `validation_month`. That makes the **walking-skeleton
> fixtures unrepresentable**: D-11 freezes the plumbing window at **2022-11-01 to
> 2022-11-07**, seven days inside F4's validation month, so no legal `score` spec
> existed for **WS-12, WS-13 or WS-20** — the three rows the fixtures evidence. Caught
> by the re-entry advisory review.
>
> **Containment is exact enough**, and this is why: the **validation months are
> disjoint** (Apr, Jul, Oct, Nov, December) even though the training ranges nest. A
> range contained in F4's validation month is in November and nowhere else, so no
> cross-partition scoring becomes representable. The training side is likewise safe —
> `FrameSpec("F1", "train", 2022-01-01, 2022-11-30)`, the Critical-1 case, still
> **raises**, because Nov 30 lies outside F1's training range regardless of
> containment-versus-equality. The identity check does the leakage work; this check
> catches an inconsistent spec.

> ## ⚠ `lead_in_hours` WAS REMOVED — OWNER DECISION, 2026-08-23
>
> **The superseded field and its rationale, preserved.** `FrameSpec` carried
> `lead_in_hours: int = 24`, on the argument that `vtec_seq_24` and `vtec_lag_24h` need
> 24 h **preceding** any scored row, so a `score` frame for December would hold late-
> November rows that are *present but never scored* — making **1 December** scorable.
>
> **Why it is gone.** FR-P1-04-5's acceptance criterion reads, verbatim: *"No window
> crosses a boundary … the first 24 h are excluded and counted."* `lead_in_hours`
> existed **precisely to make a window cross the November/December boundary**, which
> reverses an approved requirement and **enlarges the locked-test scored set**. That is
> supervisor-owned under Vision §8.2 and §8.7 and gate **G-05** — and ADR-11 itself
> states that no ADR here adopts a reading on a supervisor-owned value. Caught by the
> re-entry advisory review; the owner chose to honour FR-P1-04-5 rather than route it
> to the supervisor.
>
> **The consequence, which must be disclosed wherever December coverage is reported:**
> **1 December is not scored.** The locked test covers **30 days, not 31**, and the
> first 24 h of **every** validation month (Apr, Jul, Oct, Nov) are likewise excluded
> and counted. This is the requirement working as approved, not a defect — but a
> December coverage figure that silently reads as 31 days would be wrong.

**`scored_start` / `scored_end` bound exactly what is scored, and nothing precedes
them.** A window that would reach before `scored_start` is **excluded and counted**,
per FR-P1-04-5 and FR-P1-04-13's incomplete-`vtec_seq_24` rule. The excluded-row count
is emitted, never merely dropped — this project's standing rule that a check which
never fired must not look like one that passed.

**The sequence, for any partition *k*** — three calls, each with a stated purpose:

```python
raw   = build_features(..., spec=FrameSpec(k, "train", ...), partitions=P)   # transform_id None
T_k   = fit_transforms(raw, partition=P[k])
train = build_features(..., spec=FrameSpec(k, "train", ...), partitions=P, transform=T_k)
score = build_features(..., spec=FrameSpec(k, "score",  ...), partitions=P, transform=T_k)
```

The **untransformed** `raw` bundle is live in the process, and consuming it for
training or scoring would leak. That is closed by a check, not a convention:
`06_train_and_predict.py` and `07_evaluate_and_report.py` **raise** on any bundle
whose `transform_id is None`.

**Returning `FeatureBundle` is what makes provenance survive `05` → `06`.** The spec
and the transform identity are **the same object** as the data, so they cannot drift
from it the way a side-car manifest can. `06`/`07` assert that a bundle scored for
partition *k* carries `spec.partition_id == k`, `spec.role == "score"`, and the
`transform_id` of *k*'s own transform.

**`build_features` still raises** `LeakageError` on: any field outside the §6.2
dictionary; a carried-forward `vtec_lag_*` value (prohibited — the ≤3 h allowance is
external drivers only); an incomplete `vtec_seq_24` window that was not excluded; a
support field used as an input without a recorded G-04 approval; a target-hour quality
field; a raw-longitude column; a driver carried forward beyond 3 h. **And
`AlignmentError`** on a driver value repeated outside its own defined interval, or
shifted to a neighbouring hour (FR-P1-04-17 / TA-36's enforcement limb; the
no-interpolation limb is a static source check, not a runtime raise).

**Parity is still structural.** Both representations come from **one** window
definition in `windows.py` and now travel in one object, so FR-P1-04-8 holds by
construction rather than by assertion.

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
    partition_id: str            # added 2026-08-23 (ADR-11)
    transform_id: str            # added 2026-08-23 (ADR-11)


def fit_predict(
    model_id: str,
    *,
    bundle: FeatureBundle,
    partition: Partition,
    snapshot: ConfigSnapshot,
) -> Prediction: ...


def three_seed_mean(
    predictions: Sequence[Prediction],
    *,
    expected_seeds: frozenset[int],
) -> Prediction: ...
```
**`Prediction` carries `partition_id` and `transform_id`** (added 2026-08-23), copied
from the bundle it was produced from. Without them the provenance `FeatureBundle`
established dies at `06`: `07` receives predictions, not bundles, and could not tell
which partition's transform produced the numbers it is about to score. The stamp has
to travel the **whole** way, not just to the first consumer.

**`inverse_transform` is required, and `apply_transforms`'s removal did not delete
it.** TE §7.2's `ABL-DIFF` *"inverse-transforms to absolute TECU before any metric"*,
and `src/evaluation` must be able to do that without importing `src/features` — an
edge the dependency matrix does not carry and should not gain. The inverse is
therefore a **method on `Transform`** (`Transform.inverse(frame) -> DataFrame`), which
travels with the `Prediction`'s `transform_id` and needs no new package edge. This is
distinct from the removed `apply_transforms`: an inverse maps model output back to
TECU and can leak nothing, because it consumes predictions rather than producing
training input.

**Amended 2026-08-23 with the leakage boundary.** `fit_predict` previously took
`features: DataFrame, tensor: NDArray, fold: FoldSpec` — three parameters a caller
could assemble inconsistently, and none of which carried provenance. It now takes the
**`FeatureBundle`**, so the two representations arrive together as `build_features`
emitted them, and it **raises `LeakageError`** when `bundle.transform_id is None` —
an untransformed bundle reaching training is the leak the three-call sequence would
otherwise leave live. `partition: Partition` replaces `fold: FoldSpec` so the refit
and the locked month are expressible.

Q6's confirmatory-prediction rule. `three_seed_mean` **verifies sample alignment
explicitly** before averaging and **raises** `AlignmentError` when the three
frames do not share an identical index — averaging misaligned predictions
silently is the failure this check exists for. It **raises** `SeedError` when
given fewer than three predictions or when their seeds are not exactly
`expected_seeds`: selecting a best seed, or substituting a single-seed
prediction, is rejected here rather than left to review. The individual
predictions are preserved by the caller; this function does not discard them.

> **⚠ `expected_seeds` ADDED 2026-08-23 — THE CHECK COULD NOT EXECUTE (BLK-03).**
>
> **Superseded, preserved:** `def three_seed_mean(predictions: Sequence[Prediction]) -> Prediction: ...`
>
> The prose already claimed a raise *"when their seeds are not exactly the frozen
> set"*, but the frozen set — `{1337, 2024, 7}` (D-122, restated at
> `requirements.md` FR-P1-05-2) — appeared in **no argument**. Only two
> implementations existed, and both were wrong:
>
> 1. **Inline `{1337, 2024, 7}` inside `src/models`** — precisely the pattern TC-03e
>    and `project.md` § Forbidden prohibit ("NEVER hide a scientific constant in
>    source code or a notebook"); every scientific constant lives in `seeds.yaml`.
> 2. **Weaken to "exactly three, pairwise distinct"** — which passes a
>    wrong-but-distinct triple undetected, and is not the stated rule.
>
> `expected_seeds` is read from `ConfigSnapshot.seeds` at the call site, so the
> comparison is against the configured value and the constant is never inlined.
> This is the shape `vector_block_bootstrap(seed: int)` a few sections below
> already uses, for the identical reason — the omission here was an inconsistency
> rather than a considered difference. Raised by the advisory reviewer as prior
> finding 1, carried unresolved through the ADR-11 re-entry as **BLK-03**, and
> resolved here under the owner's 2026-08-23 ruling.

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

---

*Finalized 2026-08-23 under the stage's revision-4 completion pass. Two signature
gaps go to the approval gate unresolved: `Transform.inverse` is specified as
reachable from `Prediction.transform_id`, a `str`, with no lookup named (Critical);
and `Partition` carries no `train_start`, so the training-range comparisons in
`fit_transforms` and `build_features` rest on an unwritten January-1 convention
(Major).*
