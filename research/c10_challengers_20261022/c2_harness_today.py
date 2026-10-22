"""Re-time the unchanged Stage C C2 harness (c2_timing.all16 + timing.timed_scramble, method preint) today on
B8x52 $0.001 at n_run 2^17, 5 warm replications, C10 seed root. Separates machine state from harness differences.
Run: .context/frontier_t0_env/Scripts/python.exe -m research.c10_challengers_20261022.c2_harness_today <out_json>
"""
import research.frontier_classical_20261001.scrambles as sc  # noqa: I001

import json
import multiprocessing as mp
import sys

from research.frontier_classical_20261001.c2_timing import all16, machine_state
from research.frontier_classical_20261001.timing import wait_workers, warm_up


def main(out):
    case = sc.Case(1, 8, 52)
    st = machine_state()
    with mp.Pool(16, initializer=warm_up) as pool:
        wait_workers(pool, 16)
        runs = [all16(pool, f"c10h-{r}", case, "preint", 300 + r, 2 ** 17, purpose=3, root=2026102201)
                for r in range(5)]
    walls = sorted(r["wall"] for r in runs)
    res = dict(machine=st, walls=walls, median=walls[2], means=[r["mean"] for r in runs], label="meas")
    print(res["median"], walls, flush=True)
    with open(out, "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
