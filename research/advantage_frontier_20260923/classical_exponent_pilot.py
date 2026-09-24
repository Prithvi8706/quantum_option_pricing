"""Pilot P1: classical whole-algorithm error-vs-work exponents and implied quantum budgets.

Development diagnostic only (not a confirmation study, not a certified price).
Exact-date correlated GBM, so neither side pays SDE bias. Workloads:
  call    arithmetic Asian-basket call                  (kink)
  digital 100 * 1{arithmetic basket average > K}        (jump)
  barrier arithmetic call knocked out if any date's basket value >= H (path jump)
Methods (all scrambled Sobol + PCA of the full asset/date covariance):
  rqmc       plain randomized QMC
  rqmc_cv    RQMC with analytic geometric control (call/digital only)
  preint     RQMC after analytic integration along the first principal direction
             (all asset/date loadings are positive, so every payoff is monotone or
              interval-supported in that coordinate; the 1-D integral is closed form)
  mc_cv      iid Monte Carlo with the same geometric control (reference point)
Quantum budget: a variance-sensitive estimator needs Q = k * sigma_q / eps_stat calls.
sigma_q is the smallest per-sample std among the estimands (favours quantum) and
smoothing is granted to the quantum oracle at zero extra cost (favours quantum).
"""

import json
import math
import os
import platform
import sys
import time

for _k in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ.setdefault(_k, "1")

import numpy as np  # noqa: E402
from scipy.special import ndtr, ndtri  # noqa: E402
from scipy.stats import qmc  # noqa: E402

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "results",
                       "advantage_frontier_20260923")
OUT = os.path.join(RESULTS, "classical_exponent_pilot.json")
ROOT_SEED = 2026092231          # development root; not a confirmation stream
SCRAMBLES = 32
M_MAX = 15                       # prefixes 2^6 ... 2^15 points per scramble
CHUNK = 2 ** 12
EPS = (0.10, 0.03, 0.01)
STAT_SHARE = 0.45                # statistical share of the price error (project allocation)
K_CONST = (1, 3, 10)
T_LAYER = (1e-8, 1e-7, 1e-6, 1e-5)


class Case:
    def __init__(self, name, assets, dates, sigma=.3, corr=.4, strike=100., barrier=140.,
                 spot=100., rate=.03, maturity=1.):
        self.name, self.na, self.nt = name, assets, dates
        self.sigma, self.corr, self.K, self.H = sigma, corr, strike, barrier
        self.S0, self.r, self.T = spot, rate, maturity
        t = maturity * np.arange(1, dates + 1) / dates
        asset_cov = sigma**2 * (corr * np.ones((assets, assets)) + (1 - corr) * np.eye(assets))
        cov = np.kron(asset_cov, np.minimum.outer(t, t))          # index c = asset*nt + date
        vals, vecs = np.linalg.eigh(cov)
        order = np.argsort(vals)[::-1]
        vals, vecs = vals[order], vecs[:, order]
        if vecs[:, 0].sum() < 0:
            vecs[:, 0] *= -1
        assert vecs[:, 0].min() > 0, "first principal loadings must be positive"
        self.L = vecs * np.sqrt(np.clip(vals, 0, None))
        self.v = self.L[:, 0]                                        # first-direction loadings
        self.mu = np.log(spot) + np.tile((rate - sigma**2 / 2) * t, assets)
        self.w = np.full(assets * dates, 1.0 / (assets * dates))
        self.disc = math.exp(-rate * maturity)
        self.dim = assets * dates
        # geometric average of all coordinates is lognormal: mean m_g, variance s2_g
        self.m_g = float(self.w @ self.mu)
        self.s2_g = float(self.w @ cov @ self.w)

    def geo_call_mean(self):
        m, s = self.m_g, math.sqrt(self.s2_g)
        d1 = (m - math.log(self.K) + s * s) / s
        return self.disc * (math.exp(m + s * s / 2) * ndtr(d1) - self.K * ndtr(d1 - s))

    def geo_digital_mean(self):
        m, s = self.m_g, math.sqrt(self.s2_g)
        return self.disc * 100.0 * ndtr((m - math.log(self.K)) / s)


def newton_root(a, v, w, target, iters=8):
    """Root z of sum_c w_c exp(a_c + v_c z) = target, rows independent.

    Start at the geometric-mean root, which lies right of the true root (AM >= GM);
    Newton on the convex increasing log-sum-exp then converges monotonically."""
    z = (math.log(target) - a @ w) / (v @ w)
    for _ in range(iters):
        terms = w * np.exp(a + np.outer(z, v))
        s = terms.sum(1)
        ds = terms @ v
        z = z - (np.log(s) - math.log(target)) * s / ds
    return z


def evaluate(case, z, pre=True):
    """Per-point estimands for every method, shape (n,); pre=False skips preintegration."""
    x = z @ case.L.T                                   # (n, dim) log-price deviations
    logS = case.mu + x
    S = np.exp(logS)
    A = S @ case.w
    basket_by_date = S.reshape(-1, case.na, case.nt).mean(1)
    alive = basket_by_date.max(1) < case.H
    G = np.exp(logS @ case.w)
    out = {
        "call": case.disc * np.maximum(A - case.K, 0.0),
        "digital": case.disc * 100.0 * (A > case.K),
        "barrier": case.disc * np.maximum(A - case.K, 0.0) * alive,
        "geo_call": case.disc * np.maximum(G - case.K, 0.0),
        "geo_digital": case.disc * 100.0 * (G > case.K),
    }
    if not pre:
        return out
    # preintegration along direction 0: a_c = mu_c + (L[:,1:] z_rest)_c
    a = logS - np.outer(z[:, 0], case.v)
    v = case.v
    zs = newton_root(a, v, case.w, case.K)
    growth = np.exp(a + v * v / 2)                     # E-weighting of each coordinate
    call_pre = (case.w * growth * ndtr(v - zs[:, None])).sum(1) - case.K * ndtr(-zs)
    out["call_pre"] = case.disc * call_pre
    out["digital_pre"] = case.disc * 100.0 * ndtr(-zs)
    # barrier: knock-out region z >= z_H with z_H = min over dates of each date's root
    na, nt = case.na, case.nt
    a3 = a.reshape(-1, na, nt)
    v3 = v.reshape(na, nt)
    zh = np.full(z.shape[0], np.inf)
    for j in range(nt):
        zh = np.minimum(zh, newton_root(a3[:, :, j], v3[:, j], np.full(na, 1.0 / na), case.H))
    lo, hi = zs, np.maximum(zh, zs)
    part = (case.w * growth * (ndtr(hi[:, None] - v) - ndtr(lo[:, None] - v))).sum(1)
    out["barrier_pre"] = case.disc * (part - case.K * (ndtr(hi) - ndtr(lo)))
    return out


def normals(sampler, n):
    u = sampler.random(n)
    return ndtri(np.clip(u, 1e-15, 1 - 1e-15))


def prefix_means(case, seed):
    """One scrambled Sobol sequence; means of every estimand on prefixes 2^m."""
    sampler = qmc.Sobol(case.dim, scramble=True, seed=np.random.default_rng(seed))
    sums, count, res = {}, 0, {}
    total = 2 ** M_MAX
    while count < total:
        vals = evaluate(case, normals(sampler, CHUNK))
        csum = {k: np.cumsum(v) for k, v in vals.items()}
        for m in range(6, M_MAX + 1):
            n = 2 ** m
            if count < n <= count + CHUNK:
                for k in vals:
                    res.setdefault(k, {})[m] = (sums.get(k, 0.0) + csum[k][n - count - 1]) / n
        for k in vals:
            sums[k] = sums.get(k, 0.0) + csum[k][-1]
        count += CHUNK
    return res


def timing(case, pre, n=2 ** 13, reps=3):
    """Best-of-reps seconds per point: Sobol generation + normal transform + payoffs.

    pre=False times the base pass (paths, all plain payoffs, geometric controls);
    pre=True adds the preintegration root solves. Every plain payoff is computed in
    the base pass, so charging it to one method is conservative against classical."""
    best = math.inf
    for rep in range(reps):
        rng = np.random.default_rng([ROOT_SEED, 999, rep])
        sampler = qmc.Sobol(case.dim, scramble=True, seed=rng)
        t0 = time.perf_counter()
        evaluate(case, normals(sampler, n), pre=pre)
        best = min(best, time.perf_counter() - t0)
    return best / n


def fit_rate(ns, errs, m_min=8):
    sel = [i for i, n in enumerate(ns) if n >= 2 ** m_min]
    slope, icpt = np.polyfit(np.log(np.array(ns)[sel]), np.log(np.array(errs)[sel]), 1)
    return -slope, math.exp(icpt)


def run_case(case):
    t0 = time.perf_counter()
    per = [prefix_means(case, [ROOT_SEED, case.dim, s]) for s in range(SCRAMBLES)]
    acq = time.perf_counter() - t0
    ms = list(range(6, M_MAX + 1))
    ns = [2 ** m for m in ms]
    def arr(k):                                                   # (scrambles, m)
        return np.array([[p[k][m] for m in ms] for p in per])
    geo_c, geo_d = case.geo_call_mean(), case.geo_digital_mean()
    est = {
        ("call", "rqmc"): arr("call"),
        ("call", "rqmc_cv"): arr("call") - arr("geo_call") + geo_c,
        ("call", "preint"): arr("call_pre"),
        ("digital", "rqmc"): arr("digital"),
        ("digital", "rqmc_cv"): arr("digital") - arr("geo_digital") + geo_d,
        ("digital", "preint"): arr("digital_pre"),
        ("barrier", "rqmc"): arr("barrier"),
        ("barrier", "preint"): arr("barrier_pre"),
    }
    # pointwise (iid) std of each estimand from one large iid batch
    rng = np.random.default_rng([ROOT_SEED, 7, case.dim])
    iid = evaluate(case, rng.standard_normal((2 ** 14, case.dim)))
    pw = {
        "call": iid["call"].std(), "call_cv": (iid["call"] - iid["geo_call"]).std(),
        "call_pre": iid["call_pre"].std(), "digital": iid["digital"].std(),
        "digital_cv": (iid["digital"] - iid["geo_digital"]).std(),
        "digital_pre": iid["digital_pre"].std(), "barrier": iid["barrier"].std(),
        "barrier_pre": iid["barrier_pre"].std(),
    }
    sec_base, sec_pre = timing(case, False), timing(case, True)
    result = {"case": vars_case(case), "acquisition_seconds": acq,
              "seconds_per_point_base": sec_base, "seconds_per_point_with_preint": sec_pre,
              "pointwise_std": pw, "methods": {}}
    for (payoff, method), e in est.items():
        sd = e.std(0, ddof=1)                          # RQMC error of ONE scramble mean at n
        rate, const = fit_rate(ns, sd)
        result["methods"][f"{payoff}/{method}"] = {
            "price_estimate": float(e[:, -1].mean()),
            "price_std_error": float(e[:, -1].std(ddof=1) / math.sqrt(SCRAMBLES)),
            "n": ns, "rqmc_std_one_scramble": sd.tolist(),
            "rate_r": rate, "p_C": 1.0 / rate, "fit_constant": const,
        }
    return result


def vars_case(c):
    return {"name": c.name, "assets": c.na, "dates": c.nt, "sigma": c.sigma, "corr": c.corr,
            "strike": c.K, "barrier": c.H, "rate": c.r, "maturity": c.T, "dim": c.dim}


def budgets(res):
    """Classical time to eps (16 scrambles, t quantile) and quantum per-call budget."""
    t995 = 2.947                                        # Student t, 15 dof, two-sided 99%
    pw = res["pointwise_std"]
    rows = []
    methods = dict(res["methods"])
    # iid MC reference: n = (z99 * sigma / e_stat)^2 points, same base pass cost
    for payoff, key in (("call", "call_cv"), ("digital", "digital_cv"), ("barrier", "barrier")):
        methods[f"{payoff}/mc_cv"] = {"iid_sigma": float(pw[key])}
    for key, m in methods.items():
        payoff, method = key.split("/")
        pre = method == "preint"
        sec_pt = res["seconds_per_point_with_preint" if pre else "seconds_per_point_base"]
        for eps in EPS:
            e_stat = STAT_SHARE * eps
            # need t995 * sd(n) / sqrt(16) <= e_stat with sd(n) = const * n^-r
            if method == "mc_cv":
                n_need = math.ceil((2.576 * m["iid_sigma"] / e_stat) ** 2)
                t_c = n_need * sec_pt
            else:
                target_sd = e_stat * 4 / t995
                n_need = (m["fit_constant"] / target_sd) ** (1 / m["rate_r"])
                n_need = max(2 ** 6, 2 ** math.ceil(math.log2(n_need)))
                t_c = 16 * n_need * sec_pt
            # smallest pointwise std among estimands for this payoff (favours quantum)
            sig_q = min(v for k, v in res["pointwise_std"].items() if k.startswith(payoff))
            for k in K_CONST:
                q_calls = k * sig_q / e_stat
                c_q = t_c / (10 * q_calls)
                rows.append({"method": key, "eps": eps, "points_per_scramble": n_need,
                             "classical_seconds": t_c, "sigma_q": sig_q, "k": k,
                             "quantum_calls": q_calls, "max_seconds_per_call": c_q,
                             "max_T_depth_per_call": {f"{tl:g}": c_q / tl for tl in T_LAYER}})
    return rows


def main():
    cases = [Case("B4x12", 4, 12), Case("B8x52", 8, 52)]
    out = {"purpose": __doc__, "root_seed": ROOT_SEED, "scrambles": SCRAMBLES,
           "python": sys.version, "numpy": np.__version__, "platform": platform.platform(),
           "single_thread_blas": True, "results": []}
    for c in cases:
        r = run_case(c)
        r["budgets"] = budgets(r)
        out["results"].append(r)
        print(c.name, "acq %.1fs" % r["acquisition_seconds"], "sec/pt base %.2e pre %.2e"
              % (r["seconds_per_point_base"], r["seconds_per_point_with_preint"]))
        for k, m in r["methods"].items():
            print("  %-18s price %.5f +- %.5f  rate r=%.3f  p_C=%.2f"
                  % (k, m["price_estimate"], m["price_std_error"], m["rate_r"], m["p_C"]))
        print("  pointwise std:", {k: round(float(v), 4) for k, v in r["pointwise_std"].items()})
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
