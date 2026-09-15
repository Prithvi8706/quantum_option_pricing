import math

import mpmath as mp
import pytest
from scipy.special import betaln

from research.journal_sprint.pilot_cs import pilot_interval


@pytest.mark.parametrize("pilot", [0, 4, 8])
def test_conditional_mixture_expectation(pilot):
    a, b = pilot + 0.5, 8 - pilot + 0.5
    n = 12
    for q in (0.1, 0.5, 0.9):
        value = sum(
            math.comb(n, s)
            * q**s
            * (1 - q) ** (n - s)
            * math.exp(
                betaln(s + a, n - s + b) - betaln(a, b) - s * math.log(q) - (n - s) * math.log1p(-q)
            )
            for s in range(n + 1)
        )
        assert abs(value - 1) < 1e-12


@pytest.mark.parametrize(
    "s,n,pilot", [(1050, 32768, 32), (50000, 100000, 512), (1024, 32768, 1024)]
)
def test_high_precision_pilot_boundary(s, n, pilot):
    lo, hi = pilot_interval(s, n, pilot)
    with mp.workdps(80):
        a, b = mp.mpf(pilot) + mp.mpf(".5"), mp.mpf(1024 - pilot) + mp.mpf(".5")
        count, total = s - pilot, n - 1024
        constant = mp.log(mp.beta(count + a, total - count + b) / mp.beta(a, b))
        for q in (lo, hi):
            if 0 < q < 1:
                x = mp.mpf(q)
                value = constant - count * mp.log(x) - (total - count) * mp.log1p(-x)
                assert value >= mp.log(40)


def test_pilot_never_certifies_itself():
    assert pilot_interval(400, 1024, 400) == (0.0, 1.0)
    for args in [(0, 1023, 0), (5, 1025, 7), (True, 1024, 1)]:
        with pytest.raises(ValueError):
            pilot_interval(*args)
