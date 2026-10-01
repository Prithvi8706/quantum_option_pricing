"""sigma_Q for every case (ANALYSIS_SPEC_STAGE_C.md, section 0.4).

ddof = 1 sample sd of the discounted plain knock-out payoff over 2^20 iid exact-date paths
in the canonical factor; normals from SeedSequence([2026100107, case_index, 7, 0, 0]).
Bootstrap 95% interval (B = 1000, index from [2026100112, case_index, 7, 0, 0]); the
preintegrated sd from the same draws is a sensitivity.
"""

import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import math

import numpy as np

from research.frontier_classical_20261001.basis import canonical_factor
from research.frontier_classical_20261001.kernels import knockout_plain, knockout_preint

SIGMA_ROOT = 2026100107
BOOT_ROOT = 2026100112
PATHS = 2 ** 20
ROWS = 2 ** 14
BOOT = 1000


def sigma_q(case):
    L, _ = canonical_factor(case.na, case.nt, case.sigma, case.rho, case.maturity)
    mu = sc.drift(case)
    disc = math.exp(-case.rate * case.maturity)
    rng = np.random.default_rng([SIGMA_ROOT, case.case_index, 7, 0, 0])
    plain, pre = np.empty(PATHS), np.empty(PATHS)
    for start in range(0, PATHS, ROWS):
        z = rng.standard_normal((ROWS, case.dim))
        x = z @ L.T + mu
        plain[start:start + ROWS] = knockout_plain(x, case.na, case.nt, disc, case.strike,
                                                   case.barrier)
        pre[start:start + ROWS] = knockout_preint(x, np.ascontiguousarray(z[:, 0]),
                                                  np.ascontiguousarray(L[:, 0]), case.na,
                                                  case.nt, disc, case.strike, case.barrier)
    boot_rng = np.random.default_rng([BOOT_ROOT, case.case_index, 7, 0, 0])
    boot = np.empty(BOOT)
    for b in range(BOOT):
        boot[b] = plain[boot_rng.integers(0, PATHS, PATHS)].std(ddof=1)
    return dict(sigma_q=float(plain.std(ddof=1)),
                sigma_q_ci95=[float(x) for x in np.percentile(boot, [2.5, 97.5])],
                sigma_preint=float(pre.std(ddof=1)), mean_plain=float(plain.mean()),
                mean_preint=float(pre.mean()), paths=PATHS)
