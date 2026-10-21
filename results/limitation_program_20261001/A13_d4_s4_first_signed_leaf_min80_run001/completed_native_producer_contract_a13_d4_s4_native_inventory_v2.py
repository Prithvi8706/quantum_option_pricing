"""Unexecuted sole-row A13 d4_s4 exact native contract inventory.

No fitting, gzip decompression, scientific imports, gate emission or cost claim.
Fresh native proofs require separate ROOT release; original G2 does not transfer.
"""

import argparse
import ast
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
AUTHOR = RESEARCH / "contract_a13_d4_s4_native_inventory_v2.py"
METHOD_DOC = RESEARCH / "A13_D4_S4_NATIVE_CONTRACT_INVENTORY_PREFLIGHT_V2.md"
PREFLIGHT = RESEARCH / "a13_d4_s4_native_contract_inventory_preflight_v2.json"
READY = ROOT / ".context/A13_D4_S4_NATIVE_CONTRACT_INVENTORY_ROOT_READY_run002.json"
OUTPUT = PROGRAM / "A13_d4_s4_native_contract_inventory_run002"
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
MAX_NATIVE_CELLS = 240
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



INVENTORY_MODULE = "research.limitation_program_20261001.contract_a13_d4_s4_native_inventory_v2"
RUNTIME_INVOCATION = ["-B", "-m", INVENTORY_MODULE]
PRIOR_INVENTORY = PROGRAM / "A13_d4_s4_native_contract_inventory_run001"
PRIOR_INVENTORY_WITNESS = ROOT / ".context/A13_D4_S4_NATIVE_INVENTORY_V1_PREFIT_FAILURE_WITNESS_run001.json"
PRIOR_INVENTORY_WITNESS_SHA = "28e2a90043b4ce9fb943bd7ae81b28008010e8395a34938c8f1c4c5755fdf502"
PRIOR_INVENTORY_READY = ROOT / ".context/A13_D4_S4_NATIVE_CONTRACT_INVENTORY_ROOT_READY_run001.json"
PRIOR_INVENTORY_READY_SHA = "4da4681c4e8e27725c14ae58c87c83e409a5f2ae60c32f733e0dbebdbb20f4e6"
PRIOR_INVENTORY_LOG = ROOT / ".context/a13_d4_s4_native_contract_inventory_run001.log"
PRIOR_INVENTORY_LOG_SHA = "b5863e9ca7fe621eebef0a381aad0126332639afaacbf85683166d46b8f47e5e"
PRIOR_INVENTORY_AUTHORS = {
    "contract_a13_d4_s4_native_inventory_v1.py": "11cb6c88511101bd19ab348eb5dd6c031274c350a5dea3f97a9e154dacae3d51",
    "A13_D4_S4_NATIVE_CONTRACT_INVENTORY_PREFLIGHT_V1.md": "2667c373f70e166c6319678c8acf8aa4242af759b5029df0a919255a2b72cf4f",
    "a13_d4_s4_native_contract_inventory_preflight_v1.json": "192589cad03a24b2cccbef49a20d19151f112c72bbb8c16a94eff8ed96a03593",
}

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
        "exact_integer_native_contract_inventory_only": True,
        "new_scientific_evaluation": True,
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


ROW_ID = "d4_s4"
SELECTOR = PROGRAM / "A13_certified_candidate_selection_run002"
SELECTOR_SHA = "81e4403e7cacf6396da6559d4bf94332522f0d2c2fa63d7b81fddd5d2658544e"
SELECTOR_COUNTS = [14, 1521, 2842]
SELECTOR_READY = ROOT / ".context/A13_CERTIFIED_CANDIDATE_SELECTION_ROOT_READY_run002.json"
SELECTOR_READY_SHA = "681b95ef4129b3c1a2f5e22071dca1439f293c50befad3c2a95cddacb2870445"
SELECTOR_RESULT_REVIEW = ROOT / ".context/A13_CERTIFIED_SELECTION_V2_ROOT_RESULT_REVIEW_run001.json"
SELECTOR_RESULT_REVIEW_SHA = "c6912bce8108d05668020895882e4985db35f610f869a120ed2ea9c501d4d9a0"
SELECTOR_AUTHORS = {
    "select_a13_certified_candidates_v2.py": "a99b3bcb04c76239f6c7f3a1a76bccba864c795f6473334796eb857e597adc27",
    "A13_CERTIFIED_CANDIDATE_SELECTION_PREFLIGHT_V2.md": "28caf7ff51c4641e3a2565d96ad4b6a6d37c3dacec3889d84299f444cc40aa55",
    "a13_certified_candidate_selection_preflight_v2.json": "f9505fe30ae015287e291e68836cbe744c62f30308c4cce1f28f3a4f3e6edcd5",
}
W, Q = 72, 1 << 40
FIXED_PLAN = {
    "nodes": [
        {"value": 0, "op": "local", "args": []},
        {"value": 1, "op": "coefficient", "args": [], "degree": 0},
        {"value": 2, "op": "coefficient", "args": [], "degree": 1},
        {"value": 3, "op": "coefficient", "args": [], "degree": 2},
        {"value": 4, "op": "coefficient", "args": [], "degree": 3},
        {"value": 5, "op": "coefficient", "args": [], "degree": 4},
        {"value": 6, "op": "mul", "args": [0, 2]},
        {"value": 7, "op": "add", "args": [1, 6]},
        {"value": 8, "op": "mul", "args": [0, 4]},
        {"value": 9, "op": "add", "args": [3, 8]},
        {"value": 10, "op": "mul", "args": [0, 0]},
        {"value": 11, "op": "mul", "args": [10, 9]},
        {"value": 12, "op": "add", "args": [7, 11]},
        {"value": 13, "op": "mul", "args": [10, 10]},
        {"value": 14, "op": "mul", "args": [13, 5]},
        {"value": 15, "op": "add", "args": [12, 14]},
    ],
    "output": 15,
    "odd_term_carried_without_zero_pad": True,
    "unused_candidate_power_emitted": False,
}


def check(started):
    budget()



def runtime_invocation_guard(ready_sha):
    require(
        __name__ == "__main__"
        and __package__ == "research.limitation_program_20261001"
        and __spec__ is not None
        and __spec__.name == INVENTORY_MODULE
        and canonical(__spec__.origin) == AUTHOR
        and sys.orig_argv[1:] == RUNTIME_INVOCATION + ["--ready-sha256", ready_sha]
        and sys.flags.isolated == 0
        and sys.flags.no_site == 0
        and sys.flags.ignore_environment == 0
        and sys.flags.safe_path is False
        and sys.flags.dont_write_bytecode == 1
        and sys.dont_write_bytecode is True
        and canonical(Path.cwd()) == ROOT
        and sys.path[0] == str(ROOT),
        "Exact original-runtime-compatible -B -m invocation from workspace root",
    )


def prior_inventory_failure_witness():
    budget()
    require(
        canonical(PRIOR_INVENTORY.parent) == PROGRAM
        and PRIOR_INVENTORY.resolve(strict=False) == PRIOR_INVENTORY
        and not PRIOR_INVENTORY.exists()
        and not PRIOR_INVENTORY.is_symlink(),
        "Original pre-output inventory failure route remains physically wholly absent",
    )
    for path, expected in (
        (PRIOR_INVENTORY_WITNESS, PRIOR_INVENTORY_WITNESS_SHA),
        (PRIOR_INVENTORY_READY, PRIOR_INVENTORY_READY_SHA),
        (PRIOR_INVENTORY_LOG, PRIOR_INVENTORY_LOG_SHA),
        *((RESEARCH / name, expected) for name, expected in PRIOR_INVENTORY_AUTHORS.items()),
    ):
        require(
            digest(path, fresh=True) == expected,
            "Every original pre-output failure byte retains its ROOT expected SHA",
        )
    witness = read(PRIOR_INVENTORY_WITNESS)
    require(
        witness == {
            "schema": "root-a13-d4-s4-native-inventory-v1-prefit-failure-witness-v1",
            "actual_failed_before_output_creation": True,
            "all_scientific_results_unapproved": True,
            "failure_observed": "Exact original base/prefix/search/source-runtime scope, no scientific import",
            "invocation": "-I -S -B research/limitation_program_20261001/contract_a13_d4_s4_native_inventory_v1.py --ready-sha256 " + PRIOR_INVENTORY_READY_SHA,
            "metadata_only": True,
            "native_inventory_scientific_execution_started": False,
            "new_fixture_credit": 0,
            "original_READY_expected_SHA256": PRIOR_INVENTORY_READY_SHA,
            "original_READY_path": PRIOR_INVENTORY_READY.relative_to(ROOT).as_posix(),
            "original_author_expected_SHA256": PRIOR_INVENTORY_AUTHORS,
            "original_expected_hashes_or_runtime_scope_waived": False,
            "original_log_SHA256": PRIOR_INVENTORY_LOG_SHA,
            "original_log_path": PRIOR_INVENTORY_LOG.relative_to(ROOT).as_posix(),
            "output_route": PRIOR_INVENTORY.relative_to(ROOT).as_posix(),
            "output_route_absent": True,
            "passed": False,
            "terminal_CPU_wall_uncertified": True,
        },
        "Exact ROOT-only pre-output failure record with no partial scientific approval",
    )
    budget()


def admit_prior_inventory_failure(ready, policy):
    expectations = {
        "prior_inventory_failure_witness_SHA256": PRIOR_INVENTORY_WITNESS_SHA,
        "prior_inventory_READY_SHA256": PRIOR_INVENTORY_READY_SHA,
        "prior_inventory_log_SHA256": PRIOR_INVENTORY_LOG_SHA,
        "prior_inventory_author_SHA256": PRIOR_INVENTORY_AUTHORS,
        "prior_inventory_output_route_absent": True,
        "runtime_invocation": RUNTIME_INVOCATION,
        "original_runtime_scope_and_expected_SHA_checks_waived": False,
    }
    require(
        all(ready[key] == policy[key] == expected for key, expected in expectations.items()),
        "Externally frozen failed V1 bytes and exact compatible V2 launch without waiver",
    )
    for path, expected in (
        (PRIOR_INVENTORY_WITNESS, PRIOR_INVENTORY_WITNESS_SHA),
        (PRIOR_INVENTORY_READY, PRIOR_INVENTORY_READY_SHA),
        (PRIOR_INVENTORY_LOG, PRIOR_INVENTORY_LOG_SHA),
        *((RESEARCH / name, expected) for name, expected in PRIOR_INVENTORY_AUTHORS.items()),
    ):
        bind(path, expected)
    prior_ready = read(PRIOR_INVENTORY_READY)
    require(
        prior_ready["schema"] == "root-a13-d4-s4-native-contract-inventory-READY-v1"
        and prior_ready["author_method_SHA256"] == PRIOR_INVENTORY_AUTHORS
        and prior_ready["output"] == PRIOR_INVENTORY.relative_to(ROOT).as_posix()
        and prior_ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and prior_ready["audit_manifest_SHA256"] == AUDIT_SHA
        and prior_ready["audit_complete_counts"] == AUDIT_COUNTS
        and prior_ready["final_ROOT_manifest_SHA256"] == FINAL_ROOT_SHA
        and prior_ready["final_ROOT_complete_counts"] == FINAL_ROOT_COUNTS
        and prior_ready["approved_primary_E_allow_lower"] == ALLOWANCE,
        "Original executed V1 release and all its expected source premises are immutable",
    )
    code_caches(
        [RESEARCH / "contract_a13_d4_s4_native_inventory_v1.py"],
        prior_ready["existing_new_code_cache_SHA256"],
        prior_ready["absent_new_code_cache_paths"],
    )
    _ABSENT_RUNTIME.add(PRIOR_INVENTORY)
    prior_inventory_failure_witness()


def admission(ready_sha):
    require(
        not os.environ.get("PYTHONINTMAXSTRDIGITS")
        and "int_max_str_digits" not in sys._xoptions
        and sys.get_int_max_str_digits() == 4300,
        "Original bounded4300-digit conversion policy, no environment or -X override",
    )
    ready = read(bind(READY, ready_sha))
    require(
        ready["schema"] == "root-a13-d4-s4-native-contract-inventory-READY-v2"
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
        policy["schema"] == "a13-d4-s4-native-contract-inventory-preflight-v2"
        and policy["author_SHA256"] == authors[AUTHOR.name]
        and policy["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and policy["owned_caps_files_bytes"] == [MAX_OWN_FILES, MAX_OWN_BYTES]
        and policy["runtime_caps_files_bytes"] == [MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES]
        and policy["bookkeeping_reference_unique_bytes_hash_work_caps"]
        == [MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK]
        and policy["fixed_row_id"] == ROW_ID
        and policy["audit_manifest_SHA256"] == AUDIT_SHA
        and policy["audit_complete_counts"] == AUDIT_COUNTS
        and policy["final_ROOT_manifest_SHA256"] == FINAL_ROOT_SHA
        and policy["final_ROOT_complete_counts"] == FINAL_ROOT_COUNTS
        and policy["fixed_alpha_allocation_packets"] == ALLOCATION_PACKETS
        and policy["fixed_alpha"] == ALPHA
        and policy["approved_primary_E_allow_lower"] == ALLOWANCE
        and policy["fixed_class_segment_slots"] == 240
        and policy["maximum_native_cell_metadata"] == MAX_NATIVE_CELLS
        and policy["rational_scalar_result_bit_caps"] == [MAX_SCALAR_BITS, MAX_RESULT_BITS],
        "Exact prospective fixed rule and finite metadata/rational bounds",
    )
    admit_prior_inventory_failure(ready, policy)
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
    admit_completed_selector(ready, policy)
    return manifest


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


def independent_removal(target, source, sites, started):
    nodes = {node["out"][0]: node for node in target["nodes"]}
    endpoints = {site["polynomial"] for site in sites}
    boundaries = {site["remainder"] for site in sites}
    closure, pending = set(), list(endpoints)
    while pending:
        check(started)
        value = pending.pop()
        if value in boundaries or value in closure:
            continue
        node = nodes[value]
        require(
            node["op"] in ("const", "add", "mul") and len(node["out"]) == 1,
            "Actual original active polynomial closure",
        )
        closure.add(value)
        pending.extend(node["args"])
    replaceable_consumers = {site["stock"] for site in sites}
    retained = set()
    for value, node in nodes.items():
        check(started)
        if value not in closure and value not in replaceable_consumers:
            retained.update(argument for argument in node["args"] if argument in closure)
    changed = True
    while changed:
        check(started)
        changed = False
        for value in tuple(retained):
            for argument in nodes[value]["args"]:
                if argument in closure and argument not in retained:
                    retained.add(argument)
                    changed = True
    removable = closure - retained
    indices = [
        index for index, call in enumerate(source["forward_calls"]) if call["out"][0] in removable
    ]
    require(len(indices) == len(removable), "One actual removable forward call per SSA value")
    return dict(
        active_polynomial_value_ids=sorted(closure),
        retained_shared_or_dead_ancestor_value_ids=sorted(retained),
        removed_value_ids=sorted(removable),
        removed_forward_call_indices=indices,
        eager_unused_values_outside_closure_retained=True,
    )


"""Author-only exact native-contract functions; no author-time evaluation."""


def admit_completed_selector(ready, policy):
    expectations = {
        "completed_selector_manifest_SHA256": SELECTOR_SHA,
        "completed_selector_complete_counts": SELECTOR_COUNTS,
        "completed_selector_READY_SHA256": SELECTOR_READY_SHA,
        "completed_selector_author_SHA256": SELECTOR_AUTHORS,
        "completed_selector_ROOT_result_review_SHA256": SELECTOR_RESULT_REVIEW_SHA,
        "fixed_row_id": ROW_ID,
        "fixed_class_segment_slots": 240,
    }
    require(
        all(ready[key] == policy[key] == value for key, value in expectations.items()),
        "All separately externally expected sole-selector premises fixed before arithmetic",
    )
    require(
        ready["new_scientific_evaluation"] is True
        and ready["exact_native_contract_inventory_approved"] is True
        and policy["new_integer_native_range_induction"] is True
        and policy["new_fitting_quantization_exponential_or_gate_evaluation"] is False,
        "Separate release covers only fixed native interval induction and contract inventory",
    )
    manifest = packet(
        SELECTOR.name,
        SELECTOR_SHA,
        SELECTOR_COUNTS,
        "a13-certified-candidate-selection-manifest-v2",
        "receipt",
    )
    require(
        manifest["new_scientific_evaluation"] is False
        and manifest["candidate_feasibility"] is False
        and manifest["gate_emission_authorized"] is False
        and manifest["financial_gate_emission_authorized"] is False
        and manifest["full_G2"] is False
        and manifest["adoption"] is False
        and manifest["cost_transfer"] is False
        and manifest["new_test_credit"] == 0,
        "Completed selector grants metadata shortlist only, never leaf permission or credit",
    )
    old_ready = read(bind(SELECTOR_READY, SELECTOR_READY_SHA))
    require(
        old_ready["schema"] == "root-a13-certified-candidate-selection-READY-v2"
        and old_ready["author_method_SHA256"] == SELECTOR_AUTHORS
        and old_ready["output"] == SELECTOR.relative_to(ROOT).as_posix(),
        "Exact independently completed selector author/release bytes",
    )
    for name, expected in SELECTOR_AUTHORS.items():
        budget()
        require(
            manifest["frozen_inputs"][(RESEARCH / name).relative_to(ROOT).as_posix()] == expected,
            "Original complete selector expected source map retained",
        )
        bind(RESEARCH / name, expected)
    code_caches(
        [RESEARCH / "select_a13_certified_candidates_v2.py"],
        old_ready["existing_new_code_cache_SHA256"],
        old_ready["absent_new_code_cache_paths"],
    )
    bind(SELECTOR_RESULT_REVIEW, SELECTOR_RESULT_REVIEW_SHA)
    selector_result_witness()


def selector_result_witness():
    summary = read(SELECTOR / "summary.json")
    report = read(SELECTOR / "all20_candidate_selection.json")
    review = read(SELECTOR_RESULT_REVIEW)
    require(
        summary["schema"] == "a13-certified-candidate-selection-summary-v2"
        and summary["completed"] is True
        and summary["passed"] is True
        and summary["budget_censored"] is False
        and summary["shortlist_row_ids"] == [ROW_ID]
        and summary["audit_manifest_SHA256"] == AUDIT_SHA
        and summary["final_ROOT_manifest_SHA256"] == FINAL_ROOT_SHA
        and summary["fixed_alpha"] == ALPHA
        and summary["approved_primary_E_allow_lower"] == ALLOWANCE,
        "Externally completed sole-row shortlist and original lower allowance unchanged",
    )
    require(
        report["schema"] == "a13-certified-exact-rational-candidate-selection-v1"
        and report["row_count"] == 20
        and report["native_cell_count"] == 4500
        and report["shortlist_row_ids"] == report["nondominated_ordered_row_ids"] == [ROW_ID]
        and report["fixed_alpha"] == ALPHA
        and report["approved_primary_E_allow_lower"] == ALLOWANCE
        and len(report["eligible_row_ids"]) == 18
        and report["candidate_G2_absolute_stock_error_allocation"] is None
        and report["candidate_G2_barrier_band_allocation"] is None
        and report["gate_emission_authorized"] is False,
        "Complete original fixed selection is an expected input, never re-ranked",
    )
    require(
        review["schema"] == "root-a13-selection-v2-result-reconciliation-v1"
        and review["passed"] is True
        and review["manifest_expected_SHA256"] == SELECTOR_SHA
        and review["shortlist_row_ids"] == [ROW_ID]
        and review["rows"] == 20
        and review["all_cells"] == 4500
        and review["occupied_cells"] == 4200
        and review["eligible_row_ids"] == report["eligible_row_ids"]
        and review["full_input_map_runtime_rewalk_performed"] is False
        and review["scientific_proofs_or_gate_costs_recomputed"] is False
        and review["gate_emission_or_financial_adoption_authorized"] is False
        and review["fixture_credit"] == 0,
        "ROOT result reconciliation remains scoped metadata, no transferred live integrity or gate permission",
    )
    for document in (summary, report):
        require(
            all(
                document[key] is False
                for key in (
                    "full_G2",
                    "adoption",
                    "cost_transfer",
                    "quantum_advantage",
                    "gate_emission_authorized",
                    "financial_gate_emission_authorized",
                    "candidate_feasibility",
                )
            )
            and document["new_test_credit"] == 0,
            "All old selector no-adoption/financial/no-credit fields unchanged",
        )
    selected = [row for row in report["rows"] if row["row_id"] == ROW_ID]
    require(
        len(report["rows"]) == 20
        and len(selected) == 1
        and selected[0]["shortlisted_for_future_contract_consideration"] is True
        and selected[0]["error_and_native_eligible_for_contract_consideration"] is True
        and selected[0]["all_native_metadata_promises_valid"] is True
        and selected[0]["rejections"] == [],
        "One exact selected scientific premise, never another search architecture",
    )
    return selected[0]


def admitted_text_AST(path):
    global _HASH_WORK
    budget()
    actual = canonical(path, fresh=True)
    expected = _FROZEN.get(actual.relative_to(ROOT).as_posix())
    require(expected is not None, "Text AST source admitted from exact original expected map first")
    before = fingerprint(actual)
    require(before[2] <= 8 << 20 and actual.is_file(), "Finite source text AST admission")
    chunks, size = [], 0
    with actual.open("rb") as stream:
        while chunk := stream.read(65536):
            budget()
            size += len(chunk)
            _HASH_WORK += len(chunk)
            require(
                size <= before[2] and _HASH_WORK <= MAX_HASH_WORK,
                "Complete charged bounded source text read",
            )
            chunks.append(chunk)
    raw = b"".join(chunks)
    require(
        size == before[2]
        and fingerprint(actual) == before
        and hashlib.sha256(raw).hexdigest() == expected
        and canonical(path, fresh=True) == actual,
        "Fresh original source bytes before nonexecuting AST parse",
    )
    budget()
    tree = ast.parse(raw)
    budget()
    return {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}


def copied_metadata_provenance():
    own = admitted_text_AST(AUTHOR)
    old_selector = admitted_text_AST(RESEARCH / "select_a13_certified_candidates_v2.py")
    old_audit = admitted_text_AST(RESEARCH / "audit_exp_frontier_recovery_v6.py")
    for name, expected in (
        ("fit_round_metadata", old_selector["fit_round_metadata"]),
        ("independent_removal", old_audit["independent_removal"]),
    ):
        require(
            ast.dump(own[name], include_attributes=False)
            == ast.dump(expected, include_attributes=False),
            "Exact unexecuted original metadata/closure helper text, no source import",
        )
    budget()


def native_interval(bounds, width=72):
    budget()
    require(
        type(bounds) is list
        and len(bounds) == 2
        and all(type(value) is int for value in bounds)
        and type(width) is int
        and 1 <= width <= 144
        and -(1 << (width - 1)) <= bounds[0] <= bounds[1] < (1 << (width - 1)),
        "Exact bounded inclusive signed native interval, no wrapping or booleans",
    )
    return list(bounds)


def native_product(first, second, repeated_operand=False):
    budget()
    corners = [a * b for a in first for b in second]
    lower = 0 if repeated_operand and first[0] <= 0 <= first[1] else min(corners)
    return native_interval([lower, max(corners)], 144)


def minimum_signed_contract(bounds):
    native_interval(bounds)
    width = 1 + (max(-bounds[0], bounds[1] + 1, 1) - 1).bit_length()
    require(1 <= width <= 72, "One finite active signed width")
    require(
        -(1 << (width - 1)) <= bounds[0] <= bounds[1] < (1 << (width - 1))
        and (
            width == 1 or not (-(1 << (width - 2)) <= bounds[0] <= bounds[1] < (1 << (width - 2)))
        ),
        "Exact signed width sufficient and minimal, including negative extrema and width1",
    )
    return {
        "active_signed_width": width,
        "caller_operand_raw_hull": list(bounds),
        "full72_input_port": True,
        "promised_full_signed_width_range": [-(1 << (width - 1)), (1 << (width - 1)) - 1],
        "high72_minus_width_bits_equal_active_sign_bit": True,
        "minimality_and_sufficiency_proved_by_exact_integer_inequalities": True,
        "runtime_width_selection": False,
    }


def row_literal_contract(selected):
    row = read(MATERIAL / "rows/d4_s4.json")
    domain = read(MATERIAL / "source_domain_binding.json")
    require(
        row["row_id"] == ROW_ID
        and row["degree"] == 4
        and row["segments"] == 4
        and row["status"] == selected["status"] == "CERTIFIED_ESTIMATE"
        and selected["degree"] == 4
        and selected["segments"] == 4
        and selected["original_primary_row_SHA256"]
        == _FROZEN[(MATERIAL / "rows/d4_s4.json").relative_to(ROOT).as_posix()]
        and selected["exact_original_full72_resource_estimate"] == row["resource_estimate"],
        "Entire selected original row stays bound to its independently authorized exact expected bytes",
    )
    require(
        domain["schema"] == "a13-source-domain-binding-v1"
        and domain["fixed30_classes_retained"] is True
        and domain["generic_zero_to_ln2_domain_assumed"] is False
        and domain["source_or_gate_array_executed"] is False
        and domain["inverse_ln2_word"] == 1586259972792
        and domain["ln2_word"] == 762123384786
        and set(domain["cases"]) == set(BASELINES),
        "Actual original signed shifted reduction domains, never a substituted generic interval",
    )
    certificate = row["certificate"]
    require(
        certificate["degree"] == 4
        and certificate["segments"] == 4
        and certificate["native_evaluation_plan"] == selected["native_plan"] == FIXED_PLAN
        and certificate["no_G2_allocation_or_feasibility_claim"] is True
        and certificate["realized_candidate_gate_or_ABI_proof"] is False
        and set(certificate["cases"]) == set(BASELINES),
        "Exact16-node ordered signed72/F40 plan and both source cases",
    )
    fits, segments = row["fit"]["segment_fits"], certificate["segments_certificate"]
    require(
        type(fits) is list and type(segments) is list and len(fits) == len(segments) == 4,
        "All four actual coefficient banks",
    )
    table, regions, uniform = [], [], []
    for index, (fit, segment) in enumerate(zip(fits, segments, strict=True)):
        budget()
        fit_round_metadata(fit, 4)
        raw_bounds = native_interval(fit["raw_bounds"])
        center = fit["center_raw"]
        coefficients = fit["coefficient_raw"]
        require(
            fit["segment"] == segment["segment"] == index
            and fit["degree"] == 4
            and raw_bounds == segment["raw_bounds"]
            and type(center) is int
            and center == segment["center_raw"]
            and type(coefficients) is list
            and len(coefficients) == 5
            and all(
                type(word) is int and -(1 << 71) <= word < (1 << 71)
                for word in [center, *coefficients]
            )
            and fit["local_interval"] == segment["local_interval"]
            and [rational(endpoint) for endpoint in fit["local_interval"]]
            == [Fraction(raw_bounds[0] - center, Q), Fraction(raw_bounds[1] - center, Q)]
            and fit["global_minimax_optimality_claim"] is False
            and segment["mesh_or_exchange_convergence_used_as_uniform_proof"] is False,
            "Original literal table and exact closed segment/local interval joined to certified original raw fit",
        )
        table.append([center, *coefficients])
        regions.append(raw_bounds)
        uniform.append(rational(segment["quantized_uniform_error_upper"]))
        require(uniform[-1] >= 0, "Approved quantized polynomial uniform error nonnegative")
    require(
        table == selected["all_quantized_center_coefficient_words"]
        and regions[0][0] == domain["common_remainder_raw_hull"][0]
        and regions[-1][1] == domain["common_remainder_raw_hull"][1]
        and all(first[1] + 1 == second[0] for first, second in zip(regions, regions[1:])),
        "All24 full72 words unchanged and four integer selector regions form complete contiguous hull",
    )
    return row, domain, table, regions, uniform


def original_class_reduction(domain):
    inverse, ln2 = domain["inverse_ln2_word"], domain["ln2_word"]
    proof = {}
    for case in BASELINES:
        budget()
        source = domain["cases"][case]
        bounds = native_interval(source["clipped_log_raw_bounds"])
        require(
            source["actual_stock_sites"] == SITES[case][0]
            and source["original_joint_pairs"] == SITES[case][1]
            and len(source["reduction_cells"]) == 30,
            "Same financial coordinate counts and exact fixed30 exponent classes",
        )
        rows, covered = [], []
        for stored, k in zip(source["reduction_cells"], range(-17, 13), strict=True):
            budget()
            left = max(bounds[0], -((-k * Q * Q) // inverse))
            right = min(bounds[1], -((-(k + 1) * Q * Q) // inverse) - 1)
            empty = left > right
            require(
                stored["k"] == k
                and stored["empty"] is empty
                and stored["clipped_log_raw_bounds"] == [left, right],
                "Exact original floor80 class boundaries and explicitly empty30-slot inventory",
            )
            output = {"k": k, "empty": empty, "clipped_log_raw_bounds": [left, right]}
            if not empty:
                product = native_product([left, right], [inverse, inverse])
                scaled = native_interval([product[0] >> 40, product[1] >> 40])
                exponent = native_interval([scaled[0] >> 40, scaled[1] >> 40])
                require(
                    exponent == [k, k],
                    "Original signed floor40 then signed bits40 is actual floor80",
                )
                left40 = native_interval([k << 40, k << 40])
                ln_product = native_product(left40, [ln2, ln2])
                ln_scaled = native_interval([ln_product[0] >> 40, ln_product[1] >> 40])
                require(
                    ln_scaled == [k * ln2, k * ln2],
                    "Original unsigned modular left40 signed operand and positive-ln2 floor40 agree exactly",
                )
                remainder = native_interval([left - ln_scaled[0], right - ln_scaled[1]])
                require(
                    remainder == stored["remainder_raw_bounds"],
                    "Exact original source class remainder interval",
                )
                covered.append([left, right])
                output.update(
                    signed144_inverse_ln2_product_raw_bounds=product,
                    signed72_scaled_log_raw_bounds=scaled,
                    signed72_exponent_raw_bounds=exponent,
                    signed72_modular_left40_raw_bounds=left40,
                    signed144_ln2_product_raw_bounds=ln_product,
                    signed72_ln2_scaled_raw_bounds=ln_scaled,
                    remainder_raw_bounds=remainder,
                    signed_shift_chain_no_wrap_proved=True,
                )
            else:
                require(
                    set(stored) == {"k", "empty", "clipped_log_raw_bounds"},
                    "No invented nonempty witness in original empty class",
                )
            rows.append(output)
        require(
            covered
            and covered[0][0] == bounds[0]
            and covered[-1][1] == bounds[1]
            and all(first[1] + 1 == second[0] for first, second in zip(covered, covered[1:])),
            "All nonempty exponent classes cover full original clipped integer interval exactly once",
        )
        proof[case] = rows
    return proof


def fixed_native_cell(cell, selected_cell, table, region, original_class, uniform, allowance):
    budget()
    k, index = cell["k"], cell["segment"]
    require(
        selected_cell["k"] == k
        and selected_cell["segment"] == index
        and type(cell["empty"]) is bool,
        "Native/scientific-allowance cell joins preserve exact class/segment indices",
    )
    first = max(original_class["clipped_log_raw_bounds"][0], region[0] + k * 762123384786)
    last = min(original_class["clipped_log_raw_bounds"][1], region[1] + k * 762123384786)
    empty = original_class["empty"] or first > last
    require(
        cell["empty"] is selected_cell["empty"] is empty,
        "Native cell occupancy equals original exponent class crossed with exact threshold region",
    )
    if empty:
        require(
            set(cell) == {"k", "segment", "empty"},
            "Original empty cell remains explicit, no promoted operands",
        )
        return {"k": k, "segment": index, "empty": True}, None
    require(
        cell["clipped_log_raw_bounds"] == [first, last], "Actual whole cell integer range unchanged"
    )
    remainder = native_interval([first - k * 762123384786, last - k * 762123384786])
    local = native_interval([remainder[0] - table[index][0], remainder[1] - table[index][0]])
    require(
        cell["remainder_raw_bounds"] == remainder
        and cell["local_raw_bounds"] == local
        and region[0] <= remainder[0] <= remainder[1] <= region[1],
        "Exact center subtraction and selector threshold equality boundaries",
    )
    ranges, products, records = {}, {}, []
    require(
        len(cell["native_intermediate_ranges"]) == 16 and len(cell["signed144_products"]) == 6,
        "Complete16 stored values and six exact signed144 products",
    )
    product_records = {item["value"]: item for item in cell["signed144_products"]}
    require(
        set(product_records) == {6, 8, 10, 11, 13, 14},
        "Exact six product identities, no duplicates",
    )
    for node, saved in zip(FIXED_PLAN["nodes"], cell["native_intermediate_ranges"], strict=True):
        budget()
        value, op, args = node["value"], node["op"], node["args"]
        if op == "local":
            bounds = local
        elif op == "coefficient":
            word = table[index][1 + node["degree"]]
            bounds = [word, word]
        elif op == "add":
            a, b = (ranges[argument] for argument in args)
            bounds = [a[0] + b[0], a[1] + b[1]]
        else:
            require(op == "mul", "No reordered/substituted operation in exact fixed plan")
            a, b = (ranges[argument] for argument in args)
            product = native_product(a, b, args[0] == args[1])
            require(
                product_records[value]["product_raw_bounds"] == product,
                "Fresh integer endpoint/square relation agrees with original authorized signed144 hull",
            )
            products[value] = {
                "ordered_operand_values": list(args),
                "ordered_operand_raw_bounds": [list(a), list(b)],
                "product_raw_bounds": product,
            }
            bounds = [product[0] >> 40, product[1] >> 40]
        native_interval(bounds)
        require(
            saved["value"] == value and saved["op"] == op and saved["raw_bounds"] == bounds,
            "Every exact fresh signed72 native recurrence equals authorized original stored interval",
        )
        floor = rational(saved["native_floor_error_upper"])
        require(
            floor >= 0 and (op not in ("local", "coefficient") or floor == 0),
            "Existing independently authorized native floor payment retained separately, never recomputed from interval widths",
        )
        ranges[value] = list(bounds)
        records.append(
            {
                "value": value,
                "op": op,
                "args": list(args),
                "raw_bounds": list(bounds),
                "authorized_native_floor_error_upper": saved["native_floor_error_upper"],
            }
        )
    polynomial = ranges[15]
    require(
        polynomial[0] > 0 and cell["native_polynomial_raw_bounds"] == polynomial and -72 < k < 72,
        "Actual positive stock polynomial and original signed shift domain",
    )
    stock = native_interval(
        [polynomial[0] << k, polynomial[1] << k]
        if k >= 0
        else [polynomial[0] >> -k, polynomial[1] >> -k]
    )
    require(
        cell["stock_raw_bounds"] == stock
        and cell["all_native72_product144_and_shift_guards_passed"] is True,
        "Actual exponent-dependent original shift/F40 floor and full72 final stock no-wrap",
    )
    floor = rational(cell["native_floor_error_upper"])
    require(
        floor == rational(cell["native_intermediate_ranges"][-1]["native_floor_error_upper"]),
        "Final stored native floor payment equals authorized output value payment",
    )
    bound = uniform + floor
    require(
        floor >= 0
        and bound <= allowance
        and selected_cell["native_metadata_valid"] is True
        and selected_cell["fits_lower_allowance"] is True
        and selected_cell["approved_lower_allowance"] == ALLOWANCE
        and rational(selected_cell["quantized_uniform_error_upper"]) == uniform
        and rational(selected_cell["native_floor_error_upper"]) == floor
        and rational(selected_cell["polynomial_plus_floor_upper"]) == bound,
        "Same primary polynomial plus authorized actual native floors fits same fixed positive lower allowance",
    )
    separate = {
        "reduction_stock_error_upper_retained_separately": cell["reduction_stock_error_upper"],
        "negative_shift_floor_upper_retained_separately": cell["negative_shift_floor_upper"],
        "additive_stock_beta_upper_retained_separately": cell["additive_stock_beta_upper"],
    }
    require(
        all(selected_cell[key] == value for key, value in separate.items()),
        "Range reduction/variable shift/beta payments never spent again as polynomial allowance",
    )
    for value in separate.values():
        require(rational(value) >= 0, "Original separate authorized payments are nonnegative")
    require(
        rational(cell["negative_shift_floor_upper"]) == (Fraction(1, Q) if k < 0 else Fraction(0)),
        "Original negative final-shift floor remains explicitly paid",
    )
    payment = {
        "k": k,
        "segment": index,
        "empty": False,
        "quantized_uniform_error_upper": pair(uniform),
        "authorized_native_floor_error_upper": pair(floor),
        "polynomial_plus_floor_upper": pair(bound),
        "approved_lower_allowance": ALLOWANCE,
        "fits_lower_allowance": True,
        **separate,
        "existing_floor_theorem_or_exponential_proof_recomputed": False,
    }
    return {
        "k": k,
        "segment": index,
        "empty": False,
        "clipped_log_raw_bounds": [first, last],
        "remainder_raw_bounds": remainder,
        "local_raw_bounds": local,
        "selected_center_coefficient_words": table[index],
        "native_intermediate_ranges": records,
        "signed144_products": [
            {"value": value, **products[value]} for value in (6, 8, 10, 11, 13, 14)
        ],
        "native_polynomial_raw_bounds": polynomial,
        "stock_raw_bounds": stock,
        "fresh_integer_range_and_original_shift_chain_proved": True,
    }, payment


def native_contract_inventory(row, selected, domain, table, regions, uniform, classes):
    allowance = rational(ALLOWANCE)
    all_cells, all_payments = {}, {}
    hulls = {value: [None, None] for value in (6, 8, 10, 11, 13, 14)}
    total, occupied = 0, 0
    for case in BASELINES:
        cells = row["certificate"]["cases"][case]["intersections"]
        selected_cells = selected["all_case_cell_decisions"][case]
        require(
            len(cells) == len(selected_cells) == 120, "Every fixed120 slots for each original case"
        )
        result, payments = [], []
        covered = {k: [] for k in range(-17, 13)}
        for original, decision, (k, segment) in zip(
            cells,
            selected_cells,
            ((k, segment) for k in range(-17, 13) for segment in range(4)),
            strict=True,
        ):
            budget()
            total += 1
            require(
                total <= 240 and original["k"] == k and original["segment"] == segment,
                "Fixed240 ordered integer slots, no corpus change",
            )
            fresh, payment = fixed_native_cell(
                original,
                decision,
                table,
                regions[segment],
                classes[case][k + 17],
                uniform[segment],
                allowance,
            )
            result.append(fresh)
            if payment is None:
                payments.append({"k": k, "segment": segment, "empty": True})
                continue
            occupied += 1
            payments.append(payment)
            covered[k].append(fresh["clipped_log_raw_bounds"])
            for product in fresh["signed144_products"]:
                for position, bounds in enumerate(product["ordered_operand_raw_bounds"]):
                    old = hulls[product["value"]][position]
                    hulls[product["value"]][position] = (
                        list(bounds)
                        if old is None
                        else [min(old[0], bounds[0]), max(old[1], bounds[1])]
                    )
        for original_class in classes[case]:
            budget()
            cover = covered[original_class["k"]]
            if original_class["empty"]:
                require(cover == [], "Empty original class retains four empty slots")
            else:
                require(
                    cover
                    and cover[0][0] == original_class["clipped_log_raw_bounds"][0]
                    and cover[-1][1] == original_class["clipped_log_raw_bounds"][1]
                    and all(a[1] + 1 == b[0] for a, b in zip(cover, cover[1:])),
                    "Four selector segments cover every original integer class without gaps or overlap",
                )
        all_cells[case], all_payments[case] = result, payments
    require(total == 240 and occupied > 0, "Complete fixed two-case native proof inventory")
    contracts, signatures = [], []
    for node in FIXED_PLAN["nodes"]:
        if node["op"] != "mul":
            continue
        budget()
        operands = [minimum_signed_contract(bounds) for bounds in hulls[node["value"]]]
        signature = {
            "ordered_active_signed_widths": [
                operand["active_signed_width"] for operand in operands
            ],
            "input_ports": [72, 72],
            "output_port": 72,
            "fraction_bits": 40,
            "mathematical_signed_product_width": 144,
            "output_semantics": "dirty72 XOR ((signed72(a)*signed72(b) >>40) mod2^72)",
            "required_promised_span": "all sign-extended ordered active signed operands, arbitrary dirty72 output, zero private workspace",
            "coherent_absolute_unit_phase_and_literal_inverse_required": True,
            "possible_low_residue_implementation_bits": 112,
            "lower40_columns_and_all_signed_correction_carries_must_be_proved": True,
            "leaf_lowering_selected_or_emitted": False,
        }
        if signature not in signatures:
            signatures.append(signature)
        contracts.append(
            {
                "value": node["value"],
                "ordered_args": list(node["args"]),
                "operands": operands,
                "complete_ordered_ABI_signature": signature,
                "deduplicated_signature_index": signatures.index(signature),
                "hull_covers_both_cases_every_reachable_segment_class": True,
                "runtime_operand_swap_or_width_switch": False,
                "width_is_not_gate_cost_or_savings": True,
            }
        )
    require(
        len(contracts) == 6 and 1 <= len(signatures) <= 6,
        "Fixed six ordered shared products and at most six distinct complete signatures",
    )
    return {
        "schema": "a13-d4-s4-native-contract-inventory-v1",
        "row_id": ROW_ID,
        "fixed_plan": FIXED_PLAN,
        "fixed_cell_slots": total,
        "occupied_cell_slots": occupied,
        "all_case_cells": all_cells,
        "all_six_ordered_shared_MUL_contracts": contracts,
        "distinct_complete_ABI_signatures": signatures,
        "same_global_hull_per_shared_call_no_runtime_width_selection": True,
        "exact_integer_native_induction_complete": True,
        "gate_or_cost_or_G2_evaluated": False,
    }, {
        "schema": "a13-d4-s4-existing-allowance-payment-join-v1",
        "fixed_alpha": ALPHA,
        "approved_primary_E_allow_lower": ALLOWANCE,
        "all240_cells": all_payments,
        "certified_original_floor_uniform_and_reduction_payments_carried": True,
        "polynomial_error_and_native_operand_domain_are_distinct_proofs": True,
        "no_new_exponential_fit_quantization_or_allocation": True,
        "candidate_financial_allocation_closed": False,
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
        "One fresh selected-row inventory route, no automatic retry",
    )
    try:
        runtime_invocation_guard(args.ready_sha256)
        admission(args.ready_sha256)
        runtime = own_runtime()
        loaded_origins()
        check_code_caches()
        saved_before = saved_runtime_membership()
        failed_material_witness()
        selection_failure_witnesses()
        prior_inventory_failure_witness()
        selector_result_witness()
        first = fresh_union()
        require(
            saved_runtime_membership() == saved_before,
            "Entire saved source runtime exact across first full fresh union",
        )
        failed_material_witness()
        selection_failure_witnesses()
        prior_inventory_failure_witness()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        for path in (AUTHOR, METHOD_DOC, PREFLIGHT, READY):
            copy(path, "executed_" + path.name)
        for path in (
            PRIOR_SELECTION_FREEZE,
            PRIOR_SELECTION_READY,
            PRIOR_SELECTION_LOG,
            *(RESEARCH / name for name in PRIOR_SELECTION_AUTHORS),
        ):
            copy(path, "prior_selector_failed_" + path.name)
        for path in (
            SELECTOR_READY,
            SELECTOR_RESULT_REVIEW,
            *(RESEARCH / name for name in SELECTOR_AUTHORS),
        ):
            copy(path, "prior_selector_completed_" + path.name)
        for path in (
            PRIOR_INVENTORY_WITNESS,
            PRIOR_INVENTORY_READY,
            PRIOR_INVENTORY_LOG,
            *(RESEARCH / name for name in PRIOR_INVENTORY_AUTHORS),
        ):
            copy(path, "prior_inventory_prefit_failed_" + path.name)
        save(
            "run_started.json",
            {
                "created_UTC": datetime.now(timezone.utc).isoformat(),
                "PID": os.getpid(),
                "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
                **flags(),
            },
        )
        selected = selector_result_witness()
        copied_metadata_provenance()
        row, domain, table, regions, uniform = row_literal_contract(selected)
        source_contract = source_binding_inventory(row, domain, selected)
        classes = original_class_reduction(domain)
        native, payments = native_contract_inventory(
            row, selected, domain, table, regions, uniform, classes
        )
        selector = selector_coefficient_inventory(row, table, regions, selected)
        save(
            "completed_selector_binding.json",
            {
                "actual_manifest_SHA256": SELECTOR_SHA,
                "complete_owner_counts": SELECTOR_COUNTS,
                "root_result_review_SHA256": SELECTOR_RESULT_REVIEW_SHA,
                "fixed_row_id": ROW_ID,
                "reselection_or_reranking": False,
                "financial_gate_permission": False,
            },
        )
        save("full_original_source_obligations.json", source_contract)
        save(
            "original_signed_class_reduction.json",
            {
                "schema": "a13-d4-s4-exact-signed-source-class-reduction-v1",
                "cases": classes,
                "same_original_floor80_and_signed_shifted_reduction": True,
            },
        )
        save(
            "all240_native_contract_cells.json",
            {
                key: value
                for key, value in native.items()
                if key
                not in ("all_six_ordered_shared_MUL_contracts", "distinct_complete_ABI_signatures")
            },
        )
        save(
            "six_ordered_MUL_contracts.json",
            {
                "schema": "a13-d4-s4-six-ordered-MUL-contracts-v1",
                "contracts": native["all_six_ordered_shared_MUL_contracts"],
                "signatures": native["distinct_complete_ABI_signatures"],
                "gate_leaf_authoring_or_execution_authorized": False,
            },
        )
        save("selector_full24_coefficient_inventory.json", selector)
        save("existing_fixed_allowance_payment_join.json", payments)
        loaded_origins()
        check_code_caches()
        require(
            saved_runtime_membership() == saved_before,
            "All saved source runtime members remain exact",
        )
        failed_material_witness()
        selection_failure_witnesses()
        prior_inventory_failure_witness()
        selector_result_witness()
        second = fresh_union()
        require(
            saved_runtime_membership() == saved_before,
            "Entire saved source runtime exact across second full fresh union",
        )
        failed_material_witness()
        selection_failure_witnesses()
        prior_inventory_failure_witness()
        selector_result_witness()
        summary = {
            "schema": "a13-d4-s4-native-contract-inventory-summary-v2",
            "completed": True,
            "passed": True,
            "budget_censored": False,
            "row_id": ROW_ID,
            "fixed_cell_slots": native["fixed_cell_slots"],
            "occupied_cell_slots": native["occupied_cell_slots"],
            "ordered_shared_MUL_count": 6,
            "distinct_complete_ABI_signatures": len(native["distinct_complete_ABI_signatures"]),
            "native_integer_domain_contract_inventory_passed": True,
            "whole_source_operation_storage_selector_coefficient_copies_inverse_obligations_enumerated": True,
            "future_leaf_source_cost_release_requires_separate_peer_ROOT_approval": True,
            "original_capped_baselines_retained": BASELINES,
            "original_full72_symbolic_estimates_retained_as_estimates": row["resource_estimate"],
            "completed_selector_manifest_SHA256": SELECTOR_SHA,
            "all7_completed_owner_maps_and_owned_inventories_retained": True,
            "prior_inventory_pre_output_failure_retained_without_promotion": True,
            "runtime_invocation": RUNTIME_INVOCATION,
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
                len(owned) < MAX_OWN_FILES - 1 and total <= MAX_OWN_BYTES,
                "Inclusive owned manifest reserve",
            )
            owned[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
        complete_manifest(
            {
                "schema": "a13-d4-s4-native-contract-inventory-manifest-v2",
                "files": owned,
                "frozen_inputs": _FROZEN,
                "external_runtime_inputs": _EXTERNAL,
                "manifest_self_hash_excluded": True,
                "completed": True,
                "passed": True,
                "budget_censored": False,
                "row_id": ROW_ID,
                "completed_selector_manifest_SHA256": SELECTOR_SHA,
                "completed_selector_complete_counts": SELECTOR_COUNTS,
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
                    "row_id": ROW_ID,
                    "native_contract_inventory_only": True,
                    **flags(),
                }
            ),
            flush=True,
        )
    except BaseException as error:
        retain_failure(error)
        raise


"""Author-only A13 d4_s4 metadata joins; never imported or executed by the author.

The final owner injects ROOT, PROGRAM, Path, hashlib, json, budget, require,
canonical, digest, read and the exact independent_removal definition. All seven
owner maps are admitted before entry. Arrays are opaque expected-SHA inputs.
No arithmetic range, width, parity, array, gate, phase or cost evaluator exists
here. Original descriptor resources and stock semantics are metadata premises.
"""


def a13_contract_object_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def a13_contract_pin(path, expected):
    budget()
    actual = canonical(path)
    require(actual.is_relative_to(ROOT), "Original ROOT-owned source member")
    key = actual.relative_to(ROOT).as_posix()
    require(key in expected, "Member belongs to complete admitted expected maps")
    require(digest(actual) == expected[key], "Original expected source bytes")
    return actual, dict(path=key, sha256=expected[key])


def a13_contract_nodes(target):
    require((target["width"], target["fraction_bits"]) == (72, 40), "Original signed72/F40")
    require(type(target["nodes"]) is list and len(target["nodes"]) <= 50000, "Bounded source SSA")
    arities = dict(
        input=0,
        const=0,
        add=2,
        sub=2,
        mul=2,
        cmul=1,
        lt=2,
        select=3,
        positive=1,
        msb=1,
        bits=1,
        shift=2,
        sqrt=1,
        lookup=1,
    )
    nodes, inputs, calls = {}, [], []
    for node in target["nodes"]:
        budget()
        op, args, outs = (node[key] for key in ("op", "args", "out"))
        require(
            op in arities and type(args) is list and len(args) == arities[op],
            "Original typed arity",
        )
        require(
            type(node["params"]) is dict and type(outs) is list and 1 <= len(outs) <= 16,
            "Bounded original node ports",
        )
        require(
            all(type(arg) is int and arg in nodes for arg in args), "Original topological arguments"
        )
        require(op == "lookup" or len(outs) == 1, "Original single-output primitive")
        for value in outs:
            require(type(value) is int and value == len(nodes), "Original contiguous SSA identity")
            nodes[value] = node
        require(len(nodes) <= 60000, "Bounded native SSA storage")
        (inputs if op == "input" else calls).append(node)
    return nodes, inputs, calls


def a13_contract_node(nodes, value, operation, args=None, params=None):
    budget()
    require(type(value) is int and value in nodes, "Pinned original value ID")
    node = nodes[value]
    require(node["op"] == operation and node["out"] == [value], "Exact original operation")
    require(args is None or node["args"] == args, "Exact ordered source arguments")
    require(params is None or node["params"] == params, "Exact original source parameters")
    return node


def a13_contract_leaves(case, target, source, expected):
    route = PROGRAM / "A10_coefficient_run001" / case / "min-depth"
    library = canonical(route / "leaves")
    require(
        Path(source["library"]).is_absolute() and canonical(source["library"]) == library,
        "Exact original absolute native library path",
    )
    saved = source["library_workspace_relative"].replace("\\", "/")
    require(".." not in saved.split("/"), "No saved library traversal")
    marker = saved.lower().find("/results/")
    require(
        canonical(ROOT / (saved[marker + 1 :] if marker >= 0 else saved)) == library,
        "Exact original native library path",
    )
    keys = source["library_keys"]
    require(
        type(keys) is list and 1 <= len(keys) <= 256 and len(set(keys)) == len(keys),
        "Complete bounded original leaf keys",
    )
    leaves, refs, tables = {}, {}, {}
    operations = {node["op"] for node in target["nodes"]}
    for key in keys:
        budget()
        require(
            type(key) is str and key and all(c in "0123456789abcdef" for c in key),
            "Original leaf key",
        )
        descriptor, reference = a13_contract_pin(library / (key + ".json"), expected)
        entry = read(descriptor)
        require(entry["key"] == key and entry["op"] in operations, "Original descriptor identity")
        require(
            type(entry["args"]) is list
            and len(entry["args"]) <= 3
            and type(entry["outs"]) is list
            and 1 <= len(entry["outs"]) <= 16,
            "Original descriptor port counts",
        )
        used = set()
        for bank in entry["args"] + entry["outs"]:
            require(type(bank) is list and len(bank) == 72, "Every original full72 port")
            require(
                all(
                    type(wire) is int and 0 <= wire < entry["resources"]["qubits"] for wire in bank
                ),
                "Original wire addresses within saved descriptor resources",
            )
            require(
                len(set(bank)) == 72 and not used.intersection(bank),
                "Disjoint original local ports",
            )
            used.update(bank)
        gate_name = entry["gate_file"]
        require(
            type(gate_name) is str and gate_name == key + ".npy", "Exact original array filename"
        )
        gate, gate_reference = a13_contract_pin(library / gate_name, expected)
        require(
            gate.parent == library and gate_reference["sha256"] == entry["sha256"],
            "Descriptor expected full array bytes; no array interpretation",
        )
        require(
            type(entry["resources"]) is dict
            and set(
                (
                    "qubits",
                    "source_gates",
                    "x",
                    "cx",
                    "ccx",
                    "t_count",
                    "t_depth",
                    "clifford_t_depth",
                    "clifford_cx",
                    "clifford_h",
                    "schedule",
                )
            )
            <= set(entry["resources"]),
            "Complete retained original resource metadata",
        )
        if entry["op"] == "lookup":
            table_name = entry["params"]["table"]
            require(
                table_name in ("log", "cos") and table_name in target["tables"],
                "Original table identity",
            )
            shape = {"log": (32, 9, 5, 20736), "cos": (64, 8, 6, 36864)}[table_name]
            table = target["tables"][table_name]
            require(
                len(table) == shape[0]
                and all(len(row) == shape[1] for row in table)
                and entry["params"]["bits"] == shape[2]
                and entry["table_bits"] == shape[3]
                and len(entry["outs"]) == shape[1],
                "Original full table and descriptor shape",
            )
            tables[table_name] = dict(
                target_table_sha256=a13_contract_object_sha(table),
                descriptor=reference,
                rows=shape[0],
                columns=shape[1],
            )
        leaves[key] = entry
        refs[key] = dict(
            descriptor=reference,
            array=gate_reference,
            ABI_sha256=a13_contract_object_sha([entry["args"], entry["outs"]]),
            parameters_sha256=a13_contract_object_sha(entry["params"]),
            resources_sha256=a13_contract_object_sha(entry["resources"]),
        )
    require(set(tables) == {"log", "cos"}, "Both immutable original tables retained")
    return leaves, refs, tables


def a13_contract_stock(nodes, site):
    stock, polynomial, exponent, clipped, raw_log, remainder = (
        site[key] for key in ("stock", "polynomial", "exponent", "clipped", "raw_log", "remainder")
    )
    a13_contract_node(nodes, stock, "shift", [polynomial, exponent], {})
    exp_node = a13_contract_node(
        nodes, exponent, "bits", params={"shift": 40, "width": 72, "signed": True}
    )
    reduction = exp_node["args"][0]
    a13_contract_node(nodes, reduction, "cmul", [clipped], {"c": 1586259972792})
    top = a13_contract_node(nodes, clipped, "select", params={})
    upper_flag, middle, upper = top["args"]
    a13_contract_node(nodes, upper_flag, "lt", [middle, upper], {})
    lower = a13_contract_node(nodes, middle, "select", params={})
    lower_flag, lower_word, actual_log = lower["args"]
    require(actual_log == raw_log, "Exact original logarithm before signed clamp")
    a13_contract_node(nodes, lower_flag, "lt", [raw_log, lower_word], {})
    a13_contract_node(nodes, lower_word, "const", [], {"value": 4722366470675671057123})
    a13_contract_node(nodes, upper, "const", [], {"value": 9145480617430})
    require(
        [site["low"], site["high"], site["inverse_ln2"], site["ln2"]]
        == [-12193974156573, 9145480617430, 1586259972792, 762123384786],
        "Unchanged admitted signed clamp/reducer literal metadata",
    )
    remainder_node = a13_contract_node(nodes, remainder, "sub", params={})
    require(remainder_node["args"][0] == clipped, "Original remainder left argument")
    ln2_product = remainder_node["args"][1]
    term = a13_contract_node(nodes, ln2_product, "cmul", params={"c": 762123384786})
    exp_left40 = term["args"][0]
    a13_contract_node(
        nodes, exp_left40, "bits", [exponent], {"shift": -40, "width": 72, "signed": False}
    )
    closure, pending = set(), [stock]
    while pending:
        budget()
        require(len(closure) <= 256 and len(pending) <= 1024, "Bounded original stock closure")
        value = pending.pop()
        if value == clipped or value in closure:
            continue
        node = nodes[value]
        require(
            node["op"] in ("const", "add", "sub", "mul", "cmul", "bits", "shift")
            and node["out"] == [value],
            "Original stock-only native template",
        )
        closure.add(value)
        pending.extend(node["args"])
    require(sorted(closure) == site["values"], "All original stock-template values retained")
    signatures = {clipped: ["clipped-native-word"]}
    for value in sorted(closure):
        budget()
        node = nodes[value]
        children = [signatures[arg] for arg in node["args"]]
        if node["op"] in ("add", "mul"):
            children.sort(key=lambda child: json.dumps(child, sort_keys=True))
        signatures[value] = [node["op"], node["params"], children]
    require(
        a13_contract_object_sha(signatures[stock]) == site["actual_original_support_signature"],
        "Exact admitted original canonical stock signature",
    )
    return dict(
        stock=stock,
        polynomial=polynomial,
        exponent=exponent,
        remainder=remainder,
        clipped=clipped,
        raw_log=raw_log,
        lower_constant=lower_word,
        upper_constant=upper,
        lower_compare=lower_flag,
        upper_compare=upper_flag,
        reducer_cmul=reduction,
        exponent_left40=exp_left40,
        ln2_cmul=ln2_product,
        final_shift=stock,
        stock_template_sha256=site["actual_original_support_signature"],
    )


def a13_d4_s4_source_contract(domain, row, expected, started):
    """Metadata-only full original-source join and future paid-obligation witness."""
    budget(admission=True)
    require(
        domain["schema"] == "a13-source-domain-binding-v1"
        and domain["fixed30_classes_retained"] is True
        and domain["generic_zero_to_ln2_domain_assumed"] is False
        and domain["source_or_gate_array_executed"] is False,
        "Original domain metadata scope",
    )
    require(set(domain["cases"]) == {"B4x12", "B8x52"}, "Both original financial sources")
    require(
        (row["row_id"], row["degree"], row["segments"]) == ("d4_s4", 4, 4),
        "Sole fixed selected row",
    )
    fits = row["fit"]["segment_fits"]
    require(
        len(fits) == 4 and [fit["segment"] for fit in fits] == [0, 1, 2, 3],
        "All four immutable fit rows",
    )
    table = [[fit["center_raw"], *fit["coefficient_raw"]] for fit in fits]
    require(all(len(bank) == 6 for bank in table), "All24 dynamic center/coefficient words")
    cases = {}
    for case, shape in {
        "B4x12": (48, 30, 60, 4978, 5698, 96),
        "B8x52": (416, 234, 468, 41186, 46802, 832),
    }.items():
        budget(admission=True)
        route = PROGRAM / "A10_coefficient_run001" / case / "min-depth"
        payloads, inputs = {}, {}
        for name in ("target", "source", "schedule_capped"):
            path, reference = a13_contract_pin(route / (name + ".json"), expected)
            payloads[name], inputs[name] = read(path), reference
        target, source, schedule = (
            payloads[name] for name in ("target", "source", "schedule_capped")
        )
        nodes, original_inputs, actual_nodes = a13_contract_nodes(target)
        require(
            source["word_width"] == 72
            and source["fraction_bits"] == 40
            and source["exact_clifford_t"] is True
            and source["arbitrary_rotations"] == 0,
            "Unchanged original native/absolute-phase metadata premise",
        )
        require(
            len(original_inputs) == shape[2]
            and len(actual_nodes) == shape[3]
            and source["values"] == shape[4]
            and len(nodes) == shape[4],
            "Complete original source shape",
        )
        require(
            source["inputs"] == original_inputs and source["outputs"] == target["outputs"],
            "Original source IO",
        )
        require(
            schedule["target_fingerprint"] == a13_contract_object_sha(target)
            and schedule["source_fingerprint"] == a13_contract_object_sha(source),
            "Original schedule source identity",
        )
        require(
            source["clean_schedule"]
            == [
                "forward_calls",
                "CX each named SSA output to its separate output register",
                "reverse forward_calls with each leaf inverted",
            ],
            "Complete original clean function schedule",
        )
        require(
            source["invocation_semantics"]
            == "Copy every argument to a distinct clean local slot; bind output slots to fresh SSA output registers; execute leaf; uncopy arguments. Shared non-output local slots start/end zero."
            and source["inverse_semantics"]
            == "Reverse the clean schedule and invert every leaf; all basis gates are self-inverse.",
            "Every original argument, SSA, shared workspace and literal inverse obligation",
        )
        leaves, descriptors, original_tables = a13_contract_leaves(case, target, source, expected)
        calls = source["forward_calls"]
        require(type(calls) is list and len(calls) == shape[3], "Every original forward call")
        for node, call in zip(actual_nodes, calls, strict=True):
            budget()
            require(call["leaf"] in leaves, "Call uses an admitted actual descriptor")
            leaf = leaves[call["leaf"]]
            require(
                [leaf["op"], leaf["params"], call["args"], call["out"]]
                == [node["op"], node["params"], node["args"], node["out"]],
                "Every ordered native call matches source SSA",
            )
            require(
                len(leaf["args"]) == len(node["args"]) and len(leaf["outs"]) == len(node["out"]),
                "Every actual local ABI matches source call",
            )
            require(
                call["argument_copy_cx"] == {0: 0, 1: 144, 2: 288, 3: 432}[len(node["args"])],
                "Every original72-bit argument copy and uncopy retained",
            )
        original, estimate = domain["cases"][case], row["resource_estimate"]["cases"][case]
        require(
            original["actual_stock_sites"] == shape[0]
            and original["original_joint_pairs"] == shape[1]
            and len(original["stock_sites"]) == shape[0],
            "All original48/416 stock sites",
        )
        require(
            len({site["stock"] for site in original["stock_sites"]}) == shape[0],
            "Distinct actual stock invocations",
        )
        require(
            original["baseline_serial_resources"] == source["resources"]
            and original["baseline_capped_resources"] == schedule["resources"],
            "Retained actual baseline resources without recomputation",
        )
        baseline = {"B4x12": [520720662, 555774, 550141], "B8x52": [4267435214, 663704, 4460479]}[
            case
        ]
        require(
            [schedule["resources"][key] for key in ("t_count", "t_depth", "logical_qubits")]
            == baseline
            and schedule["qubit_cap"] == baseline[2],
            "Exact original observed capped count/depth and fixed whole-source cap",
        )
        witnesses = [a13_contract_stock(nodes, site) for site in original["stock_sites"]]
        removal = independent_removal(target, source, original["stock_sites"], started)
        require(
            removal == estimate["original_polynomial_removal"],
            "Exact original remove/retain/dead-path closure",
        )
        require(
            estimate["coefficient_QROM_rows_raw"] == table
            and estimate["threshold_raw"] == [190530846196, 381061692393, 571592538590],
            "Immutable selector/table identities",
        )
        require(
            estimate["selector"]
            == dict(
                address_bits=2,
                threshold_count=3,
                address_toggle_CX=4,
                equality_compute_uncompute_CCX=8,
                equality_CX=0,
                address_inversion_X=8,
                table_data_controlled_CX=492,
                table_constant_X=0,
            ),
            "Original symbolic selector bookkeeping only",
        )
        require(
            estimate["whole_candidate_clean_invocations"] == shape[5]
            and estimate["global_forward_and_inverse_each_use_clean_candidate"] is True,
            "Original96/832 candidate invocations in both global directions",
        )
        require(
            [
                estimate["full72_argument_copy_CX_per_forward"],
                estimate["dirty_output_XOR_CX"],
                estimate["outer_function_argument_copy_CX_per_clean_invocation"],
                estimate["function_full72_SSA_words"],
                estimate["function_private_scratch_qubits"],
            ]
            == [4032, 72, 144, 31, 14645],
            "Original candidate copy/output/storage metadata retained",
        )
        require(
            estimate["full72_bank_inventory"]
            == dict(
                candidate_IR_values=16,
                raw_remainder_bank=1,
                outer_argument_copy_bank=1,
                threshold_constant_banks=3,
                threshold_predicate_banks=3,
                selector_address_banks=1,
                QROM_center_and_coefficient_banks=6,
                external_input_output_banks=2,
            ),
            "All original candidate banks retained",
        )
        require(
            estimate["all_costs_are_estimates_until_emitted_ABI_and_capped_schedule_proofs"] is True
            and estimate["estimated_serial_depth_not_realized_capped_schedule"] is True
            and estimate["relative_phase_substitution"] is False,
            "No realized-cost or whole-depth transfer",
        )
        cases[case] = dict(
            inputs=inputs,
            source_calls_checked=shape[3],
            source_values_retained=shape[4],
            stock_sites_checked=shape[0],
            clean_candidate_invocations_retained=shape[5],
            descriptor_map=descriptors,
            original_table_signatures=original_tables,
            ordered_source_calls_sha256=a13_contract_object_sha(calls),
            stock_chains=witnesses,
            original_polynomial_removal=removal,
            full72_bank_inventory=estimate["full72_bank_inventory"],
            original_serial_resources_sha256=a13_contract_object_sha(source["resources"]),
            original_capped_resources_sha256=a13_contract_object_sha(schedule["resources"]),
        )
    return dict(
        schema="a13-d4-s4-source-contract-metadata-witness-v1",
        passed=True,
        cases=cases,
        selected_table_sha256=a13_contract_object_sha(table),
        native_contract="Full72 preserved inputs; signed144 product; native floor40; arbitrary dirty72 XOR output; clean private workspace; coherent absolute unit phase; literal full inverse.",
        source_arrays_interpreted=False,
        new_costs_evaluated=False,
        scalar_ranges_or_widths_evaluated=False,
        gate_emission_or_replay_permission=False,
        financial_G2_allocation=None,
        fixture_price_gate_replay_credit=0,
        adoption_or_quantum_advantage_claim=False,
    )


def source_binding_inventory(row, domain, selected):
    """Public inventory API; the parent admits all seven complete owner maps."""
    paths = {}
    for name, value in (("source_domain_binding.json", domain), ("rows/d4_s4.json", row)):
        path, reference = a13_contract_pin(MATERIAL / name, _FROZEN)
        require(read(path) == value, "Passed metadata object equals exact admitted original member")
        paths[name] = reference
    require(
        selected["exact_original_full72_resource_estimate"] == row["resource_estimate"]
        and selected["native_plan"] == row["certificate"]["native_evaluation_plan"],
        "Original selected resource and operation metadata joins",
    )
    result = a13_d4_s4_source_contract(domain, row, _FROZEN, _STARTED)
    result["original_domain_and_selected_row"] = paths
    return result


def selector_coefficient_inventory(row, table, regions, selected):
    """Identity and paid-obligation inventory; no selector or table cost evaluation."""
    budget()
    fits = row["fit"]["segment_fits"]
    require(
        len(fits) == len(table) == len(regions) == 4 and all(len(bank) == 6 for bank in table),
        "Fixed4-by6 full72 dynamic table",
    )
    require(
        table
        == [[fit["center_raw"], *fit["coefficient_raw"]] for fit in fits]
        == selected["all_quantized_center_coefficient_words"],
        "All24 exact selected original table words",
    )
    require(
        regions == [fit["raw_bounds"] for fit in fits], "Same four original signed selector regions"
    )
    thresholds = [190530846196, 381061692393, 571592538590]
    require(
        [region[0] for region in regions[1:]] == thresholds,
        "Exact original three comparison thresholds",
    )
    selector = dict(
        address_bits=2,
        threshold_count=3,
        address_toggle_CX=4,
        equality_compute_uncompute_CCX=8,
        equality_CX=0,
        address_inversion_X=8,
        table_data_controlled_CX=492,
        table_constant_X=0,
    )
    preserved = {}
    for case in ("B4x12", "B8x52"):
        budget()
        estimate = row["resource_estimate"]["cases"][case]
        require(
            estimate == selected["exact_original_full72_resource_estimate"]["cases"][case],
            "Original selected full72 resource metadata retained exactly",
        )
        require(
            estimate["selector"] == selector
            and estimate["threshold_raw"] == thresholds
            and estimate["coefficient_QROM_rows_raw"] == table,
            "Both case estimates name the same immutable selector and table",
        )
        unsigned = estimate["coefficient_QROM_rows_unsigned72"]
        require(
            type(unsigned) is list
            and len(unsigned) == 4
            and all(type(bank) is list and len(bank) == 6 for bank in unsigned),
            "Retained original encoded table metadata; no encoding recalculation",
        )
        require(
            estimate["dynamic_selected_coefficient_constant_multiplier_discount"] is False,
            "Dynamic table loading retained even for singleton future operand promises",
        )
        preserved[case] = dict(
            original_symbolic_selector=selector,
            original_unsigned_table_sha256=a13_contract_object_sha(unsigned),
            all_dynamic_table_words_paid=True,
            full72_comparison_and_copy_obligations_retained=True,
        )
    return dict(
        schema="a13-d4-s4-selector-coefficient-obligations-v1",
        passed=True,
        regions=regions,
        threshold_raw=thresholds,
        comparison_count=3,
        signed_comparison_word_width=72,
        predicate_bank_word_width=72,
        two_bit_address_with_full72_storage=True,
        equality_address_rows=[0, 1, 2, 3],
        full72_center_coefficient_rows=table,
        table_sha256=a13_contract_object_sha(table),
        cases=preserved,
        center_subtraction_retained=True,
        six_dynamic_ordered_products_retained=True,
        four_additions_retained=True,
        all_argument72_copy_output72_XOR_and_literal_inverse_retained=True,
        all_original_SSA_private_selector_banks_and_shared_workspace_cleanup_retained=True,
        realized_helpers_arrays_ABI_and_absolute_phase_proof_still_required=True,
        new_selector_table_or_resource_cost_evaluated=False,
        leaf_emission_or_source_feasibility_permission=False,
    )


if __name__ == "__main__":
    main()
