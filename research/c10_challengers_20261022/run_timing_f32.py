"""C10 paired timing, round 2: Stage C preint vs preint_fast vs preint_fast32 (float32 GEMM, admitted by the eps/10
check in f32_check.py), item C2 confirmation protocol as run_timing.py, $0.001 cells, 10 replications, own seed root.
Run (repo root, Stage C env without -I):
  .context/frontier_t0_env/Scripts/python.exe -m research.c10_challengers_20261022.run_timing_f32 <out_dir> [reps]
"""
import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import json
import math
import multiprocessing as mp
import sys
import time
from pathlib import Path

import numpy as np
from scipy.special import ndtri
from scipy.stats import qmc

from research.frontier_classical_20261001.basis import canonical_factor
from research.frontier_classical_20261001.c2_timing import machine_state
from research.frontier_classical_20261001.fit import SHARE, T995_15
from research.frontier_classical_20261001.kernels import knockout_preint
from research.frontier_classical_20261001.timing import CHUNK, wait_workers
from research.c10_challengers_20261022.fast_kernels import knockout_preint_fast
from research.c10_challengers_20261022.fast_pipeline import ndtri_as241
from research.c10_challengers_20261022.run_timing import warm_up

ROOT = 2026102233
METHODS = ("preint", "preint_fast", "preint_fast32")
CELLS = ((sc.Case(1, 8, 52), 0.001, 3, 2 ** 17), (sc.Case(0, 4, 12), 0.001, 3, 2 ** 17))
_F = {}


def _factor(run_id, case):
    if run_id not in _F:
        _F.clear()
        L, _ = canonical_factor(case.na, case.nt, case.sigma, case.rho, case.maturity)
        v = np.ascontiguousarray(L[:, 0])
        _F[run_id] = (L, v, np.ascontiguousarray(v[:case.nt]), np.ascontiguousarray(L.T.astype(np.float32)))
    return _F[run_id]


def timed_scramble(task):
    run_id, case, method, seed_key, n_top = task
    L, v, vdate, L32 = _factor(run_id, case)
    mu = sc.drift(case)
    disc = math.exp(-case.rate * case.maturity)
    sampler = qmc.Sobol(case.dim, scramble=True, seed=np.random.default_rng(list(seed_key)))
    total, count = 0.0, 0
    while count < n_top:
        size = min(CHUNK, n_top - count)
        u = sampler.random(size)
        if method == "preint":
            z = ndtri(np.clip(u, 1e-15, 1 - 1e-15))
            x = z @ L.T + mu
            y = knockout_preint(x, np.ascontiguousarray(z[:, 0]), v, case.na, case.nt, disc, case.strike, case.barrier)
        else:
            z = ndtri_as241(u, 1e-15, 1 - 1e-15)
            if method == "preint_fast32":
                x = (z.astype(np.float32) @ L32).astype(np.float64) + mu
            else:
                x = z @ L.T + mu
            y = knockout_preint_fast(x, np.ascontiguousarray(z[:, 0]), vdate, case.na, case.nt, disc,
                                     case.strike, case.barrier)
        total += float(np.sum(y))
        count += size
    return total / n_top


def all16(pool, run_id, case, method, key_prefix, n_top):
    tasks = [(run_id, case, method, key_prefix + (s,), n_top) for s in range(16)]
    submit = time.perf_counter()
    means = np.array(pool.map(timed_scramble, tasks, chunksize=1))
    return dict(wall=time.perf_counter() - submit, mean=float(means.mean()),
                hw99=float(T995_15 * means.std(ddof=1) / 4), scramble_means=means.tolist())


def main(out_dir, reps):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=False)
    res = dict(meta=dict(script="research/c10_challengers_20261022/run_timing_f32.py", python=sys.version, reps=reps,
                         root=ROOT), machine=[], cells={})
    t0 = time.time()
    while time.time() - t0 < 3600:
        st = machine_state()
        if st["idle"]:
            break
        time.sleep(60)
    st["waited_s"] = round(time.time() - t0)
    res["machine"].append(st)
    with mp.Pool(16, initializer=warm_up) as pool:
        wait_workers(pool, 16)
        for case, eps, ei, n_run in CELLS:
            key = f"{case.name}|{eps}"
            res["machine"].append(dict(cell=key, **machine_state()))
            runs = {m: [] for m in METHODS}
            for r in range(reps):
                for m in METHODS[r % 3:] + METHODS[:r % 3]:
                    runs[m].append(all16(pool, f"{key}-{m}-{r}", case, m, (ROOT, case.case_index, 3, 100 * ei + r), n_run))
            med = {m: float(np.median([x["wall"] for x in runs[m]])) for m in METHODS}
            res["cells"][key] = dict(n_run=n_run, median_wall=med,
                                     speedup_vs_stageC={m: med["preint"] / med[m] for m in METHODS},
                                     f32_over_fast=med["preint_fast"] / med["preint_fast32"],
                                     max_abs_mean_diff_f32_vs_stageC=float(max(abs(a["mean"] - b["mean"]) for a, b in
                                                                               zip(runs["preint"], runs["preint_fast32"]))),
                                     runs={m: [dict(wall=x["wall"], mean=x["mean"], hw99=x["hw99"]) for x in runs[m]]
                                           for m in METHODS})
            print(key, {m: round(v, 3) for m, v in med.items()}, "f32/fast", round(res["cells"][key]["f32_over_fast"], 3),
                  "mean diff", res["cells"][key]["max_abs_mean_diff_f32_vs_stageC"], flush=True)
    res["machine"].append(dict(end=True, **machine_state()))
    with open(out / "c10_timing_f32.json", "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10)
