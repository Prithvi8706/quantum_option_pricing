"""Canonical PCA factor of the basket log-price covariance (ANALYSIS_SPEC_STAGE_C.md, section 0).

The covariance is Sigma_asset (equicorrelation) kron Sigma_time (min(t_i, t_j)), indexed
c = asset * nt + date as in P1-P3. Its eigenvalues repeat, so numpy.linalg.eigh returns a
build-dependent basis (ERRATA E10). Here every eigenvector comes from a closed form:
  asset: 1/sqrt(na) and the Helmert basis of the (na-1)-fold eigenvalue sigma^2 (1 - rho);
  time:  v_k(i) = sin((2k-1) i pi / (2nt+1)), eigenvalue (T/nt) / (4 sin^2((2k-1) pi / (2(2nt+1)))).
Columns are sorted by eigenvalue, descending, ties broken by asset index, then time index.
"""

import numpy as np


def asset_basis(na, sigma, rho):
    """Orthonormal eigenvectors (columns) and eigenvalues of sigma^2 ((1-rho) I + rho 11^T)."""
    vecs = np.zeros((na, na))
    vecs[:, 0] = 1.0 / np.sqrt(na)
    for k in range(1, na):
        vecs[:k, k] = 1.0
        vecs[k, k] = -k
        vecs[:, k] /= np.sqrt(k * (k + 1))
    vals = np.full(na, sigma**2 * (1 - rho))
    vals[0] = sigma**2 * (1 + (na - 1) * rho)
    return vecs, vals


def time_basis(nt, maturity):
    """Orthonormal eigenvectors (columns) and eigenvalues of min(t_i, t_j), t_i = i T / nt."""
    i = np.arange(1, nt + 1)
    odd = 2 * np.arange(1, nt + 1) - 1
    vecs = np.sin(np.outer(i, odd) * np.pi / (2 * nt + 1))
    vecs /= np.linalg.norm(vecs, axis=0)
    vals = (maturity / nt) / (4 * np.sin(odd * np.pi / (2 * (2 * nt + 1))) ** 2)
    return vecs, vals


def canonical_factor(na, nt, sigma, rho, maturity):
    """Return (L, groups): L L^T = covariance, columns in canonical order; groups lists the
    column indices of each repeated eigenvalue (for rotation sensitivity)."""
    av, al = asset_basis(na, sigma, rho)
    tv, tl = time_basis(nt, maturity)
    a_idx, t_idx = np.meshgrid(np.arange(na), np.arange(nt), indexing="ij")
    a_idx, t_idx = a_idx.ravel(), t_idx.ravel()
    lam = al[a_idx] * tl[t_idx]
    order = np.lexsort((t_idx, a_idx, -lam))
    vecs = np.stack([np.kron(av[:, a], tv[:, t]) for a, t in zip(a_idx[order], t_idx[order])], 1)
    lam = lam[order]
    groups = []
    for t in range(nt):
        cols = [j for j, (a, tt) in enumerate(zip(a_idx[order], t_idx[order])) if tt == t and a > 0]
        if len(cols) > 1:
            groups.append(cols)
    return np.ascontiguousarray(vecs * np.sqrt(lam)), groups


def rotated_factor(L, groups, seed):
    """Apply a seeded Haar-random orthogonal rotation inside every repeated eigenspace."""
    rng = np.random.default_rng(seed)
    out = L.copy()
    for cols in groups:
        q, r = np.linalg.qr(rng.standard_normal((len(cols), len(cols))))
        q *= np.sign(np.diag(r))
        out[:, cols] = L[:, cols] @ q
    return out
