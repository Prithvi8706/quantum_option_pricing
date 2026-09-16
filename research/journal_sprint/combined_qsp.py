"""Bounded finite-table QSP/LCU experiments, not a scalable signal oracle."""

import math
import numpy as np
from numpy.polynomial.chebyshev import chebval
from scipy.optimize import least_squares


def abs_polynomial(degree):
    if type(degree) is not int or degree < 2 or degree % 2:
        raise ValueError("positive even degree required")
    coefficients = np.zeros(degree+1)
    coefficients[0] = 2/math.pi
    for k in range(1, degree//2+1):
        coefficients[2*k] = 4/math.pi*(-1)**(k+1)/(4*k*k-1)
    tail = 2/(math.pi*(degree+1))
    return coefficients/(1+tail), tail


def response(x, phases):
    x = np.asarray(x, dtype=float)
    if not np.isfinite(x).all() or np.any(abs(x) > 1):
        raise ValueError("signal outside [-1,1]")
    a = np.full(x.shape, np.exp(1j*phases[0]), dtype=complex)
    b = np.zeros_like(a)
    off = 1j*np.sqrt(np.maximum(0, 1-x*x))
    for phi in phases[1:]:
        a, b = np.exp(1j*phi)*(x*a+off*b), np.exp(-1j*phi)*(off*a+x*b)
    return a


def synthesize(degree):
    coefficients, tail = abs_polynomial(degree)
    nodes = np.cos(np.pi*(np.arange(4*degree+1)+.5)/(4*degree+1))
    target = chebval(nodes, coefficients)
    attempts, candidates = [], []
    for seed in (1201, 1202, 1203):
        initial = np.random.default_rng(seed).uniform(-np.pi, np.pi, degree+1)
        fit = least_squares(lambda phases: response(nodes, phases).real-target, initial,
                            max_nfev=1500, ftol=1e-12, xtol=1e-12, gtol=1e-12)
        error = float(np.max(abs(response(nodes, fit.x).real-target)))
        attempts.append(dict(seed=seed, evaluations=int(fit.nfev), solver_success=bool(fit.success),
                             node_error=error))
        candidates.append((error, seed, fit.x))
    error, seed, phases = min(candidates, key=lambda v: (v[0], v[1]))
    mesh = np.linspace(-1, 1, 4097)
    dense_error = float(np.max(abs(response(mesh, phases).real-chebval(mesh, coefficients))))
    return dict(degree=degree, phases=phases.tolist(), coefficients=coefficients.tolist(),
                analytic_truncation_expression=tail, abs_rescale=1+tail,
                sampled_phase_error=dense_error, attempts=attempts, selected_seed=seed,
                fit_accepted=error < 1e-8 and dense_error < 1e-8,
                uniform_phase_certificate=False)


def signal_circuit(signal):
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import UCRYGate
    signal = np.asarray(signal, dtype=float)
    bits = int(np.log2(len(signal)))
    if len(signal) != 1 << bits or not np.isfinite(signal).all() or np.any(abs(signal) > 1):
        raise ValueError("finite power-of-two signal in [-1,1] required")
    # Path wires 0..bits-1; signal ancilla at bits. W=xI+i sqrt(1-x^2)X.
    circuit = QuantumCircuit(bits+1)
    circuit.sdg(bits)
    circuit.append(UCRYGate((2*np.arccos(signal)).tolist()), [bits]+list(range(bits)))
    circuit.s(bits)
    return circuit


def qsp_circuit(signal, phases):
    from qiskit import QuantumCircuit
    block = signal_circuit(signal)
    result = QuantumCircuit(block.num_qubits)
    target = result.num_qubits-1
    result.rz(-2*phases[0], target)
    for phi in phases[1:]:
        result.compose(block, inplace=True)
        result.rz(-2*phi, target)
    return result


def weighted_depth(circuit, durations):
    """Critical path in supplied arbitrary units; not calibrated QPU runtime."""
    ready = [0.0]*circuit.num_qubits
    for item in circuit.data:
        if item.operation.name not in durations:
            raise ValueError("missing gate duration")
        wires = [circuit.find_bit(q).index for q in item.qubits]
        finish = max((ready[i] for i in wires), default=0)+durations[item.operation.name]
        for i in wires:
            ready[i] = finish
    return max(ready, default=0)


def lcu_circuit(signal, phases, call_factor, abs_rescale, coefficients, words):
    """PREP† SELECT PREP block encodes QSP call minus a parity control.

    The absolute coefficient sum beta, including the control, is essential.
    This finite-table prototype does not implement a production basket signal.
    """
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import StatePreparation
    bits = int(np.log2(len(signal)))
    if len(coefficients) != len(words)+1 or call_factor <= 0:
        raise ValueError("invalid signed control coefficients")
    raw = [call_factor*abs_rescale, call_factor]+[-float(c) for c in coefficients]
    beta = sum(abs(v) for v in raw)
    index_bits = max(1, (len(raw)-1).bit_length())
    amplitudes = np.zeros(1 << index_bits)
    amplitudes[:len(raw)] = np.sqrt(np.abs(raw)/beta)
    result = QuantumCircuit(bits+1+index_bits)
    targets = list(range(bits+1))
    index = list(range(bits+1, result.num_qubits))
    prep = StatePreparation(amplitudes)
    result.append(prep, index)
    blocks = [qsp_circuit(signal, phases), signal_circuit(signal)]
    for word in [0]+list(words):
        block = QuantumCircuit(bits+1)
        for k in range(bits):
            if (word >> k) & 1:
                block.z(k)
        blocks.append(block)
    for j, (coefficient, block) in enumerate(zip(raw, blocks)):
        if coefficient == 0:
            continue
        if coefficient < 0:
            block.global_phase += np.pi
        result.append(block.to_gate().control(index_bits, ctrl_state=j), index+targets)
    result.append(prep.inverse(), index)
    return result, beta


def hadamard_mean(unitary, weights):
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import StatePreparation
    from qiskit.quantum_info import Statevector
    bits = int(np.log2(len(weights)))
    result = QuantumCircuit(unitary.num_qubits+1)
    result.append(StatePreparation(np.sqrt(weights)), list(range(bits)))
    test = unitary.num_qubits
    result.h(test)
    result.append(unitary.to_gate().control(), [test]+list(range(test)))
    result.h(test)
    state = Statevector.from_instruction(result)
    probability_one = float(np.sum(abs(state.data[1 << test:])**2))
    return 1-2*probability_one, result
