"""Independent130 fixed-alpha A13 allocation audit; no producer/helper imports.

Fresh scalar interval recomputation uses admitted original metadata only.
No source walker, fit, gate array, fixture or estimator is evaluated.
"""

from __future__ import annotations

import argparse
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
COMPOSER_AUTHOR = RESEARCH / "experiment_exp_frontier_allocation.py"
AUDIT_AUTHOR = RESEARCH / "audit_exp_frontier_allocation.py"
METHOD = RESEARCH / "a13_fixed_relative_envelope_allocation_preflight.json"
METHOD_DOC = RESEARCH / "A13_FIXED_RELATIVE_ENVELOPE_ALLOCATION_PREFLIGHT.md"
IMPLEMENTATION = RESEARCH / "exp_frontier_allocation_implementation_preflight.json"
IMPLEMENTATION_DOC = RESEARCH / "EXP_FRONTIER_ALLOCATION_IMPLEMENTATION_PREFLIGHT.md"
READY = PROGRAM / "A13_fixed_alpha_allocation_AUDIT_READY_run001.json"
SOURCE = PROGRAM / "A13_fixed_alpha_allocation_run001"
BRIDGE = PROGRAM / "A02_BM_native_financial_bridge_run002"
BRIDGE_AUDIT = PROGRAM / "A02_BM_native_financial_bridge_audit_run002"
FAILED_BRIDGE = PROGRAM / "A02_BM_native_financial_bridge_run001"
FAILED_BRIDGE_SHA = "8beb20bfe88407479953ddd7be284fd8fe94cea1e964c392340c4ab1a2376e02"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
BOOKKEEPING_ORIGIN = RESEARCH / "compose_original_bm_g2_ledger.py"
BOOKKEEPING_ORIGIN_SHA = "7519bc1ca03459531255a2563653b00d39b2dec0bfccadcfd3267210be571d1a"
CPU, ADMISSION, WALL, DIGITS = 180, 150, 600, 130
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
Q, N = 1 << 40, 1 << 32
ALPHA, EPSILON, ALLOWANCE = Fraction(1, 1 << 24), Fraction(1, Q), Fraction(11, 2000)
CASES = {"B4x12": (4, 12, 30, 48), "B8x52": (8, 52, 234, 416)}
_PATHS, _HASHES, _OBSERVED = {}, {}, {}
_EXTERNAL_TREES, _EXTERNAL_FILES = (), ()
_EXTERNAL_ROOT, _EXCLUDED_RUNTIME, _PROCESS_CREATION_TICKS = None, (), None
_REFERENCE_COUNT, _HASH_WORK, _UNIQUE_BYTES = 0, 0, 0
_UNIQUE_INPUTS = set()
_KERNEL_ADMITTED = False
ROLE, AUTHOR = "auditor", AUDIT_AUTHOR
OUTPUT = PROGRAM / "A13_fixed_alpha_allocation_audit_run001"
PRODUCER, AUDITOR = AUTHOR, COMPOSER_AUTHOR


class BudgetCensoredError(RuntimeError):
    """One fixed all-inclusive process budget; no scientific retry."""


def forbidden_imports():
    permitted = {__name__, "research.limitation_program_20261001"}
    forbidden = [
        name
        for name in sys.modules
        if name.split(".", 1)[0]
        in {"numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
        or (name.split(".", 1)[0] == "mpmath" and not _KERNEL_ADMITTED)
        or (name.startswith("research.") and name not in permitted)
    ]
    require(
        not forbidden,
        "No producer/helper/source walker/optional backend imports: " + repr(forbidden),
    )


def require(condition, message):
    if not condition:
        raise ValueError(message)


def budget(started, admission=False):
    process_cpu = time.process_time() - started[0]
    wall = time.monotonic() - started[1]
    if process_cpu >= (ADMISSION if admission else CPU) or wall >= WALL:
        raise BudgetCensoredError("Fixed allocation 180CPU/150work/600wall limit")
    return process_cpu, wall


def charge_hash(amount, started):
    global _HASH_WORK
    budget(started)
    _HASH_WORK += amount
    require(_HASH_WORK <= MAX_HASH_WORK, "Prospective 24GiB complete actual-byte hash-work limit")


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


def packet(
    receipt,
    expected_manifest,
    frozen,
    external,
    started,
    preserve_failed=False,
    allow_rejection=False,
):
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
            summary.get("failed", False) is False
            and (
                summary.get("rejection", False) is False or (allow_rejection and receipt == SOURCE)
            ),
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
                    and (
                        value.get("rejection", False) is False
                        or (allow_rejection and receipt == SOURCE)
                    ),
                    "Uncensored successful terminal",
                )
        limit = (
            [180, 600]
            if receipt
            in (
                SOURCE,
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


def rational(value):
    require(type(value) is list and len(value) == 2, "Exact rational pair")
    require(all(type(part) is int for part in value) and value[1] > 0, "No float/bool rational")
    return Fraction(*value)


def outward(mp, value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def endpoints(value):
    result = [
        Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent
        for sign, mantissa, exponent, _ in value._mpi_
    ]
    require(len(result) == 2 and result[0] <= result[1], "Finite outward interval")
    return tuple(result)


def lower(value):
    return endpoints(value)[0]


def upper(value):
    return endpoints(value)[1]


def ready_policy(frozen, external, started):
    ready = read(READY, started)
    require(
        ready["schema"] == "a13-fixed-alpha-allocation-root-READY-v1" and ready["ready"] is True,
        "Actual immutable root READY",
    )
    same(ready["limits_CPU_work_wall"], [CPU, ADMISSION, WALL], "Fixed allocation process limits")
    same(ready["interval_digits_primary_independent"], [90, 130], "Fixed outward precisions")
    require(
        ready["threads"] == 1 and ready["alpha"] == encode(ALPHA),
        "One thread and ONE preregistered alpha",
    )
    paths = (COMPOSER_AUTHOR, AUDIT_AUTHOR, METHOD, METHOD_DOC, IMPLEMENTATION, IMPLEMENTATION_DOC)
    require(
        set(ready["author_inputs"]) == {path.relative_to(ROOT).as_posix() for path in paths},
        "Exact six author/method/implementation pins",
    )
    for key, expected in ready["author_inputs"].items():
        bind(frozen, external, ROOT / key, expected, started)
    bind(frozen, external, READY, sha(READY, started), started)
    bind(frozen, external, LAUNCHER, ready["interpreter_sha256"], started)
    bind(frozen, external, BOOKKEEPING_ORIGIN, BOOKKEEPING_ORIGIN_SHA, started)
    method, implementation = read(METHOD, started), read(IMPLEMENTATION, started)
    require(
        method["schema"] == "a13-fixed-relative-stock-envelope-allocation-paper-preflight-v1"
        and implementation["schema"] == "a13-fixed-alpha-allocation-implementation-preflight-v1",
        "Exact prospective contracts",
    )
    same(method["single_fixed_alpha"], encode(ALPHA), "No alpha search")
    same(
        [
            method["prospective_execution"][key]
            for key in ("CPU_seconds", "work_admission_CPU_seconds", "wall_seconds")
        ],
        [CPU, ADMISSION, WALL],
        "Method process limits",
    )
    same(
        method["actual_prerequisite_manifest_pins"],
        ready["manifest_inputs"],
        "No actual expected SHA override",
    )
    for key, expected in method["held_method_pins"].items():
        bind(frozen, external, ROOT / key, expected, started)
    for key, expected in implementation["required_method_SHA256"].items():
        bind(frozen, external, ROOT / key, expected, started)
    for key, expected in implementation["actual_author_SHA256"].items():
        require(
            expected is not None and ready["author_inputs"][key] == expected,
            "Frozen actual executable pins required",
        )
    for role, module, receipt in (
        (
            "producer",
            "research.limitation_program_20261001.experiment_exp_frontier_allocation",
            SOURCE,
        ),
        (
            "auditor",
            "research.limitation_program_20261001.audit_exp_frontier_allocation",
            PROGRAM / "A13_fixed_alpha_allocation_audit_run001",
        ),
    ):
        for operation in ("prepare", "run"):
            same(
                ready["commands"][role + "_" + operation],
                [str(LAUNCHER), "-B", "-m", module, operation, "--output", str(receipt)],
                "Exact pinned CLI ordering",
            )
    return ready


def prerequisites(ready, frozen, external, started):
    reports = {}
    for key, pin in ready["manifest_inputs"].items():
        receipt = (ROOT / key).parent
        reports[receipt.name] = packet(
            receipt, pin, frozen, external, started, preserve_failed=receipt == FAILED_BRIDGE
        )
    source, audit = reports[BRIDGE.name], reports[BRIDGE_AUDIT.name]
    for item in (source, audit):
        value = item["summary"]
        require(
            value["native_financial_bias_certificate_valid"] is True
            and value["financial_residual_fit"] is True
            and value["new_test_credit"] == value["new_gate_replays"] == 0,
            "Actual native bridge proof/residual fit, zero recredit",
        )
        same(
            value["actual_joint_pair_counts"],
            {"B4x12": 30, "B8x52": 234},
            "Original whole pair laws",
        )
        require(
            value["actual_stock_sites"] == 464
            and value["all_actual_native_emitted_dead_paths_product144_and_stored72_safe"] is True,
            "Complete original native safety",
        )
    require(
        audit["summary"]["independent_audit_passed"] is True
        and audit["summary"]["complete_primary_bound_authorized_by_independent130"] is True
        and audit["summary"]["source_manifest_sha256"] == source["manifest_sha256"],
        "Exact actual independently approved original premise",
    )
    root = reports["A02_BM_native_financial_bridge_root_verification_run001"]["summary"]
    require(
        root["passed"] is True
        and root["SHA_mismatches"] == 0
        and root["scientific_kernels_executed"] is False
        and root["new_fixture_credit"] == 0,
        "Actual complete root integrity premise",
    )
    inputs = {
        name: read(BRIDGE / name, started)
        for name in (
            "native_source_binding.json",
            "raw_log_prefix_envelopes.json",
            "stock_exponential_envelopes.json",
            "smooth_payoff_bounds.json",
            "closed_barrier_bands.json",
            "complete_financial_bounds.json",
        )
    }
    same(
        inputs["native_source_binding.json"],
        read(BRIDGE_AUDIT / "independent_native_source_binding.json", started),
        "Independently bound original source roles",
    )
    inputs["independent_stock_domains"] = read(
        BRIDGE_AUDIT / "independent130_stock_exponential_envelopes.json", started
    )
    approved = read(BRIDGE_AUDIT / "independent_complete_financial_bounds.json", started)
    for case, (assets, dates, pairs, stocks) in CASES.items():
        binding = inputs["native_source_binding.json"]["cases"][case]["financial_roles"]
        require(
            [binding["assets"], binding["dates"], binding["pairs"]] == [assets, dates, pairs],
            "Exact original fixed contract roles",
        )
        stock = inputs["stock_exponential_envelopes.json"]["cases"][case]
        require(
            stock["actual_stock_sites"] == stocks and len(stock["actual_sites"]) == stocks,
            "All actual stock source witnesses",
        )
        for site_row in stock["actual_sites"]:
            require(
                [site_row[key] for key in ("low", "high", "inverse_ln2", "ln2")]
                == [-12193974156573, 9145480617430, 1586259972792, 762123384786],
                "Original source-bound clamp/reduction words",
            )
        own = inputs["independent_stock_domains"][case]
        same(
            own["clamp_raw_bounds"],
            [stock["lower_clamp_raw"], stock["upper_clamp_raw"]],
            "Independent exact clamp domain",
        )
        require(
            [row["k"] for row in stock["classes"]] == list(range(-17, 13))
            and len(own["classes"]) == 30,
            "All30 declared classes retained",
        )
        for row, other in zip(stock["classes"], own["classes"], strict=True):
            require(
                row["k"] == other["k"] and row["empty"] is other["empty"],
                "Independent class occupancy",
            )
            if not row["empty"]:
                same(
                    row["remainder_raw_bounds"],
                    other["remainder_raw_bounds"],
                    "Actual independent raw remainder domain",
                )
                same(
                    row["clipped_log_raw_bounds"],
                    other["clipped_raw_bounds"],
                    "Actual independent integer input class",
                )
        prefixes = inputs["raw_log_prefix_envelopes.json"]["cases"][case]["prefixes"]
        bands = inputs["closed_barrier_bands.json"]["cases"][case]["dates"]
        require(len(prefixes) == len(bands) == dates, "All source date prefixes retained")
        for j, (prefix, band) in enumerate(zip(prefixes, bands, strict=True), start=1):
            require(
                prefix["date"] == band["date"] == j - 1
                and prefix["elapsed_dates"] == band["elapsed_dates"] == j,
                "Exact date roles",
            )
            same(prefix["lambda_upper"], band["lambda_upper"], "Unchanged accepted actual lambda")
        total = inputs["complete_financial_bounds.json"]["cases"][case]
        same(
            total["continuous_to_native_dollars_upper"],
            approved["cases"][case]["verified_primary_total_upper"],
            "Actual total independently approved",
        )
        same(
            total["pinned_primary_squared_radius_KS_upper"],
            inputs["closed_barrier_bands.json"]["pinned_squared_radius_KS_upper"],
            "Same accepted D_S",
        )
    return reports, inputs


def fixed_financial_test(mp, inputs, started):
    """Independent130 reconstruction from immutable accepted premise metadata."""
    cases = {}
    d_exact_bounds = endpoints(mp.iv.exp(outward(mp, -Fraction(3, 100))))
    for case in reversed(tuple(CASES)):
        na, nt, pair_total, _ = CASES[case]
        source_stock = inputs["stock_exponential_envelopes.json"]["cases"][case]
        source_smooth = inputs["smooth_payoff_bounds.json"]["cases"][case]
        source_total = inputs["complete_financial_bounds.json"]["cases"][case]
        average_word, discount_word = (
            source_smooth["actual_average_literal"],
            source_smooth["actual_discount_literal"],
        )
        require(
            type(average_word) is int
            and type(discount_word) is int
            and 0 < average_word < 1 << 71
            and 0 < discount_word < 1 << 71,
            "Independent actual positive signed72 finance literals",
        )
        one_date_limit = na * 140 * Q - 1
        all_stock_limit = one_date_limit * nt
        native_mean_limit = (average_word * all_stock_limit) // Q
        native_call_limit = max(0, native_mean_limit - 100 * Q)
        native_payoff_limit = (discount_word * native_call_limit) // Q
        cap_proof = {
            "date_raw_stock_sum_upper": one_date_limit,
            "total_raw_stock_sum_upper": all_stock_limit,
            "actual_average_literal": average_word,
            "actual_discount_literal": discount_word,
            "average_raw_upper": native_mean_limit,
            "positive_call_raw_upper": native_call_limit,
            "discounted_payoff_raw_upper": native_payoff_limit,
            "strict_below_40Q": 0 <= native_payoff_limit < 40 * Q,
            "original_stock_maximum_used": False,
        }
        L, U = (Fraction(source_stock[name], Q) for name in ("lower_clamp_raw", "upper_clamp_raw"))
        leakage = upper(mp.iv.exp(outward(mp, L)) * outward(mp, Fraction(1) + ALPHA)) + EPSILON
        native_top = lower(mp.iv.exp(outward(mp, U)) * outward(mp, Fraction(1) - ALPHA)) - EPSILON
        native_bottom = (
            lower(mp.iv.exp(outward(mp, L)) * outward(mp, Fraction(1) - ALPHA)) - EPSILON
        )
        guard_rows = {
            "ell_below_barrier": 0 <= leakage < 140,
            "prospective_native_upper_clip_knockout": native_top >= 140 * na,
            "prospective_native_stock_nonnegative": native_bottom >= 0,
            "conditional_native_cap40": cap_proof["strict_below_40Q"],
        }
        DS = exact(source_total["pinned_primary_squared_radius_KS_upper"])
        H_price = exact(source_total["pinned_primary_hybrid_price_upper"])
        smooth_sum, probability_sum, rows, valid_dates = Fraction(), Fraction(), [], 0
        for source_date in inputs["raw_log_prefix_envelopes.json"]["cases"][case]["prefixes"]:
            budget(started, admission=True)
            j = source_date["elapsed_dates"]
            lam = exact(source_date["lambda_upper"])
            a = lower(mp.iv.exp(outward(mp, -lam)) * outward(mp, 1 - ALPHA))
            b = upper(mp.iv.exp(outward(mp, lam)) * outward(mp, 1 + ALPHA))
            ideal_top = lower(mp.iv.exp(outward(mp, U - lam)))
            valid = 0 < a <= 1 <= b and ideal_top > 140 * na
            guard_rows["date_" + str(j) + "_multiplicative_and_ideal_clip"] = valid
            row = {
                "date": j - 1,
                "elapsed_dates": j,
                "lambda_upper": encode(lam),
                "a_lower": encode(a),
                "b_upper": encode(b),
                "ideal_upper_clip_stock_lower": encode(ideal_top),
                "guard_passed": valid,
            }
            if valid and guard_rows["ell_below_barrier"]:
                lo = Fraction(140 - leakage, b)
                hi = Fraction(140 + 2 * EPSILON, a)
                require(0 < lo <= hi, "Independent ordered CLOSED original basket band")
                common_variance = Fraction(9 * j, 250 * nt)
                density_bound = mp.iv.log(outward(mp, hi) / outward(mp, lo)) / mp.iv.sqrt(
                    outward(mp, common_variance) * 2 * mp.iv.pi
                )
                p_G = min(Fraction(1), upper(density_bound))
                pair_count = ((na + 1) * j + 1) // 2
                require(1 <= pair_count <= pair_total, "Independent whole-pair count")
                transport = pair_count * (Fraction(2, N) + 4 * DS)
                hybrid_band = min(Fraction(1), p_G + transport)
                mean_error = max(EPSILON, leakage) + 140 * max(b - 1, 1 - a)
                smooth_sum += mean_error
                probability_sum += hybrid_band
                valid_dates += 1
                row.update(
                    closed_band_lower=encode(lo),
                    closed_band_upper=encode(hi),
                    exact_common_variance=encode(common_variance),
                    continuous_Gaussian_closed_band_upper=encode(p_G),
                    relevant_whole_pairs=pair_count,
                    band_pair_law_allowance=encode(transport),
                    hybrid_closed_band_upper=encode(hybrid_band),
                    date_unrounded_mean_error_upper=encode(mean_error),
                )
            rows.append(row)
        eligible_guards = all(guard_rows.values())
        result = {
            "alpha": encode(ALPHA),
            "beta": encode(EPSILON),
            "decoded_clamps": [encode(L), encode(U)],
            "ell_upper": encode(leakage),
            "native_upper_clip_stock_lower": encode(native_top),
            "native_stock_lower": encode(native_bottom),
            "conditional_native_cap_proof": cap_proof,
            "guards": guard_rows,
            "all_guards_passed": eligible_guards,
            "dates": rows,
            "accepted_H_price_upper": encode(H_price),
            "accepted_D_S_upper": encode(DS),
            "financial_F_upper": None,
            "financial_residual_fit": False,
        }
        if eligible_guards:
            require(valid_dates == nt, "All independent date terms covered")
            c_A, d_native = (
                Fraction(source_smooth[name], Q)
                for name in ("actual_average_literal", "actual_discount_literal")
            )
            average_delta = abs(c_A - Fraction(1, na * nt))
            A = smooth_sum / nt + EPSILON + 140 * na * nt * average_delta
            discount_delta = max(abs(d_native - d_endpoint) for d_endpoint in d_exact_bounds)
            zeta = EPSILON + d_native * A + 40 * discount_delta
            switch = min(Fraction(1), probability_sum)
            financial_bound = H_price + 40 * switch + zeta
            result.update(
                actual_average_literal=source_smooth["actual_average_literal"],
                actual_discount_literal=source_smooth["actual_discount_literal"],
                average_literal_error=encode(average_delta),
                average_error_upper=encode(A),
                discount_literal_error_upper=encode(discount_delta),
                smooth_discounted_error_upper=encode(zeta),
                hybrid_any_switch_upper=encode(switch),
                financial_F_upper=encode(financial_bound),
                financial_residual_fit=financial_bound <= ALLOWANCE,
                original_stock_alpha_or_old_grid_error_readded=False,
                conditional_candidate_native_cap=encode(40),
            )
        cases[case] = result
    return {
        "schema": "a13-one-fixed-alpha-financial-test-v1",
        "interval_digits": DIGITS,
        "alpha": encode(ALPHA),
        "cases": cases,
        "both_financial_residuals_fit": all(
            value["financial_residual_fit"] for value in cases.values()
        ),
        "candidate_fresh_support_and_native_safety_still_required": True,
        "new_fixture_credit": 0,
    }


def polynomial_allowance(mp, inputs, started):
    """Independent downward class allowance from prior independently bound domains."""
    ln2_bounds = endpoints(mp.iv.log(outward(mp, Fraction(2))))
    stored_ln2 = Fraction(762123384786, Q)
    mismatch = max(abs(endpoint - stored_ln2) for endpoint in ln2_bounds)
    case_rows, constraints = {}, []
    for case in reversed(tuple(CASES)):
        own_classes = inputs["independent_stock_domains"][case]["classes"]
        primary_domains = inputs["stock_exponential_envelopes.json"]["cases"][case]["classes"]
        rows = []
        for own, original in zip(own_classes, primary_domains, strict=True):
            budget(started, admission=True)
            k = own["k"]
            require(type(k) is int and -17 <= k <= 12, "Independent fixed exponent index")
            row = {
                "k": k,
                "empty": own["empty"],
                "clipped_log_raw_bounds": original["clipped_log_raw_bounds"],
            }
            if own["empty"]:
                require(
                    original["clipped_log_raw_bounds"][1] < original["clipped_log_raw_bounds"][0],
                    "Independent retained empty class",
                )
                row.update(positive_allowance_required=False, E_k_enclosure=None)
            else:
                source_remainder = own["remainder_raw_bounds"]
                r_min = Fraction(source_remainder[0], Q)
                a_bounds = endpoints(mp.iv.exp(outward(mp, abs(k) * mismatch)))
                threshold_bracket = (
                    outward(mp, 1 + ALPHA) * mp.iv.exp(outward(mp, -mismatch * abs(k))) - 1
                )
                threshold = endpoints(threshold_bracket * mp.iv.exp(outward(mp, r_min)))
                positive = (
                    lower(threshold_bracket) > 0 and threshold[0] > 0 and a_bounds[1] < 1 + ALPHA
                )
                row.update(
                    remainder_raw_bounds=source_remainder,
                    r_min_exact=encode(r_min),
                    bracket_enclosure=[encode(value) for value in endpoints(threshold_bracket)],
                    E_k_enclosure=[encode(value) for value in threshold],
                    a_enclosure=[encode(value) for value in a_bounds],
                    positive_allowance_required=True,
                    strict_positive_allowance_passed=positive,
                    same_upper_and_lower_relative_budget_paid=True,
                )
                if positive:
                    constraints.append(threshold[0])
            rows.append(row)
        case_rows[case] = rows
    strict = all(
        row.get("strict_positive_allowance_passed", True)
        for rows in case_rows.values()
        for row in rows
    )
    require(
        all(any(not row["empty"] for row in rows) for rows in case_rows.values()),
        "Both independent source domains nonempty",
    )
    return {
        "schema": "a13-fixed-alpha-native-poly-allowance-v1",
        "interval_digits": DIGITS,
        "alpha": encode(ALPHA),
        "ln2_literal": [762123384786, Q],
        "ln2_enclosure": [encode(value) for value in ln2_bounds],
        "delta_ln2_upper": encode(mismatch),
        "cases": case_rows,
        "all_nonempty_allowances_strict_positive": strict,
        "E_allow_lower": encode(min(constraints)) if strict else None,
        "allowance_is_outward_lower_not_polynomial_error_upper": True,
        "candidate_quantization_all_internal_floors_and_full_realization_must_fit": True,
        "final_shift_floor_paid_separately": encode(EPSILON),
    }


def authorize_primary(mp, primary_finance, primary_scalar, own_finance, own_scalar, started):
    require(
        primary_finance["interval_digits"] == primary_scalar["interval_digits"] == 90,
        "Actual frozen primary precision",
    )
    same(primary_finance["alpha"], encode(ALPHA), "Primary fixed alpha")
    same(primary_scalar["alpha"], encode(ALPHA), "Primary fixed-alpha scalar release")
    require(
        exact(primary_scalar["delta_ln2_upper"]) >= exact(own_scalar["delta_ln2_upper"]),
        "Primary ln2 error independently encloses exact mismatch",
    )
    ln2_primary = [rational(value) for value in primary_scalar["ln2_enclosure"]]
    ln2_own = [rational(value) for value in own_scalar["ln2_enclosure"]]
    require(
        ln2_primary[0] <= ln2_own[0] <= ln2_own[1] <= ln2_primary[1],
        "Independent130 verifies entire primary logarithm interval",
    )
    same(primary_scalar["ln2_literal"], [762123384786, Q], "Actual immutable ln2 word")
    source_delta = exact(primary_scalar["delta_ln2_upper"])
    require(
        source_delta == max(abs(Fraction(762123384786, Q) - value) for value in ln2_primary),
        "Primary mismatch computed from its actual outward enclosure",
    )
    for case in CASES:
        budget(started)
        source, own = primary_finance["cases"][case], own_finance["cases"][case]
        require(
            exact(source["ell_upper"]) >= exact(own["ell_upper"])
            and rational(source["native_upper_clip_stock_lower"])
            <= rational(own["native_upper_clip_stock_lower"])
            and rational(source["native_stock_lower"]) <= rational(own["native_stock_lower"]),
            "Independent primary leakage/native endpoint enclosures",
        )
        assets, dates, _pairs, _stocks = CASES[case]
        source_ell = exact(source["ell_upper"])
        same(
            source["conditional_native_cap_proof"],
            own["conditional_native_cap_proof"],
            "Independent exact strict-survival/native-floor cap proof with actual literals",
        )
        guard_conditions = {
            "ell_below_barrier": 0 <= source_ell < 140,
            "prospective_native_upper_clip_knockout": rational(
                source["native_upper_clip_stock_lower"]
            )
            >= 140 * assets,
            "prospective_native_stock_nonnegative": rational(source["native_stock_lower"]) >= 0,
            "conditional_native_cap40": own["conditional_native_cap_proof"]["strict_below_40Q"],
        }
        same(
            source["accepted_H_price_upper"],
            own["accepted_H_price_upper"],
            "Same unchanged polar price premise",
        )
        same(
            source["accepted_D_S_upper"],
            own["accepted_D_S_upper"],
            "Same unchanged radial-law premise",
        )
        require(len(source["dates"]) == len(own["dates"]), "Complete primary date inventory")
        for source_date, own_date in zip(source["dates"], own["dates"], strict=True):
            same(
                [source_date["date"], source_date["elapsed_dates"], source_date["lambda_upper"]],
                [own_date["date"], own_date["elapsed_dates"], own_date["lambda_upper"]],
                "Exact original date/lambda roles",
            )
            a, b = rational(source_date["a_lower"]), rational(source_date["b_upper"])
            ideal_upper = rational(source_date["ideal_upper_clip_stock_lower"])
            require(
                a <= rational(own_date["a_lower"])
                and b >= rational(own_date["b_upper"])
                and ideal_upper <= rational(own_date["ideal_upper_clip_stock_lower"]),
                "Independent primary date multiplicative/upper-clamp enclosures",
            )
            valid = 0 < a <= 1 <= b and ideal_upper > assets * 140
            require(source_date["guard_passed"] is valid, "Exact primary date guard decision")
            guard_conditions[
                "date_" + str(source_date["elapsed_dates"]) + "_multiplicative_and_ideal_clip"
            ] = valid
            if valid and guard_conditions["ell_below_barrier"]:
                lo, hi = (140 - source_ell) / b, (140 + 2 * EPSILON) / a
                same(
                    [source_date["closed_band_lower"], source_date["closed_band_upper"]],
                    [encode(lo), encode(hi)],
                    "Primary exact closed band from its approved enclosures",
                )
                j = source_date["elapsed_dates"]
                variance = Fraction(9 * j, 250 * dates)
                checked_G = min(
                    Fraction(1),
                    upper(
                        mp.iv.log(outward(mp, hi / lo))
                        / mp.iv.sqrt(2 * mp.iv.pi * outward(mp, variance))
                    ),
                )
                p_G = exact(source_date["continuous_Gaussian_closed_band_upper"])
                require(
                    checked_G <= p_G <= 1,
                    "Independent130 verifies primary band's own Gaussian upper",
                )
                count = ((assets + 1) * j + 1) // 2
                law = count * (4 * exact(source["accepted_D_S_upper"]) + Fraction(2, N))
                same(
                    source_date["exact_common_variance"],
                    encode(variance),
                    "Exact original continuous variance",
                )
                require(
                    source_date["relevant_whole_pairs"] == count, "Complete original whole blocks"
                )
                same(
                    source_date["band_pair_law_allowance"],
                    encode(law),
                    "Exact unchanged band-law allowance",
                )
                same(
                    source_date["hybrid_closed_band_upper"],
                    encode(min(Fraction(1), p_G + law)),
                    "Exact source hybrid band sum",
                )
                same(
                    source_date["date_unrounded_mean_error_upper"],
                    encode(140 * max(1 - a, b - 1) + max(EPSILON, source_ell)),
                    "Exact source date smooth envelope",
                )
        same(source["guards"], guard_conditions, "Every exact source guard from approved endpoints")
        require(
            source["all_guards_passed"] is all(guard_conditions.values()),
            "Complete primary guard predicate",
        )
        if source["all_guards_passed"]:
            require(
                exact(source["financial_F_upper"]) >= exact(own["financial_F_upper"]),
                "Independent130 authorizes entire primary90 financial upper",
            )
            require(
                source["financial_residual_fit"]
                is (exact(source["financial_F_upper"]) <= ALLOWANCE),
                "Exact primary residual decision",
            )
            for field in (
                "actual_average_literal",
                "actual_discount_literal",
                "average_literal_error",
            ):
                same(source[field], own[field], "Original unchanged actual smooth literal")
            average_error = (
                sum(
                    (exact(row["date_unrounded_mean_error_upper"]) for row in source["dates"]),
                    Fraction(),
                )
                / dates
                + 140 * assets * dates * exact(source["average_literal_error"])
                + EPSILON
            )
            same(
                source["average_error_upper"],
                encode(average_error),
                "Complete source average floor/coefficient accounting",
            )
            source_discount_error = exact(source["discount_literal_error_upper"])
            require(
                source_discount_error >= exact(own["discount_literal_error_upper"]),
                "Independent source discount interval error",
            )
            zeta = (
                Fraction(source["actual_discount_literal"], Q) * average_error
                + 40 * source_discount_error
                + EPSILON
            )
            switch = min(
                Fraction(1),
                sum(
                    (exact(row["hybrid_closed_band_upper"]) for row in source["dates"]), Fraction()
                ),
            )
            same(
                source["smooth_discounted_error_upper"],
                encode(zeta),
                "Exact source discounted smooth ledger",
            )
            same(
                source["hybrid_any_switch_upper"],
                encode(switch),
                "Exact complete source switch union",
            )
            same(
                source["financial_F_upper"],
                encode(exact(source["accepted_H_price_upper"]) + zeta + 40 * switch),
                "Primary complete pay-once financial formula",
            )
        else:
            require(
                source["financial_F_upper"] is None and source["financial_residual_fit"] is False,
                "Rejected guard cannot supply a financial value",
            )
        primary_rows, own_rows = primary_scalar["cases"][case], own_scalar["cases"][case]
        require(len(primary_rows) == len(own_rows) == 30, "Both complete30 scalar class rows")
        for source_class, own_class in zip(primary_rows, own_rows, strict=True):
            same(
                [source_class["k"], source_class["empty"], source_class["clipped_log_raw_bounds"]],
                [own_class["k"], own_class["empty"], own_class["clipped_log_raw_bounds"]],
                "Exact independent class identities",
            )
            if not source_class["empty"]:
                same(
                    source_class["remainder_raw_bounds"],
                    own_class["remainder_raw_bounds"],
                    "Exact independently bound native remainder",
                )
                minimum = rational(source_class["r_min_exact"])
                require(
                    minimum == Fraction(own_class["remainder_raw_bounds"][0], Q),
                    "Exact source class lower remainder",
                )
                checked_bracket = endpoints(
                    outward(mp, 1 + ALPHA)
                    * mp.iv.exp(outward(mp, -abs(source_class["k"]) * source_delta))
                    - 1
                )
                source_bracket = [rational(value) for value in source_class["bracket_enclosure"]]
                require(
                    source_bracket[0]
                    <= checked_bracket[0]
                    <= checked_bracket[1]
                    <= source_bracket[1],
                    "Independent primary bracket interval at its own delta",
                )
                checked_E = endpoints(
                    mp.iv.exp(outward(mp, minimum))
                    * (
                        outward(mp, 1 + ALPHA)
                        * mp.iv.exp(outward(mp, -abs(source_class["k"]) * source_delta))
                        - 1
                    )
                )
                source_E = [rational(value) for value in source_class["E_k_enclosure"]]
                require(
                    source_E[0] <= checked_E[0] <= checked_E[1] <= source_E[1],
                    "Independent complete primary class threshold interval",
                )
                checked_a = endpoints(mp.iv.exp(outward(mp, abs(source_class["k"]) * source_delta)))
                source_a = [rational(value) for value in source_class["a_enclosure"]]
                require(
                    source_a[0] <= checked_a[0] <= checked_a[1] <= source_a[1],
                    "Independent source lower-relative proof exponential interval",
                )
                require(
                    source_class["strict_positive_allowance_passed"]
                    is (source_bracket[0] > 0 and source_E[0] > 0 and source_a[1] < 1 + ALPHA),
                    "Exact source class strict positivity predicate",
                )
                if source_class["strict_positive_allowance_passed"]:
                    require(
                        rational(source_class["E_k_enclosure"][0])
                        <= rational(own_class["E_k_enclosure"][0]),
                        "Independent130 verifies primary per-class downward allowance",
                    )
    expected_positive = all(
        row.get("strict_positive_allowance_passed", True)
        for rows in primary_scalar["cases"].values()
        for row in rows
    )
    require(
        primary_scalar["all_nonempty_allowances_strict_positive"] is expected_positive,
        "Exact complete source class positivity predicate",
    )
    if primary_scalar["all_nonempty_allowances_strict_positive"]:
        require(
            0 < exact(primary_scalar["E_allow_lower"]) <= exact(own_scalar["E_allow_lower"]),
            "Independent130 approves entire primary common downward release",
        )
        primary_class_minimum = min(
            exact(row["E_k_enclosure"][0])
            for rows in primary_scalar["cases"].values()
            for row in rows
            if not row["empty"]
        )
        require(
            exact(primary_scalar["E_allow_lower"]) == primary_class_minimum,
            "Actual full union primary minimum",
        )
    else:
        require(primary_scalar["E_allow_lower"] is None, "Rejected class cannot provide a release")
    fit = all(row["financial_residual_fit"] for row in primary_finance["cases"].values())
    require(
        primary_finance["both_financial_residuals_fit"] is fit, "Primary both-case fit predicate"
    )
    return fit and primary_scalar["all_nonempty_allowances_strict_positive"]


def seal(output, frozen, external, started, outcome):
    require(
        not (output / "manifest.json").exists(), "No provisional or overwritten terminal manifest"
    )
    fresh_count = final_verify(frozen, external, started)
    outcome = dict(
        outcome,
        budget=elapsed(started),
        limits_CPU_work_wall=[CPU, ADMISSION, WALL],
        interval_digits=DIGITS,
        verification_unique_paths=fresh_count,
        new_test_credit=0,
        new_gate_replays=0,
        full_G2=False,
        adoption=False,
        quantum_advantage=False,
    )
    save(output / "completion_outcome.json", outcome, started)
    files = owned_files(output, started)
    budget(started)
    save(
        output / "manifest.json",
        {
            "schema": "a13-fixed-alpha-allocation-" + ROLE + "-terminal-manifest-v1",
            "files": files,
            "frozen_inputs": frozen,
            "external_runtime_inputs": external,
            "manifest_self_hash_excluded": True,
            "terminal_outcome_file": "completion_outcome.json",
            "completed": outcome["completed"],
            "passed": outcome["passed"],
            "budget_censored": outcome["budget_censored"],
            "rejection": outcome.get("rejection", False),
            "terminal_budget_observation": elapsed(started),
            "all_IO_proof_hashing_output_and_retention_charged": True,
            "historical_LIVE36_references9_paths_not_waived": True,
        },
        started,
    )


def retain_failure(output, frozen, external, started, error, phase):
    if not output.exists():
        return
    try:
        require(
            not (output / "manifest.json").exists()
            and not (output / "completion_outcome.json").exists(),
            "Preserve partial terminal bytes, no reseal",
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
        try:
            with (output / "FAILED_UNSEALED.json").open("xb") as stream:
                stream.write(
                    b'{"failed":true,"completed":false,"passed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"new_test_credit":0,"partial_success_invalid":true,"fresh_version_and_receipt_required":true}\n'
                )
        except FileExistsError:
            pass


def prepare(output):
    started = process_started()
    frozen, external, created = {}, {}, False
    try:
        setup(started)
        forbidden_imports()
        require(output == OUTPUT and not output.exists(), "Fresh exact allocation receipt only")
        ready = ready_policy(frozen, external, started)
        reports, _inputs = prerequisites(ready, frozen, external, started)
        source_pin = None
        if ROLE == "auditor":
            source_pin = ready["actual_allocation_producer_manifest_SHA256"]
            packet(SOURCE, source_pin, frozen, external, started, allow_rejection=True)
        interpreter = runtime(frozen, external, started)
        runtime_policy(interpreter, started)
        verify_loaded(frozen, external, started)
        verify(frozen, external, started)
        budget(started, admission=True)
        output.mkdir()
        created = True
        (output / "executed_code").mkdir()
        for source in (
            COMPOSER_AUTHOR,
            AUDIT_AUTHOR,
            METHOD,
            METHOD_DOC,
            IMPLEMENTATION,
            IMPLEMENTATION_DOC,
            BOOKKEEPING_ORIGIN,
        ):
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
            "schema": "a13-fixed-alpha-allocation-protocol-v1",
            "role": ROLE,
            "output": output.relative_to(ROOT).as_posix(),
            "frozen_inputs": frozen,
            "external_runtime_inputs": external,
            "root_READY_sha256": sha(READY, started),
            "root_READY_snapshot_sha256": sha(output / "root_READY_snapshot.json", started),
            "limits_CPU_work_wall": [CPU, ADMISSION, WALL],
            "interval_digits": DIGITS,
            "numerical_threads": 1,
            "alpha": encode(ALPHA),
            "beta": encode(EPSILON),
            "interpreter": interpreter,
            "author_sha256": ready["author_inputs"],
            "actual_manifest_inputs": ready["manifest_inputs"],
            "actual_allocation_producer_manifest_SHA256": source_pin,
            "new_test_credit": 0,
            "no_fit_sourcewalk_or_numerical_kernel_executed_in_prepare": True,
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
    global _KERNEL_ADMITTED
    started = process_started()
    frozen, external, admitted = {}, {}, False
    try:
        setup(started)
        forbidden_imports()
        require(output == OUTPUT and output.is_dir(), "Exact prepared allocation receipt")
        no_failure(output)
        require(
            not any(
                (output / name).exists()
                for name in ("manifest.json", "run_started.json", "completion_outcome.json")
            ),
            "One fresh run; partial terminal evidence blocks reuse",
        )
        admitted = True
        protocol, prepared = (
            read(output / name, started) for name in ("protocol.json", "PREPARED_RECEIPT.json")
        )
        require(
            protocol["schema"] == "a13-fixed-alpha-allocation-protocol-v1"
            and protocol["role"] == ROLE
            and protocol["interval_digits"] == DIGITS
            and protocol["numerical_threads"] == 1,
            "Actual fixed prepared role/precision",
        )
        same(
            protocol["limits_CPU_work_wall"],
            [CPU, ADMISSION, WALL],
            "Original complete process limits",
        )
        same(protocol["alpha"], encode(ALPHA), "ONE fixed alpha")
        same(protocol["beta"], encode(EPSILON), "Original final floor allowance")
        require(
            prepared["prepared"] is True
            and prepared["terminal"] is False
            and sha(output / "protocol.json", started) == prepared["protocol_sha256"],
            "Actual immutable prepare protocol",
        )
        for mapping, is_external in (
            (protocol["frozen_inputs"], False),
            (protocol["external_runtime_inputs"], True),
        ):
            for key, expected in mapping.items():
                actual = bind(
                    frozen, external, Path(key) if is_external else ROOT / key, expected, started
                )
                require(
                    (str(actual) if is_external else actual.relative_to(ROOT).as_posix()) == key,
                    "Canonical prepared actual maps",
                )
        for name in (
            "protocol.json",
            "PREPARED_RECEIPT.json",
            "interpreter.json",
            "prerequisite_admission.json",
        ):
            bind(frozen, external, output / name, sha(output / name, started), started)
        ready = ready_policy(frozen, external, started)
        require(
            sha(READY, started) == protocol["root_READY_sha256"]
            and sha(output / "root_READY_snapshot.json", started)
            == protocol["root_READY_snapshot_sha256"],
            "Root release and exact snapshot immutable",
        )
        same(ready["author_inputs"], protocol["author_sha256"], "No author/method mutation")
        same(
            ready["manifest_inputs"],
            protocol["actual_manifest_inputs"],
            "No expected input mutation",
        )
        reports, inputs = prerequisites(ready, frozen, external, started)
        primary = None
        if ROLE == "auditor":
            pin = protocol["actual_allocation_producer_manifest_SHA256"]
            require(
                ready["actual_allocation_producer_manifest_SHA256"] == pin,
                "Same actual allocation source release",
            )
            primary = packet(SOURCE, pin, frozen, external, started, allow_rejection=True)
        interpreter = read(output / "interpreter.json", started)
        same(interpreter, protocol["interpreter"], "Actual runtime frozen in prepare")
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
        require("mpmath" not in sys.modules, "Interval kernel is deferred until full admission")
        _KERNEL_ADMITTED = True
        import mpmath as mp

        require(
            mp.__version__ == "1.3.0" and sys.modules["mpmath.libmp.backend"].BACKEND == "python",
            "Pinned pure-Python interval backend",
        )
        mp.iv.dps = mp.mp.dps = DIGITS
        verify_loaded(frozen, external, started)
        budget(started, admission=True)
        finance = fixed_financial_test(mp, inputs, started)
        scalar = polynomial_allowance(mp, inputs, started)
        own_eligible = (
            finance["both_financial_residuals_fit"]
            and scalar["all_nonempty_allowances_strict_positive"]
        )
        eligible = own_eligible
        release_value = scalar["E_allow_lower"] if eligible else None
        if ROLE == "auditor":
            source_finance, source_scalar = (
                read(SOURCE / name, started)
                for name in ("fixed_alpha_financial_test.json", "uniform_poly_allowance.json")
            )
            eligible = authorize_primary(
                mp, source_finance, source_scalar, finance, scalar, started
            )
            require(
                primary["summary"]["conditional_allocation_release_eligible"] is eligible
                and primary["summary"]["rejection"] is (not eligible),
                "Independent exact primary release decision",
            )
            release_value = source_scalar["E_allow_lower"] if eligible else None
            if eligible:
                same(
                    primary["summary"]["conditional_E_allow_lower"],
                    release_value,
                    "Actual primary common allocation value",
                )
            save(
                output / "primary_allocation_authorization.json",
                {
                    "independent130_authorizes_complete_primary90_result": True,
                    "source_manifest_sha256": primary["manifest_sha256"],
                    "conditional_allocation_release_eligible": eligible,
                    "approved_primary_E_allow_lower": release_value,
                    "independent_own_release_lower": scalar["E_allow_lower"],
                    "new_fixture_credit": 0,
                },
                started,
            )
        save(
            output
            / (
                "fixed_alpha_financial_test.json"
                if ROLE == "producer"
                else "independent130_fixed_alpha_financial_test.json"
            ),
            finance,
            started,
        )
        save(
            output
            / (
                "uniform_poly_allowance.json"
                if ROLE == "producer"
                else "independent130_uniform_poly_allowance.json"
            ),
            scalar,
            started,
        )
        save(
            output / "accepted_premise_binding.json",
            {
                "actual_manifest_inputs": ready["manifest_inputs"],
                "alpha": encode(ALPHA),
                "beta": encode(EPSILON),
                "original_lambda_H_price_D_S_and_contract_unchanged": True,
                "actual_sourcewalk_fit_gate_replay_or_fixture_executed": False,
                "changed_candidate_native_safety_and_support_not_yet_proved": True,
            },
            started,
        )
        runtime_policy(interpreter, started)
        save(
            output / "loaded_module_origins.json", verify_loaded(frozen, external, started), started
        )
        summary = {
            "schema": "a13-fixed-alpha-allocation-" + ROLE + "-summary-v1",
            "completed": True,
            "passed": True,
            "budget_censored": False,
            "rejection": not eligible,
            "one_fixed_alpha_certificate_valid": True,
            "conditional_allocation_release_eligible": eligible,
            "independent_allocation_audit_passed": ROLE == "auditor",
            "root_review_and_actual_independent_allocation_required": ROLE != "auditor",
            "conditional_E_allow_lower": release_value,
            "actual_source_manifest_sha256": None
            if primary is None
            else primary["manifest_sha256"],
            "both_financial_residual_fit": finance["both_financial_residuals_fit"],
            "all_nonempty_allowances_strict_positive": scalar[
                "all_nonempty_allowances_strict_positive"
            ],
            "alpha": encode(ALPHA),
            "case_financial_F_upper": {
                case: row["financial_F_upper"] for case, row in finance["cases"].items()
            },
            "exploratory_A13_held_method_or_null_fields_changed": False,
            "actual_candidate_G2_feasibility_established": False,
            "actual_fit_gate_emission_fixture_or_sourcewalk_executed": False,
            "new_test_credit": 0,
            "new_gate_replays": 0,
            "full_G2": False,
            "adoption": False,
            "cost_transfer": False,
            "quantum_advantage": False,
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
                "rejection": not eligible,
                "phase": "run",
                "summary_file": "summary.json",
                "conditional_allocation_release_eligible": eligible,
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
    require(output == OUTPUT, "Only the exact fresh allocation receipt")
    result = prepare(output) if args.operation == "prepare" else run(output)
    print(
        json.dumps(
            {
                "role": ROLE,
                "operation": args.operation,
                "prepared": result.get("prepared"),
                "passed": result.get("passed"),
                "release_eligible": result.get("conditional_allocation_release_eligible"),
                "new_test_credit": 0,
            }
        )
    )


if __name__ == "__main__":
    main()
