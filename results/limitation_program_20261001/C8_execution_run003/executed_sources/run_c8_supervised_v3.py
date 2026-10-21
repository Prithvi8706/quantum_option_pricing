"""Standalone local C8 supervisor. Author-only until static review and authorization.

Runs unchanged rates/timing only. Prospective 12h/8h entire-phase wall guards;
Windows suspended launch -> Job Object assignment -> resume, with tree ownership.
There are no producer patches, numerical-method overrides, retries or oracle runs.
"""

from __future__ import annotations

import argparse
import ast
import ctypes
from ctypes import wintypes as w
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import time

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
COMMIT = "b4a4bdc9bd21099fd1382dff7f9e57c470a54d3a"
ROOT = Path("C:/Users/prith/quantum_option_pricing")
AUTHOR_DIR = ROOT / "research/limitation_program_20261001"
PREFLIGHT = AUTHOR_DIR / "c8_execution_preflight_v3.json"
OWN_FILES = (
    "run_c8_supervised_v3.py",
    "capture_c8_prerun_inventory_v3.py",
    "c8_execution_preflight_v3.json",
    "C8_EXECUTION_PREFLIGHT_V3.md",
)
DEADLINE = datetime.fromisoformat("2026-10-04T00:00:00+05:30")
RESERVE = 120
BALANCED = "381b4222-f694-41f0-9685-ff5bb260df2e"
TERMINATION_UNCERTIFIED = False

PREVIOUS_AUTHOR_SHA256 = {
    "run_c8_supervised.py": "b9613c6e9a4d3ff888cb00beba39f4e9acdc95d12922f1f6d746f4daefa98358",
    "capture_c8_prerun_inventory.py": (
        "9daffa3f839a0b56ab3b25126ccc52029fd37c3b39540142c9a8cf3943a0e369"
    ),
    "c8_execution_preflight.json": (
        "6b1e03a241febcd5ab5a4304fab3f2e06ec10234720c4446aca86262870d39ad"
    ),
    "C8_EXECUTION_PREFLIGHT.md": "57eb2e82fa2c87b2bd8ea92bd85513fac44b98964e122b0a61cc77670d5997eb",
}
PREVIOUS_DIAGNOSTIC = ROOT / "results/limitation_program_20261001/C8_admission_failure_run001"
PREVIOUS_MANIFEST_SHA256 = "f5850813ecc8a31219a60c8009eeee2258769fa508571bb57c005fac2a9bfc61"


def bind_previous_admission(frozen, check, value):
    """Bind the immutable original attempt and diagnosis before any helper/science import."""
    check()
    expected_policy = dict(
        diagnostic_receipt="results/limitation_program_20261001/C8_admission_failure_run001",
        diagnostic_manifest_sha256=PREVIOUS_MANIFEST_SHA256,
        original_author_sha256=PREVIOUS_AUTHOR_SHA256,
        prior_failure_fixture_or_measurement_credit=0,
    )
    if value.get("previous_admission_bindings") != expected_policy:
        raise RuntimeError(
            "fixed original admission provenance cannot be replaced by caller expectations"
        )

    def path(name):
        check()
        value = Path(name)
        if not value.is_absolute():
            if value.drive or "\\" in str(name) or value.as_posix() != str(name):
                raise RuntimeError("canonical ROOT-relative prior admission reference required")
            value = ROOT / value
        resolved = value.resolve(strict=True)
        resolved.relative_to(ROOT.resolve(strict=True))
        return resolved

    def hashed(source):
        check()
        result = hashlib.sha256()
        with source.open("rb") as stream:
            while block := stream.read(1024 * 1024):
                check()
                result.update(block)
                check()
        check()
        return result.hexdigest()

    def add(name, expected):
        check()
        if (
            type(expected) is not str
            or len(expected) != 64
            or any(character not in "0123456789abcdef" for character in expected)
        ):
            raise RuntimeError("explicit canonical prior admission SHA256 required")
        source = path(name)
        identity = os.path.normcase(str(source))
        if identity in frozen and frozen[identity] != expected:
            raise RuntimeError("prior admission expected SHA cannot be overwritten")
        if hashed(source) != expected:
            raise RuntimeError("immutable prior admission bytes changed: " + str(source))
        frozen[identity] = expected

    manifest_path = PREVIOUS_DIAGNOSTIC / "manifest.json"
    add(manifest_path, PREVIOUS_MANIFEST_SHA256)
    manifest = json.loads(manifest_path.read_bytes())
    check()
    if (
        set(manifest) != {"files", "frozen_inputs", "manifest_self_hash_excluded"}
        or manifest["manifest_self_hash_excluded"] is not True
        or type(manifest["files"]) is not dict
        or type(manifest["frozen_inputs"]) is not dict
    ):
        raise RuntimeError("exact root diagnostic owned/frozen map schema required")
    own = set()
    for field in ("files", "frozen_inputs"):
        for name, expected in manifest[field].items():
            check()
            source = path(name)
            if field == "files":
                source.relative_to(PREVIOUS_DIAGNOSTIC.resolve(strict=True))
                own.add(source)
            add(name, expected)
    actual_own = set()
    for source in PREVIOUS_DIAGNOSTIC.rglob("*"):
        check()
        if source.is_file() and source != manifest_path:
            actual_own.add(path(source))
    if actual_own != own:
        raise RuntimeError("complete prior diagnostic owned inventory required")
    old_receipt = ROOT / "results/limitation_program_20261001/C8_execution_run001"
    expected_old = {
        path(name)
        for name in manifest["frozen_inputs"]
        if path(name).is_relative_to(old_receipt.resolve(strict=True))
    }
    actual_old = set()
    for source in old_receipt.rglob("*"):
        check()
        if source.is_file():
            actual_old.add(path(source))
    if actual_old != expected_old:
        raise RuntimeError("every original failed C8 receipt file remains a strict active binding")
    for name, expected in PREVIOUS_AUTHOR_SHA256.items():
        check()
        add(ROOT / "research/limitation_program_20261001" / name, expected)
        copied = old_receipt / "executed_sources" / name
        copied_key = copied.relative_to(ROOT).as_posix()
        if manifest["frozen_inputs"].get(copied_key) != expected:
            raise RuntimeError(
                "original executed author source belongs to root diagnostic manifest"
            )
    summary = json.loads((PREVIOUS_DIAGNOSTIC / "summary.json").read_bytes())
    check()
    if (
        summary["passed"] is not False
        or summary["original_attempt_immutable"] is not True
        or summary["original_rates_launched"] is not False
        or summary["original_timing_launched"] is not False
        or summary["new_test_or_measurement_credit"] != 0
        or summary["inventory_job_terminal_active_processes"] != 0
        or summary["source_receipt"] != "results/limitation_program_20261001/C8_execution_run001"
        or summary["all_actual_receipt_files_bound"] != len(actual_old)
    ):
        raise RuntimeError(
            "diagnosed original operational admission failure, no numerical retry or credit"
        )
    check()
    return dict(
        original_source_receipt=summary["source_receipt"],
        original_diagnostic_manifest_sha256=PREVIOUS_MANIFEST_SHA256,
        original_author_sources_bound=4,
        all_original_receipt_files_bound=len(actual_old),
        original_failure_fixture_or_measurement_credit=0,
        original_rates_or_timing_launched=False,
        newly_preregistered_operational_admission_not_numerical_retry=True,
    )


class STARTUPINFOW(ctypes.Structure):
    _fields_ = [
        ("cb", w.DWORD),
        ("lpReserved", w.LPWSTR),
        ("lpDesktop", w.LPWSTR),
        ("lpTitle", w.LPWSTR),
        ("dwX", w.DWORD),
        ("dwY", w.DWORD),
        ("dwXSize", w.DWORD),
        ("dwYSize", w.DWORD),
        ("dwXCountChars", w.DWORD),
        ("dwYCountChars", w.DWORD),
        ("dwFillAttribute", w.DWORD),
        ("dwFlags", w.DWORD),
        ("wShowWindow", w.WORD),
        ("cbReserved2", w.WORD),
        ("lpReserved2", ctypes.POINTER(w.BYTE)),
        ("hStdInput", w.HANDLE),
        ("hStdOutput", w.HANDLE),
        ("hStdError", w.HANDLE),
    ]


class PROCESS_INFORMATION(ctypes.Structure):  # noqa: N801 - preserve executed Win32 ABI names
    _fields_ = [
        ("hProcess", w.HANDLE),
        ("hThread", w.HANDLE),
        ("dwProcessId", w.DWORD),
        ("dwThreadId", w.DWORD),
    ]


class BASIC_LIMIT(ctypes.Structure):  # noqa: N801 - preserve executed Win32 ABI names
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_longlong),
        ("PerJobUserTimeLimit", ctypes.c_longlong),
        ("LimitFlags", w.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", w.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", w.DWORD),
        ("SchedulingClass", w.DWORD),
    ]


class IO_COUNTERS(ctypes.Structure):  # noqa: N801 - preserve executed Win32 ABI names
    _fields_ = [
        (name, ctypes.c_ulonglong)
        for name in (
            "ReadOperationCount",
            "WriteOperationCount",
            "OtherOperationCount",
            "ReadTransferCount",
            "WriteTransferCount",
            "OtherTransferCount",
        )
    ]


class EXTENDED_LIMIT(ctypes.Structure):  # noqa: N801 - preserve executed Win32 ABI names
    _fields_ = [
        ("BasicLimitInformation", BASIC_LIMIT),
        ("IoInfo", IO_COUNTERS),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


class ACCOUNTING(ctypes.Structure):
    _fields_ = [
        ("TotalUserTime", ctypes.c_longlong),
        ("TotalKernelTime", ctypes.c_longlong),
        ("ThisPeriodTotalUserTime", ctypes.c_longlong),
        ("ThisPeriodTotalKernelTime", ctypes.c_longlong),
        ("TotalPageFaultCount", w.DWORD),
        ("TotalProcesses", w.DWORD),
        ("ActiveProcesses", w.DWORD),
        ("TotalTerminatedProcesses", w.DWORD),
    ]


class POWER_STATUS(ctypes.Structure):  # noqa: N801 - preserve executed Win32 ABI names
    _fields_ = [
        ("ACLineStatus", w.BYTE),
        ("BatteryFlag", w.BYTE),
        ("BatteryLifePercent", w.BYTE),
        ("SystemStatusFlag", w.BYTE),
        ("BatteryLifeTime", w.DWORD),
        ("BatteryFullLifeTime", w.DWORD),
    ]


class WinJob:
    """All HANDLE functions use explicit Win64-safe prototypes."""

    def __init__(self):
        if os.name != "nt" or ctypes.sizeof(ctypes.c_void_p) != 8:
            raise RuntimeError("requires pinned 64-bit Windows runtime")
        self.k = ctypes.WinDLL("kernel32", use_last_error=True)
        definitions = {
            "CreateJobObjectW": ([ctypes.c_void_p, w.LPCWSTR], w.HANDLE),
            "SetInformationJobObject": ([w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD], w.BOOL),
            "AssignProcessToJobObject": ([w.HANDLE, w.HANDLE], w.BOOL),
            "TerminateJobObject": ([w.HANDLE, w.UINT], w.BOOL),
            "TerminateProcess": ([w.HANDLE, w.UINT], w.BOOL),
            "QueryInformationJobObject": (
                [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD, ctypes.POINTER(w.DWORD)],
                w.BOOL,
            ),
            "CloseHandle": ([w.HANDLE], w.BOOL),
            "CreateProcessW": (
                [
                    w.LPCWSTR,
                    w.LPWSTR,
                    ctypes.c_void_p,
                    ctypes.c_void_p,
                    w.BOOL,
                    w.DWORD,
                    ctypes.c_void_p,
                    w.LPCWSTR,
                    ctypes.POINTER(STARTUPINFOW),
                    ctypes.POINTER(PROCESS_INFORMATION),
                ],
                w.BOOL,
            ),
            "ResumeThread": ([w.HANDLE], w.DWORD),
            "WaitForSingleObject": ([w.HANDLE, w.DWORD], w.DWORD),
            "GetExitCodeProcess": ([w.HANDLE, ctypes.POINTER(w.DWORD)], w.BOOL),
            "GetSystemPowerStatus": ([ctypes.POINTER(POWER_STATUS)], w.BOOL),
            "GetCurrentProcess": ([], w.HANDLE),
            "GetProcessAffinityMask": (
                [w.HANDLE, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_size_t)],
                w.BOOL,
            ),
        }
        for name, (args, result) in definitions.items():
            function = getattr(self.k, name)
            function.argtypes, function.restype = args, result
        self.handle = self.k.CreateJobObjectW(None, None)
        self.process = None
        self.primary_thread = None
        self.pid = None
        self.launch = None
        self.start_cleanup_uncertified = False
        self.start_cleanup_result = None
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = EXTENDED_LIMIT()
        limits.BasicLimitInformation.LimitFlags = 0x2000  # KILL_ON_JOB_CLOSE, no breakaway.
        if not self.k.SetInformationJobObject(
            self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)
        ):
            error = ctypes.get_last_error()
            self.k.CloseHandle(self.handle)
            self.handle = None
            raise ctypes.WinError(error)

    def accounting(self):
        data = ACCOUNTING()
        if not self.k.QueryInformationJobObject(
            self.handle, 1, ctypes.byref(data), ctypes.sizeof(data), None
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        return dict(
            active_processes=int(data.ActiveProcesses),
            total_processes=int(data.TotalProcesses),
            total_terminated_processes=int(data.TotalTerminatedProcesses),
            aggregate_user_cpu_seconds=data.TotalUserTime / 10_000_000,
            aggregate_kernel_cpu_seconds=data.TotalKernelTime / 10_000_000,
            aggregate_cpu_limit_seconds=None,
        )

    def pids(self):
        # Two DWORDs precede an aligned ULONG_PTR array on Win64.
        buffer = ctypes.create_string_buffer(8 + 256 * ctypes.sizeof(ctypes.c_size_t))
        if not self.k.QueryInformationJobObject(
            self.handle, 3, buffer, ctypes.sizeof(buffer), None
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        assigned, count = struct.unpack_from("<II", buffer.raw)
        if count > 256 or assigned > 256 or assigned != count:
            raise RuntimeError("job PID inventory capacity/consistency exhausted")
        return list(struct.unpack_from(f"<{count}Q", buffer.raw, 8)) if count else []

    def start(self, argv: list[str], cwd: Path, stdout: Path, stderr: Path, guard):
        global TERMINATION_UNCERTIFIED
        import msvcrt

        guard.check()
        if self.process is not None:
            raise RuntimeError("one process root per Job Object")
        stdout.parent.mkdir(parents=True, exist_ok=True)
        info, startup = PROCESS_INFORMATION(), STARTUPINFOW()
        startup.cb = ctypes.sizeof(startup)
        startup.dwFlags = 0x100  # STARTF_USESTDHANDLES.
        environment = ctypes.create_unicode_buffer(
            "\0".join(f"{k}={v}" for k, v in sorted(os.environ.items(), key=lambda x: x[0].upper()))
            + "\0\0"
        )
        command = ctypes.create_unicode_buffer(subprocess.list2cmdline(argv))
        created = assigned = False
        try:
            with (
                open(os.devnull, "rb") as incoming,
                stdout.open("xb") as outgoing,
                stderr.open("xb") as errors,
            ):
                handles = [
                    msvcrt.get_osfhandle(file.fileno()) for file in (incoming, outgoing, errors)
                ]
                for handle in handles:
                    os.set_handle_inheritable(handle, True)
                startup.hStdInput, startup.hStdOutput, startup.hStdError = handles
                if not self.k.CreateProcessW(
                    argv[0],
                    command,
                    None,
                    None,
                    True,
                    0x4 | 0x400 | 0x08000000,
                    environment,
                    str(cwd),
                    ctypes.byref(startup),
                    ctypes.byref(info),
                ):
                    raise ctypes.WinError(ctypes.get_last_error())
                created = True
                self.process, self.pid = info.hProcess, int(info.dwProcessId)
                self.primary_thread = info.hThread
                # No script, spawn child or resource tracker executes before assignment.
                if not self.k.AssignProcessToJobObject(self.handle, info.hProcess):
                    raise ctypes.WinError(ctypes.get_last_error())
                assigned = True
                guard.check()
                if self.k.ResumeThread(info.hThread) == 0xFFFFFFFF:
                    raise ctypes.WinError(ctypes.get_last_error())
                self.launch = dict(
                    argv=argv,
                    cwd=str(cwd),
                    pid=self.pid,
                    launched_utc=datetime.now(timezone.utc).isoformat(),
                    assigned_suspended_before_resume=True,
                )
                return self.launch
        except BaseException as launch_error:
            if created:
                if assigned:
                    terminated = bool(self.k.TerminateJobObject(self.handle, 71))
                else:
                    # Exact owned CreateProcessW handle only, never a PID lookup.
                    terminated = bool(self.k.TerminateProcess(info.hProcess, 71))
                terminate_error = None if terminated else ctypes.get_last_error()
                waited = int(self.k.WaitForSingleObject(info.hProcess, 5000))
                wait_error = ctypes.get_last_error() if waited == 0xFFFFFFFF else None
                self.start_cleanup_result = dict(
                    created_own_pid=self.pid,
                    assigned_to_job=assigned,
                    termination_returned_true=terminated,
                    termination_error=terminate_error,
                    wait_result=waited,
                    wait_error=wait_error,
                    own_process_termination_confirmed=terminated and waited == 0,
                )
                if not terminated or waited != 0:
                    self.start_cleanup_uncertified = True
                    TERMINATION_UNCERTIFIED = True
                    self.start_cleanup_result["own_process_and_thread_handles_preserved"] = True
                    raise RuntimeError(
                        "created own child termination not confirmed; "
                        "empty job cannot certify an unassigned root"
                    ) from launch_error
            raise
        finally:
            if info.hThread and not self.start_cleanup_uncertified:
                self.k.CloseHandle(info.hThread)
                self.primary_thread = None

    def root_status(self):
        if not self.process:
            return None
        waited = self.k.WaitForSingleObject(self.process, 0)
        if waited == 0x102:
            return None
        if waited != 0:
            raise ctypes.WinError(ctypes.get_last_error())
        code = w.DWORD()
        if not self.k.GetExitCodeProcess(self.process, ctypes.byref(code)):
            raise ctypes.WinError(ctypes.get_last_error())
        return int(code.value)

    def terminate(self, code=72):
        if self.handle and not self.k.TerminateJobObject(self.handle, code):
            raise ctypes.WinError(ctypes.get_last_error())

    def wait_empty(self, guard):
        while self.accounting()["active_processes"]:
            guard.check()
            time.sleep(min(0.2, guard.remaining()))
        return self.accounting()

    def close(self):
        if self.start_cleanup_uncertified:
            # Retain the exact owned process/thread handles for diagnosis. Closing
            # the job still requests containment termination; it does not certify
            # an unassigned root. No foreign PID is opened or terminated.
            if self.handle:
                self.k.CloseHandle(self.handle)
                self.handle = None
            return
        if self.process:
            self.k.CloseHandle(self.process)
            self.process = None
        if self.handle:
            self.k.CloseHandle(self.handle)  # Always kills any unexpectedly surviving descendants.
            self.handle = None


PROCESS_QUERY = (
    "$ErrorActionPreference='Stop'; "
    "[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new($false); "
    "$self=$PID; $rows=@(Get-CimInstance Win32_Process | ForEach-Object { "
    "[pscustomobject]@{pid=[int]$_.ProcessId;parent=[int]$_.ParentProcessId;"
    "name=$_.Name;exe=$_.ExecutablePath;argv=$_.CommandLine;"
    "creation=$_.CreationDate.ToUniversalTime().ToString('o');"
    "kernel=[string]$_.KernelModeTime;user=[string]$_.UserModeTime} }); "
    "[pscustomobject]@{observer=$self;rows=$rows}|ConvertTo-Json -Depth 4 -Compress"
)


class Observer:
    def __init__(self, helper, receipt: Path, guard):
        self.helper, self.receipt = helper, receipt
        self.number = 0
        self.previous = None
        self.previous_time = None
        self.allowed_ancestors = set()
        self.ancestor_bindings = []
        self.capture(guard, None, initial=True)

    def argv(self, command: str) -> list[str]:
        shell = ctypes.WinDLL("shell32", use_last_error=True)
        shell.CommandLineToArgvW.argtypes = [w.LPCWSTR, ctypes.POINTER(ctypes.c_int)]
        shell.CommandLineToArgvW.restype = ctypes.POINTER(w.LPWSTR)
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.LocalFree.argtypes, kernel.LocalFree.restype = [w.HANDLE], w.HANDLE
        count = ctypes.c_int()
        array = shell.CommandLineToArgvW(command, ctypes.byref(count))
        if not array:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            return [array[i] for i in range(count.value)]
        finally:
            kernel.LocalFree(ctypes.cast(array, w.HANDLE))

    def own_ancestors(self, rows, guard):
        by_pid = {row["pid"]: row for row in rows}
        current = by_pid.get(os.getpid())
        if current is None:
            raise RuntimeError("supervisor absent from process identity inventory")
        allowed_exe = {
            self.helper.canonical(sys.executable),
            self.helper.canonical(getattr(sys, "_base_executable", sys.executable)),
        }
        expected_script = self.helper.canonical(__file__)
        seen = {os.getpid()}
        parent = current["parent"]
        while parent in by_pid and parent not in seen:
            seen.add(parent)
            row = by_pid[parent]
            try:
                same_exe = row["exe"] and self.helper.canonical(row["exe"]) in allowed_exe
                args = self.argv(row["argv"] or "")
                match = any(
                    Path(arg).is_absolute()
                    and self.helper.canonical(arg) == expected_script
                    and args[i + 1 :] == sys.argv[1:]
                    for i, arg in enumerate(args)
                    if i > 0 and Path(arg).is_file()
                )
            except (OSError, ValueError):
                same_exe = match = False
            if same_exe and match:
                self.allowed_ancestors.add(parent)
                self.ancestor_bindings.append(
                    dict(
                        pid=parent,
                        creation=row["creation"],
                        exe=row["exe"],
                        argv=row["argv"],
                        executable_sha256=self.helper.digest(Path(row["exe"]), guard),
                    )
                )
            parent = row["parent"]

    def capture(self, guard, job: WinJob | None, *, initial=False):
        guard.check()
        completed = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", PROCESS_QUERY],
            capture_output=True,
            timeout=min(15, guard.remaining()),
            creationflags=0x08000000,
        )
        guard.check()
        if completed.returncode:
            raise RuntimeError(f"process observation failed: {completed.stderr!r}")
        value = json.loads(completed.stdout.decode("utf-8-sig"))
        rows = value["rows"]
        if not isinstance(rows, list) or len(rows) > 4096:
            raise RuntimeError("bounded process inventory failed")
        if initial:
            self.own_ancestors(rows, guard)
        rows_by_pid = {row["pid"]: row for row in rows}
        stable_ancestors = {
            entry["pid"]
            for entry in self.ancestor_bindings
            if entry["pid"] in rows_by_pid
            and rows_by_pid[entry["pid"]]["creation"] == entry["creation"]
            and rows_by_pid[entry["pid"]]["exe"] == entry["exe"]
            and rows_by_pid[entry["pid"]]["argv"] == entry["argv"]
        }
        allowed = {os.getpid(), int(value["observer"]), *stable_ancestors}
        job_pids = set(job.pids()) if job is not None else set()
        allowed |= job_pids
        previous = (
            {} if self.previous is None else {(r["pid"], r["creation"]): r for r in self.previous}
        )
        conflicts = []
        noise, outside_cpu, unavailable_cpu = [], 0.0, []
        native_compute = {
            "python.exe",
            "pythonw.exe",
            "julia.exe",
            "rscript.exe",
            "matlab.exe",
            "ffmpeg.exe",
            "nvcc.exe",
            "gcc.exe",
            "clang.exe",
            "cl.exe",
            "msbuild.exe",
        }
        for row in rows:
            guard.check()
            if row["pid"] in allowed or row["name"].lower() in ("system", "system idle process"):
                continue
            old = previous.get((row["pid"], row["creation"]))
            increment = None
            if old is not None:
                try:
                    increment = (
                        int(row["kernel"])
                        + int(row["user"])
                        - int(old["kernel"])
                        - int(old["user"])
                    ) / 10_000_000
                except (TypeError, ValueError):
                    unavailable_cpu.append(
                        dict(pid=row["pid"], creation=row["creation"], name=row["name"])
                    )
            command = (row["argv"] or "").lower().replace("\\", "/")
            stage_supervisor = any(
                token in command
                for token in (
                    "stage_c_day",
                    "c7_c8_cases",
                    "c2_timing",
                    "frontier_classical_20261001",
                )
            )
            if increment is not None:
                outside_cpu += max(0.0, increment)
                if increment > 1.0:
                    noise.append(
                        dict(
                            process=row,
                            cpu_increment_seconds=increment,
                            not_a_blanket_name_based_exemption=True,
                        )
                    )
            if row["name"].lower() in native_compute or stage_supervisor:
                conflicts.append(dict(process=row, cpu_increment_seconds=increment))
        observed_time = time.monotonic()
        interval = None if self.previous_time is None else observed_time - self.previous_time
        outside_percent = (
            None if interval is None else 100.0 * outside_cpu / (interval * (os.cpu_count() or 1))
        )
        if outside_percent is not None and outside_percent >= 10.0:
            conflicts.append(
                dict(
                    aggregate_outside_cpu_percent=outside_percent,
                    reason="outside-job hardware-capacity CPU is not below10%",
                )
            )
        self.number += 1
        document = dict(
            observed_utc=datetime.now(timezone.utc).isoformat(),
            rows=rows,
            observer_pid=value["observer"],
            allowed_job_pids=sorted(job_pids),
            verified_own_launcher_ancestors=self.ancestor_bindings,
            conflicts=conflicts,
            other_cpu_increment_observations=noise,
            aggregate_outside_cpu_percent=outside_percent,
            outside_cpu_percent_is_lower_bound=True,
            lower_bound_reason=(
                "new, exited or transient processes can be missed "
                "even when sampled counters are readable"
            ),
            outside_processes_with_unavailable_cpu_counters=unavailable_cpu,
            no_process_name_blanket_exemptions=True,
            transient_external_jobs_between_samples_not_proven_absent=True,
        )
        self.helper.json_new(
            self.receipt / "process_observations" / f"{self.number:06d}.json", document
        )
        self.previous = rows
        self.previous_time = observed_time
        if conflicts:
            raise RuntimeError(f"exclusive slot conflict; {len(conflicts)} unrelated processes")
        return document


def machine_admission(helper, receipt: Path, guard):
    job = WinJob()
    try:
        status = POWER_STATUS()
        if not job.k.GetSystemPowerStatus(ctypes.byref(status)) or status.ACLineStatus != 1:
            raise RuntimeError("timing requires verified AC power")
        completed = subprocess.run(
            ["powercfg", "/getactivescheme"],
            capture_output=True,
            timeout=min(15, guard.remaining()),
            creationflags=0x08000000,
        )
        if (
            completed.returncode
            or BALANCED not in completed.stdout.decode(errors="replace").lower()
        ):
            raise RuntimeError("timing requires frozen Balanced power plan")
        command = (
            "$ErrorActionPreference='Stop'; "
            "[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new($false); "
            "$cpu=(Get-Counter '\\Processor(_Total)\\% Processor Time' -SampleInterval 1 "
            "-MaxSamples 30).CounterSamples.CookedValue|Measure-Object -Average; "
            "[pscustomobject]@{cpu_percent_30s=$cpu.Average;processors=@("
            "Get-CimInstance Win32_Processor|"
            "Select-Object Name,NumberOfCores,NumberOfLogicalProcessors)}|"
            "ConvertTo-Json -Depth 4 -Compress"
        )
        sample = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True,
            timeout=min(45, guard.remaining()),
            creationflags=0x08000000,
        )
        guard.check()
        if sample.returncode:
            raise RuntimeError("fresh 30-second CPU/machine admission failed")
        state = json.loads(sample.stdout.decode("utf-8-sig"))
        affinity, system_affinity = ctypes.c_size_t(), ctypes.c_size_t()
        if not job.k.GetProcessAffinityMask(
            job.k.GetCurrentProcess(), ctypes.byref(affinity), ctypes.byref(system_affinity)
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        state.update(
            ac_line_status=int(status.ACLineStatus),
            powercfg=completed.stdout.decode(errors="replace"),
            required_balanced_guid=BALANCED,
            supervisor_pid=os.getpid(),
            affinity_changed=False,
            observed_process_affinity_mask=int(affinity.value),
            observed_system_affinity_mask=int(system_affinity.value),
        )
        helper.json_new(receipt / "timing_machine_admission.json", state)
        if state["cpu_percent_30s"] is None or state["cpu_percent_30s"] >= 10:
            raise RuntimeError("30-second CPU average not below10%; timing refused")
        return state
    finally:
        job.close()


def phase_process(
    helper,
    receipt: Path,
    name: str,
    argv: list[str],
    worktree: Path,
    guard,
    observer: Observer,
    *,
    limit_seconds=None,
):
    global TERMINATION_UNCERTIFIED
    job = WinJob()
    started = time.monotonic()
    state = dict(
        name=name,
        argv=argv,
        cwd=str(worktree),
        passed=False,
        prospective_entire_phase_wall_guard=guard.seconds,
        own_child_wall_guard_seconds=limit_seconds,
        aggregate_cpu_limit_seconds=None,
    )
    helper.json_new(receipt / f"{name}_admission.json", state)
    try:
        observer.capture(guard, None)
        if name == "rates" and datetime.now(timezone.utc) >= DEADLINE:
            raise RuntimeError("original C8 rates launch deadline missed; not done")
        state["launch"] = job.start(
            argv, worktree, receipt / f"{name}.stdout", receipt / f"{name}.stderr", guard
        )
        if name == "rates" and datetime.fromisoformat(state["launch"]["launched_utc"]) >= DEADLINE:
            raise RuntimeError("actual original rates launch missed the calendar deadline")
        next_observation = time.monotonic() + 30
        while True:
            remaining = guard.remaining()
            if remaining <= RESERVE:
                raise TimeoutError(
                    "entire phase execution censored to retain120-second terminal reserve"
                )
            if limit_seconds is not None and time.monotonic() - started >= limit_seconds:
                raise TimeoutError(f"{name} child wall guard exhausted")
            status = job.root_status()
            if status is not None:
                state["returncode"] = status
                if status != 0:
                    raise RuntimeError(f"{name} returned {status}")
                state["job_terminal"] = job.wait_empty(guard)
                observer.capture(guard, None)
                state["passed"] = True
                return state
            if time.monotonic() >= next_observation:
                # Passive process identity sampling only, with no hashes or outcomes.
                observer.capture(guard, job)
                next_observation = time.monotonic() + 30
            time.sleep(min(1.0, guard.remaining()))
    except BaseException as exc:
        state.update(error=repr(exc), externally_censored=isinstance(exc, TimeoutError))
        try:
            job.terminate()
            if job.start_cleanup_uncertified:
                state["created_own_child_cleanup"] = job.start_cleanup_result
                raise RuntimeError(
                    "start cleanup unconfirmed; job-tree zero cannot certify the created root"
                )
            state["job_terminal"] = job.wait_empty(guard)
        except BaseException as cleanup:
            state["termination_error"] = repr(cleanup)
            state["job_tree_zero_not_certified"] = True
            TERMINATION_UNCERTIFIED = True
        raise
    finally:
        state["subprocess_control_wall_seconds"] = time.monotonic() - started
        if job.start_cleanup_result is not None:
            state["created_own_child_cleanup"] = job.start_cleanup_result
        job.close()
        helper.json_new(receipt / f"{name}_terminal.json", state)


def validate_meta(directory: Path, phase: str, capture: dict, helper, guard):
    guard.check()
    meta = json.loads((directory / "meta.json").read_bytes())
    source_rows = [row for row in capture["bindings"] if row["kind"] == "frozen_checkout_file"]
    code = {
        Path(row["actual_path"]).name: row["sha256"]
        for row in source_rows
        if Path(row["actual_path"]).suffix == ".py"
    }
    spec = next(
        row["sha256"]
        for row in source_rows
        if row["actual_path"].endswith("analysis_spec_stage_c.md")
    )
    lock = next(
        row["sha256"] for row in source_rows if row["actual_path"].endswith("t0_requirements.lock")
    )
    if (
        meta["commit"] != COMMIT
        or meta["dirty"]
        or meta["root"] != 2026100181
        or meta["phase"] != phase
        or meta["item"] != "c8"
        or meta["code_sha256"] != code
        or meta["spec_sha256"] != spec
        or meta["lock_sha256"] != lock
        or meta["numpy"] != "2.0.2"
        or meta["python"] != capture["runtime"]["python"]
    ):
        raise RuntimeError(f"{phase} original producer provenance differs from sealed capture")
    return meta


def validate_rates(directory: Path, inputs: dict, capture: dict, helper, guard):
    raw_rates = (directory / "c8_rates.json").read_bytes()
    rates = json.loads(
        raw_rates, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value))
    )
    rates_sha = hashlib.sha256(raw_rates).hexdigest()
    wanted = {str(i) for i in range(100, 124)}
    if set(rates) != wanted:
        raise RuntimeError("rates are not complete for exactly all24 cases")
    for expected in inputs["cases"]:
        guard.check()
        case = expected["case"]
        entry = rates[str(case["case_index"])]
        if (
            entry["case"] != case
            or entry["m_top"] != 17
            or set(entry["summary"]) != {"knockout_pre"}
        ):
            raise RuntimeError("rates input case/settings/summary mismatch")
        if entry["sigma"]["paths"] != 2**20:
            raise RuntimeError("sigma_Q budget differs from original")
        if set(entry["summary"]["knockout_pre"]["fits"]) != {"primary", "w8", "w12"}:
            raise RuntimeError("rate fit windows differ from the original C8 branches")
        prefix = directory / f"case{case['case_index']}.npy"
        with prefix.open("rb") as stream:
            if stream.read(6) != b"\x93NUMPY":
                raise RuntimeError("not an original prefix NPY")
            version = tuple(stream.read(2))
            if version == (1, 0):
                length = struct.unpack("<H", stream.read(2))[0]
            elif version in ((2, 0), (3, 0)):
                length = struct.unpack("<I", stream.read(4))[0]
            else:
                raise RuntimeError("unsupported prefix NPY version")
            if length > 65536:
                raise RuntimeError("bounded prefix NPY header exceeded")
            header = ast.literal_eval(
                stream.read(length).decode("utf-8" if version == (3, 0) else "latin1")
            )
            if header != dict(descr="<f8", fortran_order=False, shape=(32, 6, 12)):
                raise RuntimeError("prefix shape/dtype/order differs from32x6xm6..17")
            if prefix.stat().st_size - stream.tell() != 32 * 6 * 12 * 8:
                raise RuntimeError("truncated/extra prefix data")
    validate_meta(directory, "rates", capture, helper, guard)
    return rates, rates_sha


def validate_timing(directory: Path, rates: dict, capture: dict, helper, guard):
    packet = json.loads(
        (directory / "c8_timing.json").read_bytes(),
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
    )
    if set(packet["blocks"]) != {str(i) for i in range(100, 124)}:
        raise RuntimeError("timing is not complete for all24 cases")
    for index, block in packet["blocks"].items():
        guard.check()
        if not block["machine"]["idle"] or len(block["warm"]) != 1:
            raise RuntimeError("original idle/warm timing settings failed")
        warm = block["warm"][0]
        if warm["n_top"] != 2**17 or len(warm["scramble_means"]) != 16:
            raise RuntimeError("timing streams/n_top mismatch")
        if set(warm["all16"]) != {str(2**m) for m in range(6, 18)}:
            raise RuntimeError("timing prefix marks differ from the original")
        if (
            block["t_c_0.001"]["n_eps"]
            != rates[index]["summary"]["knockout_pre"]["n_eps"]["0.001"]["point"]
        ):
            raise RuntimeError("timing model not bound to exact rates n(eps)")
    validate_meta(directory, "timing", capture, helper, guard)
    return packet


def copy_outputs(helper, source: Path, target: Path, guard):
    if not source.exists():
        return []
    rows, total = [], 0
    for path in sorted(source.rglob("*")):
        guard.check()
        if not path.is_file():
            continue
        helper.confined(path, source)
        total += path.stat().st_size
        if len(rows) >= 20_000 or total > 2 * 1024**3:
            raise RuntimeError("bounded producer output inventory exhausted")
        rows.append(helper.snapshot(path, target / path.relative_to(source), guard))
    return rows


def source_cache_outputs(helper, worktree: Path, receipt: Path, phase: str, guard):
    stage = worktree / "research/frontier_classical_20261001"
    rows, total = [], 0
    for path in sorted(stage.rglob("*")):
        guard.check()
        if not path.is_file() or "__pycache__" not in path.relative_to(stage).parts:
            continue
        helper.confined(path, stage)
        total += path.stat().st_size
        if len(rows) >= 4096 or total > 1024**3:
            raise RuntimeError("bounded generated cache inventory exhausted")
        rows.append(
            helper.snapshot(path, receipt / f"cache_after_{phase}" / path.relative_to(stage), guard)
        )
    return rows


def wave10_admission(helper, receipt: Path, frozen: dict, guard):
    """Require the actual finite W10 terminal packet before any C8 generation."""
    directory = ROOT / "results/limitation_program_20261001/WAVE10_run002"
    manifest_path, summary_path = directory / "manifest.json", directory / "summary.json"
    if not manifest_path.is_file() or not summary_path.is_file():
        raise RuntimeError("WAVE10 terminal packet absent; C8 not admitted")
    helper.confined(directory, ROOT)
    raw_manifest, raw_summary = manifest_path.read_bytes(), summary_path.read_bytes()
    manifest = json.loads(raw_manifest)
    summary = json.loads(raw_summary)
    required = {
        "A04_mps_run001",
        "A02_quantile_financial_run005",
        "A02_quantile_financial_audit_run001",
    }
    if (
        summary.get("passed") is not True
        or summary.get("archived_or_current_integrity_passed") is not True
        or not required.issubset(summary.get("included_receipts", []))
    ):
        raise RuntimeError(
            "WAVE10 does not certify the required finite terminal dependency packets"
        )
    if (
        manifest.get("terminal_record")
        != "results/limitation_program_20261001/WAVE10_run002/summary.json"
    ):
        raise RuntimeError("WAVE10 terminal record binding differs from the fixed packet")
    owned, inputs = manifest.get("files"), manifest.get("frozen_inputs")
    if (
        not isinstance(owned, dict)
        or not isinstance(inputs, dict)
        or len(owned) + len(inputs) > 50_000
    ):
        raise RuntimeError("bounded WAVE10 recognized SHA maps missing/exhausted")
    actual_owned = {
        helper.canonical(path)
        for path in directory.rglob("*")
        if path.is_file() and path != manifest_path
    }
    seen, total = {}, 0
    for expected_map, is_owned in ((owned, True), (inputs, False)):
        for relative, expected_sha in expected_map.items():
            guard.check()
            if Path(relative).is_absolute() or ".." in Path(relative).parts:
                raise RuntimeError("WAVE10 map is not a canonical ROOT-relative binding")
            path = helper.confined(ROOT / relative, directory if is_owned else ROOT)
            identity = helper.canonical(path)
            if seen.setdefault(identity, expected_sha) != expected_sha:
                raise RuntimeError("WAVE10 canonical path has unequal-SHA aliases")
            total += path.stat().st_size
            if total > 16 * 1024**3:
                raise RuntimeError("WAVE10 input byte bound exhausted")
            if helper.digest(path, guard) != expected_sha:
                raise RuntimeError(f"WAVE10 actual prerequisite SHA mismatch: {relative}")
    owned_identities = {helper.canonical(ROOT / relative) for relative in owned}
    if owned_identities != actual_owned or helper.canonical(summary_path) not in owned_identities:
        raise RuntimeError("WAVE10 owned inventory/terminal summary is incomplete")
    if seen[helper.canonical(summary_path)] != hashlib.sha256(raw_summary).hexdigest():
        raise RuntimeError("parsed WAVE10 summary bytes differ from its terminal binding")
    seen[helper.canonical(manifest_path)] = hashlib.sha256(raw_manifest).hexdigest()
    rows = copy_outputs(helper, directory, receipt / "prerequisite_wave10", guard)
    for row in rows:
        if row["sha256"] != seen[row["actual_path"]]:
            raise RuntimeError("WAVE10 copy differs from the admitted exact source bytes")
        identity = row["snapshot_path"]
        if identity in frozen and frozen[identity] != row["sha256"]:
            raise RuntimeError("WAVE10 snapshot equal-SHA merge failed")
        frozen[identity] = row["sha256"]
    helper.json_new(
        receipt / "wave10_terminal_admission.json",
        dict(
            passed=True,
            actual_terminal_receipt=str(directory),
            immutable_snapshot_bindings=rows,
            verified_actual_owned_files=len(owned),
            verified_actual_input_references=len(inputs),
            input_bytes_charged_to_rates_wall=total,
            required_financial_and_mps_terminal_packets=sorted(required),
            legacy_global_live_mismatches_not_waived=True,
            actual_live_paths_are_provenance_only=True,
            fixture_credit=0,
        ),
    )


def terminal_seal(
    helper,
    receipt: Path,
    summary: dict,
    frozen: dict,
    guard,
    previous_frozen: dict,
    runtime_live: dict,
):
    guard.check()
    helper.json_new(receipt / "summary.json", summary)
    own = {}
    total = 0
    for path in sorted(receipt.rglob("*")):
        guard.check()
        if not path.is_file():
            continue
        helper.confined(path, receipt)
        total += path.stat().st_size
        if len(own) >= 25_000 or total > 3 * 1024**3:
            raise RuntimeError("terminal owned-byte inventory exhausted")
        own[helper.canonical(path)] = helper.digest(path, guard)
    for path, hashed in frozen.items():
        identity = helper.canonical(path)
        if identity not in own or own[identity] != hashed:
            raise RuntimeError("frozen snapshot missing/changed or conflicting SHA")
    previous = {}
    for path, hashed in previous_frozen.items():
        guard.check()
        source = helper.confined(Path(path), ROOT)
        identity = helper.canonical(source)
        if identity in frozen and frozen[identity] != hashed:
            raise RuntimeError("original admission input cannot overwrite a frozen snapshot SHA")
        if helper.digest(source, guard) != hashed:
            raise RuntimeError("immutable original admission input changed before terminal seal")
        previous[identity] = hashed
        guard.check()
    root = ROOT.resolve(strict=True)
    relative = lambda path: Path(path).resolve(strict=True).relative_to(root).as_posix()  # noqa: E731
    terminal_inputs = {relative(path): hashed for path, hashed in frozen.items()}
    for path, hashed in previous.items():
        guard.check()
        name = relative(path)
        if name in terminal_inputs and terminal_inputs[name] != hashed:
            raise RuntimeError("original admission terminal-map merge requires equal SHA")
        terminal_inputs[name] = hashed
        guard.check()
    external_runtime = {}
    base = Path(sys.base_prefix).resolve(strict=True)
    git_exe = Path(shutil.which("git") or "").resolve(strict=True)
    for name, expected in runtime_live.items():
        guard.check()
        lexical = Path(os.path.abspath(name))
        actual = lexical.resolve(strict=True)
        if actual != lexical or not actual.is_file() or helper.digest(actual, guard) != expected:
            raise RuntimeError("fresh current runtime terminal alias or SHA mismatch")
        if actual.is_relative_to(root):
            key = actual.relative_to(root).as_posix()
            if key in terminal_inputs and terminal_inputs[key] != expected:
                raise RuntimeError("current ROOT runtime canonical expected SHA conflict")
            terminal_inputs[key] = expected
        else:
            if not actual.is_relative_to(base) and actual != git_exe:
                raise RuntimeError("only actual base runtime and exact captured Git tool external")
            external_runtime[str(actual)] = expected
        guard.check()
    manifest = dict(
        schema="c8_local_terminal_manifest_v1",
        passed=summary["passed"],
        files={relative(path): hashed for path, hashed in own.items()},
        frozen_inputs=terminal_inputs,
        external_runtime_inputs=external_runtime,
        external_runtime_scopes=dict(
            actual_base_prefix=str(base), actual_git_executable=str(git_exe)
        ),
        terminal_record=relative(receipt / "summary.json"),
        manifest_self_hash_excluded=True,
        global_immutable_live_input_binding=False,
        original_admission_inputs_strictly_bound_and_reverified=True,
        original_admission_input_references=len(previous),
        current_runtime_capture_available=bool(runtime_live),
        reused_archive_and_current_runtime_both_fresh_terminal_verified=bool(runtime_live),
        old_failed_partial_runtime_is_not_a_PASS=True,
        entire_active_phase_wall_seconds_before_terminal_write=time.monotonic() - guard.started,
        active_phase_wall_limit_seconds=guard.seconds,
        owned_bytes=total,
        fixture_credit=0,
        quantum_advantage_claim=False,
    )
    serialized = json.dumps(manifest, indent=2, allow_nan=False) + "\n"
    guard.check()
    with (receipt / "manifest.json").open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(serialized)
    guard.check()


def verify_authors(helper, executed: list[dict], guard):
    for row in executed:
        for key in ("actual_path", "snapshot_path"):
            if helper.digest(Path(row[key]), guard) != row["sha256"]:
                raise RuntimeError("executed author source/preflight actual/copy changed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preflight", default=str(PREFLIGHT))
    args = ap.parse_args()
    if os.name != "nt":
        raise RuntimeError("Windows only")
    if Path(args.preflight).resolve(strict=True) != PREFLIGHT.resolve(strict=True):
        raise RuntimeError("no preflight path override")
    if Path(__file__).resolve(strict=True) != (AUTHOR_DIR / "run_c8_supervised_v3.py").resolve(
        strict=True
    ):
        raise RuntimeError("root executes only the authorized supervisor author path")
    started, own_cpu = time.monotonic(), time.process_time()
    value = json.loads(PREFLIGHT.read_bytes())
    receipt = Path(value["receipt"])
    wanted = ROOT / "results/limitation_program_20261001/C8_execution_run003"
    if receipt.absolute() != wanted.absolute() or receipt.exists():
        raise RuntimeError("fresh exact C8 receipt required")
    receipt.parent.resolve(strict=True).relative_to(ROOT.resolve(strict=True))
    # All preparation after this mutation has preserved terminal failure evidence.
    receipt.mkdir(exist_ok=False)
    frozen, previous_frozen, runtime_live, executed, helper, observer = {}, {}, {}, [], None, None
    summary = dict(
        passed=False,
        commit=COMMIT,
        fixture_credit=0,
        financial_adoption=False,
        quantum_advantage_claim=False,
        oracle_phase_executed=False,
        expected_factor_hashes_not_worker_observed=True,
        timing_rates_hash_is_external_not_internal_read_trace=True,
        model_timing_without20_replication_accuracy_confirmation=True,
    )
    active_guard = None
    failure = None
    try:
        for key in ("PYTHONPATH", "PYTHONHOME", "NUMBA_CACHE_DIR"):
            if os.environ.get(key):
                raise RuntimeError(f"nonempty inherited {key} is outside captured C8 runtime scope")
        # Tiny bootstrap copy/verification before importing even the companion helper.
        for name in OWN_FILES:
            source, target = AUTHOR_DIR / name, receipt / "executed_sources" / name
            if source.is_symlink() or not source.is_file() or source.stat().st_size > 1024**2:
                raise RuntimeError("bounded author source snapshot admission failed")
            data = source.read_bytes()
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(data)
            hashed = hashlib.sha256(data).hexdigest()
            if (
                hashlib.sha256(target.read_bytes()).hexdigest() != hashed
                or hashlib.sha256(source.read_bytes()).hexdigest() != hashed
            ):
                raise RuntimeError("author source/copy equal-SHA failed")
            actual, copied = (
                os.path.normcase(str(source.resolve())),
                os.path.normcase(str(target.resolve())),
            )
            frozen[copied] = hashed
            executed.append(dict(actual_path=actual, snapshot_path=copied, sha256=hashed))
            if time.monotonic() - started > 30:
                raise TimeoutError("bootstrap copy30-second guard exhausted")
        helper_path = receipt / "executed_sources/capture_c8_prerun_inventory_v3.py"

        def bootstrap_check():
            if time.monotonic() - started > 30:
                raise TimeoutError("bootstrap copy30-second guard exhausted")

        bootstrap_check()
        previous_admission = dict(
            complete_old_maps_delegated_to_observed_inventory900s_before_scientific_import=True,
            old_failed_attempts_are_not_runtime_or_C8_PASS=True,
        )
        summary["original_admission_failure_fixture_or_measurement_credit"] = 0
        summary["newly_preregistered_operational_admission_not_numerical_retry"] = True
        specification = importlib.util.spec_from_file_location("c8_owned_capture", helper_path)
        helper = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(helper)
        active_guard = helper.Guard(43_200, started=started)
        frozen_preflight = receipt / "executed_sources/c8_execution_preflight_v3.json"
        value = helper.policy(frozen_preflight, active_guard)
        previous_frozen.update(helper.prior_expected_metadata(value, active_guard))
        worktree, output = Path(value["execution_worktree"]), Path(value["output_base"])
        worktree.resolve(strict=True).relative_to(ROOT.resolve(strict=True))
        output.parent.resolve(strict=True).relative_to(ROOT.resolve(strict=True))
        if worktree.resolve() != (ROOT / ".context/stage_c_c8_20261003_run003").resolve():
            raise RuntimeError("fresh worktree path differs from prospective admission")
        if output.resolve() != (ROOT / "results/frontier_classical_20261001").resolve():
            raise RuntimeError("original output base changed")
        if (output / "c8/rates").exists() or (output / "c8/timing").exists():
            raise RuntimeError("original C8 output already exists; no overwrite/retry")
        if helper.canonical(sys.executable) != helper.canonical(value["interpreter"]):
            raise RuntimeError("supervisor is not using pinned interpreter")
        helper.assert_checkout(worktree, active_guard)
        if any((worktree / "research/frontier_classical_20261001").rglob("*.nbc")):
            raise RuntimeError("fresh C8 worktree has pre-existing native kernel cache")
        helper.json_new(
            receipt / "protocol.json",
            dict(
                commit=COMMIT,
                executed_source_bindings=executed,
                executed_dependencies=[
                    dict(
                        snapshot=Path(row["snapshot_path"])
                        .relative_to(receipt.resolve())
                        .as_posix(),
                        sha256=row["sha256"],
                        actual_path=row["actual_path"],
                        actual_path_is_scoped_provenance_only=True,
                    )
                    for row in executed
                ],
                preflight_sha256=frozen[helper.canonical(frozen_preflight)],
                local_only=True,
                network_allowed=False,
                rates_entire_phase_wall_seconds=43_200,
                timing_entire_phase_wall_seconds=28_800,
                no_aggregate_cpu_limit=True,
                capture_precedes_original_import_generation_and_producer=True,
                previous_admission_bindings=previous_admission,
                original_failure_fixture_or_measurement_credit=0,
                mutable_actual_source_paths_are_provenance_only=True,
            ),
        )
        observer = Observer(helper, receipt, active_guard)
        wave10_admission(helper, receipt, frozen, active_guard)
        verify_authors(helper, executed, active_guard)
        inventory_command = [
            str(sys.executable),
            "-B",
            str(helper_path),
            "--preflight",
            str(frozen_preflight),
            "--out",
            str(receipt / "inventory"),
        ]
        phase_process(
            helper,
            receipt,
            "inventory",
            inventory_command,
            worktree,
            active_guard,
            observer,
            limit_seconds=900,
        )
        capture = json.loads(
            (receipt / "inventory/source_runtime_capture_before_generation.json").read_bytes()
        )
        inputs = json.loads((receipt / "inventory/expected_inputs_sealed.json").read_bytes())
        if not inputs["passed"] or len(inputs["cases"]) != 24:
            raise RuntimeError("prospective input inventory did not seal all24 inputs")
        previous_record = json.loads(
            (receipt / "inventory/previous_admission_bindings.json").read_bytes()
        )
        if previous_record["original_owned_and_frozen_inputs"] != previous_frozen:
            raise RuntimeError(
                "child full historical byte proof differs from fixed parent expectations"
            )
        for path, hashed in capture["frozen_input_sha256"].items():
            identity = helper.canonical(helper.confined(Path(path), receipt / "inventory"))
            if identity in frozen and frozen[identity] != hashed:
                raise RuntimeError("captured source/runtime canonical equal-SHA merge failed")
            frozen[identity] = hashed
        for path, hashed in capture["reused_runtime_snapshot_sha256"].items():
            identity = helper.canonical(Path(path))
            if previous_frozen.get(identity) != hashed:
                raise RuntimeError("reused runtime archive absent from exact prior diagnostic maps")
        runtime_live.update(capture["actual_runtime_sha256"])
        for row in inputs["cases"]:
            path = helper.confined(
                Path(row["factor_snapshot"]), receipt / "inventory/expected_factors"
            )
            if helper.digest(path, active_guard) != row["factor_sha256"]:
                raise RuntimeError("expected factor snapshot mismatch")
            identity = helper.canonical(path)
            if identity in frozen and frozen[identity] != row["factor_sha256"]:
                raise RuntimeError("conflicting canonical factor SHA")
            frozen[identity] = row["factor_sha256"]
        helper.verify_capture(capture, active_guard)
        helper.assert_checkout(worktree, active_guard)
        verify_authors(helper, executed, active_guard)
        module = "research.frontier_classical_20261001.c7_c8_cases"
        rates_command = [
            str(sys.executable),
            "-m",
            module,
            "rates",
            "--item",
            "c8",
            "--out",
            str(output),
        ]
        summary["rates_process"] = phase_process(
            helper, receipt, "rates", rates_command, worktree, active_guard, observer
        )
        rates_dir = output / "c8/rates"
        rates, rates_sha = validate_rates(rates_dir, inputs, capture, helper, active_guard)
        helper.verify_capture(capture, active_guard)
        helper.assert_checkout(worktree, active_guard)
        summary["rates_output_copies"] = copy_outputs(
            helper, rates_dir, receipt / "producer_outputs/rates", active_guard
        )
        admitted_rates_copy = next(
            row
            for row in summary["rates_output_copies"]
            if row["actual_path"] == helper.canonical(rates_dir / "c8_rates.json")
        )
        if admitted_rates_copy["sha256"] != rates_sha:
            raise RuntimeError("rates output copy differs from the exact bytes validated")
        summary["rates_cache_copies"] = source_cache_outputs(
            helper, worktree, receipt, "rates", active_guard
        )
        summary["rates_entire_phase_wall_seconds"] = time.monotonic() - started
        active_guard.check()
        helper.json_new(
            receipt / "rates_phase_complete.json",
            dict(
                passed=True,
                all24_complete=True,
                wall_seconds=summary["rates_entire_phase_wall_seconds"],
                fixture_credit=0,
            ),
        )

        timing_started = time.monotonic()
        active_guard = helper.Guard(28_800, started=timing_started)
        helper.verify_capture(capture, active_guard)
        helper.assert_checkout(worktree, active_guard)
        machine_admission(helper, receipt, active_guard)
        verify_authors(helper, executed, active_guard)
        observer.capture(active_guard, None)
        rates_input = rates_dir / "c8_rates.json"
        binding = helper.snapshot(rates_input, receipt / "timing_input/c8_rates.json", active_guard)
        if binding["sha256"] != rates_sha:
            raise RuntimeError("timing rates input differs from the parsed validated rates packet")
        frozen[binding["snapshot_path"]] = binding["sha256"]
        helper.json_new(
            receipt / "timing_input_admission.json",
            dict(
                exact_input_binding=binding,
                all24_rates_complete_before_timing=True,
                internal_read_trace=False,
                no_input_writers_allowed=True,
            ),
        )
        timing_command = [
            str(sys.executable),
            "-m",
            module,
            "timing",
            "--item",
            "c8",
            "--out",
            str(output),
            "--rates",
            str(rates_input),
        ]
        summary["timing_process"] = phase_process(
            helper, receipt, "timing", timing_command, worktree, active_guard, observer
        )
        if helper.digest(rates_input, active_guard) != binding["sha256"]:
            raise RuntimeError("original rates input changed during timing")
        if helper.digest(Path(binding["snapshot_path"]), active_guard) != binding["sha256"]:
            raise RuntimeError("immutable timing rates-input snapshot changed")
        validate_timing(output / "c8/timing", rates, capture, helper, active_guard)
        helper.verify_capture(capture, active_guard)
        helper.assert_checkout(worktree, active_guard)
        summary["timing_output_copies"] = copy_outputs(
            helper, output / "c8/timing", receipt / "producer_outputs/timing", active_guard
        )
        summary["timing_cache_copies"] = source_cache_outputs(
            helper, worktree, receipt, "timing", active_guard
        )
        summary.update(
            passed=True,
            rates_complete24=True,
            timing_complete24=True,
            timing_input_sha256=binding["sha256"],
            timing_input_sha_after_equals_before=True,
            rates_timing_complete_but_c8_oracle_decision_still_open=True,
            timing_entire_phase_wall_seconds=time.monotonic() - timing_started,
        )
    except BaseException as exc:
        failure = exc
        summary.update(
            passed=False, error=repr(exc), externally_censored=isinstance(exc, TimeoutError)
        )
    finally:
        summary.update(
            total_wall_seconds=time.monotonic() - started,
            supervisor_own_cpu_seconds=time.process_time() - own_cpu,
            all_failed_or_censored_phases_fixture_credit=0,
            no_retries=True,
            no_original_producer_or_spec_edits=True,
        )
        if helper is None:
            # Even a post-mkdir bootstrap failure is retained without certification.
            with (receipt / "FAILED_UNSEALED.json").open("x", encoding="utf-8") as stream:
                json.dump(summary, stream, indent=2)
        else:
            try:
                if TERMINATION_UNCERTIFIED:
                    raise RuntimeError(
                        "job-tree zero not certified; no output verification or manifest permitted"
                    )
                active_guard.check()
                # Capture partial output once, after phase_process terminal containment.
                output = Path(value["output_base"])
                for phase in ("rates", "timing"):
                    source = output / "c8" / phase
                    target = receipt / "producer_outputs" / phase
                    if source.exists() and not target.exists():
                        summary[f"retained_partial_{phase}"] = copy_outputs(
                            helper, source, target, active_guard
                        )
                verify_authors(helper, executed, active_guard)
                if observer is not None:
                    observer.capture(active_guard, None)
                terminal_seal(
                    helper, receipt, summary, frozen, active_guard, previous_frozen, runtime_live
                )
            except BaseException as sealing:
                summary.update(
                    passed=False, terminal_seal_error=repr(sealing), manifest_certified=False
                )
                # A hard-limit exception after final manifest write invalidates the certificate.
                if (receipt / "manifest.json").exists():
                    (receipt / "manifest.json").rename(
                        receipt / "manifest_invalid_after_hard_guard.json"
                    )
                with (receipt / "FAILED_UNSEALED.json").open("x", encoding="utf-8") as stream:
                    json.dump(summary, stream, indent=2)
        if failure is not None or not summary["passed"]:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
