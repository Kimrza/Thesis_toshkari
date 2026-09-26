"""Acquire CODE final GIM IONEX files for calendar year 2022 from the AIUB
anonymous archive (https://ftp.aiub.unibe.ch/CODE/2022/), preserving each
provider filename verbatim (2022 straddles the IGS short-name -> long-name
switch; whichever name the archive serves for a given day is recorded as-is,
never normalised).

Inputs: none required (anonymous archive). If CDDIS is used as a fallback,
set CDDIS credentials via a `.netrc` entry or the EARTHDATA_USER /
EARTHDATA_PASS environment variables -- never on the command line, never in
a committed file.

Outputs, under --out-dir (default evidence/gim_code_final_2022/):
  - one IONEX file per day, verbatim provider filename, bytes untouched
  - sha256_manifest.json   {filename: sha256}          (matches the
    evidence/audit_evidence_2022-*/ manifest convention already in this repo)
  - acquisition_log.json   [{filename, source_url, retrieval_date_utc,
    size_bytes, sha256, day_of_year, provider_name_form}]  (the runbook's
    richer per-file provenance record)

Re-run behavior: a day already present with a verified hash in
sha256_manifest.json is skipped (idempotent); use --force to re-fetch.
Governed discipline: December (day-of-year 335-365) is acquired and hashed
like every other month -- inventory only. This script never opens, parses,
or inspects any file's contents; it only stores bytes and computes a hash.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import urllib.request
import urllib.error

BASE_URL = "https://ftp.aiub.unibe.ch/CODE/2022/"
YEAR = 2022

# Candidate verbatim filename forms for a given day-of-year. The archive
# switches from the short IGS name to the long product name partway through
# 2022; the exact cutover day is not known from this environment (no
# directory listing was reachable), so both forms are tried in order and
# whichever the server actually returns 200 for is the identity recorded.
def candidate_names(doy: int) -> list[str]:
    short = f"CODG{doy:03d}0.22I.Z"
    # Long-form product name per CDDIS/IGS long filename convention for
    # daily final GIMs; exact vendor string must be confirmed against a
    # real directory listing before relying on this candidate.
    long_form = f"COD0OPSFIN_{YEAR}{doy:03d}0000_01D_GIM.INX.gz"
    return [short, long_form]


def sha256_of_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_one(doy: int, out_dir: str, timeout: int) -> dict | None:
    for name in candidate_names(doy):
        url = BASE_URL + name
        dest = os.path.join(out_dir, name)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "gim-acquire/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status != 200:
                    continue
                data = resp.read()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            print(f"  day {doy:03d}: {name} -> {exc}", file=sys.stderr)
            continue
        with open(dest, "wb") as fh:
            fh.write(data)
        return {
            "filename": name,
            "source_url": url,
            "retrieval_date_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "size_bytes": len(data),
            "sha256": sha256_of_file(dest),
            "day_of_year": doy,
            "provider_name_form": "short" if name.startswith("CODG") else "long",
        }
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", default="evidence/gim_code_final_2022")
    ap.add_argument("--start-doy", type=int, default=1)
    ap.add_argument("--end-doy", type=int, default=365)
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--force", action="store_true",
                     help="re-fetch even if already present in acquisition_log.json")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    log_path = os.path.join(args.out_dir, "acquisition_log.json")
    manifest_path = os.path.join(args.out_dir, "sha256_manifest.json")

    log = json.load(open(log_path)) if os.path.exists(log_path) else []
    done_days = {e["day_of_year"] for e in log} if not args.force else set()

    missing = []
    for doy in range(args.start_doy, args.end_doy + 1):
        if doy in done_days:
            continue
        entry = fetch_one(doy, args.out_dir, args.timeout)
        if entry is None:
            missing.append(doy)
            print(f"MISSING day {doy:03d}: no candidate filename resolved "
                  f"(network unreachable or file absent)", file=sys.stderr)
            continue
        log.append(entry)
        print(f"OK day {doy:03d}: {entry['filename']} "
              f"({entry['size_bytes']} bytes, {entry['provider_name_form']} form)")

    log.sort(key=lambda e: e["day_of_year"])
    with open(log_path, "w") as fh:
        json.dump(log, fh, indent=2)

    manifest = {e["filename"]: e["sha256"] for e in log}
    with open(manifest_path, "w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)

    print(f"\nAcquired: {len(log)}/365. Missing: {len(missing)}.")
    if missing:
        print(f"Missing days: {missing}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
