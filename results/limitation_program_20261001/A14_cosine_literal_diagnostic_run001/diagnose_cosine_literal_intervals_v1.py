"""AUTHOR-ONLY bounded diagnostic of saved A14 angle/gain interval relations.

Exactly the old frozen auditor's small interval functions are AST-extracted
under explicit root-controlled diagnostic authorization. No old module, main,
source walker, native replay, fitter, row certificate or adoption is executed.
All48 angles plus finite reciprocal gain are retained regardless of diagnostic
nesting failures. Fixed180 process CPU/150 work/600 wall, purePython130 digits.
"""

import argparse
import ast
import ctypes
from ctypes import wintypes
from fractions import Fraction
from importlib import metadata
import hashlib
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
AUTHOR = RESEARCH / "diagnose_cosine_literal_intervals_v1.py"
METHOD = RESEARCH / "a14_cosine_literal_diagnostic_preflight.json"
METHOD_DOC = RESEARCH / "A14_COSINE_LITERAL_DIAGNOSTIC_PREFLIGHT.md"
OUTPUT = PROGRAM / "A14_cosine_literal_diagnostic_run001"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
SOURCE = PROGRAM / "A14_cosine_feasibility_run001"
FAILED = PROGRAM / "A14_cosine_feasibility_audit_run001"
SOURCE_SHA = "bdb01b0c69d8fab3ee3d61f1c48ce5764f1ae09488f564d186f658f180e4156b"
FAILED_SHA = "3b423ce15bd752745747807bf2970a2d7888a057d6c86ced1f2ed0efd98ece6e"
OLD_AUDITOR = RESEARCH / "audit_cosine_feasibility.py"
OLD_AUDITOR_SHA = "020a9428c4a13088201f6bef5abafa6b3daee73a8ef20166efffd83147df2e35"
ORIGIN = RESEARCH / "verify_exp_frontier_allocation_root_v2.py"
ORIGIN_SHA = "b0aac76928ad41a48cb1884d14f76168d8ef783595f918177857e5b13a91861f"
CPU, ADMISSION, WALL = 180, 150, 600
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
HELPERS = (
    "encode",
    "rational",
    "native_word",
    "interval_endpoint",
    "endpoints",
    "outward",
    "actual_literal_error",
    "cordic_reference_literals",
)
FAILURE_NAMES = (
    "FAILED_UNSEALED.json",
    "failed_unsealed.json",
    "failure.json",
    "run_failure.json",
    "prepare_failure.json",
)
_FROZEN, _EXTERNAL, _OBSERVED, _PACKETS = {}, {}, {}, {}
_HASH_WORK = _REFERENCES = 0
_STARTED = None
_OWN_INVENTORIES, _ABSENT_RUNTIME = {}, set()
_PATH_CACHE, _HASH_CACHE = {}, {}
_BASE_SCOPE, _EXCLUDED_SCOPE = None, None
_SCIENTIFIC_ALLOWED = False
_RUNTIME_INVENTORIES = {}
_STANDARD_RUNTIME_MEMBERS = set()


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
        "include-system-site-packages = false" in admitted_bytes(cfg).decode("utf-8").lower(),
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
                require(len(candidates) <= MAX_RUNTIME_FILES, "Bounded complete runtime membership")
    for directory in (
        base,
        canonical(sys.prefix),
        canonical(Path(sys.prefix) / "Lib/site-packages"),
    ):
        for path in directory.iterdir():
            budget()
            if path.is_file():
                candidates.add(canonical(path))
                require(len(candidates) <= MAX_RUNTIME_FILES, "Bounded adjacent runtime membership")
    return candidates


def loaded_origins():
    forbidden = {"numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
    require(
        not any(name.split(".", 1)[0] in forbidden for name in sys.modules),
        "No unrelated scientific or optional backend import",
    )
    require(
        _SCIENTIFIC_ALLOWED or not any(name.split(".", 1)[0] == "mpmath" for name in sys.modules),
        "No mpmath import before immutable runtime admission",
    )
    require(
        not any(
            name.startswith("research.")
            and name not in {__name__, "research.limitation_program_20261001"}
            for name in sys.modules
        ),
        "No old research module import",
    )
    for name, module in list(sys.modules.items()):
        budget()
        for attr in ("__file__", "__cached__"):
            origin = getattr(module, attr, None)
            if not origin:
                continue
            lexical = Path(os.path.abspath(str(origin)))
            require(
                not any(lexical.is_relative_to(scope) for scope in _EXCLUDED_SCOPE)
                and not any(
                    lexical.resolve(strict=False).is_relative_to(scope) for scope in _EXCLUDED_SCOPE
                ),
                "No excluded loaded origin or cache, even when vanished",
            )
            if not lexical.is_file():
                continue
            actual = canonical(lexical)
            mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
            key = (
                actual.relative_to(ROOT).as_posix() if actual.is_relative_to(ROOT) else str(actual)
            )
            if key not in mapping:
                require(
                    not name.startswith("mpmath")
                    and (actual.is_relative_to(_BASE_SCOPE) or actual == AUTHOR),
                    "Loaded package/cache must already belong to captured runtime",
                )
                add(actual, digest(actual))
            require(digest(actual) == mapping[key], "Actual loaded source/cache SHA binding")


def packet(directory, expected, *, failed):
    directory = canonical(directory)
    require(directory in {SOURCE, FAILED}, "Only the fixed two actual packets")
    require(not (directory / "FAILED_UNSEALED.json").exists(), "No unsealed packet admission")
    mf_path = add(directory / "manifest.json", expected)
    mf = read(mf_path)
    require(
        mf.get("manifest_self_hash_excluded") is True
        and mf.get("original_expected_hashes_waived") is False
        and mf.get("budget_censored") is False
        and mf.get("completed") is (not failed)
        and mf.get("passed") is (not failed),
        "Exact sealed original terminal scope",
    )
    maps = [mf.get(field) for field in ("files", "frozen_inputs", "external_runtime_inputs")]
    require(all(type(mapping) is dict for mapping in maps), "All three original maps")
    counts = [len(mapping) for mapping in maps]
    require(
        counts == ([13, 697, 2842] if failed else [24, 672, 2842]),
        "Exact observed packet map counts",
    )
    owned, frozen, external = maps
    members = set()
    for key, pin in owned.items():
        budget()
        require(
            type(key) is str
            and not Path(key).is_absolute()
            and "\\" not in key
            and ".." not in Path(key).parts,
            "Canonical relative owned key",
        )
        rooted = key.startswith("results/")
        actual = add(ROOT / key if rooted else directory / key, pin)
        require(
            actual.is_relative_to(directory)
            and actual != mf_path
            and actual not in members
            and actual.relative_to(ROOT if rooted else directory).as_posix() == key,
            "Unique exact original owned membership",
        )
        members.add(actual)
    for key, pin in frozen.items():
        budget()
        require(
            type(key) is str
            and not Path(key).is_absolute()
            and "\\" not in key
            and ".." not in Path(key).parts,
            "Canonical ROOT frozen key",
        )
        actual = add(ROOT / key, pin)
        require(
            actual.is_relative_to(ROOT) and actual.relative_to(ROOT).as_posix() == key,
            "Exact ROOT original route",
        )
    for key, pin in external.items():
        budget()
        require(type(key) is str and Path(key).is_absolute(), "Absolute external runtime key")
        actual = add(key, pin)
        require(
            not actual.is_relative_to(ROOT) and str(actual) == key, "Exact external original route"
        )
    expected_members = members | {mf_path}
    require(inventory(directory) == expected_members, "Every actual original owned byte retained")
    _OWN_INVENTORIES[directory] = expected_members
    outcome = read(directory / "completion_outcome.json")
    require(
        outcome.get("completed") is (not failed)
        and outcome.get("passed") is (not failed)
        and outcome.get("budget_censored") is False
        and outcome.get("new_test_credit") == 0,
        "Authoritative original terminal outcome, zero fixture credit",
    )
    for field in ("adoption", "cost_transfer", "full_G2"):
        require(outcome.get(field) is False, "No original adoption or fullG2 transfer")
    if failed:
        failure = read(directory / "failure.json")
        require(
            outcome.get("failed") is True
            and outcome.get("independent_audit_passed") is False
            and failure.get("error_type") == "ValueError"
            and failure.get("error")
            == "Fresh130 true-angle inclusion and actual absolute error authorization"
            and failure.get("budget_censored") is False
            and failure.get("independent_audit_passed") is False,
            "Exact retained uncensored independent failure; no assumed failing index",
        )
        require(
            OLD_AUDITOR.relative_to(ROOT).as_posix() in frozen
            and frozen[OLD_AUDITOR.relative_to(ROOT).as_posix()] == OLD_AUDITOR_SHA,
            "Extracted code is an original failed-packet frozen source",
        )
    else:
        no_failure(directory)
        summary = read(directory / "summary.json")
        require(
            summary.get("passed") is True
            and summary.get("completed") is True
            and summary.get("scientific_screen_complete") is True
            and summary.get("component_screen_eligible_rows") == [],
            "Original completed provisional screen with no eligible candidate",
        )
    _PACKETS[directory.name] = dict(
        manifest_sha256=expected,
        map_counts=counts,
        failed_original=failed,
        diagnostic_approval_only=False,
    )


def fresh_union():
    runtime_scopes()
    for alias, (previous, _) in tuple(_PATH_CACHE.items()):
        budget()
        require(canonical(alias, fresh=True) == previous, "Every original lexical alias unchanged")
    union = {}
    for mapping in (_FROZEN, _EXTERNAL):
        for key, pin in mapping.items():
            budget()
            path = Path(key) if Path(key).is_absolute() else ROOT / key
            require(path not in union or union[path] == pin, "EqualSHA merged expectations")
            union[path] = pin
    for path, pin in tuple(_OBSERVED.items()):
        budget()
        require(
            path not in union or union[path] == pin, "Observed actual bytes equal all expectations"
        )
        union[path] = pin
    total = 0
    for path, pin in union.items():
        budget()
        actual = canonical(path, fresh=True)
        total += actual.stat().st_size
        require(
            len(union) <= MAX_REFERENCES and total <= MAX_UNIQUE_BYTES,
            "Bounded full unique input and observed-byte union",
        )
        require(
            digest(actual, fresh=True, already_resolved=True) == pin,
            "Fresh full-byte union SHA: " + str(path),
        )
    for directory, members in _OWN_INVENTORIES.items():
        require(
            inventory(directory) == members, "Original packet exact terminal inventory unchanged"
        )
    for directory, members in _RUNTIME_INVENTORIES.items():
        require(
            inventory(directory) == members, "Complete mpmath/runtime metadata inventory unchanged"
        )
    require(
        standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS,
        "Complete captured reachable standard runtime and adjacent membership unchanged",
    )
    no_failure(SOURCE)
    require(not (FAILED / "FAILED_UNSEALED.json").exists(), "Retained failure remains sealed")
    require(not any(path.exists() for path in _ABSENT_RUNTIME), "Absent zip still absent")
    return dict(
        unique_paths=len(union),
        hashed_bytes=total,
        cache_bypassed_physical_resolution_and_full_SHA=True,
    )


def admitted_bytes(path):
    global _HASH_WORK
    actual = canonical(path)
    before, parts, state, total = fingerprint(actual), [], hashlib.sha256(), 0
    require(actual.is_file() and before[2] <= 128 * 1024**2, "Bounded regular code bytes")
    with actual.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            budget()
            total += len(chunk)
            _HASH_WORK += len(chunk)
            require(
                total <= before[2] and _HASH_WORK <= MAX_HASH_WORK, "Charged stable byte reader"
            )
            parts.append(chunk)
            state.update(chunk)
    require(total == before[2] and fingerprint(actual) == before, "Code read stable actual bytes")
    key = actual.relative_to(ROOT).as_posix() if actual.is_relative_to(ROOT) else str(actual)
    mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
    observed = state.hexdigest()
    require(
        mapping.get(key) == observed and (actual not in _OBSERVED or _OBSERVED[actual] == observed),
        "Admitted exact code SHA",
    )
    _OBSERVED[actual], _HASH_CACHE[actual] = observed, (before, observed)
    budget()
    return b"".join(parts)


def mpmath_runtime():
    budget()
    require(metadata.version("mpmath") == "1.3.0", "Pinned actual mpmath version")
    distribution = metadata.distribution("mpmath")
    require(distribution.files, "Actual nonempty mpmath distribution metadata")
    site = canonical(Path(sys.prefix) / "Lib/site-packages")
    package = canonical(site / "mpmath")
    metadata_roots = set()
    for entry in distribution.files:
        budget()
        parts = Path(str(entry)).parts
        for part in parts:
            if part.endswith(".dist-info"):
                metadata_roots.add(canonical(site / part))
    require(len(metadata_roots) == 1, "Exactly one actual mpmath dist-info root")
    roots = [package, *metadata_roots]
    total = count = 0
    for root in roots:
        require(root.is_relative_to(site) and root.parent == site, "Confined actual mpmath subtree")
        members = inventory(root)
        _RUNTIME_INVENTORIES[root] = members
        for path in sorted(members):
            budget()
            key = path.relative_to(ROOT).as_posix()
            require(key in _FROZEN, "EVERY actual package/cache/metadata byte already source-owned")
            require(digest(path) == _FROZEN[key], "Exact original mpmath runtime SHA")
            total += path.stat().st_size
            count += 1
            require(
                count <= MAX_RUNTIME_FILES and total <= MAX_RUNTIME_BYTES,
                "Bounded complete purePython mpmath runtime",
            )
    combined = _STANDARD_RUNTIME_MEMBERS | set().union(*_RUNTIME_INVENTORIES.values())
    combined_bytes = 0
    for path in combined:
        budget()
        combined_bytes += path.stat().st_size
        require(
            len(combined) <= MAX_RUNTIME_FILES and combined_bytes <= MAX_RUNTIME_BYTES,
            "Combined runtime24k/2GiB includes complete mpmath and metadata",
        )
    return dict(
        version="1.3.0",
        backend="python",
        package_files=count,
        package_bytes=total,
        complete_existing_bytecode_and_dist_info=True,
    )


def extracted_helpers():
    budget(admission=True)
    require(digest(OLD_AUDITOR) == OLD_AUDITOR_SHA, "Immutable failed auditor exact source")
    data = admitted_bytes(OLD_AUDITOR)
    tree = ast.parse(data, filename=str(OLD_AUDITOR))
    budget()
    definitions = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in HELPERS:
            require(
                node.name not in definitions and not node.decorator_list,
                "One undecorated exact extracted definition",
            )
            definitions[node.name] = node
    require(set(definitions) == set(HELPERS), "Exact finite8 definition allowlist")
    selected = ast.Module(body=[definitions[name] for name in HELPERS], type_ignores=[])
    require(
        all(isinstance(node, ast.FunctionDef) for node in selected.body),
        "No old imports, assignments, entrypoints or module body evaluation",
    )
    dumped = ast.dump(selected, include_attributes=False).encode("utf-8")
    budget()
    code = compile(selected, str(OLD_AUDITOR) + ":diagnostic-exact8", "exec")
    namespace = dict(
        Fraction=Fraction,
        require=require,
        check=lambda started, admission=False: budget(admission=admission),
        ITERATIONS=48,
        CORDIC_F=56,
        CORDIC_Q=1 << 56,
        CORDIC_EPSILON=Fraction(1, 1 << 56),
        __name__="root_controlled_exact8_interval_diagnostic",
    )
    exec(code, namespace)
    budget()
    return namespace, dict(
        original_source_sha256=OLD_AUDITOR_SHA,
        allowed_definition_names=list(HELPERS),
        extracted_AST_sha256=hashlib.sha256(dumped).hexdigest(),
        original_module_not_imported=True,
        original_entrypoint_or_guard_not_executed=True,
        original_definitions_AST_unchanged=True,
        runtime_diagnostic_half_ULP_predicate_retained_not_required=True,
    )


def diagnose(mp, namespace, primary):
    budget(admission=True)
    rational, encode = namespace["rational"], namespace["encode"]
    require(
        primary.get("schema") == "a14-cordic-literals-v1"
        and primary.get("iterations") == 48
        and primary.get("fractional_bits") == 56
        and primary.get("interval_digits") == 90,
        "Fixed original literal schema/precision/width/iteration scope",
    )
    rows = primary["angle_rows"]
    require(
        len(rows) == 48 and [row["i"] for row in rows] == list(range(48)),
        "All48 original literal identities exactly once",
    )
    gain = primary["gain_reciprocal"]
    independent = namespace["cordic_reference_literals"](
        mp, [row["raw"] for row in rows], gain["raw"], None, require_half_ULP=False
    )
    results = []
    for saved, fresh in zip(rows, independent["angles"], strict=True):
        budget()
        claimed = tuple(rational(value) for value in saved["true_turns_enclosure"])
        actual = tuple(rational(value) for value in fresh["true_turns_enclosure"])
        require(
            len(claimed) == len(actual) == 2
            and claimed[0] <= claimed[1]
            and actual[0] <= actual[1],
            "Ordered exact primary and130 endpoints",
        )
        declared_error = rational(saved["actual_abs_error_upper"])
        fresh_error = rational(fresh["actual_abs_error_upper"])
        contains = claimed[0] <= actual[0] <= actual[1] <= claimed[1]
        error_paid = 0 <= fresh_error <= declared_error
        row = dict(
            i=saved["i"],
            raw=saved["raw"],
            primary90_endpoints=saved["true_turns_enclosure"],
            independent130_endpoints=fresh["true_turns_enclosure"],
            primary90_abs_error_upper=saved["actual_abs_error_upper"],
            independent130_abs_error_upper=fresh["actual_abs_error_upper"],
            primary_contains_independent130=contains,
            independent130_error_no_greater_than_saved=error_paid,
            original_guard_comparison_passes=contains and error_paid,
            independent130_half_ULP_predicate=fresh["true_nearest_half_ULP_certified"],
        )
        if saved["i"] == 0:
            point, literal = Fraction(1, 8), Fraction(saved["raw"], 1 << 56)
            row["exact_analytic_a0_identity_diagnostic"] = dict(
                theorem="atan2(1,1)/(2*pi)=1/8 for positive real pi",
                point=encode(point),
                primary_contains_exact_point=claimed[0] <= point <= claimed[1],
                independent130_contains_exact_point=actual[0] <= point <= actual[1],
                actual_raw_equals_Q_over8=saved["raw"] == (1 << 56) // 8,
                exact_literal_error=encode(abs(literal - point)),
                exact_literal_error_no_greater_than_saved=abs(literal - point) <= declared_error,
                numerical_interval_not_replaced=True,
                no_original_audit_guard_waived=True,
            )
        results.append(row)
    fresh_gain = independent["reciprocal_gain"]
    claimed = tuple(rational(value) for value in gain["true_enclosure"])
    actual = tuple(rational(value) for value in fresh_gain["true_reciprocal_gain_enclosure"])
    require(
        len(claimed) == len(actual) == 2 and claimed[0] <= claimed[1] and actual[0] <= actual[1],
        "Ordered reciprocal gain endpoints",
    )
    gain_contains = claimed[0] <= actual[0] <= actual[1] <= claimed[1]
    gain_paid = (
        0
        <= rational(fresh_gain["actual_abs_error_upper"])
        <= rational(gain["actual_abs_error_upper"])
    )
    failing = [row["i"] for row in results if not row["original_guard_comparison_passes"]]
    return dict(
        schema="a14-all48-angle-and-finite-gain-interval-diagnostic-v1",
        independent_digits=130,
        primary_digits=90,
        angle_rows=results,
        actual_comparison_failing_indices=failing,
        first_actual_comparison_failing_index=failing[0] if failing else None,
        reciprocal_gain=dict(
            raw=gain["raw"],
            primary90_endpoints=gain["true_enclosure"],
            independent130_endpoints=fresh_gain["true_reciprocal_gain_enclosure"],
            primary90_abs_error_upper=gain["actual_abs_error_upper"],
            independent130_abs_error_upper=fresh_gain["actual_abs_error_upper"],
            primary_contains_independent130=gain_contains,
            independent130_error_no_greater_than_saved=gain_paid,
            original_guard_comparison_passes=gain_contains and gain_paid,
        ),
        finite_gain_enclosure=independent["finite_gain_enclosure"],
        every_actual_half_ULP_predicate=independent["every_actual_half_ULP_premise_certified"],
        all48_retained_even_if_comparison_fails=True,
        original_failed_packet_remains_failed=True,
        candidate_or_financial_or_resource_certificate=False,
        independent_audit_passed=False,
        adoption=False,
        full_G2=False,
        new_test_credit=0,
    )


def write(name, value):
    budget()
    with (OUTPUT / name).open("x", encoding="utf-8", newline="\n") as stream:
        for fragment in json.JSONEncoder(indent=2, sort_keys=True, allow_nan=False).iterencode(
            value
        ):
            budget()
            stream.write(fragment)
        stream.write("\n")
    budget()


def copy_input(path):
    budget()
    before = fingerprint(path)
    with path.open("rb") as source, (OUTPUT / path.name).open("xb") as target:
        while chunk := source.read(1024 * 1024):
            budget()
            target.write(chunk)
    require(
        fingerprint(path) == before and digest(OUTPUT / path.name) == digest(path),
        "Exact immutable source/preflight copy",
    )


def fail(error):
    if not OUTPUT.is_dir():
        return
    try:
        if (OUTPUT / "manifest.json").exists():
            (OUTPUT / "manifest.json").rename(OUTPUT / "partial_manifest.json")
    except OSError:
        pass
    try:
        if time.process_time() < CPU - 1 and time.monotonic() - _STARTED < WALL - 2:
            write(
                "failure.json",
                dict(
                    failed=True,
                    passed=False,
                    completed=False,
                    error_type=type(error).__name__,
                    error=str(error)[:2000],
                    budget_censored=None,
                    hard_budget_state_uncertified=True,
                    candidate_certificate=False,
                    independent_audit_passed=False,
                    new_test_credit=0,
                ),
            )
    except BaseException:
        pass
    try:
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"partial_success_invalid":true,"new_test_credit":0,"independent_audit_passed":false,"candidate_certificate":false}\n'
            )
    except OSError:
        pass


def main():
    global _STARTED, _SCIENTIFIC_ALLOWED
    _STARTED = process_started()
    runtime_scopes()
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    require(
        Path(os.path.abspath(args.output)) == OUTPUT and not OUTPUT.exists(),
        "Exact fresh fixed diagnostic receipt; no retry",
    )
    require(canonical(__file__) == AUTHOR, "Actual canonical new diagnostic module")
    budget(admission=True)
    OUTPUT.mkdir()
    try:
        add(METHOD, digest(METHOD))
        policy = read(METHOD)
        require(
            policy["schema"] == "a14-cosine-literal-diagnostic-preflight-v1"
            and policy["author_sha256"].keys() == {AUTHOR.name}
            and policy["CPU_admission_wall_seconds"] == [CPU, ADMISSION, WALL]
            and policy["interval_digits"] == 130
            and policy["iterations"] == 48
            and policy["source_manifest_SHA256"] == SOURCE_SHA
            and policy["failed_audit_manifest_SHA256"] == FAILED_SHA
            and policy["old_auditor_SHA256"] == OLD_AUDITOR_SHA
            and policy["runtime_backend"] == "python"
            and policy["mpmath_version"] == "1.3.0"
            and policy["numerical_threads"] == 1
            and policy["owned_files_bytes_cap"] == [MAX_OWN_FILES, MAX_OWN_BYTES]
            and policy["extracted_definition_names"] == list(HELPERS),
            "Exact frozen finite diagnostic policy and nonnull author pin",
        )
        add(AUTHOR, policy["author_sha256"][AUTHOR.name])
        require(
            digest(AUTHOR) == policy["author_sha256"][AUTHOR.name],
            "Actual reviewed new author bytes",
        )
        add(METHOD_DOC, policy["method_document_SHA256"])
        add(ORIGIN, ORIGIN_SHA)
        require(digest(ORIGIN) == ORIGIN_SHA, "Immutable copied metadata-runtime source")
        add(OLD_AUDITOR, OLD_AUDITOR_SHA)
        for path in (AUTHOR, METHOD, METHOD_DOC):
            copy_input(path)
        packet(SOURCE, SOURCE_SHA, failed=False)
        packet(FAILED, FAILED_SHA, failed=True)
        runtime = own_runtime()
        mp_runtime = mpmath_runtime()
        first = fresh_union()
        budget(admission=True)
        write(
            "admission.json",
            dict(
                schema="a14-literal-diagnostic-admission-v1",
                packet_map_counts=_PACKETS,
                own_runtime=runtime,
                mpmath_runtime=mp_runtime,
                first_fresh_union=first,
                ROOT_external_static_release_required=True,
                no_old_module_imported=True,
                no_candidate_approval=True,
            ),
        )
        os.environ["MPMATH_NOGMPY"] = "1"
        os.environ["MPMATH_NOSAGE"] = "1"
        _SCIENTIFIC_ALLOWED = True
        import mpmath as mp

        require(
            mp.__version__ == "1.3.0" and mp.libmp.BACKEND == "python",
            "Actual deferred purePython mpmath backend",
        )
        loaded_origins()
        mp.mp.dps = mp.iv.dps = 130
        require(mp.mp.dps == mp.iv.dps == 130, "Fixed130 interval/scalar contexts")
        namespace, extraction = extracted_helpers()
        primary = read(SOURCE / "cordic_literals.json")
        result = diagnose(mp, namespace, primary)
        write("extracted_definition_provenance.json", extraction)
        write("angle_gain_diagnostics.json", result)
        loaded_origins()
        second = fresh_union()
        write(
            "summary.json",
            dict(
                schema="a14-literal-interval-diagnostic-summary-v1",
                passed=True,
                completed=True,
                diagnostic_complete=True,
                budget_censored=False,
                fixed_angle_count=48,
                finite_gain_count=1,
                actual_comparison_failing_indices=result["actual_comparison_failing_indices"],
                first_actual_comparison_failing_index=result[
                    "first_actual_comparison_failing_index"
                ],
                gain_comparison_passes=result["reciprocal_gain"][
                    "original_guard_comparison_passes"
                ],
                both_full_input_union_passes=[first, second],
                source_manifest_sha256=SOURCE_SHA,
                failed_audit_manifest_sha256=FAILED_SHA,
                original_audit_remains_failed=True,
                original_primary_remains_provisional=True,
                allrow_PASS_claim=False,
                candidate_certificate=False,
                independent_audit_passed=False,
                full_G2=False,
                cost_transfer=False,
                adoption=False,
                new_test_credit=0,
                process_CPU_seconds=time.process_time(),
                wall_seconds_from_actual_process_creation=time.monotonic() - _STARTED,
                limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
            ),
        )
        require(
            not (OUTPUT / "manifest.json").exists()
            and not (OUTPUT / "completion_outcome.json").exists(),
            "Exclusive single terminal seal",
        )
        write(
            "completion_outcome.json",
            dict(
                completed=True,
                passed=True,
                diagnostic_complete=True,
                budget_censored=False,
                candidate_certificate=False,
                independent_audit_passed=False,
                adoption=False,
                full_G2=False,
                cost_transfer=False,
                new_test_credit=0,
                process_CPU_seconds=time.process_time(),
                wall_seconds_from_actual_process_creation=time.monotonic() - _STARTED,
            ),
        )
        owned = inventory(OUTPUT)
        require(
            len(owned) <= MAX_OWN_FILES
            and sum(path.stat().st_size for path in owned) <= MAX_OWN_BYTES,
            "Fixed64 owned files/128MiB diagnostic retention",
        )
        files = {}
        for path in sorted(owned):
            budget()
            files[path.relative_to(ROOT).as_posix()] = digest(path, fresh=True)
        write(
            "manifest.json",
            dict(
                schema="a14-literal-interval-diagnostic-manifest-v1",
                files=files,
                frozen_inputs=_FROZEN,
                external_runtime_inputs=_EXTERNAL,
                manifest_self_hash_excluded=True,
                completed=True,
                passed=True,
                budget_censored=False,
                diagnostic_only=True,
                original_expected_hashes_waived=False,
                candidate_certificate=False,
                independent_audit_passed=False,
                new_test_credit=0,
            ),
        )
        budget()
    except BaseException as error:
        fail(error)
        raise


if __name__ == "__main__":
    main()
