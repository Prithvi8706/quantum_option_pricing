"""Item C3 Ref A: time-ordered one-step-survival RQMC reference (ANALYSIS_SPEC_STAGE_C.md).

n = 2^22 points per scramble, 64 scrambles, keys [2026100131, case_index, 5, 0, s],
canonical asset basis. Run from a clean worktree in a non-timing slot:
  python -m research.frontier_classical_20261001.c3_refa --out <dir>
"""

import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import argparse
import json
import math
import multiprocessing as mp
import subprocess
import time
from pathlib import Path

import numpy as np
from scipy.stats import qmc
from scipy.stats import t as student_t

from research.frontier_classical_20261001.oss import oss_params, oss_paths

ROOT_C3 = 2026100131
SCRAMBLES, WORKERS, M_TOP = 64, 16, 22
DEV = (sc.Case(0, 4, 12), sc.Case(1, 8, 52))


def oss_scramble(task):
    case, s, m_top = task
    sampler = qmc.Sobol(case.dim, scramble=True,
                        seed=np.random.default_rng([ROOT_C3, case.case_index, 5, 0, s]))
    params = oss_params(case)
    total, count, prefix = 0.0, 0, {}
    while count < 2 ** m_top:
        cs = np.cumsum(oss_paths(sampler.random(sc.CHUNK), *params))
        for m in range(sc.M_MIN, m_top + 1):
            if count < 2 ** m <= count + sc.CHUNK:
                prefix[m] = (total + cs[2 ** m - count - 1]) / 2 ** m
        total += cs[-1]
        count += sc.CHUNK
    return prefix


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    out_dir = Path(ap.parse_args().out)
    if out_dir.exists():
        raise SystemExit(f"refusing to overwrite {out_dir}")
    out_dir.mkdir(parents=True)
    t995_63 = float(student_t.ppf(0.995, SCRAMBLES - 1))
    result = dict(commit=subprocess.run(["git", "rev-parse", "HEAD"], cwd=sc.ROOT,
                                        capture_output=True, text=True).stdout.strip(),
                  scrambles=SCRAMBLES, m_top=M_TOP, t995_63=t995_63, cases={})
    with mp.Pool(WORKERS) as pool:
        for case in DEV:
            t0 = time.time()
            rows = pool.map(oss_scramble, [(case, s, M_TOP) for s in range(SCRAMBLES)],
                            chunksize=1)
            ms = sorted(rows[0])
            prefix = np.array([[r[m] for m in ms] for r in rows])
            np.save(out_dir / f"B{case.na}x{case.nt}_oss_prefix.npy", prefix)
            final = prefix[:, -1]
            se = float(final.std(ddof=1) / math.sqrt(SCRAMBLES))
            result["cases"][f"B{case.na}x{case.nt}"] = dict(
                price=float(final.mean()), se=se, hw99=t995_63 * se, ms=ms,
                sd_one_scramble=prefix.std(0, ddof=1).tolist(), seconds=time.time() - t0)
            (out_dir / "ref_a.json").write_text(json.dumps(result, indent=1))
            print(json.dumps(result["cases"][f"B{case.na}x{case.nt}"])[:300], flush=True)


if __name__ == "__main__":
    main()
