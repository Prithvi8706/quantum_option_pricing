import math

import numpy as np

from research.frontier_classical_20261001.c3_refb import plain_paths


def test_plain_paths_price_agrees_with_p3_preint():
    na, nt, sigma, rho, r, T = 4, 12, 0.3, 0.4, 0.03, 1.0
    dt = T / nt
    z = np.random.default_rng(5).standard_normal((2 ** 19, nt * (na + 1)))
    y = plain_paths(z, na, nt, math.log(100.0), (r - sigma**2 / 2) * dt,
                    sigma * math.sqrt(rho * dt), sigma * math.sqrt((1 - rho) * dt),
                    math.exp(-r * T), 100.0, 140.0)
    p3_price = 3.5188852273893136                    # archived P3, SE 9.0e-5
    assert abs(y.mean() - p3_price) < 4 * y.std() / math.sqrt(len(y))
    assert abs(y.std() - 5.73) < 0.1                # P1 plain sigma 5.726 (ddof 0, 2^14 paths)
