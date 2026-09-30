"""Environment admission by identity (D-83 revision 7 §A7 items 4 and 14; §W7 W-4).

Purpose
-------
D-83 admits an environment to custody work (the pre-G-05 audit, G-06) "by the SHA-256 of the
committed per-environment identity file plus passing pin conformance; never by a declared
`environment_id`, never by a per-run hash". Both per-run hashes (`environment_lock_hash`,
`fixture_gate.environment_identity`) include `code_commit` and `config_hashes`, so keying
admission on them would admit exactly one run. This module is the single guard home for:

* the admission key: SHA-256 of `environment/identity/<environment_id>.json` (committed),
  granted only when the running interpreter's pins conform to it;
* pin conformance, one rule per layer (D-83 revision 6 §A6 item 8): pip is `name==version`
  over `pip freeze --all`, with `name @ file:///...` lines admitted only when the identity
  lists the name under `pip_exceptions`; conda is an exact match of each explicit URL line
  (name, version, build in the URL) plus its md5;
* agreement between the two representations of `environment_id` (the run record and the
  registry row), and the G-05 preflight refusal of a registry row that lacks it.

Inputs
------
The workspace root, an `environment_id`, the captured `pip freeze --all` text and, for a
conda environment, the `conda list --explicit --md5` text. Nothing is read from the network.

Re-run behaviour
----------------
Pure and deterministic: the same identity file and captures give the same key or the same
refusal. Nothing is written. The identity files themselves are produced by the environment
restore plan (D-83 §A7 item 15) and committed; this module never creates one.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Final

from src.data.config import ENVIRONMENT_IDS, UNDECLARED_ENVIRONMENT, IntegrityError

__all__ = [
    "IDENTITY_DIR",
    "admission_key",
    "assert_environment_id_agreement",
    "assert_row_declares_environment",
    "check_pin_conformance",
    "identity_path",
    "parse_conda_explicit",
    "parse_pip_freeze",
]

#: Where the committed per-environment identity files live, relative to the workspace.
IDENTITY_DIR: Final[Path] = Path("environment") / "identity"


def identity_path(workspace: Path, environment_id: str) -> Path:
    return Path(workspace) / IDENTITY_DIR / f"{environment_id}.json"


def _pep503(name: str) -> str:
    """PEP 503 normalised project name, so `Foo_Bar` and `foo-bar` compare equal."""
    return re.sub(r"[-_.]+", "-", name.strip()).lower()


def parse_pip_freeze(text: str) -> tuple[dict[str, str], dict[str, str]]:
    """Split `pip freeze --all` into `{name: version}` pins and `{name: line}` direct refs."""
    pins: dict[str, str] = {}
    direct: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if " @ " in line:
            name = _pep503(line.split(" @ ", 1)[0])
            direct[name] = line
        elif "==" in line:
            name, version = line.split("==", 1)
            pins[_pep503(name)] = version.strip()
        else:
            raise IntegrityError("pip freeze --all", f"unrecognised line {line!r}")
    return pins, direct


def parse_conda_explicit(text: str) -> set[str]:
    """The explicit URL lines (`<url>#<md5>`) of `conda list --explicit --md5`."""
    lines: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("@"):
            continue
        if "#" not in line:
            raise IntegrityError(
                "conda list --explicit --md5", f"line lacks its md5: {line!r}"
            )
        lines.add(line)
    return lines


def check_pin_conformance(
    identity: Mapping[str, Any], *, pip_freeze_all: str, conda_explicit: str | None
) -> list[str]:
    """Every disagreement between the captured environment and its identity, as text.

    Empty means conformance. Pip: both directions are checked (a package present in only
    one side is a disagreement), because an extra installed package is drift too.
    """
    problems: list[str] = []
    expected_pip = {_pep503(str(k)): str(v) for k, v in dict(identity.get("pip", {})).items()}
    exceptions = {_pep503(str(n)) for n in identity.get("pip_exceptions", [])}
    pins, direct = parse_pip_freeze(pip_freeze_all)
    for name in sorted(set(expected_pip) | set(pins)):
        if name in exceptions:
            continue
        want, got = expected_pip.get(name), pins.get(name)
        if want != got:
            problems.append(f"pip {name}: identity {want!r}, installed {got!r}")
    for name in sorted(direct):
        if name not in exceptions:
            problems.append(f"pip {name}: direct reference {direct[name]!r} is not a listed exception")
    expected_conda = identity.get("conda")
    if expected_conda is not None:
        if conda_explicit is None:
            problems.append("conda: the identity pins a conda layer but none was captured")
        else:
            want_set = {str(x) for x in expected_conda}
            got_set = parse_conda_explicit(conda_explicit)
            for line in sorted(want_set - got_set):
                problems.append(f"conda missing or differing: {line}")
            for line in sorted(got_set - want_set):
                problems.append(f"conda not in identity: {line}")
    return problems


def admission_key(
    workspace: Path,
    environment_id: str,
    *,
    pip_freeze_all: str,
    conda_explicit: str | None = None,
) -> str:
    """The admission key, or a refusal naming why the environment is not admitted.

    The key is the SHA-256 of the committed identity file bytes. It does not depend on the
    run's commit or configs, so every run in an admitted, conforming environment carries
    the same key (D-83 revision 7 §A7 item 4).
    """
    if environment_id == UNDECLARED_ENVIRONMENT or environment_id not in ENVIRONMENT_IDS:
        raise IntegrityError(
            "environment_id",
            f"{environment_id!r} is not a named environment; admission is by the identity "
            "of one of the three named environments (D-83 revision 7 section R4-7 item 1)",
        )
    path = identity_path(workspace, environment_id)
    if not path.is_file():
        raise IntegrityError(
            path,
            "no committed identity file for this environment; it is written by the "
            "environment restore plan (D-83 revision 7 section A7 item 15), never here",
        )
    # Canonical LF bytes: the key must not depend on the checkout's line endings
    # (GOV-2026-09-30-PV-09 DATA-01; `.gitattributes` also pins eol=lf).
    raw = path.read_bytes().replace(b"\r\n", b"\n")
    identity = json.loads(raw.decode("utf-8"))
    if identity.get("environment_id") != environment_id:
        raise IntegrityError(
            path, f"identity file names {identity.get('environment_id')!r}, not {environment_id!r}"
        )
    problems = check_pin_conformance(
        identity, pip_freeze_all=pip_freeze_all, conda_explicit=conda_explicit
    )
    if problems:
        raise IntegrityError(
            path,
            "pin conformance failed (D-83 revision 6 section A6 item 8): " + "; ".join(problems[:20]),
        )
    return hashlib.sha256(raw).hexdigest()


def assert_environment_id_agreement(
    registry_row: Mapping[str, Any], run_record: Any
) -> None:
    """The registry row and the run record must name the same environment (W-4)."""
    on_row = registry_row.get("environment_id")
    on_record = getattr(run_record, "environment_id", None)
    if on_row != on_record:
        raise IntegrityError(
            "environment_id",
            f"registry row says {on_row!r} but the run record says {on_record!r}; the two "
            "representations must agree (D-83 revision 7 section A7 item 14)",
        )


def assert_row_declares_environment(registry_row: Mapping[str, Any]) -> str:
    """G-05 preflight: a registry row without a named environment fails (W-4)."""
    value = registry_row.get("environment_id")
    if not isinstance(value, str) or value not in ENVIRONMENT_IDS:
        raise IntegrityError(
            f"registry row {registry_row.get('run_id')!r}",
            f"environment_id {value!r} is absent or not a named environment; the G-05 "
            "preflight refuses it (D-83 revision 6 section A6 item 7)",
        )
    return value


def g05_access_preflight(access_log: Path, *, cutoff_utc: str | None) -> int:
    """D-83 revision 7 §R4-7 item 3: every restricted-purpose access row logged before the
    cutoff fails G-05 preflight; returns the number of rows checked.

    The cutoff is the adoption timestamp of the characterising D-number (§R5-5 item 11).
    Until it exists no pre-G-05 audit can pass, so `cutoff_utc=None` refuses. The check
    keys on the guard-stamped `logged_at_utc` ONLY; a row without it, or with an
    unparseable one, fails.
    """
    import datetime as _dt

    if not cutoff_utc:
        raise IntegrityError(
            "G-05 preflight",
            "no cutoff exists: the characterising D-number (section R5-5 item 11) is not "
            "adopted, so no pre-G-05 audit can pass (D-83 revision 7 section R4-7 item 3)",
        )
    try:
        cutoff = _dt.datetime.fromisoformat(cutoff_utc.replace("Z", "+00:00"))
    except ValueError as exc:
        raise IntegrityError("G-05 preflight", f"cutoff {cutoff_utc!r} is unparseable") from exc
    if cutoff.tzinfo is None:
        raise IntegrityError(
            "G-05 preflight", f"cutoff {cutoff_utc!r} has no timezone; it must be UTC-aware"
        )
    path = Path(access_log)
    if not path.is_file():
        # An absent governed log is missing custody evidence, not an empty one
        # (GOV-2026-09-30-PV-09 DATA-10).
        raise IntegrityError(path, "the governed access log is absent; G-05 preflight cannot pass")
    checked = 0
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        checked += 1
        logged = row.get("logged_at_utc")
        try:
            when = _dt.datetime.fromisoformat(str(logged).replace("Z", "+00:00"))
        except ValueError as exc:
            raise IntegrityError(
                path, f"line {number}: logged_at_utc {logged!r} is missing or unparseable"
            ) from exc
        if when.tzinfo is None or when < cutoff:
            raise IntegrityError(
                path,
                f"line {number}: restricted-purpose row logged {logged} before the cutoff "
                f"{cutoff_utc}; it fails G-05 preflight (D-83 revision 7 section R4-7 item 3)",
            )
    return checked
