"""One-step-survival (OSS) estimator for item C3 Ref A and item C5 (ANALYSIS_SPEC_STAGE_C.md).

P2's basket OSS (research/advantage_frontier_20260923/barrier_oss_pilot.py) compiled with
numba: at each date the asset increments are driven by asset-PCA normals; survival is
equivalent to the first asset-PC normal lying below a root, so the indicator is replaced
by its conditional probability p_j = Phi(root) and that normal is drawn from the
survival-truncated law by inverse transform of the same uniform. Estimator =
discounted payoff x prod_j p_j. The inverse normal is Wichura's AS241 (PPND16).
"""

import math

import numba
import numpy as np

from research.frontier_classical_20261001.basis import asset_basis


@numba.njit(cache=True)
def ndtri(p):
    """Wichura (1988) AS241 PPND16 inverse standard normal, about 1e-16 relative accuracy."""
    q = p - 0.5
    if abs(q) <= 0.425:
        r = 0.180625 - q * q
        return q * (((((((2509.0809287301226727 * r + 33430.575583588128105) * r
                          + 67265.770927008700853) * r + 45921.953931549871457) * r
                        + 13731.693765509461125) * r + 1971.5909503065514427) * r
                      + 133.14166789178437745) * r + 3.387132872796366608) / \
            (((((((5226.495278852545925 * r + 28729.085735721942674) * r
                  + 39307.89580009271061) * r + 21213.794301586595867) * r
                + 5394.1960214247511077) * r + 687.1870074920579083) * r
              + 42.313330701600911252) * r + 1.0)
    r = p if q < 0 else 1.0 - p
    r = math.sqrt(-math.log(r))
    if r <= 5.0:
        r -= 1.6
        val = (((((((7.7454501427834140764e-4 * r + 0.0227238449892691845833) * r
                    + 0.24178072517745061177) * r + 1.27045825245236838258) * r
                  + 3.64784832476320460504) * r + 5.7694972214606914055) * r
                + 4.6303378461565452959) * r + 1.42343711074968357734) / \
            (((((((1.05075007164441684324e-9 * r + 5.475938084995344946e-4) * r
                  + 0.0151986665636164571966) * r + 0.14810397642748007459) * r
                + 0.68976733498510000455) * r + 1.6763848301838038494) * r
              + 2.05319162663775882187) * r + 1.0)
    else:
        r -= 5.0
        val = (((((((2.01033439929228813265e-7 * r + 2.71155556874348757815e-5) * r
                    + 0.0012426609473880784386) * r + 0.026532189526576123093) * r
                  + 0.29656057182850489123) * r + 1.7848265399172913358) * r
                + 5.4637849111641143699) * r + 6.6579046435011037772) / \
            (((((((2.04426310338993978564e-15 * r + 1.4215117583164458887e-7) * r
                  + 1.8463183175100546818e-5) * r + 7.868691311456132591e-4) * r
                + 0.0148753612908506148525) * r + 0.13692988092273580531) * r
              + 0.59983220655588793769) * r + 1.0)
    return -val if q < 0 else val


@numba.njit(cache=True)
def _ndtr(x):
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


@numba.njit(cache=True)
def _basket_root(a, v, na, target):
    """Newton root z of (1/na) sum_i exp(a_i + v_i z) = target (all v_i > 0)."""
    num = 0.0
    den = 0.0
    for i in range(na):
        num += a[i] / na
        den += v[i] / na
    z = (math.log(target) - num) / den
    for _ in range(50):
        s = 0.0
        ds = 0.0
        for i in range(na):
            term = math.exp(a[i] + v[i] * z) / na
            s += term
            ds += term * v[i]
        step = (math.log(s) - math.log(target)) * s / ds
        z -= step
        if abs(step) < 1e-13 * (1.0 + abs(z)):
            break
    return z


@numba.njit(cache=True)
def oss_paths(u, na, nt, B, vol, drift, log_s0, disc, strike, barrier):
    """u: (n, nt*na) uniforms, date-major (date j uses u[:, j*na:(j+1)*na], first entry is
    the truncated first asset-PC coordinate). Returns the OSS estimator per point."""
    n = u.shape[0]
    out = np.empty(n)
    logs = np.empty(na)
    a = np.empty(na)
    z = np.empty(na)
    v = np.empty(na)
    for i in range(na):
        v[i] = vol * B[i, 0]
    for p in range(n):
        for i in range(na):
            logs[i] = log_s0
        weight = 1.0
        total = 0.0
        for j in range(nt):
            for k in range(1, na):
                uk = min(max(u[p, j * na + k], 1e-15), 1.0 - 1e-15)
                z[k] = ndtri(uk)
            for i in range(na):
                s = 0.0
                for k in range(1, na):
                    s += B[i, k] * z[k]
                a[i] = logs[i] + drift + vol * s
            root = _basket_root(a, v, na, barrier)
            prob = _ndtr(root)
            u0 = min(max(u[p, j * na] * prob, 1e-300), 1.0 - 1e-16)
            z1 = ndtri(u0)
            weight *= prob
            for i in range(na):
                logs[i] = a[i] + z1 * v[i]
                total += math.exp(logs[i])
        out[p] = disc * max(total / (na * nt) - strike, 0.0) * weight
    return out


def asset_factor(case):
    """Canonical asset factor of the correlation matrix (unit variance), as in P2."""
    vecs, vals = asset_basis(case.na, 1.0, case.rho)
    return np.ascontiguousarray(vecs * np.sqrt(vals))


def oss_params(case):
    dt = case.maturity / case.nt
    return (case.na, case.nt, asset_factor(case), case.sigma * math.sqrt(dt),
            (case.rate - case.sigma**2 / 2) * dt, math.log(case.spot),
            math.exp(-case.rate * case.maturity), case.strike, case.barrier)
