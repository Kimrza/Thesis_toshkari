"""WS-20 / TA-17: the clean run — every fixture-and-reproducibility hard rule's negative control.

PURPOSE. `fixtures-and-reproducibility` W-1 … W-10 (R-133 … R-142): the thirty-nine
negative controls and eleven must-not-fire controls of `business-rules.md`
§ Negative-control count, hosted on SYNTHETIC trees (tmp_path; synthetic manifests,
receipts, registry rows, planted records, mislabelled directories, single-bit plants —
declared constants of the test apparatus, R-122; NO real config value, NO December 2022
content, NO restricted path). Plus: the per-area TE 15.2 enumeration (one case per area,
R-133 control 1), the ONLY-COPY scan (a second YAML parse of a fixture manifest anywhere
under `src/`, `scripts/` or `tests/` outside the one loader fails — R-133 control 4,
project-wide per Q2 = A), the executed-command comparison against TE 13.2's Phase 1
enumeration PARSED FROM THE TE FENCE (order AND membership, names and flags verbatim, the
ruled scope argument recognised — R-138 controls 18 and 39), and the clean-run COMPLETION
test, which runs the real sequence only when every precondition holds and otherwise SKIPS
with the exact stop-and-report reason (TE 18.3) — it NEVER passes on an abort.

CONSTANTS CONVENTION (R-122). The synthetic windows (year 2001), station token, partition
ids, tolerances, replicate counts and block lengths below are declared constants OF THE
TEST APPARATUS, explicitly NOT scientific values. No scientific constant is stated: the
frozen identities (D-11/D-14/D-20), seeds, partitions and tolerances live in
`evidence/DECISIONS.md`, `configs/` and the (not yet existing) fixture manifests. No
`fixture_manifest.yaml` exists under `tests/fixtures/` and NONE is authored here (BLK-02;
the two freeze acts are the owner's under Q-31).

INPUTS. `src/data/fixture_manifest.py` (through `parsed=`, the DOCUMENTED test-apparatus
injection point, because pyyaml is uninstallable on this clone — PyPI unreachable; the
production read path stays on pyyaml and its full-path controls `pytest.importorskip("yaml")`
and therefore SKIP BY NAME here, running in a governed environment), `fixture_gate`,
`fixture_evidence`, `run_walking_skeleton` (imported as a module), `acquisition`'s
record-date predicates (R-31 — consumed, never copied; the December rule's own negative
control lives in `tests/test_acquisition_window.py` and is not duplicated here), and the
TE document's 13.2 fence.

RE-RUN BEHAVIOUR. Pure: every tree is built fresh under tmp_path; nothing under the
repository is written; repeated runs are equivalent.

WHAT NO TEST HERE DISCHARGES. WS-20, TA-09, TA-17 and TA-21 stay `Pending`; neither
fixture has ever run; no measured value exists and none is invented; BLK-02 and BLK-08's
mechanism limb stay open; TA-03/TA-26's in-session evidence is unproducible off Kaggle;
TA-15 is not covered; G-05/G-06/G-07 stay `Blocked`. Smoke evidence only, never governed.

Run: pytest tests/test_clean_run.py -rs
"""

from __future__ import annotations

import datetime as dt
import inspect
import json
import re
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.acquisition import (  # noqa: E402
    assert_no_locked_month_records,
    assert_records_within_window,
)
from src.data.config import (  # noqa: E402
    IntegrityError,
    LeakageError,
    PhaseBoundaryError,
    RunRecord,
    environment_lock_hash,
)
from src.data.fixture_evidence import (  # noqa: E402
    DEFERRED_TO_G_P3A,
    PHASE1_ACCEPTANCE_ROWS,
    SMOKE_ONLY,
    FixtureArtifactStamp,
    assert_caveats_present,
    assert_freeze_record_agrees,
    assert_identity_agrees_with_decisions,
    assert_not_smoke_only,
    build_acceptance_table,
    build_environment_and_cpu_preflight_report,
    build_traceability_matrix,
    stamp_fixture_artifact,
    stamp_for_manifest,
)
from src.data.fixture_gate import (  # noqa: E402
    RECEIPT_KIND,
    environment_identity,
    fixture_input_version_tag,
    require_fixture_receipts,
    require_in_session_gate,
    verify_receipt,
    write_fixture_pass_receipt,
)
from src.data.fixture_manifest import (  # noqa: E402
    AREA_KEYS,
    CANDIDATE,
    FIXTURE_IDS,
    FROZEN,
    MANIFEST_NAME,
    PLUMBING_FIXTURE_ID,
    REQUIRED_OUTPUTS,
    SCIENTIFIC_FIXTURE_ID,
    SIBLING_HASH_NAME,
    FixtureManifest,
    assert_run_level_ranges,
    build_apparatus_partitions,
    compare_required_outputs,
    load_fixture_manifest,
    required_outputs_for,
    validate_manifest_mapping,
)
from src.data.release import sha256_of_file  # noqa: E402
from src.data.splits import PARTITION_IDS  # noqa: E402
from src.features.build import FrameSpec, assert_transform_identity  # noqa: E402
from src.features.transforms import Transform  # noqa: E402

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import run_walking_skeleton as skeleton  # noqa: E402

# --- apparatus constants (R-122: test apparatus, explicitly NOT scientific values) ---------

RUN_ID = "synthetic-measuring-run-0001"
PLUMBING_WINDOW = ("2001-11-01", "2001-11-07")
SCIENTIFIC_WINDOW = ("2001-03-01", "2001-03-31")
STATION = "SYNT"
CELL = "01/02"
WINDOW_DECISION = "D-901"
STATION_DECISION = "D-902"
ELIGIBILITY_DECISION = "D-903"
FREEZE_DECISION = "D-904"
APPARATUS_FOLD = "AP1"
APPARATUS_REFIT = "AP_REFIT"
TOLERANCED_OUTPUT = "metrics.json"
FP_TOLERANCE = 0.5  # apparatus tolerance of the SYNTHETIC ledger, never a scientific value
BOOTSTRAP = {"replicates": 3, "scored_range": {"hours": 96}, "block_counts": {"24": 4, "48": 2}}

TE_PATH = REPO_ROOT / "PreFlight" / "Technical_Environment_and_Research_Implementation(1)(2).md"


def _na() -> dict[str, str]:
    return {"status": "not_applicable", "reason": "Phase 2 quantity (TE 7.0 Phase 1 bar; Q3 = A)"}


def _measured(lo: float, hi: float, units: str = "count") -> dict[str, Any]:
    return {"min": lo, "max": hi, "units": units, "measuring_run_id": RUN_ID}


def _concrete_outputs(fixture_id: str) -> list[str]:
    outputs = []
    for required in required_outputs_for(fixture_id):
        if required.endswith(".*"):
            outputs.append(required[:-2] + (".png" if required.startswith("plots/") else ".json"))
        else:
            outputs.append(required)
    return outputs


def _identity(fixture_id: str, *, frozen: bool) -> dict[str, Any]:
    plumbing = fixture_id == PLUMBING_FIXTURE_ID
    start, end = PLUMBING_WINDOW if plumbing else SCIENTIFIC_WINDOW
    identity: dict[str, Any] = {
        "fixture_id": fixture_id,
        "stations": [STATION] if plumbing else ["SYNA", "SYNB", "SYNC"],
        "utc_dates": f"{start}..{end}",
        "selection_rule": "synthetic apparatus (R-122)",
        "creator": "test apparatus",
        "approval_status": "synthetic",
        "window_citation": {"decision": WINDOW_DECISION, "start_utc": start, "end_utc": end},
        "limitations": {
            "december_representativeness": "not_representative",
            "clauses": ["synthetic clause one", "synthetic clause two"],
        },
        "data07_caveat": "synthetic DATA-07 caveat: provenance unverifiable in principle",
        "eligibility_evidence": {"decision": ELIGIBILITY_DECISION, "source": "synthetic"},
        "phase_id": "P1",
        "source_id": "SRC-SYN",
        "target_definition_id": "TD-SYN",
    }
    if plumbing:
        identity["station_citation"] = {
            "decision": STATION_DECISION,
            "station_id": STATION,
            "cell": CELL,
        }
        identity["aruc_shortfall_status"] = {
            "status": "dormant",
            "reactivation_condition": "revives in full if ARUC is ever proposed",
        }
    if frozen:
        identity["freeze_citation"] = {"decision": FREEZE_DECISION}
    return identity


def _write_output_tree(root: Path, fixture_id: str) -> tuple[list[str], dict[str, str]]:
    outputs = _concrete_outputs(fixture_id)
    hashes: dict[str, str] = {}
    for index, name in enumerate(outputs):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if name == TOLERANCED_OUTPUT:
            path.write_text(json.dumps({"synthetic_metric": 1.0}), encoding="utf-8")
        else:
            path.write_text(f"synthetic output {index} of {fixture_id}\n", encoding="utf-8")
        hashes[name] = sha256_of_file(path)
    return outputs, hashes


def _ledger(outputs: list[str]) -> dict[str, dict[str, Any]]:
    ledger: dict[str, dict[str, Any]] = {}
    for name in outputs:
        if name == TOLERANCED_OUTPUT:
            ledger[name] = {
                "comparison_class": "toleranced",
                "units": "dimensionless",
                "producing_path": {"script": "scripts/07_evaluate_and_report.py"},
                "fp_tolerance": {
                    "value": FP_TOLERANCE,
                    "units": "dimensionless",
                    "measuring_run_id": RUN_ID,
                },
            }
        else:
            ledger[name] = {
                "comparison_class": "exact",
                "exact_kind": "hash",
                "units": "bytes",
                "producing_path": {"script": "scripts/run_walking_skeleton.py"},
            }
    return ledger


def build_manifest_mapping(fixture_id: str, root: Path, *, status: str) -> dict[str, Any]:
    """One complete, valid synthetic manifest mapping over a written output tree."""
    outputs, hashes = _write_output_tree(root, fixture_id)
    (root / "artifact_manifest.json").write_text(
        json.dumps({"fixture_id": fixture_id, "outputs": hashes}, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    data: dict[str, Any] = {
        "fixture_id": fixture_id,
        "status": status,
        "identity": _identity(fixture_id, frozen=status == FROZEN),
        "inputs": {
            "rinex_crx": _na(),
            "site_log": "synthetic",
            "dcb": _na(),
            "iri": "synthetic",
            "ionex": "synthetic",
            "space_weather": "synthetic",
            "prepared_vtec": {
                "evidence_dir": "evidence/synthetic_month",
                "sha256_manifest": "sha256_manifest.json",
                "files": {"records.csv": "0" * 64},
                "records_file": "records.csv",
            },
        },
        "processing": {
            "gnss_tec_version": _na(),
            "calibration_layer_commit": _na(),
            "full_config_id": "synthetic-config-id",
        },
        "expected_schema": {
            "raw": _na(),
            "intermediate": _na(),
            "hourly_target": "synthetic schema",
            "feature": "synthetic schema",
            "benchmark": "synthetic schema",
            "comparator": "synthetic schema",
            "prediction": "synthetic schema",
            "metric": "synthetic schema",
            "registry": "synthetic schema",
        },
        "units": {
            "utc_convention": "UTC",
            "coordinates": "degrees",
            "tecu": "TECU",
            "seconds_counts": "s",
            "external_index_units": "index",
        },
        "row_count_ranges": {
            "parsing": _na(),
            "valid_observation": _na(),
            "hourly_target": _measured(1, 999),
            "feature_window": _measured(1, 999),
            "split": _measured(1, 999),
        },
        "support_missingness": {
            "target_support": _measured(0, 99),
            "invalid_hour": _measured(0, 99),
            "external_feature": _measured(0, 99),
            "comparator": _measured(0, 99),
        },
        "timestamp_tolerances": {
            "parser": _na(),
            "hourly_boundary": _measured(0, 1, "s"),
            "iri": _measured(0, 1, "s"),
            "gim": _measured(0, 1, "s"),
            "feature_alignment": _measured(0, 1, "s"),
        },
        "independent_reference_checks": {
            "stec_vtec_intermediates": _na(),
            "hand_worked_dcb_pass": _na(),
            "sample_iri_gim_values": "synthetic spot-check record",
        },
        "required_outputs": {
            "artifact_manifest_ref": "artifact_manifest.json",
            "outputs": outputs,
            "comparison_ledger": _ledger(outputs),
        },
        "runtime": {
            "cpu_total": _measured(0.0, 3600.0, "s"),
            "storage_total": _measured(0, 10**9, "bytes"),
        },
        "numerical_variation": {
            "exact_fields": ["hash", "schema", "partition_membership", "id"],
            "floating_point_tolerances": _measured(0.0, FP_TOLERANCE, "dimensionless"),
        },
    }
    if fixture_id == SCIENTIFIC_FIXTURE_ID:
        data["runtime"]["widening_guard_cpu"] = _measured(0.0, 3600.0, "s")
        data["numerical_variation"]["planted_correlation_recovery_tolerance"] = _measured(
            0.0, 1.0, "dimensionless"
        )
        data["apparatus_partitions"] = {
            APPARATUS_FOLD: {
                "kind": "fold",
                "train_start": "2001-03-01",
                "train_end": "2001-03-20",
                "validation_month": "2001-03-25",
            },
            APPARATUS_REFIT: {
                "kind": "refit",
                "train_start": "2001-03-01",
                "train_end": "2001-03-28",
                "validation_month": None,
            },
        }
        data["fixture_bootstrap"] = json.loads(json.dumps(BOOTSTRAP))
    return data


def write_and_load(tmp_path: Path, fixture_id: str, *, status: str) -> FixtureManifest:
    """Write the synthetic manifest file (JSON text; hashing needs bytes, parsing uses
    `parsed=` because pyyaml is uninstallable here) plus its sibling when frozen, and load
    it through THE one loader."""
    root = tmp_path / fixture_id
    root.mkdir(parents=True, exist_ok=True)
    data = build_manifest_mapping(fixture_id, root, status=status)
    manifest_path = root / MANIFEST_NAME
    manifest_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    if status == FROZEN:
        (root / SIBLING_HASH_NAME).write_text(
            sha256_of_file(manifest_path) + "\n", encoding="utf-8"
        )
    return load_fixture_manifest(manifest_path, parsed=data)


def _lock(input_versions: list[str] | None = None, **overrides: Any) -> RunRecord:
    fields: dict[str, Any] = {
        "requirements_hash": "a" * 64,
        "pip_freeze": "synthetic==0.0",
        "runtime_versions": {"python": "3.11.16"},
        "code_commit": "c" * 40,
        "config_hashes": {"data.yaml": "d" * 64},
        "input_versions": list(input_versions or []),
        "platform": "local",
        "nondeterministic_ops": [],
    }
    fields.update(overrides)
    return RunRecord(**fields)


def _registry_template() -> dict[str, Any]:
    now = dt.datetime.now(dt.UTC).isoformat()
    return {
        "run_id": RUN_ID,
        "started_at_utc": now,
        "completed_at_utc": now,
        "status": "completed",
        "code_commit": "c" * 40,
        "environment_lock_hash": "",
        "platform": "local",
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
        "notes": "synthetic fixture-pass receipt apparatus (R-122)",
    }


DECISIONS_TEXT = f"""# Synthetic decision register (test apparatus)

## {WINDOW_DECISION} — synthetic window freeze
Window {PLUMBING_WINDOW[0]} to {PLUMBING_WINDOW[1]} inclusive; also cited for the
synthetic scientific window {SCIENTIFIC_WINDOW[0]} to {SCIENTIFIC_WINDOW[1]}.
synthetic clause one
synthetic clause two

## {STATION_DECISION} — synthetic station freeze
Station {STATION} {CELL} selected on synthetic evidence.

## {ELIGIBILITY_DECISION} — synthetic eligibility record
Recorded.

## {FREEZE_DECISION} — synthetic manifest freeze
fixture_manifest_sha256: HASHSENTINEL
"""


def _write_decisions(tmp_path: Path, *, freeze_hash: str = "") -> Path:
    path = tmp_path / "DECISIONS.md"
    path.write_text(
        DECISIONS_TEXT.replace("HASHSENTINEL", freeze_hash or "0" * 64), encoding="utf-8"
    )
    return path


# =========================================================================================
# W-1 / R-133 — the one schema, the one loader (controls 1–4, 37 + must-not-fire)
# =========================================================================================


def test_control_1_each_missing_area_fails_per_area_enumeration(tmp_path):
    """(1) A manifest missing ANY ONE of the twelve named areas fails — one case per area."""
    for area in AREA_KEYS:
        root = tmp_path / area
        root.mkdir()
        data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=CANDIDATE)
        del data[area]
        with pytest.raises(IntegrityError) as excinfo:
            validate_manifest_mapping(data, manifest_path=root / MANIFEST_NAME, file_sha256=None)
        assert area in str(excinfo.value)


def test_must_not_fire_full_manifest_validates_with_not_applicable_phase2(tmp_path):
    """Must-not-fire (R-133): all twelve blocks with Phase-2-only quantities `not_applicable`
    validate — candidate and frozen alike."""
    manifest = write_and_load(tmp_path, SCIENTIFIC_FIXTURE_ID, status=FROZEN)
    assert manifest.is_frozen
    candidate = write_and_load(tmp_path / "cand", PLUMBING_FIXTURE_ID, status=CANDIDATE)
    assert not candidate.is_frozen


def test_not_applicable_on_phase1_quantity_fails(tmp_path):
    """(Q3 = A) `not_applicable` on a Phase-1-applicable quantity fails."""
    root = tmp_path / "na"
    root.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=CANDIDATE)
    data["units"]["tecu"] = _na()
    with pytest.raises(IntegrityError, match="not_applicable"):
        validate_manifest_mapping(data, manifest_path=root / MANIFEST_NAME, file_sha256=None)


def test_control_2_hash_listing_absent_or_disagreeing_fails(tmp_path):
    """(2) An absent §15.4 listing, or a listing disagreeing with disk, fails."""
    root = tmp_path / "listing"
    root.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=CANDIDATE)
    (root / "artifact_manifest.json").unlink()
    with pytest.raises(IntegrityError, match="artifact_manifest"):
        validate_manifest_mapping(data, manifest_path=root / MANIFEST_NAME, file_sha256=None)
    root2 = tmp_path / "disk"
    root2.mkdir()
    data2 = build_manifest_mapping(PLUMBING_FIXTURE_ID, root2, status=CANDIDATE)
    (root2 / "split_manifest.json").write_text("tampered bytes", encoding="utf-8")
    with pytest.raises(IntegrityError, match="disagrees with disk|hashes to"):
        validate_manifest_mapping(data2, manifest_path=root2 / MANIFEST_NAME, file_sha256=None)


def test_control_3_required_output_without_ledger_entry_fails(tmp_path):
    """(3) A required output with no comparison-ledger entry fails."""
    root = tmp_path / "ledger"
    root.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=CANDIDATE)
    del data["required_outputs"]["comparison_ledger"]["split_manifest.json"]
    with pytest.raises(IntegrityError, match="comparison_ledger"):
        validate_manifest_mapping(data, manifest_path=root / MANIFEST_NAME, file_sha256=None)


def _yaml_parses_of_fixture_manifests(path: Path) -> list[int]:
    """AST scan: line numbers of `yaml.load`/`yaml.safe_load`/`yaml.full_load` calls whose
    argument subtree references a fixture manifest (an identifier, attribute or string
    literal mentioning `fixture_manifest`). A YAML parse of something else — a governed
    config, a synthetic test document — is NOT flagged; the control is about the ONE
    manifest contract having ONE parser (R-133 control 4)."""
    import ast

    tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    hits: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (
            isinstance(func, ast.Attribute)
            and func.attr in ("load", "safe_load", "full_load")
            and isinstance(func.value, ast.Name)
            and func.value.id == "yaml"
        ):
            continue
        mentions = False
        for arg in ast.walk(ast.Module(body=[ast.Expr(value=node)], type_ignores=[])):
            if isinstance(arg, ast.Name) and "fixture_manifest" in arg.id:
                mentions = True
            elif isinstance(arg, ast.Attribute) and "fixture_manifest" in arg.attr:
                mentions = True
            elif isinstance(arg, ast.Constant) and isinstance(arg.value, str) and (
                "fixture_manifest" in arg.value or "fixture-manifest" in arg.value
            ):
                mentions = True
        if mentions:
            hits.append(node.lineno)
    return hits


def test_control_4_only_copy_yaml_parse_scan_project_wide():
    """(4) A second YAML parse of a fixture manifest anywhere under src/, scripts/ or
    tests/ outside the one loader fails this scan (Q2 = A: project-wide)."""
    loader = REPO_ROOT / "src" / "data" / "fixture_manifest.py"
    offenders: list[str] = []
    for base in ("src", "scripts", "tests"):
        for path in sorted((REPO_ROOT / base).rglob("*.py")):
            if path.resolve() == loader.resolve():
                continue
            hits = _yaml_parses_of_fixture_manifests(path)
            if hits:
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{hits}")
    assert offenders == [], (
        f"second YAML parse of a fixture manifest outside the one loader: {offenders} "
        f"(R-133 control 4; two parsers of one contract drift independently)"
    )


def test_control_37_fixture_bootstrap_fields_and_divisibility(tmp_path):
    """(37) A scientific manifest missing any fixture_bootstrap field fails; an indivisible
    scored_range fails at freeze."""
    for key in ("replicates", "scored_range", "block_counts"):
        root = tmp_path / f"bs_{key}"
        root.mkdir()
        data = build_manifest_mapping(SCIENTIFIC_FIXTURE_ID, root, status=CANDIDATE)
        del data["fixture_bootstrap"][key]
        with pytest.raises(IntegrityError, match="fixture_bootstrap"):
            validate_manifest_mapping(data, manifest_path=root / MANIFEST_NAME, file_sha256=None)
    root = tmp_path / "bs_indivisible"
    root.mkdir()
    data = build_manifest_mapping(SCIENTIFIC_FIXTURE_ID, root, status=CANDIDATE)
    data["fixture_bootstrap"]["scored_range"] = {"hours": 100}
    with pytest.raises(IntegrityError, match="not evenly divisible|blocks"):
        validate_manifest_mapping(data, manifest_path=root / MANIFEST_NAME, file_sha256=None)


# =========================================================================================
# W-2 / R-134 — measure then freeze (controls 5–8 + must-not-fire)
# =========================================================================================


def test_control_5_candidate_manifest_cannot_produce_evidence(tmp_path):
    """(5) Evidence emitters and the comparison refuse a `candidate` manifest."""
    candidate = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status=CANDIDATE)
    frozen_sci = write_and_load(tmp_path / "sci", SCIENTIFIC_FIXTURE_ID, status=FROZEN)
    with pytest.raises(IntegrityError, match="candidate|frozen"):
        compare_required_outputs(candidate, tmp_path / PLUMBING_FIXTURE_ID)
    manifests = {PLUMBING_FIXTURE_ID: candidate, SCIENTIFIC_FIXTURE_ID: frozen_sci}
    with pytest.raises(IntegrityError, match="candidate"):
        build_traceability_matrix(
            [], workspace=REPO_ROOT, implemented_requirements=[], manifests=manifests
        )


def test_control_6_post_freeze_edit_fails_sibling_hash(tmp_path):
    """(6) A post-freeze edit without a new freeze act fails the sibling-hash check, and a
    candidate carrying a sibling raises (SD-X-01's negative control)."""
    manifest = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status=FROZEN)
    data = dict(manifest.data)
    manifest.path.write_text(
        manifest.path.read_text(encoding="utf-8") + "\n", encoding="utf-8"
    )  # the single-byte post-freeze edit
    with pytest.raises(IntegrityError, match="sibling|disagrees"):
        load_fixture_manifest(manifest.path, parsed=data)
    root = tmp_path / "cand"
    root.mkdir()
    cdata = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=CANDIDATE)
    cpath = root / MANIFEST_NAME
    cpath.write_text(json.dumps(cdata), encoding="utf-8")
    (root / SIBLING_HASH_NAME).write_text("f" * 64, encoding="utf-8")
    with pytest.raises(IntegrityError, match="candidate"):
        load_fixture_manifest(cpath, parsed=cdata)


def test_control_7_identity_disagreeing_with_cited_decision_fails(tmp_path):
    """(7) Identity fields disagreeing with the cited D-number record fail (F7's check)."""
    manifest = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status=CANDIDATE)
    decisions = _write_decisions(tmp_path)
    report = assert_identity_agrees_with_decisions(manifest, decisions_path=decisions)
    assert report["window_agrees"] and report["station_agrees"]  # must-not-fire limb
    bad = dict(manifest.data)
    bad_identity = json.loads(json.dumps(bad["identity"]))
    bad_identity["window_citation"]["end_utc"] = "2001-11-09"
    bad["identity"] = bad_identity
    root = tmp_path / "bad7"
    root.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=CANDIDATE)
    data["identity"] = bad_identity
    path = root / MANIFEST_NAME
    path.write_text(json.dumps(data), encoding="utf-8")
    disagreeing = load_fixture_manifest(path, parsed=data)
    with pytest.raises(IntegrityError, match="does not appear"):
        assert_identity_agrees_with_decisions(disagreeing, decisions_path=decisions)


def test_control_8_measured_field_without_run_id_is_unrepresentable(tmp_path):
    """(8) A measured field with no measuring-run registry id fails at the shape."""
    root = tmp_path / "prov"
    root.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=CANDIDATE)
    data["row_count_ranges"]["hourly_target"] = {"min": 1, "max": 2}
    with pytest.raises(IntegrityError, match="measuring_run_id"):
        validate_manifest_mapping(data, manifest_path=root / MANIFEST_NAME, file_sha256=None)


def test_freeze_record_agreement_and_sidecar_fallback(tmp_path):
    """SD-X-01 step 3: sibling hash == the freeze D-number's recorded hash; disagreement
    names both sites; the sidecar fallback is implemented behind the same function."""
    manifest = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status=FROZEN)
    decisions = _write_decisions(tmp_path, freeze_hash=manifest.sha256)
    report = assert_freeze_record_agrees(
        manifest.path, decisions_path=decisions, freeze_decision=FREEZE_DECISION
    )
    assert report["agrees"] and FREEZE_DECISION in str(report["source"])
    disagreeing = _write_decisions(tmp_path, freeze_hash="e" * 64)
    with pytest.raises(IntegrityError, match="disagrees"):
        assert_freeze_record_agrees(
            manifest.path, decisions_path=disagreeing, freeze_decision=FREEZE_DECISION
        )
    sidecar_dir = tmp_path / "sidecars"
    sidecar_dir.mkdir()
    (sidecar_dir / "D-999.json").write_text(
        json.dumps({"fixture_manifest_sha256": manifest.sha256}), encoding="utf-8"
    )
    report2 = assert_freeze_record_agrees(
        manifest.path,
        decisions_path=tmp_path / "absent.md",
        freeze_decision="D-999",
        sidecar_dir=sidecar_dir,
    )
    assert report2["agrees"] and "D-999.json" in str(report2["source"])


# =========================================================================================
# W-3 / R-135 — lineage (controls 9–12, 38 + must-not-fire)
# =========================================================================================


def _records(dates_stations: list[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"date": d, "station": s} for d, s in dates_stations]


def test_control_9_foreign_station_record_fails(tmp_path):
    """(9) A planted foreign-station record in the assembled plumbing input fails."""
    manifest = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status=CANDIDATE)
    records = _records([("2001-11-02", STATION), ("2001-11-03", "ARUC")])
    with pytest.raises(IntegrityError, match="cited station"):
        skeleton.assert_assembled_records(records, scope=manifest)


def test_control_10_manifest_naming_other_station_fails_citation(tmp_path):
    """(10) A manifest naming any station other than the cited one fails against the
    station decision's record."""
    root = tmp_path / "station"
    root.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=CANDIDATE)
    identity = json.loads(json.dumps(data["identity"]))
    identity["stations"] = ["OTHR"]
    identity["station_citation"]["station_id"] = "OTHR"
    identity["station_citation"]["cell"] = "09/09"
    data["identity"] = identity
    path = root / MANIFEST_NAME
    path.write_text(json.dumps(data), encoding="utf-8")
    manifest = load_fixture_manifest(path, parsed=data)
    with pytest.raises(IntegrityError, match="not the station"):
        assert_identity_agrees_with_decisions(
            manifest, decisions_path=_write_decisions(tmp_path)
        )


def test_control_11_and_38_coverage_figure_missing_either_caveat_fails():
    """(11) A coverage figure without the DATA-07 caveat fails; (38) one without
    `december_representativeness` fails — from either fixture."""
    with pytest.raises(IntegrityError, match="DATA-07"):
        assert_caveats_present(
            {"december_representativeness": "not_representative"}, surface="synthetic surface"
        )
    with pytest.raises(IntegrityError, match="december_representativeness|December"):
        assert_caveats_present({"data07_caveat": "present"}, surface="synthetic surface")
    assert_caveats_present(
        {"data07_caveat": "present", "december_representativeness": "not_representative"},
        surface="synthetic surface",
    )  # must-not-fire: both present


def _synthetic_month_evidence(tmp_path: Path) -> tuple[Path, dict[str, str]]:
    evidence_dir = tmp_path / "evidence" / "synthetic_month"
    evidence_dir.mkdir(parents=True)
    files = {}
    for name in ("records.csv", "coverage.json"):
        path = evidence_dir / name
        if name.endswith(".csv"):
            path.write_text("date,station\n2001-11-02,SYNT\n", encoding="utf-8")
        else:
            path.write_text("{}", encoding="utf-8")
        files[name] = sha256_of_file(path)
    (evidence_dir / "sha256_manifest.json").write_text(
        json.dumps(files, indent=2), encoding="utf-8"
    )
    return evidence_dir, files


def test_control_12_input_hash_disagreement_fails_before_the_run(tmp_path):
    """(12) An input artifact whose hash disagrees with the month's sha256_manifest.json
    fails BEFORE the fixture runs; the verified case proceeds (must-not-fire)."""
    evidence_dir, files = _synthetic_month_evidence(tmp_path)
    root = tmp_path / "fix"
    root.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=CANDIDATE)
    data["inputs"]["prepared_vtec"] = {
        "evidence_dir": "evidence/synthetic_month",
        "sha256_manifest": "sha256_manifest.json",
        "files": dict(files),
        "records_file": "records.csv",
    }
    path = root / MANIFEST_NAME
    path.write_text(json.dumps(data), encoding="utf-8")
    manifest = load_fixture_manifest(path, parsed=data)
    verified = skeleton.verify_declared_inputs(manifest, workspace=tmp_path)
    assert set(verified["verified"]) == set(files)  # must-not-fire: assembly proceeds
    (evidence_dir / "records.csv").write_text("date,station\nTAMPERED\n", encoding="utf-8")
    with pytest.raises(IntegrityError, match="bytes hash to|records"):
        skeleton.verify_declared_inputs(manifest, workspace=tmp_path)


# =========================================================================================
# W-4 / R-136 — smoke quarantine and record dates (controls 13–14 + must-not-fire)
# =========================================================================================


def test_control_13_smoke_only_artifact_refused_at_every_evidence_surface(tmp_path):
    """(13) A `smoke_only`-stamped artifact planted into a results artifact, the TA-09
    table or the matrix fails structurally."""
    smoke = {"fixture_stamp": {"evidence_class": SMOKE_ONLY}}
    with pytest.raises(IntegrityError, match="smoke"):
        assert_not_smoke_only(smoke, surface="results artifact")
    frozen = {
        fid: write_and_load(tmp_path / fid, fid, status=FROZEN) for fid in FIXTURE_IDS
    }
    row = {
        "requirement_id": "FR-WS-1",
        "decision_ref": WINDOW_DECISION,
        "test_or_experiment_ref": "test_acquisition_window.py",
        "evidence_artifact_id": "synthetic-evidence",
        **smoke,
    }
    with pytest.raises(IntegrityError, match="smoke"):
        build_traceability_matrix(
            [row], workspace=REPO_ROOT, implemented_requirements=["FR-WS-1"], manifests=frozen
        )


def test_control_14_december_record_caught_on_record_date_not_folder(tmp_path):
    """(14) A December-dated record planted in a fixture input is caught at assembly BY
    RECORD DATE, with the folder name deliberately mislabelled; the must-not-fire converse:
    a November-dated record in a directory whose name says December is ADMITTED."""
    mislabelled = tmp_path / "audit_evidence_2022-01"  # the TEC-09 history: label lies
    mislabelled.mkdir()
    (mislabelled / "records.csv").write_text(
        "date,station\n2022-12-05,SYNT\n", encoding="utf-8"
    )
    records = skeleton.read_records_csv(mislabelled / "records.csv")
    with pytest.raises(IntegrityError):
        assert_no_locked_month_records(records, timestamp_key="date")
    december_named = tmp_path / "december_2022_folder"
    december_named.mkdir()
    (december_named / "records.csv").write_text(
        "date,station\n2001-11-03,SYNT\n", encoding="utf-8"
    )
    admitted = skeleton.read_records_csv(december_named / "records.csv")
    assert_no_locked_month_records(admitted, timestamp_key="date")  # admitted: name ignored
    assert (
        assert_records_within_window(
            admitted,
            start=dt.date.fromisoformat(PLUMBING_WINDOW[0]),
            end=dt.date.fromisoformat(PLUMBING_WINDOW[1]),
            timestamp_key="date",
        )
        == 1
    )


# =========================================================================================
# W-5 / R-137 — apparatus partitions and the M10 step (controls 15–17 + must-not-fire)
# =========================================================================================


def test_control_15_frozen_partition_id_in_apparatus_declaration_fails(tmp_path):
    """(15) A frozen partition id in the apparatus declaration fails at the loader AND at
    `build_apparatus_partitions` (the by-hand wall)."""
    root = tmp_path / "frozenid"
    root.mkdir()
    data = build_manifest_mapping(SCIENTIFIC_FIXTURE_ID, root, status=CANDIDATE)
    declaration = json.loads(json.dumps(data["apparatus_partitions"][APPARATUS_FOLD]))
    data["apparatus_partitions"][PARTITION_IDS[0]] = declaration
    with pytest.raises(IntegrityError, match="frozen partition id"):
        validate_manifest_mapping(data, manifest_path=root / MANIFEST_NAME, file_sha256=None)
    valid = write_and_load(tmp_path / "byhand", SCIENTIFIC_FIXTURE_ID, status=CANDIDATE)
    tampered = json.loads(json.dumps(dict(valid.data)))
    tampered["apparatus_partitions"] = {PARTITION_IDS[0]: declaration}
    by_hand = FixtureManifest(
        path=valid.path,
        fixture_id=valid.fixture_id,
        status=valid.status,
        sha256=valid.sha256,
        data=tampered,
        artifact_manifest_path=valid.artifact_manifest_path,
        reference_files_present=valid.reference_files_present,
    )
    with pytest.raises(IntegrityError, match="frozen partition id"):
        build_apparatus_partitions(by_hand, embargo_hours=24)


def test_apparatus_partitions_build_and_are_quarantined(tmp_path):
    """Must-not-fire: the declared apparatus set builds, ids outside the six frozen ids."""
    manifest = write_and_load(tmp_path, SCIENTIFIC_FIXTURE_ID, status=CANDIDATE)
    partitions = build_apparatus_partitions(manifest, embargo_hours=24)
    ids = {p.partition_id for p in partitions}
    assert ids == {APPARATUS_FOLD, APPARATUS_REFIT}
    assert not (ids & set(PARTITION_IDS))


def test_control_16_fixture_partition_id_at_adr11_identity_check_raises():
    """(16) A fixture partition id offered to the ADR-11 identity check raises like any
    mismatched pair — no seventh enumerated exception is minted."""
    transform = Transform(
        transform_id=f"tr::{APPARATUS_FOLD}",
        partition_id=APPARATUS_FOLD,
        columns=("x",),
        means={"x": 0.0},
        scales={"x": 1.0},
        fitted_start=dt.datetime(2001, 3, 1, tzinfo=dt.UTC),
        fitted_end=dt.datetime(2001, 3, 20, tzinfo=dt.UTC),
    )
    spec = FrameSpec(
        "F1",
        "score",
        dt.datetime(2001, 3, 25, tzinfo=dt.UTC),
        dt.datetime(2001, 3, 26, tzinfo=dt.UTC),
    )
    with pytest.raises(LeakageError):
        assert_transform_identity(transform, spec)


def test_control_17_m10_step_wired_after_plumbing_and_never_a_receipt():
    """(17) The M10 step is a named part of the executed sequence: the command is exact,
    its modules exist, and the orchestrator invokes it on the plumbing branch. Must-not-fire:
    it is clean-run evidence, never a third receipt (the receipt id space stays two)."""
    command = skeleton.m10_command("pythonX")
    assert command == ["pythonX", "-m", "pytest", *skeleton.M10_MODULES]
    assert skeleton.M10_MODULES == (
        "tests/test_train_only_transforms.py",
        "tests/test_split_embargo.py",
    )
    for module in skeleton.M10_MODULES:
        assert (REPO_ROOT / module).is_file(), f"M10 module absent: {module}"
    source = inspect.getsource(skeleton._run)
    assert "m10_command" in source and "PLUMBING_FIXTURE_ID" in source, (
        "the M10 step is absent from the orchestrator's executed sequence (R-137 control 17)"
    )
    with pytest.raises(IntegrityError):
        fixture_input_version_tag("m10_contract_fixture", "0" * 64)  # no third receipt id


# =========================================================================================
# W-6 / R-138 — the amended §13.2 sequence (controls 18–20, 39 + must-not-fire)
# =========================================================================================


def _fence_segments() -> tuple[list[list[str]], list[list[str]]]:
    """Parse TE 13.2's fenced block: (Phase 1 python invocations, Phase 2 invocations)."""
    text = TE_PATH.read_text(encoding="utf-8", errors="replace")
    fence_match = re.search(r"```bash\n(.*?)```", text, re.DOTALL)
    assert fence_match, "TE 13.2 fence not found"
    lines = fence_match.group(1).splitlines()
    phase = 1
    segments: dict[int, list[list[str]]] = {1: [], 2: []}
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# Phase 2, only after G-P2"):
            phase = 2
            continue
        if stripped.startswith("python "):
            segments[phase].append(stripped.split())
    return segments[1], segments[2]


def test_control_18_and_39_sequence_matches_the_fence_membership_and_order():
    """(18)+(39): the executed command list equals §13.2's Phase 1 enumeration parsed from
    the TE fence — order AND membership, names and flags verbatim, the ruled scope argument
    recognised; a shuffled order is detected; the Phase 2 segment is deferred."""
    phase1, phase2 = _fence_segments()
    assert len(phase1) == 9, f"Phase 1 segment is 9 invocations, parsed {len(phase1)}"
    assert len(phase2) == 7, f"Phase 2 segment is 7 invocations, parsed {len(phase2)}"
    skeleton_calls = [argv for argv in phase1 if "run_walking_skeleton.py" in argv[1]]
    stage_calls = [argv for argv in phase1 if "run_walking_skeleton.py" not in argv[1]]
    assert len(skeleton_calls) == 2 and [c[-1] for c in skeleton_calls] == list(FIXTURE_IDS)
    fence_sequence = [
        (
            argv[1].removeprefix("scripts/"),
            int(argv[argv.index("--phase") + 1]) if "--phase" in argv else None,
        )
        for argv in stage_calls
    ]
    assert fence_sequence == list(skeleton.PHASE1_SEQUENCE), (
        f"PHASE1_SEQUENCE {list(skeleton.PHASE1_SEQUENCE)} disagrees with the fence "
        f"{fence_sequence} (order AND membership; R-138 controls 18/39)"
    )
    rotated = fence_sequence[1:] + fence_sequence[:1]
    assert rotated != list(skeleton.PHASE1_SEQUENCE)  # an out-of-order sequence is detected
    for argv in stage_calls:  # names and flags verbatim
        assert argv[0] == "python" and argv[2] == "--config" and argv[3] == "configs/"
    built = skeleton.build_phase1_commands(
        python="python",
        scripts_dir=Path("scripts"),
        config_dir=Path("configs/"),
        scope_path=Path("SCOPE"),
    )
    for argv, (script, phase) in zip(built, skeleton.PHASE1_SEQUENCE):
        core = [a for a in argv if a not in (skeleton.FIXTURE_SCOPE_OPTION, "SCOPE")]
        expected = ["python", str(Path("scripts") / script), "--config", str(Path("configs/"))]
        if phase is not None:
            expected += ["--phase", str(phase)]
        assert core == expected, (
            f"built invocation {core} is not the fence's verbatim form {expected} plus the "
            f"ruled scope argument (R-138 control 18)"
        )
    fence_phase2_only = {
        argv[1].removeprefix("scripts/")
        for argv in phase2
        if argv[1].removeprefix("scripts/") not in {s for s, _ in skeleton.PHASE1_SEQUENCE}
    }
    assert fence_phase2_only == set(skeleton.PHASE2_ONLY_SCRIPTS)


def test_control_39_phase2_only_invocation_raises_phase_boundary_error():
    """(39) A clean run that invokes a Phase-2-only script raises `PhaseBoundaryError`
    (governance-guards' exception, consumed — no fifteenth is minted); the seven Phase 1
    invocations pass (must-not-fire limb); an unknown script refuses."""
    for name in skeleton.PHASE2_ONLY_SCRIPTS:
        with pytest.raises(PhaseBoundaryError):
            skeleton.assert_phase1_invocation(name)
    for name, _phase in skeleton.PHASE1_SEQUENCE:
        skeleton.assert_phase1_invocation(name)
    with pytest.raises(IntegrityError):
        skeleton.assert_phase1_invocation("99_invented_script.py")


def test_control_19_no_gpu_visible_in_the_child_environment():
    """(19) The clean run executes with CUDA_VISIBLE_DEVICES="" — a completion that needs
    a visible GPU cannot happen; the parent's GPU setting is overridden."""
    env = skeleton.child_environment(
        {"PYTHONHASHSEED": "0", "CUDA_VISIBLE_DEVICES": "0"}, workspace=REPO_ROOT
    )
    assert env["CUDA_VISIBLE_DEVICES"] == ""
    report_gate = build_environment_and_cpu_preflight_report
    signature = inspect.signature(report_gate)
    assert "clean_run_result" in signature.parameters  # G-07 reads the CPU record as a field


def test_control_20_pythonhashseed_unset_or_late_fails():
    """(20) PYTHONHASHSEED unset (or set only after the first command would run) fails —
    the amended §13.2 clause tested as amended."""
    with pytest.raises(IntegrityError, match="PYTHONHASHSEED"):
        skeleton.child_environment({}, workspace=REPO_ROOT)
    with pytest.raises(IntegrityError, match="PYTHONHASHSEED"):
        skeleton.child_environment({"PYTHONHASHSEED": ""}, workspace=REPO_ROOT)


# =========================================================================================
# W-6 / R-139 — the comparison ledger (controls 21–25 + must-not-fire)
# =========================================================================================


def test_control_21_single_bit_plant_in_exact_artifact_fails(tmp_path):
    """(21) A planted single-bit change in an exact-class artifact fails; the untouched
    tree matches (must-not-fire: the matched-artifact report renders)."""
    manifest = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status=FROZEN)
    produced = tmp_path / "produced"
    for name in manifest.outputs:
        src = manifest.artifact_manifest_path.parent / name
        dst = produced / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
    report = compare_required_outputs(manifest, produced)
    assert report["artifact_class"] == "matched_artifact_report"
    target = produced / "split_manifest.json"
    raw = bytearray(target.read_bytes())
    raw[0] ^= 0x01  # the single-bit plant
    target.write_bytes(bytes(raw))
    with pytest.raises(IntegrityError, match="exact-class"):
        compare_required_outputs(manifest, produced)


def test_control_22_no_tolerance_lives_in_a_test_body(tmp_path):
    """(22) A tolerance sourced from a test body fails: the comparison accepts NO tolerance
    argument (only the manifest's ledger), and a toleranced entry without a manifest
    tolerance refuses at validation."""
    signature = inspect.signature(compare_required_outputs)
    assert list(signature.parameters) == ["manifest", "produced_root"], (
        "compare_required_outputs must accept no caller tolerance (R-139 control 22)"
    )
    root = tmp_path / "notol"
    root.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=CANDIDATE)
    del data["required_outputs"]["comparison_ledger"][TOLERANCED_OUTPUT]["fp_tolerance"]
    with pytest.raises(IntegrityError, match="fp_tolerance"):
        validate_manifest_mapping(data, manifest_path=root / MANIFEST_NAME, file_sha256=None)


def test_control_23_exact_mismatch_never_updates_the_expectation(tmp_path):
    """(23) An exact-class mismatch raises AND the manifest and its hash listing are
    byte-identical afterwards — §13.7's no-silent-update made executable."""
    manifest = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status=FROZEN)
    manifest_bytes = manifest.path.read_bytes()
    listing_bytes = manifest.artifact_manifest_path.read_bytes()
    produced = tmp_path / "produced"
    for name in manifest.outputs:
        dst = produced / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((manifest.artifact_manifest_path.parent / name).read_bytes())
    (produced / "mask_manifest.json").write_text("mismatching bytes", encoding="utf-8")
    with pytest.raises(IntegrityError):
        compare_required_outputs(manifest, produced)
    assert manifest.path.read_bytes() == manifest_bytes
    assert manifest.artifact_manifest_path.read_bytes() == listing_bytes


def test_control_24_runtime_or_storage_outside_measured_range_fails(tmp_path):
    """(24) A runtime or storage figure outside the manifest's measured range fails."""
    manifest = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status=FROZEN)
    within = assert_run_level_ranges(manifest, runtime_seconds=10.0, storage_bytes=100)
    assert within["within"]  # must-not-fire limb
    with pytest.raises(IntegrityError, match="runtime"):
        assert_run_level_ranges(manifest, runtime_seconds=1e9, storage_bytes=100)
    with pytest.raises(IntegrityError, match="storage"):
        assert_run_level_ranges(manifest, runtime_seconds=10.0, storage_bytes=10**12)


def test_control_25_tecu_tolerance_without_inverse_route_is_not_freezable(tmp_path):
    """(25) A toleranced entry declaring TECU units for an output whose producing path
    declares no inverse route is refused (BLK-08 checked, not inherited); with a declared
    inverse route it validates (must-not-fire)."""
    root = tmp_path / "tecu"
    root.mkdir()
    data = build_manifest_mapping(PLUMBING_FIXTURE_ID, root, status=CANDIDATE)
    entry = data["required_outputs"]["comparison_ledger"][TOLERANCED_OUTPUT]
    entry["units"] = "TECU"
    entry["fp_tolerance"]["units"] = "TECU"
    with pytest.raises(IntegrityError, match="inverse_route|TECU"):
        validate_manifest_mapping(data, manifest_path=root / MANIFEST_NAME, file_sha256=None)
    entry["producing_path"]["inverse_route"] = "evaluation.inverse_before_metric (R-103/R-104)"
    validate_manifest_mapping(data, manifest_path=root / MANIFEST_NAME, file_sha256=None)


# =========================================================================================
# W-7 / R-140 — receipts (controls 26–29 + must-not-fire, on synthetic trees)
# =========================================================================================


def _receipt_fixture(tmp_path: Path, fixture_id: str) -> dict[str, Any]:
    manifest = write_and_load(tmp_path / fixture_id, fixture_id, status=FROZEN)
    tag = fixture_input_version_tag(fixture_id, manifest.sha256)
    lock = _lock(input_versions=[tag])
    return {
        "manifest": manifest,
        "lock": lock,
        "tag": tag,
        "registry": tmp_path / "registry" / "experiment_registry.jsonl",
        "access_log": tmp_path / "registry" / "access_log.jsonl",
        "receipt_path": tmp_path / fixture_id / "fixture_pass_receipt.json",
    }


class _Snapshot:
    """Duck-typed stand-in for ConfigSnapshot where only `.platform` is consumed."""

    platform = "local"


def test_control_29_receipt_from_candidate_manifest_refused_at_write_time(tmp_path):
    """(29) A receipt written from a `candidate` manifest is refused at write time."""
    candidate = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status=CANDIDATE)
    with pytest.raises(IntegrityError, match="FROZEN|frozen"):
        write_fixture_pass_receipt(
            manifest=candidate,
            result="PASS",
            run_id=RUN_ID,
            lock=_lock(),
            snapshot=_Snapshot(),
            registry_path=tmp_path / "reg.jsonl",
            access_log_path=tmp_path / "log.jsonl",
            receipt_path=tmp_path / "receipt.json",
            registry_row=_registry_template(),
            phase=1,
        )


def test_control_26_scientific_without_plumbing_receipt_raises(tmp_path):
    """(26, write limb) The scientific receipt refuses to be written without the plumbing
    receipt it must cite; a failed result is never a receipt."""
    apparatus = _receipt_fixture(tmp_path, SCIENTIFIC_FIXTURE_ID)
    with pytest.raises(IntegrityError, match="plumbing"):
        write_fixture_pass_receipt(
            manifest=apparatus["manifest"],
            result="PASS",
            run_id=RUN_ID,
            lock=apparatus["lock"],
            snapshot=_Snapshot(),
            registry_path=apparatus["registry"],
            access_log_path=apparatus["access_log"],
            receipt_path=apparatus["receipt_path"],
            registry_row=_registry_template(),
            phase=1,
            plumbing_receipt=None,
        )
    with pytest.raises(IntegrityError, match="aborted|not"):
        write_fixture_pass_receipt(
            manifest=apparatus["manifest"],
            result="FAIL",
            run_id=RUN_ID,
            lock=apparatus["lock"],
            snapshot=_Snapshot(),
            registry_path=apparatus["registry"],
            access_log_path=apparatus["access_log"],
            receipt_path=apparatus["receipt_path"],
            registry_row=_registry_template(),
            phase=1,
        )


def test_control_27_full_year_invocation_without_both_receipts_raises(tmp_path):
    """(27) A full-year invocation without both receipts raises, asserted through the
    exported check on a synthetic tree (no real full-year job exists under any candidate)."""
    with pytest.raises(IntegrityError, match="both fixtures|missing"):
        require_fixture_receipts(
            tmp_path / "reg.jsonl", manifests={}, receipts={}, lock=_lock()
        )


def test_control_28_receipt_hash_disagreeing_with_frozen_manifest_raises(tmp_path):
    """(28) A receipt whose manifest hash disagrees with the frozen manifest in force
    raises — a re-freeze invalidates old receipts by construction."""
    apparatus = _receipt_fixture(tmp_path, PLUMBING_FIXTURE_ID)
    stale = {
        "kind": RECEIPT_KIND,
        "fixture_id": PLUMBING_FIXTURE_ID,
        "frozen_manifest_hash": "e" * 64,  # a superseded freeze
        "result": "PASS",
        "registry_run_id": RUN_ID,
        "receipt_run_id": f"{RUN_ID}/receipt/{PLUMBING_FIXTURE_ID}",
        "environment_lock": {},
        "environment_lock_hash": "",
    }
    with pytest.raises(IntegrityError, match="re-frozen|invalidates"):
        verify_receipt(
            stale,
            manifest=apparatus["manifest"],
            registry_path=apparatus["registry"],
            lock=apparatus["lock"],
            receipt_path=apparatus["receipt_path"],
        )


def test_must_not_fire_two_receipts_in_order_pass(tmp_path):
    """Must-not-fire (R-140): both receipts written under frozen manifests, in order, each
    bound to the manifest hash in force, verify and the ordering citation agrees."""
    plumbing = _receipt_fixture(tmp_path, PLUMBING_FIXTURE_ID)
    payload_p = write_fixture_pass_receipt(
        manifest=plumbing["manifest"],
        result="PASS",
        run_id=RUN_ID,
        lock=plumbing["lock"],
        snapshot=_Snapshot(),
        registry_path=plumbing["registry"],
        access_log_path=plumbing["access_log"],
        receipt_path=plumbing["receipt_path"],
        registry_row=_registry_template(),
        phase=1,
    )
    scientific = _receipt_fixture(tmp_path, SCIENTIFIC_FIXTURE_ID)
    payload_s = write_fixture_pass_receipt(
        manifest=scientific["manifest"],
        result="PASS",
        run_id=RUN_ID,
        lock=scientific["lock"],
        snapshot=_Snapshot(),
        registry_path=plumbing["registry"],
        access_log_path=plumbing["access_log"],
        receipt_path=scientific["receipt_path"],
        registry_row=_registry_template(),
        phase=1,
        plumbing_receipt=payload_p,
    )
    caller_lock = _lock()  # same environment, its own (empty) input versions
    for apparatus, payload in ((plumbing, payload_p), (scientific, payload_s)):
        verified = verify_receipt(
            payload,
            manifest=apparatus["manifest"],
            registry_path=plumbing["registry"],
            lock=caller_lock,
            receipt_path=apparatus["receipt_path"],
        )
        assert verified["accepted"]
    cited = payload_s["plumbing_receipt"]
    assert cited["receipt_run_id"] == payload_p["receipt_run_id"]
    assert cited["frozen_manifest_hash"] == payload_p["frozen_manifest_hash"]
    edited = json.loads(json.dumps(payload_p))
    edited["environment_lock"]["platform"] = "kaggle"  # the SD-X-02 Rec 7 tamper case
    with pytest.raises(IntegrityError, match="edited|hash"):
        verify_receipt(
            edited,
            manifest=plumbing["manifest"],
            registry_path=plumbing["registry"],
            lock=caller_lock,
            receipt_path=plumbing["receipt_path"],
        )


def test_receipt_lock_binding_and_environment_identity(tmp_path):
    """SD-X-02: a receipt is accepted iff its recorded lock matches the caller's own — a
    changed environment invalidates it; and the write refuses a lock that does not bind the
    frozen manifest (the row-hashed binding)."""
    plumbing = _receipt_fixture(tmp_path, PLUMBING_FIXTURE_ID)
    payload = write_fixture_pass_receipt(
        manifest=plumbing["manifest"],
        result="PASS",
        run_id=RUN_ID,
        lock=plumbing["lock"],
        snapshot=_Snapshot(),
        registry_path=plumbing["registry"],
        access_log_path=plumbing["access_log"],
        receipt_path=plumbing["receipt_path"],
        registry_row=_registry_template(),
        phase=1,
    )
    changed = _lock(pip_freeze="synthetic==9.9")  # a re-install
    assert environment_identity(changed) != environment_identity(plumbing["lock"])
    with pytest.raises(IntegrityError, match="differs|environment"):
        verify_receipt(
            payload,
            manifest=plumbing["manifest"],
            registry_path=plumbing["registry"],
            lock=changed,
            receipt_path=plumbing["receipt_path"],
        )
    with pytest.raises(IntegrityError, match="input_versions"):
        write_fixture_pass_receipt(
            manifest=plumbing["manifest"],
            result="PASS",
            run_id=RUN_ID + "-2",
            lock=_lock(),  # no manifest tag in the lock
            snapshot=_Snapshot(),
            registry_path=plumbing["registry"],
            access_log_path=plumbing["access_log"],
            receipt_path=tmp_path / "second_receipt.json",
            registry_row=_registry_template(),
            phase=1,
        )


def test_exported_check_full_path_requires_yaml(tmp_path):
    """The exported `require_fixture_receipts` full path (and its Q5 exemption through
    `load_fixture_scope`) reads manifests from disk — the production pyyaml path. Runs in a
    governed environment; SKIPS BY NAME here."""
    pytest.importorskip("yaml")
    plumbing = _receipt_fixture(tmp_path, PLUMBING_FIXTURE_ID)
    scientific = _receipt_fixture(tmp_path, SCIENTIFIC_FIXTURE_ID)
    with pytest.raises(IntegrityError, match="receipt"):
        require_fixture_receipts(
            plumbing["registry"],
            manifests={
                PLUMBING_FIXTURE_ID: plumbing["manifest"].path,
                SCIENTIFIC_FIXTURE_ID: scientific["manifest"].path,
            },
            receipts={
                PLUMBING_FIXTURE_ID: plumbing["receipt_path"],
                SCIENTIFIC_FIXTURE_ID: scientific["receipt_path"],
            },
            lock=_lock(),
        )


# =========================================================================================
# W-8 / R-141 — the in-session gate (controls 30–32 + must-not-fire)
# =========================================================================================


def _gate_payload(**overrides: Any) -> dict[str, Any]:
    lock = _lock(platform="kaggle")
    payload = {
        "kind": "in_session_gate_result",
        "platform": "kaggle",
        "environment_lock": {
            name: getattr(lock, name)
            for name in (
                "requirements_hash",
                "pip_freeze",
                "runtime_versions",
                "code_commit",
                "config_hashes",
                "input_versions",
                "platform",
                "nondeterministic_ops",
            )
        },
        "environment_lock_hash": environment_lock_hash(lock),
        "frozen_manifest_hashes": {},
        "critical_test_results": {"tests/test_iri_denial.py": "PASS"},
        "fixture_results": {fid: "PASS" for fid in FIXTURE_IDS},
        "measured_total_runtime_seconds": 1.0,
    }
    payload.update(overrides)
    return payload


def test_control_30_local_stamped_gate_result_fails():
    """(30) A `local`-stamped result offered as in-session evidence fails on the stamp."""
    with pytest.raises(IntegrityError, match="local|Kaggle"):
        require_in_session_gate(
            _gate_payload(platform="local"), lock=_lock(platform="kaggle"), manifests={}
        )


def test_control_31_lock_disagreement_fails():
    """(31) A gate result whose code commit disagrees with the governed run's own §13.1
    lock fails — the gate proves THIS run's environment (BENCH-01)."""
    caller = _lock(platform="kaggle", code_commit="f" * 40)
    with pytest.raises(IntegrityError, match="code_commit|own"):
        require_in_session_gate(_gate_payload(), lock=caller, manifests={})


def test_control_32_gate_result_predating_the_frozen_manifests_fails(tmp_path):
    """(32) A gate result predating the frozen manifests in force fails the same way a
    stale receipt does. Needs the production loader (pyyaml) — SKIPS BY NAME here."""
    pytest.importorskip("yaml")
    manifest = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status=FROZEN)
    sci = write_and_load(tmp_path / "sci", SCIENTIFIC_FIXTURE_ID, status=FROZEN)
    stale = _gate_payload(
        frozen_manifest_hashes={PLUMBING_FIXTURE_ID: "0" * 64, SCIENTIFIC_FIXTURE_ID: "1" * 64}
    )
    with pytest.raises(IntegrityError, match="predating|disagree"):
        require_in_session_gate(
            stale,
            lock=_lock(platform="kaggle"),
            manifests={PLUMBING_FIXTURE_ID: manifest.path, SCIENTIFIC_FIXTURE_ID: sci.path},
        )


# =========================================================================================
# W-9 / R-142 — the three generated evidence artifacts (controls 33–36 + must-not-fire)
# =========================================================================================


def _frozen_pair(tmp_path: Path) -> dict[str, FixtureManifest]:
    return {fid: write_and_load(tmp_path / fid, fid, status=FROZEN) for fid in FIXTURE_IDS}


def _receipt_payload(manifest: FixtureManifest, run_suffix: str) -> dict[str, Any]:
    return {
        "kind": RECEIPT_KIND,
        "fixture_id": manifest.fixture_id,
        "frozen_manifest_hash": manifest.sha256,
        "result": "PASS",
        "registry_run_id": RUN_ID,
        "receipt_run_id": f"{RUN_ID}/receipt/{run_suffix}",
    }


def test_control_33_matrix_row_citing_absent_module_fails(tmp_path):
    """(33) A matrix row citing a test module absent from the workspace fails (a PRESENCE
    check, never coverage: TA-15 is not read as covered by a matching filename); a row
    citing an existing module passes; completeness is asserted against the implemented
    list; a row missing a mandatory link fails."""
    manifests = _frozen_pair(tmp_path)
    good = {
        "requirement_id": "FR-WS-1",
        "decision_ref": WINDOW_DECISION,
        "test_or_experiment_ref": "test_acquisition_window.py",
        "evidence_artifact_id": "synthetic-evidence",
    }
    matrix = build_traceability_matrix(
        [good], workspace=REPO_ROOT, implemented_requirements=["FR-WS-1"], manifests=manifests
    )
    assert matrix["row_count"] == 1 and "TA-15" in matrix["presence_not_coverage"]
    absent = dict(good, test_or_experiment_ref="test_nonexistent_module.py")
    with pytest.raises(IntegrityError, match="absent"):
        build_traceability_matrix(
            [absent],
            workspace=REPO_ROOT,
            implemented_requirements=["FR-WS-1"],
            manifests=manifests,
        )
    with pytest.raises(IntegrityError, match="matrix row"):
        build_traceability_matrix(
            [good],
            workspace=REPO_ROOT,
            implemented_requirements=["FR-WS-1", "FR-WS-5"],
            manifests=manifests,
        )
    missing_link = dict(good)
    del missing_link["decision_ref"]
    with pytest.raises(IntegrityError, match="mandatory link"):
        build_traceability_matrix(
            [missing_link],
            workspace=REPO_ROOT,
            implemented_requirements=["FR-WS-1"],
            manifests=manifests,
        )


def _acceptance_rows(receipt_ref: str) -> list[dict[str, Any]]:
    return [
        {
            "ws_row_id": ws,
            "status": "PASS",
            "evidence_link": f"synthetic-evidence-{ws}",
            "producing_script_or_test": "tests/test_clean_run.py",
            "receipt_ref": receipt_ref,
        }
        for ws in PHASE1_ACCEPTANCE_ROWS
    ]


def test_control_34_and_35_acceptance_table_bounds(tmp_path):
    """(34) A PASS without an evidence link fails; (35) any WS-02…WS-08 row raises — the
    G-P3A deferral is a raise, not a footnote; must-not-fire: the complete 13-row table
    renders with the deferral stated on it."""
    manifests = _frozen_pair(tmp_path)
    receipts = {
        fid: _receipt_payload(manifests[fid], fid) for fid in FIXTURE_IDS
    }
    receipt_ref = receipts[PLUMBING_FIXTURE_ID]["receipt_run_id"]
    rows = _acceptance_rows(receipt_ref)
    table = build_acceptance_table(rows, manifests=manifests, receipts=receipts)
    assert table["row_count"] == len(PHASE1_ACCEPTANCE_ROWS) == 13
    assert table["deferred_to_G_P3A"] == list(DEFERRED_TO_G_P3A)
    assert "G-P3A" in table["deferral_statement"]
    no_evidence = [dict(rows[0], evidence_link="")] + rows[1:]
    with pytest.raises(IntegrityError, match="evidence link"):
        build_acceptance_table(no_evidence, manifests=manifests, receipts=receipts)
    deferred = rows + [
        {
            "ws_row_id": "WS-04",
            "status": "PASS",
            "evidence_link": "x",
            "producing_script_or_test": "x",
            "receipt_ref": receipt_ref,
        }
    ]
    with pytest.raises(IntegrityError, match="G-P3A"):
        build_acceptance_table(deferred, manifests=manifests, receipts=receipts)


def test_control_36_report_figure_missing_either_caveat_fails(tmp_path):
    """(36) A preflight report carrying a fixture coverage figure without the DATA-07
    caveat or the december_representativeness field fails; the GPU-visible completion
    fails too (control 19's report surface); the complete report renders (must-not-fire)
    and records the in-session gate's measured total runtime."""
    manifests = _frozen_pair(tmp_path)
    receipts = {fid: _receipt_payload(manifests[fid], fid) for fid in FIXTURE_IDS}
    clean = {
        "cuda_visible_devices": "",
        "completed": True,
        "runtime_seconds": 1.0,
        "storage_bytes": 10,
        "matched_artifact_report": {"outputs": {}},
    }
    figure = {
        "figure": "synthetic coverage",
        "data07_caveat": "synthetic caveat",
        "december_representativeness": "not_representative",
    }
    report = build_environment_and_cpu_preflight_report(
        lock=_lock(),
        platform="local",
        clean_run_result=clean,
        receipts=receipts,
        gate_result={"measured_total_runtime_seconds": 2.5},
        manifests=manifests,
        coverage_figures=[figure],
    )
    assert report["gate"].startswith("G-07")
    assert report["in_session_gate_measured_total_runtime_seconds"] == 2.5
    assert "aws_ai_dlc_preflight_report" in report["not_this"]
    bad_figure = {"figure": "synthetic coverage"}
    with pytest.raises(IntegrityError, match="DATA-07"):
        build_environment_and_cpu_preflight_report(
            lock=_lock(),
            platform="local",
            clean_run_result=clean,
            receipts=receipts,
            gate_result=None,
            manifests=manifests,
            coverage_figures=[bad_figure],
        )
    with pytest.raises(IntegrityError, match="GPU|CPU"):
        build_environment_and_cpu_preflight_report(
            lock=_lock(),
            platform="local",
            clean_run_result=dict(clean, cuda_visible_devices="0"),
            receipts=receipts,
            gate_result=None,
            manifests=manifests,
        )


def test_stamp_travels_and_is_never_rewritten(tmp_path):
    """R-110's pattern: the stamp is derived from the scope, embeds once, and a DIFFERENT
    stamp on the same payload refuses; plumbing artifacts are `smoke_only`, scientific are
    not (the quarantine's correct scope)."""
    plumbing = write_and_load(tmp_path, PLUMBING_FIXTURE_ID, status=CANDIDATE)
    scientific = write_and_load(tmp_path / "s", SCIENTIFIC_FIXTURE_ID, status=CANDIDATE)
    smoke_stamp = stamp_for_manifest(plumbing)
    science_stamp = stamp_for_manifest(scientific, apparatus_partition_id=APPARATUS_FOLD)
    assert smoke_stamp.evidence_class == SMOKE_ONLY
    assert science_stamp.evidence_class != SMOKE_ONLY
    assert science_stamp.apparatus_partition_id == APPARATUS_FOLD
    payload = stamp_fixture_artifact({"kind": "synthetic"}, smoke_stamp)
    assert payload["fixture_stamp"]["december_representativeness"] == "not_representative"
    with pytest.raises(IntegrityError, match="DIFFERENT"):
        stamp_fixture_artifact(payload, science_stamp)
    with pytest.raises(IntegrityError, match="december_representativeness"):
        stamp_fixture_artifact(
            {}, FixtureArtifactStamp(
                evidence_class=SMOKE_ONLY,
                fixture_id=PLUMBING_FIXTURE_ID,
                data07_caveat="x",
                december_representativeness="representative",
                phase_id="P1",
                source_id="S",
                target_definition_id="T",
            )
        )


# =========================================================================================
# W-10 — the clean-run completion test, the fence, the counts
# =========================================================================================


def _completion_preconditions() -> str | None:
    """The FIRST unmet precondition of the real §13.2 clean run, or None when all hold
    (TE 18.3 stop-and-report, named — never worked around)."""
    for module, pin_note in (("yaml", "pyyaml"), ("numpy", "numpy"), ("pandas", "pandas")):
        try:
            __import__(module)
        except ImportError:
            return (
                f"{pin_note} is not importable on this clone (PyPI unreachable); the "
                f"production read path refuses by name (TS-X-01)"
            )
    for fid in FIXTURE_IDS:
        manifest_path = REPO_ROOT / "tests" / "fixtures" / fid / MANIFEST_NAME
        if not manifest_path.is_file():
            return (
                f"no fixture manifest exists at {manifest_path.relative_to(REPO_ROOT)}: the "
                f"manifest is emitted by a measuring run and frozen by the owner's Q-31 act "
                f"(BLK-02) — never authored by hand"
            )
    for config_name, fields in (
        ("experiment.yaml", ("folds", "embargo_hours")),
        ("data.yaml", ("stations", "cell_rule")),
    ):
        config_path = REPO_ROOT / "configs" / config_name
        if not config_path.is_file():
            return f"configs/{config_name} is absent"
        text = config_path.read_text(encoding="utf-8", errors="replace")
        for field in fields:
            if field in text and "TBD" in text:
                return (
                    f"configs/{config_name}: {field} is `TBD — freeze gate`; every stage "
                    f"entry refuses at assert_no_tbd and writes an aborted row (TE 18.3: "
                    f"stop and report, never default)"
                )
    requirements = REPO_ROOT / "requirements.txt"
    if not requirements.is_file() or "tensorflow" not in requirements.read_text(
        encoding="utf-8", errors="replace"
    ):
        return "the TensorFlow pin is unfrozen; the plumbing fixture's minimal M-06 refuses on it"
    return None


def test_clean_run_completion_or_skip_with_named_reason():
    """WS-20 / TA-17 (must-not-fire, still `Pending`): the amended §13.2 sequence in order
    on CPU completes ONLY when every precondition holds; otherwise this test SKIPS with the
    exact stop-and-report reason — it NEVER passes on an abort and never fails the suite
    for a gate the owner has not signed. Recorded as `not run` while skipped."""
    reason = _completion_preconditions()
    if reason is not None:
        pytest.skip(f"clean-run completion NOT RUN — first unmet precondition: {reason}")
    import os
    import subprocess

    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"  # set once BEFORE the first command (amended TE 13.2)
    env["CUDA_VISIBLE_DEVICES"] = ""
    for fid in FIXTURE_IDS:
        argv = [
            sys.executable,
            str(REPO_ROOT / "scripts" / "run_walking_skeleton.py"),
            "--config",
            "configs/",
            "--fixture",
            fid,
        ]
        completed = subprocess.run(
            argv, cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, check=False
        )
        if completed.returncode != 0:
            pytest.fail(
                f"clean run ABORTED at {fid}: {completed.stderr[-800:]} — an abort is never "
                f"a pass (TE 18.3)"
            )
    for script, phase in skeleton.PHASE1_SEQUENCE:
        argv = [sys.executable, str(REPO_ROOT / "scripts" / script), "--config", "configs/"]
        if phase is not None:
            argv += ["--phase", str(phase)]
        completed = subprocess.run(
            argv, cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, check=False
        )
        if completed.returncode != 0:
            pytest.fail(f"clean run ABORTED at {script}: {completed.stderr[-800:]}")


def test_fixture_trees_exist_without_manifests():
    """W-10 / BLK-02: the two fixture trees exist and carry NO fixture_manifest.yaml —
    the manifests come from a measuring run and the freeze acts are the owner's."""
    for fid in FIXTURE_IDS:
        tree = REPO_ROOT / "tests" / "fixtures" / fid
        assert tree.is_dir(), f"fixture tree absent: {tree}"
        assert not (tree / MANIFEST_NAME).exists(), (
            f"{tree / MANIFEST_NAME} exists: no manifest may be authored by hand (BLK-02)"
        )
        assert (tree / "README.md").is_file()


def test_required_output_enumeration_is_20_and_19():
    """TE 15.4's enumeration, derived not carried: 20 hash-listable outputs for
    scientific_1month, 19 for plumbing_7day (`target_uncertainty_budget.json` fixture-2-only)."""
    scientific = required_outputs_for(SCIENTIFIC_FIXTURE_ID)
    plumbing = required_outputs_for(PLUMBING_FIXTURE_ID)
    print(f"required outputs derived: scientific={len(scientific)} plumbing={len(plumbing)}")
    assert len(scientific) == 20 and len(plumbing) == 19
    assert set(scientific) - set(plumbing) == {"target_uncertainty_budget.json"}
    assert len(REQUIRED_OUTPUTS) == 20


def test_function_count_derived_and_printed():
    """The count of test functions is DERIVED from this file (`grep -c "def test_"`) and
    printed before it is asserted against the collected module names — never carried."""
    source = Path(__file__).read_text(encoding="utf-8")
    grep_count = len(re.findall(r"^def test_", source, re.MULTILINE))
    collected = [name for name in globals() if name.startswith("test_")]
    print(f"def test_ count derived from source: {grep_count}; collected: {len(collected)}")
    assert grep_count == len(collected)
    assert grep_count >= 30  # the 39 controls + 11 must-not-fire land across these hosts
