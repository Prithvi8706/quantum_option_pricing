import math
import numpy as np
from .model import *
from .streaming import residual_means


def test_streaming_matches_matrix_estimator_same_paths():
    for m in MODELS:
        cap,_=choose_cap(m);s,a=outer_states(m,5,1961);f,g=future_factors(m,6,124)
        residual,_=inner_samples(s,a,f,g,m.strike,math.exp(-m.rate*m.maturity/2),cap)
        fast=residual_means(s,a,f,g,m.strike,math.exp(-m.rate*m.maturity/2),cap)
        np.testing.assert_allclose(fast,residual.mean(axis=1),atol=1e-12,rtol=1e-12)
