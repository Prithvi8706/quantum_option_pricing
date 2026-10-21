"""Prospective E12 exact static opportunity screen; no sampling or adoption.

Run only after an independently frozen ROOT release and prepared protocol.
Historical source files are byte inputs only and are never imported.
The ideal support expression is independently enclosed by fixed alternating
terms k=0..64 and next65; copied endpoints must contain that enclosure.
This prerequisite does not certify an actual digital residual support.
"""

from __future__ import annotations
import argparse
import ctypes
from ctypes import wintypes
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "research/limitation_program_20261001"
AUTHOR = HERE / "experiment_e12_near_one_lambda_static_screen_v1.py"
METHOD_MD = HERE / "E12_NEAR_ONE_LAMBDA_PROPOSAL_V1.md"
METHOD_JSON = HERE / "E12_NEAR_ONE_LAMBDA_PROPOSAL_V1.json"
READY = ROOT / ".context/E12_near_one_lambda_static_screen_ROOT_READY_run001.json"
OUTPUT = ROOT / "results/limitation_program_20261001/E12_near_one_lambda_static_screen_run001"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
BASE = Path("C:/Users/prith/AppData/Local/Programs/Python/Python312")
LAUNCHER_SHA = "41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5"
BASE_SHA = "fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b"
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
CPU_LIMIT, WORK_LIMIT, WALL_LIMIT = (180, 150, 600)
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = (4096, 512 << 20)
MAX_FROZEN_FILES, MAX_FROZEN_BYTES = (16, 8 << 20)
MAX_OWNED_FILES, MAX_OWNED_BYTES = (16, 16 << 20)
MAX_SINGLE_BYTES = 64 << 20
SHA = re.compile("[0-9a-f]{64}\\Z")
ALPHA = Fraction(1, 1000)
STREAM_ALPHA = ALPHA / 2
CS_ALPHA = FALLBACK_ALPHA = STREAM_ALPHA / 2
LAMBDAS = (Fraction(15, 16),) + tuple(Fraction(1, 1 << j) for j in range(1, 17))
CS_LOG_MAJORANT, FIXED_LOG_MAJORANT = (12, 10)
N_CAP = 1 << 20
LOOKS = tuple(1 << j for j in range(1, 21))
_ABSENT_CACHES = set()
_ATTEMPT_ROUTE_OWNED = False


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


def exp_lower(integer, terms, started):
    term = total = Fraction(1)
    for k in range(1, terms + 1):
        guard(started)
        term *= Fraction(integer, k)
        total += term
    return total


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


def root_release(expected, started):
    raw = checked_read(READY, expected, started)
    ready = json.loads(raw)
    require(
        ready.get("schema") == "root-e12-near-one-lambda-static-screen-READY-v1",
        "Exact new ROOT header",
    )
    require(
        ready.get("passed") is True
        and ready.get("static_review_only") is True
        and ready.get("root_and_independent_static_reviews_passed") is True
        and ready.get("exact_static_screen_execution_approved") is True,
        "Independent ROOT and peer release of this exact static screen only",
    )
    require(
        ready.get("ideal_support_alternating64plus_next65_check_required") is True,
        "ROOT releases the fixed independent ideal-support enclosure check",
    )
    require(
        ready.get("statistical_sampling_approved") is False
        and ready.get("financial_acquisition_approved") is False
        and ready.get("financial_adoption_approved") is False
        and ready.get("quantum_gate_emissions_authorized") is False
        and ready.get("program_fixture_credit") == 0,
        "Zero samples, finance adoption, gates and fixture credit",
    )
    require(
        ready.get("output_route") == relative(OUTPUT)
        and ready.get("CPU_admission_wall_seconds") == [CPU_LIMIT, WORK_LIMIT, WALL_LIMIT],
        "Fixed route and unchanged complete-process budgets",
    )
    expected_keys = {relative(AUTHOR)} | set(PROPOSAL_PINS) | set(REFERENCES)
    mapping = ready.get("frozen_inputs")
    require(
        type(mapping) is dict and set(mapping) == expected_keys and len(mapping) == 15,
        "Exactly fifteen selected direct source/method/history inputs",
    )
    require(
        all(mapping[k] == v for k, v in (REFERENCES | PROPOSAL_PINS).items()),
        "Immutable history and accepted proposal expected hashes",
    )
    total = 0
    for key, digest in mapping.items():
        exact_relative_key(key)
        total += len(checked_read(ROOT / key, digest, started))
    require(
        len(mapping) + 1 == MAX_FROZEN_FILES and total + len(raw) <= MAX_FROZEN_BYTES,
        "Exactly sixteen frozen members including new ROOT_READY and bounded total bytes",
    )
    proposal = json.loads(checked_read(METHOD_JSON, PROPOSAL_PINS[relative(METHOD_JSON)], started))
    require(
        proposal.get("schema") == "e12-near-one-lambda-static-proposal-v1"
        and proposal.get("immutable_history_pins") == REFERENCES,
        "Exact accepted static proposal and its twelve unchanged history pins",
    )
    future = proposal["future_static_screen_contract"]
    require(
        future["planned_route_only_not_created"] == relative(OUTPUT)
        and future["phase_CPU_seconds"] == CPU_LIMIT
        and future["admission_CPU_seconds"] == WORK_LIMIT
        and future["phase_wall_seconds_from_actual_process_creation"] == WALL_LIMIT
        and future["runtime_file_cap"] == MAX_RUNTIME_FILES
        and future["runtime_byte_cap"] == MAX_RUNTIME_BYTES
        and future["frozen_file_cap"] == MAX_FROZEN_FILES
        and future["frozen_byte_cap"] == MAX_FROZEN_BYTES
        and future["owned_file_cap_including_manifest"] == MAX_OWNED_FILES
        and future["owned_byte_cap_including_manifest"] == MAX_OWNED_BYTES
        and future["individual_file_byte_cap"] == MAX_SINGLE_BYTES
        and future["statistical_or_financial_draws"] == 0
        and future["residual_probes_or_gate_generation"] == 0,
        "All accepted prospective caps and absence of sampling remain fixed",
    )
    require(
        proposal["confidence_sequence"]["lambda_count"] == 17
        and proposal["confidence_sequence"]["lambdas"]
        == ["15/16"] + [f"1/{1 << j}" for j in range(1, 17)]
        and proposal["confidence_sequence"]["look_exponents"] == list(range(1, 21))
        and proposal["failure_allocation"]["required_future_exact_exp_checks"]
        == ["L_64(12)>136000", "L_64(10)>16000"],
        "Fixed seventeen-branch grid, twenty looks and stronger logarithm proof obligations",
    )
    history_membership(mapping, started)
    finance = pinned_json(
        (
            "results/limitation_program_20261001/E12_continuation_20"
            "261004_screen_run001/finance_admission.json"
        ),
        mapping,
        started,
    )
    foreign_protocol = pinned_json(
        "docs/limitation_program_20261001/continuation_20261004/E12/PROTOCOL.json",
        mapping,
        started,
    )
    foreign_selection = foreign_protocol["finance_admission"]
    require(
        foreign_selection["sample_cap"] == N_CAP
        and foreign_selection["inner_group_size"] == 16
        and foreign_selection["support_squared"]
        == (
            "W=10000*exp(-3/100) dollars squared, original strike 100 "
            "and half-maturity discount exp(-.015)."
        ),
        "Unchanged cap, group size and ideal-support expression in actual retained method",
    )
    selection = proposal["financial_selection"]
    require(
        finance["schema"] == "e12-finance-admission-v1"
        and finance["case"] == selection["case"] == "C4"
        and finance["compound_strike"] == selection["compound_strike"] == 6
        and finance["status"] == "FIXED_STOPPING_RULE_REJECTED_BEFORE_ACQUISITION"
        and finance["finance_draws"] == 0
        and selection["sample_cap"] == N_CAP
        and selection["inner_group_size"] == 16,
        "Exact retained finance selection; original rejection and zero draws stay intact",
    )
    for key, copied in (
        ("support_squared_lower", "support_squared_lower_copied_string"),
        ("support_squared_upper", "support_squared_upper_copied_string"),
        ("target_dollars_squared", "target_dollars_squared_copied_string"),
    ):
        require(
            type(finance[key]) is str and finance[key] == selection[copied],
            "Verbatim support and target strings; no numerical evaluation in prepare",
        )
    mapping = dict(mapping)
    mapping[relative(READY)] = expected
    return mapping


def protocol_value(frozen, runtime, runtime_bytes):
    return {
        "schema": "e12-near-one-lambda-static-screen-protocol-v1",
        "local_only": True,
        ("scientific_scope"): (
            "Exact necessary opportunity screen only; no observation"
            " source, sampling, delivery or adoption"
        ),
        "frozen_inputs": frozen,
        "external_runtime_inputs": runtime,
        "external_runtime_bytes": runtime_bytes,
        ("historical_manifest_scope"): (
            "Only twelve direct pinned bytes and their literal selec"
            "ted-member relations; old dependency/runtime maps are n"
            "ot recursively fresh verified"
        ),
        "lambda_values": [rational(x) for x in LAMBDAS],
        "cap": N_CAP,
        "looks": list(LOOKS),
        "log_majorants": {"CS": CS_LOG_MAJORANT, "fixed_N": FIXED_LOG_MAJORANT},
        "exp_recurrence_increments": 64,
        "ideal_support_enclosure_check": {
            "expression": "10000*exp(-3/100)",
            "upper_partial_terms": "k=0..64",
            "lower_partial_terms": "k=0..65",
            "required_containment": "copied_B2_lower<=exact_lower<=exact_upper<=copied_B2_upper",
            "terms_or_copied_endpoints_retuned": False,
            "actual_digital_residual_support_certified": False,
        },
        "failure": {
            "total_two_streams": rational(ALPHA),
            "stream_count": 2,
            "per_stream": rational(STREAM_ALPHA),
            "per_stream_CS": rational(CS_ALPHA),
            "per_stream_fallback": rational(FALLBACK_ALPHA),
            "per_CS_sign_lambda": rational(Fraction(1, 136000)),
            "per_fallback_sign": rational(Fraction(1, 8000)),
        },
        "positive_data_statistics": {
            "S": "sum_i X_i",
            "V": "sum_i X_i^2",
            "actual_observations_evaluated": False,
        },
        "future_sqrt_grid_not_evaluated_here": "2^-64",
        "runtime_layout": {
            "isolated": True,
            "no_site": True,
            "bytecode_writes": False,
            "sys_path": [
                str(BASE / "python312.zip"),
                str(BASE / "DLLs"),
                str(BASE / "Lib"),
                str(BASE),
            ],
            "base_prefix": str(BASE),
            "prefix": str(BASE),
            "python312_zip_expected_absent": True,
            "unused_site_packages_captured": False,
            "Windows_system_DLL_hashes_captured": False,
            "absent_loaded_cache_paths": sorted(str(path) for path in _ABSENT_CACHES),
        },
        "scope": {
            "program_fixture_credit": 0,
            "statistical_draws": 0,
            "financial_draws": 0,
            "financial_replays": 0,
            "G2_transfer": False,
            "G3_price_delivery": False,
            "classical_comparator": False,
            "finance_execution": False,
            "finance_adoption": False,
            "source_adoption": False,
            "quantum_gate_emissions": 0,
            "financial_target_delivery": False,
            "measured_latency_or_quantum_advantage": False,
        },
        "budgets": {
            "CPU": CPU_LIMIT,
            "admission_CPU": WORK_LIMIT,
            "wall": WALL_LIMIT,
            "owned_files": MAX_OWNED_FILES,
            "owned_bytes": MAX_OWNED_BYTES,
            "runtime_files": MAX_RUNTIME_FILES,
            "runtime_bytes": MAX_RUNTIME_BYTES,
            "frozen_files": MAX_FROZEN_FILES,
            "frozen_bytes": MAX_FROZEN_BYTES,
            "single_file_bytes": MAX_SINGLE_BYTES,
        },
    }


def exact_static_checks(started):
    per_process = CS_ALPHA / (2 * len(LAMBDAS))
    require(
        per_process == Fraction(1, 136000),
        "All34 fixed processes receive the complete split allocation",
    )
    require(
        FALLBACK_ALPHA / 2 == Fraction(1, 8000), "Both fixed-N signs receive their split allocation"
    )
    require(2 * (CS_ALPHA + FALLBACK_ALPHA) == ALPHA, "Complete two-stream moment failure union")
    exp12, exp10 = exp_lower(12, 64, started), exp_lower(10, 64, started)
    require(exp12 > 136000 and exp10 > 16000, "Strict rational stronger logarithm-majorant checks")
    require(
        len(LAMBDAS) == len(set(LAMBDAS)) == 17 and all(0 < x < 1 for x in LAMBDAS),
        "Fixed admissible17 positive lambdas",
    )
    intercepts = tuple(Fraction(CS_LOG_MAJORANT, 1) / x for x in LAMBDAS)
    zero = min(intercepts)
    near_slope = LAMBDAS[0] / (2 * (1 - LAMBDAS[0]))
    require(
        zero == Fraction(64, 5) and near_slope == Fraction(15, 2),
        "Exact new zero intercept and positive-V penalty",
    )
    return {
        "passed": True,
        "L64_exp12_lower": rational(exp12),
        "L64_exp10_lower": rational(exp10),
        "strict_thresholds": [136000, 16000],
        "recurrence_increments_after_constant": 64,
        "per_process_CS_failure": rational(per_process),
        "two_stream_total_failure": rational(ALPHA),
        "lambda_count": 17,
        "sign_lambda_processes_per_stream": 34,
        "u0": rational(zero),
        "near_one_V_slope": rational(near_slope),
        "Bernoulli_histories_or_seeded_traces_or_sqrt_QA": 0,
        ("proof_basis"): (
            "Howard Theorem4 and Lemma1; conservative finite linear "
            "union; Maurer-Pontil Theorem4 fixed-cap fallback"
        ),
        "actual_financial_observations_or_IID_proof": False,
    }


def finance_parameters(frozen, started):
    finance = pinned_json(
        (
            "results/limitation_program_20261001/E12_continuation_20"
            "261004_screen_run001/finance_admission.json"
        ),
        frozen,
        started,
    )
    strings = {
        key: finance[key]
        for key in ("support_squared_lower", "support_squared_upper", "target_dollars_squared")
    }
    for value in strings.values():
        require(
            type(value) is str and re.fullmatch(r"[0-9]+\.[0-9]+", value),
            "Exact retained positive finite decimal string",
        )
    low, high, target = (
        Fraction(strings[key])
        for key in ("support_squared_lower", "support_squared_upper", "target_dollars_squared")
    )
    require(
        0 < low <= high and 0 < target < low,
        "Positive ordered copied support enclosure and fixed target",
    )
    return low, high, target, strings


def ideal_support_enclosure_check(low, high, started):
    """Independent fixed alternating theorem; no decimal or exponential library."""
    argument = Fraction(3, 100)
    term = upper = Fraction(1)
    for k in range(1, 65):
        guard(started)
        require(0 < argument / k < 1, "Strictly decreasing alternating term magnitudes")
        term *= -argument / k
        upper += term
    require(term > 0, "Even64 partial sum is the alternating upper bound")
    require(0 < argument / 65 < 1, "Fixed next65 term remains strictly decreasing")
    next_term = term * (-argument / 65)
    require(next_term < 0, "Odd65 partial sum is the alternating lower bound")
    lower = upper + next_term
    exact_low, exact_high = 10000 * lower, 10000 * upper
    require(
        low <= exact_low <= exact_high <= high and exact_low > 0,
        "Copied ideal-support endpoints contain independent fixed alternating enclosure",
    )
    return {
        "passed": True,
        "expression": "10000*exp(-3/100)",
        "exact_lower_partial_k0_through65": rational(exact_low),
        "exact_upper_partial_k0_through64": rational(exact_high),
        "copied_lower_contains_exact_lower": True,
        "copied_upper_contains_exact_upper": True,
        "fixed_terms_retuned_or_support_strings_replaced": False,
        ("proof"): (
            "Alternating series with positive strictly decreasing ma"
            "gnitudes tending to zero; even64 upper, next odd65 lowe"
            "r"
        ),
        "actual_digital_residual_law_or_support_proved": False,
    }


def floor_decision(low, high, target):
    if low > target:
        return "FIXED_CHANNEL_REJECTED_BEFORE_ACQUISITION"
    if high <= target:
        return "NECESSARY_ZERO_FLOOR_GATE_CLEARS_ONLY"
    return "SUPPORT_ENCLOSURE_COMPARISON_UNRESOLVED"


def static_screen(low, high, target, started):
    rows = []
    u0 = min(Fraction(CS_LOG_MAJORANT, 1) / lam for lam in LAMBDAS)
    for n in LOOKS:
        guard(started, admission=True)
        cs_low, cs_high = low * u0 / n, high * u0 / n
        fallback_low = low * Fraction(70, 3) / (n - 1)
        fallback_high = high * Fraction(70, 3) / (n - 1)
        rows.append(
            {
                "n": n,
                "CS_floor_lower": rational(cs_low),
                "CS_floor_upper": rational(cs_high),
                "CS_zero_floor_decision": floor_decision(cs_low, cs_high, target),
                "fallback_floor_lower": rational(fallback_low),
                "fallback_floor_upper": rational(fallback_high),
                "fallback_zero_floor_decision": floor_decision(fallback_low, fallback_high, target),
                "fallback_is_allowed_delivery_look": n == N_CAP,
                (
                    "intermediate_fallback_rows_are_static_diagnostics_not_optional_stopping_bounds"
                ): True,
                "necessary_screen_is_actual_delivery": False,
            }
        )
    require(
        len(rows) == 20 and rows[-1]["n"] == N_CAP, "All20 fixed looks retained without samples"
    )
    cs = rows[-1]["CS_zero_floor_decision"]
    fallback = rows[-1]["fallback_zero_floor_decision"]
    if cs == fallback == "FIXED_CHANNEL_REJECTED_BEFORE_ACQUISITION":
        decision = "FIXED_CANDIDATE_REJECTED_BEFORE_ACQUISITION"
    elif "NECESSARY_ZERO_FLOOR_GATE_CLEARS_ONLY" in (cs, fallback):
        decision = "NECESSARY_GATE_CLEARS_FINANCE_STILL_UNAUTHORIZED"
    else:
        decision = "SUPPORT_ENCLOSURE_COMPARISON_UNRESOLVED_FINANCE_UNAUTHORIZED"
    return {
        "schema": "e12-near-one-lambda-zero-floor-screen-v1",
        "rows": rows,
        "CS_cap_decision": cs,
        "fallback_cap_decision": fallback,
        "decision": decision,
        "minimal_CS_endpoint_proof": "S,V>=0; each branch intercept>=64/5; n<=cap",
        "minimal_fallback_endpoint_proof": "S,v_sample>=0; fallback assessed only at fixed cap",
        "all_zero_financial_dataset_observed_or_claimed": False,
        "screen_clearance_proves_financial_delivery_or_source_premises": False,
    }


def branch_frontiers(high, target, started):
    rows = []
    for n in LOOKS:
        for lam in LAMBDAS:
            guard(started, admission=True)
            intercept = Fraction(CS_LOG_MAJORANT, 1) / lam
            slope = lam / (2 * (1 - lam))
            constant = (n * target / high - intercept) / slope
            s_coefficient = -1 / slope
            rows.append(
                {
                    "n": n,
                    "lambda": rational(lam),
                    "normalized_boundary_intercept": rational(intercept),
                    "normalized_boundary_V_slope": rational(slope),
                    "V_threshold": {
                        "constant": rational(constant),
                        "S_coefficient": rational(s_coefficient),
                        "formula": "constant+S_coefficient*S",
                    },
                    "S_retained_symbolically": True,
                    "requires_nonnegative_right_side_and_sound_S_V": True,
                    "conservative_support_endpoint": "B2_upper",
                    "sufficient_future_branch_test": "S+intercept+V_slope*V<=n*T/B2_upper",
                    "actual_S_or_V_observed": False,
                }
            )
    require(len(rows) == 340, "All20*17 fixed prospective branch frontiers retained")
    return {
        "schema": "e12-near-one-lambda-fixed-branch-frontiers-v1",
        "rows": rows,
        "full_grid_test": "V<=max_lambda(constant+S_coefficient*S), with nonnegative RHS",
        "admissible_statistics": "S^2/n<=V<=S<=n",
        "one_branch_fails_does_not_reject_full_grid": True,
        "empirical_S_omitted_or_replaced_by_zero": False,
        "actual_positive_data_delivery_or_acquisition_authorized": False,
    }


def prepare(args, started):
    global _ATTEMPT_ROUTE_OWNED
    invocation_check(started)
    require(not OUTPUT.exists(), "Never reuse a receipt route")
    frozen = root_release(args.root_ready_sha256, started)
    runtime, runtime_bytes = runtime_packet(started)
    require(
        str(LAUNCHER) in runtime and str(BASE / "python.exe") in runtime,
        "Both interpreters in runtime packet",
    )
    loaded_runtime_check(runtime, started)
    guard(started, admission=True)
    OUTPUT.mkdir(parents=False, exist_ok=False)
    _ATTEMPT_ROUTE_OWNED = True
    write_json(OUTPUT / "protocol.json", protocol_value(frozen, runtime, runtime_bytes), started)
    protocol_sha256 = hashlib.sha256(stable_read(OUTPUT / "protocol.json", started)).hexdigest()
    terminal = rehash(frozen, runtime, started, protocol_sha256)
    guard(started)
    print(
        json.dumps(
            {
                "prepare_passed": True,
                "scientific_evaluation": False,
                "protocol": relative(OUTPUT / "protocol.json"),
                "protocol_sha256": protocol_sha256,
                "prepare_terminal_full_verification": terminal,
                "frozen_inputs": len(frozen),
                "runtime_inputs": len(runtime),
                "observed_CPU": time.process_time(),
                "observed_wall": time.monotonic() - started,
            }
        ),
        flush=True,
    )


def seal(protocol, frozen, runtime, started, passed, error, before, after, protocol_expected):
    observed = guard(started)
    require(
        passed is True and error is None and (after is not None),
        "Only one successful complete terminal may be sealed",
    )
    require(
        {path.name for path in OUTPUT.iterdir()}
        == {
            "protocol.json",
            "run_started.json",
            "checks.json",
            "screen.json",
            "frontiers.json",
            "summary.json",
            "verification.json",
        },
        "Exact complete success artifacts; no failure marker, prior manifest or extra member",
    )
    owned, byte_count = ({}, 0)
    for path in sorted(OUTPUT.iterdir(), key=str):
        require(path.is_file() and path.name != "manifest.json", "Finite declared output set")
        data = stable_read(path, started)
        byte_count += len(data)
        owned[relative(path)] = hashlib.sha256(data).hexdigest()
    require(
        owned[relative(OUTPUT / "protocol.json")] == protocol_expected,
        "Original expected prepared protocol retained at terminal sealing",
    )
    manifest = {
        "schema": "e12-near-one-lambda-static-screen-manifest-v1",
        "passed": passed,
        "completed": passed,
        "budget_censored": bool(error and "budget" in error.lower()),
        "error": error,
        "owned_files": owned,
        "frozen_inputs": frozen,
        "external_runtime_inputs": runtime,
        "fresh_before": before,
        "fresh_after": after,
        "observed_CPU": observed[0],
        "observed_wall": observed[1],
        "scope": protocol["scope"],
        "financial_adoption_approved": False,
        "manifest_self_hash_excluded": True,
        "manifest_inclusive_owned_file_count": len(owned) + 1,
        "owned_nonmanifest_bytes": byte_count,
        "manifest_inclusive_retention_checked_before_sealing": True,
        "prepared_protocol_SHA256": owned[relative(OUTPUT / "protocol.json")],
    }
    size = 1
    for fragment in json.JSONEncoder(indent=2, sort_keys=True, allow_nan=False).iterencode(
        manifest
    ):
        guard(started)
        size += len(fragment.encode("utf-8"))
    require(
        len(owned) + 1 <= MAX_OWNED_FILES and byte_count + size <= MAX_OWNED_BYTES,
        "Manifest-inclusive owned file and byte caps",
    )
    write_json(OUTPUT / "manifest.json", manifest, started)
    actual = list(OUTPUT.iterdir())
    require(
        {relative(path) for path in actual} == set(owned) | {relative(OUTPUT / "manifest.json")}
        and len(actual) == len(owned) + 1 <= MAX_OWNED_FILES,
        "Exact complete final owned membership including manifest",
    )
    actual_bytes = 0
    for path in actual:
        guard(started)
        require(
            path.is_file() and path.resolve(strict=True) == path, "Final owned path confinement"
        )
        actual_bytes += path.stat().st_size
    require(
        (OUTPUT / "manifest.json").stat().st_size == size
        and actual_bytes == byte_count + size <= MAX_OWNED_BYTES,
        "Exact complete final owned bytes including manifest",
    )
    guard(started)


def run(args, started):
    global _ATTEMPT_ROUTE_OWNED
    require(
        OUTPUT.is_dir() and set(p.name for p in OUTPUT.iterdir()) == {"protocol.json"},
        "Fresh prepared route only",
    )
    _ATTEMPT_ROUTE_OWNED = True
    invocation_check(started)
    protocol = json.loads(checked_read(OUTPUT / "protocol.json", args.protocol_sha256, started))
    frozen = root_release(args.root_ready_sha256, started)
    require(
        protocol.get("schema") == "e12-near-one-lambda-static-screen-protocol-v1",
        "Frozen new prospective static protocol",
    )
    require(
        protocol.get("frozen_inputs") == frozen, "Exact ROOT-frozen16-member source/history packet"
    )
    runtime = protocol["external_runtime_inputs"]
    fresh_runtime, runtime_bytes = runtime_packet(started)
    require(
        fresh_runtime == runtime and runtime_bytes == protocol["external_runtime_bytes"],
        "Complete current runtime membership and hashes unchanged",
    )
    loaded_runtime_check(runtime, started)
    require(
        protocol == protocol_value(frozen, runtime, runtime_bytes),
        "Every fixed field and prepared loaded-cache absence unchanged",
    )
    before = rehash(frozen, runtime, started, args.protocol_sha256)
    guard(started, admission=True)
    write_json(
        OUTPUT / "run_started.json",
        {
            "PID": os.getpid(),
            "protocol_expected_SHA256": args.protocol_sha256,
            "root_ready_expected_SHA256": args.root_ready_sha256,
            "observed_CPU": time.process_time(),
            "observed_wall": time.monotonic() - started,
            "static_bound_evaluation_started": False,
            "scope": protocol["scope"],
        },
        started,
    )
    checks = exact_static_checks(started)
    low, high, target, strings = finance_parameters(frozen, started)
    checks["ideal_support_enclosure"] = ideal_support_enclosure_check(low, high, started)
    screen = static_screen(low, high, target, started)
    frontiers = branch_frontiers(high, target, started)
    write_json(OUTPUT / "checks.json", checks, started)
    write_json(OUTPUT / "screen.json", screen, started)
    write_json(OUTPUT / "frontiers.json", frontiers, started)
    summary = {
        "schema": "e12-near-one-lambda-static-screen-summary-v1",
        "passed": True,
        "exact_static_screen_complete": True,
        "case": "C4",
        "compound_strike": 6,
        "copied_finance_strings": strings,
        "sample_cap": N_CAP,
        "looks_completed": 20,
        "branch_frontiers_completed": 340,
        "decision": screen["decision"],
        "CS_cap_decision": screen["CS_cap_decision"],
        "fallback_cap_decision": screen["fallback_cap_decision"],
        "historical_rejection_changed": False,
        "zero_floor_clearance_is_financial_delivery": False,
        "scope": protocol["scope"],
        "missing_finance_premises": [
            "Same-law IID outer/group observations and independent fixed policy",
            "Original residual support and certified finite evaluator/normalization/statistics",
            "Both instantiated moment streams and complete price failure allocation",
            (
                "Charged full acquisition-plus-estimation and matched fi"
                "xed-N/analytic/support comparator"
            ),
        ],
    }
    write_json(OUTPUT / "summary.json", summary, started)
    after = rehash(frozen, runtime, started, args.protocol_sha256)
    write_json(
        OUTPUT / "verification.json",
        {
            "passed": True,
            "before": before,
            "after": after,
            "expected_hash_waivers": 0,
            "fixture_credit": 0,
            "finance_execution": False,
            ("historical_scope"): (
                "Selected direct historical bytes and literal equal-SHA "
                "membership; not recursive current validation of old run"
                "time/dependency maps"
            ),
        },
        started,
    )
    seal(protocol, frozen, runtime, started, True, None, before, after, args.protocol_sha256)
    print(
        json.dumps(
            {
                "passed": True,
                "exact_static_screen_complete": True,
                "decision": screen["decision"],
                "manifest": relative(OUTPUT / "manifest.json"),
                "financial_acquisition_approved": False,
                "financial_adoption_approved": False,
                "fixture_credit": 0,
                "observed_CPU": time.process_time(),
                "observed_wall": time.monotonic() - started,
            }
        ),
        flush=True,
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
