"""Complete logical-envelope accounting and explicitly incomplete physical costs."""
import json
import math
from pathlib import Path
from research.controlled_source_completion.modern_mean import plan
from research.controlled_source_completion.compiler import envelope
from research.controlled_source_completion.run import ROOT,dump
from research.controlled_source_completion.envelope import inverse_qft,controlled_U


def phase_error_bound(f):
    # atan Taylor on segments of half-width 1/64. For n>=1, |a_n|<=1/n
    # from the two complex log expansions; sum_{n>=9} h^n/n <=h^9/(9(1-h)).
    # 32 ulps generously covers coefficient/Horner/reciprocal/shift/constant
    # rounding. The float pi constant has an additional <=2e-16 phase error.
    h=1/64
    return 32*2**-f+2*h**9/(9*(1-h))+2e-16


def circuit_recipe(source,phase,allocation,path,fused=False):
    f=phase['fraction_bits'];w=source['word_width'];stages=[]
    for row in allocation['stages']:
        b=row['qpe_bits']
        stages.append(dict(**row,
            initial_state=['H on each random bit','H on each QPE bit','X-load rounded left endpoint and log2(normalizer)'],
            powers=[dict(control=j,repetitions_of_controlled_U=2**j) for j in range(b)],
            inverse_qft=dict(h=b,controlled_phase_angles=[dict(target=j,control=k,angle=-math.pi/(2**(k-j)),angle_exact_pi_multiple=[-1,2**(k-j)]) for j in range(b) for k in range(j+1,b)],
                             swaps=b//2,note='Standard inverse QFT; interpret measured bit order consistently with swaps.'),
            inverse_qft_ordered_operations=inverse_qft(list(range(b))),
            reset_between_repetitions='Reset all random-input and QPE qubits to zero; uncompute classical left/exponent loads. Arithmetic work is already clean.',
            measurement=dict(bits=b,decision='Fold phase to [0,pi], compare with threshold_abs_phase, take majority.',
                             update='If large: left += width/4. In either outcome: width *= 3/4.'),
            initial_classical_left='-sqrt(moment)' if row['stage']==0 else 'adaptive previous-stage left'))
    spec=dict(format='controlled-source-qpe-envelope-v1',source_manifest=source['path'],phase_manifest=phase['path'],
        fused_compute_phase_uncompute=fused,
        fused_override='When fused=true, replace each clean source/angle call below by only its graph forward pass or inverse. Read Y and angle from their SSA words. Redundant internal cleanup and separate output copies are cancelled. The controlled_U_gates artifact is authoritative.',
        U_operations=[
            'Execute clean source Y (uncontrolled)',
            'CX-copy Y into phase input, shifted by phase_fraction_bits-source_fraction_bits; then execute clean angle=-2*atan((Y-left)/normalizer) (uncontrolled)',
            'For angle bits j=0..f+2 apply CP(2**(j-f)) to QPE control and angle bit; signed top bit uses -2**2',
            'Execute inverse angle source and uncopy its Y input',
            'Execute inverse Y source',
            'H on random bits; X on random bits; controlled multi-Z on QPE control and all random bits; X,H on random bits; Z on QPE control'],
        phase_bits=[dict(bit=j,radians=(-1 if j==f+2 else 1)*2.**(j-f),
                        angle_exact_radians=[(-1 if j==f+2 else 1)*2**max(0,j-f),2**max(0,f-j)]) for j in range(f+3)],
        controlled_phase_decomposition='P(theta/2) on control and target; CX(control,target); P(-theta/2) on target; CX(control,target). Each P may be synthesized as Rz up to an overall global phase.',
        reflection_decomposition='Clean AND ladder across all random bits; CZ(AND,QPE control); inverse ladder; Z(QPE control) supplies required reflection sign.',
        qpe_stages=stages,allocation=allocation,
        declared_status='Executable hierarchical arithmetic and explicit repetition/gate recipe. Arbitrary single-qubit phase rotations remain unsynthesized; no all-Clifford+T or fault-tolerant execution claim.')
    dump(path,spec)


def main(revision='v1',phase_fraction=None,fused=False):
    certificates=json.loads(Path('results/controlled_residual_feasibility/parity_iid_v1/summaries.json').read_text())
    rows=[]
    costdir=('cost_v3' if fused else 'cost_'+revision)+('_phase%d'%phase_fraction if phase_fraction else '')
    for f in (24,40):
        pf=phase_fraction or f
        phase=json.loads((ROOT/('compile_'+revision)/('phase_f%d'%pf)/'source.json').read_text());phase['path']=str((ROOT/('compile_'+revision)/('phase_f%d'%pf)/'source.json').resolve())
        for name in ('C4','H8'):
            source=json.loads((ROOT/('compile_'+revision)/('%s_f%d'%(name,f))/'source.json').read_text());source['path']=str((ROOT/('compile_'+revision)/('%s_f%d'%(name,f))/'source.json').resolve())
            wrapper=controlled_U(source,phase,fused);dump(ROOT/costdir/('%s_f%d_controlled_U_gates.json'%(name,f)),wrapper)
            cert=next(c for c in certificates if c['case']==name and c['strike']==6)
            discount=math.exp(-.03*(.5 if name=='C4' else 1.5));support=round(100*discount*2**f)/2**f
            classical={'C4':11.1059177,'H8':13.847206}[name]
            for mode,moment in (('continuous_moment_conditional',cert['second_moment_upper']),('digital_support_bound',math.nextafter(support**2,math.inf))):
                # Preserve .004 total QE failure: .003 ideal tests, .0005 coherent
                # function approximation, .0005 rotation synthesis. Physical .002 separate.
                allocation=plan(moment,.002/discount,.003);last=allocation['stages'][-1];one=envelope(source,phase,last,fused)
                calls=allocation['controlled_U_calls'];qfts=sum(s['inverse_qft_controlled_rotations'] for s in allocation['stages'])
                bitphases=calls*one['controlled_bit_phases'];allcp=bitphases+qfts
                qft_exact_cp=sum(s['repetitions']*(s['qpe_bits']-1) for s in allocation['stages'])
                single_rotations=3*(allcp-qft_exact_cp);rotation_epsilon=.0005/(2*single_rotations)
                approximation_epsilon=.0005/(2*calls)
                t_arithmetic=calls*one['t_count'];td_arithmetic=calls*one['t_depth']
                maxchain=max(s['M']-1 for s in allocation['stages'])*one['t_depth']
                # All failures here are output-distribution perturbation bounds,
                # not the unrelated absolute dollar error allocation.
                ledger=dict(logical_qubits=one['logical_qubits'],controlled_U_calls=calls,
                    clean_Y_source_or_inverse_calls=2*calls,clean_angle_source_or_inverse_calls=2*calls,
                    source_call_interpretation='Conceptual clean-oracle calls; compiler fuses cleanup so actual passes are one financial forward, one phase forward, and their inverses per U.' if fused else 'Separate complete clean-oracle calls',
                    actual_financial_graph_forward_and_inverse_passes=(2 if fused else 4)*calls,
                    actual_phase_graph_forward_and_inverse_passes=(2 if fused else 4)*calls,
                    arithmetic_t_count=t_arithmetic,serial_arithmetic_t_depth=td_arithmetic,
                    additional_exact_inverse_qft_t_count=3*qft_exact_cp,
                    additional_serial_exact_inverse_qft_t_depth=2*qft_exact_cp,
                    longest_single_qpe_arithmetic_t_depth=maxchain,
                    controlled_phase_gates=allcp,unsynthesized_single_qubit_phase_gates=single_rotations,
                    controlled_phase_decomposition_cx=2*allcp,
                    qpe_executions=allocation['qpe_executions'],
                    measured_bits=sum(s['repetitions']*s['qpe_bits'] for s in allocation['stages']),
                    random_input_qubit_resets=allocation['qpe_executions']*source['resources']['random_hadamards'],
                    qpe_qubit_resets=sum(s['repetitions']*s['qpe_bits'] for s in allocation['stages']),
                    uniform_preparation_h=allocation['qpe_executions']*source['resources']['random_hadamards'],
                    qpe_preparation_and_qft_h=2*sum(s['repetitions']*s['qpe_bits'] for s in allocation['stages']),
                    qft_swap_cx=3*sum(s['repetitions']*(s['qpe_bits']//2) for s in allocation['stages']),
                    classical_constant_load_and_unload_x_upper=4*phase['word_width']*allocation['qpe_executions'],
                    arithmetic_clifford_cx=calls*one['clifford_cx'],arithmetic_clifford_h=calls*one['clifford_h'],
                    arithmetic_x=calls*one['x'],reflection_control_z=calls,
                    required_each_rotation_operator_error=rotation_epsilon,
                    required_uniform_phase_function_error=approximation_epsilon,
                    conservative_phase_function_error_bound=phase_error_bound(pf),
                    phase_bound_closes=phase_error_bound(pf)<=approximation_epsilon,
                    synthesis_t_count='unknown: add N_R * t_synth(rotation_epsilon); N_R is charged above',
                    synthesis_t_depth='unknown: add depth of synthesized controlled phases and IQFT',
                    preprocessing_seconds=cert['seconds_with_training'] if mode.startswith('continuous') else 0.,
                    preprocessing_status='Existing continuous certificate costs; digital bridge unpriced' if mode.startswith('continuous') else 'Support moment needs no iid acquisition; same policy training, surrogate price and regret costs remain',
                    classical_decoding_and_feedback='Exact-rational interval controller implemented; runtime and device feedback latency unmeasured and must be added',
                    oracle_mean_contract_only=True)
                sensitivity=[]
                for ns in (1.,10.,100.,1000.):
                    seconds=td_arithmetic*ns*1e-9
                    sensitivity.append(dict(hypothetical_T_layer_ns=ns,serial_arithmetic_seconds=seconds,
                        longest_QPE_arithmetic_seconds=maxchain*ns*1e-9,
                        required_speedup_for_10x=seconds/(classical/10),
                        interpretation='Cost of this serial leaf schedule with non-T timing, synthesis, error correction, routing and setup omitted. Not a hardware runtime.'))
                row=dict(model=name,f=f,phase_fraction_bits=pf,mode=mode,moment=moment,financial_flat_error=.002,
                    classical_full_price_seconds=classical,tenfold_total_budget_seconds=classical/10,
                    single_U=one,ledger=ledger,sensitivity=sensitivity,
                    required_T_layer_seconds_for_10x=classical/(10*td_arithmetic),
                    required_magic_T_per_second_for_10x=t_arithmetic/(classical/10),
                    ideal_unit_constant_source_calls=math.ceil(math.sqrt(moment)/(.002/discount)),
                    ideal_unit_constant_source_seconds_100ns=math.ceil(math.sqrt(moment)/(.002/discount))*source['resources']['t_depth']*1e-7,
                    data_physical_qubits_sensitivity={str(d):2*d*d*one['logical_qubits'] for d in (15,25,35)},
                    physical_mapping_note='Illustrative 2d^2 data-patch formula only; code distances NOT validated, no routing/factories/spares. No physical crossover claimed.',
                    scope='Single Kc=6 flat correction only. Digital support is valid for the bounded implemented output; continuous moment transfer, surrogate price and exercise regret are separate obligations.')
                rows.append(row);tag='%s_f%d_%s'%(name,f,mode)
                dump(ROOT/costdir/(tag+'_schedule.json'),allocation)
                circuit_recipe(source,phase,allocation,ROOT/costdir/(tag+'_circuit.json'),fused)
    dump(ROOT/costdir/'ledger.json',rows)
    for row in rows:
        print(json.dumps(dict(model=row['model'],f=row['f'],mode=row['mode'],calls=row['ledger']['controlled_U_calls'],
            t_count=row['ledger']['arithmetic_t_count'],qubits=row['ledger']['logical_qubits'],
            seconds_100ns=row['sensitivity'][2]['serial_arithmetic_seconds'],
            longest_QPE_100ns=row['sensitivity'][2]['longest_QPE_arithmetic_seconds'],
            phase_epsilon=row['ledger']['required_uniform_phase_function_error'],phase_closes=row['ledger']['phase_bound_closes'])),flush=True)


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--revision',default='v1');p.add_argument('--phase-fraction',type=int);p.add_argument('--fused',action='store_true');a=p.parse_args();main(a.revision,a.phase_fraction,a.fused)
