"""C10 candidate: float32 GEMM (z @ L^T in single precision, everything else float64). Stage C admits float32 only if
it passes eps/10 (spec item C6 rule). Paired check on Sobol points: per-point and mean differences against float64,
plus a one-process profile of the GEMM.
Run (repo root, Stage C env without -I):
  .context/frontier_t0_env/Scripts/python.exe -m research.c10_challengers_20261022.f32_check <out_json>
"""
import research.frontier_classical_20261001.scrambles as sc  # noqa: I001

import json
import math
import sys
import time

import numpy as np
from scipy.stats import qmc

from research.frontier_classical_20261001.basis import canonical_factor
from research.c10_challengers_20261022.fast_kernels import knockout_preint_fast
from research.c10_challengers_20261022.fast_pipeline import ndtri_as241


def main(out):
    res = {}
    for case in (sc.Case(0, 4, 12), sc.Case(1, 8, 52)):
        L, _ = canonical_factor(case.na, case.nt, case.sigma, case.rho, case.maturity)
        L32 = np.ascontiguousarray(L.T.astype(np.float32))
        mu = sc.drift(case)
        vdate = np.ascontiguousarray(L[:, 0][:case.nt])
        disc = math.exp(-case.rate * case.maturity)
        smp = qmc.Sobol(case.dim, scramble=True, seed=np.random.default_rng([2026102232, case.case_index, 0, 0, 0]))
        d_all, s64, s32 = [], 0.0, 0.0
        for _ in range(16):
            z = ndtri_as241(smp.random(4096), 1e-15, 1 - 1e-15)
            z0 = np.ascontiguousarray(z[:, 0])
            x64 = z @ L.T + mu
            x32 = (z.astype(np.float32) @ L32).astype(np.float64) + mu
            y64 = knockout_preint_fast(x64, z0, vdate, case.na, case.nt, disc, case.strike, case.barrier)
            y32 = knockout_preint_fast(x32, z0, vdate, case.na, case.nt, disc, case.strike, case.barrier)
            d_all.append(y32 - y64)
            s64 += y64.sum()
            s32 += y32.sum()
        d = np.concatenate(d_all)
        z = ndtri_as241(smp.random(4096), 1e-15, 1 - 1e-15)
        z32 = z.astype(np.float32)
        t = time.perf_counter()
        for _ in range(10):
            z @ L.T + mu
        g64 = (time.perf_counter() - t) / 10
        t = time.perf_counter()
        for _ in range(10):
            (z32 @ L32).astype(np.float64) + mu
        g32 = (time.perf_counter() - t) / 10
        res[case.name] = dict(n=int(d.size), max_abs_point_diff=float(np.abs(d).max()), mean_diff=float(d.mean()),
                              mean_abs_diff=float(np.abs(d).mean()), eps_over_10_at_0001=1e-4,
                              passes_eps_over_10=bool(abs(d.mean()) < 1e-4 and np.abs(d).max() < 1e-3),
                              gemm_ms_f64=g64 * 1e3, gemm_ms_f32=g32 * 1e3, label="meas")
        print(case.name, res[case.name], flush=True)
    with open(out, "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
