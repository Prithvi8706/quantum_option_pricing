"""Run in the isolated modern comparator environment; no hardware or pytest."""

import json

import numpy as np
from qiskit import QuantumCircuit

from .biqae_smoke import local_backend


def check():
    circuit = QuantumCircuit(1)
    circuit.ry(2 * np.arcsin(np.sqrt(0.17)), 0)
    circuit.measure_all()
    sequences = []
    for _ in range(2):
        sampler = local_backend()
        sequences.append(
            [
                sampler.run([circuit], shots=10).result()[0].data.meas.get_counts().get("1", 0)
                for _ in range(5)
            ]
        )
    if sequences[0] != sequences[1] or sequences[0] != [3, 0, 1, 1, 2]:
        raise RuntimeError("pinned sampler progression/replay regression failed")
    print(json.dumps({"passed": True, "sequences": sequences}))


if __name__ == "__main__":
    check()
