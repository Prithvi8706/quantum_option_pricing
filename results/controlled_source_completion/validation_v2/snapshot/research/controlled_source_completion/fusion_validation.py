"""Execute the combined financial/phase forward and inverse gate programs."""
import json
import time
import numpy as np
from research.controlled_source_completion.compiler import apply_graph_half
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.run import ROOT,dump


def main():
    phase_root=ROOT/'compile_v2'/'phase_f64';phase=json.loads((phase_root/'source.json').read_text());pdata=json.loads((phase_root/'target.json').read_text())
    rows=[];basis=json.loads((ROOT/'validation_v2'/'full_source_basis.json').read_text())
    for case in basis:
        name=case['model'];f=case['fraction_bits'];root=ROOT/'compile_v2'/('%s_f%d'%(name,f))
        source=json.loads((root/'source.json').read_text());data=json.loads((root/'target.json').read_text());w=source['word_width'];pw=phase['word_width']
        offset=source['resources']['logical_qubits'];state=np.zeros(offset+phase['resources']['logical_qubits'],np.uint8);cache={}
        for n in source['inputs']:
            raw=case['inputs'][n['params']['name']]
            for j in range(w):state[n['out'][0]*w+j]=(raw>>j)&1
        pin={n['params']['name']:offset+n['out'][0]*pw for n in phase['inputs']}
        state[pin['scale_exponent']+2]=1  # normalizer 16, left=0
        initial=state.copy();y_position=next(iter(source['outputs'].values()))*w
        angle_position=offset+phase['outputs']['angle']*pw;shift=64-f
        tic=time.perf_counter();apply_graph_half(source,state,cache=cache)
        for j in range(w):state[pin['Y']+shift+j]^=state[y_position+j]
        apply_graph_half(phase,state,offset,cache=cache)
        raw_angle=sum(int(state[angle_position+j])<<j for j in range(pw))
        _,values=evaluate(data,case['inputs'],True);raw_y=values[next(iter(data['outputs'].values()))]
        signed_y=raw_y-(1<<w) if raw_y>>(w-1) else raw_y
        _,pv=evaluate(pdata,dict(Y=signed_y<<shift,left=0,scale_exponent=4),True)
        assert raw_angle==pv[pdata['outputs']['angle']]
        # CP gates would multiply this basis amplitude by exp(i*angle) under control=1.
        # They do not change basis bits; check all arithmetic and its actual inverse.
        apply_graph_half(phase,state,offset,True,cache)
        for j in range(w):state[pin['Y']+shift+j]^=state[y_position+j]
        apply_graph_half(source,state,inverse=True,cache=cache)
        assert np.array_equal(state,initial)
        row=dict(model=name,fraction_bits=f,phase_fraction_bits=64,raw_angle=raw_angle,all_input_and_workspace_bits_restored=True,
            executed_basis_gates=source['resources']['source_gates']-w+phase['resources']['source_gates']-pw+2*w,
            seconds=time.perf_counter()-tic,scope='Full combined compute/uncompute arithmetic on a basis input; diagonal phase value checked, reflection/QPE validated separately.')
        rows.append(row);dump(ROOT/'validation_v3'/'fusion.json',rows);print(json.dumps(row),flush=True)


if __name__=='__main__':main()
