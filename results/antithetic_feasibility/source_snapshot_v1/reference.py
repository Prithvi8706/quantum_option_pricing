"""Independent full-truncation log-Euler discretization, diagnostic reference."""
import argparse
from dataclasses import asdict
import json
import math
from pathlib import Path
import time
import numpy as np
from numba import njit
from scipy.stats import t
from .classical import MODELS,draw_increments,conditional_call,control_mean,seeded


@njit(cache=True)
def euler(ds,dv,direction,dates,spot,strike,rate,T,kappa,theta,v0,xi):
    p,n,d=ds.shape;h=T/n;mon=n//dates;result=np.empty((p,2))
    for path in range(p):
        logs=np.full(d,math.log(spot));v=np.full(d,v0);slope=np.zeros(d)
        gbm=np.full(d,math.log(spot));gbmslope=np.zeros(d)
        aa=np.empty(d*dates);bb=np.empty(d*dates);ga=0.;gb=0.;idx=0
        for step in range(n):
            for asset in range(d):
                vp=max(v[asset],0.);rt=math.sqrt(vp)
                logs[asset]+=(rate-.5*vp)*h+rt*ds[path,step,asset]
                slope[asset]+=rt*direction[asset]
                v[asset]+=kappa*(theta-vp)*h+xi*rt*dv[path,step,asset]
                gbm[asset]+=(rate-.5*theta)*h+math.sqrt(theta)*ds[path,step,asset]
                gbmslope[asset]+=math.sqrt(theta)*direction[asset]
            if (step+1)%mon==0:
                for asset in range(d):
                    aa[idx]=logs[asset];bb[idx]=slope[asset];idx+=1
                    ga+=gbm[asset]/(d*dates);gb+=gbmslope[asset]/(d*dates)
        result[path,0]=math.exp(-rate*T)*conditional_call(aa,bb,strike)
        result[path,1]=math.exp(-rate*T)*conditional_call(np.array([ga]),np.array([gb]),strike)
    return result


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--levels',default='5,6')
    ap.add_argument('--power',type=int,default=12);ap.add_argument('--replicates',type=int,default=16);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);summaries=[];start=time.perf_counter()
    with (out/'rows.jsonl').open('x') as stream:
        for mi,m in enumerate(MODELS[:2]):
            for level in map(int,a.levels.split(',')):
                means=[];times=[]
                for rep in range(a.replicates+1):
                    tick=time.perf_counter();seed=seeded(2026092303,mi,level,rep)
                    ds,dv,di=draw_increments(m,level,10 if rep==0 else a.power,seed,'rqmc',True)
                    x=euler(ds,dv,di,m.dates,m.spot,m.strike,m.rate,m.maturity,m.kappa,m.theta,m.v0,m.xi)
                    if rep==0:
                        cov=np.cov(x.T);beta=float(cov[0,1]/cov[1,1]);fit=time.perf_counter()-tick;continue
                    y=x[:,0]-beta*(x[:,1]-control_mean(m));mean=float(y.mean());elapsed=time.perf_counter()-tick
                    means.append(mean);times.append(elapsed)
                    stream.write(json.dumps(dict(case=m.name,level=level,power=a.power,replicate=rep,mean=mean,variance=float(y.var(ddof=1)),seconds=elapsed,seed=seed,beta=beta))+'\n');stream.flush()
                r=dict(case=m.name,model=asdict(m),level=level,power=a.power,price=float(np.mean(means)),
                       empirical_99pct_radius=float(t.ppf(.995,a.replicates-1)*np.std(means,ddof=1)/math.sqrt(a.replicates)),
                       seconds=sum(times)+fit,training_and_first_jit_seconds=fit,means=means,
                       status='independent Euler scheme, same Gaussian model; empirical reference, not bias certificate')
                summaries.append(r);(out/'summaries.json').write_text(json.dumps(summaries,indent=2)+'\n');print(json.dumps(r),flush=True)
    (out/'complete.json').write_text(json.dumps(dict(seconds=time.perf_counter()-start),indent=2))


if __name__=='__main__':run()
