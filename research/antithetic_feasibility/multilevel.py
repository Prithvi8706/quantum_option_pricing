"""Fresh development acquisition with allocations frozen from saved pilot data."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np
from scipy.stats import t
from .classical import MODELS, values,fit_control,control_mean,seeded


def allocation(case,method,conditional,epsilon,reps):
    root=Path('results/antithetic_feasibility')
    base=json.loads((root/'classical_prices_v1/summaries.json').read_text())
    diff=json.loads((root/'classical_corrections_v1/summaries.json').read_text())
    laws=[]
    for level in range(6):
        rows=[r for r in (base if level==0 else diff) if r['case']==case and r['level']==level and r['method']==method and r['conditional']==conditional]
        rows=sorted(rows,key=lambda r:r['power']);r1,r2=rows[-2:]
        # Variance of one independent replicate mean. Cost includes setup.
        var1=float(np.var(r1['mean_values'],ddof=1));var2=float(np.var(r2['mean_values'],ddof=1))
        slope=.5 if method=='mc' else float(np.clip(math.log2(var1/var2)/(2*(r2['power']-r1['power'])),.5,1.25))
        n2=2**r2['power'];cost=(r2['seconds']-r2['fit_seconds'])/r2['replicates']
        laws.append(dict(level=level,anchor_power=r2['power'],replicate_variance=var2,slope=slope,
                         seconds_per_path=cost/n2,fit_seconds=r2['fit_seconds']))
    powers=[4]*6
    def variance(l,p):return laws[l]['replicate_variance']*2**(-2*laws[l]['slope']*(p-laws[l]['anchor_power']))
    target=(epsilon*.45/t.ppf(.995,reps-1))**2*reps
    while sum(variance(l,p) for l,p in enumerate(powers))>target:
        merit=[(variance(l,p)-variance(l,p+1))/(2**p*laws[l]['seconds_per_path']) if p<18 else -1 for l,p in enumerate(powers)]
        j=int(np.argmax(merit))
        if merit[j]<0:raise RuntimeError('allocation cap exceeded')
        powers[j]+=1
    return dict(powers=powers,laws=laws,predicted_empirical_99pct_radius=float(t.ppf(.995,reps-1)*math.sqrt(sum(variance(l,p) for l,p in enumerate(powers))/reps)))


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--replicates',type=int,default=32)
    ap.add_argument('--epsilons',default='.1,.03,.01');a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.perf_counter()
    plans=[]
    for mi,m in enumerate(MODELS[:2]):
        for method,cond in [('mc',False),('rqmc',False),('rqmc',True)]:
            for ei,eps in enumerate(map(float,a.epsilons.split(','))):
                plans.append(dict(case=m.name,model_index=mi,method=method,conditional=cond,epsilon=eps,epsilon_index=ei,
                                  **allocation(m.name,method,cond,eps,a.replicates)))
    (out/'frozen_plans.json').write_text(json.dumps(plans,indent=2)+'\n')
    (out/'sources.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')},indent=2))
    summaries=[]
    with (out/'rows.jsonl').open('x') as stream:
        for plan in plans:
            m=MODELS[plan['model_index']];cond=plan['conditional'];method=plan['method']
            coef,fit_seconds=fit_control(m,0,10,seeded(2026092301,plan['model_index'],0,int(cond)),cond)
            replicate_prices=[];times=[];level_means=[[] for _ in range(6)]
            for rep in range(a.replicates):
                price=0.;tick=time.perf_counter();rlevels=[]
                for level,power in enumerate(plan['powers']):
                    seed=seeded(2026092312,plan['model_index'],plan['epsilon_index'],int(cond),0 if method=='mc' else 1,level,rep)
                    ts=time.perf_counter();x=values(m,level,power,seed,method,cond,level>0)
                    y=x[:,0]-coef*(x[:,1]-control_mean(m)) if level==0 else x[:,0]
                    mean=float(y.mean());price+=mean;level_means[level].append(mean)
                    rlevels.append(dict(level=level,power=power,mean=mean,variance=float(y.var(ddof=1)),seconds=time.perf_counter()-ts,seed=seed))
                elapsed=time.perf_counter()-tick;replicate_prices.append(price);times.append(elapsed)
                stream.write(json.dumps(dict(case=m.name,method=method,conditional=cond,epsilon=plan['epsilon'],replicate=rep,price=price,seconds=elapsed,levels=rlevels))+'\n');stream.flush()
            summary=dict(**plan,replicates=a.replicates,price=float(np.mean(replicate_prices)),
                         empirical_99pct_radius=float(t.ppf(.995,a.replicates-1)*np.std(replicate_prices,ddof=1)/math.sqrt(a.replicates)),
                         seconds=sum(times)+fit_seconds,fit_seconds=fit_seconds,prices=replicate_prices,
                         level_means=[float(np.mean(x)) for x in level_means],
                         status='fresh development acquisition; six-level discrete target, no certified remaining bias')
            summaries.append(summary);(out/'summaries.json').write_text(json.dumps(summaries,indent=2)+'\n')
            print(json.dumps({k:v for k,v in summary.items() if k not in ('laws','prices')}),flush=True)
    (out/'complete.json').write_text(json.dumps(dict(seconds=time.perf_counter()-start),indent=2))


if __name__=='__main__':run()
