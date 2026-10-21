"""Prospective A20 run004 failed metadata only; no scientific imports or approval.

This author-only method requires separate ROOT byte freeze and release.
The original FAILED_UNSEALED marker always overrides the partial summary.
"""

import argparse
import ast
import cProfile
import copy as ast_copy
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
from importlib.util import cache_from_source
import json
import os
from pathlib import Path, PureWindowsPath
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
AUTHOR = RESEARCH / "profile_a20_signal_run004_metadata_v2.py"
METHOD_DOC = RESEARCH / "A20_SIGNAL_RUN004_METADATA_PROFILE_PREFLIGHT_V2.md"
PREFLIGHT = RESEARCH / "a20_signal_run004_metadata_profile_preflight_v2.json"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
FAILED = PROGRAM / "A20_signal_semantics_run004"
CAPTURE = PROGRAM / "A20_signal_run004_terminal_failure_capture_run001"
FREEZE = ROOT / ".context/A20_signal_run004_FAILED_OWNED_FROZEN_run001.json"
FREEZE_SHA = "130f5e83d4ddb4a03a5921dfed47d86596795e2b82b97b1a0595238fb4179eb3"
ORIGINAL_READY = ROOT / ".context/A20_signal_producer_ROOT_READY_run004.json"
ORIGINAL_READY_SHA = "d5f65f8f710882783f042f070c161abebd15b44e5142f4e0baf3883a81498284"
PROTOCOL_SHA = "5b30e876fb4c39144001812dab74c874804f53420c49a6946edd5605972a318e"
RAW_LOG = ROOT / ".context/a20_signal_run004.log"
RAW_LOG_SHA = "35528e1d08ae389768bb89c4c714e610e139cffe5814dedcb47ddebefb672e13"
MARKER_SHA = "3aa5ecb0bd421846bc945790f0e6a0621b2f87d7c325e328768d14db30869322"
RECEIPT = RESEARCH / "a20_signal_receipt_v5.py"
RECEIPT_SHA = "c130a7eed0688faba014a36300bc01c6eadf162426b1f2a6e911096aa9a1fd8c"
AST_SHA = "cf3ee7dcd06f16c425eb9a109a6332407d04f3f77caa2b70d36d8f802cabcc92"
LEXICAL_AST_SHA = "5b0a927d371309242acdfb8bdada13adc4665206b806bbfbf223414c3c146eec"
V5_AUTHORS = {
    "arithmetic_free_basket_signal_v5.py": (
        "98a6fe0295e71da76ef6499ae52193cf00f86c120aa63d44edfd8b70e24551f5"
    ),
    "a20_signal_receipt_v5.py": RECEIPT_SHA,
    "experiment_arithmetic_free_basket_signal_v5.py": (
        "586b9b3e021b90a819b0b3efa8907c473b9054eb60bdf65305a4a7db40d471bc"
    ),
    "audit_arithmetic_free_basket_signal_v5.py": (
        "e1b63dcb68250763d545a6f0b3074ddce31b1221c839b8df0d4831ff7a507a67"
    ),
    "A20_COMPARATOR_PHASE_IMPLEMENTATION_PREFLIGHT_V5.md": (
        "4d98b1d5f1042f53c069c61b5bffac4a17333dc64afb9a7b0133d5e8cd010458"
    ),
    "a20_comparator_phase_implementation_preflight_v5.json": (
        "095a108aa9e0beb293eaf0067d2d3a193c60983344b6b4d3cba4ec5c14738445"
    ),
}

V1_AUTHORS = {
    "profile_a20_signal_run004_metadata_v1.py": (
        "bc7e62d736b922e155653c81a5e7ecbc1930b73008207b75cb85d4f2a97c0d0f"
    ),
    "A20_SIGNAL_RUN004_METADATA_PROFILE_PREFLIGHT_V1.md": (
        "2487f6b18e77f06da29763148b3b04ff0af2cfc4f216295387c2a25e313535df"
    ),
    "a20_signal_run004_metadata_profile_preflight_v1.json": (
        "8d57c4443320fd0143800853a1844393d992fc2206e7281e5e8853a0f4be1545"
    ),
}
LIFECYCLE_FUNCTION_COUNTS = {
    "canonical": 2,
    "add": 2,
    "read": 1,
    "inventory": 2,
    "own_runtime": 2,
    "standard_runtime_members": 3,
    "key_for": 1,
    "loaded_origins": 3,
    "original_scope_admission": 3,
    "admitted_metadata_bytes": 1,
    "admit_actual_capture": 1,
}
LIFECYCLE_INVERSE_AST_SHA = "2854226cd44929f22e96ee93a9e473a045e7d2b8f9df8c4042988442505d611f"
PRIOR_PROFILE_REFERENCES = {
    "OLD": {
        "output": (
            "results/limitation_program_20261001/A20_signal_run004_metadata_profile_old_run001"
        ),
        "owned_freeze_path": (
            ".context/A20_SIGNAL_OLD_METADATA_PROFILE_FAILED_OWNED_FROZEN_run001.json"
        ),
        "owned_freeze_SHA256": "f8aaa9750b27741e0bb33e29be1f0078902e409cd0ad6b9a7117962cf4279f42",
        "owned_freeze_schema": "root-a20-old-metadata-profile-failed-owned-freeze-v1",
        "owned_count": 9,
        "READY_path": ".context/A20_signal_run004_METADATA_PROFILE_OLD_ROOT_READY_run001.json",
        "READY_SHA256": "704ed9de48c63bfbfb5fd8aaa58c49f587ccdb530af814c663a680cde6823b55",
        "log_path": ".context/a20_signal_metadata_profile_old_run001.log",
        "log_SHA256": "e28649b8f7d24ac810e3bbfe2767ae2344dbd62e68b5cce071ad6dd244ce68a8",
        "marker_SHA256": "2157d817aa2725fd1aa22ad0a3b1f3a7099578045cca514fb5dc808768025033",
        "observed_measured_status_key": "completed_measured_union",
        "completed_measured_union": False,
        "failure_stage": (
            "measured_union/context.digest/Receipt.check Fixed A20 process CPU/wall guard"
        ),
        "all_saved_observations_unapproved": True,
    },
    "OPT": {
        "output": (
            "results/limitation_program_20261001/A20_signal_run004_metadata_profile_opt_run002"
        ),
        "owned_freeze_path": (
            ".context/A20_SIGNAL_OPT_METADATA_PROFILE_FAILED_OWNED_FROZEN_run002.json"
        ),
        "owned_freeze_SHA256": "43e18e8f704e1c6e65184efe8cf92f9c237e7f2164c7b12db9a7448d0e29cd5e",
        "owned_freeze_schema": "root-a20-opt-metadata-profile-failed-owned-freeze-v1",
        "owned_count": 11,
        "READY_path": ".context/A20_signal_run004_METADATA_PROFILE_OPT_ROOT_READY_run002.json",
        "READY_SHA256": "3cd1dfd62c4b5b3a87805b19af2a2a376630740c0ea8148601f08ed7fd84272c",
        "log_path": ".context/a20_signal_metadata_profile_opt_run002.log",
        "log_SHA256": "eb9c50c3c1626b999b4052af7b00f3ae7ffc9b4db2e58ec1f02f0a4eb362a7e2",
        "marker_SHA256": "2157d817aa2725fd1aa22ad0a3b1f3a7099578045cca514fb5dc808768025033",
        "observed_measured_status_key": "completed_measured_union_observed_not_approved",
        "completed_measured_union": True,
        "failure_stage": "second full fresh integrity union / Process CPU guard",
        "all_saved_observations_unapproved": True,
    },
}

CPU, ADMISSION, WALL = 180, 150, 600
WORK = ADMISSION
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
MAX_PROFILE_FUNCTIONS, MAX_PROFILE_BYTES = 10000, 8 * 1024**2
FAILURE_NAMES = (
    "FAILED_UNSEALED.json",
    "failed_unsealed.json",
    "failure.json",
    "run_failure.json",
    "prepare_failure.json",
)
_FROZEN, _EXTERNAL, _OBSERVED = {}, {}, {}
_PATH_CACHE, _HASH_CACHE = {}, {}
_OWN_INVENTORIES, _ABSENT_RUNTIME = {}, set()
_CODE_CACHE_EXPECTED = {}
_BASE_SCOPE, _EXCLUDED_SCOPE = None, None
_STANDARD_RUNTIME_MEMBERS = set()
_HASH_WORK = _REFERENCES = 0
_STARTED = None
_LEXICAL_PARTS_CACHE = {}
_LIFECYCLE_LEXICAL_PARTS_CACHE = {}
_HISTORICAL_ABSENT = set()
_HISTORICAL_FAILED = set()
_HISTORICAL_SEALED = set()
_ORIGINAL_FROZEN, _ORIGINAL_EXTERNAL, _FAILED_OWNED, _PREPARED_OWNED = {}, {}, {}, {}
_WORKLOAD = {}
_SOURCE_PROTOCOL = None


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
        not any((lifecycle_lexically_under(lexical, scope) for scope in _EXCLUDED_SCOPE)),
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
        not any((lifecycle_lexically_under(actual, scope) for scope in _EXCLUDED_SCOPE)),
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
        and all((char in "0123456789abcdef" for char in expected)),
        "Exact expected SHA",
    )
    actual = canonical(path)
    require(actual.is_file(), "Regular preserved input")
    if lifecycle_lexically_under(actual, ROOT):
        key, mapping = (actual.relative_to(ROOT).as_posix(), _FROZEN)
    else:
        require(lifecycle_lexically_under(actual, _BASE_SCOPE), "Actual external base runtime")
        key, mapping = (str(actual), _EXTERNAL)
    require(key not in mapping or mapping[key] == expected, "Canonical equal-SHA expectations")
    mapping[key] = expected
    return actual


def read(path):
    global _HASH_WORK
    budget()
    path = canonical(path)
    before = fingerprint(path)
    require(path.is_file() and before[2] <= 128 * 1024**2, "Bounded regular JSON input")
    chunks, total, state = ([], 0, hashlib.sha256())
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
        if lifecycle_lexically_under(path, ROOT)
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


def inventory(directory):
    found, total = (set(), 0)
    for root, dirs, names in os.walk(directory, followlinks=False):
        budget()
        for name in dirs:
            candidate = Path(root) / name
            require(
                lifecycle_lexically_under(canonical(candidate), directory),
                "No owned directory escape",
            )
            require(not candidate.is_symlink(), "No owned directory link")
        for name in names:
            actual = canonical(Path(root) / name)
            require(
                lifecycle_lexically_under(actual, directory) and actual not in found,
                "Unique owned path",
            )
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
        and (canonical(Path.cwd()) == ROOT),
        "Exact pinned launcher/cwd and startup -B",
    )
    require(
        not any((os.environ.get(key) for key in ("PYTHONPATH", "PYTHONHOME", "NUMBA_CACHE_DIR"))),
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
            not any((lifecycle_lexically_under(lexical, scope) for scope in _EXCLUDED_SCOPE))
            and (
                not any(
                    (
                        lifecycle_lexically_under(lexical.resolve(strict=False), scope)
                        for scope in _EXCLUDED_SCOPE
                    )
                )
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
            path in permitted
            or (path.is_file() and path.parent == base and (path.suffix == ".zip")),
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
    prefix = canonical(sys.prefix)
    site = canonical(prefix / "Lib/site-packages")
    candidates = set()
    excluded = base / "Lib/site-packages"
    trees = [base / "Lib", base / "DLLs", prefix / "Scripts"]
    for module in tuple(sys.modules.values()):
        budget()
        for field in ("__file__", "__cached__"):
            spelling = getattr(module, field, None)
            if not spelling:
                continue
            lexical = Path(os.path.abspath(str(spelling)))
            if lifecycle_lexically_under(lexical, site):
                parts = lexical.relative_to(site).parts
                if len(parts) > 1:
                    package = site / parts[0]
                    if package.is_dir():
                        trees.append(canonical(package))
    for tree in dict.fromkeys(trees):
        for root, dirs, names in os.walk(tree, topdown=True, followlinks=False):
            budget()
            dirs[:] = [name for name in dirs if Path(root) / name != excluded]
            for name in dirs:
                candidate = Path(root) / name
                require(
                    not candidate.is_symlink()
                    and lifecycle_lexically_under(canonical(candidate), tree),
                    "Every full runtime directory is confined without alias",
                )
            for name in names:
                candidate = canonical(Path(root) / name)
                require(
                    lifecycle_lexically_under(candidate, tree),
                    "Every full runtime member is confined",
                )
                candidates.add(candidate)
                require(len(candidates) <= MAX_RUNTIME_FILES, "Finite complete runtime membership")
    for directory in (base, prefix, site):
        for path in directory.iterdir():
            budget()
            if path.is_file():
                candidates.add(canonical(path))
                require(len(candidates) <= MAX_RUNTIME_FILES, "Finite adjacent runtime membership")
    return candidates


def key_for(path):
    return path.relative_to(ROOT).as_posix() if lifecycle_lexically_under(path, ROOT) else str(path)


def bind(path, expected):
    actual = add(path, expected)
    require(digest(actual) == expected, "Actual admitted expected bytes")
    return actual


def loaded_origins():
    forbidden = {"mpmath", "numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
    require(
        not any((name.split(".", 1)[0] in forbidden for name in sys.modules)),
        "No numerical or optional scientific imports",
    )
    require(
        not any(
            (
                name.startswith("research.")
                and name not in {__name__, "research.limitation_program_20261001"}
                for name in sys.modules
            )
        ),
        "No builder, producer, auditor or historical scientific imports",
    )
    for module in tuple(sys.modules.values()):
        budget()
        for attribute in ("__file__", "__cached__"):
            origin = getattr(module, attribute, None)
            if not origin:
                continue
            lexical = Path(os.path.abspath(str(origin)))
            require(
                not lifecycle_lexically_under(lexical, _EXCLUDED_SCOPE[0])
                and (
                    not lifecycle_lexically_under(lexical.resolve(strict=False), _EXCLUDED_SCOPE[1])
                ),
                "No excluded runtime origin or cache",
            )
            if lexical.is_file():
                actual = canonical(lexical, fresh=True)
                key = key_for(actual)
                mapping = _FROZEN if lifecycle_lexically_under(actual, ROOT) else _EXTERNAL
                if key not in mapping:
                    require(
                        not _STANDARD_RUNTIME_MEMBERS,
                        "No new loaded source/cache expectation after complete runtime admission",
                    )
                    add(actual, digest(actual, fresh=True, already_resolved=True))
                else:
                    require(
                        digest(actual, fresh=True, already_resolved=True) == mapping[key],
                        "Fresh loaded source/cache bytes equal admitted expectation",
                    )


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


def flags():
    return {
        "metadata_integrity_only": True,
        "new_scientific_evaluation": False,
        "original_scientific_attempt_passed": False,
        "original_failed_unsealed_authoritative": True,
        "original_terminal_CPU_and_wall_uncertified": True,
        "original_partial_summary_not_approval": True,
        "new_test_credit": 0,
        "new_credited_gate_replays": 0,
        "new_price_samples": 0,
        "full_G2": False,
        "financial_adoption": False,
        "adoption": False,
        "cost_transfer": False,
        "quantum_advantage": False,
        "scientific_V6_retry_authorized": False,
        "local_only": True,
    }


def expected_path(key):
    require(type(key) is str, "Exact expected-map string")
    path = Path(key)
    if path.is_absolute():
        require(str(path) == key, "Original external native path spelling")
        return path
    require(
        "\\" not in key
        and (ROOT / key).relative_to(ROOT).as_posix() == key
        and ".." not in path.parts,
        "Original ROOT-relative canonical spelling",
    )
    return ROOT / key


def join_workload(path, expected):
    budget()
    require(
        type(expected) is str
        and len(expected) == 64
        and all(char in "0123456789abcdef" for char in expected),
        "Exact expected full SHA",
    )
    require(
        path not in _WORKLOAD or _WORKLOAD[path] == expected,
        "Original expected maps and failure observations agree without replacement",
    )
    _WORKLOAD[path] = expected
    require(len(_WORKLOAD) <= MAX_REFERENCES, "Finite measured union")


def original_scope_admission():
    global _ORIGINAL_FROZEN, _ORIGINAL_EXTERNAL, _FAILED_OWNED, _PREPARED_OWNED, _SOURCE_PROTOCOL
    frozen = read(bind(FREEZE, FREEZE_SHA))
    require(
        frozen["schema"] == "A20-run004-post-failure-observed-owned-freeze-v1"
        and frozen["scope"] == "INTEGRITY_ONLY_FAILED_UNSEALED_NOT_SCIENTIFIC_APPROVAL",
        "Externally ROOT-frozen failure-only scope",
    )
    require(
        frozen["owned_files"] == 2945
        and frozen["owned_bytes"] == 116156575
        and (frozen["source_directory"] == FAILED.relative_to(ROOT).as_posix()),
        "Exact immutable failed inventory header",
    )
    require(
        frozen["original_prepared_protocol_expected_sha256"] == PROTOCOL_SHA
        and frozen["failure_marker_expected_sha256"] == MARKER_SHA
        and (frozen["raw_failure_log_expected_sha256"] == RAW_LOG_SHA)
        and (frozen["original_prepared_expectations_unchanged"] is True),
        "Original expectations and raw failure externally pinned",
    )
    _FAILED_OWNED = dict(frozen["observed_after_authoritative_failure_files"])
    require(
        len(_FAILED_OWNED) == 2945
        and _FAILED_OWNED.get("protocol.json") == PROTOCOL_SHA
        and (_FAILED_OWNED.get("FAILED_UNSEALED.json") == MARKER_SHA)
        and ("manifest.json" not in _FAILED_OWNED),
        "Complete separately identified post-failure observations",
    )
    failed_paths = set()
    for key, pin in _FAILED_OWNED.items():
        budget()
        require(
            type(key) is str
            and "\\" not in key
            and (not Path(key).is_absolute())
            and (".." not in Path(key).parts),
            "Strict failed-owned spelling",
        )
        member = bind(FAILED / key, pin)
        require(
            lifecycle_lexically_under(member, FAILED)
            and member.relative_to(FAILED).as_posix() == key
            and (member not in failed_paths),
            "Exact unique confined failed-owned member",
        )
        failed_paths.add(member)
        join_workload(member, pin)
    _OWN_INVENTORIES[FAILED] = failed_paths
    _HISTORICAL_FAILED.add(FAILED)
    require(
        inventory(FAILED) == failed_paths
        and sum((fingerprint(path)[2] for path in failed_paths)) == 116156575,
        "Complete actual failed-owned inventory and bytes",
    )
    source_ready = read(bind(ORIGINAL_READY, ORIGINAL_READY_SHA))
    require(
        source_ready["schema"] == "A20-comparator-phase-static-READY-v5"
        and source_ready["role"] == "producer"
        and (source_ready["budget"] == [CPU, ADMISSION, WALL])
        and (source_ready["output"] == FAILED.relative_to(ROOT).as_posix()),
        "Original actual producer release kept as history only",
    )
    authors = {
        (RESEARCH / key).relative_to(ROOT).as_posix(): pin for key, pin in V5_AUTHORS.items()
    }
    require(source_ready["author_sha256"] == authors, "All six immutable V5 expected authors")
    for key, pin in authors.items():
        bind(ROOT / key, pin)
    bind(RAW_LOG, RAW_LOG_SHA)
    protocol = read(FAILED / "protocol.json")
    _SOURCE_PROTOCOL = protocol
    require(
        protocol["schema"] == "A20-comparator-phase-prepared-protocol-v5"
        and protocol["role"] == "producer"
        and (protocol["root_READY_sha256"] == ORIGINAL_READY_SHA)
        and (protocol["budget"] == [CPU, ADMISSION, WALL]),
        "Exact unchanged original prepared protocol",
    )
    _ORIGINAL_FROZEN = dict(protocol["frozen_inputs"])
    _ORIGINAL_EXTERNAL = dict(protocol["external_runtime_inputs"])
    _PREPARED_OWNED = dict(protocol["prepared_owned_files_protocol_self_hash_excluded"])
    require(
        [len(_ORIGINAL_FROZEN), len(_ORIGINAL_EXTERNAL), len(_PREPARED_OWNED)]
        == [5950, 2842, 2932],
        "Complete original prepared counts remain exact",
    )
    for key, pin in _PREPARED_OWNED.items():
        budget()
        require(
            _FAILED_OWNED.get(key) == pin and key != "protocol.json",
            "Original prepared-owned expectation never replaced by a post-failure observation",
        )
    require(
        set(_PREPARED_OWNED) | {"protocol.json"} <= set(_FAILED_OWNED),
        "Protocol plus all original prepared files retained",
    )
    for mapping in (_ORIGINAL_FROZEN, _ORIGINAL_EXTERNAL):
        for key, pin in mapping.items():
            budget()
            path = expected_path(key)
            bind(path, pin)
            join_workload(path, pin)
    require(
        _ORIGINAL_FROZEN[ORIGINAL_READY.relative_to(ROOT).as_posix()] == ORIGINAL_READY_SHA
        and all((_ORIGINAL_FROZEN[key] == pin for key, pin in authors.items())),
        "Original prepared ROOT READY and all six original author expectations unchanged",
    )
    for spelling in protocol["runtime_absent"]:
        budget()
        absent = Path(spelling)
        require(
            absent.is_absolute()
            and str(absent) == spelling
            and (absent.resolve(strict=False) == absent)
            and (not absent.exists())
            and (not absent.is_symlink()),
            "Every original runtime absence physically exact",
        )
        _HISTORICAL_ABSENT.add(absent)
    runtime_paths = protocol["runtime_paths"]
    require(
        type(runtime_paths) is list
        and len(runtime_paths) == 2892
        and (len(set(runtime_paths)) == 2892)
        and (
            runtime_paths
            == [str(path) for path in sorted((Path(value) for value in runtime_paths))]
        ),
        "Complete original runtime path list retained",
    )
    runtime_copies = protocol["runtime_live_to_snapshot"]
    require(
        set(runtime_copies) == set(runtime_paths),
        "Complete original live-to-snapshot runtime witness",
    )
    witness_maps = (
        runtime_copies,
        protocol["immutable_V2_history_live_to_snapshot"],
        protocol["immutable_V3_history_live_to_snapshot"],
        protocol["held_V4_live_to_snapshot"],
        protocol["other_agent_static_text_live_to_snapshot"],
    )
    for mapping in witness_maps:
        for live, saved in mapping.items():
            budget()
            path = expected_path(live)
            saved_path = expected_path(saved)
            require(
                lifecycle_lexically_under(saved_path, FAILED),
                "Snapshot witness stays within failed receipt",
            )
            saved_relative = saved_path.relative_to(FAILED).as_posix()
            expected = (
                _ORIGINAL_FROZEN.get(path.relative_to(ROOT).as_posix())
                if lifecycle_lexically_under(path, ROOT)
                else _ORIGINAL_EXTERNAL.get(str(path))
            )
            require(
                expected is not None and _FAILED_OWNED.get(saved_relative) == expected,
                "Original live and snapshot expected SHA witnesses identical",
            )
    for name in (
        "immutable_V2_admission_failure_history",
        "immutable_V3_admission_failure_history",
    ):
        history = protocol[name]
        require(
            history["failed_before_receipt_mkdir"] is True
            and history["failure_not_promoted_or_repaired"] is True,
            "Original pre-mkdir failure history unchanged",
        )
        for route in history["historical_output_routes_absent"]:
            require(type(route) is str and Path(route).name == route, "Exact history route")
            _HISTORICAL_ABSENT.add(PROGRAM / route)
    _HISTORICAL_ABSENT.update(
        (
            PROGRAM / route
            for route in ("A20_signal_semantics_run003", "A20_signal_semantics_audit_run003")
        )
    )
    _HISTORICAL_ABSENT.update(
        (
            ROOT / ".context" / route
            for route in (
                "A20_signal_producer_ROOT_READY_run003.json",
                "A20_signal_audit_ROOT_READY_run003.json",
            )
        )
    )
    original_packet_witnesses(protocol)
    marker = read(FAILED / "FAILED_UNSEALED.json")
    require(
        marker["passed"] is False
        and marker["authoritative_failure"] is True
        and (marker["hard_budget_state_uncertified"] is True)
        and (marker["budget_censored"] is None)
        and (marker["new_test_credit"] == 0)
        and (marker["adoption"] is False),
        "Original authoritative hard-budget failure overrides all partial successes",
    )
    source_witnesses()
    return (frozen, protocol, source_ready)


def original_packet_witnesses(protocol):
    history = protocol["external_history_scope"]
    require(
        history["schema"] == "A20-fixed-external-history-scope-v1"
        and history["original_failed_unsealed_authoritative"] is True
        and history["general_historical_live_map_or_full_runtime_promotion"] is False,
        "Historical external packets remain metadata witnesses only",
    )
    require(len(history["manifest_expected_sha256"]) == 3, "Exact three original metadata packets")
    for directory_key, pin in history["manifest_expected_sha256"].items():
        budget()
        directory = expected_path(directory_key)
        mf = directory / "manifest.json"
        require(
            _ORIGINAL_FROZEN.get(mf.relative_to(ROOT).as_posix()) == pin,
            "Historical metadata manifest already an original strict expectation",
        )
        record = read(mf)
        require(
            record["passed"] is True and record["manifest_self_hash_excluded"] is True,
            "Original sealed metadata header",
        )
        owned = {mf}
        for key, expected in record["files"].items():
            budget()
            require(
                type(key) is str
                and "\\" not in key
                and not Path(key).is_absolute()
                and ".." not in Path(key).parts,
                "Exact historical packet-owned member",
            )
            member = directory / key
            require(
                member.relative_to(directory).as_posix() == key
                and member not in owned
                and _ORIGINAL_FROZEN.get(member.relative_to(ROOT).as_posix()) == expected,
                "Original complete packet-owned witness present without new admission",
            )
            owned.add(member)
        _OWN_INVENTORIES[directory] = owned
        _HISTORICAL_SEALED.add(directory)
    foreign = PROGRAM / "A20_continuation_20261004_producer_run002"
    record = read(
        PROGRAM
        / "A20_continuation_20261004_failure_capture_run001/failed_source_owned_inventory.json"
    )
    require(len(record) == 2900, "Complete original foreign failed-owned inventory retained")
    owned = set()
    for key, expected in record.items():
        budget()
        require(
            type(key) is str
            and "\\" not in key
            and not Path(key).is_absolute()
            and ".." not in Path(key).parts,
            "Strict original foreign failed spelling",
        )
        member = foreign / key
        require(
            member.relative_to(foreign).as_posix() == key
            and member not in owned
            and _ORIGINAL_FROZEN.get(member.relative_to(ROOT).as_posix()) == expected,
            "Every original foreign failed member retains its existing expected SHA",
        )
        owned.add(member)
    _OWN_INVENTORIES[foreign] = owned
    _HISTORICAL_FAILED.add(foreign)


def source_witnesses():
    budget()
    require(
        not (FAILED / "manifest.json").exists() and not (FAILED / "manifest.json").is_symlink(),
        "Original failed run stays unsealed",
    )
    for directory, expected in _OWN_INVENTORIES.items():
        budget()
        require(
            inventory(directory) == expected,
            "All original complete metadata/failed inventories unchanged",
        )
    for directory in _HISTORICAL_SEALED:
        require(
            not any(
                (directory / name).exists() or (directory / name).is_symlink()
                for name in FAILURE_NAMES
            ),
            "Original admitted metadata packet remains without authoritative failure",
        )
    for directory in _HISTORICAL_FAILED:
        require(
            (directory / "FAILED_UNSEALED.json").is_file()
            and not (directory / "manifest.json").exists()
            and not (directory / "manifest.json").is_symlink(),
            "Both immutable scientific failures remain authoritative and unsealed",
        )
    require(
        not any(
            path.exists() or path.is_symlink() or path.resolve(strict=False) != path
            for path in _HISTORICAL_ABSENT
        ),
        "All original runtime/history/held-release absences unchanged",
    )
    budget()


def fresh_union():
    runtime_scopes()
    for lexical, (actual, _) in tuple(_PATH_CACHE.items()):
        budget()
        require(
            canonical(lexical, fresh=True) == actual,
            "Every observed physical spelling freshly resolved",
        )
    union = {}
    for mapping in (_FROZEN, _EXTERNAL):
        for key, pin in mapping.items():
            budget()
            path = expected_path(key)
            require(path not in union or union[path] == pin, "Complete immutable equal-SHA union")
            union[path] = pin
    for path, pin in tuple(_OBSERVED.items()):
        budget()
        require(
            path not in union or union[path] == pin,
            "Actual observations never replace expectations",
        )
        union[path] = pin
    size = 0
    for path, pin in sorted(union.items()):
        budget()
        actual = canonical(path, fresh=True)
        size += fingerprint(actual)[2]
        require(len(union) <= MAX_REFERENCES and size <= MAX_UNIQUE_BYTES, "Full fresh union caps")
        require(
            digest(actual, fresh=True, already_resolved=True) == pin,
            "Full uncached fresh physical confinement and SHA",
        )
    source_witnesses()
    check_code_caches()
    require(
        standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS,
        "Complete current metadata runtime membership unchanged",
    )
    require(
        not any(path.exists() or path.is_symlink() for path in _ABSENT_RUNTIME),
        "All new code/standard-runtime absences remain exact",
    )
    loaded_origins()
    budget()
    return {"unique_paths": len(union), "unique_bytes": size, "full_fresh_resolve_and_SHA": True}


def release_admission(ready_sha):
    require(
        type(ready_sha) is str
        and len(ready_sha) == 64
        and all(char in "0123456789abcdef" for char in ready_sha),
        "Externally supplied exact ROOT release SHA",
    )
    ready = read(bind(READY, ready_sha))
    require(
        ready["schema"] == RELEASE_SCHEMA
        and ready["ready"] is True
        and ready["root_and_independent_static_reviews_passed"] is True
        and ready["metadata_execution_authorized"] is True,
        "Separate explicit ROOT metadata-only release",
    )
    require(
        ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and ready["mode"] == MODE,
        "Fixed role/route/unchanged CPU cap",
    )
    require(
        all(
            ready[key] is False
            for key in (
                "full_G2",
                "adoption",
                "cost_transfer",
                "quantum_advantage",
                "scientific_V6_retry_authorized",
            )
        )
        and ready["new_test_credit"] == 0,
        "No scientific, financial or retry permission",
    )
    require(
        ready["failed_owned_freeze_SHA256"] == FREEZE_SHA
        and ready["original_prepared_protocol_SHA256"] == PROTOCOL_SHA
        and ready["original_READY_SHA256"] == ORIGINAL_READY_SHA
        and ready["raw_failure_log_SHA256"] == RAW_LOG_SHA,
        "All failure/prior protocol external expectations exact",
    )
    paths = (AUTHOR, METHOD_DOC, PREFLIGHT)
    require(
        set(ready["author_method_SHA256"]) == {path.name for path in paths},
        "Exact new author/method trio",
    )
    for path in paths:
        bind(path, ready["author_method_SHA256"][path.name])
    require(
        ready["common_lifecycle_syntax_optimization_reviewed"] is True
        and ready["common_lifecycle_predicate_count"] == 21
        and ready["separate_measured_and_lifecycle_syntax_caches"] is True
        and ready["prior_profile_history"] == PRIOR_PROFILE_REFERENCES,
        "Fixed shared lexical optimization and externally frozen actual V1 history",
    )
    for name, pin in V1_AUTHORS.items():
        bind(RESEARCH / name, pin)
    policy = read(PREFLIGHT)
    require(
        policy["schema"] == POLICY_SCHEMA
        and policy["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and policy["failed_owned_freeze_SHA256"] == FREEZE_SHA
        and policy["original_prepared_protocol_SHA256"] == PROTOCOL_SHA
        and policy["source_method_AST_SHA256"] == AST_SHA
        and policy["lexical_helper_AST_SHA256"] == LEXICAL_AST_SHA
        and policy["common_lifecycle_function_counts"] == LIFECYCLE_FUNCTION_COUNTS
        and policy["common_lifecycle_inverse_AST_SHA256"] == LIFECYCLE_INVERSE_AST_SHA
        and policy["prior_profile_history"] == PRIOR_PROFILE_REFERENCES
        and ready["completed_failure_capture_manifest_SHA256"]
        == policy["completed_failure_capture_expected_SHA256"]
        and ready["completed_failure_capture_complete_counts"]
        == policy["completed_failure_capture_complete_counts"]
        == [15, 5975, 2842]
        and policy["new_test_credit"] == 0,
        "Exact prospective method/budget/provenance",
    )
    executables = {canonical(LAUNCHER), canonical(sys._base_executable)}
    require(
        len(executables) == 2 and canonical(sys._base_executable) == _BASE_SCOPE / "python.exe",
        "Actual distinct launcher and base interpreter",
    )
    seen = set()
    for spelling, pin in ready["interpreter_expected_SHA256"].items():
        member = canonical(spelling)
        require(member in executables and member not in seen, "Exact actual interpreter binding")
        bind(member, pin)
        seen.add(member)
    require(seen == executables, "Both actual executable pins supplied externally")
    code_caches(
        [AUTHOR], ready["existing_new_code_cache_SHA256"], ready["absent_new_code_cache_paths"]
    )
    lifecycle_method_guard()
    original_scope_admission()
    budget(admission=True)
    return ready, policy


def workload_records():
    return [
        {"path": key_for(path), "expected_SHA256": pin} for path, pin in sorted(_WORKLOAD.items())
    ]


def metadata_seal(summary, schema):
    save("summary.json", summary)
    save(
        "completion_outcome.json",
        {**summary, "failed": False, "authoritative_terminal_outcome": True},
    )
    owned, size = {}, 0
    for path in sorted(inventory(OUTPUT)):
        budget()
        size += fingerprint(path)[2]
        require(
            len(owned) < MAX_OWN_FILES - 1 and size <= MAX_OWN_BYTES,
            "Prospective inclusive own reserve",
        )
        owned[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
    complete_manifest(
        {
            "schema": schema,
            "passed": True,
            "completed": True,
            "budget_censored": False,
            "manifest_self_hash_excluded": True,
            "files": owned,
            "frozen_inputs": _FROZEN,
            "external_runtime_inputs": _EXTERNAL,
            **summary,
            **flags(),
        },
        owned,
        size,
    )


def retain_failure(error):
    if not OUTPUT.is_dir():
        return
    try:
        manifest = OUTPUT / "manifest.json"
        if manifest.exists():
            manifest.rename(OUTPUT / "failed_manifest_attempt.json")
    except OSError:
        pass
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
                b'{"passed":false,"completed":false,"authoritative_failure":true,"budget_censored":null,"hard_budget_state_uncertified":true,"new_test_credit":0,"adoption":false}\n'
            )
    except OSError:
        pass


LEXICAL_PATHS = (
    ".",
    "foo",
    "foo/bar",
    "foo/../bar",
    "../foo",
    "C:",
    "C:foo",
    "C:/",
    "C:/foo",
    "c:/FOO/bar",
    "C:/foobar",
    "D:/foo",
    "//server/share/",
    "//server/share/foo",
    "/foo",
    "C:/Stra\u00dfe/x",
    "C:/STRASSE/x",
    "C:/foo/../bar",
    "C:/\u0130/x",
    "C:/i\u0307/x",
    "C:/\u039f\u03a3/x",
    "C:/\u03bf\u03c2/x",
    "C:\u03a3",
    "C:\u03c3",
    "C:\u03c2",
)


LEXICAL_PARENTS = (
    ".",
    "foo",
    "foo/..",
    "..",
    "C:",
    "C:/",
    "c:/foo",
    "C:/foobar",
    "D:/",
    "//server/share/",
    "/foo",
    "C:/STRASSE",
    "C:/\u0130",
    "C:/\u039f\u03a3",
    "C:\u03a3",
    "C:\u03c3",
    "C:\u03c2",
)


def lexical_parts(path):
    """Immutable Windows syntax only; never a physical-resolution cache."""
    require(isinstance(path, (Path, PureWindowsPath)), "Only Windows path objects")
    key = str(path)
    if key not in _LEXICAL_PARTS_CACHE:
        require(len(_LEXICAL_PARTS_CACHE) < MAX_REFERENCES, "Bounded lexical syntax cache")
        _LEXICAL_PARTS_CACHE[key] = (
            path.anchor.lower(),
            tuple(part.lower() for part in path.parts),
        )
    return _LEXICAL_PARTS_CACHE[key]


def lexically_under(path, parent):
    """Exact Path.is_relative_to syntax predicate; aliases still resolve separately."""
    if (path.drive and not path.root) or (parent.drive and not parent.root):
        return path.is_relative_to(parent)
    anchor, parts = lexical_parts(path)
    root_anchor, root_parts = lexical_parts(parent)
    return (
        anchor == root_anchor
        and len(parts) >= len(root_parts)
        and parts[: len(root_parts)] == root_parts
    )


def lexical_equivalence():
    """One preregistered 25x17 Windows-syntax matrix; no filesystem observations."""
    records = []
    for raw in LEXICAL_PATHS:
        for root in LEXICAL_PARENTS:
            budget()
            value, parent = PureWindowsPath(raw), PureWindowsPath(root)
            expected = value.is_relative_to(parent)
            actual = lexically_under(value, parent)
            require(actual == expected, "Exact Windows lexical predicate parity")
            records.append({"path": raw, "parent": root, "matches": True, "result": actual})
    require(len(records) == 425, "Fixed lexical parity corpus")
    return records


def lifecycle_lexical_parts(path):
    """Immutable Windows syntax only; never a physical-resolution cache."""
    require(isinstance(path, (Path, PureWindowsPath)), "Only Windows path objects")
    key = str(path)
    if key not in _LIFECYCLE_LEXICAL_PARTS_CACHE:
        require(
            len(_LIFECYCLE_LEXICAL_PARTS_CACHE) < MAX_REFERENCES, "Bounded lexical syntax cache"
        )
        _LIFECYCLE_LEXICAL_PARTS_CACHE[key] = (
            path.anchor.lower(),
            tuple((part.lower() for part in path.parts)),
        )
    return _LIFECYCLE_LEXICAL_PARTS_CACHE[key]


def lifecycle_lexically_under(path, parent):
    """Exact Path.is_relative_to syntax predicate; aliases still resolve separately."""
    if path.drive and (not path.root) or (parent.drive and (not parent.root)):
        return path.is_relative_to(parent)
    anchor, parts = lifecycle_lexical_parts(path)
    root_anchor, root_parts = lifecycle_lexical_parts(parent)
    return (
        anchor == root_anchor
        and len(parts) >= len(root_parts)
        and (parts[: len(root_parts)] == root_parts)
    )


MODE = OUTPUT = READY = None
RELEASE_SCHEMA = "root-a20-run004-metadata-profile-READY-v2"
POLICY_SCHEMA = "a20-run004-metadata-profile-preflight-v2"


class LexicalReplacement(ast.NodeTransformer):
    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Attribute) and node.func.attr == "is_relative_to":
            require(
                len(node.args) == 1 and not node.keywords, "Exact one-argument relative predicate"
            )
            return ast.copy_location(
                ast.Call(
                    func=ast.Name(id="lexically_under", ctx=ast.Load()),
                    args=[node.func.value, node.args[0]],
                    keywords=[],
                ),
                node,
            )
        return node


def exact_metadata_context(mode):
    budget()
    require(
        digest(RECEIPT, fresh=True) == RECEIPT_SHA,
        "Exact already-admitted V5 receipt before metadata AST extraction",
    )
    content = admitted_metadata_bytes(RECEIPT)
    module = ast.parse(content, filename=str(RECEIPT))
    classes = [
        node for node in module.body if isinstance(node, ast.ClassDef) and node.name == "Receipt"
    ]
    require(len(classes) == 1, "Exact original Receipt class text")
    names = ("check", "stamp", "canonical", "digest")
    nodes = [
        ast_copy.deepcopy(node)
        for node in classes[0].body
        if isinstance(node, ast.FunctionDef) and node.name in names
    ]
    require(
        len(nodes) == 4 and {node.name for node in nodes} == set(names),
        "Only four selected metadata definitions",
    )
    require(
        all(
            not node.decorator_list
            or (
                node.name == "stamp"
                and len(node.decorator_list) == 1
                and isinstance(node.decorator_list[0], ast.Name)
                and node.decorator_list[0].id == "staticmethod"
            )
            for node in nodes
        ),
        "Only fixed inert staticmethod decorator",
    )
    selected = ast.Module(
        body=[
            ast.ClassDef(name="MetadataOnly", bases=[], keywords=[], body=nodes, decorator_list=[])
        ],
        type_ignores=[],
    )
    normalized = hashlib.sha256(ast.dump(selected, include_attributes=False).encode()).hexdigest()
    require(normalized == AST_SHA, "Exact source-extracted metadata AST pin")
    changes = 0
    if mode == "OPT":
        for node in nodes:
            if node.name == "canonical":
                changes = sum(
                    isinstance(child, ast.Call)
                    and isinstance(child.func, ast.Attribute)
                    and child.func.attr == "is_relative_to"
                    for child in ast.walk(node)
                )
                LexicalReplacement().visit(node)
        require(changes == 5, "Exactly five operational lexical predicates, unchanged control flow")
    ast.fix_missing_locations(selected)
    namespace = {
        "__name__": "a20_v5_metadata_only_definitions",
        "require": require,
        "Path": Path,
        "os": os,
        "ROOT": ROOT,
        "CPU": CPU,
        "WORK": WORK,
        "WALL": WALL,
        "time": time,
        "hashlib": hashlib,
        "lexically_under": lexically_under,
    }
    budget()
    exec(compile(selected, str(RECEIPT), "exec"), namespace)
    budget()
    require(
        set(namespace)
        - {
            "__name__",
            "require",
            "Path",
            "os",
            "ROOT",
            "CPU",
            "WORK",
            "WALL",
            "time",
            "hashlib",
            "lexically_under",
            "__builtins__",
        }
        == {"MetadataOnly"},
        "Only selected metadata class became executable; no constructor or science",
    )
    context = namespace["MetadataOnly"]()
    context.started = _STARTED
    context.base = _BASE_SCOPE
    context.excluded, context.excluded_actual = _EXCLUDED_SCOPE
    context.cache, context.physical, context.observed = {}, {}, {}
    context.hash_work = 0
    loaded_origins()
    return context, {
        "source_SHA256": RECEIPT_SHA,
        "original_metadata_AST_SHA256": normalized,
        "mode": mode,
        "selected_definitions": list(names),
        "source_Receipt_constructor_executed": False,
        "historical_module_imported": False,
        "scientific_definition_compiled_or_called": False,
        "exact_lexical_predicates_replaced": changes,
        "distinct_empty_actual_caches": True,
    }


def admitted_metadata_bytes(path):
    global _HASH_WORK
    actual = canonical(path)
    key = key_for(actual)
    expected = _FROZEN.get(key) if lifecycle_lexically_under(actual, ROOT) else _EXTERNAL.get(key)
    before = fingerprint(actual)
    require(
        expected is not None and before[2] <= 128 * 1024**2,
        "Only already-admitted bounded metadata source",
    )
    pieces, size, state = ([], 0, hashlib.sha256())
    with actual.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            budget()
            size += len(chunk)
            _HASH_WORK += len(chunk)
            require(
                size <= before[2] and _HASH_WORK <= MAX_HASH_WORK,
                "Charged complete metadata source read",
            )
            state.update(chunk)
            pieces.append(chunk)
    require(
        size == before[2] and fingerprint(actual) == before and (state.hexdigest() == expected),
        "Exact stable already-admitted source bytes",
    )
    return b"".join(pieces)


def lexical_method_guard():
    content = admitted_metadata_bytes(AUTHOR)
    parsed = ast.parse(content, filename=str(AUTHOR))
    constants = [
        node
        for node in parsed.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id in ("LEXICAL_PATHS", "LEXICAL_PARENTS")
            for target in node.targets
        )
    ]
    functions = [
        node
        for node in parsed.body
        if isinstance(node, ast.FunctionDef)
        and node.name in ("lexical_parts", "lexically_under", "lexical_equivalence")
    ]
    require(len(constants) == 2 and len(functions) == 3, "Exact inherited lexical corpus/helpers")
    selected = ast.Module(body=constants + functions, type_ignores=[])
    normalized = hashlib.sha256(ast.dump(selected, include_attributes=False).encode()).hexdigest()
    require(normalized == LEXICAL_AST_SHA, "Exact A13 V2 lexical corpus/helper AST expected pin")
    budget()
    return normalized


def lifecycle_method_guard():
    """Prove the exact shared syntax substitution from already-admitted V1 text."""
    parsed = ast.parse(admitted_metadata_bytes(AUTHOR), filename=str(AUTHOR))
    baseline_path = RESEARCH / "profile_a20_signal_run004_metadata_v1.py"
    baseline = ast.parse(admitted_metadata_bytes(baseline_path), filename=str(baseline_path))
    current = {node.name: node for node in parsed.body if isinstance(node, ast.FunctionDef)}
    original = {node.name: node for node in baseline.body if isinstance(node, ast.FunctionDef)}
    require(
        sum(
            isinstance(node, ast.FunctionDef) and node.name in LIFECYCLE_FUNCTION_COUNTS
            for node in parsed.body
        )
        == len(LIFECYCLE_FUNCTION_COUNTS)
        and sum(
            isinstance(node, ast.FunctionDef) and node.name in LIFECYCLE_FUNCTION_COUNTS
            for node in baseline.body
        )
        == len(LIFECYCLE_FUNCTION_COUNTS),
        "Exactly eleven unique shared lifecycle functions in each admitted controller",
    )

    class Inverse(ast.NodeTransformer):
        def __init__(self):
            self.count = 0

        def visit_Call(self, node):
            self.generic_visit(node)
            if isinstance(node.func, ast.Name) and node.func.id == "lifecycle_lexically_under":
                require(len(node.args) == 2 and not node.keywords, "Exact inverse lexical adapter")
                self.count += 1
                return ast.copy_location(
                    ast.Call(
                        func=ast.Attribute(
                            value=node.args[0], attr="is_relative_to", ctx=ast.Load()
                        ),
                        args=[node.args[1]],
                        keywords=[],
                    ),
                    node,
                )
            return node

    records, restored, total = [], [], 0
    for name, expected_count in LIFECYCLE_FUNCTION_COUNTS.items():
        budget()
        inverse = Inverse()
        node = inverse.visit(ast_copy.deepcopy(current[name]))
        require(
            inverse.count == expected_count
            and ast.dump(node, include_attributes=False)
            == ast.dump(original[name], include_attributes=False),
            "Shared function differs solely by its whitelisted lexical predicates",
        )
        restored.append(node)
        total += inverse.count
        records.append(
            {"function": name, "predicate_count": inverse.count, "inverse_AST_exact": True}
        )
    normalized = hashlib.sha256(
        ast.dump(ast.Module(body=restored, type_ignores=[]), include_attributes=False).encode()
    ).hexdigest()
    require(total == 21 and normalized == LIFECYCLE_INVERSE_AST_SHA, "Exact fixed inverse AST pin")

    class Rename(ast.NodeTransformer):
        names = {
            "lifecycle_lexical_parts": "lexical_parts",
            "lifecycle_lexically_under": "lexically_under",
            "_LIFECYCLE_LEXICAL_PARTS_CACHE": "_LEXICAL_PARTS_CACHE",
        }

        def visit_FunctionDef(self, node):
            node.name = self.names.get(node.name, node.name)
            self.generic_visit(node)
            return node

        def visit_Name(self, node):
            node.id = self.names.get(node.id, node.id)
            return node

    for original_name, adapter_name in (
        ("lexical_parts", "lifecycle_lexical_parts"),
        ("lexically_under", "lifecycle_lexically_under"),
    ):
        restored_helper = Rename().visit(ast_copy.deepcopy(current[adapter_name]))
        require(
            ast.dump(restored_helper, include_attributes=False)
            == ast.dump(original[original_name], include_attributes=False)
            == ast.dump(current[original_name], include_attributes=False),
            "Lifecycle helper is exact renamed inherited measured helper",
        )
    require(
        _LIFECYCLE_LEXICAL_PARTS_CACHE is not _LEXICAL_PARTS_CACHE,
        "Disjoint syntax caches prevent common lifecycle from warming measured OPT syntax",
    )
    return {
        "V1_source_expected_SHA256": V1_AUTHORS[baseline_path.name],
        "common_lifecycle_inverse_AST_SHA256": normalized,
        "functions": records,
        "total_whitelisted_lexical_predicates": total,
        "two_renamed_helpers_AST_exact": True,
        "separate_measured_and_lifecycle_syntax_caches": True,
        "each_syntax_cache_fixed_bound": MAX_REFERENCES,
        "source_extracted_measured_methods_unchanged": True,
    }


def lifecycle_lexical_equivalence():
    """The same fixed 425 cases also check the separate common lifecycle adapter."""
    records = []
    for raw in LEXICAL_PATHS:
        for root in LEXICAL_PARENTS:
            budget()
            value, parent = PureWindowsPath(raw), PureWindowsPath(root)
            expected = value.is_relative_to(parent)
            actual = lifecycle_lexically_under(value, parent)
            require(actual == expected, "Exact shared Windows lexical predicate parity")
            records.append({"path": raw, "parent": root, "matches": True, "result": actual})
    require(len(records) == 425, "Same fixed shared lexical parity corpus")
    return records


def admit_prior_profile_history(ready):
    """Retain fixed actual V1 terminals; these bytes never enter measured workload."""
    require(
        set(PRIOR_PROFILE_REFERENCES) == {"OLD", "OPT"}
        and ready["prior_profile_history"] == PRIOR_PROFILE_REFERENCES,
        "Both actual V1 histories externally expected before this prospective release",
    )
    before = workload_records()
    history = {}
    for mode in ("OLD", "OPT"):
        budget()
        reference = PRIOR_PROFILE_REFERENCES[mode]
        route = ROOT / reference["output"]
        require(
            route.parent == PROGRAM
            and route.name
            == "A20_signal_run004_metadata_profile_"
            + mode.lower()
            + ("_run001" if mode == "OLD" else "_run002"),
            "Exact immutable original profile route",
        )
        freeze = read(bind(ROOT / reference["owned_freeze_path"], reference["owned_freeze_SHA256"]))
        require(
            freeze["schema"] == reference["owned_freeze_schema"]
            and freeze["failed_route"] == reference["output"]
            and freeze["original_READY_expected_sha256"] == reference["READY_SHA256"]
            and freeze["original_failure_log_sha256"] == reference["log_SHA256"]
            and freeze["passed"] is False
            and freeze["original_terminal_CPU_wall_uncertified"] is True
            and freeze["original_scientific_run_passed"] is False
            and freeze["new_fixture_credit"] == 0,
            "Prior failed profile observations retain original expected release and raw log",
        )
        owned = freeze["observed_owned_files"]
        require(
            len(owned) == reference["owned_count"]
            and owned.get("FAILED_UNSEALED.json") == reference["marker_SHA256"]
            and "manifest.json" not in owned
            and freeze[reference["observed_measured_status_key"]]
            is reference["completed_measured_union"]
            and freeze["failure_stage"] == reference["failure_stage"]
            and freeze["scope"] == "FAILED_METADATA_DIAGNOSTIC_ONLY_NO_SPEED_RATIO"
            and reference["all_saved_observations_unapproved"] is True,
            "Complete fixed failed profile owned-map and actual measured status",
        )
        members = set()
        for key, pin in owned.items():
            budget()
            require(
                type(key) is str
                and "\\" not in key
                and not Path(key).is_absolute()
                and ".." not in Path(key).parts,
                "Strict prior profile-owned raw key",
            )
            member = bind(route / key, pin)
            require(
                lifecycle_lexically_under(member, route)
                and member.relative_to(route).as_posix() == key
                and member not in members,
                "Every prior failed profile member stays uniquely confined",
            )
            members.add(member)
        _OWN_INVENTORIES[route] = members
        _HISTORICAL_FAILED.add(route)
        prior_ready_path = bind(ROOT / reference["READY_path"], reference["READY_SHA256"])
        prior_ready = read(prior_ready_path)
        require(
            prior_ready["schema"] == "root-a20-run004-metadata-profile-READY-v1"
            and prior_ready["mode"] == mode
            and prior_ready["output"] == reference["output"]
            and prior_ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
            and prior_ready["author_method_SHA256"] == V1_AUTHORS,
            "Original V1 expected source and unchanged budget preserved",
        )
        code_caches(
            [RESEARCH / "profile_a20_signal_run004_metadata_v1.py"],
            prior_ready["existing_new_code_cache_SHA256"],
            prior_ready["absent_new_code_cache_paths"],
        )
        bind(ROOT / reference["log_path"], reference["log_SHA256"])
        marker = read(route / "FAILED_UNSEALED.json")
        require(
            marker["passed"] is False
            and marker["completed"] is False
            and marker["authoritative_failure"] is True
            and marker["budget_censored"] is None
            and marker["hard_budget_state_uncertified"] is True
            and marker["new_test_credit"] == 0
            and marker["adoption"] is False,
            "Prior failed profiles remain authoritative with uncertified terminal clocks",
        )
        require(inventory(route) == members, "Exact complete prior failed profile inventory")
        history[mode] = reference
    require(
        workload_records() == before, "Preserving profile history never changes measured workload"
    )
    source_witnesses()
    return history


def admit_actual_capture(ready):
    pin = ready["completed_failure_capture_manifest_SHA256"]
    require(
        type(pin) is str and len(pin) == 64 and all((char in "0123456789abcdef" for char in pin)),
        "Actual completed capture expected externally by ROOT",
    )
    mf = bind(CAPTURE / "manifest.json", pin)
    record = read(mf)
    require(
        record["schema"] == "a20-run004-failure-capture-manifest-v1"
        and record["passed"] is True
        and (record["completed"] is True)
        and (record["budget_censored"] is False)
        and (record["metadata_integrity_only"] is True)
        and (record["original_scientific_attempt_passed"] is False)
        and (record["original_failed_unsealed_authoritative"] is True)
        and (record["original_failed_owned_freeze_SHA256"] == FREEZE_SHA)
        and (record["original_prepared_protocol_SHA256"] == PROTOCOL_SHA)
        and (record["manifest_self_hash_excluded"] is True),
        "Capture PASS supplies metadata integrity only",
    )
    require(
        [len(record[field]) for field in ("files", "frozen_inputs", "external_runtime_inputs")]
        == ready["completed_failure_capture_complete_counts"],
        "Externally declared exact capture three-map counts",
    )
    owned = {mf}
    for key, expected in record["files"].items():
        budget()
        require(
            type(key) is str
            and "\\" not in key
            and (not Path(key).is_absolute())
            and (".." not in Path(key).parts),
            "Strict capture-owned key",
        )
        member = bind(CAPTURE / key, expected)
        require(
            lifecycle_lexically_under(member, CAPTURE)
            and member.relative_to(CAPTURE).as_posix() == key
            and (member not in owned),
            "Complete confined capture-owned member",
        )
        owned.add(member)
    _OWN_INVENTORIES[CAPTURE] = owned
    _HISTORICAL_SEALED.add(CAPTURE)
    for mapping in (record["frozen_inputs"], record["external_runtime_inputs"]):
        for key, expected in mapping.items():
            bind(expected_path(key), expected)
    capture_ready_path = ROOT / ".context/A20_signal_run004_FAILURE_CAPTURE_ROOT_READY_run001.json"
    require(
        capture_ready_path.relative_to(ROOT).as_posix() in _FROZEN,
        "Actual capture READY already admitted through the complete capture map",
    )
    capture_ready = read(capture_ready_path)
    require(
        capture_ready["schema"] == "root-a20-run004-failure-capture-READY-v1"
        and capture_ready["mode"] == "capture"
        and (capture_ready["output"] == CAPTURE.relative_to(ROOT).as_posix()),
        "Exact historical capture release and cache policy retained",
    )
    code_caches(
        [RESEARCH / "capture_a20_signal_run004_failure_v1.py"],
        capture_ready["existing_new_code_cache_SHA256"],
        capture_ready["absent_new_code_cache_paths"],
    )
    require(
        read(CAPTURE / "original_failed_owned_expected_map.json") == _FAILED_OWNED,
        "Complete capture failed map exactly ROOT-frozen observations",
    )
    require(
        read(CAPTURE / "original_prepared_expected_maps.json")
        == {
            "frozen_inputs": _ORIGINAL_FROZEN,
            "external_runtime_inputs": _ORIGINAL_EXTERNAL,
            "prepared_owned_protocol_self_hash_excluded": _PREPARED_OWNED,
            "protocol_expected_SHA256": PROTOCOL_SHA,
            "post_failure_observations_not_substituted": True,
        },
        "Capture preserves all original prepared expectations exactly",
    )
    require(
        read(CAPTURE / "ordered_original_metadata_workload.json") == workload_records(),
        "Identical full original ordered workload across both prospective modes",
    )
    source_witnesses()
    return pin


def profile_records(profiler):
    result = []
    entries = profiler.getstats()
    require(len(entries) <= MAX_PROFILE_FUNCTIONS, "Bounded retained profiler functions")
    for entry in entries:
        budget()
        code = entry.code
        name = (
            code
            if isinstance(code, str)
            else f"{code.co_filename}:{code.co_firstlineno}:{code.co_name}"
        )
        result.append(
            {
                "function": name,
                "call_count": entry.callcount,
                "recursive_calls": entry.reccallcount,
                "total_wall_seconds": entry.totaltime,
                "inline_wall_seconds": entry.inlinetime,
            }
        )
    result.sort(key=lambda record: record["function"])
    size = len(json.dumps(result, sort_keys=True, allow_nan=False).encode())
    require(size <= MAX_PROFILE_BYTES, "Bounded saved profiler metadata")
    return result


def measured_union(context):
    total, checked, result = 0, 0, []
    source_witnesses()
    for path, pin in sorted(_WORKLOAD.items()):
        context.check()
        total += context.stamp(path)[2]
        require(
            total <= MAX_UNIQUE_BYTES and len(_WORKLOAD) <= MAX_REFERENCES,
            "Same complete measured union caps",
        )
        actual = context.digest(path, fresh=True)
        require(actual == pin, "Same actual freshly resolved and full uncached SHA witness")
        result.append((key_for(path), actual))
        checked += 1
    source_witnesses()
    context.check()
    require(
        checked == len(_WORKLOAD) == len(context.observed) == len(context.cache),
        "Every unique complete workload path hashed once",
    )
    require(
        context.hash_work - context.initial_hash_work == total,
        "All full measured byte reads exactly charged to the inclusive hash ledger",
    )
    return {
        "unique_paths": checked,
        "unique_bytes": total,
        "actual_full_SHA_bytes": context.hash_work - context.initial_hash_work,
        "ordered_result_SHA256": hashlib.sha256(
            json.dumps(result, ensure_ascii=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "same_fresh_resolve_stat_reparse_SHA_witnesses": True,
        "actual_stat_and_hash_cache_reuse": False,
        "physical_cache_paths": len(context.physical),
    }


def main():
    global _STARTED, MODE, OUTPUT, READY, _HASH_WORK
    _STARTED = process_started()
    runtime_scopes()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256", required=True)
    parser.add_argument("--mode", choices=("OLD", "OPT"), required=True)
    args = parser.parse_args()
    MODE = args.mode
    number = "003" if MODE == "OLD" else "004"
    OUTPUT = PROGRAM / ("A20_signal_run004_metadata_profile_" + MODE.lower() + "_run" + number)
    READY = (
        ROOT
        / ".context"
        / ("A20_signal_run004_METADATA_PROFILE_" + MODE + "_ROOT_READY_run" + number + ".json")
    )
    require(
        canonical(__file__) == AUTHOR and not OUTPUT.exists(),
        "Exactly one separately released prospective mode; no rerun",
    )
    try:
        ready, _ = release_admission(args.ready_sha256)
        capture_pin = admit_actual_capture(ready)
        prior_history = admit_prior_profile_history(ready)
        runtime = own_runtime()
        first = fresh_union()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        for path in (AUTHOR, METHOD_DOC, PREFLIGHT, READY):
            copy(path, "executed_" + path.name)
        save(
            "run_started.json",
            {
                "created_UTC": datetime.now(timezone.utc).isoformat(),
                "PID": os.getpid(),
                "mode": MODE,
                **flags(),
            },
        )
        lexical_method_guard()
        parity = lexical_equivalence()
        save("lexical_predicate_equivalence.json", parity)
        lifecycle_guard = lifecycle_method_guard()
        save("common_lifecycle_AST_guard.json", lifecycle_guard)
        save("common_lifecycle_lexical_predicate_equivalence.json", lifecycle_lexical_equivalence())
        context, extraction = exact_metadata_context(MODE)
        save("extraction_and_scope.json", extraction)
        workload = workload_records()
        workload_sha = hashlib.sha256(
            json.dumps(workload, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode()
        ).hexdigest()
        save("ordered_original_metadata_workload.json", workload)
        _LEXICAL_PARTS_CACHE.clear()
        check_code_caches()
        require(
            standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS,
            "Complete admitted current runtime unchanged immediately before profiling",
        )
        loaded_origins()
        source_witnesses()
        budget(admission=True)
        require(
            not _LEXICAL_PARTS_CACHE and _LEXICAL_PARTS_CACHE is not _LIFECYCLE_LEXICAL_PARTS_CACHE,
            "Measured syntax cache remains empty after all common runtime/witness checks",
        )
        context.initial_hash_work = _HASH_WORK
        context.hash_work = _HASH_WORK
        profiler = cProfile.Profile()
        cpu, wall = time.process_time(), time.monotonic()
        profiler.enable()
        try:
            measured = measured_union(context)
        finally:
            profiler.disable()
        context.check()
        measured["process_CPU_seconds"] = time.process_time() - cpu
        measured["phase_wall_seconds"] = time.monotonic() - wall
        _HASH_WORK = context.hash_work
        require(
            _HASH_WORK <= MAX_HASH_WORK,
            "Combined admission/profile/terminal full hash work stays under24GiB",
        )
        save("measured_union.json", measured)
        save(
            "profile.json",
            {
                "mode": MODE,
                "default_wall_timer_and_overhead_charged": True,
                "entries": profile_records(profiler),
            },
        )
        loaded_origins()
        second = fresh_union()
        summary = {
            "scope": "METADATA_FRESH_UNION_TIMING_ONLY_NOT_COMPONENT_PASS",
            "mode": MODE,
            "passed": True,
            "completed": True,
            "budget_censored": False,
            "failure_capture_expected_manifest_SHA256": capture_pin,
            "original_prepared_protocol_SHA256": PROTOCOL_SHA,
            "original_failed_owned_freeze_SHA256": FREEZE_SHA,
            "source_method_AST_SHA256": AST_SHA,
            "fixed425_lexical_cases_passed": True,
            "common_lifecycle_fixed425_lexical_cases_passed": True,
            "common_lifecycle_AST_guard": lifecycle_guard,
            "prior_actual_V1_profile_history": prior_history,
            "lifecycle_cache_cannot_warm_measured_OPT_cache": True,
            "ordered_workload_SHA256": workload_sha,
            "measured_union": measured,
            "two_full_uncached_integrity_unions": [first, second],
            "current_metadata_runtime": runtime,
            "process_CPU_seconds": time.process_time(),
            "creation_wall_seconds": time.monotonic() - _STARTED,
            "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
            "not_a_classical_pricing_comparator": True,
            "no_bottleneck_or_speedup_claim_until_both_completed_modes": True,
            **flags(),
        }
        metadata_seal(summary, "a20-run004-metadata-profile-manifest-v2")
    except BaseException as error:
        retain_failure(error)
        raise


if __name__ == "__main__":
    main()
