import math
from dataclasses import replace
import numpy as np
from scipy.integrate import quad
from research.antithetic_feasibility.classical import (
    Model, bridge, bridge_plan, factors, conditional_call, draw_increments,
    path_values, values, control_mean,
)


def test_bridge_is_orthogonal_and_terminal_mode_constant():
    for n in (3,12,24):
        x=np.eye(n).reshape(n,n,1)
        a=bridge(x,bridge_plan(n))[:,:,0]
        np.testing.assert_allclose(a@a.T,np.eye(n),atol=1e-14)
        np.testing.assert_allclose(a[0],np.full(n,1/math.sqrt(n)),atol=1e-14)


def test_full_covariance_matches_declared_model():
    m=Model();u,av,ash,asi=factors(m)
    ss=u@np.diag(ash**2+asi**2)@u.T
    vv=u@np.diag(av**2)@u.T
    sv=u@np.diag(ash*av)@u.T
    target=np.full((4,4),.3);np.fill_diagonal(target,1)
    np.testing.assert_allclose(ss,target,atol=1e-14)
    np.testing.assert_allclose(sv,m.leverage*target,atol=1e-14)
    np.testing.assert_allclose(vv,m.leverage**2*target+(1-m.leverage**2)*np.eye(4),atol=1e-14)


def test_conditional_formula_against_independent_quadrature():
    for a,b,k in [(np.log([90.,110.]),np.array([.2,.4]),100.),
                  (np.log([70.,120.]),np.array([-.5,.4]),110.),
                  (np.log([90.,110.]),np.array([-.2,-.4]),100.),
                  (np.log([90.,110.]),np.array([0.,0.]),80.),
                  (np.log([120.,120.]),np.array([-.3,.3]),90.)]:
        ref=quad(lambda z:max(np.exp(a+b*z).mean()-k,0)*math.exp(-z*z/2)/math.sqrt(2*math.pi),
                 -12,12,epsabs=1e-9,points=list(np.linspace(-8,8,65)),limit=500)[0]
        assert abs(conditional_call(a,b,k)-ref)<2e-7


def test_constant_variance_telescopes_pathwise():
    m=replace(Model(),xi=0.)
    for cond in (False,True):
        y=values(m,2,5,123,conditional=cond,correction=True)
        assert np.max(np.abs(y))<1e-10


def test_geometric_control_mean_with_independent_rqmc():
    m=Model()
    x=values(m,1,13,425,conditional=True)
    # Diagnostic integration check, deliberately much looser than pricing accuracy.
    assert abs(x[:,1].mean()-control_mean(m))<.03


def test_cap_and_conditional_identity_in_constant_volatility():
    m=replace(Model(assets=1),xi=0.)
    plain=values(m,0,12,754,conditional=False,cap=20.)
    smooth=values(m,0,12,754,conditional=True,cap=20.)
    assert plain[:,0].min()>=0 and plain[:,0].max()<=20*math.exp(-.03)+1e-10
    assert abs(plain[:,0].mean()-smooth[:,0].mean())<.1
    assert abs(smooth[:,1].mean()-control_mean(m,20.))<.03
