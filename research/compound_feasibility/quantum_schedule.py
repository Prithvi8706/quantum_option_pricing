"""Explicit quantum-inner hierarchy, with all primitive/inverse invocations.

Bounded normalized inner values in [0,1]. Outer signed mean estimation uses
the explicit dyadic construction, not unknown Kothari--O'Donnell constants.
This is a schedule/resource model, not a compiled coherent QPE/median program.
"""
import math
import numpy as np
from scipy.stats import binom
from research.antithetic_feasibility.estimator import schedule,power_two_at_least,median_repetitions,qae_distribution


def inner_schedule(level,bound=1.):
    error=2.**(-level-1);delta=2.**(-2*level-3)/bound**2
    # Worst-case bounded AE: pi/M + pi^2/M^2 <= error.
    M=power_two_at_least((bound*math.pi+math.sqrt((bound*math.pi)**2+4*error*bound*math.pi**2))/(2*error))
    repetitions=median_repetitions(delta);bits=M.bit_length()-1
    return dict(level=level,bound=bound,error=error,delta=delta,M=M,repetitions=repetitions,
                primitive_and_inverse_calls=repetitions*(2*M-1),grover_iterates=repetitions*(M-1),
                qft_controlled_rotations=repetitions*bits*(bits-1)//2,qpe_output_bits=repetitions*bits,
                mse_bound=error**2+delta*bound**2,
                coherent_median_comparator_upper_count=repetitions*(repetitions-1)//2,
                status='Independent QPE copies, value decoding, coherent median and clipping required; gate synthesis of decoder/median open.')


def nested_schedule(cap,epsilon,delta=.004,normalizer=None,target_second_moment=None):
    # .8epsilon allocated to numerical inner+outer statistics; remainder for tails/arithmetic/loading.
    normalizer=cap if normalizer is None else normalizer
    bound=cap/normalizer
    eta=.8*epsilon/normalizer;L=math.ceil(math.log2(2/eta));e=eta/(2*(L+1))
    rows=[];total_y=0;total_x=0
    for level in range(L+1):
        inner=inner_schedule(level,bound);previous=inner_schedule(level-1,bound) if level else None
        # A0 in [0,1]; delta_l has second moment <=10*4^-l and magnitude<=1.
        base_moment=bound**2 if target_second_moment is None else min(bound**2,(math.sqrt(target_second_moment)/normalizer+math.sqrt(3/8))**2)
        moment=base_moment if level==0 else min(bound**2,10*2.**(-2*level))
        outer=schedule(moment,e,delta/(L+1),max_magnitude=bound)
        calls_b=inner['primitive_and_inverse_calls']+(previous['primitive_and_inverse_calls'] if previous else 0)
        y=outer['calls_A']*calls_b;total_y+=y;total_x+=outer['calls_A']
        rows.append(dict(level=level,inner=inner,previous_inner=previous,outer=outer,conditional_primitive_and_inverse_calls=y,
                         outer_state_and_inverse_calls=outer['calls_A']))
    return dict(cap=cap,normalizer=normalizer,target_second_moment_bound=target_second_moment,epsilon=epsilon,eta=eta,last_level=L,rows=rows,
                conditional_primitive_and_inverse_calls=total_y,outer_state_and_inverse_calls=total_x,
                normalized_bias_bound=2.**(-L),normalized_statistical_error_bound=sum(r['outer']['total_error_bound'] for r in rows),
                dollar_bound=normalizer*(2.**(-L)+sum(r['outer']['total_error_bound'] for r in rows)),statistical_failure=delta,
                interpretation='Explicit bounded quantum-inner hierarchy plus explicit signed outer estimator. Not a fault-tolerant compiled pricing algorithm; not an optimal query lower bound.')


def exact_inner_distribution(p,strike,level):
    s=inner_schedule(level);values,prob=qae_distribution(p,s['M'])
    # Aggregate duplicate sin^2 values before applying order statistics.
    rounded=np.round(values,13);v,inv=np.unique(rounded,return_inverse=True);mass=np.bincount(inv,weights=prob)
    cdf=np.minimum(np.cumsum(mass),1.);r=s['repetitions'];medcdf=binom.sf(r//2,r,cdf)
    weights=np.diff(np.r_[0.,medcdf]);return np.maximum(v-strike,0.),weights
