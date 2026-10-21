"""Author-only fixed twenty-choice exponential approximation and cost screen.

No gate emission, price samples, fixtures, numerical execution or adoption is
performed during authoring. Preparation is stdlib byte/runtime bookkeeping only.
The one future run shares fixed300/270/900 limits across all twenty architectures.
"""

from __future__ import annotations
import argparse
import ctypes
from ctypes import wintypes
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from importlib import metadata
from importlib.util import cache_from_source
import json
from math import comb, factorial
import os
from pathlib import Path
import site
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
OUTPUT = PROGRAM / "A13_run001"
PRODUCER = RESEARCH / "experiment_exp_frontier.py"
AUDITOR = RESEARCH / "audit_exp_frontier.py"
METHOD = RESEARCH / "a13_exp_frontier_preflight.json"
METHOD_DOC = RESEARCH / "A13_EXP_FRONTIER_PREFLIGHT.md"
IMPLEMENTATION = RESEARCH / "a13_exp_frontier_implementation_preflight.json"
IMPLEMENTATION_DOC = RESEARCH / "A13_EXP_FRONTIER_IMPLEMENTATION_PREFLIGHT.md"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
METHOD_SHA = "6c0e97f33e1277c070e6e84883b6631a880997becd214772bb9ef287e1c7ba85"
METHOD_DOC_SHA = "f5b4404650c1ee9bd3a8ef2557d67e1340dda0fc059d94126e19fcfc046d7f7b"
CPU, ADMISSION, WALL = 300, 270, 900
Q, W = 1 << 40, 72
EPSILON, SIGNED_LIMIT = Fraction(1, Q), Fraction(1 << 31)
CASES = {"B4x12": (4, 12, 30), "B8x52": (8, 52, 234)}
DEGREES, SEGMENTS = (4, 6, 8, 10, 12), (1, 2, 4, 8)
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24_000, 2 * 1024**3
_PATHS, _HASHES, _OBSERVED = {}, {}, {}
_EXTERNAL_TREES, _EXTERNAL_FILES = (), ()
_EXTERNAL_ROOT = None
_EXCLUDED_RUNTIME = ()
_PROCESS_CREATION_TICKS = None


class BudgetCensoredError(RuntimeError):
    """Terminal fixed CPU/wall censor, with no retry."""


class MathematicalGuardError(ValueError):
    """A failed proof premise, distinct from a valid residual-bound rejection."""


def guard(condition, message):
    if not condition:
        raise MathematicalGuardError(message)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def budget(started, admission=False):
    cpu, wall = time.process_time() - started[0], time.monotonic() - started[1]
    if cpu >= (ADMISSION if admission else CPU) or wall >= WALL:
        raise BudgetCensoredError("Fixed A13 300CPU/270admission/900wall budget")
    return cpu, wall


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
    budget(started)
    require(
        type(expected) is str
        and len(expected) == 64
        and all(character in "0123456789abcdef" for character in expected),
        "Canonical expected SHA256",
    )
    actual = resolved(path, started)
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


def forbidden_imports():
    banned = ("numpy", "scipy", "numba", "llvmlite", "qiskit", "gmpy", "gmpy2", "sage")
    found = [
        name
        for name in sys.modules
        if any(name == prefix or name.startswith(prefix + ".") for prefix in banned)
        or (
            name.startswith("research.")
            and name
            not in (
                "research.limitation_program_20261001.experiment_exp_frontier",
                "research.limitation_program_20261001",
            )
        )
    ]
    require(
        not found, "No numerical builder, audited code or native backend imports: " + repr(found)
    )


def owner_rows(manifest_path, data, started):
    if "files" in data:
        require(
            type(data["files"]) is dict and type(data.get("frozen_inputs", {})) is dict,
            "Recognized original owner maps",
        )
        require(
            data.get("manifest_self_hash_excluded") is True, "Original nested manifest convention"
        )
        maps = [(field, data.get(field, {})) for field in ("files", "frozen_inputs")]
    else:
        require(
            manifest_path == PROGRAM / "A10_coefficient_run001/manifest.json",
            "Only pinned A10 exact historical flat manifest",
        )
        require(
            all(
                type(key) is str and type(value) is str and len(value) == 64
                for key, value in data.items()
            ),
            "Exact original flat SHA map",
        )
        maps = [("flat_owned_files", data)]
    rows = []
    for field, mapping in maps:
        for original, expected in mapping.items():
            budget(started)
            normalized = original.replace("\\", "/")
            candidate = (
                ROOT / normalized
                if normalized.startswith(
                    ("results/", "research/", "docs/", "manuscript/", ".context/")
                )
                else manifest_path.parent / normalized
            )
            actual = resolved(candidate, started)
            budget(started)
            require(actual.is_relative_to(ROOT), "Original owner membership ROOT confinement")
            rows.append((field, actual, original, expected))
    return rows


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


def literal(raw):
    require(type(raw) is int and -(1 << 71) <= raw < (1 << 72), "Typed native integer literal")
    value = raw % (1 << W)
    return value - (1 << W) if value >= (1 << 71) else value


def nearest_ratio(numerator, denominator):
    quotient, remainder = divmod(numerator, denominator)
    return quotient + (
        2 * remainder > denominator or (2 * remainder == denominator and quotient % 2)
    )


class ActualGraph:
    """Read-only typed actual SSA matching; never builds or evaluates a Graph."""

    def __init__(self, target, started):
        self.started, self.target, self.nodes = started, target, {}
        require(target["width"] == W and target["fraction_bits"] == 40, "Actual native W72/F40")
        arities = dict(
            input=0,
            const=0,
            bits=1,
            add=2,
            sub=2,
            mul=2,
            cmul=1,
            lt=2,
            select=3,
            msb=1,
            shift=2,
            positive=1,
            sqrt=1,
            lookup=1,
        )
        for node in target["nodes"]:
            budget(started)
            op, args, outputs, params = (node[key] for key in ("op", "args", "out", "params"))
            require(
                op in arities and type(args) is list and len(args) == arities[op], "Typed op/arity"
            )
            require(type(params) is dict and type(outputs) is list and outputs, "Typed node fields")
            require(
                all(type(value) is int and value in self.nodes for value in args),
                "Topological inputs",
            )
            require(
                all(
                    type(value) is int and value >= 0 and value not in self.nodes
                    for value in outputs
                ),
                "Unique SSA IDs",
            )
            require(len(set(outputs)) == len(outputs), "Unique multioutput SSA IDs")
            if op != "lookup":
                require(len(outputs) == 1, "Single output operation")
            if op in ("input", "bits", "lookup"):
                require(type(params.get("bits", params.get("width"))) is int, "Integer width field")
            if op == "bits":
                require(
                    type(params.get("shift")) is int and type(params.get("signed")) is bool,
                    "Typed bit shift",
                )
            if op in ("const", "cmul"):
                raw = params["value" if op == "const" else "c"]
                require(
                    set(params) == {"value" if op == "const" else "c"},
                    "Exact native literal parameter keys",
                )
                require(type(raw) is int, "Native literals are JSON ints, never flags")
                require(
                    0 <= raw < (1 << 72) if op == "const" else -(1 << 71) <= raw < (1 << 71),
                    "Const unsigned72/cmul signed72 canonical representations",
                )
                literal(raw)
            if op not in ("input", "const", "cmul", "bits", "lookup"):
                require(params == {}, "Exact arithmetic parameters")
            for value in outputs:
                self.nodes[value] = node
        require(set(self.nodes) == set(range(len(self.nodes))), "Contiguous actual SSA inventory")

    def node(self, value, op=None, params=None):
        budget(self.started)
        require(type(value) is int and value in self.nodes, "Actual SSA value identity")
        node = self.nodes[value]
        require(op is None or node["op"] == op, "Expected actual operation: " + str(value))
        if params is not None:
            same(node["params"], params, "Exact actual operation parameters")
        return node

    def const(self, value, raw=None):
        actual = literal(self.node(value, "const")["params"]["value"])
        require(raw is None or actual == raw, "Exact constant literal")
        return actual

    def clip(self, value, low=None, high=None):
        flag, middle, hi = self.node(value, "select")["args"]
        require(self.node(flag, "lt")["args"] == [middle, hi], "Upper clamp structure")
        lo_flag, lo, raw = self.node(middle, "select")["args"]
        require(self.node(lo_flag, "lt")["args"] == [raw, lo], "Lower clamp structure")
        lower, upper = self.const(lo, low), self.const(hi, high)
        require(lower < upper, "Ordered literal clamp")
        return raw

    def midpoint(self, value, input_id):
        args = self.node(value, "add")["args"]
        shifts = [arg for arg in args if self.node(arg)["op"] == "bits"]
        require(len(shifts) == 1, "Exact midpoint shift")
        shift = shifts[0]
        require(
            self.node(shift, "bits", dict(shift=-8, width=72, signed=False))["args"] == [input_id],
            "Midpoint raw input",
        )
        self.const(next(arg for arg in args if arg != shift), 128)

    def ancestors(self, value):
        found, pending = set(), [value]
        while pending:
            budget(self.started)
            current = pending.pop()
            if current not in found:
                found.add(current)
                pending.extend(self.node(current)["args"])
        return found

    def interpolation(self, value, name, argument):
        segments, degree, lo, index_bits = (32, 8, Q, 5) if name == "log" else (64, 7, 0, 6)
        candidates = {
            tuple(self.node(v)["out"])
            for v in self.ancestors(value)
            if self.node(v)["op"] == "lookup" and self.node(v)["params"]["table"] == name
        }
        require(len(candidates) == 1, "One actual interpolation lookup")
        outputs = next(iter(candidates))
        lookup = self.node(outputs[0], "lookup", dict(table=name, bits=index_bits))
        require(len(outputs) == degree + 1, "Complete actual Horner coefficient outputs")
        index = lookup["args"][0]
        address = self.node(
            index, "bits", dict(shift=40 - index_bits, width=index_bits, signed=False)
        )["args"][0]
        if lo:
            address, lower = self.node(address, "sub")["args"]
            self.const(lower, lo)
        bounded = address
        require(self.clip(bounded, lo, lo + Q - 1) == argument, "Actual interpolation domain")
        current, local = value, None
        for j in range(degree):
            args = self.node(current, "add")["args"]
            require(outputs[j] in args, "Actual Horner coefficient ordering")
            product = next(arg for arg in args if arg != outputs[j])
            factors = self.node(product, "mul")["args"]
            if local is None:
                possible = [v for v in factors if self.node(v)["op"] == "sub"]
                require(len(possible) == 1, "Unique Horner local coordinate")
                local = possible[0]
            require(local in factors, "Every actual Horner multiplication uses local")
            current = next(arg for arg in factors if arg != local)
        require(current == outputs[-1], "Actual Horner degree8/7 terminal coefficient")
        actual_x, center = self.node(local, "sub")["args"]
        require(actual_x == bounded, "Actual local-coordinate input")
        args = self.node(center, "add")["args"]
        shifts = [v for v in args if self.node(v)["op"] == "bits"]
        require(len(shifts) == 1, "Actual segment center shift")
        shift = shifts[0]
        require(
            self.node(shift, "bits", dict(shift=index_bits - 40, width=72, signed=False))["args"]
            == [index],
            "Actual center address",
        )
        self.const(next(v for v in args if v != shift), lo + Q // (2 * segments))
        return dict(
            output=value,
            input=argument,
            address=index,
            local=local,
            lookup_outputs=list(outputs),
            floors=degree,
        )

    def pair(self, roots, raw_u, raw_v, ln2):
        require(len(roots) == 2, "One original joint pair")
        factors = [self.node(value, "mul")["args"] for value in roots]
        common = set(factors[0]) & set(factors[1])
        require(len(common) == 1, "Exactly one shared actual radius")
        radius = next(iter(common))
        positive = self.node(radius, "sqrt")["args"][0]
        negative_two = self.node(positive, "positive")["args"][0]
        log_value = self.node(negative_two, "cmul", dict(c=-2 * Q))["args"][0]
        log_args = self.node(log_value, "add")["args"]
        terms = [v for v in log_args if self.node(v)["op"] == "cmul"]
        require(len(terms) == 1, "Unique exponent-ln2 product")
        term = terms[0]
        scaled = self.node(term, "cmul", dict(c=ln2))["args"][0]
        exponent = self.node(scaled, "bits", dict(shift=-40, width=72, signed=False))["args"][0]
        top, fraction = self.node(exponent, "sub")["args"]
        self.const(fraction, 40)
        safe = self.node(top, "msb")["args"][0]
        flag, tiny, mid_u = self.node(safe, "select")["args"]
        self.const(tiny, 1)
        require(self.node(flag, "lt")["args"] == [mid_u, tiny], "Actual safe positive log input")
        self.midpoint(mid_u, raw_u)
        poly = next(v for v in log_args if v != term)
        lookups = [self.node(v) for v in self.ancestors(poly) if self.node(v)["op"] == "lookup"]
        require(len({tuple(node["out"]) for node in lookups}) == 1, "Unique log lookup")
        index = lookups[0]["args"][0]
        address = self.node(index)["args"][0]
        clipped = self.node(address, "sub")["args"][0]
        mantissa = self.clip(clipped, Q, 2 * Q - 1)
        u, negated = self.node(mantissa, "shift")["args"]
        require(u == safe, "Actual mantissa normalized from safe midpoint")
        zero, actual_exponent = self.node(negated, "sub")["args"]
        self.const(zero, 0)
        require(actual_exponent == exponent, "Actual left-shift exponent")
        log_scope = self.interpolation(poly, "log", mantissa)
        cosines = [next(v for v in row if v != radius) for row in factors]
        arguments = []
        for cosine in cosines:
            lookup = [
                self.node(v) for v in self.ancestors(cosine) if self.node(v)["op"] == "lookup"
            ]
            require(len({tuple(node["out"]) for node in lookup}) == 1, "Unique cosine lookup")
            clip = self.node(lookup[0]["args"][0])["args"][0]
            arguments.append(self.clip(clip, 0, Q - 1))
        mid_v, quarter = arguments
        self.midpoint(mid_v, raw_v)
        wrapped = self.node(quarter, "bits", dict(shift=0, width=40, signed=False))["args"][0]
        args = self.node(wrapped, "add")["args"]
        require(mid_v in args, "Positive sine convention uses same midpoint")
        self.const(next(v for v in args if v != mid_v), 3 * Q // 4)
        scopes = [self.interpolation(v, "cos", a) for v, a in zip(cosines, arguments, strict=True)]
        inputs = {
            v for root in roots for v in self.ancestors(root) if self.node(v)["op"] == "input"
        }
        require(inputs == {raw_u, raw_v}, "Original pair input closure")
        return dict(
            normal_values=list(roots),
            raw_uniform_values=[raw_u, raw_v],
            radius=radius,
            log=log_scope,
            cosines=scopes,
            original_shared_pair_preserved=True,
        )

    def flatten(self, value, stops, op="add"):
        result, pending = Counter(), [value]
        while pending:
            budget(self.started)
            current = pending.pop()
            if current in stops:
                result[current] += 1
            else:
                pending.extend(self.node(current, op)["args"])
        return result

    def maxima(self, value, stops):
        result, pending = Counter(), [value]
        while pending:
            current = pending.pop()
            if current in stops:
                result[current] += 1
                continue
            flag, hi, lo = self.node(current, "select")["args"]
            require(self.node(flag, "lt")["args"] == [lo, hi], "Exact basket maximum tree")
            pending.extend((lo, hi))
        return result


def encode(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def iv(mp, value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def interval(value):
    result = []
    for sign, mantissa, exponent, _ in value._mpi_:
        result.append(Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent)
    require(len(result) == 2 and result[0] <= result[1], "Finite outward interval endpoints")
    return tuple(result)


def coefficient_error(value, bounds):
    return max(abs(value - bounds[0]), abs(value - bounds[1]))


def exact(value):
    require(
        type(value) is list
        and len(value) == 2
        and all(type(part) is int for part in value)
        and value[1] > 0,
        "Canonical exact rational endpoint",
    )
    result = Fraction(*value)
    require(encode(result) == value, "Reduced exact rational endpoint")
    return result


def upper(value):
    return interval(value)[1]


def lower(value):
    return interval(value)[0]


def absolute_error(word, enclosure):
    lo, hi = interval(enclosure)
    return max(abs(Fraction(word, Q) - lo), abs(Fraction(word, Q) - hi))


def signed_range(pair):
    guard(
        type(pair) is tuple
        and len(pair) == 2
        and pair[0] <= pair[1]
        and -(1 << 71) <= pair[0] <= pair[1] < 1 << 71,
        "Every actual stored72 intermediate must be signed-safe",
    )
    return pair


def product_range(pair):
    guard(
        -(1 << 143) <= pair[0] <= pair[1] < 1 << 143, "Every actual signed144 product must be safe"
    )
    return pair


def stock_site(graph, stock, raw_log, started):
    polynomial, exponent = graph.node(stock, "shift")["args"]
    scaled = graph.node(exponent, "bits", dict(shift=40, width=72, signed=True))["args"][0]
    inverse_node = graph.node(scaled, "cmul")
    clipped, cinv = inverse_node["args"][0], inverse_node["params"]["c"]
    same(graph.clip(clipped), raw_log, "Original raw log under exact decoded clamps")
    top = graph.node(clipped, "select")
    low_id = graph.node(top["args"][1], "select")["args"][1]
    low, high = graph.const(low_id), graph.const(top["args"][2])
    selected, pending = set(), [stock]
    while pending:
        budget(started)
        value = pending.pop()
        if value == clipped or value in selected:
            continue
        node = graph.node(value)
        require(
            len(node["out"]) == 1
            and node["op"] in ("const", "cmul", "bits", "sub", "mul", "add", "shift"),
            "Original actual stock range-reduction/Estrin DAG",
        )
        selected.add(value)
        pending.extend(node["args"])
    reductions = [
        value
        for value in selected
        if graph.node(value)["op"] == "sub" and graph.node(value)["args"][0] == clipped
    ]
    require(len(reductions) == 1, "One actual stock remainder")
    remainder = reductions[0]
    ln_node = graph.node(graph.node(remainder, "sub")["args"][1], "cmul")
    require(
        graph.node(ln_node["args"][0], "bits", dict(shift=-40, width=72, signed=False))["args"]
        == [exponent],
        "Actual integer-exact k*ln2 source path",
    )
    cln = ln_node["params"]["c"]
    signatures = {clipped: ["clipped-native-word"]}
    for value in sorted(selected):
        budget(started)
        node = graph.node(value)
        children = [signatures[arg] for arg in node["args"]]
        if node["op"] in ("add", "mul"):
            children.sort(key=lambda child: json.dumps(child, sort_keys=True))
        signatures[value] = [node["op"], node["params"], children]
    signature = hashlib.sha256(json.dumps(signatures[stock], sort_keys=True).encode()).hexdigest()
    return dict(
        stock=stock,
        clipped=clipped,
        raw_log=raw_log,
        polynomial=polynomial,
        exponent=exponent,
        remainder=remainder,
        low=low,
        high=high,
        inverse_ln2=cinv,
        ln2=cln,
        values=sorted(selected),
        actual_original_support_signature=signature,
    )


def integer_stock_cell(graph, site, left, right, k, started):
    ranges, products = {site["clipped"]: (left, right)}, []
    for value in site["values"]:
        budget(started)
        node = graph.node(value)
        op, args, params = node["op"], [ranges[v] for v in node["args"]], node["params"]
        if op == "const":
            result = (graph.const(value),) * 2
        elif op == "cmul":
            endpoints = [v * params["c"] for v in args[0]]
            product = product_range((min(endpoints), max(endpoints)))
            products.append(dict(value=value, product_raw_bounds=list(product)))
            result = (product[0] // Q, product[1] // Q)
        elif op == "bits":
            require(params["width"] == 72, "Full72 actual stock extraction")
            shift = params["shift"]
            if shift >= 0:
                require(params["signed"] is True, "Signed actual exponent extraction")
                result = (args[0][0] >> shift, args[0][1] >> shift)
            else:
                require(params["signed"] is False, "Actual modular full72 integer scaling")
                # Modular left-shift of a negative word cancels its 2^72 representation.
                result = (args[0][0] << -shift, args[0][1] << -shift)
        elif op in ("add", "sub"):
            a, b = args
            result = (a[0] + b[0], a[1] + b[1]) if op == "add" else (a[0] - b[1], a[1] - b[0])
        elif op == "mul":
            a, b = args
            values = [x * y for x in a for y in b]
            minimum = 0 if node["args"][0] == node["args"][1] and a[0] <= 0 <= a[1] else min(values)
            product = product_range((minimum, max(values)))
            products.append(dict(value=value, product_raw_bounds=list(product)))
            result = (product[0] // Q, product[1] // Q)
        else:
            require(op == "shift" and args[1] == (k, k), "Actual fixed native shift control")
            guard(-72 < k < 72 and args[0][0] > 0, "Native positive stock shift premise")
            result = tuple(v << k if k >= 0 else v >> -k for v in args[0])
        ranges[value] = signed_range(result)
    require(ranges[site["exponent"]] == (k, k), "Every cell gives its exact floor exponent")
    require(
        ranges[site["remainder"]] == (left - k * site["ln2"], right - k * site["ln2"]),
        "Exact actual remainder interval",
    )
    guard(ranges[site["stock"]][0] > 0, "Every clipped-domain stock word strictly positive")
    return ranges, products


def sparse_stock_model(graph, site, radius, started):
    """Fresh actual-DAG induction for literal polynomial and signed-floor errors."""
    values, steps = {}, []

    def visit(value):
        budget(started)
        if value == site["remainder"]:
            return {1: Fraction(1)}, Fraction(0)
        if value in values:
            return values[value]
        node = graph.node(value)
        if node["op"] == "const":
            coefficients, error = {0: Fraction(graph.const(value), Q)}, Fraction(0)
        else:
            require(
                node["op"] in ("add", "mul") and node["params"] == {},
                "Actual polynomial only constant/add/signed-floor-multiply",
            )
            a, ea = visit(node["args"][0])
            b, eb = visit(node["args"][1])
            ma = sum((abs(c) * radius**d for d, c in a.items()), Fraction(0))
            mb = sum((abs(c) * radius**d for d, c in b.items()), Fraction(0))
            if node["op"] == "add":
                coefficients = dict(a)
                for degree, coefficient in b.items():
                    coefficients[degree] = coefficients.get(degree, Fraction(0)) + coefficient
                error = ea + eb
            else:
                coefficients = {}
                for da, ca in a.items():
                    for db, cb in b.items():
                        degree = da + db
                        coefficients[degree] = coefficients.get(degree, Fraction(0)) + ca * cb
                error = ma * eb + mb * ea + ea * eb + EPSILON
                guard(
                    (ma + ea) * (mb + eb) * Q * Q < 1 << 143,
                    "Actual Estrin signed144 error-induction product",
                )
        magnitude = sum((abs(c) * radius**d for d, c in coefficients.items()), Fraction(0)) + error
        guard(magnitude * Q < 1 << 71, "Actual Estrin stored72 error-induction range")
        values[value] = coefficients, error
        steps.append(
            dict(
                value=value,
                op=node["op"],
                magnitude_upper=encode(magnitude),
                native_floor_error_upper=encode(error),
            )
        )
        return coefficients, error

    coefficients, error = visit(site["polynomial"])
    require(
        set(coefficients) == set(range(13)) and all(c >= 0 for c in coefficients.values()),
        "Original actual degree12 positive polynomial",
    )
    literal_error = sum(
        (abs(coefficients[d] - Fraction(1, factorial(d))) * radius**d for d in range(13)),
        Fraction(0),
    )
    return coefficients, error, literal_error, steps


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


def seal(output, frozen, external, started, outcome):
    require(
        not (output / "manifest.json").exists() and not (output / "FAILED_UNSEALED.json").exists(),
        "Single terminal outcome, no retry",
    )
    budget(started)
    verified = final_verify(frozen, external, started)
    outcome = dict(
        outcome,
        verification_unique_paths=verified,
        budget=elapsed(started),
        limits_CPU_admission_wall=[300, 270, 900],
        new_test_credit=0,
        full_G2=False,
        cost_transfer=False,
        adoption=False,
    )
    save(output / "completion_outcome.json", outcome, started)
    files = owned_files(output, started)
    budget(started)
    manifest = dict(
        schema="a13-exp-frontier-terminal-manifest-v1",
        files=files,
        frozen_inputs=frozen,
        external_runtime_inputs=external,
        manifest_self_hash_excluded=True,
        terminal_outcome_file="completion_outcome.json",
        completed=outcome["completed"],
        passed=outcome["passed"],
        budget_censored=outcome["budget_censored"],
        terminal_budget_observation=elapsed(started),
        verification_and_output_hashing_before_terminal=True,
        original_expected_hashes_waived=False,
        historical_global_LIVE_integrity=dict(
            passed=False, mismatch_references=36, distinct_paths=9, expected_hashes_waived=False
        ),
        archived_selected_receipt_validity_separate=True,
    )
    save(output / "manifest.json", manifest, started)


def retain_failure(output, frozen, external, started, error, phase):
    """Hard budget includes all failure retention; exhaustion stays explicitly unsealed."""
    if not output.exists():
        # No receipt was created: caller reports an actual pre-mkdir exception to root.
        return
    try:
        require(
            not (output / "manifest.json").exists(),
            "Existing or partial terminal manifest blocks failure reseal",
        )
        require(
            not (output / "completion_outcome.json").exists(),
            "Partial completion record blocks reseal",
        )
        budget(started)
        save(
            output / "failure.json",
            dict(
                phase=phase,
                error_type=type(error).__name__,
                error=str(error),
                traceback=traceback.format_exc(),
                failed=True,
                all_fixture_credit=0,
                budget=elapsed(started),
            ),
            started,
        )
        seal(
            output,
            frozen,
            external,
            started,
            dict(
                completed=False,
                passed=False,
                failed=True,
                budget_censored=isinstance(error, BudgetCensoredError),
                phase=phase,
                rejection=False,
                failure_file="failure.json",
            ),
        )
    except BaseException as retention_error:
        # Small exclusive marker intentionally performs no hashes or scans after hard exhaustion.
        marker = output / "FAILED_UNSEALED.json"
        if not marker.exists():
            save(
                marker,
                dict(
                    failed=True,
                    completed=False,
                    passed=False,
                    budget_censored=True,
                    phase=phase,
                    original_error_type=type(error).__name__,
                    retention_error_type=type(retention_error).__name__,
                    elapsed=elapsed(started),
                    new_test_credit=0,
                    partial_summary_or_manifest_is_not_terminal_success=True,
                    requires_fresh_version_and_receipt=True,
                ),
            )


def ceil_fraction(value):
    value = Fraction(value)
    return -((-value.numerator) // value.denominator)


def point_fraction(value):
    sign, mantissa, exponent, bits = value._mpf_
    require(
        type(mantissa) is int
        and type(exponent) is int
        and type(bits) is int
        and bits >= 0
        and sign in (0, 1),
        "Finite point value",
    )
    return Fraction((-1 if sign else 1) * mantissa) * (Fraction(2) ** exponent)


def mp_point(mp, value):
    value = Fraction(value)
    return mp.mpf(value.numerator) / value.denominator


def polynomial_value(coefficients, x):
    result = x * 0
    for coefficient in reversed(coefficients):
        result = result * x + coefficient
    return result


def segment_inventory(hull, count):
    lo, hi = hull
    span = hi - lo + 1
    require(type(count) is int and count in SEGMENTS and span >= count, "Nonempty fixed partition")
    rows = []
    for j in range(count):
        left, right = lo + j * span // count, lo + (j + 1) * span // count - 1
        center = int(nearest_ratio(left + right, 2))
        require(left <= center <= right, "Exact dyadic center is inside its closed segment")
        rows.append(
            dict(
                segment=j,
                raw_bounds=[left, right],
                center_raw=center,
                local_interval=[
                    encode(Fraction(left - center, Q)),
                    encode(Fraction(right - center, Q)),
                ],
            )
        )
    require(
        rows[0]["raw_bounds"][0] == lo and rows[-1]["raw_bounds"][1] == hi, "Complete hull cover"
    )
    require(
        all(a["raw_bounds"][1] + 1 == b["raw_bounds"][0] for a, b in zip(rows, rows[1:])),
        "Disjoint native membership",
    )
    return rows


def better_exchange(candidate, previous):
    if previous is None:
        return True
    if candidate[:2] != previous[:2]:
        return candidate[:2] > previous[:2]
    return candidate[2] < previous[2]


def fit_segment(mp, degree, segment, started):
    """Fixed fitting heuristic; no root completeness or global optimality theorem."""
    left, right = [exact(v) for v in segment["local_interval"]]
    center = Fraction(segment["center_raw"], Q)
    a, b = mp_point(mp, left), mp_point(mp, right)
    nodes = sorted(
        (a + b) / 2 + (b - a) * mp.cos(mp.pi * j / (degree + 1)) / 2 for j in range(degree + 2)
    )
    rounds = []
    coefficients = None
    for iteration in range(32):
        budget(started)
        require(
            len(nodes) == degree + 2 and all(x < y for x, y in zip(nodes, nodes[1:])),
            "Distinct alternating solve nodes",
        )
        matrix = [
            [x**j for j in range(degree + 1)] + [mp.mpf((-1) ** i)] for i, x in enumerate(nodes)
        ]
        rhs = [mp.exp(mp_point(mp, center) + x) for x in nodes]
        solved = mp.lu_solve(matrix, rhs)
        coefficients = [solved[j] for j in range(degree + 1)]
        require(len(coefficients) == degree + 1, "Exact frozen degree")
        derivative = [j * coefficients[j] for j in range(1, degree + 1)]

        def residual(x):
            return mp.exp(mp_point(mp, center) + x) - polynomial_value(coefficients, x)

        def derivative_residual(x):
            return mp.exp(mp_point(mp, center) + x) - polynomial_value(derivative, x)

        grid = [a + (b - a) * j / 64 for j in range(65)]
        values = [derivative_residual(x) for x in grid]
        critical = [a, b]
        brackets = []
        for j in range(64):
            budget(started)
            if values[j] == 0:
                critical.append(grid[j])
            if values[j] * values[j + 1] < 0:
                low, high, sign = grid[j], grid[j + 1], values[j]
                for _ in range(24):
                    budget(started)
                    middle = (low + high) / 2
                    value = derivative_residual(middle)
                    if value == 0:
                        low = high = middle
                    elif sign * value > 0:
                        low, sign = middle, value
                    else:
                        high = middle
                root = (low + high) / 2
                critical.append(root)
                brackets.append(
                    dict(
                        grid_cell=j,
                        final_bracket=[encode(point_fraction(low)), encode(point_fraction(high))],
                    )
                )
        if values[-1] == 0:
            critical.append(b)
        critical = sorted(set(critical))
        heights = [residual(x) for x in critical]
        height_fractions = [point_fraction(value) for value in heights]
        bottlenecks = {}
        for height in height_fractions:
            budget(started)
            if height == 0:
                continue
            sign = 1 if height > 0 else -1
            previous = dict(bottlenecks)
            key = (1, sign)
            bottlenecks[key] = max(abs(height), bottlenecks.get(key, abs(height)))
            for (length, last_sign), value in previous.items():
                if length < degree + 2 and last_sign != sign:
                    key = (length + 1, sign)
                    candidate = min(value, abs(height))
                    bottlenecks[key] = max(candidate, bottlenecks.get(key, candidate))
        final_bottlenecks = [
            value for (length, _), value in bottlenecks.items() if length == degree + 2
        ]
        require(final_bottlenecks, "Fixed exchange failed to find declared alternating nodes")
        threshold = max(final_bottlenecks)
        states = {}
        for index, height in enumerate(height_fractions):
            budget(started)
            if height == 0 or abs(height) < threshold:
                continue
            sign = 1 if height > 0 else -1
            previous = dict(states)
            first = (threshold, abs(height), (index,))
            if better_exchange(first, states.get((1, sign))):
                states[(1, sign)] = first
            for (length, last_sign), entry in previous.items():
                if length < degree + 2 and last_sign != sign:
                    candidate = (threshold, entry[1] + abs(height), entry[2] + (index,))
                    key = (length + 1, sign)
                    if better_exchange(candidate, states.get(key)):
                        states[key] = candidate
        choices = [value for (length, _), value in states.items() if length == degree + 2]
        require(choices, "Fixed exchange failed to find declared alternating nodes")
        selected = None
        for candidate in choices:
            if better_exchange(candidate, selected):
                selected = candidate
        following = [critical[index] for index in selected[2]]
        rounds.append(
            dict(
                round=iteration + 1,
                solve_nodes=[encode(point_fraction(v)) for v in nodes],
                solved_coefficients=[encode(point_fraction(v)) for v in coefficients],
                solved_alternating_error=encode(point_fraction(solved[degree + 1])),
                candidate_stationary_brackets=brackets,
                candidate_extrema=[encode(point_fraction(v)) for v in critical],
                candidate_residuals=[encode(point_fraction(v)) for v in heights],
                exact_exchange_bottleneck=encode(threshold),
                exact_two_pass_bottleneck_then_sum_lex=True,
                selected_next_node_indices=list(selected[2]),
                selected_next_nodes=[encode(point_fraction(v)) for v in following],
            )
        )
        nodes = following
    fractions = [point_fraction(v) for v in coefficients]
    words = [int(nearest_ratio((v * Q).numerator, (v * Q).denominator)) for v in fractions]
    require(
        all(-(1 << 71) <= v < (1 << 71) for v in words),
        "Every quantized coefficient fits canonical signed72",
    )
    return dict(
        **segment,
        degree=degree,
        exchange_rounds=rounds,
        coefficients_before_quantization=[encode(v) for v in fractions],
        coefficient_raw=words,
        coefficients_from_round32_solve=True,
        extra33rd_solve=False,
        root_search_fitting_evidence_only=True,
        global_minimax_optimality_claim=False,
    )


def bernstein_power(coefficients, left, right, degree, started):
    """Exact power->Bernstein transform on the entire closed interval."""
    width = right - left
    require(width >= 0 and len(coefficients) <= degree + 1, "Closed Bernstein domain and degree")
    transformed = []
    for k in range(degree + 1):
        budget(started)
        transformed.append(
            width**k
            * sum(
                (
                    coefficients[j] * comb(j, k) * left ** (j - k)
                    for j in range(k, len(coefficients))
                ),
                Fraction(0),
            )
        )
    result = []
    for k in range(degree + 1):
        budget(started)
        result.append(
            sum(
                (transformed[j] * Fraction(comb(k, j), comb(degree, j)) for j in range(k + 1)),
                Fraction(0),
            )
        )
    return result


def snap_enclosure(pair, bits=384):
    scale = 1 << bits
    lo, hi = pair
    return (
        Fraction((lo * scale).numerator // (lo * scale).denominator, scale),
        Fraction(ceil_fraction(hi * scale), scale),
    )


def segment_certificate(mp, fit, started):
    left, right = [exact(v) for v in fit["local_interval"]]
    center = Fraction(fit["center_raw"], Q)
    require(left <= 0 <= right, "Taylor center inside closed certificate interval")
    terms = 80
    exponential = interval(mp.iv.exp(iv(mp, center)))
    taylor = bernstein_power(
        [Fraction(1, factorial(j)) for j in range(terms)], left, right, terms - 1, started
    )
    radius = max(abs(left), abs(right))
    tail = upper(
        mp.iv.exp(iv(mp, center + right)) * iv(mp, radius**terms / Fraction(factorial(terms)))
    )
    coefficient_sets = (
        [exact(v) for v in fit["coefficients_before_quantization"]],
        [Fraction(v, Q) for v in fit["coefficient_raw"]],
    )
    result = {k: fit[k] for k in ("segment", "raw_bounds", "center_raw", "local_interval")}
    result.update(
        Taylor_terms=terms,
        exp_center_enclosure=[encode(v) for v in exponential],
        Taylor_tail_upper=encode(tail),
        Bernstein_degree=terms - 1,
        Bernstein_coefficients_count=terms,
        Bernstein_outward_binary_grid_bits=384,
    )
    for name, coefficients in zip(("fit", "quantized"), coefficient_sets, strict=True):
        polynomial = bernstein_power(coefficients, left, right, terms - 1, started)
        enclosures = []
        for p, t in zip(polynomial, taylor, strict=True):
            budget(started)
            product = (exponential[0] * t, exponential[1] * t)
            pair = snap_enclosure((p - max(product), p - min(product)))
            enclosures.append([encode(v) for v in pair])
        bound = max(abs(exact(v)) for pair in enclosures for v in pair)
        result[name + "_Bernstein_coefficient_enclosures"] = enclosures
        result[name + "_Bernstein_SHA256"] = hashlib.sha256(
            canonical(enclosures).encode()
        ).hexdigest()
        result[name + "_uniform_error_upper"] = encode(bound + tail)
    result["mesh_or_exchange_convergence_used_as_uniform_proof"] = False
    return result


def candidate_plan(degree):
    nodes = [dict(value=0, op="local", args=[])]
    for j in range(degree + 1):
        nodes.append(dict(value=len(nodes), op="coefficient", args=[], degree=j))
    current = list(range(1, degree + 2))
    power = 0
    while len(current) > 1:
        following = []
        for index in range(0, len(current) - 1, 2):
            product = len(nodes)
            nodes.append(dict(value=product, op="mul", args=[power, current[index + 1]]))
            out = len(nodes)
            nodes.append(dict(value=out, op="add", args=[current[index], product]))
            following.append(out)
        if len(current) % 2:
            following.append(current[-1])
        if len(following) > 1:
            out = len(nodes)
            nodes.append(dict(value=out, op="mul", args=[power, power]))
            power = out
        current = following
    return dict(
        nodes=nodes,
        output=current[0],
        odd_term_carried_without_zero_pad=True,
        unused_candidate_power_emitted=False,
    )


def native_candidate(plan, words, raw_bounds, started):
    """Symbolic exact range/floor induction, never gate/state replay."""
    values, polynomials, errors = {}, {}, {}
    radius = Fraction(max(abs(v) for v in raw_bounds), Q)
    records, products = [], []
    for node in plan["nodes"]:
        budget(started)
        out, op = node["value"], node["op"]
        if op == "local":
            bound = tuple(raw_bounds)
            coefficients = [Fraction(0), Fraction(1)]
            error = Fraction(0)
        elif op == "coefficient":
            word = words[node["degree"]]
            bound = (word, word)
            coefficients = [Fraction(word, Q)]
            error = Fraction(0)
        else:
            a, b = node["args"]
            pa, pb = polynomials[a], polynomials[b]
            ea, eb = errors[a], errors[b]
            if op == "add":
                coefficients = [Fraction(0)] * max(len(pa), len(pb))
                for j, v in enumerate(pa):
                    coefficients[j] += v
                for j, v in enumerate(pb):
                    coefficients[j] += v
                bound = (values[a][0] + values[b][0], values[a][1] + values[b][1])
                error = ea + eb
            else:
                require(op == "mul", "Exact frozen candidate IR")
                coefficients = [Fraction(0)] * (len(pa) + len(pb) - 1)
                for i, x in enumerate(pa):
                    for j, y in enumerate(pb):
                        coefficients[i + j] += x * y
                corners = [x * y for x in values[a] for y in values[b]]
                minimum = 0 if a == b and values[a][0] <= 0 <= values[a][1] else min(corners)
                product = product_range((minimum, max(corners)))
                products.append(dict(value=out, product_raw_bounds=list(product)))
                bound = (product[0] // Q, product[1] // Q)
                ma = sum((abs(v) * radius**j for j, v in enumerate(pa)), Fraction(0))
                mb = sum((abs(v) * radius**j for j, v in enumerate(pb)), Fraction(0))
                error = ma * eb + mb * ea + ea * eb + EPSILON
        values[out] = signed_range(bound)
        polynomials[out] = coefficients
        errors[out] = error
        records.append(
            dict(value=out, op=op, raw_bounds=list(bound), native_floor_error_upper=encode(error))
        )
    require(values[plan["output"]][0] > 0, "Positive changed native polynomial over full interval")
    return dict(
        native_intermediate_ranges=records,
        signed144_products=products,
        native_polynomial_raw_bounds=list(values[plan["output"]]),
        native_floor_error_upper=encode(errors[plan["output"]]),
    )


def architecture_certificate(mp, degree, segments, fits, domain, started):
    plan = candidate_plan(degree)
    certificates = [segment_certificate(mp, row, started) for row in fits]
    ln_error = absolute_error(domain["ln2_word"], mp.iv.log(iv(mp, 2)))
    cases = {}
    for case, data in domain["cases"].items():
        rows = []
        maximum = Fraction(0)
        maximum_alpha = Fraction(0)
        for cell in data["reduction_cells"]:
            for fit, certificate in zip(fits, certificates, strict=True):
                budget(started)
                k, segment = cell["k"], fit["segment"]
                if cell["empty"]:
                    rows.append(dict(k=k, segment=segment, empty=True))
                    continue
                raw_lo, raw_hi = cell["remainder_raw_bounds"]
                left = max(raw_lo, fit["raw_bounds"][0])
                right = min(raw_hi, fit["raw_bounds"][1])
                if left > right:
                    rows.append(dict(k=k, segment=segment, empty=True))
                    continue
                local = (left - fit["center_raw"], right - fit["center_raw"])
                signed_range(local)
                native = native_candidate(plan, fit["coefficient_raw"], local, started)
                polynomial_error = exact(certificate["quantized_uniform_error_upper"]) + exact(
                    native["native_floor_error_upper"]
                )
                scale = Fraction(2) ** k
                reduction = upper(
                    iv(mp, scale)
                    * mp.iv.exp(iv(mp, Fraction(right, Q)))
                    * (mp.iv.exp(iv(mp, abs(k) * ln_error)) - 1)
                )
                shift_floor = EPSILON if k < 0 else Fraction(0)
                error = scale * polynomial_error + reduction + shift_floor
                alpha = upper(
                    mp.iv.exp(iv(mp, abs(k) * ln_error))
                    * (1 + iv(mp, polynomial_error) * mp.iv.exp(iv(mp, Fraction(-left, Q))))
                    - 1
                )
                pmin, pmax = native["native_polynomial_raw_bounds"]
                stock = signed_range((pmin << k, pmax << k) if k >= 0 else (pmin >> -k, pmax >> -k))
                maximum = max(maximum, error)
                maximum_alpha = max(maximum_alpha, alpha)
                rows.append(
                    dict(
                        k=k,
                        segment=segment,
                        empty=False,
                        clipped_log_raw_bounds=[
                            left + k * domain["ln2_word"],
                            right + k * domain["ln2_word"],
                        ],
                        remainder_raw_bounds=[left, right],
                        local_raw_bounds=list(local),
                        **native,
                        ln2_literal_error_upper=encode(ln_error),
                        reduction_stock_error_upper=encode(reduction),
                        negative_shift_floor_upper=encode(shift_floor),
                        absolute_stock_error_upper=encode(error),
                        relative_stock_alpha_upper=encode(alpha),
                        additive_stock_beta_upper=encode(shift_floor),
                        stock_raw_bounds=list(stock),
                        all_native72_product144_and_shift_guards_passed=True,
                    )
                )
        require(
            len(rows) == 30 * segments, "All fixed class/segment intersections including empties"
        )
        cases[case] = dict(
            intersections=rows,
            maximum_absolute_stock_error_upper=encode(maximum),
            maximum_relative_stock_alpha_upper=encode(maximum_alpha),
            additive_stock_beta_upper=encode(EPSILON),
        )
    return dict(
        degree=degree,
        segments=segments,
        segments_certificate=certificates,
        native_evaluation_plan=plan,
        cases=cases,
        no_G2_allocation_or_feasibility_claim=True,
        realized_candidate_gate_or_ABI_proof=False,
    )


def freeze_owner(path, pin, frozen, external, started):
    path = bind(frozen, external, path, pin, started)
    manifest = read(path, started)
    rows = owner_rows(path, manifest, started)
    owned = [row for row in rows if row[0] in ("files", "flat_owned_files")]
    require(owned, "Actual finite owner inventory")
    for _, actual, _, expected in owned:
        budget(started)
        require(actual.is_relative_to(path.parent), "Exact original owned confinement")
        bind(frozen, external, actual, expected, started)
    actual_owned = set()
    for candidate in path.parent.rglob("*"):
        budget(started)
        if candidate.is_file():
            actual = resolved(candidate, started)
            require(
                actual.is_relative_to(path.parent) and actual not in actual_owned,
                "Exact owner inventory without aliases",
            )
            actual_owned.add(actual)
    same(
        sorted(str(v) for v in actual_owned),
        sorted(str(v) for v in {v[1] for v in owned} | {path}),
        "Complete actual original owned membership",
    )
    records = []
    for field, original, literal_key, expected in rows:
        budget(started)
        if original.is_file() and sha(original, started) == expected:
            actual = original
            archived = False
        else:
            matches = [
                candidate
                for _, candidate, _, value in owned
                if value == expected
                and candidate.name in (original.name, "executed_" + original.name)
            ]
            require(matches, "Missing equal-SHA immutable archived route for original dependency")
            actual = sorted(matches)[0]
            archived = True
        bind(frozen, external, actual, expected, started)
        records.append(
            dict(
                owner_manifest=path.relative_to(ROOT).as_posix(),
                source_map=field,
                original_key=literal_key,
                original_expected_sha256=expected,
                verified_input_path=actual.relative_to(ROOT).as_posix(),
                archived_equal_SHA_route=archived,
                expected_hash_waived=False,
            )
        )
    return records


def implementation_policy(started):
    policy = read(IMPLEMENTATION, started)
    require(
        policy["schema"] == "a13-exp-frontier-implementation-preflight-v1",
        "Exact A13 implementation",
    )
    same(policy["CPU_admission_wall_seconds"], [CPU, ADMISSION, WALL], "Fixed whole-screen limits")
    same(
        policy["fixed_grid"],
        [[d, s] for d in DEGREES for s in SEGMENTS],
        "All twenty fixed choices",
    )
    require(
        policy["primary_digits"] == 90
        and policy["independent_digits"] == 130
        and policy["threads"] == 1
        and policy["new_fixture_credit"] == 0,
        "Fixed precision/zero fixture credit",
    )
    require(
        policy["candidate_G2_absolute_stock_error_allocation"] is None
        and policy["candidate_G2_barrier_band_allocation"] is None
        and policy["gate_emission_authorized"] is False,
        "Exploratory null allocation",
    )
    same(
        policy["method_document_SHA256"],
        {METHOD.name: METHOD_SHA, METHOD_DOC.name: METHOD_DOC_SHA},
        "Held method bytes",
    )
    require(
        policy["A07_manifest_SHA256"]
        == "7380a91d89d4d7657533290406712139dee98913eef4ba60cb71e1de7e0e1f7e",
        "Root supplied actual A07 pin",
    )
    require(
        set(policy["author_sha256"]) == {PRODUCER.name, AUDITOR.name},
        "Both authored executables frozen",
    )
    for name, expected in policy["author_sha256"].items():
        budget(started)
        require(type(expected) is str and len(expected) == 64, "Null author pin blocks preparation")
        require(sha(RESEARCH / name, started) == expected, "Exact reviewed author byte SHA")
    return policy


def selected_inputs(policy, frozen, external, started):
    bind(frozen, external, METHOD, METHOD_SHA, started)
    bind(frozen, external, METHOD_DOC, METHOD_DOC_SHA, started)
    method = read(METHOD, started)
    require(method["schema"] == "a13-exp-frontier-author-preflight-v1", "Held A13 method")
    pins = method["selected_existing_manifest_expected_pins"]
    owners = {key: expected for key, expected in pins.items() if key.endswith("/manifest.json")}
    owners["results/limitation_program_20261001/A07_run003/manifest.json"] = policy[
        "A07_manifest_SHA256"
    ]
    records = []
    for key, expected in owners.items():
        budget(started)
        records.extend(freeze_owner(ROOT / key, expected, frozen, external, started))
    for key, expected in pins.items():
        budget(started)
        actual = bind(frozen, external, ROOT / key, expected, started)
        if key.endswith("/manifest.json"):
            continue
        require(
            any(
                row["verified_input_path"] == actual.relative_to(ROOT).as_posix()
                and row["original_expected_sha256"] == expected
                for row in records
            ),
            "Exact selected owner membership",
        )
    for name, expected in method["A07_domain_interface"][
        "selected_existing_bounds_expected_pins"
    ].items():
        bind(frozen, external, PROGRAM / "A07_run003" / name, expected, started)
    for path in (PRODUCER, AUDITOR, IMPLEMENTATION, IMPLEMENTATION_DOC):
        bind(frozen, external, path, sha(path, started), started)
    return method, records


def library_path(source, started):
    raw = source["library_workspace_relative"].replace("\\", "/")
    require(".." not in raw.split("/"), "No library traversal")
    marker = raw.lower().find("/results/")
    path = ROOT / raw[marker + 1 :] if marker >= 0 else ROOT / raw
    actual = resolved(path, started)
    require(actual.is_relative_to(PROGRAM), "Exact saved workspace gate library")
    return actual


def source_domain_binding(method, frozen, external, started):
    cases, graphs, sources, catalogs, schedules = {}, {}, {}, {}, {}
    hull = None
    for case, (assets, dates, pairs) in CASES.items():
        budget(started, admission=True)
        folder = PROGRAM / "A10_coefficient_run001" / case / "min-depth"
        target, source, schedule = (
            read(folder / name, started)
            for name in ("target.json", "source.json", "schedule_capped.json")
        )
        graph = ActualGraph(target, started)
        for table in target["tables"].values():
            for row in table:
                budget(started)
                require(
                    all(type(v) is int and -(1 << 71) <= v < (1 << 71) for v in row),
                    "Canonical signed72 saved table literals",
                )
        nodes = [node for node in target["nodes"] if node["op"] != "input"]
        require(
            len(nodes) == len(source["forward_calls"]),
            "Complete actual native source call inventory",
        )
        same(
            source["inputs"],
            [node for node in target["nodes"] if node["op"] == "input"],
            "Exact q32 actual source inputs",
        )
        require(
            len(source["inputs"]) == 2 * pairs
            and all(node["params"]["bits"] == 32 for node in source["inputs"]),
            "Original joint pair/q32 roles retained",
        )
        same(source["outputs"], target["outputs"], "Complete original financial outputs")
        same(
            schedule["target_fingerprint"],
            hashlib.sha256(json.dumps(target, sort_keys=True).encode()).hexdigest(),
            "Exact saved capped target fingerprint",
        )
        same(
            schedule["source_fingerprint"],
            hashlib.sha256(json.dumps(source, sort_keys=True).encode()).hexdigest(),
            "Exact saved capped source fingerprint",
        )
        baseline = method["baseline_cases"][case]
        same(
            [schedule["resources"][k] for k in ("t_count", "t_depth", "logical_qubits")],
            [
                baseline["full_source_T_count"],
                baseline["full_source_T_depth"],
                baseline["logical_qubit_cap"],
            ],
            "Accepted min-depth baseline",
        )
        require(schedule["qubit_cap"] == baseline["logical_qubit_cap"], "Original cap and schedule")
        library = library_path(source, started)
        entries = {}
        for key in source["library_keys"]:
            budget(started)
            metadata_path = library / (key + ".json")
            require(
                relative(metadata_path, started) in frozen,
                "All actual native descriptors frozen before kernels",
            )
            entry = read(metadata_path, started)
            gate = library / entry["gate_file"]
            require(
                resolved(gate, started).parent == library and sha(gate, started) == entry["sha256"],
                "Source-owned exact gate array hash, no array execution",
            )
            require(
                relative(gate, started) in frozen,
                "All actually referenced gate bytes bound before kernels",
            )
            require(entry["key"] == key, "Exact leaf identity")
            entries[key] = entry
        for node, call in zip(nodes, source["forward_calls"], strict=True):
            budget(started)
            entry = entries[call["leaf"]]
            same(
                [node["args"], node["out"]],
                [call["args"], call["out"]],
                "Original full source/call binding",
            )
            same(
                [entry["op"], entry["params"]],
                [node["op"], node["params"]],
                "Actual leaf operation and literal parameters",
            )
        original = read(PROGRAM / "E03_support_run001" / (case + "_certificate.json"), started)
        audit = read(PROGRAM / "E03_support_audit_run002" / (case + "_audit.json"), started)
        require(
            audit["passed"] is True and audit["finite_samples_used"] is False,
            "Source-identical independent universal support",
        )
        stocks = original["stock_ids"]
        require(
            len(stocks) == assets * dates and len(set(stocks)) == len(stocks),
            "All48/416 actual original stock sites",
        )
        discovered = []
        for node in target["nodes"]:
            budget(started)
            if node["op"] != "shift":
                continue
            exponent_node = graph.node(node["args"][1])
            if exponent_node["op"] != "bits" or exponent_node["params"] != dict(
                shift=40, width=72, signed=True
            ):
                continue
            scaled_node = graph.node(exponent_node["args"][0])
            if (
                scaled_node["op"] == "cmul"
                and scaled_node["params"]["c"]
                == method["fixed_native_settings"]["inverse_ln2_word"]
            ):
                discovered.append(node["out"][0])
        same(
            sorted(stocks),
            sorted(discovered),
            "Independently discovered complete actual stock shifts",
        )
        sites = []
        for stock in stocks:
            budget(started)
            polynomial, exponent = graph.node(stock, "shift")["args"]
            reduction = graph.node(graph.node(exponent, "bits")["args"][0], "cmul")
            clipped = reduction["args"][0]
            raw = graph.clip(clipped)
            site = stock_site(graph, stock, raw, started)
            require(
                site["actual_original_support_signature"]
                == audit["actual_stock_template_signature"],
                "Exact E03 commutative template binding",
            )
            sites.append(site)
        first = sites[0]
        lo, hi, inverse, ln2 = (first[key] for key in ("low", "high", "inverse_ln2", "ln2"))
        same([lo, hi], original["clipped_log_integer_bounds"], "Original signed clamps")
        same(
            [inverse, ln2],
            [original["literal_inverse_ln2"], original["literal_ln2"]],
            "Actual source reduction words",
        )
        require(
            all(
                [site[k] for k in ("low", "high", "inverse_ln2", "ln2")] == [lo, hi, inverse, ln2]
                for site in sites
            ),
            "Whole original stock domain",
        )
        require(
            inverse > 0 and -17 <= lo * inverse // Q**2 <= hi * inverse // Q**2 <= 12,
            "Actual domain in fixed30 superset",
        )
        cells = []
        next_raw = lo
        remainders = []
        for k in range(-17, 13):
            budget(started)
            left = max(lo, ceil_fraction(Fraction(k * Q**2, inverse)))
            right = min(hi, ceil_fraction(Fraction((k + 1) * Q**2, inverse)) - 1)
            if left > right:
                cells.append(dict(k=k, empty=True, clipped_log_raw_bounds=[left, right]))
                continue
            require(
                left == next_raw and left * inverse // Q**2 == right * inverse // Q**2 == k,
                "Complete exact clipped integer cell cover",
            )
            next_raw = right + 1
            bounds = [left - k * ln2, right - k * ln2]
            signed_range(bounds)
            remainders.extend(bounds)
            cells.append(
                dict(
                    k=k,
                    empty=False,
                    clipped_log_raw_bounds=[left, right],
                    remainder_raw_bounds=bounds,
                )
            )
        require(next_raw == hi + 1, "Every clipped integer admitted once")
        this_hull = [min(remainders), max(remainders)]
        require(hull is None or this_hull == hull, "Common actual source remainder hull")
        hull = this_hull
        cases[case] = dict(
            actual_stock_sites=len(sites),
            original_joint_pairs=pairs,
            stock_sites=sites,
            clipped_log_raw_bounds=[lo, hi],
            reduction_cells=cells,
            original_13_coefficients_raw=original["literal_exp_coefficients"],
            original_support_signature=audit["actual_stock_template_signature"],
            baseline_capped_resources=schedule["resources"],
            baseline_serial_resources=source["resources"],
        )
        graphs[case], sources[case], catalogs[case], schedules[case] = (
            graph,
            source,
            entries,
            schedule,
        )
    return (
        dict(
            schema="a13-source-domain-binding-v1",
            cases=cases,
            common_remainder_raw_hull=hull,
            inverse_ln2_word=first["inverse_ln2"],
            ln2_word=first["ln2"],
            fixed30_classes_retained=True,
            generic_zero_to_ln2_domain_assumed=False,
            source_or_gate_array_executed=False,
        ),
        graphs,
        sources,
        catalogs,
        schedules,
    )


def original_baseline_certificate(mp, domain, graphs, started):
    """Certify the original actual Estrin DAG, separately from a new degree12 fit."""
    cases = {}
    for case, data in domain["cases"].items():
        budget(started, admission=True)
        graph = graphs[case]
        site = data["stock_sites"][0]
        words = data["original_13_coefficients_raw"]
        hull = domain["common_remainder_raw_hull"]
        require(
            hull[0] <= 0 <= hull[1],
            "Original zero-centered polynomial within exact source remainder hull",
        )
        fit = dict(
            segment=0,
            raw_bounds=hull,
            center_raw=0,
            local_interval=[encode(Fraction(v, Q)) for v in hull],
            coefficients_before_quantization=[encode(Fraction(v, Q)) for v in words],
            coefficient_raw=words,
        )
        certificate = segment_certificate(mp, fit, started)
        ln_error = absolute_error(domain["ln2_word"], mp.iv.log(iv(mp, 2)))
        rows = []
        maximum = Fraction(0)
        alpha_max = Fraction(0)
        for cell in data["reduction_cells"]:
            budget(started)
            k = cell["k"]
            if cell["empty"]:
                rows.append(dict(k=k, empty=True))
                continue
            left, right = cell["clipped_log_raw_bounds"]
            ranges, products = integer_stock_cell(graph, site, left, right, k, started)
            rlo, rhi = cell["remainder_raw_bounds"]
            coefficients, floors, _, steps = sparse_stock_model(
                graph, site, Fraction(max(abs(rlo), abs(rhi)), Q), started
            )
            same(
                [encode(coefficients[j]) for j in range(13)],
                [encode(Fraction(v, Q)) for v in words],
                "Exact original coefficients from actual DAG",
            )
            error_poly = exact(certificate["quantized_uniform_error_upper"]) + floors
            alpha = upper(
                mp.iv.exp(iv(mp, abs(k) * ln_error))
                * (1 + iv(mp, error_poly) * mp.iv.exp(iv(mp, Fraction(-rlo, Q))))
                - 1
            )
            reduction = upper(
                iv(mp, Fraction(2) ** k)
                * mp.iv.exp(iv(mp, Fraction(rhi, Q)))
                * (mp.iv.exp(iv(mp, abs(k) * ln_error)) - 1)
            )
            beta = EPSILON if k < 0 else Fraction(0)
            error = Fraction(2) ** k * error_poly + reduction + beta
            maximum = max(maximum, error)
            alpha_max = max(alpha_max, alpha)
            rows.append(
                dict(
                    k=k,
                    empty=False,
                    remainder_raw_bounds=[rlo, rhi],
                    original_native_intermediate_raw_bounds={
                        str(v): list(pair) for v, pair in ranges.items()
                    },
                    original_signed144_products=products,
                    actual_Estrin_floor_induction=steps,
                    native_floor_error_upper=encode(floors),
                    absolute_stock_error_upper=encode(error),
                    relative_stock_alpha_upper=encode(alpha),
                    additive_stock_beta_upper=encode(beta),
                )
            )
        cases[case] = dict(
            segment_certificate=certificate,
            intersections=rows,
            maximum_absolute_stock_error_upper=encode(maximum),
            maximum_relative_stock_alpha_upper=encode(alpha_max),
            additive_stock_beta_upper=encode(EPSILON),
        )
    return dict(
        schema="a13-original-Estrin-baseline-certificate-v1",
        degree=12,
        segments=1,
        original_source_polynomial_not_new_fit=True,
        cases=cases,
        original_eager_dead_paths_retained_in_source_cost=True,
        no_G2_allocation_or_feasibility_claim=True,
    )


RESOURCE_FIELDS = (
    "source_gates",
    "x",
    "cx",
    "ccx",
    "t_count",
    "t_depth",
    "clifford_t_depth",
    "clifford_cx",
    "clifford_h",
)


def primitive_units(entries, started):
    units = {}
    for op in ("add", "sub", "mul", "lt"):
        candidates = []
        for key, entry in entries.items():
            budget(started)
            spec = entry.get("spec", {})
            contracts = (entry.get("input_contract", {}), spec.get("input_contract", {}))
            if (
                entry["op"] != op
                or entry["params"] != {}
                or any(
                    contract and contract != {"signed_operand_bits": [72, 72]}
                    for contract in contracts
                )
                or spec.get("active_operand_bits", [72, 72]) != [72, 72]
            ):
                continue
            require(
                spec.get("width", 72) == 72 and spec.get("fraction_bits", 40) == 40,
                "Universal native W72/F40 descriptor",
            )
            require(
                len(entry["args"]) == 2 and all(len(word) == 72 for word in entry["args"]),
                "Generic full72 primitive input ABI",
            )
            require(
                len(entry["outs"]) == 1 and len(entry["outs"][0]) == 72,
                "Full72 arithmetic and zero-extended predicate output ABI",
            )
            resources = entry["resources"]
            require(
                all(type(resources[k]) is int and resources[k] >= 0 for k in RESOURCE_FIELDS),
                "Actual nonnegative exact primitive resources",
            )
            require(
                resources["t_count"] == 7 * resources["ccx"],
                "Actual exact7T primitive phase convention",
            )
            candidates.append((key, resources))
        require(candidates, "Missing source-owned generic full72 primitive")
        units[op] = dict(
            resource_upper={k: max(row[k] for _, row in candidates) for k in RESOURCE_FIELDS},
            qubits_upper=max(row["qubits"] for _, row in candidates),
            actual_leaf_keys=sorted(key for key, _ in candidates),
            componentwise_max_is_conservative=True,
        )
    return units


def removable_polynomial_calls(graph, source, sites, started):
    """Only remove unshared active polynomial values; retain every eager dead path."""
    closure = set()
    pending = [site["polynomial"] for site in sites]
    boundaries = {site["remainder"] for site in sites}
    while pending:
        budget(started)
        value = pending.pop()
        if value in boundaries or value in closure:
            continue
        node = graph.node(value)
        require(node["op"] in ("const", "add", "mul"), "Actual original active polynomial closure")
        closure.add(value)
        pending.extend(node["args"])
    boundary_users = {site["stock"] for site in sites}
    retained = set()
    for node in graph.target["nodes"]:
        budget(started)
        if node["out"][0] not in closure and node["out"][0] not in boundary_users:
            retained.update(v for v in node["args"] if v in closure)
    pending = list(retained)
    while pending:
        budget(started)
        for value in graph.node(pending.pop())["args"]:
            if value in closure and value not in retained:
                retained.add(value)
                pending.append(value)
    removed = closure - retained
    indices = [j for j, call in enumerate(source["forward_calls"]) if call["out"][0] in removed]
    require(len(indices) == len(removed), "Complete removable original call identity")
    return dict(
        active_polynomial_value_ids=sorted(closure),
        retained_shared_or_dead_ancestor_value_ids=sorted(retained),
        removed_value_ids=sorted(removed),
        removed_forward_call_indices=indices,
        eager_unused_values_outside_closure_retained=True,
    )


def resource_estimate(degree, segments, fits, domain, graphs, sources, catalogs, started):
    plan = candidate_plan(degree)
    ops = Counter(node["op"] for node in plan["nodes"])
    rows = {}
    for case, data in domain["cases"].items():
        budget(started, admission=True)
        source = sources[case]
        entries = catalogs[case]
        units = primitive_units(entries, started)
        table = [[fit["center_raw"], *fit["coefficient_raw"]] for fit in fits]
        b = segments.bit_length() - 1
        require(1 << b == segments and 0 <= b <= 3, "Fixed binary selector inventory")
        bit_counts = [sum((word % (1 << 72)).bit_count() for word in row) for row in table]
        zero_controls = sum(b - j.bit_count() for j in range(segments))
        equality_ccx_per_row = (0, 0, 2, 6)[b]
        selector_ccx = segments * equality_ccx_per_row
        selector_cx = (2 * segments if b == 1 else 0) + (sum(bit_counts) if b else 0)
        selector_x = 2 * zero_controls + (sum(bit_counts) if not b else 0)
        threshold_count = segments - 1
        threshold_raw = [fit["raw_bounds"][0] for fit in fits[1:]]
        address_toggles = sum((j ^ (j - 1)).bit_count() for j in range(1, segments))
        primitive_calls = dict(add=ops["add"], mul=ops["mul"], sub=1, lt=threshold_count)
        forward = {
            k: sum(primitive_calls[op] * units[op]["resource_upper"][k] for op in primitive_calls)
            for k in RESOURCE_FIELDS
        }
        copies = sum(2 * 2 * 72 * count for count in primitive_calls.values())
        direct_x = (
            selector_x + sum((v % (1 << 72)).bit_count() for v in threshold_raw) + threshold_count
        )
        direct_cx = selector_cx + address_toggles + copies
        direct_ccx = selector_ccx
        forward["x"] += direct_x
        forward["cx"] += direct_cx
        forward["ccx"] += direct_ccx
        forward["source_gates"] += direct_x + direct_cx + direct_ccx
        forward["t_count"] += 7 * direct_ccx
        forward["t_depth"] += 7 * direct_ccx
        forward["clifford_cx"] += direct_cx + 6 * direct_ccx
        forward["clifford_h"] += 2 * direct_ccx
        forward["clifford_t_depth"] += direct_x + direct_cx + 15 * direct_ccx
        clean = {k: 2 * v for k, v in forward.items()}
        clean["cx"] += 72
        clean["source_gates"] += 72
        clean["clifford_cx"] += 72
        clean["clifford_t_depth"] += 72
        for field in ("cx", "source_gates", "clifford_cx", "clifford_t_depth"):
            clean[field] += 144
        # Separate full72 banks for every changed SSA and selector/table word.
        ssa_words = (
            len(plan["nodes"])
            + 2
            + threshold_count
            + (1 if b else 0)
            + (degree + 2)
            + threshold_count
        )
        scratch = max(
            row["qubits_upper"]
            - len(entries[row["actual_leaf_keys"][0]]["args"]) * 72
            - len(entries[row["actual_leaf_keys"][0]]["outs"][0])
            for row in units.values()
        )
        private = max(scratch, 2 * max(0, b - 2))
        function_qubits = 72 * (ssa_words + 2) + private
        removal = removable_polynomial_calls(graphs[case], source, data["stock_sites"], started)
        removed = set(removal["removed_forward_call_indices"])
        removed_leaf = {k: 0 for k in RESOURCE_FIELDS}
        removed_copies = 0
        unchanged_depth = 0
        for j, call in enumerate(source["forward_calls"]):
            budget(started)
            entry = entries[call["leaf"]]
            if j in removed:
                for k in RESOURCE_FIELDS:
                    removed_leaf[k] += entry["resources"][k]
                removed_copies += 2 * len(call["args"]) * 72
            else:
                unchanged_depth += entry["resources"]["t_depth"]
        sites = data["actual_stock_sites"]
        estimated = {
            k: source["resources"][k] - 2 * removed_leaf[k] + 2 * sites * clean[k]
            for k in RESOURCE_FIELDS
        }
        estimated["cx"] -= 2 * removed_copies
        estimated["source_gates"] -= 2 * removed_copies
        estimated["clifford_cx"] -= 2 * removed_copies
        estimated["t_depth"] = 2 * unchanged_depth + 2 * sites * clean["t_depth"]
        # Start at the original full serial allocation; infer no storage savings.
        estimated_qubits = (
            source["resources"]["logical_qubits"]
            + sites * 72 * ssa_words
            + max(0, private - source["resources"]["max_reused_scratch_qubits"])
        )
        require(
            all(v >= 0 for v in estimated.values()), "Nonnegative complete whole-source estimate"
        )
        rows[case] = dict(
            primitive_units=units,
            coefficient_QROM_rows_raw=table,
            coefficient_QROM_rows_unsigned72=[[v % (1 << 72) for v in row] for row in table],
            primitive_forward_calls=primitive_calls,
            threshold_raw=threshold_raw,
            selector=dict(
                address_bits=b,
                threshold_count=threshold_count,
                address_toggle_CX=address_toggles,
                equality_compute_uncompute_CCX=selector_ccx,
                equality_CX=2 * segments if b == 1 else 0,
                address_inversion_X=2 * zero_controls,
                table_data_controlled_CX=sum(bit_counts) if b else 0,
                table_constant_X=sum(bit_counts) if not b else 0,
            ),
            full72_argument_copy_CX_per_forward=copies,
            dirty_output_XOR_CX=72,
            outer_function_argument_copy_CX_per_clean_invocation=144,
            function_forward_resource_estimate=forward,
            function_clean_resource_estimate=clean,
            whole_candidate_clean_invocations=2 * sites,
            global_forward_and_inverse_each_use_clean_candidate=True,
            function_full72_SSA_words=ssa_words,
            function_private_scratch_qubits=private,
            full72_bank_inventory=dict(
                candidate_IR_values=len(plan["nodes"]),
                raw_remainder_bank=1,
                outer_argument_copy_bank=1,
                threshold_constant_banks=threshold_count,
                threshold_predicate_banks=threshold_count,
                selector_address_banks=1 if b else 0,
                QROM_center_and_coefficient_banks=degree + 2,
                external_input_output_banks=2,
            ),
            function_logical_qubit_upper=function_qubits,
            original_polynomial_removal=removal,
            original_removed_leaf_forward_resources=removed_leaf,
            original_removed_argument_copy_CX=removed_copies,
            whole_source_resource_estimate=estimated,
            whole_source_logical_qubit_upper=estimated_qubits,
            original_capped_source_resources=data["baseline_capped_resources"],
            original_serial_source_resources=data["baseline_serial_resources"],
            original_logical_qubit_cap=data["baseline_capped_resources"]["logical_qubits"],
            estimated_qubit_upper_within_cap=estimated_qubits
            <= data["baseline_capped_resources"]["logical_qubits"],
            estimated_serial_depth_not_realized_capped_schedule=True,
            exact7T_phase_paid=True,
            relative_phase_substitution=False,
            dynamic_selected_coefficient_constant_multiplier_discount=False,
            all_costs_are_estimates_until_emitted_ABI_and_capped_schedule_proofs=True,
        )
    return dict(
        schema="a13-symbolic-resource-estimate-v1",
        degree=degree,
        segments=segments,
        cases=rows,
        arbitrary_phase_clean_XOR_ABI_still_requires_emitted_proof=True,
        old_dead_paths_preserved=True,
        full_financial_cost_not_divided_by_coordinates=True,
        resource_adoption_or_realized_improvement_claim=False,
    )


def prepare(output):
    started = process_started()
    frozen, external = {}, {}
    created = False
    try:
        setup(started)
        require(output == OUTPUT and not output.exists(), "Exclusive fresh A13 receipt, no retry")
        require("mpmath" not in sys.modules, "Stdlib-only preparation, no fitting or source walk")
        policy = implementation_policy(started)
        method, origins = selected_inputs(policy, frozen, external, started)
        interpreter = runtime(frozen, external, started)
        runtime_policy(interpreter, started)
        verify_loaded(frozen, external, started)
        verify(frozen, external, started)
        budget(started, admission=True)
        output.mkdir()
        created = True
        (output / "executed_code").mkdir()
        (output / "rows").mkdir()
        for path in (PRODUCER, AUDITOR, IMPLEMENTATION, IMPLEMENTATION_DOC, METHOD, METHOD_DOC):
            copy_exact(path, output / "executed_code" / path.name, frozen, external, started)
        save(output / "selected_source_origins.json", origins, started)
        save(output / "interpreter.json", interpreter, started)
        verified = final_verify(frozen, external, started)
        budget(started, admission=True)
        protocol = dict(
            schema="a13-exp-frontier-protocol-v1",
            output=output.relative_to(ROOT).as_posix(),
            prepared_UTC=datetime.now(timezone.utc).isoformat(),
            producer_module="research.limitation_program_20261001.experiment_exp_frontier",
            author_sha256=policy["author_sha256"],
            method_document_SHA256=policy["method_document_SHA256"],
            A07_manifest_SHA256=policy["A07_manifest_SHA256"],
            selected_source_SHA256=method["selected_existing_manifest_expected_pins"],
            CPU_admission_wall_seconds=[CPU, ADMISSION, WALL],
            primary_digits=90,
            independent_digits=130,
            process_CPU_seconds=CPU,
            admission_process_CPU_seconds=ADMISSION,
            wall_seconds=WALL,
            threads=1,
            new_fixture_credit=0,
            startup_B_required=True,
            pure_Python_mpmath_backend_required=True,
            fixed_grid=policy["fixed_grid"],
            candidate_G2_absolute_stock_error_allocation=None,
            candidate_G2_barrier_band_allocation=None,
            gate_emission_authorized=False,
            interpreter=interpreter,
            frozen_inputs=frozen,
            external_runtime_inputs=external,
            final_fresh_preparation_verified_paths=verified,
            preparation_budget=elapsed(started),
            actual_process_creation_FILETIME_ticks=_PROCESS_CREATION_TICKS,
            all_process_CPU_and_creation_wall_charged=True,
            no_fit_bound_source_walk_gate_or_sample_executed_in_prepare=True,
        )
        save(output / "protocol.json", protocol, started)
        save(
            output / "PREPARED_RECEIPT.json",
            dict(
                prepared=True,
                terminal=False,
                protocol_sha256=sha(output / "protocol.json", started),
                preparation_budget=elapsed(started),
                no_numeric_result_claim=True,
            ),
            started,
        )
        budget(started)
        return protocol
    except BaseException as error:
        if created:
            retain_failure(output, frozen, external, started, error, "prepare")
        raise


def run(output):
    started = process_started()
    frozen, external = {}, {}
    admitted = False
    try:
        setup(started)
        require(output == OUTPUT and output.is_dir(), "Exact prepared A13 producer receipt")
        require(
            not any(
                (output / name).exists()
                for name in (
                    "manifest.json",
                    "completion_outcome.json",
                    "FAILED_UNSEALED.json",
                    "failure.json",
                    "run_started.json",
                )
            ),
            "No reused/partial/failed run",
        )
        admitted = True
        protocol = read(output / "protocol.json", started)
        prepared = read(output / "PREPARED_RECEIPT.json", started)
        require(
            prepared["prepared"] is True
            and prepared["terminal"] is False
            and sha(output / "protocol.json", started) == prepared["protocol_sha256"],
            "Actual immutable prepared protocol",
        )
        require(protocol["schema"] == "a13-exp-frontier-protocol-v1", "Exact prepared A13 schema")
        same(
            protocol["CPU_admission_wall_seconds"],
            [CPU, ADMISSION, WALL],
            "Fixed whole twenty-row run budget",
        )
        require(
            protocol["primary_digits"] == 90
            and protocol["independent_digits"] == 130
            and protocol["threads"] == 1
            and protocol["new_fixture_credit"] == 0
            and protocol["startup_B_required"] is True
            and protocol["pure_Python_mpmath_backend_required"] is True
            and protocol["candidate_G2_absolute_stock_error_allocation"] is None
            and protocol["candidate_G2_barrier_band_allocation"] is None
            and protocol["gate_emission_authorized"] is False,
            "Same exploratory precision/runtime/scope",
        )
        for field, is_external in (("frozen_inputs", False), ("external_runtime_inputs", True)):
            require(type(protocol[field]) is dict, "Complete immutable preparation maps")
            for key, expected in protocol[field].items():
                budget(started)
                require(
                    type(key) is str and Path(key).is_absolute() is is_external,
                    "Canonical ROOT/external map key convention",
                )
                actual = bind(
                    frozen, external, Path(key) if is_external else ROOT / key, expected, started
                )
                require(
                    (str(actual) if is_external else actual.relative_to(ROOT).as_posix()) == key,
                    "Canonical prepared key identity",
                )
        for name in (
            "protocol.json",
            "PREPARED_RECEIPT.json",
            "selected_source_origins.json",
            "interpreter.json",
        ):
            bind(frozen, external, output / name, sha(output / name, started), started)
        policy = implementation_policy(started)
        same(
            policy["author_sha256"],
            protocol["author_sha256"],
            "Same reviewed primary and independent bytes",
        )
        same(
            policy["method_document_SHA256"],
            protocol["method_document_SHA256"],
            "Same held method pins",
        )
        same(policy["fixed_grid"], protocol["fixed_grid"], "Same twenty frozen architectures")
        require(
            policy["A07_manifest_SHA256"] == protocol["A07_manifest_SHA256"],
            "Same actual A07 owner pin",
        )
        method, origins = selected_inputs(policy, frozen, external, started)
        same(
            origins,
            read(output / "selected_source_origins.json", started),
            "Complete strict original owner routes",
        )
        same(
            method["selected_existing_manifest_expected_pins"],
            protocol["selected_source_SHA256"],
            "Same selected historical byte expectations",
        )
        interpreter = read(output / "interpreter.json", started)
        same(interpreter, protocol["interpreter"], "Prepared actual runtime record")
        runtime_policy(interpreter, started)
        verify_loaded(frozen, external, started)
        verify(frozen, external, started)
        budget(started, admission=True)
        save(
            output / "run_started.json",
            dict(
                UTC=datetime.now(timezone.utc).isoformat(),
                process_id=os.getpid(),
                limits=[CPU, ADMISSION, WALL],
            ),
            started,
        )
        require("mpmath" not in sys.modules, "Deferred numerical import after all bytes frozen")
        import mpmath as mp

        require(
            mp.__version__ == "1.3.0" and sys.modules["mpmath.libmp.backend"].BACKEND == "python",
            "Actual pure-Python fixed mpmath backend",
        )
        mp.mp.dps = 90
        mp.iv.dps = 90
        verify_loaded(frozen, external, started)
        budget(started, admission=True)
        domain, graphs, sources, catalogs, _ = source_domain_binding(
            method, frozen, external, started
        )
        save(output / "source_domain_binding.json", domain, started)
        inventory_record = dict(
            schema="a13-fixed-inventory-v1",
            rows=[
                dict(degree=d, segments=s, row_id=f"d{d}_s{s}") for d in DEGREES for s in SEGMENTS
            ],
            separate_original_baseline=dict(
                degree=12, segments=1, new_degree12_fit_is_not_original_baseline=True
            ),
            no_adaptive_degrees_segments_or_precision=True,
        )
        save(output / "fixed_inventory.json", inventory_record, started)
        baseline = original_baseline_certificate(mp, domain, graphs, started)
        save(output / "original_baseline_certificate.json", baseline, started)
        fits_rows = []
        certificate_rows = []
        resource_rows = []
        statuses = []
        for degree in DEGREES:
            for segments in SEGMENTS:
                budget(started, admission=True)
                identity = dict(degree=degree, segments=segments, row_id=f"d{degree}_s{segments}")
                stage = "fit"
                fits = []
                try:
                    for segment in segment_inventory(domain["common_remainder_raw_hull"], segments):
                        budget(started, admission=True)
                        fits.append(fit_segment(mp, degree, segment, started))
                    stage = "certificate"
                    certificate = architecture_certificate(
                        mp, degree, segments, fits, domain, started
                    )
                    stage = "resource"
                    resource = resource_estimate(
                        degree, segments, fits, domain, graphs, sources, catalogs, started
                    )
                except BudgetCensoredError:
                    raise
                except (MathematicalGuardError, ValueError, ZeroDivisionError) as error:
                    # Rejected row: no bound credit, alternate fitter or retry.
                    status = (
                        "FIT_FAILED"
                        if stage == "fit"
                        else "CERTIFICATE_REJECTED"
                        if stage == "certificate"
                        else "RESOURCE_REJECTED"
                    )
                    row = dict(
                        **identity,
                        status=status,
                        failed_stage=stage,
                        error_type=type(error).__name__,
                        error=str(error),
                        retained_completed_segment_fits=fits,
                        no_uniform_certificate_claim=True,
                        no_resource_improvement_claim=True,
                        no_alternate_fitter_retry_or_new_choice=True,
                    )
                    fits_rows.append(
                        dict(
                            **identity,
                            status=status,
                            segment_fits=fits,
                            error_type=type(error).__name__,
                            error=str(error),
                        )
                    )
                    statuses.append(dict(**identity, status=status))
                    save(output / "rows" / (identity["row_id"] + ".json"), row, started)
                    continue
                row = dict(
                    **identity,
                    status="CERTIFIED_ESTIMATE",
                    fit=dict(segment_fits=fits),
                    certificate=certificate,
                    resource_estimate=resource,
                )
                fits_rows.append(dict(**identity, status=row["status"], segment_fits=fits))
                certificate_rows.append(
                    dict(**identity, status=row["status"], certificate=certificate)
                )
                resource_rows.append(
                    dict(**identity, status=row["status"], resource_estimate=resource)
                )
                statuses.append(dict(**identity, status=row["status"]))
                save(output / "rows" / (identity["row_id"] + ".json"), row, started)
        require(len(statuses) == 20, "Every fixed row retained exactly once")
        save(
            output / "coefficient_fit_diagnostics.json",
            dict(
                schema="a13-fit-diagnostics-v1",
                rows=fits_rows,
                round32_solve_is_final=True,
                no_extra33rd_solve=True,
                no_optimality_claim=True,
            ),
            started,
        )
        save(
            output / "exponential_approximation_certificate.json",
            dict(
                schema="a13-approximation-certificate-v1",
                rows=certificate_rows,
                original_baseline_file="original_baseline_certificate.json",
                all_uniform_bounds_are_Bernstein_not_mesh=True,
                relative_alpha_and_negative_shift_beta_separate=True,
            ),
            started,
        )
        save(
            output / "function_frontier.json",
            dict(
                schema="a13-function-frontier-v1",
                rows=resource_rows,
                fixed_row_statuses=statuses,
                all_costs_symbolic_estimates=True,
                candidate_G2_absolute_stock_error_allocation=None,
                candidate_G2_barrier_band_allocation=None,
                feasible_candidates_not_selected=True,
                gate_emission_authorized=False,
                original_capped_baseline_resources={
                    case: data["baseline_capped_resources"]
                    for case, data in domain["cases"].items()
                },
            ),
            started,
        )
        runtime_policy(interpreter, started)
        save(
            output / "loaded_module_origins.json", verify_loaded(frozen, external, started), started
        )
        certified = sum(row["status"] == "CERTIFIED_ESTIMATE" for row in statuses)
        summary = dict(
            schema="a13-exp-frontier-summary-v1",
            completed=True,
            passed=True,
            rejection=False,
            budget_censored=False,
            status="completed_exploratory_fixed_screen",
            scientific_screen_complete=True,
            fixed_architecture_rows=20,
            certified_estimate_rows=certified,
            retained_rejected_rows=20 - certified,
            all20_uniformly_certified=certified == 20,
            fixed_row_statuses=statuses,
            candidate_G2_absolute_stock_error_allocation=None,
            candidate_G2_barrier_band_allocation=None,
            original_baseline_separate=True,
            new_test_credit=0,
            new_gate_replays=0,
            new_price_samples=0,
            full_G2=False,
            adoption=False,
            cost_transfer=False,
            gate_emission_authorized=False,
            feasible_architecture_or_realized_cost_improvement_claim=False,
            source_expected_hashes_waived=False,
            independent_audit_still_required=True,
            budget=elapsed(started),
        )
        save(output / "summary.json", summary, started)
        seal(
            output,
            frozen,
            external,
            started,
            dict(
                completed=True,
                passed=True,
                rejection=False,
                budget_censored=False,
                phase="run",
                status=summary["status"],
                summary_file="summary.json",
                scientific_screen_complete=True,
            ),
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
    require(output == OUTPUT, "Only exact prospective A13 producer receipt")
    result = prepare(output) if args.operation == "prepare" else run(output)
    print(
        json.dumps(
            dict(
                operation=args.operation,
                output=output.relative_to(ROOT).as_posix(),
                prepared=args.operation == "prepare",
                passed=result.get("passed"),
                new_test_credit=0,
            )
        )
    )


if __name__ == "__main__":
    main()
