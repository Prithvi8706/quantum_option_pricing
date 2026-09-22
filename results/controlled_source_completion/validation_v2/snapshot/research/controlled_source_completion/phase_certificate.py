"""Rational checks of the actual atan coefficients used in the 64-bit circuit."""
from fractions import Fraction as F
from functools import lru_cache
import json
import math
from research.controlled_source_completion.ir import coefficients
from research.controlled_source_completion.cost import phase_error_bound
from research.controlled_source_completion.run import ROOT,dump


def alternating_atan(x,terms=100):
    if x<0:
        lo,hi=alternating_atan(-x,terms);return -hi,-lo
    assert 0<=x<1
    total=F(0);power=x
    for j in range(terms):total+=(-1)**j*power/(2*j+1);power*=x*x
    other=total+(-1)**terms*power/(2*terms+1)
    return min(total,other),max(total,other)


@lru_cache(None)
def pi_bounds():
    a,b=alternating_atan(F(1,5));c,d=alternating_atan(F(1,239))
    return 16*a-4*d,16*b-4*c


def atan_bounds(c):
    if c<=F(1,2):return alternating_atan(c)
    lo,hi=alternating_atan((c-1)/(c+1));pl,ph=pi_bounds()
    return pl/4+lo,ph/4+hi


def exact_coefficient(center,n):
    a=center/(1+center*center);b=1/(1+center*center);real,imag=F(1),F(0)
    for _ in range(n):real,imag=real*a-imag*b,real*b+imag*a
    return (-1)**(n-1)*imag/n


def main():
    f=64;table=coefficients('atan',32,8,f);checked=0
    for i,row in enumerate(table):
        center=F(2*i+1,64);lo,hi=atan_bounds(center)
        assert round(lo*2**f)==round(hi*2**f)==row[0];checked+=1
        for j in range(1,9):assert round(exact_coefficient(center,j)*2**f)==row[j];checked+=1
    pl,ph=pi_bounds();stored=F(round(float(math.pi/2)*2**f),2**f)
    pi_phase_error=2*max(abs(stored-pl/2),abs(stored-ph/2))
    assert pi_phase_error<F(2,10**16)
    h=F(1,64);tail=2*h**9/(9*(1-h));rounding=F(32,2**f);bound=rounding+tail+F(2,10**16)
    dump(ROOT/'validation_v2'/'phase_coefficient_certificate.json',dict(
        fractional_bits=f,exactly_checked_coefficients=checked,
        method='Exact Fraction alternating atan intervals and Machin pi identity for constants; rational complex powers for all positive-degree coefficients.',
        rounding_error_allowance=str(rounding),atan_phase_taylor_remainder_bound=str(tail),
        pi_constant_phase_error_upper=float(pi_phase_error),uniform_phase_bound=float(bound),
        exact_bound=[bound.numerator,bound.denominator],
        assumptions='|Y| and |left| <= 100, normalizer >=16; midpoint segment lookup and clean fixed-point leaves as specified; adaptive left loaded by nearest rounding at 64 bits.',
        proof_location='docs/controlled_source_completion/DERIVATION.md'))
    assert abs(float(bound)-phase_error_bound(f))<1e-30
    print(json.dumps(dict(coefficients_checked=checked,uniform_phase_bound=float(bound))),flush=True)


if __name__=='__main__':main()
