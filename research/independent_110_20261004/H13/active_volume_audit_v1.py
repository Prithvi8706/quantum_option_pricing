"""Fixed original leaf/chain gadget billing and logical-idle audit, no physical timing."""
from pathlib import Path
from collections import Counter
import ast
import gzip
import hashlib
import importlib.util
import json
import struct

ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('scoped_runtime',ROOT/'research/independent_110_20261004/scoped_audit_runtime_v1.py')
rt=importlib.util.module_from_spec(spec);spec.loader.exec_module(rt)
CASE='results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/'
MUL='1e0b2dc8929b29814d9a';ADD='e82b3b95aeec6ad90fab'
PRIMARY='research/independent_110_20261004/H13/primary_sources/Litinski_Nickerson_2211_15465v1.html'
OUT=ROOT/'results/independent_110_20261004/H13/run001'
MODULE_CAPACITY=20000

def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))

def npy_rows(key,q):
    raw=(ROOT/(CASE+'leaves/'+key+'.npy')).read_bytes()
    assert raw[:8]==b'\x93NUMPY\x01\x00'
    h=struct.unpack('<H',raw[8:10])[0];header=ast.literal_eval(raw[10:10+h].decode('ascii').strip())
    assert header['descr']=='<i4' and not header['fortran_order'] and header['shape'][1]==4
    assert len(raw)==10+h+16*header['shape'][0]
    rows=list(struct.iter_unpack('<4i',raw[10+h:]))
    for kind,a,b,c in rows:
        ws=(a,) if kind==1 else (a,b) if kind==2 else (a,b,c)
        assert kind in (1,2,3) and len(set(ws))==len(ws) and all(0<=w<q for w in ws)
    return rows

def expand(rows):
    for kind,a,b,c in rows:
        if kind==1:yield 'X',(a,)
        elif kind==2:yield 'CX',(a,b)
        else:
            yield from [('H',(c,)),('CX',(b,c)),('Tdg',(c,)),('CX',(a,c)),
              ('T',(c,)),('CX',(b,c)),('Tdg',(c,)),('CX',(a,c)),('T',(b,)),
              ('T',(c,)),('H',(c,)),('CX',(a,b)),('T',(a,)),('Tdg',(b,)),('CX',(a,b))]

def metrics(rows,q):
    native=Counter(g[0] for g in rows);counts=Counter();td=[0]*q;depth=[0]*q;touches=0
    for name,ws in expand(rows):
        counts[name]+=1;touches+=len(ws)
        t=max(td[w] for w in ws)+int(name in ('T','Tdg'));d=max(depth[w] for w in ws)+1
        for w in ws:td[w]=t;depth[w]=d
    D=max(depth);idle=q*D-touches
    assert idle>=0
    proxy=[0]*q
    for kind,a,b,c in rows:
        ws=(a,) if kind==1 else (a,b) if kind==2 else (a,b,c)
        value=max(proxy[w] for w in ws)+int(kind==3)
        for w in ws:proxy[w]=value
    return {'qubits':q,'source_gates':len(rows),'x':native[1],'cx':native[2],'ccx':native[3],
      't_count':counts['T']+counts['Tdg'],'t_depth':max(td),'clifford_t_depth':D,
      'clifford_cx':counts['CX'],'clifford_h':counts['H'],
      'all_allocated_ideal_wire_layers':q*D,'gate_wire_touches':touches,
      'ideal_all_to_all_idle_wire_layers':idle,'native_CCX_wire_dependency_proxy':max(proxy),
      'physical_reaction_depth':None,'physical_idle_qubit_seconds':None}

def chain(source,capped,metadata,arrays):
    selected=[27,36,35,37,38];widths=capped['widths']
    assert [widths[v] for v in selected]==[72,72,38,72,72]
    assert capped['proof_masks'][35]<(1<<38)
    assert source['forward_calls'][27]['leaf']==MUL and source['forward_calls'][28]['leaf']==ADD
    assert source['forward_calls'][27]['args']==[27,36] and source['forward_calls'][27]['out']==[37]
    assert source['forward_calls'][28]['args']==[35,37] and source['forward_calls'][28]['out']==[38]
    offsets={};cursor=0
    for v in selected:offsets[v]=cursor;cursor+=widths[v]
    output=cursor;private=cursor+72
    q=private+max(metadata[k]['resources']['qubits']-72 for k in (MUL,ADD))
    result=[];segments=[]
    for index,inverse in [(27,False),(28,False),('output',False),(28,True),(27,True)]:
        begin=len(result)
        if index=='output':
            result.extend((2,offsets[38]+j,output+j,0) for j in range(72))
            segments.append({'kind':'output_XOR','native_rows':72});continue
        call=source['forward_calls'][index];key=call['leaf'];meta=metadata[key]
        mapping={};pos=private
        for reg in meta['args']:
            for w in reg:mapping[w]=pos;pos+=1
        for reg,value in zip(meta['outs'],call['out'],strict=True):
            for j,w in enumerate(reg):mapping[w]=offsets[value]+j
        for w in range(meta['resources']['qubits']):
            if w not in mapping:mapping[w]=pos;pos+=1
        assert pos-private==meta['resources']['qubits']-72
        copies=[]
        for reg,value in zip(meta['args'],call['args'],strict=True):
            copies.extend((2,offsets[value]+j,mapping[reg[j]],0) for j in range(widths[value]))
        result.extend(copies)
        for kind,a,b,c in (reversed(arrays[key]) if inverse else arrays[key]):
            result.append((kind,mapping[a],mapping[b] if kind>=2 else 0,mapping[c] if kind==3 else 0))
        result.extend(reversed(copies))
        segments.append({'kind':'inverse_call' if inverse else 'forward_call','call':index,
          'leaf':key,'copy_CX':2*len(copies),'native_rows':len(result)-begin})
    assert len(result)==49076 and q==6117
    return result,q,segments

def emit_billing(name,rows):
    # Each native gate is bound to a named primary gadget instance. Block ranges
    # are unoptimized component IDs, not an oriented or routed block network.
    block=0
    path=OUT/(name+'_component_instances.jsonl.gz')
    with path.open('xb') as raw:
        with gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0) as z:
            for i,(kind,a,b,c) in enumerate(rows):
                if kind==1:
                    rec={'i':i,'gate':'X','w':[a],'component':'Pauli_frame_obligation','block_range':None,'cost':None}
                else:
                    n=4 if kind==2 else 12
                    rec={'i':i,'gate':'CX' if kind==2 else 'CCX','w':[a,b] if kind==2 else [a,b,c],
                      'component':'Fig7f_CNOT' if kind==2 else 'Fig14c_Toffoli',
                      'block_range':[block,block+n],'CCZ_inputs':int(kind==3)}
                    block+=n
                z.write((json.dumps(rec,separators=(',',':'))+'\n').encode())
    return block

FIELDS=['physical_module_capacity','code_distance','code_cycle_seconds','reaction_seconds','CCZ_factory_blocks',
  'CCZ_factory_failure','actual_memory_capacity','resource_buffer_peak','oriented_port_network','nonlocal_connection_schedule',
  'Pauli_frame_dispatch','complete_failure_upper','complete_execution_seconds']
def admit(r):
    assert all(r.get(k) is not None for k in FIELDS),'Missing active-volume schedule or physical cost'
    assert r['oriented_port_network'] is True and r['nonlocal_connection_schedule'] is True
    assert r['complete_failure_upper']<=3/1000

def check():
    html=(ROOT/PRIMARY).read_text(encoding='utf-8')
    assert all(s in html for s in ['2211.15465v1','reaction depth of 1','12 blocks'])
    source=read(CASE+'source.json');capped=read(CASE+'schedule_capped.json')
    assert (source['word_width'],source['fraction_bits'])==(72,40)
    meta={key:read(CASE+'leaves/'+key+'.json') for key in (MUL,ADD)}
    arrays={key:npy_rows(key,meta[key]['resources']['qubits']) for key in (MUL,ADD)}
    for key in (MUL,ADD):
        assert hashlib.sha256((ROOT/(CASE+'leaves/'+key+'.npy')).read_bytes()).hexdigest()==meta[key]['sha256']
        m=metrics(arrays[key],meta[key]['resources']['qubits'])
        assert all(m[k]==meta[key]['resources'][k] for k in ['qubits','source_gates','x','cx','ccx','t_count','t_depth','clifford_t_depth','clifford_cx','clifford_h'])
    rows,q,segments=chain(source,capped,meta,arrays)
    cases=[]
    for name,native,width in [('multiply_leaf',arrays[MUL],5791),('compute_copy_inverse_chain',rows,q)]:
        m=metrics(native,width);bill=emit_billing(name,native)
        assert bill==4*m['cx']+12*m['ccx']
        memory=MODULE_CAPACITY//2;workspace=MODULE_CAPACITY//2
        serial_reservation=width+3+6
        cases.append({'case':name,'logical_baseline_metrics':m,
          'unoptimized_primary_CNOT_Toffoli_block_subtotal':bill,'CCZ_states_required':m['ccx'],
          'full_volume_formula':'subtotal + CCX_count*C_CCZ + frame + routing + prep/readout',
          'full_active_volume':None,'oriented_or_routed_block_network_emitted':False,
          'component_registry_instances_emitted':True,'temporary_AND_substitution_applied':False,
          'isolated_Toffoli_reaction_depth':1,'reactive_output_qubits_per_serial_Toffoli':6,
          'assumed_diagnostic_module_capacity':MODULE_CAPACITY,'assumed_memory_modules':memory,
          'assumed_workspace_modules':workspace,'declared_serial_CCZ_and_reactive_output_memory_reservation':serial_reservation,
          'declared_serial_reservation_fits_assumed_capacity':serial_reservation<=memory,
          'simultaneous_CCZ_and_reactive_output_liveness_certified':False,
          'known_subtotal_workspace_cycles_lower':(bill+workspace-1)//workspace,
          'cycle_lower_bound_is_executable_schedule':False,
          'physical_reaction_layers':None,'actual_physical_capacity':None,'physical_idle_seconds':None,
          'complete_seconds':None,'same_capacity_measured_comparison':None})
    assert cases[0]['unoptimized_primary_CNOT_Toffoli_block_subtotal']==180712
    assert cases[1]['unoptimized_primary_CNOT_Toffoli_block_subtotal']==379024
    assert cases[1]['logical_baseline_metrics']['ccx']==23064
    actual={k:None for k in FIELDS};negative=[]
    for field in FIELDS:
        witness={k:True for k in FIELDS};witness.update(complete_failure_upper=0)
        witness[field]=None
        try:admit(witness)
        except AssertionError:negative.append({'missing_field':field,'rejected':True})
        else:raise AssertionError('Missing active-volume obligation admitted')
    try:admit(actual)
    except AssertionError as error:reason=str(error)
    else:raise AssertionError('Original null architecture admitted')
    return {'decision':'COMPONENT_MAPPING_COMPLETE_PHYSICAL_NETWORK_AND_SCHEDULE_UNRESOLVED',
      'primary_url':'https://arxiv.org/html/2211.15465v1','locators':['Fig7f/g','Fig14c','Fig15','Section1/4/5'],
      'checks':{'metadata_leaf_rows':2,'mapped_cases':2,'negative_interface_controls':len(negative)},
      'cases':cases,'chain_segments':segments,'actual_physical_inputs':actual,'admission_reason':reason,
      'negative_controls':negative,'H03_failed_map_reused_as_accepted_evidence':False,
      'units_ideal_wire_layers_not_physical_code_cycles':True,'baseline_idle_and_active_block_ratio_claimed':False,
      'broader_obligations':['Emit compatible oriented port and nonlocal connection network','Certify module/buffer/factory allocation and dwell','Track every reactive byproduct and frame','Choose finite code/noise/factory/readout parameters','Complete union-bound failure and latency accounting']}

if __name__=='__main__':
    rt.launch(__file__,'H13',[CASE+'source.json',CASE+'schedule_capped.json',
      CASE+'leaves/'+MUL+'.json',CASE+'leaves/'+MUL+'.npy',CASE+'leaves/'+ADD+'.json',CASE+'leaves/'+ADD+'.npy',
      'research/independent_110_20261004/H03/reaction_map_v1.py',PRIMARY,
      'results/limitation_program_20261001/H17_demand_run002/summary.json',
      'docs/limitation_audit_20261001/implementation_plan/roadmap.json'],
      ['Reconcile two original leaf gate arrays and exact seven-T metadata.',
       'Bind one compute-copy-inverse slice; emit component-gadget instances without claiming oriented routing.',
       'Separate ideal wire-idle metric, block subtotal, resource memory and unimplemented reaction/duration.'
       ,'All missing actual physical obligations reject admission.'],
      ['One original multiplier and its fixed dependent multiply-add slice; one assumed20000-module capacity diagnostic.',
       'No full frame-DAG attempt, budget retry, new arithmetic, finance samples, hardware timings or F31 crossover ledger.'],check)
