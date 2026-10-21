"""Strict metadata-only retention of untrusted A13 run002 material.

This module never fits, imports numerical modules, walks financial SSA or
authorizes mathematical claims. Only a fresh independent auditor can certify
the retained twenty-row material. The original FAILED_UNSEALED stays failed.
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
OUTPUT = PROGRAM / "A13_recovery_run001"
PRODUCER = RESEARCH / "experiment_exp_frontier_recovery.py"
AUDITOR = RESEARCH / "audit_exp_frontier_recovery.py"
METHOD = RESEARCH / "a13_exp_frontier_preflight.json"
METHOD_DOC = RESEARCH / "A13_EXP_FRONTIER_PREFLIGHT.md"
IMPLEMENTATION = RESEARCH / "a13_exp_frontier_recovery_implementation_preflight.json"
IMPLEMENTATION_DOC = RESEARCH / "A13_EXP_FRONTIER_RECOVERY_IMPLEMENTATION_PREFLIGHT.md"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
METHOD_SHA = "6c0e97f33e1277c070e6e84883b6631a880997becd214772bb9ef287e1c7ba85"
METHOD_DOC_SHA = "f5b4404650c1ee9bd3a8ef2557d67e1340dda0fc059d94126e19fcfc046d7f7b"
CPU, ADMISSION, WALL = 300, 270, 900
PRIOR_A13_FAILURE = PROGRAM / "A13_run001"
PRIOR_A13_REVIEW = PROGRAM / "A13_exp_frontier_root_review_run001"
PRIOR_A13_FAILURE_SHA = "d77077cfb2d67ee2973a02b236ea6e6b2336962f35fed6ce4aeb48ef8bb65aa8"
PRIOR_A13_REVIEW_SHA = "744e04e887ef94a218004845a8655014389cc2f4cf5d4d41153c352d7db4ebce"
PRIOR_A13_AUTHORS = {
    "experiment_exp_frontier.py": (
        "0fff55c681f3ecf0dca8cd8e50f4f20be1b276e6c7481a651ede5cd90661a78e"
    ),
    "audit_exp_frontier.py": ("3385268148620aa1618452bdd14d678eed9c457f327d0c59fcbb04cabebae93a"),
    "A13_EXP_FRONTIER_IMPLEMENTATION_PREFLIGHT.md": (
        "5aa7ace3c45c3c0734e933624b321d7b575de3d38ba206b73a27b92db41649e3"
    ),
    "a13_exp_frontier_implementation_preflight.json": (
        "08658b0283b293337c5e9965f37aff1643e21873fec99a9962fc2b9c392cee59"
    ),
}
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
    banned = ("mpmath", "numpy", "scipy", "numba", "llvmlite", "qiskit", "gmpy", "gmpy2", "sage")
    found = [
        name
        for name in sys.modules
        if any(name == prefix or name.startswith(prefix + ".") for prefix in banned)
        or (
            name.startswith("research.")
            and name
            not in (
                "research.limitation_program_20261001.experiment_exp_frontier_recovery",
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
        schema="a13-exp-frontier-recovery-terminal-manifest-v1",
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
                    budget_censored=None,
                    hard_budget_state_uncertified=True,
                    phase=phase,
                    original_error_type=type(error).__name__,
                    retention_error_type=type(retention_error).__name__,
                    elapsed=elapsed(started),
                    new_test_credit=0,
                    partial_summary_or_manifest_is_not_terminal_success=True,
                    requires_fresh_version_and_receipt=True,
                ),
            )


MATERIAL = PROGRAM / "A13_run002"
CAPTURE = PROGRAM / "A13_terminal_failure_capture_run002"
RECOVERY_METHOD = RESEARCH / "a13_exp_frontier_recovery_preflight.json"
RECOVERY_METHOD_DOC = RESEARCH / "A13_EXP_FRONTIER_RECOVERY_PREFLIGHT.md"
V2_REVIEW = PROGRAM / "A13_exp_frontier_root_review_run002"
V2_REVIEW_SHA = "6834a90acb76a5489f3fac66ce874adf81357692ba2bade7cd709455846626e3"
CAPTURE_SHA = "20126972220fc8ae35aae71e789e96b4dde6b755b9c692c97b4e89dfdb9285c3"
V2_AUTHORS = {
    "experiment_exp_frontier_v2.py": (
        "2c3d0f17c0c6b3789071ef85c31c1f8e69957fe71768bde0877b134196a3575a"
    ),
    "audit_exp_frontier_v2.py": "df66aa45c223837e820a0cf720cd112db42aacdbf87817f58139b1ce57a404f5",
    "A13_EXP_FRONTIER_IMPLEMENTATION_PREFLIGHT_V2.md": (
        "b3e5d7443ed753ecbf577a305a61ef946a18689f00629be12bbd16f20716a038"
    ),
    "a13_exp_frontier_implementation_preflight_v2.json": (
        "de40e3d7ba0def85f4b7d1b1e7bd9d06005524517feb52eca5dcaff587f41c0f"
    ),
}


def recovery_policy(frozen, external, started):
    policy = read(IMPLEMENTATION, started)
    require(
        policy["schema"] == "a13-exp-frontier-recovery-implementation-preflight-v1",
        "Exact independently reviewed recovery implementation",
    )
    same(policy["CPU_admission_wall_seconds"], [CPU, ADMISSION, WALL], "Unchanged budgets")
    same(policy["owned_caps_files_bytes"], [64, 128 * 1024**2], "Unchanged own output caps")
    same(policy["fixed_grid"], [[d, s] for d in DEGREES for s in SEGMENTS], "Exactly20 rows")
    require(
        policy["threads"] == 1
        and policy["primary_digits"] == 90
        and policy["independent_digits"] == 130
        and policy["new_fixture_credit"] == 0,
        "Original precision and zero-credit scope",
    )
    require(
        policy["candidate_G2_absolute_stock_error_allocation"] is None
        and policy["candidate_G2_barrier_band_allocation"] is None
        and policy["gate_emission_authorized"] is False,
        "No allocation or adoption release",
    )
    same(policy["prior_A13_v2_author_SHA256"], V2_AUTHORS, "Immutable v2 author quartet")
    same(policy["prior_A13_author_SHA256"], PRIOR_A13_AUTHORS, "Immutable v1 author quartet")
    require(
        policy["prior_A13_failed_receipt_manifest_SHA256"] == PRIOR_A13_FAILURE_SHA
        and policy["prior_A13_root_review_manifest_SHA256"] == PRIOR_A13_REVIEW_SHA
        and policy["prior_A13_v2_root_review_manifest_SHA256"] == V2_REVIEW_SHA,
        "Exact prior failure and reviews",
    )
    same(
        policy["original_method_document_SHA256"],
        {
            METHOD.name: METHOD_SHA,
            METHOD_DOC.name: METHOD_DOC_SHA,
        },
        "Original mathematical method remains immutable",
    )
    capture_sha = policy["capture_manifest_SHA256"]
    require(
        capture_sha == CAPTURE_SHA,
        "Actual sealed capture pin required before prepare",
    )
    same(
        [policy["recovery_source_receipt"], policy["recovery_audit_receipt"]],
        [
            OUTPUT.relative_to(ROOT).as_posix(),
            (PROGRAM / "A13_recovery_audit_run001").relative_to(ROOT).as_posix(),
        ],
        "Exact fresh metadata and independent audit routes",
    )
    require(
        policy["previous_failed_A13_credit"] == 0,
        "Original failed attempts receive no recovery credit",
    )
    same(
        sorted(policy["author_sha256"]),
        sorted([PRODUCER.name, AUDITOR.name]),
        "Exactly two recovery executables",
    )
    same(
        sorted(policy["method_document_SHA256"]),
        sorted([RECOVERY_METHOD.name, RECOVERY_METHOD_DOC.name]),
        "Exactly two independently pinned recovery method files",
    )
    for name, expected in {
        **policy["author_sha256"],
        **policy["method_document_SHA256"],
        **policy["original_method_document_SHA256"],
        **V2_AUTHORS,
        **PRIOR_A13_AUTHORS,
    }.items():
        budget(started)
        bind(frozen, external, RESEARCH / name, expected, started)
    for path in (IMPLEMENTATION, IMPLEMENTATION_DOC):
        bind(frozen, external, path, sha(path, started), started)
    method = read(RECOVERY_METHOD, started)
    require(
        method["schema"] == "a13-exp-frontier-recovery-author-preflight-v1",
        "Held finite recovery method",
    )
    return policy


def strict_owner(path, expected, frozen, external, started):
    """Bind every recognized own/frozen/external map; never infer success."""
    actual = bind(frozen, external, path, expected, started)
    require(
        actual == Path(path).absolute() and actual.is_relative_to(PROGRAM),
        "Canonical exact receipt manifest without alias",
    )
    data = read(actual, started)
    require(
        data.get("manifest_self_hash_excluded") is True, "Explicit manifest self-hash exclusion"
    )
    require(
        type(data.get("files")) is dict and type(data.get("frozen_inputs")) is dict,
        "Complete recognized nested maps",
    )
    owned = set()
    for field in ("files", "frozen_inputs", "external_runtime_inputs"):
        mapping = data.get(field, {})
        require(type(mapping) is dict, "Exact owner map type")
        for key, wanted in mapping.items():
            budget(started)
            require(
                type(key) is str and type(wanted) is str and len(wanted) == 64,
                "Exact original SHA-map reference",
            )
            if field == "external_runtime_inputs":
                candidate = Path(key)
                require(candidate.is_absolute(), "Actual external absolute runtime path")
            else:
                require(
                    not Path(key).is_absolute() and "\\" not in key and ".." not in key.split("/"),
                    "Canonical ROOT or receipt-relative reference",
                )
                candidate = (
                    ROOT / key
                    if field == "frozen_inputs"
                    or key.startswith(
                        ("results/", "research/", ".context/", "docs/", "manuscript/")
                    )
                    else actual.parent / key
                )
            observed = resolved(candidate, started)
            if field != "external_runtime_inputs":
                require(
                    observed.is_relative_to(ROOT), "ROOT-relative map cannot admit external bytes"
                )
                canonical_key = (
                    observed.relative_to(ROOT).as_posix()
                    if field == "frozen_inputs"
                    or key.startswith(
                        ("results/", "research/", ".context/", "docs/", "manuscript/")
                    )
                    else observed.relative_to(actual.parent).as_posix()
                )
                require(key == canonical_key, "Exact canonical original map spelling")
            else:
                require(
                    not observed.is_relative_to(ROOT) and str(observed) == key,
                    "Separate exact canonical external runtime map",
                )
            bind(frozen, external, observed, wanted, started)
            if field == "files":
                require(
                    observed.is_relative_to(actual.parent) and observed != actual,
                    "Owned reference escapes receipt or hashes manifest itself",
                )
                owned.add(observed)
            budget(started)
    observed_owned = set()
    for candidate in actual.parent.rglob("*"):
        budget(started)
        if candidate.is_file():
            item = resolved(candidate, started)
            require(item == candidate.absolute(), "No owned byte path alias")
            observed_owned.add(item)
    same(
        sorted(map(str, observed_owned)),
        sorted(map(str, owned | {actual})),
        "Exact immutable original owned directory membership",
    )
    return data


def material_packet(policy, frozen, external, started):
    capture = strict_owner(
        CAPTURE / "manifest.json", policy["capture_manifest_SHA256"], frozen, external, started
    )
    require(len(capture["files"]) == 3, "Actual diagnostic three metadata outputs")
    summary = read(CAPTURE / "summary.json", started)
    require(
        summary["schema"] == "failed-a13-metadata-capture-v1"
        and summary["passed"] is True
        and summary["diagnostic_integrity"] is True
        and summary["original_attempt_failed"] is True
        and summary["original_partial_success_invalid"] is True
        and summary["original_receipt"] == MATERIAL.relative_to(ROOT).as_posix()
        and summary["original_owned_files"] == 42
        and summary["original_owned_bytes"] == 243935317,
        "Capture certifies bytes of a failed original attempt, never mathematics",
    )
    require(not (MATERIAL / "manifest.json").exists(), "No original terminal manifest fabricated")
    require(not (PROGRAM / "A13_audit_run002").exists(), "Original independent audit not executed")
    marker = read(MATERIAL / "FAILED_UNSEALED.json", started)
    same(marker, summary["original_failure_marker"], "Authoritative original marker bytes")
    require(
        marker["failed"] is True
        and marker["passed"] is False
        and marker["completed"] is False
        and marker["budget_censored"] is True
        and marker["original_error_type"] == marker["retention_error_type"] == "ValueError"
        and marker["new_test_credit"] == 0
        and marker["partial_summary_or_manifest_is_not_terminal_success"] is True,
        "Retain original unsealed terminal classification exactly",
    )
    index = read(CAPTURE / "frozen_reference_index.json", started)
    require(type(index) is dict and len(index) == 42, "All42 original byte references")
    same(sorted(index), sorted(summary["preserved_members"]), "Capture/index member equality")
    actual_members, files = set(), {}
    for candidate in MATERIAL.rglob("*"):
        budget(started)
        if candidate.is_file():
            actual = resolved(candidate, started)
            require(
                actual == candidate.absolute() and actual.is_relative_to(MATERIAL),
                "Original material byte confinement without alias",
            )
            actual_members.add(actual.relative_to(ROOT).as_posix())
    same(sorted(actual_members), sorted(index), "Exactly all original42 retained files")
    for key, expected in sorted(index.items()):
        budget(started)
        require(
            capture["frozen_inputs"].get(key) == expected, "Each material original owner binding"
        )
        actual = bind(frozen, external, ROOT / key, expected, started)
        name = actual.relative_to(MATERIAL).as_posix()
        files[name] = dict(ROOT_relative_path=key, sha256=expected, bytes=actual.stat().st_size)
    require(
        sum(row["bytes"] for row in files.values()) == summary["original_owned_bytes"],
        "Complete actual retained byte count",
    )
    protocol = read(MATERIAL / "protocol.json", started)
    require(
        protocol["schema"] == "a13-exp-frontier-protocol-v1"
        and protocol["operational_A13_version"] == 2,
        "Actual original preparation schema",
    )
    same(
        protocol["author_sha256"],
        {
            name: V2_AUTHORS[name]
            for name in (
                "experiment_exp_frontier_v2.py",
                "audit_exp_frontier_v2.py",
            )
        },
        "Actual immutable original scientific authors",
    )
    same(
        protocol["CPU_admission_wall_seconds"], [CPU, ADMISSION, WALL], "Original budgets retained"
    )
    same(protocol["fixed_grid"], policy["fixed_grid"], "All20 original fixed architectures")
    for field in ("frozen_inputs", "external_runtime_inputs"):
        require(type(protocol[field]) is dict, "Complete original prepared input map")
        for key, expected in protocol[field].items():
            budget(started)
            require(
                capture[field].get(key) == expected, "Full original protocol map in capture union"
            )
            bind(
                frozen,
                external,
                ROOT / key if field == "frozen_inputs" else Path(key),
                expected,
                started,
            )
    for key in V2_AUTHORS:
        bind(frozen, external, MATERIAL / "executed_code" / key, V2_AUTHORS[key], started)
    strict_owner(V2_REVIEW / "manifest.json", V2_REVIEW_SHA, frozen, external, started)
    strict_owner(
        PRIOR_A13_FAILURE / "manifest.json", PRIOR_A13_FAILURE_SHA, frozen, external, started
    )
    strict_owner(
        PRIOR_A13_REVIEW / "manifest.json", PRIOR_A13_REVIEW_SHA, frozen, external, started
    )
    return dict(
        schema="a13-exp-frontier-untrusted-material-inventory-v1",
        material_receipt=MATERIAL.relative_to(ROOT).as_posix(),
        capture_manifest_SHA256=policy["capture_manifest_SHA256"],
        original_terminal_failure_authoritative=True,
        original_manifest_absent=True,
        original_independent_audit_absent=True,
        exact_file_count=42,
        original_file_bytes=summary["original_owned_bytes"],
        files=files,
        scientific_claims_trusted=False,
        audit_required_all20=True,
        original_summary_and_completion_are_not_authoritative=True,
        original_mathematics_refitted_or_reexecuted=False,
    )


def prepare(output):
    started = process_started()
    frozen, external, created = {}, {}, False
    try:
        setup(started)
        forbidden_imports()
        require(output == OUTPUT and not output.exists(), "Fresh exact metadata recovery output")
        policy = recovery_policy(frozen, external, started)
        material = material_packet(policy, frozen, external, started)
        interpreter = runtime(frozen, external, started)
        runtime_policy(interpreter, started)
        verify_loaded(frozen, external, started)
        verified = final_verify(frozen, external, started)
        budget(started, admission=True)
        output.mkdir()
        created = True
        (output / "executed_code").mkdir()
        for path in (
            PRODUCER,
            AUDITOR,
            IMPLEMENTATION,
            IMPLEMENTATION_DOC,
            RECOVERY_METHOD,
            RECOVERY_METHOD_DOC,
            METHOD,
            METHOD_DOC,
        ):
            copy_exact(path, output / "executed_code" / path.name, frozen, external, started)
        save(output / "material_inventory.json", material, started)
        save(output / "interpreter.json", interpreter, started)
        verified = final_verify(frozen, external, started)
        budget(started, admission=True)
        protocol = dict(
            schema="a13-exp-frontier-recovery-protocol-v1",
            output=output.relative_to(ROOT).as_posix(),
            producer_module="research.limitation_program_20261001.experiment_exp_frontier_recovery",
            author_sha256=policy["author_sha256"],
            original_author_sha256={
                name: V2_AUTHORS[name]
                for name in ("experiment_exp_frontier_v2.py", "audit_exp_frontier_v2.py")
            },
            prior_A13_v2_author_SHA256=V2_AUTHORS,
            prior_A13_author_SHA256=PRIOR_A13_AUTHORS,
            prior_A13_failed_receipt_manifest_SHA256=PRIOR_A13_FAILURE_SHA,
            prior_A13_root_review_manifest_SHA256=PRIOR_A13_REVIEW_SHA,
            prior_A13_v2_root_review_manifest_SHA256=V2_REVIEW_SHA,
            original_material_receipt=MATERIAL.relative_to(ROOT).as_posix(),
            capture_manifest_SHA256=policy["capture_manifest_SHA256"],
            method_document_SHA256=policy["method_document_SHA256"],
            original_method_document_SHA256=policy["original_method_document_SHA256"],
            A07_manifest_SHA256=policy["A07_manifest_SHA256"],
            CPU_admission_wall_seconds=[CPU, ADMISSION, WALL],
            primary_digits=90,
            independent_digits=130,
            threads=1,
            new_fixture_credit=0,
            fixed_grid=policy["fixed_grid"],
            owned_caps_files_bytes=[64, 128 * 1024**2],
            candidate_G2_absolute_stock_error_allocation=None,
            candidate_G2_barrier_band_allocation=None,
            gate_emission_authorized=False,
            candidate_material_untrusted=True,
            independent130_validation_required=True,
            no_fit_bound_source_walk_gate_or_sample_executed_in_prepare=True,
            interpreter=interpreter,
            frozen_inputs=frozen,
            external_runtime_inputs=external,
            prepared_UTC=datetime.now(timezone.utc).isoformat(),
            preparation_budget=elapsed(started),
            final_fresh_preparation_verified_paths=verified,
            all_process_CPU_and_creation_wall_charged=True,
            actual_process_creation_FILETIME_ticks=_PROCESS_CREATION_TICKS,
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
    frozen, external, admitted = {}, {}, False
    try:
        setup(started)
        require(output == OUTPUT and output.is_dir(), "Exact prepared fresh metadata receipt")
        require(
            not any(
                (output / name).exists()
                for name in (
                    "manifest.json",
                    "FAILED_UNSEALED.json",
                    "run_started.json",
                    "summary.json",
                    "completion_outcome.json",
                    "failure.json",
                )
            ),
            "Single exclusive prepared run, no retry",
        )
        admitted = True
        protocol = read(output / "protocol.json", started)
        prepared = read(output / "PREPARED_RECEIPT.json", started)
        require(
            prepared["prepared"] is True
            and prepared["terminal"] is False
            and prepared["protocol_sha256"] == sha(output / "protocol.json", started),
            "Exact exclusively prepared protocol",
        )
        frozen, external = (
            dict(protocol["frozen_inputs"]),
            dict(protocol["external_runtime_inputs"]),
        )
        policy = recovery_policy(frozen, external, started)
        same(protocol["author_sha256"], policy["author_sha256"], "Same reviewed executable pins")
        same(
            protocol["capture_manifest_SHA256"],
            policy["capture_manifest_SHA256"],
            "Same actual capture packet",
        )
        material = material_packet(policy, frozen, external, started)
        same(
            read(output / "material_inventory.json", started),
            material,
            "Complete immutable retained material inventory",
        )
        runtime_policy(protocol["interpreter"], started)
        verify_loaded(frozen, external, started)
        verify(frozen, external, started)
        budget(started, admission=True)
        save(
            output / "run_started.json",
            dict(
                started_UTC=datetime.now(timezone.utc).isoformat(),
                metadata_only=True,
            ),
            started,
        )
        admitted = True
        save(
            output / "loaded_module_origins.json", verify_loaded(frozen, external, started), started
        )
        summary = dict(
            schema="a13-exp-frontier-recovery-summary-v1",
            completed=True,
            passed=True,
            budget_censored=False,
            rejection=False,
            status="metadata_integrity_only",
            metadata_integrity=True,
            candidate_material_untrusted=True,
            independent130_validation_required=True,
            scientific_screen_complete=False,
            recovered_mathematical_pass_claim=False,
            original_attempt_still_failed=True,
            original_partial_success_invalid=True,
            old_summary_or_completion_promoted=False,
            original_material_receipt=MATERIAL.relative_to(ROOT).as_posix(),
            capture_manifest_SHA256=policy["capture_manifest_SHA256"],
            retained_files=42,
            retained_original_bytes=material["original_file_bytes"],
            fixed_rows_requiring_independent_validation=20,
            original_mathematics_refitted_or_reexecuted=False,
            new_test_credit=0,
            full_G2=False,
            adoption=False,
            cost_transfer=False,
            candidate_G2_absolute_stock_error_allocation=None,
            candidate_G2_barrier_band_allocation=None,
            gate_emission_authorized=False,
            budget=elapsed(started),
            independent_audit_still_required=True,
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
                status="metadata_integrity_only",
                summary_file="summary.json",
                metadata_integrity=True,
                candidate_material_untrusted=True,
                independent130_validation_required=True,
                scientific_screen_complete=False,
                recovered_mathematical_pass_claim=False,
            ),
        )
        budget(started)
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
    require(output == OUTPUT, "Only exact fresh metadata recovery receipt")
    result = prepare(output) if args.operation == "prepare" else run(output)
    print(
        json.dumps(
            dict(
                operation=args.operation,
                output=output.relative_to(ROOT).as_posix(),
                passed=result.get("passed"),
                new_test_credit=0,
                full_G2=False,
            )
        )
    )


if __name__ == "__main__":
    main()
