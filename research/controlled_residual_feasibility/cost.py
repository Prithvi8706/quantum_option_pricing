"""Residual query schedules and honest partial resource/crossover screens."""
import argparse
import json
import math
from pathlib import Path
from research.compound_feasibility.model import MODELS
from research.antithetic_feasibility.estimator import schedule
from .bounds import global_moment


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);root=Path('results/controlled_residual_feasibility')
    cert=json.loads((root/'parity_iid_v1/summaries.json').read_text())
    pilot=json.loads((root/'parity_pilot_v1/summaries.json').read_text())
    original=json.loads((root/'pilot_v1/summaries.json').read_text())
    oracles=json.loads(Path('results/compound_feasibility/cost_v3/oracles.json').read_text())
    blocks=json.loads(Path('results/antithetic_feasibility/compiled_blocks_v1/blocks.json').read_text())
    cold=json.loads(Path('results/compound_feasibility/cold_timing_v1/receipts.json').read_text())
    schedules=[];rows=[];sens=[]
    for m in MODELS:
        disc=math.exp(-m.rate*m.maturity/2);error=.002/disc;support=disc*m.strike
        analytic=global_moment(m)['flat_policy_residual_second_moment_bound']
        for k in (3.,6.,9.):
            cr=next(r for r in cert if r['case']==m.name and r['strike']==k)
            pr=next(r for r in pilot if r['case']==m.name and r['strike']==k)
            old=next(r for r in original if r['case']==m.name and r['strike']==k)
            # The 2*spread bound also holds for parity: R<=q(A-G),
            # a<=q E[A-G], so E[(a-R)^2]<=E[R^2]+E[a^2]<=2M2.
            bound=min(analytic,cr['second_moment_upper'])
            explicit=schedule(bound,error,.004,max_magnitude=support)
            raw=schedule(analytic,error,.004,max_magnitude=support)
            schedules.append(dict(case=m.name,strike=k,bound=bound,error=error,schedule=explicit,analytic_only_schedule=raw))
            measured=pr['statistics']['flat_residual_second_moment']['mean']
            ideal_q=max(1,math.ceil(math.sqrt(bound)/error))
            empirical_q=max(1,math.ceil(math.sqrt(max(measured,0.))/error))
            oldcold=next((r['cold_seconds'] for r in cold if r['case']==m.name),None)
            for f in (24,32):
                oracle=next(r for r in oracles if r['case']==m.name and r['fraction_bits']==f)
                exp=next(r for r in blocks if r['block']=='exp' and r['fraction_bits']==f)
                mul=next(r for r in blocks if r['block']=='multiply' and r['fraction_bits']==f)
                source_T=2*oracle['genX_T'];source_depth=2*oracle['genX_serial_T_depth']
                row=dict(case=m.name,strike=k,fraction_bits=f,financial_epsilon=.01,flat_dollar_error=.002,
                         input_second_moment_bound=bound,analytic_only_second_moment_bound=analytic,
                         empirical_parity_second_moment=measured,empirical_previous_second_moment=old['statistics']['flat_residual_second_moment']['mean'],
                         empirical_moment_reduction_factor=old['statistics']['flat_residual_second_moment']['mean']/measured,
                         explicit_A_and_inverse_calls=explicit['calls_A'],analytic_only_calls=raw['calls_A'],
                         explicit_statistical_error_dollars=disc*explicit['total_error_bound'],
                         ideal_unit_constant_queries=ideal_q,empirical_moment_unit_constant_queries=empirical_q,
                         preprocessing_seconds=cr['seconds_with_training'],regret_upper=cr['regret_upper'],regret_budget_pass=cr['regret_upper']<=.003,
                         source_arithmetic_T_subtotal=source_T,source_serial_T_depth_subtotal=source_depth,
                         explicit_arithmetic_T_subtotal=explicit['calls_A']*source_T,
                         one_exp_T_depth=exp['t_depth'],one_multiply_T_depth=mul['t_depth'],
                         previous_cold_classical_seconds=oldcold,
                         previous_10x_budget_seconds=None if oldcold is None else oldcold/10,
                         ideal_maximum_source_seconds=None if oldcold is None else oldcold/(10*ideal_q),
                         ideal_maximum_T_layer_seconds_one_exp=None if oldcold is None else oldcold/(10*ideal_q*exp['t_depth']),
                         scope='Flat residual only. Source/inverse schedule explicit; macro arithmetic subtotal excludes parity payoff, analytic controls/policy, selector synthesis and full-price baseline. No complete circuit or FT runtime claim.')
                rows.append(row)
                for layer_ns in (1.,10.,100.,1000.):
                    sens.append(dict(case=m.name,strike=k,fraction_bits=f,T_layer_ns=layer_ns,
                                     explicit_current_serial_macro_seconds=explicit['calls_A']*source_depth*layer_ns*1e-9,
                                     ideal_one_exp_seconds=ideal_q*exp['t_depth']*layer_ns*1e-9,
                                     empirical_ideal_one_exp_seconds=empirical_q*exp['t_depth']*layer_ns*1e-9,
                                     ideal_one_multiply_seconds=ideal_q*mul['t_depth']*layer_ns*1e-9,
                                     scope='Hypothetical sensitivity; ideal columns omit confidence/constants/additional inverse work; not lower bounds on other algorithms.'))
    (out/'schedules.json').write_text(json.dumps(schedules,indent=2)+'\n')
    (out/'costs.json').write_text(json.dumps(rows,indent=2)+'\n')
    (out/'sensitivity.json').write_text(json.dumps(sens,indent=2)+'\n')
    (out/'error_contract.json').write_text(json.dumps(dict(absolute_price_error=.01,
        allocations=dict(surrogate_mean=.003,flat_mean=.002,regret=.003,numerical=.002),
        failure_allocations=dict(surrogate=.002,moment=.001,regret=.001,quantum_mean=.004,physical=.002),
        unresolved=['Certified surrogate mean at assigned error/confidence, charged setup.',
                    'Finite input/arithmetic/synthesis error within numerical allocation.',
                    'Complete controlled parity/normal-CDF/policy circuits and uncomputation.',
                    'Layout, factories, physical failure and readout.',
                    'Modern optimal mean-estimator explicit implementation (ideal sensitivity is not implementation).'],
        amortization='Preprocessing and surrogate mean are not free. If reused, classical competitor gets identical reuse.'),indent=2)+'\n')
    print(json.dumps([r for r in rows if r['fraction_bits']==32 and r['strike']==6.],indent=2))


if __name__=='__main__':run()
