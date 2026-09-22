"""Actual clean GBM log step and capped-payoff X/CX/CCX streams."""
import math
from research.journal_sprint.reversible_fixed_point import Program,copy,constant,positive_part,less_than
from research.antithetic_feasibility.reversible import Builder


def gbm_step(w,f,dt,sigma,rho,rate=.03):
    p=Program(compact=True);log,common,idio=[p.register(w) for _ in range(3)];out=p.register(w)
    b=Builder(p,w,f);start=len(p.gates)
    x=b.cmul(common,sigma*math.sqrt(rho*dt));y=b.cmul(idio,sigma*math.sqrt((1-rho)*dt))
    z=b.summation([log,x,y],(rate-.5*sigma*sigma)*dt)
    end=len(p.gates);copy(p,z,out);p.undo(start,end)
    return p,(log,common,idio),(out,)


def capped_payoff(w,f,strike,discount,cap):
    p=Program(compact=True);average=p.register(w);out=p.register(w);b=Builder(p,w,f);start=len(p.gates)
    diff=b.summation([average],-strike);pos=b.word();positive_part(p,diff,pos);value=b.cmul(pos,discount)
    limit=b.word();constant(p,limit,round(cap*2**f));flag=p.register(1)[0]
    less_than(p,limit,value,flag,p.register(w+1),p.register(w+1),p.register(1)[0])
    change=b.word();copy(p,value,change);copy(p,limit,change)
    # Flip value to cap in a separate temporary, then copy and uncompute all work.
    capped=b.word();copy(p,value,capped)
    for a,o in zip(change,capped):p.gate(flag,a,o)
    end=len(p.gates);copy(p,capped,out);p.undo(start,end)
    return p,(average,),(out,)
