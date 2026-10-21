"""Freeze one structural MPS toy before q10 tables, candidates or synthesis.

This receipt must use the existing controlled_closeout_repro interpreter and
must not run until root clears Stage C timing exclusivity. Numeric comparisons
validate wiring and implementation; they are not Gaussian error certificates.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import pytest  # noqa: E402

from research.limitation_program_20261001.mps_sequential_structure import (  # noqa: E402
    require_pinned_sdk,
)

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
RESEARCH = ROOT / "research/limitation_program_20261001"
ENVIRONMENT = ROOT / ".context/controlled_closeout_repro"
INTERPRETER = ENVIRONMENT / "Scripts/python.exe"
SITE_PACKAGES = ENVIRONMENT / "Lib/site-packages"
TESTS = 16
CPU_LIMIT = 120
WALL_LIMIT = 300
CODE = (
    "mps_sequential_structure.py",
    "test_mps_sequential_structure.py",
    "experiment_mps_structure.py",
    "mps_structure_preflight.json",
    "mps_loader_preflight.json",
)
# Literal package roots, never an inventory of the entire workspace/.context.
TOOL_PACKAGE_ROOTS = (
    "numpy",
    "numpy.libs",
    "qiskit",
    "scipy",
    "scipy.libs",
    "pytest",
    "_pytest",
    "mpmath",
    "sympy",
    "symengine",
    "rustworkx",
    "stevedore",
    "dill",
    "ply",
    "dateutil",
    "packaging",
    "pluggy",
    "iniconfig",
    "colorama",
    "psutil",
    "numpy-1.26.4.dist-info",
    "qiskit_terra-0.45.3.dist-info",
)
REQUIRED_PACKAGE_ROOTS = ("numpy", "qiskit", "scipy", "pytest", "_pytest")
MAXIMUM_TOOL_FILES = 16384


class BudgetCensoredError(RuntimeError):
    """A fixed execution-budget stop, separate from a verification failure."""


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def create(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def verify(frozen):
    for name, expected in frozen.items():
        path = (ROOT / name.replace("\\", "/")).resolve()
        path.relative_to(ROOT.resolve())
        if sha(path) != expected:
            raise ValueError("Frozen structural dependency changed: " + name)


def bind_frozen(frozen, name, expected):
    path = (ROOT / str(name).replace("\\", "/")).resolve()
    path.relative_to(ROOT.resolve())
    normalized = relative(path)
    if not (
        isinstance(expected, str)
        and len(expected) == 64
        and all(char in "0123456789abcdef" for char in expected)
    ):
        raise ValueError("Explicit canonical SHA256 dependency expected")
    if normalized in frozen and frozen[normalized] != expected:
        raise ValueError("Existing frozen MPS dependency expectation conflicts: " + normalized)
    frozen[normalized] = expected


def pinned_interpreter():
    if Path(sys.executable).resolve() != INTERPRETER.resolve():
        raise RuntimeError("Use the existing controlled_closeout_repro interpreter only")
    require_pinned_sdk()


def tool_paths():
    for name in REQUIRED_PACKAGE_ROOTS:
        if not (SITE_PACKAGES / name).is_dir():
            raise FileNotFoundError("Required existing tool package missing: " + name)
    paths = {INTERPRETER}
    for name in TOOL_PACKAGE_ROOTS:
        directory = SITE_PACKAGES / name
        if directory.is_dir():
            for path in directory.rglob("*"):
                if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                    paths.add(path)
                    if len(paths) > MAXIMUM_TOOL_FILES:
                        raise RuntimeError("Fixed tool-package inventory bound exceeded")
    for name in ("six.py", "typing_extensions.py"):
        path = SITE_PACKAGES / name
        if path.is_file():
            paths.add(path)
    return sorted(paths)


def prepare(output):
    pinned_interpreter()
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    if output.exists():
        raise FileExistsError("Fresh structural receipt required")
    preflight = read(RESEARCH / "mps_structure_preflight.json")
    assert preflight["fixed_nonfinancial_emitted_toys"] == 1
    assert preflight["maximum_local_SDK_decompositions"] == 3
    assert preflight["unique_fixture_count"] == TESTS
    paths = tool_paths() + [RESEARCH / name for name in CODE]
    frozen = {}
    for path in paths:
        bind_frozen(frozen, path, sha(path))
    verify(frozen)
    output.mkdir()
    try:
        prepare_receipt(output, paths, frozen)
    except BaseException as failure:
        create(
            output / "preparation_failure.json",
            {
                "failure_type": type(failure).__name__,
                "message": str(failure),
                "traceback": traceback.format_exc(),
                "partial_files_preserved": True,
                "fixed_receipt_terminal_no_retry": True,
            },
        )
        create(
            output / "summary.json",
            {
                "passed": False,
                "local_only": True,
                "preparation_failed": True,
                "budget_censored": isinstance(failure, (BudgetCensoredError, TimeoutError)),
                "partial_files_preserved": True,
                "fixed_receipt_terminal_no_retry": True,
                "new_q10_candidates_or_synthesis_calls": 0,
                "full_q10_preparation_error_or_T_cost": None,
                "financial_sampler_changed": False,
                "quantum_advantage_claim": False,
            },
        )
        finish_manifest(output, {"frozen_inputs": frozen})
        raise


def prepare_receipt(output, paths, frozen):
    for name in CODE:
        shutil.copy2(RESEARCH / name, output / name)
        if sha(output / name) != frozen[relative(RESEARCH / name)]:
            raise ValueError("Frozen structural code snapshot differs: " + name)
    verify(frozen)
    create(
        output / "protocol.json",
        {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "local_only": True,
            "before_tests_local_unitaries_or_SDK_decompositions": True,
            "requires_root_Stage_C_timing_idle_clearance": True,
            "frozen_inputs": frozen,
            "executed_dependencies": [
                {
                    "original": relative(RESEARCH / name),
                    "snapshot": name,
                    "sha256": frozen[relative(RESEARCH / name)],
                }
                for name in CODE
            ],
            "interpreter": relative(INTERPRETER),
            "required_NumPy": "1.26.4",
            "required_Qiskit_Terra": "0.45.3",
            "fixed_emitted_toys": 1,
            "fixed_toy_output_qubits": 3,
            "fixed_toy_bond_path": [1, 2, 2, 1],
            "fixed_local_unitary_dimensions": [4, 4, 2],
            "maximum_SDK_calls": 3,
            "additional_matrix_only_expand_fixture": [2, 4],
            "additional_matrix_only_expand_SDK_calls": 0,
            "declared_unique_tests": TESTS,
            "rank_adaptation_or_precision_retries": False,
            "native_basis": ["ry", "rz", "cx"],
            "SDK_optimization_level": 0,
            "SDK_seed_transpiler": 0,
            "maximum_native_forward_primitive_slots": 4096,
            "right_canonicalization": "One normalization and right-to-left positive-diagonal QR",
            "unitary_completion": "Two-pass Gram-Schmidt, lexicographic completion, positive QR",
            "rank_threshold": "1e-12",
            "global_phases_in_full_operator_check": True,
            "shrink_cleared_wire_excluded_from_local_decomposition": True,
            "literal_inverse_dirty_entangled_diagnostic": True,
            "new_q10_Gaussian_table_evaluations": 0,
            "new_q10_compressions_or_candidates": 0,
            "new_Clifford_T_synthesis_calls": 0,
            "new_financial_prices_or_source_replays": 0,
            "full_q10_target_or_loader_error_certificate": None,
            "full_loader_T_cost_or_physical_runtime": None,
            "failed_q10_uniform_price_law_certificate_resolved": False,
            "source_sampler_or_financial_price_contract_changed": False,
            "process_CPU_limit_seconds": CPU_LIMIT,
            "post_fixture_new_work_admission_CPU_seconds": 100,
            "elapsed_wall_limit_seconds": WALL_LIMIT,
            "numerical_threads_per_process": 1,
            "tool_package_inventory_is_literal_and_bounded": True,
            "all_frozen_insertions_resolve_aliases_and_preserve_previous_SHA_expectations": True,
            "partial_preparation_failures_are_terminal_and_preserved": True,
            "SDK_imports_and_calls_occur_only_in_the_frozen_run": True,
            "maximum_tool_files": MAXIMUM_TOOL_FILES,
            "actual_tool_files_frozen": len(paths) - len(CODE),
            "python": sys.version,
        },
    )
    print("One structural MPS toy prospectively frozen", flush=True)


def receipt_files(output):
    return {
        relative(path): sha(path)
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }


def finish_manifest(output, protocol, checked_files=None):
    files = receipt_files(output) if checked_files is None else dict(checked_files)
    if checked_files is not None:
        for name in ("summary.json", "failure.json", "preparation_failure.json"):
            path = output / name
            if path.is_file():
                files[relative(path)] = sha(path)
    create(
        output / "manifest.json",
        {
            "files": files,
            "frozen_inputs": protocol["frozen_inputs"],
            "manifest_self_hash_excluded": True,
        },
    )


def run(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    if (output / "summary.json").exists():
        raise FileExistsError("Structural receipt already finished")
    protocol = read(output / "protocol.json")
    started_cpu, started_wall = time.process_time(), time.monotonic()
    checked_files = None
    previous_evidence_path = os.environ.get("A04_MPS_STRUCTURE_EVIDENCE_PATH")

    def check_budget(admission=False):
        limit = 100 if admission else CPU_LIMIT
        if (
            time.process_time() - started_cpu >= limit
            or time.monotonic() - started_wall >= WALL_LIMIT
        ):
            raise BudgetCensoredError("The fixed structural MPS execution budget was reached")

    try:
        verify(protocol["frozen_inputs"])
        pinned_interpreter()
        os.environ["A04_MPS_STRUCTURE_EVIDENCE_PATH"] = str(output / "structural_toy_evidence.json")
        rc = pytest.main(
            [
                str(RESEARCH / "test_mps_sequential_structure.py"),
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml=" + str(output / "tests.xml"),
            ]
        )
        suites = ET.parse(output / "tests.xml").getroot()
        cases = list(suites.iter("testcase"))
        identities = {(item.attrib.get("classname"), item.attrib["name"]) for item in cases}
        assert rc == 0 and len(cases) == len(identities) == TESTS
        assert not any(list(suites.iter(tag)) for tag in ("failure", "error", "skipped"))
        check_budget(admission=True)
        evidence = read(output / "structural_toy_evidence.json")
        assert evidence["actual_local_SDK_calls"] == 3 and evidence["bond_path"] == [1, 2, 2, 1]
        assert evidence["diagnostics"]["local_dimensions"] == [4, 4, 2]
        assert evidence["numerical_diagnostics_are_rigorous_error_bounds"] is False
        verify(protocol["frozen_inputs"])
        checked_files = receipt_files(output)
        check_budget()
        cpu, wall = time.process_time() - started_cpu, time.monotonic() - started_wall
        create(
            output / "summary.json",
            {
                "passed": True,
                "local_only": True,
                "budget_censored": False,
                "fixtures_passed": TESTS,
                "unique_testcases": len(identities),
                "fixed_nonfinancial_emitted_toys": 1,
                "actual_local_SDK_decompositions": 3,
                "additional_expand_fixture_SDK_calls": 0,
                "fresh_output_and_bond_wire_structure_verified": True,
                "right_canonical_fixed_normalization_and_phase_verified_numerically": True,
                "structural_shrink_scratch_support_and_full_operator_checked": True,
                "literal_inverse_dirty_entangled_diagnostic_passed": True,
                "numerical_comparisons_are_rigorous_Gaussian_error_certificates": False,
                "native_primitive_counts": evidence["diagnostics"]["native_primitive_counts"],
                "new_q10_target_evaluations_compressions_or_candidates": 0,
                "new_Clifford_T_synthesis_calls": 0,
                "full_q10_preparation_error_or_T_cost": None,
                "financial_sampler_changed": False,
                "failed_q10_uniform_law_certificate_resolved": False,
                "new_financial_price_observations": 0,
                "quantum_advantage_claim": False,
                "CPU_seconds": cpu,
                "wall_seconds": wall,
            },
        )
    except BaseException as failure:
        create(
            output / "failure.json",
            {
                "passed": False,
                "failure_type": type(failure).__name__,
                "message": str(failure),
                "traceback": traceback.format_exc(),
            },
        )
        if not (output / "summary.json").exists():
            create(
                output / "summary.json",
                {
                    "passed": False,
                    "local_only": True,
                    "budget_censored": isinstance(failure, (BudgetCensoredError, TimeoutError)),
                    "failure_type": type(failure).__name__,
                    "message": str(failure),
                    "new_q10_candidates_or_synthesis_calls": 0,
                    "full_q10_preparation_error_or_T_cost": None,
                    "financial_sampler_changed": False,
                    "quantum_advantage_claim": False,
                },
            )
        raise
    finally:
        if previous_evidence_path is None:
            os.environ.pop("A04_MPS_STRUCTURE_EVIDENCE_PATH", None)
        else:
            os.environ["A04_MPS_STRUCTURE_EVIDENCE_PATH"] = previous_evidence_path
        finish_manifest(output, protocol, checked_files)
    print("One structural MPS toy PASS; Gaussian/cost certificates remain separate", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=PROGRAM / "A04_structure_run001")
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
