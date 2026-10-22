"""C09b (review finding 4b): distribution-free 99% price by REPLICATED RQMC, so the symmetric-convention factor is a
minimum over distribution-free methods, not the iid-EB cost alone.

Each replicate is one m-point Sobol net (unscrambled, base 2^k) under an independent random digital shift plus
uniform sub-cell jitter: u = ((X xor s) + U) / 2^30, X the net's 30-bit integer coordinates, s uniform 30-bit per
dimension, U ~ U(0,1)^d. Every point is marginally uniform, so each replicate mean of the preintegrated h is unbiased,
replicates are iid, and each replicate mean lies in [0, R] with R = 17.30 (frontier probe P1 bound). The two-sided
empirical-Bernstein bound (Maurer-Pontil Thm 4, delta 0.01) is applied to the n replicate means. For each m in
{16, 64, 256, 1024} a pilot of 2^11 replicates estimates V_m; the m minimising the planned total points is run with
n fixed in advance (2% margin). Wall time includes every pilot (conservative for the classical side). Same-state
practice times before/after, as C09.
Run (repo root, Stage C env without -I):
  .context/frontier_t0_env/Scripts/python.exe -m research.c10_challengers_20261022.c09b_rep <out_dir> [case_index] [eps]
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

from research.frontier_classical_20261001.c2_timing import machine_state
from research.frontier_classical_20261001.timing import wait_workers
from research.c10_challengers_20261022 import run_timing as rt
from research.c10_challengers_20261022.c09_g4 import R_RANGE, eb_bound, n_for, practice, _setup
from research.c10_challengers_20261022.fast_kernels import knockout_preint_fast
from research.c10_challengers_20261022.fast_pipeline import ndtri_as241

ROOT_C09B = 2026102219
WORKERS = 16
MS = (16, 64, 256, 1024)
BITS = 30
_NET = {}


def _net(case, m):
    key = (case.case_index, m)
    if key not in _NET:
        pts = qmc.Sobol(case.dim, scramble=False).random_base2(int(math.log2(m)))
        X = np.round(pts * 2 ** BITS).astype(np.uint32)
        assert np.all(X < 2 ** BITS)
        _NET[key] = X
    return _NET[key]


def rep_part(task):
    """One worker's share: n_rep replicates of m points. Returns (count, sum of means, sum of squared means)."""
    case, m, seed_key, n_rep = task
    L, mu, vdate = _setup(case)
    X = _net(case, m)
    disc = math.exp(-case.rate * case.maturity)
    rng = np.random.default_rng(list(seed_key))
    per = max(1, 4096 // m)
    cnt, s1, s2 = 0, 0.0, 0.0
    while cnt < n_rep:
        r = min(per, n_rep - cnt)
        S = rng.integers(0, 2 ** BITS, size=(r, 1, case.dim), dtype=np.uint32)
        U = ((X[None, :, :] ^ S).astype(np.float64) + rng.random((r, m, case.dim))) / 2 ** BITS
        u = U.reshape(r * m, case.dim)
        z = ndtri_as241(u, 1e-15, 1 - 1e-15)
        x = z @ L.T + mu
        y = knockout_preint_fast(x, np.ascontiguousarray(z[:, 0]), vdate, case.na, case.nt, disc,
                                 case.strike, case.barrier)
        means = y.reshape(r, m).mean(axis=1)
        s1 += float(means.sum())
        s2 += float((means * means).sum())
        cnt += r
    return cnt, s1, s2


def rep_run(pool, case, m, n_rep, purpose):
    per = [n_rep // WORKERS + (1 if w < n_rep % WORKERS else 0) for w in range(WORKERS)]
    parts = pool.map(rep_part, [(case, m, (ROOT_C09B, case.case_index, purpose, m, w), per[w])
                                for w in range(WORKERS) if per[w] > 0], chunksize=1)
    cnt = sum(p[0] for p in parts)
    s1 = sum(p[1] for p in parts)
    s2 = sum(p[2] for p in parts)
    mean = s1 / cnt
    return dict(n=cnt, mean=mean, var=(s2 - cnt * mean * mean) / (cnt - 1))


def main(out_dir, case_index, eps):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=False)
    case = {0: sc.Case(0, 4, 12), 1: sc.Case(1, 8, 52)}[case_index]
    target = 0.45 * eps
    res = dict(meta=dict(script="research/c10_challengers_20261022/c09b_rep.py", python=sys.version, root=ROOT_C09B,
                         R=R_RANGE, case=case.name, eps=eps, target=target, ms=MS), machine=[machine_state()])
    with mp.Pool(WORKERS, initializer=rt.warm_up) as pool:
        wait_workers(pool, WORKERS)
        pool.map(_net_warm, [(case, m) for m in MS for _ in range(WORKERS)], chunksize=1)
        res["practice_before"] = practice(pool, case, eps, 3)
        t0 = time.perf_counter()
        pilots = {}
        for m in MS:
            p = rep_run(pool, case, m, 2 ** 11, purpose=20)
            n = int(math.ceil(1.02 * n_for(p["var"], target)))
            pilots[m] = dict(var=p["var"], sd_rep=math.sqrt(p["var"]), n_rep_planned=n, points_planned=n * m)
        m_best = min(MS, key=lambda mm: pilots[mm]["points_planned"])
        main_run = rep_run(pool, case, m_best, pilots[m_best]["n_rep_planned"], purpose=21)
        bound = eb_bound(main_run["var"], main_run["n"])
        wall = time.perf_counter() - t0
        res["practice_after"] = practice(pool, case, eps, 3)
    res["machine"].append(machine_state())
    prac = float(np.median(res["practice_before"]["walls"] + res["practice_after"]["walls"]))
    res.update(pilots={str(k): v for k, v in pilots.items()}, m_best=m_best, main=main_run, eb_bound=bound,
               success=bound <= target, wall_df=wall, practice_median=prac, factor_df_over_practice=wall / prac,
               points=main_run["n"] * m_best,
               label="meas (timed replicated-RQMC distribution-free price; same-state practice); R from P1 (mod)")
    print(case.name, eps, "pilots", {k: (round(v["sd_rep"], 5), v["points_planned"]) for k, v in pilots.items()},
          "m", m_best, "n_rep", main_run["n"], "bound", bound, "success", res["success"], "wall", round(wall, 2),
          "practice", round(prac, 3), "factor", round(wall / prac, 2), flush=True)
    with open(out / "c09b_rep.json", "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


def _net_warm(task):
    case, m = task
    _net(case, m)
    _setup(case)
    return 0


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1, float(sys.argv[3]) if len(sys.argv) > 3 else 0.001)
