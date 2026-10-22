"""C10 challenger: preintegration + closed-form control variates (preint_cv). RQMC rate study, item-C1 style.

Estimand per point: r = h - beta . (g_hat - E g), with h the Stage C preint value and g_hat the preintegrated
geometric Asian call, linear average and geometric-average knock-out (closed-form means from the canonical factor).
beta is fixed from an independent pilot (one scramble, seed purpose 9, 2^14 points); its wall time is recorded so
timing can charge it. 32 scrambles (seed root 2026102201, purpose 0) to 2^18, prefix means at 2^m for h and r on
the same points. Fit sd(n) = A n^-r on marks n >= 2^13 (OLS in logs) and n(eps) = (t_.995,15 A / (4 * 0.45 eps))^(1/r)
exactly as research/frontier_classical_20261001/fit.py.
Run (repo root, Stage C env without -I):
  .context/frontier_t0_env/Scripts/python.exe -m research.c10_challengers_20261022.rate_cv <out_dir>
"""
import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import json
import math
import multiprocessing as mp
import sys
import time
from pathlib import Path

import numpy as np
from scipy.special import ndtr
from scipy.stats import qmc

from research.frontier_classical_20261001.basis import canonical_factor
from research.frontier_classical_20261001.fit import EPS, SHARE, T995_15
from research.frontier_classical_20261001.timing import CHUNK
from research.c10_challengers_20261022.fast_kernels import preint_with_controls
from research.c10_challengers_20261022.fast_pipeline import ndtri_as241

ROOT_C10 = 2026102201
SCR = 32
M_TOP = 18
CASES = (sc.Case(0, 4, 12), sc.Case(1, 8, 52))


def control_means(case, L, mu):
    disc = math.exp(-case.rate * case.maturity)
    mG = float(np.mean(mu))
    sG = float(math.sqrt(np.sum(np.mean(L, axis=0) ** 2)))

    def ln_call(k, cap=None):
        d2 = (mG - math.log(k)) / sG
        val = math.exp(mG + sG * sG / 2) * ndtr(d2 + sG) - k * ndtr(d2)
        if cap is not None:
            d2h = (mG - math.log(cap)) / sG
            val -= math.exp(mG + sG * sG / 2) * ndtr(d2h + sG) - k * ndtr(d2h)
        return disc * val
    eA = float(np.mean(np.exp(mu + 0.5 * np.sum(L ** 2, axis=1))))
    return np.array([ln_call(case.strike), disc * eA, ln_call(case.strike, case.barrier)])


def setup(case):
    L, _ = canonical_factor(case.na, case.nt, case.sigma, case.rho, case.maturity)
    mu = sc.drift(case)
    return L, mu, np.ascontiguousarray(L[:, 0][:case.nt])


def batch(case, L, mu, vdate, u):
    z = ndtri_as241(u, 1e-15, 1 - 1e-15)
    x = z @ L.T + mu
    return preint_with_controls(x, np.ascontiguousarray(z[:, 0]), vdate, case.na, case.nt,
                                math.exp(-case.rate * case.maturity), case.strike, case.barrier)


def pilot(case):
    t = time.perf_counter()
    L, mu, vdate = setup(case)
    eg = control_means(case, L, mu)
    smp = qmc.Sobol(case.dim, scramble=True, seed=np.random.default_rng([ROOT_C10, case.case_index, 9, 0, 0]))
    Y = np.concatenate([batch(case, L, mu, vdate, smp.random(CHUNK)) for _ in range(4)])
    G = Y[:, 1:] - eg
    h = Y[:, 0]
    Gc = G - G.mean(axis=0)
    beta = np.linalg.solve(Gc.T @ Gc, Gc.T @ (h - h.mean()))
    return beta, eg, time.perf_counter() - t


def scramble(task):
    case, s, beta, eg = task
    L, mu, vdate = setup(case)
    smp = qmc.Sobol(case.dim, scramble=True, seed=np.random.default_rng([ROOT_C10, case.case_index, 0, 0, s]))
    marks = [2 ** m for m in range(6, M_TOP + 1)]
    th = tr = 0.0
    tg = np.zeros(3)
    count = 0
    ph, pr, pg = {}, {}, {}
    while count < 2 ** M_TOP:
        Y = batch(case, L, mu, vdate, smp.random(CHUNK))
        h = Y[:, 0]
        r = h - (Y[:, 1:] - eg) @ beta
        ch, cr = np.cumsum(h), np.cumsum(r)
        cg = np.cumsum(Y[:, 1:], axis=0)
        for n in marks:
            if count < n <= count + CHUNK:
                ph[n] = (th + ch[n - count - 1]) / n
                pr[n] = (tr + cr[n - count - 1]) / n
                pg[n] = ((tg + cg[n - count - 1]) / n).tolist()
        th += ch[-1]
        tr += cr[-1]
        tg += cg[-1]
        count += CHUNK
    return dict(s=s, h=ph, r=pr, g=pg)


def fit(sd):
    ns = sorted(n for n in sd if n >= 2 ** 13)
    X = np.log(np.array(ns, dtype=float))
    Yl = np.log(np.array([sd[n] for n in ns]))
    slope, icpt = np.polyfit(X, Yl, 1)
    A, r = math.exp(icpt), -slope
    return dict(A=A, r=r, n_eps={str(e): (T995_15 * A / (4.0 * SHARE * e)) ** (1.0 / r) for e in EPS})


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=False)
    res = dict(meta=dict(script="research/c10_challengers_20261022/rate_cv.py", python=sys.version, root=ROOT_C10,
                         scrambles=SCR, m_top=M_TOP), cases={})
    with mp.Pool(16) as pool:
        for case in CASES:
            beta, eg, t_pilot = pilot(case)
            rows = pool.map(scramble, [(case, s, beta, eg) for s in range(SCR)], chunksize=1)
            marks = sorted(rows[0]["h"])
            sd_h = {n: float(np.std([r["h"][n] for r in rows], ddof=1)) for n in marks}
            sd_r = {n: float(np.std([r["r"][n] for r in rows], ddof=1)) for n in marks}
            top = marks[-1]
            mh = float(np.mean([r["h"][top] for r in rows]))
            mr = float(np.mean([r["r"][top] for r in rows]))
            gbar = np.mean([r["g"][top] for r in rows], axis=0)
            gsd = np.std([r["g"][top] for r in rows], axis=0, ddof=1) / math.sqrt(SCR)
            fh, fr = fit(sd_h), fit(sd_r)
            res["cases"][case.name] = dict(
                beta=beta.tolist(), control_means_closed_form=eg.tolist(), control_means_rqmc=gbar.tolist(),
                control_means_rqmc_se=gsd.tolist(), pilot_wall_s=t_pilot,
                mean_h_top=mh, mean_r_top=mr, hw99_h_top=float(2.744 * sd_h[top] / math.sqrt(SCR)),
                hw99_r_top=float(2.744 * sd_r[top] / math.sqrt(SCR)),
                sd_h=sd_h, sd_r=sd_r, sd_ratio={n: sd_h[n] / sd_r[n] for n in marks},
                fit_preint=fh, fit_preint_cv=fr,
                n_run={k: 2 ** math.ceil(math.log2(v)) for k, v in fr["n_eps"].items()},
                n_run_preint={k: 2 ** math.ceil(math.log2(v)) for k, v in fh["n_eps"].items()},
                label="meas (RQMC, 32 scrambles, paired points)")
            c = res["cases"][case.name]
            print(case.name, "beta", np.round(beta, 4), "sd ratio at 2^17", round(c["sd_ratio"][2 ** 17], 3),
                  "r_h", round(fh["r"], 3), "r_cv", round(fr["r"], 3),
                  "n(0.001) h/cv", round(fh["n_eps"]["0.001"]), round(fr["n_eps"]["0.001"]),
                  "means h/cv", round(mh, 6), round(mr, 6), "ctrl closed vs rqmc", np.round(eg, 5), np.round(gbar, 5),
                  flush=True)
    with open(out / "rate_cv.json", "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
