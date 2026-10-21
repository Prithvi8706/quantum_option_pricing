"""One versioned theorem and finite-width admission audit; no physical schedule."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util
import json
import re

ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('scoped_runtime',ROOT/'research/independent_110_20261004/scoped_audit_runtime_v1.py')
rt=importlib.util.module_from_spec(spec);spec.loader.exec_module(rt)
CASE='results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/'
H17='results/limitation_program_20261001/H17_demand_run002/'
PRIMARY='research/independent_110_20261004/H12/primary_sources/Han_Liu_2609_28461v1.html'
CONSTANTS=['p_star','A','C_add','C_layer','C_F','C_S','C_T','C_B','b_B','c_B','Q','n_star','d0','lambda_Y','g_exponent_b']

def lower_F(n):
    assert type(n) is int and n>=1
    ell=(n-1).bit_length();M=1;rows=[]
    for j in range(1,ell+1):
        # floor(2 log2(4j)) = floor(log2((4j)^2)), exactly.
        h=((4*j)**2).bit_length()-1;u=(1<<h)-1
        assert (1<<h)<=(4*j)**2<(1<<(h+1))
        M*=u;rows.append({'j':j,'h':h,'u':u})
    return {'illustrative_n':n,'ell_lower':ell,'M_lower':M,'F_lower':n*n+n*M,'construction_rows':rows}

def admit(row):
    needed=CONSTANTS+['n','F','k_CCZ','g','compatible_full_D','physical_p','width_condition','noise_model_certificate','code_and_decoder_emitted','complete_failure_upper','physical_depth_seconds']
    assert all(row.get(k) is not None for k in needed),'Missing finite construction or interface'
    assert row['physical_p']<row['p_star'] and row['width_condition'] is True
    assert row['noise_model_certificate'] is True and row['code_and_decoder_emitted'] is True
    assert Q(*row['complete_failure_upper'])<=Q(3,1000)

def check():
    html=(ROOT/PRIMARY).read_text(encoding='utf-8')
    # Locator presence binds the audited version, not a machine proof of the theorem.
    assert all(s in html for s in ['Theorem 3.12','Corollary 3.13','2609.28461v1'])
    capped=json.loads((ROOT/(CASE+'schedule_capped.json')).read_text())
    r=capped['resources']
    assert (r['logical_qubits'],r['clifford_t_depth'],r['t_count'],r['ccx'])==(550141,1661253,520720662,74388666)
    assert r['source_gates']==r['x']+r['cx']+r['ccx']
    # Replace each native CCX by H(target), CCZ, H(target), serialize all gates.
    serial_D=r['x']+r['cx']+3*r['ccx']+r['random_hadamards']
    assert serial_D==310287740
    h17=json.loads((ROOT/(H17+'summary.json')).read_text())
    assert h17['passed'] and h17['architecture_rows']==0 and h17['physical_qubit_cap'] is None
    widths=[row['logical_qubits'] for row in h17['case_rows']]
    assert widths==[550141,4460479]
    examples=[lower_F(n) for n in [1,2,3,4,5,8,9,16,64]]
    for row in examples:
        assert row['F_lower']>=row['illustrative_n']**2
        row['required_width_if_C_F_is_one']=row['F_lower']
        row['illustrative_n_times_F_lower']=row['illustrative_n']*row['F_lower']
        row['width_results_if_C_F_is_one']=[W>=row['F_lower'] for W in widths]
    assert lower_F(4)['F_lower']<=widths[0]<lower_F(5)['F_lower']
    assert lower_F(8)['F_lower']<=widths[1]<lower_F(9)['F_lower']
    # No chosen n or C_F is supplied by these illustrative lower bounds.
    actual={k:None for k in CONSTANTS}
    actual.update(n=None,F=None,k_CCZ=None,g=None,compatible_full_D=None,physical_p=None,width_condition=None,
        noise_model_certificate=None,code_and_decoder_emitted=None,complete_failure_upper=None,physical_depth_seconds=None)
    try:admit(actual)
    except AssertionError as error:reason=str(error)
    else:raise AssertionError('Missing constants became an admitted construction')
    # Fixed-n witness: changing a legal hidden positive multiplier reverses a finite test.
    n=4;f=lower_F(n)['F_lower'];W=widths[0]
    assert W>=f and W<Q(1000)*f
    controls={
      'unavailable_constants_rejected':True,
      'log2_scale_not_usable_code_length':True,
      'single_T_or_QFT_rotation_not_native_CCZ_compilation':True,
      'source_only_depth_not_full_estimator_depth':True,
      'C_F_changes_finite_width_outcome':True,
      'n_times_F_not_theorem_width_condition':True,
      'sufficiently_large_width_not_current_width_certificate':True,
      'physical_noise_threshold_and_seconds_required':True}
    return {'decision':'FINITE_TRANSFER_CLOSED_MISSING_CONSTANTS_CODE_AND_FULL_GATE_COMPILATION',
      'primary_url':'https://arxiv.org/html/2609.28461v1','locators':['Definition2.1','Eq26-29','Theorem3.12/Eq54-59','Corollary3.13'],
      'checks':{'archived_source_rows':1,'original_width_rows':2,'illustrative_code_lengths':9,
                'executed_missing_input_rejections':1,'executed_C_F_finite_witnesses':1},
      'documentary_interface_flags_count':len(controls),
      'source_only':{'logical_width':550141,'archived_Clifford_T_depth':1661253,'serial_Clifford_CCZ_depth_upper':serial_D,
                     'serial_bound_is_not_optimized_depth':True,'arbitrary_connectivity_presumed_by_ideal_model':True},
      'theorem_width_requirement':'W >= C_F * F(n); F(n)=n^2+n*M(n)',
      'n_times_F_is_additional_diagnostic_not_required_width':True,'illustrative_lower_bound_rows':examples,
      'actual_finite_constants':actual,'admission_reason':reason,'controls':controls,
      'code_family_matrices_decoder_controller_constructed':False,'accepted_architectures':0,
      'physical_speedup_claimed':False,'broader_obligations':['Choose finite code/decoder and all constants/cutoffs','Compile complete estimator into the allowed gate model','Certify width and noise hypotheses','Emit routing, resource and classical controller schedules','Complete failure and duration accounting']}

if __name__=='__main__':
    rt.launch(__file__,'H12',[CASE+'schedule_capped.json',H17+'summary.json',H17+'manifest.json',PRIMARY,
      'docs/limitation_audit_20261001/implementation_plan/roadmap.json'],
      ['Bind original widths and distinguish archived Clifford+T from allowed Clifford+CCZ depth.',
       'Check exact illustrative lower bounds for Eq29; unavailable construction constants remain null.',
       'Reject current finite integration when gate, width, noise or complete cost facts are missing.'],
      ['One full-text versioned construction audit and nine prescribed lower-bound examples; stop numerical transfer on missing constants.',
       'No new financial circuit, gate replay, timing, hardware-noise extrapolation or asymptotic constant substituted as measured overhead.'],check)
