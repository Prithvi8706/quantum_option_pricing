"""Fixed-size bounded-control MC with a nonasymptotic statistical interval.

Targets a capped, discretized Gaussian-input model. Floating arithmetic and
continuous-model bridges are explicitly not certified by this interval.
"""
import argparse
import json
import math
from pathlib import Path
import time
import numpy as np
from .classical import MODELS,fit_control,values,control_mean,seeded


def radius(n,variance,span,delta):
    log=math.log(4/delta)
    return math.sqrt(2*variance*log/n)+7*span*log/(3*(n-1))


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    plan=dict(level=5,cap=200.,samples=2**18,batch=512,delta=.01,root_seed=2026092315,
              theorem='Maurer-Pontil 2009 Theorem 4, both tails via union bound',
              target='capped log-Milstein discrete model, Gaussian inputs; not continuous uncapped option')
    (out/'plan.json').write_text(json.dumps(plan,indent=2)+'\n');allrows=[]
    for mi,m in enumerate(MODELS[:2]):
        start=time.perf_counter();b,fit=fit_control(m,5,10,seeded(2026092301,mi,5,91),False,200.)
        mu=control_mean(m,200.);total=0.;squares=0.;mins=1e300;maxs=-1e300
        with (out/f'{m.name}_batches.jsonl').open('x') as stream:
            for j in range(plan['samples']//plan['batch']):
                x=values(m,5,9,seeded(plan['root_seed'],mi,j),'mc',False,False,200.)
                y=x[:,0]-b*(x[:,1]-mu);total+=float(y.sum());squares+=float(np.dot(y,y))
                mins=min(mins,float(y.min()));maxs=max(maxs,float(y.max()))
                stream.write(json.dumps(dict(batch=j,sum=float(y.sum()),squares=float(np.dot(y,y))))+'\n')
        n=plan['samples'];var=(squares-total*total/n)/(n-1);span=math.exp(-m.rate*m.maturity)*200*(1+abs(b))
        r=dict(case=m.name,n=n,mean=total/n,sample_variance=var,range_span=span,coefficient=b,control_mean=mu,
               radius_99pct=radius(n,var,span,.01),seconds=time.perf_counter()-start,fit_seconds=fit,
               min_observed=mins,max_observed=maxs,
               guarantee='nonasymptotic statistical bound conditional on iid Gaussian draws, exact evaluations and exact analytic control mean; no SDE/tail/float certificate')
        allrows.append(r);(out/'summaries.json').write_text(json.dumps(allrows,indent=2)+'\n');print(json.dumps(r),flush=True)


if __name__=='__main__':run()
