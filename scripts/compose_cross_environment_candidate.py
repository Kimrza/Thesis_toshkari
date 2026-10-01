"""Compose a fixture candidate manifest from RECORDED measuring results, running nothing.

Purpose: D-83 revision 8 section A8 items 9, 10 and 17 compose the item 11 per-field
tolerance from the designated (a) `tec-thesis-311` and (c) `g07-clean-run` measuring runs.
`run_walking_skeleton.py --emit-candidate --measuring-runs` can only compose while
performing ANOTHER run, which would add an undesignated run to the composition. This
script composes the same candidate from exactly the precommitted measuring results, with
the runner's own functions (`compose_measurement_ranges`, `compose_tolerances`,
`recorded_quantities`, `compose_candidate_manifest`), so there is one composition path.

Inputs: `--config configs/` (unused beyond the workspace root, kept for the stage-script
CLI convention), `--fixture`, `--identity` (the owner's identity declaration), and two or
more `--result` paths (measuring_result_<run_id>.json). The fixture root's live outputs
must be those of one of the named runs (their hash listing and recorded quantities are
read from it); `--outputs-run` names which, and it must be one of the results.
Re-run behaviour: writes `fixture_manifest.candidate_<outputs-run>+xenv.yaml` beside the
reference manifest and refuses if that file exists. Never writes `frozen` (the owner's
Q-31 act) and never touches the reference manifest.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.data.config import IntegrityError  # noqa: E402
from src.data.fixture_manifest import (  # noqa: E402
    compose_candidate_manifest,
    compose_measurement_ranges,
    load_identity_declaration,
    write_candidate_manifest,
)


def _runner():
    spec = importlib.util.spec_from_file_location(
        "run_walking_skeleton", REPO_ROOT / "scripts" / "run_walking_skeleton.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compose(
    *, fixture: str, identity: Path, results: list[Path], outputs_run: str
) -> Path:
    rws = _runner()
    workspace = REPO_ROOT
    scope = load_identity_declaration(identity)
    loaded = [json.loads(Path(p).read_text(encoding="utf-8")) for p in results]
    run_ids = [str(r.get("measuring_run_id")) for r in loaded]
    if len(set(run_ids)) != len(run_ids):
        raise IntegrityError("--result", f"duplicate measuring_run_id among {run_ids}")
    if len(loaded) < 2:
        raise IntegrityError("--result", "a candidate is composed from at least two runs")
    if outputs_run not in run_ids:
        raise IntegrityError(
            "--outputs-run", f"{outputs_run} is not one of the composed results {run_ids}"
        )
    fixture_root = workspace / "artifacts" / "walking_skeleton" / fixture
    template = scope.data.get("required_outputs", {}).get("comparison_ledger", {})
    toleranced = sorted(
        name for name, entry in template.items()
        if isinstance(entry, dict) and entry.get("comparison_class") == "toleranced"
    )
    listing, missing = rws.collect_required_outputs(fixture_root, scope)
    if missing:
        raise IntegrityError(fixture_root, f"required outputs missing: {missing}")
    composed = compose_measurement_ranges(loaded)
    tolerances = rws.compose_tolerances(loaded, template, toleranced)
    skeleton_path = rws.manifest_path_for(workspace, fixture)
    recorded = rws.recorded_quantities(
        workspace=workspace,
        fixture_root=fixture_root,
        skeleton=rws._parse_yaml_text(
            skeleton_path, skeleton_path.read_text(encoding="utf-8")
        ),
        ledger_template=template,
        driver_releases=rws.RECORDED_DRIVER_RELEASES,
        gim_release=rws.RECORDED_GIM_RELEASE,
        target_release=rws.RECORDED_TARGET_RELEASE,
        site_log=workspace / rws.RECORDED_SITE_LOG,
        site_log_manifest=workspace / rws.RECORDED_SITE_LOG_MANIFEST,
        b01_manifest=workspace / rws.RECORDED_B01_MANIFEST,
    )
    candidate = compose_candidate_manifest(
        scope.data,
        fixture_id=fixture,
        measurements=composed,
        measuring_run_id="+".join(sorted(run_ids)),
        outputs=sorted(listing),
        comparison_ledger=template,
        tolerances=tolerances,
        recorded=recorded,
        artifact_manifest_ref=os.path.relpath(
            fixture_root / rws.ARTIFACT_MANIFEST_NAME, skeleton_path.parent
        ),
    )
    target = skeleton_path.parent / f"fixture_manifest.candidate_{outputs_run}+xenv.yaml"
    if target.exists():
        raise IntegrityError(target, "already exists; a candidate is written once")
    return write_candidate_manifest(target, candidate)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", required=True)
    parser.add_argument("--fixture", required=True, choices=["plumbing_7day", "scientific_1month"])
    parser.add_argument("--identity", required=True, type=Path)
    parser.add_argument("--result", required=True, action="append", type=Path)
    parser.add_argument("--outputs-run", required=True)
    args = parser.parse_args(argv)
    try:
        written = compose(
            fixture=args.fixture, identity=args.identity,
            results=args.result, outputs_run=args.outputs_run,
        )
    except IntegrityError as exc:
        print(f"compose_cross_environment_candidate: refused: {exc}", file=sys.stderr)
        return 1
    print(written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
