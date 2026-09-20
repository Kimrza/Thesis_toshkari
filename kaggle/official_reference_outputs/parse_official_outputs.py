"""Assemble `kaggle/b01_validation_samples.json` from the saved CCMC Instant Run outputs.

Purpose: turn the eight text outputs saved from the official IRI-2016 web interface
(collected per `kaggle/b01_official_reference_collection_sheet.md`) into the R-59 area-6
samples file, WITHOUT retyping any number by hand. Every value is parsed from the saved
file and each file is matched to its template case by the header the server echoed
(year, day-of-year, UT hour, rounded lat/lon) -- never by its filename, so a mislabelled
file can only fail to match, not silently fill the wrong case.

Inputs:
  kaggle/b01_validation_samples.TEMPLATE.json   the eight predeclared cases (never edited)
  kaggle/official_reference_outputs/case_*.txt   the saved outputs (one per case)

Outputs:
  kaggle/b01_validation_samples.DRAFT.json       always written (cases without an output
                                                 keep null values and are listed)
  kaggle/b01_validation_samples.json             written ONLY when all eight cases matched

Per case the script records: `official_interface_value` (the TEC column, exactly as
printed, one decimal), `official_interface_top` (the `t/%` column: percentage of TEC above
the F2 peak), `official_interface_hmf2_km` (the D-50 hmF2 diagnostic; no threshold),
`official_interface_header` (the header block verbatim: options echoed by the server,
index values used, integration limits), and `official_interface_source` (interface, file,
retrieval instant from the file's modification time in UTC).

Re-run behaviour: deterministic for a fixed set of files; the draft is overwritten each
run, the final file is rewritten only when complete. Nothing here touches the adapter or
computes an adapter value -- the paired comparison happens only in stage 04 on Kaggle.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KAGGLE = HERE.parent
TEMPLATE = KAGGLE / "b01_validation_samples.TEMPLATE.json"
DRAFT = KAGGLE / "b01_validation_samples.DRAFT.json"
FINAL = KAGGLE / "b01_validation_samples.json"
INTERFACE_URL = "https://kauai.ccmc.gsfc.nasa.gov/instantrun/iri"

HEADER_RE = re.compile(
    r"yyyy/mmdd\(or -ddd\)/hh\.h\):\s*(\d{4})/\s*-?(\d+)/\s*([\d.]+)UT\s+geog Lat/Long/Alt=\s*([-\d.]+)/\s*([-\d.]+)/\s*([-\d.]+)"
)
HMF2_RE = re.compile(r"hmF2=\s*([\d.]+)")
LIMITS_RE = re.compile(r"from\s+([\d.]+)\s+to\s+([\d.]+)\s*km")


def parse_output(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    m = HEADER_RE.search(text)
    if not m:
        raise SystemExit(f"{path.name}: no run header line found")
    year, doy, hour, lat, lon, alt = m.groups()
    hm = HMF2_RE.search(text)
    if not hm:
        raise SystemExit(f"{path.name}: no hmF2 line found")
    lim = LIMITS_RE.search(text)
    if not lim:
        raise SystemExit(f"{path.name}: no integration-limits line found")
    # the single profile row is the last non-empty line; TEC and t/% are its last two fields
    rows = [ln for ln in lines if ln.strip()]
    data_row = rows[-1].split()
    if len(data_row) < 3:
        raise SystemExit(f"{path.name}: cannot read the profile row {rows[-1]!r}")
    tec_text, top_text = data_row[-2], data_row[-1]
    header_end = next(i for i, ln in enumerate(lines) if ln.strip().startswith("H   ELECTRON"))
    header_block = "\n".join(lines[:header_end]).strip("\n")
    when = dt.datetime(int(year), 1, 1, tzinfo=dt.timezone.utc) + dt.timedelta(
        days=int(doy) - 1, hours=float(hour)
    )
    retrieved = dt.datetime.fromtimestamp(path.stat().st_mtime, tz=dt.timezone.utc)
    return {
        "file": path.name,
        "when": when,
        "lat_rounded": float(lat),
        "lon_rounded": float(lon),
        "alt_km": float(alt),
        "tec_text": tec_text,
        "tec": float(tec_text),
        "top": float(top_text),
        "hmf2_km": float(hm.group(1)),
        "integration_km": (float(lim.group(1)), float(lim.group(2))),
        "header": header_block,
        "retrieved_at_utc": retrieved.replace(microsecond=0).isoformat(),
    }


def main() -> int:
    template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    samples = [dict(s) for s in template["samples"]]
    outputs = [parse_output(p) for p in sorted(HERE.glob("case_*.txt"))]
    used: set[str] = set()
    missing: list[str] = []
    for index, s in enumerate(samples, start=1):
        when = dt.datetime.fromisoformat(s["target_time_utc"])
        match = [
            o
            for o in outputs
            if o["when"] == when
            and abs(o["lat_rounded"] - float(s["lat"])) < 0.051
            and abs(o["lon_rounded"] - float(s["lon"])) < 0.051
            and o["file"] not in used
        ]
        if len(match) != 1:
            missing.append(f"case {index} {s['site']} {s['target_time_utc']}: {len(match)} matching output(s)")
            s.setdefault("official_interface_hmf2_km", None)
            continue
        o = match[0]
        used.add(o["file"])
        s["official_interface_value"] = o["tec"]
        s["official_interface_top"] = o["top"]
        s["official_interface_hmf2_km"] = o["hmf2_km"]
        s["official_interface_header"] = o["header"]
        s["official_interface_source"] = (
            f"CCMC Instant Run, IRI-2016 selected on the form ({INTERFACE_URL}); text output saved as "
            f"kaggle/official_reference_outputs/{o['file']} (retrieved {o['retrieved_at_utc']}, file mtime); "
            f"TEC printed as {o['tec_text']!r} (one decimal); server integration limits "
            f"{o['integration_km'][0]:g}-{o['integration_km'][1]:g} km as echoed in the header"
        )
    result = {"samples": samples}
    DRAFT.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"draft written: {DRAFT.relative_to(KAGGLE.parent)} ({len(used)}/8 cases filled)")
    for line in missing:
        print("  MISSING:", line)
    unused = sorted(set(o["file"] for o in outputs) - used)
    for f in unused:
        print("  UNMATCHED FILE:", f)
    if not missing and not unused:
        FINAL.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"final written: {FINAL.relative_to(KAGGLE.parent)}")
        return 0
    if FINAL.exists():
        print(f"NOTE: {FINAL.name} exists from an earlier complete run and was NOT touched")
    return 1


if __name__ == "__main__":
    sys.exit(main())
