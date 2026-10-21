"""Exact finite Bayesian amplitude design and proved likelihood wrapper diagnostic."""
import time
CPU_START=time.process_time()
import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path
WALL_START=time.monotonic()
ROOT=Path(__file__).resolve().parents[3]
DOC=ROOT/'docs/independent_110_20261004/E25'
OUT=ROOT/'results/independent_110_20261004/E25/amplitude_run001'
FREEZE=DOC/'FREEZE.json'
PATHS=['docs/independent_110_20261004/E25/PROTOCOL.json','docs/independent_110_20261004/E25/COVERAGE_PROOF.md','research/independent_110_20261004/E25/amplitude_screen.py','research/independent_110_20261004/E25/extract_primary.py','docs/independent_110_20261004/E25/primary_sources/Ramoa_Santos_2412_04394v5.html','docs/independent_110_20261004/E25/primary_sources/Ramoa_Santos_2412_04394v5.txt','docs/independent_110_20261004/E25/primary_sources/Ramoa_Santos_2412_04394v5.pdf','docs/independent_110_20261004/E25/primary_sources/Ramdas_et_al_SAVI_2023.pdf','research/controlled_priority_completion/estimator_bounded.py','research/controlled_priority_completion/estimator_hadamard.py','docs/limitation_audit_20261001/ESTIMATION_AND_CERTIFICATION.md','docs/limitation_audit_20261001/implementation_plan/roadmap.json','docs/independent_110_20261004/inventory_run001/WORK_LIST.txt']
def guard(admission=False):
 if time.process_time()-CPU_START>(60 if admission else 90) or time.monotonic()-WALL_START>180: raise RuntimeError('Fixed E25 administrative budget exhausted')
def sha(p):
 guard();data=p.read_bytes();guard();return hashlib.sha256(data).hexdigest()
def read(p):
 guard();a=json.loads(p.read_text(encoding='utf-8-sig'));guard();return a
def pair(x):return [x.numerator,x.denominator]
def pinned(paths):
 if len(paths)>20:raise RuntimeError('Input file cap')
 ans={};total=0
 for path in paths:
  guard();p=ROOT/path;n=p.stat().st_size;total+=n
  if n>8388608 or total>16777216:raise RuntimeError('Input byte cap')
  ans[path]={'bytes':n,'sha256':sha(p)}
 return ans
def runtime():return {str(p):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in dict.fromkeys((Path(sys.executable),Path(sys._base_executable)))}
def verify(f):assert f['inputs']==pinned(PATHS) and f['selected_runtime']==runtime()
def write(name,obj,emergency=False):
 if not emergency:guard()
 data=(json.dumps(obj,indent=2,sort_keys=True)+'\n').encode();existing=list(OUT.iterdir())
 if len(existing)+1>16 or sum(p.stat().st_size for p in existing)+len(data)+16384>2097152:raise RuntimeError('Output cap')
 with (OUT/name).open('xb') as h:h.write(data)
 if not emergency:guard()
def trim(p):
 while len(p)>1 and p[-1]==0:p.pop()
 return p
def add(p,q):return trim([(p[j] if j<len(p) else Q(0))+(q[j] if j<len(q) else Q(0)) for j in range(max(len(p),len(q)))])
def mul(p,q):
 guard();out=[Q(0)]*(len(p)+len(q)-1)
 for i,a in enumerate(p):
  for j,b in enumerate(q):out[i+j]+=a*b
  guard()
 return trim(out)
def ev(p,a):
 val=Q(0)
 for c in reversed(p):val=val*a+c
 return val
def enclosure(p,l,u):
 lo=hi=Q(0)
 for c in reversed(p):
  vals=(lo*l,lo*u,hi*l,hi*u);lo=min(vals)+c;hi=max(vals)+c
 return lo,hi
def check(protocol):
 prior=[Q(*a) for a in protocol['prior_amplitudes_exact']]
 truths=prior+[Q(*a) for a in protocol['extra_truths_exact']]
 assert len(prior)==13 and len(truths)==18 and len(set(truths))==18
 alpha=Q(1,100);acc=Q(1,64);cells=256
 polys=[mul([Q(0),Q(1)],mul([Q(x) for x in p],[Q(x) for x in p])) for p in ((1,),(3,-4),(5,-20,16),(7,-56,112,-64))]
 assert ev(polys[1],Q(0))==ev(polys[1],Q(3,4))==0
 assert ev(polys[1],Q(1,4))==ev(polys[1],Q(1))==1
 for p in polys:
  assert ev(p,Q(1,2))==Q(1,2)
  for a in truths:assert 0<=ev(p,a)<=1
 nodes={};utility_calls=0;posterior_updates=0;cell_checks=0;containments=0
 def variance(w):
  z=sum(w,Q(0));assert z>0
  mu=sum((x*y for x,y in zip(prior,w)),Q(0))/z
  m2=sum((x*x*y for x,y in zip(prior,w)),Q(0))/z
  ans=m2-mu*mu;assert ans>=0;return ans
 def utility(w,m):
  nonlocal utility_calls
  z=sum(w,Q(0));value=Q(0)
  for d in (0,1):
   guard();utility_calls+=1
   nw=[weight*(ev(polys[m],a) if d else 1-ev(polys[m],a)) for a,weight in zip(prior,w)]
   nz=sum(nw,Q(0))
   if nz: value+=nz/z*variance(nw)
  return value
 def hull(lp,z):
  nonlocal cell_checks,containments
  retained=[]
  for j in range(cells):
   guard();l,u=Q(j,cells),Q(j+1,cells);low,high=enclosure(lp,l,u);cell_checks+=1
   if high>alpha*z:retained.append(j)
  h=(Q(retained[0],cells),Q(retained[-1]+1,cells)) if retained else None
  for a in truths:
   if ev(lp,a)>alpha*z:
    assert h is not None and h[0]<=a<=h[1];containments+=1
  return h,len(retained)
 def build(history,w,lp,ms):
  nonlocal posterior_updates
  guard();z=sum(w,Q(0));assert z>0
  assert all(weight==ev(lp,a)/13 for a,weight in zip(prior,w))
  h,retained=hull(lp,z)
  item={'history':history,'likelihood_coefficients_exact':[pair(c) for c in lp],'mixture_likelihood_exact':pair(z),'hull_exact':None if h is None else [pair(h[0]),pair(h[1])],'retained_cells':retained,'accuracy_stop':h is not None and h[1]-h[0]<=2*acc,'prior_credible_set_is_confidence':False,'controls':ms,'source_forward_calls':sum(m+1 for m in ms),'source_inverse_calls':sum(ms),'each_reflection_calls':sum(ms),'shots_and_readouts':len(ms)}
  nodes[history]=item
  if len(history)==4:return
  if not history:m=0;utilities=None
  else:
   utilities=[utility(w,m) for m in range(4)]
   m=min(range(4),key=lambda j:(utilities[j],j))
  item['next_control']=m;item['utility_exact']=None if utilities is None else [pair(x) for x in utilities]
  children=[]
  for d in (0,1):
   factor=polys[m] if d else add([Q(1)],[-x for x in polys[m]])
   nw=[weight*ev(factor,a) for a,weight in zip(prior,w)]
   posterior_updates+=1;children.append(sum(nw,Q(0)))
   build(history+str(d),nw,mul(lp,factor),ms+[m])
  assert sum(children,Q(0))==z
 build('',[Q(1,13)]*13,[Q(1)],[])
 assert len(nodes)==31
 leaves=[h for h in nodes if len(h)==4]
 rows=[]
 for a in truths:
  guard();total=Q(0);failure=Q(0);stopped=Q(0);expected_forward=Q(0);expected_inverse=Q(0);expected_shots=Q(0)
  for h in leaves:
   guard();p=ev([Q(*x) for x in nodes[h]['likelihood_coefficients_exact']],a);assert p>=0;total+=p
   bad=False;terminal=nodes[h]
   for t in range(1,5):
    n=nodes[h[:t]];like=ev([Q(*x) for x in n['likelihood_coefficients_exact']],a);z=Q(*n['mixture_likelihood_exact'])
    if like<=alpha*z:bad=True
    if n['accuracy_stop']:
     terminal=n;break
   if bad:failure+=p
   if terminal['accuracy_stop']:stopped+=p
   expected_forward+=p*terminal['source_forward_calls'];expected_inverse+=p*terminal['source_inverse_calls'];expected_shots+=p*terminal['shots_and_readouts']
  assert total==1 and failure<=alpha
  rows.append({'amplitude_exact':pair(a),'law_total_exact':pair(total),'failure_at_allowed_stopping_exact':pair(failure),'accuracy_stop_probability_exact':pair(stopped),'hard_cap_UNCERTIFIED_probability_exact':pair(1-stopped),'expected_source_forward_calls_exact':pair(expected_forward),'expected_source_inverse_calls_exact':pair(expected_inverse),'expected_shots_exact':pair(expected_shots),'full_work':None})
 # A literal finite posterior support cannot cover an omitted endpoint.
 bad_prior=[a for a in prior if a!=0];assert 0 not in bad_prior
 assert all(ev(polys[m],Q(0))==0 for m in range(4))
 negative={'rule':'Report only posterior credible particles from a prior excluding0','truth_exact':[0,1],'coverage_exact':[0,1],'rejected':True,'scope':'Literal finite-support report only; no claim against continuous Bayesian inference'}
 return {'tree':list(nodes.values()),'rows':rows,'polynomials_exact':[[pair(c) for c in p] for p in polys],'negative_control':negative,'counts':{'truth_rows':18,'nonterminal_nodes':15,'all_potential_nodes':31,'full_binary_histories':16,'posterior_updates':posterior_updates,'conditional_utility_evaluations':utility_calls,'outer_cell_enclosures':cell_checks,'admitted_truth_hull_containment_checks':containments,'exact_alias_pairs':2},'maximum_recipe_counts':{'source_forward_calls':max(n['source_forward_calls'] for n in nodes.values()),'source_inverse_calls':max(n['source_inverse_calls'] for n in nodes.values()),'each_reflection_calls':max(n['each_reflection_calls'] for n in nodes.values()),'shots_readout_reset':4},'all_amplitude_coverage':'Own symbolic likelihood-ratio proof under exact ideal conditional law; grid law checks diagnostic only','noise_calibration':None,'failed_device_shots':None,'source_delivery':None,'controller_time':None,'strict_complete_work_improvement':None}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['freeze','run']);parser.add_argument('--freeze-sha256');a=parser.parse_args()
 if a.mode=='freeze':
  if FREEZE.exists():raise RuntimeError('Existing freeze immutable')
  f={'schema':'E25-author-freeze-v1','inputs':pinned(PATHS),'selected_runtime':runtime(),'scientific_functions_executed':False}
  with FREEZE.open('x',encoding='utf-8',newline='\n') as h:json.dump(f,h,indent=2,sort_keys=True);h.write('\n')
  print(json.dumps({'freeze_sha256':sha(FREEZE),'inputs':len(PATHS),'input_bytes':sum(x['bytes'] for x in f['inputs'].values())}));return
 if not sys.flags.isolated or not sys.flags.no_site or not sys.dont_write_bytecode:raise RuntimeError('Isolated flags required')
 if OUT.exists():raise RuntimeError('Fresh output required; failure receipt cannot be retried')
 OUT.mkdir(parents=True);marker=OUT/'FAILED_UNSEALED.json'
 try:
  write(marker.name,{'state':'UNSEALED','completed':False,'budget_censored':None},emergency=True)
  if sha(FREEZE)!=a.freeze_sha256:raise RuntimeError('Freeze mismatch')
  f=read(FREEZE);verify(f);guard(admission=True);p=read(DOC/'PROTOCOL.json')
  write('protocol.json',p);write('run_started.json',{'freeze_sha256':a.freeze_sha256,'science':'Exact amplitude law tree only; no draws/gates/finance'})
  result=check(p);write('diagnostic.json',result)
  write('certificate.json',{'passed':True,'completed':True,'budget_censored':False,'bounded_initial_scope_complete':True,'continuous_coverage_proof':'VALID_UNDER_EXACT_IDEAL_CONDITIONAL_SHOT_MODEL','primary_posterior_only_financial_coverage':'UNRESOLVED','financial_adoption':False,'complete_work':None,'baseline':'Retain existing certified estimator; bounded Bayesian branch not promoted','noise_calibration':None,'failed_hardware_shots':None,'new_samples':0,'new_global_fixture_credit':0,'new_gate_replay_credit':0,'quantum_advantage':False})
  write('comparison.json',{'strict_complete_work_improvement':None,'source_cost':None,'inverse_cost':None,'noise_calibration_cost':None,'controller_runtime':None,'readout_runtime':None,'matched_timing':False,'financial_accuracy':None,'compiled_or_replayed_source':False})
  verify(f);guard();members={p.relative_to(ROOT).as_posix():sha(p) for p in OUT.iterdir() if p.is_file() and p!=marker}
  mf={'passed':True,'completed':True,'budget_censored':False,'freeze_sha256':a.freeze_sha256,'frozen_inputs':f['inputs'],'selected_runtime':f['selected_runtime'],'files':members,'manifest_self_hash_excluded':True,'failure_marker_authoritative':True,'new_global_fixture_credit':0,'quantum_advantage':False}
  data=(json.dumps(mf,indent=2,sort_keys=True)+'\n').encode()
  if len(data)>49152 or sum(p.stat().st_size for p in OUT.iterdir())+len(data)+16384>2097152:raise RuntimeError('Manifest reserve cap')
  write('manifest.json',mf);guard();assert {p.name for p in OUT.iterdir()}=={'protocol.json','run_started.json','diagnostic.json','certificate.json','comparison.json','manifest.json',marker.name}
  marker.unlink();guard();print(json.dumps({'passed':True,'manifest_sha256':sha(OUT/'manifest.json')}))
 except BaseException as err:
  if not marker.exists():
   try:write(marker.name,{'state':'FAILED_UNSEALED','completed':False,'budget_censored':None},emergency=True)
   except BaseException:pass
  try:write('retained_error.json',{'type':type(err).__name__,'error':str(err)[:4000],'completed':False,'budget_censored':isinstance(err,RuntimeError) and 'budget' in str(err).lower()},emergency=True)
  except BaseException:pass
  raise
if __name__=='__main__':main()
