"""Compile gate-emitted blocks and archive counts/source hashes, never device timing."""
import argparse
import gc
import hashlib
import json
from pathlib import Path
import time
import numpy as np
from scipy.special import ndtr
from .reversible import (step_program,sqrt_program,exp_program,primitive_program,clifford_t_resources)


def gaussian_loader(q,cutoff=8.):
    from qiskit import QuantumCircuit,transpile
    from qiskit.circuit.library import StatePreparation
    edges=np.linspace(-cutoff,cutoff,2**q+1)
    probabilities=np.diff(ndtr(edges));probabilities=.5*(probabilities+probabilities[::-1])
    probabilities/=probabilities.sum()
    c=QuantumCircuit(q);c.append(StatePreparation(np.sqrt(probabilities)),range(q))
    compiled=transpile(c,basis_gates=['u','cx'],optimization_level=1)
    # Do not pretend arbitrary rotations have already been synthesized to T.
    counts={str(k):int(v) for k,v in compiled.count_ops().items()}
    return dict(qubits=q,counts=counts,depth=compiled.depth(),
                arbitrary_rotation_upper_count=3*counts.get('u',0),
                table_entries=len(probabilities),table_bytes=probabilities.nbytes,
                distribution='symmetric Gaussian bin mass conditional on [-8,8], midpoint labels',
                probability_sha256=hashlib.sha256(probabilities.tobytes()).hexdigest(),
                synthesis_status='arbitrary U gates retained; cost remains a variable, not zero')


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    allrows=[];start=time.perf_counter()
    for f in (24,32):
        w=f+16
        builders=[('sqrt',lambda:sqrt_program(w,f)),('exp',lambda:exp_program(w,f)),
                  ('multiply',lambda:primitive_program('multiply',w,f)),
                  ('add',lambda:primitive_program('add',w,f)),
                  ('compare',lambda:primitive_program('compare',w,f)),
                  ('positive',lambda:primitive_program('positive',w,f)),
                  ('step_h_1_12',lambda:step_program(w,f,1/12)),
                  ('step_h_1_24',lambda:step_program(w,f,1/24))]
        for name,build in builders:
            tick=time.perf_counter();p,ins,outs=build();emission=time.perf_counter()-tick
            resources=clifford_t_resources(p)
            # Hash compact gate bytes; archive the actual medium-size step stream.
            gate_hash=hashlib.sha256(p.gates.data.tobytes()).hexdigest()
            if name=='step_h_1_12':
                with (out/f'{name}_f{f}.gates').open('xb') as stream:p.gates.data.tofile(stream)
            row=dict(block=name,width=w,fraction_bits=f,**resources,
                     emission_seconds=emission,resource_analysis_seconds=time.perf_counter()-tick-emission,
                     compact_gate_sha256=gate_hash,input_registers=ins,output_registers=outs)
            allrows.append(row);(out/'blocks.json').write_text(json.dumps(allrows,indent=2)+'\n')
            print(json.dumps({k:v for k,v in row.items() if k not in ('input_registers','output_registers')}),flush=True)
            del p;gc.collect()
    loaders=[]
    for q in (8,10):
        tick=time.perf_counter();x=gaussian_loader(q);x['compilation_seconds']=time.perf_counter()-tick
        loaders.append(x);print(json.dumps(x),flush=True)
    (out/'loaders.json').write_text(json.dumps(loaders,indent=2)+'\n')
    final=dict(total_seconds=time.perf_counter()-start,
               source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')},
               status='emitted logical blocks and Gaussian U/CX preparation; no full price/circuit certificate')
    (out/'complete.json').write_text(json.dumps(final,indent=2)+'\n')


if __name__=='__main__':run()
