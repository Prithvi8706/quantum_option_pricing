"""Execute complete emitted financial sources on diagnostic basis inputs."""
import json
import hashlib
import time
from pathlib import Path
import numpy as np
from research.controlled_source_completion.compiler import execute
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.run import ROOT,dump


def main(revision='v1'):
    rows=[]
    for f,q in ((24,16),(40,32)):
        for mi,name in ((0,'C4'),(3,'H8')):
            root=ROOT/('compile_'+revision)/('%s_f%d'%(name,f));manifest=json.loads((root/'source.json').read_text());data=json.loads((root/'target.json').read_text())
            rng=np.random.default_rng(np.random.SeedSequence([2026092601,mi,773]))
            for attempt in range(100):
                raw=rng.integers(0,2**q,size=len(data['inputs']),dtype=np.int64)
                inputs={'uniform_%d'%i:int(z) for i,z in enumerate(raw)}
                expected,values=evaluate(data,inputs,True)
                if abs(expected['Y_6'])>1e-5:break
            else:raise AssertionError('No active diagnostic case found')
            initial=0xa5;wanted=values[data['outputs']['Y_6']]^initial
            tic=time.perf_counter();actual=execute(manifest,inputs,dict(Y_6=initial));seconds=time.perf_counter()-tic
            assert actual['values']['Y_6']==wanted,(name,f,actual,wanted)
            assert actual['workspace_clean'] and actual['inputs_preserved'],(name,f,actual)
            row=dict(model=name,fraction_bits=f,random_bits=q,attempt=attempt,inputs=inputs,
                expected_Y=expected['Y_6'],expected_raw_xor=wanted,actual=actual,seconds=seconds,
                executed_basis_gates=manifest['resources']['source_gates'],
                target_sha256=hashlib.sha256((root/'target.json').read_bytes()).hexdigest(),
                interpretation='Every emitted gate executed on this basis input, including hierarchy binding and inverse cleanup; not a statevector, noise, or hardware simulation.')
            rows.append(row);dump(ROOT/('validation_'+revision)/'full_source_basis.json',rows)
            print(json.dumps({k:v for k,v in row.items() if k!='inputs'}),flush=True)


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--revision',default='v1');a=p.parse_args();main(a.revision)
