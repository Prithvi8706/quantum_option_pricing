"""Bounded put-complement residual for the original uncapped contract."""
import math
import numpy as np
from scipy.special import ndtr
from numba import njit
from research.compound_feasibility.model import lognormal_call,moment_continuation,features


def put_moments(mu,var,strike):
    """First and second moments of (strike-exp(N(mu,var)))+."""
    k=np.asarray(strike);safe=np.maximum(k,1e-300);sd=math.sqrt(var)
    if sd==0:
        put=np.maximum(k-np.exp(mu),0.);return put,put*put
    z=(np.log(safe)-mu)/sd
    first=k*ndtr(z)-np.exp(mu+.5*var)*ndtr(z-sd)
    second=k*k*ndtr(z)-2*k*np.exp(mu+.5*var)*ndtr(z-sd)+np.exp(2*mu+2*var)*ndtr(z-2*sd)
    return np.where(k>0,np.maximum(first,0.),0.),np.where(k>0,np.maximum(second,0.),0.)


def bounds(m,spots,accrued):
    n=m.dates//2;t=np.arange(1,n+1)*m.maturity/m.dates;mt=np.minimum.outer(t,t)
    disc=math.exp(-m.rate*m.maturity/2);q=.5*disc;k=2*(m.strike-accrued)
    corr=m.rho+(1-m.rho)/m.assets;vg=m.sigma**2*corr*mt.mean();cov=m.sigma**2*corr*mt.mean(axis=1)
    mu=np.log(spots).mean(axis=1)+(m.rate-.5*m.sigma**2)*t.mean()
    eg=np.exp(mu+.5*vg);ea=spots.mean(axis=1)*np.exp(m.rate*t).mean()
    pg,pg2=put_moments(mu,vg,k);pg*=q;pg2*=q*q
    f=q*(ea-k);geo=q*lognormal_call(mu,vg,k);c0=f+pg
    lower=np.maximum(geo,np.maximum(f,0.))
    w=np.exp(m.rate*(t[:,None]+t[None,:]))
    common=np.mean(w*np.exp(m.sigma**2*m.rho*mt))
    extra=np.mean(w*(np.exp(m.sigma**2*mt)-np.exp(m.sigma**2*m.rho*mt)))
    ea2=(common*spots.sum(axis=1)**2+extra*(spots**2).sum(axis=1))/m.assets**2
    eag=eg*spots.mean(axis=1)*np.exp(m.rate*t+cov).mean()
    spread2=np.maximum(0.,q*q*(ea2-2*eag+eg*eg*np.exp(vg)))
    # Jensen upper call can tighten U; no caps/tail subtraction in this variant.
    upper_call=np.zeros(len(spots))
    for tj in t:
        upper_call+=q*lognormal_call(np.log(spots)+(m.rate-.5*m.sigma**2)*tj,m.sigma**2*tj,k[:,None]).mean(axis=1)/n
    upper=np.minimum(c0,upper_call)
    if np.any(lower>upper+1e-8):raise ArithmeticError('parity continuation interval inverted')
    upper=np.maximum(upper,lower)
    return dict(lower=lower,upper=upper,c0=c0,put=pg,put_second=pg2,forward=f,
                complement_second=np.minimum(spread2,pg2),spread_second=spread2,
                support=disc*m.strike)


def prediction(m,spots,accrued,fit,b):
    pred=moment_continuation(m,spots,accrued,-1.)
    if fit['selected']=='regression':pred+=features(m,spots,accrued,-1.)[0]@np.array(fit['coef'])
    return np.clip(pred,b['lower'],b['upper'])


def moment_bound(b,pred,strike):
    a=np.maximum(0.,b['c0']-pred);lower_mean=np.maximum(0.,b['c0']-b['upper'])
    return (pred>strike)*np.minimum(b['support']**2,np.maximum(0.,b['complement_second']+a*a-2*a*lower_mean))


@njit(cache=True)
def complement_stats(spots,accrued,factors,geom_factors,strike,discount,inner=0):
    """Shared RQMC factors or disjoint iid inner groups; no matrix temporary."""
    means=np.empty(len(spots));seconds=np.empty(len(spots))
    count=len(factors) if inner==0 else inner
    for i in range(len(spots)):
        geom=math.exp(np.log(spots[i]).mean());total=0.;square=0.
        for jj in range(count):
            j=jj if inner==0 else i*inner+jj
            av=accrued[i]
            for k in range(spots.shape[1]):av+=spots[i,k]*factors[j,k]
            pa=discount*max(strike-av,0.)
            pg=discount*max(strike-accrued[i]-.5*geom*geom_factors[j],0.)
            r=pg-pa;total+=r;square+=r*r
        means[i]=total/count;seconds[i]=square/count
    return means,seconds
