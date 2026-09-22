"""Reproducible development diagnostics and full hierarchical compilation."""
import argparse
import hashlib
import json
import time
from pathlib import Path
import numpy as np
from research.compound_feasibility.model import MODELS
from research.controlled_source_completion.finance import build_finance,float_reference,prune
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.compiler import compile_graph,phase_graph
from research.controlled_source_completion.primitives import Library

ROOT=Path('results/controlled_source_completion')


def dump(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2)+'\n')


def diagnose(samples=64):
    rows=[];start=time.perf_counter()
    for f,q in ((24,16),(40,32)):
        for mi,m in enumerate(MODELS):
            tic=time.perf_counter();g=build_finance(m,f,q);data=g.as_dict()
            rng=np.random.default_rng(np.random.SeedSequence([2026092601,mi]))
            cases=[]
            for j in range(samples):
                # Same underlying 53-bit uniforms for both precision profiles.
                high=rng.integers(0,2**53,size=len(g.inputs),dtype=np.int64);raw=high>>(53-q)
                given={'uniform_%d'%i:int(x) for i,x in enumerate(raw)}
                fixed=evaluate(data,given);ref=float_reference(m,raw,q)
                cases.append(dict(index=j,uniform_sha256=hashlib.sha256(raw.tobytes()).hexdigest(),fixed=fixed,reference=ref,
                                  error={k:fixed[k]-ref[k] for k in ref}))
            errors={k:dict(max_abs=max(abs(c['error'][k]) for c in cases),mean=float(np.mean([c['error'][k] for c in cases]))) for k in cases[0]['error']}
            row=dict(model=m.name,fraction_bits=f,uniform_bits=q,samples=samples,seed_root=2026092601,
                     max_errors=errors,classification_mismatches={str(k):sum((c['fixed']['prediction']>k)!=(c['reference']['prediction']>k) for c in cases) for k in (3,6,9)},
                     seconds=time.perf_counter()-tic,graph_nodes=len(g.nodes),graph_words=g.values,
                     interpretation='Paired development diagnostics on identical finite inputs; no tail, uniform, financial-price or confidence certificate.')
            dump(ROOT/'diagnostic_v1'/('%s_f%d.json'%(m.name,f)),dict(summary=row,cases=cases,meta=g.meta));rows.append(row)
            print(json.dumps(row),flush=True)
    dump(ROOT/'diagnostic_v1'/'summary.json',dict(rows=rows,seconds=time.perf_counter()-start))


def compile_all():
    rows=[]
    for f,q in ((24,16),(40,32)):
        lib=Library(ROOT/'compile_v1'/('leaves_f%d'%f),f+32,f,{})
        for m in (MODELS[0],MODELS[3]):
            tic=time.perf_counter();print('Building %s f%d'%(m.name,f),flush=True)
            g=build_finance(m,f,q);data=prune(g.as_dict(),['Y_6'])
            manifest,lib=compile_graph(data,ROOT/'compile_v1'/('%s_f%d'%(m.name,f)),lib)
            row=dict(model=m.name,f=f,q=q,seconds=time.perf_counter()-tic,resources=manifest['resources'],opcost=manifest['forward_operation_costs'],meta=g.meta)
            rows.append(row);dump(ROOT/'compile_v1'/'summary.json',rows);print(json.dumps(row),flush=True)
        phase=phase_graph(f);manifest,lib=compile_graph(prune(phase.as_dict(),['angle']),ROOT/'compile_v1'/('phase_f%d'%f),lib)
        print('Compiled phase f%d with %d leaves'%(f,len(lib.entries)),flush=True)
        dump(lib.path/'index.json',dict(entries=lib.entries,total_file_bytes=sum((lib.path/e['gate_file']).stat().st_size for e in lib.entries.values()),
                                      coefficient_table_bits=sum(len(t)*len(t[0])*(f+32) for t in lib.tables.values())))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['diagnose','compile']);p.add_argument('--samples',type=int,default=64);a=p.parse_args()
    diagnose(a.samples) if a.stage=='diagnose' else compile_all()
