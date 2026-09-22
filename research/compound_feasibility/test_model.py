import math
from dataclasses import replace
import numpy as np
from scipy.integrate import quad
from .model import *


def test_conditional_control_matches_large_independent_rqmc():
    m=Model();spots=np.array([[95.,101.,113.,99.],[150.,130.,110.,120.]])
    accrued=np.array([49.,75.]);cap=128.
    f,g=future_factors(m,16,7345)
    sampled=math.exp(-m.rate*m.maturity/2)*np.maximum(accrued[:,None]+.5*np.exp(np.log(spots).mean(axis=1))[:,None]*g-m.strike,0)
    sampled=np.minimum(sampled,cap)
    np.testing.assert_allclose(sampled.mean(axis=1),conditional_geometric(m,spots,accrued,cap),atol=.003,rtol=0)


def test_factorized_payoff_matches_direct_path_and_amgm():
    m=Model();s,a=outer_states(m,3,829);dw=normals(m,6,4,555)
    t=np.arange(1,7)*m.maturity/m.dates
    returns=np.exp((m.rate-.5*m.sigma**2)*t[None,:,None]+m.sigma*np.cumsum(dw,axis=1))
    f,g=future_factors(m,4,555)
    residual,h=inner_samples(s,a,f,g,m.strike,math.exp(-.015),128.)
    direct=np.minimum(128.,math.exp(-.015)*np.maximum(a[:,None]+np.einsum('id,jnd->ij',s,returns)/(m.dates*m.assets)-100,0))
    np.testing.assert_allclose(h,direct,atol=1e-12)
    assert residual.min()>-1e-12


def test_deterministic_contract_and_cap_tail():
    m=replace(Model(),sigma=0.)
    s,a=outer_states(m,2,34);y,_=continuation_samples(m,s,a,2,98,128.)
    price=math.exp(-.015)*max(math.exp(-.015)*(100*np.exp(.03*np.arange(1,13)/12).mean()-100)-1,0)
    assert abs(math.exp(-.015)*np.maximum(y.mean(axis=1)-1,0).mean()-price)<1e-12
    for model in MODELS:
        cap,bound=choose_cap(model)
        assert bound<=.0005 and cap_tail(model,cap/2)>.0005


def test_nested_bounds_and_telescoping_identity():
    rng=np.random.default_rng(287);samples=rng.normal(1,2,(512,64));k=.5;decision=rng.integers(0,2,512)
    lower=decision*(samples.mean(axis=1)-k);upper=np.maximum(samples.mean(axis=1)-k,0)
    assert np.all(lower<=upper)
    # Exact deterministic telescoping for the hierarchical block-average estimator.
    estimates=[np.maximum(samples.reshape(512,-1,2**l).mean(axis=2)-k,0).mean(axis=1) for l in range(7)]
    total=estimates[0].copy()
    for l in range(1,7):
        correction=estimates[l]-estimates[l-1]
        assert correction.max()<1e-12
        total+=correction
    np.testing.assert_allclose(total,upper,atol=1e-14)


def test_two_date_one_asset_against_conditional_quadrature():
    m=Model('analytic',1,2,.3,.2,1.);cap,_=choose_cap(m);strike=6.
    def payoff(z):
        spot=100*math.exp((.03-.5*.3**2)*.5+.3*math.sqrt(.5)*z)
        continuation=conditional_geometric(m,np.array([[spot]]),np.array([spot/2]),cap)[0]
        return math.exp(-.015)*max(continuation-strike,0.)*math.exp(-z*z/2)/math.sqrt(2*math.pi)
    ref=quad(payoff,-10,10,epsabs=1e-10,limit=300)[0]
    s,a=outer_states(m,16,19915);y,_=continuation_samples(m,s,a,2,775,cap)
    np.testing.assert_allclose(np.ptp(y,axis=1),0.,atol=1e-12)
    estimate=math.exp(-.015)*np.maximum(y.mean(axis=1)-strike,0).mean()
    assert abs(estimate-ref)<.001


def test_analytic_outer_moment_bound_against_vanilla_quadrature():
    for m in (MODELS[0],MODELS[2]):
        disc=math.exp(-m.rate*m.maturity/2);kk=m.strike+3/disc;values=[]
        for j in range(1,m.dates+1):
            time=j*m.maturity/m.dates
            value=quad(lambda z:max(m.spot*math.exp((m.rate-.5*m.sigma**2)*time+m.sigma*math.sqrt(time)*z)-kk,0.)**2*math.exp(-z*z/2)/math.sqrt(2*math.pi),-12,12,epsabs=1e-7,limit=300)[0]
            values.append(value)
        assert abs(outer_target_second_moment_bound(m)-disc**2*np.mean(values))<1e-5
