"""Prospective direct14T comparator for the immutable A16 fragment receipt.

Authoring is permitted during the Stage C hold. Execution requires root's
timing-idle clearance. Emit one direct comparator only; do not rerun A16.
"""

from __future__ import annotations

# Code is imported after the standalone script's workspace path is installed.
# ruff: noqa: E402, E501

import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from research.limitation_program_20261001.experiment_temporary_and_fulladder import (
    independent_columns,
    independent_contract,
    np,
    read,
    relative,
    save,
    sha,
    verify,
)
from research.limitation_program_20261001.direct_fulladder_control import (
    direct_schedule,
    exact_direct_contract,
    literal_adjoint_array,
)
from research.limitation_program_20261001.temporary_and_fulladder import (
    decode,
    encode,
    resources,
)

PROGRAM = ROOT / "results/limitation_program_20261001"
RESEARCH = ROOT / "research/limitation_program_20261001"
PRIOR = PROGRAM / "A16_dynamic_run001"
CODE = (
    "direct_fulladder_control.py",
    "test_direct_fulladder_control.py",
    "experiment_direct_fulladder_control.py",
)
TESTS = 5
CPU_LIMIT = 60
MAX_TOOL_FILES = 12288


def bind(frozen, name, digest):
    path = (ROOT / str(name).replace("\\", "/")).resolve()
    path.relative_to(ROOT)
    normalized = relative(path)
    if (
        not isinstance(digest, str)
        or len(digest) != 64
        or any(char not in "0123456789abcdef" for char in digest)
    ):
        raise ValueError("Explicit canonical SHA256 dependency expected")
    if normalized in frozen and frozen[normalized] != digest:
        raise ValueError("Existing frozen SHA expectation conflicts: " + normalized)
    frozen[normalized] = digest


def receipt_files(output):
    return {
        relative(path): sha(path)
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }


def tool_paths():
    import pytest
    import _pytest

    files = set()
    directories = [Path(module.__file__).resolve().parent for module in (np, pytest, _pytest)]
    directories.append(directories[0].parent / "numpy.libs")
    for directory in directories:
        if not directory.exists():
            continue
        directory.relative_to(ROOT)
        for path in directory.rglob("*"):
            if (
                path.is_file()
                and "__pycache__" not in path.parts
                and path.suffix.lower()
                in (
                    ".py",
                    ".pyd",
                    ".dll",
                    ".so",
                )
            ):
                files.add(path)
                if len(files) > MAX_TOOL_FILES:
                    raise ValueError("Fixed direct-control installed-tool inventory exceeded")
    return sorted(files)


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    if output.exists():
        raise FileExistsError("Fresh direct-control receipt required; no same-receipt retry")
    frozen = {}
    try:
        prepare_body(output, frozen)
    except BaseException as failure:
        if output.exists():
            if not (output / "protocol.json").exists():
                save(
                    output / "protocol.json",
                    dict(
                        local_only=True,
                        frozen_inputs=frozen,
                        terminal_partial_preparation=True,
                        declared_unique_tests=TESTS,
                    ),
                )
            save(
                output / "preparation_failure.json",
                dict(
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    traceback=traceback.format_exc(),
                    frozen_bytes_expected_at_failure=frozen,
                    partial_files_preserved=True,
                    same_receipt_retry_allowed=False,
                ),
            )
            save(
                output / "summary.json",
                dict(
                    passed=False,
                    new_test_credit=0,
                    local_only=True,
                    preparation_failed=True,
                    budget_censored=isinstance(failure, TimeoutError),
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    fixed_receipt_terminal_no_retry=True,
                    new_financial_prices_or_gate_observations=0,
                ),
            )
            finish_manifest(output)
        raise


def prepare_body(output, frozen):
    summary = read(PRIOR / "summary.json")
    if summary.get("passed") is not True or summary.get("budget_censored", False) is not False:
        raise ValueError("Successful uncensored immutable A16 prerequisite required")
    previous = read(PRIOR / "manifest.json")
    for field in ("files", "frozen_inputs"):
        for name, digest in previous[field].items():
            bind(frozen, name, digest)
    bind(frozen, PRIOR / "manifest.json", sha(PRIOR / "manifest.json"))
    for path in [*(RESEARCH / name for name in CODE), Path(sys.executable), *tool_paths()]:
        bind(frozen, path, sha(path))
    verify(frozen)
    output.mkdir()
    for name in CODE:
        shutil.copy2(RESEARCH / name, output / name)
        if sha(output / name) != frozen[relative(RESEARCH / name)]:
            raise ValueError("Frozen direct-control code snapshot differs: " + name)
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_tests_gate_arrays_or_channel_checks=True,
            execution_requires_root_Stage_C_timing_idle_clearance=True,
            frozen_inputs=frozen,
            declared_unique_tests=TESTS,
            fixed_new_unitary_comparators=1,
            original_dynamic_candidates_reexecuted=0,
            direct_control="Two exact seven-T CCX act directly on dirty carry; sum receives b'=a XOR b andc, then b is restored",
            logical_wires=dict(a=0, b=1, c=2, dirty_sum=3, dirty_carry=4),
            prior_ABI_unused_scratch_wires=[5, 6],
            arbitrary_unused_scratch_preserved=True,
            fresh_scratch_required=0,
            fixed_actual_serial_primitive_slots=34,
            direct_T_count=14,
            prior_declared_compute_copy_uncompute_control_T_count=28,
            prior_measured_fragment_T_count=8,
            direct_total_basis_columns=128,
            dirty_logical_output_patterns=4,
            independent_matrix_evaluator="Reuse immutable A16 dense Kronecker evaluator, separate from vectorized primitive evaluator",
            exact_gate_proof="Q(omega) full dirty-target CCX columns and exact all32 integer Boolean fulladder permutation",
            numeric_matrix_tolerance=1e-12,
            literal_adjoint_emitted=True,
            literal_adjoint_and_forward_T_counts_charged_separately=True,
            classical_reference_replay_only=True,
            process_CPU_limit_seconds=CPU_LIMIT,
            tool_package_inventory=["numpy", "pytest", "_pytest"],
            adjacent_NumPy_DLL_libraries_frozen=True,
            maximum_tool_files=MAX_TOOL_FILES,
            physical_feedback_clock_or_runtime_seconds=None,
            native_compiler_integration=None,
            best_possible_unitary_optimality_claim=False,
            new_financial_prices_or_gate_observations=0,
        ),
    )
    verify(frozen)
    print("Direct14T fulladder comparator prospectively frozen", flush=True)


def run(output):
    import pytest

    started = time.process_time()
    output = Path(output).resolve()
    if (output / "summary.json").exists():
        raise FileExistsError("Direct-control receipt already terminal; no retry")
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    rc = pytest.main(
        [
            str(RESEARCH / "test_direct_fulladder_control.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    xml = ET.parse(output / "tests.xml").getroot()
    cases = list(xml.iter("testcase"))
    assert rc == 0 and len(cases) == TESTS
    assert len({(item.attrib.get("classname"), item.attrib["name"]) for item in cases}) == TESTS
    assert (
        not list(xml.iter("failure"))
        and not list(xml.iter("error"))
        and not list(xml.iter("skipped"))
    )
    if time.process_time() - started >= CPU_LIMIT:
        raise TimeoutError("Fixed direct-control60CPU work-admission budget exceeded")
    forward_file, inverse_file = output / "direct.npy", output / "literal_adjoint.npy"
    np.save(forward_file, encode(direct_schedule()), allow_pickle=False)
    forward_array = np.load(forward_file, allow_pickle=False)
    np.save(inverse_file, literal_adjoint_array(forward_array), allow_pickle=False)
    inverse_array = np.load(inverse_file, allow_pickle=False)
    formal = exact_direct_contract(forward_array)
    save(output / "exact_direct_unitary_proof.json", formal)
    target = np.kron(np.eye(4), independent_contract())
    independent = independent_columns(forward_array, (0, 0), np.eye(128, dtype=np.complex128))
    inverse = independent_columns(inverse_array, (0, 0), independent)
    forward_error = float(np.max(np.abs(independent - target)))
    inverse_error = float(np.max(np.abs(inverse - np.eye(128))))
    assert forward_error < 1e-12 and inverse_error < 1e-12
    np.save(output / "independent_direct_unitary.npy", independent, allow_pickle=False)
    prior_kraus = np.load(PRIOR / "independent_logical_kraus.npy", allow_pickle=False)
    assert prior_kraus.shape == (4, 32, 32)
    previous_errors = [
        float(np.max(np.abs(2 * branch - independent[:32, :32]))) for branch in prior_kraus
    ]
    assert max(previous_errors) < 1e-12
    save(
        output / "channel_comparison.json",
        dict(
            new_direct_full_unitary_columns=128,
            exact_all32_dirty_sum_carry_contract=True,
            arbitrary_two_scratch_wire_values_preserved=True,
            independent_forward_matrix_error=forward_error,
            independent_literal_adjoint_error=inverse_error,
            existing_saved_dynamic_Kraus_comparison_errors=previous_errors,
            existing_dynamic_branches_loaded_not_reexecuted=4,
            exact_cyclotomic_proof_supplies_formal_phase_claim=True,
            numerical_tolerance_corroborates_only=True,
        ),
    )
    paid = resources(decode(forward_array))
    adjoint_paid = resources(decode(inverse_array))
    assert paid["T_count"] == adjoint_paid["T_count"] == 14
    assert paid["fixed_serial_operation_slots"] == 34
    assert paid["X_basis_measurements"] == 0
    paid["fresh_scratch_qubits"] = adjoint_paid["fresh_scratch_qubits"] = 0
    paid["active_primitive_support_qubits"] = adjoint_paid["active_primitive_support_qubits"] = 5
    paid["allocated_prior_comparison_ABI_qubits"] = adjoint_paid[
        "allocated_prior_comparison_ABI_qubits"
    ] = 7
    prior_resources = read(PRIOR / "resource_ledger.json")
    assert prior_resources["dynamic"]["T_count"] == 8
    assert prior_resources["unitary_control"]["T_count"] == 28
    save(
        output / "comparison_resource_ledger.json",
        dict(
            direct_forward=paid,
            explicit_literal_adjoint=adjoint_paid,
            prior_measured_fragment=prior_resources["dynamic"],
            prior_declared_compute_copy_uncompute_control=prior_resources["unitary_control"],
            actual_array_sha256=dict(forward=sha(forward_file), literal_adjoint=sha(inverse_file)),
            measured_vs_new_direct_T_gap=6,
            prior20T_gap_applied_only_to_declared28T_control=True,
            logical_T_count_frontier_is_an_explicit_two_candidate_comparison_only=True,
            optimal_unitary_cost_proved=False,
            native_financial_compiler_or_cost_changed=False,
            measured_vs_unitary_physical_seconds=None,
        ),
    )
    verify(protocol["frozen_inputs"])
    checked_files = receipt_files(output)
    if time.process_time() - started >= CPU_LIMIT:
        raise TimeoutError("Fixed direct-control60CPU terminal budget exceeded")
    save(
        output / "summary.json",
        dict(
            passed=True,
            budget_censored=False,
            local_only=True,
            fixtures_passed=TESTS,
            new_fixed_unitary_comparators=1,
            existing_dynamic_candidate_reexecutions=0,
            actual_new_forward_array_T_count=14,
            actual_literal_adjoint_T_count=14,
            previously_certified_measured_T_count=8,
            prior_declared28T_control_preserved=True,
            measured_vs_direct_logical_T_gap=6,
            direct_fresh_scratch_required=0,
            direct_active_primitive_support_qubits=5,
            preserved_previous_7qubit_comparison_ABI=True,
            independent_full_basis_columns=128,
            all_dirty_sum_carry_and_unused_scratch_values_supported=True,
            exact_gate_phases_and_Boolean_contract_verified=True,
            physical_feedback_routing_factory_clock_or_seconds=None,
            native_financial_compiler_integration=None,
            best_possible_unitary_frontier_certified=False,
            existing_financial_sources_changed=False,
            new_financial_prices_or_gate_observations=0,
            quantum_advantage_claim=False,
            elapsed_process_CPU_seconds=time.process_time() - started,
        ),
    )
    finish_manifest(output, checked_files)
    print("Direct14T fulladder comparator PASS; measured8T gap is6T", flush=True)


def finish_manifest(output, checked_files=None):
    files = receipt_files(output) if checked_files is None else dict(checked_files)
    if checked_files is not None:
        files[relative(output / "summary.json")] = sha(output / "summary.json")
    save(
        output / "manifest.json",
        dict(
            files=files,
            frozen_inputs=read(output / "protocol.json")["frozen_inputs"],
            manifest_self_hash_excluded=True,
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=PROGRAM / "A16_direct_control_run001")
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.output)
    else:
        output = args.output.resolve()
        output.relative_to(PROGRAM)
        if (output / "summary.json").exists():
            raise FileExistsError("Direct-control receipt is terminal; retry may not mutate it")
        try:
            run(args.output)
        except BaseException as failure:
            output = args.output.resolve()
            with (output / "failure.txt").open("x", encoding="utf-8") as handle:
                handle.write(traceback.format_exc())
            if not (output / "summary.json").exists():
                save(
                    output / "summary.json",
                    dict(
                        passed=False,
                        new_test_credit=0,
                        budget_censored=isinstance(failure, TimeoutError),
                        local_only=True,
                        failure_type=type(failure).__name__,
                        message=str(failure),
                        existing_dynamic_candidate_reexecutions=0,
                        existing_financial_sources_changed=False,
                        new_financial_prices_or_gate_observations=0,
                    ),
                )
            finish_manifest(output)
            raise
