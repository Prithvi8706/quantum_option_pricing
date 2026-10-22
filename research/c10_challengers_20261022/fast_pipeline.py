"""C10 challenger pipeline pieces: uniforms -> normals -> log prices without changing the points.

* `ndtri_as241`: Wichura's AS241 PPND16 (Applied Statistics 37, 477 (1988)), relative accuracy about 1e-16, compiled.
* `kron_logprices`: x = z @ L.T + mu using L = (asset basis) (x) (time basis) column by column. The canonical
  factor's column k is u_{a(k)} (x) v_{t(k)} scaled by sqrt(lambda_a mu_t), so x reshaped to (na, nt) is
  A Z T^T with A = U diag(sqrt(lambda)), T = V diag(sqrt(mu)) and Z[a, t] = z[col(a, t)]. That is two small
  matrix products (na^2 nt + na nt^2 flops per point) instead of one (na nt)^2 product.
"""
import math

import numba
import numpy as np

from research.frontier_classical_20261001.basis import asset_basis, time_basis


@numba.njit(cache=True)
def _ppnd16(p):
    q = p - 0.5
    if abs(q) <= 0.425:
        r = 0.180625 - q * q
        return q * (((((((2509.0809287301226727 * r + 33430.575583588128105) * r + 67265.770927008700853) * r
                         + 45921.953931549871457) * r + 13731.693765509461125) * r + 1971.5909503065514427) * r
                      + 133.14166789178437745) * r + 3.387132872796366608) / \
            (((((((5226.495278852545925 * r + 28729.085735721942674) * r + 39307.89580009271061) * r
                 + 21213.794301586595867) * r + 5394.1960214247511077) * r + 687.1870074920579083) * r
              + 42.313330701600911252) * r + 1.0)
    r = p if q < 0 else 1.0 - p
    r = math.sqrt(-math.log(r))
    if r <= 5.0:
        r -= 1.6
        val = (((((((7.7454501427834140764e-4 * r + 0.0227238449892691845833) * r + 0.24178072517745061177) * r
                   + 1.27045825245236838258) * r + 3.64784832476320460504) * r + 5.7694972214606914055) * r
                + 4.6303378461565452959) * r + 1.42343711074968357734) / \
            (((((((1.05075007164441684324e-9 * r + 5.475938084995344946e-4) * r + 0.0151986665636164571966) * r
                 + 0.14810397642748007459) * r + 0.68976733498510000455) * r + 1.6763848301838038494) * r
              + 2.05319162663775882187) * r + 1.0)
    else:
        r -= 5.0
        val = (((((((2.01033439929228813265e-7 * r + 2.71155556874348757815e-5) * r + 0.0012426609473880784386) * r
                   + 0.026532189526576123093) * r + 0.29656057182850489123) * r + 1.7848265399172913358) * r
                + 5.4637849111641143699) * r + 6.6579046435011037772) / \
            (((((((2.04426310338993978564e-15 * r + 1.4215117583164458887e-7) * r + 1.8463183175100546818e-5) * r
                 + 7.868691311456132591e-4) * r + 0.0148753612908506148525) * r + 0.13692988092273580531) * r
              + 0.59983220655588793769) * r + 1.0)
    return -val if q < 0 else val


@numba.njit(cache=True)
def ndtri_as241(u, lo, hi):
    out = np.empty(u.shape)
    n, d = u.shape
    for i in range(n):
        for j in range(d):
            p = u[i, j]
            if p < lo:
                p = lo
            elif p > hi:
                p = hi
            out[i, j] = _ppnd16(p)
    return out


def kron_parts(na, nt, sigma, rho, maturity):
    """Return (perm, A, T): z[:, perm] reshaped (n, na, nt) gives Z[a, t]; A (na, na), T (nt, nt) scaled bases,
    with the same column order as basis.canonical_factor."""
    av, al = asset_basis(na, sigma, rho)
    tv, tl = time_basis(nt, maturity)
    a_idx, t_idx = np.meshgrid(np.arange(na), np.arange(nt), indexing="ij")
    a_idx, t_idx = a_idx.ravel(), t_idx.ravel()
    lam = al[a_idx] * tl[t_idx]
    order = np.lexsort((t_idx, a_idx, -lam))
    # canonical column k is (a_idx[order[k]], t_idx[order[k]]); position of (a, t) in that list:
    col_of = np.empty(na * nt, dtype=np.int64)
    col_of[order] = np.arange(na * nt)
    perm = col_of  # perm[a*nt + t] = canonical column index of (a, t)
    A = av * np.sqrt(al)[None, :]
    T = tv * np.sqrt(tl)[None, :]
    return perm, np.ascontiguousarray(A), np.ascontiguousarray(T)


def kron_logprices(z, perm, A, T, mu, na, nt):
    n = z.shape[0]
    Z = z[:, perm].reshape(n, na, nt)
    W = Z @ T.T                                   # (n, na, nt): sum_t Z[a, t] T[j, t]
    X = np.einsum("ia,naj->nij", A, W, optimize=True)  # (n, na, nt)
    return X.reshape(n, na * nt) + mu
