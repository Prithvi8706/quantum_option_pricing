"""One original native adder, ideal logical cat-gate translation and bounded assumption screen."""
import time
START=time.monotonic()
import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
OUT=ROOT/'results/independent_110_20261004/H07/run001'
BASE='results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth'
LEAF='e82b3b95aeec6ad90fab'
INPUTS=[BASE+'/target.json',BASE+'/source.json',BASE+'/leaves/'+LEAF+'.json',BASE+'/leaves/'+LEAF+'.npy',
    'results/limitation_program_20261001/A10_coefficient_run001/executed_code/primitives.py',
    'research/journal_sprint/reversible_fixed_point.py',
    'results/limitation_program_20261001/H17_demand_run002/summary.json',
    'results/limitation_program_20261001/H17_demand_run002/hardware_provenance.json',
    'results/limitation_program_20261001/H17_demand_run002/manifest.json',
    'docs/limitation_audit_20261001/implementation_plan/roadmap.json',
    'docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md',
    'research/independent_110_20261004/H07/primary_sources/Guillaud_Mirrahimi_1904_09474v1.pdf',
    'research/independent_110_20261004/H07/primary_sources/Guillaud_Mirrahimi_2009_10756v1.pdf',
    Path(__file__).resolve().relative_to(ROOT).as_posix(),
    'docs/independent_110_20261004/H07/GATE_AND_NOISE_ASSUMPTIONS.txt',
    'docs/independent_110_20261004/H07/PREFLIGHT_PRIMARY_run001.json',
    'research/independent_110_20261004/H07/PRIMARY_RETRIEVAL_run001.json',
    'research/independent_110_20261004/H07/COLLECTOR_LAUNCH_FAILED_001.json']

def require(ok,message):
    if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def write(name,data):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(data,f,sort_keys=True,indent=2);f.write('\n')
def pinset():return {p:sha((ROOT/p).read_bytes()) for p in INPUTS}
def guard():require(time.process_time()<30 and time.monotonic()-START<60,'30CPU/60scriptwall cap')

def prepare():
    require(not OUT.exists(),'Fresh fixed H07 output')
    pins=pinset();require(sum((ROOT/p).stat().st_size for p in INPUTS)<16*2**20,'16MiB fixed input cap')
    OUT.mkdir(parents=True)
    write('protocol.json',{'schema':'H07-one-original-adder-screen-v1','corpus_sha256':pins,
      'original_source':'A10 B4x12 min-depth, original72/F40, call28/leaf'+LEAF,
      'target_hash':'a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384',
      'assumptions':['Ideal X/CNOT/Toffoli operators are phase-free permutations. Protected cat implementation must meet their complete quantum channel, not merely basis values.',
        'Cuccaro majority/unmajority induction proves the logical modular adder; small-register cases are bounded diagnostics, not a physical certificate.',
        'Direct protected cat gates retain preparation/correction/extraction/routing/idle and noise obligations. Finite unprovided parameters remain null.',
        'Seven-T logical Toffoli is the archived baseline; no hardware clock or new published error rate is transferred.'],
      'corpus_math':{'small_widths':[1,2,3,4],'all_input_and_dirty_output_words':True,'expected_basis_cases':4680,'majority_bit_cases':8,
        'native_original_width':72,'native_original_fraction_bits':40,'physical_gate_candidates':1,'illustrative_repetition_distance':3},
      'acceptance':['Reconstruct original native72-bit gate sequence exactly and reconcile its native/resources/call binding.',
        'Each fixed small-register input/output-word case matches independent integer signed-modular addition, preserves inputs and cleans workspace; inverse restores all bits.',
        'One cat logical gate translation and its protected-operation/error ledger are explicit; direct and distilled paths are not mixed.',
        'Six physical-admission controls reject missing noise/duration/correction/connectivity/failure data and uncharged operations.',
        'Current whole-price error-per-operation requirements are attached from archived H17; no new physical source certificate is claimed.'],
      'budgets':{'CPU_seconds':30,'script_wall_seconds':60,'input_bytes':16*2**20,'output_bytes':4*2**20,'owned_files':16},
      'stop':'One translated logical adder and one fixed finite identity/admission screen. Missing usable finite cat error/duration closes physical integration before full-source extrapolation; no second architecture/model/cutoff.',
      'new_finance_draws':0,'new_global_fixture_credit':0,'source_adoption':False,'quantum_advantage':False})
    print(json.dumps({'prepared':True,'files':len(pins),'protocol_sha256':sha((OUT/'protocol.json').read_bytes())}))

def gates(n):
    a=list(range(n));b=list(range(n,2*n));out=list(range(2*n,3*n));work=list(range(3*n,4*n));helper=4*n;rows=[]
    def cx(x,y):rows.append((2,x,y,0))
    def ccx(x,y,z):rows.append((3,x,y,z))
    def maj(x,y,z):cx(x,y);cx(x,z);ccx(z,y,x)
    def uma(x,y,z):ccx(z,y,x);cx(x,z);cx(z,y)
    for x,y in zip(a,work):cx(x,y)
    maj(b[0],work[0],helper)
    for i in range(n-1):maj(b[i+1],work[i+1],b[i])
    for i in reversed(range(n-1)):uma(b[i+1],work[i+1],b[i])
    uma(b[0],work[0],helper)
    compute=rows.copy()
    for x,y in zip(work,out):cx(x,y)
    rows+=list(reversed(compute))
    return rows

def npy_rows(path):
    data=(ROOT/path).read_bytes();require(data[:6]==b'\x93NUMPY','Original NPY magic')
    major=data[6];require(major in (1,2),'NPY versions1/2')
    length=struct.unpack('<H' if major==1 else '<I',data[8:10] if major==1 else data[8:12])[0]
    start=10 if major==1 else 12;header=ast.literal_eval(data[start:start+length].decode('latin1').strip())
    require(header['descr']=='<i4' and not header['fortran_order'] and header['shape'][1]==4,'Pinned native int32 row format')
    body=data[start+length:];require(len(body)==header['shape'][0]*16,'Exact native payload')
    return list(struct.iter_unpack('<4i',body))

def apply(rows,bits):
    for kind,a,b,c in rows:
        if kind==1:bits^=1<<a
        elif kind==2:bits^=((bits>>a)&1)<<b
        elif kind==3:bits^=(((bits>>a)&1)&((bits>>b)&1))<<c
        else:raise ValueError('Unknown native gate')
    return bits

def admission(record):
    needed=['noise_bias','leakage_bound','nonadiabatic_error_bound','gate_duration_seconds','full_channel_certificate',
      'preparation_correction_extraction','connectivity','idle_error_bound','complete_failure_upper','allocated_failure_upper']
    require(all(record.get(k) is not None for k in needed),'Missing protected cat implementation input')
    require(record['preparation_correction_extraction'] is True,'Every correction/preparation/extraction charged')
    require(record['full_channel_certificate'] is True,'Coherent full-channel identity')
    require(record['complete_failure_upper']<=record['allocated_failure_upper'],'Complete allocated failure met')

def run(expected):
    require(not (OUT/'RUN_STARTED.json').exists(),'One frozen invocation')
    protocol=json.loads((OUT/'protocol.json').read_bytes());require(sha((OUT/'protocol.json').read_bytes())==expected,'Actual protocol')
    require(pinset()==protocol['corpus_sha256'],'Fresh initial frozen SHA')
    write('RUN_STARTED.json',{'original_target_only':True,'physical_device_executed':False})
    write('FAILED_UNSEALED.json',{'passed':False,'provisional':True})
    try:
        source=json.loads((ROOT/(BASE+'/source.json')).read_bytes());leaf=json.loads((ROOT/(BASE+'/leaves/'+LEAF+'.json')).read_bytes())
        require(source['word_width']==72 and source['fraction_bits']==40 and sha((ROOT/(BASE+'/target.json')).read_bytes())==protocol['target_hash'],'Original72/F40 target')
        require(source['forward_calls'][28]['leaf']==LEAF and source['forward_calls'][28]['args']==[35,37] and source['forward_calls'][28]['out']==[38],'Exact original add call')
        original=npy_rows(BASE+'/leaves/'+LEAF+'.npy');generated=gates(72)
        require(original==generated,'Original ordered native adder rows reconstructed exactly')
        counts=Counter(r[0] for r in original)
        require(leaf['resources']['qubits']==289 and counts[2]==792 and counts[3]==288 and leaf['resources']['t_count']==7*counts[3],'Native/archived seven-T resources')
        require(sha((ROOT/(BASE+'/leaves/'+LEAF+'.npy')).read_bytes())==leaf['sha256'],'Original archived gate SHA')
        majority_cases=0
        for x in (0,1):
            for y in (0,1):
                for z in (0,1):
                    initial=x|(y<<1)|(z<<2)
                    maj=[(2,0,1,0),(2,0,2,0),(3,2,1,0)]
                    uma=[(3,2,1,0),(2,0,2,0),(2,2,1,0)]
                    after=apply(maj,initial)
                    require((after&1)==((x&y)|(x&z)|(y&z)), 'Majority carry truth table')
                    require(apply(uma,after)==x|((x^y^z)<<1)|(z<<2), 'Unmajority sum/restoration truth table')
                    majority_cases+=1
        cases=0
        for n in (1,2,3,4):
            rows=gates(n);mask=(1<<n)-1
            for a in range(1<<n):
                for b in range(1<<n):
                    for dirty in range(1<<n):
                        guard();before=a|(b<<n)|(dirty<<(2*n));after=apply(rows,before)
                        wanted=a|(b<<n)|((dirty^((a+b)&mask))<<(2*n))
                        require(after==wanted and apply(reversed(rows),after)==before,'Signed modular clean dirty-XOR/inverse case')
                        cases+=1
        require(cases==4680,'Fixed complete small-register corpus')
        h17=json.loads((ROOT/'results/limitation_program_20261001/H17_demand_run002/summary.json').read_bytes())
        missing={k:None for k in ['noise_bias','leakage_bound','nonadiabatic_error_bound','gate_duration_seconds','full_channel_certificate',
          'preparation_correction_extraction','connectivity','idle_error_bound','complete_failure_upper','allocated_failure_upper']}
        # Artificial admission controls test bookkeeping only; they are not physical scenarios.
        synthetic={k:1 for k in missing};synthetic.update(full_channel_certificate=True,preparation_correction_extraction=True,
          complete_failure_upper=0,allocated_failure_upper=1)
        controls=[]
        for key,value in [('noise_bias',None),('gate_duration_seconds',None),('full_channel_certificate',False),
            ('preparation_correction_extraction',False),('connectivity',None),('complete_failure_upper',2)]:
            bad=synthetic.copy();bad[key]=value
            try:admission(bad)
            except ValueError as error:controls.append({'field':key,'rejected':True,'reason':str(error)})
            else:raise ValueError('Escaped physical-admission control')
        try:admission(missing)
        except ValueError:physical=False
        else:raise ValueError('Missing cat architecture was admitted')
        ledger={'original_add_leaf':LEAF,'native_qubits':289,'native_CNOT':792,'native_Toffoli':288,
          'archived_seven_T_count':2016,'cat_candidate_ideal_native_gate_count':1080,
          'cat_gate_translation':{'native_CNOT':'Ideal logical protected CNOT with required bias preservation/noisy-channel certificate',
            'native_Toffoli':'Ideal logical protected Toffoli with coherent phases/corrections and finite gate-noise certificate'},
          'fixed_paper_round_robin_d3_inventory':{'data_helper_cat_modes_without_EC_ancillas':867,
            'physical_cat_CNOT_before_EC':2376,'physical_cat_Toffoli_before_EC':2592,
            'interpiece_target_EC_obligations':576,'final_full_EC_and_control_fault_detection_cost':None,
            'finite_d3_fault_tolerance_claimed':False,'concatenation_or_tailored_detection_required_for_admission':True},
          'physical_parameters':missing,'direct_cat_gate_error_equals_zero':False,'physical_architecture_admitted':physical,
          'paper_interface_only':True,'prepared_cat_blocks_and_syndrome_ancillas':None,'routing_and_controller_cost':None,
          'whole_price_H17_requirements':[{'case':r['case'],'failure_requirements':r['failure_requirements']} for r in h17['case_rows']],
          'new_physical_timing':None,'new_global_fixture_credit':0}
        write('gate_noise_ledger.json',ledger);write('negative_admission_controls.json',controls)
        write('logical_identity_checks.json',{'native72_rows_exact':len(original),'majority_cases':majority_cases,'small_basis_cases':cases,
          'dirty_output_and_inverse':True,'all_workspace_zero':True,'arbitrary_width_induction_in_proof':True,
          'candidate_noisy_full_channel_proved':False,'new_financial_gate_replays':0})
        require(pinset()==protocol['corpus_sha256'],'Fresh final frozen SHA');guard()
        write('summary.json',{'passed':True,'completed':True,'scope':'H07 one ideal logical adder translation and finite cat noise/admission screen',
          'logical_translation_passed':True,'physical_integration':'CLOSED_MISSING_FINITE_NOISE_DURATION_AND_IMPLEMENTATION',
          'native_width':72,'fraction_bits':40,'small_basis_cases':cases,'negative_controls':len(controls),
          'protected_hardware_error_or_duration_certified':False,'full_source_extrapolation':False,
          'new_global_fixture_credit':0,'source_adoption':False,'quantum_advantage':False,
          'CPU_checkpoint':time.process_time(),'script_wall_checkpoint':time.monotonic()-START})
        owned=[p for p in OUT.iterdir() if p.is_file() and p.name!='FAILED_UNSEALED.json']
        require(len(owned)+2<=16 and sum(p.stat().st_size for p in owned)+65536<4*2**20,'Reserved owned caps')
        write('manifest.json',{'files':{p.name:sha(p.read_bytes()) for p in owned},'input_pins':protocol['corpus_sha256'],'self_hash_excluded':True})
        (OUT/'FAILED_UNSEALED.json').unlink()
        print(json.dumps({'passed':True,'basis_cases':cases,'physical_integration':False,'manifest_sha256':sha((OUT/'manifest.json').read_bytes())}))
    except BaseException as error:
        (OUT/'FAILED_UNSEALED.json').write_text(json.dumps({'passed':False,'error':str(error),'error_type':type(error).__name__})+'\n')
        raise

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['prepare','run']);ap.add_argument('--protocol-sha256');a=ap.parse_args()
    if a.mode=='prepare':prepare()
    else:run(a.protocol_sha256)
