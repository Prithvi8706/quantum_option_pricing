"""Remove two assumptions in headline run006 at the binding cell B8x52 $0.001 by measuring them with the float32-GEMM
method itself: (1) the symmetric distribution-free factor, replicated RQMC (m = 16, as c09b_rep.py's selected m)
with float32 GEMM, against same-state practice runs of preint_fast32; (2) the 1-worker / 16-worker ratio of
preint_fast32. Same estimators, bound (EB, R = 17.30) and protocols as c09b_rep.py / h16_fast.py.
Run (repo root, Stage C env without -I):
  .context/frontier_t0_env/Scripts/python.exe -m research.c10_challengers_20261022.f32_consistency <out_dir>
"""
import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import json
import math
import multiprocessing as mp
import sys
import time
from pathlib import Path

import numpy as np

from research.frontier_classical_20261001.c2_timing import machine_state
from research.frontier_classical_20261001.timing import wait_workers
from research.c10_challengers_20261022 import run_timing_f32 as rf
from research.c10_challengers_20261022.c09_g4 import eb_bound, n_for, _setup
from research.c10_challengers_20261022.c09b_rep import BITS, _net
from research.c10_challengers_20261022.fast_kernels import knockout_preint_fast
from research.c10_challengers_20261022.fast_pipeline import ndtri_as241

ROOT_F = 2026102234
M = 16


def rep_part32(task):
    case, seed_key, n_rep = task
    L, mu, vdate = _setup(case)
    L32 = np.ascontiguousarray(L.T.astype(np.float32))
    X = _net(case, M)
    disc = math.exp(-case.rate * case.maturity)
    rng = np.random.default_rng(list(seed_key))
    per = 4096 // M
    cnt, s1, s2 = 0, 0.0, 0.0
    while cnt < n_rep:
        r = min(per, n_rep - cnt)
        S = rng.integers(0, 2 ** BITS, size=(r, 1, case.dim), dtype=np.uint32)
        u = (((X[None, :, :] ^ S).astype(np.float64) + rng.random((r, M, case.dim))) / 2 ** BITS).reshape(r * M, case.dim)
        z = ndtri_as241(u, 1e-15, 1 - 1e-15)
        x = (z.astype(np.float32) @ L32).astype(np.float64) + mu
        y = knockout_preint_fast(x, np.ascontiguousarray(z[:, 0]), vdate, case.na, case.nt, disc, case.strike, case.barrier)
        mm = y.reshape(r, M).mean(axis=1)
        s1 += float(mm.sum())
        s2 += float((mm * mm).sum())
        cnt += r
    return cnt, s1, s2


def rep_run(pool, case, n_rep, purpose):
    per = [n_rep // 16 + (1 if w < n_rep % 16 else 0) for w in range(16)]
    parts = pool.map(rep_part32, [(case, (ROOT_F, case.case_index, purpose, M, w), per[w]) for w in range(16)], chunksize=1)
    cnt = sum(p[0] for p in parts)
    mean = sum(p[1] for p in parts) / cnt
    return dict(n=cnt, mean=mean, var=(sum(p[2] for p in parts) - cnt * mean * mean) / (cnt - 1))


def practice(pool, case, reps, tag):
    return [rf.all16(pool, f"f32c-{tag}-{r}", case, "preint_fast32", (ROOT_F, case.case_index, 3, r), 2 ** 17)["wall"]
            for r in range(reps)]


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=False)
    case = sc.Case(1, 8, 52)
    target = 0.45 * 0.001
    res = dict(meta=dict(script="research/c10_challengers_20261022/f32_consistency.py", python=sys.version, m=M,
                         root=ROOT_F), machine=[machine_state()])
    with mp.Pool(16, initializer=rf.warm_up) as pool:
        wait_workers(pool, 16)
        before = practice(pool, case, 3, "b")
        t0 = time.perf_counter()
        pil = rep_run(pool, case, 2 ** 11, 30)
        n = int(math.ceil(1.02 * n_for(pil["var"], target)))
        main_run = rep_run(pool, case, n, 31)
        bound = eb_bound(main_run["var"], main_run["n"])
        wall = time.perf_counter() - t0
        after = practice(pool, case, 3, "a")
        w16 = float(np.median([rf.all16(pool, f"f32c-w16-{r}", case, "preint_fast32", (ROOT_F, case.case_index, 1, r),
                                        2 ** 17)["wall"] for r in range(3)]))
    with mp.Pool(1, initializer=rf.warm_up) as pool1:
        wait_workers(pool1, 1)
        w1 = float(np.median([rf.all16(pool1, f"f32c-w1-{r}", case, "preint_fast32", (ROOT_F, case.case_index, 1, r),
                                       2 ** 17)["wall"] for r in range(3)]))
    prac = float(np.median(before + after))
    res["machine"].append(machine_state())
    res.update(pilot=pil, n_rep=n, main=main_run, eb_bound=bound, success=bound <= target, wall_df=wall,
               practice=before + after, practice_median=prac, factor_df_over_practice=wall / prac,
               w1=w1, w16=w16, ratio_1_over_16=w1 / w16, label="meas (float32-GEMM method; pilot is 1 m only)")
    print("factor", round(wall / prac, 2), "success", res["success"], "bound", bound, "wall", round(wall, 2), "practice",
          round(prac, 3), "ratio_1_16", round(w1 / w16, 2), flush=True)
    with open(out / "f32_consistency.json", "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
