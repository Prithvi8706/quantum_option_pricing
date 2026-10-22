"""Per-point agreement of knockout_preint_fast with the Stage C knockout_preint, and a one-process profile.

Run (repo root, Stage C environment without -I, numpy/numba/scipy):
  .context/frontier_t0_env/Scripts/python.exe -m research.c10_challengers_20261022.selfcheck <out_json>
"""
import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import json
import math
import sys
import time

import numpy as np
from scipy.special import ndtri
from scipy.stats import qmc

from research.frontier_classical_20261001.basis import canonical_factor
from research.frontier_classical_20261001.kernels import knockout_preint
from research.c10_challengers_20261022.fast_kernels import knockout_preint_fast


def main(out):
    res = {}
    for case in (sc.Case(0, 4, 12), sc.Case(1, 8, 52)):
        L, _ = canonical_factor(case.na, case.nt, case.sigma, case.rho, case.maturity)
        v = np.ascontiguousarray(L[:, 0])
        vdate = np.ascontiguousarray(v[:case.nt])
        assert np.max(np.abs(v.reshape(case.na, case.nt) - vdate[None, :])) < 1e-15
        mu = sc.drift(case)
        disc = math.exp(-case.rate * case.maturity)
        smp = qmc.Sobol(case.dim, scramble=True, seed=np.random.default_rng([2026102201, case.case_index, 0, 0, 0]))
        u = smp.random(2 ** 12)
        z = ndtri(np.clip(u, 1e-15, 1 - 1e-15))
        x = z @ L.T + mu
        z0 = np.ascontiguousarray(z[:, 0])
        old = knockout_preint(x, z0, v, case.na, case.nt, disc, case.strike, case.barrier)
        new = knockout_preint_fast(x, z0, vdate, case.na, case.nt, disc, case.strike, case.barrier)
        diff = np.abs(old - new)
        # profile one 2^12 chunk, single process (compiled already)
        prof = {}
        reps = 5
        t = time.perf_counter()
        for _ in range(reps):
            u = smp.random(2 ** 12)
        prof["sobol"] = (time.perf_counter() - t) / reps
        t = time.perf_counter()
        for _ in range(reps):
            z = ndtri(np.clip(u, 1e-15, 1 - 1e-15))
        prof["ndtri"] = (time.perf_counter() - t) / reps
        t = time.perf_counter()
        for _ in range(reps):
            x = z @ L.T + mu
        prof["gemm"] = (time.perf_counter() - t) / reps
        z0 = np.ascontiguousarray(z[:, 0])
        t = time.perf_counter()
        for _ in range(reps):
            knockout_preint(x, z0, v, case.na, case.nt, disc, case.strike, case.barrier)
        prof["kernel_stageC"] = (time.perf_counter() - t) / reps
        t = time.perf_counter()
        for _ in range(reps):
            knockout_preint_fast(x, z0, vdate, case.na, case.nt, disc, case.strike, case.barrier)
        prof["kernel_fast"] = (time.perf_counter() - t) / reps
        res[case.name] = dict(n=int(len(old)), max_abs_diff=float(diff.max()),
                              max_rel_diff=float(np.max(diff / np.maximum(np.abs(old), 1e-300))),
                              mean_old=float(old.mean()), mean_new=float(new.mean()),
                              profile_s_per_chunk=prof,
                              label="meas (one process, one 2^12 chunk, warm)")
        print(case.name, res[case.name])
    with open(out, "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
