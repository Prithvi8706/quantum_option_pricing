"""Pilot P2: can one-step-survival (OSS) conditioning restore the RQMC rate for the
discretely monitored arithmetic-basket knock-out call that defeated first-direction
preintegration in pilot P1?  Development diagnostic only; same contract as P1.

Contract: equal-weight basket of na GBM assets (sigma .3, equicorrelation .4, S0 100,
r .03, T 1), nt monitoring dates; knocked out if the basket value at any date >= H=140;
payoff exp(-rT) * (arithmetic average over all asset/date prices - K)+ with K=100.

OSS estimator (Glasserman-Staum 2001, adapted to a basket): at each date the asset
increments are driven by asset-PCA normals; the basket value is increasing in the first
asset principal normal, so survival <=> that normal < root. Replace the indicator by its
conditional probability p_j = Phi(root) and draw the normal from the survival-truncated
law by inverse transform of the same uniform. Estimator = payoff * prod_j p_j (unbiased).
"""

import json
import math
import os
import sys
import time

for _k in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ.setdefault(_k, "1")

import numpy as np  # noqa: E402
from scipy.special import ndtr, ndtri  # noqa: E402
from scipy.stats import qmc  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classical_exponent_pilot import newton_root, fit_rate  # noqa: E402

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "results",
                       "advantage_frontier_20260923")
OUT = os.path.join(RESULTS, "barrier_oss_pilot.json")
ROOT_SEED = 2026092232
SCRAMBLES = 32
M_MAX = 15
CHUNK = 2 ** 12
SIGMA, CORR, S0, RATE, T, K, H = .3, .4, 100., .03, 1., 100., 140.


def asset_pca(na):
    c = CORR * np.ones((na, na)) + (1 - CORR) * np.eye(na)
    vals, vecs = np.linalg.eigh(c)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    if vecs[:, 0].sum() < 0:
        vecs[:, 0] *= -1
    assert vecs[:, 0].min() > 0
    return vecs * np.sqrt(vals)


def oss_estimate(u, na, nt, B):
    """u: (n, nt*na) uniforms, date-major. Returns (oss estimator, plain estimator) per point."""
    n = u.shape[0]
    dt = T / nt
    drift = (RATE - SIGMA**2 / 2) * dt
    vol = SIGMA * math.sqrt(dt)
    logS = np.full((n, na), math.log(S0))
    logS_plain = logS.copy()
    weight = np.ones(n)
    total = np.zeros(n)
    total_plain = np.zeros(n)
    alive_plain = np.ones(n, dtype=bool)
    v = vol * B[:, 0]
    wts = np.full(na, 1.0 / na)
    for j in range(nt):
        uj = np.clip(u[:, j * na:(j + 1) * na], 1e-15, 1 - 1e-15)
        z = ndtri(uj)
        # plain path (same uniforms) for reference
        logS_plain = logS_plain + drift + vol * (z @ B.T)
        Sp = np.exp(logS_plain)
        alive_plain &= Sp.mean(1) < H
        total_plain += Sp.sum(1)
        # OSS: rest of the increment from normals 2..na, first normal truncated to survival
        a = logS + drift + vol * (z[:, 1:] @ B[:, 1:].T)
        root = newton_root(a, v, wts, H)
        p = ndtr(root)
        z1 = ndtri(np.clip(uj[:, 0] * p, 1e-300, 1.0))
        logS = a + np.outer(z1, v)
        weight *= p
        total += np.exp(logS).sum(1)
    disc = math.exp(-RATE * T)
    avg = total / (na * nt)
    avg_plain = total_plain / (na * nt)
    oss = disc * np.maximum(avg - K, 0.0) * weight
    plain = disc * np.maximum(avg_plain - K, 0.0) * alive_plain
    return oss, plain


def run(na, nt):
    B = asset_pca(na)
    dim = na * nt
    ms = list(range(6, M_MAX + 1))
    per = {"oss": [], "plain_time_ordered": []}
    t0 = time.perf_counter()
    for s in range(SCRAMBLES):
        sampler = qmc.Sobol(dim, scramble=True, seed=np.random.default_rng([ROOT_SEED, dim, s]))
        sums = {"oss": 0.0, "plain_time_ordered": 0.0}
        res = {"oss": {}, "plain_time_ordered": {}}
        count = 0
        while count < 2 ** M_MAX:
            o, p = oss_estimate(sampler.random(CHUNK), na, nt, B)
            cs = {"oss": np.cumsum(o), "plain_time_ordered": np.cumsum(p)}
            for m in ms:
                n = 2 ** m
                if count < n <= count + CHUNK:
                    for k in cs:
                        res[k][m] = (sums[k] + cs[k][n - count - 1]) / n
            for k in cs:
                sums[k] += cs[k][-1]
            count += CHUNK
        for k in per:
            per[k].append([res[k][m] for m in ms])
    acq = time.perf_counter() - t0
    ns = [2 ** m for m in ms]
    rng = np.random.default_rng([ROOT_SEED, 7, dim])
    o, p = oss_estimate(rng.random((2 ** 14, dim)), na, nt, B)
    sampler = qmc.Sobol(dim, scramble=True, seed=np.random.default_rng([ROOT_SEED, 999]))
    t1 = time.perf_counter()
    oss_estimate(sampler.random(2 ** 13), na, nt, B)
    sec_pt = (time.perf_counter() - t1) / 2 ** 13
    out = {"assets": na, "dates": nt, "dim": dim, "acquisition_seconds": acq,
           "seconds_per_point_oss_plus_plain": sec_pt,
           "pointwise_std": {"oss": float(o.std()), "plain": float(p.std())}, "methods": {}}
    for k, rows in per.items():
        e = np.array(rows)
        sd = e.std(0, ddof=1)
        rate, const = fit_rate(ns, sd)
        out["methods"][k] = {"price": float(e[:, -1].mean()),
                             "std_error": float(e[:, -1].std(ddof=1) / math.sqrt(SCRAMBLES)),
                             "n": ns, "rqmc_std_one_scramble": sd.tolist(),
                             "rate_r": rate, "p_C": 1 / rate, "fit_constant": const}
    return out


def main():
    results = []
    for na, nt in ((4, 12), (8, 52)):
        r = run(na, nt)
        results.append(r)
        print(f"B{na}x{nt} acq {r['acquisition_seconds']:.1f}s"
              f" sec/pt {r['seconds_per_point_oss_plus_plain']:.2e}"
              f" pointwise std {r['pointwise_std']}")
        for k, m in r["methods"].items():
            print(f"  {k:20s} price {m['price']:.5f} +- {m['std_error']:.5f}"
                  f"  rate r={m['rate_r']:.3f}  p_C={m['p_C']:.2f}")
    with open(OUT, "w") as f:
        json.dump({"purpose": __doc__, "root_seed": ROOT_SEED, "scrambles": SCRAMBLES,
                   "numpy": np.__version__, "results": results}, f, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
