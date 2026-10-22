"""C10 challenger: two-direction smoothing (Stage C 'not executed': multi-direction numerical smoothing).

Paired RQMC rate study on the same points: h (Stage C preint estimand, fast kernel) and h2_{k,Q} (h further averaged
over canonical direction k by a Q-node Gauss-Hermite rule), for k in {1 (asset-dispersion mode), 8 (second common
time mode)} and Q in {6, 12} (Q = 12 doubles as the quadrature-bias check for Q = 6). 32 scrambles (root 2026102201,
purpose 10) to 2^16, prefix sd at each 2^m; per-chunk kernel cost measured in-process. Break-even: smoothing pays
only if sd_h / sd_h2 > (cost_h2 / cost_h)^r at equal n.
Run (repo root, Stage C env without -I):
  .context/frontier_t0_env/Scripts/python.exe -m research.c10_challengers_20261022.rate_smooth2 <out_dir>
"""
import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import json
import math
import multiprocessing as mp
import sys
import time
from pathlib import Path

import numpy as np
from scipy.stats import qmc

from research.frontier_classical_20261001.basis import canonical_factor
from research.frontier_classical_20261001.timing import CHUNK
from research.c10_challengers_20261022.fast_kernels import knockout_preint_fast, preint_smooth2
from research.c10_challengers_20261022.fast_pipeline import ndtri_as241

ROOT_C10 = 2026102201
SCR = 32
M_TOP = 16
CONFIGS = ((1, 6), (1, 12), (8, 6), (8, 12))
CASES = (sc.Case(0, 4, 12), sc.Case(1, 8, 52))


def gh(q):
    x, w = np.polynomial.hermite_e.hermegauss(q)
    return np.ascontiguousarray(x), np.ascontiguousarray(w / w.sum())


def scramble(task):
    case, s = task
    L, _ = canonical_factor(case.na, case.nt, case.sigma, case.rho, case.maturity)
    mu = sc.drift(case)
    vdate = np.ascontiguousarray(L[:, 0][:case.nt])
    disc = math.exp(-case.rate * case.maturity)
    smp = qmc.Sobol(case.dim, scramble=True, seed=np.random.default_rng([ROOT_C10, case.case_index, 10, 0, s]))
    rules = {q: gh(q) for q in {c[1] for c in CONFIGS}}
    keys = ["h"] + [f"k{k}_Q{q}" for k, q in CONFIGS]
    tot = {k: 0.0 for k in keys}
    pref = {k: {} for k in keys}
    cost = {k: 0.0 for k in keys}
    marks = [2 ** m for m in range(6, M_TOP + 1)]
    count = 0
    while count < 2 ** M_TOP:
        z = ndtri_as241(smp.random(CHUNK), 1e-15, 1 - 1e-15)
        x = z @ L.T + mu
        z0 = np.ascontiguousarray(z[:, 0])
        t = time.perf_counter()
        ys = {"h": knockout_preint_fast(x, z0, vdate, case.na, case.nt, disc, case.strike, case.barrier)}
        cost["h"] += time.perf_counter() - t
        for k, q in CONFIGS:
            t = time.perf_counter()
            ys[f"k{k}_Q{q}"] = preint_smooth2(x, z0, np.ascontiguousarray(z[:, k]), vdate,
                                              np.ascontiguousarray(L[:, k]), rules[q][0], rules[q][1],
                                              case.na, case.nt, disc, case.strike, case.barrier)
            cost[f"k{k}_Q{q}"] += time.perf_counter() - t
        for key, y in ys.items():
            cs = np.cumsum(y)
            for n in marks:
                if count < n <= count + CHUNK:
                    pref[key][n] = (tot[key] + cs[n - count - 1]) / n
            tot[key] += cs[-1]
        count += CHUNK
    return dict(prefix=pref, cost=cost)


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=False)
    res = dict(meta=dict(script="research/c10_challengers_20261022/rate_smooth2.py", python=sys.version,
                         scrambles=SCR, m_top=M_TOP, configs=CONFIGS), cases={})
    with mp.Pool(16) as pool:
        for case in CASES:
            rows = pool.map(scramble, [(case, s) for s in range(SCR)], chunksize=1)
            keys = list(rows[0]["prefix"])
            marks = sorted(rows[0]["prefix"]["h"])
            sd = {k: {n: float(np.std([r["prefix"][k][n] for r in rows], ddof=1)) for n in marks} for k in keys}
            top = marks[-1]
            mean = {k: float(np.mean([r["prefix"][k][top] for r in rows])) for k in keys}
            cost = {k: float(np.sum([r["cost"][k] for r in rows])) for k in keys}
            c = dict(sd=sd, mean_top=mean, kernel_cost_s=cost,
                     cost_ratio={k: cost[k] / cost["h"] for k in keys},
                     sd_ratio_top={k: sd["h"][top] / sd[k][top] for k in keys},
                     sd_ratio_2_14={k: sd["h"][2 ** 14] / sd[k][2 ** 14] for k in keys},
                     label="meas (RQMC, 32 scrambles, paired points; kernel cost in-process)")
            res["cases"][case.name] = c
            print(case.name, "sd ratio @2^16", {k: round(v, 3) for k, v in c["sd_ratio_top"].items()},
                  "cost ratio", {k: round(v, 2) for k, v in c["cost_ratio"].items()},
                  "means", {k: round(v, 6) for k, v in mean.items()}, flush=True)
    with open(out / "rate_smooth2.json", "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
