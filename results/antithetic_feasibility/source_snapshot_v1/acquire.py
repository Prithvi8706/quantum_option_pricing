"""Append-only acquisition. Run with the isolated environment from repo root."""
import argparse
from dataclasses import asdict
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import time
import numpy as np
import scipy
import numba
import psutil
from scipy.stats import t
from .classical import MODELS, values, fit_control, control_mean, seeded


def run():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',required=True)
    ap.add_argument('--cases',default='A1,A4')
    ap.add_argument('--powers',default='8,10,12')
    ap.add_argument('--levels',default='0,2,4')
    ap.add_argument('--replicates',type=int,default=16)
    ap.add_argument('--corrections',action='store_true')
    ap.add_argument('--cap',type=float,default=0.)
    a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter()
    # Compile every exercised shape/branch before reported warm timings.
    for cond in (False,True):
        values(MODELS[0],1,2,433,conditional=cond,correction=True,cap=a.cap)
    warmup=time.perf_counter()-start
    config=dict(arguments=vars(a),status='development acquisition, empirical intervals only',
                versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,numba=numba.__version__),
                platform=platform.platform(),cpu=platform.processor(),logical_cpus=os.cpu_count(),
                physical_cpus=psutil.cpu_count(logical=False),warmup_seconds=warmup,
                source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')})
    (out/'manifest.json').write_text(json.dumps(config,indent=2)+'\n')
    summaries=[];allrows=[]
    with (out/'rows.jsonl').open('x') as f:
        for mi,m in enumerate(MODELS):
            if m.name not in a.cases.split(','):continue
            for level in map(int,a.levels.split(',')):
                for method,cond in [('mc',False),('rqmc',False),('rqmc',True)]:
                    coeff=0.;fit_seconds=0.
                    if not a.corrections or level==0:
                        coeff,fit_seconds=fit_control(m,level,10,seeded(2026092301,mi,level,int(cond)),cond,a.cap)
                    for power in map(int,a.powers.split(',')):
                        means=[];variances=[];times=[];plainmeans=[];plainvars=[]
                        for rep in range(a.replicates):
                            seed=seeded(2026092302,mi,level,power,rep,0 if method=='mc' else 1)
                            tick=time.perf_counter()
                            x=values(m,level,power,seed,method,cond,a.corrections and level>0,a.cap)
                            if a.corrections and level>0:y=x[:,0]
                            else:y=x[:,0]-coeff*(x[:,1]-control_mean(m,a.cap))
                            elapsed=time.perf_counter()-tick
                            row=dict(case=m.name,model=asdict(m),level=level,power=power,paths=len(y),replicate=rep,
                                     method=method,conditional=cond,correction=a.corrections and level>0,
                                     mean=float(y.mean()),variance=float(y.var(ddof=1)),
                                     raw_mean=float(x[:,0].mean()),raw_variance=float(x[:,0].var(ddof=1)),
                                     auxiliary_mean=float(x[:,1].mean()),auxiliary_variance=float(x[:,1].var(ddof=1)),
                                     maximum_absolute=float(np.abs(y).max()),control_coefficient=coeff,
                                     fit_seconds=fit_seconds,seconds=elapsed,seed=seed)
                            f.write(json.dumps(row)+'\n');f.flush();allrows.append(row)
                            means.append(row['mean']);variances.append(row['variance']);times.append(elapsed)
                            plainmeans.append(row['raw_mean']);plainvars.append(row['raw_variance'])
                        summary=dict(case=m.name,level=level,power=power,method=method,conditional=cond,
                                     correction=a.corrections and level>0,replicates=a.replicates,
                                     mean=float(np.mean(means)),empirical_99pct_radius=float(t.ppf(.995,a.replicates-1)*np.std(means,ddof=1)/math.sqrt(a.replicates)),
                                     sample_variance=float(np.mean(variances)),raw_variance=float(np.mean(plainvars)),
                                     mean_sample_second_moment=float(np.mean(variances)+np.mean(means)**2),
                                     seconds=sum(times)+fit_seconds,fit_seconds=fit_seconds,control_coefficient=coeff,
                                     mean_values=means,seconds_values=times)
                        summaries.append(summary);print(json.dumps({k:v for k,v in summary.items() if not isinstance(v,list)}),flush=True)
                        (out/'summaries.json').write_text(json.dumps(summaries,indent=2)+'\n')
    end=dict(total_seconds=time.perf_counter()-start,rows=len(allrows),
             peak_working_set_bytes=psutil.Process().memory_info().peak_wset,
             limits=['No SDE-bias or floating-error certificate.','Student intervals across independent scrambles are empirical.',
                     'No held-out cases.','Python/import startup excluded; kernel warmup separately charged.',
                     'Gaussian inputs differ from the explicitly finite quantum input law until its bridge is supplied.'])
    (out/'complete.json').write_text(json.dumps(end,indent=2)+'\n');print(json.dumps(end),flush=True)


if __name__=='__main__':run()
