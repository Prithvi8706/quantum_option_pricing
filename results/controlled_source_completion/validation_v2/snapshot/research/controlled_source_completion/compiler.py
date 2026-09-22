"""Hierarchical gate-level source: explicit leaves, binding, copy and reverse.

SSA temporaries are retained; leaf scratch and argument-copy slots are reused.
This is deliberately a simple correct schedule, not a space-optimized compiler.
"""
import json
import math
from collections import Counter
from pathlib import Path
from research.controlled_source_completion.primitives import Library
import numpy as np
from numba import njit


FIELDS=('source_gates','x','cx','ccx','t_count','t_depth','clifford_t_depth','clifford_cx','clifford_h')


def compile_graph(data,path,library=None):
    path=Path(path);path.mkdir(parents=True,exist_ok=True);w=data['width'];f=data['fraction_bits']
    library=library or Library(path/'leaves',w,f,data['tables'])
    library.tables.update(data['tables']);calls=[];sums=Counter();opcost={};maxscratch=0;copies=0
    for index,node in enumerate(data['nodes']):
        if node['op']=='input':continue
        key,entry=library.get(node);r=entry['resources'];arity=len(node['args']);nout=len(node['out'])
        # The local input slots prevent aliasing when one SSA word is used twice.
        # Output slots bind directly to fresh SSA words; remaining slots are scratch.
        scratch=r['qubits']-nout*w;maxscratch=max(maxscratch,scratch)
        copies+=2*arity*w
        for field in FIELDS:sums[field]+=r[field]
        bucket=opcost.setdefault(node['op'],Counter(calls=0,t_count=0,t_depth=0));bucket['calls']+=1
        bucket['t_count']+=r['t_count'];bucket['t_depth']+=r['t_depth']
        calls.append(dict(leaf=key,args=node['args'],out=node['out'],argument_copy_cx=2*arity*w))
    words=sum(len(n['out']) for n in data['nodes']);outwords=len(data['outputs'])
    random_bits=sum(n['params']['bits'] for n in data['nodes'] if n['op']=='input' and n['params'].get('preparation','uniform')=='uniform')
    clean={field:2*sums[field] for field in FIELDS}
    clean['source_gates']+=2*copies+outwords*w;clean['cx']+=2*copies+outwords*w
    clean['clifford_cx']+=2*copies+outwords*w
    # Leaves are executed in order. Independent copies in each batch run in parallel.
    clean['clifford_t_depth']+=4*len(calls)+1
    clean.update(logical_qubits=words*w+outwords*w+maxscratch,random_hadamards=random_bits,
        ssa_words=words,max_reused_scratch_qubits=maxscratch,output_words=outwords,
        t_depth_schedule='serial clean leaves, ASAP inside each leaf; valid upper bound, not optimal circuit depth',
        ccx_expansion='exact 7 T and 6 CX, 2 H per CCX; no relative-phase substitution')
    manifest=dict(format='hierarchical-clean-xor-source-v1',word_width=w,fraction_bits=f,
        values=words,inputs=[n for n in data['nodes'] if n['op']=='input'],outputs=data['outputs'],
        forward_calls=calls,clean_schedule=['forward_calls','CX each named SSA output to its separate output register','reverse forward_calls with each leaf inverted'],
        invocation_semantics='Copy every argument to a distinct clean local slot; bind output slots to fresh SSA output registers; execute leaf; uncopy arguments. Shared non-output local slots start/end zero.',
        inverse_semantics='Reverse the clean schedule and invert every leaf; all basis gates are self-inverse.',
        library=str(library.path.resolve()),library_workspace_relative=str(library.path),library_keys=sorted({x['leaf'] for x in calls}),
        resources=clean,forward_operation_costs={k:dict(v) for k,v in opcost.items()},
        exact_clifford_t=True,arbitrary_rotations=0,meaning='Arithmetic Y source only; input Hadamards counted separately, phase-estimator envelope separate.')
    (path/'source.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (path/'target.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
    return manifest,library


def reflection_cost(random_bits):
    """Controlled (2|+><+|-I) on the random register, including relative sign.

    H, X on random bits; controlled multi-Z; X, H; Z on the phase control.
    The last Z supplies the minus sign that cannot be discarded under control.
    """
    if random_bits<2:raise ValueError('use at least two random bits')
    # MCZ on random_bits+1 wires, with clean AND ladder and its reverse.
    ccx=2*(random_bits-1)
    return dict(ccx=ccx,t_count=7*ccx,t_depth=6*ccx,
        clifford_cx=6*ccx+1,clifford_h=2*ccx+2*random_bits+2,x=2*random_bits,z=1,
        scratch=random_bits-1,
        t_depth_note='6 per Toffoli is a conservative serial bound, not a lower bound',
        convention='Controlled REFL=2|+><+|-I, including Z on the external control.')


def phase_graph(f):
    from research.controlled_source_completion.ir import Graph
    g=Graph(f);y=g.input('Y',g.w,'provided');left=g.input('left',g.w,'classical');exponent=g.input('scale_exponent',g.w,'classical')
    # norm is a positive power of two. Exponent is supplied as an unscaled integer.
    z=g.shift(g.sub(y,left),g.neg(exponent));g.outputs={'angle':g.cmul(g.atan(z),-2)}
    return g


def envelope(source,phase,stage,fused=False):
    """Concrete U = reflection * complex phase, with compute-phase-uncompute."""
    s=source['resources'];p=phase['resources'];reflection=reflection_cost(s['random_hadamards'])
    # Y and angle are evaluated without control, conditional phases are controlled,
    # then both evaluations are inverted. Control=0 is exactly the identity.
    factor=1 if fused else 2
    result={k:factor*s[k]+factor*p[k]+reflection.get(k,0) for k in ('t_count','t_depth','ccx','clifford_cx','clifford_h','x')}
    if fused:result['clifford_cx']-=source['word_width']+phase['word_width']
    # -2 atan(z) is in (-pi,pi); signed fixed-point phase has f+3 active bits.
    result['clifford_cx']+=2*source['word_width']
    result.update(controlled_bit_phases=phase['fraction_bits']+3,
        logical_qubits=s['logical_qubits']+p['logical_qubits']+reflection['scratch']+stage['qpe_bits']+1,
        initial_random_hadamards=s['random_hadamards'],qpe_bits=stage['qpe_bits'],
        fused_compute_phase_uncompute=fused,
        excluded='Arbitrary controlled-phase synthesis and inverse-QFT rotations, accounted separately.',
        control_method=('Financial graph forward; promote its SSA output; phase graph forward; controlled bit phases; phase graph inverse, uncopy Y, financial graph inverse; signed controlled reflection.' if fused else 'Uncontrolled clean Y; copy its word into phase input at the scale-adjusted bit offset; clean angle; controlled bit phases; inverse angle, uncopy Y, inverse Y; signed controlled reflection.'))
    return result


def apply_graph_half(manifest,state,base=0,inverse=False,cache=None):
    """Execute only F or F inverse; permit retained SSA values during phase kickback."""
    cache={} if cache is None else cache;w=manifest['word_width']
    scratch_base=base+(manifest['values']+len(manifest['outputs']))*w
    path=Path(manifest.get('library_workspace_relative',manifest['library']))
    if not path.exists():path=Path(manifest['library'])
    sequence=reversed(manifest['forward_calls']) if inverse else manifest['forward_calls']
    for call in sequence:
        key=(str(path),call['leaf'])
        if key not in cache:
            entry=json.loads((path/(call['leaf']+'.json')).read_text())
            cache[key]=(entry,np.load(path/entry['gate_file'],mmap_mode='r'))
        entry,gates=cache[key];arity=len(call['args']);nout=len(call['out']);mapping=np.empty(entry['resources']['qubits'],np.int64)
        for i in range(len(mapping)):
            if arity*w<=i<(arity+nout)*w:mapping[i]=base+call['out'][(i-arity*w)//w]*w+i%w
            else:mapping[i]=scratch_base+i-(nout*w if i>=(arity+nout)*w else 0)
        for a,value in enumerate(call['args']):state[scratch_base+a*w:scratch_base+(a+1)*w]^=state[base+value*w:base+(value+1)*w]
        mapped_gates(gates,state,mapping,inverse)
        for a,value in enumerate(call['args']):state[scratch_base+a*w:scratch_base+(a+1)*w]^=state[base+value*w:base+(value+1)*w]


@njit(cache=True)
def mapped_gates(gates,state,mapping,inverse):
    for ii in range(len(gates)):
        j=len(gates)-1-ii if inverse else ii
        kind,aa,bb,cc=gates[j];a=mapping[aa]
        if kind==1:state[a]^=1
        elif kind==2:state[mapping[bb]]^=state[a]
        else:state[mapping[cc]]^=state[a]&state[mapping[bb]]


def execute(manifest,inputs,initial_outputs=None):
    """Run the *emitted gates*, including binding, output copy and inverse cleanup."""
    w=manifest['word_width'];words=manifest['values'];outnames=list(manifest['outputs'])
    output_base=words*w;scratch_base=output_base+len(outnames)*w
    state=np.zeros(manifest['resources']['logical_qubits'],np.uint8);cache={}
    input_positions=set()
    for node in manifest['inputs']:
        value=int(inputs[node['params']['name']]);offset=node['out'][0]*w
        for j in range(w):state[offset+j]=(value>>j)&1;input_positions.add(offset+j)
    for i,name in enumerate(outnames):
        value=(initial_outputs or {}).get(name,0)
        for j in range(w):state[output_base+i*w+j]=(value>>j)&1
    before=state.copy()
    def invoke(call,inverse):
        key=call['leaf']
        if key not in cache:
            path=Path(manifest.get('library_workspace_relative',manifest['library']))
            if not path.exists():path=Path(manifest['library'])
            entry=json.loads((path/(key+'.json')).read_text())
            cache[key]=(entry,np.load(path/entry['gate_file'],mmap_mode='r'))
        entry,gates=cache[key];arity=len(call['args']);nout=len(call['out'])
        mapping=np.empty(entry['resources']['qubits'],np.int64)
        for i in range(len(mapping)):
            if arity*w<=i<(arity+nout)*w:mapping[i]=call['out'][(i-arity*w)//w]*w+i%w
            else:mapping[i]=scratch_base+i-(nout*w if i>=(arity+nout)*w else 0)
        for a,value in enumerate(call['args']):state[scratch_base+a*w:scratch_base+(a+1)*w]^=state[value*w:(value+1)*w]
        mapped_gates(gates,state,mapping,inverse)
        for a,value in enumerate(call['args']):state[scratch_base+a*w:scratch_base+(a+1)*w]^=state[value*w:(value+1)*w]
    for call in manifest['forward_calls']:invoke(call,False)
    for i,name in enumerate(outnames):
        value=manifest['outputs'][name];state[output_base+i*w:output_base+(i+1)*w]^=state[value*w:(value+1)*w]
    for call in reversed(manifest['forward_calls']):invoke(call,True)
    values={name:sum(int(state[output_base+i*w+j])<<j for j in range(w)) for i,name in enumerate(outnames)}
    permitted=input_positions|set(range(output_base,scratch_base))
    clean=all(state[j]==0 for j in range(len(state)) if j not in permitted)
    inputs_preserved=all(state[j]==before[j] for j in input_positions)
    return dict(values=values,workspace_clean=clean,inputs_preserved=inputs_preserved)
