"""C10 paired timing: Stage C `preint` vs the same estimand with faster arithmetic (register C10, 22 Oct 2026).

Protocol mirrors item C2 measured confirmation (ANALYSIS_SPEC_STAGE_C.md): 16 worker processes, 16 scrambles,
all-16 wall time from submission to the 16-scramble mean and 99% t half-width, factor built inside the timed
interval, warm workers. Methods share every seed key within a replication (identical Sobol points), and are
interleaved inside each replication so they see the same machine state. Seed root 2026102201 (C10's own root, per
deviation D6). n_run per cell is item C2's recorded n_run.

Methods:
  preint        Stage C pipeline exactly: scipy ndtri -> GEMM -> kernels.knockout_preint
  preint_fk     scipy ndtri -> GEMM -> fast_kernels.knockout_preint_fast
  preint_fast   AS241 ndtri -> GEMM -> fast_kernels.knockout_preint_fast
Run (repo root, Stage C env without -I):
  .context/frontier_t0_env/Scripts/python.exe -m research.c10_challengers_20261022.run_timing <out_dir> [reps]
"""
import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import hashlib
import json
import math
import multiprocessing as mp
import os
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

ROOT_C10 = 2026102201
WORKERS = SCRAMBLES = 16
METHODS = ("preint", "preint_fk", "preint_fast")
CELLS = ((sc.Case(1, 8, 52), 0.001, 3, 2 ** 17), (sc.Case(0, 4, 12), 0.001, 3, 2 ** 17),
         (sc.Case(1, 8, 52), 0.01, 2, 2 ** 11), (sc.Case(0, 4, 12), 0.01, 2, 2 ** 12))
_F = {}


def warm_up():
    for case in (sc.Case(0, 4, 12), sc.Case(1, 8, 52)):
        x = np.zeros((2, case.dim))
        knockout_preint(x, np.zeros(2), np.ones(case.dim), case.na, case.nt, 1.0, 100.0, 140.0)
        knockout_preint_fast(x, np.zeros(2), np.ones(case.nt), case.na, case.nt, 1.0, 100.0, 140.0)
    ndtri_as241(np.full((2, 4), 0.5), 1e-15, 1 - 1e-15)


def _factor(run_id, case):
    if run_id not in _F:
        _F.clear()
        L, _ = canonical_factor(case.na, case.nt, case.sigma, case.rho, case.maturity)
        v = np.ascontiguousarray(L[:, 0])
        _F[run_id] = (L, v, np.ascontiguousarray(v[:case.nt]))
    return _F[run_id]


def timed_scramble(task):
    run_id, case, method, seed_key, n_top = task
    t_start = time.perf_counter()
    L, v, vdate = _factor(run_id, case)
    mu = sc.drift(case)
    disc = math.exp(-case.rate * case.maturity)
    sampler = qmc.Sobol(case.dim, scramble=True, seed=np.random.default_rng(list(seed_key)))
    total, count = 0.0, 0
    while count < n_top:
        size = min(CHUNK, n_top - count)
        u = sampler.random(size)
        z = ndtri_as241(u, 1e-15, 1 - 1e-15) if method == "preint_fast" else ndtri(np.clip(u, 1e-15, 1 - 1e-15))
        x = z @ L.T + mu
        z0 = np.ascontiguousarray(z[:, 0])
        if method == "preint":
            y = knockout_preint(x, z0, v, case.na, case.nt, disc, case.strike, case.barrier)
        else:
            y = knockout_preint_fast(x, z0, vdate, case.na, case.nt, disc, case.strike, case.barrier)
        total += float(np.sum(y))
        count += size
    return dict(mean=total / n_top, done=time.perf_counter(), t_start=t_start)


def all16(pool, run_id, case, method, key_prefix, n_top):
    tasks = [(run_id, case, method, key_prefix + (s,), n_top) for s in range(SCRAMBLES)]
    submit = time.perf_counter()
    rows = pool.map(timed_scramble, tasks, chunksize=1)
    means = np.array([r["mean"] for r in rows])
    hw = T995_15 * means.std(ddof=1) / math.sqrt(SCRAMBLES)
    end = time.perf_counter()
    return dict(wall=end - submit, mean=float(means.mean()), hw99=float(hw), scramble_means=means.tolist())


def main(out_dir, reps):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=False)
    code = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob("*.py")}
    log = []
    res = dict(meta=dict(script="research/c10_challengers_20261022/run_timing.py", python=sys.version,
                         numpy=np.__version__, workers=WORKERS, scrambles=SCRAMBLES, root=ROOT_C10, reps=reps,
                         code_sha256=code, cpu=os.environ.get("PROCESSOR_IDENTIFIER")), cells={}, machine_log=log)
    rows_path = out / "rows.jsonl"
    t0 = time.time()
    state = None
    while time.time() - t0 < 3600:
        state = machine_state()
        if state["idle"]:
            break
        time.sleep(60)
    state["waited_s"] = round(time.time() - t0)
    log.append(state)
    with mp.Pool(WORKERS, initializer=warm_up) as pool:
        wait_workers(pool, WORKERS)
        for case, eps, eps_index, n_run in CELLS:
            key = f"{case.name}|{eps}"
            log.append(dict(cell=key, **machine_state()))
            runs = {m: [] for m in METHODS}
            for r in range(reps):
                order = METHODS[r % 3:] + METHODS[:r % 3]  # rotate so no method always goes first
                for m in order:
                    run = all16(pool, f"{key}-{m}-{r}", case, m, (ROOT_C10, case.case_index, 3, 100 * eps_index + r), n_run)
                    runs[m].append(run)
                    with open(rows_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps(dict(cell=key, method=m, rep=r, wall=run["wall"], mean=run["mean"],
                                                hw99=run["hw99"])) + "\n")
            cell = dict(n_run=n_run, eps=eps, methods={})
            for m in METHODS:
                walls = [x["wall"] for x in runs[m]]
                sd = float(np.std(np.concatenate([x["scramble_means"] for x in runs[m]]), ddof=1))
                hw16 = T995_15 * sd / math.sqrt(SCRAMBLES)
                cell["methods"][m] = dict(median_wall=float(np.median(walls)), min_wall=float(min(walls)),
                                          max_wall=float(max(walls)), pooled_hw16=hw16,
                                          hw_target=SHARE * eps, fraction_hw_ok=float(np.mean(
                                              [x["hw99"] <= SHARE * eps for x in runs[m]])),
                                          mean_of_means=float(np.mean([x["mean"] for x in runs[m]])), runs=runs[m])
            pm = [abs(a["mean"] - b["mean"]) for a, b in zip(runs["preint"], runs["preint_fast"])]
            cell["paired_max_abs_mean_diff_fast_vs_stageC"] = float(max(pm))
            cell["speedup_median"] = {m: cell["methods"]["preint"]["median_wall"] / cell["methods"][m]["median_wall"]
                                      for m in METHODS}
            res["cells"][key] = cell
            print(key, {m: round(cell["methods"][m]["median_wall"], 4) for m in METHODS},
                  "speedup", {m: round(s, 3) for m, s in cell["speedup_median"].items()},
                  "paired mean diff", cell["paired_max_abs_mean_diff_fast_vs_stageC"], flush=True)
    log.append(dict(end=True, **machine_state()))
    with open(out / "c10_timing.json", "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 20)
