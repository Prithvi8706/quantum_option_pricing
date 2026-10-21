"""Prospective fixed native72 measured clean-XOR and coherent-control packet."""

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
os.environ["NUMBA_NUM_THREADS"] = "1"

import numpy as np  # noqa: E402
import _pytest  # noqa: E402
import pytest  # noqa: E402
import numba  # noqa: E402
import llvmlite  # noqa: E402

from research.controlled_source_completion.primitives import gate_resources  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
CODE = (
    "dynamic_clean_xor_native.py",
    "test_dynamic_clean_xor_native.py",
    "experiment_dynamic_clean_xor_native.py",
    "dynamic_clean_xor_native_preflight.json",
)
PREREQUISITES = ("A16_dynamic_run001", "A16_direct_control_run001", "A16_clean_xor_w2_run001")
DEPENDENCIES = (
    "research/controlled_source_completion/primitives.py",
    "research/controlled_source_completion/exact_lookup.py",
    "research/journal_sprint/reversible_fixed_point.py",
    "research/antithetic_feasibility/reversible.py",
)
TESTS = 19
CPU_LIMIT = 180
WALL_LIMIT = 600
MAX_TOOL_FILES = 12288


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return path.resolve().relative_to(ROOT).as_posix()


def verify(frozen):
    for name, expected in frozen.items():
        path = (ROOT / name).resolve()
        path.relative_to(ROOT)
        if sha(path) != expected:
            raise ValueError("Frozen native channel dependency changed: " + name)


def bind_frozen(frozen, name, digest):
    path = (ROOT / str(name).replace("\\", "/")).resolve()
    path.relative_to(ROOT)
    name = relative(path)
    if name in frozen and frozen[name] != digest:
        raise ValueError("Prior exact native channel hashes disagree: " + name)
    frozen[name] = digest


def prepare(output):
    output = output.resolve()
    output.relative_to(PROGRAM)
    if output.exists():
        raise FileExistsError("Fresh prospective native channel receipt required")
    frozen = {}

    def bind(name, digest):
        bind_frozen(frozen, name, digest)

    for name in PREREQUISITES:
        prior = PROGRAM / name
        previous = read(prior / "summary.json")
        if (
            previous.get("passed") is not True
            or previous.get("budget_censored", False) is not False
        ):
            raise ValueError("Successful exact primitive and fixed-w2 prerequisites required")
        manifest = read(prior / "manifest.json")
        for field in ("files", "frozen_inputs"):
            for path, digest in manifest[field].items():
                bind(path, digest)
        bind(relative(prior / "manifest.json"), sha(prior / "manifest.json"))
    paths = [RESEARCH / name for name in CODE] + [ROOT / name for name in DEPENDENCIES]
    paths.append(Path(sys.executable))
    tools = set()
    for module in (np, pytest, _pytest, numba, llvmlite):
        directory = Path(module.__file__).resolve().parent
        directory.relative_to(ROOT)
        tools.update(
            path
            for path in directory.rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and path.suffix.lower() in (".py", ".pyd", ".dll", ".so")
        )
    for module in (np, llvmlite):
        directory = Path(module.__file__).resolve().parent.parent / (module.__name__ + ".libs")
        if directory.exists():
            directory.relative_to(ROOT)
            tools.update(path for path in directory.rglob("*.dll") if path.is_file())
    if len(tools) > MAX_TOOL_FILES:
        raise ValueError("Fixed native channel tool dependency inventory bound exceeded")
    paths.extend(sorted(tools))
    for path in paths:
        bind(relative(path), sha(path))
    verify(frozen)
    output.mkdir()
    try:
        prepare_files(output, frozen)
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
                "preparation_failed": True,
                "budget_censored": isinstance(failure, TimeoutError),
                "new_test_credit": 0,
                "financial_source_or_advantage_adopted": False,
                "fixed_receipt_terminal_no_retry": True,
            },
        )
        finish_manifest(output, {"frozen_inputs": frozen})
        raise


def prepare_files(output, frozen):
    for name in CODE:
        shutil.copy2(RESEARCH / name, output / name)
        if sha(output / name) != frozen[relative(RESEARCH / name)]:
            raise ValueError("Frozen native channel code snapshot differs: " + name)
    verify(frozen)
    create(
        output / "protocol.json",
        {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "local_only": True,
            "before_arrays_tests_primitive_channels_or_resource_evaluations": True,
            "requires_root_Stage_C_exclusive_timing_terminal_clearance": True,
            "frozen_inputs": frozen,
            "declared_unique_tests": TESTS,
            "fixed_native_width": 72,
            "native_fraction_bits": 40,
            "fixed_native_modes": ["uncontrolled", "coherent controlled"],
            "measurement_ANDs_per_native_invocation": 141,
            "fixed_native_operand_pairs": 6,
            "fixed_dirty_output_patterns": 4,
            "coherent_control_basis_values": [0, 1],
            "fixed_native_matched_contract_cases": 72,
            "native_measured_checks_are_actual_macro_array_replays": True,
            "native_measured_checks_are_full_primitive_statevectors": False,
            "native_exact_phase_claim": (
                "Actual macro arrays bind prior exact Q(omega) fresh-AND/CCX proofs; "
                "eight Boolean carry cases, actual lifetime binding "
                "and induction prove every history"
            ),
            "small_primitive_phase_corroboration": (
                "Every two-bit dirty logical column, both coherent control values "
                "and both outcomes; "
                "all eight three-bit histories with a nonuniform entangled external reference"
            ),
            "dense_quantum_diagnostic_limit_qubits": 17,
            "dense_quantum_diagnostic_limit_complex_elements": 1048576,
            "composed_invocations_require_shared_caller_owned_record_namespace": True,
            "adjoint_contract": "New forward channel, zero scratch, new141-bit result interval",
            "native_unitary_controls": (
                "Actual original Cuccaro compute/copy/literal-undo, "
                "with paid coherent CCX copy when selected"
            ),
            "comparison_is_not_unitary_optimality_theorem": True,
            "no_global_source_or_Program_undo_change": True,
            "dynamic_schedule": (
                "Fixed fully serial primitive schedule, all outcome-one feedback slots charged"
            ),
            "unitary_control_schedule": "Actual seven-T all-to-all ASAP within the original leaf",
            "T_depth_numbers_have_distinct_schedule_models": True,
            "process_CPU_limit_seconds": CPU_LIMIT,
            "new_work_admission_CPU_seconds": 140,
            "elapsed_wall_limit_seconds": WALL_LIMIT,
            "numerical_threads_per_process": 1,
            "new_financial_sources_prices_or_path_replays": 0,
            "physical_measurement_feedback_seconds": None,
            "full_financial_source_resources": None,
            "python": sys.version,
            "canonical_frozen_hash_insertions_preserve_all_prior_expectations": True,
            "partial_preparation_failure_is_terminal_and_preserved": True,
            "bulk_output_hashing_precedes_terminal_CPU_and_wall_check": True,
            "tool_package_inventory": ["numpy", "pytest", "_pytest", "numba", "llvmlite"],
            "adjacent_NumPy_LLVM_DLL_libraries_frozen": True,
            "maximum_tool_files": MAX_TOOL_FILES,
        },
    )
    print("Native72 channel and controlled-copy packet prospectively frozen", flush=True)


def receipt_files(output):
    return {
        relative(path): sha(path)
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }


def finish_manifest(output, protocol, checked_files=None):
    if checked_files is None:
        checked_files = receipt_files(output)
    else:
        checked_files = dict(checked_files)
        checked_files[relative(output / "summary.json")] = sha(output / "summary.json")
    create(
        output / "manifest.json",
        {
            "files": checked_files,
            "frozen_inputs": protocol["frozen_inputs"],
            "manifest_self_hash_excluded": True,
        },
    )


def run(output):
    output = output.resolve()
    output.relative_to(PROGRAM)
    if (output / "summary.json").exists():
        raise FileExistsError("Finished native channel receipt is immutable")
    protocol = read(output / "protocol.json")
    started_cpu, started_wall = time.process_time(), time.monotonic()
    checked_files = None
    try:
        verify(protocol["frozen_inputs"])
        os.environ["A16_NATIVE_ADD_EVIDENCE_PATH"] = str(output / "native_arrays")
        rc = pytest.main(
            [
                str(RESEARCH / "test_dynamic_clean_xor_native.py"),
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml=" + str(output / "tests.xml"),
            ]
        )
        suites = ET.parse(output / "tests.xml").getroot()
        cases = list(suites.iter("testcase"))
        identities = {(case.attrib.get("classname"), case.attrib["name"]) for case in cases}
        if rc != 0 or len(cases) != len(identities) or len(cases) != TESTS:
            raise ValueError("Fixed native channel fixture set did not pass")
        if any(list(suites.iter(tag)) for tag in ("failure", "error", "skipped")):
            raise ValueError("Failed or skipped native channel cases")
        if time.process_time() - started_cpu >= 140:
            raise TimeoutError("Native channel new-work admission CPU limit exceeded")
        arrays = output / "native_arrays"
        bindings = read(arrays / "recipe_binding.json")
        ledgers = {}
        for controlled, expected_t, expected_slots in ((False, 564, 2687), (True, 1565, 4689)):
            name = "controlled" if controlled else "uncontrolled"
            dynamic_path, control_path = (
                arrays / (name + "_dynamic.npy"),
                arrays / (name + "_control.npy"),
            )
            adjoint_path = arrays / (name + "_dynamic_adjoint.npy")
            dynamic = np.load(dynamic_path, allow_pickle=False)
            adjoint = np.load(adjoint_path, allow_pickle=False)
            control = np.load(control_path, allow_pickle=False)
            if dynamic.dtype != np.dtype("int16") or dynamic.shape != (expected_slots, 5):
                raise ValueError("Saved actual dynamic array shape differs")
            values, amounts = np.unique(dynamic[:, 0], return_counts=True)
            counts = dict(zip(map(int, values), map(int, amounts), strict=True))
            if counts.get(2, 0) + counts.get(3, 0) != expected_t or counts.get(7) != 141:
                raise ValueError("Saved actual T/measurement counts differ")
            expected_adjoint = dynamic.copy()
            recorded = expected_adjoint[:, 4] >= 0
            expected_adjoint[recorded, 4] += 141
            if not np.array_equal(adjoint, expected_adjoint):
                raise ValueError(
                    "Actual adjoint does not use the same recipe with fresh retained records"
                )
            if control.dtype != np.dtype("int32") or control.ndim != 2 or control.shape[1] != 4:
                raise ValueError("Saved original unitary control ABI differs")
            qubits = 4 * 72 + 1 + int(controlled)
            abc, td, ct = gate_resources(control, qubits)
            x, cx, ccx = map(int, abc)
            proof = bindings[str(controlled)]
            if proof["supported_width"] != 72 or proof["AND_fresh_targets"] != 141:
                raise ValueError("Actual native proof binding differs")
            ledgers[name] = {
                "dynamic_array": relative(dynamic_path),
                "dynamic_sha256": sha(dynamic_path),
                "dynamic_forward": {
                    "T_count": expected_t,
                    "T_depth_fixed_serial": expected_t,
                    "serial_primitive_slots": expected_slots,
                    "logical_qubits": 216 + int(controlled),
                    "allocated_qubits": 500 + int(controlled),
                    "fresh_scratch": 284,
                    "measurements": 141,
                    "feedback_CZ": 141,
                    "conditional_X_reset": 141,
                    "retained_record_bits": 141,
                    "actual_opcode_counts": counts,
                },
                "dynamic_adjoint": {
                    "actual_array": relative(adjoint_path),
                    "actual_sha256": sha(adjoint_path),
                    "record_ids": [141, 282],
                    "resource_counts_same_as_forward": True,
                    "zero_scratch_required": True,
                },
                "unitary_array": relative(control_path),
                "unitary_sha256": sha(control_path),
                "unitary_forward": {
                    "qubits": qubits,
                    "fresh_scratch": 73,
                    "x": x,
                    "cx": cx,
                    "ccx": ccx,
                    "T_count": 7 * ccx,
                    "T_depth_all_to_all_ASAP": int(td),
                    "Clifford_T_depth_all_to_all_ASAP": int(ct),
                    "source_gates": len(control),
                },
                "T_count_gap_to_this_control": 7 * ccx - expected_t,
                "T_depth_models_are_different": True,
                "unitary_optimality_proved": False,
                "financial_source_gain": None,
                "physical_seconds": None,
            }
        create(output / "resource_ledger.json", ledgers)
        verify(protocol["frozen_inputs"])
        checked_files = receipt_files(output)
        cpu, wall = time.process_time() - started_cpu, time.monotonic() - started_wall
        if cpu >= CPU_LIMIT or wall >= WALL_LIMIT:
            raise TimeoutError("Fixed native channel receipt budget exceeded")
        create(
            output / "summary.json",
            {
                "passed": True,
                "budget_censored": False,
                "local_only": True,
                "fixtures_passed": TESTS,
                "unique_testcases": len(identities),
                "native_width": 72,
                "native_modes": ["uncontrolled", "coherent controlled"],
                "native_forward_channel_arrays_emitted": 2,
                "native_adjoint_channel_arrays_emitted": 2,
                "original_unitary_control_arrays_emitted": 2,
                "native_actual_primitive_quantum_statevectors": 0,
                "native_macro_bindings_and_generic_carry_lifetime_proof": True,
                "native_matched_contract_basis_cases": 72,
                "small_width_primitive_channel_phase_and_reference_corroboration": True,
                "dynamic_adjoint_requires_fresh_records_and_zero_scratch": True,
                "measurement_array_literal_inverse_supported": False,
                "native_Program_undo_or_financial_compiler_integration": None,
                "new_financial_source_prices_or_replays": 0,
                "physical_feedback_seconds": None,
                "quantum_advantage_claim": False,
                "CPU_seconds": cpu,
                "wall_seconds": wall,
            },
        )
    except BaseException as failure:
        checked_files = None
        create(
            output / "failure.json",
            {
                "passed": False,
                "budget_censored": isinstance(failure, TimeoutError),
                "new_test_credit": 0,
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
                    "budget_censored": isinstance(failure, TimeoutError),
                    "new_test_credit": 0,
                    "local_only": True,
                    "failure_type": type(failure).__name__,
                    "message": str(failure),
                    "financial_source_or_advantage_adopted": False,
                },
            )
        raise
    finally:
        os.environ.pop("A16_NATIVE_ADD_EVIDENCE_PATH", None)
        finish_manifest(output, protocol, checked_files)
    print(
        "Native72 measured/control/adjoint packet PASS; full source integration remains separate",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=PROGRAM / "A16_clean_xor_native_run001")
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
