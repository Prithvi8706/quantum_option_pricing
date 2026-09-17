"""Exclusive bounded W1 experiment, same contract; no confirmation claims."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from numpy.polynomial.chebyshev import chebval
from qiskit import QuantumCircuit, transpile
from .asian_basket import Basket, setup
from .asian_encoding import grid
from .reflection_centered_signal import ReflectionSignal, signal_circuit
from .factorized_signal import FactorizedSignal, signal_circuit as old_circuit
from .centered_factorized_signal import CenteredFactorizedSignal, signal_circuit as subset_circuit
from .combined_qsp import response
from .decimal_enclosure import Interval as I
from .storage import ROOT, start_run, finish_run, write_json, sha256


def cost(qc):
    if not isinstance(qc,QuantumCircuit):
        wrapped = QuantumCircuit(qc.num_qubits)
        wrapped.append(qc,range(qc.num_qubits))
        qc = wrapped
    native = transpile(qc,basis_gates=['u','cx'],optimization_level=1,seed_transpiler=717)
    return dict(qubits=native.num_qubits,cx=int(native.count_ops().get('cx',0)),
                u=int(native.count_ops().get('u',0)),depth=native.depth())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    args = parser.parse_args()
    config = dict(compiled_dimensions=[2,4],compiled_q=[1,2],structural_dimensions=[4,8,16],
                  production_q=10,degrees=[16,32,64,128],strike=100,cutoff=4,
                  scope='development signal-only resources, not end-to-end pricing advantage')
    path = start_run(args.output,config)
    source = ROOT/'results/journal_sprint/normalization_approximation_v1'
    prior = {name:json.loads((source/name).read_text()) for name in
             ['model.json']+['minimax_%d.json'%n for n in config['degrees']]}
    write_json(path/'inputs.json',dict(protocol_sha256=sha256(ROOT/'docs/journal_sprint/MINIMAL_PIVOT_STUDY_PLAN.md'),
        archive_sha256={name:sha256(source/name) for name in prior},
        source_model=prior['model.json']))
    circuits = []
    for d in config['compiled_dimensions']:
        model = setup(Basket(1 if d==2 else 2,2,100))
        for q in config['compiled_q']:
            for mode in ('original','reflection'):
                plan = ReflectionSignal(model['means'],model['factor'],100,q,4,mode)
                qc,certificate = signal_circuit(plan)
                entry = dict(**plan.metadata(),certificate=certificate,cost=cost(qc),
                             controlled_cost=cost(qc.to_gate().control()))
                # Wrap gates for a genuine controlled-signal cost.
                circuits.append(entry)
                print('compiled',d,q,mode,entry['cost'],flush=True)
        if d==2:
            for label,cls,build in [('legacy_original',FactorizedSignal,old_circuit),
                                   ('legacy_subset',CenteredFactorizedSignal,subset_circuit)]:
                plan = cls(model['means'],model['factor'],100,1,4)
                circuits.append(dict(mode=label,d=d,q=1,radius=plan.B,cost=cost(build(plan))))
    write_json(path/'circuits.json',circuits)
    structure = []
    for d in config['structural_dimensions']:
        model = setup(Basket(2,d//2,100))
        for mode in ('original','reflection'):
            structure.append(ReflectionSignal(model['means'],model['factor'],100,10,4,mode).metadata())
    write_json(path/'structure.json',structure)
    # Exact original archived binary model, avoiding a new LAPACK factor choice.
    model = prior['model.json']
    production = ReflectionSignal(model['means'],model['factor'],100,10,4)
    qc,certificate = signal_circuit(production)
    write_json(path/'production.json',dict(**production.metadata(),certificate=certificate,cost=cost(qc),
                                         native_rotation_model='ideal u/cx, no physical synthesis'))
    print('production q10 compiled',flush=True)
    data = grid(Basket(2,2,100),2,4)
    if not np.array_equal(data['model']['factor'],model['factor']):
        raise ArithmeticError('diagnostic factor differs from archived model')
    A = np.exp(np.asarray(model['means'])+data['normals']@np.asarray(model['factor']).T).mean(axis=1)
    discount = math.exp(-.03)
    true_price = discount*float(data['weights']@np.maximum(A-100,0))
    rows = []
    for mode in ('original','reflection'):
        plan = ReflectionSignal(model['means'],model['factor'],100,2,4,mode)
        for degree in config['degrees']:
            record = prior['minimax_%d.json'%degree]
            candidate,residual,synthesis = record['candidate'],record['residual'],record['synthesis']
            x = (A-100)/plan.B
            high = chebval(x,candidate['coefficients'])
            low = chebval(x,model['low_coefficients'])
            approximate = discount*plan.B/2*float(data['weights']@(x+high))
            offset = discount*plan.B/2*float(data['weights']@(x+low))
            phased = offset+discount*plan.B/2*residual['rho']*float(data['weights']@response(x,synthesis['phases']).real)
            # Scalar diagnostics use the archived outward binary radius, not
            # the exact-real radius interval of the signal certificate.
            error_bound = I(discount)*I(plan.B)/2*I(candidate['uniform_error_upper'])
            rows.append(dict(mode=mode,degree=degree,radius=plan.B,true_finite_price=true_price,
                             approximate_price=approximate,phase_price=phased,
                             phase_discrepancy=abs(phased-approximate),finite_bias=approximate-true_price,
                             ideal_uniform_payoff_bound=str(error_bound.hi),
                             scalar_simulation_only=True))
    # Common ideal payoff-approximation targets on a fixed degree menu.
    screens = []
    for tolerance in (.7,1.,2.,5.):
        for mode in ('original','reflection'):
            passing = [r for r in rows if r['mode']==mode and float(r['ideal_uniform_payoff_bound'])<=tolerance]
            chosen = min(passing,key=lambda r:r['degree']) if passing else None
            signal = next(r for r in circuits if r['d']==4 and r['q']==2 and r['mode']==mode)
            screens.append(dict(tolerance=tolerance,mode=mode,degree=chosen['degree'] if chosen else None,
                signal_cx_times_degree=chosen['degree']*signal['cost']['cx'] if chosen else None,
                scope='proxy excludes probability preparation, phase projectors, AE, synthesis and statistical error'))
    write_json(path/'payoff.json',dict(rows=rows,screens=screens,
        quantum_advantage=False,confirmation=False,continuous_target_certified=False))
    finish_run(path)


if __name__ == '__main__':
    main()
