"""C10 paired timing including the preint + control-variate challenger (item C2 confirmation protocol).

Methods (interleaved per replication, rotating order; 16 workers, 16 scrambles, all-16 wall):
  preint          Stage C pipeline exactly, at item C2's recorded n_run
  preint_fast     AS241 + fast kernel, same n_run (same points as preint)
  preint_cv_fast  AS241 + preint_with_controls, residual h - beta (g - Eg), at n_run from rate_cv's own C1-style fit;
                  the pilot wall time that fixed beta (rate_cv.json) is added to each wall time.
Primary T_C per method = median wall x max(1, (pooled hw16 / 0.45 eps)^(1/r)) with r from the rate fit, as item C2.
Run (repo root, Stage C env without -I):
  .context/frontier_t0_env/Scripts/python.exe -m research.c10_challengers_20261022.run_timing_cv <rate_cv.json> <out_dir> [reps]
"""
import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import hashlib
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
from research.c10_challengers_20261022.fast_kernels import knockout_preint_fast, preint_with_controls
from research.c10_challengers_20261022.fast_pipeline import ndtri_as241

ROOT_C10 = 2026102201
WORKERS = SCRAMBLES = 16
METHODS = ("preint", "preint_fast", "preint_cv_fast")
C2_NRUN = {("B8x52_H140", 0.001): 2 ** 17, ("B4x12_H140", 0.001): 2 ** 17, ("B8x52_H140", 0.01): 2 ** 11,
           ("B4x12_H140", 0.01): 2 ** 12}
CASES = {"B8x52_H140": sc.Case(1, 8, 52), "B4x12_H140": sc.Case(0, 4, 12)}
_F = {}


def warm_up():
    for case in CASES.values():
        x = np.zeros((2, case.dim))
        knockout_preint(x, np.zeros(2), np.ones(case.dim), case.na, case.nt, 1.0, 100.0, 140.0)
        knockout_preint_fast(x, np.zeros(2), np.ones(case.nt), case.na, case.nt, 1.0, 100.0, 140.0)
        preint_with_controls(x, np.zeros(2), np.ones(case.nt), case.na, case.nt, 1.0, 100.0, 140.0)
    ndtri_as241(np.full((2, 4), 0.5), 1e-15, 1 - 1e-15)


def _factor(run_id, case):
    if run_id not in _F:
        _F.clear()
        L, _ = canonical_factor(case.na, case.nt, case.sigma, case.rho, case.maturity)
        v = np.ascontiguousarray(L[:, 0])
        _F[run_id] = (L, v, np.ascontiguousarray(v[:case.nt]))
    return _F[run_id]


def timed_scramble(task):
    run_id, case, method, seed_key, n_top, beta, eg = task
    L, v, vdate = _factor(run_id, case)
    mu = sc.drift(case)
    disc = math.exp(-case.rate * case.maturity)
    sampler = qmc.Sobol(case.dim, scramble=True, seed=np.random.default_rng(list(seed_key)))
    total, count = 0.0, 0
    while count < n_top:
        size = min(CHUNK, n_top - count)
        u = sampler.random(size)
        if method == "preint":
            z = ndtri(np.clip(u, 1e-15, 1 - 1e-15))
        else:
            z = ndtri_as241(u, 1e-15, 1 - 1e-15)
        x = z @ L.T + mu
        z0 = np.ascontiguousarray(z[:, 0])
        if method == "preint":
            y = knockout_preint(x, z0, v, case.na, case.nt, disc, case.strike, case.barrier)
        elif method == "preint_fast":
            y = knockout_preint_fast(x, z0, vdate, case.na, case.nt, disc, case.strike, case.barrier)
        else:
            Y = preint_with_controls(x, z0, vdate, case.na, case.nt, disc, case.strike, case.barrier)
            y = Y[:, 0] - (Y[:, 1:] - eg) @ beta
        total += float(np.sum(y))
        count += size
    return total / n_top


def all16(pool, run_id, case, method, key_prefix, n_top, beta, eg, extra):
    tasks = [(run_id, case, method, key_prefix + (s,), n_top, beta, eg) for s in range(SCRAMBLES)]
    submit = time.perf_counter()
    means = np.array(pool.map(timed_scramble, tasks, chunksize=1))
    hw = T995_15 * means.std(ddof=1) / math.sqrt(SCRAMBLES)
    return dict(wall=time.perf_counter() - submit + extra, mean=float(means.mean()), hw99=float(hw),
                scramble_means=means.tolist())


def main(rate_path, out_dir, reps):
    rate = json.loads(Path(rate_path).read_text(encoding="utf-8"))["cases"]
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=False)
    code = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob("*.py")}
    res = dict(meta=dict(script="research/c10_challengers_20261022/run_timing_cv.py", python=sys.version,
                         numpy=np.__version__, reps=reps, root=ROOT_C10, code_sha256=code,
                         rate_cv_sha256=hashlib.sha256(Path(rate_path).read_bytes()).hexdigest()),
               cells={}, machine_log=[])
    t0 = time.time()
    while time.time() - t0 < 3600:
        st = machine_state()
        if st["idle"]:
            break
        time.sleep(60)
    st["waited_s"] = round(time.time() - t0)
    res["machine_log"].append(st)
    with mp.Pool(WORKERS, initializer=warm_up) as pool:
        wait_workers(pool, WORKERS)
        for (cname, eps), n_c2 in C2_NRUN.items():
            case = CASES[cname]
            rc = rate[cname]
            beta, eg = np.array(rc["beta"]), np.array(rc["control_means_closed_form"])
            n_cv = rc["n_run"][str(eps)]
            r_cv, r_h = rc["fit_preint_cv"]["r"], rc["fit_preint"]["r"]
            n_of = {"preint": n_c2, "preint_fast": n_c2, "preint_cv_fast": n_cv}
            extra = {"preint": 0.0, "preint_fast": 0.0, "preint_cv_fast": rc["pilot_wall_s"]}
            eps_index = (0.10, 0.03, 0.01, 0.001).index(eps)
            key = f"{cname}|{eps}"
            res["machine_log"].append(dict(cell=key, **machine_state()))
            runs = {m: [] for m in METHODS}
            for r in range(reps):
                for m in METHODS[r % 3:] + METHODS[:r % 3]:
                    runs[m].append(all16(pool, f"{key}-{m}-{r}", case, m,
                                         (ROOT_C10, case.case_index, 3, 100 * eps_index + r), n_of[m], beta, eg,
                                         extra[m]))
                    with open(out / "rows.jsonl", "a", encoding="utf-8") as f:
                        f.write(json.dumps(dict(cell=key, method=m, rep=r, n=n_of[m], wall=runs[m][-1]["wall"],
                                                mean=runs[m][-1]["mean"], hw99=runs[m][-1]["hw99"])) + "\n")
            cell = dict(eps=eps, methods={})
            for m in METHODS:
                walls = [x["wall"] for x in runs[m]]
                sd = float(np.std(np.concatenate([x["scramble_means"] for x in runs[m]]), ddof=1))
                hw16 = T995_15 * sd / math.sqrt(SCRAMBLES)
                rr = r_cv if m == "preint_cv_fast" else r_h
                scale = max(1.0, (hw16 / (SHARE * eps)) ** (1 / rr))
                med = float(np.median(walls))
                cell["methods"][m] = dict(n_run=n_of[m], median_wall=med, primary_T_C=med * scale, scale=scale,
                                          pooled_hw16=hw16, fraction_hw_ok=float(np.mean(
                                              [x["hw99"] <= SHARE * eps for x in runs[m]])),
                                          mean_of_means=float(np.mean([x["mean"] for x in runs[m]])),
                                          walls=walls, label="meas")
            cell["speedup_vs_stageC"] = {m: cell["methods"]["preint"]["primary_T_C"] / cell["methods"][m]["primary_T_C"]
                                         for m in METHODS}
            res["cells"][key] = cell
            print(key, {m: (cell["methods"][m]["n_run"], round(cell["methods"][m]["primary_T_C"], 4),
                            round(cell["methods"][m]["fraction_hw_ok"], 2)) for m in METHODS},
                  "speedup", {m: round(v, 3) for m, v in cell["speedup_vs_stageC"].items()}, flush=True)
    res["machine_log"].append(dict(end=True, **machine_state()))
    with open(out / "c10_timing_cv.json", "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 20)
