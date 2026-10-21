"""Verify all Kraus columns of measured cleanup in the real MCX ladder.

This emits an executable Qiskit dynamic circuit and verifies its branches with
an independent matrix simulator. Logical inversion repeats this clean MCX
channel; it does not reverse measurement instructions.
"""

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, qasm3

from research.controlled_source_completion.primitives import mcx, resources
from research.journal_sprint.reversible_fixed_point import Program


def specification(controls=5):
    p = Program(compact=True)
    address = p.register(controls)
    target, reference = p.register(1)[0], p.register(1)[0]
    scratch = p.register(controls - 2)
    mcx(p, address, target, scratch)
    gates = list(p.gates)
    # The original builder computes n-2 ANDs, uses the final AND to toggle
    # target, then erases exactly those ANDs in reverse order.
    compute = gates[:controls - 2]
    assert gates[controls - 1:] == list(reversed(compute))
    assert gates[controls - 2] == (scratch[-1], address[-1], target)
    return p, address, target, reference, scratch, compute


def branch(initial, p, address, target, scratch, compute, outcomes, correction=True):
    state = initial.copy()
    indices = np.arange(1 << p.qubits)
    for gate in [*compute, (scratch[-1], address[-1], target)]:
        a, b, c = gate
        destination = indices ^ ((((indices >> a) & (indices >> b)) & 1) << c)
        state = state[destination]
    for (a, b, temporary), outcome in zip(reversed(compute), outcomes):
        paired = indices ^ (1 << temporary)
        sign = 1 - 2 * ((indices >> temporary) & 1)
        state = (sign[:, None] * state + state[paired]) / math.sqrt(2)
        state[((indices >> temporary) & 1) != outcome] = 0
        if outcome:
            if correction:
                phase = 1 - 2 * (((indices >> a) & (indices >> b)) & 1)
                state *= phase[:, None]
            state = state[paired]
    return state


def run(output):
    p, address, target, reference, scratch, compute = specification()
    logical = len(address) + 2
    initial = np.zeros((1 << p.qubits, 1 << logical), complex)
    initial[np.arange(1 << logical), np.arange(1 << logical)] = 1
    ideal = np.zeros_like(initial)
    for column in range(1 << logical):
        destination = column ^ ((1 << target) if column & 31 == 31 else 0)
        ideal[destination, column] = 1
    error = 0.
    inverse_error = 0.
    broken_fidelity = 0.
    uniform = initial.sum(axis=1, keepdims=True) / math.sqrt(1 << logical)
    ideal_uniform = ideal.sum(axis=1, keepdims=True) / math.sqrt(1 << logical)
    outcomes_list = list(itertools.product((0, 1), repeat=len(scratch)))
    for outcomes in outcomes_list:
        actual = branch(initial, p, address, target, scratch, compute, outcomes)
        error = max(error, float(np.max(np.abs(actual - ideal / math.sqrt(8)))))
        # All forward branch columns plus all inverse branch columns prove
        # composition, even when the logical data has a reference entangled.
        inverted = branch(ideal, p, address, target, scratch, compute, outcomes)
        inverse_error = max(inverse_error, float(np.max(np.abs(inverted - initial / math.sqrt(8)))))
        broken = branch(uniform, p, address, target, scratch, compute, outcomes, False)
        broken_fidelity += float(abs(np.vdot(ideal_uniform, broken)) ** 2)
    assert error < 1e-12 and inverse_error < 1e-12 and broken_fidelity < .99
    circuit = QuantumCircuit(p.qubits, len(scratch))
    for gate in [*compute, (scratch[-1], address[-1], target)]:
        circuit.ccx(*gate)
    for index, (a, b, temporary) in enumerate(reversed(compute)):
        circuit.h(temporary)
        circuit.measure(temporary, index)
        with circuit.if_test((circuit.clbits[index], 1)):
            circuit.cz(a, b)
            circuit.x(temporary)
    assert circuit.num_qubits == p.qubits and reference not in scratch
    output.mkdir(parents=True, exist_ok=False)
    (output / "mcx5.qasm").write_text(qasm3.dumps(circuit), encoding="utf-8")
    result = dict(
        real_fragment="primitives.mcx with five quantum controls and arbitrary target",
        baseline=resources(p),
        candidate=dict(qubits=p.qubits, retained_ccx=4, t_count=28,
                       measurements=3, conditional_cz_max=3, conditional_reset_x_max=3,
                       sequential_cleanup_feedback_rounds=3),
        full_kraus_columns=128, branches=8, max_forward_branch_error=error,
        max_inverse_branch_error=inverse_error,
        negative_control_fidelity_without_corrections=broken_fidelity,
        passed=True,
        disposition="Verified dynamic backend candidate; do not insert measurements "
        "into the existing unitary Program or reverse their instruction sequence.",
        timing="No hardware latency measured. T-count savings do not include "
        "measurement/feedback/routing time. Reference qubit counted equally in both.",
    )
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output)
