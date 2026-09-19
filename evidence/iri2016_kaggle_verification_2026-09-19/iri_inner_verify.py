
"""iri_inner_verify.py -- runs INSIDE the isolated venv (or the kernel env if it already
matched, per the notebook's strategy decision). Does the actual iricore
import/provenance/smoke-test/repeatability/index-hash work and prints ONE JSON object to
stdout. Never touches GNSS/VTEC target data; never runs a full-year benchmark; the
smoke test is a single permitted point evaluation at a real, approved station
coordinate and a synthetic non-December timestamp -- diagnostic only.
"""
import datetime as dt
import hashlib
import importlib.metadata
import json
import math
import re
import sys
import traceback
from pathlib import Path

OUT = {"ok": False}


def fail(stage, exc):
    OUT["ok"] = False
    OUT["failed_stage"] = stage
    OUT["exception"] = "".join(traceback.format_exception_only(type(exc), exc)).strip()
    print(json.dumps(OUT, default=str))
    sys.exit(1)


try:
    OUT["python"] = {
        "version": sys.version,
        "executable": sys.executable,
    }

    # --- 1. import and provenance -----------------------------------------------------
    OUT["_stage"] = "import_iricore"
    import iricore  # noqa: E402

    OUT["iricore_import_path"] = str(Path(iricore.__file__).resolve())
    try:
        OUT["iricore_version_dist"] = importlib.metadata.version("iricore")
    except importlib.metadata.PackageNotFoundError:
        OUT["iricore_version_dist"] = None
    OUT["iricore_version_attr"] = getattr(iricore, "__version__", None)

    from iricore.config import DEFAULT_IRI_VERSION  # noqa: E402

    OUT["installed_default_iri_version"] = DEFAULT_IRI_VERSION
    # Reconciliation vs the earlier source inspection (CR-2026-09-19-SCI-DECISIONS §3):
    # the wrapper's own default was IRI-2020, not IRI-2016 -- this notebook's smoke test
    # explicitly passes version=16 below and never relies on the default. A mismatch here
    # (e.g. an installed release that flipped the default to 16) is reported, not hidden,
    # because it would change what "explicit version=16" is guarding against.
    OUT["reconciliation"] = {
        "expected_default_from_source_inspection": 20,
        "installed_default_matches_expectation": DEFAULT_IRI_VERSION == 20,
    }

    # --- 2. locate and hash the shipped index files (D-45: pin by hash, detect drift) -
    OUT["_stage"] = "locate_and_hash_index_files_before"
    index_dir = Path(iricore.__file__).resolve().parent / "data" / "index"
    apf107 = index_dir / "apf107.dat"
    ig_rz = index_dir / "ig_rz.dat"
    if not apf107.is_file() or not ig_rz.is_file():
        raise RuntimeError(f"expected index files not found under {index_dir}")

    def sha256_of(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    hashes_before = {"apf107.dat": sha256_of(apf107), "ig_rz.dat": sha256_of(ig_rz)}
    OUT["index_files"] = {"directory": str(index_dir), "sha256_before": hashes_before}

    # --- 3. pick a safe, non-December, well-inside-coverage smoke-test date -----------
    # Parsed from the file's OWN records (13I3,3F5.1 fixed layout) rather than assumed,
    # so the choice is correct for whatever release is actually installed.
    OUT["_stage"] = "parse_apf107_coverage_and_pick_smoke_date"
    last_line = None
    with apf107.open("r", encoding="ascii", errors="strict") as fh:
        for line in fh:
            if line.strip():
                last_line = line
    if last_line is None:
        raise RuntimeError("apf107.dat has no data lines")
    m = re.match(r"\s*(\d{2})\s*(\d{1,2})\s*(\d{1,2})", last_line)
    if not m:
        raise RuntimeError(f"could not parse the last apf107.dat line: {last_line!r}")
    yy, mm, dd = (int(x) for x in m.groups())
    last_year = 1900 + yy if yy >= 32 else 2000 + yy
    last_date = dt.date(last_year, mm, dd)
    # 60 days back from the file's own last covered date, walked to a non-December day.
    candidate = last_date - dt.timedelta(days=60)
    while candidate.month == 12:
        candidate -= dt.timedelta(days=30)
    smoke_time = dt.datetime(candidate.year, candidate.month, candidate.day, 12, 0, 0)
    OUT["index_files"]["last_covered_date_in_apf107"] = last_date.isoformat()
    OUT["smoke_test_timestamp_utc"] = smoke_time.isoformat()
    assert smoke_time.month != 12, "smoke-test date must not be in December (project convention)"

    # --- 4. the approved integration settings -----------------------------------------
    # htop = 2000 km is the ONLY altitude-ceiling value TE/Vision freeze (Vision §6.11,
    # "explicit 2000 km altitude ceiling"). hbot and hstep are NOT frozen by the project;
    # this smoke test uses iricore's OWN wrapper defaults for them, disclosed as such --
    # never invented as if they were approved values.
    ARUC_LAT, ARUC_LON = 40.286, 44.086  # D-1's frozen ARUC station coordinate (public
    # station metadata, NOT a GNSS/VTEC target value; no target data is read here)
    HBOT_KM, HTOP_KM, HSTEP_KM = 90.0, 2000.0, 0.5  # HTOP frozen; HBOT/HSTEP = wrapper defaults
    IRI_VERSION = 16  # explicit -- the installed default is 20 (IRI-2020), never relied on
    OUT["integration_settings"] = {
        "lat": ARUC_LAT,
        "lon": ARUC_LON,
        "station": "ARUC (D-1 frozen coordinate; coordinate only, no target data read)",
        "hbot_km": HBOT_KM,
        "htop_km": HTOP_KM,
        "htop_km_is_te_vision_frozen": True,
        "hstep_km": HSTEP_KM,
        "hstep_km_is_frozen": False,
        "hbot_km_is_frozen": False,
        "iri_version_requested": IRI_VERSION,
        "iri_version_is_default": False,
        "output_unit": "TECU (verified from iricore.tec._integrate_ne: sums Ne*step_km, "
        "converts km->m (*1e3) then to TECU (*1e-16))",
    }

    # --- 5. the smoke test itself, called TWICE for repeatability ---------------------
    OUT["_stage"] = "smoke_test_call_1"
    first = iricore.vtec(
        smoke_time, ARUC_LAT, ARUC_LON, hbot=HBOT_KM, htop=HTOP_KM, hstep=HSTEP_KM,
        version=IRI_VERSION,
    )
    OUT["_stage"] = "smoke_test_call_2_repeatability"
    second = iricore.vtec(
        smoke_time, ARUC_LAT, ARUC_LON, hbot=HBOT_KM, htop=HTOP_KM, hstep=HSTEP_KM,
        version=IRI_VERSION,
    )
    first_val = float(first[0] if hasattr(first, "__len__") else first)
    second_val = float(second[0] if hasattr(second, "__len__") else second)
    finite = math.isfinite(first_val) and math.isfinite(second_val)
    physically_plausible = 0.0 <= first_val <= 200.0  # iricore's own internal sanity bound
    repeatable = first_val == second_val
    OUT["smoke_test"] = {
        "call_1_tecu": first_val,
        "call_2_tecu": second_val,
        "finite": finite,
        "physically_plausible_0_to_200_tecu": physically_plausible,
        "repeatable_bit_identical": repeatable,
    }
    if not finite:
        raise RuntimeError(f"non-finite smoke-test output: {first_val!r}, {second_val!r}")
    if not repeatable:
        raise RuntimeError(
            f"repeated identical call produced different output: {first_val!r} != {second_val!r}"
        )
    if not physically_plausible:
        # NOT fatal by itself (iricore only warns at this same bound) -- but it IS a
        # material mismatch worth failing loudly rather than reporting a quiet PASS.
        raise RuntimeError(
            f"smoke-test output {first_val!r} TECU outside iricore's own plausibility "
            f"bound [0, 200]; reported as a material mismatch, not silently accepted"
        )

    # --- 6. index files must be byte-identical after the calls (no silent refresh) ----
    OUT["_stage"] = "hash_index_files_after"
    hashes_after = {"apf107.dat": sha256_of(apf107), "ig_rz.dat": sha256_of(ig_rz)}
    OUT["index_files"]["sha256_after"] = hashes_after
    OUT["index_files"]["unchanged_after_smoke_test"] = hashes_before == hashes_after
    if hashes_before != hashes_after:
        raise RuntimeError(
            f"index file hash changed after the smoke-test calls (silent update "
            f"detected): before={hashes_before} after={hashes_after}"
        )

    OUT["_stage"] = "done"
    OUT["ok"] = True
    print(json.dumps(OUT, default=str))
except Exception as exc:  # noqa: BLE001 -- this script's whole job is to report, never crash silently
    fail(OUT.get("_stage", "unspecified"), exc)
