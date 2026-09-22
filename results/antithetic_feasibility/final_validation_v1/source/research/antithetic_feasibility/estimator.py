"""Explicit signed dyadic second-moment estimation, with integer QAE schedules.

This instantiates the binning mechanism of Montanaro Section 2, using the
explicit 2*pi*sqrt(p*(1-p))/M+pi^2/M^2 bound. A valid SECOND MOMENT bound about
the declared center is an input obligation, not inferred from pilot variance.
"""
import math
import numpy as np
from scipy.stats import binom


def power_two_at_least(x):return 2**max(0,math.ceil(math.log2(max(x,1.))))


def median_repetitions(delta):
    pbad=1-8/math.pi**2
    r=1
    while binom.sf(r//2,r,pbad)>delta:r+=2
    return r


def schedule(second_moment,error,delta,max_magnitude=None,center=0.,strategy='shared_moment'):
    if second_moment<0 or error<=0 or not 0<delta<1:raise ValueError('invalid contract')
    if second_moment==0:return dict(bins=[],calls_A=0,grover_iterates=0,total_error_bound=0.)
    s=math.sqrt(second_moment)
    base=2.**math.ceil(math.log2(s))
    tail_budget=error/4
    cutoff=base
    while cutoff<second_moment/tail_budget:cutoff*=2
    # R is a proved representable bound when supplied; else use second-moment tail.
    if max_magnitude is not None:
        while cutoff/2>max_magnitude and cutoff>base:cutoff/=2
        if cutoff==max_magnitude:cutoff*=2
    tail=0. if max_magnitude is not None and cutoff>=max_magnitude else second_moment/cutoff
    bounds=[];lo=0.;hi=base
    while True:
        # b*E[abs(Y)*1_bin] <= b^2 for lowest bin; <= b*E[Y^2]/lo otherwise.
        # lowest bin also bounded by b*s via Cauchy-Schwarz.
        v=min(hi*hi,hi*s) if lo==0 else min(hi*hi,hi*second_moment/lo)
        for sign in (-1,1):bounds.append((sign,lo,hi,v))
        if hi>=cutoff:break
        lo=hi;hi*=2
    ebin=(error-tail)/len(bounds)
    reps=median_repetitions(delta/len(bounds))
    # Across disjoint bins sum b E[|Y|1_bin] <= 4 E[Y^2]: low bin
    # <= base E|Y| <= 2s^2; higher bins <= 2 E[Y^2]. Cauchy-Schwarz
    # then gives sum sqrt(b E_bin) <= 2s sqrt(number of signed bins).
    aa_global=4*math.pi*s*math.sqrt(len(bounds))
    bb_global=math.pi**2*sum(x[2] for x in bounds)
    shared_M=power_two_at_least((aa_global+math.sqrt(aa_global**2+4*(error-tail)*bb_global))/(2*(error-tail)))
    rows=[]
    for sign,lo,hi,v in bounds:
        aa=2*math.pi*math.sqrt(v);bb=math.pi**2*hi
        required=(aa+math.sqrt(aa*aa+4*ebin*bb))/(2*ebin)
        M=shared_M if strategy=='shared_moment' else power_two_at_least(required)
        bound=aa/M+bb/(M*M)
        m=M.bit_length()-1
        rows.append(dict(sign=sign,lower=lo,upper=hi,M=M,qpe_qubits=m,repetitions=reps,
                         allocated_error=ebin,error_bound=bound,failure_budget=delta/len(bounds),
                         grover_iterates=reps*(M-1),calls_A=reps*(2*M-1),
                         qft_controlled_rotations=reps*m*(m-1)//2))
    return dict(second_moment=second_moment,center=center,error=error,delta=delta,
                cutoff=cutoff,tail_error_bound=tail,bins=rows,
                total_error_bound=tail+(aa_global/shared_M+bb_global/shared_M**2 if strategy=='shared_moment' else sum(r['error_bound'] for r in rows)),
                strategy=strategy,global_second_moment_error_bound=aa_global/shared_M+bb_global/shared_M**2,
                calls_A=sum(r['calls_A'] for r in rows),
                grover_iterates=sum(r['grover_iterates'] for r in rows),
                qft_controlled_rotations=sum(r['qft_controlled_rotations'] for r in rows),
                estimator='explicit signed dyadic QAE, median amplification, union bound',
                obligations=['Certified second moment about the actual center.',
                             'Coherent bin/selector encoding exact for the fixed-point value.',
                             'Preparation, numerical approximation and physical failure charged separately.'])


def qae_distribution(p,M):
    theta=math.asin(math.sqrt(p));y=np.arange(M)
    def distribution(angle):
        delta=angle-math.pi*y/M
        # sinc implements the continuous limit at eigenphases exactly on the grid.
        val=(np.sinc(M*delta/math.pi)/np.sinc(delta/math.pi))**2
        return val/val.sum()
    d=.5*(distribution(theta)+distribution(-theta))
    return np.sin(math.pi*y/M)**2,d/d.sum()
