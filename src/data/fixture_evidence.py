"""F7: the fixture artifact stamp, the three generated evidence artifacts, the agreement checks.

Purpose
-------
`fixtures-and-reproducibility` W-3 limbs 4-5, W-4, W-9 (R-135, R-136, R-142; SD-X-01 step 3;
SD-X-03). Everything here is a producing path that REFUSES — never a hand-maintained document
(TE 16: "visual inspection alone is insufficient").

**The stamp (domain-entities § 5).** `FixtureArtifactStamp` is the freight that cannot be
forgotten: `evidence_class` (`smoke_only` for every `plumbing_7day` artifact — TE 15.1's
binding limitation that the seven-day LSTM result "may not be cited, plotted as a result, or
interpreted as skill"; `scientific_fixture` otherwise), `fixture_id`, `data07_caveat` (the
DATA-07 provenance caveat as machine-readable text until the `raw_isprint_cache/` re-acquisition
discharges it), `december_representativeness: not_representative` (the operative clause of
D-11's / D-14's mandatory limitation, on BOTH fixtures — Rec 36), `apparatus_partition_id`, and
the three TEC-05 stamps. `stamp_fixture_artifact` embeds it under `fixture_stamp` in a payload
the producing path constructs; `write_sibling_stamp` writes `<artifact>.fixture_stamp.json` (or
`fixture_stamp.json` inside a directory artifact) beside an artifact an existing writer owns.
`assert_not_smoke_only` is asserted at EVERY evidence surface (R-136 control 13);
`assert_caveats_present` wherever a fixture-derived coverage figure appears (R-135 controls 11,
38; R-142 control 36).

**The three generated artifacts (R-142).** `build_traceability_matrix` (TA-21: three mandatory
links per row; completeness against the implemented-requirement list; a row citing a test
module ABSENT from the workspace refuses — control 33 — and that is a PRESENCE check, not a
coverage check: `tests/test_release_hashes.py` exists and covers none of TE 13.3's manifest
fields, so **TA-15 must not be read as covered** on the strength of a matching filename).
`build_acceptance_table` (TA-09: bounded BY CONSTRUCTION to Phase 1's thirteen rows — WS-01
plus WS-09…WS-20, derived from the enumeration and printed by the test — any WS-02…WS-08 row
refuses (35), a `PASS` without an evidence link refuses (34), the G-P3A deferral is stated on
the table). `build_environment_and_cpu_preflight_report` (G-07's evidence: the eight TE 13.1
lock items, platform, the CPU-only completion record with the GPU made invisible, runtime and
storage against the manifest's MEASURED ranges, the matched-artifact result, the two receipt
references, the in-session gate's `measured_total_runtime`, and both caveat fields wherever a
coverage figure appears). All three refuse a `candidate` manifest (R-134 control 5) and any
`smoke_only` input (13).

**Two preflight reports, two gates — stated, not blurred.** This module builds
`environment_and_cpu_preflight_report`, which evidences **G-07 Reproducibility**.
`aws_ai_dlc_preflight_report` evidences **G-09** and is TA-23's / FR-WS-7's artifact — it is
**`foundation`'s and is built nowhere here** (Rec 9).

**The agreement checks (SD-X-01 step 3; W-3 limb 1).** `assert_freeze_record_agrees` asserts the
sibling `fixture_manifest.sha256` equals the `fixture_manifest_sha256:` the freeze D-number
records in `evidence/DECISIONS.md`, naming both sites on disagreement; the machine-readable
sidecar fallback (`evidence/fixture_freeze_records/<D-number>.json`) is implemented behind the
same function and its use is reported. `assert_identity_agrees_with_decisions` asserts the
manifest's cited window dates, station and verbatim limitation clauses appear in the cited
D-number's section (R-134 control 7; R-135 control 10). Prose parsing lives HERE, in F7, so the
loader stays format-stable (TS-X-01).

**TA-27 is first-limb only.** The matrix records this unit as supporting evidence that Phase 1
cannot import raw GNSS modules; the transition-manifest hash-diff limb is deferred to
G-P2/G-P3C and is never claimed inside Phase 1.

Inputs
------
Validated `FixtureManifest`s (through the one loader), receipt and gate payloads (through
`src/data/fixture_gate`), `RunRecord` locks, caller-supplied row mappings, `evidence/DECISIONS.md`
and its optional sidecar records. Nothing here reads `configs/` (R-15) or any restricted root.

Re-run behaviour
----------------
Pure functions of their inputs; nothing is written except by the caller of the returned
mappings and by `write_sibling_stamp` (once-only). Every refusal raises the base
`IntegrityError` naming the resource and the violated expectation (Q6 = A (i)).

What this pass cannot make run (TE 18.3)
-----------------------------------------
No frozen manifest, receipt or gate result exists; the three emitters can therefore be
exercised only on synthetic inputs, and WS-20, TA-09, TA-17 and TA-21 stay `Pending`. No freeze
D-number exists for any fixture manifest (`evidence/DECISIONS.md` ends at D-32), so
`assert_freeze_record_agrees` refuses on every real path today.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Final

from src.data.config import IntegrityError, RunRecord
from src.data.fixture_gate import RECEIPT_KIND, RESULT_PASS, lock_items
from src.data.fixture_manifest import (
    FIXTURE_IDS,
    PLUMBING_FIXTURE_ID,
    SIBLING_HASH_NAME,
    FixtureManifest,
    IdentityDeclaration,
)

__all__ = [
    "SMOKE_ONLY",
    "SCIENTIFIC_FIXTURE_CLASS",
    "NOT_REPRESENTATIVE",
    "STAMP_KEY",
    "SIBLING_STAMP_SUFFIX",
    "DIRECTORY_STAMP_NAME",
    "PHASE1_ACCEPTANCE_ROWS",
    "DEFERRED_TO_G_P3A",
    "MATRIX_LINKS",
    "DECISIONS_PATH",
    "FREEZE_RECORD_SIDECAR_DIR",
    "FixtureArtifactStamp",
    "stamp_for_manifest",
    "stamp_fixture_artifact",
    "write_sibling_stamp",
    "read_stamp",
    "assert_not_smoke_only",
    "assert_caveats_present",
    "assert_freeze_record_agrees",
    "assert_identity_agrees_with_decisions",
    "build_traceability_matrix",
    "build_acceptance_table",
    "build_environment_and_cpu_preflight_report",
]

SMOKE_ONLY: Final[str] = "smoke_only"
SCIENTIFIC_FIXTURE_CLASS: Final[str] = "scientific_fixture"
NOT_REPRESENTATIVE: Final[str] = "not_representative"
STAMP_KEY: Final[str] = "fixture_stamp"
SIBLING_STAMP_SUFFIX: Final[str] = ".fixture_stamp.json"
DIRECTORY_STAMP_NAME: Final[str] = "fixture_stamp.json"

#: FR-WS-4 / TA-09's Phase 1 bound, DERIVED from the enumeration: WS-01 plus WS-09…WS-20.
PHASE1_ACCEPTANCE_ROWS: Final[tuple[str, ...]] = ("WS-01",) + tuple(
    f"WS-{n:02d}" for n in range(9, 21)
)
#: WS-02…WS-08: deferred to G-P3A (TE 16.1; the 2026-08-16 countersignature).
DEFERRED_TO_G_P3A: Final[tuple[str, ...]] = tuple(f"WS-{n:02d}" for n in range(2, 9))
#: TA-21's three mandatory links per requirement row.
MATRIX_LINKS: Final[tuple[str, ...]] = (
    "decision_ref",
    "test_or_experiment_ref",
    "evidence_artifact_id",
)
#: Where the freeze act's D-number record lives (governance home, SD-X-01 step 2).
DECISIONS_PATH: Final[str] = "evidence/DECISIONS.md"
#: The machine-readable fallback the security design named for 3.5 (one JSON per D-number).
FREEZE_RECORD_SIDECAR_DIR: Final[str] = "evidence/fixture_freeze_records"

_ISO_DATE_RE: Final[re.Pattern[str]] = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
_STATION_CELL_RE: Final[re.Pattern[str]] = re.compile(r"\b([A-Z]{4}) (\d{2}/\d{2})\b")
_FREEZE_HASH_RE: Final[re.Pattern[str]] = re.compile(
    r"fixture_manifest_sha256:\s*`?([0-9a-fA-F]{64})`?"
)
_WS_ROW_RE: Final[re.Pattern[str]] = re.compile(r"^WS-\d{2}$")
_ALLOWED_STATUSES: Final[tuple[str, ...]] = ("PASS", "FAIL", "PENDING")


def _refuse(resource: object, expectation: str) -> IntegrityError:
    return IntegrityError(resource, expectation)


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


# --- § 5: the stamp -----------------------------------------------------------------------


@dataclass(frozen=True)
class FixtureArtifactStamp:
    """domain-entities § 5; every field required, values from the manifest — never asserted."""

    evidence_class: str
    fixture_id: str
    data07_caveat: str
    december_representativeness: str
    phase_id: str
    source_id: str
    target_definition_id: str
    apparatus_partition_id: str | None = None
    frozen_manifest_hash: str | None = None

    def as_mapping(self) -> dict[str, Any]:
        return asdict(self)


def stamp_for_manifest(
    scope: FixtureManifest | IdentityDeclaration, *, apparatus_partition_id: str | None = None
) -> FixtureArtifactStamp:
    """Derive the stamp from a validated scope: `smoke_only` iff `plumbing_7day` (TC-03f)."""
    identity = scope.identity
    limitations = identity["limitations"]
    smoke = scope.fixture_id == PLUMBING_FIXTURE_ID
    return FixtureArtifactStamp(
        evidence_class=SMOKE_ONLY if smoke else SCIENTIFIC_FIXTURE_CLASS,
        fixture_id=scope.fixture_id,
        data07_caveat=str(identity["data07_caveat"]),
        december_representativeness=str(limitations["december_representativeness"]),
        phase_id=str(identity["phase_id"]),
        source_id=str(identity["source_id"]),
        target_definition_id=str(identity["target_definition_id"]),
        apparatus_partition_id=apparatus_partition_id,
        frozen_manifest_hash=scope.sha256 if getattr(scope, "is_frozen", False) else None,
    )


def stamp_fixture_artifact(
    payload: Mapping[str, Any], stamp: FixtureArtifactStamp
) -> dict[str, Any]:
    """Embed the stamp under `fixture_stamp` in a payload the producing path constructs."""
    if stamp.december_representativeness != NOT_REPRESENTATIVE:
        raise _refuse(
            "fixture stamp",
            f"december_representativeness must be {NOT_REPRESENTATIVE!r} (D-11; D-14; Rec 36)",
        )
    if not _nonempty(stamp.data07_caveat):
        raise _refuse("fixture stamp", "data07_caveat must be non-empty (team.md; R-135 limb 3)")
    existing = payload.get(STAMP_KEY)
    if isinstance(existing, Mapping) and existing != stamp.as_mapping():
        raise _refuse(
            "fixture stamp",
            "payload already carries a DIFFERENT fixture stamp; a stamp travels with the "
            "artifact from its producing path and is never rewritten (R-110's pattern)",
        )
    return {**payload, STAMP_KEY: stamp.as_mapping()}


def write_sibling_stamp(artifact_path: Path, stamp: FixtureArtifactStamp) -> Path:
    """Stamp an artifact an existing writer owns: a sibling file beside it, written once."""
    artifact = Path(artifact_path)
    target = (
        artifact / DIRECTORY_STAMP_NAME
        if artifact.is_dir()
        else artifact.with_name(artifact.name + SIBLING_STAMP_SUFFIX)
    )
    if target.exists():
        raise _refuse(target, "a fixture stamp is written once and never rewritten")
    payload = stamp_fixture_artifact({"artifact": artifact.name}, stamp)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def read_stamp(artifact: Mapping[str, Any] | Path) -> Mapping[str, Any] | None:
    """The stamp carried by a payload mapping, or by an artifact path (embedded or sibling)."""
    if isinstance(artifact, Mapping):
        stamp = artifact.get(STAMP_KEY)
        return stamp if isinstance(stamp, Mapping) else None
    path = Path(artifact)
    candidates = [
        path / DIRECTORY_STAMP_NAME
        if path.is_dir()
        else path.with_name(path.name + SIBLING_STAMP_SUFFIX),
    ]
    if path.is_file() and path.suffix.lower() == ".json":
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            payload = None
        if isinstance(payload, Mapping) and isinstance(payload.get(STAMP_KEY), Mapping):
            return payload[STAMP_KEY]
    for candidate in candidates:
        if candidate.is_file():
            try:
                payload = json.loads(candidate.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(payload, Mapping) and isinstance(payload.get(STAMP_KEY), Mapping):
                return payload[STAMP_KEY]
    return None


def assert_not_smoke_only(artifact: Mapping[str, Any] | Path, *, surface: str) -> None:
    """R-136 control 13: an evidence surface refuses any `smoke_only` input, structurally."""
    stamp = read_stamp(artifact)
    evidence_class = None
    if isinstance(stamp, Mapping):
        evidence_class = stamp.get("evidence_class")
    elif isinstance(artifact, Mapping):
        evidence_class = artifact.get("evidence_class")
    if evidence_class == SMOKE_ONLY:
        raise _refuse(
            surface,
            "a plumbing_7day (`evidence_class: smoke_only`) artifact reached an evidence "
            "surface; the seven-day fixture is a smoke test and is explicitly not scientific "
            "evidence — it may not be cited, plotted as a result, or interpreted as skill "
            "(TE 15.1; TC-03f; FR-WS-2; R-136 control 13)",
        )


def assert_caveats_present(figure: Mapping[str, Any], *, surface: str) -> None:
    """R-135 controls 11 and 38; R-142 control 36: both caveat fields on every coverage figure."""
    if not _nonempty(figure.get("data07_caveat")):
        raise _refuse(
            surface,
            "a fixture coverage figure without the DATA-07 caveat field; the caveat is "
            "machine-readable freight wherever a coverage figure is relied on (team.md; "
            "R-135 control 11)",
        )
    if figure.get("december_representativeness") != NOT_REPRESENTATIVE:
        raise _refuse(
            surface,
            f"a fixture-derived figure without `december_representativeness: "
            f"{NOT_REPRESENTATIVE}`; no fixture result may be read as evidence about December "
            f"behaviour, and the prohibition travels with the number (D-11; D-14 clause (ii); "
            f"R-135 control 38)",
        )


# --- SD-X-01 step 3 / W-3 limb 1: agreement with the decision record -------------------------


def _decision_section(decisions_text: str, decision: str) -> str:
    pattern = re.compile(rf"^## {re.escape(decision)}\b.*$", re.MULTILINE)
    match = pattern.search(decisions_text)
    if match is None:
        raise _refuse(
            DECISIONS_PATH,
            f"no `## {decision}` section; the manifest cites a decision the register does not "
            f"carry (identity by citation, R-134 control 7)",
        )
    rest = decisions_text[match.end():]
    next_heading = re.search(r"^## ", rest, re.MULTILINE)
    return rest if next_heading is None else rest[: next_heading.start()]


def _normalise(text: str) -> str:
    return re.sub(r"[\s*_`]+", " ", text).strip().lower()


def assert_freeze_record_agrees(
    manifest_path: Path,
    *,
    decisions_path: Path,
    freeze_decision: str,
    sidecar_dir: Path | None = None,
) -> dict[str, Any]:
    """Sibling `.sha256` == the freeze D-number's recorded hash; name both sites on disagreement.

    Source order: the D-number section's `fixture_manifest_sha256:` line, else the sidecar
    `<sidecar_dir>/<D-number>.json` (`{"fixture_manifest_sha256": ...}`); which was used is
    reported. Both absent -> refuse (a freeze that skipped the record is visible by design).
    """
    manifest_path = Path(manifest_path)
    sibling = manifest_path.with_name(SIBLING_HASH_NAME)
    if not sibling.is_file():
        raise _refuse(sibling, "no sibling hash; the agreement check needs the mechanical record")
    sibling_hash = sibling.read_text(encoding="utf-8").strip().split()[0].lower()
    recorded: str | None = None
    source: str | None = None
    decisions = Path(decisions_path)
    if decisions.is_file():
        section = _decision_section(decisions.read_text(encoding="utf-8"), freeze_decision)
        found = _FREEZE_HASH_RE.search(section)
        if found:
            recorded, source = found.group(1).lower(), f"{decisions}#{freeze_decision}"
    if recorded is None and sidecar_dir is not None:
        sidecar = Path(sidecar_dir) / f"{freeze_decision}.json"
        if sidecar.is_file():
            try:
                payload = json.loads(sidecar.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise _refuse(sidecar, f"freeze-record sidecar unreadable ({exc})") from exc
            value = (
                payload.get("fixture_manifest_sha256") if isinstance(payload, Mapping) else None
            )
            if _nonempty(value):
                recorded, source = str(value).lower(), str(sidecar)
    if recorded is None:
        raise _refuse(
            f"{decisions}#{freeze_decision}",
            f"the freeze record carries no `fixture_manifest_sha256:` line and no sidecar record "
            f"exists; a freeze that skips the D-number write fails this check by design "
            f"(SD-X-01 step 3)",
        )
    if recorded != sibling_hash:
        raise _refuse(
            f"{sibling} vs {source}",
            f"sibling hash {sibling_hash} disagrees with the recorded freeze hash {recorded}; a "
            f"sibling edited without a new D-number is exactly the two-representation risk this "
            f"check closes (SD-X-01 step 3)",
        )
    return {"agrees": True, "sha256": sibling_hash, "source": source}


def assert_identity_agrees_with_decisions(
    scope: FixtureManifest | IdentityDeclaration, *, decisions_path: Path
) -> dict[str, Any]:
    """R-134 control 7 / R-135 control 10: cited window, station and clauses appear in the record.

    The manifest cites; this check reads the cited D-number's section and asserts (a) both
    window dates appear there as ISO dates, (b) for `plumbing_7day` the cited `station cell`
    token appears in the station decision's section, (c) every limitation clause appears
    verbatim (whitespace and Markdown emphasis normalised) in the window decision's section.
    """
    decisions = Path(decisions_path)
    if not decisions.is_file():
        raise _refuse(decisions, "the decision register is required for the citation check")
    text = decisions.read_text(encoding="utf-8")
    identity = scope.identity
    window = identity["window_citation"]
    section = _decision_section(text, str(window["decision"]))
    dates = set(_ISO_DATE_RE.findall(section))
    start, end = scope.window
    for label, value in (("start_utc", start), ("end_utc", end)):
        if value.isoformat() not in dates:
            raise _refuse(
                f"{scope.path}: identity.window_citation.{label}",
                f"{value.isoformat()} does not appear in `## {window['decision']}`; identity is "
                f"cited from the frozen record, never re-derived, and a disagreement fails "
                f"(R-134 control 7)",
            )
    report: dict[str, Any] = {"window_decision": str(window["decision"]), "window_agrees": True}
    station = identity.get("station_citation")
    if isinstance(station, Mapping):
        station_section = _decision_section(text, str(station["decision"]))
        tokens = {f"{s} {c}" for s, c in _STATION_CELL_RE.findall(station_section)}
        cited = f"{station['station_id']} {station['cell']}"
        if cited not in tokens:
            raise _refuse(
                f"{scope.path}: identity.station_citation",
                f"{cited!r} is not the station `## {station['decision']}` records "
                f"({sorted(tokens)}); a manifest naming any other station fails against the "
                f"citation (R-135 control 10)",
            )
        report["station_decision"] = str(station["decision"])
        report["station_agrees"] = True
    normalised_section = _normalise(section)
    for index, clause in enumerate(identity["limitations"]["clauses"]):
        if _normalise(str(clause)) not in normalised_section:
            raise _refuse(
                f"{scope.path}: identity.limitations.clauses[{index}]",
                f"clause is not carried VERBATIM from `## {window['decision']}`: the limitation "
                f"travels as machine-readable freight exactly as the record states it "
                f"(D-11; D-14 clauses (i) and (ii); R-135)",
            )
    report["clauses_verbatim"] = len(identity["limitations"]["clauses"])
    return report


# --- R-142: the three generated evidence artifacts -----------------------------------------


def _require_frozen(manifests: Mapping[str, FixtureManifest], *, surface: str) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for fid in FIXTURE_IDS:
        manifest = manifests.get(fid)
        if manifest is None:
            raise _refuse(
                surface, f"no {fid} manifest supplied; evidence binds to both frozen manifests"
            )
        if not manifest.is_frozen:
            raise _refuse(
                surface,
                f"{fid} manifest is {manifest.status!r}; a run against a candidate manifest "
                f"cannot produce WS-20/TA-09/TA-17 evidence — the emitters refuse "
                f"(R-134 control 5)",
            )
        hashes[fid] = manifest.sha256
    return hashes


def _is_test_module_ref(ref: str) -> bool:
    name = ref.replace("\\", "/").split("/")[-1]
    return name.startswith("test_") and name.endswith(".py")


def build_traceability_matrix(
    rows: Sequence[Mapping[str, Any]],
    *,
    workspace: Path,
    implemented_requirements: Sequence[str],
    manifests: Mapping[str, FixtureManifest],
) -> dict[str, Any]:
    """TA-21: generated, complete, three links per row, refusing absent modules and smoke inputs.

    `test_or_experiment_ref` is a PRESENCE check on a test module (a workspace-relative path or
    module name) or a non-empty registered-run reference — never a coverage claim.
    """
    surface = "traceability matrix (TA-21)"
    frozen = _require_frozen(manifests, surface=surface)
    workspace = Path(workspace)
    seen: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        resource = f"{surface} row {index}"
        requirement = row.get("requirement_id")
        if not _nonempty(requirement):
            raise _refuse(resource, "requirement_id is required")
        missing = [link for link in MATRIX_LINKS if not _nonempty(row.get(link))]
        if missing:
            raise _refuse(
                f"{surface} row {requirement}",
                f"missing mandatory link(s) {missing}; a row missing any of its three links "
                f"FAILS rather than rendering blank (TA-21; R-142 limb 1)",
            )
        ref = str(row["test_or_experiment_ref"])
        if _is_test_module_ref(ref):
            candidate = (
                workspace / ref if "/" in ref.replace("\\", "/") else workspace / "tests" / ref
            )
            if not candidate.is_file():
                raise _refuse(
                    f"{surface} row {requirement}",
                    f"cites test module {ref!r}, absent from the workspace; the link is a "
                    f"PRESENCE check (18 of REQ-ENG-4's 21 modules were unwritten when this "
                    f"control was designed), never a coverage claim — TA-15 is not read as "
                    f"covered by a matching filename (R-142 control 33)",
                )
        assert_not_smoke_only(row, surface=f"{surface} row {requirement}")
        figure = row.get("coverage_figure")
        if isinstance(figure, Mapping):
            assert_caveats_present(figure, surface=f"{surface} row {requirement}")
        seen[str(requirement)] = dict(row)
    absent = sorted(set(implemented_requirements) - set(seen))
    if absent:
        raise _refuse(
            surface,
            f"implemented requirement(s) without a matrix row: {absent}; completeness is "
            f"asserted against the implemented-requirement list (TA-21; R-142 limb 1)",
        )
    return {
        "artifact_class": "traceability_matrix",
        "acceptance_row": "TA-21",
        "frozen_manifest_hashes": frozen,
        "links_per_row": list(MATRIX_LINKS),
        "presence_not_coverage": "test_or_experiment_ref asserts a module EXISTS; TA-15 is not "
        "covered by `tests/test_release_hashes.py`'s name (R-142 box; Rec 42)",
        "ta27_scope": "first limb only (Phase 1 cannot import raw GNSS modules); the "
        "transition-manifest hash-diff limb is deferred to G-P2/G-P3C",
        "aws_ai_dlc_preflight_report": "foundation's (G-09, TA-23, FR-WS-7); not built here",
        "rows": [seen[key] for key in sorted(seen)],
        "row_count": len(seen),
    }


def build_acceptance_table(
    rows: Sequence[Mapping[str, Any]],
    *,
    manifests: Mapping[str, FixtureManifest],
    receipts: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """TA-09's table, bounded BY CONSTRUCTION to WS-01 + WS-09…WS-20 (13 rows).

    Refuses any WS-02…WS-08 row (35 — the deferral is a raise, not a footnote), a `PASS` with no
    evidence link (34), an unknown row id, a duplicate, an incomplete set, a smoke-only input, a
    receipt that is not a pass, and a candidate manifest (5). Rows carry `ws_row_id`, `status`,
    `evidence_link`, `producing_script_or_test`, `receipt_ref`.
    """
    surface = "fixture acceptance table (TA-09)"
    frozen = _require_frozen(manifests, surface=surface)
    for fid in FIXTURE_IDS:
        receipt = receipts.get(fid)
        if not isinstance(receipt, Mapping) or receipt.get("kind") != RECEIPT_KIND:
            raise _refuse(surface, f"no {fid} fixture-pass receipt supplied")
        if receipt.get("result") != RESULT_PASS:
            raise _refuse(surface, f"{fid} receipt is not a pass")
        if receipt.get("frozen_manifest_hash") != frozen[fid]:
            raise _refuse(
                surface,
                f"{fid} receipt binds manifest {receipt.get('frozen_manifest_hash')}, not the "
                f"frozen manifest in force {frozen[fid]} (R-140 control 28)",
            )
    table: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        ws = str(row.get("ws_row_id", ""))
        if not _WS_ROW_RE.match(ws):
            raise _refuse(f"{surface} row {index}", f"ws_row_id {ws!r} is not a WS-nn id")
        if ws in DEFERRED_TO_G_P3A:
            raise _refuse(
                f"{surface} row {ws}",
                f"{ws} is deferred to G-P3A: TE 7.0's Phase 1 hard prohibition bars Phase 1 from "
                f"producing its raw-processing evidence; the table is bounded to "
                f"{list(PHASE1_ACCEPTANCE_ROWS)} by construction (FR-WS-4; TA-09's Phase 1 bound; "
                f"R-142 control 35)",
            )
        if ws not in PHASE1_ACCEPTANCE_ROWS:
            raise _refuse(f"{surface} row {ws}", f"{ws} is not a TE 16 row")
        if ws in table:
            raise _refuse(f"{surface} row {ws}", "duplicate row")
        status = str(row.get("status", ""))
        if status not in _ALLOWED_STATUSES:
            raise _refuse(
                f"{surface} row {ws}", f"status {status!r} not in {list(_ALLOWED_STATUSES)}"
            )
        if status == "PASS" and not _nonempty(row.get("evidence_link")):
            raise _refuse(
                f"{surface} row {ws}",
                "PASS without an evidence link; every check must link to machine-readable or "
                "reviewable evidence — visual inspection alone is insufficient (TE 16; R-142 "
                "control 34)",
            )
        for key in ("producing_script_or_test", "receipt_ref"):
            if not _nonempty(row.get(key)):
                raise _refuse(f"{surface} row {ws}", f"{key} is required")
        if str(row["receipt_ref"]) not in {
            str(r.get("receipt_run_id")) for r in receipts.values()
        }:
            raise _refuse(
                f"{surface} row {ws}",
                f"receipt_ref {row['receipt_ref']!r} names no supplied receipt run id",
            )
        assert_not_smoke_only(row, surface=f"{surface} row {ws}")
        table[ws] = dict(row)
    missing = [ws for ws in PHASE1_ACCEPTANCE_ROWS if ws not in table]
    if missing:
        raise _refuse(
            surface,
            f"rows absent: {missing}; the Phase 1 set is all {len(PHASE1_ACCEPTANCE_ROWS)} rows "
            f"with evidence links (FR-WS-4)",
        )
    return {
        "artifact_class": "fixture_acceptance_table",
        "acceptance_row": "TA-09",
        "phase1_rows": list(PHASE1_ACCEPTANCE_ROWS),
        "row_count": len(table),
        "deferred_to_G_P3A": list(DEFERRED_TO_G_P3A),
        "deferral_statement": "WS-02…WS-08 are deferred to G-P3A (TE 16.1; countersigned "
        "2026-08-16; WS-01 named exception 2026-08-21); no Phase 1 artifact claims one",
        "frozen_manifest_hashes": frozen,
        "receipt_refs": {fid: str(receipts[fid].get("receipt_run_id")) for fid in FIXTURE_IDS},
        "rows": [table[ws] for ws in PHASE1_ACCEPTANCE_ROWS],
    }


def build_environment_and_cpu_preflight_report(
    *,
    lock: RunRecord,
    platform: str,
    clean_run_result: Mapping[str, Any],
    receipts: Mapping[str, Mapping[str, Any]],
    gate_result: Mapping[str, Any] | None,
    manifests: Mapping[str, FixtureManifest],
    coverage_figures: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """G-07's `environment_and_cpu_preflight_report` — a fixed field set, a parse not a screenshot.

    `clean_run_result` carries the CPU-only completion record (`cuda_visible_devices` must be
    the empty string — the GPU made invisible, TC-01), `runtime_seconds`, `storage_bytes` and
    the `matched_artifact_report`. Refuses a candidate manifest (5), a smoke-only input (13), a
    coverage figure lacking either caveat (36), a receipt that is not a pass, and a completion
    record that ran with a GPU visible.
    """
    surface = "environment_and_cpu_preflight_report (G-07)"
    frozen = _require_frozen(manifests, surface=surface)
    if clean_run_result.get("cuda_visible_devices", None) != "":
        raise _refuse(
            surface,
            "the clean run must execute with the GPU made invisible (CUDA_VISIBLE_DEVICES=\"\"); "
            "a completion that depended on an accelerator is no CPU completion (TC-01; TE 9.2; "
            "R-138 control 19)",
        )
    for key in ("runtime_seconds", "storage_bytes", "matched_artifact_report"):
        if key not in clean_run_result:
            raise _refuse(surface, f"clean-run result lacks {key!r}; G-07 reads it as a field")
    assert_not_smoke_only(clean_run_result, surface=surface)
    matched = clean_run_result["matched_artifact_report"]
    if isinstance(matched, Mapping):
        assert_not_smoke_only(matched, surface=f"{surface}: matched_artifact_report")
    for fid in FIXTURE_IDS:
        receipt = receipts.get(fid)
        if not isinstance(receipt, Mapping) or receipt.get("kind") != RECEIPT_KIND:
            raise _refuse(
                surface, f"no {fid} fixture-pass receipt supplied (two references required)"
            )
        if (
            receipt.get("result") != RESULT_PASS
            or receipt.get("frozen_manifest_hash") != frozen[fid]
        ):
            raise _refuse(
                surface, f"{fid} receipt is not a pass against the frozen manifest in force"
            )
    for index, figure in enumerate(coverage_figures):
        assert_caveats_present(figure, surface=f"{surface}: coverage figure {index}")
    measured_total_runtime = None
    if gate_result is not None:
        measured_total_runtime = gate_result.get("measured_total_runtime_seconds")
    return {
        "artifact_class": "environment_and_cpu_preflight_report",
        "gate": "G-07 Reproducibility (Blocked, Supervisor)",
        "not_this": (
            "aws_ai_dlc_preflight_report evidences G-09 and is foundation's (TA-23; FR-WS-7)"
        ),
        "environment_lock": lock_items(lock),
        "platform": platform,
        "cpu_only_completion": {
            "cuda_visible_devices": "",
            "gpu_visible": False,
            "completed": bool(clean_run_result.get("completed", False)),
        },
        "runtime_seconds": clean_run_result["runtime_seconds"],
        "storage_bytes": clean_run_result["storage_bytes"],
        "matched_artifact_report": matched,
        "receipt_refs": {fid: str(receipts[fid].get("receipt_run_id")) for fid in FIXTURE_IDS},
        "frozen_manifest_hashes": frozen,
        "in_session_gate_measured_total_runtime_seconds": measured_total_runtime,
        "coverage_figures": [dict(f) for f in coverage_figures],
        "ta27_scope": "first limb only; hash-diff limb deferred to G-P2/G-P3C",
    }
