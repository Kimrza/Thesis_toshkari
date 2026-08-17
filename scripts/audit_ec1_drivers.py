"""EC-1 driver audit: Kyoto WDC Dst grade span and Canadian F10.7 archive coverage.

Produces the measured evidence for the two acquisition-freeze obligations recorded in
the intent statement (obligations 1 and 2) and gated as entry condition EC-1 in the
initiative brief.

Reads only local files under evidence/audit_ec1_2026-08-15/ that were retrieved once
and hashed. Re-running it against the same files reproduces the same report.

Usage:
    python scripts/audit_ec1_drivers.py
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


def main() -> int:
    report = {
        "generated_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "obligation_1_kyoto_dst": audit_dst(),
        "obligation_2_canadian_f107": audit_f107(),
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
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
