"""Item C3 Ref B: plain iid Monte Carlo reference price (ANALYSIS_SPEC_STAGE_C.md, item C3).

Exact-date one-factor stepping (a common normal plus na idiosyncratic normals per date),
plain knock-out payoff, 16 CPU worker processes with PCG64 streams
SeedSequence([2026100131, case_index, 2, 0, worker]). Each case runs for a fixed budget of
6 machine wall-clock hours and stops there whatever the running difference. Run alone:
  python -m research.frontier_classical_20261001.c3_refb --case 0 --out <dir>
"""

import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import argparse
import json
import math
import multiprocessing as mp
import subprocess
import time
from pathlib import Path

import numba
import numpy as np

ROOT_C3 = 2026100131
WORKERS = 16
BUDGET_S = 6 * 3600
BATCH = 2 ** 15
CHECKPOINT_S = 600
CASES = {0: sc.Case(0, 4, 12), 1: sc.Case(1, 8, 52)}


@numba.njit(cache=True)
def plain_paths(z, na, nt, log_s0, drift, vol_common, vol_idio, disc, strike, barrier):
    """z: (n, nt*(na+1)) standard normals; date j uses z[:, j(na+1)] as the common factor
    and z[:, j(na+1)+1+i] for asset i. Returns the discounted plain knock-out payoff."""
    n = z.shape[0]
    out = np.empty(n)
    logs = np.empty(na)
    for p in range(n):
        for i in range(na):
            logs[i] = log_s0
        total = 0.0
        alive = True
        for j in range(nt):
            base = j * (na + 1)
            common = vol_common * z[p, base]
            basket = 0.0
            for i in range(na):
                logs[i] += drift + common + vol_idio * z[p, base + 1 + i]
                s = math.exp(logs[i])
                basket += s
            total += basket
            if basket / na >= barrier:
                alive = False
        avg = total / (na * nt)
        out[p] = disc * max(avg - strike, 0.0) if alive else 0.0
    return out


def worker(args):
    case, w, deadline, checkpoint = args
    rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence(
        [ROOT_C3, case.case_index, 2, 0, w])))
    dt = case.maturity / case.nt
    params = (case.na, case.nt, math.log(case.spot), (case.rate - case.sigma**2 / 2) * dt,
              case.sigma * math.sqrt(case.rho * dt), case.sigma * math.sqrt((1 - case.rho) * dt),
              math.exp(-case.rate * case.maturity), case.strike, case.barrier)
    n, sums, sqs, last = 0, [], [], time.time()
    while time.time() < deadline:
        y = plain_paths(rng.standard_normal((BATCH, case.nt * (case.na + 1))), *params)
        n += BATCH
        sums.append(float(y.sum()))
        sqs.append(float((y * y).sum()))
        if time.time() - last > CHECKPOINT_S:
            Path(checkpoint).write_text(json.dumps(dict(n=n, sum=math.fsum(sums),
                                                        sumsq=math.fsum(sqs))))
            last = time.time()
    state = dict(worker=w, n=n, sum=math.fsum(sums), sumsq=math.fsum(sqs))
    Path(checkpoint).write_text(json.dumps(state))
    return state


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", type=int, required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    case = CASES[args.case]
    out_dir = Path(args.out) / f"B{case.na}x{case.nt}"
    if out_dir.exists():
        raise SystemExit(f"refusing to overwrite {out_dir}")
    out_dir.mkdir(parents=True)
    plain_paths(np.zeros((1, case.nt * (case.na + 1))), case.na, case.nt, 4.6, 0.0, 0.1, 0.1,
                1.0, 100.0, 140.0)                     # compile once before the clock starts
    start = time.time()
    deadline = start + BUDGET_S
    with mp.Pool(WORKERS) as pool:
        rows = pool.map(worker, [(case, w, deadline, out_dir / f"worker{w}.json")
                                 for w in range(WORKERS)], chunksize=1)
    n = sum(r["n"] for r in rows)
    mean = math.fsum(r["sum"] for r in rows) / n
    var = (math.fsum(r["sumsq"] for r in rows) - n * mean * mean) / (n - 1)
    se = math.sqrt(var / n)
    result = dict(
        case=f"B{case.na}x{case.nt}", paths=n, price=mean, sd=math.sqrt(var), se=se,
        hw99=2.5758293035489004 * se, wall_seconds=time.time() - start, budget_seconds=BUDGET_S,
        workers=rows, commit=subprocess.run(["git", "rev-parse", "HEAD"], cwd=sc.ROOT,
                                            capture_output=True, text=True).stdout.strip())
    (out_dir / "ref_b.json").write_text(json.dumps(result, indent=1))
    print(json.dumps({k: v for k, v in result.items() if k != "workers"}))


if __name__ == "__main__":
    main()
