"""Scramble runner for Stage C rates (ANALYSIS_SPEC_STAGE_C.md, C1): every per-scramble
prefix mean is archived. BLAS threads are pinned to 1 before numpy is imported, as in P3,
because the eigh basis depends on the LAPACK thread count (ERRATA E10)."""

import os

for _k in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_k] = "1"

import math  # noqa: E402
import time  # noqa: E402
from dataclasses import asdict, dataclass  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
from scipy.special import ndtri  # noqa: E402
from scipy.stats import qmc  # noqa: E402

from research.frontier_classical_20261001.basis import canonical_factor, rotated_factor  # noqa: E402
from research.frontier_classical_20261001.kernels import six_estimands  # noqa: E402

CHUNK = 2 ** 12
M_MIN = 6
ROTATION_ROOT = 2026100101
ROOT = Path(__file__).resolve().parents[2]
ARCHIVED_8X52 = (ROOT / "results/frontier_replay_20261001/q0_attribution"
                 / "L_8x52_numpy1.26.4_single_thread.npy")
_FACTORS = {}


@dataclass(frozen=True)
class Case:
    case_index: int
    na: int
    nt: int
    spot: float = 100.0
    strike: float = 100.0
    barrier: float = 140.0
    sigma: float = 0.3
    rho: float = 0.4
    rate: float = 0.03
    maturity: float = 1.0

    @property
    def dim(self):
        return self.na * self.nt

    @property
    def name(self):
        return f"B{self.na}x{self.nt}_H{self.barrier:g}"


def eigh_factor(case):
    """P3's construction (numpy.linalg.eigh, sorted descending), for port validation only."""
    t = case.maturity * np.arange(1, case.nt + 1) / case.nt
    asset = case.sigma**2 * (case.rho * np.ones((case.na, case.na))
                             + (1 - case.rho) * np.eye(case.na))
    vals, vecs = np.linalg.eigh(np.kron(asset, np.minimum.outer(t, t)))
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    if vecs[:, 0].sum() < 0:
        vecs[:, 0] *= -1
    assert vecs[:, 0].min() > 0
    return np.ascontiguousarray(vecs * np.sqrt(np.clip(vals, 0, None)))


def factor(case, basis):
    """Spec section 0.2 bases: 'canonical'; 'eigh' (P3's construction, one BLAS thread);
    'archived' (the factor of the archived P3 run: numpy 1.26.4/MKL/one thread for 8x52,
    identical to 'eigh' for 4x12 per Q0); ('rotation', q), q = 1..4. Cached per process."""
    key = (case, basis)
    if key not in _FACTORS:
        if basis == "eigh" or (basis == "archived" and (case.na, case.nt) != (8, 52)):
            L = eigh_factor(case)
        elif basis == "archived":
            L = np.ascontiguousarray(np.load(ARCHIVED_8X52))
        else:
            L, groups = canonical_factor(case.na, case.nt, case.sigma, case.rho, case.maturity)
            if basis != "canonical":
                L = rotated_factor(L, groups, [ROTATION_ROOT, case.case_index, basis[1]])
        _FACTORS[key] = L
    return _FACTORS[key]


def drift(case):
    t = case.maturity * np.arange(1, case.nt + 1) / case.nt
    return np.log(case.spot) + np.tile((case.rate - case.sigma**2 / 2) * t, case.na)


def run_scramble(task):
    """task = (case, basis, seed_key, m_max): one scrambled Sobol sequence seeded by
    default_rng(seed_key) to 2^m_max points; prefix means of the six estimands."""
    case, basis, seed_key, m_max = task
    t0 = time.perf_counter()
    L = factor(case, basis)
    mu, v = drift(case), np.ascontiguousarray(L[:, 0])
    disc = math.exp(-case.rate * case.maturity)
    sampler = qmc.Sobol(case.dim, scramble=True, seed=np.random.default_rng(list(seed_key)))
    ms = list(range(M_MIN, m_max + 1))
    prefix = np.empty((6, len(ms)))
    elapsed = np.empty(len(ms))
    total, count = np.zeros(6), 0
    while count < 2 ** m_max:
        u = sampler.random(CHUNK)
        z = ndtri(np.clip(u, 1e-15, 1 - 1e-15))
        y = six_estimands(z @ L.T + mu, np.ascontiguousarray(z[:, 0]), v, case.na, case.nt, disc,
                          case.strike, case.barrier)
        cs = np.cumsum(y, axis=0)
        for i, m in enumerate(ms):
            n = 2 ** m
            if count < n <= count + CHUNK:
                prefix[:, i] = (total + cs[n - count - 1]) / n
                elapsed[i] = time.perf_counter() - t0
        total += cs[-1]
        count += CHUNK
    return dict(case=asdict(case), basis=basis if isinstance(basis, str) else list(basis),
                seed_key=list(seed_key), ms=ms, prefix=prefix, elapsed=elapsed.tolist(),
                seconds=time.perf_counter() - t0)
