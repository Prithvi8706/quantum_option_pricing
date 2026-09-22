"""Cost the explicit nonlinear hierarchy; expose omitted costs and ideal cases."""
import argparse
import json
import math
from pathlib import Path
import time
from .model import MODELS,choose_cap,outer_target_second_moment_bound
from .quantum_schedule import nested_schedule
from research.antithetic_feasibility.cost_model import constant_cost,physical_scenario


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    root=Path('results/compound_feasibility');old=Path('results/antithetic_feasibility');start=time.perf_counter()
    compiled=json.loads((root/'compiled_v1/blocks.json').read_text());base=json.loads((old/'compiled_blocks_v1/blocks.json').read_text())
    loaders=json.loads((old/'compiled_blocks_v1/loaders.json').read_text());loader=next(x for x in loaders if x['qubits']==10)
    costs=[];schedules=[];oracles=[]
    for m in MODELS:
        cap,tail=choose_cap(m)
        for f in (24,32):
            w=f+16;block={r['block']:r for r in base if r['fraction_bits']==f}
            step=next(r for r in compiled if r['case']==m.name and r['fraction_bits']==f and r['block']=='gbm_step')
            payoff=next(r for r in compiled if r['case']==m.name and r['fraction_bits']==f and r['block']=='capped_payoff')
            n=m.dates//2;count=n*m.assets;average=constant_cost(w,f,1/(m.assets*m.dates))
            # Weight each fixing before accumulating, avoiding an unnecessary
            # d*dates-sized intermediate sum in the fixed-point range.
            tx=count*(step['t_count']+block['exp']['t_count']+block['add']['t_count']+average['t_count'])
            dx=count*(step['t_depth']+block['exp']['t_depth']+block['add']['t_depth']+average['t_depth_serial'])
            ty=tx+payoff['t_count']+block['compare']['t_count'];dy=dx+payoff['t_depth']+block['compare']['t_depth']
            rotations=(m.assets+1)*n*loader['arbitrary_rotation_upper_count']
            source_qubits=(m.assets+1)*n*10+3*count*w+block['exp']['qubits']+step['qubits']+payoff['qubits']+4*w
            oracle=dict(case=m.name,fraction_bits=f,genX_T=tx,genX_serial_T_depth=dx,genY_payoff_T=ty,genY_payoff_serial_T_depth=dy,
                        gaussian_arbitrary_rotation_upper_per_source=rotations,source_workspace_envelope=source_qubits,
                        status='Gate-derived serial macro with explicit cap and digital selector. q10 loading not certified sufficient; exp reused from earlier compiled blocks; full coherent finance circuit not emitted.')
            oracles.append(oracle)
            for eps in (.1,.03,.01):
                choices=[]
                for normalizer in sorted(set([1.,16.,cap])):
                    s=nested_schedule(cap,eps,normalizer=normalizer,target_second_moment=outer_target_second_moment_bound(m))
                    # Favorable paper-hierarchy coordinate: unit constants, no logarithms,
                    # no confidence amplification/inverse multiplier/decoder costs.
                    bound=cap/normalizer;e=s['eta']/(2*(s['last_level']+1));ideal_calls=0
                    for l in range(s['last_level']+1):
                        inner=math.ceil(bound*2**(l+1));prev=math.ceil(bound*2**l) if l else 0
                        base_sigma=min(bound,math.sqrt(outer_target_second_moment_bound(m))/normalizer+math.sqrt(3/8))
                        outer=math.ceil((base_sigma if l==0 else min(bound,math.sqrt(10)*2**(-l)))/e)
                        ideal_calls+=outer*(inner+prev)
                    s['ideal_unit_constant_no_log_conditional_calls']=ideal_calls
                    s['case']=m.name;choices.append(s)
                    if f==32:schedules.append(s)
                best=min(choices,key=lambda s:s['conditional_primitive_and_inverse_calls'])
                ideal=min(s['ideal_unit_constant_no_log_conditional_calls'] for s in choices)
                ny=best['conditional_primitive_and_inverse_calls'];nx=best['outer_state_and_inverse_calls'];nt=ny*ty+nx*tx;td=ny*dy+nx*dx
                # Straight independent coherent medians retain their QAE target registers.
                max_copies=max(r['inner']['repetitions']+(r['previous_inner']['repetitions'] if r['previous_inner'] else 0) for r in best['rows'])
                logical=source_qubits*(1+max_copies)+2*sum(r['inner']['qpe_output_bits'] for r in best['rows'])
                row=dict(case=m.name,fraction_bits=f,epsilon=eps,cap=cap,tail_bound=tail,target_second_moment_bound=outer_target_second_moment_bound(m),selected_normalizer=best['normalizer'],last_level=best['last_level'],
                         conditional_source_and_inverse_calls=ny,outer_source_and_inverse_calls=nx,
                         arithmetic_T_subtotal=nt,serial_arithmetic_T_depth_subtotal=td,
                         seconds_subtotal_at_100ns=td*1e-7,
                         gaussian_arbitrary_rotation_upper_count=(ny+nx)*rotations,
                         ideal_conditional_calls_no_constants_logs=ideal,
                         ideal_one_multiply_seconds_at_100ns=ideal*block['multiply']['t_depth']*1e-7,
                         ideal_one_layer_seconds_at_100ns=ideal*1e-7,
                         logical_retained_copies_envelope=logical,
                         physical_sensitivity_10m={str(p):physical_scenario(nt,td,logical,p=p) for p in (1e-3,1e-4)},
                         omissions=['QPE value-to-fixed-point decoder, coherent median sorting and outer signed-bin assembly not compiled.',
                                    'Reflection gates, QFT/loader rotation synthesis, Clifford/measurement/decoding/setup latency excluded from arithmetic subtotal.',
                                    'Finite input and arithmetic/overflow bridges not certified; quantum geometric-control circuit not implemented.',
                                    'Unit-constant coordinate is not an algorithm or a lower bound on all quantum estimators.'])
                costs.append(row);print(json.dumps({k:v for k,v in row.items() if k not in ('omissions','physical_sensitivity_10m')}),flush=True)
    for name,data in [('costs',costs),('schedules',schedules),('oracles',oracles)]:
        (out/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
    (out/'complete.json').write_text(json.dumps(dict(seconds=time.perf_counter()-start),indent=2))


if __name__=='__main__':run()
