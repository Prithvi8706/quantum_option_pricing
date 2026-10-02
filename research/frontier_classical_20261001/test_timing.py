import numpy as np
from scipy.stats import qmc

from research.frontier_classical_20261001.oss import (bridge_plan, oss_bb_dims, oss_bb_paths,
                                                      oss_params, oss_paths)
from research.frontier_classical_20261001.scrambles import Case, run_scramble
from research.frontier_classical_20261001.timing import timed_chunk, timed_scramble

CASE = Case(0, 4, 12)
KEY = (2026100121, 0, 1, 0, 3)


def test_timed_preint_and_rqmc_match_rate_runs():
    rate = run_scramble((CASE, "canonical", KEY, 13))
    for method, col in (("preint", 5), ("rqmc", 2)):
        timed = timed_scramble(("t", CASE, method, KEY, 2 ** 13))
        for m in (10, 13):
            assert np.isclose(timed["prefix"][2 ** m], rate["prefix"][col, rate["ms"].index(m)],
                              rtol=1e-12, atol=0)


def test_timed_oss_methods_match_direct_kernels():
    u = qmc.Sobol(48, scramble=True, seed=np.random.default_rng(list(KEY))).random(2 ** 12)
    direct = {"oss": oss_paths(u, *oss_params(CASE)).mean(),
              "oss_bb": oss_bb_paths(u, *oss_params(CASE), bridge_plan(12),
                                     oss_bb_dims(4, 12)).mean()}
    for method, value in direct.items():
        timed = timed_scramble(("t", CASE, method, KEY, 2 ** 12))
        assert np.isclose(timed["prefix"][2 ** 12], value, rtol=1e-12, atol=0)
        assert np.isclose(timed_chunk(("t", CASE, method, KEY, 0))["total"] / 2 ** 12, value,
                          rtol=1e-12, atol=0)
