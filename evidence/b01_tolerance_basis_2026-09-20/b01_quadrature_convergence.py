"""Independent numerical convergence check of the B-01 adapter's TEC quadrature.

Runs the EXACT pinned `iricore==1.8.0` Linux wheel (index files apf107.dat / ig_rz.dat at the
D-45 pinned hashes) on non-December 2022 profiles that are NOT the eight R-59 validation cases,
and measures, per profile:

  adapter      : iricore.vtec(hbot=90, htop=2000, hstep=0.5, version=16)  -- as the project calls it
  ref_int      : reference integral of the same IRI-2016 Ne(h) profile, 90-2000 km, composite
                 Simpson on a 0.1 km grid (adapter grid refined 5x) -- the "converged" value
  ref_int_100  : the same reference integral from 100 km (iri_tec's fixed hr(1)=100 start)
  lower_90_100 : reference integral 90-100 km   (what a 100-km start omits)
  lower_65_90  : reference integral 65-90 km    (what the form's default tecLower=65 would ADD)
  iritec_0/1/2 : emulation of IRI's own iri_tec(hstart=90, hend=2000, istep) midpoint scheme
                 (iritec.for in the wheel's own sources): segment steps
                 istep=1: 2.0/1.0/2.5/10/30 km over 100..hmF2-10..hmF2+10..hmF2+150..hmF2+250..2000
                 istep=2: 1.0/0.5/1.0/1.0/1.0 km; istep=0: 2.0/1.0/2.5/5 km + exponential topside
                 approximation above hmF2+250 (the 3-segment log-linear formula), with the
                 topside clamp Ne<=NmF2 above hmF2, Ne sampled at each segment MIDPOINT by IRI-2016.
  clean_effect : adapter value minus the plain 0.5-km rectangle sum without iricore's
                 `_clean_ne_for_tec` step (isolates that step's contribution)

Nothing here touches the eight validation cases, any official value, or any December record.
Outputs a JSON with every per-profile number and a summary of |adapter - X| statistics.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
import time

import numpy as np
import iricore
from iricore.iri_flags import get_jf
from iricore.tec import _clean_ne_for_tec, _integrate_ne

STATIONS = {  # D-1 coordinates, as transcribed in configs/data.yaml
    "ARUC": (40.286, 44.086),
    "BSHM": (32.778987, 35.022987),
    "NICO": (35.140989, 33.396450),
}
# Convergence set: NOT the eight R-59 cases (those are 2022-01-07, 03-13, 09-04, 08-04, 11-17,
# 04-14 at specific hours). Neighbouring days spanning quiet/disturbed, day/night, four seasons.
DAYS = ["2022-01-08", "2022-03-14", "2022-04-15", "2022-06-21", "2022-08-05", "2022-09-05",
        "2022-09-23", "2022-11-16"]
HOURS = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
JF = get_jf("default_edens")  # what iricore.vtec uses when jf is not given


def ne_on_grid(when, lat, lon, hbot, htop, hstep, zero_nonfinite=False):
    """Ne(h) sampled by IRI-2016 at hbot, hbot+hstep, ..., <= htop (chunks of <=1000 points)."""
    heights = np.round(np.arange(hbot, htop + hstep / 2, hstep), 6)
    out = np.empty(heights.size)
    oarr = None
    i = 0
    while i < heights.size:
        chunk = heights[i:i + 990]
        res = iricore.iri(when, [float(chunk[0]), float(chunk[-1]) + hstep, hstep], lat, lon, 16, JF.copy())
        ed = np.asarray(res.edens).reshape(-1)[: chunk.size]
        out[i:i + chunk.size] = ed
        if oarr is None:
            oarr = np.asarray(res.oarr).reshape(-1)
        i += 990
    if not np.all(np.isfinite(out)):
        if not zero_nonfinite:
            raise RuntimeError(f'non-finite Ne on grid at {heights[~np.isfinite(out)][:5]}')
        out = np.where(np.isfinite(out), out, 0.0)
    return heights, out, oarr


def simpson(y, h):
    n = y.size
    if n % 2 == 0:  # composite Simpson needs an odd count; trapezoid on the last panel
        s = simpson(y[:-1], h) + h * (y[-2] + y[-1]) / 2
        return s
    return h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())


def tecu(integral_m3_km):
    return integral_m3_km * 1e3 * 1e-16


def ne_at(when, lat, lon, heights):
    """Ne at arbitrary heights: one IRI call per distinct step pattern is impossible, so call per
    contiguous equal-step run (segments have a constant step, so one call per segment)."""
    heights = np.asarray(heights, dtype=float)
    if heights.size == 0:
        return np.array([])
    step = float(heights[1] - heights[0]) if heights.size > 1 else 1.0
    out = np.empty(heights.size)
    i = 0
    while i < heights.size:
        chunk = heights[i:i + 990]
        if chunk.size == 1:
            res = iricore.iri(when, [float(chunk[0]), float(chunk[0]) + step, step], lat, lon, 16, JF.copy())
            out[i] = np.asarray(res.edens).reshape(-1)[0]
        else:
            res = iricore.iri(when, [float(chunk[0]), float(chunk[-1]) + step, step], lat, lon, 16, JF.copy())
            out[i:i + chunk.size] = np.asarray(res.edens).reshape(-1)[: chunk.size]
        i += 990
    if not np.all(np.isfinite(out)):
        raise RuntimeError(f'non-finite Ne at {heights[~np.isfinite(out)][:5]}')
    return out


def iritec_emulation(when, lat, lon, hmf2, nmf2, hstart, hend, istep):
    """iri_tec (iritec.for, IRI-2016 as shipped in iricore 1.8.0), midpoint rule per segment.
    Returns TECU. Emulates: hr = [100, hmf2-10, hmf2+10, hmf2+150, hmf2+250, hend] (clipped to
    hend); start at max(hstart, hr(i)) by the 'find the starting point' loop; step(i) per istep;
    the last panel of each segment shortened to land on hu; topside clamp yne<=NmF2 for hx>hmf2;
    istep=0 exponential approximation above hr(4)."""
    hr = [100.0, hmf2 - 10.0, hmf2 + 10.0, hmf2 + 150.0, hmf2 + 250.0, hend]
    for i in range(1, 6):
        if hr[i] > hend:
            hr[i] = hend
    steps = {0: [2.0, 1.0, 2.5, 5.0, None], 1: [2.0, 1.0, 2.5, 10.0, 30.0], 2: [1.0, 0.5, 1.0, 1.0, 1.0]}[istep]
    expo = istep == 0 and hend > hr[4]
    # find the starting point (Fortran loop: hr(i)=hstart while hstart > hr(i))
    ia = 0
    i = 0
    while True:
        if hstart > hr[i]:
            hr[i] = hstart
            ia = i
            i += 1
            continue
        break
    # walk the panels exactly as the Fortran does, collecting (hx, delx) pairs per segment
    panels = []  # (hx, delx)
    i = ia
    h = hr[i]
    hu = hr[i + 1]
    delx = steps[i]
    while True:
        h = h + delx
        hh = h
        if h >= hu:
            delx2 = hu - h + delx
            hx = hu - delx2 / 2.0
            panels.append((hx, delx2))
            i += 1
            if i < 5:
                h = hr[i]
                hu = hr[i + 1]
                delx = steps[i]
        else:
            hx = h - delx / 2.0
            panels.append((hx, delx))
        if expo and hh >= hr[3]:
            break
        if not (hh < hend and i < 5):
            break
    hx = np.array([p[0] for p in panels])
    dx = np.array([p[1] for p in panels])
    # sample Ne at the midpoints; group by equal step so each group is one IRI call
    yne = np.empty(hx.size)
    start = 0
    while start < hx.size:
        end = start
        while end + 1 < hx.size and abs(dx[end + 1] - dx[start]) < 1e-9 and abs((hx[end + 1] - hx[end]) - dx[start]) < 1e-6:
            end += 1
        yne[start:end + 1] = ne_at(when, lat, lon, hx[start:end + 1])
        start = end + 1
    above = hx > hmf2
    yne = np.where(above & (yne > nmf2), nmf2, yne)
    total = float(np.sum(yne * dx))  # m^-3 * km
    if expo:
        hei_top, hei_end = hr[3], hend
        top_end = hei_end - hei_top
        num_step = 3
        del_hei = top_end / num_step
        xntop = float(ne_at(when, lat, lon, [hei_end])[0]) / nmf2
        if xntop > 0.9999:
            ss_t = top_end
        else:
            hei_2 = hei_top
            hei_3 = hei_2 + del_hei
            hei_4 = hei_3 + del_hei
            hei_5 = hei_end
            hss = top_end / 4.0
            xkk = np.exp(-top_end / hss) - 1.0
            x_2 = hei_2
            x_3 = hei_top - hss * np.log(xkk * (hei_3 - hei_top) / top_end + 1.0)
            x_4 = hei_top - hss * np.log(xkk * (hei_4 - hei_top) / top_end + 1.0)
            x_5 = hei_end
            ed = [min(float(ne_at(when, lat, lon, [x])[0]) / nmf2, 1.0) for x in (x_2, x_3, x_4)]
            ed_2, ed_3, ed_4 = ed
            ed_5 = xntop

            def seg(e_a, e_b, x_a, x_b):
                if e_b == e_a:
                    return e_b * (x_b - x_a)
                return (e_b - e_a) * (x_b - x_a) / np.log(e_b / e_a)

            ss_t = seg(ed_2, ed_3, x_2, x_3) + seg(ed_3, ed_4, x_3, x_4) + seg(ed_4, ed_5, x_4, x_5)
        total += ss_t * nmf2
    return tecu(total)


def main():
    t0 = time.time()
    rows = []
    for day in DAYS:
        for hour in HOURS:
            when = dt.datetime.fromisoformat(day).replace(hour=hour)
            for sid, (lat, lon) in STATIONS.items():
                adapter = float(iricore.vtec(when, lat, lon, hbot=90, htop=2000, hstep=0.5, version=16))
                # plain rectangle sum WITHOUT the clean step, on the adapter's own 4-stage grid
                # (replicates vtec's stage_ranges so the sample set is identical)
                hbot, htop, hstep = 90.0, 2000.0, 0.5
                npoints = int(np.ceil((htop - hbot) / hstep))
                nstages = int(np.ceil(npoints / 1000))
                ranges = [[hbot + hstep * (1000 * i), hbot + hstep * (1000 * (i + 1) - 1), hstep] for i in range(nstages)]
                ranges[-1][1] = htop
                raw_sum = 0.0
                cleaned_sum = 0.0
                for rg in ranges:
                    res = iricore.iri(when, rg, lat, lon, 16, JF.copy())
                    ed = np.asarray(res.edens).reshape(-1)
                    raw_sum += float(np.sum(ed * hstep))
                    cleaned_sum += float(_integrate_ne(_clean_ne_for_tec(ed.copy()), hstep))
                raw_rect = tecu(raw_sum)
                # reference: 0.1 km grid, Simpson, 90-2000 and 100-2000, plus the two lower bands
                h, ne, oarr = ne_on_grid(when, lat, lon, 90.0, 2000.0, 0.1)
                ref = tecu(simpson(ne, 0.1))
                m100 = h >= 100.0 - 1e-9
                ref_100 = tecu(simpson(ne[m100], 0.1))
                lower_90_100 = tecu(simpson(ne[h <= 100.0 + 1e-9], 0.1))
                h2, ne2, _ = ne_on_grid(when, lat, lon, 65.0, 90.0, 0.1, zero_nonfinite=True)  # night D-region: IRI returns non-finite below ~80 km; counted as 0 (upper bound on the band)
                lower_65_90 = tecu(simpson(ne2, 0.1))
                nmf2, hmf2 = float(oarr[0]), float(oarr[1])
                it = {k: iritec_emulation(when, lat, lon, hmf2, nmf2, 90.0, 2000.0, k) for k in (0, 1, 2)}
                rows.append({
                    "station": sid, "utc": when.isoformat(), "lat": lat, "lon": lon,
                    "hmF2_km": hmf2, "NmF2_m3": nmf2,
                    "adapter_tecu": adapter, "cleaned_rect_tecu": cleaned_sum, "raw_rect_tecu": raw_rect,
                    "ref_simpson_0p1km_90_2000": ref, "ref_simpson_0p1km_100_2000": ref_100,
                    "lower_90_100_tecu": lower_90_100, "lower_65_90_tecu": lower_65_90,
                    "iritec_istep0_from100": it[0], "iritec_istep1_from100": it[1], "iritec_istep2_from100": it[2],
                })
                r = rows[-1]
                print(f"{sid} {when:%Y-%m-%d %H}UT adapter={adapter:8.4f} ref={ref:8.4f} d_ref={adapter-ref:+.4f} "
                      f"d_it1={adapter-it[1]:+.4f} d_it2={adapter-it[2]:+.4f} d_it0={adapter-it[0]:+.4f} "
                      f"low90_100={lower_90_100:.4f} low65_90={lower_65_90:.4f} clean={adapter-raw_rect:+.4f}",
                      flush=True)
    def stats(key_a, key_b):
        d = np.array([r[key_a] - r[key_b] for r in rows])
        return {"n": int(d.size), "mean": float(d.mean()), "min": float(d.min()), "max": float(d.max()),
                "abs_max": float(np.abs(d).max()), "abs_p95": float(np.percentile(np.abs(d), 95))}
    summary = {
        "profiles": len(rows),
        "adapter_tecu_range": [float(min(r["adapter_tecu"] for r in rows)), float(max(r["adapter_tecu"] for r in rows))],
        "adapter_minus_ref_90_2000": stats("adapter_tecu", "ref_simpson_0p1km_90_2000"),
        "adapter_minus_ref_100_2000": stats("adapter_tecu", "ref_simpson_0p1km_100_2000"),
        "adapter_minus_iritec_istep0_from100": stats("adapter_tecu", "iritec_istep0_from100"),
        "adapter_minus_iritec_istep1_from100": stats("adapter_tecu", "iritec_istep1_from100"),
        "adapter_minus_iritec_istep2_from100": stats("adapter_tecu", "iritec_istep2_from100"),
        "iritec_istep1_minus_ref_100_2000": stats("iritec_istep1_from100", "ref_simpson_0p1km_100_2000"),
        "iritec_istep2_minus_ref_100_2000": stats("iritec_istep2_from100", "ref_simpson_0p1km_100_2000"),
        "iritec_istep0_minus_ref_100_2000": stats("iritec_istep0_from100", "ref_simpson_0p1km_100_2000"),
        "clean_step_effect_adapter_minus_raw_rect": stats("adapter_tecu", "raw_rect_tecu"),
        "lower_90_100": {"min": float(min(r["lower_90_100_tecu"] for r in rows)), "max": float(max(r["lower_90_100_tecu"] for r in rows))},
        "lower_65_90": {"min": float(min(r["lower_65_90_tecu"] for r in rows)), "max": float(max(r["lower_65_90_tecu"] for r in rows))},
        "adapter_reproduces_cleaned_rect_bitwise": all(r["adapter_tecu"] == r["cleaned_rect_tecu"] for r in rows),
        "elapsed_s": time.time() - t0,
    }
    out = {"kind": "b01_quadrature_convergence_check", "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
           "not_the_r59_cases": True, "december_records_read": False,
           "environment": {"python": sys.version, "iricore": "1.8.0 (pinned wheel, Linux x86_64 via WSL2)"},
           "settings": {"stations": STATIONS, "days": DAYS, "hours_utc": HOURS, "jf": "default_edens (iricore.vtec default)",
                        "adapter": {"hbot": 90, "htop": 2000, "hstep": 0.5, "version": 16}},
           "summary": summary, "profiles": rows}
    json.dump(out, open(sys.argv[1], "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
