"""Preserve C8 run002 partial bytes as a separate bounded local failure diagnostic.

Metadata only: CPU300/admission270/wall900/admission840; no scientific imports,
case generation, kernels, rates, timing, proof or fixture execution. Old receipt
and mutable progress/STATUS are read-only. This helper itself becomes immutable
at its first execution and is copied into the fresh diagnostic before hashing.
"""

from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import traceback

ROOT = Path("C:/Users/prith/quantum_option_pricing").resolve()
BASE = ROOT / "results/limitation_program_20261001"
SOURCE = BASE / "C8_execution_run002"
OUTPUT = BASE / "C8_admission_failure_run002"
OBSERVATION = ROOT / ".context/c8_run002_post_terminal_process_observation.json"
REVIEW = BASE / "C8_root_review_run002"
PYTHON = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
PYTHON_SHA = "41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5"
AUTHORS = {
    "run_c8_supervised_v2.py": (
        "276d2c26a356b4d8919181901922fab9a3994cab695ce9de0a49bf67cb1f4705"
    ),
    "capture_c8_prerun_inventory_v2.py": (
        "9dd9c11964f30593edf147110b474c7ec394baf3ed516c6b2f0eafa50b227ab4"
    ),
    "c8_execution_preflight_v2.json": (
        "9ea03262155edefb425af4e9441b6895d523c9141f8d1826d070c865acc35ad6"
    ),
    "C8_EXECUTION_PREFLIGHT_V2.md": (
        "e5348d2d8078485d9dac71f8d7ece8c1129e740da52dce7d412546f2935a1ea4"
    ),
}
CPU, ADMISSION_CPU, WALL, ADMISSION_WALL = 300, 270, 900, 840
MAX_FILES, MAX_BYTES, MAX_METADATA = 25_000, 2 * 1024**3, 32 * 1024**2


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fingerprint(path):
    s = path.stat()
    return (
        s.st_dev,
        s.st_ino,
        s.st_size,
        s.st_mtime_ns,
        s.st_ctime_ns,
        getattr(s, "st_file_attributes", None),
        getattr(s, "st_reparse_tag", None),
    )


class Guard:
    def __init__(self):
        require(os.name == "nt", "Pinned Windows diagnostic required")
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetCurrentProcess.argtypes = []
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [
            ctypes.POINTER(wintypes.FILETIME)
        ] * 4
        kernel.GetProcessTimes.restype = wintypes.BOOL
        fields = [wintypes.FILETIME() for _ in range(4)]
        require(
            kernel.GetProcessTimes(kernel.GetCurrentProcess(), *(ctypes.byref(f) for f in fields)),
            "Process creation time unavailable",
        )
        created = ((fields[0].dwHighDateTime << 32) | fields[0].dwLowDateTime) / 10_000_000
        created -= 11_644_473_600
        self.started = time.monotonic() - max(0, time.time() - created)
        self.hashed_bytes = 0

    def check(self, terminal=False):
        cpu, wall = (CPU, WALL) if terminal else (ADMISSION_CPU, ADMISSION_WALL)
        require(time.process_time() < cpu, "Metadata CPU limit exhausted")
        require(time.monotonic() - self.started < wall, "Metadata wall limit exhausted")


def confined(path):
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    resolved = path.resolve(strict=True)
    resolved.relative_to(ROOT)
    require(path == resolved, "Aliased or escaped ROOT path")
    return resolved


def key(path):
    return confined(path).relative_to(ROOT).as_posix()


def inventory(directory, guard):
    paths, total, spellings = {}, 0, set()
    for parent, dirs, files in os.walk(directory, followlinks=False):
        guard.check()
        for folder in dirs:
            confined(Path(parent) / folder)
        for name in files:
            path = confined(Path(parent) / name)
            token = path.relative_to(ROOT).as_posix()
            require(token.casefold() not in spellings, "Windows path alias inventory")
            spellings.add(token.casefold())
            paths[token] = fingerprint(path)
            total += paths[token][2]
            require(
                len(paths) <= MAX_FILES and total <= MAX_BYTES,
                "Complete partial inventory bound exhausted",
            )
    return paths, total


def digest(path, guard, terminal=False):
    guard.check(terminal)
    path = confined(path)
    before, result = fingerprint(path), hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            result.update(block)
            guard.hashed_bytes += len(block)
            require(guard.hashed_bytes <= MAX_BYTES * 3, "Full hash-work bound exhausted")
            guard.check(terminal)
    require(fingerprint(path) == before, "File changed during full hashing")
    return result.hexdigest()


def read(path, guard):
    guard.check()
    path = confined(path)
    before = fingerprint(path)
    require(before[2] <= MAX_METADATA, "Metadata item too large")
    value = json.loads(path.read_bytes())
    require(fingerprint(path) == before, "Metadata changed while reading")
    guard.check()
    return value


def write_new(path, value, guard, terminal=False):
    guard.check(terminal)
    data = (json.dumps(value, indent=2, allow_nan=False) + "\n").encode()
    guard.check(terminal)
    require(len(data) <= MAX_METADATA, "New metadata item too large")
    with path.open("xb") as stream:
        for offset in range(0, len(data), 1 << 20):
            guard.check(terminal)
            stream.write(data[offset : offset + (1 << 20)])
        stream.flush()
        os.fsync(stream.fileno())
    guard.check(terminal)


def copy_new(path, destination, guard):
    guard.check()
    before = fingerprint(path)
    require(before[2] <= MAX_METADATA, "Snapshot item too large")
    data = path.read_bytes()
    guard.check()
    require(fingerprint(path) == before, "Snapshot source changed")
    with destination.open("xb") as stream:
        stream.write(data)
    require(digest(destination, guard) == digest(path, guard), "Snapshot copy SHA differs")


def preserve(guard):
    own_source = confined(__file__)
    copy_new(own_source, OUTPUT / own_source.name, guard)
    copy_new(OBSERVATION, OUTPUT / "post_terminal_CIM_observation.json", guard)
    before, total = inventory(SOURCE, guard)
    require(
        len(before) == 18_126 and total == 1_052_168_451,
        "Root's observed complete partial inventory changed",
    )
    require(not (SOURCE / "manifest.json").exists(), "Original attempt must remain unsealed")
    failed = read(SOURCE / "FAILED_UNSEALED.json", guard)
    terminal = read(SOURCE / "inventory_terminal.json", guard)
    observation = read(SOURCE / "process_observations/000021.json", guard)
    protocol = read(SOURCE / "protocol.json", guard)
    current = read(OBSERVATION, guard)
    require(
        failed["passed"] is False
        and failed["manifest_certified"] is False
        and failed["fixture_credit"] == failed["all_failed_or_censored_phases_fixture_credit"] == 0,
        "Original authoritative failure classification differs",
    )
    require(
        terminal["name"] == "inventory"
        and terminal["passed"] is False
        and terminal["job_terminal"]["active_processes"] == 0,
        "Inventory job not terminal-empty",
    )
    require(
        terminal["launch"]["pid"] == 21236
        and terminal["launch"]["assigned_suspended_before_resume"] is True,
        "Actual native Job launch binding differs",
    )
    require(
        observation["outside_cpu_percent_is_lower_bound"] is True
        and observation["aggregate_outside_cpu_percent"] == 15.31532744537943
        and len(observation["conflicts"]) == 1
        and observation["allowed_job_pids"] == [],
        "Actual terminal operational conflict differs",
    )
    launch = [r for r in observation["verified_own_launcher_ancestors"] if r["pid"] == 38940]
    require(
        len(launch) == 1
        and launch[0]["creation"] == "2026-10-03T08:40:19.1593250Z"
        and launch[0]["executable_sha256"] == PYTHON_SHA,
        "PID plus creation launcher binding differs",
    )
    require(
        current["schema"] == "c8-post-terminal-root-CIM-observation-v1"
        and current["rows"] == []
        and current["point_in_time_only"] is True,
        "Fresh pre-helper observation is not Python/Ruff-empty",
    )
    require(
        protocol["local_only"] is True and protocol["network_allowed"] is False,
        "Original execution provenance differs",
    )
    for name in (
        "rates_admission.json",
        "rates_terminal.json",
        "timing_admission.json",
        "timing_terminal.json",
    ):
        require(not (SOURCE / name).exists(), "Original rates/timing launch evidence present")
    for name in (
        "source_runtime_capture_before_generation.json",
        "expected_inputs_sealed.json",
        "inventory_terminal.json",
    ):
        require(
            not (SOURCE / "inventory" / name).exists(),
            "Generation-stage completed artifact present",
        )
    require(
        not (SOURCE / "inventory/expected_factors").exists(), "Expected factors already generated"
    )
    frozen = {}
    for name, expected_stat in before.items():
        guard.check()
        path = confined(name)
        require(fingerprint(path) == expected_stat, "Original partial stat changed before hashing")
        frozen[name] = digest(path, guard)
    require(digest(PYTHON, guard) == PYTHON_SHA, "Pinned executed interpreter differs")
    frozen[key(PYTHON)] = PYTHON_SHA
    frozen[key(own_source)] = digest(own_source, guard)
    frozen[key(OBSERVATION)] = digest(OBSERVATION, guard)
    review_manifest = read(REVIEW / "manifest.json", guard)
    frozen[key(REVIEW / "manifest.json")] = digest(REVIEW / "manifest.json", guard)
    review_inventory, _ = inventory(REVIEW, guard)
    require(
        set(review_inventory)
        == set(review_manifest["files"]) | {key(REVIEW / "manifest.json")},
        "Root review exact owned membership differs",
    )
    for name, expected in review_manifest["files"].items():
        require(confined(name).is_relative_to(REVIEW), "Root review own path escaped")
        require(digest(ROOT / name, guard) == expected, "Root review owned SHA differs")
        require(name not in frozen or frozen[name] == expected, "Root review equal-SHA conflict")
        frozen[name] = expected
    review_author_pins = {}
    for name, expected in review_manifest["frozen_inputs"].items():
        path = confined(name)
        require(
            path.parent == ROOT / "research/limitation_program_20261001", "Review input escaped"
        )
        require(
            path.name in AUTHORS and expected == AUTHORS[path.name], "Review author pin differs"
        )
        require(digest(path, guard) == expected, "Root review live author SHA differs")
        require(name not in frozen or frozen[name] == expected, "Review frozen equal-SHA conflict")
        review_author_pins[path.name] = expected
        frozen[name] = expected
    require(review_author_pins == AUTHORS, "Root review complete author quartet differs")
    for name, expected in AUTHORS.items():
        copy_path = SOURCE / "executed_sources" / name
        require(frozen[key(copy_path)] == expected, "Executed immutable author quartet differs")
    copied = {
        Path(r["snapshot_path"]).name.casefold(): r["sha256"]
        for r in protocol["executed_source_bindings"]
    }
    require(
        copied == {n.casefold(): v for n, v in AUTHORS.items()},
        "Source protocol author quartet differs",
    )
    write_new(
        OUTPUT / "root_launch_binding.json",
        dict(
            observed_in_saved_terminal_record=key(SOURCE / "process_observations/000021.json"),
            launcher=launch[0],
            inventory_launch=terminal["launch"],
            post_terminal_observation=key(OUTPUT / "post_terminal_CIM_observation.json"),
            observation_is_point_in_time_only=True,
        ),
        guard,
    )
    # A new full fresh resolution/hash of every actual partial file follows the
    # first read pass. All old files, including bytecode and incomplete copies,
    # remain unchanged and receive no StageC success/fixture credit.
    for name, expected in frozen.items():
        guard.check()
        require(digest(ROOT / name, guard) == expected, "Fresh terminal full SHA differs")
    after, after_total = inventory(SOURCE, guard)
    require(after == before and after_total == total, "Old partial membership or bytes changed")
    summary = dict(
        schema="root-c8-admission-failure-diagnostic-v1",
        passed=False,
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        source_receipt=key(SOURCE),
        diagnostic_integrity_verified=True,
        original_rates_launched=False,
        original_timing_launched=False,
        original_scientific_case_generation_not_reached=True,
        source_runtime_capture_before_generation_absent=True,
        all_actual_receipt_files_bound=len(before),
        all_actual_receipt_bytes_bound=total,
        original_attempt_immutable=True,
        new_test_or_measurement_credit=0,
        inventory_job_terminal_active_processes=0,
        visible_unrelated_Python_processes=[],
        visible_process_observation_is_point_in_time_only=True,
        post_terminal_observed_utc=current["observed_utc"],
        no_certified_StageC_manifest=True,
        not_a_success_certificate=True,
        not_a_sealed_C8_result=True,
        reason=(
            "Outside-job observed CPU15.31532744537943% exceeded fixed10%; "
            "incomplete runtime capture preserved."
        ),
        observations=[
            dict(
                observation="000021",
                utc=observation["observed_utc"],
                outside_CPU_percent_lower_bound=observation["aggregate_outside_cpu_percent"],
                conflicts=observation["conflicts"],
            )
        ],
        launcher_pid_plus_creation_binding=launch[0],
        executed_helper_source=key(OUTPUT / own_source.name),
        scientific_optional_imports=0,
        new_rates_timings_prices_factors_fixtures_proofs=0,
        mutable_progress_STATUS_edits=0,
        process_CPU_seconds_after_full_verification=time.process_time(),
        wall_seconds_after_full_verification=time.monotonic() - guard.started,
        process_CPU_limit_seconds=CPU,
        process_wall_limit_seconds=WALL,
        new_work_CPU_admission_seconds=ADMISSION_CPU,
        new_work_wall_admission_seconds=ADMISSION_WALL,
        complete_fresh_partial_rehashes=len(before),
        complete_fresh_input_rehashes=len(frozen),
        total_hashwork_bytes=guard.hashed_bytes,
        next="Fresh preregistered quiet admission only; never retry or overwrite this attempt.",
    )
    write_new(OUTPUT / "summary.json", summary, guard)
    owned, _ = inventory(OUTPUT, guard)
    files = {name: digest(ROOT / name, guard) for name in owned}
    manifest = dict(
        files=files,
        frozen_inputs=frozen,
        terminal_record=key(OUTPUT / "summary.json"),
        manifest_self_hash_excluded=True,
        single_immutable_manifest=True,
        diagnostic_only_preserved_failure_not_C8_success=True,
        process_CPU_limit_seconds=CPU,
        process_wall_limit_seconds=WALL,
        process_CPU_seconds_after_bulk_hashing=time.process_time(),
        wall_seconds_after_bulk_hashing=time.monotonic() - guard.started,
    )
    write_new(OUTPUT / "manifest.json", manifest, guard, terminal=True)
    print(
        json.dumps(
            dict(
                diagnostic_integrity_PASS=True,
                original_stage_C_passed=False,
                old_partial_files=len(before),
                old_partial_bytes=total,
                own_files=len(files),
                frozen_files=len(frozen),
                manifest_sha256=digest(OUTPUT / "manifest.json", guard, terminal=True),
                process_CPU_seconds=time.process_time(),
                wall_seconds=time.monotonic() - guard.started,
            )
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    guard = Guard()
    require(
        confined(sys.executable) == PYTHON and sys.dont_write_bytecode, "Pinned Python -B required"
    )
    require(
        args.output.is_absolute() and args.output == OUTPUT and not OUTPUT.exists(),
        "Fresh exact diagnostic required",
    )
    guard.check()
    OUTPUT.mkdir(exist_ok=False)
    try:
        preserve(guard)
        return 0
    except BaseException as error:
        try:
            if (OUTPUT / "manifest.json").exists():
                (OUTPUT / "manifest.json").rename(OUTPUT / "manifest_invalid_after_hard_guard.json")
        except BaseException:
            pass
        try:
            write_new(
                OUTPUT / "failure.json",
                dict(
                    passed=False,
                    error=repr(error)[:4096],
                    traceback=traceback.format_exc()[-16000:],
                    fixture_credit=0,
                    original_attempt_unmodified=True,
                    partial_files_preserved=True,
                ),
                guard,
                terminal=True,
            )
        except BaseException:
            pass
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"passed":false,"fixture_credit":0,"diagnostic_integrity_not_certified":true,"original_attempt_unmodified":true,"emergency_constant_marker_no_budget_certificate":true}\n'
            )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
