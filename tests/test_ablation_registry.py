"""TE 7.2 ablation run-ID registration (src/models/ablation_registry.py): negative controls.

PURPOSE. A registration act is adopted only when all five TE 7.2 ablations carry a
convention-conforming, unique, non-colliding run ID and a UTC `registered_at`. Each of those
conditions has a test showing its violation is caught. The live `configs/experiment.yaml`
still reads `TBD — freeze gate`, and the test asserts that it refuses.

INPUTS. Synthetic `AblationEntry` tuples; the live config read only for the TBD assertion.

RE-RUN. Pure.
"""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

ar = pytest.importorskip("src.models.ablation_registry")
from src.data.config import IntegrityError  # noqa: E402
from src.models.train import ABLATION_IDS, AblationEntry  # noqa: E402

WHEN = "2026-10-03T09:00:00+00:00"


def _entries(**overrides) -> list[AblationEntry]:
    out = []
    for aid in ABLATION_IDS:
        fields = dict(
            ablation_id=aid,
            run_id=ar.canonical_run_id(aid),
            registered_at=WHEN,
            phase1_reachable=aid != "ABL-ZENITH",
            phase_deferral=None,
            inverse_before_metric=aid == "ABL-DIFF",
            after_primary_freeze_only=aid == "ABL-HIST48",
            configuration_change="",
        )
        fields.update(overrides.get(aid, {}))
        out.append(AblationEntry(**fields))
    return out


def test_canonical_ids_are_derived_from_identity_only_and_printed():
    ids = [ar.canonical_run_id(a) for a in ABLATION_IDS]
    print(ids)
    assert ids == [
        "ablation-abl-nodoy",
        "ablation-abl-diff",
        "ablation-abl-nosw",
        "ablation-abl-hist48",
        "ablation-abl-zenith",
    ]
    assert len(set(ids)) == 5


def test_a_complete_registration_passes():
    got = ar.assert_registration(_entries(), registry_run_ids=["models-and-baselines-x"])
    assert set(got) == set(ABLATION_IDS)


def test_unknown_ablation_has_no_canonical_id():
    with pytest.raises(IntegrityError):
        ar.canonical_run_id("ABL-INVENTED")


@pytest.mark.parametrize("field", ["run_id", "registered_at"])
def test_tbd_run_id_or_timestamp_refuses(field):
    with pytest.raises(IntegrityError, match="TBD"):
        ar.assert_registration(_entries(**{"ABL-NOSW": {field: None}}), registry_run_ids=[])


def test_missing_ablation_refuses():
    with pytest.raises(IntegrityError, match="exactly"):
        ar.assert_registration(_entries()[:4], registry_run_ids=[])


def test_duplicated_ablation_refuses():
    entries = _entries()
    with pytest.raises(IntegrityError, match="exactly"):
        ar.assert_registration(entries + [entries[0]], registry_run_ids=[])


def test_duplicate_run_id_refuses():
    entries = _entries(**{"ABL-NOSW": {"run_id": "ablation-abl-nodoy"}})
    with pytest.raises(IntegrityError, match="does not match"):
        ar.assert_registration(entries, registry_run_ids=[])


def test_swapped_run_ids_refuse():
    entries = _entries(
        **{
            "ABL-NODOY": {"run_id": "ablation-abl-diff"},
            "ABL-DIFF": {"run_id": "ablation-abl-nodoy"},
        }
    )
    with pytest.raises(IntegrityError, match="does not match"):
        ar.assert_registration(entries, registry_run_ids=[])


@pytest.mark.parametrize("existing", ["ablation-abl-hist48", "ablation-abl-hist48/F1/seed-7"])
def test_collision_with_registry_refuses(existing):
    with pytest.raises(IntegrityError, match="collides"):
        ar.assert_registration(_entries(), registry_run_ids=[existing])


def test_prefix_lookalike_is_not_a_collision():
    ar.assert_registration(_entries(), registry_run_ids=["ablation-abl-hist480"])


@pytest.mark.parametrize("bad", ["yesterday", "2026-10-03T09:00:00", "2026-10-03T09:00:00+03:30"])
def test_registered_at_must_be_iso_utc(bad):
    with pytest.raises(IntegrityError, match="registered_at"):
        ar.assert_registration(
            _entries(**{"ABL-DIFF": {"registered_at": bad}}), registry_run_ids=[]
        )


def test_child_run_id_names_fold_and_seed():
    assert (
        ar.child_run_id("ablation-abl-nosw", fold_id="F3", seed=1337)
        == "ablation-abl-nosw/F3/seed-1337"
    )


def test_the_live_config_is_still_tbd_and_refuses():
    """The registration act has not been adopted; the live config must refuse, not pass."""
    yaml = pytest.importorskip("yaml")
    block = yaml.safe_load((REPO_ROOT / "configs" / "experiment.yaml").read_text(encoding="utf-8"))
    entries = [
        dataclasses.replace(
            _entries()[i],
            run_id=None if "TBD" in str(e["run_id"]) else str(e["run_id"]),
            registered_at=None if "TBD" in str(e["registered_at"]) else str(e["registered_at"]),
        )
        for i, (aid, e) in enumerate((a, block["ablations"]["entries"][a]) for a in ABLATION_IDS)
    ]
    if all(e.run_id for e in entries):
        ar.assert_registration(entries, registry_run_ids=[])  # adopted: must then pass
    else:
        with pytest.raises(IntegrityError, match="TBD"):
            ar.assert_registration(entries, registry_run_ids=[])
