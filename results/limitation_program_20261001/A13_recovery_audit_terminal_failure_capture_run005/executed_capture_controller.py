"""Preserve the unsealed A13 audit005 failure as metadata, never scientific approval.

Fixed180CPU/150admission/600creation-wall. All original prepared expected maps
remain strict. Newly observed failed-owned bytes are separately identified,
never substituted for an existing expectation. No gzip decoding or proof calls.
"""

import argparse
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
AUTHOR = RESEARCH / "capture_a13_recovery_audit_failure_v5.py"
PREFLIGHT = RESEARCH / "a13_recovery_audit_failure_capture_preflight_v5.json"
OUTPUT = PROGRAM / "A13_recovery_audit_terminal_failure_capture_run005"
FAILED = PROGRAM / "A13_recovery_audit_run005"
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


def observe_failure_material():
    require(not (FAILED / "manifest.json").exists(), "Original failure has no seal")
    members = inventory(FAILED)
    rows = sorted(
        member.relative_to(FAILED).as_posix()
        for member in members
        if member.parent == FAILED / "rows"
    )
    require(
        rows == sorted(f"rows/d{degree}_s{count}.json.gz" for degree, count in GRID[:18]),
        "Exactly the eighteen partial unapproved proof files retained",
    )
    for missing in (
        "summary.json",
        "fixed_inventory_authorization.json",
        "manifest.json",
        "completion_outcome.json",
    ):
        require(not (FAILED / missing).exists(), "No original terminal approval or index")
    for path in sorted(members):
        budget()
        pin = digest(path)
        key = input_key(path)
        add(path, pin)
        _OWNED_OBSERVATIONS[key] = {
            "SHA256": pin,
            "bytes": path.stat().st_size,
            "observation_origin": "new_capture_of_unsealed_failed_owned_bytes",
            "preexisting_expected_SHA256": _ORIGINAL_FROZEN.get(key),
            "scientific_claims_trusted": False,
        }
    _OWN_INVENTORIES[FAILED] = members
    marker = read(FAILED / "FAILED_UNSEALED.json")
    require(
        marker.get("failed") is True
        and marker.get("completed") is False
        and marker.get("passed") is False
        and marker.get("budget_censored") is None
        and marker.get("hard_budget_state_uncertified") is True
        and marker.get("partial_success_invalid") is True
        and marker.get("new_test_credit") == 0,
        "Authoritative unsealed marker, terminal hard-budget state remains uncertified",
    )
    failure = read(FAILED / "failure.json")
    require(
        failure.get("failed") is True
        and failure.get("error_type") == "BudgetCensoredError"
        and failure.get("error") == "Fixed independent A13 CPU/wall censor"
        and failure.get("phase") == "run"
        and failure.get("new_test_credit") == 0
        and "audit_segment_certificate" in failure["traceback"]
        and "check(started, admission=True)" in failure["traceback"]
        and 270 <= failure["budget"]["process_CPU_seconds"] < 300
        and 0 <= failure["budget"]["wall_seconds"] < 900,
        "Saved admission censor observation is not exact final CPU or scientific rejection",
    )
    return marker, failure


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


def original_utf8_log(path):
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
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--author-sha256", required=True)
    parser.add_argument("--preflight-sha256", required=True)
    args = parser.parse_args()
    require(canonical(__file__) == AUTHOR and not OUTPUT.exists(), "Fresh fixed capture, no retry")
    try:
        add(AUTHOR, args.author_sha256)
        add(PREFLIGHT, args.preflight_sha256)
        policy = read(PREFLIGHT)
        require(
            policy["schema"] == "a13-audit005-unsealed-failure-capture-preflight-v1"
            and policy["author_SHA256"] == args.author_sha256
            and policy["limits_CPU_admission_wall"] == [180, 150, 600]
            and policy["new_owned_caps_files_bytes"] == [64, 134217728]
            and policy["failed_receipt"] == FAILED.relative_to(ROOT).as_posix()
            and policy["fresh_capture_receipt"] == OUTPUT.relative_to(ROOT).as_posix()
            and policy["scientific_execution"] is False
            and policy["new_test_credit"] == 0
            and policy["original_V5_author_SHA256"] == V5_AUTHORS
            and policy["source_root_review_manifest_SHA256"] == ROOT_REVIEW_SHA
            and policy["actual_finite_Bernstein_QA_manifest_SHA256"] == QA_SHA
            and policy["root_review_owned_frozen_external_counts"] == [1, 49, 0]
            and policy["finite_QA_owned_frozen_external_counts"] == [2, 6, 0],
            "Externally reviewed fixed metadata-only capture policy",
        )
        add(ORIGIN, ORIGIN_SHA)
        # Only metadata is decoded; proof gzip and old scientific artifacts are opaque bytes.
        protocol_path = FAILED / "protocol.json"
        add(protocol_path, digest(protocol_path))
        protocol = read(protocol_path)
        require(
            protocol["schema"] == "a13-exp-frontier-recovery-independent-audit-protocol-v1"
            and protocol["operational_recovery_audit_version"] == 5
            and protocol["output"] == FAILED.relative_to(ROOT).as_posix()
            and protocol["CPU_admission_wall_seconds"] == [300, 270, 900]
            and protocol["independent_digits"] == 130
            and protocol["primary_digits"] == 90
            and protocol["threads"] == 1
            and [len(protocol["frozen_inputs"]), len(protocol["external_runtime_inputs"])]
            == policy["original_protocol_frozen_external_counts"]
            == [1099, 2842],
            "Exact original prepared version5 scientific contract, never completion",
        )
        original_maps(protocol, input_key(protocol_path))
        for name, pin in V5_AUTHORS.items():
            budget()
            bind_original(RESEARCH / name, pin, "root_fixed_v5_pins", "author", name)
            require(
                protocol["frozen_inputs"].get(
                    (FAILED / "executed_code" / name).relative_to(ROOT).as_posix()
                )
                == pin,
                "Every original V5/kernel executed-copy expected hash retained",
            )
        require(
            protocol["author_sha256"]
            == {
                "audit_exp_frontier_recovery_v5.py": V5_AUTHORS["audit_exp_frontier_recovery_v5.py"]
            },
            "Original V5 author separate from new capture controller",
        )
        review = original_packet(ROOT_REVIEW, ROOT_REVIEW_SHA, [1, 49, 0])
        require(review["ready"] is True, "Original V5 static release remains static only")
        qa = original_packet(QA, QA_SHA, [2, 6, 0])
        require(qa["completed"] is True, "Actual finite arithmetic QA remains separate from all20")
        marker, failure = observe_failure_material()
        require(
            [
                len(_OWNED_OBSERVATIONS),
                sum(row["bytes"] for row in _OWNED_OBSERVATIONS.values()),
            ]
            == policy["terminal_old_owned_metadata_observation_files_bytes"]
            == [50, 25959363],
            "Exact terminal observed old inventory, no old-size cap or deletion",
        )
        logs = {}
        for name in (
            "a13_recovery_audit_actual_run005.log",
            "a13_recovery_audit_prepare_run005.log",
        ):
            path = ROOT / ".context" / name
            pin = digest(path)
            add(path, pin)
            logs[input_key(path)] = {
                "SHA256": pin,
                "bytes": path.stat().st_size,
                "origin": "new_capture_observation_of_original_log_bytes",
            }
        # Decode only the root-declared UTF8 run log; its unchanged bytes stay frozen.
        actual_log = ROOT / ".context/a13_recovery_audit_actual_run005.log"
        text = original_utf8_log(actual_log)
        require(
            "BudgetCensoredError" in text and "audit_segment_certificate" in text,
            "Actual UTF8 failure log corresponds to saved admission censor",
        )
        budget()
        runtime = own_runtime()
        first = fresh_union()
        budget(admission=True)
        OUTPUT.mkdir()
        copy_input(AUTHOR, "executed_capture_controller.py")
        copy_input(PREFLIGHT, "executed_capture_preflight.json")
        save("untrusted_failed_material_index.json", _OWNED_OBSERVATIONS)
        save("original_expected_map_memberships.json", _MEMBERSHIPS)
        save(
            "capture_input_scope.json",
            {
                "original_protocol_frozen_count": len(protocol["frozen_inputs"]),
                "original_protocol_external_count": len(protocol["external_runtime_inputs"]),
                "original_preexisting_expected_frozen_inputs": _ORIGINAL_FROZEN,
                "original_preexisting_expected_external_runtime_inputs": _ORIGINAL_EXTERNAL,
                "newly_observed_failed_owned_inputs": _OWNED_OBSERVATIONS,
                "newly_observed_original_logs": logs,
                "current_capture_runtime": runtime,
                "capture_runtime_not_original_failure_runtime": True,
                "no_preexisting_expected_hash_replaced": True,
            },
        )
        loaded_origins()
        second = fresh_union()
        summary = {
            "schema": "a13-audit005-unsealed-failure-metadata-capture-summary-v1",
            "created_UTC": datetime.now(timezone.utc).isoformat(),
            "completed": True,
            "passed": True,
            "diagnostic_integrity": True,
            "original_attempt_failed": True,
            "original_attempt_sealed": False,
            "original_failure_marker_authoritative": True,
            "original_hard_budget_state_uncertified": True,
            "original_admission_censor_observation": failure["budget"],
            "original_exact_final_CPU_wall_not_recorded": True,
            "original_marker": marker,
            "original_failure_metadata": failure,
            "original_receipt": FAILED.relative_to(ROOT).as_posix(),
            "original_owned_files": len(_OWNED_OBSERVATIONS),
            "original_owned_bytes": sum(row["bytes"] for row in _OWNED_OBSERVATIONS.values()),
            "partial_gzip_rows": [f"d{degree}_s{count}" for degree, count in GRID[:18]],
            "partial_rows_unapproved": True,
            "source_summary_index_outcome_manifest_absent": True,
            "original_prepared_expected_maps_preserved_in_full": True,
            "new_owned_observations_distinct_from_prior_expected_hashes": True,
            "original_expected_hashes_waived": False,
            "both_full_uncached_input_unions": [first, second],
            "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
            "new_owned_caps_files_bytes": [MAX_OWN_FILES, MAX_OWN_BYTES],
            "current_capture_runtime": runtime,
            "runtime_is_current_capture_only": True,
            "capture_process_CPU_seconds": time.process_time(),
            "capture_wall_seconds": time.monotonic() - _STARTED,
            "scientific_execution": False,
            "gzip_decompression_or_proof_calls": False,
            "original_scientific_inputs_or_methods_modified": False,
            "mathematical_result_or_row_approval": False,
            "new_test_credit": 0,
            "new_gate_replays": 0,
            "new_price_samples": 0,
            "full_G2": False,
            "adoption": False,
            "cost_transfer": False,
        }
        save("summary.json", summary)
        save("completion_outcome.json", summary)
        owned = inventory(OUTPUT)
        require(
            len(owned) <= MAX_OWN_FILES
            and sum(path.stat().st_size for path in owned) <= MAX_OWN_BYTES,
            "New capture owned caps only, no old file cap or deletion",
        )
        files = {}
        for path in sorted(owned):
            budget()
            files[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
        save(
            "manifest.json",
            {
                "schema": "a13-audit005-unsealed-failure-metadata-capture-manifest-v1",
                "files": files,
                "frozen_inputs": _FROZEN,
                "external_runtime_inputs": _EXTERNAL,
                "manifest_self_hash_excluded": True,
                "completed": True,
                "passed": True,
                "diagnostic_integrity": True,
                "original_attempt_failed": True,
                "original_attempt_sealed": False,
                "original_hard_budget_state_uncertified": True,
                "original_expected_hashes_waived": False,
                "newly_observed_failed_owned_SHA256": {
                    key: row["SHA256"] for key, row in _OWNED_OBSERVATIONS.items()
                },
                "new_test_credit": 0,
                "scientific_execution": False,
                "budget_censored": False,
                "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
                "terminal_budget_observation": {
                    "process_CPU_seconds": time.process_time(),
                    "wall_seconds": time.monotonic() - _STARTED,
                },
            },
        )
        budget()
        manifest_sha = digest(OUTPUT / "manifest.json", fresh=True)
        budget()
        print(
            json.dumps(
                {
                    "passed": True,
                    "diagnostic_integrity": True,
                    "original_attempt_failed": True,
                    "original_attempt_sealed": False,
                    "manifest_SHA256": manifest_sha,
                    "new_test_credit": 0,
                }
            )
        )
    except BaseException as error:
        retain_failure(error)
        raise


if __name__ == "__main__":
    main()
