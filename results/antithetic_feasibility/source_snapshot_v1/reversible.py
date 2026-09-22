"""Actually emitted reversible kernels; modular arithmetic, not price certificates."""
import math
from research.journal_sprint.reversible_fixed_point import (
    Program, add, subtract, copy, constant, fixed_multiply, less_than, positive_part,
)
from research.stronger_arithmetic.circuits import clean_exp


def constant_product(p,x,out,c,f):
    """out XOR floor(signed(x)*c/2**f) mod 2**w, shift-add implementation."""
    w=len(x);prod=p.register(2*w);extended=p.register(2*w);helper=p.register(1)[0]
    start=len(p.gates)
    for i,b in enumerate(extended):p.gate(x[min(i,w-1)],b)
    for i in range(abs(c).bit_length()):
        if (abs(c)>>i)&1:
            (add if c>0 else subtract)(p,extended[:2*w-i],prod[i:],helper)
    end=len(p.gates)
    copy(p,prod[f:f+w],out);p.undo(start,end)


def clean_sqrt(p,x,out,f):
    """out XOR floor(sqrt(unsigned(x)*2**f)); digit-by-digit exact square root.

    Stored remainders allow full inverse cleanup. Caller requires a nonnegative
    signed operand and separately interprets the fixed-point rounding error.
    """
    w=len(x);radbits=w+f;k=(radbits+1)//2;rwidth=w+2
    roots=p.register(w);remainders=[p.register(rwidth) for _ in range(k+1)]
    trial=p.register(rwidth);conditional=p.register(rwidth)
    diff=p.register(rwidth+1);ext=p.register(rwidth+1);helper=p.register(1)[0]
    start=len(p.gates)
    for stage in range(k):
        j=k-1-stage;prev=remainders[stage];nxt=remainders[stage+1]
        for z in range(rwidth-2):p.gate(prev[z],nxt[z+2])
        for bit in (0,1):
            index=2*j+bit-f
            if 0<=index<w:p.gate(x[index],nxt[bit])
        constant(p,trial,1)
        for z in range(j+1,k):p.gate(roots[z],trial[z-j+1])
        less_than(p,nxt,trial,roots[j],diff,ext,helper)
        p.gate(roots[j])
        for z in range(rwidth):p.gate(roots[j],trial[z],conditional[z])
        subtract(p,conditional,nxt,helper)
        for z in range(rwidth):p.gate(roots[j],trial[z],conditional[z])
        for z in range(j+1,k):p.gate(roots[z],trial[z-j+1])
        constant(p,trial,1)
    end=len(p.gates);copy(p,roots,out);p.undo(start,end)


class Builder:
    """Small SSA graph: temporaries retained until output copy and inverse."""
    def __init__(self,p,w,f):
        self.p=p;self.w=w;self.f=f
        self.prod=p.register(2*w);self.partial=p.register(2*w);self.dup=p.register(w)
        self.helper=p.register(1)[0]
    def word(self):return self.p.register(self.w)
    def mul(self,a,b):
        o=self.word()
        if a==b:
            copy(self.p,b,self.dup)
            fixed_multiply(self.p,a,self.dup,o,self.f,self.prod,self.partial,self.helper)
            copy(self.p,b,self.dup)
        else:fixed_multiply(self.p,a,b,o,self.f,self.prod,self.partial,self.helper)
        return o
    def cmul(self,a,c):
        o=self.word();constant_product(self.p,a,o,round(c*2**self.f),self.f);return o
    def summation(self,terms,c=0.):
        o=self.word();constant(self.p,o,round(c*2**self.f))
        for t in terms:add(self.p,t,o,self.helper)
        return o


def step_program(w,f,h,kappa=2.,theta=.09,xi=.3,rho=-.5,rate=.03):
    """Clean log-relative-spot / variance update from fixed-point Brownian inputs."""
    p=Program(compact=True)
    log,v,ws,wv=[p.register(w) for _ in range(4)]
    outlog,outv=p.register(w),p.register(w)
    b=Builder(p,w,f);start=len(p.gates)
    rt=b.word();clean_sqrt(p,v,rt,f)
    price=b.mul(rt,ws);cross=b.mul(ws,wv);vol=b.mul(rt,wv);vv=b.mul(wv,wv)
    drift=b.cmul(v,-.5*h);cross2=b.cmul(cross,xi/4)
    lv=b.summation([log,price,drift,cross2],(rate-xi*rho/4)*h)
    vol2=b.cmul(vol,xi);vv2=b.cmul(vv,xi*xi/4)
    numerator=b.summation([v,vol2,vv2],(kappa*theta-xi*xi/4)*h)
    nv=b.cmul(numerator,1/(1+kappa*h))
    end=len(p.gates);copy(p,lv,outlog);copy(p,nv,outv);p.undo(start,end)
    return p,(log,v,ws,wv),(outlog,outv)


def sqrt_program(w,f):
    p=Program(compact=True);x=p.register(w);out=p.register(w)
    clean_sqrt(p,x,out,f);return p,(x,),(out,)


def exp_program(w,f):
    p=Program(compact=True);x=p.register(w);out=p.register(w)
    coeff=[round(2**f/math.factorial(j)) for j in range(13)]
    clean_exp(p,x,out,coeff,f,5,100)
    return p,(x,),(out,)


def primitive_program(name,w,f,c=.3):
    p=Program(compact=True);a=p.register(w);b=p.register(w);out=p.register(w)
    if name=='multiply':
        fixed_multiply(p,a,b,out,f,p.register(2*w),p.register(2*w),p.register(1)[0])
    elif name=='constant_product':constant_product(p,a,out,round(c*2**f),f)
    elif name=='add':add(p,a,b,p.register(1)[0])
    elif name=='positive':positive_part(p,a,out)
    elif name=='compare':less_than(p,a,b,out[0],p.register(w+1),p.register(w+1),p.register(1)[0])
    else:raise ValueError(name)
    return p,(a,b),(out,)


def clifford_t_resources(p):
    """Exact gate counts and unlimited-connectivity ASAP depths of emitted gates.

    Standard exact seven-T Toffoli is expanded explicitly. Non-T gates propagate
    dependencies in the T-depth schedule; T and Tdag increment that schedule.
    This is a logical schedule, not a physical routing schedule.
    """
    tlevels=[0]*p.qubits;levels=[0]*p.qubits
    count={'x':0,'h':0,'cx':0,'t':0,'tdg':0,'ccx_source':0}
    for g in p.gates:
        if len(g)==1:expanded=[('x',g)]
        elif len(g)==2:expanded=[('cx',g)]
        else:
            a,b,c=g;count['ccx_source']+=1
            expanded=[('h',(c,)),('cx',(b,c)),('tdg',(c,)),('cx',(a,c)),
                      ('t',(c,)),('cx',(b,c)),('tdg',(c,)),('cx',(a,c)),
                      ('t',(b,)),('t',(c,)),('h',(c,)),('cx',(a,b)),
                      ('t',(a,)),('tdg',(b,)),('cx',(a,b))]
        for name,bits in expanded:
            count[name]+=1
            lt=max(tlevels[z] for z in bits)+(1 if name in ('t','tdg') else 0)
            la=max(levels[z] for z in bits)+1
            for z in bits:tlevels[z]=lt;levels[z]=la
    return dict(qubits=p.qubits,source_gates=len(p.gates),**count,
                t_count=count['t']+count['tdg'],t_depth=max(tlevels,default=0),
                clifford_t_depth=max(levels,default=0),schedule='all-to-all ASAP exact seven-T decomposition')
