"""Compiled coupled Heston pricing and conditional Gaussian integration.

Continuous Gaussian, discrete SDE targets. Results are not bias certificates.
The common residual price mode is integrated analytically conditional on all
variance Brownian inputs. A numerical scalar root remains, with explicit tests.
"""
from dataclasses import dataclass, asdict
import math
import time
import numpy as np
from scipy.special import ndtri, ndtr
from scipy.stats import qmc
from numba import njit


@dataclass(frozen=True)
class Model:
    name: str = 'A4'
    assets: int = 4
    dates: int = 12
    spot: float = 100.
    strike: float = 100.
    rate: float = .03
    maturity: float = 1.
    kappa: float = 2.
    theta: float = .09
    v0: float = .09
    xi: float = .3
    leverage: float = -.5
    correlation: float = .3


MODELS = [Model(name='A1', assets=1), Model(),
          Model(name='S4', theta=.04, v0=.04, xi=.5, leverage=-.7),
          Model(name='B8', assets=8, kappa=1.5, theta=.12, v0=.12,
                xi=.5, leverage=-.7, correlation=.6, maturity=2.)]


def bridge_plan(n):
    """Terminal Brownian value first; then breadth-first conditional midpoints."""
    plan = []
    queue = [(0, n)]
    while queue:
        l, r = queue.pop(0)
        if r-l > 1:
            m = (l+r)//2
            plan.append((l, m, r))
            queue.extend([(l,m), (m,r)])
    return np.asarray(plan, dtype=np.int64).reshape(-1,3)


@njit(cache=True)
def bridge(z, plan):
    p, n, d = z.shape
    b = np.zeros((p, n+1, d))
    b[:, n, :] = math.sqrt(n)*z[:, 0, :]
    for k in range(len(plan)):
        l,m,r = plan[k]
        b[:,m,:] = ((r-m)*b[:,l,:]+(m-l)*b[:,r,:])/(r-l) + math.sqrt((m-l)*(r-m)/(r-l))*z[:,k+1,:]
    return b[:,1:,:]-b[:,:-1,:]


def factors(model):
    d=model.assets
    # Deterministic orthogonal basis with common direction first.
    raw=np.eye(d)
    raw[:,0]=1.
    u,_=np.linalg.qr(raw)
    if u[0,0]<0: u[:,0]*=-1
    ls=np.full(d,1-model.correlation);ls[0]=1+(d-1)*model.correlation
    lv=model.leverage**2*ls+1-model.leverage**2
    return u, np.sqrt(lv), model.leverage*ls/np.sqrt(lv), np.sqrt(ls*(1-model.leverage**2)/lv)


def draw_increments(model, level, power, seed, method='rqmc', conditional=False):
    n=model.dates*2**level; d=model.assets; p=2**power
    if method=='rqmc':
        engine=qmc.Sobol(2*d*n,scramble=True,seed=seed)
        raw=ndtri(np.clip(engine.random_base2(power),np.finfo(float).eps,1-np.finfo(float).eps))
    else:
        raw=np.random.default_rng(seed).standard_normal((p,2*d*n))
    # Time-bridge priority, interleaved variance/price principal components.
    z=raw.reshape(p,n,2*d)
    if conditional: z[:,0,d]=0.
    b=bridge(z,bridge_plan(n))
    u, av, ash, asi=factors(model)
    dt=model.maturity/n
    dv=(b[:,:,:d]*av)@u.T*math.sqrt(dt)
    ds=((b[:,:,:d]*ash+b[:,:,d:]*asi)@u.T)*math.sqrt(dt)
    direction=np.full(d, math.sqrt(model.maturity)/n*asi[0]/math.sqrt(d)) if conditional else np.zeros(d)
    return np.ascontiguousarray(ds),np.ascontiguousarray(dv),direction


@njit(cache=True)
def phi(x):
    return .5*math.erfc(-x/math.sqrt(2.))


@njit(cache=True)
def logsum(a,b,z):
    m=-1.e300
    for i in range(len(a)): m=max(m,a[i]+b[i]*z)
    s=0.
    for i in range(len(a)): s+=math.exp(a[i]+b[i]*z-m)
    return m+math.log(s)


@njit(cache=True)
def root(a,b,k,left,right,increasing):
    lk=math.log(k*len(a))
    for _ in range(64):
        mid=.5*(left+right)
        above=logsum(a,b,mid)>lk
        if above==increasing: right=mid
        else: left=mid
    return .5*(left+right)


@njit(cache=True)
def integral_tail(a,b,k,x,right):
    s=0.
    for i in range(len(a)):
        prob=phi(b[i]-x) if right else phi(x-b[i])
        s+=math.exp(a[i]+.5*b[i]*b[i])*prob/len(a)
    return s-k*(phi(-x) if right else phi(x))


@njit(cache=True)
def conditional_call(a,b,k):
    """E[(mean(exp(a+b Z))-k)+], handling convex two-root cases."""
    lo=np.min(b); hi=np.max(b)
    if max(abs(lo),abs(hi))<1.e-14:
        return max(np.exp(a).mean()-k,0.)
    if len(a)==1:
        sd=abs(b[0]);d2=(a[0]-math.log(k))/sd
        return max(math.exp(a[0]+.5*sd*sd)*phi(d2+sd)-k*phi(d2),0.)
    if lo>=0. or hi<=0.:
        inc=lo>=0.;left=-8.;right=8.;lk=math.log(k*len(a))
        for _ in range(16):
            if (logsum(a,b,left)>lk)!=inc: break
            left*=2
        for _ in range(16):
            if (logsum(a,b,right)>lk)==inc: break
            right*=2
        x=root(a,b,k,left,right,inc)
        return max(integral_tail(a,b,k,x,inc),0.)
    # A sum of exponentials is convex. Find the unique derivative zero.
    left=-8.;right=8.
    for _ in range(16):
        m=max(a+b*left); der=np.sum(b*np.exp(a+b*left-m))
        if der<0: break
        left*=2
    for _ in range(16):
        m=max(a+b*right); der=np.sum(b*np.exp(a+b*right-m))
        if der>0: break
        right*=2
    for _ in range(64):
        mid=.5*(left+right);m=max(a+b*mid)
        if np.sum(b*np.exp(a+b*mid-m))>0: right=mid
        else: left=mid
    minimum=.5*(left+right)
    if logsum(a,b,minimum)>=math.log(k*len(a)):
        return np.exp(a+.5*b*b).mean()-k
    left=minimum-8.;right=minimum+8.
    for _ in range(16):
        if logsum(a,b,left)>math.log(k*len(a)): break
        left=minimum+2*(left-minimum)
    for _ in range(16):
        if logsum(a,b,right)>math.log(k*len(a)): break
        right=minimum+2*(right-minimum)
    xl=root(a,b,k,left,minimum,False);xr=root(a,b,k,minimum,right,True)
    return max(integral_tail(a,b,k,xl,False)+integral_tail(a,b,k,xr,True),0.)


@njit(cache=True)
def path_values(ds,dv,direction,dates,spot,strike,rate,T,kappa,theta,v0,xi,rho,mode,cap):
    p,n,d=ds.shape
    result=np.empty((p,2))
    dt=T/n;interval=n//dates
    # mode 0: plain fine, 1: adjacent-swap fine, 2: summed-increment coarse.
    step_n=n//2 if mode==2 else n
    h=2*dt if mode==2 else dt
    mon=interval//2 if mode==2 else interval
    for path in range(p):
        logs=np.full(d,math.log(spot));v=np.full(d,v0);slope=np.zeros(d)
        gbm=np.full(d,math.log(spot));gbmslope=np.zeros(d)
        aa=np.empty(d*dates);bb=np.empty(d*dates);ga=0.;gb=0.;idx=0
        for step in range(step_n):
            for asset in range(d):
                if mode==2:
                    ws=ds[path,2*step,asset]+ds[path,2*step+1,asset]
                    wv=dv[path,2*step,asset]+dv[path,2*step+1,asset]
                    direct=2*direction[asset]
                else:
                    j=(step^1) if mode==1 else step
                    ws=ds[path,j,asset];wv=dv[path,j,asset];direct=direction[asset]
                rt=math.sqrt(v[asset])
                logs[asset]+=(rate-.5*v[asset])*h+rt*ws+xi/4*(ws*wv-rho*h)
                slope[asset]+=(rt+xi/4*wv)*direct
                v[asset]=(v[asset]+kappa*theta*h+xi*rt*wv+.25*xi*xi*(wv*wv-h))/(1+kappa*h)
                gbm[asset]+=(rate-.5*theta)*h+math.sqrt(theta)*ws
                gbmslope[asset]+=math.sqrt(theta)*direct
            if (step+1)%mon==0:
                for asset in range(d):
                    aa[idx]=logs[asset];bb[idx]=slope[asset];idx+=1
                    ga+=gbm[asset]/(d*dates);gb+=gbmslope[asset]/(d*dates)
        payoff=conditional_call(aa,bb,strike)
        control=conditional_call(np.array([ga]),np.array([gb]),strike)
        if cap>0:
            payoff-=conditional_call(aa,bb,strike+cap)
            control-=conditional_call(np.array([ga]),np.array([gb]),strike+cap)
        result[path,0]=math.exp(-rate*T)*payoff
        result[path,1]=math.exp(-rate*T)*control
    return result


def values(model,level,power,seed,method='rqmc',conditional=False,correction=False,cap=0.):
    ds,dv,direction=draw_increments(model,level,power,seed,method,conditional)
    args=(ds,dv,direction,model.dates,model.spot,model.strike,model.rate,model.maturity,
          model.kappa,model.theta,model.v0,model.xi,model.leverage)
    fine=path_values(*args,0,cap)
    if not correction: return fine
    if level<1: raise ValueError('corrections require level >= 1')
    swapped=path_values(*args,1,cap);coarse=path_values(*args,2,cap)
    # Control is identical at the contractual dates for these coupled GBM paths.
    return np.column_stack((.5*(fine[:,0]+swapped[:,0])-coarse[:,0],
                            fine[:,0]-coarse[:,0]))


def control_mean(model,cap=0.):
    n=model.dates;T=model.maturity
    mu=math.log(model.spot)+(model.rate-.5*model.theta)*T*(n+1)/(2*n)
    var=model.theta*(1+(model.assets-1)*model.correlation)/model.assets*T*(n+1)*(2*n+1)/(6*n*n)
    def call(k):
        sd=math.sqrt(var);d2=(mu-math.log(k))/sd
        return math.exp(-model.rate*T)*(math.exp(mu+.5*var)*ndtr(d2+sd)-k*ndtr(d2))
    return call(model.strike)-(call(model.strike+cap) if cap>0 else 0.)


def fit_control(model,level,power,seed,conditional=False,cap=0.):
    start=time.perf_counter()
    x=values(model,level,power,seed,'mc',conditional,False,cap)
    cov=np.cov(x.T,ddof=1)
    coefficient=float(cov[0,1]/cov[1,1]) if cov[1,1]>0 else 0.
    return coefficient,time.perf_counter()-start


def seeded(root,*indices):
    return int(np.random.SeedSequence([root,*indices]).generate_state(1)[0])
