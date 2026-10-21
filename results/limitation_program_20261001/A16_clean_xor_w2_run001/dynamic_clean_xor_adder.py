"""Fixed two-bit clean-XOR measured adder and its direct unitary control.

Both inputs survive, the arbitrary output is XORed with (a+b) modulo four,
and every fresh temporary is reset. The four-T AND is used only on a fresh
target. This new dynamic representation is not the native X/CX/CCX backend.
"""

from __future__ import annotations

from collections import Counter

import numpy as np

from research.limitation_program_20261001.direct_fulladder_control import exact_ccx_proof
from research.limitation_program_20261001.experiment_temporary_and_fulladder import (
    exact_fresh_and_proof,
)
from research.limitation_program_20261001.temporary_and_fulladder import (
    and_compute,
    ccx_seven_t,
    encode,
)

WIDTH = 2
LOGICAL_QUBITS = 6
QUBITS = 10
SCRATCH = (6, 7, 8, 9)
NAMES = {1: "H", 2: "T", 3: "Tdg", 4: "Sdg", 5: "CX", 6: "CZ", 7: "MZ", 8: "X"}


def _row(code, first, second=-1, condition=-1, register=-1):
    return [code, first, second, condition, register]


def _mapped(array, mapping):
    result = array.copy()
    for row in result:
        row[1] = mapping[int(row[1])]
        if row[2] >= 0:
            row[2] = mapping[int(row[2])]
    return result


def measured_schedule(width=WIDTH):
    if type(width) is not int or width != WIDTH:
        raise ValueError("Only the declared two-bit experiment is implemented")
    # a=(0,1), b=(2,3), arbitrary out=(4,5), fresh p=(6,7), g0=8,c1=9.
    rows = [_row(5, 0, 6), _row(5, 2, 6), _row(5, 1, 7), _row(5, 3, 7)]
    rows.extend(_mapped(encode(and_compute(0, 1, 5)), {0: 0, 1: 2, 5: 8}).tolist())
    rows.extend([_row(5, 8, 9), _row(5, 6, 4), _row(5, 7, 5), _row(5, 9, 5)])
    rows.append(_row(5, 8, 9))
    rows.extend([_row(1, 8), _row(7, 8, register=0), _row(6, 0, 2, 1, 0), _row(8, 8, -1, 1, 0)])
    rows.extend([_row(5, 3, 7), _row(5, 1, 7), _row(5, 2, 6), _row(5, 0, 6)])
    result = np.asarray(rows, dtype=np.int16)
    validate_array(result)
    return result


def direct_schedule():
    rows = [_row(5, 0, 4), _row(5, 2, 4), _row(5, 1, 5), _row(5, 3, 5)]
    rows.extend(encode(ccx_seven_t(0, 2, 5)).tolist())
    result = np.asarray(rows, dtype=np.int16)
    validate_array(result)
    return result


def validate_array(array):
    if array.dtype != np.dtype(np.int16) or array.ndim != 2 or array.shape[1] != 5:
        raise ValueError("Signed int16 five-column primitive array required")
    measured = set()
    for code, first, second, condition, register in array.tolist():
        if code not in NAMES or not 0 <= first < QUBITS:
            raise ValueError("Invalid opcode or unallocated first wire")
        if code in (5, 6):
            if not 0 <= second < QUBITS or first == second:
                raise ValueError("Distinct allocated control and target required")
        elif second != -1:
            raise ValueError("Single-qubit gate has no second wire")
        if code == 7:
            if condition != -1 or register != 0 or register in measured:
                raise ValueError("Exactly one fresh result register is available")
            measured.add(register)
        elif condition == -1:
            if register != -1:
                raise ValueError("Unconditional gate has no classical dependency")
        elif condition != 1 or register not in measured or code not in (6, 8):
            raise ValueError("Feedback must follow the declared measurement")
    return array


def logical_injection():
    result = np.zeros((1 << QUBITS, 1 << LOGICAL_QUBITS), dtype=np.complex128)
    result[: 1 << LOGICAL_QUBITS] = np.eye(1 << LOGICAL_QUBITS)
    return result


def expected_permutation():
    result = np.zeros((64, 64), dtype=np.complex128)
    for word in range(64):
        a, b, old_out = word & 3, (word >> 2) & 3, word >> 4
        destination = a | (b << 2) | ((old_out ^ ((a + b) & 3)) << 4)
        result[destination, word] = 1
    return result


def run_columns(array, columns, outcome=0):
    """Bit-index vectorized evaluator, keeping every branch unnormalized."""
    validate_array(array)
    if type(outcome) is not int or outcome not in (0, 1):
        raise ValueError("One binary measurement outcome required")
    value = np.asarray(columns, dtype=np.complex128)
    if value.ndim != 2 or value.shape[0] != 1 << QUBITS:
        raise ValueError("Full ten-qubit columns required")
    indices = np.arange(1 << QUBITS)
    for code, first, second, condition, register in array.tolist():
        if condition == 1 and outcome != 1:
            continue
        selected = ((indices >> first) & 1).astype(bool)
        if code == 7:
            value = value.copy()
            value[selected != bool(outcome)] = 0
        elif code in (5, 8):
            flip = np.where(selected, 1 << second, 0) if code == 5 else 1 << first
            value = value[indices ^ flip].copy()
        elif code == 1:
            zero = indices[~selected]
            one = zero | (1 << first)
            following = value.copy()
            following[zero] = (value[zero] + value[one]) / np.sqrt(2)
            following[one] = (value[zero] - value[one]) / np.sqrt(2)
            value = following
        else:
            if code == 6:
                phase = np.where(selected & (((indices >> second) & 1) != 0), -1, 1)
            else:
                phase = np.where(
                    selected, {2: (1 + 1j) / np.sqrt(2), 3: (1 - 1j) / np.sqrt(2), 4: -1j}[code], 1
                )
            value = phase[:, None] * value
    return value


def resources(array, *, measured):
    validate_array(array)
    counts = Counter(NAMES[int(row[0])] for row in array)
    if type(measured) is not bool or measured != bool(counts["MZ"]):
        raise ValueError("Resource freshness flag must match actual measurements")
    tcount = counts["T"] + counts["Tdg"]
    return dict(
        logical_input_output_qubits=LOGICAL_QUBITS,
        comparison_ABI_allocated_qubits=QUBITS,
        active_primitive_support_qubits=QUBITS if measured else LOGICAL_QUBITS,
        fresh_scratch_required=len(SCRATCH) if measured else 0,
        primitive_counts=dict(sorted(counts.items())),
        T_count=tcount,
        T_depth=tcount,
        schedule="Fixed fully serial primitive schedule",
        fixed_serial_operation_slots=len(array),
        Clifford_T_slots=len(array) - counts["MZ"],
        X_basis_measurements=counts["MZ"],
        feedback_CZ_slots=counts["CZ"] if measured else 0,
        conditional_reset_X_slots=counts["X"] if measured else 0,
        classical_result_bits=1 if measured else 0,
        physical_measurement_feedback_routing_clock_seconds=None,
    )


def exact_fixed_contract(measured, direct):
    """Bind actual fixed macros to the previously certified exact AND and CCX."""
    assert np.array_equal(measured, measured_schedule())
    assert np.array_equal(direct, direct_schedule())
    # The saved macro's original a,b,t wires are 0,1,5, as required by its proof.
    phase_rows = exact_fresh_and_proof(encode(and_compute(0, 1, 5)))
    direct_phase_rows = exact_ccx_proof()
    boolean_rows = []
    for word in range(64):
        a0, a1, b0, b1, out0, out1 = ((word >> bit) & 1 for bit in range(6))
        p0, p1 = a0 ^ b0, a1 ^ b1
        g0 = a0 & b0
        c1 = g0
        new0, new1 = out0 ^ p0, out1 ^ p1 ^ c1
        assert (p0 | ((p1 ^ c1) << 1)) == ((a0 + 2 * a1 + b0 + 2 * b1) & 3)
        c1 ^= g0
        assert c1 == 0
        assert (p0 ^ b0 ^ a0) == (p1 ^ b1 ^ a1) == 0
        target = a0 | (a1 << 1) | (b0 << 2) | (b1 << 3) | (new0 << 4) | (new1 << 5)
        boolean_rows.append(dict(input_word=word, output_word=target, temporaries_clean=True))
    return dict(
        exact_fresh_AND_phase_rows=phase_rows,
        exact_direct_dirty_target_CCX_rows=direct_phase_rows,
        exact_all64_dirty_output_columns=boolean_rows,
        formal_proof_uses_floating_tolerance=False,
        fresh_p_g_c_lifetimes=(
            "p and original a,b survive their dependent AND cleanup; "
            "c1 is cleared before g0 cleanup; p is erased last"
        ),
        corrected_branch_Kraus_identity="K_0=K_1=U/sqrt(2), exactly; scratch returns zero",
        outcome_probability_exact=[1, 2],
        measurement_record_independent_of_input_and_external_reference=True,
        measurement_record_retained_not_coherently_uncomputed=True,
        channel_adjoint_contract=(
            "U is a clean-XOR self-inverse. Its adjoint channel is implemented by this same "
            "forward schedule with fresh zero scratch; a literal reversal of measurements "
            "is invalid."
        ),
        channel_adjoint_uses_a_fresh_classical_result_bit=True,
        native72_emitted_or_integrated=False,
    )


def arbitrary_width_lemma():
    """Analytic recipe only; no generic-width circuit is emitted or cost adopted."""
    return dict(
        domain="Integer width w>=2, modular clean-XOR output, preserved inputs, fresh scratch",
        forward=(
            "Prepare p_i=a_i XOR b_i. For i=0..w-2 prepare fresh g_i=a_i AND b_i; "
            "for i>0 prepare fresh h_i=p_i AND c_i. Set fresh c_(i+1)=g_i XOR h_i, with c0=0. "
            "Output_i XOR= p_i XOR c_i. No final overflow carry or g_(w-1)/h_(w-1) is produced."
        ),
        carry_identity=(
            "g_i*h_i=0 because g_i=1 implies p_i=0; therefore g_i XOR h_i equals their OR, "
            "the ordinary binary carry. p_i XOR c_i is the corresponding sum bit."
        ),
        reverse_lifetimes=(
            "Descending i, clear c_(i+1) with the live g_i/h_i, then erase h_i with live p_i/c_i, "
            "erase g_i with original a_i/b_i, and erase p_i only after its last dependent cleanup."
        ),
        AND_count_expression="N=1+2*(w-2)=2w-3",
        T_count_expression="4N=8w-12 for this recipe only",
        fresh_scratch_expression="w p + (w-1) g + (w-2) h + (w-1) carry = 4w-4",
        all_histories_Kraus_identity=(
            "K_m=2^(-N/2)*U; every m has input-independent probability 2^(-N)"
        ),
        arbitrary_entanglement_supported_by_linearity=True,
        clean_XOR_self_inverse_adjoint_requires_fresh_scratch=True,
        channel_adjoint_requires_new_measurement_records=True,
        no_generic_width_circuit_emitted=True,
        no_native72_resources_credited=True,
        no_unitary_optimality_theorem=True,
        backend_obligation=(
            "The current native Program.undo reverses X/CX/CCX arrays. Measurement-based "
            "erasure needs a separate dynamic channel/adjoint ABI and cannot be inserted "
            "into that literal reversal."
        ),
    )
