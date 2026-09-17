"""Exclusive bounded W2 integration, resource and classical acquisitions."""
import argparse
from dataclasses import asdict
import json
import math
from pathlib import Path
import time
import numpy as np
from numpy.polynomial.chebyshev import chebval
from scipy.stats import t
from qiskit.quantum_info import Statevector
from qiskit.algorithms import AmplitudeEstimation, EstimationProblem
from .asian_basket import Basket, setup, fit_control, estimate
from .asian_encoding import grid
from .combined_qsp import response
from .control_offset_enclosure import moment_enclosure
from .decimal_enclosure import Interval as I, pi_interval
from .encoding_enclosure import base_enclosure, at_precision
from .factorized_signal import projected_phase
from .reflection_centered_signal import ReflectionSignal, signal_circuit
from .run_minimal_pivot_week1 import cost
from .week2_pipeline import loader, walk, readout, budget, phase_error, composition_resources, choose
from .storage import ROOT, start_run, finish_run, write_json, sha256


CASES = [dict(id='D1',split='development',assets=1,dates=2,sigma=.2,strike=95.,correlation=.3),
         dict(id='D2',split='development',assets=2,dates=2,sigma=.25,strike=105.,correlation=.4),
         dict(id='E1',split='reserved_evaluation',assets=1,dates=3,sigma=.35,strike=110.,correlation=.6),
         dict(id='E2',split='reserved_evaluation',assets=2,dates=2,sigma=.4,strike=90.,correlation=.7)]
DEGREES = (16,32,64,128)


def contract_of(case):
    return Basket(**{k:v for k,v in case.items() if k not in ('id','split')})


def archives():
    source = ROOT/'results/journal_sprint/normalization_approximation_v1'
    names = ['model.json']+['minimax_%d.json'%d for d in DEGREES]
    data = {n:json.loads((source/n).read_text()) for n in names}
    return data,{str((source/n).relative_to(ROOT)):sha256(source/n) for n in names}


def tiny(data):
    contract = contract_of(CASES[0])
    finite = grid(contract,1,4)
    model = finite['model']
    A = np.exp(model['means']+finite['normals']@model['factor'].T).mean(axis=1)
    discount = math.exp(-contract.rate*contract.maturity)
    marginal,_ = loader(1)
    low = data['model.json']['low_coefficients']
    record = data['minimax_16.json']
    rows = []
    for mode in ('original','reflection'):
        plan = ReflectionSignal(model['means'],model['factor'],contract.strike,1,4,mode)
        signal,_ = signal_circuit(plan)
        unitary,_ = walk(plan,signal,record['synthesis']['phases'])
        prep = readout(plan,unitary,marginal)
        state = Statevector.from_instruction(prep)
        probability = float(state.probabilities([plan.num_qubits])[1])
        x = (A-contract.strike)/plan.B
        scalar_probability = (1-float(finite['weights']@response(x,record['synthesis']['phases']).real))/2
        if abs(probability-scalar_probability)>2e-11:
            raise ArithmeticError('integrated readout differs from independent scalar target')
        beta = discount*plan.B/2*record['residual']['rho']
        offset = discount*plan.B/2*float(finite['weights']@(x+chebval(x,low)))
        problem = EstimationProblem(prep,objective_qubits=[plan.num_qubits])
        ae = AmplitudeEstimation(3).construct_circuit(problem,measurement=False)
        distribution = Statevector.from_instruction(ae).probabilities(list(range(3)))
        labels = np.sin(np.pi*np.arange(8)/8)**2
        threshold = math.pi/8+math.pi**2/64
        success = float(distribution[abs(labels-probability)<=threshold].sum())
        if success < 8/math.pi**2-1e-10:
            raise ArithmeticError('AE theorem or phase-register convention mismatch')
        draws = np.random.default_rng(9217).choice(8,size=21,p=distribution/distribution.sum())
        amp_estimate = float(np.median(labels[draws]))
        rows.append(dict(mode=mode,contract=asdict(contract),finite_q=1,
            finite_truth=discount*float(finite['weights']@np.maximum(A-contract.strike,0)),
            scalar_payoff=discount*plan.B/2*float(finite['weights']@(x+chebval(x,record['candidate']['coefficients']))),
            integrated_qsp_price=offset+beta*(1-2*probability),
            probability=probability,scalar_probability=scalar_probability,
            ae_distribution=distribution.tolist(),ae_success_probability=success,
            simulated_measurements=draws.tolist(),simulated_ae_price=offset+beta*(1-2*amp_estimate),
            ae_statistical_price_radius=2*beta*threshold,
            readout_cost=cost(prep),ae_cost=cost(ae),
            a_calls_per_ae=15,a_calls_for_21_repetitions=315,
            scope='actual small ideal statevector circuit; classical simulated measurements; finite target only'))
        print('tiny',mode,'readout',probability,'AE success',success,flush=True)
    return rows


def production(data,path,timings):
    q = 10
    start = time.perf_counter()
    marginal,marginal_error = loader(q)
    marginal_cost = cost(marginal)
    timings['shared_loader_seconds'] = time.perf_counter()-start
    rows,decisions = [],[]
    for case in CASES:
        begin = time.perf_counter()
        contract = contract_of(case)
        model = setup(contract)
        representation = at_precision(base_enclosure(contract,model,4,'raw'),q)
        moments = moment_enclosure(model['means'],model['factor'],q,4)['moments']
        case_rows = []
        for mode in ('original','reflection'):
            plan = ReflectionSignal(model['means'],model['factor'],contract.strike,q,4,mode)
            signal,certificate = signal_circuit(plan)
            signal_cost = cost(signal)
            for degree in DEGREES:
                record = data['minimax_%d.json'%degree]
                phases = record['synthesis']['phases']
                p_error = degree*(I(math.pi)-pi_interval()).absolute()
                for phi in phases:
                    phase = projected_phase(plan.num_qubits,plan.good_qubits,float(phi))
                    p_error += phase_error(phase,float(phi))
                b = budget(contract,plan,record,data['model.json']['low_coefficients'],moments,
                           representation,certificate['operator_error_upper'],marginal_error,p_error)
                resources = composition_resources(plan,signal_cost,marginal_cost,phases,b['schedule'])
                row = dict(case=case,mode=mode,plan=plan.metadata(),budget=b,resources=resources,
                           signal_cost=signal_cost,signal_certificate=certificate)
                case_rows.append(row)
                print(case['id'],mode,degree,b['deterministic_upper'],b['schedule']['status'],flush=True)
            del signal
        rows.extend(case_rows)
        decisions.append(dict(case=case['id'],**choose(case_rows)))
        write_json(path/('case_'+case['id']+'.json'),case_rows)
        timings[case['id']+'_setup_compile_certify_seconds'] = time.perf_counter()-begin
    return dict(rows=rows,decisions=decisions,
                candidate_status='standby',quantum_advantage=False,confirmation=False)


def classical(timings):
    rows = []
    for case_index,case in enumerate(CASES):
        contract = contract_of(case)
        begin = time.perf_counter()
        model = setup(contract)
        setup_seconds = time.perf_counter()-begin
        for method_index,method in enumerate(('mc_cv','rqmc_cv','conditional_cv')):
            begin = time.perf_counter()
            beta,residual = fit_control(contract,model,np.random.default_rng(81100+case_index*10+method_index),
                                      conditional=method=='conditional_cv',count=1024)
            pilot_seconds = time.perf_counter()-begin
            for power in (10,12):
                begin = time.perf_counter()
                estimates,roots = [],[]
                seeds = [83100+case_index*1000+method_index*100+power*17+r for r in range(16)]
                for seed in seeds:
                    value,root = estimate(contract,model,power,seed,method,beta)
                    estimates.append(value)
                    roots.append(root)
                elapsed = time.perf_counter()-begin
                mean = float(np.mean(estimates))
                radius = float(t.ppf(.975,15)*np.std(estimates,ddof=1)/4)
                rows.append(dict(case=case['id'],split=case['split'],contract=asdict(contract),
                    method=method,power=power,seeds=seeds,replicates=estimates,
                    price=mean,approximate_95_halfwidth=radius,beta=beta,
                    approximate_one_dollar_precision=radius<=1,
                    paths_with_pilot=16*2**power+1024,root_residual=max([residual]+roots),
                    continuous_target=True,rigorous_coverage_certificate=False))
                timings[case['id']+'_'+method+'_'+str(power)] = dict(setup=setup_seconds,pilot=pilot_seconds,
                    evaluation=elapsed,total=setup_seconds+pilot_seconds+elapsed)
        print('classical',case['id'],'complete',flush=True)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('part',choices=['tiny','production','classical'])
    parser.add_argument('output',type=Path)
    args = parser.parse_args()
    path = start_run(args.output,dict(part=args.part,cases=CASES,degrees=DEGREES,q=10,alpha=.05,tolerance=1))
    data,hashes = archives()
    write_json(path/'inputs.json',dict(archive_sha256=hashes,
        protocol_sha256=sha256(ROOT/'docs/journal_sprint/MINIMAL_PIVOT_WEEK2_PROTOCOL.md')))
    timings = {}
    try:
        result = tiny(data) if args.part=='tiny' else production(data,path,timings) if args.part=='production' else classical(timings)
        write_json(path/'results.json',result)
        write_json(path/'timings.json',timings)
        finish_run(path)
    except Exception as error:
        write_json(path/'failure.json',dict(type=type(error).__name__,message=str(error)))
        raise


if __name__=='__main__':
    main()
