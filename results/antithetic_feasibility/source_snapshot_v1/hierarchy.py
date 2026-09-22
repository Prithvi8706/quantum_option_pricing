"""Symmetric finite Haar hierarchy and paired input-error diagnostics."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np
from scipy.special import ndtr,ndtri
from scipy.stats import qmc,t
from .classical import MODELS,path_values,seeded


def haar(leaves,dates,level,fraction_bits=None):
    """Coordinates: dates base variables followed by each level's details.

    The previous level is retained as the coarse path; it is never inferred by
    adding rounded children. Detail-sign reversal swaps the last-level children.
    """
    x=leaves[:,:dates,:].copy();offset=dates;parent=None
    for l in range(1,level+1):
        detail=leaves[:,offset:offset+x.shape[1],:];offset+=x.shape[1]
        parent=x.copy();y=np.empty((x.shape[0],2*x.shape[1],x.shape[2]))
        if fraction_bits is None:
            y[:,::2,:]=(x+detail)/math.sqrt(2)
            y[:,1::2,:]=(x-detail)/math.sqrt(2)
        else:
            s=2**fraction_bits;c=round(s/math.sqrt(2))
            y[:,::2,:]=np.floor((x+detail)*c)/s
            y[:,1::2,:]=np.floor((x-detail)*c)/s
        x=y
    return x,parent


def map_increments(model,leaves,level,fraction_bits=None):
    x,parent=haar(leaves,model.dates,level,fraction_bits)
    d=model.assets;h=model.maturity/(model.dates*2**level)
    ws=math.sqrt(model.correlation)*x[:,:,:1]+math.sqrt(1-model.correlation)*x[:,:,1:d+1]
    wv=model.leverage*ws+math.sqrt(1-model.leverage**2)*x[:,:,d+1:]
    return np.ascontiguousarray(ws*math.sqrt(h)),np.ascontiguousarray(wv*math.sqrt(h))


def pay(model,ds,dv):
    return path_values(ds,dv,np.zeros(model.assets),model.dates,model.spot,model.strike,model.rate,
                       model.maturity,model.kappa,model.theta,model.v0,model.xi,model.leverage,0,0.)[:,0]


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);rows=[];summaries=[];start=time.perf_counter()
    for mi,m in enumerate(MODELS[:2]):
        for level in (3,5):
            for rep in range(16):
                n=m.dates*2**level;dim=n*(2*m.assets+1)
                u=qmc.Sobol(dim,scramble=True,seed=seeded(2026092304,mi,level,rep)).random_base2(10)
                z=ndtri(np.clip(u,np.finfo(float).eps,1-np.finfo(float).eps)).reshape(-1,n,2*m.assets+1)
                ref=pay(m,*map_increments(m,z,level))
                for q in (8,10,12,14):
                    zz=ndtri(ndtr(-8.)+(ndtr(8.)-ndtr(-8.))*u)
                    step=16/2**q
                    zz=(-8.+(np.minimum(np.floor((zz+8.)/step),2**q-1)+.5)*step).reshape(z.shape)
                    finite=pay(m,*map_increments(m,zz,level))
                    diff=finite-ref
                    rows.append(dict(case=m.name,level=level,q=q,replicate=rep,mean_difference=float(diff.mean()),
                                     squared_difference=float(np.mean(diff*diff)),maximum_absolute=float(np.max(np.abs(diff)))))
            for q in (8,10,12,14):
                r=[x for x in rows if x['case']==m.name and x['level']==level and x['q']==q]
                x=np.array([x['mean_difference'] for x in r])
                s=dict(case=m.name,level=level,q=q,mean_difference=float(x.mean()),
                       empirical_99pct_radius=float(t.ppf(.995,15)*x.std(ddof=1)/4),
                       rms_coupled_difference=math.sqrt(np.mean([v['squared_difference'] for v in r])),
                       scope='finite input law only; float path arithmetic, no continuous-bias certificate')
                summaries.append(s);print(json.dumps(s),flush=True)
            (out/'rows.json').write_text(json.dumps(rows,indent=2)+'\n')
            (out/'summaries.json').write_text(json.dumps(summaries,indent=2)+'\n')
    (out/'complete.json').write_text(json.dumps(dict(seconds=time.perf_counter()-start,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2))


if __name__=='__main__':run()
