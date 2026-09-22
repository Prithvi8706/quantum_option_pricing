"""Fresh diagnostics and classical comparisons for the flattened residual."""
import argparse
from dataclasses import asdict
import hashlib
import json
import math
from pathlib import Path
import platform
import time
import numpy as np
from scipy.stats import t
from research.compound_feasibility.model import (MODELS,choose_cap,outer_states,future_factors,
    inner_samples,moment_continuation,policy_value,seeded)
from research.compound_feasibility.streaming import residual_means
from research.compound_feasibility.acquire import train
from .bounds import conditional_bounds,global_moment,regret_envelope,flat_moment_envelope


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True)
    ap.add_argument('--mode',choices=['pilot','classical'],default='pilot')
    ap.add_argument('--cases',default='C4,C8,H4,H8');ap.add_argument('--outer',type=int)
    ap.add_argument('--inner');ap.add_argument('--replicates',type=int);ap.add_argument('--root',type=int)
    ap.add_argument('--retrain',action='store_true');a=ap.parse_args()
    if a.outer is None:a.outer=10 if a.mode=='pilot' else 13
    if a.inner is None:a.inner='11' if a.mode=='pilot' else '4,8'
    if a.replicates is None:a.replicates=16 if a.mode=='pilot' else 32
    if a.root is None:a.root=2026092501 if a.mode=='pilot' else 2026092502
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    plan=dict(args=vars(a),models=[asdict(m) for m in MODELS],python=platform.python_version(),platform=platform.platform(),
              source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')})
    (out/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    fits=json.loads(Path('results/compound_feasibility/pilot_v1/training.json').read_text())
    allrows=[];summary=[];start=time.perf_counter();powers=list(map(int,a.inner.split(',')))
    with (out/'rows.jsonl').open('x') as f:
        for mi,m in enumerate(MODELS):
            if m.name not in a.cases.split(','):continue
            cap,tail=choose_cap(m);fit=train(m,cap,mi) if a.retrain else fits[m.name]
            rows=[];global_b=global_moment(m)
            for rep in range(a.replicates):
                tic=time.perf_counter();so=seeded(a.root,mi,a.outer,rep,0);si=seeded(a.root,mi,a.outer,rep,1)
                spots,accrued=outer_states(m,a.outer,so)
                b=conditional_bounds(m,spots,accrued,cap)
                pred=policy_value(m,spots,accrued,cap,np.array(fit['coef'])) if fit['selected']=='regression' else moment_continuation(m,spots,accrued,cap)
                pred=np.clip(pred,b['lower'],b['upper']);disc=math.exp(-m.rate*m.maturity/2)
                setup=time.perf_counter()-tic
                for power in powers:
                    tick=time.perf_counter();ff,gg=future_factors(m,power,si)
                    if a.mode=='pilot':
                        samples,raw=inner_samples(spots,accrued,ff,gg,m.strike,disc,cap)
                        avg=samples.mean(axis=1);sample_second=(samples*samples).mean(axis=1)
                        raw_second=float(np.mean(raw*raw));residual_second=float(sample_second.mean())
                        variance=float(np.var(samples,axis=1,ddof=1).mean())
                    else:
                        avg=residual_means(spots,accrued,ff,gg,m.strike,disc,cap)
                        raw_second=residual_second=variance=None
                    c_est=b['geo']+avg
                    for strike in (3.,6.,9.):
                        d=pred>strike
                        low=disc*d*(c_est-strike);up=disc*np.maximum(c_est-strike,0.)
                        regret=up-low
                        u=disc*regret_envelope(b['lower'],b['upper'],pred,strike)
                        flat=d*(c_est-pred)
                        flat_m2=None if a.mode!='pilot' else float(np.mean(d*(sample_second+2*(b['geo']-pred)*avg+(b['geo']-pred)**2)))
                        row=dict(case=m.name,strike=strike,replicate=rep,outer_power=a.outer,inner_power=power,
                                 outer_seed=so,inner_seed=si,cap=cap,cap_tail_bound=tail,
                                 lower=float(low.mean()),upper=float(up.mean()),jensen_regret_upper=float(regret.mean()),
                                 deterministic_regret_envelope_mean=float(u.mean()),deterministic_regret_envelope_second_moment=float(np.mean(u*u)),
                                 unresolved_state_fraction=float(np.mean((b['lower']<strike)&(b['upper']>strike))),
                                 surrogate_price_mean=float(np.mean(disc*np.maximum(pred-strike,0.))),
                                 flat_residual_mean=float(disc*flat.mean()),flat_residual_second_moment=flat_m2,
                                 flat_conditional_moment_bound_mean=float(flat_moment_envelope(b,pred,strike).mean()),
                                 residual_sample_second_moment=residual_second,residual_sample_conditional_variance=variance,
                                 raw_sample_second_moment=raw_second,conditional_residual_bound_mean=float(b['second_moment'].mean()),
                                 conditional_residual_bound_quantiles=np.quantile(b['second_moment'],[.5,.9,.99,1]).tolist(),
                                 shared_setup_seconds=setup,shared_evaluation_seconds=time.perf_counter()-tick)
                        assert abs(row['surrogate_price_mean']+row['flat_residual_mean']-row['lower'])<1e-10
                        rows.append(row);allrows.append(row);f.write(json.dumps(row)+'\n');f.flush()
                    if a.mode=='pilot' and rep==0:
                        np.savez_compressed(out/(m.name+'_first_states.npz'),spots=spots,accrued=accrued,pred=pred,
                            lower=b['lower'],upper=b['upper'],geo=b['geo'],conditional_m2=b['second_moment'],
                            sampled_conditional_mean=c_est,sampled_conditional_second=sample_second)
                if (rep+1)%8==0:print(json.dumps(dict(case=m.name,replicates_done=rep+1,seconds=time.perf_counter()-start)),flush=True)
            for power in powers:
                for strike in (3.,6.,9.):
                    rr=[r for r in rows if r['inner_power']==power and r['strike']==strike]
                    means={}
                    for key in ('lower','upper','jensen_regret_upper','deterministic_regret_envelope_mean','unresolved_state_fraction',
                                'surrogate_price_mean','flat_residual_mean','flat_residual_second_moment','flat_conditional_moment_bound_mean',
                                'residual_sample_second_moment','residual_sample_conditional_variance','raw_sample_second_moment','conditional_residual_bound_mean'):
                        if rr[0][key] is not None:
                            values=np.array([r[key] for r in rr]);means[key]=dict(mean=float(values.mean()),
                                empirical_99_radius=float(t.ppf(.995,len(values)-1)*values.std(ddof=1)/math.sqrt(len(values))))
                    fac=t.ppf(.9975,len(rr)-1)/math.sqrt(len(rr))
                    lo=np.array([r['lower'] for r in rr]);up=np.array([r['upper'] for r in rr])
                    left=float(lo.mean()-fac*lo.std(ddof=1));right=float(up.mean()+fac*up.std(ddof=1)+tail)
                    sm=dict(case=m.name,strike=strike,inner_power=power,outer_power=a.outer,replicates=len(rr),
                            cap=cap,cap_tail_bound=tail,global_analytic_bounds=global_b,statistics=means,
                            interval_low=left,interval_high=right,total_interval_width=right-left,
                            seconds_with_training=fit['seconds']+sum(r['shared_setup_seconds']+r['shared_evaluation_seconds'] for r in rr),
                            training_seconds=fit['seconds'],
                            scope='Empirical RQMC intervals; analytic moment formulas are separate population bounds. Whole three-strike cost charged per strike; no floating certificate.')
                    summary.append(sm)
                    print(json.dumps({k:v for k,v in sm.items() if k!='statistics'}),flush=True)
            (out/'summaries.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'complete.json').write_text(json.dumps(dict(wall_seconds=time.perf_counter()-start,rows=len(allrows)),indent=2)+'\n')


if __name__=='__main__':run()
