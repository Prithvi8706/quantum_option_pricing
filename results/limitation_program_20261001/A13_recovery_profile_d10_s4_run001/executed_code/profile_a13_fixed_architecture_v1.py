"""AUTHOR-ONLY fixed d10_s4 profile; no audit, refit, approval or registration.

The immutable V4 verifier is loaded only after complete old-byte admission.
Its original guard remains intact and is called first by a stricter wrapper.
Root must freeze this NEW source, method pair and external READY before launch.
"""

from __future__ import annotations

import argparse
import cProfile
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
from importlib import metadata
from importlib.util import cache_from_source, module_from_spec, spec_from_file_location
import json
import os
from pathlib import Path
import re
import site
import sys
import time
import traceback


ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
AUTHOR = RESEARCH / "profile_a13_fixed_architecture_v1.py"
METHOD = RESEARCH / "a13_fixed_architecture_profile_preflight.json"
METHOD_DOC = RESEARCH / "A13_FIXED_ARCHITECTURE_PROFILE_PREFLIGHT.md"
OUTPUT = PROGRAM / "A13_recovery_profile_d10_s4_run001"
READY = PROGRAM / "A13_fixed_architecture_profile_ROOT_READY_run001.json"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
VERIFIER = RESEARCH / "audit_exp_frontier_recovery_v4.py"
VERIFIER_SHA = "61c05812abd7c7c042ab654a025e14b96afcfff00afd5398e72ea334307d07ba"
FAILED = PROGRAM / "A13_recovery_audit_run004"
FAILED_SHA = "334aa0386e0321b7fb9690a52378a8c94234b5c0488fa50464d89d076ca20471"
REVIEW = PROGRAM / "A13_recovery_root_review_run004"
REVIEW_SHA = "c427b46bf39133fddbccc2d9022d14d8756545885f7a4279e788a3fbc04dec1a"
SOURCE_SHA = "e3c23aaa0697727952a7c979503424146c0224e8b2c8c32cff652974ab557dc9"
MODULE = "research.limitation_program_20261001.audit_exp_frontier_recovery_v4"
CPU, ADMISSION, WALL = 180, 150, 600
MAX_REFERENCES, MAX_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
MAX_OWNED, MAX_OWNED_BYTES = 24, 32 * 1024**2
MAX_PROFILE_FUNCTIONS, MAX_PROFILE_BYTES = 10000, 8 * 1024**2
SHA = re.compile(r"[0-9a-f]{64}\Z")
STARTED = None
BASE = BASE_SITE_LEXICAL = BASE_SITE = None
PATH_CACHE, HASH_CACHE, OBSERVED, EXPECTED = {}, {}, {}, {}
FROZEN, EXTERNAL = {}, {}
PHASES = []
REFERENCES = HASH_WORK = 0
ORIGINAL_FUNCTION_CODES = {}
ORIGINAL_SCIENTIFIC_CONSTANTS = None


class DiagnosticCensoredError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ValueError(message)


def creation_clock():
    require(os.name == "nt" and ctypes.sizeof(ctypes.c_void_p) == 8, "Pinned Win64")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.argtypes = []
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    values = [wintypes.FILETIME() for _ in range(4)]
    require(
        kernel.GetProcessTimes(kernel.GetCurrentProcess(), *(ctypes.byref(v) for v in values)),
        "Actual creation clock unavailable",
    )
    ticks = (values[0].dwHighDateTime << 32) | values[0].dwLowDateTime
    age = time.time_ns() - (ticks - 116444736000000000) * 100
    require(age >= 0, "Creation time precedes observation")
    return time.monotonic() - age / 1000000000


def check(*, admission=False):
    cpu, wall = time.process_time(), time.monotonic() - STARTED
    if cpu >= (ADMISSION if admission else CPU) or wall >= WALL:
        raise DiagnosticCensoredError("Fixed diagnostic CPU/wall censor")
    return cpu, wall


def observation():
    return {"process_CPU_seconds": time.process_time(), "wall_seconds": time.monotonic() - STARTED}


def phase(name, began):
    check()
    after = observation()
    PHASES.append(
        {
            "phase": name,
            "before": began,
            "after": after,
            "process_CPU_seconds": after["process_CPU_seconds"] - began["process_CPU_seconds"],
            "wall_seconds": after["wall_seconds"] - began["wall_seconds"],
        }
    )


def fingerprint(path):
    data = path.stat()
    return (
        data.st_dev,
        data.st_ino,
        data.st_size,
        data.st_mtime_ns,
        data.st_ctime_ns,
        data.st_mode,
        getattr(data, "st_file_attributes", None),
        getattr(data, "st_reparse_tag", None),
    )


def permitted(path):
    return path.is_relative_to(ROOT) or (
        BASE is not None
        and not path.is_relative_to(BASE_SITE)
        and (path.parent == BASE or any(path.is_relative_to(BASE / d) for d in ("Lib", "DLLs")))
    )


def actual_path(path, *, fresh=False):
    check()
    lexical = Path(path).absolute()
    require(not lexical.is_relative_to(BASE_SITE_LEXICAL), "Excluded lexical base site-packages")
    key = str(lexical)
    if not fresh and key in PATH_CACHE:
        saved, identity = PATH_CACHE[key]
        if fingerprint(lexical) == identity and fingerprint(saved) == identity:
            return saved
    actual = lexical.resolve(strict=True)
    require(permitted(actual) and actual.is_file(), "Confined actual regular file")
    require(actual == lexical, "Canonical exact physical path; aliases are not admitted")
    identity = fingerprint(actual)
    require(key not in PATH_CACHE or PATH_CACHE[key][0] == actual, "Path identity redirected")
    PATH_CACHE[key] = (actual, identity)
    check()
    return actual


def digest(path, *, fresh=False):
    global HASH_WORK
    actual = actual_path(path, fresh=fresh)
    identity = fingerprint(actual)
    if not fresh and str(actual) in HASH_CACHE and HASH_CACHE[str(actual)][0] == identity:
        return HASH_CACHE[str(actual)][1]
    state = hashlib.sha256()
    with actual.open("rb") as stream:
        while block := stream.read(1 << 20):
            check()
            HASH_WORK += len(block)
            require(HASH_WORK <= MAX_HASH_WORK, "Finite actual SHA work")
            state.update(block)
            check()
    require(fingerprint(actual) == identity, "Actual bytes changed during hash")
    value = state.hexdigest()
    require(str(actual) not in OBSERVED or OBSERVED[str(actual)] == value, "Observed SHA changed")
    OBSERVED[str(actual)] = value
    HASH_CACHE[str(actual)] = (identity, value)
    check()
    return value


def bind(path, expected):
    global REFERENCES
    check()
    REFERENCES += 1
    require(REFERENCES <= MAX_REFERENCES, "Finite map reference count")
    require(type(expected) is str and SHA.fullmatch(expected), "Canonical SHA256")
    actual = actual_path(path)
    require(str(actual) not in EXPECTED or EXPECTED[str(actual)] == expected, "Equal-SHA union")
    require(digest(actual) == expected, "Actual expected SHA mismatch: " + str(actual))
    EXPECTED[str(actual)] = expected
    mapping = FROZEN if actual.is_relative_to(ROOT) else EXTERNAL
    key = actual.relative_to(ROOT).as_posix() if actual.is_relative_to(ROOT) else str(actual)
    require(key not in mapping or mapping[key] == expected, "Conflicting canonical input")
    mapping[key] = expected
    return actual


def read_json(path):
    global HASH_WORK
    check()
    actual = actual_path(path)
    identity = fingerprint(actual)
    require(identity[2] <= 128 * 1024**2, "Finite JSON input")
    pieces, total = [], 0
    with actual.open("rb") as stream:
        while block := stream.read(1 << 20):
            check()
            total += len(block)
            require(total <= identity[2], "Input grew")
            pieces.append(block)
    require(total == identity[2] and fingerprint(actual) == identity, "Stable complete JSON bytes")
    data = b"".join(pieces)
    check()
    state = hashlib.sha256()
    for offset in range(0, len(data), 1 << 20):
        check()
        block = data[offset : offset + (1 << 20)]
        HASH_WORK += len(block)
        require(HASH_WORK <= MAX_HASH_WORK, "Finite input read/hash work")
        state.update(block)
    value = state.hexdigest()
    require(value == digest(actual), "Read bytes equal independently observed source")
    result = json.loads(data)
    check()
    return result


def write_json(path, value, *, max_bytes=MAX_OWNED_BYTES):
    check()
    data = (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    check()
    require(len(data) <= max_bytes, "Finite JSON retention")
    with path.open("xb") as stream:
        for offset in range(0, len(data), 65536):
            check()
            stream.write(data[offset : offset + 65536])
            check()


def inventory(receipt, *, include_manifest=False):
    files = set()
    for path in receipt.rglob("*"):
        check()
        if path.is_file():
            actual = actual_path(path)
            require(actual.is_relative_to(receipt), "Owned inventory confinement")
            require(actual not in files, "No duplicate owned path")
            if include_manifest or actual != receipt / "manifest.json":
                files.add(actual)
    return files


def packet(receipt, expected, counts):
    manifest_path = bind(receipt / "manifest.json", expected)
    manifest = read_json(manifest_path)
    require(manifest.get("manifest_self_hash_excluded") is True, "Exact self-hash convention")
    require(not (receipt / "FAILED_UNSEALED.json").exists(), "Sealed premise has no override")
    fields = ("files", "frozen_inputs", "external_runtime_inputs")
    require(
        [len(manifest.get(field, {})) for field in fields] == list(counts),
        "Complete declared original maps",
    )
    owned = set()
    for field in fields:
        mapping = manifest.get(field, {})
        require(type(mapping) is dict, "Exact map object")
        for key, value in mapping.items():
            check()
            require(type(key) is str, "Literal map path")
            if field == "files":
                require(
                    not Path(key).is_absolute() and "\\" not in key,
                    "Canonical ROOT-relative or receipt-relative owned key",
                )
                root_owned = key.startswith(receipt.relative_to(ROOT).as_posix() + "/")
                path = ROOT / key if root_owned else receipt / key
            elif field == "frozen_inputs":
                require(not Path(key).is_absolute() and "\\" not in key, "ROOT-relative frozen key")
                path = ROOT / key
            else:
                require(Path(key).is_absolute(), "Absolute scoped external runtime key")
                path = Path(key)
            actual = bind(path, value)
            if field == "files":
                require(actual.is_relative_to(receipt), "Owned key remains in original receipt")
                canonical_key = actual.relative_to(ROOT if root_owned else receipt).as_posix()
                require(canonical_key == key, "Canonical original owned map spelling")
                require(actual not in owned, "Unique actual owned member")
                owned.add(actual)
            elif field == "frozen_inputs":
                require(actual.is_relative_to(ROOT), "ROOT map confinement")
                require(actual.relative_to(ROOT).as_posix() == key, "Canonical ROOT input key")
            else:
                require(
                    not actual.is_relative_to(ROOT) and str(actual) == key, "External map scope"
                )
    require(inventory(receipt) == owned, "Exact actual prior-owned inventory")
    return manifest


def fresh_union():
    check()
    union = dict(OBSERVED)
    for key, value in EXPECTED.items():
        require(key not in union or union[key] == value, "Fresh equal-SHA union")
        union[key] = value
    total = 0
    for key, value in sorted(union.items()):
        check()
        actual = actual_path(key, fresh=True)
        total += actual.stat().st_size
        require(total <= MAX_BYTES, "Finite distinct input bytes")
        require(digest(actual, fresh=True) == value, "Full fresh byte verification")
    return {"unique_paths": len(union), "unique_bytes": total, "SHA_mismatches": 0}


def setup():
    global BASE, BASE_SITE_LEXICAL, BASE_SITE
    require(Path.cwd().resolve() == ROOT and Path(__file__).resolve() == AUTHOR, "Exact cwd/driver")
    require(Path(sys.executable).resolve() == LAUNCHER, "Pinned interpreter")
    require(Path(sys.prefix).resolve() == ROOT / ".context/frontier_t0_env", "Pinned venv")
    require(
        sys.dont_write_bytecode is True and site.ENABLE_USER_SITE is False,
        "Startup -B/no user site",
    )
    for name in ("PYTHONPATH", "PYTHONHOME", "SAGE_ROOT", "MPMATH_SAGE"):
        require(not os.environ.get(name), "No inherited runtime override: " + name)
    os.environ["MPMATH_NOGMPY"] = os.environ["MPMATH_NOSAGE"] = "1"
    BASE = Path(sys.base_prefix).resolve(strict=True)
    BASE_SITE_LEXICAL = BASE / "Lib/site-packages"
    BASE_SITE = BASE_SITE_LEXICAL.resolve()
    check()


def admission(ready_sha):
    bind(READY, ready_sha)
    ready = read_json(READY)
    require(
        ready["schema"] == "root-a13-fixed-architecture-profile-READY-v1"
        and ready["ready"] is True
        and ready["root_and_independent_static_reviews_passed"] is True,
        "Actual root-issued reviewed READY",
    )
    require(ready["CPU_admission_wall_seconds"] == [CPU, ADMISSION, WALL], "Diagnostic clocks")
    require(
        ready["fixed_architecture"] == {"degree": 10, "segments": 4, "row_id": "d10_s4"},
        "One fixed architecture",
    )
    require(ready["output"] == OUTPUT.relative_to(ROOT).as_posix(), "Fresh fixed route")
    require(ready["interpreter"] == str(LAUNCHER), "Absolute pinned launcher")
    require(
        ready["argv_prefix"]
        == [
            "-B",
            "-m",
            "research.limitation_program_20261001.profile_a13_fixed_architecture_v1",
            "--ready-sha256",
        ],
        "Exact startup -B before module and external READY pin argument",
    )
    authors = ready["author_method_SHA256"]
    require(
        type(authors) is dict and set(authors) == {p.name for p in (AUTHOR, METHOD, METHOD_DOC)},
        "Exactly three new pins",
    )
    for name, expected in authors.items():
        bind(RESEARCH / name, expected)
    method = read_json(METHOD)
    require(method["schema"] == "a13-fixed-architecture-profile-preflight-v1", "Exact method")
    require(
        method["driver_SHA256"] == authors[AUTHOR.name],
        "Final actual driver pin agrees with external ROOT_READY",
    )
    require(method["CPU_admission_wall_seconds"] == [CPU, ADMISSION, WALL], "Unchanged new clocks")
    require(method["verifier_SHA256"] == VERIFIER_SHA, "Frozen actual V4")
    require(method["prior_failed_audit004"]["manifest_SHA256"] == FAILED_SHA, "Failed004 pin")
    require(method["prior_root_review004"]["manifest_SHA256"] == REVIEW_SHA, "Release004 pin")
    require(method["fixed_architecture"] == ready["fixed_architecture"], "Fixed row equality")
    require(method["frozen_original_verifier_limits"] == [300, 270, 900], "Original guards")
    require(
        method["new_test_credit"] == method["new_gate_replays"] == method["new_price_samples"] == 0
        and method["row_approval"] is method["all20_approval"] is method["candidate_G2"] is False,
        "Zero scientific approval and credit",
    )
    bind(VERIFIER, VERIFIER_SHA)
    failed = packet(FAILED, FAILED_SHA, (38, 1030, 2842))
    require(
        failed["schema"] == "a13-exp-frontier-recovery-independent-audit-manifest-v1"
        and failed["completed"] is failed["passed"] is False
        and failed["budget_censored"] is True,
        "Actual004 remains failed/censored",
    )
    outcome, failure = (
        read_json(FAILED / "completion_outcome.json"),
        read_json(FAILED / "failure.json"),
    )
    require(
        outcome["completed"] is outcome["passed"] is False
        and outcome["failed"] is outcome["budget_censored"] is True
        and outcome["new_test_credit"] == 0
        and outcome["limits_CPU_admission_wall"] == [300, 270, 900]
        and failure["failed"] is True
        and failure["error_type"] == "BudgetCensoredError",
        "Authoritative failure retained",
    )
    rows = {name for name in failed["files"] if name.startswith("rows/")}
    grid = [(d, s) for d in (4, 6, 8, 10, 12) for s in (1, 2, 4, 8)]
    require(rows == {f"rows/d{d}_s{s}.json.gz" for d, s in grid[:14]}, "Exactly fourteen partials")
    require(
        not (FAILED / "summary.json").exists()
        and not (FAILED / "fixed_inventory_authorization.json").exists(),
        "No old all20 authority",
    )
    packet(REVIEW, REVIEW_SHA, (1, 37, 0))
    cache_pins = ready["existing_driver_cache_SHA256"]
    own_cache = Path(cache_from_source(str(AUTHOR)))
    require(type(cache_pins) is dict, "Explicit prospective driver cache pin map")
    require(
        set(cache_pins)
        == ({own_cache.relative_to(ROOT).as_posix()} if own_cache.exists() else set()),
        "Exact existing driver-cache membership",
    )
    for key, expected in cache_pins.items():
        bind(ROOT / key, expected)
    verifier_cache = Path(cache_from_source(str(VERIFIER)))
    if verifier_cache.exists():
        require(
            str(actual_path(verifier_cache)) in EXPECTED,
            "Existing frozen verifier cache must already have an old expected binding",
        )
    runtime_before_import(read_json(FAILED / "interpreter.json"))
    fresh_union()
    check(admission=True)
    return ready


def loaded_bootstrap():
    for name, module in tuple(sys.modules.items()):
        check()
        if module is None:
            continue
        for value in (getattr(module, "__file__", None), getattr(module, "__cached__", None)):
            if value:
                path = Path(value).absolute()
                require(
                    not path.is_relative_to(BASE_SITE_LEXICAL), "Excluded bootstrap lexical origin"
                )
                require(
                    not path.resolve().is_relative_to(BASE_SITE),
                    "Excluded bootstrap resolved origin",
                )
                if path.is_file():
                    actual = actual_path(path)
                    require(str(actual) in EXPECTED, "Unbound bootstrap source/cache: " + name)
                    require(
                        digest(actual) == EXPECTED[str(actual)], "Bootstrap bytes match admission"
                    )


def runtime_before_import(record):
    """Check original complete runtime membership before loading any helper."""
    require(record["python_version"] == sys.version, "Actual recorded Python version")
    require(record["sys_path"] == list(sys.path), "Unchanged original import search path")
    require(record["executable"] == str(LAUNCHER), "Original launcher matches actual driver")
    require(record["base_prefix"] == str(BASE), "Original base runtime scope")
    require(
        record["mpmath_version"] == metadata.version("mpmath") == "1.3.0", "Pinned package metadata"
    )
    require(record["base_site_packages_import_rejected"] is True, "Unreachable base package scope")
    for route in record["absent_standard_runtime_paths"]:
        check()
        require(not Path(route).exists(), "An absent interpreter zip appeared")
    found = set()
    for route in record["runtime_inventory"]["roots"]:
        check()
        root = Path(route).absolute()
        require(not root.is_relative_to(BASE_SITE_LEXICAL), "Excluded runtime lexical root")
        require(
            not root.resolve(strict=True).is_relative_to(BASE_SITE),
            "Excluded runtime physical root",
        )
        if root.is_file():
            found.add(actual_path(root))
        else:
            require(root.is_dir(), "Existing original runtime tree")
            for directory, dirs, files in os.walk(root, topdown=True, followlinks=False):
                check()
                current = Path(directory)
                require(current.resolve(strict=True) == current, "No runtime directory alias")
                dirs[:] = [name for name in dirs if current / name != BASE_SITE_LEXICAL]
                for name in dirs:
                    check()
                    candidate = current / name
                    require(
                        candidate.resolve(strict=True) == candidate, "No runtime subdirectory alias"
                    )
                for name in files:
                    check()
                    found.add(actual_path(current / name))
                    require(len(found) <= 24000, "Existing runtime file cap")
    total = 0
    for path in found:
        check()
        require(str(path) in EXPECTED, "Every original runtime byte has an immutable expected hash")
        total += path.stat().st_size
        require(total <= 2 * 1024**3, "Existing runtime byte cap")
    require(
        sorted(str(path) for path in found) == record["runtime_inventory"]["actual_file_paths"],
        "Exact original runtime inventory unchanged",
    )
    require(
        record["runtime_inventory"]["files"] == len(found)
        and record["runtime_inventory"]["bytes"] == total,
        "Original complete runtime counts",
    )


def load_verifier():
    global ORIGINAL_FUNCTION_CODES, ORIGINAL_SCIENTIFIC_CONSTANTS
    require(
        MODULE not in sys.modules and "mpmath" not in sys.modules, "No prior helper/science import"
    )
    loaded_bootstrap()
    require(digest(VERIFIER, fresh=True) == VERIFIER_SHA, "Fresh import source SHA")
    spec = spec_from_file_location(MODULE, VERIFIER)
    require(spec is not None and spec.loader is not None, "Exact frozen helper loader")
    verifier = module_from_spec(spec)
    sys.modules[MODULE] = verifier
    spec.loader.exec_module(verifier)
    original_check = verifier.check
    original_code = original_check.__code__
    ORIGINAL_FUNCTION_CODES = {
        name: value.__code__
        for name, value in verifier.__dict__.items()
        if callable(value)
        and hasattr(value, "__code__")
        and getattr(value, "__module__", None) == MODULE
    }
    ORIGINAL_SCIENTIFIC_CONSTANTS = scientific_constants(verifier)

    def stricter_check(started, *, admission=False):
        require(started == STARTED, "Same creation wall clock; never reset")
        result = original_check(started, admission=admission)
        check(admission=admission)
        return result

    # Explicit sole rebinding: preserve and call the unmodified original first.
    verifier.check = stricter_check
    verifier.initialize(STARTED)
    verify_guard(verifier, original_check, original_code, stricter_check)
    return verifier, original_check, original_code, stricter_check


def verify_guard(verifier, original, code, wrapper):
    require(
        verifier.check is wrapper and original.__code__ is code, "Original guard identity intact"
    )
    require(
        (verifier.CPU, verifier.ADMISSION, verifier.WALL, verifier.DIGITS) == (300, 270, 900, 130),
        "Frozen limits/precision unchanged",
    )
    require(
        verifier.AUTHOR == VERIFIER and verifier.OUTPUT == FAILED,
        "Original helper routes unchanged",
    )
    require(original.__globals__ is verifier.__dict__, "Original guard globals retained")
    for name, expected_code in ORIGINAL_FUNCTION_CODES.items():
        check()
        value = original if name == "check" else getattr(verifier, name)
        require(value.__code__ is expected_code, "Every frozen top-level function code retained")
    require(
        scientific_constants(verifier) == ORIGINAL_SCIENTIFIC_CONSTANTS,
        "Frozen scientific constants retained",
    )
    check()


def scientific_constants(verifier):
    values = {
        name: getattr(verifier, name)
        for name in (
            "W",
            "Q",
            "N",
            "CASES",
            "GRID",
            "EXPONENTS",
            "BASELINE",
            "RESOURCE_FIELDS",
            "DIGITS",
            "CPU",
            "ADMISSION",
            "WALL",
        )
    }
    values["EPS"] = [verifier.EPS.numerator, verifier.EPS.denominator]
    return json.dumps(
        values,
        sort_keys=True,
        separators=(",", ":"),
    )


def merge_verifier_maps(verifier, frozen, external):
    for mapping, parent in ((frozen, ROOT), (external, None)):
        for key, value in mapping.items():
            check()
            bind(parent / key if parent is not None else Path(key), value)
    for key, value in verifier.OBSERVED_HASHES.items():
        bind(Path(key), value)
    for key, (value, _) in PATH_CACHE.items():
        require(actual_path(key, fresh=True) == value, "Final physical alias identity")


def fixed_row(verifier):
    actual = verifier.read_json(verifier.MATERIAL / "rows/d10_s4.json", STARTED)
    fits = verifier.read_json(verifier.MATERIAL / "coefficient_fit_diagnostics.json", STARTED)
    certificates = verifier.read_json(
        verifier.MATERIAL / "exponential_approximation_certificate.json", STARTED
    )
    frontier = verifier.read_json(verifier.MATERIAL / "function_frontier.json", STARTED)
    identity = {"degree": 10, "segments": 4, "row_id": "d10_s4", "status": "CERTIFIED_ESTIMATE"}
    for key, value in identity.items():
        verifier.same(actual[key], value, "Fixed untrusted row identity")
    selected = []
    for aggregate in (fits, certificates, frontier):
        matches = [row for row in aggregate["rows"] if row["row_id"] == "d10_s4"]
        require(len(matches) == 1, "One actual fixed-row aggregate")
        for key, value in identity.items():
            verifier.same(matches[0][key], value, "Exact fixed aggregate identity")
        selected.append(matches[0])
    fit, certificate, resource = selected
    verifier.same(actual["fit"]["segment_fits"], fit["segment_fits"], "Same saved fit transcript")
    verifier.same(actual["certificate"], certificate["certificate"], "Same saved certificate")
    verifier.same(
        actual["resource_estimate"], resource["resource_estimate"], "Same saved resources"
    )
    require(len(fit["segment_fits"]) == 4, "No extra segment or architecture")
    return actual, fit


def function_key(code):
    if isinstance(code, str):
        return {"file": "~", "line": 0, "function": code, "builtin": True}
    return {
        "file": code.co_filename,
        "line": code.co_firstlineno,
        "function": code.co_name,
        "builtin": False,
    }


def profile_evidence(profiler):
    check()
    entries = profiler.getstats()
    require(len(entries) <= MAX_PROFILE_FUNCTIONS, "Finite actual cProfile function identities")
    records, edges = [], 0
    for entry in entries:
        check()
        key = function_key(entry.code)
        callers = []
        for call in entry.calls or ():
            check()
            edges += 1
            require(edges <= 100000, "Finite profile call-graph edges")
            callers.append(
                dict(
                    **function_key(call.code),
                    calls=call.callcount,
                    recursive_calls=call.reccallcount,
                    total_wall_seconds=call.inlinetime,
                    cumulative_wall_seconds=call.totaltime,
                )
            )
        records.append(
            dict(
                **key,
                calls=entry.callcount,
                recursive_calls=entry.reccallcount,
                primitive_calls=entry.callcount - entry.reccallcount,
                total_wall_seconds=entry.inlinetime,
                cumulative_wall_seconds=entry.totaltime,
                callees=sorted(callers, key=lambda r: (r["file"], r["line"], r["function"])),
            )
        )
    records.sort(key=lambda r: (-r["cumulative_wall_seconds"], r["file"], r["line"], r["function"]))
    check()
    return {
        "schema": "a13-fixed-architecture-cProfile-v1",
        "row_id": "d10_s4",
        "timer": "cProfile default wall timer",
        "profiling_overhead_included": True,
        "unprofiled_speedup_claim": False,
        "function_count": len(records),
        "call_graph_edges": edges,
        "all_function_records": records,
        "top50_cumulative_wall_seconds": records[:50],
        "row_approval": False,
        "all20_approval": False,
        "new_test_credit": 0,
    }


def scope_flags():
    return dict(
        new_test_credit=0,
        new_gate_replays=0,
        new_price_samples=0,
        diagnostic_not_independent_scientific_audit=True,
        row_approval=False,
        all20_approval=False,
        candidate_selection=False,
        gate_emission_authorized=False,
        candidate_G2=False,
        adoption=False,
        cost_transfer=False,
        quantum_advantage=False,
        prior_failed004_remains_failed=True,
        full_G2=False,
    )


def copy_sources():
    destination = OUTPUT / "executed_code"
    destination.mkdir(exist_ok=False)
    for source in (AUTHOR, METHOD, METHOD_DOC, VERIFIER, READY):
        check()
        expected = EXPECTED[str(actual_path(source))]
        target = destination / source.name
        with source.open("rb") as incoming, target.open("xb") as outgoing:
            while block := incoming.read(65536):
                check()
                outgoing.write(block)
                check()
        bind(target, expected)


def seal(outcome):
    check()
    require(
        not (OUTPUT / "manifest.json").exists() and not (OUTPUT / "FAILED_UNSEALED.json").exists(),
        "Exclusive diagnostic terminal",
    )
    verification = fresh_union()
    write_json(
        OUTPUT / "completion_outcome.json",
        dict(
            outcome,
            **scope_flags(),
            budget=observation(),
            limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
        ),
    )
    owned, total = {}, 0
    for path in sorted(inventory(OUTPUT)):
        check()
        total += path.stat().st_size
        require(
            len(owned) < MAX_OWNED and total <= MAX_OWNED_BYTES, "Finite owned diagnostic inventory"
        )
        owned[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
    manifest = dict(
        schema="a13-fixed-architecture-profile-manifest-v1",
        files=owned,
        frozen_inputs=FROZEN,
        external_runtime_inputs=EXTERNAL,
        manifest_self_hash_excluded=True,
        verification=verification,
        new_driver_hash_work_bytes=HASH_WORK,
        frozen_helper_internal_hash_work_not_in_driver_byte_counter=True,
        all_hashing_charged_to_stricter_process_CPU_wall=True,
        completed=outcome["completed"],
        passed=outcome["passed"],
        budget_censored=outcome["budget_censored"],
        terminal_outcome_file="completion_outcome.json",
        original_expected_hashes_waived=False,
        **scope_flags(),
    )
    write_json(OUTPUT / "manifest.json", manifest)
    check()


def fail(error, profiler, verifier_state):
    if not OUTPUT.exists():
        return
    try:
        check()
        if (OUTPUT / "manifest.json").exists():
            (OUTPUT / "manifest.json").rename(OUTPUT / "partial_manifest_not_terminal_success.json")
        if profiler is not None and not (OUTPUT / "profile.json").exists():
            write_json(
                OUTPUT / "profile.json", profile_evidence(profiler), max_bytes=MAX_PROFILE_BYTES
            )
        if verifier_state is not None:
            verifier, frozen, external = verifier_state
            merge_verifier_maps(verifier, frozen, external)
        write_json(
            OUTPUT / "failure.json",
            dict(
                failed=True,
                phase="fixed_architecture_profile",
                error_type=type(error).__name__,
                error=str(error),
                traceback=traceback.format_exc(),
                budget=observation(),
                **scope_flags(),
            ),
        )
        require(
            not (OUTPUT / "completion_outcome.json").exists(),
            "Partial terminal must remain unsealed",
        )
        seal(
            dict(
                completed=False,
                passed=False,
                failed=True,
                budget_censored=isinstance(error, DiagnosticCensoredError),
                failure_file="failure.json",
            )
        )
    except BaseException:
        try:
            with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
                stream.write(
                    b'{"failed":true,"completed":false,"passed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"partial_success_invalid":true,"new_test_credit":0,"row_approval":false,"all20_approval":false,"full_G2":false,"adoption":false,"fresh_version_required":true}\n'
                )
        except FileExistsError:
            pass


def main():
    global STARTED
    STARTED = creation_clock()
    parser = argparse.ArgumentParser(
        description="One frozen d10_s4 verification profile; zero scientific approval"
    )
    parser.add_argument("--ready-sha256", required=True)
    arguments = parser.parse_args()
    require(SHA.fullmatch(arguments.ready_sha256), "External root READY SHA required")
    profiler = state = None
    try:
        setup()
        require(not OUTPUT.exists(), "Fresh diagnostic only; no retries")
        began = observation()
        ready = admission(arguments.ready_sha256)
        loaded_bootstrap()
        phase("prior_failure_and_runtime_bytes_admission", began)
        check(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        copy_sources()
        write_json(
            OUTPUT / "run_started.json",
            dict(
                UTC=datetime.now(timezone.utc).isoformat(),
                PID=os.getpid(),
                READY_SHA256=arguments.ready_sha256,
                fixed_architecture=ready["fixed_architecture"],
                limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
                **scope_flags(),
            ),
        )
        began = observation()
        verifier, original, code, wrapper = load_verifier()
        frozen, external = dict(FROZEN), dict(EXTERNAL)
        state = (verifier, frozen, external)
        policy = verifier.implementation_policy(STARTED)
        method, origins, source = verifier.source_packet(policy, frozen, external, STARTED)
        require(source["manifest_sha256"] == SOURCE_SHA, "Same metadata-only source")
        interpreter = verifier.read_json(FAILED / "interpreter.json", STARTED)
        verifier.verify_runtime(interpreter, frozen, external, STARTED)
        verifier.loaded_origins(frozen, external, STARTED)
        verifier.verify_maps(frozen, external, STARTED)
        phase("frozen_helper_source_packet_and_runtime_admission", began)
        check(admission=True)
        require("mpmath" not in sys.modules, "Lazy science after complete byte admission")
        import mpmath as mp

        require(mp.__version__ == metadata.version("mpmath") == "1.3.0", "Pinned mpmath")
        require(sys.modules["mpmath.libmp.backend"].BACKEND == "python", "Pure-Python backend")
        mp.mp.dps = mp.iv.dps = 130
        verifier.loaded_origins(frozen, external, STARTED)
        began = observation()
        domain = verifier.typed_source_domain(STARTED)
        metadata_cases = verifier.original_native_metadata(frozen, STARTED)
        primary_domain = verifier.read_json(
            verifier.MATERIAL / "source_domain_binding.json", STARTED
        )
        verifier.reconcile_domain(primary_domain, domain, metadata_cases, STARTED)
        phase("original_source_domain_binding", began)
        began = observation()
        actual, fit = fixed_row(verifier)
        phase("one_fixed_saved_row_loading", began)
        verify_guard(verifier, original, code, wrapper)
        write_json(
            OUTPUT / "admission_and_guard.json",
            dict(
                frozen_verifier_SHA256=VERIFIER_SHA,
                frozen_failed004_manifest_SHA256=FAILED_SHA,
                original_guard_code_SHA256=hashlib.sha256(code.co_code).hexdigest(),
                original_limits_CPU_admission_wall=[300, 270, 900],
                stricter_limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
                original_guard_retained_and_called_first=True,
                only_guard_binding_strengthened=True,
                all_frozen_scientific_functions_and_constants_unchanged=True,
                complete_original_source_packet_admitted=True,
                prior_partials_not_approvals=True,
                all20_iterator_invoked=False,
                refit_invoked=False,
                **scope_flags(),
            ),
        )
        check(admission=True)
        profiler = cProfile.Profile()
        began = observation()
        profiler.enable()
        try:
            proof = verifier.audit_architecture(
                mp, actual["certificate"], fit["segment_fits"], 10, 4, domain, STARTED
            )
            del proof
            architecture_end = observation()
            cost = verifier.independent_resources(
                10, 4, fit["segment_fits"], primary_domain, metadata_cases, STARTED
            )
            verifier.same(
                actual["resource_estimate"], cost, "Unchanged strict fixed resource equality"
            )
            del cost
        finally:
            profiler.disable()
        phase("fixed_architecture_complete_profiled_call", began)
        PHASES.append({"phase": "architecture_return_boundary", "observation": architecture_end})
        verify_guard(verifier, original, code, wrapper)
        write_json(OUTPUT / "profile.json", profile_evidence(profiler), max_bytes=MAX_PROFILE_BYTES)
        verifier.verify_runtime(interpreter, frozen, external, STARTED)
        verifier.loaded_origins(frozen, external, STARTED)
        merge_verifier_maps(verifier, frozen, external)
        write_json(OUTPUT / "phase_observations.json", dict(phases=PHASES, **scope_flags()))
        write_json(
            OUTPUT / "summary.json",
            dict(
                schema="a13-fixed-architecture-profile-summary-v1",
                completed=True,
                passed=True,
                status="profile_retention_integrity_only",
                fixed_call_returned=True,
                fixed_architecture={"degree": 10, "segments": 4, "row_id": "d10_s4"},
                original_audit004_failed=True,
                profiling_overhead_included=True,
                unprofiled_speedup_or_budgetfit_claim=False,
                phases=PHASES,
                budget=observation(),
                **scope_flags(),
            ),
        )
        seal(dict(completed=True, passed=True, failed=False, budget_censored=False))
    except BaseException as error:
        if profiler is not None:
            profiler.disable()
        fail(error, profiler, state)
        raise


if __name__ == "__main__":
    main()
