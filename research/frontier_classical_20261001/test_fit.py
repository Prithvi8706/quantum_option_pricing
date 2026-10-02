import numpy as np

from research.frontier_classical_20261001.fit import (T995_15, c2_label, n_eps, ols_rate,
                                                      summarize)


def synthetic(r=0.6, A=0.8, scrambles=32, seed=1):
    ms = list(range(6, 20))
    rng = np.random.default_rng(seed)
    sd = A * (2.0 ** np.array(ms)) ** -r
    return ms, 3.5 + rng.standard_normal((scrambles, len(ms))) * sd


def test_ols_recovers_rate_and_constant():
    ms = list(range(6, 20))
    sd = 0.8 * (2.0 ** np.array(ms)) ** -0.6
    A, r = ols_rate(ms, sd, (10, 19))
    assert abs(r - 0.6) < 1e-12 and abs(A - 0.8) < 1e-10


def test_n_eps_inverts_the_half_width():
    n = n_eps(0.8, 0.6, 0.001)
    assert abs(T995_15 * 0.8 * n ** -0.6 / 4 - 0.45 * 0.001) < 1e-15


def test_c2_labels():
    assert c2_label(0.91, 1.0) == "restores"
    assert c2_label(0.5, 0.89) == "does_not_restore"
    assert c2_label(0.85, 0.95) == "inconclusive"


def test_summary_interval_covers_true_rate_and_is_paired():
    ms, prefix = synthetic()
    s = summarize(ms, prefix, case_index=0, reference_prefix=prefix)
    assert s["r_ci95"][0] < 0.6 < s["r_ci95"][1]
    assert s["r_minus_canonical_ci95"] == [0.0, 0.0]
    assert s["n_eps"]["0.001"]["flag"] in {"in-range", "extrapolated-high"}
