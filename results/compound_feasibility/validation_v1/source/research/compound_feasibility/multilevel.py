"""Executed antithetic nested MLRQMC with a frozen level allocation."""
import argparse
import json
import math
from pathlib import Path
import time
import numpy as np
from scipy.stats import t
from .model import *


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    fit=json.loads(Path('results/compound_feasibility/pilot_v1/training.json').read_text())
    plan=dict(inner_powers=[8,9,10],outer_powers=[13,10,9],replicates=32,seed_root=2026092406)
    (out/'plan.json').write_text(json.dumps(plan,indent=2)+'\n');rows=[];summary=[];start=time.perf_counter()
    with (out/'rows.jsonl').open('x') as stream:
        for mi,m in enumerate(MODELS):
            cap,tail=choose_cap(m);prices=[];times=[]
            for rep in range(32):
                tick=time.perf_counter();upper=np.zeros(3);lower=np.zeros(3);contributions=[]
                for li,(pi,po) in enumerate(zip(plan['inner_powers'],plan['outer_powers'])):
                    s,a0=outer_states(m,po,seeded(plan['seed_root'],mi,rep,li,0))
                    y,_=continuation_samples(m,s,a0,pi,seeded(plan['seed_root'],mi,rep,li,1),cap)
                    mean=y.mean(axis=1);disc=math.exp(-m.rate*m.maturity/2)
                    pred=policy_value(m,s,a0,cap,np.array(fit[m.name]['coef'])) if fit[m.name]['selected']=='regression' else moment_continuation(m,s,a0,cap)
                    level=[]
                    for ki,k in enumerate((3.,6.,9.)):
                        v=disc*np.maximum(mean-k,0.)
                        if li:
                            h=y.shape[1]//2
                            v-=.5*disc*(np.maximum(y[:,:h].mean(axis=1)-k,0.)+np.maximum(y[:,h:].mean(axis=1)-k,0.))
                        else:lower[ki]=float(np.mean(disc*(pred>k)*(mean-k)))
                        upper[ki]+=v.mean();level.append(float(v.mean()))
                    contributions.append(level)
                elapsed=time.perf_counter()-tick;times.append(elapsed);prices.append((lower,upper))
                row=dict(case=m.name,replicate=rep,lower=lower.tolist(),upper=upper.tolist(),contributions=contributions,shared_seconds=elapsed)
                rows.append(row);stream.write(json.dumps(row)+'\n');stream.flush()
            for ki,k in enumerate((3.,6.,9.)):
                lo=np.array([x[0][ki] for x in prices]);up=np.array([x[1][ki] for x in prices]);factor=t.ppf(.9975,31)/math.sqrt(32)
                left=float(lo.mean()-factor*lo.std(ddof=1));right=float(up.mean()+factor*up.std(ddof=1)+tail)
                r=dict(case=m.name,strike=k,interval_low=left,interval_high=right,total_interval_width=right-left,
                       lower=float(lo.mean()),upper=float(up.mean()),seconds_with_training=sum(times)+fit[m.name]['seconds'],
                       method='Antithetic nested MLRQMC; finite M=1024 upper target, frozen independent-policy lower target',
                       status='Empirical endpoints; common training charged, three outputs share work but full cost charged to each price.')
                summary.append(r);print(json.dumps(r),flush=True)
            (out/'summaries.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'complete.json').write_text(json.dumps(dict(seconds=time.perf_counter()-start),indent=2))


if __name__=='__main__':run()
