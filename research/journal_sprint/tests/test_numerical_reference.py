from fractions import Fraction

import mpmath as mp
import pytest

from research.journal_sprint.numerical_reference import (
    PRECISION,
    case_table,
    cp,
    polynomial,
    preimage,
    reference,
    union,
)
from research.journal_sprint.run_numerical_check import compare


def test_declared_matrix():
    cases = case_table()
    assert len(cases) == len({c["case_id"] for c in cases}) == 312
    assert all(len(c["counts"]) == len(c["depths"]) for c in cases)
    assert all(all(0 <= k <= 128 for k in c["counts"]) for c in cases)


@pytest.mark.parametrize("k,result", [(0, Fraction(1, 4)), (1, 1), (2, Fraction(1, 4))])
def test_polynomial_known_values(k, result):
    assert polynomial(Fraction(1, 4), k) == result
    assert polynomial(Fraction(0), k) == 0
    assert polynomial(Fraction(1), k) == 1


def test_beta_zero_count_closed_form():
    with mp.workdps(PRECISION):
        alpha = mp.mpf(".025")
        lo, hi = cp(0, 128, alpha)
        exact = 1 - (alpha / 2) ** (mp.mpf(1) / 128)
        assert lo == 0
        assert abs(hi - exact) < mp.mpf("1e-45")
        lo2, hi2 = cp(128, 128, alpha)
        assert hi2 == 1 and abs(lo2 - (1 - exact)) < mp.mpf("1e-45")


def test_all_monotone_branches_and_roots():
    with mp.workdps(PRECISION):
        result = preimage(mp.mpf(".1"), mp.mpf(".2"), 2)
        assert len(result) == 5
        for lo, hi in result:
            assert lo < hi
            for endpoint in (lo, hi):
                residual = min(abs(polynomial(endpoint, 2) - mp.mpf(v)) for v in (".1", ".2"))
                assert residual < mp.mpf("1e-44")
        assert preimage(1, 0, 2) == []
        assert preimage(0, 1, 2) == [(0, 1)]


def test_union_does_not_fill_gaps():
    assert union([(0, 0.1), (0.9, 1)]) == [(0, 0.1), (0.9, 1)]
    assert union([(0, 0.5), (0.5, 1)]) == [(0, 1)]


def test_uncertified_contrast_full_fallback():
    case = dict(counts=[0, 128, 0], depths=[0, 1, 2], calibration_errors=[32, 32], guard="0")
    assert reference(case) == [(0, 1)]


def test_small_reference_crosscheck():
    assert compare(case_table()[0])["encloses"]
