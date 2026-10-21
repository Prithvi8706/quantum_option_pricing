"""Prospective fixed w2 dynamic clean-XOR channel and direct seven-T control.

Static authoring only during Stage C timing. No generic-width emitter, native
dispatch change, financial execution, or physical runtime conversion.
"""

from __future__ import annotations

# Standalone workspace imports and explanatory protocol prose.
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
    np,
    read,
    relative,
    save,
    sha,
    verify,
)
from research.limitation_program_20261001.direct_fulladder_control import literal_adjoint_array
from research.limitation_program_20261001.dynamic_clean_xor_adder import (
    QUBITS,
    arbitrary_width_lemma,
    direct_schedule,
    exact_fixed_contract,
    logical_injection,
    measured_schedule,
    resources,
    run_columns,
    validate_array,
)

PROGRAM = ROOT / "results/limitation_program_20261001"
RESEARCH = ROOT / "research/limitation_program_20261001"
PRIORS = (PROGRAM / "A16_dynamic_run001", PROGRAM / "A16_direct_control_run001")
CODE = (
    "dynamic_clean_xor_adder.py",
    "test_dynamic_clean_xor_adder.py",
    "experiment_dynamic_clean_xor_adder.py",
)
NATIVE_SOURCE = (
    ROOT / "research/controlled_source_completion/primitives.py",
    ROOT / "research/journal_sprint/reversible_fixed_point.py",
    PROGRAM / "A10_coefficient_run001/executed_code/primitives.py",
    PROGRAM / "A10_coefficient_run001/executed_code/reversible_fixed_point.py",
)
TESTS = 8
CPU_LIMIT = 60
MAX_TOOL_FILES = 12288


def independent_contract():
    result = np.zeros((64, 64), dtype=np.complex128)
    for a in range(4):
        for b in range(4):
            for old in range(4):
                result[a + 4 * b + 16 * (old ^ ((a + b) % 4)), a + 4 * b + 16 * old] = 1
    return result


def tensor_operator(local):
    result = np.asarray([[1]], dtype=np.complex128)
    for wire in reversed(range(QUBITS)):
        result = np.kron(result, local.get(wire, np.eye(2)))
    return result


def independent_columns(array, injection, outcome=0):
    """Explicit Kronecker matrices applied in sparse coordinate form.

    No bit-mask/vectorized producer evaluator is called. The resulting full
    branch is unnormalized, including discarded projector probability.
    """
    validate_array(array)
    x = np.asarray([[0, 1], [1, 0]], dtype=np.complex128)
    h = np.asarray([[1, 1], [1, -1]], dtype=np.complex128) / np.sqrt(2)
    t = np.diag([1, (1 + 1j) / np.sqrt(2)])
    p0, p1 = np.diag([1, 0]), np.diag([0, 1])
    result = injection.copy()
    for code, first, second, condition, register in array.tolist():
        if condition == 1 and outcome != 1:
            continue
        if code == 7:
            operator = tensor_operator({first: p1 if outcome else p0})
        elif code == 5:
            operator = tensor_operator({first: p0}) + tensor_operator({first: p1, second: x})
        elif code == 6:
            operator = np.eye(1 << QUBITS) - 2 * tensor_operator({first: p1, second: p1})
        else:
            single = {1: h, 2: t, 3: t.conj().T, 4: np.diag([1, -1j]), 8: x}[code]
            operator = tensor_operator({first: single})
        destinations, sources = np.nonzero(operator)
        following = np.zeros_like(result)
        np.add.at(following, destinations, operator[destinations, sources, None] * result[sources])
        result = following
    return result


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
                    raise ValueError("Fixed w2 installed-tool inventory exceeded")
    return sorted(files)


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    if output.exists():
        raise FileExistsError("Fresh w2 receipt required; no same-receipt retry")
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
                    finance_sources_or_observations_changed=0,
                ),
            )
            finish_manifest(output)
        raise


def prepare_body(output, frozen):
    for prior in PRIORS:
        summary = read(prior / "summary.json")
        if summary.get("passed") is not True or summary.get("budget_censored", False) is not False:
            raise ValueError("Successful uncensored prerequisite required: " + prior.name)
        manifest = read(prior / "manifest.json")
        for field in ("files", "frozen_inputs"):
            for name, digest in manifest[field].items():
                bind(frozen, name, digest)
        bind(frozen, prior / "manifest.json", sha(prior / "manifest.json"))
    for path in [
        *(RESEARCH / name for name in CODE),
        *NATIVE_SOURCE,
        Path(sys.executable),
        *tool_paths(),
    ]:
        bind(frozen, path, sha(path))
    verify(frozen)
    output.mkdir()
    for name in CODE:
        shutil.copy2(RESEARCH / name, output / name)
        if sha(output / name) != frozen[relative(RESEARCH / name)]:
            raise ValueError("Frozen w2 code snapshot differs: " + name)
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_tests_arrays_or_channel_evaluations=True,
            execution_requires_root_Stage_C_timing_idle_clearance=True,
            frozen_inputs=frozen,
            declared_unique_tests=TESTS,
            fixed_width=2,
            measured_fragments=1,
            direct_unitary_controls=1,
            explicit_unitary_literal_adjoint=True,
            logical_wires=dict(a=[0, 1], b=[2, 3], arbitrary_output=[4, 5]),
            measured_fresh_scratch=dict(p=[6, 7], g0=8, c1=9),
            measurement_records_retained=True,
            adjoint_channel_requires_a_fresh_measurement_record=True,
            all_logical_basis_columns=64,
            measurement_outcome_branches=2,
            dirty_output_patterns=4,
            entangled_reference_columns=5,
            direct_full_ABI_basis_fixture_columns=1024,
            numeric_corroboration_tolerance=1e-12,
            exact_macro_proof="Reuse frozen Q(omega) fresh-target AND and full dirty-target CCX; exact64 integer Boolean enumeration binds fixed arrays",
            independent_evaluator="Ten-qubit Kronecker primitive matrices applied in coordinate sparse form, separate from bit-mask evaluator",
            original_native_clean_XOR_contract="primitives.build add preserves both inputs and XORs modular sum into arbitrary output; w work bits and one helper are fresh and erased by literal Program.undo",
            original_Cuccaro_CCX_targets_are_not_fresh_AND=True,
            original_native_source_files=[relative(path) for path in NATIVE_SOURCE],
            no_generic_width_circuit_emitter=True,
            arbitrary_width_result="Analytic carry/lifetime lemma only, no native72 array, dispatch or resources credited",
            process_CPU_limit_seconds=CPU_LIMIT,
            tool_package_inventory=["numpy", "pytest", "_pytest"],
            adjacent_NumPy_DLL_libraries_frozen=True,
            maximum_tool_files=MAX_TOOL_FILES,
            physical_seconds=None,
            compiler_channel_adjoint_ABI=None,
            finance_sources_or_observations_changed=0,
        ),
    )
    verify(frozen)
    print("Fixed w2 clean-XOR experiment prospectively frozen", flush=True)


def run(output):
    import pytest

    started = time.process_time()
    output = Path(output).resolve()
    if (output / "summary.json").exists():
        raise FileExistsError("W2 receipt already terminal; no retry")
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    rc = pytest.main(
        [
            str(RESEARCH / "test_dynamic_clean_xor_adder.py"),
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
        raise TimeoutError("Fixed w2 60CPU work-admission budget exceeded")
    paths = dict(
        measured=output / "measured_w2.npy",
        direct=output / "direct_w2.npy",
        literal_adjoint=output / "direct_literal_adjoint_w2.npy",
    )
    np.save(paths["measured"], measured_schedule(), allow_pickle=False)
    np.save(paths["direct"], direct_schedule(), allow_pickle=False)
    measured, direct = (np.load(paths[key], allow_pickle=False) for key in ("measured", "direct"))
    np.save(paths["literal_adjoint"], literal_adjoint_array(direct), allow_pickle=False)
    inverse = np.load(paths["literal_adjoint"], allow_pickle=False)
    save(output / "exact_fixed_channel_proof.json", exact_fixed_contract(measured, direct))
    save(output / "arbitrary_width_analytic_lemma.json", arbitrary_width_lemma())
    target = independent_contract()
    injection = logical_injection()
    logical = []
    branch_records = []
    state = np.asarray(
        [[complex(i + j + 1, (i * 3 - j) % 11) for j in range(5)] for i in range(64)]
    )
    state /= np.linalg.norm(state)
    for outcome in (0, 1):
        actual = independent_columns(measured, injection, outcome)
        k = actual[:64]
        reference = run_columns(measured, injection, outcome)
        errors = dict(
            logical_phase_error=float(np.max(np.abs(k - target / np.sqrt(2)))),
            scratch_cleanup_error=float(np.max(np.abs(actual[64:]))),
            vectorized_crosscheck_error=float(np.max(np.abs(actual - reference))),
            branch_probability_matrix_error=float(np.max(np.abs(k.conj().T @ k - np.eye(64) / 2))),
            external_reference_error=float(np.max(np.abs(k @ state - target @ state / np.sqrt(2)))),
        )
        assert max(errors.values()) < 1e-12
        logical.append(k)
        branch_records.append(dict(outcome=outcome, exact_probability=[1, 2], **errors))
    np.save(output / "independent_logical_kraus.npy", np.stack(logical), allow_pickle=False)
    direct_full = independent_columns(direct, injection)
    adjoint_full = independent_columns(inverse, direct_full)
    direct_error = float(np.max(np.abs(direct_full[:64] - target)))
    direct_scratch_error = float(np.max(np.abs(direct_full[64:])))
    inverse_error = float(np.max(np.abs(adjoint_full - injection)))
    assert max(direct_error, direct_scratch_error, inverse_error) < 1e-12
    save(
        output / "channel_certificate.json",
        dict(
            branches=branch_records,
            actual64_dirty_output_columns_per_branch=True,
            entangled_reference_columns=5,
            direct_clean_XOR_error=direct_error,
            direct_scratch_error=direct_scratch_error,
            actual_literal_adjoint_error=inverse_error,
            dynamic_adjoint_channel="Same forward schedule with fresh scratch, since the supported XOR unitary is self-inverse",
            adjoint_measurement_record_is_fresh=True,
            measurement_records_are_independent_and_retained=True,
            measurement_array_literal_reversal_supported=False,
            exact_macro_and_integer_proof_supplies_formal_claim=True,
            numeric_tolerances_are_corroboration_only=True,
        ),
    )
    paid = resources(measured, measured=True)
    control = resources(direct, measured=False)
    adjoint = resources(inverse, measured=False)
    assert paid["T_count"] == 4 and control["T_count"] == adjoint["T_count"] == 7
    save(
        output / "resource_ledger.json",
        dict(
            measured_forward=paid,
            measured_channel_adjoint_same_fresh_schedule=dict(paid),
            direct_forward=control,
            direct_literal_adjoint=adjoint,
            actual_array_sha256={key: sha(path) for key, path in paths.items()},
            measured_vs_direct_logical_T_gap=3,
            measured_uses4_fresh_scratch_direct_uses0=True,
            current_native_leaf_resource_claim=None,
            native72_emitted_resources=None,
            physical_seconds=None,
            best_possible_unitary_optimality_proved=False,
        ),
    )
    verify(protocol["frozen_inputs"])
    checked_files = receipt_files(output)
    if time.process_time() - started >= CPU_LIMIT:
        raise TimeoutError("Fixed w2 60CPU terminal budget exceeded")
    save(
        output / "summary.json",
        dict(
            passed=True,
            budget_censored=False,
            local_only=True,
            fixtures_passed=TESTS,
            fixed_width=2,
            measured_fragments=1,
            direct_unitary_controls=1,
            actual_logical_basis_columns=64,
            actual_measurement_branches=2,
            exact_fresh_AND_and_dirty_target_CCX_proofs=True,
            actual_channel_cleanup_and_entangled_reference_checks=True,
            measured_T_count=4,
            direct_T_count=7,
            measured_fresh_scratch=4,
            direct_fresh_scratch=0,
            dynamic_adjoint_contract_proved=True,
            arbitrary_width_result="Analytic lemma only; no arbitrary-width circuits emitted",
            native_backend_channel_adjoint_integration=None,
            native72_arrays_or_resources=None,
            physical_seconds=None,
            finance_sources_or_observations_changed=0,
            quantum_advantage_claim=False,
            elapsed_process_CPU_seconds=time.process_time() - started,
        ),
    )
    finish_manifest(output, checked_files)
    print("Fixed w2 clean-XOR channel PASS; measured4T versus direct7T", flush=True)


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
    parser.add_argument("--output", type=Path, default=PROGRAM / "A16_clean_xor_w2_run001")
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.output)
    else:
        output = args.output.resolve()
        output.relative_to(PROGRAM)
        if (output / "summary.json").exists():
            raise FileExistsError("W2 receipt is terminal; retry may not mutate it")
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
                        finance_sources_or_observations_changed=0,
                    ),
                )
            finish_manifest(output)
            raise
