"""A4 two-control expectation/conditioning audit; timing acquisition held."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scoped_audit_runtime_v1 import ROOT,Q,pair,model_rows,launch
import ast

INPUTS=['research/antithetic_feasibility/classical.py','research/antithetic_feasibility/hybrid_classical.py',
 'docs/antithetic_feasibility/RESULTS.md','docs/limitation_audit_20261001/implementation_plan/roadmap.json',
 'research/independent_110_20261004/F16/primary_sources/Sigman_2007_BM_GBM_I.pdf']
def check():
    m=next(r for r in model_rows(INPUTS[0]) if r['name']=='A4')
    assert [m[k] for k in ('assets','dates','maturity','theta','leverage','correlation')]==[4,12,1,Q(9,100),Q(-1,2),Q(3,10)]
    d,n=int(m['assets']),int(m['dates']);times=[Q(j,n)*m['maturity'] for j in range(1,n+1)]
    total=Q(0);checks=0
    for i in range(d):
        for j in range(d):
            corr=Q(1) if i==j else m['correlation']
            for s in times:
                for t in times:total+=m['theta']*corr*min(s,t);checks+=1
    var=total/(d*n)**2
    closed=m['theta']*(1+(d-1)*m['correlation'])/d*m['maturity']*(n+1)*(2*n+1)/(6*n*n)
    assert var==closed and var>0
    mu_shift=(m['rate']-m['theta']/2)*sum(times)/n
    factor=[]
    for eig in (1+(d-1)*m['correlation'],1-m['correlation']):
        rho=m['leverage'];lv=rho*rho*eig+1-rho*rho
        assert lv>0
        # ash^2 + asi^2 = eig, and ash*sqrt(lv) = rho*eig.
        shared=rho*rho*eig*eig/lv;independent=eig*(1-rho*rho)/lv
        assert shared+independent==eig
        factor.append({'price_eigenvalue':pair(eig),'variance_eigenvalue':pair(lv),
                       'residual_price_variance':pair(independent),'cross_covariance':pair(rho*eig)})
        checks+=3
    # Tower and centering identities on an exact finite algebra diagnostic, not A4 draws.
    ys=[Q(0),Q(2),Q(1),Q(5)];gs=[Q(0),Q(1),Q(2),Q(3)]
    mean_g=sum(gs)/4
    for coefficient in (Q(-2),Q(0),Q(1,2),Q(3)):
        residual=[y-coefficient*(g-mean_g) for y,g in zip(ys,gs)]
        assert sum(residual)/4==sum(ys)/4
        conditional=[sum(residual[:2])/2,sum(residual[2:])/2]
        var_raw=sum((v-sum(residual)/4)**2 for v in residual)/4
        var_cond=sum((v-sum(conditional)/2)**2 for v in conditional)/2
        assert var_cond<=var_raw;checks+=2
    src=(ROOT/INPUTS[0]).read_text(encoding='utf-8')
    hybrid=(ROOT/INPUTS[1]).read_text(encoding='utf-8')
    assert 'gbm[asset]+=(rate-.5*theta)*h+math.sqrt(theta)*ws' in src
    assert 'control_mean(m)' in hybrid and 'conditional=False' in src
    history=(ROOT/INPUTS[2]).read_text(encoding='utf-8')
    assert '10.17 of 13.75' in history and 'fixed allocation' in history
    total_old=Q(1375,100);base_old=Q(1017,100)
    return {'decision':'EXPECTATION_INTERFACES_PROVED_MATCHED_TRAINING_INCLUSIVE_COST_AND_RETUNING_HELD',
      'checks':checks+4,'geometric_log_variance':pair(var),'geometric_log_mean_shift':pair(mu_shift),
      'joint_Gaussian_factor_identities':factor,'nominal_A4_contract_unchanged':True,
      'two_candidates':['Existing frozen-volatility geometric control, analytically priced on the same Gaussian inputs.',
                        'Conditional level-zero residual by integrating the independent common price mode.'],
      'candidate1_already_used_by_saved_base':True,'candidate2_existing_conditional_method':True,
      'historical_fixed_allocation_seconds':{'base':pair(base_old),'total':pair(total_old)},
      'historical_free_correction_ceiling':pair(total_old/base_old),
      'new_control_mean_machine_error':None,'training_inclusive_new_base_cost':None,
      'retuned_allocation':None,'classical_shared_control_delivery':None,'tenfold_complete_budget_pass':None,
      'new_timing_measurements':0,'single_delivery_setup_amortized':False,
      'remaining':['Outward numerical control expectation/root accuracy.','Same-contract training-inclusive matched timings after timing ownership clears.','Reoptimize all base and correction uncertainty under the same delivered error.']}
if __name__=='__main__':launch(__file__,'F11',INPUTS,
 ['Same frozen A4 law/dates; prove analytic geometric mean and Gaussian conditioning without claiming discrete-to-continuous bias removed.',
  'Keep historical allocation floor allocation-specific; no new timing or setup amortization.'],
 'Exactly two existing coarse controls; initial proof/interface scope only; hold matched acquisition and allocation-dependent performance conclusion.',check)
