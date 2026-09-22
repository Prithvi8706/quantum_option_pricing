"""Shorter-hierarchy and ideal-oracle screens; not universal lower bounds."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from .estimator import schedule


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    root=Path('results/antithetic_feasibility')
    costs=json.loads((root/'complete_cost_screen_v1/costs.json').read_text())
    oracles=json.loads((root/'complete_cost_screen_v1/oracle_plans.json').read_text())
    classical=json.loads((root/'hybrid_classical_v1/summaries.json').read_text())
    rows=[]
    for c in costs:
        if c['fraction_bits']!=32:continue
        plans=sorted([p for p in oracles if p['case']==c['case'] and p['fraction_bits']==32],key=lambda p:p['level'])
        comparator=next(r for r in classical if r['case']==c['case'] and r['epsilon']==c['epsilon'])
        for L in (0,1,2,3,5):
            pp=plans[:L+1];ss=np.array(c['assumed_sigma_bounds'][:L+1])
            weights=np.sqrt([p['f_t_depth_serial']*s for p,s in zip(pp,ss)])
            allocation=.45*c['epsilon']*weights/weights.sum()
            schedules=[schedule(s*s,float(e),.004/(L+1),max_magnitude=1024.,center=c['schedules'][i]['center']) for i,(s,e) in enumerate(zip(ss,allocation))]
            td=sum(s['calls_A']*p['f_t_depth_serial']+s['grover_iterates']*p['reflection_t_depth_serial'] for p,s in zip(pp,schedules))
            tc=sum(s['calls_A']*p['f_t_count']+s['grover_iterates']*p['reflection_t_count'] for p,s in zip(pp,schedules))
            # Unit query constant, observed (not doubled) sigma, only one
            # path's sqrt dependency; other assets/operations are free.
            ideal=float(sum(math.sqrt(p['sqrt_only_serial_depth_one_path']*s/2) for p,s in zip(pp,ss))**2/(.45*c['epsilon']))
            budget=comparator['seconds']/10
            rows.append(dict(case=c['case'],epsilon=c['epsilon'],maximum_level=L,
                             serial_t_depth=td,t_count_excluding_rotations=tc,
                             explicit_seconds_at_100ns=td*1e-7,ideal_sqrt_only_seconds_at_100ns=ideal*1e-7,
                             required_ideal_layer_seconds_for_10x=budget/ideal,
                             classical_l5_seconds=comparator['seconds'],quantum_10x_budget_seconds=budget,
                             interpretation='L<5 grants unproved bias eligibility; classical L5 time favors quantum. Ideal coordinate is neither a constructed algorithm nor a lower bound.'))
    (out/'rows.json').write_text(json.dumps(rows,indent=2)+'\n')
    for r in rows:
        if r['epsilon']==.01:print(json.dumps(r),flush=True)


if __name__=='__main__':run()
