"""Complete subprocess latency, including imports and fresh native compilation."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def run():
    root=Path('results/antithetic_feasibility');out=root/'cold_classical_v1';out.mkdir(exist_ok=False)
    cache=Path('.context/antithetic_cold_cache_v1').resolve();cache.mkdir(exist_ok=False)
    env=os.environ.copy();env['NUMBA_CACHE_DIR']=str(cache)
    cmd=[sys.executable,'-m','research.antithetic_feasibility.hybrid_classical','--out',str(out/'acquisition'),'--cases','A4','--epsilons','.01']
    start=time.perf_counter()
    with (out/'stdout.txt').open('x') as stream:completed=subprocess.run(cmd,env=env,stdout=stream,stderr=subprocess.STDOUT)
    receipt=dict(command=cmd,returncode=completed.returncode,wall_seconds=time.perf_counter()-start,
                 fresh_numba_cache=str(cache),scope='Same fixed seeds; latency replication, not new accuracy evidence. Includes process/import/native compilation/training/acquisition/output.')
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
    if completed.returncode:raise RuntimeError('classical process failed')


if __name__=='__main__':run()
