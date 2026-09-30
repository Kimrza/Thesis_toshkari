"""Peak-RSS and CPU-model capture, and the TC-03 limit check (D-83 revision 7 §A7 item 11;
§R4-7 item 10; §W7 W-7).

Purpose
-------
TE §9.2 and TC-03g ask for measured CPU runtime, RAM and storage. Before W-7 only
`platform.machine()` was recorded and nothing captured memory (PV-01 Rec 16). This module
measures, with the standard library only (no new dependency enters the pinned environment):

* the peak resident set of a finished child process (`peak_rss_of_popen`): on Windows the
  child's `PeakWorkingSetSize` read through its still-open process handle; on POSIX the
  `RUSAGE_CHILDREN` high-water mark (an upper bound over every reaped child, reported as
  such);
* the current process's own peak (`peak_rss_self`);
* the CPU model string (`cpu_model`);
* the WSL2 VM's `MemTotal` (`meminfo_total_bytes`), which the TC-03 RAM limb binds to.

`assert_tc03_limits` applies D-83's limit rule: runtime at most 12 h wall-clock per
unattended governed run, and peak RSS at most the (c) WSL2 VM `MemTotal` recorded at G-07.

Inputs: a `subprocess.Popen` that has exited, or nothing. Re-run behaviour: read-only
measurement; nothing is written.
"""

from __future__ import annotations

import os
import platform as _platform
import sys
from pathlib import Path
from typing import Any, Final

from src.data.config import IntegrityError

__all__ = [
    "TC03_RUNTIME_LIMIT_SECONDS",
    "assert_tc03_limits",
    "cpu_model",
    "meminfo_total_bytes",
    "peak_rss_of_popen",
    "peak_rss_self",
]

#: D-83 revision 7 §R4-7 item 10: TC-03's own inherited value, kept rather than invented.
TC03_RUNTIME_LIMIT_SECONDS: Final[float] = 12 * 3600.0


def _windows_peak(handle: int) -> int | None:
    import ctypes
    from ctypes import wintypes

    class PROCESS_MEMORY_COUNTERS(ctypes.Structure):  # noqa: N801 - Win32 name
        _fields_ = [
            ("cb", wintypes.DWORD),
            ("PageFaultCount", wintypes.DWORD),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    counters = PROCESS_MEMORY_COUNTERS()
    counters.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS)
    psapi = ctypes.WinDLL("psapi")
    psapi.GetProcessMemoryInfo.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(PROCESS_MEMORY_COUNTERS),
        wintypes.DWORD,
    ]
    ok = psapi.GetProcessMemoryInfo(wintypes.HANDLE(int(handle)), ctypes.byref(counters), counters.cb)
    return int(counters.PeakWorkingSetSize) if ok else None


def peak_rss_of_popen(proc: Any) -> dict[str, Any]:
    """Peak RSS of an exited child, with the method recorded (never a silent guess)."""
    if sys.platform == "win32":
        handle = getattr(proc, "_handle", None)
        value = _windows_peak(handle) if handle is not None else None
        return {
            "bytes": value,
            "method": "GetProcessMemoryInfo.PeakWorkingSetSize (this child)",
        }
    import resource

    kib = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    scale = 1 if sys.platform == "darwin" else 1024
    return {
        "bytes": int(kib) * scale,
        "method": "getrusage(RUSAGE_CHILDREN).ru_maxrss (high-water mark over reaped children)",
    }


def peak_rss_self() -> dict[str, Any]:
    if sys.platform == "win32":
        import ctypes

        handle = ctypes.windll.kernel32.GetCurrentProcess()
        return {"bytes": _windows_peak(handle), "method": "GetProcessMemoryInfo.PeakWorkingSetSize (self)"}
    import resource

    kib = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    scale = 1 if sys.platform == "darwin" else 1024
    return {"bytes": int(kib) * scale, "method": "getrusage(RUSAGE_SELF).ru_maxrss"}


def cpu_model() -> str:
    """The CPU model string: `/proc/cpuinfo` on Linux, the registry on Windows."""
    if sys.platform.startswith("linux"):
        try:
            for line in Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines():
                if line.lower().startswith("model name"):
                    return line.split(":", 1)[1].strip()
        except OSError:
            pass
    if sys.platform == "win32":
        try:
            import winreg

            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
            ) as key:
                return str(winreg.QueryValueEx(key, "ProcessorNameString")[0]).strip()
        except OSError:
            pass
    return _platform.processor() or _platform.machine() or "unknown-cpu"


def meminfo_total_bytes(path: Path = Path("/proc/meminfo")) -> int | None:
    """`MemTotal` from `/proc/meminfo` (the WSL2 VM's memory), or None where absent."""
    try:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            if line.startswith("MemTotal:"):
                return int(line.split()[1]) * 1024
    except (OSError, ValueError, IndexError):
        return None
    return None


def assert_tc03_limits(
    *, runtime_seconds: float, peak_rss_bytes: int | None, g07_memtotal_bytes: int | None
) -> dict[str, Any]:
    """Apply D-83 revision 7 §R4-7 item 10's limit rule; a breach is a failed run.

    The RAM limb needs the (c) `MemTotal` recorded at G-07; before it exists the limb is
    reported `pending` (it is never assumed to pass). An unmeasured peak RSS fails.
    """
    if runtime_seconds > TC03_RUNTIME_LIMIT_SECONDS:
        raise IntegrityError(
            "TC-03 runtime limb",
            f"{runtime_seconds:.0f} s exceeds the 12 h wall-clock limit (D-83 section R4-7 item 10)",
        )
    if peak_rss_bytes is None:
        raise IntegrityError(
            "TC-03 RAM limb", "peak RSS was not measured; W-7 requires it on every governed run"
        )
    if g07_memtotal_bytes is None:
        return {"runtime": "pass", "ram": "pending: no (c) MemTotal recorded at G-07 yet"}
    if peak_rss_bytes > g07_memtotal_bytes:
        raise IntegrityError(
            "TC-03 RAM limb",
            f"peak RSS {peak_rss_bytes} B exceeds the (c) WSL2 MemTotal {g07_memtotal_bytes} B "
            "(D-83 section R4-7 item 10)",
        )
    return {"runtime": "pass", "ram": "pass"}


def environment_resources() -> dict[str, Any]:
    """CPU model, logical CPUs and (on Linux/WSL2) MemTotal, for the run record."""
    return {
        "cpu_model": cpu_model(),
        "logical_cpus": os.cpu_count(),
        "memtotal_bytes": meminfo_total_bytes(),
    }
