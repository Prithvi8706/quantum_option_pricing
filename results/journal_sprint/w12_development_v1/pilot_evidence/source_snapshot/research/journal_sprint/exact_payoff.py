"""Established multiplexed rotations as an exact finite-grid payoff baseline."""

import math
from dataclasses import replace

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UCRYGate
from qiskit_finance.circuit.library import LogNormalDistribution

from research.paper_a.references import grid_points, grid_probabilities
from .tighter_grid import tighter_bounds_for


def exact_components(contract, n):
    if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= 8:
        raise ValueError("finite-table prototype supports 1..8 grid qubits")
    old, _ = tighter_bounds_for(contract, n, 0.125)
    x = grid_points(old.lower, old.upper, n)
    weights = grid_probabilities(contract, old.lower, old.upper, n)
    payoff = np.maximum(x - contract.K, 0) / (old.upper - contract.K)
    if not np.all(np.isfinite(payoff)) or np.any(payoff < 0) or np.any(payoff > 1):
        raise ValueError("invalid normalized payoff")
    bounds = replace(
        old,
        sensitivity=math.exp(-contract.r * contract.T) * (old.upper - contract.K),
        offset=0.0,
        encoding=0.0,
    )
    mu = math.log(contract.S0) + (contract.r - contract.sigma**2 / 2) * contract.T
    distribution = LogNormalDistribution(
        n, mu=mu, sigma=contract.sigma**2 * contract.T, bounds=(old.lower, old.upper)
    )
    circuit = QuantumCircuit(n + 1)
    circuit.append(distribution.to_gate(), list(range(n)))
    angles = (2 * np.arcsin(np.sqrt(payoff))).tolist()
    circuit.append(UCRYGate(angles), [n] + list(range(n)))
    return circuit, bounds, float(weights @ payoff), payoff
