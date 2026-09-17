"""Strong loader controls and endpoint audit; no end-to-end speedup inference."""
import argparse
from pathlib import Path
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import StatePreparation
from qiskit.quantum_info import Statevector
from .normal_loader_budget import loader_plan, circuit
from .four_paper_probes import folded_loader, geometric
from .storage import start_run, write_json, finish_run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    args = parser.parse_args()
    path = start_run(args.output,dict(q=[2,4,6], optimization_levels=[0,3], seed=719,
                                    scope='ideal logical loader only'))
    rows = []
    for q in (2,4,6):
        plan = loader_plan(q)
        old, folded = circuit(plan), folded_loader(plan)
        standard = QuantumCircuit(q)
        standard.append(StatePreparation(Statevector(folded).data),range(q))
        for name,qc in [('prefix',old),('folded',folded),('standard',standard)]:
            for level in (0,3):
                native = transpile(qc,basis_gates=['u','cx'],optimization_level=level,
                                   seed_transpiler=719)
                rows.append(dict(q=q,method=name,optimization_level=level,
                                 counts=dict(native.count_ops()),depth=native.depth(),
                                 state_difference=float(np.linalg.norm(
                                     Statevector(native).data-Statevector(folded).data))))
    endpoints = []
    for lo,hi in [(15,29),(3,13)]:
        a,q = .5,5
        exact = float(geometric(q,a)[lo:hi+1].sum())
        printed = float((np.exp(a*hi)-np.exp(a*lo))/(np.exp(a*((1<<q)-1))-1))
        endpoints.append(dict(lo=lo,hi=hi,rate=a,q=q,inclusive_probability=exact,
                              notebook_formula_probability=printed,difference=printed-exact))
    write_json(path/'results.json',dict(loaders=rows,endpoint_formula_checks=endpoints))
    finish_run(path)


if __name__ == '__main__':
    main()
