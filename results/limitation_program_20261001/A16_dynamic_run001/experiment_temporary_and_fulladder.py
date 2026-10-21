"""Freeze and verify one measured fulladder channel and its unitary control.

The producer's independent dense-matrix evaluator reads actual saved arrays.
No finance, compiler integration, runtime conversion or extra candidates.
"""

from __future__ import annotations

# Exact algebra and receipt descriptions are readable prose.
# ruff: noqa: E402, E501

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from itertools import product
import json
import os
from pathlib import Path
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

# The declared dense matrices use one numerical thread in this process only.
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from research.limitation_program_20261001.temporary_and_fulladder import (
    channel_certificate,
    decode,
    encode,
    fulladder_schedule,
    resources,
    run_columns,
)

PROGRAM = ROOT / "results/limitation_program_20261001"
RESEARCH = ROOT / "research/limitation_program_20261001"
PRIMARY = ROOT / ".context/a16_primary/Gidney1709.06648v3.pdf"
CODE = (
    "temporary_and_fulladder.py",
    "test_temporary_and_fulladder.py",
    "experiment_temporary_and_fulladder.py",
)
FIXTURES = 15
CPU_LIMIT = 60


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def verify(files):
    for name, digest in files.items():
        assert sha(ROOT / name) == digest, ("Frozen dependency changed", name)


def local_operator(mapping):
    result = np.asarray([[1]], dtype=np.complex128)
    for wire in reversed(range(7)):
        result = np.kron(result, mapping.get(wire, np.eye(2, dtype=np.complex128)))
    return result


def independent_columns(saved_array, outcomes, injection):
    """Independent Kronecker/projector matrix evaluator, not apply()/decode()."""
    assert saved_array.dtype == np.dtype(np.int16) and saved_array.shape[1] == 5
    identity = np.eye(128, dtype=np.complex128)
    x = np.asarray([[0, 1], [1, 0]], dtype=np.complex128)
    h = np.asarray([[1, 1], [1, -1]], dtype=np.complex128) / np.sqrt(2)
    t = np.diag([1, (1 + 1j) / np.sqrt(2)])
    sdg = np.diag([1, -1j])
    p0, p1 = np.diag([1, 0]), np.diag([0, 1])
    result = injection.copy()
    measured = set()
    for code, first, second, condition, register in saved_array.tolist():
        assert 0 <= first < 7
        if condition >= 0:
            assert register in measured and condition == 1
            if outcomes[register] != condition:
                continue
        if code == 7:
            assert register in (0, 1) and register not in measured
            measured.add(register)
            matrix = local_operator({first: p1 if outcomes[register] else p0})
        elif code in (1, 2, 3, 4, 8):
            single = {1: h, 2: t, 3: t.conj().T, 4: sdg, 8: x}[code]
            matrix = local_operator({first: single})
        elif code in (5, 6):
            assert 0 <= second < 7 and first != second
            matrix = (
                local_operator({first: p0}) + local_operator({first: p1, second: x})
                if code == 5
                else identity - 2 * local_operator({first: p1, second: p1})
            )
        else:
            raise ValueError("Unknown frozen opcode")
        result = matrix @ result
    return result


def independent_contract():
    """Enumerate integer addition, independently of the circuit decomposition."""
    result = np.zeros((32, 32), dtype=np.complex128)
    for source in range(32):
        a, b, c, old_sum, old_carry = ((source >> bit) & 1 for bit in range(5))
        addition = a + b + c
        target = (
            a + 2 * b + 4 * c + 8 * (old_sum ^ (addition & 1)) + 16 * (old_carry ^ (addition >> 1))
        )
        result[target, source] = 1
    assert np.array_equal(result.conj().T @ result, np.eye(32))
    return result


def cyclotomic_add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def cyclotomic_multiply(left, right):
    # Q(omega), omega=exp(i*pi/4), with omega^4=-1.
    result = [Fraction(0)] * 4
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            power = i + j
            result[power % 4] += a * b * (-1 if power >= 4 else 1)
    return tuple(result)


def exact_fresh_and_proof(array):
    zero = (Fraction(0),) * 4
    one = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    omega = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    omega_inverse = (Fraction(0), Fraction(0), Fraction(0), Fraction(-1))
    imaginary = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
    minus_imaginary = tuple(-coefficient for coefficient in imaginary)
    half_root = (Fraction(0), Fraction(1, 2), Fraction(0), Fraction(-1, 2))
    assert cyclotomic_multiply(half_root, half_root) == (
        Fraction(1, 2),
        Fraction(0),
        Fraction(0),
        Fraction(0),
    )
    assert cyclotomic_multiply(omega, omega_inverse) == one
    rows = []
    assert array.shape == (10, 5)
    assert array[-1].tolist() == [4, 5, -1, -1, -1]
    for a, b in product((0, 1), repeat=2):
        amplitudes = [one, zero]
        before_correction = None
        for index, (code, first, second, condition, register) in enumerate(array.tolist()):
            assert condition == register == -1
            if code == 1:
                assert first == 5 and second == -1
                s0, s1 = amplitudes
                amplitudes = [
                    cyclotomic_multiply(half_root, cyclotomic_add(s0, s1)),
                    cyclotomic_multiply(half_root, cyclotomic_add(s0, tuple(-item for item in s1))),
                ]
            elif code in (2, 3, 4):
                assert first == 5 and second == -1
                phase = {2: omega, 3: omega_inverse, 4: minus_imaginary}[code]
                if code == 4:
                    before_correction = list(amplitudes)
                    expected_phase = imaginary if a & b else one
                    assert amplitudes[a & b] == expected_phase and amplitudes[1 - (a & b)] == zero
                amplitudes[1] = cyclotomic_multiply(amplitudes[1], phase)
            elif code == 5:
                assert first in (0, 1) and second == 5
                if (a, b)[first]:
                    amplitudes.reverse()
            else:
                raise AssertionError(("Unexpected fresh-AND primitive", index, code))
        assert amplitudes[a & b] == one and amplitudes[1 - (a & b)] == zero
        assert before_correction is not None
        rows.append(
            dict(
                a=a,
                b=b,
                target=a & b,
                exact_pre_Sdag_nonzero_amplitude_coefficients=[
                    [item.numerator, item.denominator] for item in before_correction[a & b]
                ],
                exact_final_nonzero_amplitude_coefficients=[
                    [item.numerator, item.denominator] for item in amplitudes[a & b]
                ],
            )
        )
    return rows


def exact_algebra(dynamic_array):
    phase_rows = exact_fresh_and_proof(dynamic_array[:10])
    boolean_rows = []
    for word in range(32):
        a, b, c, old_sum, old_carry = ((word >> bit) & 1 for bit in range(5))
        first = a & b
        temporary_b = a ^ b
        second = temporary_b & c
        carry = old_carry ^ first ^ second
        total = old_sum ^ temporary_b ^ c
        restored_b = temporary_b ^ a
        assert restored_b == b
        assert (a ^ b ^ c) == (a + b + c) % 2
        assert (first ^ second) == (a + b + c) // 2
        output = a + 2 * restored_b + 4 * c + 8 * total + 16 * carry
        boolean_rows.append(dict(input_word=word, output_word=output, inputs_restored=True))
    assert len({row["output_word"] for row in boolean_rows}) == 32
    return dict(
        formal_proof_uses_floating_tolerance=False,
        exact_cyclotomic_field="Q(omega), omega=exp(i*pi/4), omega^4=-1; sqrt(2)=omega-omega^3",
        exact_H_factor_coefficients=[[0, 1], [1, 2], [0, 1], [-1, 2]],
        exact_single_cleanup_amplitude="(omega-omega^3)/2=1/sqrt(2)",
        exact_two_cleanup_amplitude=[1, 2],
        exact_fresh_AND_phase_rows=phase_rows,
        exact_dirty_output_Boolean_permutation_rows=boolean_rows,
        primary_paper_title="Halving the cost of quantum addition",
        primary_paper_URL="https://arxiv.org/pdf/1709.06648v3",
        primary_paper_Figure=3,
        primary_pdf_sha256=sha(PRIMARY),
        exact_fresh_AND_isometry=(
            "The four-T relative-phase circuit followed by Sdag(t) sends |a,b,0> "
            "to |a,b,a*b> with phase1 for every a,b. Before Sdag the only nontrivial "
            "fresh-target phase is i on a=b=1. It is not a full Toffoli on dirty targets."
        ),
        exact_cleanup_Kraus_identity=(
            "H then measurement outcome m on |a*b> gives (-1)^(m*a*b)/sqrt(2). "
            "CZ(a,b)^m cancels that sign, and X(t)^m resets the measured target. "
            "Every corrected branch is exactly I/sqrt(2) on inputs and any untouched "
            "entangled output/reference; the outcome is independent of quantum input."
        ),
        fulladder_boolean_identity=(
            "a+b+c = (a XOR b XOR c) + 2*((a AND b) XOR ((a XOR b) AND c)). "
            "Compute both ANDs into fresh scratch, XOR them into dirty carry, XOR "
            "a XOR b XOR c into dirty sum. Erase second AND with current b'=a XOR b; "
            "restore b, then erase first AND with original a,b."
        ),
        fulladder_exact_channel_derivation=(
            "Each cleanup contributes input-independent1/sqrt(2); four full branches "
            "have K_(m0,m1)=U/2 including scratch-zero output. Therefore their probabilities "
            "are exactly1/4 and sum K rho Kdag = U rho Udag, including arbitrary "
            "superposition or external-reference entanglement. Kraus verification checks "
            "input phases; basis permutations alone would be insufficient."
        ),
        measurement_feedback_and_reset_are_charged=True,
        ancillary_initial_zero_is_required=True,
        full_financial_compute_inverse_replacement_authorized_by_this_fragment=False,
        nonunitary_cleanup_is_not_literal_circuit_inverse=True,
    )


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    assert not output.exists()
    assert PRIMARY.read_bytes().startswith(b"%PDF")
    inputs = [RESEARCH / name for name in CODE] + [PRIMARY, Path(sys.executable)]
    package = Path(np.__file__).parent
    numpy_sources = [
        path
        for path in package.rglob("*")
        if path.is_file() and path.suffix in (".py", ".pyd") and "tests" not in path.parts
    ]
    inputs += numpy_sources
    frozen = {relative(path): sha(path) for path in inputs}
    verify(frozen)
    output.mkdir()
    for path in (RESEARCH / name for name in CODE):
        shutil.copy2(path, output / path.name)
    shutil.copy2(PRIMARY, output / PRIMARY.name)
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_tests_gate_arrays_channel_or_resources=True,
            frozen_inputs=frozen,
            interpreter=sys.executable,
            numpy_version=np.__version__,
            numpy_source_and_extension_files=len(numpy_sources),
            numerical_threads_per_process=1,
            fixed_candidates=1,
            fixed_dynamic_fragment="Five logical wires plus two fresh-zero AND ancillas; two corrected X-basis cleanup measurements",
            fixed_paid_unitary_control="Same Boolean fulladder with four actual seven-T Toffoli decompositions, including compute and cleanup",
            fixed_gate_schedule="One fully serial gate/measurement/feedforward sequence; charge all conditional CZ/reset slots worst-case",
            logical_wires=dict(a=0, b=1, c=2, dirty_sum=3, dirty_carry=4),
            fresh_scratch_wires=[5, 6],
            input_logical_basis_columns=32,
            dirty_output_word_patterns=4,
            fixed_measurement_outcomes=[[0, 0], [0, 1], [1, 0], [1, 1]],
            measurement_order=[1, 0],
            classical_result_registers=2,
            scratch_initialization_required=True,
            candidate_array_encoding=[
                "opcode",
                "q0",
                "q1_or_minus1",
                "condition_value_or_minus1",
                "classical_register_or_minus1",
            ],
            opcode_binding={"H": 1, "T": 2, "Tdg": 3, "Sdg": 4, "CX": 5, "CZ": 6, "MZ": 7, "X": 8},
            numeric_matrix_tolerance=1e-12,
            declared_unique_tests=FIXTURES,
            independent_verifier="Explicit dense Kronecker gates/projectors, independent from vectorized producer gate evaluator; exact cleanup algebra also recorded",
            entangled_reference_dimension=32,
            process_CPU_limit_seconds=CPU_LIMIT,
            physical_feedback_clock_routing_factory_seconds=None,
            integrated_financial_compiler_cost=None,
            new_financial_gates_prices_or_observations=0,
            full_financial_error_or_advantage_claim=False,
        ),
    )
    print("A16 one-fragment channel protocol prospectively frozen", flush=True)


def run(output):
    started = time.process_time()
    output = Path(output).resolve()
    assert not (output / "summary.json").exists()
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    rc = pytest.main(
        [
            str(RESEARCH / "test_temporary_and_fulladder.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    xml = ET.parse(output / "tests.xml").getroot()
    cases = list(xml.iter("testcase"))
    assert rc == 0 and len(cases) == FIXTURES
    assert len({(item.attrib.get("classname"), item.attrib["name"]) for item in cases}) == FIXTURES
    assert (
        not list(xml.iter("failure"))
        and not list(xml.iter("error"))
        and not list(xml.iter("skipped"))
    )
    assert time.process_time() - started < CPU_LIMIT
    arrays = {}
    for name, measured in (("dynamic", True), ("unitary_control", False)):
        path = output / (name + ".npy")
        np.save(path, encode(fulladder_schedule(measured=measured)), allow_pickle=False)
        arrays[name] = np.load(path, allow_pickle=False)
    contract = independent_contract()
    injection = np.zeros((128, 32), dtype=np.complex128)
    injection[:32] = np.eye(32)
    expected = injection @ contract
    independent_rows = []
    kraus = []
    for outcomes in product((0, 1), repeat=2):
        columns = independent_columns(arrays["dynamic"], outcomes, injection)
        independently_targeted_error = float(np.max(np.abs(columns - expected / 2)))
        producer_columns = run_columns(decode(arrays["dynamic"]), injection, outcomes)
        crosscheck = float(np.max(np.abs(columns - producer_columns)))
        assert independently_targeted_error < 1e-12 and crosscheck < 1e-12
        active = columns[:32]
        assert np.max(np.abs(columns[32:])) < 1e-12
        # All32 EPR columns verify the arbitrary-reference channel via vec(K).
        epr_error = float(
            np.max(
                np.abs(columns.reshape(-1) / np.sqrt(32) - expected.reshape(-1) / (2 * np.sqrt(32)))
            )
        )
        assert epr_error < 1e-12
        independent_rows.append(
            dict(
                outcomes=list(outcomes),
                input_columns_checked=32,
                branch_scalar_exact=[1, 2],
                branch_probability_exact=[1, 4],
                maximum_dense_matrix_error=independently_targeted_error,
                maximum_vectorized_crosscheck_error=crosscheck,
                maximum_entangled_reference_error=epr_error,
                scratch_output_zero=True,
            )
        )
        kraus.append(active)
        assert time.process_time() - started < CPU_LIMIT
    np.save(output / "independent_logical_kraus.npy", np.asarray(kraus), allow_pickle=False)
    control = independent_columns(arrays["unitary_control"], (0, 0), injection)
    control_error = float(np.max(np.abs(control - expected)))
    assert control_error < 1e-12 and np.max(np.abs(control[32:])) < 1e-12
    np.save(output / "independent_control_unitary.npy", control[:32], allow_pickle=False)
    assert (
        np.max(
            np.abs(
                sum((matrix.conj().T @ matrix for matrix in kraus), np.zeros((32, 32))) - np.eye(32)
            )
        )
        < 1e-12
    )
    source_certificate, _ = channel_certificate(decode(arrays["dynamic"]))
    save(output / "exact_channel_derivation.json", exact_algebra(arrays["dynamic"]))
    save(
        output / "channel_certificate.json",
        dict(
            independent_full_dense_matrix_rows=independent_rows,
            vectorized_channel_check=source_certificate,
            independent_paid_control_error=control_error,
            all_four_corrected_branches_K_equals_U_over_2=True,
            joint_channel_preserves_entangled_arbitrary_inputs=True,
            dirty_sum_and_carry_tested=True,
            numeric_matrix_tolerance=1e-12,
        ),
    )
    dynamic_resources = resources(decode(arrays["dynamic"]))
    control_resources = resources(decode(arrays["unitary_control"]))
    assert dynamic_resources["T_count"] == 8 and control_resources["T_count"] == 28
    assert dynamic_resources["X_basis_measurements"] == 2
    assert dynamic_resources["conditional_CZ_scheduled_slots"] == 2
    assert dynamic_resources["conditional_X_reset_scheduled_slots"] == 2
    save(
        output / "resource_ledger.json",
        dict(
            dynamic=dynamic_resources,
            unitary_control=control_resources,
            actual_array_sha256={name: sha(output / (name + ".npy")) for name in arrays},
            T_count_saved=20,
            logical_fragment_T_count_reduction=True,
            actual_physical_time_saved=None,
            financial_compiler_integration=None,
            financial_estimator_error_or_cost_changed=False,
        ),
    )
    verify(protocol["frozen_inputs"])
    assert time.process_time() - started < CPU_LIMIT
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            fixtures_passed=FIXTURES,
            fixed_dynamic_candidates=1,
            fixed_paid_unitary_controls=1,
            actual_saved_gate_arrays=2,
            independently_verified_measurement_branches=4,
            logical_basis_columns_per_branch=32,
            verified_dirty_output_patterns=4,
            independent_entangled_reference_dimension=32,
            exact_cleanup_algebra_and_actual_matrix_channels_agree=True,
            dynamic_T_count=8,
            unitary_control_compute_and_cleanup_T_count=28,
            dynamic_fresh_scratch_qubits=2,
            dynamic_X_basis_measurements=2,
            dynamic_feedback_CZ_scheduled_slots=2,
            dynamic_conditional_X_reset_slots=2,
            dynamic_fixed_serial_T_depth=8,
            unitary_fixed_serial_T_depth=28,
            measurement_feedback_reset_physical_seconds=None,
            routing_clock_factory_or_runtime_seconds=None,
            financial_compiler_integration=None,
            changed_existing_financial_circuits=False,
            new_financial_prices_or_observations=0,
            full_financial_error_certificate=False,
            quantum_advantage_claim=False,
            elapsed_process_CPU_seconds=time.process_time() - started,
        ),
    )
    finish_manifest(output)
    print("A16 isolated fulladder actual-channel experiment PASS", flush=True)


def finish_manifest(output):
    save(
        output / "manifest.json",
        dict(
            files={relative(path): sha(path) for path in output.rglob("*") if path.is_file()},
            frozen_inputs=read(output / "protocol.json")["frozen_inputs"],
            manifest_self_hash_excluded=True,
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=PROGRAM / "A16_dynamic_run001")
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.output)
    else:
        try:
            run(args.output)
        except BaseException as error:
            output = args.output.resolve()
            (output / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
            save(
                output / "summary.json",
                dict(
                    passed=False,
                    local_only=True,
                    failure_type=type(error).__name__,
                    message=str(error),
                    fixed_dynamic_candidates=1,
                    new_financial_prices_or_observations=0,
                    changed_existing_financial_circuits=False,
                    quantum_advantage_claim=False,
                ),
            )
            finish_manifest(output)
            raise
