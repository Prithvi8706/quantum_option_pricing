"""Sequential fresh-process timings after all numerical acquisitions finish."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def run():
    out=Path('results/controlled_residual_feasibility/cold_v1');out.mkdir(parents=True,exist_ok=False);rows=[]
    # Chosen from development, before these fresh timing samples. Still NOT
    # independent held-out confirmation of advantage or statistical coverage.
    for case,inner in (('C4',4),('H8',8)):
        cache=Path('.context')/('parity_cold_'+case+'_v1');cache.mkdir(exist_ok=False)
        env=os.environ.copy();env['NUMBA_CACHE_DIR']=str(cache.resolve())
        cmd=[sys.executable,'-m','research.controlled_residual_feasibility.parity_acquire',
             '--out',str(out/case),'--mode','classical','--cases',case,'--outer','13','--inner',str(inner),
             '--replicates','32','--root','2026092506','--retrain']
        start=time.perf_counter()
        with (out/(case+'.txt')).open('x') as f:p=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT)
        row=dict(case=case,inner_power=inner,command=cmd,returncode=p.returncode,cold_seconds=time.perf_counter()-start,
                 scope='Whole three-strike price calculation, charged per requested strike. Imports, new native cache, independent training/validation, bounds, controls, preparation, evaluation and output included.')
        rows.append(row);(out/'receipts.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(row),flush=True)
        if p.returncode:raise RuntimeError('cold timing subprocess failed')


if __name__=='__main__':run()
