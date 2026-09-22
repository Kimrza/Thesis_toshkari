"""G-09 gate wrapper: writes `aws_ai_dlc_preflight_report` (TE 18.3; TA-23; FR-WS-7).

Purpose
-------
Produces the evidence artifact TE 18.3 names, by aggregating the four preflight limbs
`src/data/preflight_report.py` defines: the zero-`TBD` check and the declared-source
check are computed from `configs/`; the ten critical tests are READ from a junit XML that
an actual pytest run wrote; the supervisor sign-off is READ from a record the student
authors. Nothing is asserted from source and no limb is synthesised — an uncollected limb
renders `absent` and the verdict stays `not_green` (R-02).

Running this at a gate is a HUMAN / governed act. A `green` verdict is evidence FOR G-09,
not G-09's signature: the gate is the supervisor's (Vision 13.1).

Inputs
------
`--config configs/` (the four governed configs, read only through `load_configs`);
`--phase 1|2`; `--junit <path>` (optional; the pytest `--junitxml` file of the run whose
critical tests are being evidenced); `--signoff <path>` (optional; the six-item sign-off
record); `--code-commit` (explicit commit where no git tree exists, e.g. Kaggle);
`--output <path>` (default `artifacts/preflight/aws_ai_dlc_preflight_report_<utc>.json`).

Re-run behaviour
----------------
Read-only over configs and evidence; writes exactly one JSON per invocation, named by
UTC timestamp, so re-runs never overwrite prior evidence. Exit code 0 when the report was
written (whatever its verdict — the verdict is the content), 1 on a precondition failure
(unreadable junit or record, unloadable configs): an unusable input is a failure, never
a silently absent limb.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data.config import IntegrityError, load_configs  # noqa: E402
from src.data.preflight_report import (  # noqa: E402
    build_aws_ai_dlc_preflight_report,
    read_junit_module_outcomes,
    read_signoff_record,
)


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="gate_preflight_report.py", description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--phase", type=int, choices=(1, 2), default=1)
    parser.add_argument("--junit", type=Path, default=None)
    parser.add_argument("--signoff", type=Path, default=None)
    parser.add_argument("--code-commit", type=str, default=None)
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args(argv)


def _head_commit() -> str | None:
    import subprocess

    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        snapshot = load_configs(args.config, phase=args.phase)
        outcomes = read_junit_module_outcomes(args.junit) if args.junit else None
        record = read_signoff_record(args.signoff) if args.signoff else None
    except IntegrityError as exc:
        print(f"gate_preflight_report: precondition failure: {exc}", file=sys.stderr)
        return 1
    report = build_aws_ai_dlc_preflight_report(
        snapshot,
        phase=args.phase,
        code_commit=args.code_commit or _head_commit(),
        junit_outcomes=outcomes,
        signoff_record=record,
        junit_path=str(args.junit) if args.junit else None,
        signoff_path=str(args.signoff) if args.signoff else None,
    )
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = args.output or (
        REPO_ROOT / "artifacts" / "preflight" / f"aws_ai_dlc_preflight_report_{stamp}.json"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1, sort_keys=False), encoding="utf-8")
    print(
        f"gate_preflight_report: verdict={report['verdict']} "
        f"limbs_not_passed={report['limbs_not_passed']} -> {out}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
