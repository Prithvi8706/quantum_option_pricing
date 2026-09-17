"""Bounded centered subset LCU for finite-grid basket signals (d <= 4, q <= 10).

For t=|b|L, exp(bz)=cosh(t)+sinh(t)*r(z), with r in [-1,1].
Expand each basket row over coordinate subsets, then combine all empty subsets
and -strike into one signed constant. Nonempty coefficients are positive (zero
terms are omitted). B is their sum plus the absolute constant. In exact
arithmetic B = B_old - 2*min(strike, basket_constant), but subset SELECT costs
up to d*2**(d-1) local reflections and 1+d*(2**d-1) LCU terms. This expansion
is exponential in dimension; this module is only a bounded alternative.

Only marginal angle vectors of length 2**q are constructed, never a joint path
table. No probability preparation, hardware execution, or clean output is
provided. B and rotations are floating-point computations, NOT an outward
rounded normalization certificate or a certified minimax-|x|/phase result.
An |x| approximation error epsilon becomes B*epsilon in unnormalized units;
certified minimax and synthesis error accounting remain separate obligations.
"""

import math

import numpy as np

from .factorized_signal import projected_phase


class CenteredFactorizedSignal:
    """Plan for P U P = diag((mean(exp(means + factor @ z))-strike)/B).

    Little-endian wires: d q-bit coordinate registers, one reflection ancilla
    per coordinate, then the LCU index. P fixes every ancilla to zero. Index 0
    is the combined constant, including when it is zero. ``terms`` contains
    (row, subset_bitmask) for the remaining indices; ``coefficients`` includes
    the signed constant at index 0. Unused indices select identity.
    """

    def __init__(self, means, factor, strike, q, L, nodes=None):
        if type(q) is not int or not 1 <= q <= 10:
            raise ValueError("q must be an integer in [1,10]")
        self.means = np.array(means, dtype=float, copy=True)
        if self.means.ndim != 1 or not 1 <= self.means.size <= 4:
            raise ValueError("means must be a vector with 1 <= d <= 4 (exponential expansion)")
        self.d = self.means.size
        self.factor = np.array(factor, dtype=float, copy=True)
        if self.factor.shape != (self.d, self.d):
            raise ValueError("factor must have shape (d,d)")
        if not np.isfinite(self.means).all() or not np.isfinite(self.factor).all():
            raise ValueError("means and factor must be finite")
        self.strike, self.L = float(strike), float(L)
        if not math.isfinite(self.strike) or self.strike < 0:
            raise ValueError("strike must be finite and nonnegative")
        if not math.isfinite(self.L) or self.L <= 0:
            raise ValueError("L must be finite and positive")
        self.q = q
        with np.errstate(over="ignore", under="ignore"):
            self._t = abs(self.factor)*self.L
        if (not np.isfinite(self._t).all() or
                np.any((self.factor != 0) & (self._t == 0))):
            raise ValueError("marginal scale overflows or underflows")
        # Log products avoid overflowing intermediate exp(mu), cosh and sinh.
        log_c = np.empty_like(self._t)
        log_s = np.full_like(self._t, -np.inf)
        for i in range(self.d):
            for j in range(self.d):
                t = float(self._t[i, j])
                # Avoid even the intermediate 2*t overflowing.
                decay = math.exp(-t)**2
                log_c[i, j] = t + math.log1p(decay) - math.log(2)
                if t:
                    log_s[i, j] = t + math.log(-math.expm1(-t)* (1+math.exp(-t))) - math.log(2)

        def coefficient(row, subset):
            log_value = math.fsum([float(self.means[row]), -math.log(self.d)] +
                                  [float(log_s[row, j] if subset & (1 << j)
                                         else log_c[row, j]) for j in range(self.d)])
            try:
                value = math.exp(log_value)
            except OverflowError as exc:
                raise ValueError("coefficient overflows") from exc
            if not math.isfinite(value) or value <= 0:
                raise ValueError("coefficient overflows or underflows")
            return value

        try:
            self.basket_constant = math.fsum(coefficient(i, 0) for i in range(self.d))
            self.constant_coefficient = self.basket_constant - self.strike
            terms, coefficients = [], [self.constant_coefficient]
            for i in range(self.d):
                for subset in range(1, 1 << self.d):
                    if any(subset & (1 << j) and self.factor[i, j] == 0
                           for j in range(self.d)):
                        continue
                    terms.append((i, subset))
                    coefficients.append(coefficient(i, subset))
            self.B = math.fsum(abs(c) for c in coefficients)
        except OverflowError as exc:
            raise ValueError("normalization overflows") from exc
        if not math.isfinite(self.B) or self.B <= 0:
            raise ValueError("normalization must be finite and positive (zero signal has B=0)")
        self.terms = tuple(terms)
        self.coefficients = np.array(coefficients)
        self.path_qubits = self.d*q
        self.index_bits = max(1, (len(coefficients)-1).bit_length())
        self.num_qubits = self.path_qubits + self.d + self.index_bits
        self.good_qubits = tuple(range(self.path_qubits, self.num_qubits))
        if nodes is None:
            nodes = self.L*((np.arange(1 << q, dtype=float)+.5)*2/(1 << q)-1)
        nodes = np.asarray(nodes, dtype=float)
        if nodes.shape == (1 << q,):
            nodes = np.broadcast_to(nodes, (self.d, 1 << q))
        if (nodes.shape != (self.d, 1 << q) or not np.isfinite(nodes).all() or
                np.any(abs(nodes) > self.L)):
            raise ValueError("nodes must have shape (2**q,) or (d,2**q), within [-L,L]")
        self.nodes = np.array(nodes, copy=True)
        for array in (self.means, self.factor, self._t, self.coefficients, self.nodes):
            array.setflags(write=False)

    def marginal_values(self, row, coordinate):
        """Centered r, evaluated without cancellation for tiny nonzero b.

        For b=0 the coefficient sinh(t) vanishes; choose r=0 by convention.
        Clipping only removes floating roundoff at the analytic endpoints.
        """
        if (type(row) is not int or type(coordinate) is not int or
                not 0 <= row < self.d or not 0 <= coordinate < self.d):
            raise ValueError("row and coordinate must be integers in [0,d)")
        t = float(self._t[row, coordinate])
        if t == 0:
            return np.zeros(1 << self.q)
        u = np.sign(self.factor[row, coordinate])*(self.nodes[coordinate]/self.L)
        denominator = -math.expm1(-t)*(1+math.exp(-t))
        with np.errstate(over="ignore", under="ignore"):
            r = 1 + 2*(np.expm1(t*(u-1))/denominator)
        return np.clip(r, -1, 1)

    def marginal_angles(self, row, coordinate):
        return 2*np.arccos(self.marginal_values(row, coordinate))

    def resource_metadata(self):
        """Structural counts only: no compilation, simulation or joint table."""
        local = sum(bin(subset).count("1") for _, subset in self.terms)
        return dict(
            d=self.d, q=self.q, dimension_cap=4, q_cap=10,
            dimension_cost="exponential subset expansion",
            path_qubits=self.path_qubits, signal_ancillas=self.d,
            lcu_ancillas=self.index_bits, total_qubits=self.num_qubits,
            lcu_terms=len(self.coefficients), max_lcu_terms=1+self.d*((1 << self.d)-1),
            prep_amplitudes=1 << self.index_bits,
            marginal_entries=self.d*self.d*(1 << self.q),
            local_reflections=local, select_angle_entries=local*(1 << self.q),
            normalization=self.B, constant_coefficient=self.constant_coefficient,
            normalization_certificate=False, joint_table_enumerated=False,
            compiled_gate_counts=None, clean_ancillas=False, uniform_phase_certificate=False,
        )


def signal_circuit(plan):
    """PREP, SELECT, PREP inverse; every selected block is an involution."""
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import StatePreparation, UCRYGate

    if not isinstance(plan, CenteredFactorizedSignal):
        raise TypeError("plan must be a CenteredFactorizedSignal")
    target_count = plan.path_qubits + plan.d
    targets = list(range(target_count))
    index = list(range(target_count, plan.num_qubits))
    amplitudes = np.zeros(1 << plan.index_bits)
    amplitudes[:len(plan.coefficients)] = np.sqrt(abs(plan.coefficients)/plan.B)
    prep = StatePreparation(amplitudes)
    circuit = QuantumCircuit(plan.num_qubits, name="centered_factorized_signal")
    circuit.append(prep, index)
    if plan.constant_coefficient < 0:
        constant = QuantumCircuit(target_count)
        constant.global_phase = np.pi
        circuit.append(constant.to_gate().control(plan.index_bits, ctrl_state=0), index+targets)
    # Positive/zero constant and unused indices select identity implicitly.
    for k, (row, subset) in enumerate(plan.terms, start=1):
        block = QuantumCircuit(target_count)
        for j in range(plan.d):
            if subset & (1 << j):
                ancilla = plan.path_qubits+j
                block.z(ancilla)
                block.append(UCRYGate(plan.marginal_angles(row, j).tolist()),
                             [ancilla]+list(range(j*plan.q, (j+1)*plan.q)))
        circuit.append(block.to_gate().control(plan.index_bits, ctrl_state=k), index+targets)
    circuit.append(prep.inverse(), index)
    return circuit


def walk_circuit(plan):
    """Return (2P-I)U, retaining all garbage and the exact global phase."""
    circuit = signal_circuit(plan)
    circuit.compose(projected_phase(plan.num_qubits, plan.good_qubits, np.pi/2), inplace=True)
    circuit.global_phase -= np.pi/2
    return circuit


def phased_walk_circuit(plan, phases):
    """Good block matches complex combined_qsp.response(x, phases)."""
    if not isinstance(plan, CenteredFactorizedSignal):
        raise TypeError("plan must be a CenteredFactorizedSignal")
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
