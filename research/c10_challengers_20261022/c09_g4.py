"""C09 (register): a timed, successful, distribution-free 99% classical price at the binding cell, plus the same-state
practice RQMC time, so the symmetric-convention factor is a measured same-state ratio (N1 modelled it as 36.9x).

Distribution-free estimator: iid preintegrated samples h(y) (first canonical direction integrated; fast kernel), with
the two-sided empirical-Bernstein bound of Maurer & Pontil (2009, Thm 4) at delta = 0.01:
    |mean - mu| <= sqrt(2 V_n ln(4/delta) / n) + 7 R ln(4/delta) / (3 (n - 1)),
V_n the sample variance and R the range of h. R = 17.30: h(y) <= h*(z_H(y)) <= 17.2900 for every y (frontier probe
P1, analytic bound for the first canonical direction) and h >= 0 (mod; N1 assumed $40). n is fixed in advance from an
independent pilot (2^16 points) with a 2% margin; the run fails (reported) if the achieved bound exceeds 0.45 eps.
Wall time runs from submission to the final mean and bound and includes the pilot.
Practice run (same state, before and after): 16-scramble preint_fast at item C2's n_run, as research/c10_challengers_20261022/run_timing.py.
Run (repo root, Stage C env without -I):
  .context/frontier_t0_env/Scripts/python.exe -m research.c10_challengers_20261022.c09_g4 <out_dir> [case_index] [eps]
"""
import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import json
import math
import multiprocessing as mp
import sys
import time
from pathlib import Path

import numpy as np

from research.frontier_classical_20261001.basis import canonical_factor
from research.frontier_classical_20261001.c2_timing import machine_state
from research.frontier_classical_20261001.timing import CHUNK, wait_workers
from research.c10_challengers_20261022 import run_timing as rt
from research.c10_challengers_20261022.fast_kernels import knockout_preint_fast

ROOT_C09 = 2026102209
WORKERS = 16
DELTA = 0.01
R_RANGE = 17.30
_F = {}


def _setup(case):
    key = case.case_index
    if key not in _F:
        L, _ = canonical_factor(case.na, case.nt, case.sigma, case.rho, case.maturity)
        _F[key] = (L, sc.drift(case), np.ascontiguousarray(L[:, 0][:case.nt]))
    return _F[key]


def iid_part(task):
    """One worker's share: n_pts iid preintegrated samples. Returns (count, sum, sum of squares, min, max)."""
    case, seed_key, n_pts = task
    L, mu, vdate = _setup(case)
    disc = math.exp(-case.rate * case.maturity)
    rng = np.random.default_rng(list(seed_key))
    cnt, s1, s2, lo, hi = 0, 0.0, 0.0, math.inf, -math.inf
    while cnt < n_pts:
        m = min(CHUNK, n_pts - cnt)
        z = rng.standard_normal((m, case.dim))
        x = z @ L.T + mu
        y = knockout_preint_fast(x, np.ascontiguousarray(z[:, 0]), vdate, case.na, case.nt, disc,
                                 case.strike, case.barrier)
        s1 += float(y.sum())
        s2 += float((y * y).sum())
        lo, hi = min(lo, float(y.min())), max(hi, float(y.max()))
        cnt += m
    return cnt, s1, s2, lo, hi


def iid_run(pool, case, n, purpose):
    per = [n // WORKERS + (1 if w < n % WORKERS else 0) for w in range(WORKERS)]
    parts = pool.map(iid_part, [(case, (ROOT_C09, case.case_index, purpose, 0, w), per[w]) for w in range(WORKERS)],
                     chunksize=1)
    cnt = sum(p[0] for p in parts)
    s1 = sum(p[1] for p in parts)
    s2 = sum(p[2] for p in parts)
    mean = s1 / cnt
    var = (s2 - cnt * mean * mean) / (cnt - 1)
    return dict(n=cnt, mean=mean, var=var, min=min(p[3] for p in parts), max=max(p[4] for p in parts))


def eb_bound(var, n):
    lg = math.log(4 / DELTA)
    return math.sqrt(2 * var * lg / n) + 7 * R_RANGE * lg / (3 * (n - 1))


def n_for(var, target):
    lo, hi = 2, 10 ** 12
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if eb_bound(var, mid) <= target:
            hi = mid
        else:
            lo = mid
    return hi


def practice(pool, case, eps, reps):
    n_run = {(0, 0.001): 2 ** 17, (1, 0.001): 2 ** 17, (0, 0.01): 2 ** 12, (1, 0.01): 2 ** 11}[(case.case_index, eps)]  # item C2 n_run
    walls = []
    for r in range(reps):
        run = rt.all16(pool, f"c09p-{case.name}-{r}", case, "preint_fast", (ROOT_C09, case.case_index, 3, r), n_run)
        walls.append(run["wall"])
    return dict(n_run=n_run, walls=walls, median=float(np.median(walls)))


def main(out_dir, case_index, eps):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=False)
    case = {0: sc.Case(0, 4, 12), 1: sc.Case(1, 8, 52)}[case_index]
    target = 0.45 * eps
    res = dict(meta=dict(script="research/c10_challengers_20261022/c09_g4.py", python=sys.version, root=ROOT_C09,
                         delta=DELTA, R=R_RANGE, case=case.name, eps=eps, target=target, workers=WORKERS),
               machine=[machine_state()])
    with mp.Pool(WORKERS, initializer=rt.warm_up) as pool:
        wait_workers(pool, WORKERS)
        res["practice_before"] = practice(pool, case, eps, 3)
        t0 = time.perf_counter()
        pil = iid_run(pool, case, 2 ** 16, purpose=12)
        n = int(math.ceil(1.02 * n_for(pil["var"], target)))
        main_run = iid_run(pool, case, n, purpose=13)
        bound = eb_bound(main_run["var"], main_run["n"])
        wall = time.perf_counter() - t0
        res["practice_after"] = practice(pool, case, eps, 3)
    res["machine"].append(machine_state())
    prac = float(np.median(res["practice_before"]["walls"] + res["practice_after"]["walls"]))
    res.update(pilot=pil, n_target=n, main=main_run, eb_bound=bound, success=bound <= target, wall_df=wall,
               practice_median=prac, factor_df_over_practice=wall / prac,
               sigma_h=math.sqrt(main_run["var"]), within_range=main_run["min"] >= 0 and main_run["max"] <= R_RANGE,
               label="meas (timed distribution-free price and same-state practice time); R from P1 (mod)")
    print(case.name, eps, "n", n, "bound", bound, "target", target, "success", res["success"], "wall_df", round(wall, 2),
          "practice", round(prac, 3), "factor", round(wall / prac, 2), "range", main_run["min"], main_run["max"], flush=True)
    with open(out / "c09_g4.json", "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1, float(sys.argv[3]) if len(sys.argv) > 3 else 0.001)
