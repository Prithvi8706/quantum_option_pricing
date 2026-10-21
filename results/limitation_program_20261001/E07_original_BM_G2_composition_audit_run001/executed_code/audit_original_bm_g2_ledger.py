"""Author-only exact-source original BM G2 metadata composition.

No scientific builder, transcendental, circuit, fixture or estimator is executed.
The independent role recomputes admission and rational accounting without importing
the composer or its helper. Actual sealed bridge pins are required in root READY.
"""

from __future__ import annotations

import argparse
import copy
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from importlib import metadata
from importlib.util import cache_from_source
import json
import os
from pathlib import Path
import site
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
COMPOSER_AUTHOR = RESEARCH / "compose_original_bm_g2_ledger.py"
AUDIT_AUTHOR = RESEARCH / "audit_original_bm_g2_ledger.py"
METHOD = RESEARCH / "original_bm_g2_composition_preflight.json"
METHOD_DOC = RESEARCH / "ORIGINAL_BM_G2_COMPOSITION_PREFLIGHT.md"
READY = PROGRAM / "E07_original_BM_G2_AUDIT_READY_run001.json"
SOURCE = PROGRAM / "E07_original_BM_G2_composition_run001"
BRIDGE = PROGRAM / "A02_BM_native_financial_bridge_run002"
BRIDGE_AUDIT = PROGRAM / "A02_BM_native_financial_bridge_audit_run002"
FAILED_BRIDGE = PROGRAM / "A02_BM_native_financial_bridge_run001"
FAILED_BRIDGE_SHA = "8beb20bfe88407479953ddd7be284fd8fe94cea1e964c392340c4ab1a2376e02"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
BOOKKEEPING_ORIGIN = RESEARCH / "experiment_box_muller_polar_cdf_bv_v3.py"
BOOKKEEPING_ORIGIN_SHA = "e1e59867be43a8a66b8a7b5b9df88e41a23d2eaa211f7fe4fb101967312015a3"
CPU, ADMISSION, WALL = 300, 270, 900
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
CASES = {"B4x12": (4, 12, 30, 48, 1920), "B8x52": (8, 52, 234, 416, 14976)}
BIAS_NAMES = (
    "finite_input_law_and_joint_Box_Muller",
    "clipped_log_tail",
    "native_arithmetic_and_polynomial",
)
COMBINED_NAME = "original_joint_law_and_native_financial_bias"
_PATHS, _HASHES, _OBSERVED = {}, {}, {}
_EXTERNAL_TREES, _EXTERNAL_FILES = (), ()
_EXTERNAL_ROOT, _EXCLUDED_RUNTIME, _PROCESS_CREATION_TICKS = None, (), None
_REFERENCE_COUNT, _HASH_WORK, _UNIQUE_BYTES = 0, 0, 0
_UNIQUE_INPUTS = set()


class BudgetCensoredError(RuntimeError):
    """Fixed bookkeeping process limit; no scientific budget is changed."""


def require(condition, message):
    if not condition:
        raise ValueError(message)


def budget(started, admission=False):
    process_cpu = time.process_time() - started[0]
    wall = time.monotonic() - started[1]
    if process_cpu >= (ADMISSION if admission else CPU) or wall >= WALL:
        raise BudgetCensoredError("Composition 300CPU/270work/900wall fixed limit")
    return process_cpu, wall


def charge_hash(amount, started):
    global _HASH_WORK
    budget(started)
    _HASH_WORK += amount
    require(_HASH_WORK <= MAX_HASH_WORK, "Prospective 24GiB complete actual-byte hash-work limit")


def forbidden_imports():
    permitted = {__name__, "research.limitation_program_20261001"}
    forbidden = [
        name
        for name in sys.modules
        if name.split(".", 1)[0]
        in {"mpmath", "numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
        or (name.startswith("research.") and name not in permitted)
    ]
    require(
        not forbidden,
        "Stdlib-only composition; no producer/helper/scientific imports: " + repr(forbidden),
    )


ROLE = "auditor"
AUTHOR = AUDIT_AUTHOR
PRODUCER, AUDITOR = AUTHOR, COMPOSER_AUTHOR
OUTPUT = PROGRAM / "E07_original_BM_G2_composition_audit_run001"


def process_started():
    """Charge actual process CPU and creation-derived monotonic wall, including bootstrap."""
    global _PROCESS_CREATION_TICKS
    require(os.name == "nt" and ctypes.sizeof(ctypes.c_void_p) == 8, "Pinned Win64 runtime")
    library = ctypes.WinDLL("kernel32", use_last_error=True)
    library.GetCurrentProcess.argtypes = []
    library.GetCurrentProcess.restype = wintypes.HANDLE
    library.GetProcessTimes.argtypes = [wintypes.HANDLE, *([ctypes.POINTER(wintypes.FILETIME)] * 4)]
    library.GetProcessTimes.restype = wintypes.BOOL
    creation, exit_time, kernel, user = (wintypes.FILETIME() for _ in range(4))
    # GetCurrentProcess returns a pseudo-handle; it must not be closed as an owned handle.
    require(
        library.GetProcessTimes(
            library.GetCurrentProcess(),
            ctypes.byref(creation),
            ctypes.byref(exit_time),
            ctypes.byref(kernel),
            ctypes.byref(user),
        ),
        "Observe actual process creation time",
    )
    ticks = (creation.dwHighDateTime << 32) | creation.dwLowDateTime
    now_ns = time.time_ns()
    age_ns = now_ns - (ticks - 116444736000000000) * 100
    require(age_ns >= 0, "Observed process creation must precede current UTC")
    _PROCESS_CREATION_TICKS = ticks
    return 0.0, time.monotonic() - age_ns / 1_000_000_000


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def same(actual, expected, message):
    require(canonical(actual) == canonical(expected), message)


def read_bytes(path, started):
    """Parse only the bounded bytes whose actual SHA was observed in this invocation."""
    budget(started)
    actual = resolved(path, started)
    identity = stamp(actual)
    require(actual.is_file() and identity[2] <= 128 * 1024**2, "Bounded regular text input")
    state, chunks, total = hashlib.sha256(), [], 0
    with actual.open("rb") as stream:
        while block := stream.read(1 << 20):
            budget(started)
            total += len(block)
            require(total <= identity[2], "Text input grew beyond its observed byte bound")
            state.update(block)
            charge_hash(len(block), started)
            chunks.append(block)
            budget(started)
    require(stamp(actual) == identity and total == identity[2], "Text bytes changed while reading")
    value, key = state.hexdigest(), str(actual)
    require(
        key not in _OBSERVED or _OBSERVED[key] == value,
        "Parsed bytes contradict previously verified actual SHA",
    )
    _OBSERVED.setdefault(key, value)
    _HASHES[key] = (identity, value)
    data = b"".join(chunks)
    budget(started)
    return data


def read(path, started):
    data = read_bytes(path, started)
    budget(started)
    result = json.loads(data.decode("utf-8"))
    budget(started)
    return result


def save(path, value, started=None):
    if started is not None:
        budget(started)
    content = (json.dumps(value, indent=2, allow_nan=False) + "\n").encode()
    if started is not None:
        budget(started)
    with Path(path).open("xb") as stream:
        for offset in range(0, len(content), 1 << 20):
            if started is not None:
                budget(started)
            stream.write(content[offset : offset + (1 << 20)])
            if started is not None:
                budget(started)
    if started is not None:
        budget(started)


def setup(started):
    global _EXTERNAL_TREES, _EXTERNAL_FILES, _EXTERNAL_ROOT, _EXCLUDED_RUNTIME
    _PATHS.clear()
    _HASHES.clear()
    _OBSERVED.clear()
    require(sys.dont_write_bytecode is True, "Pinned interpreter must start with -B")
    require(Path.cwd().resolve() == ROOT, "Execute module from canonical workspace ROOT")
    require(Path(__file__).resolve() == PRODUCER.resolve(), "Execute exact producer author path")
    for name in ("PYTHONPATH", "PYTHONHOME", "SAGE_ROOT", "MPMATH_SAGE", "NUMBA_CACHE_DIR"):
        require(not os.environ.get(name), "Uncaptured runtime override: " + name)
    os.environ["MPMATH_NOGMPY"] = "1"
    os.environ["MPMATH_NOSAGE"] = "1"
    base = Path(getattr(sys, "_base_executable", sys.executable)).resolve(strict=True)
    prefix = Path(sys.base_prefix).resolve(strict=True)
    excluded = (prefix / "Lib/site-packages").absolute()
    _EXCLUDED_RUNTIME = tuple(dict.fromkeys((excluded, excluded.resolve())))
    _EXTERNAL_ROOT = prefix if not prefix.is_relative_to(ROOT) else None
    require(base.parent == prefix, "Actual base interpreter adjacent to base runtime prefix")
    _EXTERNAL_TREES = tuple(
        path.resolve(strict=True)
        for path in (prefix / "Lib", prefix / "DLLs")
        if path.is_dir() and not path.resolve().is_relative_to(ROOT)
    )
    _EXTERNAL_FILES = tuple(
        path.resolve(strict=True) for path in prefix.iterdir() if path.is_file()
    )
    require(base in _EXTERNAL_FILES or base.is_relative_to(ROOT), "Exact base runtime file scope")
    budget(started)


def reject_unreachable_origin(path, started):
    """Check even vanished module/cache origins before the existence shortcut."""
    budget(started)
    value = Path(path)
    require(not value.drive or value.is_absolute(), "No ambiguous origin drive-relative path")
    for candidate in (value.absolute(), value.resolve(strict=False)):
        require(
            not any(
                candidate == scope or candidate.is_relative_to(scope) for scope in _EXCLUDED_RUNTIME
            ),
            "Unreachable base site-packages origin or alias is forbidden",
        )
    budget(started)


def allowed(path):
    if any(path == scope or path.is_relative_to(scope) for scope in _EXCLUDED_RUNTIME):
        return False
    return (
        path.is_relative_to(ROOT)
        or path == _EXTERNAL_ROOT
        or path in _EXTERNAL_FILES
        or any(path.is_relative_to(scope) for scope in _EXTERNAL_TREES)
    )


def resolved(path, started, fresh=False):
    budget(started)
    value = Path(path)
    require(not value.drive or value.is_absolute(), "No ambiguous drive-relative path")
    require(
        not any(
            value.absolute() == scope or value.absolute().is_relative_to(scope)
            for scope in _EXCLUDED_RUNTIME
        ),
        "Unreachable base site-packages is forbidden",
    )
    lexical = str(value.absolute())
    if not fresh and lexical in _PATHS:
        return _PATHS[lexical]
    actual = value.resolve(strict=True)
    require(allowed(actual), "Path outside ROOT and exact actual base-runtime scopes")
    require(
        not fresh or lexical not in _PATHS or _PATHS[lexical] == actual,
        "Previously confined lexical alias redirected",
    )
    _PATHS[lexical] = actual
    _PATHS.setdefault(str(actual), actual)
    budget(started)
    return actual


def stamp(path):
    value = path.stat()
    return (
        value.st_dev,
        value.st_ino,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
        getattr(value, "st_file_attributes", None),
        getattr(value, "st_reparse_tag", None),
    )


def sha(path, started, fresh=False):
    actual = resolved(path, started, fresh=fresh)
    return digest(actual, started, fresh=fresh)


def digest(actual, started, fresh=False):
    budget(started)
    key, identity = str(actual), stamp(actual)
    if not fresh and key in _HASHES and _HASHES[key][0] == identity:
        budget(started)
        return _HASHES[key][1]
    result = hashlib.sha256()
    with actual.open("rb") as stream:
        while block := stream.read(1 << 20):
            budget(started)
            result.update(block)
            charge_hash(len(block), started)
            budget(started)
    require(stamp(actual) == identity, "Actual input changed during hashing")
    value = result.hexdigest()
    require(
        key not in _OBSERVED or _OBSERVED[key] == value, "Previously observed actual SHA changed"
    )
    _OBSERVED.setdefault(key, value)
    _HASHES[key] = (identity, value)
    budget(started)
    return value


def relative(path, started):
    return resolved(path, started).relative_to(ROOT).as_posix()


def bind(frozen, external, path, expected, started):
    global _REFERENCE_COUNT, _UNIQUE_BYTES
    budget(started)
    _REFERENCE_COUNT += 1
    require(_REFERENCE_COUNT <= MAX_REFERENCES, "Prospective 100000 reference bound")
    require(
        type(expected) is str
        and len(expected) == 64
        and all(character in "0123456789abcdef" for character in expected),
        "Canonical expected SHA256",
    )
    actual = resolved(path, started)
    require(actual.is_file(), "Expected input must be a regular file")
    if actual not in _UNIQUE_INPUTS:
        _UNIQUE_INPUTS.add(actual)
        _UNIQUE_BYTES += actual.stat().st_size
        require(_UNIQUE_BYTES <= MAX_UNIQUE_BYTES, "Prospective 8GiB unique input union bound")
    if actual.is_relative_to(ROOT):
        target, key = frozen, actual.relative_to(ROOT).as_posix()
    else:
        target, key = external, str(actual)
    require(key not in target or target[key] == expected, "Conflicting canonical expected SHA")
    require(sha(actual, started) == expected, "Original expected input SHA mismatch: " + key)
    target[key] = expected
    budget(started)
    return actual


def verify(frozen, external, started):
    for mapping, prefix in ((frozen, ROOT), (external, None)):
        for key, expected in mapping.items():
            budget(started)
            path = prefix / key if prefix is not None else Path(key)
            require(sha(path, started) == expected, "Frozen input changed: " + key)


def final_verify(frozen, external, started):
    for lexical, previous in tuple(_PATHS.items()):
        budget(started)
        require(resolved(lexical, started, fresh=True) == previous, "Fresh lexical alias changed")
    expected = {}
    for mapping, prefix in ((frozen, ROOT), (external, None)):
        for key, value in mapping.items():
            actual = resolved(prefix / key if prefix is not None else key, started)
            require(actual not in expected or expected[actual] == value, "Final equal-SHA merge")
            expected[actual] = value
    observed = {Path(key): value for key, value in _OBSERVED.items()}
    for path in sorted(set(expected) | set(observed)):
        budget(started)
        actual = resolved(path, started, fresh=True)
        value = digest(actual, started, fresh=True)
        require(path not in expected or value == expected[path], "Fresh expected input SHA changed")
        require(
            path not in observed or value == observed[path], "Fresh observed actual SHA changed"
        )
    return len(set(expected) | set(observed))


def runtime_candidates(root, started):
    """Prune the explicitly unreachable base site subtree before enumeration."""
    root = resolved(root, started)
    if root.is_file():
        yield root
        return
    require(root.is_dir(), "Actual runtime inventory root")
    pending, seen = [root], set()
    while pending:
        budget(started)
        current = pending.pop()
        require(current not in seen, "No aliased or recursive runtime directory")
        seen.add(current)
        for candidate in current.iterdir():
            budget(started)
            if any(candidate.absolute() == scope for scope in _EXCLUDED_RUNTIME):
                continue
            actual = resolved(candidate, started)
            require(actual.is_relative_to(root), "Runtime tree alias escaped its exact root")
            if actual.is_dir():
                pending.append(actual)
            elif actual.is_file():
                yield actual


def bootstrap_runtime_paths(site_root, started):
    """Actual startup hooks and loaded venv bytes, without admitting other packages."""
    paths = []
    for path in site_root.iterdir():
        budget(started)
        customize_name = path.name.split(".", 1)[0] in ("sitecustomize", "usercustomize")
        is_hook = path.is_file() and (
            path.suffix.lower() == ".pth"
            or customize_name
            and path.suffix.lower() in (".py", ".pyc", ".pyd")
        )
        is_package = path.is_dir() and path.name in ("sitecustomize", "usercustomize")
        if is_hook or is_package:
            actual_hook = resolved(path, started)
            require(
                actual_hook.is_relative_to(site_root),
                "Startup hook must stay in actual isolated venv",
            )
            paths.append(actual_hook)
            if path.suffix == ".py":
                cached = Path(cache_from_source(str(path)))
                if cached.is_file():
                    actual_cache = resolved(cached, started)
                    require(
                        actual_cache.is_relative_to(site_root), "Startup hook cache confinement"
                    )
                    paths.append(actual_cache)
    for name, module in tuple(sys.modules.items()):
        budget(started)
        if module is None:
            continue
        for origin in (getattr(module, "__file__", None), getattr(module, "__cached__", None)):
            if origin:
                reject_unreachable_origin(origin, started)
            if origin and Path(origin).is_file():
                actual = resolved(origin, started)
                if Path(origin).absolute().is_relative_to(site_root):
                    require(
                        actual.is_relative_to(site_root),
                        "Loaded bootstrap alias escaped actual isolated venv",
                    )
                if actual.is_relative_to(site_root) and not actual.is_relative_to(
                    site_root / "mpmath"
                ):
                    paths.append(actual)
    return sorted(set(paths))


def venv_adjacent_runtime_paths(prefix, started):
    """Record the exact admitted venv-root directory and its importable adjacent bytes."""
    paths, membership = [], []
    for candidate in prefix.iterdir():
        budget(started)
        actual = resolved(candidate, started)
        require(
            actual.parent == prefix and actual.name == candidate.name,
            "Actual venv-root member must remain directly confined without an alias",
        )
        if actual.is_file():
            membership.append([candidate.name, "file"])
            paths.append(actual)
        elif actual.is_dir():
            membership.append([candidate.name, "directory"])
            # Lib and Scripts have their separately declared complete reachable inventories.
            # A directly importable package or adjacent cache is not covered by that scope.
            if actual.name == "__pycache__" or any(
                (actual / name).is_file() for name in ("__init__.py", "__init__.pyc")
            ):
                require(actual.name not in ("Lib", "Scripts"), "No ambiguous venv package root")
                paths.append(actual)
        else:
            require(False, "Only regular file/directory venv-root members")
    return sorted(set(paths)), sorted(membership)


def inventory(paths, frozen, external, started):
    """Freeze actual directory contents, including existing caches, not RECORD alone."""
    files, total = {}, 0
    for root in paths:
        budget(started)
        root = resolved(root, started)
        candidates = runtime_candidates(root, started)
        for candidate in candidates:
            budget(started)
            if not candidate.is_file():
                continue
            path = resolved(candidate, started)
            require(path == root or path.is_relative_to(root), "Runtime directory escape")
            if path in files:
                continue
            total += path.stat().st_size
            require(len(files) < MAX_RUNTIME_FILES and total <= MAX_RUNTIME_BYTES, "Runtime cap")
            expected = sha(path, started)
            bind(frozen, external, path, expected, started)
            files[path] = expected
    return dict(
        files=len(files),
        bytes=total,
        roots=[str(path) for path in paths],
        actual_file_paths=sorted(str(path) for path in files),
    )


def runtime(frozen, external, started):
    prefix = resolved(sys.prefix, started)
    require(prefix == ROOT / ".context/frontier_t0_env", "Pinned isolated venv")
    require(resolved(sys.executable, started) == LAUNCHER, "Actual launcher provenance")
    require(site.ENABLE_USER_SITE is False, "User site disabled")
    config = prefix / "pyvenv.cfg"
    require(
        "include-system-site-packages = false" in read_bytes(config, started).decode().lower(),
        "Isolated venv",
    )
    site_root = resolved(prefix / "Lib/site-packages", started)
    distribution = metadata.distribution("mpmath")
    require(distribution.version == "1.3.0", "Fixed installed mpmath version")
    members = distribution.files
    require(members, "Nonempty mpmath installed metadata inventory")
    metadata_roots = set()
    for member in members:
        budget(started)
        path = resolved(distribution.locate_file(member), started)
        for parent in (path, *path.parents):
            if parent.name.endswith(".dist-info"):
                metadata_roots.add(parent)
                break
    require(len(metadata_roots) == 1, "Exactly one mpmath distribution metadata root")
    metadata_root = next(iter(metadata_roots))
    require(metadata_root.parent == site_root, "Confined actual distribution metadata")
    base_prefix = resolved(sys.base_prefix, started)
    roots = [
        config,
        prefix / "Scripts",
        site_root / "mpmath",
        metadata_root,
        base_prefix / "Lib",
        base_prefix / "DLLs",
        *_EXTERNAL_FILES,
    ]
    bootstrap_paths = bootstrap_runtime_paths(site_root, started)
    roots.extend(bootstrap_paths)
    adjacent_paths, adjacent_membership = venv_adjacent_runtime_paths(prefix, started)
    roots.extend(adjacent_paths)
    for source in (ROOT / "research/__init__.py", RESEARCH / "__init__.py"):
        if source.is_file():
            roots.append(source)
            cached = Path(cache_from_source(str(source)))
            if cached.is_file():
                roots.append(cached)
    # Existing producer/auditor bytecode is captured even though startup -B prevents writes.
    for source in (PRODUCER, AUDITOR):
        cached = Path(cache_from_source(str(source)))
        if cached.is_file():
            roots.append(cached)
    counts = inventory([path for path in roots if path.exists()], frozen, external, started)
    allowed_import_roots = (
        ROOT,
        prefix,
        site_root,
        base_prefix,
        base_prefix / "Lib",
        base_prefix / "DLLs",
    )
    absent = []
    for entry in sys.path:
        budget(started)
        candidate = Path(entry or ROOT)
        reject_unreachable_origin(candidate, started)
        if not candidate.exists():
            actual = candidate.resolve()
            expected_zip = base_prefix / (
                "python" + str(sys.version_info.major) + str(sys.version_info.minor) + ".zip"
            )
            require(actual == expected_zip, "Only standard absent interpreter zip path")
            absent.append(str(actual))
            continue
        path = resolved(entry or ROOT, started)
        require(
            path in _EXTERNAL_FILES or any(path == root for root in allowed_import_roots),
            "Unexpected sys.path entry: " + str(path),
        )
    return dict(
        python_version=sys.version,
        executable=str(resolved(sys.executable, started)),
        base_executable=str(resolved(sys._base_executable, started)),
        base_prefix=str(base_prefix),
        venv_prefix=str(prefix),
        mpmath_version=distribution.version,
        backend="python",
        MPMATH_NOGMPY="1",
        MPMATH_NOSAGE="1",
        startup_bytecode_disabled=True,
        user_site_disabled=True,
        runtime_inventory=counts,
        sys_path=list(sys.path),
        external_runtime_trees=[str(path) for path in _EXTERNAL_TREES],
        external_adjacent_files=[str(path) for path in _EXTERNAL_FILES],
        absent_standard_runtime_paths=absent,
        excluded_base_site_packages=str((Path(sys.base_prefix) / "Lib/site-packages").resolve()),
        excluded_base_site_packages_lexical=str(
            (Path(sys.base_prefix) / "Lib/site-packages").absolute()
        ),
        base_site_packages_import_rejected=True,
        bootstrap_hook_and_loaded_venv_paths=[str(path) for path in bootstrap_paths],
        standard_Lib_excludes_only_unreachable_base_site_packages=True,
        other_installed_venv_packages_not_blanket_admitted=True,
        exact_sys_prefix_search_path_admitted=True,
        venv_adjacent_runtime_paths=[str(path) for path in adjacent_paths],
        venv_root_directory_membership=adjacent_membership,
    )


def runtime_policy(record, started):
    budget(started)
    require(sys.version == record["python_version"], "Actual recorded interpreter version")
    require(
        str(resolved(sys.executable, started)) == record["executable"], "Actual recorded launcher"
    )
    require(
        str(resolved(sys._base_executable, started)) == record["base_executable"],
        "Actual base interpreter",
    )
    require(str(resolved(sys.base_prefix, started)) == record["base_prefix"], "Actual base prefix")
    require(
        str(resolved(sys.prefix, started)) == record["venv_prefix"], "Actual isolated venv prefix"
    )
    same(list(sys.path), record["sys_path"], "Unchanged actual interpreter search paths")
    require(
        record["excluded_base_site_packages"]
        == str((Path(sys.base_prefix) / "Lib/site-packages").resolve())
        and record["excluded_base_site_packages_lexical"]
        == str((Path(sys.base_prefix) / "Lib/site-packages").absolute())
        and record["base_site_packages_import_rejected"] is True,
        "Exact explicitly unreachable runtime scope",
    )
    require(
        record["standard_Lib_excludes_only_unreachable_base_site_packages"] is True
        and record["other_installed_venv_packages_not_blanket_admitted"] is True,
        "Explicit reachable-runtime operational policy",
    )
    site_root = resolved(Path(sys.prefix) / "Lib/site-packages", started)
    adjacent_paths, adjacent_membership = venv_adjacent_runtime_paths(
        resolved(sys.prefix, started), started
    )
    require(
        record["exact_sys_prefix_search_path_admitted"] is True,
        "Exact Windows venv-prefix search path policy",
    )
    same(
        [str(path) for path in adjacent_paths],
        record["venv_adjacent_runtime_paths"],
        "Actual adjacent venv runtime byte roots unchanged",
    )
    same(
        adjacent_membership,
        record["venv_root_directory_membership"],
        "Exact finite venv-root directory membership unchanged",
    )
    same(
        [str(path) for path in bootstrap_runtime_paths(site_root, started)],
        record["bootstrap_hook_and_loaded_venv_paths"],
        "Exact actual startup hook membership",
    )
    for entry in sys.path:
        budget(started)
        path = Path(entry or ROOT)
        reject_unreachable_origin(path, started)
        if path.exists():
            resolved(path, started)
    same(
        [str(path) for path in _EXTERNAL_TREES],
        record["external_runtime_trees"],
        "Exact external tree scope",
    )
    same(
        [str(path) for path in _EXTERNAL_FILES],
        record["external_adjacent_files"],
        "Exact adjacent runtime scope",
    )
    require(
        site.ENABLE_USER_SITE is False and sys.dont_write_bytecode is True, "Isolated startup -B"
    )
    require(
        metadata.version("mpmath") == record["mpmath_version"] == "1.3.0", "Fixed runtime metadata"
    )
    for path in record["absent_standard_runtime_paths"]:
        budget(started)
        require(not Path(path).exists(), "Previously absent interpreter zip path appeared")
    require(
        os.environ.get("MPMATH_NOGMPY") == os.environ.get("MPMATH_NOSAGE") == "1",
        "Pure Python backend policy",
    )
    actual_files = set()
    for name in record["runtime_inventory"]["roots"]:
        root = resolved(name, started)
        for candidate in runtime_candidates(root, started):
            budget(started)
            if candidate.is_file():
                actual = resolved(candidate, started)
                require(
                    actual == root or actual.is_relative_to(root), "Runtime inventory scope escape"
                )
                actual_files.add(str(actual))
    same(
        sorted(actual_files),
        record["runtime_inventory"]["actual_file_paths"],
        "Complete runtime byte inventory membership unchanged",
    )
    forbidden_imports()


def verify_loaded(frozen, external, started):
    forbidden_imports()
    observed = []
    for name, module in tuple(sys.modules.items()):
        budget(started)
        if module is None:
            continue
        origin = getattr(module, "__file__", None)
        for field, value in (("source", origin), ("cache", getattr(module, "__cached__", None))):
            if value:
                reject_unreachable_origin(value, started)
            if not value or not Path(value).is_file():
                continue
            path = resolved(value, started)
            key = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
            mapping = frozen if path.is_relative_to(ROOT) else external
            require(key in mapping, "Loaded module byte origin not frozen: " + name + ":" + key)
            require(sha(path, started) == mapping[key], "Loaded module origin changed")
            observed.append(dict(module=name, kind=field, path=key, sha256=mapping[key]))
    return observed


def copy_exact(source, destination, frozen, external, started):
    budget(started)
    expected = sha(source, started)
    with Path(source).open("rb") as incoming, Path(destination).open("xb") as outgoing:
        while block := incoming.read(1 << 20):
            budget(started)
            outgoing.write(block)
            budget(started)
    require(sha(destination, started) == expected, "Exclusive immutable copy equality")
    bind(frozen, external, destination, expected, started)


def elapsed(started):
    return dict(
        process_CPU_seconds=time.process_time() - started[0],
        wall_seconds=time.monotonic() - started[1],
    )


def owned_files(output, started):
    files, total = {}, 0
    for path in output.rglob("*"):
        budget(started)
        if not path.is_file():
            continue
        require(path.name != "manifest.json", "No terminal/partial manifest reuse")
        require(resolved(path, started).is_relative_to(output), "Owned output confinement")
        total += path.stat().st_size
        require(len(files) < 64 and total <= 128 * 1024**2, "Finite owned artifacts cap")
        files[path.relative_to(output).as_posix()] = sha(path, started)
    return files


def exact(value):
    require(type(value) is list and len(value) == 2, "Exact rational integer pair")
    require(all(type(part) is int for part in value) and value[1] > 0, "No float/bool rational")
    result = Fraction(*value)
    require(result >= 0, "Nonnegative bound")
    return result


def encode(value):
    return [value.numerator, value.denominator]


def historical_fingerprint(value, started):
    """Use the original wrapper's exact JSON serialization, without circuit work."""
    budget(started)
    data = json.dumps(value, sort_keys=True, allow_nan=False).encode()
    budget(started)
    result = hashlib.sha256(data).hexdigest()
    charge_hash(len(data), started)
    return result


def no_failure(receipt):
    names = (
        "FAILED_UNSEALED.json",
        "failed_unsealed.json",
        "failure.json",
        "run_failure.json",
        "prepare_failure.json",
    )
    require(
        not any((receipt / name).exists() for name in names),
        "Authoritative failure marker prohibits admission",
    )


def packet(receipt, expected_manifest, frozen, external, started, preserve_failed=False):
    """Verify complete actual packet bytes without importing its executed code."""
    receipt = resolved(receipt, started)
    require(receipt.is_relative_to(PROGRAM) and receipt.is_dir(), "Declared ROOT receipt")
    if preserve_failed:
        require(
            receipt == FAILED_BRIDGE and expected_manifest == FAILED_BRIDGE_SHA,
            "Only the exact historical failed bridge packet",
        )
    else:
        no_failure(receipt)
    mf_path = bind(frozen, external, receipt / "manifest.json", expected_manifest, started)
    mf = read(mf_path, started)
    flat = receipt == PROGRAM / "A10_coefficient_run001" and "files" not in mf
    if flat:
        own_map, frozen_map, external_map = mf, {}, {}
    else:
        require(mf.get("manifest_self_hash_excluded") is True, "Exact manifest self exclusion")
        own_map, frozen_map, external_map = (
            mf.get(name, {}) for name in ("files", "frozen_inputs", "external_runtime_inputs")
        )
    require(
        type(own_map) is dict
        and own_map
        and type(frozen_map) is dict
        and type(external_map) is dict,
        "Complete recognized maps",
    )
    actual_owned = set()
    for original, expected in own_map.items():
        budget(started)
        require(type(original) is str and not Path(original).is_absolute(), "Owned relative key")
        key = original.replace("\\", "/")
        candidate = ROOT / key if key.startswith("results/") else receipt / key
        actual = bind(frozen, external, candidate, expected, started)
        require(
            actual.is_relative_to(receipt) and actual.name != "manifest.json",
            "Own map confinement and no self hash",
        )
        require(actual not in actual_owned, "No duplicate/aliased own entry")
        actual_owned.add(actual)
        expected_key = (
            actual.relative_to(ROOT).as_posix()
            if key.startswith("results/")
            else actual.relative_to(receipt).as_posix()
        )
        require(
            key == expected_key,
            "Canonical owned path after explicit historical slash normalization",
        )
    for original, expected in frozen_map.items():
        budget(started)
        require(
            type(original) is str and not Path(original).is_absolute(), "ROOT-relative frozen key"
        )
        key = original.replace("\\", "/")
        actual = bind(frozen, external, ROOT / key, expected, started)
        require(
            actual.is_relative_to(ROOT) and actual.relative_to(ROOT).as_posix() == key,
            "Canonical ROOT frozen input",
        )
    for key, expected in external_map.items():
        budget(started)
        require(
            type(key) is str and Path(key).is_absolute(), "Explicit external actual runtime key"
        )
        actual = bind(frozen, external, key, expected, started)
        require(
            not actual.is_relative_to(ROOT) and str(actual) == key,
            "Separate canonical external runtime scope",
        )
    found, total = set(), 0
    for path in receipt.rglob("*"):
        budget(started)
        if path.is_file():
            actual = resolved(path, started)
            require(
                actual.is_relative_to(receipt) and actual not in found, "No owned alias or escape"
            )
            found.add(actual)
            total += actual.stat().st_size
            require(
                len(found) <= 25000 and total <= MAX_UNIQUE_BYTES, "Finite owned directory bound"
            )
    require(found == actual_owned | {mf_path}, "Exact actual owned membership")
    summary = (
        read(receipt / "summary.json", started) if (receipt / "summary.json").is_file() else None
    )
    if summary is not None and not preserve_failed:
        if receipt == PROGRAM / "A02_BM_native_financial_bridge_root_review_run001":
            require(
                summary["root_and_independent_mathematical_source_protocol_review_passed"] is True
                and summary["authors_frozen"] is True
                and summary["scientific_code_or_proof_or_source_walk_executed_by_static_review"]
                is False
                and summary["new_fixture_credit"] == 0,
                "Actual prior static root review, not a scientific PASS",
            )
            same(
                [len(own_map), len(frozen_map), len(external_map)],
                [1, 11, 0],
                "Exact static review complete maps",
            )
        else:
            require(
                summary.get("passed") is True and summary.get("budget_censored", False) is False,
                "Actual successful scoped summary",
            )
        require(
            summary.get("failed", False) is False and summary.get("rejection", False) is False,
            "No failed or rejected prerequisite",
        )
    outcome = None
    if (receipt / "completion_outcome.json").is_file():
        outcome = read(receipt / "completion_outcome.json", started)
        if preserve_failed:
            require(
                mf["completed"] is False
                and mf["passed"] is False
                and outcome["completed"] is False
                and outcome["passed"] is False
                and outcome["failed"] is True,
                "Historical failure remains failure with zero credit",
            )
            require(
                (receipt / "failure.json").is_file() and outcome["new_test_credit"] == 0,
                "Actual failure evidence preserved",
            )
            same(
                [len(own_map), len(frozen_map), len(external_map)],
                [20, 346, 2842],
                "Exact full historical failed packet maps",
            )
        else:
            for value in (mf, outcome, summary):
                require(
                    type(value) is dict
                    and value.get("completed") is True
                    and value.get("passed") is True,
                    "Actual complete terminal PASS",
                )
                require(
                    value.get("budget_censored") is False
                    and value.get("failed", False) is False
                    and value.get("rejection", False) is False,
                    "Uncensored successful terminal",
                )
        limit = (
            [180, 600]
            if receipt
            in (
                BRIDGE,
                BRIDGE_AUDIT,
                FAILED_BRIDGE,
                PROGRAM / "A02_polar_cdf_bv_run003",
                PROGRAM / "A02_polar_cdf_bv_audit_run003",
            )
            else [300, 900]
        )
        observations = [outcome["budget"], mf["terminal_budget_observation"]]
        if summary is not None and "budget" in summary:
            observations.append(summary["budget"])
        for observation in observations:
            require(
                0 <= observation["process_CPU_seconds"] < limit[0]
                and 0 <= observation["wall_seconds"] < limit[1],
                "Original packet terminal hard limits",
            )
    if not preserve_failed:
        no_failure(receipt)
    return {
        "manifest_sha256": expected_manifest,
        "manifest": mf,
        "summary": summary,
        "outcome": outcome,
        "owned_count": len(actual_owned),
        "legacy_absent_terminal_flags_convention": outcome is None,
    }


def ready_policy(frozen, external, started):
    ready = read(READY, started)
    require(
        ready.get("schema") == "original-bm-G2-composition-root-READY-v1"
        and ready.get("ready") is True,
        "Actual root READY required",
    )
    same(ready["limits_CPU_work_wall"], [CPU, ADMISSION, WALL], "Root fixed bookkeeping limits")
    require(
        ready["stdlib_only"] is True and ready["threads"] == 1,
        "Exact stdlib-only one-thread release",
    )
    paths = (COMPOSER_AUTHOR, AUDIT_AUTHOR, METHOD, METHOD_DOC)
    keys = {path.relative_to(ROOT).as_posix() for path in paths}
    require(
        type(ready["author_inputs"]) is dict and set(ready["author_inputs"]) == keys,
        "All four exact author/method SHA pins",
    )
    for key, expected in ready["author_inputs"].items():
        bind(frozen, external, ROOT / key, expected, started)
    bind(frozen, external, READY, sha(READY, started), started)
    bind(frozen, external, LAUNCHER, ready["interpreter_sha256"], started)
    bind(frozen, external, BOOKKEEPING_ORIGIN, BOOKKEEPING_ORIGIN_SHA, started)
    method = read(METHOD, started)
    require(
        method["schema"] == "original-bm-exact-source-G2-composition-author-preflight-v1",
        "Exact held method",
    )
    require(
        method["local_only"] is True and method["new_fixture_credit"] == 0,
        "Fixed no-credit local method",
    )
    same(
        [
            method["prospective_execution"][name]
            for name in ("CPU_seconds", "work_admission_CPU_seconds", "wall_seconds")
        ],
        [CPU, ADMISSION, WALL],
        "Method and root limits equal",
    )
    declared = method["selected_existing_owner_manifest_expected_pins"]
    bridge_pins = method["required_actual_native_bridge_packets"]
    manifest_keys = set(declared) | set(bridge_pins)
    require(
        type(ready["manifest_inputs"]) is dict and set(ready["manifest_inputs"]) == manifest_keys,
        "Exact complete fixed prerequisite manifest inventory",
    )
    for key, expected in declared.items():
        require(ready["manifest_inputs"][key] == expected, "No historical expected SHA override")
    for key, prospective in bridge_pins.items():
        value = ready["manifest_inputs"][key]
        require(
            type(value) is str and len(value) == 64,
            "Null actual bridge PASS pin blocks preparation",
        )
        require(
            prospective is None or prospective == value, "Non-null actual expectation preserved"
        )
    for role, module, output in (
        ("producer", "research.limitation_program_20261001.compose_original_bm_g2_ledger", SOURCE),
        (
            "auditor",
            "research.limitation_program_20261001.audit_original_bm_g2_ledger",
            PROGRAM / "E07_original_BM_G2_composition_audit_run001",
        ),
    ):
        for operation in ("prepare", "run"):
            expected_cli = [str(LAUNCHER), "-B", "-m", module, operation, "--output", str(output)]
            same(
                ready["commands"][role + "_" + operation],
                expected_cli,
                "Pinned exact CLI and ordering",
            )
    return ready, method


def prerequisites(ready, frozen, external, started):
    reports = {}
    for key, pin in ready["manifest_inputs"].items():
        receipt = (ROOT / key).parent
        reports[Path(key).parent.name] = packet(
            receipt, pin, frozen, external, started, preserve_failed=receipt == FAILED_BRIDGE
        )
    source, audit = reports[BRIDGE.name], reports[BRIDGE_AUDIT.name]
    require(
        source["manifest"]["schema"] == "box-muller-native-financial-bridge-terminal-manifest-v1",
        "Original native bridge manifest",
    )
    require(
        audit["manifest"]["schema"]
        == "box-muller-native-financial-bridge-independent-audit-manifest-v1",
        "Independent native bridge manifest",
    )
    for item in (source, audit):
        summary = item["summary"]
        require(
            summary["native_financial_bias_certificate_valid"] is True
            and summary["financial_residual_fit"] is True,
            "Actual native bridge proof and residual fit",
        )
        require(
            summary["new_test_credit"] == 0 and summary["new_gate_replays"] == 0,
            "No fixture or replay recredit",
        )
        require(
            summary["full_G2"] is False
            and summary["adoption"] is False
            and summary["cost_transfer"] is False,
            "Original scoped source claims unchanged",
        )
        same(summary["unchanged_financial_residual"], [11, 2000], "Unchanged aggregate residual")
    require(
        audit["summary"]["independent_audit_passed"] is True
        and audit["summary"]["source_passed"] is True
        and audit["summary"]["source_rejection_retained"] is False,
        "Actual independent component approval",
    )
    require(
        audit["summary"]["complete_primary_bound_authorized_by_independent130"] is True,
        "Primary bridge bound independently authorized",
    )
    require(
        audit["summary"]["source_manifest_sha256"] == source["manifest_sha256"],
        "Independent audit binds exact actual primary",
    )
    require(
        source["summary"]["exact_original_contract_and_strict_barrier_ties_preserved"] is True,
        "Audited original contract rather than continuous-monitoring or replacement target",
    )
    for item in (source, audit):
        same(
            item["summary"]["actual_joint_pair_counts"],
            {"B4x12": 30, "B8x52": 234},
            "Actual complete original joint laws",
        )
        require(
            item["summary"]["actual_stock_sites"] == 464
            and item["summary"]["all_actual_native_emitted_dead_paths_product144_and_stored72_safe"]
            is True,
            "Complete actual financial/native safety scope",
        )
    return reports


def case_inputs(case, reports, started):
    old = read(PROGRAM / "E07_complete_run001" / (case + "_complete_price_ledger.json"), started)
    estimator = read(PROGRAM / "E02_financial_run002" / case / "estimator_ledger.json", started)
    iqft = read(PROGRAM / "E02_IQFT_run001" / case / "synthesized_estimator_ledger.json", started)
    support = read(PROGRAM / "E03_support_run001" / (case + "_certificate.json"), started)
    support_audit = read(PROGRAM / "E03_support_audit_run002" / (case + "_audit.json"), started)
    wrapper_path = PROGRAM / "E02_financial_run002" / case / "iterate.json"
    wrapper = read(wrapper_path, started)
    wrapper_audit = read(
        PROGRAM / "E02_financial_audit_run001" / (case + "_wrapper_audit.json"), started
    )
    binding = read(BRIDGE / "native_source_binding.json", started)
    polar_binding = read(PROGRAM / "A02_polar_cdf_bv_run003/source_binding.json", started)
    independent_binding = read(
        PROGRAM / "A02_polar_cdf_bv_audit_run003/independent_source_binding.json", started
    )
    same(binding, polar_binding, "Native bridge and actual polar source roles exactly match")
    same(binding, independent_binding, "Independent original source-role binding agrees")
    same(
        binding["convention"]["priors"],
        [[3, 10], [2, 5], [100, 1], [3, 100], [1, 1], [100, 1], [140, 1]],
        "Exact sigma/rho/spot/rate/T/strike/barrier reference contract",
    )
    require(
        binding["convention"]["ideal_reference_is_exact_unclipped"] is True
        and binding["convention"]["native_floor_and_clamp_finance_equivalence_claimed"] is False,
        "Exact continuous reference; native errors paid by the bridge",
    )
    require(
        old["task"] == case + " original monitored arithmetic-basket knock-out call"
        and old["adaptive_quantum_stages"] == 0,
        "Exact single fixed-date original task",
    )
    route = PROGRAM / "A10_coefficient_run001" / case / "min-depth"
    target, native = (read(route / name, started) for name in ("target.json", "source.json"))
    capped = read(route / "schedule_capped.json", started)
    require(
        target["width"] == 72 and target["fraction_bits"] == 40,
        "Exact typed original native target",
    )
    same(native["outputs"], target["outputs"], "Full native target/output binding")
    require(set(target["outputs"]) == {"Y"}, "Single original discounted Y output")
    same(target["outputs"], support["target_output"], "Same already-discounted Y word")
    for field, name in (
        ("target", "target.json"),
        ("source", "source.json"),
        ("capped_schedule", "schedule_capped.json"),
    ):
        actual_path = (route / name).relative_to(ROOT).as_posix()
        expected = sha(route / name, started)
        require(
            old["source"][field] == actual_path and old["source"][field + "_sha256"] == expected,
            "E07 exact A10 source fingerprint; no unproved G1 transfer",
        )
        for row in (estimator, iqft):
            require(
                row["binding"]["hashes"][name] == expected,
                "Estimator/IQFT identical exact source hash",
            )
            require(
                resolved(row["binding"]["paths"][name], started) == route / name,
                "Same actual source path",
            )
    assets, dates, pairs, stocks, uniforms = CASES[case]
    roles = binding["cases"][case]["financial_roles"]
    require(
        roles["assets"] == assets and roles["dates"] == dates and roles["pairs"] == pairs,
        "Actual original contract source roles",
    )
    require(
        len(support["stock_ids"]) == stocks
        and support["assets"] == assets
        and support["dates"] == dates,
        "All original stock sites",
    )
    require(
        support["strict_barrier_raw"] == 140 * (1 << 40)
        and support["strike_raw"] == 100 * (1 << 40),
        "Exact integer strict barrier and strike",
    )
    require(
        support["all_original_uniform_word_patterns"] is True and support_audit["passed"] is True,
        "Universal support, not sampled maximum",
    )
    require(
        support["sampled_price_maximum_used"] is False
        and support_audit["all_actual_sum_max_average_subtract_discount_nodes_safe"] is True,
        "Universal exact output support and eager financial safety",
    )
    raw_support = support["payoff_raw_bounds"]
    require(
        type(raw_support) is list
        and len(raw_support) == 2
        and all(type(value) is int for value in raw_support),
        "Exact integer Y support",
    )
    require(
        raw_support[0] == 0 and 0 <= raw_support[1] < 1 << 46,
        "Entire full72 Y lies in unsigned46 selector support",
    )
    same(support_audit["payoff_raw_bounds"], raw_support, "Independent full-input Y support")
    same(wrapper["binding"], estimator["binding"], "Same actual financial selector binding")
    same(
        wrapper["binding_fingerprint"],
        historical_fingerprint(wrapper["binding"], started),
        "Original selector binding fingerprint",
    )
    same(
        wrapper["wrapper_fingerprint"],
        historical_fingerprint(
            {key: value for key, value in wrapper.items() if key != "wrapper_fingerprint"}, started
        ),
        "Actual wrapper metadata fingerprint",
    )
    for field, value in (
        ("target_fingerprint", target),
        ("source_fingerprint", native),
        ("capped_fingerprint", capped),
    ):
        require(
            wrapper[field] == historical_fingerprint(value, started),
            "Original actual source/target/storage fingerprint",
        )
    require(
        wrapper_audit["passed"] is True and wrapper_audit["case"] == case,
        "Independent literal native selector and reflection audit",
    )
    require(
        wrapper_audit["phase_control_zero_identity"] is True
        and wrapper_audit["controlled_reflection_relative_sign_verified"] is True,
        "Exact control-off identity and signed reflection",
    )
    for value in (wrapper, wrapper_audit):
        require(
            value["native_named_Y_copy_omitted"] is True
            and value["old_output_buffer_reused"] is True,
            "Same full72 clean source output ABI",
        )
    require(
        wrapper["format"] == "native-positive-payoff-controlled-grover-v1",
        "Original native wrapper format",
    )
    require(
        wrapper_audit["selector_bits"] == 46 and wrapper_audit["dollar_span"] == 64,
        "Independently audited strict unsigned46 selector",
    )
    require(
        wrapper["selector_native_value_register"] == list(range(72))
        and wrapper["selector_native_uniform_register"] == list(range(72, 118))
        and wrapper["selector_native_flag_wire"] == 118,
        "Full72 Y and exact uniform46 strict subtraction/sign selector ABI",
    )
    selector_mapping = wrapper["selector_mapping"]
    require(
        len(selector_mapping) == 214 and len(set(selector_mapping)) == 214,
        "Exact nonalias clean selector width",
    )
    y = target["outputs"]["Y"]
    require(
        capped["widths"][y] == 72
        and [selector_mapping[index] for index in range(72)]
        == list(range(capped["offsets"][y], capped["offsets"][y] + 72)),
        "Exact full Y wire address and width",
    )
    require(
        estimator["wrapper"] == wrapper_path.relative_to(ROOT).as_posix()
        and estimator["wrapper_sha256"] == sha(wrapper_path, started),
        "Estimator uses exact independently audited wrapper bytes",
    )
    require((64 << 40) == 1 << 46, "Exact selector normalization: no selector rounding term")
    for row in (estimator, iqft):
        value = row["binding"]
        require(
            value["word_width"] == 72
            and value["fraction_bits"] == 40
            and value["selector_bits"] == 46
            and value["dollar_span"] == 64,
            "Actual full native selector interface",
        )
        same(
            value["payoff_raw_bounds"],
            support["payoff_raw_bounds"],
            "Exact discounted support normalization",
        )
        require(
            value["certificate_sha256"]
            == sha(PROGRAM / "E03_support_run001" / (case + "_certificate.json"), started),
            "Original support hash",
        )
        require(
            value["audit_sha256"]
            == sha(PROGRAM / "E03_support_audit_run002" / (case + "_audit.json"), started),
            "Independent support hash",
        )
        require(
            row["price_output_already_discounted"] is True
            and row["second_discount_applied"] is False
            and row["normalization_span_dollars"] == 64,
            "No double discount or altered amplitude normalization",
        )
        same(row["statistical_error_dollars_exact"], [9, 2000], "Same exact statistical allowance")
    require(
        estimator["source_iterate_resources"]["original_uniform_bits"] == uniforms
        and estimator["source_iterate_resources"]["selector_uniform_bits"] == 46,
        "Original independent uniform and selector bits",
    )
    require(
        len(iqft["qpe_register_wires"]) == 16
        and iqft["serial_shots"] == 15
        and iqft["fresh_preparations"] == 15,
        "Actual synthesized estimator schedule",
    )
    schedule = read(PROGRAM / "E07_schedule_run001/schedule.json", started)
    require(
        schedule["M"] == 65536 and schedule["qpe_bits"] == 16 and schedule["repetitions"] == 15,
        "Exact original finite estimator schedule",
    )
    same(
        schedule["statistical_error_dollars_exact"],
        [9, 2000],
        "Exact source-compatible schedule dollar allowance",
    )
    total = read(BRIDGE / "complete_financial_bounds.json", started)["cases"][case][
        "continuous_to_native_dollars_upper"
    ]
    independently_approved = read(
        BRIDGE_AUDIT / "independent_complete_financial_bounds.json", started
    )["cases"][case]["verified_primary_total_upper"]
    same(total, independently_approved, "Independent130 explicitly approves exact primary total")
    same(
        total,
        reports[BRIDGE.name]["summary"]["case_dollars_upper"][case],
        "Primary total/summary reconciliation",
    )
    same(
        total,
        reports[BRIDGE_AUDIT.name]["summary"]["independently_verified_case_dollars_upper"][case],
        "Independent total/summary reconciliation",
    )
    return (
        old,
        estimator,
        iqft,
        encode(exact(total)),
        {
            "case": case,
            "exact_A10_E07_E02_IQFT_source_match": True,
            "original_full72_f40_Y_selector_bound": True,
            "strict_unsigned46_selector_original_literal_audit_admitted": True,
            "selector_normalization_exact": "64/2**46=1/2**40",
            "additional_selector_bias": [0, 1],
            "fixed_contract_monitoring_match": True,
            "G1_equivalence_transfer_needed": False,
            "source_hashes": {
                name: sha(route / name, started)
                for name in ("target.json", "source.json", "schedule_capped.json")
            },
        },
    )


def compose_case(case, old, estimator, iqft, bound, reports, started):
    """Independently reconstruct expected primary accounting from original inputs."""
    budget(started)
    require(old["schema"] == "rational-complete-price-obligations-v1", "Original ledger schema")
    require(
        old["output_includes_discount"] is True
        and old["further_discount_factor_applied"] == [1, 1],
        "Original discounted expectation",
    )
    require(
        exact(old["epsilon_dollars"]) == Fraction(1, 100)
        and exact(old["failure_cap"]) == Fraction(1, 100),
        "Original exact error and failure targets",
    )
    dollars, failures = old["dollar_terms"], old["failure_terms"]
    dollar_names = [row["name"] for row in dollars]
    expected_dollars = [
        *BIAS_NAMES,
        "monitoring_policy",
        "surrogate",
        "random_preparation",
        "statistical_digital_mean",
    ]
    require(
        dollar_names == expected_dollars and len(set(dollar_names)) == 7,
        "Every deterministic/statistical obligation appears exactly once",
    )
    by_name = {row["name"]: row for row in dollars}
    for name in BIAS_NAMES:
        require(
            by_name[name]["bound"] is None and by_name[name]["certificate"] is None,
            "Only old unfilled bias slots may be covered",
        )
    for name in ("monitoring_policy", "surrogate", "random_preparation"):
        require(exact(by_name[name]["bound"]) == 0, "Exact fixed-contract zero obligation")
        require(
            by_name[name]["certificate"]
            == "results/limitation_program_20261001/E03_support_audit_run002/summary.json",
            "Independent all-input original contract provenance",
        )
    require(
        exact(by_name["statistical_digital_mean"]["bound"]) == Fraction(9, 2000),
        "Preserved statistical dollars",
    )
    failure_names = [row["name"] for row in failures]
    require(
        failure_names
        == [
            "ideal_estimator",
            "QPE_rotation_synthesis",
            "physical_execution",
            "certificate_acquisition",
        ],
        "Exact original failure inventory",
    )
    failure_rows = {row["name"]: row for row in failures}
    require(
        exact(failure_rows["ideal_estimator"]["bound"]) == exact(iqft["ideal_failure_upper_exact"]),
        "Independent exact finite-schedule failure equality",
    )
    require(
        exact(failure_rows["QPE_rotation_synthesis"]["bound"])
        == exact(iqft["synthesis_total_observation_perturbation_upper_exact"]),
        "Independent exact synthesis observation error equality",
    )
    physical = failure_rows["physical_execution"]
    require(
        physical["bound"] is None
        and physical["certificate"] is None
        and exact(physical["allowance"]) == Fraction(3, 1000),
        "Retain unknown physical bound and allowance",
    )
    require(
        exact(failure_rows["certificate_acquisition"]["bound"]) == 0,
        "Deterministic certification acquisition",
    )
    allocated_parts, known_parts = [], []
    for row in failures:
        budget(started)
        allocated_parts.append(exact(row["allowance"]))
        if row["bound"] is not None:
            value = exact(row["bound"])
            require(
                row["certificate"] and value <= allocated_parts[-1],
                "Every certified original failure meets its unchanged allocation",
            )
            known_parts.append(value)
    allocated = sum(allocated_parts, Fraction())
    known = sum(known_parts, Fraction())
    require(
        allocated == Fraction(1, 100) and known <= allocated, "Independent exact full failure sums"
    )
    total_bias = exact(bound)
    total_dollars = total_bias + exact(by_name["statistical_digital_mean"]["bound"])
    require(
        total_bias <= Fraction(11, 2000) and total_dollars <= exact(old["epsilon_dollars"]),
        "Independent whole-bias dollar fit",
    )
    union_row = dict(
        name=COMBINED_NAME,
        bound=bound,
        covers=list(BIAS_NAMES),
        certificate=(BRIDGE / "complete_financial_bounds.json").relative_to(ROOT).as_posix(),
        independent_audit=(BRIDGE_AUDIT / "independent_complete_financial_bounds.json")
        .relative_to(ROOT)
        .as_posix(),
        primary_manifest_sha256=reports[BRIDGE.name]["manifest_sha256"],
        independent_manifest_sha256=reports[BRIDGE_AUDIT.name]["manifest_sha256"],
        pay_once=True,
    )
    expected = {key: copy.deepcopy(value) for key, value in old.items()}
    expected.update(
        schema="exact-source-original-BM-G2-composed-ledger-v1",
        dollar_terms=[union_row] + [copy.deepcopy(by_name[name]) for name in expected_dollars[3:]],
        old_unmodified_ledger="results/limitation_program_20261001/E07_complete_run001/"
        + case
        + "_complete_price_ledger.json",
        old_bias_accounting_slots_covered_once=list(BIAS_NAMES),
        all_input_error_to_original_continuous_price_certified=True,
        source_specific_mathematical_G2_bias_complete=True,
        full_price_confidence_claim=False,
        physical_execution_assumed_ideal_for_digital_certificate=True,
    )
    expected["assessment"] = dict(
        complete_price_certified=False,
        source_specific_mathematical_G2_bias_complete=True,
        known_dollar_bound_sum=encode(total_dollars),
        known_failure_bound_sum=encode(known),
        allocated_failure_sum=encode(allocated),
        ideal_logical_confidence_lower_exact=encode(Fraction(1) - known),
        open_obligations=["physical_execution"],
        missing_bounds_are_zero=False,
        physical_price_delivery_or_G3_G4_G5_claim=False,
    )
    same(expected["failure_terms"], failures, "Exact original failure rows retained without edits")
    budget(started)
    return expected


def seal(output, frozen, external, started, outcome):
    require(
        not (output / "manifest.json").exists() and not (output / "FAILED_UNSEALED.json").exists(),
        "No provisional/duplicate terminal manifest",
    )
    count = final_verify(frozen, external, started)
    outcome = dict(
        outcome,
        verification_unique_paths=count,
        budget=elapsed(started),
        limits_CPU_work_wall=[CPU, ADMISSION, WALL],
        new_test_credit=0,
        new_gate_replays=0,
        physical_price_delivery_certified=False,
        G3_G4_G5_complete=False,
        adoption=False,
        quantum_advantage=False,
    )
    save(output / "completion_outcome.json", outcome, started)
    files = owned_files(output, started)
    budget(started)
    mf = {
        "schema": "original-BM-G2-composition-" + ROLE + "-terminal-manifest-v1",
        "files": files,
        "frozen_inputs": frozen,
        "external_runtime_inputs": external,
        "manifest_self_hash_excluded": True,
        "terminal_outcome_file": "completion_outcome.json",
        "completed": outcome["completed"],
        "passed": outcome["passed"],
        "budget_censored": outcome["budget_censored"],
        "terminal_budget_observation": elapsed(started),
        "all_IO_hashing_and_output_charged": True,
        "historical_global_LIVE_mismatch_references_paths": [36, 9],
        "historical_expected_hashes_waived": False,
    }
    save(output / "manifest.json", mf, started)


def retain_failure(output, frozen, external, started, error, phase):
    if not output.exists():
        return
    try:
        require(
            not (output / "manifest.json").exists()
            and not (output / "completion_outcome.json").exists(),
            "Partial terminal data blocks reseal",
        )
        budget(started)
        save(
            output / "failure.json",
            {
                "failed": True,
                "phase": phase,
                "error_type": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(),
                "new_test_credit": 0,
                "budget": elapsed(started),
            },
            started,
        )
        seal(
            output,
            frozen,
            external,
            started,
            {
                "completed": False,
                "passed": False,
                "failed": True,
                "budget_censored": isinstance(error, BudgetCensoredError),
                "phase": phase,
            },
        )
    except BaseException:
        # Constant emergency evidence only: no rehash/scan/retry after reserve exhaustion.
        try:
            with (output / "FAILED_UNSEALED.json").open("xb") as stream:
                stream.write(
                    b'{"failed":true,"completed":false,"passed":false,"budget_censored":true,"new_test_credit":0,"partial_success_invalid":true,"requires_fresh_version_and_receipt":true}\n'
                )
        except FileExistsError:
            pass


def prepare(output):
    started = process_started()
    frozen, external, created = {}, {}, False
    try:
        setup(started)
        forbidden_imports()
        require(output == OUTPUT and not output.exists(), "Fresh exact output only")
        ready, _method = ready_policy(frozen, external, started)
        reports = prerequisites(ready, frozen, external, started)
        if ROLE == "auditor":
            producer_pin = ready.get("actual_composition_producer_manifest_SHA256")
            require(
                type(producer_pin) is str and len(producer_pin) == 64,
                "Actual passing composer pin required for auditor",
            )
            packet(SOURCE, producer_pin, frozen, external, started)
        interpreter = runtime(frozen, external, started)
        runtime_policy(interpreter, started)
        verify_loaded(frozen, external, started)
        verify(frozen, external, started)
        budget(started, admission=True)
        output.mkdir()
        created = True
        (output / "executed_code").mkdir()
        for source in (COMPOSER_AUTHOR, AUDIT_AUTHOR, METHOD, METHOD_DOC, BOOKKEEPING_ORIGIN):
            copy_exact(source, output / "executed_code" / source.name, frozen, external, started)
        copy_exact(READY, output / "root_READY_snapshot.json", frozen, external, started)
        save(output / "interpreter.json", interpreter, started)
        save(
            output / "prerequisite_admission.json",
            {
                name: {
                    key: value
                    for key, value in item.items()
                    if key not in ("manifest", "summary", "outcome")
                }
                for name, item in reports.items()
            },
            started,
        )
        verification = final_verify(frozen, external, started)
        budget(started, admission=True)
        protocol = {
            "schema": "original-BM-G2-composition-protocol-v1",
            "role": ROLE,
            "output": output.relative_to(ROOT).as_posix(),
            "frozen_inputs": frozen,
            "external_runtime_inputs": external,
            "root_READY_sha256": sha(READY, started),
            "root_READY_snapshot_sha256": sha(output / "root_READY_snapshot.json", started),
            "limits_CPU_work_wall": [CPU, ADMISSION, WALL],
            "interpreter": interpreter,
            "author_sha256": ready["author_inputs"],
            "actual_manifest_inputs": ready["manifest_inputs"],
            "actual_composition_producer_manifest_SHA256": ready.get(
                "actual_composition_producer_manifest_SHA256"
            ),
            "stdlib_only": True,
            "new_test_credit": 0,
            "preparation_sourcewalk_science_or_rational_composition_executed": False,
            "final_preparation_unique_paths": verification,
            "preparation_budget": elapsed(started),
        }
        save(output / "protocol.json", protocol, started)
        save(
            output / "PREPARED_RECEIPT.json",
            {
                "prepared": True,
                "terminal": False,
                "protocol_sha256": sha(output / "protocol.json", started),
                "budget": elapsed(started),
            },
            started,
        )
        budget(started)
        return {"prepared": True}
    except BaseException as error:
        if created:
            retain_failure(output, frozen, external, started, error, "prepare")
        raise


def run(output):
    started = process_started()
    frozen, external, admitted = {}, {}, False
    try:
        setup(started)
        forbidden_imports()
        require(output == OUTPUT and output.is_dir(), "Exact prepared output")
        no_failure(output)
        require(
            not any(
                (output / name).exists()
                for name in ("manifest.json", "run_started.json", "completion_outcome.json")
            ),
            "No reused or partial-terminal run",
        )
        admitted = True
        protocol, prepared = (
            read(output / name, started) for name in ("protocol.json", "PREPARED_RECEIPT.json")
        )
        require(
            protocol["schema"] == "original-BM-G2-composition-protocol-v1"
            and protocol["role"] == ROLE,
            "Prepared role/schema",
        )
        same(
            protocol["limits_CPU_work_wall"],
            [CPU, ADMISSION, WALL],
            "Same fixed complete run limits",
        )
        require(
            prepared["prepared"] is True
            and prepared["terminal"] is False
            and sha(output / "protocol.json", started) == prepared["protocol_sha256"],
            "Immutable actual preparation",
        )
        for mapping, external_keys in (
            (protocol["frozen_inputs"], False),
            (protocol["external_runtime_inputs"], True),
        ):
            for key, expected in mapping.items():
                budget(started)
                actual = bind(
                    frozen, external, Path(key) if external_keys else ROOT / key, expected, started
                )
                require(
                    (str(actual) if external_keys else actual.relative_to(ROOT).as_posix()) == key,
                    "Canonical prepared map key",
                )
        for name in (
            "protocol.json",
            "PREPARED_RECEIPT.json",
            "interpreter.json",
            "prerequisite_admission.json",
        ):
            bind(frozen, external, output / name, sha(output / name, started), started)
        ready, _method = ready_policy(frozen, external, started)
        require(
            sha(READY, started) == protocol["root_READY_sha256"]
            and sha(output / "root_READY_snapshot.json", started)
            == protocol["root_READY_snapshot_sha256"],
            "Immutable root release and snapshot",
        )
        same(
            ready["manifest_inputs"],
            protocol["actual_manifest_inputs"],
            "No prerequisite release mutation",
        )
        same(ready["author_inputs"], protocol["author_sha256"], "No executable/method mutation")
        reports = prerequisites(ready, frozen, external, started)
        primary = None
        if ROLE == "auditor":
            pin = protocol["actual_composition_producer_manifest_SHA256"]
            require(
                ready.get("actual_composition_producer_manifest_SHA256") == pin,
                "Same actual composer release",
            )
            primary = packet(SOURCE, pin, frozen, external, started)
            require(
                primary["summary"][
                    "eligible_source_specific_G2_pending_independent_composition_audit"
                ]
                is True,
                "Actual passing composer outcome",
            )
        interpreter = read(output / "interpreter.json", started)
        same(interpreter, protocol["interpreter"], "Actual prepared runtime record")
        runtime_policy(interpreter, started)
        verify_loaded(frozen, external, started)
        verify(frozen, external, started)
        budget(started, admission=True)
        save(
            output / "run_started.json",
            {
                "UTC": datetime.now(timezone.utc).isoformat(),
                "pid": os.getpid(),
                "limits_CPU_work_wall": [CPU, ADMISSION, WALL],
            },
            started,
        )
        case_ledgers, matches = {}, {}
        for case in CASES:
            old, estimator, iqft, bound, match = case_inputs(case, reports, started)
            result = compose_case(case, old, estimator, iqft, bound, reports, started)
            if ROLE == "auditor":
                expected_primary = copy.deepcopy(result)
                expected_primary["source_specific_mathematical_G2_bias_complete"] = False
                expected_primary["assessment"]["source_specific_mathematical_G2_bias_complete"] = (
                    False
                )
                same(
                    expected_primary,
                    read(SOURCE / (case + "_G2_composed_ledger.json"), started),
                    "Independent original-input reconstruction of the primary pending-audit ledger",
                )
            case_ledgers[case], matches[case] = result, match
            copy_exact(
                PROGRAM / "E07_complete_run001" / (case + "_complete_price_ledger.json"),
                output / (case + "_old_ledger_snapshot.json"),
                frozen,
                external,
                started,
            )
            save(output / (case + "_G2_composed_ledger.json"), result, started)
            budget(started, admission=True)
        save(output / "source_interface_matching.json", matches, started)
        coverage = {
            "combined_row": COMBINED_NAME,
            "covers": list(BIAS_NAMES),
            "each_original_obligation_paid_exactly_once": True,
            "all_deterministic_dollar_terms_covered": True,
            "physical_failure_remains_NULL": True,
            "no_A13_per_exp_allocation_created": True,
            "new_fixture_credit": 0,
            "old_controlled_residual_count_transfer": False,
        }
        save(output / "coverage.json", coverage, started)
        runtime_policy(interpreter, started)
        save(
            output / "loaded_module_origins.json", verify_loaded(frozen, external, started), started
        )
        is_audit = ROLE == "auditor"
        summary = {
            "schema": "original-BM-source-specific-G2-" + ROLE + "-summary-v1",
            "completed": True,
            "passed": True,
            "budget_censored": False,
            "rejection": False,
            "eligible_source_specific_G2_pending_independent_composition_audit": not is_audit,
            "source_specific_mathematical_G2_bias_complete": is_audit,
            "independent_composition_audit_passed": is_audit,
            "exact_source_cases_verified": list(CASES),
            "both_exact_dollar_bounds_fit": True,
            "physical_failure_remains_NULL": True,
            "complete_price_certified": False,
            "G3_G4_G5_complete": False,
            "physical_price_delivery_or_estimator_execution_certified": False,
            "new_test_credit": 0,
            "new_gate_replays": 0,
            "adoption": False,
            "cost_transfer": False,
            "quantum_advantage": False,
            "actual_bridge_manifest_sha256": reports[BRIDGE.name]["manifest_sha256"],
            "actual_bridge_audit_manifest_sha256": reports[BRIDGE_AUDIT.name]["manifest_sha256"],
            "actual_composition_producer_manifest_SHA256": None
            if primary is None
            else primary["manifest_sha256"],
            "case_dollar_totals": {
                case: value["assessment"]["known_dollar_bound_sum"]
                for case, value in case_ledgers.items()
            },
            "budget": elapsed(started),
        }
        save(output / "summary.json", summary, started)
        seal(
            output,
            frozen,
            external,
            started,
            {
                "completed": True,
                "passed": True,
                "budget_censored": False,
                "phase": "run",
                "summary_file": "summary.json",
                "source_specific_mathematical_G2_bias_complete": is_audit,
                "independent_composition_audit_passed": is_audit,
            },
        )
        return summary
    except BaseException as error:
        if admitted:
            retain_failure(output, frozen, external, started, error, "run")
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "run"))
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    require(output == OUTPUT, "Only the exact new receipt")
    value = prepare(output) if args.operation == "prepare" else run(output)
    print(
        json.dumps(
            {
                "role": ROLE,
                "operation": args.operation,
                "prepared": value.get("prepared"),
                "passed": value.get("passed"),
                "new_test_credit": 0,
            }
        )
    )


if __name__ == "__main__":
    main()
