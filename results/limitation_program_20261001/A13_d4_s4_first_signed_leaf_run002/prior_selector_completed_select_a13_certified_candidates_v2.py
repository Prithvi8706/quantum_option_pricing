"""Unexecuted exact-rational A13 certified-row eligibility and symbolic shortlist.

No fitting, gzip decompression, scientific imports, gate emission or G2 adoption.
All20 decisions depend on externally pinned completed independent and ROOT receipts.
"""

import argparse
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
from fractions import Fraction
from importlib.util import cache_from_source
import json
import os
from pathlib import Path
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
AUTHOR = RESEARCH / "select_a13_certified_candidates_v2.py"
METHOD_DOC = RESEARCH / "A13_CERTIFIED_CANDIDATE_SELECTION_PREFLIGHT_V2.md"
PREFLIGHT = RESEARCH / "a13_certified_candidate_selection_preflight_v2.json"
READY = ROOT / ".context/A13_CERTIFIED_CANDIDATE_SELECTION_ROOT_READY_run002.json"
OUTPUT = PROGRAM / "A13_certified_candidate_selection_run002"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
AUDIT_NAME = "A13_recovery_audit_run006"
AUDIT = PROGRAM / AUDIT_NAME
AUDIT_SHA = "32c0cc8658bf2a2c89c86a5e685b4316d11a4a0e8b05b6c132fc2b0e78871b84"
AUDIT_COUNTS = [63, 1208, 2842]
AUDIT_READY = ROOT / ".context/A13_RECOVERY_AUDIT_V6_ROOT_READY_run001.json"
AUDIT_READY_SHA = "f3a0b5b792b8f231dac763ab0f86f7e84bbde6e114c456036a526ff1a173f46c"
PROTOCOL_SHA = "3ab2759c557563270a4a0242675f4d41123013df1f23f70d861b30b408db59e9"
AUDIT_AUTHORS = {
    ("audit_exp_frontier_recovery_v6.py"): (
        "54d841982c1a6f26b5a57814440609d5916dfad21cc3409ab57bee492ecc6c1b"
    ),
    ("A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V6.md"): (
        "e0e433417a5fc5e8d06e50ac0371c65c9f26ad3ebdc070121008ed4287e0f47e"
    ),
    ("a13_exp_frontier_recovery_audit_implementation_preflight_v6.json"): (
        "17b95075d6c124db2dae7c35ca976048699d4c0fc0c843f606f00ab10ef00a67"
    ),
}
REQUIRED_SNAPSHOTS = {
    ("A13_BERNSTEIN_EQUIVALENCE_PREFLIGHT_V5.md"): (
        "e7ff698ea67c3ea28776c7da92078871426e3faa2ad6de210d272792ad1cd4a3"
    ),
    ("A13_EXP_FRONTIER_PREFLIGHT.md"): (
        "f5b4404650c1ee9bd3a8ef2557d67e1340dda0fc059d94126e19fcfc046d7f7b"
    ),
    ("A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V4.md"): (
        "75b962da0239f371f34bc4c675243fba29b504038a68975a6b347fa0596af3f5"
    ),
    ("A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V5.md"): (
        "06ddca7b99dba0d44c5dcc7de7f27d5c26ea82691cf8bdccfe91a2d969ceae18"
    ),
    ("A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V6.md"): (
        "e0e433417a5fc5e8d06e50ac0371c65c9f26ad3ebdc070121008ed4287e0f47e"
    ),
    ("A13_EXP_FRONTIER_RECOVERY_DP_OPTIMIZATION_PREFLIGHT_V4.md"): (
        "86e0185742c7ae425372675806dad6da772e0303ca0d1d8fab1d8a59eb7c717c"
    ),
    ("A13_EXP_FRONTIER_RECOVERY_PREFLIGHT.md"): (
        "2d86febd3e35963e051113da6490b5e8ed352b7be10c79e6d8187cdf8950b747"
    ),
    ("A13_METADATA_PROFILE_ROOT_READY_run002.json"): (
        "641a2a6b3abcbe24c5c3374a35cc3fd973b773a4a4313a5e4d3bc2940c83d168"
    ),
    ("A13_METADATA_VALIDATION_PROFILE_PREFLIGHT_V2.md"): (
        "f07512a9714e611fdac659b4c3d83be4d6aa98daa92d4fabc1e0def9a43565b2"
    ),
    ("A13_RECOVERY_AUDIT_V6_ROOT_READY_run001.json"): (
        "f3a0b5b792b8f231dac763ab0f86f7e84bbde6e114c456036a526ff1a173f46c"
    ),
    ("a13_bernstein_equivalence_preflight_v5.json"): (
        "165426876e38662577fb1e1f1f816f664188245b46ec85bdf8c508e958c5880b"
    ),
    ("a13_exp_frontier_preflight.json"): (
        "6c0e97f33e1277c070e6e84883b6631a880997becd214772bb9ef287e1c7ba85"
    ),
    ("a13_exp_frontier_recovery_audit_implementation_preflight_v4.json"): (
        "8b1bf237dd2739fdbfe59c5af4cd2bf776dc29ce198d02dcf8c900bedae1e1ea"
    ),
    ("a13_exp_frontier_recovery_audit_implementation_preflight_v5.json"): (
        "c8d592ab4e6beb52b59bc4c3275ab9a33e7e898c94ef56a8a733be821f6d6693"
    ),
    ("a13_exp_frontier_recovery_audit_implementation_preflight_v6.json"): (
        "17b95075d6c124db2dae7c35ca976048699d4c0fc0c843f606f00ab10ef00a67"
    ),
    ("a13_exp_frontier_recovery_dp_optimization_preflight_v4.json"): (
        "5a98e3e210b3e4911b7b00042504f22a1ba406fe97e0b5e286904c741d2d53fd"
    ),
    ("a13_exp_frontier_recovery_preflight.json"): (
        "c36d9c97266144a73373c1dd55922585a2271206d0a5cc1ddf0f42ddaa9ce291"
    ),
    ("a13_metadata_validation_profile_preflight_v2.json"): (
        "8e612119a7af4eff12107b4d4a44b26891180b8406d4f59f901ada354cc74b84"
    ),
    ("audit_exp_frontier_recovery_v4.py"): (
        "61c05812abd7c7c042ab654a025e14b96afcfff00afd5398e72ea334307d07ba"
    ),
    ("audit_exp_frontier_recovery_v5.py"): (
        "c34f7096f783a61caa586c4e3f30067304da3d457626b367fd609ffebc2b2593"
    ),
    ("audit_exp_frontier_recovery_v6.py"): (
        "54d841982c1a6f26b5a57814440609d5916dfad21cc3409ab57bee492ecc6c1b"
    ),
    ("bernstein_integer_kernel_v5.py"): (
        "695c10c095c17a0827d5e180195021828b1613e77cb22f6ead42783b7fa70048"
    ),
    ("experiment_exp_frontier_recovery.py"): (
        "9a83c9ed87df61415af94b1ee15840c97714f48c90bebcf2c1d0b1367d79b8d9"
    ),
    ("profile_a13_metadata_validation_v2.py"): (
        "f033e7e551bad139e56fa9c350c3ce17f7a34bda85e156f4c091e1c366e51402"
    ),
    ("verify_a13_bernstein_equivalence_v5.py"): (
        "005b266056e791f06001f073858028096ff49f415f89cdc2f79b7de62ecca3ad"
    ),
}
GRID = tuple((degree, segments) for degree in (4, 6, 8, 10, 12) for segments in (1, 2, 4, 8))
CPU, ADMISSION, WALL = 180, 150, 600
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
FAILURE_NAMES = (
    ("FAILED_UNSEALED.json"),
    ("failed_unsealed.json"),
    ("failure.json"),
    ("run_failure.json"),
    ("prepare_failure.json"),
)
_FROZEN, _EXTERNAL, _OBSERVED = {}, {}, {}
_PATH_CACHE, _HASH_CACHE = {}, {}
_OWN_INVENTORIES, _ABSENT_RUNTIME = {}, set()
_CODE_CACHE_EXPECTED = {}
_BASE_SCOPE, _EXCLUDED_SCOPE = None, None
_STANDARD_RUNTIME_MEMBERS = set()
_HASH_WORK = _REFERENCES = 0
_STARTED = None
_SOURCE_INTERPRETER = None


MATERIAL = PROGRAM / "A13_run002"
METADATA_SOURCE = PROGRAM / "A13_recovery_run001"
FINAL_ROOT = PROGRAM / "A13_recovery_audit_ROOT_verification_run006"
FINAL_ROOT_READY = ROOT / ".context/A13_RECOVERY_AUDIT_ROOT_INTEGRITY_V6_ROOT_READY_run006.json"
FINAL_ROOT_READY_SHA = "378f5252b3ffc906f70f14e522f0525e8b72bad07262e339206dc4f2f4ffb5f2"
# Externally supplied by ROOT after the completed final integrity PASS.
FINAL_ROOT_SHA = "b43d4f3f76061129af57f03b72d61d79b9a313795c543c804c5966d326989bab"
FINAL_ROOT_COUNTS = [8, 1241, 2842]
CORE_DERIVATION_SHA = "84b789dfd37ab68c4f94cd6ccde7723f7dd0a585b329878fb5c137956d2681c3"
ALPHA = [1, 16777216]
ALLOWANCE = [
    4073883417731182862847997641774456332891573449254683949318947788511038490778395976239348623,
    68351585149469122636640694597425667667286544715412888638305331450311031224980497600734786781970432,
]
BASELINES = {"B4x12": [520720662, 555774, 550141], "B8x52": [4267435214, 663704, 4460479]}
SITES = {"B4x12": [48, 30], "B8x52": [416, 234]}
ALLOCATION_PACKETS = [
    [
        "A13_fixed_alpha_allocation_run001",
        "4c863e4a031a458c5a424c75774f791f49c25c9c25e030a6fd28e5e8ec91236f",
        [19, 1008, 2842],
        "a13-fixed-alpha-allocation-producer-terminal-manifest-v1",
        "receipt",
    ],
    [
        "A13_fixed_alpha_allocation_audit_run001",
        "829712c9c71925ba74e98059a294c99c812fe659fd0b31a44c50ef35c6b31358",
        [20, 1029, 2842],
        "a13-fixed-alpha-allocation-auditor-terminal-manifest-v1",
        "receipt",
    ],
    [
        "A13_fixed_alpha_allocation_root_verification_run002",
        "39930d414dde63f1ed087423de1877d565a509038a87a68bc478c7ccb9c365bf",
        [5, 1060, 2842],
        "root-exp-frontier-allocation-integrity-manifest-v2",
        "ROOT",
    ],
]
MAX_SCALAR_BITS = 2048
MAX_RESULT_BITS = 8192
MAX_NATIVE_CELLS = 20 * 2 * 30 * 8
MAX_IR_NODES = 64
_FAILED_MATERIAL_MEMBERS = set()
_FAILED_MATERIAL_BYTES = None


PRIOR_SELECTION = PROGRAM / "A13_certified_candidate_selection_run001"
PRIOR_SELECTION_FREEZE = (
    ROOT / ".context/A13_CERTIFIED_SELECTION_V1_FAILED_OWNED_FROZEN_run001.json"
)
PRIOR_SELECTION_FREEZE_SHA = "9538230d4e268e8d57123e272b75f52b01d922c0433da9fceb5c427fdfb6f63d"
PRIOR_SELECTION_READY = ROOT / ".context/A13_CERTIFIED_CANDIDATE_SELECTION_ROOT_READY_run001.json"
PRIOR_SELECTION_READY_SHA = "b105057da6040d17d0804320ff2c80081f75ca41fd3a85b4d898d6484c83f45a"
PRIOR_SELECTION_LOG = ROOT / ".context/a13_certified_selection_run001.log"
PRIOR_SELECTION_LOG_SHA = "e67e023ff8d5f5029400709f50255594e06c2692f85e42b3a6221978eab5f4af"
PRIOR_SELECTION_AUTHORS = {
    "select_a13_certified_candidates_v1.py": (
        "4b18973647539c539c6ca7fb92d7bb328df316858b2710677f4d9a895641a7f3"
    ),
    "A13_CERTIFIED_CANDIDATE_SELECTION_PREFLIGHT_V1.md": (
        "558404e9db891ac243546788e8c53732026011ce309deb6c790eb2e1674e7b4d"
    ),
    "a13_certified_candidate_selection_preflight_v1.json": (
        "71a21f6af54f3f1900439899050a17eded15a7f03840b8d8a24780ae8c96e60b"
    ),
}
_SELECTION_FAILED_MEMBERS = set()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def process_started():
    require(os.name == "nt" and ctypes.sizeof(ctypes.c_void_p) == 8, "Pinned Win64")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.argtypes = []
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    stamps = [wintypes.FILETIME() for _ in range(4)]
    require(
        kernel.GetProcessTimes(
            kernel.GetCurrentProcess(), *[ctypes.byref(stamp) for stamp in stamps]
        ),
        "Actual process creation clock",
    )
    ticks = (stamps[0].dwHighDateTime << 32) | stamps[0].dwLowDateTime
    age_ns = time.time_ns() - (ticks - 116444736000000000) * 100
    require(age_ns >= 0, "Actual UTC creation precedes observation")
    # GetCurrentProcess is a pseudo-handle, never an owned handle to close.
    return time.monotonic() - age_ns / 1_000_000_000


def budget(admission=False):
    require(time.process_time() < (ADMISSION if admission else CPU), "Process CPU guard")
    require(time.monotonic() - _STARTED < WALL, "Creation-derived wall guard")


def runtime_scopes():
    global _BASE_SCOPE, _EXCLUDED_SCOPE
    budget()
    lexical = Path(os.path.abspath(sys.base_prefix))
    actual = lexical.resolve(strict=True)
    require(actual == lexical, "Actual base prefix has no alias")
    excluded = lexical / "Lib/site-packages"
    physical_excluded = excluded.resolve(strict=False)
    scopes = (actual, (excluded, physical_excluded))
    if _BASE_SCOPE is not None:
        require(scopes == (_BASE_SCOPE, _EXCLUDED_SCOPE), "Actual runtime scopes unchanged")
    _BASE_SCOPE, _EXCLUDED_SCOPE = scopes
    budget()


def canonical(path, fresh=False):
    budget()
    path = Path(path)
    require(not path.drive or path.is_absolute(), "No ambiguous drive-relative input")
    lexical = Path(os.path.abspath(str(path)))
    require(
        not any(lexical.is_relative_to(scope) for scope in _EXCLUDED_SCOPE),
        "Excluded base packages lexical path",
    )
    key = str(lexical)
    if not fresh and key in _PATH_CACHE:
        cached, identity = _PATH_CACHE[key]
        if fingerprint(lexical) == identity:
            budget()
            return cached
    actual = lexical.resolve(strict=True)
    require(
        not any(actual.is_relative_to(scope) for scope in _EXCLUDED_SCOPE),
        "Excluded base package alias",
    )
    require(actual == lexical, "No lexical-to-physical input alias")
    require(
        key not in _PATH_CACHE or _PATH_CACHE[key][0] == actual,
        "Previously confined lexical input did not redirect",
    )
    _PATH_CACHE[key] = (actual, fingerprint(lexical))
    budget()
    return actual


def fingerprint(path):
    stat = path.stat()
    return tuple(
        getattr(stat, name, None)
        for name in (
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


def digest(path, fresh=False, already_resolved=False):
    global _HASH_WORK
    budget()
    path = path if already_resolved else canonical(path, fresh=fresh)
    require(path.is_file(), "Actual regular SHA input")
    before, total, state = fingerprint(path), 0, hashlib.sha256()
    if not fresh and path in _HASH_CACHE and _HASH_CACHE[path][0] == before:
        budget()
        return _HASH_CACHE[path][1]
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            budget()
            total += len(chunk)
            _HASH_WORK += len(chunk)
            require(_HASH_WORK <= MAX_HASH_WORK, "Fixed24GiB hashing-work cap")
            require(total <= before[2], "Input grew while hashing")
            state.update(chunk)
    require(total == before[2] and fingerprint(path) == before, "Stable actual byte hash")
    result = state.hexdigest()
    require(
        path not in _OBSERVED or _OBSERVED[path] == result, "Previously observed bytes unchanged"
    )
    _OBSERVED.setdefault(path, result)
    _HASH_CACHE[path] = (before, result)
    budget()
    return result


def add(path, expected):
    global _REFERENCES
    budget()
    _REFERENCES += 1
    require(_REFERENCES <= MAX_REFERENCES, "Fixed100k map-reference cap")
    require(
        type(expected) is str
        and len(expected) == 64
        and all(char in "0123456789abcdef" for char in expected),
        "Exact expected SHA",
    )
    actual = canonical(path)
    require(actual.is_file(), "Regular preserved input")
    if actual.is_relative_to(ROOT):
        key, mapping = actual.relative_to(ROOT).as_posix(), _FROZEN
    else:
        require(actual.is_relative_to(_BASE_SCOPE), "Actual external base runtime")
        key, mapping = str(actual), _EXTERNAL
    require(key not in mapping or mapping[key] == expected, "Canonical equal-SHA expectations")
    mapping[key] = expected
    return actual


def read(path):
    global _HASH_WORK
    budget()
    path = canonical(path)
    before = fingerprint(path)
    require(path.is_file() and before[2] <= 128 * 1024**2, "Bounded regular JSON input")
    chunks, total, state = [], 0, hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            budget()
            total += len(chunk)
            _HASH_WORK += len(chunk)
            require(_HASH_WORK <= MAX_HASH_WORK and total <= before[2], "Bounded JSON reads")
            chunks.append(chunk)
            state.update(chunk)
    require(total == before[2] and fingerprint(path) == before, "Stable JSON bytes")
    expected = (
        _FROZEN.get(path.relative_to(ROOT).as_posix())
        if path.is_relative_to(ROOT)
        else _EXTERNAL.get(str(path))
    )
    observed = state.hexdigest()
    require(expected is not None and observed == expected, "JSON belongs to exact admitted SHA")
    require(path not in _OBSERVED or _OBSERVED[path] == observed, "Stable observed JSON SHA")
    _OBSERVED[path] = observed
    _HASH_CACHE[path] = (before, observed)
    budget()
    result = json.loads(b"".join(chunks))
    budget()
    return result


def no_failure(directory):
    require(
        not any((directory / name).exists() for name in FAILURE_NAMES),
        "Authoritative failure marker prohibits admission",
    )


def inventory(directory):
    found, total = set(), 0
    for root, dirs, names in os.walk(directory, followlinks=False):
        budget()
        for name in dirs:
            candidate = Path(root) / name
            require(canonical(candidate).is_relative_to(directory), "No owned directory escape")
            require(not candidate.is_symlink(), "No owned directory link")
        for name in names:
            actual = canonical(Path(root) / name)
            require(actual.is_relative_to(directory) and actual not in found, "Unique owned path")
            require(actual.is_file(), "Regular actual owned entry")
            found.add(actual)
            total += actual.stat().st_size
            require(len(found) <= 25000 and total <= MAX_UNIQUE_BYTES, "Finite owned inventory")
    return found


def own_runtime():
    global _STANDARD_RUNTIME_MEMBERS
    require(
        canonical(sys.executable) == canonical(LAUNCHER)
        and sys.dont_write_bytecode is True
        and canonical(Path.cwd()) == ROOT,
        "Exact pinned launcher/cwd and startup -B",
    )
    require(
        not any(os.environ.get(key) for key in ("PYTHONPATH", "PYTHONHOME", "NUMBA_CACHE_DIR")),
        "No inherited runtime search/cache overrides",
    )
    require(canonical(sys.prefix) == ROOT / ".context/frontier_t0_env", "Pinned isolated prefix")
    cfg = Path(sys.prefix) / "pyvenv.cfg"
    add(cfg, digest(cfg))
    require(
        "include-system-site-packages = false" in cfg.read_text(encoding="utf-8").lower(),
        "Base site packages disabled",
    )
    base = canonical(sys.base_prefix)
    permitted = {
        ROOT,
        RESEARCH,
        base,
        canonical(sys.prefix),
        canonical(Path(sys.prefix) / "Lib/site-packages"),
        canonical(base / "Lib"),
        canonical(base / "DLLs"),
    }
    for entry in sys.path:
        lexical = Path(os.path.abspath(str(ROOT if not entry else entry)))
        require(
            not any(lexical.is_relative_to(scope) for scope in _EXCLUDED_SCOPE)
            and not any(
                lexical.resolve(strict=False).is_relative_to(scope) for scope in _EXCLUDED_SCOPE
            ),
            "No excluded search path even when absent",
        )
        if not lexical.exists():
            expected_zip = base / (
                "python" + str(sys.version_info.major) + str(sys.version_info.minor) + ".zip"
            )
            require(
                lexical == expected_zip and lexical.resolve(strict=False) == expected_zip,
                "Only the exact absent standard interpreter zip search entry",
            )
            _ABSENT_RUNTIME.add(lexical)
            continue
        path = canonical(ROOT if not entry else entry)
        require(
            path in permitted or (path.is_file() and path.parent == base and path.suffix == ".zip"),
            "Finite actual runtime search path",
        )
        if path.is_file():
            add(path, digest(path))
    candidates = standard_runtime_members()
    _STANDARD_RUNTIME_MEMBERS = candidates
    total = 0
    for path in sorted(candidates):
        require(path.is_file(), "Regular complete runtime member")
        total += path.stat().st_size
        require(
            len(candidates) <= MAX_RUNTIME_FILES and total <= MAX_RUNTIME_BYTES,
            "Fixed24k runtime files/2GiB",
        )
        add(path, digest(path))
    loaded_origins()
    return {
        "files": len(candidates),
        "bytes": total,
        "base_site_packages_pruned_and_rejected": True,
    }


def standard_runtime_members():
    base = canonical(sys.base_prefix)
    candidates = set()
    excluded = base / "Lib/site-packages"
    for tree in (base / "Lib", base / "DLLs", Path(sys.prefix) / "Scripts"):
        for root, dirs, names in os.walk(tree, topdown=True, followlinks=False):
            budget()
            dirs[:] = [name for name in dirs if Path(root) / name != excluded]
            for name in dirs:
                require(not (Path(root) / name).is_symlink(), "No runtime directory alias")
                canonical(Path(root) / name)
            for name in names:
                candidates.add(canonical(Path(root) / name))
                require(len(candidates) <= MAX_RUNTIME_FILES, "Finite complete runtime membership")
    for directory in (
        base,
        canonical(sys.prefix),
        canonical(Path(sys.prefix) / "Lib/site-packages"),
    ):
        for path in directory.iterdir():
            budget()
            if path.is_file():
                candidates.add(canonical(path))
                require(len(candidates) <= MAX_RUNTIME_FILES, "Finite adjacent runtime membership")
    return candidates


def key_for(path):
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def bind(path, expected):
    actual = add(path, expected)
    require(digest(actual) == expected, "Actual admitted expected bytes")
    return actual


def fresh_union():
    runtime_scopes()
    for lexical, (actual, _) in tuple(_PATH_CACHE.items()):
        budget()
        require(canonical(lexical, fresh=True) == actual, "Every lexical alias freshly confined")
    union = {}
    for mapping in (_FROZEN, _EXTERNAL):
        for key, expected in mapping.items():
            budget()
            path = Path(key) if Path(key).is_absolute() else ROOT / key
            require(path not in union or union[path] == expected, "Equal-SHA complete union")
            union[path] = expected
    for path, value in tuple(_OBSERVED.items()):
        budget()
        require(path not in union or union[path] == value, "Observed never replaces expected")
        union[path] = value
    total = 0
    for path, expected in sorted(union.items()):
        budget()
        actual = canonical(path, fresh=True)
        total += actual.stat().st_size
        require(len(union) <= MAX_REFERENCES and total <= MAX_UNIQUE_BYTES, "Complete union caps")
        require(
            digest(actual, fresh=True, already_resolved=True) == expected, "Full fresh actual SHA"
        )
    for directory, members in _OWN_INVENTORIES.items():
        budget()
        require(inventory(directory) == members, "All original own inventories unchanged")
        no_failure(directory)
    require(
        standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS,
        "Complete runtime membership unchanged",
    )
    require(
        not any(path.exists() or path.is_symlink() for path in _ABSENT_RUNTIME),
        "Absent standard zip and new-code caches still absent",
    )
    return {"unique_paths": len(union), "unique_bytes": total, "full_fresh_resolve_and_SHA": True}


def code_caches(sources, pins, absent_keys):
    """External presence/absence admission; source execution never reads these caches."""
    budget()
    paths = {
        key_for(Path(cache_from_source(str(source)))): Path(cache_from_source(str(source)))
        for source in sources
    }
    present = {key for key, path in paths.items() if path.exists()}
    require(
        type(pins) is dict
        and set(pins) == present
        and type(absent_keys) is list
        and absent_keys == sorted(set(paths) - present),
        "Exact external cache presence and absence declaration",
    )
    for key in present:
        path = bind(paths[key], pins[key])
        _CODE_CACHE_EXPECTED[path] = pins[key]
    for key in absent_keys:
        path = paths[key]
        require(not path.exists() and not path.is_symlink(), "No absent cache or dangling alias")
        _ABSENT_RUNTIME.add(path)
    budget()


def check_code_caches():
    budget()
    for path, expected in _CODE_CACHE_EXPECTED.items():
        require(digest(path, fresh=True) == expected, "Declared existing cache bytes unchanged")
    require(
        not any(path.exists() or path.is_symlink() for path in _ABSENT_RUNTIME),
        "Declared absent caches and standard zip remain absent",
    )
    budget()


def complete_manifest(value, owned, nonmanifest_bytes):
    """Check exact UTF8 JSON bytes and file count including the prospective manifest."""
    budget()
    require(len(owned) + 1 <= MAX_OWN_FILES, "Manifest-inclusive owned file cap")
    value["manifest_inclusive_owned_file_count"] = len(owned) + 1
    value["owned_nonmanifest_bytes"] = nonmanifest_bytes
    value["manifest_inclusive_retention_checked_before_sealing"] = True
    manifest_bytes = 1  # save() appends exactly one newline.
    for fragment in json.JSONEncoder(sort_keys=True, indent=2, allow_nan=False).iterencode(value):
        budget()
        manifest_bytes += len(fragment.encode("utf-8"))
        require(nonmanifest_bytes + manifest_bytes <= MAX_OWN_BYTES, "Manifest-inclusive128MiB cap")
    save("manifest.json", value)
    require(
        (OUTPUT / "manifest.json").stat().st_size == manifest_bytes, "Exact encoded manifest size"
    )
    actual = inventory(OUTPUT)
    require(
        actual == {OUTPUT / name for name in owned} | {OUTPUT / "manifest.json"}
        and len(actual) == len(owned) + 1 <= MAX_OWN_FILES,
        "Complete final manifest-inclusive inventory",
    )
    total = 0
    for path in actual:
        budget()
        total += path.stat().st_size
    require(
        total == nonmanifest_bytes + manifest_bytes <= MAX_OWN_BYTES,
        "Complete final owned byte cap",
    )
    budget()


def save(name, value):
    budget()
    target = OUTPUT / name
    require(target.parent == OUTPUT and not target.exists(), "Exclusive metadata output")
    pieces, new_bytes = [], 0
    for fragment in json.JSONEncoder(indent=2, sort_keys=True, allow_nan=False).iterencode(value):
        budget()
        part = fragment.encode("utf-8")
        new_bytes += len(part)
        require(new_bytes <= MAX_OWN_BYTES, "Bounded prospective UTF8 serialization")
        pieces.append(part)
    pieces.append(b"\n")
    new_bytes += 1
    members = inventory(OUTPUT)
    current_bytes = 0
    for member in members:
        budget()
        current_bytes += member.stat().st_size
    require(
        len(members) + 1 + (name != "manifest.json") <= MAX_OWN_FILES
        and current_bytes + new_bytes <= MAX_OWN_BYTES,
        "Inclusive owned byte/file cap with a final manifest slot",
    )
    with target.open("xb") as stream:
        for piece in pieces:
            budget()
            stream.write(piece)
    require(target.stat().st_size == new_bytes, "Exactly admitted output bytes")
    budget()


def copy(path, name):
    source = canonical(path)
    before, expected = fingerprint(source), digest(source)
    target = OUTPUT / name
    members = inventory(OUTPUT)
    require(target.parent == OUTPUT and not target.exists(), "New fixed copied output")
    require(
        len(members) + 2 <= MAX_OWN_FILES
        and sum(member.stat().st_size for member in members) + before[2] <= MAX_OWN_BYTES,
        "Admitted copied bytes with a manifest slot",
    )
    total = 0
    with source.open("rb") as incoming, target.open("xb") as outgoing:
        while block := incoming.read(65536):
            budget()
            total += len(block)
            require(total <= before[2], "Copied source cannot grow")
            outgoing.write(block)
    require(total == before[2] and fingerprint(source) == before, "Stable complete source copy")
    require(digest(target) == expected, "Exact preserved copied source bytes")


def exact_relative(key):
    require(
        type(key) is str
        and key
        and not Path(key).is_absolute()
        and not Path(key).drive
        and "\\" not in key
        and all(part not in ("", ".", "..") for part in key.split("/"))
        and Path(key).as_posix() == key,
        "Exact original slash-relative spelling without adaptation",
    )


def current_packet():
    directory = canonical(AUDIT)
    manifest = bind(directory / "manifest.json", AUDIT_SHA)
    data = read(manifest)
    no_failure(directory)
    require(
        data.get("schema") == "a13-exp-frontier-recovery-independent-audit-manifest-v1"
        and data.get("passed") is True
        and data.get("completed") is True
        and data.get("budget_censored") is False
        and data.get("manifest_self_hash_excluded") is True
        and data.get("original_expected_hashes_waived") is False
        and data.get("manifest_inclusive_retention_checked") is True
        and data.get("manifest_inclusive_owned_count") == 64,
        "Only actual completed current V6 all20 scientific-audit receipt",
    )
    require(
        [len(data[field]) for field in (("files"), ("frozen_inputs"), ("external_runtime_inputs"))]
        == AUDIT_COUNTS,
        "Complete current63/1208/2842 maps, no reduced index",
    )
    owned = {manifest}
    for field in ("files", "frozen_inputs", "external_runtime_inputs"):
        require(type(data[field]) is dict, "Typed complete current maps")
        for key, expected in data[field].items():
            budget()
            if field == "external_runtime_inputs":
                require(
                    type(key) is str and Path(key).is_absolute(),
                    ("Exact absolute external spelling"),
                )
                path = Path(key)
            else:
                exact_relative(key)
                path = directory / key if field == "files" else ROOT / key
            actual = bind(path, expected)
            if field == "files":
                require(
                    actual.is_relative_to(directory)
                    and actual not in owned
                    and actual.relative_to(directory).as_posix() == key,
                    "Exact receipt-relative current owned key and physical confinement",
                )
                owned.add(actual)
            elif field == "frozen_inputs":
                require(
                    actual.is_relative_to(ROOT) and actual.relative_to(ROOT).as_posix() == key,
                    ("Exact source ROOT-relative expectation"),
                )
            else:
                require(
                    not actual.is_relative_to(ROOT) and str(actual) == key,
                    ("Exact source external expectation"),
                )
    require(
        inventory(directory) == owned and len(owned) == 64,
        ("Complete current64 actual owned inventory"),
    )
    _OWN_INVENTORIES[directory] = owned
    require(
        {
            key.split(("/"), 1)[1]: pin
            for key, pin in data[("files")].items()
            if key.startswith(("executed_code/"))
        }
        == REQUIRED_SNAPSHOTS,
        "All25 original snapshot names and hashes unchanged",
    )
    require(
        {key for key in data[("files")] if key.startswith(("rows/"))}
        == {f"rows/d{d}_s{s}.json.gz" for d, s in GRID},
        "Exactly20 fresh canonical compressed row names",
    )
    require(
        data[("files")].get(("protocol.json")) == PROTOCOL_SHA,
        ("Externally preserved prepared protocol expected SHA"),
    )
    require(
        data["historical_global_LIVE_integrity"]
        == {
            ("passed"): False,
            ("mismatch_references"): 36,
            ("distinct_paths"): 9,
            ("expected_hashes_waived"): False,
        },
        "Historical LIVE mismatch remains unapproved and unwaived",
    )
    return data


def loaded_origins():
    forbidden = {"mpmath", "numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
    require(
        not any(name.split(("."), 1)[0] in forbidden for name in sys.modules),
        ("No numerical or scientific imports"),
    )
    require(
        not any(
            name.startswith(("research."))
            and name not in {__name__, ("research.limitation_program_20261001")}
            for name in sys.modules
        ),
        "No scientific source, auditor, kernel or historical helper imports",
    )
    for module in tuple(sys.modules.values()):
        budget()
        for attribute in ("__file__", "__cached__"):
            origin = getattr(module, attribute, None)
            if not origin:
                continue
            lexical = Path(os.path.abspath(str(origin)))
            require(
                not lexical.is_relative_to(_EXCLUDED_SCOPE[0])
                and not lexical.resolve(strict=False).is_relative_to(_EXCLUDED_SCOPE[1]),
                "No excluded loaded runtime source/cache",
            )
            if lexical.is_file():
                actual = canonical(lexical)
                key = key_for(actual)
                mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
                if key not in mapping:
                    add(actual, digest(actual))
                else:
                    require(
                        digest(actual) == mapping[key],
                        ("Loaded bytes retain original expected SHA"),
                    )
            else:
                require(
                    attribute == "__cached__"
                    and not lexical.exists()
                    and not lexical.is_symlink()
                    and lexical.resolve(strict=False) == lexical,
                    "Only exact absent loaded cache route, never missing source or dangling alias",
                )
                _ABSENT_RUNTIME.add(lexical)


def source_protocol_checks(manifest):
    global _SOURCE_INTERPRETER
    protocol = read(bind(AUDIT / "protocol.json", PROTOCOL_SHA))
    require(
        protocol["schema"] == "a13-exp-frontier-recovery-independent-audit-protocol-v1"
        and protocol["operational_recovery_audit_version"] == 6
        and protocol["V6_ROOT_READY_SHA256"] == AUDIT_READY_SHA
        and protocol["output"] == AUDIT.relative_to(ROOT).as_posix()
        and protocol["CPU_admission_wall_seconds"] == [300, 270, 900]
        and protocol["independent_digits"] == 130
        and protocol["primary_digits"] == 90
        and protocol["fixed_grid"] == [list(row) for row in GRID]
        and protocol["threads"] == 1
        and protocol["gate_emission_authorized"] is False
        and protocol["new_fixture_credit"] == 0
        and protocol["candidate_G2_absolute_stock_error_allocation"] is None
        and protocol["candidate_G2_barrier_band_allocation"] is None,
        "Exact originally frozen V6 scientific scope and clocks, read as metadata only",
    )
    require(
        [len(protocol[field]) for field in (("frozen_inputs"), ("external_runtime_inputs"))]
        == [1198, 2842],
        "Complete original prospective source maps retained",
    )
    for field in ("frozen_inputs", "external_runtime_inputs"):
        require(type(protocol[field]) is dict, "Typed prospective full expected maps")
        for key, expected in protocol[field].items():
            budget()
            require(
                manifest[field].get(key) == expected,
                ("Every prospective source SHA expectation remains equal and strict"),
            )
    for name, expected in AUDIT_AUTHORS.items():
        require(
            manifest[("frozen_inputs")].get((RESEARCH / name).relative_to(ROOT).as_posix())
            == expected
            and REQUIRED_SNAPSHOTS[name] == expected,
            "Original executed trio and exact retained snapshots agree",
        )
    _SOURCE_INTERPRETER = read(AUDIT / "interpreter.json")
    require(
        _SOURCE_INTERPRETER == protocol[("interpreter")],
        ("Original full prepared interpreter record unchanged"),
    )
    require(
        _SOURCE_INTERPRETER["executable"] == str(LAUNCHER)
        and _SOURCE_INTERPRETER["base_executable"] == str(_BASE_SCOPE / "python.exe")
        and _SOURCE_INTERPRETER["base_prefix"] == str(_BASE_SCOPE)
        and _SOURCE_INTERPRETER["venv_prefix"] == str(ROOT / ".context/frontier_t0_env")
        and _SOURCE_INTERPRETER["sys_path"] == sys.path
        and _SOURCE_INTERPRETER["startup_bytecode_disabled"] is True
        and _SOURCE_INTERPRETER["standard_Lib_excludes_only_unreachable_base_site_packages"] is True
        and _SOURCE_INTERPRETER["base_site_packages_import_rejected"] is True,
        "Exact original base/prefix/search/source-runtime scope, no scientific import",
    )
    for spelling in _SOURCE_INTERPRETER["absent_standard_runtime_paths"]:
        path = Path(spelling)
        require(
            path.is_absolute()
            and not path.exists()
            and not path.is_symlink()
            and path.resolve(strict=False) == path,
            "Original declared runtime absence remains exact",
        )
        _ABSENT_RUNTIME.add(path)
    for record in read(AUDIT / "loaded_module_origins.json"):
        budget()
        require(
            type(record) is dict
            and record["kind"] in ("source", "cache")
            and type(record["module"]) is str,
            "Saved original loaded origins are metadata only",
        )
        bind(Path(record["path"]), record["sha256"])
    return protocol


def saved_runtime_membership():
    """Rewalk original file roots, including opaque numerical sources, without imports."""
    require(_SOURCE_INTERPRETER is not None, "Full source runtime metadata admitted first")
    record = _SOURCE_INTERPRETER["runtime_inventory"]
    declared = record["actual_file_paths"]
    require(
        type(declared) is list and len(declared) == len(set(declared)) == record["files"] == 3057,
        "Complete original3057 unique runtime file inventory",
    )
    found = set()
    for spelling in record["roots"]:
        budget()
        root = canonical(spelling)
        if root.is_file():
            found.add(root)
        else:
            require(root.is_dir(), "Saved runtime root remains regular file or directory")
            for directory, dirs, names in os.walk(root, followlinks=False):
                budget()
                parent = canonical(directory)
                dirs[:] = [name for name in dirs if parent / name != _EXCLUDED_SCOPE[0]]
                for name in dirs:
                    child = parent / name
                    require(
                        not child.is_symlink() and canonical(child).is_relative_to(root),
                        ("Original runtime directory has no alias or escape"),
                    )
                for name in names:
                    found.add(canonical(parent / name))
                    require(
                        len(found) <= MAX_RUNTIME_FILES, ("Bounded complete saved runtime rewalk")
                    )
    expected_paths = {Path(path) for path in declared}
    require(found == expected_paths, "Complete actual original runtime membership unchanged")
    total = 0
    for path in found:
        budget()
        require(path.is_file(), "Saved runtime path stays a regular file")
        key = key_for(path)
        mapping = _FROZEN if path.is_relative_to(ROOT) else _EXTERNAL
        require(key in mapping, "Every saved runtime member has an original admitted expected SHA")
        total += path.stat().st_size
    require(
        total == record[("bytes")] and total <= MAX_RUNTIME_BYTES,
        ("Original runtime byte count and caps unchanged"),
    )
    adjacent = {str(path) for path in _BASE_SCOPE.iterdir() if path.is_file()}
    require(
        adjacent == set(_SOURCE_INTERPRETER[("external_adjacent_files")]),
        ("Original full base adjacent membership unchanged"),
    )
    prefix = ROOT / ".context/frontier_t0_env"
    prefix_members = sorted(
        [path.name, ("file") if path.is_file() else ("directory")] for path in prefix.iterdir()
    )
    require(
        prefix_members == _SOURCE_INTERPRETER[("venv_root_directory_membership")],
        ("Original venv root membership unchanged"),
    )
    hooks = {str(path) for path in (prefix / "Lib/site-packages").glob("*.pth")}
    require(
        hooks
        == {
            path
            for path in _SOURCE_INTERPRETER[("bootstrap_hook_and_loaded_venv_paths")]
            if path.endswith((".pth"))
        },
        "No new or removed startup hook",
    )
    return {
        ("saved_runtime_files"): len(found),
        ("saved_runtime_bytes"): total,
        ("numerical_package_sources_hashed_not_imported"): True,
    }


def source_clocks(document):
    budget()
    require(
        document["budget"]["process_CPU_seconds"] >= 0
        and document["budget"]["process_CPU_seconds"] < 300
        and document["budget"]["wall_seconds"] >= 0
        and document["budget"]["wall_seconds"] < 900,
        "Retained source clock snapshots fit original limits; not a final OS-exit observation",
    )


def reconcile_metadata(manifest):
    summary = read(AUDIT / "summary.json")
    require(
        summary["schema"] == "a13-exp-frontier-recovery-independent-audit-summary-v1"
        and summary["operational_recovery_audit_version"] == 6
        and summary["V6_ROOT_READY_SHA256"] == AUDIT_READY_SHA,
        "Exact current all20 scientific summary metadata",
    )
    for key in (
        "completed",
        "passed",
        "independent_audit_passed",
        "metadata_source_passed",
        "scientific_screen_complete",
        "all20_uniformly_certified",
        "all_untrusted_claimed_rows_independently_recertified",
        "every_claimed_primary80_uniform_bound_authorized_by_independent130",
        "independent112_uniform_witnesses_retained_separately",
        "exact_finite_fitting_transcript_and_single_tie_even_quantization_checked",
        "all_claimed_native_intermediate72_product144_and_shift_guards_independently_recomputed",
        (
            "all_claimed_selector_QROM_argument_output_copies_banks_"
            "and_cleanup_costs_independently_reconstructed"
        ),
        "global_financial_forward_and_inverse_clean_function_invocations_paid",
        "symbolic_resources_not_actual_source_or_capped_schedule",
        "original_failure_remains_authoritative_zero_credit",
    ):
        require(summary[key] is True, "Retained scoped all20 certification claim: " + key)
    for key in (
        "rejection",
        "budget_censored",
        "failed_original_source_mathematical_PASS",
        "partial_v5_rows_promoted",
        "old_censored_proof_rows_promoted_or_reused",
        "scientific_producer_or_helper_imports",
        "source_expected_hashes_waived",
        "gate_emission_authorized",
        "full_G2",
        "adoption",
        "cost_transfer",
        "feasible_architecture_or_realized_cost_improvement_claim",
    ):
        require(summary[key] is False, "Retained scientific scope prohibition: " + key)
    for key in (
        "new_test_credit",
        "new_gate_replays",
        "new_price_samples",
        "retained_rejected_rows",
        "prior_failed_recovery_audit_credit",
        "prior_failed_recovery_audit_v2_credit",
        "prior_failed_recovery_audit_v3_credit",
        "prior_failed_recovery_audit_v4_credit",
        "prior_failed_recovery_audit_v5_credit",
    ):
        require(summary[key] == 0, "Zero new or prior-failure credit: " + key)
    require(
        summary["fixed_architecture_rows"] == summary["certified_estimate_rows"] == 20
        and summary["candidate_G2_absolute_stock_error_allocation"] is None
        and summary["candidate_G2_barrier_band_allocation"] is None,
        "Exactly all20 finite certificates without G2 allocation or feasibility",
    )
    source_clocks(summary)
    index = read(AUDIT / "fixed_inventory_authorization.json")
    require(
        index["all20_rows_and_rejections_retained"] is True
        and index["original_baseline_retained_separately"] is True
        and index["fixed_row_statuses"] == summary["fixed_row_statuses"],
        "Complete source row-status metadata equals exact summary",
    )
    expected_statuses = [
        {
            ("degree"): d,
            ("segments"): s,
            ("row_id"): f"d{d}_s{s}",
            ("status"): ("CERTIFIED_ESTIMATE"),
        }
        for d, s in GRID
    ]
    require(
        index[("fixed_row_statuses")] == expected_statuses,
        ("Exactly20 ordered certified fixed architecture statuses"),
    )
    rows = index["independent_row_artifacts"]
    require(type(rows) is list and len(rows) == 20, "Exactly20 original artifact descriptors")
    for descriptor, (degree, segments) in zip(rows, GRID, strict=True):
        budget()
        route = f"rows/d{degree}_s{segments}.json.gz"
        require(
            descriptor["actual_row_file"] == route
            and descriptor["row_id"] == f"d{degree}_s{segments}"
            and descriptor["degree"] == degree
            and descriptor["segments"] == segments
            and descriptor["status"] == "CERTIFIED_ESTIMATE"
            and descriptor["artifact_encoding"] == "canonical-gzip-json-v1"
            and descriptor["compact_sorted_JSON"] is True
            and descriptor["compression_level"] == 1
            and descriptor["gzip_filename"] == ""
            and descriptor["gzip_mtime"] == 0
            and descriptor["compressed_SHA256"] == manifest["files"][route]
            and descriptor["compressed_bytes"] == (AUDIT / route).stat().st_size,
            "Exact named freshly generated row descriptor and opaque compressed-byte expectation",
        )
        require(
            type(descriptor["uncompressed_JSON_SHA256"]) is str
            and len(descriptor["uncompressed_JSON_SHA256"]) == 64
            and all(c in "0123456789abcdef" for c in descriptor["uncompressed_JSON_SHA256"])
            and type(descriptor[("uncompressed_bytes")]) is int
            and descriptor[("uncompressed_bytes")] > 0,
            "Saved uncompressed descriptor is typed metadata, never a decompression claim",
        )
    outcome = read(AUDIT / "completion_outcome.json")
    require(
        outcome["phase"] == "run"
        and outcome["summary_file"] == "summary.json"
        and outcome["limits_CPU_admission_wall"] == [300, 270, 900],
        "Original exact completed run terminal and immutable clocks",
    )
    for key in (
        ("completed"),
        ("passed"),
        ("independent_audit_passed"),
        ("metadata_source_passed"),
        ("scientific_screen_complete"),
    ):
        require(outcome[key] is True, "Actual completed terminal metadata")
    for key in (
        ("budget_censored"),
        ("rejection"),
        ("full_G2"),
        ("adoption"),
        ("cost_transfer"),
        ("gate_emission_authorized"),
    ):
        require(outcome[key] is False, "Terminal retains exploratory scope and no failure")
    require(outcome["new_test_credit"] == 0, "Terminal supplies zero new programme credit")
    source_clocks(outcome)
    return {
        "current_scoped_all20_certification_metadata_reconciled": True,
        "saved_precision": {"primary": 90, "independent": 130, "separate_witness_order": 112},
        "fixed_certified_statuses": expected_statuses,
        "complete25_snapshot_count": 25,
        "complete20_opaque_row_count": 20,
        "current_owned_count_including_manifest": 64,
        "source_complete_counts": AUDIT_COUNTS,
        "proof_payload_decompressed_or_recomputed": False,
        "saved_uncompressed_descriptor_verified_as_actual_payload": False,
        "retained_source_summary_budget": summary["budget"],
        "retained_source_outcome_budget": outcome["budget"],
        **flags(),
    }


def retain_failure(error):
    if not OUTPUT.is_dir():
        return
    try:
        budget()
        save(
            "failure.json",
            {
                "passed": False,
                "completed": False,
                "error_type": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(),
                **flags(),
            },
        )
    except BaseException:
        pass
    try:
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"partial_success_invalid":true,"new_test_credit":0,"new_scientific_evaluation":false,"full_G2":false,"adoption":false,"quantum_advantage":false}\n'
            )
    except OSError:
        pass


def flags():
    return {
        "exact_rational_certified_metadata_screen_only": True,
        "new_scientific_evaluation": False,
        "scientific_imports_or_proof_decompression": False,
        "new_test_credit": 0,
        "new_credited_gate_replays": 0,
        "new_price_samples": 0,
        "candidate_G2_absolute_stock_error_allocation": None,
        "candidate_G2_barrier_band_allocation": None,
        "candidate_feasibility": False,
        "actual_emitted_source_or_capped_schedule": False,
        "actual_gate_schedule_or_cost_verified": False,
        "gate_emission_authorized": False,
        "financial_gate_emission_authorized": False,
        "full_G2": False,
        "adoption": False,
        "cost_transfer": False,
        "quantum_advantage": False,
        "old_failed_source_mathematical_PASS": False,
        "old_V5_and_partial_A20_failures_approved": False,
        "historical_global_LIVE_integrity_approved": False,
        "nested_historical_manifests_admitted_as_success": False,
        "held_A13_null_allocation_fields_changed": False,
        "local_only": True,
    }


def packet(name, pin, counts, schema, owned_contract, terminal_header=True):
    directory = canonical(PROGRAM / name)
    manifest = bind(directory / "manifest.json", pin)
    data = read(manifest)
    require(
        data["schema"] == schema and data["manifest_self_hash_excluded"] is True,
        "Exact externally pinned owner schema and self-excluded manifest",
    )
    require(
        [len(data[k]) for k in ("files", "frozen_inputs", "external_runtime_inputs")] == counts,
        "Complete original owner maps without reduced index",
    )
    if terminal_header:
        require(
            data["completed"] is True
            and data["passed"] is True
            and data["budget_censored"] is False,
            "Actual completed owner, never partial success",
        )
    no_failure(directory)
    members = {manifest}
    for field in ("files", "frozen_inputs", "external_runtime_inputs"):
        mapping = data[field]
        require(type(mapping) is dict, "Typed complete owner map")
        for key, expected in mapping.items():
            budget()
            if field == "external_runtime_inputs":
                require(type(key) is str and Path(key).is_absolute(), "Exact absolute external key")
                path = Path(key)
            else:
                exact_relative(key)
                path = (
                    directory / key
                    if field == "files" and owned_contract == "receipt"
                    else ROOT / key
                )
            actual = bind(path, expected)
            if field == "files":
                require(
                    actual.is_relative_to(directory) and actual not in members,
                    "Complete unique physically confined owner member",
                )
                required = (
                    actual.relative_to(directory).as_posix()
                    if owned_contract == "receipt"
                    else actual.relative_to(ROOT).as_posix()
                )
                require(required == key, "Exact original owner spelling")
                members.add(actual)
            elif field == "frozen_inputs":
                require(
                    actual.is_relative_to(ROOT) and actual.relative_to(ROOT).as_posix() == key,
                    "Exact ROOT-relative original input expectation",
                )
            else:
                require(
                    not actual.is_relative_to(ROOT) and str(actual) == key,
                    "Exact original absolute external expectation",
                )
    require(
        inventory(directory) == members and len(members) == counts[0] + 1,
        "Full physical owner membership plus manifest",
    )
    _OWN_INVENTORIES[directory] = members
    return data


def rational(value):
    budget()
    require(
        type(value) is list and len(value) == 2 and all(type(v) is int for v in value),
        "Canonical exact rational integer pair, never floats or booleans",
    )
    require(
        value[1] > 0 and all(abs(v).bit_length() <= MAX_SCALAR_BITS for v in value),
        "Positive denominator and prospective2048-bit saved scalar cap",
    )
    result = Fraction(value[0], value[1])
    require([result.numerator, result.denominator] == value, "Original reduced rational schema")
    budget()
    return result


def pair(value):
    budget()
    result = [value.numerator, value.denominator]
    require(
        all(abs(v).bit_length() <= MAX_RESULT_BITS for v in result),
        "Finite8192-bit derived pair fits original4300-digit JSON policy",
    )
    return result


def allocation_binding():
    source = PROGRAM / ALLOCATION_PACKETS[0][0]
    auditor = PROGRAM / ALLOCATION_PACKETS[1][0]
    root_owner = PROGRAM / ALLOCATION_PACKETS[2][0]
    primary = read(source / "summary.json")
    audit = read(auditor / "summary.json")
    root = read(root_owner / "summary.json")
    authorization = read(auditor / "primary_allocation_authorization.json")
    polynomial = read(source / "uniform_poly_allowance.json")
    require(
        primary["schema"] == "a13-fixed-alpha-allocation-producer-summary-v1"
        and audit["schema"] == "a13-fixed-alpha-allocation-auditor-summary-v1"
        and root["schema"] == "root-exp-frontier-fixed-alpha-fresh-integrity-v2",
        "Exact original primary90/independent130/ROOT allocation summaries",
    )
    for document in (primary, audit, root):
        require(
            document["completed"] is True
            and document["passed"] is True
            and document["budget_censored"] is False
            and document["conditional_allocation_release_eligible"] is True
            and document["alpha"] == ALPHA
            and document["conditional_E_allow_lower"] == ALLOWANCE,
            "Same externally approved fixed-alpha and exact primary-owned positive allowance",
        )
    require(
        audit["independent_allocation_audit_passed"] is True
        and audit["actual_source_manifest_sha256"] == ALLOCATION_PACKETS[0][1]
        and root["actual_primary90_and_independent130_terminal_PASS"] is True
        and root["primary_manifest_sha256"] == ALLOCATION_PACKETS[0][1]
        and root["audit_manifest_sha256"] == ALLOCATION_PACKETS[1][1],
        "Actual independent certification and ROOT input binding",
    )
    require(
        authorization["independent130_authorizes_complete_primary90_result"] is True
        and authorization["conditional_allocation_release_eligible"] is True
        and authorization["source_manifest_sha256"] == ALLOCATION_PACKETS[0][1]
        and authorization["approved_primary_E_allow_lower"] == ALLOWANCE
        and authorization["new_fixture_credit"] == 0,
        "Exact primary lower allowance independently authorized, no own-lower substitution",
    )
    require(
        polynomial["schema"] == "a13-fixed-alpha-native-poly-allowance-v1"
        and polynomial["interval_digits"] == 90
        and polynomial["alpha"] == ALPHA
        and polynomial["E_allow_lower"] == ALLOWANCE
        and polynomial["all_nonempty_allowances_strict_positive"] is True
        and polynomial["allowance_is_outward_lower_not_polynomial_error_upper"] is True
        and polynomial["candidate_quantization_all_internal_floors_and_full_realization_must_fit"]
        is True
        and polynomial["final_shift_floor_paid_separately"] == [1, 1 << 40],
        "Primary scalar premise separates polynomial, reduction and final shift budgets",
    )
    allowance = rational(ALLOWANCE)
    require(
        0 < allowance <= rational(authorization["independent_own_release_lower"]),
        "Strict positive primary lower bound never replaced by tighter independent result",
    )
    for document in (primary, audit):
        require(
            document["both_financial_residual_fit"] is True
            and document["all_nonempty_allowances_strict_positive"] is True,
            "Both unchanged original contracts retain allocation premise",
        )
        for key in (
            "full_G2",
            "adoption",
            "cost_transfer",
            "quantum_advantage",
            "actual_candidate_G2_feasibility_established",
        ):
            require(
                document[key] is False, "Original allocation is conditional, not changed-source G2"
            )
    return allowance


def failed_material_witness(initial=False):
    global _FAILED_MATERIAL_MEMBERS, _FAILED_MATERIAL_BYTES
    record = read(METADATA_SOURCE / "material_inventory.json")
    require(
        record["schema"] == "a13-exp-frontier-untrusted-material-inventory-v1"
        and record["material_receipt"] == MATERIAL.relative_to(ROOT).as_posix()
        and record["original_terminal_failure_authoritative"] is True
        and record["original_manifest_absent"] is True
        and record["exact_file_count"] == 42
        and record["original_file_bytes"] == 243935317,
        "Full original42 failed-owned bytes remain failed, not adopted",
    )
    mapping = record["files"]
    require(type(mapping) is dict and len(mapping) == 42, "Exact failed material inventory")
    members, total = set(), 0
    for key, entry in mapping.items():
        budget()
        exact_relative(key)
        path = MATERIAL / key
        require(
            entry["ROOT_relative_path"] == path.relative_to(ROOT).as_posix()
            and _FROZEN.get(entry["ROOT_relative_path"]) == entry["sha256"],
            "Failed input inherits original prospective expected SHA, no observed substitution",
        )
        actual = canonical(path)
        require(
            actual.is_relative_to(MATERIAL)
            and actual not in members
            and actual.is_file()
            and type(entry["bytes"]) is int
            and entry["bytes"] >= 0
            and actual.stat().st_size == entry["bytes"],
            "Complete failed-owned physical member",
        )
        members.add(actual)
        total += entry["bytes"]
    require(
        inventory(MATERIAL) == members
        and total == 243935317
        and (MATERIAL / "FAILED_UNSEALED.json").is_file()
        and not (MATERIAL / "manifest.json").exists()
        and not (MATERIAL / "manifest.json").is_symlink(),
        "Original authoritative failure and complete42 inventory remain unchanged",
    )
    if initial:
        _FAILED_MATERIAL_MEMBERS, _FAILED_MATERIAL_BYTES = members, total
    else:
        require(
            members == _FAILED_MATERIAL_MEMBERS and total == _FAILED_MATERIAL_BYTES,
            "Both union-side original failure inventories identical",
        )
    return {
        "files": len(members),
        "bytes": total,
        "authoritative_failed": True,
        "new_scientific_credit": 0,
    }


def selection_failure_witnesses():
    budget()
    require(
        inventory(PRIOR_SELECTION) == _SELECTION_FAILED_MEMBERS
        and len(_SELECTION_FAILED_MEMBERS) == 7
        and sum(fingerprint(path)[2] for path in _SELECTION_FAILED_MEMBERS) == 115343
        and (PRIOR_SELECTION / "FAILED_UNSEALED.json").is_file()
        and not (PRIOR_SELECTION / "manifest.json").exists()
        and not (PRIOR_SELECTION / "manifest.json").is_symlink(),
        "Original seven-file selector V1 stays failed, immutable and unapproved",
    )
    budget()


def admit_prior_selection_failure(ready, policy):
    expectations = {
        "prior_selector_failed_owned_freeze_SHA256": PRIOR_SELECTION_FREEZE_SHA,
        "prior_selector_READY_SHA256": PRIOR_SELECTION_READY_SHA,
        "prior_selector_log_SHA256": PRIOR_SELECTION_LOG_SHA,
        "prior_selector_author_SHA256": PRIOR_SELECTION_AUTHORS,
    }
    require(
        all(ready[key] == policy[key] == value for key, value in expectations.items()),
        "Externally frozen prior selector failure expectations without refresh",
    )
    record = read(bind(PRIOR_SELECTION_FREEZE, PRIOR_SELECTION_FREEZE_SHA))
    require(
        record["schema"] == "root-a13-certified-selection-v1-failed-owned-freeze-v1"
        and record["route"] == PRIOR_SELECTION.relative_to(ROOT).as_posix()
        and record["owned_file_count"] == 7
        and record["owned_bytes"] == 115343
        and record["manifest_absent"] is True
        and record["all_partial_results_unapproved"] is True
        and record["terminal_CPU_wall_uncertified"] is True
        and record["rational_selection_complete"] is False
        and record["fixture_credit"] == 0
        and record["observed_owned_expectations_do_not_replace_original_expected_hashes"] is True
        and record["READY_path"] == PRIOR_SELECTION_READY.relative_to(ROOT).as_posix()
        and record["READY_SHA256"] == PRIOR_SELECTION_READY_SHA
        and record["log_path"] == PRIOR_SELECTION_LOG.relative_to(ROOT).as_posix()
        and record["log_SHA256"] == PRIOR_SELECTION_LOG_SHA,
        "Exact ROOT-only frozen prior observed failure, no science approval",
    )
    mapping = record["owned_files"]
    require(
        type(mapping) is dict and len(mapping) == 7, "Complete prior observed-owned expected map"
    )
    for key, expected in mapping.items():
        exact_relative(key)
        path = bind(PRIOR_SELECTION / key, expected)
        require(
            path.is_relative_to(PRIOR_SELECTION)
            and path.relative_to(PRIOR_SELECTION).as_posix() == key
            and path not in _SELECTION_FAILED_MEMBERS,
            "Unique exact receipt-relative failed-owned membership",
        )
        _SELECTION_FAILED_MEMBERS.add(path)
    prior_ready = read(bind(PRIOR_SELECTION_READY, PRIOR_SELECTION_READY_SHA))
    require(
        prior_ready["schema"] == "root-a13-certified-candidate-selection-READY-v1"
        and prior_ready["author_method_SHA256"] == PRIOR_SELECTION_AUTHORS
        and prior_ready["output"] == PRIOR_SELECTION.relative_to(ROOT).as_posix(),
        "Every original executed author and original READY expectation retained",
    )
    for name, expected in PRIOR_SELECTION_AUTHORS.items():
        bind(RESEARCH / name, expected)
    bind(PRIOR_SELECTION_LOG, PRIOR_SELECTION_LOG_SHA)
    code_caches(
        [RESEARCH / "select_a13_certified_candidates_v1.py"],
        prior_ready["existing_new_code_cache_SHA256"],
        prior_ready["absent_new_code_cache_paths"],
    )
    marker = read(PRIOR_SELECTION / "FAILED_UNSEALED.json")
    failure = read(PRIOR_SELECTION / "failure.json")
    require(
        marker["passed"] is False
        and marker["completed"] is False
        and marker["hard_budget_state_uncertified"] is True
        and failure["passed"] is False
        and failure["completed"] is False,
        "Authoritative prior failure is never promoted by new selection",
    )
    selection_failure_witnesses()


def fit_round_metadata(fit, degree):
    rounds = fit["exchange_rounds"]
    require(
        type(rounds) is list and len(rounds) == 32,
        "Exactly32 original exchange record objects, not an integer count",
    )
    previous_nodes = None
    for number, record in enumerate(rounds, 1):
        budget()
        require(
            type(record) is dict
            and set(record)
            == {
                "round",
                "solve_nodes",
                "solved_coefficients",
                "solved_alternating_error",
                "candidate_stationary_brackets",
                "candidate_extrema",
                "candidate_residuals",
                "exact_exchange_bottleneck",
                "exact_two_pass_bottleneck_then_sum_lex",
                "selected_next_node_indices",
                "selected_next_nodes",
            }
            and type(record["round"]) is int
            and record["round"] == number
            and type(record["solve_nodes"]) is list
            and len(record["solve_nodes"]) == degree + 2
            and type(record["solved_coefficients"]) is list
            and len(record["solved_coefficients"]) == degree + 1
            and type(record["selected_next_nodes"]) is list
            and len(record["selected_next_nodes"]) == degree + 2
            and type(record["selected_next_node_indices"]) is list
            and len(record["selected_next_node_indices"]) == degree + 2
            and record["exact_two_pass_bottleneck_then_sum_lex"] is True,
            "Complete original ordered solve/exchange metadata remains exact",
        )
        require(
            previous_nodes is None or record["solve_nodes"] == previous_nodes,
            "Every original next solve uses the previous selected nodes, no hidden round",
        )
        previous_nodes = record["selected_next_nodes"]
    require(
        type(fit["coefficients_before_quantization"]) is list
        and len(fit["coefficients_before_quantization"]) == degree + 1
        and fit["coefficients_before_quantization"] == rounds[-1]["solved_coefficients"]
        and fit["coefficients_from_round32_solve"] is True
        and fit["extra33rd_solve"] is False
        and fit["root_search_fitting_evidence_only"] is True,
        "Original final32-solve coefficient anchor and authorized raw quantization unchanged",
    )


def admission(ready_sha):
    require(
        not os.environ.get("PYTHONINTMAXSTRDIGITS")
        and "int_max_str_digits" not in sys._xoptions
        and sys.get_int_max_str_digits() == 4300,
        "Original bounded4300-digit conversion policy, no environment or -X override",
    )
    ready = read(bind(READY, ready_sha))
    require(
        ready["schema"] == "root-a13-certified-candidate-selection-READY-v2"
        and ready["ready"] is True
        and ready["root_and_independent_static_reviews_passed"] is True
        and ready["local_only"] is True,
        "Separate prospective reviewed local selection release",
    )
    require(
        FINAL_ROOT_SHA is not None and FINAL_ROOT_COUNTS is not None,
        "Externally completed final ROOT receipt must be non-null before freeze",
    )
    require(
        ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and ready["audit_manifest_SHA256"] == AUDIT_SHA
        and ready["audit_complete_counts"] == AUDIT_COUNTS
        and ready["final_ROOT_manifest_SHA256"] == FINAL_ROOT_SHA
        and ready["final_ROOT_complete_counts"] == FINAL_ROOT_COUNTS
        and ready["metadata_source_manifest_SHA256"]
        == "e3c23aaa0697727952a7c979503424146c0224e8b2c8c32cff652974ab557dc9"
        and ready["fixed_alpha_allocation_packets"] == ALLOCATION_PACKETS
        and ready["fixed_alpha"] == ALPHA
        and ready["approved_primary_E_allow_lower"] == ALLOWANCE,
        "Exact externally declared six full-owner packets, same fixed allowance and caps",
    )
    for key in (
        "new_scientific_evaluation",
        "gate_emission_authorized",
        "financial_adoption",
        "full_G2",
        "cost_transfer",
        "quantum_advantage",
    ):
        require(
            ready[key] is False,
            "Only exact rational selection, no emission/adoption/advantage release",
        )
    require(ready["fixture_credit"] == 0, "No additional test credit")
    authors = ready["author_method_SHA256"]
    require(
        type(authors) is dict and set(authors) == {AUTHOR.name, METHOD_DOC.name, PREFLIGHT.name},
        "Exactly three externally frozen new selection bytes",
    )
    for name, pin in authors.items():
        bind(RESEARCH / name, pin)
    policy = read(PREFLIGHT)
    require(
        policy["schema"] == "a13-certified-candidate-selection-preflight-v2"
        and policy["author_SHA256"] == authors[AUTHOR.name]
        and policy["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and policy["owned_caps_files_bytes"] == [MAX_OWN_FILES, MAX_OWN_BYTES]
        and policy["runtime_caps_files_bytes"] == [MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES]
        and policy["bookkeeping_reference_unique_bytes_hash_work_caps"]
        == [MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK]
        and policy["grid"] == [list(row) for row in GRID]
        and policy["audit_manifest_SHA256"] == AUDIT_SHA
        and policy["audit_complete_counts"] == AUDIT_COUNTS
        and policy["final_ROOT_manifest_SHA256"] == FINAL_ROOT_SHA
        and policy["final_ROOT_complete_counts"] == FINAL_ROOT_COUNTS
        and policy["fixed_alpha_allocation_packets"] == ALLOCATION_PACKETS
        and policy["fixed_alpha"] == ALPHA
        and policy["approved_primary_E_allow_lower"] == ALLOWANCE
        and policy["maximum_global_shortlist"] == 2
        and policy["maximum_native_cell_metadata"] == MAX_NATIVE_CELLS
        and policy["rational_scalar_result_bit_caps"] == [MAX_SCALAR_BITS, MAX_RESULT_BITS],
        "Exact prospective fixed rule and finite metadata/rational bounds",
    )
    admit_prior_selection_failure(ready, policy)
    manifest = current_packet()
    source_protocol_checks(manifest)
    reconcile_metadata(manifest)
    packet(
        "A13_recovery_run001",
        "e3c23aaa0697727952a7c979503424146c0224e8b2c8c32cff652974ab557dc9",
        [16, 909, 2842],
        "a13-exp-frontier-recovery-terminal-manifest-v1",
        "receipt",
    )
    final = packet(
        FINAL_ROOT.name,
        FINAL_ROOT_SHA,
        FINAL_ROOT_COUNTS,
        "a13-recovery-audit-root-integrity-manifest-v6",
        "receipt",
    )
    require(
        final["audit_manifest_SHA256"] == AUDIT_SHA
        and final["audit_complete_counts"] == AUDIT_COUNTS
        and final["current_scoped_all20_certification_integrity_verified"] is True,
        "Actual final ROOT integrity of exact independent all20 receipt",
    )
    root_summary = read(FINAL_ROOT / "summary.json")
    require(
        root_summary["schema"] == "a13-recovery-audit-root-integrity-summary-v6"
        and root_summary["completed"] is True
        and root_summary["passed"] is True
        and root_summary["budget_censored"] is False
        and root_summary["audit_manifest_SHA256"] == AUDIT_SHA
        and root_summary["current_scoped_all20_certification_integrity_verified"] is True,
        "Completed final ROOT terminal, never old failure or foreign continuation substitution",
    )
    for args in ALLOCATION_PACKETS:
        packet(*args, terminal_header=args[0] != ALLOCATION_PACKETS[2][0])
    allocation_binding()
    audit_ready = read(bind(AUDIT_READY, AUDIT_READY_SHA))
    require(
        audit_ready["schema"] == "root-a13-recovery-audit-READY-v6"
        and audit_ready["author_method_SHA256"] == AUDIT_AUTHORS,
        "Original independent audit release retains exact original author bytes",
    )
    code_caches(
        [RESEARCH / "audit_exp_frontier_recovery_v6.py"],
        audit_ready["existing_new_code_cache_SHA256"],
        audit_ready["absent_new_code_cache_paths"],
    )
    old_root_ready = read(bind(FINAL_ROOT_READY, FINAL_ROOT_READY_SHA))
    require(
        old_root_ready["schema"] == "root-a13-recovery-audit-integrity-READY-v6"
        and old_root_ready["audit_manifest_SHA256"] == AUDIT_SHA,
        "Externally pinned actual final ROOT original release",
    )
    code_caches(
        [RESEARCH / "verify_a13_recovery_audit_root_v6.py"],
        old_root_ready["existing_new_code_cache_SHA256"],
        old_root_ready["absent_new_code_cache_paths"],
    )
    code_caches(
        [AUTHOR], ready["existing_new_code_cache_SHA256"], ready["absent_new_code_cache_paths"]
    )
    executables = {canonical(LAUNCHER), canonical(Path(sys._base_executable))}
    pinned = set()
    for spelling, expected in ready["interpreter_expected_SHA256"].items():
        actual = canonical(spelling)
        require(
            actual in executables and actual not in pinned,
            "Only actual distinct executable expected pins",
        )
        pinned.add(actual)
        bind(actual, expected)
    require(
        len(executables) == 2 and pinned == executables,
        "Both actual external interpreter expected pins",
    )
    failed_material_witness(initial=True)
    return manifest


def bounded_native_interval(value, width):
    budget()
    require(
        type(value) is list
        and len(value) == 2
        and all(type(v) is int for v in value)
        and value[0] <= value[1],
        "Exact inclusive native signed-word interval",
    )
    return -(1 << (width - 1)) <= value[0] <= value[1] < (1 << (width - 1))


def resource_binding(resource, domain, degree, segments, words):
    require(
        resource["schema"] == "a13-symbolic-resource-estimate-v1"
        and resource["degree"] == degree
        and resource["segments"] == segments
        and set(resource["cases"]) == set(BASELINES)
        and resource["arbitrary_phase_clean_XOR_ABI_still_requires_emitted_proof"] is True
        and resource["old_dead_paths_preserved"] is True
        and resource["full_financial_cost_not_divided_by_coordinates"] is True
        and resource["resource_adoption_or_realized_improvement_claim"] is False,
        "Same complete full72 symbolic resource premises, no actual source claim",
    )
    ratios, total_T, max_qubits = [], 0, 0
    cap_flags = {}
    for case, baseline in BASELINES.items():
        budget()
        item = resource["cases"][case]
        old = item["original_capped_source_resources"]
        whole = item["whole_source_resource_estimate"]
        qubits = item["whole_source_logical_qubit_upper"]
        require(
            old == domain["cases"][case]["baseline_capped_resources"]
            and item["original_serial_source_resources"]
            == domain["cases"][case]["baseline_serial_resources"]
            and [old["t_count"], old["t_depth"], old["logical_qubits"]] == baseline
            and item["original_logical_qubit_cap"] == baseline[2],
            "Exact original B4/B8 actual capped baseline and separate serial source",
        )
        require(
            all(type(whole[k]) is int and whole[k] >= 0 for k in whole)
            and type(qubits) is int
            and qubits > 0
            and item["estimated_qubit_upper_within_cap"] is (qubits <= baseline[2])
            and item["whole_candidate_clean_invocations"] == 2 * SITES[case][0]
            and item["global_forward_and_inverse_each_use_clean_candidate"] is True
            and item["estimated_serial_depth_not_realized_capped_schedule"] is True
            and item["exact7T_phase_paid"] is True
            and item["relative_phase_substitution"] is False
            and item["dynamic_selected_coefficient_constant_multiplier_discount"] is False
            and item["all_costs_are_estimates_until_emitted_ABI_and_capped_schedule_proofs"]
            is True,
            "Unchanged full copies/banks/forwardinverse/scratch/phase symbolic accounting",
        )
        require(
            item["coefficient_QROM_rows_raw"] == words,
            "Full center/coefficient QROM literal rows match certified fits",
        )
        require(
            type(item["full72_bank_inventory"]) is dict
            and all(type(v) is int and v >= 0 for v in item["full72_bank_inventory"].values())
            and item["full72_argument_copy_CX_per_forward"] >= 0
            and item["dirty_output_XOR_CX"] == 72
            and item["outer_function_argument_copy_CX_per_clean_invocation"] == 144,
            "All current full72 banks and argument/output-copy fields retained",
        )
        ratios.append(Fraction(whole["t_depth"], old["t_depth"]))
        total_T += whole["t_count"]
        max_qubits = max(max_qubits, qubits)
        cap_flags[case] = item["estimated_qubit_upper_within_cap"]
    return (max(ratios), total_T, max_qubits), cap_flags


def row_screen(actual, descriptor, domain, allowance):
    degree, segments, row_id = actual["degree"], actual["segments"], actual["row_id"]
    require(
        actual["status"] == descriptor["status"] == "CERTIFIED_ESTIMATE"
        and descriptor["degree"] == degree
        and descriptor["segments"] == segments
        and descriptor["row_id"] == row_id,
        "Exact certified original/independent row identity join",
    )
    certificate = actual["certificate"]
    fit_rows = actual["fit"]["segment_fits"]
    segment_rows = certificate["segments_certificate"]
    require(
        certificate["degree"] == degree
        and certificate["segments"] == segments
        and certificate["no_G2_allocation_or_feasibility_claim"] is True
        and certificate["realized_candidate_gate_or_ABI_proof"] is False
        and len(fit_rows) == len(segment_rows) == segments,
        "Exact originally approved fixed candidate, all actual segments, no emission proof",
    )
    words, uniform = [], {}
    native_valid = True
    for index, (fit, segment) in enumerate(zip(fit_rows, segment_rows, strict=True)):
        budget()
        fit_round_metadata(fit, degree)
        require(
            fit["segment"] == segment["segment"] == index
            and fit["degree"] == degree
            and fit["raw_bounds"] == segment["raw_bounds"]
            and fit["center_raw"] == segment["center_raw"]
            and fit["local_interval"] == segment["local_interval"]
            and fit["coefficients_from_round32_solve"] is True
            and fit["extra33rd_solve"] is False
            and fit["global_minimax_optimality_claim"] is False
            and segment["mesh_or_exchange_convergence_used_as_uniform_proof"] is False,
            "Unchanged actual32-round quantized candidate and closed uniform proof scalar",
        )
        raw = fit["coefficient_raw"]
        require(
            type(raw) is list
            and len(raw) == degree + 1
            and all(type(v) is int for v in raw)
            and type(fit["center_raw"]) is int,
            "Exact quantized literal coefficient and center inventory",
        )
        native_valid &= all(-(1 << 71) <= v < (1 << 71) for v in [fit["center_raw"], *raw])
        words.append([fit["center_raw"], *raw])
        uniform[index] = rational(segment["quantized_uniform_error_upper"])
        require(uniform[index] >= 0, "Certified quantized uniform polynomial error is nonnegative")
    plan = certificate["native_evaluation_plan"]
    require(
        plan["odd_term_carried_without_zero_pad"] is True
        and plan["unused_candidate_power_emitted"] is False
        and type(plan["nodes"]) is list
        and 0 < len(plan["nodes"]) <= MAX_IR_NODES,
        "Exact native candidate plan, no lowering or tree substitution",
    )
    seen, node_ops, muls = set(), {}, set()
    for node in plan["nodes"]:
        budget()
        value, op, args = node["value"], node["op"], node["args"]
        require(
            type(value) is int
            and value not in seen
            and op in {"local", "coefficient", "add", "mul"}
            and type(args) is list
            and all(type(v) is int and v in seen for v in args),
            "Exact bounded topological original typed plan",
        )
        require(
            len(args) == (2 if op in {"add", "mul"} else 0), "Exact original native operation arity"
        )
        seen.add(value)
        node_ops[value] = op
        if op == "mul":
            muls.add(value)
    require(plan["output"] in seen, "Actual native output remains in fixed plan")
    require(set(certificate["cases"]) == set(BASELINES), "Both fixed native cases required")
    cells, rejects, total = {}, [], 0
    for case in BASELINES:
        require(
            domain["cases"][case]["actual_stock_sites"] == SITES[case][0]
            and domain["cases"][case]["original_joint_pairs"] == SITES[case][1],
            "Original finance coordinate/site obligations retained",
        )
        intersections = certificate["cases"][case]["intersections"]
        require(
            len(intersections) == 30 * segments,
            "All occupied and empty original class/segment cells",
        )
        case_rows = []
        for cell, (k, segment_index) in zip(
            intersections, ((k, i) for k in range(-17, 13) for i in range(segments)), strict=True
        ):
            budget()
            total += 1
            require(
                total <= 2 * 30 * 8
                and cell["k"] == k
                and cell["segment"] == segment_index
                and type(cell["empty"]) is bool,
                "Exact ordered complete native class/segment cell inventory",
            )
            if cell["empty"]:
                case_rows.append({"k": k, "segment": segment_index, "empty": True})
                continue
            ranges, products = cell["native_intermediate_ranges"], cell["signed144_products"]
            require(
                type(ranges) is list
                and len(ranges) == len(seen)
                and len({v["value"] for v in ranges}) == len(seen)
                and {v["value"] for v in ranges} == seen
                and type(products) is list
                and len(products) == len(muls)
                and {v["value"] for v in products} == muls,
                "Every actual stored node and signed144 MUL witness retained",
            )
            cell_valid = cell["all_native72_product144_and_shift_guards_passed"] is True
            for item in ranges:
                budget()
                require(
                    item["op"] == node_ops[item["value"]]
                    and rational(item["native_floor_error_upper"]) >= 0,
                    "Original native value identity and floor-bound metadata",
                )
                cell_valid &= bounded_native_interval(item["raw_bounds"], 72)
            for item in products:
                budget()
                cell_valid &= bounded_native_interval(item["product_raw_bounds"], 144)
            cell_valid &= bounded_native_interval(cell["native_polynomial_raw_bounds"], 72)
            cell_valid &= bounded_native_interval(cell["stock_raw_bounds"], 72)
            native_valid &= cell_valid
            floor = rational(cell["native_floor_error_upper"])
            require(floor >= 0, "Certified actual native Estrin floors remain paid")
            bound = uniform[segment_index] + floor
            fits = bound <= allowance
            if not fits:
                rejects.append(
                    {
                        "case": case,
                        "k": k,
                        "segment": segment_index,
                        "reason": "POLYNOMIAL_PLUS_NATIVE_FLOORS_EXCEEDS_APPROVED_LOWER_ALLOWANCE",
                        "excess_exact": pair(bound - allowance),
                    }
                )
            if not cell_valid:
                rejects.append(
                    {
                        "case": case,
                        "k": k,
                        "segment": segment_index,
                        "reason": "NATIVE_72_144_OR_SHIFT_PROMISE_INVALID",
                    }
                )
            case_rows.append(
                {
                    "k": k,
                    "segment": segment_index,
                    "empty": False,
                    "quantized_uniform_error_upper": pair(uniform[segment_index]),
                    "native_floor_error_upper": pair(floor),
                    "polynomial_plus_floor_upper": pair(bound),
                    "approved_lower_allowance": ALLOWANCE,
                    "fits_lower_allowance": fits,
                    "native_metadata_valid": cell_valid,
                    "all_native72_product144_and_shift_guards_passed": cell[
                        "all_native72_product144_and_shift_guards_passed"
                    ],
                    "reduction_stock_error_upper_retained_separately": cell[
                        "reduction_stock_error_upper"
                    ],
                    "negative_shift_floor_upper_retained_separately": cell[
                        "negative_shift_floor_upper"
                    ],
                    "additive_stock_beta_upper_retained_separately": cell[
                        "additive_stock_beta_upper"
                    ],
                    "original_native_ranges_and_products_retained_as_full_input_SHA": True,
                }
            )
        require(
            any(not c["empty"] for c in case_rows), "Every fixed case has actual occupied cells"
        )
        cells[case] = case_rows
    if not native_valid and not any(
        x["reason"] == "NATIVE_72_144_OR_SHIFT_PROMISE_INVALID" for x in rejects
    ):
        rejects.append({"reason": "COEFFICIENT_OR_CENTER_SIGNED72_PROMISE_INVALID"})
    coordinates, cap_flags = resource_binding(
        actual["resource_estimate"], domain, degree, segments, words
    )
    eligible = native_valid and not rejects
    return {
        "degree": degree,
        "segments": segments,
        "row_id": row_id,
        "status": "CERTIFIED_ESTIMATE",
        "independent_opaque_row_descriptor": descriptor,
        "original_primary_row_SHA256": _FROZEN[
            (MATERIAL / "rows" / (row_id + ".json")).relative_to(ROOT).as_posix()
        ],
        "native_plan": plan,
        "all_quantized_center_coefficient_words": words,
        "all_native_metadata_promises_valid": native_valid,
        "error_and_native_eligible_for_contract_consideration": eligible,
        "all_case_cell_decisions": cells,
        "rejections": rejects,
        "symbolic_ranking_coordinates": [pair(coordinates[0]), coordinates[1], coordinates[2]],
        "exact_original_full72_resource_estimate": actual["resource_estimate"],
        "estimated_qubit_upper_within_original_caps": cap_flags,
        "all_estimated_qubit_uppers_within_caps": all(cap_flags.values()),
        "conservative_serial_upper_above_cap_proves_infeasible": False,
        "eligible_for_future_gate_release_review": eligible,
        "future_gate_release_requires_new_exact_source_ABI_capped_schedule_and_candidate_G2": True,
        "gate_execution_authorized_by_selection": False,
        **flags(),
    }, coordinates


def selection_screen():
    allowance = allocation_binding()
    index = read(AUDIT / "fixed_inventory_authorization.json")
    domain = read(MATERIAL / "source_domain_binding.json")
    require(
        domain["schema"] == "a13-source-domain-binding-v1"
        and domain["fixed30_classes_retained"] is True
        and domain["generic_zero_to_ln2_domain_assumed"] is False
        and domain["source_or_gate_array_executed"] is False
        and domain["inverse_ln2_word"] == 1586259972792
        and domain["ln2_word"] == 762123384786,
        "Already independently approved original raw-log/reduction/native source binding",
    )
    frontier = read(MATERIAL / "function_frontier.json")
    require(
        frontier["schema"] == "a13-function-frontier-v1"
        and frontier["all_costs_symbolic_estimates"] is True
        and frontier["feasible_candidates_not_selected"] is True
        and frontier["gate_emission_authorized"] is False
        and frontier["candidate_G2_absolute_stock_error_allocation"] is None
        and frontier["candidate_G2_barrier_band_allocation"] is None,
        "Original held allocation-free screen remains unchanged",
    )
    require(
        frontier["original_capped_baseline_resources"]
        == {case: domain["cases"][case]["baseline_capped_resources"] for case in BASELINES},
        "Same actual capped baselines retained separately from serial estimates",
    )
    descriptors = index["independent_row_artifacts"]
    require(
        len(descriptors) == len(frontier["rows"]) == 20,
        "Exactly20 fixed original and independent rows",
    )
    results, eligible, cell_count = [], [], 0
    for descriptor, cost, (degree, segments) in zip(
        descriptors, frontier["rows"], GRID, strict=True
    ):
        budget()
        row_id = f"d{degree}_s{segments}"
        require(
            descriptor["row_id"] == cost["row_id"] == row_id
            and descriptor["degree"] == cost["degree"] == degree
            and descriptor["segments"] == cost["segments"] == segments
            and cost["status"] == "CERTIFIED_ESTIMATE",
            "Same ordered whole-cost and approved row",
        )
        actual = read(MATERIAL / "rows" / (row_id + ".json"))
        require(
            actual["resource_estimate"] == cost["resource_estimate"],
            "Actual certified primary resource payload equals same original aggregate",
        )
        result, coordinates = row_screen(actual, descriptor, domain, allowance)
        cell_count += sum(len(v) for v in result["all_case_cell_decisions"].values())
        require(cell_count <= MAX_NATIVE_CELLS, "Fixed maximum9600 class-cell metadata comparisons")
        results.append(result)
        if result["error_and_native_eligible_for_contract_consideration"]:
            eligible.append((result, coordinates))
    nondominated = []
    for row, point in eligible:
        budget()
        dominated = any(
            all(other[j] <= point[j] for j in range(3))
            and any(other[j] < point[j] for j in range(3))
            for other_row, other in eligible
            if other_row["row_id"] != row["row_id"]
        )
        if not dominated:
            nondominated.append((row, point))
    ordered = sorted(
        nondominated, key=lambda item: (*item[1], item[0]["degree"], item[0]["segments"])
    )
    shortlist = [row["row_id"] for row, _ in ordered[:2]]
    selected = set(shortlist)
    for row in results:
        row["shortlisted_for_future_contract_consideration"] = row["row_id"] in selected
    return {
        "schema": "a13-certified-exact-rational-candidate-selection-v1",
        "row_count": 20,
        "native_cell_count": cell_count,
        "eligible_row_ids": [row["row_id"] for row, _ in eligible],
        "nondominated_ordered_row_ids": [row["row_id"] for row, _ in ordered],
        "maximum_global_architecture_slots": 2,
        "shortlist_row_ids": shortlist,
        "decision": "SHORTLIST_FOR_FUTURE_CONTRACT_REVIEW" if shortlist else "NO_CANDIDATE",
        "failed_selected_architecture_consumes_its_slot": True,
        "fallback_third_architecture_or_outcome_sensitive_retry": False,
        "fixed_alpha": ALPHA,
        "approved_primary_E_allow_lower": ALLOWANCE,
        "ranking": [
            "max_B4_B8_symbolic_serial_T_depth_to_actual_capped_baseline_ratio",
            "sum_B4_B8_symbolic_whole_T_counts",
            "max_B4_B8_symbolic_qubit_upper",
            "degree",
            "segments",
        ],
        (
            "serial_to_capped_ratios_are_symbolic_ranking_coordinates_not_realized_depth_comparisons"
        ): True,
        "no_universal_impossibility_or_advantage_conclusion": True,
        "baseline_T_count_depth_qubit_caps": BASELINES,
        "primary_original_claims_authorized_only_by_actual_independent130_all20_audit": True,
        "original_failed_material_still_failed": True,
        "opaque_gzip_payload_read_or_decompressed": False,
        "new_fitting_quantization_range_induction_or_resource_reconstruction": False,
        "rows": results,
        **flags(),
    }


def main():
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256", required=True)
    args = parser.parse_args()
    require(
        canonical(__file__) == AUTHOR and not OUTPUT.exists(),
        "Single fresh selection route, no retry",
    )
    try:
        admission(args.ready_sha256)
        runtime = own_runtime()
        loaded_origins()
        check_code_caches()
        saved_before = saved_runtime_membership()
        failed_material_witness()
        selection_failure_witnesses()
        first = fresh_union()
        require(
            saved_runtime_membership() == saved_before,
            "Complete source runtime unchanged across first fresh union",
        )
        failed_material_witness()
        selection_failure_witnesses()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        for path in (AUTHOR, METHOD_DOC, PREFLIGHT, READY):
            copy(path, "executed_" + path.name)
        save(
            "run_started.json",
            {
                "created_UTC": datetime.now(timezone.utc).isoformat(),
                "PID": os.getpid(),
                "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
                **flags(),
            },
        )
        for path in (
            PRIOR_SELECTION_FREEZE,
            PRIOR_SELECTION_READY,
            PRIOR_SELECTION_LOG,
            *(RESEARCH / name for name in PRIOR_SELECTION_AUTHORS),
        ):
            copy(path, "prior_selector_" + path.name)
        report = selection_screen()
        save("all20_candidate_selection.json", report)
        loaded_origins()
        check_code_caches()
        require(
            saved_runtime_membership() == saved_before,
            "Complete saved source runtime remains exact",
        )
        failed_material_witness()
        selection_failure_witnesses()
        second = fresh_union()
        require(
            saved_runtime_membership() == saved_before,
            "Complete source runtime unchanged across second fresh union",
        )
        failed_material_witness()
        selection_failure_witnesses()
        summary = {
            "schema": "a13-certified-candidate-selection-summary-v2",
            "completed": True,
            "passed": True,
            "prior_selector_failure_unapproved": True,
            "prior_selector_failed_owned_freeze_SHA256": PRIOR_SELECTION_FREEZE_SHA,
            "budget_censored": False,
            "audit_manifest_SHA256": AUDIT_SHA,
            "audit_complete_counts": AUDIT_COUNTS,
            "final_ROOT_manifest_SHA256": FINAL_ROOT_SHA,
            "final_ROOT_complete_counts": FINAL_ROOT_COUNTS,
            "all20_rows_retained": True,
            "shortlist_row_ids": report["shortlist_row_ids"],
            "decision": report["decision"],
            "fixed_alpha": ALPHA,
            "approved_primary_E_allow_lower": ALLOWANCE,
            "both_full_uncached_input_unions": [first, second],
            "current_runtime": runtime,
            "budget": {
                "process_CPU_seconds": time.process_time(),
                "wall_seconds": time.monotonic() - _STARTED,
            },
            "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
            **flags(),
        }
        save("summary.json", summary)
        save("completion_outcome.json", {**summary, "failed": False})
        owned, total = {}, 0
        for path in sorted(inventory(OUTPUT)):
            budget()
            total += path.stat().st_size
            require(
                len(owned) < MAX_OWN_FILES - 1 and total <= MAX_OWN_BYTES, "Inclusive owned reserve"
            )
            owned[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
        complete_manifest(
            {
                "schema": "a13-certified-candidate-selection-manifest-v2",
                "files": owned,
                "frozen_inputs": _FROZEN,
                "external_runtime_inputs": _EXTERNAL,
                "manifest_self_hash_excluded": True,
                "prior_selector_failure_unapproved": True,
                "prior_selector_failed_owned_freeze_SHA256": PRIOR_SELECTION_FREEZE_SHA,
                "completed": True,
                "passed": True,
                "budget_censored": False,
                "audit_manifest_SHA256": AUDIT_SHA,
                "audit_complete_counts": AUDIT_COUNTS,
                "final_ROOT_manifest_SHA256": FINAL_ROOT_SHA,
                "final_ROOT_complete_counts": FINAL_ROOT_COUNTS,
                "both_full_uncached_input_unions": [first, second],
                "terminal_budget_observation": {
                    "process_CPU_seconds": time.process_time(),
                    "wall_seconds": time.monotonic() - _STARTED,
                },
                **flags(),
            },
            owned,
            total,
        )
        budget()
        print(
            json.dumps(
                {
                    "passed": True,
                    "manifest_SHA256": digest(OUTPUT / "manifest.json", fresh=True),
                    "shortlist_row_ids": report["shortlist_row_ids"],
                    **flags(),
                }
            ),
            flush=True,
        )
    except BaseException as error:
        retain_failure(error)
        raise


if __name__ == "__main__":
    main()
