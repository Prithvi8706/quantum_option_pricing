"""Explicit canonical QPE: control one compiled Grover iterate, then repeat."""
import math
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import GroverOperator, QFT


def canonical_circuit(prep, objective, m):
    if type(m) is not int or not 1<=m<=6 or not 0<=objective<prep.num_qubits:
        raise ValueError('bounded canonical circuit inputs')
    native = transpile(prep,basis_gates=['u','cx'],optimization_level=1,seed_transpiler=717)
    oracle = QuantumCircuit(prep.num_qubits)
    oracle.z(objective)
    grover = GroverOperator(oracle,state_preparation=native)
    g = transpile(grover,basis_gates=['u','cx'],optimization_level=1,seed_transpiler=717)
    controlled = g.to_gate().control()
    result = QuantumCircuit(m+prep.num_qubits)
    result.append(native.to_gate(),range(m,result.num_qubits))
    result.h(list(range(m)))
    for j in range(m):
        for _ in range(1 << j):
            result.append(controlled,[j]+list(range(m,result.num_qubits)))
    result.append(QFT(m,inverse=True,do_swaps=True).to_gate(),range(m))
    return result,dict(grover_cx=int(g.count_ops().get('cx',0)),
                       controlled_grover_qubits=controlled.num_qubits,
                       a_calls=2*(1 << m)-1,
                       amplitude_error=math.pi/(1 << m)+math.pi**2/(1 << (2*m)))
