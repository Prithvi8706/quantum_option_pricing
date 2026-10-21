"""Prospective two real AS241 scalar invocations versus one original BM pair."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import traceback
import xml.etree.ElementTree as ET

from research.limitation_program_20261001.two_draw_loader_source_v2 import (
    ADMISSION,
    CAP,
    CPU,
    DIRTY,
    LABELS,
    LANES,
    LANE_MASK,
    PAIRS,
    WALL,
    Budget,
    BudgetCensoredError,
    apply_wrapper,
    canonical,
    derive_wrappers,
    fixture_row,
    initial_state,
    make_engine,
    phase_premise,
    read,
    require,
    resource_row,
    scan_leaves,
)

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
RECEIPT = PROGRAM / "A02_two_draw_loader_resource_run002"
INTERPRETER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
PREFLIGHT = RESEARCH / "two_draw_loader_implementation_preflight_v2.json"
PLAN = RESEARCH / "two_draw_loader_resource_preflight.json"
CODE = (
    "two_draw_loader_source_v2.py",
    "experiment_two_draw_loader_resource_v2.py",
    "test_two_draw_loader_source_v2.py",
    "audit_two_draw_loader_resource_v2.py",
)
DOCS = (
    "TWO_DRAW_LOADER_IMPLEMENTATION_PREFLIGHT_V2.md",
    "two_draw_loader_implementation_preflight_v2.json",
    "TWO_DRAW_LOADER_RESOURCE_PREFLIGHT.md",
    "two_draw_loader_resource_preflight.json",
)
TESTS = 32
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
TOOL_DIRECTORIES = (
    "numpy",
    "numpy.libs",
    "numba",
    "llvmlite",
    "llvmlite.libs",
    "pytest",
    "_pytest",
    "pluggy",
    "packaging",
    "iniconfig",
    "colorama",
    "pygments",
    "scipy",
    "scipy.libs",
    "numba_cuda",
    "numba_cuda.libs",
)
_PATHS = {}
_ACTUAL_HASHES = {}
_VERIFIED_ACTUAL_PATHS = {}
_BOOKKEEPING_BUDGET = None
ORIGINAL_FAILURE_MANIFEST_SHA = "b2911a9d8d1c961f75f6f8a2418ed8d0d04e8011ea869b1c5006279f03cc4bdd"
ORIGINAL_REVIEW_MANIFEST_SHA = "eaef4d44c1f8241241a11f0e7406232d8cdd564d586fd7d71bdba27f6140749c"
ORIGINAL_AUTHOR_SHA = {
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


def reset_bookkeeping(budget=None):
    global _BOOKKEEPING_BUDGET
    _PATHS.clear()
    _ACTUAL_HASHES.clear()
    _VERIFIED_ACTUAL_PATHS.clear()
    _BOOKKEEPING_BUDGET = budget


def resolved(path, fresh=False, confined=True):
    if _BOOKKEEPING_BUDGET is not None:
        _BOOKKEEPING_BUDGET.check()
    path = Path(path)
    require(not path.drive or path.is_absolute(), "No ambiguous drive-relative actual path")
    lexical = str(path.absolute())
    prior = _PATHS.get(lexical)
    if prior is not None and not fresh:
        actual = prior[0]
    else:
        actual = path.resolve()
        require(prior is None or prior[0] == actual, "Previously resolved actual path changed")
    if confined:
        actual.relative_to(ROOT)
    _PATHS[lexical] = (actual, confined or (prior is not None and prior[1]))
    if _BOOKKEEPING_BUDGET is not None:
        _BOOKKEEPING_BUDGET.check()
    return actual


def stat_identity(value):
    return (
        value.st_dev,
        value.st_ino,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
        getattr(value, "st_file_attributes", None),
    )


def save(path, value, budget=None):
    if budget is not None:
        budget.check()
    content = (json.dumps(value, indent=2, allow_nan=False) + "\n").encode()
    if budget is not None:
        budget.check()
    with Path(path).open("xb") as stream:
        for start in range(0, len(content), 1 << 20):
            if budget is not None:
                budget.check()
            stream.write(content[start : start + (1 << 20)])
            if budget is not None:
                budget.check()


def sha(path, budget, fresh=False):
    budget.check()
    path = resolved(path, fresh=fresh, confined=False)
    if not path.is_relative_to(ROOT):
        base = resolved(
            getattr(sys, "_base_executable", sys.executable), fresh=fresh, confined=False
        )
        require(
            path == base and not base.is_relative_to(ROOT),
            "Only the explicitly scoped actual base interpreter may be external",
        )
    identity = str(path)
    before = stat_identity(path.stat())
    prior = _ACTUAL_HASHES.get(identity)
    if not fresh and prior is not None and prior[0] == before:
        budget.check()
        return prior[1]
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while True:
            budget.check()
            block = stream.read(1 << 20)
            if not block:
                break
            digest.update(block)
            budget.check()
    after = stat_identity(path.stat())
    require(before == after, "Actual file metadata changed during full SHA read")
    actual = digest.hexdigest()
    require(
        identity not in _VERIFIED_ACTUAL_PATHS or _VERIFIED_ACTUAL_PATHS[identity] == actual,
        "Previously verified actual bytes changed within this invocation",
    )
    _ACTUAL_HASHES[identity] = (after, actual)
    _VERIFIED_ACTUAL_PATHS[identity] = actual
    budget.check()
    return actual


def final_fresh_bookkeeping(budget):
    """Every observed alias is resolved fresh; every actual byte is rehashed without reuse."""
    for lexical, (previous, confined) in tuple(_PATHS.items()):
        budget.check()
        require(
            resolved(lexical, fresh=True, confined=confined) == previous,
            "Fresh final actual path confinement/resolution agrees",
        )
    for name, expected_actual in tuple(_VERIFIED_ACTUAL_PATHS.items()):
        budget.check()
        require(
            sha(name, budget, fresh=True) == expected_actual,
            "Final full actual SHA agrees with its observed bytes",
        )
    budget.check()


def relative(path):
    return resolved(path).relative_to(ROOT).as_posix()


def bind(frozen, name, expected, base=ROOT):
    path = Path(str(name).replace("\\", "/"))
    require(not path.drive or path.is_absolute(), "No ambiguous drive-relative origin")
    path = resolved(path if path.is_absolute() else base / path)
    normalized = relative(path)
    require(
        type(expected) is str
        and len(expected) == 64
        and all(c in "0123456789abcdef" for c in expected),
        "Explicit canonical expected SHA256",
    )
    require(
        normalized not in frozen or frozen[normalized] == expected,
        "No original expected-SHA overwrite: " + normalized,
    )
    frozen[normalized] = expected


def verify(frozen, budget):
    for name, expected in frozen.items():
        budget.check()
        path = resolved(ROOT / name)
        require(sha(path, budget) == expected, "Frozen original/source/tool input changed: " + name)


def maps(path):
    record = read(path)
    require(type(record) is dict and record, "Nonempty original manifest")
    if all(
        type(value) is str and len(value) == 64 and all(c in "0123456789abcdef" for c in value)
        for value in record.values()
    ):
        return record, [(record, path.parent, "flat")]
    require(
        type(record.get("files")) is dict and type(record.get("frozen_inputs", {})) is dict,
        "Canonical complete original file/input maps",
    )
    if "historical_receipts_unchanged" in record:
        require(record["historical_receipts_unchanged"] is True, "Exact original historical marker")
    if "manifest_self_hash_excluded" in record:
        require(
            record["manifest_self_hash_excluded"] is True,
            "Exact original manifest self-hash exclusion",
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
    require(set(record) <= allowed, "Unknown historical manifest marker cannot be waived")
    return record, [
        (record["files"], ROOT, "files"),
        (record.get("frozen_inputs", {}), ROOT, "frozen_inputs"),
    ]


def archived_origin(path, expected, manifest, owned, budget):
    """Only exact owned snapshots or explicit recorded reconciliation references."""
    normalized = relative(path)
    for candidate, saved_sha in owned.items():
        budget.check()
        if saved_sha == expected and Path(candidate).name == path.name:
            archived = ROOT / candidate
            require(sha(archived, budget) == expected, "Exact original owned snapshot bytes")
            return archived, "same-owner archived snapshot with same basename and exact SHA"
    reconciliation = PROGRAM / "A01_drift_run001/reconciliation.json"
    for row in read(reconciliation)["rows"]:
        budget.check()
        if row["path"] != normalized or row["expected_old_sha256"] != expected:
            continue
        references = [
            r
            for r in row["references"]
            if r["receipt"] == manifest.parent.name
            and r["expected_sha256"] == expected
            and r["manifest_sha256"] == sha(manifest, budget)
        ]
        require(
            len(references) == 1
            and row["historical_old_bytes_recovered"] is True
            and row["expected_hash_waived"] is False,
            "Explicit original owner/expected-SHA archived reference",
        )
        archived = resolved(ROOT / row["recovered_snapshot_path"])
        archived.relative_to(resolved(reconciliation.parent))
        require(
            row["recovered_snapshot_sha256"] == expected and sha(archived, budget) == expected,
            "Explicit recovered original bytes",
        )
        return archived, "explicit A01_drift original-owner reconciliation"
    raise ValueError("No exact archived original for changed prerequisite: " + normalized)


def receipt(
    name, frozen, origins, budget, expected_manifest=None, dependencies=True, allow_archived=True
):
    directory = PROGRAM / name
    manifest = directory / "manifest.json"
    actual = sha(manifest, budget)
    require(
        expected_manifest is None or actual == expected_manifest,
        "Pinned original manifest: " + name,
    )
    _, records = maps(manifest)
    owned = {}
    for mapping, base, _ in records:
        for key, expected in mapping.items():
            budget.check()
            path = Path(str(key).replace("\\", "/"))
            path = resolved(path if path.is_absolute() else base / path)
            if path.is_relative_to(resolved(directory)):
                bind(owned, path, expected)
    for mapping, base, field in records:
        for key, expected in mapping.items():
            budget.check()
            path = Path(str(key).replace("\\", "/"))
            path = resolved(path if path.is_absolute() else base / path)
            if not dependencies and not path.is_relative_to(resolved(directory)):
                continue
            origin, route = path, "current original expected bytes"
            if sha(path, budget) != expected:
                require(allow_archived, "Required active original bytes changed: " + relative(path))
                require(
                    not path.is_relative_to(resolved(directory)),
                    "Original owned packet bytes changed",
                )
                origin, route = archived_origin(path, expected, manifest, owned, budget)
            bind(frozen, origin, expected)
            origins.append(
                dict(
                    owner_manifest=relative(manifest),
                    source_map=field,
                    original_path=relative(path),
                    expected_sha256=expected,
                    verified_input_path=relative(origin),
                    route=route,
                    legitimate_expected_hash_waived=False,
                )
            )
    bind(frozen, manifest, actual)
    summary = read(directory / "summary.json")
    return summary


def tools(frozen, budget):
    require(
        resolved(sys.executable) == resolved(INTERPRETER),
        "Pinned accepted scalar scanner interpreter",
    )
    for name, expected in PACKAGES.items():
        budget.check()
        require(
            importlib.metadata.version(name) == expected,
            "Unchanged existing package version: " + name,
        )
    bind(frozen, INTERPRETER, sha(INTERPRETER, budget))
    base = resolved(getattr(sys, "_base_executable", sys.executable), confined=False)
    base_sha = sha(base, budget)
    record = dict(
        launcher_workspace_relative=relative(INTERPRETER),
        launcher_sha256=sha(INTERPRETER, budget),
        base_interpreter=dict(
            absolute_path=str(base),
            sha256=base_sha,
            included_in_workspace_frozen_map=base.is_relative_to(ROOT),
        ),
    )
    if record["base_interpreter"]["included_in_workspace_frozen_map"]:
        bind(frozen, base, base_sha)
    site = INTERPRETER.parent.parent / "Lib/site-packages"
    record["installed_tool_dependency_versions"] = {
        name: importlib.metadata.version(name) for name in TOOL_DEPENDENCIES
    }
    for package in TOOL_DIRECTORIES:
        directory = site / package
        require(
            directory.is_dir() or package.endswith(".libs"), "Existing package origin: " + package
        )
        if directory.is_dir():
            for path in sorted(directory.rglob("*")):
                budget.check()
                if path.is_file():
                    bind(frozen, path, sha(path, budget))
    for name in (*PACKAGES, *TOOL_DEPENDENCIES):
        budget.check()
        distribution = importlib.metadata.distribution(name)
        entries = distribution.files
        require(entries is not None and len(entries) > 0, "Complete installed metadata inventory")
        metadata_roots = set()
        for entry in entries:
            budget.check()
            if ".dist-info/" in str(entry).replace("\\", "/"):
                path = resolved(distribution.locate_file(entry))
                roots = [parent for parent in path.parents if parent.name.endswith(".dist-info")]
                require(
                    len(roots) == 1 and roots[0].parent == resolved(site),
                    "One confined installed distribution metadata root",
                )
                metadata_roots.add(roots[0])
        require(
            len(metadata_roots) == 1, "Exactly one actual installed distribution metadata directory"
        )
        for path in sorted(next(iter(metadata_roots)).rglob("*")):
            budget.check()
            if path.is_file():
                bind(frozen, path, sha(path, budget))
    for module in (
        sys.modules[__name__],
        sys.modules["research.limitation_program_20261001.two_draw_loader_source_v2"],
    ):
        budget.check()
        cached = getattr(module, "__cached__", None)
        if cached and Path(cached).is_file():
            bind(frozen, cached, sha(cached, budget))
    for name in CODE:
        budget.check()
        cached = Path(importlib.util.cache_from_source(str(RESEARCH / name)))
        if cached.is_file():
            bind(frozen, cached, sha(cached, budget))
    record["scanner_packages"] = PACKAGES
    return record


def verify_tools(protocol, budget):
    expected = protocol["interpreter_binding"]
    require(
        relative(Path(sys.executable)) == expected["launcher_workspace_relative"]
        and sha(Path(sys.executable), budget) == expected["launcher_sha256"],
        "Actual bound launcher",
    )
    base = resolved(getattr(sys, "_base_executable", sys.executable), confined=False)
    require(
        str(base) == expected["base_interpreter"]["absolute_path"]
        and sha(base, budget) == expected["base_interpreter"]["sha256"],
        "Actual base interpreter bytes",
    )
    for name, version in PACKAGES.items():
        budget.check()
        require(importlib.metadata.version(name) == version, "Pinned numerical version")
    require(
        set(expected["installed_tool_dependency_versions"]) == set(TOOL_DEPENDENCIES),
        "Exactly the frozen installed scientific and fixture dependencies",
    )
    for name, version in expected["installed_tool_dependency_versions"].items():
        budget.check()
        require(
            importlib.metadata.version(name) == version, "Bound installed tool dependency version"
        )


def verify_loaded_tool_modules(frozen, budget):
    prefixes = {name for name in TOOL_DIRECTORIES if not name.endswith(".libs")}
    prefixes.add("research.limitation_program_20261001.two_draw_loader_source_v2")
    for name, module in tuple(sys.modules.items()):
        if (
            name.split(".")[0] not in prefixes
            and name not in prefixes
            and module is not sys.modules[__name__]
        ):
            continue
        budget.check()
        source = getattr(module, "__file__", None)
        cached = getattr(module, "__cached__", None)
        for path in (source, cached):
            if path and Path(path).is_file():
                key = relative(path)
                require(
                    key in frozen and sha(path, budget) == frozen[key],
                    "Every actual imported tool source or bytecode origin was frozen: " + key,
                )


def finish(output, frozen, budget, summary):
    verify(frozen, budget)
    save(output / "summary.json", summary, budget)
    files = {
        relative(path): sha(path, budget) for path in sorted(output.rglob("*")) if path.is_file()
    }
    verify(frozen, budget)
    final_fresh_bookkeeping(budget)
    cpu, wall = budget.check()
    save(
        output / "manifest.json",
        dict(
            files=files,
            frozen_inputs=frozen,
            manifest_self_hash_excluded=True,
            all_inputs_and_bulk_hashes_verified_before_terminal=True,
            process_CPU_seconds_before_terminal=cpu,
            wall_seconds_before_terminal=wall,
            every_verified_actual_path_freshly_resolved_and_fully_rehashed=True,
            invocation_local_actual_hash_cache_never_substitutes_expected_hashes=True,
        ),
        budget,
    )


def failure(output, frozen, budget, exception, phase):
    if not output.exists():
        return
    try:
        budget.check()
        save(
            output / (phase + "_failure.json"),
            dict(
                failure_type=type(exception).__name__,
                message=str(exception),
                traceback=traceback.format_exc(),
                partial_files_preserved=True,
                no_retry=True,
            ),
            budget,
        )
        terminal = output / (
            "completion_outcome.json" if (output / "summary.json").exists() else "summary.json"
        )
        save(
            terminal,
            dict(
                passed=False,
                local_only=True,
                budget_censored=isinstance(exception, (BudgetCensoredError, TimeoutError)),
                new_test_credit=0,
                fixed_receipt_terminal_no_retry=True,
                partial_files_preserved=True,
            ),
            budget,
        )
        require(
            not (output / "manifest.json").exists(),
            "Failure cannot replace an existing or partial manifest",
        )
        verification_error = None
        try:
            verify(frozen, budget)
        except BudgetCensoredError:
            raise
        except BaseException as changed:
            verification_error = str(changed)
        files = {
            relative(path): sha(path, budget)
            for path in sorted(output.rglob("*"))
            if path.is_file()
        }
        final_fresh_bookkeeping(budget)
        save(
            output / "manifest.json",
            dict(
                files=files,
                frozen_inputs=frozen,
                manifest_self_hash_excluded=True,
                terminal_record=relative(terminal),
                failure_inputs_verified=verification_error is None,
                verification_error=verification_error,
                failed_fixture_credit=0,
            ),
            budget,
        )
    except BaseException as sealing:
        marker = output / "failed_unsealed.json"
        if not marker.exists():
            save(
                marker,
                dict(
                    passed=False,
                    local_only=True,
                    receipt_unsealed=True,
                    new_test_credit=0,
                    original_failure_type=type(exception).__name__,
                    failure_retention_error=str(sealing),
                    budget_censored=isinstance(exception, (BudgetCensoredError, TimeoutError))
                    or isinstance(sealing, BudgetCensoredError),
                    overrides_any_intermediate_success=True,
                    no_more_hashing_or_retry=True,
                ),
            )


def prepare(output):
    reset_bookkeeping()
    output = resolved(output)
    require(
        output == resolved(RECEIPT) and not output.exists(),
        "Fresh exclusive paired component receipt",
    )
    frozen, origins, budget = {}, [], Budget()
    reset_bookkeeping(budget)
    try:
        require(
            sys.dont_write_bytecode is True, "Interpreter starts with bytecode writes disabled (-B)"
        )
        preflight, plan = read(PREFLIGHT), read(PLAN)
        require(
            preflight["fixed_fixture_count"] == TESTS
            and preflight["logical_qubit_cap"] == CAP
            and preflight["process_CPU_seconds"] == CPU
            and preflight["admission_CPU_seconds"] == ADMISSION
            and preflight["wall_seconds"] == WALL
            and preflight["fixed_labels"] == list(LABELS)
            and canonical(preflight["input_pairs"]) == canonical([list(pair) for pair in PAIRS])
            and canonical(preflight["dirty_outputs_each72"]) == canonical(list(DIRTY)),
            "Fixed unchanged paired method/fixtures/budget",
        )
        require(
            preflight["original_admission_failure_manifest_sha256"] == ORIGINAL_FAILURE_MANIFEST_SHA
            and preflight["original_root_review_manifest_sha256"] == ORIGINAL_REVIEW_MANIFEST_SHA
            and canonical(preflight["original_author_sha256"]) == canonical(ORIGINAL_AUTHOR_SHA),
            "Original failed admission and all frozen source pins are immutable",
        )
        require(
            not (PROGRAM / "A02_two_draw_loader_resource_run001").exists(),
            "Original pre-mkdir failed intended receipt remains absent; no fabricated protocol",
        )
        for name, expected in ORIGINAL_AUTHOR_SHA.items():
            budget.check()
            bind(frozen, RESEARCH / name, expected)
        review = receipt(
            "A02_two_draw_root_review_run001",
            frozen,
            origins,
            budget,
            ORIGINAL_REVIEW_MANIFEST_SHA,
            allow_archived=False,
        )
        require(
            review["root_and_peer_static_review_passed"] is True
            and review["no_actual_numeric_cost_replay_or_fixture_result_claim"] is True
            and canonical(review["reviewed_source_sha256"]) == canonical(ORIGINAL_AUTHOR_SHA),
            "Preserved original root static review, no fabricated numerical result",
        )
        admission_failure = receipt(
            "A02_two_draw_loader_admission_failure_run001",
            frozen,
            origins,
            budget,
            ORIGINAL_FAILURE_MANIFEST_SHA,
            allow_archived=False,
        )
        require(
            admission_failure["passed"] is False
            and admission_failure["new_test_credit"] == 0
            and admission_failure["failed_intended_receipt_absent"] is True
            and admission_failure["failed_intended_receipt"]
            == "A02_two_draw_loader_resource_run001"
            and admission_failure["protocol_or_array_or_cost_or_replay_or_fixture_execution"]
            is False
            and canonical(admission_failure["fixed_CPU_hard_admission_wall_seconds"])
            == canonical([CPU, ADMISSION, WALL]),
            "Original operational failure is zero credit and has no numerical execution",
        )
        for row in plan["author_readonly_input_bindings"]:
            budget.check()
            bind(frozen, row["path"], row["author_readonly_sha256"])
        archive = receipt(
            "A01_drift_run001",
            frozen,
            origins,
            budget,
            preflight["archive_reconciliation_manifest_sha256"],
        )
        require(archive["passed"] is True, "Immutable explicit archive owner receipt")
        pinned = {
            Path(row["path"]).parent.name: row["author_readonly_sha256"]
            for row in plan["author_readonly_input_bindings"]
            if row["path"].endswith("/manifest.json")
        }
        for name in (
            "A02_quantile_scalar_run001",
            "A02_quantile_scalar_audit_run001",
            "C06_pair_run001",
            "C06_pair_audit_run001",
            "A10_coefficient_run001",
        ):
            summary = receipt(name, frozen, origins, budget, pinned[name])
            require(
                summary["passed"] is True and not summary.get("budget_censored", False),
                "Accepted uncensored source: " + name,
            )
        for row in (
            plan["AS241_wrapper"]["actual_leaf_inventory"]
            + plan["BoxMuller_wrapper"]["actual_leaf_inventory"]
        ):
            budget.check()
            require(
                frozen.get(relative(ROOT / row["metadata"])) == row["metadata_sha256"]
                and frozen.get(relative(ROOT / row["native_gate_file"]))
                == row["native_gate_sha256_from_archived_metadata"],
                "Selected actual native bytes have original manifest membership",
            )
        failed = receipt(
            "WAVE10_run001",
            frozen,
            origins,
            budget,
            preflight["failed_WAVE10_run001_manifest_sha256"],
            allow_archived=False,
        )
        require(
            failed["passed"] is False
            and failed["budget_censored"] is True
            and failed["new_test_credit"] == 0,
            "Original censored W10 retained at zero credit",
        )
        wave = receipt("WAVE10_run002", frozen, origins, budget, dependencies=False)
        require(
            wave["passed"] is True
            and wave["archived_or_current_integrity_passed"] is True
            and wave["global_live_integrity"] is False
            and wave["legitimate_expected_hashes_waived"] is False,
            "Successful exact archived/current W10run002 release with original expectations",
        )
        require(
            read(PROGRAM / "WAVE10_run002/progress_snapshot.json")["static_author_preflights"][
                "dependency_order"
            ]
            == preflight["fixed18_selected_labels"],
            "Exact selected005 fixed18 snapshot",
        )
        for path in (
            RESEARCH / "temporary_and_fulladder.py",
            PROGRAM / "A17_quantile_divider_run001/exact_CCX_phase_proof.json",
        ):
            budget.check()
            require(
                relative(path) in frozen and sha(path, budget) == frozen[relative(path)],
                "Directly read phase premise has strict active original binding",
            )
        interpreter = tools(frozen, budget)
        for name in CODE + DOCS:
            budget.check()
            bind(frozen, RESEARCH / name, sha(RESEARCH / name, budget))
        verify(frozen, budget)
        budget.check(admission=True)
        output.mkdir()
        for name in CODE + DOCS:
            budget.check()
            shutil.copy2(RESEARCH / name, output / name)
            require(
                sha(output / name, budget) == frozen[relative(RESEARCH / name)],
                "Exact reviewed source copy",
            )
            bind(frozen, output / name, frozen[relative(RESEARCH / name)])
        save(
            output / "dependency_origins.json",
            dict(rows=origins, original_expected_hashes_never_overwritten=True),
            budget,
        )
        bind(
            frozen,
            output / "dependency_origins.json",
            sha(output / "dependency_origins.json", budget),
        )
        verify(frozen, budget)
        final_fresh_bookkeeping(budget)
        save(
            output / "protocol.json",
            dict(
                schema="two-actual-draw-native-component-protocol-v1",
                created_utc=datetime.now(timezone.utc).isoformat(),
                local_only=True,
                frozen_before_closure_arrays_costs_replays_tests=True,
                frozen_inputs=frozen,
                interpreter_binding=interpreter,
                fixed_labels=list(LABELS),
                declared_unique_tests=TESTS,
                fixed_input_pairs=[list(pair) for pair in PAIRS],
                dirty_outputs_each72=list(DIRTY),
                packed_lanes_per_loader=LANES,
                packed_lane_mask=LANE_MASK,
                native_input_bits=144,
                uniform_preparation_H_separate=64,
                dirty_output_bits=144,
                native_width=72,
                fraction_bits=40,
                logical_qubit_cap=CAP,
                process_CPU_seconds=CPU,
                admission_CPU_seconds=ADMISSION,
                wall_seconds=WALL,
                numerical_threads=1,
                JIT_disk_cache=False,
                bytecode_writes_disabled=True,
                existing_package_bytecode_and_distribution_metadata_bound=True,
                exact7T_phase_proof_separate_from_basis_fixtures=True,
                full_array_chunk_gate_rows=65536,
                historical_fixture_credit_added_again=0,
                original_failed_admission_credit=0,
                invocation_local_canonical_path_and_stat_actualSHA_bookkeeping_cache=True,
                cache_contains_observed_actual_hashes_never_caller_expected_hashes=True,
                all_verified_actual_paths_freshly_resolved_and_fully_rehashed_before_protocol=True,
                failed_WAVE10_run001_credit=0,
                required_release_packet="WAVE10_run002",
                requires_root_C8_and_timing_exclusive_clearance=True,
                full_financial_sampler_adoption=False,
                full_G2=False,
                advantage_established=False,
                all_110_obligations_retained=True,
            ),
            budget,
        )
        verify(frozen, budget)
        budget.check()
    except BaseException as exception:
        failure(output, frozen, budget, exception, "prepare")
        raise


def run(output):
    reset_bookkeeping()
    output = resolved(output)
    require(
        output == resolved(RECEIPT)
        and not any(
            (output / name).exists()
            for name in ("summary.json", "run_started.json", "failed_unsealed.json")
        ),
        "Prepared receipt cannot retry",
    )
    protocol = read(output / "protocol.json")
    frozen, budget = protocol["frozen_inputs"], Budget()
    reset_bookkeeping(budget)
    try:
        require(
            sys.dont_write_bytecode is True, "Interpreter starts with bytecode writes disabled (-B)"
        )
        for key in (
            "OPENBLAS_NUM_THREADS",
            "MKL_NUM_THREADS",
            "OMP_NUM_THREADS",
            "NUMBA_NUM_THREADS",
            "NUMEXPR_NUM_THREADS",
        ):
            os.environ[key] = "1"
        os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        verify(frozen, budget)
        verify_tools(protocol, budget)
        save(
            output / "run_started.json",
            dict(fixed_receipt_no_retry=True, two_fixed_rows_only=True),
            budget,
        )
        budget.check(admission=True)
        save(output / "exact_CCX_phase_premise.json", phase_premise(ROOT), budget)
        wrappers, targets = derive_wrappers(read(PLAN), ROOT, budget.check)
        save(output / "wrappers.json", wrappers, budget)
        save(output / "selected_original_targets.json", targets, budget)
        engine = make_engine()
        budget.check()
        np = engine[0]
        verify_loaded_tool_modules(frozen, budget)
        for name in PACKAGES:
            module = sys.modules[name]
            path = resolved(module.__file__)
            require(
                relative(path) in frozen and sha(path, budget) == frozen[relative(path)],
                "Actual lazily imported package origin",
            )
        ledger, evidence = {}, []
        literals = read(PROGRAM / "A02_quantile_scalar_run001/literals.json")
        for label in LABELS:
            budget.check(admission=True)
            wrapper = wrappers[label]
            leaves, loaded = scan_leaves(wrapper, ROOT, engine, budget.check)
            ledger[label] = resource_row(wrapper, leaves)
            save(output / (label + "_native_resource_row.json"), ledger[label], budget)
            budget.check(admission=True)
            state = initial_state(wrapper, np)
            before = state.copy()
            np.save(output / (label + "_before.npy"), before, allow_pickle=False)
            apply_wrapper(wrapper, state, loaded, engine, budget.check)
            after = state.copy()
            np.save(output / (label + "_after.npy"), after, allow_pickle=False)
            apply_wrapper(wrapper, state, loaded, engine, budget.check, inverse=True)
            np.save(output / (label + "_restored.npy"), state, allow_pickle=False)
            for pair_index in range(len(PAIRS)):
                for dirty_index in range(len(DIRTY)):
                    budget.check()
                    evidence.append(
                        fixture_row(
                            wrapper,
                            targets[label],
                            literals,
                            before,
                            after,
                            state,
                            pair_index,
                            dirty_index,
                        )
                    )
        save(output / "native_resource_ledger.json", ledger, budget)
        save(
            output / "actual_gate_replays.json",
            dict(
                completed_replays=len(evidence),
                rows=evidence,
                fixed_basis_diagnostics_not_all_input_or_phase_proof=True,
                old_fixture_recredit=0,
            ),
            budget,
        )
        budget.check(admission=True)
        import pytest

        os.environ["TWO_DRAW_LOADER_SOURCE"] = str(output)
        code = pytest.main(
            [
                str(output / "test_two_draw_loader_source_v2.py"),
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml=" + str(output / "tests.xml"),
            ]
        )
        budget.check()
        verify_loaded_tool_modules(frozen, budget)
        cases = list(ET.parse(output / "tests.xml").getroot().iter("testcase"))
        identities = [[case.attrib.get("classname", ""), case.attrib["name"]] for case in cases]
        require(
            code == 0
            and len(cases) == len({tuple(row) for row in identities}) == TESTS
            and not any(
                case.find(tag) is not None
                for case in cases
                for tag in ("failure", "error", "skipped")
            ),
            "Exactly32 successful distinct actual full-state fixtures",
        )
        save(
            output / "test_credit_reconciliation.json",
            dict(
                unique_new_fixtures_passed=TESTS,
                prior_fixture_counts_added_again=0,
                test_identities=identities,
            ),
            budget,
        )
        require(
            len(evidence) == TESTS
            and all(ledger[label]["clean_resources"]["logical_qubits"] <= CAP for label in LABELS),
            "Both entire matched ABI loaders validated under common cap",
        )
        as_cost, bm_cost = (ledger[label]["clean_resources"]["t_count"] for label in LABELS)
        decision = dict(
            AS241_component_strict_T_improvement=as_cost < bm_cost,
            AS241_component_eligible_pending_independent_audit=as_cost < bm_cost,
            paired_AS241_component_adopted=False,
            independent_resource_audit_still_required=True,
            both_losing_or_winning_resource_rows_preserved=True,
            comparison_unit=(
                "two actual AS241 scalar invocations versus one actual unchanged shared BM pair"
            ),
            financial_source_cost_divided_by_coordinate_count=False,
            complete_financial_sampler_or_estimator_adopted=False,
        )
        save(output / "paired_component_decision.json", decision, budget)
        verify_tools(protocol, budget)
        finish(
            output,
            frozen,
            budget,
            dict(
                passed=True,
                local_only=True,
                budget_censored=False,
                fixed_receipt_terminal_no_retry=True,
                tests_completed=TESTS,
                new_test_credit=TESTS,
                new_unique_fixtures_passed=TESTS,
                old_fixture_recredit=0,
                completed_actual_basis_fixtures=TESTS,
                actual_loader_rows=2,
                both_complete_dirty72_clean_ABI_validated=True,
                all_full72_banks_argument_copies_high_scratch_and_literal_inverse_paid=True,
                initial_Hadamards_separate=64,
                logical_qubit_cap=CAP,
                paired_component_decision=decision,
                full_financial_sampler_or_estimator_adopted=False,
                full_financial_native_cost=None,
                physical_runtime=None,
                full_G2=False,
                quantum_advantage_established=False,
                all_110_obligations_retained=True,
            ),
        )
    except BaseException as exception:
        failure(output, frozen, budget, exception, "run")
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    (prepare if args.phase == "prepare" else run)(args.output)


if __name__ == "__main__":
    main()
