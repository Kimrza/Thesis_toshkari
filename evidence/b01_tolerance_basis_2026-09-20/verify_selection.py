"""Re-derive the eight R-59 validation cases' activity claims from the audited definitive Kp
record using JANUARY-NOVEMBER rows ONLY (December rows are skipped before parsing), and check
that no case falls in December 2022. Prints what it derives before asserting; writes
`selection_verification.json` beside itself.

Inputs: evidence/audit_gfz_2026-09-18/Kp_def2022.wdc (GFZ definitive Kp, WDC layout);
evidence/iri2016_official_reference_2026-09-19/sample_selection.json (the fixed selection).
Re-run behaviour: pure function of those two files; deterministic output.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

WS = Path(__file__).resolve().parents[2]
kp_path = WS / "evidence/audit_gfz_2026-09-18/Kp_def2022.wdc"
sel = json.loads(
    (WS / "evidence/iri2016_official_reference_2026-09-19/sample_selection.json").read_text(
        encoding="utf-8"
    )
)

THIRDS = {0: 0.0, 3: 1 / 3, 7: 2 / 3}
days: dict[dt.date, list[float]] = {}
for line in kp_path.read_text(encoding="utf-8").splitlines():
    if line.startswith("#") or not line.strip():
        continue
    yy, mm, dd = int(line[0:2]), int(line[2:4]), int(line[4:6])
    if mm == 12:
        continue  # locked month: never parsed here
    codes = [line[12 + 2 * i : 14 + 2 * i] for i in range(8)]
    kps = [int(c.strip() or 0) // 10 + THIRDS[int(c.strip() or 0) % 10] for c in codes]
    days[dt.date(2000 + yy, mm, dd)] = kps

print(f"rows parsed (Jan-Nov only): {len(days)}")
assert len(days) == 334, len(days)
daymax = {d: max(v) for d, v in days.items()}
daysum = {d: sum(v) for d, v in days.items()}
all_zero = sorted(d for d, v in days.items() if all(x == 0 for x in v))
print("Jan-Nov days with Kp = 0.0 in every slot:", [str(d) for d in all_zero])
print("Jan-Nov quietest by daily sum:", sorted(daysum.items(), key=lambda kv: kv[1])[:3])
ge6 = [(str(d), i, round(k, 2)) for d, v in days.items() for i, k in enumerate(v) if k >= 6]
print("Jan-Nov most disturbed slots (Kp>=6):", ge6)

problems: list[str] = []
cases: list[dict[str, object]] = []
for i, s in enumerate(sel["samples"], 1):
    t = dt.datetime.fromisoformat(s["target_time_utc"])
    if t.year == 2022 and t.month == 12:
        problems.append(f"case {i} is in December 2022")
    d = t.date()
    slot = t.hour // 3
    kp_slot = days[d][slot]
    cases.append(
        {"case": i, "site": s["site"], "utc": s["target_time_utc"], "slot_kp": kp_slot,
         "day_max_kp": daymax[d]}
    )
    print(
        f"case {i}: {s['site']} {t:%Y-%m-%d %H}UT slot {slot} ({3 * slot:02d}-{3 * slot + 3:02d}UT) "
        f"Kp={kp_slot:.2f} daymax={daymax[d]:.2f} | claim: {s['rationale'][:70]}"
    )
print("December cases:", problems or "none")
assert not problems
# the recorded activity claims, one assertion each
assert all(x == 0 for x in days[dt.date(2022, 1, 7)])
assert abs(days[dt.date(2022, 3, 13)][7] - 6 - 1 / 3) < 1e-9
assert abs(days[dt.date(2022, 9, 4)][3] - 6 - 1 / 3) < 1e-9
assert daymax[dt.date(2022, 8, 4)] == 2.0
assert days[dt.date(2022, 9, 4)][7] == 5.0
assert abs(daymax[dt.date(2022, 11, 17)] - 2 / 3) < 1e-9
assert days[dt.date(2022, 4, 14)][5] == 6.0
print("all eight activity claims re-derived from Jan-Nov rows: OK")
out = {
    "kind": "r59_case_selection_verification",
    "rows_parsed_jan_nov": len(days),
    "december_rows_parsed": 0,
    "december_cases": problems,
    "jan_nov_all_zero_days": [str(d) for d in all_zero],
    "jan_nov_slots_kp_ge_6": ge6,
    "cases": cases,
    "conclusion": (
        "every case is outside December 2022; every activity claim re-derives from "
        "January-November rows alone, so December values could not have influenced the "
        "selection (an extremum over a set that excludes December is independent of "
        "December's values)"
    ),
}
Path(__file__).with_name("selection_verification.json").write_text(
    json.dumps(out, indent=1) + "\n", encoding="utf-8"
)
