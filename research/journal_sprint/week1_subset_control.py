"""Stronger centered-subset control: share multiplexers, retain subset growth."""
import argparse
from pathlib import Path
from qiskit import QuantumCircuit
from .centered_factorized_signal import CenteredFactorizedSignal
from .reflection_centered_signal import prep_tree, phase_on_word
from .four_paper_probes import multiplexer
from .decimal_enclosure import Interval as I
from .asian_basket import Basket, setup
from .run_minimal_pivot_week1 import cost
from .storage import start_run, finish_run, write_json


def circuit(plan):
    index = list(range(plan.path_qubits+plan.d,plan.num_qubits))
    signals = list(range(plan.path_qubits,plan.path_qubits+plan.d))
    weights = [I(abs(float(c))) for c in plan.coefficients]
    weights += [I(0)]*((1 << plan.index_bits)-len(weights))
    prep,_,_ = prep_tree(weights)
    qc = QuantumCircuit(plan.num_qubits)
    qc.compose(prep,index,inplace=True)
    qc.z(signals)
    for j in range(plan.d):
        table = [plan.marginal_angles(row,j).tolist() for row in range(plan.d)]
        angles = []
        for k in range(1 << plan.index_bits):
            if 1 <= k <= len(plan.terms):
                row,mask = plan.terms[k-1]
                angles.extend(table[row] if mask & (1 << j) else [0.]*(1 << plan.q))
            else:
                angles.extend([0.]*(1 << plan.q))
        controls = list(range(j*plan.q,(j+1)*plan.q))+index
        qc.compose(multiplexer(angles),[signals[j]]+controls,inplace=True)
    if plan.constant_coefficient < 0:
        phase_on_word(qc,index,0)
    qc.compose(prep.inverse(),index,inplace=True)
    return qc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    args = parser.parse_args()
    path = start_run(args.output,dict(scope='adaptive stronger subset control after first resource results',
                                    grid=[[2,1],[2,2],[4,1],[4,2]]))
    rows = []
    for d,q in ((2,1),(2,2),(4,1),(4,2)):
        m = setup(Basket(1 if d==2 else 2,2,100))
        plan = CenteredFactorizedSignal(m['means'],m['factor'],100,q,4)
        qc = circuit(plan)
        row = dict(d=d,q=q,radius=plan.B,cost=cost(qc),controlled_cost=cost(qc.to_gate().control()),
                   subset_terms=len(plan.coefficients),formal_operator_certificate=False)
        rows.append(row)
        print(row,flush=True)
    write_json(path/'results.json',rows)
    finish_run(path)


if __name__ == '__main__':
    main()
