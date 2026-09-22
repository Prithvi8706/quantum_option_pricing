"""Gate-emitted compound-pricing blocks; full path is a charged macro."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import time
from .model import MODELS,choose_cap
from .reversible import gbm_step,capped_payoff
from research.antithetic_feasibility.reversible import clifford_t_resources


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    rows=[];start=time.perf_counter()
    for m in MODELS:
        cap,_=choose_cap(m)
        for f in (24,32):
            w=f+16
            for name,fn in [('gbm_step',lambda:gbm_step(w,f,m.maturity/m.dates,m.sigma,m.rho)),
                            ('capped_payoff',lambda:capped_payoff(w,f,m.strike,math.exp(-m.rate*m.maturity/2),cap))]:
                p,ins,outs=fn();r=dict(case=m.name,fraction_bits=f,block=name,**clifford_t_resources(p),
                                     gate_sha256=hashlib.sha256(p.gates.data.tobytes()).hexdigest(),input_registers=ins,output_registers=outs)
                if m.name=='C4':
                    with (out/f'{name}_f{f}.gates').open('xb') as stream:p.gates.data.tofile(stream)
                rows.append(r);print(json.dumps({k:v for k,v in r.items() if k not in ('input_registers','output_registers')}),flush=True)
                (out/'blocks.json').write_text(json.dumps(rows,indent=2)+'\n')
    (out/'complete.json').write_text(json.dumps(dict(wall_seconds=time.perf_counter()-start,source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')}),indent=2))


if __name__=='__main__':run()
