"""Finite fixed-point SSA and elementary functions; every leaf has a circuit.

This is an executable digital target. No floating-point financial certificate
is inferred from its existence. Tables are small one-dimensional coefficients,
never a table of paths/prices, and are included in the emitted QROM circuits.
"""
import math
import json
from functools import lru_cache
import mpmath as mp


@lru_cache(None)
def coefficients(name,segments,degree,f):
    mp.mp.dps=90
    if name=='log':a,b=mp.mpf(1),mp.mpf(2);fn=mp.log
    elif name=='cdf':a,b=mp.mpf(-8),mp.mpf(8);fn=lambda x:(1+mp.erf(x/mp.sqrt(2)))/2
    elif name=='cos':a,b=mp.mpf(0),mp.mpf(1);fn=lambda x:mp.cos(2*mp.pi*x)
    elif name=='atan':a,b=mp.mpf(0),mp.mpf(1);fn=mp.atan
    else:raise ValueError(name)
    rows=[]
    for i in range(segments):
        center=a+(i+mp.mpf('.5'))*(b-a)/segments
        rows.append(tuple(int(mp.nint(c*2**f)) for c in mp.taylor(fn,center,degree)))
    return tuple(rows)


class Graph:
    def __init__(self,f=40,integer_bits=32):
        self.f=f;self.w=f+integer_bits;self.nodes=[];self.values=0;self.constants={};self.inputs=[];self.tables={};self.outputs={}
    def node(self,op,args=(),params=None,nout=1):
        ids=tuple(range(self.values,self.values+nout));self.values+=nout
        self.nodes.append(dict(op=op,args=list(args),params=params or {},out=list(ids)))
        return ids[0] if nout==1 else ids
    def input(self,name,bits,preparation='uniform'):
        x=self.node('input',params=dict(name=name,bits=bits,preparation=preparation));self.inputs.append(x);return x
    def const_int(self,value):
        value=int(value)
        if value not in self.constants:self.constants[value]=self.node('const',params=dict(value=value))
        return self.constants[value]
    def c(self,value):return self.const_int(round(float(value)*2**self.f))
    def add(self,a,b):return self.node('add',(a,b))
    def sub(self,a,b):return self.node('sub',(a,b))
    def mul(self,a,b):return self.node('mul',(a,b))
    def cmul(self,a,c):return self.node('cmul',(a,),dict(c=round(float(c)*2**self.f)))
    def lt(self,a,b):return self.node('lt',(a,b))
    def select(self,flag,a,b):return self.node('select',(flag,a,b))
    def pos(self,a):return self.node('positive',(a,))
    def neg(self,a):return self.sub(self.c(0),a)
    def maximum(self,a,b):return self.select(self.lt(a,b),b,a)
    def minimum(self,a,b):return self.select(self.lt(a,b),a,b)
    def clip(self,x,lo,hi):return self.minimum(self.maximum(x,lo),hi)
    def summation(self,xs):
        cur=self.c(0)
        for x in xs:cur=self.add(cur,x)
        return cur
    def mean(self,xs):return self.cmul(self.summation(xs),1/len(xs))
    def bits(self,x,shift,width=None,signed=False):
        return self.node('bits',(x,),dict(shift=shift,width=self.w if width is None else width,signed=signed))
    def shift(self,x,k):return self.node('shift',(x,k))
    def div(self,a,b):return self.node('divide',(a,self.maximum(b,self.const_int(1))))
    def sqrt(self,a):return self.node('sqrt',(self.pos(a),))
    def interpolate(self,name,x):
        specs={'log':(1.,2.,32,8),'cdf':(-8.,8.,256,7),'cos':(0.,1.,64,7),'atan':(0.,1.,32,8)}
        a,b,n,degree=specs[name];step=(b-a)/n
        xx=self.clip(x,self.c(a),self.const_int(round(b*2**self.f)-1))
        index=self.bits(self.sub(xx,self.c(a)),self.f+int(round(math.log2(step))),int(math.log2(n)))
        center=self.add(self.bits(index,-(self.f+int(round(math.log2(step))))),self.c(a+step/2))
        local=self.sub(xx,center);table=coefficients(name,n,degree,self.f);self.tables[name]=table
        cs=self.node('lookup',(index,),dict(table=name,bits=int(math.log2(n))),degree+1)
        p=cs[-1]
        for c in reversed(cs[:-1]):p=self.add(self.mul(p,local),c)
        return p
    def log(self,x):
        x=self.maximum(x,self.const_int(1));top=self.node('msb',(x,));exponent=self.sub(top,self.const_int(self.f))
        mantissa=self.shift(x,self.neg(exponent))
        return self.add(self.interpolate('log',mantissa),self.cmul(self.bits(exponent,-self.f),math.log(2)))
    def exp(self,x):
        # Range-reduce, evaluate Taylor on [0,ln2], then a reversible bit shift.
        k=self.bits(self.cmul(x,1/math.log(2)),self.f,signed=True)
        r=self.sub(x,self.cmul(self.bits(k,-self.f),math.log(2)))
        p=self.c(1/math.factorial(12))
        for j in range(11,-1,-1):p=self.add(self.mul(p,r),self.c(1/math.factorial(j)))
        return self.shift(p,k)
    def cdf(self,x):
        p=self.interpolate('cdf',x)
        p=self.select(self.lt(x,self.c(-8)),self.c(0),p)
        return self.select(self.lt(self.c(8),x),self.c(1),p)
    def cos_unit(self,u):return self.interpolate('cos',u)
    def atan(self,x):
        sign=self.lt(x,self.c(0));mag=self.select(sign,self.neg(x),x);large=self.lt(self.c(1),mag)
        reduced=self.select(large,self.div(self.c(1),mag),mag)
        small=self.interpolate('atan',reduced)
        value=self.select(large,self.sub(self.c(math.pi/2),small),small)
        return self.select(sign,self.neg(value),value)
    def as_dict(self):
        return dict(format='reversible-fixed-point-ssa-v1',fraction_bits=self.f,width=self.w,
                    nodes=self.nodes,inputs=self.inputs,outputs=self.outputs,tables=self.tables,
                    semantics='Signed two-complement fixed-point; flags and indexes are unscaled integers; all output arithmetic is modulo 2^width.')
    def dump(self,path):path.write_text(json.dumps(self.as_dict(),separators=(',',':'))+'\n')


def evaluate(data,inputs,trace=False):
    w=data['width'];f=data['fraction_bits'];mask=2**w-1;sign=2**(w-1);vals=[0]*sum(len(n['out']) for n in data['nodes'])
    def signed(x):return x-2**w if x&sign else x
    for n in data['nodes']:
        op=n['op'];p=n['params'];raw=[vals[i] for i in n['args']];v=[signed(x) for x in raw]
        if op=='input':result=[int(inputs[p['name']])]
        elif op=='const':result=[p['value']]
        elif op=='add':result=[v[0]+v[1]]
        elif op=='sub':result=[v[0]-v[1]]
        elif op=='mul':result=[(v[0]*v[1])>>f]
        elif op=='cmul':result=[(v[0]*p['c'])>>f]
        elif op=='lt':result=[int(v[0]<v[1])]
        elif op=='select':result=[raw[1] if raw[0]&1 else raw[2]]
        elif op=='positive':result=[max(v[0],0)]
        elif op=='divide':result=[((raw[0]<<f)//raw[1]) if raw[1] else mask]
        elif op=='sqrt':result=[math.isqrt(raw[0]<<f)]
        elif op=='msb':result=[max(0,raw[0].bit_length()-1)]
        elif op=='shift':
            k=v[1]
            result=[0 if k>=w else (-1 if v[0]<0 else 0) if k<=-w else v[0]<<k if k>=0 else v[0]>>-k]
        elif op=='bits':
            x=v[0] if p.get('signed') else raw[0];shift=p['shift']
            result=[(x>>shift if shift>=0 else x<<-shift)&((1<<p['width'])-1)]
        elif op=='lookup':result=data['tables'][p['table']][raw[0]&((1<<p['bits'])-1)]
        else:raise ValueError(op)
        for i,z in zip(n['out'],result):vals[i]=int(z)&mask
    output={k:signed(vals[i])/2**f for k,i in data['outputs'].items()}
    return (output,vals) if trace else output
