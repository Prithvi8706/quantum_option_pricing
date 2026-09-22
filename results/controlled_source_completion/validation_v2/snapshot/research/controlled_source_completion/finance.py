"""Same parity-controlled compound contract, with an explicit finite source."""
from dataclasses import asdict
import json
import math
from pathlib import Path
import numpy as np
from research.controlled_source_completion.ir import Graph,evaluate
from research.compound_feasibility.model import MODELS

TRAINING=Path('results/compound_feasibility/pilot_v1/training.json')


def normals_graph(g,count,q):
    result=[]
    for j in range((count+1)//2):
        rawu=g.input('uniform_%d'%(2*j),q);rawv=g.input('uniform_%d'%(2*j+1),q)
        u=g.add(g.bits(rawu,q-g.f),g.const_int(1<<(g.f-q-1)))
        v=g.add(g.bits(rawv,q-g.f),g.const_int(1<<(g.f-q-1)))
        radius=g.sqrt(g.cmul(g.log(u),-2))
        angle2=g.bits(g.add(v,g.c(.75)),0,g.f)
        result.extend([g.mul(radius,g.cos_unit(v)),g.mul(radius,g.cos_unit(angle2))])
    return result[:count]


def lognormal(g,mu,var,k,mean=None):
    """Both call and put; positive-k formula evaluated behind a safe argument guard."""
    sd=g.sqrt(var);mean=g.exp(g.add(mu,g.cmul(var,.5))) if mean is None else mean
    kk=g.maximum(k,g.const_int(1))
    # Division is unsigned at the leaf. Supply the sign explicitly for d2.
    numerator=g.sub(mu,g.log(kk));sgn=g.lt(numerator,g.c(0))
    dabs=g.div(g.select(sgn,g.neg(numerator),numerator),sd)
    d2=g.select(sgn,g.neg(dabs),dabs);d1=g.add(d2,sd)
    call=g.pos(g.sub(g.mul(mean,g.cdf(d1)),g.mul(k,g.cdf(d2))))
    put=g.pos(g.sub(g.mul(k,g.cdf(g.neg(d2))),g.mul(mean,g.cdf(g.neg(d1)))))
    nonpositive=g.lt(k,g.const_int(1))
    return g.select(nonpositive,g.sub(mean,k),call),g.select(nonpositive,g.c(0),put)


def build_finance(m,f=40,q=32,strikes=(3.,6.,9.)):
    if f<=q:raise ValueError('midpoint inputs need at least q+1 fractional bits')
    fit=json.loads(TRAINING.read_text())[m.name];g=Graph(f);d=m.assets;n=m.dates//2
    dt=m.maturity/m.dates;t=np.arange(1,n+1)*dt;discount=math.exp(-m.rate*m.maturity/2);scale=.5*discount
    zs=normals_graph(g,m.dates*(d+1),q);logs=[g.c(math.log(m.spot))]*d
    past=[];future=[];futurelogs=[];spots_tau=None;logs_tau=None
    lo=g.c(math.log(2**-16));hi=g.c(math.log(4096.))
    for j in range(m.dates):
        common=g.cmul(zs[j*(d+1)],m.sigma*math.sqrt(dt*m.rho))
        for i in range(d):
            step=g.add(common,g.cmul(zs[j*(d+1)+1+i],m.sigma*math.sqrt(dt*(1-m.rho))))
            logs[i]=g.add(logs[i],g.add(step,g.c((m.rate-.5*m.sigma**2)*dt)))
        guarded=[g.clip(x,lo,hi) for x in logs];stocks=[g.exp(x) for x in guarded]
        if j<n:past.extend(stocks)
        else:future.extend(stocks);futurelogs.extend(guarded)
        if j==n-1:
            # Clipped conditional state explicitly defines this digital source.
            spots_tau=stocks;logs_tau=guarded;logs=list(guarded)
    accrued=g.cmul(g.summation(past),1/(d*m.dates));a=g.mean(future);geom=g.exp(g.mean(futurelogs))
    k=g.cmul(g.sub(g.c(m.strike),accrued),2)
    basket=g.mean(spots_tau);ea=g.cmul(basket,float(np.exp(m.rate*t).mean()))
    forward=g.cmul(g.sub(ea,k),scale)
    mint=np.minimum.outer(t,t);vg=m.sigma**2*(m.rho+(1-m.rho)/d)*mint.mean()
    mug=g.add(g.mean(logs_tau),g.c((m.rate-.5*m.sigma**2)*float(t.mean())))
    geocall,geoput=lognormal(g,mug,g.c(vg),k);geocall=g.cmul(geocall,scale);geoput=g.cmul(geoput,scale)
    c0=g.add(forward,geoput);lower=g.maximum(g.maximum(forward,g.c(0)),geocall)
    upperterms=[]
    for tj in t:
        for l in logs_tau:
            call,_=lognormal(g,g.add(l,g.c((m.rate-.5*m.sigma**2)*tj)),g.c(m.sigma**2*tj),k)
            upperterms.append(call)
    upper=g.maximum(lower,g.minimum(c0,g.cmul(g.mean(upperterms),scale)))
    weights=np.exp(m.rate*(t[:,None]+t[None,:]))
    common=float(np.mean(weights*np.exp(m.sigma**2*m.rho*mint)))
    extra=float(np.mean(weights*(np.exp(m.sigma**2*mint)-np.exp(m.sigma**2*m.rho*mint))))
    total=g.summation(spots_tau);squares=g.summation([g.mul(s,s) for s in spots_tau])
    second=g.cmul(g.add(g.cmul(g.mul(total,total),common),g.cmul(squares,extra)),1/(d*d))
    ratio=g.maximum(g.div(second,g.mul(ea,ea)),g.const_int(2**f+1))
    variance=g.maximum(g.log(ratio),g.const_int(1));mu=g.sub(g.log(ea),g.cmul(variance,.5))
    mm,_=lognormal(g,mu,variance,k,mean=ea);mm=g.cmul(mm,scale);prediction=mm
    if fit['selected']=='regression':
        dispersion=g.div(g.sqrt(g.pos(g.sub(g.cmul(squares,1/d),g.mul(basket,basket)))),basket)
        z=g.clip(g.cmul(g.sub(g.add(accrued,g.cmul(basket,.5)),g.c(m.strike)),1/(m.spot*m.sigma*math.sqrt(m.maturity))),g.c(-5),g.c(5))
        z2=g.mul(z,z);gap=g.sub(mm,geocall)
        features=[g.c(1),z,z2,g.mul(z2,z),dispersion,g.mul(dispersion,dispersion),gap,
                  g.mul(gap,z),g.mul(gap,z2),g.mul(gap,dispersion),g.sub(g.cmul(basket,.01),g.c(1)),g.sub(g.cmul(accrued,.02),g.c(1))]
        prediction=g.add(mm,g.summation([g.cmul(x,c) for x,c in zip(features,fit['coef'])]))
    prediction=g.clip(prediction,lower,upper)
    residual=g.pos(g.cmul(g.sub(g.pos(g.sub(k,geom)),g.pos(g.sub(k,a))),scale))
    offset=g.sub(c0,prediction);support=discount*m.strike
    g.outputs=dict(accrued=accrued,average=a,geometric=geom,forward=forward,geoput=geoput,
                   c0=c0,lower=lower,upper=upper,prediction=prediction,residual=residual,offset=offset)
    for kc in strikes:
        active=g.lt(g.c(kc),prediction)
        y=g.select(active,g.sub(offset,residual),g.c(0))
        g.outputs['Y_%g'%kc]=g.clip(y,g.c(-support),g.c(support))
        g.outputs['base_%g'%kc]=g.cmul(g.pos(g.sub(prediction,g.c(kc))),discount)
    g.meta=dict(model=asdict(m),random_bits=q,fit=fit,spot_guard=[2**-16,4096.],
                root_seed=2026092601,law='independent midpoint uniforms, paired Box-Muller; reset to guarded tau state',
                continuous_bridge='NOT CERTIFIED',support=support)
    return g


def prune(data,output_names):
    """Dead-code elimination before resource counting; preserve all random inputs."""
    keep=set(data['outputs'][k] for k in output_names);nodes=[]
    for node in reversed(data['nodes']):
        if node['op']=='input' or keep.intersection(node['out']):
            nodes.append(node);keep.update(node['args'])
    # Renumber because evaluators use contiguous SSA words.
    mapping={};outnodes=[]
    for node in reversed(nodes):
        new=dict(node);new['args']=[mapping[i] for i in node['args']]
        new['out']=[]
        for i in node['out']:mapping[i]=len(mapping);new['out'].append(mapping[i])
        outnodes.append(new)
    return dict(data,nodes=outnodes,inputs=[mapping[i] for i in data['inputs']],
                outputs={k:mapping[data['outputs'][k]] for k in output_names})


def float_reference(m,uniform_integers,q,strikes=(3.,6.,9.)):
    """Independent NumPy/SciPy real-arithmetic evaluation on the same finite inputs."""
    from research.controlled_residual_feasibility.parity import bounds,prediction
    fit=json.loads(TRAINING.read_text())[m.name]
    u=(np.asarray(uniform_integers,float)+.5)/2**q;radius=np.sqrt(-2*np.log(u[0::2]));angle=2*np.pi*u[1::2]
    z=np.column_stack((radius*np.cos(angle),radius*np.sin(angle))).ravel()[:m.dates*(m.assets+1)]
    z=z.reshape(m.dates,m.assets+1);dt=m.maturity/m.dates
    increments=(m.rate-.5*m.sigma**2)*dt+m.sigma*math.sqrt(dt)*(math.sqrt(m.rho)*z[:,:1]+math.sqrt(1-m.rho)*z[:,1:])
    n=m.dates//2;raw=np.log(m.spot)+np.cumsum(increments[:n],axis=0)
    pastlogs=np.clip(raw,math.log(2**-16),math.log(4096));stocks=np.exp(pastlogs)
    spots=stocks[-1:];accrued=np.array([stocks.sum()/(m.dates*m.assets)])
    futurelogs=np.clip(pastlogs[-1]+np.cumsum(increments[n:],axis=0),math.log(2**-16),math.log(4096))
    a=np.exp(futurelogs).mean();geo=np.exp(futurelogs.mean());k=2*(m.strike-accrued[0]);disc=math.exp(-m.rate*m.maturity/2)
    b=bounds(m,spots,accrued);pred=float(prediction(m,spots,accrued,fit,b)[0]);r=.5*disc*(max(k-geo,0)-max(k-a,0));offset=float(b['c0'][0])-pred
    out=dict(accrued=float(accrued[0]),average=a,geometric=geo,forward=float(b['forward'][0]),geoput=float(b['put'][0]),
             c0=float(b['c0'][0]),lower=float(b['lower'][0]),upper=float(b['upper'][0]),prediction=pred,residual=r,offset=offset)
    for kc in strikes:out['Y_%g'%kc]=np.clip((offset-r) if pred>kc else 0.,-disc*m.strike,disc*m.strike);out['base_%g'%kc]=disc*max(pred-kc,0)
    return out
