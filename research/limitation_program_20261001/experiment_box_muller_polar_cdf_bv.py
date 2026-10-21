"""Prospective original native-radius / ideal-angle exact-GBM law component.

Preparation is standard-library bookkeeping only. The run defers mpmath and
source kernels until immutable runtime/input verification. Native financial
arithmetic, clipping, costs and complete G2 are outside this certificate.
"""

from __future__ import annotations

import argparse
import ast
import ctypes
from ctypes import wintypes
from collections import Counter
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
OUTPUT = PROGRAM / "A02_polar_cdf_bv_run001"
METHOD = RESEARCH / "box_muller_polar_cdf_bv_preflight.json"
METHOD_DOC = RESEARCH / "BOX_MULLER_POLAR_CDF_BV_PREFLIGHT.md"
IMPLEMENTATION = RESEARCH / "box_muller_polar_cdf_bv_implementation_preflight.json"
IMPLEMENTATION_DOC = RESEARCH / "BOX_MULLER_POLAR_CDF_BV_IMPLEMENTATION_PREFLIGHT.md"
PRODUCER = RESEARCH / "experiment_box_muller_polar_cdf_bv.py"
AUDITOR = RESEARCH / "audit_box_muller_polar_cdf_bv.py"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
METHOD_SHA = "6305d69109fd8d73c6d0da1e32880ebfd292e975a66f40ee6fa395c630f7e37d"
METHOD_DOC_SHA = "4bf87dbd3ebd526cd5317faab8c54b01c639ea9d8a5bff907f1f8eb5debf888a"
CPU, ADMISSION, WALL = 180, 150, 600
Q, N, W = 1 << 40, 1 << 32, 72
EPSILON, SIGNED_LIMIT = Fraction(1, Q), Fraction(1 << 31)
CASES = {"B4x12": (4, 12, 30), "B8x52": (8, 52, 234)}
ROOT_LEAF = "160a18dba2e09b8e1ad2"
ROOT_PROOF_RECEIPT = PROGRAM / "A01_run011"
ROOT_PROVENANCE_PATHS = tuple(
    [
        f"results/limitation_program_20261001/A10_coefficient_run001/{case}/min-depth/leaves/{ROOT_LEAF}.{suffix}"
        for case in CASES
        for suffix in ("json", "npy")
    ]
    + [
        "results/limitation_program_20261001/A10_coefficient_run001/executed_code/" + name
        for name in (
            "nonrestoring_sqrt.py",
            "prove_nonrestoring_input.py",
            "reversible_fixed_point.py",
            "reversible.py",
        )
    ]
    + [
        "results/limitation_program_20261001/A01_run011/" + name
        for name in (
            "nonrestoring_arithmetic_certificate.json",
            "leaf_audit.json",
            "executed_code/reconcile_nonrestoring_v2.py",
        )
    ]
    + [
        "results/limitation_program_20261001/A11_nonrestoring_leaf_run001/02b69bbccf8176e3b72d."
        + suffix
        for suffix in ("json", "npy")
    ]
)
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24_000, 2 * 1024**3
_PATHS, _HASHES, _OBSERVED = {}, {}, {}
_EXTERNAL_TREES, _EXTERNAL_FILES = (), ()
_EXTERNAL_ROOT = None
_PROCESS_CREATION_TICKS = None


class BudgetCensoredError(RuntimeError):
    """Terminal fixed CPU/wall censor, with no retry."""


def require(condition, message):
    if not condition:
        raise ValueError(message)


def budget(started, admission=False):
    cpu, wall = time.process_time() - started[0], time.monotonic() - started[1]
    if cpu >= (ADMISSION if admission else CPU) or wall >= WALL:
        raise BudgetCensoredError("Fixed polar component 180CPU/150admission/600wall budget")
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
    global _EXTERNAL_TREES, _EXTERNAL_FILES, _EXTERNAL_ROOT
    _PATHS.clear()
    _HASHES.clear()
    _OBSERVED.clear()
    require(sys.dont_write_bytecode is True, "Pinned interpreter must start with -B")
    require(Path.cwd().resolve() == ROOT, "Execute module from canonical workspace ROOT")
    require(Path(__file__).resolve() == PRODUCER.resolve(), "Execute exact producer author path")
    for name in ("PYTHONPATH", "PYTHONHOME", "SAGE_ROOT", "MPMATH_SAGE"):
        require(not os.environ.get(name), "Uncaptured runtime override: " + name)
    os.environ["MPMATH_NOGMPY"] = "1"
    os.environ["MPMATH_NOSAGE"] = "1"
    base = Path(getattr(sys, "_base_executable", sys.executable)).resolve(strict=True)
    prefix = Path(sys.base_prefix).resolve(strict=True)
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


def allowed(path):
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
                "research.limitation_program_20261001.experiment_box_muller_polar_cdf_bv",
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
            actual = candidate.resolve()
            budget(started)
            require(actual.is_relative_to(ROOT), "Original owner membership ROOT confinement")
            rows.append((field, actual, original, expected))
    return rows


def selected_sources(frozen, external, started):
    bind(frozen, external, METHOD, METHOD_SHA, started)
    bind(frozen, external, METHOD_DOC, METHOD_DOC_SHA, started)
    plan = read(METHOD, started)
    require(plan["status"] == "HELD_AUTHOR_ONLY_NO_EXECUTOR_OR_EXECUTION", "Original method plan")
    pins = plan["source_bindings_SHA256"]
    require(len(pins) == 17, "Exactly fixed17 selected source pins")
    owners = []
    for key, expected in pins.items():
        if key.endswith("/manifest.json"):
            manifest_path = bind(frozen, external, ROOT / key, expected, started)
            data = read(manifest_path, started)
            rows = owner_rows(manifest_path, data, started)
            owners.append((key, rows))
    require(len(owners) == 3, "Three pinned original owner manifests, not self-membership")
    origins = []
    for key, expected in pins.items():
        actual = bind(frozen, external, ROOT / key, expected, started)
        if key.endswith("/manifest.json"):
            continue
        matches = [
            dict(
                owner_manifest=owner, source_map=field, original_key=original, expected_sha256=value
            )
            for owner, rows in owners
            for field, path, original, value in rows
            if path == actual and value == expected
        ]
        require(matches, "Selected input requires original equal-SHA manifest membership: " + key)
        origins.append(
            dict(
                path=key,
                sha256=expected,
                original_memberships=matches,
                archived_route=False,
                expected_hash_waived=False,
            )
        )
    require(len(origins) == 14, "All14 nonmanifest selected origins are accounted for")
    return plan, origins


def root_provenance(implementation, frozen, external, started):
    pins = implementation["additional_native_root_provenance_SHA256"]
    require(type(pins) is dict and pins, "Actual native root provenance required")
    require(
        set(pins) == set(ROOT_PROVENANCE_PATHS), "Exact finite13 additional root provenance inputs"
    )
    owners = []
    for path in (
        PROGRAM / "A10_coefficient_run001/manifest.json",
        PROGRAM / "A01_run011/manifest.json",
    ):
        key = path.relative_to(ROOT).as_posix()
        expected = implementation["original_root_owner_manifest_SHA256"][key]
        bind(frozen, external, path, expected, started)
        owners.append((key, owner_rows(path, read(path, started), started)))
    origins = []
    for key, expected in pins.items():
        path = bind(frozen, external, ROOT / key, expected, started)
        matches = [
            dict(
                owner_manifest=owner, source_map=field, original_key=original, expected_sha256=value
            )
            for owner, rows in owners
            for field, actual, original, value in rows
            if actual == path and value == expected
        ]
        require(matches, "Native root input original owner equal-SHA membership")
        origins.append(
            dict(
                path=key, sha256=expected, original_memberships=matches, expected_hash_waived=False
            )
        )
    return origins


def root_semantics(started):
    """Bind the actual array to the already executed universal induction/structure audit."""
    proof = read(ROOT_PROOF_RECEIPT / "nonrestoring_arithmetic_certificate.json", started)
    structure = read(ROOT_PROOF_RECEIPT / "leaf_audit.json", started)
    audited = read(PROGRAM / "A11_nonrestoring_leaf_run001/02b69bbccf8176e3b72d.json", started)
    prior_manifest = read(ROOT_PROOF_RECEIPT / "manifest.json", started)
    archived_source_routes = []
    for original, snapshot in (
        ("research/controlled_source_completion/nonrestoring_sqrt.py", "nonrestoring_sqrt.py"),
        ("research/journal_sprint/reversible_fixed_point.py", "reversible_fixed_point.py"),
        ("research/antithetic_feasibility/reversible.py", "reversible.py"),
    ):
        archived = PROGRAM / "A10_coefficient_run001/executed_code" / snapshot
        expected = prior_manifest["frozen_inputs"][original]
        require(
            sha(archived, started) == expected, "Exact prior proof-source SHA in archived A10 code"
        )
        archived_source_routes.append(
            dict(
                original_owner="A01_run011",
                original_map="frozen_inputs",
                original_key=original,
                expected_sha256=expected,
                verified_archived_path=archived.relative_to(ROOT).as_posix(),
                current_original_path_integrity_asserted=False,
                expected_hash_waived=False,
            )
        )
    require(
        proof["passed"] is True and proof["algebraic_all_guarded_input_identity"] is True,
        "Prior universal induction is required, not finite fixtures",
    )
    require(
        proof["input_formula"] == "isqrt(unsigned_x << fraction_bits)", "Exact prior root formula"
    )
    require(
        proof["invariant"] == "Q=isqrt(N); R=N-Q² if nonnegative, else N-(Q+1)²",
        "Prior non-restoring algebraic invariant",
    )
    require(structure["passed"] is True, "Prior actual gate structure audit")
    parser = structure["structural_parser"]
    require(
        parser["passed"] is True
        and parser["all_stages"] == 43
        and parser["full_native_argument_bits"] == parser["full_native_output_bits"] == 72
        and parser["signed_remainder_bits"] == 45
        and parser["retained_remainder_history_count"] == 44
        and parser["arbitrary_output_xor"] is True
        and parser["literal_forward_reverse_cleanup"] is True
        and parser["input_high_bits_untouched"] is True
        and parser["output_high_bits_unchanged"] is True,
        "Complete prior actual recurrence, interface and literal cleanup scope",
    )
    descriptors = {}
    for case in CASES:
        path = (
            PROGRAM / "A10_coefficient_run001" / case / "min-depth/leaves" / (ROOT_LEAF + ".json")
        )
        descriptor = read(path, started)
        spec = descriptor["spec"]
        require(
            descriptor["key"] == ROOT_LEAF
            and descriptor["op"] == "sqrt"
            and descriptor["params"] == {},
            "Exact actual integrated root leaf",
        )
        same(
            descriptor["input_contract"],
            {"unsigned_input_bits": 46},
            "Actual root unsigned46 contract",
        )
        same(descriptor["args"], [list(range(72))], "Full72 native argument-copy bank")
        same(descriptor["outs"], [list(range(72, 144))], "Full72 native dirty-output bank")
        require(
            spec["width"] == 72
            and spec["fraction_bits"] == 40
            and spec["active_input_bits"] == 46
            and spec["radicand_bits"] == 86
            and spec["result_bits"] == 43
            and spec["remainder_bits"] == 45
            and spec["remainder_history_count"] == 44
            and spec["operand_bits"] == 45
            and spec["adder_helper_bits"] == 1,
            "Exact signed-remainder structural sizes",
        )
        require(
            spec["algorithm"] == "signed-remainder-single-cuccaro-add"
            and spec["lowering"] == "unsigned-nonrestoring-sqrt-signed-remainder-v1"
            and spec["integration_lowering"] == "same-target-nonrestoring-unsigned-sqrt-library-v1",
            "Original native root algorithm",
        )
        same(
            spec["input_contract"],
            descriptor["input_contract"],
            "Inner/outer exact contract equality",
        )
        expected_key = hashlib.sha256(canonical(spec).encode()).hexdigest()[:20]
        require(expected_key == ROOT_LEAF, "Actual descriptor specification key")
        base_spec = dict(spec)
        del base_spec["integration_lowering"]
        same(base_spec, audited["spec"], "Same actual prior audited root specification")
        same(descriptor["args"], audited["args"], "Same prior native input bank")
        same(descriptor["outs"], audited["outs"], "Same prior native output bank")
        require(
            descriptor["sha256"] == audited["sha256"],
            "Same actual array SHA as universal realization audit",
        )
        gate = path.parent / descriptor["gate_file"]
        require(
            gate.name == ROOT_LEAF + ".npy" and sha(gate, started) == descriptor["sha256"],
            "Actual native array byte binding",
        )
        descriptors[case] = dict(
            path=path.relative_to(ROOT).as_posix(),
            spec=spec,
            gate_path=gate.relative_to(ROOT).as_posix(),
            gate_sha256=descriptor["sha256"],
        )
    # Same original emitter was frozen in both the universal audit and the integrated A10 receipt.
    require(
        sha(PROGRAM / "A10_coefficient_run001/executed_code/nonrestoring_sqrt.py", started)
        == "69d97fad09c450a065c025a3ad40904e36e5e30e7d28fa9a2677830704e84fb6",
        "Frozen original emitter underlying prior all-input realization",
    )
    return dict(
        actual_descriptors=descriptors,
        prior_universal_induction=proof,
        prior_actual_gate_structure=parser,
        prior_proof_source_archived_equal_SHA_routes=archived_source_routes,
        source_array_identity_not_fixture_inference=True,
        root_semantics="out XOR isqrt(unsigned argument <<40), high argument bits46..71 zero",
        no_new_gate_scan_replay_or_synthesis=True,
    )


def inventory(paths, frozen, external, started):
    """Freeze actual directory contents, including existing caches, not RECORD alone."""
    files, total = {}, 0
    for root in paths:
        budget(started)
        root = resolved(root, started)
        candidates = root.rglob("*") if root.is_dir() else (root,)
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
    for source in (ROOT / "research/__init__.py", RESEARCH / "__init__.py"):
        if source.is_file():
            roots.append(source)
    # Existing producer/auditor bytecode is captured even though startup -B prevents writes.
    for source in (PRODUCER, AUDITOR):
        cached = Path(cache_from_source(str(source)))
        if cached.is_file():
            roots.append(cached)
    counts = inventory([path for path in roots if path.exists()], frozen, external, started)
    allowed_import_roots = (ROOT, site_root, base_prefix, base_prefix / "Lib", base_prefix / "DLLs")
    absent = []
    for entry in sys.path:
        budget(started)
        candidate = Path(entry or ROOT)
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
        for candidate in root.rglob("*") if root.is_dir() else (root,):
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
        if not origin:
            continue
        for field, value in (("source", origin), ("cache", getattr(module, "__cached__", None))):
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


def source_convention(started):
    paths = {
        "contract": ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py",
        "sampler": ROOT / "research/controlled_source_completion/finance.py",
        "semantics": ROOT / "research/controlled_source_completion/ir.py",
    }
    trees = {}
    for name, path in paths.items():
        budget(started)
        trees[name] = ast.parse(read_bytes(path, started).decode("utf-8"), filename=str(path))
    assignment = next(
        node
        for node in trees["contract"].body
        if isinstance(node, ast.Assign)
        and isinstance(node.targets[0], ast.Tuple)
        and [item.id for item in node.targets[0].elts]
        == ["SIGMA", "CORR", "S0", "RATE", "T", "K", "H"]
    )
    values = [Fraction(str(item.value)) for item in assignment.value.elts]
    same(
        [encode(value) for value in values],
        [[3, 10], [2, 5], [100, 1], [3, 100], [1, 1], [100, 1], [140, 1]],
        "Original exact reference priors",
    )
    functions = {
        node.name: node for node in trees["contract"].body if isinstance(node, ast.FunctionDef)
    }
    build = functions["build"]
    build_expressions = {ast.dump(node, include_attributes=False) for node in ast.walk(build)}
    expressions = (
        "nt * (na + 1)",
        "T / nt",
        "zs[j * (na + 1)]",
        "zs[j * (na + 1) + 1 + i]",
        "SIGMA * math.sqrt(dt * CORR)",
        "SIGMA * math.sqrt(dt * (1 - CORR))",
        "g.lt(tree(g, baskets, g.maximum), g.c(H))",
        "g.cmul(tree(g, [s for row in stocks for s in row], g.add), 1 / (na * nt))",
        "g.cmul(g.pos(g.sub(average, g.c(K))), math.exp(-RATE * T))",
        "g.select(alive, payoff, g.c(0))",
    )
    witnesses = []
    for expression in expressions:
        budget(started)
        expected = ast.dump(ast.parse(expression, mode="eval").body, include_attributes=False)
        require(expected in build_expressions, "Original exact financial convention expression")
        witnesses.append(dict(expression=expression, actual_AST=expected))
    sampler = next(
        node
        for node in trees["sampler"].body
        if isinstance(node, ast.FunctionDef) and node.name == "normals_graph"
    )
    sampler_nodes = {ast.dump(node, include_attributes=False) for node in ast.walk(sampler)}
    for expression in (
        "g.input('uniform_%d' % (2*j), q)",
        "g.input('uniform_%d' % (2*j+1), q)",
        "g.sqrt(g.cmul(g.log(u), -2))",
        "g.mul(radius, g.cos_unit(v))",
        "g.mul(radius, g.cos_unit(angle2))",
    ):
        expected = ast.dump(ast.parse(expression, mode="eval").body, include_attributes=False)
        require(expected in sampler_nodes, "Original joint polar sampler expression")
        witnesses.append(dict(expression=expression, actual_AST=expected))
    semantic_nodes = {
        ast.dump(node, include_attributes=False) for node in ast.walk(trees["semantics"])
    }
    root_expression = "math.isqrt(raw[0] << f)"
    require(
        ast.dump(ast.parse(root_expression, mode="eval").body, include_attributes=False)
        in semantic_nodes,
        "Actual floor-root integer semantics",
    )
    return dict(
        priors=[encode(value) for value in values],
        AST_witnesses=witnesses,
        actual_root_expression=root_expression,
        ideal_reference_is_exact_unclipped=True,
        native_floor_and_clamp_finance_equivalence_claimed=False,
    )


def finance_roles(graph, normals, assets, dates, pairs):
    """Recover every raw prefix incidence from actual output; do not evaluate finance."""
    normal_index = {value: index for index, value in enumerate(normals)}
    require(len(normal_index) == dates * (assets + 1), "Complete distinct normal source values")
    outputs = graph.target["outputs"]
    require(set(outputs) == {"Y"}, "Original sole financial output")
    alive, payoff, zero = graph.node(outputs["Y"], "select")["args"]
    graph.const(zero, 0)
    discount = graph.node(payoff, "cmul")
    require(literal(discount["params"]["c"]) > 0, "Positive native discount literal")
    positive = graph.node(discount["args"][0], "positive")["args"][0]
    average, strike = graph.node(positive, "sub")["args"]
    graph.const(strike, 100 * Q)
    average_node = graph.node(average, "cmul")
    require(
        literal(average_node["params"]["c"]) == nearest_ratio(Q, assets * dates),
        "Actual original average literal",
    )
    stocks = set()
    pending = [average_node["args"][0]]
    while pending:
        value = pending.pop()
        node = graph.node(value)
        if node["op"] == "shift":
            stocks.add(value)
        else:
            pending.extend(graph.node(value, "add")["args"])
    require(len(stocks) == assets * dates, "All original distinct asset/date stock sites")
    require(
        graph.flatten(average_node["args"][0], stocks) == Counter({v: 1 for v in stocks}),
        "Average includes every stock once",
    )
    stock_matrix, prefix_witnesses = {}, []
    common_literals, idio_literals, initial_literals, drift_literals, clamps = (
        set(),
        set(),
        set(),
        set(),
        set(),
    )
    for stock in sorted(stocks):
        polynomial, k = graph.node(stock, "shift")["args"]
        reduced = graph.node(k, "bits", dict(shift=40, width=72, signed=True))["args"][0]
        clipped = graph.node(reduced, "cmul")["args"][0]
        raw = graph.clip(clipped)
        clamp_hi = graph.node(clipped, "select")["args"][2]
        clamp_lo = graph.node(graph.node(clipped, "select")["args"][1], "select")["args"][1]
        clamps.add((graph.const(clamp_lo), graph.const(clamp_hi)))
        # The frozen degree-12 polynomial is a prerequisite; its error bridge remains open.
        require(graph.node(polynomial)["op"] == "add", "Original Estrin polynomial root")
        components, constants, work = Counter(), Counter(), [raw]
        while work:
            value = work.pop()
            node = graph.node(value)
            if node["op"] == "add":
                work.extend(node["args"])
            elif node["op"] == "const":
                constants[graph.const(value)] += 1
            else:
                node = graph.node(value, "cmul")
                require(
                    node["args"][0] in normal_index,
                    "Raw prefix only literal-scaled original normals",
                )
                index = normal_index[node["args"][0]]
                coefficient = literal(node["params"]["c"])
                require(coefficient > 0, "Actual positive original common/idio coefficient")
                components[index] += 1
                (common_literals if index % (assets + 1) == 0 else idio_literals).add(coefficient)
        require(
            components and all(count == 1 for count in components.values()),
            "Each driver enters prefix exactly once",
        )
        idio_roles = {index % (assets + 1) for index in components if index % (assets + 1)}
        require(len(idio_roles) == 1, "Exactly one asset idiosyncratic role in stock prefix")
        asset = next(iter(idio_roles)) - 1
        date = len(components) // 2 - 1
        expected = Counter(
            {t * (assets + 1) + role: 1 for t in range(date + 1) for role in (0, asset + 1)}
        )
        require(
            components == expected and 0 <= date < dates, "Exact complete linear cumulative prefix"
        )
        require((asset, date) not in stock_matrix, "Unique asset/date role site")
        stock_matrix[asset, date] = stock
        initial = [value for value in constants if value > 0]
        drift = [value for value in constants if value < 0]
        require(
            len(initial) == len(drift) == 1
            and constants[initial[0]] == 1
            and constants[drift[0]] == date + 1
            and len(constants) == 2,
            "Initial plus one drift per increment",
        )
        initial_literals.add(initial[0])
        drift_literals.add(drift[0])
        prefix_witnesses.append(
            dict(
                stock=stock,
                raw_log=raw,
                asset=asset,
                date=date,
                original_normal_indices=sorted(components),
                every_driver_multiplicity=1,
                constants=[[value, count] for value, count in sorted(constants.items())],
            )
        )
    require(
        set(stock_matrix) == {(i, j) for i in range(assets) for j in range(dates)},
        "Complete stock role matrix",
    )
    require(
        all(
            len(items) == 1
            for items in (common_literals, idio_literals, initial_literals, drift_literals, clamps)
        ),
        "Shared actual original literal inventories",
    )
    maximum, barrier = graph.node(alive, "lt")["args"]
    graph.const(barrier, 140 * Q)
    basket_ids = set()
    pending = [maximum]
    while pending:
        value = pending.pop()
        if graph.node(value)["op"] == "cmul":
            basket_ids.add(value)
        else:
            flag, hi, lo = graph.node(value, "select")["args"]
            require(graph.node(flag, "lt")["args"] == [lo, hi], "Strict original maximum reduction")
            pending.extend((lo, hi))
    require(
        len(basket_ids) == dates
        and graph.maxima(maximum, basket_ids) == Counter({v: 1 for v in basket_ids}),
        "Every monitored basket once",
    )
    basket_dates = set()
    basket_witnesses = []
    for basket in sorted(basket_ids):
        node = graph.node(basket, "cmul", dict(c=Q // assets))
        row = graph.flatten(node["args"][0], stocks)
        matched = [
            j
            for j in range(dates)
            if row == Counter({stock_matrix[i, j]: 1 for i in range(assets)})
        ]
        require(
            len(matched) == 1 and matched[0] not in basket_dates, "Exact all-asset same-date basket"
        )
        basket_dates.add(matched[0])
        basket_witnesses.append(dict(basket=basket, date=matched[0], stocks=sorted(row)))
    pair_roles = []
    for pair in range(pairs):
        indices = [2 * pair, 2 * pair + 1]
        roles = [dict(date=index // (assets + 1), role=index % (assets + 1)) for index in indices]
        kinds = [item["role"] for item in roles]
        if kinds[0] == 0:
            require(
                kinds[1] == 1 and roles[0]["date"] == roles[1]["date"], "Common/first-idio pair"
            )
            kind = "same_date_common_first_idio"
        elif kinds[1] == 0:
            require(
                kinds[0] == assets and roles[1]["date"] == roles[0]["date"] + 1,
                "Cross-date last-idio/common pair",
            )
            kind = "cross_date_last_idio_common"
        else:
            require(
                kinds[1] == kinds[0] + 1 and roles[0]["date"] == roles[1]["date"],
                "Two distinct same-date idios",
            )
            kind = "same_date_distinct_idios"
        incidences = []
        for asset in range(assets):
            for date in range(dates):
                active = [item["date"] <= date and item["role"] in (0, asset + 1) for item in roles]
                # Exact ideal squared coefficients: sigma² dt rho or sigma² dt (1-rho).
                square = sum(
                    (
                        Fraction(9, 100 * dates)
                        * (Fraction(2, 5) if item["role"] == 0 else Fraction(3, 5))
                        for item, present in zip(roles, active, strict=True)
                        if present
                    ),
                    Fraction(0),
                )
                require(square <= Fraction(9, 100 * dates), "Actual roles support ideal norm bound")
                if all(active):
                    require(0 in kinds, "Both current coordinates affect a stock only common+idio")
                incidences.append(
                    dict(asset=asset, date=date, active=active, ideal_squared_norm=encode(square))
                )
        pair_roles.append(
            dict(
                pair=pair,
                scalar_indices=indices,
                roles=roles,
                kind=kind,
                stock_prefix_incidence=incidences,
            )
        )
    return dict(
        assets=assets,
        dates=dates,
        pairs=pairs,
        prefix_witnesses=prefix_witnesses,
        baskets=basket_witnesses,
        actual_common_literal=next(iter(common_literals)),
        actual_idio_literal=next(iter(idio_literals)),
        actual_initial_literal=next(iter(initial_literals)),
        actual_drift_literal=next(iter(drift_literals)),
        actual_clamps=list(next(iter(clamps))),
        native_discount_literal=literal(discount["params"]["c"]),
        actual_pair_roles=pair_roles,
        ideal_maximum_squared_norm=encode(Fraction(9, 100 * dates)),
        native_literal_coefficients_equal_ideal_claimed=False,
    )


def bind_actual_sources(started):
    certificate = read(PROGRAM / "C06_pair_run001/certificate.json", started)
    archived_scopes = read(PROGRAM / "C06_pair_audit_run001/actual_pair_scope_audit.json", started)
    native_root = root_semantics(started)
    reports, common_table, common_ln2 = {}, None, None
    for case, (assets, dates, pairs) in CASES.items():
        budget(started, admission=True)
        binding = certificate["source_bindings"][case]
        target_path = PROGRAM / "A10_coefficient_run001" / case / "min-depth/target.json"
        require(ROOT / binding["target"] == target_path, "Original C06 target route")
        target = read(target_path, started)
        source = read(target_path.parent / "source.json", started)
        graph = ActualGraph(target, started)
        inputs = [node for node in target["nodes"] if node["op"] == "input"]
        require(len(inputs) == dates * (assets + 1) == 2 * pairs, "Original input and pair counts")
        for index, node in enumerate(inputs):
            same(
                node["params"],
                dict(name="uniform_" + str(index), bits=32, preparation="uniform"),
                "Independent raw q32 input roles",
            )
        same(source["inputs"], inputs, "Native source actual inputs")
        require(source["word_width"] == W and source["fraction_bits"] == 40, "Native source ABI")
        same(source["outputs"], target["outputs"], "Native source outputs")
        noninputs = [node for node in target["nodes"] if node["op"] != "input"]
        calls = {}
        require(
            len(noninputs) == len(source["forward_calls"]), "Complete native source call inventory"
        )
        for node, call in zip(noninputs, source["forward_calls"], strict=True):
            budget(started)
            same(
                [node["args"], node["out"]],
                [call["args"], call["out"]],
                "Every actual source call value mapping",
            )
            for value in node["out"]:
                calls[value] = call
        normals, ln2 = binding["normal_values"], binding["literal_ln2"]
        require(
            type(ln2) is int and 0 < ln2 < Q and len(normals) == 2 * pairs,
            "Original fixed ln2 and normal values",
        )
        table = target["tables"]["log"]
        require(
            len(table) == 32
            and all(len(row) == 9 and all(type(value) is int for value in row) for row in table),
            "Actual288 log table coefficients",
        )
        if common_table is None:
            common_table, common_ln2 = table, ln2
        same(table, common_table, "Same fixed log table across both source contracts")
        require(ln2 == common_ln2, "Same original ln2 literal")
        scopes = []
        for pair in range(pairs):
            budget(started)
            roots = normals[2 * pair : 2 * pair + 2]
            scope = graph.pair(
                roots, inputs[2 * pair]["out"][0], inputs[2 * pair + 1]["out"][0], ln2
            )
            root_call = calls[scope["radius"]]
            require(
                root_call["leaf"] == ROOT_LEAF and root_call["argument_copy_cx"] == 144,
                "Every actual radius invokes the bound full72 unsigned46 root leaf",
            )
            same(
                root_call["args"],
                graph.node(scope["radius"], "sqrt")["args"],
                "Actual root call argument mapping",
            )
            same(root_call["out"], [scope["radius"]], "Actual root call output mapping")
            scopes.append(scope)
        same(
            scopes,
            archived_scopes[case]["independently_walked_pair_scopes"],
            "All actual pair scopes equal independent archived scope",
        )
        reports[case] = dict(
            joint_pair_scopes=scopes,
            source_call_count=len(noninputs),
            financial_roles=finance_roles(graph, normals, assets, dates, pairs),
            actual_root_descriptor=native_root["actual_descriptors"][case],
            actual_root_calls=[calls[scope["radius"]] for scope in scopes],
        )
    return (
        dict(convention=source_convention(started), native_root_prior=native_root, cases=reports),
        common_table,
        common_ln2,
    )


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


def log_radius_envelope(mp, rows, ln2, started):
    radius, checks, row_errors, maximum = Fraction(1, 64), [], [], Fraction(0)
    for index, row in enumerate(rows):
        budget(started)
        center = 1 + Fraction(2 * index + 1, 64)
        errors = []
        for degree, raw in enumerate(row):
            budget(started)
            require(-(1 << 71) <= raw < (1 << 71), "Signed actual lookup coefficient")
            bounds = (
                interval(mp.iv.log(iv(mp, center)))
                if degree == 0
                else (Fraction((-1) ** (degree - 1), degree) / center**degree,) * 2
            )
            error = coefficient_error(Fraction(raw, Q), bounds)
            require(
                error <= EPSILON / 2, "Every saved log coefficient meets fixed nearest allowance"
            )
            errors.append(error)
            checks.append(
                dict(
                    row=index,
                    degree=degree,
                    raw=raw,
                    exact_coefficient_enclosure=[encode(value) for value in bounds],
                    literal_error_upper=encode(error),
                )
            )
        row_errors.append(
            sum((error * radius**degree for degree, error in enumerate(errors)), Fraction(0))
        )
        bound = abs(Fraction(row[-1], Q))
        maximum = max(maximum, bound)
        for raw in reversed(row[:-1]):
            product = bound * radius + EPSILON
            bound = abs(Fraction(raw, Q)) + product
            maximum = max(maximum, bound, product)
    require(len(checks) == 288 and maximum < SIGNED_LIMIT, "288 checks and actual Horner no-wrap")
    remainder, coefficient_rounding = radius**9 / 9, max(row_errors)
    floors = EPSILON * sum((radius**degree for degree in range(8)), Fraction(0))
    table_error = remainder + coefficient_rounding + floors
    ln2_bounds = interval(mp.iv.log(iv(mp, 2)))
    ln2_error = coefficient_error(Fraction(ln2, Q), ln2_bounds)
    require(ln2_error <= EPSILON / 2, "Actual ln2 fixed nearest allowance")
    log_error = table_error + 33 * ln2_error
    root_argument_bound = 66 * ln2_bounds[1] + 2 * log_error
    B = interval(mp.iv.sqrt(iv(mp, root_argument_bound)))[1]
    require(
        2 * (33 * abs(Fraction(ln2, Q)) + maximum) < SIGNED_LIMIT
        and root_argument_bound < SIGNED_LIMIT
        and B < SIGNED_LIMIT,
        "All midpoint log/exponent/-2/root signed no-wrap premises",
    )
    require(root_argument_bound * Q < (1 << 46), "Actual unsigned46 root-input source contract")
    # Raw midpoint top bits range7..39; e=top-40 is exactly -33..-1.
    require(
        (128).bit_length() - 1 - 40 == -33 and (Q - 128).bit_length() - 1 - 40 == -1,
        "All q32 midpoint exponent extremes",
    )
    require(
        2 * Q - 1 < (1 << 71) and 33 * ln2 < (1 << 71),
        "Exact left shift and integer-ln2 raw safety",
    )
    exponent_classes, next_k = [], 0
    for exponent in range(-33, 0):
        budget(started)
        top = exponent + 40
        lower_raw, upper_raw = max(128, 1 << top), min(Q - 128, (1 << (top + 1)) - 1)
        first_k = max(0, (lower_raw - 128 + 255) // 256)
        last_k = min(N - 1, (upper_raw - 128) // 256)
        require(first_k == next_k and last_k >= first_k, "Nonempty contiguous q32 exponent class")
        first, last = 256 * first_k + 128, 256 * last_k + 128
        require(
            Q <= first << (-exponent) <= last << (-exponent) <= 2 * Q - 1,
            "Every class normalizes exactly into the frozen log interpolation domain",
        )
        exponent_classes.append(
            dict(
                exponent=exponent,
                first_raw_uniform=first_k,
                last_raw_uniform=last_k,
                count=last_k - first_k + 1,
                midpoint_raw_bounds=[first, last],
                normalized_raw_bounds=[first << (-exponent), last << (-exponent)],
            )
        )
        next_k = last_k + 1
    require(next_k == N and len(exponent_classes) == 33, "Entire q32 word union without sampling")
    eta = 2 * log_error + 2 * EPSILON * B + EPSILON**2
    D_S = min(Fraction(1), Fraction(1, 2 * N) + eta / 2)
    return (
        dict(
            coefficient_checks=checks,
            coefficient_count=288,
            log_table_remainder_upper=encode(remainder),
            log_table_literal_rounding_upper=encode(coefficient_rounding),
            log_table_floor_upper=encode(floors),
            log_table_error_upper=encode(table_error),
            log_Horner_maximum_magnitude=encode(maximum),
            ln2_literal=ln2,
            ln2_true_enclosure=[encode(value) for value in ln2_bounds],
            ln2_literal_error_upper=encode(ln2_error),
            log_error_all_midpoints_upper=encode(log_error),
            root_argument_upper=encode(root_argument_bound),
            root_input_unsigned_bit_contract=46,
            root_input_raw_upper=encode(root_argument_bound * Q),
            internal_radius_upper=encode(B),
            square_error_eta_upper=encode(eta),
            squared_radius_KS_upper=encode(D_S),
            midpoint_exponents=[-33, -1],
            exact_exponent_class_partition=exponent_classes,
            all_midpoints_covered_without_sweep=True,
            internal_radius_not_final_normal_norm=True,
            root_formula="R_raw=isqrt(max(-2*L_raw,0)*Q); Rhat=R_raw/Q",
            root_squared_floor="0<=A_positive-Rhat^2<2*epsilon*Rhat+epsilon^2",
            native_map_monotonicity_used=False,
            radial_Holder_or_cutoff_used=False,
        ),
        B,
        D_S,
    )


class Polynomial:
    """Small exact formal identity checker; no values or numerical samples."""

    def __init__(self, terms=None):
        self.terms = {key: Fraction(value) for key, value in (terms or {}).items() if value}

    @classmethod
    def variable(cls, name):
        return cls({(name,): 1})

    @classmethod
    def scalar(cls, value):
        return cls({(): value})

    def __add__(self, other):
        terms = Counter(self.terms)
        for key, value in other.terms.items():
            terms[key] += value
        return Polynomial(terms)

    def __neg__(self):
        return Polynomial({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        terms = Counter()
        for left, a in self.terms.items():
            for right, b in other.terms.items():
                terms[tuple(sorted(left + right))] += a * b
        return Polynomial(terms)

    def __pow__(self, degree):
        require(type(degree) is int and 0 <= degree <= 4, "Finite symbolic identity degree")
        result = Polynomial.scalar(1)
        for _ in range(degree):
            result = result * self
        return result

    def encoded(self):
        return [[list(key), encode(value)] for key, value in sorted(self.terms.items())]


def method_obligations(started):
    """Exact identity witnesses plus explicit analytic lemmas and all premises."""
    budget(started)
    A, B, s, c, k, U, V = [
        Polynomial.variable(name) for name in ("A", "B", "s", "c", "k", "U", "V")
    ]
    one, two = Polynomial.scalar(1), Polynomial.scalar(2)
    y, X = -A * s + B * c, c * U + s * V
    identities = {
        "pointwise_nonnegative_remainder": (
            k * (s**2 * A + c**2 * B) - y**2,
            s**2 * A * (k - A) + c**2 * B * (k - B) + two * s * c * A * B,
        ),
        "stationary_U_circle_remainder": (U - c * X - s * (s * U - c * V), U * (one - c**2 - s**2)),
        "stationary_V_circle_remainder": (V - s * X - c * (c * V - s * U), V * (one - c**2 - s**2)),
        "circle_sum_bound": ((s + c) ** 2, one + two * s * c + (s**2 + c**2 - one)),
        "circle_product_bound": ((s - c) ** 2, s**2 + c**2 - two * s * c),
    }
    witnesses = []
    for name, (left, right) in identities.items():
        budget(started)
        require(not (left - right).terms, "Exact formal angular identity: " + name)
        witnesses.append(
            dict(name=name, left=left.encoded(), right=right.encoded(), zero_difference=[])
        )
    return dict(
        exact_formal_identity_witnesses=witnesses,
        radial_CDF=[
            (
                "Midpoint quantile atoms at (k+1/2)/N give sup CDF discrepancy 1/(2N) from "
                "the continuous exponential law, also at atom jumps."
            ),
            (
                "For every k, |Rhat_k^2-S_k|<=eta implies {S_k<=t-eta} subset "
                "{Rhat_k^2<=t} subset {S_k<=t+eta}. This uses no ordering of the native "
                "map."
            ),
            (
                "F(t)=0 below0 and 1-exp(-t/2) above0 is globally 1/2-Lipschitz. The event "
                "inclusions plus midpoint discrepancy give D_S<=min(1,1/(2N)+eta/2)."
            ),
            (
                "Positive-part projection is1-Lipschitz and S_k>=0. A=max(-2Lhat,0), "
                "R_raw=isqrt(A_raw*Q), and R_raw^2<=A_raw*Q<(R_raw+1)^2 give "
                "eta=2E_L+2epsilonB+epsilon^2."
            ),
        ],
        radial_BV=[
            (
                "Fix all other pairs and current angle. Every exact unclipped stock is "
                "c*exp(beta*r), c>0; real beta may have either sign. Baskets and exact "
                "average are convex on r>=0."
            ),
            (
                "Each strict basket sublevel is an interval; their intersection I is an "
                "interval, including empty/full/unbounded/constant cases. On I, "
                "h=discount*(average-strike)^+ is convex, nonnegative, and bounded by "
                "C=(H-K)*discount."
            ),
            (
                "Convex nonnegative h<=C has variation at most2C on I. Zero extension adds "
                "at most two endpoint jumps, each<=C, including strict endpoint ties. "
                "Total variation<=4C. r=sqrt(s) is monotone, so the same bound holds for "
                "squared radius."
            ),
            (
                "Integration by parts for probability measures of equal total mass gives "
                "|E_native h-E_continuous h|<=TV(h)*sup|F_native-F_continuous|. Endpoint "
                "values at atoms must be retained in variation."
            ),
        ],
        angular_BV=[
            (
                "For exact unclipped stocks x_i=A_i*c+B_i*s, y_i=-A_i*s+B_i*c, w_i>0, "
                "A_i,B_i>=0, A_i^2+B_i^2<=kappa^2<2. Nonconstant basket derivatives are "
                "sum(w*y), sum(w*(y^2-x))."
            ),
            (
                "In quadrantI, A_i,B_i<=kappa and the first exact identity has nonnegative "
                "right side. At stationarity c*V=s*U and c^2+s^2=1, the next identities "
                "give U=c*X,V=s*X with X=sum(w*x)>0."
            ),
            (
                "Thus sum(w*y^2)<=kappa*s*c*(s+c)*X. The circle identities imply sc<=1/2 "
                "and s+c<=sqrt2, hence sc(s+c)<=1/sqrt2. Since kappa<sqrt2, every "
                "nonconstant quadrantI stationary point has second derivative<0."
            ),
            (
                "QuadrantII derivative is strictly negative and quadrantIV strictly "
                "positive unless all coefficients vanish. In quadrantIII x<=0 and "
                "sum(w*(y^2-x))>0 for any nonzero vector, so derivative is strictly "
                "increasing. There is one maximum/minimum; all-zero and r0 cases are "
                "constant."
            ),
            (
                "A zero derivative at0 forces all B_i=0; at pi/2 forces all A_i=0. These "
                "one-axis cases are monotone semicircles. No missing endpoint stationary "
                "case is assumed away."
            ),
            (
                "Each strict threshold indicator on the circle has TV<=2, including "
                "empty/full/constant cases and H=maximum, where one removed point costs2. "
                "The exact Asian average has the same positive-weight form, so "
                "min(C,discount*(average-K)^+) has TV<=2C."
            ),
            (
                "The product of nt indicators has TV<=2nt; the bounded-product inequality "
                "therefore gives payoff TV<=2C(nt+1). A closed finite basket band may have "
                "two arcs and TV4; native band transfer remains open."
            ),
        ],
        midpoint_circle=[
            (
                "Split the circle in turns into N equal cells. Each cell midpoint "
                "integration error is at most cell variation/(2N); sum gives "
                "TV_circle/(2N), with exact strict-tie values included. There is no "
                "extra2pi probability factor."
            ),
            (
                "The exact+.75 wrapped midpoint grid is a permutation of the same N turn "
                "midpoints, and cos(theta+3pi/2)=+sin(theta). The coordinates remain one "
                "joint pair, not two independent digital normals."
            ),
        ],
        actual_point_value_BV_convention=[
            (
                "Variation uses the actual priced value at every point: both the left-limit "
                "to point-value jump and the point-value to right-limit jump count. A strict "
                "barrier tie is not replaced by a right-continuous representative."
            ),
            (
                "Decompose a bounded-variation function using open and closed threshold "
                "indicators. Against the continuous comparison law, both indicator errors "
                "are bounded by D_S, using F(t) and its one-sided limit F(t-). The sum of "
                "the absolute jump weights is the actual-point variation."
            ),
            (
                "A singleton removed maximum therefore costs two jumps in circular "
                "variation. The angular cell-midpoint bound also retains exact midpoint "
                "point values, including singleton ties; no endpoint convention discards "
                "an atom that the native grid can price."
            ),
        ],
        hybrid_order=[
            (
                "For each original independent raw-input pair, replace radius FIRST, "
                "applying radial BV uniformly in fixed angle and other pairs. Then replace "
                "that current angle at its now bounded native radius, applying angular BV "
                "uniformly in the positive weights contributed by other pairs."
            ),
            (
                "Other pairs may still have unbounded continuous radii because they only "
                "change positive weights. Applying the angular lemma before bounding the "
                "current radius is forbidden. Sum the joint-pair errors, never divide by "
                "scalar coordinates."
            ),
        ],
        analytical_premises_are_not_native_finance_equivalence=True,
        strict_threshold_TV=2,
        closed_finite_band_TV=4,
        radial_payoff_TV_multiplier=4,
        native_cosine_or_clipped_unimodality_certified=False,
    )


def angular_guards(B, binding, started):
    rows, passed = {}, True
    for case, (assets, dates, pairs) in CASES.items():
        budget(started)
        norm = Fraction(*binding["cases"][case]["financial_roles"]["ideal_maximum_squared_norm"])
        require(norm == Fraction(9, 100 * dates), "Source role norm equals exact sigma²dt")
        kappa_squared = B**2 * norm
        guard = kappa_squared < 2
        passed = passed and guard
        rows[case] = dict(
            assets=assets,
            dates=dates,
            joint_pairs=pairs,
            ideal_squared_norm_upper=encode(norm),
            radius_upper=encode(B),
            kappa_squared_upper=encode(kappa_squared),
            strict_threshold=2,
            passed=guard,
            actual_native_finance_literals_used=False,
        )
    return dict(
        all_strict_guards_passed=passed,
        cases=rows,
        rejection_blocks_angular_and_dollar_certificates=True,
    )


def ideal_hybrid_bounds(mp, D_S, guards, started):
    require(guards["all_strict_guards_passed"] is True, "No price bound after failed angular guard")
    discount = interval(mp.iv.exp(iv(mp, -Fraction(3, 100))))
    C = (40 * discount[0], 40 * discount[1])
    require(0 < C[0] <= C[1] < 40, "Exact unclipped survival cap")
    rows = {}
    for case, (_, dates, pairs) in CASES.items():
        budget(started)
        radial = 4 * C[1] * D_S
        angular = C[1] * Fraction(dates + 1, N)
        total = pairs * (radial + angular)
        rows[case] = dict(
            joint_pairs=pairs,
            squared_radius_KS_upper=encode(D_S),
            exact_cap_enclosure=[encode(value) for value in C],
            one_pair_radial_dollars_upper=encode(radial),
            one_pair_angular_dollars_upper=encode(angular),
            hybrid_dollars_upper=encode(total),
            unchanged_residual_dollars=encode(Fraction(11, 2000)),
            partial_bound_below_context_residual=total < Fraction(11, 2000),
            residual_spent_or_reallocated=False,
            full_native_G2_acceptance=False,
            adoption=False,
        )
    return dict(
        schema="original-native-radius-ideal-midpoint-angle-exact-GBM-hybrid-bound-v1",
        interval_digits=90,
        outward_exact_rational_endpoints=True,
        exact_discount_enclosure=[encode(value) for value in discount],
        cases=rows,
        pair_order="each current radius FIRST then current ideal angle",
        joint_digital_normals_asserted_independent=False,
        native_cosine_envelope_computed=False,
        native_financial_bridge_open=True,
        no_old_Holder_or_grid_term_added_again=True,
        full_G2=False,
        test_credit=0,
        cost_transfer=False,
        adoption=False,
    )


def implementation_policy(started):
    data = read(IMPLEMENTATION, started)
    require(
        data["schema"] == "box-muller-polar-cdf-bv-implementation-preflight-v1",
        "Implementation preflight schema",
    )
    same(
        data["producer_CPU_admission_wall_seconds"],
        [180, 150, 600],
        "Fixed complete producer budget",
    )
    same(
        data["independent_auditor_CPU_admission_wall_seconds"],
        [180, 150, 600],
        "Fixed complete auditor budget",
    )
    require(
        data["primary_interval_decimal_digits"] == 90
        and data["independent_interval_decimal_digits"] == 130,
        "Fixed distinct interval precisions",
    )
    require(
        data["numerical_threads"] == 1 and data["new_fixture_credit"] == 0,
        "No fixtures/single thread",
    )
    require(
        data["runtime_backend"] == "python"
        and data["cosine_512_coefficient_envelope_in_scope"] is False,
        "Held runtime and bridge scope",
    )
    same(
        data["method_document_SHA256"],
        {METHOD.name: METHOD_SHA, METHOD_DOC.name: METHOD_DOC_SHA},
        "Immutable held method docs",
    )
    hashes = data["author_sha256"]
    require(set(hashes) == {PRODUCER.name, AUDITOR.name}, "Both executable author SHA pins")
    for name, expected in hashes.items():
        budget(started)
        require(
            type(expected) is str and len(expected) == 64,
            "Auditor must exist and be pinned before preparation",
        )
        require(sha(RESEARCH / name, started) == expected, "Exact author SHA before work")
    return data


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
        limits_CPU_admission_wall=[180, 150, 600],
        new_test_credit=0,
        full_G2=False,
        cost_transfer=False,
        adoption=False,
    )
    save(output / "completion_outcome.json", outcome, started)
    files = owned_files(output, started)
    budget(started)
    manifest = dict(
        schema="box-muller-polar-cdf-bv-terminal-manifest-v1",
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


def prepare(output):
    started = process_started()
    frozen, external = {}, {}
    created = False
    try:
        setup(started)
        require(output == OUTPUT and not output.exists(), "Fresh exact producer receipt only")
        require("mpmath" not in sys.modules, "Standard-library-only preparation")
        implementation = implementation_policy(started)
        plan, origins = selected_sources(frozen, external, started)
        root_origins = root_provenance(implementation, frozen, external, started)
        for path in (PRODUCER, AUDITOR, IMPLEMENTATION, IMPLEMENTATION_DOC):
            bind(frozen, external, path, sha(path, started), started)
        interpreter = runtime(frozen, external, started)
        runtime_policy(interpreter, started)
        verify_loaded(frozen, external, started)
        verify(frozen, external, started)
        budget(started, admission=True)
        output.mkdir()
        created = True
        (output / "executed_code").mkdir()
        for path in (PRODUCER, AUDITOR, IMPLEMENTATION, IMPLEMENTATION_DOC, METHOD, METHOD_DOC):
            copy_exact(path, output / "executed_code" / path.name, frozen, external, started)
        save(output / "selected_source_origins.json", origins, started)
        save(output / "native_root_provenance.json", root_origins, started)
        save(output / "interpreter.json", interpreter, started)
        verification_count = final_verify(frozen, external, started)
        budget(started, admission=True)
        protocol = dict(
            schema="box-muller-polar-cdf-bv-protocol-v1",
            output=output.relative_to(ROOT).as_posix(),
            prepared_UTC=datetime.now(timezone.utc).isoformat(),
            producer_module="research.limitation_program_20261001.experiment_box_muller_polar_cdf_bv",
            frozen_inputs=frozen,
            external_runtime_inputs=external,
            immutable_author_sha256=implementation["author_sha256"],
            method_document_SHA256=implementation["method_document_SHA256"],
            selected_source_SHA256=plan["source_bindings_SHA256"],
            additional_native_root_provenance_SHA256=implementation[
                "additional_native_root_provenance_SHA256"
            ],
            original_root_owner_manifest_SHA256=implementation[
                "original_root_owner_manifest_SHA256"
            ],
            interpreter=interpreter,
            process_CPU_seconds=180,
            admission_process_CPU_seconds=150,
            wall_seconds=600,
            primary_interval_decimal_digits=90,
            independent_interval_decimal_digits=130,
            numerical_threads=1,
            fixture_credit=0,
            startup_B_required=True,
            pure_Python_mpmath_backend_required=True,
            cosine_512_envelope_computed=False,
            full_native_financial_bridge_open=True,
            runtime_and_source_frozen_before_kernel_import=True,
            final_fresh_preparation_verified_paths=verification_count,
            preparation_budget=elapsed(started),
            clock_policy=dict(
                CPU_includes_actual_process_bootstrap=True,
                wall_includes_actual_GetProcessTimes_creation=True,
                actual_process_creation_FILETIME_ticks=_PROCESS_CREATION_TICKS,
                monotonic_origin_derived_from_creation_UTC_observation=True,
            ),
            no_numerical_kernel_source_walk_or_bound_executed_in_prepare=True,
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
        require(output == OUTPUT and output.is_dir(), "Exact prepared output")
        require(
            not any(
                (output / name).exists()
                for name in (
                    "manifest.json",
                    "run_started.json",
                    "FAILED_UNSEALED.json",
                    "failure.json",
                )
            ),
            "No reused run or failed preparation",
        )
        admitted = True
        protocol = read(output / "protocol.json", started)
        prepared = read(output / "PREPARED_RECEIPT.json", started)
        require(
            prepared["prepared"] is True and prepared["terminal"] is False,
            "Actual preparation record",
        )
        require(
            sha(output / "protocol.json", started) == prepared["protocol_sha256"],
            "Prepared protocol immutable",
        )
        require(
            protocol["schema"] == "box-muller-polar-cdf-bv-protocol-v1", "Prepared protocol schema"
        )
        same(
            [
                protocol["process_CPU_seconds"],
                protocol["admission_process_CPU_seconds"],
                protocol["wall_seconds"],
            ],
            [180, 150, 600],
            "Fixed all-inclusive run budget",
        )
        require(
            protocol["primary_interval_decimal_digits"] == 90
            and protocol["fixture_credit"] == 0
            and protocol["numerical_threads"] == 1
            and protocol["startup_B_required"] is True
            and protocol["pure_Python_mpmath_backend_required"] is True
            and protocol["cosine_512_envelope_computed"] is False,
            "Prepared numerical policy",
        )
        for field, external_map in (("frozen_inputs", False), ("external_runtime_inputs", True)):
            require(type(protocol[field]) is dict, "Complete recognized protocol input map")
            for key, expected in protocol[field].items():
                budget(started)
                path = Path(key) if external_map else ROOT / key
                require(
                    path.is_absolute() if external_map else not Path(key).is_absolute(),
                    "Exact map path convention",
                )
                bind(frozen, external, path, expected, started)
        for path in (
            output / "protocol.json",
            output / "PREPARED_RECEIPT.json",
            output / "selected_source_origins.json",
            output / "native_root_provenance.json",
            output / "interpreter.json",
        ):
            bind(frozen, external, path, sha(path, started), started)
        implementation = implementation_policy(started)
        same(
            implementation["author_sha256"],
            protocol["immutable_author_sha256"],
            "Prepared immutable authors",
        )
        plan, origins = selected_sources(frozen, external, started)
        root_origins = root_provenance(implementation, frozen, external, started)
        same(
            root_origins,
            read(output / "native_root_provenance.json", started),
            "Prepared native root owner memberships",
        )
        same(
            implementation["additional_native_root_provenance_SHA256"],
            protocol["additional_native_root_provenance_SHA256"],
            "Prepared native root provenance pins",
        )
        same(
            plan["source_bindings_SHA256"],
            protocol["selected_source_SHA256"],
            "Exactly fixed17 input pins",
        )
        same(
            origins,
            read(output / "selected_source_origins.json", started),
            "Actual selected owner provenance",
        )
        interpreter = read(output / "interpreter.json", started)
        same(interpreter, protocol["interpreter"], "Prepared interpreter record")
        runtime_policy(interpreter, started)
        verify_loaded(frozen, external, started)
        verify(frozen, external, started)
        budget(started, admission=True)
        save(
            output / "run_started.json",
            dict(
                UTC=datetime.now(timezone.utc).isoformat(),
                process_id=os.getpid(),
                limits=[180, 150, 600],
            ),
            started,
        )
        require("mpmath" not in sys.modules, "Deferred fresh pure-Python interval import")
        import mpmath as mp

        require(
            mp.__version__ == "1.3.0" and sys.modules["mpmath.libmp.backend"].BACKEND == "python",
            "Actual pure Python mpmath backend",
        )
        mp.iv.dps, mp.mp.dps = 90, 90
        verify_loaded(frozen, external, started)
        budget(started, admission=True)
        binding, rows, ln2 = bind_actual_sources(started)
        save(output / "source_binding.json", binding, started)
        budget(started, admission=True)
        envelope, B, D_S = log_radius_envelope(mp, rows, ln2, started)
        save(output / "log_radius_envelope.json", envelope, started)
        budget(started, admission=True)
        obligations = method_obligations(started)
        save(output / "method_obligations.json", obligations, started)
        guards = angular_guards(B, binding, started)
        save(output / "angular_guards.json", guards, started)
        passed = guards["all_strict_guards_passed"]
        if passed:
            budget(started, admission=True)
            save(
                output / "ideal_hybrid_bounds.json",
                ideal_hybrid_bounds(mp, D_S, guards, started),
                started,
            )
        runtime_policy(interpreter, started)
        loaded = verify_loaded(frozen, external, started)
        save(output / "loaded_module_origins.json", loaded, started)
        summary = dict(
            schema="box-muller-polar-cdf-bv-summary-v1",
            completed=True,
            passed=passed,
            rejection=not passed,
            budget_censored=False,
            status="ideal_hybrid_component_passed" if passed else "rejected_angular_guard",
            complete_actual_pair_counts={case: count for case, (_, _, count) in CASES.items()},
            log_coefficients_recomputed=288,
            log_segments=32,
            midpoint_exponent_classes=33,
            squared_radius_CDF_retained=True,
            angular_dollar_certificate_retained=passed,
            new_test_credit=0,
            all_fixture_credit=0,
            full_G2=False,
            native_financial_bridge_open=True,
            residual_spent_or_reallocated=False,
            native_cosine_envelope_computed=False,
            cost_transfer=False,
            adoption=False,
            basis_or_circuit_or_price_estimator_replays=0,
            budget=elapsed(started),
            source_expected_hashes_waived=False,
        )
        save(output / "summary.json", summary, started)
        seal(
            output,
            frozen,
            external,
            started,
            dict(
                completed=True,
                passed=passed,
                rejection=not passed,
                budget_censored=False,
                phase="run",
                summary_file="summary.json",
                status=summary["status"],
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
    require(output == OUTPUT, "Only exact prospective producer receipt")
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
