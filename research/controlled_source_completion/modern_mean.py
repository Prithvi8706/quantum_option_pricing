"""Explicit known-second-moment Kothari--O'Donnell phase estimator.

Theorem3.19 plus a conservative interval contraction (Lemma4.3 mechanism).
This is not the unknown-variance/quantile reduction of the final theorem.
"""
import math
from fractions import Fraction
import numpy as np
from scipy.stats import binom


def pow2(x):return 2**max(0,math.ceil(math.log2(max(1.,x))))


def repetitions(delta):
    r=1
    while binom.sf(r//2,r,1/3)>delta:r+=2
    return r


def plan(moment,error,failure=.004,endpoint_bits=64):
    if moment<0 or error<=0 or not 0<failure<1:raise ValueError('invalid contract')
    m=Fraction(float(moment));scaled=m*(1<<(2*endpoint_bits));root=math.isqrt(scaled.numerator//scaled.denominator)
    if root*root*scaled.denominator<scaled.numerator:root+=1
    exact_s=Fraction(root,1<<endpoint_bits);s=float(exact_s)
    if exact_s<=Fraction(float(error)):return dict(moment=moment,error=error,initial_radius=s,stages=[],controlled_U_calls=0,
                           value_evaluations_and_inverses=0,interpretation='Return zero from the supplied moment bound.')
    # |left|<=s at every stage, so ||(Y-left)/norm||_2 <=2s/norm<=1/16.
    norm=pow2(32*s)
    while Fraction(norm)<32*exact_s:norm*=2
    count=0;exact_width=2*exact_s
    while exact_width/2>Fraction(float(error)):count+=1;exact_width*=Fraction(3,4)
    exact_width=2*exact_s;rows=[]
    for j in range(count):
        width=float(exact_width)
        epsilon=width/(2*norm);phase_error=epsilon/6
        # Conservative Fejer-kernel tail: >9 grid cells has probability <1/9.
        # M >= 20pi/phase_error leaves ten cells of angular tolerance.
        M=pow2(20*math.pi/phase_error)
        reps=repetitions(failure/count);bits=M.bit_length()-1
        rows.append(dict(stage=j,width=width,width_exact=[exact_width.numerator,exact_width.denominator],normalizer=norm,test_epsilon=epsilon,
                         phase_error=phase_error,M=M,qpe_bits=bits,repetitions=reps,
                         threshold_abs_phase=1.42*epsilon,stage_failure=failure/count,
                         ideal_spectral_failure=2/9,phase_failure_bound=1/9,
                         controlled_U_calls=reps*(M-1),value_evaluations_and_inverses=2*reps*(M-1),
                         distribution_preparation_and_inverse_calls=reps*(2*(M-1)+1),
                         inverse_qft_controlled_rotations=reps*bits*(bits-1)//2))
        exact_width*=Fraction(3,4)
    return dict(moment=moment,error=error,failure=failure,initial_radius=s,normalizer=norm,
                initial_radius_exact=[exact_s.numerator,exact_s.denominator],endpoint_bits=endpoint_bits,
                stages=rows,final_interval_radius=float(exact_width/2),
                controlled_U_calls=sum(r['controlled_U_calls'] for r in rows),
                value_evaluations_and_inverses=sum(r['value_evaluations_and_inverses'] for r in rows),
                qpe_executions=sum(r['repetitions'] for r in rows),
                interpretation='Explicit known-moment complex-phase algorithm, not an ideal sigma/epsilon curve. Integer QPE and majority counts included.')


def controller(allocation,measure_qpe):
    """Executable adaptive classical controller; callback supplies measured integers.

    measure_qpe(stage, left_fixed_integer) returns exactly repetitions integers
    in [0,M). A physical device or a finite-unitary simulator may supply them.
    Classical interval endpoints stay exact rational numbers; only the phase
    circuit's endpoint load is rounded, and its error is charged separately.
    """
    if not allocation['stages']:return dict(estimate=0.,radius=allocation['initial_radius'],history=[])
    left=-Fraction(*allocation['initial_radius_exact']);width=-2*left;history=[];f=allocation['endpoint_bits']
    for stage in allocation['stages']:
        assert width==Fraction(*stage['width_exact'])
        scaled=left*(1<<f);raw=round(scaled)
        measurements=list(measure_qpe(stage,raw))
        if len(measurements)!=stage['repetitions'] or any(type(k) is not int or not 0<=k<stage['M'] for k in measurements):raise ValueError('invalid QPE measurements')
        threshold=stage['threshold_abs_phase'];M=stage['M']
        large=sum(2*math.pi*min(k,M-k)/M>threshold for k in measurements)>len(measurements)//2
        if large:left+=width/4
        width*=Fraction(3,4)
        history.append(dict(stage=stage['stage'],large=large,left_load=raw,left_exact=[left.numerator,left.denominator]))
    return dict(estimate=float(left+width/2),radius=float(width/2),history=history)


def update(left,width,large):
    # Small promise: mu-left<=width/4. Large promise: mu-left>=width/2.
    # In the indeterminate gap both returned intervals contain mu.
    return (left+width/4 if large else left),.75*width


def unitary(values,probabilities):
    p=np.asarray(probabilities,float);v=np.asarray(values,float)
    if np.any(p<0) or not np.isclose(p.sum(),1.):raise ValueError('invalid law')
    start=np.sqrt(p);reflection=2*np.outer(start,start)-np.eye(len(p))
    # Keep the sign of reflection: under a control its global sign is observable.
    return reflection@np.diag(np.exp(-2j*np.arctan(v))),start


def spectral_law(values,probabilities):
    from scipy.linalg import schur
    U,start=unitary(values,probabilities);tri,vec=schur(U,output='complex')
    if np.max(np.abs(tri-np.diag(np.diag(tri))))>1e-9:raise ArithmeticError('non-diagonal unitary Schur form')
    return np.angle(np.diag(tri)),np.abs(vec.conj().T@start)**2


def exact_qpe_test_probability(values,probabilities,M,threshold):
    phases,weights=spectral_law(values,probabilities);grid=2*math.pi*np.arange(M)/M
    folded=np.minimum(grid,2*math.pi-grid);prob=0.
    for phase,weight in zip(phases,weights):
        diff=(phase-grid+math.pi)%(2*math.pi)-math.pi
        mass=(np.sinc(M*diff/(2*math.pi))/np.sinc(diff/(2*math.pi)))**2
        prob+=weight*mass[folded>threshold].sum()/mass.sum()
    return float(prob)
