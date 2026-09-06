"""The TE 10.1 External Method and Code-Reuse Register: registered BEFORE use, or refused.

Purpose
-------
NFR-LIC-01, TE 10.1 and gate G-P2's mechanism (R-29, R-30, SD-G-06). Any reused or
materially adapted third-party source is recorded with **all fifteen 10.1 fields**
before the code is used and before G-P2. Enforcement is two-sided:

* every adapter module carries a mandatory **provenance marker**
  (``REUSE-PROVENANCE: <reuse_id>``) — without it an unregistered copy is
  indistinguishable from original work by inspection, and the completeness assertion
  has nothing to range over;
* the register is asserted complete against the set of marked modules — a marked
  module with no complete register row is a **failure** (use before registration),
  and a row missing any of the fifteen fields is refused at construction and again
  at load.

**Reimplementation is the standing default, not a fallback.** `project.md` § Forbidden
prohibits copying or materially adapting third-party source whose licence is absent,
ambiguous or incompatible — reimplement the published method from the paper with a
citation instead. The register is the exception path, deliberately harder to reach
than reimplementation, because that is the policy actually in force. The AGPLv3
Global-TEC-forecasting repository is the one approved direct-copy source today, and
**whether its repository-distribution obligations permit that copying is a governance
dependency this project does not resolve on its own** — stated here, not resolved.

Inputs
------
* `register_path` — the JSONL register file (created on first append).
* `ReuseRecord` — one complete fifteen-field row per reused source.
* module trees (`src/`, `scripts/`) — scanned read-only for provenance markers.

Re-run behaviour
----------------
`register_reuse` is append-safe and idempotence-free by design: every call appends one
newline-terminated row under append mode, flushed and fsynced before returning, and
never reads, rewrites or reorders prior rows (the NFR-AUD-01 posture foundation's
registry writer set). The scans and assertions are pure reads. TA-28 stays `Pending`:
this module supplies mechanism, never acceptance evidence.

Governance
----------
* TE 10.1's full field set as affirmed in `project.md` § Mandated (fifteen fields,
  superseding the abbreviated list previously implied).
* `ReuseError` rides foundation R-01's "any future integrity-related exception"
  clause and derives from `IntegrityError` (`src/data/config.py`); every raise names
  the resource and the violated expectation.
* Proven by `tests/test_reuse_registry.py` (R-29's named evidence module).
"""

from __future__ import annotations

import json
import os
import re
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass
from dataclasses import fields as _dataclass_fields
from pathlib import Path
from typing import Final

from src.data.config import IntegrityError

__all__ = [
    "REUSE_REGISTER_FIELDS",
    "PROVENANCE_MARKER",
    "ReuseError",
    "ReuseRecord",
    "register_reuse",
    "load_register",
    "find_marked_modules",
    "assert_reuse_registered_before_use",
]


class ReuseError(IntegrityError):
    """A reuse-register obligation is violated: use before registration, or a short row.

    Rides foundation R-01's "any future integrity-related exception" clause: declared
    here because only this module and its test raise it.
    """


#: TE 10.1's fifteen fields, exactly as affirmed in `project.md` § Mandated:
#: reuse_id; repository URL; immutable commit or tag; upstream file and line or
#: function; retrieval date; licence and SPDX ID; copied-versus-adapted status;
#: destination file; scientific purpose; modifications; tests; original citation;
#: notice location; reviewer; approval date. Field identities, not scientific
#: constants (TC-03e does not reach a register schema).
REUSE_REGISTER_FIELDS: Final[tuple[str, ...]] = (
    "reuse_id",
    "repository_url",
    "commit_or_tag",
    "upstream_reference",
    "retrieval_date",
    "licence_spdx_id",
    "copied_or_adapted",
    "destination_file",
    "scientific_purpose",
    "modifications",
    "tests",
    "original_citation",
    "notice_location",
    "reviewer",
    "approval_date",
)

#: The mandatory provenance marker an adapter module carries, followed by its
#: `reuse_id`. An unmarked module is asserted to contain no reuse; a marked module
#: with no complete register row is a failure (W-9, R-29).
PROVENANCE_MARKER: Final[str] = "REUSE-PROVENANCE:"

_MARKER_PATTERN: Final[re.Pattern[str]] = re.compile(
    re.escape(PROVENANCE_MARKER) + r"\s*(?P<reuse_id>[A-Za-z0-9_.-]+)"
)


@dataclass(frozen=True)
class ReuseRecord:
    """One complete TE 10.1 register row. Every field is required and non-empty."""

    reuse_id: str
    repository_url: str
    commit_or_tag: str
    upstream_reference: str
    retrieval_date: str
    licence_spdx_id: str
    copied_or_adapted: str
    destination_file: str
    scientific_purpose: str
    modifications: str
    tests: str
    original_citation: str
    notice_location: str
    reviewer: str
    approval_date: str

    def __post_init__(self) -> None:
        empty = [
            field.name
            for field in _dataclass_fields(self)
            if not str(getattr(self, field.name)).strip()
        ]
        if empty:
            raise ReuseError(
                "ReuseRecord",
                f"incomplete register row: field(s) {', '.join(empty)} empty; TE 10.1 "
                f"requires ALL fifteen fields before the code is used (NFR-LIC-01, "
                f"gate G-P2) — an incomplete row is refused, never stored",
            )
        if self.copied_or_adapted not in ("copied", "adapted"):
            raise ReuseError(
                "ReuseRecord",
                f"copied_or_adapted must be 'copied' or 'adapted', got "
                f"{self.copied_or_adapted!r}; the status is one of TE 10.1's fifteen "
                f"required facts, not free text",
            )


def register_reuse(register_path: Path, record: ReuseRecord) -> None:
    """Append one complete row, flushed and fsynced before returning (append-safe).

    Never rewrites or reorders prior rows; registering must happen BEFORE the code is
    used and before gate G-P2 (TE 10.1). Raises `ReuseError` when the append cannot be
    confirmed durable — a register row that might not exist is not a registration.
    """
    register_path = Path(register_path)
    register_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(asdict(record), sort_keys=True, ensure_ascii=False) + "\n"
    try:
        with register_path.open("a", encoding="utf-8") as handle:
            handle.write(line)
            handle.flush()
            os.fsync(handle.fileno())
    except OSError as exc:
        raise ReuseError(
            register_path,
            f"register append failed ({exc}); a reuse whose registration is not "
            f"durable is a reuse that is not registered (TE 10.1, NFR-LIC-01)",
        ) from exc


def load_register(register_path: Path) -> dict[str, Mapping[str, str]]:
    """Parse the register into `reuse_id -> row`. Fail-closed on every defect.

    Raises
    ------
    ReuseError
        an unparseable line, a row missing or blank on any of the fifteen fields, or
        a duplicated `reuse_id` — a register the assertion cannot trust proves
        nothing, so every defect is a failure rather than a skipped line.
    """
    path = Path(register_path)
    rows: dict[str, Mapping[str, str]] = {}
    if not path.is_file():
        return rows
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ReuseError(
                path,
                f"line {number} is not parseable JSON ({exc}); an unreadable register "
                f"row cannot evidence a registration and is a failure, not a skip",
            ) from exc
        if not isinstance(parsed, dict):
            raise ReuseError(path, f"line {number} is not a JSON object")
        missing = [name for name in REUSE_REGISTER_FIELDS if not str(parsed.get(name, "")).strip()]
        if missing:
            raise ReuseError(
                path,
                f"line {number} is missing or blank on required field(s) "
                f"{', '.join(missing)}; TE 10.1 requires all fifteen",
            )
        reuse_id = str(parsed["reuse_id"])
        if reuse_id in rows:
            raise ReuseError(
                path,
                f"reuse_id {reuse_id!r} appears more than once; a duplicated identity "
                f"is a malformed register, not a longer one",
            )
        rows[reuse_id] = {name: str(parsed[name]) for name in REUSE_REGISTER_FIELDS}
    return rows


def find_marked_modules(roots: Iterable[Path]) -> dict[str, str]:
    """Scan module trees for provenance markers: `module path -> declared reuse_id`.

    A module carrying more than one marker maps each marker to a row obligation; for
    simplicity of the return shape the FIRST marker names the module and additional
    markers are validated by `assert_reuse_registered_before_use`.
    """
    marked: dict[str, str] = {}
    for root in roots:
        root = Path(root)
        if not root.is_dir():
            continue
        for module in sorted(root.rglob("*.py")):
            try:
                text = module.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                raise ReuseError(
                    module,
                    f"cannot be read while scanning for provenance markers ({exc}); "
                    f"an unreadable module cannot be asserted reuse-free",
                ) from exc
            match = _MARKER_PATTERN.search(text)
            if match:
                marked[module.as_posix()] = match.group("reuse_id")
    return marked


def assert_reuse_registered_before_use(
    roots: Iterable[Path], register_path: Path
) -> dict[str, str]:
    """R-29's completeness assertion: every marked module has a complete register row.

    Returns the `module -> reuse_id` mapping that was verified, so the caller (and the
    test) can record the population explicitly — an empty mapping is a derived fact
    about the tree, never a vacuous pass hidden from the reader.

    Raises
    ------
    ReuseError
        a marked module whose `reuse_id` has no register row (use before
        registration — the code exists to be used and its registration does not), or
        any register defect `load_register` refuses.
    """
    marked = find_marked_modules(roots)
    register = load_register(register_path)
    unregistered = {
        module: reuse_id for module, reuse_id in marked.items() if reuse_id not in register
    }
    if unregistered:
        raise ReuseError(
            ", ".join(sorted(unregistered)),
            f"provenance-marked module(s) with no complete register row for "
            f"{sorted(set(unregistered.values()))}; TE 10.1 requires registration "
            f"BEFORE the code is used and before gate G-P2 (NFR-LIC-01) — "
            f"reimplementation from the paper with a citation remains the standing "
            f"default while the AGPLv3 distribution question is open",
        )
    return marked
