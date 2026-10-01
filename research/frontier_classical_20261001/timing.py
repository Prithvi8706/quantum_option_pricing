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

CHUNK = sc.CHUNK
_RUN_FACTOR = {}


def warm_up():
    """Pool initializer: load or compile both kernels in this worker (warm start state)."""
    x = np.zeros((2, 48))
    knockout_preint(x, np.zeros(2), np.ones(48), 4, 12, 1.0, 100.0, 140.0)
    knockout_plain(x, 4, 12, 1.0, 100.0, 140.0)


def _factor(run_id, case):
    """Canonical factor, built once per worker per timed run (spec item C1 pipeline)."""
    key = (run_id, case)
    if key not in _RUN_FACTOR:
        _RUN_FACTOR.clear()
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


def timed_scramble(task):
    """One scramble to n_top points. Returns prefix means at every 2^m <= n_top (and at
    n_top), with the absolute clock at each mark and at task start."""
    run_id, case, method, seed_key, n_top = task
    t_start = time.perf_counter()
    L = _factor(run_id, case)
    mu = sc.drift(case)
    sampler = qmc.Sobol(case.dim, scramble=True, seed=np.random.default_rng(list(seed_key)))
    marks = sorted({2 ** m for m in range(sc.M_MIN, 30) if 2 ** m <= n_top} | {n_top})
    prefix, stamps = {}, {}
    total, count = 0.0, 0
    while count < n_top:
        size = min(CHUNK, n_top - count)
        u = sampler.random(size)
        y = _estimate(method, case, L, mu, ndtri(np.clip(u, 1e-15, 1 - 1e-15)))
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
    L = _factor(run_id, case)
    sampler = qmc.Sobol(case.dim, scramble=True, seed=np.random.default_rng(list(seed_key)))
    if chunk:
        sampler.fast_forward(chunk * CHUNK)
    u = sampler.random(CHUNK)
    cs = np.cumsum(_estimate(method, case, L, sc.drift(case), ndtri(np.clip(u, 1e-15, 1 - 1e-15))))
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
