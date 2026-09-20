"""Build the B-01 (IRI-2016 benchmark) Kaggle execution package.

Purpose
-------
Collect the EXACT project files the benchmark path needs on Kaggle -- `src/` (the
adapter `src/external/iri.py` and everything `scripts/04_build_external_products.py`
imports), that stage script, the four governed configs, `requirements.txt` (the
environment lock hashes it), and the fixture manifests the TE 9.2 receipt gate reads --
into one zip with a SHA-256 manifest and the source commit, so the notebook can verify
what it unpacks before running anything. Nothing under `evidence/locked_test_restricted/`
is ever collected (the locked December targets are not an input of this package).

Inputs
------
The working tree. Run from the repository root:

    python kaggle/build_b01_package.py [--out kaggle/dist/tec_b01_package.zip]

Optionally place `kaggle/b01_validation_samples.json` (the 5-10 samples with official
IRI-2016 interface values; see `kaggle/b01_validation_samples.TEMPLATE.json`) beside
this script and it is packaged too.

Re-run behaviour
----------------
Deterministic for a given tree: the manifest lists every packaged file with its
SHA-256; the zip's own hash is printed. Re-running after any edit produces a different
manifest and a different zip hash -- the notebook records both.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN_PREFIXES = ("evidence/locked_test_restricted",)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _collect() -> list[Path]:
    files: list[Path] = []
    files += sorted(p for p in (REPO_ROOT / "src").rglob("*.py") if "__pycache__" not in p.parts)
    # every stage script + the walking-skeleton orchestrator: the fixture runs invoke the
    # seven Phase 1 stage scripts as subprocesses (TE 13.2 order)
    files += sorted(p for p in (REPO_ROOT / "scripts").glob("*.py"))
    files += sorted((REPO_ROOT / "configs").glob("*.yaml"))
    files.append(REPO_ROOT / "requirements.txt")
    files.append(REPO_ROOT / "pyproject.toml")
    # tests: the plumbing fixture runs the M10 contract fixture (two pytest modules) and the
    # fixture trees hold the identity declarations / frozen manifests the gate reads
    files += sorted(
        p for p in (REPO_ROOT / "tests").rglob("*") if p.is_file() and "__pycache__" not in p.parts
    )
    # fixture inputs, as the identity declarations cite them: the November 2022 acquisition
    # evidence, the driver audits (classes 1-5 of the custody scan; driver content only),
    # and the decision register the skeleton asserts fixture identity against
    for sub in ("audit_evidence_2022-11", "audit_ec1_2026-08-15", "audit_gfz_2026-09-18"):
        files += sorted(p for p in (REPO_ROOT / "evidence" / sub).rglob("*") if p.is_file())
    files.append(REPO_ROOT / "evidence" / "DECISIONS.md")
    samples = REPO_ROOT / "kaggle" / "b01_validation_samples.json"
    if samples.is_file():
        files.append(samples)
    files.append(REPO_ROOT / "kaggle" / "b01_validation_samples.TEMPLATE.json")
    for f in files:
        rel = f.relative_to(REPO_ROOT).as_posix()
        if rel.startswith(FORBIDDEN_PREFIXES):
            raise SystemExit(f"refusing to package {rel}: locked-test material is never an input")
    return files


def _git_commit() -> str:
    try:
        # fixed argv, no user input; git on PATH is the documented precondition
        git = ["git", "-C", str(REPO_ROOT)]
        out = subprocess.run(
            [*git, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        dirty = subprocess.run(
            [*git, "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        return out + ("+dirty" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        return "unknown (no git tree)"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--out", type=Path, default=REPO_ROOT / "kaggle" / "dist" / "tec_b01_package.zip"
    )
    args = parser.parse_args(argv)
    files = _collect()
    manifest = {
        "package": "tec_b01_package",
        "built_at_utc": dt.datetime.now(dt.UTC).isoformat(),
        "source_commit": _git_commit(),
        "builder_python": sys.version.split()[0],
        "files": {f.relative_to(REPO_ROOT).as_posix(): _sha256(f) for f in files},
        "excluded_by_rule": list(FORBIDDEN_PREFIXES),
    }
    # one identifier for the packaged working-tree content, independent of HEAD: the hash of
    # the sorted "path:sha256" lines (uncommitted edits change it; the commit does not)
    manifest["tree_sha256"] = hashlib.sha256(
        "\n".join(f"{k}:{v}" for k, v in sorted(manifest["files"].items())).encode("utf-8")
    ).hexdigest()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, f.relative_to(REPO_ROOT).as_posix())
        zf.writestr("package_manifest.json", json.dumps(manifest, indent=2) + "\n")
    print(
        f"wrote {args.out} ({len(files)} files) zip sha256 {_sha256(args.out)} "
        f"tree sha256 {manifest['tree_sha256']} commit {manifest['source_commit']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
