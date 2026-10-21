"""E09 theorem-backed support fallback; unknown-variance finite interface held."""
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
DOC=ROOT/'docs/independent_110_20261004/E09'
OUT=ROOT/'results/independent_110_20261004/E09/controller_run001'
FREEZE=DOC/'FREEZE.json'
M=4096
ALPHA=Q(1,100)
ERROR=Q(1,1024)
READOUT=Q(1,2**24)
PATHS=[
 'docs/independent_110_20261004/E09/PROTOCOL.json','docs/independent_110_20261004/E09/THEOREM_AND_CONTROLLER.md',
 'research/independent_110_20261004/E09/controller_screen.py','research/independent_110_20261004/E09/readout_interval.py',
 'docs/independent_110_20261004/E09/primary_sources/Kothari_ODonnell_2208_07544v1.pdf',
 'docs/independent_110_20261004/E09/primary_sources/BHMT_quant_ph_0005055v1.pdf',
 'docs/independent_110_20261004/inventory_run001/WORK_LIST.txt',
 'docs/limitation_audit_20261001/implementation_plan/roadmap.json',
 'docs/limitation_audit_20261001/ESTIMATION_AND_CERTIFICATION.md',
 'research/controlled_source_completion/modern_mean.py','docs/controlled_source_completion/DERIVATION.md',
 'research/independent_110_20261004/F23/screen_covariance_compression.py',
 'research/independent_110_20261004/E09/author_readout_helper.py',
 'docs/independent_110_20261004/E09/PREPARATION_FAILURE_run001.json']


def guard(admission=False):
 if time.process_time()-CPU_START>(60 if admission else 90) or time.monotonic()-WALL_START>180:
  raise RuntimeError('Fixed E09 administrative CPU/wall budget exhausted')


def sha(p):
 guard(); value=hashlib.sha256(p.read_bytes()).hexdigest(); guard(); return value


def read(p):
 guard(); value=json.loads(p.read_text(encoding='utf-8-sig')); guard(); return value


def pair(q): return [q.numerator,q.denominator]


def write(p,v,emergency=False):
 payload=(json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
 if emergency: assert len(payload)<=16384
 else:
  guard(); files=[x for x in OUT.iterdir() if x.is_file()]
  assert len(files)+1<=16 and sum(x.stat().st_size for x in files)+len(payload)+16384<=2097152
 with p.open('xb') as handle: handle.write(payload)
 if not emergency: guard()


def verify(f):
 assert set(f['inputs'])==set(PATHS)
 for name,pin in f['inputs'].items(): assert (ROOT/name).stat().st_size==pin['bytes'] and sha(ROOT/name)==pin['sha256'],name
 for name,pin in f['selected_runtime'].items(): assert sha(Path(name))==pin['sha256']


def freeze():
 assert not FREEZE.exists() and not OUT.exists() and len(PATHS)<=20
 pins={}
 for name in PATHS:
  p=ROOT/name; assert p.stat().st_size<=2097152
  pins[name]={'sha256':sha(p),'bytes':p.stat().st_size}
 assert sum(x['bytes'] for x in pins.values())<=8388608
 runtime={str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(set([Path(sys.executable),Path(sys.base_prefix)/'python.exe']),key=str)}
 with FREEZE.open('x',encoding='utf-8') as handle:
  json.dump({'inputs':pins,'selected_runtime':runtime,'science_started':False,'runtime_scope':'Selected launcher/base interpreter only'},handle,indent=2,sort_keys=True); handle.write('\n')
 print(json.dumps({'freeze_sha256':sha(FREEZE),'inputs':len(pins),'bytes':sum(x['bytes'] for x in pins.values())}))


def tail(r,q):
 return sum((Q(math.comb(r,j))*q**j*(1-q)**(r-j) for j in range(r//2+1,r+1)),Q(0))


def decoder(helper,k):
 if type(k) is not int or not 0<=k<M: raise ValueError('Invalid QPE outcome')
 folded=min(k,M-k)
 enclosure=helper.sin_ratio(Q(folded,M)).square()
 midpoint=(enclosure.lo+enclosure.hi)/2
 estimate=Q(round(midpoint*(1<<24)),1<<24)
 assert max(abs(estimate-enclosure.lo),abs(estimate-enclosure.hi))<=READOUT
 return estimate,enclosure


def controller(helper,measurements,r):
 values=list(measurements)
 if len(values)!=r or any(type(k) is not int or not 0<=k<M for k in values): raise ValueError('Invalid fixed-shot callback')
 selected=sorted(min(k,M-k) for k in values)[r//2]
 return decoder(helper,selected)[0]


def check():
 spec=importlib.util.spec_from_file_location('e09_owned_readout',ROOT/'research/independent_110_20261004/E09/readout_interval.py')
 helper=importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
 helper.guard=guard; helper.PI=helper.pi_interval()
 assert helper.PI.hi<Q(22,7)
 worst=Q(22,7)/M+Q(22,7)**2/M**2
 assert worst+READOUT<=ERROR
 q=Q(23,121)
 admitted=[r for r in range(1,32,2) if tail(r,q)<=ALPHA]
 assert admitted
 r=admitted[0]
 assert all(tail(j,q)>ALPHA for j in range(1,r,2))
 for k in range(M):
  guard(); decoder(helper,k)
 for values in ([0]*(r-1),[M]*r,[True]*r):
  try: controller(helper,values,r)
  except ValueError: pass
  else: raise AssertionError('Invalid callback accepted')
 assert controller(helper,[0]*r,r)==0
 assert controller(helper,[M//2]*r,r)==1
 assert controller(helper,[M//4]*r,r)==Q(1,2)
 rows=[]
 quantile=[]
 for b,p in ((1,Q(1,2)),(8,Q(1,256)),(16,Q(1,65536))):
  guard(); assert p==Q(1,2**b)
  mean,variance=p,p*(1-p)
  assert variance<=Q(1,4)
  ccx=0 if b==1 else 2*b-3
  cx=1 if b==1 else 0
  rows.append({'law_probability_exact':pair(p),'mean_exact':pair(mean),'variance_exact':pair(variance),
   'fixture_probability_used_by_controller':False,'uniform_source_bits':b,'F_clean_CCX':ccx,'F_clean_CX':cx,'F_clean_X':2*b,
   'source_forward_calls':r*M,'source_inverse_calls':r*(M-1),'initial_shots':r,'each_reflection_calls':r*(M-1),
   'initial_QPE_H':r*12,'IQFT_H':r*12,'IQFT_controlled_phase_applications':r*12*11//2,'measured_QPE_bits':r*12,
   'source_F_CCX_directions':r*(2*M-1)*ccx,'fallback_quantile_calls':0,'fallback_centering_calls':0,
   'unknown_variance_quantile_calls':None,'unknown_variance_full_cost':None,'physical_cost':None})
  for m in (0,1):
   nonzero=p if m==0 else 1-p
   assert nonzero>=Q(1,512**2)
   quantile.append({'p_exact':pair(p),'centering_sample':m,'centered_nonzero_probability_exact':pair(nonzero),
    'n_diagnostic':512,'B1_first_tail_promise_pass':True,'B1_strict_tail_probability_exact':[0,1],
    'B0_requires_unknown_C_at_least_exact':pair(nonzero*512**2),'C_value':None,'n0':None,
    'centering_samples_in_unknown_variant':1,'quantile_primitive_total_calls':None,'selected_cap':None})
 return {'M':M,'repetitions':r,'worst_probability_error_upper_exact':pair(worst),'readout_allowance_exact':pair(READOUT),
         'absolute_error_upper_exact':pair(worst+READOUT),'majority_failure_upper_exact':pair(tail(r,q)),
         'single_shot_failure_upper_exact':pair(q),'rows':rows,'quantile_promise_diagnostics':quantile,
         'counts':{'decoder_outcomes':M,'invalid_callbacks':3,'controller_boundaries':3,'exact_law_rows':3,'centered_quantile_rows':6}}


def run(expected):
 assert sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
 if OUT.exists(): raise RuntimeError('Fresh E09 receipt required; no retries')
 OUT.mkdir(parents=True); marker=OUT/'FAILED_UNSEALED.json'
 write(marker,{'passed':False,'completed':False,'decision':'UNSEALED_FROM_START'},emergency=True)
 try:
  assert sha(FREEZE)==expected; frozen=read(FREEZE); verify(frozen); guard(admission=True)
  write(OUT/'protocol.json',read(DOC/'PROTOCOL.json'))
  write(OUT/'run_started.json',{'freeze_sha256':expected,'finance_draws':0,'stopping_rule_revisions':0})
  results=check(); write(OUT/'controller_accounting.json',results)
  write(OUT/'certificate.json',{'passed':True,'completed':True,'budget_censored':False,
   'E09_bounded_initial_audit_complete':True,'unknown_variance_finance_branch':'CONDITIONAL_FINITE_CONSTANTS_AND_REDUCTION_UNRESOLVED',
   'unknown_variance_controller_implemented':False,'support_fallback_absolute_error_certified':True,
   'support_fallback_scope':'Ideal exact coherent toy source and independent QAE shots; emitted gates/synthesis/physical delivery unproved',
   'unknown_variance_cost':None,'complete_financial_cost':None,'stopping_rule_revisions':0,
   'new_samples':0,'source_adoption':False,'new_global_fixture_credit':0,'new_gate_replay_credit':0,'quantum_advantage':False})
  write(OUT/'comparison.json',{'support_fallback_query_totals':results['rows'],'unknown_variance_query_totals':None,
   'strict_complete_work_improvement':None,'matched_timing':False,'finance_admission':False})
  verify(frozen)
  files={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in OUT.iterdir() if p.is_file() and p!=marker}
  write(OUT/'manifest.json',{'passed':True,'completed':True,'budget_censored':False,'files':files,'frozen_inputs':frozen['inputs'],
   'selected_runtime':frozen['selected_runtime'],'freeze_sha256':expected,'manifest_self_hash_excluded':True,
   'failure_marker_authoritative':True,'new_global_fixture_credit':0,'quantum_advantage':False})
  assert set(p.name for p in OUT.iterdir())=={'FAILED_UNSEALED.json','protocol.json','run_started.json','controller_accounting.json','certificate.json','comparison.json','manifest.json'}
  guard(); marker.unlink(); print(json.dumps({'passed':True,'repetitions':results['repetitions'],'manifest_sha256':sha(OUT/'manifest.json')}))
 except BaseException as exc:
  payload=(json.dumps({'passed':False,'completed':False,'decision':'FAILED_UNSEALED','type':type(exc).__name__,'message':str(exc)[:2048],
                      'budget_censored':'budget' in str(exc).lower(),'failure_overrides_partial_pass':True,'new_global_fixture_credit':0},indent=2)+'\n').encode()
  assert len(payload)<=16384; marker.write_bytes(payload); raise


if __name__=='__main__':
 parser=argparse.ArgumentParser(); parser.add_argument('mode',choices=('freeze','run')); parser.add_argument('--freeze-sha256'); args=parser.parse_args()
 if args.mode=='freeze': freeze()
 else:
  if not args.freeze_sha256: parser.error('run requires --freeze-sha256')
  run(args.freeze_sha256)
