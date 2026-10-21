"""One fresh-ancilla measured fulladder fragment and its paid unitary control.

Five logical wires preserve a,b,c and XOR their sum/carry into arbitrary
outputs. Two scratch wires are fresh zero. Every measurement result is
retained and its conditional CZ and X reset are included in the schedule.
This is an isolated channel experiment, not a financial compiler rewrite.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import product

import numpy as np

OPCODES = {"H": 1, "T": 2, "Tdg": 3, "Sdg": 4, "CX": 5, "CZ": 6, "MZ": 7, "X": 8}
GATES = {value: key for key, value in OPCODES.items()}
QUBITS = 7
LOGICAL_QUBITS = 5
SCRATCH = (5, 6)


@dataclass(frozen=True)
class Operation:
    gate: str
    wires: tuple[int, ...]
    condition_value: int = -1
    classical_register: int = -1

    def __post_init__(self):
        if self.gate not in OPCODES:
            raise ValueError("Unsupported exact Clifford/T/measurement operation")
        expected = 2 if self.gate in ("CX", "CZ") else 1
        if len(self.wires) != expected or len(set(self.wires)) != len(self.wires):
            raise ValueError("Distinct wires and gate arity required")
        if any(type(wire) is not int or not 0 <= wire < QUBITS for wire in self.wires):
            raise ValueError("Seven-wire fragment required")
        if self.gate == "MZ":
            if self.condition_value != -1 or self.classical_register not in (0, 1):
                raise ValueError("Unconditional measurement needs its result register")
        elif self.condition_value == -1:
            if self.classical_register != -1:
                raise ValueError("Unconditional gate has no classical dependency")
        elif self.condition_value != 1 or self.classical_register not in (0, 1):
            raise ValueError("Only outcome-one feedforward is used")


def gate(name, *wires, result=-1, condition=-1):
    return Operation(name, tuple(wires), condition, result)


def and_compute(a, b, target):
    """Four T/Tdag gates: exact AND isometry only for target initially zero."""
    return [
        gate("H", target),
        gate("T", target),
        gate("CX", b, target),
        gate("Tdg", target),
        gate("CX", a, target),
        gate("T", target),
        gate("CX", b, target),
        gate("Tdg", target),
        gate("H", target),
        gate("Sdg", target),
    ]


def and_cleanup(a, b, target, result):
    return [
        gate("H", target),
        gate("MZ", target, result=result),
        gate("CZ", a, b, result=result, condition=1),
        gate("X", target, result=result, condition=1),
    ]


def ccx_seven_t(a, b, target):
    """Exact full Toffoli, including its control-wire phase corrections."""
    return [
        gate("H", target),
        gate("CX", b, target),
        gate("Tdg", target),
        gate("CX", a, target),
        gate("T", target),
        gate("CX", b, target),
        gate("Tdg", target),
        gate("CX", a, target),
        gate("T", b),
        gate("T", target),
        gate("H", target),
        gate("CX", a, b),
        gate("T", a),
        gate("Tdg", b),
        gate("CX", a, b),
    ]


def fulladder_schedule(*, measured):
    a, b, c, total, carry, first, second = range(QUBITS)
    operations = []
    compute = and_compute if measured else ccx_seven_t
    operations.extend(compute(a, b, first))
    operations.append(gate("CX", a, b))
    operations.extend(compute(b, c, second))
    operations.extend(
        [
            gate("CX", first, carry),
            gate("CX", second, carry),
            gate("CX", b, total),
            gate("CX", c, total),
        ]
    )
    operations.extend(and_cleanup(b, c, second, 1) if measured else ccx_seven_t(b, c, second))
    operations.append(gate("CX", a, b))
    operations.extend(and_cleanup(a, b, first, 0) if measured else ccx_seven_t(a, b, first))
    return operations


def encode(operations):
    """Actual fixed schedule: opcode,q0,q1,condition_value,classical_register."""
    return np.asarray(
        [
            [
                OPCODES[op.gate],
                op.wires[0],
                op.wires[1] if len(op.wires) == 2 else -1,
                op.condition_value,
                op.classical_register,
            ]
            for op in operations
        ],
        dtype=np.int16,
    )


def decode(array):
    if array.dtype != np.dtype(np.int16) or array.ndim != 2 or array.shape[1] != 5:
        raise ValueError("Signed-int16 five-column schedule required")
    operations = []
    for code, first, second, condition, result in array.tolist():
        if code not in GATES:
            raise ValueError("Unknown primitive opcode")
        wires = (first,) if second == -1 else (first, second)
        operations.append(Operation(GATES[code], wires, condition, result))
    return operations


def apply(operation, columns, outcomes):
    """Apply one saved primitive to every input column, without normalization."""
    if operation.condition_value >= 0:
        if outcomes[operation.classical_register] != operation.condition_value:
            return columns
    dimension = columns.shape[0]
    if dimension != 1 << QUBITS:
        raise ValueError("Full seven-wire column array required")
    indices = np.arange(dimension)
    first = operation.wires[0]
    mask = 1 << first
    bit = (indices & mask) != 0
    if operation.gate == "MZ":
        result = columns.copy()
        result[bit != bool(outcomes[operation.classical_register])] = 0
        return result
    if operation.gate in ("CX", "X"):
        flip = (
            np.full(dimension, mask)
            if operation.gate == "X"
            else np.where(bit, 1 << operation.wires[1], 0)
        )
        return columns[indices ^ flip].copy()
    if operation.gate == "H":
        zero = indices[~bit]
        one = zero | mask
        result = columns.copy()
        result[zero] = (columns[zero] + columns[one]) / np.sqrt(2)
        result[one] = (columns[zero] - columns[one]) / np.sqrt(2)
        return result
    if operation.gate == "CZ":
        phase = np.where(bit & ((indices & (1 << operation.wires[1])) != 0), -1, 1)
    else:
        value = {"T": np.exp(1j * np.pi / 4), "Tdg": np.exp(-1j * np.pi / 4), "Sdg": -1j}[
            operation.gate
        ]
        phase = np.where(bit, value, 1)
    return phase[:, None] * columns


def run_columns(operations, columns, outcomes=(0, 0)):
    if len(outcomes) != 2 or any(type(bit) is not int or bit not in (0, 1) for bit in outcomes):
        raise ValueError("Two declared binary measurement outcomes required")
    value = np.asarray(columns, dtype=np.complex128)
    if value.ndim != 2 or value.shape[0] != 1 << QUBITS:
        raise ValueError("Two-dimensional full seven-wire columns required")
    observed = set()
    for operation in operations:
        if operation.condition_value >= 0 and operation.classical_register not in observed:
            raise ValueError("Feedback requires an earlier actual measurement")
        if operation.gate == "MZ":
            if operation.classical_register in observed:
                raise ValueError("Classical result register reused")
            observed.add(operation.classical_register)
        value = apply(operation, value, outcomes)
    return value


def logical_injection():
    value = np.zeros((1 << QUBITS, 1 << LOGICAL_QUBITS), dtype=np.complex128)
    value[: 1 << LOGICAL_QUBITS] = np.eye(1 << LOGICAL_QUBITS)
    return value


def expected_logical_permutation():
    """Independent arithmetic contract; both output bits may start dirty."""
    value = np.zeros((32, 32), dtype=np.complex128)
    for word in range(32):
        bits = [(word >> bit) & 1 for bit in range(5)]
        integer_total = sum(bits[:3])
        bits[3] ^= integer_total % 2
        bits[4] ^= integer_total // 2
        output = sum(bit << index for index, bit in enumerate(bits))
        value[output, word] = 1
    return value


def resources(operations):
    """Counts include worst-case scheduled conditional CZ and X reset slots."""
    count = Counter(op.gate for op in operations)
    t_count = count["T"] + count["Tdg"]

    def branch_counts(name):
        return {
            "".join(map(str, bits)): sum(
                op.gate == name and op.condition_value == 1 and bits[op.classical_register] == 1
                for op in operations
            )
            for bits in product((0, 1), repeat=2)
        }

    return dict(
        logical_qubits=LOGICAL_QUBITS,
        fresh_scratch_qubits=len(SCRATCH),
        total_logical_qubits=QUBITS,
        primitive_counts=dict(sorted(count.items())),
        T_count=t_count,
        T_depth=t_count,
        T_depth_schedule=(
            "One fixed fully serial primitive schedule; no parallel gate scheduling claim"
        ),
        serial_Clifford_T_operation_slots=len(operations) - count["MZ"],
        fixed_serial_operation_slots=len(operations),
        X_basis_measurements=count["MZ"],
        conditional_CZ_scheduled_slots=sum(
            op.gate == "CZ" and op.condition_value == 1 for op in operations
        ),
        conditional_X_reset_scheduled_slots=sum(
            op.gate == "X" and op.condition_value == 1 for op in operations
        ),
        measurement_feedforward_rounds=count["MZ"],
        branch_CZ_execution_counts=branch_counts("CZ"),
        branch_X_reset_execution_counts=branch_counts("X"),
        classical_result_bits=count["MZ"],
        physical_measurement_feedback_reset_seconds=None,
        physical_routing_factory_or_execution_seconds=None,
        integrated_financial_compiler_cost=None,
    )


def channel_certificate(operations):
    expected = expected_logical_permutation()
    injection = logical_injection()
    full_target = injection @ expected
    rows = []
    kraus = []
    for outcomes in product((0, 1), repeat=2):
        columns = run_columns(operations, injection, outcomes)
        active = columns[:32]
        scalar = np.vdot(expected, active) / 32
        residual = float(np.max(np.abs(columns - scalar * full_target)))
        cleanup = float(np.max(np.abs(columns[32:])))
        probability_deviation = float(np.max(np.abs(active.conj().T @ active - np.eye(32) / 4)))
        assert residual < 1e-12 and cleanup < 1e-12 and probability_deviation < 1e-12
        assert abs(abs(scalar) - 0.5) < 1e-12
        # Vectorization is the action on one half of a maximally entangled state.
        entangled = columns.reshape(-1) / np.sqrt(32)
        expected_entangled = (scalar * full_target).reshape(-1) / np.sqrt(32)
        assert np.max(np.abs(entangled - expected_entangled)) < 1e-12
        rows.append(
            dict(
                outcomes=list(outcomes),
                input_columns_checked=32,
                input_independent_branch_scalar_real=float(scalar.real),
                input_independent_branch_scalar_imag=float(scalar.imag),
                expected_probability_exact=[1, 4],
                maximum_channel_column_error=residual,
                maximum_scratch_cleanup_error=cleanup,
                maximum_branch_probability_error=probability_deviation,
                maximally_entangled_reference_dimension=32,
            )
        )
        kraus.append(active)
    completeness = sum(
        (matrix.conj().T @ matrix for matrix in kraus), np.zeros((32, 32), dtype=np.complex128)
    )
    assert np.max(np.abs(completeness - np.eye(32))) < 1e-12
    # Every branch is a scalar times the same U, including its input phases.
    # Linearity proves the joint channel U tensor I for any reference/input.
    return dict(
        branch_rows=rows,
        maximum_completeness_error=float(np.max(np.abs(completeness - np.eye(32)))),
        channel_identity_for_all_dirty_output_columns=True,
        arbitrary_superposition_and_entangled_reference_follows_from_Kraus_identity=True,
        global_phase_may_depend_on_branch_but_not_input=True,
        truth_table_only_check=False,
        numeric_matrix_tolerance=1e-12,
        mathematical_channel_contract=(
            "K_m=exp(i*theta_m)*U/2, for all four outcomes and all32 logical basis "
            "columns; scratch outputs are zero. Sum_m K_m rho K_m^dagger=U rho U^dagger, "
            "also when rho is entangled with any external reference."
        ),
    ), kraus
