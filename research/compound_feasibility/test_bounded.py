import math
import numpy as np
from .model import *
from .bounded_iid import iid_means


def test_iid_future_scenarios_are_disjoint_by_outer_state():
    m=MODELS[0];cap,_=choose_cap(m);s,a=outer_states(m,3,813,'mc');f,g=future_factors(m,6,516,'mc')
    fast=iid_means(s,a,f,g,8,m.strike,math.exp(-m.rate*m.maturity/2),cap)
    ref=[]
    for i in range(8):
        residual,_=inner_samples(s[i:i+1],a[i:i+1],f[i*8:(i+1)*8],g[i*8:(i+1)*8],m.strike,math.exp(-m.rate*m.maturity/2),cap)
        ref.append(residual.mean())
    np.testing.assert_allclose(fast,ref,atol=1e-12)
