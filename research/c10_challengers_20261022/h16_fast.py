"""H16 re-measure: 1-worker / 16-worker wall ratio for Stage C preint and the C10 fast method (same points, warm).

The decision table's '1 lane vs 1 core' column multiplies T_C by this ratio (H16 grid run001, Stage C kernel). Here:
the four confirmation cells, 3 replications per (method, workers), all-16 convention as item C2.
Run (repo root, Stage C env without -I):
  .context/frontier_t0_env/Scripts/python.exe -m research.c10_challengers_20261022.h16_fast <out_dir>
"""
import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import json
import multiprocessing as mp
import sys
from pathlib import Path

import numpy as np

from research.frontier_classical_20261001.c2_timing import machine_state
from research.frontier_classical_20261001.timing import wait_workers
from research.c10_challengers_20261022 import run_timing as rt

ROOT_H16 = 2026102216
CELLS = rt.CELLS  # (case, eps, eps_index, n_run)
REPS = 3


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=False)
    res = dict(meta=dict(script="research/c10_challengers_20261022/h16_fast.py", python=sys.version, reps=REPS,
                         root=ROOT_H16), machine=[machine_state()], cells={})
    walls = {}
    for workers in (16, 1):
        with mp.Pool(workers, initializer=rt.warm_up) as pool:
            wait_workers(pool, workers)
            for case, eps, eps_index, n_run in CELLS:
                for m in ("preint", "preint_fast"):
                    w = [rt.all16(pool, f"h16-{workers}-{case.name}-{m}-{r}", case, m,
                                  (ROOT_H16, case.case_index, 1, 100 * eps_index + r), n_run)["wall"]
                         for r in range(REPS)]
                    walls[(case.name, eps, m, workers)] = float(np.median(w))
                    print(case.name, eps, m, workers, round(walls[(case.name, eps, m, workers)], 4), flush=True)
    for case, eps, _, n_run in CELLS:
        key = f"{case.name}|{eps}"
        res["cells"][key] = {m: dict(w1=walls[(case.name, eps, m, 1)], w16=walls[(case.name, eps, m, 16)],
                                     ratio_1_over_16=walls[(case.name, eps, m, 1)] / walls[(case.name, eps, m, 16)])
                             for m in ("preint", "preint_fast")}
        res["cells"][key]["n_run"] = n_run
    res["machine"].append(machine_state())
    res["label"] = "meas (median of 3 warm replications; Best-performance overlay today, CF absolute, ratios meas)"
    with open(out / "h16_fast.json", "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
