import math
import os
import sys

import numpy as np
from scipy.special import ndtri as scipy_ndtri

from research.frontier_classical_20261001.oss import ndtri, oss_params, oss_paths
from research.frontier_classical_20261001.scrambles import Case

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "advantage_frontier_20260923"))
import barrier_oss_pilot as p2  # noqa: E402


def test_as241_matches_scipy_including_tails():
    ps = np.concatenate([np.logspace(-300, -1, 400), np.linspace(0.01, 0.99, 400),
                         1 - np.logspace(-15, -1, 100)])
    for p in ps:
        ref = scipy_ndtri(p)
        assert abs(ndtri(p) - ref) <= 1e-13 * max(1.0, abs(ref)), p


def test_oss_matches_p2_on_identical_uniforms():
    for na, nt in ((4, 12), (8, 52)):
        u = np.random.default_rng(9).random((256, na * nt))
        B = p2.asset_pca(na)
        old, _ = p2.oss_estimate(u, na, nt, B)
        params = list(oss_params(Case(0, na, nt)))
        params[2] = np.ascontiguousarray(B)
        new = oss_paths(u, *params)
        assert np.allclose(new, old, rtol=1e-9, atol=1e-12)


def test_oss_is_unbiased_with_canonical_basis():
    u = np.random.default_rng(4).random((2 ** 17, 48))
    y = oss_paths(u, *oss_params(Case(0, 4, 12)))
    assert abs(y.mean() - 3.5188852273893136) < 4 * y.std() / math.sqrt(len(y))
