"""R2 render guards: the TEN rendering refusals of SD-R-01 — one home, fail-closed.

Purpose
-------
`regimes-diagnostics-reporting` SD-R-01 (Q2 = A) fixes ONE guard module owning every
rendering refusal, so drift between two copies of one rule has no second copy to drift —
the same one-guard-home shape the sibling's `src/evaluation/guards.py` gives the
metric-entry boundary. **The boundary split, stated so no check is homeless or
double-owned:** metric-entry checks (stamps, registered mask, DEC hash receipt, target
space) are the sibling's `guards.py` and run where metrics are computed; RENDERING checks
(this module) run where values become reader-visible text, tables and figures. One copy
each side; nothing checked twice, nothing checked nowhere.

The ten guards, exactly SD-R-01's table:

* ``require_estimand_fields`` — an estimand value without `benchmark_minus_model`
  orientation + `equal_station` weighting (SEC-R-02 half 1). Called by W-3, W-5.
* ``require_lineage_caveat`` — any IRI/GIM comparison without the lineage caveat; for a
  figure, "present" means the caveat rendered into the caption or figure metadata
  (SEC-R-02 half 2; TEC-06). Called by W-3, W-5, W-7.
* ``require_units`` — a value whose units assertion is absent or non-TECU where TECU is
  required (R-125 limb 6; BLK-08's reach made checked, not silent). Called by W-3, W-5, W-6.
* ``require_complete_members`` — a table missing any declared comparison-set member's
  metric (SEC-R-01; FR-P1-05-9). Called by W-3.
* ``require_d17_bound`` — a breakdown stratum outside the configured D-17 enumerated set
  (R-127). Called by W-5.
* ``require_registered_surface`` — emission of a conclusion-bearing artifact not
  registered in the `ConclusionSurfaceArtifact` registry (Q1 = A; SD-R-03; the R-120
  widening comparator has no registered surface, so this guard is its quarantine at the
  rendering boundary). Called by W-3, W-5, W-7, W-4.
* ``require_beats_model`` — a table row missing its per-benchmark `beats_model` field
  (R-125 control (9); the flag is PRINTED, never judged). Called by W-3.
* ``require_provenance_block`` — a table OR BREAKDOWN artifact missing any of the five
  provenance values, or a scored-window statement disagreeing with the registered mask's
  (R-125 controls (32)/(33); Vision §8.9; D-28). Called by W-3 AND W-5.
* ``require_derived_label`` — a derived quantity rendered without its `derived: true`
  label (R-127 control (34); Vision §9.5 required result 2). Called by W-5.
* ``require_driver_caveat`` — a per-station breakdown emitted without the standing TC-12
  driver-identity caveat (R-127 control (38)). Called by W-5.

Exception classes: ``require_complete_members`` raises `FairnessError` — the imported
class of the consumed R-110 limb 1 completeness precondition (R-125 limb 1). Every other
rendering refusal raises `RegimeError` (`domain-entities.md` § 5's placement: reporting-
discipline refusals reuse `RegimeError`; no fifteenth exception is minted).

Inputs
------
In-memory artifact mappings (the primary-table artifact, breakdown artifacts, plot
manifest entries, the checklist), the registered `ComparisonMask`, and a
`ConclusionSurfaceRegistry` directory on disk. Imports ONLY `src/data`,
`src/evaluation/metrics` (for the canonical sentence/orientation tokens) and the standard
library — no `src/features`, `src/models` or `src/external`, directly or transitively
(TE §12; D-27).

Re-run behaviour
----------------
Guards are pure checks. `ConclusionSurfaceRegistry.register` writes one file per artifact
ID under the registry root via the write-once atomic idiom (`.tmp` → flush+fsync → rename;
a second registration of the same ID refuses — NFR-AUD-01's no-silent-replacement).
``emit_registered_artifact`` registers THEN writes in one call so an artifact cannot be
emitted registered-but-unguarded or guarded-but-unregistered (the nfr-design transaction
note, honoured at 3.5).

Governance
----------
SD-R-01…SD-R-03; R-125…R-129; TC-12 (`binding: hard`, interpretive half);
GOV-2026-08-28-FD-01 Recs 16/17/20/21. The registry bounds what the PIPELINE produces:
hand-authored prose outside the pipeline never passes a producing path and cannot be
forced to register — narrowed, not closed, and no artifact may describe the checklist as
fully enforced (SD-R-03's stated residual).
"""

from __future__ import annotations

import json
import os
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from src.data.config import FairnessError, RegimeError
from src.evaluation.metrics import (
    EXTERNAL_COMPARATOR_IDS,
    ORIENTATION,
    SPATIAL_REPRESENTATIVENESS_SENTENCE,
    WEIGHTING,
)

__all__ = [
    "REQUIRED_UNITS",
    "DRIVER_IDENTITY_CAVEAT",
    "CONCLUSION_SURFACE_KEYS",
    "PROVENANCE_FIELDS",
    "ConclusionSurfaceRegistry",
    "emit_registered_artifact",
    "require_estimand_fields",
    "require_lineage_caveat",
    "require_units",
    "require_complete_members",
    "require_d17_bound",
    "require_registered_surface",
    "require_beats_model",
    "require_provenance_block",
    "require_derived_label",
    "require_driver_caveat",
]

#: The one reporting unit (BLK-08's bound: TECU or refuse). An identity token.
REQUIRED_UNITS: str = "TECU"

#: TC-12's standing caveat (`project.md` § Mandated, `binding: hard` — both halves),
#: wording fixed by the governing rule, emitted by the per-station producing path (Rec 17).
DRIVER_IDENTITY_CAVEAT: str = (
    "Every external driver value is identical across all three cells by construction; no "
    "station performance difference may be attributed to local forcing the dataset does "
    "not contain"
)

#: The three text surfaces of the ConclusionSurfaceArtifact (`domain-entities.md` § 6).
CONCLUSION_SURFACE_KEYS: tuple[str, ...] = (
    "abstract_level_interpretation",
    "conclusion",
    "limitations",
)

#: The five provenance fields (Vision §8.9; D-28; Rec 16) — printed, never restated.
PROVENANCE_FIELDS: tuple[str, ...] = (
    "mask_id",
    "feature_set_id",
    "surviving_row_counts",
    "exclusion_counts",
    "scored_window_statement",
)


# --- the ConclusionSurfaceArtifact registry (R6; Q1 = A) ----------------------------------


def _write_once_atomic(path: Path, payload: bytes, *, what: str) -> None:
    if path.exists():
        raise RegimeError(
            path,
            f"{what} already exists and is never silently replaced (write-once atomic "
            f"idiom; NFR-AUD-01)",
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


class ConclusionSurfaceRegistry:
    """The single thesis-level location enumeration (Q1 = A; SD-R-03).

    A location is thesis-level IFF registered here. The checklist inspects exactly this
    registered set, and registration is enforced at every producing path
    (``require_registered_surface``), so the registry grows with the surface
    automatically and its enumeration cannot go stale independently of what it bounds.
    """

    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    def _entry_path(self, artifact_id: str) -> Path:
        safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in artifact_id)
        return self.root / f"{safe}.json"

    def register(self, entry: Mapping[str, Any]) -> Path:
        """Write-once registration of one conclusion-bearing artifact.

        Raises
        ------
        RegimeError
            a missing `artifact_id`, `kind` or mandated stamp; a duplicate registration.
        """
        artifact_id = str(entry.get("artifact_id", ""))
        if not artifact_id:
            raise RegimeError(
                "conclusion-surface registration",
                "artifact_id is absent; an unnamed surface cannot be enumerated (Q1 = A)",
            )
        missing = [
            key
            for key in ("kind", "phase_id", "source_id", "target_definition_id")
            if not entry.get(key)
        ]
        if missing:
            raise RegimeError(
                f"conclusion-surface registration {artifact_id}",
                f"required field(s) {missing} absent; every registered surface carries "
                f"its kind and the three stamps (TEC-05; domain-entities § 6)",
            )
        path = self._entry_path(artifact_id)
        payload = json.dumps(dict(entry), sort_keys=True, indent=2, default=str)
        _write_once_atomic(
            path,
            payload.encode("utf-8"),
            what=f"conclusion-surface registration for {artifact_id!r}",
        )
        return path

    def lookup(self, artifact_id: str) -> Mapping[str, Any] | None:
        """The registered entry, or None. Absence of the whole registry root is a
        fail-closed condition surfaced by ``require_registered_surface`` / the checklist."""
        path = self._entry_path(str(artifact_id))
        if not path.is_file():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def ids(self) -> tuple[str, ...]:
        """Every registered artifact ID (the checklist's exact inspection set)."""
        if not self.root.is_dir():
            return ()
        out = []
        for path in sorted(self.root.glob("*.json")):
            entry = json.loads(path.read_text(encoding="utf-8"))
            out.append(str(entry.get("artifact_id", path.stem)))
        return tuple(out)

    def exists(self) -> bool:
        return self.root.is_dir()


def emit_registered_artifact(
    artifact: Mapping[str, Any], path: Path, *, registry: ConclusionSurfaceRegistry
) -> Path:
    """Register THEN write, one call — the registration/emission transaction boundary.

    The artifact must carry `artifact_id`, `kind` and the three stamps (they form the
    registry entry). The file write is `.tmp` → fsync → atomic rename and refuses to
    overwrite (NFR-AUD-01).

    Raises
    ------
    RegimeError
        registration refused (missing fields, duplicate) or the target file exists.
    """
    entry = {
        "artifact_id": artifact.get("artifact_id"),
        "kind": artifact.get("kind") or artifact.get("artifact_class"),
        "phase_id": artifact.get("phase_id"),
        "source_id": artifact.get("source_id"),
        "target_definition_id": artifact.get("target_definition_id"),
        "path": str(path),
    }
    registry.register(entry)
    payload = json.dumps(dict(artifact), sort_keys=True, indent=2, default=str)
    _write_once_atomic(
        Path(path), payload.encode("utf-8"), what=f"reported artifact {entry['artifact_id']!r}"
    )
    return Path(path)


# --- the ten guards -----------------------------------------------------------------------


def require_estimand_fields(row: Mapping[str, Any], *, surface: str) -> None:
    """Guard 1: refuse an estimand value without the canonical orientation + weighting.

    Raises
    ------
    RegimeError
        `orientation` absent or not `benchmark_minus_model`; `weighting` absent or not
        `equal_station` (SEC-R-02 half 1; R-108's machine-readable convention consumed).
    """
    if row.get("orientation") != ORIENTATION or row.get("weighting") != WEIGHTING:
        raise RegimeError(
            surface,
            f"estimand row {row.get('benchmark_id', '?')!r} carries orientation "
            f"{row.get('orientation')!r} / weighting {row.get('weighting')!r}, not the "
            f"recorded {ORIENTATION!r} / {WEIGHTING!r}; a value without its machine-"
            f"readable convention never renders (SEC-R-02 half 1)",
        )


def require_lineage_caveat(
    item: Mapping[str, Any], *, surface: str, kind: str = "row"
) -> None:
    """Guard 2: refuse any IRI/GIM comparison without the lineage caveat.

    For ``kind="row"`` (table/breakdown), the caveat is the TEC-06 sentence field emitted
    by the comparison-producing path — presence asserted, nothing emitted here. For
    ``kind="figure"``, "present" means the caveat rendered into the CAPTION or the figure
    METADATA (the gate's Rec 9 widening).

    Applies only to items that ARE IRI/GIM comparisons: a `benchmark_id` in the external
    comparator set, or an explicit `is_irigim_comparison` flag.

    Raises
    ------
    RegimeError
        the caveat absent or altered on an IRI/GIM item.
    """
    is_irigim = bool(item.get("is_irigim_comparison")) or (
        str(item.get("benchmark_id", "")) in EXTERNAL_COMPARATOR_IDS
    )
    if not is_irigim:
        return
    if kind == "figure":
        caption = str(item.get("caption", ""))
        metadata = item.get("metadata")
        labels = item.get("caveat_labels", ())
        in_metadata = isinstance(metadata, Mapping) and (
            metadata.get("spatial_representativeness_sentence")
            == SPATIAL_REPRESENTATIVENESS_SENTENCE
        )
        present = (
            SPATIAL_REPRESENTATIVENESS_SENTENCE in caption
            or SPATIAL_REPRESENTATIVENESS_SENTENCE in tuple(labels)
            or in_metadata
        )
    else:
        present = (
            item.get("spatial_representativeness_sentence")
            == SPATIAL_REPRESENTATIVENESS_SENTENCE
        )
    if not present:
        raise RegimeError(
            surface,
            f"IRI/GIM comparison {item.get('benchmark_id', item.get('plot_id', '?'))!r} "
            f"carries no lineage caveat (for a figure, 'present' means the caveat "
            f"rendered into the caption or figure metadata); the spatial-"
            f"representativeness statement travels wherever the comparison is reported "
            f"(TEC-06; Vision §6.6; SEC-R-02 half 2)",
        )


def require_units(mapping: Mapping[str, Any], *, surface: str) -> None:
    """Guard 3: refuse a value whose units assertion is absent or non-TECU.

    BLK-08's bound made checked, not silent: until the co-owner adopts its half of the
    R-103 joint contract no design path returns model output to TECU, so on real inputs
    THIS refusal is what fires instead of a wrong number shipping.

    Raises
    ------
    RegimeError
        `units` absent or not TECU.
    """
    units = mapping.get("units")
    if units != REQUIRED_UNITS:
        raise RegimeError(
            surface,
            f"units metadata is {units!r}, not {REQUIRED_UNITS!r} read from the "
            f"artifact; the table's units are asserted from metadata, never assumed "
            f"(R-125 limb 6; BLK-08 checked, not resolved)",
        )


def require_complete_members(
    present_member_ids: Sequence[str], *, declared_member_ids: Sequence[str], surface: str
) -> None:
    """Guard 4: refuse a table missing any declared comparison-set member's metric.

    Raises
    ------
    FairnessError
        the imported class of the consumed R-110 limb 1 completeness precondition —
        redundancy at the honesty boundary by design (R-125 limb 1).
    """
    missing = sorted(set(map(str, declared_member_ids)) - set(map(str, present_member_ids)))
    if missing:
        raise FairnessError(
            surface,
            f"declared member(s) {missing} carry no metric in the rendered table; the "
            f"render refuses rather than shipping a table with a member silently absent "
            f"(R-125 limb 1; PC-03/PC-04; FR-P1-05-9)",
        )


def require_d17_bound(
    stratum_field: str, *, configured_fields: Sequence[str], surface: str
) -> None:
    """Guard 5: refuse a breakdown stratum outside the configured D-17 enumerated set.

    Raises
    ------
    RegimeError
        a stratum on any field not in the configured enumeration (satellite count,
        elevation and zenith angle are absent from the five-column product by D-17).
    """
    if str(stratum_field) not in tuple(map(str, configured_fields)):
        raise RegimeError(
            surface,
            f"quality stratum requested on {stratum_field!r}, outside the configured "
            f"D-17 enumerated set {sorted(map(str, configured_fields))}; the strata "
            f"surface accepts only D-17's measured-available fields, never free strings "
            f"(R-127; D-17 § Observation-quality strata)",
        )


def require_registered_surface(
    artifact_id: str, *, registry: ConclusionSurfaceRegistry | None, surface: str
) -> Mapping[str, Any]:
    """Guard 6: refuse emission of a conclusion-bearing artifact not registered (Q1 = A).

    Fail-closed on an absent registry. The R-120 widening comparator has no registered
    surface, so any attempt to render its numbers lands here.

    Raises
    ------
    RegimeError
        no registry, or the artifact ID unregistered.
    """
    if registry is None or not registry.exists():
        raise RegimeError(
            surface,
            f"no ConclusionSurfaceArtifact registry exists at "
            f"{getattr(registry, 'root', '<none>')}; the registered-surface check fails "
            f"CLOSED — 'unrunnable therefore skipped' is not a path (Rec 21; control (36))",
        )
    entry = registry.lookup(str(artifact_id))
    if entry is None:
        raise RegimeError(
            surface,
            f"artifact {artifact_id!r} is conclusion-bearing and not registered in the "
            f"ConclusionSurfaceArtifact registry; emitting an unregistered surface "
            f"refuses (Q1 = A; SD-R-03; the widening comparator has no registered "
            f"surface by construction, R-120)",
        )
    return entry


def require_beats_model(rows: Sequence[Mapping[str, Any]], *, surface: str) -> None:
    """Guard 7: refuse a table row missing its per-benchmark `beats_model` field.

    The flag is PRINTED, never judged: this guard asserts presence only and never reads
    the value into a decision (R-16 stays a field comparison end to end).

    Raises
    ------
    RegimeError
        any benchmark row without the field.
    """
    for row in rows:
        if "beats_model" not in row:
            raise RegimeError(
                surface,
                f"benchmark row {row.get('benchmark_id', '?')!r} carries no beats_model "
                f"field; FR-P1-05-20's disclosure check is a field comparison and the "
                f"field must exist to compare (R-125 control (9))",
            )


def require_provenance_block(artifact: Mapping[str, Any], *, mask: Any, surface: str) -> None:
    """Guard 8: the five provenance fields present, then the scored window agrees.

    Presence (control (32)) covers a rendered primary table OR BREAKDOWN artifact —
    control (32)'s own wording — and the agreement half (control (33)) asserts the
    artifact's `scored_window_statement` equals the registered mask's own asserted scored
    range, so no independently authored denominator can render.

    Raises
    ------
    RegimeError
        any of the five fields absent/empty (naming them), or a scored-window statement
        that does not equal the mask's (naming both strings and the mask).
    """
    missing = [field for field in PROVENANCE_FIELDS if not artifact.get(field)]
    if missing:
        raise RegimeError(
            surface,
            f"provenance field(s) {missing} absent from the rendered artifact; the five "
            f"values are printed from the producing objects and never restated (Vision "
            f"§8.9; D-28; R-125 control (32); R-127 carries the same block on every "
            f"breakdown)",
        )
    stated = str(artifact.get("scored_window_statement", ""))
    recorded = str(getattr(mask, "scored_window_statement", ""))
    if stated != recorded:
        raise RegimeError(
            surface,
            f"scored_window_statement {stated!r} does not equal the registered mask "
            f"{getattr(mask, 'mask_id', '?')!r}'s asserted scored range {recorded!r}; "
            f"one denominator exists in one place (D-28; R-125 control (33))",
        )


def require_derived_label(field: Mapping[str, Any], *, surface: str) -> None:
    """Guard 9: refuse a derived quantity rendered without its `derived: true` label.

    Raises
    ------
    RegimeError
        the §5.5 percentage RMSE reduction (or any derived field passed here) whose
        `derived` label is absent or not True (Vision §9.5 required result 2, "clearly
        labeled as derived"; R-127 control (34)).
    """
    if field.get("derived") is not True:
        raise RegimeError(
            surface,
            f"derived quantity {field.get('name', 'derived_percentage_rmse_reduction')!r} "
            f"rendered without its explicit derived: true label; a derived summary is "
            f"clearly labeled as derived, always (Vision §9.5 required result 2; R-127 "
            f"control (34))",
        )


def require_driver_caveat(breakdown: Mapping[str, Any], *, surface: str) -> None:
    """Guard 10: refuse a per-station breakdown without the standing TC-12 caveat.

    Raises
    ------
    RegimeError
        `driver_identity_caveat` absent or altered on a per-station/per-cell breakdown
        (TC-12 `binding: hard`; R-127 control (38); emitted by the producing path so it
        cannot be omitted from a breakdown nobody has written yet).
    """
    if breakdown.get("driver_identity_caveat") != DRIVER_IDENTITY_CAVEAT:
        raise RegimeError(
            surface,
            f"per-station breakdown {breakdown.get('breakdown_id', '?')!r} carries no "
            f"standing driver-identity caveat; every external driver value is identical "
            f"across the three cells by construction and the no-local-forcing caveat is "
            f"emitted from the producing path itself (TC-12; Rec 17; R-127 control (38))",
        )
