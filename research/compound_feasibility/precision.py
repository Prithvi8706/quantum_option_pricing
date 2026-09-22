"""Paired finite-normal and independent integer GBM path diagnostics."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.special import ndtr,ndtri
from .model import MODELS,choose_cap,seeded
from research.antithetic_feasibility.fixed_point import exp_value,wrap


def floating(m,z,cap):
    dt=m.maturity/m.dates;dw=(math.sqrt(m.rho)*z[:,:,:1]+math.sqrt(1-m.rho)*z[:,:,1:])*math.sqrt(dt)
    logs=np.cumsum((m.rate-.5*m.sigma**2)*dt+m.sigma*dw,axis=1)
    return np.minimum(cap,math.exp(-m.rate*m.maturity/2)*np.maximum(100*np.exp(logs).mean(axis=(1,2))-m.strike,0))


def integer_pay(m,z,cap,f):
    w=f+16;s=2**f;dt=m.maturity/m.dates;ca=round(s*m.sigma*math.sqrt(m.rho*dt));cb=round(s*m.sigma*math.sqrt((1-m.rho)*dt));dr=round(s*(m.rate-.5*m.sigma**2)*dt)
    av=round(s/(m.assets*m.dates));discount=round(s*math.exp(-m.rate*m.maturity/2));prices=[];maxlog=-1e9
    for path in z:
        logs=[0]*m.assets;total=0
        for j in range(m.dates):
            common=round(path[j,0]*s)
            for k in range(m.assets):
                logs[k]=wrap(logs[k]+common*ca//s+round(path[j,k+1]*s)*cb//s+dr,w)
                maxlog=max(maxlog,logs[k]/s);spot=exp_value(logs[k],w,f)
                if spot<0:raise ArithmeticError('observed spot overflow')
                total+=spot*av//s
        price=min(round(cap*s),max(total-round(m.strike*s),0)*discount//s)
        prices.append(price/s)
    return np.array(prices),maxlog


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=False);rows=[]
    for mi,m in enumerate(MODELS):
        cap,_=choose_cap(m);rng=np.random.default_rng(seeded(2026092401,mi,993));z=rng.standard_normal((512,m.dates,m.assets+1));ref=floating(m,z,cap)
        for q in (10,14):
            step=16/2**q;finite=-8+(np.floor((np.clip(z,-8,8-step)+8)/step)+.5)*step
            yf=floating(m,finite,cap)
            diff=yf-ref;rows.append(dict(case=m.name,kind='finite_input',q=q,paths=len(z),mean=float(diff.mean()),paired_standard_error=float(diff.std(ddof=1)/math.sqrt(len(z))),max_abs=float(np.max(np.abs(diff)))))
        for f in (24,32):
            y,maxlog=integer_pay(m,z,cap,f);diff=y-ref
            rows.append(dict(case=m.name,kind='fixed_arithmetic',fraction_bits=f,paths=len(z),mean=float(diff.mean()),paired_standard_error=float(diff.std(ddof=1)/math.sqrt(len(z))),max_abs=float(np.max(np.abs(diff))),max_log=maxlog))
        (out/'rows.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows[-4:]),flush=True)
    (out/'scope.txt').write_text('Diagnostic inner-payoff samples only; not the full nested quantum distribution, a uniform bound, or a floating-error certificate.\n')


if __name__=='__main__':run()
