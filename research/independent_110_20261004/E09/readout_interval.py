"""Owned numerical extraction of frozen F23 dyadic120 routines; no finance code."""
import math
import functools
from fractions import Fraction as Q
SCALE=1<<120
guard=lambda: None
PI=None

def down(v):
    v=Q(v)
    return Q((v.numerator*SCALE)//v.denominator,SCALE)


def up(v):
    return -down(-Q(v))


class I:
    def __init__(self, lo, hi=None):
        self.lo, self.hi=down(lo),up(lo if hi is None else hi)
        assert self.lo<=self.hi
    def __add__(self,o):
        o=o if isinstance(o,I) else I(o)
        return I(self.lo+o.lo,self.hi+o.hi)
    def __sub__(self,o):
        o=o if isinstance(o,I) else I(o)
        return I(self.lo-o.hi,self.hi-o.lo)
    def __mul__(self,o):
        o=o if isinstance(o,I) else I(o)
        v=[a*b for a in (self.lo,self.hi) for b in (o.lo,o.hi)]
        return I(min(v),max(v))
    def __truediv__(self,o):
        o=o if isinstance(o,I) else I(o)
        assert o.lo>0 or o.hi<0
        return self*I(1/o.hi,1/o.lo)
    def square(self):
        return I(0 if self.lo<=0<=self.hi else min(self.lo*self.lo,self.hi*self.hi),max(self.lo*self.lo,self.hi*self.hi))
    def sqrt(self):
        assert self.lo>=0
        def root(v):
            k=math.isqrt((v.numerator*SCALE*SCALE)//v.denominator)
            return k
        a,b=root(self.lo),root(self.hi)
        return I(Q(a,SCALE),Q(b if Q(b,SCALE)**2==self.hi else b+1,SCALE))
    def pair(self):
        return {"lower_exact":[self.lo.numerator,self.lo.denominator],"upper_exact":[self.hi.numerator,self.hi.denominator]}


def atan_inverse(n,terms):
    partial=sum((Q((-1)**k,(2*k+1)*n**(2*k+1)) for k in range(terms)),Q(0))
    next_term=Q((-1)**terms,(2*terms+1)*n**(2*terms+1))
    return I(min(partial,partial+next_term),max(partial,partial+next_term))


def pi_interval():
    return atan_inverse(5,60)*16-atan_inverse(239,20)*4


@functools.lru_cache(maxsize=2048)
def sin_ratio(r):
    guard()
    r=r%2
    sign=1
    if r>1:
        sign=-1
        r-=1
    if r>Q(1,2):
        r=1-r
    if r==0:
        return I(0)
    x=PI*I(r)
    x2=x.square()
    term,total=x,x
    for k in range(1,32):
        term=(term*x2)/I((2*k)*(2*k+1))
        total=total-term if k%2 else total+term
    rem=Q(2**65,math.factorial(65))
    result=I(max(0,total.lo-rem),min(1,total.hi+rem))
    return result*sign

