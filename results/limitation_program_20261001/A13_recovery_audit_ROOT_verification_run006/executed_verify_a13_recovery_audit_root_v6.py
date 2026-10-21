"""Prospective A13 all20 V6 ROOT metadata integrity, never scientific replay.

Current completed run006 is the only admitted scientific-success receipt.
Nested old failures remain opaque historical inputs and remain unapproved.
Saved gzip rows are byte-hashed, never decompressed or scientifically evaluated.
"""

import argparse
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
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
AUTHOR = RESEARCH / "verify_a13_recovery_audit_root_v6.py"
METHOD_DOC = RESEARCH / "A13_RECOVERY_AUDIT_ROOT_INTEGRITY_PREFLIGHT_V6.md"
PREFLIGHT = RESEARCH / "a13_recovery_audit_root_integrity_preflight_v6.json"
READY = ROOT / ".context/A13_RECOVERY_AUDIT_ROOT_INTEGRITY_V6_ROOT_READY_run006.json"
OUTPUT = PROGRAM / "A13_recovery_audit_ROOT_verification_run006"
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


def flags():
    return {
        "metadata_integrity_only": True,
        "new_scientific_evaluation": False,
        "new_test_credit": 0,
        "new_credited_gate_replays": 0,
        "new_price_samples": 0,
        "scientific_imports_or_proof_decompression": False,
        "candidate_feasibility": False,
        "actual_gate_schedule_or_cost_verified": False,
        "candidate_G2_absolute_stock_error_allocation": None,
        "candidate_G2_barrier_band_allocation": None,
        "gate_emission_authorized": False,
        "full_G2": False,
        "adoption": False,
        "cost_transfer": False,
        "quantum_advantage": False,
        "old_failed_source_mathematical_PASS": False,
        "old_V5_and_partial_A20_failures_approved": False,
        "nested_historical_manifests_admitted_as_success": False,
        "historical_global_LIVE_integrity_approved": False,
        "original_scientific_receipts_unchanged": True,
    }


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


def admission(ready_sha):
    ready = read(bind(READY, ready_sha))
    require(
        ready["schema"] == "root-a13-recovery-audit-integrity-READY-v6"
        and ready["ready"] is True
        and ready["root_and_independent_static_reviews_passed"] is True
        and ready["local_only"] is True,
        "Independent ROOT release explicitly local and metadata only",
    )
    require(
        ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and ready["audit_manifest_SHA256"] == AUDIT_SHA
        and ready["audit_complete_counts"] == AUDIT_COUNTS
        and ready["source_ROOT_READY_SHA256"] == AUDIT_READY_SHA
        and ready["prepared_protocol_SHA256"] == PROTOCOL_SHA,
        "ROOT externally pins this exact completed packet and immutable protocol",
    )
    require(
        ready["new_scientific_evaluation"] is False
        and ready["financial_adoption"] is False
        and ready["gate_emission_authorized"] is False
        and ready["fixture_credit"] == 0
        and ready["candidate_feasibility"] is False
        and ready["quantum_advantage"] is False,
        "Only scoped metadata integrity release, zero science/feasibility/adoption/advantage",
    )
    own = ready["author_method_SHA256"]
    require(
        type(own) is dict and set(own) == {AUTHOR.name, METHOD_DOC.name, PREFLIGHT.name},
        ("Exactly three new verifier files"),
    )
    for name, expected in own.items():
        bind(RESEARCH / name, expected)
    policy = read(PREFLIGHT)
    require(
        policy["schema"] == "a13-recovery-audit-root-integrity-preflight-v6"
        and policy["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and policy["owned_caps_files_bytes"] == [MAX_OWN_FILES, MAX_OWN_BYTES]
        and policy["runtime_caps_files_bytes"] == [MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES]
        and policy[("bookkeeping_reference_unique_bytes_hash_work_caps")]
        == [MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK]
        and policy["audit_manifest_SHA256"] == AUDIT_SHA
        and policy["audit_complete_counts"] == AUDIT_COUNTS
        and policy["source_ROOT_READY_SHA256"] == AUDIT_READY_SHA
        and policy["prepared_protocol_SHA256"] == PROTOCOL_SHA
        and policy["source_author_method_SHA256"] == AUDIT_AUTHORS
        and policy["required25_snapshot_SHA256"] == REQUIRED_SNAPSHOTS
        and policy["author_sha256"] == {AUTHOR.name: own[AUTHOR.name]}
        and policy["new_scientific_evaluation"] is False
        and policy["local_only"] is True,
        "Exact prospective local scoped integrity policy and original expectations",
    )
    source_ready = read(bind(AUDIT_READY, AUDIT_READY_SHA))
    require(
        source_ready["schema"] == "root-a13-recovery-audit-READY-v6"
        and source_ready[("ready")] is True
        and source_ready[("root_and_independent_static_reviews_passed")] is True
        and source_ready["author_method_SHA256"] == AUDIT_AUTHORS
        and source_ready["output"] == AUDIT.relative_to(ROOT).as_posix()
        and source_ready["CPU_admission_wall_seconds"] == [300, 270, 900]
        and source_ready[("gate_emission_authorized")] is False
        and source_ready[("new_fixture_credit")] == 0,
        "Exact original executed V6 ROOT_READY remains bound without new permission",
    )
    for name, expected in AUDIT_AUTHORS.items():
        bind(RESEARCH / name, expected)
    code_caches(
        [RESEARCH / "audit_exp_frontier_recovery_v6.py"],
        source_ready["existing_new_code_cache_SHA256"],
        source_ready["absent_new_code_cache_paths"],
    )
    code_caches(
        [AUTHOR], ready[("existing_new_code_cache_SHA256")], ready[("absent_new_code_cache_paths")]
    )
    manifest = current_packet()
    source_protocol_checks(manifest)
    executables = {canonical(LAUNCHER), canonical(Path(sys._base_executable))}
    require(
        len(executables) == 2 and canonical(sys._base_executable) == _BASE_SCOPE / ("python.exe"),
        ("Both actual distinct launcher/base executables"),
    )
    pinned_executables = set()
    for spelling, expected in ready["interpreter_expected_SHA256"].items():
        actual = canonical(spelling)
        require(
            actual in executables and actual not in pinned_executables,
            ("Only actual distinct interpreter expected pins"),
        )
        pinned_executables.add(actual)
        bind(actual, expected)
    require(
        pinned_executables == executables,
        ("Both externally declared actual interpreter pins present"),
    )
    return manifest


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


def main():
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256", required=True)
    args = parser.parse_args()
    require(
        canonical(__file__) == AUTHOR and not OUTPUT.exists(), ("Single fresh ROOT-integrity route")
    )
    try:
        manifest = admission(args.ready_sha256)
        runtime = own_runtime()
        loaded_origins()
        check_code_caches()
        saved_before = saved_runtime_membership()
        first = fresh_union()
        require(
            saved_runtime_membership() == saved_before,
            ("Original source runtime stable through first complete fresh union"),
        )
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
        report = reconcile_metadata(manifest)
        save("metadata_reconciliation.json", report)
        loaded_origins()
        check_code_caches()
        saved_after = saved_runtime_membership()
        require(saved_after == saved_before, "Complete saved source runtime still unchanged")
        second = fresh_union()
        require(
            saved_runtime_membership() == saved_after,
            ("Original source runtime stable through final complete fresh union"),
        )
        summary = {
            "schema": "a13-recovery-audit-root-integrity-summary-v6",
            "completed": True,
            "passed": True,
            "budget_censored": False,
            "audit_manifest_SHA256": AUDIT_SHA,
            "audit_complete_counts": AUDIT_COUNTS,
            "source_ROOT_READY_SHA256": AUDIT_READY_SHA,
            "prepared_protocol_SHA256": PROTOCOL_SHA,
            "current_scoped_all20_certification_integrity_verified": True,
            "complete_saved_source_runtime": [saved_before, saved_after],
            "both_full_uncached_input_unions": [first, second],
            "current_runtime": runtime,
            ("budget"): {
                ("process_CPU_seconds"): time.process_time(),
                ("wall_seconds"): time.monotonic() - _STARTED,
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
                ("Inclusive owned reserve"),
            )
            owned[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
        complete_manifest(
            {
                "schema": "a13-recovery-audit-root-integrity-manifest-v6",
                "files": owned,
                "frozen_inputs": _FROZEN,
                "external_runtime_inputs": _EXTERNAL,
                "manifest_self_hash_excluded": True,
                "completed": True,
                "passed": True,
                "budget_censored": False,
                "audit_manifest_SHA256": AUDIT_SHA,
                "audit_complete_counts": AUDIT_COUNTS,
                "source_ROOT_READY_SHA256": AUDIT_READY_SHA,
                "prepared_protocol_SHA256": PROTOCOL_SHA,
                "current_scoped_all20_certification_integrity_verified": True,
                "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
                "both_full_uncached_input_unions": [first, second],
                ("terminal_budget_observation"): {
                    ("process_CPU_seconds"): time.process_time(),
                    ("wall_seconds"): time.monotonic() - _STARTED,
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
                    ("passed"): True,
                    ("manifest_SHA256"): digest(OUTPUT / ("manifest.json"), fresh=True),
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
