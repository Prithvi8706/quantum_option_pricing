"""Cold process timing for fixed single-model three-strike acquisitions."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def run():
    out=Path('results/compound_feasibility/cold_timing_v1');out.mkdir(exist_ok=False);rows=[]
    for case in ('C4','H8'):
        cache=Path('.context')/('compound_cold_'+case+'_v1');cache.mkdir(exist_ok=False)
        env=os.environ.copy();env['NUMBA_CACHE_DIR']=str(cache.resolve())
        cmd=[sys.executable,'-m','research.compound_feasibility.streaming','--out',str(out/case),'--cases',case,'--outer','13','--inner','8','--replicates','32','--root','2026092416','--retrain']
        start=time.perf_counter()
        with (out/(case+'.txt')).open('x') as stream:p=subprocess.run(cmd,env=env,stdout=stream,stderr=subprocess.STDOUT)
        row=dict(case=case,command=cmd,returncode=p.returncode,cold_seconds=time.perf_counter()-start,
                 scope='Fresh process and native cache: imports, independent policy training/validation, acquisition and output. Full three-strike time charged to any one requested price. Development parameters, fresh sampling root.')
        rows.append(row);(out/'receipts.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(row),flush=True)
        if p.returncode:raise RuntimeError('cold subprocess failed')


if __name__=='__main__':run()
