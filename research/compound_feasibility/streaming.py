"""Same policy/Jensen estimator with streaming inner sums, no N-by-M arrays."""
import argparse
import json
import math
from pathlib import Path
import time
import numpy as np
from numba import njit
from scipy.stats import t
from .model import *


@njit(cache=True)
def residual_means(spots,accrued,factors,geom_factors,strike,discount,cap):
    out=np.empty(len(spots))
    for i in range(len(spots)):
        geom=math.exp(np.log(spots[i]).mean());total=0.
        for j in range(len(factors)):
            average=accrued[i]
            for k in range(spots.shape[1]):average+=spots[i,k]*factors[j,k]
            h=min(cap,discount*max(average-strike,0.))
            g=min(cap,discount*max(accrued[i]+.5*geom*geom_factors[j]-strike,0.))
            total+=h-g
        out[i]=total/len(factors)
    return out


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--cases',default='C4,C8,H4,H8');ap.add_argument('--outer',type=int,default=15);ap.add_argument('--inner',type=int,default=11)
    ap.add_argument('--replicates',type=int,default=32);ap.add_argument('--root',type=int,default=2026092404);ap.add_argument('--retrain',action='store_true');a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.perf_counter();rows=[];summaries=[]
    (out/'plan.json').write_text(json.dumps(vars(a),indent=2)+'\n')
    fits=json.loads(Path('results/compound_feasibility/pilot_v1/training.json').read_text())
    from .acquire import train
    with (out/'rows.jsonl').open('x') as stream:
        for mi,m in enumerate(MODELS):
            if m.name not in a.cases.split(','):continue
            cap,tail=choose_cap(m);fit=train(m,cap,mi) if a.retrain else fits[m.name];rr=[]
            for rep in range(a.replicates):
                tick=time.perf_counter();so=seeded(a.root,mi,a.outer,rep,0);si=seeded(a.root,mi,a.outer,rep,1)
                spots,accrued=outer_states(m,a.outer,so);ff,gg=future_factors(m,a.inner,si)
                mean=conditional_geometric(m,spots,accrued,cap)+residual_means(spots,accrued,ff,gg,m.strike,math.exp(-m.rate*m.maturity/2),cap)
                pred=policy_value(m,spots,accrued,cap,np.array(fit['coef'])) if fit['selected']=='regression' else moment_continuation(m,spots,accrued,cap)
                lower=[];upper=[]
                for k in (3.,6.,9.):
                    lower.append(float(math.exp(-m.rate*m.maturity/2)*np.mean((pred>k)*(mean-k))))
                    upper.append(float(math.exp(-m.rate*m.maturity/2)*np.maximum(mean-k,0.).mean()))
                row=dict(case=m.name,replicate=rep,lower=lower,upper=upper,shared_seconds=time.perf_counter()-tick,outer_seed=so,inner_seed=si)
                rr.append(row);rows.append(row);stream.write(json.dumps(row)+'\n');stream.flush()
            for ki,k in enumerate((3.,6.,9.)):
                lo=np.array([r['lower'][ki] for r in rr]);up=np.array([r['upper'][ki] for r in rr]);fac=t.ppf(.9975,len(rr)-1)/math.sqrt(len(rr))
                left=float(lo.mean()-fac*lo.std(ddof=1));right=float(up.mean()+fac*up.std(ddof=1)+tail)
                r=dict(case=m.name,strike=k,outer_power=a.outer,inner_power=a.inner,replicates=len(rr),lower=float(lo.mean()),upper=float(up.mean()),
                       interval_low=left,interval_high=right,total_interval_width=right-left,mean_gap=float(up.mean()-lo.mean()),cap=cap,cap_tail_bound=tail,
                       seconds_with_training=sum(v['shared_seconds'] for v in rr)+fit['seconds'],training_seconds=fit['seconds'],
                       scope='Same crossed RQMC policy/Jensen estimator; full shared three-price cost charged to each strike, empirical simultaneous-endpoint interval per price; no floating certificate.')
                summaries.append(r);print(json.dumps(r),flush=True)
            (out/'summaries.json').write_text(json.dumps(summaries,indent=2)+'\n')
    (out/'complete.json').write_text(json.dumps(dict(wall_seconds=time.perf_counter()-start,rows=len(rows)),indent=2))


if __name__=='__main__':run()
