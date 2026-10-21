"""A1 affine supersolution/CIR tail proof arithmetic; no SDE draws or compiler."""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import ast
import hashlib
import json
import math
import time

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'results/independent_110_20261004/F15/run001'
DOC=ROOT/'docs/independent_110_20261004/F15'
AUTHOR=Path(__file__).resolve();PROOF=DOC/'NEGATIVE_LEVERAGE_TAIL_PROOF.txt'
CORPUS=[ROOT/p for p in ['research/antithetic_feasibility/classical.py',
 'research/limitation_audit_20261001/experiment_heston_screen.py',
 'results/limitation_audit_20261001/heston_screen_v1/summary.json',
 'docs/limitation_audit_20261001/implementation_plan/roadmap.json',
 'research/independent_110_20261004/F15/primary_sources/Herman_et_al_2602_03725v1.html']]
M=1024;VAR_CAP=64;I_CAP=64;TAIL_ALLOWANCE=Q(1,400)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def pair(q):return [q.numerator,q.denominator]
def upper_sqrt(q):
    scale=1<<80;n=math.isqrt(q.numerator*scale*scale//q.denominator)
    if n*n*q.denominator<q.numerator*scale*scale:n+=1
    out=Q(n,scale);assert out*out>=q and (out-Q(1,scale))**2<q
    return out
def exp_upper(q,parts):
    assert q>=0 and q<parts
    # exp(q/parts)<=1/(1-q/parts), from its positive Taylor series.
    return (1-q/parts)**(-parts)

def prepare():
    assert not OUT.exists() and PROOF.exists()
    OUT.mkdir(parents=True)
    dump(OUT/'protocol.json',{'author_sha256':sha(AUTHOR),'proof_sha256':sha(PROOF),
      'corpus':{str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in CORPUS},
      'contract':'Existing A1 one-asset Heston arithmetic Asian call; all12dates, S0/K100,r.03,T1,kappa2,theta/v0.09,xi.3,rho-.5.',
      'methods':['Affine exponential supersolutions for stockp8(lambda12) andp2(lambda1).',
                 'CIR exponential supersolutions(lambda1,s1) and Cauchy-Schwarz for variance/integral exclusion.'],
      'fixed_cutoffs':{'stock':M,'variance_endpoints':VAR_CAP,'integrated_variance':I_CAP},
      'diagnostic_tail_dollar_allowance':pair(TAIL_ALLOWANCE),
      'allocation_scope':'Proposed standalone tail allowance1/400; no shared activeG2allocation is changed or asserted assigned.',
      'acceptance':['Actual archived A1 and AST parameters match; original direct sufficient-bound failure remains closed.',
                    'Analytic localization/Fatou proves moment-domain bounds before exact rational cutoff arithmetic.',
                    'All12date bounds compose without independence; tail dollar bound<=1/400 for specified state-space truncated target.',
                    'Primitive/inverse/lower-endpoint/increment-law/loading errors and20%complete-cost comparison remain null unless proved.'],
      'budgets':{'cpu_seconds':30,'wall_seconds':60,'output_bytes':4*1024*1024},
      'stop':'The two named bounding methods, these fixed cutoffs and one primitive-interface screen only. No A4extension, new model, MonteCarlo, direct-screen rerun or large compiler.',
      'new_finance_draws':0,'new_global_fixture_credit':0})
    print('F15 A1 negative-leverage proof and fixed cutoffs frozen.')

def run():
    cpu=time.process_time();wall=time.monotonic();p=json.loads((OUT/'protocol.json').read_text())
    assert not (OUT/'RUN_STARTED.json').exists() and sha(AUTHOR)==p['author_sha256'] and sha(PROOF)==p['proof_sha256']
    for path,wanted in p['corpus'].items():assert sha(ROOT/path)==wanted
    dump(OUT/'RUN_STARTED.json',{'models':['A1'],'financial_draws':0,'old_direct_screen_rerun':False})
    old=json.loads(CORPUS[2].read_text());row=next(r for r in old['cases'] if r['model']['name']=='A1')
    model={k:Q(str(v)) for k,v in row['model'].items() if isinstance(v,(int,float))}
    tree=ast.parse(CORPUS[0].read_text(encoding='utf-8'))
    defaults={}
    for node in next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Model').body:
        if isinstance(node,ast.AnnAssign):
            value=ast.literal_eval(node.value)
            if isinstance(value,(int,float)):defaults[node.target.id]=Q(str(value))
    for k in ['dates','spot','strike','rate','maturity','kappa','theta','v0','xi','leverage']:
        assert defaults[k]==model[k]
    assert model['assets']==1 and model['dates']==12
    kappa,theta,v0,xi,rho,rate=[model[k] for k in ['kappa','theta','v0','xi','leverage','rate']]
    spot=model['spot'];T=model['maturity'];N=int(model['dates'])
    assert (kappa,theta,v0,xi,rho,rate,T)==(Q(2),Q(9,100),Q(9,100),Q(3,10),Q(-1,2),Q(3,100),Q(1))
    assert row['direct_transfer_of_full_stated_bound'] is False
    tail_middle=2*kappa*xi*rho-rho*rho*xi*xi
    assert tail_middle==Q(-249,400)<0 and 4*kappa*theta/(xi*xi)==8
    def stock_drift(power,lam,leverage=rho):
        return xi*xi*lam*lam/2+(leverage*xi*power-kappa)*lam+Q(power*(power-1),2)
    drifts={'stock_p8_lambda12':stock_drift(8,12),'stock_p2_lambda1':stock_drift(2,1),
            'variance_lambda1':xi*xi/2-kappa,'integral_s1_lambda1':xi*xi/2-kappa+1}
    assert all(v<=0 for v in drifts.values())
    date_rows=[]
    for date in range(1,N+1):
        t=Q(date,N)*T
        stock8=spot**8*exp_upper((8*rate+kappa*theta*12)*t+12*v0,8)
        stock2=spot**2*exp_upper((2*rate+kappa*theta)*t+v0,1)
        cir=exp_upper(kappa*theta*t+v0,1)
        date_rows.append({'date':date,'time':pair(t),'E_stock8_upper':pair(stock8),
          'E_stock2_upper':pair(stock2),'E_exp_variance_and_integral_upper':pair(cir),
          'E_stock_excess_upper':pair(stock8/Q(M)**7)})
    stock_tail=sum(Q(*r['E_stock_excess_upper']) for r in date_rows)/N
    moment2=sum(Q(*r['E_stock2_upper']) for r in date_rows)/N
    max_cir=max(Q(*r['E_exp_variance_and_integral_upper']) for r in date_rows)
    bad_probability=(N+1)*max_cir/Q(2)**64
    var_integral_tail=upper_sqrt(moment2*bad_probability)
    tail=stock_tail+var_integral_tail
    assert tail<=TAIL_ALLOWANCE
    negative=[]
    for name,bad in [('stock_no_affine_tilt',stock_drift(8,0)),
                     ('reuse_lambda12_after_changing_leverage',stock_drift(8,12,Q(1,2))),
                     ('integral_exponent3_without_new_supersolution',xi*xi/2-kappa+3)]:
        assert bad>0;negative.append({'attempt':name,'positive_drift':pair(bad),'proposed_bound_rejected':True})
    # A marginal moment or finite state window does not imply a coherent increment loader.
    primitive={'conditional_CIR_endpoint_noncentral_chi2':None,
       'integrated_variance_conditional_characteristic_function_inversion':None,
       'equity_gaussian_conditional_on_variance_path':None,'joint_increment_box_truncation':None,
       'lower_integrated_variance_endpoint':None,'loading_and_discretization_dollar_error':None,
       'reversible_stock_and_payoff_precision':None,'source_inverse':None,
       'transition_complete_cost':None,'matched_existing_transition_cost':None,'20_percent_improvement':None,
       'large_compiler_authorized_by_this_receipt':False}
    cutoff={'stock_cap':M,'variance_cap_all12dates':VAR_CAP,'integrated_variance_cap_total':I_CAP,
       'truncated_target':'Unconditional original-path payoff with all stocks min(S,M), and output0 if any endpointvariance>64 or totalI_T>64; no resampling or renormalization.',
       'stock_tail_dollars_upper':pair(stock_tail),'bad_variance_integral_probability_upper':pair(bad_probability),
       'variance_integral_dollars_upper':pair(var_integral_tail),'total_tail_dollars_upper':pair(tail),
       'tail_dollars_upper_display':float(tail),'diagnostic_tail_allowance':pair(TAIL_ALLOWANCE),
       'loading_and_numerical_error':None,'total_financial_error':None,'original_discount_upper_bound_used':1,
       'all_dates_retained':True,'changed_source_adopted':False}
    summary={'passed':True,'completed':True,'scope':'F15 initial A1 upper-state tail proof plus one primitive-interface screen.',
       'tail_proof_passed':True,'cutoff_tail_upper_display':float(tail),'fixed_tail_budget_display':float(TAIL_ALLOWANCE),
       'complete_fast_forward_transfer':'DEFERRED_MISSING_INCREMENT_LOWER_ENDPOINT_AND_IMPLEMENTATION_CERTIFICATES',
       'original_direct_transfer_reopened':False,'A4_joint_law_extension_claimed':False,
       'financial_G2_complete':False,'source_adoption':False,'quantum_advantage':False,
       'new_finance_draws':0,'new_global_fixture_credit':0}
    dump(OUT/'moment_domain_checks.json',{'affine_drift_coefficients':{k:pair(v) for k,v in drifts.items()},
       'date_moments':date_rows,'negative_controls':negative,'model_nominal_decimal_parameters':{k:pair(v) for k,v in model.items()},
       'continuous_SDE_only':True,'finite_machine_source_equivalence':None})
    dump(OUT/'cutoff_error_ledger.json',cutoff);dump(OUT/'primitive_screen.json',primitive);dump(OUT/'reopening_decision.json',summary)
    for path,wanted in p['corpus'].items():assert sha(ROOT/path)==wanted
    assert time.process_time()-cpu<=30 and time.monotonic()-wall<=60
    files=[q for q in OUT.iterdir() if q.is_file()]+[PROOF]
    assert sum(q.stat().st_size for q in files)+32768<=4*1024*1024
    dump(OUT/'manifest.json',{'files':{str(q.relative_to(ROOT)).replace('\\','/'):{'sha256':sha(q),'bytes':q.stat().st_size} for q in files},'author_sha256':sha(AUTHOR),'input_pins':p['corpus']})
    print(json.dumps(summary))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['prepare','run']);args=ap.parse_args()
    if args.mode=='prepare':prepare()
    else:
        try:run()
        except BaseException as exc:
            if OUT.exists():dump(OUT/'FAILED_UNSEALED.json',{'passed':False,'completed':False,'message':str(exc)[:2048],'failure_overrides_partial_summary':True})
            raise
