"""Train independently and acquire replicated policy/Jensen price brackets."""
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
from .model import *


def train(m,cap,index):
    start=time.perf_counter();s,a=outer_states(m,12,seeded(2026092402,index,0))
    y,_=continuation_samples(m,s,a,7,seeded(2026092402,index,1),cap)
    x,geo,mm=features(m,s,a,cap);target=y.mean(axis=1)-mm
    scale=np.sqrt(np.mean(x*x,axis=0));scale=np.maximum(scale,1e-8);z=x/scale
    reg=1e-7*np.eye(z.shape[1]);coef=np.linalg.solve(z.T@z+reg,z.T@target)/scale
    sv,av=outer_states(m,10,seeded(2026092402,index,2));yv,_=continuation_samples(m,sv,av,9,seeded(2026092402,index,3),cap)
    ref=yv.mean(axis=1);pred=policy_value(m,sv,av,cap,coef);baseline=moment_continuation(m,sv,av,cap)
    chosen='regression' if np.mean((pred-ref)**2)<np.mean((baseline-ref)**2) else 'moment'
    return dict(coef=coef.tolist(),selected=chosen,seconds=time.perf_counter()-start,
                validation_rmse_regression=float(np.sqrt(np.mean((pred-ref)**2))),validation_rmse_moment=float(np.sqrt(np.mean((baseline-ref)**2))),
                status='Independent training/validation; target noisy. Price bracket does not assume policy accuracy.')


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--cases',default='C4,C8,H4,H8')
    ap.add_argument('--outer',type=int,default=11);ap.add_argument('--inner',default='2,4,6,8');ap.add_argument('--replicates',type=int,default=16)
    ap.add_argument('--method',default='rqmc');ap.add_argument('--training');ap.add_argument('--root',type=int,default=2026092403);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.perf_counter();rows=[];summaries=[];training={}
    manifest=dict(args=vars(a),models=[asdict(m) for m in MODELS],platform=platform.platform(),python=platform.python_version(),
                  source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')})
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    powers=list(map(int,a.inner.split(',')));prior=json.loads(Path(a.training).read_text()) if a.training else {}
    with (out/'rows.jsonl').open('x') as stream:
        for mi,m in enumerate(MODELS):
            if m.name not in a.cases.split(','):continue
            cap,tail=choose_cap(m);fit=prior.get(m.name) or train(m,cap,mi);training[m.name]=fit
            (out/'training.json').write_text(json.dumps(training,indent=2)+'\n');print('TRAIN '+m.name+' '+json.dumps(fit),flush=True)
            for rep in range(a.replicates):
                tick=time.perf_counter();so=seeded(a.root,mi,a.outer,rep,0);si=seeded(a.root,mi,a.outer,rep,1)
                spots,accrued=outer_states(m,a.outer,so,a.method)
                pred=policy_value(m,spots,accrued,cap,np.array(fit['coef'])) if fit['selected']=='regression' else moment_continuation(m,spots,accrued,cap)
                setup=time.perf_counter()-tick
                for power in powers:
                    tt=time.perf_counter();y,raw=continuation_samples(m,spots,accrued,power,si,cap,a.method)
                    mean=y.mean(axis=1);discount=math.exp(-m.rate*m.maturity/2)
                    for strike in (3.,6.,9.):
                        decision=pred>strike;lower=discount*decision*(mean-strike);upper=discount*np.maximum(mean-strike,0)
                        lo_raw=discount*decision*(raw.mean(axis=1)-strike);up_raw=discount*np.maximum(raw.mean(axis=1)-strike,0)
                        half=len(y[0])//2;ua=np.maximum(y[:,:half].mean(axis=1)-strike,0);ub=np.maximum(y[:,half:].mean(axis=1)-strike,0)
                        correction=upper-.5*discount*(ua+ub)
                        row=dict(case=m.name,outer_power=a.outer,inner_power=power,replicate=rep,strike=strike,cap=cap,cap_tail_bound=tail,
                                 lower=float(lower.mean()),upper=float(upper.mean()),gap=float(np.mean(upper-lower)),
                                 raw_lower=float(lo_raw.mean()),raw_upper=float(up_raw.mean()),
                                 correction_mean=float(correction.mean()),correction_variance=float(correction.var(ddof=1)),
                                 payoff_second_moment=float(np.mean(raw*raw)),residual_sample_variance=float(np.mean(np.var(y,axis=1,ddof=1))),
                                 exercise_fraction=float(decision.mean()),outer_seed=so,inner_seed=si,
                                 shared_setup_seconds=setup,shared_three_strike_seconds=time.perf_counter()-tt)
                        rows.append(row);stream.write(json.dumps(row)+'\n');stream.flush()
            for power in powers:
                for strike in (3.,6.,9.):
                    rr=[r for r in rows if r['case']==m.name and r['inner_power']==power and r['strike']==strike]
                    lower=np.array([r['lower'] for r in rr]);upper=np.array([r['upper'] for r in rr]);rad=t.ppf(.9975,len(rr)-1)/math.sqrt(len(rr))
                    rl=float(rad*lower.std(ddof=1));ru=float(rad*upper.std(ddof=1))
                    r=dict(case=m.name,outer_power=a.outer,inner_power=power,strike=strike,cap=cap,cap_tail_bound=tail,
                           lower=float(lower.mean()),upper=float(upper.mean()),lower_radius=rl,upper_radius=ru,
                           interval_low=float(lower.mean()-rl),interval_high=float(upper.mean()+ru+tail),
                           total_interval_width=float(upper.mean()-lower.mean()+ru+rl+tail),mean_gap=float(upper.mean()-lower.mean()),
                           mean_raw_gap=float(np.mean([v['raw_upper']-v['raw_lower'] for v in rr])),
                           seconds_with_training=fit['seconds']+sum(v['shared_setup_seconds']+v['shared_three_strike_seconds'] for v in rr),
                           training_seconds=fit['seconds'],replicates=len(rr),lower_values=lower.tolist(),upper_values=upper.tolist(),
                           scope='Empirical endpoint intervals around valid expectation bounds; includes analytic cap-tail bound, not floating/PRNG certificate. Full shared preparation charged to each strike.')
                    summaries.append(r);print(json.dumps({k:v for k,v in r.items() if not k.endswith('_values')}),flush=True)
            (out/'summaries.json').write_text(json.dumps(summaries,indent=2)+'\n')
    (out/'complete.json').write_text(json.dumps(dict(wall_seconds=time.perf_counter()-start,rows=len(rows)),indent=2))


if __name__=='__main__':run()
