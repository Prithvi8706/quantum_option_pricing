import math
import numpy as np
from scipy.stats import binom
from .estimator import schedule,qae_distribution,median_repetitions


def test_actual_qae_error_bound_on_probability_grid():
    for M in (16,64,256):
        for p in np.r_[0.,1.,np.linspace(.00001,.99999,51)]:
            estimates,probs=qae_distribution(p,M)
            bound=2*math.pi*math.sqrt(p*(1-p))/M+math.pi**2/M**2
            success=probs[np.abs(estimates-p)<=bound+1e-13].sum()
            assert success>=8/math.pi**2-1e-12


def test_explicit_schedule_allocations_and_counts():
    for moment in (1e-8,1e-3,2.,100.):
        for error in (.001,.01,.1):
            s=schedule(moment,error,.001)
            assert s['total_error_bound']<=error*(1+1e-12)
            assert sum(r['failure_budget'] for r in s['bins'])<=.001*(1+1e-12)
            assert s['calls_A']==sum(r['repetitions']*(2*r['M']-1) for r in s['bins'])
            for r in s['bins']:
                assert r['M']&(r['M']-1)==0
                assert binom.sf(r['repetitions']//2,r['repetitions'],1-8/math.pi**2)<=r['failure_budget']


def test_bins_cover_signed_finite_distribution_and_moment_inequality():
    x=np.array([-20.,-2.,-.1,0.,.2,3.,15.]);p=np.array([.001,.04,.1,.6,.2,.058,.001])
    m=float(np.dot(p,x*x));s=schedule(m,.01,.005,max_magnitude=20.)
    total=0.
    for row in s['bins']:
        sign=row['sign'];y=sign*x
        mask=(y>=row['lower'])&(y<row['upper'])
        value=np.dot(p,np.where(mask,y,0.))
        total+=sign*value
        variance_proxy=row['upper']*value
        expected_bound=min(row['upper']**2,row['upper']*math.sqrt(m)) if row['lower']==0 else min(row['upper']**2,row['upper']*m/row['lower'])
        assert variance_proxy<=expected_bound+1e-12
    assert abs(total-np.dot(p,x))<1e-12
