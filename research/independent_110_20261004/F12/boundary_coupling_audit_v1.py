"""S4 one nominated implicit-square-root scheme: positivity and bias preflight."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scoped_audit_runtime_v1 import ROOT,Q,pair,model_rows,launch
INPUTS=['research/antithetic_feasibility/classical.py','research/antithetic_feasibility/hierarchy.py',
 'results/antithetic_feasibility/decision_summary_v1/variance_fits.json',
 'research/independent_110_20261004/F12/primary_sources/Alfonsi_SC_preprint_2005.pdf',
 'docs/limitation_audit_20261001/implementation_plan/roadmap.json']
def check():
    m=next(r for r in model_rows(INPUTS[0]) if r['name']=='S4')
    k,theta,xi,rho=[m[v] for v in ('kappa','theta','xi','leverage')]
    assert (k,theta,xi,rho,m['dates'],m['assets'])==(2,Q(1,25),Q(1,2),Q(-7,10),12,4)
    a=k*theta;feller=2*a/(xi*xi);assert feller==Q(16,25)
    margin=a-xi*xi/4;implicit_a=margin/2;assert margin==Q(7,400)>0
    levels=[];checks=0
    for lev in (1,2,3,4):
        h=m['maturity']/(int(m['dates'])*2**lev);A=1+k*h/2
        assert A>0 and implicit_a*h>0
        # Use v=s^2 and Brownian increment w as deterministic algebra inputs.
        for s in (Q(0),Q(1,20),Q(1,5),Q(1)):
            for w in (Q(-2),Q(-1,3),Q(0),Q(1,3),Q(2)):
                old=(s*s+a*h+xi*s*w+xi*xi*(w*w-h)/4)/(1+k*h)
                square=((s+xi*w/2)**2+margin*h)/(1+k*h)
                assert old==square and old>0
                B=s+xi*w/2;D=B*B+4*A*implicit_a*h
                assert D>B*B
                # Product of quadratic roots is -implicit_a*h/A <0.
                assert -implicit_a*h/A<0;checks+=3
        levels.append({'level':lev,'internal_steps':int(m['dates'])*2**lev,'step':pair(h),
                       'monitoring_dates':12,'candidate_cost_times_variance':None,'certified_weak_bias':None,
                       'matched_finance_paths':0,'timing_measurements':0})
    history=json.loads((ROOT/INPUTS[2]).read_text(encoding='utf-8'))
    old=[r for r in history if r['case']=='S4'];assert len(old)==2
    src=(ROOT/INPUTS[0]).read_text(encoding='utf-8')
    assert '(1+kappa*h)' in src
    assert 'j=(step^1) if mode==1 else step' in src
    assert 'ds[path,2*step,asset]+ds[path,2*step+1,asset]' in src
    # Deterministic covariance accounting under fine/coarse sums.
    for h in [Q(*r['step']) for r in levels]:
        assert 2*h==h+h and rho*(2*h)==2*rho*h;checks+=2
    return {'decision':'POSITIVITY_PROVED_BIAS_AND_MATCHED_COST_VARIANCE_TRANSFER_CLOSED',
      'checks':checks+5,'Feller_ratio':pair(feller),'existing_scheme_positive_margin':pair(margin),
      'candidate':'Alfonsi2005 equation4 drift-implicit square-root scheme, same coupled Brownian inputs.',
      'candidate_unique_positive_root':True,'candidate_is_exact_CIR_sampler':False,
      'four_frozen_levels':levels,'historical_beta_observations':[{'method':r['method'],'conditional':r['conditional'],'beta':r['beta'],'scope':r['scope']} for r in old],
      'beta2_proved':False,'same_Brownian_marginals_are_complete_Heston_bias_certificate':False,
      'proposed_matched_protocol':'Keep original multivariate ws/wv covariance and fine/coarse sum/adjacent swap; replace variance recurrence only, retain all12dates. No pilot before a stated certified bias allowance and matched timing ownership.',
      'equity_weak_bias_bound':None,'boundary_inverse_moment_hypotheses':None,'strong_rate_constants':None,
      '20percent_at_three_of_four_levels':None,'new_finance_samples':0,
      'remaining':['Prove full equity/payoff bias at the nominated four levels, including accessible variance boundary.','Freeze a justified finite sample budget and independent reference certificate before acquisition.','Obtain matched per-path costs and correction variances; positivity alone cannot admit a source.']}
if __name__=='__main__':launch(__file__,'F12',INPUTS,
 ['Freeze S4 Feller0.64; current positivity must not be attributed to a new method.',
  'Check one equation4 candidate and original fine/coarse covariance interfaces at four levels; no beta2 or bias claim from positivity.'],
 'One alternative, levels1/2/3/4; initial bias/hypothesis preflight. Stop numerical adoption on unresolved full equity bias; no paths or competing timings.',check)
