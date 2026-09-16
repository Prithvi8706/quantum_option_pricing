"""Finite Fourier-sampling controls and exact classical competitors."""

import numpy as np


def fwht(values):
    out = np.asarray(values, dtype=float).copy()
    if out.ndim != 1 or not len(out) or len(out) & (len(out)-1) or not np.isfinite(out).all():
        raise ValueError("finite power-of-two vector required")
    step = 1
    while step < len(out):
        for start in range(0, len(out), 2*step):
            a, b = out[start:start+step].copy(), out[start+step:start+2*step].copy()
            out[start:start+step], out[start+step:start+2*step] = a+b, a-b
        step *= 2
    return out


def parity_matrix(bits):
    if type(bits) is not int or not 1 <= bits <= 12:
        raise ValueError("bounded parity audit supports 1..12 bits")
    labels = np.arange(1 << bits, dtype=np.int64)
    overlap = labels[:, None] & labels[None, :]
    parity = np.zeros_like(overlap)
    for k in range(bits):
        parity ^= (overlap >> k) & 1
    return 1.0-2.0*parity


def discovery_vector(payoff, weights, training):
    payoff, weights, training = np.asarray(payoff), np.asarray(weights), np.asarray(training)
    if payoff.ndim != 1 or weights.shape != payoff.shape or training.dtype != bool or training.shape != payoff.shape:
        raise ValueError("matching vectors and Boolean training mask required")
    if not np.isfinite(payoff).all() or not np.isfinite(weights).all() or np.any(weights < 0) or weights[training].sum() <= 0:
        raise ValueError("invalid finite training distribution")
    center = np.average(payoff[training], weights=weights[training])
    vector = np.where(training, weights*(payoff-center), 0)
    norm = np.linalg.norm(vector)
    if norm <= 1e-14:
        raise ValueError("no feature-discovery signal")
    return vector/norm


def quantum_discovery(vector):
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import StatePreparation
    from qiskit.quantum_info import Statevector
    vector = np.asarray(vector, dtype=float)
    transformed = fwht(vector)/np.sqrt(len(vector))
    if not np.isclose(np.linalg.norm(vector), 1):
        raise ValueError("normalized amplitudes required")
    circuit = QuantumCircuit(int(np.log2(len(vector))))
    circuit.append(StatePreparation(vector), circuit.qubits)
    circuit.h(circuit.qubits)
    state = Statevector.from_instruction(circuit)
    discrepancy = float(np.max(abs(state.data-transformed)))
    if discrepancy > 1e-10:
        raise ArithmeticError("Fourier circuit disagrees with exact transform")
    return circuit, abs(state.data)**2, discrepancy


def rank_words(scores, count):
    if type(count) is not int or not 0 < count < len(scores):
        raise ValueError("invalid feature count")
    return sorted(range(1, len(scores)), key=lambda j: (-float(scores[j]), j))[:count]


def fit_control(payoff, weights, training, columns):
    columns = np.asarray(columns, dtype=float)
    design = np.column_stack([np.ones(len(payoff)), columns])
    root = np.sqrt(weights[training])
    coefficients = np.linalg.lstsq(design[training]*root[:, None], payoff[training]*root, rcond=1e-12)[0]
    predicted = design @ coefficients
    residual = payoff-predicted
    testing = ~training
    variance = np.average((residual-np.dot(weights, residual))**2, weights=weights)
    return dict(coefficients=coefficients, residual=residual,
                control_expectation=float(weights @ predicted),
                residual_sd=float(np.sqrt(max(0, variance))),
                holdout_rmse=float(np.sqrt(np.average(residual[testing]**2, weights=weights[testing]))),
                finite_residual_absmax=float(np.max(abs(residual))),
                control_l1=float(np.sum(abs(coefficients))))


def greedy_words(payoff, weights, training, parities, count):
    selected = []
    for _ in range(count):
        candidates = []
        for j in range(1, parities.shape[1]):
            if j in selected:
                continue
            fit = fit_control(payoff, weights, training, parities[:, selected+[j]])
            loss = float(np.average(fit["residual"][training]**2, weights=weights[training]))
            candidates.append((loss, j))
        selected.append(min(candidates)[1])
    return selected


def mps_diagnostic(amplitudes, bond):
    amplitudes = np.asarray(amplitudes, dtype=float)
    if type(bond) is not int or bond < 1 or not np.isfinite(amplitudes).all():
        raise ValueError("finite vector and positive bond required")
    bits = int(np.log2(len(amplitudes)))
    if len(amplitudes) != 1 << bits or not np.isclose(np.linalg.norm(amplitudes), 1):
        raise ValueError("normalized power-of-two vector required")
    cores, work, left = [], amplitudes.copy(), 1
    for _ in range(bits-1):
        u, s, vh = np.linalg.svd(work.reshape(left*2, -1), full_matrices=False)
        rank = min(bond, len(s))
        cores.append(u[:, :rank].reshape(left, 2, rank))
        work, left = s[:rank, None]*vh[:rank], rank
    cores.append(work.reshape(left, 2, 1))
    recovered = cores[0]
    for core in cores[1:]:
        recovered = np.tensordot(recovered, core, axes=(-1, 0))
    recovered = recovered.reshape(-1)
    recovered /= np.linalg.norm(recovered)
    return dict(bond=bond, tensor_parameters=sum(c.size for c in cores),
                observed_vector_error=float(np.linalg.norm(recovered-amplitudes)),
                observed_probability_tv=float(np.sum(abs(recovered**2-amplitudes**2))/2),
                circuit_synthesized=False, certified=False)
