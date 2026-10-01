#!/usr/bin/env bash
# environment/bootstrap_b01.sh -- rebuild environment (b), `b01_iri`, on WSL2 Ubuntu from
# its two hashed linux-64 locks.
#
# Purpose: D-83 R6-5 "PV-03 Rec 12 execution plan" step 3 (a hashed requirements file for
#   `b01_iri`, then a reinstall with --require-hashes) and section R5-5 item 16 (b01_iri
#   pins). Environment (b) is used ONLY under D-49 and its addenda, for B-01 generation and
#   `verify_runtime` (D-83 A8 item 11); its `environment_id` literal is `b01_iri`.
# Inputs: environment/b01_iri-conda-linux64.lock (conda explicit, URL#sha256) and
#   environment/b01_iri-wheels-linux64.lock (pip layer, wheel#sha256), and
#   configs/experiment.yaml (the iricore wheel and companion SHA-256 pins, D-45/D-49).
# Re-run behaviour: refuses if the target conda env exists (this script never deletes);
#   after install it re-checks the lock's iricore/numpy/fortranformat/pymap3d hashes
#   against configs/experiment.yaml and every installed iricore file against its RECORD,
#   and exits non-zero naming any mismatch.
#
# Usage: bash environment/bootstrap_b01.sh
set -euo pipefail

CONDA=${CONDA:-$HOME/miniconda3/bin/conda}
ENV=${B01_ENV:-b01_iri}  # override only to verify the bootstrap itself
HERE=$(cd "$(dirname "$0")" && pwd)

if "$CONDA" env list | awk '{print $1}' | grep -qx "$ENV"; then
  echo "bootstrap_b01: refusing: conda env $ENV already exists" >&2; exit 2
fi

"$CONDA" create -y -n "$ENV" --file "$HERE/b01_iri-conda-linux64.lock"
PY=$("$CONDA" run -n "$ENV" python -c 'import sys;print(sys.executable)')

REQ=$(mktemp)
while IFS='#' read -r wheel sha; do
  [ -z "$wheel" ] && continue
  name=${wheel%%-[0-9]*}; rest=${wheel#"$name"-}; version=${rest%%-*}
  echo "${name//_/-}==$version --hash=sha256:$sha" >> "$REQ"
done < "$HERE/b01_iri-wheels-linux64.lock"
"$PY" -m pip install --no-deps --require-hashes --only-binary=:all: -r "$REQ"

"$PY" - "$HERE/b01_iri-wheels-linux64.lock" "$HERE/../configs/experiment.yaml" <<'PYEOF'
import base64, hashlib, importlib.metadata as m, re, sys
lock = dict(line.strip().split("#", 1) for line in open(sys.argv[1]) if "#" in line)
cfg = open(sys.argv[2], encoding="utf-8").read()
bad = []
want_wheel = re.search(r'wheel_sha256: "([0-9a-f]{64})"', cfg).group(1)
iricore = [s for w, s in lock.items() if w.startswith("iricore-")]
if iricore != [want_wheel]:
    bad.append(f"iricore wheel sha256 {iricore} != experiment.yaml {want_wheel}")
for pkg in ("numpy", "fortranformat", "pymap3d"):
    pin = re.search(rf'{pkg}: {{version: "[^"]+", sha256: "([0-9a-f]{{64}})"}}', cfg).group(1)
    got = [s for w, s in lock.items() if w.startswith(pkg + "-")]
    if got != [pin]:
        bad.append(f"{pkg} wheel sha256 {got} != experiment.yaml {pin}")
d = m.distribution("iricore")
for f in d.files:
    if f.hash is None:
        continue
    h = base64.urlsafe_b64encode(hashlib.sha256(open(d.locate_file(f), "rb").read()).digest())
    if h.rstrip(b"=").decode() != f.hash.value:
        bad.append(f"iricore installed file {f} disagrees with RECORD")
if sys.version.split()[0] != "3.10.12":
    bad.append(f"python {sys.version.split()[0]} != 3.10.12 (D-49)")
if bad:
    sys.exit("bootstrap_b01: " + "; ".join(bad))
print("bootstrap_b01: wheel pins, RECORD and interpreter all match")
PYEOF
echo "bootstrap_b01: env $ENV ready ($PY)"
