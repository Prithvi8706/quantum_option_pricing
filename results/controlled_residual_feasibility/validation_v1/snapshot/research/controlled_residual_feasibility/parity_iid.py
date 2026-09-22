"""Fixed-N iid upper bounds for parity residual moments and exercise regret.

Preprocessing time is part of any hybrid quantum method using these bounds.
It is not an uncharged oracle supplying a variance estimate.
"""
import argparse
import json
import math
from pathlib import Path
import time
import numpy as np
from research.compound_feasibility.model import MODELS,outer_states,future_factors,seeded
from .parity import bounds,prediction,moment_bound,complement_stats


def eb_radius(variance,n,value_range,failure):
    # Maurer-Pontil Theorem4, union over X and -X for two-sided use.
    factor=math.log(4/failure)
    return math.sqrt(2*max(variance,0.)*factor/n)+7*value_range*factor/(3*(n-1))


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--cases',default='C4,C8,H4,H8')
    ap.add_argument('--power',type=int,default=20);ap.add_argument('--inner',type=int,default=4);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);root=2026092505;bp=11;n=2**a.power
    plan=dict(args=vars(a),outer_samples=n,inner_samples=2**a.inner,batch_power=bp,root=root,
              moment_failure=.001,regret_failure=.001,flat_mean_failure=.002,
              allocation_status='Fixed before first draw. No data-dependent stopping. Per-price budgets, not simultaneous over twelve prices.',
              quantum_error_allocation=dict(surrogate_mean=.003,flat_mean=.002,regret=.003,numerical=.002),
              quantum_failure_allocation=dict(surrogate=.002,moment=.001,regret=.001,quantum_mean=.004,physical=.002),
              scope='Statistical guarantees assume exact iid sampling and real evaluation. Numerical certificate separate; quantum preprocessing cost charged.')
    (out/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    fits=json.loads(Path('results/compound_feasibility/pilot_v1/training.json').read_text());rows=[]
    for mi,m in enumerate(MODELS):
        if m.name not in a.cases.split(','):continue
        disc=math.exp(-m.rate*m.maturity/2);fit=fits[m.name]
        sums=np.zeros((4,3));squares=np.zeros((4,3));start=time.perf_counter()
        for batch in range(2**(a.power-bp)):
            s,ac=outer_states(m,bp,seeded(root,mi,batch,0),'mc');b=bounds(m,s,ac);pred=prediction(m,s,ac,fit,b)
            ff,gg=future_factors(m,bp+a.inner,seeded(root,mi,batch,1),'mc')
            mean,second=complement_stats(s,ac,ff,gg,m.strike,disc,2**a.inner)
            c=b['c0']-mean;shift=b['c0']-pred
            for ki,k in enumerate((3.,6.,9.)):
                d=pred>k
                # r(Z) is convex, hence its mean upper bounds true policy regret.
                regret=disc*(np.maximum(c-k,0.)-d*(c-k))
                ymean=disc*d*(shift-mean)
                # Also acquire unbiased E[Y^2] directly, not square of inner mean.
                ysecond=d*(second-2*shift*mean+shift**2)
                vals=(moment_bound(b,pred,k),regret,ymean,ysecond)
                for j,x in enumerate(vals):
                    if j in (0,3) and (x.min()<-1e-8 or x.max()>b['support']**2+1e-8):raise ArithmeticError('second-moment support violation')
                    if j==1 and (x.min()<-1e-8 or x.max()>disc*b['support']+1e-8):raise ArithmeticError('regret support violation')
                    sums[j,ki]+=x.sum();squares[j,ki]+=np.dot(x,x)
            if (batch+1)%64==0:
                p=dict(case=m.name,completed_outer=(batch+1)*2**bp,seconds=time.perf_counter()-start)
                (out/'progress.json').write_text(json.dumps(p)+'\n');print(json.dumps(p),flush=True)
        elapsed=time.perf_counter()-start
        for ki,k in enumerate((3.,6.,9.)):
            means=sums[:,ki]/n;v=np.maximum(0.,(squares[:,ki]-n*means**2)/(n-1))
            # Selecting min of two upper-confidence bounds: split .001 moment budget.
            ranges=(b['support']**2,disc*b['support'],2*disc*b['support'],b['support']**2)
            failures=(.0005,.001,.002,.0005)
            rad=np.array([eb_radius(v[j],n,ranges[j],failures[j]) for j in range(4)])
            upper_moment=float(min(means[0]+rad[0],means[3]+rad[3]))
            row=dict(case=m.name,strike=k,samples=n,inner_samples=2**a.inner,
                     conditional_moment_envelope_mean=float(means[0]),conditional_moment_envelope_radius=float(rad[0]),
                     direct_second_moment_mean=float(means[3]),direct_second_moment_radius=float(rad[3]),
                     second_moment_upper=upper_moment,moment_failure=.001,
                     regret_estimator_mean=float(means[1]),regret_radius=float(rad[1]),regret_upper=float(means[1]+rad[1]),regret_failure=.001,
                     discounted_flat_mean=float(means[2]),flat_mean_radius=float(rad[2]),flat_mean_failure=.002,
                     flat_plus_regret_absolute_bias_upper=float(abs(means[2])+rad[2]+means[1]+rad[1]),
                     seconds_with_training=elapsed+fit['seconds'],preprocessing_seconds=elapsed,
                     scope='Fixed-N empirical-Bernstein inequalities with proved support; per-price statistical guarantee under ideal iid/exact evaluation. Not a complete price certificate.')
            rows.append(row);print(json.dumps(row),flush=True)
        (out/'summaries.json').write_text(json.dumps(rows,indent=2)+'\n')


if __name__=='__main__':run()
