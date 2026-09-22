"""Classical RQMC base plus iid antithetic corrections, all paid and fresh seeds."""
import argparse
import json
import math
from pathlib import Path
import time
import numpy as np
from scipy.stats import t
from .classical import MODELS,fit_control,values,control_mean,seeded


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True)
    ap.add_argument('--cases',default='A1,A4');ap.add_argument('--epsilons',default='.1,.03,.01');a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    base_powers={.1:(9,8),.03:(12,11),.01:(15,14)}
    corrections={.1:[5,4,4,4,4],.03:[8,6,5,4,4],.01:[11,9,8,6,5]}
    plans=[dict(case=m.name,mi=mi,epsilon=eps,powers=[base_powers[eps][mi]]+corrections[eps])
           for mi,m in enumerate(MODELS[:2]) if m.name in a.cases.split(',') for eps in map(float,a.epsilons.split(','))]
    (out/'frozen_plans.json').write_text(json.dumps(plans,indent=2)+'\n')
    summaries=[];start=time.perf_counter()
    with (out/'rows.jsonl').open('x') as stream:
        for plan in plans:
            m=MODELS[plan['mi']];coef,fit=fit_control(m,0,10,seeded(2026092301,plan['mi'],0,0))
            prices=[];timings=[];leveltimes=np.zeros(6);levelmeans=np.zeros(6)
            for rep in range(32):
                price=0.;tick=time.perf_counter();rows=[]
                for level,power in enumerate(plan['powers']):
                    tt=time.perf_counter();method='rqmc' if level==0 else 'mc'
                    seed=seeded(2026092314,plan['mi'],round(plan['epsilon']*1000),level,rep)
                    x=values(m,level,power,seed,method,False,level>0)
                    y=x[:,0]-coef*(x[:,1]-control_mean(m)) if level==0 else x[:,0]
                    mean=float(y.mean());elapsed=time.perf_counter()-tt
                    price+=mean;leveltimes[level]+=elapsed;levelmeans[level]+=mean/32
                    rows.append(dict(level=level,mean=mean,seconds=elapsed,seed=seed,power=power,variance=float(y.var(ddof=1))))
                prices.append(price);timings.append(time.perf_counter()-tick)
                stream.write(json.dumps(dict(case=m.name,epsilon=plan['epsilon'],replicate=rep,price=price,levels=rows))+'\n');stream.flush()
            r=dict(**plan,price=float(np.mean(prices)),empirical_99pct_radius=float(t.ppf(.995,31)*np.std(prices,ddof=1)/math.sqrt(32)),
                   seconds=sum(timings)+fit,fit_seconds=fit,level_seconds=leveltimes.tolist(),level_means=levelmeans.tolist(),prices=prices,
                   method='RQMC geometric-control base + iid antithetic corrections',
                   status='development, same six-level discrete target; bias/numerical bounds unresolved')
            summaries.append(r);(out/'summaries.json').write_text(json.dumps(summaries,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='prices'}),flush=True)
    (out/'complete.json').write_text(json.dumps(dict(seconds=time.perf_counter()-start),indent=2))


if __name__=='__main__':run()
