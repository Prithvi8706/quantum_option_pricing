"""H03 fixed, stdlib-only reaction-interface inventory; no scientific imports."""
from __future__ import annotations
import argparse
import ast
import cmath
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
BASE = 'results/limitation_program_20261001/A10_coefficient_run001'
CASE = BASE + '/B4x12/min-depth'
H17 = 'results/limitation_program_20261001/H17_demand_run002'
OWN = 'research/independent_110_20261004/H03'
MUL = '1e0b2dc8929b29814d9a'
ADD = 'e82b3b95aeec6ad90fab'
OUT = ROOT / 'results/independent_110_20261004/H03/run001'
INPUTS = [
    CASE+'/target.json', CASE+'/source.json', CASE+'/schedule_capped.json',
    CASE+'/leaves/'+MUL+'.json', CASE+'/leaves/'+MUL+'.npy',
    CASE+'/leaves/'+ADD+'.json', CASE+'/leaves/'+ADD+'.npy',
    BASE+'/executed_code/primitives.py', BASE+'/executed_code/compiler.py',
    H17+'/protocol.json', H17+'/B4x12/hardware_demand.json',
    H17+'/executed_code/hardware_demand_v2.py',
    OWN+'/primary_sources/Fowler_1210_4626v3.pdf',
    OWN+'/primary_sources/Fowler_1210_4626v3_abs.html',
    OWN+'/reaction_map_v1.py',
    'docs/independent_110_20261004/H03/ASSUMPTIONS_run001.txt',
]
CAPS = dict(cpu_seconds=60, wall_seconds=90, input_bytes=16*1024**2,
            output_bytes=32*1024**2, output_files=32, expanded_gates=600000)
COUNT_KEYS = ('source_gates','x','cx','ccx','t_count','t_depth',
              'clifford_t_depth','clifford_cx','clifford_h')
PINNED_TARGET = 'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384'
PHYSICAL = ('code_cycle_seconds','measurement_seconds','transport_seconds',
            'decoder_seconds','conditional_dispatch_seconds',
            'clifford_surgery_seconds','S_correction_seconds',
            'resource_preparation_seconds','routing_seconds',
            'physical_peak_qubits','connectivity_certificate',
            'preparation_opportunity_count','feedback_opportunity_count',
            'idle_opportunity_count','complete_failure_bound')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_json(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))


def write_json(name, data):
    path = OUT/name
    if path.exists():
        raise ValueError('Refuse overwrite: '+str(path))
    path.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n',encoding='utf-8')


def prepare():
    if OUT.exists():
        raise ValueError('Fresh output required')
    records = []
    for path in INPUTS:
        raw = (ROOT/path).read_bytes()
        records.append(dict(path=path, bytes=len(raw), sha256=digest(raw)))
    total = sum(item['bytes'] for item in records)
    if total > CAPS['input_bytes']:
        raise ValueError('Input budget exceeded')
    OUT.mkdir(parents=True)
    write_json('protocol.json', dict(
        schema='H03-reaction-interface-protocol-v1', corpus=records,
        corpus_bytes=total, budgets=CAPS, cases=['multiply_leaf','clean_multiply_add_slice'],
        interfaces=['conventional_immediate_S','Bell_T_with_selective_S_obligation'],
        acceptance=['native_metadata_control','clean_slice_bindings','gadget_identities',
                    'explicit_measurement_correction_DAG','failure_admission_controls'],
        stop='One fixed invocation, two cases/two interfaces; no missing-field transfer or scaling',
        no_science_imports=True, no_financial_gate_replay=True, no_timing_benchmark=True,
        source_version='original72-F40-A10-compatible-with-H17_demand_run002',
        selective_macro_complete=False, physical_schedules_adopted=0,
        primary=dict(url='https://arxiv.org/pdf/1210.4626v3',version='v3',
                     locators=['Fig. 1','Fig. 2','Fig. 3'],
                     arxiv_v3_date='2013-02-02',PDF_header_date='2024-11-27',
                     chronology_resolved=False)))
    print(json.dumps(dict(prepared=True, files=len(records), input_bytes=total,
                          protocol_sha256=digest((OUT/'protocol.json').read_bytes()))))


class Guard:
    def __init__(self):
        self.wall = time.monotonic()
        self.cpu = time.process_time()
        self.expanded = 0

    def check(self):
        if time.monotonic()-self.wall > CAPS['wall_seconds']:
            raise ValueError('Wall budget exceeded')
        if time.process_time()-self.cpu > CAPS['cpu_seconds']:
            raise ValueError('CPU budget exceeded')
        if self.expanded > CAPS['expanded_gates']:
            raise ValueError('Expanded gate budget exceeded')
        files = [p for p in OUT.iterdir() if p.is_file()]
        # Reserve one manifest and a failure marker.
        if len(files)+2 > CAPS['output_files']:
            raise ValueError('Output file budget exceeded')
        if sum(p.stat().st_size for p in files)+65536 > CAPS['output_bytes']:
            raise ValueError('Output byte budget exceeded')


def npy_rows(path, qubits):
    raw=(ROOT/path).read_bytes()
    if raw[:6] != b'\x93NUMPY' or raw[6:8] != b'\x01\x00':
        raise ValueError('Unsupported fixed NPY header')
    hlen=struct.unpack('<H',raw[8:10])[0]
    header=ast.literal_eval(raw[10:10+hlen].decode('ascii').strip())
    if header['descr']!='<i4' or header['fortran_order'] or len(header['shape'])!=2 or header['shape'][1]!=4:
        raise ValueError('NPY layout mismatch')
    n=header['shape'][0]
    if len(raw)!=10+hlen+n*16:
        raise ValueError('NPY byte extent mismatch')
    rows=list(struct.iter_unpack('<4i',raw[10+hlen:]))
    for kind,a,b,c in rows:
        ws=(a,) if kind==1 else (a,b) if kind==2 else (a,b,c)
        if kind not in (1,2,3) or len(set(ws))!=len(ws) or any(w<0 or w>=qubits for w in ws):
            raise ValueError('Invalid native gate/wire')
    return rows


def expand(rows):
    for kind,a,b,c in rows:
        if kind==1:
            yield 'X',(a,)
        elif kind==2:
            yield 'CX',(a,b)
        else:
            yield from [('H',(c,)),('CX',(b,c)),('Tdg',(c,)),('CX',(a,c)),
                        ('T',(c,)),('CX',(b,c)),('Tdg',(c,)),('CX',(a,c)),
                        ('T',(b,)),('T',(c,)),('H',(c,)),('CX',(a,b)),
                        ('T',(a,)),('Tdg',(b,)),('CX',(a,b))]


def resources(rows, q):
    native=Counter(g[0] for g in rows)
    t=[0]*q; d=[0]*q
    counts=Counter()
    for name,ws in expand(rows):
        counts[name]+=1
        tt=max(t[w] for w in ws)+int(name in ('T','Tdg'))
        dd=max(d[w] for w in ws)+1
        for w in ws:
            t[w]=tt; d[w]=dd
    return dict(qubits=q, source_gates=len(rows),x=native[1],cx=native[2],ccx=native[3],
                t_count=counts['T']+counts['Tdg'],t_depth=max(t),clifford_t_depth=max(d),
                clifford_cx=counts['CX'],clifford_h=counts['H'])


def slice_rows(source, capped, metadata, arrays):
    widths=capped['widths']
    selected=[27,36,35,37,38]
    if [widths[v] for v in selected] != [72,72,38,72,72]:
        raise ValueError('Selected compact widths changed')
    offsets={}; cursor=0
    for value in selected:
        offsets[value]=cursor; cursor+=widths[value]
    output=cursor; private=cursor+72
    private_size=max(metadata[k]['resources']['qubits']-72 for k in (MUL,ADD))
    q=private+private_size
    result=[]; segments=[]
    for call_index,direction in [(27,False),(28,False),('output',False),(28,True),(27,True)]:
        begin=len(result)
        if call_index=='output':
            result.extend((2,offsets[38]+j,output+j,0) for j in range(72))
            segments.append(dict(kind='named_output_XOR',start=begin,stop=len(result),cx=72))
            continue
        call=source['forward_calls'][call_index]; key=call['leaf']; meta=metadata[key]
        mapping={}; pos=private
        for reg in meta['args']:
            for w in reg:
                mapping[w]=pos; pos+=1
        for reg,value in zip(meta['outs'],call['out'],strict=True):
            for j,w in enumerate(reg):
                mapping[w]=offsets[value]+j
        for w in range(meta['resources']['qubits']):
            if w not in mapping:
                mapping[w]=pos;pos+=1
        if pos-private != meta['resources']['qubits']-72:
            raise ValueError('Private native allocation mismatch')
        copies=[]
        for reg,value in zip(meta['args'],call['args'],strict=True):
            copies.extend((2,offsets[value]+j,mapping[reg[j]],0) for j in range(widths[value]))
        result.extend(copies)
        for kind,a,b,c in (reversed(arrays[key]) if direction else arrays[key]):
            result.append((kind,mapping[a],mapping[b] if kind>=2 else 0,
                           mapping[c] if kind==3 else 0))
        result.extend(reversed(copies))
        segments.append(dict(kind='inverse_call' if direction else 'forward_call',
                             call_index=call_index,leaf=key,start=begin,stop=len(result),
                             active_argument_bits=len(copies),copy_CX=2*len(copies)))
    return result,q,segments,list(range(output,output+72))


class Stream:
    def __init__(self,path):
        self.raw=path.open('xb')
        self.z=gzip.GzipFile(filename='',fileobj=self.raw,mode='wb',mtime=0)

    def emit(self,value):
        self.z.write((json.dumps(value,separators=(',',':'))+'\n').encode())

    def close(self):
        self.z.close(); self.raw.close()


class Frames:
    """Topological XOR DAG. Conservative causal depth is not a physical clock."""
    def __init__(self,q,stream):
        self.x=[0]*q; self.z=[0]*q
        self.depth=[0];self.stream=stream;self.measured=0;self.nodes=0

    def node(self,value,depth):
        self.depth.append(depth); self.nodes+=1
        self.stream.emit([len(self.depth)-1,*value])
        return len(self.depth)-1

    def xor(self,a,b):
        if a==0:return b
        if b==0:return a
        if a==b:return 0
        return self.node(['xor',a,b],max(self.depth[a],self.depth[b]))

    def gate(self,name,ws,gid):
        if name=='H':
            w=ws[0];self.x[w],self.z[w]=self.z[w],self.x[w]
        elif name=='CX':
            a,b=ws;self.x[b]=self.xor(self.x[b],self.x[a]);self.z[a]=self.xor(self.z[a],self.z[b])
        elif name in ('T','Tdg'):
            w=ws[0]; x,z=self.x[w],self.z[w]
            d=self.depth[x]+1
            a=self.node(['measurement','a',gid,'conservative_cell_waits_for_incoming_X',x],d)
            b=self.node(['measurement','b',gid,'conservative_cell_waits_for_incoming_X',x],d)
            u=self.xor(a,x)
            self.x[w]=u;self.z[w]=self.xor(self.xor(b,z),u)
            self.measured+=2
            self.stream.emit(['T_cell',gid,1 if name=='T' else -1,w,x,z,a,b,u,self.x[w],self.z[w],d])
            return d,int(x!=0)
        return 0,0


def map_case(label,rows,q,outputs,guard):
    control=resources(rows,q)
    operations=Stream(OUT/(label+'_operations.jsonl.gz'))
    frames_stream=Stream(OUT/(label+'_candidate_frames.jsonl.gz'))
    frames=Frames(q,frames_stream)
    last=[0]*q;t=[0]*q;d=[0]*q;max_adaptive=0;prior_x=0;n_t=0
    try:
        for gid,(name,ws) in enumerate(expand(rows),start=1):
            guard.expanded+=1
            tt=max(t[w] for w in ws)+int(name in ('T','Tdg'))
            dd=max(d[w] for w in ws)+1
            preds=sorted({last[w] for w in ws if last[w]})
            operations.emit(['gate',gid,name,ws,preds,tt,dd])
            if name in ('T','Tdg'):
                n_t+=1
                operations.emit(['conventional_measurement',gid,'Z_ancilla',gid])
                operations.emit(['conventional_correction',gid,'S' if name=='T' else 'Sdg',
                                 'decoded_Z_ancilla_bit',gid,
                                 'gate_completion_includes_materialized_conditional_S'])
            rr,has_prior=frames.gate(name,ws,gid)
            max_adaptive=max(max_adaptive,rr);prior_x+=has_prior
            for w in ws:last[w]=gid;t[w]=tt;d[w]=dd
            if gid%8192==0:guard.check()
        if n_t!=control['t_count'] or max(t)!=control['t_depth'] or max(d)!=control['clifford_t_depth']:
            raise ValueError('Control mapping depth/count mismatch')
        # These are future readout/correction obligations. The chain output
        # remains coherent; this inventory does not measure it.
        final=[dict(wire=w,X_frame_expression=frames.x[w],Z_frame_expression=frames.z[w],
                    last_gate=last[w]) for w in outputs]
        frames_stream.emit(['final_coherent_output_frames',final])
        frames_stream.emit(['all_retained_wire_frames',frames.x,frames.z])
    finally:
        operations.close();frames_stream.close()
    unknown={field:None for field in PHYSICAL}
    return dict(logical_control=control,
        conventional=dict(base_T_injection_measurements=n_t,conditional_S_or_Sdg_decisions=n_t,
            Clifford_CX=control['clifford_cx'],Clifford_H=control['clifford_h'],
            conventional_S_materializations_up_to=n_t,T_resource_consumptions=n_t,
            physical_parity_measurements=None,resource_preparation_paid=True,
            injection_ancilla_peak=None,physical_inputs=unknown,
            executable_latency_seconds=None,admitted=False),
        time_optimal_candidate=dict(base_Bell_measurements=frames.measured,
            conditional_selective_S_decisions=n_t,T_resource_consumptions=n_t,
            base_Bell_resource_qubits_if_all_prepared=2*n_t,
            base_Bell_resource_preparation_CX=n_t,
            additional_selective_macro_measurements=None,additional_selective_macro_resources=None,
            additional_selective_macro_peak_qubits=None,prepared_Clifford_network_cost=None,
            frame_expression_nodes=frames.nodes,selection_events_with_prior_X_expression=prior_x,
            conservative_interface_adaptive_cell_layers=max_adaptive,
            adaptive_depth_is_executable_physical_depth=False,
            reaction_depth_optimality_proved=False,resource_preparation_paid=True,
            physical_inputs=unknown,executable_latency_seconds=None,admitted=False),
        terminal_readout=dict(physical_measurements=None,frame_interpretation_obligations=len(final),
                             chain_output_measured=False))


def apply_one(state,name,w):
    n=len(state);out=state.copy(); step=1<<w
    if name=='H':
        for a in range(n):
            if not a&step:
                b=a|step;out[a]=(state[a]+state[b])/2**0.5;out[b]=(state[a]-state[b])/2**0.5
    elif name=='X':
        for a in range(n):out[a^step]=state[a]
    else:
        phase=cmath.exp((1j if name=='T' else -1j)*cmath.pi/4)
        for a in range(n):
            if a&step:out[a]*=phase
    return out


def gadget_checks():
    # Independent explicit 2x2 operators, not repository imports.
    I=((1,0),(0,1));X=((0,1),(1,0));Z=((1,0),(0,-1))
    def mul(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    def equivalent(A,B):
        pairs=[(A[i][j],B[i][j]) for i in range(2) for j in range(2)]
        aa,bb=next((a,b) for a,b in pairs if abs(b)>1e-9)
        phase=aa/bb
        return abs(abs(phase)-1)<1e-10 and all(abs(a-phase*b)<1e-10 for a,b in pairs)
    checked=0
    for sign in (-1,1):
        T=((1,0),(0,cmath.exp(1j*sign*cmath.pi/4)))
        S=((1,0),(0,cmath.exp(1j*sign*cmath.pi/2)))
        Td=((1,0),(0,cmath.exp(-1j*sign*cmath.pi/4)))
        for x in (0,1):
            for z in (0,1):
                P=mul(X if x else I,Z if z else I)
                for m in (0,1):
                    u=m^x
                    A=mul(S if u else I,mul(T if m==0 else Td,P))
                    target=mul(mul(X if x else I,Z if z^(x&(1-m)) else I),T)
                    if not equivalent(A,target):raise ValueError('Injection frame identity failed')
                    checked+=1
                for a in (0,1):
                    for b in (0,1):
                        u=a^x;zz=b^z^u
                        A=mul(S if u else I,mul(T,mul(mul(X if a else I,Z if b else I),P)))
                        target=mul(mul(X if u else I,Z if zz else I),T)
                        if not equivalent(A,target):raise ValueError('Bell frame identity failed')
                        checked+=1
    ccx_columns=0
    for column in range(8):
        state=[0j]*8;state[column]=1
        for name,ws in expand([(3,0,1,2)]):
            if name=='CX':
                a,b=ws;out=[0j]*8
                for k,v in enumerate(state):out[k^(1<<b) if k&(1<<a) else k]=v
                state=out
            else:state=apply_one(state,name,ws[0])
        expected=column^4 if column&3==3 else column
        if any(abs(v-(1 if k==expected else 0))>1e-10 for k,v in enumerate(state)):
            raise ValueError('Exact seven-T CCX identity failed')
        ccx_columns+=1
    # Fowler Fig. 3: a teleportation Z frame passes through H into X,
    # then CNOT control-X reaches a later T target. This is not independent.
    s=Stream(OUT/'dependency_controls.jsonl.gz')
    try:
        f=Frames(3,s);f.z[0]=f.node(['measurement','inherited_Z',0],1)
        f.gate('H',(0,),1);f.gate('CX',(0,1),2)
        d,dependent=f.gate('T',(1,),3)
        d_disjoint,disjoint=f.gate('T',(2,),4)
        if not (dependent==1 and d==2 and disjoint==0 and d_disjoint==1):
            raise ValueError('Byproduct dependency controls failed')
    finally:s.close()
    return dict(two_sign_frame_and_measurement_identities=checked,CCX_basis_columns=ccx_columns,
                inherited_Z_H_CX_later_T_detected=True,disjoint_T_no_prior_dependency=True,
                numerical_tolerance=1e-10,financial_gate_replays=0)


def admissible(record):
    if any(record.get(k) is None for k in PHYSICAL):return False
    if any(not isinstance(record[k],(int,float)) or isinstance(record[k],bool) or record[k]<0
           for k in PHYSICAL if k!='connectivity_certificate'):return False
    categories=('data_failure_upper','magic_failure_upper','control_failure_upper')
    if any(not isinstance(record.get(k),(int,float)) or isinstance(record.get(k),bool)
           or not 0<=record[k]<=1/1000 for k in categories):return False
    return (record['connectivity_certificate'] is True and record.get('preparation_paid') is True
            and record.get('all_failure_opportunities_counted') is True
            and record['complete_failure_bound']<=3/1000
            and sum(record[k] for k in categories)<=record['complete_failure_bound']
            and record.get('same_failure_allowance')==[3,1000])


def admission_checks():
    positive={k:1 for k in PHYSICAL};positive.update(
        connectivity_certificate=True,complete_failure_bound=1/1000,preparation_paid=True,
        all_failure_opportunities_counted=True,same_failure_allowance=[3,1000],
        data_failure_upper=1/10000,magic_failure_upper=1/10000,control_failure_upper=1/10000)
    if not admissible(positive):raise ValueError('Synthetic admission positive control failed')
    edits=[('missing_preparation',{'resource_preparation_seconds':None}),
           ('missing_workspace',{'physical_peak_qubits':None}),
           ('missing_reaction',{'decoder_seconds':None}),
           ('unpaid_preparation',{'preparation_paid':False}),
           ('excess_failure',{'complete_failure_bound':4/1000}),
           ('unaccounted_extra_opportunities',{'all_failure_opportunities_counted':False})]
    for name,edit in edits:
        if admissible(dict(positive,**edit)):raise ValueError('Negative admission control accepted: '+name)
    return dict(synthetic_positive_controls=1,negative_controls=[name for name,_ in edits],
                actual_hardware_rows=0,positive_control_is_observation=False)


def bind_inputs(protocol):
    for item in protocol['corpus']:
        raw=(ROOT/item['path']).read_bytes()
        if len(raw)!=item['bytes'] or digest(raw)!=item['sha256']:
            raise ValueError('Frozen corpus changed: '+item['path'])
    source=read_json(CASE+'/source.json');capped=read_json(CASE+'/schedule_capped.json')
    demand=read_json(H17+'/B4x12/hardware_demand.json')
    if demand['binding']['hashes']['target.json']!=PINNED_TARGET or digest((ROOT/(CASE+'/target.json')).read_bytes())!=PINNED_TARGET:
        raise ValueError('Original target binding failed')
    for name in ('source.json','schedule_capped.json'):
        if digest((ROOT/(CASE+'/'+name)).read_bytes())!=demand['binding']['hashes'][name]:
            raise ValueError('Original H17 source/schedule binding failed')
    if source['word_width']!=72 or source['fraction_bits']!=40 or not source['exact_clifford_t']:
        raise ValueError('Native contract changed')
    expected=[(27,MUL,[27,36],[37],144),(28,ADD,[35,37],[38],110)]
    for index,key,args,out,active in expected:
        call=source['forward_calls'][index]
        if call['leaf']!=key or call['args']!=args or call['out']!=out:
            raise ValueError('Selected chain attachment failed')
        records=[r for batch in demand['source_batch_profile']['batches'] for r in batch['calls'] if r['call_index']==index]
        if len(records)!=1 or records[0]['leaf']!=key or records[0]['active_argument_copy_bits']!=active:
            raise ValueError('H17 compact call attachment failed')
    metadata={k:read_json(CASE+'/leaves/'+k+'.json') for k in (MUL,ADD)}
    arrays={}
    controls={}
    for k,meta in metadata.items():
        raw=(ROOT/(CASE+'/leaves/'+k+'.npy')).read_bytes()
        if digest(raw)!=meta['sha256']:raise ValueError('Native array archived hash mismatch')
        rows=npy_rows(CASE+'/leaves/'+k+'.npy',meta['resources']['qubits'])
        arrays[k]=rows
        costs=resources(rows,meta['resources']['qubits'])
        if any(costs[field]!=meta['resources'][field] for field in COUNT_KEYS):
            raise ValueError('Archived resource control mismatch: '+k)
        controls[k]=dict(forward=costs,literal_inverse=resources(list(reversed(rows)),costs['qubits']))
    return source,capped,demand,metadata,arrays,controls


def run():
    if not (OUT/'protocol.json').exists() or (OUT/'ATTEMPT.json').exists():
        raise ValueError('Prepare first; exactly one invocation')
    protocol=json.loads((OUT/'protocol.json').read_text())
    if protocol['budgets']!=CAPS or [r['path'] for r in protocol['corpus']]!=INPUTS:
        raise ValueError('Protocol mismatch')
    write_json('ATTEMPT.json',dict(status='STARTED',one_fixed_invocation=True))
    guard=Guard()
    try:
        source,capped,demand,meta,arrays,controls=bind_inputs(protocol)
        gadget=gadget_checks();admission=admission_checks();guard.check()
        chain,q,segments,outputs=slice_rows(source,capped,meta,arrays)
        if [s['kind'] for s in segments]!=['forward_call','forward_call','named_output_XOR','inverse_call','inverse_call']:
            raise ValueError('Compute/copy/uncompute slice changed')
        if len(chain)!=2*(len(arrays[MUL])+len(arrays[ADD]))+2*(288+220)+72:
            raise ValueError('Clean chain gate/copy accounting mismatch')
        mapped={
            'multiply_leaf':map_case('multiply_leaf',arrays[MUL],meta[MUL]['resources']['qubits'],meta[MUL]['outs'][0],guard),
            'clean_multiply_add_slice':map_case('clean_multiply_add_slice',chain,q,outputs,guard)}
        if mapped['clean_multiply_add_slice']['logical_control']['t_count']!=2*(controls[MUL]['forward']['t_count']+controls[ADD]['forward']['t_count']):
            raise ValueError('Chain T accounting mismatch')
        for case in mapped.values():
            for interface in ('conventional','time_optimal_candidate'):
                rec=case[interface]['physical_inputs']
                if admissible(rec):raise ValueError('Actual incomplete physical interface admitted')
        summary=dict(status='PASS_CONDITIONAL_DEPENDENCY_SCREEN_PHYSICAL_TRANSFER_UNRESOLVED',
            controls=controls,gadget_checks=gadget,admission_checks=admission,cases=mapped,
            chain_segments=segments,chain_private_bank_reuse='serial clean scratch only',
            common_H17_failure_requirements=demand['failure_requirements'],
            extra_preparation_idle_feedback_failure_opportunities=None,
            primary=protocol['primary'],new_financial_gate_replays=0,
            accepted_physical_mappings=0,new_compilations_adopted=0,full_source_credit=False,
            expanded_gates_inventory=guard.expanded,
            implementation_limit='Candidate conditional selective-S macro and conventional surgery layout unresolved',
            check_CPU_seconds=time.process_time()-guard.cpu,check_wall_seconds=time.monotonic()-guard.wall,
            check_times_are_performance_measurements=False)
        write_json('summary.json',summary);guard.check()
        write_json('SUCCESS.json',dict(status=summary['status'],physical_transfer_admitted=False))
        files=[p for p in OUT.iterdir() if p.is_file()]
        manifest=dict(files=[dict(path=p.name,bytes=p.stat().st_size,sha256=digest(p.read_bytes())) for p in sorted(files)],
                      no_missing_cost_zeroed=True)
        encoded=json.dumps(manifest,indent=2,sort_keys=True)+'\n'
        if sum(p.stat().st_size for p in files)+len(encoded.encode())>CAPS['output_bytes']:
            raise ValueError('Final manifest budget exceeded')
        write_json('manifest.json',manifest)
        print(json.dumps(dict(status=summary['status'],expanded_gates=guard.expanded,
                              summary_sha256=digest((OUT/'summary.json').read_bytes()))))
    except BaseException as exc:
        if not (OUT/'FAILED.json').exists():
            write_json('FAILED.json',dict(status='FAILED_PRESERVED',error_type=type(exc).__name__,error=str(exc)))
        raise


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['prepare','run'])
    args=parser.parse_args()
    prepare() if args.mode=='prepare' else run()
