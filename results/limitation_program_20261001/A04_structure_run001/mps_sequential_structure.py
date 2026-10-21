"""Sequential MPS wire structure; numerical diagnostics are not certificates.

The emission interface fixes the basis order and removes inactive bond wires
structurally.  No Gaussian table, compression, synthesis, or financial circuit
is evaluated here.  Local unitary completion and SDK decomposition residuals
must be charged by a later interval certificate before loader adoption.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from importlib.metadata import version
import math
from typing import Sequence

import numpy as np


MAX_SITES = 10
MAX_BOND = 8
RANK_TOLERANCE = 1e-12


@dataclass(frozen=True)
class CanonicalMPS:
    cores: tuple[np.ndarray, ...]
    initial_normalizer: float
    final_gauge_scalar: complex
    reconstruction_residual_numeric: float
    maximum_row_isometry_defect_numeric: float


@dataclass(frozen=True)
class Transition:
    site: int
    output_wire: int
    left_rank: int
    right_rank: int
    local_wires: tuple[int, ...]
    swap_before: tuple[int, int] | None
    newly_cleared_wire: int | None
    isometry_columns: np.ndarray
    matrix: np.ndarray
    completion_change_numeric: float
    unitary_defect_numeric: float


@dataclass(frozen=True)
class StructurePlan:
    transitions: tuple[Transition, ...]
    output_wires_msb_first: tuple[int, ...]
    bond_wires_low_bit_first: tuple[int, ...]
    num_wires: int
    required_initial_zero_wires: tuple[int, ...]
    final_bond_rank: int


@dataclass(frozen=True)
class Primitive:
    gate: str
    wires: tuple[int, ...]
    angle: Fraction | None = None


def _power_two(value):
    return type(value) is int and value > 0 and value & (value - 1) == 0


def validate_cores(cores: Sequence[np.ndarray], max_bond=MAX_BOND):
    if not _power_two(max_bond) or max_bond > MAX_BOND:
        raise ValueError("Power-of-two bond cap at most eight required")
    if not 1 <= len(cores) <= MAX_SITES:
        raise ValueError("Between one and ten physical sites required")
    checked, previous = [], 1
    for core in cores:
        value = np.asarray(core, dtype=np.complex128)
        if value.ndim != 3 or value.shape[1] != 2:
            raise ValueError("Each core must have shape(left,2,right)")
        left, _, right = map(int, value.shape)
        if left != previous or not (_power_two(left) and _power_two(right)):
            raise ValueError("Consecutive power-of-two bond dimensions required")
        if max(left, right) > max_bond or not (left <= 2 * right and right <= 2 * left):
            raise ValueError("Bond growth/shrink must be at most a factor of two")
        if not np.all(np.isfinite(value)):
            raise ValueError("Every real and imaginary core literal must be finite")
        checked.append(value.copy())
        previous = right
    if previous != 1:
        raise ValueError("The final bond dimension must be one")
    return tuple(checked)


def contract_mps(cores):
    """Lexicographic site order: first site is the most significant output."""
    checked = validate_cores(cores)
    state = checked[0][0]
    for core in checked[1:]:
        state = np.tensordot(state, core, axes=([-1], [0]))
    return state[..., 0].reshape(-1)


def _positive_diagonal_qr(matrix):
    q, r = np.linalg.qr(matrix, mode="reduced")
    diagonal = np.diag(r)
    if np.any(np.abs(diagonal) <= RANK_TOLERANCE):
        raise ValueError("Fixed rank threshold rejected a deficient isometry")
    phase = diagonal / np.abs(diagonal)
    return q * phase[np.newaxis, :], np.conjugate(phase)[:, np.newaxis] * r


def right_canonicalize(cores):
    """One normalization and one right-to-left QR pass; no rank adaptation."""
    checked = list(validate_cores(cores))
    original = contract_mps(checked)
    normalizer = float(np.linalg.norm(original))
    if not math.isfinite(normalizer) or normalizer <= RANK_TOLERANCE:
        raise ValueError("Fixed normalization rejected a zero or deficient state")
    checked[0] /= normalizer
    gauge_scalar = 1 + 0j
    for site in reversed(range(len(checked))):
        core = checked[site]
        left, _, right = core.shape
        # M = R^dagger Q^dagger; rows of Q^dagger are orthonormal.
        q, r = _positive_diagonal_qr(core.reshape(left, 2 * right).conjugate().T)
        checked[site] = q.conjugate().T.reshape(left, 2, right)
        gauge = r.conjugate().T
        if site:
            checked[site - 1] = np.tensordot(checked[site - 1], gauge, axes=([-1], [0]))
        else:
            gauge_scalar = complex(gauge[0, 0])
    defects = []
    for core in checked:
        rows = core.reshape(core.shape[0], -1)
        defects.append(float(np.linalg.norm(rows @ rows.conjugate().T - np.eye(len(rows)))))
    residual = float(np.linalg.norm(original / normalizer - contract_mps(checked)))
    return CanonicalMPS(tuple(checked), normalizer, gauge_scalar, residual, max(defects))


def complete_isometry(columns):
    """Fixed two-pass Gram-Schmidt, lexicographic completion, positive QR.

    The input columns are retained as a comparison target. Their numerical
    change and the returned matrix's finite-literal unitarity defect are saved;
    neither is declared rigorously zero.
    """
    columns = np.asarray(columns, dtype=np.complex128)
    if columns.ndim != 2 or not 1 <= columns.shape[1] <= columns.shape[0] <= 16:
        raise ValueError("At most sixteen-dimensional local isometry required")
    if not np.all(np.isfinite(columns)):
        raise ValueError("Finite local isometry literals required")
    size, retained = columns.shape
    basis = []

    def append(vector, required):
        value = vector.copy()
        for _ in range(2):
            for previous in basis:
                value -= previous * np.vdot(previous, value)
        norm = float(np.linalg.norm(value))
        if norm <= RANK_TOLERANCE:
            if required:
                raise ValueError("Fixed rank threshold rejected dependent input columns")
            return
        basis.append(value / norm)

    for index in range(retained):
        append(columns[:, index], True)
    for index in range(size):
        if len(basis) == size:
            break
        append(np.eye(size, dtype=complex)[:, index], False)
    if len(basis) != size:
        raise ValueError("Fixed lexicographic completion did not fill the local space")
    unitary, _ = _positive_diagonal_qr(np.column_stack(basis))
    change = float(np.linalg.norm(unitary[:, :retained] - columns))
    defect = float(np.linalg.norm(unitary.conjugate().T @ unitary - np.eye(size)))
    return unitary, change, defect


def transition_from_core(core, site, output_wire, bond_wires):
    """Local bit order is low bond bits followed by the physical output bit."""
    core = np.asarray(core, dtype=np.complex128)
    if core.ndim != 3 or core.shape[1] != 2:
        raise ValueError("Transition core must have shape(left,2,right)")
    left, _, right = map(int, core.shape)
    if not (_power_two(left) and _power_two(right)) or not (
        left <= 2 * right and right <= 2 * left
    ):
        raise ValueError("Supported adjacent power-of-two bond ranks required")
    bond_wires = tuple(bond_wires)
    wires = (output_wire,) + bond_wires
    if any(type(wire) is not int or wire < 0 for wire in wires) or len(set(wires)) != len(wires):
        raise ValueError("Output and bond wires must be distinct nonnegative integers")
    left_bits, right_bits = left.bit_length() - 1, right.bit_length() - 1
    if max(left_bits, right_bits) > len(bond_wires):
        raise ValueError("The fixed scratch register cannot hold this bond")
    columns = core.reshape(left, 2 * right).T.copy()
    matrix, change, defect = complete_isometry(columns)
    local_wires = bond_wires[:right_bits] + (output_wire,)
    swap = cleared = None
    if left == 2 * right:
        # Fresh output0 moves onto the retired high bond bit. All subsequent
        # local operations exclude it, even if their approximation is imperfect.
        cleared = bond_wires[left_bits - 1]
        swap = (cleared, output_wire)
    return Transition(
        site, output_wire, left, right, local_wires, swap, cleared,
        columns, matrix, change, defect,
    )


def make_structure_plan(canonical):
    cores = validate_cores(canonical.cores if isinstance(canonical, CanonicalMPS) else canonical)
    count = len(cores)
    largest = max(max(core.shape[0], core.shape[2]) for core in cores)
    scratch = tuple(range(count, count + largest.bit_length() - 1))
    outputs = tuple(reversed(range(count)))
    transitions = tuple(
        transition_from_core(core, site, output, scratch)
        for site, (core, output) in enumerate(zip(cores, outputs, strict=True))
    )
    return StructurePlan(
        transitions, outputs, scratch, count + len(scratch),
        tuple(range(count + len(scratch))), 1,
    )


def require_pinned_sdk():
    if np.__version__ != "1.26.4" or version("qiskit-terra") != "0.45.3":
        raise RuntimeError("Existing controlled_closeout_repro NumPy1.26.4/Qiskit0.45.3 required")


def decompose_plan(plan, maximum_local_calls=10, maximum_operations=20000):
    """One SDK decomposition per local unitary; no optimization or retries."""
    require_pinned_sdk()
    if len(plan.transitions) > maximum_local_calls:
        raise ValueError("Fixed local-decomposition call cap would be exceeded")
    from qiskit import QuantumCircuit, transpile
    from qiskit.circuit.library import UnitaryGate

    operations, local_records = [], []
    for transition in plan.transitions:
        if transition.swap_before is not None:
            operations.append(Primitive("swap", transition.swap_before))
        circuit = QuantumCircuit(len(transition.local_wires))
        circuit.append(UnitaryGate(transition.matrix, check_input=True), range(circuit.num_qubits))
        native = transpile(
            circuit, basis_gates=["ry", "rz", "cx"], optimization_level=0, seed_transpiler=0,
        )
        phase = Fraction.from_float(float(native.global_phase))
        if phase:
            operations.append(Primitive("phase", (), phase))
        start = len(operations)
        for item in native.data:
            gate = item.operation.name
            if gate not in ("ry", "rz", "cx"):
                raise ValueError("Fixed native basis produced an unsupported operation")
            wires = tuple(
                transition.local_wires[native.find_bit(qubit).index] for qubit in item.qubits
            )
            angle = Fraction.from_float(float(item.operation.params[0])) if gate != "cx" else None
            operations.append(Primitive(gate, wires, angle))
        local_records.append(
            {"site": transition.site, "native_slots": len(operations) - start,
             "recorded_global_phase_exact": [phase.numerator, phase.denominator],
             "float_unitarity_predicate_is_not_a_certificate": True}
        )
        if len(operations) > maximum_operations:
            raise ValueError("Fixed native operation cap exceeded; no retry is allowed")
    return tuple(operations), tuple(local_records)


def inverse_operations(operations):
    output = []
    for operation in reversed(operations):
        if operation.gate in ("ry", "rz", "phase"):
            output.append(Primitive(operation.gate, operation.wires, -operation.angle))
        elif operation.gate in ("cx", "swap"):
            output.append(operation)
        else:
            raise ValueError("Unknown primitive cannot receive a literal inverse")
    return tuple(output)


def _primitive_matrix(operation):
    if operation.gate == "ry":
        half = float(operation.angle) / 2
        c, s = math.cos(half), math.sin(half)
        return np.array([[c, -s], [s, c]], dtype=complex)
    if operation.gate == "rz":
        half = float(operation.angle) / 2
        return np.diag([np.exp(-1j * half), np.exp(1j * half)])
    if operation.gate in ("cx", "swap"):
        result = np.zeros((4, 4), dtype=complex)
        for index in range(4):
            destination = index ^ 2 if operation.gate == "cx" and index & 1 else index
            if operation.gate == "swap":
                destination = ((index & 1) << 1) | ((index >> 1) & 1)
            result[destination, index] = 1
        return result
    raise ValueError("Unknown local primitive")


def apply_local_matrix(state, matrix, wires, num_wires):
    wires = tuple(wires)
    if len(set(wires)) != len(wires) or any(wire < 0 or wire >= num_wires for wire in wires):
        raise ValueError("Distinct local wires inside the declared register required")
    size = 1 << len(wires)
    if np.shape(matrix) != (size, size) or np.shape(state) != (1 << num_wires,):
        raise ValueError("State and local matrix dimensions must match the wire mapping")
    mask = sum(1 << wire for wire in wires)
    bases = np.arange(1 << num_wires)
    bases = bases[(bases & mask) == 0]
    offsets = np.array([
        sum(((index >> bit) & 1) << wire for bit, wire in enumerate(wires))
        for index in range(size)
    ])
    indices = bases[:, None] + offsets[None, :]
    result = np.array(state, dtype=complex, copy=True)
    result[indices] = result[indices] @ np.asarray(matrix).T
    return result


def apply_operations(state, operations, num_wires):
    result = np.array(state, dtype=complex, copy=True)
    if result.shape != (1 << num_wires,):
        raise ValueError("State dimension does not match the declared register")
    for operation in operations:
        if operation.gate == "phase":
            result *= np.exp(1j * float(operation.angle))
        else:
            result = apply_local_matrix(
                result, _primitive_matrix(operation), operation.wires, num_wires,
            )
    return result


def apply_structure(state, plan):
    """Numerical local-matrix diagnostic; not an operator-error certificate."""
    result = np.array(state, dtype=complex, copy=True)
    for transition in plan.transitions:
        if transition.swap_before is not None:
            result = apply_local_matrix(
                result, _primitive_matrix(Primitive("swap", transition.swap_before)),
                transition.swap_before, plan.num_wires,
            )
        result = apply_local_matrix(
            result, transition.matrix, transition.local_wires, plan.num_wires,
        )
    return result


def structure_diagnostics(plan, operations):
    counts = {
        name: sum(op.gate == name for op in operations)
        for name in ("ry", "rz", "cx", "swap", "phase")
    }
    return {
        "num_wires": plan.num_wires,
        "output_qubits": len(plan.output_wires_msb_first),
        "bond_scratch_qubits": len(plan.bond_wires_low_bit_first),
        "local_dimensions": [len(item.matrix) for item in plan.transitions],
        "native_primitive_counts": counts,
        "native_forward_slots_including_tracked_phase": len(operations),
        "native_literal_inverse_slots_including_tracked_phase": len(inverse_operations(operations)),
        "fresh_zero_input_required_for_preparation": True,
        "shrink_step_excludes_its_newly_cleared_scratch_wire": all(
            item.newly_cleared_wire not in item.local_wires
            for item in plan.transitions if item.newly_cleared_wire is not None
        ),
        "rounded_core_or_completion_operator_error_certificate": None,
        "Clifford_T_synthesis_error_or_cost": None,
        "Gaussian_target_or_q10_price_law_adopted": False,
    }
