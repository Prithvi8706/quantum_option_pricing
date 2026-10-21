"""F25 integer/fraction accounting only, no density or quantum execution."""
import argparse
import ast
from fractions import Fraction as F
import hashlib
import json
from math import comb,factorial
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[3]
OWN='research/independent_110_20261004/F25'
OUT=ROOT/'results/independent_110_20261004/F25/run001'
INPUTS=['research/release_checks/targets.py','research/journal_sprint/asian_basket.py',
        OWN+'/primary_sources/Guseynov_2511_04942v1.html',
        OWN+'/primary_sources/BHMT_quant_ph_0005055v1.pdf',OWN+'/readout_ledger_v1.py',
        'docs/independent_110_20261004/F25/OVERLAP_PROOF_run001.txt']
CAPS=dict(cpu_seconds=5,wall_seconds=15,input_bytes=4*1024**2,output_bytes=1024**2,output_files=16)
D1=dict(id='D1',split='development',assets=1,dates=2,sigma=.2,strike=95.,correlation=.3)
def sha(x):return hashlib.sha256(x).hexdigest()
def ex(x):return [x.numerator,x.denominator]
def ceil(x):return -(-x.numerator//x.denominator)
def write(name,data):
    p=OUT/name
    if p.exists():raise ValueError('Refuse overwrite')
    p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def prepare():
    if OUT.exists():raise ValueError('Fresh output required')
    corpus=[dict(path=p,bytes=(ROOT/p).stat().st_size,sha256=sha((ROOT/p).read_bytes())) for p in INPUTS]
    size=sum(x['bytes'] for x in corpus)
    if size>CAPS['input_bytes']:raise ValueError('Input cap')
    OUT.mkdir(parents=True)
    write('protocol.json',dict(corpus=corpus,budgets=CAPS,corpus_bytes=size,contract=D1,
        finite_candidate_valid_cells=1089,padded_basis=2048,qubits=11,log_X_domain=[-2,2],Q_domain=[0,300],
        denominator_amplitude_lower=[1,64],denominator_squared_lower=[1,4096],price_scale_upper=205,
        overlap_error_dollars=[1,1000],statistical_failure=[3,1000],AE_fresh_medians=35,
        readouts=['squared_overlap_swap_copies','real_overlap_Hadamard_canonical_AE'],
        density_evolutions=0,quantum_circuits=0,stop='Two conditional ledgers; missing M/access/bias/times stay unresolved'))
    print(json.dumps(dict(prepared=True,files=len(corpus),bytes=size,protocol_sha256=sha((OUT/'protocol.json').read_bytes()))))

def source_contract():
    t=ast.parse((ROOT/'research/release_checks/targets.py').read_text())
    n=next(x for x in t.body if isinstance(x,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='CASES' for a in x.targets))
    case={kw.arg:ast.literal_eval(kw.value) for kw in n.value.elts[0].keywords}
    if case!=D1:raise ValueError('D1 contract changed')

def AE(eta):
    M=2
    while 2*(F(22,7*M)+F(22,7)**2/M**2)>eta:M*=2
    return dict(M=M,phase_qubits=M.bit_length()-1,fresh_runs=35,
        W_forward_calls=35*M,W_inverse_calls=35*(M-1),
        zero_reflections=35*(M-1),flag_reflections=35*(M-1),
        IQFT_runs=35,QPE_readout_bits=35*(M.bit_length()-1),
        source_normalized_density_forward_calls=35*M,
        source_normalized_density_inverse_calls=35*(M-1),
        complete_source_forward_cost=None,complete_source_inverse_cost=None,
        coherent_postselection_amplification_cost=None,controlled_access_cost=None,
        reflection_and_IQFT_synthesis_cost=None,total_physical_time=None)

def run():
    if (OUT/'ATTEMPT.json').exists():raise ValueError('One invocation only')
    p=json.loads((OUT/'protocol.json').read_text());wall=time.monotonic();cpu=time.process_time()
    write('ATTEMPT.json',dict(status='STARTED',kind='fixed_readout_fraction_accounting'))
    try:
        if p['budgets']!=CAPS or p['contract']!=D1 or [x['path'] for x in p['corpus']]!=INPUTS:raise ValueError('Protocol changed')
        for r in p['corpus']:
            raw=(ROOT/r['path']).read_bytes()
            if len(raw)!=r['bytes'] or sha(raw)!=r['sha256']:raise ValueError('Frozen input changed')
        source_contract()
        e=F(1,1000);B=F(205);d0=F(1,64);b0=d0**2;alpha=F(3,1000)
        eta_a=e**2*b0/(8*B**2);eta_b=e*b0**2/(4*B)
        eta_c=e*d0/(4*B);eta_d=e*d0**2/(4*B)
        if eta_b>b0/2 or eta_d>d0/2:raise ValueError('Denominator stability budget failed')
        if B*(2*eta_c/d0+2*eta_d/d0**2)>e:raise ValueError('Amplitude dollar allocation failed')
        taylor=sum(F(8)**j/factorial(j) for j in range(13))
        if taylor<=F(4000,3):raise ValueError('Hoeffding finite-copy constant failed')
        n_a=ceil(16/(eta_a/2)**2);n_b=ceil(16/(eta_b/2)**2)
        median_failure=sum(F(comb(35,j))*F(1,4)**j*F(3,4)**(35-j) for j in range(18,36))
        if 2*median_failure>=alpha:raise ValueError('Two AE medians exceed alpha')
        # Positive denominator/scaling algebra controls plus retained countercases.
        weights=[F(1,3),F(2,3)];payoffs=[F(0),F(9)]
        expected=sum(w*f for w,f in zip(weights,payoffs))
        if expected!=6 or sum(weights)!=1:raise ValueError('Exact mass/payoff control failed')
        scaled_mass=F(1,2)
        if scaled_mass*expected==expected:raise ValueError('Omitted subprobability mass was accepted')
        def valid_density(m):return bool(m) and all(x>=0 for x in m) and 0<sum(m)<=1
        if not valid_density(weights) or valid_density([F(0),F(0)]) or valid_density([F(-1),F(2)]):
            raise ValueError('Density positivity/norm controls failed')
        controls=dict(executed_negative_counterchecks=['subprobability_M_omission','zero_density_norm','signed_density'],
            documentary_flags=dict(no_positive_numerator_lower_assumed=True,
                unknown_state_error_not_reduced_by_more_copies=True,
                no_unitary_inverse_inferred_from_postselection=True,shot_count_is_not_full_runtime=True))
        swap=dict(eta_a=ex(eta_a),eta_b=ex(eta_b),shot_eta_a=ex(eta_a/2),shot_eta_b=ex(eta_b/2),
            reserved_state_eta_a=ex(eta_a/2),reserved_state_eta_b=ex(eta_b/2),overlap_dollar_error_upper=ex(F(7,8)*e),
            numerator_fresh_copies=n_a,denominator_fresh_copies=n_b,
            complete_density_preparation_evolutions=n_a+n_b,payoff_state_preparations=n_a,
            uniform11H_preparations=n_b,swap_ancilla_readouts=n_a+n_b,
            controlled_swap_positions=11*(n_a+n_b),
            state_loading_error_upper=None,density_evolution_error_upper=None,total_physical_time=None,
            ideal_copy_bound_is_actual_certificate=False)
        ae_c=AE(eta_c/2);ae_d=AE(eta_d/2)
        coherent=dict(eta_c=ex(eta_c),eta_d=ex(eta_d),shot_eta_c=ex(eta_c/2),shot_eta_d=ex(eta_d/2),
            reserved_state_control_eta_c=ex(eta_c/2),reserved_state_control_eta_d=ex(eta_d/2),overlap_dollar_error_upper=ex(e),
            numerator=ae_c,denominator=ae_d,
            total_density_forward_calls=ae_c['W_forward_calls']+ae_d['W_forward_calls'],
            total_density_inverse_calls=ae_c['W_inverse_calls']+ae_d['W_inverse_calls'],
            payoff_inverse_calls=ae_c['W_forward_calls'],payoff_forward_calls=ae_c['W_inverse_calls'],
            total_two_overlap_failure_upper=ex(2*median_failure),normalized_unitary_access_supplied=False)
        summary=dict(status='PASS_NORMALIZATION_PROOF_ACCOUNTING_ONLY_F25_UNRESOLVED',swap=swap,coherent=coherent,
            controls=controls,finite_density_mass_M=None,finite_payoff_norm_certificate=None,
            required_estimated_B_clipping_interval=[[0,1],[205,1]],
            B_error_propagation_coefficient_upper=64,
            B_error_bound_uses_true_ratio_and_clipped_estimated_scale=True,
            B_normalization_error_upper=None,grid_truncation_event_price_bias_upper=None,
            density_evolution_and_preparation_cost=None,fastest_eligible_classical_time=None,
            full_F25_acceptance=False,actual_density_states_prepared=0,actual_overlap_measurements=0,
            actual_quantum_or_financial_samples=0,quantum_advantage_claimed=False,
            primary_date_discrepancy_preserved=True,primary_call_put_label_discrepancy_preserved=True)
        if time.process_time()-cpu>CAPS['cpu_seconds'] or time.monotonic()-wall>CAPS['wall_seconds']:raise ValueError('Budget cap')
        write('summary.json',summary);write('SUCCESS.json',dict(status=summary['status'],full_F25_acceptance=False))
        files=[f for f in OUT.iterdir() if f.is_file()]
        manifest=dict(files=[dict(path=f.name,bytes=f.stat().st_size,sha256=sha(f.read_bytes())) for f in sorted(files)])
        if len(files)+1>CAPS['output_files'] or sum(f.stat().st_size for f in files)+len(json.dumps(manifest).encode())>CAPS['output_bytes']:raise ValueError('Output cap')
        write('manifest.json',manifest)
        print(json.dumps(dict(status=summary['status'],swap_density_copies=n_a+n_b,
                              coherent_density_calls=coherent['total_density_forward_calls']+coherent['total_density_inverse_calls'],
                              summary_sha256=sha((OUT/'summary.json').read_bytes()))))
    except BaseException as exc:
        if not (OUT/'FAILED.json').exists():write('FAILED.json',dict(status='FAILED_PRESERVED',error=str(exc)))
        raise

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('mode',choices=['prepare','run']);args=a.parse_args()
    prepare() if args.mode=='prepare' else run()
