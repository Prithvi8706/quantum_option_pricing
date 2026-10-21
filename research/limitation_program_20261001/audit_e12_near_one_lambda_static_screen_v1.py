"""Unexecuted independent E12 certificate-only static audit; external ROOT release required.
No primary scientific helper import, toy traces, sqrt, samples or financial source proof.
Only metadata/lifecycle text is inherited; all mathematical consumption is independent.
"""
from __future__ import annotations
import argparse
import ctypes
from ctypes import wintypes
from fractions import Fraction
import hashlib
import json
from math import factorial
import os
from pathlib import Path
import re
import sys
import time
ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "research/limitation_program_20261001"
AUTHOR = HERE / "audit_e12_near_one_lambda_static_screen_v1.py"
METHOD_MD = HERE / "E12_NEAR_ONE_LAMBDA_STATIC_AUDIT_PREFLIGHT_V1.md"
METHOD_JSON = HERE / "e12_near_one_lambda_static_audit_preflight_v1.json"
READY = ROOT / ".context/E12_near_one_lambda_static_audit_ROOT_READY_run001.json"
OUTPUT = ROOT / "results/limitation_program_20261001/E12_near_one_lambda_static_audit_run001"
PRIMARY = ROOT / "results/limitation_program_20261001/E12_near_one_lambda_static_screen_run001"
PRIMARY_MANIFEST = PRIMARY / "manifest.json"
PRIMARY_MANIFEST_SHA = "84a8257fbbe9b0cdf531bc6f87dd3e8905ccfd9e6e390d726b01b09d81f960c5"
PRIMARY_SOURCE_KEY = "research/limitation_program_20261001/experiment_e12_near_one_lambda_static_screen_v1.py"
PRIMARY_SOURCE_SHA = "f31ec5fb6f1b660d2b1383bcc9865dba2038e2a6eff4cd0548129d9974d41ac7"
PRIMARY_READY_KEY = ".context/E12_near_one_lambda_static_screen_ROOT_READY_run001.json"
PRIMARY_READY_SHA = "4eabd83b6242f16d6c517d9286fd9e23246c1fb038efc401e83a55bdb7ccc0b5"
PRIMARY_PROTOCOL_SHA = "dd83b20f270ccda24fa79833882f0979d59966d2cb84c10c8b40b045d7385917"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
BASE = Path("C:/Users/prith/AppData/Local/Programs/Python/Python312")
LAUNCHER_SHA = "41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5"
BASE_SHA = "fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b"
CPU_LIMIT, WORK_LIMIT, WALL_LIMIT = 180, 150, 600
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 4096, 512 << 20
MAX_FROZEN_FILES, MAX_FROZEN_BYTES = 16, 8 << 20
MAX_OWNED_FILES, MAX_OWNED_BYTES = 16, 16 << 20
MAX_SINGLE_BYTES = 64 << 20
MAX_PRIMARY_INPUT_MEMBERS, MAX_ADMITTED_ROOT_MEMBERS = 2859, 28
SUPPORT_EVEN_TERMS, SUPPORT_ODD_TERMS, POSITIVE_EXP_TERMS = 96, 97, 80
N_CAP = 1 << 20
LOOKS = tuple(1 << j for j in range(1, 21))
_ABSENT_CACHES = set()
_ATTEMPT_ROUTE_OWNED = False
_PRIMARY_RUNTIME_EXPECTED = {}
_SCOPE = {"certificate_only": True, "program_fixture_credit": 0, "statistical_draws": 0,
          "financial_draws": 0, "financial_replays": 0, "quantum_gate_emissions": 0,
          "finance_execution": False, "finance_adoption": False, "source_adoption": False,
          "G2_transfer": False, "G3_price_delivery": False, "classical_comparator": False,
          "financial_target_delivery": False, "actual_financial_IID_or_digital_support_proved": False,
          "measured_latency_or_quantum_advantage": False}
PRIMARY_OWNED = {
    "checks.json": "f1828ea9388691be665b09aa1fb23628749b2dea055cd2060999ca7ac135f7bb",
    "frontiers.json": "31600530000715fe1022fe255b777c28b8a9ac53ade38f584be495b5561a5f88",
    "protocol.json": "dd83b20f270ccda24fa79833882f0979d59966d2cb84c10c8b40b045d7385917",
    "run_started.json": "304d41273dddc3037f0fc807f2eba5e22994ab802be1cfa1da9fd10986b75db7",
    "screen.json": "ce7e05685da34bf6bf6e4315dbf6d9d0eb741e06a9163e148be5d58e05b116dd",
    "summary.json": "857797066a587f5b3446b160282e1bff8c8974ddf97b1d62d2ff55d4035a1d56",
    "verification.json": "d7077ef7d5a548edfb73b8edde3712a36fc241c464188ab3587e6929c7b46e95",
}


SHA = re.compile("[0-9a-f]{64}\\Z")

REFERENCES = {
    ("research/limitation_program_20261001/experiment_e12_anytime_moment_v1.py"): (
        "5347eefef9beddc2221ce1b71a59b176313d2cc4094b4aecb3eaf68535b85b64"
    ),
    ("research/limitation_program_20261001/E12_ANYTIME_MOMENT_PREFLIGHT_V1.md"): (
        "e9e3211354a37d50ab848ebd1318bb9ab30867a736b5283dcb33395827ec4703"
    ),
    ("research/limitation_program_20261001/e12_anytime_moment_preflight_v1.json"): (
        "c13c0d98881d14bbb0908c24e7832885dc7e1735621618bfe442f472ddda2bb0"
    ),
    ("results/limitation_program_20261001/E12_anytime_moment_run001/manifest.json"): (
        "72ff4bc7ad82e95c387f19a3e8432e7767488432ed8ece2247496fd5c5a0acca"
    ),
    ("results/limitation_program_20261001/E12_anytime_moment_run001/protocol.json"): (
        "d2d65c4bd58a158347d4f759f841c0ec676138f62ff47de1f3a1acf54dd3f7bb"
    ),
    ("results/limitation_program_20261001/E12_anytime_moment_run001/summary.json"): (
        "f4a3d37f4cf8f64d792b1e0afb0bcf2f8dfcc4ed34c76e7f5184becb9f3d2a23"
    ),
    (
        "results/limitation_program_20261001/E12_continuation_20"
        "261004_screen_run001/finance_admission.json"
    ): ("8fd4839d293686c40e34c5e2c156218871f9a1b2e27b3396ce934f6db9a372bc"),
    ("docs/limitation_program_20261001/continuation_20261004/E12/PROTOCOL.json"): (
        "e4be2ad2e9ced6b60c43f299b247838414e79318d13903a495dd96b392b253e9"
    ),
    ("docs/limitation_program_20261001/continuation_20261004/E12/THEOREM_AND_SCOPE.md"): (
        "e5b66c4001ef0095c906918d801ecb8f62e3de0e7b7d3f23c9f317e3b0a71db4"
    ),
    ("results/limitation_program_20261001/E12_continuation_20261004_screen_run001/manifest.json"): (
        "bdc6946689367f982912cf28c0068d93d2fcc982e6f2cd0a0ee0e043ce05cdec"
    ),
    (
        "results/limitation_program_20261001/E12_continuation_20"
        "261004_ROOT_integrity_run001/manifest.json"
    ): ("31cd94def7129dfbc45e4c6a0a648a0a5f872e4caa1d8d0fae165db822000a6c"),
    (
        "results/limitation_program_20261001/E12_continuation_20"
        "261004_screen_run001/certificate.json"
    ): ("0fe9304296d7c324887989f7c9acca4aa6f7f7db7fcc47d33db141244579cb38"),
}

PROPOSAL_PINS = {
    ("research/limitation_program_20261001/E12_NEAR_ONE_LAMBDA_PROPOSAL_V1.md"): (
        "9bed9bb996e497e5834b42494b5ea4558a15c7fe18669dec86ef54cef28735d0"
    ),
    ("research/limitation_program_20261001/E12_NEAR_ONE_LAMBDA_PROPOSAL_V1.json"): (
        "3c0d93b782c9bb99a5aa8e7ae6dc94b64632662c821b6ea9e519460c478a7a37"
    ),
}

def require(value, message):
    if not value:
        raise ValueError(message)

def started_clock():
    require(sys.platform == "win32", "Frozen experiment requires Windows")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    values = [wintypes.FILETIME() for _ in range(4)]
    require(
        kernel.GetProcessTimes(kernel.GetCurrentProcess(), *(ctypes.byref(x) for x in values)),
        "Actual process creation time",
    )
    ticks = values[0].dwHighDateTime << 32 | values[0].dwLowDateTime
    elapsed = (time.time_ns() - (ticks - 116444736000000000) * 100) / 1000000000
    require(elapsed >= 0, "Nonnegative process age")
    return time.monotonic() - elapsed

def guard(started, admission=False):
    cpu, wall = (time.process_time(), time.monotonic() - started)
    if cpu >= (WORK_LIMIT if admission else CPU_LIMIT) or wall >= WALL_LIMIT:
        raise RuntimeError(f"E12 fixed budget reached: CPU={cpu}, wall={wall}")
    return (cpu, wall)

def stable_read(path, started):
    guard(started)
    require(
        path.is_absolute() and path.resolve(strict=True) == path, "Exact absolute path, no alias"
    )
    before = path.stat()
    require(path.is_file() and before.st_size <= MAX_SINGLE_BYTES, "Finite regular input")
    parts = []
    with path.open("rb") as stream:
        while True:
            guard(started)
            part = stream.read(1 << 20)
            if not part:
                break
            parts.append(part)
            require(sum(map(len, parts)) <= MAX_SINGLE_BYTES, "Bounded file read")
    data = b"".join(parts)
    after = path.stat()
    fields = (
        "st_dev",
        "st_ino",
        "st_size",
        "st_mtime_ns",
        "st_ctime_ns",
        "st_mode",
        "st_file_attributes",
        "st_reparse_tag",
    )
    require(all((getattr(before, k) == getattr(after, k) for k in fields)), "Stable file identity")
    require(path.resolve(strict=True) == path, "Exact nonredirected input after complete read")
    require(len(data) == before.st_size, "Full observed byte count")
    guard(started)
    return data

def checked_read(path, expected, started):
    require(isinstance(expected, str) and SHA.fullmatch(expected), "Exact expected SHA-256")
    data = stable_read(path, started)
    require(hashlib.sha256(data).hexdigest() == expected, "Fresh bytes equal frozen expected SHA")
    return data

def rational(value):
    return [value.numerator, value.denominator]

def write_json(path, value, started):
    guard(started)
    require(
        path.parent == OUTPUT and OUTPUT.resolve(strict=True) == OUTPUT,
        "Exact confined owned output directory",
    )
    require(not path.exists() and (not path.is_symlink()), "New owned output only")
    prior = set(OUTPUT.iterdir())
    prior_bytes = 0
    for member in prior:
        guard(started)
        require(
            member.is_file() and member.resolve(strict=True) == member,
            "Existing owned members are confined regular files",
        )
        prior_bytes += member.stat().st_size
    require(
        len(prior) + 1 <= MAX_OWNED_FILES and prior_bytes < MAX_OWNED_BYTES,
        "Prospective exclusive write stays within owned capacities",
    )
    encoded_bytes = 1
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        for fragment in json.JSONEncoder(indent=2, sort_keys=True, allow_nan=False).iterencode(
            value
        ):
            guard(started)
            encoded_bytes += len(fragment.encode("utf-8"))
            require(encoded_bytes <= MAX_SINGLE_BYTES, "Bounded exclusive JSON encoding")
            require(
                prior_bytes + encoded_bytes <= MAX_OWNED_BYTES,
                "Guarded encoded bytes stay within remaining owned capacity",
            )
            stream.write(fragment)
            guard(started)
        stream.write("\n")
    require(path.stat().st_size == encoded_bytes, "Exact actual UTF8 owned byte count")
    actual = set(OUTPUT.iterdir())
    require(
        actual == prior | {path} and len(actual) <= MAX_OWNED_FILES,
        "Exact guarded write ownership count",
    )
    actual_bytes = 0
    for member in actual:
        guard(started)
        require(
            member.is_file() and member.resolve(strict=True) == member,
            "Final written owned members retain exact routes",
        )
        actual_bytes += member.stat().st_size
    require(
        actual_bytes == prior_bytes + encoded_bytes <= MAX_OWNED_BYTES,
        "Actual complete guarded write ownership bytes",
    )
    guard(started)

def relative(path):
    return path.relative_to(ROOT).as_posix()

def invocation_check(started):
    require(sys.version_info[:3] == (3, 12, 4), "Pinned Python 3.12.4")
    require(sys.flags.isolated == 1 and sys.flags.no_site == 1, "Use -I -S")
    require(sys.dont_write_bytecode, "Use -B")
    require(Path(sys.executable).resolve(strict=True) == LAUNCHER, "Actual pinned launcher")
    require(Path(sys.base_prefix).resolve(strict=True) == BASE, "Actual pinned interpreter root")
    require(Path(sys.prefix).resolve(strict=True) == BASE, "No-site base interpreter prefix")
    expected_path = [str(BASE / "python312.zip"), str(BASE / "DLLs"), str(BASE / "Lib"), str(BASE)]
    require(sys.path == expected_path, "Exact isolated standard-library search path")
    require(not (BASE / "python312.zip").exists(), "Frozen absent runtime ZIP")
    require(not (BASE / "python312.zip").is_symlink(), "No dangling alias for absent runtime ZIP")
    require(
        not any((name == "site" or name.startswith("research.") for name in sys.modules)),
        "No site startup or scientific module admitted",
    )
    checked_read(LAUNCHER, LAUNCHER_SHA, started)
    checked_read(BASE / "python.exe", BASE_SHA, started)

def runtime_packet(started):
    paths = {LAUNCHER, BASE / "python.exe"}
    require(BASE.resolve(strict=True) == BASE, "Exact base interpreter directory")
    for path in BASE.iterdir():
        guard(started)
        if path.is_file():
            paths.add(path)
    for tree in (BASE / "Lib", BASE / "DLLs"):
        for directory, names, files in os.walk(tree, followlinks=False):
            guard(started)
            parent = Path(directory)
            require(
                parent.resolve(strict=True) == parent, "Runtime inventory does not follow aliases"
            )
            names[:] = [name for name in names if name.casefold() != "site-packages"]
            for name in names:
                child = parent / name
                require(
                    not child.is_symlink() and child.resolve(strict=True) == child,
                    "No silently skipped runtime directory alias",
                )
            paths.update((parent / name for name in files))
            require(len(paths) <= MAX_RUNTIME_FILES, "Finite isolated runtime file count")
    mapping, total = ({}, 0)
    for path in sorted(paths, key=str):
        data = stable_read(path, started)
        total += len(data)
        require(total <= MAX_RUNTIME_BYTES, "Finite isolated runtime byte count")
        mapping[str(path)] = hashlib.sha256(data).hexdigest()
    return (mapping, total)

def loaded_runtime_check(runtime, started):
    origins = set()
    for module in tuple(sys.modules.values()):
        guard(started)
        spec = getattr(module, "__spec__", None)
        origin = getattr(spec, "origin", None)
        if origin in (None, "built-in", "frozen"):
            continue
        path = Path(origin)
        require(
            path.is_absolute() and path.resolve(strict=True) == path,
            "Loaded runtime origin has no lexical alias",
        )
        require(str(path) in runtime, "Every imported runtime module has a frozen input")
        origins.add(str(path))
        cache = getattr(spec, "cached", None)
        if cache:
            cache_path = Path(cache)
            require(cache_path.is_absolute(), "Declared loaded cache has an absolute route")
            if cache_path.exists():
                require(
                    cache_path.resolve(strict=True) == cache_path and str(cache_path) in runtime,
                    "Existing imported bytecode is exact and frozen",
                )
            else:
                require(not cache_path.is_symlink(), "No dangling alias for absent loaded cache")
                _ABSENT_CACHES.add(cache_path)
    require(
        not any((path.exists() or path.is_symlink() for path in _ABSENT_CACHES)),
        "Every declared absent loaded cache remains absent",
    )
    return len(origins)

def rehash(mapping, runtime, started, protocol_expected=None):
    invocation_check(started)
    current, _ = runtime_packet(started)
    require(current == runtime, "Complete runtime tree membership and hashes remain frozen")
    total = 0
    for key, digest in mapping.items():
        total += len(checked_read(ROOT / key, digest, started))
    for key, digest in runtime.items():
        total += len(checked_read(Path(key), digest, started))
    if protocol_expected is not None:
        total += len(checked_read(OUTPUT / "protocol.json", protocol_expected, started))
    return {
        "unique_paths": len(mapping) + len(runtime) + int(protocol_expected is not None),
        "bytes": total,
        "sha_mismatches": 0,
        "expected_hash_waivers": 0,
        "loaded_module_origins": loaded_runtime_check(runtime, started),
    }

def exact_relative_key(key):
    require(
        type(key) is str
        and key
        and not Path(key).is_absolute()
        and not Path(key).drive
        and "\\" not in key
        and all(part not in ("", ".", "..") for part in key.split("/"))
        and Path(key).as_posix() == key,
        "Exact slash-relative historical member spelling",
    )

def pinned_json(key, frozen, started):
    exact_relative_key(key)
    require(key in REFERENCES and frozen[key] == REFERENCES[key], "Fixed direct historical pin")
    return json.loads(checked_read(ROOT / key, REFERENCES[key], started))

def historical_map(mapping, count, started, row_objects=False, absolute_keys=False, legacy=False):
    """Validate archived literal maps only; never hash their unselected dependencies."""
    require(type(mapping) is dict and len(mapping) == count, "Complete retained historical map")
    for key, value in mapping.items():
        guard(started)
        require(type(key) is str and key, "Literal historical map key")
        if Path(key).is_absolute():
            require(absolute_keys, "Absolute spelling only in declared historical scope")
            require(".." not in Path(key).parts, "No historical absolute traversal")
        elif legacy:
            require(
                "/" not in key
                and not Path(key).drive
                and all(part not in ("", ".", "..") for part in key.split("\\")),
                "Only original ROOT-integrity Windows-relative literal keys",
            )
        else:
            exact_relative_key(key)
        if row_objects:
            require(
                type(value) is dict
                and set(value) == {"sha256", "bytes"}
                and type(value["bytes"]) is int
                and value["bytes"] >= 0,
                "Exact archived SHA/byte record shape",
            )
            value = value["sha256"]
        require(type(value) is str and SHA.fullmatch(value), "Original literal expected SHA")

def history_membership(frozen, started):
    main_key = "results/limitation_program_20261001/E12_anytime_moment_run001/manifest.json"
    main = pinned_json(main_key, frozen, started)
    require(
        main.get("schema") == "e12-anytime-moment-manifest-v1"
        and main.get("passed") is True
        and main.get("completed") is True
        and main.get("budget_censored") is False
        and main.get("error") is None
        and main.get("manifest_self_hash_excluded") is True
        and main.get("financial_adoption_approved") is False,
        "Exact completed bounded-toy history without finance adoption",
    )
    historical_map(main["owned_files"], 6, started)
    historical_map(main["frozen_inputs"], 7, started)
    historical_map(main["external_runtime_inputs"], 2843, started, absolute_keys=True)
    for key in (
        "research/limitation_program_20261001/experiment_e12_anytime_moment_v1.py",
        "research/limitation_program_20261001/E12_ANYTIME_MOMENT_PREFLIGHT_V1.md",
        "research/limitation_program_20261001/e12_anytime_moment_preflight_v1.json",
    ):
        require(
            main["frozen_inputs"].get(key) == REFERENCES[key], "Selected original author membership"
        )
    for key in (
        "results/limitation_program_20261001/E12_anytime_moment_run001/protocol.json",
        "results/limitation_program_20261001/E12_anytime_moment_run001/summary.json",
    ):
        require(
            main["owned_files"].get(key) == REFERENCES[key],
            "Selected original toy owned membership",
        )
    screen_key = (
        "results/limitation_program_20261001/E12_continuation_20261004_screen_run001/manifest.json"
    )
    screen = pinned_json(screen_key, frozen, started)
    require(
        screen.get("schema") == "e12-continuation-owned-and-input-manifest-v1"
        and screen.get("manifest_self_excluded") is True
        and screen.get("component_passed") is True
        and screen.get("finance_rule_rejected") is True,
        "Original rejected fixed stopping rule remains rejected",
    )
    historical_map(screen["owned_files"], 9, started, row_objects=True)
    historical_map(screen["frozen_inputs"], 31, started, row_objects=True, absolute_keys=True)
    for key in (
        (
            "results/limitation_program_20261001/E12_continuation_20"
            "261004_screen_run001/finance_admission.json"
        ),
        (
            "results/limitation_program_20261001/E12_continuation_20"
            "261004_screen_run001/certificate.json"
        ),
    ):
        row = screen["owned_files"].get(key)
        require(
            row is not None and row["sha256"] == REFERENCES[key],
            "Selected rejected-screen owned membership",
        )
        require(
            len(checked_read(ROOT / key, REFERENCES[key], started)) == row["bytes"],
            "Selected owned exact byte count",
        )
    for key in (
        "docs/limitation_program_20261001/continuation_20261004/E12/PROTOCOL.json",
        "docs/limitation_program_20261001/continuation_20261004/E12/THEOREM_AND_SCOPE.md",
    ):
        row = screen["frozen_inputs"].get(key)
        require(
            row is not None and row["sha256"] == REFERENCES[key],
            "Selected retained finance method membership",
        )
        require(
            len(checked_read(ROOT / key, REFERENCES[key], started)) == row["bytes"],
            "Selected method exact byte count",
        )
    root_key = (
        "results/limitation_program_20261001/E12_continuation_20"
        "261004_ROOT_integrity_run001/manifest.json"
    )
    historical_root = pinned_json(root_key, frozen, started)
    require(
        historical_root.get("passed") is True
        and historical_root.get("integrity_only") is True
        and historical_root.get("manifest_self_hash_excluded") is True
        and historical_root.get("new_test_credit") == 0,
        "Retained ROOT integrity is metadata only",
    )
    historical_map(historical_root["files"], 2, started)
    historical_map(historical_root["frozen_inputs"], 41, started, absolute_keys=True, legacy=True)
    # These five spellings are literal keys of the exact separately pinned old map.
    # They are never normalized, resolved or used to admit other current inputs.
    old_keys = {
        ("docs\\limitation_program_20261001\\continuation_20261004\\E12\\PROTOCOL.json"): (
            "docs/limitation_program_20261001/continuation_20261004/E12/PROTOCOL.json"
        ),
        ("docs\\limitation_program_20261001\\continuation_20261004\\E12\\THEOREM_AND_SCOPE.md"): (
            "docs/limitation_program_20261001/continuation_20261004/E12/THEOREM_AND_SCOPE.md"
        ),
        (
            "results\\limitation_program_20261001\\E12_continuation_20"
            "261004_screen_run001\\finance_admission.json"
        ): (
            "results/limitation_program_20261001/E12_continuation_20"
            "261004_screen_run001/finance_admission.json"
        ),
        (
            "results\\limitation_program_20261001\\E12_continuation_20"
            "261004_screen_run001\\certificate.json"
        ): (
            "results/limitation_program_20261001/E12_continuation_20"
            "261004_screen_run001/certificate.json"
        ),
        (
            "results\\limitation_program_20261001\\E12_continuation_20"
            "261004_screen_run001\\manifest.json"
        ): screen_key,
    }
    for old_key, current_key in old_keys.items():
        require(
            historical_root["frozen_inputs"].get(old_key) == REFERENCES[current_key],
            "Exact original legacy metadata key and equal SHA; no spelling waiver",
        )

def preserve_failure(error, started):
    """Every owned incomplete attempt is authoritative; no failed packet is resealed."""
    if not _ATTEMPT_ROUTE_OWNED or not OUTPUT.is_dir():
        return
    try:
        guard(started)
        if not (OUTPUT / "failure.json").exists():
            write_json(
                OUTPUT / "failure.json",
                {
                    "failed": True,
                    "passed": False,
                    "completed": False,
                    "error_type": type(error).__name__,
                    "error": str(error),
                    "observed_CPU": time.process_time(),
                    "observed_wall": time.monotonic() - started,
                    "no_partial_scientific_approval": True,
                    "original_expected_hashes_waived": False,
                    "fixture_credit": 0,
                    "finance_execution": False,
                },
                started,
            )
    except BaseException:
        pass
    try:
        require(OUTPUT.resolve(strict=True) == OUTPUT, "Confined failed attempt route")
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"partial_success_invalid":true,"fixture_credit":0,"finance_execution":false}\n'
            )
    except (OSError, ValueError):
        pass

def merge_expected(target, source, started):
    for key, expected in source.items():
        guard(started)
        require(type(expected) is str and SHA.fullmatch(expected), "Exact externally expected SHA")
        require(key not in target or target[key] == expected, "No conflicting or substituted expectation")
        target[key] = expected


def primary_inventory(started):
    require(PRIMARY.resolve(strict=True) == PRIMARY, "Exact immutable primary receipt route")
    actual = set(PRIMARY.iterdir())
    expected = {PRIMARY / name for name in PRIMARY_OWNED} | {PRIMARY_MANIFEST}
    require(actual == expected, "Complete primary inventory; no failure, extra member or prior mutation")
    total = 0
    for path in actual:
        guard(started)
        require(path.is_file() and path.resolve(strict=True) == path, "Confined primary regular member")
        total += path.stat().st_size
    require(len(actual) == 8 and total <= MAX_OWNED_BYTES, "Primary unchanged inclusive ownership caps")


def primary_packet(started):
    global _PRIMARY_RUNTIME_EXPECTED
    manifest = json.loads(checked_read(PRIMARY_MANIFEST, PRIMARY_MANIFEST_SHA, started))
    require(
        manifest.get("schema") == "e12-near-one-lambda-static-screen-manifest-v1"
        and manifest.get("passed") is True and manifest.get("completed") is True
        and manifest.get("budget_censored") is False and manifest.get("error") is None
        and manifest.get("manifest_self_hash_excluded") is True
        and manifest.get("financial_adoption_approved") is False
        and manifest.get("manifest_inclusive_owned_file_count") == 8
        and manifest.get("manifest_inclusive_retention_checked_before_sealing") is True,
        "Exact completed primary certificate; no financial transfer",
    )
    owned, frozen, external = (manifest[key] for key in ("owned_files", "frozen_inputs", "external_runtime_inputs"))
    historical_map(owned, 7, started)
    historical_map(frozen, 16, started)
    historical_map(external, 2843, started, absolute_keys=True)
    require(owned == {relative(PRIMARY / name): value for name, value in PRIMARY_OWNED.items()},
            "All seven original externally pinned primary owned files")
    expected_frozen = dict(REFERENCES | PROPOSAL_PINS)
    expected_frozen[PRIMARY_SOURCE_KEY] = PRIMARY_SOURCE_SHA
    expected_frozen[PRIMARY_READY_KEY] = PRIMARY_READY_SHA
    require(frozen == expected_frozen, "Exact16 primary source/history/READY members")
    require(len(frozen) + len(external) == MAX_PRIMARY_INPUT_MEMBERS, "Full2859 primary input members")
    _PRIMARY_RUNTIME_EXPECTED = dict(external)
    primary_inventory(started)
    root_map = {}
    merge_expected(root_map, frozen, started)
    merge_expected(root_map, owned, started)
    root_map[relative(PRIMARY_MANIFEST)] = PRIMARY_MANIFEST_SHA
    frozen_bytes, owned_bytes, runtime_bytes = 0, 0, 0
    for key, expected in frozen.items():
        frozen_bytes += len(checked_read(ROOT / key, expected, started))
    for key, expected in owned.items():
        owned_bytes += len(checked_read(ROOT / key, expected, started))
    for key, expected in external.items():
        guard(started)
        path = Path(key)
        require(path.is_absolute() and str(path) == key and path.resolve(strict=True) == path,
                "Primary runtime exact physical absolute spelling")
        require(path == LAUNCHER or (path.is_relative_to(BASE) and not path.is_relative_to(BASE / "Lib/site-packages")),
                "Primary isolated runtime only; historical runtime maps are metadata")
        runtime_bytes += len(checked_read(path, expected, started))
        require(runtime_bytes <= MAX_RUNTIME_BYTES, "Complete primary expected runtime byte cap")
    require(frozen_bytes <= MAX_FROZEN_BYTES and owned_bytes == manifest["owned_nonmanifest_bytes"],
            "Exact retained primary frozen/owned byte accounting")
    require(owned_bytes + len(checked_read(PRIMARY_MANIFEST, PRIMARY_MANIFEST_SHA, started)) <= MAX_OWNED_BYTES,
            "Complete primary bytes inclusive of self-excluded manifest")
    ready = json.loads(checked_read(ROOT / PRIMARY_READY_KEY, PRIMARY_READY_SHA, started))
    protocol = json.loads(checked_read(PRIMARY / "protocol.json", PRIMARY_PROTOCOL_SHA, started))
    require(ready["schema"] == "root-e12-near-one-lambda-static-screen-READY-v1"
            and ready["frozen_inputs"] == {k: v for k, v in frozen.items() if k != PRIMARY_READY_KEY}
            and ready["output_route"] == relative(PRIMARY)
            and ready["CPU_admission_wall_seconds"] == [180, 150, 600]
            and ready["root_and_independent_static_reviews_passed"] is True
            and ready["exact_static_screen_execution_approved"] is True,
            "Original READY source set, route and phase limits remain exact")
    require(protocol["schema"] == "e12-near-one-lambda-static-screen-protocol-v1"
            and protocol["frozen_inputs"] == frozen and protocol["external_runtime_inputs"] == external
            and protocol["external_runtime_bytes"] == runtime_bytes
            and manifest["prepared_protocol_SHA256"] == PRIMARY_PROTOCOL_SHA,
            "Original independently frozen protocol maps and byte totals unchanged")
    zero_keys = {"program_fixture_credit", "statistical_draws", "financial_draws", "financial_replays", "quantum_gate_emissions"}
    require(manifest["scope"] == protocol["scope"]
            and all((type(value) is int and value == 0) if key in zero_keys else value is False
                    for key, value in protocol["scope"].items()),
            "Primary retains exact zero scientific/financial credit")
    for packet in (manifest["fresh_before"], manifest["fresh_after"]):
        require(packet["sha_mismatches"] == packet["expected_hash_waivers"] == 0,
                "Both original complete input checks recorded without waivers")
    history_membership(root_map, started)
    return root_map


def root_release(expected, started):
    raw = checked_read(READY, expected, started)
    ready = json.loads(raw)
    require(ready.get("schema") == "root-e12-near-one-lambda-static-audit-READY-v1"
            and ready.get("passed") is True and ready.get("static_review_only") is True
            and ready.get("root_and_independent_static_reviews_passed") is True
            and ready.get("independent_exact_static_audit_execution_approved") is True,
            "Separate externally frozen independent auditor ROOT release")
    require(ready.get("primary_manifest_SHA256") == PRIMARY_MANIFEST_SHA
            and ready.get("primary_source_SHA256") == PRIMARY_SOURCE_SHA
            and ready.get("primary_READY_SHA256") == PRIMARY_READY_SHA
            and ready.get("primary_protocol_SHA256") == PRIMARY_PROTOCOL_SHA,
            "Exact externally released complete primary certificate pins")
    require(ready.get("output_route") == relative(OUTPUT)
            and ready.get("CPU_admission_wall_seconds") == [180, 150, 600]
            and ready.get("independent_support_terms_even_odd") == [96, 97]
            and ready.get("independent_positive_exp_terms") == 80,
            "One fixed audit route, finite oracles and process budgets")
    require(all(ready.get(key) is False for key in ("statistical_sampling_approved", "financial_acquisition_approved", "financial_adoption_approved", "quantum_gate_emissions_authorized"))
            and ready.get("program_fixture_credit") == 0,
            "No samples, finance adoption, gates or fixture credit")
    release = ready.get("frozen_inputs")
    require(type(release) is dict and set(release) == {relative(AUTHOR), relative(METHOD_MD), relative(METHOD_JSON)},
            "Exactly three separately frozen new author files")
    release_bytes = len(raw)
    for key, digest in release.items():
        exact_relative_key(key)
        release_bytes += len(checked_read(ROOT / key, digest, started))
    require(len(release) + 1 <= MAX_FROZEN_FILES and release_bytes <= MAX_FROZEN_BYTES,
            "New release retains finite16-file8MiB limits")
    method = json.loads(checked_read(METHOD_JSON, release[relative(METHOD_JSON)], started))
    require(method.get("schema") == "e12-near-one-lambda-static-audit-preflight-v1"
            and method["immutable_history_pins"] == REFERENCES
            and method["primary_manifest_SHA256"] == PRIMARY_MANIFEST_SHA
            and method["primary_expected_counts"] == [7, 16, 2843]
            and method["independent_support_terms_even_odd"] == [96, 97]
            and method["independent_positive_exp_terms"] == 80
            and method["limits_CPU_admission_wall"] == [180, 150, 600]
            and method["owned_caps_files_bytes"] == [16, MAX_OWNED_BYTES]
            and method["runtime_caps_files_bytes"] == [4096, MAX_RUNTIME_BYTES]
            and method["new_output"] == relative(OUTPUT) and method["new_ROOT_READY"] == relative(READY),
            "Exact new independent method, endpoints and bounded caps")
    mapping = primary_packet(started)
    merge_expected(mapping, release, started)
    merge_expected(mapping, {relative(READY): expected}, started)
    require(len(mapping) == MAX_ADMITTED_ROOT_MEMBERS, "Exact28 complete root-relative inputs")
    return mapping


def complete_union(frozen, runtime, started, protocol_expected=None):
    require(runtime == _PRIMARY_RUNTIME_EXPECTED,
            "Current isolated runtime equals all2843 externally expected primary runtime bytes")
    primary_inventory(started)
    history_membership(frozen, started)
    result = rehash(frozen, runtime, started, protocol_expected)
    primary_inventory(started)
    result["primary_owned_frozen_external_counts"] = [7, 16, 2843]
    result["historical_scope"] = "Twelve direct metadata bytes and exact selected literal map relations only"
    result["historical_recursive_runtime_validation"] = False
    return result


def protocol_value(frozen, runtime, runtime_bytes):
    return {
        "schema": "e12-near-one-lambda-static-audit-protocol-v1", "local_only": True,
        "frozen_inputs": frozen, "external_runtime_inputs": runtime, "external_runtime_bytes": runtime_bytes,
        "primary_manifest_SHA256": PRIMARY_MANIFEST_SHA, "primary_source_SHA256": PRIMARY_SOURCE_SHA,
        "primary_READY_SHA256": PRIMARY_READY_SHA, "primary_protocol_SHA256": PRIMARY_PROTOCOL_SHA,
        "primary_expected_counts": [7, 16, 2843],
        "source_execution": {"primary_or_historical_imported_or_executed": False, "independent_scientific_arithmetic_in_prepare": False},
        "independent_oracles": {"support_even_odd": [96, 97], "positive_exp_terms": 80,
                                "construction": "Direct integer powers/factorials; no primary recurrence"},
        "complete_comparison_counts": {"looks": 20, "branches": 17, "branch_zero_floors": 340, "S_retaining_frontiers": 340},
        "new_release_and_primary_root_relative_members": MAX_ADMITTED_ROOT_MEMBERS,
        "complete_primary_input_map_members": MAX_PRIMARY_INPUT_MEMBERS,
        "historical_scope": "Twelve exact metadata bytes and selected literal membership; no recursive historical runtime promotion",
        "runtime_layout": {"isolated": True, "no_site": True, "bytecode_writes": False,
                           "sys_path": [str(BASE / "python312.zip"), str(BASE / "DLLs"), str(BASE / "Lib"), str(BASE)],
                           "base_prefix": str(BASE), "prefix": str(BASE), "python312_zip_expected_absent": True,
                           "unused_site_packages_captured": False, "Windows_system_DLL_hashes_captured": False,
                           "absent_loaded_cache_paths": sorted(str(path) for path in _ABSENT_CACHES)},
        "scope": dict(_SCOPE),
        "budgets": {"CPU": CPU_LIMIT, "admission_CPU": WORK_LIMIT, "wall": WALL_LIMIT,
                    "owned_files": MAX_OWNED_FILES, "owned_bytes": MAX_OWNED_BYTES,
                    "runtime_files": MAX_RUNTIME_FILES, "runtime_bytes": MAX_RUNTIME_BYTES,
                    "release_files": MAX_FROZEN_FILES, "release_bytes": MAX_FROZEN_BYTES, "single_file_bytes": MAX_SINGLE_BYTES},
    }


def prepare(args, started):
    global _ATTEMPT_ROUTE_OWNED
    invocation_check(started)
    require(not OUTPUT.exists() and not OUTPUT.is_symlink(), "Never reuse an auditor route")
    frozen = root_release(args.root_ready_sha256, started)
    runtime, runtime_bytes = runtime_packet(started)
    require(runtime == _PRIMARY_RUNTIME_EXPECTED, "Current runtime hashes match the complete externally pinned primary runtime")
    loaded_runtime_check(runtime, started)
    guard(started, admission=True)
    OUTPUT.mkdir(parents=False, exist_ok=False)
    _ATTEMPT_ROUTE_OWNED = True
    write_json(OUTPUT / "protocol.json", protocol_value(frozen, runtime, runtime_bytes), started)
    protocol_sha256 = hashlib.sha256(stable_read(OUTPUT / "protocol.json", started)).hexdigest()
    terminal = complete_union(frozen, runtime, started, protocol_sha256)
    guard(started)
    print(json.dumps({"prepare_passed": True, "scientific_evaluation": False,
                      "protocol": relative(OUTPUT / "protocol.json"), "protocol_sha256": protocol_sha256,
                      "prepare_terminal_full_verification": terminal,
                      "observed_CPU": time.process_time(), "observed_wall": time.monotonic() - started}), flush=True)


def pair_value(pair):
    require(type(pair) is list and len(pair) == 2 and all(type(value) is int for value in pair)
            and pair[1] > 0, "Exact rational integer pair")
    value = Fraction(pair[0], pair[1])
    require([value.numerator, value.denominator] == pair, "Primary pair remains reduced and canonical")
    return value


def same_pair(pair, expected, message):
    actual = pair_value(pair)
    require(actual.numerator * expected.denominator == expected.numerator * actual.denominator, message)


def decimal_value(text):
    require(type(text) is str and re.fullmatch(r"[0-9]+\.[0-9]+", text), "Original positive finite decimal literal")
    whole, fraction = text.split(".")
    return Fraction(int(whole + fraction), 10 ** len(fraction))


def direct_signed_terms(base_numerator, base_denominator, last, started):
    values = []
    for degree in range(last + 1):
        guard(started, admission=True)
        values.append(Fraction(base_numerator ** degree, (base_denominator ** degree) * factorial(degree)))
    return values


def independent_oracles(checks, low, high, started):
    positive_records = []
    for argument, threshold, primary_key in ((12, 136000, "L64_exp12_lower"), (10, 16000, "L64_exp10_lower")):
        terms = direct_signed_terms(argument, 1, POSITIVE_EXP_TERMS - 1, started)
        require(len(terms) == 80 and all(value > 0 for value in terms), "Exactly80 positive finite terms k0..79")
        bound80 = sum(terms, Fraction(0))
        primary64 = sum(terms[:65], Fraction(0))
        require(bound80 > threshold and primary64 > threshold and primary64 < bound80,
                "Independent strict rational logarithm proof and original64-prefix consistency")
        same_pair(checks[primary_key], primary64, "Independently rebuilt original exact64 polynomial")
        positive_records.append({"argument": argument, "strict_threshold": threshold,
                                 "independent_positive_80term_sum": rational(bound80), "independent_original_L64": rational(primary64),
                                 "positive_tail_proof": "All omitted terms are positive, so finite polynomial is strictly below exp"})
    terms = direct_signed_terms(-3, 100, SUPPORT_ODD_TERMS, started)
    require(len(terms) == 98 and all(abs(terms[k + 1]) < abs(terms[k]) for k in range(97)),
            "Fixed98 signed terms with strictly decreasing magnitudes")
    lower97 = 10000 * sum(terms, Fraction(0))
    upper96 = 10000 * sum(terms[:SUPPORT_EVEN_TERMS + 1], Fraction(0))
    require(0 < low <= lower97 < upper96 <= high,
            "Copied exact support endpoints contain fixed96/97 alternating enclosure")
    primary_lower65 = 10000 * sum(terms[:66], Fraction(0))
    primary_upper64 = 10000 * sum(terms[:65], Fraction(0))
    old = checks["ideal_support_enclosure"]
    same_pair(old["exact_lower_partial_k0_through65"], primary_lower65, "Independent factorial reconstruction of primary odd65 value")
    same_pair(old["exact_upper_partial_k0_through64"], primary_upper64, "Independent factorial reconstruction of primary even64 value")
    require(primary_lower65 < lower97 < upper96 < primary_upper64,
            "New fixed enclosure is nested inside independently reconstructed original enclosure")
    require(old["passed"] is True and old["expression"] == "10000*exp(-3/100)"
            and old["copied_lower_contains_exact_lower"] is True and old["copied_upper_contains_exact_upper"] is True
            and old["fixed_terms_retuned_or_support_strings_replaced"] is False
            and old["actual_digital_residual_law_or_support_proved"] is False,
            "Primary support proof remains ideal-only with fixed endpoints")
    return {"schema": "e12-near-one-independent-rational-oracles-v1", "passed": True,
            "positive_exp_proofs": positive_records, "support_lower97": rational(lower97),
            "support_upper96": rational(upper96), "support_term_magnitude_ratio": "3/[100*(k+1)]<1 and tends to0",
            "alternating_remainder_proof": "Even96 upper and next odd97 lower, strictly decreasing magnitudes tending to zero",
            "copied_support_enclosure_proved": True, "primary64_65_certificate_reconstructed": True,
            "scientific_primary_functions_reused": False, "scope": dict(_SCOPE)}


def branch_basis(started):
    rows = [{"lambda": Fraction(15, 16), "intercept": Fraction(64, 5),
             "slope": Fraction(15, 2), "inverse_slope": Fraction(2, 15)}]
    for exponent in range(1, 17):
        guard(started, admission=True)
        denominator = 2 ** exponent
        rows.append({"lambda": Fraction(1, denominator), "intercept": Fraction(12 * denominator),
                     "slope": Fraction(1, 2 * denominator - 2), "inverse_slope": Fraction(2 * denominator - 2)})
    require(len(rows) == 17 and len({row["lambda"] for row in rows}) == 17, "All17 original branches remain paid")
    for row in rows:
        guard(started, admission=True)
        lam, intercept, slope, inverse = (row[key] for key in ("lambda", "intercept", "slope", "inverse_slope"))
        require(0 < lam < 1 and intercept > 0 and slope > 0 and inverse > 0, "Every frozen normalization and sign premise")
        require(intercept * lam == 12 and slope * inverse == 1 and 2 * slope * (1 - lam) == lam,
                "Independent closed forms satisfy exact boundary equations")
    require(min(row["intercept"] for row in rows) == Fraction(64, 5), "Exact full-grid zero intercept")
    return rows


def allocation_check(protocol, checks, branches, started):
    per_process, fallback_sign = Fraction(1, 136000), Fraction(1, 8000)
    per_CS, per_F = 2 * len(branches) * per_process, 2 * fallback_sign
    per_stream, total = per_CS + per_F, 2 * (per_CS + per_F)
    require(per_CS == per_F == Fraction(1, 4000) and per_stream == Fraction(1, 2000)
            and total == Fraction(1, 1000), "Complete stream, sign and all-lambda budgets reserved")
    expected = {"total_two_streams": total, "per_stream": per_stream, "per_stream_CS": per_CS,
                "per_stream_fallback": per_F, "per_CS_sign_lambda": per_process, "per_fallback_sign": fallback_sign}
    require(protocol["failure"]["stream_count"] == 2 and set(protocol["failure"]) == set(expected) | {"stream_count"},
            "Exact complete primary failure allocation shape")
    for key, value in expected.items():
        guard(started, admission=True)
        same_pair(protocol["failure"][key], value, "Primary allocation equals independent complete union")
    same_pair(checks["per_process_CS_failure"], per_process, "Original per-process CS failure")
    same_pair(checks["two_stream_total_failure"], total, "Original two-stream failure")
    same_pair(checks["u0"], Fraction(64, 5), "Original minimum intercept")
    same_pair(checks["near_one_V_slope"], Fraction(15, 2), "Original near-one slope")
    require(checks["passed"] is True and checks["lambda_count"] == 17 and checks["sign_lambda_processes_per_stream"] == 34
            and checks["strict_thresholds"] == [136000, 16000] and checks["recurrence_increments_after_constant"] == 64
            and checks["Bernoulli_histories_or_seeded_traces_or_sqrt_QA"] == 0
            and checks["actual_financial_observations_or_IID_proof"] is False,
            "Original completed checks retain fixed certificate-only scope")
    require(protocol["lambda_values"] == [rational(row["lambda"]) for row in branches]
            and protocol["cap"] == N_CAP and protocol["looks"] == list(LOOKS)
            and protocol["log_majorants"] == {"CS": 12, "fixed_N": 10}
            and protocol["positive_data_statistics"] == {"S": "sum_i X_i", "V": "sum_i X_i^2", "actual_observations_evaluated": False},
            "True squared group statistic; no Bernoulli shortcut or extra factor4")
    return {"passed": True, "per_stream": rational(per_stream), "two_stream_total": rational(total),
            "per_CS_sign_lambda": rational(per_process), "per_fallback_sign": rational(fallback_sign),
            "all_sign_lambda_processes_reserved_per_stream": 34, "stream_count": 2,
            "predictable_bounded_predictor": "0", "true_V": "sum_i X_i^2", "Howard_scale_c": 1,
            "additional_factor4": False, "fallback_fixed_cap_only": True,
            "Howard_Theorem4_Lemma1": "https://arxiv.org/html/1810.08240v5",
            "Maurer_Pontil_Theorem4": "https://arxiv.org/pdf/0907.3740", "scope": dict(_SCOPE)}


def independent_decision(low, high, target):
    if low.numerator * target.denominator > target.numerator * low.denominator:
        return "FIXED_CHANNEL_REJECTED_BEFORE_ACQUISITION"
    if high.numerator * target.denominator <= target.numerator * high.denominator:
        return "NECESSARY_ZERO_FLOOR_GATE_CLEARS_ONLY"
    return "SUPPORT_ENCLOSURE_COMPARISON_UNRESOLVED"


def comparison_rows(screen, frontiers, low, high, target, branches, started):
    require(screen["schema"] == "e12-near-one-lambda-zero-floor-screen-v1"
            and frontiers["schema"] == "e12-near-one-lambda-fixed-branch-frontiers-v1"
            and type(screen["rows"]) is list and len(screen["rows"]) == 20
            and type(frontiers["rows"]) is list and len(frontiers["rows"]) == 340,
            "Complete primary20-look340-frontier evidence")
    floors, frontier_rows = [], []
    for look_index, n in enumerate(LOOKS):
        guard(started, admission=True)
        row = screen["rows"][look_index]
        require(row["n"] == n, "Exact ordered frozen look")
        branch_floors = []
        for branch_index, branch in enumerate(branches):
            guard(started, admission=True)
            intercept, slope, inverse = (branch[key] for key in ("intercept", "slope", "inverse_slope"))
            floor_low, floor_high = low * intercept / n, high * intercept / n
            branch_floors.append({"lambda": rational(branch["lambda"]), "lower": rational(floor_low), "upper": rational(floor_high)})
            saved = frontiers["rows"][17 * look_index + branch_index]
            constant = inverse * n * target / high - inverse * intercept
            S_coefficient = -inverse
            require(saved["n"] == n, "Exact original branch look")
            same_pair(saved["lambda"], branch["lambda"], "Every frozen branch lambda")
            same_pair(saved["normalized_boundary_intercept"], intercept, "Every independent intercept")
            same_pair(saved["normalized_boundary_V_slope"], slope, "Every independent positive V slope")
            same_pair(saved["V_threshold"]["constant"], constant, "Every exact frontier constant including sign")
            same_pair(saved["V_threshold"]["S_coefficient"], S_coefficient, "Every negative empirical-S coefficient")
            require(S_coefficient < 0 and constant * slope + intercept == n * target / high and S_coefficient * slope == -1,
                    "All normalization and empirical mean algebra retained")
            require(saved["S_retained_symbolically"] is True and saved["requires_nonnegative_right_side_and_sound_S_V"] is True
                    and saved["conservative_support_endpoint"] == "B2_upper"
                    and saved["sufficient_future_branch_test"] == "S+intercept+V_slope*V<=n*T/B2_upper"
                    and saved["actual_S_or_V_observed"] is False and saved["V_threshold"]["formula"] == "constant+S_coefficient*S",
                    "Original frontier retains S, upper support and nonnegative RHS")
            frontier_rows.append({"n": n, "lambda": rational(branch["lambda"]), "intercept": rational(intercept),
                                  "V_slope": rational(slope), "constant": rational(constant),
                                  "constant_sign": (constant > 0) - (constant < 0), "S_coefficient": rational(S_coefficient),
                                  "all_primary_coefficients_match": True, "S_retained_symbolically": True})
        cs_low = min(pair_value(branch["lower"]) for branch in branch_floors)
        cs_high = min(pair_value(branch["upper"]) for branch in branch_floors)
        fallback_low, fallback_high = low * 70 / (3 * (n - 1)), high * 70 / (3 * (n - 1))
        for key, value in (("CS_floor_lower", cs_low), ("CS_floor_upper", cs_high),
                           ("fallback_floor_lower", fallback_low), ("fallback_floor_upper", fallback_high)):
            same_pair(row[key], value, "Every exact primary floor endpoint")
        cs_decision = independent_decision(cs_low, cs_high, target)
        fallback_decision = independent_decision(fallback_low, fallback_high, target)
        require(row["CS_zero_floor_decision"] == cs_decision and row["fallback_zero_floor_decision"] == fallback_decision
                and row["fallback_is_allowed_delivery_look"] is (n == N_CAP)
                and row["intermediate_fallback_rows_are_static_diagnostics_not_optional_stopping_bounds"] is True
                and row["necessary_screen_is_actual_delivery"] is False,
                "Every directed floor decision and fixed-cap fallback restriction")
        floors.append({"n": n, "all17_branch_zero_floors": branch_floors,
                       "CS_floor_lower": rational(cs_low), "CS_floor_upper": rational(cs_high),
                       "fallback_floor_lower": rational(fallback_low), "fallback_floor_upper": rational(fallback_high),
                       "CS_decision": cs_decision, "fallback_decision": fallback_decision,
                       "fallback_permitted_delivery_look": n == N_CAP, "conditional_screen_only": True})
    cs, fallback = floors[-1]["CS_decision"], floors[-1]["fallback_decision"]
    if cs == fallback == "FIXED_CHANNEL_REJECTED_BEFORE_ACQUISITION":
        decision = "FIXED_CANDIDATE_REJECTED_BEFORE_ACQUISITION"
    elif "NECESSARY_ZERO_FLOOR_GATE_CLEARS_ONLY" in (cs, fallback):
        decision = "NECESSARY_GATE_CLEARS_FINANCE_STILL_UNAUTHORIZED"
    else:
        decision = "SUPPORT_ENCLOSURE_COMPARISON_UNRESOLVED_FINANCE_UNAUTHORIZED"
    require(screen["CS_cap_decision"] == cs and screen["fallback_cap_decision"] == fallback and screen["decision"] == decision
            and screen["all_zero_financial_dataset_observed_or_claimed"] is False
            and screen["screen_clearance_proves_financial_delivery_or_source_premises"] is False,
            "Primary whole-grid necessary conclusion reconstructed without synthetic observations")
    require(frontiers["admissible_statistics"] == "S^2/n<=V<=S<=n"
            and frontiers["full_grid_test"] == "V<=max_lambda(constant+S_coefficient*S), with nonnegative RHS"
            and frontiers["one_branch_fails_does_not_reject_full_grid"] is True
            and frontiers["empirical_S_omitted_or_replaced_by_zero"] is False
            and frontiers["actual_positive_data_delivery_or_acquisition_authorized"] is False,
            "Original full-grid S-retaining sufficient-frontier semantics preserved")
    return floors, frontier_rows, decision


def audit_primary(frozen, started):
    packets = {name: json.loads(checked_read(PRIMARY / name, PRIMARY_OWNED[name], started))
               for name in ("protocol.json", "checks.json", "screen.json", "frontiers.json", "summary.json")}
    finance = pinned_json("results/limitation_program_20261001/E12_continuation_20261004_screen_run001/finance_admission.json", frozen, started)
    proposal_key = next(key for key in PROPOSAL_PINS if key.endswith(".json"))
    proposal = json.loads(checked_read(ROOT / proposal_key, PROPOSAL_PINS[proposal_key], started))
    names = (("support_squared_lower", "support_squared_lower_copied_string"),
             ("support_squared_upper", "support_squared_upper_copied_string"),
             ("target_dollars_squared", "target_dollars_squared_copied_string"))
    strings = {}
    for original, selected in names:
        require(finance[original] == proposal["financial_selection"][selected], "Exact support and target strings are never retuned")
        strings[original] = finance[original]
    low, high, target = [decimal_value(strings[key]) for key, _ in names]
    require(0 < low < high and 0 < target < low, "Directed positive exact decimal support and target")
    branches = branch_basis(started)
    allocation = allocation_check(packets["protocol.json"], packets["checks.json"], branches, started)
    oracles = independent_oracles(packets["checks.json"], low, high, started)
    floors, frontiers, decision = comparison_rows(packets["screen.json"], packets["frontiers.json"], low, high, target, branches, started)
    summary = packets["summary.json"]
    require(summary["schema"] == "e12-near-one-lambda-static-screen-summary-v1"
            and summary["passed"] is True and summary["exact_static_screen_complete"] is True
            and summary["case"] == "C4" and summary["compound_strike"] == 6
            and summary["copied_finance_strings"] == strings and summary["sample_cap"] == N_CAP
            and summary["looks_completed"] == 20 and summary["branch_frontiers_completed"] == 340
            and summary["decision"] == decision and summary["CS_cap_decision"] == floors[-1]["CS_decision"]
            and summary["fallback_cap_decision"] == floors[-1]["fallback_decision"]
            and summary["historical_rejection_changed"] is False and summary["zero_floor_clearance_is_financial_delivery"] is False
            and summary["scope"] == packets["protocol.json"]["scope"],
            "Exact primary conditional necessary-screen summary independently consumed")
    return allocation, oracles, floors, frontiers, decision


def seal(protocol, frozen, runtime, started, before, after, protocol_expected):
    observed = guard(started)
    names = {"protocol.json", "run_started.json", "allocation_audit.json", "oracle_audit.json",
             "floor_audit.json", "frontier_audit.json", "summary.json", "verification.json"}
    require({path.name for path in OUTPUT.iterdir()} == names, "Only exact complete audit artifacts may seal")
    owned, total = {}, 0
    for path in sorted(OUTPUT.iterdir(), key=str):
        data = stable_read(path, started)
        total += len(data)
        owned[relative(path)] = hashlib.sha256(data).hexdigest()
    require(owned[relative(OUTPUT / "protocol.json")] == protocol_expected, "Expected external phase protocol unchanged")
    value = {"schema": "e12-near-one-lambda-static-audit-manifest-v1", "passed": True, "completed": True,
             "budget_censored": False, "error": None, "owned_files": owned, "frozen_inputs": frozen,
             "external_runtime_inputs": runtime, "fresh_before": before, "fresh_after": after,
             "prepared_protocol_SHA256": protocol_expected, "primary_manifest_SHA256": PRIMARY_MANIFEST_SHA,
             "scope": protocol["scope"], "financial_adoption_approved": False,
             "manifest_self_hash_excluded": True, "manifest_inclusive_owned_file_count": len(owned) + 1,
             "owned_nonmanifest_bytes": total, "manifest_inclusive_retention_checked_before_sealing": True,
             "observed_CPU": observed[0], "observed_wall": observed[1]}
    encoded = 1
    for fragment in json.JSONEncoder(indent=2, sort_keys=True, allow_nan=False).iterencode(value):
        guard(started)
        encoded += len(fragment.encode("utf-8"))
        require(total + encoded <= MAX_OWNED_BYTES, "Pre-admitted UTF8 bytes inclusive of audit manifest")
    require(len(owned) + 1 <= MAX_OWNED_FILES, "Complete audit file cap inclusive of manifest")
    write_json(OUTPUT / "manifest.json", value, started)
    actual = set(OUTPUT.iterdir())
    require(actual == {ROOT / key for key in owned} | {OUTPUT / "manifest.json"}
            and len(actual) == len(owned) + 1 <= MAX_OWNED_FILES, "Exact complete final audit ownership")
    actual_bytes = 0
    for path in actual:
        guard(started)
        require(path.is_file() and path.resolve(strict=True) == path, "Final regular confined audit member")
        actual_bytes += path.stat().st_size
    require((OUTPUT / "manifest.json").stat().st_size == encoded and actual_bytes == total + encoded <= MAX_OWNED_BYTES,
            "Exact inclusive final audit UTF8 byte accounting")
    guard(started)


def run(args, started):
    global _ATTEMPT_ROUTE_OWNED
    require(OUTPUT.is_dir() and OUTPUT.resolve(strict=True) == OUTPUT
            and {path.name for path in OUTPUT.iterdir()} == {"protocol.json"}, "One exact fresh prepared auditor route")
    _ATTEMPT_ROUTE_OWNED = True
    invocation_check(started)
    protocol = json.loads(checked_read(OUTPUT / "protocol.json", args.protocol_sha256, started))
    frozen = root_release(args.root_ready_sha256, started)
    runtime, runtime_bytes = runtime_packet(started)
    require(runtime == _PRIMARY_RUNTIME_EXPECTED and runtime == protocol["external_runtime_inputs"],
            "Complete original expected runtime and prepared auditor runtime agree")
    loaded_runtime_check(runtime, started)
    require(protocol == protocol_value(frozen, runtime, runtime_bytes), "Entire separately frozen auditor protocol exact")
    before = complete_union(frozen, runtime, started, args.protocol_sha256)
    guard(started, admission=True)
    write_json(OUTPUT / "run_started.json", {"PID": os.getpid(), "protocol_expected_SHA256": args.protocol_sha256,
               "root_ready_expected_SHA256": args.root_ready_sha256, "independent_bound_evaluation_started": False,
               "observed_CPU": time.process_time(), "observed_wall": time.monotonic() - started, "scope": dict(_SCOPE)}, started)
    allocation, oracles, floors, frontiers, decision = audit_primary(frozen, started)
    write_json(OUTPUT / "allocation_audit.json", allocation, started)
    write_json(OUTPUT / "oracle_audit.json", oracles, started)
    write_json(OUTPUT / "floor_audit.json", {"passed": True, "rows": floors, "look_count": 20,
               "all_branch_floor_count": 340, "decision": decision, "scope": dict(_SCOPE)}, started)
    write_json(OUTPUT / "frontier_audit.json", {"passed": True, "rows": frontiers, "comparison_count": 340,
               "S_retained_symbolically": True, "actual_data_supplied": False, "scope": dict(_SCOPE)}, started)
    write_json(OUTPUT / "summary.json", {"schema": "e12-near-one-lambda-static-audit-summary-v1", "passed": True,
               "independent_exact_static_audit_complete": True, "primary_manifest_SHA256": PRIMARY_MANIFEST_SHA,
               "primary_decision_reconstructed": decision, "frozen_looks_compared": 20, "branch_zero_floors_rebuilt": 340,
               "S_retaining_frontiers_compared": 340, "necessary_floor_clearance_is_conditional_only": True,
               "financial_IID_digital_support_or_actual_delivery_proved": False, "scope": dict(_SCOPE)}, started)
    after = complete_union(frozen, runtime, started, args.protocol_sha256)
    write_json(OUTPUT / "verification.json", {"passed": True, "before": before, "after": after,
               "expected_hash_waivers": 0, "fixture_credit": 0, "primary_or_historical_source_executed": False,
               "scope": dict(_SCOPE)}, started)
    seal(protocol, frozen, runtime, started, before, after, args.protocol_sha256)
    print(json.dumps({"passed": True, "independent_exact_static_audit_complete": True,
                      "primary_decision_reconstructed": decision, "manifest": relative(OUTPUT / "manifest.json"),
                      "scope": dict(_SCOPE), "observed_CPU": time.process_time(),
                      "observed_wall": time.monotonic() - started}), flush=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--root-ready-sha256", required=True)
    parser.add_argument("--protocol-sha256")
    args = parser.parse_args()
    started = started_clock()
    require(
        args.mode == "prepare" or args.protocol_sha256 is not None,
        "ROOT must separately freeze prepared protocol",
    )
    try:
        if args.mode == "prepare":
            require(args.protocol_sha256 is None, "Prepare does not admit a pre-existing protocol")
            prepare(args, started)
        else:
            run(args, started)
    except BaseException as error:
        preserve_failure(error, started)
        raise

if __name__ == "__main__":
    main()
