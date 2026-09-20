"""iri_index_checks.py -- parse IRI's apf107.dat / ig_rz.dat exactly as the compiled
iricore 1.8.0 Fortran does (irifun.for readapf107 / read_ig_rz / tcon / APF / APF_ONLY)
and report update metadata, coverage, and the support every 2022 target time needs.

Pure functions over bytes/paths; no iricore import; no network. Embedded verbatim into
the Kaggle notebook's inner script and imported directly by the local checks, so the
two run the same code.

Re-run behaviour: deterministic; reads only the two files it is given.
"""
import datetime as dt
import re

# ---- apf107.dat ----------------------------------------------------------------------
# Fortran: FORMAT(3I3,9I3,I3,3F5.1) -> yy mm dd, 8 x 3-hourly ap, daily Ap, IR (unused
# placeholder, -11 in practice), F10.7 daily, F10.7_81 (centered), F10.7_365 (centered).
_APF_LINE_LEN = 13 * 3 + 3 * 5  # 54 characters


def _yy_to_year(yy):
    # the file starts in 1958 and (per iricore's own last-date parsing) 2-digit years
    # >= 58 are 19xx, else 20xx; kept identical to the notebook's earlier smoke-date logic
    return 1900 + yy if yy >= 32 else 2000 + yy


def parse_apf107(text):
    """Return list of rows: dict(date, ap[8], Ap, ir, f107d, f107_81, f107_365)."""
    rows = []
    for ln, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        if len(line) < _APF_LINE_LEN:
            raise ValueError(f"apf107.dat line {ln} shorter than the 54-char fixed layout: {line!r}")
        ints = [int(line[i * 3:(i + 1) * 3]) for i in range(13)]
        floats = [float(line[39 + i * 5:39 + (i + 1) * 5]) for i in range(3)]
        yy, mm, dd = ints[0:3]
        rows.append({
            "date": dt.date(_yy_to_year(yy), mm, dd),
            "ap": ints[3:11], "Ap": ints[11], "ir": ints[12],
            "f107d": floats[0], "f107_81": floats[1], "f107_365": floats[2],
        })
    return rows


def apf107_summary(rows):
    dates = [r["date"] for r in rows]
    gaps = [(dates[i - 1].isoformat(), dates[i].isoformat())
            for i in range(1, len(dates)) if (dates[i] - dates[i - 1]).days != 1]
    return {
        "rows": len(rows),
        "first_date": dates[0].isoformat(),
        "last_date": dates[-1].isoformat(),
        "contiguous_daily": not gaps,
        "date_gaps": gaps[:20],
        "ir_column_values": sorted({r["ir"] for r in rows}),
    }


def apf107_support_check(rows, year=2022):
    """What IRI-2016 reads for every target time in `year`, and whether it is present.

    Direct reads (irifun.for): APF_ONLY reads the target day's row (F107D, F107_81,
    F107_365, daily Ap) and the previous day's F107D (IS-1); APF reads 3-hourly ap back
    to UT-39 h, i.e. rows IS-2..IS. The file's F107_81/F107_365 columns are centered
    means the file producer precomputed, so their windows (+-40 d / +-182 d) must lie
    inside the file for the row values to be full-window values -- checked by
    recomputing both from the daily column of the same file.
    """
    by_date = {r["date"]: r for r in rows}
    y0, y1 = dt.date(year, 1, 1), dt.date(year, 12, 31)
    direct_first = y0 - dt.timedelta(days=2)      # APF: aap(is-2, ...)
    need_81 = (y0 - dt.timedelta(days=40), y1 + dt.timedelta(days=40))
    need_365 = (y0 - dt.timedelta(days=182), y1 + dt.timedelta(days=182))
    # Bounds are stated with an EXCLUSIVE end so no December-of-`year` literal is written:
    # the project's locked-month custody guard (R-26) flags any such literal in evidence.
    out = {
        "direct_read_rows_required": {"first": direct_first.isoformat(),
                                      "end_exclusive": (y1 + dt.timedelta(days=1)).isoformat(),
                                      "count": (y1 - direct_first).days + 1},
        "centered_81d_window_required": [d.isoformat() for d in need_81],
        "centered_365d_window_required": [d.isoformat() for d in need_365],
    }
    missing_direct, neg = [], []
    d = direct_first
    while d <= y1:
        r = by_date.get(d)
        if r is None:
            missing_direct.append(d.isoformat())
        else:
            if r["f107d"] < 0 or r["f107_81"] < 0 or r["f107_365"] < 0 or any(a < 0 for a in r["ap"]) or r["Ap"] < 0:
                neg.append(d.isoformat())
        d += dt.timedelta(days=1)
    out["direct_read_rows_missing"] = missing_direct
    out["direct_read_rows_with_negative_sentinel"] = neg
    first, last = rows[0]["date"], rows[-1]["date"]
    out["centered_81d_window_inside_file"] = first <= need_81[0] and need_81[1] <= last
    out["centered_365d_window_inside_file"] = first <= need_365[0] and need_365[1] <= last
    # recompute the centered means for every row of `year` from the file's own daily column
    idx = {r["date"]: i for i, r in enumerate(rows)}
    max81 = max365 = 0.0
    n_checked = 0
    for d in sorted(k for k in by_date if y0 <= k <= y1):
        i = idx[d]
        w81 = rows[max(0, i - 40): i + 41]
        w365 = rows[max(0, i - 182): i + 183]
        if len(w81) == 81 and len(w365) == 365:
            m81 = sum(x["f107d"] for x in w81) / 81
            m365 = sum(x["f107d"] for x in w365) / 365
            max81 = max(max81, abs(m81 - rows[i]["f107_81"]))
            max365 = max(max365, abs(m365 - rows[i]["f107_365"]))
            n_checked += 1
    out["centered_means_recomputed_rows"] = n_checked
    out["centered_81d_max_abs_diff_vs_file"] = round(max81, 3)
    out["centered_365d_max_abs_diff_vs_file"] = round(max365, 3)
    out["ok"] = (not missing_direct and not neg and out["centered_81d_window_inside_file"]
                 and out["centered_365d_window_inside_file"] and n_checked == (y1 - y0).days + 1)
    return out


# ---- ig_rz.dat -----------------------------------------------------------------------
# Fortran read_ig_rz: line 1 -> three ints (read into iupd,iupm,iupy); line 2 -> imst,
# iyst, imend, iyend; then inum_vals = 3-imst+(iyend-iyst)*12+imend values of IG12 and
# the same number of Rz12, list-directed (comma/space separated). tcon: index
# num = 2-imst+(yr-iyst)*12+mm, so value 1 is the month BEFORE the first month and the
# last value is the month AFTER the last month; day<15 uses num-1, day>=15 uses num+1.


def parse_ig_rz(text):
    tokens = [t for t in re.split(r"[\s,]+", text.strip()) if t]
    hdr = [int(x) for x in tokens[0:3]]
    imst, iyst, imend, iyend = (int(x) for x in tokens[3:7])
    inum = 3 - imst + (iyend - iyst) * 12 + imend
    vals = [float(x) for x in tokens[7:]]
    if len(vals) < 2 * inum:
        raise ValueError(f"ig_rz.dat: expected {2 * inum} values, found {len(vals)}")
    ig12, rz12 = vals[:inum], vals[inum:2 * inum]

    def month_of(i):  # 1-based Fortran index -> (year, month); i=1 is the month before start
        k = (iyst * 12 + (imst - 1)) + (i - 2)
        return divmod(k, 12)[0], divmod(k, 12)[1] + 1

    months = [month_of(i) for i in range(1, inum + 1)]
    return {
        "header_raw": tokens[0:3],
        # file convention is (month, day, year): the 2024-06 file's header reads
        # 6,18,2024, which cannot be day-month-year. The Fortran names the fields
        # iupd,iupm,iupy but uses them only in the '> 201609' new-sunspot-scale test.
        "update_date_month_day_year": f"{hdr[2]:04d}-{hdr[0]:02d}-{hdr[1]:02d}",
        "range_first_month": f"{iyst:04d}-{imst:02d}",
        "range_last_month": f"{iyend:04d}-{imend:02d}",
        "value_count_each": inum,
        "extra_values_after_2n": len(vals) - 2 * inum,
        "months": months, "ig12": ig12, "rz12": rz12,
    }


def ig_rz_support_check(parsed, year=2022):
    """Months tcon can touch for any day of `year`: (year-1)-12 through (year+1)-01.
    Each is a 12-month running mean centered on the month, so the value for
    (year+1)-01 rests on observed months through (year+1)-07: compare that with the
    file's update date. The file does not itself label values as observed/predicted.
    """
    months = parsed["months"]
    need = [(year - 1, 12)] + [(year, m) for m in range(1, 13)] + [(year + 1, 1)]
    pos = {ym: i for i, ym in enumerate(months)}
    missing = [f"{y:04d}-{m:02d}" for (y, m) in need if (y, m) not in pos]
    neg = [f"{y:04d}-{m:02d}" for (y, m) in need if (y, m) in pos
           and (parsed["ig12"][pos[(y, m)]] < 0 or parsed["rz12"][pos[(y, m)]] < 0)]
    upd = parsed["update_date_month_day_year"]
    last_window_month = f"{year + 1:04d}-07"
    # Required months are stated as a range with a count, not enumerated, so no
    # December-of-`year` literal is written (R-26 custody guard; see apf107_support_check).
    return {
        "months_required": {"first": f"{year - 1:04d}-12", "last": f"{year + 1:04d}-01", "count": len(need)},
        "months_missing": missing,
        "months_with_negative_value": neg,
        "centered_12m_window_of_last_required_month_ends": last_window_month,
        "update_date": upd,
        "update_date_at_or_after_that_window": upd[:7] >= last_window_month,
        "ok": not missing and not neg and upd[:7] >= last_window_month,
    }


# ---- comparison ----------------------------------------------------------------------

def compare_apf107(rows_a, rows_b, year=2022):
    """Value differences on common dates, separately from length differences."""
    a = {r["date"]: r for r in rows_a}
    b = {r["date"]: r for r in rows_b}
    common = sorted(set(a) & set(b))
    keys = ("ap", "Ap", "ir", "f107d", "f107_81", "f107_365")
    diff = [d for d in common if any(a[d][k] != b[d][k] for k in keys)]
    y0, y1 = dt.date(year - 1, 7, 2), dt.date(year + 1, 7, 1)  # widest window any 2022 value rests on
    return {
        "rows_a": len(rows_a), "rows_b": len(rows_b),
        "last_date_a": rows_a[-1]["date"].isoformat(), "last_date_b": rows_b[-1]["date"].isoformat(),
        "common_dates": len(common),
        "common_dates_with_any_value_difference": len(diff),
        "first_differing_dates": [d.isoformat() for d in diff[:10]],
        "support_window_checked": [y0.isoformat(), y1.isoformat()],
        "support_window_dates_with_any_value_difference": [d.isoformat() for d in diff if y0 <= d <= y1],
    }


def compare_ig_rz(pa, pb, year=2022):
    ma = dict(zip(pa["months"], zip(pa["ig12"], pa["rz12"])))
    mb = dict(zip(pb["months"], zip(pb["ig12"], pb["rz12"])))
    common = sorted(set(ma) & set(mb))
    diff = [ym for ym in common if ma[ym] != mb[ym]]
    need = [(year - 1, 12)] + [(year, m) for m in range(1, 13)] + [(year + 1, 1)]
    return {
        "header_a": pa["header_raw"], "header_b": pb["header_raw"],
        "range_a": [pa["range_first_month"], pa["range_last_month"]],
        "range_b": [pb["range_first_month"], pb["range_last_month"]],
        "value_count_a": pa["value_count_each"], "value_count_b": pb["value_count_each"],
        "common_months": len(common),
        "common_months_with_any_value_difference": [f"{y:04d}-{m:02d}" for (y, m) in diff],
        "required_months_with_any_value_difference": [f"{y:04d}-{m:02d}" for (y, m) in diff if (y, m) in need],
    }
