"""Exclusive local acquisition; no cloud or author code execution."""
import argparse
import json
from pathlib import Path
import numpy as np
from qiskit import transpile
from qiskit.quantum_info import Statevector
from .four_paper_probes import folded_loader, folded_rounding_bound, run_identities
from .normal_loader_budget import loader_plan, circuit
from .storage import ROOT, start_run, finish_run, write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    path = start_run(args.output, dict(q=list(range(1,7))+[10],
        original_cost_limit_q=6, basis=['ry','rz','h','x','cx'], optimization_level=0,
        purpose='development identities and ideal loader compilation, not confirmation'))
    write_json(path/'identities.json', run_identities())
    archived = ROOT/'results/journal_sprint/normalization_approximation_v1/loader.json'
    archive = json.loads(archived.read_text())
    print('archived loader keys:', list(archive), flush=True)
    rows = []
    for q in list(range(1,7))+[10]:
        plan = loader_plan(q) if q < 10 else archive
        qc = folded_loader(plan)
        native = transpile(qc,basis_gates=['ry','rz','h','x','cx'],optimization_level=0)
        row = dict(q=q, folded_counts=dict(native.count_ops()), folded_depth=native.depth(),
                   rounding=folded_rounding_bound(plan),
                   state_norm=float(np.linalg.norm(Statevector(native).data)))
        if q <= 6:
            old = transpile(circuit(plan),basis_gates=['ry','rz','h','x','cx'],optimization_level=0)
            row.update(original_counts=dict(old.count_ops()), original_depth=old.depth(),
                       state_difference=float(np.linalg.norm(Statevector(old).data-Statevector(native).data)))
        rows.append(row)
        print(row, flush=True)
    write_json(path/'loader.json', dict(rows=rows, archived_plan_sha256=sha256(archived),
                                       quantum_advantage_established=False))
    finish_run(path)


if __name__ == '__main__':
    main()
