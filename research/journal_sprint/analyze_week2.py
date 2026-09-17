"""Transparent W2 summaries and independent analytic AE-distribution checks."""
import argparse
import math
from pathlib import Path
import numpy as np
from numpy.polynomial.chebyshev import chebval
from .storage import ROOT, sha256, write_json
from .verify_minimal_pivot_week2 import read
from .run_minimal_pivot_week2 import CASES, contract_of, archives
from .asian_encoding import grid
from .reflection_centered_signal import ReflectionSignal
from .week2_decoding import median_price


def corrected_cost(row):
    """Explicit replacement IQFT uses swaps; original projection omitted them."""
    schedule = row['budget']['schedule']
    swap_cx = schedule['repetitions']*3*(schedule['phase_qubits']//2)
    return row['resources']['total_cx_projection']+swap_cx,swap_cx


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    args = parser.parse_args()
    base = ROOT/'results/journal_sprint'
    paths = {k:base/('minimal_pivot_week2_'+k+suffix)/'results.json'
             for k,suffix in [('tiny','_v2'),('production','_v1'),('classical','_v1')]}
    data = {k:read(p) for k,p in paths.items()}
    comparisons = []
    for case in CASES:
        alternatives = {}
        for mode in ('original','reflection'):
            eligible = [r for r in data['production']['rows'] if r['case']['id']==case['id']
                        and r['mode']==mode and r['budget']['schedule']['status']=='ideal_plan']
            winner = min(eligible,key=lambda r:corrected_cost(r)[0]) if eligible else None
            alternatives[mode] = None if winner is None else dict(degree=winner['budget']['degree'],
                deterministic_upper=winner['budget']['deterministic_upper'],
                statistical_upper=winner['budget']['schedule']['statistical_dollar_bound'],
                a_calls=winner['budget']['schedule']['a_calls'],
                projected_cx=corrected_cost(winner)[0],
                raw_projected_cx=winner['resources']['total_cx_projection'],
                explicit_iqft_swap_cx=corrected_cost(winner)[1],
                qubits=winner['resources']['total_qubits'])
        ratio = None
        if all(alternatives.values()):
            ratio = alternatives['original']['projected_cx']/alternatives['reflection']['projected_cx']
        classical = [r for r in data['classical'] if r['case']==case['id'] and r['power']==12]
        comparisons.append(dict(case=case,alternatives=alternatives,
            original_over_reflection_projected_cx=ratio,
            classical=[{k:r[k] for k in ('method','price','approximate_95_halfwidth','paths_with_pilot')} for r in classical]))
    ae_checks = []
    archived,_ = archives()
    c = contract_of(CASES[0])
    finite = grid(c,1,4)
    model = finite['model']
    average = np.exp(model['means']+finite['normals']@model['factor'].T).mean(axis=1)
    for row in data['tiny']:
        p = row['probability']
        theta = math.asin(math.sqrt(p))/math.pi
        expected = np.zeros(8)
        for sign in (-1,1):
            delta = sign*theta-np.arange(8)/8
            expected += abs(np.exp(2j*np.pi*np.outer(delta,np.arange(8))).sum(axis=1)/8)**2/2
        error = float(np.max(abs(expected-row['ae_distribution'])))
        if error>2e-10:
            raise ArithmeticError('AE distribution fails analytic Fourier-kernel check')
        plan = ReflectionSignal(model['means'],model['factor'],c.strike,1,4,row['mode'])
        x = (average-c.strike)/plan.B
        factor = math.exp(-c.rate*c.maturity)*plan.B/2
        beta = factor*archived['minimax_16.json']['residual']['rho']
        offset = factor*float(finite['weights']@(x+chebval(x,archived['model.json']['low_coefficients'])))
        decoded = median_price(row['simulated_measurements'],8,offset,beta)
        ae_checks.append(dict(mode=row['mode'],distribution_max_error=error,
            directed_decoder=decoded,
            old_libm_decoder_difference=abs(decoded['value']-row['simulated_ae_price'])))
    write_json(args.output,dict(comparisons=comparisons,analytic_ae_checks=ae_checks,
        inputs_sha256={k:sha256(p) for k,p in paths.items()},
        analyzer_sha256=sha256(Path(__file__)),candidate_status='standby',
        projection_correction='charge 3 CX per explicit inverse-QFT swap, floor(m/2) swaps per repetition; raw archives preserved',
        quantum_over_classical_advantage_established=False,confirmation_admitted=False,
        scope='logical composition projections and classical approximate intervals; no matched hardware runtime claim'))
    print('Compared all cases and independently checked actual AE distributions.')


if __name__=='__main__':
    main()
