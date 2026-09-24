"""Pilot P3: compiled multicore version of the strongest classical knock-out method (P1).

Same contract and estimator as P1 `barrier/preint` (first-principal-direction analytic
preintegration of the discretely monitored basket knock-out call), but:
  * numba-compiled per-point kernel (Newton roots, closed-form 1-D integral);
  * single-thread BLAS gemm for the PCA map, in chunks;
  * one randomized-QMC scramble per worker process, 16 worker processes.
Measures the RQMC rate up to 2^17 points per scramble and the complete wall time per
scramble, so the classical time-to-accuracy used in the quantum budget is measured,
not assumed. Requires numba (run with an interpreter that has numba, e.g. anaconda).
Development diagnostic only.
"""

import os

for _k in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_k] = "1"

import json  # noqa: E402
import math  # noqa: E402
import multiprocessing as mp  # noqa: E402
import platform  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

import numba  # noqa: E402
import numpy as np  # noqa: E402
from scipy.special import ndtri  # noqa: E402
from scipy.stats import qmc  # noqa: E402

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "results",
                       "advantage_frontier_20260923")
OUT = os.path.join(RESULTS, "barrier_fast_classical.json")
ROOT_SEED = 2026092333
SCRAMBLES = 32
WORKERS = 16
M_MIN, M_MAX = 8, 17
CHUNK = 2 ** 12
SIGMA, CORR, S0, RATE, T, K, H = .3, .4, 100., .03, 1., 100., 140.


def setup(na, nt):
    """PCA factor of the flattened asset/date log-price covariance (as in P1)."""
    t = T * np.arange(1, nt + 1) / nt
    asset_cov = SIGMA**2 * (CORR * np.ones((na, na)) + (1 - CORR) * np.eye(na))
    cov = np.kron(asset_cov, np.minimum.outer(t, t))
    vals, vecs = np.linalg.eigh(cov)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    if vecs[:, 0].sum() < 0:
        vecs[:, 0] *= -1
    assert vecs[:, 0].min() > 0
    L = np.ascontiguousarray(vecs * np.sqrt(np.clip(vals, 0, None)))
    mu = np.log(S0) + np.tile((RATE - SIGMA**2 / 2) * t, na)
    return L, mu


@numba.njit(cache=True, fastmath=False)
def _ndtr(x):
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


@numba.njit(cache=True)
def _root(a, v, w, target, idx):
    """Newton root of sum_i w_i exp(a[idx_i] + v[idx_i] z) = target (P1 algorithm)."""
    num = 0.0
    den = 0.0
    for i in idx:
        num += a[i] * w
        den += v[i] * w
    z = (math.log(target) - num) / den
    for _ in range(8):
        s = 0.0
        ds = 0.0
        for i in idx:
            term = w * math.exp(a[i] + v[i] * z)
            s += term
            ds += term * v[i]
        step = (math.log(s) - math.log(target)) * s / ds
        z = z - step
        if abs(step) < 1e-13 * (1.0 + abs(z)):
            break
    return z


@numba.njit(cache=True)
def estimand(x, z0, v, na, nt, disc):
    """x: (n, dim) log prices; z0: first normal. Returns preintegrated payoff per point."""
    n, dim = x.shape
    out = np.empty(n)
    a = np.empty(dim)
    all_idx = np.arange(dim)
    w_all = 1.0 / dim
    date_idx = np.empty((nt, na), dtype=np.int64)
    for j in range(nt):
        for i in range(na):
            date_idx[j, i] = i * nt + j
    for p in range(n):
        for c in range(dim):
            a[c] = x[p, c] - z0[p] * v[c]
        zs = _root(a, v, w_all, K, all_idx)
        zh = math.inf
        for j in range(nt):
            r = _root(a, v, 1.0 / na, H, date_idx[j])
            if r < zh:
                zh = r
        lo = zs
        hi = zh if zh > zs else zs
        part = 0.0
        for c in range(dim):
            g = math.exp(a[c] + v[c] * v[c] / 2)
            part += w_all * g * (_ndtr(hi - v[c]) - _ndtr(lo - v[c]))
        out[p] = disc * (part - K * (_ndtr(hi) - _ndtr(lo)))
    return out


def scramble_run(args):
    na, nt, s = args
    t0 = time.perf_counter()
    L, mu = setup(na, nt)
    dim = na * nt
    v = np.ascontiguousarray(L[:, 0])
    disc = math.exp(-RATE * T)
    sampler = qmc.Sobol(dim, scramble=True, seed=np.random.default_rng([ROOT_SEED, dim, s]))
    t_setup = time.perf_counter() - t0
    total, count, prefix = 0.0, 0, {}
    marks = []
    while count < 2 ** M_MAX:
        u = sampler.random(CHUNK)
        z = ndtri(np.clip(u, 1e-15, 1 - 1e-15))
        x = z @ L.T + mu
        y = estimand(x, np.ascontiguousarray(z[:, 0]), v, na, nt, disc)
        cs = np.cumsum(y)
        for m in range(M_MIN, M_MAX + 1):
            n = 2 ** m
            if count < n <= count + CHUNK:
                prefix[m] = (total + cs[n - count - 1]) / n
                marks.append((m, time.perf_counter() - t0))
        total += cs[-1]
        count += CHUNK
    return dict(scramble=s, prefix=prefix, setup_seconds=t_setup,
                elapsed_at_prefix={m: e for m, e in marks}, seconds=time.perf_counter() - t0)


def run(na, nt, pool):
    t0 = time.perf_counter()
    rows = pool.map(scramble_run, [(na, nt, s) for s in range(SCRAMBLES)])
    wall = time.perf_counter() - t0
    ms = list(range(M_MIN, M_MAX + 1))
    ns = [2 ** m for m in ms]
    e = np.array([[r["prefix"][m] for m in ms] for r in rows])
    sd = e.std(0, ddof=1)
    sel = [i for i, n in enumerate(ns) if n >= 2 ** 9]
    slope, icpt = np.polyfit(np.log(np.array(ns)[sel]), np.log(sd[sel]), 1)
    # per-scramble elapsed time to reach 2^m points (includes setup and compile-cache load)
    tm = {m: float(np.median([r["elapsed_at_prefix"][m] for r in rows])) for m in ms}
    return dict(assets=na, dates=nt, dim=na * nt, scrambles=SCRAMBLES, workers=WORKERS,
                wall_seconds_all_scrambles=wall, price=float(e[:, -1].mean()),
                std_error=float(e[:, -1].std(ddof=1) / math.sqrt(SCRAMBLES)),
                n=ns, rqmc_std_one_scramble=sd.tolist(), rate_r=-slope, fit_constant=math.exp(icpt),
                median_scramble_seconds_to_prefix=tm,
                median_setup_seconds=float(np.median([r["setup_seconds"] for r in rows])))


def main():
    L, mu = setup(4, 12)                       # compile once in the parent (cache=True)
    estimand(np.tile(mu, (2, 1)), np.zeros(2), np.ascontiguousarray(L[:, 0]), 4, 12, 1.0)
    out = dict(purpose=__doc__, root_seed=ROOT_SEED, python=sys.version, numba=numba.__version__,
               numpy=np.__version__, platform=platform.platform(), processor=platform.processor(),
               cpu_count=os.cpu_count(), results=[])
    with mp.Pool(WORKERS) as pool:
        for na, nt in ((4, 12), (8, 52)):
            r = run(na, nt, pool)
            out["results"].append(r)
            print(f"B{na}x{nt} wall {r['wall_seconds_all_scrambles']:.1f}s price {r['price']:.5f}"
                  f" +- {r['std_error']:.5f} rate r={r['rate_r']:.3f}"
                  f" scramble time to 2^{M_MAX}:"
                  f" {r['median_scramble_seconds_to_prefix'][M_MAX]:.1f}s")
            sys.stdout.flush()
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
