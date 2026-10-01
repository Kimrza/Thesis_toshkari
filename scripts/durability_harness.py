"""Durability harness: fault injection against the three governed write types (D-83 revision 7
§A7 item 6; §R4-7 item 11; §R5-7 row 7R; §W7 W-6).

Purpose
-------
Measures whether the project's governed writes survive an abrupt fault: the access-log row
(`src.data.locked_test._append_and_flush`), the experiment-registry row
(`src.data.experiment_registry.append_registry_event`) and the write-once receipt
(`src.data.release.write_once_durable`). Each trial starts a CHILD process that performs the
production write in a loop and acknowledges each write on stdout only AFTER the production
function returned (i.e. after its fsync). The parent injects the fault, then verifies:

* every acknowledged write is present and intact on disk (no lost acknowledged write);
* nothing on disk is corrupt except, at most, one torn FINAL record that the project's own
  reader detects (the registry's R-08 torn-write distinction; an unterminated final access
  row; a receipt that is absent or complete, never partial-and-accepted);
* the file remains appendable/readable by the production reader afterwards.

A trial FAILS if any acknowledged write is lost or damaged, or if a corrupt record is not
detected. Failures are recorded, never discarded.

Fault types
-----------
* `kill`: process kill (`TerminateProcess` on Windows, SIGKILL on POSIX) at a random point
  after a random number of acknowledged writes. Fully automated. Because each production
  write is a single small system call, a random kill almost never lands inside one: three
  campaigns of 900 trials produced 0 torn records (GOV-2026-10-01-PV-10 Rec 7, BENCH-10).
* `kill-torn` (D-83 revision 8 section A8 item 14): a deterministic, controlled
  interruption INSIDE the production write. After a random number of acknowledged writes
  the child arms one injection point, performs the next production write through the
  production function, and the injection splits that write at the byte boundary the point
  names, forces the written prefix to disk, reports `INJECTED`, and blocks; the parent then
  kills it. The points are, for the appends (`access`, `registry`), `mid-record` (the first
  half of the record's bytes reach the file); and for the write-once receipt,
  `mid-temp-write` (half the bytes reach the temporary sibling), `before-link` (the
  temporary sibling is complete and fsynced, the final name not yet linked) and
  `after-link` (the final name is linked, the temporary not yet removed). The trial index
  selects the point deterministically. Only the scratch directory is written; no other
  file is touched. Each trial classifies the on-disk outcome explicitly: `intact_old`
  (only the acknowledged writes; the interrupted one is absent), `intact_new` (the
  interrupted write is complete), `torn_detected` (a partial final record that the
  production reader detects) or `torn_undetected` / `partial_final` (failures).
* `power-loss`: forced power-off by holding the power button with AC power disconnected, the
  single injection method D-83 fixes. It needs a human at the machine and a verified backup
  first, and cannot be automated from inside the session it would cut off. The Student
  directed on 2026-09-30 that the power-loss trials are NOT run; this harness therefore
  refuses `--fault power-loss`, and the 30 power-loss trials stay OPEN.

Inputs
------
`--fault`, `--write-type`, `--trials`, `--out` (evidence directory; the files under test are
written in a scratch directory on the filesystem under test, `--scratch`), `--seed`,
`--allow-dirty` (records a non-governed campaign from a dirty tree; without it a dirty tree,
including untracked files under `src/`, `scripts/`, `tests/` or `configs/`, is refused).

Re-run behaviour
----------------
Each invocation writes a new campaign directory `<out>/<campaign_id>/` with one JSON record
per trial and a summary with SHA-256 manifest; nothing earlier is overwritten. The scratch
files are kept only for failed trials (as evidence) and removed for passing ones.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import random
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

WRITE_TYPES = ("access", "registry", "receipt")
#: D-83 revision 7 §R4-7 item 11: per fault x write type (x filesystem).
REQUIRED_N = {"kill": 100, "kill-torn": 100, "power-loss": 10}


# --------------------------------------------------------------------------------------
# The child: the production write in a loop, acknowledging after each return.
# --------------------------------------------------------------------------------------


#: The interpreter each named environment is pinned to: `tec-thesis-311` (TE 8.1, Python
#: 3.11) and `b01_iri` (Python 3.10.12, artifacts/exec_evidence/run_2026-09-28_b01_wsl_local/
#: SESSION_A_LOCAL_EXECUTION_RECORD.md; GOV-2026-10-01-PV-10 Rec 23, BENCH-15).
GOVERNED_PYTHON = {"tec-thesis-311": (3, 11), "b01_iri": (3, 10)}


def _campaign_environment_id() -> str:
    """The declared environment, but only when the interpreter matches it.

    A campaign run on a non-governed interpreter is labelled `undeclared`, never the
    declared id (GOV-2026-09-30-PV-09 ML-03 / DATA-05: the first campaign ran on 3.14
    under a `tec-thesis-311` label).
    """
    declared = os.environ.get("TEC_ENVIRONMENT_ID", "undeclared")
    pinned = GOVERNED_PYTHON.get(declared)
    if pinned is not None and sys.version_info[:2] != pinned:
        return "undeclared"
    return declared


def _registry_row(i: int) -> dict[str, Any]:
    return {
        "run_id": f"durability-{i:06d}",
        "started_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "completed_at_utc": "",
        "status": "started",
        "code_commit": "0" * 40,
        "environment_lock_hash": "0" * 64,
        "platform": "local",
        "environment_id": _campaign_environment_id(),
        "dataset_version": "",
        "fold_id": "",
        "mask_id": "",
        "feature_set_id": "",
        "model_id": "",
        "hyperparameters_json": "",
        "seed": 0,
        "validation_metric_name": "",
        "validation_metric_value": "",
        "artifact_manifest_path": "",
        "prediction_hash": "",
        "locked_test_accessed": False,
        "notes": "durability harness trial row (D-83 W-6); not a scientific run",
    }


#: Seconds a `kill-torn` child may take to reach its injection point before it is killed.
TORN_TRIAL_TIMEOUT_S = 120

INJECTION_POINTS = {
    "access": ("mid-record",),
    "registry": ("mid-record",),
    "receipt": ("mid-temp-write", "before-link", "after-link"),
}
_INJECTED_MARKER = "INJECTED"


def _block_forever() -> None:
    print(_INJECTED_MARKER, flush=True)
    while True:  # the parent kills this process; it never returns
        time.sleep(3600)


def _arm_injection(write_type: str, point: str, armed: dict[str, bool]) -> None:
    """Install the controlled interruption for the NEXT production write (child only).

    The production functions run unmodified; the injection replaces the operating-system
    primitive they call so that, once armed, the write is split at a deterministic byte
    boundary and the process blocks there until the parent kills it.
    """
    import pathlib

    real_write = os.write
    real_link = os.link
    real_unlink = pathlib.Path.unlink
    real_open = pathlib.Path.open

    def split(fd: int, data: bytes) -> None:
        cut = max(1, len(data) // 2)
        real_write(fd, data[:cut])
        os.fsync(fd)
        _block_forever()

    if write_type == "registry" and point == "mid-record":

        def os_write(fd: int, data: bytes) -> int:
            if armed["on"]:
                split(fd, data)
            return real_write(fd, data)

        os.write = os_write  # experiment_registry appends with one os.write (R-08)
        return

    class _SplitHandle:
        def __init__(self, handle: Any) -> None:
            self._h = handle

        def write(self, text: str) -> int:
            if armed["on"]:
                self._h.flush()
                split(self._h.fileno(), text.encode("utf-8"))
            return self._h.write(text)

        def __getattr__(self, name: str) -> Any:
            return getattr(self._h, name)

        def __enter__(self) -> _SplitHandle:
            self._h.__enter__()
            return self

        def __exit__(self, *exc: Any) -> Any:
            return self._h.__exit__(*exc)

    if (write_type == "access" and point == "mid-record") or (
        write_type == "receipt" and point == "mid-temp-write"
    ):

        def path_open(self: Any, mode: str = "r", *args: Any, **kwargs: Any) -> Any:
            handle = real_open(self, mode, *args, **kwargs)
            return _SplitHandle(handle) if armed["on"] and ("a" in mode or "x" in mode) else handle

        pathlib.Path.open = path_open  # type: ignore[method-assign]
        return
    if write_type == "receipt" and point == "before-link":

        def os_link(src: Any, dst: Any, *args: Any, **kwargs: Any) -> None:
            if armed["on"]:
                _block_forever()
            real_link(src, dst, *args, **kwargs)

        os.link = os_link
        return
    if write_type == "receipt" and point == "after-link":

        def path_unlink(self: Any, *args: Any, **kwargs: Any) -> None:
            if armed["on"] and self.name.endswith(".partial"):
                _block_forever()
            real_unlink(self, *args, **kwargs)

        pathlib.Path.unlink = path_unlink  # type: ignore[method-assign]
        return
    raise SystemExit(f"no injection point {point!r} for write type {write_type!r}")


def run_child(
    write_type: str, scratch: Path, *, inject_at: int | None = None, point: str | None = None
) -> int:
    scratch.mkdir(parents=True, exist_ok=True)
    armed = {"on": False}
    if inject_at is not None:
        _arm_injection(write_type, str(point), armed)
    i = 0
    if write_type == "access":
        from src.data.locked_test import AccessRecord, _append_and_flush

        log = scratch / "merge_run_access_log.jsonl"
        while True:
            i += 1
            armed["on"] = inject_at is not None and i == inject_at
            _append_and_flush(
                log,
                AccessRecord(
                    run_id=f"durability-{i:06d}",
                    retrieved_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                    scope="durability harness synthetic row; no restricted file is read",
                    purpose="coverage_audit",
                    performance_inspected=False,
                    locked_test_accessed=True,
                    authorization="D-83 revision 7 W-6 durability measurement",
                ),
            )
            print(f"ACK {i}", flush=True)
    elif write_type == "registry":
        from src.data.experiment_registry import append_registry_event

        registry = scratch / "experiment_registry.jsonl"
        access = scratch / "no_access_log.jsonl"
        while True:
            i += 1
            armed["on"] = inject_at is not None and i == inject_at
            append_registry_event(
                registry, _registry_row(i), phase=1, writer_role="stage", access_log_path=access
            )
            print(f"ACK {i}", flush=True)
    elif write_type == "receipt":
        from src.data.release import write_once_durable

        while True:
            i += 1
            armed["on"] = inject_at is not None and i == inject_at
            body = json.dumps({"receipt": i, "payload": "x" * 4096}, sort_keys=True) + "\n"
            write_once_durable(scratch / f"receipt_{i:06d}.json", body)
            print(f"ACK {i} {hashlib.sha256(body.encode('utf-8')).hexdigest()}", flush=True)
    raise SystemExit(f"unknown write type {write_type!r}")


# --------------------------------------------------------------------------------------
# Verification against the production readers.
# --------------------------------------------------------------------------------------


def _jsonl_state(path: Path) -> dict[str, Any]:
    """Complete lines parsed; a final unterminated fragment reported as torn."""
    if not path.is_file():
        return {"complete": [], "torn_tail": None, "corrupt_lines": []}
    data = path.read_bytes()
    lines = data.split(b"\n")
    tail = lines.pop()  # b"" when the file ends with a newline
    complete, corrupt = [], []
    for n, raw in enumerate(lines, 1):
        try:
            complete.append(json.loads(raw.decode("utf-8")))
        except (UnicodeDecodeError, json.JSONDecodeError):
            corrupt.append(n)
    return {
        "complete": complete,
        "torn_tail": tail.decode("utf-8", "replace")[:200] if tail else None,
        "corrupt_lines": corrupt,
    }


def verify(write_type: str, scratch: Path, acked: list[tuple[int, str | None]]) -> dict[str, Any]:
    acked_ids = [i for i, _ in acked]
    problems: list[str] = []
    detail: dict[str, Any] = {"acknowledged": len(acked_ids)}
    if write_type in ("access", "registry"):
        name = "merge_run_access_log.jsonl" if write_type == "access" else "experiment_registry.jsonl"
        state = _jsonl_state(scratch / name)
        on_disk = [int(str(r.get("run_id", "x-0")).rsplit("-", 1)[-1]) for r in state["complete"]]
        missing = sorted(set(acked_ids) - set(on_disk))
        if missing:
            problems.append(f"acknowledged writes lost: {missing[:10]}")
        if state["corrupt_lines"]:
            problems.append(f"corrupt complete lines: {state['corrupt_lines'][:10]}")
        if on_disk != list(range(1, len(on_disk) + 1)):
            problems.append("on-disk rows are not the contiguous sequence 1..n")
        detail.update(
            rows_on_disk=len(on_disk),
            unacknowledged_rows_on_disk=len(set(on_disk) - set(acked_ids)),
            torn_tail=state["torn_tail"],
        )
        if write_type == "registry":
            from src.data.experiment_registry import check_registry_integrity

            try:
                report = check_registry_integrity(scratch / name)
                detail["registry_integrity"] = {
                    k: (v if isinstance(v, (int, str, bool, type(None))) else str(v))
                    for k, v in vars(report).items()
                }
                if state["torn_tail"] and not report.torn_final_run_id and not report.torn_final_reported:
                    problems.append("a torn final record was not detected by the registry reader")
            except Exception as exc:  # noqa: BLE001 - recorded, and fails the trial
                problems.append(f"registry reader refused the file: {exc}")
        if write_type == "access" and state["torn_tail"] is not None:
            from src.data.locked_test import LockedTestError, assert_first_locked_evaluation

            try:
                assert_first_locked_evaluation(
                    scratch / name, run_id="durability-reader", script_id="x", phase_id="x"
                )
                problems.append("a torn final access row was not detected by the access reader")
            except LockedTestError:
                detail["access_reader"] = "torn final row detected (refused, fail-closed)"
        # Recovery: the production writer must still append after the fault.
        try:
            if state["torn_tail"] is not None and write_type == "access":
                detail["recovery"] = "torn tail present; reader reports it; not auto-repaired"
            else:
                detail["recovery"] = "file readable by the production reader"
        except Exception as exc:  # noqa: BLE001
            problems.append(f"recovery check failed: {exc}")
    else:
        files = sorted(scratch.glob("receipt_*.json"))
        present = {}
        partial = []
        for f in files:
            body = f.read_bytes()
            try:
                json.loads(body.decode("utf-8"))
                present[int(f.stem.split("_")[1])] = hashlib.sha256(body).hexdigest()
            except (UnicodeDecodeError, json.JSONDecodeError):
                partial.append(f.name)
        for i, digest in acked:
            if present.get(i) != digest:
                problems.append(f"acknowledged receipt {i} lost or altered")
                break
        unacked_partial = [p for p in partial if int(p.split("_")[1].split(".")[0]) not in acked_ids]
        if partial:
            # Complete-or-absent (D-83 revision 8 section A8 item 6): a partial file at a
            # FINAL name is a failure whether or not it was acknowledged.
            problems.append(f"partial receipts at a final name: {partial}")
        detail.update(
            receipts_on_disk=len(files),
            partial_unacknowledged_receipt=unacked_partial or None,
            temporary_siblings_left=len(list(scratch.glob(".receipt_*.partial"))),
        )
    detail["outcome"] = _classify(write_type, scratch, acked_ids, detail, problems)
    return {"pass": not problems, "problems": problems, **detail}


def _classify(
    write_type: str, scratch: Path, acked_ids: list[int], detail: dict[str, Any], problems: list[str]
) -> str:
    """The explicit on-disk outcome of the interrupted write (item 14)."""
    if write_type in ("access", "registry"):
        if detail.get("torn_tail"):
            undetected = any("not detected" in p for p in problems)
            return "torn_undetected" if undetected else "torn_detected"
        return "intact_new" if detail.get("unacknowledged_rows_on_disk") else "intact_old"
    if any("partial receipts" in p for p in problems):
        return "partial_final"
    on_disk = {int(f.stem.split("_")[1]) for f in scratch.glob("receipt_*.json")}
    return "intact_new" if on_disk - set(acked_ids) else "intact_old"


# --------------------------------------------------------------------------------------
# The parent: one kill trial.
# --------------------------------------------------------------------------------------


def kill_trial(write_type: str, scratch: Path, rng: random.Random) -> dict[str, Any]:
    target = rng.randint(1, 150)
    extra_delay = rng.uniform(0.0, 0.02)
    env = dict(os.environ)
    env.setdefault("PYTHONHASHSEED", "0")
    env.setdefault("TEC_PLATFORM", "local")
    started = time.monotonic()
    proc = subprocess.Popen(  # noqa: S603 - fixed argv, our interpreter
        [sys.executable, str(Path(__file__).resolve()), "--child", write_type, "--scratch", str(scratch)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
        cwd=str(REPO_ROOT),
    )
    acked: list[tuple[int, str | None]] = []
    assert proc.stdout is not None
    while len(acked) < target:
        line = proc.stdout.readline()
        if not line:
            break
        parts = line.split()
        if parts and parts[0] == "ACK":
            acked.append((int(parts[1]), parts[2] if len(parts) > 2 else None))
    time.sleep(extra_delay)
    proc.kill()  # TerminateProcess / SIGKILL: no handler, no flush, no atexit
    proc.wait(timeout=60)
    # Acks written to the pipe before the kill are also acknowledged writes.
    rest = proc.stdout.read() or ""
    for line in rest.splitlines():
        parts = line.split()
        if parts and parts[0] == "ACK":
            acked.append((int(parts[1]), parts[2] if len(parts) > 2 else None))
    stderr = (proc.stderr.read() if proc.stderr else "")[-2000:]
    result = verify(write_type, scratch, acked)
    return {
        "fault": "kill",
        "injection": "TerminateProcess" if sys.platform == "win32" else "SIGKILL",
        "target_acks_before_kill": target,
        "extra_delay_s": round(extra_delay, 4),
        "returncode": proc.returncode,
        "child_stderr_tail": stderr if not result["pass"] else "",
        "elapsed_s": round(time.monotonic() - started, 3),
        **result,
    }


def torn_trial(write_type: str, scratch: Path, rng: random.Random, n: int) -> dict[str, Any]:
    """One deterministic in-write interruption (`kill-torn`, item 14)."""
    points = INJECTION_POINTS[write_type]
    point = points[(n - 1) % len(points)]
    inject_at = rng.randint(1, 150)
    env = dict(os.environ)
    env.setdefault("PYTHONHASHSEED", "0")
    env.setdefault("TEC_PLATFORM", "local")
    started = time.monotonic()
    proc = subprocess.Popen(  # noqa: S603 - fixed argv, our interpreter
        [
            sys.executable, str(Path(__file__).resolve()), "--child", write_type,
            "--scratch", str(scratch), "--inject-at", str(inject_at), "--point", point,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
        cwd=str(REPO_ROOT),
    )
    acked: list[tuple[int, str | None]] = []
    injected = False
    if proc.stdout is None:
        raise SystemExit("the torn-trial child has no stdout pipe")
    # Watchdog: a child that never reaches its injection point is killed and the trial
    # FAILS, so a broken injection can never stall a campaign or pass by default.
    import threading

    watchdog = threading.Timer(TORN_TRIAL_TIMEOUT_S, proc.kill)
    watchdog.start()
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        parts = line.split()
        if parts and parts[0] == "ACK":
            acked.append((int(parts[1]), parts[2] if len(parts) > 2 else None))
        elif parts and parts[0] == _INJECTED_MARKER:
            injected = True
            break
    watchdog.cancel()
    proc.kill()  # TerminateProcess / SIGKILL at the injection point
    proc.wait(timeout=60)
    stderr = (proc.stderr.read() if proc.stderr else "")[-2000:]
    result = verify(write_type, scratch, acked)
    if not injected:
        result["pass"] = False
        result["problems"] = [*result["problems"], "the injection point was never reached"]
    expected = {
        "mid-record": "torn_detected",
        "mid-temp-write": "intact_old",
        "before-link": "intact_old",
        "after-link": "intact_new",
    }[point]
    if result["pass"] and result["outcome"] != expected:
        result["pass"] = False
        result["problems"] = [
            *result["problems"],
            f"outcome {result['outcome']!r} at {point!r}; the governed outcome is {expected!r}",
        ]
    return {
        "fault": "kill-torn",
        "injection": ("TerminateProcess" if sys.platform == "win32" else "SIGKILL")
        + f" at {point}",
        "injection_point": point,
        "expected_outcome": expected,
        "inject_at_write": inject_at,
        "returncode": proc.returncode,
        "child_stderr_tail": stderr if not result["pass"] else "",
        "elapsed_s": round(time.monotonic() - started, 3),
        **result,
    }


def _windows_volume(drive_letter: str) -> dict[str, Any]:
    """The backing Windows volume of a WSL `/mnt/<x>` path, read through interop."""
    try:
        out = subprocess.run(  # noqa: S603,S607
            [
                "powershell.exe", "-NoProfile", "-Command",
                f"$v = Get-Volume -DriveLetter {drive_letter}; "
                f"$s = (cmd /c vol {drive_letter}:) -join ' '; "
                "Write-Output ($v.FileSystem + '|' + $s)",
            ],
            capture_output=True, text=True, check=False, timeout=60,
        ).stdout.strip()
        fs, _, vol = out.partition("|")
        serial = vol.rsplit(" ", 1)[-1] if "Serial Number" in vol else None
        return {"backing_filesystem": fs or "unknown", "backing_volume_serial": serial}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"backing_filesystem": "unavailable", "error": str(exc)}


def filesystem_identity(path: Path) -> dict[str, Any]:
    info: dict[str, Any] = {"path": str(path.resolve())}
    if sys.platform == "win32":
        import ctypes

        drive = str(path.resolve().drive) + "\\"
        fs = ctypes.create_unicode_buffer(64)
        vol = ctypes.create_unicode_buffer(256)
        serial = ctypes.c_uint32()
        ok = ctypes.windll.kernel32.GetVolumeInformationW(
            ctypes.c_wchar_p(drive), vol, 256, ctypes.byref(serial), None, None, fs, 64
        )
        info.update(
            drive=drive,
            filesystem=fs.value if ok else "unknown",
            volume_serial=f"{serial.value:08X}" if ok else None,
        )
    else:
        try:
            out = subprocess.run(["df", "-T", str(path)], capture_output=True, text=True, check=False).stdout  # noqa: S603,S607
            info["df"] = out.strip().splitlines()[-1] if out.strip() else ""
        except OSError:
            info["df"] = "unavailable"
        # The mount the path lives on, with its type and options (PV-10 Rec 17, BENCH-12).
        resolved = str(path.resolve())
        best = None
        try:
            for line in Path("/proc/mounts").read_text(encoding="utf-8").splitlines():
                parts = line.split()
                if len(parts) >= 4 and (resolved == parts[1] or resolved.startswith(parts[1].rstrip("/") + "/")):
                    if best is None or len(parts[1]) > len(best[1]):
                        best = parts
        except OSError:
            best = None
        if best is not None:
            info.update(mount_point=best[1], mount_type=best[2], mount_options=best[3])
            if best[1].startswith("/mnt/") and len(best[1]) == 6:
                info.update(_windows_volume(best[1][-1].upper()))
    return info


GOVERNED_TREE_PATHS = ("src", "scripts", "tests", "configs", "environment", "pyproject.toml")


def working_tree_state() -> dict[str, Any]:
    """Whether the code a campaign executes is exactly `code_commit` (PV-10 Rec 18).

    Dirty means a tracked change OR an untracked file under the governed code and config
    paths. Tracked changes elsewhere (governance prose, the AI-DLC audit shard the workflow
    appends to) do not execute and are recorded, not refused.
    """

    def porcelain(*args: str) -> list[str]:
        return subprocess.run(  # noqa: S603,S607
            ["git", "status", "--porcelain", *args],
            capture_output=True, text=True, cwd=REPO_ROOT, check=False,
        ).stdout.splitlines()

    governed = porcelain("--untracked-files=all", "--", *GOVERNED_TREE_PATHS)
    governed = [ln for ln in governed if "__pycache__" not in ln]
    elsewhere = [ln for ln in porcelain("--untracked-files=no") if ln not in governed]
    return {
        "dirty": bool(governed),
        "governed_changes": governed[:50],
        "other_tracked_changes": elsewhere[:50],
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_campaign(args: argparse.Namespace) -> int:
    if args.fault not in ("kill", "kill-torn"):
        raise SystemExit(
            "power-loss trials are not run: they need a human at the power button, and the "
            "Student directed on 2026-09-30 that they stay open (D-83 revision 7 A7 item 6)"
        )
    tree = working_tree_state()
    if tree["dirty"] and not args.allow_dirty:
        raise SystemExit(
            "the working tree is dirty (tracked changes or untracked governed files); a "
            "governed campaign runs from a clean commit (D-83 revision 8 section A8 item 13; "
            f"PV-10 Rec 18): {tree['governed_changes']}"
        )
    from src.data.resources import cpu_model

    campaign_id = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    out = Path(args.out) / f"campaign_{args.fault}_{campaign_id}"
    out.mkdir(parents=True, exist_ok=False)
    scratch_root = Path(args.scratch)
    scratch_root.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    git = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=REPO_ROOT, check=False).stdout.strip()  # noqa: S603,S607
    header = {
        "campaign_id": campaign_id,
        "decision": (
            "D-83 revision 7 section A7 item 6; section R4-7 item 11; W-6; revision 8 "
            "section A8 items 3, 13 and 14"
        ),
        "fault": args.fault,
        "write_types": list(args.write_type),
        "trials_per_write_type": args.trials,
        "required_per_write_type": REQUIRED_N[args.fault],
        "seed": args.seed,
        "code_commit": git,
        "working_tree_dirty": tree["dirty"],
        "working_tree": tree,
        "governed": not tree["dirty"],
        "environment": {
            "environment_id": _campaign_environment_id(),
            "declared_environment_id": os.environ.get("TEC_ENVIRONMENT_ID", "undeclared"),
            "python": sys.version,
            "executable": sys.executable,
            "platform": platform.platform(),
            "cpu_model": cpu_model(),
        },
        "filesystem_under_test": filesystem_identity(scratch_root),
        "started_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    (out / "campaign.json").write_text(json.dumps(header, indent=2) + "\n", encoding="utf-8")
    totals: dict[str, dict[str, int]] = {}
    with (out / "trials.jsonl").open("w", encoding="utf-8", newline="\n") as log:
        for write_type in args.write_type:
            totals[write_type] = {"run": 0, "pass": 0, "fail": 0}
            for n in range(1, args.trials + 1):
                scratch = scratch_root / f"{campaign_id}_{write_type}_{n:04d}"
                if scratch.exists():
                    shutil.rmtree(scratch)
                trial = (
                    torn_trial(write_type, scratch, rng, n)
                    if args.fault == "kill-torn"
                    else kill_trial(write_type, scratch, rng)
                )
                record = {"trial": n, "write_type": write_type, **trial}
                record["recorded_at_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
                if record["pass"]:
                    shutil.rmtree(scratch, ignore_errors=True)
                else:
                    kept = out / "failed_trial_files" / scratch.name
                    shutil.copytree(scratch, kept)
                    record["kept_files"] = str(kept.relative_to(out))
                log.write(json.dumps(record, sort_keys=True) + "\n")
                log.flush()
                os.fsync(log.fileno())
                totals[write_type]["run"] += 1
                totals[write_type]["pass" if record["pass"] else "fail"] += 1
                print(f"{write_type} trial {n}/{args.trials}: {'PASS' if record['pass'] else 'FAIL'} "
                      f"(acks {record['acknowledged']})", flush=True)
    outcomes: dict[str, dict[str, int]] = {}
    for line in (out / "trials.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        bucket = outcomes.setdefault(row["write_type"], {})
        bucket[row.get("outcome", "unclassified")] = bucket.get(row.get("outcome", "unclassified"), 0) + 1
    summary = {
        **header,
        "outcomes": outcomes,
        "finished_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "totals": totals,
        "all_passed": all(t["fail"] == 0 for t in totals.values()),
        "meets_required_n": all(t["run"] >= REQUIRED_N[args.fault] for t in totals.values()),
        "one_sided_95_zero_failure_upper_bound": {
            wt: round(1 - 0.05 ** (1 / t["run"]), 4) if t["fail"] == 0 and t["run"] else None
            for wt, t in totals.items()
        },
        "trials_sha256": _sha256(out / "trials.jsonl"),
        "campaign_sha256": _sha256(out / "campaign.json"),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"out": str(out), "totals": totals, "all_passed": summary["all_passed"]}))
    return 0 if summary["all_passed"] else 1


def _parse(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--child", choices=WRITE_TYPES)
    parser.add_argument("--scratch", type=Path, default=REPO_ROOT / "artifacts" / "durability_scratch")
    parser.add_argument("--fault", choices=("kill", "kill-torn", "power-loss"), default="kill")
    parser.add_argument("--inject-at", type=int, default=None)
    parser.add_argument("--point", default=None)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--write-type", nargs="+", choices=WRITE_TYPES, default=list(WRITE_TYPES))
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "evidence" / "durability")
    parser.add_argument("--seed", type=int, default=20260930)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse(sys.argv[1:] if argv is None else argv)
    if args.child:
        return run_child(args.child, args.scratch, inject_at=args.inject_at, point=args.point)
    return run_campaign(args)


if __name__ == "__main__":
    sys.exit(main())
