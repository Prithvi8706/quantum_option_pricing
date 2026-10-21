"""Item C5: stronger classical smoothers, OSS-BB (primary) and time-ordered OSS
(ANALYSIS_SPEC_STAGE_C.md, item C5).

  rates (non-timing slot):
    python -m research.frontier_classical_20261001.c5_smoothers rates --out <dir>
  timing (exclusive slot):
    python -m research.frontier_classical_20261001.c5_smoothers timing --out <dir> --rates <json>
Rates use 32 scrambles to 2^19, keys [2026100151, case_index, 0, 0, s]; timing reuses the
item C2 protocol (`c2_timing.run_block`) with the C5 rate fits.
"""

import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import argparse
import json
import multiprocessing as mp
import time
from pathlib import Path

import numpy as np
from scipy.stats import qmc

from research.frontier_classical_20261001 import c2_timing
from research.frontier_classical_20261001.fit import summarize
from research.frontier_classical_20261001.provenance import meta, require_clean
from research.frontier_classical_20261001.oss import (bridge_plan, oss_bb_dims, oss_bb_paths,
                                                      oss_params, oss_paths)

ROOT_C5 = 2026100151
SCRAMBLES, WORKERS, M_TOP = 32, 16, 19
METHODS = ("oss_bb", "oss")
DEV = (sc.Case(0, 4, 12), sc.Case(1, 8, 52))


def smoother_scramble(task):
    case, method, s = task
    sampler = qmc.Sobol(case.dim, scramble=True,
                        seed=np.random.default_rng([ROOT_C5, case.case_index, 0, 0, s]))
    params = oss_params(case)
    plan, dims = bridge_plan(case.nt), oss_bb_dims(case.na, case.nt)
    ms = list(range(sc.M_MIN, M_TOP + 1))
    prefix = np.empty(len(ms))
    total, count = 0.0, 0
    while count < 2 ** M_TOP:
        u = sampler.random(sc.CHUNK)
        y = oss_bb_paths(u, *params, plan, dims) if method == "oss_bb" else oss_paths(u, *params)
        cs = np.cumsum(y)
        for i, m in enumerate(ms):
            if count < 2 ** m <= count + sc.CHUNK:
                prefix[i] = (total + cs[2 ** m - count - 1]) / 2 ** m
        total += cs[-1]
        count += sc.CHUNK
    return prefix


def rates(out_dir):
    result = {}
    with mp.Pool(WORKERS) as pool:
        for case in DEV:
            name = f"B{case.na}x{case.nt}"
            for method in METHODS:
                t0 = time.time()
                prefix = np.array(pool.map(smoother_scramble,
                                           [(case, method, s) for s in range(SCRAMBLES)],
                                           chunksize=1))
                np.save(out_dir / f"{name}_{method}.npy", prefix)
                ms = list(range(sc.M_MIN, M_TOP + 1))
                result[f"{name}/{method}"] = dict(summary=summarize(ms, prefix, case.case_index),
                                                  seconds=time.time() - t0)
                (out_dir / "c5_rates.json").write_text(json.dumps(result, indent=1))
                print(name, method, round(result[f"{name}/{method}"]["summary"]["fits"]
                                          ["primary"]["r"], 3), flush=True)
    return result


def timing(out_dir, rates_path):
    rates_summary = json.loads(Path(rates_path).read_text())
    log, result = [], {}
    for case in DEV:
        name = f"B{case.na}x{case.nt}"
        for method in METHODS:
            est = rates_summary[f"{name}/{method}"]["summary"]
            result[f"{name}/{method}"] = c2_timing.run_block(case, method, est, log,
                                                             root=ROOT_C5)
            (out_dir / "c5_timing.json").write_text(json.dumps(
                dict(machine_log=log, blocks=result), indent=1, default=str))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=("rates", "timing"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--rates")
    args = ap.parse_args()
    if args.phase == "timing" and not args.rates:
        ap.error("the timing phase needs --rates <c5_rates.json>")
    require_clean()
    out_dir = Path(args.out) / args.phase
    if out_dir.exists():
        raise SystemExit(f"refusing to overwrite {out_dir}")
    out_dir.mkdir(parents=True)
    (out_dir / "meta.json").write_text(json.dumps(meta(phase=args.phase, root=ROOT_C5), indent=1))
    if args.phase == "rates":
        rates(out_dir)
    else:
        timing(out_dir, args.rates)


if __name__ == "__main__":
    main()
