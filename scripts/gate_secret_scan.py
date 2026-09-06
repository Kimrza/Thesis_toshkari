"""TA-22 gate-scan wrapper: the history-inclusive secret scan, emitting SD-01's evidence.

Purpose
-------
A thin wrapper around the pinned `gitleaks` binary so the HISTORY-INCLUSIVE scan —
the only mode whose result can be attached to TA-22 (SD-01, Q1=B) — emits the evidence
contract SD-01 fixes: tool name and PINNED version, the commit range scanned, the scan
scope (which of history, configurations, logs and artifacts were covered), and the
result. A scan report that does not name its commit range is not evidence: TA-22 is a
claim about a range, and a report without one cannot be checked against the commit
being gated.

Running this at a gate is a HUMAN / governed act. Nothing in this module claims TA-22
discharged: NFR-SEC-01 and TA-22 remain unclaimed until the required checks have
actually passed and the evidence is accepted at the gate (R-14's dated clause,
2026-08-28). The incremental pre-commit scan (`.githooks/pre-commit`) is a preventive
net and proves nothing about history; the two modes must never be confused.

Inputs
------
* the repository working tree and its FULL git history (``gitleaks git`` mode);
* `.gitleaks.toml` — the reviewed allowlist;
* CLI: ``--output <path>`` for the evidence JSON (default
  ``artifacts/exec_evidence/ta22_secret_scan_<utc>.json``), ``--range <rev-range>``
  to narrow the scanned range (default: the full history reachable from HEAD).

Re-run behaviour
----------------
Read-only over the repository; writes exactly one evidence JSON per invocation, named
by UTC timestamp so re-runs never overwrite prior evidence. Deterministic for a fixed
tree, history and gitleaks version. Exit code: 0 on a clean scan, 1 on findings or on
any precondition failure (unpinned tool, missing config) — an unusable scan is a
failure, never a silently absent check.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The pinned gitleaks version (SD-01, Q2=A). Must agree with requirements.txt's
#: comment pin and .githooks/pre-commit; drift between them is a silent narrowing.
PINNED_GITLEAKS_VERSION = "8.18.4"

#: SD-01's scan-scope declaration for TA-22: what this invocation covers.
SCAN_SCOPE = {
    "history": True,          # gitleaks git mode walks every commit in the range
    "configurations": True,   # tracked configs are in the tree at every commit
    "logs": True,             # tracked logs likewise; untracked logs are out of git's reach
    "artifacts": True,        # tracked artifacts likewise
    "note": (
        "scope covers everything version control has ever recorded in the scanned "
        "range; files never committed are outside a history scan by construction"
    ),
}


def _fail(message: str) -> int:
    print(f"gate_secret_scan: {message}", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=None, help="evidence JSON path")
    parser.add_argument(
        "--range",
        dest="rev_range",
        default=None,
        help="git rev range to scan (default: full history reachable from HEAD)",
    )
    args = parser.parse_args(argv)

    config = REPO_ROOT / ".gitleaks.toml"
    if not config.is_file():
        return _fail(f"{config} is missing; the reviewed allowlist is part of the scan")

    # --- the tool must be the PINNED version (SD-01) -----------------------------------
    try:
        version_output = subprocess.run(
            ["gitleaks", "version"], capture_output=True, text=True, timeout=60, check=True
        ).stdout.strip().lstrip("v")
    except (OSError, subprocess.SubprocessError) as exc:
        return _fail(
            f"gitleaks is not runnable ({exc}); install the pinned "
            f"{PINNED_GITLEAKS_VERSION} — an unpinned or absent scanner produces no "
            f"evidence"
        )
    if version_output != PINNED_GITLEAKS_VERSION:
        return _fail(
            f"gitleaks {version_output} found but {PINNED_GITLEAKS_VERSION} is pinned; "
            f"refusing to produce TA-22 evidence with an unpinned tool"
        )

    # --- the commit range (the part of the evidence contract most often omitted) -------
    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        ).stdout.strip()
        root_commit = subprocess.run(
            ["git", "rev-list", "--max-parents=0", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
            check=True,
        ).stdout.strip().splitlines()[-1]
    except (OSError, subprocess.SubprocessError) as exc:
        return _fail(f"the commit range could not be determined ({exc})")
    commit_range = args.rev_range or f"{root_commit}..{head} (full history)"

    # --- the scan -----------------------------------------------------------------------
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    findings_path = REPO_ROOT / "artifacts" / "exec_evidence" / f"ta22_findings_{stamp}.json"
    findings_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "gitleaks",
        "git",
        "--config",
        str(config),
        "--redact",
        "--report-format",
        "json",
        "--report-path",
        str(findings_path),
        "--exit-code",
        "2",
        str(REPO_ROOT),
    ]
    if args.rev_range:
        command[2:2] = ["--log-opts", args.rev_range]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=3600)
    if completed.returncode not in (0, 2):
        return _fail(
            f"gitleaks failed to run (exit {completed.returncode}): "
            f"{completed.stderr.strip()[:2000]}"
        )
    clean = completed.returncode == 0

    # --- SD-01's evidence contract -------------------------------------------------------
    evidence = {
        "evidence_for": "TA-22 (NFR-SEC-01, REQ-ENG-6, FR-P1-01-10)",
        "claim_status": (
            "NOT CLAIMED by this script: acceptance is a gate act; this file is the "
            "evidence input (SD-01)"
        ),
        "tool": {"name": "gitleaks", "pinned_version": PINNED_GITLEAKS_VERSION,
                 "running_version": version_output},
        "commit_range": commit_range,
        "scan_scope": SCAN_SCOPE,
        "allowlist_config": str(config.relative_to(REPO_ROOT)),
        "result": "clean" if clean else "FINDINGS PRESENT",
        "findings_report": str(findings_path.relative_to(REPO_ROOT)),
        "scanned_at_utc": stamp,
    }
    output = args.output or (
        REPO_ROOT / "artifacts" / "exec_evidence" / f"ta22_secret_scan_{stamp}.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"gate_secret_scan: evidence written to {output}")
    print(f"gate_secret_scan: result = {evidence['result']}")
    return 0 if clean else 1


if __name__ == "__main__":
    sys.exit(main())
