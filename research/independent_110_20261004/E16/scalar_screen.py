"""Frozen scalar population proof/accounting check; no financial source imports."""
import time
CPU_START=time.process_time()
import argparse
import hashlib
import importlib.util
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path
WALL_START=time.monotonic()
ROOT=Path(__file__).resolve().parents[3]
DOC=ROOT/'docs/independent_110_20261004/E16'
OUT=ROOT/'results/independent_110_20261004/E16/scalar_run001'
FREEZE=DOC/'FREEZE.json'
PATHS=[
 'docs/independent_110_20261004/E16/PROTOCOL.json',
 'docs/independent_110_20261004/E16/SCALAR_PROOF.md',
 'research/independent_110_20261004/E16/scalar_screen.py',
 'research/independent_110_20261004/E16/interval_helper.py',
 'research/independent_110_20261004/E16/author_helper.py',
 'research/independent_110_20261004/F23/screen_covariance_compression.py',
 'docs/independent_110_20261004/E16/primary_sources/Hamoudi_2108_12172v1.pdf',
 'docs/independent_110_20261004/E09/primary_sources/BHMT_quant_ph_0005055v1.pdf',
 'research/compound_feasibility/model.py',
 'research/controlled_source_completion/finance.py',
 'docs/controlled_residual_feasibility/DERIVATION.md',
 'docs/limitation_audit_20261001/ESTIMATION_AND_CERTIFICATION.md',
 'docs/limitation_audit_20261001/implementation_plan/roadmap.json',
 'docs/independent_110_20261004/inventory_run001/WORK_LIST.txt']
def guard(admission=False):
 if time.process_time()-CPU_START>(60 if admission else 90) or time.monotonic()-WALL_START>180: raise RuntimeError('Fixed E16 administrative budget exhausted')
def sha(p):
 guard(); b=p.read_bytes(); guard(); return hashlib.sha256(b).hexdigest()
def read(p):
 guard(); obj=json.loads(p.read_text(encoding='utf-8-sig')); guard(); return obj
def pair(x): return [x.numerator,x.denominator]
def pinned(paths):
 ans={}; total=0
 if len(paths)>20: raise RuntimeError('Input file cap')
 for p in paths:
  guard(); n=(ROOT/p).stat().st_size; total+=n
  if n>2097152 or total>8388608: raise RuntimeError('Input byte cap')
  ans[p]={'sha256':sha(ROOT/p),'bytes':n}
 return ans
def runtime():
 return {str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in dict.fromkeys([Path(sys.executable),Path(sys._base_executable)])}
def verify(f):
 assert f['inputs']==pinned(PATHS) and f['selected_runtime']==runtime()
def write(name,obj,emergency=False):
 if not emergency: guard()
 p=OUT/name
 data=(json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()
 existing=list(OUT.glob('*'))
 if len(existing)+1>16 or sum(x.stat().st_size for x in existing)+len(data)+16384>2097152: raise RuntimeError('Output cap')
 with p.open('xb') as h: h.write(data)
 if not emergency: guard()
def check():
 spec=importlib.util.spec_from_file_location('e16_owned',ROOT/'research/independent_110_20261004/E16/interval_helper.py')
 mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
 I=mod.I
 def exp(x):
  guard(); x=Q(x)
  if x<0: return I(1)/exp(-x)
  pieces=1
  while x>1: x/=2; pieces*=2; guard()
  a=mod.exp_positive(x)
  while pieces>1: a=a.square(); pieces//=2; guard()
  return a
 pi=mod.pi_interval(); assert pi.hi<Q(22,7)
 p4=exp(Q(6,25))*10**8
 moment=exp(Q(1,25))*10000
 D=exp(Q(79,50))*20; assert D.hi<100
 assert (D*5).hi<500
 t8=exp(-32)*2
 q=Q(23,121)
 def tail(r): return sum((Q(math.comb(r,k))*q**k*(1-q)**(r-k) for k in range((r+1)//2,r+1)),Q(0))
 r=next(k for k in range(1,32,2) if tail(k)<=Q(1,100)); assert r==11
 # Exact coefficients of density exponent after multiplying tilted density and likelihood.
 sigma=Q(1,5); v=sigma*sigma
 assert (-sigma*sigma/2+v/2)==0 and sigma-sigma==0
 orders=[]
 for j in (0,1,2,4):
  assert -j*v/2+j*j*v/2==(j*j-j)*v/2
  orders.append(j)
 # Positive factorization of the p4 tail inequality, coefficient-by-coefficient.
 a=Q(4,3); b=Q(8,3); c=Q(16,3)
 assert b-2*a==0 and c-2*a*b+a*a==0
 assert -2*a*c+a*a*b==-Q(256,27) and a*a*c==Q(256,27)
 rows=[]; negatives=[]
 for eps,B in ((Q(1,100),2048),(Q(1,1000),4096)):
  guard(); raw_tail=p4*Q(27,256*B**3)
  assert raw_tail.hi<=eps/4
  wrong=p4*Q(27,256*(B//2)**3); assert wrong.lo>eps/4
  negatives.append({'kind':'fixed_half_cap_fails','epsilon_exact':pair(eps),'cap':B//2,'tail_bound':wrong.pair(),'rejected':True})
  grid=(D*Q(1,2**21))
  bridges={'capped':t8*B+grid,'quantile':exp(-Q(1521,50))*100+grid,'weighted':t8*100+I(Q(20,2**21))}
  for kind,support in (('capped',B),('quantile',500),('weighted',100)):
   guard(); coupling=bridges[kind]; arithmetic=eps/64; loading=eps/64
   assert coupling.hi+arithmetic+loading<=eps/4
   coarse=Q(20 if kind=='weighted' else 100,2048)
   assert coarse>eps/4
   negatives.append({'kind':'coarse_grid_budget_fails','construction':kind,'epsilon_exact':pair(eps),'diagnostic_radius_exact':pair(coarse),'rejected':True})
   base={'construction':kind,'epsilon_exact':pair(eps),'support_exact':[support,1], 'continuous_second_moment_upper':(I(10000) if kind=='weighted' else moment).pair(), 'finite_coupling_upper':coupling.pair(), 'tail_bias_upper':(raw_tail if kind=='capped' else I(0)).pair(), 'required_arithmetic_error_exact':pair(arithmetic),'required_loader_TV_exact':pair(loading/support), 'implemented_arithmetic_error':None,'implemented_loader_TV':None,'exact_Gaussian_cells':1<<24,'full_financial_error_certified':False,'complete_work':None,'strict_complete_improvement':None,'physical_time':None}
   if kind=='quantile':
    root=moment.sqrt()+grid+arithmetic
    actual_m2=root.square()+support*loading
    assert actual_m2.hi<104**2
    n=math.ceil(Q(104*5)/(eps/2))
    assert Q(104*5,n)<=eps/2 and n>=5
    base.update({'finite_moment_with_required_interfaces_upper':actual_m2.pair(),'theorem_n':n,'quantile_calls':None,'source_forward_calls':None,'source_inverse_calls':None,'comparison_calls':None,'rotation_calls':None,'centering_calls':None,'controller_work':None,'readout':None,'status':'CONDITIONAL_FINITE_QUANTILE_PRIMITIVES'})
   else:
    M=2
    while M<=1<<32:
     guard(); err=(pi/I(M)+pi.square()/I(M*M))*support+eps/64
     if err.hi<=eps/2: break
     M*=2
    assert M<=1<<32
    total=raw_tail.hi if kind=='capped' else Q(0)
    assert total+coupling.hi+arithmetic+loading+err.hi<=eps
    bits=M.bit_length()-1
    base.update({'M':M,'independent_shots':r,'estimator_including_readout_upper':err.pair(),'source_forward_calls':r*M,'source_inverse_calls':r*(M-1),'each_reflection_calls':r*(M-1),'IQFT_H':r*bits,'IQFT_controlled_phases':r*bits*(bits-1)//2,'measured_bits':r*bits,'quantile_calls':0,'centering_calls':0,'readout_allowance_exact':pair(eps/64),'classical_controller_cost':None,'status':'CONDITIONAL_LOADING_ARITHMETIC_SYNTHESIS'})
   base['coherent_preparation_per_call']=None
   base['payoff_and_likelihood_per_call']=None
   base['output_rotation_and_cleanup_per_call']=None
   base['approximate_loading_and_arithmetic_budget_pass_if_interfaces_met']=True
   rows.append(base)
 return {'rows':rows,'negative_controls':negatives,'algebra_orders':orders,'counts':{'candidate_rows':6,'negative_controls':8,'moment_orders':4,'density_coefficient_identities':2,'cap_factor_coefficients':4},'exact_majority_failure_upper':pair(tail(r)),'selected_repetitions':r,'moment_bound':moment.pair(),'weighted_support':100,'pi_interval':pi.pair()}
def main():
 parser=argparse.ArgumentParser(); parser.add_argument('mode',choices=['freeze','run']);parser.add_argument('--freeze-sha256');args=parser.parse_args()
 if args.mode=='freeze':
  if FREEZE.exists(): raise RuntimeError('Freeze already exists')
  DOC.mkdir(parents=True,exist_ok=True)
  f={'schema':'E16-author-freeze-v1','inputs':pinned(PATHS),'selected_runtime':runtime(),'scientific_functions_executed':False}
  with FREEZE.open('x',encoding='utf-8',newline='\n') as h: json.dump(f,h,indent=2,sort_keys=True);h.write('\n')
  print(json.dumps({'freeze_sha256':sha(FREEZE),'inputs':len(PATHS),'input_bytes':sum(x['bytes'] for x in f['inputs'].values())}));return
 if not sys.flags.isolated or not sys.flags.no_site or not sys.dont_write_bytecode: raise RuntimeError('Required isolated flags absent')
 if OUT.exists(): raise RuntimeError('Fresh output required; no retry of failed receipt')
 OUT.mkdir(parents=True)
 marker=OUT/'FAILED_UNSEALED.json'
 try:
  write(marker.name,{'state':'UNSEALED','completed':False,'budget_censored':None},emergency=True)
  if sha(FREEZE)!=args.freeze_sha256: raise RuntimeError('Freeze SHA mismatch')
  f=read(FREEZE);verify(f);guard(admission=True)
  write('protocol.json',read(DOC/'PROTOCOL.json'));write('run_started.json',{'freeze_sha256':args.freeze_sha256,'science':'symbolic_population_interval_accounting_only'})
  checked=check();write('scalar_accounting.json',checked)
  write('certificate.json',{'passed':True,'completed':True,'budget_censored':False,'bounded_initial_scope_complete':True,'finite_bias_and_moment_math_pass':True,'full_financial_error_certified':False,'conditional_interfaces':['exact/TV-certified Gaussian state preparation','all-input payoff/likelihood arithmetic and cleanup','rotation synthesis','finite quantile primitive calibration','classical analytic CDF enclosure and complete comparison'],'advancement':'NONE_RETAIN_CAPPED_SUPPORT_AND_ANALYTIC_COMPARATOR','complete_work':None,'source_adoption':False,'new_samples':0,'new_global_fixture_credit':0,'new_gate_replay_credit':0,'quantum_advantage':False})
  write('comparison.json',{'scalar_classical_comparator':'Analytic lognormal call with the same caps/tilt available','classical_CDF_enclosure':None,'matched_timing':False,'candidate_complete_costs':[None]*6,'strict_complete_work_improvement':None,'original_B4_B8_and_parity_residual_unchanged':True})
  verify(f);guard()
  members={p.relative_to(ROOT).as_posix():sha(p) for p in OUT.iterdir() if p.is_file() and p!=marker}
  mf={'passed':True,'completed':True,'budget_censored':False,'freeze_sha256':args.freeze_sha256,'frozen_inputs':f['inputs'],'selected_runtime':f['selected_runtime'],'files':members,'manifest_self_hash_excluded':True,'failure_marker_authoritative':True,'new_global_fixture_credit':0,'quantum_advantage':False}
  data=(json.dumps(mf,indent=2,sort_keys=True)+'\n').encode()
  if len(data)>49152 or sum(p.stat().st_size for p in OUT.iterdir())+len(data)+16384>2097152: raise RuntimeError('Manifest reserve cap')
  write('manifest.json',mf);guard()
  assert {p.name for p in OUT.iterdir()}=={'protocol.json','run_started.json','scalar_accounting.json','certificate.json','comparison.json','manifest.json',marker.name}
  marker.unlink();guard()
  print(json.dumps({'passed':True,'candidate_rows':6,'manifest_sha256':sha(OUT/'manifest.json')}))
 except BaseException as err:
  if not marker.exists():
   try: write(marker.name,{'state':'FAILED_UNSEALED','completed':False,'budget_censored':None},emergency=True)
   except BaseException: pass
  try: write('retained_error.json',{'type':type(err).__name__,'error':str(err)[:4000],'completed':False,'budget_censored':isinstance(err,RuntimeError) and 'budget' in str(err).lower()},emergency=True)
  except BaseException: pass
  raise
if __name__=='__main__':main()
