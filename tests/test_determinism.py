"""C-1 Resolve tests: determinism, configs, preflight, platform, credentials, the lock.

Purpose
-------
The executable controls for `src/data/config.py` (C-1), created as
`tests/test_determinism.py` under the authority of `CR-2026-08-22-TE-AMEND` (which
granted the module NAME; writing it is this Bolt's act under G-09/D-31). Covers:
R-02/R-03 (`assert_no_tbd` fires on a planted `TBD — freeze gate`; required-fields map),
R-05 (re-exec establishes `PYTHONHASHSEED` before any framework import; the sentinel is
read once and popped; `seed_everything` raises when TensorFlow is already initialised),
R-06 (declared-vs-observed mismatches surface; an empty `nondeterministic_ops` is never
presented as proof), R-14 (credential NAMES only; missing names fail early BY NAME; no
canary value in any foundation return), R-15 (no foundation module constructs a path
into the restricted root — a static source scan), R-16 (no absolute path in a governed
config; relocation leaves hashes unchanged), R-17 (module docstrings carry purpose /
inputs / re-run), W-2 (strict YAML, duplicate keys rejected, verbatim snapshot),
W-5/REQ-ENG-10 (the eight-item lock captured 8/8, and an incomplete lock FAILS), W-8
(`PlatformError` on any platform that is not exactly kaggle|local), and the
governed-config hash-mismatch termination naming file + expectation.

R-01's ENUMERATION CENSUS lives here too, in the final section: the control R-01's own
text mandates, re-deriving every project-defined `*Error` name raised across the units'
`functional-design` artifacts and failing when one is neither in R-01's enumeration nor
disclosed under its any-future clause. It is homed in this module because
`src/data/config.py` -- this module's subject -- is R-01's declaration site, and because
this is already where the unit's static-scan controls (R-15, R-17) live. Neither R-01 nor
`foundation`'s design names a module for it, and placing it here needs no TE 12 `tests/`
naming amendment.

Inputs
------
`tmp_path` and `monkeypatch`; the repository `configs/` tree is read but never written.
The R-01 census additionally READS (never writes) the record tree at
`aidlc/spaces/default/intents/260813-tec-hourly-forecast/construction/*/functional-design/*.md`,
and `src/data/config.py` as text. No network. No restricted-root path is constructed (the
static R-15 control scans source text, which is the sanctioned way to name the boundary
without reaching it).

Re-run behaviour
----------------
Deterministic and self-contained; every test builds its own config tree in `tmp_path`.
The re-exec control runs a child interpreter via subprocess with a file handshake, so
Windows `os.execv` (spawn-replacement) semantics do not race the assertion.

The R-01 census is deterministic for a given record tree and asserts no numeral, so it
re-runs unchanged as the artifact set grows: it reports a reconciliation, and the only
event that turns it red is a project-defined `*Error` name that is neither enumerated by
R-01 nor disclosed under R-01's any-future clause. Its own negative controls run entirely
in `tmp_path` and never read the record tree.
"""

from __future__ import annotations

import builtins
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import NamedTuple

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import (  # noqa: E402
    CREDENTIAL_NAME_MAP,
    GOVERNED_CONFIG_FILES,
    REEXEC_SENTINEL_ENV,
    REQUIRED_FIELDS_MAP,
    TBD_SENTINEL,
    ConfigError,
    DeterminismError,
    IntegrityError,
    PlatformError,
    PreflightError,
    SeedError,
    assert_config_hashes_match,
    assert_credential_names_present,
    assert_declared_sources_exist,
    assert_lock_complete,
    assert_no_tbd,
    capture_environment_lock,
    environment_lock_hash,
    load_configs,
    required_fields_for,
    resolve_platform_roots,
    seed_everything,
)

CONFIGS_DIR = REPO_ROOT / "configs"

#: Foundation's own modules — the R-15/R-17 static-scan population. `locked_test.py`
#: is `governance-guards`' and is deliberately NOT in this list.
FOUNDATION_MODULES = (
    REPO_ROOT / "src" / "data" / "config.py",
    REPO_ROOT / "src" / "data" / "release.py",
    REPO_ROOT / "src" / "data" / "experiment_registry.py",
)


# --- helpers ----------------------------------------------------------------------------


def _write_config_tree(root: Path, *, seeds_extra: str = "") -> Path:
    """A minimal valid four-file governed config tree in tmp space.

    Every consumer immediately parses the tree through `load_configs`, whose production
    read path is pyyaml BY DESIGN (TS-01: refuse by name, never a second parser) — so on
    a clone where pyyaml is uninstallable these tests SKIP BY NAME here rather than
    erroring at the loader's refusal. Classification, not suppression: the same tests
    run in full in a governed environment. (Owner gate worklist 2026-09-10, item 3;
    flagged for `foundation`'s record.)
    """
    pytest.importorskip("yaml")
    config_dir = root / "configs"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "data.yaml").write_text(
        'schema_version: "1.0.0"\n'
        "roots:\n"
        '  release_root: "artifacts/releases"\n'
        '  snapshot_root: "artifacts/run_snapshots"\n'
        '  registry_root: "artifacts/registry"\n'
        "declared_sources: []\n",
        encoding="utf-8",
    )
    (config_dir / "features.yaml").write_text(
        'schema_version: "1.0.0"\nfeature_set_id: "TBD — freeze gate"\n', encoding="utf-8"
    )
    (config_dir / "experiment.yaml").write_text(
        'schema_version: "1.0.0"\nfolds: "TBD — freeze gate"\n', encoding="utf-8"
    )
    (config_dir / "seeds.yaml").write_text(
        'schema_version: "1.0.0"\n'
        "development: 42\n"
        "final: [1337, 2024, 7]\n"
        "bootstrap: 20221201\n"
        "determinism:\n"
        "  expected_nondeterministic_ops: []\n" + seeds_extra,
        encoding="utf-8",
    )
    return config_dir


@pytest.fixture()
def snapshot(tmp_path, monkeypatch):
    """A ConfigSnapshot over a tmp config tree, platform forced local, workspace tmp."""
    config_dir = _write_config_tree(tmp_path)
    monkeypatch.setenv("TEC_PLATFORM", "local")
    monkeypatch.setenv("TEC_WORKSPACE_ROOT", str(tmp_path))
    return load_configs(config_dir, phase=1)


# --- the four governed configs in the repository ----------------------------------------


def test_repository_configs_exist_and_parse(monkeypatch, tmp_path) -> None:
    """The real configs/ tree: all four exist, parse strictly, and carry no machine path."""
    pytest.importorskip("yaml")  # the loader's read path is pyyaml by design (TS-01)
    monkeypatch.setenv("TEC_PLATFORM", "local")
    monkeypatch.setenv("TEC_WORKSPACE_ROOT", str(tmp_path))
    snap = load_configs(CONFIGS_DIR, phase=1)
    assert set(snap.hashes) == set(GOVERNED_CONFIG_FILES)
    # Frozen D-122 values, transcribed with their D-number, are present and resolved.
    assert snap.seeds["development"] == 42
    assert snap.seeds["final"] == [1337, 2024, 7]
    assert snap.seeds["bootstrap"] == 20221201


def test_no_config_value_parses_as_an_absolute_path(monkeypatch, tmp_path) -> None:
    """R-16 negative control, half 1: no value in any of the four configs is absolute."""
    pytest.importorskip("yaml")  # the loader's read path is pyyaml by design (TS-01)
    monkeypatch.setenv("TEC_PLATFORM", "local")
    monkeypatch.setenv("TEC_WORKSPACE_ROOT", str(tmp_path))
    snap = load_configs(CONFIGS_DIR, phase=1)

    def _walk(node, trail):
        if isinstance(node, dict):
            for key, value in node.items():
                _walk(value, f"{trail}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                _walk(value, f"{trail}[{index}]")
        elif isinstance(node, str):
            assert not Path(node).is_absolute(), (
                f"{trail} = {node!r} parses as an absolute path; no machine path may "
                f"enter a governed config (R-16, ADR-07)"
            )

    for name, config in (
        ("data", snap.data),
        ("features", snap.features),
        ("experiment", snap.experiment),
        ("seeds", snap.seeds),
    ):
        _walk(dict(config), name)


def test_relocating_the_workspace_leaves_governed_hashes_unchanged(
    tmp_path, monkeypatch
) -> None:
    """R-16 negative control, half 2: moving the tree never changes a governed hash."""
    config_dir = _write_config_tree(tmp_path / "site_a")
    monkeypatch.setenv("TEC_PLATFORM", "local")
    monkeypatch.setenv("TEC_WORKSPACE_ROOT", str(tmp_path / "site_a"))
    hashes_a = load_configs(config_dir, phase=1).hashes

    relocated = _write_config_tree(tmp_path / "site_b")  # identical bytes, new location
    monkeypatch.setenv("TEC_WORKSPACE_ROOT", str(tmp_path / "site_b"))
    hashes_b = load_configs(relocated, phase=1).hashes
    assert hashes_a == hashes_b


def test_an_absolute_root_in_a_config_is_refused(tmp_path, monkeypatch) -> None:
    """R-16 enforced at load: a config-declared absolute root terminates, named."""
    config_dir = _write_config_tree(tmp_path)
    (config_dir / "data.yaml").write_text(
        'schema_version: "1.0.0"\nroots:\n  release_root: "C:/absolute/machine/path"\n',
        encoding="utf-8",
    )
    monkeypatch.setenv("TEC_PLATFORM", "local")
    monkeypatch.setenv("TEC_WORKSPACE_ROOT", str(tmp_path))
    with pytest.raises(ConfigError) as excinfo:
        load_configs(config_dir, phase=1)
    assert "release_root" in str(excinfo.value)
    assert "R-16" in str(excinfo.value)


def test_duplicate_yaml_key_is_an_integrity_failure(tmp_path, monkeypatch) -> None:
    """W-2 step 2: a duplicate key silently dropping a governed value is refused."""
    config_dir = _write_config_tree(tmp_path)
    (config_dir / "seeds.yaml").write_text(
        "development: 42\ndevelopment: 43\n", encoding="utf-8"
    )
    monkeypatch.setenv("TEC_PLATFORM", "local")
    monkeypatch.setenv("TEC_WORKSPACE_ROOT", str(tmp_path))
    with pytest.raises(ConfigError) as excinfo:
        load_configs(config_dir, phase=1)
    assert "duplicate key" in str(excinfo.value)


def test_missing_config_file_is_named(tmp_path, monkeypatch) -> None:
    config_dir = _write_config_tree(tmp_path)
    (config_dir / "experiment.yaml").unlink()
    monkeypatch.setenv("TEC_PLATFORM", "local")
    monkeypatch.setenv("TEC_WORKSPACE_ROOT", str(tmp_path))
    with pytest.raises(ConfigError) as excinfo:
        load_configs(config_dir, phase=1)
    assert "experiment.yaml" in str(excinfo.value)


def test_invalid_phase_is_refused(tmp_path) -> None:
    with pytest.raises(ConfigError):
        load_configs(_write_config_tree(tmp_path), phase=3)


def test_snapshot_is_verbatim(snapshot, tmp_path) -> None:
    """W-2 step 3: the snapshot copies are byte-identical to what the run read."""
    for name in GOVERNED_CONFIG_FILES:
        original = (tmp_path / "configs" / name).read_bytes()
        copy = (snapshot.snapshot_dir / name).read_bytes()
        assert original == copy


def test_governed_hash_mismatch_terminates_naming_file_and_expectation(snapshot) -> None:
    """Negative control (plan step 4): a tampered snapshot copy terminates, named."""
    tampered = snapshot.snapshot_dir / "seeds.yaml"
    tampered.write_text("development: 999\n", encoding="utf-8")
    with pytest.raises(ConfigError) as excinfo:
        assert_config_hashes_match(snapshot)
    message = str(excinfo.value)
    assert "seeds.yaml" in message  # names the file
    assert "hash" in message  # names the violated expectation


# --- W-3: assert_no_tbd and declared sources --------------------------------------------


def test_assert_no_tbd_fires_on_a_planted_sentinel(snapshot) -> None:
    """Negative control (R-02): the literal `TBD — freeze gate` is caught and named."""
    with pytest.raises(PreflightError) as excinfo:
        assert_no_tbd(snapshot, required=["features.feature_set_id"])
    message = str(excinfo.value)
    assert "features.feature_set_id" in message
    assert TBD_SENTINEL in message


def test_assert_no_tbd_collects_every_offender_and_absentees(snapshot) -> None:
    """R-02: ALL offenders in one raise — absent fields and sentinels alike."""
    with pytest.raises(PreflightError) as excinfo:
        assert_no_tbd(
            snapshot,
            required=["features.feature_set_id", "experiment.folds", "data.no_such_field"],
        )
    message = str(excinfo.value)
    assert "features.feature_set_id" in message
    assert "experiment.folds" in message
    assert "data.no_such_field" in message and "absent" in message


def test_assert_no_tbd_passes_on_resolved_fields(snapshot) -> None:
    assert_no_tbd(
        snapshot, required=["seeds.development", "seeds.final", "seeds.bootstrap"]
    )


def test_required_fields_map_has_no_silent_empty_default() -> None:
    """R-03: an absent (stage, phase) entry is a loud failure, never an empty set."""
    assert required_fields_for("foundation", 1) == (
        "seeds.development",
        "seeds.final",
        "seeds.bootstrap",
    )
    with pytest.raises(ConfigError):
        required_fields_for("no_such_stage", 1)


def test_required_fields_map_completeness(monkeypatch, tmp_path) -> None:
    """R-03's completeness control: every governed non-TBD scientific field in the
    repository configs appears in at least one map entry (today: the D-122 seeds)."""
    pytest.importorskip("yaml")  # the loader's read path is pyyaml by design (TS-01)
    monkeypatch.setenv("TEC_PLATFORM", "local")
    monkeypatch.setenv("TEC_WORKSPACE_ROOT", str(tmp_path))
    snap = load_configs(CONFIGS_DIR, phase=1)
    frozen_fields = {"seeds.development", "seeds.final", "seeds.bootstrap"}
    mapped = {field for entry in REQUIRED_FIELDS_MAP.values() for field in entry}
    unmapped = frozen_fields - mapped
    assert not unmapped, (
        f"governed frozen fields appear in no REQUIRED_FIELDS_MAP entry: {unmapped}; "
        f"the map is a list and this test is what makes it a rule (R-03)"
    )
    assert snap.seeds["development"] == 42  # the fields the map names are real


def test_declared_source_that_does_not_resolve_is_a_failure(tmp_path, monkeypatch) -> None:
    """W-3 step 5 (DATA-13): a declared hash that does not resolve fails, never warns."""
    config_dir = _write_config_tree(tmp_path)
    (config_dir / "data.yaml").write_text(
        'schema_version: "1.0.0"\n'
        "declared_sources:\n"
        '  - path: "no/such/file.h5"\n'
        '    sha256: "'
        + "0" * 64
        + '"\n',
        encoding="utf-8",
    )
    monkeypatch.setenv("TEC_PLATFORM", "local")
    monkeypatch.setenv("TEC_WORKSPACE_ROOT", str(tmp_path))
    snap = load_configs(config_dir, phase=1)
    with pytest.raises(PreflightError) as excinfo:
        assert_declared_sources_exist(snap)
    assert "no/such/file.h5" in str(excinfo.value)


def test_declared_source_with_wrong_hash_is_a_failure(tmp_path, monkeypatch) -> None:
    config_dir = _write_config_tree(tmp_path)
    payload = tmp_path / "input.bin"
    payload.write_bytes(b"real bytes")
    (config_dir / "data.yaml").write_text(
        'schema_version: "1.0.0"\n'
        "declared_sources:\n"
        '  - path: "input.bin"\n'
        '    sha256: "'
        + "f" * 64
        + '"\n',
        encoding="utf-8",
    )
    monkeypatch.setenv("TEC_PLATFORM", "local")
    monkeypatch.setenv("TEC_WORKSPACE_ROOT", str(tmp_path))
    snap = load_configs(config_dir, phase=1)
    with pytest.raises(PreflightError) as excinfo:
        assert_declared_sources_exist(snap)
    assert "does not resolve" in str(excinfo.value)


def test_declared_sources_pass_when_empty_and_when_resolving(snapshot) -> None:
    assert_declared_sources_exist(snapshot)  # empty declaration set: nothing to fail


# --- W-8: platform resolution and the credential presence check -------------------------


def test_unknown_platform_raises_platform_error() -> None:
    """Negative control (plan step 4): TC-03c authorises exactly two platforms."""
    with pytest.raises(PlatformError) as excinfo:
        resolve_platform_roots({"TEC_PLATFORM": "colab"})
    assert "colab" in str(excinfo.value)


def test_colab_markers_are_refused_not_defaulted() -> None:
    """Colab is explicitly removed as a governed platform (TE 9.1; Vision 8.3)."""
    with pytest.raises(PlatformError):
        resolve_platform_roots({"COLAB_RELEASE_TAG": "release"})


def test_kaggle_and_local_resolve(tmp_path) -> None:
    label, roots = resolve_platform_roots({"KAGGLE_KERNEL_RUN_TYPE": "Interactive"})
    assert label == "kaggle" and roots["workspace"] == Path("/kaggle/working")
    label, roots = resolve_platform_roots({"TEC_WORKSPACE_ROOT": str(tmp_path)})
    assert label == "local" and roots["workspace"] == tmp_path


def test_resolve_returns_no_credential_value(monkeypatch, tmp_path) -> None:
    """R-14 negative control: a canary secret in the environment reaches no return
    value of the foundation resolve path."""
    canary = "CANARY-NOT-A-REAL-SECRET-12345"
    env = {
        "TEC_PLATFORM": "local",
        "TEC_WORKSPACE_ROOT": str(tmp_path),
        "MADRIGAL_API_KEY": canary,
    }
    label, roots = resolve_platform_roots(env)
    serialized = label + json.dumps({k: str(v) for k, v in roots.items()})
    assert canary not in serialized


def test_missing_credential_name_fails_early_by_name() -> None:
    """R-14: the failing message identifies the missing NAME; no value is touched."""
    with pytest.raises(PreflightError) as excinfo:
        assert_credential_names_present(["MADRIGAL_USER", "MADRIGAL_TOKEN"], {})
    message = str(excinfo.value)
    assert "MADRIGAL_USER" in message and "MADRIGAL_TOKEN" in message


def test_present_credential_names_pass_without_reading_values() -> None:
    class _NoValueRead(dict):
        def __getitem__(self, key):  # pragma: no cover - the point is it never runs
            raise AssertionError("a credential VALUE was read (R-14 violation)")

        def get(self, key, default=None):
            raise AssertionError("a credential VALUE was read (R-14 violation)")

    env = _NoValueRead()
    dict.__setitem__(env, "MADRIGAL_USER", "secret-value")
    assert_credential_names_present(["MADRIGAL_USER"], env)


def test_credential_name_map_is_declared_and_empty() -> None:
    """SD-02: the map is a shape without contents until configs name providers."""
    assert dict(CREDENTIAL_NAME_MAP) == {}


# --- W-4 / R-05 / R-06: seeding and the determinism record ------------------------------


def test_seed_everything_raises_when_tensorflow_already_initialised(
    snapshot, monkeypatch
) -> None:
    """R-05 negative control: import TensorFlow first, then call seed_everything."""
    monkeypatch.setitem(sys.modules, "tensorflow", type(sys)("tensorflow"))
    with pytest.raises(DeterminismError) as excinfo:
        seed_everything(snapshot, stage="test")
    assert "tensorflow" in str(excinfo.value)


def test_seed_everything_applies_the_frozen_development_seed(snapshot) -> None:
    record = seed_everything(snapshot, stage="test")
    assert record.seeds_applied["python"] == 42
    assert record.pythonhashseed == os.environ.get("PYTHONHASHSEED", "unset")
    assert "python.random" in record.probe_scope
    # An empty nondeterministic_ops is accompanied by an honest status, never
    # presented as proof (R-06): TF absent here means the assessment is partial.
    assert record.measurement_status in ("partial", "not-yet-measured")


def test_seed_everything_refuses_a_missing_or_tbd_seed(tmp_path, monkeypatch) -> None:
    config_dir = _write_config_tree(tmp_path)
    (config_dir / "seeds.yaml").write_text(
        'development: "TBD — freeze gate"\n', encoding="utf-8"
    )
    monkeypatch.setenv("TEC_PLATFORM", "local")
    monkeypatch.setenv("TEC_WORKSPACE_ROOT", str(tmp_path))
    snap = load_configs(config_dir, phase=1)
    with pytest.raises(SeedError) as excinfo:
        seed_everything(snap, stage="test")
    assert "seeds.yaml" in str(excinfo.value)


def test_declared_vs_observed_mismatches_surface_both_ways(
    tmp_path, monkeypatch
) -> None:
    """R-06 negative control: a declared op the probe does not observe surfaces as a
    mismatch rather than being silently reconciled."""
    config_dir = _write_config_tree(
        tmp_path,
    )
    (config_dir / "seeds.yaml").write_text(
        "development: 42\nfinal: [1337, 2024, 7]\nbootstrap: 20221201\n"
        "determinism:\n  expected_nondeterministic_ops: [tf.scatter_nd]\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("TEC_PLATFORM", "local")
    monkeypatch.setenv("TEC_WORKSPACE_ROOT", str(tmp_path))
    snap = load_configs(config_dir, phase=1)
    record = seed_everything(snap, stage="test")
    assert any(
        "declared-not-observed: tf.scatter_nd" in item
        for item in record.declared_vs_observed_mismatches
    )


def test_reexec_establishes_pythonhashseed_and_records_exactly_one_run(tmp_path) -> None:
    """R-05 negative control: invoke a stage-shaped script with PYTHONHASHSEED unset;
    assert `reexec_performed` is True, PYTHONHASHSEED=0, the sentinel is POPPED (a
    subprocess must not inherit it), and exactly one run is recorded."""
    script = tmp_path / "stage_script.py"
    out_file = tmp_path / "result.json"
    script.write_text(
        f"""
import json, os, sys
sys.path.insert(0, {str(REPO_ROOT)!r})
from src.data.config import ensure_process_determinism, reexec_performed, REEXEC_SENTINEL_ENV

def main():
    ensure_process_determinism(sys.argv)  # FIRST statement, before any framework import
    result = {{
        "reexec_performed": reexec_performed(),
        "pythonhashseed": os.environ.get("PYTHONHASHSEED"),
        "sentinel_still_in_env": REEXEC_SENTINEL_ENV in os.environ,
    }}
    with open({str(out_file)!r}, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(result) + "\\n")

if __name__ == "__main__":
    main()
""",
        encoding="utf-8",
    )
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONHASHSEED",)}
    env.pop(REEXEC_SENTINEL_ENV, None)
    subprocess.run([sys.executable, str(script)], env=env, timeout=120, check=False)
    # Windows os.execv spawns a replacement process; wait for the handshake file.
    deadline = time.time() + 60
    while time.time() < deadline and not out_file.exists():
        time.sleep(0.2)
    assert out_file.exists(), "the re-exec'd child never wrote its result"
    time.sleep(0.5)  # let the write complete fully
    lines = [ln for ln in out_file.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 1, f"exactly one run must be recorded, found {len(lines)}"
    result = json.loads(lines[0])
    assert result["reexec_performed"] is True
    assert result["pythonhashseed"] == "0"
    assert result["sentinel_still_in_env"] is False  # the pop is load-bearing (R-05)


def test_no_reexec_when_pythonhashseed_already_set(tmp_path) -> None:
    """The return-immediately path: already-set PYTHONHASHSEED, no sentinel, no re-exec."""
    script = tmp_path / "stage_script.py"
    out_file = tmp_path / "result.json"
    script.write_text(
        f"""
import json, os, sys
sys.path.insert(0, {str(REPO_ROOT)!r})
from src.data.config import ensure_process_determinism, reexec_performed

ensure_process_determinism(sys.argv)
with open({str(out_file)!r}, "w", encoding="utf-8") as handle:
    json.dump({{"reexec_performed": reexec_performed()}}, handle)
""",
        encoding="utf-8",
    )
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env.pop(REEXEC_SENTINEL_ENV, None)
    subprocess.run([sys.executable, str(script)], env=env, timeout=120, check=True)
    assert json.loads(out_file.read_text(encoding="utf-8"))["reexec_performed"] is False


# --- R-05 exit-code propagation (CR-2026-09-13-R05-WINDOWS-EXIT-CODE) --------------------
# Before this repair, os.execv on Windows detached the child and terminated the parent
# with exit code 0 unconditionally, so a genuine refusal reported success (observed
# 2026-09-13: `run_walking_skeleton.py` printed `preflight refusal: …` and exited 0).
# These controls pin the repaired contract on BOTH platforms: the caller of a
# re-exec'd stage script observes exactly the child's exit code.


def _reexec_exit_probe(tmp_path, exit_code: int) -> int:
    """Run a stage-shaped script that re-execs (PYTHONHASHSEED unset) and then exits
    with `exit_code`; return what the CALLER observes. The child also records
    `reexec_performed` so a probe that silently skipped the re-exec cannot pass."""
    script = tmp_path / "stage_script.py"
    out_file = tmp_path / "result.json"
    script.write_text(
        f"""
import json, os, sys
sys.path.insert(0, {str(REPO_ROOT)!r})
from src.data.config import ensure_process_determinism, reexec_performed

ensure_process_determinism(sys.argv)  # FIRST statement, before any framework import
with open({str(out_file)!r}, "w", encoding="utf-8") as handle:
    json.dump({{"reexec_performed": reexec_performed()}}, handle)
sys.exit({exit_code})
""",
        encoding="utf-8",
    )
    env = {k: v for k, v in os.environ.items() if k != "PYTHONHASHSEED"}
    env.pop(REEXEC_SENTINEL_ENV, None)
    proc = subprocess.run([sys.executable, str(script)], env=env, timeout=120, check=False)
    assert out_file.exists(), "the re-exec'd child never ran to its exit statement"
    assert json.loads(out_file.read_text(encoding="utf-8"))["reexec_performed"] is True
    return proc.returncode


def test_reexec_child_failure_exit_code_propagates_to_caller(tmp_path) -> None:
    """R-05 negative control, the load-bearing one: a refusal/failure in the re-exec'd
    child must reach the caller as a non-zero exit — it can NEVER become 0. On the
    pre-repair code this test fails with observed exit 0 (the Windows detach); it must
    fail again on any regression to detached spawning."""
    observed = _reexec_exit_probe(tmp_path, 7)
    assert observed == 7, (
        f"caller observed exit {observed} where the re-exec'd child exited 7; a "
        f"non-zero child exit converted to {observed} means integrity refusals report "
        f"as success (TE 13.2 / TE 9.2; CR-2026-09-13-R05-WINDOWS-EXIT-CODE)"
    )


def test_reexec_child_success_exit_code_is_zero(tmp_path) -> None:
    """The happy-path half: a successful re-exec'd child still yields exit 0 — the
    repair must not manufacture spurious non-zero exits."""
    observed = _reexec_exit_probe(tmp_path, 0)
    assert observed == 0, f"successful child reported exit {observed}, expected 0"


def test_r05_platform_split_is_exact_in_source() -> None:
    """AST control on the mechanism itself: the `os.name == "nt"` branch spawns via
    `subprocess.run` and raises `SystemExit` with its return code; the POSIX path still
    calls `os.execv`; and there is no third relaunch path. Pins the repaired shape so a
    later edit cannot silently reintroduce the detach or drop the POSIX exec."""
    import ast as _ast

    source = (REPO_ROOT / "src" / "data" / "config.py").read_text(encoding="utf-8")
    tree = _ast.parse(source)
    func = next(
        node
        for node in _ast.walk(tree)
        if isinstance(node, _ast.FunctionDef) and node.name == "ensure_process_determinism"
    )
    dumped = _ast.dump(func)
    # Windows branch: guarded on os.name == "nt", spawn-and-wait, SystemExit(rc).
    assert "attr='name'" in dumped and "'nt'" in dumped, (
        "the os.name == 'nt' platform guard is gone from ensure_process_determinism"
    )
    calls = {
        f"{_ast.dump(node.func)}"
        for node in _ast.walk(func)
        if isinstance(node, _ast.Call)
    }
    assert any("attr='run'" in c and "id='subprocess'" in c for c in calls), (
        "the Windows spawn-and-wait (subprocess.run) is gone"
    )
    assert any("attr='execv'" in c and "id='os'" in c for c in calls), (
        "the POSIX os.execv relaunch is gone"
    )
    raises_systemexit = any(
        isinstance(node, _ast.Raise)
        and isinstance(node.exc, _ast.Call)
        and isinstance(node.exc.func, _ast.Name)
        and node.exc.func.id == "SystemExit"
        for node in _ast.walk(func)
    )
    assert raises_systemexit, (
        "the Windows branch no longer exits the parent with the child's return code"
    )
    # No shell anywhere in the relaunch (S603/S606 posture preserved).
    func_source = _ast.get_source_segment(source, func) or ""
    assert func_source, "could not extract ensure_process_determinism's source segment"
    assert "shell=True" not in func_source, "relaunch must never use a shell"


# --- W-5 / REQ-ENG-10: the eight-item environment lock ----------------------------------


def test_environment_lock_captures_eight_of_eight(snapshot, tmp_path) -> None:
    """Happy path + the plan's 8/8 completeness control."""
    (tmp_path / "requirements.txt").write_text("numpy==1.26.4\n", encoding="utf-8")
    determinism = seed_everything(snapshot, stage="test")
    record = capture_environment_lock(
        snapshot,
        determinism,
        requirements_path=tmp_path / "requirements.txt",
        code_commit="0" * 40,  # explicit, as a Kaggle session would pass it
    )
    assert_lock_complete(record)  # 8/8 populated or raise
    assert record.requirements_hash and record.pip_freeze
    assert record.config_hashes == snapshot.hashes
    assert record.platform == "local"
    lock_hash = environment_lock_hash(record)
    assert len(lock_hash) == 64 and environment_lock_hash(record) == lock_hash


def test_missing_requirements_file_is_an_integrity_failure(snapshot, tmp_path) -> None:
    determinism = seed_everything(snapshot, stage="test")
    with pytest.raises(IntegrityError) as excinfo:
        capture_environment_lock(
            snapshot,
            determinism,
            requirements_path=tmp_path / "absent-requirements.txt",
            code_commit="0" * 40,
        )
    assert "requirements" in str(excinfo.value)


def test_incomplete_lock_fails_rather_than_completing_silently(snapshot, tmp_path) -> None:
    """REQ-ENG-10 negative control: an unpopulated field is a named failure."""
    (tmp_path / "requirements.txt").write_text("numpy==1.26.4\n", encoding="utf-8")
    determinism = seed_everything(snapshot, stage="test")
    record = capture_environment_lock(
        snapshot,
        determinism,
        requirements_path=tmp_path / "requirements.txt",
        code_commit="0" * 40,
    )
    from dataclasses import replace

    broken = replace(record, code_commit="")
    with pytest.raises(IntegrityError) as excinfo:
        assert_lock_complete(broken)
    assert "code_commit" in str(excinfo.value)


# --- R-15 / R-17: static controls over foundation's own modules -------------------------


def test_no_foundation_module_constructs_a_restricted_root_path() -> None:
    """R-15 negative control: the restricted-root literal appears in NO foundation
    module. Only `src/data/locked_test.py` (governance-guards') may reach it; this scan
    names the boundary without constructing a path into it.

    The needle is DERIVED from the chokepoint's exported constant rather than held (or
    assembled) here: the earlier `"locked_test" + "_restricted"` assembly dodged the
    one-door TEXTUAL scan, and the AST constant-folding scan that closed DISC-2's
    named evasion at stage 3.5 caught it on first run — exactly the +-concatenation
    Q2 = B was chosen to close (runtime assembly remains statically unclosable and is
    disclosed where that scan lives).
    Deriving it at run time keeps this module off R-28's exemption list (membership is
    ruled at exactly seven) while R-15's control stays intact. This is not the
    circularity R-28 row 1 rejects: `locked_test.py` is not the module under test
    here, and no path is resolved from the derived name."""
    from src.data.locked_test import RESTRICTED_ROOT

    literal = RESTRICTED_ROOT.rsplit("/", 1)[-1]
    for module in FOUNDATION_MODULES:
        source = module.read_text(encoding="utf-8")
        assert literal not in source, (
            f"{module.name} mentions the restricted root; no foundation code path may "
            f"construct a path into it (R-15, SD-05, D-15)"
        )


def test_every_foundation_module_has_a_purpose_inputs_rerun_docstring() -> None:
    """R-17: purpose, inputs, and re-run behaviour, in every module this unit owns."""
    import ast

    for module in FOUNDATION_MODULES:
        tree = ast.parse(module.read_text(encoding="utf-8"))
        docstring = ast.get_docstring(tree) or ""
        lowered = docstring.lower()
        assert "purpose" in lowered, f"{module.name}: docstring lacks a Purpose section"
        assert "inputs" in lowered, f"{module.name}: docstring lacks an Inputs section"
        assert "re-run" in lowered, f"{module.name}: docstring lacks re-run behaviour"


# --- R-01: the enumeration census over the units' functional-design artifacts ------------
#
# R-01's mandated control, quoted from its own text:
#
#   "**Negative control -- the enumeration itself, added 2026-08-28 per Recommendation 8.**
#    A test **re-derives** the distinct project-defined `*Error` names raised across the
#    twelve units' `functional-design` artifacts and **fails when a name is neither in
#    R-01's fifteen nor disclosed by its raising unit under the any-future clause**. This
#    is the control that catches the failure R-01 suffered twice: a subclass added later
#    with nobody updating the enumeration. It asserts a **reconciliation**, not a number,
#    so it does not itself go stale when the census legitimately grows."
#
# Two design consequences follow from that last sentence, and both are deliberate.
#
# 1. NO NUMERAL IS ASSERTED anywhere below. R-01 went stale on its own count twice (six ->
#    fourteen, fourteen -> fifteen) and its standing obligation is to "re-run the
#    derivation and print its output rather than trusting 'fifteen'". The unit directories
#    are DERIVED (a `construction/` child is a unit iff it holds a `functional-design/`
#    subdirectory, which excludes the stage directories `code-generation`,
#    `functional-design`, `nfr-design` and `nfr-requirements`); the Python builtins to
#    subtract are DERIVED from `builtins`; the any-future disclosures are DERIVED from the
#    artifacts. Only R-01's fifteen is a fixed list, because it is an authored contract
#    rather than a census output -- it is the thing being reconciled AGAINST -- and
#    `test_r01s_fifteen_match_the_declaration_site` pins it to `src/data/config.py` so the
#    two cannot drift apart silently.
#
# 2. DISCLOSURE IS READ WORKSPACE-WIDE, not per raising unit. R-01's control sentence says
#    "disclosed by its raising unit", but foundation's own § Assumptions records the
#    per-raising-unit declaration obligation as an OPEN cross-unit item that this unit
#    "cannot do for them" -- so asserting it here would make foundation's census red on
#    another unit's unfinished work, conflating two distinct failures. The census asserts
#    the reconciliation it owns (is the name disclosed under the clause anywhere in the
#    artifact set?); the per-unit declaration obligation stays where foundation recorded
#    it, as an open item on the raising units.
#
# The disclosure scan is LINE-SCOPED: a name counts as disclosed when it shares a line
# with any-future-clause language. That bound can only ever UNDER-detect disclosure, so
# its failure mode is a false alarm that sends a reader to the artifact -- never a false
# pass that lets an undisclosed subclass through. That is the safe direction for a guard.

#: The construction record root the census walks. Unit directory names are derived from it.
_CONSTRUCTION_ROOT = (
    REPO_ROOT
    / "aidlc"
    / "spaces"
    / "default"
    / "intents"
    / "260813-tec-hourly-forecast"
    / "construction"
)

#: R-01's FIFTEEN, quoted from R-01's Rule paragraph in `foundation`'s `business-rules.md`:
#: the six `foundation` raises, then the nine "raised by other units and derive from the
#: same base". `PartitionError` is the fifteenth, promoted 2026-08-28 on the project
#: decision owner's ruling on `GOV-2026-08-28-FD-01` Recommendation 8.
R01_ENUMERATION = frozenset(
    {
        # foundation's own six
        "ConfigError",
        "PreflightError",
        "PlatformError",
        "DeterminismError",
        "ReleaseError",
        "RegistryError",
        # raised by other units, same base
        "PhaseBoundaryError",
        "LockedTestError",
        "LeakageError",
        "AlignmentError",
        "SeedError",
        "FairnessError",
        "BootstrapError",
        "RegimeError",
        "PartitionError",
    }
)

#: Derived, never listed: whatever the running interpreter calls a builtin `*Error`.
_PYTHON_BUILTIN_ERRORS = frozenset(
    name for name in dir(builtins) if name.endswith("Error")
)

_ERROR_NAME_RE = re.compile(r"\b([A-Z][A-Za-z0-9]*Error)\b")

#: The ways the artifact set spells R-01's "any future integrity-related exception" clause.
_ANY_FUTURE_MARKERS = (
    re.compile(r"any future integrity-related exception", re.IGNORECASE),
    re.compile(r"any[- ]future clause", re.IGNORECASE),
    re.compile(r"rid(?:e|es|ing)\s+R-01", re.IGNORECASE),
    re.compile(r"R-01['’]?s?\s+(?:named\s+)?fifteen", re.IGNORECASE),
)


class _Census(NamedTuple):
    """One run of R-01's enumeration census over a `construction/` tree."""

    units: tuple[str, ...]
    artifacts: int
    raised: dict[str, set[str]]
    disclosed: dict[str, set[str]]

    def undisclosed(self) -> list[str]:
        """Derived names in NEITHER R-01's fifteen NOR the any-future disclosures."""
        return sorted(
            name
            for name in self.raised
            if name not in R01_ENUMERATION and name not in self.disclosed
        )

    def unreached(self) -> list[str]:
        """R-01's fifteen that the census did not reach (the anti-vacuity direction)."""
        return sorted(R01_ENUMERATION - set(self.raised))


def _derive_unit_dirs(construction_root: Path) -> list[Path]:
    """A `construction/` child is a UNIT iff it holds a `functional-design/` directory.

    Derived rather than listed, so a renamed, added or removed unit is picked up instead
    of silently dropping out of the census.
    """
    return sorted(
        child
        for child in construction_root.iterdir()
        if child.is_dir() and (child / "functional-design").is_dir()
    )


def _run_enumeration_census(construction_root: Path) -> _Census:
    """Re-derive every project-defined `*Error` name across the units' artifacts.

    Returns the raised names (name -> units mentioning it) and the subset disclosed on a
    line carrying any-future-clause language (name -> units disclosing it).
    """
    raised: dict[str, set[str]] = {}
    disclosed: dict[str, set[str]] = {}
    unit_dirs = _derive_unit_dirs(construction_root)
    artifacts = 0

    for unit_dir in unit_dirs:
        for artifact in sorted((unit_dir / "functional-design").glob("*.md")):
            artifacts += 1
            for line in artifact.read_text(encoding="utf-8").splitlines():
                names = {match.group(1) for match in _ERROR_NAME_RE.finditer(line)}
                names -= _PYTHON_BUILTIN_ERRORS
                names.discard("IntegrityError")  # the base, not a subclass
                if not names:
                    continue
                is_disclosure = any(marker.search(line) for marker in _ANY_FUTURE_MARKERS)
                for name in names:
                    raised.setdefault(name, set()).add(unit_dir.name)
                    if is_disclosure:
                        disclosed.setdefault(name, set()).add(unit_dir.name)

    return _Census(
        units=tuple(unit_dir.name for unit_dir in unit_dirs),
        artifacts=artifacts,
        raised=raised,
        disclosed=disclosed,
    )


def _format_census(census: _Census) -> str:
    """Render the derivation R-01's standing obligation requires printed, not trusted."""
    subclasses = sorted(census.raised)
    enumerated = sorted(name for name in subclasses if name in R01_ENUMERATION)
    riding = sorted(
        name for name in subclasses if name not in R01_ENUMERATION and name in census.disclosed
    )
    lines = [
        "R-01 enumeration census -- derived, not carried",
        f"  units derived from construction/*/functional-design/ : {len(census.units)}",
    ]
    lines += [f"      {name}" for name in census.units]
    lines += [
        f"  artifacts scanned .................................. : {census.artifacts}",
        f"  distinct project-defined SUBCLASS names ............ : {len(subclasses)}",
        f"    of which named in R-01's enumeration ............. : {len(enumerated)}",
        f"    of which disclosed under the any-future clause ... : {len(riding)}",
        "",
        f"  R-01's enumeration ({len(R01_ENUMERATION)}):",
    ]
    for name in sorted(R01_ENUMERATION):
        reached = "" if name in census.raised else "   <-- NOT reached by the census"
        lines.append(f"      {name}{reached}")
    lines += ["", "  disclosed under the any-future clause:"]
    for name in riding:
        lines.append(f"      {name}  [{', '.join(sorted(census.disclosed[name]))}]")
    lines += [
        "",
        "  SET DIFFERENCE, direction 1 -- DERIVED but in NEITHER list:",
    ]
    undisclosed = census.undisclosed()
    if undisclosed:
        lines += [
            f"      {name}  raised in: {', '.join(sorted(census.raised[name]))}"
            for name in undisclosed
        ]
    else:
        lines.append("      (none)")
    lines += ["", "  SET DIFFERENCE, direction 2 -- in R-01's enumeration but NOT reached:"]
    unreached = census.unreached()
    lines += [f"      {name}" for name in unreached] if unreached else ["      (none)"]
    return "\n".join(lines)


def test_r01_enumeration_census_reconciles_every_derived_error_name() -> None:
    """R-01's mandated control: no `*Error` name is raised across the units' artifacts
    that is neither in R-01's fifteen nor disclosed under R-01's any-future clause.

    This is the control that catches the failure R-01 suffered twice -- a subclass added
    later with nobody updating the enumeration -- and it asserts a reconciliation rather
    than a count, so it survives the census legitimately growing. The derivation is
    PRINTED on every run, per R-01's standing obligation that whoever revisits the
    hierarchy "re-runs the derivation above and prints its output".
    """
    census = _run_enumeration_census(_CONSTRUCTION_ROOT)
    report = _format_census(census)
    print("\n" + report)

    undisclosed = census.undisclosed()
    assert not undisclosed, (
        f"{_CONSTRUCTION_ROOT}: R-01 reconciliation FAILED. These project-defined "
        f"`*Error` names are raised in the units' functional-design artifacts but are "
        f"neither in R-01's enumeration nor disclosed under its any-future clause: "
        f"{', '.join(undisclosed)}. Each must be added to R-01's enumeration or "
        f"disclosed by its raising unit as an `IntegrityError` subclass riding the "
        f"any-future clause -- otherwise R-10's stage-entry catch lets it exit with no "
        f"`aborted` registry row (NFR-AUD-01).\n\n{report}"
    )


def test_the_census_reaches_every_name_in_r01s_enumeration() -> None:
    """Anti-vacuity guard, and the second direction of the set difference.

    A census whose walk silently matched nothing would pass the reconciliation above by
    finding no names at all. Every one of R-01's fifteen is raised somewhere in the
    artifact set, so requiring the census to reach all of them detects a broken walk --
    a moved record root, a renamed `functional-design/` directory, an artifact extension
    change -- without asserting any numeral.
    """
    census = _run_enumeration_census(_CONSTRUCTION_ROOT)
    unreached = census.unreached()
    assert not unreached, (
        f"the census reached {len(census.units)} unit(s) and {census.artifacts} "
        f"artifact(s) but never saw {', '.join(unreached)} -- every name in R-01's "
        f"enumeration is raised in the artifact set, so the walk is broken rather than "
        f"the enumeration.\n\n{_format_census(census)}"
    )


def test_r01s_fifteen_match_the_declaration_site() -> None:
    """R-01's enumeration and its declaration site must not drift apart.

    `src/data/config.py` declares `IntegrityError` and, above the
    "riding R-01's any-future clause" marker, exactly the subclasses R-01 enumerates.
    Pinning the two together is what keeps `R01_ENUMERATION` above an authored contract
    rather than a hand-copied list that can go stale a fourth time.
    """
    import ast

    source = (REPO_ROOT / "src" / "data" / "config.py").read_text(encoding="utf-8")
    marker = "# --- riding R-01's any-future clause"
    assert marker in source, (
        "src/data/config.py lost the any-future-clause section marker; the boundary "
        "between R-01's enumeration and the riders is no longer expressed in the "
        "declaration site"
    )
    marker_lineno = source[: source.index(marker)].count("\n") + 1

    declared = {
        node.name
        for node in ast.parse(source).body
        if isinstance(node, ast.ClassDef)
        and node.lineno < marker_lineno
        and any(
            isinstance(base, ast.Name) and base.id == "IntegrityError"
            for base in node.bases
        )
    }
    assert declared == set(R01_ENUMERATION), (
        "R-01's enumeration and src/data/config.py disagree. Declared above the "
        f"any-future marker but not enumerated: {sorted(declared - R01_ENUMERATION)}; "
        f"enumerated but not declared above the marker: "
        f"{sorted(set(R01_ENUMERATION) - declared)}"
    )


def _write_synthetic_unit(root: Path, unit: str, body: str) -> None:
    """Build one `<unit>/functional-design/business-rules.md` under a synthetic root."""
    artifact_dir = root / unit / "functional-design"
    artifact_dir.mkdir(parents=True)
    (artifact_dir / "business-rules.md").write_text(body, encoding="utf-8")


def test_census_catches_an_undisclosed_name(tmp_path) -> None:
    """NEGATIVE CONTROL: the census FAILS on a subclass nobody disclosed.

    This is the control that proves R-01's census does its job rather than that a clean
    workspace happens to pass. A synthetic unit raises `WidgetError` with no any-future
    disclosure anywhere; the reconciliation must name it. Without this, a census that
    returned the empty set for every input would pass the live assertion above.
    """
    construction = tmp_path / "construction"
    _write_synthetic_unit(
        construction,
        "synthetic-unit",
        "RAISES `WidgetError` when the widget contract is violated.\n",
    )

    census = _run_enumeration_census(construction)

    assert census.units == ("synthetic-unit",)
    assert "WidgetError" in census.raised
    assert census.undisclosed() == ["WidgetError"], (
        "the census did not flag an undisclosed subclass -- R-01's mandated control is "
        f"inert. Census said: {_format_census(census)}"
    )


def test_census_accepts_a_name_disclosed_under_the_any_future_clause(tmp_path) -> None:
    """NEGATIVE CONTROL, the other way: a disclosed name must NOT be flagged.

    A census that flagged everything would pass the test above for the wrong reason. The
    same synthetic `WidgetError` is disclosed in R-01's own wording; it must drop out of
    the undisclosed set while an adjacent undisclosed `GadgetError` stays in it, which
    also proves the disclosure is attributed per name rather than blanket-applied to the
    artifact.

    The disclosure sentence is one LINE, not one paragraph: the scan is line-scoped, and
    writing the fixture any other way would assert a proximity rule the census does not
    implement. The wording is `external-products`' real disclosure of
    `FeatureAvailabilityError`, with the name swapped.
    """
    construction = tmp_path / "construction"
    _write_synthetic_unit(
        construction,
        "synthetic-unit",
        "`WidgetError` derives from R-01's `IntegrityError` base under that rule's "
        '"any future integrity-related exception" clause and is not claimed as one of '
        "R-01's named fifteen.\n"
        "RAISES `GadgetError` when the gadget contract is violated.\n",
    )

    census = _run_enumeration_census(construction)

    assert census.disclosed.get("WidgetError") == {"synthetic-unit"}
    assert census.undisclosed() == ["GadgetError"], (
        "disclosure is not being attributed per name -- a disclosure on one line must "
        f"not cover an undisclosed name elsewhere. Census said: {_format_census(census)}"
    )


def test_census_never_flags_a_name_in_r01s_enumeration(tmp_path) -> None:
    """An enumerated name needs no any-future disclosure; it IS the enumeration."""
    construction = tmp_path / "construction"
    _write_synthetic_unit(
        construction, "synthetic-unit", "RAISES `SeedError` on a defaulted seed.\n"
    )

    census = _run_enumeration_census(construction)

    assert "SeedError" in census.raised
    assert census.undisclosed() == []


def test_census_unit_derivation_skips_a_directory_without_functional_design(
    tmp_path,
) -> None:
    """EDGE CASE: the twelve unit names are derived, so stage directories drop out.

    `construction/` also holds `code-generation`, `functional-design`, `nfr-design` and
    `nfr-requirements`, which are stage directories rather than units and hold no
    `functional-design/` child. Hardcoding twelve names would have hidden a renamed unit;
    deriving them means only the shape of a unit directory decides membership.
    """
    construction = tmp_path / "construction"
    _write_synthetic_unit(
        construction, "real-unit", "RAISES `WidgetError` on a violated contract.\n"
    )
    stage_dir = construction / "a-stage-directory"
    stage_dir.mkdir()
    (stage_dir / "some-stage-artifact.md").write_text(
        "RAISES `NeverCountedError` -- this file is not under a unit.\n", encoding="utf-8"
    )

    census = _run_enumeration_census(construction)

    assert census.units == ("real-unit",)
    assert "NeverCountedError" not in census.raised
    assert census.artifacts == 1


def test_python_builtin_errors_are_excluded_from_the_census(tmp_path) -> None:
    """EDGE CASE: `TypeError` and `NotImplementedError` occur in the real artifacts.

    They are not project-defined, so they must never reach the reconciliation. The
    exclusion set is derived from `builtins` rather than listed, so a builtin added by a
    later Python does not need this test changed.
    """
    construction = tmp_path / "construction"
    _write_synthetic_unit(
        construction,
        "synthetic-unit",
        "RAISES `TypeError` and `NotImplementedError`, neither project-defined.\n",
    )

    census = _run_enumeration_census(construction)

    assert census.raised == {}
    assert census.undisclosed() == []
