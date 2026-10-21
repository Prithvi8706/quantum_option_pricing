"""Independent complete native two-draw resource and packed-state audit.

No audited builder, counter, evaluator or research helper is imported. Numerical
imports occur only in run(), after the independent protocol has been frozen.
The fixed producer lanes are reexecuted independently, with zero fixture credit.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from math import isqrt
import os
from pathlib import Path
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
RESEARCH = ROOT / "research/limitation_program_20261001"
SOURCE = PROGRAM / "A02_two_draw_loader_resource_run002"
OUTPUT = PROGRAM / "A02_two_draw_loader_resource_audit_run002"
PREFLIGHT = RESEARCH / "two_draw_loader_implementation_preflight_v2.json"
PLAN = RESEARCH / "two_draw_loader_resource_preflight.json"
SCALAR = PROGRAM / "A02_quantile_scalar_run001"
BM = PROGRAM / "A10_coefficient_run001/B4x12/min-depth"
CPU, ADMISSION, WALL = 180, 150, 600
W, F, SCALE = 72, 40, 1 << 40
MASK = (1 << 72) - 1
CAP, CHUNK, LANEMASK = 45000, 65536, 65535
PACKAGES = {"numpy": "2.0.2", "numba": "0.60.0", "llvmlite": "0.43.0"}
TOOL_DEPENDENCIES = (
    "pytest",
    "pluggy",
    "packaging",
    "iniconfig",
    "colorama",
    "pygments",
    "scipy",
    "numba-cuda",
)
TOOL_PREFIXES = {
    "numpy",
    "numba",
    "llvmlite",
    "pytest",
    "_pytest",
    "pluggy",
    "packaging",
    "iniconfig",
    "colorama",
    "pygments",
    "scipy",
    "numba_cuda",
}
FAILED_W10_SHA = "1c47fee27c640587c2a52d988112c4411a9928eb7fc4df301ddae3a2ae0d97d5"
DRIFT_MANIFEST_SHA = "7c33669d38f25c61f375366fbddaeccd6507cfce276eadf88aa7784f340d3123"
ADMISSION_FAILURE_SHA = "b2911a9d8d1c961f75f6f8a2418ed8d0d04e8011ea869b1c5006279f03cc4bdd"
ROOT_REVIEW_SHA = "eaef4d44c1f8241241a11f0e7406232d8cdd564d586fd7d71bdba27f6140749c"
ORIGINAL_AUTHORS = {
    "two_draw_loader_source.py": "64358f2606632a4c6202e4a03f895f9232d70bdd5a1a0b6e59be70128f7e5636",
    "experiment_two_draw_loader_resource.py": (
        "f459950fd9cc3d94df9cc7dec0df5c778625cf29a2777f4b18bb25294af6613a"
    ),
    "test_two_draw_loader_source.py": (
        "5446698f313c6c7f34d18ef552dfb3628294f546de9fc4b89289bc302acf4a34"
    ),
    "audit_two_draw_loader_resource.py": (
        "2b31150c720ecf8e3d10a74d572755ab5bf1ecd4718e0b8d92d79c1d17a1e278"
    ),
    "TWO_DRAW_LOADER_IMPLEMENTATION_PREFLIGHT.md": (
        "2b4ffc1d93bffc0d8b2e61c994c5e5bb9432c72ba1b5719c547ce4d0ed6ed476"
    ),
    "two_draw_loader_implementation_preflight.json": (
        "e5c9bb92a5a444b288ce60fc3bb270b4f8d37acb9d57f36bab49a32cbe4d3f6a"
    ),
    "TWO_DRAW_LOADER_RESOURCE_PREFLIGHT.md": (
        "f6e0e1036a81749b5fbbc922fa30ea413e4e09b23bdc7a3e169965a00714ab77"
    ),
    "two_draw_loader_resource_preflight.json": (
        "fc27fe0eef27a4a0e6cb0de65d6c33c3b45cafd66401ea3fb112269f93e28558"
    ),
}
_PATHS = {}
_HASHES = {}
_OBSERVED = {}
LABELS = ("AS241_two_actual_scalar_invocations", "BoxMuller_one_actual_shared_pair")
PAIRS = (
    (0, 0),
    (0, 4294967295),
    (4294967295, 0),
    (4294967295, 4294967295),
    (322122546, 322122547),
    (3972844749, 3972844748),
    (2147483647, 2147483648),
    (1073741824, 3221225472),
)
FIELDS = ("x", "cx", "ccx", "source_gates", "t_count", "t_depth", "clifford_t_depth")
CCX = (
    ("H", "target"),
    ("CX", "b", "target"),
    ("Tdg", "target"),
    ("CX", "a", "target"),
    ("T", "target"),
    ("CX", "b", "target"),
    ("Tdg", "target"),
    ("CX", "a", "target"),
    ("T", "b"),
    ("T", "target"),
    ("H", "target"),
    ("CX", "a", "b"),
    ("T", "a"),
    ("Tdg", "b"),
    ("CX", "a", "b"),
)


class BudgetCensoredError(RuntimeError):
    """Terminal hard-budget failure; no retry or method change."""


def require(condition, message):
    if not condition:
        raise ValueError(message)


def budget(started, admission=False):
    cpu, wall = time.process_time() - started[0], time.monotonic() - started[1]
    if cpu >= (ADMISSION if admission else CPU) or wall >= WALL:
        raise BudgetCensoredError("Fixed independent paired-loader CPU/wall budget")
    return cpu, wall


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


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


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def same(actual, expected, message):
    require(canonical(actual) == canonical(expected), message)


def resolved(path, fresh=False):
    require(
        not Path(path).drive or Path(path).is_absolute(), "No ambiguous drive-relative audit path"
    )
    lexical = str(Path(path).absolute())
    if not fresh and lexical in _PATHS:
        return _PATHS[lexical]
    value = Path(path).resolve()
    value.relative_to(ROOT)
    require(
        not fresh or lexical not in _PATHS or _PATHS[lexical] == value,
        "Previously confined audit path resolution changed",
    )
    _PATHS[lexical] = value
    _PATHS.setdefault(str(value), value)
    return value


def path_key(path):
    return resolved(path).relative_to(ROOT).as_posix()


def hash_path(path, started, fresh=False):
    budget(started)
    lexical = Path(path).absolute()
    if lexical.is_relative_to(ROOT):
        actual = resolved(lexical, fresh=fresh)
    else:
        actual = lexical.resolve()
        base = Path(getattr(sys, "_base_executable", sys.executable)).resolve()
        require(
            actual == base and not base.is_relative_to(ROOT),
            "Only the explicitly scoped actual base interpreter may be external",
        )
    budget(started)
    return actual


def stat_identity(path):
    status = path.stat()
    return (
        status.st_dev,
        status.st_ino,
        status.st_size,
        status.st_mtime_ns,
        status.st_ctime_ns,
        getattr(status, "st_file_attributes", None),
        getattr(status, "st_reparse_tag", None),
    )


def sha(path, started, fresh=False):
    actual = hash_path(path, started, fresh=fresh)
    return actual_digest(actual, started, fresh=fresh)


def actual_digest(actual, started, fresh=False):
    budget(started)
    key, identity = str(actual), stat_identity(actual)
    if not fresh and key in _HASHES and _HASHES[key][0] == identity:
        budget(started)
        return _HASHES[key][1]
    value = hashlib.sha256()
    budget(started)
    with actual.open("rb") as stream:
        while block := stream.read(1 << 20):
            value.update(block)
            budget(started)
    require(stat_identity(actual) == identity, "Actual file changed while hashing")
    budget(started)
    digest = value.hexdigest()
    require(
        key not in _OBSERVED or _OBSERVED[key] == digest, "Previously observed actual bytes changed"
    )
    _OBSERVED.setdefault(key, digest)
    _HASHES[key] = (identity, digest)
    return digest


def bind(frozen, path, expected, started):
    budget(started)
    key = path_key(ROOT / str(path).replace("\\", "/"))
    require(
        type(expected) is str
        and len(expected) == 64
        and all(ch in "0123456789abcdef" for ch in expected),
        "Canonical expected SHA256",
    )
    require(key not in frozen or frozen[key] == expected, "Conflicting expected SHA: " + key)
    frozen[key] = expected
    budget(started)


def verify(frozen, started, fresh=False):
    for key, expected in frozen.items():
        budget(started)
        require(
            sha(resolved(ROOT / key, fresh=fresh), started, fresh=fresh) == expected,
            "Frozen audit input changed: " + key,
        )


def final_verify(frozen, started):
    # Expected and actual hashes stay separate. Fresh verification includes the
    # complete frozen map and every path observed by any hashing interface,
    # including the explicitly scoped external actual base interpreter.
    for lexical, previous in tuple(_PATHS.items()):
        budget(started)
        require(
            resolved(lexical, fresh=True) == previous,
            "Every original lexical alias retains its fresh ROOT-confined resolution",
        )
        budget(started)
    declared = {}
    for key, expected in frozen.items():
        budget(started)
        actual = str(hash_path(ROOT / key, started))
        require(
            actual not in declared or declared[actual] == expected,
            "Final canonical equal-SHA merge",
        )
        declared[actual] = expected
    observed = dict(_OBSERVED)
    for key in sorted(set(declared) | set(observed)):
        budget(started)
        actual = hash_path(key, started, fresh=True)
        digest = actual_digest(actual, started, fresh=True)
        require(
            key not in declared or digest == declared[key],
            "Final complete frozen input verification",
        )
        require(
            key not in observed or digest == observed[key],
            "Final actual-observed byte identity verification",
        )


def verify_runtime(record, frozen, started):
    launcher = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
    require(
        path_key(sys.executable) == path_key(launcher) == record["launcher_workspace_relative"]
        and sha(launcher, started) == record["launcher_sha256"] == frozen[path_key(launcher)],
        "Actual invoked pinned independent scanner interpreter bytes",
    )
    actual_base = Path(getattr(sys, "_base_executable", sys.executable)).resolve()
    require(
        str(actual_base) == record["base_interpreter"]["absolute_path"]
        and sha(actual_base, started) == record["base_interpreter"]["sha256"],
        "Actual base interpreter bytes, separately scoped if external",
    )
    same(record["scanner_packages"], PACKAGES, "Pinned numerical scanner versions")
    for name, version in PACKAGES.items():
        budget(started)
        require(importlib.metadata.version(name) == version, "Actual numerical package version")
    dependencies = record["installed_tool_dependency_versions"]
    require(
        set(dependencies) == set(TOOL_DEPENDENCIES),
        "Exact frozen scientific and fixture dependencies",
    )
    for name, version in dependencies.items():
        budget(started)
        require(importlib.metadata.version(name) == version, "Actual bound tool dependency version")
    site = resolved(launcher.parent.parent / "Lib/site-packages")
    for name in (*PACKAGES, *TOOL_DEPENDENCIES):
        budget(started)
        distribution = importlib.metadata.distribution(name)
        entries = distribution.files
        require(
            entries is not None and len(entries) > 0,
            "Nonempty actual distribution metadata inventory",
        )
        roots = set()
        for entry in entries:
            budget(started)
            if ".dist-info/" not in str(entry).replace("\\", "/"):
                continue
            actual = resolved(Path(distribution.locate_file(entry)))
            roots.update(
                parent for parent in (actual, *actual.parents) if parent.name.endswith(".dist-info")
            )
        require(
            len(roots) == 1 and next(iter(roots)).parent == site,
            "Exactly one actual metadata directory directly inside pinned site-packages",
        )
        for path in sorted(next(iter(roots)).rglob("*")):
            budget(started)
            if path.is_file():
                require(
                    frozen.get(path_key(path)) == sha(path, started),
                    "Every actual distribution metadata byte was frozen before source work",
                )


def verify_loaded_tools(frozen, started):
    require(
        sys.dont_write_bytecode is True, "Independent lazy imports cannot create unbound bytecode"
    )
    current = sys.modules[__name__]
    for name, module in tuple(sys.modules.items()):
        if name.split(".")[0] not in TOOL_PREFIXES and module is not current:
            continue
        budget(started)
        source, cached = getattr(module, "__file__", None), getattr(module, "__cached__", None)
        if source:
            require(Path(source).is_file(), "Actual imported module source exists")
        for path in (source, cached):
            if path and Path(path).is_file():
                key = path_key(path)
                require(
                    frozen.get(key) == sha(path, started),
                    "Actual imported independent source or existing bytecode origin was frozen: "
                    + key,
                )


def bound(path, frozen):
    key = path_key(path)
    require(key in frozen, "Unfrozen audit input: " + key)
    return ROOT / key


def merge_manifest(directory, frozen, started, expected=None):
    manifest = directory / "manifest.json"
    actual = sha(manifest, started)
    require(expected is None or actual == expected, "Trusted original manifest SHA mismatch")
    data = read(manifest)
    require(
        type(data.get("files")) is dict and type(data.get("frozen_inputs", {})) is dict,
        "Recognized strict ROOT-relative source maps",
    )
    require(
        data.get("manifest_self_hash_excluded") is True,
        "Source manifest excludes only its own hash explicitly",
    )
    for field in ("files", "frozen_inputs"):
        for key, value in data.get(field, {}).items():
            bind(frozen, key, value, started)
    own = {path_key(path) for path in directory.rglob("*") if path.is_file() and path != manifest}
    require(
        {path_key(ROOT / key) for key in data["files"]} == own,
        "Source manifest must bind every owned byte",
    )
    bind(frozen, manifest, actual, started)
    return data


def original_maps(path):
    data = read(path)

    def is_sha(value):
        return (
            type(value) is str
            and len(value) == 64
            and all(ch in "0123456789abcdef" for ch in value)
        )

    if data and all(is_sha(value) for value in data.values()):
        return [(data, path.parent, "flat")]
    require(
        type(data.get("files")) is dict and type(data.get("frozen_inputs", {})) is dict,
        "Exact original recognized file/input map forms",
    )
    if "historical_receipts_unchanged" in data:
        require(data["historical_receipts_unchanged"] is True, "Exact C06 historical marker")
    if "manifest_self_hash_excluded" in data:
        require(
            data["manifest_self_hash_excluded"] is True, "Exact historical manifest self-hash scope"
        )
    allowed = {
        "files",
        "frozen_inputs",
        "manifest_self_hash_excluded",
        "historical_receipts_unchanged",
        "all_inputs_and_bulk_hashes_verified_before_terminal",
        "process_CPU_seconds_before_terminal",
        "wall_seconds_before_terminal",
        "terminal_record",
        "partial_failure_terminal_without_retry",
        "failed_finalizer_fixture_credit",
        "single_immutable_manifest",
        "process_CPU_limit_seconds",
        "wall_limit_seconds",
        "all_input_verification_and_bulk_output_hashing_before_terminal",
        "preterminal_process_CPU_seconds",
        "preterminal_wall_seconds",
    }
    require(set(data) <= allowed, "Unknown historical manifest metadata cannot be waived")
    return [(data["files"], ROOT, "files"), (data.get("frozen_inputs", {}), ROOT, "frozen_inputs")]


def original_owned(path, started):
    owned = {}
    for mapping, base, _ in original_maps(path):
        for name, expected in mapping.items():
            budget(started)
            actual = resolved(base / str(name).replace("\\", "/"))
            if actual.is_relative_to(resolved(path.parent)):
                key = path_key(actual)
                require(
                    key not in owned or owned[key] == expected, "Original owned equal-SHA aliases"
                )
                owned[key] = expected
    return owned


def verify_dependency_origins(frozen, started):
    document = read(bound(SOURCE / "dependency_origins.json", frozen))
    require(
        document["original_expected_hashes_never_overwritten"] is True,
        "No original expected hash waiver",
    )
    owners = (
        "A02_quantile_scalar_run001",
        "A02_quantile_scalar_audit_run001",
        "C06_pair_run001",
        "C06_pair_audit_run001",
        "A10_coefficient_run001",
        "A01_drift_run001",
        "WAVE10_run001",
        "WAVE10_run002",
        "A02_two_draw_loader_admission_failure_run001",
        "A02_two_draw_root_review_run001",
    )
    expected_rows, metadata = Counter(), {}
    for owner in owners:
        manifest = bound(PROGRAM / owner / "manifest.json", frozen)
        owned = original_owned(manifest, started)
        metadata[path_key(manifest)] = (manifest, owned)
        for mapping, base, field in original_maps(manifest):
            for name, expected in mapping.items():
                budget(started)
                original = resolved(base / str(name).replace("\\", "/"))
                if owner == "WAVE10_run002" and not original.is_relative_to(manifest.parent):
                    continue
                expected_rows[(path_key(manifest), field, path_key(original), expected)] += 1
    actual_rows = Counter()
    reconciliation = None
    for row in document["rows"]:
        budget(started)
        require(
            row["legitimate_expected_hash_waived"] is False, "Original expected hashes retained"
        )
        signature = (
            row["owner_manifest"],
            row["source_map"],
            row["original_path"],
            row["expected_sha256"],
        )
        require(signature in expected_rows, "Origin must name a real original manifest reference")
        actual_rows[signature] += 1
        origin = bound(ROOT / row["verified_input_path"], frozen)
        require(
            frozen[path_key(origin)] == row["expected_sha256"],
            "Origin's strict original expected SHA",
        )
        original = ROOT / row["original_path"]
        manifest, owned = metadata[row["owner_manifest"]]
        if manifest.parent.name in (
            "WAVE10_run001",
            "A02_two_draw_loader_admission_failure_run001",
            "A02_two_draw_root_review_run001",
        ):
            require(origin == original, "Failed original W10 maps remain strict active obligations")
        if origin == original:
            require(
                row["route"] == "current original expected bytes",
                "Current origin is scoped exactly",
            )
        elif origin.is_relative_to(manifest.parent) and origin.name == original.name:
            require(
                owned.get(path_key(origin)) == row["expected_sha256"]
                and row["route"] == "same-owner archived snapshot with same basename and exact SHA",
                "Exact original same-owner snapshot membership",
            )
        else:
            if reconciliation is None:
                reconciliation = read(
                    bound(PROGRAM / "A01_drift_run001/reconciliation.json", frozen)
                )
            matches = [
                entry
                for entry in reconciliation["rows"]
                if entry["path"] == row["original_path"]
                and entry["expected_old_sha256"] == row["expected_sha256"]
                and entry["recovered_snapshot_path"] == path_key(origin)
                and entry["recovered_snapshot_sha256"] == row["expected_sha256"]
                and entry["historical_old_bytes_recovered"] is True
                and entry["expected_hash_waived"] is False
            ]
            require(
                len(matches) == 1
                and origin.is_relative_to(PROGRAM / "A01_drift_run001")
                and row["route"] == "explicit A01_drift original-owner reconciliation",
                "Exact recorded archival origin",
            )
            references = [
                entry
                for entry in matches[0]["references"]
                if entry["receipt"] == manifest.parent.name
                and entry["expected_sha256"] == row["expected_sha256"]
                and entry["manifest_sha256"] == frozen[path_key(manifest)]
            ]
            require(len(references) == 1, "Archived original owner/reference manifest must match")
    require(
        actual_rows == expected_rows,
        "Complete original map reference inventory, no dropped or invented rows",
    )
    return dict(
        original_references_verified=sum(actual_rows.values()),
        original_owner_manifests=len(owners),
        legitimate_expected_hashes_waived=False,
        all_recorded_original_routes_independently_verified=True,
    )


def phase_premise(frozen):
    manifest = read(bound(PROGRAM / "A17_quantile_divider_run001/manifest.json", frozen))
    proof_key = path_key(PROGRAM / "A17_quantile_divider_run001/exact_CCX_phase_proof.json")
    macro_key = path_key(RESEARCH / "temporary_and_fulladder.py")
    require(
        manifest["files"].get(proof_key) == frozen[proof_key]
        and manifest["frozen_inputs"].get(macro_key) == frozen[macro_key],
        "Exact proof and macro membership in original complete divider receipt",
    )
    proof = read(bound(PROGRAM / "A17_quantile_divider_run001/exact_CCX_phase_proof.json", frozen))
    expected = [
        dict(input=i, output=i ^ (((i & 1) & ((i >> 1) & 1)) << 2), exact_nonzero_phase=1)
        for i in range(8)
    ]
    same(proof, expected, "Hash-bound prior exact phase-one columns for all native CCX inputs")
    macro = bound(RESEARCH / "temporary_and_fulladder.py", frozen)
    functions = [
        node
        for node in ast.parse(macro.read_text(encoding="utf-8")).body
        if isinstance(node, ast.FunctionDef) and node.name == "ccx_seven_t"
    ]
    require(len(functions) == 1, "One original full exact seven-T macro")
    returns = [node for node in functions[0].body if isinstance(node, ast.Return)]
    require(len(returns) == 1 and isinstance(returns[0].value, ast.List), "Literal exact macro")
    rows = []
    for call in returns[0].value.elts:
        require(
            isinstance(call, ast.Call)
            and isinstance(call.func, ast.Name)
            and call.func.id == "gate"
            and not call.keywords
            and isinstance(call.args[0], ast.Constant)
            and all(isinstance(arg, ast.Name) for arg in call.args[1:]),
            "Exact macro syntax",
        )
        rows.append((call.args[0].value, *(arg.id for arg in call.args[1:])))
    same(rows, CCX, "Chronology and both actual control-wire phase terms")
    return dict(
        exact_macro=[list(row) for row in rows],
        exact_native_phase_one=True,
        proof_columns=8,
        basis_fixtures_are_not_phase_proof=True,
    )


def closure(target, outputs, inputs):
    require((target["width"], target["fraction_bits"]) == (W, F), "Original native72/f40")
    definitions = {}
    for node in target["nodes"]:
        require(
            type(node["args"]) is list
            and type(node["out"]) is list
            and all(type(v) is int and v >= 0 for v in node["args"] + node["out"]),
            "Canonical complete SSA identifiers",
        )
        require(
            node["op"] == "input" or all(arg in definitions for arg in node["args"]),
            "Topologically ordered original source",
        )
        for value in node["out"]:
            require(value not in definitions, "Unique SSA producer")
            definitions[value] = node
    required, work = set(), list(outputs)
    while work:
        value = work.pop()
        if value in required:
            continue
        require(value in definitions, "Original output producer exists")
        node = definitions[value]
        required.update(node["out"])
        work.extend(node["args"])
    selected = [node for node in target["nodes"] if set(node["out"]) & required]
    same(
        sorted(v for node in selected if node["op"] == "input" for v in node["out"]),
        inputs,
        "Exactly the original q32 external inputs",
    )
    return selected, required


def derive_one(label, plan, frozen, started):
    scalar = label == LABELS[0]
    directory = SCALAR / "candidate64" if scalar else BM
    target_path = SCALAR / "scalar_target.json" if scalar else BM / "target.json"
    source = read(bound(directory / "source.json", frozen))
    target = read(bound(target_path, frozen))
    outputs, inputs, total, calls_count = (
        ([170], [0], 171, 162) if scalar else ([94, 125], [0, 1], 126, 102)
    )
    nodes, values = closure(target, outputs, inputs)
    require(
        values == set(range(total)) and len(nodes) == calls_count + len(inputs),
        "Complete original closure, including multi-output table banks",
    )
    require(
        source["format"] == "hierarchical-clean-xor-source-v1"
        and (source["word_width"], source["fraction_bits"]) == (W, F)
        and source["exact_clifford_t"] is True
        and source["arbitrary_rotations"] == 0,
        "Original exact native source ABI",
    )
    if scalar:
        require(source["values"] == total and source["outputs"] == {"Z": 170}, "Scalar ABI")
    calls = source["forward_calls"][:calls_count]
    selected = [node for node in nodes if node["op"] != "input"]
    inventory = plan["AS241_wrapper" if scalar else "BoxMuller_wrapper"]["actual_leaf_inventory"]
    origins = {row["key"]: row for row in inventory}
    require(
        len(origins) == (59 if scalar else 32)
        and set(origins) == {call["leaf"] for call in calls}
        and len(calls) == len(selected) == calls_count,
        "Exact original selected native leaves/calls",
    )
    private = 0
    metadata = {}
    trusted_files = original_owned(
        bound((SCALAR if scalar else PROGRAM / "A10_coefficient_run001") / "manifest.json", frozen),
        started,
    )
    for node, call in zip(selected, calls, strict=True):
        budget(started)
        same(
            (call["args"], call["out"]),
            (node["args"], node["out"]),
            "Original call order/arity/SSA",
        )
        require(
            call["argument_copy_cx"] == 2 * W * len(node["args"]), "Full72 copies per occurrence"
        )
        origin = origins[call["leaf"]]
        entry_path, gate_path = (
            bound(ROOT / origin["metadata"], frozen),
            bound(ROOT / origin["native_gate_file"], frozen),
        )
        require(
            frozen[path_key(entry_path)]
            == origin["metadata_sha256"]
            == trusted_files.get(path_key(entry_path)),
            "Original manifest pins each native metadata byte",
        )
        entry = read(entry_path)
        require(
            entry["key"] == call["leaf"]
            and frozen[path_key(gate_path)]
            == origin["native_gate_sha256_from_archived_metadata"]
            == entry["sha256"]
            == trusted_files.get(path_key(gate_path)),
            "Actual gate hash agrees with trusted original manifest and native metadata",
        )
        same(
            (entry["op"], entry["params"]),
            (node["op"], node["params"]),
            "Actual literal native operation",
        )
        arity, nout = len(node["args"]), len(node["out"])
        same(
            entry["args"],
            [list(range(i * W, (i + 1) * W)) for i in range(arity)],
            "Complete native inputs",
        )
        same(
            entry["outs"],
            [list(range((arity + i) * W, (arity + i + 1) * W)) for i in range(nout)],
            "Complete native outputs",
        )
        qubits = entry["resources"]["qubits"]
        require(
            type(qubits) is int
            and qubits >= (arity + nout) * W
            and qubits == origin["native_qubits_declared_in_metadata"],
            "Original full native allocation",
        )
        private = max(private, qubits - nout * W)
        metadata[call["leaf"]] = entry
    noninputs = total - len(inputs)
    invocations = []
    for instance in range(2 if scalar else 1):
        external = [instance] if scalar else [0, 1]
        banks = [word * W for word in external]
        banks.extend(4 * W + (value - len(inputs)) * W for value in range(len(inputs), total))
        invocations.append(
            dict(
                value_banks=banks,
                external_input_words=external,
                external_output_words=external,
                outputs=outputs,
                forward_calls=calls,
            )
        )
    wrapper = dict(
        schema="two-draw-actual-native-wrapper-v1",
        label=label,
        word_width=W,
        fraction_bits=F,
        native_input_offsets=[0, W],
        dirty_output_offsets=[2 * W, 3 * W],
        internal_SSA_words=noninputs,
        SSA_base=4 * W,
        private_base=(4 + noninputs) * W,
        private_qubits=private,
        logical_qubits=(4 + noninputs) * W + private,
        initial_H_separate=64,
        original_source=path_key(directory / "source.json"),
        original_target=path_key(target_path),
        invocations=invocations,
        leaves=origins,
        clean_schedule="F, full72 output XORs, literal F inverse; serial complete invocations",
        literal_wrapper_inverse="reverse invocation order; same F/CX/literal F^-1 blocks",
        scratch_reuse_only_after_complete_cleanup=True,
        original_nodes_retained=len(nodes),
    )
    require(wrapper["logical_qubits"] <= CAP, "Both complete wrappers fit common45000 cap")
    return wrapper, metadata, dict(nodes=nodes, tables=target["tables"], outputs=outputs)


def make_engine():
    """Only our independent scanner and full packed traversal; no disk JIT cache."""
    import numpy as np
    from numba import njit

    @njit(cache=False)
    def scan(array, start, stop, inverse, tlevels, clevels, counts, macro_wires, macro_t):
        size = len(tlevels)
        for position in range(start, stop):
            row = len(array) - 1 - position if inverse else position
            kind, a, b, c = array[row]
            if kind < 1 or kind > 3 or a < 0 or a >= size:
                raise ValueError("Native opcode/allocated first wire")
            if kind == 1 and b != 0 or kind != 3 and c != 0:
                raise ValueError("Unused native operands must be zero")
            if kind >= 2 and (b < 0 or b >= size or b == a):
                raise ValueError("Distinct allocated second wire")
            if kind == 3 and (c < 0 or c >= size or c == a or c == b):
                raise ValueError("Distinct allocated third wire")
            counts[kind - 1] += 1
            if kind == 1:
                clevels[a] += 1
            elif kind == 2:
                tl, cl = max(tlevels[a], tlevels[b]), max(clevels[a], clevels[b]) + 1
                tlevels[a] = tlevels[b] = tl
                clevels[a] = clevels[b] = cl
            else:
                wires = (a, b, c)
                for step in range(len(macro_t)):
                    first, second = wires[macro_wires[step, 0]], wires[macro_wires[step, 1]]
                    tl = max(tlevels[first], tlevels[second]) + macro_t[step]
                    cl = max(clevels[first], clevels[second]) + 1
                    tlevels[first] = tlevels[second] = tl
                    clevels[first] = clevels[second] = cl

    @njit(cache=False)
    def traverse(array, mapping, state, start, stop, inverse):
        for position in range(start, stop):
            row = len(array) - 1 - position if inverse else position
            opcode, a, b, c = array[row]
            if opcode == 1:
                state[mapping[a]] ^= np.uint64(65535)
            elif opcode == 2:
                state[mapping[b]] ^= state[mapping[a]]
            elif opcode == 3:
                state[mapping[c]] ^= state[mapping[a]] & state[mapping[b]]
            else:
                raise ValueError("Unscanned native opcode")

    roles = {"a": 0, "b": 1, "target": 2}
    wires = np.asarray([(roles[row[1]], roles[row[-1]]) for row in CCX], dtype=np.int64)
    tflags = np.asarray([int(row[0] in ("T", "Tdg")) for row in CCX], dtype=np.int64)
    return np, scan, traverse, wires, tflags


def scan_leaves(wrapper, metadata, engine, frozen, started):
    np, scanner, _, macro_wires, macro_t = engine
    leaves, loaded = {}, {}
    for key, origin in sorted(wrapper["leaves"].items()):
        budget(started)
        entry = metadata[key]
        array = np.load(
            bound(ROOT / origin["native_gate_file"], frozen), mmap_mode="r", allow_pickle=False
        )
        require(
            array.dtype == np.dtype("int32") and array.ndim == 2 and array.shape[1] == 4,
            "Actual int32(N,4) native array",
        )
        qubits = entry["resources"]["qubits"]
        directions = []
        for inverse in (False, True):
            levels, depths, counts = (
                np.zeros(qubits, np.int64),
                np.zeros(qubits, np.int64),
                np.zeros(3, np.int64),
            )
            for start in range(0, len(array), CHUNK):
                budget(started)
                scanner(
                    array,
                    start,
                    min(start + CHUNK, len(array)),
                    inverse,
                    levels,
                    depths,
                    counts,
                    macro_wires,
                    macro_t,
                )
                budget(started)
            x, cx, ccx = (int(value) for value in counts)
            directions.append(
                dict(
                    x=x,
                    cx=cx,
                    ccx=ccx,
                    source_gates=len(array),
                    t_count=7 * ccx,
                    t_depth=int(levels.max()),
                    clifford_t_depth=int(depths.max()),
                )
            )
        same(
            {field: entry["resources"][field] for field in FIELDS},
            directions[0],
            "Independent forward scan matches original immutable resources",
        )
        leaves[key] = dict(
            qubits=qubits,
            native_args=entry["args"],
            native_outputs=entry["outs"],
            native_gate_file=origin["native_gate_file"],
            gate_sha256=entry["sha256"],
            forward=directions[0],
            literal_inverse=directions[1],
        )
        loaded[key] = (entry, array)
    return leaves, loaded


def resources(wrapper, leaves):
    fwd, inv = Counter(), Counter()
    argument_cx, argument_depth, output_cx, output_depth = 0, 0, 0, 0
    for invocation in wrapper["invocations"]:
        for call in invocation["forward_calls"]:
            for field in FIELDS:
                fwd[field] += leaves[call["leaf"]]["forward"][field]
                inv[field] += leaves[call["leaf"]]["literal_inverse"][field]
            argument_cx += 2 * W * len(call["args"])
            argument_depth += max(Counter(call["args"]).values(), default=0)
        output_cx += W * len(invocation["outputs"])
        output_depth += max(Counter(invocation["outputs"]).values(), default=0)
    clean = {field: fwd[field] + inv[field] for field in FIELDS}
    clean["cx"] += 2 * argument_cx + output_cx
    clean["source_gates"] += 2 * argument_cx + output_cx
    clean["clifford_t_depth"] += 4 * argument_depth + output_depth
    clean.update(
        clifford_cx=clean["cx"] + 6 * clean["ccx"],
        clifford_h=2 * clean["ccx"],
        logical_qubits=wrapper["logical_qubits"],
        max_reused_scratch_qubits=wrapper["private_qubits"],
        internal_full72_SSA_words=wrapper["internal_SSA_words"],
        native_input_words=2,
        dirty_output_words=2,
        initial_Hadamards_separate=64,
        t_depth_schedule="serial complete actual leaves; exact7T ASAP each direction",
        ccx_expansion="phase-correct sevenT/sixCX/twoH with both control-wire phases",
    )
    return dict(
        label=wrapper["label"],
        clean_resources=clean,
        native_leaves=leaves,
        forward_native_resources=dict(fwd),
        literal_inverse_native_resources=dict(inv),
        argument_copy_CX_forward=argument_cx,
        argument_copy_CX_inverse=argument_cx,
        argument_copy_depth_sum_forward=argument_depth,
        full72_output_copy_CX=output_cx,
        full72_output_copy_depth=output_depth,
        immutable_source_invocations=len(wrapper["invocations"]),
        native_high_wires_full_banks_literal_uncompute_all_charged=True,
        financial_source_cost_divided_by_coordinate_count=False,
    )


def quantile(raw, literals):
    require(type(raw) is int and 0 <= raw < 1 << 32, "Exact raw q32 quantile input")
    p = 256 * raw + 128
    displacement = p - SCALE // 2
    probability = min(p, SCALE - p)

    def polynomial(coefficients, x):
        total = coefficients[-1]
        for coefficient in reversed(coefficients[:-1]):
            total = total * x // SCALE + coefficient
        return total

    if probability * 40 < 3 * SCALE:
        exponent = probability.bit_length() - 41
        normalized = probability << -exponent
        bucket = (normalized - SCALE) >> 35
        offset = normalized - SCALE - (bucket << 35) - (1 << 34)
        logvalue = (
            polynomial(literals["log_table"][bucket], offset) + exponent * literals["ln2_raw"]
        )
        x = isqrt(-logvalue * SCALE) - literals["tail_shift_raw"]
        numerator = polynomial(literals["tail_A_raw"], x)
        denominator = polynomial(literals["tail_B_raw"], x)
    else:
        absolute = abs(displacement)
        x = literals["central_rconstant_raw"] - absolute * absolute // SCALE
        numerator = absolute * polynomial(literals["central_A_raw"], x) // SCALE
        denominator = polynomial(literals["central_B_raw"], x)
    require(
        0 <= numerator < 1 << W and SCALE <= denominator < 1 << 64,
        "Native numerator/denominator diagnostic contract",
    )
    result = numerator * SCALE // denominator
    return (-result if displacement < 0 else result) & MASK


def original_pair(target, words):
    values = {}
    for node in target["nodes"]:
        args = [values[value] for value in node["args"]]
        signed = [raw - (1 << W) if raw >= 1 << 71 else raw for raw in args]
        op, params = node["op"], node["params"]
        if op == "input":
            results = [words[node["out"][0]]]
        elif op == "const":
            results = [params["value"]]
        elif op == "add":
            results = [sum(signed)]
        elif op == "sub":
            results = [signed[0] - signed[1]]
        elif op == "mul":
            results = [signed[0] * signed[1] // SCALE]
        elif op == "cmul":
            results = [signed[0] * params["c"] // SCALE]
        elif op == "lt":
            results = [int(signed[0] < signed[1])]
        elif op == "select":
            results = [args[1] if args[0] & 1 else args[2]]
        elif op == "positive":
            results = [max(0, signed[0])]
        elif op == "sqrt":
            results = [isqrt(args[0] * SCALE)]
        elif op == "msb":
            results = [max(0, args[0].bit_length() - 1)]
        elif op == "shift":
            shift = signed[1]
            results = [
                0
                if shift >= W
                else int(signed[0] < 0) * -1
                if shift <= -W
                else signed[0] * (1 << shift)
                if shift >= 0
                else signed[0] // (1 << -shift)
            ]
        elif op == "bits":
            value = signed[0] if params.get("signed") else args[0]
            shift = params["shift"]
            results = [
                (value // (1 << shift) if shift >= 0 else value * (1 << -shift))
                & ((1 << params["width"]) - 1)
            ]
        elif op == "lookup":
            results = target["tables"][params["table"]][args[0] & ((1 << params["bits"]) - 1)]
        else:
            raise ValueError("Unexpected original pair operation: " + op)
        require(len(results) == len(node["out"]), "Native pair multi-output arity")
        for output, value in zip(node["out"], results, strict=True):
            require(type(value) is int, "Native integer semantics only")
            values[output] = value & MASK
    return [values[output] for output in target["outputs"]]


def initial_state(wrapper, np):
    state = np.zeros(wrapper["logical_qubits"], dtype=np.uint64)
    for pair_index, words in enumerate(PAIRS):
        for dirty_index in range(2):
            lane, dirty = 2 * pair_index + dirty_index, MASK if dirty_index else 0
            for word_index, word in enumerate((*words, dirty, dirty)):
                for bit in range(W):
                    state[word_index * W + bit] |= np.uint64(((word >> bit) & 1) << lane)
    return state


def apply(wrapper, state, loaded, engine, started, inverse=False):
    np, _, traversal, _, _ = engine
    require(
        state.dtype == np.dtype("uint64")
        and state.shape == (wrapper["logical_qubits"],)
        and not np.any(state >> np.uint64(16)),
        "Complete allocated uint64 fixed16lane state",
    )
    invocations = list(reversed(wrapper["invocations"])) if inverse else wrapper["invocations"]
    for invocation in invocations:
        budget(started)
        require(not np.any(state[wrapper["SSA_base"] :]), "All work zero before reuse")
        banks = invocation["value_banks"]

        def dispatch(call, reverse):
            entry, array = loaded[call["leaf"]]
            nargs, nout = len(call["args"]), len(call["out"])
            scratch = wrapper["private_base"]
            mapping = np.empty(entry["resources"]["qubits"], dtype=np.int64)
            for wire in range(len(mapping)):
                if nargs * W <= wire < (nargs + nout) * W:
                    output = call["out"][(wire // W) - nargs]
                    mapping[wire] = banks[output] + wire % W
                elif wire < nargs * W:
                    mapping[wire] = scratch + wire
                else:
                    mapping[wire] = scratch + wire - nout * W
            require(
                len(set(int(value) for value in mapping)) == len(mapping)
                and int(mapping.min()) >= 0
                and int(mapping.max()) < len(state),
                "Complete native high-wire map is injective and allocated",
            )
            copies = list(enumerate(call["args"]))
            if reverse:
                copies.reverse()
            for occurrence, arg in copies:
                low = scratch + occurrence * W
                state[low : low + W] ^= state[banks[arg] : banks[arg] + W]
            for start in range(0, len(array), CHUNK):
                budget(started)
                traversal(array, mapping, state, start, min(start + CHUNK, len(array)), reverse)
                budget(started)
            for occurrence, arg in copies:
                low = scratch + occurrence * W
                state[low : low + W] ^= state[banks[arg] : banks[arg] + W]
            require(
                not np.any(state[scratch:]), "All argument/private bits restored after native call"
            )

        for call in invocation["forward_calls"]:
            dispatch(call, False)
        outputs = list(zip(invocation["outputs"], invocation["external_output_words"], strict=True))
        if inverse:
            outputs.reverse()
        for value, word in outputs:
            low = (2 + word) * W
            state[low : low + W] ^= state[banks[value] : banks[value] + W]
        for call in reversed(invocation["forward_calls"]):
            dispatch(call, True)
        require(
            not np.any(state[wrapper["SSA_base"] :]),
            "Every full72 work word and private bit restored",
        )
    require(not np.any(state >> np.uint64(16)), "No state bits beyond the fixed16 lanes")


def replay_rows(wrapper, target, literals, states, started):
    before, after, restored = states
    rows = []
    for pair_index, words in enumerate(PAIRS):
        for dirty_index in range(2):
            budget(started)
            lane, dirty = 2 * pair_index + dirty_index, MASK if dirty_index else 0
            values = (
                [quantile(word, literals) for word in words]
                if wrapper["label"] == LABELS[0]
                else original_pair(target, words)
            )
            expected = [value ^ dirty for value in values]
            for wire in range(wrapper["logical_qubits"]):
                if wire % 1024 == 0:
                    budget(started)
                bank, bit = divmod(wire, W)
                input_word = (*words, dirty, dirty)[bank] if bank < 4 else 0
                output_word = (*words, *expected)[bank] if bank < 4 else 0
                require(
                    ((int(before[wire]) >> lane) & 1) == ((input_word >> bit) & 1),
                    "Every initial allocated bit",
                )
                require(
                    ((int(after[wire]) >> lane) & 1) == ((output_word >> bit) & 1),
                    "Every final input/dirtyoutput/work bit",
                )
                require(
                    ((int(restored[wire]) >> lane) & 1) == ((input_word >> bit) & 1),
                    "Every literal inverse restored bit",
                )
            observed = [
                sum(((int(after[(2 + bank) * W + bit]) >> lane) & 1) << bit for bit in range(W))
                for bank in range(2)
            ]
            rows.append(
                dict(
                    loader=wrapper["label"],
                    pair_index=pair_index,
                    dirty_index=dirty_index,
                    lane=lane,
                    q32_raw=list(words),
                    initial_outputs72=[dirty, dirty],
                    expected_outputs72=expected,
                    observed_outputs72=observed,
                    full_native_inputs72_preserved=True,
                    all_full_SSA_and_native_private_bits_clean=True,
                    literal_inverse_restores_complete_state=True,
                    all_allocated_bits_checked=True,
                    allocated_state_qubits=len(after),
                    actual_immutable_gate_replay=True,
                    basis_diagnostic_is_not_all_input_or_phase_proof=True,
                )
            )
    return rows


def seal(output, frozen, summary, started):
    final_verify(frozen, started)
    save(output / "summary.json", summary, started)
    files = {
        path_key(path): sha(path, started) for path in sorted(output.rglob("*")) if path.is_file()
    }
    verify(frozen, started)
    cpu, wall = budget(started)
    content = (
        json.dumps(
            dict(
                files=files,
                frozen_inputs=frozen,
                terminal_record=path_key(output / "summary.json"),
                manifest_self_hash_excluded=True,
                process_CPU_seconds_before_terminal=cpu,
                wall_seconds_before_terminal=wall,
            ),
            indent=2,
            allow_nan=False,
        )
        + "\n"
    ).encode()
    budget(started)
    with (output / "manifest.json").open("xb") as stream:
        for offset in range(0, len(content), 1 << 20):
            budget(started)
            stream.write(content[offset : offset + (1 << 20)])
            budget(started)


def preserve_failure(output, frozen, failure, phase, started):
    if not output.exists():
        return
    try:
        budget(started)
        save(
            output / (phase + "_failure.json"),
            dict(
                type=type(failure).__name__,
                message=str(failure),
                traceback=traceback.format_exc(),
                fixed_receipt_terminal_no_retry=True,
            ),
            started,
        )
        terminal = output / (
            "completion_outcome.json" if (output / "summary.json").exists() else "summary.json"
        )
        summary = dict(
            passed=False,
            budget_censored=isinstance(failure, (BudgetCensoredError, TimeoutError)),
            local_only=True,
            new_test_credit=0,
            fixed_receipt_terminal_no_retry=True,
            financial_source_adopted=False,
            quantum_advantage_claim=False,
        )
        save(terminal, summary, started)
        require(
            not (output / "manifest.json").exists(), "Existing/partial manifest cannot be replaced"
        )
        files = {
            path_key(path): sha(path, started)
            for path in sorted(output.rglob("*"))
            if path.is_file()
        }
        final_verify(frozen, started)
        encoded = (
            json.dumps(
                dict(
                    files=files,
                    frozen_inputs=frozen,
                    terminal_record=path_key(terminal),
                    manifest_self_hash_excluded=True,
                    failed_audit_fixture_credit=0,
                ),
                indent=2,
            )
            + "\n"
        ).encode()
        budget(started)
        with (output / "manifest.json").open("xb") as stream:
            for offset in range(0, len(encoded), 1 << 20):
                budget(started)
                stream.write(encoded[offset : offset + (1 << 20)])
                budget(started)
    except BaseException as retention:
        marker = output / "failed_unsealed.json"
        if not marker.exists():
            save(
                marker,
                dict(
                    passed=False,
                    receipt_unsealed=True,
                    new_test_credit=0,
                    phase=phase,
                    error=str(failure)[:1024],
                    retention_error=str(retention)[:1024],
                    budget_censored=isinstance(failure, (BudgetCensoredError, TimeoutError))
                    or isinstance(retention, BudgetCensoredError),
                    fixed_receipt_terminal_no_retry=True,
                    no_further_hashing_or_verification=True,
                ),
            )


def prepare(output):
    _PATHS.clear()
    _HASHES.clear()
    _OBSERVED.clear()
    require(
        sys.dont_write_bytecode is True, "Audit process must start with bytecode writes disabled"
    )
    output = Path(output).resolve()
    require(output == OUTPUT.resolve() and not output.exists(), "Fresh exact independent receipt")
    started, frozen = (time.process_time(), time.monotonic()), {}
    try:
        summary = read(SOURCE / "summary.json")
        require(
            summary.get("passed") is True
            and summary.get("budget_censored") is False
            and summary.get("new_test_credit") == 32
            and summary.get("tests_completed") == 32,
            "Completed uncensored source with exactly32 fixed fixtures",
        )
        require(
            summary["full_financial_sampler_or_estimator_adopted"] is False
            and summary["full_financial_native_cost"] is None
            and summary["physical_runtime"] is None
            and summary["full_G2"] is False
            and summary["quantum_advantage_established"] is False,
            "Source preserves component-only scope and unresolved financial obligations",
        )
        require(
            not any(
                (SOURCE / name).exists()
                for name in (
                    "failed_unsealed.json",
                    "completion_outcome.json",
                    "prepare_failure.json",
                    "run_failure.json",
                )
            ),
            "Failed/unsealed producer cannot release audit",
        )
        merge_manifest(SOURCE, frozen, started)
        source_protocol = read(bound(SOURCE / "protocol.json", frozen))
        require(
            source_protocol["frozen_before_closure_arrays_costs_replays_tests"] is True
            and source_protocol["required_release_packet"] == "WAVE10_run002"
            and source_protocol["historical_fixture_credit_added_again"] == 0
            and source_protocol["failed_WAVE10_run001_credit"] == 0
            and source_protocol["JIT_disk_cache"] is False
            and source_protocol["bytecode_writes_disabled"] is True
            and source_protocol["existing_package_bytecode_and_distribution_metadata_bound"] is True
            and source_protocol["declared_unique_tests"] == 32
            and source_protocol["native_input_bits"] == 144
            and source_protocol["dirty_output_bits"] == 144
            and source_protocol["uniform_preparation_H_separate"] == 64
            and source_protocol["native_width"] == W
            and source_protocol["fraction_bits"] == F,
            "Original immutable source protocol before all actual work",
        )
        require(
            source_protocol["process_CPU_seconds"] == 300
            and source_protocol["admission_CPU_seconds"] == 240
            and source_protocol["wall_seconds"] == 600
            and source_protocol["numerical_threads"] == 1
            and source_protocol["exact7T_phase_proof_separate_from_basis_fixtures"] is True
            and source_protocol["full_array_chunk_gate_rows"] == CHUNK,
            "Published producer budgets, serial scan chunks and phase-proof scope stay fixed",
        )
        same(source_protocol["fixed_labels"], LABELS, "Exactly two frozen loaders")
        same(source_protocol["fixed_input_pairs"], PAIRS, "Exactly the frozen eight input pairs")
        same(
            source_protocol["dirty_outputs_each72"], [0, MASK], "Exactly two dirty output patterns"
        )
        require(
            source_protocol["packed_lanes_per_loader"] == 16
            and source_protocol["packed_lane_mask"] == LANEMASK
            and source_protocol["logical_qubit_cap"] == CAP,
            "Fixed complete packed allocation and cap",
        )
        for path in (Path(__file__).resolve(), PREFLIGHT, PLAN):
            require(
                frozen.get(path_key(path)) == sha(path, started),
                "Independent author/preflight frozen before producer work",
            )
        plan = read(PLAN)
        preflight = read(PREFLIGHT)
        same(
            preflight["original_author_sha256"],
            ORIGINAL_AUTHORS,
            "All original8 author SHA pins unchanged",
        )
        require(
            preflight["original_admission_failure_manifest_sha256"] == ADMISSION_FAILURE_SHA
            and preflight["original_root_review_manifest_sha256"] == ROOT_REVIEW_SHA,
            "Pinned original root review and observed pre-mkdir admission failure",
        )
        require(
            not (PROGRAM / "A02_two_draw_loader_resource_run001").exists(),
            "Original failed intended receipt remains absent, no fabricated protocol",
        )
        for name, expected in ORIGINAL_AUTHORS.items():
            budget(started)
            require(
                frozen.get(path_key(RESEARCH / name)) == expected,
                "Original frozen author bytes retained before new producer work",
            )
        for name, expected, counts in (
            ("A02_two_draw_loader_admission_failure_run001", ADMISSION_FAILURE_SHA, (10, 10)),
            ("A02_two_draw_root_review_run001", ROOT_REVIEW_SHA, (1, 8)),
        ):
            budget(started)
            manifest_path = bound(PROGRAM / name / "manifest.json", frozen)
            require(
                frozen[path_key(manifest_path)] == expected,
                "Original prerequisite manifest SHA fixed",
            )
            manifest_data = read(manifest_path)
            require(
                (len(manifest_data["files"]), len(manifest_data["frozen_inputs"])) == counts,
                "Complete original prerequisite map inventory",
            )
            for mapping, base, _ in original_maps(manifest_path):
                for path, expected_hash in mapping.items():
                    budget(started)
                    require(
                        frozen.get(path_key(base / path)) == expected_hash,
                        "Every original diagnostic/review byte frozen before producer work",
                    )
        failure_summary = read(
            bound(PROGRAM / "A02_two_draw_loader_admission_failure_run001/summary.json", frozen)
        )
        require(
            failure_summary["passed"] is False
            and failure_summary["failed_intended_receipt"] == "A02_two_draw_loader_resource_run001"
            and failure_summary["failed_intended_receipt_absent"] is True
            and failure_summary["protocol_or_array_or_cost_or_replay_or_fixture_execution"] is False
            and failure_summary["new_test_credit"] == 0
            and failure_summary["frozen_original8_author_bytes_preserved"] is True,
            "Original pre-mkdir failure has no protocol, numerical work, fixtures or credit",
        )
        same(
            failure_summary["fixed_CPU_hard_admission_wall_seconds"],
            [300, 240, 600],
            "Original producer budget unchanged",
        )
        review = read(bound(PROGRAM / "A02_two_draw_root_review_run001/summary.json", frozen))
        require(
            review["root_and_peer_static_review_passed"] is True
            and review["no_actual_numeric_cost_replay_or_fixture_result_claim"] is True,
            "Original root review retained separately from execution",
        )
        same(
            review["reviewed_source_sha256"],
            ORIGINAL_AUTHORS,
            "Original root review exact8 source hashes",
        )
        require(
            preflight["independent_audit"]["process_CPU_seconds"] == CPU
            and preflight["independent_audit"]["admission_CPU_seconds"] == ADMISSION
            and preflight["independent_audit"]["wall_seconds"] == WALL,
            "Fixed independent admission/CPU/wall budgets",
        )
        require(
            preflight["failed_WAVE10_run001_manifest_sha256"] == FAILED_W10_SHA
            and frozen.get(path_key(PROGRAM / "WAVE10_run001/manifest.json")) == FAILED_W10_SHA,
            "Original failed finalizer manifest fixed independently",
        )
        require(
            preflight["archive_reconciliation_manifest_sha256"] == DRIFT_MANIFEST_SHA
            and frozen.get(path_key(PROGRAM / "A01_drift_run001/manifest.json"))
            == DRIFT_MANIFEST_SHA,
            "Complete original archival reconciliation owner manifest pinned independently",
        )
        failed = read(bound(PROGRAM / "WAVE10_run001/summary.json", frozen))
        require(
            failed["passed"] is False
            and failed["budget_censored"] is True
            and failed["new_test_credit"] == 0,
            "Censored original cumulative packet is zero credit",
        )
        wave = read(bound(PROGRAM / "WAVE10_run002/summary.json", frozen))
        require(
            wave["passed"] is True
            and wave["archived_or_current_integrity_passed"] is True
            and wave["global_live_integrity"] is False
            and wave["legitimate_expected_hashes_waived"] is False,
            "Completed strict W10 release retains historical mismatch evidence",
        )
        same(
            read(bound(PROGRAM / "WAVE10_run002/progress_snapshot.json", frozen))[
                "static_author_preflights"
            ]["dependency_order"],
            preflight["fixed18_selected_labels"],
            "Exact immutable fixed18 release snapshot",
        )
        for row in plan["author_readonly_input_bindings"]:
            bind(frozen, row["path"], row["author_readonly_sha256"], started)
        for name in (
            "A02_quantile_scalar_run001",
            "A02_quantile_scalar_audit_run001",
            "C06_pair_run001",
            "C06_pair_audit_run001",
            "A10_coefficient_run001",
        ):
            budget(started)
            previous = read(bound(PROGRAM / name / "summary.json", frozen))
            require(
                previous["passed"] is True and not previous.get("budget_censored", False),
                "Original source and independent audit prerequisite passed uncensored",
            )
        # The source's strict frozen map already contains complete original
        # receipt maps. These independent plan hashes establish their trust roots.
        for specification in ("AS241_wrapper", "BoxMuller_wrapper"):
            for row in plan[specification]["actual_leaf_inventory"]:
                bind(frozen, row["metadata"], row["metadata_sha256"], started)
                bind(
                    frozen,
                    row["native_gate_file"],
                    row["native_gate_sha256_from_archived_metadata"],
                    started,
                )
        verify(frozen, started)
        verify_runtime(source_protocol["interpreter_binding"], frozen, started)
        verify_loaded_tools(frozen, started)
        budget(started, admission=True)
        output.mkdir()
        for path in (Path(__file__).resolve(), PREFLIGHT):
            destination = output / path.name
            shutil.copy2(path, destination)
            require(
                sha(destination, started) == frozen[path_key(path)],
                "Immutable audit source/preflight copy",
            )
            bind(frozen, destination, frozen[path_key(path)], started)
        verify(frozen, started)
        save(
            output / "protocol.json",
            dict(
                schema="independent-two-draw-audit-protocol-v2",
                created_utc=datetime.now(timezone.utc).isoformat(),
                frozen_inputs=frozen,
                source_receipt=path_key(SOURCE),
                local_only=True,
                audited_helper_imports=0,
                numerical_imports_before_protocol=0,
                JIT_disk_cache=False,
                bytecode_writes_disabled=True,
                installed_distribution_metadata_bytes_bound=True,
                existing_tool_bytecode_bytes_bound=True,
                independent_native_reexecutions=32,
                unique_new_fixture_credit=0,
                process_CPU_seconds=CPU,
                admission_CPU_seconds=ADMISSION,
                wall_seconds=WALL,
                actual_interpreter=path_key(sys.executable),
                python_version=sys.version,
                interpreter_binding=source_protocol["interpreter_binding"],
                invocation_local_confined_path_cache=True,
                invocation_local_stat_guarded_actual_SHA_cache=True,
                expected_SHA_values_never_inserted_into_actual_cache=True,
                final_fresh_verification_includes_all_actual_observed_paths_and_scoped_base=True,
                original_paired_admission_failure_fixture_credit=0,
                final_unique_input_verification_fresh=True,
            ),
            started,
        )
    except BaseException as failure:
        preserve_failure(output, frozen, failure, "prepare", started)
        raise


def run(output):
    _PATHS.clear()
    _HASHES.clear()
    _OBSERVED.clear()
    require(
        sys.dont_write_bytecode is True, "Audit process must start with bytecode writes disabled"
    )
    output = Path(output).resolve()
    require(output == OUTPUT.resolve() and output.is_dir(), "Exact prepared independent audit")
    require(
        not any(
            (output / name).exists()
            for name in (
                "summary.json",
                "run_started.json",
                "run_failure.json",
                "prepare_failure.json",
                "failed_unsealed.json",
                "manifest.json",
            )
        ),
        "No terminal/partial audit retry",
    )
    started = (time.process_time(), time.monotonic())
    protocol = read(output / "protocol.json")
    frozen = protocol["frozen_inputs"]
    try:
        verify(frozen, started)
        require(
            path_key(sys.executable) == protocol["actual_interpreter"]
            and sys.version == protocol["python_version"],
            "Actual invoked interpreter unchanged",
        )
        for key in (
            "OPENBLAS_NUM_THREADS",
            "MKL_NUM_THREADS",
            "OMP_NUM_THREADS",
            "NUMBA_NUM_THREADS",
            "NUMEXPR_NUM_THREADS",
        ):
            os.environ[key] = "1"
        verify_runtime(protocol["interpreter_binding"], frozen, started)
        verify_loaded_tools(frozen, started)
        save(
            output / "run_started.json",
            dict(
                fixed_receipt_terminal_no_retry=True,
                independent_native_reexecution_count=32,
                unique_new_fixture_credit=0,
            ),
            started,
        )
        origin_checks = verify_dependency_origins(frozen, started)
        plan = read(bound(PLAN, frozen))
        phase = phase_premise(frozen)
        budget(started, admission=True)
        engine = make_engine()
        verify_loaded_tools(frozen, started)
        np = engine[0]
        for name in PACKAGES:
            path = Path(sys.modules[name].__file__)
            require(
                frozen.get(path_key(path)) == sha(path, started),
                "Actual independent lazy numerical package origin was frozen",
            )
        wrappers = read(bound(SOURCE / "wrappers.json", frozen))
        saved_resources = read(bound(SOURCE / "native_resource_ledger.json", frozen))
        saved_targets = read(bound(SOURCE / "selected_original_targets.json", frozen))
        require(
            set(wrappers) == set(saved_resources) == set(saved_targets) == set(LABELS),
            "Exactly the two declared complete loaders",
        )
        literals = read(bound(SCALAR / "literals.json", frozen))
        pair_scope = read(
            bound(PROGRAM / "C06_pair_audit_run001/actual_pair_scope_audit.json", frozen)
        )
        row = pair_scope["B4x12"]["independently_walked_pair_scopes"][0]
        same(
            (
                row["normal_values"],
                row["raw_uniform_values"],
                row["radius"],
                row["log"]["output"],
                [value["output"] for value in row["cosines"]],
            ),
            ([94, 125], [0, 1], 58, 52, [93, 124]),
            "Original shared pair provenance, with both cosines retained",
        )
        binding = read(bound(PROGRAM / "C06_pair_run001/certificate.json", frozen))[
            "source_bindings"
        ]["B4x12"]
        require(
            binding["target_sha256"] == frozen[path_key(BM / "target.json")]
            and binding["normal_values"][:2] == [94, 125],
            "Original accepted pair target binding",
        )
        ledgers, records = {}, []
        for label in LABELS:
            budget(started)
            wrapper, metadata, target = derive_one(label, plan, frozen, started)
            same(
                saved_targets[label],
                dict(width=W, fraction_bits=F, **target),
                "Selected original target retains actual nodes/tables/outputs unchanged",
            )
            same(wrappers[label], wrapper, "Independently reconstructed complete wrapper/bank maps")
            budget(started, admission=True)
            verify_loaded_tools(frozen, started)
            leaves, loaded = scan_leaves(wrapper, metadata, engine, frozen, started)
            ledger = resources(wrapper, leaves)
            same(saved_resources[label], ledger, "Independently scanned complete resource ledger")
            ledgers[label] = ledger
            budget(started, admission=True)
            verify_loaded_tools(frozen, started)
            before = initial_state(wrapper, np)
            after = before.copy()
            apply(wrapper, after, loaded, engine, started)
            restored = after.copy()
            apply(wrapper, restored, loaded, engine, started, inverse=True)
            for suffix, state in zip(
                ("before", "after", "restored"), (before, after, restored), strict=True
            ):
                saved = np.load(
                    bound(SOURCE / (label + "_" + suffix + ".npy"), frozen), allow_pickle=False
                )
                require(
                    saved.dtype == np.dtype("uint64")
                    and saved.shape == state.shape
                    and not np.any(saved >> np.uint64(16))
                    and np.array_equal(saved, state),
                    "Independent traversal agrees with every original allocated lane mask: "
                    + suffix,
                )
                budget(started)
                np.save(
                    output / (label + "_independent_" + suffix + ".npy"), state, allow_pickle=False
                )
                budget(started)
            records.extend(
                replay_rows(wrapper, target, literals, (before, after, restored), started)
            )
        replay = read(bound(SOURCE / "actual_gate_replays.json", frozen))
        require(
            replay["completed_replays"] == 32
            and replay["old_fixture_recredit"] == 0
            and replay["fixed_basis_diagnostics_not_all_input_or_phase_proof"] is True,
            "Exactly32 retained basis diagnostics, no old credit or all-input claim",
        )
        same(
            replay["rows"],
            records,
            "Every producer replay record agrees with independent traversal and integers",
        )
        xml = ET.parse(bound(SOURCE / "tests.xml", frozen)).getroot()
        testcases = list(xml.iter("testcase"))
        identities = [(case.get("classname", ""), case.get("name")) for case in testcases]
        require(
            len(testcases) == len(set(identities)) == 32
            and all(name for _, name in identities)
            and not any(
                case.find(tag) is not None
                for case in testcases
                for tag in ("error", "failure", "skipped")
            ),
            "Exactly32 distinct successful actual XML test identities",
        )
        expected_names = {
            "test_actual_complete_native_loader_and_literal_inverse["
            + f"{label}-pair{pair}-dirty{dirty}]"
            for label in LABELS
            for pair in range(len(PAIRS))
            for dirty in range(2)
        }
        require(
            {name for _, name in identities} == expected_names,
            "Actual XML retains exactly the two-loader/eight-pair/two-dirty fixture inventory",
        )
        suites = [suite for suite in xml.iter("testsuite") if list(suite.findall("testcase"))]
        require(
            sum(int(suite.get("tests", 0)) for suite in suites) == 32
            and all(
                int(suite.get(field, 0)) == 0
                for suite in suites
                for field in ("errors", "failures", "skipped")
            ),
            "JUnit declared counts agree with all32 actual successful identities",
        )
        credit = read(bound(SOURCE / "test_credit_reconciliation.json", frozen))
        require(
            credit["unique_new_fixtures_passed"] == 32
            and credit["prior_fixture_counts_added_again"] == 0,
            "Producer's new fixed fixture credit reconciled",
        )
        same(
            sorted(credit["test_identities"]),
            sorted(identities),
            "Actual XML identities equal credit ledger",
        )
        adopted = (
            ledgers[LABELS[0]]["clean_resources"]["t_count"]
            < ledgers[LABELS[1]]["clean_resources"]["t_count"]
        )
        decision = read(bound(SOURCE / "paired_component_decision.json", frozen))
        same(
            read(bound(SOURCE / "summary.json", frozen))["paired_component_decision"],
            decision,
            "Original terminal summary and provisional component decision agree",
        )
        require(
            decision["AS241_component_strict_T_improvement"] is adopted
            and decision["AS241_component_eligible_pending_independent_audit"] is adopted
            and decision["paired_AS241_component_adopted"] is False
            and decision["independent_resource_audit_still_required"] is True
            and decision["both_losing_or_winning_resource_rows_preserved"] is True
            and decision["comparison_unit"]
            == "two actual AS241 scalar invocations versus one actual unchanged shared BM pair"
            and decision["financial_source_cost_divided_by_coordinate_count"] is False
            and decision["complete_financial_sampler_or_estimator_adopted"] is False,
            "Producer comparison remains provisional until this independent complete audit",
        )
        save(output / "independent_dependency_origin_checks.json", origin_checks, started)
        save(output / "independent_phase_premise.json", phase, started)
        save(output / "independent_native_resource_ledger.json", ledgers, started)
        save(
            output / "independent_actual_gate_replays.json",
            dict(
                completed_independent_reexecutions=32,
                rows=records,
                all_allocated_lane_masks_compared=True,
                unique_new_fixture_credit=0,
                basis_diagnostics_not_all_input_or_phase_proof=True,
            ),
            started,
        )
        verify_runtime(protocol["interpreter_binding"], frozen, started)
        verify_loaded_tools(frozen, started)
        cpu, wall = budget(started)
        summary = dict(
            passed=True,
            budget_censored=False,
            local_only=True,
            independent_two_draw_resource_audit_passed=True,
            producer_actual_tests_verified=32,
            independent_native_reexecutions=32,
            new_test_credit=0,
            original_paired_admission_failure_fixture_credit=0,
            old_fixture_recredit=0,
            both_complete_loaders_fit_common_cap=True,
            complete_native_forward_and_literal_reverse_scanned=True,
            all_output_argument_copies_full_native_wires_and_72bit_SSA_charged=True,
            actual_native_wrapper_and_literal_inverse_reexecuted_independently=True,
            every_allocated_wire_and_fixed_lane_mask_matches_producer=True,
            component_AS241_adopted_under_strict_T_rule=adopted,
            losing_resource_rows_retained=True,
            financial_source_adopted=False,
            full_G2_established=False,
            quantum_advantage_claim=False,
            financial_source_cost_divided_by_coordinate_count=False,
            numerical_threads=1,
            JIT_disk_cache=False,
            audited_helper_imports=0,
            independent_process_CPU_seconds_before_bulk_hashes=cpu,
            independent_wall_seconds_before_bulk_hashes=wall,
        )
        seal(output, frozen, summary, started)
    except BaseException as failure:
        preserve_failure(output, frozen, failure, "run", started)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    (prepare if arguments.operation == "prepare" else run)(arguments.output)
