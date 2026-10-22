"""C10 challenger kernels (register C10/F06/F07, 22 Oct 2026).

`knockout_preint_fast` computes exactly the Stage C `preint` estimand (research/frontier_classical_20261001/
kernels.py::knockout_preint: first canonical PCA direction integrated in closed form) with less arithmetic. The first
canonical column is u_0 (x) v_1 with u_0 = 1/sqrt(na) constant across assets, so its loading v is constant within a
date, v[i*nt + j] = vdate[j]. Then:
  * each date's barrier root is closed form, z_j = (ln(na H) - ln sum_i e^{a_ij}) / vdate[j] (Stage C: 8 Newton
    steps over na terms per date);
  * the strike root is a Newton solve over nt date sums instead of na*nt coordinates;
  * the closed-form integral groups coordinates by date: 2 nt + 2 normal CDFs instead of 2 na nt + 2.
Same estimand, same points; only the arithmetic changes (agreement checked per point in `selfcheck`).
"""
import math

import numba
import numpy as np


@numba.njit(cache=True, fastmath=False)
def _ndtr(x):
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


@numba.njit(cache=True)
def knockout_preint_fast(x, z0, vdate, na, nt, disc, strike, barrier):
    """x: (n, na*nt) log prices (c = asset*nt + date); z0: first normal; vdate: (nt,) loading per date."""
    n = x.shape[0]
    dim = na * nt
    out = np.empty(n)
    bsum = np.empty(nt)
    ln_bar = math.log(na * barrier)
    ln_tgt = math.log(dim * strike)
    vbar = 0.0
    for j in range(nt):
        vbar += vdate[j]
    vbar /= nt
    for p in range(n):
        zp = z0[p]
        abar = 0.0
        for j in range(nt):
            s = 0.0
            for i in range(na):
                a = x[p, i * nt + j] - zp * vdate[j]
                abar += a
                s += math.exp(a)
            bsum[j] = s
        abar /= dim
        zh = math.inf
        for j in range(nt):
            r = (ln_bar - math.log(bsum[j])) / vdate[j]
            if r < zh:
                zh = r
        # strike root of sum_j bsum_j e^{vdate_j z} = dim K (Stage C's starting point, Newton in log form)
        z = (math.log(strike) - abar) / vbar
        for _ in range(60):
            s = 0.0
            ds = 0.0
            for j in range(nt):
                t = bsum[j] * math.exp(vdate[j] * z)
                s += t
                ds += t * vdate[j]
            step = (math.log(s) - ln_tgt) * s / ds
            z -= step
            if abs(step) < 1e-13 * (1.0 + abs(z)):
                break
        lo = z
        hi = zh if zh > z else z
        part = 0.0
        for j in range(nt):
            v = vdate[j]
            part += bsum[j] * math.exp(v * v / 2) * (_ndtr(hi - v) - _ndtr(lo - v))
        out[p] = disc * (part / dim - strike * (_ndtr(hi) - _ndtr(lo)))
    return out


@numba.njit(cache=True)
def preint_with_controls(x, z0, vdate, na, nt, disc, strike, barrier):
    """Columns: h (the Stage C preint estimand), and the preintegrated controls with closed-form means:
    geometric Asian call, linear average A, geometric-average knock-out (G < H). Same arithmetic as
    knockout_preint_fast for h."""
    n = x.shape[0]
    dim = na * nt
    out = np.empty((n, 4))
    bsum = np.empty(nt)
    ln_bar = math.log(na * barrier)
    ln_tgt = math.log(dim * strike)
    vbar = 0.0
    for j in range(nt):
        vbar += vdate[j]
    vbar /= nt
    for p in range(n):
        zp = z0[p]
        abar = 0.0
        for j in range(nt):
            s = 0.0
            for i in range(na):
                a = x[p, i * nt + j] - zp * vdate[j]
                abar += a
                s += math.exp(a)
            bsum[j] = s
        abar /= dim
        zh = math.inf
        for j in range(nt):
            r = (ln_bar - math.log(bsum[j])) / vdate[j]
            if r < zh:
                zh = r
        z = (math.log(strike) - abar) / vbar
        for _ in range(60):
            s = 0.0
            ds = 0.0
            for j in range(nt):
                t = bsum[j] * math.exp(vdate[j] * z)
                s += t
                ds += t * vdate[j]
            step = (math.log(s) - ln_tgt) * s / ds
            z -= step
            if abs(step) < 1e-13 * (1.0 + abs(z)):
                break
        lo = z
        hi = zh if zh > z else z
        part = 0.0
        lin = 0.0
        for j in range(nt):
            v = vdate[j]
            e = bsum[j] * math.exp(v * v / 2)
            part += e * (_ndtr(hi - v) - _ndtr(lo - v))
            lin += e
        out[p, 0] = disc * (part / dim - strike * (_ndtr(hi) - _ndtr(lo)))
        out[p, 2] = disc * lin / dim
        # ln G(z) = abar + vbar z
        zk = (math.log(strike) - abar) / vbar
        zu = (math.log(barrier) - abar) / vbar
        eg = math.exp(abar + vbar * vbar / 2)
        out[p, 1] = disc * (eg * _ndtr(vbar - zk) - strike * _ndtr(-zk))
        if zu > zk:
            out[p, 3] = disc * (eg * (_ndtr(zu - vbar) - _ndtr(zk - vbar)) - strike * (_ndtr(zu) - _ndtr(zk)))
        else:
            out[p, 3] = 0.0
    return out


@numba.njit(cache=True)
def preint_smooth2(x, z0, z1, vdate, w1, nodes, weights, na, nt, disc, strike, barrier):
    """Two-direction smoothing: the first canonical direction (date-constant loading vdate) is integrated in closed
    form as in knockout_preint_fast; a second direction with full loading vector w1 (dim,) is integrated by the
    given Gauss-Hermite rule for E over N(0,1): out = sum_q weights[q] h(x + (nodes[q] - z1) w1)."""
    n = x.shape[0]
    dim = na * nt
    out = np.empty(n)
    bsum = np.empty(nt)
    ln_bar = math.log(na * barrier)
    ln_tgt = math.log(dim * strike)
    vbar = 0.0
    for j in range(nt):
        vbar += vdate[j]
    vbar /= nt
    for p in range(n):
        acc = 0.0
        for q in range(nodes.shape[0]):
            shift = nodes[q] - z1[p]
            abar = 0.0
            for j in range(nt):
                s = 0.0
                for i in range(na):
                    c = i * nt + j
                    a = x[p, c] - z0[p] * vdate[j] + shift * w1[c]
                    abar += a
                    s += math.exp(a)
                bsum[j] = s
            abar /= dim
            zh = math.inf
            for j in range(nt):
                r = (ln_bar - math.log(bsum[j])) / vdate[j]
                if r < zh:
                    zh = r
            z = (math.log(strike) - abar) / vbar
            for _ in range(60):
                s = 0.0
                ds = 0.0
                for j in range(nt):
                    t = bsum[j] * math.exp(vdate[j] * z)
                    s += t
                    ds += t * vdate[j]
                step = (math.log(s) - ln_tgt) * s / ds
                z -= step
                if abs(step) < 1e-13 * (1.0 + abs(z)):
                    break
            lo = z
            hi = zh if zh > z else z
            part = 0.0
            for j in range(nt):
                v = vdate[j]
                part += bsum[j] * math.exp(v * v / 2) * (_ndtr(hi - v) - _ndtr(lo - v))
            acc += weights[q] * disc * (part / dim - strike * (_ndtr(hi) - _ndtr(lo)))
        out[p] = acc
    return out
