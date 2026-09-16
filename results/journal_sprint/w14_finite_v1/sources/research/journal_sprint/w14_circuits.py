"""Executed finite Asian Grover circuits and explicitly defined density noise."""

import math
import time

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator
from qiskit.quantum_info import Operator, Statevector

from .asian_encoding import circuits, resources


DEPTHS = (0, 1, 2, 3, 4)


def response(data, precision, representation, k, eta):
    """Global depolarization after each A or A-inverse; perfect reflections.

    Evolves actual compiled unitary matrices and full density matrices, rather
    than generating a response table from the sine formula under test.
    Noise is NOT a per-CX hardware model or calibrated device estimate.
    """
    if (
        isinstance(k, bool)
        or not isinstance(k, int)
        or k not in DEPTHS
        or isinstance(eta, bool)
        or not math.isfinite(eta)
        or not 0 <= eta < 1
    ):
        raise ValueError("invalid depth/noise")
    started = time.perf_counter()
    _, _, preparation = circuits(data, precision, representation, "product")
    if preparation.num_qubits > 7:
        raise ValueError("bounded density diagnostic supports at most seven qubits")
    oracle = QuantumCircuit(preparation.num_qubits)
    oracle.z(preparation.num_qubits - 1)
    grover = GroverOperator(oracle=oracle, state_preparation=preparation)
    quantum = preparation.compose(grover.power(k)) if k else preparation
    compiled, counts = resources(quantum)
    measured = QuantumCircuit(preparation.num_qubits, 1)
    measured.compose(quantum, inplace=True)
    measured.measure(preparation.num_qubits - 1, 0)
    _, measured_counts = resources(measured)
    compiled_a, a_counts = resources(preparation)
    ideal = Statevector.from_instruction(compiled)
    half = 2 ** (preparation.num_qubits - 1)
    probability = float(np.abs(ideal.data[half:]) @ np.abs(ideal.data[half:]))
    a = float(data["weights"] @ data[representation] / data[representation].max())
    formula = math.sin((2 * k + 1) * math.asin(math.sqrt(a))) ** 2
    unitary = Operator(compiled_a).data
    size = unitary.shape[0]
    rho = np.zeros((size, size), dtype=complex)
    rho[0, 0] = 1
    mixed = np.eye(size) / size
    sf = np.ones(size)
    sf[half:] = -1
    s0 = np.ones(size)
    s0[0] = -1

    def apply(matrix, state):
        evolved = matrix @ state @ matrix.conj().T
        return (1 - eta) * evolved + eta * mixed

    rho = apply(unitary, rho)
    for _ in range(k):
        rho = sf[:, None] * rho * sf[None, :]
        rho = apply(unitary.conj().T, rho)
        rho = s0[:, None] * rho * s0[None, :]
        rho = apply(unitary, rho)
    noisy = float(np.trace(rho[half:, half:]).real)
    predicted = (1 - eta) ** (2 * k + 1) * formula + (1 - (1 - eta) ** (2 * k + 1)) / 2
    errors = dict(
        ideal=abs(probability - formula),
        noise=abs(noisy - predicted),
        trace=abs(complex(np.trace(rho)) - 1),
        hermiticity=float(np.max(np.abs(rho - rho.conj().T))),
    )
    minimum_eigenvalue = float(np.linalg.eigvalsh(rho).min())
    if max(errors.values()) > 1e-10 or minimum_eigenvalue < -1e-10:
        raise ArithmeticError("executed response validation failed")
    return dict(
        representation=representation,
        k=k,
        eta=eta,
        amplitude=a,
        ideal_probability=probability,
        formula_probability=formula,
        density_probability=noisy,
        model_probability=predicted,
        errors=errors,
        minimum_eigenvalue=minimum_eigenvalue,
        circuit=counts,
        measurement_circuit=measured_counts,
        depth_convention="circuit excludes measurement; measurement_circuit includes it",
        preparation=a_counts,
        A_calls=2 * k + 1,
        Q_calls=k,
        simulator_seconds=time.perf_counter() - started,
        shots=0,
        hardware_seconds=None,
    )


def fixed_interval(counts, shots, depths, eta):
    """Established all-branch CP inversion under known depolarizing rate.

    Not IQAE, Bayesian inference, or a novel estimator. Fixed schedule alpha
    allocation; no uncharged calibration is implied by treating eta as known.
    """
    from .intervals import invert

    return invert(counts, shots, depths, eta_bounds=(eta, eta), alpha=0.05)
