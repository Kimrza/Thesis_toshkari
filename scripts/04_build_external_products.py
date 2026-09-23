"""Stage script 04: external products -- drivers audited, benchmark and comparator refused.

Purpose
-------
The fifth of the nine phase-aware stage scripts (TE 12/13.2; `services.md` section The
nine stage scripts -- P1-04). It ORCHESTRATES `src/external/spaceweather.py`,
`src/external/iri.py` and `src/external/gim.py` (W-5 ... W-8): the driver-series audit
with its two-tier manifest, and the IRI-benchmark and GIM-comparator generation
attempts, BOTH OF WHICH REFUSE TODAY -- the refusals are the deliverable (R-59's
validation has not run; Q-15's interpolation rule is UNSET). This script and modules
under `src/evaluation/` are TE 12's ONLY permitted importers of `iri` and `gim`; both
imports are deferred inside the attempt paths, so the default driver-audit path never
loads the guarded modules at all.

What this script can and cannot run today
-----------------------------------------
* **The driver-audit path runs** (default): `audit_ec1_drivers.py`'s logic is MIGRATED
  here (W-8), gaining `--config configs/` and its numbered position; the original is
  left untouched this run and its retirement is a gate item. The `:184` unconditional
  `return 0` is CLOSED onto the two-tier posture (R-61, REQ-ENG-9): a missing month is
  a completeness shortfall, recorded as a machine-readable manifest field NAMING which
  months, non-fatal; a hash mismatch against the previously recorded audit report is an
  integrity violation, terminating non-zero and naming the file and the violated
  expectation. Every output value routes through acquisition's `guard_egress` and
  carries a provenance stamp (SD-E-03's producing half, evidentiary not cryptographic).
* **`--attempt-benchmark` REFUSES**, naming the missing passing pre-declared validation
  report (R-59; BenchmarkError; the aborted registry row records the refusal honestly).
* **`--attempt-comparator` REFUSES**, naming Q-15's unset Student-owned interpolation
  rule (R-60 obligation 1; ComparatorError).
* `--gate-state <json>` on either attempt runs the SAME gates over INJECTED state as a
  negative control; a state satisfying every gate still refuses (injection mode never
  generates -- injected state is not governed evidence).

Scope notes
-----------
The audit reads DRIVER evidence only (Kyoto Dst monthly tables, NRCan `fluxtable.txt`)
under `evidence/audit_ec1_2026-08-15/` -- exactly the files the original approved script
reads today, including the December Dst table that the original's own report covers. It
touches no VTEC target, computes no model-relevant statistic, and never constructs a
path into the December-target custody root (D-15) -- this script does not even name
that root's path (R-28's one-door property). The
audit window is calendar 2022, the migrated original's own window and D-8's frozen
claim boundary; the F10.7 outage-start date 2022-03-18 is the measured fact the
original recorded, preserved as-is by the migration.

Inputs
------
`--config configs/` (the four governed configs, read only through `load_configs`);
`--phase 1|2` (phase-aware per 13.2; every path below is phase-1-legal);
`--evidence-root` (workspace-relative driver-evidence directory, default
`evidence/audit_ec1_2026-08-15`); `--out` (workspace-relative manifest output,
default `artifacts/external/ec1_driver_audit_manifest.json`); `--code-commit`
(explicit commit for the environment lock where no git tree exists -- Kaggle, or a
temporary smoke workspace); `--attempt-benchmark` / `--attempt-comparator` /
`--gate-state`.

Re-run behaviour
----------------
Each run appends its own `started` and terminal rows to the experiment registry
(append-only, R-08/R-09; failed and aborted runs stay visible, NFR-AUD-01). The driver
audit is a pure function of the evidence bytes: re-running against the same files
reproduces the same manifest content (modulo the stamp timestamp). A re-run against
CHANGED evidence bytes terminates on the hash check (SD-E-07's posture: byte-identical,
or explicitly divergent and refused).

Boundaries this script holds
----------------------------
* Step 1 of the entry contract is `ensure_process_determinism`; `assert_phase_boundary`
  is step 4; `assert_no_raw_fields` runs BEFORE the first write (R-23/R-24).
* `iri`/`gim` imports are DEFERRED inside the attempt paths (plan Step 3: the `iricore`
  import lives inside iri.py's gated path only; deferring here keeps the default path
  from loading the guarded modules).
* Every output value routes through `guard_egress` inside the library writer; no
  credential, token or signed URL enters any output (NFR-SEC-01).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
import uuid
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Final

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import (  # noqa: E402
    IntegrityError,
    assert_declared_sources_exist,
    assert_lock_complete,
    assert_no_tbd,
    capture_environment_lock,
    ensure_process_determinism,
    environment_lock_hash,
    load_configs,
    required_fields_for,
    seed_everything,
)
from src.data.experiment_registry import (  # noqa: E402
    append_registry_event,
    record_abort_honestly,
)
from src.data.fixture_gate import require_receipts_for_snapshot  # noqa: E402
from src.data.fixture_manifest import (  # noqa: E402
    WALKING_SKELETON_ROOT,
    load_fixture_scope,
)
from src.data.phase_contract import assert_no_raw_fields, assert_phase_boundary  # noqa: E402
from src.data.prepared import resolve_target_identity  # noqa: E402
from src.data.release import (  # noqa: E402
    MANIFEST_NAME,
    ReleaseError,
    content_hash_of,
    sha256_of_file,
    write_release,
)
from src.external.spaceweather import write_driver_manifest  # noqa: E402

STAGE = "external-products"
PHASE_DEFAULT = 1

#: The NON-FIXTURE audit window: calendar 2022, migrated unchanged from
#: `audit_ec1_drivers.py` and matching D-8's frozen claim boundary ("calendar year
#: 2022"). The migration preserves the original's window identity; it decides no new
#: scientific value. On a fixture run the audit window is the fixture scope's cited
#: window instead (CR-2026-09-13-04-FIXTURE-WINDOW, owner-ruled Option a): the
#: declaration is made true by narrowing the READS, never by narrowing the report.
_AUDIT_YEAR = 2022

#: The non-fixture default manifest path (the pre-repair `--out` default, unchanged).
_DEFAULT_OUT = Path("artifacts/external/ec1_driver_audit_manifest.json")

#: The F10.7 outage-window start the ORIGINAL audit measured and recorded
#: (2022-03-18); preserved by the migration as the recorded fact it is (TC-20's
#: measured gap), never re-decided here.
_OUTAGE_START = dt.date(2022, 3, 18)

#: The original's parse pattern for `fluxtable.txt` rows, migrated as-is.
_FLUX_RE = re.compile(
    r"^(?P<date>\d{8})\s+(?P<time>\d{6})\s+(?P<julian>[\d.]+)\s+"
    r"(?P<carrington>[\d.]+)\s+(?P<obs>[\d.]+)\s+(?P<adj>[\d.]+)\s+(?P<ursi>[\d.]+)\s*$"
)

#: The manifest/artifact field names this run can produce, screened through R-23's
#: produced-field limb BEFORE the first write (R-24).
PRODUCED_FIELDS: tuple[str, ...] = (
    "artifact_class",
    "derived",
    "partial",
    "missing_months",
    "series",
    "series_id",
    "release_status",
    "retrieval_date",
    "provider_product_identity",
    "sha256",
    "per_file_sha256",
    "provenance_verifiability",
    "documented_absence",
    "unverified_status_statement",
    "grade_basis",
    "carried_forward_epochs",
    "coverage",
    "day_rows_parsed",
    "expected_days",
    "missing_days",
    "records_2022",
    "days_present_2022",
    "days_missing_2022",
    "days_missing_from_outage_start",
    "unparsed_lines",
    "produced_by",
    "provenance_stamp",
    "provenance_stamp_note",
    "source",
    "stamp_class",
    "stamped_at_utc",
    # CR-2026-09-13-04-FIXTURE-WINDOW: fixture-run labelling fields (TC-03f — plumbing
    # evidence, never scientific governed-run evidence).
    "evidence_class",
    "audit_window",
    "fixture_scope_id",
    "plumbing_statement",
)


def _assert_phase1_field_contract(phase: int) -> None:
    """R-24: the produced-field guard, called before this run's first write."""
    assert_no_raw_fields(PRODUCED_FIELDS, phase=phase)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="04_build_external_products.py",
        description=(
            "External products (P1-04): driver-series audit with the two-tier "
            "manifest; IRI-benchmark and GIM-comparator generation attempts, both of "
            "which REFUSE today (R-59 validation unrun; Q-15 unset)."
        ),
    )
    parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="the governed configs directory (always configs/; TE 13.2)",
    )
    parser.add_argument(
        "--phase",
        type=int,
        choices=(1, 2),
        default=PHASE_DEFAULT,
        help="phase-aware per services.md; every path below is phase-1-legal",
    )
    parser.add_argument(
        "--evidence-root",
        type=Path,
        default=Path("evidence/audit_ec1_2026-08-15"),
        help="workspace-relative driver-evidence directory for the migrated audit",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help=(
            "workspace-relative driver-manifest output path. When absent: the standing "
            "full-year path on a non-fixture run; on a fixture run, "
            "artifacts/walking_skeleton/<fixture_id>/external/… so a plumbing artifact "
            "never lands on the governed manifest path "
            "(CR-2026-09-13-04-FIXTURE-WINDOW)"
        ),
    )
    parser.add_argument(
        "--code-commit",
        type=str,
        default=None,
        help=(
            "explicit code commit for the environment lock where no git tree exists "
            "(a Kaggle session, or a temporary smoke workspace); the lock is never "
            "written unpopulated (REQ-ENG-10)"
        ),
    )
    parser.add_argument(
        "--attempt-benchmark",
        action="store_true",
        help="attempt IRI benchmark generation; REFUSES today (R-59: no passing report)",
    )
    parser.add_argument(
        "--verify-runtime",
        action="store_true",
        help=(
            "B-01 runtime pin protection (D-45): verify the installed iricore release, its "
            "default IRI version and the FULL SHA-256 of the two index files it would "
            "consume against experiment.benchmark_b01; writes the runtime identity"
        ),
    )
    parser.add_argument(
        "--build-validation-report",
        type=Path,
        default=None,
        help=(
            "JSON file of 5-10 student-supplied samples (site, lat, lon, target_time_utc, "
            "local_time_class, activity_class, official_interface_value); computes the "
            "adapter value for each and writes the R-59 seven-area report (status passed or "
            "failed -- never hidden) using the PREDECLARED tolerance from configuration"
        ),
    )
    parser.add_argument(
        "--generate-benchmark",
        action="store_true",
        help=(
            "the production path: pins verified, all four R-59 limbs over the report named "
            "by --validation-report, hourly grid from data.yaml stations, workload, pins "
            "re-verified, stamped rows + provenance written; refuses on any failed gate"
        ),
    )
    parser.add_argument(
        "--validation-report",
        type=Path,
        default=None,
        help="the governed R-59 report JSON --generate-benchmark gates on",
    )
    parser.add_argument(
        "--months",
        type=str,
        default=None,
        help=(
            "comma-separated months restricting the grid (a PARTIAL product, labelled so); "
            "absent = the full year (the 26,000-call workload, TC-04)"
        ),
    )
    parser.add_argument(
        "--attempt-comparator",
        action="store_true",
        help="attempt GIM comparator generation; REFUSES today (Q-15 unset; R-60)",
    )
    parser.add_argument(
        "--gate-state",
        type=Path,
        default=None,
        help=(
            "JSON file of INJECTED gate state for a negative-control attempt; the "
            "same gates run over it, and a state satisfying every gate still refuses "
            "(injection mode never generates)"
        ),
    )
    parser.add_argument(
        "--render-comparison",
        type=Path,
        default=None,
        help=(
            "JSON file of an INJECTED comparison + overlap-audit state; runs the "
            "reporting path's disclosure contract (obligation 3's emitted statements; "
            "the comparison-existence overlap-flag trigger) through the allowlisted "
            "importer and prints the rendered report -- no artifact is written"
        ),
    )
    parser.add_argument(
        "--fixture-manifest",
        type=Path,
        default=None,
        help=(
            "the walking-skeleton fixture scope (a fixture manifest or identity declaration, "
            "validated through the one loader). When given, this run is a FIXTURE run: the "
            "TE 9.2 two-receipt gate is exempt (a fixture run is not a full-year job, Q5 = A) "
            "and the exemption is recorded, never silent. Additive edit flagged for "
            "`external-products`' record (fixtures-and-reproducibility CR-2026-09-07)"
        ),
    )
    return parser.parse_args(argv)


def _declared_data_window() -> tuple[dt.date, dt.date]:
    """Board Rec 2 (ML-01, owner-authorised per CR-2026-09-07 §11.5; flagged for
    `external-products`' record): the data window a NON-FIXTURE run declares and audits —
    the migrated audit's own calendar-year window, derived from `_AUDIT_YEAR` (the
    constant the migration preserved from `audit_ec1_drivers.py`, matching D-8's frozen
    claim boundary; c59 — this script's own input declaration, not narrative).

    On a fixture run this function is NOT the declaration: per the owner's Option (a)
    ruling (CR-2026-09-13-04-FIXTURE-WINDOW) the declared window IS the fixture scope's
    cited window, and the audit's reads are bounded to it, so the declaration is true by
    construction. The earlier state — declaring this full year under any fixture scope —
    made the ladder's `04` step refuse unconditionally (the deadlock that ruling
    resolves)."""
    return (dt.date(_AUDIT_YEAR, 1, 1), dt.date(_AUDIT_YEAR, 12, 31))


def _stage_entry(
    config_dir: Path,
    *,
    phase: int,
    code_commit: str | None,
    fixture_manifest: Path | None = None,
    full_year_job: bool = True,
) -> dict[str, Any]:
    """Steps 2-6 of the stage entry contract (step 1, determinism, ran in main()).

    2. `load_configs` -- snapshot, hash, resolve roots (the only read of configs/).
    3. Preflight: `assert_no_tbd` over this stage's required fields (deliberately
       minimal -- `features.carry_forward_composition` is enforced at availability
       resolution via FeatureAvailabilityError, never blanket-listed here) and
       `assert_declared_sources_exist`.
    4. `assert_phase_boundary` -- no raw-processing module loaded.
    5. No authenticated provider access is declared for this stage (the audit reads
       local, already-retrieved driver evidence); the credential-NAME presence check
       has nothing to check and nothing is silently skipped -- this line records it.
    6. Seed, capture the eight-item environment lock, open the run record, then
       `require_receipts_for_snapshot` (TE 9.2: both fixtures pass before any full-year
       job; exempt on a fixture run carrying `--fixture-manifest`, Q5 = A). On a fixture
       run the declared window IS the scope's cited window and the audit reads only that
       window (CR-2026-09-13-04-FIXTURE-WINDOW, Option a) -- the declaration is made
       true by narrowing the reads, never by narrowing the report. The scope is loaded
       through the same one loader the gate uses; the gate itself is unmodified and
       re-validates the manifest internally.
    """
    snapshot = load_configs(config_dir, phase=phase)
    assert_no_tbd(snapshot, required=required_fields_for(STAGE, PHASE_DEFAULT))
    assert_declared_sources_exist(snapshot)
    assert_phase_boundary(phase, loaded_modules=sys.modules)
    determinism = seed_everything(snapshot, stage=STAGE)
    lock = capture_environment_lock(snapshot, determinism, code_commit=code_commit)
    assert_lock_complete(lock)
    if fixture_manifest is not None:
        # Option (a): the fixture scope's cited window is BOTH the declaration and the
        # audit's read bound. `_declared_data_window()` (full year) is deliberately not
        # consulted on this path -- declaring it under a 7-day/1-month scope is the
        # unconditional refusal the owner's ruling repairs.
        scope = load_fixture_scope(fixture_manifest)
        audit_window: tuple[dt.date, dt.date] = scope.window
        fixture_scope_id: str | None = scope.fixture_id
        declared_window: tuple[dt.date, dt.date] | None = audit_window
    else:
        audit_window = _declared_data_window()
        fixture_scope_id = None
        declared_window = None
    if full_year_job:
        receipts_gate: Any = require_receipts_for_snapshot(
            snapshot,
            lock,
            fixture_manifest=fixture_manifest,
            declared_window=declared_window,
            declared_window_resource=(
                "scripts/04_build_external_products.py: declared audit window "
                "(fixture scope's cited window on a fixture run; calendar year otherwise)"
            ),
        )
    else:
        # TE 9.2 gates FULL-YEAR jobs. `--verify-runtime` (hashing two files) and
        # `--build-validation-report` (5-10 calls, no product) are bounded checks that
        # produce no artifact a full-year job consumes; the exemption is recorded, never
        # silent. EVERY `--generate-benchmark` run, partial or not, keeps the gate.
        receipts_gate = {
            "status": "not required",
            "reason": "bounded B-01 runtime/validation check, not a full-year job (TE 9.2)",
        }
    return {
        "snapshot": snapshot,
        "determinism": determinism,
        "lock": lock,
        "receipts_gate": receipts_gate,
        "audit_window": audit_window,
        "fixture_scope_id": fixture_scope_id,
    }


def _registry_paths(snapshot: Any) -> tuple[Path, Path]:
    registry_root = Path(
        snapshot.resolved_roots.get(
            "registry_root", snapshot.resolved_roots["artifacts"] / "registry"
        )
    )
    registry_path = registry_root / "experiment_registry.jsonl"
    access_log = (
        Path(snapshot.resolved_roots["workspace"]) / "evidence" / "merge_run_access_log.jsonl"
    )
    return registry_path, access_log


def _registry_row(
    run_id: str, *, status: str, lock_hash: str, snapshot: Any, reason: str = ""
) -> dict[str, Any]:
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    row: dict[str, Any] = {
        "run_id": run_id,
        "started_at_utc": now,
        "completed_at_utc": now if status in ("completed", "aborted", "failed") else "",
        "status": status,
        "code_commit": "",  # populated from the lock by the caller
        "environment_lock_hash": lock_hash,
        "platform": snapshot.platform,
        "dataset_version": "",
        "fold_id": "",
        "mask_id": "",
        "feature_set_id": "",
        "model_id": "",
        "hyperparameters_json": "",
        "seed": "",
        "validation_metric_name": "",
        "validation_metric_value": "",
        "artifact_manifest_path": "",
        "prediction_hash": "",
        "locked_test_accessed": False,
        "notes": "external-products run (P1-04)",
    }
    if reason:
        row["reason"] = reason
    return row


# =======================================================================================
# The migrated EC-1 driver audit (W-8; R-61: the :184 gap closed onto the two tiers)
# =======================================================================================


def _months_in_window(window: tuple[dt.date, dt.date]) -> list[tuple[int, int]]:
    """The (year, month) pairs intersecting `window`, in calendar order.

    CR-2026-09-13-04-FIXTURE-WINDOW: the audit's month iteration derives from the run's
    audit window (the fixture scope's cited window on a fixture run; `_AUDIT_YEAR`'s
    calendar year otherwise). For the full-year window this yields exactly the twelve
    months the pre-repair loop hardcoded.
    """
    start, end = window
    if start > end:
        raise IntegrityError(
            "audit window",
            f"window {start}..{end} is inverted; an inverted window audits nothing and "
            f"refuses rather than reporting vacuous coverage",
        )
    months: list[tuple[int, int]] = []
    cursor = dt.date(start.year, start.month, 1)
    while cursor <= end:
        months.append((cursor.year, cursor.month))
        cursor = (
            dt.date(cursor.year + 1, 1, 1)
            if cursor.month == 12
            else dt.date(cursor.year, cursor.month + 1, 1)
        )
    return months


def _dst_month_from_name(file_name: str) -> tuple[int, int] | None:
    """Parse (year, month) from a recorded `dst_provisional_YYYYMM.html` name, else None."""
    match = re.match(r"^dst_provisional_(\d{4})(\d{2})\.html$", file_name)
    if not match:
        return None
    year, month = int(match.group(1)), int(match.group(2))
    if not 1 <= month <= 12:
        return None
    return (year, month)


def _verify_recorded_hashes(
    evidence_root: Path,
    *,
    window: tuple[dt.date, dt.date],
    fixture_scoped: bool,
) -> None:
    """The integrity tier: current bytes must match the previously recorded audit hashes.

    CR-2026-09-13-04-FIXTURE-WINDOW: on a fixture run (`fixture_scoped=True`) the checks
    are bounded to the window — a recorded dst entry for an out-of-window month is
    neither read nor required (a fixture run touches only its cited window, board
    Rec 2), while a recorded dst entry whose month cannot be parsed from its filename
    REFUSES fail-closed (it cannot be proven out-of-window). The recorded fluxtable
    entry keeps full semantics on both paths: it is the carrier file for in-window F10.7
    days, so recorded-but-missing stays a violation. On a non-fixture run the checked
    set is byte-identical to the pre-repair behaviour.

    The original run's `ec1-audit-report.json` records a sha256 per evidence file; a
    file whose current bytes do not match is evidence altered since the run, and the
    audit TERMINATES naming the file and the violated expectation -- never continuing
    silently past a failed hash (team.md Mandated; R-61 integrity tier). A file listed
    in the report but absent is the same violation. An absent report is not a
    violation: the first audit of a fresh evidence set has nothing recorded yet, and
    completeness is the OTHER tier's business.

    Raises
    ------
    IntegrityError
        naming the file and the recorded-vs-actual hashes.
    """
    report_path = evidence_root / "ec1-audit-report.json"
    if not report_path.is_file():
        return
    try:
        recorded = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrityError(
            report_path,
            f"the recorded audit report is unreadable ({exc}); an unverifiable "
            f"integrity record terminates the run rather than being skipped",
        ) from exc

    in_window_months = set(_months_in_window(window))
    checks: list[tuple[Path, str]] = []
    dst_months = recorded.get("obligation_1_kyoto_dst", {})
    if isinstance(dst_months, Mapping):
        for info in dst_months.values():
            if isinstance(info, Mapping) and "sha256" in info and "file" in info:
                if fixture_scoped:
                    parsed = _dst_month_from_name(str(info["file"]))
                    if parsed is None:
                        raise IntegrityError(
                            evidence_root / "kyoto_dst" / str(info["file"]),
                            "recorded dst entry whose month cannot be parsed from its "
                            "filename; on a fixture run the integrity checks are bounded "
                            "to the scope's cited window, and an unattributable entry "
                            "cannot be proven out-of-window -- fail closed "
                            "(CR-2026-09-13-04-FIXTURE-WINDOW)",
                        )
                    if parsed not in in_window_months:
                        continue  # neither read nor required: out of the cited window
                checks.append(
                    (evidence_root / "kyoto_dst" / str(info["file"]), str(info["sha256"]))
                )
    f107 = recorded.get("obligation_2_canadian_f107", {})
    if isinstance(f107, Mapping) and "sha256" in f107 and "file" in f107:
        checks.append((evidence_root / "nrcan_f107" / str(f107["file"]), str(f107["sha256"])))

    for path, expected in checks:
        if not path.is_file():
            raise IntegrityError(
                path,
                f"listed in {report_path.name} with recorded sha256 {expected} but "
                f"missing on disk; the audit never proceeds past a failed integrity "
                f"check (R-61 integrity tier)",
            )
        actual = sha256_of_file(path)
        if actual != expected:
            raise IntegrityError(
                path,
                f"FAILED hash check (recorded {expected}, actual {actual}) -- evidence "
                f"altered since the recorded audit run; a hash mismatch terminates "
                f"non-zero naming the file and the violated expectation, never a "
                f"warning (R-61, REQ-ENG-9, team.md two-tier posture)",
            )


def _audit_dst(
    kyoto_dir: Path, *, window: tuple[dt.date, dt.date]
) -> tuple[list[dict[str, Any]], list[str]]:
    """Obligation 1 (migrated): per-month Dst coverage over the audit window, missing
    months NAMED.

    Returns (per-month coverage records, missing-month names). A month whose file was
    never retrieved is a COMPLETENESS shortfall: named machine-readably, non-fatal --
    the closure of the original's `:184` unconditional `return 0` is that the fact is
    recorded where a consumer reads it, not that the run aborts (R-61: making an
    ordinary partial retrieval abort the run is how a guard gets worked around).

    CR-2026-09-13-04-FIXTURE-WINDOW: iteration, day expectations, parsed-row counting
    and missing-day accounting are all bounded to `window`. A monthly file for an
    out-of-window month is neither opened, hashed, counted, nor required. For the
    full-year window this is byte-identical to the pre-repair twelve-month loop.
    """
    start, end = window
    coverage: list[dict[str, Any]] = []
    missing_months: list[str] = []
    for year, month in _months_in_window(window):
        path = kyoto_dir / f"dst_provisional_{year}{month:02d}.html"
        if not path.is_file():
            missing_months.append(f"{year}-{month:02d} (dst: file not retrieved)")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        day_rows: set[int] = set()
        for line in text.splitlines():
            match = re.match(r"^\s*(\d{1,2})((?:\s+-?\d+){24})\s*$", line)
            if match:
                day_rows.add(int(match.group(1)))
        month_start = dt.date(year, month, 1)
        next_month_start = dt.date(year + 1, 1, 1) if month == 12 else dt.date(year, month + 1, 1)
        # The in-window slice of this month (whole month on a full-year window).
        lo = max(month_start, start)
        hi = min(next_month_start - dt.timedelta(days=1), end)
        expected_days = (hi - lo).days + 1
        in_window_days = set(range(lo.day, hi.day + 1))
        coverage.append(
            {
                "month": f"{year}-{month:02d}",
                "file": path.name,
                "sha256": sha256_of_file(path),
                "expected_days": expected_days,
                "day_rows_parsed": len(day_rows & in_window_days),
                "missing_days": sorted(in_window_days - day_rows),
            }
        )
    return coverage, missing_months


def _audit_f107(flux_path: Path, *, window: tuple[dt.date, dt.date]) -> dict[str, Any]:
    """Obligation 2 (migrated): F10.7 archive coverage over the audit window.

    An absent `fluxtable.txt` is a completeness shortfall for the SERIES (recorded by
    the caller); missing days inside the window are recorded machine-readably, with the
    outage-window subset named separately, exactly as the original reported them.

    CR-2026-09-13-04-FIXTURE-WINDOW: row counting and missing-day accounting are bounded
    to `window`. `fluxtable.txt` stays the carrier file (it is read if present — it
    holds the in-window days); only its ACCOUNTING is window-bounded. For the full-year
    window the date-range filter is extensionally identical to the pre-repair
    `date.year == _AUDIT_YEAR` filter.
    """
    if not flux_path.is_file():
        return {"present": False}
    start, end = window
    by_day: dict[dt.date, int] = {}
    unparsed = 0
    with flux_path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith(("fluxdate", "---")):
                continue
            match = _FLUX_RE.match(line)
            if not match:
                unparsed += 1
                continue
            date = dt.datetime.strptime(match.group("date"), "%Y%m%d").date()
            if start <= date <= end:
                by_day[date] = by_day.get(date, 0) + 1
    all_days = [start + dt.timedelta(days=i) for i in range((end - start).days + 1)]
    missing = [day for day in all_days if day not in by_day]
    return {
        "present": True,
        "file": flux_path.name,
        "sha256": sha256_of_file(flux_path),
        "records_2022": sum(by_day.values()),
        "days_present_2022": len(by_day),
        "days_missing_2022": [day.isoformat() for day in missing],
        "days_missing_from_outage_start": [
            day.isoformat() for day in missing if day >= _OUTAGE_START
        ],
        "unparsed_lines": unparsed,
    }


def _combined_digest(hashes: list[str]) -> str:
    """One digest over a series' per-file hashes (sorted), for the per-series manifest
    field -- a derived identity binding the entry to the exact byte set audited."""
    import hashlib

    return hashlib.sha256("\n".join(sorted(hashes)).encode("ascii")).hexdigest()


def _run_driver_audit(entry: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    """W-8: the migrated EC-1 audit, closed onto the two-tier posture (R-61).

    CR-2026-09-13-04-FIXTURE-WINDOW: both tiers and all accounting run over
    `entry["audit_window"]` — the fixture scope's cited window on a fixture run, the
    calendar year otherwise. Fixture-run artifacts are plumbing evidence (TC-03f),
    written under the walking-skeleton root, never onto the governed manifest path.
    """
    _assert_phase1_field_contract(args.phase)  # R-24: before the first write, always

    snapshot = entry["snapshot"]
    window: tuple[dt.date, dt.date] = entry["audit_window"]
    fixture_scope_id = entry.get("fixture_scope_id")
    window_label = f"{window[0]:%Y-%m}..{window[1]:%Y-%m}"
    workspace = Path(snapshot.resolved_roots["workspace"])
    evidence_root = workspace / args.evidence_root
    if not evidence_root.is_dir():
        raise IntegrityError(
            evidence_root,
            "driver-evidence directory does not exist; the audit has no bytes to "
            "verify and refuses rather than reporting vacuous coverage",
        )

    # Integrity tier FIRST: a failed hash invalidates everything downstream of it.
    _verify_recorded_hashes(
        evidence_root, window=window, fixture_scoped=fixture_scope_id is not None
    )

    dst_coverage, missing_months = _audit_dst(evidence_root / "kyoto_dst", window=window)
    f107 = _audit_f107(evidence_root / "nrcan_f107" / "fluxtable.txt", window=window)

    # The retrieval date is the evidence set's own recorded identity (the dated
    # directory name of the one-time 2026-08-15 retrieval), not a value chosen here.
    retrieval_date = evidence_root.name.removeprefix("audit_ec1_")

    series_entries: list[dict[str, Any]] = []
    if dst_coverage:
        per_file = {record["file"]: record["sha256"] for record in dst_coverage}
        series_entries.append(
            {
                "series_id": "dst",
                "release_status": "provisional",
                "retrieval_date": retrieval_date,
                "provider_product_identity": (
                    f"kyoto_dst/dst_provisional_{_AUDIT_YEAR}MM.html "
                    f"({len(dst_coverage)} monthly files present)"
                ),
                "sha256": _combined_digest(list(per_file.values())),
                "per_file_sha256": per_file,
                "provenance_verifiability": {
                    "status": "declared-status-only",
                    "documented_absence": (
                        "the Kyoto monthly tables carry no provenance column; the "
                        "grade is inferable from the filename alone"
                    ),
                    "unverified_status_statement": (
                        "the declared 'provisional' grade is recorded, not verified: "
                        "D-10.1's open item on the 2022 Kyoto grade remains unchecked "
                        "per D-11, and no detection is possible from the bytes -- "
                        "bounded, not closed (R-63's Constraint, carried to G-04)"
                    ),
                    "grade_basis": "filename token 'provisional' (declared)",
                },
                "carried_forward_epochs": [],
                "coverage": dst_coverage,
            }
        )
    else:
        missing_months.append(f"{window_label} (dst: no file retrieved)")

    if f107.get("present"):
        series_entries.append(
            {
                "series_id": "f107",
                "release_status": "observed (grade undeclared by provider)",
                "retrieval_date": retrieval_date,
                "provider_product_identity": "nrcan_f107/fluxtable.txt",
                "sha256": f107["sha256"],
                "per_file_sha256": {f107["file"]: f107["sha256"]},
                "provenance_verifiability": {
                    "status": "declared-status-only",
                    "documented_absence": (
                        "fluxtable.txt has exactly seven columns and no correction, "
                        "revision, version or provenance column (D-22)"
                    ),
                    "unverified_status_statement": (
                        "the provider's publication latency is not derivable from the "
                        "held file (D-21) and no reanalysed-value detection is "
                        "possible from the bytes -- bounded, not closed (R-63's "
                        "Constraint, carried to G-04)"
                    ),
                    "grade_basis": "no provenance column exists; absence documented",
                },
                "carried_forward_epochs": [],
                "coverage": {key: value for key, value in f107.items() if key not in ("present",)},
            }
        )
    else:
        missing_months.append(f"{window_label} (f107: fluxtable.txt not retrieved)")

    # The two GFZ series were retrieved on 2026-09-18 into
    # evidence/audit_gfz_2026-09-18/ (scripts/audit_gfz_drivers.py; D-39, D-40; R-63
    # control 5 executed literally for Kp/ap and as the accepted substitute for Hp60/ap60)
    # but are NOT YET CONSUMED by this stage: no driver product is built from them here
    # and no producer artifact exists (D-41 identities only). Recorded as a completeness
    # fact, named per series across the whole window -- never console text only, and
    # never fatal (R-61). Wording updated 2026-09-18 (gate item G-6); the superseded text
    # read "never retrieved -- no GFZ directory in the evidence set".
    for gfz_series in ("kp_ap3", "hp60_ap60"):
        missing_months.append(
            f"{window_label} ({gfz_series}: retrieved 2026-09-18 into "
            f"evidence/audit_gfz_2026-09-18/ but not yet consumed by this stage; no "
            f"driver product built from it here -- integration owed under D-39/D-40/D-41)"
        )

    if fixture_scope_id is not None:
        # TC-03f: a fixture-scoped audit artifact is plumbing evidence, never scientific
        # governed-run evidence. Labelled on every series entry, and written under the
        # walking-skeleton root so it cannot land on (or divergently collide with) the
        # governed full-year manifest path (CR-2026-09-13-04-FIXTURE-WINDOW).
        plumbing_label = {
            "evidence_class": "fixture_plumbing",
            "fixture_scope_id": fixture_scope_id,
            "audit_window": {
                "start": window[0].isoformat(),
                "end": window[1].isoformat(),
            },
        }
        for series_entry in series_entries:
            series_entry.update(plumbing_label)

    if args.out is not None:
        out_rel = args.out
    elif fixture_scope_id is not None:
        out_rel = (
            Path(WALKING_SKELETON_ROOT)
            / fixture_scope_id
            / "external"
            / "ec1_driver_audit_manifest.json"
        )
    else:
        out_rel = _DEFAULT_OUT
    out_path = workspace / out_rel
    manifest_path = write_driver_manifest(
        out_path,
        series_entries=series_entries,
        missing_months=missing_months,
        produced_by="scripts/04_build_external_products.py",
    )
    driver_releases = _publish_driver_releases(
        entry=entry,
        evidence_root=evidence_root,
        gfz_root=workspace / "evidence" / "audit_gfz_2026-09-18",
    )
    summary: dict[str, Any] = {
        "driver_manifest": str(manifest_path),
        "missing_month_entries": len(missing_months),
        "series_audited": len(series_entries),
        "driver_releases": driver_releases,
    }
    if fixture_scope_id is not None:
        summary["evidence_class"] = "fixture_plumbing"
        summary["fixture_scope_id"] = fixture_scope_id
        summary["audit_window"] = {
            "start": window[0].isoformat(),
            "end": window[1].isoformat(),
        }
        summary["plumbing_statement"] = (
            "fixture-scoped driver audit: plumbing/fixture evidence only, never "
            "scientific governed-run evidence (TC-03f; the seven-day fixture is a smoke "
            "test, TE 9.2)"
        )
    return summary


# =======================================================================================
# The driver releases (D-61's option A, applied at the 04 -> 05 boundary; D-63 identities)
# =======================================================================================
#
# WHY IT LIVES HERE. This script has said so in its own words since 2026-09-18: the two GFZ
# series "are NOT YET CONSUMED by this stage: no driver product is built from them here and
# no producer artifact exists (D-41 identities only)". D-63 then named the producing-artifact
# identity of every driver-class TE 6.2 row, and `configs/features.yaml: permitted_producers`
# transcribes them, so `build_features` already knows which artifact each row must come from
# — nothing published one. The owner ruled on 2026-09-23 that D-61's option A extends here:
# the stage publishes the release the downstream stages consume, under the D-63 identities,
# with no new D-number.
#
# ONE RELEASE PER PRODUCING ARTIFACT, named for the identity itself, so the mapping from
# `permitted_producers` to a directory under the release root is the identity and not a
# convention a reader has to learn.
#
# NOTHING IS FABRICATED, AND NOTHING IS FILLED. Values come from the provider bytes this run
# has already hash-verified, through the ONE parser per format (src/external/spaceweather.py).
# A provider missing marker is released as an EMPTY cell and counted — never as -1, never
# interpolated, never carried forward (D-5; D-10.2: gaps are explicit NaN at acquisition,
# and the 3-hour carry-forward is a FEATURE-time rule applied at the availability boundary,
# not an acquisition-time fill). Rows are bounded to this run's audit window, so a fixture
# run publishes the fixture's window and nothing wider.
#
# TC-12 IS VISIBLE IN THE SHAPE. A driver release carries one value per epoch and no station
# axis at all: `row_counts.by_station` records `time_indexed_no_station_axis` rather than a
# per-station count, because a driver series that could be counted per station is already
# the defect TC-12 exists to prevent.
#
# RE-RUNS AND R-13, exactly as stage 02's target release: identical content republishes
# nothing; different content REFUSES naming both hashes rather than overwriting a citation.


#: The four D-63 producing-artifact identities, each with the series it carries, the
#: evidence file it is parsed from, and the units of its columns. The identity strings are
#: `src/external/spaceweather.py: DRIVER_PRODUCERS`' values and are asserted equal to them
#: at publication time, so config, constant and release cannot drift apart.
_DRIVER_RELEASES: Final[tuple[dict[str, Any], ...]] = (
    {
        "artifact": "gfz_kp_ap_nowcast_2022",
        "rows_for": "kp_ap",
        "file": "kp_ap_3h.csv",
        "decision": "D-39 (archived settled nowcast Kp_now2022.wdc, DOI 10.5880/Kp.0001)",
        "release_status": "nowcast",
        "units": {"kp": "dimensionless (thirds)", "ap": "nT"},
        "cadence_hours": 3,
    },
    {
        "artifact": "gfz_hp60ap60_v2_2022",
        "rows_for": "hp60_ap60",
        "file": "hp60_ap60_1h.csv",
        "decision": "D-40 (Hp60ap60doi_2022.txt V2.0, DOI 10.5880/Hpo.0002; V3.0 is a comparator only)",
        "release_status": "hpo_v2.0_contemporaneous",
        "units": {"hp60": "dimensionless (thirds)", "ap60": "nT"},
        "cadence_hours": 1,
    },
    {
        "artifact": "nrcan_f107_observed_daily_median_2022",
        "rows_for": "f107",
        "file": "f107_daily_median.csv",
        "decision": "D-21/D-22/D-23 (NRCan observed flux; project-derived daily median)",
        "release_status": "observed",
        "units": {"f107_daily_median": "sfu"},
        "cadence_hours": 24,
    },
    {
        "artifact": "kyoto_wdc_dst_2022",
        "rows_for": "dst",
        "file": "dst_1h.csv",
        "decision": "D-10.1 (Kyoto WDC; one release grade, recorded before use)",
        "release_status": "provisional (per the retrieved file names; D-10.1's grade rule)",
        "units": {"dst_nt": "nT"},
        "cadence_hours": 1,
    },
)

#: Recorded where a fold, mask or feature-set id does not exist yet — stage 04 precedes all
#: three. Deliberately unusable as a real identifier, the same device stages 00 and 02 use.
_STAGE04_ID_PLACEHOLDER: Final[str] = "NOT_YET_ASSIGNED_stage_04_precedes_splits_masks_features"

_DRIVER_RELEASE_CHANGE_RECORD: Final[str] = "CR-2026-09-23-DRIVER-RELEASE-OPTION-A"

#: What `processing`'s target-shaped keys mean for a driver release. TE 13.3 requires all
#: seven keys non-empty, and four of them describe a gridded TARGET: a driver series has no
#: cell, no provider experiment/kindat and no hourly target aggregation. Each therefore
#: carries an explicit statement of non-applicability rather than a value borrowed from the
#: target's release, which would be false, or an empty string, which `write_release` refuses.
_DRIVER_NOT_APPLICABLE: Final[str] = (
    "not applicable to a driver release: driver series are TIME-INDEXED ONLY, one value per "
    "epoch identical across all three cells (TC-12, binding: hard) — no cell is selected, no "
    "provider experiment/kindat applies, and no hourly target aggregation is performed here"
)


def _utc(year: int, month: int, day: int, hour: int) -> str:
    return dt.datetime(year, month, day, hour, tzinfo=dt.timezone.utc).isoformat()


def _interval_rows(
    parsed: Mapping[tuple[int, int, int, int], tuple[float, int]],
    *,
    window: tuple[dt.date, dt.date],
    cadence_hours: int,
    value_names: tuple[str, str],
) -> tuple[list[dict[str, str]], int]:
    """Interval-valued driver rows inside the window, and the count of ABSENT values.

    Both provider boundaries are preserved on every row (D-43: the safe-lag reference
    instant is the interval END, so a consumer that has only a start cannot apply the rule).
    A provider missing marker becomes an EMPTY cell and is counted; it is never written as
    the sentinel and never filled.
    """
    start, end = window
    rows: list[dict[str, str]] = []
    absent = 0
    for (year, month, day, hour), values in sorted(parsed.items()):
        moment = dt.date(year, month, day)
        if not (start <= moment <= end):
            continue
        row = {
            "interval_start_utc": _utc(year, month, day, hour),
            "interval_end_utc": (
                dt.datetime(year, month, day, hour, tzinfo=dt.timezone.utc)
                + dt.timedelta(hours=cadence_hours)
            ).isoformat(),
        }
        for name, value in zip(value_names, values, strict=True):
            missing = float(value) < 0
            absent += 1 if missing else 0
            row[name] = "" if missing else str(value)
        rows.append(row)
    return rows, absent


def _f107_rows(
    flux_path: Path, *, window: tuple[dt.date, dt.date]
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    """D-21's project-derived daily median of the OBSERVED flux, with D-22/D-23's flags.

    The median is computed by `spaceweather.daily_medians_from_readings` — the module that
    owns driver-product arithmetic — never re-implemented here. A day with no reading is
    simply ABSENT from the release: no row is invented for it (D-5).
    """
    from src.external.spaceweather import daily_medians_from_readings

    start, end = window
    readings: list[dict[str, Any]] = []
    with flux_path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith(("fluxdate", "---")):
                continue
            match = _FLUX_RE.match(line)
            if not match:
                continue
            day = dt.datetime.strptime(match.group("date"), "%Y%m%d").date()
            if start <= day <= end:
                readings.append(
                    {"day": day, "time": match.group("time"), "value": float(match.group("obs"))}
                )
    derived = daily_medians_from_readings(readings)
    medians = dict(derived["medians"])
    duplicates = dict(derived["duplicate_days"])
    spreads = dict(derived["high_spread_days"])
    rows = [
        {
            "day_utc": day.isoformat(),
            "f107_daily_median": str(value),
            "duplicate_readings_averaged": str(duplicates.get(day, 0)),
            "high_spread_pct": str(spreads[day]) if day in spreads else "",
        }
        for day, value in sorted(medians.items())
    ]
    expected = (end - start).days + 1
    return rows, {
        "readings_read": len(readings),
        "days_released": len(rows),
        "days_absent": expected - len(rows),
        "duplicate_days": len(duplicates),
        "high_spread_days": len(spreads),
    }


def _dst_rows(
    kyoto_dir: Path, *, window: tuple[dt.date, dt.date]
) -> tuple[list[dict[str, str]], int]:
    """Hourly Dst from the retrieved Kyoto monthly tables, bounded to the window.

    Dst stays DIAGNOSTIC-ONLY (TC-11; `DIAGNOSTIC_ONLY_SERIES`): publishing it as a release
    records its provenance and admits nothing about its use, and the modelling-input bar is
    `assert_grade_eligible`'s, not this function's. The provider's missing marker (|value|
    >= 9999) becomes an empty cell and is counted.
    """
    start, end = window
    rows: list[dict[str, str]] = []
    absent = 0
    for year, month in _months_in_window(window):
        path = kyoto_dir / f"dst_provisional_{year}{month:02d}.html"
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            match = re.match(r"^\s*(\d{1,2})((?:\s+-?\d+){24})\s*$", line)
            if not match:
                continue
            day = int(match.group(1))
            try:
                moment = dt.date(year, month, day)
            except ValueError:
                continue
            if not (start <= moment <= end):
                continue
            values = [int(v) for v in match.group(2).split()]
            for hour, value in enumerate(values):
                missing = abs(value) >= 9999
                absent += 1 if missing else 0
                rows.append(
                    {
                        "interval_start_utc": _utc(year, month, day, hour),
                        "dst_nt": "" if missing else str(value),
                    }
                )
    rows.sort(key=lambda row: row["interval_start_utc"])
    return rows, absent


def _driver_release_manifest(
    *,
    spec: Mapping[str, Any],
    snapshot: Any,
    window: tuple[dt.date, dt.date],
    source_files: list[dict[str, Any]],
    rows: list[Mapping[str, str]],
    absent: int,
    output_files: Mapping[str, str],
    fixture_scope_id: str | None,
) -> dict[str, Any]:
    """The thirteen caller-supplied TE 13.3 fields for one driver release."""
    identity = resolve_target_identity(snapshot.data)
    months: dict[str, int] = {}
    key = "interval_start_utc" if rows and "interval_start_utc" in rows[0] else "day_utc"
    for row in rows:
        months[str(row[key])[:7]] = months.get(str(row[key])[:7], 0) + 1
    return {
        "source_manifest_id": f"{spec['artifact']}:{spec['decision']}",
        "source_files": source_files,
        "processing": {
            # The identity stamps are the study's, so a driver release cannot be mistaken
            # for another lineage's (TEC-05/R-70).
            "phase_id": identity["phase_id"],
            "target_definition_id": identity["target_definition_id"],
            "provider_experiment_kindat": _DRIVER_NOT_APPLICABLE,
            "parameters": sorted(spec["units"]),
            "station_coordinate_to_cell_rule": _DRIVER_NOT_APPLICABLE,
            "selected_cell_bounds": {"time_indexed_only": _DRIVER_NOT_APPLICABLE},
            "hourly_aggregation": (
                "project-derived daily median of the observed flux (D-21/D-22/D-23)"
                if spec["rows_for"] == "f107"
                else "none: values are released at the provider's own cadence, unaggregated"
            ),
        },
        "schema_version": str(snapshot.data.get("schema_version", "")),
        "units": dict(spec["units"]),
        "row_counts": {
            # TC-12 made visible: a driver series has no station axis, and a per-station
            # count here would be the artefact the rule exists to prevent.
            "by_station": {"time_indexed_no_station_axis": len(rows)},
            "by_month": months,
            "by_split": {"unsplit_stage_04": len(rows)},
            "by_qc_stage": {"as_provided_no_qc_applied": len(rows)},
        },
        "exclusions_qc_summary": [
            {
                "reason": (
                    "provider value absent at this epoch: released as an explicit empty "
                    "cell, never as the provider's sentinel and never filled (D-5; D-10.2)"
                ),
                "count": int(absent),
            }
        ],
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "fold_ids": [_STAGE04_ID_PLACEHOLDER],
        "mask_ids": [_STAGE04_ID_PLACEHOLDER],
        "feature_set_ids": [_STAGE04_ID_PLACEHOLDER],
        "output_files": dict(output_files),
        "change_record_id": _DRIVER_RELEASE_CHANGE_RECORD,
        # Read by the feature build as the (row, producer) pair's producer half: the
        # release states which D-63 identity it IS, rather than leaving a consumer to infer
        # it from the directory name.
        "producing_artifact": spec["artifact"],
        "release_status": spec["release_status"],
        "window": {"start": window[0].isoformat(), "end": window[1].isoformat()},
        # TC-03f, stamped ON the release rather than left to the directory name. A fixture
        # run publishes the fixture's window -- seven days, not a year -- under the same
        # governed citation a full-year run would use, and a reader who meets this manifest
        # without its run log must be able to tell the two apart. `window` above says how
        # much; this says what KIND. The open naming question (whether a fixture-scoped
        # release should live under a fixture-named directory, which the target release
        # cannot do while 05/06/07 resolve its directory by a fixed name) is recorded in
        # CR-2026-09-23-DRIVER-RELEASE-OPTION-A rather than decided here.
        "evidence_class": "fixture_plumbing" if fixture_scope_id else "governed_run",
        "fixture_scope_id": fixture_scope_id or "",
    }


def _publish_driver_releases(
    *, entry: Mapping[str, Any], evidence_root: Path, gfz_root: Path
) -> list[dict[str, Any]]:
    """Publish one immutable release per D-63 producing artifact. Returns per-release facts."""
    from src.external.spaceweather import DRIVER_PRODUCERS, parse_hpo_v2, parse_kp_ap_wdc

    snapshot = entry["snapshot"]
    window: tuple[dt.date, dt.date] = entry["audit_window"]
    workspace = Path(snapshot.resolved_roots["workspace"])
    release_root = Path(
        snapshot.resolved_roots.get(
            "release_root", snapshot.resolved_roots["artifacts"] / "releases"
        )
    )
    known = set(DRIVER_PRODUCERS.values())
    published: list[dict[str, Any]] = []

    for spec in _DRIVER_RELEASES:
        artifact = str(spec["artifact"])
        if artifact not in known:
            raise IntegrityError(
                artifact,
                f"is not one of D-63's producing-artifact identities {sorted(known)}; a "
                f"release published under an identity the permitted-producer list does not "
                f"carry could never be admitted by build_features (SD-F-01)",
            )

        rows: list[dict[str, str]]
        absent = 0
        extra: dict[str, Any] = {}
        sources: list[Path] = []
        if spec["rows_for"] == "kp_ap":
            source = gfz_root / "Kp_now2022.wdc"
            if not source.is_file():
                published.append(
                    {
                        "artifact": artifact,
                        "published": False,
                        "reason": f"{source.name} not retrieved",
                    }
                )
                continue
            rows, absent = _interval_rows(
                parse_kp_ap_wdc(source), window=window, cadence_hours=3, value_names=("kp", "ap")
            )
            sources = [source]
        elif spec["rows_for"] == "hp60_ap60":
            source = gfz_root / "hp60ap60doi_2022_v2.txt"
            if not source.is_file():
                published.append(
                    {
                        "artifact": artifact,
                        "published": False,
                        "reason": f"{source.name} not retrieved",
                    }
                )
                continue
            rows, absent = _interval_rows(
                parse_hpo_v2(source), window=window, cadence_hours=1, value_names=("hp60", "ap60")
            )
            sources = [source]
        elif spec["rows_for"] == "f107":
            source = evidence_root / "nrcan_f107" / "fluxtable.txt"
            if not source.is_file():
                published.append(
                    {
                        "artifact": artifact,
                        "published": False,
                        "reason": "fluxtable.txt not retrieved",
                    }
                )
                continue
            rows, extra = _f107_rows(source, window=window)
            sources = [source]
        else:
            kyoto = evidence_root / "kyoto_dst"
            rows, absent = _dst_rows(kyoto, window=window)
            sources = sorted(
                path
                for path in kyoto.glob("dst_provisional_*.html")
                if (parsed := _dst_month_from_name(path.name)) is not None
                and window[0] <= dt.date(parsed[0], parsed[1], 1)
                and dt.date(parsed[0], parsed[1], 1) <= window[1].replace(day=1)
            )
            if not rows:
                published.append(
                    {
                        "artifact": artifact,
                        "published": False,
                        "reason": "no in-window Dst table retrieved",
                    }
                )
                continue

        source_files = [
            {
                "provider": artifact.split("_")[0].upper(),
                "citation": spec["decision"],
                "location_date": f"{path.parent.name} ({window[0].isoformat()}..{window[1].isoformat()})",
                "filename": path.name,
                "retrieval_date": path.parent.name.split("_")[-1],
                "sha256": sha256_of_file(path),
            }
            for path in sources
        ]

        directory = release_root / artifact
        directory.mkdir(parents=True, exist_ok=True)
        rows_path = directory / str(spec["file"])
        columns = list(rows[0])
        with rows_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
        manifest = _driver_release_manifest(
            spec=spec,
            snapshot=snapshot,
            window=window,
            source_files=source_files,
            rows=rows,
            absent=absent,
            output_files={rows_path.name: sha256_of_file(rows_path)},
            fixture_scope_id=entry.get("fixture_scope_id"),
        )

        manifest_path = directory / MANIFEST_NAME
        if manifest_path.is_file():
            existing = json.loads(manifest_path.read_text(encoding="utf-8"))
            would_be = content_hash_of(manifest)
            if would_be == str(existing.get("content_hash", "")):
                published.append(
                    {
                        "artifact": artifact,
                        "published": False,
                        "dataset_version": str(existing.get("dataset_version", "")),
                        "rows": len(rows),
                        "reason": "identical content already published; R-13 refuses an "
                        "overwrite and none was attempted",
                        **extra,
                    }
                )
                continue
            raise IntegrityError(
                manifest_path,
                f"a DIFFERENT driver product is already published under {artifact!r} "
                f"(published content_hash {existing.get('content_hash', '')}, this run's "
                f"{would_be}); TE 13.3 requires a new version rather than an overwrite, and "
                f"choosing it is an owner act (R-13)",
            )
        try:
            written = write_release(directory, manifest, release_root=release_root)
        except ReleaseError as exc:
            raise IntegrityError(directory, f"the {artifact} release was refused: {exc}") from exc
        published.append(
            {
                "artifact": artifact,
                "published": True,
                "dataset_version": written["dataset_version"],
                "rows": len(rows),
                "absent_values": absent,
                "release_dir": str(directory.relative_to(workspace)),
                **extra,
            }
        )
    return published


# =======================================================================================
# The two refusal paths (the refusals ARE the deliverable)
# =======================================================================================


def _load_gate_state(path: Path | None) -> Mapping[str, Any] | None:
    if path is None:
        return None
    try:
        loaded = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrityError(
            str(path),
            f"gate-state file is unreadable ({exc}); an injection control "
            f"over unparseable state proves nothing",
        ) from exc
    if not isinstance(loaded, Mapping):
        raise IntegrityError(str(path), "gate-state file must hold a JSON object")
    return loaded


def _attempt_benchmark(entry: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    """Attempt IRI benchmark generation -- REFUSES today (R-59 limb 1).

    The `iri` import is deferred here: this script is one of TE 12's two allowlisted
    importers, and the default driver-audit path never loads the module.
    """
    _assert_phase1_field_contract(args.phase)
    from src.external import iri  # allowlisted importer; deferred by design

    state = _load_gate_state(args.gate_state)
    if state is None:
        # The real attempt: no governed validation report exists, so limb 1 refuses.
        iri.generate_benchmark(
            validation_report=None,
            report_name="iri_implementation_validation_report",
            availability_matrix=None,
            benchmark_drivers=iri.BENCHMARK_DRIVER_IDS,
            injection_mode=False,
        )
    else:
        iri.generate_benchmark(
            validation_report=state.get("validation_report"),
            report_name=str(state.get("report_name", "injected_validation_report")),
            availability_matrix=state.get("availability_matrix"),
            benchmark_drivers=tuple(state.get("benchmark_drivers", ("f107", "kp_ap3"))),
            injection_mode=True,
        )
    raise IntegrityError(  # pragma: no cover - generate_benchmark always raises today
        "iri benchmark attempt",
        "generate_benchmark returned without raising; the gate contract requires a "
        "refusal on every attempt today",
    )


def _b01_out_dir(entry: Mapping[str, Any], args: argparse.Namespace) -> Path:
    workspace = Path(entry["snapshot"].resolved_roots["workspace"])
    out = args.out if args.out is not None else Path("artifacts/external/b01")
    out = out if out.is_absolute() else workspace / out
    out.mkdir(parents=True, exist_ok=True)
    return out


def _write_json(path: Path, payload: Any) -> Path:
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    return path


def _write_manifest(out: Path, files: list[Path]) -> Path:
    manifest = {f.name: sha256_of_file(f) for f in files}
    return _write_json(out / "sha256_manifest.json", manifest)


def _verify_runtime(entry: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    """D-45 runtime pin protection, run before an execution session (annotation item 2)."""
    _assert_phase1_field_contract(args.phase)
    from src.external import iri  # allowlisted importer; deferred by design

    contract = iri.read_benchmark_contract(entry["snapshot"])
    identity = iri.verify_runtime(contract)
    out = _b01_out_dir(entry, args)
    identity["environment_lock_hash"] = environment_lock_hash(entry["lock"])
    identity["config_hashes"] = dict(entry["snapshot"].hashes)
    path = _write_json(out / "b01_runtime_identity.json", identity)
    _write_manifest(out, [path])
    print(f"04_build_external_products: runtime verified: {identity['index_files_sha256']}")
    return {"runtime_identity": path}


def _load_json_object(path: Path, *, what: str) -> Any:
    try:
        loaded = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrityError(str(path), f"{what} is unreadable ({exc})") from exc
    return loaded


def _build_validation_report(entry: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    """R-59's seven-area report from student-supplied samples; the tolerance is the
    predeclared one in configuration. A failed report is written with status failed."""
    _assert_phase1_field_contract(args.phase)
    from src.external import iri  # allowlisted importer; deferred by design

    samples = _load_json_object(args.build_validation_report, what="validation samples file")
    if isinstance(samples, Mapping) and "samples" in samples:
        samples = samples["samples"]
    if not isinstance(samples, list):
        raise IntegrityError(
            str(args.build_validation_report),
            "must hold a JSON list of samples (or an object with a 'samples' list)",
        )
    contract = iri.read_benchmark_contract(entry["snapshot"])
    identity = iri.verify_runtime(contract)
    report = iri.build_validation_report(contract, identity, samples)
    out = _b01_out_dir(entry, args)
    path = _write_json(out / f"{contract.report_name}.json", report)
    _write_manifest(out, [path])
    print(f"04_build_external_products: validation report {report['status'].upper()} -> {path}")
    if report["status"] != "passed":
        raise IntegrityError(
            str(path),
            "validation report status is 'failed': at least one sample exceeds the predeclared "
            "tolerance; the report is written as-is and generation stays blocked (R-59) -- "
            "the implementation is never silently switched",
        )
    return {"validation_report": path}


def _generate_benchmark(entry: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    """The production path (R-59 all limbs; D-45 pins before and after the session)."""
    _assert_phase1_field_contract(args.phase)
    from src.data.registry import load_registry  # station coordinates (D-1)
    from src.external import iri  # allowlisted importer; deferred by design

    if args.validation_report is None:
        raise IntegrityError(
            "--validation-report",
            "required with --generate-benchmark: the governed R-59 report to gate on (limb 1)",
        )
    report = _load_json_object(args.validation_report, what="validation report")
    if not isinstance(report, Mapping):
        raise IntegrityError(
            str(args.validation_report), "validation report must be a JSON object"
        )
    months = [int(m) for m in args.months.split(",")] if args.months else None
    contract = iri.read_benchmark_contract(entry["snapshot"])
    stations = load_registry(entry["snapshot"])

    def progress(done: int, total: int) -> None:
        print(f"04_build_external_products: B-01 {done}/{total} calls", flush=True)

    result = iri.run_gated_generation(
        contract=contract,
        validation_report=report,
        stations=stations,
        months=months,
        progress=progress,
    )
    out = _b01_out_dir(entry, args)
    rows_path = out / (
        "b01_iri2016_rows_partial.jsonl" if result["partial"] else "b01_iri2016_rows.jsonl"
    )
    with rows_path.open("w", encoding="utf-8") as handle:
        for row in result["rows"]:
            handle.write(json.dumps(row, default=str) + "\n")
    prov = dict(result["provenance"])
    prov["rows_file"] = rows_path.name
    prov["rows_sha256"] = sha256_of_file(rows_path)
    prov["validation_report_file"] = str(args.validation_report)
    prov["validation_report_sha256"] = sha256_of_file(Path(args.validation_report))
    prov["environment_lock_hash"] = environment_lock_hash(entry["lock"])
    prov["config_hashes"] = dict(entry["snapshot"].hashes)
    prov["artifact_class"] = (
        "B-01 benchmark rows (generated, not trained); partial"
        if result["partial"]
        else "B-01 benchmark rows (generated, not trained)"
    )
    prov_path = _write_json(out / "b01_provenance.json", prov)
    _write_manifest(out, [rows_path, prov_path])
    print(
        f"04_build_external_products: B-01 generated {prov['call_count']} rows "
        f"({prov['error_rows']} error rows) in {prov['workload_seconds']} s -> {rows_path}"
    )
    return {"benchmark_rows": rows_path, "provenance": prov_path}


def _attempt_comparator(entry: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    """Attempt GIM comparator generation -- REFUSES today (Q-15 unset; R-60)."""
    _assert_phase1_field_contract(args.phase)
    from src.external import gim  # allowlisted importer; deferred by design

    state = _load_gate_state(args.gate_state)
    snapshot = entry["snapshot"]
    if state is None:
        # The real attempt: Q-15 is resolved from the governed experiment config and
        # is UNSET, so obligation 1 refuses. No default is supplied (TE 18.2).
        gim.generate_comparator(
            interpolation_rule=gim.interpolation_rule_from(snapshot.experiment),
            hand_check=None,
            overlap_audit=None,
            injection_mode=False,
        )
    else:
        now = None
        if state.get("generation_attempt_utc"):
            now = dt.datetime.fromisoformat(str(state["generation_attempt_utc"]))
            if now.tzinfo is None:
                raise IntegrityError(
                    str(args.gate_state),
                    "generation_attempt_utc carries no timezone; a naive timestamp "
                    "cannot evidence ordering (R-60 obligation 2)",
                )
        gim.generate_comparator(
            interpolation_rule=state.get("interpolation_rule"),
            hand_check=state.get("hand_check"),
            overlap_audit=state.get("overlap_audit"),
            injection_mode=True,
            now=now,
        )
    raise IntegrityError(  # pragma: no cover - generate_comparator always raises today
        "gim comparator attempt",
        "generate_comparator returned without raising; the gate contract requires a "
        "refusal on every attempt today",
    )


def _render_comparison(entry: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    """The reporting-path contract check over INJECTED state (obligation 3; R-60).

    Runs `gim.render_comparison_report` -- the chokepoint that EMITS the
    map-product-to-map-product limitation and the spatial-representativeness mismatch
    itself, and that refuses any comparison with no registered overlap-audit result --
    through this script, TE 12's allowlisted importer. The rendered report is printed,
    never written: the injected comparison is contract-check state, not a governed
    artifact, and no GIM comparison artifact is produced by this unit.
    """
    _assert_phase1_field_contract(args.phase)
    from src.data.acquisition import guard_egress  # deferred with the attempt paths
    from src.external import gim  # allowlisted importer; deferred by design

    state = _load_gate_state(args.render_comparison)
    if state is None:  # pragma: no cover - argparse routing guarantees the path
        raise IntegrityError(
            "render-comparison", "no state file was supplied to the reporting-path check"
        )
    report = gim.render_comparison_report(
        comparison=state.get("comparison", {}),
        overlap_audit=state.get("overlap_audit"),
    )
    guard_egress(report, context="gim_comparison_report[render-contract-check]")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return {"rendered": "stdout (contract check over injected state; no artifact written)"}


def main() -> int:
    ensure_process_determinism(sys.argv)  # FIRST statement, before any framework import
    args = _parse_args(sys.argv[1:])

    try:
        entry = _stage_entry(
            args.config,
            phase=args.phase,
            code_commit=args.code_commit,
            fixture_manifest=args.fixture_manifest,
            full_year_job=not (args.verify_runtime or args.build_validation_report is not None),
        )
    except IntegrityError as exc:
        print(f"04_build_external_products: preflight refusal: {exc}", file=sys.stderr)
        return 1

    snapshot = entry["snapshot"]
    lock = entry["lock"]
    lock_hash = environment_lock_hash(lock)
    registry_path, access_log = _registry_paths(snapshot)
    run_id = (
        f"external-products-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
        f"-{uuid.uuid4().hex[:8]}"
    )

    started = _registry_row(run_id, status="started", lock_hash=lock_hash, snapshot=snapshot)
    started["code_commit"] = lock.code_commit
    append_registry_event(
        registry_path,
        started,
        phase=args.phase,
        writer_role="stage",
        access_log_path=access_log,
    )

    try:
        if args.attempt_benchmark:
            summary = _attempt_benchmark(entry, args)
        elif args.verify_runtime:
            summary = _verify_runtime(entry, args)
        elif args.build_validation_report is not None:
            summary = _build_validation_report(entry, args)
        elif args.generate_benchmark:
            summary = _generate_benchmark(entry, args)
        elif args.attempt_comparator:
            summary = _attempt_comparator(entry, args)
        elif args.render_comparison is not None:
            summary = _render_comparison(entry, args)
        else:
            summary = _run_driver_audit(entry, args)
    except IntegrityError as exc:
        aborted = _registry_row(
            run_id, status="aborted", lock_hash=lock_hash, snapshot=snapshot, reason=str(exc)
        )
        aborted["code_commit"] = lock.code_commit
        record_abort_honestly(
            registry_path,
            aborted,
            phase=args.phase,
            writer_role="stage",
            access_log_path=access_log,
            original_error=exc,
        )
        print(f"04_build_external_products: aborted: {exc}", file=sys.stderr)
        return 1

    completed = _registry_row(run_id, status="completed", lock_hash=lock_hash, snapshot=snapshot)
    completed["code_commit"] = lock.code_commit
    completed["artifact_manifest_path"] = str(next(iter(summary.values())))
    append_registry_event(
        registry_path,
        completed,
        phase=args.phase,
        writer_role="stage",
        access_log_path=access_log,
    )
    print(f"04_build_external_products: completed: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
