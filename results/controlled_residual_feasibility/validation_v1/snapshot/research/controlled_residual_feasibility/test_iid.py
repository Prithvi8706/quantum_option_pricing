import math
from .parity_iid import eb_radius


def test_zero_observations_still_have_positive_confidence_radius():
    n=2**20;r=eb_radius(0.,n,100.,.001)
    assert r>0
    assert math.isclose(r,7*100*math.log(4000)/(3*(n-1)))


def test_failure_split_and_sample_scaling():
    assert eb_radius(.2,2**20,100.,.0005)>eb_radius(.2,2**20,100.,.001)
    assert eb_radius(.2,2**21,100.,.001)<eb_radius(.2,2**20,100.,.001)
