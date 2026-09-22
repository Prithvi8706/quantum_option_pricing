import math
from research.journal_sprint.reversible_fixed_point import basis,read
from .reversible import gbm_step,capped_payoff


def test_small_gbm_step_matches_integer_reference_and_cleans():
    w=10;f=6;dt=.1;sigma=.4;rho=.2;p,ins,outs=gbm_step(w,f,dt,sigma,rho)
    for log,c,i in [(0,20,-31),(17,-100,70),(-80,40,55)]:
        expected=(log+c*round(2**f*sigma*math.sqrt(rho*dt))//2**f+i*round(2**f*sigma*math.sqrt((1-rho)*dt))//2**f+round((.03-.5*sigma**2)*dt*2**f))%2**w
        initial=basis(ins[0],log)|basis(ins[1],c)|basis(ins[2],i)
        assert p.run(initial)==initial|basis(outs[0],expected)


def test_capped_payoff_all_small_inputs():
    p,(x,),(o,)=capped_payoff(7,3,1.,.875,3.)
    for v in range(64):
        expected=min(24,max(v-8,0)*7//8)
        initial=basis(x,v)
        assert p.run(initial)==initial|basis(o,expected)
