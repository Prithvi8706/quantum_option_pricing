"""Analytic AM-GM moment bounds and exact policy-residual decomposition.

All formulas are for real arithmetic/ideal lognormal laws. Floating evaluation
is not interval arithmetic and does not itself certify rounding errors.
"""
import math
import numpy as np
from research.compound_feasibility.model import conditional_geometric, lognormal_call


def lognormal_spread_moments(mu, covariance):
    """Exact E[A-G], E[(A-G)^2] for equal-weight correlated lognormals."""
    mu = np.asarray(mu)
    v = np.diag(covariance)
    vg = covariance.mean()
    mg = mu.mean()
    ea = np.exp(mu + .5*v).mean()
    eg = math.exp(mg + .5*vg)
    ea2 = np.exp(mu[:, None]+mu[None, :]+.5*(v[:, None]+v[None, :])+covariance).mean()
    eag = np.exp(mu+mg+.5*(v+vg)+covariance.mean(axis=1)).mean()
    eg2 = math.exp(2*mg+2*vg)
    return float(max(0., ea-eg)), float(max(0., ea2-2*eag+eg2))


def global_moment(m):
    """Proved unconditional E[D^2] bound for D=H_cap-G_cap >= 0.

H and G use the SAME accrued average and half-weight future arithmetic and
geometric averages. Their capped call map is discount/2 Lipschitz in the
future average. Absolute future dates include randomness before exercise.
"""
    n=m.dates//2
    times=np.repeat(np.arange(n+1,m.dates+1)*m.maturity/m.dates,m.assets)
    asset=np.tile(np.arange(m.assets),n)
    rho=m.rho+(1-m.rho)*(asset[:,None]==asset[None,:])
    covariance=m.sigma**2*np.minimum.outer(times,times)*rho
    mu=np.log(m.spot)+(m.rate-.5*m.sigma**2)*times
    first,second=lognormal_spread_moments(mu,covariance)
    factor=.5*math.exp(-m.rate*m.maturity/2)
    return dict(residual_mean_bound=factor*first,residual_second_moment_bound=factor**2*second,
                flat_policy_residual_second_moment_bound=2*factor**2*second,
                interpretation='Analytic population bounds, not fitted to pilot moments. Real arithmetic; capped payoff Lipschitz domination.')


def conditional_bounds(m,spots,accrued,cap):
    """L <= C_cap <= U and E[D^2|X] <= m2 for EVERY positive spot state."""
    n=m.dates//2
    times=np.arange(1,n+1)*m.maturity/m.dates
    mint=np.minimum.outer(times,times)
    corr=m.rho+(1-m.rho)/m.assets
    vg=m.sigma**2*corr*mint.mean()
    cov=m.sigma**2*corr*mint.mean(axis=1)
    disc=math.exp(-m.rate*m.maturity/2)
    mean_s=spots.mean(axis=1)
    ea=mean_s*np.exp(m.rate*times).mean()
    eg=np.exp(np.log(spots).mean(axis=1)+(m.rate-.5*m.sigma**2)*times.mean()+.5*vg)
    w=np.exp(m.rate*(times[:,None]+times[None,:]))
    common=np.mean(w*np.exp(m.sigma**2*m.rho*mint))
    extra=np.mean(w*(np.exp(m.sigma**2*mint)-np.exp(m.sigma**2*m.rho*mint)))
    ea2=(common*spots.sum(axis=1)**2+extra*(spots**2).sum(axis=1))/m.assets**2
    eag=eg*mean_s*np.exp(m.rate*times+cov).mean()
    eg2=eg*eg*np.exp(vg)
    mean_gap=np.maximum(0.,.5*disc*(ea-eg))
    m2=np.minimum(cap*cap,np.maximum(0.,.25*disc*disc*(ea2-2*eag+eg2)))
    geo=conditional_geometric(m,spots,accrued,cap)
    # Jensen call bounds: E[(A-k)+] <= average E[(S_j-k)+].
    # Use uncapped upper call; subtract a valid upper bound on its cap tail
    # for the arithmetic Jensen lower bound. The capped call is not convex.
    k=2*(m.strike-accrued)
    upper_call=np.zeros(len(spots));tail_upper=np.zeros(len(spots))
    for t in times:
        mu=np.log(spots)+(m.rate-.5*m.sigma**2)*t
        var=m.sigma**2*t
        upper_call+=lognormal_call(mu,var,k[:,None]).mean(axis=1)/n
        tail_upper+=lognormal_call(mu,var,(k+2*cap/disc)[:,None]).mean(axis=1)/n
    lower=np.maximum(geo,.5*disc*(np.maximum(ea-k,0.)-tail_upper))
    upper=np.minimum(np.minimum(cap,geo+np.minimum(mean_gap,np.sqrt(m2))),.5*disc*upper_call)
    # Tiny floating violations should be visible, not silently hidden as data.
    if np.any(lower>upper+1e-8):raise ArithmeticError('conditional interval numerically inverted')
    upper=np.maximum(upper,lower)
    return dict(lower=lower,upper=upper,geo=geo,second_moment=m2,mean_gap=mean_gap)


def regret_envelope(lower,upper,pred,strike):
    """0 <= (C-K)+ - d(C-K) <= envelope whenever C in [L,U]."""
    d=pred>strike
    return np.where(d,np.maximum(strike-lower,0.),np.maximum(upper-strike,0.))


def flat_moment_envelope(bounds,pred,strike):
    """Conditional second moment of d(D+g-pred) from an ED^2 upper bound.

Pred is clipped into [L,U]; a=pred-g >=0 and E[D]>=L-g. Keeping the negative
cross term tightens the bound. Its population mean still needs integration;
the universal analytic fallback is 2*global_moment.
"""
    shift=pred-bounds['geo']
    return (pred>strike)*np.maximum(0.,bounds['second_moment']+shift*shift-2*shift*(bounds['lower']-bounds['geo']))
