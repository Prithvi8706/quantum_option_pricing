"""Item C2 worker functions (ANALYSIS_SPEC_STAGE_C.md, item C2).

Timed tasks record absolute `time.perf_counter()` stamps (QueryPerformanceCounter, a
system-wide clock on Windows), so the parent can measure from submission to the last
scramble. Each timed run builds the factor once per worker inside the timed interval.
"""

import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import math
import os
import time

import numpy as np
from scipy.special import ndtri
from scipy.stats import qmc

from research.frontier_classical_20261001.basis import canonical_factor
from research.frontier_classical_20261001.kernels import knockout_plain, knockout_preint
from research.frontier_classical_20261001.oss import (bridge_plan, oss_bb_dims, oss_bb_paths,
                                                      oss_params, oss_paths)

CHUNK = sc.CHUNK
_RUN_FACTOR = {}


def warm_up():
    """Pool initializer: load or compile every timed kernel in this worker (warm state)."""
    x = np.zeros((2, 48))
    knockout_preint(x, np.zeros(2), np.ones(48), 4, 12, 1.0, 100.0, 140.0)
    knockout_plain(x, 4, 12, 1.0, 100.0, 140.0)
    case = sc.Case(0, 4, 12)
    u = np.full((2, 48), 0.5)
    oss_paths(u, *oss_params(case))
    oss_bb_paths(u, *oss_params(case), bridge_plan(12), oss_bb_dims(4, 12))


def _factor(run_id, case, method):
    """Factor (preint/rqmc: canonical PCA; oss/oss_bb: canonical asset factor and bridge
    plan), built once per worker per timed run (spec item C1 pipeline)."""
    key = (run_id, case, method)
    if key not in _RUN_FACTOR:
        _RUN_FACTOR.clear()
        if method in ("oss", "oss_bb"):
            _RUN_FACTOR[key] = (oss_params(case), bridge_plan(case.nt),
                                oss_bb_dims(case.na, case.nt))
        else:
            L, _ = canonical_factor(case.na, case.nt, case.sigma, case.rho, case.maturity)
            _RUN_FACTOR[key] = L
    return _RUN_FACTOR[key]


def _estimate(method, case, L, mu, z):
    disc = math.exp(-case.rate * case.maturity)
    x = z @ L.T + mu
    if method == "preint":
        return knockout_preint(x, np.ascontiguousarray(z[:, 0]), np.ascontiguousarray(L[:, 0]),
                               case.na, case.nt, disc, case.strike, case.barrier)
    return knockout_plain(x, case.na, case.nt, disc, case.strike, case.barrier)


def _estimate_u(method, case, built, mu, u):
    """Per-point estimator from uniforms: OSS methods take uniforms directly; preint and
    rqmc apply the pinned ndtri -> GEMM pipeline."""
    if method == "oss":
        return oss_paths(u, *built[0])
    if method == "oss_bb":
        return oss_bb_paths(u, *built[0], built[1], built[2])
    return _estimate(method, case, built, mu, ndtri(np.clip(u, 1e-15, 1 - 1e-15)))


def timed_scramble(task):
    """One scramble to n_top points. Returns prefix means at every 2^m <= n_top (and at
    n_top), with the absolute clock at each mark and at task start."""
    run_id, case, method, seed_key, n_top = task
    t_start = time.perf_counter()
    built = _factor(run_id, case, method)
    mu = sc.drift(case)
    sampler = qmc.Sobol(case.dim, scramble=True, seed=np.random.default_rng(list(seed_key)))
    marks = sorted({2 ** m for m in range(sc.M_MIN, 30) if 2 ** m <= n_top} | {n_top})
    prefix, stamps = {}, {}
    total, count = 0.0, 0
    while count < n_top:
        size = min(CHUNK, n_top - count)
        y = _estimate_u(method, case, built, mu, sampler.random(size))
        cs = np.cumsum(y)
        for n in marks:
            if count < n <= count + size:
                prefix[n] = (total + cs[n - count - 1]) / n
                stamps[n] = time.perf_counter()
        total += cs[-1]
        count += size
    return dict(t_start=t_start, prefix=prefix, stamps=stamps)


def timed_chunk(task):
    """Load-balanced convention (iii): one 2^12-point chunk of one scramble, via fast_forward.
    Returns the chunk's sums at every sub-chunk mark (chunk 0) and its completion clock."""
    run_id, case, method, seed_key, chunk = task
    built = _factor(run_id, case, method)
    sampler = qmc.Sobol(case.dim, scramble=True, seed=np.random.default_rng(list(seed_key)))
    if chunk:
        sampler.fast_forward(chunk * CHUNK)
    cs = np.cumsum(_estimate_u(method, case, built, sc.drift(case), sampler.random(CHUNK)))
    sub = {2 ** m: float(cs[2 ** m - 1]) for m in range(sc.M_MIN, 13)} if chunk == 0 else {}
    return dict(chunk=chunk, seed_key=list(seed_key), total=float(cs[-1]), sub=sub,
                done=time.perf_counter())


def _worker_pid(_):
    time.sleep(0.2)
    return os.getpid()


def wait_workers(pool, workers):
    """Barrier for warm start: return once every worker has finished its initializer and run
    a task (Pool() returns before its initializers complete)."""
    seen = set()
    while len(seen) < workers:
        seen |= set(pool.map(_worker_pid, range(workers), chunksize=1))
    return len(seen)
