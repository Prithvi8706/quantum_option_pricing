"""Prospective F44 Stage K metadata integrity only; no scientific imports.

The audit manifest is an externally issued ROOT expectation, never an observed
digest promoted into a prerequisite. Scoped integrity permits no Stage C or G2
release, new pricing source, resource transfer, or financial adoption.
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
AUTHOR = RESEARCH / "verify_taylor_f44_stage_k_root_v1.py"
METHOD_DOC = RESEARCH / "A14_TAYLOR_F44_STAGE_K_ROOT_INTEGRITY_PREFLIGHT_V1.md"
PREFLIGHT = RESEARCH / "a14_taylor_f44_stage_k_root_integrity_preflight_v1.json"
READY = ROOT / ".context/A14_TAYLOR_F44_STAGE_K_INTEGRITY_ROOT_READY_run001.json"
OUTPUT = PROGRAM / "A14_taylor_f44_stage_K_root_verification_run001"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
SOURCE_NAME = "A14_taylor_f44_stage_K_run001"
AUDIT_NAME = "A14_taylor_f44_stage_K_audit_run001"
SOURCE = PROGRAM / SOURCE_NAME
AUDIT = PROGRAM / AUDIT_NAME
SOURCE_SHA = "b03c8a7cb62655301b9a231eb987f38e5ec496f612206ff6701143f6cefb8b88"
ROOT_DECLARED_AUDIT_SHA = "2c253beba55b1271dec594db8231c8bdbfcaffbf4d797dedb840eda72568f5be"
SOURCE_READY = ROOT / ".context/A14_TAYLOR_F44_STAGE_K_ROOT_READY_run001.json"
SOURCE_READY_SHA = "ce6e00b8cb2f53e05383d14e20e003e36207cd65096b232bb47df157782df3ba"
AUDIT_READY = ROOT / ".context/A14_TAYLOR_F44_STAGE_K_AUDIT_ROOT_READY_run001.json"
AUDIT_READY_SHA = "67bf1f1a944f8aafd94f5eafdd418210ff053bf84a3586fd5c2b85c4b67a304a"
SOURCE_COUNTS, AUDIT_COUNTS = [17, 774, 2842], [10, 796, 2842]
SOURCE_AUTHORS = {
    "taylor_f44_stage_k_source.py": (
        "fd1324ef0b9e0e0135a40a7af4706db8ec0a8b4d35808ba555f8cbf1856ce4c9"
    ),
    "experiment_taylor_f44_stage_k.py": (
        "b727533be3f26ee25f0019a45aceb6c6d3dbc32e0ff6461ceb2e55bf6716a989"
    ),
    "A14_TAYLOR_F44_STAGE_K_IMPLEMENTATION_PREFLIGHT.md": (
        "d4e005bb184da469e22a511b48df03434ba5a70b09277d5533b008b4bc8eb9f5"
    ),
    "a14_taylor_f44_stage_k_implementation_preflight.json": (
        "34537571425539de0222d438e99346b4598c6b7f2152fa954e8d499a0a1127ab"
    ),
}
AUDIT_AUTHORS = {
    "audit_taylor_f44_stage_k.py": (
        "6fdb3dbf74f5f82662904cab0303c014e99507343355ed019c71dc0bf6d5b651"
    ),
    "A14_TAYLOR_F44_STAGE_K_AUDIT_PREFLIGHT.md": (
        "de8685d3aca030ac57b675b75cfe175124fe3c016100624e2e975a232edb396e"
    ),
    "a14_taylor_f44_stage_k_audit_preflight.json": (
        "980656d56876fb5b85fffddc0612ed86afd592fa1c8906c9fcd683acf6c8e7a0"
    ),
}
COSINE_PACKETS = {
    "A14_cosine_feasibility_run001": (
        "bdb01b0c69d8fab3ee3d61f1c48ce5764f1ae09488f564d186f658f180e4156b",
        [24, 672, 2842],
    ),
    "A14_cosine_feasibility_audit_run003": (
        "52c88dc17c6a53b1df30bd93a431d3e263cb202462901589aaaa30bb87631f0f",
        [17, 752, 2842],
    ),
}
CPU, ADMISSION, WALL = 180, 150, 600
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
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


def packet(name, pin, counts):
    directory = canonical(PROGRAM / name)
    manifest = bind(directory / "manifest.json", pin)
    data = read(manifest)
    no_failure(directory)
    require(
        data.get("passed") is True
        and data.get("completed") is True
        and data.get("budget_censored") is False
        and data.get("manifest_self_hash_excluded") is True,
        "Actual completed uncensored scoped source/audit, not candidate eligibility",
    )
    require(
        [len(data[field]) for field in ("files", "frozen_inputs", "external_runtime_inputs")]
        == counts,
        "Complete original maps",
    )
    owned = {manifest}
    for field in ("files", "frozen_inputs", "external_runtime_inputs"):
        require(type(data[field]) is dict, "Typed complete original input maps")
        for key, expected in data[field].items():
            budget()
            require(type(key) is str, "Literal original key")
            if field == "external_runtime_inputs":
                require(Path(key).is_absolute(), "Scoped external original key")
                path = Path(key)
            else:
                require(
                    not Path(key).is_absolute() and "\\" not in key and ".." not in Path(key).parts,
                    "Exact slash-relative old key",
                )
                root_owned = key.startswith(directory.relative_to(ROOT).as_posix() + "/")
                path = ROOT / key if field == "frozen_inputs" or root_owned else directory / key
            actual = bind(path, expected)
            if field == "files":
                require(
                    actual.is_relative_to(directory)
                    and actual not in owned
                    and actual.relative_to(ROOT if root_owned else directory).as_posix() == key,
                    "Exact no-alias original own membership",
                )
                owned.add(actual)
            elif field == "frozen_inputs":
                require(
                    actual.is_relative_to(ROOT) and actual.relative_to(ROOT).as_posix() == key,
                    "Exact original ROOT membership",
                )
            else:
                require(
                    not actual.is_relative_to(ROOT) and str(actual) == key,
                    "Exact external original membership",
                )
    require(inventory(directory) == owned, "Exact complete prior inventory")
    _OWN_INVENTORIES[directory] = owned
    return data


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


def loaded_origins():
    forbidden = {"mpmath", "numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
    require(
        not any(name.split(".", 1)[0] in forbidden for name in sys.modules),
        "No numerical or optional scientific imports",
    )
    require(
        not any(
            name.startswith("research.")
            and name not in {__name__, "research.limitation_program_20261001"}
            for name in sys.modules
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
                not lexical.is_relative_to(_EXCLUDED_SCOPE[0])
                and not lexical.resolve(strict=False).is_relative_to(_EXCLUDED_SCOPE[1]),
                "No excluded runtime origin or cache",
            )
            if lexical.is_file():
                actual = canonical(lexical)
                key = key_for(actual)
                mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
                if key not in mapping:
                    add(actual, digest(actual))
                else:
                    require(digest(actual) == mapping[key], "Loaded bytes equal frozen expectation")


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


def flags():
    return {
        "metadata_integrity_only": True,
        "new_scientific_evaluation": False,
        "new_test_credit": 0,
        "new_credited_gate_replays": 0,
        "new_price_samples": 0,
        "Stage_C_release_authorized": False,
        "full_G2": False,
        "adoption": False,
        "cost_transfer": False,
        "quantum_advantage": False,
        "Stage_K_diagnostics_not_cosine_or_financial_certificate": True,
        "previous_A14_rejected_rows_unchanged": True,
        "original_scientific_receipts_unchanged": True,
    }


def scoped_success(record, schema):
    require(
        record["schema"] == schema
        and record["passed"] is True
        and record["completed"] is True
        and record["budget_censored"] is False,
        "Completed uncensored scoped success",
    )
    for key in ("new_test_credit", "new_credited_gate_replays", "new_price_samples"):
        require(type(record[key]) is int and record[key] == 0, "Zero scientific fixture credit")
    for key in (
        "Stage_C_release_authorized",
        "full_G2",
        "adoption",
        "cost_transfer",
        "quantum_advantage",
    ):
        require(record[key] is False, "No promotion beyond arithmetic component")
    require(
        record["Stage_K_diagnostics_not_cosine_or_financial_certificate"] is True,
        "Original Stage K scope stays explicit",
    )
    require(record["previous_A14_rejected_rows_unchanged"] is True, "Earlier rejections retained")
    require(
        record["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL], "Original bounded clocks"
    )
    observed = record.get("budget", record.get("terminal_budget_observation"))
    require(
        isinstance(observed, dict)
        and 0 <= observed["process_CPU_seconds"] < CPU
        and 0 <= observed["wall_seconds"] < WALL,
        "Recorded process timing stays bounded",
    )


def admission(ready_sha):
    ready = read(bind(READY, ready_sha))
    require(
        ready["schema"] == "root-a14-taylor-f44-stage-k-integrity-READY-v1"
        and ready["ready"] is True
        and ready["root_and_independent_static_reviews_passed"] is True,
        "ROOT-issued static release required",
    )
    require(
        ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL],
        "Fixed root verifier route and limits",
    )
    require(
        ready["source_manifest_SHA256"] == SOURCE_SHA
        and ready["audit_manifest_SHA256"] == ROOT_DECLARED_AUDIT_SHA
        and ready["source_complete_counts"] == SOURCE_COUNTS
        and ready["audit_complete_counts"] == AUDIT_COUNTS,
        "Externally ROOT-frozen actual producer and audit prerequisites",
    )
    require(
        ready["Stage_C_release_authorized"] is False
        and ready["financial_adoption"] is False
        and ready["fixture_credit"] == 0,
        "ROOT release approves only integrity validation",
    )
    own = ready["author_method_SHA256"]
    require(
        set(own) == {AUTHOR.name, METHOD_DOC.name, PREFLIGHT.name}, "Exactly three verifier files"
    )
    for name, expected in own.items():
        bind(RESEARCH / name, expected)
    policy = read(PREFLIGHT)
    require(
        policy["schema"] == "a14-taylor-f44-stage-k-root-integrity-preflight-v1"
        and policy["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and policy["owned_caps_files_bytes"] == [MAX_OWN_FILES, MAX_OWN_BYTES]
        and policy["runtime_caps_files_bytes"] == [MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES]
        and policy["bookkeeping_reference_unique_bytes_hash_work_caps"]
        == [MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK]
        and policy["source_manifest_SHA256"] == SOURCE_SHA
        and policy["ROOT_declared_actual_audit_manifest_SHA256"] == ROOT_DECLARED_AUDIT_SHA
        and policy["new_scientific_evaluation"] is False,
        "Exact prospective integrity method",
    )
    producer_ready = read(bind(SOURCE_READY, SOURCE_READY_SHA))
    audit_ready = read(bind(AUDIT_READY, AUDIT_READY_SHA))
    require(
        producer_ready["schema"] == "root-a14-taylor-f44-stage-k-READY-v1"
        and producer_ready["ready"] is True
        and producer_ready["author_method_SHA256"] == SOURCE_AUTHORS
        and producer_ready["stage_C_release_authorized"] is False,
        "Exact original producer READY",
    )
    require(
        audit_ready["schema"] == "root-a14-taylor-f44-stage-k-audit-READY-v1"
        and audit_ready["ready"] is True
        and audit_ready["author_method_SHA256"] == AUDIT_AUTHORS
        and audit_ready["producer_author_method_SHA256"] == SOURCE_AUTHORS
        and audit_ready["producer_ROOT_READY_SHA256"] == SOURCE_READY_SHA
        and audit_ready["source_manifest_SHA256"] == SOURCE_SHA
        and audit_ready["source_complete_counts"] == SOURCE_COUNTS
        and audit_ready["Stage_C_release_authorized"] is False,
        "Exact original independent audit READY",
    )
    prior_pins = {name: pin for name, (pin, _) in COSINE_PACKETS.items()}
    prior_counts = {name: counts for name, (_, counts) in COSINE_PACKETS.items()}
    require(
        producer_ready["required_existing_packet_manifest_SHA256"] == prior_pins
        and policy["original_cosine_packet_manifest_SHA256"] == prior_pins
        and policy["original_cosine_packet_complete_counts"] == prior_counts,
        "Original cosine inventory obligations remain binding",
    )
    for name, (pin, counts) in COSINE_PACKETS.items():
        packet(name, pin, counts)
    for authors in (SOURCE_AUTHORS, AUDIT_AUTHORS):
        for name, expected in authors.items():
            bind(RESEARCH / name, expected)
    code_caches(
        [RESEARCH / "experiment_taylor_f44_stage_k.py", RESEARCH / "taylor_f44_stage_k_source.py"],
        producer_ready["existing_new_code_cache_SHA256"],
        producer_ready["absent_new_code_cache_paths"],
    )
    code_caches(
        [RESEARCH / "audit_taylor_f44_stage_k.py"],
        audit_ready["existing_new_code_cache_SHA256"],
        audit_ready["absent_new_code_cache_paths"],
    )
    code_caches(
        [AUTHOR], ready["existing_new_code_cache_SHA256"], ready["absent_new_code_cache_paths"]
    )
    source_manifest = packet(SOURCE_NAME, ready["source_manifest_SHA256"], SOURCE_COUNTS)
    audit_manifest = packet(AUDIT_NAME, ready["audit_manifest_SHA256"], AUDIT_COUNTS)
    scoped_success(source_manifest, "a14-taylor-f44-stage-k-manifest-v1")
    scoped_success(audit_manifest, "a14-taylor-f44-stage-k-audit-manifest-v1")
    require(
        audit_manifest["source_manifest_SHA256"] == SOURCE_SHA
        and audit_manifest["independent_scientific_audit_complete"] is True
        and audit_manifest["ROOT_integrity_still_required"] is True
        and source_manifest["independent_scientific_audit_still_required"] is True,
        "Independent audit is tied to the same actual producer",
    )
    executables = {canonical(LAUNCHER), canonical(Path(sys._base_executable))}
    require(
        len(executables) == 2 and canonical(sys._base_executable) == _BASE_SCOPE / "python.exe",
        "Distinct actual pinned launcher/base interpreter",
    )
    observed_executables = set()
    for spelling, expected in ready["interpreter_expected_SHA256"].items():
        path = canonical(spelling)
        require(
            path in executables and path not in observed_executables,
            "Only distinct actual launcher/base interpreter pins",
        )
        observed_executables.add(path)
        bind(path, expected)
    require(observed_executables == executables, "Both executable expected pins present")
    return source_manifest, audit_manifest


def reconcile_metadata():
    source_summary = read(SOURCE / "summary.json")
    source_outcome = read(SOURCE / "completion_outcome.json")
    audit_summary = read(AUDIT / "summary.json")
    audit_outcome = read(AUDIT / "completion_outcome.json")
    for value in (source_summary, source_outcome):
        scoped_success(value, "a14-taylor-f44-stage-k-summary-v1")
        require(
            value["fixed_diagnostic_counts"] == [16, 40, 32, 88]
            and value["actual_full_leaf_replay_calls"] == 168
            and value["actual_Boolean_prefix_replay_calls"] == 64
            and value["native_rows_total"] == 25030
            and value["actual_array_matched_universal_structure"] is True
            and value["absolute7T_phase_proof_bound"] is True,
            "Exact original completed producer scope",
        )
    for value in (audit_summary, audit_outcome):
        scoped_success(value, "a14-taylor-f44-stage-k-audit-summary-v1")
        require(
            value["source_manifest_SHA256"] == SOURCE_SHA
            and value["fixed_diagnostic_counts"] == [16, 40, 32, 88]
            and value["independent_scientific_audit_complete"] is True
            and value["actual_binary_independent_replay"] is True
            and value["actual_resource_recount"] is True
            and value["actual_array_matched_universal_structure"] is True
            and value["absolute7T_phase_proof_bound"] is True
            and value["ROOT_integrity_still_required"] is True,
            "Exact completed independent audit scope",
        )
    require(
        source_outcome["failed"] is False and audit_outcome["failed"] is False,
        "Both authoritative outcomes are successful",
    )
    source_cases = read(SOURCE / "fixed_diagnostics.json")
    audit_cases = read(AUDIT / "independent_fixed_diagnostics.json")
    require(
        source_cases["fixed_total"] == audit_cases["fixed_total"] == 88
        and source_cases["cases"] == audit_cases["cases"]
        and {key: len(rows) for key, rows in source_cases["cases"].items()}
        == {"multiplier": 16, "rounder": 40, "Boolean_prefix": 32},
        "Every saved diagnostic record agrees; no binary replay here",
    )
    source_cost = read(SOURCE / "primitive_resources.json")
    audit_cost = read(AUDIT / "independent_primitive_resources.json")
    require(
        source_cost["no_prior_resource_transfer"] is True
        and source_cost["full_cosine_or_financial_cost_claim"] is False
        and all(source_cost[name] == audit_cost[name] for name in ("multiplier", "rounder")),
        "Exact saved primitive resource agreement, no recount or full-source transfer",
    )
    arrays = read(SOURCE / "native_gate_arrays.json")
    require(
        source_summary["native_gate_arrays"] == arrays
        and set(arrays) == {"multiplier", "rounder"}
        and arrays["multiplier"]["rows"] == 24352
        and arrays["rounder"]["rows"] == 678,
        "Exact saved array descriptors; binary bytes are hashed only",
    )
    return {
        "fixed_diagnostic_counts": [16, 40, 32, 88],
        "native_rows_total": 25030,
        "saved_reports_equal": True,
        "saved_primitive_resources_equal": True,
        "native_gate_binary_interpreted": False,
        "primitive_resources": {name: source_cost[name] for name in ("multiplier", "rounder")},
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
                b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,'
                b'"hard_budget_state_uncertified":true,"new_test_credit":0,'
                b'"Stage_C_release_authorized":false,"full_G2":false,"adoption":false}\n'
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
    require(canonical(__file__) == AUTHOR and not OUTPUT.exists(), "Single fresh integrity route")
    try:
        admission(args.ready_sha256)
        runtime = own_runtime()
        loaded_origins()
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
                "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
                **flags(),
            },
        )
        report = reconcile_metadata()
        save("metadata_reconciliation.json", report)
        loaded_origins()
        check_code_caches()
        second = fresh_union()
        summary = {
            "schema": "a14-taylor-f44-stage-k-root-integrity-summary-v1",
            "completed": True,
            "passed": True,
            "budget_censored": False,
            "source_manifest_SHA256": SOURCE_SHA,
            "audit_manifest_SHA256": ROOT_DECLARED_AUDIT_SHA,
            "source_complete_counts": SOURCE_COUNTS,
            "audit_complete_counts": AUDIT_COUNTS,
            "original_scientific_receipts_integrity_verified": True,
            "saved_diagnostic_and_resource_metadata_reconciled": True,
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
                len(owned) < MAX_OWN_FILES - 1 and total <= MAX_OWN_BYTES, "Inclusive own reserve"
            )
            owned[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
        complete_manifest(
            {
                "schema": "a14-taylor-f44-stage-k-root-integrity-manifest-v1",
                "files": owned,
                "frozen_inputs": _FROZEN,
                "external_runtime_inputs": _EXTERNAL,
                "manifest_self_hash_excluded": True,
                "completed": True,
                "passed": True,
                "budget_censored": False,
                "source_manifest_SHA256": SOURCE_SHA,
                "audit_manifest_SHA256": ROOT_DECLARED_AUDIT_SHA,
                "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
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
