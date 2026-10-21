"""Fixed-policy pointwise and population-bound interfaces; no E12 acquisition."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scoped_audit_runtime_v1 import ROOT,Q,pair,model_rows,launch
INPUTS=['research/compound_feasibility/model.py','research/controlled_residual_feasibility/bounds.py',
 'results/compound_feasibility/pilot_v1/training.json','docs/compound_feasibility/RESULTS.md',
 'docs/limitation_audit_20261001/implementation_plan/roadmap.json']
WIDTHS=[Q(1,100),Q(1,20),Q(1,10)]
def check():
    training=json.loads((ROOT/INPUTS[2]).read_text(encoding='utf-8'))
    models=model_rows(INPUTS[0]);assert len(models)==4 and all(m['name'] in training for m in models)
    checks=0;K=Q(3);states=[]
    for C in [Q(j,2) for j in range(13)]:
        for pred in [Q(j,2) for j in range(13)]:
            exercise=pred>K
            regret=max(C-K,0)-int(exercise)*(C-K)
            error=abs(C-pred)
            assert 0<=regret<=error;checks+=1
            for width in WIDTHS:
                inside=abs(pred-K)<=width
                bound=width+error if inside else error*error/width
                assert regret<=bound;checks+=1
            for low,high in [(max(Q(0),C-Q(1,2)),C+Q(1,2)),(C,C)]:
                env=max(K-low,0) if exercise else max(high-K,0)
                assert regret<=env
                certified=(low>=K and exercise) or (high<=K and not exercise)
                if certified:assert regret==0 and env==0
                checks+=2
    # Exact diagnostic law with tiny unseen mass: sampled zero regret does not
    # imply zero population regret; this is an implication counterexample.
    tail_prob=Q(1,1000000);rare_C=Q(1000000);rare_pred=Q(0)
    tail_regret=tail_prob*(rare_C-K)
    assert tail_regret>Q(9,10)
    for width in WIDTHS:
        assert tail_regret<=tail_prob*(rare_C-rare_pred)**2/width;checks+=1
    cases=[]
    for m in models:
        frozen=training[m['name']]
        assert frozen['selected'] in ('moment','regression')
        cases.append({'case':m['name'],'assets':int(m['assets']),'dates':int(m['dates']),
          'fixed_policy_selector':frozen['selected'],'policy_retrained':False,
          'observed_validation_rmse':frozen['validation_rmse_'+frozen['selected']],
          'observed_rmse_is_population_moment_bound':False,
          'bands':[{'width':pair(w),'population_band_probability':None,'population_continuation_error_second_moment':None,
                    'unsampled_tail_error':None,'total_population_regret':None,'localized_complete_cost':None} for w in WIDTHS]})
        checks+=1
    src=(ROOT/INPUTS[1]).read_text(encoding='utf-8')
    assert 'lower>upper+1e-8' in src and 'upper=np.maximum(upper,lower)' in src
    return {'decision':'POINTWISE_BOUNDARY_LEDGER_PROVED_POPULATION_AND_LOCALIZED_COST_CERTIFICATION_UNAVAILABLE_RETAIN_POLICY',
      'checks':checks+3,'three_band_widths':list(map(pair,WIDTHS)),'cases':cases,
      'conditional_interval_scope':'Analytic real-law AM-GM/Jensen intervals for the capped continuation; floating implementation is not an interval enclosure.',
      'pointwise_regret':'r=(C-K)+-1{pred>K}(C-K)=|C-K|1{wrong}<=|C-pred|.',
      'population_band_bound':'r <= (w+|C-pred|)1{|pred-K|<=w}+(C-pred)^2/w*1{|pred-K|>w}; expectation <=w*p+sqrt(m2*p)+m2/w when population m2 and p are certified.',
      'rare_unsampled_counterexample':{'probability':pair(tail_prob),'continuation':pair(rare_C),'predictor':pair(rare_pred),'population_regret':pair(tail_regret),'workload_role':'Algebraic implication counterexample only, no new financial contract.'},
      'historical_sampled_brackets':'Previously observed about4e-8 through6e-6 dollars; observations only, not population bounds.',
      'outside_decision_interval_numeric_certificate':None,'population_regret_dollar_allowance_assigned':None,
      '20percent_complete_localization_saving':None,'new_samples':0,'E12_inputs_or_acquisitions_changed':False,
      'remaining':['Outward continuation intervals on the unchanged capped law plus cap/unsampled-tail transfer.','Independent population expectation certificate for regret envelope or band/error moments.','Boundary-detection, confidence and padded/coherent source cost before compiler admission.']}
if __name__=='__main__':launch(__file__,'F17',INPUTS,
 ['Retain all four existing development cases, saved policy choice/coefficients and three bands0.01/0.05/0.1.',
  'Prove pointwise envelope and band composition; sampled RMSE or bracket never substitutes for a population certificate.'],
 'Three boundary widths and one pointwise/population interface audit; no retraining, samples, E12 rule changes or localized compiler. Stop localization on unavailable population certification.',check)
