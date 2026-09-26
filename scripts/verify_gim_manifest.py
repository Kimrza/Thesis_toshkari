"""Independently re-verify a GIM acquisition bundle.

Re-hashes every file in --dir against sha256_manifest.json and reports any
mismatch, missing file, or extra file not in the manifest. Also cross-checks
acquisition_log.json entries against the manifest (same filename -> same
hash) so the two records cannot silently drift apart.

Usage:
    python scripts/verify_gim_manifest.py --dir evidence/gim_code_final_2022

Exit code 0 = every file verified; non-zero = at least one integrity
failure, with the specific file and violated expectation printed (project
convention: never continue silently past a failed hash check).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys


def sha256_of_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", required=True)
    args = ap.parse_args()

    manifest_path = os.path.join(args.dir, "sha256_manifest.json")
    log_path = os.path.join(args.dir, "acquisition_log.json")

    if not os.path.exists(manifest_path):
        sys.exit(f"FATAL: {manifest_path} missing -- refusing to verify unmanifested evidence.")

    manifest = json.load(open(manifest_path, encoding="utf-8-sig"))
    failures = []

    on_disk = {
        f for f in os.listdir(args.dir)
        if f not in ("sha256_manifest.json", "acquisition_log.json")
    }

    for filename, expected_hash in manifest.items():
        path = os.path.join(args.dir, filename)
        if not os.path.exists(path):
            failures.append(f"MISSING: {filename} listed in manifest but not on disk")
            continue
        actual = sha256_of_file(path)
        if actual != expected_hash:
            failures.append(
                f"HASH MISMATCH: {filename} expected {expected_hash} got {actual}"
            )
        on_disk.discard(filename)

    for extra in sorted(on_disk):
        failures.append(f"UNMANIFESTED FILE: {extra} present on disk but not in sha256_manifest.json")

    if os.path.exists(log_path):
        log = json.load(open(log_path, encoding="utf-8-sig"))
        for entry in log:
            fname = entry.get("filename")
            if fname not in manifest:
                failures.append(f"LOG/MANIFEST DRIFT: {fname} in acquisition_log.json but not in sha256_manifest.json")
            elif entry.get("sha256") != manifest[fname]:
                failures.append(f"LOG/MANIFEST DRIFT: {fname} hash differs between acquisition_log.json and sha256_manifest.json")
    else:
        failures.append(f"MISSING: {log_path} (per-file provenance log absent)")

    if failures:
        print(f"VERIFICATION FAILED -- {len(failures)} issue(s):", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print(f"VERIFIED: {len(manifest)} files, all hashes match, log and manifest agree.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
