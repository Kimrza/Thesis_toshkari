"""Discriminating-power check for the B-01 tolerance: how much does TEC move under each
configuration mismatch the R-59 validation exists to catch? Same non-December, non-R-59
profile set as the convergence check; the pinned iricore 1.8.0 wheel.

Variants (relative to the adapter's call: version=16, jf='default_edens', 90-2000 km, 0.5 km):
  hmF2_AMTB        : jf(39)=F, jf(40)=T  (the CCMC form DEFAULT; IRI-2016 standard is Shubin)
  hmF2_M3000F2     : jf(39)=T            (old hmF2 from M3000F2)
  foF2_CCIR        : jf(5)=T             (CCIR instead of URSI-88)
  B0_Bil2000       : jf(4)=T             (Bil-2000 thickness instead of ABT-2009)
  no_foF2_storm    : jf(26)=F            (storm model off)
  topside_IRI01corr: jf(29)=T, jf(30)=F  (IRI-2001 corrected topside instead of NeQuick)
  version_2020     : version=20
  htop_1000        : htop=1000 km (ceiling mismatch)
Fortran jf(k) <-> python index k-1.
"""
import datetime as dt
import json
import sys
import time
import warnings

import numpy as np
import iricore
from iricore.iri_flags import get_jf

warnings.simplefilter("ignore")
STATIONS = {"ARUC": (40.286, 44.086), "BSHM": (32.778987, 35.022987), "NICO": (35.140989, 33.396450)}
DAYS = ["2022-01-08", "2022-03-14", "2022-04-15", "2022-06-21", "2022-08-05", "2022-09-05", "2022-09-23", "2022-11-16"]
HOURS = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]


def jf_with(**changes):
    jf = get_jf("default_edens").copy()
    for k, v in changes.items():  # k like 'f39' -> Fortran jf(39)
        jf[int(k[1:]) - 1] = 1 if v else 0
    return jf


VARIANTS = {
    "hmF2_AMTB": dict(jf=jf_with(f39=False, f40=True)),
    "hmF2_M3000F2": dict(jf=jf_with(f39=True, f40=True)),
    "foF2_CCIR": dict(jf=jf_with(f5=True)),
    "B0_Bil2000": dict(jf=jf_with(f4=True, f31=False)),
    "no_foF2_storm": dict(jf=jf_with(f26=False)),
    "topside_IRI01corr": dict(jf=jf_with(f29=True, f30=False)),
    "version_2020": dict(version=20),
    "htop_1000": dict(htop=1000),
}


def main():
    t0 = time.time()
    rows = []
    for day in DAYS:
        for hour in HOURS:
            when = dt.datetime.fromisoformat(day).replace(hour=hour)
            for sid, (lat, lon) in STATIONS.items():
                base = float(iricore.vtec(when, lat, lon, hbot=90, htop=2000, hstep=0.5, version=16))
                row = {"station": sid, "utc": when.isoformat(), "adapter_tecu": base}
                for name, kw in VARIANTS.items():
                    args = dict(hbot=90, htop=2000, hstep=0.5, version=16)
                    args.update(kw)
                    row[name] = float(iricore.vtec(when, lat, lon, **args))
                rows.append(row)
                print(sid, when, f"{base:.3f}", {k: round(row[k] - base, 3) for k in VARIANTS}, flush=True)
    base = np.array([r["adapter_tecu"] for r in rows])
    summary = {}
    for name in VARIANTS:
        d = np.array([r[name] for r in rows]) - base
        ad = np.abs(d)
        summary[name] = {"abs_min": float(ad.min()), "abs_median": float(np.median(ad)), "abs_max": float(ad.max()),
                         "share_abs_gt_1p0": float((ad > 1.0).mean()), "share_abs_gt_0p5": float((ad > 0.5).mean()),
                         "share_abs_gt_0p25": float((ad > 0.25).mean()), "signed_mean": float(d.mean())}
    out = {"kind": "b01_mismatch_sensitivity", "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
           "profiles": len(rows), "not_the_r59_cases": True, "december_records_read": False,
           "environment": {"python": sys.version, "iricore": "1.8.0 pinned wheel, Linux x86_64 via WSL2"},
           "summary": summary, "rows": rows, "elapsed_s": time.time() - t0}
    json.dump(out, open(sys.argv[1], "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
