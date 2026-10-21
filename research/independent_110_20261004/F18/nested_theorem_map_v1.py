"""One frozen compound-contract theorem map; no simulation or shared imports."""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/independent_110_20261004/F18/run001'
DOC = ROOT / 'docs/independent_110_20261004/F18'
AUTHOR = Path(__file__).resolve()
PROOF = DOC / 'NESTED_ASSUMPTIONS.txt'
CORPUS = [ROOT / p for p in [
    'research/compound_feasibility/model.py',
    'research/compound_feasibility/quantum_schedule.py',
    'research/compound_feasibility/multilevel.py',
    'docs/compound_feasibility/PROTOCOL.md',
    'docs/compound_feasibility/RESULTS.md',
    'docs/limitation_audit_20261001/implementation_plan/roadmap.json',
    'docs/independent_110_20261004/F16/PROOF_AND_LIMITS.txt',
    'docs/independent_110_20261004/E17/MOMENT_PROOF_v2.md',
    'research/independent_110_20261004/F18/primary_sources/Sun_Wang_Blanchet_2602_08120v1.html',
]]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def pair(q):
    return [q.numerator, q.denominator]

def dump(p, v):
    p.write_text(json.dumps(v, indent=2, sort_keys=True) + '\n')

def prepare():
    if OUT.exists():
        raise ValueError('Fresh F18 output required')
    assert PROOF.exists()
    OUT.mkdir(parents=True)
    dump(OUT / 'protocol.json', {'author_sha256': sha(AUTHOR), 'proof_sha256': sha(PROOF),
        'corpus': {str(p.relative_to(ROOT)).replace('\\', '/'): sha(p) for p in CORPUS},
        'contract': 'Existing uncapped GBM compound Asian basket, C4/C8/H4/H8; original strikes3/6/9; no contract activation or change.',
        'assumptions': ['Ideal exact-date GBM population; historical capped and finite-source variants need separately charged bias.',
                        'Paper block-history interpretation is recorded separately from its literal scalar notation; no implementable scalar reduction is assumed.',
                        'External theorem exponents apply in their stated error norms and fixed-depth unit-cost model only.'],
        'corpus_math': {'strikes': [3, 6, 9], 'discount_rationals': [[1,1], [9,10], [99,100]],
                        'z_grid': [-2,-1,0,1,2,3,4,6,9],
                        'epsilon_dollars': [[1,10], [3,100], [1,100]],
                        'diagnostic_bias_fractions': [[0,1], [1,10], [1,2]],
                        'diagnostic_failure_allocations': [[1,250], [3,1000], [1,100]]},
        'acceptance': ['Analytic global Lipschitz/moment arguments with fixed exact boundary diagnostics.',
                       'Every exponent has norm, depth and primary locator; scalar/block and conditional-source transfer obligations explicit.',
                       'RMSE/Lp conversion includes dollar bias and remaining joint failure allowances; unknown execution inputs never become zero.',
                       'Classical factor reuse/control setup and crossed dependence are retained; no cubic classical baseline is assumed.'],
        'budgets': {'cpu_seconds': 30, 'wall_seconds': 60, 'output_bytes': 4*1024*1024},
        'stop': 'One current-contract theorem map; no new simulation, paper search or compilation after missing implementable access is found.',
        'new_finance_draws': 0, 'new_global_fixture_credit': 0})
    print('F18 theorem map prospectively frozen.')

def run():
    cpu, wall = time.process_time(), time.monotonic()
    protocol = json.loads((OUT / 'protocol.json').read_text())
    assert not (OUT / 'RUN_STARTED.json').exists()
    assert sha(AUTHOR) == protocol['author_sha256'] and sha(PROOF) == protocol['proof_sha256']
    for path, expected in protocol['corpus'].items():
        assert sha(ROOT/path) == expected
    dump(OUT/'RUN_STARTED.json', {'finance_draws': 0, 'theorem_map_count': 1})
    m = protocol['corpus_math']
    diagnostics = []
    for strike in m['strikes']:
        for num, den in m['discount_rationals']:
            discount = Q(num, den)
            for a in m['z_grid']:
                for b in m['z_grid']:
                    lhs = abs(discount*max(Q(a-strike),0)-discount*max(Q(b-strike),0))
                    rhs = discount*abs(a-b)
                    assert lhs <= rhs
                    diagnostics.append({'strike': strike, 'discount': pair(discount), 'a': a, 'b': b,
                                        'difference': pair(lhs), 'bound': pair(rhs)})
    conversions = []
    for epsilon_pair in m['epsilon_dollars']:
        epsilon = Q(*epsilon_pair)
        for bias_pair in m['diagnostic_bias_fractions']:
            bias = epsilon*Q(*bias_pair)
            margin = epsilon-bias
            for alpha_pair in m['diagnostic_failure_allocations']:
                alpha = Q(*alpha_pair)
                rmse2 = alpha*margin*margin
                assert rmse2/(margin*margin) == alpha
                conversions.append({'epsilon': pair(epsilon), 'diagnostic_bias': pair(bias),
                    'statistical_margin': pair(margin), 'stat_failure': pair(alpha),
                    'sufficient_dollar_rmse_squared': pair(rmse2),
                    'remaining_total_99_failure_allowance': pair(Q(1,100)-alpha),
                    'actual_algorithm_rmse_and_other_failures_certified': False})
    # Negative controls: allocating only RMSE <= epsilon permits failure near one;
    # bias consumes the dollar margin, and other failures consume joint allowance.
    negative = [
        {'reason': 'RMSE equals target alone only bounds failure by1', 'failure_upper_bound': [1,1]},
        {'reason': 'Uncharged bias exhausts margin', 'epsilon': [1,100], 'bias': [1,100], 'admissible': False},
        {'reason': 'Statistical and other failure sum exceeds1%', 'sum': pair(Q(1,100)+Q(1,1000)), 'admissible': False},
        {'reason': 'Absent conditional coherent access cannot be charged zero', 'conditional_cost': None, 'admissible': False},
    ]
    assumptions = [
        {'id':'target', 'status':'proved', 'result':'One outer positive part of one conditional inner payoff; fixed block depthD=1 gives two expectation operators.'},
        {'id':'outer_Lipschitz', 'status':'proved', 'result':'g0(x,z)=d0(z-Kc)+; global constantL0=d0<=1; its kink does not violate Lipschitz.'},
        {'id':'terminal_L2', 'status':'proved_ideal_GBM', 'result':'H<=d1*A. Jensen gives E[H^2]<=d1^2/(d*N) sum_i,l E[S_i(t_l)^2]<infinity; correlated drivers do not affect marginal finiteness.'},
        {'id':'history_representation', 'status':'unresolved_literal_scalar_transfer', 'result':'X and future paths are vector blocks. Paper writes scalar coordinates; no emitted unit-cost scalar encoding or separately checked vector theorem is supplied.'},
        {'id':'finite_digital_law', 'status':'unresolved', 'result':'Gaussian clipping/loading, arithmetic, caps and synthesis have price-law errors requiring separate certification.'},
        {'id':'conditional_coherent_access', 'status':'unresolved', 'result':'Coherent conditional prep, payoff, inverse and level decoding/median/reflection schedule for this theorem are unbuilt.'},
        {'id':'error_norm', 'status':'proved_conversion_only', 'result':'Chebyshev converts an actual dollar RMSE guaranteer to stat failure<=r^2/(epsilon-bias)^2. No finite theorem constants are extracted from big-O.'},
        {'id':'joint_99', 'status':'unresolved_execution', 'result':'Conversion is available; actual norm guarantee, all deterministic biases, numerical constants and fault/readout allowances are not jointly instantiated.'},
        {'id':'classical_comparator', 'status':'included_not_retimed', 'result':'Existing factor reuse, geometric controls and fixed-policy/MLRQMC evidence; crossed samples are dependent and empirical intervals are not a rigorous99% certificate.'},
    ]
    costs = {'scope':'Oracle/cost interface, not complete-time crossover ledger.',
        'classical': {'future_setup':'J*d*n Gaussian/path/exponential work plus controls',
                      'outer_setup':'I*d*n path work', 'pair_work':'I*J*d products plus payoff/control work',
                      'reuse_and_cross_dependence': True, 'matched_cost_seconds': None,
                      'rigorous_99_financial_delivery': False},
        'quantum': {'fixed_block_depth':1, 'literal_scalar_reduction_cost':None,
                    'conditional_preparation':None, 'terminal_arithmetic':None,
                    'inverse_cleanup':None, 'outer_preparation':None,
                    'level_decoding_and_coherent_median':None, 'reflections':None,
                    'confidence_conversion_schedule':None, 'synthesis_and_fault_budget':None,
                    'readout':None, 'complete_cost':None,
                    'existing_quantum_schedule_is_compilation_of_this_theorem':False},
        'transfer_decision':'CLOSED_MISSING_IMPLEMENTABLE_ACCESS_AND_COMPLETE_CONFIDENCE_COST',
        'classical_cubic_exponent_required':False, 'quantum_advantage':False}
    dump(OUT/'assumption_map.json', assumptions)
    dump(OUT/'error_norm_conversion.json', {'conversions':conversions, 'negative_controls':negative,
        'lp_conversion':'If E|error|^p<=r^p, stat failure <=(r/(epsilon-bias))^p; RMSE usesp=2.',
        'active_allocations_changed':False})
    dump(OUT/'actual_cost_ledger.json', costs)
    dump(OUT/'diagnostics.json', {'exact_Lipschitz_cases':diagnostics, 'case_count':len(diagnostics)})
    summary = {'passed':True, 'completed':True, 'scope':'F18 one current-contract theorem/access/error-norm map, bounded stop rule.',
        'decision':costs['transfer_decision'], 'exact_Lipschitz_checks':len(diagnostics),
        'exact_conversion_checks':len(conversions), 'negative_controls':len(negative),
        'financial_delivery_certified':False, 'source_adoption':False, 'quantum_advantage':False,
        'remaining_obligations':['Literal scalar/block theorem interface.', 'Actual coherent conditional sources, finite constants, level schedule and paid function work.',
            'Joint99% dollar bias/stat/fault certificate.', 'Eligible matched factor-reuse/control comparison.'],
        'new_finance_draws':0, 'new_global_fixture_credit':0}
    for path, expected in protocol['corpus'].items():
        assert sha(ROOT/path) == expected
    assert time.process_time()-cpu <=30 and time.monotonic()-wall<=60
    dump(OUT/'summary.json', summary)
    files = [p for p in OUT.iterdir() if p.is_file()] + [PROOF]
    assert sum(p.stat().st_size for p in files)+32768 <=4*1024*1024
    dump(OUT/'manifest.json', {'files':{str(p.relative_to(ROOT)).replace('\\','/'):{'sha256':sha(p),'bytes':p.stat().st_size} for p in files},
        'author_sha256':sha(AUTHOR), 'input_pins':protocol['corpus']})
    print(json.dumps(summary))

if __name__ == '__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('mode',choices=['prepare','run']); args=ap.parse_args()
    if args.mode=='prepare':
        prepare()
    else:
        try:
            run()
        except BaseException as exc:
            if OUT.exists():
                dump(OUT/'FAILED_UNSEALED.json', {'passed':False,'completed':False,'error_type':type(exc).__name__,
                    'message':str(exc)[:2048], 'failure_overrides_partial_summary':True})
            raise
