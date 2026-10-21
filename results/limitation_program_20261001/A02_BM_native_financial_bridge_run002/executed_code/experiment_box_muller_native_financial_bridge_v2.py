"""Prospective original Box-Muller continuous-to-native financial bias bridge.

Preparation is standard-library bookkeeping only. The run defers mpmath and
source kernels until immutable runtime/input verification and actual independently
passing polar packets. Source/cost adoption and complete estimator G2 remain open.
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
from math import factorial
import os
from pathlib import Path
import site
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
OUTPUT = PROGRAM / "A02_BM_native_financial_bridge_run002"
POLAR_SOURCE = PROGRAM / "A02_polar_cdf_bv_run003"
POLAR_AUDIT = PROGRAM / "A02_polar_cdf_bv_audit_run003"
METHOD = RESEARCH / "box_muller_native_financial_bridge_preflight_v2.json"
METHOD_DOC = RESEARCH / "BOX_MULLER_NATIVE_FINANCIAL_BRIDGE_PREFLIGHT_V2.md"
IMPLEMENTATION = RESEARCH / "box_muller_native_financial_bridge_implementation_preflight_v2.json"
IMPLEMENTATION_DOC = RESEARCH / "BOX_MULLER_NATIVE_FINANCIAL_BRIDGE_IMPLEMENTATION_PREFLIGHT_V2.md"
PRODUCER = RESEARCH / "experiment_box_muller_native_financial_bridge_v2.py"
AUDITOR = RESEARCH / "audit_box_muller_native_financial_bridge_v2.py"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
METHOD_SHA = "263dbcd26beea4d4337e67f648e667663a0b666ee4a4986b69914c44645c2ce8"
METHOD_DOC_SHA = "b999f56da7eeb68ddee96e14260d96dd99a69cadf3157b2524908a3960b53c74"
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
PRIOR_BRIDGE = PROGRAM / "A02_BM_native_financial_bridge_run001"
PRIOR_BRIDGE_REVIEW = PROGRAM / "A02_BM_native_financial_bridge_root_review_run001"
PRIOR_BRIDGE_FAILURE_SHA = "8beb20bfe88407479953ddd7be284fd8fe94cea1e964c392340c4ab1a2376e02"
PRIOR_BRIDGE_REVIEW_SHA = "60c5c37bed87950e555ed89e09176ce2f87a1cb3daffd481111b17572ded316c"
PRIOR_BRIDGE_AUTHORS = {
    "experiment_box_muller_native_financial_bridge.py": (
        "3293ed961b1466e10d3cc256682da216c4c8556049fb9925da1ce66c3c2dead9"
    ),
    "audit_box_muller_native_financial_bridge.py": (
        "6d24237826b9b39a0d1d2cf1c587a19cdff871ac3af4a9ea42317ae32d2706a4"
    ),
    "BOX_MULLER_NATIVE_FINANCIAL_BRIDGE_IMPLEMENTATION_PREFLIGHT.md": (
        "b4723a4259bd1a07be544e4d1a3c5293f6a2f9034d3ae2b2844a31131f4f0ec9"
    ),
    "box_muller_native_financial_bridge_implementation_preflight.json": (
        "ade363c31239a265fd72ea8a3bb362b07eb83a9ce012df4726f66bc0ceb66807"
    ),
}
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
        raise BudgetCensoredError("Fixed native bridge 180CPU/150admission/600wall budget")
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
                "research.limitation_program_20261001.experiment_box_muller_native_financial_bridge_v2",
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
    require(
        plan["schema"] == "original-box-muller-native-financial-bridge-author-preflight-v2"
        and plan["status"] == "HELD_AUTHOR_ONLY_ROUTE_CORRECTION_NO_EXECUTION",
        "Held route-only original method plan",
    )
    pins = plan["original_selected_source_pins_from_existing_manifest_metadata"]
    require(len(pins) == 25, "Exactly fixed25 selected source pins")
    owners = []
    for key, expected in pins.items():
        if key.endswith("/manifest.json"):
            manifest_path = bind(frozen, external, ROOT / key, expected, started)
            data = read(manifest_path, started)
            rows = owner_rows(manifest_path, data, started)
            owners.append((key, rows))
    require(len(owners) == 5, "Five pinned original owner manifests, not self-membership")
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
    require(len(origins) == 20, "All20 nonmanifest selected origins are accounted for")
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
    reports, graphs, common_table, common_ln2 = {}, {}, None, None
    for case, (assets, dates, pairs) in CASES.items():
        budget(started, admission=True)
        binding = certificate["source_bindings"][case]
        target_path = PROGRAM / "A10_coefficient_run001" / case / "min-depth/target.json"
        require(ROOT / binding["target"] == target_path, "Original C06 target route")
        target = read(target_path, started)
        source = read(target_path.parent / "source.json", started)
        graph = ActualGraph(target, started)
        graphs[case] = graph
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
        graphs,
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


def polar_packets(implementation, frozen, external, started):
    """Admit existing actual packets; no source walk or interval evaluation here."""
    pins = implementation["required_polar_manifest_SHA256"]
    expected_keys = {
        (receipt / "manifest.json").relative_to(ROOT).as_posix()
        for receipt in (POLAR_SOURCE, POLAR_AUDIT)
    }
    require(
        type(pins) is dict and set(pins) == expected_keys,
        "Both exact polar prerequisite manifest pins required",
    )
    packets = {}
    for receipt, schema in (
        (POLAR_SOURCE, "box-muller-polar-cdf-bv-terminal-manifest-v1"),
        (POLAR_AUDIT, "box-muller-polar-cdf-bv-independent-audit-manifest-v1"),
    ):
        budget(started)
        require(
            receipt.is_dir()
            and not any(
                (receipt / marker).exists() for marker in ("FAILED_UNSEALED.json", "failure.json")
            ),
            "Actual passing polar packet, never failed or partial evidence",
        )
        manifest_path = receipt / "manifest.json"
        pin = pins[manifest_path.relative_to(ROOT).as_posix()]
        require(type(pin) is str and len(pin) == 64, "Null actual polar pin blocks prepare")
        bind(frozen, external, manifest_path, pin, started)
        manifest = read(manifest_path, started)
        require(
            manifest["schema"] == schema
            and manifest["manifest_self_hash_excluded"] is True
            and manifest["terminal_outcome_file"] == "completion_outcome.json"
            and manifest["completed"] is True
            and manifest["passed"] is True
            and manifest["budget_censored"] is False
            and manifest["original_expected_hashes_waived"] is False
            and manifest["verification_and_output_hashing_before_terminal"] is True,
            "Complete uncensored actual prerequisite PASS",
        )
        same(
            manifest["historical_global_LIVE_integrity"],
            dict(
                passed=False, mismatch_references=36, distinct_paths=9, expected_hashes_waived=False
            ),
            "Historical LIVE defects remain separate",
        )
        files = manifest["files"]
        require(
            type(files) is dict and 0 < len(files) <= 64, "Finite complete receipt-local owned map"
        )
        found, total = set(), 0
        for candidate in receipt.rglob("*"):
            budget(started)
            if candidate.is_file():
                actual = resolved(candidate, started)
                require(actual.is_relative_to(receipt), "Polar owned directory confinement")
                key = actual.relative_to(receipt).as_posix()
                require(key not in found, "No aliased polar owned file")
                found.add(key)
                total += actual.stat().st_size
        require(
            found == set(files) | {"manifest.json"} and total <= 128 * 1024**2,
            "Every actual polar owned byte, including terminal outcome",
        )
        for key, expected in files.items():
            budget(started)
            require(
                type(key) is str and not Path(key).is_absolute() and key != "manifest.json",
                "Explicit receipt-local owned map schema",
            )
            actual = bind(frozen, external, receipt / key, expected, started)
            require(
                actual.is_relative_to(receipt) and actual.relative_to(receipt).as_posix() == key,
                "Exact rebased canonical polar owned path",
            )
        for field, is_external in (("frozen_inputs", False), ("external_runtime_inputs", True)):
            mapping = manifest[field]
            require(type(mapping) is dict, "Complete polar frozen/external map")
            for key, expected in mapping.items():
                budget(started)
                require(
                    type(key) is str and Path(key).is_absolute() is is_external,
                    "ROOT-relative versus separately scoped external map convention",
                )
                actual = bind(
                    frozen, external, Path(key) if is_external else ROOT / key, expected, started
                )
                canonical_key = str(actual) if is_external else actual.relative_to(ROOT).as_posix()
                require(
                    canonical_key == key and actual.is_relative_to(ROOT) is not is_external,
                    "Strict canonical complete prerequisite map",
                )
        protocol = read(receipt / "protocol.json", started)
        for field in ("frozen_inputs", "external_runtime_inputs"):
            require(type(protocol[field]) is dict, "Actual prerequisite preparation map")
            for key, expected in protocol[field].items():
                budget(started)
                require(
                    manifest[field].get(key) == expected, "No prepared prerequisite byte dropped"
                )
        same(
            [
                protocol[name]
                for name in ("process_CPU_seconds", "admission_process_CPU_seconds", "wall_seconds")
            ],
            [180, 150, 600],
            "Actual polar fixed budgets",
        )
        outcome, summary = (
            read(receipt / name, started) for name in ("completion_outcome.json", "summary.json")
        )
        for value in (outcome, summary):
            require(
                value["completed"] is True
                and value["passed"] is True
                and value["budget_censored"] is False
                and value["new_test_credit"] == 0
                and value["full_G2"] is False
                and value["adoption"] is False
                and value["cost_transfer"] is False,
                "Actual hybrid-only uncensored PASS",
            )
        if receipt == POLAR_SOURCE:
            require(
                summary["rejection"] is False
                and summary["angular_dollar_certificate_retained"] is True,
                "Rejected primary polar component cannot admit bridge",
            )
        else:
            require(
                summary["independent_audit_passed"] is True
                and summary["ideal_hybrid_component_passed"] is True
                and summary["source_passed"] is True
                and summary["source_rejection_retained"] is False,
                "Independent polar audit actually approves same component",
            )
        for value in (
            outcome["budget"],
            summary["budget"],
            manifest["terminal_budget_observation"],
        ):
            require(
                0 <= value["process_CPU_seconds"] < CPU and 0 <= value["wall_seconds"] < WALL,
                "Actual prerequisite terminal hard limits",
            )
        for name, expected in implementation["required_polar_author_SHA256"].items():
            budget(started)
            require(
                sha(receipt / "executed_code" / name, started) == expected,
                "Actual independently reviewed polar executable copies",
            )
        packets[receipt.name] = dict(
            manifest_sha256=pin, protocol=protocol, summary=summary, outcome=outcome
        )
    source = {
        name: read(POLAR_SOURCE / name, started)
        for name in (
            "source_binding.json",
            "log_radius_envelope.json",
            "angular_guards.json",
            "ideal_hybrid_bounds.json",
        )
    }
    independent = {
        name: read(POLAR_AUDIT / name, started)
        for name in (
            "independent_source_binding.json",
            "independent130_log_radius_envelope.json",
            "independent_angular_guards.json",
            "independent130_ideal_hybrid_bounds.json",
        )
    }
    same(
        source["source_binding.json"],
        independent["independent_source_binding.json"],
        "Actual independently confirmed source/role/root binding",
    )
    return dict(packets=packets, source=source, independent=independent)


def operational_provenance(plan, frozen, external, started):
    """Retain complete actual metadata packets and both method generations, zero credit."""
    policy = plan["operational_v2_provenance"]
    require(
        policy["route_only_change_mathematical_contract_unchanged"] is True
        and policy["no_expected_hash_override_or_old_failure_reclassification"] is True,
        "Held route correction preserves the original mathematical contract",
    )
    for field in (
        "original_method_SHA256",
        "original_polar_author_SHA256",
        "original_polar_v2_author_SHA256",
    ):
        require(
            type(policy[field]) is dict and policy[field], "Strict actual prior author inventory"
        )
        for key, expected in policy[field].items():
            budget(started)
            actual = bind(frozen, external, ROOT / key, expected, started)
            require(actual.relative_to(ROOT).as_posix() == key, "Canonical prior author path")
    for label in (
        "A02_polar_cdf_bv_run001",
        "A02_polar_cdf_bv_audit_run001",
        "A02_polar_cdf_bv_run002",
        "A02_polar_cdf_bv_audit_run002",
    ):
        require(not (PROGRAM / label).exists(), "Actual prior pre-mkdir failures remain absent")
    reports = []
    for row in policy["prior_metadata_packets"]:
        budget(started)
        require(row["scientific_or_fixture_credit"] == 0, "No prior metadata promoted to science")
        receipt = resolved(ROOT / row["receipt"], started)
        require(receipt.is_relative_to(PROGRAM), "Finite declared operational receipt")
        mf_path = bind(frozen, external, receipt / "manifest.json", row["manifest_SHA256"], started)
        manifest = read(mf_path, started)
        require(
            manifest["manifest_self_hash_excluded"] is True
            and [len(manifest["files"]), len(manifest["frozen_inputs"])]
            == row["owned_frozen_counts"],
            "Exact complete actual metadata maps, not a fabricated runtime map",
        )
        owned = set()
        for field in ("files", "frozen_inputs"):
            require(type(manifest[field]) is dict, "Declared complete metadata map schema")
            for key, expected in manifest[field].items():
                budget(started)
                require(
                    type(key) is str and not Path(key).is_absolute(), "Operational ROOT-key map"
                )
                actual = bind(frozen, external, ROOT / key, expected, started)
                require(
                    actual.relative_to(ROOT).as_posix() == key,
                    "Canonical strict equal-SHA metadata merge",
                )
                if field == "files":
                    require(actual.is_relative_to(receipt), "Metadata owned bytes stay in receipt")
                    owned.add(actual.relative_to(receipt).as_posix())
        found = set()
        for path in receipt.rglob("*"):
            budget(started)
            if path.is_file():
                actual = resolved(path, started)
                require(actual.is_relative_to(receipt), "Metadata directory byte confinement")
                key = actual.relative_to(receipt).as_posix()
                require(key not in found, "No metadata byte alias")
                found.add(key)
        require(found == owned | {"manifest.json"}, "All actual owned metadata bytes accounted for")
        reports.append(
            dict(
                receipt=row["receipt"],
                manifest_sha256=row["manifest_SHA256"],
                owned_frozen_counts=row["owned_frozen_counts"],
                scientific_or_fixture_credit=0,
            )
        )
    return reports


def support_evidence(binding, graphs, started):
    """Reuse source-identical universal support, with fresh actual shape binding."""
    reports = {}
    for case, (assets, dates, _) in CASES.items():
        budget(started)
        certificate = read(PROGRAM / "E03_support_run001" / (case + "_certificate.json"), started)
        audit = read(PROGRAM / "E03_support_audit_run002" / (case + "_audit.json"), started)
        roles = binding["cases"][case]["financial_roles"]
        graph = graphs[case]
        stocks = sorted(row["stock"] for row in roles["prefix_witnesses"])
        require(
            certificate["complete_builder_equality"] is True
            and certificate["all_original_uniform_word_patterns"] is True
            and certificate["stock_support"]["all_clipped_integer_inputs"] is True
            and certificate["stock_support"]["positive_and_no_native_overflow"] is True
            and certificate["all_stock_tree_sums_no_overflow"] is True,
            "Original universal support, never finite samples or builder imports",
        )
        require(
            audit["passed"] is True
            and audit["assets"] == assets
            and audit["dates"] == dates
            and audit["actual_stock_templates_checked"] == assets * dates
            and audit["all_stock_native_intermediates_no_overflow"] is True
            and audit["all_actual_sum_max_average_subtract_discount_nodes_safe"] is True
            and audit["finite_samples_used"] is False
            and audit["new_financial_gate_replays"] == 0,
            "Previously independent actual-SSA support audit",
        )
        same(sorted(certificate["stock_ids"]), stocks, "Actual original stock identity inventory")
        same(
            certificate["target_output"], graph.target["outputs"], "Exact original financial output"
        )
        alive, payoff, _ = graph.node(graph.target["outputs"]["Y"], "select")["args"]
        discount = graph.node(payoff, "cmul")["params"]["c"]
        average, strike = graph.node(
            graph.node(graph.node(payoff, "cmul")["args"][0], "positive")["args"][0], "sub"
        )["args"]
        c_average = graph.node(average, "cmul")["params"]["c"]
        graph.const(strike, 100 * Q)
        graph.const(graph.node(alive, "lt")["args"][1], 140 * Q)
        require(
            certificate["basket_coefficient"] == Q // assets
            and certificate["average_coefficient"] == c_average
            and certificate["discount_coefficient"] == discount
            and certificate["strict_barrier_raw"] == 140 * Q
            and certificate["strike_raw"] == 100 * Q,
            "All actual financial literal premises",
        )
        guard(0 < discount <= Q, "Native discount must lie in (0,1]")
        total_upper = assets * dates * 140 * Q - dates
        average_upper = total_upper * c_average // Q
        native_cap_raw = max(0, average_upper - 100 * Q) * discount // Q
        same(
            certificate["payoff_raw_bounds"],
            [0, native_cap_raw],
            "Fresh strict-integer survival and native payoff cap",
        )
        same(audit["payoff_raw_bounds"], [0, native_cap_raw], "Independent original support cap")
        guard(0 <= native_cap_raw < 40 * Q, "Both actual nonnegative payoffs supported below40")
        reports[case] = dict(
            certificate=certificate,
            independent_support_audit=audit,
            stock_raw_support_bounds=[
                certificate["stock_support"]["lower"],
                certificate["stock_support"]["upper"],
            ],
            native_cap_upper=encode(Fraction(native_cap_raw, Q)),
            actual_average_literal=c_average,
            actual_discount_literal=discount,
            strict_surviving_unrounded_stock_sum_raw_upper=total_upper,
            strict_integer_survival_sum_proved=True,
            original_universal_support_source_identical=True,
            historical_builder_or_AS241_certificate_imported=False,
        )
    return reports


def cosine_envelope(mp, graphs, B, started):
    """All512 original literal errors are paid; no nearest-half-ULP predicate."""
    table = graphs["B4x12"].target["tables"]["cos"]
    same(table, graphs["B8x52"].target["tables"]["cos"], "Both original cosine tables")
    require(len(table) == 64 and all(len(row) == 8 for row in table), "Actual64x8 cosine inventory")
    pi = mp.iv.pi
    radius = Fraction(1, 128)
    records, row_errors, native_steps = [], [], []
    for row_index, row in enumerate(table):
        budget(started)
        center = Fraction(2 * row_index + 1, 128)
        errors = []
        for degree, word in enumerate(row):
            budget(started)
            require(
                type(word) is int and -(1 << 71) <= word < 1 << 71,
                "Canonical actual signed72 cosine coefficient",
            )
            true_coefficient = (
                (2 * pi) ** degree
                * mp.iv.cos(2 * pi * iv(mp, center) + degree * pi / 2)
                / factorial(degree)
            )
            error = absolute_error(word, true_coefficient)
            errors.append(error)
            records.append(
                dict(
                    row=row_index,
                    degree=degree,
                    raw=word,
                    exact_coefficient_enclosure=[encode(v) for v in interval(true_coefficient)],
                    actual_literal_error_upper=encode(error),
                )
            )
        row_errors.append(
            sum((error * radius**degree for degree, error in enumerate(errors)), Fraction(0))
        )
        magnitude = Fraction(abs(row[-1]), Q)
        steps = []
        for degree in range(6, -1, -1):
            budget(started)
            guard(magnitude * radius * Q * Q < 1 << 143, "Actual cosine full signed144 product")
            magnitude = magnitude * radius + EPSILON + Fraction(abs(row[degree]), Q)
            guard(magnitude * Q < 1 << 71, "Actual cosine stored72 Horner step")
            steps.append(dict(degree=degree, magnitude_upper=encode(magnitude)))
        native_steps.append(dict(row=row_index, steps=steps))
    remainder = upper((2 * pi) ** 8 * iv(mp, radius) ** 8 / factorial(8))
    literal_error = max(row_errors)
    floors = EPSILON * sum((radius**power for power in range(7)), Fraction(0))
    E_cos = remainder + literal_error + floors
    delta_Z = B * E_cos + EPSILON
    native_abs = B * (1 + E_cos) + EPSILON
    guard(
        native_abs * Q < 1 << 71 and B * (1 + E_cos) * Q * Q < 1 << 143,
        "Actual final signed radius product and stored72 normal safety",
    )
    return dict(
        schema="original-BM-cosine-arithmetic-envelope-v1",
        interval_digits=90,
        coefficient_count=512,
        coefficient_checks=records,
        local_absolute_radius=encode(radius),
        native_Horner_steps=native_steps,
        Taylor_degree7_remainder_upper=encode(remainder),
        literal_rounding_upper=encode(literal_error),
        Horner_floor_upper=encode(floors),
        cosine_error_upper=encode(E_cos),
        pinned_native_radius_upper=encode(B),
        remaining_coordinate_error_upper=encode(delta_Z),
        native_normal_absolute_upper=encode(native_abs),
        exact_midpoint_and_positive_sine_quarter_wrap=True,
        absent_rounded_two_pi_multiply_not_charged=True,
        final_signed_product_floor_upper=encode(EPSILON),
        old_radius_Holder_log_root_or_grid_terms_added_again=False,
        all_actual_coefficients_paid_without_half_ULP_assumption=True,
        all_product144_and_stored72_guards_passed=True,
    )


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


def stock_exponential_envelopes(mp, graphs, binding, supports, started):
    reports = {}
    for case, (assets, dates, _) in CASES.items():
        budget(started, admission=True)
        graph, certificate = graphs[case], supports[case]["certificate"]
        sites = [
            stock_site(graph, row["stock"], row["raw_log"], started)
            for row in binding["cases"][case]["financial_roles"]["prefix_witnesses"]
        ]
        first = sites[0]
        for stock_scope in sites:
            budget(started)
            require(
                stock_scope["actual_original_support_signature"]
                == supports[case]["independent_support_audit"]["actual_stock_template_signature"],
                "Every fresh original stock matches independent actual-source support",
            )
            same(
                [stock_scope[key] for key in ("low", "high", "inverse_ln2", "ln2")],
                [first[key] for key in ("low", "high", "inverse_ln2", "ln2")],
                "All actual original stock range literals",
            )
        lo, hi, cinv, cln = (first[key] for key in ("low", "high", "inverse_ln2", "ln2"))
        require(
            [lo, hi] == certificate["clipped_log_integer_bounds"]
            and cinv == certificate["literal_inverse_ln2"]
            and cln == certificate["literal_ln2"],
            "Original support literal identity, signed clamp decode",
        )
        guard(
            cinv > 0
            and cln > 0
            and lo < hi
            and -17 <= lo * cinv // (Q * Q) <= hi * cinv // (Q * Q) <= 12,
            "Actual clipped exponent domain contained in unchanged fixed30 classes",
        )
        ln_error = absolute_error(cln, mp.iv.log(iv(mp, 2)))
        rows, occupied, alpha, clamp_stock = [], [], Fraction(0), None
        for k in range(-17, 13):
            budget(started)
            left = max(lo, -((-k * Q * Q) // cinv))
            right = min(hi, -((-(k + 1) * Q * Q) // cinv) - 1)
            if left > right:
                rows.append(dict(k=k, empty=True, clipped_log_raw_bounds=[left, right]))
                continue
            ranges, products = integer_stock_cell(graph, first, left, right, k, started)
            remainder = ranges[first["remainder"]]
            radius = Fraction(max(abs(v) for v in remainder), Q)
            coefficients, floors, literals, steps = sparse_stock_model(
                graph, first, radius, started
            )
            same(
                [encode(coefficients[d]) for d in range(13)],
                [encode(Fraction(word, Q)) for word in certificate["literal_exp_coefficients"]],
                "All13 degree coefficients freshly recovered from actual Estrin DAG",
            )
            Taylor = upper(mp.iv.exp(iv(mp, radius)) * iv(mp, radius) ** 13 / factorial(13))
            E_k = floors + literals + Taylor
            relative = upper(
                mp.iv.exp(iv(mp, abs(k) * ln_error))
                * (1 + iv(mp, E_k) * mp.iv.exp(-iv(mp, Fraction(remainder[0], Q))))
                - 1
            )
            alpha = max(alpha, relative)
            row = dict(
                k=k,
                empty=False,
                clipped_log_raw_bounds=[left, right],
                remainder_raw_bounds=list(remainder),
                polynomial_raw_bounds=list(ranges[first["polynomial"]]),
                stock_raw_bounds=list(ranges[first["stock"]]),
                actual_polynomial_coefficients=[encode(coefficients[d]) for d in range(13)],
                polynomial_literal_error_upper=encode(literals),
                polynomial_native_floor_error_upper=encode(floors),
                Taylor_degree12_remainder_upper=encode(Taylor),
                polynomial_error_upper=encode(E_k),
                ln2_literal_error_upper=encode(ln_error),
                relative_stock_error_upper=encode(relative),
                polynomial_floor_and_range_steps=steps,
                signed144_products=products,
                all_actual_native_intermediates_signed72_safe=True,
                k_times_ln2_extra_rounding=0,
            )
            rows.append(row)
            occupied.append(row)
            if left <= hi <= right:
                point, _ = integer_stock_cell(graph, first, hi, hi, k, started)
                require(
                    point[first["stock"]][0] == point[first["stock"]][1], "Exact upper-clamp point"
                )
                clamp_stock = point[first["stock"]][0]
        require(
            occupied
            and occupied[0]["clipped_log_raw_bounds"][0] == lo
            and occupied[-1]["clipped_log_raw_bounds"][1] == hi
            and all(
                a["clipped_log_raw_bounds"][1] + 1 == b["clipped_log_raw_bounds"][0]
                for a, b in zip(occupied, occupied[1:])
            ),
            "Whole integer clipped domain without gap/overlap",
        )
        guard(
            0 <= alpha < 1 and clamp_stock is not None,
            "Positive multiplicative native stock envelope",
        )
        reports[case] = dict(
            actual_stock_sites=assets * dates,
            actual_sites=sites,
            fixed_exponent_superset=[-17, 12],
            retained_classes=30,
            classes=rows,
            whole_clipped_integer_domain_covered=True,
            alpha_upper=encode(alpha),
            beta_upper=encode(EPSILON),
            lower_clamp_raw=lo,
            upper_clamp_raw=hi,
            actual_native_upper_clamp_stock_raw=clamp_stock,
            all_positive_stock_stored72_product144_shift_guards_passed=True,
            final_negative_shift_floor_charged_once=True,
            AS241_financial_theorem_transferred=False,
        )
    return dict(
        schema="original-BM-stock-exponential-envelopes-v1", interval_digits=90, cases=reports
    )


def ceil_fraction(value):
    value = Fraction(value)
    return -(-value.numerator // value.denominator)


def raw_log_prefix_envelopes(mp, graphs, binding, cosine, B, started):
    """Bound every actual raw partial sum before any clamp or survivor restriction."""
    delta = exact(cosine["remaining_coordinate_error_upper"])
    native_absolute = exact(cosine["native_normal_absolute_upper"])
    normal_raw_limit = ceil_fraction(native_absolute * Q)
    guard(
        0 <= B and 0 <= delta and normal_raw_limit < 1 << 71,
        "Pinned internal radius and remaining coordinate envelope",
    )
    reports = {}
    for case, (assets, dates, pairs) in CASES.items():
        budget(started, admission=True)
        graph = graphs[case]
        roles = binding["cases"][case]["financial_roles"]
        normal_ids = [
            value
            for scope in binding["cases"][case]["joint_pair_scopes"]
            for value in scope["normal_values"]
        ]
        require(
            len(normal_ids) == 2 * pairs and len(set(normal_ids)) == len(normal_ids),
            "Whole original pair coordinates supply the raw prefix stops",
        )
        ranges = {value: (-normal_raw_limit, normal_raw_limit) for value in normal_ids}
        selected, pending = set(), [row["raw_log"] for row in roles["prefix_witnesses"]]
        while pending:
            budget(started)
            value = pending.pop()
            if value in ranges or value in selected:
                continue
            node = graph.node(value)
            require(
                node["op"] in ("add", "const", "cmul"),
                "Fresh raw logs contain only original additions/constants/scaled normals",
            )
            if node["op"] == "cmul":
                require(
                    node["args"][0] in ranges, "Every raw cmul acts directly on one original normal"
                )
            selected.add(value)
            pending.extend(node["args"])
        product_rows, intermediate_rows = [], []
        for value in sorted(selected):
            budget(started)
            node = graph.node(value)
            if node["op"] == "const":
                result = (graph.const(value),) * 2
            elif node["op"] == "cmul":
                source = ranges[node["args"][0]]
                coefficient = node["params"]["c"]
                endpoints = [word * coefficient for word in source]
                product = product_range((min(endpoints), max(endpoints)))
                product_rows.append(dict(value=value, product_raw_bounds=list(product)))
                result = (product[0] // Q, product[1] // Q)
            else:
                first, second = [ranges[arg] for arg in node["args"]]
                result = (first[0] + second[0], first[1] + second[1])
            ranges[value] = signed_range(result)
            intermediate_rows.append(dict(value=value, op=node["op"], raw_bounds=list(result)))
        a_word, b_word, mu_word, initial_word = [
            roles[field]
            for field in (
                "actual_common_literal",
                "actual_idio_literal",
                "actual_drift_literal",
                "actual_initial_literal",
            )
        ]
        true_a = mp.iv.sqrt(iv(mp, Fraction(9, 250 * dates)))
        true_b = mp.iv.sqrt(iv(mp, Fraction(27, 500 * dates)))
        true_mu = Fraction(-3, 200 * dates)
        e_a, e_b = absolute_error(a_word, true_a), absolute_error(b_word, true_b)
        e_mu = abs(Fraction(mu_word, Q) - true_mu)
        e_initial = absolute_error(initial_word, mp.iv.log(iv(mp, 100)))
        per_increment = (
            (abs(Fraction(a_word, Q)) + abs(Fraction(b_word, Q))) * delta
            + (e_a + e_b) * B
            + e_mu
            + 2 * EPSILON
        )
        prefix_rows = []
        for date in range(dates):
            budget(started)
            witnesses = sorted(
                (row for row in roles["prefix_witnesses"] if row["date"] == date),
                key=lambda row: row["asset"],
            )
            require(
                len(witnesses) == assets
                and [row["asset"] for row in witnesses] == list(range(assets)),
                "Every asset/date raw prefix proved",
            )
            lam = e_initial + (date + 1) * per_increment
            guard(lam >= 0, "Nonnegative uniform native-to-ideal raw log envelope")
            prefix_rows.append(
                dict(
                    date=date,
                    elapsed_dates=date + 1,
                    lambda_upper=encode(lam),
                    actual_raw_log_sites=[row["raw_log"] for row in witnesses],
                    actual_raw_log_bounds=[list(ranges[row["raw_log"]]) for row in witnesses],
                    original_driver_count_per_stock=2 * (date + 1),
                    original_driver_multiplicity=1,
                    original_drift_multiplicity=date + 1,
                )
            )
        reports[case] = dict(
            actual_common_literal=a_word,
            actual_idio_literal=b_word,
            actual_drift_literal=mu_word,
            actual_initial_literal=initial_word,
            exact_common_coefficient_enclosure=[encode(v) for v in interval(true_a)],
            exact_idio_coefficient_enclosure=[encode(v) for v in interval(true_b)],
            exact_drift=encode(true_mu),
            common_literal_error_upper=encode(e_a),
            idio_literal_error_upper=encode(e_b),
            drift_literal_error_upper=encode(e_mu),
            initial_log_spot_error_upper=encode(e_initial),
            per_increment_error_upper=encode(per_increment),
            normal_raw_absolute_upper=normal_raw_limit,
            native_partial_sum_inventory=intermediate_rows,
            native_full144_product_inventory=product_rows,
            prefixes=prefix_rows,
            every_stored72_raw_partial_sum_safe=True,
            every_signed144_scaled_normal_product_safe=True,
            raw_prefix_proof_before_clips_and_survival=True,
            addition_rounding_paid=0,
            signed_scaled_normal_floors_per_increment=2,
            normal_radius_or_grid_error_paid_again=False,
        )
    return dict(
        schema="original-BM-raw-log-prefix-envelopes-v1",
        interval_digits=90,
        pinned_internal_radius_upper=encode(B),
        remaining_coordinate_error_upper=encode(delta),
        cases=reports,
    )


def eager_financial_tail_safety(graph, roles, support, started):
    """Check all actual eager branches after the source-identical stock support."""
    stock_bounds = tuple(support["stock_raw_support_bounds"])
    signed_range(stock_bounds)
    guard(stock_bounds[0] > 0, "Pinned original full clipped-domain positive stock support")
    stocks = {row["stock"] for row in roles["prefix_witnesses"]}
    ranges = {value: stock_bounds for value in stocks}
    selected, pending = set(), [graph.target["outputs"]["Y"]]
    while pending:
        budget(started)
        value = pending.pop()
        if value in ranges or value in selected:
            continue
        node = graph.node(value)
        require(
            node["op"] in ("const", "add", "sub", "cmul", "positive", "lt", "select"),
            "Original actual financial sum/max/average/discount/select closure",
        )
        selected.add(value)
        # Both branches remain eager; no survivor assumption removes an arithmetic path.
        pending.extend(node["args"])
    rows, products = [], []
    for value in sorted(selected):
        budget(started)
        node = graph.node(value)
        op, args = node["op"], [ranges[arg] for arg in node["args"]]
        if op == "const":
            result = (graph.const(value),) * 2
        elif op in ("add", "sub"):
            first, second = args
            result = (
                (first[0] + second[0], first[1] + second[1])
                if op == "add"
                else (first[0] - second[1], first[1] - second[0])
            )
        elif op == "cmul":
            coefficient = node["params"]["c"]
            endpoints = [word * coefficient for word in args[0]]
            product = product_range((min(endpoints), max(endpoints)))
            products.append(dict(value=value, product_raw_bounds=list(product)))
            result = (product[0] // Q, product[1] // Q)
        elif op == "positive":
            result = (max(0, args[0][0]), max(0, args[0][1]))
        elif op == "lt":
            result = (0, 1)
        else:
            require(
                op == "select" and args[0][0] >= 0 and args[0][1] <= 1,
                "Actual unscaled native flag and eager select",
            )
            result = (min(args[1][0], args[2][0]), max(args[1][1], args[2][1]))
        ranges[value] = signed_range(result)
        rows.append(dict(value=value, op=op, raw_bounds=list(result)))
    guard(ranges[graph.target["outputs"]["Y"]][0] >= 0, "Nonnegative actual native payoff")
    return dict(
        stock_raw_bounds=list(stock_bounds),
        actual_eager_tail_nodes=rows,
        actual_full144_products=products,
        all_stored72_and_product144_safe=True,
        both_select_branches_bound=True,
        no_knockout_path_removed=True,
    )


def whole_emitted_finance_safety(graphs, binding, cosine, stocks, started):
    """Fresh topological safety includes emitted dead polynomial powers, such as r16."""
    limit = ceil_fraction(exact(cosine["native_normal_absolute_upper"]) * Q)
    reports = {}
    for case in CASES:
        budget(started, admission=True)
        graph = graphs[case]
        normal_ids = [
            value
            for scope in binding["cases"][case]["joint_pair_scopes"]
            for value in scope["normal_values"]
        ]
        sampler = set()
        for value in normal_ids:
            budget(started)
            sampler.update(graph.ancestors(value))
        output_ancestors = graph.ancestors(graph.target["outputs"]["Y"])
        ranges = {value: (-limit, limit) for value in normal_ids}
        occupied = [row for row in stocks["cases"][case]["classes"] if not row["empty"]]
        remainder_bounds = (
            min(row["remainder_raw_bounds"][0] for row in occupied),
            max(row["remainder_raw_bounds"][1] for row in occupied),
        )
        special_remainders = {site["remainder"] for site in stocks["cases"][case]["actual_sites"]}
        clips = {
            site["clipped"]: (site["low"], site["high"])
            for site in stocks["cases"][case]["actual_sites"]
        }
        rows, products, dead = [], [], []
        for node in graph.target["nodes"]:
            budget(started)
            require(
                len(node["out"]) == 1 or all(value in sampler for value in node["out"]),
                "Every nonsampler emitted node has one native output",
            )
            if node["op"] != "const" and all(value in sampler for value in node["out"]):
                continue
            value = node["out"][0]
            op = node["op"]
            require(
                op
                in (
                    "const",
                    "add",
                    "sub",
                    "mul",
                    "cmul",
                    "bits",
                    "lt",
                    "select",
                    "positive",
                    "shift",
                ),
                "No unproved eager operation outside the whole original sampler closure",
            )
            require(
                all(arg in ranges for arg in node["args"]),
                "Nonsampler source uses original normals/constants, never an unbounded sampler "
                "intermediate",
            )
            args = [ranges[arg] for arg in node["args"]]
            if op == "const":
                result = (graph.const(value),) * 2
            elif op in ("add", "sub"):
                first, second = args
                result = (
                    (first[0] + second[0], first[1] + second[1])
                    if op == "add"
                    else (first[0] - second[1], first[1] - second[0])
                )
                # Each source-identical remainder cell was proved with its exact k correlation.
                if value in special_remainders:
                    result = remainder_bounds
            elif op in ("mul", "cmul"):
                first = args[0]
                second = args[1] if op == "mul" else (node["params"]["c"],) * 2
                corners = [a * b for a in first for b in second]
                lo = (
                    0
                    if op == "mul"
                    and node["args"][0] == node["args"][1]
                    and first[0] <= 0 <= first[1]
                    else min(corners)
                )
                product = product_range((lo, max(corners)))
                products.append(dict(value=value, product_raw_bounds=list(product)))
                result = (product[0] // Q, product[1] // Q)
            elif op == "bits":
                params = node["params"]
                require(params["width"] == 72, "Actual financial full72 bit extraction")
                shift = params["shift"]
                if shift < 0:
                    require(params["signed"] is False, "Exact full72 modular integer left scaling")
                    result = (args[0][0] << -shift, args[0][1] << -shift)
                else:
                    require(
                        params["signed"] is True or args[0][0] >= 0,
                        "Unsigned right extraction has a proved nonnegative source",
                    )
                    result = (args[0][0] >> shift, args[0][1] >> shift)
            elif op == "lt":
                result = (0, 1)
            elif op == "select":
                require(0 <= args[0][0] <= args[0][1] <= 1, "Actual unscaled native flag")
                result = (min(args[1][0], args[2][0]), max(args[1][1], args[2][1]))
                if value in clips:
                    result = clips[value]
            elif op == "positive":
                result = (max(0, args[0][0]), max(0, args[0][1]))
            else:
                require(op == "shift", "Actual financial variable exponent shift")
                first, controls = args
                guard(
                    first[0] > 0 and -72 < controls[0] <= controls[1] < 72,
                    "Every eager positive stock shift has its proved exponent range",
                )
                shift_lo, shift_hi = controls
                result = (
                    first[0] << shift_lo if shift_lo >= 0 else first[0] >> -shift_lo,
                    first[1] << shift_hi if shift_hi >= 0 else first[1] >> -shift_hi,
                )
            ranges[value] = signed_range(result)
            rows.append(
                dict(
                    value=value,
                    op=op,
                    raw_bounds=list(result),
                    exact_cell_correlation_reused=value in special_remainders,
                    exact_clamp_domain_reused=value in clips,
                )
            )
            if value not in output_ancestors and value not in sampler:
                dead.append(value)
        all_values = set(graph.nodes)
        require(
            all_values == sampler | set(ranges),
            "Every actual emitted SSA value is sampler-proved or freshly finance-range-proved",
        )
        reports[case] = dict(
            actual_nonsampler_emitted_ranges=rows,
            actual_nonsampler_signed144_products=products,
            actual_dead_emitted_nonsampler_values=dead,
            full_emitted_value_count=len(all_values),
            sampler_closure_value_count=len(sampler),
            all_emitted_dead_paths_and_polynomial_powers_retained=True,
            no_safety_obligation_dropped_as_unreachable_or_knocked_out=True,
            all_product144_and_stored72_guards_passed=True,
        )
    return dict(schema="original-BM-all-emitted-financial-safety-v1", cases=reports)


def closed_barrier_bands(mp, graphs, binding, prefixes, stocks, supports, polar, DS, started):
    """Two-direction clip discharge, closed ties and whole-pair band transport."""
    reports = {}
    guard(0 <= DS <= 1, "Pinned squared-radius Kolmogorov upper bound")
    guard(
        polar["source"]["angular_guards.json"]["all_strict_guards_passed"] is True,
        "Actual bounded-current-radius angular guards are a prerequisite",
    )
    for case, (assets, dates, pairs) in CASES.items():
        budget(started, admission=True)
        roles = binding["cases"][case]["financial_roles"]
        stock = stocks["cases"][case]
        alpha, beta = exact(stock["alpha_upper"]), exact(stock["beta_upper"])
        L, U = Fraction(stock["lower_clamp_raw"], Q), Fraction(stock["upper_clamp_raw"], Q)
        ell = upper(iv(mp, 1 + alpha) * mp.iv.exp(iv(mp, L))) + beta
        guard(0 <= ell < 140 and beta == EPSILON, "Lower-clamp leakage and final right-shift floor")
        guard(
            stock["actual_native_upper_clamp_stock_raw"] >= assets * 140 * Q,
            "Actual native upper-clamp stock alone knocks out the basket",
        )
        require(
            supports[case]["certificate"]["basket_coefficient"] == Q // assets and Q % assets == 0,
            "Exact binary native basket coefficient",
        )
        # Fresh checks cover all actual stock sites/clamp comparisons; source role binding
        # has already matched each comparison/select and every strict date predicate.
        clamp_rows = []
        for witness in roles["prefix_witnesses"]:
            budget(started)
            raw_range = next(
                row["actual_raw_log_bounds"][witness["asset"]]
                for row in prefixes["cases"][case]["prefixes"]
                if row["date"] == witness["date"]
            )
            signed_range(tuple(raw_range))
            signed_range(
                (
                    min(raw_range[0], stock["lower_clamp_raw"]),
                    max(raw_range[1], stock["lower_clamp_raw"]),
                )
            )
            signed_range((stock["lower_clamp_raw"], stock["upper_clamp_raw"]))
            clamp_rows.append(
                dict(
                    stock=witness["stock"],
                    raw_log=witness["raw_log"],
                    raw_log_bounds=raw_range,
                    eager_lt_flag_bounds=[0, 1],
                    decoded_lower_upper_raw=[stock["lower_clamp_raw"], stock["upper_clamp_raw"]],
                )
            )
        rows = []
        for prefix in prefixes["cases"][case]["prefixes"]:
            budget(started)
            j, lam = prefix["elapsed_dates"], exact(prefix["lambda_upper"])
            a = lower(iv(mp, 1 - alpha) * mp.iv.exp(iv(mp, -lam)))
            b = upper(iv(mp, 1 + alpha) * mp.iv.exp(iv(mp, lam)))
            ideal_upper_clip_lower = lower(mp.iv.exp(iv(mp, U - lam)))
            guard(
                0 < a <= 1 <= b and ideal_upper_clip_lower > assets * 140,
                "Both strict survivor paths exclude upper-clamped stocks",
            )
            lower_band, upper_band = Fraction(140 - ell, b), Fraction(140 + beta + EPSILON, a)
            guard(0 < lower_band <= upper_band, "Positive ordered CLOSED ideal basket band")
            # Variance is for the independent continuous common driver only.
            variance = Fraction(9 * j, 250 * dates)
            gaussian_upper = min(
                Fraction(1),
                upper(
                    mp.iv.log(iv(mp, upper_band / lower_band))
                    / mp.iv.sqrt(2 * mp.iv.pi * iv(mp, variance))
                ),
            )
            relevant_pairs = ((assets + 1) * j + 1) // 2
            require(
                0 < relevant_pairs <= pairs, "Relevant WHOLE source pair count with unused partner"
            )
            allowance = relevant_pairs * (4 * DS + Fraction(2, N))
            hybrid_upper = min(Fraction(1), gaussian_upper + allowance)
            guard(
                0 <= gaussian_upper <= 1 and 0 <= hybrid_upper <= 1,
                "Closed-band probability upper bounds",
            )
            rows.append(
                dict(
                    date=j - 1,
                    elapsed_dates=j,
                    lambda_upper=encode(lam),
                    a_lower=encode(a),
                    b_upper=encode(b),
                    ell_upper=encode(ell),
                    ideal_upper_clip_stock_lower=encode(ideal_upper_clip_lower),
                    native_upper_clip_stock_raw=stock["actual_native_upper_clamp_stock_raw"],
                    closed_band_lower=encode(lower_band),
                    closed_band_upper=encode(upper_band),
                    exact_continuous_common_variance=encode(variance),
                    gaussian_closed_band_probability_upper=encode(gaussian_upper),
                    relevant_whole_pairs=relevant_pairs,
                    pair_law_allowance=encode(allowance),
                    hybrid_closed_band_probability_upper=encode(hybrid_upper),
                    radial_band_pointwise_TV_upper=4,
                    circular_band_pointwise_TV_upper=4,
                    strict_threshold_TV2_not_substituted=True,
                    unused_future_pair_partner_retained=True,
                )
            )
        switch = min(
            Fraction(1),
            sum((exact(row["hybrid_closed_band_probability_upper"]) for row in rows), Fraction(0)),
        )
        reports[case] = dict(
            alpha_upper=encode(alpha),
            beta_upper=encode(beta),
            decoded_lower_clamp=encode(L),
            decoded_upper_clamp=encode(U),
            ell_upper=encode(ell),
            dates=rows,
            hybrid_any_switch_probability_upper=encode(switch),
            actual_eager_clamp_inventory=clamp_rows,
            eager_financial_tail_safety=eager_financial_tail_safety(
                graphs[case], roles, supports[case], started
            ),
            two_direction_upper_clip_knockout_guards_passed=True,
            all_strict_comparison_and_closed_endpoint_ties_retained=True,
            no_survival_clipping_or_good_radius_conditioning_in_Gaussian_bound=True,
        )
    return dict(
        schema="original-BM-closed-barrier-band-envelopes-v1",
        interval_digits=90,
        pinned_squared_radius_KS_upper=encode(DS),
        pair_transport_order="CURRENT_RADIUS_THEN_CURRENT_ANGLE",
        actual_point_value_BV_convention=True,
        cases=reports,
    )


def smooth_payoff_bounds(mp, binding, supports, bands, started):
    reports = {}
    true_discount = mp.iv.exp(iv(mp, Fraction(-3, 100)))
    for case, (assets, dates, _) in CASES.items():
        budget(started)
        roles, support = binding["cases"][case]["financial_roles"], supports[case]
        require(
            roles["native_discount_literal"] == support["actual_discount_literal"],
            "Actual original native discount literal",
        )
        d_hat = Fraction(support["actual_discount_literal"], Q)
        c_average = Fraction(support["actual_average_literal"], Q)
        guard(0 < d_hat <= 1 and c_average > 0, "Positive native discount and all-stock average")
        average_literal_error = abs(c_average - Fraction(1, assets * dates))
        discount_error = absolute_error(support["actual_discount_literal"], true_discount)
        beta, ell = (
            exact(bands["cases"][case]["beta_upper"]),
            exact(bands["cases"][case]["ell_upper"]),
        )
        date_errors = []
        for row in bands["cases"][case]["dates"]:
            budget(started)
            a, b = exact(row["a_lower"]), exact(row["b_upper"])
            error = 140 * max(1 - a, b - 1) + max(beta, ell)
            guard(error >= 0, "Both-path strict-survivor unrounded mean-stock envelope")
            date_errors.append(
                dict(date=row["date"], unrounded_mean_stock_error_upper=encode(error))
            )
        average_error = (
            sum(
                (exact(row["unrounded_mean_stock_error_upper"]) for row in date_errors), Fraction(0)
            )
            / dates
            + assets * dates * 140 * average_literal_error
            + EPSILON
        )
        zeta = d_hat * average_error + 40 * discount_error + EPSILON
        require(
            support["strict_integer_survival_sum_proved"] is True,
            "floor(S_raw/na)<H*Q proves the unrounded surviving stock mean<H",
        )
        guard(
            0 <= exact(support["native_cap_upper"]) < 40,
            "Original source-identical native support below40",
        )
        reports[case] = dict(
            date_mean_stock_errors=date_errors,
            actual_average_literal=support["actual_average_literal"],
            exact_average_literal_error=encode(average_literal_error),
            actual_discount_literal=support["actual_discount_literal"],
            exact_discount_enclosure=[encode(v) for v in interval(true_discount)],
            discount_literal_error_upper=encode(discount_error),
            average_error_upper=encode(average_error),
            smooth_discounted_payoff_error_upper=encode(zeta),
            fixed_both_payoffs_safe_cap=encode(40),
            native_cap_upper=support["native_cap_upper"],
            averaging_ALL_native_stock_words=True,
            rounded_baskets_not_averaged=True,
            basket_floor_charged_only_in_barrier_band=True,
            average_floor_upper=encode(EPSILON),
            final_discount_floor_upper=encode(EPSILON),
            strict_survival_unrounded_mean_proof=True,
            positive_part_is_1_Lipschitz_and_same_exact_strike=True,
        )
    return dict(schema="original-BM-smooth-payoff-envelopes-v1", interval_digits=90, cases=reports)


def bridge_method_obligations():
    """Reviewer-checkable paper steps; not a numerical substitute or native BV claim."""
    return dict(
        actual_point_value_BV_convention=(
            "Both left-limit to actual value and actual value to right-limit jumps count, "
            "including "
            "singleton contacts and the periodic seam. Open/closed threshold probabilities "
            "use F(t-) "
            "and F(t); the continuous law has the same limits, but the hybrid may have atoms."
        ),
        radial_closed_band=(
            "For fixed other pairs and ideal angle, each exact unclipped stock is "
            "c*exp(beta*r), c>0. "
            "The basket is convex on r>=0. Its closed sublevel is an interval; removing its "
            "open lower "
            "sublevel leaves at most two closed intervals, possibly singleton contacts. Each costs "
            "at most two pointwise jumps, hence TV<=4. The map s->sqrt(s) preserves this variation."
        ),
        angular_closed_band=(
            "The pinned original positive-role/kappa<sqrt2 polar theorem applies after "
            "replacing the "
            "CURRENT pair radius by bounded native Rhat. The exact ideal-angle basket has "
            "one max/min "
            "or is constant. A closed finite band is at most two arcs, including extrema "
            "ties, hence "
            "circular pointwise TV<=4. No claim applies to native rounded cosine or clipped "
            "finance."
        ),
        whole_pair_transport=(
            "Replace each CURRENT pair radius first and its angle second. Other independent pairs "
            "only modify positive weights. A band costs 4*DS+4/(2N). All source drivers "
            "through date j "
            "occupy ceil((na+1)*j/2) WHOLE blocks; an unused future partner remains in its "
            "joint law."
        ),
        continuous_anti_concentration=(
            "Only in the continuous reference, a stock at date j factors its shared common "
            "Gaussian: "
            "B_j=exp(s_j*Z)*W, W>0 independent of Z, s_j^2=sigma^2*rho*j/nt. Conditional "
            "closed-band "
            "log length is log(Uj/Lj)/s_j; standard normal density<=1/sqrt(2pi). Integrate W "
            "without "
            "conditioning on survival, clipping or a radius event. Add the separate "
            "whole-pair band "
            "allowance, then the union bound for switches."
        ),
        clipping_and_band=(
            "Native stock>=0, exact binary basket1/na, and BOTH native S_N(U)>=na*H and ideal "
            "exp(U-lambda)>na*H exclude upper-clip events from either survivor. Lower clip leaks "
            "at most ell. Summing the stock envelope and paying the basket floor gives "
            "a_j*B_H-beta-eps<=B_N<=b_j*B_H+ell. Opposite strict barrier decisions force the "
            "CLOSED "
            "band [(H-ell)/b_j,(H+beta+eps)/a_j], retaining native equality and all endpoint ties."
        ),
        survival_and_smooth=(
            "For integer date stock sum S_raw, floor(S_raw/na)<H*Q implies S_raw<na*H*Q. On "
            "both-path "
            "strict survival, each unrounded mean<H. Inverting a_j and b_j envelope gives "
            "mean-stock "
            "error<=H*max(1-a_j,b_j-1)+max(beta,ell). The source averages ALL stock words: "
            "divide the "
            "sum of date errors by nt, pay actual average-literal error against "
            "total<na*nt*H and its "
            "one floor. Positive part with exact same strike is 1-Lipschitz; pay native discount "
            "literal and final floor. Both nonnegative payoffs lie in [0,40], so a switch costs40."
        ),
        pay_once=(
            "Pinned primary polar H_price already pays original native internal-radius log/root "
            "and ideal midpoint-angle law. Remaining coordinate error=B*Ecos+eps pays cosine and "
            "final product only. Bridge=zeta+40*P_H(any switch), Total=H_price+Bridge. Band "
            "variation "
            "is itemized separately; do not add an old Holder radius term, old grid "
            "coupling, extra "
            "generic dimension/N cutoff or a second augmented-envelope presentation."
        ),
        native_convexity_or_unimodality_claimed=False,
        AS241_theorem_imported=False,
    )


def complete_financial_bounds(polar, bands, smooth, started):
    reports = {}
    for case, (_, dates, pairs) in CASES.items():
        budget(started)
        source = polar["source"]["ideal_hybrid_bounds.json"]["cases"][case]
        H_price = exact(source["hybrid_dollars_upper"])
        C_lower, C_upper = [exact(v) for v in source["exact_cap_enclosure"]]
        DS = exact(polar["source"]["log_radius_envelope.json"]["squared_radius_KS_upper"])
        guard(
            0 <= C_lower <= C_upper <= 40 and H_price >= 0,
            "Actual independently approved primary ideal payoff cap and law bound",
        )
        require(
            H_price == pairs * (4 * C_upper * DS + C_upper * Fraction(dates + 1, N)),
            "Pinned primary whole-pair hybrid price identity, no relabeling or recalculation",
        )
        zeta = exact(smooth["cases"][case]["smooth_discounted_payoff_error_upper"])
        switch = exact(bands["cases"][case]["hybrid_any_switch_probability_upper"])
        bridge = zeta + 40 * switch
        total = H_price + bridge
        reports[case] = dict(
            pinned_primary_hybrid_price_upper=encode(H_price),
            pinned_primary_exact_cap_enclosure=source["exact_cap_enclosure"],
            pinned_primary_squared_radius_KS_upper=encode(DS),
            smooth_discounted_payoff_error_upper=encode(zeta),
            hybrid_any_switch_probability_upper=encode(switch),
            fixed_safe_switch_cap=encode(40),
            native_bridge_dollars_upper=encode(bridge),
            continuous_to_native_dollars_upper=encode(total),
            unchanged_financial_residual=encode(Fraction(11, 2000)),
            financial_residual_fit=total <= Fraction(11, 2000),
            native_financial_bias_certificate_valid=True,
            actual_joint_pairs=pairs,
            independent_audit_still_required=True,
        )
    return dict(
        schema="original-BM-complete-native-financial-bounds-v1",
        cases=reports,
        all_financial_residuals_fit=all(row["financial_residual_fit"] for row in reports.values()),
        native_financial_bias_certificate_valid=True,
        full_G2=False,
        adoption=False,
        cost_transfer=False,
        estimator_99percent_delivery_certified=False,
        matched_classical_or_quantum_advantage_claimed=False,
        new_fixture_credit=0,
    )


def prior_bridge_provenance(implementation, frozen, external, started):
    """Preserve the complete real failed packet; no partial arithmetic credit."""
    same(implementation["prior_bridge_author_SHA256"], PRIOR_BRIDGE_AUTHORS, "Old quartet pins")
    require(
        implementation["prior_bridge_failed_receipt_manifest_SHA256"] == PRIOR_BRIDGE_FAILURE_SHA
        and implementation["prior_bridge_root_review_manifest_SHA256"] == PRIOR_BRIDGE_REVIEW_SHA,
        "Exact actual failed-packet and review pins",
    )
    require(
        not (PROGRAM / "A02_BM_native_financial_bridge_audit_run001").exists(),
        "Original independent audit was never admitted",
    )
    for name, expected in PRIOR_BRIDGE_AUTHORS.items():
        budget(started)
        bind(frozen, external, RESEARCH / name, expected, started)
    for receipt, pin, counts, local_owned in (
        (PRIOR_BRIDGE, PRIOR_BRIDGE_FAILURE_SHA, [20, 346, 2842], True),
        (PRIOR_BRIDGE_REVIEW, PRIOR_BRIDGE_REVIEW_SHA, [1, 11, 0], False),
    ):
        budget(started)
        require(
            receipt.is_dir() and not (receipt / "FAILED_UNSEALED.json").exists(),
            "Both prior packets are real sealed immutable evidence",
        )
        path = bind(frozen, external, receipt / "manifest.json", pin, started)
        manifest = read(path, started)
        require(manifest["manifest_self_hash_excluded"] is True, "Exact prior self-hash policy")
        mappings = [
            manifest["files"],
            manifest["frozen_inputs"],
            manifest.get("external_runtime_inputs", {}),
        ]
        require(
            all(type(mapping) is dict for mapping in mappings)
            and [len(mapping) for mapping in mappings] == counts,
            "Every prior owned, frozen and external reference retained",
        )
        owned = set()
        for field, mapping in zip(
            ("files", "frozen_inputs", "external_runtime_inputs"), mappings, strict=True
        ):
            for key, expected in mapping.items():
                budget(started)
                outside = field == "external_runtime_inputs"
                require(
                    type(key) is str and Path(key).is_absolute() is outside,
                    "Prior ROOT/receipt versus scoped external key convention",
                )
                parent = receipt if field == "files" and local_owned else ROOT
                actual = bind(
                    frozen, external, Path(key) if outside else parent / key, expected, started
                )
                require(
                    (str(actual) if outside else actual.relative_to(parent).as_posix()) == key,
                    "Strict canonical prior map key, no alias or expected-SHA override",
                )
                if field == "files":
                    require(actual.is_relative_to(receipt), "Prior owned receipt confinement")
                    owned.add(actual.relative_to(receipt).as_posix())
        found, total = set(), 0
        for candidate in receipt.rglob("*"):
            budget(started)
            if candidate.is_file():
                actual = resolved(candidate, started)
                require(actual.is_relative_to(receipt), "Prior actual owned directory confinement")
                key = actual.relative_to(receipt).as_posix()
                require(key not in found, "No aliased prior owned byte")
                found.add(key)
                total += actual.stat().st_size
                require(len(found) <= 65 and total <= 128 * 1024**2, "Finite prior owned packet")
        require(found == owned | {"manifest.json"}, "Complete exact prior owned inventory")
        if local_owned:
            require(
                manifest["schema"] == "box-muller-native-financial-bridge-terminal-manifest-v1"
                and manifest["completed"] is False
                and manifest["passed"] is False
                and manifest["budget_censored"] is False
                and manifest["original_expected_hashes_waived"] is False,
                "Actual prior support-signature failure, not a valid residual rejection",
            )
            same(
                manifest["historical_global_LIVE_integrity"],
                dict(
                    passed=False,
                    mismatch_references=36,
                    distinct_paths=9,
                    expected_hashes_waived=False,
                ),
                "Prior global LIVE mismatches remain unchanged",
            )
            outcome = read(receipt / "completion_outcome.json", started)
            require(
                outcome["completed"] is False
                and outcome["passed"] is False
                and outcome["failed"] is True
                and outcome["budget_censored"] is False
                and outcome["new_test_credit"] == 0
                and outcome["full_G2"] is outcome["adoption"] is outcome["cost_transfer"] is False,
                "Prior failure grants no credit or adoption",
            )
            failure = read(receipt / "failure.json", started)
            require(
                failure["failed"] is True
                and failure["all_fixture_credit"] == 0
                and failure["error_type"] == "ValueError"
                and failure["error"]
                == "Every fresh original stock matches independent actual-source support",
                "Exact retained prior comparator failure",
            )
            for name, expected in PRIOR_BRIDGE_AUTHORS.items():
                budget(started)
                require(
                    sha(receipt / "executed_code" / name, started) == expected,
                    "All executed original author copies preserved exactly",
                )
            protocol = read(receipt / "protocol.json", started)
            for field in ("frozen_inputs", "external_runtime_inputs"):
                for key, expected in protocol[field].items():
                    budget(started)
                    require(manifest[field].get(key) == expected, "No prior prepared byte dropped")
        else:
            review = read(receipt / "summary.json", started)
            require(
                review["root_and_independent_mathematical_source_protocol_review_passed"] is True
                and review["authors_frozen"] is True
                and review["scientific_code_or_proof_or_source_walk_executed_by_static_review"]
                is False
                and review["new_fixture_credit"] == 0,
                "Original review is static evidence only",
            )
    return dict(
        failed_receipt=PRIOR_BRIDGE.relative_to(ROOT).as_posix(),
        failed_manifest_sha256=PRIOR_BRIDGE_FAILURE_SHA,
        failed_owned_frozen_external_counts=[20, 346, 2842],
        root_review_receipt=PRIOR_BRIDGE_REVIEW.relative_to(ROOT).as_posix(),
        root_review_manifest_sha256=PRIOR_BRIDGE_REVIEW_SHA,
        root_review_owned_frozen_counts=[1, 11],
        original_author_sha256=PRIOR_BRIDGE_AUTHORS,
        zero_new_fixture_credit=True,
        numerical_bound_credit=False,
        original_source_receipt_immutable=True,
        original_independent_audit_receipt_absent=True,
    )


def implementation_policy(started):
    data = read(IMPLEMENTATION, started)
    require(
        data["schema"] == "box-muller-native-financial-bridge-implementation-preflight-v2",
        "Implementation preflight schema",
    )
    same(
        data["implementation_receipt_route_override"],
        dict(
            source=OUTPUT.relative_to(ROOT).as_posix(),
            audit=(PROGRAM / "A02_BM_native_financial_bridge_audit_run002")
            .relative_to(ROOT)
            .as_posix(),
        ),
        "Only this new implementation authorizes fresh versioned receipt routes",
    )
    require(
        data["original_method_future_labels_remain_run001"] is True
        and data["stock_support_signature_exact_E03_add_mul_child_canonicalization"] is True
        and data["actual_native_argument_order_and_mathematical_kernels_unchanged"] is True,
        "Narrow structural signature correction, original method remains immutable",
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
        and data["cosine_512_coefficient_envelope_in_scope"] is True,
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
    same(
        data["required_polar_receipts"],
        [POLAR_SOURCE.relative_to(ROOT).as_posix(), POLAR_AUDIT.relative_to(ROOT).as_posix()],
        "Actual polar v3 release routes",
    )
    require(
        data["runtime_scope"]["base_Lib_site_packages"] == "EXCLUDED_UNREACHABLE_AND_REJECTED"
        and data["runtime_scope"]["exact_sys_prefix_search_path_admitted"] is True
        and data["runtime_scope"]["actual_venv_adjacent_bytes_and_directory_membership_frozen"]
        is True,
        "Accepted actual reachable runtime policy and source/cache capture",
    )
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
        schema="box-muller-native-financial-bridge-terminal-manifest-v1",
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
        bridge_previous = prior_bridge_provenance(implementation, frozen, external, started)
        plan, origins = selected_sources(frozen, external, started)
        previous = operational_provenance(plan, frozen, external, started)
        root_origins = root_provenance(implementation, frozen, external, started)
        polar = polar_packets(implementation, frozen, external, started)
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
        save(output / "operational_provenance.json", previous, started)
        save(output / "prior_bridge_provenance.json", bridge_previous, started)
        save(output / "polar_prerequisites.json", polar, started)
        save(output / "interpreter.json", interpreter, started)
        verification_count = final_verify(frozen, external, started)
        budget(started, admission=True)
        protocol = dict(
            schema="box-muller-native-financial-bridge-protocol-v1",
            output=output.relative_to(ROOT).as_posix(),
            prepared_UTC=datetime.now(timezone.utc).isoformat(),
            producer_module="research.limitation_program_20261001.experiment_box_muller_native_financial_bridge_v2",
            operational_bridge_version=2,
            prior_bridge_author_SHA256=PRIOR_BRIDGE_AUTHORS,
            prior_bridge_failed_receipt_manifest_SHA256=PRIOR_BRIDGE_FAILURE_SHA,
            prior_bridge_root_review_manifest_SHA256=PRIOR_BRIDGE_REVIEW_SHA,
            previous_failed_bridge_credit=0,
            frozen_inputs=frozen,
            external_runtime_inputs=external,
            immutable_author_sha256=implementation["author_sha256"],
            method_document_SHA256=implementation["method_document_SHA256"],
            required_polar_manifest_SHA256=implementation["required_polar_manifest_SHA256"],
            required_polar_author_SHA256=implementation["required_polar_author_SHA256"],
            selected_source_SHA256=plan[
                "original_selected_source_pins_from_existing_manifest_metadata"
            ],
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
            cosine_512_envelope_in_scope=True,
            cosine_512_envelope_computed_in_prepare=False,
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
    frozen, external, admitted = {}, {}, False
    try:
        setup(started)
        require(output == OUTPUT and output.is_dir(), "Exact prepared native bridge output")
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
            "No reused run, partial terminal result or failed preparation",
        )
        admitted = True
        protocol = read(output / "protocol.json", started)
        prepared = read(output / "PREPARED_RECEIPT.json", started)
        require(
            prepared["prepared"] is True
            and prepared["terminal"] is False
            and sha(output / "protocol.json", started) == prepared["protocol_sha256"],
            "Actual immutable preparation protocol",
        )
        require(
            protocol["schema"] == "box-muller-native-financial-bridge-protocol-v1",
            "Prepared native bridge schema",
        )
        same(
            [
                protocol[field]
                for field in (
                    "process_CPU_seconds",
                    "admission_process_CPU_seconds",
                    "wall_seconds",
                )
            ],
            [180, 150, 600],
            "Same all-inclusive fixed run clocks",
        )
        require(
            protocol["primary_interval_decimal_digits"] == 90
            and protocol["independent_interval_decimal_digits"] == 130
            and protocol["numerical_threads"] == 1
            and protocol["fixture_credit"] == 0
            and protocol["startup_B_required"] is True
            and protocol["pure_Python_mpmath_backend_required"] is True
            and protocol["cosine_512_envelope_in_scope"] is True
            and protocol["cosine_512_envelope_computed_in_prepare"] is False,
            "Prepared finite original native financial method",
        )
        for field, external_map in (("frozen_inputs", False), ("external_runtime_inputs", True)):
            require(type(protocol[field]) is dict, "Complete recognized preparation map")
            for key, expected in protocol[field].items():
                budget(started)
                require(
                    type(key) is str and Path(key).is_absolute() is external_map,
                    "Preparation ROOT versus separately scoped external key convention",
                )
                path = Path(key) if external_map else ROOT / key
                actual = bind(frozen, external, path, expected, started)
                require(
                    (str(actual) if external_map else actual.relative_to(ROOT).as_posix()) == key,
                    "Strict canonical prepared map keys",
                )
        for name in (
            "protocol.json",
            "PREPARED_RECEIPT.json",
            "selected_source_origins.json",
            "native_root_provenance.json",
            "operational_provenance.json",
            "prior_bridge_provenance.json",
            "polar_prerequisites.json",
            "interpreter.json",
        ):
            path = output / name
            bind(frozen, external, path, sha(path, started), started)
        implementation = implementation_policy(started)
        bridge_previous = prior_bridge_provenance(implementation, frozen, external, started)
        require(
            protocol["operational_bridge_version"] == 2
            and protocol["previous_failed_bridge_credit"] == 0
            and protocol["prior_bridge_failed_receipt_manifest_SHA256"] == PRIOR_BRIDGE_FAILURE_SHA
            and protocol["prior_bridge_root_review_manifest_SHA256"] == PRIOR_BRIDGE_REVIEW_SHA,
            "Actual prepared structural correction and zero-credit failed prerequisites",
        )
        same(
            protocol["prior_bridge_author_SHA256"],
            PRIOR_BRIDGE_AUTHORS,
            "All original authors retained",
        )
        same(
            bridge_previous,
            read(output / "prior_bridge_provenance.json", started),
            "Complete original failed packet and review remain strict immutable evidence",
        )
        same(
            implementation["author_sha256"],
            protocol["immutable_author_sha256"],
            "Exact prepared author pins",
        )
        same(
            implementation["method_document_SHA256"],
            protocol["method_document_SHA256"],
            "Exact held method pins",
        )
        for field in (
            "required_polar_manifest_SHA256",
            "required_polar_author_SHA256",
            "additional_native_root_provenance_SHA256",
            "original_root_owner_manifest_SHA256",
        ):
            same(
                implementation[field],
                protocol[field],
                "Prepared strict prerequisite release: " + field,
            )
        plan, origins = selected_sources(frozen, external, started)
        same(
            plan["original_selected_source_pins_from_existing_manifest_metadata"],
            protocol["selected_source_SHA256"],
            "Exactly fixed25 original source pins",
        )
        same(
            origins,
            read(output / "selected_source_origins.json", started),
            "All20 original selected nonmanifest memberships",
        )
        previous = operational_provenance(plan, frozen, external, started)
        same(
            previous,
            read(output / "operational_provenance.json", started),
            "Complete unchanged operational history at zero credit",
        )
        roots = root_provenance(implementation, frozen, external, started)
        same(
            roots,
            read(output / "native_root_provenance.json", started),
            "Actual unsigned46 root realization provenance",
        )
        polar = polar_packets(implementation, frozen, external, started)
        same(
            polar,
            read(output / "polar_prerequisites.json", started),
            "Actual independently passed polar source/audit packets unchanged",
        )
        interpreter = read(output / "interpreter.json", started)
        same(interpreter, protocol["interpreter"], "Prepared exact runtime record")
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
        require("mpmath" not in sys.modules, "Deferred pure-Python interval import")
        import mpmath as mp

        require(
            mp.__version__ == "1.3.0" and sys.modules["mpmath.libmp.backend"].BACKEND == "python",
            "Actual fixed pure-Python mpmath backend, no optional backend",
        )
        mp.iv.dps, mp.mp.dps = 90, 90
        verify_loaded(frozen, external, started)
        budget(started, admission=True)
        binding, _, _, graphs = bind_actual_sources(started)
        same(
            binding,
            polar["source"]["source_binding.json"],
            "Fresh complete original source/role/root binding equals the actual polar premise",
        )
        save(output / "native_source_binding.json", binding, started)
        supports = support_evidence(binding, graphs, started)
        save(output / "original_support_evidence.json", supports, started)
        B = exact(polar["source"]["log_radius_envelope.json"]["internal_radius_upper"])
        DS = exact(polar["source"]["log_radius_envelope.json"]["squared_radius_KS_upper"])
        budget(started, admission=True)
        cosine = cosine_envelope(mp, graphs, B, started)
        save(output / "cosine_envelope.json", cosine, started)
        budget(started, admission=True)
        prefixes = raw_log_prefix_envelopes(mp, graphs, binding, cosine, B, started)
        save(output / "raw_log_prefix_envelopes.json", prefixes, started)
        budget(started, admission=True)
        stocks = stock_exponential_envelopes(mp, graphs, binding, supports, started)
        save(output / "stock_exponential_envelopes.json", stocks, started)
        budget(started, admission=True)
        emitted = whole_emitted_finance_safety(graphs, binding, cosine, stocks, started)
        save(output / "all_emitted_financial_safety.json", emitted, started)
        budget(started, admission=True)
        bands = closed_barrier_bands(
            mp, graphs, binding, prefixes, stocks, supports, polar, DS, started
        )
        save(output / "closed_barrier_bands.json", bands, started)
        budget(started, admission=True)
        smooth = smooth_payoff_bounds(mp, binding, supports, bands, started)
        save(output / "smooth_payoff_bounds.json", smooth, started)
        obligations = bridge_method_obligations()
        save(output / "method_obligations.json", obligations, started)
        complete = complete_financial_bounds(polar, bands, smooth, started)
        save(output / "complete_financial_bounds.json", complete, started)
        runtime_policy(interpreter, started)
        save(
            output / "loaded_module_origins.json", verify_loaded(frozen, external, started), started
        )
        fit = complete["all_financial_residuals_fit"]
        summary = dict(
            schema="original-BM-native-financial-bridge-summary-v1",
            completed=True,
            passed=fit,
            rejection=not fit,
            budget_censored=False,
            status="native_financial_bias_component_passed"
            if fit
            else "certificate_method_rejected_residual",
            native_financial_bias_certificate_valid=True,
            financial_residual_fit=fit,
            independent_audit_still_required=True,
            unchanged_financial_residual=encode(Fraction(11, 2000)),
            case_dollars_upper={
                case: row["continuous_to_native_dollars_upper"]
                for case, row in complete["cases"].items()
            },
            actual_joint_pair_counts={case: pairs for case, (_, _, pairs) in CASES.items()},
            actual_stock_sites=464,
            fresh_cosine_coefficients_checked=512,
            retained_stock_exponent_classes=60,
            all_actual_native_emitted_dead_paths_product144_and_stored72_safe=True,
            exact_original_contract_and_strict_barrier_ties_preserved=True,
            no_old_radius_Holder_log_root_grid_or_cutoff_term_added_again=True,
            new_test_credit=0,
            all_fixture_credit=0,
            new_gate_replays=0,
            basis_or_circuit_or_price_estimator_replays=0,
            source_expected_hashes_waived=False,
            full_G2=False,
            adoption=False,
            cost_transfer=False,
            estimator_99percent_delivery_certified=False,
            matched_classical_or_quantum_advantage_claimed=False,
            residual_spent_or_reallocated=False,
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
                passed=fit,
                rejection=not fit,
                budget_censored=False,
                phase="run",
                summary_file="summary.json",
                status=summary["status"],
                native_financial_bias_certificate_valid=True,
                financial_residual_fit=fit,
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
