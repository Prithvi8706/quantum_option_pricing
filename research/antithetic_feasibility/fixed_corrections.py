"""Paired fixed arithmetic correction diagnostic, with Gaussian inputs."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from .classical import MODELS,draw_increments,seeded
from .hierarchy import pay
from .fixed_point import step,exp_value


def fixed_pay(m,ds,dv,level,f):
    w=f+16;s=2**f;n=ds.shape[1];h=m.maturity/n;prices=[]
    for p in range(len(ds)):
        logs=[0]*m.assets;vs=[round(m.v0*s)]*m.assets;total=0
        for j in range(n):
            for k in range(m.assets):
                logs[k],vs[k]=step(logs[k],vs[k],round(ds[p,j,k]*s),round(dv[p,j,k]*s),w,f,h,m.kappa,m.theta,m.xi,m.leverage,m.rate)
            if (j+1)%2**level==0:total+=sum(exp_value(x,w,f) for x in logs)
        prices.append(math.exp(-m.rate*m.maturity)*max(total/(s*m.assets*m.dates)-m.strike,0.))
    return np.array(prices)


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);rows=[]
    for mi,m in enumerate(MODELS[:2]):
        for L in (1,3,5):
            ds,dv,_=draw_increments(m,L,6,seeded(2026092304,mi,L,998),'mc')
            n=ds.shape[1];sw=np.arange(n)^1
            cs=ds[:,::2]+ds[:,1::2];cv=dv[:,::2]+dv[:,1::2]
            ys=.5*(pay(m,ds,dv)+pay(m,ds[:,sw],dv[:,sw]))-pay(m,cs,cv)
            for f in (24,32):
                y=.5*(fixed_pay(m,ds,dv,L,f)+fixed_pay(m,ds[:,sw],dv[:,sw],L,f))-fixed_pay(m,cs,cv,L-1,f)
                diff=y-ys
                r=dict(case=m.name,level=L,fraction_bits=f,paths=len(y),float_variance=float(ys.var(ddof=1)),fixed_variance=float(y.var(ddof=1)),
                       difference_mean=float(diff.mean()),difference_rms=float(np.sqrt(np.mean(diff**2))),difference_max=float(np.max(np.abs(diff))),
                       scope='Gaussian coupled input with independently rounded increments; does not certify finite Haar implementation or rare tails.')
                rows.append(r);print(json.dumps(r),flush=True)
                (out/'rows.json').write_text(json.dumps(rows,indent=2)+'\n')


if __name__=='__main__':run()
