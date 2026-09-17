"""Bounded component-composed comparison; no hardware/confirmation admission."""

import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path

import numpy as np

from .arithmetic_plan import raw_plan
from .asian_basket import setup
from .asian_encoding import grid
from .claim_assessment import projected_cost, schedule
from .combined_qsp import response
from .decimal_enclosure import Interval as I
from .encoding_enclosure import at_precision, base_enclosure
from .fixed_exp_budget import evaluate_integer
from .matched_aggregation import aggregation_resources
from .reviewed_reflection_signal import ReviewedReflectionSignal
from .run_minimal_pivot_week1 import cost
from .run_minimal_pivot_week2 import CASES, archives, contract_of
from .storage import ROOT, finish_run, sha256, start_run, write_json
from .week2_pipeline import controlled_zero, loader


PROTOCOL = 'docs/journal_sprint/MATCHED_ARITHMETIC_PROTOCOL_20260917.md'
PRODUCTION = 'results/journal_sprint/minimal_pivot_week2_production_v1/results.json'
CONFIG = dict(cases=['D1', 'D2'], finite_q=[1, 2], production_q=10,
              fraction_bits=20, width=40, degree=24, tolerance='1',
              confidence='0.95', repetitions=17, call_cap=10_000_000,
              candidate_status='standby', development_only=True)


def plan_for(contract, model, q):
    return raw_plan(model['means'], model['factor'], normal_bits=q, cutoff=4,
                    fraction_bits=CONFIG['fraction_bits'], width=CONFIG['width'],
                    degree=CONFIG['degree'], spot=100, strike=int(contract.strike),
                    discount=(-I(str(contract.rate))*I(str(contract.maturity))).exp())


def integer_payoffs(plan, packed):
    scale = 1 << plan['fraction_bits']
    rows = plan['affine_rows']
    result = []
    for word in packed:
        logs = [a+sum(((int(word) >> i) & 1)*c for i, c in enumerate(cs))
                for a, cs in rows]
        prices = [evaluate_integer(x, plan['exp_budget']['coefficients'],
                                   plan['fraction_bits']) for x in logs]
        payoff = max(sum(prices)-plan['strike_sum'], 0)
        if payoff >= 1 << plan['selector_bits']:
            raise ArithmeticError('selector truncates payoff')
        result.append(payoff/scale/len(rows))
    return np.asarray(result)


def finite_diagnostic(case, q, data):
    contract = contract_of(case)
    finite = grid(contract, q, 4)
    model = finite['model']
    plan = plan_for(contract, model, q)
    if not plan['overflow_safe']:
        raise ArithmeticError('finite arithmetic overflow certificate failed')
    discount = math.exp(-contract.rate*contract.maturity)
    prices = np.exp(model['means']+finite['normals']@model['factor'].T).mean(axis=1)
    target = discount*np.maximum(prices-contract.strike, 0)
    arithmetic = discount*integer_payoffs(plan, range(len(target)))
    observed = float(np.max(np.abs(arithmetic-target)))
    if observed > float(plan['arithmetic_price_error_upper'])+1e-10:
        raise ArithmeticError('arithmetic diagnostic exceeds analytic bound')
    reflection = ReviewedReflectionSignal(model['means'], model['factor'],
                                          contract.strike, q, 4, 'reflection')
    x = (prices-contract.strike)/reflection.B
    low = data['model.json']['low_coefficients']
    from numpy.polynomial.chebyshev import chebval
    rows = []
    for degree in (16, 32, 64, 128):
        record = data['minimax_%d.json' % degree]
        approximation = discount*reflection.B/2*(x+chebval(x, low)
            +record['residual']['rho']*response(x, record['synthesis']['phases']).real)
        rows.append(dict(degree=degree, price=float(finite['weights']@approximation),
                         max_pointwise_error=float(np.max(np.abs(approximation-target)))))
    return dict(case=case['id'], q=q, paths=len(target),
                target_price=float(finite['weights']@target),
                arithmetic_price=float(finite['weights']@arithmetic),
                arithmetic_max_pointwise_error=observed,
                arithmetic_price_error_upper=plan['arithmetic_price_error_upper'],
                overflow_safe=True, reflection=rows,
                scope='exhaustive scalar finite-grid diagnostic, not circuit simulation or continuous price')


def arithmetic_budget(contract, model, plan, loader_error, angle_error):
    representation = at_precision(base_enclosure(contract, model, 4, 'raw'), 10)
    sensitivity = I(plan['sensitivity_upper'])
    beta_interval = sensitivity/2
    beta = float(beta_interval.hi)
    # Exact beta is rounded upward before use in the rational schedule.
    if I(beta).lo < beta_interval.hi:
        beta = math.nextafter(beta, math.inf)
    # A includes d loaders, aggregation and its inverse. Probability deviation
    # <=2||A-Aideal||. AE estimates the stored-angle unitary's probability.
    parts = dict(representation=I(representation['partial_sum']['upper']),
                 arithmetic=I(plan['arithmetic_price_error_upper']),
                 preparation=2*sensitivity*len(model['means'])*I.coerce(loader_error),
                 aggregation=4*sensitivity*I(angle_error),
                 decoding=I(16)*I(2.**-52)*sensitivity+I(2.**-1022))
    decoder_scale = 2*beta
    exact_scale = (I(plan['discount_lower'], plan['discount_upper'])*(1 << plan['selector_bits'])
                   /(1 << plan['fraction_bits'])/len(model['means']))
    decoder_bridge = ((I(decoder_scale)-exact_scale).absolute()
                      +I(2.**-52)*I(abs(decoder_scale))+I(2.**-1022))
    if decoder_bridge.hi > parts['decoding'].lo:
        raise ArithmeticError('declared decoder bridge exceeds allowance')
    total = sum(parts.values(), I(0))
    return dict(components={k: str(v.hi) for k, v in parts.items()},
                deterministic_upper=str(total.hi), sensitivity_upper=plan['sensitivity_upper'],
                beta_upper=beta, schedule=schedule(F(beta), F(total.hi)),
                decoder_scale=decoder_scale, decoder_bridge_upper=str(decoder_bridge.hi),
                probability_decoding='ideal sin-squared AE label; one binary64 scale multiplication',
                physical_execution_error=None, confirmation_admitted=False)


def full_resources(native, num_qubits, ae):
    """Same gate-by-gate conservative control convention as reflection W2."""
    cx, u = native['cx'], native['u']
    zero = cost(controlled_zero(num_qubits))['cx']
    result = dict(a_cx_projection=cx, a_u_projection=u,
                  controlled_a_cx_projection=6*cx+2*u,
                  zero_reflection_cx_projection=zero,
                  clean_workspace_qubits=num_qubits-2, a_qubits=num_qubits,
                  total_qubits=None, total_cx_projection=None,
                  state_preparation_included=True, inverses_included=True,
                  qft_included=True, physical_execution_error=None,
                  scope='conservative component composition, not a full transpiled or simulated AE circuit')
    if ae['status'] == 'ideal_plan':
        result['total_cx_projection'] = projected_cost(result, ae['M'], ae['repetitions'])
        result['total_qubits'] = 2*num_qubits-2+ae['phase_qubits']
    result['control_cancelled_total_cx_projection'] = cancelled_cost(result, ae)
    return result


def cancelled_cost(resources, ae):
    if ae['status'] != 'ideal_plan':
        return None
    adjusted = {**resources, 'controlled_a_cx_projection': resources['a_cx_projection']}
    return projected_cost(adjusted, ae['M'], ae['repetitions'])


def reflected_rows(case, model, archived):
    plan = ReviewedReflectionSignal(model['means'], model['factor'],
                                   contract_of(case).strike, 10, 4, 'reflection')
    if plan.negative_constant:
        raise ValueError('unexpected sign: cannot reuse archived positive-constant circuit')
    rows = []
    for row in archived['rows']:
        if row['case']['id'] != case['id'] or row['mode'] != 'reflection':
            continue
        if row['case'] != case or row['plan']['q'] != 10 or row['plan']['radius'] != plan.B:
            raise ValueError('archived reflection target mismatch')
        b = row['budget']
        ae = schedule(F(b['beta']), F(b['deterministic_upper']))
        if (ae['status'], ae['M']) != (b['schedule']['status'], b['schedule']['M']):
            raise ValueError('reflection schedule mismatch')
        r = dict(row['resources'])
        r['total_cx_projection'] = (projected_cost(r, ae['M'], ae['repetitions'])
                                    if ae['status'] == 'ideal_plan' else None)
        r['control_cancelled_total_cx_projection'] = cancelled_cost(r, ae)
        rows.append(dict(mode='reflection', degree=b['degree'], budget={**b, 'schedule': ae},
                         resources=r, evidence='archived W2, corrected IQFT swaps, positive sign checked'))
    if len(rows) != 4:
        raise ValueError('reflection degree menu incomplete')
    return rows


def run(path):
    from .matched_arithmetic import arithmetic_components
    from .verify_minimal_pivot_week2 import verify_archive
    data, inputs = archives()
    inputs[PRODUCTION] = sha256(ROOT/PRODUCTION)
    for name in ('planned.json', 'complete.json'):
        relative = str(Path(PRODUCTION).with_name(name)).replace('\\', '/')
        inputs[relative] = sha256(ROOT/relative)
    config = {**CONFIG, 'protocol_sha256': sha256(ROOT/PROTOCOL)}
    path = start_run(path, config)
    try:
        write_json(path/'inputs.json', inputs)
        prior_integrity = verify_archive((ROOT/PRODUCTION).parent)
        archived = json.loads((ROOT/PRODUCTION).read_text(encoding='utf-8'))
        finite = [finite_diagnostic(c, q, data) for c in CASES[:2] for q in (1, 2)]
        write_json(path/'finite.json', finite)
        marginal, marginal_error = loader(10)
        marginal_cost = cost(marginal)
        comparisons = []
        for case in CASES[:2]:
            print('component acquisition', case['id'], flush=True)
            contract = contract_of(case)
            model = setup(contract)
            plan = plan_for(contract, model, 10)
            if not plan['overflow_safe']:
                raise ArithmeticError('production arithmetic overflow certificate failed')
            components = arithmetic_components(plan)
            alternatives = reflected_rows(case, model, archived)
            aggregations = {}
            for mode in ('ripple', 'fourier'):
                aggregation = aggregation_resources(plan['width'], len(model['means']), mode,
                                                    zero_initialized=True)
                aggregations[mode] = aggregation
                b = arithmetic_budget(contract, model, plan, marginal_error,
                                      aggregation['angle_error_upper'])
                base = components['native_excluding_aggregation']
                native = {k: base[k]+2*aggregation['uncontrolled'][k]
                          +len(model['means'])*marginal_cost[k] for k in ('u', 'cx')}
                # Selector H plus conservative controlled-global-phase allowance.
                native['u'] += plan['selector_bits']+1
                n = components['a_qubits_excluding_aggregation_helper']+(mode == 'ripple')
                r = full_resources(native, n, b['schedule'])
                alternatives.append(dict(mode=mode, degree=plan['degree'], budget=b, resources=r))
            eligible = [a for a in alternatives if a['resources']['total_cx_projection'] is not None]
            winner = min(eligible, key=lambda a: a['resources']['total_cx_projection']) if eligible else None
            secondary = min(eligible, key=lambda a: a['resources']['control_cancelled_total_cx_projection']) if eligible else None
            result = dict(case=case, arithmetic_plan=plan, arithmetic_components=components,
                          aggregation=aggregations, alternatives=alternatives,
                          lowest_projection=None if winner is None else dict(mode=winner['mode'], degree=winner['degree']),
                          lowest_control_cancelled_projection=None if secondary is None else dict(mode=secondary['mode'], degree=secondary['degree']),
                          production_choice=None, quantum_advantage=False, confirmation=False)
            write_json(path/('case_'+case['id']+'.json'), result)
            comparisons.append(result)
            print(case['id'], result['lowest_projection'], flush=True)
        results = dict(comparisons=comparisons, candidate_status='standby',
                       prior_archive_integrity=prior_integrity,
                       quantum_over_classical_advantage_established=False, confirmation_admitted=False,
                       scope='bounded matched ideal logical component projections; not optimized external solvers')
        write_json(path/'results.json', results)
        planned = json.loads((path/'planned.json').read_text(encoding='utf-8'))
        for name, digest in {**planned['source_sha256'], **inputs, PROTOCOL: config['protocol_sha256']}.items():
            if sha256(ROOT/name) != digest:
                raise ValueError('source/input changed during acquisition: '+name)
        finish_run(path)
    except BaseException as error:
        write_json(path/'failed.json', dict(type=type(error).__name__, message=str(error)))
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    run(parser.parse_args().output)
