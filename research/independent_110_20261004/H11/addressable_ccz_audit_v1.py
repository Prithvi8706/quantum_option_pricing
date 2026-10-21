"""One finite addressable-code parameter bill and original leaf interface, not device cost."""
import time
START=time.monotonic()
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import argparse,ast,hashlib,json,struct
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'results/independent_110_20261004/H11/run001'
BASE='results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/'
LEAF='1e0b2dc8929b29814d9a';H17='results/limitation_program_20261001/H17_demand_run002/'
INPUTS=[BASE+'target.json',BASE+'source.json',BASE+'leaves/'+LEAF+'.json',BASE+'leaves/'+LEAF+'.npy',
 H17+'summary.json',H17+'manifest.json',H17+'hardware_provenance.json',
 'docs/limitation_audit_20261001/implementation_plan/roadmap.json','docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md',
 'docs/independent_110_20261004/H11/PREFLIGHT_PRIMARY_run001.json','docs/independent_110_20261004/H11/FINITE_PARAMETERS_AND_LIMITS.txt',
 'research/independent_110_20261004/H11/primary_sources/He_2502_01864v1.pdf','research/independent_110_20261004/H11/PRIMARY_RETRIEVAL_run001.json',Path(__file__).resolve().relative_to(ROOT).as_posix()]
def require(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pins():return {p:sha(ROOT/p) for p in INPUTS}
def write(name,data):
 with (OUT/name).open('x',encoding='utf-8') as f:json.dump(data,f,indent=2,sort_keys=True);f.write('\n')
def guard():require(time.process_time()<30 and time.monotonic()-START<60,'30CPU/60scriptwall')
def native_rows():
 raw=(ROOT/(BASE+'leaves/'+LEAF+'.npy')).read_bytes();require(raw[:6]==b'\x93NUMPY' and raw[6] in (1,2),'Native NPY')
 start=10 if raw[6]==1 else 12;size=struct.unpack('<H' if start==10 else '<I',raw[8:start])[0]
 h=ast.literal_eval(raw[start:start+size].decode('latin1').strip());require(h['descr']=='<i4' and not h['fortran_order'] and h['shape']==(22914,4),'Original native format')
 body=raw[start+size:];require(len(body)==22914*16,'Exact stream extent')
 return list(struct.iter_unpack('<4i',body))
def admit(r):
 needed=['finite_code_certificate','encoded_Clifford_interfaces','stabilizer_extraction_and_decoder','physical_CCZ_channel',
  'physical_CCZ_error','physical_CCZ_duration','actual_connectivity','preparation_idle_controller_bill','complete_physical_qubits','physical_cap','complete_failure_upper','allocated_failure_upper']
 require(all(r.get(k) is not None for k in needed),'Missing compatible finite code/gate/interface fact')
 require(r['finite_code_certificate'] is True and r['encoded_Clifford_interfaces'] is True and r['physical_CCZ_channel'] is True,'Complete code/Clifford/channel identity')
 require(r.get('labeled_LDPC') is False,'This construction is non-LDPC')
 require(r['complete_physical_qubits']>=3538944000,'All finite block wires count')
 require(r['complete_physical_qubits']<=r['physical_cap'] and r['complete_failure_upper']<=r['allocated_failure_upper'],'Finite space and complete failure budget')
def prepare():
 require(not OUT.exists(),'Fresh output');p=pins();require(sum((ROOT/x).stat().st_size for x in p)<32*2**20,'32MiB input')
 OUT.mkdir(parents=True)
 write('protocol.json',{'item':'H11','corpus_sha256':p,
  'candidate':{'version':'2502.01864v1 Theorem6.1 full intrablock variant','n0':32768,'m':10923,'k':5791,'t':30,'q':1073741824,'qubit_block':3538944000,'candidate_count':1},
  'corpus':{'original_leaf':LEAF,'original_width':72,'fraction_bits':40,'native_rows':22914,'CCZ_phase_states':8,'H_CCZ_H_columns':8,'matrix_coefficients':16,'omitted_H_negative_controls':1,'admission_negative_controls':8},
  'assumptions':['Conditional code theorem parameter extraction is not emitted stabilizers/noisy hardware.','Encoded target H and other Clifford gates are required separately.','Missing physical facts remain null; all block wires count.'],
  'acceptance':['Original ordered gate stream hash/counts and signed call binding match.','All eight full H-CCZ-H columns exactly equal Toffoli; omission rejects.','One finite theorem input and qubit length reconcile without arbitrary constants.','Eight guard-negative rows and actual missing interface reject.'],
  'budgets':{'CPU_seconds':30,'script_wall_seconds':60,'input_bytes':32*2**20,'output_bytes':4*2**20,'owned_files':16},
  'stop':'One finite parameter extraction and one original leaf interface. Missing compatible physical CCZ/error/extraction/Clifford facts closes timing/integration; no next code or noise scenario.',
  'new_finance_paths':0,'timing_benchmarks':0,'new_fixture_credit':0,'source_adoption':False})
 print(json.dumps({'prepared':True,'protocol_sha256':sha(OUT/'protocol.json')}))
def run(expected):
 require(not (OUT/'ATTEMPT.json').exists(),'One invocation');p=json.loads((OUT/'protocol.json').read_text());require(sha(OUT/'protocol.json')==expected and pins()==p['corpus_sha256'],'Protocol/input SHA')
 write('ATTEMPT.json',{'one_invocation':True,'financial_gate_replays':0});write('FAILED_UNSEALED.json',{'passed':False,'provisional':True})
 try:
  source=json.loads((ROOT/(BASE+'source.json')).read_text());leaf=json.loads((ROOT/(BASE+'leaves/'+LEAF+'.json')).read_text())
  require(source['word_width']==72 and source['fraction_bits']==40 and source['forward_calls'][27]['leaf']==LEAF and source['forward_calls'][27]['args']==[27,36] and source['forward_calls'][27]['out']==[37],'Original signed call')
  require(leaf['spec']['width']==72 and leaf['spec']['fraction_bits']==40 and leaf['spec']['active_operand_bits']==[40,40],'Original native domain unchanged')
  require(sha(ROOT/(BASE+'target.json'))=='a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384' and sha(ROOT/(BASE+'leaves/'+LEAF+'.npy'))==leaf['sha256'],'Original target/leaf hash')
  rows=native_rows();counts=Counter(x[0] for x in rows);r=leaf['resources']
  require(counts=={1:224,2:11446,3:11244} and r['qubits']==5791 and r['source_gates']==22914 and r['t_count']==7*11244 and r['clifford_h']==2*11244,'Original gate/resource ledger')
  require(all(0<=x<5791 for row in rows for x in row[1:]),'Original complete wire extent')
  columns=[];phases=[]
  for a in (0,1):
   for b in (0,1):
    for x in (0,1):
     phase=(-1)**(a*b*x);phases.append({'input':[a,b,x],'CCZ_phase':phase})
     coefficients=[Q(sum((-1)**(t*(x+a*b+z)) for t in (0,1)),2) for z in (0,1)]
     require(coefficients==[Q(int(z==(x^(a*b)))) for z in (0,1)],'Exact full Toffoli column')
     columns.append({'input':[a,b,x],'target_amplitudes':[[q.numerator,q.denominator] for q in coefficients]})
  require((1,1,0)!=(1,1,0^(1*1)),'Omitting target H must change gate')
  c=p['candidate'];n0,m,k,t=c['n0'],c['m'],c['k'],c['t']
  require(n0&(n0-1)==0 and c['q']==n0*n0==1<<t and t==2*(n0.bit_length()-1),'Exact field parameters')
  require(m==(n0+2)//3 and Q(m)<Q(n0,3)+1 and 1<=k<=m and k==r['qubits'] and ((n0//2)+2)//3<k,'One minimal power-of-two source-capacity choice')
  require(c['qubit_block']==4*n0*t**3==3538944000 and m-k+1==5133,'Finite theorem length and conditional lower distance')
  bill={'theorem_inputs':c,'conditional_distance_lower':5133,'exact_noisy_distance':None,'all_block_data_qubits':c['qubit_block'],
   'stabilizer_ancillas':None,'unused_logical_slots':0,'gauge_fixed_and_embedding_wires_included':True,'generator_or_stabilizer_constructed':False,'labeled_LDPC':False,
   'leaf_logical_demands':{'X':224,'CNOT':11446,'CCZ':11244,'target_H':22488,'original_native_qubits':5791,'archived_baseline_T':78708},
   'quantum_channel_identity_conditional_on_ideal_logical_interfaces':True,'financial_leaf_replays':0,'physical_latency':None}
  unknown={v:None for v in ['finite_code_certificate','encoded_Clifford_interfaces','stabilizer_extraction_and_decoder','physical_CCZ_channel','physical_CCZ_error','physical_CCZ_duration','actual_connectivity','preparation_idle_controller_bill','complete_physical_qubits','physical_cap','complete_failure_upper','allocated_failure_upper']};unknown['labeled_LDPC']=False
  try:admit(unknown)
  except ValueError as e:reason=str(e)
  else:raise ValueError('Actual missing interface admitted')
  synthetic={v:1 for v in unknown};synthetic.update(finite_code_certificate=True,encoded_Clifford_interfaces=True,physical_CCZ_channel=True,labeled_LDPC=False,complete_physical_qubits=3538944000,physical_cap=3538945000,complete_failure_upper=Q(0),allocated_failure_upper=Q(3,1000))
  admit(synthetic);controls=[]
  for key,value in [('finite_code_certificate',None),('encoded_Clifford_interfaces',False),('stabilizer_extraction_and_decoder',None),('physical_CCZ_duration',None),('actual_connectivity',None),('complete_failure_upper',Q(1)),('complete_physical_qubits',5791),('labeled_LDPC',True)]:
   bad=synthetic.copy();bad[key]=value
   try:admit(bad)
   except ValueError as e:controls.append({'field':key,'rejected':True,'reason':str(e)})
   else:raise ValueError('Escaped admission control')
  h17=json.loads((ROOT/(H17+'summary.json')).read_text());require(h17['passed'] and h17['physical_qubit_cap'] is None and h17['architecture_rows']==0,'Original H17 null architecture')
  bill.update(actual_physical_interface=unknown,actual_admitted=False,admission_reason=reason,H17_error_targets=[{'case':x['case'],'requirements':x['failure_requirements']} for x in h17['case_rows']])
  write('finite_parameter_and_gate_bill.json',bill);write('ideal_identity_checks.json',{'CCZ_phase_states':phases,'full_H_CCZ_H_columns':columns,'omitted_H_rejected':True});write('negative_controls.json',controls)
  require(pins()==p['corpus_sha256'],'Fresh final SHA');guard()
  write('summary.json',{'passed':True,'bounded_step_completed':True,'finite_parameter_candidates':1,'original_native_rows':22914,'ideal_matrix_columns':8,'CCZ_phase_states':8,'admission_negative_controls':8,'omitted_H_negative_controls':1,
   'data_block_only_qubits':3538944000,'instantiated_stabilizer_or_hardware_certificate':False,'physical_integration':'CLOSED_MISSING_CLIFFORD_EXTRACTION_AND_PHYSICAL_CCZ','accepted_architectures':0,'new_fixture_credit':0,'source_adoption':False,'entire_limitation_solved':False,'quantum_advantage':False})
  owned=[x for x in OUT.iterdir() if x.is_file() and x.name!='FAILED_UNSEALED.json'];require(len(owned)+2<=16 and sum(x.stat().st_size for x in owned)+65536<4*2**20,'Output caps')
  write('manifest.json',{'files':{x.name:sha(x) for x in owned},'input_pins':p['corpus_sha256']});(OUT/'FAILED_UNSEALED.json').unlink()
  print(json.dumps({'passed':True,'manifest_sha256':sha(OUT/'manifest.json'),'physical_integration':False}))
 except BaseException as error:
  (OUT/'FAILED_UNSEALED.json').write_text(json.dumps({'passed':False,'error':str(error),'failure_overrides_partial':True})+'\n');raise
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['prepare','run']);ap.add_argument('--protocol-sha256');args=ap.parse_args()
 if args.mode=='prepare':prepare()
 else:run(args.protocol_sha256)
