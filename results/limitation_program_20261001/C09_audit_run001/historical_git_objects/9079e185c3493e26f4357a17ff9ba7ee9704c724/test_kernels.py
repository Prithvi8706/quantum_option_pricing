import os
import sys

import numpy as np
import pytest

from research.frontier_classical_20261001.basis import canonical_factor
from research.frontier_classical_20261001.kernels import ESTIMANDS, knockout_preint, six_estimands

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "advantage_frontier_20260923"))
import barrier_fast_classical as p3  # noqa: E402
import classical_exponent_pilot as p1  # noqa: E402


def points(na, nt, n=512, seed=7):
    L, mu = p3.setup(na, nt)
    z = np.random.default_rng(seed).standard_normal((n, na * nt))
    return L, mu, z, z @ L.T + mu


@pytest.mark.parametrize("na,nt", [(4, 12), (8, 52)])
def test_knockout_preint_matches_p3(na, nt):
    L, mu, z, x = points(na, nt)
    v = np.ascontiguousarray(L[:, 0])
    disc = np.exp(-p3.RATE * p3.T)
    old = p3.estimand(x, np.ascontiguousarray(z[:, 0]), v, na, nt, disc)
    new = knockout_preint(x, np.ascontiguousarray(z[:, 0]), v, na, nt, disc, p3.K, p3.H)
    assert np.allclose(new, old, rtol=1e-12, atol=1e-12)


@pytest.mark.parametrize("na,nt", [(4, 12), (8, 52)])
def test_six_estimands_match_p1(na, nt):
    case = p1.Case(f"B{na}x{nt}", na, nt)
    z = np.random.default_rng(11).standard_normal((512, case.dim))
    ref = p1.evaluate(case, z)
    x = z @ case.L.T + case.mu
    got = six_estimands(x, np.ascontiguousarray(z[:, 0]), np.ascontiguousarray(case.v),
                        na, nt, case.disc, case.K, case.H)
    names = dict(call="call", digital="digital", knockout="barrier", call_pre="call_pre",
                 digital_pre="digital_pre", knockout_pre="barrier_pre")
    for j, name in enumerate(ESTIMANDS):
        assert np.allclose(got[:, j], ref[names[name]], rtol=1e-11, atol=1e-11), name


def test_preintegration_is_unbiased_with_canonical_basis():
    na, nt = 4, 12
    L, _ = canonical_factor(na, nt, p3.SIGMA, p3.CORR, p3.T)
    _, mu = p3.setup(na, nt)
    z = np.random.default_rng(3).standard_normal((200_000, na * nt))
    got = six_estimands(z @ L.T + mu, np.ascontiguousarray(z[:, 0]),
                        np.ascontiguousarray(L[:, 0]), na, nt, np.exp(-p3.RATE * p3.T),
                        p3.K, p3.H)
    for plain, pre in ((0, 3), (1, 4), (2, 5)):
        diff = got[:, plain] - got[:, pre]
        assert abs(diff.mean()) < 4 * diff.std() / np.sqrt(len(diff)), ESTIMANDS[plain]
