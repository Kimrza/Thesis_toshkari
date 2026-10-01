"""Value-level (c) vs (a)-reference diff of every exact output: max abs and max ULP per column."""
import json
import math
import sys
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq

ref_dir, prod_dir = Path(sys.argv[1]), Path(sys.argv[2])


def ulps(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    ia = a.view(np.int64).astype(np.int64)
    ib = b.view(np.int64).astype(np.int64)
    ia = np.where(ia < 0, np.int64(-0x8000000000000000) - ia, ia)
    ib = np.where(ib < 0, np.int64(-0x8000000000000000) - ib, ib)
    both_nan = np.isnan(a) & np.isnan(b)
    d = np.abs(ia - ib).astype(float)
    d[both_nan] = 0
    return d


for name in sorted(p.name for p in ref_dir.iterdir()):
    r, p = ref_dir / name, prod_dir / name
    if not p.exists():
        print(name, "MISSING in produced")
        continue
    if r.read_bytes() == p.read_bytes():
        print(name, "byte-equal")
        continue
    if name.endswith(".parquet"):
        ta, tb = pq.read_table(r), pq.read_table(p)
        if not ta.schema.equals(tb.schema):
            print(name, "SCHEMA differs")
            continue
        out = []
        for col in ta.column_names:
            x, y = ta[col].to_numpy(zero_copy_only=False), tb[col].to_numpy(zero_copy_only=False)
            if x.dtype.kind == "f":
                if not np.array_equal(x, y, equal_nan=True):
                    out.append(f"{col}: max_abs={np.nanmax(np.abs(x - y)):.3g} max_ulp={ulps(x, y).max():.0f}")
            elif not all((a == b) or (a != a and b != b) for a, b in zip(x.tolist(), y.tolist())):
                out.append(f"{col}: NON-FLOAT differs")
        print(name, "values:", "; ".join(out) if out else "equal (bytes differ only)")
    elif name.endswith((".json", ".yaml")):
        a, b = json.loads(r.read_text()), json.loads(p.read_text())
        a.pop("fixture_stamp", None)
        b.pop("fixture_stamp", None)
        diffs = []

        def walk(x, y, t=""):
            if isinstance(x, dict) and isinstance(y, dict):
                for k in set(x) | set(y):
                    walk(x.get(k), y.get(k), f"{t}/{k}")
            elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
                for i, (u, v) in enumerate(zip(x, y)):
                    walk(u, v, f"{t}[{i}]")
            elif x != y:
                if isinstance(x, float) and isinstance(y, float):
                    diffs.append(f"{t} ulp={ulps([x],[y])[0]:.0f}")
                else:
                    diffs.append(f"{t}: {str(x)[:40]} | {str(y)[:40]}")

        walk(a, b)
        print(name, "json diffs:", len(diffs), diffs[:4])
