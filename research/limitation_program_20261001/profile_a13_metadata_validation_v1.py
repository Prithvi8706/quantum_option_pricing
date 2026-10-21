"""Selected V5 metadata validation profile; no science or result approval.

Complete captured input maps and two fresh unions remain strict. The exact
frozen freeze_owner control flow is extracted only after actual byte admission.
No historical module or numerical definition is imported or evaluated.
"""

import argparse
import ast
import cProfile
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
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
AUTHOR = RESEARCH / "profile_a13_metadata_validation_v1.py"
PREFLIGHT = RESEARCH / "a13_metadata_validation_profile_preflight.json"
METHOD_DOC = RESEARCH / "A13_METADATA_VALIDATION_PROFILE_PREFLIGHT.md"
OUTPUT = PROGRAM / "A13_metadata_validation_profile_run001"
FAILED = PROGRAM / "A13_recovery_audit_run005"
CAPTURE = PROGRAM / "A13_recovery_audit_terminal_failure_capture_run005"
CAPTURE_SHA = "e6eef6653d70e0b5d61ea52162617cf551088c165b1ac1f1e2eb8d21f1c51a6b"
CAPTURE_CONTROLLER = RESEARCH / "capture_a13_recovery_audit_failure_v5.py"
CAPTURE_CONTROLLER_SHA = "4da5c31fab43ec3d27363923117325408adc469149d9a2e604dc5f8b96552280"
VERIFIER = RESEARCH / "audit_exp_frontier_recovery_v5.py"
VERIFIER_SHA = "c34f7096f783a61caa586c4e3f30067304da3d457626b367fd609ffebc2b2593"
ORIGINAL_METHOD = RESEARCH / "a13_exp_frontier_preflight.json"
ORIGINAL_METHOD_SHA = "6c0e97f33e1277c070e6e84883b6631a880997becd214772bb9ef287e1c7ba85"
PROTOCOL_SHA = "bc7dc2f880c31fdbc40543923d3b3d7e1faca27a154af9d8c03d6d72f8169bcb"
A07_SHA = "7380a91d89d4d7657533290406712139dee98913eef4ba60cb71e1de7e0e1f7e"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
ROOT_REVIEW = PROGRAM / "A13_recovery_root_review_run005"
ROOT_REVIEW_SHA = "0f39476d4e25793f7ee029d4df979d329e77a589623055e2bb307be890c2a9e4"
QA = PROGRAM / "A13_Bernstein_equivalence_check_run001"
QA_SHA = "574876915ac0418ab80d44f7763d98f4051b56a40f54d9e29717a8fff131401e"
ORIGIN = RESEARCH / "verify_exp_frontier_allocation_root_v2.py"
ORIGIN_SHA = "b0aac76928ad41a48cb1884d14f76168d8ef783595f918177857e5b13a91861f"
V5_AUTHORS = {
    "audit_exp_frontier_recovery_v5.py": (
        "c34f7096f783a61caa586c4e3f30067304da3d457626b367fd609ffebc2b2593"
    ),
    "A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V5.md": (
        "06ddca7b99dba0d44c5dcc7de7f27d5c26ea82691cf8bdccfe91a2d969ceae18"
    ),
    "a13_exp_frontier_recovery_audit_implementation_preflight_v5.json": (
        "c8d592ab4e6beb52b59bc4c3275ab9a33e7e898c94ef56a8a733be821f6d6693"
    ),
    "bernstein_integer_kernel_v5.py": (
        "695c10c095c17a0827d5e180195021828b1613e77cb22f6ead42783b7fa70048"
    ),
}
CPU, ADMISSION, WALL = 180, 150, 600
WORK_CPU, WORK_WALL = 120, 510
MAX_PROFILE_FUNCTIONS, MAX_PROFILE_BYTES = 10000, 8 * 1024**2
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
GRID = tuple((degree, count) for degree in (4, 6, 8, 10, 12) for count in (1, 2, 4, 8))
FAILURE_NAMES = ("FAILED_UNSEALED.json", "failure.json", "failed_unsealed.json")
_FROZEN, _EXTERNAL, _OBSERVED = {}, {}, {}
_ORIGINAL_FROZEN, _ORIGINAL_EXTERNAL, _OWNED_OBSERVATIONS, _MEMBERSHIPS = {}, {}, {}, []
_OWN_INVENTORIES, _ABSENT_RUNTIME = {}, set()
_PATH_CACHE, _HASH_CACHE = {}, {}
_BASE_SCOPE, _EXCLUDED_SCOPE = None, None
_STANDARD_RUNTIME_MEMBERS = set()
_HASH_WORK = _REFERENCES = 0
_STARTED = None
_PHASES, _PROFILE_COUNTS = [], {}
_PROFILER = None

# Bounded stdlib runtime and byte bookkeeping follows the frozen optimized
# root-verifier pattern, including explicit runtime membership rechecks.
# No historical module is imported.


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


def loaded_origins():
    forbidden = {"mpmath", "numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
    require(
        not any(name.split(".", 1)[0] in forbidden for name in sys.modules),
        "No optional/scientific kernels imported",
    )
    require(
        not any(
            name.startswith("research.")
            and name not in {__name__, "research.limitation_program_20261001"}
            for name in sys.modules
        ),
        "No historical scientific module imported",
    )
    for module in list(sys.modules.values()):
        for attr in ("__file__", "__cached__"):
            origin = getattr(module, attr, None)
            if not origin:
                continue
            lexical = Path(os.path.abspath(str(origin)))
            base_site = Path(sys.base_prefix) / "Lib/site-packages"
            require(
                not lexical.is_relative_to(base_site)
                and not lexical.resolve(strict=False).is_relative_to(base_site.resolve()),
                "No excluded loaded origin or cache",
            )
            if lexical.is_file():
                actual = canonical(lexical)
                require(
                    actual.is_relative_to(ROOT)
                    or actual.is_relative_to(canonical(sys.base_prefix)),
                    "Confined actual stdlib/owned origin",
                )
                key = (
                    actual.relative_to(ROOT).as_posix()
                    if actual.is_relative_to(ROOT)
                    else str(actual)
                )
                mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
                if key not in mapping:
                    add(actual, digest(actual))
                else:
                    require(digest(actual) == mapping[key], "Loaded origin same exact bytes")


def input_key(path):
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def bind_original(path, pin, owner, field, original_key):
    budget()
    actual = add(path, pin)
    target = _ORIGINAL_FROZEN if actual.is_relative_to(ROOT) else _ORIGINAL_EXTERNAL
    key = input_key(actual)
    require(key not in target or target[key] == pin, "No prior expected SHA replacement")
    target[key] = pin
    _MEMBERSHIPS.append(
        {
            "owner": owner,
            "source_map": field,
            "original_key": original_key,
            "verified_input_path": key,
            "original_expected_SHA256": pin,
            "expected_hash_waived": False,
        }
    )
    budget()
    return actual


def original_maps(document, owner, allow_absent_external=False):
    require(
        type(document.get("frozen_inputs")) is dict
        and (
            type(document.get("external_runtime_inputs")) is dict
            or (
                allow_absent_external is True
                and owner == QA.name
                and "external_runtime_inputs" not in document
            )
        ),
        "Complete original expected ROOT and external maps",
    )
    for field in ("frozen_inputs", "external_runtime_inputs"):
        for key, pin in document.get(field, {}).items():
            budget()
            require(type(key) is str, "Original map key")
            if field == "frozen_inputs":
                require(
                    not Path(key).is_absolute() and "\\" not in key and ".." not in Path(key).parts,
                    "Canonical prior ROOT-relative expected key",
                )
                path = ROOT / key
            else:
                require(Path(key).is_absolute(), "Canonical prior absolute external key")
                path = Path(key)
            actual = bind_original(path, pin, owner, field, key)
            require(input_key(actual) == key, "Exact original map key and scoped origin")
            require(
                actual.is_relative_to(ROOT) is (field == "frozen_inputs"),
                "Original expected scope retained",
            )
            budget()


def original_packet(directory, pin, counts):
    directory = canonical(directory)
    mf_path = bind_original(
        directory / "manifest.json", pin, directory.name, "manifest", "manifest.json"
    )
    document = read(mf_path)
    require(
        document.get("manifest_self_hash_excluded") is True
        and document.get("passed") is True
        and document.get("new_test_credit") == 0,
        "Pinned original owner packet, finite QA or static provenance only",
    )
    require(
        [
            len(document.get(key, {}))
            for key in ("files", "frozen_inputs", "external_runtime_inputs")
        ]
        == counts,
        "Exact complete original packet maps",
    )
    actual_owned = set()
    for key, expected in document["files"].items():
        budget()
        require(
            type(key) is str
            and not Path(key).is_absolute()
            and "\\" not in key
            and ".." not in Path(key).parts,
            "Canonical original owned member",
        )
        root_relative = key.startswith("results/")
        member = bind_original(
            ROOT / key if root_relative else directory / key,
            expected,
            directory.name,
            "files",
            key,
        )
        require(
            member.is_relative_to(directory)
            and member != mf_path
            and member not in actual_owned
            and member.relative_to(ROOT if root_relative else directory).as_posix() == key,
            "Exact confined unique original owned member",
        )
        actual_owned.add(member)
    original_maps(
        document,
        directory.name,
        allow_absent_external=(directory == QA and pin == QA_SHA),
    )
    _OWN_INVENTORIES[directory] = actual_owned | {mf_path}
    require(inventory(directory) == _OWN_INVENTORIES[directory], "Exact original owner inventory")
    return document


def fresh_union():
    runtime_scopes()
    for lexical, (previous, _) in tuple(_PATH_CACHE.items()):
        budget()
        require(
            canonical(lexical, fresh=True) == previous, "Every original lexical alias unchanged"
        )
    union = {}
    for mapping in (_FROZEN, _EXTERNAL):
        for key, pin in mapping.items():
            budget()
            path = Path(key) if Path(key).is_absolute() else ROOT / key
            require(path not in union or union[path] == pin, "Equal complete union expectations")
            union[path] = pin
    for path, pin in tuple(_OBSERVED.items()):
        budget()
        require(
            path not in union or union[path] == pin, "Observed bytes never replace expectations"
        )
        union[path] = pin
    total = 0
    for path, pin in sorted(union.items()):
        budget()
        actual = canonical(path, fresh=True)
        total += actual.stat().st_size
        require(len(union) <= MAX_REFERENCES and total <= MAX_UNIQUE_BYTES, "Finite complete union")
        require(
            digest(actual, fresh=True, already_resolved=True) == pin, "Fresh complete SHA equality"
        )
    for directory, members in _OWN_INVENTORIES.items():
        budget()
        require(inventory(directory) == members, "Every preserved original inventory unchanged")
    require(
        standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS,
        "Captured current metadata runtime membership unchanged",
    )
    require(
        not any(path.exists() for path in _ABSENT_RUNTIME), "Absent standard zip remains absent"
    )
    for name in (
        "summary.json",
        "fixed_inventory_authorization.json",
        "manifest.json",
        "completion_outcome.json",
    ):
        require(not (FAILED / name).exists(), "Old failure remains unsealed and unapproved")
    budget()
    return {"unique_paths": len(union), "unique_bytes": total, "full_fresh_resolve_and_SHA": True}


def save(name, value):
    budget()
    path = OUTPUT / name
    require(path.parent == OUTPUT and not path.exists(), "Exclusive new metadata artifact")
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        for fragment in json.JSONEncoder(indent=2, sort_keys=True, allow_nan=False).iterencode(
            value
        ):
            budget()
            stream.write(fragment)
        stream.write("\n")
    budget()
    require(path.stat().st_size <= MAX_OWN_BYTES, "Own metadata file cap")


def copy_input(path, name):
    actual = canonical(path)
    before, pin = fingerprint(actual), digest(actual)
    with actual.open("rb") as incoming, (OUTPUT / name).open("xb") as outgoing:
        total = 0
        while chunk := incoming.read(1 << 20):
            budget()
            total += len(chunk)
            require(total <= before[2], "Stable bounded input copy")
            outgoing.write(chunk)
            budget()
    require(total == before[2] and fingerprint(actual) == before, "Immutable copy source")
    require(digest(OUTPUT / name) == pin, "Exact current capture code/preflight copy")


def admitted_utf8_text(path):
    global _HASH_WORK
    actual = canonical(path)
    before, total, chunks, state = fingerprint(actual), 0, [], hashlib.sha256()
    require(before[2] <= MAX_OWN_BYTES, "Bounded original log metadata read")
    with actual.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            budget()
            total += len(chunk)
            _HASH_WORK += len(chunk)
            require(total <= before[2] and _HASH_WORK <= MAX_HASH_WORK, "Charged stable log read")
            state.update(chunk)
            chunks.append(chunk)
            budget()
    require(total == before[2] and fingerprint(actual) == before, "Original log bytes unchanged")
    require(state.hexdigest() == _FROZEN[input_key(actual)], "Original log expected captured bytes")
    budget()
    decoded = b"".join(chunks).decode("utf-8")
    budget()
    return decoded


class MetadataWorkCensoredError(RuntimeError):
    pass


def observation():
    return {"process_CPU_seconds": time.process_time(), "wall_seconds": time.monotonic() - _STARTED}


def phase(name, before):
    budget()
    after = observation()
    _PHASES.append(
        {
            "phase": name,
            "before": before,
            "after": after,
            "process_CPU_seconds": after["process_CPU_seconds"] - before["process_CPU_seconds"],
            "wall_seconds": after["wall_seconds"] - before["wall_seconds"],
        }
    )


def work_check(started, *, admission=False):
    """Original V5 limits first, then stricter diagnostic and retention reserve."""
    require(started == _STARTED, "One creation clock, never reset")
    cpu, wall = time.process_time(), time.monotonic() - started
    require(cpu < (270 if admission else 300) and wall < 900, "Original V5 guard retained")
    budget(admission=admission)
    if cpu >= WORK_CPU or wall >= WORK_WALL:
        raise MetadataWorkCensoredError("Fixed120CPU/510wall selected-work retention reserve")
    _PROFILE_COUNTS["checkpoint_calls"] = _PROFILE_COUNTS.get("checkpoint_calls", 0) + 1


def metadata_bind(frozen, external, path, pin, started):
    work_check(started)
    require(type(pin) is str and len(pin) == 64, "Typed original expected SHA")
    actual = add(path, pin)
    # Expectations never enter the actual-byte cache. Only an observed digest can.
    require(digest(actual) == pin, "Selected original current/archive SHA equality")
    mapping = frozen if actual.is_relative_to(ROOT) else external
    key = input_key(actual)
    require(key not in mapping or mapping[key] == pin, "Exact diagnostic adapter equal-SHA map")
    mapping[key] = pin
    _PROFILE_COUNTS["bind_adapter_calls"] = _PROFILE_COUNTS.get("bind_adapter_calls", 0) + 1
    work_check(started)
    return actual


def metadata_read(path, started):
    work_check(started)
    result = read(path)
    _PROFILE_COUNTS["JSON_adapter_calls"] = _PROFILE_COUNTS.get("JSON_adapter_calls", 0) + 1
    _PROFILE_COUNTS["JSON_adapter_bytes"] = (
        _PROFILE_COUNTS.get("JSON_adapter_bytes", 0) + canonical(path).stat().st_size
    )
    work_check(started)
    return result


def metadata_canonical(path, started):
    work_check(started)
    result = canonical(path)
    _PROFILE_COUNTS["canonical_adapter_calls"] = (
        _PROFILE_COUNTS.get("canonical_adapter_calls", 0) + 1
    )
    work_check(started)
    return result


def metadata_sha(path, started):
    work_check(started)
    result = digest(path)
    _PROFILE_COUNTS["SHA_adapter_calls"] = _PROFILE_COUNTS.get("SHA_adapter_calls", 0) + 1
    work_check(started)
    return result


def exact_metadata_functions():
    """Compile only two pinned metadata definitions, never the historical module."""
    budget(admission=True)
    require(digest(VERIFIER, fresh=True) == VERIFIER_SHA, "Exact V5 source before AST extraction")
    text = admitted_utf8_text(VERIFIER)
    tree = ast.parse(text, filename=str(VERIFIER))
    budget()
    names = ("no_failure", "freeze_owner")
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
    require(
        len(nodes) == 2 and {node.name for node in nodes} == set(names), "Exact two definitions"
    )
    for node in nodes:
        require(not node.decorator_list, "No executable extraction decorators")
    module = ast.Module(body=nodes, type_ignores=[])
    normalized = ast.dump(module, include_attributes=False)
    budget()
    namespace = {
        "__name__": "a13_v5_selected_metadata_definitions",
        "ROOT": ROOT,
        "PROGRAM": PROGRAM,
        "Path": Path,
        "require": require,
        "check": work_check,
        "bind": metadata_bind,
        "read_json": metadata_read,
        "canonical_path": metadata_canonical,
        "sha": metadata_sha,
    }
    code = compile(module, str(VERIFIER), "exec")
    budget()
    exec(code, namespace)
    budget()
    require(
        set(namespace)
        - {
            "__name__",
            "__builtins__",
            "ROOT",
            "PROGRAM",
            "Path",
            "require",
            "check",
            "bind",
            "read_json",
            "canonical_path",
            "sha",
        }
        == set(names),
        "Only metadata functions became executable",
    )
    require(
        not any(
            name.startswith("research.limitation_program_20261001.audit_") for name in sys.modules
        )
        and "mpmath" not in sys.modules,
        "No historical auditor or scientific module imported",
    )
    return namespace, {
        "source_path": VERIFIER.relative_to(ROOT).as_posix(),
        "source_SHA256": VERIFIER_SHA,
        "exact_extracted_definitions": list(names),
        "normalized_AST_SHA256": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
        "historical_module_imported": False,
        "scientific_definitions_compiled_or_called": False,
        "checked_adapters": ["bind", "read_json", "canonical_path", "sha", "check", "require"],
        "adapter_timings_not_identical_to_V5_helpers": True,
        "original_owner_entries_is_unused_in_V5_and_not_profiled": True,
    }


def selected_membership_scan(pins, records, frozen, external):
    """Exact selected_inputs existential scan; every record remains present."""
    selected = []
    for key, pin in pins.items():
        work_check(_STARTED)
        actual = metadata_bind(frozen, external, ROOT / key, pin, _STARTED)
        if not key.endswith("/manifest.json"):
            found = False
            for row in records:
                work_check(_STARTED)
                _PROFILE_COUNTS["selected_membership_record_comparisons"] = (
                    _PROFILE_COUNTS.get("selected_membership_record_comparisons", 0) + 1
                )
                if (
                    row["verified_input_path"] == actual.relative_to(ROOT).as_posix()
                    and row["original_expected_sha256"] == pin
                ):
                    found = True
                    break
            require(found, "Exact original equal-SHA selected membership")
            selected.append({"path": key, "SHA256": pin, "membership_found": True})
    return selected


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
    budget()
    entries = profiler.getstats()
    require(len(entries) <= MAX_PROFILE_FUNCTIONS, "Finite profile function count")
    records, edge_count = [], 0
    for entry in entries:
        budget()
        callees = []
        for call in entry.calls or ():
            budget()
            edge_count += 1
            require(edge_count <= 100000, "Finite profile call graph")
            callees.append(
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
                **function_key(entry.code),
                calls=entry.callcount,
                recursive_calls=entry.reccallcount,
                total_wall_seconds=entry.inlinetime,
                cumulative_wall_seconds=entry.totaltime,
                callees=callees,
            )
        )
    records.sort(
        key=lambda row: (-row["cumulative_wall_seconds"], row["file"], row["line"], row["function"])
    )
    budget()
    return {
        "schema": "a13-selected-metadata-validation-cProfile-v1",
        "timer": "cProfile default wall timer",
        "profiling_overhead_included": True,
        "complete_V5_source_packet_profile": False,
        "complete_prepare_or_run_profile": False,
        "scientific_or_native_kernel_profile": False,
        "input_SHA_cache_warm_from_prior_complete_union": True,
        "unprofiled_speedup_or_budget_fit_claim": False,
        "function_count": len(records),
        "call_graph_edges": edge_count,
        "all_function_records": records,
        "top50_cumulative_wall_seconds": records[:50],
        "adapter_counters": _PROFILE_COUNTS,
        "new_test_credit": 0,
    }


def scope_flags():
    return {
        "scientific_execution": False,
        "scientific_module_import_or_proof_calls": False,
        "gzip_decompression_or_native_source_DAG_walk": False,
        "new_test_credit": 0,
        "new_gate_replays": 0,
        "new_price_samples": 0,
        "mathematical_result_or_row_approval": False,
        "all20_approval": False,
        "candidate_selection": False,
        "gate_emission_authorized": False,
        "full_G2": False,
        "adoption": False,
        "cost_transfer": False,
        "original_attempt_failed": True,
        "original_attempt_sealed": False,
        "original_expected_hashes_waived": False,
    }


def admitted_failed_capture():
    capture = original_packet(CAPTURE, CAPTURE_SHA, [7, 1146, 2842])
    summary = read(CAPTURE / "summary.json")
    require(
        capture["schema"] == "a13-audit005-unsealed-failure-metadata-capture-manifest-v1"
        and capture["diagnostic_integrity"] is True
        and capture["original_attempt_failed"] is True
        and capture["original_attempt_sealed"] is False
        and summary["scientific_execution"] is False
        and summary["partial_rows_unapproved"] is True
        and summary["original_prepared_expected_maps_preserved_in_full"] is True,
        "Actual capture approves only failed-byte integrity",
    )
    members = read(CAPTURE / "untrusted_failed_material_index.json")
    require(type(members) is dict and len(members) == 50, "All50 captured old owned bytes")
    found = set()
    total = 0
    for key, row in members.items():
        budget()
        actual = bind_original(
            ROOT / key, row["SHA256"], CAPTURE.name, "untrusted_owned_index", key
        )
        require(actual.is_relative_to(FAILED) and actual not in found, "Exact old failed inventory")
        require(
            row["scientific_claims_trusted"] is False and actual.stat().st_size == row["bytes"],
            "Opaque failed bytes",
        )
        found.add(actual)
        total += row["bytes"]
    require(inventory(FAILED) == found and total == 25959363, "Complete old50 inventory unchanged")
    _OWN_INVENTORIES[FAILED] = found
    rows = {path.relative_to(FAILED).as_posix() for path in found if path.parent == FAILED / "rows"}
    require(
        rows == {f"rows/d{d}_s{s}.json.gz" for d, s in GRID[:18]}, "Only18 opaque unapproved rows"
    )
    marker, failure = read(FAILED / "FAILED_UNSEALED.json"), read(FAILED / "failure.json")
    require(
        marker == summary["original_marker"] and failure == summary["original_failure_metadata"],
        "Actual authoritative failure unchanged",
    )
    require(
        marker["failed"] is True
        and marker["passed"] is False
        and marker["budget_censored"] is None
        and marker["hard_budget_state_uncertified"] is True
        and failure["error_type"] == "BudgetCensoredError"
        and failure["new_test_credit"] == 0,
        "No old failure promotion",
    )
    protocol_path = bind_original(
        FAILED / "protocol.json", PROTOCOL_SHA, FAILED.name, "prepared_protocol", "protocol.json"
    )
    protocol = read(protocol_path)
    require(
        protocol["operational_recovery_audit_version"] == 5
        and protocol["CPU_admission_wall_seconds"] == [300, 270, 900]
        and protocol["independent_digits"] == 130
        and protocol["primary_digits"] == 90
        and protocol["threads"] == 1
        and [len(protocol["frozen_inputs"]), len(protocol["external_runtime_inputs"])]
        == [1099, 2842],
        "Original prepared scientific contract remains unchanged",
    )
    for field in ("frozen_inputs", "external_runtime_inputs"):
        for key, pin in protocol[field].items():
            budget()
            require(
                capture[field].get(key) == pin, "Every prepared expectation preserved in capture"
            )
    original_maps(protocol, FAILED.name + "/protocol.json")
    return capture, summary, protocol


def retain_failure(error):
    if not OUTPUT.is_dir():
        return
    try:
        budget()
        require(
            not (OUTPUT / "manifest.json").exists()
            and not (OUTPUT / "completion_outcome.json").exists(),
            "Partial terminal cannot be resealed or overwritten",
        )
        save(
            "failure.json",
            {
                "failed": True,
                "passed": False,
                "error_type": type(error).__name__,
                "error": str(error),
                "new_test_credit": 0,
                "scientific_execution": False,
            },
        )
    except BaseException:
        pass
    try:
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"failed":true,"passed":false,"diagnostic_integrity":false,"budget_censored":null,"hard_budget_state_uncertified":true,"partial_success_invalid":true,"new_test_credit":0,"scientific_execution":false}\n'
            )
    except OSError:
        pass


def main():
    global _STARTED, _PROFILER
    _STARTED = process_started()
    runtime_scopes()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--author-sha256", required=True)
    parser.add_argument("--preflight-sha256", required=True)
    args = parser.parse_args()
    require(
        canonical(__file__) == AUTHOR and not OUTPUT.exists(), "Fresh fixed diagnostic, no retry"
    )
    try:
        add(AUTHOR, args.author_sha256)
        add(PREFLIGHT, args.preflight_sha256)
        policy = read(PREFLIGHT)
        require(
            policy["schema"] == "a13-selected-metadata-validation-profile-preflight-v1"
            and policy["author_SHA256"] == args.author_sha256
            and policy["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
            and policy["selected_work_CPU_wall"] == [WORK_CPU, WORK_WALL]
            and policy["new_owned_caps_files_bytes"] == [MAX_OWN_FILES, MAX_OWN_BYTES]
            and policy["runtime_caps_files_bytes"] == [MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES]
            and policy["reference_unique_bytes_hash_work_caps"]
            == [MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK]
            and policy["fresh_receipt"] == OUTPUT.relative_to(ROOT).as_posix()
            and policy["failed_capture_manifest_SHA256"] == CAPTURE_SHA
            and policy["frozen_V5_source_SHA256"] == VERIFIER_SHA
            and policy["original_prepared_protocol_SHA256"] == PROTOCOL_SHA
            and policy["original_scientific_limits_CPU_admission_wall"] == [300, 270, 900]
            and policy["scientific_execution"] is False
            and policy["new_test_credit"] == 0,
            "Externally pinned fixed metadata-only scope and budgets",
        )
        add(METHOD_DOC, policy["method_document_SHA256"])
        add(CAPTURE_CONTROLLER, CAPTURE_CONTROLLER_SHA)
        add(ORIGIN, ORIGIN_SHA)
        before = observation()
        capture, failure_summary, protocol = admitted_failed_capture()
        review = original_packet(ROOT_REVIEW, ROOT_REVIEW_SHA, [1, 49, 0])
        require(review["ready"] is True, "Original V5 review static only")
        qa = original_packet(QA, QA_SHA, [2, 6, 0])
        require(qa["completed"] is True, "Finite QA is not all20 science approval")
        for name, pin in V5_AUTHORS.items():
            budget()
            bind_original(RESEARCH / name, pin, "actual_frozen_v5", "author", name)
        add(ORIGINAL_METHOD, ORIGINAL_METHOD_SHA)
        method = read(ORIGINAL_METHOD)
        require(method["schema"] == "a13-exp-frontier-author-preflight-v1", "Held original method")
        pins = method["selected_existing_manifest_expected_pins"]
        require(
            type(pins) is dict and len(pins) == 20,
            "All20 fixed selected pins, no outcome selection",
        )
        owners = {key: pin for key, pin in pins.items() if key.endswith("/manifest.json")}
        owners["results/limitation_program_20261001/A07_run003/manifest.json"] = A07_SHA
        require(
            owners == policy["fixed_profile_owner_manifest_SHA256"],
            "Exactly the four fixed actual selected_inputs owners",
        )
        require(len(owners) == 4, "Fixed finite owner count")
        for key, pin in owners.items():
            budget()
            require(
                protocol["frozen_inputs"].get(key) == pin,
                "Every selected owner retains prepared expectation",
            )
            bind_original(ROOT / key, pin, "actual_selected_inputs", "manifest", key)
        runtime = own_runtime()
        phase("complete_captured_maps_and_current_runtime_admission", before)
        before = observation()
        first = fresh_union()
        phase("first_full_uncached_resolve_and_SHA_union", before)
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        copy_input(AUTHOR, "executed_profile_controller.py")
        copy_input(PREFLIGHT, "executed_profile_preflight.json")
        copy_input(METHOD_DOC, "executed_profile_method.md")
        namespace, extraction = exact_metadata_functions()
        save("extraction_and_scope.json", extraction)
        save(
            "run_started.json",
            dict(
                created_UTC=datetime.now(timezone.utc).isoformat(),
                PID=os.getpid(),
                limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
                selected_work_CPU_wall=[WORK_CPU, WORK_WALL],
                **scope_flags(),
            ),
        )
        records, selected = [], []
        selected_frozen, selected_external = {}, {}
        _PROFILER = cProfile.Profile()
        before = observation()
        _PROFILER.enable()
        try:
            for key, pin in owners.items():
                work_check(_STARTED, admission=True)
                owner_before = observation()
                owner_records = namespace["freeze_owner"](
                    ROOT / key, pin, selected_frozen, selected_external, _STARTED
                )
                receipt = (ROOT / key).parent
                owned = {canonical(ROOT / key)}
                for row in owner_records:
                    work_check(_STARTED)
                    if row["source_map"] in ("files", "flat_owned_files"):
                        owned.add(canonical(ROOT / row["verified_input_path"]))
                require(inventory(receipt) == owned, "Selected original full owned inventory")
                _OWN_INVENTORIES[receipt] = owned
                records.extend(owner_records)
                _PROFILE_COUNTS["owner_map_records"] = _PROFILE_COUNTS.get(
                    "owner_map_records", 0
                ) + len(owner_records)
                phase("exact_freeze_owner:" + key, owner_before)
            scan_before = observation()
            selected = selected_membership_scan(pins, records, selected_frozen, selected_external)
            # Exact selected_inputs also binds these two already pinned A07 interface members.
            for name, pin in method["A07_domain_interface"][
                "selected_existing_bounds_expected_pins"
            ].items():
                work_check(_STARTED)
                metadata_bind(
                    selected_frozen, selected_external, PROGRAM / "A07_run003" / name, pin, _STARTED
                )
            phase("exact_selected_inputs_membership_scan_and_A07_bounds_bind", scan_before)
        finally:
            _PROFILER.disable()
        phase("selected_metadata_profile_complete", before)
        loaded_origins()
        save("profile.json", profile_evidence(_PROFILER))
        require(
            (OUTPUT / "profile.json").stat().st_size <= MAX_PROFILE_BYTES,
            "Bounded profile retention",
        )
        save(
            "selected_metadata_authorization.json",
            {
                "owner_manifest_SHA256": owners,
                "complete_owner_map_record_count": len(records),
                "selected_memberships": selected,
                "selected_membership_count": len(selected),
                "selected_actual_frozen_paths": len(selected_frozen),
                "selected_actual_external_paths": len(selected_external),
                "records_not_dropped_or_replaced_by_index": True,
                "warm_checked_adapter_SHA_cache": True,
                "no_global_prerequisite_validity_claim": True,
                **scope_flags(),
            },
        )
        before = observation()
        second = fresh_union()
        phase("second_full_uncached_resolve_and_SHA_union", before)
        require(
            not (OUTPUT / "manifest.json").exists()
            and not (OUTPUT / "completion_outcome.json").exists()
            and not (OUTPUT / "FAILED_UNSEALED.json").exists(),
            "Exclusive new diagnostic terminal",
        )
        summary = {
            "schema": "a13-selected-metadata-validation-profile-summary-v1",
            "completed": True,
            "passed": True,
            "diagnostic_integrity": True,
            "status": "selected_metadata_profile_retained_only",
            "fixed_metadata_calls_returned": True,
            "complete_V5_source_packet_or_prepare_run_profile": False,
            "remaining_native_or_mathematical_cost_measured": False,
            "profiling_overhead_included": True,
            "unprofiled_speedup_or_budget_fit_claim": False,
            "source_manifest_capture_SHA256": CAPTURE_SHA,
            "captured_original_admission_censor_observation": failure_summary[
                "original_admission_censor_observation"
            ],
            "original_exact_final_CPU_wall_not_inferred": True,
            "current_diagnostic_runtime": runtime,
            "runtime_is_current_diagnostic_only": True,
            "complete_original_protocol_maps_counts": [
                len(protocol["frozen_inputs"]),
                len(protocol["external_runtime_inputs"]),
            ],
            "complete_capture_maps_counts": [
                len(capture["files"]),
                len(capture["frozen_inputs"]),
                len(capture["external_runtime_inputs"]),
            ],
            "both_full_uncached_input_unions": [first, second],
            "phases": _PHASES,
            "adapter_counters": _PROFILE_COUNTS,
            "budget": observation(),
            "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
            "selected_work_CPU_wall": [WORK_CPU, WORK_WALL],
            **scope_flags(),
        }
        save("summary.json", summary)
        save("completion_outcome.json", dict(summary, failed=False, budget_censored=False))
        files, total = {}, 0
        for path in sorted(inventory(OUTPUT)):
            budget()
            total += path.stat().st_size
            require(len(files) < MAX_OWN_FILES and total <= MAX_OWN_BYTES, "New owned caps only")
            files[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
        save(
            "manifest.json",
            {
                "schema": "a13-selected-metadata-validation-profile-manifest-v1",
                "files": files,
                "frozen_inputs": _FROZEN,
                "external_runtime_inputs": _EXTERNAL,
                "manifest_self_hash_excluded": True,
                "completed": True,
                "passed": True,
                "diagnostic_integrity": True,
                "budget_censored": False,
                "terminal_budget_observation": observation(),
                "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
                "both_full_uncached_input_unions": [first, second],
                "actual_hash_work_bytes": _HASH_WORK,
                "map_reference_count": _REFERENCES,
                **scope_flags(),
            },
        )
        budget()
        print(
            json.dumps(
                {
                    "passed": True,
                    "diagnostic_integrity": True,
                    "manifest_SHA256": digest(OUTPUT / "manifest.json", fresh=True),
                    **scope_flags(),
                }
            )
        )
    except BaseException as error:
        if _PROFILER is not None:
            _PROFILER.disable()
            if OUTPUT.is_dir() and not (OUTPUT / "profile.json").exists():
                try:
                    save(
                        "profile.json",
                        dict(
                            profile_evidence(_PROFILER),
                            incomplete=True,
                            selected_metadata_calls_completed=False,
                            mathematical_approval=False,
                        ),
                    )
                except BaseException:
                    pass
        retain_failure(error)
        raise


if __name__ == "__main__":
    main()
