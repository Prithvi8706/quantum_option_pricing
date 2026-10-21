"""One Sun v1 D1 schedule audit with two bounded refinements; QAMC gaps retained."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scoped_audit_runtime_v1 import ROOT,Q,pair,launch
INPUTS=['research/independent_110_20261004/F18/primary_sources/Sun_Wang_Blanchet_2602_08120v1.html',
 'research/compound_feasibility/quantum_schedule.py','results/compound_feasibility/cost_v3/schedules.json',
 'results/independent_110_20261004/E15/run002/certificate.json',
 'docs/limitation_audit_20261001/implementation_plan/roadmap.json']
ERRORS=[Q(1,10),Q(3,100),Q(1,100)]
def cutoff(r):
    n=0
    while Q(1,2**n)>r*r:n+=1
    return n
def check():
    p=[Q(1,4),Q(3,4)];g=lambda v:max(v-Q(1,2),0)
    target=sum(g(v) for v in p)/2;assert target==Q(1,8)
    rows=[];checks=1
    for error in ERRORS:
        rmse=error/16;B=cutoff(rmse);refined=B+2
        written=2*rmse*rmse/9+2*Q(1,2**B)
        corrected=2*rmse*rmse/9+2*Q(1,2**refined)
        assert written>rmse*rmse and corrected<=rmse*rmse
        assert rmse*rmse/(error*error)==Q(1,256)<=Q(1,250)
        levels=[]
        for n in range(refined+1):
            levels.append({'level':n,'inner_RMSE_squared':pair(Q(1,2**n)),
              'previous_inner_RMSE_squared':None if n==0 else pair(Q(1,2**(n-1))),
              'outer_level_RMSE':pair(rmse/(3*(refined+1))),
              'difference_second_moment_upper':pair(Q(1) if n==0 else min(Q(1),6*Q(1,2**n))),
              'finite_QAMC_repetitions':None,'conditional_source_and_inverse_calls':None,
              'decoder_and_coherent_wrapper_gate_count':None})
        # Exact-inner outputs satisfy every stated RMSE promise. They expose
        # what literal n0 successive difference telescopes to without a base.
        literal=sum(sum(g(v)-g(v) for v in p)/2 for n in range(refined+1))
        with_base=sum(g(v) for v in p)/2
        assert literal==0 and abs(literal-target)==Q(1,8)>error
        assert with_base==target
        rows.append({'same_two_point_toy_error':pair(error),'stat_failure_allowance':pair(Q(1,250)),
          'chosen_RMSE':pair(rmse),'integer_written_cutoff':B,'first_refinement_cutoff':refined,
          'literal_proof_MSE_upper':pair(written),'corrected_proof_MSE_upper':pair(corrected),
          'literal_base_convention_counterexample_output':pair(literal),
          'second_refinement_explicit_Delta0_output':pair(with_base),'deterministic_levels':levels,
          'coherent_interface_status':'Exact E15 inner toy certificate retained as interface evidence; not a Sun QAMC implementation.',
          'same_contract_finite_call_comparison':None,'compiled_complete_work':None})
        checks+=6+len(levels)
    archived=json.loads((ROOT/INPUTS[2]).read_text(encoding='utf-8'))
    selected=[]
    for error in ERRORS:
        r=next(r for r in archived if r['case']=='C4' and Q(str(r['epsilon']))==error and r['normalizer']==1)
        assert r['conditional_primitive_and_inverse_calls']>0
        selected.append({'case':'C4','epsilon':pair(error),'saved_calls':r['conditional_primitive_and_inverse_calls'],
                         'role':'Historical financial control; not same two-point toy, so no ratio or speedup comparison.'})
        checks+=1
    source=(ROOT/INPUTS[0]).read_text(encoding='utf-8')
    assert 'Algorithm 6' in source and 'Corollary 3.2' in source
    return {'decision':'FINITE_D1_SCHEDULE_SCREEN_COMPLETE_THEOREM_CONTROLLER_AND_SAME_CONTRACT_COST_TRANSFER_CLOSED',
      'checks':checks+2,'toy':'X uniform0/1, conditional Bernoulli p=(1+2X)/4, g0(z)=(z-1/2)+; D1.',
      'exact_target':pair(target),'terminal_second_moment_upper':pair(Q(1)),'outer_Lipschitz_constant':1,
      'one_theorem_variant':'Sun/Wang/Blanchet2602.08120v1 Algorithm6, Prop3.4, Cor3.2.',
      'two_prospective_refinements':['Add two cutoff levels to match the displayed proof factor4.','Declare Delta0=g0(R1); telescope only positive-level differences.'],
      'source_scope':'Two written-source conventions require explicit resolution before implementation; no paper-wide theorem refutation.',
      'three_schedule_rows':rows,'saved_financial_controls':selected,
      'finite_Kothari_ODonnell_QAMC_constants':None,'coherent_recursive_QAMC_unitary':None,
      'median_decoder_synthesis_and_inverse':None,'source_gate_based_comparison':None,
      'same_contract_strict_improvement':None,'saved_hierarchy_is_universal_lower_bound':False,
      'remaining':['Instantiate a finite quantitative QAMC controller and emitted source/decoder/inverse gates at the same toy contract.','Resolve exact base and cutoff conventions in the nominated version.','Compare integer conditional calls at all three same-error/confidence targets before finance integration.']}
if __name__=='__main__':launch(__file__,'E14',INPUTS,
 ['One D1 two-point bounded transition, L1 outer payoff, exact target and errors0.1/0.03/0.01.',
  'Retain literal cutoff/base tests plus at most two declared refinements; unknown finite QAMC constants/calls remain null.'],
 'One theorem variant, three errors, two refinements. Stop advance on missing implementable finite QAMC controller; no finance/compiler integration or inferred big-O constants.',check)
