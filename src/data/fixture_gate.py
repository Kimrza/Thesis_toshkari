"""F4 + F6: fixture-pass receipts, the exported two-receipt check, the in-session gate result.

Purpose
-------
`fixtures-and-reproducibility` W-7 and W-8 (R-140, R-141; SD-X-02 with governance Rec 7).

**Receipts (R-140).** TE 9.2's rule — both walking-skeleton fixtures pass, in order, before any
full-year job — is made an executable gate that survives sessions and platforms. On each
fixture pass `run_walking_skeleton.py` calls `write_fixture_pass_receipt`, which

* REFUSES a `candidate` manifest at write time (R-140 control 29: only a frozen expectation can
  be passed against);
* writes the receipt payload ONCE (fixture id, the FROZEN manifest's SHA-256, the result, the
  fixture run's registry id, `completed_at_utc`, the platform from `ConfigSnapshot`, the eight
  TE 13.1 lock items in force, and — on `scientific_1month` — the plumbing receipt it found,
  identity by citation);
* records it as **append-safe experiment-registry rows** through `append_registry_event`
  (Q6 = A (ii); SD-X-02 Rec 7): a `started`/`completed` pair under the child run id
  `<run_id>/receipt/<fixture_id>`, `artifact_manifest_path` naming the payload, `notes`
  carrying only the literal kind marker. TE 13.4's twenty columns are used as defined — none
  is repurposed.

**Why the registry row gives the receipt tamper-evidence.** The row's `environment_lock_hash`
is the SHA-256 over the eight lock items (`config.environment_lock_hash`), and the fixture
run's lock carries `input_versions = [fixture_manifest:<fixture_id>:<sha256>]`. The check
recomputes the lock hash FROM THE PAYLOAD and compares it with the append-only row: an edit
to the payload's recorded lock, OR to its frozen-manifest binding, breaks agreement with a
row nothing can rewrite (R-08). SD-X-02's discriminator — a receipt is valid iff its lock
matches the caller's own TE 13.1 lock — is computed over the seven ENVIRONMENT items
(`environment_identity`: every lock item except `input_versions`, which is per-run by
nature), so a config edit or re-install invalidates receipts and an unchanged environment
reuses them regardless of session age.

**The exported check** `require_fixture_receipts` refuses each of the four bypass routes:
a scientific-fixture run without a plumbing receipt (26), a full-year invocation without both
receipts (27), a receipt whose manifest hash disagrees with the frozen manifest in force (28
— a re-freeze invalidates old receipts by construction), and a receipt from a candidate
manifest (29, refused at write time; re-checked on read). `require_receipts_for_snapshot`
derives every path from the `ConfigSnapshot` so each of the seven Phase 1 stage scripts
calls it with ONE line inside `_stage_entry`, right after `assert_lock_complete` (Q5 = A).
It is EXEMPT when the run carries a fixture scope (`fixture_manifest` given) — a fixture run
is not a full-year job — and the exemption is satisfied only by a scope that VALIDATES
through `load_fixture_scope`, never by a bare flag.

**The in-session gate (R-141; TC-03g).** `emit_in_session_gate_result` records the platform
FROM `ConfigSnapshot.platform` (never caller-asserted), the eight lock items, both frozen
manifest hashes in force, per-test and per-fixture results, and its own `measured_total_runtime`
(recorded against no ceiling: no session or wall-clock limit exists in any authority, and none
is invented). `require_in_session_gate` refuses a `local` stamp (30), a lock disagreement on
`code_commit` or the config-snapshot hashes (31), and a result predating the frozen manifests
in force — detected as a hash disagreement, the same binding receipts use (32).

Inputs
------
`FixtureManifest`s through `src/data/fixture_manifest.load_fixture_manifest` (the only read
path); `RunRecord` locks from `src/data/config`; the experiment registry through
`src/data/experiment_registry.append_registry_event`; receipt/gate payload files this module
writes and reads; `src/data/release.sha256_of_file` for any digest (nothing here re-implements
hashing).

Re-run behaviour
----------------
Every write is once-only: an existing payload file refuses, and the registry append is
append-only by the writer's contract. Every check is a pure read. Two receipts is the whole
receipt set — the M10 contract-fixture result is clean-run evidence, never a third receipt.

What this pass cannot make run (TE 18.3)
-----------------------------------------
No frozen manifest exists, so `require_fixture_receipts` refuses every full-year invocation
today naming the missing manifest — which is TE 9.2's intent and Q5 = A's stated immediate
cost; no receipt can be written because no fixture can run (BLK-02; the TensorFlow pin;
`embargo_hours` TBD). The in-session gate is emitted only inside a Kaggle session.

Every refusal raises the base `IntegrityError` naming the resource and the violated
expectation (Q6 = A (i); no `FixtureError` is minted).
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from collections.abc import Mapping
from dataclasses import fields as _dataclass_fields
from pathlib import Path
from typing import Any, Final

from src.data.acquisition import assert_records_within_window
from src.data.config import ConfigSnapshot, IntegrityError, RunRecord, environment_lock_hash
from src.data.experiment_registry import append_registry_event
from src.data.fixture_manifest import (
    FIXTURE_IDS,
    PLUMBING_FIXTURE_ID,
    SCIENTIFIC_FIXTURE_ID,
    FixtureManifest,
    fixture_root_for,
    load_fixture_manifest,
    load_fixture_scope,
    manifest_path_for,
)

__all__ = [
    "RECEIPT_KIND",
    "GATE_RESULT_KIND",
    "RECEIPT_NAME",
    "GATE_RESULT_NAME",
    "RESULT_PASS",
    "KAGGLE",
    "LOCK_ITEMS",
    "ENVIRONMENT_IDENTITY_ITEMS",
    "FIXTURE_INPUT_TAG_PREFIX",
    "lock_items",
    "lock_from_items",
    "environment_identity",
    "fixture_input_version_tag",
    "receipt_path_for",
    "gate_result_path_for",
    "assert_declared_window_within_scope",
    "write_fixture_pass_receipt",
    "read_receipt",
    "verify_receipt",
    "require_plumbing_receipt",
    "require_fixture_receipts",
    "require_receipts_for_snapshot",
    "emit_in_session_gate_result",
    "read_gate_result",
    "require_in_session_gate",
]

RECEIPT_KIND: Final[str] = "fixture_pass_receipt"
GATE_RESULT_KIND: Final[str] = "in_session_gate_result"
RECEIPT_NAME: Final[str] = "fixture_pass_receipt.json"
GATE_RESULT_NAME: Final[str] = "in_session_gate_result.json"
#: A receipt records a pass; a failed fixture is an `aborted` registry row, never a receipt.
RESULT_PASS: Final[str] = "PASS"
#: TC-03g: the platform the governed run runs on (config.resolve_platform_roots' label).
KAGGLE: Final[str] = "kaggle"
#: TE 13.1's eight lock items, DERIVED from foundation's RunRecord — never restated.
LOCK_ITEMS: Final[tuple[str, ...]] = tuple(f.name for f in _dataclass_fields(RunRecord))
#: SD-X-02's discriminator: the environment items — every lock item except `input_versions`.
ENVIRONMENT_IDENTITY_ITEMS: Final[tuple[str, ...]] = tuple(
    item for item in LOCK_ITEMS if item != "input_versions"
)
FIXTURE_INPUT_TAG_PREFIX: Final[str] = "fixture_manifest:"
_WRITER_ROLE: Final[str] = "stage"


def _refuse(resource: object, expectation: str) -> IntegrityError:
    return IntegrityError(resource, expectation)


# --- lock items --------------------------------------------------------------------------


def lock_items(lock: RunRecord | Mapping[str, Any]) -> dict[str, Any]:
    """The eight TE 13.1 items as a JSON-safe mapping (a `RunRecord` or an already-mapped one)."""
    source: Mapping[str, Any]
    if isinstance(lock, RunRecord):
        source = {name: getattr(lock, name) for name in LOCK_ITEMS}
    else:
        source = lock
    missing = [name for name in LOCK_ITEMS if name not in source]
    if missing:
        raise _refuse(
            "environment lock", f"TE 13.1 lock item(s) missing: {', '.join(missing)}"
        )
    out: dict[str, Any] = {}
    for name in LOCK_ITEMS:
        value = source[name]
        if isinstance(value, Mapping):
            out[name] = dict(sorted((str(k), str(v)) for k, v in value.items()))
        elif isinstance(value, list | tuple):
            out[name] = [str(v) for v in value]
        else:
            out[name] = str(value)
    return out


def lock_from_items(items: Mapping[str, Any]) -> RunRecord:
    """Rebuild a `RunRecord` from recorded items, so its hash can be recomputed."""
    normalised = lock_items(items)
    return RunRecord(
        requirements_hash=str(normalised["requirements_hash"]),
        pip_freeze=str(normalised["pip_freeze"]),
        runtime_versions=dict(normalised["runtime_versions"]),
        code_commit=str(normalised["code_commit"]),
        config_hashes=dict(normalised["config_hashes"]),
        input_versions=list(normalised["input_versions"]),
        platform=str(normalised["platform"]),
        nondeterministic_ops=list(normalised["nondeterministic_ops"]),
    )


def environment_identity(lock: RunRecord | Mapping[str, Any]) -> str:
    """SD-X-02's staleness discriminator: SHA-256 over the seven environment items."""
    items = lock_items(lock)
    payload = {name: items[name] for name in ENVIRONMENT_IDENTITY_ITEMS}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def fixture_input_version_tag(fixture_id: str, manifest_sha256: str) -> str:
    """The `input_versions` entry that binds the manifest hash into the row-hashed lock."""
    if fixture_id not in FIXTURE_IDS:
        raise _refuse("fixture_id", f"{fixture_id!r} is not one of {list(FIXTURE_IDS)}")
    return f"{FIXTURE_INPUT_TAG_PREFIX}{fixture_id}:{manifest_sha256}"


def assert_declared_window_within_scope(
    scope: Any, *, declared_start: dt.date, declared_end: dt.date, resource: str
) -> dict[str, str]:
    """Board Rec 2 (ML-01, owner-authorised per CR §11.5): the TE 9.2 exemption is bound to
    the fixture scope's cited window, no longer granted on a validating flag alone.

    A record-date assertion reusing `acquisition.assert_records_within_window` (R-31
    consumed, never copied): the caller's declared data window's endpoints are asserted
    inside the scope's cited window. A full-scale invocation carrying a valid scope but
    out-of-window inputs REFUSES here — this is the ONE guard home for the exemption
    boundary (nfr-design c58), and each caller derives its own declared window from its own
    input declaration (c59).

    Raises
    ------
    IntegrityError
        the declared window's endpoints do not lie inside the scope's cited window, or the
        declared window is inverted.
    """
    start, end = scope.window
    if declared_start > declared_end:
        raise _refuse(resource, f"declared window {declared_start}..{declared_end} is inverted")
    endpoints = [
        {"date": declared_start.isoformat()},
        {"date": declared_end.isoformat()},
    ]
    try:
        assert_records_within_window(endpoints, start=start, end=end, timestamp_key="date")
    except IntegrityError as exc:
        raise _refuse(
            resource,
            f"declared data window {declared_start}..{declared_end} does not lie inside the "
            f"fixture scope's cited window {start}..{end}; the TE 9.2 receipt-gate exemption "
            f"is bound to the scope's window and is not granted on a validating flag alone — "
            f"a fixture run touches only its cited window (board Rec 2 / ML-01; R-31's "
            f"record-date assertion reused, never copied)",
        ) from exc
    return {
        "declared_start": declared_start.isoformat(),
        "declared_end": declared_end.isoformat(),
        "scope_start": start.isoformat(),
        "scope_end": end.isoformat(),
    }


def receipt_path_for(workspace: Path, fixture_id: str) -> Path:
    """`<workspace>/artifacts/walking_skeleton/<fixture_id>/fixture_pass_receipt.json`."""
    return fixture_root_for(workspace, fixture_id) / RECEIPT_NAME


def gate_result_path_for(workspace: Path) -> Path:
    """`<workspace>/artifacts/walking_skeleton/in_session_gate_result.json`."""
    return Path(workspace) / "artifacts" / "walking_skeleton" / GATE_RESULT_NAME


# --- payload files and registry rows ------------------------------------------------------


def _write_once_json(path: Path, payload: Mapping[str, Any]) -> Path:
    target = Path(path)
    if target.exists():
        raise _refuse(
            target,
            "a receipt or gate-result payload is written exactly once and never overwritten "
            "(NFR-AUD-01; a re-run writes a new payload under a new run id)",
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return target


def _read_json(path: Path, *, kind: str) -> dict[str, Any]:
    target = Path(path)
    if not target.is_file():
        raise _refuse(target, f"no {kind} exists at this path")
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise _refuse(target, f"{kind} is unreadable ({exc})") from exc
    if not isinstance(payload, Mapping) or payload.get("kind") != kind:
        raise _refuse(target, f"payload does not carry `kind: {kind}`")
    return dict(payload)


def _registry_rows(registry_path: Path) -> list[Mapping[str, Any]]:
    path = Path(registry_path)
    if not path.is_file():
        return []
    rows: list[Mapping[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue  # a malformed row is check_registry_integrity's report, not this check's
        if isinstance(parsed, Mapping):
            rows.append(parsed)
    return rows


def _completed_row(registry_path: Path, run_id: str) -> Mapping[str, Any]:
    rows = [r for r in _registry_rows(registry_path) if str(r.get("run_id")) == run_id]
    if not rows:
        raise _refuse(
            registry_path,
            f"no experiment-registry row for run {run_id!r}; a receipt is identified by its "
            f"registry run id and verified by hash, never by path convention (services.md "
            f"§ Ordering contract; R-140)",
        )
    completed = [r for r in rows if r.get("status") == "completed"]
    if not completed:
        raise _refuse(
            registry_path,
            f"run {run_id!r} has no `completed` row (statuses: "
            f"{[r.get('status') for r in rows]}); an aborted or failed fixture run is no pass",
        )
    return completed[-1]


def _child_rows(
    *,
    registry_path: Path,
    access_log_path: Path,
    phase: int,
    child_run_id: str,
    template: Mapping[str, Any],
    lock: RunRecord,
    platform: str,
    artifact_path: Path,
    kind: str,
) -> None:
    now = dt.datetime.now(dt.UTC).isoformat()
    base = dict(template)
    base.update(
        {
            "run_id": child_run_id,
            "code_commit": lock.code_commit,
            "environment_lock_hash": environment_lock_hash(lock),
            "platform": platform,
            "prediction_hash": "",
            "locked_test_accessed": False,
            "notes": kind,
        }
    )
    base.pop("reason", None)
    started = {**base, "status": "started", "started_at_utc": now, "completed_at_utc": ""}
    completed = {
        **base,
        "status": "completed",
        "started_at_utc": now,
        "completed_at_utc": now,
        "artifact_manifest_path": str(artifact_path),
    }
    append_registry_event(
        registry_path,
        started,
        phase=phase,
        writer_role=_WRITER_ROLE,
        access_log_path=access_log_path,
    )
    append_registry_event(
        registry_path,
        completed,
        phase=phase,
        writer_role=_WRITER_ROLE,
        access_log_path=access_log_path,
    )


# --- W-7 / R-140: receipts -------------------------------------------------------------------


def write_fixture_pass_receipt(
    *,
    manifest: FixtureManifest,
    result: str,
    run_id: str,
    lock: RunRecord,
    snapshot: ConfigSnapshot,
    registry_path: Path,
    access_log_path: Path,
    receipt_path: Path,
    registry_row: Mapping[str, Any],
    phase: int,
    plumbing_receipt: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Write ONE fixture-pass receipt as a payload file plus append-safe registry rows.

    Raises
    ------
    IntegrityError
        the manifest is not frozen (control 29); the result is not a pass; the fixture run's
        lock does not carry the manifest's input-version tag (the row binding would be empty);
        `scientific_1month` without the plumbing receipt it found (ordering by citation); an
        existing payload at `receipt_path`.
    """
    if not manifest.is_frozen:
        raise _refuse(
            manifest.path,
            f"a fixture-pass receipt is written from a FROZEN manifest only; status "
            f"{manifest.status!r} is refused at write time — a run against a candidate cannot "
            f"be passed against an expectation the owner has not frozen (R-140 control 29; "
            f"R-134's evidence bound)",
        )
    if result != RESULT_PASS:
        raise _refuse(
            receipt_path,
            f"result {result!r} is not {RESULT_PASS!r}; a failed fixture is an aborted registry "
            f"row with its reason, never a receipt",
        )
    tag = fixture_input_version_tag(manifest.fixture_id, manifest.sha256)
    if tag not in list(lock.input_versions):
        raise _refuse(
            "environment lock",
            f"input_versions does not carry {tag!r}; the fixture run's lock must bind the frozen "
            f"manifest so the append-only registry row hashes it (SD-X-02 Rec 7)",
        )
    if manifest.fixture_id == SCIENTIFIC_FIXTURE_ID:
        if (
            not isinstance(plumbing_receipt, Mapping)
            or plumbing_receipt.get("kind") != RECEIPT_KIND
        ):
            raise _refuse(
                receipt_path,
                "the scientific receipt records the plumbing receipt it found (identity by "
                "citation: its registry run id and frozen-manifest hash); none was supplied "
                "(R-140 control 26; SD-X-02)",
            )
        cited = {
            "registry_run_id": str(plumbing_receipt["registry_run_id"]),
            "receipt_run_id": str(plumbing_receipt["receipt_run_id"]),
            "frozen_manifest_hash": str(plumbing_receipt["frozen_manifest_hash"]),
        }
    else:
        if plumbing_receipt is not None:
            raise _refuse(receipt_path, "the plumbing receipt cites no prior receipt")
        cited = None
    child_run_id = f"{run_id}/receipt/{manifest.fixture_id}"
    payload: dict[str, Any] = {
        "kind": RECEIPT_KIND,
        "fixture_id": manifest.fixture_id,
        "frozen_manifest_hash": manifest.sha256,
        "frozen_manifest_path": str(manifest.path),
        "result": RESULT_PASS,
        "registry_run_id": run_id,
        "receipt_run_id": child_run_id,
        "completed_at_utc": dt.datetime.now(dt.UTC).isoformat(),
        "platform": snapshot.platform,
        "environment_lock": lock_items(lock),
        "environment_lock_hash": environment_lock_hash(lock),
        "environment_identity": environment_identity(lock),
        "plumbing_receipt": cited,
        "receipt_set": "exactly two: plumbing_7day, scientific_1month; the M10 contract-fixture "
        "result is clean-run evidence, never a third receipt (TC-03f; Q12 = C)",
    }
    written = _write_once_json(receipt_path, payload)
    _child_rows(
        registry_path=registry_path,
        access_log_path=access_log_path,
        phase=phase,
        child_run_id=child_run_id,
        template=registry_row,
        lock=lock,
        platform=snapshot.platform,
        artifact_path=written,
        kind=RECEIPT_KIND,
    )
    return payload


def read_receipt(path: Path) -> dict[str, Any]:
    return _read_json(path, kind=RECEIPT_KIND)


def verify_receipt(
    payload: Mapping[str, Any],
    *,
    manifest: FixtureManifest,
    registry_path: Path,
    lock: RunRecord,
    receipt_path: Path,
) -> dict[str, Any]:
    """The per-receipt checks; the resource named is the receipt payload."""
    if not manifest.is_frozen:
        raise _refuse(
            manifest.path,
            f"the manifest in force is {manifest.status!r}, not frozen; no receipt can be "
            f"accepted against an unfrozen expectation (R-140 control 29; R-134)",
        )
    if payload.get("fixture_id") != manifest.fixture_id:
        raise _refuse(
            receipt_path,
            f"receipt names fixture {payload.get('fixture_id')!r}, not {manifest.fixture_id!r}",
        )
    if payload.get("result") != RESULT_PASS:
        raise _refuse(receipt_path, f"receipt result {payload.get('result')!r} is not a pass")
    if payload.get("frozen_manifest_hash") != manifest.sha256:
        raise _refuse(
            receipt_path,
            f"receipt binds frozen manifest {payload.get('frozen_manifest_hash')} but the "
            f"manifest in force hashes to {manifest.sha256}; a re-frozen manifest "
            f"invalidates old receipts by construction (R-140 control 28)",
        )
    recorded_lock = payload.get("environment_lock")
    if not isinstance(recorded_lock, Mapping):
        raise _refuse(receipt_path, "receipt carries no recorded TE 13.1 lock (SD-X-02)")
    recomputed = environment_lock_hash(lock_from_items(recorded_lock))
    if recomputed != payload.get("environment_lock_hash"):
        raise _refuse(
            receipt_path,
            "the receipt's recorded lock does not hash to its own environment_lock_hash; the "
            "payload was edited after it was written (SD-X-02 Rec 7)",
        )
    tag = fixture_input_version_tag(manifest.fixture_id, manifest.sha256)
    if tag not in [str(v) for v in recorded_lock.get("input_versions", [])]:
        raise _refuse(
            receipt_path,
            f"the receipt's recorded lock does not carry {tag!r}; the manifest binding is part "
            f"of the row-hashed lock and is missing (SD-X-02 Rec 7)",
        )
    row = _completed_row(registry_path, str(payload.get("receipt_run_id", "")))
    if row.get("environment_lock_hash") != recomputed:
        raise _refuse(
            receipt_path,
            f"the append-only registry row for {payload.get('receipt_run_id')!r} records "
            f"environment_lock_hash {row.get('environment_lock_hash')}, the receipt's recorded "
            f"lock hashes to {recomputed}; the receipt disagrees with the row nothing can rewrite "
            f"(SD-X-02 Rec 7; R-08)",
        )
    if str(row.get("artifact_manifest_path", "")) != str(receipt_path):
        raise _refuse(
            receipt_path,
            f"the registry row names payload {row.get('artifact_manifest_path')!r}, not this file",
        )
    if environment_identity(recorded_lock) != environment_identity(lock):
        raise _refuse(
            receipt_path,
            "the receipt's environment (requirements hash, pip freeze, versions, code commit, "
            "config hashes, platform, nondeterministic ops) differs from this run's own TE 13.1 "
            "lock; a receipt is accepted iff its recorded lock matches the caller's — a config "
            "edit or re-install invalidates receipts (SD-X-02, Q2 = A at nfr-design)",
        )
    return {
        "fixture_id": manifest.fixture_id,
        "frozen_manifest_hash": manifest.sha256,
        "receipt_run_id": str(payload["receipt_run_id"]),
        "registry_run_id": str(payload["registry_run_id"]),
        "platform": str(payload.get("platform")),
        "accepted": True,
    }


def require_plumbing_receipt(
    *, registry_path: Path, plumbing_manifest_path: Path, receipt_path: Path, lock: RunRecord
) -> dict[str, Any]:
    """R-140 control 26: the scientific fixture may start only on a verified plumbing receipt."""
    manifest = load_fixture_manifest(plumbing_manifest_path)
    if not Path(receipt_path).is_file():
        raise _refuse(
            receipt_path,
            "no plumbing_7day receipt; the scientific fixture runs only after the plumbing "
            "fixture has passed under its frozen manifest (TE 9.2 in order; R-140 control 26)",
        )
    payload = read_receipt(receipt_path)
    verified = verify_receipt(
        payload,
        manifest=manifest,
        registry_path=registry_path,
        lock=lock,
        receipt_path=receipt_path,
    )
    return {**verified, "payload": payload}


def require_fixture_receipts(
    registry_path: Path,
    *,
    manifests: Mapping[str, Path],
    receipts: Mapping[str, Path],
    lock: RunRecord,
    fixture_manifest: Path | None = None,
    declared_window: tuple[dt.date, dt.date] | None = None,
    declared_window_resource: str = "declared data window",
) -> dict[str, Any]:
    """The exported two-receipt check every full-year job passes (R-140; Q5 = A).

    Exempt when `fixture_manifest` names a scope that validates (a fixture run is not a
    full-year job); the exemption is recorded, never silent. When the caller passes its
    `declared_window`, the exemption is additionally BOUND to the scope's cited window
    (board Rec 2 / ML-01, owner-authorised per CR §11.5): out-of-window inputs refuse.

    Raises
    ------
    IntegrityError
        a fixture scope that does not validate; a declared window outside the scope's cited
        window (Rec 2); a missing or unfrozen manifest in force; a missing receipt (27); a
        receipt failing any `verify_receipt` check (28/29 and the SD-X-02 binding); the
        scientific receipt not citing the plumbing receipt found (26).
    """
    if fixture_manifest is not None:
        scope = load_fixture_scope(fixture_manifest)
        window_check: dict[str, str] | None = None
        if declared_window is not None:
            window_check = assert_declared_window_within_scope(
                scope,
                declared_start=declared_window[0],
                declared_end=declared_window[1],
                resource=declared_window_resource,
            )
        start, end = scope.window
        return {
            "exempt": True,
            "reason": "a fixture run is not a full-year job (TE 9.2; Q5 = A)",
            "fixture_id": scope.fixture_id,
            "scope_kind": type(scope).__name__,
            "scope_sha256": scope.sha256,
            "scope_window_start": start.isoformat(),
            "scope_window_end": end.isoformat(),
            "declared_window_checked": window_check,
        }
    missing_ids = [fid for fid in FIXTURE_IDS if fid not in manifests or fid not in receipts]
    if missing_ids:
        raise _refuse(
            "require_fixture_receipts",
            f"manifest and receipt paths are required for both fixtures; missing {missing_ids}",
        )
    loaded = {fid: load_fixture_manifest(manifests[fid]) for fid in FIXTURE_IDS}
    verified: dict[str, dict[str, Any]] = {}
    payloads: dict[str, dict[str, Any]] = {}
    for fid in FIXTURE_IDS:
        receipt_path = Path(receipts[fid])
        if not receipt_path.is_file():
            raise _refuse(
                receipt_path,
                f"no {fid} receipt; both walking-skeleton fixtures pass, in order, before any "
                f"full-year job (TE 9.2; TC-03f; R-140 control 27)",
            )
        payloads[fid] = read_receipt(receipt_path)
        verified[fid] = verify_receipt(
            payloads[fid],
            manifest=loaded[fid],
            registry_path=registry_path,
            lock=lock,
            receipt_path=receipt_path,
        )
    cited = payloads[SCIENTIFIC_FIXTURE_ID].get("plumbing_receipt")
    plumbing = payloads[PLUMBING_FIXTURE_ID]
    if (
        not isinstance(cited, Mapping)
        or cited.get("receipt_run_id") != plumbing.get("receipt_run_id")
        or cited.get("frozen_manifest_hash") != plumbing.get("frozen_manifest_hash")
    ):
        raise _refuse(
            receipts[SCIENTIFIC_FIXTURE_ID],
            "the scientific receipt does not cite the plumbing receipt in force (run id and "
            "frozen-manifest hash); 'in order' is checked from the artifacts, not from "
            "timestamps (R-140 control 26; SD-X-02)",
        )
    return {"exempt": False, "receipts": verified}


def _registry_path_for(snapshot: ConfigSnapshot) -> Path:
    registry_root = Path(
        snapshot.resolved_roots.get(
            "registry_root", Path(snapshot.resolved_roots["artifacts"]) / "registry"
        )
    )
    return registry_root / "experiment_registry.jsonl"


def require_receipts_for_snapshot(
    snapshot: ConfigSnapshot,
    lock: RunRecord,
    *,
    fixture_manifest: Path | None = None,
    declared_window: tuple[dt.date, dt.date] | None = None,
    declared_window_resource: str = "declared data window",
) -> dict[str, Any]:
    """The ONE-line call every stage script's `_stage_entry` makes after `assert_lock_complete`.

    Derives the registry path, both manifest paths and both receipt paths from the snapshot's
    resolved roots, so no script restates a path convention. `declared_window` is the
    caller's own data-window derivation (c59), bound to the scope on a fixture run (Rec 2).
    """
    workspace = Path(snapshot.resolved_roots["workspace"])
    return require_fixture_receipts(
        _registry_path_for(snapshot),
        manifests={fid: manifest_path_for(workspace, fid) for fid in FIXTURE_IDS},
        receipts={fid: receipt_path_for(workspace, fid) for fid in FIXTURE_IDS},
        lock=lock,
        fixture_manifest=fixture_manifest,
        declared_window=declared_window,
        declared_window_resource=declared_window_resource,
    )


# --- W-8 / R-141: the in-session gate --------------------------------------------------------


def _frozen_hashes(manifests: Mapping[str, Path]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for fid in FIXTURE_IDS:
        if fid not in manifests:
            raise _refuse("manifests", f"no path for {fid}")
        manifest = load_fixture_manifest(manifests[fid])
        if not manifest.is_frozen:
            raise _refuse(
                manifest.path,
                f"{fid} manifest is {manifest.status!r}; the gate binds to FROZEN manifests in "
                f"force (R-141; R-134 control 5)",
            )
        hashes[fid] = manifest.sha256
    return hashes


def _parse_utc(value: object, *, resource: str) -> dt.datetime:
    if not isinstance(value, str):
        raise _refuse(resource, f"{value!r} is not an ISO-8601 timestamp")
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        stamp = dt.datetime.fromisoformat(text)
    except ValueError as exc:
        raise _refuse(resource, f"{value!r} is not an ISO-8601 timestamp") from exc
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=dt.UTC)
    return stamp.astimezone(dt.UTC)


def emit_in_session_gate_result(
    *,
    snapshot: ConfigSnapshot,
    lock: RunRecord,
    manifests: Mapping[str, Path],
    critical_test_results: Mapping[str, str],
    fixture_results: Mapping[str, str],
    started_at_utc: str,
    completed_at_utc: str,
    registry_path: Path,
    access_log_path: Path,
    result_path: Path,
    registry_row: Mapping[str, Any],
    run_id: str,
    phase: int,
) -> dict[str, Any]:
    """Emit the in-session gate result (R-141) — platform FROM the snapshot, never asserted.

    `measured_total_runtime_seconds` is `completed - started`: the wall-clock total of the
    critical set plus both fixtures as executed in that session, recorded against NO ceiling
    (Rec 47). Written once and recorded as registry rows exactly as receipts are.
    """
    if not critical_test_results or not fixture_results:
        raise _refuse(
            result_path,
            "the gate result records per-test AND per-fixture results; an empty set proves "
            "nothing ran in-session (TC-03g; R-141)",
        )
    missing_fixtures = [fid for fid in FIXTURE_IDS if fid not in fixture_results]
    if missing_fixtures:
        raise _refuse(result_path, f"fixture results missing for {missing_fixtures}")
    started = _parse_utc(started_at_utc, resource=f"{result_path}: started_at_utc")
    completed = _parse_utc(completed_at_utc, resource=f"{result_path}: completed_at_utc")
    if completed < started:
        raise _refuse(result_path, "completed_at_utc precedes started_at_utc")
    payload: dict[str, Any] = {
        "kind": GATE_RESULT_KIND,
        "platform": snapshot.platform,
        "environment_lock": lock_items(lock),
        "environment_lock_hash": environment_lock_hash(lock),
        "environment_identity": environment_identity(lock),
        "frozen_manifest_hashes": _frozen_hashes(manifests),
        "started_at_utc": started.isoformat(),
        "completed_at_utc": completed.isoformat(),
        "critical_test_results": dict(critical_test_results),
        "fixture_results": dict(fixture_results),
        "measured_total_runtime_seconds": (completed - started).total_seconds(),
        "runtime_ceiling": None,
        "runtime_ceiling_note": "recorded against no ceiling: no session or wall-clock limit "
        "exists in any authority and none is invented (R-141; Rec 47)",
        "registry_run_id": run_id,
        "gate_run_id": f"{run_id}/in_session_gate",
    }
    written = _write_once_json(result_path, payload)
    _child_rows(
        registry_path=registry_path,
        access_log_path=access_log_path,
        phase=phase,
        child_run_id=payload["gate_run_id"],
        template=registry_row,
        lock=lock,
        platform=snapshot.platform,
        artifact_path=written,
        kind=GATE_RESULT_KIND,
    )
    return payload


def read_gate_result(path: Path) -> dict[str, Any]:
    return _read_json(path, kind=GATE_RESULT_KIND)


def require_in_session_gate(
    result: Mapping[str, Any], *, lock: RunRecord, manifests: Mapping[str, Path]
) -> dict[str, Any]:
    """Refuse the three BENCH-01 substance violations before domain work (R-141).

    (30) a `local` stamp — wrong platform; (31) `code_commit` or config-snapshot hashes
    disagreeing with this run's own lock — wrong code; (32) frozen-manifest hashes disagreeing
    with the manifests in force — wrong manifests (a stale result predating a re-freeze).
    """
    if result.get("kind") != GATE_RESULT_KIND:
        raise _refuse(
            "in-session gate result",
            f"payload kind {result.get('kind')!r} is not a gate result",
        )
    platform = str(result.get("platform", ""))
    if platform != KAGGLE:
        raise _refuse(
            "in-session gate result",
            f"stamped platform {platform!r}; the critical set and both fixtures run INSIDE the "
            f"Kaggle session before any governed run there — a local result proves nothing about "
            f"that environment (TC-03g; TE 9.1/9.2; R-141 control 30)",
        )
    recorded = result.get("environment_lock")
    if not isinstance(recorded, Mapping):
        raise _refuse("in-session gate result", "no recorded TE 13.1 lock")
    caller = lock_items(lock)
    for item in ("code_commit", "config_hashes"):
        if lock_items(recorded)[item] != caller[item]:
            raise _refuse(
                "in-session gate result",
                f"recorded {item} disagrees with this governed run's own TE 13.1 lock; the gate "
                f"proves the environment of THIS run, not of an earlier session (BENCH-01; "
                f"R-141 control 31)",
            )
    in_force = _frozen_hashes(manifests)
    recorded_hashes = result.get("frozen_manifest_hashes")
    if not isinstance(recorded_hashes, Mapping) or {
        k: str(v) for k, v in recorded_hashes.items()
    } != in_force:
        raise _refuse(
            "in-session gate result",
            f"recorded frozen-manifest hashes {recorded_hashes!r} disagree with the manifests in "
            f"force {in_force!r}; a gate result predating the frozen manifests fails the way a "
            f"stale receipt does (R-141 control 32)",
        )
    return {
        "accepted": True,
        "platform": platform,
        "measured_total_runtime_seconds": result.get("measured_total_runtime_seconds"),
    }
