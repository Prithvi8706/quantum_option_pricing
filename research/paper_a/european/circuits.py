"""Exact ideal-statevector circuit layer.

The objective qubit is located from the amplitude function's own register
layout, never by a hand-written bit shift, per the E0 gate.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from qiskit import QuantumCircuit
from qiskit.circuit.library import LinearAmplitudeFunction
from qiskit.quantum_info import Statevector
from qiskit_finance.circuit.library import LogNormalDistribution

from research.paper_a.benchmark import Contract
from research.paper_a.payoff import h_inverse


@dataclass(frozen=True)
class EuropeanCircuit:
    circuit: QuantumCircuit
    objective_qubit: int
    L: float
    U: float
    n: int


def build_european(c: Contract, L: float, U: float, n: int,
                   rescaling: float) -> EuropeanCircuit:
    """State preparation composed with the linear payoff objective.

    LogNormalDistribution takes the log-VARIANCE as `sigma`.
    LinearAmplitudeFunction's `slope` and `image` must share units: the
    payoff is f(x) = x - K on [K, U], so slope is 1.0 and image is (0, U-K).
    """
    mu_ln = (c.r - 0.5 * c.sigma ** 2) * c.T + math.log(c.S0)
    s_ln = c.sigma * math.sqrt(c.T)

    distribution = LogNormalDistribution(
        n, mu=mu_ln, sigma=s_ln ** 2, bounds=(L, U))
    objective = LinearAmplitudeFunction(
        n,
        slope=[0.0, 1.0],
        offset=[0.0, 0.0],
        domain=(L, U),
        image=(0.0, U - c.K),
        rescaling_factor=rescaling,
        breakpoints=[L, c.K],
    )

    circuit = QuantumCircuit(objective.num_qubits)
    circuit.append(distribution.to_gate(), range(n))
    circuit.append(objective.to_gate(), range(objective.num_qubits))
    return EuropeanCircuit(circuit=circuit, objective_qubit=n, L=L, U=U, n=n)


def statevector_amplitude(ec: EuropeanCircuit) -> float:
    """a_sv: marginal probability that the named objective qubit reads 1."""
    marginal = Statevector(ec.circuit).probabilities([ec.objective_qubit])
    return float(marginal[1])


def p_circuit(c: Contract, ec: EuropeanCircuit, rescaling: float) -> float:
    """P_circuit = e^{-rT} h(a_sv)."""
    return math.exp(-c.r * c.T) * h_inverse(
        statevector_amplitude(ec), c.K, ec.U, rescaling)
