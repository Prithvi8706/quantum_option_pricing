"""Corrected tiny acquisition; identical target, phases and AE budget to v1."""
import argparse
import math
from pathlib import Path
import numpy as np
from numpy.polynomial.chebyshev import chebval
from qiskit.quantum_info import Statevector
from .run_minimal_pivot_week2 import archives, CASES, contract_of
from .asian_encoding import grid
from .combined_qsp import response
from .reflection_centered_signal import ReflectionSignal, signal_circuit
from .week2_pipeline import loader, walk, readout
from .week2_explicit_ae import canonical_circuit
from .run_minimal_pivot_week1 import cost
from .storage import ROOT, start_run, finish_run, write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    args = parser.parse_args()
    path = start_run(args.output,dict(scope='explicit canonical AE tiny replacement',q=1,degree=16,m=3,repetitions=21))
    data,hashes = archives()
    write_json(path/'inputs.json',dict(archive_sha256=hashes,
        protocol_sha256=sha256(ROOT/'docs/journal_sprint/MINIMAL_PIVOT_WEEK2_PROTOCOL.md')))
    contract = contract_of(CASES[0])
    finite = grid(contract,1,4)
    model = finite['model']
    average = np.exp(model['means']+finite['normals']@model['factor'].T).mean(axis=1)
    discount = math.exp(-contract.rate*contract.maturity)
    marginal,_ = loader(1)
    record = data['minimax_16.json']
    rows = []
    for mode in ('original','reflection'):
        plan = ReflectionSignal(model['means'],model['factor'],contract.strike,1,4,mode)
        signal,_ = signal_circuit(plan)
        unitary,_ = walk(plan,signal,record['synthesis']['phases'])
        prep = readout(plan,unitary,marginal)
        p = float(Statevector.from_instruction(prep).probabilities([plan.num_qubits])[1])
        x = (average-contract.strike)/plan.B
        scalar = (1-float(finite['weights']@response(x,record['synthesis']['phases']).real))/2
        if abs(p-scalar)>2e-11:
            raise ArithmeticError('integrated readout mismatch')
        print(mode,'readout checked',flush=True)
        ae,metadata = canonical_circuit(prep,plan.num_qubits,3)
        print(mode,'AE constructed',flush=True)
        distribution = Statevector.from_instruction(ae).probabilities([0,1,2])
        labels = np.sin(np.pi*np.arange(8)/8)**2
        success = float(distribution[abs(labels-p)<=metadata['amplitude_error']].sum())
        if success<8/math.pi**2-1e-10:
            raise ArithmeticError('AE probability convention mismatch')
        beta = discount*plan.B/2*record['residual']['rho']
        offset = discount*plan.B/2*float(finite['weights']@(x+chebval(x,data['model.json']['low_coefficients'])))
        draws = np.random.default_rng(9217).choice(8,size=21,p=distribution/distribution.sum())
        estimated = float(np.median(labels[draws]))
        rows.append(dict(mode=mode,probability=p,scalar_probability=scalar,
            finite_truth=discount*float(finite['weights']@np.maximum(average-contract.strike,0)),
            scalar_payoff=discount*plan.B/2*float(finite['weights']@(x+chebval(x,record['candidate']['coefficients']))),
            integrated_qsp_price=offset+beta*(1-2*p),
            ae_distribution=distribution.tolist(),ae_success_probability=success,
            simulated_measurements=draws.tolist(),simulated_ae_price=offset+beta*(1-2*estimated),
            ae_statistical_price_radius=2*beta*metadata['amplitude_error'],
            readout_cost=cost(prep),ae_cost=cost(ae),metadata=metadata,
            scope='small ideal circuit and simulated measurements, finite target only'))
        print(mode,'complete',flush=True)
    write_json(path/'results.json',rows)
    write_json(path/'timings.json',{})
    finish_run(path)


if __name__=='__main__':
    main()
