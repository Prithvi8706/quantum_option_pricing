"""Item C2: timing and measured time to accuracy (ANALYSIS_SPEC_STAGE_C.md).

Run from a clean detached worktree of a committed revision, after item C1, on an idle machine:
  python -m research.frontier_classical_20261001.c2_timing --c1 <c1_summary.json> --out <dir>
"""

import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import argparse
import hashlib
import json
import math
import multiprocessing as mp
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
from scipy.stats import t as student_t

from research.frontier_classical_20261001.fit import EPS, SHARE, T995_15
from research.frontier_classical_20261001.timing import (CHUNK, timed_chunk, timed_scramble,
                                                         wait_workers, warm_up)

ROOT_C2 = 2026100121
WORKERS, LB_WORKERS, SCRAMBLES = 16, 22, 16
N_TOP = 2 ** 19
WARM, FRESH, COLD, LB = range(0, 5), 5, 6, range(10, 15)
REPLICATIONS = 20
METHODS = {"preint": "knockout_pre", "rqmc": "knockout"}
DEV = (sc.Case(0, 4, 12), sc.Case(1, 8, 52))
SPEC = "manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_C.md"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def powershell(cmd):
    return subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True,
                          text=True).stdout.strip()


def machine_state():
    """30 s CPU average, other python processes' CPU use, and AC/battery status."""
    cpu = powershell("(Get-Counter '\\Processor(_Total)\\% Processor Time' -SampleInterval 1 "
                     "-MaxSamples 30).CounterSamples.CookedValue | Measure-Object -Average | "
                     "ForEach-Object { $_.Average }")
    procs = powershell("$a = Get-Process python -ErrorAction SilentlyContinue | "
                       "Select-Object Id,CPU; Start-Sleep 5; $b = Get-Process python "
                       "-ErrorAction SilentlyContinue | Select-Object Id,CPU; foreach ($p in $b) "
                       "{ $o = $a | Where-Object Id -eq $p.Id; if ($o) { '{0} {1:N2}' -f $p.Id, "
                       "($p.CPU - $o.CPU) } }")
    busy = [line for line in procs.splitlines()
            if line.split()[0] != str(os.getpid()) and float(line.split()[1]) > 0.5]
    battery = powershell("(Get-CimInstance Win32_Battery).BatteryStatus")
    try:
        cpu_avg = float(cpu)
    except ValueError:
        cpu_avg = None
    return dict(cpu_percent_30s=cpu_avg, busy_python=busy, battery_status=battery,
                idle=cpu_avg is not None and cpu_avg < 10 and not busy)


def wait_idle(log, max_wait_s=7200):
    t0 = time.time()
    while True:
        state = machine_state()
        if state["idle"] or time.time() - t0 > max_wait_s:
            state["waited_s"] = round(time.time() - t0)
            log.append(state)
            return state
        time.sleep(60)


def all16(pool, run_id, case, method, replication, n_top, purpose=1, submit=None):
    """Convention (ii) and (i) from one 16-scramble run. `submit` lets fresh/cold runs start
    their clock before the pool is created."""
    tasks = [(run_id, case, method, (ROOT_C2, case.case_index, purpose, replication, s), n_top)
             for s in range(SCRAMBLES)]
    submit = time.perf_counter() if submit is None else submit
    rows = pool.map(timed_scramble, tasks, chunksize=1)
    means = np.array([r["prefix"][n_top] for r in rows])
    hw = T995_15 * means.std(ddof=1) / math.sqrt(SCRAMBLES)
    end = time.perf_counter()
    marks = sorted(rows[0]["stamps"])
    return dict(
        n_top=n_top, wall=end - submit, mean=float(means.mean()), hw99=float(hw),
        scramble_means=means.tolist(),
        all16={n: max(r["stamps"][n] for r in rows) - submit for n in marks},
        per_scramble_median={n: float(np.median([r["stamps"][n] - r["t_start"] for r in rows]))
                             for n in marks})


def load_balanced(pool, run_id, case, method, replication, n_top):
    chunks = n_top // CHUNK
    tasks = [(run_id, case, method, (ROOT_C2, case.case_index, 1, replication, s), c)
             for c in range(chunks) for s in range(SCRAMBLES)]
    submit = time.perf_counter()
    rows = list(pool.imap_unordered(timed_chunk, tasks, chunksize=1))
    end = time.perf_counter()
    marks = [2 ** m for m in range(sc.M_MIN, 20) if 2 ** m <= n_top]
    elapsed = {n: max(r["done"] for r in rows if r["chunk"] < max(1, n // CHUNK)) - submit
               for n in marks}
    totals = {}
    for r in rows:
        totals[r["seed_key"][-1]] = totals.get(r["seed_key"][-1], 0.0) + r["total"]
    return dict(n_top=n_top, wall=end - submit, all16=elapsed,
                mean=float(np.mean([v / n_top for v in totals.values()])))


def fit_ab(per_mark):
    """OLS T(n) = a + b n on per-mark medians over repeats, marks n >= 2^13."""
    ns = sorted(n for n in per_mark if n >= 2 ** 13)
    b, a = np.polyfit(np.array(ns, dtype=float), np.array([per_mark[n] for n in ns]), 1)
    return float(a), float(b)


def medians(runs, key):
    marks = runs[0][key].keys()
    return {n: float(np.median([r[key][n] for r in runs])) for n in marks}


def t_c(block, c1_est, eps):
    """Primary T_C(eps) and its sensitivities for one (case, method), by the spec's rules."""
    n = c1_est["n_eps"][str(eps)]["point"]
    r = c1_est["fits"]["primary"]["r"]
    warm_all16 = medians(block["warm"], "all16")
    a, b = block["fits"]["all16"]
    model = a + b * n
    out = dict(n_eps=n, model_all16_unrounded=model,
               model_per_scramble_median=sum(x * y for x, y in zip(block["fits"]["per_scramble"],
                                                                    (1, n))),
               model_load_balanced=sum(x * y for x, y in zip(block["fits"]["load_balanced"],
                                                             (1, n))))
    conf = block["confirmation"].get(str(eps))
    if conf:
        sd = np.std(np.concatenate([c["scramble_means"] for c in conf["runs"]]), ddof=1)
        hw16 = T995_15 * sd / math.sqrt(SCRAMBLES)
        wall = float(np.median([c["wall"] for c in conf["runs"]]))
        scale = max(1.0, (hw16 / (SHARE * eps)) ** (1 / r))
        out.update(primary=wall * scale, convention="measured confirmation",
                   n_run=conf["n_run"], median_wall=wall, pooled_hw16=float(hw16),
                   scale=scale, fraction_hw_ok=float(np.mean([c["hw99"] <= SHARE * eps
                                                              for c in conf["runs"]])))
    elif n < 2 ** 13:
        mark = min(m for m in warm_all16 if m >= max(n, 2 ** 6))
        out.update(primary=warm_all16[mark], convention="measured small-n mark", mark=mark)
    else:
        out.update(primary=model, convention="modelled all-16")
    fresh = block["fresh"]["all16"]
    mark = min((m for m in fresh if m >= max(n, 2 ** 6)), default=max(fresh))
    out["fresh_cached"] = out["primary"] + fresh[mark] - warm_all16[mark]
    return out


def run_block(case, method, c1_est, log):
    run = f"{case.case_index}-{method}"
    block = dict(machine=wait_idle(log))
    with mp.Pool(WORKERS, initializer=warm_up) as pool:
        wait_workers(pool, WORKERS)
        block["warm"] = [all16(pool, f"{run}-w{r}", case, method, r, N_TOP) for r in WARM]
        block["confirmation"] = {}
        for eps_index, eps in enumerate(EPS):
            n = c1_est["n_eps"][str(eps)]["point"]
            if eps not in (0.01, 0.001) or n > 2 ** 21:
                continue
            n_run = 2 ** math.ceil(math.log2(n))
            runs = [all16(pool, f"{run}-c{eps_index}-{k}", case, method, 100 * eps_index + k,
                          n_run, purpose=3) for k in range(REPLICATIONS)]
            block["confirmation"][str(eps)] = dict(n_run=n_run, runs=runs)
    start = time.perf_counter()
    with mp.Pool(WORKERS) as pool:
        block["fresh"] = all16(pool, f"{run}-fresh", case, method, FRESH, N_TOP, submit=start)
    cache = tempfile.mkdtemp(prefix="numba_cold_")
    old = os.environ.get("NUMBA_CACHE_DIR")
    os.environ["NUMBA_CACHE_DIR"] = cache
    start = time.perf_counter()
    with mp.Pool(WORKERS) as pool:
        block["cold"] = all16(pool, f"{run}-cold", case, method, COLD, N_TOP, submit=start)
    if old is None:
        os.environ.pop("NUMBA_CACHE_DIR")
    else:
        os.environ["NUMBA_CACHE_DIR"] = old
    with mp.Pool(LB_WORKERS, initializer=warm_up) as pool:
        wait_workers(pool, LB_WORKERS)
        block["load_balanced"] = [load_balanced(pool, f"{run}-lb{r}", case, method, r, N_TOP)
                                  for r in LB]
    block["fits"] = dict(all16=fit_ab(medians(block["warm"], "all16")),
                         per_scramble=fit_ab(medians(block["warm"], "per_scramble_median")),
                         load_balanced=fit_ab(medians(block["load_balanced"], "all16")))
    block["t_c"] = {str(eps): t_c(block, c1_est, eps) for eps in EPS}
    return block


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--c1", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out_dir = Path(args.out)
    if out_dir.exists():
        raise SystemExit(f"refusing to overwrite {out_dir}")
    out_dir.mkdir(parents=True)
    c1 = json.loads(Path(args.c1).read_text())
    meta = dict(
        commit=subprocess.run(["git", "rev-parse", "HEAD"], cwd=sc.ROOT, capture_output=True,
                              text=True).stdout.strip(),
        dirty=bool(subprocess.run(["git", "status", "--porcelain"], cwd=sc.ROOT,
                                  capture_output=True, text=True).stdout.strip()),
        spec_sha256=sha(sc.ROOT / SPEC), c1_summary_sha256=sha(args.c1),
        code_sha256={p.name: sha(p) for p in sorted(Path(__file__).parent.glob("*.py"))},
        python=sys.version, numpy=np.__version__, workers=WORKERS, lb_workers=LB_WORKERS,
        t995_15=T995_15, t99_31=float(student_t.ppf(0.99, 31)),
        cpu=powershell("(Get-CimInstance Win32_Processor).Name"),
        power_plan=subprocess.run(["powercfg", "/getactivescheme"], capture_output=True,
                                  text=True).stdout.strip(), affinity="none set")
    log, result = [], {}
    for case in DEV:
        name = f"B{case.na}x{case.nt}"
        for method, est in METHODS.items():
            c1_est = c1["cases"][name]["summary"]["canonical"][est]
            result[f"{name}/{method}"] = run_block(case, method, c1_est, log)
            (out_dir / "c2_timing.json").write_text(json.dumps(
                dict(meta=meta, machine_log=log, blocks=result), indent=1, default=str))
            print(name, method, {e: round(v["primary"], 3)
                                 for e, v in result[f"{name}/{method}"]["t_c"].items()}, flush=True)
    print("wrote", out_dir)


if __name__ == "__main__":
    main()
