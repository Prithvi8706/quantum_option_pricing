"""Compiled per-point estimands for Stage C (ANALYSIS_SPEC_STAGE_C.md).

`knockout_preint` is P3's estimand (research/advantage_frontier_20260923/
barrier_fast_classical.py) with K and H as arguments instead of module constants; its
arithmetic is unchanged. `six_estimands` adds the plain payoffs and the call/digital
preintegration of P1 (classical_exponent_pilot.evaluate) for the C1 rate study only;
timing (C2) uses `knockout_preint` alone so that no extra payoff is charged to classical.
"""

import math

import numba
import numpy as np


@numba.njit(cache=True, fastmath=False)
def _ndtr(x):
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


@numba.njit(cache=True)
def _root(a, v, w, target, idx):
    """Newton root of sum_i w exp(a[idx_i] + v[idx_i] z) = target (P3 algorithm)."""
    num = 0.0
    den = 0.0
    for i in idx:
        num += a[i] * w
        den += v[i] * w
    z = (math.log(target) - num) / den
    for _ in range(8):
        s = 0.0
        ds = 0.0
        for i in idx:
            term = w * math.exp(a[i] + v[i] * z)
            s += term
            ds += term * v[i]
        step = (math.log(s) - math.log(target)) * s / ds
        z = z - step
        if abs(step) < 1e-13 * (1.0 + abs(z)):
            break
    return z


@numba.njit(cache=True)
def _date_index(na, nt):
    date_idx = np.empty((nt, na), dtype=np.int64)
    for j in range(nt):
        for i in range(na):
            date_idx[j, i] = i * nt + j
    return date_idx


@numba.njit(cache=True)
def knockout_preint(x, z0, v, na, nt, disc, strike, barrier):
    """x: (n, dim) log prices; z0: first normal. Preintegrated knock-out payoff per point."""
    n, dim = x.shape
    out = np.empty(n)
    a = np.empty(dim)
    all_idx = np.arange(dim)
    w_all = 1.0 / dim
    date_idx = _date_index(na, nt)
    for p in range(n):
        for c in range(dim):
            a[c] = x[p, c] - z0[p] * v[c]
        zs = _root(a, v, w_all, strike, all_idx)
        zh = math.inf
        for j in range(nt):
            r = _root(a, v, 1.0 / na, barrier, date_idx[j])
            if r < zh:
                zh = r
        lo = zs
        hi = zh if zh > zs else zs
        part = 0.0
        for c in range(dim):
            g = math.exp(a[c] + v[c] * v[c] / 2)
            part += w_all * g * (_ndtr(hi - v[c]) - _ndtr(lo - v[c]))
        out[p] = disc * (part - strike * (_ndtr(hi) - _ndtr(lo)))
    return out


ESTIMANDS = ("call", "digital", "knockout", "call_pre", "digital_pre", "knockout_pre")


@numba.njit(cache=True)
def six_estimands(x, z0, v, na, nt, disc, strike, barrier):
    """Columns in ESTIMANDS order: plain call, digital (100 * 1{A > K}), knock-out, and
    their first-direction preintegrated versions (P1 definitions)."""
    n, dim = x.shape
    out = np.empty((n, 6))
    a = np.empty(dim)
    all_idx = np.arange(dim)
    w_all = 1.0 / dim
    date_idx = _date_index(na, nt)
    for p in range(n):
        avg = 0.0
        alive = True
        for j in range(nt):
            b = 0.0
            for i in range(na):
                b += math.exp(x[p, date_idx[j, i]])
            avg += b
            if b / na >= barrier:
                alive = False
        avg /= dim
        out[p, 0] = disc * max(avg - strike, 0.0)
        out[p, 1] = disc * 100.0 * (1.0 if avg > strike else 0.0)
        out[p, 2] = out[p, 0] if alive else 0.0
        for c in range(dim):
            a[c] = x[p, c] - z0[p] * v[c]
        zs = _root(a, v, w_all, strike, all_idx)
        zh = math.inf
        for j in range(nt):
            r = _root(a, v, 1.0 / na, barrier, date_idx[j])
            if r < zh:
                zh = r
        hi = zh if zh > zs else zs
        call_part = 0.0
        ko_part = 0.0
        for c in range(dim):
            g = w_all * math.exp(a[c] + v[c] * v[c] / 2)
            call_part += g * _ndtr(v[c] - zs)
            ko_part += g * (_ndtr(hi - v[c]) - _ndtr(zs - v[c]))
        out[p, 3] = disc * (call_part - strike * _ndtr(-zs))
        out[p, 4] = disc * 100.0 * _ndtr(-zs)
        out[p, 5] = disc * (ko_part - strike * (_ndtr(hi) - _ndtr(zs)))
    return out
