"""EC-1 driver audit: Kyoto WDC Dst grade span and Canadian F10.7 archive coverage.

Produces the measured evidence for the two acquisition-freeze obligations recorded in
the intent statement (obligations 1 and 2) and gated as entry condition EC-1 in the
initiative brief.

Reads only local files under evidence/audit_ec1_2026-08-15/ that were retrieved once
and hashed. Re-running it against the same files reproduces the same report.

Usage:
    python scripts/audit_ec1_drivers.py

PRE-TC-06 TOOLING, PENDING A RETIREMENT RULING (board Recommendation 51, 2026-09-20).
This script predates TC-06 and does not meet the §12/§13.2 CLI convention: no `argparse`,
no `--config configs/`, no governed configuration read, and no `NN_verb_noun.py` ordinal
position. Its successors are `scripts/00_acquire_prepared_vtec.py` (retrieval and
provenance) and `scripts/01_inventory_and_registry.py` (inventory and audit). The approved
disposition is RETIREMENT rather than migration, and the owner is drafting that ruling; the
script is NOT migrated here.

On the two-tier posture (`team.md` § Code Style), read precisely. The machine-readable half
is already satisfied: `audit_dst` writes `missing_days` and `expected_days` per month into
the emitted report, so a completeness shortfall is a field and not console text. A
completeness shortfall is also legitimately NON-FATAL, so `main`'s unconditional `return 0`
is correct and is not the defect. What was unmet is the remaining clause — "the artifact
explicitly marked derived and/or partial" — and the report now carries a top-level
`partial` flag with the months that set it. That one field stands whether or not the
retirement ruling lands.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "audit_ec1_2026-08-15"
KYOTO = EVIDENCE / "kyoto_dst"
NRCAN = EVIDENCE / "nrcan_f107" / "fluxtable.txt"

YEAR = 2022
OUTAGE_START = dt.date(2022, 3, 18)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def days_in_year(year: int) -> list[dt.date]:
    start, end = dt.date(year, 1, 1), dt.date(year, 12, 31)
    return [start + dt.timedelta(days=i) for i in range((end - start).days + 1)]


# --------------------------------------------------------------------------
# Obligation 1 — Kyoto WDC Dst
# --------------------------------------------------------------------------

def audit_dst() -> dict:
    """Confirm a single grade across 2022 and count the day rows each month carries."""
    if not KYOTO.is_dir():
        raise SystemExit(f"missing evidence directory: {KYOTO}")

    months = {}
    for month in range(1, 13):
        path = KYOTO / f"dst_provisional_2022{month:02d}.html"
        if not path.exists():
            months[month] = {"error": "file not retrieved"}
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        # The monthly table is one line per day: the day number in columns 1-2,
        # followed by 24 hourly integers.
        day_rows = set()
        for line in text.splitlines():
            m = re.match(r"^\s*(\d{1,2})((?:\s+-?\d+){24})\s*$", line)
            if m:
                day_rows.add(int(m.group(1)))

        expected = (dt.date(2022, month % 12 + 1, 1) if month < 12 else dt.date(2023, 1, 1))
        expected_days = (expected - dt.date(2022, month, 1)).days

        months[month] = {
            "file": path.name,
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
            "expected_days": expected_days,
            "day_rows_parsed": len(day_rows),
            "missing_days": sorted(set(range(1, expected_days + 1)) - day_rows),
        }

    return months


# --------------------------------------------------------------------------
# Obligation 2 — Canadian observed F10.7
# --------------------------------------------------------------------------

FLUX_RE = re.compile(
    r"^(?P<date>\d{8})\s+(?P<time>\d{6})\s+(?P<julian>[\d.]+)\s+"
    r"(?P<carrington>[\d.]+)\s+(?P<obs>[\d.]+)\s+(?P<adj>[\d.]+)\s+(?P<ursi>[\d.]+)\s*$"
)


def audit_f107() -> dict:
    if not NRCAN.exists():
        raise SystemExit(f"missing evidence file: {NRCAN}")

    by_day: dict[dt.date, list[dict]] = defaultdict(list)
    unparsed: list[str] = []
    prev_date = None
    monotonic = True
    total = 0

    with NRCAN.open("r", encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if not line.strip():
                continue
            if line.lstrip().startswith(("fluxdate", "---")):
                continue
            m = FLUX_RE.match(line)
            if not m:
                unparsed.append(line[:120])
                continue
            total += 1
            date = dt.datetime.strptime(m.group("date"), "%Y%m%d").date()
            if prev_date is not None and date < prev_date:
                monotonic = False
            prev_date = date
            if date.year == YEAR:
                by_day[date].append({"time": m.group("time"), "obs": float(m.group("obs"))})

    all_days = days_in_year(YEAR)
    present = sorted(by_day)
    missing = [d for d in all_days if d not in by_day]
    missing_from_outage = [d for d in missing if d >= OUTAGE_START]

    # Contiguous runs of missing days, so an outage reads as one span not N dates.
    runs = []
    for d in missing:
        if runs and d == runs[-1][-1] + dt.timedelta(days=1):
            runs[-1].append(d)
        else:
            runs.append([d])

    return {
        "file": NRCAN.name,
        "sha256": sha256(NRCAN),
        "bytes": NRCAN.stat().st_size,
        "records_total": total,
        "records_2022": sum(len(v) for v in by_day.values()),
        "dates_monotonic_non_decreasing": monotonic,
        "unparsed_lines": len(unparsed),
        "unparsed_sample": unparsed[:5],
        "days_expected_2022": len(all_days),
        "days_present_2022": len(present),
        "days_missing_2022": [d.isoformat() for d in missing],
        "days_missing_from_2022_03_18": [d.isoformat() for d in missing_from_outage],
        "missing_runs": [
            {
                "start": run[0].isoformat(),
                "end": run[-1].isoformat(),
                "length_days": len(run),
            }
            for run in runs
        ],
        "readings_per_day_distribution": {
            str(n): sum(1 for v in by_day.values() if len(v) == n)
            for n in sorted({len(v) for v in by_day.values()})
        },
        "first_2022_date": present[0].isoformat() if present else None,
        "last_2022_date": present[-1].isoformat() if present else None,
    }


def _partial_reasons(dst: dict, f107: dict) -> list[str]:
    """Every measured completeness shortfall, as machine-readable reasons.

    `team.md` § Code Style: a completeness shortfall is non-fatal but the artifact must be
    "explicitly marked derived and/or partial". The per-month `missing_days` fields already
    carried the detail; what a reader had no way to see at a glance was whether the report
    as a whole is complete. Derived from the measurements, never asserted alongside them.
    """
    reasons: list[str] = []
    for month, info in sorted(dst.items()):
        if info.get("error"):
            reasons.append(f"kyoto_dst 2022-{int(month):02d}: {info['error']}")
        elif info.get("missing_days"):
            reasons.append(
                f"kyoto_dst 2022-{int(month):02d}: {len(info['missing_days'])} of "
                f"{info.get('expected_days')} day rows absent"
            )
    if f107.get("days_missing_2022"):
        reasons.append(
            f"nrcan_f107: {len(f107['days_missing_2022'])} of "
            f"{f107.get('days_expected_2022')} calendar days absent"
        )
    if f107.get("unparsed_lines"):
        reasons.append(f"nrcan_f107: {f107['unparsed_lines']} unparsed line(s)")
    return reasons


def main() -> int:
    dst = audit_dst()
    f107 = audit_f107()
    partial_reasons = _partial_reasons(dst, f107)
    report = {
        "generated_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        # Recommendation 51: the artifact marks ITSELF derived and partial. `partial` is
        # the flag a reader or a downstream check can act on; `partial_reasons` is why,
        # derived from the measurements above rather than restated beside them. A
        # completeness shortfall stays non-fatal — `main` still returns 0 — so the exit
        # code reports integrity and this field reports completeness, which is the
        # two-tier split (`team.md` § Code Style).
        "artifact_kind": "DERIVED -- audit over locally retrieved, hashed evidence",
        "partial": bool(partial_reasons),
        "partial_reasons": partial_reasons,
        "obligation_1_kyoto_dst": dst,
        "obligation_2_canadian_f107": f107,
    }
    out = EVIDENCE / "ec1-audit-report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["obligation_2_canadian_f107"], indent=2))
    print("\n--- Dst grade span ---")
    for month, info in report["obligation_1_kyoto_dst"].items():
        print(
            f"2022-{int(month):02d}  rows={info.get('day_rows_parsed')}/"
            f"{info.get('expected_days')}  missing={info.get('missing_days')}"
        )
    if partial_reasons:
        print("\nPARTIAL — recorded in the report's `partial`/`partial_reasons` fields:")
        for reason in partial_reasons:
            print(f"  {reason}")
    print(f"\nwrote {out}")
    # Completeness shortfalls are non-fatal by contract and are recorded as fields above,
    # never signalled by the exit code. A non-zero exit here would mean an INTEGRITY
    # violation, and the two must not be conflated (`team.md` § Code Style).
    return 0


if __name__ == "__main__":
    sys.exit(main())
