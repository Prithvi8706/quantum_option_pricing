"""Separable finite-grid basket block encoding, with explicit garbage and scale.

No joint table or probability state is constructed here. Coordinates use a finite
grid in [-L, L]; a product-normal probability preparation is the caller's job.
The default grid consists of uniform cell midpoints, not normal quantiles.
Only d*d*2**q marginal values are needed. This is not a phase certificate or a
claim of efficient compiled gates: controlled multiplexors and PREP cost gates,
and recovering A-K from its block incurs the normalization B (potentially large).
"""

import math

import numpy as np


class FactorizedSignal:
    """Plan for (A-K)/B, A = mean_i exp(means_i + factor_i dot z).

    Wires are little endian: d consecutive q-bit coordinate registers, d signal
    ancillas, then ceil(log2(d+1)) LCU ancillas. P fixes *all* ancillas to zero.
    Nodes may be a shared vector of length 2**q or a (d, 2**q) array. No normal
    distribution weights are assumed or prepared by this signal oracle.
    """

    def __init__(self, means, factor, strike, q, L, nodes=None):
        if type(q) is not int or q < 1:
            raise ValueError("q must be a positive integer")
        self.means = np.array(means, dtype=float, copy=True)
        self.factor = np.array(factor, dtype=float, copy=True)
        if self.means.ndim != 1 or self.means.size == 0:
            raise ValueError("means must be a nonempty vector")
        self.d = len(self.means)
        if self.factor.shape != (self.d, self.d):
            raise ValueError("factor must have shape (d, d)")
        if not np.isfinite(self.means).all() or not np.isfinite(self.factor).all():
            raise ValueError("means and factor must be finite")
        self.strike, self.L = float(strike), float(L)
        if not math.isfinite(self.strike) or self.strike < 0:
            raise ValueError("strike must be finite and nonnegative")
        if not math.isfinite(self.L) or self.L <= 0:
            raise ValueError("L must be finite and positive")
        self.q = q
        self.path_qubits = self.d*q
        self.index_bits = self.d.bit_length()
        self.num_qubits = self.path_qubits + self.d + self.index_bits
        self.good_qubits = tuple(range(self.path_qubits, self.num_qubits))
        # Check the coefficient bound before allocating even marginal arrays.
        with np.errstate(over="ignore", under="ignore", invalid="ignore"):
            logs = self.means + self.L*np.sum(abs(self.factor), axis=1) - math.log(self.d)
            self.coefficients = np.exp(logs)
            self.B = float(np.sum(self.coefficients) + self.strike)
        if (not np.isfinite(self.coefficients).all() or
                np.any(self.coefficients <= 0) or not math.isfinite(self.B) or self.B <= 0):
            raise ValueError("normalization overflows or coefficients underflow")
        if nodes is None:
            nodes = self.L*((np.arange(1 << q, dtype=float) + .5)*2/(1 << q) - 1)
        nodes = np.asarray(nodes, dtype=float)
        if nodes.shape == (1 << q,):
            nodes = np.broadcast_to(nodes, (self.d, 1 << q))
        if (nodes.shape != (self.d, 1 << q) or not np.isfinite(nodes).all() or
                np.any(abs(nodes) > self.L)):
            raise ValueError("nodes must have shape (2**q,) or (d, 2**q), within [-L,L]")
        self.nodes = np.array(nodes, copy=True)
        for array in (self.means, self.factor, self.coefficients, self.nodes):
            array.setflags(write=False)

    def marginal_values(self, row, coordinate):
        """Return one marginal a_ij, never a joint-grid vector."""
        if (type(row) is not int or type(coordinate) is not int or
                not 0 <= row < self.d or not 0 <= coordinate < self.d):
            raise ValueError("row and coordinate must be integers in [0,d)")
        b = self.factor[row, coordinate]
        # This form avoids overflow and cancellation in b*z - abs(b)*L.
        with np.errstate(over="ignore", under="ignore"):
            return np.exp(-abs(b)*(self.L - np.sign(b)*self.nodes[coordinate]))

    def resource_metadata(self):
        """Structural counts only; no circuit compilation or joint enumeration."""
        return dict(
            d=self.d, q=self.q, path_qubits=self.path_qubits,
            signal_ancillas=self.d, lcu_ancillas=self.index_bits,
            total_qubits=self.num_qubits, marginal_entries=self.d*self.d*(1 << self.q),
            local_reflections=self.d*self.d, lcu_terms=self.d+1,
            prep_amplitudes=1 << self.index_bits, normalization=self.B,
            joint_table_enumerated=False, compiled_gate_counts=None,
            clean_ancillas=False, uniform_phase_certificate=False,
        )


def signal_circuit(plan):
    """Hermitian involution U with P U P = diag((A-K)/B) on P.

    Every row is a tensor product of Ry(2 acos(a)) Z reflections. The unused
    LCU index states select identity; strike selects -I. PREP conjugation keeps
    the whole operator Hermitian and involutory. Ancilla garbage is retained.
    """
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import StatePreparation, UCRYGate

    if not isinstance(plan, FactorizedSignal):
        raise TypeError("plan must be a FactorizedSignal")
    target_count = plan.path_qubits + plan.d
    targets = list(range(target_count))
    index = list(range(target_count, plan.num_qubits))
    amplitudes = np.zeros(1 << plan.index_bits)
    amplitudes[:plan.d] = np.sqrt(plan.coefficients/plan.B)
    amplitudes[plan.d] = math.sqrt(plan.strike/plan.B)
    prep = StatePreparation(amplitudes)
    circuit = QuantumCircuit(plan.num_qubits, name="factorized_signal")
    circuit.append(prep, index)
    for row in range(plan.d):
        block = QuantumCircuit(target_count)
        for j in range(plan.d):
            ancilla = plan.path_qubits+j
            block.z(ancilla)
            angles = 2*np.arccos(plan.marginal_values(row, j))
            block.append(UCRYGate(angles.tolist()),
                         [ancilla] + list(range(j*plan.q, (j+1)*plan.q)))
        circuit.append(block.to_gate().control(plan.index_bits, ctrl_state=row), index+targets)
    # A controlled global phase is essential: dropping it loses the strike sign.
    strike = QuantumCircuit(target_count)
    strike.global_phase = np.pi
    circuit.append(strike.to_gate().control(plan.index_bits, ctrl_state=plan.d), index+targets)
    circuit.append(prep.inverse(), index)
    return circuit


def projected_phase(num_qubits, good_qubits, phi):
    """Exactly exp(i phi (2P-I)), including its global exp(-i phi)."""
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import PhaseGate

    if type(num_qubits) is not int or num_qubits < 1:
        raise ValueError("num_qubits must be a positive integer")
    good_qubits = tuple(good_qubits)
    if (not good_qubits or any(type(k) is not int or not 0 <= k < num_qubits
                              for k in good_qubits) or
            len(set(good_qubits)) != len(good_qubits)):
        raise ValueError("good_qubits must be nonempty distinct valid wire indices")
    phi = float(phi)
    if not math.isfinite(phi):
        raise ValueError("phase must be finite")
    circuit = QuantumCircuit(num_qubits, name="projected_phase")
    circuit.global_phase = -phi
    circuit.x(list(good_qubits))
    gate = PhaseGate(2*phi)
    if len(good_qubits) > 1:
        gate = gate.control(len(good_qubits)-1)
    circuit.append(gate, list(good_qubits))
    circuit.x(list(good_qubits))
    return circuit


def walk_circuit(plan):
    """Return R U for R=2P-I (U acts first)."""
    circuit = signal_circuit(plan)
    circuit.compose(projected_phase(plan.num_qubits, plan.good_qubits, np.pi/2), inplace=True)
    circuit.global_phase -= np.pi/2
    return circuit


def phased_walk_circuit(plan, phases):
    """Match combined_qsp.response(x, phases) on the good block, including phase.

    Chronological order is phase[0], RU, phase[1], RU, ... . In each invariant
    signal plane RU=[[x,s],[-s,x]] is diagonally similar to [[x,i*s],[i*s,x]].
    That similarity commutes with projector phases and fixes the good vector,
    so even the complex good block matches response, not merely its real part.
    This circuit retains garbage; it does not extract a clean real polynomial.
    """
    phases = np.asarray(phases, dtype=float)
    if phases.ndim != 1 or len(phases) == 0 or not np.isfinite(phases).all():
        raise ValueError("phases must be a nonempty finite vector")
    circuit = projected_phase(plan.num_qubits, plan.good_qubits, phases[0])
    if len(phases) > 1:
        walk = walk_circuit(plan)
        for phi in phases[1:]:
            circuit.compose(walk, inplace=True)
            circuit.compose(projected_phase(plan.num_qubits, plan.good_qubits, phi), inplace=True)
    return circuit
