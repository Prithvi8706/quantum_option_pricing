"""A1 Broadie-Kaya endpoint/moment and negative-leverage primitive audit."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scoped_audit_runtime_v1 import ROOT,Q,pair,model_rows,launch
INPUTS=['research/antithetic_feasibility/classical.py',
 'results/limitation_audit_20261001/heston_screen_v1/summary.json',
 'research/independent_110_20261004/F14/primary_sources/Broadie_Kaya_OR_2006.pdf',
 'docs/limitation_audit_20261001/implementation_plan/roadmap.json']
def check():
    m=next(r for r in model_rows(INPUTS[0]) if r['name']=='A1')
    k,theta,xi,rho=[m[v] for v in ('kappa','theta','xi','leverage')]
    assert (k,theta,xi,rho,m['assets'],m['dates'])==(2,Q(9,100),Q(3,10),Q(-1,2),1,12)
    nu=4*k*theta/(xi*xi);assert nu==8
    checks=1
    moments=[]
    # q denotes exp(-kappa*h); these rational diagnostic q values test algebra,
    # never substitute for the actual contractual exponential.
    for q in (Q(1,4),Q(1,2),Q(2,3),Q(9,10)):
        c=xi*xi*(1-q)/(4*k)
        for v in (Q(0),m['v0'],Q(1),Q(64)):
            lam=q*v/c
            mean=c*(nu+lam);variance=2*c*c*(nu+2*lam)
            want_mean=q*v+theta*(1-q)
            want_variance=xi*xi*v*q*(1-q)/k+theta*xi*xi*(1-q)**2/(2*k)
            assert mean==want_mean and variance==want_variance
            # Normal-square construction: one (Z+sqrt(lambda))^2 and seven Z^2.
            assert nu+lam==8+lam and 2*(nu+2*lam)==16+4*lam
            moments.append({'q_algebra_test':pair(q),'v':pair(v),'conditional_mean':pair(mean),'conditional_variance':pair(variance)})
            checks+=4
    h=m['maturity']/m['dates'];formulas=[]
    for v,w,I in [(Q(9,100),Q(1,10),Q(1,100)),(Q(0),Q(1,20),Q(1,50)),(Q(1),Q(3,4),Q(1,5))]:
        J=(w-v-k*theta*h+k*I)/xi
        assert w-v==k*theta*h-k*I+xi*J
        logmean=m['rate']*h-I/2+rho*J
        logvariance=(1-rho*rho)*I
        assert logvariance>0
        if J:assert logmean!=m['rate']*h-I/2 # leverage cannot be dropped
        formulas.append({'v':pair(v),'v_next':pair(w),'I':pair(I),'J':pair(J),'log_increment_conditional_mean':pair(logmean),'conditional_variance':pair(logvariance)})
        checks+=3
    assert nu/2-1==3 and 1-rho*rho==Q(3,4);checks+=2
    ledger={name:{'per_date_calls':count,'all12date_calls':12*count,'certified_law_or_precision_error':None,
                    'emitted_T_count':None,'inverse_T_count':None,'physical_seconds':None}
      for name,count in [('endpoint_normal_draws',8),('conditional_integral_uniform',1),('equity_normal_draws',1),
                         ('endpoint_exponential_and_sqrt',1),('conditional_complex_Bessel_CF',1),
                         ('conditional_Fourier_inversion',1),('CDF_inverse_bracket',1),('stock_exp_update',1),('payoff_accumulation',1)]}
    return {'decision':'ENDPOINT_AND_LEVERAGE_LAWS_MAPPED_CONDITIONAL_INTEGRAL_CERTIFICATE_MISSING_STOP_BEFORE_PILOT_COMPILATION',
      'checks':checks,'contract':'Original A1 one asset twelve dates; negative leverage retained.',
      'CIR_degrees_of_freedom':pair(nu),'conditional_Bessel_order':pair(nu/2-1),
      'CIR_endpoint_moment_algebra_controls':moments,'negative_leverage_identities':formulas,
      'primitive_ledger':ledger,'per_date_integral_CF_evaluation_count':None,
      'proposed_capped_payoff_TV_error_relation':'If a capped payoff<=B and per-transition total variation<=eta_j, coupling and union give dollar error<=B*sum_j eta_j; uncapped tail and stock/arithmetic errors require additional bounds.',
      'cap_B_and_assigned_error':None,'CF_tail_and_quadrature_error':None,'inverse_CDF_and_special_function_error':None,
      'uncapped_payoff_tail_and_loader_bridge':None,'complete_all12date_transition_cost':None,
      'refined_reference_uncertainty_interval':None,'exact_transition_pilot_executed':False,
      'A4_joint_covariance_extension':None,'new_financial_samples':0,
      'remaining':['Uniform conditional integrated-CIR CF/inverse error, including small endpoint/low integral regime.','A fully charged finite implementation and independent refined-price comparison with valid interval.','Exact correlated joint construction before any A4 transfer.']}
if __name__=='__main__':launch(__file__,'F14',INPUTS,
 ['Validate fixed A1 endpoint moment and stock-leverage identities; charge every original date and inverse/precision primitive.',
  'Do not rename a trapezoidal integral or independent endpoint sampler an exact full Heston transition.'],
 'One Broadie-Kaya primitive inventory and law preflight. Stop before the end-to-end transition pilot/compiler because conditional integral inverse accuracy is uninstantiated.',check)
