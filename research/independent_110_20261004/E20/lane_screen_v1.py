"""Fixed metadata/accounting screen only; no science imports or execution."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import factorial
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[3]
CASE='results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth'
ITERATE='results/limitation_program_20261001/E02_financial_run002/B4x12/iterate.json'
H17='results/limitation_program_20261001/H17_demand_run002/B4x12/hardware_demand.json'
E21='results/limitation_program_20261001/E21_conversion_run001/certificate.json'
OWN='research/independent_110_20261004/E20'
OUT=ROOT/'results/independent_110_20261004/E20/run001'
INPUTS=[CASE+'/target.json',CASE+'/source.json',CASE+'/schedule_capped.json',ITERATE,H17,E21,
        'research/controlled_priority_completion/capacity_screen.py',
        OWN+'/primary_sources/Oshio_Wada_Yamamoto_2508_06121v3.html',OWN+'/lane_screen_v1.py',
        'docs/independent_110_20261004/E20/ASSUMPTIONS_run001.txt']
CAPS=dict(cpu_seconds=5,wall_seconds=15,input_bytes=8*1024**2,output_bytes=1024**2,output_files=16)
TARGET='a7a682731b3cdb6f16b32a9b1a467d6bfeccb32ea97e583ab79e5252bb7a9384'

def sha(raw):return hashlib.sha256(raw).hexdigest()
def exact(x):return [x.numerator,x.denominator]
def load(path):return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def write(name,x):
    p=OUT/name
    if p.exists():raise ValueError('Refuse overwrite')
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def prepare():
    if OUT.exists():raise ValueError('Fresh output required')
    inputs=[dict(path=p,bytes=(ROOT/p).stat().st_size,sha256=sha((ROOT/p).read_bytes())) for p in INPUTS]
    size=sum(r['bytes'] for r in inputs)
    if size>CAPS['input_bytes']:raise ValueError('Input cap')
    OUT.mkdir(parents=True)
    write('protocol.json',dict(corpus=inputs,budgets=CAPS,corpus_bytes=size,shortlist=[1,2,4],
        source='original72-F40-A10/E02/H17',architecture_label='ASSUMED minimum distance3 rotated patches',
        physical_cap=10000000,physical_qubits_per_logical_patch=17,K=18,nu_per_basis=512,
        statistical_dollars=[9,2000],statistical_alpha=[3,1000],RMSE_dollars=[1,4096],
        stop='First impossible bare-memory cap; one fixed invocation; no full latency admission',
        no_scientific_samples=True,no_benchmarks=True,no_source_changes=True))
    print(json.dumps(dict(prepared=True,files=len(inputs),bytes=size,protocol_sha256=sha((OUT/'protocol.json').read_bytes()))))

def run():
    if (OUT/'ATTEMPT.json').exists():raise ValueError('One invocation only')
    p=json.loads((OUT/'protocol.json').read_text());cpu=time.process_time();wall=time.monotonic()
    write('ATTEMPT.json',dict(status='STARTED',kind='fixed_metadata_accounting'))
    try:
        if p['budgets']!=CAPS or [r['path'] for r in p['corpus']]!=INPUTS:raise ValueError('Protocol changed')
        for r in p['corpus']:
            raw=(ROOT/r['path']).read_bytes()
            if len(raw)!=r['bytes'] or sha(raw)!=r['sha256']:raise ValueError('Frozen input changed')
        s=load(CASE+'/source.json');c=load(CASE+'/schedule_capped.json');it=load(ITERATE);h=load(H17);e21=load(E21)
        if sha((ROOT/(CASE+'/target.json')).read_bytes())!=TARGET:raise ValueError('Wrong original target')
        for rec in (h,it):
            if rec['binding']['hashes']['target.json']!=TARGET:raise ValueError('Wrong source attachment')
            for name in ('source.json','schedule_capped.json'):
                if rec['binding']['hashes'][name]!=sha((ROOT/(CASE+'/'+name)).read_bytes()):raise ValueError('Source binding changed')
        if s['word_width']!=72 or s['fraction_bits']!=40 or not s['exact_clifford_t']:raise ValueError('Contract changed')
        n=c['resources']['logical_qubits']
        if n!=550141 or it['resources']['logical_qubits']!=n or h['logical_qubits']!=n:raise ValueError('Lane allocation mismatch')
        if it['binding']['dollar_span']!=64 or it['second_discount_applied']:raise ValueError('Dollar mapping changed')
        if e21['statistical_error_dollars_exact']!=[9,2000] or e21['failure_allowance_exact']!=[3,1000]:raise ValueError('E21 allowance changed')
        # Fully rational conditional confidence certificate.
        epsilon=F(9,2000);alpha=F(3,1000);rmse=F(1,4096)
        failure=rmse**2/epsilon**2
        if failure>=alpha:raise ValueError('RMSE conversion does not fit alpha')
        partial=sum(F(7,10)**j/F(factorial(j)) for j in range(5))
        if partial<=2 or F(2)*512*F(7,40)**2<=44*F(7,10):raise ValueError('Exponential bound premises failed')
        phase_mse=F(44,21)**2*(F(1,4**18)+F(256,3)*F(1,2**44))
        amplitude_mse=phase_mse/16
        if amplitude_mse>=F(1,262144)**2:raise ValueError('Conditional finite RPE MSE failed')
        controls=dict(P2_one_source_memory_reuse_rejected=2*(n+1)!=n+1,
                      RMSE_equals_e_rejected=epsilon**2/epsilon**2>alpha,
                      missing_physical_inputs_rejected=not h['parameterized_runtime_interface']['all_parameters_supplied'])
        if not all(controls.values()):raise ValueError('Accounting control failed')
        rows=[];stopped=False
        for P in p['shortlist']:
            footprint=P*(n+1)*17
            if stopped:
                rows.append(dict(P=P,status='NOT_EXECUTED_STOP_RULE',monotonic_bare_memory_rejection_inference=True,
                                 bare_footprint_if_reserved=footprint,physical_admitted=False))
                continue
            fits=footprint<=10000000
            stages=[]
            for k in (range(1,19) if fits else ()):
                Pk=min(P,2**(k-1));Tk=F(2**(k-1),Pk)
                stages.append(dict(k=k,Pk=Pk,Tk=exact(Tk),fresh_trials=1024,
                    GHZ_H=1024,GHZ_CX=1024*(Pk-1),GHZ_CX_tree_depth=(Pk-1).bit_length(),
                    local_probe_readouts=1024*Pk,sine_probe_basis_rotations=512,
                    QSP_conversion_norm_tolerance=exact(F(1,16*P)),
                    QSP_synthesis_norm_tolerance=exact(F(1,16*P)),
                    finite_QSP_degree_L=None,source_and_inverse_calls=None,
                    source_calls_per_V_symbolic='L_k+2 combined Ua/Ua_inverse queries; finite L/split unresolved'))
            rows.append(dict(P=P,status='BARE_MEMORY_PASSES_NECESSARY_ONLY' if fits else 'BARE_MEMORY_REJECTED_ASSUMED_ARCHITECTURE',
                lane_source_qubits=P*n,GHZ_QSP_probes=P,total_logical_bare=P*(n+1),
                bare_physical_qubits=footprint,bare_memory_headroom=10000000-footprint,
                rotated_patch_distance=3,distance_is_fidelity_certified=False,
                synthesis_workspace=None,factory_qubits=None,routing_qubits=None,
                finite_QSP_angles=None,controlled_reflection_gate_compatibility=None,
                complete_preparation_and_readout_cost=None,physical_latency_seconds=None,
                complete_failure_upper=None,physical_admitted=False,stages=stages,
                simultaneous_source_workspace_paid=True,serial_time_divided_by_P=False))
            if not fits:stopped=True
        certificate=dict(statistical_error_dollars=exact(epsilon),alpha=exact(alpha),RMSE_dollars=exact(rmse),
            exact_squared_error_failure_upper=exact(failure),phase_MSE_upper=exact(phase_mse),
            amplitude_MSE_upper=exact(amplitude_mse),conditional_probability_bias_beta=[1,8],
            finite_QSP_bias_premises_proved_by_compilation=False,original_continuous_bias_covered=False,
            hardware_allowance_and_obligations=h['failure_requirements'])
        summary=dict(status='PASS_NECESSARY_ACCOUNTING_ONLY_E20_TRANSFER_UNRESOLVED',rows=rows,
            certificate=certificate,controls=controls,stop_trigger='P2 bare capacity rejection',
            physical_architectures_adopted=0,finite_entangled_AE_circuits_compiled=0,
            quantum_speedup_claimed=False,new_financial_replays=0,matched_timings=0,
            source_logical_query_depth_is_physical_latency=False)
        if time.process_time()-cpu>CAPS['cpu_seconds'] or time.monotonic()-wall>CAPS['wall_seconds']:raise ValueError('Budget cap')
        write('summary.json',summary);write('SUCCESS.json',dict(status=summary['status'],complete_E20_acceptance=False))
        files=[x for x in OUT.iterdir() if x.is_file()]
        if len(files)+1>CAPS['output_files']:raise ValueError('Output file cap')
        manifest=dict(files=[dict(path=x.name,bytes=x.stat().st_size,sha256=sha(x.read_bytes())) for x in sorted(files)])
        if sum(x.stat().st_size for x in files)+len(json.dumps(manifest).encode())>CAPS['output_bytes']:raise ValueError('Output cap')
        write('manifest.json',manifest)
        print(json.dumps(dict(status=summary['status'],P1_bare=rows[0]['bare_physical_qubits'],P2_bare=rows[1]['bare_physical_qubits'],
                              summary_sha256=sha((OUT/'summary.json').read_bytes()))))
    except BaseException as exc:
        if not (OUT/'FAILED.json').exists():write('FAILED.json',dict(status='FAILED_PRESERVED',error=str(exc)))
        raise

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('mode',choices=['prepare','run']);args=a.parse_args()
    prepare() if args.mode=='prepare' else run()
