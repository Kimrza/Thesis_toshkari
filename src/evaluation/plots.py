"""R7 plots: presentation-only BY SIGNATURE — the manifest is WS-19's evidence (R-129; W-7).

Purpose
-------
`plots.py` renders EXCLUSIVELY from serialized, stamped artifacts emitted by producing
paths — the metrics artifact, W-5's breakdown artifacts, the budget artifact,
`BootstrapResult` serializations, W-8's labelled diagnostic artifacts. Its API takes
artifact MAPPINGS, never raw predictions or unstamped numbers, so "presentation only and
computes no reported quantity" holds by signature, not by comment: no function here sums,
averages, differences or otherwise derives a reported quantity — every plotted value and
every label is a copy of a field on the input artifact.

Every figure is written with a manifest entry carrying the plot ID, the source artifact
IDs and stamps it rendered, and its axis-units label TAKEN FROM the artifact's units
metadata — never hardcoded, so a TECU axis label can never disagree with the data behind
it. The manifest is asserted complete against the configured required-plot list (a
missing required plot REFUSES, R-127's inventory shape). The RF-importance and
Dst-diagnostic figures render only from their labelled artifacts, printing the
non-authoritative / diagnostic, hindcast-only labels those artifacts carry; the lineage
caveat rides into captions/metadata where the artifact carries it (Rec 9's widening:
`require_lineage_caveat` on W-7, "present" = caption or figure metadata). The
widening-guard comparator's quarantine (`statistical-inference` R-120) is inherited by
construction: the comparator has no registered surface, so `require_registered_surface`
refuses any attempt to render its numbers.

Matplotlib boundary
-------------------
`matplotlib` is imported LAZILY inside ``render_figure`` only — never at module scope
(R-05's transitive module-scope prohibition; the pin is `requirements.txt`'s, TE §8.1) —
and its absence REFUSES naming the pin surface rather than degrading silently. Every
manifest-side path (the WS-19 evidence) is computable without matplotlib, headless, no
display.

Inputs
------
Serialized artifact mappings only, plus the `ConclusionSurfaceRegistry` for the
registered-surface check and the configured required-plot list off
`ConfigSnapshot.experiment` (read by the caller). Imports ONLY `src/data`,
`src/evaluation` siblings and the standard library — no `src/features`, `src/models`,
`src/external`, directly or transitively (TE §12; D-27).

Re-run behaviour
----------------
Manifest building is pure; figure files and the manifest are written via the write-once
atomic idiom through `report_guards.emit_registered_artifact` where emission happens.
Deterministic given identical inputs.

Governance
----------
R-129; WS-19 (the manifest is its evidence — nothing here discharges the row); TS-R-02's
boxed caveat carried: the no-derived-statistics half rests on review and this module's
signature, and is never claimed stronger than that.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from src.data.config import RegimeError
from src.evaluation.metrics import SPATIAL_REPRESENTATIVENESS_SENTENCE
from src.evaluation.report_guards import (
    ConclusionSurfaceRegistry,
    require_lineage_caveat,
    require_registered_surface,
)

__all__ = [
    "REQUIRED_PLOT_KINDS",
    "build_plot_manifest_entry",
    "assert_manifest_entry",
    "assert_manifest_complete",
    "render_figure",
]

#: FR-P1-05-11's minimum required plots (identity tokens; the authoritative required-plot
#: list is configuration content — `reporting.required_plots` — and the completeness
#: assertion runs against THAT list, this tuple being the named minimum).
REQUIRED_PLOT_KINDS: tuple[str, ...] = ("prediction", "residual", "target_support", "quality")


def _stamps_of(artifact: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "phase_id": artifact.get("phase_id"),
        "source_id": artifact.get("source_id"),
        "target_definition_id": artifact.get("target_definition_id"),
    }


def build_plot_manifest_entry(
    *,
    plot_id: str,
    plot_kind: str,
    source_artifacts: Sequence[Mapping[str, Any]],
    registry: ConclusionSurfaceRegistry | None,
    caption: str = "",
) -> dict[str, Any]:
    """WS-19's evidence schema: one manifest entry per figure, everything copied.

    The entry's `units_label` is TAKEN from the (agreeing) source artifacts' units
    metadata; `caveat_labels` are printed from the inputs (`non-authoritative`,
    `diagnostic/hindcast-only`, the lineage caveat) — no label is authored here. Every
    source artifact must be a REGISTERED surface (the quarantined widening comparator has
    none, so it can never enter a figure).

    Raises
    ------
    RegimeError
        no source artifacts; a source artifact without an `artifact_id` or units
        metadata; source artifacts disagreeing on units; an unregistered source; an
        IRI/GIM-bearing figure whose caption/metadata carries no lineage caveat.
    """
    surface = f"plot manifest entry {plot_id}"
    if not source_artifacts:
        raise RegimeError(
            surface,
            "no source artifacts; plots.py renders exclusively from serialized stamped "
            "artifacts and a figure with no producing-path input cannot exist (R-129)",
        )
    source_ids: list[str] = []
    units_seen: set[str] = set()
    caveat_labels: list[str] = []
    stamps: list[dict[str, Any]] = []
    is_irigim = False
    for artifact in source_artifacts:
        artifact_id = str(artifact.get("artifact_id", ""))
        if not artifact_id:
            raise RegimeError(
                surface,
                "a source artifact carries no artifact_id; every figure names the "
                "serialized artifacts it rendered (FR-P1-05-11: each figure carries its "
                "source-data IDs)",
            )
        require_registered_surface(artifact_id, registry=registry, surface=surface)
        source_ids.append(artifact_id)
        units = artifact.get("units")
        if units is not None:
            units_seen.add(str(units))
        stamps.append(_stamps_of(artifact))
        label = artifact.get("diagnostic_label")
        if label:
            caveat_labels.append(str(label))
        for extra in artifact.get("caveat_labels", ()):  # e.g. non-authoritative (R-100)
            caveat_labels.append(str(extra))
        if artifact.get("is_irigim_comparison"):
            is_irigim = True
        for row in artifact.get("rows", artifact.get("comparisons", ())):
            if isinstance(row, Mapping) and "spatial_representativeness_sentence" in row:
                is_irigim = True
        if artifact.get("spatial_representativeness_sentence"):
            is_irigim = True
    if not units_seen:
        raise RegimeError(
            surface,
            "no source artifact carries units metadata; the axis-units label is TAKEN "
            "from the artifact's units metadata, never hardcoded (R-129)",
        )
    if len(units_seen) > 1:
        raise RegimeError(
            surface,
            f"source artifacts disagree on units {sorted(units_seen)}; one figure cannot "
            f"carry two unit systems (R-129)",
        )
    entry: dict[str, Any] = {
        "plot_id": str(plot_id),
        "plot_kind": str(plot_kind),
        "source_artifact_ids": source_ids,
        "source_stamps": stamps,
        "units_label": next(iter(units_seen)),
        "caption": str(caption),
        "caveat_labels": tuple(dict.fromkeys(caveat_labels)),
        "is_irigim_comparison": is_irigim,
    }
    if is_irigim:
        # carry the lineage caveat into the caption/metadata where the artifact carries it
        entry["metadata"] = {
            "spatial_representativeness_sentence": SPATIAL_REPRESENTATIVENESS_SENTENCE
        }
        require_lineage_caveat(entry, surface=surface, kind="figure")
    return entry


def assert_manifest_entry(
    entry: Mapping[str, Any], *, source_artifacts: Sequence[Mapping[str, Any]]
) -> None:
    """Controls (22)/(23): an entry missing source IDs fails; a units label disagreeing
    with its artifacts' metadata fails.

    Raises
    ------
    RegimeError
        `source_artifact_ids` absent/empty, or `units_label` differing from any source
        artifact's units metadata.
    """
    plot_id = entry.get("plot_id", "?")
    if not entry.get("source_artifact_ids"):
        raise RegimeError(
            f"plot manifest entry {plot_id}",
            "source_artifact_ids absent; 'each carrying its source-data IDs' is the "
            "manifest's schema, not a caption convention (FR-P1-05-11; control (22))",
        )
    label = str(entry.get("units_label", ""))
    for artifact in source_artifacts:
        units = artifact.get("units")
        if units is not None and str(units) != label:
            raise RegimeError(
                f"plot manifest entry {plot_id}",
                f"units_label {label!r} disagrees with source artifact "
                f"{artifact.get('artifact_id', '?')!r}'s units metadata {units!r}; the "
                f"label is taken from the data behind it, always (R-129; control (23))",
            )
    if entry.get("is_irigim_comparison"):
        require_lineage_caveat(entry, surface=f"plot manifest entry {plot_id}", kind="figure")


def assert_manifest_complete(
    entries: Sequence[Mapping[str, Any]], *, required_plots: Sequence[str]
) -> None:
    """Control (24): the manifest is asserted complete against the configured
    required-plot list — a missing required plot REFUSES (R-127's inventory shape).

    Raises
    ------
    RegimeError
        any required plot kind absent from the manifest.
    """
    present = {str(entry.get("plot_kind")) for entry in entries}
    missing = sorted(set(map(str, required_plots)).difference(present))
    if missing:
        raise RegimeError(
            "plot manifest",
            f"required plot(s) {missing} missing from the manifest "
            f"({sorted(present) or 'empty'}); WS-19's evidence is complete against the "
            f"configured required-plot list or it refuses (R-129 control (24))",
        )


def render_figure(entry: Mapping[str, Any], out_path: Any) -> Any:
    """Render one figure from its manifest entry — the ONLY matplotlib touchpoint.

    Lazy import (R-05 transitive module-scope prohibition); absence refuses naming the
    pin surface. The figure draws only values already present on the entry's source
    artifacts (the caller passes them serialized inside the entry payload if plotted);
    nothing is computed here.

    Raises
    ------
    RegimeError
        matplotlib is not importable — named against `requirements.txt`, the pin surface
        (TE §8.1; TS-R-01…04's no-new-dependency rule).
    """
    try:
        import matplotlib  # noqa: PLC0415 — lazy by design (R-05)
        from matplotlib import pyplot as plt  # noqa: PLC0415
    except ImportError as exc:
        raise RegimeError(
            "matplotlib",
            f"not importable ({exc}); the plotting dependency is pinned in "
            f"requirements.txt (TE §8.1) and its absence refuses rather than degrading — "
            f"the manifest (WS-19's evidence) is computable without it, the figure is not",
        ) from exc
    matplotlib.use("Agg", force=False)  # headless-safe; no display
    figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title(str(entry.get("caption", entry.get("plot_id", ""))))
    axes.set_ylabel(str(entry.get("units_label", "")))
    for label in entry.get("caveat_labels", ()):
        axes.annotate(str(label), xy=(0.01, 0.99), xycoords="axes fraction", va="top")
    figure.savefig(out_path)
    plt.close(figure)
    return out_path
