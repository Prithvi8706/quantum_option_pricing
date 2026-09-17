import math
import pytest
from research.journal_sprint.week2_decoding import amplitude_interval, median_price


@pytest.mark.parametrize('M',[2,8,1024])
def test_outcome_decoding(M):
    for y in (0,1,M//2,M-1):
        a = amplitude_interval(y,M)
        assert 0<=a.lo<=a.hi<=1
        assert float(a.lo)==pytest.approx(math.sin(math.pi*y/M)**2,abs=2e-15)
        assert float(a.hi-a.lo)<1e-60


def test_median_price_and_validation():
    result = median_price([1,2,3],8,10.,2.)
    assert result['value']==pytest.approx(10.)
    assert float(result['rounding_upper'])<1e-12
    with pytest.raises(ValueError):
        amplitude_interval(8,8)
    with pytest.raises(ValueError):
        median_price([1,2],8,10.,2.)
