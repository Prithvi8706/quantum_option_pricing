"""Item C4: coverage of the 16-scramble preint interval (ANALYSIS_SPEC_STAGE_C.md).

`run` archives raw estimates: per development case, R = 1000 replications of 16 fresh
scrambles to 2^13 (nested prefixes give 2^10..2^13), keys [2026100141, case_index, 4, rep, s];
for 4x12 also replications 1000..1999 to 2^17. `score` computes coverage once the item C3
reference exists.
  python -m research.frontier_classical_20261001.c4_coverage --out <dir>
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
from scipy.special import ndtri
from scipy.stats import beta, qmc
from scipy.stats import t as student_t

from research.frontier_classical_20261001.basis import canonical_factor
from research.frontier_classical_20261001.kernels import knockout_preint

ROOT_C4 = 2026100141
R, SCRAMBLES, WORKERS = 1000, 16, 16
LEVELS = (10, 11, 12, 13)
DEV = (sc.Case(0, 4, 12), sc.Case(1, 8, 52))
_L = {}


def preint_scramble(task):
    """Prefix means of the preint knock-out estimand at 2^m for m in `levels`."""
    case, rep, s, levels = task
    if case not in _L:
        _L[case] = canonical_factor(case.na, case.nt, case.sigma, case.rho, case.maturity)[0]
    L, mu = _L[case], sc.drift(case)
    sampler = qmc.Sobol(case.dim, scramble=True,
                        seed=np.random.default_rng([ROOT_C4, case.case_index, 4, rep, s]))
    disc = math.exp(-case.rate * case.maturity)
    n_top = 2 ** max(levels)
    total, count, out = 0.0, 0, {}
    while count < n_top:
        size = min(sc.CHUNK, n_top)
        z = ndtri(np.clip(sampler.random(size), 1e-15, 1 - 1e-15))
        y = knockout_preint(z @ L.T + mu, np.ascontiguousarray(z[:, 0]),
                            np.ascontiguousarray(L[:, 0]), case.na, case.nt, disc,
                            case.strike, case.barrier)
        cs = np.cumsum(y)
        for m in levels:
            if count < 2 ** m <= count + size:
                out[m] = (total + cs[2 ** m - count - 1]) / 2 ** m
        total += cs[-1]
        count += size
    return [out[m] for m in levels]


def run_arm(pool, case, reps, levels):
    tasks = [(case, rep, s, levels) for rep in reps for s in range(SCRAMBLES)]
    rows = pool.map(preint_scramble, tasks, chunksize=SCRAMBLES)
    return np.array(rows).reshape(len(reps), SCRAMBLES, len(levels))


def score(estimates, levels, reference, ref_hw99, alpha_cells=18):
    """Raw and widened coverage of nominal 99% and 95% t-intervals, Clopper-Pearson 95%
    intervals, and the Bonferroni-level under-coverage check of the primary cell."""
    def cp(k, n, level=0.95):
        a = 1 - level
        lo = beta.ppf(a / 2, k, n - k + 1) if k > 0 else 0.0
        hi = beta.ppf(1 - a / 2, k + 1, n - k) if k < n else 1.0
        return [float(lo), float(hi)]
    out = {}
    means = estimates.mean(1)
    s = estimates.std(1, ddof=1)
    for j, m in enumerate(levels):
        cell = {}
        for nominal in (0.99, 0.95):
            t = float(student_t.ppf(1 - (1 - nominal) / 2, SCRAMBLES - 1))
            hw = t * s[:, j] / math.sqrt(SCRAMBLES)
            raw = np.abs(means[:, j] - reference) <= hw
            widened = np.abs(means[:, j] - reference) <= hw + ref_hw99
            k = int(raw.sum())
            cell[str(nominal)] = dict(
                raw=k / len(raw), raw_cp95=cp(k, len(raw)),
                widened=float(widened.mean()),
                reference_limited=bool(ref_hw99 > 0.25 * float(np.median(
                    float(student_t.ppf(0.975, SCRAMBLES - 1)) * s[:, j] / math.sqrt(SCRAMBLES)))),
                raw_cp_bonferroni=cp(k, len(raw), 1 - 0.05 / alpha_cells))
        q = np.abs(means[:, j] - reference) / (s[:, j] / math.sqrt(SCRAMBLES))
        cell["c_empirical_99"] = float(np.quantile(q, 0.99))
        out[str(2 ** m)] = cell
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    out_dir = Path(ap.parse_args().out)
    if out_dir.exists():
        raise SystemExit(f"refusing to overwrite {out_dir}")
    out_dir.mkdir(parents=True)
    meta = dict(commit=subprocess.run(["git", "rev-parse", "HEAD"], cwd=sc.ROOT,
                                      capture_output=True, text=True).stdout.strip(),
                replications=R, scrambles=SCRAMBLES, levels=LEVELS, seconds={})
    with mp.Pool(WORKERS) as pool:
        for case in DEV:
            name = f"B{case.na}x{case.nt}"
            t0 = time.time()
            np.save(out_dir / f"{name}_levels10to13.npy", run_arm(pool, case, range(R), LEVELS))
            meta["seconds"][name] = time.time() - t0
            (out_dir / "c4_raw.json").write_text(json.dumps(meta, indent=1))
        t0 = time.time()
        np.save(out_dir / "B4x12_level17.npy", run_arm(pool, DEV[0], range(R, 2 * R), (17,)))
        meta["seconds"]["B4x12_2^17"] = time.time() - t0
    (out_dir / "c4_raw.json").write_text(json.dumps(meta, indent=1))
    print("wrote", out_dir)


if __name__ == "__main__":
    main()
