"""Fixed-N iid compound-price brackets with empirical-Bernstein endpoints.

Statistical theorem assumes exact iid draws/evaluation; floating error remains
separate. Each outer state gets independent inner paths, unlike crossed RQMC.
"""
import argparse
import json
import math
from pathlib import Path
import time
import numpy as np
from numba import njit
from .model import *


@njit(cache=True)
def iid_means(spots,accrued,factors,geom_factors,inner,strike,discount,cap):
    out=np.empty(len(spots))
    for i in range(len(spots)):
        geom=math.exp(np.log(spots[i]).mean());total=0.
        for jj in range(inner):
            j=i*inner+jj;average=accrued[i]
            for k in range(spots.shape[1]):average+=spots[i,k]*factors[j,k]
            h=min(cap,discount*max(average-strike,0.));g=min(cap,discount*max(accrued[i]+.5*geom*geom_factors[j]-strike,0.))
            total+=h-g
        out[i]=total/inner
    return out


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--power',type=int,default=22);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);m=MODELS[0];cap,tail=choose_cap(m);batchpow=12;innerpow=4;N=2**a.power
    fit=json.loads(Path('results/compound_feasibility/pilot_v1/training.json').read_text())[m.name]
    plan=dict(case=m.name,outer_samples=N,inner_samples=2**innerpow,batch_power=batchpow,root=2026092412,cap=cap,cap_tail_bound=tail,endpoint_failure=.005,
              statement='Fixed before acquisition; union of two two-sided EB endpoints gives >=99% per-price statistical coverage under ideal iid/exact arithmetic.')
    (out/'plan.json').write_text(json.dumps(plan,indent=2)+'\n');sums=np.zeros((2,3));squares=np.zeros((2,3));start=time.perf_counter()
    for batch in range(2**(a.power-batchpow)):
        s,ac=outer_states(m,batchpow,seeded(plan['root'],batch,0),'mc');ff,gg=future_factors(m,batchpow+innerpow,seeded(plan['root'],batch,1),'mc')
        mean=conditional_geometric(m,s,ac,cap)+iid_means(s,ac,ff,gg,2**innerpow,m.strike,math.exp(-m.rate*m.maturity/2),cap)
        pred=policy_value(m,s,ac,cap,np.array(fit['coef'])) if fit['selected']=='regression' else moment_continuation(m,s,ac,cap)
        for ki,k in enumerate((3.,6.,9.)):
            lower=math.exp(-m.rate*m.maturity/2)*(pred>k)*(mean-k);upper=math.exp(-m.rate*m.maturity/2)*np.maximum(mean-k,0)
            for j,x in enumerate((lower,upper)):sums[j,ki]+=x.sum();squares[j,ki]+=np.dot(x,x)
        if (batch+1)%128==0:
            progress=dict(completed_outer=(batch+1)*2**batchpow,seconds=time.perf_counter()-start)
            (out/'progress.json').write_text(json.dumps(progress));print(json.dumps(progress),flush=True)
    elapsed=time.perf_counter()-start;rows=[];factor=math.log(4/.005)
    for ki,k in enumerate((3.,6.,9.)):
        means=sums[:,ki]/N;variance=(squares[:,ki]-N*means**2)/(N-1)
        # Include outer discount; use the valid larger range 2cap for both endpoints.
        R=2*cap*math.exp(-m.rate*m.maturity/2)
        radius=np.sqrt(2*variance*factor/N)+7*R*factor/(3*(N-1))
        low=float(means[0]-radius[0]);high=float(means[1]+radius[1]+tail)
        row=dict(case=m.name,strike=k,lower=float(means[0]),upper=float(means[1]),variances=variance.tolist(),radii=radius.tolist(),
                 interval_low=low,interval_high=high,total_interval_width=high-low,seconds_with_training=elapsed+fit['seconds'],
                 scope='Rigorous statistical inequality with analytic cap bias under ideal iid/exact floating-free evaluation. PRNG/floating error not certified. Full three-price cost charged to each.')
        rows.append(row);print(json.dumps(row),flush=True)
    (out/'summaries.json').write_text(json.dumps(rows,indent=2)+'\n')


if __name__=='__main__':run()
