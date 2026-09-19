"""Run one test in a FRESH interpreter — the stage scripts' own execution model.

Purpose
-------
R-05 (`foundation`): `seed_everything` enables TensorFlow op determinism before any
graph construction and REFUSES when TensorFlow is already initialised in the process.
Every stage script calls it exactly once, first thing, in its own process. A pytest
process is not that model: once any test has imported TensorFlow — including
`seed_everything`'s own deferred import — every later in-process call correctly refuses,
and every "`tensorflow` not in `sys.modules`" import-purity assertion stops measuring
the module under test. Those failures appeared the first time the suite ran with the
pinned TensorFlow installed (`CR-2026-09-19-GATE-PREP-2`, gate item G-7).

`in_fresh_process` re-runs the decorated test in a new interpreter (`python -m pytest
<nodeid>`), where "first call in the process" and "nothing imported yet" are literally
true, exactly as they are for a stage script. The test body is unchanged and is asserted
in the child; the parent asserts the child's exit status and relays its output. Nothing
is skipped, no assertion is weakened, and no ordering dependence is hidden: a child
that fails, fails the parent.

Inputs: the environment (inherited, `PYTHONHASHSEED` included), the repository root.
Re-run behaviour: deterministic given the child's; the recursion guard is the
`TEC_FRESH_PROCESS_CHILD` variable.
"""

from __future__ import annotations

import functools
import inspect
import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_CHILD_FLAG = "TEC_FRESH_PROCESS_CHILD"


def in_fresh_process(test_fn: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator: execute `test_fn` in a fresh interpreter via pytest, once."""
    module_path = Path(inspect.getsourcefile(test_fn) or "").resolve()

    @functools.wraps(test_fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if os.environ.get(_CHILD_FLAG) == "1":
            return test_fn(*args, **kwargs)
        nodeid = f"{module_path.relative_to(REPO_ROOT).as_posix()}::{test_fn.__name__}"
        env = {**os.environ, _CHILD_FLAG: "1"}
        proc = subprocess.run(  # noqa: S603 — sys.executable, fixed argv, no shell
            [sys.executable, "-m", "pytest", nodeid, "-q", "-p", "no:cacheprovider", "--tb=short"],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        assert proc.returncode == 0, (
            f"{nodeid} failed in a fresh interpreter (exit {proc.returncode}):\n"
            f"{proc.stdout[-4000:]}\n{proc.stderr[-2000:]}"
        )
        return None

    return wrapper
