import math
import numpy as np
from numpy.polynomial.hermite import hermgauss
from research.compound_feasibility.model import Model,MODELS,outer_states,future_factors,continuation_samples
from .parity import put_moments,bounds,moment_bound,complement_stats


def test_put_moments_by_quadrature():
    from scipy.integrate import quad
    mu=4.6;v=.07;k=np.array([75.,100.,135.]);mean,second=put_moments(mu,v,k)
    for i,kk in enumerate(k):
        boundary=(math.log(kk)-mu)/math.sqrt(v)
        for p,expected in ((1,mean[i]),(2,second[i])):
            val=quad(lambda z:(kk-math.exp(mu+math.sqrt(v)*z))**p*math.exp(-z*z/2)/math.sqrt(2*math.pi),-15,boundary,epsabs=1e-9)[0]
            np.testing.assert_allclose(val,expected,rtol=1e-9,atol=1e-9)


def test_parity_identity_and_bounded_flat_residual():
    m=MODELS[0];s,ac=outer_states(m,8,324);ff,gg=future_factors(m,6,897)
    b=bounds(m,s,ac);disc=math.exp(-m.rate*m.maturity/2)
    for j in range(8):
        arithmetic=ac+s@ff[j];geom=ac+.5*np.exp(np.log(s).mean(axis=1))*gg[j]
        h=disc*np.maximum(arithmetic-m.strike,0.);g=disc*np.maximum(geom-m.strike,0.)
        spread=disc*(arithmetic-geom)
        r=disc*(np.maximum(m.strike-geom,0.)-np.maximum(m.strike-arithmetic,0.))
        np.testing.assert_allclose(h-g,spread-r,atol=1e-12)
        assert r.min()>-1e-12 and r.max()<=b['support']+1e-12
        pred=(b['lower']+b['upper'])/2;a=b['c0']-pred
        assert a.min()>-1e-10 and np.max(a-b['put'])<1e-10
        assert np.max(np.abs(a-r))<=b['support']+1e-10


def test_streaming_parity_with_disjoint_groups():
    m=MODELS[0];s,ac=outer_states(m,3,743);ff,gg=future_factors(m,6,848);disc=math.exp(-m.rate*m.maturity/2)
    mean,second=complement_stats(s,ac,ff,gg,m.strike,disc,inner=8)
    for i in range(len(s)):
        a,b=complement_stats(s[i:i+1],ac[i:i+1],ff[8*i:8*i+8],gg[8*i:8*i+8],m.strike,disc)
        np.testing.assert_allclose([mean[i],second[i]],[a[0],b[0]])


def test_parity_conditional_moment_and_interval_with_quadrature():
    m=Model(assets=2,dates=2,sigma=.2,rho=0.,maturity=1.)
    s=np.array([[95.,105.]]);ac=np.array([50.]);b=bounds(m,s,ac)
    x,w=hermgauss(90);z=np.array(np.meshgrid(x,x,indexing='ij')).reshape(2,-1).T*math.sqrt(2);weights=np.outer(w,w).ravel()/math.pi
    future=s*np.exp((m.rate-.5*m.sigma**2)*.5+m.sigma*math.sqrt(.5)*z)
    disc=math.exp(-m.rate*.5);aa=ac+.5*future.mean(axis=1);gg=ac+.5*np.sqrt(future.prod(axis=1))
    h=disc*np.maximum(aa-100,0);r=disc*(np.maximum(100-gg,0)-np.maximum(100-aa,0))
    pred=(b['lower']+b['upper'])/2;yy=b['c0'][0]-pred[0]-r
    assert b['lower'][0]-.002<=weights@h<=b['upper'][0]+.002
    assert weights@(r*r)<=b['complement_second'][0]+.002
    assert weights@(yy*yy)<=moment_bound(b,pred,0.)[0]+.002
