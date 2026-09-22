"""Full pricing and moment diagnostics using a bounded parity residual."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np
from scipy.stats import t
from research.compound_feasibility.model import MODELS,choose_cap,outer_states,future_factors,seeded
from research.compound_feasibility.acquire import train
from .parity import bounds,prediction,moment_bound,complement_stats
from .bounds import regret_envelope


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mode',choices=['pilot','classical'],default='pilot')
    ap.add_argument('--cases',default='C4,C8,H4,H8');ap.add_argument('--outer',type=int);ap.add_argument('--inner')
    ap.add_argument('--replicates',type=int);ap.add_argument('--root',type=int);ap.add_argument('--retrain',action='store_true');a=ap.parse_args()
    a.outer=a.outer if a.outer is not None else (10 if a.mode=='pilot' else 13)
    a.inner=a.inner or ('11' if a.mode=='pilot' else '4,8')
    a.replicates=a.replicates or (16 if a.mode=='pilot' else 32)
    a.root=a.root or (2026092503 if a.mode=='pilot' else 2026092504)
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    (out/'plan.json').write_text(json.dumps(dict(args=vars(a),source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')}),indent=2)+'\n')
    fits=json.loads(Path('results/compound_feasibility/pilot_v1/training.json').read_text());all_summary=[];start=time.perf_counter()
    with (out/'rows.jsonl').open('x') as stream:
        for mi,m in enumerate(MODELS):
            if m.name not in a.cases.split(','):continue
            fit=train(m,choose_cap(m)[0],mi) if a.retrain else fits[m.name];rows=[];disc=math.exp(-m.rate*m.maturity/2)
            for rep in range(a.replicates):
                tick=time.perf_counter();so=seeded(a.root,mi,a.outer,rep,0);si=seeded(a.root,mi,a.outer,rep,1)
                s,ac=outer_states(m,a.outer,so);b=bounds(m,s,ac);pred=prediction(m,s,ac,fit,b);setup=time.perf_counter()-tick
                for power in map(int,a.inner.split(',')):
                    tick=time.perf_counter();ff,gg=future_factors(m,power,si);mean,second=complement_stats(s,ac,ff,gg,m.strike,disc)
                    c=b['c0']-mean;shift=b['c0']-pred
                    for k in (3.,6.,9.):
                        d=pred>k;lo=disc*d*(c-k);up=disc*np.maximum(c-k,0.)
                        y2=d*(second-2*shift*mean+shift**2)
                        row=dict(case=m.name,strike=k,replicate=rep,outer_power=a.outer,inner_power=power,
                                 outer_seed=so,inner_seed=si,lower=float(lo.mean()),upper=float(up.mean()),
                                 jensen_regret_upper=float(np.mean(up-lo)),flat_residual_mean=float(np.mean(disc*d*(shift-mean))),
                                 flat_residual_second_moment=float(y2.mean()),conditional_moment_bound_mean=float(moment_bound(b,pred,k).mean()),
                                 deterministic_regret_envelope_mean=float(disc*regret_envelope(b['lower'],b['upper'],pred,k).mean()),
                                 unresolved_state_fraction=float(np.mean((b['lower']<k)&(b['upper']>k))),
                                 surrogate_price_mean=float(np.mean(disc*np.maximum(pred-k,0.))),
                                 residual_absolute_bound=b['support'],shared_setup_seconds=setup,shared_evaluation_seconds=time.perf_counter()-tick)
                        assert abs(row['surrogate_price_mean']+row['flat_residual_mean']-row['lower'])<1e-10
                        rows.append(row);stream.write(json.dumps(row)+'\n');stream.flush()
                if (rep+1)%8==0:print(json.dumps(dict(case=m.name,replicates_done=rep+1,seconds=time.perf_counter()-start)),flush=True)
            for power in map(int,a.inner.split(',')):
                for k in (3.,6.,9.):
                    rr=[r for r in rows if r['strike']==k and r['inner_power']==power];stats={}
                    for key in ('lower','upper','jensen_regret_upper','flat_residual_mean','flat_residual_second_moment',
                                'conditional_moment_bound_mean','deterministic_regret_envelope_mean','unresolved_state_fraction','surrogate_price_mean'):
                        v=np.array([r[key] for r in rr]);stats[key]=dict(mean=float(v.mean()),empirical_99_radius=float(t.ppf(.995,len(v)-1)*v.std(ddof=1)/math.sqrt(len(v))))
                    fac=t.ppf(.9975,len(rr)-1)/math.sqrt(len(rr));lo=np.array([r['lower'] for r in rr]);up=np.array([r['upper'] for r in rr])
                    left=float(lo.mean()-fac*lo.std(ddof=1));right=float(up.mean()+fac*up.std(ddof=1))
                    summary=dict(case=m.name,strike=k,outer_power=a.outer,inner_power=power,replicates=len(rr),statistics=stats,
                                 interval_low=left,interval_high=right,total_interval_width=right-left,
                                 seconds_with_training=fit['seconds']+sum(r['shared_setup_seconds']+r['shared_evaluation_seconds'] for r in rr),
                                 training_seconds=fit['seconds'],residual_absolute_bound=b['support'],
                                 scope='Original uncapped financial contract; empirical RQMC intervals, exact expectation bracket; no rounding/PRNG certificate.')
                    all_summary.append(summary);print(json.dumps({k:v for k,v in summary.items() if k!='statistics'}),flush=True)
            (out/'summaries.json').write_text(json.dumps(all_summary,indent=2)+'\n')
    (out/'complete.json').write_text(json.dumps(dict(wall_seconds=time.perf_counter()-start),indent=2)+'\n')


if __name__=='__main__':run()
