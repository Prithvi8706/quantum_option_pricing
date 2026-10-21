"""Metadata-only preservation of two fixed failed attempts, never proof promotion.

Each fresh invocation:300 CPU/270 admission/900 wall, one thread;
128 failed-owned files/512MiB,24k union paths/8GiB,24GiB hash work.
All original failure markers and partial claims remain immutable/untrusted.
"""

import ast
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
RESEARCH = ROOT / "research/limitation_program_20261001"
CPU, ADMISSION, WALL = 300, 270, 900
MAX_FILES, MAX_BYTES, HASH_BYTES = 24000, 8 * 1024**3, 24 * 1024**3
MAP, HASH_WORK, STARTED = {}, 0, None
BASE = Path(sys.base_prefix).resolve()
EXCLUDED = (BASE / "Lib/site-packages").resolve()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def budget(admission=False):
    require(time.process_time() < (ADMISSION if admission else CPU), "Fixed CPU cap")
    require(time.monotonic() - STARTED < WALL, "Fixed creation-wall cap")


def creation_clock():
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    stamps = [wintypes.FILETIME() for _ in range(4)]
    require(kernel.GetProcessTimes(kernel.GetCurrentProcess(), *map(ctypes.byref, stamps)), "Clock")
    ticks = (stamps[0].dwHighDateTime << 32) | stamps[0].dwLowDateTime
    age = (time.time_ns() - (ticks - 116444736000000000) * 100) / 1_000_000_000
    require(age >= 0, "Nonnegative creation age")
    return time.monotonic() - age


def lexical(path):
    path = Path(os.path.abspath(str(path)))
    require(path.is_relative_to(ROOT) or path.is_relative_to(BASE), "Confined input")
    require(not path.is_relative_to(EXCLUDED), "Excluded base packages")
    return path


def actual(path):
    path = lexical(path)
    resolved = path.resolve(strict=True)
    require(path == resolved and not resolved.is_relative_to(EXCLUDED), "No physical alias")
    require(resolved.is_file(), "Regular immutable file")
    return resolved


def fingerprint(path):
    stat = path.stat()
    return tuple(
        getattr(stat, key, None)
        for key in (
            "st_dev",
            "st_ino",
            "st_size",
            "st_mtime_ns",
            "st_ctime_ns",
            "st_mode",
            "st_file_attributes",
            "st_reparse_tag",
        )
    )


def sha(path):
    global HASH_WORK
    budget()
    path = actual(path)
    before, state, amount = fingerprint(path), hashlib.sha256(), 0
    with path.open("rb") as stream:
        while block := stream.read(1024**2):
            budget()
            HASH_WORK += len(block)
            amount += len(block)
            require(HASH_WORK <= HASH_BYTES and amount <= before[2], "Finite stable hashing")
            state.update(block)
    require(amount == before[2] and fingerprint(path) == before, "Stable file bytes")
    budget()
    return state.hexdigest()


def key(path):
    path = lexical(path)
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def bind(path, expected=None):
    budget()
    name = key(path)
    if expected is None:
        expected = sha(path)
    require(type(expected) is str and len(expected) == 64, "Actual SHA pin")
    require(all(v in "0123456789abcdef" for v in expected), "Hex SHA pin")
    require(name not in MAP or MAP[name] == expected, "Equal canonical expected hashes")
    MAP[name] = expected
    require(len(MAP) <= MAX_FILES, "Finite complete union")


def load(path):
    require(path.stat().st_size < 8 * 1024**2, "Metadata JSON only")
    bind(path)
    return json.loads(path.read_bytes())


def maps(document):
    for name, expected in document.get("frozen_inputs", {}).items():
        require(not Path(name).is_absolute() and ".." not in Path(name).parts, "ROOT key")
        bind(ROOT / name, expected)
    for name, expected in document.get("external_runtime_inputs", {}).items():
        require(Path(name).is_absolute(), "Absolute external key")
        bind(name, expected)


def packet(label, expected):
    directory = PROGRAM / label
    mf = directory / "manifest.json"
    bind(mf, expected)
    require(sha(mf) == expected, "Original immutable manifest SHA")
    document = json.loads(mf.read_bytes())
    own = document["files"] if "files" in document else document
    for name, pin in own.items():
        normalized = name.replace("\\", "/")
        bind(
            ROOT / normalized if normalized.startswith("results/") else directory / normalized, pin
        )
    maps(document)


def inventory(directory):
    members, total = set(), 0
    for parent, dirs, names in os.walk(directory, followlinks=False):
        budget()
        for name in dirs:
            candidate = Path(parent) / name
            require(candidate.resolve(strict=True) == candidate.absolute(), "No directory alias")
        for name in names:
            path = actual(Path(parent) / name)
            members.add(key(path))
            total += path.stat().st_size
            require(len(members) <= 128 and total <= 512 * 1024**2, "Failed archive cap")
    return members, total


def fresh_union():
    total = 0
    for name, expected in MAP.items():
        path = Path(name) if Path(name).is_absolute() else ROOT / name
        total += path.stat().st_size
        require(total <= MAX_BYTES and sha(path) == expected, "Fresh union SHA/size")
    return total


def save(directory, name, data):
    budget()
    with (directory / name).open("x", encoding="utf-8", newline="\n") as stream:
        for fragment in json.JSONEncoder(indent=2, allow_nan=False).iterencode(data):
            budget()
            stream.write(fragment)
        stream.write("\n")
    budget()


def main():
    global STARTED
    STARTED = creation_clock()
    require(sys.dont_write_bytecode and os.name == "nt", "Windows startup -B")
    require(
        Path(sys.executable).resolve() == ROOT / ".context/frontier_t0_env/Scripts/python.exe",
        "Launcher",
    )
    require(len(sys.argv) == 2 and sys.argv[1] in ("screen", "allocation"), "Fixed diagnostic mode")
    mode = sys.argv[1]
    label, outlabel = (
        ("A13_run002", "A13_terminal_failure_capture_run002")
        if mode == "screen"
        else (
            "A13_fixed_alpha_allocation_root_verification_run001",
            "A13_allocation_root_failure_capture_run001",
        )
    )
    source, output = PROGRAM / label, PROGRAM / outlabel
    require(
        not output.exists() and (source / "FAILED_UNSEALED.json").is_file(), "Fresh failed capture"
    )
    members, owned_bytes = inventory(source)
    for name in members:
        bind(ROOT / name)
    marker = load(source / "FAILED_UNSEALED.json")
    require(marker["failed"] is True and marker["passed"] is False, "Failure remains authoritative")
    bind(Path(__file__))
    if mode == "screen":
        protocol = load(source / "protocol.json")
        require(protocol["CPU_admission_wall_seconds"] == [300, 270, 900], "Original screen caps")
        maps(protocol)
        packet(
            "A13_exp_frontier_root_review_run002",
            "6834a90acb76a5489f3fac66ce874adf81357692ba2bade7cd709455846626e3",
        )
        packet("A13_run001", "d77077cfb2d67ee2973a02b236ea6e6b2336962f35fed6ce4aeb48ef8bb65aa8")
        logs = [
            "a13_frontier002_prepare.stdout.log",
            "a13_frontier002_prepare.stderr.log",
            "a13_frontier002_run.stdout.log",
            "a13_frontier002_run.stderr.log",
        ]
    else:
        author = RESEARCH / "verify_exp_frontier_allocation_root_v1.py"
        bind(author, "803d3bbb267a616a0ffa9f6114c9edf21168a437383f4d3d982f9a627d128ecb")
        require(sha(author) == MAP[key(author)], "Original failed verifier bytes")
        constants = {}
        for node in ast.parse(author.read_bytes()).body:
            if (
                isinstance(node, ast.Assign)
                and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
            ):
                name = node.targets[0].id
                if name in ("AUTHORS", "READY_PINS", "PREREQUISITES"):
                    constants[name] = ast.literal_eval(node.value)
        require(
            set(constants) == {"AUTHORS", "READY_PINS", "PREREQUISITES"},
            "Exact failed author constants",
        )
        for name, pin in constants["AUTHORS"].items():
            bind(RESEARCH / name, pin)
        for name, pin in constants["READY_PINS"].items():
            bind(PROGRAM / name, pin)
        for name, pin in constants["PREREQUISITES"].items():
            packet(name, pin)
        packet(
            "A13_fixed_alpha_allocation_run001",
            "4c863e4a031a458c5a424c75774f791f49c25c9c25e030a6fd28e5e8ec91236f",
        )
        packet(
            "A13_fixed_alpha_allocation_audit_run001",
            "829712c9c71925ba74e98059a294c99c812fe659fd0b31a44c50ef35c6b31358",
        )
        logs = ["a13_allocation_root001.stdout.log", "a13_allocation_root001.stderr.log"]
    for name in logs:
        bind(ROOT / ".context" / name)
    for module in list(sys.modules.values()):
        for attribute in ("__file__", "__cached__"):
            path = getattr(module, attribute, None)
            if path and Path(path).is_file():
                bind(path)
    total = fresh_union()
    require(inventory(source)[0] == members, "Unchanged exact failed inventory")
    budget(admission=True)
    output.mkdir()
    try:
        summary = dict(
            schema="failed-a13-metadata-capture-v1",
            created_utc=datetime.now(timezone.utc).isoformat(),
            passed=True,
            diagnostic_integrity=True,
            original_attempt_failed=True,
            original_partial_success_invalid=True,
            original_failure_marker=marker,
            original_receipt=source.relative_to(ROOT).as_posix(),
            original_owned_files=len(members),
            original_owned_bytes=owned_bytes,
            preserved_members=sorted(members),
            fresh_unique_paths=len(MAP),
            fresh_unique_bytes=total,
            new_fixture_credit=0,
            new_gate_replays=0,
            mathematical_result_or_candidate_adoption_claim=False,
            scientific_import_or_evaluation_executed=False,
            limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
            all_old_expected_hashes_retained=True,
        )
        save(output, "summary.json", summary)
        save(output, "frozen_reference_index.json", {name: MAP[name] for name in sorted(members)})
        total = fresh_union()
        require(inventory(source)[0] == members, "Terminal exact failed inventory")
        save(
            output,
            "completion_outcome.json",
            dict(
                completed=True,
                passed=True,
                diagnostic_integrity=True,
                original_attempt_failed=True,
                new_fixture_credit=0,
                fresh_unique_paths=len(MAP),
                fresh_unique_bytes=total,
                process_CPU_seconds=time.process_time(),
                wall_seconds=time.monotonic() - STARTED,
            ),
        )
        own = {path.relative_to(output).as_posix(): sha(path) for path in output.iterdir()}
        frozen = {name: pin for name, pin in MAP.items() if not Path(name).is_absolute()}
        external = {name: pin for name, pin in MAP.items() if Path(name).is_absolute()}
        save(
            output,
            "manifest.json",
            dict(
                files=own,
                frozen_inputs=frozen,
                external_runtime_inputs=external,
                manifest_self_hash_excluded=True,
                diagnostic_integrity=True,
                original_attempt_failed=True,
                new_fixture_credit=0,
            ),
        )
        print(
            json.dumps(
                {
                    "mode": mode,
                    "diagnostic_manifest_SHA256": sha(output / "manifest.json"),
                    "original_attempt_failed": True,
                    "new_fixture_credit": 0,
                }
            )
        )
    except BaseException:
        with (output / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"failed":true,"passed":false,"diagnostic_integrity":false,"new_fixture_credit":0}\n'
            )
        raise


if __name__ == "__main__":
    main()
