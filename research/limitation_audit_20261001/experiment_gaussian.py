"""Explicit scalar Gaussian preparation and a separate MPS compression screen.

The target is a specified binned, conditionally truncated normal, NOT the
archived finite Box-Muller law. Rotation synthesis is explicitly outstanding.
"""

import argparse
import math
from pathlib import Path

import mpmath as mp
import numpy as np
from qiskit import QuantumCircuit, qasm3
from qiskit.quantum_info import Statevector

from research.limitation_audit_20261001.experiment_lookup import dump


def gaussian_probabilities(bits, cutoff=6):
    mp.mp.dps = 90
    size = 1 << bits
    edges = [-mp.mpf(cutoff) + mp.mpf(2 * cutoff) * i / size for i in range(size + 1)]
    cdf = [(1 + mp.erf(x / mp.sqrt(2))) / 2 for x in edges]
    mass = cdf[-1] - cdf[0]
    return np.array([float((cdf[i + 1] - cdf[i]) / mass) for i in range(size)])


def prepare(probabilities):
    bits = len(probabilities).bit_length() - 1
    circuit = QuantumCircuit(bits)
    for level in range(bits):
        blocks = probabilities.reshape(1 << level, -1)
        left = blocks[:, :blocks.shape[1] // 2].sum(axis=1)
        total = blocks.sum(axis=1)
        angles = 2 * np.arccos(np.sqrt(np.clip(left / total, 0, 1)))
        target = bits - level - 1
        controls = list(range(target + 1, bits))
        # Explicit Walsh/Gray multiplexor: no implicit small-angle pruning.
        # The pinned UCRY routine drops angles below 1e-10, which fails the
        # ten-qubit target. Higher transpiler levels lose still more accuracy.
        beta = angles.copy()
        stride = 1
        while stride < len(beta):
            for start in range(0, len(beta), 2 * stride):
                left = beta[start:start + stride].copy()
                right = beta[start + stride:start + 2 * stride].copy()
                beta[start:start + stride] = left + right
                beta[start + stride:start + 2 * stride] = left - right
            stride *= 2
        beta /= len(beta)
        for index in range(len(beta)):
            gray = index ^ (index >> 1)
            if beta[gray] != 0:
                circuit.ry(float(beta[gray]), target)
            if controls:
                following = (index + 1) % len(beta)
                next_gray = following ^ (following >> 1)
                changed = (gray ^ next_gray).bit_length() - 1
                circuit.cx(controls[changed], target)
    return circuit


def mps_screen(amplitudes, bond):
    bits = len(amplitudes).bit_length() - 1
    tensor = amplitudes.copy().reshape(1, -1)
    cores, rank, discarded = [], 1, 0.
    for _ in range(bits - 1):
        matrix = tensor.reshape(rank * 2, -1)
        u, s, vh = np.linalg.svd(matrix, full_matrices=False)
        keep = min(bond, len(s))
        discarded += float(np.sum(s[keep:] ** 2))
        cores.append(u[:, :keep].reshape(rank, 2, keep))
        tensor = s[:keep, None] * vh[:keep]
        rank = keep
    cores.append(tensor.reshape(rank, 2, 1))
    rebuilt = cores[0]
    for core in cores[1:]:
        rebuilt = np.tensordot(rebuilt, core, axes=(-1, 0))
    approximation = rebuilt.ravel()
    norm = float(np.linalg.norm(approximation))
    approximation /= norm
    # Stable pure-state trace distance, without subtracting near-equal squares.
    overlap = np.vdot(amplitudes, approximation)
    orthogonal = approximation - overlap * amplitudes
    return dict(bond_cap=bond, actual_bonds=[c.shape[-1] for c in cores[:-1]],
                tensor_entries=sum(c.size for c in cores), discarded_norm_squared=discarded,
                trace_distance=float(np.linalg.norm(orthogonal)),
                probability_total_variation=float(.5 * np.abs(
                    approximation ** 2 - amplitudes ** 2).sum()),
                scope="Numerical compression only; MPS preparation gates not synthesized")


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    cutoff, rows = 6, []
    for bits in (4, 6, 8, 10):
        probabilities = gaussian_probabilities(bits, cutoff)
        amplitudes = np.sqrt(probabilities)
        circuit = prepare(probabilities)
        actual = Statevector.from_instruction(circuit)
        error = float(np.max(np.abs(actual.data - amplitudes)))
        inverse = actual.evolve(circuit.inverse()).data
        ideal_zero = np.zeros_like(inverse)
        ideal_zero[0] = 1
        inverse_error = float(np.max(np.abs(inverse - ideal_zero)))
        assert error < 1e-11 and inverse_error < 1e-11
        tail = math.erfc(cutoff / math.sqrt(2))
        spacing = 2 * cutoff / (1 << bits)
        w1 = spacing / 2 + math.sqrt(2 / math.pi) * math.exp(-cutoff ** 2 / 2) + cutoff * tail
        row = dict(bits=bits, cutoff=cutoff, grid_spacing=spacing,
                   max_amplitude_error=error, inverse_error=inverse_error,
                   operations=dict(circuit.count_ops()), depth=circuit.depth(),
                   rotation_synthesis_t_count=None,
                   continuous_to_grid_wasserstein_1_upper_bound=w1,
                   continuous_tail_mass=tail, union_tail_bound_468_coordinates=468 * tail,
                   mps=[mps_screen(amplitudes, bond) for bond in (2, 4, 8)])
        rows.append(row)
        dump(output / ("gaussian_" + str(bits) + ".json"), row)
        (output / ("gaussian_" + str(bits) + ".qasm")).write_text(
            qasm3.dumps(circuit), encoding="utf-8",
        )
        print("Gaussian", bits, "qubits PASS", dict(circuit.count_ops()), flush=True)
    dump(output / "summary.json", dict(cases=rows, passed=True,
         disposition="Keep as an executable alternative and compression experiment; "
         "do not replace the production law until a price-error bridge and rotation "
         "synthesis are complete. The table of prefix angles grows exponentially.",
         certificate_scope="The analytic W1 bound concerns the ideal binned normal and "
         "1-Lipschitz scalar observables. It is not a barrier-payoff dollar certificate. "
         "Floating point angle/state errors are numerical checks, not interval proofs.",
         qsvt="Not implemented in this experiment; the prefix-rotation loader is a "
         "separate candidate, not evidence for QSVT's compiled cost."))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output)
