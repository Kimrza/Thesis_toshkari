"""`aws_ai_dlc_preflight_report` (G-09; TA-23; FR-WS-7) — R-02's five negative controls.

The report is an aggregation surface and must not self-certify: each limb withheld in turn
(a `TBD` field, an unresolving declared hash, a failing critical test, an absent sign-off)
must yield a `not_green` verdict naming that limb, and a never-collected limb must render
`absent`, never `passed`. The positive case — every limb passed — is the one route to
`green`. Runs against synthetic snapshots and synthetic junit / sign-off files only;
nothing under `configs/` or `evidence/` is read.
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import (  # noqa: E402
    REQUIRED_FIELDS_MAP,
    TBD_SENTINEL,
    ConfigSnapshot,
    PreflightError,
)
from src.data.preflight_report import (  # noqa: E402
    CRITICAL_TESTS,
    SIGNOFF_ITEMS,
    build_aws_ai_dlc_preflight_report,
    read_junit_module_outcomes,
    read_signoff_record,
    required_fields_for_phase,
)

UTC = dt.timezone.utc
NOW = dt.datetime(2026, 9, 21, 12, 0, tzinfo=UTC)


def _set(tree: dict[str, Any], dotted: str, value: Any) -> None:
    node = tree
    parts = dotted.split(".")
    for part in parts[:-1]:
        node = node.setdefault(part, {})
    node[parts[-1]] = value


def _snapshot(
    tmp_path: Path, *, tbd_field: str | None = None, bad_hash: bool = False
) -> ConfigSnapshot:
    """A snapshot in which EVERY phase-1 required field is resolved, unless one is withheld."""
    configs: dict[str, dict[str, Any]] = {
        "data": {},
        "features": {},
        "experiment": {},
        "seeds": {},
    }
    for field in required_fields_for_phase(1):
        top, rest = field.split(".", 1)
        _set(configs[top], rest, TBD_SENTINEL if field == tbd_field else "resolved")
    source = tmp_path / "declared.txt"
    source.write_bytes(b"declared-bytes")
    import hashlib

    digest = hashlib.sha256(b"declared-bytes").hexdigest()
    configs["data"]["declared_sources"] = [
        {"path": "declared.txt", "sha256": ("0" * 64) if bad_hash else digest}
    ]
    return ConfigSnapshot(
        data=configs["data"],
        features=configs["features"],
        experiment=configs["experiment"],
        seeds=configs["seeds"],
        hashes={"data.yaml": "x", "features.yaml": "y", "experiment.yaml": "z", "seeds.yaml": "w"},
        snapshot_dir=tmp_path,
        resolved_roots={"workspace": tmp_path},
        platform="local",
    )


def _junit(tmp_path: Path, *, failing: str | None = None, omit: str | None = None) -> Path:
    """A junit file carrying one passing case per phase-1 critical module, one optionally
    failing, one optionally omitted."""
    cases: list[str] = []
    for spec in CRITICAL_TESTS:
        for module, phase in spec["modules"]:
            if phase != 1 or module == omit:
                continue
            classname = module[:-3].replace("/", ".")
            body = "<failure message='boom'/>" if module == failing else ""
            cases.append(
                f"<testcase classname='{classname}' name='test_x' file='{module}'>{body}</testcase>"
            )
    path = tmp_path / "junit.xml"
    path.write_text(
        f"<testsuites><testsuite name='pytest'>{''.join(cases)}</testsuite></testsuites>"
    )
    return path


def _signoff(tmp_path: Path, *, drop: str | None = None) -> Path:
    import yaml

    record = {
        item: {
            "decision": f"D-{n}",
            "statement": "student's report of countersignature",
            "recorded_at": "2026-09-21",
        }
        for n, item in enumerate(SIGNOFF_ITEMS, start=1)
        if item != drop
    }
    path = tmp_path / "signoff.yaml"
    path.write_text(yaml.safe_dump(record), encoding="utf-8")
    return path


def _build(tmp_path: Path, **kw: Any) -> dict[str, Any]:
    pytest.importorskip("yaml")
    snapshot = _snapshot(
        tmp_path, tbd_field=kw.get("tbd_field"), bad_hash=kw.get("bad_hash", False)
    )
    junit = (
        _junit(tmp_path, failing=kw.get("failing"), omit=kw.get("omit"))
        if kw.get("junit", True)
        else None
    )
    signoff = _signoff(tmp_path, drop=kw.get("drop")) if kw.get("signoff", True) else None
    return build_aws_ai_dlc_preflight_report(
        snapshot,
        phase=1,
        code_commit="deadbeef",
        junit_outcomes=read_junit_module_outcomes(junit) if junit else None,
        signoff_record=read_signoff_record(signoff) if signoff else None,
        junit_path=str(junit) if junit else None,
        signoff_path=str(signoff) if signoff else None,
        now=NOW,
    )


# --- the positive route to green -------------------------------------------------------


def test_every_limb_passed_is_the_only_route_to_green(tmp_path: Path) -> None:
    report = _build(tmp_path)
    assert report["verdict"] == "green", report["limbs_not_passed"]
    assert report["limbs_not_passed"] == []
    assert {k: v["status"] for k, v in report["limbs"].items()} == {
        "zero_tbd": "passed",
        "declared_sources": "passed",
        "critical_tests": "passed",
        "supervisor_signoff": "passed",
    }
    assert report["artifact_class"] == "aws_ai_dlc_preflight_report"
    assert report["gate"].startswith("G-09")
    # the two Phase-2-only modules are named as deferred, never counted as passed
    first = report["limbs"]["critical_tests"]["tests"][0]
    assert first["modules"]["tests/test_dcb_sign.py"]["status"] == "deferred"
    assert first["modules"]["tests/test_hourly_target.py"]["status"] == "deferred"
    assert first["status"] == "passed"  # its Phase 1 module passed


# --- R-02's four withheld-limb controls ------------------------------------------------


def test_a_tbd_required_field_withholds_green_and_names_the_limb(tmp_path: Path) -> None:
    field = required_fields_for_phase(1)[0]
    report = _build(tmp_path, tbd_field=field)
    assert report["verdict"] == "not_green"
    assert "zero_tbd" in report["limbs_not_passed"]
    assert field in report["limbs"]["zero_tbd"]["offenders"][0]


def test_an_unresolving_declared_hash_withholds_green(tmp_path: Path) -> None:
    report = _build(tmp_path, bad_hash=True)
    assert report["verdict"] == "not_green"
    assert report["limbs"]["declared_sources"]["status"] == "failed"
    assert "does not resolve" in report["limbs"]["declared_sources"]["problems"][0]


def test_one_failing_critical_test_withholds_green_and_is_named(tmp_path: Path) -> None:
    report = _build(tmp_path, failing="tests/test_iri_denial.py")
    assert report["verdict"] == "not_green"
    limb = report["limbs"]["critical_tests"]
    assert limb["status"] == "failed"
    assert "IRI-free denial: failed" in limb["not_passed_by_name"]


def test_an_absent_signoff_item_withholds_green_and_is_named(tmp_path: Path) -> None:
    report = _build(tmp_path, drop="estimand")
    assert report["verdict"] == "not_green"
    limb = report["limbs"]["supervisor_signoff"]
    assert limb["status"] == "failed"
    assert limb["items"]["estimand"] == "absent"
    assert "estimand: absent" in limb["problems"]


# --- the fifth control: never collected renders absent, never passed --------------------


def test_a_never_collected_limb_renders_absent_never_passed(tmp_path: Path) -> None:
    report = _build(tmp_path, junit=False, signoff=False)
    assert report["verdict"] == "not_green"
    assert report["limbs"]["critical_tests"]["status"] == "absent"
    assert all(t["status"] == "absent" for t in report["limbs"]["critical_tests"]["tests"])
    assert report["limbs"]["supervisor_signoff"]["status"] == "absent"
    assert set(report["limbs_not_passed"]) == {"critical_tests", "supervisor_signoff"}


def test_a_critical_module_missing_from_the_junit_renders_absent_not_passed(
    tmp_path: Path,
) -> None:
    """The restricted reader `test_release_hashes.py` is the live case: an ordinary suite
    run deselects it (Recommendation 30), so its test must show `absent`, not `passed`."""
    report = _build(tmp_path, omit="tests/test_release_hashes.py")
    assert report["verdict"] == "not_green"
    limb = report["limbs"]["critical_tests"]
    assert limb["status"] == "absent"
    assert "release hashes: absent" in limb["not_passed_by_name"]


# --- inputs that are unusable fail, never render empty ---------------------------------


def test_an_unreadable_junit_is_a_precondition_failure(tmp_path: Path) -> None:
    with pytest.raises(PreflightError):
        read_junit_module_outcomes(tmp_path / "missing.xml")
    bad = tmp_path / "bad.xml"
    bad.write_text("<not-closed")
    with pytest.raises(PreflightError):
        read_junit_module_outcomes(bad)


def test_required_fields_are_the_phase_keyed_union_of_the_map() -> None:
    fields = required_fields_for_phase(1)
    expected = sorted({f for (_s, p), fs in REQUIRED_FIELDS_MAP.items() if p == 1 for f in fs})
    assert list(fields) == expected
    assert all("." in f for f in fields)
