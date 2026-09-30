"""D-83 revision 7 §W7 W-4 and W-5: admission by identity, `environment_id`, Kaggle dormancy.

Purpose: prove each W-4 / W-5 control refuses what D-83 says it refuses (negative controls)
and admits what it says it admits. Inputs: synthetic identity files and captures in
`tmp_path`; no network, no December content. Re-run behaviour: pure; nothing persists.
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import pytest

from src.data import admission
from src.data.config import (
    IntegrityError,
    PlatformError,
    RunRecord,
    assert_platform_not_dormant,
    environment_lock_hash,
    resolve_environment_id,
    resolve_platform_roots,
)

PIP = "numpy==2.1.3\npip==24.2\nsetuptools==84.0.0\nwheel==0.48.0\n"
CONDA = "https://conda.anaconda.org/conda-forge/win-64/python-3.11.9-hb12b558_2.conda#abc123\n"


def _identity(tmp_path: Path, env_id: str = "tec-thesis-311", **extra) -> Path:
    body = {
        "environment_id": env_id,
        "pip": {"numpy": "2.1.3", "pip": "24.2", "setuptools": "84.0.0", "wheel": "0.48.0"},
        "pip_exceptions": [],
        "conda": [CONDA.strip()],
        **extra,
    }
    path = admission.identity_path(tmp_path, env_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body), encoding="utf-8")
    return path


def _lock(**kw) -> RunRecord:
    base = dict(
        requirements_hash="r",
        pip_freeze=PIP,
        runtime_versions={"python": "3.11.9"},
        code_commit="aaaa",
        config_hashes={"data.yaml": "d"},
        input_versions=[],
        platform="local",
        nondeterministic_ops=[],
        environment_id="tec-thesis-311",
    )
    base.update(kw)
    return RunRecord(**base)


# --- admission key -------------------------------------------------------------------


def test_conforming_environment_is_admitted_with_the_identity_file_hash(tmp_path) -> None:
    import hashlib

    path = _identity(tmp_path)
    key = admission.admission_key(
        tmp_path, "tec-thesis-311", pip_freeze_all=PIP, conda_explicit=CONDA
    )
    assert key == hashlib.sha256(path.read_bytes()).hexdigest()


def test_new_commit_run_in_admitted_environment_passes(tmp_path) -> None:
    """The key does not depend on the run: two runs on different commits and configs in
    the admitted environment carry the same key (the per-run hashes differ)."""
    _identity(tmp_path)
    key_a = admission.admission_key(tmp_path, "tec-thesis-311", pip_freeze_all=PIP, conda_explicit=CONDA)
    key_b = admission.admission_key(tmp_path, "tec-thesis-311", pip_freeze_all=PIP, conda_explicit=CONDA)
    assert key_a == key_b
    assert environment_lock_hash(_lock(code_commit="aaaa")) != environment_lock_hash(
        _lock(code_commit="bbbb")
    )


def test_ci_environment_is_never_admitted(tmp_path, monkeypatch) -> None:
    with pytest.raises(PlatformError):
        resolve_platform_roots({"GITHUB_ACTIONS": "true"})
    with pytest.raises(PlatformError):
        resolve_environment_id({"TEC_ENVIRONMENT_ID": "ci"})
    with pytest.raises(IntegrityError):
        admission.admission_key(tmp_path, "ci", pip_freeze_all=PIP)


def test_undeclared_environment_is_refused(tmp_path) -> None:
    assert resolve_environment_id({}) == "undeclared"
    with pytest.raises(IntegrityError):
        admission.admission_key(tmp_path, "undeclared", pip_freeze_all=PIP)


def test_missing_identity_file_is_refused(tmp_path) -> None:
    with pytest.raises(IntegrityError) as exc:
        admission.admission_key(tmp_path, "b01_iri", pip_freeze_all=PIP)
    assert "identity file" in str(exc.value)


@pytest.mark.parametrize(
    "pip_text",
    [
        PIP.replace("numpy==2.1.3", "numpy==2.1.4"),  # version drift
        PIP + "extra==1.0\n",  # a package outside the identity
        PIP.replace("pip==24.2", "pip @ file:///C:/pip.whl"),  # unlisted direct reference
        PIP.replace("wheel==0.48.0\n", ""),  # missing (the --all capture matters)
    ],
)
def test_pip_nonconformance_is_refused(tmp_path, pip_text) -> None:
    _identity(tmp_path)
    with pytest.raises(IntegrityError) as exc:
        admission.admission_key(tmp_path, "tec-thesis-311", pip_freeze_all=pip_text, conda_explicit=CONDA)
    assert "pin conformance" in str(exc.value)


def test_listed_pip_direct_reference_exception_is_admitted(tmp_path) -> None:
    _identity(tmp_path, pip_exceptions=["pip"])
    admission.admission_key(
        tmp_path,
        "tec-thesis-311",
        pip_freeze_all=PIP.replace("pip==24.2", "pip @ file:///C:/pip.whl"),
        conda_explicit=CONDA,
    )


def test_conda_md5_or_build_drift_is_refused(tmp_path) -> None:
    _identity(tmp_path)
    for text in (CONDA.replace("abc123", "def456"), CONDA.replace("hb12b558_2", "hb00fc5c_0")):
        with pytest.raises(IntegrityError):
            admission.admission_key(tmp_path, "tec-thesis-311", pip_freeze_all=PIP, conda_explicit=text)


# --- environment_id in both representations -----------------------------------------


def test_lock_hash_is_derived_from_every_runrecord_field() -> None:
    names = {f.name for f in dataclasses.fields(RunRecord)}
    assert "environment_id" in names
    base = _lock()
    for field in names:
        value = getattr(base, field)
        changed = (
            {**value, "x": "y"} if isinstance(value, dict)
            else [*value, "x"] if isinstance(value, list)
            else f"{value}-changed"
        )
        assert environment_lock_hash(dataclasses.replace(base, **{field: changed})) != environment_lock_hash(base), field


def test_locks_differing_only_in_environment_id_hash_differently() -> None:
    assert environment_lock_hash(_lock(environment_id="tec-thesis-311")) != environment_lock_hash(
        _lock(environment_id="g07-clean-run")
    )


def test_environment_id_representations_must_agree() -> None:
    admission.assert_environment_id_agreement({"environment_id": "tec-thesis-311"}, _lock())
    with pytest.raises(IntegrityError):
        admission.assert_environment_id_agreement({"environment_id": "b01_iri"}, _lock())


@pytest.mark.parametrize("row", [{"run_id": "r"}, {"run_id": "r", "environment_id": ""}, {"run_id": "r", "environment_id": "undeclared"}])
def test_registry_row_without_environment_id_fails_g05_preflight(row) -> None:
    with pytest.raises(IntegrityError):
        admission.assert_row_declares_environment(row)


def test_registry_writes_environment_id_extension(tmp_path) -> None:
    from src.data.experiment_registry import EXTENSION_FIELDS

    assert "environment_id" in EXTENSION_FIELDS


# --- W-5: Kaggle is dormant, including in code ---------------------------------------


def test_governed_run_on_kaggle_is_refused() -> None:
    label, _ = resolve_platform_roots({"TEC_PLATFORM": "kaggle"})
    with pytest.raises(PlatformError) as exc:
        assert_platform_not_dormant(label)
    assert "dormant" in str(exc.value)
    label, _ = resolve_platform_roots({"KAGGLE_KERNEL_RUN_TYPE": "Interactive"})
    with pytest.raises(PlatformError):
        assert_platform_not_dormant(label)
    assert_platform_not_dormant("local")


def test_load_configs_refuses_kaggle(monkeypatch) -> None:
    from src.data.config import load_configs

    monkeypatch.setenv("TEC_PLATFORM", "kaggle")
    with pytest.raises(PlatformError) as exc:
        load_configs(Path("configs"), phase=1)
    assert "dormant" in str(exc.value)


# --- D-83 §R4-7 item 3: the G-05 access preflight --------------------------------------


def _alog(tmp_path, *rows):
    path = tmp_path / "log.jsonl"
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return path


def test_no_pre_g05_audit_passes_before_the_cutoff_exists(tmp_path) -> None:
    with pytest.raises(IntegrityError):
        admission.g05_access_preflight(_alog(tmp_path), cutoff_utc=None)


def test_pre_cutoff_row_fails_even_if_its_environment_was_later_admitted(tmp_path) -> None:
    row = {"run_id": "r", "logged_at_utc": "2026-09-01T00:00:00+00:00", "environment_id": "tec-thesis-311"}
    with pytest.raises(IntegrityError):
        admission.g05_access_preflight(_alog(tmp_path, row), cutoff_utc="2026-10-01T00:00:00+00:00")


@pytest.mark.parametrize("logged", [None, "not-a-time", "2026-10-05T00:00:00"])
def test_missing_unparseable_or_naive_logged_at_fails(tmp_path, logged) -> None:
    row = {"run_id": "r", "retrieved_at_utc": "2026-12-01T00:00:00+00:00"}
    if logged is not None:
        row["logged_at_utc"] = logged
    with pytest.raises(IntegrityError):
        admission.g05_access_preflight(_alog(tmp_path, row), cutoff_utc="2026-10-01T00:00:00+00:00")


def test_post_cutoff_rows_pass(tmp_path) -> None:
    row = {"run_id": "r", "logged_at_utc": "2026-10-02T00:00:00+00:00"}
    assert admission.g05_access_preflight(_alog(tmp_path, row), cutoff_utc="2026-10-01T00:00:00Z") == 1


# --- GOV-2026-09-30-PV-09 remediation negative controls --------------------------------


def test_pep503_names_compare_equal(tmp_path) -> None:
    """DATA-08: `Foo_Bar==1` installed conforms to an identity pinning `foo-bar`."""
    path = _identity(tmp_path)
    body = json.loads(path.read_text(encoding="utf-8"))
    body["pip"]["foo-bar"] = "1.0"
    path.write_text(json.dumps(body), encoding="utf-8")
    admission.admission_key(
        tmp_path, "tec-thesis-311", pip_freeze_all=PIP + "Foo_Bar==1.0\n", conda_explicit=CONDA
    )


def test_crlf_checkout_does_not_change_the_admission_key(tmp_path) -> None:
    """DATA-01: the key is taken over canonical LF bytes."""
    path = _identity(tmp_path)
    lf = json.dumps(json.loads(path.read_text(encoding="utf-8")), indent=1)
    path.write_bytes(lf.encode("utf-8"))
    key_lf = admission.admission_key(tmp_path, "tec-thesis-311", pip_freeze_all=PIP, conda_explicit=CONDA)
    path.write_bytes(lf.replace("\n", "\r\n").encode("utf-8"))
    key_crlf = admission.admission_key(tmp_path, "tec-thesis-311", pip_freeze_all=PIP, conda_explicit=CONDA)
    assert key_lf == key_crlf


def test_missing_access_log_fails_g05_preflight(tmp_path) -> None:
    """DATA-10: an absent governed log is missing evidence, not an empty pass."""
    with pytest.raises(IntegrityError):
        admission.g05_access_preflight(tmp_path / "absent.jsonl", cutoff_utc="2026-10-01T00:00:00Z")


@pytest.mark.parametrize("cutoff", ["2026-10-01T00:00:00", "not-a-time"])
def test_naive_or_unparseable_cutoff_is_refused_by_name(tmp_path, cutoff) -> None:
    """DATA-10: never a TypeError from comparing naive with aware datetimes."""
    row = {"run_id": "r", "logged_at_utc": "2026-10-02T00:00:00+00:00"}
    with pytest.raises(IntegrityError):
        admission.g05_access_preflight(_alog(tmp_path, row), cutoff_utc=cutoff)


def test_legacy_lock_without_environment_id_is_refused_by_name() -> None:
    """DATA-03: a pre-W-4 lock is refused, never upcast to `undeclared`."""
    from src.data.fixture_gate import lock_items

    legacy = {f.name: getattr(_lock(), f.name) for f in dataclasses.fields(RunRecord)}
    legacy.pop("environment_id")
    with pytest.raises(IntegrityError) as exc:
        lock_items(legacy)
    assert "item 29" in str(exc.value)


def test_registry_write_refuses_an_unnamed_environment_id(tmp_path) -> None:
    """DATA-02: the production registry write path refuses an unknown environment_id."""
    from src.data import experiment_registry as reg

    with pytest.raises(reg.RegistryError) as exc:
        reg._validate_row(
            tmp_path / "r.jsonl", {"status": "started", "environment_id": "kaggle-box"},
            phase=1, writer_role="stage",
        )
    assert "environment_id" in str(exc.value)


def test_kaggle_marker_with_declared_local_label_is_refused(monkeypatch) -> None:
    """BENCH-05: TEC_PLATFORM=local on a Kaggle host does not bypass dormancy."""
    from src.data.config import load_configs

    monkeypatch.setenv("TEC_PLATFORM", "local")
    monkeypatch.setenv("KAGGLE_KERNEL_RUN_TYPE", "Batch")
    with pytest.raises(PlatformError) as exc:
        load_configs(Path("configs"), phase=1)
    assert "dormant" in str(exc.value)


def test_write_once_durable_is_complete_or_absent(tmp_path, monkeypatch) -> None:
    """BENCH-02: a failure before the link leaves no file at the final name."""
    import os

    from src.data.release import write_once_durable

    target = tmp_path / "receipt.json"

    def boom(*a, **k):
        raise OSError("killed before link")

    monkeypatch.setattr(os, "link", boom)
    with pytest.raises(OSError):
        write_once_durable(target, "{}\n")
    assert not target.exists()
    assert not list(tmp_path.glob("*.partial"))
    monkeypatch.undo()
    write_once_durable(target, "{}\n")
    assert target.read_bytes() == b"{}\n"
    with pytest.raises(FileExistsError):
        write_once_durable(target, "{}\n")
