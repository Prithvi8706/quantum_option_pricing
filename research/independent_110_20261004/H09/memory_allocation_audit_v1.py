"""Fixed original-source allocation/admission screen; no finance imports or timing."""
import time
START=time.monotonic()
from pathlib import Path
from fractions import Fraction as Q
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'results/independent_110_20261004/H09/run001'
H17='results/limitation_program_20261001/H17_demand_run002/'
INPUTS=[H17+'summary.json',H17+'hardware_provenance.json',H17+'manifest.json',
 'docs/limitation_audit_20261001/implementation_plan/roadmap.json','docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md',
 'docs/independent_110_20261004/H09/PREFLIGHT_PRIMARY_run001.json','docs/independent_110_20261004/H09/MEMORY_INTERFACE_AND_LIMITS.txt',
 'research/independent_110_20261004/H09/primary_sources/Bravyi_2308_07915v1.pdf',
 'research/independent_110_20261004/H09/PRIMARY_RETRIEVAL_run001.json',Path(__file__).resolve().relative_to(ROOT).as_posix()]
def require(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pins():return {p:sha(ROOT/p) for p in INPUTS}
def write(name,data):
 with (OUT/name).open('x',encoding='utf-8') as f:json.dump(data,f,indent=2,sort_keys=True);f.write('\n')
def guard():require(time.process_time()<30 and time.monotonic()-START<60,'30CPU/60scriptwall')
def capacity(m):
 require(type(m) is int and m>=0,'Nonnegative declared storage count')
 blocks=(m+11)//12
 return {'declared_stored_logical':m,'blocks':blocks,'data_qubits':144*blocks,'check_qubits':144*blocks,
  'physical_memory_only':288*blocks,'unused_logical_slots':12*blocks-m,'active_factory_interface_cost_included':False}
def admit(r,total,private):
 needed=['stored_data','active_data','source_ancillas','factory_physical_qubits','physical_cap','conversion_cost',
  'conversion_error','actual_topology','memory_idle_budget','complete_failure_upper','allocated_failure_upper','complete_physical_qubits']
 require(all(r.get(k) is not None for k in needed),'Missing finite allocation/interface fact')
 require(all(type(r[k]) is int and r[k]>=0 for k in ['stored_data','active_data','source_ancillas','factory_physical_qubits']),'Typed nonnegative counts')
 require(sum(r[k] for k in ['stored_data','active_data','source_ancillas'])==total,'Disjoint exhaustive source categories')
 require(r['active_data']+r['source_ancillas']>=private,'Active/private workspace cannot be silently moved to storage')
 require(r['complete_physical_qubits']>=capacity(r['stored_data'])['physical_memory_only']+r['factory_physical_qubits'],'All memory and factory charges')
 require(r['complete_physical_qubits']<=r['physical_cap'],'Physical cap')
 require(r['complete_failure_upper']<=r['allocated_failure_upper'],'Complete error allocation')
def prepare():
 require(not OUT.exists(),'Fresh output');p=pins();require(sum((ROOT/x).stat().st_size for x in p)<16*2**20,'16MiB corpus')
 OUT.mkdir(parents=True)
 write('protocol.json',{'item':'H09','corpus_sha256':p,'candidate':{'n':144,'k':12,'nominal_distance':12,'check_qubits':144,'connectivity_degree':6,'syndrome_CNOT_layers':7,'circuit_distance_upper':10},
  'corpus':{'original_cases':['B4x12','B8x52'],'capacities':[0,1,11,12,13,550141,4460479],'admission_negative_controls':8},
  'assumptions':['Native-private peak is not a live-storage measurement.','A memory block is not a universal gate/factory/interface implementation.','Finite unavailable facts remain null.'],
  'acceptance':['Exact original H17 demands and error fractions reconcile.','Capacity boundaries and unused slots are checked.','Both actual null allocation records are rejected; eight controls reject unknowns, overlap/coverage and uncharged obligations.'],
  'budgets':{'CPU_seconds':30,'script_wall_seconds':60,'input_bytes':16*2**20,'output_bytes':4*2**20,'owned_files':16},
  'stop':'One finite memory candidate and one original allocation record at each B4/B8 current cap. Missing liveness, cap or conversion closes integration.',
  'new_finance_paths':0,'timing_benchmarks':0,'global_fixture_credit':0,'source_adoption':False})
 print(json.dumps({'prepared':True,'protocol_sha256':sha(OUT/'protocol.json')}))
def run(expected):
 require(not (OUT/'ATTEMPT.json').exists(),'One invocation');p=json.loads((OUT/'protocol.json').read_text());require(sha(OUT/'protocol.json')==expected and pins()==p['corpus_sha256'],'Frozen protocol/input SHA')
 write('ATTEMPT.json',{'science_invocations':1,'finance_samples':0});write('FAILED_UNSEALED.json',{'passed':False,'provisional':True})
 try:
  original=json.loads((ROOT/(H17+'summary.json')).read_text());require(original['passed'] and original['physical_qubit_cap'] is None and original['architecture_rows']==0,'Original null physical cap')
  expected_rows=[('B4x12',550141,195017,511911060861915,1182602002711185),('B8x52',4460479,1516959,4195204814583315,9691531767803025)]
  allocations=[]
  for row,exp in zip(original['case_rows'],expected_rows):
   name,total,private,tcount,gcount=exp
   require((row['case'],row['logical_qubits'],row['max_simultaneous_native_private_qubits'],row['consumed_T_states'],row['primitive_elementary_gate_count'])==exp,'Original demands')
   f=row['failure_requirements'];require(Q(*f['required_error_per_consumed_T_state_exact'])==Q(1,1000*tcount) and Q(*f['required_data_error_per_elementary_logical_gate_exact'])==Q(1,1000*gcount),'Original exact error targets')
   require(sum(Q(*v) for v in f['allocation_exact'].values())==Q(3,1000) and f['idle_or_code_cycle_opportunity_count'] is None and not f['known_gate_union_targets_cover_idle_and_feedback'],'Physical unknowns not filled')
   record={k:None for k in ['stored_data','active_data','source_ancillas','factory_physical_qubits','physical_cap','conversion_cost','conversion_error','actual_topology','memory_idle_budget','complete_failure_upper','allocated_failure_upper','complete_physical_qubits']}
   try:admit(record,total,private)
   except ValueError as e:record.update(case=name,admitted=False,reason=str(e),logical_total=total,native_private_peak=private)
   else:raise ValueError('Actual missing allocation admitted')
   allocations.append(record)
  require(len(original['case_rows'])==2,'Fixed two cases')
  rows=[capacity(m) for m in p['corpus']['capacities']]
  for r in rows:
   m=r['declared_stored_logical'];b=r['blocks'];require(12*b>=m and (b==0 or 12*(b-1)<m) and 0<=r['unused_logical_slots']<12,'Exact minimal block capacity')
  synthetic={'stored_data':12,'active_data':4,'source_ancillas':4,'factory_physical_qubits':5,'physical_cap':1000,'conversion_cost':1,'conversion_error':Q(0),'actual_topology':'synthetic','memory_idle_budget':1,'complete_failure_upper':Q(0),'allocated_failure_upper':Q(3,1000),'complete_physical_qubits':400}
  admit(synthetic,20,8)
  edits=[('stored_data',None),('physical_cap',None),('conversion_cost',None),('actual_topology',None),('factory_physical_qubits',None),('complete_failure_upper',Q(1)),('active_data',0),('complete_physical_qubits',288)]
  controls=[]
  for key,value in edits:
   bad=synthetic.copy();bad[key]=value
   try:admit(bad,20,8)
   except ValueError as e:controls.append({'field':key,'rejected':True,'reason':str(e)})
   else:raise ValueError('Escaped negative admission control')
  write('allocation_records.json',allocations);write('capacity_only_rows.json',rows);write('negative_controls.json',controls)
  require(pins()==p['corpus_sha256'],'Fresh final SHA');guard()
  write('summary.json',{'passed':True,'bounded_step_completed':True,'candidate_count':1,'original_allocation_records':2,'capacity_checks':7,'negative_controls':8,'synthetic_positive_guard_cases':1,
   'actual_admitted_architectures':0,'physical_integration':'CLOSED_MISSING_LIVENESS_CAP_AND_CONVERSION','storage_savings_claimed':False,'quantum_advantage':False,'new_fixture_credit':0,'source_adoption':False,'entire_limitation_solved':False})
  owned=[x for x in OUT.iterdir() if x.is_file() and x.name!='FAILED_UNSEALED.json'];require(len(owned)+2<=16 and sum(x.stat().st_size for x in owned)+65536<4*2**20,'Output caps')
  write('manifest.json',{'files':{x.name:sha(x) for x in owned},'input_pins':p['corpus_sha256']});(OUT/'FAILED_UNSEALED.json').unlink()
  print(json.dumps({'passed':True,'manifest_sha256':sha(OUT/'manifest.json'),'physical_integration':False}))
 except BaseException as error:
  (OUT/'FAILED_UNSEALED.json').write_text(json.dumps({'passed':False,'error':str(error),'failure_overrides_partial':True})+'\n');raise
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['prepare','run']);ap.add_argument('--protocol-sha256');args=ap.parse_args()
 if args.mode=='prepare':prepare()
 else:run(args.protocol_sha256)
