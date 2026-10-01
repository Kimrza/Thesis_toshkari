#!/usr/bin/env bash
# environment/bootstrap_g07.sh -- rebuild environment (c), `g07-clean-run`, on WSL2 Ubuntu
# from the two hashed linux-64 locks, and check out a FRESH clone for the G-07 run.
#
# Purpose: D-83 revision 7 R5-5 item 15 ("linux-64 hashed lock and bootstrap for (c);
#   sparse-checkout / fresh-clone procedure"). Environment (c) is G-07 reproduction only
#   (D-83 A8 item 11); its `environment_id` literal is `g07-clean-run`.
# Inputs: environment/conda-linux64.lock (conda explicit, URL#sha256 -- conda verifies
#   each artifact's sha256), environment/wheels-linux64.lock (pip layer, wheel#sha256),
#   requirements.txt (the governed pins), and the source repository path to clone from.
# Re-run behaviour: refuses if the conda environment already exists (remove it yourself
#   first; this script never deletes); the clone target must not exist. Pins are checked
#   after install and any mismatch exits non-zero naming the package.
#
# Usage: bash environment/bootstrap_g07.sh <source-repo> <clone-dir> [<commit>]
set -euo pipefail

SRC=${1:?source repository path}
DEST=${2:?clone directory (must not exist)}
COMMIT=${3:-HEAD}
CONDA=${CONDA:-$HOME/miniconda3/bin/conda}
ENV=${G07_ENV:-g07-clean-run}  # override only to verify the bootstrap itself
HERE=$(cd "$(dirname "$0")" && pwd)

if "$CONDA" env list | awk '{print $1}' | grep -qx "$ENV"; then
  echo "bootstrap_g07: refusing: conda env $ENV already exists" >&2; exit 2
fi
[ -e "$DEST" ] && { echo "bootstrap_g07: refusing: $DEST exists" >&2; exit 2; }

"$CONDA" create -y -n "$ENV" --file "$HERE/conda-linux64.lock"
PY=$("$CONDA" run -n "$ENV" python -c 'import sys;print(sys.executable)')

WHEELS=$(mktemp -d)
REQ="$WHEELS/requirements-hashed.txt"
while IFS='#' read -r wheel sha; do
  [ -z "$wheel" ] && continue
  name=${wheel%%-[0-9]*}; rest=${wheel#"$name"-}; version=${rest%%-*}
  echo "${name//_/-}==$version --hash=sha256:$sha" >> "$REQ"
done < "$HERE/wheels-linux64.lock"
"$PY" -m pip install --no-deps --require-hashes --only-binary=:all: -r "$REQ"

"$PY" - "$HERE/../requirements.txt" <<'PYEOF'
import importlib.metadata as m, sys
bad = []
for line in open(sys.argv[1], encoding="utf-8"):
    line = line.split("#", 1)[0].strip()
    if "==" not in line:
        continue
    name, want = line.split("==")
    got = m.version(name)
    if got != want:
        bad.append(f"{name}: pinned {want}, installed {got}")
if sys.version_info[:3] != (3, 11, 16):
    bad.append(f"python: pinned 3.11.16, installed {sys.version.split()[0]}")
if bad:
    sys.exit("bootstrap_g07: pin mismatch: " + "; ".join(bad))
print("bootstrap_g07: all governed pins match")
PYEOF

git clone --no-local "$SRC" "$DEST"
git -C "$DEST" checkout --detach "$COMMIT"
echo "bootstrap_g07: env $ENV ready; fresh clone at $DEST ($(git -C "$DEST" rev-parse HEAD))"
echo "run with: TEC_ENVIRONMENT_ID=g07-clean-run TEC_PLATFORM=local $PY ..."
