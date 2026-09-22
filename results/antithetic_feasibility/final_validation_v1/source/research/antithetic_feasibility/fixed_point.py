"""Independent integer reference and finite-precision development diagnostics."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np
from .classical import MODELS,draw_increments,seeded


def wrap(x,w):return (int(x)+2**(w-1))%2**w-2**(w-1)


def step(log,v,ws,wv,w,f,h,kappa=2.,theta=.09,xi=.3,rho=-.5,rate=.03):
    s=2**f
    def mul(a,b):return wrap(a*b//s,w)
    def cmul(a,c):return mul(a,round(c*s))
    if v<0:raise ArithmeticError('negative fixed-point variance; no silent repair')
    rt=math.isqrt(v*s)
    price=mul(rt,ws);cross=mul(ws,wv);vol=mul(rt,wv);vv=mul(wv,wv)
    lv=wrap(log+price+cmul(v,-.5*h)+cmul(cross,xi/4)+round((rate-xi*rho/4)*h*s),w)
    numerator=wrap(v+cmul(vol,xi)+cmul(vv,xi*xi/4)+round((kappa*theta-xi*xi/4)*h*s),w)
    return lv,cmul(numerator,1/(1+kappa*h))


def exp_value(x,w,f):
    s=2**f;c=[round(s/math.factorial(j)) for j in range(13)]
    while len(c)>1 and c[-1]==0:c.pop()
    reduced=x//32;y=c[-1]
    for cc in reversed(c[:-1]):y=wrap(y*reduced//s+cc,w)
    for _ in range(5):y=wrap(y*y//s,w)
    return wrap(100*y,w)


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);rows=[];start=time.perf_counter()
    # Paired path comparison isolates arithmetic from SDE discretization/input-law bias.
    for mi,m in enumerate(MODELS[:2]):
        for level in (0,3,5):
            ds,dv,_=draw_increments(m,level,5,seeded(2026092304,mi,level,991),'mc')
            n=ds.shape[1];h=m.maturity/n
            from .hierarchy import pay
            ref=pay(m,ds,dv)
            for f in (16,24,32):
                w=f+16;s=2**f;prices=[];minv=1.e9;maxlog=-1.e9
                for p in range(len(ds)):
                    logs=[0]*m.assets;vs=[round(m.v0*s)]*m.assets;total=0
                    for j in range(n):
                        for asset in range(m.assets):
                            logs[asset],vs[asset]=step(logs[asset],vs[asset],round(ds[p,j,asset]*s),round(dv[p,j,asset]*s),w,f,h,
                                                      m.kappa,m.theta,m.xi,m.leverage,m.rate)
                            minv=min(minv,vs[asset]/s);maxlog=max(maxlog,logs[asset]/s)
                        if (j+1)%(2**level)==0:
                            total+=sum(exp_value(x,w,f) for x in logs)
                    prices.append(math.exp(-m.rate*m.maturity)*max(total/(s*m.assets*m.dates)-m.strike,0.))
                diff=np.asarray(prices)-ref
                row=dict(case=m.name,level=level,fraction_bits=f,paths=len(ref),mean_arithmetic_difference=float(diff.mean()),
                         maximum_absolute_difference=float(np.abs(diff).max()),rms_difference=float(np.sqrt(np.mean(diff*diff))),
                         minimum_variance=minv,maximum_log_relative_spot=maxlog,
                         status='development arithmetic diagnostic only; no uniform path/domain certificate')
                rows.append(row);print(json.dumps(row),flush=True)
                (out/'rows.json').write_text(json.dumps(rows,indent=2)+'\n')
    (out/'complete.json').write_text(json.dumps(dict(seconds=time.perf_counter()-start,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2))


if __name__=='__main__':run()
