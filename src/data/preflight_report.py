"""`aws_ai_dlc_preflight_report` — the TE 18.3 preflight gate's evidence artifact (G-09; TA-23).

Purpose
-------
Builds the evidence artifact TE 18.3 names for **G-09 Agent preflight** (Vision 13.1;
TE 19 row TA-23; FR-WS-7), as `foundation`'s functional design fixes it
(`business-logic-model.md` W-3 box; `business-rules.md` R-02): an AGGREGATION surface over
the gate's four limbs —

1. **zero `TBD`** — no required field in `data.yaml`, `features.yaml`, `experiment.yaml`
   or `seeds.yaml` is absent or carries the `TBD — freeze gate` sentinel (W-3 steps 1-4,
   `assert_no_tbd` over every `REQUIRED_FIELDS_MAP` entry of the requested phase);
2. **declared sources** — every declared source path and SHA-256 resolves (W-3 step 5,
   `assert_declared_sources_exist`);
3. **critical tests** — the ten gate tests TE 18.3 enumerates, read from a junit XML
   produced by an actual pytest run, never asserted from source;
4. **supervisor sign-off** — the scientific hierarchy, IRI role, horizons, estimand, seeds
   and locked-test protocol, read from a sign-off record the student authors, never
   synthesised here.

Two of those limbs (1, 2) are computed here; two (3, 4) are COLLECTED from evidence produced
elsewhere. **The report must not become self-certifying** (R-02): a limb with no collected
evidence renders `absent`, never `passed`, and the overall verdict is `green` only when every
limb is `passed`. A `deferred` critical test is one TE 12 attaches to a Phase 2 stage
(`test_dcb_sign.py`, `test_hourly_target.py`); it is not a failure in a Phase 1 preflight
(NFR-PHASE-01) and is reported by name as deferred rather than counted as passed.

The restricted-reading module `tests/test_release_hashes.py` belongs to the gate/freeze
suite (`.githooks/pre-commit` § 2, Recommendation 30): it appears in a junit file only when
an authorised occasion ran it, so the "release hashes" test renders `absent` on an ordinary
suite run — which is the truthful state, not a defect of this module.

Inputs
------
`snapshot` (a `ConfigSnapshot` from `load_configs`); `phase`; an optional junit XML path; an
optional sign-off record path (YAML mapping with the six required keys, each a mapping
carrying `decision`, `statement`, `recorded_at`). `code_commit` for the environment lock.

Re-run behaviour
----------------
Pure function of its inputs plus the wall-clock `generated_at_utc`; writes nothing itself
(`scripts/gate_preflight_report.py` is the writer, one timestamped file per invocation).
Deterministic for fixed configs, junit and record.

Boundaries
----------
Imports nothing from `src/external/` (TE 12 import-boundary rule) and reads no path under
the December custody root (D-15; the literal lives in `locked_test.py` alone, R-28). G-09 is a supervisor gate: building this report signs
nothing and authorises nothing.
"""

from __future__ import annotations

import datetime as dt
import xml.etree.ElementTree as ET
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Final

from src.data.config import (
    REQUIRED_FIELDS_MAP,
    ConfigSnapshot,
    PreflightError,
    assert_declared_sources_exist,
    assert_no_tbd,
)

__all__ = [
    "ARTIFACT_CLASS",
    "CRITICAL_TESTS",
    "SIGNOFF_ITEMS",
    "LIMB_STATUSES",
    "build_aws_ai_dlc_preflight_report",
    "read_junit_module_outcomes",
    "read_signoff_record",
    "required_fields_for_phase",
]

ARTIFACT_CLASS: Final[str] = "aws_ai_dlc_preflight_report"

#: The four limb outcomes R-02 distinguishes. `deferred` is a per-test status only.
LIMB_STATUSES: Final[tuple[str, ...]] = ("passed", "failed", "absent")

#: TE 18.3's ten required gate tests, in the document's order, each mapped to the TE 12
#: module(s) that carry it and the phase the module attaches to (TE 12: `test_dcb_sign.py`
#: and `test_hourly_target.py` are Phase 2 only). A test whose EVERY module is Phase-2-only
#: is `deferred` in a Phase 1 preflight. "release hashes" maps to the restricted reader
#: and renders `absent` unless an authorised run's junit carries it.
CRITICAL_TESTS: Final[tuple[dict[str, Any], ...]] = (
    {
        "name": "target contract and DCB sign",
        "modules": (
            ("tests/test_prepared_target_schema.py", 1),
            ("tests/test_hourly_target.py", 2),
            ("tests/test_dcb_sign.py", 2),
        ),
    },
    {"name": "availability lags", "modules": (("tests/test_feature_availability.py", 1),)},
    {"name": "IRI-free denial", "modules": (("tests/test_iri_denial.py", 1),)},
    {"name": "split embargo", "modules": (("tests/test_split_embargo.py", 1),)},
    {"name": "train-only transforms", "modules": (("tests/test_train_only_transforms.py", 1),)},
    {
        "name": "comparison-wide masks and matched windows",
        "modules": (("tests/test_common_masks.py", 1),),
    },
    {"name": "checkpoint restore", "modules": (("tests/test_checkpoint_restore.py", 1),)},
    {"name": "vector bootstrap", "modules": (("tests/test_bootstrap.py", 1),)},
    {"name": "release hashes", "modules": (("tests/test_release_hashes.py", 1),)},
    {"name": "locked-test access guard", "modules": (("tests/test_locked_test_guard.py", 1),)},
)

#: TE 18.3 precondition 3: the six items the supervisor signs.
SIGNOFF_ITEMS: Final[tuple[str, ...]] = (
    "scientific_hierarchy",
    "iri_role",
    "horizons",
    "estimand",
    "seeds",
    "locked_test_protocol",
)

_SIGNOFF_ENTRY_FIELDS: Final[tuple[str, ...]] = ("decision", "statement", "recorded_at")


def required_fields_for_phase(phase: int) -> tuple[str, ...]:
    """The union of every `REQUIRED_FIELDS_MAP` entry keyed to `phase`, sorted, de-duplicated.

    The map is keyed `(stage, phase)` (R-03) so a Phase-2 field never enters a Phase 1
    preflight. An empty union is refused: a phase with no required field is a map gap,
    not a clean preflight.
    """
    fields = sorted(
        {f for (_stage, p), fs in REQUIRED_FIELDS_MAP.items() if p == phase for f in fs}
    )
    if not fields:
        raise PreflightError(
            "REQUIRED_FIELDS_MAP", f"no required field is declared for phase {phase}; refusing"
        )
    return tuple(fields)


def _module_key(classname: str, file_attr: str | None) -> str | None:
    """Normalise a junit testcase to its `tests/<module>.py` path, or None if unknowable."""
    if file_attr:
        return file_attr.replace("\\", "/")
    if not classname:
        return None
    # pytest's junit classname is dotted: `tests.test_iri_denial[.TestClass]`.
    parts = classname.split(".")
    if not parts:
        return None
    # take the longest prefix ending in a `test_*` segment
    for index in range(len(parts), 0, -1):
        if parts[index - 1].startswith("test_"):
            return "/".join(parts[:index]) + ".py"
    return None


def read_junit_module_outcomes(junit_path: Path) -> dict[str, dict[str, int]]:
    """Per-module counts from a junit XML: `{module: {passed, failed, errors, skipped}}`.

    A module with zero testcases is simply absent from the mapping — the caller renders it
    `absent`. Raises `PreflightError` if the file is missing or unparseable: an unreadable
    evidence file is a failed collection, never an empty one.
    """
    if not junit_path.is_file():
        raise PreflightError(str(junit_path), "junit evidence file is absent")
    try:
        # the junit file is this project's own pytest output, never untrusted input
        root = ET.parse(junit_path).getroot()  # noqa: S314
    except ET.ParseError as exc:
        raise PreflightError(str(junit_path), f"junit XML is unparseable ({exc})") from exc
    outcomes: dict[str, dict[str, int]] = {}
    for case in root.iter("testcase"):
        key = _module_key(case.get("classname", ""), case.get("file"))
        if key is None:
            continue
        bucket = outcomes.setdefault(key, {"passed": 0, "failed": 0, "errors": 0, "skipped": 0})
        if case.find("failure") is not None:
            bucket["failed"] += 1
        elif case.find("error") is not None:
            bucket["errors"] += 1
        elif case.find("skipped") is not None:
            bucket["skipped"] += 1
        else:
            bucket["passed"] += 1
    return outcomes


def _critical_tests_limb(
    outcomes: Mapping[str, Mapping[str, int]] | None, *, phase: int
) -> dict[str, Any]:
    tests: list[dict[str, Any]] = []
    limb_status = "passed"
    if outcomes is None:
        for spec in CRITICAL_TESTS:
            tests.append({"name": spec["name"], "status": "absent", "modules": {}})
        return {"status": "absent", "reason": "no junit evidence supplied", "tests": tests}
    for spec in CRITICAL_TESTS:
        per_module: dict[str, Any] = {}
        statuses: list[str] = []
        for module, module_phase in spec["modules"]:
            counts = outcomes.get(module)
            if module_phase > phase:
                per_module[module] = {"status": "deferred", "phase": module_phase}
                statuses.append("deferred")
            elif counts is None or (counts["passed"] + counts["failed"] + counts["errors"]) == 0:
                per_module[module] = {"status": "absent"}
                statuses.append("absent")
            elif counts["failed"] or counts["errors"]:
                per_module[module] = {"status": "failed", **dict(counts)}
                statuses.append("failed")
            else:
                per_module[module] = {"status": "passed", **dict(counts)}
                statuses.append("passed")
        if "failed" in statuses:
            status = "failed"
        elif "absent" in statuses:
            status = "absent"
        elif all(s == "deferred" for s in statuses):
            status = "deferred"
        else:
            status = "passed"
        tests.append({"name": spec["name"], "status": status, "modules": per_module})
    if any(t["status"] == "failed" for t in tests):
        limb_status = "failed"
    elif any(t["status"] == "absent" for t in tests):
        limb_status = "absent"
    named = [f"{t['name']}: {t['status']}" for t in tests if t["status"] != "passed"]
    return {
        "status": limb_status,
        "not_passed_by_name": named,
        "tests": tests,
        "criterion": "TE 18.3: no failing critical test; absent evidence is absent, never passed",
    }


def read_signoff_record(path: Path) -> dict[str, Any]:
    """The student-authored sign-off record: a YAML mapping over `SIGNOFF_ITEMS`.

    Each item must be a mapping carrying `decision`, `statement` and `recorded_at`; a
    missing item or field is a `failed` limb naming it, never a silently partial pass.
    """
    import yaml  # local: the four governed configs are the only other YAML readers

    if not path.is_file():
        raise PreflightError(str(path), "sign-off record is absent")
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, Mapping):
        raise PreflightError(str(path), "sign-off record must be a mapping")
    return dict(loaded)


def _signoff_limb(record: Mapping[str, Any] | None, *, record_path: str | None) -> dict[str, Any]:
    if record is None:
        return {
            "status": "absent",
            "reason": "no sign-off record supplied; a supervisor act is recorded, never synthesised",
            "items": {item: "absent" for item in SIGNOFF_ITEMS},
        }
    items: dict[str, Any] = {}
    problems: list[str] = []
    for item in SIGNOFF_ITEMS:
        entry = record.get(item)
        if not isinstance(entry, Mapping):
            items[item] = "absent"
            problems.append(f"{item}: absent")
            continue
        missing = [f for f in _SIGNOFF_ENTRY_FIELDS if not str(entry.get(f, "") or "").strip()]
        if missing:
            items[item] = f"incomplete ({', '.join(missing)})"
            problems.append(f"{item}: incomplete ({', '.join(missing)})")
        else:
            items[item] = {f: str(entry[f]) for f in _SIGNOFF_ENTRY_FIELDS}
    return {
        "status": "failed" if problems else "passed",
        "record": record_path,
        "problems": problems,
        "items": items,
    }


def build_aws_ai_dlc_preflight_report(
    snapshot: ConfigSnapshot,
    *,
    phase: int,
    code_commit: str | None,
    junit_outcomes: Mapping[str, Mapping[str, int]] | None,
    signoff_record: Mapping[str, Any] | None,
    junit_path: str | None = None,
    signoff_path: str | None = None,
    now: dt.datetime | None = None,
) -> dict[str, Any]:
    """Assemble the report. Never raises on a failed limb — a failure is REPORTED by name;
    it raises only when an input is structurally unusable (an unreadable junit is the
    caller's `PreflightError` before this is reached)."""
    generated = (now or dt.datetime.now(dt.timezone.utc)).isoformat()
    required = required_fields_for_phase(phase)
    limbs: dict[str, Any] = {}

    try:
        assert_no_tbd(snapshot, required=required)
        limbs["zero_tbd"] = {
            "status": "passed",
            "required_fields": list(required),
            "offenders": [],
        }
    except PreflightError as exc:
        limbs["zero_tbd"] = {
            "status": "failed",
            "required_fields": list(required),
            "offenders": [str(exc)],
        }

    try:
        assert_declared_sources_exist(snapshot)
        limbs["declared_sources"] = {"status": "passed", "problems": []}
    except PreflightError as exc:
        limbs["declared_sources"] = {"status": "failed", "problems": [str(exc)]}

    limbs["critical_tests"] = {
        "junit": junit_path,
        **_critical_tests_limb(junit_outcomes, phase=phase),
    }
    limbs["supervisor_signoff"] = _signoff_limb(signoff_record, record_path=signoff_path)

    not_passed = sorted(name for name, limb in limbs.items() if limb["status"] != "passed")
    verdict = "green" if not not_passed else "not_green"
    return {
        "artifact_class": ARTIFACT_CLASS,
        "gate": "G-09 Agent preflight",
        "acceptance_row": "TA-23",
        "requirement": "FR-WS-7",
        "authority": "TE 18.3; Vision 13.1; foundation W-3 / R-02",
        "generated_at_utc": generated,
        "phase": phase,
        "code_commit": code_commit,
        "config_hashes": dict(snapshot.hashes),
        "limbs": limbs,
        "verdict": verdict,
        "limbs_not_passed": not_passed,
        "self_certification_bar": (
            "a limb with no collected evidence renders absent, never passed; the verdict is "
            "green only when all four limbs are passed (R-02)"
        ),
        "authorises": "nothing — G-09 is a supervisor gate; this artifact is its evidence, not its signature",
    }


def limb_names() -> Sequence[str]:
    """The four limb keys, in report order."""
    return ("zero_tbd", "declared_sources", "critical_tests", "supervisor_signoff")
