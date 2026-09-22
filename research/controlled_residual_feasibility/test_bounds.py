import math
import numpy as np
from numpy.polynomial.hermite import hermgauss
from research.compound_feasibility.model import Model,MODELS,outer_states,choose_cap
from .bounds import lognormal_spread_moments,conditional_bounds,global_moment,regret_envelope,flat_moment_envelope


def test_lognormal_moments_against_independent_gaussian_quadrature():
    mu=np.array([4.4,4.8]);cov=np.array([[.04,.012],[.012,.07]])
    x,w=hermgauss(24);z=np.array(np.meshgrid(x,x,indexing='ij')).reshape(2,-1).T*math.sqrt(2)
    weights=np.outer(w,w).ravel()/math.pi
    s=np.exp(mu+z@np.linalg.cholesky(cov).T);spread=s.mean(axis=1)-np.sqrt(s[:,0]*s[:,1])
    first,second=lognormal_spread_moments(mu,cov)
    np.testing.assert_allclose([first,second],[weights@spread,weights@(spread**2)],rtol=1e-10)


def test_conditional_spread_moment_matches_general_log_normal_identity():
    m=MODELS[1];cap,_=choose_cap(m);spots,accrued=outer_states(m,3,71623)
    b=conditional_bounds(m,spots,accrued,cap)
    times=np.repeat(np.arange(1,m.dates//2+1)*m.maturity/m.dates,m.assets)
    asset=np.tile(np.arange(m.assets),m.dates//2)
    cov=m.sigma**2*np.minimum.outer(times,times)*(m.rho+(1-m.rho)*(asset[:,None]==asset[None,:]))
    for i,s in enumerate(spots):
        mu=np.tile(np.log(s),m.dates//2)+(m.rate-.5*m.sigma**2)*times
        first,second=lognormal_spread_moments(mu,cov)
        np.testing.assert_allclose(b['mean_gap'][i],.5*math.exp(-m.rate*m.maturity/2)*first,rtol=1e-10)
        np.testing.assert_allclose(b['second_moment'][i],min(cap**2,.25*math.exp(-m.rate*m.maturity)*second),rtol=1e-9)


def test_exact_finite_law_flattening_regret_and_centered_moment_bound():
    # Enumerate conditional residual laws; policy is deliberately sometimes wrong.
    rng=np.random.default_rng(77)
    for _ in range(100):
        residual=rng.uniform(0,3,7);weights=rng.dirichlet(np.ones(7));g=rng.uniform(0,5)
        c=g+weights@residual;lo=g;up=g+3;pred=rng.uniform(lo,up);k=rng.uniform(0,8);d=pred>k
        y=d*(residual+g-pred);regret=max(c-k,0)-d*(c-k)
        np.testing.assert_allclose(max(c-k,0),max(pred-k,0)+weights@y+regret,atol=1e-14)
        assert 0<=regret+1e-14<=regret_envelope(lo,up,pred,k)+1e-13
        b=dict(lower=np.array([lo]),upper=np.array([up]),geo=np.array([g]),second_moment=np.array([weights@(residual**2)]))
        assert weights@(y*y)<=flat_moment_envelope(b,np.array([pred]),k)[0]+1e-12


def test_cap_interval_against_small_exact_gaussian_quadrature():
    # One future fixing for each of two independent assets; accrued term fixed.
    m=Model(assets=2,dates=2,sigma=.2,rho=0.,maturity=1.)
    x,w=hermgauss(80);z=np.array(np.meshgrid(x,x,indexing='ij')).reshape(2,-1).T*math.sqrt(2)
    weights=np.outer(w,w).ravel()/math.pi
    for spot in ([80.,90.],[95.,110.],[120.,130.]):
        for accrued in (35.,50.,75.):
            s=np.array([spot]);a=np.array([accrued]);cap=7.
            b=conditional_bounds(m,s,a,cap)
            future=s*np.exp((m.rate-.5*m.sigma**2)*.5+m.sigma*math.sqrt(.5)*z)
            h=np.minimum(cap,math.exp(-m.rate*.5)*np.maximum(accrued+.5*future.mean(axis=1)-100,0))
            c=weights@h
            # Quadrature is approximate at the kink; intervals are comfortably wider.
            assert b['lower'][0]-2e-4<=c<=b['upper'][0]+2e-4
            g=np.minimum(cap,math.exp(-m.rate*.5)*np.maximum(accrued+.5*np.sqrt(future.prod(axis=1))-100,0))
            assert weights@((h-g)**2)<=b['second_moment'][0]+1e-8


def test_global_and_local_bounds_use_correct_future_dates_and_discount():
    # Tower identity: averaging conditional spread bounds reproduces the global
    # spread moment. RQMC accuracy here is only a regression check of formulas.
    m=MODELS[0];s,a=outer_states(m,15,7391);b=conditional_bounds(m,s,a,1e9)
    glob=global_moment(m)
    np.testing.assert_allclose(b['second_moment'].mean(),glob['residual_second_moment_bound'],rtol=.005)
    assert np.all(b['lower']<=b['upper'])
    assert np.all(b['lower']>=b['geo']-1e-10)
