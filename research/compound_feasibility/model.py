"""Exact-date GBM, conditional geometric controls, reusable future return paths."""
from dataclasses import dataclass
import math
import numpy as np
from numba import njit
from scipy.special import ndtr,ndtri
from scipy.stats import qmc
from research.antithetic_feasibility.classical import bridge,bridge_plan,seeded


@dataclass(frozen=True)
class Model:
    name:str='C4'
    assets:int=4
    dates:int=12
    sigma:float=.2
    rho:float=.2
    maturity:float=1.
    strike:float=100.
    spot:float=100.
    rate:float=.03


MODELS=[Model(),Model('C8',8,12,.4,.2,1.),Model('H4',4,12,.4,.7,3.),Model('H8',8,24,.4,.2,3.)]


def lognormal_call(mu,var,k):
    mean=np.exp(mu+.5*var)
    if np.ndim(k)==0 and k<=0:return mean-k
    kk=np.maximum(k,1e-300);sd=np.sqrt(var)
    if np.all(sd==0):return np.maximum(mean-k,0.)
    d2=(mu-np.log(kk))/sd
    return np.where(np.asarray(k)<=0,mean-k,mean*ndtr(d2+sd)-kk*ndtr(d2))


def cap_tail(m,cap):
    # Lipschitz outer call + Jensen over all fixings yields this uncapped-price bound.
    t=np.arange(1,m.dates+1)*m.maturity/m.dates
    threshold=m.strike+cap*math.exp(m.rate*m.maturity/2)
    mu=math.log(m.spot)+(m.rate-.5*m.sigma**2)*t
    return float(math.exp(-m.rate*m.maturity)*np.mean(lognormal_call(mu,m.sigma**2*t,threshold)))


def choose_cap(m,budget=.0005):
    cap=128.
    while cap_tail(m,cap)>budget:cap*=2
    return cap,cap_tail(m,cap)


def outer_target_second_moment_bound(m,compound_strike=3.):
    """E[(C-Kc)+^2] <= E[(H-Kc)+^2] <= vanilla-fixing Jensen bound."""
    t=np.arange(1,m.dates+1)*m.maturity/m.dates;v=m.sigma**2*t
    mu=math.log(m.spot)+(m.rate-.5*m.sigma**2)*t;sd=np.sqrt(v)
    disc=math.exp(-m.rate*m.maturity/2);k=m.strike+compound_strike/disc
    d=(mu-math.log(k))/sd
    squared=np.exp(2*mu+2*v)*ndtr(d+2*sd)-2*k*np.exp(mu+.5*v)*ndtr(d+sd)+k*k*ndtr(d)
    return float(disc*disc*np.mean(squared))


def normals(m,steps,power,seed,method='rqmc'):
    d=m.assets
    if method=='rqmc':
        u=qmc.Sobol(d*steps,scramble=True,seed=seed).random_base2(power)
        z=ndtri(np.clip(u,np.finfo(float).eps,1-np.finfo(float).eps))
    else:z=np.random.default_rng(seed).standard_normal((2**power,d*steps))
    raw=np.eye(d);raw[:,0]=1.;basis,_=np.linalg.qr(raw)
    if basis[0,0]<0:basis[:,0]*=-1
    eig=np.full(d,1-m.rho);eig[0]=1+(d-1)*m.rho
    x=bridge(z.reshape(-1,steps,d),bridge_plan(steps))
    return ((x*np.sqrt(eig))@basis.T)*math.sqrt(m.maturity/m.dates)


def outer_states(m,power,seed,method='rqmc'):
    n=m.dates//2;dw=normals(m,n,power,seed,method)
    t=np.arange(1,n+1)*m.maturity/m.dates
    paths=m.spot*np.exp((m.rate-.5*m.sigma**2)*t[None,:,None]+m.sigma*np.cumsum(dw,axis=1))
    return np.ascontiguousarray(paths[:,-1,:]),np.ascontiguousarray(paths.sum(axis=(1,2))/(m.assets*m.dates))


def future_factors(m,power,seed,method='rqmc'):
    n=m.dates//2;dw=normals(m,n,power,seed,method)
    t=np.arange(1,n+1)*m.maturity/m.dates
    logs=(m.rate-.5*m.sigma**2)*t[None,:,None]+m.sigma*np.cumsum(dw,axis=1)
    return np.ascontiguousarray(np.exp(logs).sum(axis=1)/(m.assets*m.dates)),np.ascontiguousarray(np.exp(logs.mean(axis=(1,2))))


def conditional_geometric(m,spots,accrued,cap):
    n=m.dates//2;t=np.arange(1,n+1)*m.maturity/m.dates;disc=math.exp(-m.rate*m.maturity/2)
    mu=np.log(spots).mean(axis=1)+(m.rate-.5*m.sigma**2)*t.mean()
    var=m.sigma**2*(m.rho+(1-m.rho)/m.assets)*np.minimum.outer(t,t).mean()
    k=(m.strike-accrued)*2
    value=.5*disc*lognormal_call(mu,var,k)
    if cap>0:value-=.5*disc*lognormal_call(mu,var,k+2*cap/disc)
    return value


def moment_continuation(m,spots,accrued,cap):
    n=m.dates//2;t=np.arange(1,n+1)*m.maturity/m.dates;disc=math.exp(-m.rate*m.maturity/2)
    weights=np.exp(m.rate*(t[:,None]+t[None,:]));mint=np.minimum.outer(t,t)
    common=np.mean(weights*np.exp(m.sigma**2*m.rho*mint))
    independent=np.mean(weights*(np.exp(m.sigma**2*mint)-np.exp(m.sigma**2*m.rho*mint)))
    total=spots.sum(axis=1);squares=(spots**2).sum(axis=1)
    mean=spots.mean(axis=1)*np.exp(m.rate*t).mean()
    second=(common*total**2+independent*squares)/m.assets**2
    var=np.log(np.maximum(second/mean**2,1+1e-15));mu=np.log(mean)-.5*var;k=2*(m.strike-accrued)
    value=.5*disc*lognormal_call(mu,var,k)
    if cap>0:value-=.5*disc*lognormal_call(mu,var,k+2*cap/disc)
    return value


@njit(cache=True)
def inner_samples(spots,accrued,factors,geom_factors,strike,discount,cap):
    out=np.empty((len(spots),len(factors)));raw=np.empty_like(out)
    for i in range(len(spots)):
        geom=math.exp(np.log(spots[i]).mean())
        for j in range(len(factors)):
            average=accrued[i]
            for k in range(spots.shape[1]):average+=spots[i,k]*factors[j,k]
            h=min(cap,discount*max(average-strike,0.))
            g=min(cap,discount*max(accrued[i]+.5*geom*geom_factors[j]-strike,0.))
            raw[i,j]=h;out[i,j]=h-g
    return out,raw


def continuation_samples(m,spots,accrued,power,seed,cap,method='rqmc'):
    ff,gg=future_factors(m,power,seed,method)
    residual,raw=inner_samples(spots,accrued,ff,gg,m.strike,math.exp(-m.rate*m.maturity/2),cap)
    mean=conditional_geometric(m,spots,accrued,cap)
    return residual+mean[:,None],raw


def features(m,spots,accrued,cap):
    geo=conditional_geometric(m,spots,accrued,cap);mm=moment_continuation(m,spots,accrued,cap)
    basket=spots.mean(axis=1);disp=spots.std(axis=1)/basket
    z=(accrued+.5*basket-m.strike)/(m.spot*m.sigma*math.sqrt(m.maturity))
    z=np.clip(z,-5,5);g=(mm-geo)
    # Regress a small correction to an analytic approximation, not the entire option value.
    x=np.column_stack([np.ones(len(z)),z,z*z,z**3,disp,disp**2,g,g*z,g*z*z,g*disp,basket/100-1,accrued/50-1])
    return x,geo,mm


def policy_value(m,spots,accrued,cap,coef):
    x,geo,mm=features(m,spots,accrued,cap)
    return np.clip(mm+x@coef,geo,cap)
