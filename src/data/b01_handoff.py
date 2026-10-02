"""B-01 cross-environment handoff: receipts bound across (b) -> (a), and admission in (a).

Purpose
-------
D-83 confines B-01 (IRI-2016 benchmark) generation to environment (b) `b01_iri` and every
stage script, the confirmatory set and the evaluation-time IRI join to environment (a)
`tec-thesis-311`. TE 9.2 makes `--generate-benchmark` a full-year job, so it calls
`require_receipts_for_snapshot`; `fixture_gate.verify_receipt` accepts a receipt only when
the receipt's environment identity equals the CALLER's (SD-X-02). Receipts exist in (a) and
(c) only, so a governed January-November generation in (b) refuses by construction. This
module is the drafted remedy; it has two halves with different authority.

1. `require_cross_environment_receipts` (runs in (b)). It accepts the (a) fixture receipts
   for a generation run in (b), provided that the code commit, the config-snapshot hashes and
   the platform are equal. It does NOT accept equal requirements hashes, pip freeze or
   runtime versions, because (b) is a different environment by design (D-49). This changes what a
   receipt binds to, so it is GATED: it refuses unless `evidence/DECISIONS.md` carries a
   `## D-<n>` section containing the literal `CROSS_ENVIRONMENT_RECEIPT_MARKER`. That entry
   is the Student's register act (project.md `code-generation:c5`, `c31`). Until it exists,
   the (b) generation refuses exactly as it does today, and nothing is weakened.
2. `admit_jan_nov_receipt` (runs in (a), ungated, strictly additive). The transferred
   January-November B-01 receipt is re-verified in (a) before anything consumes it:
   - transfer hashes;
   - the generating environment is `b01_iri`, recorded in a lock that hashes to the
     provenance's own `environment_lock_hash`;
   - the code commit and config hashes equal (a)'s own lock, with the only permitted
     `data.yaml` difference being the `gates` node, as D-83 revision 8 §A8 item 4 already
     allows;
   - the phase_id;
   - the row set equals the expected target grid exactly (no missing point, no extra point,
     no duplicate `(station_id, target_time_utc)`);
   - every `ok` row carries a finite, non-negative TECU value.

   Error rows are a completeness shortfall: counted and recorded in the marker, never
   fatal (team.md two-tier posture). A write-once admission marker records which
   environment generated the artifact and which admitted it, so the two are never blurred.

The module imports nothing from `src/external/` (TE 12 import boundary): the caller (script
04, an allowlisted importer) supplies the expected grid keys.

Inputs
------
Provenance JSON + rows JSONL + SHA-256 manifest as written by script 04's
`_generate_benchmark`; `RunRecord` locks; the receipt files `fixture_gate` reads;
`evidence/DECISIONS.md`.

Re-run behaviour
----------------
Every check is a pure read. The admission marker is written once; a second admission for the
same `phase_id` refuses. Every refusal raises `IntegrityError` naming the resource and the
violated expectation.
"""

from __future__ import annotations

import datetime as dt
import json
import math
import re
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any, Final

from src.data.config import ConfigSnapshot, IntegrityError, RunRecord, environment_lock_hash
from src.data.fixture_gate import (
    _registry_path_for,
    lock_from_items,
    lock_items,
    read_receipt,
    receipt_path_for,
    verify_receipt,
)
from src.data.fixture_manifest import (
    FIXTURE_IDS,
    PLUMBING_FIXTURE_ID,
    SCIENTIFIC_FIXTURE_ID,
    load_fixture_manifest,
    manifest_path_for,
)
from src.data.release import sha256_of_file

__all__ = [
    "GENERATING_ENVIRONMENT_ID",
    "ADMITTING_ENVIRONMENT_ID",
    "CROSS_ENVIRONMENT_RECEIPT_MARKER",
    "CROSS_BOUND_LOCK_ITEMS",
    "find_authorizing_decision",
    "require_cross_environment_receipts",
    "verify_transferred_receipt",
    "validate_b01_rows",
    "admission_marker_path",
    "admit_jan_nov_receipt",
    "require_jan_nov_admission",
]

#: D-83 revision 8 §A8 item 11: environment literals are pinned, never prose labels.
GENERATING_ENVIRONMENT_ID: Final[str] = "b01_iri"
ADMITTING_ENVIRONMENT_ID: Final[str] = "tec-thesis-311"
#: The literal the authorizing D-number must carry; the gate searches for it verbatim.
CROSS_ENVIRONMENT_RECEIPT_MARKER: Final[str] = (
    "cross_environment_receipt_binding: b01_iri <- tec-thesis-311"
)
#: The lock items that must still be EQUAL across (b) and (a): the code, the governed
#: configs and the platform. Requirements hash, pip freeze and runtime versions differ by
#: design (D-49), and the cross-binding exists only for that reason.
CROSS_BOUND_LOCK_ITEMS: Final[tuple[str, ...]] = ("code_commit", "config_hashes", "platform")
JAN_NOV: Final[list[int]] = list(range(1, 12))
DATA_YAML: Final[str] = "data.yaml"
_DECISION_HEADING = re.compile(r"^## (D-\d+)\b.*$", re.MULTILINE)


def _refuse(resource: object, expectation: str) -> IntegrityError:
    return IntegrityError(str(resource), expectation)


def find_authorizing_decision(decisions_path: Path) -> str:
    """The D-number whose section carries the marker literal; refuses when none does."""
    path = Path(decisions_path)
    if not path.is_file():
        raise _refuse(path, "the decision register is required to authorize cross-binding")
    text = path.read_text(encoding="utf-8")
    headings = list(_DECISION_HEADING.finditer(text))
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        if CROSS_ENVIRONMENT_RECEIPT_MARKER in text[heading.end() : end]:
            return heading.group(1)
    raise _refuse(
        path,
        f"no D-number section carries {CROSS_ENVIRONMENT_RECEIPT_MARKER!r}; accepting (a)'s "
        f"fixture receipts for a (b) B-01 generation changes what a receipt binds to "
        f"(SD-X-02), and is a governed act the Student records, never an agent default "
        f"(project.md code-generation:c5, c31)",
    )


def _cross_bound(items: Mapping[str, Any]) -> dict[str, Any]:
    return {name: items[name] for name in CROSS_BOUND_LOCK_ITEMS}


def require_cross_environment_receipts(
    snapshot: ConfigSnapshot,
    lock: RunRecord,
    *,
    decisions_path: Path,
    receipt_environment_id: str = ADMITTING_ENVIRONMENT_ID,
) -> dict[str, Any]:
    """In (b): accept (a)'s two receipts for a B-01 generation, under an authorizing D-number.

    Every `verify_receipt` integrity check still runs: the manifest is frozen and in force,
    the result is PASS, the payload's lock hashes to itself and to the append-only registry
    row, and the manifest is bound into the lock. The only check replaced is the
    caller-identity binding, which becomes: the receipt was written in
    `receipt_environment_id`, the caller is `GENERATING_ENVIRONMENT_ID`, and
    `CROSS_BOUND_LOCK_ITEMS` are equal.
    """
    decision = find_authorizing_decision(decisions_path)
    caller = lock_items(lock)
    if caller["environment_id"] != GENERATING_ENVIRONMENT_ID:
        raise _refuse(
            "environment lock",
            f"cross-environment receipts are accepted only for a B-01 generation in "
            f"{GENERATING_ENVIRONMENT_ID!r}; this run is {caller['environment_id']!r}",
        )
    workspace = Path(snapshot.resolved_roots["workspace"])
    registry = _registry_path_for(snapshot)
    payloads: dict[str, dict[str, Any]] = {}
    verified: dict[str, dict[str, Any]] = {}
    for fid in FIXTURE_IDS:
        receipt_path = receipt_path_for(workspace, fid)
        if not receipt_path.is_file():
            raise _refuse(
                receipt_path,
                f"no {fid} receipt; both fixtures pass before any full-year job (TE 9.2)",
            )
        payload = read_receipt(receipt_path)
        recorded = payload.get("environment_lock")
        if not isinstance(recorded, Mapping):
            raise _refuse(receipt_path, "receipt carries no recorded TE 13.1 lock")
        recorded_items = lock_items(recorded)
        if recorded_items["environment_id"] != receipt_environment_id:
            raise _refuse(
                receipt_path,
                f"receipt was written in {recorded_items['environment_id']!r}, not "
                f"{receipt_environment_id!r}",
            )
        # Every integrity check against the receipt's OWN lock (self-consistency, row, binding).
        verified[fid] = verify_receipt(
            payload,
            manifest=load_fixture_manifest(manifest_path_for(workspace, fid)),
            registry_path=registry,
            lock=lock_from_items(recorded),
            receipt_path=receipt_path,
        )
        for name in CROSS_BOUND_LOCK_ITEMS:
            if recorded_items[name] != caller[name]:
                raise _refuse(
                    receipt_path,
                    f"lock item {name!r} differs between the {receipt_environment_id} receipt "
                    f"({recorded_items[name]!r}) and this {GENERATING_ENVIRONMENT_ID} run "
                    f"({caller[name]!r}); cross-binding requires the same code, configs and "
                    f"platform",
                )
        payloads[fid] = payload
    cited = payloads[SCIENTIFIC_FIXTURE_ID].get("plumbing_receipt")
    plumbing = payloads[PLUMBING_FIXTURE_ID]
    if (
        not isinstance(cited, Mapping)
        or cited.get("receipt_run_id") != plumbing.get("receipt_run_id")
        or cited.get("frozen_manifest_hash") != plumbing.get("frozen_manifest_hash")
    ):
        raise _refuse(
            receipt_path_for(workspace, SCIENTIFIC_FIXTURE_ID),
            "the scientific receipt does not cite the plumbing receipt in force (R-140 control 26)",
        )
    return {
        "exempt": False,
        "cross_environment": True,
        "decision": decision,
        "receipt_environment_id": receipt_environment_id,
        "caller_environment_id": caller["environment_id"],
        "cross_bound": _cross_bound(caller),
        "receipts": verified,
    }


def _load_json(path: Path, *, what: str) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise _refuse(path, f"{what} unreadable ({exc})") from exc


def verify_transferred_receipt(prov_path: Path) -> dict[str, Any]:
    """Provenance, rows and SHA-256 manifest agree after transfer (missing or corrupt refuses)."""
    prov_path = Path(prov_path)
    if not prov_path.is_file():
        raise _refuse(prov_path, "the B-01 provenance file is missing")
    prov = _load_json(prov_path, what="B-01 provenance")
    if not isinstance(prov, Mapping):
        raise _refuse(prov_path, "B-01 provenance must be a JSON object")
    rows_name = str(prov.get("rows_file", ""))
    rows_path = prov_path.parent / rows_name
    if not rows_name or not rows_path.is_file():
        raise _refuse(rows_path, "the provenance's rows file is missing")
    if sha256_of_file(rows_path) != prov.get("rows_sha256"):
        raise _refuse(rows_path, "rows SHA-256 differs from the provenance (corrupt transfer)")
    manifest_path = prov_path.parent / rows_name.replace(
        "b01_iri2016_rows_", "b01_sha256_manifest_"
    ).replace(".jsonl", ".json")
    if not manifest_path.is_file():
        raise _refuse(manifest_path, "the SHA-256 manifest is missing")
    expected = {
        rows_path.name: sha256_of_file(rows_path),
        prov_path.name: sha256_of_file(prov_path),
    }
    if _load_json(manifest_path, what="B-01 manifest") != expected:
        raise _refuse(manifest_path, "manifest disagrees with the transferred files")
    return dict(prov)


def validate_b01_rows(
    rows: Iterable[Mapping[str, Any]],
    *,
    expected_keys: Iterable[tuple[str, str]],
    output_field: str,
    phase_id: str,
    resource: object,
) -> dict[str, Any]:
    """The row set equals the expected grid; no duplicates; `ok` values finite and >= 0."""
    expected = set(expected_keys)
    seen: set[tuple[str, str]] = set()
    errors = 0
    for index, row in enumerate(rows):
        key = (str(row.get("station_id")), str(row.get("target_time_utc")))
        if key in seen:
            raise _refuse(
                resource, f"duplicate (station_id, target_time_utc) {key} at row {index}"
            )
        seen.add(key)
        if row.get("phase_id") != phase_id:
            raise _refuse(
                resource, f"row {index} phase_id {row.get('phase_id')!r} != {phase_id!r}"
            )
        status = row.get("status")
        if status == "ok":
            value = row.get(output_field)
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise _refuse(resource, f"row {index} {output_field}={value!r} is not a number")
            if not math.isfinite(value) or value < 0:
                raise _refuse(
                    resource,
                    f"row {index} {output_field}={value!r} is not a finite non-negative TECU "
                    f"value (vertical TEC is a column density)",
                )
        elif status == "error":
            if row.get(output_field) is not None:
                raise _refuse(resource, f"row {index} is an error row carrying a value")
            errors += 1
        else:
            raise _refuse(resource, f"row {index} status {status!r} is neither 'ok' nor 'error'")
    missing, extra = expected - seen, seen - expected
    if missing or extra:
        raise _refuse(
            resource,
            f"row set is not the expected target grid: {len(missing)} missing "
            f"(e.g. {sorted(missing)[:3]}), {len(extra)} unexpected (e.g. {sorted(extra)[:3]})",
        )
    return {"rows": len(seen), "error_rows": errors, "ok_rows": len(seen) - errors}


def admission_marker_path(workspace: Path, phase_id: str) -> Path:
    return Path(workspace) / "evidence" / "b01_admission" / f"jan_nov_admission_{phase_id}.json"


def admit_jan_nov_receipt(
    prov_path: Path,
    *,
    snapshot: ConfigSnapshot,
    lock: RunRecord,
    phase_id: str,
    expected_keys: Iterable[tuple[str, str]],
    output_field: str,
    data_yaml_sans_gates_sha256: str,
) -> dict[str, Any]:
    """In (a): re-verify the transferred January-November B-01 receipt and write the marker."""
    caller = lock_items(lock)
    if caller["environment_id"] != ADMITTING_ENVIRONMENT_ID:
        raise _refuse(
            "environment lock",
            f"B-01 admission runs in {ADMITTING_ENVIRONMENT_ID!r}; this run is "
            f"{caller['environment_id']!r} (D-83 revision 8 item 1)",
        )
    prov = verify_transferred_receipt(prov_path)
    if prov.get("months") != JAN_NOV:
        raise _refuse(prov_path, f"not the January-November half: months {prov.get('months')!r}")
    if prov.get("phase_id") != phase_id:
        raise _refuse(prov_path, f"phase_id {prov.get('phase_id')!r} != {phase_id!r}")
    recorded = prov.get("environment_lock")
    if not isinstance(recorded, Mapping):
        raise _refuse(prov_path, "provenance records no generating-environment lock")
    recorded_items = lock_items(recorded)
    if environment_lock_hash(lock_from_items(recorded)) != prov.get("environment_lock_hash"):
        raise _refuse(prov_path, "recorded lock does not hash to environment_lock_hash (edited)")
    if recorded_items["environment_id"] != GENERATING_ENVIRONMENT_ID:
        raise _refuse(
            prov_path,
            f"generated in {recorded_items['environment_id']!r}, not "
            f"{GENERATING_ENVIRONMENT_ID!r} (D-83 revision 8 item 1)",
        )
    if recorded_items["code_commit"] != caller["code_commit"]:
        raise _refuse(
            prov_path,
            f"generated at code {recorded_items['code_commit']!r}; this admission runs at "
            f"{caller['code_commit']!r}",
        )
    recorded_cfg = dict(recorded_items["config_hashes"])
    current_cfg = dict(caller["config_hashes"])
    others_equal = {k: v for k, v in recorded_cfg.items() if k != DATA_YAML} == {
        k: v for k, v in current_cfg.items() if k != DATA_YAML
    }
    if not others_equal or set(recorded_cfg) != set(current_cfg):
        raise _refuse(
            prov_path,
            f"config hashes other than data.yaml differ: recorded {recorded_cfg} vs this run "
            f"{current_cfg}",
        )
    if recorded_cfg.get(DATA_YAML) != current_cfg.get(DATA_YAML) and (
        prov.get("data_yaml_sans_gates_sha256") != data_yaml_sans_gates_sha256
    ):
        raise _refuse(
            prov_path, "data.yaml differs outside the `gates` node (D-83 revision 8 item 4)"
        )
    rows_path = Path(prov_path).parent / str(prov["rows_file"])
    rows = []
    for number, line in enumerate(rows_path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise _refuse(rows_path, f"line {number} is not JSON ({exc})") from exc
    counts = validate_b01_rows(
        rows,
        expected_keys=expected_keys,
        output_field=output_field,
        phase_id=phase_id,
        resource=rows_path,
    )
    if counts["error_rows"] != prov.get("error_rows"):
        raise _refuse(
            prov_path,
            f"provenance records {prov.get('error_rows')} error rows, the file holds "
            f"{counts['error_rows']}",
        )
    marker = admission_marker_path(Path(snapshot.resolved_roots["workspace"]), phase_id)
    if marker.exists():
        raise _refuse(marker, f"a January-November B-01 half for {phase_id} is already admitted")
    marker.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "phase_id": phase_id,
        "months": JAN_NOV,
        "receipt": Path(prov_path).name,
        "receipt_sha256": sha256_of_file(Path(prov_path)),
        "rows_sha256": prov["rows_sha256"],
        "generating_environment_id": recorded_items["environment_id"],
        "generating_environment_lock_hash": prov["environment_lock_hash"],
        "admitting_environment_id": caller["environment_id"],
        "admitting_environment_lock_hash": environment_lock_hash(lock),
        "code_commit": caller["code_commit"],
        "row_counts": counts,
        "completeness_note": "error rows are a completeness shortfall, recorded, never imputed",
        "admitted_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    with marker.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, indent=2) + "\n")
    return {"jan_nov_marker": marker, **counts}


def require_jan_nov_admission(
    workspace: Path, phase_id: str, *, prov_path: Path
) -> dict[str, Any]:
    """Assembly consumes only the January-November half (a) admitted, byte for byte."""
    marker = admission_marker_path(workspace, phase_id)
    if not marker.is_file():
        raise _refuse(marker, "no admitted January-November B-01 half; admit it in (a) first")
    admitted = _load_json(marker, what="admission marker")
    if admitted.get("receipt_sha256") != sha256_of_file(Path(prov_path)):
        raise _refuse(prov_path, "the January-November half is not the receipt (a) admitted")
    return dict(admitted)
