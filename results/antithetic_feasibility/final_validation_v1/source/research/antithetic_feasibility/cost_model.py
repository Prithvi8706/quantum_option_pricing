"""Source-bound macro composition and explicit estimator/physical sensitivity.

Gate-emitted block counts are real; macro depth is a declared serial-block
schedule. Arbitrary-rotation synthesis and the financial certificate remain
open. Nothing in this module establishes a best-algorithm lower bound.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np
from .classical import MODELS
from .estimator import schedule
from .bin_oracle import bin_program
from .reversible import clifford_t_resources


ROOT=Path('results/antithetic_feasibility')


def constant_cost(w,f,c):
    value=abs(round(c*2**f))
    lengths=[2*w-i for i in range(value.bit_length()) if (value>>i)&1]
    # Each Cuccaro add has 2n Toffoli, then the product is uncomputed.
    return dict(t_count=28*sum(lengths),t_depth_serial=16*sum(lengths))


def step_cost(blocks,w,f,h,m):
    constants=[-.5*h,m.xi/4,m.xi,m.xi*m.xi/4,1/(1+m.kappa*h)]
    cs=[constant_cost(w,f,c) for c in constants]
    tc=2*(blocks['sqrt']['t_count']+4*blocks['multiply']['t_count']+sum(x['t_count'] for x in cs)+7*blocks['add']['t_count'])
    td=2*(blocks['sqrt']['t_depth']+4*blocks['multiply']['t_depth']+sum(x['t_depth_serial'] for x in cs)+7*blocks['add']['t_depth'])
    return dict(t_count=tc,t_depth_serial=td,constants=constants)


def oracle_plan(m,level,f,q,blocks,loader):
    w=f+16;n=m.dates*2**level;dim=2*m.assets+1
    entries=[]
    def item(name,multiplicity,tc,td,detail=''):
        entries.append(dict(name=name,multiplicity=multiplicity,t_count_each=int(tc),t_depth_serial_each=int(td),detail=detail))
    add=blocks['add'];exp=blocks['exp'];cmp=blocks['compare'];pos=blocks['positive']
    haar=constant_cost(w,f,1/math.sqrt(2))
    item('Haar add/subtract',2*dim*(n-m.dates),add['t_count'],add['t_depth'])
    item('Haar child scaling',2*dim*(n-m.dates),haar['t_count'],haar['t_depth_serial'])
    paths=[('base',n,1)] if level==0 else [('fine_and_swapped',n,2),('coarse',n//2,1)]
    stored_states=0
    for name,steps,multiplicity in paths:
        h=m.maturity/steps;sc=step_cost(blocks,w,f,h,m)
        item(name+'_state_update',multiplicity*steps*m.assets,sc['t_count'],sc['t_depth_serial'])
        item(name+'_monitor_exp',multiplicity*m.dates*m.assets,exp['t_count'],exp['t_depth'])
        item(name+'_accumulate',multiplicity*m.dates*m.assets,add['t_count'],add['t_depth'])
        stored_states+=multiplicity*((steps+1)*2*m.assets*w+m.dates*m.assets*w)
    # Fine/swapped share increments. Coarse uses retained parent Haar coordinates.
    for steps in ([n] if level==0 else [n,n//2]):
        h=m.maturity/steps
        cs=[math.sqrt(h*m.correlation),math.sqrt(h*(1-m.correlation)),m.leverage,math.sqrt(h*(1-m.leverage**2))]
        tc=sum(constant_cost(w,f,c)['t_count'] for c in cs)+2*add['t_count']
        td=sum(constant_cost(w,f,c)['t_depth_serial'] for c in cs)+2*add['t_depth']
        item('Brownian_correlation_and_scale',steps*m.assets,tc,td)
    if level==0:
        # Geometric GBM log control: weighted Brownian sum, exp and positive part.
        # Compute/add/uncompute each term to reuse its workspace.
        for j in range(n):
            dates_remaining=m.dates-j//(2**level)
            c=math.sqrt(m.theta)*dates_remaining/(m.dates*m.assets)
            cc=constant_cost(w,f,c)
            item('geometric_control_weight',m.assets,2*cc['t_count']+add['t_count'],2*cc['t_depth_serial']+add['t_depth'])
        item('geometric_control_exp',1,exp['t_count'],exp['t_depth'])
        # Charge a general multiplication for fitted control coefficient.
        item('control_coefficient',1,blocks['multiply']['t_count'],blocks['multiply']['t_depth'])
    # Division by asset/date count and discount use constant arithmetic.
    divisor=constant_cost(w,f,1/(m.assets*m.dates));disc=constant_cost(w,f,math.exp(-m.rate*m.maturity))
    item('average_and_discount',1 if level==0 else 3,divisor['t_count']+disc['t_count'],divisor['t_depth_serial']+disc['t_depth_serial'])
    item('payoff_cap_and_signed_combination',1,8*cmp['t_count']+12*add['t_count']+4*pos['t_count'],
         8*cmp['t_depth']+12*add['t_depth']+4*pos['t_depth'],
         'declared serial block envelope; cap/overflow financial bridge still open')
    binp,_,_=bin_program(w,w,2**(w-3),2**(w-2),1)
    br=clifford_t_resources(binp)
    item('signed_bin_selector',1,br['t_count'],br['t_depth'])
    noise_qubits=dim*n*q
    # A time-for-space choice: retain parent/child words and path states;
    # step scratch is reused across all updates, not reallocated per step.
    stored_haar=(2*n-m.dates)*dim*w
    correlation_words=(n+(n//2 if level else 0))*m.assets*2*w
    logical=noise_qubits+stored_haar+correlation_words+stored_states+blocks['step_h_1_12']['qubits']+br['qubits']+10*w
    return dict(case=m.name,level=level,fraction_bits=f,normal_bits=q,entries=entries,
                f_t_count=sum(x['multiplicity']*x['t_count_each'] for x in entries),
                f_t_depth_serial=sum(x['multiplicity']*x['t_depth_serial_each'] for x in entries),
                logical_qubits_stored_history=logical,input_qubits=noise_qubits,
                gaussian_preparations=dim*n,loader_u=dim*n*loader['counts']['u'],
                loader_cx=dim*n*loader['counts']['cx'],loader_arbitrary_rotation_upper_count=dim*n*loader['arbitrary_rotation_upper_count'],
                reflection_t_count=14*(noise_qubits+w+1),reflection_t_depth_serial=8*(noise_qubits+w+1),
                sqrt_only_serial_depth_one_path=n*blocks['sqrt']['t_depth'],
                status='hierarchical macro composition from gate-emitted blocks; not emitted monolithic price circuit or financial certificate')


def physical_scenario(nt,td,logical,p=1e-3,cycle=1e-6,cap=10_000_000):
    """Litinski Eq10/Fig19 sensitivity; approximate code fit, no placed layout."""
    magic_p=35*(35*p**3)**3
    if nt*magic_p>.0025:return dict(feasible=False,reason='two-level distillation fidelity insufficient',magic_failure=nt*magic_p)
    # At least one 176-tile two-level factory; 2x data tiles for routing reserve.
    for distance in range(5,102,2):
        data_tiles=2*logical
        fmax=(cap//(2*distance**2)-data_tiles)//176
        if fmax<1:
            # Higher distances only consume more physical qubits.
            return dict(feasible=False,reason='data and one factory exceed physical cap before failure condition is met',distance=distance,
                        minimum_physical_qubits=(data_tiles+176)*2*distance**2)
        for factories in sorted(set([1,int(fmax)])):
            tiles=data_tiles+176*factories
            # Fig19: 15d cycles/output; 20% throughput derating is an assumption.
            cycles=max(td*distance,nt*15*distance/(.8*factories))
            pl=.1*(100*p)**((distance+1)/2)
            fail=tiles*cycles*pl+nt*magic_p
            if fail<=.005:
                return dict(feasible=True,distance=distance,factories=factories,physical_qubits=tiles*2*distance**2,
                            seconds=cycles*cycle,model_failure_bound=fail,
                            status='approximate architecture sensitivity, not validated routing/decoder/factory certificate')
    return dict(feasible=False,reason='no distance in declared search')


def run():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.perf_counter()
    raw=json.loads((ROOT/'compiled_blocks_v1/blocks.json').read_text())
    loaders=json.loads((ROOT/'compiled_blocks_v1/loaders.json').read_text());loader=next(x for x in loaders if x['qubits']==10)
    bp=json.loads((ROOT/'classical_prices_v1/summaries.json').read_text())
    cp=json.loads((ROOT/'classical_corrections_v1/summaries.json').read_text())
    alloracles=[];results=[]
    for f in (24,32):
        blocks={r['block']:r for r in raw if r['fraction_bits']==f}
        # Exact operation-count identity independently binds the macro formula.
        for h,key in [(1/12,'step_h_1_12'),(1/24,'step_h_1_24')]:
            assert step_cost(blocks,f+16,f,h,MODELS[1])['t_count']==blocks[key]['t_count']
        for model in MODELS[:2]:
            plans=[oracle_plan(model,l,f,10,blocks,loader) for l in range(6)];alloracles+=plans
            sigmas=[];centers=[]
            for l in range(6):
                r=next(r for r in (bp if l==0 else cp) if r['case']==model.name and r['level']==l and r['method']=='mc' and not r['conditional'] and r['power']==(12 if l==0 else 10))
                # Conditional assumption: 4x pilot variance bounds centered moment.
                sigmas.append(2*math.sqrt(r['sample_variance']+(r['mean']**2 if l else 0.)))
                centers.append(r['mean'] if l==0 else 0.)
            for eps in (.1,.03,.01):
                weights=np.sqrt(np.array([p['f_t_depth_serial'] for p in plans])*sigmas)
                allocations=.45*eps*weights/weights.sum()
                schedules=[schedule(s*s,float(e),.004/6,max_magnitude=1024.,center=c) for s,e,c in zip(sigmas,allocations,centers)]
                nt=0;td=0;rot=0;max_serial=0;calls=0
                for p,s in zip(plans,schedules):
                    ca=s['calls_A'];g=s['grover_iterates'];calls+=ca
                    nt+=ca*p['f_t_count']+g*p['reflection_t_count']
                    td+=ca*p['f_t_depth_serial']+g*p['reflection_t_depth_serial']
                    rot+=ca*p['loader_arbitrary_rotation_upper_count']+3*s['qft_controlled_rotations']
                    for b in s['bins']:
                        # Even unlimited simultaneous medians/bins leave this QPE depth.
                        max_serial=max(max_serial,(2*b['M']-1)*p['f_t_depth_serial']+(b['M']-1)*p['reflection_t_depth_serial'])
                ideal_weights=np.sqrt(np.array([p['sqrt_only_serial_depth_one_path'] for p in plans])*np.array(sigmas)/2)
                ideal_depth=float(ideal_weights.sum()**2/(.45*eps))
                r=dict(case=model.name,fraction_bits=f,epsilon=eps,allocations=allocations.tolist(),
                       assumed_sigma_bounds=sigmas,schedules=schedules,source_invocations=calls,
                       t_count_excluding_rotation_synthesis=nt,t_depth_serial_blocks_excluding_rotations=td,
                       arbitrary_rotation_upper_count=rot,max_single_qpe_t_depth_serial_blocks=max_serial,
                       peak_logical_qubits_stored_history=max(p['logical_qubits_stored_history'] for p in plans),
                       ideal_sigma_over_epsilon_sqrt_only_depth=ideal_depth,
                       depth_seconds_at_layer_times={str(t):td*t for t in (1e-7,1e-6,1e-5)},
                       fully_parallel_bins_seconds_at_100ns=max_serial*1e-7,
                       physical_10m_cap={str(p):physical_scenario(nt,td,max(x['logical_qubits_stored_history'] for x in plans),p=p) for p in (1e-3,1e-4)},
                       unknowns=['Second-moment bounds not proved for finite circuit law.','Full domain/overflow/error certificate open.',
                                 'Arbitrary-rotation T synthesis and physical routing/decoding not completed.',
                                 'Finite-law quantum target differs from Gaussian floating reference until bridge certified.'],
                       interpretation='Concrete estimator cost screen. Favorable sqrt-only coordinate is NOT an algorithm or lower bound on all algorithms.')
                results.append(r)
                print(json.dumps({k:v for k,v in r.items() if k not in ('schedules','unknowns')}),flush=True)
    (out/'oracle_plans.json').write_text(json.dumps(alloracles,indent=2)+'\n')
    (out/'costs.json').write_text(json.dumps(results,indent=2)+'\n')
    (out/'complete.json').write_text(json.dumps(dict(seconds=time.perf_counter()-start,source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')}),indent=2))


if __name__=='__main__':run()
